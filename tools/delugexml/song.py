"""API di alto livello sopra il documento: tempo, clip, note.

Tutto qui sopra e' costruito su cio' che e' stato osservato nei file reali.
Dove una relazione e' derivata e non ancora confermata sul dispositivo
(il tempo) e' segnalato esplicitamente nel docstring e in docs/FINDINGS.md.
"""
from __future__ import annotations

from . import notes as notes_mod
from .parser import Document, Node   # noqa: F401  (Node usato nelle firme)

SAMPLE_RATE = 44100
# 110250 = 44100 * 60 / 24. Il fattore 24 e' la risoluzione di riferimento del
# clock interno; la scala effettiva per movimento e' 24 * 2^inputTickMagnitude,
# cioe' 48 tick/movimento al valore piu' comune (magnitude = 1).
TEMPO_NUMERATOR = SAMPLE_RATE * 60 / 24
TWO32 = 1 << 32


def _u32(v: str) -> int:
    i = int(v)
    return i + TWO32 if i < 0 else i


def _s32(i: int) -> int:
    return i - TWO32 if i >= (1 << 31) else i


# ------------------------------------------------------------------ griglia

def ticks_per_beat(song: Node) -> int:
    """Tick interni per movimento: 24 * 2^inputTickMagnitude.

    CONFERMATA in due modi indipendenti. Dal dispositivo: in una song con
    magnitude 2, una nota a posizione 144 cade sul quarto ottavo della prima
    battuta, quindi 48 tick = un ottavo e 96 = un movimento. Dal corpus: il MCD
    delle posizioni delle note raddoppia esattamente (x2.00) passando dalle
    song con magnitude 1 a quelle con magnitude 2.

    E' la stessa costante che compare in get_bpm(): tempo e griglia misurano
    la stessa cosa.
    """
    return 24 * 2 ** int(song.get('inputTickMagnitude', '0'))


def ticks_per_bar(song: Node, beats_per_bar: int = 4) -> int:
    """Assume 4/4. Il Deluge non salva un'indicazione di tempo esplicita."""
    return ticks_per_beat(song) * beats_per_bar


def beats_to_ticks(song: Node, beats: float) -> int:
    return round(beats * ticks_per_beat(song))


# ------------------------------------------------------------------- tempo

def samples_per_tick(song: Node) -> float:
    return int(song.get('timePerTimerTick')) + \
        _u32(song.get('timerTickFraction', '0')) / TWO32


def get_bpm(song: Node) -> float:
    """BPM = 110250 / (campioni_per_tick * 2^inputTickMagnitude).

    Derivata dal corpus (valori interi su 26 song su 27) e CONFERMATA sul
    dispositivo il 10 agosto 2026: Mark.XML mostra 88 BPM sul Deluge, che e'
    esattamente il valore previsto.

    Il sorgente del firmware conferma anche la struttura degli attributi:
    timePerTimerTick e timerTickFraction sono le due meta' di un unico uint64
    in virgola fissa 32.32 (song.cpp scrive `timePerTimerTickBig >> 32` e
    `(uint32_t)timePerTimerTickBig`), che e' il motivo per cui la frazione
    appare negativa in 11 song su 27.
    """
    mag = int(song.get('inputTickMagnitude', '0'))
    return TEMPO_NUMERATOR / (samples_per_tick(song) * 2 ** mag)


def set_bpm(song: Node, bpm: float) -> float:
    """Imposta il tempo mantenendo inputTickMagnitude. Restituisce i BPM reali.

    L'arrotondamento e' inevitabile: il tempo e' un punto fisso 32.32, quindi
    il valore riletto puo' differire nell'ultima cifra decimale.
    """
    if bpm <= 0:
        raise ValueError('bpm deve essere positivo')
    mag = int(song.get('inputTickMagnitude', '0'))
    spt = TEMPO_NUMERATOR / (bpm * 2 ** mag)
    whole = int(spt)
    frac = int(round((spt - whole) * TWO32))
    if frac >= TWO32:                     # riporto
        whole += 1
        frac = 0
    song.set('timePerTimerTick', str(whole))
    song.set('timerTickFraction', str(_s32(frac)))
    return get_bpm(song)


# -------------------------------------------------------------------- clip

def clips(doc: Document) -> list[tuple[str, Node]]:
    """(contenitore, nodo) per ogni clip: sessionClips o arrangementOnlyTracks."""
    out = []
    for container in ('sessionClips', 'arrangementOnlyTracks', 'arrangementClips'):
        c = doc.root.find(container)
        if c is None:
            continue
        for clip in c.children:
            out.append((container, clip))
    return out


def clip_label(clip: Node) -> str:
    for a in ('clipName', 'instrumentPresetName', 'trackName', 'name'):
        v = clip.get(a)
        if v:
            return v
    return f'({clip.tag})'


def note_rows(clip: Node) -> list[Node]:
    nr = clip.find('noteRows')
    return nr.children if nr else []


def read_notes(row: Node) -> list[notes_mod.Note]:
    r = notes_mod.read_row(row)
    return r[2] if r else []


def write_notes(row: Node, ns, create: bool = False) -> None:
    notes_mod.write_row(row, ns, create=create)


# -------------------------------------------------------- scala e tonalita

def scale_pitch_classes(song: Node) -> set[int]:
    """Le 12 classi di altezza ammesse dalla scala della song.

    La scala e' una proprieta' della SONG, non della clip: il manuale dice che
    tutte le clip in modalita' scala di una song condividono la stessa scala.
    `rootNote` e' la tonica in semitoni da C, `modeNotes` sono gli intervalli.
    """
    root = int(song.get('rootNote', '0'))
    mn = song.find('modeNotes')
    if mn is None:
        return set(range(12))
    modes = [int(c.text) for c in mn.children if c.text]
    return {(root + m) % 12 for m in modes} if modes else set(range(12))


def in_scale(song: Node, y: int) -> bool:
    return y % 12 in scale_pitch_classes(song)


def snap_to_scale(song: Node, y: int) -> int:
    """L'altezza della scala piu' vicina a `y`, a parita' preferendo il grave."""
    allowed = scale_pitch_classes(song)
    if y % 12 in allowed:
        return y
    for d in range(1, 12):
        for cand in (y - d, y + d):
            if cand % 12 in allowed:
                return cand
    return y


# --------------------------------------------------------- synth contro kit

# ------------------------------------------------------- livello song: scala

#: Modi come intervalli in semitoni dalla tonica, nella forma in cui il
#: firmware li scrive dentro <modeNotes>. Il maggiore (0,2,4,5,7,9,11) e'
#: quello osservato nelle song del corpus.
MODI = {
    'maggiore':      (0, 2, 4, 5, 7, 9, 11),
    'minore':        (0, 2, 3, 5, 7, 8, 10),
    'dorico':        (0, 2, 3, 5, 7, 9, 10),
    'frigio':        (0, 1, 3, 5, 7, 8, 10),
    'lidio':         (0, 2, 4, 6, 7, 9, 11),
    'misolidio':     (0, 2, 4, 5, 7, 9, 10),
    'locrio':        (0, 1, 3, 5, 6, 8, 10),
    'minore armonica': (0, 2, 3, 5, 7, 8, 11),
    'minore melodica': (0, 2, 3, 5, 7, 9, 11),
}

NOTE_NOMI = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')


def get_scale(doc: Document) -> tuple[int, tuple[int, ...]]:
    """(rootNote, intervalli) della song.

    Gli intervalli stanno in <modeNotes> come figli <modeNote> con il valore
    nel testo, in semitoni dalla tonica — non come altezze assolute.
    """
    root = int(doc.root.get('rootNote', '0') or 0)
    nodo = doc.root.find('modeNotes')
    if nodo is None:
        return root, ()
    return root, tuple(int(c.text) for c in nodo.children if c.text)


def scale_name(doc: Document) -> str:
    """Il nome leggibile della scala, o una descrizione se non e' fra i modi noti."""
    root, intervalli = get_scale(doc)
    nome = next((k for k, v in MODI.items() if v == intervalli), None)
    tonica = NOTE_NOMI[root % 12]
    return f'{tonica} {nome}' if nome else f'{tonica} {list(intervalli)}'


def set_scale(doc: Document, root: int | str, mode: str | tuple[int, ...]) -> None:
    """Imposta tonica e modo della song.

    `root` puo' essere un numero 0-11 o un nome di nota -- qualunque cosa
    accetti `musica.altezza()`: italiano o inglese, diesis o bemolle ('re',
    'D', 'fa#', 'Bb', 'Ab', ...). Non duplica quel parser: chiede ad
    `altezza()` la nota su un'ottava arbitraria e ne tiene solo la classe,
    modulo 12.

    [BUG CORRETTO] La versione precedente faceva `root.upper().replace('B',
    '#')` sul nome: un bemolle come 'Ab' diventava 'A#' invece di 'G#' --
    UN SEMITONO SBAGLIATO, IN SILENZIO, perche' 'A#' resta comunque un nome
    valido nella tabella e nessun errore lo segnalava. Misurato: 'Ab' dava
    rootNote 10 (A#) invece di 8 (G#); stesso per 'Db' (3, D#, invece di 1,
    C#) e 'Gb' (8, G#, invece di 6, F#). E i nomi italiani ('re') e i
    bemolle inglesi a due 'B' come 'Eb'/'Bb' (che diventavano 'E#'/'##',
    entrambi assenti dalla tabella) venivano rifiutati anche se legittimi.

    `mode` un nome fra MODI o direttamente gli intervalli.

    Non tocca le note gia' scritte: cambiare scala sul Deluge cambia come la
    griglia viene disegnata, non le altezze registrate.
    """
    if isinstance(root, str):
        from . import musica as MU                          # import locale: ciclo
        grezzo = root.strip()
        try:
            root = MU.altezza(f'{grezzo}4') % 12
        except ValueError:
            raise ValueError(
                f'nota "{root}" sconosciuta. Usa un nome come lo accetta '
                f'musica.altezza() (es. re, D, fa#, Bb, Ab) o un intero '
                f'0-11') from None
    root = int(root)
    if not 0 <= root <= 11:
        raise ValueError(f'rootNote {root} fuori da 0-11')

    if isinstance(mode, str):
        if mode not in MODI:
            raise ValueError(f'modo "{mode}" sconosciuto. '
                             f'Noti: {", ".join(sorted(MODI))}')
        intervalli = MODI[mode]
    else:
        intervalli = tuple(int(x) for x in mode)
    if any(not 0 <= i <= 11 for i in intervalli):
        raise ValueError(f'intervalli fuori da 0-11: {intervalli}')

    doc.root.set('rootNote', str(root))
    nodo = doc.root.find('modeNotes')
    if nodo is None:
        nodo = doc.root.insert(0, Node(tag='modeNotes'))
    nodo.children = [Node(tag='modeNote', text=str(i)) for i in intervalli]
    nodo.touch()


#: Il display mostra lo swing come 0-100 con 50 al centro; nel file e' un
#: valore CON SEGNO centrato sullo zero. Misurato sul dispositivo: scritto 25,
#: il display mostra 75. Confermato dal corpus, dove swingAmount va da -10 a
#: +20, il valore piu' frequente e' 0 (41 volte, cioe' "dritto") e 26 valori
#: sono negativi. L'ipotesi alternativa display = 100 - valore e' esclusa:
#: farebbe di 0, il valore piu' comune, lo swing massimo.
SWING_CENTRO = 50


#: `swingInterval` -> la figura che viene SWINGATA, cioe' esattamente
#: l'etichetta che il Deluge mostra a schermo.
#:
#: **Misurato sul dispositivo il 17 agosto 2026**, cinque salvataggi (uno per
#: posizione del menu) piu' l'ascolto. Le note si muovono a COPPIE della
#: figura nominata: con "8th" la prima croma resta ferma e la seconda si
#: sposta; con "4th" e' il secondo quarto a spostarsi. Sotto 50 il secondo
#: arriva in anticipo invece che in ritardo.
SWING_FIGURA_PER_INTERVALLO = {4: '1/2', 5: '1/4', 6: '1/8', 7: '1/16',
                               8: '1/32'}
SWING_INTERVALLO_PER_FIGURA = {v: k for k, v in
                               SWING_FIGURA_PER_INTERVALLO.items()}

#: Il default del firmware e' **7**, cioe' le semicrome, ed e' il valore di
#: tutte e 146 le song del corpus. Per swingare le CROME -- il jazz, e
#: qualunque groove di crome -- serve **6**.
SWING_INTERVALLO_DEFAULT = 7

#: ⚠️ **Il sorgente NON torna con la misura, e la misura vince.**
#: `playback_handler.cpp` calcola `3 << (10 - swingInterval)` e lo chiama
#: `doubleSwingInterval`: per l'intervallo 6 fa 48 tick, cioe' una croma. Ma
#: l'orecchio dice che con l'intervallo 6 la coppia swingata e' croma+croma,
#: quindi il blocco vale una semiminima, 96 tick -- il doppio.
#:
#: Lo scarto e' esattamente un fattore 2, quindi i "swung tick" di quel codice
#: non sono i tick delle posizioni di nota. Cosa siano di preciso resta
#: **ignoto**: non si e' trovato il punto in cui i due si convertono.
#:
#: E' scritto qui perche' una derivazione che non torna va dichiarata, non
#: nascosta: questa e' gia' costata una tabella sbagliata, corretta solo
#: perche' l'utente ha detto che non tornava.
SWING_SCARTO_SORGENTE = 2


def swing_intervallo_per(figura: str) -> int:
    """L'intervallo che swinga la figura richiesta: `'1/8'` -> 6.

    La figura e' quella che si vuole SWINGARE, ed e' anche l'etichetta che
    compare sul Deluge: non c'e' traduzione da fare. Passare da qui evita
    comunque di scrivere il numero nudo, che non dice niente a chi legge.
    """
    if figura not in SWING_INTERVALLO_PER_FIGURA:
        raise ValueError(
            f'figura {figura!r} sconosciuta, usare '
            f'{sorted(SWING_INTERVALLO_PER_FIGURA)}: sono le stesse che il '
            f'menu del Deluge mostra')
    return SWING_INTERVALLO_PER_FIGURA[figura]


def get_swing(doc: Document) -> tuple[int, int]:
    """(swing come lo mostra il display 0-100, intervallo)."""
    grezzo = int(doc.root.get('swingAmount', '0') or 0)
    return grezzo + SWING_CENTRO, int(doc.root.get('swingInterval', '0') or 0)


def set_swing(doc: Document, display: int, interval: int | None = None, *,
              figura: str | None = None) -> int:
    """Swing nelle unita' del display: 0-100, con **50 = dritto**.

    Il display **e' la posizione percentuale del levare dentro il blocco** --
    derivato dal sorgente del firmware, non supposto: la prima meta' del
    blocco viene dilatata di `(50 + swingAmount)/50` e la seconda compressa di
    `(50 - swingAmount)/50`, quindi il punto di mezzo cade a
    `(50 + swingAmount)/100`. Percio' 50 e' dritto, **66-67 e' la terzina**, e
    il rapporto fra le due meta' vale `display / (100 - display)`.

    `figura` dice quale figura si vuole swingare (`'1/8'` per le crome) e
    sceglie l'intervallo da se'. Usare quella invece di `interval`: il menu
    del Deluge nomina il BLOCCO, che e' il doppio della figura spostata, e
    scrivere `interval=5` per swingare le crome non lo dice a nessuno.

    Ritorna il valore grezzo scritto nel file. Chi volesse scrivere il grezzo
    direttamente puo' usare `doc.root.set('swingAmount', ...)`, ma passare per
    qui evita l'errore di scambiare le due scale — che e' gia' costato una
    prova sul dispositivo.
    """
    if figura is not None:
        if interval is not None:
            raise ValueError('serve figura= OPPURE interval=, non entrambi')
        interval = swing_intervallo_per(figura)
    display = int(display)
    if not 0 <= display <= 100:
        raise ValueError(f'swing {display} fuori da 0-100 (50 = dritto)')
    grezzo = display - SWING_CENTRO
    doc.root.set('swingAmount', str(grezzo))
    if interval is not None:
        doc.root.set('swingInterval', str(int(interval)))
    return grezzo


# ------------------------------------------------------ livello song: sezioni

#: Il firmware scrive SEMPRE 24 <section>, in 34 song su 34 del corpus, anche
#: se il manuale ne descrive 12. E' una costante, non una variabile.
#: Quante `<section>` dichiara una song. Nel corpus vale 12 (103 song) oppure
#: 24 (36 song) secondo la versione: non darlo per scontato, si conta.
N_SEZIONI = 24


def sections(doc: Document) -> list[Node]:
    """Le sezioni della song. Una sezione e' una SCENA.

    Ogni `<section>` porta due soli attributi, `id` e `numRepeats`, e il
    contenuto vero sta altrove: e' l'attributo `section` sulle clip a dire
    quali clip appartengono a quale scena. Le clip con lo stesso `section`
    partono insieme.

    Nel corpus la forma tipica e' la sezione 0 con una clip per strumento —
    il brano "pieno" — e le altre con poche clip, cioe' le varianti. Il caso
    puro e' `Electronic.XML`, dove le sezioni 0-3 contengono tutte lo stesso
    strumento `000 TR-808` con quattro clip diverse: sono quattro variazioni
    dello stesso strumento.

    Dalla documentazione community, in grid view questo e' letterale: le righe
    sono le clip uniche e **le colonne sono le sezioni**, cioe' le variazioni.
    Con un limite pratico: se due clip dello stesso strumento cadono nella
    stessa sezione, in grid se ne vede una sola. Succede in 91 sezioni del
    corpus, quindi e' legale ma e' uno stato degradato — vedi
    `same_section_conflicts()`.

    `numRepeats` vale 0 in tutte e 2100 le sezioni del corpus: nessuno lo usa.

    Una clip **senza** `section` e' un caso a parte e non sta qui: e' la clip
    "bianca" dell'arranger, vedi `arranger.place_unique()`.
    """
    nodo = doc.root.find('sections')
    return nodo.children if nodo else []


def clips_in_section(doc: Document, section_id: int | str) -> list[Node]:
    """Le clip di sessione che appartengono a una scena."""
    sid = str(section_id)
    from . import arranger as A                           # import locale: ciclo
    return [c for c in A.clip_list(doc, False) if c.get('section') == sid]


def no_playing_clip(doc: Document) -> list[str]:
    """Nessuna clip di sessione ha `isPlaying='1'`: premendo play non parte nulla.

    Trovato sul dispositivo il 17 agosto 2026, e costato quattro prove e un
    blocco del Deluge. Una song generata con `create.add_track()` senza
    `playing=True` -- che e' il DEFAULT -- esce con la clip a `isPlaying='0'`.
    Se e' l'unica clip della song, il file si carica, passa `verifica()`,
    `check_clip_types()` e ogni altro controllo, e poi non suona.

    E' la famiglia di `yScrollSongView`: contenuto presente e inerte. Con una
    variante nuova pero' -- li' era uno stato di VISTA, qui e' uno stato di
    LANCIO.

    ⚠️ **Informa, non blocca**, e la soglia e' misurata: nel corpus **10 song
    su 146** (il 6,8%) sono in questo stato, e sono song vere scritte dal
    dispositivo -- salvate da ferme, con le clip da lanciare a mano. Un
    controllo bloccante accuserebbe dieci file sani, che e' la trappola dei
    falsi positivi gia' pagata due volte in questo progetto.

    Non si accusa una song **senza** clip di sessione: li' non c'e' niente da
    lanciare e non e' un difetto, e' una song vuota.
    """
    nodo = doc.root.find('sessionClips')
    if nodo is None or not nodo.children:
        return []
    if any(c.get('isPlaying') == '1' for c in nodo.children):
        return []
    quante = len(nodo.children)
    return [f'nessuna delle {quante} clip di sessione ha isPlaying=1: '
            f'premendo play non partira niente, le clip vanno lanciate a mano '
            f'(create.add_track(..., playing=True) le fa partire)']


def same_section_conflicts(doc: Document) -> list[str]:
    """Due clip dello stesso strumento nella stessa sezione.

    In grid view se ne vede una sola: la seconda c'e', si carica e suona, ma
    non ha una colonna dove mostrarsi. E' la stessa famiglia di
    `yScrollSongView` — contenuto presente e invisibile — ma qui il rimedio
    non e' uno scroll, e' spostare la clip in un'altra sezione.
    """
    from . import arranger as A                           # import locale: ciclo

    visti: dict[tuple[str, str], Node] = {}
    fuori = []
    for c in A.clip_list(doc, False):
        sid = c.get('section')
        if sid is None:
            continue
        inst = instrument_of(doc, c)
        if inst is None:
            continue
        k = (sid, id(inst).__str__())
        if k in visti:
            fuori.append(f'sezione {sid}: {clip_label(c)!r} e '
                         f'{clip_label(visti[k])!r} sono dello stesso '
                         f'strumento')
        else:
            visti[k] = c
    return fuori


def notes_beyond_clip_end(doc: Document) -> list[str]:
    """Note che cadono oltre la fine EFFETTIVA della propria clip.

    [LACUNA capitolato] il dispositivo carica un file cosi' senza protestare
    -- non e' un motivo di rifiuto, quindi questo controllo sta in
    `musica.avvertenze()`, non in `musica.verifica()` -- ma non le suona:
    stessa condizione gia' usata in `set_clip_length()` per le note che
    restano indietro quando si accorcia una clip, qui applicata al
    documento cosi' com'e', non solo a un cambio di lunghezza esplicito.

    "Fine effettiva" NON e' sempre `clip.get('length')`: una `<noteRow>`
    puo' portare un `length` proprio, piu' lungo di quello della clip (vedi
    HANDOFF.md sezione 7, il poliritmo) -- una nota entro quella lunghezza propria
    NON e' oltre la fine, anche se supera quella della clip. Ignorare
    questo e' esattamente la trappola gia' costata cara due volte in questo
    progetto ("same_section_conflicts" e "check_notes_playable"): un
    controllo nuovo che accusa file sani. Misurato sui 139 file scritti dal
    dispositivo (refs/songs + corpus_versions): un controllo che guarda
    solo `clip.length` trova 254 note "fuori" in 22 file, TUTTE dentro una
    noteRow con un length proprio piu' lungo -- zero, considerando la fine
    effettiva.
    """
    fuori = []
    for _, clip in clips(doc):
        if clip.tag == 'audioClip':
            continue
        lunghezza_clip = int(clip.get('length') or 0)
        attr = row_index_attr(clip)
        for r in note_rows(clip):
            lunghezza_riga = r.get('length')
            effettiva = max(lunghezza_clip, int(lunghezza_riga)) \
                if lunghezza_riga else lunghezza_clip
            ns = [n for n in read_notes(r) if n.pos >= effettiva]
            if ns:
                fuori.append(
                    f'clip {clip_label(clip)!r}: {attr}={r.get(attr)}: '
                    f'{len(ns)} note oltre la fine ({effettiva} tick), '
                    f'non suonano')
    return fuori


def set_section_repeats(doc: Document, section_id: int | str, repeats: int) -> Node:
    """Quante volte una sezione si ripete prima di passare oltre. 0 = infinito."""
    sid = str(section_id)
    for s in sections(doc):
        if s.get('id') == sid:
            s.set('numRepeats', str(int(repeats)))
            return s
    raise ValueError(f'sezione {sid} inesistente (ce ne sono {len(sections(doc))})')


def set_clip_length(clip: Node, ticks: int) -> list[str]:
    """Cambia la lunghezza di una clip.

    Ritorna gli avvisi: le note oltre la nuova lunghezza NON vengono tolte —
    il dispositivo le conserva e semplicemente non le suona — ma e' bene
    saperlo invece di scoprirlo dopo.
    """
    if ticks <= 0:
        raise ValueError(f'lunghezza {ticks} non valida')
    avvisi = []
    attr = row_index_attr(clip)
    for r in note_rows(clip):
        fuori = [n for n in read_notes(r) if n.pos >= ticks]
        if fuori:
            avvisi.append(f'{attr}={r.get(attr)}: {len(fuori)} note oltre '
                          f'{ticks} tick (restano nel file, non suonano)')
    clip.set('length', str(int(ticks)))
    return avvisi


#: Righe di clip view. Come in song view, la griglia ne mostra 8.
CLIP_VIEW_ROWS = 8


def set_key_mode(clip: Node, in_key: bool) -> None:
    """`inKeyMode`: la griglia mostra i gradi della scala, o i semitoni.

    In key mode le righe SONO i gradi della scala. Una nota fuori scala non ha
    una riga dove stare: non si vede e **non si suona**, per quanto si scrolli.
    In modalita' cromatica ogni semitono ha la sua riga e qualunque altezza e'
    rappresentabile.
    """
    clip.set('inKeyMode', '1' if in_key else '0')


def notes_out_of_scale(doc: Document, clip: Node) -> list[tuple[int, int, int]]:
    """(altezza, quante note, altezza in scala piu' vicina) per le note fuori
    dalla scala dichiarata dalla song.

    ⚠ NON E' UN ERRORE. Le song scritte dal dispositivo ne sono piene:
    su 70 song del corpus con note melodiche, 7 hanno note fuori scala, e
    `Progsong.XML` ne ha **315**. In scale mode il Deluge non le scarta —
    adatta la scala per includerle. Il nodo `<scales>` porta un `userScale`
    che e' una maschera a 12 bit (4095 = tutti i semitoni).

    Questa funzione serve solo a *sapere* cosa si sta scrivendo, per esempio
    per decidere se applicare `snap_to_scale()`. Non e' una diagnosi di
    malfunzionamento: una precedente versione la presentava come tale, ed era
    sbagliata.
    """
    fuori = []
    if is_kit_clip(clip):
        return fuori
    for r in note_rows(clip):
        if not r.has('y'):
            continue
        ns = read_notes(r)
        if not ns:
            continue
        y = int(r.get('y'))
        if not in_scale(doc.root, y):
            fuori.append((y, len(ns), snap_to_scale(doc.root, y)))
    return fuori


def check_notes_playable(doc: Document, clip: Node) -> list[str]:
    """DEPRECATA: la diagnosi che dava era sbagliata.

    Diceva che le note fuori scala non hanno una riga e non suonano. Falso:
    il dispositivo adatta la scala, e song reali ne contengono a centinaia.
    Usa `notes_out_of_scale()` per sapere cosa c'e', e
    `fit_clip_scroll_to_notes()` per il problema vero, che era lo scroll
    ereditato da un'altra clip.
    """
    import warnings
    warnings.warn('check_notes_playable dava una diagnosi sbagliata: usa '
                  'notes_out_of_scale() e fit_clip_scroll_to_notes()',
                  DeprecationWarning, stacklevel=2)
    return []
    avvisi: list[str] = []
    if is_kit_clip(clip):
        return avvisi
    if clip.get('inKeyMode') != '1':
        return avvisi

    fuori = []
    for r in note_rows(clip):
        if not r.has('y') or not read_notes(r):
            continue
        y = int(r.get('y'))
        if not in_scale(doc.root, y):
            fuori.append((y, len(read_notes(r)), snap_to_scale(doc.root, y)))
    if fuori:
        elenco = ', '.join(f'y={y} ({n} note, in scala sarebbe {s})'
                           for y, n, s in fuori)
        avvisi.append(
            f'clip in key mode su scala {scale_name(doc)}: {elenco}. '
            'Queste note non hanno una riga e non suoneranno. '
            'Usa set_key_mode(clip, False) per la griglia cromatica, '
            'oppure snap_to_scale() sulle altezze.')
    return avvisi


def drum_rows_sounding(clip: Node) -> list[int]:
    """Le POSIZIONI delle righe che suonano, in una clip di kit.

    Posizione fra i nodi `<noteRow>`, non `drumIndex`: sul dispositivo
    l'ordine delle righe di un kit lo decide l'utente, e riordinarle cambia
    l'ordine dei nodi mentre i `drumIndex` restano quelli che sono. Nel corpus
    ne esiste un esemplare, `Xmasjam1.XML`, con le righe in ordine
    [4, 6, 8, 10, 12, 14, 0, 1, 2, 3, 5, 7, 9, 11].

    Nei file normali le due cose coincidono -- 355 clip di kit su 356 hanno i
    nodi in ordine di `drumIndex` -- e proprio per questo la differenza e'
    facile da non vedere finche' non morde. E' la stessa forma dell'errore che
    questo progetto ha gia' pagato con `clipCode`: un indice e' una posizione,
    non un identificatore.
    """
    return [k for k, r in enumerate(note_rows(clip)) if read_notes(r)]


def clip_rows_with_notes(doc: Document, clip: Node) -> list[int]:
    """Le righe di schermo occupate da note, nell'unita' della clip.

    La geometria e' UNA SOLA in tutto il dispositivo -- `riga = valore -
    yScroll`, otto righe a schermo -- ma l'unita' cambia col tipo di clip, e
    ciascuna e' stata misurata con una coppia controllata:

        synth cromatico   il semitono          (0 falsi positivi su 44 clip)
        synth in scala    il GRADO             SCALA0/1, SCALB0/1
        kit               la POSIZIONE riga    KITSCR0/1

    Le tre coppie stanno in `refs/songs/`.
    """
    if is_kit_clip(clip):
        return drum_rows_sounding(clip)
    return sorted({clip_row_of(doc, clip, int(r.get('y')))
                   for r in note_rows(clip) if r.has('y') and read_notes(r)})


def scale_degree(doc: Document, y: int) -> int:
    """Quanti gradi della scala stanno in [0, y]. E' l'unita' di riga in scala.

    Verificato sul dispositivo con la coppia controllata SCALB0/SCALB1
    (`refs/songs/`): la stessa nota D3 (y=62) portata a mano dalla riga piu'
    bassa dello schermo alla piu' alta, in re maggiore, ha dato
    `yScroll` 37 e 30. Sette righe, sette unita' -- e 37 e' esattamente
    questo conteggio per D3.
    """
    classi = sorted(scale_pitch_classes(doc.root))
    if not classi:
        return y
    ottave, resto = divmod(y, 12)
    return ottave * len(classi) + sum(1 for c in classi if c <= resto)


def clip_row_of(doc: Document, clip: Node, y: int) -> int:
    """La riga di clip view su cui cade l'altezza `y`, nella modalita' giusta.

    In cromatico una riga e' un semitono e la riga E' l'altezza. In modalita'
    a scala una riga e' un GRADO, e le due cose non si somigliano affatto:
    per un basso a y=38 la differenza fra i due conti e' di quindici righe.

    Governa `yScroll` in ENTRAMBE le modalita'. `inKeyScrollOffset` no: nella
    coppia SCALA0/SCALA1 uno scroll di una riga in modalita' a scala muove
    `yScroll` e lascia `inKeyScrollOffset` fermo.
    """
    return scale_degree(doc, y) if clip.get('inKeyMode') == '1' else y


def fit_clip_scroll_to_notes(doc: Document, clip: Node) -> dict[str, str]:
    """Porta la finestra verticale della clip dove stanno davvero le note.

    IL PROBLEMA CHE RISOLVE, ed e' reale: una clip creata istanziando un
    modello eredita `yScroll` e `inKeyScrollOffset` dal modello, cioe' da una
    clip con un altro preset e altre altezze. Sono posizioni di scroll che non
    hanno nulla a che vedere con le note che ci scriviamo — un difetto a
    prescindere da come il dispositivo le interpreti.

    `yScroll` governa la finestra di OGNI tipo di clip -- synth cromatico, in
    scala, e kit -- ciascuno nella propria unita': vedi `clip_rows_with_notes()`.

    ⚠ [CORREZIONE, 16 agosto 2026] Questa funzione scriveva l'altezza in
    `yScroll` sempre, calcolava un `inKeyScrollOffset` con una formula mai
    verificata, e le clip di kit le saltava del tutto. Sbagliate tutte e tre,
    ed era un difetto VIVO: ogni clip generata da Deluge Pal nasce con
    `inKeyMode=1` e `yScroll=37` (CLIP_BASE viene da TEMPL0), quindi le song
    caricate sul dispositivo si aprivano con lo schermo VUOTO -- note corrette
    e invisibili finche' non si scrollava. Guardato su `TRASF201`, e sui kit
    una seconda volta su `TRASF203`.

    `inKeyScrollOffset` e `drumsScrollOffset` non vengono toccati: le coppie
    SCALA0/1 e KITSCR0/1 mostrano che non si muovono scrollando la clip view,
    quindi governano altro. Cosa, resta ignoto -- e scrivere valori in
    attributi che non si sono capiti e' esattamente come nascevano questi
    difetti.

    Ritorna gli attributi cambiati, per poterlo dire a chi genera.
    """
    righe = clip_rows_with_notes(doc, clip)
    if not righe:
        return {}

    # Si ANCORA la riga piu' bassa in fondo allo schermo, sempre. La tentazione
    # e' di non muovere una vista che gia' mostra qualcosa -- e' la regola
    # giusta per gli scroll di song view, dove si conserva dove l'utente ha
    # lasciato la vista -- ma qui e' sbagliata: questa funzione si chiama
    # "porta la finestra dove sono le note", e una finestra che ne mostra una
    # su quattro il suo mestiere non l'ha fatto.
    #
    # Il caso che l'ha dimostrato, visto sul dispositivo: scritte le note, fit
    # porta yScroll a 23; poi una trasposizione di un grado alza le righe a
    # 24-31; con "almeno una visibile" yScroll resta 23, la prima riga resta
    # sprecata e la nota piu' alta esce dallo schermo. Ancorando entrano tutte.
    corrente = clip.get('yScroll')
    nuovo = min(righe)
    if is_kit_clip(clip):
        # non oltre l'ultima schermata: sotto le righe del kit non c'e' nulla
        nuovo = min(nuovo, max(0, len(note_rows(clip)) - CLIP_VIEW_ROWS))
    if corrente == str(nuovo):
        return {}
    clip.set('yScroll', str(nuovo))
    return {'yScroll': str(nuovo)}


def notes_hidden_by_scroll(doc: Document) -> list[str]:
    """Note che esistono ma restano fuori dalla finestra di scroll della clip.

    Il gemello, a livello di CLIP, del famigerato yScrollSongView (HANDOFF.md
    3.1): contenuto presente, invisibile finche' non si scrolla.
    `fit_clip_scroll_to_notes()` CORREGGE il problema; questa funzione lo
    SEGNALA per chi si dimentica di chiamarla -- va in `musica.avvertenze()`,
    non in `musica.verifica()`, per lo stesso motivo di
    `notes_beyond_clip_end()`: il file carica, il contenuto c'e', solo non si
    vede finche' non si scrolla.

    Il caso concreto e' reale: `create.add_track()` da' a OGNI clip nuova
    `yScroll='37'` (da CLIP_BASE, preso pari pari da TEMPL0), indipendente
    da quali note ci si scrivono sopra. Un basso profondo scritto li' dentro
    puo' restare interamente sotto la finestra da 8 righe. Misurato su
    TEMPL0.XML: yScroll=37 e note a y=24/31/36 (tutte sotto la finestra
    [37, 44]) -- ne' `verifica()` ne' `avvertenze()` (prima di questa
    funzione) dicevano nulla.

    ENTRAMBE LE MODALITA', da quando la coppia controllata SCALB0/SCALB1 ha
    chiuso la formula in scala (vedi `scale_degree()`). Prima questa funzione
    saltava le clip in modalita' a scala, perche' la conversione allora in uso
    -- via `inKeyScrollOffset` -- accusava 109 clip su 131 del corpus fidato,
    una percentuale implausibile per un difetto reale.

    Non era prudenza: era la funzione cieca proprio dove stava il difetto. Le
    clip generate da Deluge Pal sono TUTTE in modalita' a scala, e cinque song
    sono finite sul dispositivo con lo schermo vuoto senza che questa
    avvertenza dicesse niente.

    In cromatico il conto da' ZERO falsi positivi su 44 clip del corpus
    fidato. In scala il corpus resta in parte inspiegato, e il motivo va detto:
    **un file scritto dal dispositivo non deve per forza mostrare le proprie
    note.** Se si scrolla altrove e si salva, il Deluge salva li', e la clip e'
    davvero "con le note fuori schermo" -- il che e' cio' che questa funzione
    dichiara. Sta in `avvertenze()` e non in `verifica()` proprio per questo:
    informa, non blocca.

    Le clip di kit non ci sono: indicizzano le righe per drumIndex, non per
    `y`, e `fit_clip_scroll_to_notes()` le salta per lo stesso motivo.
    """
    fuori = []
    for _, clip in clips(doc):
        if clip.tag == 'audioClip':
            continue
        righe = clip_rows_with_notes(doc, clip)
        yscroll = clip.get('yScroll')
        if not righe or yscroll is None:
            continue
        yscroll = int(yscroll)
        if any(yscroll <= r < yscroll + CLIP_VIEW_ROWS for r in righe):
            continue
        unita = ('righe di drum' if is_kit_clip(clip)
                 else 'gradi' if clip.get('inKeyMode') == '1' else 'semitoni')
        fuori.append(
            f'clip {clip_label(clip)!r}: note su {righe}, nessuna visibile '
            f'con yScroll={yscroll} (finestra {yscroll}-'
            f'{yscroll + CLIP_VIEW_ROWS - 1} in {unita}) -- '
            f'fit_clip_scroll_to_notes() la corregge')
    return fuori


def is_kit_clip(clip: Node) -> bool:
    """Una clip su kit indicizza le righe per drumIndex, non per altezza.

    Nel corpus una noteRow porta `y` oppure `drumIndex`, mai entrambi
    (1686 contro 2059 righe). Guardare le righe e' la prova diretta;
    `affectEntire` — presente su tutte le clip kit e su nessuna synth — serve
    da ripiego quando la clip non ha ancora righe.
    """
    rows = note_rows(clip)
    if any(r.has('drumIndex') for r in rows):
        return True
    if any(r.has('y') for r in rows):
        return False
    return clip.has('affectEntire')


def row_index_attr(clip: Node) -> str:
    return 'drumIndex' if is_kit_clip(clip) else 'y'


#: Il contenitore dei parametri sulla clip, per tipo di strumento.
PARAMS_PER_TIPO = {'kit': 'kitParams', 'sound': 'soundParams'}


def check_clip_types(doc: Document) -> list[str]:
    """Ogni clip deve dichiarare lo stesso tipo da tre parti indipendenti.

    Il tag dei parametri non e' un'etichetta: e' cio' che dice al caricatore
    di che tipo e' la clip. Dal firmware (`instrument_clip.cpp`):

        else if (!strcmp(tagName, "soundParams")) {
            outputTypeWhileLoading = OutputType::SYNTH;

    Quindi una clip di kit con `soundParams` si annuncia come synth, poi mostra
    righe con `drumIndex` e uno strumento `<kit>`: il Deluge rifiuta l'intero
    file come corrotto. E' successo, e non lo aveva visto nessuno dei controlli
    esistenti — il file era XML valido e si rileggeva senza errori.

    Le tre dichiarazioni, che devono concordare:

        il tag <kitParams|soundParams>   il tipo del nodo <kit|sound>
        l'indice delle righe (drumIndex|y)

    Nel corpus: `kitParams` su 395 clip di kit su 395, `soundParams` su tutte
    le clip di synth che hanno un contenitore (153 non ne hanno affatto, ed e'
    lecito). `affectEntire` su 395 clip di kit su 395 e su 0 di synth su 551.
    """
    from . import arranger as A                           # import locale: ciclo

    problemi = []
    for da_arr in (False, True):
        for clip in A.clip_list(doc, da_arr):
            if clip.tag != 'instrumentClip':
                continue
            nome = clip_label(clip)

            # cosa dice la clip di se stessa, da tre parti indipendenti
            righe = note_rows(clip)
            per_righe = (True if any(r.has('drumIndex') for r in righe)
                         else False if any(r.has('y') for r in righe) else None)
            per_flag = clip.has('affectEntire') or None
            per_params = (True if clip.find('kitParams') is not None
                          else False if clip.find('soundParams') is not None
                          else None)

            detto = {'righe': per_righe, 'affectEntire': per_flag,
                     'params': per_params}
            visti = {k: v for k, v in detto.items() if v is not None}
            if len(set(visti.values())) > 1:
                kit = [k for k, v in visti.items() if v]
                syn = [k for k, v in visti.items() if not v]
                problemi.append(
                    f'{nome}: si dichiara di kit secondo {kit} e di synth '
                    f'secondo {syn}; il caricatore userebbe <'
                    f'{PARAMS_PER_TIPO["kit" if per_params else "sound"]}> '
                    f'per dedurre il tipo e rifiuterebbe il file')

            # e se lo strumento si risolve senza ambiguita', deve concordare.
            # Solo per i file che legano per NOME: nei vecchi file a slot due
            # strumenti possono condividere lo slot (un <sound> e un <kit> sullo
            # slot 0 in `Pacmegajam.XML`) e la risoluzione non e' decidibile.
            inst = (instrument_of(doc, clip)
                    if clip.get('instrumentPresetName') is not None else None)
            if (inst is not None and inst.tag in PARAMS_PER_TIPO
                    and visti and len(set(visti.values())) == 1):
                sola = next(iter(visti.values()))
                if sola != (inst.tag == 'kit'):
                    problemi.append(
                        f'{nome}: si dichiara '
                        f'{"di kit" if sola else "di synth"} ma e legata a '
                        f'<{inst.tag}> {nome_strumento(inst)!r}')
    return problemi


def nome_strumento(inst: Node) -> str:
    return (inst.get('presetName') or inst.get('name')
            or f'slot {inst.get("presetSlot")}')


# ------------------------------------------------- dai numeri ai nomi dei drum

def instruments(doc: Document) -> list[Node]:
    """Gli strumenti dichiarati dalla song, nell'ordine del file."""
    node = doc.root.find('instruments')
    return node.children if node else []


def instrument_of(doc: Document, clip: Node) -> Node | None:
    """Lo strumento a cui la clip e' legata, o None se non si risolve.

    La clip non porta nessun riferimento diretto: il legame va ricostruito, e
    il corpus ne mostra QUATTRO forme diverse, tutte ancora in circolazione.
    Vanno provate in quest'ordine, perche' i file recenti portano il nome e
    quelli vecchi solo lo slot numerico:

        instrumentPresetName (+Folder)  ->  presetName (+presetFolder)
        instrumentPresetSlot (+SubSlot) ->  presetSlot (+presetSubSlot)
        trackName                       ->  <audioTrack name=…>
        midiChannel / cvChannel         ->  <midiChannel|cvChannel channel=…>

    Per le clip di kit si pretende anche che il nodo sia un <kit>, cosi' un
    synth omonimo non puo' essere scambiato per un kit.
    """
    want_kit = is_kit_clip(clip)

    name = clip.get('instrumentPresetName')
    if name is not None:
        folder = clip.get('instrumentPresetFolder')
        for inst in instruments(doc):
            if inst.get('presetName') != name:
                continue
            if folder is not None and inst.get('presetFolder') != folder:
                continue
            if want_kit and inst.tag != 'kit':
                continue
            return inst
        return None

    slot = clip.get('instrumentPresetSlot')
    if slot is not None:
        sub = clip.get('instrumentPresetSubSlot')
        for inst in instruments(doc):
            if inst.get('presetSlot') != slot:
                continue
            if sub is not None and inst.get('presetSubSlot') != sub:
                continue
            if want_kit and inst.tag != 'kit':
                continue
            return inst
        return None

    track = clip.get('trackName')
    if track is not None:
        for inst in instruments(doc):
            if inst.tag == 'audioTrack' and inst.get('name') == track:
                return inst
        return None

    for attr, tag in (('midiChannel', 'midiChannel'), ('cvChannel', 'cvChannel')):
        ch = clip.get(attr)
        if ch is None:
            continue
        for inst in instruments(doc):
            if inst.tag == tag and inst.get('channel') == ch:
                return inst
        return None
    return None


def drums(kit: Node) -> list[Node]:
    """I suoni di un <kit>, nell'ordine in cui `drumIndex` li indicizza."""
    ss = kit.find('soundSources')
    return ss.children if ss else []


def drum_names(doc: Document, clip: Node) -> list[str]:
    """I nomi dei drum della clip, indicizzati da `drumIndex`.

    `drumIndex` e' la posizione ordinale dentro <kit>/<soundSources>.
    Verificato su TEMPL4, dove le note erano state messe sul dispositivo in
    posizioni decise in anticipo: l'indice 0 porta le note del kick (movimenti
    1 e 3) e si chiama KICK, l'indice 1 quelle dello snare (2 e 4) e si chiama
    SNARE.
    """
    if not is_kit_clip(clip):
        raise ValueError(f'la clip "{clip_label(clip)}" non e su un kit: '
                         'le sue righe sono altezze, non drum')
    kit = instrument_of(doc, clip)
    if kit is None:
        raise ValueError(f'kit "{clip.get("instrumentPresetName")}" non '
                         'trovato fra gli strumenti della song')
    return [d.get('name') or f'({d.tag} {i})' for i, d in enumerate(drums(kit))]


def drum_index(doc: Document, clip: Node, name: str) -> int:
    """L'indice del drum che si chiama `name`, per non ragionare per numeri.

    Il confronto ignora maiuscole e spazi: sul dispositivo i nomi sono tutti
    maiuscoli, ma chi descrive un pattern non deve doverlo sapere.
    """
    names = drum_names(doc, clip)
    target = name.strip().upper()
    for i, n in enumerate(names):
        if (n or '').strip().upper() == target:
            return i
    raise ValueError(f'nessun drum "{name}" in questo kit. '
                     f'Disponibili: {", ".join(names)}')


def drum_row(doc: Document, clip: Node, name: str, *, create: bool = False) -> Node:
    """La noteRow del drum che si chiama `name`, su una clip di kit.

    Compone drum_index() e note_row(): i due passi che chiunque scrive note
    per nome di drum farebbe comunque, in un solo nome. Con create=False (il
    default) pretende che la riga esista gia' -- vero per ogni clip fatta da
    create.add_track(), che ora le crea tutte all'inizio. create=True serve
    solo per i kit vecchi o modificati a mano che non rispettano quella
    regola (vedi create.py, e le due eccezioni trovate nel corpus).
    """
    i = drum_index(doc, clip, name)
    return note_row(clip, i, create=create)


# ------------------------------------------------------- creazione e copia

#: flag che nel corpus valgono 1 al massimo su una clip per song.
#: Un duplicato deve quindi azzerarli, altrimenti la song avrebbe due clip
#: "in modifica" o due "selezionate".
EXCLUSIVE_FLAGS = ('beingEdited', 'selected')


def set_edited_clip(doc: Document, clip: Node) -> None:
    """Rende `clip` la clip aperta, azzerando il flag sulle altre.

    `beingEdited` dice quale clip il dispositivo apre quando entri in clip
    view. Nel corpus vale 1 su al massimo una clip per song — da qui
    EXCLUSIVE_FLAGS.

    Serve saperlo perche' scrivere un contenuto senza aggiornarlo lo rende
    INVISIBILE: si atterra su un'altra clip e non si vede nulla. Verificato
    sul dispositivo con un'automazione scritta sulla clip 1 mentre
    `beingEdited` era rimasto sulla clip 0: il blob era corretto e non
    compariva. Spostato il flag, e' comparso.

    E' la terza volta che questo progetto incontra la stessa forma — prima
    `yScrollSongView` con la clip fuori schermo, poi lo stato della vista
    automazione. Il dato c'e', manca cio' che ci porta a guardarlo.
    """
    for _, c in clips(doc):
        if c is clip:
            c.set('beingEdited', '1')
        elif c.has('beingEdited'):
            c.set('beingEdited', '0')


def same_instrument(a: Node, b: Node) -> bool:
    """Due clip suonano lo stesso strumento?

    Il criterio dipende dal tipo: preset per synth e kit, nome per le audio
    track, canale per MIDI e CV.
    """
    for key in ('trackName', 'cvChannel', 'midiChannel'):
        if a.has(key) or b.has(key):
            return a.get(key) == b.get(key)
    return (a.get('instrumentPresetName') == b.get('instrumentPresetName')
            and a.get('instrumentPresetFolder') == b.get('instrumentPresetFolder'))


def first_free_section(doc: Document) -> str:
    """La prima sezione dichiarata che nessuna clip sta usando.

    Serve per collocare una variazione in modo che sia lanciabile senza
    fermare l'originale.
    """
    used = {c.get('section') for _, c in clips(doc) if c.has('section')}
    sections = doc.root.find('sections')
    declared = [s.get('id') for s in sections.children] if sections else []
    for sid in declared:
        if sid not in used:
            return sid
    return str(len(declared))


SONG_VIEW_ROWS = 8      # righe fisiche della griglia, numerate 0-7


def _keep_row_visible(doc: Document, attr: str, row: int) -> str | None:
    """Alza lo scroll `attr` quel tanto che basta perche' `row` sia a schermo.

    Nucleo condiviso da song view e arranger: stessa griglia da 8 righe,
    stessa aritmetica. Cambia solo cosa conta come riga.
    """
    root = doc.root
    if not root.has(attr):
        return None                       # song che non dichiara questo scroll
    try:
        current = int(root.get(attr))
    except (TypeError, ValueError):
        return None
    lowest = row - (SONG_VIEW_ROWS - 1)   # scroll minimo che tiene `row` a schermo
    if current >= lowest:
        return None                       # gia' visibile, non tocchiamo la vista
    root.set(attr, str(lowest))
    return str(lowest)


def _keep_view_within(doc: Document, attr: str, last_row: int) -> str | None:
    """Abbassa lo scroll `attr` quel tanto che basta perche' `last_row` sia a
    schermo. Il gemello di `_keep_row_visible`, per il verso opposto.

    Quello alza lo scroll quando il contenuto finisce SOTTO il bordo: e' il
    caso dell'aggiunta. Questo lo abbassa quando la vista resta parcheggiata
    SOPRA il contenuto: e' il caso della rimozione, e produce lo stesso difetto
    visto da HANDOFF §3.1 -- tutto nel file, niente sullo schermo.

    Il caso e' reale, non teorico: 11 song su 36 hanno `yScrollSongView`
    positivo, e Progsong.XML vale 27 con 42 clip. Tolte venti clip, lo scroll
    punterebbe oltre l'ultima.

    Scende SOLO fino a rendere visibile l'ultima riga, e non ri-ancora in
    fondo: il dispositivo stesso tiene l'ultima riga alla riga 7 solo in 15
    song su 36, nelle altre 21 lo scroll e' dove l'ha lasciato una persona.
    Cosa faccia il Deluge quando si cancella non e' mai stato misurato, quindi
    la correzione si ferma a cio' che si puo' dimostrare: la vista non e' cieca.
    """
    root = doc.root
    if not root.has(attr):
        return None                       # song che non dichiara questo scroll
    try:
        current = int(root.get(attr))
    except (TypeError, ValueError):
        return None
    if current <= last_row:
        return None                       # la vista mostra gia' del contenuto
    root.set(attr, str(last_row))
    return str(last_row)


def shrink_song_view_to(doc: Document, last_row: int) -> str | None:
    """Riporta `yScrollSongView` sopra l'ultima clip, se e' rimasto oltre."""
    return _keep_view_within(doc, 'yScrollSongView', last_row)


def shrink_arrangement_view_to(doc: Document, last_row: int) -> str | None:
    """Come sopra per l'arranger, dove le righe sono gli STRUMENTI."""
    return _keep_view_within(doc, 'yScrollArrangementView', last_row)


def scroll_arrangement_view_to(doc: Document, row: int) -> str | None:
    """Come `scroll_song_view_to`, ma per l'arranger, dove le righe sono gli
    STRUMENTI e non le clip.

    Verificato con la scala TEMPL2 -> TEMPL3 -> TEMPL4, tre song salvate dal
    dispositivo a un passo l'una dall'altra:

    - aggiungere note a una clip esistente non muove nessuno dei due scroll
      (nessuna clip nuova, nessuno strumento nuovo)
    - aggiungere una clip di kit, che porta con se' uno strumento nuovo, li
      muove ENTRAMBI di +1: `yScrollSongView` -7 -> -6 e
      `yScrollArrangementView` -7 -> -6

    Nel corpus, in tutte le song salvate dal dispositivo e non riscrollate a
    mano, l'ultimo strumento cade esattamente alla riga 7, come l'ultima clip.

    Oggi nessuno la chiama: `duplicate_clip` riusa lo strumento della clip
    sorgente, quindi non ne aggiunge. Serve appena esistera' un percorso che
    crea strumenti — e dimenticarsene riprodurrebbe nell'arranger il caso
    yScrollSongView, che e' costato due sessioni.
    """
    return _keep_row_visible(doc, 'yScrollArrangementView', row)


def scroll_song_view_to(doc: Document, row: int) -> str | None:
    """Alza `yScrollSongView` quel tanto che basta perche' `row` sia a schermo.

    In song view ogni clip e' una riga, e la finestra visibile parte da
    `yScrollSongView`: la clip di indice i sta alla riga di schermo
    `i - yScrollSongView`. Il manuale, cap. 7 Song View:

        «Individual clips compressed to one row each in song view. The rows can
        be navigated up and down BEYOND THE 8 PHYSICALLY DISPLAYED.»

    Accodare una clip senza toccare lo scroll la manda alla riga 8, che non
    esiste. La clip c'e' ed e' caricata, ma resta sotto il bordo inferiore
    dello schermo — ed e' esattamente il motivo per cui la clip duplicata
    "non compariva", cosa che e' costata un'indagine intera perche' cercata
    dentro la clip invece che nel nodo <song>.

    Verificato sul dispositivo con due file diversi per un solo byte: quello
    con yScrollSongView="-5" mostra 3 righe su 4, quello con "-4" tutte e 4.
    Vedi docs/TEST_yscroll.md.

    E' anche cio' che fa il dispositivo: clonando una clip passa da -5 a -4,
    per tenere la riga nuova in fondo allo schermo. Confermato una seconda
    volta, in modo controllato, dalla scala TEMPL3 -> TEMPL4: una clip in piu'
    e lo scroll passa da -7 a -6, che e' esattamente quello che calcola questa
    funzione.

    Ritorna il nuovo valore, o None se non c'era bisogno di toccarlo.
    """
    return _keep_row_visible(doc, 'yScrollSongView', row)


def duplicate_clip(doc: Document, index: int, *, section: str | None = None,
                   name: str | None = None,
                   colour_offset: str | None = None) -> Node:
    """Copia la clip `index` e la accoda al suo stesso contenitore.

    E' il pattern "template-injection": si parte da una clip vera, con tutti i
    suoi soundParams, arpeggiator e patch cable gia' coerenti, invece di
    costruirne una da zero.

    LA COPIA NASCE FERMA (isPlaying="0"), e non e' un dettaglio estetico.
    Il manuale, capitolo Song View:

        «Deluge will only play one instrument at one time in song view. So for
        example, if two clips use the same synth preset, the clip rows can each
        be launched but each one will stop playback of the other»

        «Where there are multiple instances of the same instrument preset they
        will not play simultaneously.»

    Due clip sullo stesso strumento sono VARIAZIONI, mutuamente esclusive.
    Lasciare la copia in riproduzione mentre lo e' anche l'originale descrive
    uno stato che il dispositivo non puo' rappresentare: caricando la song, il
    Deluge ne scarta una — cosa osservata sul dispositivo prima di capirne il
    motivo.

    Diverso e' il caso di piu' clip che suonano insieme in una sezione: quella
    e' polifonia fra strumenti DIVERSI, non fra clip dello stesso strumento.
    """
    all_clips = clips(doc)
    if not 0 <= index < len(all_clips):
        raise IndexError(f'clip {index} inesistente (ce ne sono {len(all_clips)})')
    container_tag, src = all_clips[index]
    container = doc.root.find(container_tag)

    dup = src.copy()
    for flag in EXCLUSIVE_FLAGS:
        if dup.has(flag):
            dup.set(flag, '0')
    # la variazione nasce ferma: la fa partire chi lancia la sezione
    if dup.has('isPlaying'):
        dup.set('isPlaying', '0')
    if dup.has('isSoloing'):
        dup.set('isSoloing', '0')
    if section is not None:
        dup.set('section', str(section))
    if name is not None:
        dup.set('clipName', name)
    if colour_offset is not None:
        dup.set('colourOffset', str(colour_offset))

    container.append(dup)

    # la riga nuova deve stare a schermo, altrimenti la clip esiste ma non si
    # vede: song view mostra 8 righe e la copia finisce in fondo
    if container_tag == 'sessionClips':
        scroll_song_view_to(doc, len(container.children) - 1)

    # avviso, non errore: due variazioni nella stessa sezione sono legali ma
    # si fermano a vicenda, quindi quasi mai e' cio' che si vuole
    if section is None and same_instrument(src, dup):
        import warnings
        warnings.warn(
            f'la copia resta nella sezione {dup.get("section")} come '
            f'l originale e suona lo stesso strumento: essendo variazioni '
            f'mutuamente esclusive, lanciarne una fermera l altra. '
            f'Passa section= per renderle lanciabili separatamente.',
            stacklevel=2)
    return dup


def add_note_row(clip: Node, index: int) -> Node:
    """Crea una <noteRow> vuota nella posizione giusta.

    `index` e' un'altezza MIDI per le clip melodiche e un numero di suono del
    kit per quelle su kit: l'attributo giusto viene scelto da row_index_attr().

    Le noteRow sono sempre ordinate per indice crescente: verificato su tutte
    le 308 clip del corpus, nessuna eccezione. Inserire in fondo romperebbe
    l'invariante.
    """
    attr = row_index_attr(clip)
    rows_parent = clip.find('noteRows')
    if rows_parent is None:
        rows_parent = clip.append(Node(tag='noteRows'))

    for r in rows_parent.children:
        if r.has(attr) and int(r.get(attr)) == index:
            raise ValueError(f'esiste gia una noteRow con {attr}={index}')

    row = Node(tag='noteRow', attrs=[(attr, str(index))], self_closing=True)
    pos = len(rows_parent.children)
    for i, r in enumerate(rows_parent.children):
        if r.has(attr) and int(r.get(attr)) > index:
            pos = i
            break
    rows_parent.insert(pos, row)
    return row


def note_row(clip: Node, index: int, create: bool = False) -> Node:
    """La noteRow per `index`; la crea se manca e create=True."""
    attr = row_index_attr(clip)
    for r in note_rows(clip):
        if r.has(attr) and int(r.get(attr)) == index:
            return r
    if not create:
        have = ', '.join(str(r.get(attr)) for r in note_rows(clip) if r.has(attr))
        raise ValueError(f'nessuna noteRow con {attr}={index}. Presenti: {have}')
    return add_note_row(clip, index)


# ------------------------------------------------------------------ rimozione

#: I contenitori di clip, nell'ordine in cui `clips()` li visita.
CONTENITORI_CLIP = ('sessionClips', 'arrangementOnlyTracks', 'arrangementClips')


def remove_clip(doc: Document, clip: Node) -> dict:
    """Toglie una clip dalla song, e rinumera cio' che la seguiva.

    L'operazione pericolosa di questo modulo, come `kit.remove_drum` lo e' del
    suo: il censimento del corpus dice che a una clip puntano DUE cose sole --
    i `clipCode` nell'arranger e `yScrollSongView` -- ma nessuna delle due la
    nomina, entrambe la contano.

    Ritorna il rapporto di cosa e' stato mosso.
    """
    from . import arranger as A                           # import locale: ciclo

    dove = A.index_of(doc, clip)
    if dove is None:
        raise ValueError(f'la clip "{clip_label(clip)}" non appartiene a '
                         'questa song')
    indice, da_arranger = dove

    for nome in CONTENITORI_CLIP:
        cont = doc.root.find(nome)
        if cont is not None and any(c is clip for c in cont.children):
            cont.children = [c for c in cont.children if c is not clip]
            cont.touch()
            break

    rapporto = {'clip': clip_label(clip), 'indice': indice, 'lista': nome}
    rapporto.update(A.renumber_after_removal(doc, indice, da_arranger))

    # song view conta le clip di sessione, e solo quelle: le tracce di solo
    # arranger non hanno una riga li'
    if nome == 'sessionClips':
        sceso = shrink_song_view_to(doc, len(cont.children) - 1)
        if sceso is not None:
            rapporto['yScrollSongView'] = sceso
    return rapporto


def map_notes(clip: Node, f) -> int:
    """Riscrive ogni nota di ogni riga passandola per `f`. Ritorna quante.

    `f` riceve una `Note` e ne ritorna una nuova -- usare
    `dataclasses.replace`, cosi' i campi che non c'entrano (velocity, lift,
    condition, iterance) viaggiano intatti invece di essere ricostruiti coi
    default, che li perderebbe in silenzio.
    """
    quante = 0
    for r in note_rows(clip):
        note = read_notes(r)
        if not note:
            continue
        write_notes(r, [f(n) for n in note], create=True)
        quante += len(note)
    return quante


def first_note_pos(clip: Node) -> int | None:
    """La posizione della nota piu' a sinistra, o None se la clip e' muta."""
    pos = [n.pos for r in note_rows(clip) for n in read_notes(r)]
    return min(pos) if pos else None


def retune_rows(clip: Node, mappa: dict[int, int]) -> dict:
    """Riassegna le altezze delle righe secondo `mappa` (y vecchio -> y nuovo).

    Le righe non nominate dalla mappa restano dove sono. Due righe che
    finiscono sulla STESSA altezza vengono FUSE: le note della seconda si
    aggiungono alla prima. Non e' un caso di laboratorio -- la trasposizione
    per gradi non e' biiettiva e lo produce in qualunque scala.

    Se due note fuse cadono sulla stessa posizione ne resta una sola: dentro
    una noteRow le posizioni sono strettamente crescenti (FINDINGS §note), e
    due note allo stesso tick sarebbero una riga che il firmware non scrive
    mai. Quante se ne perdono sta nel rapporto, perche' perdere musica in
    silenzio e' la cosa peggiore che possa fare questa funzione.
    """
    cont = clip.find('noteRows')
    if cont is None:
        return {'righe': 0, 'fuse': 0, 'note_perse': 0}

    senza_y = [r for r in cont.children if not r.has('y')]
    per_nuova = {}
    fuse = perse = 0

    for r in [x for x in cont.children if x.has('y')]:
        nuova = mappa.get(int(r.get('y')), int(r.get('y')))
        base = per_nuova.get(nuova)
        if base is None:
            r.set('y', str(nuova))
            per_nuova[nuova] = r
            continue
        fuse += 1
        note = read_notes(base)
        occupate = {n.pos for n in note}
        for n in read_notes(r):
            if n.pos in occupate:
                perse += 1
                continue
            occupate.add(n.pos)
            note.append(n)
        write_notes(base, note, create=True)

    cont.children = senza_y + [per_nuova[y] for y in sorted(per_nuova)]
    cont.touch()
    return {'righe': len(per_nuova) + fuse, 'fuse': fuse, 'note_perse': perse}


def remove_note_row(clip: Node, row: Node) -> dict:
    """Toglie una noteRow. Su una clip di KIT viene rifiutato, e si spiega.

    Su un synth la riga E' un'altezza (`y`): non la indicizza nessuno,
    toglierla non lascia riferimenti appesi.

    Su un kit la riga e' indicizzata da `drumIndex`, e nel corpus 393 clip di
    kit su 395 hanno una riga per OGNI drum, con indici contigui da 0. Toglierne
    una romperebbe l'invariante e il file verrebbe fermato da `verifica()`.
    Quello che una persona chiede dicendo "togli il rullante" e' una di due
    cose diverse, e vanno tenute diverse:

        la riga in questa clip  ->  svuotarla: `write_notes(riga, [])`
        il drum dal kit         ->  `kit.remove_drum()`, che rinumera tutto
    """
    if is_kit_clip(clip):
        raise ValueError(
            f'"{clip_label(clip)}" e una clip di kit: le sue righe non si '
            'tolgono, una per drum deve esserci sempre. Per farla tacere qui '
            'svuotala con write_notes(riga, []); per togliere il drum dal kit '
            'usa kit.remove_drum(), che rinumera i drumIndex di tutte le clip')

    cont = clip.find('noteRows')
    if cont is None or not any(r is row for r in cont.children):
        raise ValueError(f'la riga non appartiene a "{clip_label(clip)}"')
    cont.children = [r for r in cont.children if r is not row]
    cont.touch()
    return {'clip': clip_label(clip), 'y': row.get('y'),
            'note': len(read_notes(row))}


def remove_instrument(doc: Document, inst: Node) -> dict:
    """Toglie uno strumento e tutte le clip che lo suonano.

    Nessun ordinale punta a uno strumento: le clip lo risolvono per nome, slot
    o canale (`instrument_of`, quattro forme). Non c'e' quindi niente da
    rinumerare fra gli strumenti -- ma le clip che lo nominano resterebbero
    APPESE, presenti e senza piu' niente che le suoni, quindi vanno via con lui.

    Le clip si tolgono UNA ALLA VOLTA, ricalcolando ogni volta quali sono sue:
    ogni `remove_clip` rinumera i `clipCode`, e una lista raccolta in anticipo
    sarebbe indici vecchi applicati a una song gia' cambiata. E' la stessa
    trappola che `kit.remove_drum` evita rinumerando in un colpo solo.
    """
    from . import arranger as A                           # import locale: ciclo

    if not any(i is inst for i in instruments(doc)):
        raise ValueError(f'lo strumento "{A.nome_di(inst)}" non appartiene a '
                         'questa song')

    rapporto = {'strumento': A.nome_di(inst), 'tipo': inst.tag, 'clip': []}
    while True:
        sue = [c for _, c in clips(doc) if instrument_of(doc, c) is inst]
        if not sue:
            break
        rapporto['clip'].append(remove_clip(doc, sue[0])['clip'])

    cont = doc.root.find('instruments')
    cont.children = [i for i in cont.children if i is not inst]
    cont.touch()

    # l'arranger conta gli STRUMENTI, non le clip: una riga in meno anche li'
    sceso = shrink_arrangement_view_to(doc, len(cont.children) - 1)
    if sceso is not None:
        rapporto['yScrollArrangementView'] = sceso
    return rapporto


def clip_summary(clip: Node) -> dict:
    rows = note_rows(clip)
    total = sum(len(read_notes(r)) for r in rows)
    return {
        'tipo': clip.tag,
        'nome': clip_label(clip),
        'length': clip.get('length'),
        'section': clip.get('section'),
        'righe': len(rows),
        'note': total,
    }
