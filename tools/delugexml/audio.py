"""Le clip audio: un campione sulla timeline, invece di note da suonare.

E' l'unico tipo di clip che non contiene musica ma un RIFERIMENTO a un file:

    <audioClip trackName="AUDIO3" filePath="SAMPLES/CLIPS/REC00133.WAV"
               startSamplePos="2086" endSamplePos="1461948" length="3072" …>
        <params … />
    </audioClip>

Nel corpus: 192 `<audioTrack>` in 40 song e 194 `<audioClip>`.

TRE COSE CHE NON SI DEDUCONO GUARDANDO LE ALTRE CLIP
----------------------------------------------------
**Il contenitore dei parametri e' `<params>`**, un terzo nome dopo
`soundParams` e `kitParams` — su 194 clip su 194. Con 31 attributi, che sono
quelli della catena effetti, non di un motore di sintesi: non c'e' nessun
suono da descrivere.

**Il legame con lo strumento e' per nome**: `trackName` sulla clip contro
`name` sull'`<audioTrack>`. Non c'e' preset, non c'e' cartella.

**Le clip audio portano attributi DUPLICATI**, scritti due volte dal firmware:
`isPlaying`, `isSoloing`, `isArmedForRecording`, `length`, `colourOffset`,
`section` compaiono in coppia su 71 clip (265 attributi contati su 194 clip).
E' lo stesso difetto del firmware per cui questo progetto ha un parser
tollerante. Qui si scrivono UNA volta sola: il duplicato e' un difetto di chi
scrive, non un requisito di chi legge.

CAMPIONI E TICK
---------------
`startSamplePos` e `endSamplePos` sono in **frame**, `length` in **tick**. Il
sorgente (`audio_clip.cpp`) mostra come il dispositivo li lega registrando:

    double samplesPerTick = sampleHolder.getDurationInSamples(true) / numTicksDone;
    sampleHolder.endPos = sampleHolder.startPos + samplesPerTick * suggestedLength + 0.5;

cioe' `fine - inizio = length * campioni_per_tick`. Nel corpus la relazione
regge entro l'1% su 154 clip su 185, con mediana esattamente 1.0000 — le altre
sono state allungate o accorciate a mano.

Non e' pero' un VINCOLO, perche' `pitchSpeedIndependent` vale 1 su tutte e 194
le clip: il Deluge **stira il campione** per farlo stare nella lunghezza della
clip. Scrivere le posizioni secondo la relazione significa "suona alla velocita'
naturale"; scriverle diverse significa allungare o accorciare.

LA CLIP VUOTA
-------------
Una clip con `filePath=""` e' uno slot pronto a registrare e senza campione, e
porta sempre `startSamplePos="0"`, `endSamplePos="9999999"` e
`attack="-2147483648"` (cioe' 0 sul display). Nel corpus sono 9, ed e' una
corrispondenza **esatta**: le 9 clip con `filePath` vuoto sono le stesse 9 con
`endSamplePos="9999999"`, nessuna di piu' e nessuna di meno.

Quel 9999999 sembrava una sentinella "fino alla fine del file". Non lo e': il
sorgente scrive e rilegge il valore grezzo senza nessun caso speciale, ed e'
semplicemente il valore iniziale di una clip che non ha ancora un campione.
Una clip vuota e' quindi uno stato legittimo, non un difetto — `check()` non
la segnala.
"""
from __future__ import annotations

from .parser import Document, Node, parse

#: Un `<audioTrack>` e il `<params>` di una `<audioClip>`, presi da `Lfx.XML`
#: (c1.3.0). Stanno qui come testo e non come dizionari perche' hanno una
#: struttura annidata — l'audioTrack porta `delay`, `sidechain`,
#: `audioCompressor` e `stutter` — e trascriverla a mano sarebbe un modo per
#: sbagliarla. `name` e `clipInstances` sono stati tolti: dipendono dall'istanza.
TRACCIA_XML = '''<audioTrack
	mode="Player"
	inputChannel="left"
	outputRecordingIndex="0"
	isArmedForRecording="0"
	activeModFunction="0"
	colour="0"
	modFXCurrentParam="feedback"
	currentFilterType="lpf"
	modFXType="flanger"
	lpfMode="24dB"
	hpfMode="HPLadder"
	filterRoute="H2L">
	<delay
		pingPong="1"
		analog="0"
		syncLevel="8"
		syncType="0" />
	<sidechain
		attack="327244"
		release="936"
		syncLevel="7"
		syncType="0" />
	<audioCompressor
		attack="83886080"
		release="83886080"
		thresh="0"
		ratio="1073741824"
		compHPF="0"
		compBlend="2147483647" />
	<stutter
		quantized="1"
		reverse="0"
		pingPong="0" />
</audioTrack>'''

PARAMS_XML = '''<params
	reverbAmount="0x80000000"
	volume="0xE0000000"
	pan="0x00000000"
	sidechainCompressorShape="0xDC28F5B2"
	modFXDepth="0x00000000"
	modFXRate="0xE0000000"
	stutterRate="0x00000000"
	sampleRateReduction="0x80000000"
	bitCrush="0x80000000"
	modFXOffset="0x00000000"
	modFXFeedback="0x80000000"
	compressorThreshold="0x00000000"
	arpeggiatorGate="0x7FFFFFFF"
	noteProbability="0x7FFFFFFF"
	bassProbability="0x80000000"
	swapProbability="0x80000000"
	glideProbability="0x80000000"
	reverseProbability="0x80000000"
	chordProbability="0x80000000"
	ratchetProbability="0x80000000"
	ratchetAmount="0x80000000"
	sequenceLength="0x80000000"
	chordPolyphony="0x80000000"
	rhythm="0x80000000"
	spreadVelocity="0x80000000"
	spreadGate="0x80000000"
	spreadOctave="0x80000000"
	lpfMorph="0x80000000"
	hpfMorph="0x80000000"
	tempo="0x00000000"
	arpeggiatorRate="0x00000000">
	<delay
		rate="0x00000000"
		feedback="0x80000000" />
	<lpf
		frequency="0x7FFFFFFF"
		resonance="0x80000000" />
	<hpf
		frequency="0x80000000"
		resonance="0x80000000" />
	<equalizer
		bass="0x00000000"
		treble="0x00000000"
		bassFrequency="0x00000000"
		trebleFrequency="0x00000000" />
</params>'''

#: Da dove prende il segnale una traccia audio. Valori TESTUALI, non numeri.
INGRESSI = ('none', 'left', 'right', 'stereo', 'balanced')

#: `Player` riproduce, `Looper/FX` registra e cicla. Nel corpus 5 contro 1.
MODI = ('Player', 'Looper/FX')

#: Attributi della clip audio oltre a quelli comuni, coi valori che il
#: dispositivo scrive: `pitchSpeedIndependent`, `priority` e
#: `overdubsShouldCloneAudioTrack` valgono 1 su tutte e 194 le clip del corpus.
CLIP_AUDIO_BASE = {
    'pitchSpeedIndependent': '1',
    'attack': '-1546188233',        # display 7, il valore di default scritto
    'priority': '1',
    'overdubsShouldCloneAudioTrack': '1',
    'isPlaying': '0',
    'isSoloing': '0',
    'isArmedForRecording': '1',
}


def tracks(doc: Document) -> list[Node]:
    from . import song as S                               # import locale: ciclo
    return [i for i in S.instruments(doc) if i.tag == 'audioTrack']


def clips(doc: Document) -> list[Node]:
    from . import arranger as A                           # import locale: ciclo
    return [c for da in (False, True) for c in A.clip_list(doc, da)
            if c.tag == 'audioClip']


def track_of(doc: Document, clip: Node) -> Node | None:
    """La traccia della clip: `trackName` contro `name`."""
    nome = clip.get('trackName')
    if nome is None:
        return None
    for t in tracks(doc):
        if t.get('name') == nome:
            return t
    return None


def nome_libero(doc: Document, base: str = 'AUDIO') -> str:
    """Il primo `AUDIOn` non ancora usato, come li numera il dispositivo."""
    usati = {t.get('name') for t in tracks(doc)}
    n = 1
    while f'{base}{n}' in usati:
        n += 1
    return f'{base}{n}'


# --------------------------------------------------------- campioni e tick

def samples_per_tick(doc: Document) -> float:
    from . import song as S                               # import locale: ciclo
    return S.samples_per_tick(doc.root)


def ticks_to_samples(doc: Document, ticks: int) -> int:
    """Quanti frame durano `ticks` al tempo della song."""
    return round(ticks * samples_per_tick(doc))


def wav_frames(path) -> tuple[int, int, int]:
    """(frame, sample rate, canali) leggendo l'intestazione di un WAV.

    Serve per calcolare `endSamplePos` invece di indovinarlo: le posizioni
    sono in frame, e senza sapere quanto e' lungo il file non si puo' dire
    dove finisce. Il file si puo' scaricare dalla SD con `dsysex get`.
    """
    import struct                                         # noqa: PLC0415
    from pathlib import Path                              # noqa: PLC0415

    d = Path(path).read_bytes()
    if d[:4] != b'RIFF' or d[8:12] != b'WAVE':
        raise ValueError(f'{path}: non e un WAV (RIFF/WAVE assenti)')
    i, fmt, dati = 12, None, None
    while i + 8 <= len(d):
        cid = d[i:i + 4]
        size = struct.unpack('<I', d[i + 4:i + 8])[0]
        if cid == b'fmt ':
            fmt = struct.unpack('<HHIIHH', d[i + 8:i + 8 + 16])
        elif cid == b'data':
            dati = size
        i += 8 + size + (size & 1)
    if fmt is None or dati is None:
        raise ValueError(f'{path}: manca il chunk fmt o data')
    _, canali, rate, _, align, _ = fmt
    return dati // align, rate, canali


# ------------------------------------------------------------------ scrittura

def add_audio_track(doc: Document, *, name: str | None = None,
                    input_channel: str = 'none',
                    mode: str = 'Player') -> Node:
    """Una traccia audio vuota. La clip si aggiunge con `add_audio_clip()`."""
    from . import song as S                               # import locale: ciclo

    if input_channel not in INGRESSI:
        raise ValueError(f'ingresso {input_channel!r} fuori da {INGRESSI}')
    if mode not in MODI:
        raise ValueError(f'modo {mode!r} fuori da {MODI}')

    strumenti = doc.root.find('instruments')
    if strumenti is None:
        raise ValueError('la song non ha <instruments>')
    nome = name or nome_libero(doc)
    if any(t.get('name') == nome for t in tracks(doc)):
        raise ValueError(f'esiste gia una traccia audio di nome {nome!r}')

    inst = parse(TRACCIA_XML).roots[0].copy_detached()
    inst.set('inputChannel', input_channel)
    inst.set('mode', mode)
    # `name` va per primo, come lo scrive il dispositivo
    inst.attrs.insert(0, ('name', nome))
    inst.dirty = True
    strumenti.append(inst)
    S.scroll_arrangement_view_to(doc, len(strumenti.children) - 1)
    return inst


def add_audio_clip(doc: Document, traccia: Node, file_path: str, *,
                   length: int = 384, start: int = 0,
                   end: int | None = None, wav: str | None = None,
                   section: str = '0', colour_offset: str = '0',
                   playing: bool = False) -> Node:
    """Una clip che suona `file_path` sulla traccia data.

    `end` di default e' calcolato dalla relazione del firmware, cioe'
    `start + length * campioni_per_tick`: il campione suona alla velocita'
    naturale. Passando `wav` — il file scaricato dalla SD — la fine viene
    limitata ai frame che il file ha davvero, che e' l'unico modo di non
    indicare una posizione inesistente.
    """
    from . import song as S                               # import locale: ciclo

    if traccia.tag != 'audioTrack':
        raise ValueError(f'serve un <audioTrack>, non <{traccia.tag}>')
    if length <= 0:
        raise ValueError(f'lunghezza non valida: {length}')
    if start < 0:
        raise ValueError(f'posizione di partenza negativa: {start}')

    if end is None:
        end = start + ticks_to_samples(doc, length)
    if wav is not None:
        disponibili, _, _ = wav_frames(wav)
        if start >= disponibili:
            raise ValueError(f'{file_path}: parte a {start} ma il file ha '
                             f'{disponibili} frame')
        end = min(end, disponibili)
    if end <= start:
        raise ValueError(f'fine {end} non oltre l inizio {start}')

    attrs = {'trackName': traccia.get('name'), 'filePath': file_path,
             'startSamplePos': str(start), 'endSamplePos': str(end)}
    attrs.update(CLIP_AUDIO_BASE)
    attrs.update({
        'isPlaying': '1' if playing else '0',
        'length': str(length),
        'colourOffset': str(colour_offset),
        'section': str(section),
    })
    clip = Node(tag='audioClip', attrs=list(attrs.items()))
    clip.append(parse(PARAMS_XML).roots[0].copy_detached())

    contenitore = doc.root.find('sessionClips')
    if contenitore is None:
        raise ValueError('la song non ha <sessionClips>')
    contenitore.append(clip)
    S.scroll_song_view_to(doc, len(contenitore.children) - 1)
    return clip


def set_sample(doc: Document, clip: Node, file_path: str, *,
               start: int | None = None, end: int | None = None,
               wav: str | None = None) -> Node:
    """Cambia il campione di una clip esistente, ricalcolando le posizioni."""
    if clip.tag != 'audioClip':
        raise ValueError(f'serve una <audioClip>, non <{clip.tag}>')
    clip.set('filePath', file_path)
    if start is not None:
        clip.set('startSamplePos', str(start))
    s = int(clip.get('startSamplePos') or 0)
    if end is None:
        end = s + ticks_to_samples(doc, int(clip.get('length') or 0))
    if wav is not None:
        end = min(end, wav_frames(wav)[0])
    clip.set('endSamplePos', str(end))
    return clip


def check(doc: Document) -> list[str]:
    """I problemi delle clip audio.

    Il caso che conta e' la clip che non risolve la sua traccia: il legame e'
    per nome e nient'altro, quindi un `trackName` che non corrisponde a nessun
    `<audioTrack name=…>` lascia la clip senza un posto dove suonare.
    """
    problemi = []
    nomi = [t.get('name') for t in tracks(doc)]
    for n in set(nomi):
        if n is not None and nomi.count(n) > 1:
            problemi.append(f'due tracce audio si chiamano {n!r}: '
                            f'le clip non possono distinguerle')
    for t in tracks(doc):
        ing = t.get('inputChannel')
        if ing is not None and ing not in INGRESSI:
            problemi.append(f'{t.get("name")!r}: inputChannel {ing!r} '
                            f'fuori da {INGRESSI}')
        m = t.get('mode')
        if m is not None and m not in MODI:
            problemi.append(f'{t.get("name")!r}: mode {m!r} fuori da {MODI}')
    for c in clips(doc):
        nome = c.get('trackName')
        if track_of(doc, c) is None:
            problemi.append(f'clip su {nome!r}: nessun <audioTrack> con quel '
                            f'nome, la clip non ha dove suonare')
        if c.find('params') is None:
            problemi.append(f'clip su {nome!r}: manca <params>')
        if is_empty(c):
            continue          # slot pronto a registrare: stato legittimo
        try:
            s, e = int(c.get('startSamplePos')), int(c.get('endSamplePos'))
            if e <= s:
                problemi.append(f'clip su {nome!r}: endSamplePos {e} non '
                                f'oltre startSamplePos {s}')
        except (TypeError, ValueError):
            problemi.append(f'clip su {nome!r}: posizioni non leggibili')
    return problemi


#: I valori che il dispositivo lascia su una clip audio senza campione.
VUOTA = {'startSamplePos': '0', 'endSamplePos': '9999999',
         'attack': '-2147483648'}


def is_empty(clip: Node) -> bool:
    """La clip e' uno slot senza campione, pronto a registrare."""
    return not clip.get('filePath')


def describe(doc: Document) -> list[str]:
    from . import arranger as A                           # import locale: ciclo

    out = []
    for t in tracks(doc):
        cs = [c for c in clips(doc) if c.get('trackName') == t.get('name')]
        out.append(f'{t.get("name")}: ingresso {t.get("inputChannel")}, '
                   f'{t.get("mode") or "Player"}, {len(cs)} clip, '
                   f'{len(A.instances(t))} istanze d arranger')
        for c in cs:
            s, e = int(c.get('startSamplePos')), int(c.get('endSamplePos'))
            sec = (e - s) / 44100
            out.append(f'    {c.get("filePath")}  frame {s}-{e} '
                       f'(~{sec:.2f}s) su {c.get("length")} tick')
    return out
