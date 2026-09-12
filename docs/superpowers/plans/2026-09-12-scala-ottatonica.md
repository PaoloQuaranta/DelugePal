# La scala ottatonica — piano d'implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`).

**Goal:** scrivere la prima istruzione su una scala non diatonica — l'**ottatonica** (la diminuita), un colore simmetrico fuori dal tonale — e provarla su un pezzo costruito da zero: il ciclo di dom7 a terza minore, caricato sul Deluge.

**Architecture:** stessa forma delle istruzioni armoniche (principio → vocabolario → come si scrive → esempio), più un test `[CALC]`. L'ottatonica diventa una scala nominata in `song.MODI`; il pezzo sta in un nuovo `tools/ottatonica_scritto.py`.

**Tech Stack:** Python 3 + `tools/delugexml`, runner in `tests/test_all.py`, `dsysex.py` (da **PowerShell**).

## Global Constraints

- **Fonte:** Smith, *Jazz Theory* (4ª ed.), cap. IX, p. 75-77 («The "Diminished" Scale»); Piston cap. 31 (scale artificiali) come secondaria, pagina da pinnare.
- Gradi `[LIB]`/`[CALC]`/`[DEC]`/`[OSS]`; niente sorteggio; voicing per terze; file a LF; commit `area: descrizione` senza accenti + trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **dsysex `put` da PowerShell** (memoria `dsysex-da-powershell`).
- L'ottatonica è **simmetrica per terza minore**, 8 note, solo 3 forme distinte. Non risolverla tonalmente (colore, non funzione).
- Test: `.venv/Scripts/python.exe tests/test_all.py`; uno solo via `-c "...; import test_all; test_all.<nome>()"`.

---

### Task 1: L'ottatonica in `song.MODI` + il test `[CALC]`

**Files:** Modify `tools/delugexml/song.py` (dict `MODI`); Modify `tests/test_all.py`.

- [ ] **Step 1:** aggiungere a `MODI`, dopo `'minore melodica'`:

```python
    # l'ottatonica (diminuita): semitono-tono (HW), la forma per i dom7b9; la
    # tono-semitono (WH) e' la stessa scala su un'altra nota. Smith p. 75-77
    'ottatonica':    (0, 1, 3, 4, 6, 7, 9, 10),
```

- [ ] **Step 2: il test** (accanto agli altri test di scala/armonia):

```python
def test_scala_ottatonica():
    """Le affermazioni [CALC] di docs/istruzioni/scala-ottatonica.md.

    L'ottatonica e' simmetrica per terza minore, e i quattro dom7 a terza
    minore stanno tutti dentro la stessa scala.
    """
    from delugexml import musica as MU, song as S              # noqa: PLC0415
    ott = set(S.MODI['ottatonica'])

    check("l'ottatonica ha 8 note", len(S.MODI['ottatonica']) == 8, str(len(ott)))
    check("l'ottatonica e simmetrica per terza minore (+3 semitoni)",
          {(p + 3) % 12 for p in ott} == ott,
          str(sorted({(p + 3) % 12 for p in ott})))
    # i quattro dom7 a terza minore, tutti dentro l'ottatonica di Do (tonica 0)
    for sigla in ('C7', 'Eb7', 'Gb7', 'A7'):
        note = {y % 12 for y in MU.voci(sigla)}
        check(f'{sigla} sta dentro l\'ottatonica di Do',
              note <= ott, str(sorted(note - ott)))
```

- [ ] **Step 3:** lanciare `test_scala_ottatonica` (tutte `PASS`), poi la suite intera. ⚠️ Se un test contava le voci di `MODI`, aggiornarlo: l'ottatonica è un'aggiunta legittima.
- [ ] **Step 4:** commit `scala: l'ottatonica entra in MODI, col suo guardiano [CALC]`.

---

### Task 2: L'istruzione `scala-ottatonica.md`

**Files:** Create `docs/istruzioni/scala-ottatonica.md`.

- [ ] **Step 1: leggere la fonte** — Smith p. 75-77 (già letto in parte); pinnare la pagina di Piston cap. 31 sulle scale simmetriche (cercare «octatonic»/«whole-tone»/«symmetric» nel PDF).
- [ ] **Step 2: scrivere** nella forma delle istruzioni: **A cosa serve** → **grado di prova** → **principio** (colore simmetrico, non funzione; il contrasto/parallelo con `armonia-modale.md`, linkato) → **cos'è** (8 note, WH/HW, 3 forme, simmetrica per terza minore, `[LIB]` Smith p. 75-77) → **vocabolario** (dim7, dom7♭9, il ciclo dei quattro dom7 a terza minore `C7 Eb7 Gb7 A7`; `[CALC]` il test) → **come si stabilisce** (il ciclo per terza minore, senza risolvere) → **come si scrive** (`S.set_scale(doc, 'C', 'ottatonica')` + `MU.armonia`) → **esempio lavorato** (da riempire al Task 5) → **cosa manca** (esatonale, cromatismo, l'uso funzionale sopra una dominante).
- [ ] **Step 3:** LF check + suite (stesso numero di fallimenti) + commit `istruzioni: la scala ottatonica, colore simmetrico fuori dal tonale`.

---

### Task 3: Il pezzo di prova `ottatonica_scritto.py`

**Files:** Create `tools/ottatonica_scritto.py`; Modify `tests/test_all.py`.

- [ ] **Step 1: il test (fallisce: modulo assente)**

```python
def test_ottatonica_scritto():
    """Il pezzo ottatonico sta in piedi: il ciclo di dom7 a terza minore, e
    la melodia tutta dentro l'ottatonica."""
    import ottatonica_scritto as OT                            # noqa: PLC0415
    from delugexml import musica as MU, song as S              # noqa: PLC0415

    accordi = [a.strip() for a in OT.PROGRESSIONE.split('|')]
    check('il giro ha 8 battute', len(accordi) == 8, str(len(accordi)))
    check('il ciclo e C7-Eb7-Gb7-A7',
          accordi[:4] == ['C7', 'Eb7', 'Gb7', 'A7'], str(accordi[:4]))

    ott = set(S.MODI['ottatonica'])
    classi = {MU.altezza(n) % 12 for n in OT.MELODIA.split()}
    check('la melodia sta tutta dentro l\'ottatonica',
          classi <= ott, str(sorted(classi - ott)))
```

- [ ] **Step 2:** lanciare, verificare che fallisce (`ModuleNotFoundError`).
- [ ] **Step 3: scrivere lo script**

```python
"""Il pezzo di prova della scala ottatonica, COMPOSTO seguendo
docs/istruzioni/scala-ottatonica.md.

Il ciclo dei quattro dom7 a terza minore -- C7 Eb7 Gb7 A7 -- tutti dentro una
sola ottatonica, con una linea ottatonica discendente in cima. Il suono
sospeso e simmetrico della scala: non risolve, shimmera. Nessun sorteggio.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: 8 battute: il ciclo per terza minore, due rotazioni. Non risolve: e' il
#: punto. Tutti e quattro i dom7 stanno nell'ottatonica HW di Do.
PROGRESSIONE = 'C7 | Eb7 | Gb7 | A7 | C7 | Eb7 | Gb7 | A7'

#: La linea ottatonica discendente, una nota per battuta (do-sib-la-sol-solb-
#: mi-mib-reb): fa sentire la scala per intero, in cima.
MELODIA = 'do5 sib4 la4 sol4 solb4 mi4 mib4 reb4'

#: Il basso sulle fondamentali del ciclo (do-mib-solb-la, per terze minori).
BASSO = 'do2 mib2 solb2 la2 do2 mib2 solb2 la2'


def comping():
    """Gli accordi del ciclo, voicing per terze (la simmetria da' note comuni)."""
    return MU.armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                      durata='1/1')


def tema():
    """La linea ottatonica discendente."""
    return MU.melodia(MELODIA, durata='1/1')


def basso():
    """Il basso sulle fondamentali."""
    return MU.melodia(BASSO, durata='1/1')


if __name__ == '__main__':
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3'))
```

- [ ] **Step 4:** lanciare il test (passa) + la suite intera (niente regressioni).
- [ ] **Step 5:** commit `ottatonica: il pezzo di prova, il ciclo di dom7 a terza minore`.

---

### Task 4: Assemblaggio + caricamento + ascolto (interattivo)

⚠️ Serve il Deluge collegato (ping prima). `S.set_scale(doc, 'C', 'ottatonica')`, tre tracce (Rhodes/Trumpet/SawBass) `playing=True`, `length=8*384`; `MU.scrivi` con `OT.comping()/tema()/basso()`; `verifica` vuota; `racconta`; `write_file` in scratchpad; `put` di **`OTTATON01`** (`MU.destinazione('ottaton', 1)`) da **PowerShell**.

- [ ] L'utente apre `OTTATON01`, ascolta il ciclo simmetrico e la linea ottatonica, dà il verdetto.

---

### Task 5: L'esempio lavorato

**Files:** Modify `docs/istruzioni/scala-ottatonica.md`.

- [ ] Aggiungere l'esempio lavorato (il ciclo, la linea discendente, il colore simmetrico) col **verdetto** `[OSS]`. Se il verdetto chiede modifiche, cambiarle e ripetere il Task 4.
- [ ] LF + commit `ottatonica: l'esempio lavorato, col verdetto sul ciclo simmetrico`.
