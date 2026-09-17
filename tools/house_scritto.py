"""HOUSE (four-on-the-floor), seguendo docs/istruzioni/batteria-house.md e
basso-house.md.

Secondo genere del perimetro 3. ⚠️ NIENTE CORPUS: techno e house sono generi
PROGRAMMATI (il Groove MIDI ha solo `dance` = 7 esecuzioni, 2 batteristi, [OSS]).
Quindi e' [LIB]+[DEC], la convenzione di genere.

Il four-on-the-floor: cassa su OGNI movimento (il motore), clap sul 2 e 4, open
hat sui LEVARE (il «tss», la firma), closed hat sui sedicesimi. Il basso sta
FUORI dalla cassa, sui levare, a ottave che rimbalzano -- l'opposto dell'hip hop.
Stab jazzy (piano) in levare. Swing leggero (55, lo shuffle house). Kit 808 (il
suono E' il genere). Un giro in La minore.

⚠️ Cosa NON c'e', ed e' l'essenza del genere (in «cosa manca» delle istruzioni):
l'ARRANGIAMENTO (build/drop su 32-64 battute) e il FILTRO in movimento (LFO sul
cutoff). Qui c'e' il groove; l'arco e il filtro sono il prossimo passo.

Metodo: ritmo, l'ascolto pieno. Verdetto (17 settembre 2026): «funziona».
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

B = MU.TICK_PER_BATTUTA      # 384
MOV = MU.TICK_PER_MOVIMENTO  # 96
CROMA = MOV // 2             # 48
P = MOV // 4                 # 24

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
PRESET_PIANO = RADICE / 'refs' / 'synths' / 'Pianism I.XML'
PRESET_BASSO = RADICE / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = RADICE / 'refs' / 'kits' / '808 From Mars.XML'

# i drum del kit 808, per nome esatto
KICK = 'BD A 808 Decay C 04'
CLAP = 'Clap A 808 Tape'
OH = 'OH 808 Decay 05'
CH = 'CH Combo 808'

BPM = 124                                  # house classica
SWING = 55                                 # lo shuffle house leggero (techno: 50)
LOOP = ['Am9', 'Dm9', 'Fmaj9', 'Em9']
SIGLE = LOOP * 2                           # 8 battute
BATTUTE = len(SIGLE)


def _grave(pc: int, rif: int, lo: int = 26, hi: int = 41) -> int:
    best = None
    for y in range(lo, hi + 1):
        if y % 12 == pc and (best is None or abs(y - rif) < abs(best - rif)):
            best = y
    return best


def batteria() -> dict:
    """Four-on-the-floor: cassa ogni movimento, clap 2-4, open hat sui levare (la
    firma), closed hat sui sedicesimi molli."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voci = {KICK: [], CLAP: [], OH: [], CH: []}
    for bar in range(BATTUTE):
        da = bar * B
        voci[KICK] += MU.passi('x...x...x...x...', da=da, velocity=112)   # il motore
        voci[CLAP] += MU.passi('....x.......x...', da=da, velocity=100)   # 2 e 4
        voci[OH] += MU.passi('..x...x...x...x.', da=da, velocity=80)      # i levare: LA FIRMA
        for i in (1, 3, 5, 7, 9, 11, 13, 15):                            # sedicesimi molli
            voci[CH].append(Note(pos=da + i * P, length=P, velocity=46))
    return voci


def basso() -> dict:
    """In levare, FUORI dalla cassa: fondamentale grave sul levare di 1 e 3,
    ottava sopra sul levare di 2 e 4 -- il rimbalzo house."""
    from delugexml.notes import Note                          # noqa: PLC0415
    rif = 33
    voce: dict = {}
    for bar, sig in enumerate(SIGLE):
        da = bar * B
        root = _grave(MU.sigla(sig).fondamentale, rif)
        rif = root
        # i quattro levare (la "&" di ogni movimento): 48, 144, 240, 336
        for pos, alt, vel in [
            (48,  root,      100),   # levare del 1: fondamentale grave
            (144, root + 12,  90),   # levare del 2: ottava (rimbalzo)
            (240, root,      100),   # levare del 3: fondamentale
            (336, root + 12,  90),   # levare del 4: ottava
        ]:
            voce.setdefault(alt, []).append(Note(pos=da + pos, length=40, velocity=vel))
    return voce


def comping() -> dict:
    """Lo stab jazzy: accordo rootless, CORTO, sul levare del 2 e del 4 (il push
    house). L'armonia la porta lui."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voce: dict = {}
    for bar, sig in enumerate(SIGLE):
        da = bar * B
        for alt in MU.voci(sig, voicing='senza-fondamentale', registro='do4'):
            for pos in (144, 336):                            # la "&" di 2 e 4
                voce.setdefault(alt, []).append(
                    Note(pos=da + pos, length=60, velocity=72))   # stab corto
    return voce


def costruisci() -> tuple[object, dict]:
    """Il pezzo dell'ascolto. Ritorna (doc, {}). Solleva FileNotFoundError se
    manca una fixture."""
    import warnings                                           # noqa: PLC0415
    from delugexml import parse_file, song as S              # noqa: PLC0415
    from delugexml import create as C, arranger as A         # noqa: PLC0415

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(str(TEMPL))
        S.set_bpm(doc.root, BPM)
        S.set_swing(doc, SWING, figura='1/8')      # lo shuffle house
        S.set_scale(doc, 'C', 'maggiore')          # La minore = relativa
        for strumento in list(S.instruments(doc)):
            MU.togli(doc, strumento)

        lung = BATTUTE * B

        iP, cP = C.add_track(doc, str(PRESET_PIANO), name='STAB',
                             folder='SYNTHS', length=lung, playing=True)
        MU.scrivi(doc, cP, comping())

        iB, cB = C.add_track(doc, str(PRESET_BASSO), name='BASS', folder='SYNTHS',
                             length=lung, colour_offset='16', playing=True)
        try:
            MU.applica_verbo(doc, iB, 'piu scuro')      # sub caldo
        except Exception:                               # noqa: BLE001
            pass
        MU.scrivi(doc, cB, basso())

        kit, cK = C.add_track(doc, str(KIT), name='K808', folder='KITS',
                              length=lung, colour_offset='32', playing=True)
        for drum, note in batteria().items():
            if note:
                MU.scrivi(doc, cK, note, dove=drum)

        A.place(doc, iP, cP, 0, lung)
        A.place(doc, iB, cB, 0, lung)
        A.place(doc, kit, cK, 0, lung)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc, {}


if __name__ == '__main__':
    doc, _ = costruisci()
    b = basso()
    print('basso in levare:', sum(len(v) for v in b.values()), 'note /', BATTUTE, 'battute')
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
