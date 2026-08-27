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


def _media_versori(scarti, passo: float) -> float:
    """Il nucleo comune a `origine()` e `_media_circolare()`, in tick.

    Media i VERSORI di una lista di scarti gia' avvolti (dentro
    `(-passo/2, +passo/2]`), perche' la fase GIRA: la media aritmetica di
    1 e 23 tick su un passo di 24 darebbe 12, cioe' il contrario di zero.

    NON FILTRA NIENTE: prende la lista che il chiamante ha gia' deciso di
    includere. `origine()` ci passa solo gli scarti dentro la sua
    `finestra`; `_media_circolare()` ci passa TUTTI gli scarti, senza
    finestra. Questa funzione non sa quale delle due situazioni sta
    vivendo, e non deve saperlo.

    ⚠️ NON aggiungere qui un parametro `finestra` o un filtro. Se lo si
    facesse, basterebbe una riga in `_media_circolare()` per farle
    ereditare la finestra di `origine()` -- esattamente la delegazione che
    il taglio `'voce'` deve evitare (vedi il docstring di
    `_media_circolare()` per il perche').

    Ritorna 0.0 se la lista e' vuota, o se le fasi sono cosi' sparse che
    il versore medio ha modulo trascurabile (nessuna fase comune).
    """
    if not scarti:
        return 0.0
    fasi = [s / passo * 2 * math.pi for s in scarti]
    x = sum(math.cos(a) for a in fasi) / len(fasi)
    y = sum(math.sin(a) for a in fasi) / len(fasi)
    if abs(x) < 1e-12 and abs(y) < 1e-12:
        return 0.0                      # fasi sparse: nessuna fase comune
    return math.atan2(y, x) / (2 * math.pi) * passo


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

    LA SORELLA: `_media_circolare()` usa lo stesso nucleo aritmetico
    (`_media_versori()`, condiviso) ma SENZA la finestra, e serve al
    taglio `'voce'`. Le due non si possono sostituire l'una all'altra:
    QUESTA funzione filtra i colpi lontani dalla griglia e stima lo scarto
    comune del KIT prima che lo swing sia tolto; l'altra non filtra niente
    e stima la fase di UNA VOCE dopo. Condividere l'aritmetica non cambia
    questo: il filtro resta qui, non li'.

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
    return _media_versori(vicini, passo)


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


#: I modi di taglio: come si sceglie il passo su cui un colpo va contato.
#: Il default e' `'voce'` dal 26 agosto 2026 -- la scelta e le ragioni sono
#: nello Step 3 di `.superpowers/sdd/2026-08-26-stimatore-per-passo/
#: task-6-brief.md`: la misura chiude che `'vicino'` non e' uno stimatore
#: (pendenza 0,808 contro 0,998), ma NON chiude fra `'voce'` e `'rado'` --
#: la regola scritta prima selezionava `'rado'`, e la decisione fra i due
#: l'ha presa il proprietario, per iscritto, contro quella regola.
TAGLI = ('vicino', 'voce', 'rado')


def _media_circolare(posizioni, passo: float) -> float:
    """La fase media della voce dentro il passo, in tick, CON SEGNO.

    Stesso nucleo aritmetico di `origine()` -- condividono
    `_media_versori()`, che media i versori perche' la fase GIRA e la
    media aritmetica di 1 e 23 darebbe 12, cioe' il contrario di zero --
    ma SENZA la sua finestra, ed e' una differenza che va capita prima di
    "semplificare" chiamando `origine()`.

    ⚠️ PERCHE' SENZA FINESTRA. `origine()` tiene solo i colpi dentro
    0,25 passo per non far sporcare lo scarto comune del kit dai LEVARE
    SWINGATI, che stanno a 8 tick su 24 dalla griglia dei passi. Qui lo
    swing lo ha gia' tolto `_senza_swing()`, e un levare swingato e' ormai
    SU un passo: la ragione della finestra non si trasporta. Se la si
    tenesse, sul charleston a pedale di `drummer10/session1/1` questa
    funzione vedrebbe 58 colpi su 143 -- scartando proprio gli anticipati,
    che sono il fenomeno -- e darebbe -0,40 tick invece di -8,80 `[OSS]`,
    cioe' non sposterebbe nessun passo.

    ⚠️ Il nucleo condiviso, `_media_versori()`, non prende un parametro
    `finestra` apposta: questa funzione gli passa TUTTI gli scarti, senza
    filtrarli, e il filtro NON va aggiunto qui ne' li'. Farlo basterebbe a
    far ereditare a `'voce'` la finestra di `origine()`, cioe' esattamente
    la delegazione che questa funzione esiste per evitare.

    IL LIMITE, DICHIARATO: la media circolare di una voce sparsa e' un
    numero debole. Sul charleston di quell'esecuzione la concentrazione
    vale R = 0,16. E' il sospetto che la prova di traslazione per voce
    (`tools/misura_groove.py`, `la_prova_di_traslazione()`) deve mettere
    alla prova, e la ragione per cui i candidati sono due.
    """
    scarti = []
    for p in posizioni:
        s = p % passo
        if s > passo / 2:
            s -= passo                  # la fase gira: 23 su 24 e' -1
        scarti.append(s)
    return _media_versori(scarti, passo)


def _vuoto_piu_largo(posizioni, passo: float) -> tuple[float, float, float]:
    """L'arco di fase piu' VUOTO di una voce: (centro, larghezza, buco medio).

    Il centro sta in [0, passo). La larghezza e' il buco piu' grande fra due
    colpi consecutivi, CIRCOLARMENTE. Il buco medio e' `passo / n`, cioe'
    quanto varrebbe ogni buco se i colpi fossero sparsi in modo piatto: non
    serve a decidere niente qui, serve a `misura_groove.py` per dire se quel
    vuoto e' un vuoto VERO o solo il piu' largo di tanti uguali.

    ⚠️ IL CENTRO, NON IL PRIMO PUNTO VUOTO, e la ragione e' misurata il 26
    agosto 2026. Una prima stesura cercava il minimo di densita' dentro una
    finestra e ne prendeva l'argmin. Ma quel minimo e' un ALTOPIANO -- un
    arco intero senza colpi -- e l'argmin ne prendeva il primo punto della
    scansione, che sta sempre a fase 0. Ne usciva un taglio INCOLLATO:
    traslando la voce di -4, -2, 0, +2, +4 tick lo spostamento restava
    -12,00 tutte le volte. Il centro del vuoto invece trasla coi dati, e la
    stessa prova da' una rampa di pendenza 1.

    ⚠️ IL BUCO CHE GIRA VA CONTATO A PARTE. Con tutti i colpi sulla stessa
    fase i buchi fra consecutivi sono zero, e `(fasi[0] - fasi[-1]) % passo`
    darebbe zero anche per quello che avvolge: una voce perfettamente sulla
    griglia uscirebbe con vuoto ZERO invece che con vuoto MASSIMO, cioe' il
    rovescio esatto. Si calcola come `passo - (fasi[-1] - fasi[0])`.
    """
    fasi = sorted(p % passo for p in posizioni)
    if not fasi:
        return 0.0, 0.0, 0.0
    buchi = [fasi[i + 1] - fasi[i] for i in range(len(fasi) - 1)]
    buchi.append(passo - (fasi[-1] - fasi[0]))
    i = max(range(len(fasi)), key=lambda k: buchi[k])
    return (fasi[i] + buchi[i] / 2) % passo, buchi[i], passo / len(fasi)


def spostamento_del_taglio(dritte, passo_tick: float,
                           modo: str = 'vicino') -> float:
    """Di quanto spostare il TAGLIO fra due passi, per questa voce, in tick.

    Il passo si sceglie poi con `round((dritta - spostamento) / passo_tick)`:
    spostare il taglio NON sposta la griglia, sposta solo il confine su cui
    si decide a quale passo un colpo appartiene. Il residuo riportato resta
    misurato dalla griglia vera.

    `'vicino'` e' l'assenza di spostamento, cioe' il `round()` di sempre:
    taglia a meta' fra due passi. E' il termine di paragone.
    """
    if modo not in TAGLI:
        raise ValueError(f'taglio {modo!r} sconosciuto: ci sono {list(TAGLI)}')
    if modo == 'vicino':
        return 0.0
    if modo == 'voce':
        return _media_circolare(dritte, passo_tick)
    if modo == 'rado':
        centro, largo, _ = _vuoto_piu_largo(dritte, passo_tick)
        if largo <= 0:
            return 0.0                  # nessun colpo: niente da spostare
        # il taglio di `round()` cade a meta' fra due passi: portarlo sul
        # centro del vuoto vuol dire spostarlo di (centro - mezzo passo).
        return centro - passo_tick / 2


class Passo(NamedTuple):
    """Cosa fa uno strumento su un passo della battuta, misurato."""

    passo: int          # 0..15
    velocity: int       # la MEDIANA dei colpi su quel passo
    #: tick di residuo rispetto al passo, con segno. POSITIVO = il colpo
    #: cade DOPO la griglia (in ritardo), NEGATIVO = prima (in anticipo).
    #: Lo conferma `musica.applica_groove()`, che fa `pos + scarto`.
    #: ⚠️ Fino al 19 agosto 2026 questa riga diceva '+ spinge, -
    #: trattiene', cioe' il rovescio, ed era copiata in altri tre posti:
    #: ha fatto concludere che il charleston a pedale del jazz stesse
    #: DIETRO agli altri mentre li ANTICIPA. Il segno si legge da qui.
    #: ⚠️ IL LIMITE SI E' ALLARGATO, il 26 agosto 2026. Con `taglio='vicino'`
    #: il passo e' il piu' VICINO, quindi |scarto| <= mezzo passo (12 tick)
    #: per costruzione. Con un taglio spostato non e' piu' vero: uno scarto
    #: puo' arrivare fino a UN PASSO INTERO, ed e' voluto -- e' l'unico modo
    #: di dire "anticipa di mezza semicroma" invece di dire "e' in ritardo
    #: sul passo prima". Ne segue che `applica_groove()` puo' posare una nota
    #: nel territorio del passo accanto.
    scarto: float
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


# taglio='voce' e' il default dal 26 agosto 2026 -- vedi TAGLI, sopra.
def profilo_da_colpi(colpi: dict[str, list[tuple[float, int]]], ppq: float,
                     *, id: str = '', drummer: str = '', style: str = '',
                     bpm: int = 0, taglio: str = 'voce',
                     origine_fissa: float | None = None,
                     levare_fisso: float | None = None) -> Profilo:
    """Il profilo, da colpi gia' letti: strumento -> [(posizione, velocity)].

    LA CATENA, E L'ORDINE E' LA COSA CHE CONTA:

    1. togli l'ORIGINE della griglia -- se no ogni esecuzione dichiara un
       anticipo che e' latenza di cattura, non feel;
    2. misura il BUR e TOGLILO -- se no lo swing viene applicato due volte,
       una dal firmware e una da qui;
    3. quel che resta e' il RESIDUO -- chi arriva prima e chi dopo rispetto
       al resto del kit. E' il solo microtiming che il template porta;
    4. aggrega per strumento e per passo, sedici per battuta.
    """
    if taglio not in TAGLI:
        raise ValueError(f'taglio {taglio!r} sconosciuto: ci sono {list(TAGLI)}')
    passo_tick = ppq / 4                            # un 1/16
    tutte = [p for note in colpi.values() for p, _ in note]

    # ⚠️ ORIGINE E LEVARE SI POSSONO CONGELARE, e serve a una cosa sola:
    # la prova di traslazione per voce. Traslando UNA voce si muove anche
    # l'origine del KIT, di circa delta per la quota di colpi di quella
    # voce, e chi non la congela misura anche quell'artefatto invece dello
    # stimatore. Fuori da quella prova NON si passano: una stima congelata
    # e' una stima che non guarda i dati.
    off = origine(tutte, passo_tick) if origine_fissa is None else origine_fissa

    if levare_fisso is None:
        bur = bur_da_posizioni([p - off for p in tutte], ppq)
        levare = da_bur(bur) if bur is not None else 0.5
    else:
        bur = in_bur(levare_fisso)
        levare = levare_fisso

    # PRIMA PASSATA: la posizione DRITTA di ogni colpo -- origine tolta,
    # swing tolto -- raggruppata per strumento. Il passo NON si sceglie
    # qui: uno spostamento del taglio dipende da TUTTI i colpi di una
    # voce, e finche' non li abbiamo visti tutti non si puo' decidere.
    dritte: dict[str, list[tuple[float, int]]] = {}
    for nome, note in colpi.items():
        for pos, vel in note:
            p = pos - off
            # il movimento in cui la nota CADE, e la sua fase dentro di
            # esso: floor-division, la stessa convenzione di
            # `levare_da_posizioni()`, e per p negativi -144 // 96 fa -2.
            #
            # ⚠️ LA FASE STA IN [0,1) E NON PUO' USCIRNE, perche' e' il
            # dominio su cui `_senza_swing()` e' l'inversa della mappa del
            # firmware. Fino al 24 agosto 2026 qui c'era mezzo passo di
            # grazia -- `math.floor(p / ppq + 0.125)` -- e una nota
            # nell'ultimo ottavo usciva con fase NEGATIVA, su cui
            # `_senza_swing()` applicava il ramo sbagliato. Non era
            # l'inversa di niente.
            movimento, resto = divmod(p, ppq)
            fase = resto / ppq
            dritte.setdefault(nome, []).append(
                ((movimento + _senza_swing(fase, levare)) * ppq, vel))

    # SECONDA PASSATA: una voce alla volta, col suo spostamento del taglio.
    per_passo: dict[str, dict[int, list[tuple[int, float]]]] = {}
    ultimo = 0
    for nome, note in dritte.items():
        sp = spostamento_del_taglio([d for d, _ in note], passo_tick, taglio)
        for dritta, vel in note:
            # ⚠️ il passo si decide DOPO aver tolto lo swing: un levare
            # swingato sta a 2,67 passi e si arrotonderebbe al 3.
            passo = round((dritta - sp) / passo_tick)
            ultimo = max(ultimo, passo)
            # ⚠️ il residuo si misura dalla GRIGLIA, non dal taglio
            # spostato: e' la posizione vera del colpo rispetto al passo su
            # cui lo scriviamo. Sottrarre anche `sp` toglierebbe il feel
            # invece di collocarlo.
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


# taglio='voce' e' il default dal 26 agosto 2026 -- vedi TAGLI, sopra.
def profilo(base: Path | str, id: str, *, taglio: str = 'voce') -> Profilo:
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
                            bpm=e.bpm, taglio=taglio)


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
