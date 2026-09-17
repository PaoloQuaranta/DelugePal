"""TWOBEAT (dixieland), seguendo docs/istruzioni/basso-twobeat.md e
batteria-twobeat.md.

Il terzo feel diverso dallo swing (priorita' 3 dell'utente, dopo funk e ballad).
Come la ballad, la sezione ritmica NON ha corpus: il Groove MIDI non ha un feel
«twobeat», la Weimar da' il solista (32 assoli TWOBEAT, tutti TRADITIONAL --
Armstrong, Bechet, Kid Ory, Bix, Dodds, mediana 184 BPM). Quindi qui e'
[LIB]+[DEC] sulla sezione ritmica, [MIS] solo sul genere e sul tempo.

Il twobeat e' il 2-feel VELOCE e SALTELLANTE: 1 e 3 come la ballad, ma corto,
brillante, con lo scatto (Riley p. 57: «non lasciare che la musica suoni
addormentata»). Il feel e' l'OOM-PAH:

  basso      1 e 3, note CORTE, brillanti, + rilancio; una battuta «in 4» al V7
  cassa      1 e 3, con il basso -- l'oom
  charleston 2 e 4, croccante -- il pah
  rullante   press roll approssimato (crome molli, accento sul 2 e 4)
  comping    «stride»: accordi corti sul 2 e 4 (four-to-the-bar ai giunti)
  ride       niente spang-a-lang -- solo uno splash a inizio frase

Giro dixieland in Sib: la catena di dominanti (III7-VI7-II7-V7-I), la firma del
ragtime/trad. Metodo: ritmo, l'ascolto pieno. Verdetto (17 settembre 2026): «ok funziona».
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
PRESET_PIANO = RADICE / 'refs' / 'synths' / 'Pianism I.XML'
PRESET_BASSO = RADICE / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = RADICE / 'refs' / 'kits' / 'KIT009.XML'

BPM = 184                                  # la mediana MISURATA del twobeat Weimar
SWING = 62                                 # levare ~62%: lo swing pieno dei 180-240 (jazz.md casella 4)
# la catena di dominanti in Sib -- la firma del dixieland/ragtime
PROG = 'Bb6 | D7 | G7 | C7 | F7 | Bb6 | Eb6 | F7'
SIGLE = [s.strip() for s in PROG.split('|')]
BATTUTE = len(SIGLE)

# le battute «in 4» (rilancio in walking sotto una dominante che risolve al Sib)
BATTUTE_IN_QUATTRO = {4, 7}
# le battute col rilancio cromatico sull'ultima croma (una ogni tanto, non tutte)
BATTUTE_RILANCIO = {1, 5}


def _vicino(pc: int, rif: int, lo: int = 28, hi: int = 48) -> int:
    """La nota di classe `pc` piu' vicina a `rif`, dentro mi1-do3."""
    best = None
    for y in range(lo, hi + 1):
        if y % 12 == pc and (best is None or abs(y - rif) < abs(best - rif)):
            best = y
    return best


def _roots() -> list[int]:
    """La fondamentale scelta (numero di nota) di ogni battuta, incatenata per
    prossimita' come nel walking."""
    rif = 34                                   # Sib1
    out = []
    for sig in SIGLE:
        r = _vicino(MU.sigla(sig).fondamentale, rif)
        out.append(r)
        rif = r
    return out


def basso() -> dict:
    """Il 2-feel dixieland: fond. sul 1, quinta sul 3, CORTE (non minime tenute
    come la ballad), + un rilancio cromatico su alcune battute; due battute «in
    4» che camminano sotto il V7 verso il Sib."""
    from delugexml.notes import Note                          # noqa: PLC0415
    roots = _roots()
    voce: dict = {}

    def metti(alt, pos, dur, vel):
        voce.setdefault(alt, []).append(Note(pos=pos, length=dur, velocity=vel))

    for bar, sig in enumerate(SIGLE):
        da = bar * B
        root = roots[bar]
        prossima = roots[(bar + 1) % BATTUTE]

        if bar in BATTUTE_IN_QUATTRO:
            # «in 4»: il V7 (F7) cammina in discesa verso il Sib della battuta dopo
            # Fa2 - Mib2 - Re2 - Do2  ->  Sib1 sul downbeat seguente
            for i, alt in enumerate((41, 39, 38, 36)):
                metti(alt, da + i * MOV, 84, 86)      # semiminime corte
            continue

        s = MU.sigla(sig)
        quinta = _vicino((s.fondamentale + s.gradi.get(5, 7)) % 12, root)
        metti(root, da, 72, 92)                        # il 1  (corto, con scatto)
        metti(quinta, da + MIN, 72, 88)                # il 3
        if bar in BATTUTE_RILANCIO:
            # rilancio: un semitono sotto la fond. della battuta dopo, sull'ultima croma
            metti(prossima - 1, da + B - CROMA, CROMA, 80)
    return voce


def batteria() -> dict:
    """L'oom-pah: cassa 1-3, charleston croccante 2-4, press roll sul rullante
    (crome molli, accento sul backbeat), un piatto solo a inizio frase. NIENTE
    spang-a-lang (Riley: nel 2-feel meno figure di semiminima sul ride)."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voci = {'KICK': [], 'HATC': [], 'SNARE': [], 'RIDE': []}
    for bar in range(BATTUTE):
        da = bar * B
        # oom: cassa su 1 e 3
        voci['KICK'] += MU.passi('x.......x.......', da=da, velocity=70)
        # pah: charleston croccante su 2 e 4
        voci['HATC'] += MU.passi('....x.......x...', da=da, velocity=64)
        # press roll: crome molli, tocco piu' fermo che ARRIVA sul 2 e sul 4
        for i in range(8):
            pos = da + i * CROMA
            sul_backbeat = pos % B in (MOV, 3 * MOV)   # 2 e 4
            vel = 46 if sul_backbeat else 30
            if bar == BATTUTE - 1 and i >= 6:          # turnaround: pickup fill
                vel = 54
            voci['SNARE'].append(Note(pos=pos, length=P, velocity=vel))
        # ride: solo uno splash a inizio delle frasi (bar 0 e 4), mai il giggidi'
        if bar in (0, 4):
            voci['RIDE'].append(Note(pos=da, length=MOV, velocity=42))
    return voci


def comping() -> dict:
    """Lo «stride» dixieland: accordi corti sul 2 e sul 4 (il pah), four-to-the-
    bar ai giunti (bar 4 e 7) per spingere. Voicing chiuso, registro medio."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voce: dict = {}
    for bar, sig in enumerate(SIGLE):
        da = bar * B
        note = MU.voci(sig, voicing='chiuso', registro='do4')
        battiti = (0, MOV, MIN, 3 * MOV) if bar in BATTUTE_IN_QUATTRO \
            else (MOV, 3 * MOV)                        # 2 e 4, oppure tutti e 4
        for b in battiti:
            for alt in note:
                voce.setdefault(alt, []).append(
                    Note(pos=da + b, length=60, velocity=58))   # corti, «chomp»
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
        S.set_swing(doc, SWING, figura='1/8')      # lilt sulle crome (roll, rilanci)
        S.set_scale(doc, 'Bb', 'maggiore')
        for strumento in list(S.instruments(doc)):
            MU.togli(doc, strumento)

        lung = BATTUTE * B

        iP, cP = C.add_track(doc, str(PRESET_PIANO), name='PIANO',
                             folder='SYNTHS', length=lung, playing=True)
        MU.scrivi(doc, cP, comping())

        iB, cB = C.add_track(doc, str(PRESET_BASSO), name='BASSO', folder='SYNTHS',
                             length=lung, colour_offset='16', playing=True)
        try:
            MU.applica_verbo(doc, iB, 'piu brillante')   # basso trad brillante, non scuro
        except Exception:                                # noqa: BLE001
            pass
        MU.scrivi(doc, cB, basso())

        kit, cK = C.add_track(doc, str(KIT), name='KIT009', folder='KITS',
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
    print('basso 2-feel:', sum(len(v) for v in b.values()), 'note /', BATTUTE,
          'battute =', round(sum(len(v) for v in b.values()) / BATTUTE, 2), 'per battuta')
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
