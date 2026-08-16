"""Fase 0 - inventario empirico dello schema XML Deluge.

Attraversa un insieme di file XML e produce, per ogni PATH di elemento
(es. song/sessionClips/instrumentClip/noteRows/noteRow):

  - quante volte compare, in quanti file
  - i figli osservati e la loro cardinalita' (min/max per genitore)
  - gli attributi osservati: frequenza, tipo inferito, range o enum dei valori
  - se l'elemento ha testo (contenuto misto / valore scalare)

Tutto quello che finisce nel report e' OSSERVATO. Nessuna inferenza sullo
schema "legale": solo su cosa e' presente nei file dati in input.

Uso:
    python extract_schema.py <dir_o_file> [...] --json out.json --md out.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file          # noqa: E402

# ---------------------------------------------------------------- tipi valore

HEX32_RE = re.compile(r'^0x[0-9A-Fa-f]{8}$')
HEXBLOB_RE = re.compile(r'^[0-9A-Fa-f]{16,}$')
INT_RE = re.compile(r'^-?\d+$')
FLOAT_RE = re.compile(r'^-?\d+\.\d+$')

# valore massimo di enum distinti prima di trattare l'attributo come "libero"
ENUM_MAX = 24
# quanti esempi conservare per gli attributi non-enum
SAMPLE_MAX = 5


def classify(v: str) -> str:
    if HEX32_RE.match(v):
        return 'hex32'
    if INT_RE.match(v):
        return 'int'
    if FLOAT_RE.match(v):
        return 'float'
    if HEXBLOB_RE.match(v):
        return 'hexblob'
    return 'string'


class AttrStat:
    __slots__ = ('count', 'types', 'values', 'overflow', 'imin', 'imax',
                 'samples', 'maxlen')

    def __init__(self):
        self.count = 0
        self.types = Counter()
        self.values = Counter()      # usato finche' non supera ENUM_MAX
        self.overflow = False
        self.imin = None
        self.imax = None
        self.samples = []
        self.maxlen = 0

    def add(self, v: str):
        self.count += 1
        t = classify(v)
        self.types[t] += 1
        self.maxlen = max(self.maxlen, len(v))
        if t == 'int':
            i = int(v)
            self.imin = i if self.imin is None else min(self.imin, i)
            self.imax = i if self.imax is None else max(self.imax, i)
        if not self.overflow:
            self.values[v] += 1
            if len(self.values) > ENUM_MAX:
                self.overflow = True
                self.values.clear()
        if len(self.samples) < SAMPLE_MAX and v not in self.samples:
            self.samples.append(v)

    def to_dict(self):
        d = {
            'count': self.count,
            'types': dict(self.types.most_common()),
            'max_len': self.maxlen,
        }
        if self.imin is not None:
            d['int_range'] = [self.imin, self.imax]
        if not self.overflow:
            d['enum'] = dict(self.values.most_common())
        else:
            d['samples'] = self.samples
        return d


class NodeStat:
    __slots__ = ('count', 'files', 'attrs', 'children', 'child_card',
                 'has_text', 'text', 'attr_order')

    def __init__(self):
        self.count = 0
        self.files = set()
        self.attrs = defaultdict(AttrStat)
        self.children = Counter()
        self.child_card = defaultdict(lambda: [None, 0])  # tag -> [min, max]
        self.has_text = 0
        self.text = AttrStat()
        self.attr_order = Counter()   # tuple ordinata degli attributi

    def to_dict(self):
        return {
            'count': self.count,
            'n_files': len(self.files),
            'attrs': {k: v.to_dict() for k, v in sorted(self.attrs.items())},
            'attr_orders': [
                {'order': list(k), 'count': n}
                for k, n in self.attr_order.most_common(3)
            ],
            'children': {
                tag: {'total': n,
                      'per_parent_min': self.child_card[tag][0],
                      'per_parent_max': self.child_card[tag][1]}
                for tag, n in self.children.most_common()
            },
            'text_count': self.has_text,
            'text': self.text.to_dict() if self.has_text else None,
        }


def walk(elem, path: str, stats: dict, fname: str):
    st = stats.setdefault(path, NodeStat())
    st.count += 1
    st.files.add(fname)

    if elem.attrs:
        st.attr_order[tuple(k for k, _ in elem.attrs)] += 1
    for k, v in elem.attrs:
        st.attrs[k].add(v)

    txt = (elem.text or '').strip()
    if txt:
        st.has_text += 1
        st.text.add(txt)

    local = Counter(c.tag for c in elem.children)
    for tag, n in local.items():
        st.children[tag] += n
        card = st.child_card[tag]
        card[0] = n if card[0] is None else min(card[0], n)
        card[1] = max(card[1], n)
    # i figli assenti abbassano il minimo a 0
    for tag in list(st.child_card):
        if tag not in local:
            st.child_card[tag][0] = 0

    for child in elem.children:
        walk(child, f'{path}/{child.tag}', stats, fname)


def collect_files(inputs) -> list[Path]:
    out = []
    for i in inputs:
        p = Path(i)
        if p.is_dir():
            out += [q for q in sorted(p.rglob('*'))
                    if q.is_file() and q.suffix.lower() == '.xml'
                    and not q.name.startswith('._')]
        elif p.is_file():
            out.append(p)
    return out


def render_md(stats: dict, files: list[Path]) -> str:
    L = []
    L.append('# Inventario schema XML Deluge (osservato)\n')
    L.append(f'File analizzati: **{len(files)}**\n')
    L.append('<details><summary>elenco file</summary>\n')
    for f in files:
        L.append(f'- `{f}`')
    L.append('\n</details>\n')
    L.append(f'Path di elemento distinti: **{len(stats)}**\n')
    L.append('---\n')

    for path in sorted(stats):
        st = stats[path]
        L.append(f'## `{path}`\n')
        L.append(f'occorrenze: {st.count} — file: {len(st.files)}\n')

        if st.attrs:
            L.append('| attributo | n | tipi | range / valori |')
            L.append('|---|---:|---|---|')
            for name, a in sorted(st.attrs.items()):
                types = ', '.join(f'{t}' for t in a.types)
                if not a.overflow:
                    vals = ', '.join(f'`{v}`' for v, _ in a.values.most_common(ENUM_MAX))
                    dom = f'enum({len(a.values)}): {vals}'
                elif a.imin is not None:
                    dom = f'int [{a.imin} … {a.imax}]'
                else:
                    dom = 'es. ' + ', '.join(f'`{s[:40]}`' for s in a.samples)
                L.append(f'| `{name}` | {a.count} | {types} | {dom} |')
            L.append('')

        if st.has_text:
            a = st.text
            if not a.overflow:
                dom = 'enum: ' + ', '.join(f'`{v}`' for v, _ in a.values.most_common(ENUM_MAX))
            elif a.imin is not None:
                dom = f'int [{a.imin} … {a.imax}]'
            else:
                dom = 'es. ' + ', '.join(f'`{s[:40]}`' for s in a.samples)
            L.append(f'**testo**: {st.has_text} occorrenze — {dom}\n')

        if st.children:
            L.append('| figlio | totale | per genitore (min–max) |')
            L.append('|---|---:|---|')
            for tag, n in st.children.most_common():
                lo, hi = st.child_card[tag]
                L.append(f'| `{tag}` | {n} | {lo}–{hi} |')
            L.append('')

    return '\n'.join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('inputs', nargs='+')
    ap.add_argument('--json')
    ap.add_argument('--md')
    args = ap.parse_args()

    files = collect_files(args.inputs)
    stats: dict[str, NodeStat] = {}
    errors = []

    anomalies = Counter()
    for f in files:
        try:
            doc = parse_file(f)
        except Exception as e:                      # noqa: BLE001
            errors.append((str(f), f'{type(e).__name__}: {e}'))
            continue
        for pr in doc.problems:
            anomalies[pr.kind] += 1
        for root in doc.roots:
            walk(root, root.tag, stats, f.name)

    print(f'file letti : {len(files) - len(errors)}')
    print(f'errori     : {len(errors)}')
    for f, e in errors:
        print(f'  ! {f}: {e}')
    print(f'path unici : {len(stats)}')
    if anomalies:
        print(f'anomalie   : {dict(anomalies)}')

    if args.json:
        Path(args.json).write_text(
            json.dumps({p: s.to_dict() for p, s in sorted(stats.items())},
                       indent=1, ensure_ascii=False),
            encoding='utf-8')
        print(f'JSON -> {args.json}')
    if args.md:
        Path(args.md).write_text(render_md(stats, files), encoding='utf-8')
        print(f'MD   -> {args.md}')


if __name__ == '__main__':
    sys.exit(main())
