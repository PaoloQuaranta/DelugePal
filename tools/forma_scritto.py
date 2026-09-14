"""Il pezzo di esempio della STRUTTURA lunga, seguendo docs/istruzioni/struttura.md.

Un AABA vero, steso sull'arranger con `MU.forma`: la forma piu' comune del
repertorio (casella 9 di docs/repertori/jazz.md: 103 assoli). Due strumenti --
Rhodes per gli accordi, tromba per la melodia -- e due materiali:

  sezione  materiale                        cosa fa
  A        Cmaj7 Am7 Dm7 G7 + tema alfa     la casa: I-vi-ii-V, melodia media
  B (ponte) Fmaj7 Bb7 Cmaj7 G7 + tema beta  il contrasto: parte sul IV, tema acuto

  mappa:  A  A  B  A     (sezioni da 4 battute, 16 battute in tutto)

L'orecchio deve sentire la FORMA: l'A che TORNA riconoscibile, il ponte che
CONTRASTA e riporta a casa. Suona dall'ARRANGER (open_in_arranger): la timeline
e' la forma, non i lanci di sessione.

Metodo (struttura.md): [CALC] + un ascolto. `MU.forma` fa i conti (dove cade ogni
sezione); l'AI ha deciso la mappa e il materiale. `test_forma` blinda i conti;
qui l'utente ascolta se la forma si sente.
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import parse_file, musica as MU               # noqa: E402
from delugexml import song as S, create as C, arranger as A  # noqa: E402

BARRA = MU.TICK_PER_BATTUTA

#: La mappa: AABA, la forma di 32 battute (qui compressa a 4 per sezione).
MAPPA = 'A A B A'
BATTUTE_SEZIONE = 4

#: Il materiale delle due sezioni.
ACCORDI_A = 'Cmaj7 | Am7 | Dm7 | G7'      # la casa: I-vi-ii-V
MELODIA_A = 'mi4 sol4 mi4 re4 do4 mi4 re4 do4'
ACCORDI_B = 'Fmaj7 | Bb7 | Cmaj7 | G7'    # il ponte: parte sul IV, chiude sul V
MELODIA_B = 'la4 do5 la4 sol4 fa4 la4 sol4 fa4'

REGISTRO = 'do3'


def _svuota_note(clip) -> None:
    """Toglie le note di una clip (la copia nasce con quelle dell'originale)."""
    nr = clip.find('noteRows')
    if nr is not None:
        clip.children.remove(nr)


def _indice(doc, clip) -> int:
    return next(i for i, (_cont, c) in enumerate(S.clips(doc)) if c is clip)


def nuovo() -> tuple[object, dict]:
    """Un doc fresco: due strumenti, ciascuno con la clip A e la clip B.

    Ritorna `(doc, sezioni)`, dove `sezioni` e' la mappa nome -> clip pronta
    per `MU.forma`. Non stende ancora niente sull'arranger.
    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')      # duplicate_clip avvisa sulle variazioni
        doc = parse_file('refs/songs/TEMPL0.XML')
        MU.togli(doc, doc.root.find('instruments').children[0])
        S.set_scale(doc, 'C', 'maggiore')
        S.set_bpm(doc.root, 120)

        # gli strumenti, ciascuno con la clip A
        _instC, cRA = C.add_track(doc, 'refs/synths/Tal Rhodes.XML',
                                  name='CHORDS', folder='SYNTHS',
                                  length=BATTUTE_SEZIONE * BARRA)
        _instM, mTA = C.add_track(doc, 'refs/synths/062 Trumpet.XML',
                                  name='MELODY', folder='SYNTHS',
                                  length=BATTUTE_SEZIONE * BARRA, colour_offset='16')
        MU.scrivi(doc, cRA, MU.armonia(ACCORDI_A, durata='1/1', registro=REGISTRO))
        MU.scrivi(doc, mTA, MU.melodia(MELODIA_A, durata='1/2'))

        # la clip B (il ponte) per gli stessi strumenti: copia, svuota, riscrive
        cRB = S.duplicate_clip(doc, _indice(doc, cRA), section='1', name='CHORDS_B')
        mTB = S.duplicate_clip(doc, _indice(doc, mTA), section='1', name='MELODY_B')
        _svuota_note(cRB)
        _svuota_note(mTB)
        MU.scrivi(doc, cRB, MU.armonia(ACCORDI_B, durata='1/1', registro=REGISTRO))
        MU.scrivi(doc, mTB, MU.melodia(MELODIA_B, durata='1/2'))

    return doc, {'A': [cRA, mTA], 'B': [cRB, mTB]}


def costruisci() -> tuple[object, list]:
    """Il doc con l'AABA steso sull'arranger, pronto da caricare."""
    doc, sezioni = nuovo()
    piano = MU.forma(doc, MAPPA, sezioni, battute=BATTUTE_SEZIONE)
    A.open_in_arranger(doc)
    return doc, piano


if __name__ == '__main__':
    doc, piano = costruisci()
    print(MU.racconta_forma(piano))
    print('extent:', A.extent(doc))
    print('verifica:', MU.verifica(doc) or 'ok')
