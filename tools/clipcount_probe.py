"""Esiste un attributo, da qualche parte, che conta le clip?

Se il numero di clip fosse dichiarato anche altrove — a livello di <song> o di
<instruments> — aggiungere una clip senza aggiornare quel numero spiegherebbe
perche' il dispositivo la ignora.

Cerca ogni attributo intero dell'elemento <song> e di ogni <instrument> il cui
valore coincida con un conteggio di clip, su tutte le song del corpus. Un
attributo che coincide in TUTTE le song e' un candidato serio; uno che coincide
per caso in due o tre no.

Uso: python clipcount_probe.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    a = ap.parse_args()

    matches_song = Counter()
    seen_song = Counter()
    matches_instr = Counter()
    seen_instr = Counter()
    n_songs = 0

    for p in sorted(Path(a.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue
        n_songs += 1
        sc = doc.root.find('sessionClips')
        n_ses = len(sc.children) if sc else 0
        ins = doc.root.find('instruments')
        n_ins = len(ins.children) if ins else 0
        targets = {n_ses, n_ins, n_ses - 1, n_ses + 1}

        for k, v in doc.root.attrs:
            try:
                iv = int(v)
            except ValueError:
                continue
            seen_song[k] += 1
            if iv in targets:
                matches_song[k] += 1

        if ins:
            for t in ins.children:
                # quante clip di sessione puntano a questo strumento?
                n_clips = 0
                if sc:
                    for c in sc.children:
                        if (c.get('instrumentPresetName') == t.get('presetName')
                                and t.get('presetName') is not None):
                            n_clips += 1
                for k, v in t.attrs:
                    try:
                        iv = int(v)
                    except ValueError:
                        continue
                    seen_instr[k] += 1
                    if iv == n_clips:
                        matches_instr[k] += 1

    print(f'song analizzate: {n_songs}\n')
    print('attributi di <song> che coincidono con un conteggio di clip:')
    print(f'{"attributo":<28} {"coincide":>9} {"su":>5}')
    for k, n in matches_song.most_common(12):
        flag = '  <== sempre' if n == seen_song[k] == n_songs else ''
        print(f'{k:<28} {n:>9} {seen_song[k]:>5}{flag}')

    print('\nattributi di <instrument> che coincidono col numero di sue clip:')
    for k, n in matches_instr.most_common(12):
        print(f'{k:<28} {n:>9} {seen_instr[k]:>5}')

    if not any(n == seen_song[k] == n_songs for k, n in matches_song.items()):
        print('\nNessun attributo di <song> conta le clip in modo affidabile.')


if __name__ == '__main__':
    sys.exit(main())
