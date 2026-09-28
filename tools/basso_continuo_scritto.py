"""Una linea di basso con cifre, realizzata da un synth sul Deluge.

Piston, Harmony, 5a ed., cap. 6 pp. 84-85: gli intervalli si leggono sopra
la nota effettiva del basso; registro, condotta e ritmo sono una realizzazione.
La linea non si ripete: questo e' continuo, non basso ostinato.

Il vocabolario delle cifre e' volutamente piccolo e dichiarato. ``7/#3`` e'
una notazione interna esplicita per una settima con la terza innalzata; non
pretende di riprodurre una convenzione tipografica storica.
"""
from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU  # noqa: E402

B = MU.TICK_PER_BATTUTA
P = MU.TICK_PER_MOVIMENTO // 4
BARS = 8
BPM = 104

TEMPLATE = ROOT / 'refs' / 'songs' / 'TEMPL0.XML'
SYNTH = ROOT / 'refs' / 'synths' / 'TEMPL.XML'
BASS = ROOT / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = ROOT / 'refs' / 'kits' / '808 From Mars.XML'
OUT = ROOT / 'out' / 'BASSOC01.XML'

KICK = 'BD B 808 Decay C 02'
RIM = 'Rim Shot A 808'
HAT = 'CH Combo 808'

# La durata di ogni bass note e' fino all'evento successivo. I cambiamenti
# a 288/1824, vicini alla fine della battuta, evitano un basso a blocchi.
SCORE = (
    (0,       're2',  '5/3'),
    (288,     'fa2',  '6/3'),
    (B,       'sol2', '5/3'),
    (B + 192, 'la2',  '7/#3'),
    (2*B,     're2',  '5/3'),
    (2*B+192, 'do2',  '6/3'),
    (3*B,     'sib1', '5/3'),
    (3*B+192, 'la1',  '7/#3'),
    (4*B,     'sol2', '5/3'),
    (4*B+288, 'fa2',  '6/3'),
    (5*B,     'do#2', '6/5'),
    (5*B+192, 're2',  '5/3'),
    (6*B,     'sol2', '5/3'),
    (6*B+192, 'fa2',  '6/3'),
    (7*B,     'la2',  '7/#3'),
    (7*B+192, 're2',  '5/3'),
)

# Intervalli diatonici sopra il basso. La scala di Re minore include Sib;
# l'alterazione esplicita #3 alza Do a Do# su La dominante.
FIGURES = {
    '5/3': ('3', '5'),
    '6/3': ('3', '6'),
    '6/4': ('4', '6'),
    '7/#3': ('#3', '5', '7'),
    '6/5': ('3', '5', '6'),
}
LETTERS = ('do', 're', 'mi', 'fa', 'sol', 'la', 'si')
D_MINOR = {'do': 0, 're': 2, 'mi': 4, 'fa': 5,
           'sol': 7, 'la': 9, 'si': 10}
NOTE_PATTERN = re.compile(r'^(do|re|mi|fa|sol|la|si)([#b]?)(\d+)$')


def upper_pitch_classes(bass: str, figure: str) -> tuple[int, ...]:
    """Interpreta le cifre come intervalli diatonici sopra il basso reale."""
    match = NOTE_PATTERN.fullmatch(bass)
    if match is None:
        raise ValueError(f'nota di basso non riconosciuta: {bass!r}')
    if figure not in FIGURES:
        raise ValueError(f'cifra non supportata: {figure!r}')
    base = LETTERS.index(match.group(1))
    pcs = []
    for item in FIGURES[figure]:
        sharp = item.startswith('#')
        degree = int(item.lstrip('#'))
        letter = LETTERS[(base + degree - 1) % 7]
        pcs.append((D_MINOR[letter] + int(sharp)) % 12)
    return tuple(pcs)


def _choices(bass: str, figure: str) -> list[tuple[int, int, int]]:
    """Tre voci nell'area centrale, tutte sopra il basso, nel medesimo accordo."""
    pcs = list(upper_pitch_classes(bass, figure))
    if len(pcs) == 2:  # triade: la terza voce raddoppia la nota del basso
        pcs.append(MU.altezza(bass) % 12)
    bottom = MU.altezza(bass)
    alternatives = [[n for n in range(53, 77) if n % 12 == pc]
                    for pc in pcs]
    candidates = set()
    for notes in itertools.product(*alternatives):
        ordered = tuple(sorted(notes))
        if (len(set(ordered)) == 3 and ordered[0] > bottom + 7
                and ordered[-1] - ordered[0] <= 12):
            candidates.add(ordered)
    if not candidates:
        raise ValueError(f'nessuna disposizione per {bass} {figure}')
    return sorted(candidates)


def _parallel_perfects(old_bass: int, old: tuple[int, int, int],
                       new_bass: int, new: tuple[int, int, int]) -> int:
    """Conta 5e/8e parallele fra qualunque coppia delle quattro voci."""
    before, after = (old_bass, *old), (new_bass, *new)
    count = 0
    for lower in range(4):
        for upper in range(lower + 1, 4):
            first = (before[upper] - before[lower]) % 12
            second = (after[upper] - after[lower]) % 12
            moves = (after[lower] - before[lower],
                     after[upper] - before[upper])
            if first == second and first in (0, 7) and moves[0] * moves[1] > 0:
                count += 1
    return count


def realize() -> list[tuple[int, int, str, str, tuple[int, int, int]]]:
    """(tick, durata, basso, cifre, tre note alte) con condotta ravvicinata."""
    result = []
    previous = None
    previous_bass = None
    for index, (pos, bass, figure) in enumerate(SCORE):
        stop = SCORE[index + 1][0] if index + 1 < len(SCORE) else BARS * B
        candidates = _choices(bass, figure)
        if previous is None:
            chosen = min(candidates, key=lambda c: (sum(abs(n - 63) for n in c),
                                                     c[-1] - c[0], c))
        else:
            chosen = min(candidates, key=lambda c: (
                _parallel_perfects(previous_bass, previous,
                                   MU.altezza(bass), c),
                sum(abs(x - y) for x, y in zip(c, previous)),
                sum(abs(n - 63) for n in c), c))
        result.append((pos, stop - pos, bass, figure, chosen))
        previous = chosen
        previous_bass = MU.altezza(bass)
    return result


def bass_line() -> dict[int, list]:
    from delugexml.notes import Note  # noqa: PLC0415

    rows: dict[int, list] = {}
    for pos, duration, bass, _, _ in realize():
        pitch = MU.altezza(bass)
        rows.setdefault(pitch, []).append(
            Note(pos=pos, length=max(1, duration - 12), velocity=82))
    return rows


def upper_realization() -> dict[int, list]:
    """Voci comuni tenute; la superficie si anima nella seconda meta'."""
    from delugexml.notes import Note  # noqa: PLC0415

    rows: dict[int, list] = {}
    events = realize()
    for index, (pos, duration, _, _, notes) in enumerate(events):
        if index and notes == events[index - 1][4]:
            continue  # il basso cambia, le voci superiori restano tenute
        last = index
        while last + 1 < len(events) and events[last + 1][4] == notes:
            last += 1
            duration += events[last][1]
        animated = pos >= 4 * B
        chord_length = min(duration - 12, 72 if animated else duration - 12)
        for pitch in notes:
            rows.setdefault(pitch, []).append(
                Note(pos=pos, length=max(1, chord_length), velocity=64))
        if animated and duration >= 192:
            for offset, pitch in ((96, notes[1]), (144, notes[2])):
                rows.setdefault(pitch, []).append(
                    Note(pos=pos + offset, length=36, velocity=49))
    for notes in rows.values():
        notes.sort(key=lambda n: n.pos)
    return rows


def drums() -> dict[str, list]:
    from delugexml.notes import Note  # noqa: PLC0415

    rows = {KICK: [], RIM: [], HAT: []}
    for bar in range(BARS):
        base = bar * B
        for beat in ((0, 2) if bar < 4 else (0, 2, 3)):
            rows[KICK].append(Note(pos=base + beat * 96, length=P,
                                   velocity=108 if beat == 0 else 84))
        rows[RIM].append(Note(pos=base + 96, length=P, velocity=68))
        rows[HAT].extend(Note(pos=base + offset, length=12, velocity=46)
                         for offset in (48, 144, 240, 336))
    return rows


def costruisci():
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
        for inst in list(S.instruments(doc)):
            MU.togli(doc, inst)

        length = BARS * B
        i_upper, c_upper = C.add_track(
            doc, str(SYNTH), name='CIFRE', folder='SYNTHS',
            length=length, playing=True)
        ST.set_osc(i_upper, 1, type='triangle', transpose=0, cents=0)
        ST.set_osc(i_upper, 2, type='analogSaw', transpose=0, cents=-7)
        SND.set(c_upper, 'oscAVolume', 35)
        SND.set(c_upper, 'oscBVolume', 14)
        SND.set(c_upper, 'envelope1.attack', 3)
        SND.set(c_upper, 'envelope1.sustain', 35)
        SND.set(c_upper, 'envelope1.release', 14)
        MU.scrivi(doc, c_upper, upper_realization())
        S.set_key_mode(c_upper, False)

        i_bass, c_bass = C.add_track(
            doc, str(BASS), name='BASSO', folder='SYNTHS',
            length=length, colour_offset='16', playing=True)
        MU.scrivi(doc, c_bass, bass_line())
        S.set_key_mode(c_bass, False)

        i_kit, c_kit = C.add_track(
            doc, str(KIT), name='BEAT', folder='KITS',
            length=length, colour_offset='32', playing=True)
        for drum, notes in drums().items():
            MU.scrivi(doc, c_kit, notes, dove=drum)

        for inst, clip in ((i_upper, c_upper), (i_bass, c_bass),
                           (i_kit, c_kit)):
            A.place(doc, inst, clip, 0, length)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc


def scrivi(path: Path = OUT) -> Path:
    from delugexml import write_file  # noqa: PLC0415
    from delugexml.writer import FormatTable  # noqa: PLC0415

    doc = costruisci()
    problems = MU.verifica(doc)
    if problems:
        raise ValueError(f'song non valida: {problems}')
    write_file(doc, path, FormatTable.load(ROOT / 'out' / 'format_table.json'))
    return path


if __name__ == '__main__':
    doc = costruisci()
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('bassoc', 1))
