"""BASSO che REAGISCE alla forma, seguendo docs/istruzioni/reazione.md.

Rimette in scena il difetto d'origine del progetto e la sua correzione. La stessa
melodia (densita' che alterna rado/fitto), due bassi di fila:

  passata  basso        densita'    cosa fa
  1        UNIFORME     4 4 4 4     4 note ogni battuta, deviazione 0,00 --
                                    «applicato acriticamente», il difetto d'origine
  2        REATTIVO     4 1 4 1     cammina dove la melodia tace, TIENE dove e'
                                    fitta -- complementa, fa spazio

Cosi' la differenza all'orecchio e' SOLO se il basso reagisce. `MU.reazione`
misura: l'uniforme e' `uniforme` (dev 0), il reattivo `complementa` (correlazione
negativa con la melodia). test_reazione e test_reazione_scritto blindano i conti;
qui l'utente ascolta se il basso reattivo «respira» col tema.

Metodo: ritmo, quindi l'ascolto pieno. Vale per la batteria allo stesso modo
(batteria_scritta.py lo fa gia' a mano: la batteria e' rada dove il tema e' fitto).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

B = MU.TICK_PER_BATTUTA

#: La melodia (riferimento): densita' 1 4 1 4 -- alterna rado e fitto.
MELODIA = [
    (0 * B, 'do5', '1/1'),
    (1 * B + 0, 'si4', '1/4'), (1 * B + 96, 'la4', '1/4'),
    (1 * B + 192, 'sol4', '1/4'), (1 * B + 288, 'mi4', '1/4'),
    (2 * B, 'sol4', '1/1'),
    (3 * B + 0, 'la4', '1/4'), (3 * B + 96, 'si4', '1/4'),
    (3 * B + 192, 'do5', '1/4'), (3 * B + 288, 're5', '1/4'),
]

#: Il basso UNIFORME: quattro note ogni battuta, sempre -- il difetto d'origine.
BASSO_UNIFORME = [
    (b * B + i * 96, alt, '1/4')
    for b in range(4)
    for i, alt in enumerate(('do2', 'mi2', 'sol2', 'la2'))
]

#: Il basso REATTIVO: cammina (4) dove la melodia tace, tiene (1) dove e' fitta.
BASSO_REATTIVO = [
    (0 * B + 0, 'do2', '1/4'), (0 * B + 96, 'mi2', '1/4'),
    (0 * B + 192, 'sol2', '1/4'), (0 * B + 288, 'la2', '1/4'),   # b.1: cammina
    (1 * B, 'do2', '1/1'),                                       # b.2: TIENE
    (2 * B + 0, 'sol2', '1/4'), (2 * B + 96, 'la2', '1/4'),
    (2 * B + 192, 'si2', '1/4'), (2 * B + 288, 'do3', '1/4'),    # b.3: cammina
    (3 * B, 'sol2', '1/1'),                                      # b.4: TIENE
]

#: Passata: 4 battute di tema + 2 vuote, cosi' l'orecchio stacca.
_PASSATA = 6 * B


def melodia() -> dict:
    return MU.linea(MELODIA, velocity=84)


def basso_uniforme() -> dict:
    return MU.linea(BASSO_UNIFORME, articolazione='staccato', velocity=80)


def basso_reattivo() -> dict:
    return MU.linea(BASSO_REATTIVO, articolazione='staccato', velocity=80)


def _sposta(voce: dict, da: int) -> dict:
    from delugexml.notes import Note                          # noqa: PLC0415
    return {y: [Note(pos=n.pos + da, length=n.length, velocity=n.velocity)
                for n in note] for y, note in voce.items()}


def voce_alta() -> dict:
    """Il tema, in tutte e due le passate."""
    fuse: dict = {}
    for parte in (melodia(), _sposta(melodia(), _PASSATA)):
        for y, note in parte.items():
            fuse.setdefault(y, []).extend(note)
    return fuse


def voce_bassa() -> dict:
    """Il basso: uniforme nella passata 1, reattivo nella 2."""
    fuse: dict = {}
    for parte in (basso_uniforme(), _sposta(basso_reattivo(), _PASSATA)):
        for y, note in parte.items():
            fuse.setdefault(y, []).extend(note)
    return fuse


def costruisci() -> tuple[object, dict]:
    """Il doc con le due passate, pronto da caricare. Ritorna `(doc, verdetti)`."""
    import warnings                                           # noqa: PLC0415
    from delugexml import parse_file, song as S              # noqa: PLC0415
    from delugexml import create as C, arranger as A         # noqa: PLC0415
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file('refs/songs/TEMPL0.XML')
        MU.togli(doc, doc.root.find('instruments').children[0])
        S.set_scale(doc, 'C', 'maggiore')
        S.set_bpm(doc.root, 120)
        _iM, cM = C.add_track(doc, 'refs/synths/062 Trumpet.XML', name='TEMA',
                              folder='SYNTHS', length=2 * _PASSATA)
        _iB, cB = C.add_track(doc, 'refs/synths/Square Saw Bass.XML', name='BASSO',
                              folder='SYNTHS', length=2 * _PASSATA, colour_offset='16')
        MU.scrivi(doc, cM, voce_alta())
        MU.scrivi(doc, cB, voce_bassa())
        A.place(doc, _iM, cM, 0, 2 * _PASSATA, )
        A.place(doc, _iB, cB, 0, 2 * _PASSATA)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    verdetti = {
        'uniforme': MU.reazione(basso_uniforme(), melodia()).verdetto,
        'reattivo': MU.reazione(basso_reattivo(), melodia()).verdetto,
    }
    return doc, verdetti


if __name__ == '__main__':
    print('UNIFORME'); print(MU.racconta_reazione(basso_uniforme(), melodia(),
                                                   nomi=('basso', 'tema')))
    print(); print('REATTIVO'); print(MU.racconta_reazione(basso_reattivo(), melodia(),
                                                            nomi=('basso', 'tema')))
