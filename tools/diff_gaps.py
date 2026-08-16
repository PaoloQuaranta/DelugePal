"""Trova quali byte sono spariti fra l'originale e il file riletto.

Serve a capire il pattern di perdita di una scrittura via SysEx: se mancano
gruppi a intervalli regolari, la causa e' l'impacchettamento 7/8 con un gruppo
finale incompleto.
"""
from __future__ import annotations

import difflib
import sys
from pathlib import Path


def main():
    a = Path(sys.argv[1]).read_bytes()
    b = Path(sys.argv[2]).read_bytes()
    block = int(sys.argv[3]) if len(sys.argv) > 3 else 768
    print(f'originale {len(a)}  riletto {len(b)}  mancano {len(a)-len(b)}\n')

    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    gaps = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ('delete', 'replace'):
            gaps.append((i1, i2 - i1))

    print(f'{"offset":>9} {"persi":>6} {"blocco":>7} {"pos nel blocco":>15}')
    print('-' * 42)
    for off, n in gaps[:25]:
        print(f'{off:>9} {n:>6} {off//block:>7} {off % block:>15}')
    if len(gaps) > 25:
        print(f'… altri {len(gaps)-25} buchi')

    tot = sum(n for _, n in gaps)
    print(f'\nbuchi: {len(gaps)}, byte persi in totale: {tot}')
    if gaps:
        sizes = {}
        for _, n in gaps:
            sizes[n] = sizes.get(n, 0) + 1
        print(f'dimensioni dei buchi: {dict(sorted(sizes.items()))}')
        pos = [off % block for off, _ in gaps]
        print(f'posizione nel blocco: min {min(pos)}, max {max(pos)}, '
              f'distinte {len(set(pos))}')
        # un blocco da `block` byte contiene block//7 gruppi pieni piu' un resto
        print(f'\nblocco {block}: {block//7} gruppi da 7, resto {block % 7} byte')


if __name__ == '__main__':
    main()
