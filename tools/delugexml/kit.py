"""Kit e drum: aggiungere, togliere, assegnare campioni.

COM'E' FATTO UN KIT
-------------------
    <kit presetName="…">
      <defaultParams …/>            parametri del kit (31)
      <soundSources>
        <sound name="KICK" path="…">   un drum E' UN SOUND COMPLETO:
          <osc1 type="sample" fileName="SAMPLES/…"><zone …/></osc1>
          <osc2 …/> <lfo1..4/> <unison/> <defaultParams/> <arpeggiator/>
          <modKnobs/> <midiOutput/> <delay/> <sidechain/> …
        </sound>
        …
      </soundSources>
      <selectedDrumIndex>0</selectedDrumIndex>
    </kit>

Nella clip, ogni drum ha **una noteRow**, con `drumIndex` che e' la posizione
ordinale dentro `<soundSources>`, e un proprio `<soundParams>` da 55
attributi — i parametri di quel singolo drum in quella clip. Si leggono e
scrivono con `sound.py` come qualunque altro.

L'INVARIANTE CHE QUESTO MODULO PROTEGGE
---------------------------------------
`drumIndex` e' un indice posizionale, non un identificatore. Verificato: in
tutte le clip di kit del corpus gli indici sono contigui a partire da 0 e in
corrispondenza uno a uno con i drum. Aggiungere in fondo e' sicuro; togliere
o inserire in mezzo **rinumera tutto cio' che segue**, in ogni clip che usa
quel kit. Farlo a mano significa quasi certamente spostare le note su un
altro drum senza accorgersene.
"""
from __future__ import annotations

from dataclasses import dataclass

from .parser import Document, Node
from . import song as S


def kit_clips(doc: Document, kit: Node) -> list[Node]:
    """Le clip che suonano questo kit.

    Risolve con `song.instrument_of()`, che prova nome+cartella e poi slot
    numerico nell'ordine giusto — non un confronto diretto degli attributi.
    [BUG trovato dal cancello] La versione precedente confrontava
    `instrumentPresetName`/`instrumentPresetFolder` con `==`: nei file di
    formato vecchio, dove sia il kit sia la clip non portano affatto un nome
    (`None == None`), QUALUNQUE clip di kit risultava "di questo kit", anche
    se il file ha piu' kit su slot diversi. Verificato su `Looptest .XML` e
    `Polymap .XML` del corpus (3.0.0): un kit da 1 drum riceveva anche le
    clip di un secondo kit da 16, dando falsi "drumIndex oltre i drum del
    kit". Non era un difetto dei file.
    """
    return [clip for _, clip in S.clips(doc)
           if S.is_kit_clip(clip) and S.instrument_of(doc, clip) is kit]


def drum_index_of(kit: Node, name: str) -> int:
    """L'indice del drum che si chiama `name`."""
    bersaglio = name.strip().upper()
    for i, d in enumerate(S.drums(kit)):
        if (S.nome_drum(d) or '').strip().upper() == bersaglio:
            return i
    disponibili = ', '.join(S.nome_drum(d) or '?' for d in S.drums(kit))
    raise ValueError(f'nessun drum "{name}" in questo kit. '
                     f'Disponibili: {disponibili}')


def copy_drum(kit: Node, which: int | str) -> Node:
    """Una copia staccata di un drum, pronta per un ALTRO kit o file.

    Staccata perche' un nodo copiato conserva gli offset del documento di
    provenienza: riemesso altrove, il serializzatore ne ricopierebbe i byte
    sbagliati. Vedi `Node.copy_detached()`.
    """
    i = which if isinstance(which, int) else drum_index_of(kit, which)
    tutti = S.drums(kit)
    if not 0 <= i < len(tutti):
        raise IndexError(f'drum {i} inesistente (ce ne sono {len(tutti)})')
    return tutti[i].copy_detached()


def add_drum(doc: Document, kit: Node, drum: Node, *,
             name: str | None = None) -> int:
    """Aggiunge un drum IN FONDO al kit e la noteRow corrispondente in ogni
    clip che lo usa. Ritorna il nuovo `drumIndex`.

    In fondo e non in mezzo: inserire rinumererebbe i drum successivi, e con
    loro tutte le note gia' scritte.
    """
    sorgenti = kit.find('soundSources')
    if sorgenti is None:
        raise ValueError('il kit non ha <soundSources>')
    nuovo = drum if drum.span is None else drum.copy_detached()
    if name is not None:
        nuovo.set('name', name)
    sorgenti.append(nuovo)
    indice = len(sorgenti.children) - 1

    for clip in kit_clips(doc, kit):
        riga = S.add_note_row(clip, indice)
        # ogni riga di kit del corpus porta un colourOffset; e' cosmetico ma
        # la sua assenza sarebbe l'unica differenza da cio' che scrive il
        # dispositivo, e non vale la pena introdurla
        riga.set('colourOffset', str((indice * 7) % 72 - 36))
        # e soprattutto un <soundParams>: sono i parametri di QUEL drum in
        # QUELLA clip, 55 attributi, presenti su ogni riga di kit scritta dal
        # dispositivo. Senza, il drum non ha volume ne' pan propri e
        # `sound.py` non trova nulla su cui lavorare.
        _monta_params_riga(nuovo, riga)
    return indice


def _monta_params_riga(drum: Node, riga: Node) -> None:
    """Da `<defaultParams>` del drum al `<soundParams>` della sua noteRow.

    E' lo stesso schema che vale per i preset di synth: i valori di partenza
    vivono nel preset come `defaultParams` e diventano i parametri della clip.
    Il drum conserva comunque i suoi, come fa il dispositivo.
    """
    if riga.find('soundParams') is not None:
        return
    sorgente = drum.find('defaultParams')
    params = (sorgente.copy_detached() if sorgente is not None
              else Node(tag='defaultParams'))
    params.tag = 'soundParams'
    params.dirty = True
    riga.self_closing = False
    riga.append(params)


def remove_drum(doc: Document, kit: Node, which: int | str) -> int:
    """Toglie un drum e RINUMERA tutto cio' che segue, in ogni clip.

    E' l'operazione pericolosa del modulo: senza rinumerazione, ogni nota
    scritta su un drum successivo finirebbe su quello sbagliato. Ritorna
    l'indice rimosso.
    """
    i = which if isinstance(which, int) else drum_index_of(kit, which)
    sorgenti = kit.find('soundSources')
    tutti = sorgenti.children if sorgenti else []
    if not 0 <= i < len(tutti):
        raise IndexError(f'drum {i} inesistente (ce ne sono {len(tutti)})')

    sorgenti.children = [d for j, d in enumerate(tutti) if j != i]
    sorgenti.touch()

    for clip in kit_clips(doc, kit):
        righe = S.note_rows(clip)
        contenitore = clip.find('noteRows')
        tenute = []
        for r in righe:
            if not r.has('drumIndex'):
                tenute.append(r)
                continue
            idx = int(r.get('drumIndex'))
            if idx == i:
                continue                      # la riga del drum tolto
            if idx > i:
                r.set('drumIndex', str(idx - 1))
            tenute.append(r)
        contenitore.children = tenute
        contenitore.touch()

    # il drum selezionato potrebbe non esistere piu'
    sel = kit.find('selectedDrumIndex')
    if sel is not None and sel.text and int(sel.text) >= len(sorgenti.children):
        sel.text = str(max(0, len(sorgenti.children) - 1))
        sel.touch()
    return i


#: Estremi di una nota MIDI.
NOTA_MIN, NOTA_MAX = 0, 127


def transpose_drum(drum: Node, semitoni: int) -> str:
    """Intona un drum di semitoni. Ritorna cosa e' stato mosso.

    Un kit puo' contenere righe di quattro tipi -- il manuale: «A synth, MIDI
    or CV row can be added in the kit view» -- e non tutte si intonano allo
    stesso modo, ne' si intonano tutte:

        'midi'     una riga MIDI: si sposta `note`, fra 0 e 127
        'osc'      campione o sintetizzato: `transpose` sui suoi <osc>
        'saltato'  un <gateOutput>, o una riga senza niente da intonare

    Una riga MIDI e' un `<midiOutput>` dentro `<soundSources>`, FRATELLO dei
    `<sound>`, e porta la sua altezza nell'attributo `note`:

        <midiOutput name="" channel="0" note="0" />

    [CORREZIONE] Questo progetto aveva prima implementato un'ipotesi, ed era
    sbagliata su tutti e due i punti: cercava un `<sound>` con un
    `<midiOutput>` FIGLIO e spostava `noteForDrum`. Quel figlio esiste su ogni
    `<sound>` ma vale `channel="255" noteForDrum="255"` in tutti e 1180 i casi
    del corpus -- e' un'altra cosa, mai vista attiva, e non e' la riga MIDI di
    un kit. La forma vera si e' potuta vedere solo facendo salvare al
    dispositivo un kit con una riga MIDI: `refs/songs/TRASF401MIDI.XML`.

    Vale la pena ricordare perche' l'ipotesi sembrava ragionevole: `noteForDrum`
    ERA un attributo osservato, quindi non si stava inventando una struttura.
    Non e' bastato -- un nome osservato nel posto sbagliato e' comunque il
    posto sbagliato.

    Una riga di un tipo che non conosciamo cade in 'saltato' invece di far
    fallire la trasposizione di tutto il kit.
    """
    if drum.tag == 'midiOutput':
        nota = drum.get('note')
        if nota is None:
            return 'saltato'
        drum.set('note', str(max(NOTA_MIN,
                                 min(NOTA_MAX, int(nota) + semitoni))))
        return 'midi'

    osc = [o for n in ('osc1', 'osc2') if (o := drum.find(n)) is not None]
    if not osc:
        return 'saltato'                      # <gateOutput>: un gate non ha altezza
    for o in osc:
        o.set('transpose', str(int(o.get('transpose') or 0) + semitoni))
    return 'osc'


def transpose(kit: Node, semitoni: int) -> dict:
    """Intona tutti i drum di un kit. Vedi `transpose_drum` per i casi."""
    esiti = [transpose_drum(d, semitoni) for d in S.drums(kit)]
    return {'drum': sum(1 for e in esiti if e != 'saltato'),
            'midi': sum(1 for e in esiti if e == 'midi'),
            'saltati': sum(1 for e in esiti if e == 'saltato')}


def set_sample(drum: Node, path: str, *, start: int | None = None,
               end: int | None = None, osc: int = 1) -> Node:
    """Assegna un campione a un drum.

    Il percorso e' relativo alla radice della SD, come lo scrive il
    dispositivo: `SAMPLES/…/nome.wav`. Non viene verificata l'esistenza del
    file: questo modulo non sa dove sia la SD. Un riferimento rotto si vede
    solo sul dispositivo, come sample mancante.
    """
    nodo = drum.find(f'osc{osc}')
    if nodo is None:
        raise ValueError(f'il drum non ha <osc{osc}>')
    if nodo.find('sampleRanges') is not None:
        raise ValueError('oscillatore multisample: usare set_multisample()')
    nodo.set('type', 'sample')
    nodo.set('fileName', path)
    if start is not None or end is not None:
        zona = nodo.find('zone')
        if zona is None:
            zona = nodo.append(Node(tag='zone', self_closing=True))
        if start is not None:
            zona.set('startSamplePos', str(int(start)))
        if end is not None:
            zona.set('endSamplePos', str(int(end)))
    return nodo


def sample_of(drum: Node, osc: int = 1) -> str | None:
    nodo = drum.find(f'osc{osc}')
    return nodo.get('fileName') if nodo is not None else None


@dataclass(frozen=True)
class SampleRange:
    """Un campione fino a `top_note` inclusa; l'ultimo arriva fino a TOP."""

    path: str
    top_note: int | None
    start: int
    end: int
    transpose: int = 0
    cents: int = 0


def set_multisample(sound: Node, ranges: list[SampleRange], *, osc: int = 1) -> Node:
    """Sostituisce i range per nota di un oscillatore sample di un preset reale.

    Il preset deve gia' contenere `<sampleRanges>/<sampleRange>/<zone>`:
    i nodi nuovi sono copie di quella struttura osservata, non XML inventato.
    L'ultimo range non porta `rangeTopNote`, come nel preset Tal Rhodes.
    """
    if sound.tag != 'sound' or osc not in (1, 2):
        raise ValueError('serve un <sound> e osc 1 o 2')
    source = sound.find(f'osc{osc}')
    container = source.find('sampleRanges') if source is not None else None
    model = container.find('sampleRange') if container is not None else None
    if model is None or model.find('zone') is None:
        raise ValueError('serve un preset multisample osservato come modello')
    if {key for key, _ in model.find('zone').attrs} - {
            'startSamplePos', 'endSamplePos'}:
        raise ValueError('il modello ha altri punti di loop: preservarlo')
    if not ranges:
        raise ValueError('serve almeno un range')
    previous = -1
    for i, r in enumerate(ranges):
        if (not all(isinstance(v, int) and not isinstance(v, bool)
                    for v in (r.start, r.end, r.transpose, r.cents))
                or (r.top_note is not None and
                    (not isinstance(r.top_note, int)
                     or isinstance(r.top_note, bool)))):
            raise ValueError(f'range {i}: posizioni e accordatura intere')
        if not r.path or not r.path.startswith('SAMPLES/'):
            raise ValueError(f'range {i}: percorso SAMPLES/ richiesto')
        if r.start < 0 or r.end <= r.start:
            raise ValueError(f'range {i}: zona non valida')
        if i == len(ranges) - 1:
            if r.top_note is not None:
                raise ValueError('l ultimo range deve arrivare a TOP')
        elif (r.top_note is None or not 0 <= r.top_note <= 127
              or r.top_note <= previous):
            raise ValueError(f'range {i}: rangeTopNote non crescente')
        if r.top_note is not None:
            previous = r.top_note
    nuovi = []
    for r in ranges:
        item = model.copy_detached()
        if r.top_note is None:
            item.remove('rangeTopNote')
        else:
            item.set('rangeTopNote', str(r.top_note))
        item.set('fileName', r.path)
        for key, value in (('transpose', r.transpose), ('cents', r.cents)):
            if value:
                item.set(key, str(value))
            elif item.has(key):
                item.remove(key)
        zone = item.find('zone')
        zone.set('startSamplePos', str(r.start))
        zone.set('endSamplePos', str(r.end))
        nuovi.append(item)
    container.children = nuovi
    container.touch()
    source.set('type', 'sample')
    return container


def set_sample_playback(sound: Node, *, osc: int = 1,
                        loop: str | None = None,
                        reverse: bool | None = None,
                        stretch: bool | None = None) -> Node:
    """Loop, reverse e stretch sull'oscillatore sample di synth o drum."""
    if sound.tag != 'sound' or osc not in (1, 2):
        raise ValueError('serve un <sound> e osc 1 o 2')
    source = sound.find(f'osc{osc}')
    if source is None or source.get('type') != 'sample':
        raise ValueError(f'<osc{osc}> non e un oscillatore sample')
    if loop is not None and loop not in LOOP_MODE:
        raise ValueError(f'loop {loop!r} sconosciuto')
    if reverse is not None and not isinstance(reverse, bool):
        raise ValueError('reverse deve essere bool')
    if stretch is not None and not isinstance(stretch, bool):
        raise ValueError('stretch deve essere bool')
    if loop is not None:
        source.set('loopMode', str(LOOP_MODE[loop]))
    if reverse is not None:
        source.set('reversed', '1' if reverse else '0')
    if stretch is not None:
        source.set('timeStretchEnable', '1' if stretch else '0')
    return source


#: I `loopMode` (REPEAT MODE del guidebook, cap. 9.13): CUT=0, ONCE=1, LOOP=2,
#: STRETCH=3. ONCE=1 e CUT=0 sono verificati contro lo Slicer NATIVO del Deluge:
#: una fetta salvata dal dispositivo (`MMYEAH.XML`) ha osc1 `loopMode=1` (ONCE)
#: con la zona `[start,end]` -- e ONCE suona la ZONA CARICATA `[start,end]`, non
#: l'intero file. (Un one-shot ha zona = tutto il file, e per quello suona tutto:
#: e' la zona a delimitare, non il mode.)
LOOP_MODE = {'cut': 0, 'once': 1, 'loop': 2, 'stretch': 3}


def affetta(doc: Document, kit: Node, path: str, frames: int, *,
            n: int = 16, base: int = 0, mode: str = 'once') -> list[str]:
    """Affetta un campione in un kit di N drum-fetta -- il vocal chop, o il break.

    Ogni drum-fetta e' una COPIA del drum `base` (per ereditarne inviluppi e
    struttura -- un drum che funziona), con `fileName=path`, una `<zone>` a
    `[i*frames//n, (i+1)*frames//n]` (l'ultima fino a `frames`), e il REPEAT MODE
    `mode`.

    ⚠️ `mode='once'` (default) e' quello che usa lo **Slicer NATIVO del Deluge**:
    verificato copiando una fetta salvata dal dispositivo -- osc1 `loopMode=1`
    (ONCE) + `<zone>`, byte per byte come questa funzione produce. **ONCE suona la
    ZONA `[start,end]`** (la fetta), non tutto il file: e' la zona a delimitare.
    Quindi ogni innesco riproduce l'intera fetta, che e' cio' che serve al chop.
    (`mode='cut'` esiste -- la fetta si ferma con la nota -- ma non e' come slicea
    il Deluge.)

    `path` e' relativo alla SD (`SAMPLES/...`); `frames` da
    `audio.wav_frames(path_locale)[0]`. Riusabile per il break di jungle/DnB.
    Ritorna i nomi `['fetta 1', ...]`.
    """
    from . import song as S                                    # noqa: PLC0415
    if n < 1:
        raise ValueError('servono almeno 1 fetta')
    if mode not in LOOP_MODE:
        raise ValueError(f'mode {mode!r} sconosciuto, usare {sorted(LOOP_MODE)}')
    orig = S.drums(kit)
    if not 0 <= base < len(orig):
        raise ValueError(f'drum base {base} inesistente (ce ne sono {len(orig)})')
    n_orig = len(orig)
    modello = copy_drum(kit, base)                 # copia staccata
    # aggiungi N fette in fondo, poi togli gli n_orig originali dal fronte
    for i in range(n):
        add_drum(doc, kit, modello.copy_detached(), name=f'fetta {i + 1}')
    for _ in range(n_orig):
        remove_drum(doc, kit, 0)
    dur = frames // n
    fette = S.drums(kit)
    nomi = []
    for i in range(n):
        a = i * dur
        b = frames if i == n - 1 else (i + 1) * dur
        set_sample(fette[i], path, start=a, end=b)
        osc = fette[i].find('osc1')                # REPEAT MODE (ONCE = come lo Slicer)
        if osc is not None:
            osc.set('loopMode', str(LOOP_MODE[mode]))
        nomi.append(f'fetta {i + 1}')
    return nomi


def check_indices(doc: Document, kit: Node) -> list[str]:
    """Verifica l'invariante drum <-> noteRow. Vuoto se e' tutto a posto."""
    n = len(S.drums(kit))
    problemi = []
    for clip in kit_clips(doc, kit):
        idx = sorted(int(r.get('drumIndex')) for r in S.note_rows(clip)
                     if r.has('drumIndex'))
        if idx != list(range(len(idx))):
            problemi.append(f'clip "{S.clip_label(clip)}": indici non '
                            f'contigui da 0: {idx}')
        fuori = [i for i in idx if i >= n]
        if fuori:
            problemi.append(f'clip "{S.clip_label(clip)}": drumIndex {fuori} '
                            f'oltre i {n} drum del kit')
    return problemi
