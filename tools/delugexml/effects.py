"""Effetti standard, formato community b76ed39.

Modi e saturazione sono condivisi dallo strumento; i valori sono della
clip (params_node), o del preset se omesso. Le scritture validano tutti
gli argomenti prima di mutare qualsiasi nodo. I valori non richiesti,
comprese le automazioni, restano intatti.

Fonti: mod_controllable_audio.cpp, util/functions.cpp, model/sync.h,
song.cpp e gui/menu_item/reverb della build indicata. Vedi docs/EFFETTI.md.
"""
from __future__ import annotations

import struct

from .parser import Node
from . import sound as SND, params as P

MOD_FX_TYPES = ('none', 'flanger', 'phaser', 'chorus', 'StereoChorus',
                'dimension', 'TapeWarble', 'grainFX')
SYNC_TYPES = {'even': 0, 'triplet': 10, 'dotted': 19}
REVERB_MODELS = {'freeverb': 0, 'mutable': 1, 'digital': 2}


def _integer(name, value, low=0, high=50):
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ValueError(f'{name} richiede un intero {low}..{high}')
    return value


def _choice(name, value, choices):
    if not isinstance(value, str) or value not in choices:
        raise ValueError(f'{name}: valori ammessi {", ".join(choices)}')
    return value


def _owner(node):
    if node.tag not in ('sound', 'kit', 'song', 'audioTrack'):
        raise ValueError('gli effetti strutturali richiedono sound, kit, song o audioTrack')


def _param_writes(node, values):
    """Prepara scritture senza toccare nodi, anche con parametri mancanti."""
    writes = []
    cont = SND.container(node)
    for name, value in values:
        if value is None:
            continue
        _integer(name, value)
        found = SND._cerca(cont, name) if cont is not None else None
        if found is None:
            raise ValueError(f'parametro {name!r} inesistente su <{node.tag}>')
        target, attr = found
        writes.append((target, attr, P.from_display(value)))
    return writes


def _write(writes):
    for node, attr, value in writes:
        node.set(attr, value)


def set_delay(owner: Node, *, analog=None, ping_pong=None, sync_level=None,
              sync_type=None, feedback=None, rate=None, params_node=None):
    """Delay analogico/digitale e parametri 0-50.

sync_level e' il valore XML assoluto (0 = libero), NON l'indice del menu.
Si accettano i livelli XML 0..9; la durata non viene dedotta dall'indice.
sync_type: even, triplet, dotted. Omettere un argomento lo conserva.
Song, kit e audio possono avere delay.rate/feedback invece dei nomi piatti.
"""
    _owner(owner)
    attrs = []
    for name, value in (('analog', analog), ('pingPong', ping_pong)):
        if value is not None:
            if not isinstance(value, bool):
                raise ValueError(f'{name} richiede un booleano')
            attrs.append((name, str(int(value))))
    if sync_level is not None:
        attrs.append(('syncLevel', str(_integer('sync_level', sync_level, 0, 9))))
    if sync_type is not None:
        attrs.append(('syncType', str(SYNC_TYPES[_choice('sync_type', sync_type, SYNC_TYPES)])))
    target = owner if params_node is None else params_node
    values = []
    for flat, nested, value in (('delayFeedback', 'delay.feedback', feedback),
                                 ('delayRate', 'delay.rate', rate)):
        name = flat if SND.get_raw(target, flat) is not None else nested
        values.append((name, value))
    writes = _param_writes(target, values)
    if attrs:
        delay = owner.find('delay')
        if delay is None:
            delay = owner.append(Node(tag='delay', self_closing=True))
        writes.extend((delay, name, value) for name, value in attrs)
    _write(writes)


def set_mod_fx(owner: Node, *, kind=None, rate=None, depth=None,
               feedback=None, offset=None, params_node=None):
    """Tipo XML esatto e controlli 0-50; kind='none' disattiva il mod FX."""
    _owner(owner)
    if kind is not None:
        _choice('kind', kind, MOD_FX_TYPES)
    writes = _param_writes(owner if params_node is None else params_node,
                           [('modFXRate', rate), ('modFXDepth', depth),
                            ('modFXFeedback', feedback), ('modFXOffset', offset)])
    if kind is not None:
        writes.append((owner, 'modFXType', kind))
    _write(writes)


def set_eq(node: Node, *, bass=None, treble=None, bass_frequency=None,
           treble_frequency=None):
    """EQ nei parametri di clip/preset/song/riga: 0-50, gain neutro a 25."""
    _write(_param_writes(node, [('equalizer.bass', bass),
                               ('equalizer.treble', treble),
                               ('equalizer.bassFrequency', bass_frequency),
                               ('equalizer.trebleFrequency', treble_frequency)]))


def set_distortion(owner: Node, *, saturation=None, bitcrush=None,
                   decimation=None, params_node=None):
    """Saturazione 0-15 sullo strumento; bitcrush/decimation 0-50 nei parametri."""
    _owner(owner)
    if saturation is not None:
        _integer('saturation', saturation, 0, 15)
    writes = _param_writes(owner if params_node is None else params_node,
                           [('bitCrush', bitcrush), ('sampleRateReduction', decimation)])
    if saturation is not None:
        writes.append((owner, 'clippingAmount', str(saturation)))
    _write(writes)


def set_reverb_send(node: Node, amount: int):
    """Mandata 0-50 della parte, indipendente dalle impostazioni globali."""
    _write(_param_writes(node, [('reverbAmount', amount)]))


def _reverb_value(value):
    # Il menu usa float32(value / 50); song.cpp moltiplica per 2**31.
    scaled = struct.unpack('f', struct.pack('f', value / 50))[0] * (1 << 31)
    return str(min(int(scaled), (1 << 31) - 1))


def set_reverb(song: Node, *, model=None, room_size=None, damping=None,
               width=None, hpf=None, lpf=None):
    """Riverbero globale: modello e controlli 0-50, salvati in decimale.

Conserva pan, compressore e attributi non richiesti. Richiede un nodo
reverb esistente nella song: non inventa un preset globale incompleto.
"""
    if song.tag != 'song':
        raise ValueError('il riverbero globale richiede il nodo song')
    reverb = song.find('reverb')
    if reverb is None:
        raise ValueError('la song non ha un riverbero: partire da un modello reale')
    writes = []
    if model is not None:
        key = _choice('model', model, REVERB_MODELS)
        writes.append((reverb, 'model', str(REVERB_MODELS[key])))
    for name, value in (('roomSize', room_size), ('dampening', damping),
                        ('width', width), ('hpf', hpf), ('lpf', lpf)):
        if value is not None:
            _integer(name, value)
            writes.append((reverb, name, _reverb_value(value)))
    _write(writes)
