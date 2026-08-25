"""La coppia controllata dello swing: SWINGA e SWINGB.

LA DOMANDA
----------
`GR.profilo()` TOGLIE lo swing dalle posizioni misurate (`_senza_swing()`)
perche' lo rimetta il firmware con `S.set_swing()`. Se i due modelli non
coincidono, il groove template porta un residuo sbagliato e non se ne accorge
nessuno. La verifica gia' fatta -- togliere lo swing e rimetterlo con la
formula della docstring di `set_swing()` -- torna a zero **contro se' stessa**:
le due formule sono la stessa formula, quindi si invertono per costruzione e
tornerebbero a zero anche se fossero tutt'e due sbagliate.

Questa coppia mette il firmware in mezzo:

    out/SWINGA.XML   le posizioni ORIGINALI, swing 50 (dritto)
    out/SWINGB.XML   le STESSE note senza swing, piu' set_swing(display)

Se il modello di `_senza_swing()` e' quello del firmware, A e B suonano
identiche. Se no, no -- e la tabella che questo script stampa dice di quanto,
nota per nota, sotto ognuno dei modelli plausibili.

⚠️ NON passa da `GR.profilo()` ne' da `MU.applica_groove()`: il profilo
aggrega su 16 passi e prende la mediana fra le battute, cioe' e' lossy per
costruzione, e A e B fallirebbero per l'aggregazione invece che per lo swing.
Qui servono le STESSE note, una per una, quindi le `Note` si costruiscono a
mano dalle posizioni misurate.

⚠️ USA `GR._senza_swing`, che e' privata, ED E' VOLUTO: quella funzione e'
l'oggetto in esame, non un dettaglio da cui passare. Chiamare un wrapper
pubblico nasconderebbe proprio cio' che si vuole mettere alla prova.

Da lanciare da D:\\DelugePal:

    .venv/Scripts/python.exe tools/genera_swing.py

⚠️ Vuole due cose non versionate: `refs/songs/TEMPL0.XML` (la song di
partenza) e il Groove MIDI Dataset in `to-read/`. Senza, si ferma dicendolo.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import parse_file, write_file                 # noqa: E402
from delugexml import song as S, create as C                 # noqa: E402
from delugexml import kit as K, musica as MU                 # noqa: E402
from delugexml import groove as GR, midi as MI               # noqa: E402
from delugexml.notes import Note                             # noqa: E402
from delugexml.writer import FormatTable                     # noqa: E402

RADICE = Path(__file__).resolve().parent.parent
BASE_GROOVE = RADICE / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
KIT = RADICE / 'refs' / 'kits' / 'CR78FROMMARS.XML'
TABELLA = RADICE / 'out' / 'format_table.json'

#: L'esecuzione che fa da sorgente, e la scelta e' argomentata.
#:
#: - e' `jazz`, `beat`, 4-4, cioe' un groove continuo e non un fill;
#: - il ride suona lo *spang-a-lang*, cioe' la coppia di crome swingate
#:   ESPLICITA: e' l'ancora percettiva, chi ascolta sente lo swing li';
#: - il rullante comping cade anche FRA le crome, ed e' quello che permette
#:   di separare i modelli fra loro invece che solo dal vero (vedi
#:   `modelli()`);
#: - suona a 102 BPM, cioe' quasi il tempo a cui la coppia va ascoltata:
#:   NON serve la licenza di trasporre che la coppia del cancello ha dovuto
#:   dichiarare, e i millisecondi del residuo sono quelli del batterista.
#:
#: E' nominata perche' quel che ne esce e' [OSS] su un esecutore, mai [MIS]
#: su un repertorio.
ESECUZIONE = 'drummer1/session1/47'

#: Le due battute dell'estratto. La prima e' il ride nudo col charleston a
#: pedale sul 2 e sul 4 -- l'ancora; la seconda aggiunge il comping di
#: rullante e cassa, che e' dove stanno le note fra le crome.
DA_BATTUTA = 4
BATTUTE = 2
LUNGHEZZA = BATTUTE * MU.TICK_PER_BATTUTA

#: Le quattro voci tenute, e il drum su cui vanno.
#:
#: ⚠️ Il drum si sceglie per il TRANSIENTE, non per la verosimiglianza: la
#: domanda e' se una nota cade prima o dopo, e un piatto con la coda lunga
#: la nasconde. Per questo il charleston a pedale finisce su un rim e non su
#: un open hat. Il kit e' lo stesso della coppia del cancello, cosi' chi
#: ascolta non deve anche riabituare l'orecchio a un timbro nuovo.
VOCI = (
    # voce del Groove MIDI,   drum del kit
    ('ride',                  'CH CR78 03'),
    ('charleston a pedale',   'Rim CR78 02'),
    ('rullante',              'Snare CR78 13'),
    ('kick',                  'Kick CR78 12'),
)

#: I drum che restano nel kit: quattro righe stanno in una schermata sola.
TENUTI = tuple(d for _, d in VOCI)

#: La durata di ogni nota. Sui drum di un kit e' un one-shot e non cambia il
#: suono; serve solo a non far accavallare due note sulla stessa riga, e il
#: divario minimo fra due colpi della stessa voce nell'estratto e' 32 tick.
DURATA = MU.TICK_PER_PASSO


# ------------------------------------------------------- i modelli in esame
#
# Ogni modello e' una mappa DIRETTA -- da posizione scritta a posizione
# suonata -- che il firmware POTREBBE applicare quando `swingAmount` non e'
# zero. `_senza_swing()` e' l'inversa esatta del primo, e di nessun altro.


def avanti(s: float, levare: float, blocco: float) -> float:
    """La mappa lineare a tratti dello swing, su un blocco di `blocco` tick.

    La prima meta' del blocco viene dilatata fino a `levare`, la seconda
    compressa in quel che resta: e' la descrizione del sorgente
    (`playback_handler.cpp` dilata di `(50+swingAmount)/50` e comprime di
    `(50-swingAmount)/50`), quindi il blocco dura sempre uguale.
    """
    m, g = divmod(float(s), blocco)
    if g < blocco / 2:
        return m * blocco + g * 2 * levare
    return m * blocco + levare * blocco + (g - blocco / 2) * 2 * (1 - levare)


def solo_la_seconda(s: float, levare: float, tolleranza: float = 0.0) -> float:
    """Solo la nota SULLA seconda croma si sposta; le altre restano.

    E' l'altra lettura possibile di «le note si muovono a coppie della figura
    nominata, e a spostarsi e' la seconda della coppia»: uno spostamento di
    EVENTO agganciato alla griglia, invece di una deformazione del tempo. Una
    nota che cade FRA le crome, sotto questo modello, non si muove affatto --
    ed e' esattamente il caso che nessuna fonte del progetto copre.

    `tolleranza` e' la finestra, in tick, entro cui una nota conta come
    "sulla seconda croma": 0 vuol dire esattamente, e allora sull'estratto non
    si muove niente.
    """
    return (s + (levare - 0.5) * 96 if abs(s % 96 - 48) <= tolleranza
            else float(s))


def traslata(s: float, levare: float) -> float:
    """La seconda meta' TRASLATA invece che compressa: il blocco si allunga.

    Implementazione ingenua e possibile, ma **il sorgente la esclude**: li' la
    somma delle due meta' non cambia. Sta qui perche' ha una firma sua --
    lascia intatti i levare e manda in ritardo i battere anticipati -- e
    quindi si riconosce senza confondersi con gli altri.
    """
    m, g = divmod(float(s), 96.0)
    return m * 96.0 + (g if g < 48 else g + (levare - 0.5) * 96)


#: I modelli, nell'ordine in cui la tabella li stampa. Il primo e' quello che
#: `_senza_swing()` assume: sotto quello, e solo sotto quello, A e B devono
#: suonare identiche.
MODELLI = (
    ('M96', 'blocco 96 tick (croma+croma)', lambda s, L: avanti(s, L, 96.0)),
    ('M48', 'blocco 48 tick (doubleSwingInterval alla lettera)',
     lambda s, L: avanti(s, L, 48.0)),
    ('M192', 'blocco 192 tick (il fattore 2 dall altra parte)',
     lambda s, L: avanti(s, L, 192.0)),
    ('MSOLO', 'solo la nota esattamente sulla seconda croma',
     lambda s, L: solo_la_seconda(s, L)),
    ('MSOLO6', 'come MSOLO ma con una finestra di +/- 6 tick',
     lambda s, L: solo_la_seconda(s, L, 6.0)),
    ('MTRASL', 'la seconda meta traslata invece che compressa', traslata),
)


def senza_swing(t: float, levare: float) -> float:
    """Toglie lo swing da una posizione assoluta in tick Deluge.

    La fase e' `(t mod 96)/96`, cioe' l'inversa ESATTA del blocco del
    firmware.

    ⚠️ MISURA STORICA, e la data conta: 24 agosto 2026. IL GIORNO IN CUI
    QUESTA COPPIA E' STATA COSTRUITA E ASCOLTATA `profilo_da_colpi()`
    assegnava il movimento con `floor(t/96 + 0.125)` -- mezzo passo di
    grazia -- e trattava quindi una nota nell'ultimo ottavo di movimento
    come un ANTICIPO del movimento dopo, con una fase NEGATIVA che non e'
    nel dominio di `_senza_swing()`. Su questo estratto costava fino a
    3,2 tick, e tenerla qui avrebbe mescolato due variabili in una coppia
    che ne deve avere una sola: e' stata lasciata fuori apposta e `main()`
    la misura a parte.

    DAL COMMIT `18f26e5` LA GRAZIA NON C'E' PIU'. `profilo_da_colpi()` fa
    `divmod(p, ppq)`, cioe' esattamente l'aritmetica di movimento e fase di
    questa funzione, e la divergenza e' chiusa: quel che segue non descrive
    piu' un ramo del codice, descrive quanto costava quello vecchio.
    """
    m, g = divmod(float(t), 96.0)
    return m * 96.0 + GR._senza_swing(g / 96.0, levare) * 96.0


# ------------------------------------------------------------- il materiale


def sorgente():
    """L'estratto: le note misurate, il levare e il display che ne viene.

    Ritorna `(note, levare, display, bpm, bur)`, con `note` gia' in tick
    Deluge relativi all'inizio dell'estratto e con l'origine della griglia
    tolta.
    """
    e = [x for x in GR.elenco(BASE_GROOVE) if x.id == ESECUZIONE][0]
    f = MI.leggi(BASE_GROOVE / e.midi_filename)

    colpi = []
    for traccia in f.tracce:
        for n in traccia.note:
            nome = MI.GM_PERCUSSIONI.get(n.y)
            if nome is not None:
                colpi.append((float(n.pos), nome, n.velocity))
    colpi.sort()

    # l'origine si stima su TUTTA l'esecuzione, non sulle due battute: il
    # tick 0 del file non e' un movimento del batterista, e due battute non
    # bastano a dirlo.
    passo = f.ppq / 4
    off = GR.origine([p for p, _, _ in colpi], passo)
    bur = GR.bur_da_posizioni([p - off for p, _, _ in colpi], float(f.ppq))
    levare = MU.da_bur(bur)

    scala = float(MI.TICK_PER_MOVIMENTO_DELUGE) / f.ppq
    da = DA_BATTUTA * MU.TICK_PER_BATTUTA
    quali = {v for v, _ in VOCI}
    note = []
    for p, nome, vel in colpi:
        t = (p - off) * scala - da
        if nome in quali and 0 <= t < LUNGHEZZA:
            note.append((t, nome, vel))
    note.sort()
    return note, levare, round(levare * 100), e.bpm, bur


def modelli(note, levare_esatto: float, display: int, bpm: int) -> None:
    """LA PREVISIONE, nota per nota e prima dell'ascolto.

    Per ogni nota: dove sta in A (la posizione originale, arrotondata al
    tick), dove sta in B (senza swing, arrotondata al tick), e dove il
    firmware la farebbe SUONARE sotto ognuno dei modelli. Lo scarto e'
    `suonata(B) - A`: zero vuol dire che A e B suonano uguali.

    ⚠️ Il levare con cui si TOGLIE lo swing e' quello misurato, mentre quello
    con cui il firmware lo RIMETTE e' il display arrotondato all'intero: sono
    due numeri diversi apposta, perche' e' cosi' che la catena vera funziona.
    """
    lev_firmware = display / 100.0
    tick_ms = 60000 / (bpm * MI.TICK_PER_MOVIMENTO_DELUGE)
    print(f'levare misurato {levare_esatto:.5f}, display {display}, '
          f'cioe\' il firmware userebbe {lev_firmware}')
    print(f'un tick vale {tick_ms:.3f} ms a {bpm} BPM')
    print()

    intestazione = (f'{"voce":22s} {"A":>5s} {"B":>5s} {"fase":>6s} | '
                    + ' '.join(f'{m:>7s}' for m, _, _ in MODELLI))
    print(intestazione)
    print('-' * len(intestazione))
    scarti = {m: [] for m, _, _ in MODELLI}
    for t, nome, _ in note:
        a = round(t)
        b = round(senza_swing(t, levare_esatto))
        riga = []
        for m, _, fn in MODELLI:
            d = fn(b, lev_firmware) - a
            scarti[m].append(d)
            riga.append(f'{d:7.2f}')
        print(f'{nome:22s} {a:5d} {b:5d} {(b % 96) / 96:6.3f} | '
              + ' '.join(riga))
    print()
    for m, cosa, _ in MODELLI:
        v = scarti[m]
        medio = sum(abs(x) for x in v) / len(v)
        massimo = max(abs(x) for x in v)
        print(f'{m:7s} medio {medio:5.2f} tick ({medio * tick_ms:5.1f} ms), '
              f'massimo {massimo:5.2f} tick ({massimo * tick_ms:5.1f} ms), '
              f'oltre 1 tick {sum(1 for x in v if abs(x) > 1):2d}/{len(v)}'
              f'   {cosa}')

    # da cosa e' fatto il residuo di M96: sono le due sole perdite della
    # catena, e stanno tutt'e due SOTTO la griglia dei tick. Nessun ascolto
    # puo' escluderle: e' un fatto sui numeri, non sull'orecchio.
    print()
    print('e il residuo di M96, scomposto nelle sue due perdite:')
    for cosa, fn in (
            ('il display arrotondato all intero',
             lambda t: avanti(senza_swing(t, levare_esatto),
                              lev_firmware, 96.0) - t),
            ('le posizioni arrotondate al tick',
             lambda t: avanti(round(senza_swing(t, levare_esatto)),
                              levare_esatto, 96.0) - round(t))):
        v = [fn(t) for t, _, _ in note]
        medio = sum(abs(x) for x in v) / len(v)
        massimo = max(abs(x) for x in v)
        print(f'        {cosa:36s} medio {medio:6.4f} tick '
              f'({medio * tick_ms:5.3f} ms), massimo {massimo:6.4f} tick '
              f'({massimo * tick_ms:5.3f} ms)')

    # La seconda variabile, misurata a parte e non messa dentro la coppia.
    # ⚠️ MISURA STORICA, non comportamento corrente: il conto qui sotto
    # rifa' quel che `profilo_da_colpi()` faceva FINO AL COMMIT `18f26e5`
    # (24 agosto 2026), cioe' col mezzo passo di grazia. Oggi quella
    # funzione fa `divmod` come `senza_swing()` qui sopra, e questo ramo non
    # esiste piu' da nessuna parte: resta perche' e' il numero che dice
    # perche' la grazia e' stata tenuta fuori dalla coppia ascoltata.
    peggio = []
    for t, _, _ in note:
        movimento = math.floor(t / 96.0 + 0.125)
        fase = t / 96.0 - movimento
        b = round((movimento + GR._senza_swing(fase, levare_esatto)) * 96.0)
        peggio.append(avanti(b, lev_firmware, 96.0) - round(t))
    medio = sum(abs(x) for x in peggio) / len(peggio)
    massimo = max(abs(x) for x in peggio)
    print()
    print(f'e se B togliesse lo swing con la grazia di mezzo passo, come '
          f'faceva `profilo_da_colpi()` FINO AL 24 agosto 2026 (misura '
          f'storica: oggi quella funzione fa `divmod`, come qui sopra):')
    print(f'        medio {medio:5.2f} tick ({medio * tick_ms:5.1f} ms), '
          f'massimo {massimo:5.2f} tick ({massimo * tick_ms:5.1f} ms) '
          f'ANCHE sotto M96')


# ------------------------------------------------------------- le due song


def costruisci(note, levare: float, display: int, bpm: int, *, con_swing: bool):
    """La song. L'UNICA differenza fra le due e' dove vive lo swing.

    `con_swing=False` -> SWINGA: posizioni originali, `swingAmount` a zero.
    `con_swing=True`  -> SWINGB: posizioni senza swing, `swingAmount` dal
    display misurato.

    ⚠️ `figura='1/8'` si scrive in TUTT'E DUE. Con `swingAmount` a zero
    l'intervallo non ha effetto -- la dilatazione vale 1 -- quindi scriverlo
    anche in A non cambia niente di cio' che si sente, e fa si' che le due
    song differiscano per il SOLO `swingAmount` piu' i blob delle note. Una
    coppia controllata si giudica anche dal diff.
    """
    doc = parse_file(TEMPL)
    S.set_bpm(doc.root, bpm)
    S.set_swing(doc, display if con_swing else S.SWING_CENTRO, figura='1/8')

    for strumento in list(S.instruments(doc)):
        MU.togli(doc, strumento)

    kit, clip = C.add_track(doc, KIT, name='CR78FROMMARS', folder='KITS',
                            length=LUNGHEZZA, playing=True)
    for nome in [d.get('name') for d in S.drums(kit)]:
        if nome not in TENUTI:
            K.remove_drum(doc, kit, nome)

    rapporti = []
    for voce, drum in VOCI:
        righe = []
        for t, nome, vel in note:
            if nome != voce:
                continue
            pos = round(senza_swing(t, levare) if con_swing else t)
            righe.append(Note(pos=pos, length=DURATA, velocity=vel))
        rapporti.append(MU.scrivi(doc, clip, righe, dove=drum))
    rapporti.append(S.fit_clip_scroll_to_notes(doc, clip))
    return doc, rapporti


def scrivi_song(doc, nome: str) -> tuple[Path, str]:
    """Il percorso remoto lo costruisce `destinazione()` (regola 5), e da
    quello viene il nome locale: nessun percorso scritto a mano."""
    remoto = MU.destinazione(nome, None)
    locale = RADICE / 'out' / Path(remoto).name
    write_file(doc, locale, FormatTable.load(TABELLA))
    return locale, remoto


def confronta(a: Path, b: Path) -> None:
    """Il controllo che rende la coppia una coppia: cosa e' cambiato davvero.

    Fuori dai blob delle note deve cambiare il solo `swingAmount`: qualunque
    altra riga diversa vorrebbe dire che A e B differiscono per qualcosa che
    non e' lo swing, e la differenza che si ascolta non sarebbe attribuibile.
    """
    prima = a.read_text('utf-8', 'surrogateescape').splitlines()
    dopo = b.read_text('utf-8', 'surrogateescape').splitlines()
    diverse = [(i, x, y) for i, (x, y) in enumerate(zip(prima, dopo), 1)
               if x != y]
    print('=' * 70)
    print(f'confronto {a.name} / {b.name}')
    print('=' * 70)
    if len(prima) != len(dopo):
        print(f'  ⚠ righe diverse in numero: {len(prima)} contro {len(dopo)}')
    fuori = [r for r in diverse
             if 'noteData' not in r[1] and 'noteData' not in r[2]]
    atteso = [r for r in fuori if 'swingAmount' in r[1]]
    inatteso = [r for r in fuori if r not in atteso]
    print(f'  righe totali: {len(prima)}')
    print(f'  righe diverse: {len(diverse)}, di cui su noteData: '
          f'{len(diverse) - len(fuori)}, su swingAmount: {len(atteso)}')
    for i, x, y in atteso:
        print(f'    r{i} - {x.strip()}')
        print(f'    r{i} + {y.strip()}')
    if inatteso:
        print('  ⚠ DIFFERENZE INATTESE -- la coppia non e controllata:')
        for i, x, y in inatteso[:20]:
            print(f'    r{i} - {x.strip()[:100]}')
            print(f'    r{i} + {y.strip()[:100]}')
    else:
        print('  nessun altra differenza: la coppia e controllata')


def main() -> int:
    for percorso, cosa in ((TEMPL, 'la song di partenza'),
                           (KIT, 'il kit'),
                           (BASE_GROOVE, 'il Groove MIDI Dataset')):
        if not percorso.exists():
            print(f'manca {cosa}: {percorso}', file=sys.stderr)
            return 2

    note, levare, display, bpm, bur = sorgente()
    print(f'sorgente: {GR.racconta(BASE_GROOVE, ESECUZIONE)}')
    print(f'          BUR {bur:.4f}, estratto: battute {DA_BATTUTA} e '
          f'{DA_BATTUTA + 1}, {len(note)} note, '
          f'{len({n for _, n, _ in note})} voci')
    print()
    modelli(note, levare, display, bpm)
    print()

    scritti = []
    for nome, con_swing in (('swinga', False), ('swingb', True)):
        doc, rapporti = costruisci(note, levare, display, bpm,
                                   con_swing=con_swing)

        problemi = MU.verifica(doc)
        if problemi:
            print(f'{nome}: il cancello e chiuso, NON si carica: '
                  + '; '.join(problemi), file=sys.stderr)
            return 1
        avvisi = MU.avvertenze(doc)

        locale, remoto = scrivi_song(doc, nome)
        scritti.append(locale)

        print('=' * 70)
        print(f'{locale.name}  ->  {remoto}')
        print('=' * 70)
        for r in rapporti:
            if r:
                print('  ', r)
        for a in avvisi:
            print('   avvertenza:', a)
        print()
        print(MU.racconta(doc))
        print()

    confronta(*scritti)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
