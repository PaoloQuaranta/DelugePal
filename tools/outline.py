"""Stampa lo scheletro strutturale di un file Deluge.

Serve a vedere come e' composta una song senza annegare nelle migliaia di
attributi: solo i tag, la loro annidatura, e quali attributi "identificano"
ciascun nodo.

Uso:
    python outline.py <file> [--depth N] [--path song/sessionClips]
                             [--attrs name,length,section]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file           # noqa: E402

# attributi che aiutano a riconoscere un nodo a colpo d'occhio
ID_ATTRS = ('name', 'clipName', 'instrumentPresetName', 'instrumentPresetFolder',
            'trackName', 'y', 'drumIndex', 'length', 'section', 'colourOffset',
            'presetSlot', 'id', 'type', 'source', 'destination', 'controlsParam')


def show(node, depth, maxdepth, prefix, out, want_attrs):
    if depth > maxdepth:
        return
    attrs = want_attrs or ID_ATTRS
    bits = [f'{k}={v!r}' for k, v in node.attrs if k in attrs]
    extra = len(node.attrs) - len(bits)
    label = f'{prefix}{node.tag}'
    if bits:
        label += '  ' + ' '.join(bits)
    if extra:
        label += f'  (+{extra} attr)'
    if node.text:
        label += f'  = {node.text[:40]!r}'
    out.append(label)

    # raggruppa i figli identici consecutivi per non stampare 200 righe uguali
    i = 0
    kids = node.children
    while i < len(kids):
        j = i
        while (j + 1 < len(kids) and kids[j + 1].tag == kids[i].tag
               and not kids[i].children and not kids[j + 1].children):
            j += 1
        n = j - i + 1
        if n > 3 and depth + 1 <= maxdepth:
            show(kids[i], depth + 1, maxdepth, prefix + '  ', out, want_attrs)
            out.append(f'{prefix}  … altri {n-1} <{kids[i].tag}>')
        else:
            for k in range(i, j + 1):
                show(kids[k], depth + 1, maxdepth, prefix + '  ', out, want_attrs)
        i = j + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--depth', type=int, default=4)
    ap.add_argument('--path', help='mostra solo il sottoalbero a questo percorso')
    ap.add_argument('--attrs', help='attributi da mostrare, separati da virgola')
    a = ap.parse_args()

    doc = parse_file(a.file)
    want = tuple(a.attrs.split(',')) if a.attrs else None
    out = []
    if a.path:
        found = 0
        for path, node in doc.path_iter():
            if path == a.path:
                found += 1
                show(node, 0, a.depth, '', out, want)
                out.append('')
        if not found:
            paths = sorted({p for p, _ in doc.path_iter()})
            print(f'percorso non trovato. Disponibili sotto quel livello:')
            for p in paths:
                if p.startswith(a.path.rsplit('/', 1)[0]):
                    print(f'  {p}')
            return 1
    else:
        for r in doc.roots:
            show(r, 0, a.depth, '', out, want)
    print('\n'.join(out))


if __name__ == '__main__':
    sys.exit(main())
