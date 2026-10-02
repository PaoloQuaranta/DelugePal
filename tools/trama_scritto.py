"""TRAMA03: IDM cameristica originale in forma narrativa, 58 battute.

Conserva tema, ground e forma di TRAMA02, ma ne corregge il risultato
d'ascolto: batteria continua, una sola voce superiore fitta alla volta, un
solo episodio a tre parti e tre identita timbriche strutturalmente distinte.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU  # noqa: E402
from delugexml.notes import Note  # noqa: E402
import tema_variazioni_scritto as TV  # noqa: E402

B = MU.TICK_PER_BATTUTA
BPM = 102
TOTAL_BARS = 58
VERSION = 3

INTRO = (0, 6)
A = (6, 14)
A_VAR = (14, 22)
BUILD = (22, 32)
DEVELOPMENT = (32, 44)
RETURN = (44, 52)
CODA = (50, 58)
THREE_PART_BARS = (36, 40)
FILL_BARS = (21, 31, 43, 51)
SECTIONS = (
    ('intro', *INTRO), ('A', *A), ('A-var', *A_VAR),
    ('build', *BUILD), ('sviluppo', *DEVELOPMENT),
    ('ritorno', *RETURN), ('coda', *CODA),
)

TEMPLATE = ROOT / 'refs' / 'songs' / 'TEMPL0.XML'
SYNTH = ROOT / 'refs' / 'synths' / 'TEMPL.XML'
BASS_PRESET = ROOT / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = ROOT / 'refs' / 'kits' / '808 From Mars.XML'
OUT = ROOT / 'out' / 'TRAMA03.XML'

KICK = 'BD B 808 Decay C 02'
RIM = 'Rim Shot A 808'
HAT = 'CH Combo 808'

# Il basso della variazione a tre parti e' gia stato verificato contro entrambe
# le voci superiori. Diventa il ground letterale del brano.
GROUND = TV.THIRD_C
GROUND_STARTS = (6, 10, 14, 18, 32, 36, 40, 44, 48)


def _eventi(voce: dict[int, list[Note]]):
    return sorted((note.pos, pitch, note.length, note.velocity)
                  for pitch, row in voce.items() for note in row)


def _da_eventi(events) -> dict[int, list[Note]]:
    result: dict[int, list[Note]] = {}
    for pos, pitch, length, velocity in events:
        result.setdefault(pitch, []).append(
            Note(pos=pos, length=length, velocity=velocity))
    for notes in result.values():
        notes.sort(key=lambda note: note.pos)
    return result


def _sposta(voce: dict[int, list[Note]], offset: int,
            *, transpose: int = 0, velocity: int = 0) -> dict[int, list[Note]]:
    return _da_eventi((pos + offset, pitch + transpose, length,
                       max(1, min(127, vel + velocity)))
                      for pos, pitch, length, vel in _eventi(voce))


def _unisci(*voci: dict[int, list[Note]]) -> dict[int, list[Note]]:
    return _da_eventi(event for voce in voci for event in _eventi(voce))


def _linea(score, *, velocity: int) -> dict[int, list[Note]]:
    return MU.linea(tuple(score), velocity=velocity, stacco=0)


def _note_assolute(events) -> dict[int, list[Note]]:
    """Crea una linea da eventi (pos, nome/numero, durata, velocity)."""
    rows: dict[int, list[Note]] = {}
    for pos, pitch, length, velocity in events:
        midi = MU.altezza(pitch) if isinstance(pitch, str) else pitch
        rows.setdefault(midi, []).append(
            Note(pos=pos, length=length, velocity=velocity))
    for notes in rows.values():
        notes.sort(key=lambda note: note.pos)
    return rows


def sviluppo_tre_parti() -> tuple[dict[int, list[Note]], ...]:
    """La cellula contrappuntistica di quattro battute dello sviluppo."""
    return TV.variazione_tre_parti()


def coda_aumentata() -> dict[int, list[Note]]:
    """Tema al doppio della durata e un'ottava sotto, relativo alla coda."""
    return _da_eventi((pos * 2, pitch - 12, length * 2, velocity - 8)
                      for pos, pitch, length, velocity
                      in _eventi(TV.tema_alta()))


def _lead_build() -> dict[int, list[Note]]:
    """La build cresce in registro e dinamica, non nel numero di attacchi."""
    cells = {
        22: (('sib4', 48), ('sol4', 240)),
        23: (('fa4', 96), ('la4', 288)),
        26: (('sol4', 48), ('re5', 264)),
        27: (('sib4', 96), ('mi5', 288)),
        30: (('la4', 48), ('fa5', 264)),
    }
    out = []
    for bar, notes in cells.items():
        for index, (pitch, offset) in enumerate(notes):
            out.append((bar * B + offset, pitch, 90 if index else 132,
                        58 + (bar - 22) * 2))
    return _note_assolute(out)


def _counter_build() -> dict[int, list[Note]]:
    cells = {
        24: (('re3', 48), ('fa3', 288)),
        25: (('sib2', 96), ('re3', 240)),
        28: (('sol2', 48), ('mib3', 288)),
        29: (('la2', 96), ('do#3', 264)),
    }
    out = []
    for bar, notes in cells.items():
        for index, (pitch, offset) in enumerate(notes):
            out.append((bar * B + offset, pitch, 78 if index else 156,
                        54 + (bar - 22) * 2))
    return _note_assolute(out)


def _intro_lead() -> dict[int, list[Note]]:
    return _note_assolute((
        (2 * B + 240, 'sib4', 96, 48),
        (3 * B + 144, 'sol4', 120, 52),
        (4 * B + 240, 'sib4', 72, 58),
        (5 * B + 96, 'sol4', 120, 62),
        (5 * B + 288, 'fa4', 72, 58),
    ))


def _lead_answers() -> dict[int, list[Note]]:
    """Quattro risposte lunghe sopra la presentazione della controvoce."""
    return _note_assolute(tuple(
        ((10 + index) * B + 288, pitch, 78, 52 + index * 2)
        for index, pitch in enumerate(('re5', 'la4', 'sol4', 'la4'))))


def _lead_variation() -> dict[int, list[Note]]:
    """Variazione cameristica: il motivo respira fra coppie di attacchi."""
    return _note_assolute((
        (14 * B + 48, 'sib4', 156, 61), (14 * B + 288, 'sol4', 72, 56),
        (15 * B + 96, 'fa4', 180, 59),
        (16 * B + 48, 'la4', 120, 63), (16 * B + 264, 'mi4', 96, 58),
        (17 * B + 144, 'sol4', 144, 62),
    ))


def _counter_colour() -> dict[int, list[Note]]:
    """Risposta scura, separata dalla variazione del lead."""
    return _note_assolute((
        (18 * B + 48, 're3', 180, 54), (18 * B + 288, 'fa3', 72, 49),
        (19 * B + 144, 'mib3', 156, 56),
        (20 * B + 48, 'sib2', 180, 57), (20 * B + 288, 're3', 72, 52),
        (21 * B + 144, 'do#3', 144, 60),
    ))


def _development_lead() -> dict[int, list[Note]]:
    return _note_assolute((
        (32 * B + 48, 're5', 180, 64), (32 * B + 288, 'sib4', 72, 57),
        (33 * B + 144, 'sol4', 168, 60),
        (34 * B + 48, 'la4', 180, 66), (34 * B + 288, 'mi5', 72, 61),
        (35 * B + 144, 'fa5', 156, 68),
    ))


def _thin_three_parts() -> tuple[dict[int, list[Note]], dict[int, list[Note]]]:
    """Alterna la voce attiva dentro la sola finestra a tre parti."""
    lead, counter, _ = sviluppo_tre_parti()

    def thin(voce, busy_bars):
        selected = []
        grouped = {bar: [] for bar in range(4)}
        for event in _eventi(voce):
            grouped[min(3, event[0] // B)].append(event)
        for bar, events in grouped.items():
            selected.extend(events if bar in busy_bars else events[:1])
        return _da_eventi(selected)

    return thin(lead, {0, 2}), thin(counter, {1, 3})


def _lead_climax_and_return_tail() -> dict[int, list[Note]]:
    """Il culmine e' alto e lungo; il ritorno lascia due tracce nella coda."""
    return _note_assolute((
        (40 * B + 48, 'fa5', 240, 72),
        (41 * B + 96, 'mi5', 192, 70),
        (42 * B + 144, 're5', 168, 67),
        (48 * B + 48, 'sib4', 156, 62), (48 * B + 288, 'sol4', 72, 57),
        (49 * B + 144, 'fa4', 156, 59),
        (50 * B + 288, 'la4', 72, 54),
        (51 * B + 240, 're5', 96, 50),
    ))


def _pad() -> dict[int, list[Note]]:
    rows: dict[int, list[Note]] = {}

    def chord(start_bar: int, bars: int, names, velocity: int) -> None:
        for name in names:
            rows.setdefault(MU.altezza(name), []).append(
                Note(pos=start_bar * B, length=bars * B, velocity=velocity))

    # Campo lento: dyad e note singole, mai una terza melodia implicita.
    chord(0, 2, ('re3', 'la3'), 34)
    chord(2, 2, ('sib2', 'fa3'), 36)
    chord(4, 2, ('re3', 'la3'), 38)
    ground_harmony = (
        ('re3', 'mi4'), ('sib2', 'la3'),
        ('sol2', 'la3'), ('la2', 'sol3'),
    )
    for section, velocity in ((6, 39), (44, 43)):
        for index, names in enumerate(ground_harmony):
            chord(section + 2 * index, 2, names, velocity + index)
    for index, names in enumerate(ground_harmony):
        chord(14 + 2 * index, 2, names[:1], 38 + index)
    build_harmony = (
        ('re3', 'la3'), ('sib2', 'la3'), ('sol2', 're3'),
        ('mib3', 'sib3'), ('la2', 'mi3'),
    )
    for index, names in enumerate(build_harmony):
        chord(22 + 2 * index, 2, names, 38 + index * 2)
    chord(32, 4, ('re3', 'la3'), 38)
    # 36-40 resta davvero a tre parti: lead, controvoce, basso.
    chord(40, 3, ('la2', 'mi3'), 43)
    chord(52, 2, ('re3', 'fa3'), 38)
    chord(54, 2, ('re3', 'la3'), 35)
    chord(56, 2, ('re3',), 31)
    for notes in rows.values():
        notes.sort(key=lambda note: note.pos)
    return rows


def _bass_build() -> dict[int, list[Note]]:
    events = []
    roots = ('re2', 're2', 'sib1', 'sib1', 'sol1',
             'sol1', 'mib2', 'mib2', 'la1', 'la1')
    for index, root in enumerate(roots):
        start = (22 + index) * B
        events.append((start, root, 216, 70 + index))
        if index < 9:
            fifth = MU.nome_altezza(MU.altezza(root) + 7)
            events.append((start + 264, fifth, 96, 62 + index))
    return _note_assolute(events)


def _bass() -> dict[int, list[Note]]:
    ground = _linea(GROUND, velocity=72)
    voices = [_sposta(ground, start * B) for start in GROUND_STARTS]
    intro = _note_assolute(((0, 're2', 2 * B, 46),
                            (2 * B, 'sib1', 2 * B, 48),
                            (4 * B, 'la1', 2 * B, 52)))
    pedal = _note_assolute(((52 * B, 're2', 6 * B, 54),))
    return _unisci(intro, _bass_build(), pedal, *voices)


def parti_complete() -> tuple[dict[int, list[Note]], ...]:
    """Lead, controvoce, pad e basso sull'intera forma."""
    thin_lead, thin_counter = _thin_three_parts()

    lead = _unisci(
        _intro_lead(),
        _sposta(TV.tema_alta(), 6 * B),
        _lead_answers(),
        _lead_variation(),
        _lead_build(),
        _development_lead(),
        _sposta(thin_lead, 36 * B),
        _lead_climax_and_return_tail(),
        _sposta(TV.tema_alta(), 44 * B, velocity=5),
    )
    counter = _unisci(
        _sposta(TV.tema_bassa(), 10 * B),
        _counter_colour(),
        _counter_build(),
        _sposta(thin_counter, 36 * B),
        _sposta(coda_aumentata(), CODA[0] * B),
    )
    pad = _pad()
    return lead, counter, pad, _bass()


def batteria() -> dict[str, list[Note]]:
    """Groove stabile; le sezioni sottraggono layer, i giunti soli riempiono."""
    rows = {KICK: [], RIM: [], HAT: []}

    def hit(drum: str, bar: int, offset: int, velocity: int,
            length: int = 18) -> None:
        rows[drum].append(Note(pos=bar * B + offset, length=length,
                               velocity=velocity))

    for bar in range(TOTAL_BARS):
        if bar < 4:
            continue
        if bar < 6:
            kick, rim, hats = (0,), (), (144, 336)
        elif bar < 52:
            kick, rim = (0, 216), (96, 288)
            if bar in (10, 11, 18, 19, 24, 25, 32, 33, 50, 51):
                hats = (48, 240)
            elif bar in (30, 31, 42, 43):
                hats = ()
            else:
                hats = (48, 144, 240, 336)
            if bar in FILL_BARS:
                kick += (336,)
                rim += (360,)
                hats += (312,)
        elif bar < 54:
            kick, rim, hats = (0, 216), (96,), (48, 240)
        elif bar < 56:
            kick, rim, hats = (0,), (), (144,)
        elif bar == 56:
            kick, rim, hats = (0,), (), ()
        else:
            kick, rim, hats = (), (), ()
        for offset in kick:
            hit(KICK, bar, offset, 104 if offset == 0 else 82, 24)
        for offset in rim:
            hit(RIM, bar, offset, 72 if offset in (96, 288) else 64, 18)
        for index, offset in enumerate(hats):
            hit(HAT, bar, offset, 46 + (index % 2) * 6, 12)
    return rows


def costruisci():
    """Costruisce TRAMA03 senza scrivere file o usare il dispositivo."""
    import warnings  # noqa: PLC0415
    from delugexml import parse_file, song as S, create as C  # noqa: PLC0415
    from delugexml import arranger as AR, structure as ST  # noqa: PLC0415
    from delugexml import sound as SND, synthesis as SY  # noqa: PLC0415
    from delugexml import effects as FX  # noqa: PLC0415

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(str(TEMPLATE))
        S.set_bpm(doc.root, BPM)
        S.set_swing(doc, 54, figura='1/8')
        S.set_scale(doc, 'D', 'minore')
        for instrument in list(S.instruments(doc)):
            MU.togli(doc, instrument)

        total = TOTAL_BARS * B
        specs = (('FILO', SYNTH, '0'), ('OMBRA', SYNTH, '16'),
                 ('CAMPO', SYNTH, '30'), ('GROUND', BASS_PRESET, '44'))
        for notes, spec in zip(parti_complete(), specs):
            name, preset, colour = spec
            instrument, clip = C.add_track(
                doc, str(preset), name=name, folder='SYNTHS', length=total,
                colour_offset=colour, playing=True)
            if name == 'FILO':
                op = SY.DX7Operator
                operators = (
                    op(rates=(99, 72, 42, 58), levels=(99, 62, 0, 0),
                       level=82, coarse=1, velocity=5, detune=7),
                    op(rates=(99, 83, 50, 62), levels=(99, 44, 0, 0),
                       level=67, coarse=5, fine=19, velocity=4, detune=8),
                    op(rates=(99, 69, 38, 55), levels=(99, 58, 0, 0),
                       level=74, coarse=2, velocity=4, detune=6),
                    op(rates=(99, 78, 47, 61), levels=(99, 39, 0, 0),
                       level=61, coarse=7, fine=31, velocity=5, detune=9),
                    op(rates=(99, 65, 34, 51), levels=(99, 54, 0, 0),
                       level=66, coarse=3, velocity=3, detune=7),
                    op(rates=(99, 76, 45, 59), levels=(99, 36, 0, 0),
                       level=55, coarse=11, fine=8, velocity=4, detune=5),
                )
                SY.set_dx7(instrument, SY.DX7Patch(
                    operators, algorithm=5, feedback=1, lfo_speed=18,
                    name='TRAMA FILO'), params_node=clip)
                ST.set_filter(instrument, lpf='12dB', hpf='HPLadder', route='H2L')
                for param, value in (
                        ('volume', 25), ('lpfFrequency', 44),
                        ('lpfResonance', 4), ('hpfFrequency', 11),
                        ('envelope1.attack', 0), ('envelope1.sustain', 8),
                        ('envelope1.release', 19)):
                    SND.set(clip, param, value)
                SND.set_patch_cable(clip, 'velocity', 'lpfFrequency', 8)
                FX.set_delay(instrument, analog=False, ping_pong=True,
                             sync_level=7, sync_type='dotted', feedback=11,
                             params_node=clip)
                FX.set_reverb_send(clip, 17)
            elif name == 'OMBRA':
                ST.set_synth_mode(instrument, 'ringmod')
                ST.set_osc(instrument, 1, type='analogSquare', transpose=0, cents=0)
                ST.set_osc(instrument, 2, type='sine', transpose=12, cents=7)
                ST.set_filter(instrument, lpf='SVF_Band', hpf='Off', route='H2L')
                for param, value in (
                        ('volume', 23), ('oscAVolume', 32), ('oscBVolume', 22),
                        ('lpfFrequency', 29), ('lpfResonance', 13),
                        ('envelope1.attack', 2), ('envelope1.decay', 24),
                        ('envelope1.sustain', 9), ('envelope1.release', 10),
                        ('envelope2.attack', 0), ('envelope2.decay', 17),
                        ('envelope2.sustain', 0), ('envelope2.release', 7)):
                    SND.set(clip, param, value)
                SND.set_patch_cable(clip, 'envelope2', 'lpfFrequency', 17)
                SND.set_patch_cable(clip, 'velocity', 'oscBVolume', 8)
                FX.set_distortion(instrument, saturation=3, params_node=clip)
                FX.set_reverb_send(clip, 11)
            elif name == 'CAMPO':
                ST.set_osc(instrument, 1, type='analogSaw', transpose=0, cents=0)
                ST.set_osc(instrument, 2, type='triangle', transpose=-12, cents=-7)
                ST.set_unison(instrument, num=2, detune=5, spread=18)
                ST.set_lfo(instrument, 1, type='rwalk')
                ST.set_filter(instrument, lpf='SVF_Notch', hpf='HPLadder', route='L2H')
                for param, value in (
                        ('volume', 21), ('oscAVolume', 21), ('oscBVolume', 25),
                        ('waveFold', 8), ('lpfFrequency', 32),
                        ('lpfResonance', 10), ('hpfFrequency', 8),
                        ('lfo1Rate', 3), ('envelope1.attack', 22),
                        ('envelope1.sustain', 39), ('envelope1.release', 33)):
                    SND.set(clip, param, value)
                SND.set_patch_cable(clip, 'lfo1', 'lpfFrequency', 7)
                SND.set_patch_cable(clip, 'random', 'pan', 9)
                FX.set_mod_fx(instrument, kind='grainFX', rate=3, depth=17,
                              feedback=6, params_node=clip)
                FX.set_reverb_send(clip, 29)
            S.set_key_mode(clip, False)
            MU.scrivi(doc, clip, notes)
            AR.place(doc, instrument, clip, 0, total)

        kit, clip_kit = C.add_track(
            doc, str(KIT), name='TRAMA BEAT', folder='KITS', length=total,
            colour_offset='56', playing=True)
        for drum, notes in batteria().items():
            MU.scrivi(doc, clip_kit, notes, dove=drum)
        AR.place(doc, kit, clip_kit, 0, total)

        AR.fit_view(doc)
        AR.open_in_arranger(doc)
    return doc


def scrivi(path: Path = OUT) -> Path:
    """Scrive soltanto la revisione canonica, senza poter toccare TRAMA02."""
    from delugexml import write_file  # noqa: PLC0415
    from delugexml.writer import FormatTable  # noqa: PLC0415

    path = Path(path)
    if path.resolve() != OUT.resolve():
        raise ValueError(f'TRAMA03 si scrive soltanto in {OUT}')
    doc = costruisci()
    errors = MU.verifica(doc)
    warnings = MU.avvertenze(doc)
    if errors or warnings:
        raise ValueError(f'song non pronta: errori={errors}, avvertenze={warnings}')
    write_file(doc, path, FormatTable.load(ROOT / 'out' / 'format_table.json'))
    return path


if __name__ == '__main__':
    doc = costruisci()
    print('forma:', ' / '.join(name for name, _, _ in SECTIONS))
    print('durata:', TOTAL_BARS, 'battute @', BPM, 'BPM')
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('trama', VERSION))
