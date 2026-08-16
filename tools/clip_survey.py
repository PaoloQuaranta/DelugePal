"""Cosa lega una clip al suo strumento, e cosa deve essere unico.

Domande a cui risponde, guardando i file reali invece di ipotizzare:

  1. Piu' clip possono riferirsi allo stesso strumento? (serve per duplicare)
  2. Quanti <instrument> ci sono rispetto al numero di clip?
  3. Quali attributi di <instrumentClip> sono unici nella song e quali no —
     cioe' cosa va cambiato quando si duplica una clip.

Uso: python clip_survey.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402
from delugexml import song as S            # noqa: E402


def instrument_key(clip):
    return (clip.get('instrumentPresetName'),
            clip.get('instrumentPresetFolder'),
            clip.get('instrumentPresetSlot'),
            clip.get('trackName'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    a = ap.parse_args()

    shared_examples = []
    ratio = []
    # attributo -> quante volte era unico / quante volte ripetuto nella song
    uniq = defaultdict(lambda: [0, 0])
    n_songs = 0

    for p in sorted(Path(a.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue
        n_songs += 1
        clips = [c for _, c in S.clips(doc)]
        if not clips:
            continue

        instruments = doc.root.find('instruments')
        n_instr = len(instruments.children) if instruments else 0
        ratio.append((p.name, len(clips), n_instr))

        keys = Counter(instrument_key(c) for c in clips)
        for k, n in keys.items():
            if n > 1 and len(shared_examples) < 8:
                shared_examples.append((p.name, k[0] or k[3], n))

        # per ogni attributo: e' unico fra le clip di questa song?
        names = set()
        for c in clips:
            names.update(k for k, _ in c.attrs)
        for name in names:
            vals = [c.get(name) for c in clips if c.has(name)]
            if len(vals) < 2:
                continue
            if len(set(vals)) == len(vals):
                uniq[name][0] += 1
            else:
                uniq[name][1] += 1

    print(f'song analizzate: {n_songs}\n')

    print('=== 1. piu clip sullo stesso strumento? ===')
    if shared_examples:
        print('SI, osservato:')
        for name, instr, n in shared_examples:
            print(f'  {name:<24} {n} clip su "{instr}"')
    else:
        print('mai osservato nel corpus')

    print('\n=== 2. numero di clip contro numero di <instrument> ===')
    more = [r for r in ratio if r[1] > r[2]]
    print(f'song con piu clip che strumenti: {len(more)} su {len(ratio)}')
    for name, nc, ni in sorted(more, key=lambda r: r[2] - r[1])[:6]:
        print(f'  {name:<24} {nc} clip, {ni} strumenti')

    print('\n=== 3. attributi di instrumentClip: unici o ripetibili? ===')
    print(f'{"attributo":<28} {"sempre unico":>13} {"ripetuto":>9}')
    print('-' * 54)
    for name, (u, r) in sorted(uniq.items(), key=lambda kv: -kv[1][0]):
        flag = '  <== candidato a identificatore' if r == 0 and u > 3 else ''
        print(f'{name:<28} {u:>13} {r:>9}{flag}')


if __name__ == '__main__':
    sys.exit(main())
