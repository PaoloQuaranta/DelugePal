"""Canone rigoroso a due voci, all'ottava e a distanza di una battuta.

Piston, *Counterpoint* (1970), cap. 11: nel canone la seconda voce imita
continuamente la prima a un intervallo e a una distanza temporale stabiliti.
Qui l'intervallo e' l'ottava superiore e la distanza e' una battuta. Timbro e
forma breve sono scelte elettroniche, non una ricostruzione stilistica.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU  # noqa: E402

B = MU.TICK_PER_BATTUTA
GUIDE_BARS = 8
DELAY = B
TOTAL_BARS = GUIDE_BARS + 1
BPM = 104

TEMPLATE = ROOT / 'refs' / 'songs' / 'TEMPL0.XML'
SYNTH = ROOT / 'refs' / 'synths' / 'TEMPL.XML'
OUT = ROOT / 'out' / 'CANONE01.XML'

# Una sola linea di otto battute. I profili ritmici cambiano da battuta a
# battuta: quando la risposta entra, gli attacchi non si riducono a un delay
# su griglia. L'ultimo Re riempie esattamente la fine dell'ottava battuta.
GUIDE = (
    (0,       're4', 72), (96,       'fa4', 72),
    (192,     'la4', 72), (288,      'do5', 72),
    (B,       're5', 120), (B+144,   'do5', 72),
    (B+240,   'la4', 72), (B+336,    'sib4', 48),
    (2*B,     'sol4', 72), (2*B+96,  'sib4', 120),
    (2*B+240, 'do5', 72), (2*B+336,  'sib4', 48),
    (3*B,     'do5', 72), (3*B+96,   'sib4', 72),
    (3*B+192, 're5', 120), (3*B+336, 'do5', 48),
    (4*B,     'la4', 72), (4*B+96,   'sib4', 72),
    (4*B+192, 'sol4', 72), (4*B+288, 'sib4', 72),
    (5*B,     're5', 120), (5*B+144, 'do5', 72),
    (5*B+240, 'sib4', 72), (5*B+336, 'la4', 48),
    (6*B,     'sol4', 72), (6*B+96,  'sib4', 72),
    (6*B+192, 'la4', 120), (6*B+336, 'sol4', 48),
    (7*B,     'mi4', 72), (7*B+96,   're4', 72),
    (7*B+192, 'do4', 72), (7*B+288,  're4', 96),
)


def guida() -> dict[int, list]:
    """La dux: una linea monofonica completa di otto battute."""
    return MU.linea(GUIDE, velocity=82, stacco=0)


def risposta() -> dict[int, list]:
    """La comes: stessa linea, una battuta dopo e un'ottava sopra."""
    events = tuple((pos + DELAY, MU.altezza(pitch) + 12, length)
                   for pos, pitch, length in GUIDE)
    return MU.linea(events, velocity=72, stacco=0)


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
        i_guide, c_guide = C.add_track(
            doc, str(SYNTH), name='GUIDA', folder='SYNTHS',
            length=length, playing=True)
        ST.set_osc(i_guide, 1, type='triangle', transpose=0, cents=0)
        ST.set_osc(i_guide, 2, type='analogSaw', transpose=0, cents=-5)
        SND.set(c_guide, 'oscAVolume', 38)
        SND.set(c_guide, 'oscBVolume', 13)
        SND.set(c_guide, 'envelope1.attack', 3)
        SND.set(c_guide, 'envelope1.sustain', 32)
        SND.set(c_guide, 'envelope1.release', 12)
        S.set_key_mode(c_guide, False)
        MU.scrivi(doc, c_guide, guida())

        i_answer, c_answer = C.add_track(
            doc, str(SYNTH), name='RISPOSTA', folder='SYNTHS',
            length=length, colour_offset='16', playing=True)
        ST.set_osc(i_answer, 1, type='square', transpose=0, cents=0)
        ST.set_osc(i_answer, 2, type='triangle', transpose=0, cents=4)
        SND.set(c_answer, 'oscAVolume', 24)
        SND.set(c_answer, 'oscBVolume', 19)
        SND.set(c_answer, 'envelope1.attack', 1)
        SND.set(c_answer, 'envelope1.sustain', 24)
        SND.set(c_answer, 'envelope1.release', 9)
        S.set_key_mode(c_answer, False)
        MU.scrivi(doc, c_answer, risposta())

        A.place(doc, i_guide, c_guide, 0, length)
        A.place(doc, i_answer, c_answer, 0, length)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc


def scrivi(path: Path = OUT) -> Path:
    """Scrive una song valida con la tabella di formato locale."""
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
    print(MU.racconta_contrappunto(
        guida(), risposta(), nomi=('guida', 'risposta')))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('canone', 1))
