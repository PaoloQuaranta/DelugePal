"""Il pezzo di CONFRONTO dei voicing, seguendo docs/istruzioni/voicing.md.

Lo STESSO ii-V-I -- Dm7 | G7 | Cmaj7 -- suonato tre volte di fila, ognuna con un
voicing diverso, sullo stesso materiale: cosi' la differenza all'orecchio e'
SOLO il voicing. Un basso sulle fondamentali gira per tutte e tre (necessario
perche' il rootless la fondamentale non ce l'ha, e raddoppia quella degli altri
due). Rhodes per gli accordi, Square Saw Bass per il basso. Niente melodia ne'
batteria: si ascolta il PESO.

Metodo (voicing.md, 13 settembre 2026): [CALC] + un ascolto. Le meccaniche sono
gia' blindate dai test test_voicing_*; qui l'utente ascolta QUALE voicing regge,
e per quale contesto -- la parte che il [CALC] non decide.

  passata  battute  voicing              cosa si sente
  1        1-3      chiuso               il corpo, tutte le note vicine
  2        5-7      senza-fondamentale   il suono del pianista jazz (col basso)
  3        9-11     drop2                la tessitura spalancata
  (le battute 4, 8, 12 sono vuote: staccano una passata dall'altra)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: Lo stesso ii-V-I per tutte e tre le passate.
PROGRESSIONE = 'Dm7 | G7 | Cmaj7'

#: I tre voicing messi a confronto, nell'ordine in cui si sentono.
VOICINGS = ('chiuso', 'senza-fondamentale', 'drop2')

#: Un accordo per battuta; ogni passata sono 3 battute + 1 vuota = 4 battute,
#: cosi' l'orecchio stacca una passata dall'altra. Dodici battute in tutto.
_BATTUTA = MU.durata_in_tick('1/1')
_PASSATA = 4 * _BATTUTA
REGISTRO = 'do3'

#: Il basso sulle fondamentali (re-sol-do), una passata alla volta, con la
#: quarta battuta vuota (`.`). Da' la fondamentale al rootless e raddoppia
#: quella del chiuso e del drop2.
BASSO = ('re2 sol2 do2 . ' * 3).strip()


def comping() -> dict[int, list]:
    """Le tre passate del ii-V-I, una per voicing, in fila nel tempo."""
    fuse: dict[int, list] = {}
    for i, voic in enumerate(VOICINGS):
        parte = MU.armonia(PROGRESSIONE, voicing=voic, registro=REGISTRO,
                           durata='1/1', da=i * _PASSATA, velocity=76)
        for y, note in parte.items():
            fuse.setdefault(y, []).extend(note)
    return fuse


def basso() -> dict[int, list]:
    """Il basso sulle fondamentali, per tutte e tre le passate."""
    return MU.melodia(BASSO, durata='1/1', articolazione='staccato', velocity=80)


if __name__ == '__main__':
    for voic in VOICINGS:
        print(f'--- {voic} ---')
        print(MU.racconta_armonia(PROGRESSIONE, voicing=voic, registro=REGISTRO))
