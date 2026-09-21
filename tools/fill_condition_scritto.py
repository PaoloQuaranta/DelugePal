"""Fixture controllata per verificare FILL e NOT-FILL per nota sul Deluge.

Una clip di una battuta con tre note simultanee su ogni movimento:

- DO4: OFF, riferimento che suona sempre;
- MI4: NOT-FILL, suona soltanto durante la riproduzione normale;
- SOL4: FILL, suona soltanto mentre il comando FILL e' attivo.

Senza FILL si deve sentire Do+Mi; con FILL attivo Do+Sol. La prova e'
completa dopo avere verificato entrambi gli stati sul display, ascoltato la
sostituzione e risalvato/riscaricato la song.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                         # noqa: E402

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
PRESET = RADICE / 'refs' / 'synths' / 'TEMPL.XML'
OUT = RADICE / 'out' / 'FILLCOND01.XML'

SEMPRE = MU.altezza('do4')
FUORI_FILL = MU.altezza('mi4')
SOLO_FILL = MU.altezza('sol4')


def costruisci() -> tuple[object, tuple[dict[str, object], dict[str, object]]]:
    """Costruisce la song e ritorna i rapporti delle due condizioni."""
    from delugexml import create as C, parse_file, song as S  # noqa: PLC0415

    doc = parse_file(TEMPL)
    for strumento in list(S.instruments(doc)):
        MU.togli(doc, strumento)
    S.set_bpm(doc.root, 90)
    S.set_scale(doc, 'C', 'maggiore')

    _, clip = C.add_track(doc, PRESET, name='FILL CONDITION', folder='SYNTHS',
                          length=MU.TICK_PER_BATTUTA, playing=True)
    sempre = MU.passi('x...x...x...x...', velocity=75)
    fuori = MU.passi('x...x...x...x...', velocity=95)
    solo = MU.passi('x...x...x...x...', velocity=110)
    rapporti = (MU.fill(fuori, 'not-fill'), MU.fill(solo, 'fill'))
    MU.scrivi(doc, clip, sempre, dove=SEMPRE)
    MU.scrivi(doc, clip, fuori, dove=FUORI_FILL)
    MU.scrivi(doc, clip, solo, dove=SOLO_FILL)
    return doc, rapporti


def scrivi(path: Path = OUT) -> Path:
    """Valida e scrive la fixture localmente; non effettua il trasferimento."""
    from delugexml import write_file                       # noqa: PLC0415
    from delugexml.writer import FormatTable              # noqa: PLC0415

    doc, _ = costruisci()
    problemi = MU.verifica(doc)
    if problemi:
        raise ValueError(f'fixture condizione fill non valida: {problemi}')
    write_file(doc, path, FormatTable.load(RADICE / 'out' / 'format_table.json'))
    return path


if __name__ == '__main__':
    doc, rapporti = costruisci()
    print('fill:', rapporti)
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('fillcond', 1))
