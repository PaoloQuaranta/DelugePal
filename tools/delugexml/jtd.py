"""Leggere il Jazz Trio Database: il trio che suona INSIEME.

PERCHE' ESISTE
--------------
Fino al 1 settembre 2026 l'handoff diceva, in tre punti, che «nessun corpus
in casa ha l'insieme che suona insieme -- non e' questione di quanti dati, e'
che il dato non c'e'», e da li' faceva discendere che il prossimo passo fosse
un lettore di partiture MusicXML. La riga era falsa in due modi:

  1. il dato ESISTE e ha una licenza: il Jazz Trio Database (Cheston,
     Schlichting, Cross, Harrison -- TISMIR 2024, MIT) porta 1294 esecuzioni
     di trio jazz con gli onset di PIANO, BASSO E BATTERIA allineati agli
     STESSI beat;
  2. il MusicXML non l'avrebbe risolta comunque: nel piu' grande corpus
     libero (PDMX, 250 000 spartiti di pubblico dominio) oltre il 90% ha meno
     di cinque parti e piu' della meta' sono pezzi solistici. Niente batteria.

Serve alla casella 5 di `docs/repertori/jazz.md`, «ruoli e spartizione», che
il 30 agosto 2026 ha fermato tre lavori in un giorno solo.

COSA PORTA, E COSA NO
---------------------
Porta: quando ciascuno dei tre ha suonato, rispetto a un beat comune e alla
posizione nella battuta; e le altezze del PIANO, che ha il suo MIDI.

NON porta: le altezze di basso e batteria, e nemmeno QUALE pezzo di batteria
ha suonato -- gli onset sono aggregati. Qualunque affermazione del tipo «il
rullante fa X» non e' ricavabile da qui, e va rifiutata invece che stimata.

⚠️ E le annotazioni sono AUTOMATICHE: separazione di sorgente, poi
rilevamento di onset e beat, con F-measure dichiarata 0,94. Solo 34 brani su
1294 hanno una validazione manuale; il sottoinsieme curato JTD-300 ne ha 300.

QUESTO MODULO NON DECIDE NIENTE DI MUSICALE
-------------------------------------------
Restituisce cio' che il corpus dice. Ogni soglia -- cosa sia «insieme», cosa
sia un accordo, quante battute servano per contare -- sta in
`tools/misura_spartizione.py` con accanto la frase che la giustifica. E' la
stessa divisione che c'e' fra `wjazz.py` e `misura_melodia.py`.

LO ZIP NON SI DECOMPRIME
------------------------
Regola di HANDOFF §6-duodecies: `zipfile` e' stdlib, i membri si leggono in
memoria. Chi cicla su tante tracce apre lo zip UNA volta con `apri()` e passa
l'oggetto; chi fa una chiamata sola puo' passare il percorso, e in quel caso
la funzione apre e richiude da se'.
"""
from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path
from typing import NamedTuple

from . import midi

#: La cartella che lo zip si porta dentro. Cambia col numero di versione del
#: corpus, quindi sta qui e non sparsa nel codice.
RADICE = 'jazz-trio-database-v02'

#: I tre strumenti, nei nomi che il corpus usa nelle sue colonne e nei suoi
#: nomi di file. Non tradotti apposta: sono chiavi di dati altrui.
STRUMENTI = ('piano', 'bass', 'drums')


class Brano(NamedTuple):
    """Un'esecuzione, coi campi che servono per sceglierla."""

    fname: str
    titolo: str
    album: str
    anno: int | None
    pianista: str
    bassista: str
    batterista: str
    metro: int
    tempo: float | None
    #: sta nel sottoinsieme curato JTD-300 (`in_30_corpus`)
    curato: bool
    #: ha una validazione manuale (`has_annotations`): solo 34 su 1294
    validato: bool

    def __str__(self) -> str:
        t = f'{self.tempo:.0f} bpm' if self.tempo else 'tempo ignoto'
        return (f'{self.pianista} - {self.titolo} ({self.anno}), '
                f'basso {self.bassista}, batteria {self.batterista}, '
                f'{self.metro}/4, {t}')


def apri(path: Path | str) -> zipfile.ZipFile:
    """Lo zip del corpus. Solleva `FileNotFoundError` se non c'e'.

    L'eccezione e' quella giusta di proposito: la suite la traduce in un
    SALTO, perche' il corpus non appartiene a questo repo.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))
    return zipfile.ZipFile(p)


def _zip(sorgente: zipfile.ZipFile | Path | str) -> tuple[zipfile.ZipFile, bool]:
    """Lo zip, e se l'abbiamo aperto noi (e quindi tocca a noi chiuderlo)."""
    if isinstance(sorgente, zipfile.ZipFile):
        return sorgente, False
    return apri(sorgente), True


def _senza_nan(v):
    """`metadata.json` usa `NaN` per «non lo so»: diventa `None`.

    `json` di Python accetta `NaN` -- non e' JSON stretto, e altri lettori lo
    rifiutano. Normalizzarlo all'ingresso evita che un `float('nan')` giri
    per il codice, dove ogni confronto con lui e' falso, `==` compreso.
    """
    if isinstance(v, float) and v != v:
        return None
    if isinstance(v, dict):
        return {k: _senza_nan(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_senza_nan(x) for x in v]
    return v


def metadati(sorgente, fname: str) -> dict:
    """Il `metadata.json` di un brano, coi `NaN` gia' resi `None`."""
    z, nostro = _zip(sorgente)
    try:
        return _senza_nan(json.loads(z.read(f'{RADICE}/{fname}/metadata.json')))
    finally:
        if nostro:
            z.close()


def _in_brano(m: dict, fname: str) -> Brano:
    mus = m.get('musicians') or {}
    anno = m.get('recording_year')
    return Brano(
        fname=fname,
        titolo=m.get('track_name') or '',
        album=m.get('album_name') or '',
        anno=int(anno) if anno else None,
        pianista=mus.get('pianist') or '',
        bassista=mus.get('bassist') or '',
        batterista=mus.get('drummer') or '',
        metro=int(m.get('time_signature') or 4),
        tempo=m.get('tempo'),
        curato=bool(m.get('in_30_corpus')),
        validato=bool(m.get('has_annotations')),
    )


def nomi(sorgente) -> list[str]:
    """I `fname` dei brani, in ordine alfabetico."""
    z, nostro = _zip(sorgente)
    try:
        coda = '/metadata.json'
        return sorted(n.split('/')[1] for n in z.namelist() if n.endswith(coda))
    finally:
        if nostro:
            z.close()


def brano(sorgente, fname: str) -> Brano:
    """Un brano per nome."""
    return _in_brano(metadati(sorgente, fname), fname)


def elenco(sorgente, *, pianista: str | None = None,
           bassista: str | None = None, batterista: str | None = None,
           metro: int | None = None, curati: bool = False,
           limite: int | None = None) -> list[Brano]:
    """I brani che rispondono ai filtri.

    I nomi dei musicisti sono quelli del corpus, per esteso e con le
    maiuscole («Ray Drummond»): un nome scritto diversamente da' una lista
    vuota invece di un errore. `curati=True` restringe al sottoinsieme
    JTD-300, i 300 brani su cui gli autori hanno lavorato di piu'.
    """
    z, nostro = _zip(sorgente)
    try:
        fuori = []
        for fname in nomi(z):
            b = _in_brano(metadati(z, fname), fname)
            if pianista is not None and b.pianista != pianista:
                continue
            if bassista is not None and b.bassista != bassista:
                continue
            if batterista is not None and b.batterista != batterista:
                continue
            if metro is not None and b.metro != metro:
                continue
            if curati and not b.curato:
                continue
            fuori.append(b)
            if limite is not None and len(fuori) >= limite:
                break
        return fuori
    finally:
        if nostro:
            z.close()


class Beat(NamedTuple):
    """Un beat, e chi c'era sopra.

    `scarti` vale, per ogni strumento, l'onset MENO l'istante del beat: il
    segno dice chi tira avanti e chi trattiene. `None` vuol dire che quello
    strumento NON ha suonato su questo beat, ed e' un'informazione, non un
    buco nei dati -- ⚠️ salvo quando e' un fallimento del rilevatore, che e'
    il controllo 2 di `tools/controlla_jtd.py`.
    """

    indice: int
    istante: float
    #: 1..metro, da `metre_auto`. 1 e' il tempo forte.
    posizione: int
    scarti: dict[str, float | None]

    def tace(self, strumento: str) -> bool:
        return self.scarti[strumento] is None


def _numero(testo: str | None) -> float | None:
    """Una cella di CSV: `None` se e' vuota o `nan`."""
    testo = (testo or '').strip()
    if not testo or testo.lower() == 'nan':
        return None
    return float(testo)


def griglia(sorgente, fname: str) -> list[Beat]:
    """I beat di un brano, con la posizione metrica e i tre allineamenti."""
    z, nostro = _zip(sorgente)
    try:
        testo = z.read(f'{RADICE}/{fname}/beats.csv').decode('utf-8')
    finally:
        if nostro:
            z.close()

    fuori = []
    for i, riga in enumerate(csv.DictReader(io.StringIO(testo))):
        istante = _numero(riga['beats'])
        posizione = _numero(riga['metre_auto'])
        if istante is None or posizione is None:
            # Non si e' mai visto su 32 110 beat controllati, ma un beat senza
            # istante o senza posizione non e' un beat: si scarta invece di
            # inventargli un posto.
            continue
        scarti = {}
        for s in STRUMENTI:
            o = _numero(riga[s])
            scarti[s] = None if o is None else o - istante
        fuori.append(Beat(indice=i, istante=istante, posizione=int(posizione),
                          scarti=scarti))
    return fuori


def microtiming(sorgente, fname: str, strumento: str = 'bass') -> list[float]:
    """La SEQUENZA delle deviazioni di uno strumento dal beat, in secondi, in
    ordine di tempo, per i soli beat su cui ha suonato.

    E' il `float` di UN esecutore nominato: nota per nota di quanto arriva
    prima (-) o dopo (+) il beat. Serve a dare a un basso scritto il microtiming
    che non ha -- vedi `musica.applica_microtiming()` e
    `docs/istruzioni/aggancio.md`. Come tutto qui, RESTITUISCE il dato e non
    decide niente: la scelta di quale esecuzione, e come applicarla, sta altrove.

    ⚠️ E' [OSS] su quell'esecuzione, non [MIS] su un repertorio: mediare il
    microtiming di bassisti diversi lo tira verso zero -- la stessa ragione per
    cui il groove template della batteria viene da un'esecuzione sola.
    """
    if strumento not in STRUMENTI:
        raise ValueError(f'strumento {strumento!r}: uno di {STRUMENTI}')
    return [bt.scarti[strumento] for bt in griglia(sorgente, fname)
            if bt.scarti[strumento] is not None]


class Battuta(NamedTuple):
    """Una battuta completa, e cosa ci hanno suonato dentro i tre.

    `onsets` porta gli onset GREZZI, quelli fra i beat compresi: e' la
    differenza fra «il basso ha suonato sul 2» e «il basso ha suonato una
    croma fra il 2 e il 3», e la seconda e' meta' di quello che si vuole
    sapere.
    """

    numero: int
    inizio: float
    fine: float
    beat: tuple[Beat, ...]
    onsets: dict[str, tuple[float, ...]]

    @property
    def densita(self) -> dict[str, int]:
        """Quanti onset per strumento, in questa battuta."""
        return {s: len(self.onsets[s]) for s in STRUMENTI}


class Divisione(NamedTuple):
    """Le battute complete, e quante se ne sono buttate.

    Dichiara lo scarto invece di tacerlo, come `Conversione` in `midi.py`:
    un brano che perde meta' delle battute non e' un brano da cui misurare.
    """

    battute: list[Battuta]
    scartate: int

    def __str__(self) -> str:
        return (f'{len(self.battute)} battute complete, {self.scartate} '
                f'scartate perche incomplete')


def onsets(sorgente, fname: str, strumento: str) -> list[float]:
    """Gli onset grezzi di uno strumento, in secondi e in ordine."""
    if strumento not in STRUMENTI:
        raise ValueError(f'strumento {strumento!r}: usare uno di {STRUMENTI}')
    z, nostro = _zip(sorgente)
    try:
        testo = z.read(
            f'{RADICE}/{fname}/{strumento}_onsets.csv').decode('utf-8')
    finally:
        if nostro:
            z.close()
    # Il file e' una colonna sola, senza intestazione.
    return sorted(float(r) for r in testo.splitlines() if r.strip())


def battute(sorgente, fname: str) -> Divisione:
    """Le battute COMPLETE di un brano, con gli onset dei tre dentro.

    Una battuta e' completa quando i suoi `metro` beat portano le posizioni
    1..metro in fila E c'e' un beat dopo che la chiude: senza quello non si
    sa dove finisce, e una battuta senza fine falserebbe la densita' in
    difetto. I mozziconi si scartano; `scartate` conta quelli che
    COMINCIAVANO sul tempo forte e non si sono chiusi -- il mozzicone di
    testa, che comincia a meta' battuta, non e' una battuta mancata e non si
    conta.
    """
    z, nostro = _zip(sorgente)
    try:
        metro = brano(z, fname).metro
        g = griglia(z, fname)
        tutti = {s: onsets(z, fname, s) for s in STRUMENTI}
    finally:
        if nostro:
            z.close()

    fuori: list[Battuta] = []
    scartate = 0
    attese = list(range(1, metro + 1))
    i = 0
    while i < len(g):
        gruppo = g[i:i + metro]
        completa = (len(gruppo) == metro
                    and [b.posizione for b in gruppo] == attese
                    and i + metro < len(g))
        if not completa:
            if g[i].posizione == 1:
                scartate += 1
            i += 1
            continue
        inizio, fine = gruppo[0].istante, g[i + metro].istante
        fuori.append(Battuta(
            numero=len(fuori),
            inizio=inizio,
            fine=fine,
            beat=tuple(gruppo),
            onsets={s: tuple(o for o in tutti[s] if inizio <= o < fine)
                    for s in STRUMENTI},
        ))
        i += metro
    return Divisione(battute=fuori, scartate=scartate)


def piano(sorgente, fname: str) -> midi.FileMidi:
    """Il `piano_midi.mid` del brano, letto DENTRO lo zip.

    E' l'unico dei tre strumenti che porta le altezze: basso e batteria hanno
    solo gli onset.
    """
    z, nostro = _zip(sorgente)
    try:
        dati = z.read(f'{RADICE}/{fname}/piano_midi.mid')
    finally:
        if nostro:
            z.close()
    return midi.leggi_bytes(dati, nome=f'{fname}/piano_midi.mid')
