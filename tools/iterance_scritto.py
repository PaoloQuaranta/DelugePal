"""Fixture controllata per verificare iterance classica e CUSTOM sul Deluge.

Una clip di una battuta, due righe sullo stesso synth vuoto:

- DO4: una nota con iterance 1of4;
- SOL4: una nota con iterance CUSTOM 1+3of4.

Su quattro ripetizioni il Do deve suonare solo al primo giro, il Sol al primo
e al terzo. La prova e' completa solo dopo avere letto entrambe le condizioni
sul display, ascoltato almeno quattro giri e risalvato/riscaricato la song.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                         # noqa: E402

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
PRESET = RADICE / 'refs' / 'synths' / 'TEMPL.XML'
OUT = RADICE / 'out' / 'ITERANCE01.XML'

BASSA = MU.altezza('do4')
ALTA = MU.altezza('sol4')


def costruisci() -> tuple[object, tuple[dict[str, object], dict[str, object]]]:
    """Costruisce la song e ritorna i rapporti delle due operazioni."""
    from delugexml import create as C, parse_file, song as S  # noqa: PLC0415

    doc = parse_file(TEMPL)
    for strumento in list(S.instruments(doc)):
        MU.togli(doc, strumento)
    S.set_bpm(doc.root, 90)
    S.set_scale(doc, 'C', 'maggiore')

    _, clip = C.add_track(doc, PRESET, name='ITERANCE', folder='SYNTHS',
                          length=MU.TICK_PER_BATTUTA, playing=True)
    classica = MU.passi('x...', velocity=90)
    custom = MU.passi('x...', velocity=105)
    rapporti = (MU.iterance(classica, 1, ogni=4),
                MU.iterance(custom, [1, 3], ogni=4))
    MU.scrivi(doc, clip, classica, dove=BASSA)
    MU.scrivi(doc, clip, custom, dove=ALTA)
    return doc, rapporti


def scrivi(path: Path = OUT) -> Path:
    """Valida e scrive la fixture localmente; non effettua il trasferimento."""
    from delugexml import write_file                       # noqa: PLC0415
    from delugexml.writer import FormatTable              # noqa: PLC0415

    doc, _ = costruisci()
    problemi = MU.verifica(doc)
    if problemi:
        raise ValueError(f'fixture iterance non valida: {problemi}')
    write_file(doc, path, FormatTable.load(RADICE / 'out' / 'format_table.json'))
    return path


if __name__ == '__main__':
    doc, rapporti = costruisci()
    print('iterance:', rapporti)
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('iterance', 1))
