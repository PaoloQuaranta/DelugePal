"""Il pezzo dell'ARCO DINAMICO, seguendo docs/istruzioni/arco-dinamico.md.

Lo stesso AABA di forma_scritto, ma con l'ARCO steso sopra (casella 9 di
docs/repertori/jazz.md): si parte radi, si cresce, si CULMINA sul ponte, si
RICADE sull'ultimo A. Tre leve insieme, tutte che salgono verso il ponte:

  sezione  densita' (note)  ritmo armonico   dinamica     cosa fa
  A1       rada  (4)        lento (1/batt)   piano (0.65) la casa, sottovoce
  A2       media (8)        lento (1/batt)   mezzo (0.85) cresce
  B ponte  fitta (16)       VELOCE (2/batt)  forte (1.2)  il CULMINE
  A3       rada  (4)        lento (1/batt)   mezzo (0.75) ricade a casa

⚠️ Il ponte fa DUE cose in una: e' il culmine dell'arco E raddoppia il ritmo
armonico (2 accordi a battuta invece di 1). Cosi' questo pezzo prova, nello
stesso ascolto, l'arco dinamico e il ritmo armonico (docs/istruzioni/ritmo-armonico.md,
che non era mai stato ascoltato).

Metodo: [CALC] + un ascolto. `MU.dinamica` scala le velocity (la leva delle
dinamiche); densita' e ritmo armonico vengono da quante note si scrivono e da
`durata`. test_dinamica e test_arco_scritto blindano i conti; qui l'utente
ascolta se l'arco si sente. Si suona dall'arranger.
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import parse_file, musica as MU               # noqa: E402
from delugexml import song as S, create as C, arranger as A  # noqa: E402

BARRA = MU.TICK_PER_BATTUTA
MAPPA = 'A1 A2 B A3'
BATTUTE_SEZIONE = 4
REGISTRO = 'do3'
VEL_BASE = 90

#: Le quattro sezioni: (accordi, durata_acc, melodia, durata_mel, dinamica).
#: L'arco e' nelle tre leve -- densita', durata (ritmo armonico), dinamica.
SEZIONI = {
    # A1: rada, armonia lenta (1 accordo a battuta), piano
    'A1': ('Cmaj7 | Am7 | Dm7 | G7', '1/1',
           'mi4 sol4 mi4 do4', '1/1', 0.65),
    # A2: piu' densa, stessa armonia lenta, mezzo forte
    'A2': ('Cmaj7 | Am7 | Dm7 | G7', '1/1',
           'mi4 sol4 la4 sol4 mi4 re4 do4 re4', '1/2', 0.85),
    # B (ponte): il culmine -- fitto, armonia VELOCE (2 accordi a battuta), forte
    'B':  ('Fmaj7 | Bb7 | Em7 | A7 | Dm7 | G7 | Cmaj7 | G7', '1/2',
           'sol4 la4 si4 do5 re5 do5 si4 la4 sol4 la4 si4 do5 si4 la4 sol4 mi4', '1/4', 1.2),
    # A3: ricade -- rada, armonia lenta, mezzo piano
    'A3': ('Cmaj7 | Am7 | Dm7 | G7', '1/1',
           'mi4 sol4 mi4 do4', '1/1', 0.75),
}


def _accordi(nome: str):
    spec, dur, _m, _dm, vel = SEZIONI[nome]
    return MU.dinamica(MU.armonia(spec, durata=dur, registro=REGISTRO,
                                  velocity=VEL_BASE), vel)


def _melodia(nome: str):
    _s, _d, mspec, dur, vel = SEZIONI[nome]
    return MU.dinamica(MU.melodia(mspec, durata=dur, velocity=VEL_BASE), vel)


def _idx(doc, clip) -> int:
    return next(i for i, (_c, c) in enumerate(S.clips(doc)) if c is clip)


def _svuota(clip) -> None:
    nr = clip.find('noteRows')
    if nr is not None:
        clip.children.remove(nr)


def nuovo() -> tuple[object, dict]:
    """Un doc fresco con le 8 clip (4 sezioni x 2 strumenti), arco gia' scritto.

    Ritorna `(doc, sezioni)` pronto per `MU.forma`."""
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file('refs/songs/TEMPL0.XML')
        MU.togli(doc, doc.root.find('instruments').children[0])
        S.set_scale(doc, 'C', 'maggiore')
        S.set_bpm(doc.root, 120)

        _iC, cA1 = C.add_track(doc, 'refs/synths/Tal Rhodes.XML',
                               name='CHORDS', folder='SYNTHS', length=4 * BARRA)
        _iM, mA1 = C.add_track(doc, 'refs/synths/062 Trumpet.XML',
                               name='MELODY', folder='SYNTHS',
                               length=4 * BARRA, colour_offset='16')
        MU.scrivi(doc, cA1, _accordi('A1'))
        MU.scrivi(doc, mA1, _melodia('A1'))

        sez = {'A1': [cA1, mA1]}
        for k, nome in enumerate(('A2', 'B', 'A3'), start=1):
            cX = S.duplicate_clip(doc, _idx(doc, cA1), section=str(k),
                                  name=f'CH_{nome}')
            mX = S.duplicate_clip(doc, _idx(doc, mA1), section=str(k),
                                  name=f'ME_{nome}')
            _svuota(cX)
            _svuota(mX)
            MU.scrivi(doc, cX, _accordi(nome))
            MU.scrivi(doc, mX, _melodia(nome))
            sez[nome] = [cX, mX]

    return doc, sez


def costruisci() -> tuple[object, list]:
    """Il doc con l'AABA e l'arco steso sull'arranger, pronto da caricare."""
    doc, sez = nuovo()
    piano = MU.forma(doc, MAPPA, sez, battute=BATTUTE_SEZIONE)
    A.open_in_arranger(doc)
    return doc, piano


def profilo() -> dict:
    """L'arco misurato sul materiale: densita', attacchi d'accordo, velocity."""
    out = {}
    for nome in ('A1', 'A2', 'B', 'A3'):
        me = _melodia(nome)
        ch = _accordi(nome)
        note = [n for v in me.values() for n in v]
        out[nome] = {
            'note': len(note),
            'accordi': len({n.pos for v in ch.values() for n in v}),
            'vel': round(sum(n.velocity for n in note) / max(1, len(note))),
        }
    return out


if __name__ == '__main__':
    for nome, p in profilo().items():
        print(f"{nome:<4} note {p['note']:>2}  accordi {p['accordi']}  vel {p['vel']:>3}")
    doc, piano = costruisci()
    print(MU.racconta_forma(piano))
    print('verifica:', MU.verifica(doc) or 'ok')
