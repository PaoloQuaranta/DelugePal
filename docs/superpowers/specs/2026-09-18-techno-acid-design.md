# Techno acid — il 303, la linea, il filtro che evolve — progetto

**Data:** 18 settembre 2026
**Cos'è:** il filo lasciato nominato ma non implementato dall'arrangiamento house
(`docs/istruzioni/arrangiamento-house.md`, «cosa manca»): il **suono acid** — il
TB-303 — con la sua linea che rotola e il filtro che evolve. Chiude la **casella 8**
(melodia/lead: la linea acid *è* il riff del techno, oggi vuota) della scheda
`docs/repertori/house.md` e approfondisce la **10** (il suono in movimento).

## Perché, e cosa si è deciso

Il techno acid è **suono** prima che note: una linea quasi ferma (una-due altezze
che rotolano sui sedicesimi) resa viva dal **filtro risonante** che la scolpisce
per nota (lo *squelch* del 303) e che **evolve** lungo il pezzo. È il lato del
genere che le istruzioni house rimandavano.

Deciso in brainstorming il 18 settembre 2026:

- **pezzo nuovo** `tools/acid_scritto.py` (techno minimale, non innesto su house2):
  l'acid techno ha un feel suo — dritto, scuro, ipnotico;
- **303 pieno + sweep sull'arco**: lo squelch per-nota (env→cutoff + risonanza +
  accento + slide) **e** una rampa lenta di cutoff/risonanza sulla sezione;
- **la linea acid sta nell'esempio**, non è una primitiva (è compositiva);
- **la forma d'onda è un parametro** di `MU.acid` (`onda='saw'|'square'`), default
  **saw** (l'acid iconico); entrambe sono forme d'onda vere del 303;
- **techno**: dritto (`set_swing(50)`), ~132, scuro, armonia minima (un vamp su
  una nota).

⚠️ **Metodo (deciso):** suono = **ascolto pieno dell'utente**. Lo spec porta la
`verifica()` pulita e il file; i valori del suono (risonanza, amount dei cavi,
decay di env2, tempo di glide, profondità dello sweep) sono `[DEC]` di partenza,
`[da verificare]` all'orecchio.

## Il meccanismo, dai file veri e dal corpus

Ordine di ricerca rispettato: doc/guidebook → sorgente/schema → libreria. Fatti
grounded:

- **I parametri e i patch cable di un synth vivono sulla CLIP**, non sullo
  strumento: `create.add_track` sposta il `<defaultParams>` del preset sul
  `<params>` della clip (lezione già pagata con `MU.sidechain`). Quindi
  risonanza, cutoff base e i patch cable dell'acid si scrivono su **ogni clip**
  del bersaglio; la **struttura** (mono, osc, portamento) sta sullo **strumento**.
- **I due patch cable dell'acid sono attestati nel corpus** (`sound._COPPIE`):
  `('envelope2','lpfFrequency')` **157** volte (lo squelch per nota),
  `('velocity','lpfFrequency')` **129** (l'accento). Terreno battuto, non ipotesi.
- `lpfResonance` e `lpfFrequency` sono in `param_ids` (automatizzabili, con
  `mark_view`); `portamento` è un parametro UNPATCHED_SOUND. ⚠️ Fra i due filtri,
  **solo `lpfFrequency` è verificato sul dispositivo** (`param_ids`): la risonanza
  in automazione è `[da verificare]` — coerente col metodo (l'orecchio decide).
- Lo **slide** del 303 è il glide del mono: in `polyphonic='mono'` due note
  **legate** (la prima che sfora sull'attacco della seconda) glissano; il tempo
  del glide è `portamento`.
- L'**accento** del 303: `velocity → lpfFrequency` (le note accentate aprono più
  il filtro) — la velocity alta *è* l'accento.

## I quattro artefatti di questo giro

### 1. La primitiva del suono — `MU.acid`

```
acid(doc, bersaglio, *, onda='saw', risonanza=40, cutoff=8, env_cutoff=30,
     acc_cutoff=15, glide=15, env2_decay=18) -> dict
```

Trasforma il synth `bersaglio` (nodo strumento) in un 303. Tocca due livelli, come
`MU.sidechain`:

- **strumento**: `polyphonic='mono'` (`structure.set_attr`), osc1 `type=onda`
  (`structure.set_osc`), e `portamento` (il glide, valore `glide`);
- **ogni clip del bersaglio** (`song.clips` + `instrument_of`): `lpfResonance`
  alto (`risonanza`), `lpfFrequency` basso (`cutoff`, così l'inviluppo ha spazio
  per aprirlo), i patch cable `envelope2→lpfFrequency` (amount `env_cutoff`) e
  `velocity→lpfFrequency` (amount `acc_cutoff`), e la forma percussiva di env2
  (decay `env2_decay`, sustain basso).

Riconosce il bersaglio come `MU.sidechain`. **Racconta** cosa ha cambiato
(regola 4) e dichiara `da_verificare=True`. I valori sono `[DEC]`+`[da verificare]`.

⚠️ `portamento` e i patch cable possono **non esistere** nei params di partenza:
si aggiungono al container (attributi/nodi verificati), non via `sound.set` che
pretende l'esistenza. `set_patch_cable` crea il `<patchCables>` da sé.

### 2. La generalizzazione — `MU.automatizza`, e `apri_filtro` come wrapper

```
automatizza(doc, clip, param, da, a, da_tick, a_tick, *, passi=7) -> dict
```

Quello che oggi fa `apri_filtro` ma per **qualunque** parametro (in unità display
0-50): converte, `automation.ramp_internal`, scrive il blob nel container della
clip, `mark_view`. `apri_filtro(...)` diventa `automatizza(..., 'lpfFrequency')`
(retrocompatibile, stessi argomenti). Serve perché il macro-sweep acid rampa
**cutoff e risonanza**, non solo il cutoff.

⚠️ `mark_view` vuole il param in `param_ids`: `lpfResonance` c'è. Per un parametro
non in tabella, `automatizza` scrive comunque il blob ma **salta** `mark_view` (e
lo dice nel racconto) invece di sollevare.

### 3. Il pezzo — `tools/acid_scritto.py`

Techno minimale e dritta:

- **~132 BPM, `set_swing(50)`** (dritto), scala su **La** (vamp su una nota);
- **batteria**: four-on-the-floor 808/909 — cassa ogni movimento, closed hat sui
  sedicesimi, open hat sui levare, clap sul 2-4 (dal drop). Scura, minimale;
- **la linea acid** (nell'esempio, funzione `linea()`): sedicesimi che rotolano,
  quasi tutti su **La**, con qualche ottava/♭7/quinta; **accenti** (velocity ~120
  su alcuni passi, contro ~70 di base) e **slide** (note legate, `length` che
  sfora sul passo dopo → il mono glissa);
- **il suono**: `MU.acid(doc, iAcid, onda='saw')`;
- **l'arco** (con `MU.forma`): intro (batteria + acid filtrato bassissimo) →
  build (il filtro **apre**: `MU.automatizza` su cutoff e risonanza) → drop (tutto,
  filtro aperto) → un breakdown corto. Più compatto di house2 (il movimento acid è
  il filtro, non tante sezioni);
- `verifica()` vuota; `test_acid_scritto` che controlla il suono (mono, patch cable
  presenti sulle clip, portamento), l'arco e lo sweep.

### 4. L'istruzione — `docs/istruzioni/acid.md`

Forma collaudata (perimetro → gradi → vocabolario → vincoli → come si decide →
esempio → cosa manca). Copre:

- **cos'è il 303**: un osc (saw **o** quadra), LPF **molto risonante**, inviluppo
  sul cutoff, accento, slide. Il carattere è il **filtro**, non le note;
- **il suono** (`MU.acid`): i due livelli, i patch cable attestati, la forma d'onda;
- **la linea**: rada in altezza, fitta in ritmo; accenti e slide, e cosa fanno;
- **il filtro che evolve** (`MU.automatizza` su cutoff/risonanza): l'anima dell'acid;
- **i vincoli**: risonanza alta o non è acid; la linea non è melodica (è ritmo +
  filtro); l'accento è la velocity; lo slide è il legato in mono;
- link con `arrangiamento-house.md` (l'acid è un caso del suo «filtro in movimento»)
  e `basso-house.md`.

## La scheda e l'indice

- `docs/repertori/house.md`: **casella 8** da «Vuota» a piena (il lead/riff acid,
  `[LIB]`+`[DEC]`); **casella 10** ampliata (il suono acid, i patch cable `[OSS]`);
  casella 3/4 nota il tempo/feel techno acid; verdetto d'ascolto **in sospeso**.
- `docs/MUSICA.md`: la riga house/techno, casella 8 non più vuota.

## Cosa resta fuori (YAGNI)

- il **vocal chop** (l'altra metà della casella 8): è `audio.py` (campioni), non note;
- la **distorsione/overdrive** sul 303 (tipica dell'acid spinto): è un effetto di
  suono in più, nominato non implementato;
- una primitiva per la **linea** acid: sta nell'esempio, per scelta;
- il **tuning fine** dei valori 303: è ascolto, non spec.

## Rischi e come si chiudono

| rischio | mossa |
|---|---|
| valori 303 (risonanza/amount/decay/glide) sbagliati all'orecchio | `[DEC]` di partenza esposti come argomenti di `MU.acid`; l'utente li tara; `da_verificare` nel racconto |
| risonanza in automazione non verificata sul device | `[da verificare]`; se non regge, si tiene la risonanza fissa alta e si rampa il solo cutoff |
| lo slide non glissa (note non abbastanza legate, o portamento a 0) | `portamento`>0 e `length` delle note-slide che sfora sul passo dopo; verificare all'ascolto |
| patch cable/param assenti nei params di partenza | aggiungerli al container (`set_patch_cable` crea il contenitore); mai `sound.set` su un attributo assente |
| fine-riga corrotti | `write_bytes`/`newline=''`; `git diff --stat` == `--ignore-cr-at-eol` prima di committare |
| `print()` con `⚠️` | vietato: console cp1252, solo ASCII |

## Fatto =

- `MU.acid` e `MU.automatizza` con i test verdi; `apri_filtro` ancora verde (wrapper);
- `acid_scritto.py` che costruisce l'arco, `verifica()` vuota, `test_acid_scritto` verde;
- l'istruzione, la scheda (caselle 8 e 10) e l'indice aggiornati e coerenti;
- il file caricato sul Deluge per l'ascolto — il verdetto chiude il giro.
