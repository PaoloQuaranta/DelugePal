"""Contrappunto libero a tre parti, senza accompagnamento.

Piston, *Counterpoint* (1970), capp. 7-8: in tre parti ogni linea deve
conservare ritmo e curva propri, ma la consonanza si valuta anche rispetto al
basso che sostiene l'intera sonorita'. Qui le tre voci entrano una per battuta,
si intrecciano per sei battute e convergono su Re minore.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU  # noqa: E402

B = MU.TICK_PER_BATTUTA
TOTAL_BARS = 8
BPM = 102

TEMPLATE = ROOT / 'refs' / 'songs' / 'TEMPL0.XML'
SYNTH = ROOT / 'refs' / 'synths' / 'TEMPL.XML'
OUT = ROOT / 'out' / 'TREPARTI01.XML'

# Ogni coppia ha meno del 75% di attacchi comuni. I punti fra i movimenti
# forti sono note di passaggio o vicine; sui movimenti forti, dalla terza
# battuta, le tre classi formano una sonorita' consonante completa. Le ultime
# tre note sono Fa5, La4 e Re3.
ALTA = (
    (0, 62), (96, 65), (240, 69), (288, 72),
    (384, 70), (480, 69), (624, 67), (720, 65),
    (768, 67), (816, 62), (864, 65), (960, 65),
    (1008, 67), (1056, 64), (1152, 65), (1200, 67),
    (1248, 65), (1344, 67), (1392, 70), (1440, 69),
    (1536, 69), (1584, 74), (1632, 69), (1728, 67),
    (1776, 64), (1824, 69), (1920, 69), (1968, 74),
    (2016, 70), (2112, 70), (2160, 72), (2208, 69),
    (2304, 67), (2352, 65), (2400, 69), (2496, 70),
    (2544, 65), (2592, 69), (2688, 74), (2736, 70),
    (2784, 74), (2880, 76), (2928, 72), (2976, 77),
)

MEDIA = (
    (384, 62), (528, 65), (624, 64), (720, 62),
    (768, 62), (840, 57), (864, 58), (960, 57),
    (1032, 61), (1056, 57), (1152, 57), (1224, 55),
    (1248, 58), (1344, 62), (1416, 61), (1440, 64),
    (1536, 62), (1608, 58), (1632, 60), (1728, 60),
    (1800, 62), (1824, 64), (1920, 62), (1992, 58),
    (2016, 62), (2112, 65), (2184, 60), (2208, 64),
    (2304, 62), (2376, 67), (2400, 65), (2496, 65),
    (2568, 61), (2592, 64), (2688, 69), (2760, 65),
    (2784, 70), (2880, 69), (2952, 64), (2976, 69),
)

BASSA = (
    (768, 46), (792, 45), (864, 50), (960, 50),
    (984, 52), (1056, 49), (1152, 50), (1176, 52),
    (1248, 50), (1344, 46), (1368, 48), (1440, 49),
    (1536, 53), (1560, 50), (1632, 53), (1728, 52),
    (1752, 48), (1824, 49), (1920, 53), (1944, 50),
    (2016, 55), (2112, 50), (2136, 52), (2208, 49),
    (2304, 46), (2328, 48), (2400, 50), (2496, 50),
    (2520, 52), (2592, 49), (2688, 53), (2712, 52),
    (2784, 55), (2880, 49), (2904, 48), (2976, 50),
)


def _linea(punti, *, velocity: int) -> dict[int, list]:
    """Trasforma una curva di attacchi in una linea legata fino a battuta 8."""
    events = []
    for index, (pos, pitch) in enumerate(punti):
        end = punti[index + 1][0] if index + 1 < len(punti) else TOTAL_BARS * B
        events.append((pos, pitch, end - pos))
    return MU.linea(events, velocity=velocity, stacco=0)


def voce_alta() -> dict[int, list]:
    return _linea(ALTA, velocity=80)


def voce_media() -> dict[int, list]:
    return _linea(MEDIA, velocity=72)


def voce_bassa() -> dict[int, list]:
    return _linea(BASSA, velocity=76)


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
        specs = (
            ('VOCE ALTA', voce_alta(), '0', 'triangle', 'analogSaw',
             35, 11, 3, 31, 12),
            ('VOCE MEDIA', voce_media(), '16', 'square', 'triangle',
             20, 23, 2, 27, 10),
            ('VOCE BASSA', voce_bassa(), '24', 'analogSaw', 'triangle',
             17, 25, 1, 30, 8),
        )
        for (name, notes, colour, osc_a, osc_b, vol_a, vol_b,
             attack, sustain, release) in specs:
            instrument, clip = C.add_track(
                doc, str(SYNTH), name=name, folder='SYNTHS', length=length,
                colour_offset=colour, playing=True)
            ST.set_osc(instrument, 1, type=osc_a, transpose=0, cents=0)
            ST.set_osc(instrument, 2, type=osc_b, transpose=0,
                       cents=-4 if name == 'VOCE ALTA' else 4)
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
    if errors:
        raise ValueError(f'song non valida: {errors}')
    write_file(doc, path, FormatTable.load(ROOT / 'out' / 'format_table.json'))
    return path


if __name__ == '__main__':
    doc = costruisci()
    voci = (voce_alta(), voce_media(), voce_bassa())
    nomi = ('alta', 'media', 'bassa')
    for i, j in ((0, 1), (0, 2), (1, 2)):
        print(MU.racconta_contrappunto(
            voci[i], voci[j], nomi=(nomi[i], nomi[j])))
        print()
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('treparti', 1))
