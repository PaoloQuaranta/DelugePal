"""Il pezzo di prova della scala esatonale, COMPOSTO seguendo
docs/istruzioni/scala-esatonale.md.

Il ciclo dei dom7#5 che salgono per tono -- C7#5 D7#5 E7#5 ... -- tutti dentro
una sola esatonale, con una melodia ondeggiante whole-tone in cima. Il suono
sospeso, acquatico, di Debussy: non risolve, galleggia. Nessun sorteggio.

  battuta  accordo  melodia  (la linea ondeggia sull'esatonale di Do)
  1        C7#5      sol#4
  2        D7#5      la#4
  3        E7#5      do5
  4        F#7#5     re5
  5        G#7#5     mi5
  6        A#7#5     re5
  7        C7#5      do5
  8        D7#5      la#4

Il ciclo sale per toni e non si posa: e' il punto.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: 8 battute: i dom7#5 salgono per tono, i sei distinti piu' il ritorno. Non
#: risolve: galleggia. Tutti dentro l'esatonale di Do.
PROGRESSIONE = 'C7#5 | D7#5 | E7#5 | F#7#5 | G#7#5 | A#7#5 | C7#5 | D7#5'

#: La melodia ondeggiante, whole-tone, una nota per battuta.
MELODIA = 'sol#4 la#4 do5 re5 mi5 re5 do5 la#4'

#: Il basso sulle fondamentali del ciclo (do-re-mi-fa#-sol#-la#, per toni).
BASSO = 'do2 re2 mi2 fa#2 sol#2 la#2 do2 re2'


def comping():
    """Gli accordi del ciclo, voicing per terze."""
    return MU.armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                      durata='1/1')


def tema():
    """La melodia ondeggiante whole-tone."""
    return MU.melodia(MELODIA, durata='1/1')


def basso():
    """Il basso sulle fondamentali."""
    return MU.melodia(BASSO, durata='1/1')


if __name__ == '__main__':
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3'))
