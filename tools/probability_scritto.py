"""Fixture controllata per verificare la probability indipendente sul Deluge.

Una battuta, due righe sullo stesso synth vuoto:

- DO4: quattro note al 100%, riferimento che suona sempre;
- SOL4: quattro note al 25%, evento probabilistico chiaramente udibile.

La prova e' completa solo dopo avere aperto il file sul dispositivo, letto il
25% sul display, ascoltato piu' giri e risalvato/riscaricato la song.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                         # noqa: E402

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
PRESET = RADICE / 'refs' / 'synths' / 'TEMPL.XML'
OUT = RADICE / 'out' / 'PROBABILITY01.XML'

BASSA = MU.altezza('do4')
ALTA = MU.altezza('sol4')


def costruisci() -> tuple[object, dict[str, int]]:
    """Costruisce la song e ritorna anche il rapporto dell'operazione."""
    from delugexml import create as C, parse_file, song as S  # noqa: PLC0415

    doc = parse_file(TEMPL)
    for strumento in list(S.instruments(doc)):
        MU.togli(doc, strumento)
    S.set_bpm(doc.root, 90)
    # Scelta musicale esplicita: entrambe le altezze (C e G) appartengono a
    # Do maggiore. Non ereditare mai tonica e scala dal template.
    S.set_scale(doc, 'C', 'maggiore')

    _, clip = C.add_track(doc, PRESET, name='PROBABILITY', folder='SYNTHS',
                          length=MU.TICK_PER_BATTUTA, playing=True)
    riferimento = MU.passi('x...x...x...x...', velocity=90)
    casuali = MU.passi('x...x...x...x...', velocity=105)
    rapporto = MU.probabilita(casuali, 25)
    MU.scrivi(doc, clip, riferimento, dove=BASSA)
    MU.scrivi(doc, clip, casuali, dove=ALTA)
    return doc, rapporto


def scrivi(path: Path = OUT) -> Path:
    """Valida e scrive la fixture localmente; non effettua il trasferimento."""
    from delugexml import write_file                       # noqa: PLC0415
    from delugexml.writer import FormatTable              # noqa: PLC0415

    doc, _ = costruisci()
    problemi = MU.verifica(doc)
    if problemi:
        raise ValueError(f'fixture probability non valida: {problemi}')
    write_file(doc, path, FormatTable.load(RADICE / 'out' / 'format_table.json'))
    return path


if __name__ == '__main__':
    doc, rapporto = costruisci()
    print('probability:', rapporto)
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('probability', 1))
