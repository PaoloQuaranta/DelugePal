"""Il pezzo delle TRANSIZIONI, seguendo docs/istruzioni/transizioni.md.

Lo stesso AABA, con due GIUNTI articolati dalla clip "bianca" (MU.variazione,
sopra arranger.place_unique). L'A d'apertura resta piana; le variazioni vivono
solo sulla timeline, senza toccare l'originale:

  giunto        dove       modo        cosa fa
  A2 -> B       fine A2    rampa/build il pickup: la melodia sale nell'ultima
                                       battuta e "consegna" il ponte
  ritorno       A3         morbido     il turnaround: l'ultimo A stringe il ritmo
                                       armonico (Dm7 G7 in una battuta) e RISOLVE
                                       su Cmaj7 -- la cadenza che chiude

  arrangiamento:  A1(piana)  A2(pickup)  B(piana)  A3(turnaround)

⚠️ Solo A2-melodia e A3 sono variazioni (clip bianche); A1, B e A2-accordi sono
le clip di sezione piane. La variazione tocca solo la voce che cambia. Il
turnaround e' anche l'accelerazione del ritmo armonico verso la cadenza
(ritmo-armonico.md): la stessa mossa, vista dal giunto.

Metodo: [CALC] + un ascolto. `MU.variazione` da' la clip bianca (indipendente);
il materiale del giunto lo scrive l'AI. test_variazione e test_transizioni_scritto
blindano i conti; qui l'utente ascolta se i giunti "cuciono". Si suona dall'arranger.
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import parse_file, musica as MU               # noqa: E402
from delugexml import song as S, create as C, arranger as A  # noqa: E402

BARRA = MU.TICK_PER_BATTUTA
REGISTRO = 'do3'

#: Le sezioni piane.
A_CH = 'Cmaj7 | Am7 | Dm7 | G7'
A_ME = 'mi4 sol4 la4 sol4 mi4 re4 do4 re4'
B_CH = 'Fmaj7 | Bb7 | Em7 | A7'
B_ME = 'la4 do5 si4 la4 sol4 la4 sol4 mi4'


def _fondi(*parti: dict) -> dict:
    out: dict = {}
    for p in parti:
        for y, ns in p.items():
            out.setdefault(y, []).extend(ns)
    return out


def a2_melodia_pickup() -> dict:
    """A2 con il PICKUP nel giunto verso il ponte: 3 battute come A, poi
    l'ultima battuta sale (sol la si do5) e consegna il ponte."""
    return _fondi(
        MU.melodia('mi4 sol4 la4 sol4 mi4 re4', durata='1/2', da=0),   # bar 1-3
        MU.melodia('sol4 la4 si4 do5', durata='1/4', da=3 * BARRA),    # bar 4: sale
    )


def a3_accordi_turnaround() -> dict:
    """A3 col TURNAROUND: bar 1-2 come A, bar 3 stringe (Dm7 G7 a minima),
    bar 4 RISOLVE su Cmaj7 -- la cadenza finale."""
    return _fondi(
        MU.armonia('Cmaj7 | Am7', durata='1/1', da=0, registro=REGISTRO),
        MU.armonia('Dm7 | G7', durata='1/2', da=2 * BARRA, registro=REGISTRO),
        MU.armonia('Cmaj7', durata='1/1', da=3 * BARRA, registro=REGISTRO),
    )


def a3_melodia_cadenza() -> dict:
    """La melodia dell'ultimo A: si fa piu' fitta sul turnaround e si posa sul do."""
    return _fondi(
        MU.melodia('mi4 sol4 la4 sol4', durata='1/2', da=0),           # bar 1-2
        MU.melodia('fa4 mi4 re4 mi4', durata='1/4', da=2 * BARRA),     # bar 3: fitto
        MU.melodia('do4', durata='1/1', da=3 * BARRA),                 # bar 4: risolve
    )


def _idx(doc, clip) -> int:
    return next(i for i, (_c, c) in enumerate(S.clips(doc)) if c is clip)


def _svuota(clip) -> None:
    nr = clip.find('noteRows')
    if nr is not None:
        clip.children.remove(nr)


def costruisci() -> tuple[object, dict]:
    """Il doc con l'AABA e i due giunti, pronto da caricare. Ritorna
    `(doc, clip_bianche)` per la verifica."""
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file('refs/songs/TEMPL0.XML')
        MU.togli(doc, doc.root.find('instruments').children[0])
        S.set_scale(doc, 'C', 'maggiore')
        S.set_bpm(doc.root, 120)

        iC, cA = C.add_track(doc, 'refs/synths/Tal Rhodes.XML',
                             name='CHORDS', folder='SYNTHS', length=4 * BARRA)
        iM, mA = C.add_track(doc, 'refs/synths/062 Trumpet.XML',
                             name='MELODY', folder='SYNTHS',
                             length=4 * BARRA, colour_offset='16')
        MU.scrivi(doc, cA, MU.armonia(A_CH, durata='1/1', registro=REGISTRO))
        MU.scrivi(doc, mA, MU.melodia(A_ME, durata='1/2'))

        cB = S.duplicate_clip(doc, _idx(doc, cA), section='1', name='CH_B')
        mB = S.duplicate_clip(doc, _idx(doc, mA), section='1', name='ME_B')
        _svuota(cB)
        _svuota(mB)
        MU.scrivi(doc, cB, MU.armonia(B_CH, durata='1/1', registro=REGISTRO))
        MU.scrivi(doc, mB, MU.melodia(B_ME, durata='1/2'))

        # A1 (piana), A2 (accordi piani + melodia col pickup), B (piana)
        A.place(doc, iC, cA, 0, 4 * BARRA)
        A.place(doc, iM, mA, 0, 4 * BARRA)
        A.place(doc, iC, cA, 4 * BARRA, 4 * BARRA)
        v_pickup = MU.variazione(doc, mA, 4 * BARRA)
        _svuota(v_pickup)
        MU.scrivi(doc, v_pickup, a2_melodia_pickup())
        A.place(doc, iC, cB, 8 * BARRA, 4 * BARRA)
        A.place(doc, iM, mB, 8 * BARRA, 4 * BARRA)

        # A3: il ritorno col turnaround, tutte e due le voci variate (clip bianche)
        v_ch = MU.variazione(doc, cA, 12 * BARRA)
        _svuota(v_ch)
        MU.scrivi(doc, v_ch, a3_accordi_turnaround())
        v_me = MU.variazione(doc, mA, 12 * BARRA)
        _svuota(v_me)
        MU.scrivi(doc, v_me, a3_melodia_cadenza())

        A.fit_view(doc)
        A.open_in_arranger(doc)

    return doc, {'pickup': v_pickup, 'turnaround_ch': v_ch, 'turnaround_me': v_me}


if __name__ == '__main__':
    doc, bianche = costruisci()
    from delugexml import arranger as A2                      # noqa: E402
    print('clip bianche (arranger-only):',
          {k: A2.is_white(v) for k, v in bianche.items()})
    print('extent:', A2.extent(doc))
    print('verifica:', MU.verifica(doc) or 'ok', ' arranger:', A2.check(doc) or 'ok')
