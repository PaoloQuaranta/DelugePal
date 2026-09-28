"""Sequenza tonale in tre riprese, poi rottura e cadenza elettronica.

Piston, Harmony, 5a ed., cap. 20, pp. 315-318: trasposizione sistematica
del disegno melodico, ritmico e armonico; tre apparizioni stabiliscono la
sequenza; la terza spesso precede la rottura della simmetria.

Tre gruppi di due battute: Dm-Gm, Eo-Am, F-Bb, con fondamentali che salgono
di un grado nella scala di Re minore. Poi A7-Dm, con il motivo ritmico
compresso e una risoluzione. Beat e timbri restano elettronici.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU  # noqa: E402

B = MU.TICK_PER_BATTUTA
P = MU.TICK_PER_MOVIMENTO // 4
BARS = 8
BPM = 112

TEMPLATE = ROOT / 'refs' / 'songs' / 'TEMPL0.XML'
SYNTH = ROOT / 'refs' / 'synths' / 'TEMPL.XML'
BASS = ROOT / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = ROOT / 'refs' / 'kits' / '808 From Mars.XML'
OUT = ROOT / 'out' / 'SEQUENZA01.XML'

KICK = 'BD B 808 Decay C 02'
RIM = 'Rim Shot A 808'
HAT = 'CH Combo 808'

# Ogni coppia di armonie forma un'unità da trasporre di un grado diatonico.
# La qualità degli accordi cambia per restare nella tonalità: sequenza tonale.
TRIADS = (
    ('re', 'fa', 'la'), ('sol', 'sib', 're'),
    ('mi', 'sol', 'sib'), ('la', 'do', 'mi'),
    ('fa', 'la', 'do'), ('sib', 're', 'fa'),
)
LEAD_TRIADS = (
    ('re4', 'fa4', 'la4'), ('sol4', 'sib4', 're5'),
    ('mi4', 'sol4', 'sib4'), ('la4', 'do5', 'mi5'),
    ('fa4', 'la4', 'do5'), ('sib4', 're5', 'fa5'),
)
CADENCE = (('la', 'do#', 'mi', 'sol'), ('re', 'fa', 'la'))
MOTIF_ONSETS = (0, 72, 168, 264)
MOTIF_LENGTHS = (48, 72, 72, 96)


def tonal_sequence() -> dict[int, list]:
    """Sei misure in tre coppie: stesso ritmo/profilo, gradi in ascesa."""
    events = []
    for bar, chord in enumerate(LEAD_TRIADS):
        pitches = (chord[0], chord[1], chord[2], chord[1])
        events.extend((bar * B + onset, pitch, duration)
                      for onset, pitch, duration in zip(
                          MOTIF_ONSETS, pitches, MOTIF_LENGTHS))
    return MU.linea(events, velocity=82)


def break_and_cadence() -> dict[int, list]:
    """Figura piu' rapida su A7, poi una nota lunga su Re minore."""
    events = [(6 * B + i * 48, name, 42)
              for i, name in enumerate(
                  ('la4', 'sol4', 'mi4', 'do#5',
                   'la4', 'sol4', 'mi4', 'do#5'))]
    events.append((7 * B, 're5', 336))
    return MU.linea(events, velocity=84)


def lead() -> dict[int, list]:
    notes = tonal_sequence()
    for pitch, row in break_and_cadence().items():
        notes.setdefault(pitch, []).extend(row)
    return notes


def chords() -> dict[int, list]:
    events = []
    for bar, chord in enumerate((*TRIADS, *CADENCE)):
        for name in chord:
            events.append((bar * B, name + '3', 336 if bar == 7 else B))
    return MU.linea(events, velocity=49)


def bass() -> dict[int, list]:
    roots = [chord[0] + '2' for chord in (*TRIADS, *CADENCE)]
    return MU.linea([(bar * B, root, 336 if bar == 7 else B)
                     for bar, root in enumerate(roots)], velocity=79)


def drums() -> dict[str, list]:
    from delugexml.notes import Note  # noqa: PLC0415

    rows = {KICK: [], RIM: [], HAT: []}
    for bar in range(BARS):
        base = bar * B
        beats = (0, 1, 2, 3) if bar == 6 else (0, 2)
        if bar == 7:
            beats = (0, 2)
        rows[KICK].extend(Note(pos=base + beat * 96, length=P,
                               velocity=105 if beat == 0 else 88)
                          for beat in beats)
        rows[RIM].append(Note(pos=base + 96, length=P, velocity=74))
        rows[HAT].extend(Note(pos=base + step * 48, length=12,
                              velocity=44 if step % 2 else 55)
                         for step in range(8 if bar != 7 else 7))
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
        i_lead, c_lead = C.add_track(
            doc, str(SYNTH), name='SEQUENZA', folder='SYNTHS',
            length=length, playing=True)
        ST.set_osc(i_lead, 1, type='triangle', transpose=0, cents=0)
        ST.set_osc(i_lead, 2, type='analogSaw', transpose=0, cents=-5)
        SND.set(c_lead, 'oscAVolume', 40)
        SND.set(c_lead, 'oscBVolume', 17)
        SND.set(c_lead, 'envelope1.attack', 2)
        SND.set(c_lead, 'envelope1.release', 13)
        MU.scrivi(doc, c_lead, lead())

        i_pad, c_pad = C.add_track(
            doc, str(SYNTH), name='ARMONIA', folder='SYNTHS',
            length=length, colour_offset='16', playing=True)
        ST.set_osc(i_pad, 1, type='triangle', transpose=0, cents=0)
        ST.set_osc(i_pad, 2, type='analogSaw', transpose=0, cents=-7)
        SND.set(c_pad, 'oscAVolume', 25)
        SND.set(c_pad, 'oscBVolume', 12)
        SND.set(c_pad, 'envelope1.attack', 12)
        SND.set(c_pad, 'envelope1.sustain', 42)
        SND.set(c_pad, 'envelope1.release', 14)
        MU.scrivi(doc, c_pad, chords())

        i_bass, c_bass = C.add_track(
            doc, str(BASS), name='BASSO', folder='SYNTHS',
            length=length, colour_offset='32', playing=True)
        MU.scrivi(doc, c_bass, bass())

        i_kit, c_kit = C.add_track(
            doc, str(KIT), name='BEAT', folder='KITS',
            length=length, colour_offset='48', playing=True)
        for drum, notes in drums().items():
            MU.scrivi(doc, c_kit, notes, dove=drum)

        for inst, clip in ((i_lead, c_lead), (i_pad, c_pad),
                           (i_bass, c_bass), (i_kit, c_kit)):
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
    print('destinazione:', MU.destinazione('sequenza', 1))
