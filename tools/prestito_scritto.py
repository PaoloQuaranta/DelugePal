"""Il pezzo di prova del prestito modale, COMPOSTO seguendo
docs/istruzioni/armonia-prestito.md.

Un giro in Do maggiore col iv minore (Fm7) come colore centrale -- il prestito
piu' caldo, dal Do minore parallelo (Smith, Jazz Theory, p. 66). La melodia ci
canta sopra il la bemolle: e' li' che il prestito si sente, in cima.

Nessun sorteggio: ogni nota e' una scelta, col motivo accanto.

  battuta  accordo   grado   melodia   perche'
  1        Cmaj7     I        mi4      la casa, stabile
  2        Em7       iii      sol4     ancora diatonico
  3        Fmaj7     IV       la4      il IV, con il la NATURALE in cima
  4        Fm7       iv       lab4     il PRESTITO: il la scende al la bemolle
  5        Em7       iii      sol4     si rientra in casa
  6        Dm7       ii       fa4      la preparazione
  7        G7        V        re4      la dominante
  8        Cmaj7     I        do4      a casa

Il cuore e' il IV->iv->I delle battute 3-4-5: il la naturale del Fmaj7 cala al
la bemolle del Fm7 e poi la casa torna. Il colore e' tutto in quel semitono.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: 8 battute. Il IV diventa iv fra la 3 e la 4: Fmaj7 -> Fm7, il prestito.
#: Poi ii-V (Dm7 G7) e ritorno a casa. Una sola sigla per battuta.
PROGRESSIONE = 'Cmaj7 | Em7 | Fmaj7 | Fm7 | Em7 | Dm7 | G7 | Cmaj7'

#: La melodia, una nota per battuta, registro do4 (sopra il comping a do3).
#: Il la naturale della battuta 3 (su Fmaj7) scende al la bemolle della 4 (su
#: Fm7): e' il colore IV->iv portato in cima, la ragione del pezzo.
MELODIA = 'mi4 sol4 la4 lab4 sol4 fa4 re4 do4'

#: Il basso sulle fondamentali, una per battuta, registro do2.
BASSO = 'do2 mi2 fa2 fa2 mi2 re2 sol2 do2'


def comping():
    """Gli accordi, voicing per terze (NON quartale -- lezione di PERCHE)."""
    return MU.armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                      durata='1/1')


def tema():
    """La melodia sopra il comping."""
    return MU.melodia(MELODIA, durata='1/1')


def basso():
    """Il basso sulle fondamentali."""
    return MU.melodia(BASSO, durata='1/1')


if __name__ == '__main__':
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3'))
