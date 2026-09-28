"""Cinque variazioni elettroniche sopra un basso ostinato letterale.

Piston, Harmony, 5a ed., cap. 7 p. 94: ground bass = ostinato nella
voce piu grave lungo almeno una frase. La prova isola questa proprieta,
senza chiamare passacaglia ogni suo possibile uso storico.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU  # noqa: E402
from delugexml.notes import Note  # noqa: E402

B = MU.TICK_PER_BATTUTA
GROUND_BARS = 4
CYCLES = 5
BARS = GROUND_BARS * CYCLES
BPM = 106

TEMPLATE = ROOT / 'refs' / 'songs' / 'TEMPL0.XML'
SYNTH = ROOT / 'refs' / 'synths' / 'TEMPL.XML'
BASS = ROOT / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = ROOT / 'refs' / 'kits' / '808 From Mars.XML'
OUT = ROOT / 'out' / 'OSTINATO01.XML'

KICK = 'BD B 808 Decay C 02'
RIM = 'Rim Shot A 808'
HAT = 'CH Combo 808'

# Non e' una semplice ripetizione delle quattro fondamentali: il profilo
# include risposte prima e dopo il movimento centrale della battuta.
GROUND = (
    (0, 're2', 216), (240, 'la2', 120),
    (B, 'do2', 168), (B + 192, 'sol2', 168),
    (2 * B, 'sib1', 216), (2 * B + 240, 'fa2', 120),
    (3 * B, 'la1', 168), (3 * B + 192, 'mi2', 72),
    (3 * B + 288, 'la1', 72),
)

# Ogni battuta corrisponde al centro Dm, C, Bb, A7. I cinque cicli
# trasformano la superficie lasciando fermo il medesimo oggetto grave.
CHORDS = (
    ('re4', 'fa4', 'la4'),
    ('do4', 'mi4', 'sol4'),
    ('sib3', 're4', 'fa4'),
    ('do#4', 'mi4', 'sol4'),
)


def ground_line() -> dict[int, list[Note]]:
    rows: dict[int, list[Note]] = {}
    for pos, pitch, length in GROUND:
        rows.setdefault(MU.altezza(pitch), []).append(
            Note(pos=pos, length=length, velocity=84))
    return rows


def upper_variations() -> dict[int, list[Note]]:
    rows: dict[int, list[Note]] = {}

    def add(pitch: str, pos: int, length: int, velocity: int) -> None:
        rows.setdefault(MU.altezza(pitch), []).append(
            Note(pos=pos, length=length, velocity=velocity))

    for cycle in range(CYCLES):
        for bar, chord in enumerate(CHORDS):
            start = (cycle * GROUND_BARS + bar) * B
            if cycle == 0:  # esposizione: spazio e un accordo breve
                for pitch in chord:
                    add(pitch, start, 240, 56)
            elif cycle == 1:  # figurazione regolare in ottavi
                for index, offset in enumerate(range(0, B, 48)):
                    add(chord[(index + bar) % 3], start + offset, 39, 58)
            elif cycle == 2:  # risposte sincopate in alto
                for offset, member in ((72, 2), (168, 1), (264, 2), (336, 0)):
                    add(chord[member], start + offset, 36, 64)
            elif cycle == 3:  # sottrazione: una sola risposta per battuta
                add(chord[1], start + 240, 96, 46)
            else:  # ripresa: voicing iniziale e frammenti della figurazione
                for pitch in chord:
                    add(pitch, start, 168, 62)
                for offset, member in ((216, 2), (312, 1)):
                    add(chord[member], start + offset, 48, 55)
    for notes in rows.values():
        notes.sort(key=lambda note: note.pos)
    return rows


def drums() -> dict[str, list[Note]]:
    rows = {KICK: [], RIM: [], HAT: []}
    for bar in range(BARS):
        cycle = bar // GROUND_BARS
        start = bar * B
        kick_offsets = (0,) if cycle == 3 else (0, 192)
        for offset in kick_offsets:
            rows[KICK].append(Note(pos=start + offset, length=24,
                                   velocity=106 if offset == 0 else 82))
        if cycle != 3:
            rows[RIM].append(Note(pos=start + 96, length=24, velocity=69))
        if cycle in (1, 2, 4):
            offsets = (48, 144, 240, 336)
        elif cycle == 0:
            offsets = (144, 336)
        else:
            offsets = ()
        rows[HAT].extend(Note(pos=start + offset, length=12, velocity=45)
                         for offset in offsets)
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
        S.set_scale(doc, 'D', 'minore')
        for instrument in list(S.instruments(doc)):
            MU.togli(doc, instrument)

        total = BARS * B
        period = GROUND_BARS * B
        i_upper, c_upper = C.add_track(
            doc, str(SYNTH), name='VARIAZIONI', folder='SYNTHS',
            length=total, playing=True)
        ST.set_osc(i_upper, 1, type='triangle', transpose=0, cents=0)
        ST.set_osc(i_upper, 2, type='analogSaw', transpose=0, cents=-7)
        SND.set(c_upper, 'oscAVolume', 36)
        SND.set(c_upper, 'oscBVolume', 12)
        SND.set(c_upper, 'envelope1.attack', 2)
        SND.set(c_upper, 'envelope1.sustain', 30)
        SND.set(c_upper, 'envelope1.release', 10)
        S.set_key_mode(c_upper, False)
        MU.scrivi(doc, c_upper, upper_variations())

        i_bass, c_bass = C.add_track(
            doc, str(BASS), name='GROUND', folder='SYNTHS',
            length=period, colour_offset='16', playing=True)
        S.set_key_mode(c_bass, False)
        MU.scrivi(doc, c_bass, ground_line())

        i_kit, c_kit = C.add_track(
            doc, str(KIT), name='BEAT', folder='KITS',
            length=total, colour_offset='32', playing=True)
        for drum, notes in drums().items():
            MU.scrivi(doc, c_kit, notes, dove=drum)

        A.place(doc, i_upper, c_upper, 0, total)
        for cycle in range(CYCLES):
            A.place(doc, i_bass, c_bass, cycle * period, period)
        A.place(doc, i_kit, c_kit, 0, total)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc


def scrivi(path: Path = OUT) -> Path:
    from delugexml import write_file  # noqa: PLC0415
    from delugexml.writer import FormatTable  # noqa: PLC0415

    doc = costruisci()
    errors = MU.verifica(doc)
    if errors:
        raise ValueError(f'song non valida: {errors}')
    write_file(doc, path, FormatTable.load(ROOT / 'out' / 'format_table.json'))
    return path


if __name__ == '__main__':
    doc = costruisci()
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('ostinato', 1))
