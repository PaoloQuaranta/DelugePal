"""La linea di walking del blues, SCRITTA seguendo `docs/istruzioni/walking.md`.

⚠️ Non c'e' nessun sorteggio qui dentro. Ogni nota e' stata scelta applicando
la procedura del *Jazz Theory Justified*, cap. IV, e accanto a ogni battuta c'e'
scritto quale regola. E' la prova del 10 settembre 2026: una linea COMPOSTA
suona meglio di una linea campionata?

La procedura, in breve:

  1. la fondamentale dell'accordo sul movimento in cui l'accordo entra, nella
     ottava che minimizza l'intervallo con la fondamentale precedente;
  2. si riempie guardando l'INTERVALLO fra le fondamentali: terza -> nota di
     passaggio diatonica; quarta o quinta -> una nota del primo accordo;
     seconda -> ripetizione o salto d'ottava; accordo per tutta la battuta ->
     per grado dalla fondamentale alla quinta;
  3. si ammorbidisce con terza, quinta, settima o note estranee.

IL FORMATO. Una riga per battuta, quattro gettoni, uno per movimento:

    fa2      attacca quella nota
    -        NON attacca: la nota precedente continua (il respiro)
    do2/re2  due crome: la seconda cade sul levare, che il firmware swinga

Tutto quello che segue `#` e' commento e dice quale regola e' stata usata.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                          # noqa: E402

TICK_BATTUTA = 384
TICK_MOVIMENTO = 96

#: Il registro del basso, come in `docs/istruzioni/walking.md`: mi1-do3.
BASSO_MIN, BASSO_MAX = 28, 48


#: I tre giri del blues in fa. ⚠️ L'ULTIMA BATTUTA E' F7 e non il turnaround:
#: il pezzo si ferma, non gira.
LINEA_BLUES = '''
# --- primo giro: il TEMA. Quarti quasi tutti, due respiri. -----------------
fa2   mib2  re2   do2    # 1  F7   regola d: per grado dalla fondamentale (fa) alla quinta (do)
sib1  do2   re2   mi2    # 2  Bb7  la quinta do scende di un grado al sib; poi risale, mi e' la sensibile del fa
fa2   mib2  re2   -      # 3  F7   regola d, e il quarto movimento respira: il re dura due movimenti
fa2   sol2  la2   si2    # 4  F7   sale per grado verso il sib del IV grado; si naturale e' l'approccio cromatico da sopra
sib2  lab2  sol2  fa2    # 5  Bb7  regola d: dal sib giu' alla quinta fa
sib2  lab2  sol2  solb2  # 6  Bb7  salto di quinta su per ripartire, poi discesa con solb che approccia il fa da sopra
fa2   -     re2   do2    # 7  F7   il secondo movimento respira: il fa dura due movimenti
fa2   la2   do3   lab2   # 8  F7   arpeggio fa-la-do (passo 3: terza e quinta), lab approccia il sol del ii grado
sol2  fa2   mib2  re2    # 9  Gm7  regola d: dal sol giu' alla quinta re
do2   re2   mib2  mi2    # 10 C7   il re scende al do (un grado), poi salita cromatica al fa
fa2   sol2  la2   lab2   # 11 F7   regola a: sol e' la nota di passaggio fra fa e la; lab approccia il sol da sopra
sol2  fa2   do2   mi2    # 12 Gm7|C7  regola b: sol e do distano una quinta, in mezzo il fa che e' dell'accordo di sol minore

# --- secondo giro: l'ASSOLO. Piu' mosso, piu' respiri, due crome. ----------
fa2   la2   do3   sib2   # 13 F7   arpeggio in su invece della discesa: il giro cambia carattere
sib2  -     lab2  sol2   # 14 Bb7  il sib dura due movimenti, poi scende
fa2   mib2  re2   do2    # 15 F7   regola d
fa2   sol2/lab2  la2  si2  # 16 F7  la croma sul secondo movimento: lab e' cromatica fra sol e la
sib2  do3   -     la2    # 17 Bb7  sale alla nona, tiene, poi scende
sib2  lab2  sol2  solb2  # 18 Bb7  come la 6
fa2   la2   -     do2    # 19 F7   la terza tiene due movimenti
fa2   sol2  la2/sib2  lab2  # 20 F7  croma sul terzo movimento, lab approccia il sol
sol2  -     fa2   mib2   # 21 Gm7  il sol tiene, poi scende
do2   sol2  mib2  mi2    # 22 C7   quinta dell'accordo, poi cromatica al fa
fa2   sol2  la2   lab2   # 23 F7   come la 11
sol2  fa2   do2   mi2    # 24 Gm7|C7  come la 12

# --- terzo giro: il TEMA di nuovo, e la chiusa. ---------------------------
fa2   mib2  re2   do2    # 25 F7
sib1  do2   re2   mi2    # 26 Bb7
fa2   -     re2   do2    # 27 F7   il respiro si sposta sul secondo movimento
fa2   sol2  la2   si2    # 28 F7
sib2  lab2  sol2  fa2    # 29 Bb7
sib2  -     sol2  solb2  # 30 Bb7  respiro sul secondo movimento
fa2   mib2  re2   do2    # 31 F7
fa2   la2   do3   lab2   # 32 F7
sol2  fa2   mib2  re2    # 33 Gm7
do2   re2   mib2  mi2    # 34 C7
fa2   mib2  re2   do2    # 35 F7   discesa piana verso la chiusa
fa2   -     -     -      # 36 F7   la chiusa: una nota sola, tenuta tutta la battuta
'''


def leggi(testo: str = LINEA_BLUES) -> list[tuple[int, int, int]]:
    """Da testo a `(tick, altezza, durata)`, pronti per `MU.linea()`.

    La durata di ogni nota arriva fino all'attacco successivo: un movimento
    che non attacca allunga la nota di prima, ed e' cosi' che si scrive il
    respiro.
    """
    attacchi: list[tuple[int, int]] = []
    battuta = 0
    for riga in testo.splitlines():
        riga = riga.split('#')[0].strip()
        if not riga:
            continue
        gettoni = riga.split()
        if len(gettoni) != 4:
            raise ValueError(f'battuta {battuta + 1}: {len(gettoni)} gettoni '
                             f'invece di 4 -> {gettoni}')
        for movimento, gettone in enumerate(gettoni):
            tick = battuta * TICK_BATTUTA + movimento * TICK_MOVIMENTO
            if gettone == '-':
                if not attacchi:
                    raise ValueError('la prima nota del pezzo non puo\' essere '
                                     'un respiro: non c\'e\' niente da tenere')
                continue
            for i, nome in enumerate(gettone.split('/')):
                y = MU.altezza(nome)
                if not BASSO_MIN <= y <= BASSO_MAX:
                    raise ValueError(f'battuta {battuta + 1} movimento '
                                     f'{movimento + 1}: {nome} = {y}, fuori '
                                     f'dal registro {BASSO_MIN}-{BASSO_MAX}')
                attacchi.append((tick + i * (TICK_MOVIMENTO // 2), y))
        battuta += 1

    fine = battuta * TICK_BATTUTA
    return [(t, y, (attacchi[k + 1][0] if k + 1 < len(attacchi) else fine) - t)
            for k, (t, y) in enumerate(attacchi)]


def battute(testo: str = LINEA_BLUES) -> int:
    """Quante battute porta la linea scritta."""
    return sum(1 for r in testo.splitlines() if r.split('#')[0].strip())


if __name__ == '__main__':
    eventi = leggi()
    print(f'{battute()} battute, {len(eventi)} note')
    import collections
    per_battuta = collections.Counter(t // TICK_BATTUTA for t, _, _ in eventi)
    conti = [per_battuta.get(i, 0) for i in range(battute())]
    import statistics as st
    print(f'note per battuta: media {st.mean(conti):.2f}, '
          f'deviazione {st.pstdev(conti):.2f}')
    diverse = 100 * sum(1 for c in conti if c != 4) / len(conti)
    print(f'battute diverse da quattro: {diverse:.1f}%   (corpus 51,3%)')
    ticks = {t for t, _, _ in eventi}
    muti = sum(1 for b in range(battute()) for m in range(4)
               if b * TICK_BATTUTA + m * TICK_MOVIMENTO not in ticks)
    print(f'movimenti non attaccati: {100 * muti / (4 * battute()):.1f}%   '
          f'(corpus 15,0%)')
