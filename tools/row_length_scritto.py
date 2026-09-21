"""Fixture controllata per la lunghezza indipendente delle noteRow.

Una sola clip kit di sedici sedicesimi contiene tre impulsi, ciascuno su una
riga col proprio ciclo:

- kick: 5/16;
- rim: 7/16;
- hi-hat: 11/16.

Poiche' nessun periodo divide la clip, i tre accenti devono attraversare il
confine della battuta senza riallinearsi ogni sedici passi. La prova e'
completa solo dopo ascolto, controllo delle tre lunghezze sul display e
risalvataggio / rilettura della song.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                         # noqa: E402

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
KIT = RADICE / 'refs' / 'kits' / '808 From Mars.XML'
OUT = RADICE / 'out' / 'ROWLENGTH01.XML'

KICK = 'BD B 808 Decay C 02'
RIM = 'Rim Shot A 808'
HAT = 'CH Combo 808'


def costruisci() -> tuple[object, list[dict[str, object]]]:
    """Costruisce la song e ritorna i tre rapporti di row length."""
    from delugexml import create as C, parse_file, song as S  # noqa: PLC0415

    doc = parse_file(TEMPL)
    for strumento in list(S.instruments(doc)):
        MU.togli(doc, strumento)
    S.set_bpm(doc.root, 90)
    S.set_swing(doc, 50, figura='1/8')

    _, clip = C.add_track(doc, KIT, name='ROW LENGTH', folder='KITS',
                          length=MU.TICK_PER_BATTUTA, playing=True)
    impulso = MU.passi('x...............', velocity=105)
    for drum in (KICK, RIM, HAT):
        MU.scrivi(doc, clip, impulso, dove=drum)

    rapporti = [
        MU.lunghezza_riga(doc, clip, KICK, 5),
        MU.lunghezza_riga(doc, clip, RIM, 7),
        MU.lunghezza_riga(doc, clip, HAT, 11),
    ]
    return doc, rapporti


def scrivi(path: Path = OUT) -> Path:
    """Valida e scrive la fixture localmente; non effettua il trasferimento."""
    from delugexml import write_file                       # noqa: PLC0415
    from delugexml.writer import FormatTable              # noqa: PLC0415

    doc, _ = costruisci()
    problemi = MU.verifica(doc)
    if problemi:
        raise ValueError(f'fixture row length non valida: {problemi}')
    write_file(doc, path, FormatTable.load(RADICE / 'out' / 'format_table.json'))
    return path


if __name__ == '__main__':
    doc, rapporti = costruisci()
    print('row length:', rapporti)
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('rowlength', 1))
