"""FUNK dritto, seguendo docs/istruzioni/batteria-funk.md e basso-funk.md.

Il primo pezzo del feel funk (15-16 settembre 2026): il passo oltre lo swing.
Niente walking, niente giggidi'. Cassa sincopata ancorata sul *the one*,
backbeat sul 2 e sul 4 col tessuto dei ghost, charleston in crome; il basso e'
un riff fitto (~7 note/battuta, MISURATO su 40 basslinee funk), fatto di
fondamentale ribattuta, ottave, ghost note e cromatismi, agganciato alla cassa.

E' l'ESEMPIO LAVORATO che le due istruzioni dichiarano mancante: una parte
intera, battuta per battuta, col motivo scritto accanto. NON e' un generatore --
ogni battuta e' una decisione, e il vamp e' Em7 | A7 (E dorico), otto battute.

Il tocco viene da drummer8/session1/1 (funk pulito, 95 BPM, BUR 1,07): kick e
rullante prendono velocity e microtiming MISURATI (applica_groove), il pocket e'
tight (scarti -1/-2 tick) perche' il funk sta sulla griglia -- il carattere e'
nelle velocity, non nello spostamento.

Metodo: ritmo, quindi l'ascolto pieno. I conti li fa la libreria; l'orecchio
dice se groova e se il *the one* tira.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402
from delugexml import groove as GR                            # noqa: E402
from delugexml.notes import Note                             # noqa: E402

B = MU.TICK_PER_BATTUTA      # 384
MOV = MU.TICK_PER_MOVIMENTO  # 96
P = MU.TICK_PER_PASSO        # 24 (un sedicesimo)

#: Fixture e dataset non versionati: chi non li ha, il pezzo non si costruisce.
BASE = RADICE / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
KIT = RADICE / 'refs' / 'kits' / 'KIT009.XML'
PRESET_BASSO = RADICE / 'refs' / 'synths' / 'Square Saw Bass.XML'

BPM = 100                              # mediana del funk nel Groove MIDI
ESEC_BATT = 'drummer8/session1/1'      # funk pulito, BUR 1,07
BATTUTE = 8

#: groove voce -> drum del kit KIT009
VOCI = {'kick': 'KICK', 'rullante': 'SNARE', 'charleston chiuso': 'HATC'}

# --------------------------------------------------------------------------
# La batteria, battuta per battuta. X = accento, x = colpo, o = ghost, . = pausa
# griglia:      1 e + a 2 e + a 3 e + a 4 e + a
# --------------------------------------------------------------------------
KICK_BATT = [
    'x..x....x..x....',   # 1 Em  the one + a-di-1 + il 3 + a-di-3
    'x..x....x..x....',   # 2 A   stesso lock: il funk ripete
    'x..x...xx.......',   # 3 Em  la a-di-2 spinge dentro il 3
    'x..x....x..x..x.',   # 4 A   +di-4: spinge dentro la seconda frase
    'x..x....x..x....',   # 5 Em
    'x..x....x..x....',   # 6 A
    'x..x...xx..x....',   # 7 Em  variazione
    'x..x....x.......',   # 8 A   scarna: lascia posto al fill del rullante
]
SNARE_BATT = [
    '....X..o....X..o',   # 1 backbeat 2 e 4, ghost sulla a-di-2 e a-di-4
    '....X..o....X..o',   # 2
    '....X.o.o...X..o',   # 3 piu' fantasmi (e-di-3)
    '....X..o....X.oo',   # 4 ghost verso il giro
    '....X..o....X..o',   # 5
    '....X..o....X..o',   # 6
    '....X.o.o...X..o',   # 7
    '....X..o..o.oXo.',   # 8 fill leggero nella seconda meta'
]
HATC_BATT = [
    'x.x.x.x.x.x.x.x.',   # crome, il clock
    'x.x.x.x.x.x.x.x.',
    'x.x.x.x.x.x.x.x.',
    'x.x.x.x.x.x.x.x.',
    'x.x.x.x.x.x.x.x.',
    'x.x.x.x.x.x.x.x.',
    'x.x.x.x.x.x.x.x.',
    'x.x.x.x.x.......',   # 8 si ritira per il fill
]
#: charleston aperto: un solo accento sul +di-4 della battuta 4, la spinta di frase
HATO_BATT = {3: 14}      # battuta indice 3 (la 4a), passo 14

# --------------------------------------------------------------------------
# Il basso, battuta per battuta. (passo, altezza, durata_tick, velocity)
# ~7 note/battuta (mediana MISURATA): fondamentale ribattuta, ottava, ghost,
# cromatico. Il CORPO (the one + levare) cade con la cassa (0,3,8), i ghost e i
# levare (2,6,10,14) riempiono dove la cassa tace -- la propulsione.
# Em: E1=28 G1=31 G#1=32 E2=40   A: A1=33 G2=43 A2=45   (mi1-do3 = 28-48)
# --------------------------------------------------------------------------
def _em():
    return [(0, 28, 30, 110),   # E1  THE ONE, accento
            (2, 28, 12, 42),    # E1  ghost ribattuto (+di-1)
            (3, 28, 18, 92),    # E1  push (lock cassa a-di-1)
            (6, 40, 24, 100),   # E2  OTTAVA sul levare del 2
            (8, 28, 18, 90),    # E1  il 3 (lock cassa)
            (10, 31, 18, 86),   # G1  levare del 3
            (14, 32, 12, 82)]   # G#1 approccio cromatico all'A che segue

def _a():
    return [(0, 33, 30, 108),   # A1  THE ONE
            (2, 33, 12, 42),    # A1  ghost ribattuto
            (3, 33, 18, 90),    # A1  push
            (6, 45, 24, 100),   # A2  OTTAVA sul levare del 2
            (8, 33, 18, 90),    # A1  il 3
            (10, 43, 18, 86),   # G2  b7 di A7, levare del 3 (bluesy)
            (14, 28, 12, 82)]   # E1  anticipa il the one dell'Em che segue

BASSO_BATT = [
    _em(),                                   # 1
    _a(),                                    # 2
    _em(),                                   # 3
    _a(),                                    # 4
    _em(),                                   # 5
    _a(),                                    # 6
    _em(),                                   # 7
    # 8  turnaround: A1 - A2 - G2 - F#2 - E2, scende cromatico nel giro
    [(0, 33, 30, 108), (2, 33, 12, 42), (3, 33, 18, 90), (6, 45, 24, 100),
     (8, 45, 18, 96), (10, 43, 18, 90), (12, 42, 12, 86), (14, 40, 12, 90)],
]


def note_voce(voce_groove: str) -> list:
    """Le note di una voce di batteria su tutte le battute (senza tocco)."""
    patt = {'kick': KICK_BATT, 'rullante': SNARE_BATT,
            'charleston chiuso': HATC_BATT}[voce_groove]
    note = []
    for bar in range(BATTUTE):
        note.extend(MU.passi(patt[bar], da=bar * B))
    return note


def note_hato() -> list:
    fuori = []
    for bar, passo in HATO_BATT.items():
        fuori.extend(MU.passi('.' * passo + 'X' + '.' * (15 - passo),
                              da=bar * B))
    return fuori


def note_basso() -> dict:
    voce: dict = {}
    for bar in range(BATTUTE):
        for passo, alt, dur, vel in BASSO_BATT[bar]:
            pos = bar * B + passo * P
            voce.setdefault(alt, []).append(Note(pos=pos, length=dur, velocity=vel))
    return voce


def costruisci() -> tuple[object, dict]:
    """Il pezzo dell'ascolto. Ritorna (doc, rapporti). Solleva FileNotFoundError
    se manca il dataset o una fixture."""
    import warnings                                           # noqa: PLC0415
    from delugexml import parse_file, song as S              # noqa: PLC0415
    from delugexml import create as C, arranger as A         # noqa: PLC0415

    prof = GR.profilo(BASE, ESEC_BATT)
    rapporti: dict = {}
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(str(TEMPL))
        S.set_bpm(doc.root, BPM)
        S.set_swing(doc, 50)               # DRITTO: nessuno swing (funk)
        S.set_scale(doc, 'E', 'dorico')    # il vamp Em7 | A7
        for strumento in list(S.instruments(doc)):
            MU.togli(doc, strumento)

        lung = BATTUTE * B

        # --- batteria: il tocco misurato su kick e rullante e charleston ---
        kit, clip_kit = C.add_track(doc, str(KIT), name='KIT009', folder='KITS',
                                    length=lung, playing=True)
        for voce_groove, drum in VOCI.items():
            note = note_voce(voce_groove)
            rapporti[drum] = MU.applica_groove(note, prof, dove=voce_groove)
            MU.scrivi(doc, clip_kit, note, dove=drum)
        MU.scrivi(doc, clip_kit, note_hato(), dove='HATO')

        # --- basso: il riff agganciato, dritto ---
        iB, clip_basso = C.add_track(doc, str(PRESET_BASSO), name='BASSO',
                                     folder='SYNTHS', length=lung,
                                     colour_offset='16', playing=True)
        MU.scrivi(doc, clip_basso, note_basso())

        A.place(doc, kit, clip_kit, 0, lung)
        A.place(doc, iB, clip_basso, 0, lung)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc, rapporti


if __name__ == '__main__':
    doc, rapporti = costruisci()
    for drum, r in rapporti.items():
        sa = r.get('senza_appoggio') if isinstance(r, dict) else None
        print(f"{drum:6s}: toccate={r.get('toccate')} senza_appoggio={sa}")
    from delugexml import musica as MU2
    print('\n--- verifica ---')
    print(MU2.verifica(doc) or 'ok, vuota')
    print('--- avvertenze ---')
    print(MU2.avvertenze(doc) or 'nessuna')
