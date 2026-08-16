"""Come fa una clip a dire a quale TRACK appartiene?

Modello corretto, dalla documentazione community:

    Song -> Track -> Clip
    «tracks contain one or more clips»
    «only one clip can be active (playing) in a track at a time»

Quindi <instruments> elenca i TRACK, non i preset. Due track distinti possono
essere stati caricati dallo stesso file di preset, e restano indipendenti — e'
il caso che l'utente chiama "polifonia". Percio' `instrumentPresetName` NON
identifica un track.

Questo script cerca cosa lo identifica davvero: guarda le song che hanno due
track con lo stesso presetName e vede cosa li distingue, e come le clip si
distribuiscono.

Uso: python track_binding.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402

CLIP_REF = ('instrumentPresetName', 'instrumentPresetFolder',
            'instrumentPresetSlot', 'instrumentPresetSubSlot', 'trackName',
            'midiChannel', 'cvChannel', 'section')
INSTR_ID = ('presetName', 'presetFolder', 'presetSlot', 'presetSubSlot',
            'name', 'channel', 'slot')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--song', help='esamina una sola song, in dettaglio')
    a = ap.parse_args()

    dup_tracks = []
    for p in sorted(Path(a.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        if a.song and p.name != a.song:
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue
        ins = doc.root.find('instruments')
        if not ins:
            continue

        names = Counter()
        for t in ins.children:
            names[(t.tag, t.get('presetName'), t.get('presetFolder'))] += 1
        repeated = {k: v for k, v in names.items() if v > 1}
        if repeated:
            dup_tracks.append((p.name, repeated, ins, doc))

    print(f'song con due o piu TRACK dallo stesso preset: {len(dup_tracks)}\n')

    for name, repeated, ins, doc in dup_tracks[:3]:
        print(f'=== {name} ===')
        for key, n in repeated.items():
            print(f'  {n} track <{key[0]}> con presetName={key[1]!r}')
            for i, t in enumerate(ins.children):
                if (t.tag, t.get('presetName'), t.get('presetFolder')) != key:
                    continue
                bits = [f'{k}={t.get(k)!r}' for k in INSTR_ID if t.has(k)]
                print(f'    indice {i}: ' + ' '.join(bits))
            # e le clip che li nominano
            sc = doc.root.find('sessionClips')
            if sc:
                for j, c in enumerate(sc.children):
                    if c.get('instrumentPresetName') != key[1]:
                        continue
                    bits = [f'{k}={c.get(k)!r}' for k in CLIP_REF if c.has(k)]
                    play = c.get('isPlaying')
                    print(f'    clip {j}: isPlaying={play} ' + ' '.join(bits))
        print()


if __name__ == '__main__':
    sys.exit(main())
