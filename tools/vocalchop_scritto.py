"""VOCAL CHOP -- l'mmyeah affettato in un kit di fette, su un beat house.

Riempie la casella 8 (il vocal chop) di house/trip-hop. Il campione
SAMPLES/RECORD/REC00027.WAV (il «mmyeah» dell'utente, 142725 frame, ~3,24 s) e'
tagliato in 8 fette uguali con kit.affetta -- un kit dove ogni drum e' una <zone>
dello stesso file, REPEAT MODE ONCE (come lo Slicer nativo del Deluge: la ZONA
delimita la fetta, ogni innesco la suona intera). Le fette si innescano a ritmo,
SPEZZETTATE -- buchi, stutter, salti: le fette in fila ricostruirebbero la parola,
il chop sta nel romperla.

Contesto: house four-on-the-floor (808), la casa del vocal chop; basso in levare.

⚠️ Il campione e' gia' sulla SD; niente upload. Lo slicing e' lo stesso meccanismo
che sblocca il break di jungle/DnB.

Metodo: audio -> ascolto pieno dell'utente. Il pattern del chop e' [DEC], da rifinire
all'orecchio. Verdetto: da dare.
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
PRESET_BASSO = RADICE / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = RADICE / 'refs' / 'kits' / '808 From Mars.XML'

# il campione: gia' sulla SD. FRAMES misurato con audio.wav_frames dalla SD.
SAMPLE = 'SAMPLES/RECORD/REC00027.WAV'
FRAMES = 142725
NFETTE = 8

# i drum del kit 808 per il beat
KICK = 'BD A 808 Decay C 04'
CLAP = 'Clap A 808 Tape'
OH = 'OH 808 Decay 05'
CH = 'CH Combo 808'

BPM = 124
SWING = 55
LOOP = ['Am9', 'Dm9']          # vamp minimale, 2 battute (il vocal e' il protagonista)
BATTUTE = 8


def _grave(pc: int, rif: int, lo: int = 26, hi: int = 41) -> int:
    best = None
    for y in range(lo, hi + 1):
        if y % 12 == pc and (best is None or abs(y - rif) < abs(best - rif)):
            best = y
    return best


def batteria() -> dict:
    """Four-on-the-floor house: cassa ogni movimento, clap 2-4, open hat sui levare,
    closed hat sui sedicesimi."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voci = {KICK: [], CLAP: [], OH: [], CH: []}
    for bar in range(BATTUTE):
        da = bar * B
        voci[KICK] += MU.passi('x...x...x...x...', da=da, velocity=112)
        voci[CLAP] += MU.passi('....x.......x...', da=da, velocity=100)
        voci[OH] += MU.passi('..x...x...x...x.', da=da, velocity=80)
        for i in (1, 3, 5, 7, 9, 11, 13, 15):
            voci[CH].append(Note(pos=da + i * P, length=P, velocity=46))
    return voci


def basso() -> dict:
    """House in levare, fuori dalla cassa: fondamentale grave e ottava che rimbalza,
    sul vamp Am | Dm."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voce: dict = {}
    rif = 33
    for bar in range(BATTUTE):
        da = bar * B
        sig = LOOP[bar % len(LOOP)]
        root = _grave(MU.sigla(sig).fondamentale, rif)
        rif = root
        for pos, alt, vel in [(48, root, 100), (144, root + 12, 90),
                              (240, root, 100), (336, root + 12, 90)]:
            voce.setdefault(alt, []).append(Note(pos=da + pos, length=40, velocity=vel))
    return voce


def chop(fette: list[str]) -> dict:
    """Le fette dell'mmyeah SPEZZETTATE: buchi (silenzio), stutter (ripetizioni) e
    salti fra fette non contigue -- NON 1-2-3-... in fila, che ricostruirebbe la
    parola. Con ONCE ogni innesco suona la fetta intera; il chop e' nel ritmo. Un
    motivo di 2 battute ripetuto. [DEC], da rifinire all'orecchio (anche QUALI fette
    stanno bene insieme si decide sentendo)."""
    from delugexml.notes import Note                          # noqa: PLC0415
    # (passo in sedicesimi su 2 battute, fetta 1-based). I passi non elencati sono
    # SILENZIO -> frammenti staccati. Salti e uno stutter, non la parola in fila.
    motivo = [(0, 8), (3, 8), (6, 5), (10, 1), (13, 6),
              (16, 8), (17, 8), (18, 8), (22, 5), (24, 1), (28, 6), (30, 6)]
    voci: dict = {}
    for rep in range(BATTUTE // 2):                # 4 ripetizioni del motivo di 2 battute
        base = rep * 2 * B
        for passo, f in motivo:
            nome = fette[f - 1]
            voci.setdefault(nome, []).append(
                Note(pos=base + passo * P, length=CROMA, velocity=112))
    return voci


def strumento(doc, nome: str):
    """Lo strumento della song che si chiama `nome` (presetName)."""
    from delugexml import song as S                           # noqa: PLC0415
    for inst in S.instruments(doc):
        if inst.get('presetName') == nome or inst.get('name') == nome:
            return inst
    raise ValueError(f'nessuno strumento "{nome}" nella song')


def costruisci() -> tuple[object, dict]:
    """Il pezzo dell'ascolto. Ritorna (doc, {}). Solleva FileNotFoundError se manca
    una fixture."""
    import warnings                                           # noqa: PLC0415
    from delugexml import parse_file, song as S              # noqa: PLC0415
    from delugexml import create as C, arranger as A         # noqa: PLC0415
    from delugexml import kit as K                           # noqa: PLC0415

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(str(TEMPL))
        S.set_bpm(doc.root, BPM)
        S.set_swing(doc, SWING, figura='1/8')
        S.set_scale(doc, 'C', 'maggiore')          # La minore = relativa
        for inst in list(S.instruments(doc)):
            MU.togli(doc, inst)

        lung = BATTUTE * B

        # il kit di fette: l'mmyeah affettato in 8 fette (il vocal chop)
        iChop, cChop = C.add_track(doc, str(KIT), name='CHOP', folder='KITS',
                                   length=lung, colour_offset='48', playing=True)
        fette = K.affetta(doc, iChop, SAMPLE, FRAMES, n=NFETTE)
        for nome, note in chop(fette).items():
            if note:
                MU.scrivi(doc, cChop, note, dove=nome)

        # il beat house (kit 808 a parte)
        iBeat, cBeat = C.add_track(doc, str(KIT), name='BEAT', folder='KITS',
                                   length=lung, colour_offset='32', playing=True)
        for drum, note in batteria().items():
            if note:
                MU.scrivi(doc, cBeat, note, dove=drum)

        # il basso house in levare
        iB, cB = C.add_track(doc, str(PRESET_BASSO), name='BASS', folder='SYNTHS',
                             length=lung, colour_offset='16', playing=True)
        try:
            MU.applica_verbo(doc, iB, 'piu scuro')
        except Exception:                          # noqa: BLE001
            pass
        MU.scrivi(doc, cB, basso())

        A.place(doc, iChop, cChop, 0, lung)
        A.place(doc, iBeat, cBeat, 0, lung)
        A.place(doc, iB, cB, 0, lung)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc, {}


if __name__ == '__main__':
    doc, _ = costruisci()
    from delugexml import arranger as A
    print('fette:', NFETTE, 'campione:', SAMPLE, FRAMES, 'frame')
    print('arco:', A.extent(doc))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
