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


# --- il secondo pezzo: casa MINORE, il IV maggiore preso dal maggiore parallelo
#
#   battuta  accordo  grado  melodia  perche'
#   1        Am       i       mi4     la casa minore
#   2        Em       v       sol4    diatonico
#   3        Dm       iv       fa4     il iv, col fa NATURALE (b6)
#   4        D        IV      fa#4    il PRESTITO: il fa sale al fa# (nat6), la schiaritura
#   5        Am       i       mi4     si rientra
#   6        Dm       iv       fa4     di nuovo il iv
#   7        E7       V7      mi4     la dominante (il sol# e' la sensibile, NON un prestito)
#   8        Am       i       la4     a casa
#
#: Il cuore e' il iv->IV delle battute 3-4: Dm -> D maggiore, il fa che sale al
#: fa#. E' il contrario simmetrico del IV->iv (la -> la bemolle) del pezzo in Do.
PROGRESSIONE_MIN = 'Am | Em | Dm | D | Am | Dm | E7 | Am'
MELODIA_MIN = 'mi4 sol4 fa4 fa#4 mi4 fa4 mi4 la4'
BASSO_MIN = 'la2 mi2 re2 re2 la2 re2 mi2 la2'


def comping_min():
    """Gli accordi del pezzo in minore, voicing per terze."""
    return MU.armonia(PROGRESSIONE_MIN, voicing='chiuso', registro='la2',
                      durata='1/1')


def tema_min():
    """La melodia del pezzo in minore."""
    return MU.melodia(MELODIA_MIN, durata='1/1')


def basso_min():
    """Il basso del pezzo in minore."""
    return MU.melodia(BASSO_MIN, durata='1/1')


# --- il terzo pezzo: i colori del minore JAZZ (line cliche') + Piccardia finale
#
#   battuta  accordo   grado      melodia  perche'
#   1        Am        i           la4     tonica, l'inizio del cliche'
#   2        Am(maj7)  i(maj7)    sol#4    il nat7 (G#), preso dal maggiore
#   3        Am7       i7          sol4    il b7 (G), la discesa continua
#   4        Am6       i6         fa#4     il nat6 (F#): il colore della minore melodica
#   5        Dm7       iv          fa4     ci si muove
#   6        E7        V7          mi4     la dominante (NON un prestito)
#   7        Am        i           mi4     tonica minore
#   8        A         I (Picc.)  do#4     la Piccardia: la tonica diventa MAGGIORE
#
#: Bat. 1-4: il line cliche', la discesa A-G#-G-F# su pedale di La -- il nat7 e
#: il nat6 presi dal maggiore parallelo, il suono della minore melodica/jazz.
#: Bat. 8: la terza di Piccardia, il finale che si apre su La maggiore.
PROGRESSIONE_JAZZMIN = 'Am | Am(maj7) | Am7 | Am6 | Dm7 | E7 | Am | A'
MELODIA_JAZZMIN = 'la4 sol#4 sol4 fa#4 fa4 mi4 mi4 do#4'
BASSO_JAZZMIN = 'la1 la1 la1 la1 re2 mi2 la1 la1'


def comping_jazzmin():
    """Gli accordi del terzo pezzo, voicing per terze."""
    return MU.armonia(PROGRESSIONE_JAZZMIN, voicing='chiuso', registro='la2',
                      durata='1/1')


def tema_jazzmin():
    """La melodia del terzo pezzo (il line cliche' in cima)."""
    return MU.melodia(MELODIA_JAZZMIN, durata='1/1')


def basso_jazzmin():
    """Il basso del terzo pezzo: pedale di La sotto il cliche'."""
    return MU.melodia(BASSO_JAZZMIN, durata='1/1')


if __name__ == '__main__':
    print('=== pezzo in Do maggiore (il iv minore) ===')
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3'))
    print('\n=== pezzo in La minore (il IV maggiore) ===')
    print(MU.racconta_armonia(PROGRESSIONE_MIN, voicing='chiuso', registro='la2'))
    print('\n=== pezzo in La minore jazz (line cliche + Piccardia) ===')
    print(MU.racconta_armonia(PROGRESSIONE_JAZZMIN, voicing='chiuso', registro='la2'))
