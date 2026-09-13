"""Il pezzo di CONFRONTO del comping, seguendo docs/istruzioni/comping.md.

Lo STESSO ii-V-I -- Dm7 | G7 | Cmaj7 -- comped in due modi di fila, sullo stesso
materiale: uno RADO E ANTICIPATO (con spazio, e la x sull'ultima croma che spinge
sul cambio), uno FITTO (colpi su ogni movimento e i levare). Cosi' la differenza
all'orecchio e' SOLO il ritmo del comping. Rootless (Bill Evans) col basso sotto;
niente melodia, cosi' lo SPAZIO del rado si sente.

Metodo (comping.md, 13 settembre 2026): [CALC] + un ascolto. Le meccaniche sono
blindate da test_comping; qui l'utente ascolta il FEEL -- lo spazio, la spinta.

  passata  battute  comping                cosa si sente
  1        1-3      rado, anticipato       lo spazio, e la spinta sul cambio
  2        5-7      fitto                  il martellato, senza aria
  (le battute 4, 8 sono vuote: staccano una passata dall'altra)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: Lo stesso ii-V-I per tutte e due le passate.
PROGRESSIONE = 'Dm7 | G7 | Cmaj7'

#: RADO E ANTICIPATO: colpi su 1 e sul levare del 2, e la x sull'ottava croma
#: ANTICIPA il battere della battuta dopo (la spinta). L'ultima battuta non
#: anticipa: si posa.
RITMO_RADO = ['x..x...x', 'x..x...x', 'x..x....']

#: FITTO: un colpo su ogni movimento e i levare -- il martellato senza aria.
RITMO_FITTO = ['x.x.x.x.', 'x.x.x.x.', 'x.x.x.x.']

#: Ogni passata sono 3 battute + 1 vuota = 4 battute, cosi' l'orecchio stacca
#: una passata dall'altra. Otto battute in tutto.
_PASSATA = 4 * MU.durata_in_tick('1/1')
REGISTRO = 'do3'

#: Il basso sulle fondamentali (re-sol-do), una passata alla volta, con la
#: quarta battuta vuota. Da' la fondamentale al rootless.
BASSO = ('re2 sol2 do2 . ' * 2).strip()


def comping() -> dict[int, list]:
    """Le due passate, rado e fitto, in fila nel tempo."""
    fuse: dict[int, list] = {}
    for i, ritmo in enumerate((RITMO_RADO, RITMO_FITTO)):
        parte = MU.comping(PROGRESSIONE, ritmo, voicing='senza-fondamentale',
                           registro=REGISTRO, da=i * _PASSATA, velocity=76)
        for y, note in parte.items():
            fuse.setdefault(y, []).extend(note)
    return fuse


def basso() -> dict[int, list]:
    """Il basso sulle fondamentali, per tutte e due le passate."""
    return MU.melodia(BASSO, durata='1/1', articolazione='staccato', velocity=80)


if __name__ == '__main__':
    for nome, ritmo in (('rado', RITMO_RADO), ('fitto', RITMO_FITTO)):
        colpi = sum(r.count('x') for r in ritmo)
        print(f'{nome}: {colpi} colpi su 24 crome')
