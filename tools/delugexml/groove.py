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
import math
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
    tutte = elenco(base)
    for e in tutte:
        if e.id == id:
            return e
    esempi = ', '.join(e.id for e in tutte[:3])
    raise ValueError(
        f'nessuna esecuzione con id {id!r}: ce ne sono {len(tutte)}, per '
        f'esempio {esempi} -- vedi elenco() per la lista completa')


def origine(posizioni, passo: float, *, finestra: float = 0.25) -> float:
    """Lo scarto comune di tutti gli onset dalla griglia, in tick, CON SEGNO.

    MEDIA CIRCOLARE, e non e' pignoleria. La fase dentro il passo e' una
    grandezza che GIRA: un colpo a 23 tick su 24 e' un anticipo di 1, non un
    ritardo di 23, e la media aritmetica di 1 e 23 darebbe 12 -- cioe' il
    contrario di zero. Si mediano i versori e si torna indietro.

    Il risultato sta in (-passo/2, +passo/2]. Va SOTTRATTO dalle posizioni.

    SI STIMA SOLO SUI COLPI VICINI ALLA GRIGLIA, dentro `finestra`. Se no
    lo swing la sporca: un levare swingato sta a 2/3 di movimento, cioe' a
    2,67 passi, e la sua fase (-8 tick su 24) entrerebbe nella media come se
    fosse uno scarto comune. Non lo e': e' swing, e lo toglie il passo dopo.

    IL LIMITE, DICHIARATO: uno scarto comune piu' grande di un quarto di
    passo cadrebbe fuori dalla finestra e non verrebbe visto. Nel dataset
    misurato vale circa un tick su ventiquattro, quindi la finestra sta larga
    dieci volte il necessario -- ma se un giorno un corpus diverso desse
    origine zero su dati palesemente storti, e' il primo posto da guardare.

    PERCHE' ESISTE. Misurato su `drummer1/session3/2_jazz-swing_185_beat_4-4`:
    ride, kick, rullante e charleston hanno TUTTI il picco a 0,958 del
    movimento. Tutti insieme vuol dire che non e' feel, e' l'origine. La
    prima nota del file sta a tick 1287, e il tick 0 non e' un movimento.

    Quello che si toglie NON si dichiara come feel: a 185 BPM il 5% vale
    16 ms, indistinguibile dalla latenza di cattura del kit elettronico su
    cui il dataset e' registrato. Il feel e' cio' che RESTA dopo averlo tolto.
    """
    vicini = []
    for p in posizioni:
        scarto = p % passo
        if scarto > passo / 2:
            scarto -= passo             # la fase gira: 23 su 24 e' -1
        # confronto stretto (< non <=): NON e' per tenere fuori i levare
        # swingati -- quelli stanno a 8 tick su 24, ben oltre il bordo a 6
        # (finestra di default 0.25 * passo), un terzo di margine, non ci
        # arrivano vicino. E' che il bordo va deciso in un verso solo e
        # dichiarato: un colpo con scarto ESATTAMENTE uguale al bordo deve
        # avere un esito fisso, perche' il Task 4 (swing) e il Task 5 (i
        # groove template) si appoggiano a questa soglia.
        if abs(scarto) < finestra * passo:
            vicini.append(scarto)
    if not vicini:
        return 0.0
    fasi = [s / passo * 2 * math.pi for s in vicini]
    x = sum(math.cos(a) for a in fasi) / len(fasi)
    y = sum(math.sin(a) for a in fasi) / len(fasi)
    if abs(x) < 1e-12 and abs(y) < 1e-12:
        return 0.0                      # fasi sparse: nessuna origine comune
    return math.atan2(y, x) / (2 * math.pi) * passo


def racconta(base: Path | str, id: str) -> str:
    """Cosa c'e' in un'esecuzione, in una riga."""
    e = _una(base, id)
    return (f'{e.id}: {e.drummer}, {e.style}, {e.bpm} BPM, '
            f'{e.beat_type}, {e.time_signature}, {e.duration:.1f} s')
