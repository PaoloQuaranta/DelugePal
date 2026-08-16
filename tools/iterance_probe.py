"""I byte 11-13 di noteDataWithSplitProb sono iterance e fill?

Indizi che portano all'ipotesi:

  - il changelog c1.3.0 dice che una nota porta velocity, probability, lift,
    ITERANCE e FILL, e che l'iterance CUSTOM ha un "DIVISOR parameter (1 to 8)"
    con dei toggle per i singoli passi;
  - il nome stesso dell'attributo, noteDataWithSplitProb, suggerisce che la
    probabilita' e' stata SEPARATA da qualcos'altro con cui prima condivideva
    un byte;
  - i range osservati: byte 11 sta in 0..8, byte 12 in 0..128, byte 13 sempre 0.

Predizione verificabile: se il byte 11 e' il divisore e il byte 12 la maschera
dei passi attivi, allora ogni bit acceso nel byte 12 deve stare sotto il
divisore — non ha senso attivare il passo 5 su un divisore di 4. E il byte 12
deve essere 0 quando il byte 11 lo e'.

Uso: python iterance_probe.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402
from delugexml import notes as N           # noqa: E402

W = 14
ATTR = 'noteDataWithSplitProb'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    a = ap.parse_args()

    pairs = Counter()
    total = 0
    with_extra = 0
    coherent = incoherent = 0
    b13 = Counter()

    for p in sorted(Path(a.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        for _, node in doc.path_iter():
            if node.tag != 'noteRow':
                continue
            v = node.get(ATTR)
            if not v:
                continue
            raw = bytes.fromhex(v[2:] if v.lower().startswith('0x') else v)
            for i in range(0, len(raw), W):
                r = raw[i:i + W]
                if len(r) < W:
                    break
                total += 1
                div, mask, last = r[11], r[12], r[13]
                b13[last] += 1
                if div or mask:
                    with_extra += 1
                    pairs[(div, mask)] += 1
                    # ogni bit acceso deve stare sotto il divisore
                    ok = div > 0 and mask > 0 and mask < (1 << div)
                    if div == 0 and mask == 0:
                        ok = True
                    coherent += ok
                    incoherent += not ok

    print(f'note totali            : {total}')
    print(f'con byte 11-13 non zero: {with_extra}')
    print(f'byte 13: {dict(b13)}')

    print(f'\ncoppie (byte11, byte12) osservate:')
    print(f'{"div":>5} {"mask":>6} {"mask binaria":>14} {"n":>5}  coerente?')
    for (div, mask), n in sorted(pairs.items()):
        ok = 'si' if (div > 0 and 0 < mask < (1 << div)) else 'NO'
        print(f'{div:>5} {mask:>6} {mask:>14b} {n:>5}  {ok}')

    print(f'\ncoerenti {coherent}, incoerenti {incoherent}')
    if with_extra and incoherent == 0:
        print('\nOgni maschera sta dentro il proprio divisore: ipotesi retta.')
    elif incoherent:
        print('\nCi sono maschere fuori range: l ipotesi NON regge cosi come e.')


if __name__ == '__main__':
    sys.exit(main())
