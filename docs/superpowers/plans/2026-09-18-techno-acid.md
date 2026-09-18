# Techno acid — piano di implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** il suono acid (TB-303) con la sua linea e il filtro che evolve; chiude la casella 8 (lead) e approfondisce la 10 della scheda house/techno.

**Architecture:** una primitiva `MU.acid` (il 303: mono/osc sullo strumento; risonanza, cutoff, env→cutoff, accento, glide, forma di env2 sulle clip), una generalizzazione `MU.automatizza` (di cui `apri_filtro` diventa un wrapper) per rampare cutoff **e** risonanza, un esempio `tools/acid_scritto.py` (techno minimale + linea acid + arco), l'istruzione e la scheda. Verdetto finale: ascolto dell'utente.

**Tech Stack:** Python stdlib + libreria `delugexml`. Test in `tests/test_all.py` (idioma `check`/`salta`). Trasferimento via `tools/dsysex.py` da PowerShell.

## Global Constraints

- **Mai scrivere XML a mano** — solo chiamate alla libreria; attributi solo se verificati/esistenti (regola 2).
- **Fine-riga LF** su codice/istruzioni; `git diff --stat` == `--ignore-cr-at-eol` prima di ogni commit (memoria `fine-riga-nel-repo`).
- **`print()` solo ASCII** — console cp1252.
- **`MU.verifica(doc)` vuota** prima di dichiarare un pezzo caricabile.
- **Valori del 303 `[DEC]`+`[da verificare]`**: esposti come argomenti di `MU.acid`, tarati all'orecchio. La **risonanza in automazione** non è verificata sul device (solo `lpfFrequency` lo è): se non regge, risonanza fissa alta e si rampa il solo cutoff.
- **Contratto delle schede**: titoli caselle esatti + indice coerente; **suite INTERA** prima di committare una scheda.
- **Attribuzione commit:** `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

Fatti grounded (dal preset `refs/synths/Square Saw Bass.XML` e dal corpus):
- il preset ha già `portamento`, `<envelope2>`, `<patchCables>` con `envelope2→lpfFrequency`, `lpfResonance` (a `0x80000000` = 0, da alzare), `lpfFrequency`. `add_track` sposta il `<defaultParams>` sul `<params>` della clip → i param/cable del synth vivono **sulla clip**.
- patch cable attestati: `('envelope2','lpfFrequency')` 157×, `('velocity','lpfFrequency')` 129×.
- `structure.set_attr(inst,'polyphonic','mono')`, `structure.set_osc(inst,1,type='saw'|'square')`, `sound.set(node,name,display)`, `sound.set_patch_cable(node,src,dst,amount)` (crea il `<patchCables>`, `amount` −50..+50), `sound.container(clip)` → `<params>`.
- `lpfResonance`/`lpfFrequency`/`portamento` sono in `param_ids`; `mark_view` funziona per lpfResonance.

---

## File Structure

- `tools/delugexml/musica.py` — **modifica**: `automatizza` (nuova), `apri_filtro` (→ wrapper), `acid` (nuova). Vicino ad `apri_filtro`/`sidechain`.
- `tests/test_all.py` — **modifica**: `test_automatizza`, `test_acid`, `test_acid_scritto` (e `test_apri_filtro` resta verde).
- `tools/acid_scritto.py` — **crea**.
- `docs/istruzioni/acid.md` — **crea**.
- `docs/repertori/house.md` — **modifica**: caselle 8 e 10.
- `docs/MUSICA.md` — **modifica**: riga house/techno (casella 8).

---

## Task 1: `MU.automatizza` + `apri_filtro` come wrapper

**Files:**
- Modify: `tools/delugexml/musica.py` (`apri_filtro` → wrapper; nuova `automatizza`)
- Test: `tests/test_all.py` (`test_automatizza`; `test_apri_filtro` deve restare verde)

**Interfaces:**
- Consumes: `automation.ramp_internal`/`encode`/`mark_view`, `sound.container`, `params`, `param_ids`.
- Produces: `automatizza(doc, clip, param, da, a, da_tick, a_tick, *, passi=7) -> dict` — rampa `param` (unità display 0-50) sulla clip; se `param` non è in `param_ids`, scrive il blob ma salta `mark_view` (racconto `vista=False`). `apri_filtro(...)` = `automatizza(..., 'lpfFrequency', ...)`.

- [ ] **Step 1: Write the failing test**

```python
def test_automatizza():
    """MU.automatizza: una rampa di QUALUNQUE parametro (qui lpfResonance)."""
    from delugexml import musica as MU                          # noqa: PLC0415
    from delugexml import automation as A, sound as SND, params as P  # noqa: PLC0415
    p = REFS / 'songs' / 'TEMPL4.XML'
    if not p.exists():
        salta('test_automatizza', 'TEMPL4.XML assente')
        return
    doc = parse_file(p)
    clip = [c for _, c in S.clips(doc)][1]
    r = MU.automatizza(doc, clip, 'lpfResonance', 5, 40, 0, 384, passi=5)
    grezzo = SND.container(clip).get('lpfResonance')
    check('automatizza scrive un blob su lpfResonance', A.is_automation(grezzo),
          str(grezzo)[:40])
    disp = [P.to_display(pt.hex) for pt in A.decode(grezzo)[1]]
    check('la rampa di risonanza sale', disp[0] <= 7 and disp[-1] >= 38, str(disp))
    check('automatizza segna la vista (lpfResonance e in tabella)',
          r.get('vista') is True, str(r))
    # apri_filtro resta un wrapper funzionante
    r2 = MU.apri_filtro(doc, clip, 10, 45, 0, 384)
    check('apri_filtro e ancora lpfFrequency', r2['param'] == 'lpfFrequency', str(r2))
    check('apri_filtro scrive automazione',
          A.is_automation(SND.container(clip).get('lpfFrequency')))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_automatizza()"`
Expected: FAIL — `MU.automatizza` non esiste.

- [ ] **Step 3: Refactor `apri_filtro` and add `automatizza`**

Sostituire il corpo di `apri_filtro` e aggiungere `automatizza` sopra di esso:

```python
def automatizza(doc, clip, param: str, da: int, a: int, da_tick: int,
                a_tick: int, *, passi: int = 7) -> dict:
    """Una rampa lineare di `param` sulla clip, in unita' display (0-50).

    Generalizza il "filtro che apre": vale per qualunque parametro rampabile
    (cutoff, risonanza, ...). Scrive il blob nel container della clip e prova a
    rendere visibile la vista; se `param` non e' nella tabella di param_ids
    (mark_view lo richiede), scrive comunque e lo dice (`vista=False`).
    """
    from . import automation as AU                              # noqa: PLC0415
    from . import sound as SND                                  # noqa: PLC0415
    from . import params as P                                   # noqa: PLC0415
    if not (0 <= da <= 50 and 0 <= a <= 50):
        raise ValueError(f'valori fuori da 0-50: da={da}, a={a}')
    def _interno(d):
        return min(P.INTERNO_MAX, round(d * P.INTERNI / 50))
    testa, punti = AU.ramp_internal(_interno(da), _interno(a), da_tick, a_tick, passi)
    cont = SND.container(clip)
    if cont is None:
        raise ValueError('la clip non ha un contenitore di parametri')
    cont.set(param, AU.encode(testa, punti))
    try:
        AU.mark_view(doc, clip, param)
        vista = True
    except ValueError:
        vista = False        # param non in tabella: il blob c'e', la vista no
    return {'param': param, 'da': da, 'a': a, 'da_tick': da_tick,
            'a_tick': a_tick, 'passi': passi, 'vista': vista}


def apri_filtro(doc, clip, da: int, a: int, da_tick: int, a_tick: int,
                *, passi: int = 7) -> dict:
    """Il filtro che apre: una rampa del cutoff (lpfFrequency) sulla clip.

    Wrapper di `automatizza` su `lpfFrequency`. Vive nella clip, quindi vale
    solo dove quella clip suona -- il build house apre, il drop e' spalancato.
    """
    return automatizza(doc, clip, 'lpfFrequency', da, a, da_tick, a_tick, passi=passi)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_automatizza(); test_all.test_apri_filtro()"`
Expected: PASS entrambi.

- [ ] **Step 5: Commit**

```bash
git add tools/delugexml/musica.py tests/test_all.py
git commit -m "feat: MU.automatizza -- rampa di qualunque parametro; apri_filtro e' un wrapper

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: `MU.acid` — il suono del 303

**Files:**
- Modify: `tools/delugexml/musica.py` (nuova `acid`, dopo `sidechain`)
- Test: `tests/test_all.py` (`test_acid`)

**Interfaces:**
- Consumes: `structure.set_attr`/`set_osc`, `sound.set`/`set_patch_cable`/`container`, `song.clips`/`instrument_of`.
- Produces: `acid(doc, bersaglio, *, onda='saw', risonanza=40, cutoff=8, env_cutoff=30, acc_cutoff=15, glide=15, env2_decay=18) -> dict` — rende `bersaglio` (nodo strumento synth) un 303: mono + osc1=`onda` (strumento); risonanza/cutoff/portamento/forma-env2 + patch cable `envelope2→lpfFrequency` e `velocity→lpfFrequency` su **ogni clip** del bersaglio. Ritorna un racconto con `clip` (quante toccate) e `da_verificare=True`.

- [ ] **Step 1: Write the failing test**

```python
def test_acid():
    """MU.acid: il 303 -- mono/saw sullo strumento, risonanza+env->cutoff+accento
    sulle clip. Struttura verificata; i valori sono [da verificare] all'orecchio."""
    from delugexml import musica as MU                          # noqa: PLC0415
    from delugexml import sound as SND, create as C            # noqa: PLC0415
    import warnings                                             # noqa: PLC0415
    preset = REFS / 'synths' / 'Square Saw Bass.XML'
    tem = REFS / 'songs' / 'TEMPL0.XML'
    if not (preset.exists() and tem.exists()):
        salta('test_acid', 'manca una fixture')
        return
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(tem)
        iA, cA = C.add_track(doc, str(preset), name='ACID', folder='SYNTHS',
                             length=384, playing=True)
        r = MU.acid(doc, iA, onda='saw', risonanza=40, cutoff=8)
    check('lo strumento e mono', iA.get('polyphonic') == 'mono', iA.get('polyphonic'))
    check('osc1 e saw', iA.find('osc1').get('type') == 'saw',
          iA.find('osc1').get('type'))
    cont = SND.container(cA)
    check('la risonanza e alta', SND.get(cA, 'lpfResonance') == 40,
          str(SND.get(cA, 'lpfResonance')))
    check('il cutoff base e basso', SND.get(cA, 'lpfFrequency') == 8,
          str(SND.get(cA, 'lpfFrequency')))
    cables = {(c['source'], c['destination']) for c in SND.patch_cables(cA)}
    check('c e il cavo env2 -> cutoff (lo squelch)',
          ('envelope2', 'lpfFrequency') in cables, str(cables))
    check('c e il cavo velocity -> cutoff (l accento)',
          ('velocity', 'lpfFrequency') in cables, str(cables))
    check('acid conta le clip toccate e dichiara da_verificare',
          r.get('clip') == 1 and r.get('da_verificare') is True, str(r))
    check('il documento resta valido', MU.verifica(doc) == [], str(MU.verifica(doc)))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_acid()"`
Expected: FAIL — `MU.acid` non esiste.

- [ ] **Step 3: Write minimal implementation**

In `musica.py`, dopo `sidechain`:

```python
def acid(doc, bersaglio, *, onda: str = 'saw', risonanza: int = 40,
         cutoff: int = 8, env_cutoff: float = 30, acc_cutoff: float = 15,
         glide: int = 15, env2_decay: int = 18) -> dict:
    """Rende `bersaglio` (nodo strumento synth) un TB-303 -- il suono acid.

    Il carattere del 303 e' il FILTRO, non le note: LPF molto risonante, un
    inviluppo (env2) che ne apre il cutoff a ogni nota (lo "squelch"), l'accento
    (velocity->cutoff) e lo slide (glide del mono). Tocca due livelli, come
    `MU.sidechain`:

    - STRUMENTO: `polyphonic='mono'` e osc1 `type=onda` ('saw' o 'square', le due
      forme d'onda vere del 303, default saw -- l'acid iconico);
    - OGNI CLIP del bersaglio (e' li' che vivono param e patch cable dei synth):
      `lpfResonance` alto, `lpfFrequency` basso (spazio per l'inviluppo),
      `portamento` (glide), env2 percussivo (attacco 0, decay corto, sustain 0),
      e i due patch cable attestati nel corpus -- `envelope2->lpfFrequency`
      (amount `env_cutoff`) e `velocity->lpfFrequency` (amount `acc_cutoff`).

    ⚠️ I valori sono `[DEC]`+`[da verificare]`: il 303 si tara all'orecchio.
    Sono argomenti apposta, cosi' la correzione e' una parola.
    """
    from . import structure as ST                              # noqa: PLC0415
    from . import sound as SND                                 # noqa: PLC0415
    from . import song as S                                    # noqa: PLC0415

    ST.set_attr(bersaglio, 'polyphonic', 'mono')
    ST.set_osc(bersaglio, 1, type=onda)

    def _voce(clip):
        SND.set(clip, 'lpfResonance', risonanza)
        SND.set(clip, 'lpfFrequency', cutoff)
        SND.set(clip, 'portamento', glide)
        for nome, val in (('envelope2.attack', 0), ('envelope2.decay', env2_decay),
                          ('envelope2.sustain', 0)):
            try:
                SND.set(clip, nome, val)
            except ValueError:
                pass                       # il preset non ha quello stadio: pazienza
        SND.set_patch_cable(clip, 'envelope2', 'lpfFrequency', env_cutoff)
        SND.set_patch_cable(clip, 'velocity', 'lpfFrequency', acc_cutoff)

    n = 0
    for _, clip in S.clips(doc):
        if S.instrument_of(doc, clip) is bersaglio:
            _voce(clip)
            n += 1
    return {'onda': onda, 'risonanza': risonanza, 'cutoff': cutoff,
            'env_cutoff': env_cutoff, 'acc_cutoff': acc_cutoff, 'glide': glide,
            'clip': n, 'da_verificare': True}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_acid()"`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/delugexml/musica.py tests/test_all.py
git commit -m "feat: MU.acid -- il suono del TB-303 (mono/osc + risonanza/env->cutoff/accento/glide)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: `tools/acid_scritto.py` — techno acid

**Files:**
- Create: `tools/acid_scritto.py`
- Test: `tests/test_all.py` (`test_acid_scritto`)

**Interfaces:**
- Consumes: `MU.acid`, `MU.automatizza`, `MU.forma`, `MU.passi`, `create.add_track`, `song.duplicate_clip`, `arranger`.
- Produces: `costruisci() -> tuple[doc, dict]`; `strumento(doc, nome)`; costanti `KICK`, `ROOT`.

**L'arco (32 battute), con `MU.forma`:**

| sezione | batt. | clip |
|---|---|---|
| `intro` | 8 | `drum_intro` (kick + closed hat), `acid_intro` (cutoff basso fisso) |
| `build` | 8 | `drum_full`, `acid_build` (cutoff+risonanza che salgono, `MU.automatizza`) |
| `drop` | 16 | `drum_full`, `acid_drop` (cutoff alto) |

- **la linea acid** (`linea()`): sedicesimi che rotolano su **La** (ROOT=33), con qualche ottava/♭7; accenti (velocity ~120 su alcuni passi contro ~70 base) e slide (note-slide con `length` che sfora sul passo dopo → il mono glissa). 4 battute.
- **batteria**: 808, `drum_full` = kick 4-on-floor + clap 2-4 + open hat sui levare + closed hat sedicesimi; `drum_intro` = solo kick + closed hat. 4 battute, `set_swing(50)`.
- ordine in `costruisci()`: crea strumenti → duplica le clip (vuote) → scrivi note → **`MU.acid(doc, iAcid, onda='saw')`** (dopo aver creato tutte le clip acid, così tocca tutte) → per-clip: `acid_intro` resta col cutoff base; `acid_build` `MU.automatizza(cutoff 8→42)` e `MU.automatizza(risonanza 30→45)`; `acid_drop` `SND.set('lpfFrequency', 42)` → `MU.forma('intro build drop', …, battute_per={'intro':8,'build':8,'drop':16})` → `open_in_arranger`.

- [ ] **Step 1: Write the failing test**

```python
def test_acid_scritto():
    """acid_scritto.py: techno acid -- il 303, la linea, il filtro che evolve."""
    from delugexml import musica as MU                          # noqa: PLC0415
    from delugexml import sound as SND, arranger as AR, automation as A  # noqa: PLC0415
    try:
        import acid_scritto as AC                               # noqa: PLC0415
    except FileNotFoundError:
        salta('test_acid_scritto', 'manca una fixture')
        return
    try:
        doc, _ = AC.costruisci()
    except FileNotFoundError:
        salta('test_acid_scritto (build)', 'manca una fixture')
        return
    check('il pezzo ACID e valido', MU.verifica(doc) == [], str(MU.verifica(doc)))
    check('nessuna avvertenza', MU.avvertenze(doc) == [], str(MU.avvertenze(doc)))
    est = AR.extent(doc)
    check('l arco e lungo 32 battute',
          est is not None and est[1] == 32 * MU.TICK_PER_BATTUTA, str(est))
    iA = AC.strumento(doc, 'ACID')
    check('l acid e mono', iA.get('polyphonic') == 'mono', iA.get('polyphonic'))
    acid_clips = [c for _, c in S.clips(doc) if S.instrument_of(doc, c) is iA]
    cav = {(c['source'], c['destination'])
           for cl in acid_clips for c in SND.patch_cables(cl)}
    check('ogni clip acid ha env2->cutoff e velocity->cutoff',
          ('envelope2', 'lpfFrequency') in cav and ('velocity', 'lpfFrequency') in cav,
          str(cav))
    # il build ha una rampa sul cutoff
    ha_ramp = any(A.is_automation(SND.container(cl).get('lpfFrequency') or '')
                  for cl in acid_clips)
    check('una clip acid ha il filtro che apre (automazione)', ha_ramp)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_acid_scritto()"`
Expected: FAIL — modulo assente.

- [ ] **Step 3: Write `tools/acid_scritto.py`**

Struttura come `house2_scritto.py` (stesso scheletro: costanti, `strumento`, funzioni-nota, `costruisci`, `__main__` che stampa extent/verifica/avvertenze). Preset acid = `Square Saw Bass.XML`. Kit = `808 From Mars.XML`. `ROOT = 33` (La1). BPM 132, swing 50, scala C (La = relativa). Duplicare le clip con `song.duplicate_clip` + `arranger.index_of` (come house2), sezioni distinte per evitare `avvertenze`. Verificare `MU.avvertenze(doc)` vuota nel `__main__`.

La linea acid — un giro di 16 passi ripetuto (l'acid muove col FILTRO, non con le note):

```python
def linea() -> dict:
    """Il riff 303: sedicesimi che rotolano su La, accenti e slide. Il movimento
    vero e' il filtro (MU.acid + MU.automatizza), non le altezze."""
    from delugexml.notes import Note                          # noqa: PLC0415
    #        passo:  0  1   2  3  4   5  6  7  8   9 10 11  12 13 14  15
    OFF   =        [0, 0, 12, 0, 0, 10, 0, 0, 0, 12, 0, 0,  7, 0, 0, 10]
    ACC   =        [1, 0,  0, 1, 0,  0, 0, 1, 0,  0, 0, 0,  1, 0, 0,  0]
    SLIDE =        [0, 1,  0, 0, 0,  1, 0, 0, 0,  1, 0, 0,  0, 0, 1,  0]
    voce: dict = {}
    for bar in range(BARS):
        for i in range(16):
            alt = ROOT + OFF[i]
            vel = 120 if ACC[i] else 70                      # l'accento e' la velocity
            dur = P + 8 if SLIDE[i] else P - 4               # slide = sfora sul passo dopo (legato -> glide)
            voce.setdefault(alt, []).append(
                Note(pos=bar * B + i * P, length=dur, velocity=vel))
    return voce
```

`P = MU.TICK_PER_MOVIMENTO // 4` (24, un sedicesimo); una nota-slide (length 32) sfora sull'attacco della successiva (a 24) → in mono glissa; le altre (length 20) lasciano un buco.

- [ ] **Step 4: Run the module then the test**

Run: `.venv/Scripts/python.exe tools/acid_scritto.py` (deve stampare `verifica: vuota`), poi
`.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_acid_scritto()"`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/acid_scritto.py tests/test_all.py
git commit -m "feat: acid_scritto -- techno acid con il 303, la linea e il filtro che evolve

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: l'istruzione `docs/istruzioni/acid.md`

**Files:**
- Create: `docs/istruzioni/acid.md`

Forma collaudata (perimetro → gradi → vocabolario → vincoli → come si decide → esempio → cosa manca). Contenuto obbligato:
- **cos'è il 303**: un osc (saw **o** quadra, entrambe vere), LPF **molto risonante**, env sul cutoff, accento, slide; il carattere è il **filtro**, non le note;
- **il suono** (`MU.acid`): i due livelli, la forma d'onda parametro, i patch cable attestati (`envelope2→cutoff` 157×, `velocity→cutoff` 129×);
- **la linea**: rada in altezza (una-due note), fitta in ritmo (sedicesimi); l'**accento** è la velocity, lo **slide** è il legato in mono (`portamento`);
- **il filtro che evolve** (`MU.automatizza` su cutoff/risonanza): l'anima dell'acid — «una battuta non dice niente, è il filtro che cambia»;
- **i vincoli**: risonanza alta o non è acid; la linea non è melodica; l'accento è velocity; lo slide è legato in mono; ⚠️ risonanza in automazione `[da verificare]` (solo il cutoff è verificato sul device);
- **gradi**: `[LIB]`+`[DEC]` (convenzione), patch cable `[OSS]` (corpus), valori `[da verificare]`;
- link con `arrangiamento-house.md` (l'acid è un caso del «filtro in movimento») e `basso-house.md`.

- [ ] **Step 1: Scrivere il file** (LF).
- [ ] **Step 2: Verificare i fine-riga** (`git diff --stat` == `--ignore-cr-at-eol`).
- [ ] **Step 3: Commit**

```bash
git add docs/istruzioni/acid.md
git commit -m "istruzioni: techno acid -- il 303, la linea, il filtro che evolve

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: la scheda `house.md` e l'indice `MUSICA.md`

**Files:**
- Modify: `docs/repertori/house.md` (casella 8; casella 10 ampliata; header; fonti)
- Modify: `docs/MUSICA.md` (riga house/techno, casella 8)

- [ ] **Step 1: Aggiornare `house.md`**
  - **casella 8 (Melodia e ornamentazione):** da «Vuota» a piena per il **lead acid** (il riff 303: rada in altezza, accenti, slide), `[LIB]`+`[DEC]`; link a `acid.md`. Notare che il **vocal chop** resta fuori (è `audio.py`);
  - **casella 10 (Sul Deluge):** aggiungere il **suono acid** (`MU.acid`, i patch cable `[OSS]`) e `MU.automatizza` per il sweep di cutoff/risonanza; nota che la risonanza in automazione è `[da verificare]`;
  - **casella 3/4** (tempo/feel): nota il techno acid (~132, dritto);
  - header: house/techno ora copre anche l'acid; verdetto d'ascolto dell'acid **in sospeso**;
  - fonti: aggiungere `acid.md` e `tools/acid_scritto.py`.

- [ ] **Step 2: Aggiornare l'indice in `MUSICA.md`** — riga house/techno: casella **8** da `○` a `●`; **titoli caselle invariati**.

- [ ] **Step 3: Verificare i fine-riga** sui due file.

- [ ] **Step 4: Lanciare la suite INTERA** (contratto delle schede):

Run: `.venv/Scripts/python.exe tests/test_all.py`
Expected: verde (i test nuovi passano; nessun rosso).

- [ ] **Step 5: Commit**

```bash
git add docs/repertori/house.md docs/MUSICA.md
git commit -m "repertori: house -- casella 8 (lead acid) e 10 (suono acid) piene

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: caricamento e ascolto (chiude il giro)

- [ ] **Step 1:** generare il file con `acid_scritto.costruisci()` + `write_file` (format table); `verifica()` vuota.
- [ ] **Step 2:** destinazione `MU.destinazione('acid', 1, 'SONGS')` → `/SONGS/DelugePal/ACID01.XML` (se esiste, incrementare).
- [ ] **Step 3:** trasferire con `tools/dsysex.py` **da PowerShell**, senza troncare l'output di `put`. Se il Deluge non risponde al `ping`: scrivere il file locale e **dirlo**.
- [ ] **Step 4: l'utente ascolta.** Guardare/ascoltare sul Deluge: il 303 «strilla» (risonanza)? l'accento si sente sui passi forti? lo slide glissa fra le note legate? il filtro **evolve** nel build? il decay di env2 dà lo squelch giusto?
- [ ] **Step 5: pinnare i `[da verificare]`.** Col verdetto: fissare i valori di `MU.acid` (risonanza/env_cutoff/acc_cutoff/glide/env2_decay) e dello sweep in `acid_scritto.py`, aggiornare la scheda col verdetto e il grado. Commit finale + HANDOFF.

---

## Self-Review

**1. Spec coverage:** `MU.acid` → Task 2; `MU.automatizza` (+apri_filtro wrapper) → Task 1; linea acid nell'esempio → Task 3; pezzo techno + arco + sweep → Task 3; istruzione → Task 4; scheda 8/10 + indice → Task 5; ascolto → Task 6; forma d'onda parametro default saw → Task 2/3; risonanza-automazione `[da verificare]` → Task 1 (vista) + costanti globali + Task 6. YAGNI (niente vocal chop, niente overdrive, niente primitiva-linea) rispettato.

**2. Placeholder scan:** nessun TODO di contenuto. I valori 303 sono argomenti `[DEC]`/`[da verificare]` per scelta di metodo (ascolto). La `linea()` di Task 3 Step 3 è descritta a parole con i numeri chiave (ROOT 33, velocity 120/70, slide = length che sfora); il codice concreto lo scrive l'implementatore sul modello di `house2_scritto.basso()`.

**3. Type consistency:** `automatizza`/`apri_filtro`/`acid`/`costruisci`/`strumento(doc,nome)` usati con le stesse firme in Task 1-3 e nei test. `lpfResonance`/`lpfFrequency`/`portamento`/`envelope2.*`/`envelope2→lpfFrequency`/`velocity→lpfFrequency` scritti con gli stessi nomi ovunque, coerenti col preset e col corpus.
