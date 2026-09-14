"""GROOVE TEMPLATE: il tocco di un batterista vero, seguendo
docs/istruzioni/groove-template.md.

Isola COSA aggiunge un groove template. Lo STESSO pattern di batteria -- che gia'
reagisce alla forma (rado dove il tema e' fitto, come reazione.md) -- suonato due
passate di fila:

  passata 1  PIATTO   velocity uniforme 80, sulla griglia -- un metronomo
  passata 2  TOCCO    applica_groove(drummer1/session1/49): la velocity e il
                      microtiming di un batterista vero, posati sullo stesso pattern

La differenza all'orecchio e' SOLO il tocco: la cassa sfiorata (vel ~42 contro
80), i fantasmi del rullante (~24), il piede del charleston che PESA e ANTICIPA
(~93, scarto negativo), il ride che respira. Il pattern e' identico nelle due
passate, quindi cambia solo la mano che lo suona.

⚠️ LO SWING E' DI SONG, non del template. `S.set_swing()` vale per tutte e due le
passate; il profilo porta il SOLO residuo (di quanto ogni voce arriva prima o
dopo il resto del kit). Se il template portasse anche lo swing, sarebbe doppio.

⚠️ IL TEMPO E' 125 BPM perche' e' quello a cui il template e' misurato. Lo scarto
che `applica_groove()` scrive e' in TICK, cioe' una frazione di movimento:
scriverlo al tempo di misura ne conserva i millisecondi. A un tempo diverso lo
stesso scarto si allunga o si accorcia (casella 6 di docs/repertori/jazz.md).

⚠️ LA DINAMICA E' RIMAPPATA SUL KIT. Il template porta i fantasmi del rullante a
velocity ~24 e la cassa sfiorata a ~42: sul KIT009 (un RX-5 elettronico) a quel
volume SPARISCONO all'udito -- la parte suona come se avesse note in meno
(verdetto dell'utente sulla prima stesura, 14 settembre 2026: «la versione col
tocco lascia fuori troppe note, le cancella»). `MU.rimappa_dinamica()` alza il
FONDO fino a `PAVIMENTO`, dove il kit da' voce, tenendo i RAPPORTI di kit
(fantasma < comp < ride < piede). Non e' ritoccare la misura: e' adattarla allo
strumento -- una decisione dichiarata, e il rapporto lo dice.

Metodo: ritmo, quindi l'ascolto pieno. `applica_groove()` fa i conti (regola 4:
il rapporto dice `toccate`, `senza_appoggio`, `collisioni`); l'orecchio dice se il
tocco fa la differenza fra una macchina e una persona. ⚠️ La POSIZIONE e' la
parte piu' sottile -- §6-terdecies: sul giro intero a tempo pieno si sente
soprattutto la velocity, il residuo di posizione emerge al tempo lento.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402
from delugexml import groove as GR                            # noqa: E402

B = MU.TICK_PER_BATTUTA

#: Il dataset e le fixture non sono versionati (vedi genera_jazz.py): il test
#: salta se mancano, come quelli di GR e WJ.
BASE = RADICE / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
KIT = RADICE / 'refs' / 'kits' / 'KIT009.XML'
PRESET_TEMA = RADICE / 'refs' / 'synths' / '062 Trumpet.XML'

#: L'esecuzione NOMINATA. jazz 4/4, 125 BPM, 60 battute. Su di lei il ride e'
#: davvero il ride (281 colpi sui passi giusti): la mappa GM non inganna -- ma
#: il principio resta che la voce si sceglie dai colpi, non dal nome.
ESECUZIONE = 'drummer1/session1/49'
BPM = 125
SWING = 60                                    # crome swingate, di SONG

#: La velocity minima che il KIT009 da' voce. Il template scende fino a ~24
#: (fantasmi), che su questo kit sparisce: si rimappa il fondo qui. Da tarare a
#: orecchio -- e' ritmo, quindi l'ascolto pieno.
PAVIMENTO = 55

#: La voce nel PROFILO (mappa GM) -> il drum nel KIT009 (un RX-5). Le quattro
#: voci del jazz, la stessa mappa collaudata in genera_jazz.py.
VOCI = {'ride': 'RIDE', 'charleston a pedale': 'HATC',
        'rullante': 'SNARE', 'kick': 'KICK'}

#: Le due voci del segnatempo: COSTANTI su tutte le battute.
#:   ride: lo spang-a-lang, 0 4 6 8 12 14 -- non si buca mai ([LIB] Riley p.8)
#:   charleston a pedale: il piede su 2 e 4 (passi 4 e 12)
RIDE = 'x...x.x.x...x.x.'
PEDALE = '....x.......x...'

#: Rullante e cassa REAGISCONO. Il tema alterna una nota tenuta (battute 1 e 3,
#: rado) e una corsa di crome (battute 2 e 4, fitto): la batteria comps dove il
#: tema tace, fa spazio dove corre. Solo passi che il batterista suona davvero,
#: cosi' niente finisce in `senza_appoggio`.
SNARE = ['..x......x......',   # b1 (tema rado): due fantasmi, si comps
         '................',   # b2 (tema fitto): spazio
         '..x......x....x.',   # b3 (tema rado): comps, un colpo in piu'
         '.........x......']   # b4 (tema fitto): un solo fantasma
KICK = ['......x.......x.',    # b1: feathering leggero
        '......x.........',    # b2
        '......x.......x.',    # b3
        '......x.........']    # b4
BATTUTE = 4

#: Una passata: 4 battute di groove + 2 vuote, cosi' l'orecchio stacca prima
#: di risentire lo stesso pattern con l'altra mano.
PASSATA = (BATTUTE + 2) * B


def _pattern_per_voce() -> dict[str, list[str]]:
    """{voce GM: [pattern per battuta]}. Ride e pedale costanti, snare e kick per battuta."""
    return {'ride': [RIDE] * BATTUTE, 'charleston a pedale': [PEDALE] * BATTUTE,
            'rullante': SNARE, 'kick': KICK}


def note_voce(voce: str, offset: int) -> list:
    """Le note di una voce sulle 4 battute, spostate di `offset` tick. Tutte a
    velocity 80: la passata piatta le lascia cosi', quella col tocco le riscrive."""
    per_voce = _pattern_per_voce()
    note = []
    for bar, patt in enumerate(per_voce[voce]):
        note.extend(MU.passi(patt, da=offset + bar * B, velocity=80))
    return note


def profilo():
    """Il groove template dell'esecuzione nominata. Puo' sollevare
    FileNotFoundError se il dataset non c'e'."""
    return GR.profilo(BASE, ESECUZIONE)


def voci_col_tocco(prof, offset: int = 0) -> tuple[dict[str, list], dict]:
    """Le quattro voci col tocco applicato E rimappato sul range udibile del
    kit. Ritorna `(tocchi, rapporti)`: `tocchi[voce]` sono le Note (mutate),
    `rapporti` porta un report per voce (`applica_groove`) piu' `'rimappa'`
    (`rimappa_dinamica`), tutti da leggere (regola 4)."""
    tocchi = {v: note_voce(v, offset) for v in VOCI}
    rap = {v: MU.applica_groove(tocchi[v], prof, dove=v) for v in VOCI}
    # ⚠️ una sola rimappa su TUTTE le voci: la dinamica che conta e' quella di kit
    rap['rimappa'] = MU.rimappa_dinamica(list(tocchi.values()), PAVIMENTO)
    return tocchi, rap


def rapporti(prof) -> dict[str, dict]:
    """I soli rapporti (per __main__ e per i test)."""
    return voci_col_tocco(prof)[1]


#: Il tema (tromba): tiene una nota nelle battute 1 e 3 (rado), corre di crome
#: nelle 2 e 4 (fitto). Identico nelle due passate -- e' lo sfondo, non varia.
def _tema_eventi(offset: int) -> list:
    return [
        (offset + 0 * B, 'sol4', '1/1'),                              # b1: TIENE
        (offset + 1 * B + 0, 're5', '1/4'), (offset + 1 * B + 96, 'do5', '1/4'),
        (offset + 1 * B + 192, 'si4', '1/4'), (offset + 1 * B + 288, 'la4', '1/4'),  # b2: corre
        (offset + 2 * B, 'sol4', '1/1'),                              # b3: TIENE
        (offset + 3 * B + 0, 'la4', '1/4'), (offset + 3 * B + 96, 'si4', '1/4'),
        (offset + 3 * B + 192, 'do5', '1/4'), (offset + 3 * B + 288, 're5', '1/4'),  # b4: corre
    ]


def tema() -> dict:
    return MU.linea(_tema_eventi(0) + _tema_eventi(PASSATA), velocity=84)


def costruisci() -> tuple[object, dict]:
    """Monta il pezzo dell'ascolto: una passata piatta, una col tocco, sul kit
    KIT009 (che ha il ride vero). Ritorna `(doc, rapporti)`. Solleva
    FileNotFoundError se manca il dataset o una fixture."""
    import warnings                                           # noqa: PLC0415
    from delugexml import parse_file, song as S              # noqa: PLC0415
    from delugexml import create as C, arranger as A         # noqa: PLC0415
    from delugexml import kit as K                           # noqa: PLC0415

    prof = profilo()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(str(TEMPL))
        S.set_bpm(doc.root, BPM)
        S.set_swing(doc, SWING, figura='1/8')                # lo swing e' di SONG
        S.set_scale(doc, 'C', 'maggiore')
        for strumento in list(S.instruments(doc)):
            MU.togli(doc, strumento)

        kit, clip_kit = C.add_track(doc, str(KIT), name='KIT009', folder='KITS',
                                    length=2 * PASSATA, playing=True)
        tenuti = tuple(VOCI.values())
        for nome in [S.nome_drum(d) for d in S.drums(kit)]:
            if nome and nome not in tenuti:
                K.remove_drum(doc, kit, nome)

        tocchi, rap = voci_col_tocco(prof, PASSATA)           # passata 2: tocco + rimappa
        for voce, drum in VOCI.items():
            piatto = note_voce(voce, 0)                       # passata 1: velocity 80
            MU.scrivi(doc, clip_kit, piatto + tocchi[voce], dove=drum)

        itema, clip_tema = C.add_track(doc, str(PRESET_TEMA), name='TEMA',
                                       folder='SYNTHS', length=2 * PASSATA)
        MU.scrivi(doc, clip_tema, tema())

        A.place(doc, kit, clip_kit, 0, 2 * PASSATA)
        A.place(doc, itema, clip_tema, 0, 2 * PASSATA)
        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc, rap


def racconta_tocco(prof) -> str:
    """Il tocco a confronto col piatto, voce per voce: la velocity che SUONA
    (misurata dal batterista, poi rimappata sul kit) e lo scarto. Per guardare
    la mano invece di immaginarla (regola 4)."""
    tocchi, rap = voci_col_tocco(prof, 0)
    dmin, dmax = rap['rimappa']['da']
    pmin, pmax = rap['rimappa']['a']
    righe = [f'esecuzione {prof.id}  {prof.style}  {prof.bpm} BPM  '
             f'BUR {prof.bur:.2f}  {prof.battute} battute',
             'piatto: ogni colpo a velocity 80, sulla griglia.',
             f'tocco: dinamica misurata [{dmin}..{dmax}] rimappata udibile '
             f'[{pmin}..{pmax}], scarto in tick.', '']
    for voce in VOCI:
        per_passo = {p.passo: p for p in prof.passi[voce]}
        # il passo si legge dalla posizione ORIGINALE (griglia): dopo il tocco
        # la nota e' gia' spostata dallo scarto e non cade piu' sul suo passo.
        griglia = note_voce(voce, 0)
        vista = {}
        for orig, toc in zip(griglia, tocchi[voce]):
            passo = (orig.pos // MU.TICK_PER_PASSO) % 16
            vista[passo] = (toc.velocity, per_passo[passo].scarto)
        pezzi = [f'p{passo} vel{v} scarto{s:+.0f}'
                 for passo, (v, s) in sorted(vista.items())]
        righe.append(f'  {voce:20s} ' + '  '.join(pezzi))
    return '\n'.join(righe)


if __name__ == '__main__':
    prof = profilo()
    print(racconta_tocco(prof))
    print('\n--- rapporti (regola 4) ---')
    rap = rapporti(prof)
    for voce in VOCI:
        r = rap[voce]
        print(f'  {voce:20s} toccate={r["toccate"]:2d}  '
              f'senza_appoggio={r["senza_appoggio"]}  collisioni={r["collisioni"]}')
    rm = rap['rimappa']
    print(f'  rimappa dinamica     {rm["da"]} -> {rm["a"]}  '
          f'({rm["toccate"]} note)')
