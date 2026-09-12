# La scala esatonale (whole-tone) — piano

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`).

**Goal:** scrivere l'istruzione sull'esatonale (whole-tone) — colore simmetrico che galleggia — e provarla su un pezzo da zero: il ciclo di dom7♯5 che sale per tono, sul Deluge.

**Architecture:** gemella dell'ottatonica. L'esatonale entra in `song.MODI`; il pezzo in `tools/esatonale_scritto.py`.

## Global Constraints

- **Fonte: Piston** (NON Smith), cap. 31 p. 490 (la scala) e cap. 28 p. 439 (le triadi aumentate che perdono la tonalità).
- Gradi `[LIB]`/`[CALC]`/`[DEC]`/`[OSS]`; niente sorteggio; voicing per terze; file a LF; commit `area: descrizione` senza accenti + trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **dsysex `put` da PowerShell**.
- L'esatonale è simmetrica per **tono**, 6 note, 2 forme distinte; solo triadi aumentate (niente quinta giusta). Non risolverla.

---

### Task 1: L'esatonale in `song.MODI` + il test `[CALC]`

**Files:** Modify `tools/delugexml/song.py`; Modify `tests/test_all.py`.

- [ ] **Step 1:** aggiungere a `MODI`, dopo `'ottatonica'`:

```python
    # l'esatonale (whole-tone): tutti toni, nessuna quinta giusta -> solo
    # triadi aumentate; simmetrica per tono, 2 forme distinte. Piston cap. 31 p. 490
    'esatonale':     (0, 2, 4, 6, 8, 10),
```

- [ ] **Step 2: il test** (accanto a `test_scala_ottatonica`):

```python
def test_scala_esatonale():
    """Le affermazioni [CALC] di docs/istruzioni/scala-esatonale.md.

    L'esatonale e' simmetrica per tono, e i dom7#5 del ciclo stanno tutti
    dentro la stessa scala.
    """
    from delugexml import musica as MU, song as S              # noqa: PLC0415
    wt = set(S.MODI['esatonale'])

    check("l'esatonale ha 6 note", len(S.MODI['esatonale']) == 6, str(len(wt)))
    check("l'esatonale e simmetrica per tono (+2 semitoni)",
          {(p + 2) % 12 for p in wt} == wt,
          str(sorted({(p + 2) % 12 for p in wt})))
    check("ci sono 2 esatonali distinte (trasposta di 1 semitono e' l'altra)",
          {(p + 1) % 12 for p in wt} != wt, 'identica a se stessa?!')
    # i dom7#5 del ciclo, tutti dentro l'esatonale di Do
    for sigla in ('C7#5', 'D7#5', 'E7#5', 'F#7#5'):
        note = {y % 12 for y in MU.voci(sigla)}
        check(f'{sigla} sta dentro l\'esatonale di Do',
              note <= wt, str(sorted(note - wt)))
```

- [ ] **Step 3:** lanciare `test_scala_esatonale` (PASS), poi la suite intera.
- [ ] **Step 4:** commit `scala: l'esatonale entra in MODI, col suo guardiano [CALC]`.

---

### Task 2: L'istruzione `scala-esatonale.md`

**Files:** Create `docs/istruzioni/scala-esatonale.md`.

- [ ] **Step 1: scrivere** nella forma delle istruzioni (come `scala-ottatonica.md`): **A cosa serve** → **grado di prova** → **principio** (colore simmetrico, niente quinta giusta → solo aumentate; il parallelo con ottatonica e modale, linkati; `[LIB]` Piston cap. 31 p. 490 e cap. 28 p. 439) → **cos'è** (6 note, 2 forme, simmetrica per tono) → **vocabolario** (le 2 triadi aumentate, i dom7♯5/♭5, il ciclo per tono; `[CALC]` il test) → **come si stabilisce** (dom7♯5 paralleli per tono, senza risolvere) → **come si scrive** (`S.set_scale(doc, 'C', 'esatonale')` + `MU.armonia`) → **esempio lavorato** (da riempire al Task 5) → **cosa manca** (cromatismo, uso funzionale).
- [ ] **Step 2:** LF check + suite + commit `istruzioni: la scala esatonale, il colore che galleggia (Piston)`.

---

### Task 3: Il pezzo di prova `esatonale_scritto.py`

**Files:** Create `tools/esatonale_scritto.py`; Modify `tests/test_all.py`.

- [ ] **Step 1: il test (fallisce: modulo assente)**

```python
def test_esatonale_scritto():
    """Il pezzo esatonale sta in piedi: il ciclo di dom7#5 che sale per tono,
    e la melodia tutta dentro l'esatonale."""
    import esatonale_scritto as ES                             # noqa: PLC0415
    from delugexml import musica as MU, song as S              # noqa: PLC0415

    accordi = [a.strip() for a in ES.PROGRESSIONE.split('|')]
    check('il giro ha 8 battute', len(accordi) == 8, str(len(accordi)))
    check('il ciclo parte C7#5-D7#5-E7#5',
          accordi[:3] == ['C7#5', 'D7#5', 'E7#5'], str(accordi[:3]))

    wt = set(S.MODI['esatonale'])
    classi = {MU.altezza(n) % 12 for n in ES.MELODIA.split()}
    check("la melodia sta tutta dentro l'esatonale",
          classi <= wt, str(sorted(classi - wt)))
```

- [ ] **Step 2:** lanciare, verificare che fallisce.
- [ ] **Step 3: scrivere lo script**

```python
"""Il pezzo di prova della scala esatonale, COMPOSTO seguendo
docs/istruzioni/scala-esatonale.md.

Il ciclo dei dom7#5 che salgono per tono -- C7#5 D7#5 E7#5 ... -- tutti dentro
una sola esatonale, con una melodia ondeggiante whole-tone in cima. Il suono
sospeso, acquatico, di Debussy: non risolve, galleggia. Nessun sorteggio.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: 8 battute: i dom7#5 salgono per tono, i sei distinti piu' il ritorno. Non
#: risolve: galleggia. Tutti dentro l'esatonale di Do.
PROGRESSIONE = 'C7#5 | D7#5 | E7#5 | F#7#5 | G#7#5 | A#7#5 | C7#5 | D7#5'

#: La melodia ondeggiante, whole-tone, una nota per battuta.
MELODIA = 'sol#4 la#4 do5 re5 mi5 re5 do5 la#4'

#: Il basso sulle fondamentali del ciclo (do-re-mi-fa#-sol#-la#, per toni).
BASSO = 'do2 re2 mi2 fa#2 sol#2 la#2 do2 re2'


def comping():
    """Gli accordi del ciclo, voicing per terze."""
    return MU.armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                      durata='1/1')


def tema():
    """La melodia ondeggiante whole-tone."""
    return MU.melodia(MELODIA, durata='1/1')


def basso():
    """Il basso sulle fondamentali."""
    return MU.melodia(BASSO, durata='1/1')


if __name__ == '__main__':
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3'))
```

- [ ] **Step 4:** lanciare il test (passa) + la suite intera.
- [ ] **Step 5:** commit `esatonale: il pezzo di prova, il ciclo di dom7#5 per tono`.

---

### Task 4: Assemblaggio + caricamento + ascolto (interattivo)

⚠️ Deluge collegato (ping prima). `S.set_scale(doc, 'C', 'esatonale')`, tre tracce (Rhodes/Trumpet/SawBass) `playing=True`, `length=8*384`; `MU.scrivi` con `ES.comping()/tema()/basso()`; `verifica` vuota; `racconta`; `write_file` in scratchpad; `put` di **`ESATON01`** (`MU.destinazione('esaton', 1)`) da **PowerShell**.

- [ ] L'utente apre `ESATON01`, ascolta il galleggiamento whole-tone, dà il verdetto.

---

### Task 5: L'esempio lavorato

**Files:** Modify `docs/istruzioni/scala-esatonale.md`.

- [ ] Aggiungere l'esempio lavorato (il ciclo per tono, la melodia ondeggiante, il colore sospeso) col **verdetto** `[OSS]`. Se il verdetto chiede modifiche, cambiarle e ripetere il Task 4.
- [ ] LF + commit `esatonale: l'esempio lavorato, col verdetto sul galleggiamento`.
