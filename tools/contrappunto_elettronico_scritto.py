"""Una forma elettronica breve che prende due gesti dal Counterpoint di Piston.

16 battute, quattro sezioni di 4:
    A (0-3)   il motivo nasce sul synth; il rim ne marca gli attacchi.
    B (4-7)   risposta del pluck e rim negli spazi del motivo.
    C (8-11)  il motivo passa al pluck un'ottava sopra; cassa dimezzata.
    A' (12-15) il synth torna e il pluck gli risponde; cassa piena.

Il riferimento e' Piston, Counterpoint, cap. 6 (struttura motivica) e
conclusione p. 229 (contrappunto anche fra figure percussive senza altezza).
Scambio di timbro e forma sono scelte compositive, non ricostruzione stilistica.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU  # noqa: E402

B = MU.TICK_PER_BATTUTA
P = MU.TICK_PER_MOVIMENTO // 4
BARS = 16
BPM = 112

TEMPLATE = ROOT / 'refs' / 'songs' / 'TEMPL0.XML'
SYNTH = ROOT / 'refs' / 'synths' / 'TEMPL.XML'
BASS = ROOT / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = ROOT / 'refs' / 'kits' / '808 From Mars.XML'
OUT = ROOT / 'out' / 'CONTRELE01.XML'

KICK = 'BD B 808 Decay C 02'
RIM = 'Rim Shot A 808'
HAT = 'CH Combo 808'

# Quattro attacchi asimmetrici: il profilo resta riconoscibile nel cambio
# di ottava/timbro della sezione C. I tick sono relativi a una battuta.
MOTIF_ONSETS = (0, 72, 168, 264)
MOTIF_LENGTHS = (48, 48, 72, 72)
MOTIF_PITCHES = ('re4', 'fa4', 'mi4', 'do4')


def _merge(*parts: dict[int, list]) -> dict[int, list]:
    merged: dict[int, list] = {}
    for part in parts:
        for pitch, notes in part.items():
            merged.setdefault(pitch, []).extend(notes)
    return merged


def motif(bar: int, *, octave: int = 0, velocity: int = 86) -> dict[int, list]:
    """La stessa cellula con un cambio di registro, senza cambiare il ritmo."""
    pitches = [MU.altezza(name) + 12 * octave for name in MOTIF_PITCHES]
    return MU.linea([(bar * B + onset, pitch, length)
                     for onset, pitch, length in zip(
                         MOTIF_ONSETS, pitches, MOTIF_LENGTHS)],
                    velocity=velocity)


def lead() -> dict[int, list]:
    """A, B e ritorno A': in C cede del tutto il motivo al pluck."""
    return _merge(*(motif(bar) for bar in (0, 2, 4, 6, 12, 14)))


def pluck() -> dict[int, list]:
    """Risposte negli spazi di B/A', poi eredita l'intero motivo in C."""
    answers = []
    for start in (4, 6, 12, 14):
        answers += [
            (start * B + 216, 'la4', 48),
            ((start + 1) * B + 48, 'sol4', 48),
            ((start + 1) * B + 240, 'fa4', 72),
        ]
    return _merge(MU.linea(answers, velocity=72),
                  *(motif(bar, octave=1, velocity=82) for bar in (8, 10)))


def sub() -> dict[int, list]:
    """Perno sul Re; le entrate in levare lasciano liberi i battere del motivo."""
    events = []
    for bar in range(BARS):
        events.extend(((bar * B + 48, 're2', 60),
                       (bar * B + 240, 'la2', 60)))
    return MU.linea(events, velocity=75)


def drums() -> dict[str, list]:
    """Il rim passa dagli attacchi comuni ad accenti complementari."""
    from delugexml.notes import Note  # noqa: PLC0415

    rows = {KICK: [], RIM: [], HAT: []}
    for bar in range(BARS):
        base = bar * B
        kick_beats = (0, 2) if 8 <= bar < 12 else (0, 1, 2, 3)
        rows[KICK].extend(Note(pos=base + beat * 96, length=P, velocity=105)
                          for beat in kick_beats)
        rows[HAT].extend(Note(pos=base + step * P, length=12,
                              velocity=48 if step % 4 else 62)
                         for step in (2, 6, 10, 14))
        # A: unisono ritmico col motivo. B, C e A': risposta nei vuoti.
        if bar < 4:
            rim_onsets = (0, 168) if bar in (0, 2) else ()
        else:
            rim_onsets = (48, 120, 216, 312)
        rows[RIM].extend(Note(pos=base + offset, length=P,
                              velocity=84 if offset in (0, 216) else 68)
                         for offset in rim_onsets)
    return rows


def costruisci():
    """Costruisce la song; la funzione non scrive file e non usa il dispositivo."""
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
            doc, str(SYNTH), name='MOTIVO', folder='SYNTHS',
            length=length, playing=True)
        ST.set_osc(i_lead, 1, type='triangle', transpose=0, cents=0)
        ST.set_osc(i_lead, 2, type='analogSaw', transpose=0, cents=-5)
        SND.set(c_lead, 'oscAVolume', 40)
        SND.set(c_lead, 'oscBVolume', 15)
        SND.set(c_lead, 'envelope1.attack', 4)
        SND.set(c_lead, 'envelope1.release', 17)
        MU.scrivi(doc, c_lead, lead())

        i_pluck, c_pluck = C.add_track(
            doc, str(SYNTH), name='RISPOSTA', folder='SYNTHS',
            length=length, colour_offset='16', playing=True)
        ST.set_osc(i_pluck, 1, type='square', transpose=0, cents=0)
        SND.set(c_pluck, 'oscAVolume', 32)
        SND.set(c_pluck, 'oscBVolume', 0)
        SND.set(c_pluck, 'envelope1.attack', 0)
        SND.set(c_pluck, 'envelope1.sustain', 12)
        SND.set(c_pluck, 'envelope1.release', 9)
        MU.scrivi(doc, c_pluck, pluck())

        i_sub, c_sub = C.add_track(
            doc, str(BASS), name='SUB', folder='SYNTHS',
            length=length, colour_offset='32', playing=True)
        MU.scrivi(doc, c_sub, sub())

        i_kit, c_kit = C.add_track(
            doc, str(KIT), name='PULSE', folder='KITS',
            length=length, colour_offset='48', playing=True)
        for drum, notes in drums().items():
            MU.scrivi(doc, c_kit, notes, dove=drum)

        for inst, clip in ((i_lead, c_lead), (i_pluck, c_pluck),
                           (i_sub, c_sub), (i_kit, c_kit)):
            A.place(doc, inst, clip, 0, length)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc


def scrivi(path: Path = OUT) -> Path:
    """Scrive una song valida con la tabella di formato locale."""
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
    print('destinazione:', MU.destinazione('contrele', 1))
