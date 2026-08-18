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
import statistics
from pathlib import Path
from typing import NamedTuple

from . import midi as MI
from .musica import da_bur, in_bur

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


#: La finestra dentro il movimento in cui si cerca il levare, in frazione.
#: Larga abbastanza da prendere sia il dritto (0,5) sia la terzina (0,667) e
#: oltre, stretta abbastanza da non prendere la semicroma a 0,25 ne quella a
#: 0,75, che farebbero passare per levare cio' che levare non e'.
FINESTRA_LEVARE = (0.35, 0.75)


def levare_da_posizioni(posizioni, ppq: float, *,
                        finestra=FINESTRA_LEVARE) -> list[float]:
    """Le posizioni del levare in frazione di movimento, una per movimento.

    Un movimento contribuisce SOLO se ha un colpo sul battere e ESATTAMENTE
    un colpo dentro la finestra. Due colpi vogliono dire semicrome, e li' non
    c'e' una coppia di crome da misurare.
    """
    per_movimento: dict[int, list[float]] = {}
    for p in posizioni:
        # floor-division, non troncamento: per p negativi (li' dove il Task
        # 5 li passera', gia' traslati) -144 // 96 fa -2, non -1 -- il resto
        # p % ppq segue la stessa convenzione e la fase resta corretta.
        per_movimento.setdefault(int(p // ppq), []).append((p % ppq) / ppq)
    fuori = []
    for fasi in per_movimento.values():
        if not any(f < finestra[0] for f in fasi):
            continue                    # senza battere non e' una coppia
        # il bordo superiore resta CHIUSO qui: un colpo esattamente sul
        # bordo (0,75) conta ancora per il conteggio, perche' e' cosi' che
        # la semicroma a quattro colpi (0, 0,25, 0,5, 0,75) finisce con DUE
        # colpi in finestra e si scarta -- vedi il test 'semicrome'.
        dentro = [f for f in fasi if finestra[0] <= f <= finestra[1]]
        # ma da SOLO, un colpo esattamente sul bordo non e' mai il levare:
        # e' la semicroma che FINESTRA_LEVARE dichiara di voler escludere.
        # Il confronto e' quindi stretto solo qui, all'accettazione finale.
        if len(dentro) == 1 and dentro[0] < finestra[1]:
            fuori.append(dentro[0])
    return fuori


def bur_da_posizioni(posizioni, ppq: float, *,
                     finestra=FINESTRA_LEVARE) -> float | None:
    """La BUR MEDIANA dell'esecuzione, o None se non ci sono coppie.

    Mediana e non media: la distribuzione ha una coda lunga di colpi che la
    finestra non ha saputo scartare, e la media ci andrebbe dietro.
    """
    lev = levare_da_posizioni(posizioni, ppq, finestra=finestra)
    if not lev:
        return None
    return in_bur(statistics.median(lev))


class Passo(NamedTuple):
    """Cosa fa uno strumento su un passo della battuta, misurato."""

    passo: int          # 0..15
    velocity: int       # la MEDIANA dei colpi su quel passo
    scarto: float       # tick di residuo, con segno. + spinge, - trattiene
    colpi: int          # quante volte quel passo e' stato colpito


class Profilo(NamedTuple):
    """Il groove template: una esecuzione, misurata e ripulita.

    ⚠️ Viene da UNA esecuzione nominata, non dalla media di un sottoinsieme.
    Mediare il microtiming di batteristi diversi lo tira verso zero, cioe'
    verso la griglia: si perderebbe esattamente cio' che si e' andati a
    prendere. Percio' quello che ne esce e' [OSS] su quell'esecuzione, mentre
    la scala aggregata di `scala()` e' [MIS].
    """

    id: str
    drummer: str
    style: str
    bpm: int
    bur: float | None
    battute: int
    passi: dict[str, list[Passo]]


def _senza_swing(fase: float, levare: float) -> float:
    """Da fase dentro il movimento a fase SENZA swing.

    L'inverso della mappa dello swing, che e' lineare a tratti: la prima
    meta' del movimento e' stata dilatata fino a `levare`, la seconda
    compressa in quel che resta. Con `levare` = 0,5 non cambia niente.
    """
    if levare <= 0 or levare >= 1:
        return fase
    if fase < levare:
        return fase * 0.5 / levare
    return 0.5 + (fase - levare) * 0.5 / (1 - levare)


def profilo_da_colpi(colpi: dict[str, list[tuple[float, int]]], ppq: float,
                     *, id: str = '', drummer: str = '', style: str = '',
                     bpm: int = 0) -> Profilo:
    """Il profilo, da colpi gia' letti: strumento -> [(posizione, velocity)].

    LA CATENA, E L'ORDINE E' LA COSA CHE CONTA:

    1. togli l'ORIGINE della griglia -- se no ogni esecuzione dichiara un
       anticipo che e' latenza di cattura, non feel;
    2. misura il BUR e TOGLILO -- se no lo swing viene applicato due volte,
       una dal firmware e una da qui;
    3. quel che resta e' il RESIDUO: il ride che spinge rispetto al rullante
       che tiene indietro. E' il solo microtiming che il template porta;
    4. aggrega per strumento e per passo, sedici per battuta.
    """
    passo_tick = ppq / 4                            # un 1/16
    tutte = [p for note in colpi.values() for p, _ in note]
    off = origine(tutte, passo_tick)

    bur = bur_da_posizioni([p - off for p in tutte], ppq)
    levare = da_bur(bur) if bur is not None else 0.5

    per_passo: dict[str, dict[int, list[tuple[int, float]]]] = {}
    ultimo = 0
    for nome, note in colpi.items():
        for pos, vel in note:
            p = pos - off
            # il movimento PIU' VICINO, tollerando un colpo appena prima di
            # esso. ⚠️ senza il mezzo passo di grazia un anticipo finirebbe
            # nel movimento precedente con fase 0,99 invece che -0,01, e il
            # residuo uscirebbe grande quanto un movimento intero.
            movimento = math.floor(p / ppq + 0.125)
            fase = p / ppq - movimento
            dritta = (movimento + _senza_swing(fase, levare)) * ppq
            # ⚠️ il passo si decide DOPO aver tolto lo swing: un levare
            # swingato sta a 2,67 passi e si arrotonderebbe al 3.
            passo = round(dritta / passo_tick)
            ultimo = max(ultimo, passo)
            residuo = dritta - passo * passo_tick
            per_passo.setdefault(nome, {}).setdefault(
                passo % 16, []).append((vel, residuo))

    passi = {}
    for nome, dentro in per_passo.items():
        passi[nome] = [
            Passo(passo=k,
                  velocity=int(round(statistics.median(v for v, _ in vs))),
                  scarto=statistics.median(s for _, s in vs),
                  colpi=len(vs))
            for k, vs in sorted(dentro.items())]

    return Profilo(id=id, drummer=drummer, style=style, bpm=bpm, bur=bur,
                   battute=ultimo // 16 + 1, passi=passi)


def profilo(base: Path | str, id: str) -> Profilo:
    """Il profilo di UNA esecuzione del dataset, nominata.

    Le posizioni del file MIDI sono nella risoluzione DEL FILE (nel Groove
    MIDI Dataset, 480 tick per movimento), non in quella del Deluge (96). Se
    si passassero cosi' come sono a `profilo_da_colpi()`, `Passo.scarto`
    uscirebbe in tick-file: un residuo di ~40 ms (grande quanto lo swing
    stesso) uscirebbe come "59 tick", che sembra enorme, mentre in tick
    Deluge e' ~12 -- piccolo, com'e' un residuo dopo aver tolto lo swing.
    `Profilo` non porta con se' il ppq di provenienza, quindi la scala va
    fissata qui, una volta per tutte, sulla stessa risoluzione che usa il
    resto del progetto per scrivere sul Deluge (`musica.TICK_PER_PASSO`,
    `midi.TICK_PER_MOVIMENTO_DELUGE`): e' la stessa conversione che
    `MI._converti()` applica gia' per `MI.batteria()`.
    """
    e = _una(base, id)
    f = MI.leggi(Path(base) / e.midi_filename)
    fattore = MI.TICK_PER_MOVIMENTO_DELUGE / f.ppq
    colpi: dict[str, list[tuple[float, int]]] = {}
    for t in f.tracce:
        for n in t.note:
            nome = MI.GM_PERCUSSIONI.get(n.y)
            if nome is None:
                continue                # una percussione fuori dalla mappa GM
            colpi.setdefault(nome, []).append((n.pos * fattore, n.velocity))
    return profilo_da_colpi(colpi, float(MI.TICK_PER_MOVIMENTO_DELUGE),
                            id=e.id, drummer=e.drummer, style=e.style,
                            bpm=e.bpm)


class Livelli(NamedTuple):
    """La distribuzione delle velocity di uno strumento, su un sottoinsieme.

    ⚠️ `batteristi` NON e' rendicontazione: e' il numero che decide se
    l'affermazione e' [MIS] su un repertorio o [OSS] su un esecutore.
    """

    strumento: str
    mediana: int
    q1: int
    q3: int
    minimo: int
    massimo: int
    colpi: int
    esecuzioni: int
    batteristi: int


def scala(base: Path | str, *, style: str | None = None,
          beat_type: str | None = 'beat') -> dict[str, Livelli]:
    """La scala di velocity per strumento, su un sottoinsieme del dataset.

    Il default `beat_type='beat'` e' voluto: i `fill` sono un altro animale,
    e mescolarli alle esecuzioni continue alzerebbe le code senza dire niente
    di nessuno dei due. Per i fill si passa `beat_type='fill'`.

    Non riscala le posizioni -- non ne legge nemmeno: guarda solo le
    velocity, che non dipendono dalla risoluzione temporale del file.
    """
    scelte = elenco(base, style=style, beat_type=beat_type)
    raccolta: dict[str, list[int]] = {}
    quali: dict[str, set[str]] = {}
    chi: dict[str, set[str]] = {}
    for e in scelte:
        f = MI.leggi(Path(base) / e.midi_filename)
        for t in f.tracce:
            for n in t.note:
                nome = MI.GM_PERCUSSIONI.get(n.y)
                if nome is None:
                    continue                # percussione fuori dalla mappa GM
                raccolta.setdefault(nome, []).append(n.velocity)
                quali.setdefault(nome, set()).add(e.id)
                chi.setdefault(nome, set()).add(e.drummer)

    fuori = {}
    for nome, vs in raccolta.items():
        vs.sort()
        # sotto i quattro COLPI (non battute: e' len(vs), il conteggio dei
        # colpi raccolti, non una misura di tempo) i quartili interpolati di
        # statistics.quantiles() non direbbero niente di sensato -- e con
        # pochi punti possono anche cadere sotto la mediana, che e' calcolata
        # a parte. Il ripiego deve preservare q1 <= mediana <= q3 SEMPRE:
        # il minimo e il massimo lo fanno per costruzione (mediana e' uno
        # dei vs, quindi vs[0] <= mediana <= vs[-1]), mentre collassare
        # entrambi al minimo no -- vedi il rilievo di revisione sul Task 6.
        q = statistics.quantiles(vs, n=4) if len(vs) >= 4 else [vs[0], 0, vs[-1]]
        fuori[nome] = Livelli(
            strumento=nome, mediana=int(statistics.median(vs)),
            q1=int(q[0]), q3=int(q[2]), minimo=vs[0], massimo=vs[-1],
            colpi=len(vs), esecuzioni=len(quali[nome]),
            batteristi=len(chi[nome]))
    return dict(sorted(fuori.items(), key=lambda kv: -kv[1].colpi))
