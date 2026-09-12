"""Il pezzo di prova del planing cromatico, COMPOSTO seguendo
docs/istruzioni/armonia-parallela.md.

Un'onda cromatica di dom7 paralleli -- la stessa forma che scivola per semitoni,
senza funzione. La tromba cavalca la voce in cima (la settima), una linea
cromatica. condotta=False: la forma resta rigida. Nessun sorteggio.

  battuta  accordo  melodia (la 7a di ogni dom7, linea cromatica)
  1        C7        sib4
  2        Db7       si4
  3        D7        do5
  4        Eb7       reb5
  5        E7        re5
  6        Eb7       reb5
  7        D7        do5
  8        Db7       si4

Sale di cinque semitoni e ridiscende: non risolve, e' uno stream.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: 8 battute: il dom7 sale di cinque semitoni e ridiscende. Non risolve.
PROGRESSIONE = 'C7 | Db7 | D7 | Eb7 | E7 | Eb7 | D7 | Db7'

#: La melodia cavalca la settima di ogni dom7 -- una linea cromatica pura
#: (sib-si-do-reb-re-reb-do-si).
MELODIA = 'sib4 si4 do5 reb5 re5 reb5 do5 si4'

#: Il basso sulle fondamentali (anch'esse cromatiche).
BASSO = 'do2 reb2 re2 mib2 mi2 mib2 re2 reb2'


def comping():
    """Gli accordi, voicing per terze, SENZA condotta: la forma resta rigida e
    parallela (con la condotta si romperebbe il planing)."""
    return MU.armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                      durata='1/1', condotta=False)


def tema():
    """La linea cromatica in cima."""
    return MU.melodia(MELODIA, durata='1/1')


def basso():
    """Il basso sulle fondamentali."""
    return MU.melodia(BASSO, durata='1/1')


if __name__ == '__main__':
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                              condotta=False))
