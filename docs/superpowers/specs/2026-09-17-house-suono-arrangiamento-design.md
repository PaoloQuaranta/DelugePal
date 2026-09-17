# House: suono + arrangiamento (build/drop, filtro, sidechain) — progetto

**Data:** 17 settembre 2026
**Cos'è:** chiude le due caselle dichiarate vuote/parziali della scheda
`docs/repertori/house.md` — la **9 (forma: build/drop)** e la **10 (suono:
filtro in movimento + sidechain)**. È il «prossimo lavoro vero sul genere»
nominato in `HANDOFF.md` («ma l'essenza di house/techno resta da fare»).

## Perché, e cosa si è deciso

La four-on-the-floor c'era già (batteria, basso, stab, esempio
`tools/house_scritto.py`, verdetto d'ascolto *«funziona»*). Ma la scheda lo dice
in chiaro: *«manca proprio ciò che fa il genere»* — l'arrangiamento e il suono in
movimento. Una battuta di house non dice niente di un pezzo house; il genere
**è forma** (build/drop) e **è filtro/pompaggio**.

Deciso in brainstorming il 17 settembre 2026:

- **risultato:** un **pezzo lavorato** + **primitive riusabili** (non solo il pezzo);
- **arco:** **compatto, 32 battute**;
- **house**, non techno (~124 BPM, swing 55), sul loop già approvato
  `Am9 | Dm9 | Fmaj9 | Em9`;
- **sidechain interno del Deluge**, non un'automazione di volume finta, e
  **NON** il compressore (`<audioCompressor>`) — correzione esplicita dell'utente;
- **entrambe** le primitive: `MU.sidechain` **e** `MU.apri_filtro`.

⚠️ **Metodo (deciso, `HANDOFF` §prossimo lavoro):** suono e ritmo si chiudono con
l'**ascolto pieno dell'utente**. Questo documento porta la `verifica()` pulita e
il file; il **verdetto è l'orecchio**, non il `[CALC]`.

## Il meccanismo del sidechain, dal manuale (non dedotto)

Ordine di ricerca rispettato: doc community → schema c1.3.0 → libreria. Fonte:
[delugecommunity.com](https://delugecommunity.com) (Menu Hierarchies, Tips and
Tricks) e `docs/SCHEMA_song_c1.3.0.md`.

Sul Deluge c1.3.0 **sidechain e compressore sono due cose separate**:

| elemento XML | cos'è | qui |
|---|---|---|
| `<audioCompressor>` | il compressore vero (Threshold/Ratio/Blend/HPF) | **NON si tocca** |
| `<sidechain>` | inviluppo attack/release **innescato da note di kit**, sync a tempo | **è il pompaggio** |

Come pompa la house, in tre pezzi:

1. **il trigger** — la cassa **manda** al sidechain: attributo `sideChainSend`
   sulla riga di kit del kick (i kit di serie hanno il kick a **50** = pieno);
2. **il ducking** — i suoni che devono respirare (basso, stab) abbassano il
   volume a ogni cassa: parametro `sidechainCompressorVolume` (negativo = duck)
   nei loro `<defaultParams>`/`<soundParams>`, più `sidechainCompressorShape`;
3. **il tempo** — l'inviluppo del sidechain ha Attack/Release/Sync: elemento
   `<sidechain attack=… release=… syncLevel=… syncType=…>` (già nel template di
   `tools/delugexml/audio.py`).

⚠️ **Il corpus NON ha un esempio di volume-ducking** (`grep` su `refs/`: zero
`sidechainCompressorVolume`, zero `source="compressor"` verso `volume`). È il caso
della memoria *«il corpus non è autoritativo»*: assente dal corpus ≠ assente dal
firmware. Quindi:

> **Il valore numerico esatto del ducking e del send si pinna da una coppia
> controllata sul Deluge (o round-trip), non si inventa.** È la regola che è già
> costata due difetti (`FINDINGS` §6-quater, §6-quinquies). Se il Deluge non è
> collegato al momento della generazione, si scrive il file, lo si dichiara, e si
> lascia il ducking a un valore prudente **marcato da verificare**.

## Cosa esiste già (si riusa, non si riscrive)

| serve per | c'è già |
|---|---|
| la rampa del cutoff (il filtro che apre) | `automation.ramp()` / `ramp_internal()` su `lpfFrequency` |
| lo stato di vista dell'automazione | `automation.mark_view()` |
| la mappa di forma per sezioni | `MU.forma(doc, mappa, sezioni, …)` |
| piazzare clip diverse per sezione | `arranger.place()` / `place_unique()` |
| scurire/aprire il filtro a valore fisso | `MU.applica_verbo` (`lpfFrequency`) |

## I tre artefatti di questo giro

### 1. Le due primitive nuove

#### `MU.sidechain(doc, bersaglio, *, quanto, sync, manda_da)`

Accende il pompaggio del Deluge. Un'unica chiamata fa i tre pezzi:

- **`manda_da`**: lo strumento/kit + nome-drum del kick → gli mette
  `sideChainSend` al massimo (il trigger);
- **`bersaglio`**: lo strumento che deve respirare (basso, stab) → gli scrive
  `sidechainCompressorVolume` (il ducking) e `sidechainCompressorShape`, e
  imposta l'elemento `<sidechain>` con `syncLevel`/`syncType`;
- **`quanto`**: la profondità del duck in unità display (0-50), `[DEC]` un
  default house sensato;
- **`sync`**: la figura del pompaggio (movimento / croma), tradotta in
  `syncLevel`/`syncType`.

Riconosce il bersaglio come fa `MU.togli`/`trasponi` (strumento). **Racconta**
cosa ha cambiato (regola 4). ⚠️ Il valore esatto di `quanto→sidechainCompressorVolume`
e di `sideChainSend` è **pinnato da coppia controllata**, non indovinato: finché
non lo è, la funzione lo dichiara nel racconto come `[da verificare]`.

#### `MU.apri_filtro(doc, clip, da_display, a_display, da_tick, a_tick, *, passi)`

Sottile wrapper di `automation.ramp`: prende i valori del cutoff in **unità
display (0-50)** invece che int32, li converte, e scrive la rampa
sull'`lpfFrequency` della clip fra `da_tick` e `a_tick`, chiamando `mark_view`
così l'automazione si vede. Serve perché chi scrive un pezzo pensa «apri da 10 a
45», non in `0x80000000`.

### 2. Il pezzo lavorato — `tools/house2_scritto.py`

L'arco a 32 battute, sul loop approvato. Cinque sezioni, ognuna una clip
d'arranger:

| sezione | batt. | cosa suona | suono |
|---|---|---|---|
| **intro** | 8 | cassa + closed hat; open hat da metà | filtro un po' chiuso |
| **build** | 4 | entrano basso e stab | **cutoff apre** (rampa) |
| **drop** | 8 | tutto | **sidechain acceso**, filtro aperto |
| **breakdown** | 4 | via la cassa; stab + basso | stab **filtrato** |
| **drop 2** | 8 | rientro pieno | sidechain, filtro aperto |

- realizzato con `MU.forma` (entra/esce) + `arranger.place`/`place_unique` per le
  clip di sezione;
- la cassa **si buca solo** nel breakdown (l'unica eccezione ammessa dalle
  istruzioni house);
- il sidechain acceso nei drop, spento altrove → il pezzo respira;
- `verifica()` vuota prima del caricamento; test `test_house2_scritto` che
  costruisce il doc, controlla la forma (le parti giuste per sezione), il
  sidechain presente sui bersagli e assente altrove, e la rampa del cutoff.

### 3. L'istruzione — `docs/istruzioni/arrangiamento-house.md`

Nel dance build/drop e filtro/sidechain **sono lo stesso gesto** (il drop = tutto
dentro + filtro aperto + sidechain acceso), quindi **un** documento solo, non due.
Segue la forma collaudata (vocabolario → vincoli → procedura locale → esempio
lavorato), coi gradi `[LIB]`/`[DEC]`/`[OSS]`. Copre:

- l'**arco** dance (intro/build/drop/breakdown/drop) e cosa entra/esce quando;
- il **filtro che apre** (la rampa, `MU.apri_filtro`);
- il **sidechain interno** (il meccanismo di sopra, con la distinzione dal
  compressore in chiaro — è la trappola);
- i **vincoli**: la cassa si buca solo nel breakdown, il drop non aggiunge note
  ma *toglie e rimette parti* + apre il filtro, il pompaggio è mix non nota;
- link reciproci con `batteria-house.md` e `basso-house.md`.

## La scheda e l'indice

- `docs/repertori/house.md`: casella **9** da «Vuota» a piena (l'arco, con
  `MU.forma` + arranger), casella **10** da «Parziale» a piena (filtro + sidechain,
  `[DEC]`+`[OSS]`), aggiornando le note «cosa manca» e la riga «verdetto»;
- `docs/MUSICA.md`: la riga d'indice di house/techno aggiornata (9 e 10 non più
  vuote).

## Cosa resta fuori (YAGNI)

- **techno acid** (LFO→cutoff rotolante, la nota sola): il filtro qui è la rampa
  di build, non l'acid continuo. Si nomina nell'istruzione come vicino, non si
  implementa;
- **il lead/topline e il vocal chop** (casella 8): restano vuoti, sono `audio.py`;
- **un primitivo d'arrangiamento nuovo**: si riusa `MU.forma`, non se ne aggiunge;
- **il tuning fine del mix** (reverb, coda del kick): è ascolto, non spec.

## Rischi e come si chiudono

| rischio | mossa |
|---|---|
| valore del ducking/send indovinato male | coppia controllata sul Deluge; finché non pinnato, `[da verificare]` nel racconto |
| il sidechain non si vede/non pompa sul device | verificare **guardando/ascoltando** sul Deluge, non dal file (regola 0) |
| la rampa del cutoff «scende invece di salire» per il wrap-around | è il caso noto in `automation.ramp` — usare la funzione, non l'aritmetica a mano |
| fine-riga corrotti nel commit | `write_bytes`/`newline=''`; `git diff --stat` == `--ignore-cr-at-eol` prima di committare (memoria `fine-riga-nel-repo`) |

## Fatto = 

- le due primitive con i loro test verdi;
- `house2_scritto.py` che costruisce l'arco, `verifica()` vuota, `test_house2_scritto` verde;
- l'istruzione, la scheda e l'indice aggiornati e coerenti (contratto delle schede);
- il file caricato sul Deluge (se collegato) per l'ascolto dell'utente — il verdetto chiude il giro.
