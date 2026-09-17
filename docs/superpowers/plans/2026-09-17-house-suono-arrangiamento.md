# House suono + arrangiamento — piano di implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** chiudere le caselle 9 (build/drop) e 10 (filtro + sidechain) della scheda house, con due primitive riusabili, un pezzo lavorato, l'istruzione e la scheda.

**Architecture:** due primitive nuove in `tools/delugexml/musica.py` (`apri_filtro`, `sidechain`) costruite su ciò che c'è già (`automation.ramp_internal`/`encode`/`mark_view`, `sound.container`/`set_raw`); un esempio lavorato `tools/house2_scritto.py` che stende l'arco a 32 battute con `MU.forma` + `arranger` e accende filtro e sidechain; poi l'istruzione, la scheda e l'indice. Il verdetto finale è l'ascolto dell'utente sul Deluge.

**Tech Stack:** Python stdlib + la libreria `delugexml` del progetto. Test in `tests/test_all.py` (idioma `check`/`salta`, niente pytest). Trasferimento via `tools/dsysex.py` da PowerShell.

## Global Constraints

Copiati dallo spec e dalle regole del progetto. Ogni task li eredita:

- **Mai scrivere XML a mano** — solo chiamate alla libreria; attributi solo se verificati dai file veri (regola 2, `SKILL.md`).
- **Fine-riga LF** su codice/istruzioni. Scrivere con `write_bytes`/`newline=''`; **prima di ogni commit** verificare `git diff --stat` == `git diff --stat --ignore-cr-at-eol` (memoria `fine-riga-nel-repo`).
- **`print()` solo ASCII** — la console Windows è cp1252, `⚠️` la fa crashare (`HANDOFF` §6-vicies).
- **`MU.verifica(doc)` vuota** prima di dichiarare un pezzo caricabile.
- **Il valore del ducking è `[da verificare]`**: struttura verificata dai file veri, magnitudine/verso da pinnare all'orecchio/dispositivo. `sidechainCompressorVolume` NON è in `param_ids`, quindi si scrive come attributo nel container, non via `sound.set`.
- **Contratto delle schede** (memoria `contratto-schede-repertorio`): titoli caselle esatti + indice coerente; **lanciare la suite INTERA** prima di committare una scheda.
- **Attribuzione commit:** ogni messaggio finisce con `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

Valori di riferimento verificati (dallo schema c1.3.0 e dai file veri):
- `sideChainSend="2147483647"` = send pieno (il kick manda).
- `sidechainCompressorVolume` osservati nei file: `0xF2000000`, `0xDE000000`, `0xFC000000` (attributo hex32 nei `<params>`).
- `sidechainCompressorShape="0xDC28F5B2"` = default.
- `<sidechain>` figlio del `<sound>`: `attack`, `release`, `syncLevel`, `syncType` (int).
- `P.INTERNI = 128`, `P.INTERNO_MAX = 127`, display 0-50; `A.ramp_internal(da,a,inizio,fine,passi)` vuole unità interne 0-127.

---

## File Structure

- `tools/delugexml/musica.py` — **modifica**: aggiunge `apri_filtro` e `sidechain` (accanto alle altre primitive, dopo `variazione`/prima dei verbi). Un helper privato `_sound_di_drum(kit, nome)`.
- `tests/test_all.py` — **modifica**: aggiunge `test_apri_filtro`, `test_sidechain`, `test_house2_scritto`.
- `tools/house2_scritto.py` — **crea**: l'esempio lavorato dell'arco.
- `docs/istruzioni/arrangiamento-house.md` — **crea**: l'istruzione (build/drop + filtro + sidechain).
- `docs/repertori/house.md` — **modifica**: caselle 9 e 10, note «cosa manca», verdetto.
- `docs/MUSICA.md` — **modifica**: la riga d'indice di house/techno.

---

## Task 1: `MU.apri_filtro` — la rampa del cutoff

**Files:**
- Modify: `tools/delugexml/musica.py` (nuova funzione dopo `variazione`)
- Test: `tests/test_all.py` (`test_apri_filtro`)

**Interfaces:**
- Consumes: `automation.ramp_internal`, `automation.encode`, `automation.mark_view`, `sound.container`, `params.INTERNI`/`INTERNO_MAX`.
- Produces: `apri_filtro(doc, clip, da, a, da_tick, a_tick, *, passi=7) -> dict` — scrive un'automazione lineare di `lpfFrequency` sulla `clip` da `da` a `a` (display 0-50) fra `da_tick` e `a_tick`, rende la vista visibile, e ritorna un racconto `{'param','da','a','da_tick','a_tick','passi'}`.

- [ ] **Step 1: Write the failing test**

In `tests/test_all.py`, aggiungi:

```python
def test_apri_filtro():
    """MU.apri_filtro: una rampa del cutoff in unita' display (0-50), sulla clip."""
    from delugexml import musica as MU                          # noqa: PLC0415
    from delugexml import automation as A, sound as SND, params as P  # noqa: PLC0415
    p = REFS / 'songs' / 'TEMPL4.XML'
    if not p.exists():
        salta('test_apri_filtro', 'TEMPL4.XML assente')
        return
    doc = parse_file(p)
    clip = [c for _, c in S.clips(doc)][1]        # una clip di synth
    r = MU.apri_filtro(doc, clip, 10, 45, 0, 384, passi=7)
    grezzo = SND.container(clip).get('lpfFrequency')
    check('apri_filtro scrive un blob di automazione su lpfFrequency',
          A.is_automation(grezzo), str(grezzo)[:40])
    testa, punti = A.decode(grezzo)
    disp = [P.to_display(pt.hex) for pt in punti]
    check('la rampa parte da ~10 e arriva a ~45',
          disp[0] <= 12 and disp[-1] >= 43, str(disp))
    check('la rampa sale davvero, punto per punto',
          all(b >= a for a, b in zip(disp, disp[1:])), str(disp))
    check('le posizioni vanno da 0 a 384',
          (punti[0].pos, punti[-1].pos) == (0, 384),
          f'{punti[0].pos}..{punti[-1].pos}')
    check('la vista automazione e sulla clip',
          clip.get('lastSelectedParamID') == '24', clip.get('lastSelectedParamID'))
    check('apri_filtro racconta cosa ha fatto', r['param'] == 'lpfFrequency', str(r))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_apri_filtro()"`
Expected: FAIL/AttributeError — `MU.apri_filtro` non esiste ancora.

- [ ] **Step 3: Write minimal implementation**

In `tools/delugexml/musica.py`, dopo `variazione`:

```python
def apri_filtro(doc, clip, da: int, a: int, da_tick: int, a_tick: int,
                *, passi: int = 7) -> dict:
    """Una rampa lineare del cutoff (lpfFrequency) sulla clip, in unita' display.

    `da` e `a` sono il cutoff 0-50 come sul display; `da_tick`/`a_tick` il tratto
    in tick. Scrive il blob di automazione e rende la vista visibile (senno' sul
    dispositivo l'automazione, pur corretta, non si vede -- `automation.mark_view`).
    E' il "filtro che apre" del build house. Wrapper di `automation.ramp_internal`,
    che tiene i punti sulla griglia interna (come fa il firmware).
    """
    from . import automation as AU                              # noqa: PLC0415
    from . import sound as SND                                  # noqa: PLC0415
    from . import params as P                                   # noqa: PLC0415
    if not (0 <= da <= 50 and 0 <= a <= 50):
        raise ValueError(f'cutoff fuori da 0-50: da={da}, a={a}')
    interno = lambda d: min(P.INTERNO_MAX, round(d * P.INTERNI / 50))  # noqa: E731
    testa, punti = AU.ramp_internal(interno(da), interno(a), da_tick, a_tick, passi)
    cont = SND.container(clip)
    if cont is None:
        raise ValueError('la clip non ha un contenitore di parametri')
    cont.set('lpfFrequency', AU.encode(testa, punti))
    AU.mark_view(doc, clip, 'lpfFrequency')
    return {'param': 'lpfFrequency', 'da': da, 'a': a,
            'da_tick': da_tick, 'a_tick': a_tick, 'passi': passi}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_apri_filtro()"`
Expected: PASS (o SALTATO se manca `TEMPL4.XML`; in tal caso lanciare la suite intera, che ha le fixture).

- [ ] **Step 5: Commit**

```bash
git add tools/delugexml/musica.py tests/test_all.py
git commit -m "feat: MU.apri_filtro -- la rampa del cutoff in unita' display

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: `MU.sidechain` — il pompaggio interno del Deluge

**Files:**
- Modify: `tools/delugexml/musica.py` (nuova funzione + helper `_sound_di_drum`)
- Test: `tests/test_all.py` (`test_sidechain`)

**Interfaces:**
- Consumes: `sound.container`, `song.drums`, `kit.drum_index_of`, `parser.Node`.
- Produces:
  - `sidechain(doc, bersaglio, *, quanto='0xDE000000', sync=7, manda_da=None) -> dict` — accende il sidechain: sul `bersaglio` (nodo strumento synth) scrive `sidechainCompressorVolume=quanto` e assicura `sidechainCompressorShape` nel container, e imposta `syncLevel=sync`/`syncType=0` nel figlio `<sidechain>`; se `manda_da=(kit, nome_drum)`, mette `sideChainSend="2147483647"` sul `<sound>` di quel drum (il trigger). Ritorna un racconto con i valori scritti e `da_verificare=True`.
  - `_sound_di_drum(kit, nome) -> Node` — il nodo `<sound>` del drum che si chiama `nome`.

- [ ] **Step 1: Write the failing test**

In `tests/test_all.py`, aggiungi:

```python
def test_sidechain():
    """MU.sidechain: send sul kick + volume-ducking sul bersaglio + <sidechain> sync.

    Struttura verificata dai file veri (schema c1.3.0). La MAGNITUDINE del duck
    e' [da verificare] all'orecchio: il test controlla la struttura, non il suono.
    """
    from delugexml import musica as MU                          # noqa: PLC0415
    from delugexml import sound as SND                          # noqa: PLC0415
    from delugexml import create as C                           # noqa: PLC0415
    import warnings                                             # noqa: PLC0415
    piano = REFS / 'synths' / 'Pianism I.XML'
    kitf = REFS / 'kits' / '808 From Mars.XML'
    tem = REFS / 'songs' / 'TEMPL0.XML'
    if not (piano.exists() and kitf.exists() and tem.exists()):
        salta('test_sidechain', 'manca una fixture')
        return
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(tem)
        iP, cP = C.add_track(doc, str(piano), name='STAB', folder='SYNTHS',
                             length=384, playing=True)
        kit, cK = C.add_track(doc, str(kitf), name='K808', folder='KITS',
                              length=384, playing=True)
        r = MU.sidechain(doc, iP, quanto='0xDE000000', sync=7,
                         manda_da=(kit, 'BD A 808 Decay C 04'))
    # il bersaglio duck: l'attributo c'e' nel defaultParams dello strumento...
    check('il ducking e scritto sul bersaglio',
          SND.container(iP).get('sidechainCompressorVolume') == '0xDE000000',
          SND.container(iP).get('sidechainCompressorVolume'))
    # ...e PROPAGATO ai <params> della clip (e' lei che suona)
    check('il ducking e propagato alla clip',
          SND.container(cP).get('sidechainCompressorVolume') == '0xDE000000',
          SND.container(cP).get('sidechainCompressorVolume'))
    check('sidechain conta le clip toccate', r.get('clip_ducked') == 1, str(r))
    check('lo shape del sidechain e presente',
          SND.container(iP).get('sidechainCompressorShape') == '0xDC28F5B2',
          SND.container(iP).get('sidechainCompressorShape'))
    sc = iP.find('sidechain')
    check('il <sidechain> ha il sync chiesto',
          sc is not None and sc.get('syncLevel') == '7', str(sc and sc.attrs))
    # il kick manda al sidechain
    kick = MU._sound_di_drum(kit, 'BD A 808 Decay C 04')
    check('il kick manda al sidechain (send pieno)',
          kick.get('sideChainSend') == '2147483647', kick.get('sideChainSend'))
    check('sidechain dichiara il valore da verificare',
          r.get('da_verificare') is True, str(r))
    check('il documento resta valido', MU.verifica(doc) == [], str(MU.verifica(doc)))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_sidechain()"`
Expected: FAIL/AttributeError — `MU.sidechain` non esiste.

- [ ] **Step 3: Write minimal implementation**

In `tools/delugexml/musica.py`:

```python
def _sound_di_drum(kit, nome: str):
    """Il nodo <sound> del drum che si chiama `nome`, dentro un <kit>."""
    from . import song as S                                     # noqa: PLC0415
    from . import kit as K                                      # noqa: PLC0415
    return S.drums(kit)[K.drum_index_of(kit, nome)]


def sidechain(doc, bersaglio, *, quanto: str = '0xDE000000', sync: int = 7,
              manda_da=None) -> dict:
    """Accende il SIDECHAIN interno del Deluge -- il pompaggio della house.

    NON e' il compressore (`<audioCompressor>`): quello e' un'altra cosa e non si
    tocca. Il sidechain e' un inviluppo attack/release innescato dalle note di un
    kit; qui si fanno i tre pezzi:

    1. il TRIGGER -- `manda_da=(kit, nome_drum)` mette `sideChainSend` al massimo
       sul `<sound>` di quel drum (di solito il kick): e' lui a innescare la pompa;
    2. il DUCKING -- sul `bersaglio` (nodo strumento synth: basso, stab) scrive
       `sidechainCompressorVolume=quanto` nel container e assicura
       `sidechainCompressorShape`: e' il volume che respira sotto la cassa;
    3. il TEMPO -- `syncLevel=sync`/`syncType=0` nel figlio `<sidechain>`.

    ⚠️ STRUTTURA verificata dai file veri (schema c1.3.0); la MAGNITUDINE e il
    VERSO del duck sono `[da verificare]` all'orecchio -- `sidechainCompressorVolume`
    non e' in `param_ids`, quindi si scrive come attributo grezzo, non via
    `sound.set`. I valori osservati nei file: 0xF2000000, 0xDE000000, 0xFC000000.
    Il pompaggio si sente solo DOVE batte il kick: l'arrangiamento lo accende e
    lo spegne senza automazione (nel breakdown manca il trigger).
    """
    from . import sound as SND                                  # noqa: PLC0415
    from . import song as S                                     # noqa: PLC0415

    def _duck(nodo):
        cont = SND.container(nodo)
        if cont is None:
            return False
        cont.set('sidechainCompressorVolume', quanto)
        if not cont.has('sidechainCompressorShape'):
            cont.set('sidechainCompressorShape', '0xDC28F5B2')
        return True

    # il ducking va nel defaultParams dello strumento E nei <params> di OGNI sua
    # clip: e' il params della clip che suona (creata come copia del default). Se
    # si scrivesse solo sul default, le clip gia' create non pomperebbero.
    if not _duck(bersaglio):
        raise ValueError(f'<{bersaglio.tag}> non ha un contenitore di parametri')
    n_clip = 0
    for _, clip in S.clips(doc):
        if S.instrument_of(doc, clip) is bersaglio and _duck(clip):
            n_clip += 1

    # il tempo del pompaggio: l'elemento <sidechain> sta sullo STRUMENTO
    sc = bersaglio.find('sidechain')
    if sc is None:
        sc = bersaglio.append(Node(tag='sidechain'))
    sc.set('syncLevel', str(sync))
    sc.set('syncType', '0')

    inviato = None
    if manda_da is not None:
        kit, nome = manda_da
        _sound_di_drum(kit, nome).set('sideChainSend', '2147483647')
        inviato = nome
    return {'bersaglio': getattr(bersaglio, 'tag', '?'), 'quanto': quanto,
            'sync': sync, 'clip_ducked': n_clip, 'manda_da': inviato,
            'da_verificare': True}
```

Nota: `Node` è già importato in `musica.py` (usato da `passi`/`scrivi`). Se non lo fosse, aggiungere `from .parser import Node` in cima; verificare con un grep prima di aggiungerlo.

⚠️ **Ordine in `house2_scritto`:** chiamare `MU.sidechain` **dopo** aver creato tutte le clip dei bersagli, così la propagazione le raggiunge tutte.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_sidechain()"`
Expected: PASS (o SALTATO se mancano le fixture).

- [ ] **Step 5: Commit**

```bash
git add tools/delugexml/musica.py tests/test_all.py
git commit -m "feat: MU.sidechain -- il pompaggio interno (send + ducking + sync)

Struttura dai file veri; la magnitudine del duck resta [da verificare].

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: `tools/house2_scritto.py` — l'arco a 32 battute

**Files:**
- Create: `tools/house2_scritto.py`
- Test: `tests/test_all.py` (`test_house2_scritto`)

**Interfaces:**
- Consumes: `MU.forma`, `MU.apri_filtro`, `MU.sidechain`, `MU.passi`, `MU.voci`, `MU.sigla`, `create.add_track`, `arranger`, `song`.
- Produces: `costruisci() -> tuple[doc, dict]` (come `house_scritto.py`), che stende l'arco e ritorna `(doc, {})`. `verifica(doc)` vuota.

**L'arco (32 battute), realizzato con `MU.forma`.** Le sezioni e le clip che suonano in ciascuna:

| sezione (mappa) | battute | clip che suonano |
|---|---|---|
| `intro` | 8 | `drum_intro` (kick + closed hat; open hat dalla 5ª battuta) |
| `build` | 4 | `drum_full`, `bass`, `stab_build` (col cutoff che apre) |
| `drop` | 8 | `drum_full`, `bass`, `stab` |
| `break` | 4 | `bass`, `stab_filtrato` (niente drum → niente pompa) |
| `drop` | 8 | (ripete: `MU.forma` riusa le stesse clip di `drop`) |

- `mappa = 'intro build drop break drop'`, `battute_per={'intro':8,'build':4,'drop':8,'break':4}`.
- Il sidechain si imposta **una volta** su `bass` e `stab` (send dal kick di `drum_full`), prima di stendere la forma: pompa da sé dove c'è il kick (nei drop sì, nel break no).
- `stab_build` e `stab_filtrato` sono clip **distinte** dello stesso strumento stab: la prima con `apri_filtro` (chiuso→aperto), la seconda con cutoff basso fisso (`MU.applica_verbo(..., 'piu chiuso')` o un valore fisso).

- [ ] **Step 1: Write the failing test**

```python
def test_house2_scritto():
    """house2_scritto.py: l'arco a 32 battute (build/drop) con filtro e sidechain.
    Chiude le caselle 9 e 10 della scheda house."""
    from delugexml import musica as MU                          # noqa: PLC0415
    from delugexml import sound as SND, arranger as AR          # noqa: PLC0415
    try:
        import house2_scritto as H2                             # noqa: PLC0415
    except FileNotFoundError:
        salta('test_house2_scritto', 'manca una fixture')
        return
    try:
        doc, _ = H2.costruisci()
    except FileNotFoundError:
        salta('test_house2_scritto (build)', 'manca una fixture')
        return
    check('il pezzo HOUSE2 e valido', MU.verifica(doc) == [], str(MU.verifica(doc)))
    # l'arco copre 32 battute
    est = AR.extent(doc)
    check('l arco e lungo 32 battute',
          est is not None and est[1] == 32 * MU.TICK_PER_BATTUTA, str(est))
    # il sidechain e' impostato sui bersagli
    bass = H2.strumento(doc, 'BASS')
    stab = H2.strumento(doc, 'STAB')
    check('il basso duck',
          SND.container(bass).get('sidechainCompressorVolume') is not None)
    check('lo stab duck',
          SND.container(stab).get('sidechainCompressorVolume') is not None)
    # il kick manda al sidechain
    kit = H2.strumento(doc, 'K808')
    kick = MU._sound_di_drum(kit, H2.KICK)
    check('il kick manda al sidechain', kick.get('sideChainSend') == '2147483647')
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_house2_scritto()"`
Expected: FAIL — `house2_scritto` non esiste.

- [ ] **Step 3: Write the module `tools/house2_scritto.py`**

Struttura (parti da `house_scritto.py`, che è approvato; qui si aggiungono forma, filtro, sidechain). Punti fissi:
- costanti identiche a `house_scritto.py` (KIT, PRESET_*, i nomi drum, BPM 124, SWING 55, loop `Am9|Dm9|Fmaj9|Em9`);
- `strumento(doc, nome)` = helper che ritrova lo strumento per nome (`song.instruments` filtrando `name`);
- funzioni che ritornano i dict di note per ciascuna clip (`drum_intro`, `drum_full`, `basso`, `stab`), riusando `MU.passi`/`MU.voci` come nell'esempio approvato;
- `costruisci()`:
  1. carica `TEMPL0`, set BPM/swing/scala, `MU.togli` gli strumenti del template;
  2. `add_track` per STAB, BASS, K808 (ognuno nasce con **una** clip di sessione);
  3. **clip di sezione distinte**: dove un solo pattern non basta, si duplica la clip dello strumento con `song.duplicate_clip(doc, index, name=…)` e vi si scrivono note diverse. La prima clip dello strumento fa una sezione, le duplicate le altre:
     - **K808**: la clip nativa → `drum_full`; una duplicata → `drum_intro` (solo kick + closed hat, open hat dalla 5ª battuta);
     - **STAB**: la nativa → `stab` (drop); una duplicata → `stab_build`; una duplicata → `stab_filtrato` (break);
     - **BASS**: la nativa → `bass`, riusata in build/drop/break/drop (stesso contenuto);
     scrivere le note con `MU.scrivi` in ciascuna. ⚠️ `duplicate_clip` prende un **indice** in `song.clips(doc)`: ricavarlo con `arranger.index_of(doc, clip)[0]` sulla clip nota. ⚠️ Due clip dello stesso strumento sono variazioni **mutuamente esclusive in session** ma **legittime nell'arranger a tempi diversi** (è l'arco): controllare che `MU.avvertenze(doc)` non segnali «due clip nella stessa sezione» — se lo fa, dare `section` distinte alle duplicate;
  4. `MU.apri_filtro(doc, stab_build, 10, 45, 0, 4*B)` — il cutoff apre sulle 4 battute del build; su `stab_filtrato` invece cutoff basso fisso (`MU.applica_verbo(doc, iStab_clip?, 'piu chiuso')` sul suono, o un valore fisso con `sound.set`);
  5. `MU.sidechain(doc, bass, manda_da=(kit, KICK))` e `MU.sidechain(doc, stab, manda_da=(kit, KICK))` — una volta, a livello di suono;
  6. `MU.forma(doc, 'intro build drop break drop', sezioni, battute_per={'intro':8,'build':4,'drop':8,'break':4})` con `sezioni = {'intro':[drum_intro], 'build':[drum_full, bass, stab_build], 'drop':[drum_full, bass, stab], 'break':[bass, stab_filtrato]}`;
  7. `A.open_in_arranger(doc)`; ritorna `(doc, {})`.

⚠️ `MU.forma` piazza la STESSA clip a più posizioni per una sezione che si ripete: le due `drop` riusano gli stessi oggetti-clip (`drum_full`/`bass`/`stab`), ed è il comportamento voluto (una clip instanziata due volte).

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe tools/house2_scritto.py` (deve stampare `verifica: vuota`), poi
`.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_house2_scritto()"`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/house2_scritto.py tests/test_all.py
git commit -m "feat: house2_scritto -- l'arco build/drop con filtro e sidechain

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: l'istruzione `docs/istruzioni/arrangiamento-house.md`

**Files:**
- Create: `docs/istruzioni/arrangiamento-house.md`

Un documento solo (build/drop + filtro + sidechain sono lo stesso gesto). Segue la forma delle altre istruzioni house (`batteria-house.md`, `basso-house.md`): perimetro → gradi di prova → vocabolario → vincoli → «come si decide una sezione» → esempio lavorato → cosa manca. Contenuto obbligato:

- **l'arco** (intro/build/drop/break/drop), cosa entra/esce, con la tabella del pezzo;
- **il filtro che apre** (`MU.apri_filtro`, la rampa del cutoff nel build);
- **il sidechain interno** (`MU.sidechain`): la distinzione **dal compressore** in chiaro (è la trappola), i tre pezzi (send/ducking/sync), e che pompa **da sé dove batte il kick** — il break lo spegne senza automazione;
- **i vincoli**: la cassa si buca **solo** nel break; il drop non aggiunge note, **toglie e rimette parti** + apre il filtro; il pompaggio è mix, non nota;
- **il grado di prova**: `[LIB]`+`[DEC]` (convenzione dance) per l'arco e il filtro; `[OSS]` per la struttura XML del sidechain (dai file veri) + `[da verificare]` per la magnitudine del duck;
- link reciproci con `batteria-house.md` e `basso-house.md`; e riga «esempio lavorato: `tools/house2_scritto.py`».

- [ ] **Step 1: Scrivere il file** (con `write_bytes`/LF).
- [ ] **Step 2: Verificare i fine-riga**: `git diff --stat` == `git diff --stat --ignore-cr-at-eol`.
- [ ] **Step 3: Commit**

```bash
git add docs/istruzioni/arrangiamento-house.md
git commit -m "istruzioni: house build/drop + filtro + sidechain interno

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: la scheda `house.md` e l'indice `MUSICA.md`

**Files:**
- Modify: `docs/repertori/house.md` (caselle 9 e 10; note «cosa manca»; verdetto)
- Modify: `docs/MUSICA.md` (riga d'indice house/techno)

- [ ] **Step 1: Aggiornare `house.md`**
  - **casella 9 (Forma e densità):** da «Vuota» a piena — l'arco build/drop con `MU.forma`+arranger, la tabella delle sezioni, `[LIB]`+`[DEC]`; link all'istruzione;
  - **casella 10 (Sul Deluge):** da «Parziale» a piena — filtro in movimento (`MU.apri_filtro`) + sidechain interno (`MU.sidechain`, `[OSS]` struttura + `[da verificare]` magnitudine), togliere il «⚠️ Cosa manca» risolto;
  - aggiornare l'intestazione «Parziale»/«manca proprio ciò che fa il genere» ora che 9 e 10 sono coperte;
  - aggiungere la riga «esempio: `tools/house2_scritto.py`» e il verdetto d'ascolto (lasciato **in sospeso** finché l'utente non ascolta — non scrivere «funziona» senza il suo verdetto, regola 4 e «non dire verificato avendo ascoltato»/viceversa).

- [ ] **Step 2: Aggiornare l'indice in `docs/MUSICA.md`** — la riga di house/techno: 9 e 10 non più vuote (usare gli stessi simboli di stato delle altre righe; **titoli delle caselle identici** al contratto).

- [ ] **Step 3: Verificare i fine-riga** su entrambi i file (come sopra).

- [ ] **Step 4: Lanciare la suite INTERA** (contratto delle schede):

Run: `.venv/Scripts/python.exe tests/test_all.py`
Expected: verde (i test nuovi passano o SALTANO senza fixture; nessun rosso oltre al noto `COPPIE_OSSERVATE` locale descritto in `HANDOFF` §2).

- [ ] **Step 5: Commit**

```bash
git add docs/repertori/house.md docs/MUSICA.md
git commit -m "repertori: house -- caselle 9 (build/drop) e 10 (filtro+sidechain)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: caricamento e ascolto (chiude il giro)

**Files:** nessuno (operativo). È il passo che pinna il `[da verificare]`.

- [ ] **Step 1: Generare il file** con `house2_scritto.costruisci()` e scriverlo con `write_file(doc, out, FormatTable.load('out/format_table.json'))`; `MU.verifica(doc)` deve essere vuota.
- [ ] **Step 2: Destinazione** con `MU.destinazione('house', 2, 'SONGS')` → `/SONGS/DelugePal/HOUSE02.XML` (mai a mano; se `HOUSE02` esiste, incrementare).
- [ ] **Step 3: Trasferire** via `tools/dsysex.py` **da PowerShell** (memoria `dsysex-da-powershell`), senza troncare l'output di `put` (memoria `dsysex-put-non-troncare`). Se il Deluge non risponde al `ping`: scrivere il file locale e **dirlo**, non fingere il caricamento (regola: Deluge non collegato).
- [ ] **Step 4: L'utente ascolta.** Verificare **guardando/ascoltando sul Deluge**, non dal file (regola 0). Domande all'orecchio: il filtro apre nel build? il drop pompa? il break respira senza pompa? il duck è troppo/poco (regolare `quanto` in `MU.sidechain`) e il verso è giusto?
- [ ] **Step 5: Pinnare il `[da verificare]`.** Col verdetto: fissare `quanto`/`sync`/attack-release nel `default` di `MU.sidechain` e in `house2_scritto.py`, aggiornare la scheda con il verdetto reale e il grado di prova che sale da `[da verificare]` a `[OSS]`/`[MIS-sul-device]`. Commit finale.

---

## Self-Review

**1. Spec coverage:**
- primitive `MU.sidechain` + `MU.apri_filtro` → Task 1, 2 ✓
- pezzo `house2_scritto.py` + test → Task 3 ✓
- istruzione `arrangiamento-house.md` → Task 4 ✓
- scheda 9/10 + indice → Task 5 ✓
- sidechain interno (non compressore), pin da coppia controllata → Task 2 (struttura) + Task 6 (valore) ✓
- filtro che apre → Task 1 + Task 3 ✓
- sidechain una volta a livello di suono, pompa dove batte il kick → Task 2 impl + Task 3 arco ✓
- metodo = ascolto pieno dell'utente → Task 6 ✓
- YAGNI (niente acid continuo, niente lead, niente primitivo d'arrangiamento nuovo — si riusa `MU.forma`) ✓

**2. Placeholder scan:** nessun TODO di contenuto. La creazione delle clip di sezione è risolta (`song.duplicate_clip` + `arranger.index_of`, con i caveat su mutua esclusività e `avvertenze`). L'unico valore lasciato aperto **di proposito** è la magnitudine del ducking (`[da verificare]` in Task 2/6): non è un buco del piano ma il punto che il metodo del progetto affida all'orecchio.

**3. Type consistency:** `MU.sidechain`, `MU.apri_filtro`, `_sound_di_drum`, `costruisci`, `strumento(doc, nome)` usati con le stesse firme nei task 1-3 e nei test. `sidechainCompressorVolume`/`sideChainSend`/`sidechainCompressorShape`/`syncLevel` scritti con gli stessi nomi ovunque, coerenti con lo schema c1.3.0.
