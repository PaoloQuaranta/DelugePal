"""Scansiona tutti gli XML della SD e riporta firmwareVersion / earliestCompatibleFirmware.

Uso: python scan_versions.py <root_sd> [--csv out.csv]

Non modifica nulla. Legge solo l'header di ogni file (primi 4 KB) per velocita'.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

FW_RE = re.compile(rb'firmwareVersion\s*=\s*"([^"]*)"')
EARLIEST_RE = re.compile(rb'earliestCompatibleFirmware\s*=\s*"([^"]*)"')
ROOT_RE = re.compile(rb'<\s*([A-Za-z_][\w:.-]*)')


def head(path: Path, n: int = 8192) -> bytes:
    with path.open('rb') as f:
        return f.read(n)


def root_tag(blob: bytes) -> str:
    # salta la dichiarazione xml
    body = blob.split(b'?>', 1)[-1]
    m = ROOT_RE.search(body)
    return m.group(1).decode('ascii', 'replace') if m else '?'


def scan(root: Path):
    rows = []
    for p in sorted(root.rglob('*')):
        if not p.is_file() or p.suffix.lower() != '.xml':
            continue
        if 'System Volume Information' in str(p):
            continue
        try:
            blob = head(p)
        except OSError as e:
            rows.append((str(p), 'ERR', str(e), '', 0))
            continue
        fw = FW_RE.search(blob)
        ea = EARLIEST_RE.search(blob)
        rows.append((
            str(p),
            root_tag(blob),
            fw.group(1).decode('ascii', 'replace') if fw else '',
            ea.group(1).decode('ascii', 'replace') if ea else '',
            p.stat().st_size,
        ))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--csv')
    args = ap.parse_args()

    rows = scan(Path(args.root))

    counts = {}
    for _, tag, fw, _, _ in rows:
        counts[(tag, fw)] = counts.get((tag, fw), 0) + 1

    print(f'File XML trovati: {len(rows)}\n')
    print(f'{"root tag":<16} {"firmwareVersion":<24} {"n":>5}')
    print('-' * 48)
    for (tag, fw), n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f'{tag:<16} {fw or "(assente)":<24} {n:>5}')

    if args.csv:
        with open(args.csv, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['path', 'root_tag', 'firmwareVersion',
                        'earliestCompatibleFirmware', 'size'])
            w.writerows(rows)
        print(f'\nCSV: {args.csv}')


if __name__ == '__main__':
    sys.exit(main())
