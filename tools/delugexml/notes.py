"""Codifica/decodifica dei blob di note delle noteRow.

Layout ricavato empiricamente (vedi docs/FINDINGS.md, §note):

  noteDataWithLift       11 byte per nota
  noteDataWithSplitProb  14 byte per nota  (= gli stessi 11 + 3)

    byte 0-3   posizione in tick, uint32 big-endian
    byte 4-7   durata in tick,    uint32 big-endian
    byte 8     velocity           1..127   (osservato)
    byte 9     lift               0..127   (osservato)
    byte 10    condizione/probabilita'     (osservato 1..140; 20 = 100%,
               presente in 10386/10511 note del corpus. I valori >=128
               sono le condizioni "iteration dependence" del vecchio formato.)
    byte 11    (solo WithSplitProb) divisore dell'iterance, 1..8
    byte 12    (solo WithSplitProb) maschera dei passi attivi
    byte 13    (solo WithSplitProb) sempre 0 nel corpus; presumibilmente fill

Iterance, byte 11 e 12
----------------------
Il changelog c1.3.0 dice che una nota porta velocity, probability, lift,
ITERANCE e FILL, e che l'iterance CUSTOM ha un divisore da 1 a 8 con i singoli
passi attivabili. Il nome stesso dell'attributo — "WithSplitProb" — dice che la
probabilita' e' stata separata da cio' con cui prima divideva un byte.

Predizione verificata sul corpus: ogni bit acceso nella maschera deve stare
sotto il divisore (non ha senso attivare il passo 5 su un divisore di 4).
**76 note su 76 coerenti, zero eccezioni.** Le coppie osservate si leggono da
sole: (4, 0b1000) = "4 di 4", (8, 0b10000000) = "8 di 8", (2, 0b01) = "1 di 2".
Nel corpus la maschera ha sempre un solo bit acceso, cioe' la forma classica
"N di M"; il modo CUSTOM con piu' bit e' previsto dal firmware ma non usato qui.

Le larghezze 11 e 14 sono confermate su 3628 noteRow / oltre 10000 note:
sono le uniche per cui le posizioni risultano ovunque strettamente crescenti.
"""
from __future__ import annotations

from dataclasses import dataclass, field

PROB_100 = 20          # valore osservato per "probabilita' 100%"
DEFAULT_VELOCITY = 64
DEFAULT_LIFT = 64

ATTR_WIDTH = {
    'noteDataWithLift': 11,
    'noteDataWithSplitProb': 14,
    'noteData': 10,        # formato piu' vecchio, non presente in c1.3.0
}


@dataclass
class Note:
    pos: int
    length: int
    velocity: int = DEFAULT_VELOCITY
    lift: int = DEFAULT_LIFT
    condition: int = PROB_100
    #: divisore dell'iterance (0 = disattivata, 1..8 osservati)
    iterance_divisor: int = 0
    #: maschera dei passi attivi; il bit k accende il passo k+1
    iterance_steps: int = 0
    #: byte 13, sempre 0 nel corpus. Conservato senza interpretarlo.
    fill: int = 0

    @property
    def iterance(self) -> str | None:
        """L'iterance nella notazione del dispositivo, es. "3of4"."""
        if not self.iterance_divisor:
            return None
        steps = [k + 1 for k in range(8) if self.iterance_steps >> k & 1]
        if len(steps) == 1:
            return f'{steps[0]}of{self.iterance_divisor}'
        return f'{"+".join(map(str, steps))}of{self.iterance_divisor}'

    def __repr__(self):
        bits = [f'pos={self.pos}', f'len={self.length}',
                f'vel={self.velocity}', f'lift={self.lift}']
        if self.condition != PROB_100:
            bits.append(f'cond={self.condition}')
        if self.iterance:
            bits.append(f'iter={self.iterance}')
        if self.fill:
            bits.append(f'fill={self.fill}')
        return 'Note(' + ' '.join(bits) + ')'


def decode(blob: str, width: int) -> list[Note]:
    h = blob[2:] if blob.lower().startswith('0x') else blob
    raw = bytes.fromhex(h)
    if width and len(raw) % width:
        raise ValueError(f'blob di {len(raw)} byte non divisibile per {width}')
    out = []
    for i in range(0, len(raw), width):
        r = raw[i:i + width]
        out.append(Note(
            pos=int.from_bytes(r[0:4], 'big'),
            length=int.from_bytes(r[4:8], 'big'),
            velocity=r[8],
            lift=r[9],
            # `noteData`, il formato piu' vecchio, e' largo 10 byte e finisce
            # qui: pos, length, velocity, lift e basta. Leggerlo come se avesse
            # il byte di condition faceva esplodere qualunque file di quel
            # formato — e ce ne sono, 1850 righe nel corpus.
            condition=r[10] if width > 10 else PROB_100,
            iterance_divisor=r[11] if width > 11 else 0,
            iterance_steps=r[12] if width > 12 else 0,
            fill=r[13] if width > 13 else 0,
        ))
    return out


def encode(notes: list[Note], width: int) -> str:
    out = bytearray()
    for n in sorted(notes, key=lambda x: x.pos):
        out += n.pos.to_bytes(4, 'big')
        out += n.length.to_bytes(4, 'big')
        out += bytes([n.velocity & 0xFF, n.lift & 0xFF, n.condition & 0xFF])
        extra = [n.iterance_divisor & 0xFF, n.iterance_steps & 0xFF,
                 n.fill & 0xFF]
        pad = width - 11
        if pad > 0:
            out += bytes(extra[:pad]) + bytes(max(0, pad - len(extra)))
    return '0x' + out.hex().upper()


def read_row(node) -> tuple[str, int, list[Note]] | None:
    """(nome_attributo, larghezza, note) per una noteRow, o None se e' vuota."""
    for attr, w in ATTR_WIDTH.items():
        v = node.get(attr)
        if v:
            return attr, w, decode(v, w)
    return None


#: attributi da creare su una riga nuova. Nel corpus 1783 righe portano
#: entrambi e 62 solo noteDataWithSplitProb; nessuna ha solo WithLift.
#: Scriviamo entrambi, che e' il caso dominante.
NEW_ROW_ATTRS = ('noteDataWithSplitProb', 'noteDataWithLift')


def write_row(node, notes: list[Note], create: bool = False) -> None:
    """Riscrive TUTTI gli attributi di note presenti sulla noteRow.

    Una noteRow puo' portare sia noteDataWithLift sia noteDataWithSplitProb:
    devono restare coerenti, altrimenti il firmware legge una delle due e
    l'altra resta a raccontare una storia diversa.

    Con create=True, su una riga che non ne ha ancora li crea entrambi.
    Senza, solleva un errore: aggiungere note a una riga vuota e' una cosa
    diversa dal modificarne una esistente, ed e' meglio doverlo dire.
    """
    if not notes:
        # Una riga senza note non porta attributi di note: nel corpus le 1901
        # righe vuote non ne hanno nessuno. Scrivere un blob vuoto ("0x")
        # sarebbe una forma che il firmware non produce mai, quindi si
        # rimuovono del tutto.
        for attr in ATTR_WIDTH:
            if node.has(attr):
                node.remove(attr)
        node.self_closing = not node.children
        return

    touched = False
    for attr, w in ATTR_WIDTH.items():
        if node.has(attr):
            node.set(attr, encode(notes, w))
            touched = True
    if touched:
        return
    if not create:
        # una riga vuota non ha NESSUN attributo di note: e' la forma che usa
        # il firmware, ed e' la norma sui kit, dove esistono tutte e 16 le
        # righe anche se solo due suonano. Identificarla per y qui sarebbe
        # fuorviante: su un kit la chiave e' drumIndex.
        chiave = ('drumIndex', node.get('drumIndex')) \
            if node.has('drumIndex') else ('y', node.get('y'))
        raise ValueError(
            f'<noteRow {chiave[0]}={chiave[1]}> non ha attributi di note '
            '(riga vuota). Usa create=True per aggiungerli.')
    for attr in NEW_ROW_ATTRS:
        node.set(attr, encode(notes, ATTR_WIDTH[attr]))
