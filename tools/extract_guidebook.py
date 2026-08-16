"""Estrae il testo del guidebook del Deluge in un file indicizzabile.

Il PDF non contiene caratteri spazio: le parole sono separate solo dalla
posizione sulla pagina, quindi il testo estratto esce tutto attaccato
("Theseoctaveswillfollow..."). Resta leggibile, e soprattutto resta
cercabile se si cerca senza spazi.

Aggiunge un marcatore per pagina, con il numero stampato sulla pagina quando
si riesce a leggerlo, perche' l'indice del manuale usa quello e non l'indice
del PDF (c'e' uno scarto di circa 6).

Uso: python extract_guidebook.py <pdf> -o <out.txt>
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit('serve pypdf:  .venv\\Scripts\\python.exe -m pip install pypdf')

# le pagine iniziano con "<numero>DelugeOfficialManual" o simili
PRINTED = re.compile(r'^\s*(\d{1,3})\s*Deluge', re.M)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf')
    ap.add_argument('-o', '--out', required=True)
    a = ap.parse_args()

    r = PdfReader(a.pdf)
    chunks = []
    mapping = []
    for i, page in enumerate(r.pages):
        t = page.extract_text() or ''
        m = PRINTED.search(t)
        printed = m.group(1) if m else '?'
        mapping.append((i + 1, printed))
        chunks.append(f'\n\n===== PDF {i+1}  |  stampata {printed} =====\n{t}')

    Path(a.out).write_text(''.join(chunks), encoding='utf-8')
    print(f'{len(r.pages)} pagine -> {a.out}')

    # scarto fra numero PDF e numero stampato, utile per navigare l'indice
    offs = [p - int(s) for p, s in mapping if s != '?']
    if offs:
        from collections import Counter
        c = Counter(offs)
        print(f'scarto PDF - stampata: {c.most_common(3)}')


if __name__ == '__main__':
    sys.exit(main())
