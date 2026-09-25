"""La struttura del suono: cosa non passa dalla scala 0-50.

Sui 1442 attributi del formato, 776 non sono valori modulabili ma STRUTTURA:
tipo di sintesi, forme d'onda, modalita' di filtro, unisono, arpeggiatore.
Stanno sui nodi dello strumento, non nei contenitori di parametri.

PERCHE' UN ELENCO DI VALORI AMMESSI
-----------------------------------
Sono enumerazioni, e un valore inventato non produce un errore: produce un
file che il dispositivo interpreta a modo suo. Qui si accettano solo i valori
**osservati in file reali** oppure confermati dal firmware (FIRMWARE),
con le due fonti mantenute distinte. Chi vuole
scriverne uno mai visto deve dirlo esplicitamente (`force=True`), e sa di
essere fuori dal terreno verificato.

Osservati su `refs/` piu' `corpus_versions/`, cioe' 144 file di 17 versioni
di firmware.

IL CASO CHE HA MOTIVATO QUESTO MODULO
--------------------------------------
Una patch FM commerciale aveva `lpfMode="Off"`: cambiare `lpfFrequency` e
`lpfResonance` non produceva nessun effetto, perche' il filtro era spento a
monte. Non era una limitazione della sintesi FM — portando `lpfMode` a
`"24dB"` il filtro si sente, **verificato sul dispositivo**. I valori di
struttura decidono se i valori modulabili contano qualcosa.
"""
from __future__ import annotations

from .parser import Node

#: (tag, attributo) -> valori osservati, con quante volte. Il primo e' il piu'
#: frequente, cioe' il "normale".
OSSERVATI: dict[tuple[str, str], dict[str, int]] = {
    ('sound', 'mode'):        {'subtractive': 4100, 'fm': 63, 'ringmod': 8},
    ('sound', 'lpfMode'):     {'24dB': 3968, '12dB': 119, '24dBDrive': 35,
                               'Off': 32, 'flanger': 10, 'SVF_Band': 6,
                               'SVF_Notch': 1},
    ('sound', 'hpfMode'):     {'HPLadder': 1600, 'Off': 32, 'flanger': 10,
                               'SVF_Notch': 1, 'SVF_Band': 1},
    ('sound', 'polyphonic'):  {'auto': 3495, 'poly': 372, 'choke': 259,
                               'legato': 23, 'mono': 22},
    ('sound', 'modFXType'):   {'none': 4131, 'phaser': 15, 'flanger': 10,
                               'chorus': 9, 'StereoChorus': 4, 'grainFX': 2},
    ('kit', 'lpfMode'):       {'24dB': 239, '24dBDrive': 4, '12dB': 1},
    ('kit', 'modFXType'):     {'flanger': 184, 'none': 60},
    ('osc1', 'type'):         {'sample': 3904, 'saw': 64, 'square': 56,
                               'sine': 23, 'analogSquare': 16,
                               'wavetable': 14, 'analogSaw': 9,
                               'triangle': 7, 'inLeft': 4},
    ('osc2', 'type'):         {'sample': 3780, 'square': 217, 'saw': 37,
                               'sine': 28, 'analogSquare': 17, 'triangle': 16,
                               'analogSaw': 5, 'wavetable': 4, 'inStereo': 4},
    ('lfo1', 'type'):         {'sine': 2093, 'triangle': 2070, 'saw': 3,
                               'square': 3, 'rwalk': 2},
    ('lfo2', 'type'):         {'sine': 2092, 'triangle': 2070, 'saw': 6,
                               'square': 2, 'rwalk': 1},
    ('arpeggiator', 'mode'):  {'off': 4178, 'arp': 15, 'up': 4},
}

#: attributi numerici, con l'intervallo osservato
INTERVALLI: dict[tuple[str, str], tuple[int, int]] = {
    ('unison', 'num'):    (1, 8),
    ('unison', 'detune'): (0, 50),
    ('unison', 'spread'): (0, 50),
    ('sound', 'maxVoices'): (8, 8),
}

#: Build 2d7cdf8: model/mod_controllable/filters/filter_config.cpp.
#: I modi disponibili per ciascuno slot sono documentati nei menu community.
#: Non sono conteggi di osservazioni; flanger e' un vecchio valore del corpus,
#: assente dalla mappa della build corrente, e richiede force=True.
FIRMWARE = {
    (tag, attr): values
    for tag in ('sound', 'kit')
    for attr, values in (
        ('filterRoute', ('H2L', 'L2H', 'PARA')),
        ('lpfMode', ('12dB', '24dB', '24dBDrive', 'SVF_Band', 'SVF_Notch', 'Off')),
        ('hpfMode', ('HPLadder', 'SVF_Band', 'SVF_Notch', 'Off')),
    )
}
SOLO_UN_VALORE = {}


def valori_ammessi(tag: str, attr: str) -> list[str]:
    """Valori confermati dal firmware, oppure osservati nel corpus."""
    if (tag, attr) in FIRMWARE:
        return list(FIRMWARE[(tag, attr)])
    d = OSSERVATI.get((tag, attr))
    if d:
        return list(d)
    if (tag, attr) in SOLO_UN_VALORE:
        return [SOLO_UN_VALORE[(tag, attr)]]
    r = INTERVALLI.get((tag, attr))
    return [f'{r[0]}..{r[1]}'] if r else []


def set_attr(node: Node, attr: str, value, *, force: bool = False) -> str:
    """Imposta un attributo di struttura, verificando che il valore esista.

    `force=True` scrive comunque: serve per esplorare valori che il firmware
    potrebbe accettare ma che nessun file del corpus mostra. In quel caso si
    e' fuori dal terreno verificato, e va detto.
    """
    v = str(value)
    chiave = (node.tag, attr)
    if not force:
        enum = FIRMWARE.get(chiave, OSSERVATI.get(chiave))
        if enum is not None and v not in enum:
            raise ValueError(
                f'<{node.tag} {attr}="{v}"> non supportato. '
                f'Valori ammessi: {", ".join(enum)}. '
                'Usa force=True se vuoi provarlo lo stesso.')
        limiti = INTERVALLI.get(chiave)
        if limiti is not None:
            try:
                n = int(v)
            except ValueError:
                raise ValueError(f'{node.tag}.{attr} vuole un numero, non {v!r}')
            if not limiti[0] <= n <= limiti[1]:
                raise ValueError(
                    f'{node.tag}.{attr}={n} fuori dall intervallo osservato '
                    f'{limiti[0]}..{limiti[1]}. Usa force=True per provarlo.')
        unico = SOLO_UN_VALORE.get(chiave)
        if unico is not None and v != unico:
            raise ValueError(
                f'{node.tag}.{attr} vale sempre {unico!r} nel corpus '
                f'({v!r} mai visto). Usa force=True per esplorare.')
    node.set(attr, v)
    return v


# ------------------------------------------------------------ scorciatoie

def set_filter(inst: Node, *, lpf: str | None = None,
               hpf: str | None = None, route: str | None = None,
               lpf_morph: int | None = None, hpf_morph: int | None = None,
               params_node: Node | None = None, force: bool = False) -> None:
    """Modalita' dei filtri sullo strumento.

    `lpf='Off'` spegne il filtro passa-basso: da li' in poi `lpfFrequency` e
    `lpfResonance` non hanno piu' effetto, pur restando scrivibili. E' il caso
    che ha fatto sembrare inefficaci le modifiche a una patch FM.

    route: H2L (HPF -> LPF), L2H (LPF -> HPF), PARA (parallelo).
    I morph sono 0-50: SVF LP -> band/notch -> HP sullo slot LPF,
    direzione inversa sullo slot HPF; drive nei ladder LPF e FM in HPLadder.
    Il cambio di modo conserva i morph se non passati esplicitamente.
    Per un preset i parametri stanno in inst; in una song passare la clip
    (o noteRow del drum) come params_node. Modi e route sono condivisi da
    tutte le clip dello strumento, i morph appartengono ai loro parametri.
    Valida tutto prima di scrivere; force riguarda solo le enumerazioni.
    """
    from copy import deepcopy
    from . import sound as SND

    if inst.tag not in ('sound', 'kit'):
        raise ValueError('set_filter richiede uno strumento sound o kit')
    attributes = [('lpfMode', lpf), ('hpfMode', hpf), ('filterRoute', route)]
    values = [('lpfMorph', lpf_morph), ('hpfMorph', hpf_morph)]
    target = inst if params_node is None else params_node
    probe = deepcopy(inst)
    for attr, value in attributes:
        if value is not None:
            set_attr(probe, attr, value, force=force)
    probe_params = deepcopy(target)
    for name, value in values:
        if value is not None:
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 50:
                raise ValueError(f'{name} richiede un intero 0-50')
            SND.set(probe_params, name, value)
    for attr, value in attributes:
        if value is not None:
            set_attr(inst, attr, value, force=force)
    for name, value in values:
        if value is not None:
            SND.set(target, name, value)


#: Attributi di `<modulator1>`, coi valori neutri. Presi dai suoni FM del
#: corpus: 80 su 80 hanno esattamente questi nomi, e `modulator2` ne ha uno
#: in piu', `toModulator1`, che sceglie fra i due algoritmi (0 = i due
#: modulatori vanno in parallelo sui carrier, 1 = il secondo modula il primo,
#: cioe' una catena).
_MODULATORE = (('transpose', '0'), ('cents', '0'), ('retrigPhase', '0'))
_MODULATORE2_EXTRA = ('toModulator1', '0')


def ensure_fm_modulators(inst: Node) -> list[str]:
    """Crea i `<modulator1>`/`<modulator2>` se mancano. Ritorna quali.

    Serve perche' i preset subtractive non li hanno: `refs/synths/TEMPL.XML`,
    che e' il synth vuoto del dispositivo, ha osc1/osc2/lfo1-4/unison e basta.
    Portarlo a `mode="fm"` senza modulatori lascerebbe il suono in uno stato
    che il dispositivo non scrive mai — nel corpus i modulatori ci sono in
    **80 suoni FM su 80**.

    I livelli dei modulatori NON stanno qui: sono parametri
    (`modulator1Amount`, `modulator1Feedback`, …), gia' presenti nel
    contenitore, e si toccano con `sound.set()`.
    """
    creati = []
    dopo = inst.find('osc2')
    posizione = (inst.children.index(dopo) + 1) if dopo is not None else 0
    for n, extra in ((1, None), (2, _MODULATORE2_EXTRA)):
        tag = f'modulator{n}'
        if inst.find(tag) is not None:
            continue
        attrs = list(_MODULATORE)
        if extra is not None:
            attrs.append(extra)
        inst.insert(posizione, Node(tag=tag, attrs=attrs, self_closing=True))
        posizione += 1
        creati.append(tag)
    return creati


def set_synth_mode(inst: Node, mode: str, *, force: bool = False) -> None:
    """`subtractive`, `fm` o `ringmod`.

    Cambiare modo non converte il suono: cambia quale motore lo interpreta.

    Passando a `fm` fa anche le due cose che il dispositivo fa e che, non
    fatte, lasciano un suono a meta':

    1. **crea i modulatori** se mancano (vedi `ensure_fm_modulators`);
    2. **toglie `type` dagli oscillatori**, perche' in FM non c'e' forma
       d'onda da scegliere e nel corpus gli osc di un suono FM portano solo
       `transpose`/`cents`/`retrigPhase` — 80 su 80. Lasciare un `type`
       ereditato dal preset subtractive sarebbe un attributo scritto nel
       posto sbagliato, che e' il modo in cui questo progetto si e' gia'
       fatto male una volta.
    """
    set_attr(inst, 'mode', mode, force=force)
    if mode != 'fm':
        return
    ensure_fm_modulators(inst)
    for w in ('osc1', 'osc2'):
        o = inst.find(w)
        if o is not None and o.has('type'):
            o.remove('type')


def set_osc(inst: Node, which: int, *, type: str | None = None,  # noqa: A002
            transpose: int | None = None, cents: int | None = None,
            force: bool = False) -> Node:
    """Oscillatore 1 o 2: forma d'onda e accordatura."""
    if which not in (1, 2):
        raise ValueError('gli oscillatori sono 1 e 2')
    nodo = inst.find(f'osc{which}')
    if nodo is None:
        raise ValueError(f'lo strumento non ha <osc{which}>')
    if type is not None:
        set_attr(nodo, 'type', type, force=force)
    if transpose is not None:
        nodo.set('transpose', str(int(transpose)))
    if cents is not None:
        nodo.set('cents', str(int(cents)))
    return nodo


def set_lfo(inst: Node, which: int, *, type: str | None = None,  # noqa: A002
            sync: int | None = None, force: bool = False) -> Node:
    if which not in (1, 2):
        raise ValueError('qui si impostano LFO 1 e 2')
    nodo = inst.find(f'lfo{which}')
    if nodo is None:
        raise ValueError(f'lo strumento non ha <lfo{which}>')
    if type is not None:
        set_attr(nodo, 'type', type, force=force)
    if sync is not None:
        nodo.set('syncLevel', str(int(sync)))
    return nodo


def set_unison(inst: Node, *, num: int | None = None,
               detune: int | None = None, spread: int | None = None,
               force: bool = False) -> Node:
    nodo = inst.find('unison')
    if nodo is None:
        raise ValueError('lo strumento non ha <unison>')
    for attr, val in (('num', num), ('detune', detune), ('spread', spread)):
        if val is not None:
            set_attr(nodo, attr, val, force=force)
    return nodo


def describe(inst: Node) -> dict[str, str | None]:
    """La struttura dello strumento, per capire cosa si sta modificando."""
    out: dict[str, str | None] = {
        'tipo': inst.tag,
        'preset': inst.get('presetName'),
        'mode': inst.get('mode'),
        'lpfMode': inst.get('lpfMode'),
        'hpfMode': inst.get('hpfMode'),
        'filterRoute': inst.get('filterRoute'),
        'polyphonic': inst.get('polyphonic'),
        'modFXType': inst.get('modFXType'),
    }
    for w in (1, 2):
        o = inst.find(f'osc{w}')
        if o is not None:
            out[f'osc{w}'] = o.get('type') or '(nessun type: sintesi FM)'
        lf = inst.find(f'lfo{w}')
        if lf is not None:
            out[f'lfo{w}'] = lf.get('type')
    u = inst.find('unison')
    if u is not None:
        out['unison'] = f'{u.get("num")} voci, detune {u.get("detune")}'
    return out
