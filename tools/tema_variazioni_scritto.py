"""Tema e quattro variazioni elettroniche in una forma di 24 battute.

Il tema e il controcanto sono le prime quattro battute di INVERT01. La forma
non sostituisce il tema con materiale affine: ne conserva gli attacchi
portanti nella figurazione, lo distribuisce fra timbri, lo espande a tre parti
e infine ne raddoppia esattamente attacchi e durate.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU  # noqa: E402
from delugexml.notes import Note  # noqa: E402

B = MU.TICK_PER_BATTUTA
TOTAL_BARS = 24
BPM = 102

TEMPLATE = ROOT / 'refs' / 'songs' / 'TEMPL0.XML'
SYNTH = ROOT / 'refs' / 'synths' / 'TEMPL.XML'
OUT = ROOT / 'out' / 'VARIAZ01.XML'

THEME_A = (
    (0,       'sib4', 72), (96,      'sol4', 120),
    (240,     'sib4', 120), (B + 48, 'sol4', 120),
    (B + 192, 'mi4', 72), (B + 288,  'fa4', 96),
    (2 * B,   'sol4', 72), (2 * B + 144, 'fa4', 72),
    (2 * B + 240, 'mi4', 72), (2 * B + 336, 'fa4', 48),
    (3 * B,   'sol4', 168), (3 * B + 192, 'sib4', 72),
    (3 * B + 288, 'do5', 96),
)

COUNTER_B = (
    (0,       'sol3', 168), (192,     'sib3', 72),
    (288,     'sol3', 96), (B,        'mi3', 120),
    (B + 144, 'sol3', 72), (B + 240,  'la3', 144),
    (2 * B + 48, 'sib3', 120), (2 * B + 192, 'la3', 72),
    (2 * B + 288, 'sol3', 96), (3 * B, 'sib3', 72),
    (3 * B + 96, 'sol3', 120), (3 * B + 240, 'mi3', 72),
    (3 * B + 336, 'fa3', 48),
)


def _linea(score, *, velocity: int) -> dict[int, list]:
    return MU.linea(tuple((pos, pitch, length) for pos, pitch, length in score),
                    velocity=velocity, stacco=0)


def _eventi(voce: dict[int, list]) -> list[tuple[int, int, int, int]]:
    return sorted((note.pos, pitch, note.length, note.velocity)
                  for pitch, row in voce.items() for note in row)


def _da_eventi(events) -> dict[int, list]:
    result: dict[int, list] = {}
    for pos, pitch, length, velocity in events:
        result.setdefault(pitch, []).append(
            Note(pos=pos, length=length, velocity=velocity))
    for notes in result.values():
        notes.sort(key=lambda note: note.pos)
    return result


def _sposta(voce: dict[int, list], offset: int) -> dict[int, list]:
    return _da_eventi((pos + offset, pitch, length, velocity)
                      for pos, pitch, length, velocity in _eventi(voce))


def _unisci(*voci: dict[int, list]) -> dict[int, list]:
    result: dict[int, list] = {}
    for voce in voci:
        for pitch, notes in voce.items():
            result.setdefault(pitch, []).extend(notes)
    for notes in result.values():
        notes.sort(key=lambda note: note.pos)
    return result


def tema_alta() -> dict[int, list]:
    return _linea(THEME_A, velocity=84)


def tema_bassa() -> dict[int, list]:
    return _linea(COUNTER_B, velocity=72)


def figurale_alta() -> dict[int, list]:
    """Conserva ogni pilastro del tema e ne anima gli spazi con note vicine."""
    events = []
    scale = (62, 64, 65, 67, 69, 70, 72, 74)
    for index, (pos, name, _length) in enumerate(THEME_A):
        pitch = MU.altezza(name)
        next_pos = THEME_A[index + 1][0] if index + 1 < len(THEME_A) else 4 * B
        gap = next_pos - pos
        events.append((pos, pitch, min(42, gap), 86))
        if gap >= 72:
            scale_index = min(range(len(scale)), key=lambda i: abs(scale[i] - pitch))
            direction = 1 if index % 2 == 0 else -1
            neighbour = scale[max(0, min(len(scale) - 1,
                                         scale_index + direction))]
            events.append((pos + 48, neighbour, min(30, gap - 48), 64))
        if gap >= 120:
            events.append((pos + 96, pitch, min(30, gap - 96), 70))
    return _da_eventi(events)


def figurale_bassa() -> dict[int, list]:
    """Il controcanto risponde in note brevi senza duplicare la figurazione."""
    events = []
    for index, (pos, name, _length) in enumerate(COUNTER_B):
        pitch = MU.altezza(name)
        next_pos = COUNTER_B[index + 1][0] if index + 1 < len(COUNTER_B) else 4 * B
        events.append((pos, pitch, min(72, next_pos - pos), 68))
        if index in (1, 4, 7, 10) and next_pos - pos >= 96:
            events.append((pos + 72, pitch + 2, 24, 55))
    return _da_eventi(events)


def variazione_timbrica() -> tuple[dict[int, list], ...]:
    """Distribuisce il tema letterale fra luce e ombra, una battuta ciascuna."""
    parti = ([], [], [])
    for event in THEME_A:
        bar = event[0] // B
        parti[bar % 2].append(event)
    return tuple(_linea(part, velocity=82 if index == 0 else 75)
                 for index, part in enumerate(parti))


def timbrica_controcanto() -> dict[int, list]:
    return _linea(COUNTER_B, velocity=65)


THIRD_C = (
    (48,       're2', 120), (240,      'fa2', 96),
    (B + 96,   'mi2', 120), (B + 264,  'la2', 96),
    (2 * B,    're2', 120), (2 * B + 216, 'do2', 96),
    (3 * B + 48, 'sib1', 120), (3 * B + 264, 're2', 120),
)


def variazione_tre_parti() -> tuple[dict[int, list], ...]:
    return (tema_alta(), tema_bassa(), _linea(THIRD_C, velocity=69))


def aumentata_alta() -> dict[int, list]:
    return _linea(tuple((pos * 2, pitch, length * 2)
                        for pos, pitch, length in THEME_A), velocity=82)


def aumentata_bassa() -> dict[int, list]:
    return _linea(tuple((pos * 2, pitch, length * 2)
                        for pos, pitch, length in COUNTER_B), velocity=69)


def coda_profonda() -> dict[int, list]:
    """Un pedale terminale allarga l'ultima cadenza senza mutare il tema."""
    return _linea(((6 * B, 're2', 2 * B),), velocity=58)


def parti_complete() -> tuple[dict[int, list], ...]:
    timbri = variazione_timbrica()
    tre = variazione_tre_parti()
    return (
        _unisci(tema_alta(), _sposta(figurale_alta(), 4 * B),
                _sposta(timbri[0], 8 * B), _sposta(tre[0], 12 * B),
                _sposta(aumentata_alta(), 16 * B)),
        _unisci(tema_bassa(), _sposta(figurale_bassa(), 4 * B),
                _sposta(timbri[1], 8 * B), _sposta(tre[1], 12 * B),
                _sposta(aumentata_bassa(), 16 * B)),
        _unisci(_sposta(timbrica_controcanto(), 8 * B),
                _sposta(tre[2], 12 * B),
                _sposta(coda_profonda(), 16 * B)),
    )


def costruisci():
    """Costruisce VARIAZ01 senza scrivere file o usare il dispositivo."""
    import warnings  # noqa: PLC0415
    from delugexml import parse_file, song as S, create as C  # noqa: PLC0415
    from delugexml import arranger as A, structure as ST  # noqa: PLC0415
    from delugexml import sound as SND  # noqa: PLC0415

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(str(TEMPLATE))
        S.set_bpm(doc.root, BPM)
        S.set_swing(doc, 50, figura='1/8')
        S.set_scale(doc, 'D', 'minore')
        for instrument in list(S.instruments(doc)):
            MU.togli(doc, instrument)

        length = TOTAL_BARS * B
        specs = (
            ('TEMA LUCE', '0', 'triangle', 'analogSaw', 38, 12, 3, 33, 13),
            ('TEMA OMBRA', '16', 'square', 'triangle', 22, 21, 2, 27, 10),
            ('FONDO', '28', 'analogSaw', 'triangle', 16, 25, 6, 31, 16),
        )
        for notes, spec in zip(parti_complete(), specs):
            (name, colour, osc_a, osc_b, vol_a, vol_b,
             attack, sustain, release) = spec
            instrument, clip = C.add_track(
                doc, str(SYNTH), name=name, folder='SYNTHS', length=length,
                colour_offset=colour, playing=True)
            ST.set_osc(instrument, 1, type=osc_a, transpose=0, cents=0)
            ST.set_osc(instrument, 2, type=osc_b, transpose=0,
                       cents=-5 if name == 'TEMA LUCE' else 4)
            SND.set(clip, 'oscAVolume', vol_a)
            SND.set(clip, 'oscBVolume', vol_b)
            SND.set(clip, 'envelope1.attack', attack)
            SND.set(clip, 'envelope1.sustain', sustain)
            SND.set(clip, 'envelope1.release', release)
            S.set_key_mode(clip, False)
            MU.scrivi(doc, clip, notes)
            A.place(doc, instrument, clip, 0, length)

        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc


def scrivi(path: Path = OUT) -> Path:
    from delugexml import write_file  # noqa: PLC0415
    from delugexml.writer import FormatTable  # noqa: PLC0415

    doc = costruisci()
    errors = MU.verifica(doc)
    warnings = MU.avvertenze(doc)
    if errors or warnings:
        raise ValueError(f'song non pronta: errori={errors}, avvertenze={warnings}')
    write_file(doc, path, FormatTable.load(ROOT / 'out' / 'format_table.json'))
    return path


if __name__ == '__main__':
    doc = costruisci()
    print('forma: tema / figurale / timbrica / tre parti / aumentazione-coda')
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('variaz', 1))
