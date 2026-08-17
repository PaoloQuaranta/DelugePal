"""Leggere la Weimar Jazz Database e tradurla nelle forme che `musica` usa.

PERCHE' ESISTE
--------------
Il jazz **non sta nei formati di partitura**. kern, MusicXML e ABC sono nati
per la musica scritta, e di jazz come repertorio codificato non ne hanno
quasi. Il jazz simbolico sta altrove, e soprattutto qui: 456 assoli
trascritti a mano da 340 tracce e 197 dischi, con gli **accordi e i battiti
allineati all'audio**.

E' l'unica fonte che porta la linea suonata INSIEME all'accordo su cui e'
suonata. Un MIDI di un assolo da' le note e basta; qui c'e' anche su cosa
stavano sopra, che e' meta' di quello che serve per imparare.

`wjazzd.db` sta in `to-read/MIDI/`, che NON e' versionato: e' opera di terzi.
I test che lo usano saltano se non c'e', come quelli del corpus.

PERCHE' `sqlite3` E BASTA
-------------------------
E' nella stdlib. Nessuna dipendenza nuova, come `midi.py` che si e' scritto
il lettore di Standard MIDI File invece di tirarsi dentro `mido`. Qui il
lavoro e' anche meno: il formato e' gia' un database.

LE DUE COSE CHE HANNO RICHIESTO ATTENZIONE
------------------------------------------
1. **Gli accordi sono in un dialetto.** Il 22% delle 30 548 occorrenze non e'
   leggibile da `MU.sigla()`, e i fallimenti sono sistematici, non sparsi.
   Vedi `sigla_weimar()`. Il dialetto sta QUI e non in `MU.SIGLE`: quella e'
   la notazione da lead sheet, comune a tutte le fonti, e infilarci le
   abitudini di un database solo la sporcherebbe per sempre.

   ⚠️ Verificato anche il verso opposto, che era il rischio vero: le code che
   `MU.sigla()` legge -- `7`, `-7`, `-`, `6`, `sus`, `m7b5`, `7alt` -- vogliono
   dire la STESSA cosa nei due dialetti. Un simbolo che si legge non e' un
   simbolo che si legge giusto, e un falso positivo li' sarebbe stato muto.

2. **La posizione metrica c'e' gia', accanto al tempo reale.** La tabella
   `melody` porta `bar/beat/tatum/division` (la griglia) E `onset` in secondi
   (l'esecuzione vera). Non serve dedurre la metrica dagli onset: e' annotata.
   E la differenza fra le due e' la micro-tempistica, cioe' il motivo per cui
   questo database vale piu' di una raccolta di MIDI. Qui si converte la
   griglia; misurare lo scarto e' un passo a parte, non ancora fatto.

   ⚠️ `division` vale 5 o 10 per 7242 note su 200 809 (il 3,6%), e 96 non si
   divide per 5: 19,2 tick. Quelle si arrotondano, e `Conversione` lo
   **dichiara**, come in `midi.py`.
"""
from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import NamedTuple

from . import musica as MU
from .midi import TICK_PER_MOVIMENTO_DELUGE, Conversione
from .notes import Note

#: Le qualita' del dialetto, come mappa grado -> semitoni. Il prefisso e' uno
#: solo e viene subito dopo la fondamentale.
QUALITA_WEIMAR: dict[str, dict[int, int]] = {
    '':    {1: 0, 3: 4, 5: 7},      # maggiore / dominante
    '-':   {1: 0, 3: 3, 5: 7},      # minore
    '+':   {1: 0, 3: 4, 5: 8},      # aumentato
    'o':   {1: 0, 3: 3, 5: 6},      # diminuito
    'sus': {1: 0, 4: 5, 5: 7},      # sospeso, senza terza
}

#: I gradi che possono comparire, dal piu' lungo: '13' va provato prima di
#: '1' e di '3', se no '13' si legge come due gradi diversi.
GRADI_WEIMAR = (13, 11, 9, 7, 6, 5)

#: Semitoni sopra la fondamentale, prima delle alterazioni. La settima e'
#: quella di dominante: diventa maggiore con la 'j' e diminuita sotto 'o'.
SEMITONI_WEIMAR = {5: 7, 6: 9, 7: 10, 9: 14, 11: 17, 13: 21}

#: Come si scrive "nessun accordo".
NIENTE_ACCORDO = 'NC'

#: La sola fondamentale. Le sigle di Weimar sono in inglese e maiuscole, e
#: nessuna qualita' comincia per 'b' o '#', quindi prendere l'alterazione
#: quando c'e' non e' ambiguo.
_FONDAMENTALE = re.compile(r'^[A-G][b#]?')


def sigla_weimar(testo: str) -> MU.Sigla | None:
    """Da una sigla nel dialetto di Weimar a una `MU.Sigla`, o None.

    La grammatica, ricavata dai 419 simboli distinti del database e
    verificata su tutti quelli che `MU.sigla()` non sapeva leggere:

        fondamentale  qualita?  'j'?  (grado alterazione?)*  ('/' basso)?

    Tre differenze dalla notazione da lead sheet, tutte sistematiche:

    - **`j` rende maggiore la settima che segue**: `Ebj7` e' mibmaj7, `C-j7`
      e' do minore con settima maggiore.
    - **l'alterazione sta DOPO il grado**: `D79b` e' re7b9, non re7 con
      qualcosa che comincia per 9. `C79b13b` sono due alterazioni in fila.
    - **`o` e' il diminuito e `sus` precede la settima**: `Fsus7` e' fa7sus4.

    Torna `None` per `NC` e per la casella vuota -- che nel database sono la
    stessa cosa, "qui non c'e' un accordo", e non vanno confusi con un
    errore di lettura.

    La fondamentale passa da `MU.sigla()`, cosi' il vocabolario delle altezze
    resta uno solo in tutto il progetto.
    """
    if not isinstance(testo, str):
        raise ValueError(f'sigla_weimar() vuole una stringa, non '
                         f'{type(testo).__name__} ({testo!r})')
    grezzo = testo.strip()
    if not grezzo or grezzo.upper() == NIENTE_ACCORDO:
        return None

    # Prima si prova la lettura CANONICA, e non per pigrizia: e' misurato che
    # le code lette da entrambi i dialetti vogliono dire la stessa cosa
    # (`7`, `-7`, `-`, `6`, `-6`, `sus`, `m7b5`, `69`, `+`, `7alt`), cioe' il
    # 78% delle occorrenze. Scendere al dialetto solo quando quella fallisce
    # evita di riscrivere una grammatica che gia' esiste -- e soprattutto
    # evita il caso `m7b5`, dove il `b5` e' un'alterazione scritta PRIMA del
    # grado e la grammatica di Weimar la leggerebbe come una settima bemolle.
    try:
        return MU.sigla(grezzo)
    except ValueError:
        pass

    basso = None
    if '/' in grezzo:
        capo, _, coda = grezzo.rpartition('/')
        try:
            basso = MU.sigla(coda).fondamentale
        except ValueError:
            raise ValueError(f'{testo!r}: {coda!r} dopo lo slash non e una '
                             f'nota') from None
        grezzo = capo

    #: La fondamentale si estrae con una regex sua, NON con `MU.sigla()`:
    #: quello e' un parser di accordi interi e su 'C7' si mangerebbe anche la
    #: settima, lasciando una triade. [difetto vero, trovato dai test]
    m = _FONDAMENTALE.match(grezzo)
    if not m:
        raise ValueError(f'{testo!r}: non riconosco la fondamentale')
    fondamentale = MU.sigla(m.group(0)).fondamentale
    resto = grezzo[m.end():]

    qualita = ''
    for q in ('sus', '-', '+', 'o'):            # 'sus' per prima: e' lunga
        if resto.startswith(q):
            qualita, resto = q, resto[len(q):]
            break
    settima_maggiore = resto.startswith('j')
    if settima_maggiore:
        resto = resto[1:]

    gradi = dict(QUALITA_WEIMAR[qualita])
    while resto:
        for g in GRADI_WEIMAR:
            if not resto.startswith(str(g)):
                continue
            resto = resto[len(str(g)):]
            alterazione = 0
            if resto[:1] == 'b':
                alterazione, resto = -1, resto[1:]
            elif resto[:1] == '#':
                alterazione, resto = +1, resto[1:]
            semitoni = SEMITONI_WEIMAR[g]
            if g == 7:
                if settima_maggiore:
                    semitoni = 11
                elif qualita == 'o':
                    semitoni = 9                # settima DIMINUITA
            gradi[g] = semitoni + alterazione
            break
        else:
            raise ValueError(
                f'{testo!r}: non so leggere {resto!r}. La grammatica di '
                f'Weimar e "fondamentale, qualita, j, poi gradi con '
                f'l alterazione in coda" -- i gradi ammessi sono '
                f'{list(GRADI_WEIMAR)}')
    #: Una 'j' senza settima scritta resta comunque una settima maggiore:
    #: nel database non capita, ma leggerla come triade sarebbe muto.
    if settima_maggiore and 7 not in gradi:
        gradi[7] = 11
    return MU.Sigla(testo=testo, fondamentale=fondamentale, gradi=gradi,
                    basso=basso, letto_come=None)


# ------------------------------------------------------------- il database

class Solo(NamedTuple):
    """I dati di un assolo, quelli che servono per sceglierlo."""

    melid: int
    performer: str
    title: str
    instrument: str
    style: str
    rhythmfeel: str
    key: str
    signature: str
    tempo: float
    tempoclass: str
    chorus_count: int
    note: int

    def __str__(self) -> str:
        return (f'[{self.melid}] {self.performer} - {self.title} '
                f'({self.instrument}, {self.style}, {self.rhythmfeel}, '
                f'{self.tempo:.0f} bpm, {self.key}, {self.note} note)')


class Accordo(NamedTuple):
    """Un accordo della griglia, dove comincia e come si e' letto."""

    tick: int
    bar: int
    beat: int
    testo: str
    #: `None` quando il testo era `NC`, cioe' quando non c'e' un accordo.
    sigla: MU.Sigla | None


def apri(path: Path | str) -> sqlite3.Connection:
    """Il database in sola lettura. Solleva `FileNotFoundError` se non c'e'.

    L'eccezione e' quella giusta di proposito: la suite la traduce in un
    SALTO, perche' `wjazzd.db` non appartiene a questo repo.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))
    con = sqlite3.connect(f'file:{p.as_posix()}?mode=ro', uri=True)
    con.row_factory = sqlite3.Row
    return con


def quanti(path: Path | str) -> int:
    """Quanti assoli ci sono."""
    with apri(path) as con:
        return con.execute('select count(*) from solo_info').fetchone()[0]


_CAMPI_SOLO = """
    s.melid, s.performer, s.title, s.instrument, s.style, s.rhythmfeel,
    s.key, s.signature, s.avgtempo, s.tempoclass, s.chorus_count,
    (select count(*) from melody m where m.melid = s.melid) as note
"""


def _in_solo(r: sqlite3.Row) -> Solo:
    return Solo(melid=r['melid'], performer=r['performer'], title=r['title'],
                instrument=r['instrument'], style=r['style'],
                rhythmfeel=r['rhythmfeel'], key=r['key'],
                signature=r['signature'], tempo=r['avgtempo'] or 0.0,
                tempoclass=r['tempoclass'], chorus_count=r['chorus_count'],
                note=r['note'])


def solo(path: Path | str, melid: int) -> Solo:
    """Un assolo per numero."""
    with apri(path) as con:
        r = con.execute(f'select {_CAMPI_SOLO} from solo_info s '
                        f'where s.melid = ?', (melid,)).fetchone()
    if r is None:
        raise ValueError(f'non c e nessun assolo con melid={melid}')
    return _in_solo(r)


def elenco(path: Path | str, *, style: str | None = None,
           rhythmfeel: str | None = None, performer: str | None = None,
           instrument: str | None = None, limite: int = 50) -> list[Solo]:
    """Gli assoli che rispondono ai filtri.

    I valori ammessi si guardano con `valori()`: sono etichette del database
    (`POSTBOP`, `SWING`, `LATIN`...), non testo libero, e sbagliarne una da'
    una lista vuota invece di un errore.
    """
    dove, arg = [], []
    for campo, valore in (('s.style', style), ('s.rhythmfeel', rhythmfeel),
                          ('s.performer', performer),
                          ('s.instrument', instrument)):
        if valore is not None:
            dove.append(f'{campo} = ?')
            arg.append(valore)
    filtro = ('where ' + ' and '.join(dove)) if dove else ''
    with apri(path) as con:
        righe = con.execute(
            f'select {_CAMPI_SOLO} from solo_info s {filtro} '
            f'order by s.melid limit ?', (*arg, limite)).fetchall()
    return [_in_solo(r) for r in righe]


def valori(path: Path | str, campo: str) -> dict[str, int]:
    """Le etichette di un campo di `solo_info`, con quante volte compaiono."""
    ammessi = {'style', 'rhythmfeel', 'instrument', 'performer', 'tempoclass',
               'key', 'signature'}
    if campo not in ammessi:
        raise ValueError(f'campo {campo!r} non interrogabile, usare '
                         f'{sorted(ammessi)}')
    with apri(path) as con:
        return {r[0]: r[1] for r in con.execute(
            f'select {campo}, count(*) from solo_info group by {campo} '
            f'order by count(*) desc')}


def con_suddivisione(path: Path | str, division: int) -> int | None:
    """Il primo assolo che contiene note con quella suddivisione, o None.

    Serve a scegliere un caso di prova invece di supporre che esista: le
    quintine ci sono, ma non in tutti gli assoli.
    """
    with apri(path) as con:
        r = con.execute('select melid from melody where division = ? '
                        'order by melid limit 1', (division,)).fetchone()
    return r[0] if r else None


def _movimenti_per_battuta(con: sqlite3.Connection, melid: int) -> int:
    """Quanti movimenti ha una battuta, dal numeratore del tempo in chiave.

    Si prende quello piu' frequente fra le note: il campo esiste su ogni
    nota, e alcuni assoli cambiano metro per strada.
    """
    r = con.execute('select num, count(*) as q from melody where melid = ? '
                    'group by num order by q desc limit 1',
                    (melid,)).fetchone()
    return int(r['num']) if r and r['num'] else 4


def _posizione(bar: int, beat: int, tatum: int, division: int,
               movimenti: int, tpm: int) -> float:
    """La posizione in tick, esatta (puo' non essere intera)."""
    dentro = 0.0 if division <= 1 else (tatum - 1) * tpm / division
    return ((bar * movimenti) + (beat - 1)) * tpm + dentro


def melodia(path: Path | str, melid: int, *,
            tick_per_movimento: int = TICK_PER_MOVIMENTO_DELUGE
            ) -> tuple[dict[int, list[Note]], Conversione]:
    """Le note di un assolo, raggruppate per altezza, e come sono state rese.

    Stessa forma di `MU.melodia()` e di `midi.melodia()` -- `altezza -> note`
    -- quindi entra in `MU.scrivi()` senza adattatori.

    Le posizioni vengono dalla **griglia metrica annotata**
    (`bar/beat/tatum/division`), non dagli onset in secondi: gli onset sono
    l'esecuzione vera, e servono a misurare lo scarto, non a collocare le
    note. Le durate invece vengono dai secondi, riportate in tick col
    `beatdur` di quella nota -- cosi' seguono il tempo locale invece di un
    tempo medio.

    L'origine e' la prima nota: gli assoli che cominciano in levare hanno
    battute negative nel database, e tick negativi non esistono.
    """
    with apri(path) as con:
        movimenti = _movimenti_per_battuta(con, melid)
        righe = con.execute(
            'select bar, beat, tatum, division, pitch, duration, beatdur '
            'from melody where melid = ? order by eventid', (melid,)).fetchall()
    if not righe:
        raise ValueError(f'l assolo melid={melid} non ha note')

    tpm = tick_per_movimento
    grezze = []
    for r in righe:
        esatta = _posizione(r['bar'], r['beat'], r['tatum'],
                            r['division'] or 1, movimenti, tpm)
        beatdur = r['beatdur'] or 0
        lunga = (r['duration'] / beatdur * tpm) if beatdur else tpm / 4
        grezze.append((esatta, lunga, int(r['pitch'])))

    origine = min(e for e, _, _ in grezze)
    arrotondate, scarto = 0, 0.0
    out: dict[int, list[Note]] = {}
    for esatta, lunga, y in grezze:
        rel = esatta - origine
        pos = round(rel)
        lung = max(1, round(lunga))
        d = abs(pos - rel)
        if d > 1e-9:
            arrotondate += 1
            scarto = max(scarto, d)
        out.setdefault(y, []).append(
            Note(pos=pos, length=lung, velocity=MU.VEL_COLPO))
    return out, Conversione(len(grezze), arrotondate, scarto)


def armonia(path: Path | str, melid: int, *,
            tick_per_movimento: int = TICK_PER_MOVIMENTO_DELUGE
            ) -> list[Accordo]:
    """La griglia armonica di un assolo, gia' sciolta in `MU.Sigla`.

    Nel database l'accordo e' scritto **solo dove cambia** e la casella resta
    vuota finche' dura: qui vengono restituiti solo i cambi, che e' come si
    legge una griglia.

    L'origine dei tick e' la stessa di `melodia()` -- la prima nota -- cosi'
    le due si sovrappongono senza aggiustamenti.
    """
    with apri(path) as con:
        movimenti = _movimenti_per_battuta(con, melid)
        prima = con.execute(
            'select bar, beat, tatum, division from melody where melid = ? '
            'order by eventid', (melid,)).fetchall()
        battiti = con.execute(
            "select bar, beat, chord from beats where melid = ? "
            "and chord <> '' order by beatid", (melid,)).fetchall()
    if not prima:
        raise ValueError(f'l assolo melid={melid} non ha note')

    tpm = tick_per_movimento
    origine = min(_posizione(r['bar'], r['beat'], r['tatum'],
                             r['division'] or 1, movimenti, tpm)
                  for r in prima)
    fuori = []
    for b in battiti:
        tick = _posizione(b['bar'], b['beat'], 1, 1, movimenti, tpm) - origine
        fuori.append(Accordo(tick=round(tick), bar=b['bar'], beat=b['beat'],
                             testo=b['chord'],
                             sigla=sigla_weimar(b['chord'])))
    return fuori


# ------------------------------------------------------------------ lo swing
#
# COSA SI MISURA
# --------------
# Dove cade il **levare** dentro il movimento, in frazione: 0,5 e' dritto,
# 0,667 e' la terzina. Il rapporto fra le due meta' e' la BUR (beat-upbeat
# ratio) della letteratura: BUR = p / (1 - p), quindi 1 dritto e 2 terzina.
#
# I due estremi del movimento sono i battiti VERI, presi da `beats.onset`, e
# il levare e' l'onset vero della nota. Nessuno dei tre viene dalla griglia.
#
# ⚠️ L'ERRORE CHE HA BRUCIATO TRE TENTATIVI, E VALE PIU' DEL RISULTATO
# --------------------------------------------------------------------
# La posizione **annotata** (`tatum`/`division`) **contiene gia' lo swing**: i
# trascrittori scrivono una coppia di crome swingate come `tatum 1 e 3 di
# division 3`, cioe' mettono la terzina nella griglia metrica. Quindi
# selezionare le coppie con `division == 2` -- che sembra la cosa ovvia da
# fare, "prendi le crome" -- seleziona in realta' le sole coppie che il
# trascrittore ha giudicato DRITTE.
#
# Tre metodi diversi hanno dato 1,10, 1,19 e 1,10, e sembravano confermarsi a
# vicenda. Erano lo stesso errore tre volte: una distorsione di SELEZIONE, non
# di calcolo. A trovarla non e' stato un test -- e' stato guardare le righe
# grezze di un assolo lento e vedere `tatum=1/3` e `tatum=3/3`.
#
# Il controllo che l'ha smascherata viene da fuori: la letteratura dice che lo
# swing CALA al salire del tempo e che i generi a crome dritte stanno sotto.
# Nessuna delle due compariva. Ora compaiono entrambe.
#
# ⚠️ QUANTO VALE, E QUANTO NO
# ---------------------------
# I numeri sono misurati e riproducibili, ma **non sono stati riconciliati con
# la letteratura in valore assoluto**: «Playing It Straight» riporta ~1,3 di
# mediana sullo stesso database, questa misura da' ~1,6. Il metodo di quel
# lavoro non e' leggibile (articolo a pagamento), quindi la differenza resta
# non spiegata e i valori assoluti vanno presi come provvisori. Le
# DIFFERENZE fra sottoinsiemi -- swing contro funk, lento contro veloce --
# sono invece coerenti con quanto e' pubblicato.

#: Fuori da questa finestra non e' una coppia di crome: e' un'altra figura,
#: o un errore di allineamento. Dichiarata perche' e' una scelta, non una
#: legge di natura.
FINESTRA_LEVARE = (0.3, 0.8)


class Swing(NamedTuple):
    """Dove cade il levare, su un insieme di assoli."""

    assoli: int
    coppie: int
    #: Posizione mediana del levare nel movimento, 0-1. 0,5 e' dritto.
    levare: float
    q1: float
    q3: float

    @property
    def bur(self) -> float:
        """Il rapporto fra le due meta' del movimento. 1 dritto, 2 terzina."""
        return in_bur(self.levare)

    @property
    def percento(self) -> float:
        return self.levare * 100

    def __str__(self) -> str:
        if not self.coppie:
            return 'nessuna coppia di crome misurabile'
        return (f'{self.assoli} assoli, {self.coppie} coppie: levare al '
                f'{self.percento:.1f}% del movimento (BUR {self.bur:.2f}), '
                f'quartili {self.q1 * 100:.1f}%-{self.q3 * 100:.1f}%')


def in_bur(levare: float) -> float:
    """Da posizione del levare a BUR. 0,5 -> 1 (dritto), 0,667 -> 2."""
    if not 0 < levare < 1:
        raise ValueError(f'il levare sta fra 0 e 1, non {levare}')
    return levare / (1 - levare)


def levare_da_dati(battiti, note, finestra=FINESTRA_LEVARE) -> list[float]:
    """Le posizioni del levare, da battiti e note gia' letti.

    `battiti` sono terne `(bar, beat, onset)` in ordine; `note` sono quaterne
    `(bar, beat, tatum, onset)`. Sta separata dal database per poterla
    provare su dati costruiti a mano.

    Si tiene un movimento solo quando contiene **esattamente due eventi** e il
    primo sta **sul** movimento (`tatum == 1`): due eventi in un movimento
    sono una coppia di crome, tre o piu' sono un'altra figura.

    Il `tatum` del SECONDO evento non viene guardato di proposito -- vedi la
    nota qui sopra: quello e' annotato e lo swing ce l'ha gia' dentro.
    """
    griglia = {(b, m): t for b, m, t in battiti}
    ordine = [(b, m) for b, m, _ in battiti]
    dopo = {ordine[i]: ordine[i + 1] for i in range(len(ordine) - 1)}

    dentro: dict[tuple[int, int], list[tuple[int, float]]] = {}
    for bar, beat, tatum, onset in note:
        dentro.setdefault((bar, beat), []).append((tatum, onset))

    basso, alto = finestra
    fuori = []
    for chiave, eventi in dentro.items():
        if len(eventi) != 2:
            continue
        (tatum_a, _), (_, onset_b) = eventi
        if tatum_a != 1:
            continue
        seguente = dopo.get(chiave)
        if seguente is None or chiave not in griglia or seguente not in griglia:
            continue
        t0, t1 = griglia[chiave], griglia[seguente]
        if t1 <= t0:
            continue
        p = (onset_b - t0) / (t1 - t0)
        if basso < p < alto:
            fuori.append(p)
    return fuori


def levare(path: Path | str, melid: int,
           finestra=FINESTRA_LEVARE) -> list[float]:
    """Le posizioni del levare di un assolo."""
    with apri(path) as con:
        battiti = [(r['bar'], r['beat'], r['onset']) for r in con.execute(
            'select bar, beat, onset from beats where melid = ? '
            'order by beatid', (melid,))]
        note = [(r['bar'], r['beat'], r['tatum'], r['onset'])
                for r in con.execute(
                    'select bar, beat, tatum, onset from melody '
                    'where melid = ? order by eventid', (melid,))]
    return levare_da_dati(battiti, note, finestra)


def swing(path: Path | str, *, melid: int | None = None,
          style: str | None = None, rhythmfeel: str | None = None,
          instrument: str | None = None, tempo_min: float | None = None,
          tempo_max: float | None = None, minimo_coppie: int = 20,
          finestra=FINESTRA_LEVARE) -> Swing:
    """Quanto e' swingato un insieme di assoli.

    Si aggrega sulla **mediana per assolo**, non su tutte le coppie in un
    mucchio: se no un assolo lungo e prolisso peserebbe come dieci corti, e si
    misurerebbe chi ha suonato piu' note invece di come si suona.

    Gli assoli con meno di `minimo_coppie` coppie non entrano: una mediana su
    quattro valori non e' una mediana.
    """
    dove, arg = [], []
    for campo, valore in (('melid', melid), ('style', style),
                          ('rhythmfeel', rhythmfeel),
                          ('instrument', instrument)):
        if valore is not None:
            dove.append(f'{campo} = ?')
            arg.append(valore)
    if tempo_min is not None:
        dove.append('avgtempo >= ?')
        arg.append(tempo_min)
    if tempo_max is not None:
        dove.append('avgtempo <= ?')
        arg.append(tempo_max)
    filtro = ('where ' + ' and '.join(dove)) if dove else ''

    from statistics import median, quantiles                # noqa: PLC0415

    with apri(path) as con:
        scelti = [r[0] for r in con.execute(
            f'select melid from solo_info {filtro} order by melid', arg)]
        mediane, coppie = [], 0
        for uno in scelti:
            battiti = [(r['bar'], r['beat'], r['onset']) for r in con.execute(
                'select bar, beat, onset from beats where melid = ? '
                'order by beatid', (uno,))]
            note = [(r['bar'], r['beat'], r['tatum'], r['onset'])
                    for r in con.execute(
                        'select bar, beat, tatum, onset from melody '
                        'where melid = ? order by eventid', (uno,))]
            v = levare_da_dati(battiti, note, finestra)
            if len(v) >= minimo_coppie:
                mediane.append(median(v))
                coppie += len(v)

    if not mediane:
        return Swing(assoli=0, coppie=0, levare=0.5, q1=0.5, q3=0.5)
    if len(mediane) >= 4:
        q = quantiles(mediane, n=4)
        q1, q3 = q[0], q[2]
    else:
        q1 = q3 = median(mediane)
    return Swing(assoli=len(mediane), coppie=coppie, levare=median(mediane),
                 q1=q1, q3=q3)


def racconta(path: Path | str, melid: int) -> str:
    """Cosa c'e' in un assolo, in parole. Il gemello di `midi.racconta()`."""
    s = solo(path, melid)
    note, conv = melodia(path, melid)
    acc = armonia(path, melid)
    altezze = sorted(note)
    ignoti = [a.testo for a in acc if a.sigla is None and a.testo]
    righe = [
        str(s),
        f'  {conv}',
        f'  estensione {MU.nome_altezza(altezze[0])} - '
        f'{MU.nome_altezza(altezze[-1])} su {len(altezze)} altezze diverse',
        f'  {len(acc)} cambi di accordo',
    ]
    if acc:
        primi = ' | '.join(a.testo for a in acc[:8])
        righe.append(f'  griglia: {primi}' + (' ...' if len(acc) > 8 else ''))
    if ignoti:
        righe.append(f'  {len(ignoti)} caselle senza accordo (NC)')
    return '\n'.join(righe)
