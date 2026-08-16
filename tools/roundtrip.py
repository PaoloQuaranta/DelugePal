"""Fase 1 - round-trip test.

Per ogni file: parse -> serialize -> confronto byte per byte con l'originale.
Esegue due modalita':

  surgical : i rami non modificati sono ricopiati dal sorgente.
             Deve essere byte-esatto sempre; se fallisce, il parser sta
             perdendo informazione.
  rebuild  : tutto riscritto dalle regole di formato.
             Se e' byte-esatto, sappiamo generare nodi nuovi corretti.

Uso:
    python roundtrip.py <dir> [--table out/format_table.json] [--learn]
                        [--diff N] [--dump-dir DIR]
"""
from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file, serialize          # noqa: E402
from delugexml.writer import FormatTable             # noqa: E402


def files_in(root: Path):
    if root.is_file():
        return [root]
    return [p for p in sorted(root.rglob('*'))
            if p.is_file() and p.suffix.lower() == '.xml'
            and not p.name.startswith('._')]


def show_diff(orig: str, got: str, name: str, maxlines: int):
    d = difflib.unified_diff(orig.splitlines(), got.splitlines(),
                             f'{name} (originale)', f'{name} (riscritto)',
                             lineterm='', n=2)
    for k, line in enumerate(d):
        if k >= maxlines:
            print('      … (troncato)')
            break
        print('      ' + line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--table', default=None)
    ap.add_argument('--learn', action='store_true',
                    help='apprende la tabella di formato dai file dati')
    ap.add_argument('--diff', type=int, default=0,
                    help='righe di diff da mostrare per file fallito')
    ap.add_argument('--dump-dir')
    args = ap.parse_args()

    paths = files_in(Path(args.root))
    docs = []
    print(f'parsing {len(paths)} file…')
    for p in paths:
        docs.append((p, parse_file(p)))

    if args.learn:
        table = FormatTable().learn(d for _, d in docs)
        if args.table:
            table.save(args.table)
            print(f'tabella di formato -> {args.table}')
        print(f'  percorsi appresi : {len(table.by_path)}')
        print(f'  tag appresi      : {len(table.by_tag)}')
        if table.conflicts:
            print(f'  percorsi ambigui : {len(table.conflicts)}')
            for k, v in list(table.conflicts.items())[:10]:
                print(f'    {k}: {v}')
    elif args.table:
        table = FormatTable.load(args.table)
    else:
        table = FormatTable()

    probs = sum(len(d.problems) for _, d in docs)
    kinds = {}
    for _, d in docs:
        for pr in d.problems:
            kinds[pr.kind] = kinds.get(pr.kind, 0) + 1
    print(f'\nanomalie rilevate dal parser: {probs}')
    for k, v in sorted(kinds.items(), key=lambda kv: -kv[1]):
        print(f'  {k:<20} {v}')

    for mode in ('surgical', 'rebuild'):
        ok = bad = 0
        failures = []
        for p, d in docs:
            got = serialize(d, table, rebuild=(mode == 'rebuild'))
            if got == d.raw:
                ok += 1
            else:
                bad += 1
                failures.append((p, d, got))
        print(f'\n=== {mode}: {ok}/{len(docs)} byte-identici ===')
        for p, d, got in failures[:8]:
            o, g = d.raw.splitlines(), got.splitlines()
            first = next((i for i, (a, b) in enumerate(zip(o, g)) if a != b),
                         min(len(o), len(g)))
            print(f'  ✗ {p.name}  righe {len(o)}->{len(g)}  '
                  f'prima differenza r{first+1}')
            if args.diff:
                show_diff(d.raw, got, p.name, args.diff)
            if args.dump_dir:
                out = Path(args.dump_dir)
                out.mkdir(parents=True, exist_ok=True)
                (out / f'{p.stem}.{mode}.xml').write_text(
                    got, encoding='utf-8', errors='surrogateescape')
        if len(failures) > 8:
            print(f'  … altri {len(failures)-8} file falliti')

    return 0


if __name__ == '__main__':
    sys.exit(main())
