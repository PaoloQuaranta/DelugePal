"""Leggere Standard MIDI File e tradurli nelle forme che `musica` gia' usa.

PERCHE' ESISTE
--------------
Fino al 16 agosto 2026 il progetto aveva deciso di NON leggere MIDI, e la
skill lo diceva: «i suoi `scripts/*.py` producono file MIDI e non si usano
qui». La decisione e' stata riaperta dall'utente, con due ragioni che valgono
piu' del costo:

  1. **meta' di `music-composer` produce MIDI** — `generate_melody.py`,
     `generate_chords.py`, `generate_drums.py`. Senza leggerlo, meta' della
     skill e' inservibile.
  2. **il materiale libero e' quasi tutto MIDI**: librerie di loop di batteria
     divise per genere, e soprattutto i **groove template**, che sono file
     MIDI ordinari — portano il timing e le velocity di un groove suonato,
     cioe' esattamente cio' che la prosa sui generi descrive a parole e non
     mostra mai.

PERCHE' SCRITTO A MANO E NON CON `mido`
---------------------------------------
`mido` c'e', ma **solo nel `.venv`** (che esiste per il SysEx). I test girano
con il Python di sistema (`python tests/test_all.py`), dove mido NON c'e':
un modulo di libreria che lo importasse avrebbe test non eseguibili dalla
suite. Lo Standard MIDI File e' un formato piccolo, fermo dal 1988 e senza
le patologie dell'XML del Deluge, quindi il costo di leggerlo qui e' basso.
E' lo stesso ragionamento che ha prodotto il parser XML su misura.

IL PUNTO CHE POTEVA ESSERE UN DISASTRO E NON LO E'
--------------------------------------------------
Le altezze **coincidono**. `musica.altezza('do4')` vale 60, `do-1` vale 0,
`sol9` vale 127; il do centrale MIDI e' 60. Quindi **il numero di nota MIDI
e' gia' la `y` del Deluge**, senza nessuno scarto di ottava — e anche
`music-composer` usa la stessa convenzione (`NOTE_NAMES[n] + (octave+1)*12`).
Verificato prima di scrivere una riga: era il candidato numero uno a errore
silenzioso, del tipo "tutto funziona ma suona un'ottava sotto".

Attenzione invece a quello che NON coincide: il **tempo in tick**. Un MIDI ha
i suoi PPQ (spesso 96, 480 o 960), il Deluge ha `24 x 2^inputTickMagnitude`
per movimento — 96 con la RESOLUTION di default. Quando i due non sono in
rapporto intero le posizioni si **arrotondano**, e li' se ne va proprio la
micro-tempistica che rende utile un groove template. Per questo la
conversione **dichiara quanto ha arrotondato** invece di tacere.
"""
from __future__ import annotations

import struct
from pathlib import Path
from typing import NamedTuple

from .notes import Note

#: Quanti tick per movimento ha il Deluge con la RESOLUTION di default
#: (`inputTickMagnitude="2"`). E' anche cio' che `musica` da' per scontato.
TICK_PER_MOVIMENTO_DELUGE = 96

#: Il canale della batteria in General MIDI, contato da 0 (il "canale 10").
CANALE_BATTERIA = 9


class NotaMidi(NamedTuple):
    """Una nota come sta nel file MIDI: posizioni in tick MIDI."""
    pos: int
    length: int
    y: int                      # numero di nota MIDI = y del Deluge
    velocity: int
    canale: int


class Traccia(NamedTuple):
    indice: int
    nome: str | None
    note: list[NotaMidi]

    @property
    def canali(self) -> tuple[int, ...]:
        return tuple(sorted({n.canale for n in self.note}))

    @property
    def e_batteria(self) -> bool:
        return CANALE_BATTERIA in self.canali


class FileMidi(NamedTuple):
    formato: int
    ppq: int
    bpm: float | None
    metro: tuple[int, int] | None
    tracce: list[Traccia]

    @property
    def note(self) -> list[NotaMidi]:
        return [n for t in self.tracce for n in t.note]


# ------------------------------------------------------------- lettura grezza

def _vlq(dati: bytes, i: int) -> tuple[int, int]:
    """Variable Length Quantity: 7 bit per byte, il bit alto dice "continua"."""
    valore = 0
    for _ in range(4):
        b = dati[i]
        i += 1
        valore = (valore << 7) | (b & 0x7F)
        if not b & 0x80:
            return valore, i
    raise ValueError('VLQ piu lungo di 4 byte: file corrotto')


def _chunks(dati: bytes):
    i = 0
    while i + 8 <= len(dati):
        tipo = dati[i:i + 4]
        (lung,) = struct.unpack('>I', dati[i + 4:i + 8])
        yield tipo, dati[i + 8:i + 8 + lung]
        i += 8 + lung


def _eventi_traccia(dati: bytes, indice: int) -> tuple[Traccia, float | None,
                                                       tuple[int, int] | None]:
    """Gli eventi di una MTrk, gia' accoppiati in note.

    Accoppia note-on e note-off tenendo una pila per (canale, altezza): due
    note uguali sovrapposte sono legali in MIDI, e chiuderle in ordine
    sbagliato darebbe durate assurde.
    """
    i = 0
    ora = 0
    stato = None                       # running status
    aperte: dict[tuple[int, int], list[tuple[int, int]]] = {}
    note: list[NotaMidi] = []
    nome = None
    bpm = None
    metro = None

    while i < len(dati):
        delta, i = _vlq(dati, i)
        ora += delta
        if i >= len(dati):
            break
        b = dati[i]

        if b == 0xFF:                                   # meta evento
            i += 1
            tipo = dati[i]
            i += 1
            lung, i = _vlq(dati, i)
            corpo = dati[i:i + lung]
            i += lung
            if tipo == 0x03 and nome is None:
                nome = corpo.decode('latin-1', 'replace').strip() or None
            elif tipo == 0x51 and lung == 3:            # set tempo
                usec = (corpo[0] << 16) | (corpo[1] << 8) | corpo[2]
                if usec and bpm is None:
                    bpm = 60_000_000 / usec
            elif tipo == 0x58 and lung >= 2 and metro is None:
                metro = (corpo[0], 1 << corpo[1])
            continue

        if b in (0xF0, 0xF7):                           # sysex
            i += 1
            lung, i = _vlq(dati, i)
            i += lung
            continue

        if b & 0x80:
            stato = b
            i += 1
        elif stato is None:
            raise ValueError(f'dato senza status a byte {i}: file corrotto')

        comando = stato & 0xF0
        canale = stato & 0x0F
        quanti = 1 if comando in (0xC0, 0xD0) else 2
        arg = dati[i:i + quanti]
        i += quanti
        if len(arg) < quanti:
            break

        if comando == 0x90 and arg[1] > 0:              # note on
            aperte.setdefault((canale, arg[0]), []).append((ora, arg[1]))
        elif comando == 0x80 or (comando == 0x90 and arg[1] == 0):
            pila = aperte.get((canale, arg[0]))
            if pila:
                inizio, vel = pila.pop(0)
                note.append(NotaMidi(pos=inizio, length=max(1, ora - inizio),
                                     y=arg[0], velocity=vel, canale=canale))

    # note rimaste aperte: il file finisce senza chiuderle. Si chiudono alla
    # fine invece di buttarle: buttarle silenziosamente sarebbe peggio.
    for (canale, y), pila in aperte.items():
        for inizio, vel in pila:
            note.append(NotaMidi(pos=inizio, length=max(1, ora - inizio),
                                 y=y, velocity=vel, canale=canale))

    note.sort(key=lambda n: (n.pos, n.y))
    return Traccia(indice=indice, nome=nome, note=note), bpm, metro


def leggi(path: Path | str) -> FileMidi:
    """Legge uno Standard MIDI File. Nessuna dipendenza esterna."""
    dati = Path(path).read_bytes()
    testa = None
    tracce: list[Traccia] = []
    bpm = None
    metro = None

    for tipo, corpo in _chunks(dati):
        if tipo == b'MThd':
            if testa is None:
                testa = struct.unpack('>HHh', corpo[:6])
        elif tipo == b'MTrk':
            t, b, m = _eventi_traccia(corpo, len(tracce))
            tracce.append(t)
            bpm = bpm if bpm is not None else b
            metro = metro if metro is not None else m

    if testa is None:
        raise ValueError(f'{path}: non e uno Standard MIDI File (manca MThd)')
    formato, _ntracce, divisione = testa
    if divisione <= 0:
        raise ValueError(
            f'{path}: divisione SMPTE ({divisione}), non PPQ. Non gestita: '
            'nel materiale musicale non si incontra praticamente mai, e '
            'indovinarla sarebbe peggio che rifiutarla.')
    return FileMidi(formato=formato, ppq=divisione, bpm=bpm, metro=metro,
                    tracce=tracce)


# --------------------------------------------------------------- conversione

class Conversione(NamedTuple):
    """L'esito della conversione dei tick, con quanto si e' perso."""
    note: int
    arrotondate: int
    scarto_massimo: float          # in tick del Deluge

    @property
    def esatta(self) -> bool:
        return self.arrotondate == 0

    def __str__(self) -> str:
        if self.esatta:
            return f'{self.note} note, conversione esatta'
        return (f'{self.note} note, {self.arrotondate} arrotondate '
                f'(scarto massimo {self.scarto_massimo:.2f} tick): '
                f'la micro-tempistica non e conservata per intero')


def _converti(note, ppq: int, tick_per_movimento: int):
    """Da tick MIDI a tick Deluge, dichiarando quanto arrotonda."""
    fattore = tick_per_movimento / ppq
    fuori = []
    arrotondate = 0
    scarto = 0.0
    for n in note:
        esatta_pos = n.pos * fattore
        esatta_len = n.length * fattore
        pos = round(esatta_pos)
        lung = max(1, round(esatta_len))
        for v, e in ((pos, esatta_pos), (lung, esatta_len)):
            d = abs(v - e)
            if d > 1e-9:
                arrotondate += 1
                scarto = max(scarto, d)
                break
        fuori.append((n, Note(pos=pos, length=lung, velocity=n.velocity)))
    return fuori, Conversione(len(note), arrotondate, scarto)


#: La mappa percussioni di General MIDI, con i nomi in italiano. Non e'
#: dedotta: e' lo standard GM, e i primi undici coincidono con il `DRUM_MAP`
#: di `music-composer`, che e' la sorgente che si importera' piu' spesso.
GM_PERCUSSIONI: dict[int, str] = {
    35: 'grancassa acustica', 36: 'kick', 37: 'rim', 38: 'rullante',
    39: 'clap', 40: 'rullante elettrico', 41: 'tom bassissimo',
    42: 'charleston chiuso', 43: 'tom basso', 44: 'charleston a pedale',
    45: 'tom medio-basso', 46: 'charleston aperto', 47: 'tom medio',
    48: 'tom medio-alto', 49: 'crash', 50: 'tom alto', 51: 'ride',
    52: 'china', 53: 'campana del ride', 54: 'tamburello', 55: 'splash',
    56: 'campanaccio', 57: 'crash 2', 58: 'vibraslap', 59: 'ride 2',
    60: 'bongo alto', 61: 'bongo basso', 62: 'conga alta chiusa',
    63: 'conga alta', 64: 'conga bassa', 65: 'timbale alto',
    66: 'timbale basso', 67: 'agogo alto', 68: 'agogo basso',
    69: 'cabasa', 70: 'maracas', 71: 'fischio corto', 72: 'fischio lungo',
    73: 'guiro corto', 74: 'guiro lungo', 75: 'claves',
    76: 'legnetto alto', 77: 'legnetto basso', 78: 'cuica chiusa',
    79: 'cuica aperta', 80: 'triangolo chiuso', 81: 'triangolo aperto',
}


def _scegli(f: FileMidi, traccia: int | None, canale: int | None,
            batteria: bool | None) -> list[NotaMidi]:
    note = []
    for t in f.tracce:
        if traccia is not None and t.indice != traccia:
            continue
        for n in t.note:
            if canale is not None and n.canale != canale:
                continue
            if batteria is True and n.canale != CANALE_BATTERIA:
                continue
            if batteria is False and n.canale == CANALE_BATTERIA:
                continue
            note.append(n)
    return note


def melodia(sorgente: FileMidi | Path | str, *, traccia: int | None = None,
            canale: int | None = None,
            tick_per_movimento: int = TICK_PER_MOVIMENTO_DELUGE,
            trasporta: int = 0) -> tuple[dict[int, list[Note]], Conversione]:
    """Le note melodiche di un MIDI, nella forma che ritorna `musica.melodia()`.

    Cioe' `altezza -> note`, pronto per `musica.scrivi(doc, clip, note)`.
    Ritorna anche il rapporto di conversione: **va letto**, perche' dice se
    la tempistica e' stata conservata o arrotondata.

    Il canale 10 (batteria) e' escluso di default: le sue "altezze" sono
    strumenti, non note, e finirebbero su righe di synth senza senso.
    """
    f = sorgente if isinstance(sorgente, FileMidi) else leggi(sorgente)
    grezze = _scegli(f, traccia, canale, batteria=False)
    coppie, esito = _converti(grezze, f.ppq, tick_per_movimento)
    fuori: dict[int, list[Note]] = {}
    for orig, n in coppie:
        y = orig.y + trasporta
        if not 0 <= y <= 127:
            continue
        fuori.setdefault(y, []).append(n)
    for v in fuori.values():
        v.sort(key=lambda n: n.pos)
    return fuori, esito


def batteria(sorgente: FileMidi | Path | str, *, traccia: int | None = None,
             tick_per_movimento: int = TICK_PER_MOVIMENTO_DELUGE
             ) -> tuple[dict[str, list[Note]], Conversione]:
    """Le percussioni di un MIDI, raggruppate per NOME General MIDI.

    Ritorna `nome -> note`, cioe' la forma che vuole
    `musica.scrivi(doc, clip, note, dove=nome_del_drum)` una riga per volta.
    Si passa per il nome e non per il numero perche' un kit del Deluge
    indirizza i drum per nome, e un numero GM non dice niente a chi legge.

    Un'altezza fuori dalla mappa GM viene resa come `'nota 84'` invece di
    essere buttata: nei loop veri capita, e perderla in silenzio sarebbe la
    solita perdita muta.
    """
    f = sorgente if isinstance(sorgente, FileMidi) else leggi(sorgente)
    grezze = _scegli(f, traccia, canale=None, batteria=True)
    if not grezze and traccia is None:
        # certi file mettono la batteria su un canale qualunque: se il canale
        # 10 e' vuoto non si finge che il file sia vuoto
        grezze = _scegli(f, None, None, batteria=None)
    coppie, esito = _converti(grezze, f.ppq, tick_per_movimento)
    fuori: dict[str, list[Note]] = {}
    for orig, n in coppie:
        nome = GM_PERCUSSIONI.get(orig.y, f'nota {orig.y}')
        fuori.setdefault(nome, []).append(n)
    for v in fuori.values():
        v.sort(key=lambda n: n.pos)
    return fuori, esito


def racconta(sorgente: FileMidi | Path | str) -> str:
    """Cosa c'e' dentro un MIDI, prima di importarlo."""
    f = sorgente if isinstance(sorgente, FileMidi) else leggi(sorgente)
    righe = [f'MIDI formato {f.formato}, {f.ppq} tick per movimento'
             + (f', {f.bpm:.1f} BPM' if f.bpm else '')
             + (f', {f.metro[0]}/{f.metro[1]}' if f.metro else '')]

    fattore = TICK_PER_MOVIMENTO_DELUGE / f.ppq
    righe.append(
        f'  conversione al Deluge: x{fattore:g}'
        + ('  (esatta)' if float(fattore).is_integer()
           or (f.ppq % TICK_PER_MOVIMENTO_DELUGE == 0)
           else '  (non intera: le posizioni verranno arrotondate)'))

    for t in f.tracce:
        if not t.note:
            righe.append(f'  traccia {t.indice}: vuota'
                         + (f' ({t.nome})' if t.nome else ''))
            continue
        battute = max(n.pos + n.length for n in t.note) / (f.ppq * 4)
        etichetta = 'batteria' if t.e_batteria else 'melodica'
        righe.append(
            f'  traccia {t.indice} [{etichetta}]'
            + (f' "{t.nome}"' if t.nome else '')
            + f': {len(t.note)} note, canali {list(t.canali)}, '
              f'{battute:.2f} battute')
        if t.e_batteria:
            conti: dict[str, int] = {}
            for n in t.note:
                if n.canale == CANALE_BATTERIA:
                    nome = GM_PERCUSSIONI.get(n.y, f'nota {n.y}')
                    conti[nome] = conti.get(nome, 0) + 1
            for nome, c in sorted(conti.items(), key=lambda kv: -kv[1]):
                righe.append(f'      {nome:24} {c}')
        else:
            vel = [n.velocity for n in t.note]
            righe.append(f'      velocity {min(vel)}-{max(vel)}, '
                         f'{len({n.velocity for n in t.note})} livelli')
    return '\n'.join(righe)
