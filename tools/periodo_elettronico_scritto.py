"""Due frasi 4+4 sul Deluge: domanda sulla dominante, risposta sulla tonica.

Piston, Harmony, 5a ed., cap. 11 p. 175 (semicadenza) e cap. 13 p. 212
(periodo: due frasi bilanciate, la seconda con chiusura piu' finale).
Il beat e i synth sono scelte elettroniche; non si ricostruisce uno stile.
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
BPM = 108

TEMPLATE = ROOT / 'refs' / 'songs' / 'TEMPL0.XML'
SYNTH = ROOT / 'refs' / 'synths' / 'TEMPL.XML'
BASS = ROOT / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = ROOT / 'refs' / 'kits' / '808 From Mars.XML'
OUT = ROOT / 'out' / 'PERIODO01.XML'

KICK = 'BD B 808 Decay C 02'
RIM = 'Rim Shot A 808'
HAT = 'CH Combo 808'

# Il primo emistichio torna letteralmente all'inizio della seconda frase.
OPENING = ((0, 're4', 72), (96, 'fa4', 72), (192, 'la4', 144),
           (B, 'sol4', 72), (B + 96, 'sib4', 72),
           (B + 192, 'la4', 72), (B + 288, 'fa4', 72))

ANTECEDENT_END = ((2 * B, 'mi4', 96), (2 * B + 96, 'fa4', 96),
                  (2 * B + 192, 'mi4', 96), (2 * B + 288, 're4', 72),
                  (3 * B, 'do#4', 96), (3 * B + 96, 'mi4', 96),
                  (3 * B + 192, 'do#5', 144))

CONSEQUENT_END = ((2 * B, 'mi4', 96), (2 * B + 96, 'sol4', 96),
                  (2 * B + 192, 'mi4', 96), (2 * B + 288, 'do#5', 72),
                  (3 * B, 're5', 336))

# Le prime due armonie tornano; la prima frase termina su A (V), la seconda
# prepara A7 e risolve su Dm (i). Identica pausa di 48 tick dopo le due cadenze.
CHORDS = (
    ('re3', 'fa3', 'la3'), ('sol3', 'sib3', 're4'),
    ('re3', 'fa3', 'la3'), ('la3', 'do#4', 'mi4'),
    ('re3', 'fa3', 'la3'), ('sol3', 'sib3', 're4'),
    ('la3', 'do#4', 'mi4', 'sol4'), ('re3', 'fa3', 'la3'),
)
ROOTS = ('re2', 'sol2', 're2', 'la2', 're2', 'sol2', 'la2', 're2')


def antecedente() -> dict[int, list]:
    return MU.linea((*OPENING, *ANTECEDENT_END), velocity=84)


def conseguente() -> dict[int, list]:
    events = tuple((tick + 4 * B, pitch, duration)
                   for tick, pitch, duration in (*OPENING, *CONSEQUENT_END))
    return MU.linea(events, velocity=84)


def melodia() -> dict[int, list]:
    voice = antecedente()
    for pitch, notes in conseguente().items():
        voice.setdefault(pitch, []).extend(notes)
    return voice


def armonia() -> dict[int, list]:
    events = [(bar * B, pitch, 336 if bar in (3, 7) else B)
              for bar, chord in enumerate(CHORDS) for pitch in chord]
    return MU.linea(events, velocity=54)


def basso() -> dict[int, list]:
    return MU.linea([(bar * B, root, 336 if bar in (3, 7) else B)
                     for bar, root in enumerate(ROOTS)], velocity=79)


def batteria() -> dict[str, list]:
    """Groove stabile; la stessa breve pausa rende udibili entrambe le fini."""
    from delugexml.notes import Note  # noqa: PLC0415

    rows = {KICK: [], RIM: [], HAT: []}
    for bar in range(BARS):
        base = bar * B
        end_bar = bar in (3, 7)
        for beat in ((0, 1, 2) if end_bar else (0, 1, 2, 3)):
            rows[KICK].append(Note(pos=base + beat * 96, length=P,
                                   velocity=104 if beat == 0 else 91))
        for beat in ((1,) if end_bar else (1, 3)):
            rows[RIM].append(Note(pos=base + beat * 96, length=P, velocity=72))
        for offset in ((48, 144, 240) if end_bar else (48, 144, 240, 336)):
            rows[HAT].append(Note(pos=base + offset, length=12, velocity=52))
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
            doc, str(SYNTH), name='FRASE', folder='SYNTHS',
            length=length, playing=True)
        ST.set_osc(i_lead, 1, type='triangle', transpose=0, cents=0)
        ST.set_osc(i_lead, 2, type='analogSaw', transpose=0, cents=-4)
        SND.set(c_lead, 'oscAVolume', 40)
        SND.set(c_lead, 'oscBVolume', 14)
        SND.set(c_lead, 'envelope1.attack', 4)
        SND.set(c_lead, 'envelope1.release', 15)
        MU.scrivi(doc, c_lead, melodia())

        i_pad, c_pad = C.add_track(
            doc, str(SYNTH), name='ARMONIA', folder='SYNTHS',
            length=length, colour_offset='16', playing=True)
        ST.set_osc(i_pad, 1, type='triangle', transpose=0, cents=0)
        ST.set_osc(i_pad, 2, type='analogSaw', transpose=0, cents=-7)
        SND.set(c_pad, 'oscAVolume', 26)
        SND.set(c_pad, 'oscBVolume', 12)
        SND.set(c_pad, 'envelope1.attack', 12)
        SND.set(c_pad, 'envelope1.sustain', 40)
        SND.set(c_pad, 'envelope1.release', 14)
        MU.scrivi(doc, c_pad, armonia())

        i_bass, c_bass = C.add_track(
            doc, str(BASS), name='BASSO', folder='SYNTHS',
            length=length, colour_offset='32', playing=True)
        MU.scrivi(doc, c_bass, basso())

        i_kit, c_kit = C.add_track(
            doc, str(KIT), name='BEAT', folder='KITS',
            length=length, colour_offset='48', playing=True)
        for drum, notes in batteria().items():
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
    print('destinazione:', MU.destinazione('periodo', 1))
