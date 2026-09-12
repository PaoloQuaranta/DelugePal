# Prestito, casa minore: colori jazz e Piccardia — piano

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`).

**Goal:** chiudere gli ultimi due colori della casa minore in `armonia-prestito.md` — il **minore jazz** (m6/m(maj7), il line cliché) e la **terza di Piccardia** — in un solo pezzo in La minore, provato sul Deluge.

**Architecture:** terza iterazione della stessa forma (test `[CALC]`, sezione d'istruzione, pezzo in `prestito_scritto.py`, assemblaggio + SysEx). I due colori stanno in un unico pezzo: il line cliché `Am→Am(maj7)→Am7→Am6` (bat. 1-4) che chiude in Piccardia su `A` (bat. 8).

## Global Constraints

- **Fonte:** Smith p. 74 (il ♮6/♮7 «dal maggiore parallelo»); Piston per la Piccardia (pagina da pinnare scrivendo). Il line cliché è `[DEC]`, applicazione idiomatica.
- `MU.sigla` legge già `Am6`, `Am(maj7)`, `A` — nessuna sigla nuova.
- Niente sorteggio; voicing per terze; file a LF; commit `area: descrizione` senza accenti + trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **dsysex `put` da PowerShell** (memoria `dsysex-da-powershell`).
- Test: `.venv/Scripts/python.exe tests/test_all.py`; uno solo via `-c "...; import test_all; test_all.<nome>()"`.

---

### Task 1: Estendere il test `[CALC]` coi colori jazz-minore

**Files:** Modify `tests/test_all.py` — nel dizionario `prestiti` di `test_armonia_prestito_casa_minore`.

- [ ] **Step 1:** aggiungere `Am6` (♮6=9) e `AmMaj7` (♮7=11) al dizionario:

```python
    prestiti = {'D': 9, 'Bm': 9, 'A': 4, 'Am6': 9, 'AmMaj7': 11}
```

- [ ] **Step 2:** lanciare `test_armonia_prestito_casa_minore` — tutte `PASS` (le due nuove comprese).
- [ ] **Step 3:** commit `test: i colori jazz-minore (m6, m-maj7) nel guardiano della casa minore`.

---

### Task 2: La sottosezione nell'istruzione

**Files:** Modify `docs/istruzioni/armonia-prestito.md` (dentro «La direzione inversa: una casa minore»).

- [ ] **Step 1:** aggiungere, dopo la tabella della casa minore, un blocco **«Il colore del minore jazz»**: gli accordi **m6** (♮6) e **m(maj7)** (♮7) come tonica colorata dalla minore melodica, mostrati col *line cliché* `Am → Am(maj7) → Am7 → Am6` (la discesa A-G#-G-F# su pedale di tonica). `[LIB]` Smith p. 74; il line cliché `[DEC]`. E un richiamo alla **Piccardia** (già in tabella) come **chiusura**: un pezzo in minore che finisce su una tonica maggiore. Pinnare la pagina di Piston (cercare «Picardy»/«tierce» nel PDF).
- [ ] **Step 2:** aggiornare «Cosa manca» — la Piccardia e il ♮6/♮7 jazz non sono più fuori; resta solo le scale non diatoniche.
- [ ] **Step 3:** LF check + suite intera (stesso numero di fallimenti) + commit `istruzioni: il colore del minore jazz e la Piccardia, casa minore chiusa`.

---

### Task 3: Il terzo pezzo in `prestito_scritto.py`

**Files:** Modify `tools/prestito_scritto.py`; Modify `tests/test_all.py`.

- [ ] **Step 1: il test (fallisce: costanti assenti)**

```python
def test_prestito_scritto_jazzmin():
    """Il terzo pezzo: il line cliche' jazz-minore e la Piccardia finale."""
    import prestito_scritto as PR                              # noqa: PLC0415
    from delugexml import musica as MU                         # noqa: PLC0415

    accordi = [a.strip() for a in PR.PROGRESSIONE_JAZZMIN.split('|')]
    check('il giro ha 8 battute', len(accordi) == 8, str(len(accordi)))
    check('il line cliche e Am->Am(maj7)->Am7->Am6',
          accordi[:4] == ['Am', 'Am(maj7)', 'Am7', 'Am6'], str(accordi[:4]))
    check('chiude in Piccardia su La maggiore', accordi[-1] == 'A', accordi[-1])

    per_battuta: dict[int, set[int]] = {}
    for y, note in MU.melodia(PR.MELODIA_JAZZMIN, durata='1/1').items():
        for n in note:
            per_battuta.setdefault(n.pos // 384, set()).add(y % 12)
    check('battuta 2 (Am-maj7): la melodia ha il sol# (8), il nat7',
          8 in per_battuta.get(1, set()), str(sorted(per_battuta.get(1, set()))))
    check('battuta 4 (Am6): la melodia ha il fa# (6), il nat6',
          6 in per_battuta.get(3, set()), str(sorted(per_battuta.get(3, set()))))
    check('battuta 8 (A): la melodia ha il do# (1), la Piccardia',
          1 in per_battuta.get(7, set()), str(sorted(per_battuta.get(7, set()))))
```

- [ ] **Step 2:** lanciare, verificare che fallisce (`AttributeError: ...PROGRESSIONE_JAZZMIN`).
- [ ] **Step 3: estendere lo script** (in coda, prima di `if __name__`):

```python
# --- il terzo pezzo: i colori del minore JAZZ (line cliche') + Piccardia finale
#
#   battuta  accordo   grado      melodia  perche'
#   1        Am        i           la4     tonica, l'inizio del cliche'
#   2        Am(maj7)  i(maj7)    sol#4    il nat7 (G#), preso dal maggiore
#   3        Am7       i7          sol4    il b7 (G), la discesa continua
#   4        Am6       i6         fa#4     il nat6 (F#): il colore della minore melodica
#   5        Dm7       iv          fa4     ci si muove
#   6        E7        V7          mi4     la dominante (NON un prestito)
#   7        Am        i           mi4     tonica minore
#   8        A         I (Picc.)  do#4     la Piccardia: la tonica diventa MAGGIORE
#
#: Bat. 1-4: il line cliche', la discesa A-G#-G-F# su pedale di La -- il nat7 e
#: il nat6 presi dal maggiore parallelo, il suono della minore melodica/jazz.
#: Bat. 8: la terza di Piccardia, il finale che si apre su La maggiore.
PROGRESSIONE_JAZZMIN = 'Am | Am(maj7) | Am7 | Am6 | Dm7 | E7 | Am | A'
MELODIA_JAZZMIN = 'la4 sol#4 sol4 fa#4 fa4 mi4 mi4 do#4'
BASSO_JAZZMIN = 'la1 la1 la1 la1 re2 mi2 la1 la1'


def comping_jazzmin():
    """Gli accordi del terzo pezzo, voicing per terze."""
    return MU.armonia(PROGRESSIONE_JAZZMIN, voicing='chiuso', registro='la2',
                      durata='1/1')


def tema_jazzmin():
    """La melodia del terzo pezzo (il line cliche' in cima)."""
    return MU.melodia(MELODIA_JAZZMIN, durata='1/1')


def basso_jazzmin():
    """Il basso del terzo pezzo: pedale di La sotto il cliche'."""
    return MU.melodia(BASSO_JAZZMIN, durata='1/1')
```

E aggiungere al blocco `__main__` un `racconta_armonia(PROGRESSIONE_JAZZMIN, ..., registro='la2')`.

- [ ] **Step 4:** lanciare il test (passa) + la suite intera (niente regressioni).
- [ ] **Step 5:** commit `prestito: il terzo pezzo, line cliche jazz-minore e Piccardia`.

---

### Task 4: Assemblaggio + caricamento + ascolto (interattivo)

⚠️ Serve il Deluge collegato (ping prima). Come gli altri, con `set_scale(doc, 'A', 'minore')` e le costanti `*_JAZZMIN`; `put` di `PRESTITO03` (`MU.destinazione('prestito', 3)`) da **PowerShell**.

- [ ] Costruire (template `TEMPL0`, via il track di default, tre tracce Rhodes/Trumpet/SawBass `playing=True`, `length=8*384`); `verifica` vuota; `racconta`; `write_file` in scratchpad; `ping`; `put PRESTITO03`.
- [ ] L'utente apre `PRESTITO03`, ascolta il line cliché (bat. 1-4) e la Piccardia (bat. 8), dà il verdetto.

---

### Task 5: Il terzo esempio lavorato

**Files:** Modify `docs/istruzioni/armonia-prestito.md`.

- [ ] Aggiungere il terzo esempio lavorato (La minore, line cliché + Piccardia) col **verdetto** `[OSS]`. Se il verdetto chiede modifiche, cambiarle e ripetere il Task 4.
- [ ] LF + commit `prestito: il terzo esempio lavorato, minore jazz e Piccardia, col verdetto`.
