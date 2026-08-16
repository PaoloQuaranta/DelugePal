"""Dai valori esadecimali alle unita' che si leggono sul display.

Il Deluge scrive i parametri di suono come int32 esadecimali: `volume="0x4CCCCCA8"`,
`lpfFrequency="0x1999997E"`. Sul dispositivo gli stessi parametri si leggono
come numeri da 0 a 50. Questo modulo fa la conversione nei due sensi.

DUE GRIGLIE, NON UNA
--------------------
Il display mostra 0-50 — confermato da chi usa il dispositivo, ed e' la scarsa
risoluzione per cui il firmware ufficiale veniva criticato. Ma internamente si
lavora piu' fine, e nei file convivono due griglie.

**Storica**, 50 gradini su tutto l'int32:

    valore_senza_segno = display * 85899345          85899345 = 2^32 // 50

Uguaglianza esatta in aritmetica intera, non una regressione: su 183 101
valori del corpus il 56.7% la soddisfa al byte.

**Interna**, 128 gradini — quella che scrive il firmware community:

    valore_senza_segno = interno * 33554432          33554432 = 2^32 // 128
    display            = round(interno * 50 / 128)

VERIFICATA SUL DISPOSITIVO: il volume di un synth portato a 35 sullo schermo
ha prodotto `0x34000000`, cioe' interno 90, e round(90 * 50/128) = 35. NON
`0x33333313`, che e' quello che darebbe la griglia storica. Per questo
`from_display()` passa dalla griglia interna: un file generato deve somigliare
a quello che scriverebbe il firmware di oggi, non a quello di cinque anni fa.

Conseguenza da tenere a mente: **passare per il display perde risoluzione**,
perche' 129 valori interni si schiacciano su 51 mostrati. Chi vuole la piena
risoluzione usa `internal_of()` e `from_internal()`, che sono byte-esatti.

Valori speciali, fuori da entrambe le griglie:

    0x80000000   display  0   (minimo)
    0x00000000   display 25   (centro: il dispositivo scrive lo zero esatto)
    0x7FFFFFFF   display 50   (massimo, saturato all'int32)

COSA NON COPRE
--------------
Il 4.1% restante. Attenzione a come va letto: **non sono certi attributi a
essere fuori scala, sono certi VALORI.** Lo stesso `lpfFrequency` sta sulla
griglia in una song e fuori in un'altra — perche' un valore puo' arrivare da
un'automazione o da una regolazione fine, non da uno dei 51 gradini del menu.
Quindi non esiste una lista di attributi da escludere, e chi cerchi di
scriverla si accorgera' che non chiude.

Due scale diverse sono invece identificate:

- `patchCable/amount` — modulazioni CON SEGNO; il file lo dichiara da se' con
  `polarity="bipolar"`. Scala non ancora fissata: il MCD dei valori osservati
  e' 1, quindi non stanno su una griglia sola
- `pan` — griglia di **128** passi invece di 50: il MCD dei suoi valori fuori
  griglia e' esattamente 0x02000000 = 2^32/128. E' il livello "0-128 interno"
  di cui parla HANDOFF §7

Per tutto cio' che non cade sulla griglia `to_display()` ritorna **None**
invece di un numero approssimato. E' la scelta importante di questo modulo:
"circa 27" nasconderebbe che la domanda e' mal posta, e questo progetto ha gia'
pagato caro il costo delle risposte plausibili e sbagliate.

DA VERIFICARE SUL DISPOSITIVO
-----------------------------
Che il display mostri davvero 0-50 con questa corrispondenza e' dedotto dai
file, non ancora letto sullo schermo. Basta una prova: mettere un parametro a
un valore noto, salvare, e leggere l'esadecimale.
"""
from __future__ import annotations

SPAN = 1 << 32
HALF = 1 << 31
DISPLAY_MAX = 50

#: griglia "storica": 50 gradini su tutto l'int32. Domina il corpus.
STEP = SPAN // 50           # 85899345 = 0x051EB851

#: griglia interna a 128 gradini, quella che scrive il firmware community.
#: Verificata sul dispositivo: volume portato a 35 sul display -> 0x34000000,
#: cioe' 90 * STEP_INTERNO - 2^31, e round(90 * 50/128) = 35.
INTERNI = 128                       # quanti valori, non l'indice massimo
INTERNO_MAX = INTERNI - 1           # 127: oltre, il valore rientra sul minimo
STEP_INTERNO = SPAN // INTERNI      # 33554432 = 0x02000000

#: valori che il firmware scrive come costanti, fuori da entrambe le griglie
SPECIALI = {
    0x80000000: 0,
    0x00000000: 25,
    0x7FFFFFFF: 50,
}


def _raw(hexval: str) -> int | None:
    if not (isinstance(hexval, str) and hexval.startswith('0x')
            and len(hexval) == 10):
        return None
    try:
        return int(hexval, 16)
    except ValueError:
        return None


def to_display(hexval: str) -> int | None:
    """Il valore 0-50 mostrato dal dispositivo, o None se non e' sulla griglia.

    Ritornare None invece di un numero approssimato e' voluto: un parametro
    bipolare o automatizzato NON si legge con questa scala, e restituire
    "circa 27" nasconderebbe il fatto che la domanda e' mal posta.
    """
    raw = _raw(hexval)
    if raw is None:
        return None
    if raw in SPECIALI:
        return SPECIALI[raw]
    shifted = (raw + HALF) % SPAN

    # griglia storica: 50 gradini, il valore E' gia' il numero del display
    q, r = divmod(shifted, STEP)
    if r == 0 and 0 <= q <= DISPLAY_MAX:
        return q

    # griglia interna a 128: il display e' una riduzione del valore interno
    q, r = divmod(shifted, STEP_INTERNO)
    if r == 0 and 0 <= q <= INTERNI:
        return round(q * DISPLAY_MAX / INTERNI)

    return None


def internal_of(hexval: str) -> int | None:
    """Il valore interno 0-128, che ha piu' risoluzione di quello a display.

    Serve quando i 51 gradini non bastano: la scarsa risoluzione era una delle
    critiche piu' frequenti al firmware ufficiale, e quello community la
    supera lavorando internamente piu' fine di quanto lo schermo mostri.
    """
    raw = _raw(hexval)
    if raw is None:
        return None
    shifted = (raw + HALF) % SPAN
    q, r = divmod(shifted, STEP_INTERNO)
    return q if r == 0 and 0 <= q <= INTERNI else None


def from_display(value: int) -> str:
    """L'esadecimale che il firmware community scrive per questo valore 0-50.

    Passa dalla griglia interna a 128, che e' cio' che fa il dispositivo:
    verificato portando il volume di un synth a 35, che ha prodotto
    0x34000000 = interno 90, e non 0x33333313 come darebbe la griglia a 50.

    I valori speciali vengono riprodotti alla lettera, cosi' un file generato
    resta indistinguibile da uno scritto dal Deluge.
    """
    if not 0 <= value <= DISPLAY_MAX:
        raise ValueError(f'valore {value} fuori dalla scala 0-{DISPLAY_MAX}')
    value = int(value)
    for raw, disp in SPECIALI.items():
        if disp == value:
            return f'0x{raw:08X}'
    return from_internal(round(value * INTERNI / DISPLAY_MAX))


def from_internal(value: int) -> str:
    """L'esadecimale per un valore interno 0-127, a piena risoluzione.

    Il massimo e' 127, non 128: i valori sono 128 e partono da zero. Passare
    128 farebbe rientrare il risultato su 0x80000000, cioe' sul MINIMO, con un
    wrap-around silenzioso — una rampa che finisce a fondo scala invece che in
    cima. Meglio un errore.
    """
    if not 0 <= value <= INTERNO_MAX:
        raise ValueError(f'valore interno {value} fuori da 0-{INTERNO_MAX} '
                         f'({INTERNI} valori a partire da zero)')
    return f'0x{(int(value) * STEP_INTERNO - HALF) % SPAN:08X}'


# ------------------------------------------------- i patch cable (modulazioni)

#: fondoscala di un patch cable: display +50. Il formato permetterebbe il
#: doppio, ma dal menu non si va oltre — nel corpus, su 15 372 valori,
#: NESSUNO supera questo limite e cinque ci stanno esattamente sopra.
CABLE_MAX_RAW = 1 << 30                 # 0x40000000
CABLE_DISPLAY_MAX = 50


def cable_to_display(hexval: str) -> float | None:
    """La profondita' di modulazione come la mostra il dispositivo, -50..+50.

        display = amount * 100 / 2^31

    Misurato: `lfo1 -> modulator1Volume` portato a 30 ha prodotto
    `0x26666666` = round(0.3 * 2^31). Il range mostrato e' BIPOLARE, quindi
    +50 cade a 0x40000000, cioe' meta' dell'int32.

    Ritorna un float, non un intero: la risoluzione interna e' molto piu' fine
    di quella dello schermo, quindi arrotondare qui butterebbe via
    informazione che il chiamante potrebbe volere. Sul corpus solo lo 0.67%
    dei valori corrisponde a un display intero — gli altri vengono da
    regolazioni fini, non dal menu.

    ATTENZIONE: `amount` non e' sempre un int32. Puo' contenere
    un'AUTOMAZIONE, cioe' una sequenza impacchettata lunga anche 1000
    caratteri. Qui viene rifiutata con None invece di essere letta come numero.
    """
    raw = _raw(hexval)
    if raw is None:
        return None
    s = raw - SPAN if raw >= HALF else raw
    if abs(s) > CABLE_MAX_RAW:
        return None                     # fuori dal fondoscala: non e' un cable
    return s * 100 / HALF


def cable_from_display(value: float) -> str:
    """L'esadecimale per una profondita' di modulazione -50..+50."""
    if not -CABLE_DISPLAY_MAX <= value <= CABLE_DISPLAY_MAX:
        raise ValueError(f'profondita {value} fuori da '
                         f'-{CABLE_DISPLAY_MAX}..+{CABLE_DISPLAY_MAX}')
    return f'0x{round(value * HALF / 100) % SPAN:08X}'


def is_on_grid(hexval: str) -> bool:
    """Il valore e' esprimibile nella scala 0-50?"""
    return to_display(hexval) is not None
