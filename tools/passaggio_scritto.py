"""Il pezzo di prova degli accordi di passaggio e approccio, COMPOSTO seguendo
docs/istruzioni/accordi-di-passaggio.md.

La diminuita di passaggio (C#dim7, basso cromatico do->do#->re) e il tritone
sub (Db7, approccio a Do dall'alto), in un turnaround in Do. condotta di
default: la colla e' morbida. Nessun sorteggio.

  battuta  accordo   melodia  perche'
  1        Cmaj7      sol4    la casa
  2        C#dim7     la#4    diminuita di passaggio (basso do#), la 7a
  3        Dm7        la4     il ii
  4        Db7        lab4    tritone sub del G7: approccia Do dall'alto
  (le battute 5-8 ripetono: il turnaround rigira in cima)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: 8 battute: un turnaround in Do con la diminuita di passaggio e il tritone
#: sub. Il Db7 dell'ultima battuta rigira sul Cmaj7 in cima.
PROGRESSIONE = 'Cmaj7 | C#dim7 | Dm7 | Db7 | Cmaj7 | C#dim7 | Dm7 | Db7'

#: La melodia tiene note d'accordo, con la discesa sib->la->lab che eco del
#: movimento cromatico del basso.
MELODIA = 'sol4 la#4 la4 lab4 sol4 la#4 la4 lab4'

#: Il basso sulle fondamentali (do-do#-re-reb...): porta il cromatismo.
BASSO = 'do2 do#2 re2 reb2 do2 do#2 re2 reb2'


def comping():
    """Gli accordi, voicing per terze, con la condotta (la colla e' morbida)."""
    return MU.armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                      durata='1/1')


def tema():
    """La melodia su note d'accordo."""
    return MU.melodia(MELODIA, durata='1/1')


def basso():
    """Il basso cromatico sulle fondamentali."""
    return MU.melodia(BASSO, durata='1/1')


if __name__ == '__main__':
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3'))
