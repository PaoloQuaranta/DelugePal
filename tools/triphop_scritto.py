"""TRIP-HOP -- la fusione: batteria hip-hop rallentata, basso dub, armonia minore
jazzy, e lo spazio del dub (l'eco).

Terzo genere del perimetro 3. Non e' una capacita' nuova ma una RICOMBINAZIONE col
carattere Portishead: downtempo (~84), scuro, laid-back, cinematico. L'unico suono
nuovo e' l'ECO DUB (MU.eco_dub).

- ARMONIA (il centro, priorita' 1): il vamp minore Cm9 | Cm9 | Abmaj7 | G7b9 --
  i-i-bVI-V7b9 (il bVI caldo, la dominante alterata scura). Chiuso col [CALC]
  (racconta_armonia): Cm9 rootless Eb G Bb D, Abmaj7 C Eb G Bb, G7b9 Ab B D F.
  Rhodes rootless, tenuto, con l'eco dub e un velo di riverbero.
- BATTERIA: boom-bap RALLENTATO e morbido -- cassa 1-3 + sincope, backbeat 2-4 piu'
  morbido (non 127), ghost molli, hi-hat in crome con aria. Swing 56 (laid-back).
  Riusa gli idiomi di batteria-hiphop.md (variante lo-fi).
- BASSO: dub -- sub profondo, rado, tenuto, segue le fondamentali del vamp.

⚠️ NIENTE CORPUS trip-hop (il Groove MIDI non ha l'etichetta): [LIB]+[DEC], la
batteria appoggiata al [MIS] boom-bap dell'hip hop. L'eco e' [OSS]+[da verificare].

Metodo misto: armonia [CALC]; batteria/basso/eco = ascolto pieno. Verdetto: da dare.
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

BPM = 84                                   # downtempo
SWING = 56                                 # laid-back (il lilt lo-fi), NON dritto
VAMP = ['Cm9', 'Cm9', 'Abmaj7', 'G7b9']    # il giro minore, 4 battute
BARS = len(VAMP)
LUNG = BARS * B


def _grave(pc: int, rif: int, lo: int = 24, hi: int = 39) -> int:
    """La nota di classe `pc` piu' vicina a `rif`, nel registro grave del sub."""
    best = None
    for y in range(lo, hi + 1):
        if y % 12 == pc and (best is None or abs(y - rif) < abs(best - rif)):
            best = y
    return best


def comping() -> dict:
    """Il vamp minore jazzy, tenuto e molle sul Rhodes -- condotto (voice-leading).
    L'armonia e' chiusa col [CALC]; qui la si posa."""
    return MU.armonia(' | '.join(VAMP), voicing='senza-fondamentale',
                      registro='do3', durata='1/1', velocity=55,
                      articolazione='legato')


def triphop_batteria() -> dict:
    """Boom-bap RALLENTATO e morbido: cassa 1-3 + sincope, backbeat 2-4 morbido
    (non 127), ghost molli, hi-hat in crome con aria. Laid-back (swing 56)."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voci = {'KICK': [], 'SNARE': [], 'HATC': []}
    for bar in range(BARS):
        da = bar * B
        voci['KICK'] += MU.passi('x.x.....x.......' if bar % 2 == 0
                                 else 'x.......x...x...', da=da, velocity=64)
        for i in range(8):                                   # hi-hat crome, molli, con aria
            pos = da + i * CROMA
            voci['HATC'].append(Note(pos=pos, length=P, velocity=44 if (pos % MOV) else 36))
        for b in (MOV, 3 * MOV):                             # backbeat 2 e 4, MORBIDO
            voci['SNARE'].append(Note(pos=da + b, length=P, velocity=106))
        for g in ([7, 9] if bar % 2 == 0 else [9, 15]):     # ghost molli
            voci['SNARE'].append(Note(pos=da + g * P, length=P, velocity=40))
    return voci


def triphop_basso() -> dict:
    """Il sub dub: RADO e tenuto, grave, segue le fondamentali del vamp, dietro
    il beat. Nota lunga sul 1, una ribattuta corta sul 3."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voce: dict = {}
    rif = 33
    for bar, sig in enumerate(VAMP):
        da = bar * B
        root = _grave(MU.sigla(sig).fondamentale, rif)
        rif = root
        voce.setdefault(root, []).append(Note(pos=da, length=MIN + 96, velocity=92))
        voce.setdefault(root, []).append(Note(pos=da + 2 * MOV, length=MOV, velocity=78))
    return voce


def strumento(doc, nome: str):
    """Lo strumento della song che si chiama `nome` (presetName)."""
    from delugexml import song as S                           # noqa: PLC0415
    for inst in S.instruments(doc):
        if inst.get('presetName') == nome or inst.get('name') == nome:
            return inst
    raise ValueError(f'nessuno strumento "{nome}" nella song')


def costruisci() -> tuple[object, dict]:
    """Il pezzo dell'ascolto. Ritorna (doc, {}). Solleva FileNotFoundError se
    manca una fixture."""
    import warnings                                           # noqa: PLC0415
    from delugexml import parse_file, song as S              # noqa: PLC0415
    from delugexml import create as C, arranger as A         # noqa: PLC0415
    from delugexml import sound as SND                       # noqa: PLC0415

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(str(TEMPL))
        S.set_bpm(doc.root, BPM)
        S.set_swing(doc, SWING, figura='1/8')      # laid-back
        S.set_scale(doc, 'C', 'minore')            # Do minore
        for inst in list(S.instruments(doc)):
            MU.togli(doc, inst)

        iR, cR = C.add_track(doc, str(PRESET_RHODES), name='RHODES',
                             folder='SYNTHS', length=LUNG, playing=True)
        MU.scrivi(doc, cR, comping())

        iB, cB = C.add_track(doc, str(PRESET_BASSO), name='SUB', folder='SYNTHS',
                             length=LUNG, colour_offset='16', playing=True)
        try:
            MU.applica_verbo(doc, iB, 'piu scuro')      # sub grave e pieno
        except Exception:                               # noqa: BLE001
            pass
        MU.scrivi(doc, cB, triphop_basso())

        kit, cK = C.add_track(doc, str(KIT), name='KIT009', folder='KITS',
                              length=LUNG, colour_offset='32', playing=True)
        for drum, note in triphop_batteria().items():
            if note:
                MU.scrivi(doc, cK, note, dove=drum)

        # lo spazio: l'eco dub sul Rhodes + un velo di riverbero
        MU.eco_dub(doc, iR, feedback=36, sync=7, analog=True, pingpong=True)
        try:
            SND.set(cR, 'reverbAmount', 22)
        except Exception:                               # noqa: BLE001
            pass

        # la forma: intro (solo Rhodes + eco) -> full (tutti)
        sezioni = {'intro': [cR], 'full': [cR, cK, cB]}
        MU.forma(doc, 'intro full', sezioni, battute_per={'intro': 4, 'full': 8})
        A.open_in_arranger(doc)
    return doc, {}


if __name__ == '__main__':
    doc, _ = costruisci()
    from delugexml import arranger as A
    print(MU.racconta_armonia(' | '.join(VAMP), voicing='senza-fondamentale',
                              registro='do3'))
    print('arco:', A.extent(doc))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
