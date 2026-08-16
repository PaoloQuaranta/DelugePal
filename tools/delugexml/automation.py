"""Le automazioni: un parametro che cambia nel tempo.

Un parametro automatizzato non porta piu' un int32 ma una sequenza
impacchettata nello STESSO attributo:

    lpfFrequency="0x7FFFFFFF"                        <- valore fisso
    lpfFrequency="0x80000000 80000000 00000000 …"    <- automazione (senza spazi)

FORMATO
-------
Confermato sul sorgente del firmware, `src/deluge/modulation/automation/
auto_param.cpp`, branch `community` — non dedotto:

    writer.write("0x"); intToHex(valueNow);        <- intestazione
    per ogni nodo:  intToHex(node->value);
                    pos = node->pos;
                    if (node->interpolated) pos |= (1 << 31);
                    intToHex(pos);

Quindi, in parole da 32 bit esadecimali maiuscole senza separatori:

    [valueNow] (valore, posizione) (valore, posizione) …

- **una** parola di intestazione — e' il VALORE CORRENTE del parametro, non un
  conteggio. Il numero di parole e' quindi dispari, ed e' il modo piu' rapido
  per riconoscere il formato
- `valore` e' un int32 come quelli fissi, quindi si legge con `params.py`
- `posizione` e' in tick, ma il **bit 31 e' il flag di INTERPOLAZIONE**, non
  parte della posizione: va mascherato prima di usarla

Sempre dal sorgente, cosa rende un parametro automatizzato:

    «a parameter is considered automated when nodes.getNumElements() > 0»

cioe' basta la presenza di nodi. Non esiste nessun flag separato da attivare.

Ricavato da un'automazione disegnata sul dispositivo e decodificata contro
una forma nota in anticipo — mezza battuta di rampa in salita e mezza in
discesa. Il decoder ha restituito esattamente quel triangolo:

    display  0  7 14 21 29 36 43 50 | 50 43 36 29 21 14  7  0
    tick     0 24 48 72 96 120 144 168   216 240 264 288 312 336 360

[OSS] Cosa sia l'intestazione non e' dimostrato. Nell'unico esemplare vale
`0x80000000` ed e' uguale al primo valore, il che suggerisce "valore corrente"
o "valore di partenza", ma un solo campione non decide. Viene conservata e
riemessa tale e quale, mai reinterpretata.
"""
from __future__ import annotations

from typing import NamedTuple

PAROLA = 8                      # cifre esadecimali per parola da 32 bit


BIT_INTERPOLAZIONE = 1 << 31


class Punto(NamedTuple):
    """Un nodo dell'automazione."""
    pos: int                    # tick, senza il bit di interpolazione
    raw: int                    # valore int32 senza segno, come nel file
    interp: bool = False        # bit 31 della parola di posizione

    @property
    def hex(self) -> str:
        return f'0x{self.raw:08X}'

    @property
    def pos_word(self) -> int:
        """La parola di posizione come sta nel file, flag compreso."""
        return self.pos | BIT_INTERPOLAZIONE if self.interp else self.pos


def is_automation(value: str) -> bool:
    """L'attributo contiene una sequenza invece di un valore singolo?

    Serve a chiunque legga parametri: convertire un'automazione come se fosse
    un numero produce risultati plausibili e sbagliati. E' gia' successo.
    """
    if not (isinstance(value, str) and value.startswith('0x')):
        return False
    corpo = value[2:]
    return len(corpo) > PAROLA and len(corpo) % PAROLA == 0


def decode(value: str) -> tuple[int, list[Punto]]:
    """(intestazione, punti) da un attributo automatizzato."""
    if not is_automation(value):
        raise ValueError(f'{value[:24]}… non e un automazione')
    corpo = value[2:]
    parole = [int(corpo[i:i + PAROLA], 16)
              for i in range(0, len(corpo), PAROLA)]
    if len(parole) % 2 != 1:
        raise ValueError(f'attese parole in numero dispari '
                         f'(1 intestazione + coppie), trovate {len(parole)}')
    testa, resto = parole[0], parole[1:]
    punti = []
    for i in range(0, len(resto), 2):
        parola_pos = resto[i + 1]
        punti.append(Punto(pos=parola_pos & ~BIT_INTERPOLAZIONE,
                           raw=resto[i],
                           interp=bool(parola_pos & BIT_INTERPOLAZIONE)))
    return testa, punti


def encode(testa: int, punti: list[Punto]) -> str:
    """L'attributo per questa automazione.

    I punti vengono riordinati per posizione: il dispositivo li scrive in
    ordine, e una sequenza disordinata non e' mai stata osservata.
    """
    parole = [testa]
    for p in sorted(punti, key=lambda x: x.pos):
        parole.append(p.raw)
        parole.append(p.pos_word)
    return '0x' + ''.join(f'{w:08X}' for w in parole)


SPAN = 1 << 32
HALF = 1 << 31

#: Coordinate della scorciatoia sulla griglia. **NON SONO NECESSARIE**:
#: verificato sul dispositivo generando automazioni per `pan` e
#: `reverbAmount` senza scriverle — funzionano lo stesso. Si conservano solo
#: dove osservate, per somigliare a cio' che scrive il firmware.
SCORCIATOIE = {'lpfFrequency': ('8', '7'), 'arpeggiatorGate': ('11', '2')}

#: Valori che accompagnano lo stato di vista e che nell'unico esemplare
#: osservato erano questi. Non e' chiaro cosa rappresentino oltre al nome.
VISTA_FISSI = {
    'onAutomationInstrumentClipView': '1',
    'lastSelectedInstrumentType': '0',
    'lastSelectedPatchSource': '15',
}


def mark_view(doc, clip, param: str) -> dict[str, str]:
    """Rende visibile sul dispositivo l'automazione appena scritta.

    Da chiamare DOPO aver scritto il blob. Fa due cose, e servono entrambe:

    1. segna sulla clip che la vista automazione riguarda `param`
    2. rende quella clip la clip APERTA (`beingEdited`), perche' altrimenti il
       dispositivo ne apre un'altra e l'automazione, pur corretta, non si vede

    Il punto 2 non era ovvio e ha richiesto una bisezione sul dispositivo:
    erano stati esclusi prima l'ordine degli attributi e i nodi `<bendRange>`,
    che non c'entravano.
    """
    from . import song as S                             # import locale: ciclo
    from . import param_ids as PI                       # noqa: PLC0415

    p = PI.by_name(param)                # solleva se il nome non e' in tabella
    attrs = dict(VISTA_FISSI)
    attrs['lastSelectedParamID'] = str(p.id)
    attrs['lastSelectedParamKind'] = str(p.kind)
    sc = SCORCIATOIE.get(param)
    if sc is not None:
        attrs['lastSelectedParamShortcutX'] = sc[0]
        attrs['lastSelectedParamShortcutY'] = sc[1]

    for k, v in attrs.items():
        clip.set(k, v)
    S.set_edited_clip(doc, clip)
    return attrs


def ramp(da: int, a: int, inizio: int, fine: int, passi: int,
         testa: int | None = None) -> tuple[int, list[Punto]]:
    """Una rampa lineare fra due valori int32, a passi regolari.

    `da` e `a` sono valori grezzi: si ottengono da `params.from_display()` o
    `params.from_internal()`.

    L'interpolazione avviene nello spazio TRASLATO di 2^31, non su quello
    grezzo. Interpolare i valori senza segno sarebbe sbagliato: il minimo e'
    0x80000000 e il massimo 0x7FFFFFFF, quindi una retta fra i due passa dalla
    parte sbagliata del wrap-around e produce una rampa che scende invece di
    salire. Nello spazio traslato il minimo e' 0 e il massimo 2^32-1, cioe'
    l'ordine e' quello che si vede sul display.
    """
    if passi < 2:
        raise ValueError('servono almeno due punti per una rampa')
    da_s = (da + HALF) % SPAN
    a_s = (a + HALF) % SPAN
    punti = []
    for i in range(passi):
        f = i / (passi - 1)
        pos = round(inizio + (fine - inizio) * f)
        raw = (round(da_s + (a_s - da_s) * f) - HALF) % SPAN
        punti.append(Punto(pos=pos, raw=raw))
    return (da if testa is None else testa), punti


def ramp_internal(da: int, a: int, inizio: int, fine: int, passi: int,
                  testa: int | None = None) -> tuple[int, list[Punto]]:
    """Una rampa espressa in unita' interne 0-128, che e' come si autora.

    Differenza pratica da `ramp()`: qui i punti cadono TUTTI sulla griglia
    interna, quindi restano leggibili con `params.to_display()`. Interpolando
    invece verso il massimo saturato 0x7FFFFFFF si ottengono punti intermedi
    fuori griglia, perche' quel valore non e' un multiplo esatto del passo.

    E' anche cio' che fa il dispositivo: nell'automazione misurata i valori
    erano 0, 18, 37, 55, 73, 91, 110 — tutti sulla griglia — e solo il picco
    era 0x7FFFFFFF.
    """
    from . import params as P                            # import locale: ciclo

    if passi < 2:
        raise ValueError('servono almeno due punti per una rampa')
    if not (0 <= da <= P.INTERNO_MAX and 0 <= a <= P.INTERNO_MAX):
        raise ValueError(f'valori interni fuori da 0-{P.INTERNO_MAX}: '
                         f'{da}, {a}')
    punti = []
    for i in range(passi):
        f = i / (passi - 1)
        pos = round(inizio + (fine - inizio) * f)
        interno = round(da + (a - da) * f)
        punti.append(Punto(pos=pos, raw=int(P.from_internal(interno), 16)))
    testa_raw = int(P.from_internal(da), 16) if testa is None else testa
    return testa_raw, punti
