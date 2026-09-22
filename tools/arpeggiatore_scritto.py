"""Fixture controllata per l'arpeggiatore community del Deluge.

Tre clip dello stesso synth, in sezioni diverse e quindi mutuamente
esclusive, tengono per una battuta lo stesso accordo di Do minore settima:

- ARP UP: riferimento semplice, due ottave, nessun rhythm/randomizer;
- ARP RHYTHM: preset BOTH, pattern ``0-0`` e repeat 2;
- ARP RANDOM: WALK3 + ottave random, ratchet e spread bloccati.

Sul dispositivo si lanciano una alla volta. La prova e' completa dopo avere
letto i valori sul display, ascoltato alcuni giri di ciascuna e
risalvato/riscaricato la song.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                         # noqa: E402

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
PRESET = RADICE / 'refs' / 'synths' / 'TEMPL.XML'
OUT = RADICE / 'out' / 'ARP01.XML'


def costruisci() -> tuple[object, tuple[dict[str, object], ...]]:
    """Costruisce la song e ritorna i rapporti riletti dalle tre clip."""
    from delugexml import create as C, parse_file, song as S  # noqa: PLC0415

    doc = parse_file(TEMPL)
    for strumento in list(S.instruments(doc)):
        MU.togli(doc, strumento)
    S.set_bpm(doc.root, 96)
    S.set_scale(doc, 'C', 'minore')

    _, up = C.add_track(
        doc, PRESET, name='ARP TEST', folder='SYNTHS',
        length=MU.TICK_PER_BATTUTA, section='0', playing=True)
    up.set('clipName', 'ARP UP')
    accordo = MU.accordi(
        'do4 mib4 sol4 sib4', durata='1/1', velocity=100,
        articolazione='legato')
    MU.scrivi(doc, up, accordo)
    rapporto_up = MU.arpeggiatore(
        up, preset='up', ottave=2, ripetizioni=1, ritmo=0,
        ratchet=0, probabilita_ratchet=0, probabilita_nota=50,
        spread_velocity=0, spread_gate=0, spread_ottava=0,
        blocca_random=True)

    rhythm = S.duplicate_clip(
        doc, 0, section='1', name='ARP RHYTHM', colour_offset='24')
    rapporto_rhythm = MU.arpeggiatore(
        rhythm, preset='both', ottave=3, ripetizioni=2, ritmo='0-0',
        ratchet=0, probabilita_ratchet=0, probabilita_nota=50,
        spread_velocity=0, spread_gate=0, spread_ottava=0,
        blocca_random=True)

    casuale = S.duplicate_clip(
        doc, 0, section='2', name='ARP RANDOM', colour_offset='48')
    rapporto_casuale = MU.arpeggiatore(
        casuale, modo_note='walk3', modo_ottave='random', ottave=3,
        ripetizioni=1, ritmo='00-0-', ratchet=35,
        probabilita_ratchet=35, probabilita_nota=50,
        probabilita_basso=10, probabilita_scambio=10,
        probabilita_glide=8, probabilita_reverse=10,
        probabilita_accordo=8, spread_velocity=15, spread_gate=10,
        spread_ottava=12, blocca_random=True)

    return doc, (rapporto_up, rapporto_rhythm, rapporto_casuale)


def scrivi(path: Path = OUT) -> Path:
    """Valida e scrive la fixture localmente; non la trasferisce."""
    from delugexml import write_file                       # noqa: PLC0415
    from delugexml.writer import FormatTable              # noqa: PLC0415

    doc, _ = costruisci()
    problemi = MU.verifica(doc)
    if problemi:
        raise ValueError(f'fixture arpeggiatore non valida: {problemi}')
    write_file(doc, path, FormatTable.load(RADICE / 'out' / 'format_table.json'))
    return path


if __name__ == '__main__':
    doc, rapporti = costruisci()
    print('arpeggiatori:')
    for rapporto in rapporti:
        print(' ', rapporto)
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('arp', 1))
