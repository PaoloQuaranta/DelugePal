# Il lettore JTD e la casella 5 — piano di attuazione

> **Per chi lavora a comando:** SOTTO-SKILL RICHIESTA: usare
> `superpowers:subagent-driven-development` (consigliata) oppure
> `superpowers:executing-plans` per attuare questo piano un compito alla
> volta. I passi hanno la casella (`- [ ]`) per essere spuntati.

**Obiettivo:** misurare come basso, batteria e piano di un trio jazz si
spartiscono la battuta, su 1294 esecuzioni vere, e scrivere il risultato nella
casella 5 di `docs/repertori/jazz.md`.

**Architettura:** un lettore in stdlib pura (`tools/delugexml/jtd.py`) che
apre lo zip del Jazz Trio Database **senza decomprimerlo** e ne cava tre
forme — l'elenco dei brani, la griglia dei beat, le battute complete con gli
onset dei tre strumenti dentro; sopra di esso uno strumento di misura
(`tools/misura_spartizione.py`) che stampa cinque misure con i conteggi che le
reggono. Nessuna dipendenza nuova, nessuna modifica al generatore.

**Tecnologie:** Python 3 della stdlib — `zipfile`, `csv`, `json`, `statistics`.
Nessun pacchetto esterno, mai.

## Vincoli globali

- **Nessuna dipendenza esterna nella libreria.** I test girano col Python di
  sistema (`python tests/test_all.py`), dove `mido`, `numpy` e `pandas` NON ci
  sono. Un `import` di terze parti in `tools/delugexml/` rende la suite non
  eseguibile.
- **Gli archivi non si decomprimono:** si leggono i membri con `zipfile`.
  Regola di HANDOFF §6-duodecies.
- **Il corpus non entra nel repo.** Sta in `to-read/`, che è in `.gitignore`.
  Ogni test che lo usa **salta** se manca: basta sollevare `FileNotFoundError`,
  il runner in fondo a `tests/test_all.py` lo traduce già in SKIP.
- **Output degli strumenti in ASCII puro.** Finiscono in `out/` per
  redirezione e la console di Windows è cp1252. Vale per
  `tools/misura_spartizione.py`, non per i documenti in `docs/`.
- **Mai `pathlib.write_text()` nudo** per scrivere file: su Windows traduce
  `\n` in `\r\n`. Si usa `write_bytes()` o `open(..., newline='')`, e prima di
  committare si controlla che `git diff --stat` e
  `git diff --stat --ignore-cr-at-eol` diano lo stesso numero.
- **Ogni numero che entra in `docs/` porta il suo grado** (`[MIS]`, `[OSS]`,
  `[IPO]`, `[WEB]`, `[MAN]`) e, se è `[MIS]`, **quante esecuzioni e quanti
  esecutori lo reggono**.
- **Il ramo è `spartizione-jtd`**, già creato, e il generatore non si tocca.
- Il corpus è in `to-read/MIDI/jazz-trio-database-v02.zip` (24 MB, già
  scaricato). Dentro, ogni brano è una cartella
  `jazz-trio-database-v02/<fname>/`.

---

## Struttura dei file

| file | responsabilità |
|---|---|
| `tools/delugexml/jtd.py` | **nuovo.** Legge il corpus e basta: elenco, griglia, onset, battute. Nessuna statistica, nessuna soglia musicale |
| `tools/delugexml/midi.py` | **tre righe:** `leggi_bytes()` accanto a `leggi()`, per leggere un MIDI che sta dentro uno zip |
| `tools/misura_spartizione.py` | **nuovo.** Tutte le scelte statistiche e musicali (finestre, soglie, quantili) stanno qui, dichiarate |
| `tests/test_all.py` | **in coda:** i test nuovi, che saltano senza corpus |
| `docs/repertori/jazz.md` | la casella 5, riscritta coi numeri |
| `docs/MUSICA.md`, `docs/FONTI.md`, `HANDOFF.md` | indice, attribuzione, e la correzione delle tre righe false |

**La divisione che conta:** `jtd.py` non decide **niente** di musicale — non sa
cosa sia una corsa, una finestra di coincidenza o un walking. Restituisce
quello che il corpus dice. Ogni soglia sta in `misura_spartizione.py` con
accanto la frase che la giustifica. È la stessa divisione fra `wjazz.py` e
`misura_melodia.py`.

---

## Task 1: `midi.leggi_bytes()`

**File:**
- Modifica: `tools/delugexml/midi.py:199-227` (la funzione `leggi`)
- Test: `tests/test_all.py` (in coda)

**Interfacce:**
- Consuma: niente.
- Produce: `midi.leggi_bytes(dati: bytes, nome: str = '<bytes>') -> FileMidi`,
  usata dal Task 4 per leggere `piano_midi.mid` dentro lo zip.

- [ ] **Passo 1: scrivere il test che fallisce**

In coda a `tests/test_all.py`:

```python
def test_midi_leggi_bytes():
    """Un MIDI si legge anche quando sta dentro un archivio.

    `leggi()` vuole un percorso; i MIDI del Jazz Trio Database stanno dentro
    uno zip che la regola di §6-duodecies dice di non decomprimere. Le due
    strade devono dare lo STESSO risultato: se divergessero, ogni misura
    presa dallo zip sarebbe diversa da quella presa dal disco senza che
    nessuno se ne accorga.
    """
    from delugexml import midi as MI                        # noqa: PLC0415

    campione = ROOT / 'to-read' / 'MIDI' / 'POP909-Dataset-master'
    campione = campione / 'POP909-Dataset-master' / 'POP909' / '001' / '001.mid'
    if not campione.exists():
        raise FileNotFoundError(str(campione))

    da_disco = MI.leggi(campione)
    da_bytes = MI.leggi_bytes(campione.read_bytes(), nome=str(campione))
    check('leggi_bytes da lo stesso numero di tracce',
          len(da_bytes.tracce) == len(da_disco.tracce),
          f'{len(da_bytes.tracce)} vs {len(da_disco.tracce)}')
    check('e le stesse note',
          da_bytes.note == da_disco.note,
          f'{len(da_bytes.note)} vs {len(da_disco.note)} note')
    check('e lo stesso ppq', da_bytes.ppq == da_disco.ppq, str(da_bytes.ppq))
```

- [ ] **Passo 2: farlo girare e vederlo fallire**

```bash
cd /d/DelugePal && python tests/test_all.py 2>&1 | grep -i "leggi_bytes"
```

Atteso: FAIL con `eccezione AttributeError: module 'delugexml.midi' has no attribute 'leggi_bytes'`.

- [ ] **Passo 3: implementare**

In `tools/delugexml/midi.py`, sostituire la firma di `leggi()` e aggiungere la
nuova funzione. Il corpo di `leggi()` resta identico: cambia solo da dove
arrivano i byte e cosa compare nei messaggi d'errore.

```python
def leggi(path: Path | str) -> FileMidi:
    """Legge uno Standard MIDI File. Nessuna dipendenza esterna."""
    return leggi_bytes(Path(path).read_bytes(), nome=str(path))


def leggi_bytes(dati: bytes, nome: str = '<bytes>') -> FileMidi:
    """Come `leggi()`, ma da byte gia' in memoria.

    Serve a leggere un MIDI che sta DENTRO un archivio senza estrarlo, che e'
    la regola di HANDOFF §6-duodecies. `nome` compare solo nei messaggi
    d'errore, per dire di quale file si sta parlando.
    """
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
        raise ValueError(f'{nome}: non e uno Standard MIDI File (manca MThd)')
    formato, _ntracce, divisione = testa
    if divisione <= 0:
        raise ValueError(
            f'{nome}: divisione SMPTE ({divisione}), non PPQ. Non gestita: '
            'nel materiale musicale non si incontra praticamente mai, e '
            'indovinarla sarebbe peggio che rifiutarla.')
    return FileMidi(formato=formato, ppq=divisione, bpm=bpm, metro=metro,
                    tracce=tracce)
```

- [ ] **Passo 4: farlo girare e vederlo passare**

```bash
cd /d/DelugePal && python tests/test_all.py 2>&1 | tail -5
```

Atteso: il conteggio finale sale di 3 test e non compare nessun FAIL.
Se POP909 non c'è, il test SALTA: va bene, ma allora **verificarlo a mano** su
un qualunque `.mid` presente in `to-read/`.

- [ ] **Passo 5: commit**

```bash
git add tools/delugexml/midi.py tests/test_all.py && git commit -m "midi: leggi_bytes(), per leggere un MIDI dentro un archivio"
```

---

## Task 2: `jtd.py` — apertura, elenco, metadati

**File:**
- Crea: `tools/delugexml/jtd.py`
- Test: `tests/test_all.py` (in coda)

**Interfacce:**
- Consuma: niente.
- Produce: `RADICE`, `STRUMENTI`, `Brano`, `apri(path) -> zipfile.ZipFile`,
  `_zip(sorgente) -> tuple[zipfile.ZipFile, bool]`,
  `elenco(sorgente, *, pianista=None, bassista=None, batterista=None,
  metro=None, curati=False, limite=None) -> list[Brano]`,
  `metadati(sorgente, fname) -> dict`.

- [ ] **Passo 1: scrivere il test che fallisce**

```python
def test_jtd_elenco():
    """L'indice del Jazz Trio Database. SALTA se il corpus non c'e'.

    I valori attesi vengono dal corpus stesso, che qui e' l'artefatto in
    esame. Il primo brano in ordine alfabetico e' `All God's Children` di
    Kenny Barron, 1990, con Ray Drummond al basso e Ben Riley alla batteria.
    """
    from delugexml import jtd as JT                         # noqa: PLC0415

    zip_ = ROOT / 'to-read' / 'MIDI' / 'jazz-trio-database-v02.zip'
    if not zip_.exists():
        raise FileNotFoundError(str(zip_))

    with JT.apri(zip_) as z:
        tutti = JT.elenco(z)
        check('il corpus ha 1294 brani', len(tutti) == 1294, str(len(tutti)))

        b = tutti[0]
        check('il primo e Kenny Barron', b.pianista == 'Kenny Barron', b.pianista)
        check('con Ray Drummond al basso', b.bassista == 'Ray Drummond', b.bassista)
        check('e Ben Riley alla batteria', b.batterista == 'Ben Riley', b.batterista)
        check('in 4/4', b.metro == 4, str(b.metro))
        check('del 1990', b.anno == 1990, str(b.anno))

        curati = JT.elenco(z, curati=True)
        check('JTD-300 ha 300 brani', len(curati) == 300, str(len(curati)))

        tre = JT.elenco(z, metro=3)
        check('90 brani in 3/4', len(tre) == 90, str(len(tre)))
        check('e il filtro sul metro non lascia passare altro',
              all(x.metro == 3 for x in tre))

        suoi = JT.elenco(z, bassista='Ray Drummond')
        check('il filtro sul bassista tiene',
              suoi and all(x.bassista == 'Ray Drummond' for x in suoi),
              f'{len(suoi)} brani')

        m = JT.metadati(z, b.fname)
        check('i NaN di metadata.json diventano None',
              m['first_downbeat'] is None, repr(m['first_downbeat']))
        check('e i campi buoni restano',
              m['track_name'] == 'All Gods Children', m['track_name'])
```

- [ ] **Passo 2: farlo girare e vederlo fallire**

```bash
cd /d/DelugePal && python tests/test_all.py 2>&1 | grep -i "jtd"
```

Atteso: FAIL con `eccezione ModuleNotFoundError: No module named 'delugexml.jtd'`.

- [ ] **Passo 3: implementare**

Creare `tools/delugexml/jtd.py`:

```python
"""Leggere il Jazz Trio Database: il trio che suona INSIEME.

PERCHE' ESISTE
--------------
Fino al 1 settembre 2026 l'handoff diceva, in tre punti, che «nessun corpus
in casa ha l'insieme che suona insieme -- non e' questione di quanti dati, e'
che il dato non c'e'», e da li' faceva discendere che il prossimo passo fosse
un lettore di partiture MusicXML. La riga era falsa in due modi:

  1. il dato ESISTE e ha una licenza: il Jazz Trio Database (Cheston,
     Schlichting, Cross, Harrison -- TISMIR 2024, MIT) porta 1294 esecuzioni
     di trio jazz con gli onset di PIANO, BASSO E BATTERIA allineati agli
     STESSI beat;
  2. il MusicXML non l'avrebbe risolta comunque: nel piu' grande corpus
     libero (PDMX, 250 000 spartiti di pubblico dominio) oltre il 90% ha meno
     di cinque parti e piu' della meta' sono pezzi solistici. Niente batteria.

Serve alla casella 5 di `docs/repertori/jazz.md`, «ruoli e spartizione», che
il 30 agosto 2026 ha fermato tre lavori in un giorno solo.

COSA PORTA, E COSA NO
---------------------
Porta: quando ciascuno dei tre ha suonato, rispetto a un beat comune e alla
posizione nella battuta; e le altezze del PIANO, che ha il suo MIDI.

NON porta: le altezze di basso e batteria, e nemmeno QUALE pezzo di batteria
ha suonato -- gli onset sono aggregati. Qualunque affermazione del tipo «il
rullante fa X» non e' ricavabile da qui, e va rifiutata invece che stimata.

LO ZIP NON SI DECOMPRIME
------------------------
Regola di HANDOFF §6-duodecies: `zipfile` e' stdlib, i membri si leggono in
memoria. Chi cicla su tante tracce apre lo zip UNA volta con `apri()` e passa
l'oggetto; chi fa una chiamata sola puo' passare il percorso, e in quel caso
la funzione apre e richiude da se'.
"""
from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path
from typing import NamedTuple

from . import midi

#: La cartella che lo zip si porta dentro. Cambia col numero di versione del
#: corpus, quindi sta qui e non sparsa nel codice.
RADICE = 'jazz-trio-database-v02'

#: I tre strumenti, nei nomi che il corpus usa nelle sue colonne e nei suoi
#: nomi di file. Non tradotti apposta: sono chiavi di dati altrui.
STRUMENTI = ('piano', 'bass', 'drums')


class Brano(NamedTuple):
    """Un'esecuzione, coi campi che servono per sceglierla."""

    fname: str
    titolo: str
    album: str
    anno: int | None
    pianista: str
    bassista: str
    batterista: str
    metro: int
    tempo: float | None
    #: sta nel sottoinsieme curato JTD-300 (`in_30_corpus`)
    curato: bool
    #: ha una validazione manuale (`has_annotations`): solo 34 su 1294
    validato: bool

    def __str__(self) -> str:
        t = f'{self.tempo:.0f} bpm' if self.tempo else 'tempo ignoto'
        return (f'{self.pianista} - {self.titolo} ({self.anno}), '
                f'basso {self.bassista}, batteria {self.batterista}, '
                f'{self.metro}/4, {t}')


def apri(path: Path | str) -> zipfile.ZipFile:
    """Lo zip del corpus. Solleva `FileNotFoundError` se non c'e'.

    L'eccezione e' quella giusta di proposito: la suite la traduce in un
    SALTO, perche' il corpus non appartiene a questo repo.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))
    return zipfile.ZipFile(p)


def _zip(sorgente: zipfile.ZipFile | Path | str) -> tuple[zipfile.ZipFile, bool]:
    """Lo zip, e se l'abbiamo aperto noi (e quindi tocca a noi chiuderlo)."""
    if isinstance(sorgente, zipfile.ZipFile):
        return sorgente, False
    return apri(sorgente), True


def _senza_nan(v):
    """`metadata.json` usa `NaN` per «non lo so»: diventa `None`.

    `json` di Python accetta `NaN` -- non e' JSON stretto, e altri lettori lo
    rifiutano. Normalizzarlo all'ingresso evita che un `float('nan')` giri per
    il codice, dove ogni confronto con lui e' falso, `==` compreso.
    """
    if isinstance(v, float) and v != v:
        return None
    if isinstance(v, dict):
        return {k: _senza_nan(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_senza_nan(x) for x in v]
    return v


def metadati(sorgente, fname: str) -> dict:
    """Il `metadata.json` di un brano, coi `NaN` gia' resi `None`."""
    z, nostro = _zip(sorgente)
    try:
        return _senza_nan(json.loads(z.read(f'{RADICE}/{fname}/metadata.json')))
    finally:
        if nostro:
            z.close()


def _in_brano(m: dict, fname: str) -> Brano:
    mus = m.get('musicians') or {}
    anno = m.get('recording_year')
    return Brano(
        fname=fname,
        titolo=m.get('track_name') or '',
        album=m.get('album_name') or '',
        anno=int(anno) if anno else None,
        pianista=mus.get('pianist') or '',
        bassista=mus.get('bassist') or '',
        batterista=mus.get('drummer') or '',
        metro=int(m.get('time_signature') or 4),
        tempo=m.get('tempo'),
        curato=bool(m.get('in_30_corpus')),
        validato=bool(m.get('has_annotations')),
    )


def nomi(sorgente) -> list[str]:
    """I `fname` dei brani, in ordine alfabetico."""
    z, nostro = _zip(sorgente)
    try:
        coda = '/metadata.json'
        return sorted(n.split('/')[1] for n in z.namelist() if n.endswith(coda))
    finally:
        if nostro:
            z.close()


def elenco(sorgente, *, pianista: str | None = None,
           bassista: str | None = None, batterista: str | None = None,
           metro: int | None = None, curati: bool = False,
           limite: int | None = None) -> list[Brano]:
    """I brani che rispondono ai filtri.

    I nomi dei musicisti sono quelli del corpus, per esteso e con le maiuscole
    («Ray Drummond»): un nome scritto diversamente da' una lista vuota invece
    di un errore. `curati=True` restringe al sottoinsieme JTD-300.
    """
    z, nostro = _zip(sorgente)
    try:
        fuori = []
        for fname in nomi(z):
            b = _in_brano(metadati(z, fname), fname)
            if pianista is not None and b.pianista != pianista:
                continue
            if bassista is not None and b.bassista != bassista:
                continue
            if batterista is not None and b.batterista != batterista:
                continue
            if metro is not None and b.metro != metro:
                continue
            if curati and not b.curato:
                continue
            fuori.append(b)
            if limite is not None and len(fuori) >= limite:
                break
        return fuori
    finally:
        if nostro:
            z.close()
```

- [ ] **Passo 4: farlo girare e vederlo passare**

```bash
cd /d/DelugePal && python tests/test_all.py 2>&1 | grep -iE "jtd|test superati"
```

Atteso: tutti PASS. `elenco()` legge 1294 file JSON dallo zip: sui 3-4 secondi.
Se supera i 30 secondi, il collo di bottiglia è l'apertura ripetuta dello zip —
verificare che il test passi `z` e non il percorso.

- [ ] **Passo 5: commit**

```bash
git add tools/delugexml/jtd.py tests/test_all.py && git commit -m "jtd: l'elenco dei 1294 trii, letto dentro lo zip"
```

---

## Task 3: `jtd.py` — la griglia dei beat

**File:**
- Modifica: `tools/delugexml/jtd.py` (in coda)
- Test: `tests/test_all.py` (in coda)

**Interfacce:**
- Consuma: `RADICE`, `STRUMENTI`, `_zip` dal Task 2.
- Produce: `Beat(indice, istante, posizione, scarti)` con
  `scarti: dict[str, float | None]`, e `griglia(sorgente, fname) -> list[Beat]`.

- [ ] **Passo 1: scrivere il test che fallisce**

```python
def test_jtd_griglia():
    """La griglia dei beat, e la colonna vuota che vale piu' di tutte.

    In `beats.csv` una cella vuota vuol dire che QUELLO strumento non ha
    suonato su QUEL beat. E' il dato su cui poggia la casella 5: un walking
    vero lascia buchi, e qui si vede dove.

    I valori attesi vengono dal corpus: il primo brano ha 762 beat, comincia
    in terza posizione di battuta (l'estratto parte a meta' battuta) e il
    basso tace su 17 di quei beat.
    """
    from delugexml import jtd as JT                         # noqa: PLC0415

    zip_ = ROOT / 'to-read' / 'MIDI' / 'jazz-trio-database-v02.zip'
    if not zip_.exists():
        raise FileNotFoundError(str(zip_))
    fname = 'barronk-allgodschildren-drummondrrileyb-1990-8b77c067'

    with JT.apri(zip_) as z:
        g = JT.griglia(z, fname)
        check('762 beat', len(g) == 762, str(len(g)))
        check('il primo cade a 0,08 s', abs(g[0].istante - 0.08) < 1e-9,
              str(g[0].istante))
        check('in terza posizione di battuta', g[0].posizione == 3,
              str(g[0].posizione))
        check('le posizioni stanno tutte dentro il metro',
              all(1 <= b.posizione <= 4 for b in g))

        muti = {s: sum(1 for b in g if b.scarti[s] is None)
                for s in JT.STRUMENTI}
        check('il basso tace su 17 beat', muti['bass'] == 17, str(muti['bass']))
        check('la batteria su 136', muti['drums'] == 136, str(muti['drums']))
        check('il piano su 217', muti['piano'] == 217, str(muti['piano']))

        # lo scarto e' l'onset MENO l'istante del beat: piccolo, e con segno.
        scarti = [b.scarti['bass'] for b in g if b.scarti['bass'] is not None]
        check('gli scarti sono piccoli e hanno segno',
              max(abs(s) for s in scarti) < 0.5 and min(scarti) < 0 < max(scarti),
              f'da {min(scarti):.3f} a {max(scarti):.3f} s')
```

- [ ] **Passo 2: farlo girare e vederlo fallire**

```bash
cd /d/DelugePal && python tests/test_all.py 2>&1 | grep -i "jtd_griglia"
```

Atteso: FAIL con `eccezione AttributeError: module 'delugexml.jtd' has no attribute 'griglia'`.

- [ ] **Passo 3: implementare**

In coda a `tools/delugexml/jtd.py`:

```python
class Beat(NamedTuple):
    """Un beat, e chi c'era sopra.

    `scarti` vale, per ogni strumento, l'onset MENO l'istante del beat: il
    segno dice chi tira avanti e chi trattiene. `None` vuol dire che quello
    strumento NON ha suonato su questo beat, ed e' un'informazione, non un
    buco nei dati -- ⚠️ salvo quando e' un fallimento del rilevatore, che e'
    il controllo 2 di `misura_spartizione.py`.
    """

    indice: int
    istante: float
    #: 1..metro, da `metre_auto`. 1 e' il tempo forte.
    posizione: int
    scarti: dict[str, float | None]

    def tace(self, strumento: str) -> bool:
        return self.scarti[strumento] is None


def _numero(testo: str) -> float | None:
    """Una cella di CSV: `None` se e' vuota o `nan`."""
    testo = (testo or '').strip()
    if not testo or testo.lower() == 'nan':
        return None
    return float(testo)


def griglia(sorgente, fname: str) -> list[Beat]:
    """I beat di un brano, con la posizione metrica e i tre allineamenti."""
    z, nostro = _zip(sorgente)
    try:
        testo = z.read(f'{RADICE}/{fname}/beats.csv').decode('utf-8')
    finally:
        if nostro:
            z.close()

    fuori = []
    for i, riga in enumerate(csv.DictReader(io.StringIO(testo))):
        istante = _numero(riga['beats'])
        posizione = _numero(riga['metre_auto'])
        if istante is None or posizione is None:
            # Non si e' mai visto su 32 110 beat controllati, ma se capitasse
            # un beat senza istante o senza posizione non e' un beat.
            continue
        fuori.append(Beat(
            indice=i,
            istante=istante,
            posizione=int(posizione),
            scarti={s: (None if _numero(riga[s]) is None
                        else _numero(riga[s]) - istante) for s in STRUMENTI},
        ))
    return fuori
```

- [ ] **Passo 4: farlo girare e vederlo passare**

```bash
cd /d/DelugePal && python tests/test_all.py 2>&1 | grep -iE "jtd_griglia|test superati"
```

Atteso: tutti PASS.

- [ ] **Passo 5: commit**

```bash
git add tools/delugexml/jtd.py tests/test_all.py && git commit -m "jtd: la griglia dei beat, e la cella vuota che dice chi taceva"
```

---

## Task 4: `jtd.py` — onset, battute, e il piano

**File:**
- Modifica: `tools/delugexml/jtd.py` (in coda)
- Test: `tests/test_all.py` (in coda)

**Interfacce:**
- Consuma: `Beat`, `griglia`, `_zip`, `STRUMENTI`, `midi.leggi_bytes` (Task 1).
- Produce: `onsets(sorgente, fname, strumento) -> list[float]`,
  `Battuta(numero, inizio, fine, beat, onsets)` con proprietà `densita`,
  `Divisione(battute, scartate)`, `battute(sorgente, fname) -> Divisione`,
  `piano(sorgente, fname) -> midi.FileMidi`.

- [ ] **Passo 1: scrivere il test che fallisce**

```python
def test_jtd_battute():
    """Le battute complete, e quante se ne buttano ai bordi.

    Il primo brano da' 189 battute complete: l'estratto comincia a meta'
    battuta e finisce senza chiudere l'ultima, e quei due mozziconi si
    scartano invece di contarli come battute corte -- che falserebbero ogni
    densita'.

    ⚠️ E qui c'e' gia' la risposta alla domanda che apre la casella 5. Il
    generatore fa 4,00 note di basso per battuta con deviazione ZERO. Ray
    Drummond, in questo brano solo, fa 3 in 18 battute, 4 in 135, 5 in 33,
    6 in 2 e 7 in 1.
    """
    from delugexml import jtd as JT                         # noqa: PLC0415
    import collections                                      # noqa: PLC0415

    zip_ = ROOT / 'to-read' / 'MIDI' / 'jazz-trio-database-v02.zip'
    if not zip_.exists():
        raise FileNotFoundError(str(zip_))
    fname = 'barronk-allgodschildren-drummondrrileyb-1990-8b77c067'

    with JT.apri(zip_) as z:
        o = JT.onsets(z, fname, 'bass')
        check('783 onset di basso', len(o) == 783, str(len(o)))
        check('il primo a 0,09 s', abs(o[0] - 0.09) < 1e-9, str(o[0]))
        check('e sono in ordine', o == sorted(o))

        d = JT.battute(z, fname)
        check('189 battute complete', len(d.battute) == 189,
              str(len(d.battute)))
        check('e lo dice quante ne ha scartate', d.scartate >= 1,
              str(d.scartate))
        check('ogni battuta ha 4 beat',
              all(len(b.beat) == 4 for b in d.battute))
        check('e i beat cominciano sul tempo forte',
              all(b.beat[0].posizione == 1 for b in d.battute))

        dens = collections.Counter(b.densita['bass'] for b in d.battute)
        check('la densita del basso NON e costante',
              dict(sorted(dens.items())) == {3: 18, 4: 135, 5: 33, 6: 2, 7: 1},
              str(dict(sorted(dens.items()))))

        f = JT.piano(z, fname)
        check('il MIDI del piano si legge dentro lo zip',
              len(f.note) > 0, f'{len(f.note)} note')
```

- [ ] **Passo 2: farlo girare e vederlo fallire**

```bash
cd /d/DelugePal && python tests/test_all.py 2>&1 | grep -i "jtd_battute"
```

Atteso: FAIL con `AttributeError: ... has no attribute 'onsets'`.

- [ ] **Passo 3: implementare**

In coda a `tools/delugexml/jtd.py`:

```python
class Battuta(NamedTuple):
    """Una battuta completa, e cosa ci hanno suonato dentro i tre.

    `onsets` porta gli onset GREZZI, quelli fra i beat compresi: e' la
    differenza fra «il basso ha suonato sul 2» e «il basso ha suonato una
    crome fra il 2 e il 3», e la seconda e' meta' di quello che si vuole
    sapere.
    """

    numero: int
    inizio: float
    fine: float
    beat: tuple[Beat, ...]
    onsets: dict[str, tuple[float, ...]]

    @property
    def densita(self) -> dict[str, int]:
        """Quanti onset per strumento, in questa battuta."""
        return {s: len(self.onsets[s]) for s in STRUMENTI}


class Divisione(NamedTuple):
    """Le battute complete, e quante se ne sono buttate.

    Dichiara lo scarto invece di tacerlo, come `Conversione` in `midi.py`:
    un brano che perde meta' delle battute non e' un brano da cui misurare.
    """

    battute: list[Battuta]
    scartate: int

    def __str__(self) -> str:
        return (f'{len(self.battute)} battute complete, {self.scartate} '
                f'scartate perche incomplete')


def onsets(sorgente, fname: str, strumento: str) -> list[float]:
    """Gli onset grezzi di uno strumento, in secondi e in ordine."""
    if strumento not in STRUMENTI:
        raise ValueError(f'strumento {strumento!r}: usare uno di {STRUMENTI}')
    z, nostro = _zip(sorgente)
    try:
        testo = z.read(f'{RADICE}/{fname}/{strumento}_onsets.csv').decode('utf-8')
    finally:
        if nostro:
            z.close()
    # Il file e' una colonna sola, senza intestazione.
    return sorted(float(r) for r in testo.splitlines() if r.strip())


def battute(sorgente, fname: str) -> Divisione:
    """Le battute COMPLETE di un brano, con gli onset dei tre dentro.

    Una battuta e' completa quando i suoi `metro` beat portano le posizioni
    1..metro in fila E c'e' un beat dopo che la chiude: senza quello non si
    sa dove finisce, e una battuta senza fine falserebbe la densita' in
    difetto. I mozziconi si scartano; `scartate` conta quelli che
    COMINCIAVANO sul tempo forte e non si sono chiusi -- il mozzicone di
    testa, che comincia a meta' battuta, non e' una battuta mancata e non si
    conta.
    """
    z, nostro = _zip(sorgente)
    try:
        metro = _in_brano(metadati(z, fname), fname).metro
        g = griglia(z, fname)
        tutti = {s: onsets(z, fname, s) for s in STRUMENTI}
    finally:
        if nostro:
            z.close()

    fuori: list[Battuta] = []
    scartate = 0
    i = 0
    while i < len(g):
        gruppo = g[i:i + metro]
        completa = (len(gruppo) == metro
                    and [b.posizione for b in gruppo] == list(range(1, metro + 1))
                    and i + metro < len(g))
        if not completa:
            if g[i].posizione == 1:
                scartate += 1
            i += 1
            continue
        inizio, fine = gruppo[0].istante, g[i + metro].istante
        fuori.append(Battuta(
            numero=len(fuori),
            inizio=inizio,
            fine=fine,
            beat=tuple(gruppo),
            onsets={s: tuple(o for o in tutti[s] if inizio <= o < fine)
                    for s in STRUMENTI},
        ))
        i += metro
    return Divisione(battute=fuori, scartate=scartate)


def piano(sorgente, fname: str) -> midi.FileMidi:
    """Il `piano_midi.mid` del brano, letto DENTRO lo zip.

    E' l'unico dei tre strumenti che porta le altezze: basso e batteria hanno
    solo gli onset.
    """
    z, nostro = _zip(sorgente)
    try:
        dati = z.read(f'{RADICE}/{fname}/piano_midi.mid')
    finally:
        if nostro:
            z.close()
    return midi.leggi_bytes(dati, nome=f'{fname}/piano_midi.mid')
```

- [ ] **Passo 4: farlo girare e vederlo passare**

```bash
cd /d/DelugePal && python tests/test_all.py 2>&1 | grep -iE "jtd_battute|densita del basso|test superati"
```

Atteso: tutti PASS, compreso `la densita del basso NON e costante`.
⚠️ Se quel test fallisce coi conteggi spostati di poco, il colpevole è quasi
sempre il confronto sui bordi (`inizio <= o < fine`): un onset esattamente sul
confine deve appartenere alla battuta che comincia, non a quella che finisce.

- [ ] **Passo 5: commit**

```bash
git add tools/delugexml/jtd.py tests/test_all.py && git commit -m "jtd: le battute complete, e il primo numero che smentisce il generatore"
```

---

## Task 5: i cinque controlli, PRIMA di qualunque misura

**File:**
- Crea: `tools/controlla_jtd.py`
- Produce: `out/controlli_jtd.txt`

**Interfacce:**
- Consuma: tutto `jtd.py` (Task 2-4).
- Produce: nessuna API. Produce **un verdetto**: se il controllo 1 fallisce, il
  piano si ferma e si ripianifica.

⚠️ **Questo compito è un cancello, non un adempimento.** Ognuno dei cinque, se
salta, rende sbagliata ogni cifra a valle **senza far fallire un test**.

- [ ] **Passo 1: scrivere lo strumento**

Creare `tools/controlla_jtd.py`:

```python
"""I controlli da passare PRIMA di fidarsi di un numero preso dal JTD.

    .venv/Scripts/python.exe tools/controlla_jtd.py > out/controlli_jtd.txt

Nessuno di questi cinque fa fallire un test se salta: sbaglierebbero in
silenzio ogni misura a valle. Per questo stanno in uno strumento a parte e il
loro esito si SCRIVE, anche quando l'esito e' «va bene».
"""
from __future__ import annotations

import collections
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import jtd as JT                             # noqa: E402

ZIP = Path(__file__).resolve().parent.parent / 'to-read' / 'MIDI' / \
    'jazz-trio-database-v02.zip'

#: Quanto lontano da un beat puo' stare un onset perche' si possa dire che
#: «e' quel beat». 50 ms a 200 bpm sono un sesto di beat: larga abbastanza da
#: assorbire il rilevatore, stretta abbastanza da non inghiottire una croma.
FINESTRA_VICINO = 0.050


def uno_il_beat_e_quello_che_il_tempo_conta(z, brani):
    """CONTROLLO 1. Se il beat annotato non fosse quello del tempo dichiarato,
    ogni densita' «per battuta» sarebbe sbagliata di un fattore due."""
    rapporti = []
    for b in brani:
        g = JT.griglia(z, b.fname)
        if len(g) < 8 or not b.tempo:
            continue
        ibi = st.median([y.istante - x.istante for x, y in zip(g, g[1:])])
        if ibi > 0:
            rapporti.append((60 / ibi) / b.tempo)
    r = sorted(rapporti)
    print('CONTROLLO 1 -- il beat annotato e quello che il tempo conta')
    print(f'   (60/intervallo) / tempo dichiarato, su {len(r)} brani:')
    print(f'   mediana {st.median(r):.4f}   min {r[0]:.3f}   max {r[-1]:.3f}')
    ok = 0.95 < st.median(r) < 1.05
    print(f'   ESITO: {"passa" if ok else "NON PASSA -- FERMARSI"}')
    return ok


def due_la_cella_vuota_e_un_silenzio(z, brani):
    """CONTROLLO 2. Una cella vuota deve voler dire «non ha suonato». Se in
    quell'intorno un onset grezzo c'e', e' il rilevatore che ha mancato
    l'allineamento, e allora la misura 2 conta errori invece che silenzi."""
    muti = smentiti = 0
    for b in brani:
        g = JT.griglia(z, b.fname)
        ons = JT.onsets(z, b.fname, 'bass')
        i = 0
        for beat in g:
            if not beat.tace('bass'):
                continue
            muti += 1
            while i < len(ons) and ons[i] < beat.istante - FINESTRA_VICINO:
                i += 1
            if i < len(ons) and abs(ons[i] - beat.istante) <= FINESTRA_VICINO:
                smentiti += 1
    perc = 100 * smentiti / muti if muti else 0.0
    print('\nCONTROLLO 2 -- la cella vuota e un silenzio, non un errore')
    print(f'   beat in cui il basso tace: {muti}')
    print(f'   di questi, con un onset grezzo entro {FINESTRA_VICINO*1000:.0f} ms: '
          f'{smentiti} ({perc:.1f}%)')
    print(f'   ESITO: {"passa" if perc < 10 else "ATTENZIONE: va dichiarato"}')
    return perc


def tre_i_nan_sono_spariti(z, brani):
    """CONTROLLO 3. Nessun `float(nan)` deve uscire da `metadati()`: ogni
    confronto con lui e' falso, `==` compreso, e sbaglia in silenzio."""
    trovati = 0
    for b in brani:
        for v in JT.metadati(z, b.fname).values():
            if isinstance(v, float) and v != v:
                trovati += 1
    print('\nCONTROLLO 3 -- i NaN di metadata.json sono diventati None')
    print(f'   NaN sopravvissuti: {trovati}')
    print(f'   ESITO: {"passa" if trovati == 0 else "NON PASSA"}')
    return trovati == 0


def quattro_i_tre_quarti_stanno_a_parte(z):
    """CONTROLLO 4. Una densita' per battuta mediata fra 3/4 e 4/4 non vuol
    dire niente. Si contano e si tengono fuori."""
    q = JT.elenco(z, metro=4)
    t = JT.elenco(z, metro=3)
    print('\nCONTROLLO 4 -- i 3/4 stanno a parte')
    print(f'   brani in 4/4: {len(q)}   in 3/4: {len(t)}')
    print('   ESITO: le misure girano sui soli 4/4, e il numero dei 3/4 si cita')
    return len(q), len(t)


def cinque_il_campione_regge(z, brani):
    """CONTROLLO 5. Quanti esecutori distinti reggono i numeri, e quanto pesa
    il piu' rappresentato: un corpus dominato da un bassista solo misurerebbe
    lui, non il repertorio. E' la trappola della casella 6 del reggae."""
    per_bassista = collections.Counter(b.bassista for b in brani)
    per_batterista = collections.Counter(b.batterista for b in brani)
    print('\nCONTROLLO 5 -- il campione regge')
    for nome, c in (('bassisti', per_bassista), ('batteristi', per_batterista)):
        primo, quante = c.most_common(1)[0]
        print(f'   {nome}: {len(c)} distinti; il piu presente e {primo} '
              f'con {quante} brani ({100*quante/sum(c.values()):.1f}%)')
    return per_bassista, per_batterista


def main() -> int:
    if not ZIP.exists():
        print(f'manca {ZIP}')
        return 1
    with JT.apri(ZIP) as z:
        brani = JT.elenco(z, metro=4)
        print(f'JTD: {len(brani)} brani in 4/4\n')
        if not uno_il_beat_e_quello_che_il_tempo_conta(z, brani):
            print('\n⚠️ FERMARSI: il controllo 1 non passa.')
            return 2
        due_la_cella_vuota_e_un_silenzio(z, brani)
        tre_i_nan_sono_spariti(z, brani)
        quattro_i_tre_quarti_stanno_a_parte(z)
        cinque_il_campione_regge(z, brani)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

⚠️ Togliere il carattere `⚠️` dalla riga di `print` prima di eseguire, oppure
sostituirlo con `ATTENZIONE:`: l'output va in `out/` e la console di Windows è
cp1252. Il vincolo globale «output in ASCII puro» vale anche qui.

- [ ] **Passo 2: eseguirlo**

```bash
cd /d/DelugePal && .venv/Scripts/python.exe tools/controlla_jtd.py > out/controlli_jtd.txt 2>&1; type out\controlli_jtd.txt
```

Atteso sul controllo 1: mediana ≈ **0,996**, min ≈ 0,978, max ≈ 1,021 —
misurato su 40 brani il 1 settembre 2026. **Se la mediana non sta fra 0,95 e
1,05 il piano si ferma qui** e si ripianifica: vorrebbe dire che il beat
annotato non è quello che il tempo conta.

Sugli altri quattro non c'è un valore atteso: sono la prima misura che ne
produce uno.

- [ ] **Passo 3: scrivere l'esito nella spec**

Aggiungere in fondo alla sezione «I controlli da fare PRIMA di fidarsi di
qualunque numero» di
`docs/superpowers/specs/2026-09-01-jtd-spartizione-design.md` una tabella
`controllo | esito | numero`, con i cinque risultati veri. **Anche quelli che
passano**: un controllo il cui esito non è scritto non è stato fatto.

- [ ] **Passo 4: commit**

```bash
git add tools/controlla_jtd.py out/controlli_jtd.txt docs/superpowers/specs/2026-09-01-jtd-spartizione-design.md && git commit -m "jtd: i cinque controlli, e il beat annotato e' quello giusto"
```

---

## Task 6: misure 1 e 2 — il basso

**File:**
- Crea: `tools/misura_spartizione.py`
- Produce: `out/spartizione_jazz.txt`

**Interfacce:**
- Consuma: `jtd.battute`, `jtd.griglia`, `jtd.elenco`.
- Produce: `densita_del_basso(z, brani) -> dict`,
  `il_beat_saltato(z, brani) -> dict`, e la costante `MINIMO_BATTUTE`.

- [ ] **Passo 1: scrivere lo strumento**

```python
"""Come il trio si spartisce la battuta: la misura della casella 5.

    .venv/Scripts/python.exe tools/misura_spartizione.py > out/spartizione_jazz.txt

Risponde al difetto sentito il 30 agosto 2026, che l'utente ha detto cosi':
«le interruzioni, accenti e struttura delle parti di batteria sono
strettamente correlati alla sezione ritmica, e non le puoi applicare
acriticamente». Misurato allora sui tre pezzi generati: deviazione standard
dei colpi per battuta, batteria 1,48-1,65, comping 0,54-0,61, basso 0,00.

⚠️ IL BASSO NON VARIA MAI: 4,00 note per battuta, zero battute diverse da
quattro su 228. Qui si misura di quanto varia un bassista vero.

TUTTE LE SOGLIE STANNO QUI, non in `jtd.py`: il lettore non decide niente di
musicale. Ognuna porta accanto la frase che la giustifica.
"""
from __future__ import annotations

import collections
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import jtd as JT                             # noqa: E402

ZIP = Path(__file__).resolve().parent.parent / 'to-read' / 'MIDI' / \
    'jazz-trio-database-v02.zip'

#: Sotto questo numero di battute complete un brano non entra nelle medie:
#: un estratto corto da' distribuzioni che dipendono da dove e' stato
#: tagliato piu' che da chi suona.
MINIMO_BATTUTE = 32


def _brani(z, curati: bool):
    return JT.elenco(z, metro=4, curati=curati)


def densita_del_basso(z, brani) -> dict:
    """MISURA 1. Quanti onset di basso per battuta, e quanto si scostano.

    Il confronto e' col generatore: 4,00 esatte, deviazione 0,00.
    """
    per_battuta = collections.Counter()
    medie, deviazioni, esecutori, usati = [], [], set(), 0
    for b in brani:
        d = JT.battute(z, b.fname)
        if len(d.battute) < MINIMO_BATTUTE:
            continue
        usati += 1
        esecutori.add(b.bassista)
        conti = [x.densita['bass'] for x in d.battute]
        per_battuta.update(conti)
        medie.append(st.mean(conti))
        deviazioni.append(st.pstdev(conti))
    tot = sum(per_battuta.values())
    print('MISURA 1 -- la densita del basso per battuta')
    print(f'   {tot} battute, {usati} esecuzioni, {len(esecutori)} bassisti')
    print('   note per battuta   battute   %')
    for n in sorted(per_battuta):
        print(f'   {n:16}   {per_battuta[n]:7}   {100*per_battuta[n]/tot:5.1f}')
    print(f'   media per esecuzione: mediana {st.median(medie):.2f}')
    print(f'   deviazione entro l esecuzione: mediana {st.median(deviazioni):.2f}')
    print(f'   -> il generatore fa 4,00 con deviazione 0,00')
    return {'per_battuta': dict(per_battuta), 'esecuzioni': usati,
            'esecutori': len(esecutori),
            'deviazione_mediana': st.median(deviazioni)}


def il_beat_saltato(z, brani) -> dict:
    """MISURA 2. Quanto spesso il basso NON suona sul beat, e su quale.

    ⚠️ Il numero grezzo va corretto col controllo 2: una parte di questi
    silenzi e' il rilevatore che ha mancato l'allineamento.
    """
    per_posizione = collections.Counter()
    beat_per_posizione = collections.Counter()
    esecutori, usati = set(), 0
    for b in brani:
        g = JT.griglia(z, b.fname)
        if len(g) < MINIMO_BATTUTE * 4:
            continue
        usati += 1
        esecutori.add(b.bassista)
        for beat in g:
            beat_per_posizione[beat.posizione] += 1
            if beat.tace('bass'):
                per_posizione[beat.posizione] += 1
    tot_muti = sum(per_posizione.values())
    tot = sum(beat_per_posizione.values())
    print('\nMISURA 2 -- il beat su cui il basso tace')
    print(f'   {tot} beat, {usati} esecuzioni, {len(esecutori)} bassisti')
    print(f'   il basso tace su {tot_muti} beat ({100*tot_muti/tot:.1f}%)')
    print('   posizione   beat   taciuti   %')
    for p in sorted(beat_per_posizione):
        q = per_posizione[p]
        print(f'   {p:9}   {beat_per_posizione[p]:6}   {q:7}   '
              f'{100*q/beat_per_posizione[p]:5.1f}')
    return {'per_posizione': dict(per_posizione), 'esecuzioni': usati,
            'esecutori': len(esecutori)}


def main() -> int:
    if not ZIP.exists():
        print(f'manca {ZIP}')
        return 1
    with JT.apri(ZIP) as z:
        brani = _brani(z, curati=False)
        print(f'JTD -- {len(brani)} esecuzioni in 4/4\n')
        densita_del_basso(z, brani)
        il_beat_saltato(z, brani)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

- [ ] **Passo 2: eseguirlo su un campione e controllare a occhio**

Prima su pochi brani, per non aspettare 1204 letture:

```bash
cd /d/DelugePal && .venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tools'); from delugexml import jtd as JT; import misura_spartizione as M; z=JT.apri(M.ZIP); b=JT.elenco(z, metro=4, limite=25); M.densita_del_basso(z,b); M.il_beat_saltato(z,b)"
```

Atteso: la distribuzione ha una **moda a 4** e code su 3 e 5, e la deviazione
mediana entro l'esecuzione è **maggiore di zero**. Se uscisse 0,00, il bug è
in `battute()`, non nel corpus.

- [ ] **Passo 3: girarlo intero e salvare**

```bash
cd /d/DelugePal && .venv/Scripts/python.exe tools/misura_spartizione.py > out/spartizione_jazz.txt 2>&1; type out\spartizione_jazz.txt
```

- [ ] **Passo 4: commit**

```bash
git add tools/misura_spartizione.py out/spartizione_jazz.txt && git commit -m "casella 5: quanto varia un walking vero, e su quale beat tace"
```

---

## Task 7: misure 3 e 4 — come i tre si rispondono

**File:**
- Modifica: `tools/misura_spartizione.py` (in coda, prima di `main`)
- Produce: `out/spartizione_jazz.txt` aggiornato

**Interfacce:**
- Consuma: `MINIMO_BATTUTE`, `JT.battute`, `JT.griglia`.
- Produce: `accoppiamento(z, brani) -> dict`, `chi_sta_avanti(z, brani) -> dict`,
  e la costante `FINESTRA_COINCIDENZA`.

- [ ] **Passo 1: scrivere le due misure**

In `tools/misura_spartizione.py`, sopra `main()`:

```python
#: Due onset entro questa distanza si dicono «insieme». 30 ms e' la soglia
#: sotto la quale due attacchi sono percepiti come un evento solo nella
#: letteratura sulla percezione ritmica; qui e' una SCELTA dichiarata, non
#: una legge, ed e' il motivo per cui la misura 3 la ripete a 20 e 50.
FINESTRA_COINCIDENZA = 0.030


def accoppiamento(z, brani, finestre=(0.020, 0.030, 0.050)) -> dict:
    """MISURA 3. La batteria risponde al basso, o va per conto suo?

    Due cose diverse, e vanno tenute separate:
      a) le densita' per battuta si muovono insieme? (correlazione)
      b) quando uno dei due esce dalla griglia, ci esce anche l'altro?
    """
    coppie, esecutori, usati = [], set(), 0
    dentro = collections.Counter()
    fuori_basso = 0
    for b in brani:
        d = JT.battute(z, b.fname)
        if len(d.battute) < MINIMO_BATTUTE:
            continue
        usati += 1
        esecutori.add((b.bassista, b.batterista))
        bassi = [x.densita['bass'] for x in d.battute]
        batterie = [x.densita['drums'] for x in d.battute]
        if st.pstdev(bassi) > 0 and st.pstdev(batterie) > 0:
            coppie.append(_correlazione(bassi, batterie))
        # b) gli onset FUORI dai beat: chi accompagna chi
        for x in d.battute:
            sul_beat = {bt.istante for bt in x.beat}
            fb = [o for o in x.onsets['bass']
                  if all(abs(o - t) > FINESTRA_COINCIDENZA for t in sul_beat)]
            fuori_basso += len(fb)
            for o in fb:
                for f in finestre:
                    if any(abs(o - d2) <= f for d2 in x.onsets['drums']):
                        dentro[f] += 1
    print('\nMISURA 3 -- l accoppiamento fra batteria e basso')
    print(f'   {usati} esecuzioni, {len(esecutori)} coppie basso-batteria')
    print(f'   correlazione fra le densita per battuta: '
          f'mediana {st.median(coppie):+.3f}' if coppie else '   correlazione: n/d')
    print(f'   onset di basso FUORI griglia: {fuori_basso}')
    for f in finestre:
        q = dentro[f]
        print(f'   di questi, con un colpo di batteria entro {f*1000:3.0f} ms: '
              f'{q} ({100*q/fuori_basso:.1f}%)' if fuori_basso else '')
    return {'correlazione': st.median(coppie) if coppie else None,
            'fuori_griglia': fuori_basso, 'coincidenze': dict(dentro),
            'esecuzioni': usati, 'coppie': len(esecutori)}


def _correlazione(a, b) -> float:
    """Pearson, scritto a mano: `statistics.correlation` c'e' solo da 3.10 e
    la suite gira col Python di sistema, che qui non e' garantito."""
    ma, mb = st.mean(a), st.mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den if den else 0.0


def chi_sta_avanti(z, brani) -> dict:
    """MISURA 4. Lo scarto di ciascuno rispetto al beat di consenso.

    Il segno dice chi tira e chi trattiene. E' una relazione d'ensemble: non
    dice cosa si suona, dice come si sta insieme.
    """
    per_strumento = {s: [] for s in JT.STRUMENTI}
    esecutori, usati = set(), 0
    for b in brani:
        g = JT.griglia(z, b.fname)
        if len(g) < MINIMO_BATTUTE * 4:
            continue
        usati += 1
        esecutori.add(b.fname)
        for s in JT.STRUMENTI:
            v = [bt.scarti[s] for bt in g if bt.scarti[s] is not None]
            if v:
                per_strumento[s].append(st.mean(v))
    print('\nMISURA 4 -- chi sta avanti rispetto al beat comune')
    print(f'   {usati} esecuzioni')
    print('   strumento   scarto medio (ms)   mediana fra le esecuzioni')
    for s in JT.STRUMENTI:
        v = per_strumento[s]
        if v:
            print(f'   {s:9}   {1000*st.mean(v):+17.1f}   {1000*st.median(v):+8.1f}')
    return {s: (1000 * st.median(v) if v else None)
            for s, v in per_strumento.items()}
```

E aggiungere le due chiamate in `main()`, dopo `il_beat_saltato(z, brani)`:

```python
        accoppiamento(z, brani)
        chi_sta_avanti(z, brani)
```

- [ ] **Passo 2: eseguire su 25 brani e controllare i segni**

```bash
cd /d/DelugePal && .venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tools'); from delugexml import jtd as JT; import misura_spartizione as M; z=JT.apri(M.ZIP); b=JT.elenco(z, metro=4, limite=25); M.accoppiamento(z,b); M.chi_sta_avanti(z,b)"
```

⚠️ Controllo di sanità sulla misura 4: gli scarti mediani devono stare **entro
±40 ms**. Se uscissero centinaia di millisecondi, l'errore è di segno o di
unità in `griglia()`, non una scoperta sul jazz.

- [ ] **Passo 3: girarlo intero e salvare**

```bash
cd /d/DelugePal && .venv/Scripts/python.exe tools/misura_spartizione.py > out/spartizione_jazz.txt 2>&1; type out\spartizione_jazz.txt
```

- [ ] **Passo 4: commit**

```bash
git add tools/misura_spartizione.py out/spartizione_jazz.txt && git commit -m "casella 5: la batteria risponde al basso, e di quanto"
```

---

## Task 8: misura 5 — il piano, con la sua incertezza dichiarata

**File:**
- Modifica: `tools/misura_spartizione.py` (in coda, prima di `main`)

**Interfacce:**
- Consuma: `JT.piano`, `JT.battute`, `MINIMO_BATTUTE`.
- Produce: `il_piano(z, brani, finestre=(0.030, 0.050, 0.080)) -> dict`,
  costante `FINESTRA_ACCORDO`.

⚠️ **Questa misura poggia su una regola non misurata**, ed è l'unica del
gruppo. In un trio il pianista fa comping *e* assolo e `piano_midi.mid` è un
flusso solo: la separazione è `[IPO]`. Per questo la misura si ripete a tre
finestre e **stampa la sensibilità accanto al valore**.

- [ ] **Passo 1: scrivere la misura**

```python
#: Quante note devono attaccare entro `FINESTRA_ACCORDO` perche' si dica
#: «accordo», cioe' comping e non linea.
NOTE_PER_ACCORDO = 2

#: ⚠️ REGOLA [IPO], NON MISURATA. In un trio il pianista fa comping e assolo,
#: e il MIDI e' un flusso solo. 50 ms e' la finestra centrale; la misura si
#: ripete a 30 e 80 e la differenza si STAMPA: se il risultato balla, il
#: numero non si scrive nella scheda.
FINESTRA_ACCORDO = 0.050


def il_piano(z, brani, finestre=(0.030, 0.050, 0.080)) -> dict:
    """MISURA 5. Il piano contro la sezione ritmica.

    Due numeri: la densita' del piano per battuta (che e' `[MIS]`), e la
    quota di quella densita' che cade in accordi invece che in note singole
    (che e' `[IPO]`, perche' dipende dalla regola qui sopra).
    """
    densita, quote = [], {f: [] for f in finestre}
    esecutori, usati = set(), 0
    for b in brani:
        d = JT.battute(z, b.fname)
        if len(d.battute) < MINIMO_BATTUTE:
            continue
        f_midi = JT.piano(z, b.fname)
        if not f_midi.note:
            continue
        usati += 1
        esecutori.add(b.pianista)
        densita.append(st.mean([x.densita['piano'] for x in d.battute]))
        # gli onset del piano in secondi, dal CSV: il MIDI ha i suoi tick e
        # qui interessa solo la simultaneita', non l'altezza.
        ons = JT.onsets(z, b.fname, 'piano')
        for f in finestre:
            in_accordo = i = 0
            while i < len(ons):
                j = i
                while j + 1 < len(ons) and ons[j + 1] - ons[i] <= f:
                    j += 1
                n = j - i + 1
                if n >= NOTE_PER_ACCORDO:
                    in_accordo += n
                i = j + 1
            quote[f].append(in_accordo / len(ons))
    print('\nMISURA 5 -- il piano contro la sezione ritmica')
    print(f'   {usati} esecuzioni, {len(esecutori)} pianisti')
    print(f'   densita del piano per battuta: mediana {st.median(densita):.2f}'
          '   [MIS]')
    print('   quota di onset in accordo (= comping) -- [IPO], dipende dalla finestra:')
    for f in finestre:
        print(f'      entro {f*1000:3.0f} ms: {100*st.median(quote[f]):5.1f}%')
    forbice = 100 * (st.median(quote[max(finestre)]) - st.median(quote[min(finestre)]))
    print(f'   FORBICE fra la finestra piu stretta e la piu larga: {forbice:.1f} punti')
    print('   -> se la forbice supera 15 punti, il numero NON si scrive nella'
          ' scheda: si scrive la forbice.')
    return {'densita': st.median(densita), 'quote':
            {f: st.median(v) for f, v in quote.items()}, 'forbice': forbice,
            'esecuzioni': usati, 'esecutori': len(esecutori)}
```

E in `main()`, dopo `chi_sta_avanti(z, brani)`:

```python
        il_piano(z, brani)
```

- [ ] **Passo 2: eseguire su 25 brani**

```bash
cd /d/DelugePal && .venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tools'); from delugexml import jtd as JT; import misura_spartizione as M; z=JT.apri(M.ZIP); b=JT.elenco(z, metro=4, limite=25); M.il_piano(z,b)"
```

Atteso: tre percentuali crescenti con la finestra. **La forbice è il
risultato**, non un contorno: se supera 15 punti la regola non regge e nella
scheda va la forbice al posto del numero.

- [ ] **Passo 3: la doppia misura, che è un requisito della spec**

Ogni numero di titolo va calcolato **su tutto e su JTD-300**, i 300 brani del
sottoinsieme curato. Se i due divergono vince JTD-300, e **la divergenza si
scrive**: è il modo in cui questo progetto distingue un risultato da un
artefatto del campione.

In `main()`, sostituire il corpo con due passate:

```python
def main() -> int:
    if not ZIP.exists():
        print(f'manca {ZIP}')
        return 1
    with JT.apri(ZIP) as z:
        for etichetta, curati in (('TUTTO IL CORPUS', False),
                                  ('SOLO JTD-300 (curato)', True)):
            brani = _brani(z, curati)
            print(f'\n{"=" * 68}\n{etichetta} -- {len(brani)} esecuzioni in 4/4\n')
            densita_del_basso(z, brani)
            il_beat_saltato(z, brani)
            accoppiamento(z, brani)
            chi_sta_avanti(z, brani)
            il_piano(z, brani)
    return 0
```

- [ ] **Passo 4: girarlo intero e salvare**

```bash
cd /d/DelugePal && .venv/Scripts/python.exe tools/misura_spartizione.py > out/spartizione_jazz.txt 2>&1; type out\spartizione_jazz.txt
```

⚠️ Le due passate leggono circa 12 000 membri dello zip: **qualche minuto** è
normale, non è un blocco. Se supera i venti minuti, il colpevole è quasi
sempre uno zip riaperto dentro il ciclo invece di passato come oggetto.

- [ ] **Passo 5: confrontare le due passate**

Mettere fianco a fianco i numeri di titolo delle due colonne — densità mediana
del basso, deviazione, percentuale di beat taciuti, correlazione, forbice del
piano. **Uno scarto sotto il 10% si cita e si va avanti; sopra, il numero che
entra nella scheda è quello di JTD-300** e la divergenza si scrive accanto.

- [ ] **Passo 6: commit**

```bash
git add tools/misura_spartizione.py out/spartizione_jazz.txt && git commit -m "casella 5: il piano, la forbice, e la doppia misura su JTD-300"
```

---

## Task 9: la scheda, l'indice, l'attribuzione e le tre righe false

**File:**
- Modifica: `docs/repertori/jazz.md` (la casella 5, oggi «Vuota»)
- Modifica: `docs/MUSICA.md` (l'indice: jazz, colonna 5)
- Modifica: `docs/FONTI.md` (JTD fra le fonti, con la nota MIT)
- Modifica: `HANDOFF.md` (sezione nuova + correzione di tre righe)

**Interfacce:**
- Consuma: `out/spartizione_jazz.txt` e `out/controlli_jtd.txt` (Task 5-8).
- Produce: niente codice.

- [ ] **Passo 1: riscrivere la casella 5 di `docs/repertori/jazz.md`**

Sostituire il corpo della casella (oggi comincia con «**Vuota, ed è il muro
che il 30 agosto 2026 ha fermato tre cose di fila.**») con le cinque misure.
Per ognuna: il numero, il **grado**, e **quante esecuzioni e quanti esecutori**
lo reggono. La sezione «Le tre cose che questa casella ha fermato» **resta**,
con una riga in testa che dice quale delle tre è stata sciolta e quale no.

⚠️ Tre cose che devono comparire, e sono le più facili da dimenticare:

1. **la batteria non è per strumento** — nessun numero di questa casella può
   dire «il rullante», «la cassa» o «il ride»;
2. **la misura 5 è `[IPO]`** per la parte che distingue comping e assolo, con
   la forbice accanto;
3. **il conteggio del campione**, come nella casella 6: `[MIS]` senza il
   numero di esecutori è la trappola già presa una volta col reggae, dove
   venti esecuzioni di due batteristi stavano per essere firmate col nome di
   un genere.

- [ ] **Passo 2: l'indice in `docs/MUSICA.md`**

Nella matrice repertorio × casella, la riga `jazz` passa da `○` a `●` (o `◐`
se la forbice della misura 5 fosse risultata larga) nella colonna 5.

- [ ] **Passo 3: l'attribuzione in `docs/FONTI.md`**

Aggiungere JTD fra le fonti primarie, con: gli autori (Cheston, Schlichting,
Cross, Harrison — TISMIR 2024), la licenza **MIT** e la sua nota di copyright,
il fatto che **l'audio non è incluso né serve**, e i limiti (annotazioni
automatiche, F-measure 0,94; batteria non per strumento).

- [ ] **Passo 4: `HANDOFF.md` — la sezione nuova e le tre righe false**

Aggiungere `## 6-noviesdecies` con: la premessa verificata e trovata falsa, il
corpus, le cinque misure e cosa hanno detto, e cosa resta aperto.

⚠️ **E correggere le tre righe**, che è la parte che serve a chi riprende:

| dove | cosa dice oggi | cosa deve dire |
|---|---|---|
| «Il prossimo lavoro», in testa | il prossimo passo è un lettore di partiture MusicXML | il lettore MusicXML resta per classica/barocca/antica (OpenScore, CC0); la casella 5 è stata chiusa dal JTD |
| §6-octodecies, «Il difetto aperto» | «la correlazione non è misurabile da nessun corpus in casa… il dato non c'è» | il dato esiste e ha una licenza; ⚠️ ed è la **quarta** volta che una casella scritta senza domanda manda a cercare fuori qualcosa di raggiungibile |
| casella 5 di `jazz.md`, «Le tre cose» | «Qui non manca il corpus, manca il codice che lo apre» | mancavano tutt'e due, e nessuno l'aveva verificato: MusicXML su disco, zero file |

- [ ] **Passo 5: la guardia dei fine riga, e commit**

```bash
cd /d/DelugePal && git diff --stat && git diff --stat --ignore-cr-at-eol
```

I due comandi devono dare **lo stesso numero di righe**. Se differiscono, un
file è stato riscritto in CRLF: recuperarlo e riscriverlo con `write_bytes()`
o `open(..., newline='')`.

```bash
git add docs/repertori/jazz.md docs/MUSICA.md docs/FONTI.md HANDOFF.md && git commit -m "casella 5 chiusa: come il trio si spartisce la battuta, e tre righe corrette"
```

- [ ] **Passo 6: la suite intera, un'ultima volta**

```bash
cd /d/DelugePal && python tests/test_all.py 2>&1 | tail -5
```

Atteso: nessun FAIL, e il totale salito di **circa 25 test** rispetto ai 997
di partenza. I test nuovi **saltano** su una macchina senza corpus, ed è
giusto così.

---

## Cosa NON fa questo piano

- **Non tocca il generatore.** I numeri servono a decidere cosa spendere, e
  quella decisione è il lavoro dopo, con un pezzo da far sentire all'utente.
- **Non misura la forma.** JTD non annota sezioni: «cosa cambia al confine di
  ritornello» resta fuori.
- **Non usa i 241 file jazz di `songs_archive`.** Restano una controprova
  disponibile a costo quasi zero, non usata qui.
- **Non scrive niente sul Deluge.** Nessun caricamento, nessuna song.
