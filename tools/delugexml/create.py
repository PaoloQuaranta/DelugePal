"""Creare strumenti e clip da zero, istanziando un preset.

IL FATTO CHE RENDE POSSIBILE TUTTO QUESTO
-----------------------------------------
Un file preset (`SYNTHS/*.XML`, `KITS/*.XML`) e il nodo strumento dentro la
song sono quasi lo stesso nodo. Misurato su `refs/synths/TEMPL.XML` contro
`refs/songs/TEMPL4.XML`: stesso tag, 8 attributi in comune, e differenze
sistematiche:

  - il preset porta `firmwareVersion` e `earliestCompatibleFirmware`,
    metadati di file: si tolgono
  - la song aggiunge attributi di ISTANZA: `presetName`, `presetFolder`,
    `colour`, `defaultVelocity`, `activeModFunction`, `isArmedForRecording`
  - `<defaultParams>` del preset diventa il `<soundParams>` DELLA CLIP
  - `<arpeggiator>` sta sullo strumento nel preset e sulla clip nella song

Quindi creare uno strumento non significa scrivere 778 attributi di suono:
significa istanziare un preset, che e' cio' che fa il dispositivo. I 778
attributi servono per MODIFICARE un suono, non per crearne uno.

LA FORMA DI UNA CLIP VUOTA
--------------------------
Presa da `refs/songs/TEMPL0.XML`, che e' una song nuova con una sola clip
vuota scritta dal dispositivo â€” non dedotta da clip piene di storia.

Da notare: una clip di SYNTH senza note **non ha affatto** il nodo
`<noteRows>` - le righe li sono altezze, e si aggiungono quando servono.

UNA CLIP DI KIT E' DIVERSA: LE RIGHE CI SONO GIA' TUTTE
--------------------------------------------------------
Sul Deluge un kit mostra sempre un drum per riga, non se ne aggiungono: lo sa
gia' `tools/dsong.py` (`row-add` su un kit rifiuta e rimanda a `note-add`).
Misurato sul corpus (139 file scritti dal dispositivo): **395 clip di kit su
395** hanno `drumIndex` contigui da 0, e **393 su 395** hanno esattamente una
riga per drum del kit (le due eccezioni sono `Drone 2.XML`, un file piu'
vecchio o modificato a mano). Una clip di kit senza righe e' uno stato che il
dispositivo non scrive mai: `add_track()` per un preset di kit crea quindi
una `<noteRow>` vuota per ciascun drum, indicizzate `0..N-1` - vedi
`_righe_per_ogni_drum`. Senza, chi aggiunge note a mano coi propri
`drumIndex` ottiene indici non contigui, che `musica.verifica()` rifiuta.
"""
from __future__ import annotations

from pathlib import Path

from .parser import Document, Node, parse_file
from . import song as S

#: Attributi che il preset porta come file e che non vanno dentro la song.
SOLO_FILE = ('firmwareVersion', 'earliestCompatibleFirmware')

#: Figli del preset che nella song vivono sulla CLIP, non sullo strumento.
FIGLI_DELLA_CLIP = ('defaultParams', 'arpeggiator')

#: Come si chiama sulla clip il `<defaultParams>` del preset, secondo il tipo.
#: E' il tag che DICHIARA il tipo della clip al caricatore del firmware, non
#: un'etichetta: sbagliarlo fa rifiutare il file. Vedi `instrument_from_preset`.
PARAMS_DELLA_CLIP = {'sound': 'soundParams', 'kit': 'kitParams'}

#: Attributi di istanza che la song aggiunge allo strumento, con i valori
#: osservati su strumenti scritti dal dispositivo.
ISTANZA_STRUMENTO = {
    'defaultVelocity': '100',
    # 0 e non 1: sugli STRUMENTI il dispositivo scrive sempre 0 — 356 <sound>
    # su 356 e 241 <kit> su 241. L'1 sta sulle CLIP, non qui, e scriverlo
    # faceva nascere armata per la registrazione ogni traccia generata.
    'isArmedForRecording': '0',
    # scelta fra i valori osservati, non una cattura: e' la funzione
    # selezionata sulle manopole, e varia (1 in 181 casi, 0 in 84, poi 3,4,7,5)
    'activeModFunction': '0',
    'colour': '0',
}

#: Attributi di una clip vuota, dai valori di TEMPL0. Quelli che dipendono
#: dall'istanza (preset, lunghezza, sezione, colore) vengono passati a parte.
CLIP_BASE = {
    'clipName': '',
    'inKeyMode': '1',
    'yScroll': '37',
    'yScrollKeyboard': '50',
    'isPlaying': '0',
    'isSoloing': '0',
    'isArmedForRecording': '1',
    'keyboardLayout': '0',
    'keyboardRowInterval': '5',
    'drumsScrollOffset': '0',
    'drumsZoomLevel': '8',
    'inKeyScrollOffset': '21',
    'inKeyRowInterval': '3',
}

#: Una clip di kit porta `affectEntire` e una di synth no: nel corpus e' su
#: 395 clip kit su 395 e su 0 clip synth su 551, quindi e' la discriminante.
#: Serve anche a `song.is_kit_clip()`, che senza righe non ha altro su cui
#: decidere — e una clip appena creata non ha righe.
#: Va subito dopo `yScrollKeyboard` (358 casi su 395) e vale '0' per default.
KIT_AFFECT_ENTIRE = ('affectEntire', '0')


def _senza(node: Node, chiavi) -> None:
    node.attrs = [(k, v) for k, v in node.attrs if k not in chiavi]
    node.dirty = True


def _colonne_default() -> Node:
    """<columnControls>, presente su ogni clip scritta dal dispositivo."""
    return Node(tag='columnControls', children=[
        Node(tag='leftCol', attrs=[('type', 'velocity')], self_closing=True),
        Node(tag='rightCol', attrs=[('type', 'mod')], self_closing=True),
    ])


def _righe_per_ogni_drum(clip: Node, kit_inst: Node) -> None:
    """Una `<noteRow drumIndex="i">` vuota per ciascun drum del kit, `0..N-1`.

    Niente `<soundParams>` sulla riga. Decisione presa su due fatti misurati,
    non supposti, e in conflitto fra loro:

      - nel corpus le righe di kit portano `soundParams` quasi sempre
        (7495 casi su 7513: un'abitudine di come il dispositivo SALVA, dopo
        che l'utente ha toccato quella riga);
      - ma e' gia' stato verificato SUL DISPOSITIVO che una clip di kit
        funziona anche senza (`SCENE2.XML`, `docs/FINDINGS.md`, sezione
        6-quinquies, "Cosa invece NON serve").

    Fra un'abitudine di scrittura osservata e una prova di caricamento sul
    dispositivo, vince la prova di caricamento: e' la stessa gerarchia che
    l'HANDOFF mette al primo posto ("solo il dispositivo dice se funziona").
    Aggiungere qui `soundParams` copiati da `defaultParams` (come fa
    `kit.add_drum`, per un drum aggiunto a un kit gia' in uso) introdurrebbe
    778 attributi per drum non richiesti da CREARE la clip, replicando per
    ogni drum l'errore concettuale che il modulo doc gia' segnala altrove:
    non serve scrivere l'attrezzatura completa di un suono per farlo esistere.
    """
    for i in range(len(S.drums(kit_inst))):
        S.add_note_row(clip, i)


def instrument_from_preset(preset: Document | Path | str, *, name: str,
                           folder: str) -> tuple[Node, Node | None, Node | None]:
    """Trasforma un preset in un nodo strumento pronto per `<instruments>`.

    Ritorna (strumento, params_per_la_clip, arpeggiator_per_la_clip): i due
    ultimi vanno sulla clip, non sullo strumento.
    """
    doc = preset if isinstance(preset, Document) else parse_file(Path(preset))
    inst = doc.root.copy_detached()   # da un ALTRO file: gli span non valgono qui
    if inst.tag not in ('sound', 'kit'):
        raise ValueError(f'un preset ha radice <sound> o <kit>, non <{inst.tag}>')

    _senza(inst, SOLO_FILE)

    # i due figli che nella song vivono sulla clip
    params = arp = None
    restanti = []
    for figlio in inst.children:
        if figlio.tag == 'defaultParams':
            params = figlio.copy_detached()
            # Il nome NON e' cosmetico: dichiara al caricatore il tipo della
            # clip. Dal firmware (`instrument_clip.cpp`):
            #     else if (!strcmp(tagName, "soundParams")) {
            #         outputTypeWhileLoading = OutputType::SYNTH;
            # Mettere `soundParams` su una clip di kit le fa dire "sono un
            # synth", e poi le sue righe hanno `drumIndex` e lo strumento e'
            # un <kit>: il Deluge rifiuta il file come corrotto.
            # Nel corpus: kitParams su 395 clip di kit su 395.
            params.tag = PARAMS_DELLA_CLIP[inst.tag]
            params.dirty = True
        elif figlio.tag == 'arpeggiator':
            arp = figlio.copy_detached()
        else:
            restanti.append(figlio)
    inst.children = restanti

    for k, v in ISTANZA_STRUMENTO.items():
        if not inst.has(k):
            inst.set(k, v)
    inst.set('presetName', name)
    inst.set('presetFolder', folder)
    return inst, params, arp


def add_track(doc: Document, preset: Document | Path | str, *, name: str,
              folder: str, length: int = 384, section: str = '0',
              colour_offset: str = '0', playing: bool = False) -> tuple[Node, Node]:
    """Aggiunge alla song uno strumento istanziato dal preset e una clip che
    lo suona. Ritorna (strumento, clip).

    Aggiorna anche gli scroll delle due viste e `beingEdited`: senza, la roba
    esiste e non si vede â€” tre volte su tre e' stato quello il problema.
    """
    inst, params, arp = instrument_from_preset(preset, name=name, folder=folder)

    strumenti = doc.root.find('instruments')
    if strumenti is None:
        raise ValueError('la song non ha <instruments>')
    strumenti.append(inst)

    attrs = {}
    for k, v in CLIP_BASE.items():
        attrs[k] = v
        # senza `affectEntire` la clip non e' riconoscibile come clip di kit
        # finche' non ha righe, e una clip appena creata non ne ha: `is_kit_clip`
        # ricadrebbe sul ramo synth e `note-add --drum` fallirebbe
        if k == 'yScrollKeyboard' and inst.tag == 'kit':
            attrs[KIT_AFFECT_ENTIRE[0]] = KIT_AFFECT_ENTIRE[1]
    attrs.update({
        'instrumentPresetName': name,
        'instrumentPresetFolder': folder,
        'length': str(length),
        'colourOffset': str(colour_offset),
        'section': str(section),
        'isPlaying': '1' if playing else '0',
    })
    clip = Node(tag='instrumentClip', attrs=list(attrs.items()))
    if arp is not None:
        clip.append(arp)
    if params is not None:
        clip.append(params)
    clip.append(_colonne_default())
    if inst.tag == 'kit':
        _righe_per_ogni_drum(clip, inst)
    # altrimenti niente <noteRows>: una clip di synth vuota non lo porta

    contenitore = doc.root.find('sessionClips')
    if contenitore is None:
        raise ValueError('la song non ha <sessionClips>')
    contenitore.append(clip)

    # far sÃ¬ che si veda: righe di song view = clip, dell'arranger = strumenti
    S.scroll_song_view_to(doc, len(contenitore.children) - 1)
    S.scroll_arrangement_view_to(doc, len(strumenti.children) - 1)
    S.set_edited_clip(doc, clip)
    return inst, clip

