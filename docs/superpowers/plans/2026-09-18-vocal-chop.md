# Vocal chop — piano di implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** il vocal chop — affettare un campione in un kit di fette e suonarlo a ritmo — che riempie la casella 8 di house/trip-hop; lo stesso slicing sblocca poi jungle/DnB.

**Architecture:** una primitiva `kit.affetta` (N drum-fetta, ognuno = una `<zone>` dello stesso file, loopMode ereditato da un drum one-shot vero), un esempio `tools/vocalchop_scritto.py` (beat house + l'mmyeah in 8 fette come hook), l'istruzione e l'aggiornamento delle schede.

**Tech Stack:** Python stdlib + libreria `delugexml`. Test in `tests/test_all.py`. Trasferimento via `tools/dsysex.py` (SD di nuovo nel Deluge).

## Global Constraints

- **Mai scrivere XML a mano / attributi non capiti** — il `loopMode` della fetta si **eredita** copiando un drum one-shot vero (BD A di `808 From Mars`, `loopMode=1`=ONCE, il kick suona intero), non si scrive.
- **Fine-riga LF** su codice/istruzioni; `git diff --stat` == `--ignore-cr-at-eol` prima di ogni commit; **HANDOFF.md CRLF** (memoria `fine-riga-nel-repo`).
- **`print()` solo ASCII** (console cp1252).
- **`MU.verifica(doc)` vuota** e **`MU.avvertenze(doc)` letta** prima del caricamento.
- **Contratto delle schede**: titoli caselle esatti; l'indice deve coincidere con la scheda (c'è un test); **suite INTERA** prima di committare le schede.
- **`kit.set_sample(path,...)`**: `path` è **relativo alla SD** (`SAMPLES/RECORD/REC00027.WAV`), come lo scrive il dispositivo; il file c'è già sulla SD (niente upload).
- **Attribuzione commit:** `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

Fatti grounded (misurati/letti):
- campione `SAMPLES/RECORD/REC00027.WAV`, **142725 frame** (mono 24-bit 44.1k, ~3,24 s), letto con `audio.wav_frames` dalla SD nel lettore.
- una fetta nel file: `<osc type="sample" loopMode="1" …><zone startSamplePos endSamplePos/></osc>` (posizioni in **frame**); `loopMode=1`=ONCE (il BD A di `808 From Mars` lo usa: un one-shot che suona intero).
- helper kit: `copy_drum(kit, i)` (copia staccata), `add_drum(doc, kit, drum, name=)` (append + noteRow per clip, ritorna indice), `remove_drum(doc, kit, i)` (toglie + rinumera + aggiorna clip), `set_sample(drum, path, start=, end=)` (scrive type=sample, fileName, `<zone>`), `S.drums(kit)`, `S.nome_drum` (attributo `name`).

---

## File Structure

- `tools/delugexml/kit.py` — **modifica**: `affetta` (nuova).
- `tests/test_all.py` — **modifica**: `test_affetta`, `test_vocalchop_scritto`.
- `tools/vocalchop_scritto.py` — **crea**.
- `docs/istruzioni/vocal-chop.md` — **crea**.
- `docs/repertori/house.md`, `docs/repertori/trip-hop.md` — **modifica**: casella 8.

---

## Task 1: `kit.affetta` — l'affetta-campione

**Files:**
- Modify: `tools/delugexml/kit.py` (nuova `affetta`)
- Test: `tests/test_all.py` (`test_affetta`)

**Interfaces:**
- Produces: `affetta(doc, kit, path, frames, *, n=16, base=0) -> list[str]` — trasforma `kit` in N drum-fetta (copie del drum `base`, per ereditarne `loopMode`), ognuno con `fileName=path` e `<zone>` a `[i*frames//n, (i+1)*frames//n]` (l'ultima fino a `frames`). Ritorna `['fetta 1', …, 'fetta N']`.

- [ ] **Step 1: Write the failing test**

```python
def test_affetta():
    """kit.affetta: N drum-fetta da un campione, zone sequenziali, loopMode ereditato."""
    from delugexml import kit as K, song as S, create as C     # noqa: PLC0415
    import warnings                                             # noqa: PLC0415
    preset = REFS / 'kits' / '808 From Mars.XML'
    tem = REFS / 'songs' / 'TEMPL0.XML'
    if not (preset.exists() and tem.exists()):
        salta('test_affetta', 'manca una fixture')
        return
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(tem)
        kit, clip = C.add_track(doc, str(preset), name='CHOP', folder='KITS',
                                length=384, playing=True)
        base_loop = S.drums(kit)[0].find('osc1').get('loopMode')
        nomi = K.affetta(doc, kit, 'SAMPLES/RECORD/REC00027.WAV', 142725, n=4)
    drums = S.drums(kit)
    check('il kit ha 4 fette', len(drums) == 4, str(len(drums)))
    check('i nomi sono fetta 1..4', nomi == ['fetta 1', 'fetta 2', 'fetta 3', 'fetta 4'],
          str(nomi))
    zone = [(int(d.find('osc1').find('zone').get('startSamplePos')),
             int(d.find('osc1').find('zone').get('endSamplePos'))) for d in drums]
    check('le zone sono sequenziali e coprono il file',
          zone == [(0, 35681), (35681, 71362), (71362, 107043), (107043, 142725)],
          str(zone))
    check('ogni fetta punta al campione',
          all(d.find('osc1').get('fileName') == 'SAMPLES/RECORD/REC00027.WAV'
              for d in drums))
    check('il loopMode e ereditato dal base (one-shot), non scritto a caso',
          all(d.find('osc1').get('loopMode') == base_loop for d in drums), base_loop)
    check('le clip hanno una noteRow per fetta',
          all(len([r for r in S.note_rows(c) if r.has('drumIndex')]) == 4
              for _, c in S.clips(doc) if S.instrument_of(doc, c) is kit))
    check('il documento resta valido', MU_ok(doc))


def MU_ok(doc):
    from delugexml import musica as MU                          # noqa: PLC0415
    return MU.verifica(doc) == []
```

(`35681 = 142725//4`; l'ultima zona arriva a `142725`.)

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_affetta()"`
Expected: FAIL — `K.affetta` non esiste.

- [ ] **Step 3: Write minimal implementation** (in `kit.py`, dopo `set_sample`)

```python
def affetta(doc: Document, kit: Node, path: str, frames: int, *,
            n: int = 16, base: int = 0) -> list[str]:
    """Affetta un campione in un kit di N drum-fetta -- il vocal chop, o il break.

    Ogni drum-fetta e' una COPIA del drum `base`, cosi' ne EREDITA `loopMode`
    (one-shot), gli inviluppi e il resto: un drum che funziona, invece di
    scrivere `loopMode` alla cieca (regola del progetto). Su ognuno si cambia
    solo `fileName=path` e la `<zone>` a `[i*frames//n, (i+1)*frames//n]`
    (l'ultima fino a `frames`, per coprire il resto). `path` e' relativo alla SD
    (`SAMPLES/...`); `frames` da `audio.wav_frames(path_locale)[0]`. Riusabile
    per il break di jungle/DnB. Ritorna i nomi `['fetta 1', ...]`.
    """
    from . import song as S                                    # noqa: PLC0415
    if n < 1:
        raise ValueError('servono almeno 1 fetta')
    orig = S.drums(kit)
    if not 0 <= base < len(orig):
        raise ValueError(f'drum base {base} inesistente (ce ne sono {len(orig)})')
    n_orig = len(orig)
    modello = copy_drum(kit, base)                 # copia staccata: loopMode ereditato
    # aggiungi N fette in fondo, poi togli gli n_orig originali dal fronte
    for i in range(n):
        add_drum(doc, kit, modello.copy_detached(), name=f'fetta {i + 1}')
    for _ in range(n_orig):
        remove_drum(doc, kit, 0)
    dur = frames // n
    fette = S.drums(kit)
    nomi = []
    for i in range(n):
        a = i * dur
        b = frames if i == n - 1 else (i + 1) * dur
        set_sample(fette[i], path, start=a, end=b)
        nomi.append(f'fetta {i + 1}')
    return nomi
```

⚠️ Se `modello.copy_detached()` non desse copie distinte (fette con la stessa zona), il test lo becca: in quel caso copiare da un originale conservato prima delle rimozioni. Verificare `Node.copy_detached()` sul volo.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_affetta()"`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/delugexml/kit.py tests/test_all.py
git commit -m "feat: kit.affetta -- affetta un campione in un kit di N fette (vocal chop, break)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: `tools/vocalchop_scritto.py` — house + l'mmyeah affettato

**Files:**
- Create: `tools/vocalchop_scritto.py`
- Test: `tests/test_all.py` (`test_vocalchop_scritto`)

**Interfaces:**
- Consumes: `kit.affetta`, `MU.passi`, `MU.scrivi`, `MU.forma`/`arranger`, `create.add_track`, `sound`.
- Produces: `costruisci() -> tuple[doc, dict]`; `strumento(doc, nome)`; costanti `SAMPLE`, `FRAMES`, `NFETTE`.

Scheletro come `house_scritto.py` (four-on-the-floor 808). Aggiunte:
- costanti: `SAMPLE = 'SAMPLES/RECORD/REC00027.WAV'`, `FRAMES = 142725` (misurato dalla SD; il file e' gia' sulla SD), `NFETTE = 8`, `BPM = 124`, `SWING = 55`.
- **il kit di fette** (strumento a sé, dal preset `808 From Mars` — ha drum one-shot da cui ereditare):

```python
    iChop, cChop = C.add_track(doc, str(KIT), name='CHOP', folder='KITS',
                               length=lung, colour_offset='48', playing=True)
    fette = K.affetta(doc, iChop, SAMPLE, FRAMES, n=NFETTE)   # ['fetta 1'..'fetta 8']
    for nome, note in chop(fette).items():
        if note:
            MU.scrivi(doc, cChop, note, dove=nome)
```

- **il pattern del chop** (`chop(fette)` → `{nome_fetta: [Note]}`), 2 battute, sedicesimi; la parola in crome + qualche stutter (`[DEC]`, all'orecchio):

```python
def chop(fette: list[str]) -> dict:
    """Le fette dell'mmyeah innescate a ritmo: la parola in crome (fette 1-8),
    poi uno stutter. [DEC], da rifinire all'orecchio. ONCE = la fetta suona intera."""
    from delugexml.notes import Note                          # noqa: PLC0415
    CROMA = MU.TICK_PER_MOVIMENTO // 2                        # 48
    P = MU.TICK_PER_MOVIMENTO // 4                            # 24
    # (passo in sedicesimi su 2 battute, fetta 1-based)
    eventi = [(0, 1), (2, 2), (4, 3), (6, 4), (8, 5), (10, 6), (12, 7), (14, 8),
              (16, 1), (17, 1), (18, 1), (20, 8), (24, 4), (26, 5), (28, 8)]
    voci: dict = {}
    for passo, f in eventi:
        nome = fette[f - 1]
        voci.setdefault(nome, []).append(
            Note(pos=passo * P, length=CROMA, velocity=112))
    return voci
```

- batteria house (riusa `house_scritto` idiomi: cassa four-on-floor, clap 2-4, open hat sui levare, closed hat) su un secondo kit 808 (`name='BEAT'`), e un basso house in levare (`Square Saw Bass` scurito). Minimale: il vocal e' il protagonista.
- forma: 8 battute (il chop di 2 battute ripetuto), `A.place` o `MU.forma`. `verifica()` vuota, `avvertenze()` pulite.

- [ ] **Step 1: Write the failing test**

```python
def test_vocalchop_scritto():
    """vocalchop_scritto.py: house + l'mmyeah in 8 fette come hook."""
    from delugexml import musica as MU, song as S             # noqa: PLC0415
    try:
        import vocalchop_scritto as VC                          # noqa: PLC0415
    except FileNotFoundError:
        salta('test_vocalchop_scritto', 'manca una fixture')
        return
    try:
        doc, _ = VC.costruisci()
    except FileNotFoundError:
        salta('test_vocalchop_scritto (build)', 'manca una fixture')
        return
    check('il pezzo VOCALCHOP e valido', MU.verifica(doc) == [], str(MU.verifica(doc)))
    check('nessuna avvertenza', MU.avvertenze(doc) == [], str(MU.avvertenze(doc)))
    iChop = VC.strumento(doc, 'CHOP')
    drums = S.drums(iChop)
    check('il kit CHOP ha 8 fette', len(drums) == 8, str(len(drums)))
    check('le fette puntano all mmyeah',
          all(d.find('osc1').get('fileName') == VC.SAMPLE for d in drums))
    check('le zone sono crescenti',
          [int(d.find('osc1').find('zone').get('startSamplePos')) for d in drums]
          == sorted(int(d.find('osc1').find('zone').get('startSamplePos')) for d in drums))
```

- [ ] **Step 2: Run to fail** — modulo assente.
- [ ] **Step 3: Write `tools/vocalchop_scritto.py`** (scheletro `house_scritto.py` + `chop()` + il kit di fette + `strumento(doc,nome)` + `costruisci()` + `__main__` che stampa extent/verifica/avvertenze).
- [ ] **Step 4: Run the module then the test** — `.venv/Scripts/python.exe tools/vocalchop_scritto.py` (verifica vuota), poi il test. PASS.
- [ ] **Step 5: Commit**

```bash
git add tools/vocalchop_scritto.py tests/test_all.py
git commit -m "feat: vocalchop_scritto -- house + l'mmyeah affettato in 8 fette come hook

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: l'istruzione `docs/istruzioni/vocal-chop.md`

**Files:** Create: `docs/istruzioni/vocal-chop.md`

Contenuto: cos'è (un campione vocale tagliato in un kit di fette, innescate a ritmo); come si taglia (`kit.affetta`, fette uguali; lo Slicer nativo del Deluge fa lo stesso — tieni premuto Select → SLICE); il MODE **ONCE** (`loopMode`, ereditato da un drum one-shot, non scritto a mano); come si **compone** il chop (ricostruire la parola, poi ripetizioni/stutter/ri-ordine delle fette — è ritmo + scelta, `[DEC]` all'orecchio); il legame col **break** (jungle/DnB: stesso meccanismo su un break di batteria); i gradi (`[LIB]`+`[DEC]`; struttura della fetta `[OSS]` — Slicer/FINDINGS §«Campioni e tick»); l'esempio `tools/vocalchop_scritto.py`; cosa manca (taglio sui transienti, pitch/stretch delle fette, effetti — futuro). Verdetto d'ascolto: **in sospeso**.

- [ ] Step 1: scrivere (LF). Step 2: fine-riga OK. Step 3: commit `istruzioni: vocal chop ...`.

---

## Task 4: le schede (casella 8 di house e trip-hop)

**Files:** Modify `docs/repertori/house.md`, `docs/repertori/trip-hop.md`.

- [ ] **Step 1: `house.md` casella 8** — aggiungere il **vocal chop** accanto al lead acid: la tecnica (`kit.affetta`, l'mmyeah in fette, il hook a ritmo), `[LIB]`+`[DEC]`, struttura `[OSS]`; link a `vocal-chop.md`, esempio `tools/vocalchop_scritto.py`. ⚠️ La prima riga non vuota della casella determina lo stato nell'indice: casella 8 di house era già `●` (lead acid) → resta `●`, l'indice non cambia.
- [ ] **Step 2: `trip-hop.md` casella 8** — da «Parziale» (vocal mancante) a piena: il vocal chop ora è coperto (`kit.affetta`); link a `vocal-chop.md`. ⚠️ Se la prima riga passa da `**Parziale.**` a piena, lo stato indice della casella 8 di trip-hop cambia da `◐` a `●`: **aggiornare la riga di trip-hop in `docs/MUSICA.md`** di conseguenza (casella 8 → `●`), o lasciare `◐` se il vocal-chop copre solo una parte (decidere e rendere indice==scheda). Il test del contratto lo verifica.
- [ ] **Step 3: fine-riga** sui file toccati (incluso `MUSICA.md` se cambia).
- [ ] **Step 4: suite INTERA** — `.venv/Scripts/python.exe tests/test_all.py`, verde (attenzione al test `l indice coincide con la scheda`).
- [ ] **Step 5: commit** `repertori: vocal chop nella casella 8 di house e trip-hop`.

---

## Task 5: caricamento e ascolto (SD nel Deluge)

- [ ] **Step 1:** generare con `vocalchop_scritto.costruisci()` + `write_file`; `verifica()` vuota, `avvertenze()` pulite.
- [ ] **Step 2:** `MU.destinazione('vocalchop', 1, 'SONGS')` → verificare il nome (se troppo lungo/rifiutato, usare `vchop`); se esiste, incrementare.
- [ ] **Step 3:** `ports`/`ping`; se il Deluge risponde, `put` da **PowerShell** senza troncare l'output; se non risponde, scrivere il file locale e **dirlo**. Il campione è già sulla SD.
- [ ] **Step 4: l'utente ascolta.** Le fette suonano intere (ONCE) o si troncano? Il chop ricostruisce l'«mmyeah» e lo stutter funziona? Le fette cadono nei punti giusti (i tagli uguali sono musicali o servono altre N)?
- [ ] **Step 5: pinnare.** Col verdetto: rifinire il pattern/`NFETTE` se serve, scrivere il verdetto in scheda/istruzione, aggiornare il HANDOFF (CRLF) — inclusa la nota che **`dir` via SysEx funziona** su questo firmware. Commit finale.

---

## Self-Review

**1. Spec coverage:** `kit.affetta` → Task 1; mmyeah 8 fette + house → Task 2; istruzione → Task 3; casella 8 house+trip-hop → Task 4; ascolto → Task 5; loopMode ereditato (non scritto) → Task 1; break riusa affetta (nominato) → Task 1/3. YAGNI (niente onset, niente pitch/stretch, niente riga d'indice nuova) rispettato.

**2. Placeholder scan:** nessun TODO di contenuto. Il pattern `chop()` è concreto (`[DEC]`, all'orecchio). L'unico ramo da verificare sul volo è `Node.copy_detached()` su un nodo già staccato (Task 1, con fallback dichiarato) e il nome `destinazione('vocalchop')` (Task 5, con fallback `vchop`).

**3. Type consistency:** `affetta`/`chop`/`costruisci`/`strumento(doc,nome)`/`SAMPLE`/`FRAMES`/`NFETTE` con le stesse firme in Task 1-2 e nei test. `fileName`/`<zone>`/`startSamplePos`/`endSamplePos`/`loopMode` coerenti col formato reale. Campione `SAMPLES/RECORD/REC00027.WAV` e `142725` identici ovunque.
