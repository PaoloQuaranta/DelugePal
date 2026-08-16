"""Diagnostica: quanti e quali file XML del Deluge non sono well-formed, e perche'.

Cerca i due difetti gia' osservati piu' eventuali altri:
  A) '&' non escapato dentro un valore di attributo o nel testo
  B) attributi duplicati sullo stesso elemento
  C) altri errori riportati da ElementTree

Uso: python audit_wellformed.py <dir_o_file> [...]
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

# entita' XML valide che il Deluge potrebbe legittimamente emettere
VALID_ENT = re.compile(r'&(?:amp|lt|gt|quot|apos|#\d+|#x[0-9A-Fa-f]+);')

# apertura tag + tutti gli attributi fino a '>' o '/>'
TAG_RE = re.compile(r'<([A-Za-z_][\w.-]*)((?:\s+[\w.:-]+\s*=\s*"[^"]*")*)\s*/?>',
                    re.S)
ATTR_RE = re.compile(r'([\w.:-]+)\s*=\s*"([^"]*)"')


def bad_amp(text: str):
    """Posizioni di '&' che non aprono un'entita' valida."""
    out = []
    for m in re.finditer(r'&', text):
        if not VALID_ENT.match(text, m.start()):
            line = text.count('\n', 0, m.start()) + 1
            ctx = text[max(0, m.start() - 45):m.start() + 25].replace('\n', ' ')
            out.append((line, ctx.strip()))
    return out


def dup_attrs(text: str):
    out = []
    for m in TAG_RE.finditer(text):
        names = [a.group(1) for a in ATTR_RE.finditer(m.group(2))]
        c = Counter(names)
        dups = {k: v for k, v in c.items() if v > 1}
        if dups:
            line = text.count('\n', 0, m.start()) + 1
            out.append((line, m.group(1), dups))
    return out


def bad_raw_lt(text: str):
    """'<' dentro un valore di attributo (romperebbe il parsing)."""
    out = []
    for m in TAG_RE.finditer(text):
        for a in ATTR_RE.finditer(m.group(2)):
            if '<' in a.group(2):
                line = text.count('\n', 0, m.start()) + 1
                out.append((line, m.group(1), a.group(1), a.group(2)[:40]))
    return out


def collect(inputs):
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('inputs', nargs='+')
    ap.add_argument('-v', '--verbose', action='store_true')
    args = ap.parse_args()

    files = collect(args.inputs)
    tally = Counter()
    dup_names = Counter()
    amp_ctx = Counter()

    for f in files:
        raw = f.read_bytes().decode('utf-8', 'replace')
        amps = bad_amp(raw)
        dups = dup_attrs(raw)
        lts = bad_raw_lt(raw)
        try:
            ET.fromstring(raw)
            parses = True
            err = ''
        except ET.ParseError as e:
            parses = False
            err = str(e)

        if amps:
            tally['file con & non escapato'] += 1
        if dups:
            tally['file con attributi duplicati'] += 1
        if lts:
            tally['file con < in un attributo'] += 1
        if not parses:
            tally['file che ET rifiuta'] += 1
        if not (amps or dups or lts) and parses:
            tally['file puliti'] += 1

        for _, tag, d in dups:
            for k, n in d.items():
                dup_names[f'{tag}@{k}'] += 1
        for _, ctx in amps:
            amp_ctx[ctx[-30:]] += 1

        if amps or dups or lts or not parses:
            print(f'\n{f.name}')
            if not parses:
                print(f'   ET: {err}')
            for line, ctx in amps[:3 if not args.verbose else 99]:
                print(f'   & riga {line}: …{ctx}')
            if len(amps) > 3 and not args.verbose:
                print(f'   & … altri {len(amps)-3}')
            for line, tag, d in dups[:3 if not args.verbose else 99]:
                print(f'   dup riga {line}: <{tag}> {d}')
            if len(dups) > 3 and not args.verbose:
                print(f'   dup … altri {len(dups)-3}')
            for line, tag, an, av in lts[:3]:
                print(f'   < riga {line}: <{tag} {an}="{av}">')

    print('\n' + '=' * 60)
    print(f'file totali: {len(files)}')
    for k, v in tally.most_common():
        print(f'  {k:<32} {v}')
    if dup_names:
        print('\nattributi duplicati per elemento:')
        for k, v in dup_names.most_common(15):
            print(f'  {k:<40} {v}')


if __name__ == '__main__':
    sys.exit(main())
