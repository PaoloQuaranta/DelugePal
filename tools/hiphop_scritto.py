"""HIP HOP boom-bap, seguendo docs/istruzioni/batteria-hiphop.md e
basso-hiphop.md.

Il primo genere del perimetro 3 (i contemporanei). La BATTERIA e' [MIS] (Groove
MIDI, etichetta hiphop, 34 esecuzioni beat, 5 batteristi, mediana 91 BPM, BUR
1,03 = DRITTO, pocket stretto), corroborata dai loop boom-bap di (aq) HipHop. Il
BASSO e' [LIB]+[DEC] come ballad/twobeat: nessun corpus in casa (Groove MIDI e'
batteria sola, (aq) HipHop e' drum loop senza basso).

Il boom-bap: cassa pesante sul 1 e sul 3 (il «boom») + sincopi sul levare,
rullante che spacca sul 2 e 4 (v127, il «bap») con ghost molli, hi-hat in CROME
(non sedicesimi: l'hip hop lascia aria). Dritto (swing 50). Basso sub, RADO,
agganciato alla cassa sul 1 e 3, grave. L'armonia e' il loop «polveroso» (Rhodes):
un giro lo-fi di 4 battute in La minore, ripetuto.

Metodo: ritmo, l'ascolto pieno. Verdetto (17 settembre 2026): «ok funziona».
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

B = MU.TICK_PER_BATTUTA      # 384
MOV = MU.TICK_PER_MOVIMENTO  # 96
MIN = 2 * MOV                # 192, una minima
CROMA = MOV // 2             # 48
P = MOV // 4                 # 24, un sedicesimo

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
PRESET_RHODES = RADICE / 'refs' / 'synths' / 'Tal Rhodes.XML'
PRESET_BASSO = RADICE / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = RADICE / 'refs' / 'kits' / 'KIT009.XML'

BPM = 90                                   # la mediana MISURATA del boom-bap
SWING = 50                                 # DRITTO (BUR 1,03): il boom-bap non swinga
LOOP = ['Am9', 'Dm9', 'Fmaj7', 'E7#9']     # il giro lo-fi, 4 battute
SIGLE = LOOP * 2                           # ripetuto: 8 battute
BATTUTE = len(SIGLE)


def _grave(pc: int, rif: int, lo: int = 26, hi: int = 41) -> int:
    """La nota di classe `pc` piu' vicina a `rif`, nel registro grave del sub."""
    best = None
    for y in range(lo, hi + 1):
        if y % 12 == pc and (best is None or abs(y - rif) < abs(best - rif)):
            best = y
    return best


def _roots() -> list[int]:
    rif = 33                                   # La1
    out = []
    for sig in SIGLE:
        r = _grave(MU.sigla(sig).fondamentale, rif)
        out.append(r)
        rif = r
    return out


# la cassa (boom), per battuta: sul 1 e sul 3 + sincopi sul levare. Non uguale
# ogni battuta -- due varianti che si alternano (niente stampo).
KICK_A = 'x.x.....x.......'      # 1, +del1, 3
KICK_B = 'x.......x...x...'      # 1, 3, +del4 (spinge nella battuta dopo)
HATS = 'x.x.x.x.x.x.x.x.'       # crome, molli (NON sedicesimi)


def batteria() -> dict:
    """Boom-bap: cassa 1-3 + sincopi (il boom), rullante backbeat v127 + ghost
    molli (il bap), hi-hat in crome. Dritto."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voci = {'KICK': [], 'SNARE': [], 'HATC': []}
    for bar in range(BATTUTE):
        da = bar * B
        voci['KICK'] += MU.passi(KICK_A if bar % 2 == 0 else KICK_B, da=da, velocity=62)
        # hi-hat in crome, molle, i levare appena su
        for i in range(8):
            pos = da + i * CROMA
            vel = 46 if (pos % MOV) else 38            # il "+" un filo piu' presente
            voci['HATC'].append(Note(pos=pos, length=P, velocity=vel))
        # rullante: backbeat che SPACCA sul 2 e 4 (v127)
        for b in (MOV, 3 * MOV):
            voci['SNARE'].append(Note(pos=da + b, length=P, velocity=127))
        # ghost molli, dove il corpus li mette (a-del-2, e-del-3, a-del-4), variati
        ghost = [7, 9] if bar % 2 == 0 else [9, 15]
        for g in ghost:
            voci['SNARE'].append(Note(pos=da + g * P, length=P, velocity=44))
    return voci


def basso() -> dict:
    """Il sub: RADO e agganciato alla cassa (1 e 3), grave, la fondamentale del
    loop. Nota lunga sul 1 (il sub tenuto), corta ribattuta sul 3; un pickup
    cromatico verso l'accordo dopo su alcune battute."""
    from delugexml.notes import Note                          # noqa: PLC0415
    roots = _roots()
    voce: dict = {}

    def metti(alt, pos, dur, vel):
        voce.setdefault(alt, []).append(Note(pos=pos, length=dur, velocity=vel))

    for bar in range(BATTUTE):
        da = bar * B
        root = roots[bar]
        prossima = roots[(bar + 1) % BATTUTE]
        metti(root, da, 168, 96)                       # il 1: sub tenuto (col boom)
        metti(root, da + MIN, 84, 88)                  # il 3: ribattuto corto (col boom)
        if bar % 2 == 1:                               # pickup, una battuta si' una no
            metti(prossima - 1, da + B - CROMA, CROMA, 76)   # cromatico verso la fond. dopo
    return voce


def comping() -> dict:
    """Il loop «polveroso»: accordi rootless tenuti (il Rhodes lo-fi), uno per
    battuta, morbidi. L'armonia la porta lui, non il basso."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voce: dict = {}
    for bar, sig in enumerate(SIGLE):
        da = bar * B
        for alt in MU.voci(sig, voicing='senza-fondamentale', registro='do4'):
            voce.setdefault(alt, []).append(
                Note(pos=da, length=B - P, velocity=50))       # tenuto quasi tutta la battuta
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
        S.set_swing(doc, SWING, figura='1/8')      # 50 = dritto
        S.set_scale(doc, 'C', 'maggiore')          # La minore = relativa
        for strumento in list(S.instruments(doc)):
            MU.togli(doc, strumento)

        lung = BATTUTE * B

        iR, cR = C.add_track(doc, str(PRESET_RHODES), name='RHODES',
                             folder='SYNTHS', length=lung, playing=True)
        MU.scrivi(doc, cR, comping())

        iB, cB = C.add_track(doc, str(PRESET_BASSO), name='SUB', folder='SYNTHS',
                             length=lung, colour_offset='16', playing=True)
        try:
            MU.applica_verbo(doc, iB, 'piu scuro')      # sub grave e pieno, non brillante
        except Exception:                               # noqa: BLE001
            pass
        MU.scrivi(doc, cB, basso())

        kit, cK = C.add_track(doc, str(KIT), name='KIT009', folder='KITS',
                              length=lung, colour_offset='32', playing=True)
        for drum, note in batteria().items():
            if note:
                MU.scrivi(doc, cK, note, dove=drum)

        A.place(doc, iR, cR, 0, lung)
        A.place(doc, iB, cB, 0, lung)
        A.place(doc, kit, cK, 0, lung)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc, {}


if __name__ == '__main__':
    doc, _ = costruisci()
    b = basso()
    print('basso sub:', sum(len(v) for v in b.values()), 'note /', BATTUTE,
          'battute =', round(sum(len(v) for v in b.values()) / BATTUTE, 2), 'per battuta')
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
