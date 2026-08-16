"""Deriva empiricamente le regole di formattazione del writer XML del Deluge.

Domanda a cui risponde: quando il firmware scrive gli attributi tutti sulla
stessa riga e quando invece uno per riga? Esiste una soglia (n attributi?
lunghezza riga?) oppure dipende dall'elemento?

Uso: python analyze_format.py <dir_o_file> [...]
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

OPEN_RE = re.compile(
    r'<(?P<tag>[A-Za-z_][\w.-]*)(?P<attrs>(?:\s+[\w.:-]+\s*=\s*"[^"]*")*)\s*(?P<close>/?)>')
ATTR_RE = re.compile(r'([\w.:-]+)\s*=\s*"([^"]*)"')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('inputs', nargs='+')
    args = ap.parse_args()

    files = []
    for i in args.inputs:
        p = Path(i)
        files += ([q for q in sorted(p.rglob('*'))
                   if q.is_file() and q.suffix.lower() == '.xml'
                   and not q.name.startswith('._')] if p.is_dir() else [p])

    # n_attr -> Counter{'inline': n, 'multiline': n}
    by_nattr = defaultdict(lambda: {'inline': 0, 'multiline': 0})
    # esempi di inline piu' lunghi e multiline piu' corti (per cercare la soglia)
    longest_inline = []
    shortest_multi = []
    # elementi che appaiono in entrambe le forme
    forms = defaultdict(set)
    indent_chars = set()

    for f in files:
        raw = f.read_bytes().decode('utf-8', 'replace')
        for m in OPEN_RE.finditer(raw):
            body = m.group(0)
            n = len(ATTR_RE.findall(m.group('attrs')))
            if n == 0:
                continue
            multiline = '\n' in body
            key = 'multiline' if multiline else 'inline'
            by_nattr[n][key] += 1
            forms[m.group('tag')].add(key)

            # lunghezza della riga completa in cui inizia il tag
            ls = raw.rfind('\n', 0, m.start()) + 1
            indent = raw[ls:m.start()]
            if indent.strip() == '':
                indent_chars.add(repr(indent[:1]) if indent else "''")
            if not multiline:
                le = raw.find('\n', m.start())
                longest_inline.append((le - ls, n, m.group('tag'), f.name))
            else:
                # lunghezza che avrebbe avuto se scritto inline
                flat = re.sub(r'\s+', ' ', body)
                shortest_multi.append((len(indent) + len(flat), n,
                                       m.group('tag'), f.name))

    print(f'file: {len(files)}\n')
    print(f'{"n attributi":>12} | {"inline":>8} | {"multiline":>10}')
    print('-' * 36)
    for n in sorted(by_nattr):
        d = by_nattr[n]
        print(f'{n:>12} | {d["inline"]:>8} | {d["multiline"]:>10}')

    print(f'\ncaratteri di indentazione osservati: {sorted(indent_chars)}')

    longest_inline.sort(reverse=True)
    shortest_multi.sort()
    print('\ninline PIU LUNGHI (lunghezza riga, n attr, tag, file):')
    for x in longest_inline[:8]:
        print('  ', x)
    print('\nmultiline che sarebbero stati PIU CORTI se inline:')
    for x in shortest_multi[:8]:
        print('  ', x)

    both = {t: v for t, v in forms.items() if len(v) > 1}
    print(f'\ntag visti in ENTRAMBE le forme: {len(both)}')
    for t in sorted(both)[:20]:
        print('  ', t)


if __name__ == '__main__':
    sys.exit(main())
