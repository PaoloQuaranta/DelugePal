"""MIDI e CV: gli strumenti che il Deluge non suona ma comanda.

Sono l'angolo piu' semplice del formato, e per una ragione strutturale: non
c'e' nessun suono da descrivere. `<midiChannel>` e `<cvChannel>` sono nodi
**senza figli**, solo attributi — niente `<soundSources>`, niente
`<defaultParams>`, niente patch cable. Tutto il peso sta sulla clip, che porta
le note e basta.

    <midiChannel channel="13" suffix="-1" isArmedForRecording="0" />
    <cvChannel channel="0" defaultVelocity="100" activeModFunction="1" />

Nel corpus: 94 strumenti MIDI in 44 song e 9 CV in 7 song; 144 clip MIDI e 12
CV.

IL CANALE
---------
MIDI: `channel` 0-15 nel file, che sul display sono i canali **1-16**. Il
manuale, capitolo MIDI, parla di un intervallo di 16 canali.

CV: `channel` 0 e 1, cioe' le **due uscite** CV OUTPUT 1 e 2 del pannello. Dal
manuale i gate 1-2 si appaiano automaticamente alle CV 1-2.

IL SUFFIX, che non e' un dettaglio
----------------------------------
Dal manuale, capitolo MIDI: se si vuole che piu' di una clip esca sullo stesso
canale MIDI **simultaneamente**, le clip in piu' prendono un suffisso dopo il
numero di canale — `2A`, `2B` e cosi' via — e questo le fa trattare come
strumenti distinti pur uscendo sullo stesso canale.

Quindi `suffix="-1"` (93 casi su 94) vuol dire "nessun suffisso". Due strumenti
MIDI con lo STESSO canale e lo STESSO suffisso non sono due strumenti: sono un
conflitto, ed e' la stessa famiglia di `song.same_section_conflicts()` — roba
che esiste nel file e non puo' suonare insieme. Vedi `check()`.

[OSS] Che `suffix=0` corrisponda ad "A" e' dedotto dall'esempio del manuale:
nel corpus c'e' un solo esemplare diverso da -1, e vale 0.

CV2
---
`cv2Source` sceglie cosa esce dalla seconda uscita CV. Dal sorgente
(`cv_instrument.cpp`), che serializza `static_cast<int32_t>(cvmode[1])`:

    0 = off   1 = pitch   2 = mod   3 = aftertouch   4 = velocity

[OSS] L'enum viene da una sola lettura del sorgente e non e' stato verificato
sul dispositivo. Nel corpus compare solo il valore 1, in 6 strumenti su 9.

MPE
---
Il firmware accetta anche zone MPE al posto di un canale, con un tag `<zone>`
che vale `lower` o `upper` (`midi_instrument.cpp`):

    if (!strcmp(text, "lower")) setChannel(MIDI_CHANNEL_MPE_LOWER_ZONE);

Nel corpus non ce n'e' nessuno — tutti e 94 gli strumenti MIDI hanno un canale
0-15 — quindi qui non si scrive, e `check()` si limita a non ostacolarlo.
"""
from __future__ import annotations

from .parser import Document, Node

MIDI_CANALI = 16                 # 0-15 nel file, 1-16 sul display
CV_CANALI = 2                    # le due uscite del pannello
SENZA_SUFFIX = -1

TAG = {'midi': 'midiChannel', 'cv': 'cvChannel'}
ATTR_CLIP = {'midi': 'midiChannel', 'cv': 'cvChannel'}

#: Cosa esce dalla seconda uscita CV. Dal sorgente, non verificato.
CV2_SORGENTI = {0: 'off', 1: 'pitch', 2: 'mod', 3: 'aftertouch',
                4: 'velocity'}

#: Attributi d'istanza, dai valori osservati sugli strumenti scritti dal
#: dispositivo. `activeModFunction` differisce fra i due tipi: 0 sul MIDI
#: (81 casi su 84) e 1 sul CV (9 su 9).
ISTANZA_MIDI = {
    'suffix': str(SENZA_SUFFIX),
    'isArmedForRecording': '0',
    'defaultVelocity': '100',
    'activeModFunction': '0',
}
ISTANZA_CV = {
    'defaultVelocity': '100',
    'isArmedForRecording': '0',
    'activeModFunction': '1',
    'colour': '0',
}


#: L'<arpeggiator> di una clip MIDI/CV, catturato da `Bounce.XML` (c1.3.0).
#: Nel c1.3.0 le clip MIDI/CV lo portano tutte e 10 su 10, e non nascendo da
#: un preset non c'e' da dove copiarlo a tempo di esecuzione: sta qui come
#: CLIP_BASE sta in create.py.
#:
#: `bendRange` e `bendRangeMPE` sono nodi di solo testo, 9 clip su 10 a
#: c1.3.0, con questi valori.
BEND_RANGE = ('12', '48')
ARPEGGIATOR_BASE = {
    'mode': 'off',
    'syncLevel': '7',
    'numOctaves': '2',
    'syncType': '0',
    'arpMode': 'off',
    'chordType': '0',
    'noteMode': 'up',
    'octaveMode': 'up',
    'mpeVelocity': 'off',
    'stepRepeat': '1',
    'randomizerLock': '0',
    'kitArp': '1',
    'lastLockedNoteProb': '0',
    'lockedNoteProbArray': '00000000000000000000000000000000',
    'lastLockedBassProb': '0',
    'lockedBassProbArray': '00000000000000000000000000000000',
    'lastLockedSwapProb': '0',
    'lockedSwapProbArray': '00000000000000000000000000000000',
    'lastLockedGlideProb': '0',
    'lockedGlideProbArray': '00000000000000000000000000000000',
    'lastLockedReverseProb': '0',
    'lockedReverseProbArray': '00000000000000000000000000000000',
    'lastLockedChordProb': '0',
    'lockedChordProbArray': '00000000000000000000000000000000',
    'lastLockedRatchetProb': '0',
    'lockedRatchetProbArray': '00000000000000000000000000000000',
    'lastLockedVelocitySpread': '0',
    'lockedVelocitySpreadArray': '00000000000000000000000000000000',
    'lastLockedGateSpread': '0',
    'lockedGateSpreadArray': '00000000000000000000000000000000',
    'lastLockedOctaveSpread': '0',
    'lockedOctaveSpreadArray': '00000000000000000000000000000000',
    'notePattern': '00000102020306060502010703070D0E',
    'gate': '0',
    'rate': '0',
    'noteProbability': '-1',
    'bassProbability': '0',
    'swapProbability': '0',
    'glideProbability': '0',
    'reverseProbability': '0',
    'chordProbability': '0',
    'ratchetProbability': '0',
    'ratchetAmount': '0',
    'sequenceLength': '0',
    'chordPolyphony': '0',
    'rhythm': '0',
    'spreadVelocity': '0',
    'spreadGate': '0',
    'spreadOctave': '0',
}


def tracks(doc: Document, tipo: str | None = None) -> list[Node]:
    """Gli strumenti MIDI e/o CV della song, nell'ordine del file."""
    from . import song as S                               # import locale: ciclo

    voluti = (TAG[tipo],) if tipo else tuple(TAG.values())
    return [i for i in S.instruments(doc) if i.tag in voluti]


def kind(inst: Node) -> str | None:
    for k, tag in TAG.items():
        if inst.tag == tag:
            return k
    return None


def channel_of(inst: Node) -> int | None:
    v = inst.get('channel')
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def label(inst: Node) -> str:
    """Come il dispositivo lo chiama: `MIDI 14`, `MIDI 3A`, `CV 1`.

    I canali sono 0-based nel file e 1-based sul display, quindi il numero
    mostrato e' `channel + 1`.
    """
    ch = channel_of(inst)
    if ch is None:
        zona = inst.find('zone')
        return f'MIDI zona {zona.text}' if zona is not None else f'<{inst.tag}>'
    if inst.tag == 'cvChannel':
        return f'CV {ch + 1}'
    try:
        suf = int(inst.get('suffix', SENZA_SUFFIX))
    except (TypeError, ValueError):
        suf = SENZA_SUFFIX
    coda = '' if suf < 0 else chr(ord('A') + suf)
    return f'MIDI {ch + 1}{coda}'


def find_track(doc: Document, tipo: str, channel: int,
               suffix: int = SENZA_SUFFIX) -> Node | None:
    for i in tracks(doc, tipo):
        if channel_of(i) != channel:
            continue
        if tipo == 'cv':
            return i
        if int(i.get('suffix', SENZA_SUFFIX)) == suffix:
            return i
    return None


# ------------------------------------------------------------------ scrittura

def _aggiungi(doc: Document, tipo: str, channel: int, attrs: dict,
              *, length: int, section: str, colour_offset: str,
              playing: bool) -> tuple[Node, Node]:
    from . import song as S                               # import locale: ciclo
    from .create import CLIP_BASE, _colonne_default       # noqa: PLC0415

    strumenti = doc.root.find('instruments')
    contenitore = doc.root.find('sessionClips')
    if strumenti is None or contenitore is None:
        raise ValueError('la song non ha <instruments> o <sessionClips>')

    inst = Node(tag=TAG[tipo],
                attrs=[('channel', str(channel))] + list(attrs.items()),
                self_closing=True)
    strumenti.append(inst)

    a = dict(CLIP_BASE)
    a.update({
        ATTR_CLIP[tipo]: str(channel),
        'length': str(length),
        'colourOffset': str(colour_offset),
        'section': str(section),
        'isPlaying': '1' if playing else '0',
    })
    clip = Node(tag='instrumentClip', attrs=list(a.items()))
    # nell'ordine in cui il dispositivo li scrive
    clip.append(Node(tag='arpeggiator', attrs=list(ARPEGGIATOR_BASE.items()),
                     self_closing=True))
    for tag, testo in zip(('bendRange', 'bendRangeMPE'), BEND_RANGE):
        clip.append(Node(tag=tag, text=testo))
    clip.append(_colonne_default())
    # niente contenitore di parametri: 135 clip MIDI su 144 e tutte e 12 le
    # CV non ne hanno, e su una clip senza suono non avrebbe cosa contenere
    contenitore.append(clip)

    S.scroll_song_view_to(doc, len(contenitore.children) - 1)
    S.scroll_arrangement_view_to(doc, len(strumenti.children) - 1)
    S.set_edited_clip(doc, clip)
    return inst, clip


def add_midi_track(doc: Document, channel: int, *,
                   suffix: int = SENZA_SUFFIX, length: int = 384,
                   section: str = '0', colour_offset: str = '0',
                   playing: bool = False) -> tuple[Node, Node]:
    """Una traccia MIDI in uscita sul canale dato, con la sua clip.

    `channel` e' 0-based come nel file: 0 e' il canale 1 del display.
    `suffix` serve solo per una SECONDA traccia sullo stesso canale che debba
    suonare insieme alla prima — vedi il docstring del modulo.
    """
    if not 0 <= channel < MIDI_CANALI:
        raise ValueError(f'canale MIDI fuori da 0-{MIDI_CANALI - 1}: {channel}')
    if find_track(doc, 'midi', channel, suffix) is not None:
        raise ValueError(
            f'esiste gia una traccia su MIDI {channel + 1} con suffix '
            f'{suffix}: due tracce con lo stesso canale E lo stesso suffisso '
            f'non possono suonare insieme, servono suffissi diversi')
    attrs = dict(ISTANZA_MIDI)
    attrs['suffix'] = str(suffix)
    return _aggiungi(doc, 'midi', channel, attrs, length=length,
                     section=section, colour_offset=colour_offset,
                     playing=playing)


def add_cv_track(doc: Document, channel: int, *, cv2_source: int | None = None,
                 length: int = 384, section: str = '0',
                 colour_offset: str = '0',
                 playing: bool = False) -> tuple[Node, Node]:
    """Una traccia CV su una delle due uscite, con la sua clip."""
    if not 0 <= channel < CV_CANALI:
        raise ValueError(
            f'il Deluge ha {CV_CANALI} uscite CV, canale 0 o 1: {channel}')
    if find_track(doc, 'cv', channel) is not None:
        raise ValueError(f'esiste gia una traccia su CV {channel + 1}')
    attrs = dict(ISTANZA_CV)
    if cv2_source is not None:
        if cv2_source not in CV2_SORGENTI:
            raise ValueError(f'cv2Source fuori tabella {CV2_SORGENTI}: '
                             f'{cv2_source}')
        attrs['cv2Source'] = str(cv2_source)
    return _aggiungi(doc, 'cv', channel, attrs, length=length,
                     section=section, colour_offset=colour_offset,
                     playing=playing)


def check(doc: Document) -> list[str]:
    """I problemi delle tracce MIDI e CV.

    Il caso che conta e' il conflitto di canale: due tracce MIDI sullo stesso
    canale con lo stesso suffisso, o due tracce sulla stessa uscita CV. Nel
    file ci stanno, ma sono un solo strumento visto due volte e non possono
    suonare insieme — e' il suffisso a renderle distinte, non l'esistenza.
    """
    problemi = []
    visti: dict[tuple, Node] = {}
    for inst in tracks(doc):
        t = kind(inst)
        ch = channel_of(inst)
        if ch is None:
            continue                       # zona MPE: non la giudichiamo
        limite = MIDI_CANALI if t == 'midi' else CV_CANALI
        if not 0 <= ch < limite:
            problemi.append(
                f'{label(inst)}: canale {ch} fuori da 0-{limite - 1}')
        chiave = (t, ch, inst.get('suffix') if t == 'midi' else None)
        if chiave in visti:
            problemi.append(
                f'{label(inst)}: stesso canale e stesso suffisso di una '
                f'traccia precedente, non possono suonare insieme')
        else:
            visti[chiave] = inst
        if t == 'cv':
            s = inst.get('cv2Source')
            if s is not None and int(s) not in CV2_SORGENTI:
                problemi.append(f'{label(inst)}: cv2Source {s} fuori tabella')
    return problemi


def describe(doc: Document) -> list[str]:
    """Una riga per traccia, come la chiamerebbe il dispositivo."""
    from . import song as S                               # import locale: ciclo
    from . import arranger as A                           # noqa: PLC0415

    out = []
    for inst in tracks(doc):
        t = kind(inst)
        clip = [c for _, c in S.clips(doc)
                if c.get(ATTR_CLIP[t]) == inst.get('channel')]
        note = sum(len(S.read_notes(r)) for c in clip for r in S.note_rows(c))
        extra = ''
        if t == 'cv' and inst.get('cv2Source') is not None:
            extra = f', CV2 = {CV2_SORGENTI[int(inst.get("cv2Source"))]}'
        out.append(f'{label(inst)}: {len(clip)} clip, {note} note, '
                   f'{len(A.instances(inst))} istanze d arranger{extra}')
    return out
