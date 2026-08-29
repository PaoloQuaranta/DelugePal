"""Il primo pezzo jazz di Deluge Pal: un blues di 12 battute in fa.

    out/JAZZ0<N>.XML   ->   /SONGS/DelugePal/JAZZ0<N>.XML

Forma TEMA / ASSOLO / TEMA, 36 battute, hardbop, 128 BPM. Quattro tracce:
batteria (KIT009, un RX-5), basso walking, comping, tema.

Il progetto sta in `docs/superpowers/specs/2026-08-29-primo-pezzo-jazz-design.md`
e dice da dove viene ogni cosa, col grado di prova. In due righe:

  - lo SWING e la SCALA DI VELOCITY sono `[MIS]`, dalla casella 4 e dalla 6
    di `docs/repertori/jazz.md`;
  - il GROOVE TEMPLATE e' `[OSS]` su UN batterista, `drummer10/session1/1`;
  - il GIRO ARMONICO e' letto dalla trascrizione di `Walkin'` in `wjazzd.db`
    (melid 196): blues classico in fa, nessuna sostituzione bebop;
  - i VOICING e il WALKING vengono dalla skill `music-composition`, `[WEB]`;
  - il TEMA e l'ASSOLO sono ORIGINALI. Di `Walkin'` si e' osservata la
    FORMA -- densita' 5,2 note/battuta, 61% degli intervalli entro 2
    semitoni, una frase ogni ~2,7 battute -- e non si e' copiata nessuna
    nota.

⚠️ PERCHE' 128 BPM E NON 140. Lo scarto che `MU.applica_groove()` scrive e'
in TICK, cioe' una frazione di movimento: scriverlo a un tempo diverso da
quello a cui e' stato misurato ne conserva la proporzione e ne cambia i
millisecondi. Il template e' misurato a 124 BPM. A 128 si sposta del 3%; a
140 dell'11%. 128 e' il tempo che non trasporta niente.

⚠️ PERCHE' NON IL TEMPLATE CHE LA CASELLA 6 RACCOMANDA. Lei raccomanda
`drummer1/session3/2` perche' e' la piu' lunga delle `jazz/swing` 4/4. Due
ragioni per non usarla qui: sta a 185 BPM (un tick vale 3,378 ms contro i
4,883 di 128, quindi lo stesso scarto uscirebbe +45% piu' lungo), e su di
lei il nome GM non e' il ruolo musicale -- il disegno del ride sta per otto
decimi sulla nota 43, che la mappa chiama `tom basso`. Su
`drummer10/session1/1` il ride e' il ride: 219 colpi, spang-a-lang, l'83%
dei quali sui sei passi 0-4-6-8-12-14.

⚠️ NON E' UNA COPPIA CONTROLLATA. E' un pezzo di musica da far ascoltare:
quello che ne esce e' `[OSS]`, e vale la regola del comune «Un ascolto non
e' una misura di percezione». Rigenerarlo non distrugge niente -- al
contrario di `genera_groove.py` e `genera_swing.py`, che NON vanno lanciati.

Da lanciare da D:\\DelugePal:

    .venv/Scripts/python.exe tools/genera_jazz.py

⚠️ Vuole tre cose non versionate: `refs/songs/TEMPL0.XML`, i quattro preset
in `refs/kits/` e `refs/synths/`, e il Groove MIDI Dataset in `to-read/`.
Senza, si ferma dicendolo.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import parse_file, write_file                 # noqa: E402
from delugexml import song as S, create as C                 # noqa: E402
from delugexml import kit as K, musica as MU                 # noqa: E402
from delugexml import groove as GR                           # noqa: E402
from delugexml.writer import FormatTable                     # noqa: E402

RADICE = Path(__file__).resolve().parent.parent
TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
KIT = RADICE / 'refs' / 'kits' / 'KIT009.XML'
PRESET_BASSO = RADICE / 'refs' / 'synths' / 'Square Saw Bass.XML'
PRESET_COMPING = RADICE / 'refs' / 'synths' / 'Pianism I.XML'
PRESET_TEMA = RADICE / 'refs' / 'synths' / '062 Trumpet.XML'
BASE_GROOVE = RADICE / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
TABELLA = RADICE / 'out' / 'format_table.json'

#: L'esecuzione da cui esce il groove template. Va NOMINATA ogni volta che se
#: ne cita un numero: e' `[OSS]` su un esecutore, non `[MIS]` sul jazz.
ESECUZIONE = 'drummer10/session1/1'

#: La versione che si scrive. `put` non sovrascrive mai: si incrementa.
#:   01  29 agosto 2026, assolo scritto a mano. «Poco pirotecnico».
#:   02  29 agosto 2026, assolo generato dalle cinque regole della
#:       casella 8. Tutto il resto e' identico alla 01, di proposito:
#:       se la differenza si sente, e' attribuibile.
#:       Verdetto: «alcune note sembrano fuori tonalita'... non mi sembra
#:       piu' pirotecnico, soprattutto perche' e' tutto in ottavi».
#:   03  29 agosto 2026, e cambia DUE cose insieme, che va detto perche'
#:       limita l'attribuzione: le note si scelgono sulla distribuzione
#:       misurata dei gradi SULLA TONICA DEL PEZZO invece che sulla scala
#:       dell'accordo, e la griglia dell'assolo passa a sedicesimi.
#:       Verdetto: «ora suona molto meglio. Le note sono a posto, le corse
#:       suonano bene ed e' decisamente piu' pirotecnico».
#:
#: ⚠️ E' il primo giro CHIUSO di questo progetto: una lamentela all'orecchio,
#: una misura sul corpus, una correzione, e lo stesso orecchio che approva.
#: Le tre versioni restano una coppia controllata a tre -- batteria, basso e
#: comping hanno le stesse identiche note in tutte e tre -- quindi i tre
#: verdetti parlano dell'assolo e di nient'altro.
VERSIONE = 3

BPM = 128
#: Casella 10 di `docs/repertori/jazz.md`, riga HARDBOP/BEBOP. `figura='1/8'`
#: perche' il default del firmware swinga le SEMICROME e su una linea di
#: crome non muove niente.
SWING = 64

TICK_BATTUTA = 384
BATTUTE = 36
LUNGHEZZA = TICK_BATTUTA * BATTUTE

# --------------------------------------------------------------------------
# L'armonia
# --------------------------------------------------------------------------

#: Il giro, letto da `wjazzd.db` melid 196 (`Walkin'`, J.J. Johnson, F-maj,
#: HARDBOP, SWING, 128 BPM, forma `A12`). Blues classico in fa col
#: turnaround ii-V, nessuna sostituzione bebop. Una casella per battuta;
#: la 12 ne porta due, meta' e meta'.
GIRO = ('F7', 'Bb7', 'F7', 'F7', 'Bb7', 'Bb7',
        'F7', 'F7', 'Gm7', 'C7', 'F7', 'Gm7|C7')

#: I voicing SENZA FONDAMENTALE, scritti a mano dalle tabelle di
#: `assets/jazz-voicings.md` della skill `music-composition`, e alternati
#: A (3-5-7-9) / B (7-9-3-5) per la condotta delle parti.
#:
#: ⚠️ NON si ottengono con `MU.armonia(voicing=…)`: `MU.VOICING` ha UNA sola
#: forma senza fondamentale, quindi la «B» non esiste e nessun argomento la
#: produce. La casella 7 dichiara la lacuna e prescrive questo ripiego.
#:
#: La condotta che ne esce, verificata a mano:
#:     F7 -> Bb7    -1,  0, -1, -2      (una nota comune)
#:     Gm7 -> C7     0,  0, -1, -2      (DUE note comuni: il ii-V)
#:     C7 -> F7     -1, -2, -1,  0      (una nota comune)
VOICING = {
    'F7':  (57, 60, 63, 67),   # A: la3  do4  mib4 sol4   (3-5-7-9)
    'Bb7': (56, 60, 62, 65),   # B: lab3 do4  re4  fa4    (7-9-3-5)
    'Gm7': (58, 62, 65, 69),   # A: sib3 re4  fa4  la4    (3-5-7-9)
    'C7':  (58, 62, 64, 67),   # B: sib3 re4  mi4  sol4   (7-9-3-5)
}

#: Il ritmo del comping, otto crome per battuta, `x` suona e `.` tace.
#: Sincopato e VARIO: un comping identico dodici volte e' la stessa morte
#: formale del primo dub. Il primo e il terzo giro (il tema) lasciano piu'
#: spazio, il secondo (l'assolo) risponde di piu'.
#: ⚠️ La battuta 12 di ogni giro ne porta due, di accordi: la sua stringa
#: vale per Gm7 sulla prima meta' e C7 sulla seconda.
COMPING = (
    # giro 1 -- il tema. Rado.
    'x..x....', '...x....', 'x.....x.', '...x....',
    'x..x....', '......x.', 'x..x....', '....x...',
    'x..x....', '...x....', 'x.....x.', 'x...x...',
    # giro 2 -- l'assolo. Piu' fitto.
    '...x....', 'x..x..x.', '...x....', 'x.....x.',
    '..x...x.', '...x....', 'x..x....', '......x.',
    'x..x....', '..x...x.', 'x.....x.', 'x...x...',
    # giro 3 -- il tema che torna. Come il primo, un filo piu' pieno.
    'x..x....', '...x....', 'x.....x.', '...x....',
    'x..x....', '..x...x.', 'x..x....', '....x...',
    'x..x....', '...x....', 'x.....x.', 'x.......',
)

# --------------------------------------------------------------------------
# Il basso
# --------------------------------------------------------------------------

#: I gradi di ogni accordo, in semitoni dalla fondamentale, per costruire il
#: walking. Fondamentale come classe di altezza (do = 0).
ACCORDI = {
    'F7':  (5,  (0, 4, 7, 10)),
    'Bb7': (10, (0, 4, 7, 10)),
    'Gm7': (7,  (0, 3, 7, 10)),
    'C7':  (0,  (0, 4, 7, 10)),
}

#: La forma della battuta di walking: quali gradi sui primi tre movimenti.
#: Il quarto e' sempre l'AVVICINAMENTO alla fondamentale della battuta dopo
#: -- `references/instrument-idiom/bass.md` della skill: «stepwise/chromatic
#: connection». `[WEB]`.
FORME = {
    'su':   (0, 4, 7),     # fondamentale, terza, quinta
    'giu':  (0, 10, 7),    # fondamentale, settima sotto, quinta
    'arco': (0, 7, 4),     # fondamentale, quinta, terza
    'sest': (0, 4, 9),     # fondamentale, terza, sesta
}

#: Una forma per battuta, per tutte e 36. Cambia fra i tre giri cosi' che il
#: basso non ripeta la stessa linea tre volte.
FORME_PER_BATTUTA = (
    'su', 'giu', 'arco', 'su', 'giu', 'su', 'arco', 'sest', 'su', 'giu', 'arco', 'su',
    'giu', 'su', 'sest', 'arco', 'su', 'giu', 'su', 'arco', 'giu', 'su', 'sest', 'arco',
    'arco', 'su', 'giu', 'sest', 'arco', 'su', 'giu', 'su', 'arco', 'giu', 'su', 'su',
)

#: La finestra di registro del basso, in numeri di nota MIDI: mi1 - do3.
#: `instrument-idiom/bass.md`: mi1-do2 e' la fondazione, do2-sol2 e' dove il
#: walking resta chiaro. `[WEB]`.
BASSO_MIN, BASSO_MAX = 28, 48


def _vicino(classe: int, riferimento: int) -> int:
    """La nota di quella classe di altezza piu' vicina a `riferimento`,
    tenuta dentro la finestra di registro del basso."""
    migliore, distanza = None, 10 ** 6
    for ottava in range(1, 5):
        n = 12 * ottava + classe
        if not BASSO_MIN <= n <= BASSO_MAX:
            continue
        d = abs(n - riferimento)
        if d < distanza:
            migliore, distanza = n, d
    return migliore if migliore is not None else riferimento


def walking(giro_esteso: list[str]) -> list[int]:
    """La linea di walking: una nota per movimento, 4 per battuta.

    Fondamentale sul primo movimento, due gradi dell'accordo, e sul quarto
    l'AVVICINAMENTO alla fondamentale della battuta successiva -- cromatico
    da sopra o da sotto secondo quale dei due e' piu' vicino a dove si e'
    arrivati. Non e' un'invenzione: e' la costruzione che la skill descrive.
    """
    note, precedente = [], 41       # fa2, da cui si parte
    for i, sigla in enumerate(giro_esteso):
        fond, _ = ACCORDI[sigla]
        prossima = ACCORDI[giro_esteso[(i + 1) % len(giro_esteso)]][0]
        forma = FORME[FORME_PER_BATTUTA[i % len(FORME_PER_BATTUTA)]]

        radice = _vicino(fond, precedente)
        battuta = [radice]
        for grado in forma[1:]:
            battuta.append(_vicino((fond + grado) % 12, battuta[-1]))

        # il quarto movimento: cromatico verso la fondamentale che viene
        bersaglio = _vicino(prossima, battuta[-1])
        sopra, sotto = bersaglio + 1, bersaglio - 1
        avvicinamento = sopra if abs(sopra - battuta[-1]) <= abs(sotto - battuta[-1]) else sotto
        battuta.append(max(BASSO_MIN, min(BASSO_MAX, avvicinamento)))

        note.extend(battuta)
        precedente = battuta[-1]
    return note


# --------------------------------------------------------------------------
# Il tema e l'assolo -- ORIGINALI
# --------------------------------------------------------------------------

#: Otto crome per battuta, numero di nota MIDI oppure `None` per pausa.
#: Il TEMA e' piu' rado e piu' cantabile dell'assolo: ~2,8 note per battuta
#: contro le 5,2 misurate su un assolo, ed e' una scelta dichiarata -- una
#: testa non e' un chorus.
TEMA_NOTE = (
    (None, None, 72, 74, 75, 77, None, None),   #  1  F7
    (None, None, 77, None, 75, None, 74, None), #  2  Bb7
    (72, None, None, None, None, None, None, None),  # 3  F7
    (None, None, None, None, None, None, 69, 70),    # 4  F7  (levare)
    (72, 74, 75, 77, None, None, None, None),   #  5  Bb7
    (None, None, 77, None, 75, None, 74, None), #  6  Bb7
    (72, None, None, None, None, None, None, None),  # 7  F7
    (None, None, None, None, None, None, None, None),  # 8  F7  -- spazio
    (None, None, 70, 72, 74, None, 77, None),   #  9  Gm7
    (None, 75, None, 74, None, 72, None, 70),   # 10  C7   (mib = #9, blue)
    (69, None, 72, None, 69, None, None, None), # 11  F7
    (None, None, None, None, None, None, 69, 70),    # 12 turnaround (levare)
)

#: L'ultima battuta del pezzo: al posto del levare, la fondamentale tenuta.
TEMA_CHIUSA = (77, None, None, None, None, None, None, None)

#: ⚠️ L'ASSOLO NON E' PIU' UNA TABELLA SCRITTA A MANO. Fino al 29 agosto 2026
#: lo era, e il difetto si e' sentito: l'utente lo ha giudicato «poco
#: pirotecnico». La casella 11 porta il numero che gli da' ragione -- media e
#: mediana centrate sul corpus, DISPERSIONE DIMEZZATA, zero battute vuote,
#: zero corse. Scrivere per centrare una media produce la media.
#:
#: Adesso l'assolo esce dalle cinque regole misurate nella CASELLA 8:
#:
#:   1. l'arco del giro: poche corse all'inizio, il picco sul ii-V, il vuoto
#:      sul turnaround;
#:   2. il respiro a fine frase: battute 4, 8 e 12, con la 12 la piu' vuota;
#:   3. una corsa dura UNA battuta, due al massimo;
#:   4. le corse si ADDENSANO, non si alternano ai silenzi;
#:   5. un motivo e' di almeno CINQUE note -- sotto le quattro la ripetizione
#:      e' indistinguibile dal caso.

#: Note per battuta, una per posizione del giro. NON e' una scelta di gusto:
#: segue l'arco misurato su 66 assoli e 38 solisti. Le corse (8) cadono sul
#: ii-V, i respiri (2, 1, 0) sulle chiusure delle tre frasi, e la 12 e' vuota
#: perche' e' la posizione piu' vuota del corpus (14,8%).
#:
#: ⚠️ DALLA VERSIONE 03 LA GRIGLIA E' DI SEDICESIMI, 16 per battuta. Fino
#: alla 02 era di crome col massimo a 8, e l'utente ha detto: «non mi sembra
#: piu' pirotecnico, soprattutto perche' e' tutto in ottavi, perche' non usi
#: anche sedicesimi?». Aveva ragione -- il corpus arriva a 16 note per
#: battuta, e senza semicrome una corsa non e' una corsa.
#:
#: ⚠️ IL PUNTO APERTO NON E' STATO CHIUSO, e' stato attraversato. Una
#: semicroma sotto `set_swing(figura='1/8')` cade FRA le crome, e cosa il
#: firmware ne faccia sta in `HANDOFF.md` §7. Si e' scelto di scriverci sopra
#: e di far decidere all'orecchio, che e' l'unico strumento che qui puo'
#: decidere. SE LA CORSA SUONA STORTA, la prima cosa da sospettare e' questa e
#: non la scelta delle note.
DENSITA = (5, 6, 6, 2, 5, 7, 6, 1, 12, 12, 5, 0)

#: Dove cadono le note dentro la battuta, su 16 sedicesimi. I respiri mettono
#: le note ALL'INIZIO e poi tacciono: sono chiusure di frase, non levare. Le
#: corse sono tre movimenti di sedicesimi e poi aria -- una corsa che riempie
#: la battuta intera non atterra da nessuna parte.
SLOT = {
    0:  '................',
    1:  'x...............',
    2:  'x.x.............',
    5:  'x...x...x.x...x.',
    6:  'x...x.x.x...x.x.',
    7:  'x.x.x.x.x...x.x.',
    12: 'xxxxxxxxxxxx....',
}

#: Le due corse non partono dallo stesso posto: la 9 entra sul secondo
#: movimento, la 10 sul primo. Due corse identiche di fila sono un esercizio.
SLOT_BATTUTA = {9: '....xxxxxxxxxxxx'}

#: Il motivo: cinque note, cioe' quattro intervalli. ⚠️ Cinque e non tre: a
#: tre note la ripetizione e' indistinguibile dal caso (1,02x contro la stessa
#: linea mescolata), a cinque vale 4,2x in 78 assoli su 80. Sono i gradi della
#: scala dell'accordo, non semitoni.
MOTIVO = (0, 1, 2, 4, 3)

#: Dove il motivo viene enunciato: battuta del giro -> trasposizione in
#: SEMITONI dalla prima enunciazione.
#: ⚠️ In semitoni e non per grado, ed e' la ragione per cui il motivo si
#: ritrova: la misura della casella 8 conta i profili di INTERVALLI, e una
#: trasposizione per grado ne cambierebbe uno. +5 sulla battuta 5 porta il
#: materiale di F7 su Bb7 conservando il rapporto, che e' la risposta classica
#: del blues.
ENUNCIAZIONI = {1: 0, 5: 5, 11: 0}

#: ⚠️ LA SCALA DELL'ACCORDO ERA L'ERRORE DELLA VERSIONE 02, e l'utente l'ha
#: sentito: «alcune note sembrano fuori tonalita'... il solo suona troppo
#: distante dalla tonalita'». Costruire la scala di OGNI ACCORDO -- misolidia
#: su F7 e Bb7, dorica su Gm7, misolidia su C7 -- e' corretto sull'accordo e
#: sbagliato sul pezzo. Misurato su 80 assoli e 33 714 note, sui gradi
#: relativi alla TONICA DEL PEZZO:
#:
#:   - il grado 11 (in fa il mi naturale) stava al 18,8% sulle battute 9-10
#:     contro il 6,7% del corpus, QUASI IL TRIPLO, e proprio sulle corse;
#:   - il grado 3, la TERZA BLUES, stava all'1,7% contro l'8,3%;
#:   - i gradi 1, 6 e 8 erano a ZERO contro 3,7%, 5,0% e 4,2%.
#:
#: Un assolo di blues non cambia scala a ogni accordo: sta sulla tonica e usa
#: TUTTI E DODICI i gradi, con quelli fuori a bassa quota.

#: La quota misurata di ogni grado sulla tonica del pezzo `[MIS]`, da
#: `tools/misura_melodia.py`. E' il bersaglio della scelta delle note: non una
#: scala da cui pescare a caso, ma una distribuzione da rispettare.
GRADI_CORPUS = {
    0: 14.3,   # do   -- tonica
    1:  3.7,   # do#
    2:  9.8,   # re
    3:  8.3,   # mib  -- la terza blues
    4:  8.9,   # mi
    5: 10.8,   # fa
    6:  5.0,   # fa#
    7: 12.5,   # sol  -- quinta
    8:  4.2,   # lab
    9:  9.4,   # la
    10: 7.4,   # sib
    11: 5.6,   # si
}

#: La tonica del PEZZO, come classe di altezza. Fa.
TONICA = 5

#: Sui movimenti si preferisce una nota dell'accordo: e' li' che una nota
#: fuori si sente come un errore invece che come un passaggio.
PESO_ACCORDO = 3.0

#: La finestra dell'assolo, in numeri di nota MIDI: re4 - la5. Il tema sta
#: dentro do5 - fa5, quindi l'assolo ha piu' spazio sotto e sopra.
ASSOLO_MIN, ASSOLO_MAX = 62, 81
#: da dove parte il motivo la prima volta: fa4, la fondamentale
ASSOLO_PARTENZA = 65
SEME_ASSOLO = 8


def _peso(nota: int, sigla: str, forte: bool) -> float:
    """Quanto quella nota e' probabile qui, secondo il corpus.

    Il peso base e' la quota misurata di quel grado SULLA TONICA DEL PEZZO --
    non sulla fondamentale dell'accordo, che era l'errore della versione 02.
    Cosi' tutti e dodici i gradi sono disponibili, ognuno alla sua frequenza:
    la terza blues all'8,3%, il grado 11 al 5,6%, i cromatici sotto il 5%.

    ⚠️ Sui MOVIMENTI una nota dell'accordo pesa `PESO_ACCORDO` volte tanto. E'
    li' che una nota fuori si sente come un errore invece che come un
    passaggio, e senza questa distinzione la distribuzione giusta produrrebbe
    comunque una linea storta: non conta solo QUANTE volte una nota compare,
    ma DOVE.
    """
    p = GRADI_CORPUS[(nota - TONICA) % 12]
    if forte:
        fond, gradi = ACCORDI[sigla]
        if (nota - fond) % 12 in gradi:
            p *= PESO_ACCORDO
    return p


def assolo(giro_del_solista: list[str]) -> tuple:
    """Le dodici battute dell'assolo, sedici sedicesimi ciascuna.

    Non sceglie quante note ne' dove: quelle le dicono `DENSITA` e `SLOT`, che
    vengono dall'arco misurato. Sceglie QUALI, e lo fa camminando per gradi
    congiunti -- il 61% degli intervalli di un assolo vero sta entro 2
    semitoni -- pescando fra i vicini con la probabilita' misurata di ogni
    grado.
    """
    rng = random.Random(SEME_ASSOLO)
    fuori = []
    corrente = ASSOLO_PARTENZA
    direzione = 1

    for i, sigla in enumerate(giro_del_solista):
        battuta = i + 1
        d = DENSITA[i]
        pattern = SLOT_BATTUTA.get(battuta, SLOT[d])
        note = [None] * 16

        if battuta in ENUNCIAZIONI:
            # il motivo, alle stesse altezze ogni volta piu' la trasposizione
            base = ASSOLO_PARTENZA + ENUNCIAZIONI[battuta]
            passo = [0, 2, 4, 7, 5]          # i gradi di MOTIVO in semitoni
            posti = [k for k, c in enumerate(pattern) if c == 'x']
            for k, s in enumerate(posti):
                if k < len(passo):
                    note[s] = base + passo[k]
            corrente = base + passo[min(len(passo), len(posti)) - 1]
            fuori.append(tuple(note))
            continue

        for s, c in enumerate(pattern):
            if c != 'x':
                continue
            forte = s % 4 == 0                      # i quattro movimenti
            vicini = [n for n in range(corrente - 4, corrente + 5)
                      if ASSOLO_MIN <= n <= ASSOLO_MAX and n != corrente]
            avanti = [n for n in vicini
                      if (n - corrente) * direzione > 0] or vicini
            pesi = [_peso(n, sigla, forte) / (1 + abs(n - corrente)) ** 2
                    for n in avanti]
            scelta = rng.choices(avanti, weights=pesi, k=1)[0]
            note[s] = scelta
            corrente = scelta
            if corrente >= ASSOLO_MAX - 2 or corrente <= ASSOLO_MIN + 2 \
                    or rng.random() < 0.18:
                direzione = -direzione
        fuori.append(tuple(note))
    return tuple(fuori)


# --------------------------------------------------------------------------
# La batteria
# --------------------------------------------------------------------------

#: La voce nel PROFILO (mappa GM) e il drum nel KIT009 (un RX-5).
#: La voce si sceglie dai colpi e dalla posizione, mai dal nome -- ma su
#: QUESTA esecuzione il ride e' davvero il ride, e la mappa non inganna.
VOCI = {
    'ride':                'RIDE',
    'charleston a pedale': 'HATC',
    'kick':                'KICK',
    'rullante':            'SNARE',
    'tom medio-alto':      'TIMH',
    'tom basso':           'TIML',
}

#: I drum che restano nel kit. Gli altri si tolgono: cosi' le righe stanno
#: in una schermata e chi deve guardare le posizioni non scrolla.
TENUTI = tuple(VOCI.values())

#: Spang-a-lang: i sei passi su cui sta l'83% dei colpi di ride
#: dell'esecuzione (181 su 219). Il template ci mette sopra la forma
#: dinamica: 127 sui movimenti, 70 sulle crome swingate.
RIDE = 'x...x.x.x...x.x.'

#: Il piede sul 2 e sul 4. Velocity 55-56 dal template, e uno scarto di
#: -10,75 e -11,17 tick: e' la STRATIFICAZIONE misurata, ed e' la prima
#: volta che finisce dentro un pezzo invece che dentro una coppia di prova.
PEDALE = '....x.......x...'

#: Cassa rada. Il template da' 96 sul passo 0 e 86 sull'8 -- il feathering
#: -- e 118-127 sui passi 4 e 12, che sono le bombe.
CASSE = (
    'x.......x.......',   # solo il feathering
    'x.......x.....x.',   # con una bomba sul levare del 4
    'x.....x.x.......',   # con una bomba sul levare del 2
    'x.......x...x...',   # con la bomba sul 4
)
CASSA_PER_BATTUTA = (
    0, 0, 1, 0, 0, 2, 0, 3, 0, 1, 0, 0,
    0, 1, 0, 2, 0, 0, 3, 0, 0, 1, 0, 0,
    0, 2, 0, 0, 1, 0, 0, 3, 0, 0, 1, 0,
)

#: Comping di rullante, irregolare. Tutti i passi usati stanno nel profilo.
RULLANTI = (
    '................',   # tace
    '.......x....x...',
    '..........x.....',
    '....x.......x...',
    '.......x..x.....',
    '..........x...x.',
)
RULLANTE_PER_BATTUTA = (
    0, 1, 0, 2, 1, 0, 3, 0, 1, 2, 4, 0,
    2, 1, 4, 0, 1, 3, 2, 5, 1, 4, 2, 0,
    0, 1, 2, 0, 4, 1, 3, 0, 1, 2, 5, 0,
)

#: Il FILL, sulle battute 12 e 24 -- il turnaround. Casella 9: un fill dura
#: UNA battuta, sta sui 15,7 colpi, il ride cade dal 20,4% al 3,3% e i tom
#: salgono dal 9,9% al 29,0%, e NON e' piu' forte. `[MIS]` su 2 batteristi.
#: ⚠️ DOVE vada un fill il corpus non lo dice -- i fill sono file staccati.
#: Metterli sul turnaround e' una decisione, non una misura.
FILL_BATTUTE = (11, 23)          # indici da zero: le battute 12 e 24
FILL = {
    'RIDE':  '................',
    'HATC':  '....x.......x...',
    'KICK':  'x.......x.......',
    'SNARE': 'x.x.xxx.x.......',
    'TIMH':  '..........x.x...',
    'TIML':  '.............xx.',
}
#: ⚠️ I passi dei due tom NON sono scelti a orecchio: sono quelli che il
#: profilo di questa esecuzione copre davvero. La prima stesura ne usava due
#: che il batterista non ha mai suonato -- il 9 sul tom medio-alto e il 15 sul
#: basso -- e `applica_groove()` li ha riferiti in `senza_appoggio` invece di
#: inventarli. Quelli usati adesso poggiano su 15, 8, 5 e 10 colpi.


# --------------------------------------------------------------------------

def _spec_melodia(battute) -> str:
    """Da una tabella di numeri di nota MIDI alla stringa che `melodia()`
    legge. `None` diventa un punto, cioe' una pausa."""
    fuori = []
    for battuta in battute:
        for n in battuta:
            fuori.append('.' if n is None else MU.nome_altezza(n))
    return ' '.join(fuori)


def _spec_comping(giro_esteso: list[str]) -> str:
    """La progressione del comping: un gruppo per croma, separati da `|`.
    Un gruppo che e' un punto solo e' una pausa."""
    gruppi = []
    for battuta, ritmo in enumerate(COMPING):
        sigla = giro_esteso[battuta]
        # la battuta 12 del giro porta due accordi: Gm7 sulla prima meta'
        doppia = (battuta % 12) == 11
        for slot, c in enumerate(ritmo):
            if c != 'x':
                gruppi.append('.')
                continue
            corrente = sigla
            if doppia and sigla == 'Gm7' and slot >= 4:
                corrente = 'C7'
            gruppi.append(' '.join(MU.nome_altezza(n) for n in VOICING[corrente]))
    return ' | '.join(gruppi)


def _giro_esteso() -> list[str]:
    """Le 36 battute come sigle, una per battuta. La 12 di ogni giro porta
    Gm7 (e C7 sulla seconda meta', che `_spec_comping` gestisce). L'ULTIMA
    battuta del pezzo e' F7: il pezzo finisce, non gira."""
    fuori = []
    for _ in range(3):
        for casella in GIRO:
            fuori.append(casella.split('|')[0])
    fuori[-1] = 'F7'
    return fuori


def batteria(prof) -> list[tuple[str, list, dict]]:
    """Le righe di batteria, 36 battute, col template posato sopra."""
    per_drum: dict[str, list] = {d: [] for d in TENUTI}

    for battuta in range(BATTUTE):
        da = battuta * TICK_BATTUTA
        if battuta in FILL_BATTUTE:
            for drum, pattern in FILL.items():
                per_drum[drum].extend(MU.passi(pattern, da=da))
            continue
        per_drum['RIDE'].extend(MU.passi(RIDE, da=da))
        per_drum['HATC'].extend(MU.passi(PEDALE, da=da))
        per_drum['KICK'].extend(
            MU.passi(CASSE[CASSA_PER_BATTUTA[battuta]], da=da))
        rull = RULLANTI[RULLANTE_PER_BATTUTA[battuta]]
        if rull.strip('.'):
            per_drum['SNARE'].extend(MU.passi(rull, da=da))

    fuori = []
    for voce, drum in VOCI.items():
        note = per_drum[drum]
        if not note:
            continue
        rapporto = MU.applica_groove(note, prof, dove=voce)
        fuori.append((drum, note, rapporto))
    return fuori


def costruisci(prof):
    """La song intera. Ritorna (doc, rapporti)."""
    doc = parse_file(TEMPL)
    S.set_bpm(doc.root, BPM)
    S.set_swing(doc, SWING, figura='1/8')
    # fa misolidio: fa sol la sib do re mib, cioe' l'armonia di dominante
    # del blues. TEMPL0 arriva in re maggiore, che con questo pezzo non
    # c'entra: la scala non cambia le altezze scritte, cambia come il
    # dispositivo disegna la griglia -- ma lasciarla sbagliata e' informazione
    # falsa in un file, e `racconta()` la ripete.
    S.set_scale(doc, 'fa', 'misolidio')

    # la song di partenza porta roba sua: qui serve solo il pezzo
    for strumento in list(S.instruments(doc)):
        MU.togli(doc, strumento)

    rapporti = []
    giro = _giro_esteso()

    # --- batteria ---------------------------------------------------------
    kit, clip_kit = C.add_track(doc, KIT, name='KIT009', folder='KITS',
                                length=LUNGHEZZA, playing=True)
    for nome in [S.nome_drum(d) for d in S.drums(kit)]:
        if nome and nome not in TENUTI:
            K.remove_drum(doc, kit, nome)
    for drum, note, rapporto in batteria(prof):
        rapporti.append(rapporto)
        rapporti.append(MU.scrivi(doc, clip_kit, note, dove=drum))

    # --- basso walking ----------------------------------------------------
    _, clip_basso = C.add_track(doc, PRESET_BASSO, name='Square Saw Bass',
                                folder='SYNTHS', length=LUNGHEZZA,
                                playing=True)
    linea = walking(giro)
    spec = ' '.join(MU.nome_altezza(n) for n in linea)
    note = MU.melodia(spec, durata='1/4', articolazione='staccato',
                      velocity=78)
    rapporti.append(MU.scrivi(doc, clip_basso, note))

    # --- comping ----------------------------------------------------------
    _, clip_comping = C.add_track(doc, PRESET_COMPING, name='Pianism I',
                                  folder='SYNTHS', length=LUNGHEZZA,
                                  playing=True)
    note = MU.accordi(_spec_comping(giro), durata='1/8',
                      articolazione='staccato', velocity=72)
    rapporti.append(MU.scrivi(doc, clip_comping, note))

    # --- tema e assolo ----------------------------------------------------
    _, clip_tema = C.add_track(doc, PRESET_TEMA, name='062 Trumpet',
                               folder='SYNTHS', length=LUNGHEZZA,
                               playing=True)
    # ⚠️ TRE CHIAMATE E NON UNA, ed e' la ragione per cui `da=` esiste.
    # `melodia()` applica UNA durata a tutta la stringa: dalla versione 03
    # l'assolo e' in sedicesimi e il tema no, e passarli insieme
    # dimezzerebbe la lunghezza di ogni nota del tema senza che nessuno se ne
    # accorga. Il tema resta in crome, l'assolo va in sedicesimi, e le tre
    # parti si uniscono per altezza -- che e' la forma in cui il Deluge tiene
    # le righe di una clip.
    ultimo = list(TEMA_NOTE[:-1]) + [TEMA_CHIUSA]
    parti = (
        MU.melodia(_spec_melodia(TEMA_NOTE), durata='1/8',
                   da=0, velocity=95),
        MU.melodia(_spec_melodia(assolo(giro[12:24])), durata='1/16',
                   da=12 * TICK_BATTUTA, velocity=95),
        MU.melodia(_spec_melodia(ultimo), durata='1/8',
                   da=24 * TICK_BATTUTA, velocity=95),
    )
    note = {}
    for parte in parti:
        for altezza, ns in parte.items():
            note.setdefault(altezza, []).extend(ns)
    rapporti.append(MU.scrivi(doc, clip_tema, note))

    return doc, rapporti


def main() -> int:
    mancanti = [p for p in (TEMPL, KIT, PRESET_BASSO, PRESET_COMPING,
                            PRESET_TEMA, BASE_GROOVE,
                            TABELLA) if not p.exists()]
    if mancanti:
        for p in mancanti:
            print(f'manca: {p}')
        return 1

    prof = GR.profilo(BASE_GROOVE, ESECUZIONE)
    print(f'template: {prof.id}  {prof.style}  {prof.bpm} BPM  '
          f'BUR {prof.bur:.2f}  {prof.battute} battute')

    doc, rapporti = costruisci(prof)

    print('\n--- rapporti (regola 4) ---')
    for r in rapporti:
        print(f'  {r}')

    problemi = MU.verifica(doc)
    if problemi:
        print('\n⚠️ verifica() NON e\' vuota: non si carica.')
        for p in problemi:
            print(f'  {p}')
        return 1
    print('\nverifica(): vuota')

    avvisi = MU.avvertenze(doc)
    print(f'avvertenze(): {avvisi if avvisi else "nessuna"}')

    remoto = MU.destinazione('jazz', VERSIONE)
    locale = RADICE / 'out' / Path(remoto).name
    write_file(doc, locale, FormatTable.load(TABELLA))
    print(f'\nscritto {locale}')
    print(f'destinazione: {remoto}')

    print('\n--- racconta() ---')
    print(MU.racconta(doc))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
