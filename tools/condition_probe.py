"""Come si distribuiscono i valori del byte 10 (condizione) di una nota.

Il manuale dice che la probabilita' si regola dal 5% al 100% a passi di 5,
cioe' 20 gradini, e che 100% e' il valore predefinito. Nel corpus il valore
dominante e' proprio 20. Restano da caratterizzare i valori sopra 20.

Uso: python condition_probe.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402
from delugexml import notes as N           # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    a = ap.parse_args()

    counts = Counter()
    for p in sorted(Path(a.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        for _, node in doc.path_iter():
            if node.tag != 'noteRow':
                continue
            for attr, w in N.ATTR_WIDTH.items():
                v = node.get(attr)
                if not v:
                    continue
                raw = bytes.fromhex(v[2:] if v.lower().startswith('0x') else v)
                for i in range(0, len(raw), w):
                    r = raw[i:i + w]
                    if len(r) < w:
                        break
                    counts[r[10]] += 1

    print('valori del byte 10, per frequenza:')
    for v, k in counts.most_common(20):
        if v <= 20:
            cat = f'probabilita {v * 5}%'
        elif v < 128:
            cat = 'fra 21 e 127 — non spiegato'
        else:
            cat = f'bit alto acceso, resto {v - 128}'
        print(f'  {v:>4}  x{k:<7} {cat}')

    lo = sum(k for v, k in counts.items() if v <= 20)
    mid = sum(k for v, k in counts.items() if 20 < v < 128)
    hi = sum(k for v, k in counts.items() if v >= 128)
    print(f'\ndistinti: {len(counts)}')
    print(f'  <= 20      : {lo}')
    print(f'  21..127    : {mid}')
    print(f'  >= 128     : {hi}')
    if mid:
        vals = sorted(v for v in counts if 20 < v < 128)
        print(f'  valori nella fascia intermedia: {vals}')
        print(f'  meno 20: {[v - 20 for v in vals]}')


if __name__ == '__main__':
    sys.exit(main())
