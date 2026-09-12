# L'armonia parallela (planing cromatico) — piano

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`).

**Goal:** scrivere l'istruzione sul planing cromatico (armonia parallela) — una forma d'accordo che scivola in parallelo, senza funzione — e provarla su un pezzo da zero: un'onda cromatica di dom7 paralleli, sul Deluge.

**Architecture:** stessa forma delle istruzioni. Il cromatismo NON è una scala ma una condotta; si aggiunge però `'cromatica'` (le 12 note) a `song.MODI` per la `set_scale`. Il pezzo in `tools/planing_scritto.py`. Il punto tecnico: `MU.armonia(..., condotta=False)`.

## Global Constraints

- **Fonte: Piston**, cap. 31 «Parallel and Antiparallel Harmony» (pagina da pinnare scrivendo).
- Gradi `[LIB]`/`[CALC]`/`[DEC]`/`[OSS]`; niente sorteggio; file a LF; commit `area: descrizione` senza accenti + trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **dsysex `put` da PowerShell**.
- ⚠️ **`condotta=False`** è il planing: la condotta di default romperebbe il parallelo. Movimento **per semitono**. Non risolvere.

---

### Task 1: `'cromatica'` in `song.MODI` + il test `[CALC]`

**Files:** Modify `tools/delugexml/song.py`; Modify `tests/test_all.py`.

- [ ] **Step 1:** aggiungere a `MODI`, dopo `'esatonale'`:

```python
    # la cromatica: tutte e 12 le note. Non e' un campo armonico con un centro
    # ma "nessuna tonalita'": serve a set_scale per il planing (movimento per
    # semitoni). Il cromatismo e' una condotta, non una scala.
    'cromatica':     (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
```

- [ ] **Step 2: il test** (accanto a `test_scala_esatonale`):

```python
def test_planing_cromatico():
    """Le affermazioni [CALC] di docs/istruzioni/armonia-parallela.md.

    Il planing e' una forma rigida che scivola in parallelo: il dom7 spostato
    di N semitoni e' voci() della base + N. E la cromatica ha 12 note.
    """
    from delugexml import musica as MU, song as S              # noqa: PLC0415
    check("la cromatica ha 12 note",
          len(S.MODI['cromatica']) == 12, str(len(S.MODI['cromatica'])))
    base = sorted(MU.voci('C7', registro='do3'))
    for sem, sigla in enumerate(['C7', 'Db7', 'D7', 'Eb7', 'E7']):
        got = sorted(MU.voci(sigla, registro='do3'))
        check(f'{sigla} = C7 + {sem} semitoni (forma parallela rigida)',
              got == [y + sem for y in base], str(got))
```

- [ ] **Step 3:** lanciare `test_planing_cromatico` (PASS), poi la suite intera.
- [ ] **Step 4:** commit `scala: la cromatica entra in MODI, e il guardiano [CALC] del planing`.

---

### Task 2: L'istruzione `armonia-parallela.md`

**Files:** Create `docs/istruzioni/armonia-parallela.md`.

- [ ] **Step 1: pinnare la pagina di Piston** — cercare «Parallel and Antiparallel Harmony» nel PDF (cap. 31, dopo la whole-tone p. 490).
- [ ] **Step 2: scrivere** nella forma delle istruzioni: **A cosa serve** → **grado di prova** → **principio** (la forma scivola, la funzione sparisce; tutte le voci si muovono dello stesso intervallo, l'opposto della condotta; `[LIB]` Piston cap. 31; il legame con ottatonica/esatonale, linkate) → **il punto tecnico** (`condotta=False`, verificato; movimento per semitono) → **vocabolario** (dom7, triadi, quartali da far scivolare; cromatico vs diatonico) → **come si stabilisce** (scegli una forma, falla scivolare, non risolvere) → **come si scrive** (`S.set_scale(doc, 'C', 'cromatica')` + `MU.armonia(..., condotta=False)`) → **esempio lavorato** (da riempire al Task 5) → **cosa manca** (diatonic planing, medianti cromatiche, accordi di passaggio).
- [ ] **Step 3:** LF check + suite + commit `istruzioni: l'armonia parallela, il planing cromatico (Piston cap. 31)`.

---

### Task 3: Il pezzo di prova `planing_scritto.py`

**Files:** Create `tools/planing_scritto.py`; Modify `tests/test_all.py`.

- [ ] **Step 1: il test (fallisce: modulo assente)**

```python
def test_planing_scritto():
    """Il pezzo di planing sta in piedi: i dom7 scivolano in parallelo per
    semitono, e la melodia e' una linea cromatica."""
    import planing_scritto as PL                               # noqa: PLC0415
    from delugexml import musica as MU                         # noqa: PLC0415

    accordi = [a.strip() for a in PL.PROGRESSIONE.split('|')]
    check('il giro ha 8 battute', len(accordi) == 8, str(len(accordi)))
    check('parte col planing C7-Db7-D7',
          accordi[:3] == ['C7', 'Db7', 'D7'], str(accordi[:3]))
    # i primi quattro passi salgono in parallelo di 1 semitono
    for i in range(4):
        a = sorted(MU.voci(accordi[i], registro='do3'))
        b = sorted(MU.voci(accordi[i + 1], registro='do3'))
        check(f'{accordi[i]}->{accordi[i + 1]}: scivola di +1 (parallelo)',
              b == [y + 1 for y in a], f'{a} -> {b}')
    # la melodia e' una linea cromatica (passi di 1 semitono)
    ys = [MU.altezza(n) for n in PL.MELODIA.split()]
    check('la melodia e cromatica (passi di 1 semitono)',
          all(abs(x - y) == 1 for x, y in zip(ys, ys[1:])), str(ys))
```

- [ ] **Step 2:** lanciare, verificare che fallisce.
- [ ] **Step 3: scrivere lo script**

```python
"""Il pezzo di prova del planing cromatico, COMPOSTO seguendo
docs/istruzioni/armonia-parallela.md.

Un'onda cromatica di dom7 paralleli -- la stessa forma che scivola per semitoni,
senza funzione. La tromba cavalca la voce in cima (la settima), una linea
cromatica. condotta=False: la forma resta rigida. Nessun sorteggio.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: 8 battute: il dom7 sale di cinque semitoni e ridiscende. Non risolve:
#: e' uno stream parallelo.
PROGRESSIONE = 'C7 | Db7 | D7 | Eb7 | E7 | Eb7 | D7 | Db7'

#: La melodia cavalca la settima di ogni dom7 -- una linea cromatica pura
#: (sib-si-do-reb-re-reb-do-si).
MELODIA = 'sib4 si4 do5 reb5 re5 reb5 do5 si4'

#: Il basso sulle fondamentali (anch'esse cromatiche).
BASSO = 'do2 reb2 re2 mib2 mi2 mib2 re2 reb2'


def comping():
    """Gli accordi, voicing per terze, SENZA condotta: la forma resta rigida e
    parallela (con la condotta si romperebbe il planing)."""
    return MU.armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                      durata='1/1', condotta=False)


def tema():
    """La linea cromatica in cima."""
    return MU.melodia(MELODIA, durata='1/1')


def basso():
    """Il basso sulle fondamentali."""
    return MU.melodia(BASSO, durata='1/1')


if __name__ == '__main__':
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                              condotta=False))
```

- [ ] **Step 4:** lanciare il test (passa) + la suite intera.
- [ ] **Step 5:** commit `planing: il pezzo di prova, l'onda cromatica di dom7 paralleli`.

---

### Task 4: Assemblaggio + caricamento + ascolto (interattivo)

⚠️ Deluge collegato (ping prima). `S.set_scale(doc, 'C', 'cromatica')`, tre tracce (Rhodes/Trumpet/SawBass) `playing=True`, `length=8*384`; `MU.scrivi` con `PL.comping()/tema()/basso()`; `verifica` vuota; `racconta`; `write_file` in scratchpad; `put` di **`PLANING01`** (`MU.destinazione('planing', 1)`) da **PowerShell**.

- [ ] L'utente apre `PLANING01`, ascolta lo scivolamento parallelo, dà il verdetto.

---

### Task 5: L'esempio lavorato

**Files:** Modify `docs/istruzioni/armonia-parallela.md`.

- [ ] Aggiungere l'esempio lavorato (l'onda di dom7 paralleli, la linea cromatica, `condotta=False`) col **verdetto** `[OSS]`. Se il verdetto chiede modifiche, cambiarle e ripetere il Task 4.
- [ ] LF + commit `planing: l'esempio lavorato, col verdetto sullo scivolamento parallelo`.
