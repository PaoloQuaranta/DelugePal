"""Lo strato musicale: dalla lingua che parliamo alle chiamate alla libreria.

Questo modulo non COSTRUISCE ne' SERIALIZZA XML: chi vuole scrivere un file
passa da `delugexml.song`, `create`, `arranger`. Qui si traduce lingua
musicale -- altezze, ritmi, intenzioni -- in chiamate a quella libreria.

`verifica()` e `avvertenze()`, in fondo al file, prendono in ingresso un
`Document` gia' costruito altrove: non lo fabbricano, lo leggono soltanto,
per validare la traduzione appena fatta prima che esca. E' il motivo per
cui il cancello sta qui e non in `song.py`: e' il punto di uscita di questo
strato, non un'altra fabbrica di XML.
"""
from __future__ import annotations

import re

#: I gradi della scala cromatica dal do, per nome.
NOMI_IT = {'do': 0, 're': 2, 'mi': 4, 'fa': 5, 'sol': 7, 'la': 9, 'si': 11}
NOMI_EN = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}

#: Come si scrive un'altezza in uscita, preferendo i diesis.
CROMATICA_IT = ('do', 'do#', 're', 're#', 'mi', 'fa', 'fa#', 'sol', 'sol#',
                'la', 'la#', 'si')
CROMATICA_EN = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

#: do4 = 60, la convenzione MIDI standard.
OTTAVA_DEL_DO_CENTRALE = 4

# Il '#' e' inequivocabile (non e' mai una lettera di nota) e lo cattura la
# regex. La 'b' del bemolle invece e' anche una lettera di nota inglese, e
# in italiano e' l'ultima lettera di 'sol' e 'si': va sciolta a mano, vedi
# `_grado_e_bemolle`.
_ALTEZZA = re.compile(r'^([a-z]+)(#)?(-?\d+)$')


def _grado_e_bemolle(lettere: str) -> tuple[int | None, bool]:
    """Riconosce la base italiana o inglese dentro `lettere`.

    Si prova prima il nome per intero (compresi quelli di piu' lettere come
    'sol' o 'si'): se combacia, non c'e' bemolle. Solo se non combacia, e se
    finisce per 'b', si riprova togliendo quella 'b' finale e trattandola
    come bemolle attaccato alla nota. Cosi' 'sib' e' si bemolle (non 'si' +
    lettera a caso) e 'bb' e' b (inglese) bemolle, mentre 'b' da sola resta
    la nota inglese si, naturale — non c'e' ambiguita' perche' nessun nome
    completo (ne' italiano ne' inglese) finisce gia' per 'b'.
    """
    if lettere in NOMI_IT:
        return NOMI_IT[lettere], False
    if lettere in NOMI_EN:
        return NOMI_EN[lettere], False
    if len(lettere) > 1 and lettere[-1] == 'b':
        base = lettere[:-1]
        if base in NOMI_IT:
            return NOMI_IT[base], True
        if base in NOMI_EN:
            return NOMI_EN[base], True
    return None, False


def altezza(nome: str) -> int:
    """Il numero MIDI di un nome di altezza: `do4`, `C4`, `fa#3`, `mib5`.

    Accetta nomi italiani e inglesi, maiuscole o minuscole indifferentemente.
    do4 = C4 = 60, la convenzione MIDI standard (do centrale).
    """
    if not isinstance(nome, str):
        raise ValueError(f'altezza() vuole un nome (stringa) come "do4", '
                         f'non {type(nome).__name__} ({nome!r})')
    testo = nome.strip().lower()
    m = _ALTEZZA.match(testo)
    if not m:
        raise ValueError(f'{nome!r} non e un nome di altezza (es. do4, fa#3)')
    lettere, diesis, ottava = m.group(1), m.group(2), int(m.group(3))

    grado, bemolle = _grado_e_bemolle(lettere)
    if grado is None:
        raise ValueError(f'{nome!r}: {lettere!r} non e una nota')

    if diesis:
        grado += 1
    elif bemolle:
        grado -= 1

    midi = (ottava + 1) * 12 + grado
    if not 0 <= midi <= 127:
        raise ValueError(f'{nome!r} da {midi}, fuori dall estensione MIDI 0-127')
    return midi


def nome_altezza(midi: int, italiano: bool = True) -> str:
    """Il nome di un numero MIDI, coi diesis: 60 -> 'do4'."""
    if not 0 <= midi <= 127:
        raise ValueError(f'{midi} fuori dall estensione MIDI 0-127')
    tabella = CROMATICA_IT if italiano else CROMATICA_EN
    return f'{tabella[midi % 12]}{midi // 12 - 1}'


# ------------------------------------------------------------------ ritmi

from .notes import Note                                   # noqa: E402

#: La griglia del Deluge e' larga 16 colonne per battuta, e una battuta e'
#: 384 tick: ogni colonna e' un sedicesimo.
TICK_PER_PASSO = 24
TICK_PER_BATTUTA = 384

#: Un movimento (quarto) e' 4 sedicesimi: e' il taglio minimo ammesso per
#: un pattern, non la battuta intera. [BUG capitolato] la versione proposta
#: nel capitolato esigeva un multiplo di 16 (una battuta intera), ma il test
#: passa un pattern di 8 caratteri ('X...x...', mezza battuta) aspettandosi
#: che venga accettato: verificato che 4 (un movimento) e' il taglio giusto.
PASSI_PER_MOVIMENTO = 4

#: I caratteri di un pattern a passi.
PAUSA = '.'
COLPO = 'x'
ACCENTO = 'X'
#: Il colpo FANTASMA: quello che non si sente come evento ma come tessuto.
#: [LACUNA trovata usando la libreria, 16 agosto 2026] Fino a qui i livelli
#: erano due, `x` e `X`, e con due livelli un pattern resta piatto: i colpi
#: fantasma sono meta' del mestiere di chi programma una batteria, e senza
#: di loro il groove "marcia" invece di respirare.
FANTASMA = 'o'

#: Velocity di default per i tre livelli. I numeri non sono inventati: la
#: pratica corrente di programmazione li colloca cosi' su 127 --
#: 110-127 massimo, 100-110 forte, 90-100 normale, 80-90 sottovoce,
#: sotto 70 fantasma (35-50 per un rullante fantasma).
VEL_COLPO = 90
VEL_ACCENTO = 110
VEL_FANTASMA = 42


def passi(pattern: str, *, velocity: int = VEL_COLPO,
          accento: int = VEL_ACCENTO, fantasma: int = VEL_FANTASMA,
          lunghezza: int | None = None, da: int = 0) -> list[Note]:
    """Le note di un pattern percussivo: `'x...x...x...x...'`.

    Un carattere per sedicesimo, come le colonne della griglia del Deluge:
    `x` colpo, `X` colpo accentato, **`o` colpo fantasma**, `.` silenzio. La
    lunghezza dev'essere un multiplo di 4, cioe' un numero intero di
    movimenti (non serve una battuta intera: mezza battuta o un solo
    movimento sono pattern validi).

    I tre livelli servono a una cosa sola, ed e' la ragione per cui il
    fantasma e' stato aggiunto: **con due soli livelli il groove marcia.**
    Un charleston fatto di colpi tutti uguali appiattisce il polso, e un
    rullante senza fantasma fra un accento e l'altro non ha tessuto. Vedi
    `docs/MUSICA.md`, «Velocity groove».

    `lunghezza`, se data, e' GIA' in tick grezzi -- la DURATA della nota,
    non il passo fra una e l'altra. [NOME CORRETTO] si chiamava `durata`
    fino alla revisione finale, e il nome era ingannevole: in `melodia()` e
    `accordi()` (qui sotto) `durata` e' tutt'altra cosa, il PASSO fra le
    note, e passa SEMPRE da `durata_in_tick()` (accetta '1/8' come una
    stringa). Chiamare `passi(pattern, durata='1/8')` non sollevava nulla e
    creava una `Note` con `length` uguale alla stringa `'1/8'`, che esplode
    molto piu' tardi con un `AttributeError` lontano dalla causa. Rinominato
    apposta perche' un nome diverso obbliga a controllare cosa si vuole
    dire, invece di trascinare l'abitudine presa con `melodia()`.
    """
    if not isinstance(pattern, str):
        raise ValueError(f'passi() vuole una stringa di passi (es. '
                         f'"x...x..."), non {type(pattern).__name__} '
                         f'({pattern!r})')
    if lunghezza is not None and not isinstance(lunghezza, int):
        raise ValueError(
            f'lunghezza deve essere un intero in tick grezzi, non '
            f'{type(lunghezza).__name__} ({lunghezza!r}) -- per una durata '
            f'come "1/8" usare durata_in_tick() prima di passarla qui')
    testo = pattern.replace(' ', '')
    if not testo or len(testo) % PASSI_PER_MOVIMENTO:
        raise ValueError(
            f'un pattern ha una lunghezza multipla di {PASSI_PER_MOVIMENTO} '
            f'passi (un movimento), questo ne ha {len(testo)}')
    ammessi = {PAUSA, COLPO, ACCENTO, FANTASMA}
    estranei = sorted(set(testo) - ammessi)
    if estranei:
        raise ValueError(f'caratteri non ammessi {estranei}, '
                         f'usare {sorted(ammessi)}')
    livello = {COLPO: velocity, ACCENTO: accento, FANTASMA: fantasma}
    lung = TICK_PER_PASSO if lunghezza is None else lunghezza
    out = []
    for i, c in enumerate(testo):
        if c == PAUSA:
            continue
        out.append(Note(pos=da + i * TICK_PER_PASSO, length=lung,
                        velocity=livello[c]))
    return out


def durata_in_tick(spec: str | int) -> int:
    """`'1/8'` -> 48 tick. Un intero passa invariato, gia' in tick."""
    if isinstance(spec, int):
        if spec <= 0:
            raise ValueError(f'{spec} tick: la durata deve essere positiva')
        return spec
    testo = str(spec).strip()
    if '/' not in testo:
        raise ValueError(f'{spec!r} non e una durata (es. 1/8, 1/4)')
    num, den = testo.split('/', 1)
    try:
        n, d = int(num), int(den)
    except ValueError:
        raise ValueError(f'{spec!r} non e una durata (es. 1/8, 1/4)') from None
    if d <= 0 or n <= 0:
        raise ValueError(f'{spec!r}: numeratore e denominatore positivi')
    tick = TICK_PER_BATTUTA * n // d
    if tick <= 0:
        raise ValueError(f'{spec!r} da {tick} tick')
    return tick


#: Vocabolario delle articolazioni: quanta parte del passo occupa la nota,
#: in proporzione (non un numero fisso di tick). E' una proporzione e non
#: un valore assoluto perche' un tick fisso non scala col tempo: pochi tick
#: sono impercettibili a un passo lento e sproporzionati a uno veloce, una
#: frazione del passo invece resta lo stesso "sapore" a qualunque tempo.
#: 'legato' = 1.0: la nota dura quanto il passo, cioe' tocca la successiva.
ARTICOLAZIONI = {
    'staccato': 0.5,
    'normale': 0.85,
    'legato': 1.0,
}


def melodia(spec: str, *, durata: str | int = '1/8', da: int = 0,
            velocity: int = 80, articolazione: str = 'normale',
            stacco: int | None = None) -> dict[int, list[Note]]:
    """Da `'re2 fa#2 la2 re3'` alle note, raggruppate per altezza.

    Il Deluge tiene le note in righe, una per altezza, quindi il risultato e'
    un dizionario altezza -> note e non una lista piatta: due `re2` nella
    stessa frase finiscono nella STESSA riga, non in due.

    Un punto e' una pausa: occupa il suo posto e non produce nota.
    `articolazione` e' il vocabolario espressivo (vedi `ARTICOLAZIONI`): un
    basso vuole 'staccato', un pad 'legato'. `stacco`, se dato, e' uno
    scavalco esplicito in tick e vince sull'articolazione, per chi vuole il
    controllo fine.
    """
    if not isinstance(spec, str):
        raise ValueError(f'melodia() vuole una stringa di altezze (es. '
                         f'"do4 re4"), non {type(spec).__name__} ({spec!r})')
    if articolazione not in ARTICOLAZIONI:
        raise ValueError(
            f'articolazione {articolazione!r} sconosciuta, usare '
            f'{sorted(ARTICOLAZIONI)}')
    passo = durata_in_tick(durata)
    if stacco is not None:
        lung = max(1, passo - stacco)
    else:
        lung = max(1, round(passo * ARTICOLAZIONI[articolazione]))
    out: dict[int, list[Note]] = {}
    for i, gettone in enumerate(spec.split()):
        if gettone == PAUSA:
            continue
        y = altezza(gettone)
        out.setdefault(y, []).append(
            Note(pos=da + i * passo, length=lung, velocity=velocity))
    return out


#: Il separatore fra un accordo e il successivo, dentro `accordi()`.
SEPARATORE_ACCORDI = '|'


def accordi(spec: str, *, durata: str | int = '1/4', da: int = 0,
           velocity: int = 80, articolazione: str = 'normale',
           stacco: int | None = None) -> dict[int, list[Note]]:
    """Da `'re3 fa3 la3 | sib3 re4 fa4'` a una PROGRESSIONE di accordi.

    [LACUNA capitolato] `melodia()` mette una nota per passo, in sequenza:
    e' giusto per una linea, ma un accordo vuole le sue note ALLA STESSA
    posizione, e un accompagnamento e' quasi sempre una PROGRESSIONE, non
    un accordo isolato -- da qui il separatore `|`, cosi' un'intera
    progressione si scrive in una riga sola.

    Ogni gruppo separato da `|` e' un accordo: le altezze al suo interno,
    separate da spazi come in `melodia()`, condividono tutte la stessa
    posizione. Un gruppo che e' un solo punto (`'.'`) e' una pausa: occupa
    il suo passo e non produce nessuna nota, esattamente come in
    `melodia()`.

    Il resto e' identico a `melodia()`, di proposito -- stesso vocabolario,
    stessa firma dove ha senso: `durata` e' il passo fra un accordo e il
    successivo, `articolazione` (vedi `ARTICOLAZIONI`) e `stacco` governano
    quanto dura ogni nota dentro il suo passo, e il ritorno raggruppa per
    altezza (`y -> note`) perche' e' cosi' che il Deluge tiene le righe di
    una clip: due accordi che condividono un'altezza mettono le loro note
    nella STESSA riga, non in due.
    """
    if not isinstance(spec, str):
        raise ValueError(f'accordi() vuole una stringa di accordi (es. '
                         f'"do3 mi3 sol3"), non {type(spec).__name__} '
                         f'({spec!r})')
    if articolazione not in ARTICOLAZIONI:
        raise ValueError(
            f'articolazione {articolazione!r} sconosciuta, usare '
            f'{sorted(ARTICOLAZIONI)}')
    if not spec.strip():
        raise ValueError('accordi(): la sequenza e vuota')
    passo = durata_in_tick(durata)
    if stacco is not None:
        lung = max(1, passo - stacco)
    else:
        lung = max(1, round(passo * ARTICOLAZIONI[articolazione]))

    out: dict[int, list[Note]] = {}
    for i, gruppo in enumerate(spec.split(SEPARATORE_ACCORDI)):
        gettoni = gruppo.split()
        if not gettoni or gettoni == [PAUSA]:
            continue
        pos = da + i * passo
        for gettone in gettoni:
            if gettone == PAUSA:
                continue
            y = altezza(gettone)
            out.setdefault(y, []).append(
                Note(pos=pos, length=lung, velocity=velocity))
    return out


# ------------------------------------------------------------------ il cancello

def verifica(doc) -> list[str]:
    """Tutti i controlli che BLOCCANO, in una chiamata sola.

    **Nessun file sale sul Deluge se questa lista non e' vuota.** Non e' una
    formalita': due file generati in questo progetto erano XML validi, si
    rileggevano senza errori, e il dispositivo li ha rifiutati -- uno con un
    crash. Ma i due casi non sono fermati dalla stessa cosa, e affermarlo
    genericamente e' FALSO -- misurato, non supposto:

    - il rifiuto "file corrupted" (`docs/FINDINGS.md` sezione 6-quater, una
      clip di kit che si dichiarava synth via `soundParams`) e' esattamente
      cio' che ferma `check_clip_types()`, qui sotto: dimostrato.
    - il crash E365 (sezione 6-quinquies, il `<params>` di una clip audio
      troncato da 31 a 11 attributi con valori inventati) questo cancello
      NON lo ferma. Misurato riproducendo quel file: `verifica()` ritorna
      `[]`, e `avvertenze()` pure. `docs/FINDINGS.md` lo dice gia': il file
      era XML valido, si rileggeva, e passava `check_clip_types()` e
      `arranger.check()` -- "nessun controllo semantico puo' accorgersi di
      dati inventati che sembrano giusti". Cio' che ferma DAVVERO questo
      caso e' la regola "mai trascrivere a mano, le costanti si generano da
      codice" (skill deluge-pal, regola 2) piu' `test_audio_costanti`, che
      confronta la costante incorporata col nodo vero attributo per
      attributo e figlio per figlio.

      Non allargare qui il cancello per farlo diventare vero: e' gia'
      misurato che non si puo' senza aprire un altro falso positivo. Delle
      194 clip audio scritte dal dispositivo, 109 hanno esattamente 11
      attributi nel loro `<params>` (distribuzione: 11x109, 12x13, 14x1,
      15x65, 16x2, 31x3, 32x1) -- un controllo di completezza accuserebbe
      190 file su 194 SANI. E' la stessa trappola dei falsi positivi gia'
      costata due volte in questo progetto (vedi `same_section_conflicts()`
      e `notes_beyond_clip_end()` in `avvertenze()`).

    [DEVIAZIONE dal capitolato] La bozza includeva anche
    `song.same_section_conflicts()`; qui non c'e', perche' non descrive uno
    stato che il dispositivo rifiuta -- vedi `avvertenze()`, dove sta ora.

    Non tutti i controlli rimasti hanno lo stesso grado di prova, e va detto
    con onesta':

    - `check_clip_types()` e' **dimostrato**: e' la causa nota del rifiuto
      "file corrupted" (`docs/FINDINGS.md` sezione 6-quater).
    - `arranger.check()` coglie riferimenti che non risolvono affatto:
      l'indice oltre la fine della lista (la clip non esiste piu'), e
      l'indice che risolve alla clip di un ALTRO strumento (indici scalati,
      tipicamente una clip rimossa senza rinumerare) -- stati che un
      caricatore non puo' interpretare, non solo subottimali.
    - `kit.check_indices()` coglie lo stesso genere di riferimento rotto sul
      lato kit: `drumIndex` non contigui da 0 (una riga manca o e' fuori
      sequenza), e `drumIndex` oltre il numero di drum che il kit ha
      davvero.
    - `audio.check()` coglie il legame clip-traccia rotto (un `trackName`
      che non risolve a nessun `<audioTrack>`) e le posizioni del campione
      incoerenti (`endSamplePos` non oltre `startSamplePos`). NON copre il
      caso del crash qui sopra: un `<params>` con pochi attributi ma tutti
      sintatticamente validi non si distingue da uno vero guardando solo la
      struttura -- e' esattamente il buco che questo cancello non chiude.

    [OSS] Due controlli restano per prudenza, non per prova diretta -- hanno
    la STESSA forma logica di `same_section_conflicts()`, che si e' rivelata
    non bloccante (vedi `avvertenze()`), e potrebbero risultare altrettanto
    tollerati dal firmware invece che causa di rifiuto:

    - `arranger.check()`, il caso "istanze sovrapposte sullo stesso
      strumento": il file contiene entrambe le clip, semplicemente non
      possono suonare insieme -- nessuna prova che il dispositivo lo rifiuti.
    - `midicv.check()`, il caso "stesso canale e stesso suffisso": stessa
      forma, stesso dubbio.

    Restano qui perche' non c'e' nemmeno la prova del contrario -- a
    differenza di `same_section_conflicts()`, che e' stata spostata solo
    dopo aver trovato la prova che il dispositivo la scrive lui stesso 91
    volte nel corpus. Andrebbero verificati con una coppia controllata sul
    dispositivo, come si e' fatto per la struttura dell'arranger (sezione
    6-ter) e per il tipo di clip (sezione 6-quater), prima di poter
    affermare con certezza se bloccano o solo degradano.
    """
    from . import song as S                               # import locale: ciclo
    from . import arranger as A                            # noqa: PLC0415
    from . import midicv as M                              # noqa: PLC0415
    from . import audio as AU                              # noqa: PLC0415
    from . import kit as K                                 # noqa: PLC0415

    problemi = []
    problemi += S.check_clip_types(doc)
    problemi += A.check(doc)
    problemi += M.check(doc)
    problemi += AU.check(doc)
    for strumento in S.instruments(doc):
        if strumento.tag == 'kit':
            problemi += K.check_indices(doc, strumento)
    return problemi


def avvertenze(doc) -> list[str]:
    """Cio' che NON blocca il caricamento ma chi genera deve sapere.

    **`verifica()` blocca, `avvertenze()` informa.** La differenza non e'
    cosmetica: qui dentro va tutto cio' che il dispositivo carica e fa
    suonare comunque, ma con un effetto collaterale silenzioso che solo
    guardando lo schermo si nota -- la stessa famiglia di `yScrollSongView`
    (contenuto presente, invisibile).

    Contiene `song.same_section_conflicts()`: due clip dello stesso
    strumento nella stessa sezione. In grid view se ne vede una sola; la
    seconda c'e', carica e suona, ma non ha una colonna dove mostrarsi. Non
    e' un'ipotesi -- e' il dispositivo STESSO a scriverlo cosi': nel corpus
    dei 139 file scritti dal Deluge questo pattern compare in **91 sezioni
    di 18 file** (`docs/FINDINGS.md`, sezione sulle sezioni: "e' legale ma
    degradato"), quindi non puo' essere un motivo di rifiuto -- e per quello
    non e' in `verifica()`. E' pero' un'informazione persa se non la si
    espone: chi genera una song vuole sapere che una clip finira' in una
    colonna gia' occupata e non si vedra', per correggere la sezione se
    vuole, non per rinunciare a caricare.

    [LACUNA capitolato] Contiene anche `song.notes_beyond_clip_end()`: note
    la cui posizione supera la fine della propria clip (o della propria
    noteRow, se ha un `length` piu' lungo -- vedi li' per il perche').
    Emersa dalla prova d'accettazione finale: una progressione scritta piu'
    lunga della clip che la ospita produce un file valido che il
    dispositivo carica senza protestare, ma quelle note restano mute in
    silenzio. Stessa famiglia di `yScrollSongView` e dello stesso conflitto
    di sezione qui sopra -- contenuto presente, inudibile.

    Contiene anche `song.notes_hidden_by_scroll()`: il gemello a livello di
    CLIP di `yScrollSongView` (HANDOFF.md 3.1) -- note scritte che restano
    sotto la finestra di scroll ereditata da `create.add_track()`
    (`yScroll='37'` su ogni clip nuova, indipendente da cosa ci si scrive).
    `out/genera_pal01.py` e `out/genera_pal02.py` chiamano entrambi
    `fit_clip_scroll_to_notes()` dopo aver scritto le note -- serviva
    davvero, e senza questo controllo nessuno se ne accorge senza guardare
    lo schermo. Copre solo le clip CROMATICHE (`inKeyMode` diverso da '1'):
    dentro la modalita' a scala la stessa idea, applicata a
    `inKeyScrollOffset`, accusa 109 clip su 131 in modalita' a scala nel
    corpus fidato -- vedi il docstring della funzione per la misura e il
    perche' non e' coperta.
    """
    from . import song as S                               # import locale: ciclo

    return (S.same_section_conflicts(doc) + S.notes_beyond_clip_end(doc)
            + S.notes_hidden_by_scroll(doc))


# ------------------------------------------------------------------ il racconto

def _nome_strumento(strumento) -> str:
    """Il nome umano di uno strumento qualunque: mai un frammento di tag XML.

    [BUG capitolato, secondo sito] Il primo giro aveva corretto solo la riga
    che scriveva `f'<{strumento.tag}>'` in `racconta()`; `arranger.nome_di()`
    ha lo STESSO fallback (giustamente: li' serve per diagnostica, non e'
    stato toccato) e veniva chiamata da `racconta()` per l'arrangiamento. I
    nodi <cvChannel>/<midiChannel> del corpus non portano mai `name` ne'
    `presetName`, quindi quel fallback scattava sempre: `Bounce.XML` aveva
    19 righe con `<cvChannel>` letterale nel racconto.

    Qui si usa `midicv.label()` per MIDI/CV -- il nome che il dispositivo
    mostra davvero ('MIDI 14', 'CV 1') -- e `presetName`/`name` per il resto
    (sound, kit, audioTrack). Se anche quello manca, un'etichetta fra
    parentesi TONDE: mai angolari, per non far rientrare l'XML dal racconto.
    """
    from . import midicv as M                               # import locale: ciclo

    if M.kind(strumento) is not None:
        nome = M.label(strumento)
        if '<' not in nome:
            return nome
    return (strumento.get('presetName') or strumento.get('name')
            or f'({strumento.tag})')


def _nome_altezza_libero(midi: int) -> str:
    """Il nome di un'altezza qualunque, anche fuori dall'estensione MIDI 0-127.

    [BUG capitolato] `racconta_clip()` chiamava `nome_altezza()`, che e' un
    cancello apposta (task 1): rifiuta cio' che e' fuori 0-127. Ma le
    noteRow del corpus reale ci escono -- `Lfx.XML` arriva a `y=143`,
    `Piano.XML` scende a `y=-3` -- e qui il compito non e' convalidare la
    song, e' descrivere quello che c'e' davvero prima di correggerlo:
    un'altezza fuori estensione va raccontata per quello che e', non fatta
    esplodere in un'eccezione. Stessa formula di `nome_altezza()`, senza il
    controllo di range: `%` e `//` di Python restano corretti per i negativi.
    """
    return f'{CROMATICA_IT[midi % 12]}{midi // 12 - 1}'


def racconta_clip(doc, clip) -> str:
    """Una clip in termini musicali: il campione se e' audio, righe e note
    se e' di strumento, sempre con posizioni in battute."""
    from . import song as S                               # import locale: ciclo

    tpb = S.ticks_per_bar(doc.root)
    testa = (f'   clip {S.clip_label(clip)!r}: '
             f'{int(clip.get("length") or 0) / tpb:g} battute, '
             f'sezione {clip.get("section")}')

    if clip.tag == 'audioClip':
        # [BUG capitolato] la bozza non trattava le audioClip affatto: senza
        # noteRow finivano descritte "(vuota)" pur portando un campione.
        # Chi legge il racconto per decidere se riusare uno slot rischiava
        # di sovrascrivere un campione messo a mano dall'utente credendolo
        # libero -- esattamente cio' che "raccontare prima di toccare"
        # dovrebbe impedire.
        from . import audio as AU                           # import locale: ciclo
        if AU.is_empty(clip):
            return testa + ' (nessun campione impostato)'
        s = int(clip.get('startSamplePos') or 0)
        e = int(clip.get('endSamplePos') or 0)
        durata = (e - s) / 44100
        return f'{testa}: campione {clip.get("filePath")!r} (~{durata:.2f}s)'

    kit = S.is_kit_clip(clip)
    nomi = S.drum_names(doc, clip) if kit else []
    righe = []
    for r in S.note_rows(clip):
        note = S.read_notes(r)
        if not note:
            continue
        if kit:
            i = int(r.get('drumIndex') or -1)
            etichetta = nomi[i] if 0 <= i < len(nomi) else f'drum {i}'
        else:
            etichetta = _nome_altezza_libero(int(r.get('y')))
        quando = ', '.join(f'{n.pos / tpb + 1:g}' for n in note[:8])
        coda = '...' if len(note) > 8 else ''
        righe.append(f'      {etichetta:16} {len(note):2} note a battuta '
                     f'{quando}{coda}')
    return '\n'.join([testa] + righe) if righe else testa + ' (vuota)'


def racconta(doc) -> str:
    """L'intera song in termini musicali, senza una riga di XML.

    Va letta dopo ogni riscaricamento dal dispositivo: e' il modo di sapere
    cosa c'e' davvero prima di modificarlo, e cio' che permette all'utente di
    correggere a parole quello che e' stato fatto.
    """
    from . import song as S                               # import locale: ciclo
    from . import arranger as A                           # noqa: PLC0415
    from . import midicv as M                             # noqa: PLC0415
    from . import audio as AU                             # noqa: PLC0415

    tpb = S.ticks_per_bar(doc.root)
    fuori = [f'{S.get_bpm(doc.root):.0f} BPM, {S.scale_name(doc)}, '
             f'swing {S.get_swing(doc)[0]}']

    fuori.append('')
    fuori.append('strumenti e clip:')
    for strumento in S.instruments(doc):
        # [BUG capitolato] la bozza scriveva `f'<{strumento.tag}>'`, che
        # inietta letteralmente un frammento di tag XML nel racconto -- il
        # test lo vieta esplicitamente ('non contiene XML'). `_nome_strumento`
        # tiene il nome del tag come informazione ma senza angolari, e usa
        # `midicv.label()` per MIDI/CV, che non hanno mai name/presetName.
        fuori.append(f'   {strumento.tag}: {_nome_strumento(strumento)}')
        for _, clip in S.clips(doc):
            if S.instrument_of(doc, clip) is strumento:
                fuori.append(racconta_clip(doc, clip))

    ist = A.arrangement(doc)
    fuori.append('')
    if ist:
        fuori.append(f'arrangiamento ({len(ist)} blocchi):')
        for strumento, i, clip in ist:
            nome = _nome_strumento(strumento)
            # [BUG capitolato, secondo] la bozza ignorava `clip` (gia' in
            # mano) e stampava solo il nome dello strumento: con piu' clip
            # dello stesso strumento nell'arrangiamento -- 10 song su 34 nel
            # corpus, es. Aolac.XML/BassGuitar con 3 pattern distinti su una
            # quarantina di blocchi -- il racconto le rendeva indistinguibili.
            # La sezione (gia' stampata sopra per la stessa clip) basta a
            # dire QUALE pattern sta suonando in quel blocco.
            if clip is None:
                extra = ''
            elif A.is_white(clip):
                extra = ' [bianca]'
            else:
                extra = f' (sezione {clip.get("section")})'
            fuori.append(f'   battuta {i.pos / tpb + 1:g} per '
                         f'{i.length / tpb:g}: {nome}{extra}')
    else:
        fuori.append('arrangiamento: vuoto (le clip vivono solo in session view)')

    extra = M.describe(doc) + AU.describe(doc)
    if extra:
        fuori.append('')
        fuori += ['   ' + r for r in extra]
    return '\n'.join(fuori)


# ------------------------------------------------------------------ i verbi

#: Il centro della scala del display, dove `pan` e' centrato.
CENTRO = 25

#: Le parole verso i parametri, con lo spostamento in unita' del display
#: 0-50. `forza` (in `applica_verbo`) moltiplica questo passo.
#:
#: **Questa tabella e' gusto, non un fatto.** Nasce piccola e arbitraria, e
#: cresce dalle correzioni: quando l'utente dice «no, piu' scuro vuol dire
#: anche togliere risonanza», si aggiunge qui e si annota in docs/MUSICA.md.
#: Ogni applicazione riferisce cosa ha mosso, cosi' resta scavalcabile. Stessa
#: natura di `ARTICOLAZIONI` sopra: promossa a vocabolario esplicito invece
#: che nascosta in un default, perche' il proprietario del progetto ha detto
#: che questo genere di scelta dipende dal prompt.
#:
#: [REVISIONE] La prima versione aveva UNA SOLA tabella e infilava dentro
#: anche 'al centro' come `('pan', 0)`, con `passo == 0` interpretato da
#: `applica_verbo` come "vai al centro" invece che "nessuno spostamento". Il
#: revisore ha dimostrato la trappola eseguendo il codice: quel ramo ignorava
#: `forza` in silenzio (`forza=0` e `forza=-3` davano lo stesso salto a 25),
#: e chi avesse aggiunto un domani `('volume', 0)` pensando "nessuna
#: variazione" avrebbe preso invece un salto a 25 -- un valore che ha senso
#: solo per `pan`. Zero test coprivano quel ramo. Separare le due tabelle
#: toglie il significato doppio dal dato stesso, non da un commento: `passo`
#: in questa tabella vuol dire sempre e solo "sposta di tanto", mai "vai a
#: un punto fisso".
VERBI_RELATIVI: dict[str, tuple[str, int]] = {
    'piu scuro': ('lpfFrequency', -8),
    'piu chiuso': ('lpfFrequency', -8),
    'piu brillante': ('lpfFrequency', +8),
    'piu aperto': ('lpfFrequency', +8),
    'piu forte': ('volume', +5),
    'piu piano': ('volume', -5),
    'piu riverbero': ('reverbAmount', +8),
    'meno riverbero': ('reverbAmount', -8),
    'a sinistra': ('pan', -10),
    'a destra': ('pan', +10),
}

#: Le parole che portano un parametro a un valore FISSO, non a uno
#: spostamento: `forza` non li tocca (non c'e' un "quanto" da moltiplicare,
#: solo un "dove"). Tabella separata da `VERBI_RELATIVI` apposta, cosi' il
#: significato di ogni voce e' inequivocabile leggendo solo il nome della
#: tabella in cui sta, non un valore magico dentro l'altra.
VERBI_ASSOLUTI: dict[str, tuple[str, int]] = {
    'al centro': ('pan', CENTRO),
}


def verbi_disponibili() -> list[str]:
    """Tutti i verbi noti, relativi e assoluti insieme, in ordine alfabetico."""
    return sorted(set(VERBI_RELATIVI) | set(VERBI_ASSOLUTI))


def applica_verbo(doc, nodo, verbo: str, forza: int = 1) -> dict[str, object]:
    """Applica un verbo a una clip o a uno strumento, e dice cosa ha fatto.

    `doc` non e' usato nel corpo: resta in firma per uniformita' con le
    altre funzioni di uscita del modulo (`verifica(doc)`, `racconta(doc)`),
    che prendono sempre il documento anche quando operano su un nodo solo.

    Un verbo RELATIVO (`VERBI_RELATIVI`) sposta il parametro di `passo *
    forza`. Un verbo ASSOLUTO (`VERBI_ASSOLUTI`) lo porta a un valore fisso
    e ignora `forza` -- non c'e' "quanto", solo "dove". Il risultato riporta
    parametro, valore prima e valore dopo: senza quello l'utente non puo'
    correggere una scelta che e' di gusto (bastano quei due numeri per
    tornare indietro: `sound.set(nodo, esito['parametro'], esito['prima'])`).
    Il valore resta sempre nella scala del display, 0-50: la clausola
    `max(0, min(50, ...))` non e' un dettaglio, e' cio' che rende sicuro
    applicare lo stesso verbo piu' volte o con `forza` alta.
    """
    from . import sound as SN                             # import locale: ciclo

    chiave = verbo.strip().lower()
    if chiave in VERBI_RELATIVI:
        parametro, passo = VERBI_RELATIVI[chiave]
        prima = SN.get(nodo, parametro)
        if prima is None:
            raise ValueError(f'{parametro} non e impostabile su questo nodo '
                             f'(assente o automatizzato)')
        dopo = max(0, min(50, prima + passo * forza))
    elif chiave in VERBI_ASSOLUTI:
        parametro, valore = VERBI_ASSOLUTI[chiave]
        prima = SN.get(nodo, parametro)
        if prima is None:
            raise ValueError(f'{parametro} non e impostabile su questo nodo '
                             f'(assente o automatizzato)')
        dopo = max(0, min(50, valore))
    else:
        raise ValueError(f'{verbo!r} non e un verbo noto. Ci sono: '
                         f'{", ".join(verbi_disponibili())}')
    SN.set(nodo, parametro, dopo)
    return {'verbo': chiave, 'parametro': parametro,
            'prima': prima, 'dopo': dopo}


# ------------------------------------------------------------------ scrivere

def scrivi(doc, clip, note, dove=None) -> dict[str, object]:
    """Scrive note in una clip, senza che chi chiama sappia di che tipo e'.

    Prima questa cosa richiedeva di comporre tre primitive con un idioma
    DIVERSO per i due tipi di clip:

        synth   S.write_notes(S.add_note_row(clip, y), note, create=True)
        kit     S.write_notes(S.drum_row(doc, clip, nome), note, create=True)

    piu' `S.fit_clip_scroll_to_notes(doc, clip)` da ricordarsi in coda, pena
    note scritte e invisibili. Sbagliare quale dei due valeva e' il primo
    difetto trovato dalla prova d'accettazione, e SKILL.md lo insegnava in
    tre righe separate: tre occasioni di prendere quella sbagliata.

    Non serve dichiarare il caso, perche' LA FORMA DELLE NOTE lo dice gia':
    `melodia()` e `accordi()` tornano `altezza -> note`, perche' il Deluge
    tiene le note in righe una per altezza; `passi()` torna una lista, perche'
    un drum e' una riga sola.

        dict            una riga per altezza          solo clip di synth
        lista + dove    quella riga                   drum (kit) o altezza (synth)

    Su una clip di synth chiude con `fit_clip_scroll_to_notes()`, che e' cio'
    che impedisce alle note di restare scritte e fuori dalla finestra visibile.
    Su un kit non serve: le righe sono i drum, non le altezze.
    """
    from . import song as S                                 # import locale: ciclo

    e_kit = S.is_kit_clip(clip)

    if isinstance(note, dict):
        if e_kit:
            raise ValueError(
                f'"{S.clip_label(clip)}" e una clip di kit: le sue righe sono '
                'drum, non altezze. melodia() e accordi() non hanno senso qui '
                '-- usa passi() e dove=<nome del drum>')
        righe = 0
        quante = 0
        for y, ns in sorted(note.items()):
            S.write_notes(S.note_row(clip, y, create=True), ns, create=True)
            righe += 1
            quante += len(ns)
        esito = {'clip': S.clip_label(clip), 'righe': righe, 'note': quante}
        esito['scroll'] = S.fit_clip_scroll_to_notes(doc, clip)
        return esito

    if dove is None:
        raise ValueError(
            'una lista di note va su UNA riga, ma non e detto quale: passa '
            + ('dove=<nome del drum>' if e_kit else "dove=<altezza, es. 're2'>"))

    if e_kit:
        riga = S.drum_row(doc, clip, dove, create=True)
        S.write_notes(riga, note, create=True)
        # anche un kit ha la sua finestra: le righe sono i drum, e ne stanno
        # a schermo otto. Senza questo, un drum oltre l'ottavo si scrive e
        # non si vede -- visto sul dispositivo con il rim all'indice 13
        return {'clip': S.clip_label(clip), 'righe': 1, 'note': len(note),
                'drum': dove, 'scroll': S.fit_clip_scroll_to_notes(doc, clip)}

    y = altezza(dove) if isinstance(dove, str) else int(dove)
    S.write_notes(S.note_row(clip, y, create=True), note, create=True)
    esito = {'clip': S.clip_label(clip), 'righe': 1, 'note': len(note),
             'altezza': y}
    esito['scroll'] = S.fit_clip_scroll_to_notes(doc, clip)
    return esito


# ------------------------------------------------------------------ trasformare

def _grado_e_scarto(y: int, root: int, intervalli) -> tuple[int, int]:
    """(grado assoluto, scarto cromatico) di un'altezza dentro una scala.

    Il grado assoluto conta i gradi da sempre, ottave comprese, cosi' salire
    di N gradi e' una somma sola. Lo SCARTO e' quanti semitoni la nota sta
    sopra il suo grado: vale 0 per le note in scala e 1 o 2 per le altre, ed
    e' il numero che permette di trasporre una nota fuori scala senza
    schiacciarla dentro.
    """
    pc = (y - root) % 12
    ottava = (y - root) // 12
    grado = max(i for i, m in enumerate(intervalli) if m <= pc)
    return ottava * len(intervalli) + grado, pc - intervalli[grado]


def _per_gradi(y: int, root: int, intervalli, gradi: int) -> int:
    """L'altezza `y` spostata di `gradi` dentro la scala, scarto conservato."""
    assoluto, scarto = _grado_e_scarto(y, root, intervalli)
    ottava, grado = divmod(assoluto + gradi, len(intervalli))
    return root + ottava * 12 + intervalli[grado] + scarto


def _mappa_altezze(doc, clip, semitoni, gradi) -> dict[int, int]:
    from . import song as S                                 # import locale: ciclo

    ys = [int(r.get('y')) for r in S.note_rows(clip) if r.has('y')]
    if semitoni is not None:
        return {y: y + semitoni for y in ys}
    root, intervalli = S.get_scale(doc)
    if not intervalli:
        raise ValueError('questa song non dichiara una scala, quindi non ha '
                         'gradi: usare semitoni=')
    return {y: _per_gradi(y, root, intervalli, gradi) for y in ys}


def trasponi(doc, bersaglio, semitoni: int | None = None,
             gradi: int | None = None) -> dict[str, object]:
    """Trasporta un bersaglio, in semitoni oppure per gradi di scala.

    `semitoni=12` alza di un'ottava, sempre e ovunque. `gradi=2` sale di due
    gradi DENTRO la scala della song -- che e' una proprieta' della song e non
    della clip -- quindi una terza resta in tonalita' invece di essere un
    numero fisso di semitoni.

    Il bersaglio si riconosce per identita', come in `togli()`: strumento,
    clip o `noteRow`.

    **Su un synth si muovono le righe**, perche' le righe SONO le altezze. Le
    note fuori scala conservano il loro scarto dal grado: una nota un semitono
    sopra il terzo grado resta un semitono sopra il NUOVO terzo grado.
    `snap_to_scale()` qui sarebbe sbagliata -- schiaccerebbe in scala le note
    che il corpus dice di rispettare (FINDINGS §6, Progsong ne ha 315).

    **Su un kit si muove il suono**, non il `drumIndex`: `transpose` sugli
    oscillatori del drum, che il manuale documenta come «Semitones + cents for
    adjustment». Questo cambia lo STRUMENTO, quindi tutte le clip di quel kit:
    il rapporto lo dichiara in `condiviso`. E un drum non ha gradi di scala,
    quindi `gradi=` su un kit e' un errore.
    """
    from . import kit as K                                  # import locale: ciclo
    from . import song as S                                 # import locale: ciclo

    if (semitoni is None) == (gradi is None):
        raise ValueError('serve semitoni= OPPURE gradi=: senza nessuno dei due '
                         'non c e niente da fare, con tutti e due non si sa '
                         'quale vince')

    def kit_di(nodo, condiviso):
        if gradi is not None:
            raise ValueError(
                'un drum non ha gradi di scala: su un kit vale solo '
                'semitoni=. Per intonarlo di una terza, dire se maggiore '
                '(4 semitoni) o minore (3)')
        esito = K.transpose(nodo, semitoni)
        return {'semitoni': semitoni, 'condiviso': condiviso, **esito}

    # --- uno strumento
    if any(i is bersaglio for i in S.instruments(doc)):
        if bersaglio.tag == 'kit':
            return kit_di(bersaglio, True)
        esito = {'semitoni': semitoni, 'gradi': gradi, 'righe': 0,
                 'fuse': 0, 'note_perse': 0, 'clip': 0}
        for _, c in S.clips(doc):
            if S.instrument_of(doc, c) is not bersaglio:
                continue
            r = trasponi(doc, c, semitoni=semitoni, gradi=gradi)
            esito['clip'] += 1
            for k in ('righe', 'fuse', 'note_perse'):
                esito[k] += r.get(k, 0)
        return esito

    # --- una clip
    from . import arranger as A                             # import locale: ciclo
    if A.index_of(doc, bersaglio) is not None:
        if S.is_kit_clip(bersaglio):
            kit = S.instrument_of(doc, bersaglio)
            if kit is None:
                raise ValueError(f'il kit di "{S.clip_label(bersaglio)}" non si '
                                 'trova fra gli strumenti della song')
            return kit_di(kit, True)
        esito = S.retune_rows(bersaglio,
                              _mappa_altezze(doc, bersaglio, semitoni, gradi))
        esito.update({'semitoni': semitoni, 'gradi': gradi,
                      'scroll': S.fit_clip_scroll_to_notes(doc, bersaglio)})
        return esito

    # --- una riga
    if bersaglio.tag == 'noteRow':
        clip = _clip_della_riga(doc, bersaglio)
        if clip is None:
            raise ValueError('questa noteRow non sta in nessuna clip della song')
        if S.is_kit_clip(clip):
            kit = S.instrument_of(doc, clip)
            i = int(bersaglio.get('drumIndex'))
            if gradi is not None:
                raise ValueError('un drum non ha gradi di scala: usare semitoni=')
            esito = K.transpose_drum(S.drums(kit)[i], semitoni)
            return {'semitoni': semitoni, 'condiviso': True, 'drum': 1,
                    'mosso': esito}
        y = int(bersaglio.get('y'))
        nuova = (y + semitoni if semitoni is not None
                 else _per_gradi(y, *S.get_scale(doc), gradi))
        esito = S.retune_rows(clip, {y: nuova})
        esito.update({'semitoni': semitoni, 'gradi': gradi,
                      'scroll': S.fit_clip_scroll_to_notes(doc, clip)})
        return esito

    raise ValueError(
        f'<{bersaglio.tag}> non e qualcosa che si possa trasporre: si '
        'trasportano strumenti, clip e noteRow')


# --------------------------------------------------- trasformare: il tempo

def _clip_o_no(doc, clip, verbo: str):
    """Le operazioni sul tempo prendono una clip, e lo dicono se non e' una."""
    from . import arranger as A                             # import locale: ciclo

    if A.index_of(doc, clip) is None:
        raise ValueError(f'{verbo}() lavora su una clip, e <{clip.tag}> non lo '
                         'e. Per uno strumento intero, chiamarla su ognuna '
                         'delle sue clip')
    return int(clip.get('length'))


def sposta(doc, clip, tick: int | None = None,
           battute: float | None = None) -> dict[str, object]:
    """Trasla le note nel tempo. La clip resta lunga uguale.

    `battute` passa da `ticks_per_bar()`, quindi segue la RESOLUTION della
    song invece di un numero fisso.

    Prima del tick 0 non c'e' posto: spostare troppo indietro viene RIFIUTATO
    e l'errore dice quanto spazio c'e' davvero. Scartare le note che escono
    sarebbe perdere musica in silenzio, che e' la cosa peggiore fra quelle
    possibili -- e chi chiama non avrebbe modo di accorgersene.

    Le note che finiscono oltre la fine della clip restano invece dove sono:
    il dispositivo le conserva e non le suona, e lo segnala `avvertenze()`.
    """
    from dataclasses import replace                         # noqa: PLC0415
    from . import song as S                                 # import locale: ciclo

    _clip_o_no(doc, clip, 'sposta')
    if (tick is None) == (battute is None):
        raise ValueError('serve tick= OPPURE battute=, non nessuno e non entrambi')
    if battute is not None:
        tick = int(round(battute * S.ticks_per_bar(doc.root)))

    primo = S.first_note_pos(clip)
    if primo is not None and primo + tick < 0:
        raise ValueError(
            f'spostare di {tick} tick porterebbe una nota a {primo + tick}, '
            f'prima dell inizio della clip. Indietro c e spazio per {primo} '
            'tick')
    quante = S.map_notes(clip, lambda n: replace(n, pos=n.pos + tick))
    return {'tick': tick, 'note': quante}


def repeat(doc, clip, volte: int) -> dict[str, object]:
    """La clip diventa `volte` piu' lunga e il materiale si ripete.

    Le durate delle note NON cambiano: e' l'operazione che allunga una
    sezione senza riscriverla, non quella che cambia il rate.

    Una riga con una LUNGHEZZA PROPRIA (poliritmo) si ripete sul proprio
    ciclo, non su quello della clip, e la sua lunghezza viene moltiplicata
    come quella della clip. Senza, il poliritmo si romperebbe in silenzio.
    Nel corpus c1.3.0 ne esiste un solo esemplare, `Qbix.XML`.
    """
    from dataclasses import replace                         # noqa: PLC0415
    from . import song as S                                 # import locale: ciclo

    lung = _clip_o_no(doc, clip, 'repeat')
    if int(volte) != volte or volte < 2:
        raise ValueError(f'repeat() vuole un numero intero di volte, almeno 2, '
                         f'non {volte!r}')
    volte = int(volte)

    quante = 0
    for r in S.note_rows(clip):
        propria = int(r.get('length')) if r.has('length') else None
        note = S.read_notes(r)
        if note:
            ciclo = propria or lung
            S.write_notes(r, [replace(n, pos=n.pos + k * ciclo)
                              for k in range(volte) for n in note], create=True)
            quante += len(note) * volte
        if propria is not None:
            r.set('length', str(propria * volte))

    S.set_clip_length(clip, lung * volte)
    return {'volte': volte, 'lunghezza': lung * volte, 'note': quante}


def stretch(doc, clip, fattore: float) -> dict[str, object]:
    """Scala il tempo: note E lunghezza della clip, insieme.

    Il materiale resta identico, cambia solo il rate — `stretch(0.5)` lo fa
    suonare al doppio della velocita' in meta' spazio. E' la primitiva su cui
    poggiano `double_time()` e `half_time()`.
    """
    from dataclasses import replace                         # noqa: PLC0415
    from . import song as S                                 # import locale: ciclo

    lung = _clip_o_no(doc, clip, 'stretch')
    if fattore <= 0:
        raise ValueError(f'fattore {fattore!r}: deve essere positivo')

    quante = S.map_notes(clip, lambda n: replace(
        n, pos=int(round(n.pos * fattore)),
        length=max(1, int(round(n.length * fattore)))))
    for r in S.note_rows(clip):
        if r.has('length'):
            r.set('length', str(max(1, int(round(int(r.get('length'))
                                                 * fattore)))))
    nuova = max(1, int(round(lung * fattore)))
    S.set_clip_length(clip, nuova)
    return {'fattore': fattore, 'lunghezza': nuova, 'note': quante}


def double_time(doc, clip) -> dict[str, object]:
    """Il materiale al doppio della velocita', nella STESSA lunghezza.

    Otto ottavi diventano sedici sedicesimi: si comprime e si ripete due volte
    per riempire la battuta. E' quello che si intende dicendo «raddoppia» o
    «piu' veloce» davanti a un pattern.
    """
    lung = _clip_o_no(doc, clip, 'double_time')
    stretch(doc, clip, 0.5)
    esito = repeat(doc, clip, 2)
    return {'lunghezza': esito['lunghezza'], 'note': esito['note'],
            'invariata': esito['lunghezza'] == lung}


def half_time(doc, clip) -> dict[str, object]:
    """Il materiale a meta' velocita'. La clip RADDOPPIA.

    Otto ottavi diventano otto quarti, e non ci stanno piu' in una battuta:
    in meta' tempo un pattern di una battuta ne occupa due davvero. L'asimmetria
    con `double_time()` non e' una svista, e' quello che fa un musicista.
    """
    return stretch(doc, clip, 2)


# ------------------------------------------------------------------ togliere

def _clip_della_riga(doc, riga):
    """La clip che contiene questa noteRow, per identita'."""
    from . import song as S                                 # import locale: ciclo

    for _, clip in S.clips(doc):
        if any(r is riga for r in S.note_rows(clip)):
            return clip
    return None


def togli(doc, bersaglio, quando=None) -> dict[str, object]:
    """Toglie qualcosa dalla song, riconoscendo da se' cosa gli e' stato dato.

    Meta' di quello che una persona dice davanti a una song e' sottrattivo --
    «togli il piano», «leva quel pattern nella seconda meta'», «il basso non
    ci va» -- e fino a qui la libreria sapeva solo aggiungere e sostituire.

    Il bersaglio si riconosce per IDENTITA', non per tag: appartiene alla
    lista degli strumenti, o a quella delle clip, oppure e' una `noteRow`.
    Andare per tag sarebbe una tabella in piu' da tenere aggiornata, e nel
    corpus convivono gia' `<midi>` e `<midiChannel>`.

        strumento                 le sue clip, poi lui
        strumento + quando=(a,b)  solo le istanze d'arranger in quel tratto
        clip                      la clip, e i clipCode che la seguivano
        noteRow di kit            SVUOTATA: una riga per drum deve esserci
        noteRow di synth          tolta

    `quando` distingue «togli il basso» da «leva il basso nella seconda
    meta'»: nel secondo caso lo strumento e la clip restano, sparisce solo
    quel tratto della linea del tempo. Darlo insieme a una clip e' un errore
    e non un silenzio, perche' vorrebbe dire una cosa che non si puo' fare:
    una clip non ha posizioni nel tempo, le hanno le sue istanze.

    Ritorna il rapporto di cio' che ha mosso, come `applica_verbo`.
    """
    from . import arranger as A                             # import locale: ciclo
    from . import song as S                                 # import locale: ciclo

    if any(i is bersaglio for i in S.instruments(doc)):
        if quando is not None:
            da, a = quando
            return A.remove_instances_in(bersaglio, da, a)
        return S.remove_instrument(doc, bersaglio)

    if quando is not None:
        raise ValueError(
            'quando= vale solo su uno strumento, che ha una linea del tempo. '
            'Una clip non ha posizioni: le hanno le istanze che la piazzano')

    if A.index_of(doc, bersaglio) is not None:
        return S.remove_clip(doc, bersaglio)

    if bersaglio.tag == 'noteRow':
        clip = _clip_della_riga(doc, bersaglio)
        if clip is None:
            raise ValueError('questa noteRow non sta in nessuna clip della song')
        if S.is_kit_clip(clip):
            # una riga per drum deve esserci sempre: si svuota, non si toglie
            quante = len(S.read_notes(bersaglio))
            S.write_notes(bersaglio, [])
            return {'clip': S.clip_label(clip), 'riga': 'svuotata',
                    'drumIndex': bersaglio.get('drumIndex'), 'note': quante}
        return S.remove_note_row(clip, bersaglio)

    raise ValueError(
        f'<{bersaglio.tag}> non e qualcosa che si possa togliere: si tolgono '
        'strumenti, clip e noteRow. Per un parametro di suono usa '
        'applica_verbo(), per un drum dal kit usa kit.remove_drum()')


# ------------------------------------------------------------------ la destinazione sulla SD

#: Le QUATTRO cartelle di primo livello in cui Deluge Pal puo' scrivere,
#: sempre dentro la propria sottocartella (vedi SOTTOCARTELLA). Le song, i
#: kit e i campioni dell'utente stanno alla radice di queste stesse
#: cartelle e non vanno toccati: mescolarci i file generati e' gia' costato
#: una pulizia di 34 file a mano, sparsi fra le 135 song personali.
CARTELLE_SD = ('SONGS', 'KITS', 'SYNTHS', 'SAMPLES')

#: Il nome della sottocartella dedicata, identico nelle quattro cartelle.
#: Esiste gia' sulla SD in tutte e quattro (creata a mano): `dsysex` non ha
#: un comando per crearne una nuova via SysEx, quindi se ne servisse una
#: destinazione diversa da queste quattro andrebbe preparata spostando la
#: SD, non generata al volo dal codice.
SOTTOCARTELLA = 'DelugePal'

#: L'estensione dipende dal TIPO di contenuto della cartella, non e' sempre
#: .XML: SAMPLES contiene campioni audio (.wav); le altre tre, file XML del
#: formato Deluge. Scriverebbe un file che il dispositivo non riconosce
#: forzare .XML su un campione.
_ESTENSIONE = {
    'SONGS': '.XML',
    'KITS': '.XML',
    'SYNTHS': '.XML',
    'SAMPLES': '.wav',
}

#: Sottostringhe che farebbero uscire un nome dalla propria sottocartella.
#: Un nome che le contiene va RIFIUTATO, non ripulito in silenzio: ripulirlo
#: nasconderebbe un errore di chi chiama invece di segnalarlo.
_VIETATI = ('/', '\\', '..')

#: Caratteri singoli che FAT32/Windows non ammettono in un nome di file,
#: oltre ai separatori gia' in _VIETATI. Non aggirano il confine (il file
#: resta comunque dentro SOTTOCARTELLA), ma un nome che li contiene e' un
#: nome che il Deluge rifiutera' comunque -- solo piu' tardi, con un errore
#: meno leggibile e in un punto dove risalire alla causa e' piu' difficile.
#: Rifiutarlo qui, presto, e' lo stesso principio gia' applicato ai
#: separatori: non rimandare al dispositivo un problema nostro.
_CARATTERI_VIETATI = frozenset('<>:"|?*')

#: Le estensioni che il progetto CONOSCE: quella che il Deluge scrive
#: (.XML) e i formati audio che potrebbero arrivare come campione. Un
#: insieme DICHIARATO, non una regola sintattica indovinata.
#:
#: [REVISIONE] La prima versione (`_estensione_sospetta`, rimossa)
#: trattava come estensione QUALUNQUE suffisso di 1-4 alfanumerici con
#: almeno una lettera. Il revisore ha dimostrato che rifiutava a torto nomi
#: legittimi come 'Drum.V2', 'Bass.HD', 'Song.Live', 'Kick.Pro' -- nessuno
#: dei quali e' un'estensione di niente -- con un messaggio che affermava
#: il falso ("porta gia' l'estensione '.V2'"). Un insieme dichiarato non ha
#: questo problema per costruzione: se il suffisso non e' uno di QUESTI,
#: il punto fa parte del nome e non riguarda questa funzione. E' anche piu'
#: leggibile: chi vuole accettare un formato nuovo lo aggiunge qui, in un
#: punto solo, invece di ragionare su una regex.
_ESTENSIONI_NOTE = ('.XML', '.wav', '.aif', '.aiff', '.mp3', '.flac', '.ogg')


def _estensione_nota(testo: str) -> str | None:
    """Il suffisso di `testo` se e' una fra `_ESTENSIONI_NOTE`, altrimenti None.

    Confronto senza distinguere maiuscole/minuscole (`'.WAV'` conta come
    `'.wav'`), ma il valore restituito conserva il case originale del
    nome, per poterlo togliere con precisione.
    """
    basso = testo.lower()
    for ext in _ESTENSIONI_NOTE:
        if basso.endswith(ext.lower()):
            return testo[-len(ext):]
    return None


#: La versione occupa sempre due cifre (01..99): e' cosi' che compare nel
#: nome finale. Oltre 99 non c'e' un modo a due cifre di rappresentarla.
_VERSIONE_MIN = 1
_VERSIONE_MAX = 99


def destinazione(nome: str, versione: int | None = 1,
                 cartella: str = 'SONGS') -> str:
    """Il percorso remoto per SCRIVERE un file generato, sempre dentro la
    sottocartella dedicata della cartella scelta: `destinazione('house', 1)`
    da' `/SONGS/DelugePal/HOUSE01.XML`, `destinazione('kick', cartella=
    'SAMPLES')` da' `/SAMPLES/DelugePal/kick01.wav`.

    `dsysex put` non sovrascrive mai, quindi ogni iterazione del ciclo sale
    con la versione successiva. Elencare la cartella remota non e' un modo
    affidabile di scoprire la versione libera: il comando `dir` puo' smettere
    di rispondere pur con tutto il resto del canale funzionante (osservato,
    docs/SYSEX.md §4-bis). Meglio provare la versione 1 e incrementare finche'
    `put` accetta.

    Scrive SEMPRE e SOLO dentro `<cartella>/SOTTOCARTELLA`, per una delle
    QUATTRO `cartella` in `CARTELLE_SD`: un'altra viene RIFIUTATA, dicendo
    quali esistono. Nessun argomento puo' far uscire il percorso da li'. Un
    `nome` che contiene '/', '..' o '\\' viene RIFIUTATO, non ripulito --
    ripulirlo nasconderebbe un errore di chi chiama. Lo stesso vale per i
    caratteri che FAT32/Windows non ammettono in un nome di file (`<>:"|?*`)
    e per i caratteri di controllo (codepoint sotto 32, NUL compreso):
    nessuno di questi esce dalla sottocartella, ma un nome cosi' fatto e' un
    nome che il Deluge rifiutera' comunque -- solo piu' tardi, con un errore
    meno leggibile. Meglio dirlo subito.

    L'estensione dipende dalla cartella (vedi `_ESTENSIONE`) e la sceglie
    SEMPRE questa funzione, mai chi chiama: `.XML` per song/kit/synth,
    `.wav` per i campioni. Solo le cartelle XML normalizzano il nome in
    maiuscolo -- e' cosi' che il dispositivo mostra le song; un campione
    invece mantiene il case dato, perche' i file `.wav` reali del corpus
    hanno case misto (`REC00133.WAV` accanto ad `AUDIO1_000.wav`) e non c'e'
    una convenzione unica da imporre. Se `nome` finisce per una delle
    `_ESTENSIONI_NOTE` (un insieme DICHIARATO, non una forma sintattica
    indovinata -- vedi `_estensione_nota`) che COINCIDE con quella attesa,
    viene tolta prima di riaggiungerla (cosi' `'house.xml'` non raddoppia
    in `'HOUSE01.XML.XML'`); se ne porta una DIVERSA (`'kick.mp3'` per
    `SAMPLES`, che vuole `.wav`) viene RIFIUTATA invece di produrre un
    doppio suffisso silenzioso come `'kick.mp301.wav'` -- stessa disciplina
    degli altri controlli di questa funzione: un errore nostro si segnala,
    non si nasconde componendolo comunque. Un nome che finisce per
    qualcos'altro (`'Drum.V2'`, `'Song.Live'`, un numero di versione come
    `'Kit v2.1'`) non e' toccato: quel punto fa parte del nome, non e'
    un'estensione, e rifiutarlo sarebbe un falso positivo.

    `versione` ha senso per un ciclo che genera `HOUSE01`, `HOUSE02`, ...;
    meno per un kit o un synth che di solito si chiama col proprio nome e
    basta. `versione=None` non aggiunge alcun suffisso.
    """
    if cartella not in CARTELLE_SD:
        raise ValueError(
            f'cartella {cartella!r} sconosciuta, ci sono: '
            f'{", ".join(CARTELLE_SD)}')

    grezzo = nome.strip()
    if not grezzo:
        raise ValueError('il nome non puo essere vuoto')
    for vietato in _VIETATI:
        if vietato in grezzo:
            raise ValueError(
                f'{nome!r}: non puo contenere {vietato!r} '
                f'(uscirebbe da /{cartella}/{SOTTOCARTELLA})')
    for c in grezzo:
        if c in _CARATTERI_VIETATI or ord(c) < 32:
            raise ValueError(
                f'{nome!r}: contiene {c!r} (codepoint {ord(c)}), non '
                f'ammesso in un nome di file FAT32/Windows')

    estensione = _ESTENSIONE[cartella]
    base = grezzo
    trovata = _estensione_nota(base)
    if trovata is not None:
        if trovata.lower() == estensione.lower():
            base = base[:-len(trovata)]
        else:
            raise ValueError(
                f'{nome!r}: porta gia l estensione {trovata!r}, ma '
                f'{cartella!r} usa sempre {estensione!r} -- destinazione() '
                f'la aggiunge da sola: passare il nome senza estensione, o '
                f'con quella giusta')
    if estensione == '.XML':
        base = base.upper()
    if not base:
        raise ValueError(
            f'{nome!r}: senza l estensione non resta nessun nome')

    if versione is None:
        suffisso = ''
    else:
        if not _VERSIONE_MIN <= versione <= _VERSIONE_MAX:
            raise ValueError(
                f'versione {versione} fuori da {_VERSIONE_MIN}-{_VERSIONE_MAX} '
                f'(compare sempre come due cifre)')
        suffisso = f'{versione:02d}'

    return f'/{cartella}/{SOTTOCARTELLA}/{base}{suffisso}{estensione}'


def origine(nome: str, cartella: str = 'SONGS') -> str:
    """Il percorso per LEGGERE un file qualunque della SD -- non solo dentro
    `CARTELLE_SD`, non solo dentro `SOTTOCARTELLA`: ovunque.

    Non e' il simmetrico di `destinazione()`, ed e' voluto, non una
    dimenticanza. `destinazione()` blocca la SCRITTURA fuori dalla propria
    sottocartella perche' scriverci fuori e' quanto e' gia' costato la
    pulizia a mano di 34 file sparsi fra le 135 song personali dell'utente:
    la scrittura altera lo stato della SD, e un errore li' si paga con del
    lavoro perso. La LETTURA non condivide quel rischio -- leggere un file
    non lo modifica -- e anzi restringerla allo stesso modo sarebbe un
    difetto nella direzione OPPOSTA: Deluge Pal deve poter partire da
    qualunque song, kit o campione GIA' esistente dell'utente ("fammi una
    variazione di questa mia song", "usa il rullante di quel kit"). Per
    questo qui non si controlla ne' `cartella` (puo' essere una qualunque
    della SD, comprese sottocartelle come `SAMPLES/DRUMS/Kick`, non solo le
    quattro di `CARTELLE_SD`) ne' `nome` (puo' contenere una sua propria
    sottostruttura, come i campioni annidati nel corpus reale). L'unico
    controllo e' che nessuno dei due sia vuoto: un percorso vuoto non e' un
    percorso.
    """
    cartella_pulita = cartella.strip().strip('/')
    if not cartella_pulita:
        raise ValueError('la cartella non puo essere vuota')
    nome_pulito = nome.strip()
    if not nome_pulito:
        raise ValueError('il nome non puo essere vuoto')
    return f'/{cartella_pulita}/{nome_pulito}'
