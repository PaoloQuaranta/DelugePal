# Gli accordi di passaggio e approccio — piano

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`).

**Goal:** scrivere l'istruzione sugli accordi di passaggio (diminuita di passaggio) e di approccio (sostituzione di tritono, ♭II7) — la colla cromatica funzionale — e provarla su un pezzo da zero, sul Deluge. Chiude il cromatismo.

**Architecture:** stessa forma delle istruzioni. Funzionali (casa Do maggiore, niente `MODI`). Il pezzo in `tools/passaggio_scritto.py`. `condotta=True`.

## Global Constraints

- **Fonte:** Smith, *Jazz Theory* (4ª ed.), cap. VIII p. 59 (tritone sub + voice-leading chords) e cap. IX p. 75 (dim7 di passaggio, m7 cromatico).
- Gradi `[LIB]`/`[CALC]`/`[DEC]`/`[OSS]`; niente sorteggio; file a LF; commit `area: descrizione` senza accenti + trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **dsysex `put` da PowerShell**.
- ⚠️ `condotta=True` (default). Sono funzionali: vivono dentro una tonalità.

---

### Task 1: Il test `[CALC]`

**Files:** Modify `tests/test_all.py` (accanto a `test_medianti_cromatiche`).

- [ ] **Step 1:**

```python
def test_accordi_di_passaggio():
    """Le affermazioni [CALC] di docs/istruzioni/accordi-di-passaggio.md.

    La diminuita di passaggio ha la fondamentale un semitono fra i due accordi
    (basso cromatico); il tritone sub condivide il tritono col V7.
    """
    from delugexml import musica as MU                         # noqa: PLC0415
    # diminuita di passaggio: Do(0) -> C#dim7(1) -> Re m(2), basso cromatico
    fond = [MU.sigla(s).fondamentale for s in ('C', 'C#dim7', 'Dm7')]
    check('C#dim7 passa col basso cromatico fra Do (0) e Re (2)',
          fond == [0, 1, 2], str(fond))
    # tritone sub: Db7 (bII7) e G7 (V7) condividono il tritono fa-si
    g7 = {y % 12 for y in MU.voci('G7')}
    db7 = {y % 12 for y in MU.voci('Db7')}
    check('Db7 (tritone sub) e G7 condividono il tritono (fa=5, si=11)',
          {5, 11} <= g7 and {5, 11} <= db7, f'G7 {sorted(g7)}, Db7 {sorted(db7)}')
```

- [ ] **Step 2:** lanciare il test (PASS), poi la suite intera.
- [ ] **Step 3:** commit `test: il guardiano [CALC] degli accordi di passaggio e approccio`.

---

### Task 2: L'istruzione `accordi-di-passaggio.md`

**Files:** Create `docs/istruzioni/accordi-di-passaggio.md`.

- [ ] **Step 1: scrivere** nella forma delle istruzioni: **A cosa serve** → **grado di prova** → **principio** (la colla cromatica FUNZIONALE, contro i colori non-funzionali di planing/medianti — linkati; approccio per semitono) → **i due dispositivi** (diminuita di passaggio: `[LIB]` Smith cap. VIII p. 59 + cap. IX p. 75, basso cromatico do→do#→re; tritone sub ♭II7: `[LIB]` Smith cap. VIII p. 59, Db7→C, condivide il tritono con G7) → **il punto tecnico** (`condotta=True`, morbida) → **come si stabilisce** (infila la dim7 fra due diatonici / sostituisci il V7 col ♭II7, e risolvi) → **come si scrive** (`S.set_scale(doc, 'C', 'maggiore')` + `MU.armonia`) → **esempio lavorato** (da riempire al Task 5) → **cosa manca** (doppie medianti, diatonic planing; e la chiusura del cromatismo).
- [ ] **Step 2:** LF check + suite + commit `istruzioni: gli accordi di passaggio e approccio, la colla cromatica (Smith)`.

---

### Task 3: Il pezzo di prova `passaggio_scritto.py`

**Files:** Create `tools/passaggio_scritto.py`; Modify `tests/test_all.py`.

- [ ] **Step 1: il test (fallisce: modulo assente)**

```python
def test_passaggio_scritto():
    """Il pezzo di passaggio sta in piedi: la diminuita di passaggio e il
    tritone sub, la melodia su note d'accordo."""
    import passaggio_scritto as PS                             # noqa: PLC0415
    from delugexml import musica as MU                         # noqa: PLC0415

    accordi = [a.strip() for a in PS.PROGRESSIONE.split('|')]
    check('il giro ha 8 battute', len(accordi) == 8, str(len(accordi)))
    check('la diminuita di passaggio (C#dim7) e alla battuta 2',
          accordi[1] == 'C#dim7', accordi[1])
    check('il tritone sub (Db7) e alla battuta 4', accordi[3] == 'Db7', accordi[3])
    # il basso sale cromatico do->do#->re nelle battute 1-3
    fond = [MU.sigla(accordi[i]).fondamentale for i in (0, 1, 2)]
    check('il basso sale cromatico do->do#->re (bat. 1-3)',
          fond == [0, 1, 2], str(fond))
    # la melodia sta su note d'accordo
    per_b: dict[int, set[int]] = {}
    for y, note in MU.melodia(PS.MELODIA, durata='1/1').items():
        for n in note:
            per_b.setdefault(n.pos // 384, set()).add(y % 12)
    ok = all(per_b.get(i, set()) <= {y % 12 for y in MU.voci(accordi[i])}
             for i in range(8))
    check('ogni nota della melodia e una nota del suo accordo', ok, '')
```

- [ ] **Step 2:** lanciare, verificare che fallisce.
- [ ] **Step 3: scrivere lo script**

```python
"""Il pezzo di prova degli accordi di passaggio e approccio, COMPOSTO seguendo
docs/istruzioni/accordi-di-passaggio.md.

La diminuita di passaggio (C#dim7, basso cromatico do->do#->re) e il tritone
sub (Db7, approccio a Do dall'alto), in un turnaround in Do. condotta di
default: la colla e' morbida. Nessun sorteggio.

  battuta  accordo   melodia  perche'
  1        Cmaj7      sol4    la casa
  2        C#dim7     la#4    diminuita di passaggio (basso do#), la 7a
  3        Dm7        la4     il ii
  4        Db7        lab4    tritone sub del G7: approccia Do dall'alto
  (le battute 5-8 ripetono: il turnaround rigira in cima)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

#: 8 battute: un turnaround in Do con la diminuita di passaggio e il tritone
#: sub. Il Db7 dell'ultima battuta rigira sul Cmaj7 in cima.
PROGRESSIONE = 'Cmaj7 | C#dim7 | Dm7 | Db7 | Cmaj7 | C#dim7 | Dm7 | Db7'

#: La melodia tiene note d'accordo, con la discesa sib->la->lab che eco del
#: movimento cromatico del basso.
MELODIA = 'sol4 la#4 la4 lab4 sol4 la#4 la4 lab4'

#: Il basso sulle fondamentali (do-do#-re-reb...): porta il cromatismo.
BASSO = 'do2 do#2 re2 reb2 do2 do#2 re2 reb2'


def comping():
    """Gli accordi, voicing per terze, con la condotta (la colla e' morbida)."""
    return MU.armonia(PROGRESSIONE, voicing='chiuso', registro='do3',
                      durata='1/1')


def tema():
    """La melodia su note d'accordo."""
    return MU.melodia(MELODIA, durata='1/1')


def basso():
    """Il basso cromatico sulle fondamentali."""
    return MU.melodia(BASSO, durata='1/1')


if __name__ == '__main__':
    print(MU.racconta_armonia(PROGRESSIONE, voicing='chiuso', registro='do3'))
```

- [ ] **Step 4:** lanciare il test (passa) + la suite intera.
- [ ] **Step 5:** commit `passaggio: il pezzo di prova, la diminuita di passaggio e il tritone sub`.

---

### Task 4: Assemblaggio + caricamento + ascolto (interattivo)

⚠️ Deluge collegato (ping prima). `S.set_scale(doc, 'C', 'maggiore')`, tre tracce (Rhodes/Trumpet/SawBass) `playing=True`, `length=8*384`; `MU.scrivi` con `PS.comping()/tema()/basso()`; `verifica` vuota; `racconta`; `write_file` in scratchpad; `put` di **`PASSAGG01`** (`MU.destinazione('passagg', 1)`) da **PowerShell**.

- [ ] L'utente apre `PASSAGG01`, ascolta la colla cromatica, dà il verdetto.

---

### Task 5: L'esempio lavorato

**Files:** Modify `docs/istruzioni/accordi-di-passaggio.md`.

- [ ] Aggiungere l'esempio lavorato (i due dispositivi nel turnaround) col **verdetto** `[OSS]`. Dichiarare che **il cromatismo e' chiuso** (tre facce). Se il verdetto chiede modifiche, cambiarle e ripetere il Task 4.
- [ ] LF + commit `passaggio: l'esempio lavorato, e il cromatismo chiuso`.
