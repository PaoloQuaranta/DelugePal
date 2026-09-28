"""Doppio contrappunto all'ottava, in due disposizioni sul Deluge.

Piston, *Counterpoint* (1970), capp. 9-10: due linee sono invertibili quando
possono scambiarsi la posizione verticale conservando la propria identita' e
un rapporto musicale valido. Qui A e B durano quattro battute; nella seconda
passata A scende di un'ottava e B sale di un'ottava, senza altre modifiche.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU  # noqa: E402

B = MU.TICK_PER_BATTUTA
PASSAGE_BARS = 4
TOTAL_BARS = 8
BPM = 102

TEMPLATE = ROOT / 'refs' / 'songs' / 'TEMPL0.XML'
SYNTH = ROOT / 'refs' / 'synths' / 'TEMPL.XML'
OUT = ROOT / 'out' / 'INVERT01.XML'

# Le linee condividono soltanto due attacchi su tredici. Gli intervalli forti
# sono scelti per restare consonanti anche quando l'ordine verticale si
# capovolge: nessuna quinta che, invertita, diventerebbe una quarta.
LINE_A = (
    (0,       'sib4', 72), (96,      'sol4', 120),
    (240,     'sib4', 120), (B+48,   'sol4', 120),
    (B+192,   'mi4', 72), (B+288,    'fa4', 96),
    (2*B,     'sol4', 72), (2*B+144, 'fa4', 72),
    (2*B+240, 'mi4', 72), (2*B+336,  'fa4', 48),
    (3*B,     'sol4', 168), (3*B+192, 'sib4', 72),
    (3*B+288, 'do5', 96),
)

LINE_B = (
    (0,       'sol3', 168), (192,     'sib3', 72),
    (288,     'sol3', 96), (B,        'mi3', 120),
    (B+144,   'sol3', 72), (B+240,    'la3', 144),
    (2*B+48,  'sib3', 120), (2*B+192, 'la3', 72),
    (2*B+288, 'sol3', 96), (3*B,      'sib3', 72),
    (3*B+96,  'sol3', 120), (3*B+240, 'mi3', 72),
    (3*B+336, 'fa3', 48),
)


def _linea(score, *, da: int = 0, semitoni: int = 0,
           velocity: int) -> dict[int, list]:
    events = tuple((pos + da, MU.altezza(pitch) + semitoni, length)
                   for pos, pitch, length in score)
    return MU.linea(events, velocity=velocity, stacco=0)


def prima_a() -> dict[int, list]:
    return _linea(LINE_A, velocity=82)


def prima_b() -> dict[int, list]:
    return _linea(LINE_B, velocity=72)


def seconda_a() -> dict[int, list]:
    return _linea(LINE_A, da=PASSAGE_BARS * B, semitoni=-12, velocity=82)


def seconda_b() -> dict[int, list]:
    return _linea(LINE_B, da=PASSAGE_BARS * B, semitoni=12, velocity=72)


def _unisci(*voci: dict[int, list]) -> dict[int, list]:
    result: dict[int, list] = {}
    for voce in voci:
        for pitch, notes in voce.items():
            result.setdefault(pitch, []).extend(notes)
    for notes in result.values():
        notes.sort(key=lambda note: note.pos)
    return result


def costruisci():
    """Costruisce la song; non scrive file e non usa il dispositivo."""
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
        i_a, c_a = C.add_track(
            doc, str(SYNTH), name='LINEA A', folder='SYNTHS',
            length=length, playing=True)
        ST.set_osc(i_a, 1, type='triangle', transpose=0, cents=0)
        ST.set_osc(i_a, 2, type='analogSaw', transpose=0, cents=-5)
        SND.set(c_a, 'oscAVolume', 37)
        SND.set(c_a, 'oscBVolume', 13)
        SND.set(c_a, 'envelope1.attack', 3)
        SND.set(c_a, 'envelope1.sustain', 32)
        SND.set(c_a, 'envelope1.release', 12)
        MU.scrivi(doc, c_a, _unisci(prima_a(), seconda_a()))

        i_b, c_b = C.add_track(
            doc, str(SYNTH), name='LINEA B', folder='SYNTHS',
            length=length, colour_offset='16', playing=True)
        ST.set_osc(i_b, 1, type='square', transpose=0, cents=0)
        ST.set_osc(i_b, 2, type='triangle', transpose=0, cents=4)
        SND.set(c_b, 'oscAVolume', 24)
        SND.set(c_b, 'oscBVolume', 18)
        SND.set(c_b, 'envelope1.attack', 1)
        SND.set(c_b, 'envelope1.sustain', 24)
        SND.set(c_b, 'envelope1.release', 9)
        MU.scrivi(doc, c_b, _unisci(prima_b(), seconda_b()))

        A.place(doc, i_a, c_a, 0, length)
        A.place(doc, i_b, c_b, 0, length)
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
    print('disposizione 1')
    print(MU.racconta_contrappunto(
        prima_a(), prima_b(), nomi=('A sopra', 'B sotto')))
    print('\ndisposizione 2')
    print(MU.racconta_contrappunto(
        seconda_a(), seconda_b(), nomi=('A sotto', 'B sopra')))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('invert', 1))
