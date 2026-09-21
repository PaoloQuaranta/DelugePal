"""Fixture controllata per il sequencer euclideo per noteRow.

Una sola clip kit di sedici sedicesimi contiene tre distribuzioni generate
con la stessa formula del firmware Deluge:

- kick: 5 eventi su 16 passi, nessuna rotazione;
- rim: 4 eventi su 13 passi, rotazione +2 (verso destra);
- hi-hat: 7 eventi su 11 passi, rotazione -1 (verso sinistra).

La prova e' completa solo dopo ascolto, controllo sul display dei tre cicli e
risalvataggio / rilettura della song dal dispositivo.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                         # noqa: E402

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
KIT = RADICE / 'refs' / 'kits' / '808 From Mars.XML'
OUT = RADICE / 'out' / 'EUCLID01.XML'

KICK = 'BD B 808 Decay C 02'
RIM = 'Rim Shot A 808'
HAT = 'CH Combo 808'


def costruisci() -> tuple[object, list[dict[str, object]]]:
    """Costruisce la song e ritorna i rapporti delle tre righe."""
    from delugexml import create as C, parse_file, song as S  # noqa: PLC0415

    doc = parse_file(TEMPL)
    for strumento in list(S.instruments(doc)):
        MU.togli(doc, strumento)
    S.set_bpm(doc.root, 90)
    S.set_swing(doc, 50, figura='1/8')

    _, clip = C.add_track(doc, KIT, name='EUCLID', folder='KITS',
                          length=MU.TICK_PER_BATTUTA, playing=True)
    rapporti = [
        MU.euclideo(doc, clip, KICK, eventi=5, passi=16,
                    rotazione=0, velocity=110),
        MU.euclideo(doc, clip, RIM, eventi=4, passi=13,
                    rotazione=2, velocity=105),
        MU.euclideo(doc, clip, HAT, eventi=7, passi=11,
                    rotazione=-1, velocity=88),
    ]
    return doc, rapporti


def scrivi(path: Path = OUT) -> Path:
    """Valida e scrive la fixture localmente; non effettua il trasferimento."""
    from delugexml import write_file                       # noqa: PLC0415
    from delugexml.writer import FormatTable              # noqa: PLC0415

    doc, _ = costruisci()
    problemi = MU.verifica(doc)
    if problemi:
        raise ValueError(f'fixture euclidea non valida: {problemi}')
    write_file(doc, path, FormatTable.load(RADICE / 'out' / 'format_table.json'))
    return path


if __name__ == '__main__':
    doc, rapporti = costruisci()
    clip = doc.root.find('sessionClips').children[0]
    print('euclideo:', rapporti)
    print(MU.racconta_clip(doc, clip))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('euclid', 1))
