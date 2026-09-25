"""Espressione MPE per nota nelle ``noteRow`` melodiche.

Il Deluge salva pitch, asse Y (slide / timbro) e pressione come tre
automazioni dentro ``noteRow/expressionData``. Le posizioni sono assolute
nella clip; i valori pubblici restano nelle unita MIDI invece degli int32
interni del firmware.
"""
from __future__ import annotations

from typing import NamedTuple

from . import automation as A
from .midicv import (_bend_to_raw, _cc_to_raw, _pressure_to_raw,
                     _raw_to_bend, _raw_to_cc, _raw_to_pressure)
from .parser import Node


class MPEValuePoint(NamedTuple):
    """Un punto MPE nelle unita' MIDI, non nell'int32 interno."""
    pos: int
    value: int
    interp: bool


def _note_row(clip: Node, pitch: int) -> Node | None:
    from . import song as S                              # import locale: ciclo

    if clip.tag != 'instrumentClip' or S.is_kit_clip(clip):
        raise ValueError('serve una <instrumentClip> melodica, non un kit')
    if type(pitch) is not int or not 0 <= pitch <= 127:
        raise ValueError(f'altezza MIDI deve essere un intero 0..127, non {pitch!r}')
    for row in S.note_rows(clip):
        if row.get('y') == str(pitch):
            return row
    return None


def _read_axis(clip: Node, pitch: int, name: str, decode_value) \
        -> list[MPEValuePoint]:
    row = _note_row(clip, pitch)
    if row is None:
        return []
    expression = row.find('expressionData')
    if expression is None or expression.get(name) is None:
        return []
    _, points = A.decode(expression.get(name))
    return [MPEValuePoint(p.pos, decode_value(p.raw), p.interp)
            for p in points]


def read_pitch_bend(clip: Node, pitch: int) -> list[MPEValuePoint]:
    """Pitch per-nota come valori MIDI firmati ``-8192..8191``."""
    return _read_axis(clip, pitch, 'pitchBend', _raw_to_bend)


def read_slide(clip: Node, pitch: int) -> list[MPEValuePoint]:
    """Asse Y MPE (slide / timbro, CC74) nella scala ``0..127``."""
    return _read_axis(clip, pitch, 'yExpression', _raw_to_cc)


def read_pressure(clip: Node, pitch: int) -> list[MPEValuePoint]:
    """Pressione per-nota nella scala MIDI ``0..127``."""
    return _read_axis(clip, pitch, 'pressure', _raw_to_pressure)


def _strict_int(name: str, value: object, minimo: int, massimo: int) -> int:
    if type(value) is not int or not minimo <= value <= massimo:
        raise ValueError(f'{name} deve essere un intero {minimo}..{massimo}, '
                         f'non {value!r}')
    return value


def _row_length(clip: Node, row: Node) -> int:
    raw = row.get('length', clip.get('length'))
    try:
        length = int(raw)
    except (TypeError, ValueError):
        raise ValueError('la clip o noteRow MPE non ha una length intera') from None
    if length <= 0:
        raise ValueError(f'la lunghezza MPE deve essere positiva, non {length}')
    return length


def _nodes(clip: Node, row: Node, points, *, minimo: int, massimo: int,
           encode_value, interpolated: bool) -> list[A.Punto]:
    if type(interpolated) is not bool:
        raise ValueError(f'interpolated deve essere bool, non {interpolated!r}')
    if not isinstance(points, (list, tuple)) or not points:
        raise ValueError('servono uno o piu punti (tick, valore)')
    length = _row_length(clip, row)
    out = []
    previous = -1
    for i, point in enumerate(points):
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            raise ValueError(f'punto {i}: attesa coppia (tick, valore), '
                             f'non {point!r}')
        pos = _strict_int(f'punto {i} tick', point[0], 0, length - 1)
        value = _strict_int(f'punto {i} valore', point[1], minimo, massimo)
        if pos <= previous:
            raise ValueError('i tick devono essere crescenti e distinti')
        out.append(A.Punto(pos, encode_value(value), interpolated))
        previous = pos
    return out


def _expression(row: Node, *, create: bool) -> Node | None:
    expression = row.find('expressionData')
    if expression is None and create:
        expression = Node(tag='expressionData', self_closing=True)
        index = next((i for i, c in enumerate(row.children)
                      if c.tag == 'soundParams'), len(row.children))
        row.insert(index, expression)
    return expression


def _set_axis(clip: Node, pitch: int, name: str, points, *,
              minimo: int, massimo: int, encode_value,
              interpolated: bool) -> dict[str, object]:
    from . import song as S                              # import locale: ciclo

    row = _note_row(clip, pitch)
    if row is None:
        raise ValueError(f'nessuna noteRow melodica per altezza MIDI {pitch}')
    if not S.read_notes(row):
        raise ValueError(f'la noteRow MIDI {pitch} non contiene note')
    nodes = _nodes(clip, row, points, minimo=minimo, massimo=massimo,
                   encode_value=encode_value, interpolated=interpolated)
    encoded = A.encode(nodes[0].raw, nodes)
    expression = _expression(row, create=True)
    expression.set(name, encoded)
    return {'asse': name, 'altezza': pitch, 'punti': len(nodes),
            'da_tick': nodes[0].pos, 'a_tick': nodes[-1].pos,
            'interpolata': interpolated}


def set_pitch_bend(clip: Node, pitch: int, points, *,
                   interpolated: bool = True) -> dict[str, object]:
    """Scrive pitch per-nota ``-8192..8191`` sulla riga melodica."""
    return _set_axis(clip, pitch, 'pitchBend', points,
                     minimo=-8192, massimo=8191, encode_value=_bend_to_raw,
                     interpolated=interpolated)


def set_slide(clip: Node, pitch: int, points, *,
              interpolated: bool = True) -> dict[str, object]:
    """Scrive l'asse Y MPE (slide / timbro, ``0..127``)."""
    return _set_axis(clip, pitch, 'yExpression', points,
                     minimo=0, massimo=127, encode_value=_cc_to_raw,
                     interpolated=interpolated)


def set_pressure(clip: Node, pitch: int, points, *,
                 interpolated: bool = True) -> dict[str, object]:
    """Scrive pressione per-nota ``0..127`` sulla riga melodica."""
    return _set_axis(clip, pitch, 'pressure', points,
                     minimo=0, massimo=127, encode_value=_pressure_to_raw,
                     interpolated=interpolated)
