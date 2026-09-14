"""AGGANCIO: il basso che va incontro alla batteria, seguendo
docs/istruzioni/aggancio.md.

Il difetto d'origine dell'aggancio (casella 5 di docs/repertori/jazz.md, 6
settembre 2026): il basso del generatore era **quantizzato esatto, dispersione
zero**, e un basso senza microtiming NON puo' andare incontro a una batteria che
ce l'ha (il groove template). Restava un metronomo sotto una parte che respira.

Isola la cura. Lo STESSO walking, sotto la STESSA batteria (groove template di
drummer1/session1/49), due passate:

  passata 1  QUANTIZZATO  il basso sulla griglia esatta -- il difetto
  passata 2  CON FLOAT    il float REALE di un basso JTD nominato (Rufus Reid,
                          "Bemsha Swing", 1984), nota per nota

La batteria e' identica nelle due passate: cambia solo se il basso ha il suo
microtiming. `jtd.microtiming()` da' la sequenza di deviazioni del basso vero;
`MU.applica_microtiming()` la posa sul walking, in ordine.

⚠️ IL FLOAT E' [OSS] SU UN'ESECUZIONE, non una media: mediare il microtiming di
bassisti diversi lo tira verso zero -- la stessa ragione del groove template.

⚠️ NON riproduce la misura 3 (coincidenza fuori griglia 1,60x). Quello e' un
numero di corpus, e sul generatore la griglia a sedicesimi lo rende
tutto-o-niente (casella 5). Qui si sente un'altra cosa, piu' semplice: un basso
che RESPIRA contro uno che e' un metronomo. Metodo: ritmo, l'ascolto pieno.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402
from delugexml import groove as GR                            # noqa: E402
from delugexml import jtd as JT                               # noqa: E402

B = MU.TICK_PER_BATTUTA
MOV = MU.TICK_PER_MOVIMENTO

#: Fixture e dataset non versionati: il test salta se mancano.
BASE = RADICE / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
JTD = RADICE / 'to-read' / 'MIDI' / 'jazz-trio-database-v02.zip'
TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
KIT = RADICE / 'refs' / 'kits' / 'KIT009.XML'
PRESET_BASSO = RADICE / 'refs' / 'synths' / 'Square Saw Bass.XML'

BPM = 125
SWING = 60
PAVIMENTO = 55                                # come groove-template.md

#: La batteria: l'esecuzione nominata del groove template (§6-terdecies).
ESEC_BATT = 'drummer1/session1/49'
#: Il basso: l'esecuzione JTD nominata da cui viene il float. Rufus Reid, un
#: bassista con un lay-back netto (misurato: +2 tick, dispersione ~3).
BASSO_JTD = 'barronk-bemshaswing-reidrwaitsf-1984-05bc9ae9'

VOCI = {'ride': 'RIDE', 'charleston a pedale': 'HATC',
        'rullante': 'SNARE', 'kick': 'KICK'}

#: Un groove steady (non reattivo: qui il fuoco e' il basso). Costante ogni battuta.
RIDE = 'x...x.x.x...x.x.'
PEDALE = '....x.......x...'
SNARE = '..x......x......'
KICK = '......x.......x.'
BATTUTE = 4
PASSATA = (BATTUTE + 2) * B

#: Il walking: quattro semiminime per battuta, un ii-V-I in Do (le altezze non
#: sono il punto -- il punto e' il TIMING).
WALKING = [
    ('re2', 'fa2', 'la2', 'do3'),     # Dm7
    ('si2', 'sol2', 'fa2', 're2'),    # G7
    ('do2', 'mi2', 'sol2', 'la2'),    # Cmaj7
    ('sol2', 'mi2', 're2', 'do2'),    # Cmaj7
]


def _pattern_batteria() -> dict[str, str]:
    return {'ride': RIDE, 'charleston a pedale': PEDALE,
            'rullante': SNARE, 'kick': KICK}


def note_batteria(voce: str, offset: int) -> list:
    patt = _pattern_batteria()[voce]
    note = []
    for bar in range(BATTUTE):
        note.extend(MU.passi(patt, da=offset + bar * B, velocity=80))
    return note


def batteria_col_tocco(prof, offset: int):
    tocchi = {v: note_batteria(v, offset) for v in VOCI}
    for v in VOCI:
        MU.applica_groove(tocchi[v], prof, dove=v)
    MU.rimappa_dinamica(list(tocchi.values()), PAVIMENTO)
    return tocchi


def eventi_walking(offset: int) -> list:
    fuori = []
    for bar, note4 in enumerate(WALKING):
        for k, alt in enumerate(note4):
            fuori.append((offset + bar * B + k * MOV, alt, '1/4'))
    return fuori


def scarti_float_tick(n: int) -> list[int]:
    """I primi `n` scarti del basso JTD nominato, in tick al tempo del pezzo."""
    sec = JT.microtiming(JTD, BASSO_JTD, 'bass')
    ticks_per_sec = 96 * BPM / 60
    return [round(s * ticks_per_sec) for s in sec[:n]]


def basso_quantizzato(offset: int) -> dict:
    return MU.linea(eventi_walking(offset), articolazione='staccato', velocity=78)


def basso_con_float(offset: int) -> tuple[dict, list[int]]:
    voce = MU.linea(eventi_walking(offset), articolazione='staccato', velocity=78)
    flat = [nt for note in voce.values() for nt in note]
    scarti = scarti_float_tick(len(flat))
    MU.applica_microtiming(flat, scarti)
    return voce, scarti


def costruisci() -> tuple[object, dict]:
    """Il pezzo dell'ascolto. Ritorna `(doc, info)`. Solleva FileNotFoundError
    se manca il dataset o una fixture."""
    import warnings                                           # noqa: PLC0415
    from delugexml import parse_file, song as S              # noqa: PLC0415
    from delugexml import create as C, arranger as A         # noqa: PLC0415
    from delugexml import kit as K                           # noqa: PLC0415

    prof = GR.profilo(BASE, ESEC_BATT)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(str(TEMPL))
        S.set_bpm(doc.root, BPM)
        S.set_swing(doc, SWING, figura='1/8')
        S.set_scale(doc, 'C', 'maggiore')
        for strumento in list(S.instruments(doc)):
            MU.togli(doc, strumento)

        # --- batteria: identica nelle due passate ---
        kit, clip_kit = C.add_track(doc, str(KIT), name='KIT009', folder='KITS',
                                    length=2 * PASSATA, playing=True)
        tenuti = tuple(VOCI.values())
        for nome in [S.nome_drum(d) for d in S.drums(kit)]:
            if nome and nome not in tenuti:
                K.remove_drum(doc, kit, nome)
        for voce, drum in VOCI.items():
            b1 = batteria_col_tocco(prof, 0)[voce]
            b2 = batteria_col_tocco(prof, PASSATA)[voce]
            MU.scrivi(doc, clip_kit, b1 + b2, dove=drum)

        # --- basso: quantizzato (1) vs col float (2) ---
        iB, clip_basso = C.add_track(doc, str(PRESET_BASSO), name='BASSO',
                                     folder='SYNTHS', length=2 * PASSATA,
                                     colour_offset='16')
        quant = basso_quantizzato(0)
        flott, scarti = basso_con_float(PASSATA)
        fuse: dict = {}
        for parte in (quant, flott):
            for y, note in parte.items():
                fuse.setdefault(y, []).extend(note)
        MU.scrivi(doc, clip_basso, fuse)

        A.place(doc, kit, clip_kit, 0, 2 * PASSATA)
        A.place(doc, iB, clip_basso, 0, 2 * PASSATA)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc, {'scarti_float': scarti}


if __name__ == '__main__':
    scarti = scarti_float_tick(16)
    print(f'basso JTD: {BASSO_JTD}')
    print(f'float (primi 16 scarti, tick @{BPM} BPM): {scarti}')
    import statistics as st
    print(f'  min {min(scarti)}  max {max(scarti)}  '
          f'mediana {st.median(scarti):.1f}  dispersione {st.pstdev(scarti):.1f}')
