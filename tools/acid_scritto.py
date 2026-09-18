"""TECHNO ACID -- il TB-303, la linea che rotola, il filtro che evolve.

Chiude la casella 8 (lead) e approfondisce la 10 della scheda house/techno. Il
carattere dell'acid e' il FILTRO risonante, non le note: una linea quasi ferma
(La, coi suoi salti d'ottava/b7/quinta) resa viva dallo squelch del 303 per nota
e dal filtro che apre lungo l'arco.

Il suono: MU.acid trasforma `Square Saw Bass` in un 303 -- mono + saw + risonanza
alta + env2->cutoff (squelch) + velocity->cutoff (accento) + portamento (slide).
Il movimento: MU.automatizza rampa cutoff E risonanza nel build.

L'arco (32 battute, con MU.forma):
    intro  8  batteria minimale + acid col cutoff basso (muffled)
    build  8  entra la batteria piena; il filtro APRE (cutoff+risonanza salgono)
    drop  16  tutto, filtro aperto -- l'acid strilla

⚠️ NIENTE CORPUS (generi programmati): [LIB]+[DEC]. I patch cable del 303 sono
[OSS] (corpus). I valori del suono sono [DEC]+[da verificare] all'orecchio.

Metodo: suono = ascolto pieno dell'utente.
Verdetto (18 settembre 2026): «l'idea generale c'e'». La risonanza (40) regge --
semmai da abbassare un pelo, ritocco rimandato per scelta dell'utente.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

B = MU.TICK_PER_BATTUTA      # 384
MOV = MU.TICK_PER_MOVIMENTO  # 96
P = MOV // 4                 # 24, un sedicesimo

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
PRESET_ACID = RADICE / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = RADICE / 'refs' / 'kits' / '808 From Mars.XML'

KICK = 'BD A 808 Decay C 04'
CLAP = 'Clap A 808 Tape'
OH = 'OH 808 Decay 05'
CH = 'CH Combo 808'

BPM = 132                                  # techno
SWING = 50                                 # dritto
ROOT = 33                                  # La1, il sub dell'acid
BARS = 4                                   # ogni clip dura 4 battute e si ripete
LUNG = BARS * B


def _batteria(*, clap: bool, open_hat: bool) -> dict:
    """Four-on-the-floor techno su BARS battute. `clap`/`open_hat` dicono se
    entrano i due elementi che separano l'intro dal pieno."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voci = {KICK: [], CLAP: [], OH: [], CH: []}
    for bar in range(BARS):
        da = bar * B
        voci[KICK] += MU.passi('x...x...x...x...', da=da, velocity=115)   # il motore
        if clap:
            voci[CLAP] += MU.passi('....x.......x...', da=da, velocity=98)    # 2 e 4
        if open_hat:
            voci[OH] += MU.passi('..x...x...x...x.', da=da, velocity=78)      # i levare
        for i in (1, 3, 5, 7, 9, 11, 13, 15):                            # sedicesimi molli
            voci[CH].append(Note(pos=da + i * P, length=P, velocity=44))
    return {k: v for k, v in voci.items() if v}


def linea() -> dict:
    """Il riff 303: sedicesimi che rotolano su La, accenti e slide. Il movimento
    vero e' il filtro (MU.acid + MU.automatizza), non le altezze."""
    from delugexml.notes import Note                          # noqa: PLC0415
    #        passo:  0  1   2  3  4   5  6  7  8   9 10 11  12 13 14  15
    OFF = [0, 0, 12, 0, 0, 10, 0, 0, 0, 12, 0, 0, 7, 0, 0, 10]
    ACC = [1, 0,  0, 1, 0,  0, 0, 1, 0,  0, 0, 0, 1, 0, 0,  0]
    SLIDE = [0, 1, 0, 0, 0,  1, 0, 0, 0,  1, 0, 0, 0, 0, 1,  0]
    voce: dict = {}
    for bar in range(BARS):
        for i in range(16):
            alt = ROOT + OFF[i]
            vel = 120 if ACC[i] else 70                       # l'accento e' la velocity
            dur = P + 8 if SLIDE[i] else P - 4                # slide = sfora sul passo dopo (legato -> glide)
            voce.setdefault(alt, []).append(
                Note(pos=bar * B + i * P, length=dur, velocity=vel))
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
        S.set_swing(doc, SWING, figura='1/8')      # dritto
        S.set_scale(doc, 'C', 'maggiore')          # La minore = relativa
        for inst in list(S.instruments(doc)):
            MU.togli(doc, inst)

        # --- strumenti, ognuno con la prima clip (vuota), lunga 4 battute ---
        iAcid, cAcidDrop = C.add_track(doc, str(PRESET_ACID), name='ACID',
                                       folder='SYNTHS', length=LUNG, playing=True)
        iKit, cDrumFull = C.add_track(doc, str(KIT), name='K808', folder='KITS',
                                      length=LUNG, colour_offset='32', playing=True)

        # --- clip di sezione distinte (duplicate vuote, poi si scrivono le note) ---
        def _dup(clip, *, name, section):
            idx = A.index_of(doc, clip)[0]
            return S.duplicate_clip(doc, idx, name=name, section=str(section))

        cAcidBuild = _dup(cAcidDrop, name='ACID', section=1)
        cAcidIntro = _dup(cAcidDrop, name='ACID', section=2)
        cDrumIntro = _dup(cDrumFull, name='K808', section=1)

        # --- le note (la stessa linea in tutte le clip acid: muove il filtro) ---
        for clip in (cAcidDrop, cAcidBuild, cAcidIntro):
            MU.scrivi(doc, clip, linea())
        for drum, note in _batteria(clap=True, open_hat=True).items():
            MU.scrivi(doc, cDrumFull, note, dove=drum)
        for drum, note in _batteria(clap=False, open_hat=False).items():
            MU.scrivi(doc, cDrumIntro, note, dove=drum)

        # --- il suono acid, su tutte le clip di ACID (dopo averle create) ---
        MU.acid(doc, iAcid, onda='saw')

        # --- il filtro per sezione ---
        # intro: resta col cutoff base (muffled) -- non tocco cAcidIntro
        # build: il filtro APRE -- cutoff e risonanza salgono
        MU.automatizza(doc, cAcidBuild, 'lpfFrequency', 8, 42, 0, LUNG, passi=9)
        MU.automatizza(doc, cAcidBuild, 'lpfResonance', 30, 46, 0, LUNG, passi=9)
        # drop: filtro aperto, fisso
        SND.set(cAcidDrop, 'lpfFrequency', 42)

        # --- l'arco ---
        sezioni = {
            'intro': [cDrumIntro, cAcidIntro],
            'build': [cDrumFull, cAcidBuild],
            'drop':  [cDrumFull, cAcidDrop],
        }
        MU.forma(doc, 'intro build drop', sezioni,
                 battute_per={'intro': 8, 'build': 8, 'drop': 16})
        A.open_in_arranger(doc)
    return doc, {}


if __name__ == '__main__':
    doc, _ = costruisci()
    from delugexml import arranger as A
    print('arco:', A.extent(doc), '(atteso (0, %d))' % (32 * B))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
