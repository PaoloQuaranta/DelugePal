"""Verifica la risoluzione della griglia: quanti tick vale un movimento?

Il tempo e la griglia delle note dovrebbero misurare la stessa cosa. La formula
del tempo assume tick_per_movimento = 24 * 2^inputTickMagnitude. Se e' giusta,
allora le lunghezze delle clip devono venire numeri interi di battute quando le
si divide per 4 * 24 * 2^mag — e devono NON venirlo con l'altra ipotesi.

Osservazione che ha motivato il test: in Perche.XML (mag=2) una nota a posizione
144 cade sul quarto ottavo della prima battuta. Quindi 48 tick = un ottavo,
96 tick = un movimento = 24 * 2^2. Confermato dal dispositivo.

Uso: python grid_probe.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402
from delugexml import song as S            # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    args = ap.parse_args()

    verdict = Counter()
    rows = []

    for p in sorted(Path(args.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue
        mag = int(doc.root.get('inputTickMagnitude', '0'))
        tpb = 24 * 2 ** mag          # tick per movimento secondo il modello
        alt = 48                     # ipotesi alternativa: sempre 48

        lengths, positions = [], []
        for _, clip in S.clips(doc):
            L = clip.get('length')
            if L:
                lengths.append(int(L))
            for row in S.note_rows(clip):
                positions += [n.pos for n in S.read_notes(row) if n.pos]

        if not lengths:
            continue
        g = 0
        for x in positions:
            g = gcd(g, x)

        rows.append((p.name, mag, tpb, min(lengths), max(lengths), g))
        verdict[mag] += 1

    print(f'{"file":<24} {"mag":>3} {"tick/mov atteso":>15} {"len min":>8} '
          f'{"len max":>8} {"gcd posizioni":>14}')
    print('-' * 78)
    for name, mag, tpb, lo, hi, g in sorted(rows, key=lambda r: (r[1], r[0])):
        print(f'{name:<24} {mag:>3} {tpb:>15} {lo:>8} {hi:>8} {g:>14}')

    # Il test che discrimina: se tick/movimento = 24 * 2^mag, la stessa
    # suddivisione musicale costa il DOPPIO dei tick nelle song con mag=2.
    # Se invece fosse 48 fissi, le due popolazioni sarebbero indistinguibili.
    def med(xs):
        xs = sorted(xs)
        return xs[len(xs) // 2] if xs else 0

    print('\ntest discriminante: la granularita\' raddoppia con la magnitude?')
    print(f'{"mag":>4} {"n":>4} {"mediana gcd posizioni":>22} '
          f'{"mediana lunghezza minima":>26}')
    prev = None
    for mag in sorted(verdict):
        sel = [r for r in rows if r[1] == mag]
        mg, ml = med([r[5] for r in sel]), med([r[3] for r in sel])
        print(f'{mag:>4} {len(sel):>4} {mg:>22} {ml:>26}')
        if prev:
            print(f'       rapporto rispetto a mag={prev[0]}: '
                  f'gcd x{mg / prev[1]:.2f}, lunghezza minima x{ml / prev[2]:.2f}'
                  f'   (il modello prevede x2.00)')
        prev = (mag, mg, ml)


if __name__ == '__main__':
    sys.exit(main())
