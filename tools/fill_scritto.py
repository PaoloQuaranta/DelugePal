"""Il FILL, seguendo docs/istruzioni/fill.md.

Completa la lacuna dichiarata di `batteria_scritta.py`: le battute 12 e 24 del
blues erano marcate «(fill)» e lasciate come tempo, perche' il fill era «una
decisione arbitraria messa sul turnaround». Qui il fill e' scritto con la firma
MISURATA (casella 9 di docs/repertori/jazz.md): il ride si ferma, arrivano i tom,
la densita' sale di poco, la voce non si alza.

  DOVE va: al GIUNTO -- l'ultima battuta di una sezione, sul turnaround. Lo dice
    la FORMA (priorita' 2), non il corpus: «dove va un fill non lo dice il
    corpus» (casella 9). Si posa con la clip bianca `MU.variazione`.
  QUANTO dura: una battuta (`[MIS]` mediana 0,93).
  COSA cambia: ride 20% -> 3%, tom 10% -> 29%; ~1,2x piu' fitto, non il doppio;
    stessa velocity o meno. La firma NON e' la densita', e' il cambio di
    strumento (`[MIS]`, 2 batteristi -- vedi la cautela nella casella 9).

Metodo: ritmo, quindi l'ascolto pieno. `MU.controlla_fill` fa i conti sulla
firma (il corpus «prende gli errori»); l'orecchio dice se il fill «annuncia» la
sezione nuova senza strappare. test_controlla_fill e test_fill_scritto blindano
i conti.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: Un BEAT di riferimento (dal vocabolario di batteria_scritta.py): il groove su
#: cui il fill si misura. ride costante, charleston a pedale, rullante sui
#: levare, cassa su 1 e 3 (il feathering).
BEAT = {
    'ride': 'x...x.x.x...x.x.',
    'charleston a pedale': '....x.......x...',
    'rullante': '.......x....x...',
    'cassa': 'x.......x.......',
}

#: Il FILL del turnaround (le battute 12 e 24): il ride si ferma dopo il primo
#: movimento, i tom scendono verso la sezione nuova, il rullante li lega, la
#: cassa tiene il basso. Un filo piu' fitto del beat, non il doppio.
FILL = {
    'ride': 'x...............',        # solo l'attacco, poi tace: il ride si ferma
    'rullante': 'x.x...x.x.......',
    'tom-medio': '....x.x.....x...',
    'tom-basso': '........x.x.x.x.',   # scende verso il downbeat della sezione dopo
    'cassa': 'x.......x.......',
}


def beat_note() -> dict[str, list]:
    return {ruolo: MU.passi(p) for ruolo, p in BEAT.items()}


def fill_note() -> dict[str, list]:
    return {ruolo: MU.passi(p) for ruolo, p in FILL.items()}


def controllo() -> MU.Fill:
    """Il controllo del fill contro la firma misurata (deve essere pulito)."""
    return MU.controlla_fill(beat_note(), fill_note())


# --- Il pezzo per l'ascolto (FILL01) --------------------------------------
#
# ⚠️ Kit di RIPIEGO: il TR-808 di refs/songs/DRUMS1_4.XML e' l'unico a portare i
# tom (TOML/TOMM/TOMH). E' elettronico e NON ha il ride, quindi il segnatempo e'
# il charleston (HATC). Si sente la STRUTTURA del fill -- segnatempo che si ferma,
# tom che arrivano al giunto -- non il timbro jazz. Un kit acustico coi tom resta
# il modo di sentirlo nel suo suono.

BARRA = MU.TICK_PER_BATTUTA

#: Il groove e il fill mappati sui drum del kit 808 (niente ride: il charleston
#: fa il segnatempo).
GROOVE_808 = {'HATC': 'x.x.x.x.x.x.x.x.', 'SNARE': '....x.......x...',
              'KICK': 'x.......x.......'}
FILL_808 = {'HATC': 'x...............', 'SNARE': 'x.x...x.x.......',
            'TOMM': '....x.x.....x...', 'TOML': '........x.x.x.x.',
            'KICK': 'x.......x.......'}


def costruisci() -> tuple[object, list]:
    """Monta FILL01: 8 battute, due sezioni, un fill al giunto (batt. 4) e alla
    chiusa (batt. 8), posati con la clip bianca. Ritorna `(doc, [clip fill])`."""
    import warnings                                           # noqa: PLC0415
    from delugexml import parse_file, song as S              # noqa: PLC0415
    from delugexml import create as C, arranger as A         # noqa: PLC0415
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file('refs/songs/DRUMS1_4.XML')
        for inst in list(doc.root.find('instruments').children):
            if inst.tag == 'sound':                          # via il synth, tengo il kit
                MU.togli(doc, inst)
        S.set_scale(doc, 'C', 'maggiore')
        S.set_bpm(doc.root, 120)

        kit = doc.root.find('instruments').children[0]
        kit_clip = S.clips(doc)[0][1]
        for row in list(kit_clip.find('noteRows').children):
            MU.togli(doc, row)                               # svuota il groove esistente
        for drum, patt in GROOVE_808.items():
            MU.scrivi(doc, kit_clip, MU.passi(patt), dove=drum)

        iR, cR = C.add_track(doc, 'refs/synths/Tal Rhodes.XML', name='CHORDS',
                             folder='SYNTHS', length=4 * BARRA)
        MU.scrivi(doc, cR, MU.armonia('Cmaj7 | Am7 | Dm7 | G7', durata='1/1',
                                      registro='do3'))
        idx = next(i for i, (_c, c) in enumerate(S.clips(doc)) if c is cR)
        cRB = S.duplicate_clip(doc, idx, section='2', name='CH_B')
        nr = cRB.find('noteRows')
        if nr is not None:
            cRB.children.remove(nr)
        MU.scrivi(doc, cRB, MU.armonia('Fmaj7 | Bb7 | Em7 | A7', durata='1/1',
                                       registro='do3'))

        A.place(doc, iR, cR, 0, 4 * BARRA)
        A.place(doc, iR, cRB, 4 * BARRA, 4 * BARRA)
        A.place(doc, kit, kit_clip, 0, 3 * BARRA)
        fills = []
        for pos in (3 * BARRA, 7 * BARRA):                   # fill al giunto e alla chiusa
            f = MU.variazione(doc, kit_clip, pos)
            for row in list(f.find('noteRows').children):
                MU.togli(doc, row)
            for drum, patt in FILL_808.items():
                MU.scrivi(doc, f, MU.passi(patt), dove=drum)
            fills.append(f)
        A.place(doc, kit, kit_clip, 4 * BARRA, 3 * BARRA)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc, fills


if __name__ == '__main__':
    print(MU.racconta_fill(beat_note(), fill_note()))
