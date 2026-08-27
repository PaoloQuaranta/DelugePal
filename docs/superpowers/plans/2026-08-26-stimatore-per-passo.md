# Lo stimatore per passo — piano di attuazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** dare a `profilo_da_colpi()` tre modi di scegliere il passo su cui contare un colpo, misurare quale dei tre è uno stimatore vero sotto traslazione per voce, e scegliere il default con quei numeri in mano — chiudendo il punto aperto che `docs/repertori/jazz.md` dichiara e non prende.

**Architecture:** il ciclo di `profilo_da_colpi()` si spezza in **due passate**: la prima calcola la posizione «dritta» di ogni colpo (origine tolta, swing tolto) raggruppata per strumento; la seconda sceglie il passo **una voce alla volta**, usando uno *spostamento del taglio* che dipende da tutti i colpi di quella voce. Lo spostamento lo calcola una funzione sola, `spostamento_del_taglio()`, con tre modi. Il residuo riportato resta `dritta − passo · passo_tick`, cioè misurato rispetto alla griglia vera.

**Tech Stack:** Python 3, **solo stdlib** (`math`, `statistics`). Nessuna dipendenza nuova, mai.

## Global Constraints

- **Nessuna dipendenza nuova.** Solo stdlib. È la regola per cui `midi.py` si è scritto un lettore di Standard MIDI File invece di tirarsi dentro `mido`.
- **Niente pytest.** I test stanno tutti in `tests/test_all.py`, si scrivono con `check(nome, condizione, dettaglio)` e si eseguono con `.venv/Scripts/python.exe tests/test_all.py`. Una funzione il cui nome comincia per `test_` viene raccolta da sola dal runner in fondo al file. I test nuovi vanno **prima** del blocco `if __name__ == '__main__':`.
- **Baseline della suite: 943/943 test superati**, misurato il 26 agosto 2026 prima di questo lavoro. Nessun task può farla scendere.
- **`to-read/` è in `.gitignore`.** Un test che tocca il dataset deve sollevare `FileNotFoundError` quando manca: il runner lo converte in `SKIP`. Percorso: `to-read/MIDI/groove-v1.0.0-midionly/groove/`, con `info.csv` dentro.
- **Il commento in italiano senza accenti** nel codice (`perche'`, `gia'`); nei documenti Markdown gli accenti si scrivono normali.
- **Un numero vive in un posto solo.** Mai ricopiare un valore in due file: altrove è un rimando.
- Costanti già esistenti da riusare, mai ridefinire: `midi.TICK_PER_MOVIMENTO_DELUGE` = 96, `musica.TICK_PER_PASSO` = 24, `musica.TICK_PER_BATTUTA` = 384, `midi.GM_PERCUSSIONI`.
- ⚠️ **`pathlib.write_text()` su Windows traduce `\n` in `\r\n`** e rende illeggibile la revisione. Chi genera o riscrive un file usa `write_bytes()`. Vale per tutti i task che toccano Markdown.
- ⚠️ **Non si rigenerano** `out/GROOVE0.XML`, `out/GROOVE1.XML`, `out/SWINGA.XML`, `out/SWINGB.XML`. Sono l'unico esemplare su cui poggiano i quattro ascolti e il giro sul dispositivo. `tools/genera_groove.py` e `tools/genera_swing.py` **non si eseguono** in nessun task di questo piano.
- **Commit dopo ogni task**, messaggio in italiano, con `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>` in fondo.
- **Il default non cambia** fino al Task 6. Cambiare stimatore e cambiare default nello stesso diff renderebbe illeggibile quale delle due cose ha mosso un numero.

---

## File

| file | responsabilità |
|---|---|
| `tools/delugexml/groove.py` | **modifica**: `TAGLI`, `spostamento_del_taglio()`, le due passate di `profilo_da_colpi()`, il parametro `taglio` anche su `profilo()`, il limite nel docstring di `Passo` |
| `tools/delugexml/musica.py` | **modifica**: `applica_groove()` riferisce le **collisioni** — due note su passi adiacenti che finiscono sullo stesso tick, cosa che il limite allargato rende possibile (Task 3) |
| `tools/misura_groove.py` | **modifica**: `il_vuoto_delle_voci()` (Task 3), `la_prova_di_traslazione()` (Task 4), `l_ancoraggio()` (Task 5), e `il_bordo_del_passo()` che gira sui tre tagli (Task 6) |
| `tests/test_all.py` | **modifica**: i check nuovi in fondo, prima di `if __name__ == '__main__':` |
| `docs/repertori/jazz.md` | **modifica**: «Il bordo fra due passi» prende la decisione; i numeri della casella 6 rifatti (Task 7) |
| `docs/MUSICA.md` | **modifica**: «Il groove template», il limite dichiarato di `Passo.scarto` (Task 7) |
| `.claude/skills/deluge-pal/SKILL.md` | **modifica**: la riga di `applica_groove()` (Task 7) |
| `HANDOFF.md` | **modifica**: §7 perde il punto aperto, §6-terdecies acquista la sezione (Task 7) |

---

## Task 1: Le due passate, e il parametro che non cambia niente

Il ciclo di `profilo_da_colpi()` oggi fa tutto in una passata: per ogni colpo calcola la dritta e sceglie subito il passo. Uno spostamento del taglio dipende da **tutti** i colpi di una voce, quindi la scelta del passo va rimandata a una seconda passata.

**Questo task è una ristrutturazione, e il suo test è un'uguaglianza.** Si fa per primo apposta: finché il default è `'vicino'` e lo spostamento è `0.0`, ogni numero prodotto deve restare **identico** a prima. Se non lo è, tutto il confronto dei task successivi è inattribuibile.

**Files:**
- Modify: `tools/delugexml/groove.py:238-252` (docstring di `Passo`), `:287-357` (`profilo_da_colpi`), `:360-387` (`profilo`)
- Test: `tests/test_all.py`

**Interfaces:**
- Produces: `groove.TAGLI = ('vicino', 'voce', 'rado')`; `groove.spostamento_del_taglio(dritte: list[float], passo_tick: float, modo: str = 'vicino') -> float`; `groove.profilo_da_colpi(colpi, ppq, *, id='', drummer='', style='', bpm=0, taglio='vicino') -> Profilo`; `groove.profilo(base, id, *, taglio='vicino') -> Profilo`.
- Consumes: niente di nuovo.

- [ ] **Step 1: Scrivere i test che falliscono**

In fondo a `tests/test_all.py`, prima del blocco `if __name__ == '__main__':`:

```python
def test_groove_taglio_neutro():
    """Il parametro `taglio` esiste, e sul default non cambia NIENTE.

    ⚠️ E' il cancello di tutto il confronto fra stimatori: se `'vicino'` non
    riproduce esattamente i numeri di prima, ogni differenza misurata fra i
    tagli e' inattribuibile -- non si sa se l'ha mossa lo stimatore o la
    ristrutturazione del ciclo.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0
    # due voci, posizioni scelte a mano: un kick sui battere e un ride sulle
    # crome swingate. Nessun colpo al bordo: qui non si misura il bordo, si
    # misura che il refactoring non abbia mosso niente.
    colpi = {
        'kick': [(float(b * 384 + m * 96), 100) for b in range(4)
                 for m in (0, 2)],
        'ride': [(float(b * 384 + m * 96 + d), 80) for b in range(4)
                 for m in range(4) for d in (0, 64)],
    }
    senza = GR.profilo_da_colpi(colpi, ppq, id='finto/1')
    con = GR.profilo_da_colpi(colpi, ppq, id='finto/1', taglio='vicino')
    check('taglio="vicino" da lo stesso Profilo di prima', senza == con,
          f'{senza}\n{con}')

    check('un taglio sconosciuto e un errore che elenca i modi',
          _raises(lambda: GR.profilo_da_colpi(colpi, ppq, taglio='pippo'),
                  ValueError))
    try:
        GR.profilo_da_colpi(colpi, ppq, taglio='pippo')
    except ValueError as e:
        check('e il messaggio nomina i tre modi',
              all(m in str(e) for m in GR.TAGLI), str(e))

    check('lo spostamento di "vicino" e zero',
          GR.spostamento_del_taglio([1.0, 2.0, 3.0], 24.0, 'vicino') == 0.0,
          str(GR.spostamento_del_taglio([1.0, 2.0, 3.0], 24.0, 'vicino')))


def test_groove_taglio_neutro_sul_corpus():
    """Lo stesso cancello, sul dataset vero. SALTA se non c'e'.

    Il caso sintetico non ha colpi al bordo; il corpus ne ha. Se la
    ristrutturazione avesse cambiato qualcosa, e' qui che si vede.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    base = ROOT / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
    if not (base / GR.INVENTARIO).exists():
        raise FileNotFoundError(str(base / GR.INVENTARIO))

    for quale in ('drummer1/session3/2', 'drummer10/session1/1'):
        p = GR.profilo(base, quale)
        v = GR.profilo(base, quale, taglio='vicino')
        check(f'{quale}: il default e "vicino", identico', p == v,
              f'{quale}')
```

- [ ] **Step 2: Eseguire i test e verificare che falliscano**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "taglio|^[0-9]+/"`

Expected: FAIL — le due funzioni sollevano `TypeError: profilo_da_colpi() got an unexpected keyword argument 'taglio'`, che il runner converte in un check rosso `test_groove_taglio_neutro` con `eccezione TypeError`.

- [ ] **Step 3: Aggiungere `TAGLI` e `spostamento_del_taglio()`**

In `tools/delugexml/groove.py`, subito **prima** di `class Passo`:

```python
#: I modi di taglio: come si sceglie il passo su cui un colpo va contato.
#: Il default resta `'vicino'` finche' la misura non ha scelto -- vedi
#: `docs/superpowers/specs/2026-08-26-stimatore-per-passo-design.md`.
TAGLI = ('vicino', 'voce', 'rado')


def spostamento_del_taglio(dritte, passo_tick: float,
                           modo: str = 'vicino') -> float:
    """Di quanto spostare il TAGLIO fra due passi, per questa voce, in tick.

    Il passo si sceglie poi con `round((dritta - spostamento) / passo_tick)`:
    spostare il taglio NON sposta la griglia, sposta solo il confine su cui
    si decide a quale passo un colpo appartiene. Il residuo riportato resta
    misurato dalla griglia vera.

    `'vicino'` e' l'assenza di spostamento, cioe' il `round()` di sempre:
    taglia a meta' fra due passi. E' il termine di paragone.
    """
    if modo not in TAGLI:
        raise ValueError(f'taglio {modo!r} sconosciuto: ci sono {list(TAGLI)}')
    return 0.0
```

- [ ] **Step 4: Spezzare il ciclo di `profilo_da_colpi()` in due passate**

Sostituire il corpo fra `passo_tick = ppq / 4` e la costruzione di `passi` con questo. **La firma prende `taglio='vicino'` come keyword-only**, in coda a quelli che ci sono già:

```python
def profilo_da_colpi(colpi: dict[str, list[tuple[float, int]]], ppq: float,
                     *, id: str = '', drummer: str = '', style: str = '',
                     bpm: int = 0, taglio: str = 'vicino') -> Profilo:
```

e il corpo:

```python
    if taglio not in TAGLI:
        raise ValueError(f'taglio {taglio!r} sconosciuto: ci sono {list(TAGLI)}')
    passo_tick = ppq / 4                            # un 1/16
    tutte = [p for note in colpi.values() for p, _ in note]
    off = origine(tutte, passo_tick)

    bur = bur_da_posizioni([p - off for p in tutte], ppq)
    levare = da_bur(bur) if bur is not None else 0.5

    # PRIMA PASSATA: la posizione DRITTA di ogni colpo -- origine tolta,
    # swing tolto -- raggruppata per strumento. Il passo NON si sceglie
    # qui: uno spostamento del taglio dipende da TUTTI i colpi di una
    # voce, e finche' non li abbiamo visti tutti non si puo' decidere.
    dritte: dict[str, list[tuple[float, int]]] = {}
    for nome, note in colpi.items():
        for pos, vel in note:
            p = pos - off
            # il movimento in cui la nota CADE, e la sua fase dentro di
            # esso: floor-division, la stessa convenzione di
            # `levare_da_posizioni()`, e per p negativi -144 // 96 fa -2.
            #
            # ⚠️ LA FASE STA IN [0,1) E NON PUO' USCIRNE, perche' e' il
            # dominio su cui `_senza_swing()` e' l'inversa della mappa del
            # firmware. Fino al 24 agosto 2026 qui c'era mezzo passo di
            # grazia -- `math.floor(p / ppq + 0.125)` -- e una nota
            # nell'ultimo ottavo usciva con fase NEGATIVA, su cui
            # `_senza_swing()` applicava il ramo sbagliato. Non era
            # l'inversa di niente.
            movimento, resto = divmod(p, ppq)
            fase = resto / ppq
            dritte.setdefault(nome, []).append(
                ((movimento + _senza_swing(fase, levare)) * ppq, vel))

    # SECONDA PASSATA: una voce alla volta, col suo spostamento del taglio.
    per_passo: dict[str, dict[int, list[tuple[int, float]]]] = {}
    ultimo = 0
    for nome, note in dritte.items():
        sp = spostamento_del_taglio([d for d, _ in note], passo_tick, taglio)
        for dritta, vel in note:
            # ⚠️ il passo si decide DOPO aver tolto lo swing: un levare
            # swingato sta a 2,67 passi e si arrotonderebbe al 3.
            passo = round((dritta - sp) / passo_tick)
            ultimo = max(ultimo, passo)
            # ⚠️ il residuo si misura dalla GRIGLIA, non dal taglio
            # spostato: e' la posizione vera del colpo rispetto al passo su
            # cui lo scriviamo. Sottrarre anche `sp` toglierebbe il feel
            # invece di collocarlo.
            residuo = dritta - passo * passo_tick
            per_passo.setdefault(nome, {}).setdefault(
                passo % 16, []).append((vel, residuo))
```

Il blocco che costruisce `passi` e il `return Profilo(...)` restano **invariati**.

- [ ] **Step 5: Passare `taglio` anche da `profilo()`**

In `profilo()`, aggiungere il parametro keyword-only e inoltrarlo:

```python
def profilo(base: Path | str, id: str, *, taglio: str = 'vicino') -> Profilo:
```

e nella chiamata finale:

```python
    return profilo_da_colpi(colpi, float(MI.TICK_PER_MOVIMENTO_DELUGE),
                            id=e.id, drummer=e.drummer, style=e.style,
                            bpm=e.bpm, taglio=taglio)
```

- [ ] **Step 6: Eseguire tutta la suite**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | tail -5`

Expected: PASS su tutti, e il totale sale dalla baseline di **943** ai check nuovi (943 + 6 se il dataset c'è, 943 + 4 se salta). **Nessun test che c'era prima deve diventare rosso**: se ne cade uno, la ristrutturazione ha mosso qualcosa e va trovato prima di andare avanti.

- [ ] **Step 7: Commit**

```bash
git add tools/delugexml/groove.py tests/test_all.py
git commit -m "groove: due passate invece di una, e un parametro che non cambia niente

Uno spostamento del taglio dipende da tutti i colpi di una voce, quindi la
scelta del passo va rimandata a una seconda passata. Il default resta
'vicino', cioe' lo zero, e il test e' un'uguaglianza: identico a prima.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 2: `'voce'` — la media circolare della voce, senza finestra

**Files:**
- Modify: `tools/delugexml/groove.py` (`spostamento_del_taglio`)
- Test: `tests/test_all.py`

**Interfaces:**
- Consumes: `groove.TAGLI`, `groove.spostamento_del_taglio(dritte, passo_tick, modo)` dal Task 1.
- Produces: `spostamento_del_taglio(..., 'voce')` ritorna la media circolare delle fasi in `(-passo_tick/2, +passo_tick/2]`.

⚠️ **`GR.origine()` NON si può chiamare qui, ed è il punto in cui questo task è facile da sbagliare.** `origine()` tiene solo i colpi dentro `finestra = 0,25 · passo`, e sul charleston di `drummer10/session1/1` ne tiene **58 su 143** — scarta proprio gli anticipati, che sono il fenomeno. Ne uscirebbe **−0,40 tick** invece di **−8,80**, cioè un candidato finto che passa il confronto senza spostare nessun passo. La finestra di `origine()` serve a tenere fuori i **levare swingati** dalla stima dello scarto comune del kit; qui lo swing l'ha già tolto `_senza_swing()`, e un levare swingato è ormai *su* un passo. La ragione non si trasporta.

- [ ] **Step 1: Scrivere il test che fallisce**

```python
def test_groove_taglio_voce():
    """`'voce'` chiude la spaccatura di un gesto a cavallo del confine.

    Il caso: una voce che anticipa di 14 tick i passi 4 e 12 -- cioe' il 2 e
    il 4, come il charleston a pedale del jazz -- con dispersione di 3 tick.
    Anticipare di piu' di mezzo passo (12 tick) e' esattamente il caso che
    `round()` non sa rappresentare.

    ⚠️ Questo test NON asserisce su QUALE passo il gesto finisca ancorato.
    L'ancoraggio e' una domanda a se' -- i dati soli non distinguono "14 tick
    prima del passo 4" da "10 tick dopo il passo 3", e il gesto e' pure piu'
    VICINO al passo 3 -- e la MISURA il Task 5. Qui si misura una cosa sola:
    che il gesto smetta di stare in DUE celle con segni opposti.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0
    # 12 battute, il gesto sul passo 4 e sul passo 12, anticipato di 14 tick
    # con dispersione fissa (non casuale: un test deve dare sempre lo stesso
    # numero). 96-14 = 82 e 288-14 = 274, piu' gli scarti.
    posizioni = [float(b * 384 + base + d)
                 for b in range(12) for base in (82, 274)
                 for d in (-3, -1, 1, 3)]
    colpi = {'charleston a pedale': [(p, 90) for p in posizioni]}

    vicino = GR.profilo_da_colpi(colpi, ppq, taglio='vicino')
    voce = GR.profilo_da_colpi(colpi, ppq, taglio='voce')

    def celle(prof):
        return {p.passo: p for p in prof.passi['charleston a pedale']
                if p.colpi >= 10}

    cv, cc = celle(vicino), celle(voce)

    check('con "vicino" il gesto sta in quattro celle (due per battere)',
          len(cv) == 4, str(sorted(cv)))
    coppie = [(k, k + 1) for k in (3, 11) if k in cv and k + 1 in cv]
    check('e sono coppie adiacenti di segno opposto',
          len(coppie) == 2
          and all(cv[a].scarto * cv[b].scarto < 0 for a, b in coppie),
          str({k: round(v.scarto, 2) for k, v in sorted(cv.items())}))
    check('col BATTERE IN MINORANZA: la semicroma prima porta piu colpi',
          all(cv[a].colpi > cv[b].colpi for a, b in coppie),
          str({k: v.colpi for k, v in sorted(cv.items())}))

    check('con "voce" il gesto sta in due celle sole, una per battere',
          len(cc) == 2, str(sorted(cc)))
    check('e ognuna porta tutti i colpi del suo gesto',
          all(v.colpi == 48 for v in cc.values()),
          str({k: v.colpi for k, v in sorted(cc.items())}))

    # lo spostamento e' quello che ci si aspetta da quelle fasi: le fasi
    # sono 7, 9, 11 e -11 tick, la cui media circolare vale +10.
    dritte = [p for p in posizioni]
    sp = GR.spostamento_del_taglio(dritte, 24.0, 'voce')
    check('lo spostamento della voce vale +10 tick',
          abs(sp - 10.0) < 0.01, f'{sp:.3f}')

    # ⚠️ la funzione col cancello sbagliato: GR.origine() ha una finestra
    # che scarta proprio gli anticipati, e qui darebbe zero.
    check('GR.origine() su questa voce da un numero DIVERSO, ed e per questo '
          'che "voce" non la chiama',
          abs(GR.origine(dritte, 24.0) - sp) > 1.0,
          f'origine {GR.origine(dritte, 24.0):.3f} contro voce {sp:.3f}')
```

- [ ] **Step 2: Eseguire il test e verificare che fallisca**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "taglio_voce|voce|^[0-9]+/"`

Expected: FAIL sui check di `'voce'` — lo spostamento è ancora `0.0`, quindi `'voce'` dà le stesse quattro celle di `'vicino'`.

- [ ] **Step 3: Implementare il modo `'voce'`**

In `spostamento_del_taglio()`, sostituire `return 0.0` con:

```python
    if modo == 'vicino':
        return 0.0
    if modo == 'voce':
        return _media_circolare(dritte, passo_tick)
    raise ValueError(f'taglio {modo!r} non ancora implementato')
```

e aggiungere sopra:

```python
def _media_circolare(posizioni, passo: float) -> float:
    """La fase media della voce dentro il passo, in tick, CON SEGNO.

    Stessa aritmetica di `origine()` -- si mediano i versori, perche' la
    fase GIRA e la media aritmetica di 1 e 23 darebbe 12, cioe' il
    contrario di zero -- ma SENZA la sua finestra, ed e' una differenza che
    va capita prima di "semplificare" chiamando `origine()`.

    ⚠️ PERCHE' SENZA FINESTRA. `origine()` tiene solo i colpi dentro
    0,25 passo per non far sporcare lo scarto comune del kit dai LEVARE
    SWINGATI, che stanno a 8 tick su 24 dalla griglia dei passi. Qui lo
    swing lo ha gia' tolto `_senza_swing()`, e un levare swingato e' ormai
    SU un passo: la ragione della finestra non si trasporta. Se la si
    tenesse, sul charleston a pedale di `drummer10/session1/1` questa
    funzione vedrebbe 58 colpi su 143 -- scartando proprio gli anticipati,
    che sono il fenomeno -- e darebbe -0,40 tick invece di -8,80 `[OSS]`,
    cioe' non sposterebbe nessun passo.

    IL LIMITE, DICHIARATO: la media circolare di una voce sparsa e' un
    numero debole. Sul charleston di quell'esecuzione la concentrazione
    vale R = 0,16. E' il sospetto che la prova di traslazione per voce
    (`tools/misura_groove.py`, `la_prova_di_traslazione()`) deve mettere
    alla prova, e la ragione per cui i candidati sono due.
    """
    fasi = []
    for p in posizioni:
        s = p % passo
        if s > passo / 2:
            s -= passo                  # la fase gira: 23 su 24 e' -1
        fasi.append(s / passo * 2 * math.pi)
    if not fasi:
        return 0.0
    x = sum(math.cos(a) for a in fasi) / len(fasi)
    y = sum(math.sin(a) for a in fasi) / len(fasi)
    if abs(x) < 1e-12 and abs(y) < 1e-12:
        return 0.0                      # fasi sparse: nessuna fase media
    return math.atan2(y, x) / (2 * math.pi) * passo
```

- [ ] **Step 4: Nominare la sorella dentro `origine()`**

In `origine()`, in fondo alla sezione «IL LIMITE, DICHIARATO», aggiungere:

```python
    LA SORELLA: `_media_circolare()` fa la stessa aritmetica SENZA la
    finestra, e serve al taglio `'voce'`. Le due non si possono
    sostituire l'una all'altra: la a finestra stima lo scarto comune del
    KIT prima che lo swing sia tolto, l'altra la fase di UNA VOCE dopo.
```

- [ ] **Step 5: Eseguire tutta la suite**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | tail -5`

Expected: tutti PASS, totale = quello del Task 1 + 7.

- [ ] **Step 6: Verifica per inversione**

Rimettere temporaneamente `return origine(dritte, passo_tick)` al posto di `_media_circolare(...)` nel ramo `'voce'`, rieseguire la suite, **verificare che i check di `test_groove_taglio_voce` diventino rossi**, poi rimettere com'era.

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -c FAIL`

Expected: almeno 3 FAIL con la versione sbagliata, 0 con quella giusta. **Un test che passa in tutt'e due i casi non sta misurando quello che dice.**

- [ ] **Step 7: Commit**

```bash
git add tools/delugexml/groove.py tests/test_all.py
git commit -m "groove: il taglio 'voce', e perche' non puo' chiamare origine()

La finestra di origine() scarta proprio i colpi anticipati -- 58 su 143 sul
charleston di drummer10/session1/1 -- e darebbe -0,40 invece di -8,80. Serve
a tenere fuori i levare swingati dallo scarto comune del kit, ma qui lo swing
lo ha gia' tolto _senza_swing(). La ragione non si trasporta.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 3: `'rado'` — tagliare nel mezzo del vuoto più largo

L'idea in una riga: **non tagliare attraverso un gesto**. Invece di tagliare a metà fra due passi, si taglia dove la voce non ha colpi.

> ⚠️ **Questa sezione è stata riscritta il 26 agosto 2026, e il perché va letto prima del codice.** La prima stesura cercava il **minimo di densità** con una finestra larga `LARGHEZZA_RADO`, e ne prendeva l'argmin. Eseguita alla lettera, ha prodotto tre difetti, tutti misurati:
>
> 1. **il taglio si incollava.** Il minimo di densità è un **altopiano** — un arco intero senza colpi — e l'argmin ne prendeva il primo punto della scansione, che sta sempre a fase 0. Traslando la voce di −4, −2, 0, +2, +4 tick lo spostamento restava **−12,00 tutte le volte**. Uno stimatore che non si muove quando i dati si muovono non è uno stimatore, ed è **esattamente ciò che la prova del Task 4 misura**: `'rado'` sarebbe stato bocciato per un difetto di contabilità invece che per la sua idea;
> 2. **il ripiego non poteva scattare.** Il caso di prova «semicrome piene» e il criterio `minimo >= RIPIEGO_RADO * medio` si contraddicevano: dati esatti sulla griglia collassano tutti su una fase sola, quindi il minimo è 0 comunque e il ripiego non scatta mai;
> 3. **la regola che doveva fissare `LARGHEZZA_RADO` non decideva.** Misurata su 118 voci del corpus jazz, la colonna «voci che si muovono oltre 1 tick» fa **35 → 25 → 36** per larghezze 2 → 3 → 4: non-monotona, nessun pianoro. L'implementatore ha fatto la cosa giusta e **non ha inventato uno spareggio**.
>
> Il criterio nuovo — **il centro dell'arco vuoto più largo** — li chiude tutti e tre insieme: trasla coi dati (rampa di pendenza 1, verificata), dà spostamento **esattamente 0** sulle semicrome piene per costruzione, e **non ha nessun parametro** da fissare.

**Files:**
- Modify: `tools/delugexml/groove.py` (`_vuoto_piu_largo`, il ramo `'rado'` di `spostamento_del_taglio`, il limite nel docstring di `Passo`)
- Modify: `tools/delugexml/musica.py` (`applica_groove()` riferisce le collisioni)
- Modify: `tools/misura_groove.py` (`_dritte_della_voce`, `il_vuoto_delle_voci`, e la chiamata in `main()`)
- Test: `tests/test_all.py`

**Interfaces:**
- Consumes: `groove.spostamento_del_taglio(dritte, passo_tick, modo)`, `groove.TAGLI`.
- Produces: `groove._vuoto_piu_largo(posizioni, passo: float) -> tuple[float, float, float]` che ritorna `(centro del vuoto, sua larghezza, buco medio)`; il ramo `'rado'` di `spostamento_del_taglio()`; `musica.applica_groove()` che ritorna anche `'collisioni': list[int]`.
- **Non produce nessuna costante.** `LARGHEZZA_RADO` e `RIPIEGO_RADO` non esistono: se sono già nel working tree da una stesura precedente, **vanno tolti**, insieme a `_piu_rado()` e a `la_sensibilita_del_rado()`.

- [ ] **Step 1: Scrivere il test che fallisce**

```python
def test_groove_taglio_rado():
    """`'rado'` taglia nel mezzo del vuoto, e sulle voci piene non taglia.

    Quattro casi, e il quarto e' quello che conta: uno stimatore deve
    SEGUIRE i dati. I valori attesi sono misurati, non dedotti.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0
    # (a) lo stesso gesto del taglio "voce": anticipo di 14 tick sui passi
    # 4 e 12, dispersione 3. Le fasi sono 7, 9, 11 e 13; il vuoto piu'
    # largo va da 13 a 31, largo 18, e il suo centro cade a 22.
    posizioni = [float(b * 384 + base + d)
                 for b in range(12) for base in (82, 274)
                 for d in (-3, -1, 1, 3)]
    colpi = {'charleston a pedale': [(p, 90) for p in posizioni]}
    rado = GR.profilo_da_colpi(colpi, ppq, taglio='rado')
    celle = {p.passo: p for p in rado.passi['charleston a pedale']
             if p.colpi >= 10}
    check('con "rado" il gesto sta in due celle sole', len(celle) == 2,
          str(sorted(celle)))
    check('e ognuna porta tutti i colpi del suo gesto',
          all(v.colpi == 48 for v in celle.values()),
          str({k: v.colpi for k, v in sorted(celle.items())}))
    sp = GR.spostamento_del_taglio(posizioni, 24.0, 'rado')
    check('lo spostamento e il centro del vuoto meno mezzo passo: +10',
          abs(sp - 10.0) < 1e-9, f'{sp:.3f}')

    # (b) una voce di semicrome PIENE, tutte esattamente sulla griglia.
    # ⚠️ NON e' il caso "densita' piatta": le fasi collassano tutte su
    # ZERO, cioe' e' il caso piu' CONCENTRATO che esista. Il vuoto piu'
    # largo e' allora l'intero passo, il suo centro cade a mezzo passo dai
    # colpi, e lo spostamento esce zero -- che e' giusto, perche' su una
    # voce gia' sulla griglia non c'e' niente da spostare.
    piene = [float(b * 384 + k * 24) for b in range(12) for k in range(16)]
    check('su semicrome sulla griglia "rado" non sposta niente',
          GR.spostamento_del_taglio(piene, 24.0, 'rado') == 0.0,
          str(GR.spostamento_del_taglio(piene, 24.0, 'rado')))
    centro, largo, medio = GR._vuoto_piu_largo(piene, 24.0)
    check('e il vuoto misurato e un passo intero', abs(largo - 24.0) < 1e-9,
          f'centro {centro} largo {largo} medio {medio}')

    # (c) le stesse semicrome con un jitter di +-2 tick: il vuoto resta
    # largo 20 e centrato a 12, quindi ancora nessuno spostamento.
    sporche = [float(b * 384 + k * 24 + (k % 5) - 2)
               for b in range(12) for k in range(16)]
    check('e nemmeno su semicrome con jitter di +-2 tick',
          GR.spostamento_del_taglio(sporche, 24.0, 'rado') == 0.0,
          str(GR.spostamento_del_taglio(sporche, 24.0, 'rado')))

    # (d) ⚠️ LA COSA CHE UNO STIMATORE DEVE SAPER FARE: seguire i dati.
    # Traslando la voce di delta, il taglio si sposta di delta. Avvolge a
    # +-mezzo passo perche' una fase vive su un cerchio, e l'avvolgimento
    # NON e' un salto: sposta anche il passo, quindi la posizione
    # dichiarata resta continua (e' il motivo per cui il Task 4 appaia le
    # celle per posizione dichiarata e non per numero di passo).
    for d in (-8, -6, -4, -2, 2, 4, 6, 8):
        atteso = ((10.0 + d + 12.0) % 24.0) - 12.0
        ottenuto = GR.spostamento_del_taglio(
            [p + d for p in posizioni], 24.0, 'rado')
        check(f'traslando la voce di {d:+d} il taglio si sposta di {d:+d}',
              abs(ottenuto - atteso) < 1e-9,
              f'atteso {atteso:+.2f}, ottenuto {ottenuto:+.2f}')

    # (e) il limite del residuo, che si e' allargato: con un taglio
    # spostato il residuo non sta piu' dentro mezzo passo, ma resta dentro
    # UN passo.
    for taglio in GR.TAGLI:
        p = GR.profilo_da_colpi(colpi, ppq, taglio=taglio)
        peggio = max(abs(s.scarto) for v in p.passi.values() for s in v)
        check(f'taglio {taglio!r}: |scarto| <= un passo intero',
              peggio <= 24.0 + 1e-9, f'{peggio:.3f}')
```

- [ ] **Step 2: Eseguire il test e verificare che fallisca**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "rado|^[0-9]+/"`

Expected: FAIL — `GR._vuoto_piu_largo` non esiste, e il ramo `'rado'` di `spostamento_del_taglio()` o non c'è o è quello vecchio.

- [ ] **Step 3: Implementare `_vuoto_piu_largo()` e il ramo `'rado'`**

⚠️ Se `LARGHEZZA_RADO`, `RIPIEGO_RADO` o `_piu_rado()` esistono già nel file da una stesura precedente, **si tolgono**: non sono più parte del disegno, e lasciarli sarebbe lasciare in giro un criterio che questa sezione documenta come sbagliato.

Sopra `spostamento_del_taglio()`:

```python
def _vuoto_piu_largo(posizioni, passo: float) -> tuple[float, float, float]:
    """L'arco di fase piu' VUOTO di una voce: (centro, larghezza, buco medio).

    Il centro sta in [0, passo). La larghezza e' il buco piu' grande fra due
    colpi consecutivi, CIRCOLARMENTE. Il buco medio e' `passo / n`, cioe'
    quanto varrebbe ogni buco se i colpi fossero sparsi in modo piatto: non
    serve a decidere niente qui, serve a `misura_groove.py` per dire se quel
    vuoto e' un vuoto VERO o solo il piu' largo di tanti uguali.

    ⚠️ IL CENTRO, NON IL PRIMO PUNTO VUOTO, e la ragione e' misurata il 26
    agosto 2026. Una prima stesura cercava il minimo di densita' dentro una
    finestra e ne prendeva l'argmin. Ma quel minimo e' un ALTOPIANO -- un
    arco intero senza colpi -- e l'argmin ne prendeva il primo punto della
    scansione, che sta sempre a fase 0. Ne usciva un taglio INCOLLATO:
    traslando la voce di -4, -2, 0, +2, +4 tick lo spostamento restava
    -12,00 tutte le volte. Il centro del vuoto invece trasla coi dati, e la
    stessa prova da' una rampa di pendenza 1.

    ⚠️ IL BUCO CHE GIRA VA CONTATO A PARTE. Con tutti i colpi sulla stessa
    fase i buchi fra consecutivi sono zero, e `(fasi[0] - fasi[-1]) % passo`
    darebbe zero anche per quello che avvolge: una voce perfettamente sulla
    griglia uscirebbe con vuoto ZERO invece che con vuoto MASSIMO, cioe' il
    rovescio esatto. Si calcola come `passo - (fasi[-1] - fasi[0])`.
    """
    fasi = sorted(p % passo for p in posizioni)
    if not fasi:
        return 0.0, 0.0, 0.0
    buchi = [fasi[i + 1] - fasi[i] for i in range(len(fasi) - 1)]
    buchi.append(passo - (fasi[-1] - fasi[0]))
    i = max(range(len(fasi)), key=lambda k: buchi[k])
    return (fasi[i] + buchi[i] / 2) % passo, buchi[i], passo / len(fasi)
```

e nel corpo di `spostamento_del_taglio()`, al posto del `raise` finale:

```python
    if modo == 'rado':
        centro, largo, _ = _vuoto_piu_largo(dritte, passo_tick)
        if largo <= 0:
            return 0.0                  # nessun colpo: niente da spostare
        # il taglio di `round()` cade a meta' fra due passi: portarlo sul
        # centro del vuoto vuol dire spostarlo di (centro - mezzo passo).
        return centro - passo_tick / 2
```

⚠️ **Nessun ripiego, ed è una scelta dichiarata.** Il criterio non ha soglie da tarare. Se il vuoto più largo fosse largo quanto gli altri il suo centro sarebbe arbitrario — ma se serva un ripiego lo dice il corpus, non un'ipotesi: lo misura lo Step 6.

- [ ] **Step 4: Allargare il limite nel docstring di `Passo`**

In `class Passo`, sotto la riga del segno, aggiungere:

```python
    #: ⚠️ IL LIMITE SI E' ALLARGATO, il 26 agosto 2026. Con `taglio='vicino'`
    #: il passo e' il piu' VICINO, quindi |scarto| <= mezzo passo (12 tick)
    #: per costruzione. Con un taglio spostato non e' piu' vero: uno scarto
    #: puo' arrivare fino a UN PASSO INTERO, ed e' voluto -- e' l'unico modo
    #: di dire "anticipa di mezza semicroma" invece di dire "e' in ritardo
    #: sul passo prima". Ne segue che `applica_groove()` puo' posare una nota
    #: nel territorio del passo accanto.
```

- [ ] **Step 5: Il rapporto di `applica_groove()` dice le collisioni**

Uno scarto che arriva a un passo intero può posare **due note sullo stesso tick**: un pattern con un colpo sul passo 3 (scarto +12) e uno sul 4 (scarto −12) li manda tutt'e due a 84. Il Deluge non lo vieta, ma un'operazione silenziosa non è correggibile.

Il test, in `tests/test_all.py`:

```python
def test_applica_groove_dice_le_collisioni():
    """Due note su passi adiacenti possono finire sullo stesso tick.

    ⚠️ Diventato possibile il 26 agosto 2026, quando lo scarto ha smesso di
    stare dentro mezzo passo. Non e' vietato -- il Deluge lo accetta -- ma
    va DETTO: un'operazione silenziosa non e' correggibile.
    """
    from delugexml import groove as GR                      # noqa: PLC0415
    from delugexml import musica as MU                      # noqa: PLC0415

    prof = GR.Profilo(
        id='finto/3', drummer='drummerX', style='jazz', bpm=120, bur=1.6,
        battute=1,
        passi={'kick': [GR.Passo(passo=3, velocity=100, scarto=12.0, colpi=20),
                        GR.Passo(passo=4, velocity=100, scarto=-12.0,
                                 colpi=20)]})
    note = MU.passi('...xx...........')
    r = MU.applica_groove(note, prof, dove='kick')
    check('le due note finiscono sullo stesso tick',
          note[0].pos == note[1].pos, f'{note[0].pos} {note[1].pos}')
    check('e il rapporto lo dice', r['collisioni'] == [note[0].pos],
          str(r.get('collisioni')))

    # e quando non c'e' collisione, la lista e' vuota: non si allarma a vuoto
    prof2 = GR.Profilo(
        id='finto/4', drummer='drummerX', style='jazz', bpm=120, bur=1.6,
        battute=1,
        passi={'kick': [GR.Passo(passo=3, velocity=100, scarto=0.0, colpi=20),
                        GR.Passo(passo=4, velocity=100, scarto=0.0,
                                 colpi=20)]})
    r2 = MU.applica_groove(MU.passi('...xx...........'), prof2, dove='kick')
    check('senza collisioni la lista e vuota', r2['collisioni'] == [],
          str(r2['collisioni']))
```

Eseguirlo e verificare che fallisca (`KeyError: 'collisioni'`). Poi, in `tools/delugexml/musica.py`, in fondo a `applica_groove()`, prima del `return`:

```python
    # ⚠️ DAL 26 AGOSTO 2026 due note possono finire sullo stesso tick: uno
    # scarto puo' arrivare a un passo intero, quindi il passo 3 in ritardo e
    # il 4 in anticipo si incontrano. Il Deluge lo accetta e non e' un
    # errore, ma va riferito -- e' la regola 4, un'operazione silenziosa non
    # e' correggibile.
    quante: dict[int, int] = {}
    for n in note:
        quante[n.pos] = quante.get(n.pos, 0) + 1
    collisioni = sorted(p for p, q in quante.items() if q > 1)
```

e aggiungere `'collisioni': collisioni` al dizionario ritornato. Aggiornare il docstring di `applica_groove()` nominando il campo nuovo.

Rieseguire la suite: tutti PASS.

- [ ] **Step 6: Misurare se il vuoto è un vuoto vero**

⚠️ **Se `la_sensibilita_del_rado()` esiste già in `tools/misura_groove.py` da una stesura precedente, si toglie** — misurava la sensibilità a una finestra che non esiste più — e si toglie la sua chiamata da `main()`. `_dritte_della_voce()` invece **resta**: serve anche qui.

`'rado'` non ha più nessun parametro da fissare. Resta una domanda che solo il corpus può chiudere: quel vuoto è sempre un vuoto **vero**? Su una voce i cui colpi fossero sparsi in modo piatto sulla fase, il buco più largo sarebbe largo quanto gli altri e il suo centro arbitrario — e uno spostamento arbitrario riassegnerebbe i passi in blocco.

In `tools/misura_groove.py`, la funzione ausiliaria (se non c'è già):

```python
def _dritte_della_voce(e, nome, colpi=None) -> list[float]:
    """Le posizioni DRITTE di una voce: origine tolta, swing tolto.

    Rifa' la prima passata di `GR.profilo_da_colpi()` per poter interrogare
    i tagli senza passare da un `Profilo` gia' aggregato. `colpi` si passa
    quando si interrogano piu' voci della stessa esecuzione, per non
    rileggere il file MIDI una volta per voce.
    """
    c = _colpi(e) if colpi is None else colpi
    tutte = [p for v in c.values() for p, _ in v]
    off = GR.origine(tutte, PPQ / 4)
    bur = GR.bur_da_posizioni([p - off for p in tutte], PPQ)
    lev = da_bur(bur) if bur is not None else 0.5
    fuori = []
    for pos, _ in c.get(nome, []):
        p = pos - off
        mov, resto = divmod(p, PPQ)
        fuori.append((mov + GR._senza_swing(resto / PPQ, lev)) * PPQ)
    return fuori
```

e la misura:

```python
def il_vuoto_delle_voci():
    """Quanto e' netto il vuoto su cui `'rado'` mette il taglio.

    ⚠️ PERCHE' ESISTE, e cosa NON fa. `'rado'` non ha parametri: il centro
    del vuoto piu' largo e' una grandezza geometrica, non una taratura.
    Resta pero' una domanda che solo il corpus chiude: se il buco piu'
    largo fosse largo quanto gli altri, il suo centro sarebbe arbitrario e
    lo spostamento riassegnerebbe i passi in blocco.

    Questa sezione misura il rapporto `largo / medio` -- quanto il buco piu'
    largo supera quello che ci sarebbe se i colpi fossero sparsi piatti.
    NON decide niente: se quel rapporto stesse vicino a 1 su molte voci,
    servirebbe un ripiego, e sarebbe una decisione da prendere, non da
    inventare qui.
    """
    print('\n=== il vuoto su cui "rado" taglia: e un vuoto vero? ===')
    rapporti, spostamenti = [], []
    esecuzioni, batteristi = 0, set()
    for e in GR.elenco(BASE, style=STILE, beat_type='beat',
                       time_signature='4-4'):
        if e.style in FUORI_DALLO_SWING:
            continue
        c = _colpi(e)
        esecuzioni += 1
        batteristi.add(e.drummer)
        for nome in sorted(c):
            dritte = _dritte_della_voce(e, nome, colpi=c)
            if len(dritte) < 40:
                continue
            centro, largo, medio = GR._vuoto_piu_largo(dritte, PPQ / 4)
            if medio <= 0:
                continue
            rapporti.append(largo / medio)
            spostamenti.append(abs(centro - PPQ / 8))
    r = sorted(rapporti)
    q = statistics.quantiles(r, n=4)
    print(f'    {esecuzioni} esecuzioni, {len(batteristi)} batteristi, '
          f'{len(r)} voci con almeno 40 colpi')
    print(f'    largo/medio : min {r[0]:.1f}  q1 {q[0]:.1f}  '
          f'mediana {statistics.median(r):.1f}  q3 {q[2]:.1f}  '
          f'max {r[-1]:.1f}')
    for soglia in (1.5, 2.0, 3.0, 5.0):
        n = sum(1 for x in r if x < soglia)
        print(f'    voci col vuoto meno di {soglia:.1f} volte il medio: '
              f'{n:3d} su {len(r)}  ({100 * n / len(r):.1f}%)')
    s = sorted(spostamenti)
    print(f'    |spostamento| : mediana {statistics.median(s):.2f} tick, '
          f'q3 {s[int(len(s) * 0.75)]:.2f}, massimo {max(s):.2f}')
```

Aggiungere `il_vuoto_delle_voci()` in `main()`, subito dopo `il_bordo_del_passo()`.

Run: `.venv/Scripts/python.exe tools/misura_groove.py > out/groove_jazz.txt 2>&1` e leggere la sezione. **La lettura si riporta nel rapporto**, non si agisce: se il rapporto mediano fosse basso (vicino a 1,5 o meno), è una cosa da riferire, non da riparare qui.

- [ ] **Step 7: Eseguire tutta la suite**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | tail -5`

Expected: tutti PASS, totale = quello del Task 2 (956) + 17.

- [ ] **Step 8: Commit**

```bash
git add tools/delugexml/groove.py tools/delugexml/musica.py tools/misura_groove.py tests/test_all.py
git commit -m "groove: il taglio 'rado' taglia nel mezzo del vuoto, e segue i dati

Il criterio del minimo di densita' si incollava: il minimo e' un altopiano e
l'argmin ne prendeva il primo punto della scansione, sempre a fase 0.
Traslando la voce di -4, -2, 0, +2, +4 lo spostamento restava -12,00 tutte
le volte -- uno stimatore che non si muove quando i dati si muovono.

Il centro del vuoto piu' largo trasla coi dati, da' spostamento zero sulle
voci gia' sulla griglia per costruzione, e non ha nessun parametro da
tarare: spariscono LARGHEZZA_RADO, RIPIEGO_RADO e la regola del pianoro che
sui 118 voci del corpus non decideva (35 -> 25 -> 36, non-monotona).

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 4: La prova che decide — linearità sotto traslazione per voce

**Il criterio:** uno stimatore è uno stimatore se la sua risposta **segue la cosa che misura**. Si trasla **una voce sola** di δ tick e si richiede che la posizione dichiarata da quella voce si muova di δ.

**Files:**
- Modify: `tools/delugexml/groove.py` (`profilo_da_colpi`: due parametri per congelare)
- Modify: `tools/misura_groove.py` (`la_prova_di_traslazione`, e la chiamata in `main()`)
- Test: `tests/test_all.py`

**Interfaces:**
- Consumes: `groove.profilo_da_colpi(colpi, ppq, *, ..., taglio)`.
- Produces: `groove.profilo_da_colpi(..., origine_fissa: float | None = None, levare_fisso: float | None = None)`.

⚠️ **La trappola di questa misura.** Traslare una voce sola muove **anche** `origine()` del kit, di circa `δ · (colpi della voce / colpi totali)`, e per la stessa ragione può muovere il BUR. Chi non lo neutralizza misura *anche quello* e conclude che nessuno stimatore è lineare. **Origine e levare si congelano ai valori di δ = 0.**

⚠️ **E le celle vanno appaiate per posizione dichiarata, non per numero di passo.** Uno stimatore che ripiega **sposta un gesto da una cella all'altra**: appaiando per `k` si confronterebbero due popolazioni diverse sotto la stessa etichetta.

- [ ] **Step 1: Scrivere il test che fallisce**

```python
def test_groove_congelare_origine_e_levare():
    """`profilo_da_colpi()` sa accettare origine e levare dall'esterno.

    ⚠️ Serve alla prova di traslazione per voce: traslando UNA voce si
    muove anche l'origine del KIT, di circa delta per la quota di colpi di
    quella voce. Chi non la congela misura anche quello.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0
    colpi = {
        'kick': [(float(b * 384 + m * 96), 100) for b in range(8)
                 for m in (0, 2)],
        'ride': [(float(b * 384 + m * 96), 80) for b in range(8)
                 for m in range(4)],
    }
    base = GR.profilo_da_colpi(colpi, ppq)
    check('senza congelare, il BUR resta None su colpi tutti sui battere',
          base.bur is None, str(base.bur))

    # tutto il kit spostato di +5: l'origine se lo mangia, il profilo non
    # si muove.
    spostato = {n: [(p + 5.0, v) for p, v in note] for n, note in colpi.items()}
    check('una traslazione COMUNE la riassorbe origine()',
          GR.profilo_da_colpi(spostato, ppq).passi == base.passi)

    # una voce sola spostata di +5: l'origine si muove, ed e' l'artefatto.
    una = dict(colpi)
    una['ride'] = [(p + 5.0, v) for p, v in colpi['ride']]
    libero = GR.profilo_da_colpi(una, ppq)
    congelato = GR.profilo_da_colpi(una, ppq, origine_fissa=0.0,
                                    levare_fisso=0.5)
    k_libero = {p.passo: p.scarto for p in libero.passi['kick']}
    k_congelato = {p.passo: p.scarto for p in congelato.passi['kick']}
    check('senza congelare, il kick NON TRASLATO si muove lo stesso',
          any(abs(k_libero[k]) > 0.01 for k in k_libero),
          str({k: round(v, 2) for k, v in sorted(k_libero.items())}))
    check('congelando, il kick non traslato resta fermo',
          all(abs(v) < 1e-9 for v in k_congelato.values()),
          str({k: round(v, 2) for k, v in sorted(k_congelato.items())}))
    check('e il ride traslato si muove di esattamente +5',
          all(abs(p.scarto - 5.0) < 1e-9
              for p in congelato.passi['ride']),
          str([round(p.scarto, 2) for p in congelato.passi['ride']]))
```

- [ ] **Step 2: Eseguire il test e verificare che fallisca**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "congelare|^[0-9]+/"`

Expected: FAIL con `TypeError: ... unexpected keyword argument 'origine_fissa'`.

- [ ] **Step 3: Implementare il congelamento**

Firma:

```python
def profilo_da_colpi(colpi: dict[str, list[tuple[float, int]]], ppq: float,
                     *, id: str = '', drummer: str = '', style: str = '',
                     bpm: int = 0, taglio: str = 'vicino',
                     origine_fissa: float | None = None,
                     levare_fisso: float | None = None) -> Profilo:
```

e le due righe che le calcolano:

```python
    # ⚠️ ORIGINE E LEVARE SI POSSONO CONGELARE, e serve a una cosa sola:
    # la prova di traslazione per voce. Traslando UNA voce si muove anche
    # l'origine del KIT, di circa delta per la quota di colpi di quella
    # voce, e chi non la congela misura anche quell'artefatto invece dello
    # stimatore. Fuori da quella prova NON si passano: una stima congelata
    # e' una stima che non guarda i dati.
    off = origine(tutte, passo_tick) if origine_fissa is None else origine_fissa

    if levare_fisso is None:
        bur = bur_da_posizioni([p - off for p in tutte], ppq)
        levare = da_bur(bur) if bur is not None else 0.5
    else:
        bur = in_bur(levare_fisso)
        levare = levare_fisso
```

⚠️ `in_bur` è già importata in cima al modulo (`from .musica import da_bur, in_bur`): non aggiungere import.

- [ ] **Step 4: Scrivere `la_prova_di_traslazione()`**

In `tools/misura_groove.py`, prima di `def main()`:

```python
#: Di quanto si trasla una voce sola, in tick, nella prova di linearita'.
#: Fino a 8 su un passo da 24: oltre un terzo di passo la domanda cambia --
#: non e' piu' "lo stimatore segue?" ma "quale passo e' quello giusto?".
DELTA = (-8, -6, -4, -2, 0, 2, 4, 6, 8)


def la_prova_di_traslazione():
    """Uno stimatore e' uno stimatore se la sua risposta SEGUE i dati.

    ⚠️ E' LA MISURA CHE DECIDE il default di `GR.TAGLI`, ed e' scelta il 26
    agosto 2026 CONTRO due criteri piu' ovvi. L'errore di ricostruzione per
    inversione premia lo stimatore rotto -- spezzare un gesto in due celle
    rende ciascuna delle due mediane piu' stretta, quindi l'errore SCENDE. E
    la tenuta delle conclusioni della casella 6 come bersaglio sarebbe
    fabbricare la conclusione, che e' il difetto della finestra di grazia.

    ⚠️ ORIGINE E LEVARE SI CONGELANO ai valori di delta = 0: traslando una
    voce sola si muove anche l'origine del kit, e chi non lo neutralizza
    misura quell'artefatto e conclude che nessuno stimatore e' lineare.

    ⚠️ LE CELLE SI APPAIANO PER POSIZIONE DICHIARATA, non per numero di
    passo. E' il punto: uno stimatore che ripiega SPOSTA un gesto da una
    cella all'altra, quindi `k` cambia mentre il gesto e' lo stesso.
    Appaiare per `k` confronterebbe due popolazioni diverse sotto la stessa
    etichetta.
    """
    print('\n=== la prova di traslazione per voce: lo stimatore segue? ===')
    print(f'    delta provati: {DELTA} tick su un passo da {PPQ/4:.0f}')
    esiti = {t: {'pendenze': [], 'salti': [], 'voci': 0} for t in GR.TAGLI}
    esecuzioni, batteristi = 0, set()
    for e in GR.elenco(BASE, style=STILE, beat_type='beat',
                       time_signature='4-4'):
        if e.style in FUORI_DALLO_SWING:
            continue
        c = _colpi(e)
        tutte = [p for v in c.values() for p, _ in v]
        off0 = GR.origine(tutte, PPQ / 4)
        bur0 = GR.bur_da_posizioni([p - off0 for p in tutte], PPQ)
        lev0 = da_bur(bur0) if bur0 is not None else 0.5
        esecuzioni += 1
        batteristi.add(e.drummer)
        for nome in sorted(c):
            if len(c[nome]) < 40:
                continue
            for taglio in GR.TAGLI:
                dichiarate = {}
                for d in DELTA:
                    mosso = dict(c)
                    mosso[nome] = [(p + d, v) for p, v in c[nome]]
                    p = GR.profilo_da_colpi(
                        mosso, PPQ, taglio=taglio,
                        origine_fissa=off0, levare_fisso=lev0)
                    dichiarate[d] = sorted(
                        s.passo * PPQ / 4 + s.scarto
                        for s in p.passi.get(nome, []) if s.colpi >= 10)
                base = dichiarate[0]
                if not base:
                    continue
                esiti[taglio]['voci'] += 1
                # appaiamento per posizione dichiarata piu' vicina a delta=0
                mosse = []
                for d in DELTA:
                    if d == 0:
                        continue
                    scarti = [min(dichiarate[d], key=lambda x: abs(x - b)) - b
                              for b in base] if dichiarate[d] else []
                    if scarti:
                        mosse.append((d, statistics.median(scarti)))
                if len(mosse) < 2:
                    continue
                # pendenza per minimi quadrati passanti per l'origine
                num = sum(d * m for d, m in mosse)
                den = sum(d * d for d, _ in mosse)
                pend = num / den if den else 0.0
                esiti[taglio]['pendenze'].append(pend)
                esiti[taglio]['salti'].append(max(abs(m - d) for d, m in mosse))
    print(f'    {esecuzioni} esecuzioni, {len(batteristi)} batteristi')
    print(f'    {"taglio":10s} {"voci":>5s} {"pendenza mediana":>18s} '
          f'{"scarto max mediano":>20s} {"voci con un salto >= 12 tick":>30s}')
    for taglio in GR.TAGLI:
        v = esiti[taglio]
        if not v['pendenze']:
            continue
        print(f'    {taglio:10s} {v["voci"]:5d} '
              f'{statistics.median(v["pendenze"]):18.3f} '
              f'{statistics.median(v["salti"]):20.2f} '
              f'{sum(1 for s in v["salti"] if s >= PPQ / 8):30d}')
```

Aggiungere `la_prova_di_traslazione()` in `main()`, subito dopo `il_vuoto_delle_voci()`.

- [ ] **Step 5: Eseguire la misura e leggerla**

Run: `.venv/Scripts/python.exe tools/misura_groove.py > out/groove_jazz.txt 2>&1` e leggere la sezione.

Expected: `'vicino'` mostra pendenza sotto 1 e salti grandi su una parte delle voci; almeno uno dei due candidati mostra pendenza vicina a 1 e salti piccoli. **Se tutti e tre danno pendenza 1 e nessun salto, la misura è rotta** — il primo posto da guardare è il congelamento (Step 3) e il secondo l'appaiamento.

- [ ] **Step 6: Eseguire tutta la suite**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | tail -5`

Expected: tutti PASS, totale = quello del Task 3 + 5.

- [ ] **Step 7: Commit**

```bash
git add tools/delugexml/groove.py tools/misura_groove.py tests/test_all.py
git commit -m "groove: la prova di traslazione per voce, e le sue due trappole

Uno stimatore e' uno stimatore se la sua risposta segue i dati. Traslando una
voce sola si muove anche l'origine del kit: si congela. E le celle si
appaiano per posizione dichiarata, non per numero di passo, perche' e'
proprio spostare un gesto da una cella all'altra quel che si sta misurando.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 5: L'ancoraggio — misurarlo prima di decidere se serve

⚠️ **Questo task è un'aggiunta trovata scrivendo il piano, e non sta nella spec.** Costruendo il caso sintetico del Task 2 è venuto fuori che `'voce'` e `'rado'` chiudono la **spaccatura** ma non decidono l'**ancoraggio**: un gesto centrato 14 tick prima del passo 4 finisce, con tutt'e due, in una cella sola **sul passo 3** con scarto +10. Dai dati soli i due non si distinguono — «14 tick prima del passo 4» e «10 tick dopo il passo 3» sono la stessa cosa. A distinguerli è il **metro**, non la misura.

Conta perché `applica_groove()` cerca la cella del passo che il **pattern** chiede: se il pattern chiede il passo 4 e il profilo ha solo il 3, la nota finisce in `senza_appoggio` e il template non si applica **proprio al gesto che questo lavoro ha appena riparato**.

**Ma sul corpus vero il problema potrebbe non esserci:** nella sonda del 26 agosto `'voce'` su `drummer10/session1/1` ha ancorato correttamente sul 4 (50 colpi) e non sul 3 (20). Quindi **prima si misura quanto è frequente, poi si decide se serve una regola.** YAGNI: se il conteggio è zero, la regola non si scrive e il fatto si documenta.

⚠️ **Questo task misura e riferisce, e non tocca la libreria.** Se il conteggio non è zero, la forma della regola è una decisione di disegno nuova — vedi lo Step 3 — e va riportata, non inventata.

**Files:**
- Modify: `tools/misura_groove.py` (`l_ancoraggio`, e la chiamata in `main()`)

**Interfaces:**
- Consumes: `groove.profilo(base, id, *, taglio)`, `groove.TAGLI`.
- Produces: niente di codice. Produce **un numero e una decisione da prendere**.

- [ ] **Step 1: Scrivere la misura**

In `tools/misura_groove.py`, prima di `def main()`:

```python
def l_ancoraggio():
    """Quante celle finiscono ancorate sul passo DEBOLE accanto a un battere.

    ⚠️ PERCHE' ESISTE. `'voce'` e `'rado'` chiudono la spaccatura di un gesto
    ma non decidono su QUALE passo ancorarlo: dai dati soli "14 tick prima
    del passo 4" e "10 tick dopo il passo 3" sono la stessa cosa. Conta
    perche' `applica_groove()` cerca la cella del passo che il PATTERN
    chiede: ancorato sul 3, un pattern che chiede il 4 non trova niente.

    Il conteggio: celle forti (>= 10 colpi) su un passo DISPARI adiacente a
    un battere (0, 4, 8, 12), con scarto positivo oltre mezzo passo -- cioe'
    celle che dicono "molto in ritardo su un passo debole" dove la lettura
    musicale sarebbe "in anticipo sul battere".
    """
    print('\n=== l ancoraggio: celle sul passo debole accanto a un battere ===')
    conta = {t: {} for t in GR.TAGLI}
    esecuzioni, batteristi = 0, set()
    for e in GR.elenco(BASE, style=STILE, beat_type='beat',
                       time_signature='4-4'):
        if e.style in FUORI_DALLO_SWING:
            continue
        esecuzioni += 1
        batteristi.add(e.drummer)
        for taglio in GR.TAGLI:
            p = GR.profilo(BASE, e.id, taglio=taglio)
            for nome, passi in p.passi.items():
                if sum(s.colpi for s in passi) < 40:
                    continue
                for s in passi:
                    if (s.colpi >= 10 and (s.passo + 1) % 16 in (0, 4, 8, 12)
                            and s.scarto > PPQ / 8):
                        conta[taglio][nome] = conta[taglio].get(nome, 0) + 1
    print(f'    {esecuzioni} esecuzioni, {len(batteristi)} batteristi')
    for taglio in GR.TAGLI:
        tot = sum(conta[taglio].values())
        detta = '  '.join(f'{n}:{k}' for n, k in
                          sorted(conta[taglio].items(), key=lambda kv: -kv[1]))
        print(f'    {taglio:10s} celle mal ancorate: {tot:3d}   {detta}')
```

Aggiungere `l_ancoraggio()` in `main()`, subito dopo `la_prova_di_traslazione()`.

- [ ] **Step 2: Eseguire la misura e leggerla**

Run: `.venv/Scripts/python.exe tools/misura_groove.py > out/groove_jazz.txt 2>&1` e leggere la sezione.

- [ ] **Step 3: Riferire, e fermarsi se il conteggio non e' zero**

**Se il conteggio sul taglio candidato e' 0**: la regola non serve, e non si
scrive. Si annota il conteggio **con la data** nel docstring di
`l_ancoraggio()`, si scrive che il fenomeno esiste solo nel caso sintetico del
Task 2, e si va allo Step 4. YAGNI: una regola che non ha casi e' una regola
che non ha nemmeno un modo di essere sbagliata visibilmente.

**Se il conteggio e' maggiore di 0**: ⚠️ **ci si ferma e si riferisce.** La
forma della regola e' una decisione di disegno nuova, che non sta nella spec e
che l'implementatore non deve inventare. Il motivo, e va riportato insieme al
conteggio perche' e' la parte che serve a decidere:

> Il gesto sintetico del Task 2 sta a 82 tick. Il passo 3 e' a 72, il passo 4
> a 96: il gesto e' **piu' vicino al passo 3** (10 tick) che al 4 (14).
> Nessuna regola di **distanza** puo' quindi preferire il battere — sarebbe
> `round()` al contrario. A dire «e' il 2, anticipato» c'e' solo il **metro**,
> e quanto pesarlo contro la distanza e' precisamente cio' che va deciso.

Una prima stesura di questo piano conteneva una regola —
`if (passo + 1) % 16 in (0, 4, 8, 12) and dritta > passo * passo_tick` — e
**era sbagliata**: avrebbe spostato al battere qualunque colpo appena in
ritardo sul passo debole, mandando una nota a 73 tick sul passo 4 con scarto
−23. E' registrata qui perche' e' l'errore che chiunque riprovi fara' per
primo.

Cosa riferire: il conteggio per taglio e per voce, quali esecuzioni, e se le
celle mal ancorate stanno tutte su una voce sola o sono sparse. Con quei
numeri la decisione si prende, e diventa un task suo.

- [ ] **Step 4: Eseguire tutta la suite**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | tail -5`

Expected: tutti PASS, totale invariato rispetto al Task 4 — questo task
**non aggiunge codice di libreria**, solo una misura.

- [ ] **Step 5: Commit**

```bash
git add tools/misura_groove.py
git commit -m "groove: l'ancoraggio, misurato prima di decidere se serve una regola

I due tagli chiudono la spaccatura ma non dicono su quale passo ancorare un
gesto: dai dati soli \"14 tick prima del 4\" e \"10 dopo il 3\" sono la stessa
cosa, e il gesto e' pure piu' VICINO al 3. Nessuna regola di distanza puo'
preferire il battere: a dirlo c'e' solo il metro.

Conta perche' applica_groove() cerca il passo che il pattern chiede: ancorato
sul 3, un pattern che chiede il 4 non trova niente e finisce in
senza_appoggio.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 6: Scegliere il default, e raccogliere le conseguenze

**Files:**
- Modify: `tools/delugexml/groove.py` (il default di `taglio` in `profilo_da_colpi` e `profilo`)
- Modify: `tools/misura_groove.py` (`il_bordo_del_passo` gira sui tre tagli)
- Test: `tests/test_all.py`

**Interfaces:**
- Consumes: le misure dei Task 4 e 5.
- Produces: il default scelto, e `out/groove_jazz.txt` col confronto.

- [ ] **Step 1: Far girare `il_bordo_del_passo()` sui tre tagli**

In `tools/misura_groove.py`, dentro `il_bordo_del_passo()`, avvolgere il ciclo esistente in un ciclo esterno `for taglio in GR.TAGLI:`, passare `taglio=taglio` a `GR.profilo(BASE, e.id, ...)`, e stampare l'intestazione di ogni blocco. La sezione «i passi del battere, sulle esecuzioni che la scheda NOMINA» si ripete anch'essa per taglio: sono i numeri che finiscono nella scheda.

- [ ] **Step 2: Eseguire tutte le misure**

Run: `.venv/Scripts/python.exe tools/misura_groove.py > out/groove_jazz.txt 2>&1`

- [ ] **Step 3: Il default è `'voce'`, e come ci si è arrivati**

⚠️ **La scelta è già stata presa, dal proprietario del progetto, il 26 agosto 2026, e questo Step la esegue invece di rifarla.** Sta scritta qui per intero — compreso il fatto che **la regola scritta prima selezionava l'altro** — perché una decisione presa contro la propria regola va registrata come decisione, non travestita da esito della regola.

I numeri sul tavolo quando è stata presa, tutti `[MIS]` su 42 esecuzioni, 5 batteristi, 111 voci:

| | `vicino` (l'attuale) | `voce` | `rado` |
|---|---:|---:|---:|
| pendenza mediana sotto traslazione | 0,808 | **0,998** | **0,998** |
| scarto massimo mediano (tick) | 3,28 | **1,47** | 1,97 |
| voci con un salto ≥ mezzo passo | 16 / 111 | 4 / 111 | **3 / 111** |
| celle mal ancorate | 0 *(impossibile per costruzione)* | **2** | 5 |

**Cosa la misura chiude da sola, senza bisogno di nessun giudizio:** `'vicino'` non è uno stimatore. La sua risposta segue i dati per lo 0,808, contro lo 0,998 di tutt'e due i candidati, e ha **16 voci su 111** che saltano di mezzo passo contro 3 e 4. Questo è il risultato del lavoro, ed è netto.

**Cosa la misura NON chiude:** quale dei due candidati. La pendenza è pari a tre decimali.

**La regola che era stata scritta prima** diceva: scartare per pendenza, poi vincere con meno salti, poi a parità vincere con meno parametri. Applicata alla lettera seleziona **`'rado'`** — 3 salti contro 4. Il proprietario ha scelto **`'voce'`**, e le ragioni, dette per intero:

- il margine di `'rado'` è **una voce su 111**, cioè plausibilmente rumore, mentre `'voce'` vince su **due** grandezze e con margini più larghi: scarto massimo mediano 1,47 contro 1,97, e celle mal ancorate 2 contro 5;
- il **terzo criterio della regola era diventato void**: diceva «a parità vince quello con meno parametri, `'voce'` non ne ha e `'rado'` ne ha due», ma dopo la riscrittura del Task 3 nemmeno `'rado'` ne ha;
- la colonna **dell'ancoraggio non esisteva** quando la regola è stata scritta: la misura del Task 5 è nata dopo;
- `'voce'` riusa macchinario già nel modulo e già rivisto — la media circolare di `_media_versori()` — invece di aggiungere una seconda idea geometrica.

⚠️ **E la cosa che va scritta accanto, perché è il rischio che questo progetto ha già pagato una volta:** scavalcare una regola dopo aver visto i numeri è esattamente il meccanismo della finestra di grazia, dove un criterio messo per una ragione plausibile fabbricava la conclusione. Qui la differenza è che **la regola non viene riscritta per far vincere `'voce'`**: viene dichiarata insufficiente a decidere una parità che non aveva previsto, e la decisione la prende una persona, per iscritto, con tutte e quattro le colonne visibili. Chi rilegge può non essere d'accordo — e ha davanti i numeri per dirlo.

⚠️ **Il «battere in minoranza», il 43,7% e il 12 su 15 NON sono entrati in questa scelta.** Sono conseguenze: si riportano al Task 7, non decidono.

Cambiare il default a `'voce'` in `profilo_da_colpi()` e in `profilo()`, e scrivere accanto alla firma la data e il rimando a questa sezione.

- [ ] **Step 4: Aggiornare il test di neutralità**

`test_groove_taglio_neutro` confronta il default con `'vicino'`: se il default non è più `'vicino'`, quel check ora asserisce il contrario di ciò che vuole. Sostituirlo con:

```python
    check('il default e il taglio scelto il 26 agosto 2026',
          GR.profilo_da_colpi(colpi, ppq, id='finto/1')
          == GR.profilo_da_colpi(colpi, ppq, id='finto/1', taglio=SCELTO),
          SCELTO)
```

dove `SCELTO` è `'voce'`, e aggiungere sopra, nel test, il commento con la **data della scelta e la ragione in una riga**. Fare la stessa sostituzione in `test_groove_taglio_neutro_sul_corpus`.

- [ ] **Step 5: Eseguire tutta la suite**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | tail -5`

Expected: tutti PASS. ⚠️ **Se un test scritto prima di questo piano diventa rosso, non lo si aggiusta per farlo passare**: è un numero della casella 6 che si è mosso, ed è precisamente ciò che il Task 7 deve andare a riscrivere nella scheda. Si annota quale, e si va avanti.

- [ ] **Step 6: Commit**

```bash
git add tools/delugexml/groove.py tools/misura_groove.py tests/test_all.py out/
git commit -m "groove: il default e' 'voce', e la regola scritta prima diceva 'rado'

La misura chiude da sola la domanda vera: 'vicino' non e' uno stimatore,
pendenza 0,808 contro 0,998, e 16 voci su 111 che saltano di mezzo passo
contro 3 e 4. Quale dei due candidati non lo chiude: la pendenza e' pari a
tre decimali.

La regola scritta prima selezionava 'rado' per una voce su 111. Il
proprietario ha scelto 'voce', che vince su scarto massimo mediano (1,47
contro 1,97) e ancoraggio (2 celle contro 5). La sostituzione sta scritta
nel piano come decisione, non travestita da esito della regola.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

⚠️ `out/` è in `.gitignore`: se `git add out/` non aggiunge niente, va bene — il file resta come stato del disco, e i numeri si copiano a mano nella scheda al Task 7.

---

## Task 7: La scheda prende la decisione, e il punto esce dagli aperti

**Files:**
- Modify: `docs/repertori/jazz.md` (sezione «Il bordo fra due passi», e i numeri della casella 6 che si sono mossi)
- Modify: `docs/MUSICA.md` (§ «Il groove template»)
- Modify: `.claude/skills/deluge-pal/SKILL.md` (la riga di `applica_groove()`)
- Modify: `HANDOFF.md` (§7 e §6-terdecies)

- [ ] **Step 1: `jazz.md` — la casella prende la decisione**

Nella sezione «Il bordo fra due passi», sostituire il paragrafo che dice *«è una decisione di disegno che questa casella non prende: la dichiara, e la lascia a chi verrà»* con la decisione **datata 26 agosto 2026**, che deve contenere: il taglio scelto e con quale misura; la tabella del «battere in minoranza» **coi numeri vecchi accanto ai nuovi**; e la riga su cosa non si è mosso (scala di velocity, BUR, casella 4).

⚠️ **I numeri vecchi non si cancellano.** In questo progetto una correzione sta datata accanto a ciò che correggeva, non al suo posto: è così che le due correzioni del conteggio reggae sono leggibili.

⚠️ **E la casella deve dichiarare il limite che RESTA, che non è lo stesso di prima.** Il rovesciamento del segno è chiuso; al suo posto c'è l'**ancoraggio**, ed è un limite più piccolo e di natura diversa. Va scritto con questi elementi:

- **cos'è:** chiuso lo spezzarsi di un gesto fra due celle, resta indeciso su **quale** dei due passi ancorarlo. Dai dati soli «14 tick prima del passo 4» e «10 tick dopo il passo 3» sono la stessa cosa, e il gesto è anzi **più vicino** al passo debole: nessun criterio di distanza può preferire il battere. A distinguerli c'è solo il **metro**;
- **quanto pesa, misurato** il 26 agosto 2026 su 42 esecuzioni e 5 batteristi: **2 celle** col taglio scelto (kick di `drummer10/session1/8`, passi 7 e 15), contro 5 con `'rado'` e 0 con `'vicino'` — dove lo zero di `'vicino'` è **impossibile per costruzione**, non una virtù. Gli scarti stanno fra **+12,70 e +16,50** tick: sporgono di 1-4 tick oltre il punto in cui la distanza smette di decidere, cioè sono casi **genuinamente ambigui**, non collocazioni grossolanamente sbagliate;
- **perché non si è scritta una regola**, deciso il 26 agosto 2026: `MU.applica_groove()` **già lo riferisce**. Se il pattern chiede un passo che il profilo non ha, la nota resta com'è e il passo finisce in `senza_appoggio`, che va letto. Il caso è **visibile e non silenzioso**, ed è lo stesso principio del «non inventa». Una regola avrebbe dovuto pesare il metro contro la distanza senza nessuna misura che dica quanto — cioè inventare un numero per 2 celle.

- [ ] **Step 2: `jazz.md` — i numeri della casella 6 che si sono mossi**

Rileggere `out/groove_jazz.txt` e aggiornare, ognuno **con la sua data**: il profilo posizionale (il 43,7%), il charleston contro il ride (**12 su 15**, e mai «15 su 15»: quello che regge è delle fasi grezze), la stratificazione, il massimo spostamento e l'escursione.

⚠️ **Se il massimo spostamento o l'escursione si sono mossi**, va detto **esplicitamente** se il valore di `set_swing()` si muove: da quello dipende se l'A/B già ascoltato dall'utente va riletto. Se non si muovono, si scrive che non si muovono.

- [ ] **Step 3: `MUSICA.md` e `SKILL.md` — il limite nuovo**

Nel § «Il groove template» di `docs/MUSICA.md` e nella riga di `applica_groove()` in `.claude/skills/deluge-pal/SKILL.md`, scrivere che uno scarto può arrivare a **un passo intero** e che quindi il template può posare una nota nel territorio del passo accanto. Un numero vive in un posto solo: qui va il rimando alla scheda, non la ripetizione dei valori.

- [ ] **Step 4: `HANDOFF.md`**

In **§7**, togliere il punto «l'aggregazione per passo del groove template» dall'elenco dei punti aperti. In **§6-terdecies**, sotto «Cosa resta aperto», sostituire il punto sul limite dello stimatore con due righe che dicono **che è stato chiuso, quando, e con quale criterio** — e che i due criteri più ovvi erano trappole.

Nell'elenco dei punti aperti **entra l'ancoraggio**, con una riga che dice cos'è, quanto pesa (2 celle su 42 esecuzioni), perché non si è chiuso, e che `senza_appoggio` lo rende visibile. È un punto aperto **più piccolo** di quello che chiude, e va detto anche questo.

⚠️ Il punto **«la stratificazione misurata non è mai stata messa davanti a un orecchio»** resta aperto, e va aggiornato: la coppia da ascoltare è su `drummer10/session1/1`, passi 4 e 12, cioè **le celle che questo lavoro ha spostato**. I divari di 5,64 e 5,93 tick sono **da rimisurare** col taglio scelto prima di costruire quella coppia.

- [ ] **Step 5: Verificare i terminatori di riga**

Run: `git diff --stat` e poi, per ogni file Markdown toccato:

```bash
git diff --numstat -- docs/repertori/jazz.md docs/MUSICA.md HANDOFF.md
```

Expected: un diff **piccolo**, proporzionato alle righe cambiate. ⚠️ Se un file toccato mostra centinaia o migliaia di righe cambiate, i terminatori sono passati da LF a CRLF. È già successo due volte in questo progetto, con diff gonfiati a 1410 e 958 righe.

Per confermarlo si contano i **byte**, non le righe:

```bash
python -c "import sys,pathlib; b=pathlib.Path(sys.argv[1]).read_bytes(); print('CR:', b.count(b'\r'), 'LF:', b.count(b'\n'))" docs/repertori/jazz.md
```

⚠️ **Non usare `grep -c $'\r' <file>`**: in Git Bash quel pattern si riduce a un pattern vuoto, che matcha **ogni riga**, e il conteggio che ne esce è il numero totale di righe. Sembra un file tutto CRLF anche quando è tutto LF — chi scrive questo piano ci è cascato il 26 agosto 2026.

Se i CR ci sono davvero, si riscrive il file con `write_bytes()` e i terminatori LF prima del commit. ⚠️ E vale anche per gli strumenti di modifica: **il diff va riletto dopo ogni riscrittura di un Markdown**, non solo alla fine.

- [ ] **Step 6: Eseguire tutta la suite un'ultima volta**

Run: `.venv/Scripts/python.exe tests/test_all.py 2>&1 | tail -5`

Expected: tutti PASS.

- [ ] **Step 7: Commit**

```bash
git add docs/repertori/jazz.md docs/MUSICA.md HANDOFF.md .claude/skills/deluge-pal/SKILL.md
git commit -m "musica: la casella 6 prende la decisione che dichiarava, e i numeri la seguono

Il bordo fra due passi non e' piu' un punto aperto: il taglio e' scelto, con
la prova di traslazione per voce, e i numeri vecchi stanno datati accanto ai
nuovi invece che sostituiti.

Resta aperta la coppia d'ascolto sulla stratificazione, e va rimisurata:
poggiava sui passi 4 e 12 di drummer10/session1/1, cioe' sulle celle che
questo lavoro ha spostato.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```
