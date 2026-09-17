"""HOUSE con ARRANGIAMENTO (build/drop) + FILTRO + SIDECHAIN.

Chiude le caselle 9 (forma) e 10 (suono) della scheda docs/repertori/house.md.
Estende tools/house_scritto.py -- la four-on-the-floor gia' approvata («funziona»)
-- con l'ESSENZA del genere: l'arco su 32 battute e il suono in movimento.

L'arco, in cinque sezioni (mappa 'intro build drop break drop'):

    intro  8 batt.  solo cassa + closed hat            (anticipazione)
    build  4 batt.  entrano basso e stab, il filtro APRE (rampa del cutoff)
    drop   8 batt.  tutto + il SIDECHAIN pompa          (c'e' la cassa)
    break  4 batt.  via la cassa, stab filtrato + basso (niente pompa: niente cassa)
    drop   8 batt.  rientro pieno                        (torna la pompa)

Il suono in movimento:
- FILTRO: MU.apri_filtro stende una rampa del cutoff sulla clip stab del build;
- SIDECHAIN: MU.sidechain accende il pompaggio INTERNO del Deluge (send pieno sul
  kick 808 + volume-ducking su basso e stab). NON e' il compressore. Si imposta
  una volta: pompa da se' dove batte la cassa (drop si', break no).

⚠️ NIENTE CORPUS (generi programmati): [LIB]+[DEC]. La struttura del sidechain e'
[OSS] (file veri); la MAGNITUDINE del duck (`QUANTO=0xDE000000`) e' stata tarata
all'orecchio.

Metodo: suono+arrangiamento = ascolto pieno dell'utente.
Verdetto (17 settembre 2026): «va bene».
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
SWING = 55                                 # lo shuffle house leggero
LOOP = ['Am9', 'Dm9', 'Fmaj9', 'Em9']      # il giro, 4 battute
BARS = len(LOOP)                           # 4 -- la lunghezza di ogni clip-loop
LUNG = BARS * B                            # una clip dura 4 battute e si ripete

# La profondita' del ducking. Valore osservato in file veri del Deluge (schema
# c1.3.0) e CONFERMATO all'orecchio per questa house (verdetto «va bene», 17 set
# 2026). Per un kit o un pezzo diverso, ri-giudicare suonando.
QUANTO = '0xDE000000'


def _grave(pc: int, rif: int, lo: int = 26, hi: int = 41) -> int:
    best = None
    for y in range(lo, hi + 1):
        if y % 12 == pc and (best is None or abs(y - rif) < abs(best - rif)):
            best = y
    return best


def _batteria(*, clap: bool, open_hat: bool) -> dict:
    """Una batteria four-on-the-floor su BARS battute. `clap`/`open_hat` dicono
    se entrano i due elementi che separano l'intro dal pieno."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voci = {KICK: [], CLAP: [], OH: [], CH: []}
    for bar in range(BARS):
        da = bar * B
        voci[KICK] += MU.passi('x...x...x...x...', da=da, velocity=112)   # il motore
        if clap:
            voci[CLAP] += MU.passi('....x.......x...', da=da, velocity=100)   # 2 e 4
        if open_hat:
            voci[OH] += MU.passi('..x...x...x...x.', da=da, velocity=80)      # i levare
        for i in (1, 3, 5, 7, 9, 11, 13, 15):                            # sedicesimi molli
            voci[CH].append(Note(pos=da + i * P, length=P, velocity=46))
    return {k: v for k, v in voci.items() if v}


def basso() -> dict:
    """In levare, FUORI dalla cassa: fondamentale grave sul levare di 1 e 3,
    ottava sopra sul levare di 2 e 4 -- il rimbalzo house."""
    from delugexml.notes import Note                          # noqa: PLC0415
    rif = 33
    voce: dict = {}
    for bar, sig in enumerate(LOOP):
        da = bar * B
        root = _grave(MU.sigla(sig).fondamentale, rif)
        rif = root
        for pos, alt, vel in [
            (48,  root,      100),   # levare del 1: fondamentale grave
            (144, root + 12,  90),   # levare del 2: ottava (rimbalzo)
            (240, root,      100),   # levare del 3: fondamentale
            (336, root + 12,  90),   # levare del 4: ottava
        ]:
            voce.setdefault(alt, []).append(Note(pos=da + pos, length=40, velocity=vel))
    return voce


def stab() -> dict:
    """Lo stab jazzy: accordo rootless, CORTO, sul levare del 2 e del 4."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voce: dict = {}
    for bar, sig in enumerate(LOOP):
        da = bar * B
        for alt in MU.voci(sig, voicing='senza-fondamentale', registro='do4'):
            for pos in (144, 336):                            # la "&" di 2 e 4
                voce.setdefault(alt, []).append(
                    Note(pos=da + pos, length=60, velocity=72))
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
        S.set_swing(doc, SWING, figura='1/8')      # lo shuffle house
        S.set_scale(doc, 'C', 'maggiore')          # La minore = relativa
        for inst in list(S.instruments(doc)):
            MU.togli(doc, inst)

        # --- strumenti, ognuno con la sua prima clip (vuota), lunga 4 battute ---
        iStab, cStab = C.add_track(doc, str(PRESET_PIANO), name='STAB',
                                   folder='SYNTHS', length=LUNG, playing=True)
        iBass, cBass = C.add_track(doc, str(PRESET_BASSO), name='BASS',
                                   folder='SYNTHS', length=LUNG,
                                   colour_offset='16', playing=True)
        try:
            MU.applica_verbo(doc, iBass, 'piu scuro')          # sub caldo
        except Exception:                                      # noqa: BLE001
            pass
        iKit, cDrumFull = C.add_track(doc, str(KIT), name='K808', folder='KITS',
                                      length=LUNG, colour_offset='32', playing=True)

        # --- le clip di sezione distinte: si duplica la clip (vuota) e vi si
        #     scrivono note diverse. duplicate_clip prende un indice in clips(). ---
        def _dup(clip, *, name, section):
            idx = A.index_of(doc, clip)[0]
            return S.duplicate_clip(doc, idx, name=name, section=str(section))

        cDrumIntro = _dup(cDrumFull, name='K808', section=1)
        cStabBuild = _dup(cStab, name='STAB', section=1)
        cStabFilt = _dup(cStab, name='STAB', section=2)

        # --- le note ---
        for drum, note in _batteria(clap=True, open_hat=True).items():
            MU.scrivi(doc, cDrumFull, note, dove=drum)
        for drum, note in _batteria(clap=False, open_hat=False).items():
            MU.scrivi(doc, cDrumIntro, note, dove=drum)
        MU.scrivi(doc, cBass, basso())
        MU.scrivi(doc, cStab, stab())
        MU.scrivi(doc, cStabBuild, stab())
        MU.scrivi(doc, cStabFilt, stab())

        # --- il suono in movimento ---
        # il filtro APRE sulle 4 battute del build (chiuso -> aperto)
        MU.apri_filtro(doc, cStabBuild, 8, 45, 0, LUNG, passi=9)
        # lo stab del break, filtrato scuro (fisso)
        SND.set(cStabFilt, 'lpfFrequency', 16)
        # il SIDECHAIN interno: send dal kick, ducking su basso e stab. Dopo aver
        # creato tutte le clip, cosi' la propagazione le raggiunge tutte.
        MU.sidechain(doc, iBass, quanto=QUANTO, sync=7, manda_da=(iKit, KICK))
        MU.sidechain(doc, iStab, quanto=QUANTO, sync=7, manda_da=(iKit, KICK))

        # --- l'arco: la mappa delle sezioni nel tempo ---
        sezioni = {
            'intro': [cDrumIntro],
            'build': [cDrumFull, cBass, cStabBuild],
            'drop':  [cDrumFull, cBass, cStab],
            'break': [cBass, cStabFilt],
        }
        MU.forma(doc, 'intro build drop break drop', sezioni,
                 battute_per={'intro': 8, 'build': 4, 'drop': 8, 'break': 4})
        A.open_in_arranger(doc)
    return doc, {}


if __name__ == '__main__':
    doc, _ = costruisci()
    from delugexml import arranger as A
    print('arco:', A.extent(doc), '(atteso (0, %d))' % (32 * B))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
