"""Leggere il Groove MIDI Dataset: velocity e micro-tempistica di batteristi veri.

PERCHE' ESISTE
--------------
La scala delle velocity che il progetto usa viene dal web, e l'ascolto
dell'utente l'ha gia' dovuta correggere una volta: i pattern del primo dub
erano quasi giusti e PIATTI. Qui ci sono 1150 esecuzioni annotate per stile e
per BPM, suonate su un kit elettronico, con la velocity e l'onset esatto di
ogni colpo. La micro-tempistica E' lo scarto di quegli onset dalla griglia.

Il dataset sta in `to-read/MIDI/groove-v1.0.0-midionly/`, che NON e'
versionato: e' opera di terzi. I test che lo usano saltano se non c'e', come
quelli del corpus e quelli di `wjazz.py`.

IL CONFINE
----------
Questo modulo LEGGE. Non tocca mai un `Document`, non costruisce `Note`, non
sa cosa sia una clip. Il verbo che scrive -- `MU.applica_groove()` -- sta in
`musica.py` con tutti gli altri verbi. E' lo stesso confine di `wjazz.py`.

PERCHE' NON DENTRO `midi.py`
----------------------------
`midi.py` e' il lettore GENERICO di Standard MIDI File, validato nota per nota
contro `mido`. Questo e' un DATASET: `info.csv`, le etichette di stile, `beat`
contro `fill` non sono roba di MIDI. Metterle nel lettore comune lo
sporcherebbero per sempre -- la stessa ragione per cui il dialetto di Weimar
sta in `wjazz.py` e non in `MU.SIGLE`.

IL PREFISSO, NON LA SOTTOSTRINGA
---------------------------------
Cercare `reggae` dentro l'etichetta prenderebbe anche `latin/reggaeton` e
`latin/brazilian-sambareggae`, che reggae non sono.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import NamedTuple

#: Il file che etichetta ogni esecuzione. Sta nella radice del dataset.
INVENTARIO = 'info.csv'


class Esecuzione(NamedTuple):
    """Una riga di `info.csv`, con i soli campi che servono."""

    id: str
    drummer: str
    style: str
    bpm: int
    beat_type: str
    time_signature: str
    midi_filename: str
    duration: float


def per_prefisso(valore: str, filtro: str) -> bool:
    """`reggae` prende `reggae` e `reggae/slow`, NON `latin/reggaeton`.

    E' la regola di filtro di questo modulo, ed e' una funzione a se' perche'
    e' esattamente il punto in cui e' facile sbagliare.
    """
    return valore == filtro or valore.startswith(filtro + '/')


def _righe(base: Path | str) -> list[dict[str, str]]:
    """Le righe grezze di `info.csv`. Solleva se il dataset non c'e'."""
    inventario = Path(base) / INVENTARIO
    if not inventario.exists():
        raise FileNotFoundError(str(inventario))
    with inventario.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def elenco(base: Path | str, *, style: str | None = None,
           beat_type: str | None = None, drummer: str | None = None,
           time_signature: str | None = None) -> list[Esecuzione]:
    """Le esecuzioni che soddisfano i filtri. `style` va per PREFISSO."""
    fuori = []
    for r in _righe(base):
        if style is not None and not per_prefisso(r['style'], style):
            continue
        if beat_type is not None and r['beat_type'] != beat_type:
            continue
        if drummer is not None and r['drummer'] != drummer:
            continue
        if time_signature is not None and r['time_signature'] != time_signature:
            continue
        fuori.append(Esecuzione(
            id=r['id'], drummer=r['drummer'], style=r['style'],
            bpm=int(r['bpm']), beat_type=r['beat_type'],
            time_signature=r['time_signature'],
            midi_filename=r['midi_filename'], duration=float(r['duration'])))
    return fuori


def valori(base: Path | str, colonna: str) -> dict[str, int]:
    """Quali etichette esistono in una colonna, e quante volte."""
    righe = _righe(base)
    if righe and colonna not in righe[0]:
        raise ValueError(
            f'colonna {colonna!r} assente: ci sono {sorted(righe[0])}')
    conto: dict[str, int] = {}
    for r in righe:
        conto[r[colonna]] = conto.get(r[colonna], 0) + 1
    return dict(sorted(conto.items(), key=lambda kv: (-kv[1], kv[0])))


def _una(base: Path | str, id: str) -> Esecuzione:
    """L'esecuzione con quell'id, o un errore che dice quante ce ne sono."""
    for e in elenco(base):
        if e.id == id:
            return e
    raise ValueError(f'nessuna esecuzione con id {id!r}')


def racconta(base: Path | str, id: str) -> str:
    """Cosa c'e' in un'esecuzione, in una riga."""
    e = _una(base, id)
    return (f'{e.id}: {e.drummer}, {e.style}, {e.bpm} BPM, '
            f'{e.beat_type}, {e.time_signature}, {e.duration:.1f} s')
