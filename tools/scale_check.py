"""La `y` di una noteRow e' una nota MIDI assoluta o un grado della scala?

La domanda conta: se il generatore scrive y = radice + semitoni ma il Deluge
interpreta y come indice di riga nella scala, il risultato e' sbagliato.

Il test: prendere `rootNote` e `modeNotes` della song (che definiscono la
scala) e vedere se le y usate ci stanno dentro. Se le y sono note MIDI
assolute e la song e' in scala, quasi tutte devono appartenere alla scala.
Se molte cadono fuori, o le clip sono cromatiche o y significa altro.

Uso: python scale_check.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402
from delugexml import song as S            # noqa: E402

NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    a = ap.parse_args()

    print(f'{"song":<22} {"root":>5} {"modeNotes":<24} {"inKey":>6} '
          f'{"y in scala":>11} {"fuori":>6}')
    print('-' * 82)
    tot_in = tot_out = 0

    for p in sorted(Path(a.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue
        root = int(doc.root.get('rootNote', '0'))
        mn = doc.root.find('modeNotes')
        modes = [int(c.text) for c in mn.children if c.text] if mn else []
        if not modes:
            continue
        scale = {(root + m) % 12 for m in modes}

        inside = outside = 0
        inkey = Counter()
        for _, clip in S.clips(doc):
            if clip.has('inKeyMode'):
                inkey[clip.get('inKeyMode')] += 1
            for row in S.note_rows(clip):
                if not row.has('y') or not S.read_notes(row):
                    continue
                y = int(row.get('y'))
                if y % 12 in scale:
                    inside += 1
                else:
                    outside += 1
        if inside + outside == 0:
            continue
        tot_in += inside
        tot_out += outside
        pct = 100 * inside / (inside + outside)
        modestr = ','.join(str(m) for m in modes)
        ik = '/'.join(f'{k}:{v}' for k, v in sorted(inkey.items()))
        print(f'{p.name:<22} {NAMES[root % 12]:>5} {modestr:<24} {ik:>6} '
              f'{pct:>10.0f}% {outside:>6}')

    tot = tot_in + tot_out
    print(f'\ntotale: {tot_in}/{tot} righe con note dentro la scala '
          f'({100*tot_in/tot:.1f}%)')
    print('\nSe la percentuale e alta, `y` e una nota MIDI assoluta e le song')
    print('rispettano la propria scala. Se fosse un grado di scala, il')
    print('confronto y%12 contro la scala non avrebbe motivo di tornare.')


if __name__ == '__main__':
    sys.exit(main())
