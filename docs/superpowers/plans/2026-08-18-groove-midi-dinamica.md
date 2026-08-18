# Il Groove MIDI e il groove template — piano di attuazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** chiudere la casella 6 (Dinamica) della scheda jazz con numeri misurati sul Groove MIDI, e costruire il **groove template** — velocity e microtiming residuo di un'esecuzione vera, posati su un pattern scritto con `MU.passi()`.

**Architecture:** un lettore di corpus nuovo, `tools/delugexml/groove.py`, sul modello esatto di `wjazz.py`: riceve la radice del dataset come argomento, non tocca mai un `Document`, e ha un **nucleo puro** (funzioni che prendono liste di numeri) provato senza corpus più un guscio che apre i file e salta quando `to-read/` non c'è. Il verbo che scrive, `MU.applica_groove()`, sta in `musica.py` come tutti gli altri verbi.

**Tech Stack:** Python 3, **solo stdlib** (`csv`, `math`, `statistics`, `pathlib`). Il lettore MIDI è già in casa (`delugexml.midi`). Nessuna dipendenza nuova, mai.

## Global Constraints

- **Nessuna dipendenza nuova.** Solo stdlib. È la regola per cui `midi.py` si è scritto un lettore di Standard MIDI File invece di tirarsi dentro `mido`.
- **`to-read/` è in `.gitignore`** e non è versionato. Ogni test che lo tocca deve sollevare `FileNotFoundError` quando manca: il runner in fondo a `tests/test_all.py` lo converte in `SKIP`. Non versionare mai file del dataset.
- **Niente pytest.** I test stanno tutti in `tests/test_all.py`, si scrivono con `check(nome, condizione, dettaglio)` e si eseguono con `.venv/Scripts/python.exe tests/test_all.py`. Una funzione il cui nome comincia per `test_` viene raccolta da sola.
- **Un numero vive in un posto solo.** Mai ricopiare un valore in due file: altrove è un rimando.
- **Il commento in italiano senza accenti** nel codice (`perche'`, `gia'`), come tutto il resto della libreria; nei documenti Markdown invece gli accenti si scrivono normali.
- **Prefisso, mai sottostringa**, per filtrare le etichette di stile: `reggae` deve prendere `reggae` e `reggae/slow` e **non** `latin/reggaeton`.
- Percorso del dataset: `to-read/MIDI/groove-v1.0.0-midionly/groove/`, con `info.csv` dentro.
- Colonne di `info.csv`, in quest'ordine: `drummer,session,id,style,bpm,beat_type,time_signature,midi_filename,audio_filename,duration,split`.
- Costanti già esistenti da riusare, mai ridefinire: `midi.TICK_PER_MOVIMENTO_DELUGE` = 96, `musica.TICK_PER_PASSO` = 24, `musica.TICK_PER_BATTUTA` = 384, `midi.GM_PERCUSSIONI`.
- **Commit dopo ogni task**, con messaggio in italiano e `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>` in fondo.

---

## File

| file | responsabilità |
|---|---|
| `tools/delugexml/musica.py` | **modifica**: ci si promuove l'aritmetica del BUR (Task 1) e ci si aggiunge `applica_groove()` (Task 7) |
| `tools/delugexml/wjazz.py` | **modifica**: smette di definire `in_bur()` e la importa (Task 1) |
| `tools/delugexml/groove.py` | **nuovo**: il lettore del Groove MIDI. Inventario, origine della griglia, BUR, profilo, scala |
| `tools/misura_groove.py` | **nuovo**: lo script che esegue le misure e stampa in `out/`. Non è libreria: non lo importa nessuno |
| `tests/test_all.py` | **modifica**: i test nuovi in fondo, prima del blocco `if __name__ == '__main__':` |
| `docs/repertori/jazz.md` | **modifica**: caselle 4, 6, 9, 10 |
| `docs/repertori/reggae-dub.md` | **modifica**: casella 6, l'agenda corretta |
| `docs/MUSICA.md` | **modifica**: il comune («Velocity groove», «La macchina») e l'indice |
| `.claude/skills/deluge-pal/SKILL.md` | **modifica**: `GR` fra le importazioni |
| `HANDOFF.md` | **modifica**: la 6-terdecies |

---

## Task 1: L'aritmetica del BUR in comune

`in_bur()` sta in `wjazz.py:497` e serve a due lettori. Duplicarla è vietato, e far dipendere un lettore di corpus dall'altro è assurdo. Si promuove in `musica.py`, che è il vocabolario musicale comune che `wjazz.py` già importa. **Primo task apposta**: tocca codice che funziona, e va fatto quando i test esistenti possono ancora dire se si è rotto qualcosa.

**Files:**
- Modify: `tools/delugexml/musica.py`
- Modify: `tools/delugexml/wjazz.py:497-501`
- Test: `tests/test_all.py`

**Interfaces:**
- Produces: `musica.in_bur(levare: float) -> float`, `musica.da_bur(bur: float) -> float`. `wjazz.in_bur` resta risolvibile come prima (import, non copia).

- [ ] **Step 1: Scrivere il test che fallisce**

In fondo a `tests/test_all.py`, prima del blocco `if __name__ == '__main__':`:

```python
def test_bur_in_comune():
    """L'aritmetica del BUR sta in `musica`, e i due lettori la condividono.

    Stava in `wjazz.py`. Serve anche a `groove.py`, e le alternative erano
    duplicarla (vietato) o far dipendere un corpus dall'altro (assurdo).
    """
    from delugexml import musica as MU                      # noqa: PLC0415
    from delugexml import wjazz as WJ                       # noqa: PLC0415

    check('dritto e BUR 1', MU.in_bur(0.5) == 1.0, str(MU.in_bur(0.5)))
    check('la terzina e BUR 2', abs(MU.in_bur(2 / 3) - 2.0) < 1e-9,
          str(MU.in_bur(2 / 3)))
    check('il jazz misurato, 61,7%, da 1,61',
          abs(MU.in_bur(0.617) - 1.61) < 0.01, f'{MU.in_bur(0.617):.3f}')

    for bur in (1.0, 1.61, 2.0, 3.0):
        check(f'da_bur e l inverso di in_bur, BUR {bur}',
              abs(MU.in_bur(MU.da_bur(bur)) - bur) < 1e-9,
              f'{MU.in_bur(MU.da_bur(bur))}')

    check('un levare fuori da (0,1) e un errore',
          _raises(lambda: MU.in_bur(1.0), ValueError))
    check('e `wjazz` usa la stessa funzione, non una copia',
          WJ.in_bur is MU.in_bur)
```

- [ ] **Step 2: Eseguire e verificare che fallisca**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i "bur_in_comune"`
Expected: FAIL — `eccezione AttributeError: module 'delugexml.musica' has no attribute 'in_bur'`

- [ ] **Step 3: Promuovere la funzione in `musica.py`**

In `tools/delugexml/musica.py`, accanto alle altre conversioni musicali:

```python
# ------------------------------------------------------------- lo swing
#
# Dove cade il LEVARE dentro il movimento, in frazione: 0,5 e' dritto,
# 0,667 e' la terzina. Il rapporto fra le due meta' del movimento e' la BUR
# (beat-upbeat ratio) della letteratura: 1 dritto, 2 terzina.
#
# Sta QUI e non in un lettore di corpus perche' la usano in due -- `wjazz`
# sulla Weimar e `groove` sul Groove MIDI -- e un numero, o una formula,
# vive in un posto solo.


def in_bur(levare: float) -> float:
    """Da posizione del levare a BUR. 0,5 -> 1 (dritto), 0,667 -> 2."""
    if not 0 < levare < 1:
        raise ValueError(f'il levare sta fra 0 e 1, non {levare}')
    return levare / (1 - levare)


def da_bur(bur: float) -> float:
    """L'inverso: da BUR a posizione del levare. 2 -> 0,667."""
    if bur <= 0:
        raise ValueError(f'la BUR e\' positiva, non {bur}')
    return bur / (1 + bur)
```

- [ ] **Step 4: Far importare `wjazz.py` invece di definire**

In `tools/delugexml/wjazz.py`, cancellare la definizione di `in_bur` (righe 497-501) e aggiungere il nome all'import di `musica` già presente in testa al file:

```python
from .musica import in_bur                          # noqa: F401  (ri-esportato)
```

Il commento `noqa` serve perché il nome non è usato altrove nel modulo ma **deve** restare raggiungibile come `WJ.in_bur`: è nell'interfaccia pubblica documentata in `SKILL.md`, e c'è già un test che lo chiama.

- [ ] **Step 5: Eseguire tutta la suite**

Run: `.venv/Scripts/python.exe tests/test_all.py`
Expected: il nuovo test PASS, e **tutti i test `test_wjazz_*` ancora verdi** — sono loro a dire se la promozione ha rotto qualcosa.

- [ ] **Step 6: Commit**

```bash
git add tools/delugexml/musica.py tools/delugexml/wjazz.py tests/test_all.py
git commit -m "musica: l aritmetica del BUR promossa in comune"
```

---

## Task 2: `groove.py` — l'inventario

Leggere `info.csv` e filtrare per etichetta. La regola del **prefisso** è il cuore del task: è già scritta nelle schede come il controesempio da non sbagliare.

**Files:**
- Create: `tools/delugexml/groove.py`
- Test: `tests/test_all.py`

**Interfaces:**
- Produces: `groove.Esecuzione` (NamedTuple), `groove.per_prefisso(valore, filtro) -> bool`, `groove.elenco(base, *, style=None, beat_type=None, drummer=None, time_signature=None) -> list[Esecuzione]`, `groove.valori(base, colonna) -> dict[str, int]`, `groove.racconta(base, id) -> str`. `base` è un `Path` alla cartella che contiene `info.csv`.

- [ ] **Step 1: Scrivere il test che fallisce**

```python
def test_groove_prefisso():
    """`reggae` prende `reggae/slow` e NON `latin/reggaeton`.

    La sottostringa e' la regola sbagliata, ed e' scritta come controesempio
    nella casella 6 di `docs/repertori/jazz.md`. Nucleo puro: nessun file.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    check('un prefisso prende se stesso', GR.per_prefisso('reggae', 'reggae'))
    check('e prende la sottocategoria',
          GR.per_prefisso('reggae/slow', 'reggae'))
    check('ma NON una parola che lo contiene',
          not GR.per_prefisso('latin/reggaeton', 'reggae'))
    check('ne una che ci somiglia',
          not GR.per_prefisso('latin/brazilian-sambareggae', 'reggae'))
    check('jazz prende jazz/funk', GR.per_prefisso('jazz/funk', 'jazz'))
    check('e non prende funk', not GR.per_prefisso('funk', 'jazz'))
```

- [ ] **Step 2: Eseguire e verificare che fallisca**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i groove_prefisso`
Expected: FAIL — `eccezione ModuleNotFoundError: No module named 'delugexml.groove'`

- [ ] **Step 3: Scrivere il modulo, parte inventario**

Creare `tools/delugexml/groove.py`:

```python
"""Leggere il Groove MIDI Dataset: velocity e micro-tempistica di batteristi veri.

PERCHE' ESISTE
--------------
La scala delle velocity che il progetto usa viene dal web, e l'ascolto
dell'utente l'ha gia' dovuta correggere una volta: i pattern del primo dub
erano quasi giusti e PIATTI. Qui ci sono 1150 esecuzioni annotate per stile e
per BPM, suonate su un kit elettronico, con la velocity e l'onset esatto di
ogni colpo. La micro-tempistica E' lo scarto di quegli onset dalla griglia.

Il dataset sta in `to-read/MIDI/groove-v1.0.0-midionly/`, che NON e'
versionato: e' opera di terzi. I test che lo usano saltano se non c'e', come
quelli del corpus e quelli di `wjazz.py`.

IL CONFINE
----------
Questo modulo LEGGE. Non tocca mai un `Document`, non costruisce `Note`, non
sa cosa sia una clip. Il verbo che scrive -- `MU.applica_groove()` -- sta in
`musica.py` con tutti gli altri verbi. E' lo stesso confine di `wjazz.py`.

PERCHE' NON DENTRO `midi.py`
----------------------------
`midi.py` e' il lettore GENERICO di Standard MIDI File, validato nota per nota
contro `mido`. Questo e' un DATASET: `info.csv`, le etichette di stile, `beat`
contro `fill` non sono roba di MIDI. Metterle nel lettore comune lo
sporcherebbero per sempre -- la stessa ragione per cui il dialetto di Weimar
sta in `wjazz.py` e non in `MU.SIGLE`.

⚠️ IL PREFISSO, NON LA SOTTOSTRINGA
-----------------------------------
Cercare `reggae` dentro l'etichetta prenderebbe anche `latin/reggaeton` e
`latin/brazilian-sambareggae`, che reggae non sono.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import NamedTuple

#: Il file che etichetta ogni esecuzione. Sta nella radice del dataset.
INVENTARIO = 'info.csv'


class Esecuzione(NamedTuple):
    """Una riga di `info.csv`, con i soli campi che servono."""

    id: str
    drummer: str
    style: str
    bpm: int
    beat_type: str
    time_signature: str
    midi_filename: str
    duration: float


def per_prefisso(valore: str, filtro: str) -> bool:
    """`reggae` prende `reggae` e `reggae/slow`, NON `latin/reggaeton`.

    E' la regola di filtro di questo modulo, ed e' una funzione a se' perche'
    e' esattamente il punto in cui e' facile sbagliare.
    """
    return valore == filtro or valore.startswith(filtro + '/')


def _righe(base: Path | str) -> list[dict[str, str]]:
    """Le righe grezze di `info.csv`. Solleva se il dataset non c'e'."""
    inventario = Path(base) / INVENTARIO
    if not inventario.exists():
        raise FileNotFoundError(str(inventario))
    with inventario.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def elenco(base: Path | str, *, style: str | None = None,
           beat_type: str | None = None, drummer: str | None = None,
           time_signature: str | None = None) -> list[Esecuzione]:
    """Le esecuzioni che soddisfano i filtri. `style` va per PREFISSO."""
    fuori = []
    for r in _righe(base):
        if style is not None and not per_prefisso(r['style'], style):
            continue
        if beat_type is not None and r['beat_type'] != beat_type:
            continue
        if drummer is not None and r['drummer'] != drummer:
            continue
        if time_signature is not None and r['time_signature'] != time_signature:
            continue
        fuori.append(Esecuzione(
            id=r['id'], drummer=r['drummer'], style=r['style'],
            bpm=int(r['bpm']), beat_type=r['beat_type'],
            time_signature=r['time_signature'],
            midi_filename=r['midi_filename'], duration=float(r['duration'])))
    return fuori


def valori(base: Path | str, colonna: str) -> dict[str, int]:
    """Quali etichette esistono in una colonna, e quante volte."""
    righe = _righe(base)
    if righe and colonna not in righe[0]:
        raise ValueError(
            f'colonna {colonna!r} assente: ci sono {sorted(righe[0])}')
    conto: dict[str, int] = {}
    for r in righe:
        conto[r[colonna]] = conto.get(r[colonna], 0) + 1
    return dict(sorted(conto.items(), key=lambda kv: (-kv[1], kv[0])))


def _una(base: Path | str, id: str) -> Esecuzione:
    """L'esecuzione con quell'id, o un errore che dice quante ce ne sono."""
    for e in elenco(base):
        if e.id == id:
            return e
    raise ValueError(f'nessuna esecuzione con id {id!r}')


def racconta(base: Path | str, id: str) -> str:
    """Cosa c'e' in un'esecuzione, in una riga."""
    e = _una(base, id)
    return (f'{e.id}: {e.drummer}, {e.style}, {e.bpm} BPM, '
            f'{e.beat_type}, {e.time_signature}, {e.duration:.1f} s')
```

- [ ] **Step 4: Eseguire e verificare che passi**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i groove_prefisso`
Expected: PASS su tutte le sei condizioni.

- [ ] **Step 5: Aggiungere il test sul corpus vero**

```python
def test_groove_inventario():
    """Lettura vera del dataset. SALTA se non c'e': non e' roba del repo.

    I conteggi vengono dal dataset stesso, che qui e' l'artefatto in esame,
    e sono lo stato del disco del 18 agosto 2026.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    base = ROOT / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
    if not (base / GR.INVENTARIO).exists():
        raise FileNotFoundError(str(base / GR.INVENTARIO))

    tutte = GR.elenco(base)
    check('il dataset ha 1150 esecuzioni', len(tutte) == 1150, str(len(tutte)))

    jazz = GR.elenco(base, style='jazz')
    check('101 esecuzioni jazz', len(jazz) == 101, str(len(jazz)))
    beat = GR.elenco(base, style='jazz', beat_type='beat')
    check('di cui 50 `beat`', len(beat) == 50, str(len(beat)))
    check('e 5 batteristi', len({e.drummer for e in jazz}) == 5,
          str(sorted({e.drummer for e in jazz})))

    reggae = GR.elenco(base, style='reggae')
    check('20 esecuzioni reggae', len(reggae) == 20, str(len(reggae)))
    check('ma UN batterista sole quattro `beat`',
          len({e.drummer for e in reggae}) == 2
          and len([e for e in reggae if e.beat_type == 'beat']) == 4,
          f'{sorted({e.drummer for e in reggae})}, '
          f'{len([e for e in reggae if e.beat_type == "beat"])} beat')
    check('e nessuna e reggaeton',
          all(not e.style.startswith('latin') for e in reggae),
          str(sorted({e.style for e in reggae})))
```

- [ ] **Step 6: Eseguire e verificare**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i groove_inventario`
Expected: PASS (o SKIP su una macchina senza `to-read/`).

- [ ] **Step 7: Commit**

```bash
git add tools/delugexml/groove.py tests/test_all.py
git commit -m "groove: l inventario del Groove MIDI, e il prefisso che non e' la sottostringa"
```

---

## Task 3: L'origine della griglia

Il trabocchetto del progetto. In un `jazz/swing` a 185 BPM **tutti** gli strumenti hanno il picco a 0,958 del movimento: il tick 0 del file non è un movimento del batterista. Misurare da lì darebbe un anticipo sistematico del 5% per ogni esecuzione — pulito, ripetibile e falso.

**Files:**
- Modify: `tools/delugexml/groove.py`
- Test: `tests/test_all.py`

**Interfaces:**
- Produces: `groove.origine(posizioni: Sequence[float], passo: float, *, finestra: float = 0.25) -> float` — lo scarto comune **con segno**, in tick, in `(-passo/2, +passo/2]`.

- [ ] **Step 1: Scrivere il test che fallisce**

```python
def test_groove_origine_della_griglia():
    """Lo scarto comune si stima e si toglie, con la media CIRCOLARE.

    E' il trabocchetto di questo corpus: il tick 0 del file non e' un
    movimento del batterista, e misurare da li' darebbe un anticipo
    sistematico del 5% per OGNI esecuzione. Stesso errore della Weimar,
    nella stessa posizione: l'origine della misura.

    Nucleo puro: liste di numeri, nessun file.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    passo = 24.0                                    # un 1/16 sul Deluge

    dritte = [k * passo for k in range(32)]
    check('senza scarto, l origine e zero',
          abs(GR.origine(dritte, passo)) < 1e-9, str(GR.origine(dritte, passo)))

    avanti = [k * passo + 3 for k in range(32)]
    check('uno scarto di +3 tick si ritrova',
          abs(GR.origine(avanti, passo) - 3) < 1e-9, str(GR.origine(avanti, passo)))

    # ⚠️ il caso che la media aritmetica sbaglia: una fase appena PRIMA del
    # passo successivo e' un anticipo, non un ritardo di quasi un passo.
    indietro = [k * passo - 1 for k in range(1, 32)]
    check('e uno di -1 torna NEGATIVO, non +23',
          abs(GR.origine(indietro, passo) + 1) < 1e-9,
          str(GR.origine(indietro, passo)))

    misto = [k * passo - 1 for k in range(1, 16)] + [k * passo + 1
                                                     for k in range(16, 32)]
    check('scarti opposti si annullano',
          abs(GR.origine(misto, passo)) < 0.1, str(GR.origine(misto, passo)))

    check('senza colpi, l origine e zero e non un errore',
          GR.origine([], passo) == 0.0)

    # ⚠️ i levare swingati NON devono entrare nella stima: stanno a 2/3 di
    # movimento, cioe' a 2,67 passi, e la loro fase e' swing, non origine.
    swingate = [k * passo for k in range(32)] + [
        k * 96 + 64 for k in range(8)]
    check('un levare swingato non sporca l origine',
          abs(GR.origine(swingate, passo)) < 1e-9,
          str(GR.origine(swingate, passo)))
```

- [ ] **Step 2: Eseguire e verificare che fallisca**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i groove_origine`
Expected: FAIL — `AttributeError: module 'delugexml.groove' has no attribute 'origine'`

- [ ] **Step 3: Scrivere la funzione**

Aggiungere a `tools/delugexml/groove.py` (e `import math` in testa):

```python
def origine(posizioni, passo: float) -> float:
    """Lo scarto comune di tutti gli onset dalla griglia, in tick, CON SEGNO.

    ⚠️ MEDIA CIRCOLARE, e non e' pignoleria. La fase dentro il passo e' una
    grandezza che GIRA: un colpo a 23 tick su 24 e' un anticipo di 1, non un
    ritardo di 23, e la media aritmetica di 1 e 23 darebbe 12 -- cioe' il
    contrario di zero. Si mediano i versori e si torna indietro.

    Il risultato sta in (-passo/2, +passo/2]. Va SOTTRATTO dalle posizioni.

    ⚠️ SI STIMA SOLO SUI COLPI VICINI ALLA GRIGLIA, dentro `finestra`. Se no
    lo swing la sporca: un levare swingato sta a 2/3 di movimento, cioe' a
    2,67 passi, e la sua fase (-8 tick su 24) entrerebbe nella media come se
    fosse uno scarto comune. Non lo e': e' swing, e lo toglie il passo dopo.

    ⚠️ IL LIMITE, DICHIARATO: uno scarto comune piu' grande di un quarto di
    passo cadrebbe fuori dalla finestra e non verrebbe visto. Nel dataset
    misurato vale circa un tick su ventiquattro, quindi la finestra sta larga
    dieci volte il necessario -- ma se un giorno un corpus diverso desse
    origine zero su dati palesemente storti, e' il primo posto da guardare.

    PERCHE' ESISTE. Misurato su `drummer1/session3/2_jazz-swing_185_beat_4-4`:
    ride, kick, rullante e charleston hanno TUTTI il picco a 0,958 del
    movimento. Tutti insieme vuol dire che non e' feel, e' l'origine. La
    prima nota del file sta a tick 1287, e il tick 0 non e' un movimento.

    ⚠️ Quello che si toglie NON si dichiara come feel: a 185 BPM il 5% vale
    16 ms, indistinguibile dalla latenza di cattura del kit elettronico su
    cui il dataset e' registrato. Il feel e' cio' che RESTA dopo averlo tolto.
    """
    vicini = []
    for p in posizioni:
        scarto = p % passo
        if scarto > passo / 2:
            scarto -= passo             # la fase gira: 23 su 24 e' -1
        if abs(scarto) < finestra * passo:
            vicini.append(scarto)
    if not vicini:
        return 0.0
    fasi = [s / passo * 2 * math.pi for s in vicini]
    x = sum(math.cos(a) for a in fasi) / len(fasi)
    y = sum(math.sin(a) for a in fasi) / len(fasi)
    if abs(x) < 1e-12 and abs(y) < 1e-12:
        return 0.0                      # fasi sparse: nessuna origine comune
    return math.atan2(y, x) / (2 * math.pi) * passo
```

La firma è `origine(posizioni, passo: float, *, finestra: float = 0.25) -> float`. Il confronto è **stretto** (`<`, non `<=`) apposta — ma non perché un levare swingato ci caschi sopra: con passo=24 e finestra=0.25 il suo scarto è di 8 tick, un terzo oltre il bordo di 6 (finestra × passo), non "a un quarto di passo dal bordo" come diceva prima questa frase. La ragione vera è che il bordo va deciso in un verso solo e dichiarato: un colpo con scarto esattamente uguale al bordo deve avere un esito fisso, perché il Task 4 (lo swing) e il Task 5 (i groove template) si appoggiano a questa soglia.

- [ ] **Step 4: Eseguire e verificare che passi**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i groove_origine`
Expected: PASS su tutte e cinque le condizioni.

- [ ] **Step 5: Commit**

```bash
git add tools/delugexml/groove.py tests/test_all.py
git commit -m "groove: l origine della griglia, con la media circolare"
```

---

## Task 4: Il BUR di un'esecuzione

Dove cade il levare dentro il movimento, misurato sui colpi veri. Serve due volte: per **toglierlo** dal profilo (se no lo swing viene applicato due volte, una dal firmware e una dal template) e come **controllo indipendente** sull'1,61 di Weimar.

**Files:**
- Modify: `tools/delugexml/groove.py`
- Test: `tests/test_all.py`

**Interfaces:**
- Consumes: `musica.in_bur` (Task 1), `groove.origine` (Task 3).
- Produces: `groove.levare_da_posizioni(posizioni: Sequence[float], ppq: float, *, finestra=(0.35, 0.75)) -> list[float]` e `groove.bur_da_posizioni(posizioni, ppq) -> float | None`.

- [ ] **Step 1: Scrivere il test che fallisce**

```python
def test_groove_bur_nucleo():
    """Dove cade il levare, su colpi costruiti a mano.

    Un movimento contribuisce solo se dentro la finestra c'e' ESATTAMENTE un
    colpo: due colpi vogliono dire semicrome, e li' una coppia di crome non
    c'e'. E' la stessa cautela di `WJ.levare_da_dati()`.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0

    dritto = []
    for k in range(8):
        dritto += [k * ppq, k * ppq + ppq / 2]
    lev = GR.levare_da_posizioni(dritto, ppq)
    check('crome dritte danno il levare a 0,5',
          len(lev) == 8 and all(abs(v - 0.5) < 1e-9 for v in lev), str(lev[:3]))
    check('e in BUR fa 1', abs(GR.bur_da_posizioni(dritto, ppq) - 1.0) < 1e-9,
          str(GR.bur_da_posizioni(dritto, ppq)))

    terzina = []
    for k in range(8):
        terzina += [k * ppq, k * ppq + ppq * 2 / 3]
    check('la terzina da BUR 2',
          abs(GR.bur_da_posizioni(terzina, ppq) - 2.0) < 0.01,
          str(GR.bur_da_posizioni(terzina, ppq)))

    jazz = []
    for k in range(8):
        jazz += [k * ppq, k * ppq + ppq * 0.617]
    check('il levare del jazz misurato da 1,61',
          abs(GR.bur_da_posizioni(jazz, ppq) - 1.61) < 0.02,
          str(GR.bur_da_posizioni(jazz, ppq)))

    semicrome = []
    for k in range(8):
        semicrome += [k * ppq, k * ppq + ppq / 4, k * ppq + ppq / 2,
                      k * ppq + ppq * 3 / 4]
    check('con DUE colpi in finestra il movimento si scarta',
          GR.levare_da_posizioni(semicrome, ppq) == [],
          str(GR.levare_da_posizioni(semicrome, ppq)))

    check('senza coppie il BUR e None',
          GR.bur_da_posizioni([0.0, 96.0, 192.0], ppq) is None)
```

- [ ] **Step 2: Eseguire e verificare che fallisca**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i groove_bur_nucleo`
Expected: FAIL — `AttributeError: ... has no attribute 'levare_da_posizioni'`

- [ ] **Step 3: Scrivere le due funzioni**

Aggiungere a `groove.py` (e `import statistics` in testa, più `from .musica import in_bur`):

```python
#: La finestra dentro il movimento in cui si cerca il levare, in frazione.
#: Larga abbastanza da prendere sia il dritto (0,5) sia la terzina (0,667) e
#: oltre, stretta abbastanza da non prendere la semicroma a 0,25 ne quella a
#: 0,75, che farebbero passare per levare cio' che levare non e'.
FINESTRA_LEVARE = (0.35, 0.75)


def levare_da_posizioni(posizioni, ppq: float, *,
                        finestra=FINESTRA_LEVARE) -> list[float]:
    """Le posizioni del levare in frazione di movimento, una per movimento.

    Un movimento contribuisce SOLO se ha un colpo sul battere e ESATTAMENTE
    un colpo dentro la finestra. Due colpi vogliono dire semicrome, e li' non
    c'e' una coppia di crome da misurare.
    """
    per_movimento: dict[int, list[float]] = {}
    for p in posizioni:
        per_movimento.setdefault(int(p // ppq), []).append((p % ppq) / ppq)
    fuori = []
    for fasi in per_movimento.values():
        if not any(f < finestra[0] for f in fasi):
            continue                    # senza battere non e' una coppia
        dentro = [f for f in fasi if finestra[0] <= f <= finestra[1]]
        if len(dentro) == 1:
            fuori.append(dentro[0])
    return fuori


def bur_da_posizioni(posizioni, ppq: float, *,
                     finestra=FINESTRA_LEVARE) -> float | None:
    """La BUR MEDIANA dell'esecuzione, o None se non ci sono coppie.

    Mediana e non media: la distribuzione ha una coda lunga di colpi che la
    finestra non ha saputo scartare, e la media ci andrebbe dietro.
    """
    lev = levare_da_posizioni(posizioni, ppq, finestra=finestra)
    if not lev:
        return None
    return in_bur(statistics.median(lev))
```

- [ ] **Step 4: Eseguire e verificare che passi**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i groove_bur_nucleo`
Expected: PASS su tutte e sei le condizioni.

- [ ] **Step 5: Commit**

```bash
git add tools/delugexml/groove.py tests/test_all.py
git commit -m "groove: il BUR di un esecuzione, misurato sui colpi veri"
```

---

## Task 5: Il profilo — il groove template

La catena completa, e **l'ordine è la cosa che conta**: origine, poi BUR, poi il residuo. Quello che resta è il solo microtiming che il template porta, perché lo swing lo farà `set_swing()` a livello di song.

**Files:**
- Modify: `tools/delugexml/groove.py`
- Test: `tests/test_all.py`

**Interfaces:**
- Consumes: `groove.origine` (Task 3), `groove.bur_da_posizioni` (Task 4), `musica.da_bur` (Task 1), `midi.leggi`, `midi.GM_PERCUSSIONI`, `midi.TICK_PER_MOVIMENTO_DELUGE`, `musica.TICK_PER_PASSO`.
- Produces: `groove.Passo(passo: int, velocity: int, scarto: float, colpi: int)`, `groove.Profilo(id, drummer, style, bpm, bur, battute, passi: dict[str, list[Passo]])`, `groove.profilo_da_colpi(colpi: dict[str, list[tuple[float, int]]], ppq: float) -> Profilo`, `groove.profilo(base, id) -> Profilo`.

- [ ] **Step 1: Scrivere il test che fallisce**

```python
def test_groove_profilo_nucleo():
    """La catena: origine, poi BUR, poi il RESIDUO. In quest'ordine.

    Su un'esecuzione costruita a mano che swinga a BUR 2 e ha un ride
    spostato di +2 tick rispetto a tutto il resto: il template deve portare
    quel +2 e NON lo swing, che sul Deluge lo fa `set_swing()`. Se portasse
    anche lo swing, lo swing verrebbe applicato due volte.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0

    # ---- fixture A: swing. Tutti i colpi SULLA griglia hanno lo stesso
    # scarto (+2), cosi' l'origine e' esattamente 2 e il BUR viene esatto.
    a = {'kick': [], 'ride': []}
    for b in range(16):                             # 16 movimenti = 4 battute
        a['kick'].append((b * ppq + 2, 100))
        a['ride'].append((b * ppq + 2, 90))
        a['ride'].append((b * ppq + 2 + ppq * 2 / 3, 70))

    pa = GR.profilo_da_colpi(a, ppq)
    check('il BUR misurato e 2', abs(pa.bur - 2.0) < 0.02, str(pa.bur))
    check('quattro battute', pa.battute == 4, str(pa.battute))

    # ⚠️ IL TEST CHE CONTA. Il levare swingato sta a 2,67 passi: senza
    # togliere lo swing finirebbe arrotondato al passo 3. Se e' sul 2, lo
    # swing e' stato tolto -- ed e' giusto che lo sia, perche' sul Deluge lo
    # rimette `set_swing()`, e due volte sarebbe una volta di troppo.
    ride = {s.passo for s in pa.passi['ride']}
    check('il levare swingato cade sul passo 2, non sul 3',
          2 in ride and 3 not in ride, str(sorted(ride)))

    r2 = [s for s in pa.passi['ride'] if s.passo == 2][0]
    check('e senza residuo, perche lo swing era tutto lo scarto',
          abs(r2.scarto) < 0.6, str(r2.scarto))
    check('con la sua velocity piu bassa', r2.velocity == 70, str(r2.velocity))

    k0 = [s for s in pa.passi['kick'] if s.passo == 0][0]
    check('il kick porta la sua velocity', k0.velocity == 100, str(k0.velocity))
    check('e quante volte e stato colpito', k0.colpi == 4, str(k0.colpi))
    check('uno strumento assente non compare', 'rullante' not in pa.passi,
          str(sorted(pa.passi)))

    # ---- fixture B: il residuo RELATIVO, senza swing di mezzo.
    #
    # ⚠️ Si misura la DIFFERENZA fra strumenti, non il valore assoluto: se
    # il kick sta a 0 e il ride a +2, non esiste un'origine "vera" che dica
    # quale dei due e' spostato. E' la ragione per cui la scheda dichiara il
    # ride che spinge RISPETTO al rullante, e mai un anticipo assoluto.
    b_ = {'kick': [], 'ride': []}
    for b in range(16):
        b_['kick'].append((b * ppq, 100))
        b_['ride'].append((b * ppq + 2, 90))

    pb = GR.profilo_da_colpi(b_, ppq)
    dk = [s for s in pb.passi['kick'] if s.passo == 0][0].scarto
    dr = [s for s in pb.passi['ride'] if s.passo == 0][0].scarto
    check('il ride spinge di 2 tick RISPETTO al kick',
          abs((dr - dk) - 2) < 0.6, f'{dr:.2f} - {dk:.2f}')
```

- [ ] **Step 2: Eseguire e verificare che fallisca**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i groove_profilo_nucleo`
Expected: FAIL — `AttributeError: ... has no attribute 'profilo_da_colpi'`

- [ ] **Step 3: Scrivere il nucleo**

Aggiungere a `groove.py`:

```python
class Passo(NamedTuple):
    """Cosa fa uno strumento su un passo della battuta, misurato."""

    passo: int          # 0..15
    velocity: int       # la MEDIANA dei colpi su quel passo
    scarto: float       # tick di residuo, con segno. + spinge, - trattiene
    colpi: int          # quante volte quel passo e' stato colpito


class Profilo(NamedTuple):
    """Il groove template: una esecuzione, misurata e ripulita.

    ⚠️ Viene da UNA esecuzione nominata, non dalla media di un sottoinsieme.
    Mediare il microtiming di batteristi diversi lo tira verso zero, cioe'
    verso la griglia: si perderebbe esattamente cio' che si e' andati a
    prendere. Percio' quello che ne esce e' [OSS] su quell'esecuzione, mentre
    la scala aggregata di `scala()` e' [MIS].
    """

    id: str
    drummer: str
    style: str
    bpm: int
    bur: float | None
    battute: int
    passi: dict[str, list[Passo]]


def _senza_swing(fase: float, levare: float) -> float:
    """Da fase dentro il movimento a fase SENZA swing.

    L'inverso della mappa dello swing, che e' lineare a tratti: la prima
    meta' del movimento e' stata dilatata fino a `levare`, la seconda
    compressa in quel che resta. Con `levare` = 0,5 non cambia niente.
    """
    if levare <= 0 or levare >= 1:
        return fase
    if fase < levare:
        return fase * 0.5 / levare
    return 0.5 + (fase - levare) * 0.5 / (1 - levare)


def profilo_da_colpi(colpi: dict[str, list[tuple[float, int]]], ppq: float,
                     *, id: str = '', drummer: str = '', style: str = '',
                     bpm: int = 0) -> Profilo:
    """Il profilo, da colpi gia' letti: strumento -> [(posizione, velocity)].

    LA CATENA, E L'ORDINE E' LA COSA CHE CONTA:

    1. togli l'ORIGINE della griglia -- se no ogni esecuzione dichiara un
       anticipo che e' latenza di cattura, non feel;
    2. misura il BUR e TOGLILO -- se no lo swing viene applicato due volte,
       una dal firmware e una da qui;
    3. quel che resta e' il RESIDUO: il ride che spinge rispetto al rullante
       che tiene indietro. E' il solo microtiming che il template porta;
    4. aggrega per strumento e per passo, sedici per battuta.
    """
    passo_tick = ppq / 4                            # un 1/16
    tutte = [p for note in colpi.values() for p, _ in note]
    off = origine(tutte, passo_tick)

    bur = bur_da_posizioni([p - off for p in tutte], ppq)
    levare = da_bur(bur) if bur is not None else 0.5

    per_passo: dict[str, dict[int, list[tuple[int, float]]]] = {}
    ultimo = 0
    for nome, note in colpi.items():
        for pos, vel in note:
            p = pos - off
            # il movimento PIU' VICINO, tollerando un colpo appena prima di
            # esso. ⚠️ senza il mezzo passo di grazia un anticipo finirebbe
            # nel movimento precedente con fase 0,99 invece che -0,01, e il
            # residuo uscirebbe grande quanto un movimento intero.
            movimento = math.floor(p / ppq + 0.125)
            fase = p / ppq - movimento
            dritta = (movimento + _senza_swing(fase, levare)) * ppq
            # ⚠️ il passo si decide DOPO aver tolto lo swing: un levare
            # swingato sta a 2,67 passi e si arrotonderebbe al 3.
            passo = round(dritta / passo_tick)
            ultimo = max(ultimo, passo)
            residuo = dritta - passo * passo_tick
            per_passo.setdefault(nome, {}).setdefault(
                passo % 16, []).append((vel, residuo))

    passi = {}
    for nome, dentro in per_passo.items():
        passi[nome] = [
            Passo(passo=k,
                  velocity=int(round(statistics.median(v for v, _ in vs))),
                  scarto=statistics.median(s for _, s in vs),
                  colpi=len(vs))
            for k, vs in sorted(dentro.items())]

    return Profilo(id=id, drummer=drummer, style=style, bpm=bpm, bur=bur,
                   battute=ultimo // 16 + 1, passi=passi)
```

Aggiungere anche `from .musica import da_bur, in_bur` in testa (sostituendo l'import del solo `in_bur` fatto al Task 4).

- [ ] **Step 4: Eseguire e verificare che passi**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i groove_profilo_nucleo`
Expected: PASS su tutte e nove le condizioni. **Se «anche sul levare il residuo è +2» fallisce, l'errore è nell'ordine della catena, non nell'aritmetica**: vuol dire che lo swing non è stato tolto prima di calcolare il residuo.

- [ ] **Step 5: Aggiungere il guscio che apre i file**

```python
def profilo(base: Path | str, id: str) -> Profilo:
    """Il profilo di UNA esecuzione del dataset, nominata."""
    e = _una(base, id)
    f = MI.leggi(Path(base) / e.midi_filename)
    colpi: dict[str, list[tuple[float, int]]] = {}
    for t in f.tracce:
        for n in t.note:
            nome = MI.GM_PERCUSSIONI.get(n.y)
            if nome is None:
                continue                # una percussione fuori dalla mappa GM
            colpi.setdefault(nome, []).append((float(n.pos), n.velocity))
    return profilo_da_colpi(colpi, float(f.ppq), id=e.id, drummer=e.drummer,
                            style=e.style, bpm=e.bpm)
```

Aggiungere `from . import midi as MI` in testa al modulo.

- [ ] **Step 6: Aggiungere il test sul corpus vero**

```python
def test_groove_profilo_corpus():
    """Il profilo di un'esecuzione vera. SALTA senza il dataset.

    L'esecuzione e' nominata apposta: un profilo viene da UN batterista, e
    dichiararlo e' cio' che tiene onesto il marcatore [OSS].
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    base = ROOT / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
    if not (base / GR.INVENTARIO).exists():
        raise FileNotFoundError(str(base / GR.INVENTARIO))

    p = GR.profilo(base, 'drummer1/session3/2')
    check('e drummer1 in jazz/swing a 185',
          p.drummer == 'drummer1' and p.style == 'jazz/swing' and p.bpm == 185,
          f'{p.drummer} {p.style} {p.bpm}')
    check('il BUR e fra 1 e 2,5', p.bur is not None and 1.0 < p.bur < 2.5,
          str(p.bur))
    check('c e il ride', 'ride' in p.passi, str(sorted(p.passi))[:120])
    check('ogni passo sta fra 0 e 15',
          all(0 <= s.passo <= 15 for v in p.passi.values() for s in v))
    check('e il residuo e piccolo: e cio che RESTA dopo aver tolto lo swing',
          all(abs(s.scarto) <= 12 for v in p.passi.values() for s in v),
          str(max(abs(s.scarto) for v in p.passi.values() for s in v)))
```

- [ ] **Step 7: Eseguire e commit**

Run: `.venv/Scripts/python.exe tests/test_all.py`
Expected: entrambi i test del profilo PASS, e nessuna regressione.

```bash
git add tools/delugexml/groove.py tests/test_all.py
git commit -m "groove: il profilo di un esecuzione, e il residuo che resta tolto lo swing"
```

---

## Task 6: La scala di velocity aggregata

Il numero che sostituisce la tabella `[WEB]` dei cinque livelli, per il jazz. È **aggregato**, quindi `[MIS]` — ma solo se porta con sé quanti batteristi lo sostengono, perché è quello che decide fra `[MIS]` e `[OSS]`.

**Files:**
- Modify: `tools/delugexml/groove.py`
- Test: `tests/test_all.py`

**Interfaces:**
- Produces: `groove.Livelli(strumento, mediana, q1, q3, minimo, massimo, colpi, esecuzioni, batteristi)`, `groove.scala(base, *, style=None, beat_type='beat') -> dict[str, Livelli]`.

- [ ] **Step 1: Scrivere il test che fallisce**

```python
def test_groove_scala():
    """La scala di velocity, aggregata. SALTA senza il dataset.

    ⚠️ Ogni riga porta quanti BATTERISTI la sostengono, e non e' un dettaglio
    di rendicontazione: e' cio' che decide fra [MIS] e [OSS]. Sul reggae del
    Groove MIDI il batterista e' UNO, e chiamare [MIS] quel che ne esce
    sarebbe travestire un esecutore da repertorio.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    base = ROOT / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
    if not (base / GR.INVENTARIO).exists():
        raise FileNotFoundError(str(base / GR.INVENTARIO))

    jazz = GR.scala(base, style='jazz')
    check('il jazz ha il ride', 'ride' in jazz, str(sorted(jazz))[:120])
    r = jazz['ride']
    check('le velocity stanno fra 1 e 127',
          1 <= r.minimo <= r.mediana <= r.massimo <= 127,
          f'{r.minimo}/{r.mediana}/{r.massimo}')
    check('i quartili sono in ordine', r.q1 <= r.mediana <= r.q3,
          f'{r.q1}/{r.mediana}/{r.q3}')
    check('e la riga dichiara 5 batteristi', r.batteristi == 5,
          str(r.batteristi))

    reggae = GR.scala(base, style='reggae')
    check('il reggae ne dichiara UNO, ed e il motivo per cui resta [WEB]',
          all(v.batteristi == 1 for v in reggae.values()),
          str({k: v.batteristi for k, v in reggae.items()}))
```

- [ ] **Step 2: Eseguire e verificare che fallisca**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i groove_scala`
Expected: FAIL — `AttributeError: ... has no attribute 'scala'`

- [ ] **Step 3: Scrivere la funzione**

```python
class Livelli(NamedTuple):
    """La distribuzione delle velocity di uno strumento, su un sottoinsieme.

    ⚠️ `batteristi` NON e' rendicontazione: e' il numero che decide se
    l'affermazione e' [MIS] su un repertorio o [OSS] su un esecutore.
    """

    strumento: str
    mediana: int
    q1: int
    q3: int
    minimo: int
    massimo: int
    colpi: int
    esecuzioni: int
    batteristi: int


def scala(base: Path | str, *, style: str | None = None,
          beat_type: str | None = 'beat') -> dict[str, Livelli]:
    """La scala di velocity per strumento, su un sottoinsieme del dataset.

    Il default `beat_type='beat'` e' voluto: i `fill` sono un altro animale,
    e mescolarli alle esecuzioni continue alzerebbe le code senza dire niente
    di nessuno dei due. Per i fill si passa `beat_type='fill'`.
    """
    scelte = elenco(base, style=style, beat_type=beat_type)
    raccolta: dict[str, list[int]] = {}
    quali: dict[str, set[str]] = {}
    chi: dict[str, set[str]] = {}
    for e in scelte:
        f = MI.leggi(Path(base) / e.midi_filename)
        for t in f.tracce:
            for n in t.note:
                nome = MI.GM_PERCUSSIONI.get(n.y)
                if nome is None:
                    continue
                raccolta.setdefault(nome, []).append(n.velocity)
                quali.setdefault(nome, set()).add(e.id)
                chi.setdefault(nome, set()).add(e.drummer)

    fuori = {}
    for nome, vs in raccolta.items():
        vs.sort()
        q = statistics.quantiles(vs, n=4) if len(vs) >= 4 else [vs[0]] * 3
        fuori[nome] = Livelli(
            strumento=nome, mediana=int(statistics.median(vs)),
            q1=int(q[0]), q3=int(q[2]), minimo=vs[0], massimo=vs[-1],
            colpi=len(vs), esecuzioni=len(quali[nome]),
            batteristi=len(chi[nome]))
    return dict(sorted(fuori.items(), key=lambda kv: -kv[1].colpi))
```

- [ ] **Step 4: Eseguire e commit**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i groove_scala`
Expected: PASS.

```bash
git add tools/delugexml/groove.py tests/test_all.py
git commit -m "groove: la scala di velocity, col conteggio dei batteristi accanto"
```

---

## Task 7: `MU.applica_groove()` — il verbo che scrive

**Files:**
- Modify: `tools/delugexml/musica.py`
- Test: `tests/test_all.py`

**Interfaces:**
- Consumes: `groove.Profilo`, `groove.Passo` (Task 5), `notes.Note`, `musica.TICK_PER_PASSO`.
- Produces: `musica.applica_groove(note: list[Note], profilo, dove: str) -> dict[str, object]` con chiavi `'toccate'`, `'senza_appoggio'`, `'strumento'`, `'da'`.

- [ ] **Step 1: Scrivere il test che fallisce**

```python
def test_applica_groove():
    """Il template posato su un pattern di `passi()`.

    ⚠️ E il RIFIUTO che lo fa valere: su un passo dove quel batterista non ha
    mai suonato, la funzione NON inventa una velocity. E' lo stesso cancello
    della sigla sconosciuta in `MU.armonia()`, e serve alla stessa cosa --
    un template che riempie i buchi da se' sarebbe di nuovo inventare con la
    benedizione della riga scritta per impedirlo.
    """
    from delugexml import musica as MU                      # noqa: PLC0415
    from delugexml import groove as GR                      # noqa: PLC0415

    prof = GR.Profilo(
        id='finto/1', drummer='drummerX', style='jazz', bpm=120, bur=1.6,
        battute=1,
        passi={'ride': [GR.Passo(passo=0, velocity=104, scarto=2.0, colpi=8),
                        GR.Passo(passo=4, velocity=78, scarto=-1.0, colpi=8)]})

    note = MU.passi('x...x...........')
    rapporto = MU.applica_groove(note, prof, dove='ride')

    check('due note toccate', rapporto['toccate'] == 2, str(rapporto))
    check('la prima prende velocity e scarto',
          note[0].velocity == 104 and note[0].pos == 2,
          f'{note[0].velocity} {note[0].pos}')
    check('la seconda tiene indietro',
          note[1].velocity == 78 and note[1].pos == MU.TICK_PER_PASSO * 4 - 1,
          f'{note[1].velocity} {note[1].pos}')
    check('e nessun passo e rimasto senza appoggio',
          rapporto['senza_appoggio'] == [], str(rapporto['senza_appoggio']))

    orfane = MU.passi('x.x.x...........')
    r2 = MU.applica_groove(orfane, prof, dove='ride')
    check('il passo 2 non ha appoggio e lo DICE',
          r2['senza_appoggio'] == [2], str(r2['senza_appoggio']))
    check('e quella nota resta com era, non inventata',
          orfane[1].velocity == 90 and orfane[1].pos == MU.TICK_PER_PASSO * 2,
          f'{orfane[1].velocity} {orfane[1].pos}')

    check('uno strumento assente dal profilo e un errore che elenca',
          _raises(lambda: MU.applica_groove(MU.passi('x...'), prof,
                                            dove='rullante'), ValueError))

    # ⚠️ il residuo negativo sul PRIMO passo manderebbe la nota prima
    # dell'inizio della clip, che il Deluge non sa leggere: va fermata a 0.
    presto = GR.Profilo(
        id='finto/2', drummer='drummerX', style='jazz', bpm=120, bur=1.6,
        battute=1,
        passi={'kick': [GR.Passo(passo=0, velocity=100, scarto=-5.0,
                                 colpi=8)]})
    bordo = MU.passi('x...............')
    MU.applica_groove(bordo, presto, dove='kick')
    check('un residuo negativo sul primo passo si ferma a zero',
          bordo[0].pos == 0, str(bordo[0].pos))
    check('ma la velocity la prende lo stesso', bordo[0].velocity == 100,
          str(bordo[0].velocity))
```

- [ ] **Step 2: Eseguire e verificare che fallisca**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i applica_groove`
Expected: FAIL — `AttributeError: module 'delugexml.musica' has no attribute 'applica_groove'`

- [ ] **Step 3: Scrivere il verbo**

In `tools/delugexml/musica.py`, accanto agli altri verbi:

```python
def applica_groove(note, profilo, dove: str) -> dict[str, object]:
    """Posa velocity e residuo misurati su un pattern uscito da `passi()`.

    Il pattern resta la stringa leggibile che e'; il feel arriva da
    un'esecuzione vera. `dove` e' il nome GM dello strumento nel profilo.

    ⚠️ LO SWING NON E' QUI. Il profilo porta il solo RESIDUO -- il ride che
    spinge rispetto al rullante che tiene indietro -- perche' lo swing lo fa
    `song.set_swing()`, che e' di song e vale anche per basso e comping. Un
    template che portasse anche lo swing lo farebbe applicare due volte.

    ⚠️ NON INVENTA. Se il pattern chiede un colpo su un passo dove quel
    batterista non ha mai suonato, la nota resta com'e' e il passo finisce
    in `senza_appoggio`. Riempire i buchi da se' sarebbe inventare con la
    benedizione della funzione scritta per impedirlo.

    Ritorna un rapporto (regola 4: un'operazione silenziosa non e'
    correggibile).
    """
    if dove not in profilo.passi:
        raise ValueError(
            f'lo strumento {dove!r} non e\' nel profilo {profilo.id!r}: '
            f'ci sono {sorted(profilo.passi)}')
    per_passo = {p.passo: p for p in profilo.passi[dove]}

    toccate = 0
    senza = []
    for i, n in enumerate(note):
        passo = (n.pos // TICK_PER_PASSO) % 16
        misura = per_passo.get(passo)
        if misura is None:
            if passo not in senza:
                senza.append(passo)
            continue
        # `Note` e' una dataclass MUTABILE (verificato): si scrivono i campi.
        # `max(0, ...)` perche' un residuo negativo sul primo passo manderebbe
        # la nota prima dell'inizio della clip, che il Deluge non sa leggere.
        n.velocity = misura.velocity
        n.pos = max(0, n.pos + int(round(misura.scarto)))
        toccate += 1

    return {'strumento': dove, 'da': profilo.id, 'toccate': toccate,
            'senza_appoggio': sorted(senza)}
```

- [ ] **Step 4: Eseguire e verificare che passi**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i applica_groove`
Expected: PASS su tutte e otto le condizioni.

- [ ] **Step 5: Commit**

```bash
git add tools/delugexml/musica.py tests/test_all.py
git commit -m "musica: applica_groove, e il rifiuto sui passi senza appoggio"
```

---

## Task 8: Le misure vere, e le caselle 4, 6 e 9 del jazz

Qui non si scrive codice: si **eseguono** le misure e si scrivono i numeri dove servono a prendere una decisione musicale.

**Files:**
- Create: `tools/misura_groove.py`
- Modify: `docs/repertori/jazz.md` (caselle 4, 6, 9)
- Create: `out/groove_jazz.txt` (l'uscita grezza delle misure, **non** versionata — controllare che `out/` sia già in `.gitignore` tranne `format_table.json`)

- [ ] **Step 1: Eseguire le misure e salvarle**

Scrivere `tools/misura_groove.py` — uno script di misura, non libreria, come già esistono altri strumenti sotto `tools/`:

```python
"""Le misure che riempiono la casella 6 del jazz. Uscita in `out/`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from delugexml import groove as GR                          # noqa: E402

BASE = Path('to-read/MIDI/groove-v1.0.0-midionly/groove')
STILE = 'jazz'


def main() -> None:
    print(f'=== scala di velocity, {STILE}, beat ===')
    for v in GR.scala(BASE, style=STILE).values():
        print(f'{v.strumento:24s} mediana {v.mediana:3d}  '
              f'q1-q3 {v.q1:3d}-{v.q3:3d}  min-max {v.minimo:3d}-{v.massimo:3d}'
              f'  colpi {v.colpi:6d}  esecuzioni {v.esecuzioni:3d}'
              f'  batteristi {v.batteristi}')

    print(f'\n=== scala di velocity, {STILE}, fill ===')
    for v in GR.scala(BASE, style=STILE, beat_type='fill').values():
        print(f'{v.strumento:24s} mediana {v.mediana:3d}  '
              f'colpi {v.colpi:6d}  esecuzioni {v.esecuzioni:3d}')

    print(f'\n=== BUR per esecuzione, {STILE}, beat 4/4 ===')
    bur = []
    for e in GR.elenco(BASE, style=STILE, beat_type='beat',
                       time_signature='4-4'):
        p = GR.profilo(BASE, e.id)
        if p.bur is None:
            continue
        bur.append(p.bur)
        print(f'{e.id:28s} {e.style:16s} {e.bpm:4d} BPM  BUR {p.bur:.2f}')
    if bur:
        bur.sort()
        print(f'\nmediana su {len(bur)} esecuzioni: {bur[len(bur) // 2]:.2f}')

    print('\n=== profilo del template ===')
    scelte = [e for e in GR.elenco(BASE, style='jazz/swing', beat_type='beat',
                                   time_signature='4-4')]
    scelta = max(scelte, key=lambda e: e.duration)
    print(GR.racconta(BASE, scelta.id))
    p = GR.profilo(BASE, scelta.id)
    print(f'BUR {p.bur:.2f}, battute {p.battute}')
    for nome, passi in p.passi.items():
        if sum(s.colpi for s in passi) < 20:
            continue                    # troppo raro per dire qualcosa
        righe = '  '.join(f'{s.passo:2d}:v{s.velocity:3d}/{s.scarto:+.1f}'
                          for s in passi)
        print(f'{nome:24s} {righe}')


if __name__ == '__main__':
    main()
```

Eseguire e salvare:

```bash
.venv/Scripts/python.exe tools/misura_groove.py > out/groove_jazz.txt
```

⚠️ `out/` è ignorato tranne `format_table.json`: **verificare** che `out/groove_jazz.txt` non finisca in `git status` prima di committare. Se ci finisce, non aggiungerlo — è un artefatto derivato da materiale non versionato.

- [ ] **Step 2: Scegliere l'esecuzione del template e dichiararla**

Criterio: la più lunga fra `style='jazz/swing'`, `beat_type='beat'`, `time_signature='4-4'` — che al 18 agosto 2026 è `drummer1/session3/2`, 185 BPM, 250 s. **Va nominata nella scheda con batterista, stile e BPM**, perché è `[OSS]` su un esecutore e non `[MIS]` su un repertorio.

- [ ] **Step 3: Scrivere la casella 6**

Sostituire il corpo di `## 6. Dinamica` in `docs/repertori/jazz.md`. Deve contenere, e **niente di più**:

1. la scala di velocity per strumento (`ride`, `kick`, `rullante`, `charleston`), con mediana e quartili, marcata `[MIS]` e **col numero di esecuzioni e di batteristi accanto**;
2. la frase che qualifica il numero: cinque batteristi di studio, `drummer1` domina con 19 `beat` su 50;
3. la **delimitazione**: che `jazz/funk` (24) e `jazz/fusion` (11) stanno dentro l'etichetta ma fuori dallo swing, e che le misure di swing li escludono;
4. il **profilo posizionale** — quali passi il batterista accenta davvero;
5. il **rimando** alla casella 4 per il BUR, senza copiarlo;
6. come si usa: `GR.profilo(base, id)` + `MU.applica_groove(note, prof, dove=…)`;
7. **cancellare** la riga «*Nel frattempo, per comporre*», che esiste solo finché la casella è vuota.

- [ ] **Step 4: Scrivere nella casella 4**

Aggiungere una sottosezione «Lo swing, misurato una seconda volta» con il BUR del Groove MIDI accanto a quello di Weimar, e **i due metodi dichiarati** (Weimar: onset veri contro battiti annotati, 333 assoli; Groove MIDI: onset contro griglia MIDI, N esecuzioni). Se divergono, si scrivono entrambi e si dice che non si sa quale credere — non si sceglie il più comodo.

- [ ] **Step 5: Scrivere nella casella 9**

I `fill`: 51 esecuzioni jazz, cosa dicono di densità (colpi per battuta rispetto al `beat`) e di collocazione. Portare la casella da **vuota** a **parziale**, e dire di cosa: manca la forma (AABA, il blues), ci sono i fill.

- [ ] **Step 6: Verificare che il test dell'indice se ne accorga**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i indice`
Expected: **FAIL** — l'indice in `MUSICA.md` dice ancora `○` dove la scheda ora dice pieno. È il test che funziona; si sistema al Task 9.

- [ ] **Step 7: Commit**

```bash
git add tools/misura_groove.py docs/repertori/jazz.md
git commit -m "musica: la dinamica del jazz, misurata su cinque batteristi"
```

---

## Task 9: Il reggae, il comune, l'indice, la skill

- [ ] **Step 1: Correggere la casella 6 del reggae**

In `docs/repertori/reggae-dub.md`, sostituire la sottosezione «L'agenda: qui i `[WEB]` si possono rimpiazzare con dei `[MIS]`». Il titolo stesso è la cosa da correggere. Scrivere: 20 esecuzioni ma **2 batteristi, uno con 18**, e **4 sole `beat`** (78, 78, 141, 126 BPM) più 16 fill da meno di tre secondi, dieci minuti in tutto — quindi la casella **resta `[WEB]`**, e il perché. Rimandare alla casella 6 del jazz per la scala misurata, senza copiarne i numeri.

- [ ] **Step 2: Il comune di `MUSICA.md`**

In «Velocity groove»: la tabella `[WEB]` dei cinque livelli **resta dov'è** — vale per tutti i generi ed è quello che c'è quando un repertorio non ha misure sue — con accanto **un rimando** alla casella 6 del jazz, mai una copia. In «La macchina»: il **groove template** e il **quantize/humanize del dispositivo** (`AUDITION` + `TEMPO`, orario quantizza, antiorario umanizza, per riga e **distruttivo**), che cancella il template senza che chi lo gira lo sappia.

- [ ] **Step 3: L'indice**

Nella matrice in fondo a `MUSICA.md`: **jazz 6 da `○` a `●`, jazz 9 da `○` a `◐`**.

- [ ] **Step 4: Far passare il test dell'indice**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i indice`
Expected: PASS. Se fallisce, **è l'indice a sbagliare, non la scheda**: la scheda è la fonte, l'indice ne è la vista.

- [ ] **Step 5: `SKILL.md`**

In `.claude/skills/deluge-pal/SKILL.md`: `from delugexml import groove as GR` nel blocco delle importazioni, e una sottosezione «Importare dal Groove MIDI» accanto a quella della Weimar, con la tabella `per`/`usare` delle cinque funzioni pubbliche e le due avvertenze (il prefisso; che il template è `[OSS]` su un esecutore). Sotto «Importare MIDI», dove i groove template sono nominati da sempre, sostituire la promessa col rimando a `GR`.

- [ ] **Step 6: Eseguire tutta la suite e commit**

Run: `.venv/Scripts/python.exe tests/test_all.py`
Expected: tutti verdi. Annotare il **conteggio esatto** dei test, che serve al Task 10.

```bash
git add docs/repertori/reggae-dub.md docs/MUSICA.md .claude/skills/deluge-pal/SKILL.md
git commit -m "musica: il reggae che il corpus non regge, e l indice allineato"
```

---

## Task 10: Il cancello sul dispositivo

**Il solo task che può dichiarare il lavoro finito.** Fin qui nessuna nota fuori griglia è mai uscita da un Deluge.

- [ ] **Step 1: Costruire la coppia controllata**

Una clip di **sola batteria**, non un pezzo jazz. Stesso pattern due volte: `GROOVE0` senza template, `GROOVE1` con `MU.applica_groove()`. Passare da `MU.verifica(doc)` (regola 3) e raccontare con `MU.racconta(doc)` (regola 4). Percorsi con `MU.destinazione('groove', 0)` e `MU.destinazione('groove', 1)`, **mai a mano** (regola 5).

- [ ] **Step 2: Caricare e riscaricare**

```bash
.venv/Scripts/python.exe tools/dsysex.py --in "Deluge 0" --out "Deluge 1" put out/GROOVE1.XML "/SONGS/DelugePal/GROOVE1.XML"
```

Poi `get` dello stesso percorso e confronto attributo per attributo. **Questo dice solo che il giro è pulito**, non che il Deluge accetti le posizioni.

- [ ] **Step 3: La prova che decide — chiedere all'utente**

Chiedere all'utente di **aprire `GROOVE1` sul Deluge e risalvarla**. Poi riscaricarla e confrontare le posizioni delle note con quelle scritte.

- se tornano sulla griglia → **il Deluge riquantizza**, il template va ripensato, e cade **solo lo scarto di posizione**: la misura, la scala di velocity e il confronto BUR restano validi;
- se restano → il meccanismo è verificato sul dispositivo, e lo si può scrivere come tale.

⚠️ **Non dire «verificato sul dispositivo» avendo ascoltato**, né viceversa. Il punto 3 è ciò che si vede; il punto 4 è ciò che si sente. Sono due affermazioni diverse e vanno scritte separate.

- [ ] **Step 4: L'ascolto**

Far ascoltare all'utente `GROOVE0` e `GROOVE1` in fila, e chiedere se il residuo si sente o se sta sotto la soglia. La risposta va nella casella 6 del jazz **con la data**, e se è una correzione va anche nella casella 11 — che è vuota per costruzione e si riempie solo così.

- [ ] **Step 5: Scrivere l'esito nella casella 10 e in `HANDOFF.md`**

Nella casella 10 di `docs/repertori/jazz.md` vanno **quattro cose e nessuna di più**:

1. **come si scrive un template nel jazz**: `GR.profilo()` + `MU.applica_groove()`, con l'esecuzione nominata, e che lo swing lo fa `set_swing(doc, …, figura='1/8')` — il template porta solo il residuo;
2. **cosa è stato verificato sul dispositivo e cosa no**, distinti in due frasi separate. Il punto 3 del cancello è ciò che *si vede*; il punto 4 è ciò che *si sente*. Non scrivere «verificato sul dispositivo» per l'ascolto, né viceversa;
3. un **rimando** al comune per il quantize/humanize (`AUDITION` + `TEMPO`) — **non una copia**: il meccanismo è di macchina e vale per tutti i repertori, quindi vive nel comune e qui c'è solo il rimando. È la regola violata e corretta tre volte nella sessione precedente;
4. una riga su `length` di `<noteRow>`: che il poliritmo è **un meccanismo altro**, serve ai tempi dispari e non allo swing di crome in 4/4, e che **non è verificato sul dispositivo** — col rimando al punto aperto in `HANDOFF.md` §7.

In `HANDOFF.md`, una **6-terdecies** con: l'origine della griglia (il trabocchetto, e che si è visto perché *tutti* gli strumenti avevano lo stesso picco), il doppio swing e la spartizione, il reggae che il corpus non regge, il 384esimo che è un tick, e l'esito del cancello. Aggiornare il conteggio dei test in testa al documento e in §2 col numero **misurato** al Task 9, non stimato — e se una cifra è derivata invece che rimisurata, dichiararlo come tale.

- [ ] **Step 6: Commit**

```bash
git add docs/repertori/jazz.md HANDOFF.md
git commit -m "handoff: il groove template sul dispositivo, e cosa ha detto l ascolto"
```

---

## Note per chi esegue

- **Se il Task 5 dà un residuo grande** (sopra i 12 tick), la catena è sbagliata: si controlla nell'ordine l'origine (Task 3) e poi la rimozione dello swing (`_senza_swing`). Non si allarga la tolleranza del test.
- **Se una misura non riproduce una previsione nota** — per esempio se il BUR del Groove MIDI venisse 1,0 tondo — la misura è sbagliata anche se è ripetibile. È già successo tre volte su questo progetto, sempre sull'origine.
- **I numeri contati il 18 agosto 2026** (1150, 101, 50, 20, 4, 5 batteristi) sono lo stato del disco di quel giorno. Se un test li trova diversi, il dataset è cambiato: si aggiornano i numeri e **si aggiorna anche la data** nelle schede.
