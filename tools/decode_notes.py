"""Ricava il layout binario dei blob di note (`noteData*`) provandolo sui dati.

Il Deluge impacchetta le note di una noteRow in un unico attributo esadecimale.
Il layout non e' documentato. Qui non lo si indovina: si enumerano le larghezze
di record possibili e, per ognuna, si verifica un invariante forte —

    le posizioni delle note dentro una riga devono essere strettamente
    crescenti e comprese fra 0 e la lunghezza della clip

— su tutte le noteRow del corpus. Una larghezza che soddisfa l'invariante
ovunque, con migliaia di campioni, e' praticamente certa.

Uso: python decode_notes.py <dir> [--attr noteDataWithLift]
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402

NOTE_ATTRS = ('noteDataWithLift', 'noteDataWithSplitProb', 'noteData')


def collect_rows(root: Path):
    """(nome_attributo, blob_hex, lunghezza_clip, y) per ogni noteRow."""
    out = []
    for p in sorted(root.rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue
        for path, node in doc.path_iter():
            if node.tag != 'noteRow':
                continue
            clip_len = None
            # risali: la lunghezza sta sull'instrumentClip antenato
            for a in ANCESTORS.get(id(node), []):
                pass
            for attr in NOTE_ATTRS:
                v = node.get(attr)
                if v:
                    out.append((p.name, attr, v, clip_len, node.get('y')))
    return out


ANCESTORS: dict = {}


def collect_with_len(root: Path):
    out = []
    for p in sorted(root.rglob('*.XML')):
        if p.name.startswith('._'):
            continue
        doc = parse_file(p)
        if doc.root.tag != 'song':
            continue

        def walk(node, clip_len):
            if node.tag in ('instrumentClip', 'audioClip') and node.has('length'):
                clip_len = int(node.get('length'))
            if node.tag == 'noteRow':
                for attr in NOTE_ATTRS:
                    v = node.get(attr)
                    if v:
                        out.append((p.name, attr, v, clip_len))
            for c in node.children:
                walk(c, clip_len)

        for r in doc.roots:
            walk(r, None)
    return out


def try_width(blob: str, width: int, pos_hex: int = 8):
    """Decodifica assumendo record da `width` char, posizione nei primi 8."""
    h = blob[2:] if blob.startswith('0x') else blob
    if len(h) % width:
        return None
    recs = [h[i:i + width] for i in range(0, len(h), width)]
    try:
        return [int(r[:pos_hex], 16) for r in recs]
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    args = ap.parse_args()

    rows = collect_with_len(Path(args.root))
    by_attr = defaultdict(list)
    for _, attr, blob, clen in rows:
        by_attr[attr].append((blob, clen))
    print(f'noteRow con dati: {len(rows)}')
    for a, v in by_attr.items():
        print(f'  {a:<24} {len(v)}')

    for attr, items in by_attr.items():
        print(f'\n=== {attr} ===')
        lens = Counter(len(b[2:] if b.startswith("0x") else b) for b, _ in items)
        print('  lunghezze blob (in char hex), i 6 valori piu comuni:')
        for L, n in lens.most_common(6):
            divisors = [w for w in range(12, 33, 2) if L % w == 0]
            print(f'    {L:>7}  x{n:<5}  divisibile per: {divisors}')

        print('  test invariante "posizioni crescenti e < lunghezza clip":')
        for width in range(12, 33, 2):
            ok = bad = skipped = 0
            maxpos_over = 0
            for blob, clen in items:
                pos = try_width(blob, width)
                if pos is None:
                    skipped += 1
                    continue
                good = all(pos[i] < pos[i + 1] for i in range(len(pos) - 1))
                if good and clen:
                    good = pos[-1] < clen
                    if not good:
                        maxpos_over += 1
                ok += good
                bad += not good
            total = ok + bad
            if total == 0:
                continue
            pct = 100 * ok / total
            flag = '  <== COERENTE' if pct == 100 and total > 50 else ''
            print(f'    width {width:>2}: {ok:>5}/{total:<5} ({pct:5.1f}%) '
                  f'non decodificabili {skipped}{flag}')


if __name__ == '__main__':
    sys.exit(main())
