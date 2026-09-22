"""Configurazione dell'arpeggiatore community del Deluge.

La struttura (preset, modi, ottave, repeat e lock) vive sempre nel nodo
``<arpeggiator>``. I valori 0-50 del randomizer hanno invece due formati:
nei synth/kit sono parametri esadecimali del suono, mentre MIDI/CV li salva
direttamente sull'arpeggiatore come int32 decimali. Questa API nasconde la
differenza e restituisce sempre le unita' mostrate dal display.
"""
from __future__ import annotations

from .parser import Node
from . import sound as SND


# Ordine esatto della tabella ``ARP_RHYTHM_PATTERNS`` del firmware community
# 2d7cdf8. L'indice 0 e' il ritmo continuo, senza pattern di pause.
RITMI: tuple[str | None, ...] = (
    None,
    '0--', '00-', '0-0', '0-00', '00--', '000-', '0--0', '00-0',
    '0----', '0-000', '00---', '0000-', '0---0', '00-00', '0-0--',
    '000-0', '0--0-', '0--00', '000--', '00--0', '0-00-', '00-0-',
    '0-0-0', '0-----', '0-0000', '00----', '00000-', '0----0',
    '00-000', '0-0---', '0000-0', '0---0-', '000-00', '0--000',
    '000---', '0000--', '0---00', '00--00', '0-00--', '000--0',
    '0--00-', '0-0-00', '00-0--', '000-0-', '0--0-0', '0-000-',
    '00---0', '00--0-', '0-0--0', '00-0-0',
)

_PRESET = {
    'off': ('off', 'off', None, None),
    'up': ('arp', 'arp', 'up', 'up'),
    'down': ('arp', 'arp', 'down', 'down'),
    'both': ('arp', 'arp', 'up', 'alt'),
    'random': ('arp', 'arp', 'random', 'random'),
    'walk': ('arp', 'arp', 'walk2', 'alt'),
}
_ALIAS_PRESET = {
    'spento': 'off', 'su': 'up', 'giu': 'down', 'giù': 'down',
    'entrambi': 'both', 'casuale': 'random',
}
_MODI_NOTA = {
    'up', 'down', 'upDown', 'random', 'walk1', 'walk2', 'walk3',
    'asPlayed', 'pattern',
}
_ALIAS_NOTA = {
    'up-down': 'upDown', 'up_down': 'upDown',
    'as-played': 'asPlayed', 'as_played': 'asPlayed',
}
_MODI_OTTAVA = {'up', 'down', 'alt', 'random'}

_PARAMETRI = {
    'ritmo': 'rhythm',
    'ratchet': 'ratchetAmount',
    'probabilita_ratchet': 'ratchetProbability',
    'probabilita_nota': 'noteProbability',
    'probabilita_basso': 'bassProbability',
    'probabilita_scambio': 'swapProbability',
    'probabilita_glide': 'glideProbability',
    'probabilita_reverse': 'reverseProbability',
    'probabilita_accordo': 'chordProbability',
    'lunghezza_sequenza': 'sequenceLength',
    'polifonia_accordo': 'chordPolyphony',
    'spread_velocity': 'spreadVelocity',
    'spread_gate': 'spreadGate',
    'spread_ottava': 'spreadOctave',
}

_SPAN = 1 << 32
_STEP = _SPAN // 50


def _nodo_arp(target: Node) -> Node:
    arp = target if target.tag == 'arpeggiator' else target.find('arpeggiator')
    if arp is None:
        raise ValueError(f'<{target.tag}> non contiene <arpeggiator>')
    return arp


def _intero(nome: str, valore: object, minimo: int, massimo: int) -> int:
    if type(valore) is not int or not minimo <= valore <= massimo:
        raise ValueError(
            f'{nome} deve essere un intero fra {minimo} e {massimo}, '
            f'non {valore!r}')
    return valore


def _ritmo_indice(valore: object) -> int:
    if type(valore) is int:
        return _intero('ritmo', valore, 0, len(RITMI) - 1)
    if isinstance(valore, str):
        normalizzato = valore.strip()
        if normalizzato.lower() in {'none', 'nessuno', 'continuo'}:
            return 0
        try:
            return RITMI.index(normalizzato)
        except ValueError:
            pass
    raise ValueError(
        f'ritmo deve essere un indice 0-{len(RITMI) - 1} o un pattern '
        f'esatto della tabella community, non {valore!r}')


def _direct_encode(display: int) -> str:
    """Scala non-audio del firmware: uint32, serializzato come int32."""
    raw = (display * _STEP) & 0xFFFFFFFF
    signed = raw if raw < (1 << 31) else raw - _SPAN
    return str(signed)


def _direct_decode(grezzo: str) -> int | None:
    try:
        raw = int(grezzo) & 0xFFFFFFFF
    except (TypeError, ValueError):
        return None
    # Corrisponde a ``getValuePossiblyForMenu()`` del firmware.
    return ((raw * 50) + (1 << 31)) >> 32


def _scrive_nel_suono(target: Node, nome: str) -> bool:
    return SND.get_raw(target, nome) is not None


def _leggi_parametro(target: Node, arp: Node, nome: str) -> int | None:
    if _scrive_nel_suono(target, nome):
        try:
            return SND.get(target, nome)
        except SND.Automatizzato:
            return None
    if arp.has(nome):
        return _direct_decode(arp.get(nome))
    return None


def _preset_corrente(arp: Node) -> str:
    if arp.get('mode') != 'arp' and arp.get('arpMode') != 'arp':
        return 'off'
    coppia = (arp.get('noteMode', 'up'), arp.get('octaveMode', 'up'))
    for nome, (_, _, modo_nota, modo_ottava) in _PRESET.items():
        if nome != 'off' and coppia == (modo_nota, modo_ottava):
            return nome
    return 'custom'


def leggi(target: Node) -> dict[str, object]:
    """Rilegge una configurazione nelle unita' visibili sul Deluge."""
    arp = _nodo_arp(target)
    out: dict[str, object] = {
        'preset': _preset_corrente(arp),
        'modo_note': arp.get('noteMode', 'up'),
        'modo_ottave': arp.get('octaveMode', 'up'),
        'ottave': int(arp.get('numOctaves', '1')),
        'ripetizioni': int(arp.get('stepRepeat', '1')),
        'blocca_random': arp.get('randomizerLock', '0') == '1',
    }
    for pubblico, xml in _PARAMETRI.items():
        valore = _leggi_parametro(target, arp, xml)
        if valore is not None:
            out[pubblico] = valore
    indice = out.get('ritmo')
    if isinstance(indice, int) and 0 <= indice < len(RITMI):
        out['ritmo_indice'] = indice
        out['ritmo'] = RITMI[indice]
    return out


def configura(
        target: Node, *, preset: str | None = None,
        modo_note: str | None = None, modo_ottave: str | None = None,
        ottave: int | None = None, ripetizioni: int | None = None,
        ritmo: int | str | None = None, ratchet: int | None = None,
        probabilita_ratchet: int | None = None,
        probabilita_nota: int | None = None,
        probabilita_basso: int | None = None,
        probabilita_scambio: int | None = None,
        probabilita_glide: int | None = None,
        probabilita_reverse: int | None = None,
        probabilita_accordo: int | None = None,
        lunghezza_sequenza: int | None = None,
        polifonia_accordo: int | None = None,
        spread_velocity: int | None = None,
        spread_gate: int | None = None,
        spread_ottava: int | None = None,
        blocca_random: bool | None = None) -> dict[str, object]:
    """Configura l'arpeggiatore, validando tutto prima di modificare l'XML.

    I preset sono ``off``, ``up``, ``down``, ``both``, ``random`` e
    ``walk``. Per un comportamento custom usare ``modo_note`` e/o
    ``modo_ottave``. Tutti i valori di rhythm/randomizer sono 0-50.
    """
    arp = _nodo_arp(target)

    # Normalizzazione e validazione completa: nessuna scrittura precede
    # questa sezione, quindi un errore non puo' lasciare una mezza modifica.
    preset_norm: str | None = None
    if preset is not None:
        if not isinstance(preset, str):
            raise ValueError(f'preset sconosciuto: {preset!r}')
        preset_norm = _ALIAS_PRESET.get(preset.lower(), preset.lower())
        if preset_norm not in _PRESET:
            raise ValueError(
                f'preset {preset!r} sconosciuto: off, up, down, both, '
                'random, walk')
        if modo_note is not None or modo_ottave is not None:
            raise ValueError('preset e modi custom sono alternativi')

    note_norm: str | None = None
    if modo_note is not None:
        if not isinstance(modo_note, str):
            raise ValueError(f'modo_note sconosciuto: {modo_note!r}')
        note_norm = _ALIAS_NOTA.get(modo_note, modo_note)
        if note_norm not in _MODI_NOTA:
            raise ValueError(
                f'modo_note {modo_note!r} sconosciuto: '
                f'{", ".join(sorted(_MODI_NOTA))}')

    ottava_norm: str | None = None
    if modo_ottave is not None:
        if not isinstance(modo_ottave, str):
            raise ValueError(f'modo_ottave sconosciuto: {modo_ottave!r}')
        if modo_ottave in {'up-down', 'up_down', 'upDown'}:
            raise ValueError(
                'modo_ottave up-down non e sicuro sulla build 2d7cdf8: '
                'il firmware lo rilegge come random')
        ottava_norm = modo_ottave
        if ottava_norm not in _MODI_OTTAVA:
            raise ValueError(
                f'modo_ottave {modo_ottave!r} sconosciuto: '
                f'{", ".join(sorted(_MODI_OTTAVA))}')

    ottave_norm = (_intero('ottave', ottave, 1, 8)
                    if ottave is not None else None)
    repeat_norm = (_intero('ripetizioni', ripetizioni, 1, 8)
                   if ripetizioni is not None else None)
    if blocca_random is not None and type(blocca_random) is not bool:
        raise ValueError('blocca_random deve essere True o False')

    numerici = {
        'ratchet': ratchet,
        'probabilita_ratchet': probabilita_ratchet,
        'probabilita_nota': probabilita_nota,
        'probabilita_basso': probabilita_basso,
        'probabilita_scambio': probabilita_scambio,
        'probabilita_glide': probabilita_glide,
        'probabilita_reverse': probabilita_reverse,
        'probabilita_accordo': probabilita_accordo,
        'lunghezza_sequenza': lunghezza_sequenza,
        'polifonia_accordo': polifonia_accordo,
        'spread_velocity': spread_velocity,
        'spread_gate': spread_gate,
        'spread_ottava': spread_ottava,
    }
    if ritmo is not None:
        numerici['ritmo'] = _ritmo_indice(ritmo)
    normalizzati = {
        nome: _intero(nome, valore, 0, 50)
        for nome, valore in numerici.items() if valore is not None
    }
    for pubblico in normalizzati:
        xml = _PARAMETRI[pubblico]
        if not _scrive_nel_suono(target, xml) and not arp.has(xml):
            raise ValueError(
                f'parametro arpeggiatore {xml!r} inesistente su '
                f'<{target.tag}>')

    # Solo da qui in poi si modifica il documento.
    if preset_norm is not None:
        mode, arp_mode, nota, ottava = _PRESET[preset_norm]
        arp.set('mode', mode)
        arp.set('arpMode', arp_mode)
        if nota is not None:
            arp.set('noteMode', nota)
        if ottava is not None:
            arp.set('octaveMode', ottava)
    elif note_norm is not None or ottava_norm is not None:
        arp.set('mode', 'arp')
        arp.set('arpMode', 'arp')
        if note_norm is not None:
            arp.set('noteMode', note_norm)
        if ottava_norm is not None:
            arp.set('octaveMode', ottava_norm)

    if ottave_norm is not None:
        arp.set('numOctaves', str(ottave_norm))
    if repeat_norm is not None:
        arp.set('stepRepeat', str(repeat_norm))
    if blocca_random is not None:
        arp.set('randomizerLock', '1' if blocca_random else '0')

    for pubblico, display in normalizzati.items():
        xml = _PARAMETRI[pubblico]
        if _scrive_nel_suono(target, xml):
            SND.set(target, xml, display)
        else:
            arp.set(xml, _direct_encode(display))

    return leggi(target)
