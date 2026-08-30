"""Ri-deriva `sound.COPPIE_OSSERVATE` dal corpus e ne stampa il sorgente.

    .venv/Scripts/python.exe tools/genera_coppie_cable.py

Stampa il blocco Python da incollare in `tools/delugexml/sound.py`, e in
coda dice cosa e' cambiato rispetto alla tabella che c'e' adesso. Con
`--scrivi` lo sostituisce da se'.

PERCHE' ESISTE
--------------
La tabella era «generata da uno script e poi incollata» -- lo dice il suo
commento in `sound.py` -- ma lo script NON era nel repo. Un incollaggio
irripetibile: chi aggiungeva un file a `refs/` vedeva
`test_patch_cable_tabelle` diventare rosso e non aveva modo di rifare la
tabella se non a mano. E' successo il 29 agosto 2026, scaricando quattro
preset per il primo pezzo jazz.

⚠️ COSA E' QUESTA TABELLA, E COSA NON E'. Non e' una specifica: e' il grado
di battutezza di un percorso, che `sound.set_patch_cable()` riferisce per
informare. Il corpus dice cosa l'utente ha suonato, NON cosa il firmware
accetta -- il firmware espone 56 destinazioni, il corpus ne usa una
quarantina. Per sapere cosa il firmware accetta si guardano `param_ids.py` e
il guidebook, mai il corpus. E' la regola 0 di `HANDOFF.md`, e questa tabella
e' precisamente il caso in cui e' facile violarla.

⚠️ QUINDI RIGENERARLA INCIDE IL CORPUS LOCALE IN UN FILE VERSIONATO, e non e'
una decisione da prendere di slancio: i conteggi che escono descrivono la
libreria di CHI LANCIA lo script. Va fatto quando il corpus e' quello giusto,
non ogni volta che il test diventa rosso.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import parse_file                            # noqa: E402
from delugexml import sound as SND                          # noqa: E402

RADICE = Path(__file__).resolve().parent.parent
SORGENTE = RADICE / 'tools' / 'delugexml' / 'sound.py'
#: Le stesse radici che `test_patch_cable_tabelle` percorre: se le due liste
#: divergessero, la tabella e il suo test guarderebbero corpora diversi.
RADICI = (RADICE / 'refs', RADICE / 'corpus_versions')

APERTURA = 'COPPIE_OSSERVATE: dict[tuple[str, str], int] = {'
LARGHEZZA = 79


def deriva() -> tuple[Counter, int]:
    """Le coppie sorgente-destinazione osservate, col numero di volte."""
    coppie: Counter = Counter()
    n_file = 0
    for radice in RADICI:
        if not radice.exists():
            continue
        for p in sorted(radice.rglob('*.XML')):
            try:
                doc = parse_file(p)
            except Exception:                       # noqa: BLE001, PERF203
                continue
            n_file += 1
            pila = [doc.root]
            while pila:
                n = pila.pop()
                if n.tag == 'patchCable':
                    s, d = n.get('source'), n.get('destination')
                    if s and d and d != 'none':
                        coppie[(s, d)] += 1
                pila.extend(n.children)
    return coppie, n_file


def sorgente(coppie: Counter, n_file: int) -> str:
    """Il blocco Python, formattato come quello che c'e' gia'."""
    voci = [f"({s!r}, {d!r}): {n}," for (s, d), n in
            sorted(coppie.items(), key=lambda kv: (-kv[1], kv[0]))]
    righe, corrente = [], '   '
    for v in voci:
        if len(corrente) + 1 + len(v) > LARGHEZZA:
            righe.append(corrente)
            corrente = '   '
        corrente += ' ' + v
    if corrente.strip():
        righe.append(corrente)
    testa = (
        "#: Le coppie sorgente-destinazione **osservate**, col numero di\n"
        "#: volte. NON e' una specifica: e' il grado di battutezza di un\n"
        "#: percorso, usato solo per informare nel rapporto di\n"
        "#: `set_patch_cable`. Si ri-deriva con `tools/genera_coppie_cable.py`\n"
        f"#: e la ricontrolla `test_patch_cable_tabelle`. Ultimo giro:\n"
        f"#: {n_file} file, {sum(coppie.values())} cable, {len(coppie)} coppie.\n"
    )
    return testa + APERTURA + '\n' + '\n'.join(righe) + '\n}'


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--scrivi', action='store_true',
                    help='sostituisce la tabella in sound.py invece di stamparla')
    args = ap.parse_args()

    coppie, n_file = deriva()
    if len(coppie) < 50:
        print(f'servono le song del corpus: trovate {len(coppie)} coppie in '
              f'{n_file} file. Vedi README, "Bring your own corpus".')
        return 1

    vecchie = SND.COPPIE_OSSERVATE
    nuove = dict(coppie)
    print(f'{n_file} file, {sum(coppie.values())} cable, {len(coppie)} coppie '
          f'(in tabella ce ne sono {len(vecchie)})\n')
    aggiunte = sorted(set(nuove) - set(vecchie))
    tolte = sorted(set(vecchie) - set(nuove))
    mosse = sorted(k for k in set(nuove) & set(vecchie)
                   if nuove[k] != vecchie[k])
    for eti, elenco in (('coppie NUOVE', aggiunte), ('coppie SPARITE', tolte)):
        if elenco:
            print(f'{eti}: {len(elenco)}')
            for k in elenco[:12]:
                print(f'    {k}  x{nuove.get(k, vecchie.get(k))}')
    if mosse:
        print(f'conteggi cambiati: {len(mosse)}')
        for k in mosse[:12]:
            print(f'    {k}  {vecchie[k]} -> {nuove[k]}')
    if not (aggiunte or tolte or mosse):
        print('la tabella coincide gia col corpus: niente da fare')
        return 0

    blocco = sorgente(coppie, n_file)
    if not args.scrivi:
        print('\n' + '-' * LARGHEZZA)
        print(blocco)
        print('-' * LARGHEZZA)
        print('\n(--scrivi per sostituirla in sound.py)')
        return 0

    testo = SORGENTE.read_text(encoding='utf-8')
    i = testo.find(APERTURA)
    if i < 0:
        print(f'non trovo {APERTURA!r} in {SORGENTE}')
        return 1
    # ⚠️ si risale al commento `#:` che la precede, perche' porta il conteggio
    # dell'ultimo giro e resterebbe a dire un numero vecchio
    while i > 0:
        prec = testo.rfind('\n', 0, i - 1) + 1
        if not testo[prec:i].startswith('#:'):
            break
        i = prec
    j = testo.find('\n}', testo.find(APERTURA)) + 2
    # ⚠️ `write_bytes` e non `write_text`: su Windows quest'ultima traduce il
    # fine riga e riscriverebbe tutto il file. HANDOFF, «Cosa NON rifare».
    SORGENTE.write_bytes((testo[:i] + blocco + testo[j:]).encode('utf-8'))
    print(f'\nscritta in {SORGENTE}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
