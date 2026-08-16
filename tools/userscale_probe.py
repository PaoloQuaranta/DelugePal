"""`userScale` e' una maschera a 12 bit dei semitoni della scala?

Indizio: fra i valori osservati c'e' 4095 = 0b111111111111, cioe' tutti e 12 i
semitoni. Se l'ipotesi regge, i bit accesi devono coincidere con i <modeNotes>
della stessa song.

Uso: python userscale_probe.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    a = ap.parse_args()

    ok = bad = skipped = 0
    print(f'{"song":<24} {"userScale":>10}  {"bit accesi":<34} esito')
    print('-' * 78)

    for p in sorted(Path(a.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue
        sc = doc.root.find('scales')
        if sc is None:
            continue
        us = sc.find('userScale')
        if us is None or not us.text or us.text == '0':
            skipped += 1
            continue
        v = int(us.text)
        bits = [k for k in range(12) if v >> k & 1]
        mn = doc.root.find('modeNotes')
        modes = [int(c.text) for c in mn.children if c.text] if mn else []
        same = bits == modes
        ok += same
        bad += not same
        print(f'{p.name:<24} {v:>10}  {str(bits):<34} '
              f'{"= modeNotes" if same else "DIVERSO da " + str(modes)}')

    print(f'\ncorrispondenti {ok}, diversi {bad}, con userScale=0 {skipped}')
    if ok and not bad:
        print('\nuserScale e la stessa scala di modeNotes, in forma di maschera '
              'a 12 bit.')


if __name__ == '__main__':
    sys.exit(main())
