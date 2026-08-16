"""Validazione leave-one-out della tabella di formato.

Il test "rebuild byte-identico" e' circolare se la tabella e' stata appresa
dagli stessi file. Qui, per ogni file, la tabella viene appresa da TUTTI GLI
ALTRI e poi si prova a ricostruire quel file. Se passa, le regole
generalizzano e possiamo usarle su materiale mai visto.

Riporta anche quali percorsi del file di test non erano presenti nella
tabella (copertura), perche' li' il writer sta usando un ripiego.

Uso: python crossval.py <dir> [--extra dir_altri_tipi_di_file]
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file, serialize          # noqa: E402
from delugexml.writer import FormatTable, sig_of     # noqa: E402


def files_in(root: Path):
    if root.is_file():
        return [root]
    return [p for p in sorted(root.rglob('*'))
            if p.is_file() and p.suffix.lower() == '.xml'
            and not p.name.startswith('._')]


def coverage(table: FormatTable, doc):
    """Come viene risolto ogni nodo con attributi: sig / path / tag / default."""
    c = Counter()
    unknown = Counter()
    for path, node in doc.path_iter():
        if not node.attrs:
            continue
        if f'{path}|{sig_of(node)}' in table.by_sig:
            c['sig'] += 1
        elif f'{node.tag}|{sig_of(node)}' in table.by_tag_sig:
            c['tag_sig'] += 1
        elif path in table.by_path:
            c['path'] += 1
            unknown[f'{path}|{sig_of(node)}'] += 1
        elif node.tag in table.by_tag:
            c['tag'] += 1
            unknown[path] += 1
        else:
            c['default'] += 1
            unknown[path] += 1
    return c, unknown


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--extra', help='file di tipo diverso (kit, synth, settings)')
    args = ap.parse_args()

    paths = files_in(Path(args.root))
    docs = [(p, parse_file(p)) for p in paths]
    print(f'corpus: {len(docs)} file\n')

    ok = 0
    fallback_tot = Counter()
    worst = []
    for i, (p, d) in enumerate(docs):
        table = FormatTable().learn(x for j, (_, x) in enumerate(docs) if j != i)
        got = serialize(d, table, rebuild=True)
        cov, unknown = coverage(table, d)
        fallback_tot.update({k: v for k, v in cov.items() if k != 'sig'})
        if got == d.raw:
            ok += 1
            mark = 'ok'
        else:
            o, g = d.raw.splitlines(), got.splitlines()
            first = next((k for k, (a, b) in enumerate(zip(o, g)) if a != b),
                         min(len(o), len(g)))
            mark = f'DIVERSO (prima differenza r{first+1})'
            worst.append((p.name, first, unknown.most_common(5)))
        nonsig = sum(v for k, v in cov.items() if k != 'sig')
        print(f'  {p.name:<26} {mark:<34} '
              f'nodi risolti per firma {cov["sig"]}, per ripiego {nonsig}')

    print(f'\nleave-one-out: {ok}/{len(docs)} byte-identici')
    print(f'risoluzioni di ripiego totali: {dict(fallback_tot)}')
    for name, line, unk in worst[:5]:
        print(f'\n  ✗ {name} r{line+1} — percorsi non coperti:')
        for k, v in unk:
            print(f'      {k}  x{v}')

    if args.extra:
        print('\n=== generalizzazione a file di tipo diverso ===')
        table = FormatTable().learn(d for _, d in docs)
        for p in files_in(Path(args.extra)):
            d = parse_file(p)
            got = serialize(d, table, rebuild=True)
            cov, unknown = coverage(table, d)
            if got == d.raw:
                print(f'  ok      {p.name}  (firma {cov["sig"]}, '
                      f'ripiego {sum(v for k,v in cov.items() if k!="sig")})')
            else:
                o, g = d.raw.splitlines(), got.splitlines()
                first = next((k for k, (a, b) in enumerate(zip(o, g)) if a != b),
                             min(len(o), len(g)))
                print(f'  DIVERSO {p.name}  prima differenza r{first+1}')
                for k, v in unknown.most_common(6):
                    print(f'            non coperto: {k} x{v}')
                for k in range(max(0, first - 1), min(len(o), first + 4)):
                    print(f'            - {o[k]}')
                for k in range(max(0, first - 1), min(len(g), first + 4)):
                    print(f'            + {g[k]}')


if __name__ == '__main__':
    sys.exit(main())
