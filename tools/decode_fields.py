"""Identifica i singoli campi dentro un record di nota.

Larghezza del record gia' determinata da decode_notes.py:
    noteDataWithLift      = 11 byte
    noteDataWithSplitProb = 14 byte

Qui si decodifica ogni byte / gruppo di byte e se ne riporta il range
osservato su tutto il corpus. Un campo che sta stabilmente in 1..127 e' quasi
certamente una velocity o una lift; uno che cresce fino alla lunghezza della
clip e' una posizione o una durata.

Uso: python decode_fields.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402

WIDTHS = {'noteDataWithLift': 11, 'noteDataWithSplitProb': 14}


class Field:
    def __init__(self, name):
        self.name = name
        self.lo = None
        self.hi = None
        self.vals = Counter()
        self.n = 0

    def add(self, v):
        self.n += 1
        self.lo = v if self.lo is None else min(self.lo, v)
        self.hi = v if self.hi is None else max(self.hi, v)
        if len(self.vals) <= 40:
            self.vals[v] += 1

    def line(self):
        distinct = f'{len(self.vals)}+' if len(self.vals) > 40 else str(len(self.vals))
        top = ', '.join(f'{v}({n})' for v, n in self.vals.most_common(6)) \
            if len(self.vals) <= 40 else ''
        return (f'  {self.name:<26} n={self.n:<7} range [{self.lo} … {self.hi}]'
                f'  distinti={distinct}  {top}')


def records(blob: str, width: int):
    h = blob[2:] if blob.startswith('0x') else blob
    b = bytes.fromhex(h)
    return [b[i:i + width] for i in range(0, len(b), width)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    args = ap.parse_args()

    stats = {a: {} for a in WIDTHS}
    span_ok = Counter()

    for p in sorted(Path(args.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue

        def walk(node, clip_len):
            if node.tag in ('instrumentClip',) and node.has('length'):
                clip_len = int(node.get('length'))
            if node.tag == 'noteRow':
                for attr, w in WIDTHS.items():
                    v = node.get(attr)
                    if not v:
                        continue
                    S = stats[attr]
                    for r in records(v, w):
                        def f(name):
                            return S.setdefault(name, Field(name))
                        pos = int.from_bytes(r[0:4], 'big')
                        length = int.from_bytes(r[4:8], 'big')
                        f('byte 0-3  (pos)').add(pos)
                        f('byte 4-7  (durata)').add(length)
                        for k in range(8, w):
                            f(f'byte {k}').add(r[k])
                        if clip_len:
                            span_ok[(attr, pos + length <= clip_len)] += 1
            for c in node.children:
                walk(c, clip_len)

        for r in doc.roots:
            walk(r, None)

    for attr, S in stats.items():
        print(f'\n=== {attr} (record da {WIDTHS[attr]} byte) ===')
        for name in sorted(S, key=lambda x: (len(x), x)):
            print(S[name].line())

    print('\ncontrollo "pos + durata <= lunghezza clip":')
    for (attr, ok), n in sorted(span_ok.items()):
        print(f'  {attr:<24} {"rispettato" if ok else "VIOLATO   "} {n}')


if __name__ == '__main__':
    sys.exit(main())
