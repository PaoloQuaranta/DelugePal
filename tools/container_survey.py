"""Dove stanno davvero le clip, e quante ce ne sono per strumento.

Nasce da un errore: `S.clips()` mette insieme sessionClips e
arrangementOnlyTracks, e su quel conteggio avevo concluso che "17 song su 27
hanno piu' clip che strumenti". Se pero' le clip in eccesso stanno
nell'arrangement e non nella sessione, la conclusione non vale per la
duplicazione in session view — che e' il caso che mi interessa.

Uso: python container_survey.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402

CONTAINERS = ('sessionClips', 'arrangementOnlyTracks', 'arrangementClips')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    a = ap.parse_args()

    print(f'{"song":<24} {"session":>8} {"arrang.":>8} {"strum.":>7} '
          f'{"session > strum.?":>18}')
    print('-' * 70)
    more = same = fewer = 0
    tags_in_arr = Counter()
    dup_in_session = []

    for p in sorted(Path(a.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue
        counts = {}
        for c in CONTAINERS:
            node = doc.root.find(c)
            counts[c] = len(node.children) if node else 0
            if c != 'sessionClips' and node:
                tags_in_arr.update(x.tag for x in node.children)
        ins = doc.root.find('instruments')
        n_ins = len(ins.children) if ins else 0
        n_ses = counts['sessionClips']
        n_arr = sum(v for k, v in counts.items() if k != 'sessionClips')

        verdict = 'piu' if n_ses > n_ins else ('uguale' if n_ses == n_ins else 'meno')
        more += n_ses > n_ins
        same += n_ses == n_ins
        fewer += n_ses < n_ins
        print(f'{p.name:<24} {n_ses:>8} {n_arr:>8} {n_ins:>7} {verdict:>18}')

        # quante clip di sessione condividono lo stesso strumento?
        node = doc.root.find('sessionClips')
        if node:
            by = defaultdict(int)
            for clip in node.children:
                key = (clip.get('instrumentPresetName'),
                       clip.get('instrumentPresetFolder'),
                       clip.get('trackName'))
                by[key] += 1
            shared = {k: v for k, v in by.items() if v > 1 and any(k)}
            if shared:
                dup_in_session.append((p.name, shared))

    print(f'\nsessionClips contro instruments: '
          f'piu {more}, uguale {same}, meno {fewer}')
    print(f'tag dentro i contenitori di arrangement: {dict(tags_in_arr)}')

    print(f'\nsong in cui DUE CLIP DI SESSIONE condividono uno strumento: '
          f'{len(dup_in_session)}')
    for name, shared in dup_in_session[:10]:
        for k, v in shared.items():
            print(f'  {name:<24} {v} clip su {k[0] or k[2]!r}')


if __name__ == '__main__':
    sys.exit(main())
