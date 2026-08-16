"""Ricava empiricamente la relazione fra gli attributi di tempo e i BPM.

Il Deluge non salva i BPM: salva `timePerTimerTick` + `timerTickFraction`
(punto fisso 32.32, campioni audio per tick interno) e `inputTickMagnitude`.
Questo script calcola i BPM candidati sotto piu' ipotesi e mostra quale
produce valori "sensati" (interi o mezzi) sul corpus reale.

NIENTE QUI E' DATO PER CERTO finche' non e' confermato leggendo un BPM sul
dispositivo per una song nota.

Uso: python tempo_probe.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402

SR = 44100.0          # frequenza di campionamento del Deluge (assunta)
TWO32 = 4294967296.0


def u32(v: str) -> int:
    """Il firmware scrive la frazione come int32 con segno."""
    i = int(v)
    return i + (1 << 32) if i < 0 else i


def samples_per_tick(node) -> float | None:
    tpt = node.get('timePerTimerTick')
    if tpt is None:
        return None
    frac = u32(node.get('timerTickFraction', '0'))
    return int(tpt) + frac / TWO32


def roundness(x: float) -> float:
    """Distanza dal multiplo di 0.5 piu' vicino."""
    return abs(x * 2 - round(x * 2)) / 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    args = ap.parse_args()

    rows = []
    for p in sorted(Path(args.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        song = doc.root
        if song.tag != 'song':
            continue
        spt = samples_per_tick(song)
        if spt is None:
            continue
        mag = int(song.get('inputTickMagnitude', '0'))
        rows.append((p.name, spt, mag, song.get('swingAmount'),
                     song.get('swingInterval')))

    hyps = {
        'A: 48 tick/beat, no mag':      lambda s, m: SR * 60 / (s * 48),
        'B: 48 tick/beat, x2^(mag-1)':  lambda s, m: SR * 60 / (s * 48) * 2 ** (m - 1),
        'C: 48 tick/beat, /2^(mag-1)':  lambda s, m: SR * 60 / (s * 48) / 2 ** (m - 1),
        'D: 24 tick/beat, no mag':      lambda s, m: SR * 60 / (s * 24),
        'E: 96 tick/beat, no mag':      lambda s, m: SR * 60 / (s * 96),
    }

    print(f'{"file":<24} {"spt":>14} {"mag":>4} | ' +
          ' '.join(f'{k.split(":")[0]:>9}' for k in hyps))
    print('-' * (24 + 14 + 6 + 3 + 10 * len(hyps)))
    scores = {k: 0.0 for k in hyps}
    for name, spt, mag, *_ in rows:
        vals = {k: f(spt, mag) for k, f in hyps.items()}
        for k, v in vals.items():
            scores[k] += roundness(v)
        print(f'{name:<24} {spt:>14.6f} {mag:>4} | ' +
              ' '.join(f'{vals[k]:>9.3f}' for k in hyps))

    print('\nquanto sono "rotondi" i valori (piu basso = ipotesi migliore):')
    for k, v in sorted(scores.items(), key=lambda kv: kv[1]):
        print(f'  {v / max(1, len(rows)):8.4f}   {k}')

    mags = {}
    for _, _, mag, *_ in rows:
        mags[mag] = mags.get(mag, 0) + 1
    print(f'\ndistribuzione inputTickMagnitude: {dict(sorted(mags.items()))}')


if __name__ == '__main__':
    sys.exit(main())
