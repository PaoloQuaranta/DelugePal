# Prestito modale (modal interchange) — piano d'implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** scrivere la seconda istruzione armonica del progetto — prendere in prestito un accordo da un modo parallelo per colorare una tonalità di casa — e provarla su un pezzo in Do maggiore costruito da zero, col *iv* minore come colore centrale, caricato sul Deluge.

**Architecture:** un'istruzione in prosa (`docs/istruzioni/armonia-prestito.md`) fondata sulla fonte e blindata da due test di guardia; un pezzo di prova composto nota per nota (`tools/prestito_scritto.py`, nessun sorteggio); l'assemblaggio in song e il caricamento via SysEx fatti a mano con la libreria, come per PERCHE. Le note le decide la composizione, le primitive (`MU.armonia`, `MU.melodia`) calcolano.

**Tech Stack:** Python 3 (stdlib + `tools/delugexml`), il runner di test custom in `tests/test_all.py`, `tools/dsysex.py` per il trasferimento USB.

## Global Constraints

- **Fonte del mestiere:** Smith, *Jazz Theory* (4ª ed.), cap. VIII «Functional Harmony», p. 66-69, e cap. IX «Chord-Scale Theory», p. 75 («Borrowed chords»); Piston, *Harmony* (5ª ed.), i capitoli sul mixture. Il materiale è in `to-read/`, **non versionato**.
- **I gradi di prova:** `[LIB]` (libro + pagina), `[CALC]` (calcolo verificato da un test), `[DEC]` (decisione, con la ragione), `[OSS]` (osservato all'ascolto).
- **Niente sorteggio, niente campionamento:** ogni nota è una scelta, col motivo accanto. Le primitive calcolano, non pescano.
- **Voicing per terze, non quartale** — lezione di PERCHE (11 settembre): il quartale è un colore, non un traguardo.
- **Le maiuscole contano nelle sigle:** `Cm7` ≠ `CM7`. Una sigla sconosciuta viene rifiutata da `MU.sigla()`; non inventarla.
- **File a LF, mai CRLF.** Write/Edit scrivono già LF; prima di committare verifica `git diff --cached --stat` == `git diff --cached --stat --ignore-cr-at-eol`.
- **Messaggi di commit:** stile del progetto — `area: descrizione`, **senza accenti** (usa `priorita'`, `perche'`). Ogni commit termina con la riga trailer: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **I test si lanciano** dalla radice con `.venv/Scripts/python.exe tests/test_all.py`; il runner esegue TUTTE le `test_*`. Per vedere le righe di un test nuovo, filtra l'output: `… tests/test_all.py 2>&1 | grep -i prestito`.

---

### Task 1: I due test di guardia

Due test in `tests/test_all.py`. Sono **test di guardia**: verificano fatti che devono restare veri, non codice nuovo — quindi passano al primo colpo se la premessa regge (ed è proprio quello che confermano). Vanno accanto a `test_armonia_modale_note_caratteristiche` (≈ riga 7368), così i test d'armonia stanno insieme.

**Files:**
- Modify: `tests/test_all.py` (aggiungere due funzioni vicino a riga 7368)

**Interfaces:**
- Consumes: `delugexml.musica.voci(sigla) -> list[int]`, `delugexml.musica.armonia(spec, *, registro, durata) -> dict[int, list[Note]]`, `delugexml.song.MODI: dict[str, tuple[int,...]]`; l'helper `check(name, cond, detail='')` del file.
- Produces: due `test_*` che il runner raccoglie da sé.

- [ ] **Step 1: Scrivere il test della pipeline (accordo fuori scala)**

Questo chiude il rischio dichiarato nella spec: l'Fm ha il la bemolle, fuori dal Do maggiore, e `voci()`/`armonia()` lo realizzano lo stesso perché partono dalla sigla, non dalla scala.

```python
def test_armonia_prestito_accordo_fuori_scala():
    """La premessa di docs/istruzioni/armonia-prestito.md.

    Il iv minore (Fm in Do maggiore) ha il la bemolle, che non e' nel Do
    maggiore. voci()/armonia() lo calcolano dalla sigla, non dalla scala --
    e set_scale() non tocca le note gia' scritte (e' scritto nella sua
    docstring): sul Deluge la scala e' il layout della griglia, non un filtro.
    """
    from delugexml import musica as MU                         # noqa: PLC0415

    classi = {y % 12 for y in MU.voci('Fm7')}
    check('Fm7 contiene il la bemolle (classe 8)',
          8 in classi, str(sorted(classi)))

    note = MU.armonia('Cmaj7 | Fm7 | Cmaj7', registro='do3', durata='1/1')
    altezze = {y % 12 for y in note}
    check('il giro col iv minore porta il la bemolle',
          8 in altezze, str(sorted(altezze)))
```

- [ ] **Step 2: Scrivere il test [CALC] del vocabolario**

Rispecchia `test_armonia_modale_note_caratteristiche`: deriva i fatti da `S.MODI` e li asserisce. Blinda le affermazioni `[CALC]` che l'istruzione (Task 2) farà sui prestiti.

```python
def test_armonia_prestito_accordi_dal_parallelo():
    """Le affermazioni [CALC] di docs/istruzioni/armonia-prestito.md.

    In una casa maggiore i prestiti vengono dal minore parallelo: le note di
    colore -- b3, b6, b7 -- sono esattamente quelle che il minore ha e il
    maggiore no. Se qualcuno cambia song.MODI, questo prende il documento che
    mente.
    """
    from delugexml import musica as MU, song as S              # noqa: PLC0415
    mag, minn = set(S.MODI['maggiore']), set(S.MODI['minore'])

    check('il minore parallelo abbassa b3, b6, b7',
          minn - mag == {3, 8, 10}, str(sorted(minn - mag)))

    # prestito -> la sua nota di colore, classe relativa alla tonica (Do = 0)
    prestiti = {'Fm': 8, 'Ab': 8, 'Bb': 10, 'Eb': 3, 'Cm': 3, 'Dm7b5': 8}
    for testo, colore in prestiti.items():
        classi = {y % 12 for y in MU.voci(testo)}
        check(f'{testo}: porta la nota di colore {colore}',
              colore in classi, str(sorted(classi)))
        check(f'{testo}: quella nota e fuori dal Do maggiore',
              colore not in mag, f'{colore} in {sorted(mag)}')
```

- [ ] **Step 3: Lanciare i due test**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i "prestito\|bemolle\|parallelo"`
Expected: tutte le righe `PASS`. Se una è `FAIL`, la premessa non regge: **fermarsi e riferire** (non aggirare — vuol dire che una sigla non si realizza come previsto, o che `MODI` è cambiato).

- [ ] **Step 4: Lanciare la suite intera (niente regressioni)**

Run: `.venv/Scripts/python.exe tests/test_all.py`
Expected: l'ultima riga dice `N/N test superati` con lo stesso numero di fallimenti di prima (0, salvo i `COPPIE_OSSERVATE` già noti come rossi in locale — vedi HANDOFF §6-sexdecies).

- [ ] **Step 5: Commit**

```bash
git add tests/test_all.py
git commit -m "test: i due guardiani del prestito modale -- pipeline e [CALC]" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: L'istruzione `armonia-prestito.md`

La prosa, fondata sulla fonte, nella forma collaudata delle istruzioni. Prima **leggere** le pagine: Smith p. 66-69 e p. 75 (già estraibili da `to-read/Jazz Theory.pdf`, testo, non scansione), e in Piston il capitolo sul mixture/accordi presi in prestito (`to-read/`). Le affermazioni `[CALC]` della tabella sono già blindate dal Task 1.

**Files:**
- Create: `docs/istruzioni/armonia-prestito.md`
- Modify: `docs/istruzioni/armonia-modale.md` (il punto «il modal interchange» in «Cosa manca a questa istruzione», righe ≈ 213-215)

**Interfaces:**
- Consumes: i fatti blindati da `test_armonia_prestito_accordi_dal_parallelo`; l'API in «come si scrive» (`S.set_scale`, `MU.armonia`), verificata dal Task 1.
- Produces: il file che il Task 3 e il Task 5 citano come loro fonte; la sezione «Esempio lavorato» che il Task 5 riempirà.

- [ ] **Step 1: Leggere la fonte**

Estrarre e leggere Smith p. 66-69 (già fatto in brainstorming, ma rileggere) e p. 73-76 (cap. IX, «Borrowed chords»), e trovare in Piston il capitolo del mixture. Comando per estrarre una pagina in UTF-8 (la console Windows va in errore se si stampa diretto):

```bash
.venv/Scripts/python.exe - <<'PY'
from pypdf import PdfReader
r = PdfReader("to-read/Jazz Theory.pdf")
open("scratch_p75.txt","w",encoding="utf-8").write(r.pages[74].extract_text() or "")
PY
```

- [ ] **Step 2: Scrivere il documento**

Struttura (come `armonia-modale.md`): **A cosa serve** → **Il grado di prova** (`[LIB]`/`[CALC]`/`[DEC]`/`[OSS]`) → **Il principio** (una casa, un colore preso a prestito; il contrasto con l'armonia modale, linkato) → **Il vocabolario** (la tabella qui sotto) → **I vincoli** → **La procedura locale** → **Come si scrive** → **Esempio lavorato** (da riempire al Task 5) → **Cosa manca**.

La tabella del vocabolario, prestiti in una casa maggiore (da blindare col test del Task 1):

| prestito | accordo in Do | colore | fonte |
|---|---|---|---|
| **iv** | Fm | caldo, plagale, nostalgico | `[LIB]` Smith p. 66 (*Sunny Side of the Street*) |
| **♭VI** | A♭ | cinematografico, ampio | `[LIB]` Piston (mixture) |
| **♭VII** | B♭ | modale/rock; il I↔♭VII «tonic-by-assertion» | `[LIB]` Smith p. 69 (*Killer Joe*) |
| **♭III** | E♭ | scuro, bluesy | `[CALC]` dal minore parallelo |
| **♭II** | D♭ | napoletano, teatrale | `[LIB]` Piston |
| **Im / I→Im** | Cm | scivolata luce→ombra | `[LIB]` Smith p. 67 (*On Green Dolphin Street*) |
| **iiø7** | Dm7♭5 | tensione pre-cadenza | `[CALC]` dal minore |

I vincoli (ognuno nella forma «cosa NON fare, e perché»): **torna a casa** (se non torni, hai modulato — Smith tratta la modulazione a parte, p. 67-68); **non incatenare** due-tre prestiti di fila; il prestito in **posizione di colore/passaggio**; **la melodia regge la nota presa in prestito** (il la♭ del Fm stona se la melodia batte il la naturale).

La procedura locale (forma «una decisione, poi si compone»): 1) parti da un giro diatonico; 2) scegli il punto del colore (spesso il IV→iv, o prima di un ritorno a I); 3) prendi l'accordo dal parallelo per colore (caldo→iv, cupo→♭VI/♭II, rock→♭VII); 4) controlla i vincoli.

«Come si scrive» — il blocco verificato dal Task 1:

```python
from delugexml import song as S, musica as MU
S.set_scale(doc, 'C', 'maggiore')
note = MU.armonia('Cmaj7 | Fmaj7 | Fm7 | Cmaj7', registro='do3', durata='1/1')
# voicing per terze (default 'chiuso'), NON quartale
```

- [ ] **Step 3: Linkare le due istruzioni**

In `armonia-prestito.md` il principio rimanda a `armonia-modale.md` come orientamento opposto. In `armonia-modale.md`, il punto «il modal interchange» di «Cosa manca» (righe ≈ 213-215) smette di essere un rimando al libro e diventa un rimando al documento nuovo:

```
- **il modal interchange** — prendere in prestito un accordo da un modo
  parallelo, che è il ponte verso l'eclettismo che l'utente cerca: ora c'è,
  in `docs/istruzioni/armonia-prestito.md`.
```

- [ ] **Step 4: Verificare LF e che i test reggano ancora**

Run: `git add docs/istruzioni/armonia-prestito.md docs/istruzioni/armonia-modale.md && git diff --cached --stat && git diff --cached --stat --ignore-cr-at-eol`
Expected: i due conteggi coincidono.
Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | tail -3`
Expected: stesso numero di fallimenti di prima (le affermazioni `[CALC]` dell'istruzione sono già coperte dal Task 1).

- [ ] **Step 5: Commit**

```bash
git commit -m "istruzioni: la seconda armonica -- prendere in prestito (modal interchange)" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Il pezzo di prova composto

Lo script che tiene il materiale del pezzo — progressione, melodia, basso — con la ragione accanto a ogni scelta, come `walking_scritto.py`. Nessun sorteggio. Non assembla la song (quello è il Task 4): produce il materiale e lo si può raccontare.

**Files:**
- Create: `tools/prestito_scritto.py`
- Modify: `tests/test_all.py` (una `test_*` accanto a `test_walking_scritto`, ≈ riga 7329)

**Interfaces:**
- Consumes: `MU.armonia`, `MU.melodia` (dict altezza→`list[Note]`, `Note.pos` in tick), `MU.racconta_armonia`.
- Produces: `PROGRESSIONE: str`, `MELODIA: str`, `BASSO: str`, e `comping()/tema()/basso()` che il Task 4 usa per riempire le clip.

- [ ] **Step 1: Scrivere il test (fallisce: il modulo non esiste)**

```python
def test_prestito_scritto():
    """Il pezzo di prova del prestito modale sta in piedi (non che sia bello).

    armonia-prestito.md, esempio lavorato: un giro in Do maggiore col iv
    minore (Fm7) alla battuta 4, e la melodia che ci canta sopra il la bemolle.
    """
    import prestito_scritto as PR                              # noqa: PLC0415
    from delugexml import musica as MU                         # noqa: PLC0415

    accordi = [a.strip() for a in PR.PROGRESSIONE.split('|')]
    check('il giro ha 8 battute', len(accordi) == 8, str(len(accordi)))
    check('il iv minore (Fm7) e alla battuta 4', accordi[3] == 'Fm7', accordi[3])
    check('il giro torna a casa sul Cmaj7', accordi[-1] == 'Cmaj7', accordi[-1])

    # la melodia: la naturale (9) sulla battuta 3 (Fmaj7), la bemolle (8) sulla
    # 4 (Fm7) -- e' il colore IV->iv portato in cima
    per_battuta: dict[int, set[int]] = {}
    for y, note in MU.melodia(PR.MELODIA, durata='1/1').items():
        for n in note:
            per_battuta.setdefault(n.pos // 384, set()).add(y % 12)
    check('battuta 3 (Fmaj7): la melodia ha il la naturale (9)',
          9 in per_battuta.get(2, set()), str(sorted(per_battuta.get(2, set()))))
    check('battuta 4 (Fm7): la melodia ha il la bemolle (8)',
          8 in per_battuta.get(3, set()), str(sorted(per_battuta.get(3, set()))))
```

- [ ] **Step 2: Lanciare il test, verificare che fallisce**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i "prestito_scritto\|battuta"`
Expected: FAIL — `ModuleNotFoundError: No module named 'prestito_scritto'` (il runner lo marca come eccezione del test).

- [ ] **Step 3: Scrivere lo script**

```python
"""Il pezzo di prova del prestito modale, COMPOSTO seguendo
docs/istruzioni/armonia-prestito.md.

Un giro in Do maggiore col iv minore (Fm7) come colore centrale -- il prestito
piu' caldo, dal Do minore parallelo (Smith, Jazz Theory, p. 66). La melodia ci
canta sopra il la bemolle: e' li' che il prestito si sente, in cima.

Nessun sorteggio: ogni nota e' una scelta, col motivo accanto.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: 8 battute. Il IV diventa iv fra la 3 e la 4: Fmaj7 -> Fm7, il prestito.
#: Poi ii-V (Dm7 G7) e ritorno a casa. Una sola sigla per battuta.
PROGRESSIONE = 'Cmaj7 | Em7 | Fmaj7 | Fm7 | Em7 | Dm7 | G7 | Cmaj7'

#: La melodia, una nota per battuta, registro do4 (sopra il comping a do3).
#: Il la naturale della battuta 3 (su Fmaj7) scende al la bemolle della 4 (su
#: Fm7): e' il colore IV->iv portato in cima, la ragione del pezzo.
MELODIA = 'mi4 sol4 la4 lab4 sol4 fa4 re4 do4'

#: Il basso sulle fondamentali, una per battuta, registro do2.
BASSO = 'do2 mi2 fa2 fa2 mi2 re2 sol2 do2'


def comping():
    """Gli accordi, voicing per terze (NON quartale -- lezione di PERCHE)."""
    return MU.armonia(PROGRESSIONE, voicing='chiuso', registro='do3', durata='1/1')


def tema():
    """La melodia sopra il comping."""
    return MU.melodia(MELODIA, durata='1/1')


def basso():
    """Il basso sulle fondamentali."""
    return MU.melodia(BASSO, durata='1/1')


if __name__ == '__main__':
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3'))
```

- [ ] **Step 4: Lanciare il test, verificare che passa**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -i "battuta\|8 battute\|casa"`
Expected: tutte `PASS`.

- [ ] **Step 5: Guardare cosa dice (regola 4: raccontare)**

Run: `.venv/Scripts/python.exe tools/prestito_scritto.py`
Expected: `racconta_armonia` stampa le note di ogni sigla; controlla a occhio che la battuta 4 (Fm7) porti fa-la♭-do-mi♭.

- [ ] **Step 6: Commit**

```bash
git add tools/prestito_scritto.py tests/test_all.py
git commit -m "prestito: il pezzo di prova in Do, col iv minore alla battuta 4" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Assemblaggio + caricamento + ascolto (interattivo)

⚠️ **Questo task è interattivo e dipende dal dispositivo.** Non è automatizzabile: serve il Deluge collegato e i preset locali dell'utente (`refs/`, non versionati). È il flusso della skill `deluge-pal` («Come si fa» + «Trasferimento»), e la prova vera del pezzo. Se il Deluge non risponde al `ping`, salvare il file locale e dirlo — non fingere che sia salito.

**Files:**
- Nessun file versionato (la song non è pubblicabile: §9 dell'HANDOFF). L'XML va in scratchpad o direttamente sulla SD via `dsysex`.

**Interfaces:**
- Consumes: `prestito_scritto.comping()/tema()/basso()`; `create.add_track`, `musica.scrivi`, `song.set_scale`, `musica.verifica`, `musica.racconta`, `writer.write_file`, `dsysex.py`.

- [ ] **Step 1: Costruire la song**

Partire da un template di song vuoto (locale, non versionato, es. `refs/songs/TEMPL0.XML`) e istanziare tre tracce da preset scelti fra quelli dell'utente in `refs/synths/` (una tastiera per il comping, un lead per la melodia, un basso). ⚠️ `playing=True` su ogni traccia, se no premere play non fa partire niente (costò un blocco del Deluge il 17 agosto).

```python
import sys; sys.path.insert(0, 'tools')
from delugexml import parse_file, write_file, musica as MU
from delugexml import song as S, create as C
from delugexml.writer import FormatTable
import prestito_scritto as PR

doc = parse_file('refs/songs/TEMPL0.XML')   # template locale, non versionato
S.set_scale(doc, 'C', 'maggiore')
# i nomi dei preset dipendono da cosa c'e' in refs/synths/: sceglierli a mano
_, clip_keys  = C.add_track(doc, 'refs/synths/<tastiera>.XML', name='PRESTITO-KEYS',  folder='SYNTHS', length=8*384, playing=True)
_, clip_lead  = C.add_track(doc, 'refs/synths/<lead>.XML',     name='PRESTITO-LEAD',  folder='SYNTHS', length=8*384, playing=True)
_, clip_bass  = C.add_track(doc, 'refs/synths/<basso>.XML',    name='PRESTITO-BASS',  folder='SYNTHS', length=8*384, playing=True)
MU.scrivi(doc, clip_keys, PR.comping())
MU.scrivi(doc, clip_lead, PR.tema())
MU.scrivi(doc, clip_bass, PR.basso())
```

- [ ] **Step 2: Controllare e raccontare (regole 3 e 4)**

```python
print(MU.verifica(doc))      # deve essere vuota, se no NON caricare
print(MU.avvertenze(doc))    # non blocca, ma va detto cosa non si vedra'
print(MU.racconta(doc))
write_file(doc, 'scratch_prestito.XML', FormatTable.load('out/format_table.json'))
```

Expected: `verifica()` vuota. Se non lo è, fermarsi e riferire.

- [ ] **Step 3: Caricare sul Deluge**

```bash
.venv/Scripts/python.exe tools/dsysex.py --in "Deluge 0" --out "Deluge 1" put scratch_prestito.XML "$(.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tools'); from delugexml import musica as MU; print(MU.destinazione('prestito', 1))")"
```

(Oppure costruire il percorso con `MU.destinazione('prestito', 1)` → `/SONGS/DelugePal/PRESTITO01.XML` e passarlo a `put`.) Le porte vanno sempre indicate; `put` rilegge e confronta gli hash da sé.

- [ ] **Step 4: L'utente apre e ascolta**

Chiedere all'utente di aprire `PRESTITO01` sul Deluge e ascoltare, con attenzione alla battuta 4 (il IV che diventa iv, il la♭ in cima). Raccogliere il **verdetto** testuale — è lui che chiude l'istruzione al Task 5, come *«frigio mi piace molto»* chiuse l'armonia modale.

---

### Task 5: Piegare il verdetto nell'esempio lavorato

Con il verdetto dell'utente in mano, riempire la sezione «Esempio lavorato» di `armonia-prestito.md` — la progressione, la scelta del la♭ in cima, e cosa l'utente ha detto (`[OSS]`). Se il verdetto chiede cambiamenti (un prestito diverso, un voicing diverso), applicarli a `prestito_scritto.py` **prima** di scrivere l'esempio, e ripetere il Task 4.

**Files:**
- Modify: `docs/istruzioni/armonia-prestito.md` (sezione «Esempio lavorato»)
- Modify (se il verdetto lo chiede): `tools/prestito_scritto.py`

**Interfaces:**
- Consumes: il verdetto del Task 4; la struttura dell'istruzione del Task 2.

- [ ] **Step 1: Scrivere l'esempio lavorato**

Nella forma di PERCHE in `armonia-modale.md`: l'idea (Do maggiore da zero), cosa si è fatto (il IV→iv alla battuta 4, il la♭ in cima), la progressione, e **il verdetto dell'utente** marcato `[OSS]` con la data. Se è emersa una lezione (come «il quartale non è meglio» per il modale), scriverla.

- [ ] **Step 2: Aggiornare «Cosa manca» se serve**

Se il pezzo ha scoperto un bisogno del flusso «da zero» che l'«armonizzare» non aveva (una melodia inventata, una forma), annotarlo in «Cosa manca a questa istruzione». La direzione inversa (casa minore che prende dal maggiore) resta comunque lì, non provata.

- [ ] **Step 3: Verificare LF e commit**

```bash
git add docs/istruzioni/armonia-prestito.md tools/prestito_scritto.py
git diff --cached --stat && git diff --cached --stat --ignore-cr-at-eol
git commit -m "prestito: l'esempio lavorato, col verdetto sul pezzo in Do" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```
