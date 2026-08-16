"""Confronta i blob di note della stessa clip in due file.

Serve a verificare se il Deluge, caricando e risalvando una song, riscrive
identici i dati di nota prodotti dal progetto — cioe' se li ha interpretati
esattamente come intendevamo.

Uso: python compare_blobs.py <file_a> <indice_a> <file_b> <indice_b>
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402
from delugexml import song as S            # noqa: E402
from delugexml import notes as N           # noqa: E402


def main():
    fa, ia, fb, ib = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    a = [c for _, c in S.clips(parse_file(fa))][ia]
    b = [c for _, c in S.clips(parse_file(fb))][ib]
    print(f'A: {Path(fa).name} clip {ia} — {S.clip_label(a)}')
    print(f'B: {Path(fb).name} clip {ib} — {S.clip_label(b)}\n')

    rows_a = {r.get('y'): r for r in S.note_rows(a) if r.has('y')}
    rows_b = {r.get('y'): r for r in S.note_rows(b) if r.has('y')}
    print(f'righe A: {len(rows_a)}   righe B: {len(rows_b)}')
    only_a = sorted(set(rows_a) - set(rows_b), key=int)
    only_b = sorted(set(rows_b) - set(rows_a), key=int)
    if only_a:
        print(f'  solo in A: y = {", ".join(only_a)}')
    if only_b:
        print(f'  solo in B: y = {", ".join(only_b)}')

    same = diff = 0
    for y in sorted(set(rows_a) & set(rows_b), key=int):
        for attr in N.ATTR_WIDTH:
            va, vb = rows_a[y].get(attr), rows_b[y].get(attr)
            if va is None and vb is None:
                continue
            if va == vb:
                same += 1
            else:
                diff += 1
                if diff <= 3:
                    print(f'\n  DIVERSO y={y} {attr}')
                    print(f'    A: {va}')
                    print(f'    B: {vb}')

    print(f'\nblob identici: {same}   diversi: {diff}')
    if same and not diff:
        print('\nIl dispositivo ha riscritto i dati di nota BYTE PER BYTE come')
        print('li avevamo prodotti: li ha interpretati esattamente cosi.')


if __name__ == '__main__':
    sys.exit(main())
