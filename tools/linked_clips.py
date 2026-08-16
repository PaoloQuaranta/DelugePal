"""Cosa distingue una clip "collegata" da quella originale?

Il manuale (Song View, 7.4) dice che clonando una clip in song view «the clip
will be cloned ... and assigned a different section and won't be launched.
Cloned clips are initially linked to the original».

Quindi fra due clip sullo stesso strumento una e' l'originale e le altre sono
collegate. Se la differenza e' visibile nel file, duplicare correttamente
significa riprodurla — ed e' probabilmente cio' che manca al duplicato prodotto
dal progetto, che il dispositivo scarta.

Confronta i FIGLI e gli ATTRIBUTI delle clip che condividono uno strumento.

Uso: python linked_clips.py <dir> [--song Electronic.XML]
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402


def key_of(clip):
    for k in ('trackName', 'cvChannel', 'midiChannel'):
        if clip.has(k):
            return (k, clip.get(k))
    return ('preset', clip.get('instrumentPresetName'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--song')
    a = ap.parse_args()

    child_diff = Counter()
    attr_diff = Counter()
    examples = []

    for p in sorted(Path(a.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        if a.song and p.name != a.song:
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue
        sc = doc.root.find('sessionClips')
        if not sc:
            continue

        groups = defaultdict(list)
        for i, c in enumerate(sc.children):
            groups[key_of(c)].append((i, c))

        for key, members in groups.items():
            if len(members) < 2 or not key[1]:
                continue
            # figli presenti in ciascuna clip del gruppo
            sets = [(i, frozenset(x.tag for x in c.children)) for i, c in members]
            first = sets[0][1]
            for i, s in sets[1:]:
                for tag in first - s:
                    child_diff[f'solo nella prima: {tag}'] += 1
                for tag in s - first:
                    child_diff[f'solo nelle successive: {tag}'] += 1
            # attributi presenti in una e non nell'altra
            asets = [(i, frozenset(k for k, _ in c.attrs)) for i, c in members]
            fa = asets[0][1]
            for i, s in asets[1:]:
                for k in fa - s:
                    attr_diff[f'solo nella prima: {k}'] += 1
                for k in s - fa:
                    attr_diff[f'solo nelle successive: {k}'] += 1

            if len(examples) < 4:
                examples.append((p.name, key[1],
                                 [(i, sorted(frozenset(x.tag for x in c.children)))
                                  for i, c in members]))

    print('differenze nei FIGLI fra clip che condividono uno strumento:')
    if child_diff:
        for k, n in child_diff.most_common(15):
            print(f'  {k:<48} {n}')
    else:
        print('  nessuna')

    print('\ndifferenze negli ATTRIBUTI:')
    if attr_diff:
        for k, n in attr_diff.most_common(15):
            print(f'  {k:<48} {n}')
    else:
        print('  nessuna')

    print('\nesempi (indice clip -> figli):')
    for name, instr, members in examples:
        print(f'  {name} — {instr!r}')
        for i, tags in members:
            print(f'    clip {i}: {tags}')


if __name__ == '__main__':
    sys.exit(main())
