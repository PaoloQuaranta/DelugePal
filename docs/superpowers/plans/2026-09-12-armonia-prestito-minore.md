# Prestito modale, casa minore — piano d'implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** estendere `docs/istruzioni/armonia-prestito.md` con la direzione inversa — una casa **minore** che prende in prestito dal **maggiore** parallelo, col **IV maggiore** (la schiaritura dorica) come colore — e provarla su un pezzo in La minore costruito da zero, caricato sul Deluge.

**Architecture:** è l'estensione simmetrica del lavoro del 12 settembre (il pezzo in Do col iv minore). Stessa forma: un test di guardia `[CALC]`, una sezione nuova nell'istruzione, un secondo pezzo composto dentro `tools/prestito_scritto.py`, assemblaggio + SysEx a mano.

**Tech Stack:** Python 3 + `tools/delugexml`, il runner custom in `tests/test_all.py`, `tools/dsysex.py` (da **PowerShell**, non Git Bash — i path remoti si storpiano).

## Global Constraints

- **Fonte:** Smith, *Jazz Theory* (4ª ed.), cap. IX, p. 74 (il ♮6/♮7 in minore «presi in prestito dal maggiore parallelo»); Piston per la terza di Piccardia.
- **Gradi di prova** `[LIB]`/`[CALC]`/`[DEC]`/`[OSS]`; niente sorteggio; voicing per terze.
- ⚠️ **Il V maggiore (E7) NON è un prestito**: è la normale dominante del minore armonico. Dirlo esplicitamente.
- **File a LF**; commit `area: descrizione` senza accenti, con trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **dsysex `put` da PowerShell** (vedi memoria `dsysex-da-powershell`): da Git Bash `/SONGS/...` diventa `C:/Program Files/Git/SONGS/...` e l'open fallisce.
- Test: `.venv/Scripts/python.exe tests/test_all.py` (gira tutto); un test solo: `... -c "import sys; sys.path.insert(0,'tests'); sys.path.insert(0,'tools'); import test_all; test_all.<nome>()"`.

---

### Task 1: Il test di guardia `[CALC]` della casa minore

**Files:** Modify `tests/test_all.py` (accanto a `test_armonia_prestito_accordi_dal_parallelo`).

- [ ] **Step 1: Scrivere il test**

```python
def test_armonia_prestito_casa_minore():
    """Le affermazioni [CALC] della sezione 'casa minore' di armonia-prestito.md.

    In una casa minore i prestiti vengono dal maggiore parallelo: le note di
    colore -- 3, 6, 7 alzate -- sono quelle che il maggiore ha e il minore no.
    """
    from delugexml import musica as MU, song as S              # noqa: PLC0415
    mag, minn = set(S.MODI['maggiore']), set(S.MODI['minore'])

    check('il maggiore parallelo alza 3, 6, 7',
          mag - minn == {4, 9, 11}, str(sorted(mag - minn)))

    # casa La minore: tonica La (classe 9), note di colore relative alla tonica
    TON = 9
    prestiti = {'D': 9, 'Bm': 9, 'A': 4}  # IV magg (nat6), ii min (nat6), I magg/Piccardia (nat3)
    for testo, colore in prestiti.items():
        rel = {(y - TON) % 12 for y in MU.voci(testo)}
        check(f'{testo}: porta la nota di colore {colore} (rel. alla tonica)',
              colore in rel, str(sorted(rel)))
        check(f'{testo}: quella nota viene dal maggiore',
              colore in (mag - minn), f'{colore} in {sorted(mag - minn)}')
```

- [ ] **Step 2: Lanciare il test**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); sys.path.insert(0,'tools'); import test_all; test_all.test_armonia_prestito_casa_minore()"`
Expected: tutte `PASS`.

- [ ] **Step 3: Commit**

```bash
git add tests/test_all.py
git commit -m "test: il guardiano [CALC] del prestito in casa minore" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: La sezione «casa minore» nell'istruzione

**Files:** Modify `docs/istruzioni/armonia-prestito.md`.

- [ ] **Step 1: Aggiungere la sezione**

Dopo «Il vocabolario» (o come sua sottosezione «La direzione inversa: una casa minore»), con la tabella:

| prestito | in La minore | nota di colore | fonte |
|---|---|---|---|
| **IV maggiore** | Re (D F# A) | fa# (♮6) | `[LIB]` Smith p. 74 — la schiaritura dorica |
| **ii minore** | Bm (B D F#) | fa# (♮6) | `[CALC]` dal maggiore |
| **I maggiore (Piccardia)** | La (A C# E) | do# (♮3) | `[LIB]` Piston, cap. 26 e dintorni |

`[LIB]` Smith p. 74: in minore i gradi 6 e 7 si possono alzare, e i gradi alzati sono *«presi in prestito dal maggiore parallelo»*. ⚠️ Dire che il **V maggiore (E7) NON è un prestito**: è la normale dominante del minore armonico (il sol# è la sensibile, non un colore preso a prestito). Il test `[CALC]` di copertura è `test_armonia_prestito_casa_minore`.

- [ ] **Step 2: Aggiornare «Cosa manca»**

Il punto «la direzione inversa» non è più mancante (questa sezione la copre). La terza di Piccardia e il ♮6/♮7 jazz restano nominati ma non provati a fondo.

- [ ] **Step 3: LF + lanciare la suite + commit**

Run: `git add docs/istruzioni/armonia-prestito.md && git diff --cached --stat && git diff --cached --stat --ignore-cr-at-eol` (devono coincidere).
Run: `.venv/Scripts/python.exe tests/test_all.py` → stesso numero di fallimenti di prima.

```bash
git commit -m "istruzioni: il prestito in casa minore, il IV maggiore (Smith p. 74)" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Il secondo pezzo (La minore) in `prestito_scritto.py`

**Files:** Modify `tools/prestito_scritto.py`; Modify `tests/test_all.py`.

- [ ] **Step 1: Scrivere il test (fallisce: le costanti non esistono)**

```python
def test_prestito_scritto_minore():
    """Il pezzo in minore sta in piedi: iv->IV (Dm->D) alla battuta 4, la
    melodia che alza il fa al fa# sopra."""
    import prestito_scritto as PR                              # noqa: PLC0415
    from delugexml import musica as MU                         # noqa: PLC0415

    accordi = [a.strip() for a in PR.PROGRESSIONE_MIN.split('|')]
    check('il giro minore ha 8 battute', len(accordi) == 8, str(len(accordi)))
    check('il IV maggiore (D) e alla battuta 4', accordi[3] == 'D', accordi[3])
    check('il giro torna a casa su Am', accordi[-1] == 'Am', accordi[-1])

    per_battuta: dict[int, set[int]] = {}
    for y, note in MU.melodia(PR.MELODIA_MIN, durata='1/1').items():
        for n in note:
            per_battuta.setdefault(n.pos // 384, set()).add(y % 12)
    check('battuta 3 (Dm): la melodia ha il fa naturale (5)',
          5 in per_battuta.get(2, set()), str(sorted(per_battuta.get(2, set()))))
    check('battuta 4 (D): la melodia ha il fa# (6)',
          6 in per_battuta.get(3, set()), str(sorted(per_battuta.get(3, set()))))
```

- [ ] **Step 2: Lanciare, verificare che fallisce** (`AttributeError: module ... has no attribute 'PROGRESSIONE_MIN'`).

- [ ] **Step 3: Estendere lo script**

In coda a `tools/prestito_scritto.py`:

```python
# --- il secondo pezzo: casa MINORE, il IV maggiore preso dal maggiore parallelo
#
#   battuta  accordo  grado  melodia  perche'
#   1        Am       i       mi4     la casa minore
#   2        Em       v       sol4    diatonico
#   3        Dm       iv       fa4     il iv, col fa NATURALE (b6)
#   4        D        IV      fa#4    il PRESTITO: il fa sale al fa# (nat6), la schiaritura
#   5        Am       i       mi4     si rientra
#   6        Dm       iv       fa4     di nuovo il iv
#   7        E7       V7      mi4     la dominante (il sol# e' la sensibile, NON un prestito)
#   8        Am       i       la4     a casa
#
#: Il cuore e' il iv->IV delle battute 3-4: Dm -> D maggiore, il fa che sale al
#: fa#. Simmetrico al IV->iv (la -> la bemolle) del pezzo in Do.
PROGRESSIONE_MIN = 'Am | Em | Dm | D | Am | Dm | E7 | Am'
MELODIA_MIN = 'mi4 sol4 fa4 fa#4 mi4 fa4 mi4 la4'
BASSO_MIN = 'la2 mi2 re2 re2 la2 re2 mi2 la2'


def comping_min():
    """Gli accordi del pezzo in minore, voicing per terze."""
    return MU.armonia(PROGRESSIONE_MIN, voicing='chiuso', registro='la2',
                      durata='1/1')


def tema_min():
    """La melodia del pezzo in minore."""
    return MU.melodia(MELODIA_MIN, durata='1/1')


def basso_min():
    """Il basso del pezzo in minore."""
    return MU.melodia(BASSO_MIN, durata='1/1')
```

- [ ] **Step 4: Lanciare il test (passa), poi la suite intera (niente regressioni).**

- [ ] **Step 5: Commit**

```bash
git add tools/prestito_scritto.py tests/test_all.py
git commit -m "prestito: il secondo pezzo, La minore col IV maggiore alla battuta 4" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Assemblaggio + caricamento + ascolto (interattivo)

⚠️ Interattivo, serve il Deluge collegato. Come il pezzo in Do, ma con `set_scale(doc, 'A', 'minore')` e le costanti `*_MIN`.

- [ ] **Step 1: Costruire la song** — template `refs/songs/TEMPL0.XML`, via il track di default, tre tracce (Tal Rhodes / 062 Trumpet / Square Saw Bass) `playing=True`, `length=8*384`; `S.set_scale(doc, 'A', 'minore')`; `MU.scrivi` con `PR.comping_min()/tema_min()/basso_min()`.
- [ ] **Step 2: `MU.verifica(doc)` vuota; `MU.avvertenze`; `MU.racconta`; `write_file` in scratchpad.**
- [ ] **Step 3: Caricare da PowerShell** — `dsysex ... put <scratch> "/SONGS/DelugePal/PRESTITO02.XML"` (versione 2, `MU.destinazione('prestito', 2)`).
- [ ] **Step 4: L'utente apre `PRESTITO02`, ascolta il iv→IV (battuta 3-4), dà il verdetto.**

---

### Task 5: Il secondo esempio lavorato

**Files:** Modify `docs/istruzioni/armonia-prestito.md`.

- [ ] **Step 1:** aggiungere, sotto l'esempio in Do, il secondo esempio lavorato (La minore, il iv→IV, il fa→fa# in cima) col **verdetto dell'utente** `[OSS]`. Se il verdetto chiede modifiche, cambiarle in `prestito_scritto.py` e ripetere il Task 4.
- [ ] **Step 2: LF + commit.**
