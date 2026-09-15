"""INTERAZIONE a livello di evento, seguendo docs/istruzioni/interazione.md.

Il passo oltre la reazione (densita' per battuta): qui conta la COLLOCAZIONE
dentro la battuta. Un tema che CHIAMA (una frase sui movimenti 1-2, poi un buco
sul 3-4), e un Rhodes che risponde -- due passate:

  passata 1  PESTA      il Rhodes stacca sul movimento 1, SOPRA il tema
  passata 2  RISPONDE   il Rhodes stacca sul movimento 3, NEL BUCO del tema

⚠️ Le due passate hanno la STESSA densita' (uno stab per battuta): cambia solo
DOVE cade. Percio' `MU.reazione` (densita' per battuta) e' muto -- le vede
identiche -- mentre `MU.interazione` (presenza per movimento) dice `insieme` alla
prima e `risponde` alla seconda. E' la differenza fra i due, resa udibile: nella
prima le due voci si accavallano, nella seconda si parlano.

Metodo: ritmo, quindi l'ascolto pieno. `MU.interazione` fa i conti (il corpus
prende gli errori, come `reazione`); l'orecchio dice se e' una conversazione.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402
from delugexml.notes import Note                             # noqa: E402

B = MU.TICK_PER_BATTUTA
MOV = MU.TICK_PER_MOVIMENTO

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
PRESET_TEMA = RADICE / 'refs' / 'synths' / '062 Trumpet.XML'
PRESET_RHODES = RADICE / 'refs' / 'synths' / 'Tal Rhodes.XML'

BPM = 120
PROGRESSIONE = ['Dm7', 'G7', 'Cmaj7', 'Cmaj7']

#: Il tema CHIAMA: un accento sul movimento 1, una nota sul 2, poi TACE sul 3-4.
#: E' il buco del 3-4 che aspetta una risposta.
TEMA = [
    ('la4', 'do5'),    # b1 Dm7
    ('si4', 're5'),    # b2 G7
    ('do5', 'mi5'),    # b3 Cmaj7
    ('sol4', 'mi4'),   # b4 Cmaj7
]
BATTUTE = 4
PASSATA = (BATTUTE + 2) * B                    # 4 battute + 2 vuote


def tema_eventi(offset: int) -> list:
    fuori = []
    for bar, (n1, n2) in enumerate(TEMA):
        fuori.append((offset + bar * B + 0 * MOV, n1, '1/4'))   # accento (movimento 1)
        fuori.append((offset + bar * B + 1 * MOV, n2, '1/4'))   # movimento 2
    return fuori


def tema(offset: int = 0) -> dict:
    voce = MU.linea(tema_eventi(offset), articolazione='staccato', velocity=84)
    # l'accento del movimento 1 di ogni battuta
    for note in voce.values():
        for n in note:
            if (n.pos - offset) % B == 0:
                n.velocity = 110
    return voce


def rhodes(offset: int, movimento: int) -> dict:
    """Uno stab d'accordo per battuta, sul `movimento` scelto (0 = beat 1, 2 = beat 3)."""
    voce: dict = {}
    for bar, sigla in enumerate(PROGRESSIONE):
        pos = offset + bar * B + movimento * MOV
        for y in MU.voci(sigla, voicing='shell', registro='do3'):
            voce.setdefault(y, []).append(Note(pos=pos, length=48, velocity=72))
    return voce


def rhodes_pesta(offset: int = 0) -> dict:
    return rhodes(offset, 0)                    # sul movimento 1, SOPRA il tema


def rhodes_risponde(offset: int = 0) -> dict:
    return rhodes(offset, 2)                    # sul movimento 3, NEL BUCO


def _fondi(*parti: dict) -> dict:
    fuse: dict = {}
    for parte in parti:
        for y, note in parte.items():
            fuse.setdefault(y, []).extend(note)
    return fuse


def costruisci() -> tuple[object, dict]:
    """Il pezzo dell'ascolto. Ritorna `(doc, verdetti)`. Solleva FileNotFoundError
    se manca una fixture."""
    import warnings                                           # noqa: PLC0415
    from delugexml import parse_file, song as S              # noqa: PLC0415
    from delugexml import create as C, arranger as A         # noqa: PLC0415
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(str(TEMPL))
        S.set_bpm(doc.root, BPM)
        S.set_scale(doc, 'C', 'maggiore')
        for strumento in list(S.instruments(doc)):
            MU.togli(doc, strumento)

        iT, cT = C.add_track(doc, str(PRESET_TEMA), name='TEMA', folder='SYNTHS',
                             length=2 * PASSATA, playing=True)
        iR, cR = C.add_track(doc, str(PRESET_RHODES), name='RHODES', folder='SYNTHS',
                             length=2 * PASSATA, colour_offset='16', playing=True)
        MU.scrivi(doc, cT, _fondi(tema(0), tema(PASSATA)))
        MU.scrivi(doc, cR, _fondi(rhodes_pesta(0), rhodes_risponde(PASSATA)))

        A.place(doc, iT, cT, 0, 2 * PASSATA)
        A.place(doc, iR, cR, 0, 2 * PASSATA)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    verdetti = {
        'pesta': MU.interazione(rhodes_pesta(), tema()).verdetto,
        'risponde': MU.interazione(rhodes_risponde(), tema()).verdetto,
    }
    return doc, verdetti


if __name__ == '__main__':
    print('PESTA (Rhodes sul movimento 1, sopra il tema)')
    print(MU.racconta_interazione(rhodes_pesta(), tema(), nomi=('rhodes', 'tema')))
    print('\nRISPONDE (Rhodes sul movimento 3, nel buco)')
    print(MU.racconta_interazione(rhodes_risponde(), tema(), nomi=('rhodes', 'tema')))
    print('\n--- e la reazione (densita per battuta) le vede uguali? ---')
    print('pesta   :', MU.reazione(rhodes_pesta(), tema()).verdetto,
          '| risponde:', MU.reazione(rhodes_risponde(), tema()).verdetto)
