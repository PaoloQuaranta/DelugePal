"""Il pezzo di prova delle medianti cromatiche, COMPOSTO seguendo
docs/istruzioni/medianti-cromatiche.md.

Do che oscilla con le sue due medianti maggiori -- Lab (sotto) e Mi (sopra) --
e torna a casa. Ogni cambio condivide una nota con Do: la morbidezza. La
melodia tocca le note cromatiche nuove (mib, sol#). condotta di default: la
nota comune tiene. Nessun sorteggio.

  battuta  accordo  melodia  perche'
  1        C         mi4     la casa
  2        Ab        mib4    mediante sotto (terza magg.): nota comune do, nuovo il mib
  3        C         mi4     a casa
  4        E         sol#4   mediante sopra (terza magg.): nota comune mi, nuovo il sol#
  5        C         sol4    a casa
  6        Ab        lab4    di nuovo sotto
  7        E         si4     di nuovo sopra (Lab->Mi e' anch'esso mediante, comune sol#)
  8        C         do5     a casa
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: 8 battute: Do fra Lab (mediante giu') e Mi (mediante su'), ritorno a casa.
PROGRESSIONE = 'C | Ab | C | E | C | Ab | E | C'

#: La melodia tocca la nota cromatica nuova di ogni mediante (mib su Lab, sol#
#: su Mi) e chiude sul do.
MELODIA = 'mi4 mib4 mi4 sol#4 sol4 lab4 si4 do5'

#: Il basso sulle fondamentali (do-lab-mi, le medianti).
BASSO = 'do2 lab2 do2 mi2 do2 lab2 mi2 do2'


def comping():
    """Gli accordi, voicing per terze, con la condotta (la nota comune tiene)."""
    return MU.armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                      durata='1/1')


def tema():
    """La melodia che tocca le note cromatiche."""
    return MU.melodia(MELODIA, durata='1/1')


def basso():
    """Il basso sulle fondamentali."""
    return MU.melodia(BASSO, durata='1/1')


if __name__ == '__main__':
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3'))
