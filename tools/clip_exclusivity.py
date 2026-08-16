"""Due clip sullo stesso strumento possono essere entrambe in riproduzione?

Ipotesi nata da un fallimento: una clip duplicata non compariva sul
dispositivo. In Electronic.XML cinque clip condividono il kit 000 TR-808, ma
stanno in cinque sezioni diverse e **una sola** ha isPlaying=1.

Sul Deluge uno strumento suona una clip alla volta: le clip che lo condividono
sono alternative, non voci simultanee. Se e' cosi', deve valere ovunque.

Uso: python clip_exclusivity.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402
from delugexml import song as S            # noqa: E402


def track_of(clip):
    """Cosa identifica il TRACK a cui appartiene una clip.

    Dipende dal tipo di track, e nel corpus non ci sono due track dello stesso
    tipo con lo stesso identificatore:

        synth / kit  -> presetName + presetFolder
        audio track  -> trackName  (AUDIO1, AUDIO2, …)
        CV           -> cvChannel
        MIDI         -> midiChannel
    """
    for key in ('trackName', 'cvChannel', 'midiChannel'):
        if clip.has(key):
            return (key, clip.get(key))
    return ('preset', clip.get('instrumentPresetName'),
            clip.get('instrumentPresetFolder'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    a = ap.parse_args()

    playing_hist = Counter()
    section_hist = Counter()
    violations = []
    groups = 0

    for p in sorted(Path(a.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue
        by_instr = defaultdict(list)
        for _, clip in S.clips(doc):
            by_instr[instrument_of(clip)].append(clip)

        for key, cl in by_instr.items():
            if len(cl) < 2:
                continue
            groups += 1
            n_play = sum(1 for c in cl if c.get('isPlaying') == '1')
            playing_hist[n_play] += 1
            secs = [c.get('section') for c in cl]
            section_hist[len(set(secs)) == len(secs)] += 1
            if n_play > 1:
                violations.append((p.name, key[0] or key[2], len(cl), n_play, secs))

    print(f'gruppi di clip che condividono uno strumento: {groups}\n')

    print('quante di quelle clip hanno isPlaying=1:')
    for n, c in sorted(playing_hist.items()):
        flag = '   <== piu di una!' if n > 1 else ''
        print(f'  {n} clip in riproduzione : {c} gruppi{flag}')

    print('\nle clip di un gruppo stanno tutte in sezioni diverse?')
    for ok, c in sorted(section_hist.items()):
        print(f'  {"si" if ok else "no"} : {c} gruppi')

    if violations:
        print('\ngruppi con piu di una clip in riproduzione:')
        for name, instr, n, np, secs in violations[:10]:
            print(f'  {name}: "{instr}" {n} clip, {np} in riproduzione, '
                  f'sezioni {secs}')
    else:
        print('\nNESSUN gruppo ha piu di una clip in riproduzione: '
              'e una regola, non una coincidenza.')


if __name__ == '__main__':
    sys.exit(main())
