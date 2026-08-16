"""Raggruppa gli errori di parsing XML per tipo, con esempi di contesto.

Uso: python error_taxonomy.py <dir> [--fw c1.3.0]
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

FW_RE = re.compile(r'firmwareVersion\s*=\s*"([^"]*)"')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--fw', help='filtra per firmwareVersion')
    ap.add_argument('--examples', type=int, default=2)
    args = ap.parse_args()

    groups = defaultdict(list)   # (kind, fw) -> [(file, line, col, context)]
    total = 0

    for f in sorted(Path(args.root).rglob('*')):
        if not f.is_file() or f.suffix.lower() != '.xml' or f.name.startswith('._'):
            continue
        raw = f.read_bytes().decode('utf-8', 'replace')
        m = FW_RE.search(raw[:4096])
        fw = m.group(1) if m else '(assente)'
        if args.fw and fw != args.fw:
            continue
        total += 1
        try:
            ET.fromstring(raw)
            continue
        except ET.ParseError as e:
            kind = re.sub(r'[:,] line \d+, column \d+', '', str(e)).strip()
            line, col = e.position
            lines = raw.split('\n')
            ctx = lines[line - 1][:120] if 0 < line <= len(lines) else ''
            groups[(kind, fw)].append((f.name, line, col, ctx))

    print(f'file esaminati: {total}')
    nbad = sum(len(v) for v in groups.values())
    print(f'file rifiutati: {nbad}\n')

    for (kind, fw), items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        print(f'[{len(items):>4}]  {kind}   (fw {fw})')
        for name, line, col, ctx in items[:args.examples]:
            print(f'         {name} r{line}c{col}: {ctx.strip()[:100]}')
        print()


if __name__ == '__main__':
    sys.exit(main())
