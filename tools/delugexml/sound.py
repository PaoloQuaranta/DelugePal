"""Accesso ai parametri di suono per nome, nelle unita' del display.

DOVE STANNO I PARAMETRI
-----------------------
Misurato sullo schema del corpus: i valori scalabili (esadecimali a 32 bit)
stanno in pochi contenitori ben precisi, non sparsi ovunque.

    clip di synth   <instrumentClip>/<soundParams>          56 attributi
    clip di kit     <instrumentClip>/<kitParams>            31
    riga di kit     <noteRow>/<soundParams>                 55  (per drum)
    clip audio      <audioClip>/<params>                    32
    livello song    <song>/<songParams>                     31

piu' i figli di quei contenitori: <envelope1..4> (attack, decay, sustain,
release), <equalizer> (bass, treble e le loro frequenze), <patchCables>.

Il resto — 776 attributi su 1442 — e' STRUTTURA, non valori: tipi di
oscillatore, forme d'onda, modalita' di filtro, impostazioni di arpeggiatore.
Sta sui nodi dello strumento e non passa da qui.

LE UNITA'
---------
Tutto viene esposto come lo mostra il dispositivo, 0-50. La conversione e in
`params.py`, insieme alla griglia interna a 128 per chi vuole piena
risoluzione. Confermato dalla documentazione community, che descrive la
griglia dell'automazione come «value ranges (0-128, displayed as 0-50 for
consistency)».

QUANDO UN PARAMETRO E' AUTOMATIZZATO
------------------------------------
L'attributo non contiene piu' un valore ma una sequenza. `get()` lo dice
invece di restituire un numero inventato: un'automazione letta come numero e'
un errore silenzioso, ed e' gia' costato tempo in questo progetto.
"""
from __future__ import annotations

from .parser import Document, Node
from . import params as P
from . import automation as A

#: I contenitori di valori, in ordine di ricerca.
#:
#: `defaultParams` sta in fondo ed e' arrivato dopo: e' il contenitore di un
#: PRESET (`refs/synths/TEMPL.XML`) e di un DRUM dentro `<soundSources>`.
#: Senza, progettare il suono di un drum era impossibile — `container()`
#: restituiva None e `set()` non trovava nulla su cui lavorare. Sta in fondo
#: perche' un nodo che ha gia' un `soundParams` deve continuare a rispondere
#: con quello.
CONTENITORI = ('soundParams', 'kitParams', 'params', 'songParams',
               'defaultParams')

#: Figli di un contenitore che portano a loro volta valori.
FIGLI_CON_VALORI = ('envelope1', 'envelope2', 'envelope3', 'envelope4',
                    'equalizer', 'lpf', 'hpf', 'delay')


class Automatizzato(ValueError):
    """Il parametro non ha un valore singolo: e' un'automazione."""


def container(node: Node) -> Node | None:
    """Il contenitore di parametri di un nodo (clip, song, noteRow)."""
    for tag in CONTENITORI:
        c = node.find(tag)
        if c is not None:
            return c
    return None


def _cerca(cont: Node, name: str) -> tuple[Node, str] | None:
    """(nodo, attributo) dove vive `name`, cercando anche nei figli."""
    if cont.has(name):
        return cont, name
    for figlio in cont.children:
        if figlio.tag in FIGLI_CON_VALORI and figlio.has(name):
            return figlio, name
    # forma "envelope1.attack" per disambiguare fra i quattro inviluppi
    if '.' in name:
        tag, attr = name.split('.', 1)
        figlio = cont.find(tag)
        if figlio is not None and figlio.has(attr):
            return figlio, attr
    return None


def names(node: Node) -> list[str]:
    """Tutti i parametri di questo nodo, ordinati.

    I nomi dei figli vengono qualificati (`envelope1.attack`) perche' i
    quattro inviluppi usano gli stessi quattro nomi: senza prefisso si
    scriverebbe sul primo credendo di scrivere sul terzo.
    """
    cont = container(node)
    if cont is None:
        return []
    out = [k for k, v in cont.attrs
           if isinstance(v, str) and v.startswith('0x')]
    for figlio in cont.children:
        if figlio.tag in FIGLI_CON_VALORI:
            out += [f'{figlio.tag}.{k}' for k, v in figlio.attrs
                    if isinstance(v, str) and v.startswith('0x')]
    return sorted(out)


def get(node: Node, name: str) -> int | None:
    """Il valore 0-50 del parametro, o None se non e' sulla griglia.

    Solleva `Automatizzato` se il parametro varia nel tempo: in quel caso
    usa `automation.decode()` sul valore grezzo.
    """
    grezzo = get_raw(node, name)
    if grezzo is None:
        return None
    if A.is_automation(grezzo):
        raise Automatizzato(
            f'"{name}" e automatizzato: non ha un valore singolo. '
            'Usa get_raw() e automation.decode().')
    return P.to_display(grezzo)


def get_raw(node: Node, name: str) -> str | None:
    """Il valore esadecimale grezzo, automazioni comprese."""
    cont = container(node)
    if cont is None:
        return None
    trovato = _cerca(cont, name)
    return trovato[0].get(trovato[1]) if trovato else None


def set(node: Node, name: str, display: int) -> str:  # noqa: A001
    """Imposta il parametro nelle unita' del display (0-50).

    Ritorna l'esadecimale scritto. Un parametro che non esiste e' un errore,
    con l'elenco di quelli disponibili: sbagliare nome e ottenere silenzio
    sarebbe peggio.
    """
    cont = container(node)
    if cont is None:
        raise ValueError(f'<{node.tag}> non ha un contenitore di parametri '
                         f'({", ".join(CONTENITORI)})')
    trovato = _cerca(cont, name)
    if trovato is None:
        disponibili = ', '.join(names(node)[:12])
        raise ValueError(f'parametro "{name}" inesistente qui. '
                         f'Alcuni disponibili: {disponibili}…')
    bersaglio, attr = trovato
    valore = P.from_display(display)
    bersaglio.set(attr, valore)
    return valore


def set_raw(node: Node, name: str, hexval: str) -> None:
    """Scrive il valore grezzo, per automazioni o piena risoluzione."""
    cont = container(node)
    trovato = _cerca(cont, name) if cont else None
    if trovato is None:
        raise ValueError(f'parametro "{name}" inesistente qui')
    trovato[0].set(trovato[1], hexval)


# ------------------------------------------------------------- patch cable
#
# PERCHE' QUESTO NON E' UN CANCELLO SUL CORPUS
# --------------------------------------------
# `structure.py` rifiuta i valori mai osservati, e li' ha senso: sono
# enumerazioni corte (7 modalita' di filtro, 3 modi di sintesi) dove il corpus
# le esaurisce. Qui no. Le combinazioni sorgente-destinazione possibili sono
# centinaia e nel corpus se ne vedono **148**: l'assenza di una coppia dice
# quasi sempre che l'utente non l'ha usata, non che il firmware la rifiuti.
# Prendere il corpus per specifica avrebbe reso impossibile mezzo sound design.
#
# Quindi l'autorita' e' un'altra, ed e' doppia:
#   - le SORGENTI vengono dalla matrice del capitolo Modulation del guidebook
#     (ARCHITETTURA.md §9b) piu' le aggiunte community (LFO 3-4, ENV 3-4);
#   - le DESTINAZIONI si derivano da `param_ids.py`, cioe' dall'enum di
#     `param.h` del firmware, filtrando i parametri PATCHED.
# Il corpus resta come **informazione**: il rapporto dice quante volte quella
# coppia e' stata vista, cosi' chi legge sa se sta su terreno battuto.

#: Le sorgenti di modulazione [MAN]. Il nome che non coincide: quella che il
#: manuale chiama SIDECHAIN nell'XML si scrive `compressor`.
#: `envelope3`/`envelope4` non compaiono in nessuno dei 16 056 patch cable del
#: corpus — e non e' una ragione per rifiutarli, il firmware community ha
#: quattro inviluppi e quattro LFO.
SORGENTI = ('compressor', 'lfo1', 'lfo2', 'lfo3', 'lfo4',
            'envelope1', 'envelope2', 'envelope3', 'envelope4',
            'velocity', 'note', 'random', 'aftertouch', 'x', 'y')

#: Le due sorgenti che il manuale dichiara **globali al suono**; tutte le
#: altre sono per voce.
SORGENTI_GLOBALI = ('compressor', 'lfo1')

#: I parametri che il manuale dichiara globali al suono: accettano **solo** una
#: sorgente globale. Modularli con LFO2 o un inviluppo non produce un errore,
#: produce silenzio — la stessa famiglia di guai di `lpfMode="Off"`.
DEST_GLOBALI = ('delayRate', 'delayFeedback', 'modFXRate', 'modFXDepth',
                'reverbAmount', 'arpeggiatorRate', 'lfo1Rate', 'lfo2Rate',
                'volumePostFX', 'volumePostReverbSend')

#: I patch cable usano un vocabolario **diverso** da quello degli attributi di
#: `<soundParams>`, e confonderli e' un errore silenzioso: come attributo il
#: parametro si chiama `modulator1Amount`, come destinazione di un cable
#: `modulator1Volume`. Gli inviluppi sono il caso piu' netto — come attributi
#: sono figli (`<envelope1 attack="…">`), come destinazioni sono nomi piatti
#: (`env1Attack`). Questa mappa copre le voci dell'enum che `param_ids._NOMI`
#: lascia a None oppure nomina secondo l'altro vocabolario.
_DEST_DA_ENUM = {
    'LOCAL_MODULATOR_0_VOLUME': 'modulator1Volume',
    'LOCAL_MODULATOR_1_VOLUME': 'modulator2Volume',
    'LOCAL_OSC_A_PHASE_WIDTH': 'oscAPhaseWidth',
    'LOCAL_OSC_B_PHASE_WIDTH': 'oscBPhaseWidth',
    'LOCAL_OSC_A_PITCH_ADJUST': 'oscAPitch',
    'LOCAL_OSC_B_PITCH_ADJUST': 'oscBPitch',
    'LOCAL_MODULATOR_0_PITCH_ADJUST': 'modulator1Pitch',
    'LOCAL_MODULATOR_1_PITCH_ADJUST': 'modulator2Pitch',
}

#: `range` compare 13 volte nel corpus come destinazione e non sta nell'enum
#: dei PATCHED: e' quasi certamente una destinazione di espressione (MPE).
#: Sta qui perche' esiste nei file, non perche' si sia capita.
_DEST_EXTRA = ('range',)


def _nomi_inviluppi() -> list[str]:
    """`env1Attack` … `env4Release`, generati e non trascritti.

    L'enum del firmware numera gli inviluppi da 0 (`LOCAL_ENV_0_ATTACK`) e le
    destinazioni da 1 (`env1Attack`): lo scarto e' proprio qui, e scriverlo a
    mano sedici volte sarebbe stato sedici occasioni di sbagliarlo.
    """
    return [f'env{i}{stadio}'
            for i in range(1, 5)
            for stadio in ('Attack', 'Decay', 'Sustain', 'Release')]


def destinazioni_disponibili() -> list[str]:
    """Le destinazioni di un patch cable, dall'enum del firmware.

    Derivate da `param_ids.PARAMETRI` filtrando i PATCHED, tradotte nel
    vocabolario dei cable, piu' gli inviluppi e le extra osservate.

    ⚠ Qui dentro NON si usa il builtin `set`: questo modulo definisce una
    funzione `set(node, name, display)` che lo oscura, e chiamarlo da' un
    `TypeError` che sembra venire da tutt'altra parte. Si deduplica con un
    dict, che conserva anche l'ordine.
    """
    from . import param_ids as PI                      # noqa: PLC0415
    fuori: dict[str, None] = {}
    for p in PI.PARAMETRI:
        if p.kind != PI.KIND_PATCHED:
            continue
        nome = _DEST_DA_ENUM.get(p.enum, p.nome)
        if nome:
            fuori[nome] = None
    for nome in (*_nomi_inviluppi(), *_DEST_EXTRA):
        fuori[nome] = None
    return sorted(fuori)


def _contenitore_cavi(node: Node, *, create: bool = False) -> Node | None:
    """Il `<patchCables>` dentro il contenitore di parametri."""
    cont = container(node)
    if cont is None:
        if not create:
            return None
        raise ValueError(
            f'<{node.tag}> non ha un contenitore di parametri '
            f'({", ".join(CONTENITORI)}): non e un nodo su cui esistano cable')
    cavi = cont.find('patchCables')
    if cavi is None and create:
        cont.self_closing = False
        cavi = cont.append(Node(tag='patchCables'))
    return cavi


def patch_cables(node: Node) -> list[dict[str, object]]:
    """I patch cable di questo nodo, con l'amount nelle unita' del display.

    `amount` e' un float e non un intero: la risoluzione interna e' molto piu'
    fine dello schermo, e solo lo 0,67% dei valori del corpus corrisponde a un
    display intero (FINDINGS §6). Arrotondare qui darebbe un numero pulito e
    falso. `None` se il cable e' automatizzato.
    """
    cavi = _contenitore_cavi(node)
    if cavi is None:
        return []
    fuori = []
    for c in cavi.children:
        if c.tag != 'patchCable':
            continue
        grezzo = c.get('amount') or ''
        fuori.append({
            'source': c.get('source'),
            'destination': c.get('destination'),
            'amount': None if A.is_automation(grezzo)
                      else P.cable_to_display(grezzo),
            'automatizzato': A.is_automation(grezzo),
            'nodo': c,
        })
    return fuori


def set_patch_cable(node: Node, source: str, destination: str,
                    amount: float, *, force: bool = False) -> dict[str, object]:
    """Crea o aggiorna un patch cable. `amount` in unita' display, −50…+50.

    Ritorna un rapporto di cosa e' stato fatto, come `musica.applica_verbo`:
    un'operazione di sound design silenziosa non e' correggibile.

    Il rapporto porta due segnalazioni che **non bloccano**:

    `mai_visto`   la coppia non compare nel corpus. Non e' un difetto: il
                  corpus dice cosa l'utente ha suonato, non cosa il firmware
                  accetta. E' solo un avviso che si e' fuori dal battuto.
    `inefficace`  la destinazione e' globale al suono e la sorgente non lo e'.
                  Il manuale dice che quei parametri accettano solo Sidechain
                  e LFO1; scrivere altro non da' errore, da' silenzio.

    `polarity` NON viene scritto. Nei file e' assente in 11 466 cable su
    16 056, e cosa significhi davvero resta ignoto — il solo esemplare
    misurato si dichiarava `unipolar` mentre il dispositivo mostrava un range
    bipolare (FINDINGS §6). Non si scrive in un attributo che non si e' capito.
    """
    if not force:
        if source not in SORGENTI:
            raise ValueError(
                f'"{source}" non e una sorgente di modulazione. '
                f'Sono: {", ".join(SORGENTI)}. '
                'Usa force=True se vuoi provarla lo stesso.')
        ammesse = destinazioni_disponibili()
        if destination not in ammesse:
            raise ValueError(
                f'"{destination}" non e fra i parametri modulabili del '
                f'firmware. Alcuni: {", ".join(ammesse[:14])}… '
                'Usa force=True per esplorare.')
    if not -P.CABLE_DISPLAY_MAX <= amount <= P.CABLE_DISPLAY_MAX:
        raise ValueError(
            f'amount {amount} fuori scala: i patch cable vanno da '
            f'−{P.CABLE_DISPLAY_MAX} a +{P.CABLE_DISPLAY_MAX}')

    cavi = _contenitore_cavi(node, create=True)
    esistente = None
    for c in cavi.children:
        if (c.tag == 'patchCable' and c.get('source') == source
                and c.get('destination') == destination):
            esistente = c
            break

    grezzo = P.cable_from_display(amount)
    if esistente is None:
        esistente = cavi.append(Node(
            tag='patchCable',
            attrs=[('source', source), ('destination', destination),
                   ('amount', grezzo)],
            self_closing=True))
        azione = 'creato'
        prima = None
    else:
        vecchio = esistente.get('amount') or ''
        prima = (None if A.is_automation(vecchio)
                 else P.cable_to_display(vecchio))
        esistente.set('amount', grezzo)
        azione = 'aggiornato'

    globale_ok = (destination not in DEST_GLOBALI
                  or source in SORGENTI_GLOBALI)
    return {
        'azione': azione,
        'source': source,
        'destination': destination,
        'da': prima,
        'a': amount,
        'grezzo': grezzo,
        'visto_nel_corpus': COPPIE_OSSERVATE.get((source, destination), 0),
        'mai_visto': (source, destination) not in COPPIE_OSSERVATE,
        'inefficace': not globale_ok,
        'nodo': esistente,
    }


def remove_patch_cable(node: Node, source: str, destination: str) -> bool:
    """Toglie un patch cable. True se c'era."""
    cavi = _contenitore_cavi(node)
    if cavi is None:
        return False
    tenuti = [c for c in cavi.children
              if not (c.tag == 'patchCable' and c.get('source') == source
                      and c.get('destination') == destination)]
    if len(tenuti) == len(cavi.children):
        return False
    cavi.children = tenuti
    cavi.touch()
    return True


#: Le coppie sorgente-destinazione **osservate**, col numero di volte. NON e'
#: una specifica: e' il grado di battutezza di un percorso, usato solo per
#: informare nel rapporto di `set_patch_cable`. Generata dal corpus (162 file,
#: 16 056 cable) e ricontrollata da `test_patch_cable_tabelle`.
COPPIE_OSSERVATE: dict[tuple[str, str], int] = {
    ('velocity', 'volume'): 8100, ('aftertouch', 'volume'): 3082,
    ('y', 'lpfFrequency'): 3009, ('lfo1', 'pitch'): 175,
    ('envelope2', 'lpfFrequency'): 156, ('velocity', 'lpfFrequency'): 129,
    ('compressor', 'volumePostReverbSend'): 122, ('note', 'lpfFrequency'): 93,
    ('y', 'modulator1Volume'): 73, ('velocity', 'oscAVolume'): 63,
    ('velocity', 'oscBVolume'): 62, ('envelope1', 'lpfFrequency'): 60,
    ('note', 'volume'): 56, ('envelope2', 'carrier1Feedback'): 54,
    ('random', 'pan'): 47, ('random', 'pitch'): 44,
    ('envelope1', 'carrier1Feedback'): 40, ('envelope2', 'carrier2Feedback'): 40,
    ('envelope2', 'modulator2Volume'): 31, ('lfo1', 'delayRate'): 30,
    ('envelope2', 'modulator1Volume'): 28, ('note', 'modulator1Volume'): 26,
    ('lfo2', 'oscAPhaseWidth'): 26, ('random', 'oscBVolume'): 22,
    ('random', 'oscAPhaseWidth'): 22, ('lfo2', 'lpfFrequency'): 19,
    ('lfo1', 'hpfFrequency'): 18, ('envelope2', 'hpfFrequency'): 16,
    ('lfo2', 'oscBVolume'): 15, ('random', 'lpfResonance'): 14,
    ('note', 'modulator2Volume'): 13, ('random', 'lpfFrequency'): 13,
    ('lfo1', 'lfo2Rate'): 13, ('lfo2', 'oscAWavetablePosition'): 12,
    ('envelope2', 'oscBPitch'): 12, ('lfo1', 'lpfFrequency'): 12,
    ('lfo1', 'modulator1Volume'): 9, ('lfo1', 'oscBPitch'): 9,
    ('random', 'carrier1Feedback'): 9, ('random', 'env2Attack'): 9,
    ('envelope2', 'noiseVolume'): 8, ('lfo2', 'oscBPhaseWidth'): 8,
    ('lfo2', 'range'): 8, ('lfo2', 'env2Attack'): 7,
    ('envelope2', 'oscBVolume'): 6, ('random', 'env2Decay'): 6,
    ('lfo1', 'oscAPhaseWidth'): 6, ('velocity', 'pitch'): 6,
    ('lfo1', 'lpfResonance'): 5, ('envelope2', 'oscAPhaseWidth'): 5,
    ('envelope2', 'lpfResonance'): 5, ('lfo2', 'oscBPitch'): 5,
    ('note', 'lfo2Rate'): 5, ('lfo2', 'oscAVolume'): 5,
    ('random', 'oscBPitch'): 5, ('random', 'oscAPitch'): 5,
    ('envelope2', 'env1Decay'): 5, ('envelope2', 'modulator1Feedback'): 4,
    ('lfo2', 'lpfResonance'): 4, ('note', 'hpfFrequency'): 4,
    ('envelope2', 'waveFold'): 4, ('envelope2', 'modulator1Pitch'): 4,
    ('envelope1', 'oscBVolume'): 4, ('note', 'oscBVolume'): 4,
    ('envelope2', 'oscAPitch'): 4, ('envelope1', 'oscAVolume'): 4,
    ('envelope1', 'modulator2Volume'): 4, ('envelope2', 'range'): 4,
    ('lfo1', 'oscAVolume'): 4, ('envelope2', 'env2Attack'): 3,
    ('aftertouch', 'lpfFrequency'): 3, ('envelope1', 'env1Decay'): 3,
    ('velocity', 'modulator1Volume'): 3, ('envelope2', 'modulator2Feedback'): 3,
    ('random', 'lpfMorph'): 3, ('compressor', 'lpfFrequency'): 3,
    ('envelope1', 'modulator1Volume'): 3, ('random', 'carrier2Feedback'): 3,
    ('lfo1', 'pan'): 2, ('envelope1', 'env1Attack'): 2,
    ('envelope1', 'oscBPitch'): 2, ('lfo1', 'env1Sustain'): 2,
    ('envelope1', 'oscBPhaseWidth'): 2, ('random', 'lfo2Rate'): 2,
    ('lfo1', 'volume'): 2, ('envelope1', 'lpfResonance'): 2,
    ('lfo2', 'pitch'): 2, ('lfo1', 'modulator2Volume'): 2,
    ('note', 'lpfResonance'): 2, ('lfo1', 'noiseVolume'): 2,
    ('envelope1', 'oscAPhaseWidth'): 1, ('lfo1', 'oscAPitch'): 1,
    ('lfo1', 'carrier2Feedback'): 1, ('x', 'lpfFrequency'): 1,
    ('lfo4', 'lfo2Rate'): 1, ('y', 'hpfFrequency'): 1,
    ('lfo3', 'hpfResonance'): 1, ('lfo2', 'waveFold'): 1,
    ('velocity', 'lpfResonance'): 1, ('note', 'noiseVolume'): 1,
    ('note', 'modulator1Pitch'): 1, ('velocity', 'modulator1Pitch'): 1,
    ('note', 'modulator2Feedback'): 1, ('note', 'modulator1Feedback'): 1,
    ('random', 'noiseVolume'): 1, ('velocity', 'env1Release'): 1,
    ('lfo1', 'modFXRate'): 1, ('lfo2', 'carrier2Feedback'): 1,
    ('lfo2', 'carrier1Feedback'): 1, ('lfo2', 'oscAPitch'): 1,
    ('lfo3', 'lpfFrequency'): 1, ('y', 'waveFold'): 1,
    ('envelope1', 'hpfResonance'): 1, ('envelope1', 'hpfFrequency'): 1,
    ('lfo2', 'modulator2Volume'): 1, ('lfo1', 'oscBVolume'): 1,
    ('envelope2', 'pitch'): 1, ('lfo1', 'modFXDepth'): 1,
    ('random', 'oscBPhaseWidth'): 1, ('velocity', 'lfo2Rate'): 1,
    ('envelope2', 'lfo2Rate'): 1, ('velocity', 'modulator1Feedback'): 1,
    ('lfo2', 'modulator1Pitch'): 1, ('envelope1', 'modulator1Feedback'): 1,
    ('lfo2', 'hpfResonance'): 1, ('lfo2', 'pan'): 1,
    ('lfo2', 'noiseVolume'): 1, ('lfo1', 'env2Attack'): 1,
    ('lfo1', 'oscBPhaseWidth'): 1, ('envelope1', 'oscAPitch'): 1,
    ('envelope1', 'range'): 1, ('velocity', 'modulator2Volume'): 1,
    ('note', 'oscBPitch'): 1, ('velocity', 'oscBPitch'): 1,
    ('compressor', 'oscBPitch'): 1, ('compressor', 'oscAPitch'): 1,
    ('compressor', 'lpfResonance'): 1, ('random', 'env2Sustain'): 1,
    ('envelope2', 'oscBPhaseWidth'): 1, ('random', 'modulator1Feedback'): 1,
    ('random', 'env1Decay'): 1,
}


def read_all(node: Node) -> dict[str, int | str | None]:
    """Tutti i parametri: valore 0-50, oppure 'automatizzato', oppure None."""
    cont = container(node)
    if cont is None:
        return {}
    out: dict[str, int | str | None] = {}
    sorgenti = [(None, cont)] + [(c.tag, c) for c in cont.children
                                 if c.tag in FIGLI_CON_VALORI]
    for prefisso, nodo in sorgenti:
        for k, v in nodo.attrs:
            chiave = k if prefisso is None else f'{prefisso}.{k}'
            if not (isinstance(v, str) and v.startswith('0x')):
                continue
            out[chiave] = 'automatizzato' if A.is_automation(v) \
                else P.to_display(v)
    return out
