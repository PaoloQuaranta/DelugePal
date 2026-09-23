"""Fixture controllata per clip di tre e tre movimenti e mezzo.

Due variazioni dello stesso kit sono in sezioni separate: 3/4 parte al
caricamento, 7/8 si lancia dalla sua riga. Gli accenti finali rendono
riconoscibile il punto in cui ciascun ciclo torna all'inizio.

Il trasferimento byte-esatto non basta a chiudere la prova: servono controllo
dei cicli sul Deluge, ascolto e rilettura dopo un salvataggio sul dispositivo.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                         # noqa: E402

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
KIT = RADICE / 'refs' / 'kits' / '808 From Mars.XML'
OUT = RADICE / 'out' / 'METRO01.XML'

KICK = 'BD B 808 Decay C 02'
RIM = 'Rim Shot A 808'


def costruisci():
    """Costruisce due clip con lunghezze derivate dalla griglia della song."""
    from delugexml import create as C, parse_file, song as S  # noqa: PLC0415

    doc = parse_file(TEMPL)
    for strumento in list(S.instruments(doc)):
        MU.togli(doc, strumento)
    S.set_bpm(doc.root, 90)
    S.set_swing(doc, 50, figura='1/8')

    _, tre_quarti = C.add_track(
        doc, KIT, name='METRO TEST', folder='KITS',
        length=S.ticks_per_bar(doc.root), section='0', playing=True)
    tre_quarti.set('clipName', '3/4')
    S.set_clip_length_beats(doc.root, tre_quarti, 3)
    MU.scrivi(doc, tre_quarti, MU.passi('x...x.......', velocity=105),
             dove=KICK)
    MU.scrivi(doc, tre_quarti, MU.passi('........x...', velocity=110),
             dove=RIM)

    sette_ottavi = S.duplicate_clip(
        doc, 0, section='1', name='7/8', colour_offset='24')
    S.set_clip_length_beats(doc.root, sette_ottavi, 3.5)
    MU.scrivi(doc, sette_ottavi, MU.passi('x...x...x.......', velocity=105),
             dove=KICK)
    MU.scrivi(doc, sette_ottavi, MU.passi('............x...', velocity=110),
             dove=RIM)
    return doc


def scrivi(path: Path = OUT) -> Path:
    """Valida e scrive la fixture localmente; non la trasferisce."""
    from delugexml import write_file                       # noqa: PLC0415
    from delugexml.writer import FormatTable              # noqa: PLC0415

    doc = costruisci()
    problemi = MU.verifica(doc)
    if problemi:
        raise ValueError(f'fixture metro non valida: {problemi}')
    write_file(doc, path, FormatTable.load(RADICE / 'out' / 'format_table.json'))
    return path


if __name__ == '__main__':
    doc = costruisci()
    print('movimenti e tick:')
    for movimenti, clip in zip((3, 3.5), doc.root.find('sessionClips').children):
        print(f'  {movimenti}: {clip.get("length")}')
        print(MU.racconta_clip(doc, clip))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('metro', 1))
