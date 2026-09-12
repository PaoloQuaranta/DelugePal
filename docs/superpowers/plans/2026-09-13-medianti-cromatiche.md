# Le medianti cromatiche — piano

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`).

**Goal:** scrivere l'istruzione sulle medianti cromatiche — accordi a terza con una nota in comune, il colore cinematografico — e provarla su un pezzo da zero: Do che oscilla con le sue medianti e torna a casa, sul Deluge.

**Architecture:** stessa forma delle istruzioni. NON una scala (niente `MODI`): la casa è Do maggiore, le medianti sono colore cromatico. Il pezzo in `tools/medianti_scritto.py`. Punto tecnico: `condotta=True` (la nota comune tenuta).

## Global Constraints

- **Fonte:** il rigore è nel `[CALC]` (il fatto della nota comune, testato); Piston cap. 28 fa da contesto. Il termine «mediante cromatica» non è nei libri in casa — dichiararlo, non spacciare una citazione.
- Gradi `[LIB]`/`[CALC]`/`[DEC]`/`[OSS]`; niente sorteggio; file a LF; commit `area: descrizione` senza accenti + trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **dsysex `put` da PowerShell**.
- ⚠️ `condotta=True` (il default) — la nota comune tiene. Non risolvere per dominante.

---

### Task 1: Il test `[CALC]`

**Files:** Modify `tests/test_all.py` (accanto a `test_planing_cromatico`).

- [ ] **Step 1:**

```python
def test_medianti_cromatiche():
    """Le affermazioni [CALC] di docs/istruzioni/medianti-cromatiche.md.

    Una mediante cromatica condivide UNA sola nota con la casa; una mediante
    diatonica ne condivide due.
    """
    from delugexml import musica as MU                         # noqa: PLC0415
    do = {y % 12 for y in MU.voci('C')}
    for sigla in ('Ab', 'E', 'Eb', 'A'):
        m = {y % 12 for y in MU.voci(sigla)}
        check(f'Do e {sigla}: una sola nota in comune (mediante cromatica)',
              len(do & m) == 1, str(sorted(do & m)))
    em = {y % 12 for y in MU.voci('Em')}
    check('Do e Em (mediante diatonica): due note in comune',
          len(do & em) == 2, str(sorted(do & em)))
```

- [ ] **Step 2:** lanciare il test (PASS), poi la suite intera.
- [ ] **Step 3:** commit `test: il guardiano [CALC] delle medianti cromatiche`.

---

### Task 2: L'istruzione `medianti-cromatiche.md`

**Files:** Create `docs/istruzioni/medianti-cromatiche.md`.

- [ ] **Step 1: scrivere** nella forma delle istruzioni: **A cosa serve** → **grado di prova** → **principio** (a terza, una nota in comune vs due della diatonica; la nota comune = morbidezza, lo scarto = sorpresa; ⚠️ la nota sulla fonte: `[CALC]` core + Piston cap. 28 contesto, il termine non è nei libri — dichiararlo; link a armonia-prestito e ai colori cromatici) → **il punto tecnico** (`condotta=True`, la nota comune tiene — opposto del planing) → **vocabolario** (le 4 medianti di Do: Ab, E a terza maggiore; Eb, A a terza minore; il ciclo esatonico Do→Ab→Mi→Do) → **come si stabilisce** (vai a una mediante tenendo la nota comune, torna; non risolvere per dominante) → **come si scrive** (`S.set_scale(doc, 'C', 'maggiore')` + `MU.armonia`, condotta di default) → **esempio lavorato** (da riempire al Task 5) → **cosa manca** (diatonic planing, accordi di passaggio/approccio).
- [ ] **Step 2:** LF check + suite + commit `istruzioni: le medianti cromatiche, il colore cinematografico`.

---

### Task 3: Il pezzo di prova `medianti_scritto.py`

**Files:** Create `tools/medianti_scritto.py`; Modify `tests/test_all.py`.

- [ ] **Step 1: il test (fallisce: modulo assente)**

```python
def test_medianti_scritto():
    """Il pezzo di medianti sta in piedi: Do oscilla con le sue medianti
    cromatiche (una nota in comune a ogni cambio), la melodia tocca le note
    cromatiche nuove."""
    import medianti_scritto as MD                              # noqa: PLC0415
    from delugexml import musica as MU                         # noqa: PLC0415

    accordi = [a.strip() for a in MD.PROGRESSIONE.split('|')]
    check('il giro ha 8 battute', len(accordi) == 8, str(len(accordi)))
    check('oscilla fra Do e le sue medianti (Ab, E), torna a casa',
          accordi[0] == 'C' and accordi[-1] == 'C'
          and set(accordi) == {'C', 'Ab', 'E'}, str(accordi))
    # ogni cambio d'accordo condivide una sola nota (mediante cromatica)
    for a, b in zip(accordi, accordi[1:]):
        na = {y % 12 for y in MU.voci(a)}
        nb = {y % 12 for y in MU.voci(b)}
        check(f'{a}->{b}: una sola nota in comune',
              len(na & nb) == 1, str(sorted(na & nb)))
    # la melodia tocca le note cromatiche: mib (3) sul Lab, sol# (8) sul Mi
    per_b: dict[int, set[int]] = {}
    for y, note in MU.melodia(MD.MELODIA, durata='1/1').items():
        for n in note:
            per_b.setdefault(n.pos // 384, set()).add(y % 12)
    check('battuta 2 (Ab): la melodia ha il mib (3)',
          3 in per_b.get(1, set()), str(sorted(per_b.get(1, set()))))
    check('battuta 4 (E): la melodia ha il sol# (8)',
          8 in per_b.get(3, set()), str(sorted(per_b.get(3, set()))))
```

- [ ] **Step 2:** lanciare, verificare che fallisce.
- [ ] **Step 3: scrivere lo script**

```python
"""Il pezzo di prova delle medianti cromatiche, COMPOSTO seguendo
docs/istruzioni/medianti-cromatiche.md.

Do che oscilla con le sue due medianti maggiori -- Lab (sotto) e Mi (sopra) --
e torna a casa. Ogni cambio condivide una nota con Do: la morbidezza. La
melodia tocca le note cromatiche nuove (mib, sol#). condotta di default: la
nota comune tiene. Nessun sorteggio.

  battuta  accordo  melodia  perche'
  1        C         mi4     la casa
  2        Ab        mib4    mediante sotto (terza magg.): nota comune do, nuovo il mib
  3        C         mi4     a casa
  4        E         sol#4   mediante sopra (terza magg.): nota comune mi, nuovo il sol#
  5        C         sol4    a casa
  6        Ab        lab4    di nuovo sotto
  7        E         si4     di nuovo sopra (Lab->Mi e' anch'esso mediante, comune sol#)
  8        C         do5     a casa
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: 8 battute: Do fra Lab (mediante giu') e Mi (mediante su'), ritorno a casa.
PROGRESSIONE = 'C | Ab | C | E | C | Ab | E | C'

#: La melodia tocca la nota cromatica nuova di ogni mediante (mib su Lab, sol#
#: su Mi) e chiude sul do.
MELODIA = 'mi4 mib4 mi4 sol#4 sol4 lab4 si4 do5'

#: Il basso sulle fondamentali (do-lab-mi, le medianti).
BASSO = 'do2 lab2 do2 mi2 do2 lab2 mi2 do2'


def comping():
    """Gli accordi, voicing per terze, con la condotta (la nota comune tiene)."""
    return MU.armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                      durata='1/1')


def tema():
    """La melodia che tocca le note cromatiche."""
    return MU.melodia(MELODIA, durata='1/1')


def basso():
    """Il basso sulle fondamentali."""
    return MU.melodia(BASSO, durata='1/1')


if __name__ == '__main__':
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3'))
```

- [ ] **Step 4:** lanciare il test (passa) + la suite intera.
- [ ] **Step 5:** commit `medianti: il pezzo di prova, Do fra le sue medianti cromatiche`.

---

### Task 4: Assemblaggio + caricamento + ascolto (interattivo)

⚠️ Deluge collegato (ping prima). `S.set_scale(doc, 'C', 'maggiore')`, tre tracce (Rhodes/Trumpet/SawBass) `playing=True`, `length=8*384`; `MU.scrivi` con `MD.comping()/tema()/basso()`; `verifica` vuota; `racconta`; `write_file` in scratchpad; `put` di **`MEDIANT01`** (`MU.destinazione('mediant', 1)`) da **PowerShell**.

- [ ] L'utente apre `MEDIANT01`, ascolta lo scarto cromatico morbido, dà il verdetto.

---

### Task 5: L'esempio lavorato

**Files:** Modify `docs/istruzioni/medianti-cromatiche.md`.

- [ ] Aggiungere l'esempio lavorato (Do fra le medianti, le note cromatiche in melodia) col **verdetto** `[OSS]`. Se il verdetto chiede modifiche, cambiarle e ripetere il Task 4.
- [ ] LF + commit `medianti: l'esempio lavorato, col verdetto sul colore cinematografico`.
