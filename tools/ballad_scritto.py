"""BALLAD jazz, seguendo docs/istruzioni/basso-ballad.md e batteria-ballad.md.

Il secondo feel diverso dallo swing (16 settembre 2026). ⚠️ Al contrario di funk
e swing, la sezione ritmica della ballad NON ha corpus: il Groove MIDI non ha un
feel «ballad», il Jazz Trio Database parte da 102 BPM (niente ballad), la Weimar
da' il solista, non basso e batteria. Quindi qui e' [LIB]+[DEC], non [MIS].

La ballad e' fatta di ARMONIA, spazio e tempo lento. Percio' la demo e' una
sezione ritmica intera -- comping (Rhodes), basso in 2, batteria soft -- su un
giro ricco di 8 battute in Fa. Il feel:

  comping    accordi tenuti, rootless (3-5-7-9), morbidi -- l'armonia porta il pezzo
  basso      2-feel: fondamentale sul 1, quinta sul 3 (minime), legato e scuro
  batteria   spazzole (ripiego: kit acustico pianissimo) -- pedale 2 e 4, cassa
             feathered sul 1, un ride soft col lilt di terzina (set_swing 66)

⚠️ IL RUBATO non c'e': la sezione ritmica sta in tempo lento e STABILE, il rubato
vero e' del solista (che il Deluge non suona qui). E le SPAZZOLE vere sono un
campione che manca: qui e' un kit soft. Sono le due cose in «Cosa manca» delle
istruzioni. Metodo: ritmo, l'ascolto pieno.
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

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
PRESET_RHODES = RADICE / 'refs' / 'synths' / 'Tal Rhodes.XML'
PRESET_BASSO = RADICE / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = RADICE / 'refs' / 'kits' / 'KIT009.XML'

BPM = 60
SWING = 66                                 # la terzina: il lilt della ballad
PROG = 'Fmaj7 | Dm7 | Gm7 | C7 | Am7 | D7 | Gm7 | C7'
SIGLE = [s.strip() for s in PROG.split('|')]
BATTUTE = len(SIGLE)


def _vicino(pc: int, rif: int, lo: int = 28, hi: int = 48) -> int:
    """La nota di classe `pc` piu' vicina a `rif`, dentro mi1-do3."""
    best = None
    for y in range(lo, hi + 1):
        if y % 12 == pc and (best is None or abs(y - rif) < abs(best - rif)):
            best = y
    return best


def basso_due() -> dict:
    """Il 2-feel: fondamentale sul 1, quinta sul 3, minime. All'ultima battuta
    (turnaround) un po' di momentum -- minima + due semiminime verso il Fa."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voce: dict = {}
    rif = 33
    for bar, sig in enumerate(SIGLE):
        s = MU.sigla(sig)
        root = _vicino(s.fondamentale, rif)
        quinta = _vicino((s.fondamentale + s.gradi.get(5, 7)) % 12, root)
        pos = bar * B
        if bar == BATTUTE - 1:
            # turnaround: C (minima) -> D -> E, semiminime verso il Fa del giro
            voce.setdefault(root, []).append(Note(pos=pos, length=MIN, velocity=68))
            voce.setdefault(_vicino(2, root), []).append(
                Note(pos=pos + MIN, length=MOV, velocity=62))          # re
            voce.setdefault(_vicino(4, root), []).append(
                Note(pos=pos + MIN + MOV, length=MOV, velocity=62))    # mi -> Fa
        else:
            voce.setdefault(root, []).append(Note(pos=pos, length=MIN, velocity=68))
            voce.setdefault(quinta, []).append(
                Note(pos=pos + MIN, length=MIN, velocity=64))
        rif = quinta
    return voce


# batteria soft, per battuta. Nessun groove template: non c'e' corpus ballad.
# ⚠️ NIENTE spang-a-lang: a tempo di ballad il ride col bastone non c'e' ([LIB]).
# Il tempo lo tiene lo STROFINIO sul rullante, non il ride (batteria-ballad.md).
KICK = 'x...............'      # feathered sul 1
HATC = '....x.......x...'      # charleston morbido su 2 e 4 (la destra)
SWEEP = 'x.x.x.x.x.x.x.x.'     # lo strofinio: crome soft, swing 66 -> lilt; il MOTORE


def batteria() -> dict:
    """La texture di spazzole: lo strofinio (rullante soft sulle crome) e' il
    motore; charleston su 2 e 4; cassa feathered sul 1; un tocco di piatto solo a
    inizio frase, per colore -- non a tenere il tempo."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voci = {'KICK': [], 'HATC': [], 'SNARE': [], 'RIDE': []}
    for bar in range(BATTUTE):
        da = bar * B
        voci['KICK'] += MU.passi(KICK, da=da, velocity=32)
        voci['HATC'] += MU.passi(HATC, da=da, velocity=42)
        voci['SNARE'] += MU.passi(SWEEP, da=da, velocity=28)     # il mormorio
        if bar in (0, 4):                                        # inizio delle frasi
            voci['RIDE'].append(Note(pos=da, length=MOV, velocity=34))
    return voci


def comping() -> dict:
    """Accordi tenuti, rootless (3-5-7-9), morbidi: l'armonia della ballad."""
    return MU.armonia(PROG, voicing='senza-fondamentale', registro='do4',
                      durata='1/1', velocity=54, articolazione='legato')


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
        S.set_swing(doc, SWING, figura='1/8')      # la terzina sulle crome
        S.set_scale(doc, 'F', 'maggiore')
        for strumento in list(S.instruments(doc)):
            MU.togli(doc, strumento)

        lung = BATTUTE * B

        iR, cR = C.add_track(doc, str(PRESET_RHODES), name='RHODES',
                             folder='SYNTHS', length=lung, playing=True)
        MU.scrivi(doc, cR, comping())

        iB, cB = C.add_track(doc, str(PRESET_BASSO), name='BASSO', folder='SYNTHS',
                             length=lung, colour_offset='16', playing=True)
        try:
            MU.applica_verbo(doc, iB, 'piu scuro')      # basso caldo, non brillante
        except Exception:                               # noqa: BLE001
            pass
        MU.scrivi(doc, cB, basso_due())

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
    b = basso_due()
    print('basso 2-feel:', sum(len(v) for v in b.values()), 'note /', BATTUTE, 'battute')
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
