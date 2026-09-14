"""Il pezzo di CONFRONTO del contrappunto, seguendo docs/istruzioni/contrappunto.md.

Lo STESSO tema, con due seconde voci di fila, sullo stesso materiale:

  passata  battute  seconda voce      cosa si sente
  1        1-2      DIPENDENTE        una voce sola, raddoppiata: le due parti
                                      salgono e scendono insieme (terze), stesso
                                      ritmo, stesso picco
  2        4-5      INDIPENDENTE      DUE voci: moto contrario, due note tenute
                                      (obliquo) mentre il tema passa, ritmo
                                      sfasato, picchi in momenti diversi
  (la battuta 3 e' vuota: stacca una passata dall'altra)

Cosi' la differenza all'orecchio e' SOLO il grado di indipendenza della seconda
voce. Il tema e' identico; cambia solo cosa gli si mette sotto.

Metodo (contrappunto.md): [CALC] + un ascolto. MU.contrappunto misura i due
rapporti -- la dipendente e' tutta in moto parallelo/diretto e attacca sempre
insieme al tema; la indipendente ha moto contrario e obliquo e attacca meno
spesso insieme. test_contrappunto e test_contrappunto_scritto blindano i conti;
qui l'utente ascolta se "due voci" e' quello che sente davvero.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: Il TEMA (voce alta): sale nella prima battuta, torna a casa nella seconda.
#: Otto quarti, due battute. E' lo stesso per tutte e due le passate.
TEMA = 'mi4 fa4 sol4 la4 sol4 mi4 re4 do4'

#: La seconda voce DIPENDENTE: una terza sotto, nota per nota, stesso ritmo.
#: Sale e scende col tema -- l'orecchio sente una voce raddoppiata, non due.
DIPENDENTE = 'do4 re4 mi4 fa4 mi4 do4 si3 la3'

#: La seconda voce INDIPENDENTE: un basso che va in moto CONTRARIO al tema, con
#: due note TENUTE (obliquo) mentre il tema si muove, e un ritmo diverso dal suo
#: -- (tick, altezza, durata). Chiude in ottava per moto contrario.
INDIPENDENTE = [
    (0,   'do3',  '1/2'),   # tiene t0..t192: obliquo mentre il tema sale a fa4
    (192, 'sol2', '1/4'),
    (288, 'fa2',  '1/4'),
    (384, 'sol2', '1/2'),   # tiene t384..t480: obliquo mentre il tema scende a mi4
    (576, 'si2',  '1/4'),
    (672, 'do3',  '1/4'),   # chiude do3 sotto do4: ottava, per moto contrario
]

#: Due battute di tema + una vuota, cosi' l'orecchio stacca una passata dall'altra.
_PASSATA = 3 * MU.durata_in_tick('1/1')


def tema() -> dict[int, list]:
    """Il tema, una passata (per il test e per costruire le voci alte)."""
    return MU.melodia(TEMA, durata='1/4', velocity=84)


def dipendente() -> dict[int, list]:
    """La seconda voce dipendente (terze parallele), una passata."""
    return MU.melodia(DIPENDENTE, durata='1/4', velocity=76)


def indipendente() -> dict[int, list]:
    """La seconda voce indipendente (moto contrario, obliquo), una passata."""
    return MU.linea(INDIPENDENTE, velocity=76)


def _sposta(voce: dict[int, list], da: int) -> dict[int, list]:
    """La stessa voce spostata di `da` tick, per metterla nella passata 2."""
    from delugexml.notes import Note                          # noqa: PLC0415
    return {y: [Note(pos=n.pos + da, length=n.length, velocity=n.velocity)
                for n in note] for y, note in voce.items()}


def voce_alta() -> dict[int, list]:
    """Il tema, suonato in tutte e due le passate (dipendente, poi indipendente)."""
    fuse: dict[int, list] = {}
    for parte in (tema(), _sposta(tema(), _PASSATA)):
        for y, note in parte.items():
            fuse.setdefault(y, []).extend(note)
    return fuse


def voce_bassa() -> dict[int, list]:
    """La seconda voce: dipendente nella passata 1, indipendente nella 2."""
    fuse: dict[int, list] = {}
    for parte in (dipendente(), _sposta(indipendente(), _PASSATA)):
        for y, note in parte.items():
            fuse.setdefault(y, []).extend(note)
    return fuse


if __name__ == '__main__':
    t = tema()
    for nome, voce in (('dipendente', dipendente()), ('indipendente', indipendente())):
        an = MU.contrappunto(t, voce)
        print(f'{nome}: moti {an.moti}, simultaneita {an.simultaneita:.0%}, '
              f'parallele {an.paralleli}')
