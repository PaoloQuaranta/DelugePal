"""Confronta gli attributi delle clip di una song, a coppie.

Serve per mettere fianco a fianco una clip clonata dal dispositivo e una
duplicata dal progetto, e vedere cosa scrive il Deluge che noi non scriviamo.

Uso: python compare_clips.py <song> <indice_a> <indice_b> [...]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402
from delugexml import song as S            # noqa: E402


def main():
    doc = parse_file(sys.argv[1])
    idx = [int(x) for x in sys.argv[2:]]
    clips = [c for _, c in S.clips(doc)]
    sel = [(i, clips[i]) for i in idx]

    names = []
    for _, c in sel:
        names += [k for k, _ in c.attrs]
    names = sorted(set(names))

    w = max(len(n) for n in names) + 1
    head = ' '.join(f'clip {i}'.center(26) for i, _ in sel)
    print(f'{"attributo":<{w}} {head}')
    print('-' * (w + 27 * len(sel)))
    for n in names:
        vals = [c.get(n) for _, c in sel]
        same = len(set(vals)) == 1
        mark = '  ' if same else '≠ '
        cells = ' '.join(('—' if v is None else str(v))[:26].center(26)
                         for v in vals)
        print(f'{mark}{n:<{w-2}} {cells}')

    print()
    for i, c in sel:
        kids = [x.tag for x in c.children]
        rows = S.note_rows(c)
        n_notes = sum(len(S.read_notes(r)) for r in rows)
        print(f'clip {i}: figli {kids}')
        print(f'         {len(rows)} righe, {n_notes} note')


if __name__ == '__main__':
    sys.exit(main())
