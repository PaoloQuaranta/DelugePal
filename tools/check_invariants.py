"""Invarianti da rispettare quando si duplica una clip o si crea una noteRow.

  1. `beingEdited` e `selected`: al massimo una clip per song puo' averli a 1?
  2. le <noteRow> sono sempre ordinate per y crescente?
  3. una noteRow con note porta sempre entrambi gli attributi di note?

Uso: python check_invariants.py <dir>
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402
from delugexml import song as S            # noqa: E402
from delugexml import notes as N           # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    a = ap.parse_args()

    flags = Counter()
    order_ok = order_bad = 0
    bad_examples = []
    attr_combo = Counter()
    n_songs = 0

    for p in sorted(Path(a.root).rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue
        n_songs += 1
        clips = [c for _, c in S.clips(doc)]

        for name in ('beingEdited', 'selected'):
            n = sum(1 for c in clips if c.get(name) == '1')
            flags[f'{name}=1 su {n} clip'] += 1

        for c in clips:
            rows = S.note_rows(c)
            ys = [int(r.get('y')) for r in rows if r.has('y')]
            if ys == sorted(ys):
                order_ok += 1
            else:
                order_bad += 1
                if len(bad_examples) < 5:
                    bad_examples.append((p.name, ys[:12]))
            for r in rows:
                have = tuple(sorted(k for k, _ in r.attrs
                                    if k in N.ATTR_WIDTH))
                attr_combo[have] += 1

    print(f'song analizzate: {n_songs}\n')

    print('=== 1. flag di stato per song ===')
    for k, v in sorted(flags.items()):
        print(f'  {k:<28} {v} song')

    print('\n=== 2. noteRow ordinate per y? ===')
    print(f'  clip ordinate   : {order_ok}')
    print(f'  clip NON ordinate: {order_bad}')
    for name, ys in bad_examples:
        print(f'    {name}: {ys}')

    print('\n=== 3. attributi di note presenti su una noteRow ===')
    for combo, n in attr_combo.most_common():
        label = ', '.join(combo) if combo else '(riga vuota, nessun dato)'
        print(f'  {n:>6}  {label}')


if __name__ == '__main__':
    sys.exit(main())
