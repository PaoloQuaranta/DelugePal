"""Il pezzo di prova della scala ottatonica, COMPOSTO seguendo
docs/istruzioni/scala-ottatonica.md.

Il ciclo dei quattro dom7 a terza minore -- C7 Eb7 Gb7 A7 -- tutti dentro una
sola ottatonica, con una linea ottatonica discendente in cima. Il suono
sospeso e simmetrico della scala: non risolve, shimmera. Nessun sorteggio.

  battuta  accordo  melodia  (la linea discende sull'ottatonica di Do)
  1        C7        do5
  2        Eb7       sib4
  3        Gb7       la4
  4        A7        sol4
  5        C7        solb4
  6        Eb7       mi4
  7        Gb7       mib4
  8        A7        reb4

Il ciclo gira per terze minori e non torna mai a una tonica: e' il punto.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: 8 battute: il ciclo per terza minore, due rotazioni. Non risolve. Tutti e
#: quattro i dom7 stanno nell'ottatonica HW di Do.
PROGRESSIONE = 'C7 | Eb7 | Gb7 | A7 | C7 | Eb7 | Gb7 | A7'

#: La linea ottatonica discendente, una nota per battuta (do-sib-la-sol-solb-
#: mi-mib-reb): fa sentire la scala per intero, in cima.
MELODIA = 'do5 sib4 la4 sol4 solb4 mi4 mib4 reb4'

#: Il basso sulle fondamentali del ciclo (do-mib-solb-la, per terze minori).
BASSO = 'do2 mib2 solb2 la2 do2 mib2 solb2 la2'


def comping():
    """Gli accordi del ciclo, voicing per terze (la simmetria da' note comuni)."""
    return MU.armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                      durata='1/1')


def tema():
    """La linea ottatonica discendente."""
    return MU.melodia(MELODIA, durata='1/1')


def basso():
    """Il basso sulle fondamentali."""
    return MU.melodia(BASSO, durata='1/1')


if __name__ == '__main__':
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3'))
