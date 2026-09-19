# DnB / Jungle

**Parziale.** Compilata il 19 settembre 2026, **primo genere della riga aggregata
«elettronica · IDM · DnB · jungle»**. DnB/jungle **amen-led**: un break di batteria
(l'amen) affettato e **ri-sequenziato** a ~170 BPM, sotto un **sub half-time** e
un'**armonia minore** scura. Non serve una capacità nuova: lo **slicing**
(`kit.affetta`) è lo stesso gesto del **vocal chop** — cambia il materiale (un break)
e il fine del chop (ricostruire e editare un groove, non rompere una parola).

Il dettaglio operativo sta in [dnb-jungle.md](../istruzioni/dnb-jungle.md), che rimanda
a [vocal-chop.md](../istruzioni/vocal-chop.md) per il meccanismo delle fette; l'esempio
in `tools/dnb_scritto.py`. Questa scheda è la vista per casella.

Il grado di prova: `[LIB]` convenzione · `[OSS]` osservato · `[CALC]` calcolato ·
`[DEC]` deciso qui.

---

## 1. Cos'è, e cosa non è

**Parziale.** `[LIB]`+`[DEC]` Copre la **jungle / breakbeat-DnB amen-led**: il break
è il protagonista, scuro, veloce (~170) ma sentito **in half-time**. La corsa la fa la
batteria; sotto, tutto va lento.

**Cosa NON è:** la **house/techno** (non four-on-the-floor: qui la batteria è un break
affettato, non una cassa su ogni movimento); il **trip-hop / hip-hop** (non lento e
laid-back: qui è veloce, e il feel non è programmato); una **batteria programmata** (il
break è una **registrazione** di un batterista vero — la sua dinamica e il suo timing
sono nell'audio). Restano fuori i **sottogeneri** (liquid, ragga, neuro) e la **Reese
bass**: qui c'è l'ossatura amen-led.

## 2. Metro e griglia

`[DEC]` 4/4, **16 passi** (1/16). Il break si affetta sulla griglia di 1/16 (**64 fette
su 4 battute**). Percepito in **half-time**: il colpo «forte» pare cadere ogni due
movimenti, ed è lì che vanno sub e armonia.

## 3. Tempo

`[LIB]`+`[DEC]` **~160-175 BPM**, il cuore del DnB. L'esempio è a **171** — il tempo
nativo dell'amen stretchato usato, e non è un caso: vedi casella 10, perché il tempo
della song deve combaciare col tempo nativo del break.

## 4. Feel

`[DEC]` **DRITTO** (`S.set_swing(doc, 50)`), e **non è una dimenticanza.** Il break è
una registrazione: il suo micro-timing umano è già **nell'audio** delle fette. Uno
swing di song lo sposterebbe una **seconda** volta (e sposterebbe anche sub e pad). ⚠️
È il rovescio dello swing jazz, dove il feel sta nelle **posizioni scritte**: qui sta
nel **disco**. Non trasferire per riflesso l'idioma dello swing (memoria
`riflesso-idioma-fuori-contesto`). È la stessa domanda della casella 4 di jazz e
reggae — «dove cade il levare» — con una risposta di tipo nuovo: *nell'audio, non nella
griglia*.

## 5. Ruoli e spartizione

La spartizione: **break = il motore** (la batteria, tutta la griglia ritmica veloce),
**sub = il peso half-time** (rado, gravissimo, sul 1), **pad = l'armonia e il colore**
(tenuto, lento). Il break occupa lo spazio ritmico per intero; sub e armonia lo
lasciano libero andando lenti — è il **contrasto** a fare il genere.

- **break** `[OSS]`+`[DEC]`: l'amen in 64 fette, ri-sequenziato per **beat** (4 fette
  contigue = un movimento coerente), casse gravi sui movimenti forti, rullate a
  chiudere le frasi (casella 6, 10);
- **sub** `[LIB]`+`[DEC]`: grave e rado, fondamentale tenuta sul 1 + spinta sul 4,
  sulle fondamentali del vamp;
- **pad**: il vamp minore, rootless, tenuto (casella 7).

## 6. Dinamica

`[DEC]`+`[OSS]` **La dinamica del break è NELL'AUDIO, non si programma.** Le fette si
innescano a velocity ~uniforme (~115): sono gli accenti e i fantasmi del batterista
vero, registrati, a portare la dinamica — è metà del perché l'amen suona vivo. Un
break «appiattito» a velocity costante e note MIDI perderebbe proprio questo. Quali
fette sono cassa/rullante lo dice un'**analisi di energia** stdlib (RMS + banda grave):
nell'amen le casse gravi sono le fette **0, 24, 56** `[OSS]`. Sub e pad: morbidi.

## 7. Armonia

`[CALC]` **Scura e cinematica**, ritmo armonico **lento** (un accordo per battuta o
meno) — il half-time vale anche per l'armonia. Minore, ed è **scelta compositiva**:
accordi estesi (min9), **prestito modale** (il **♭VImaj7** caldo), **dominante
alterata** (V7♭9 scura) — lo stesso colore approvato nel trip-hop, arrangiato per il
DnB. Rootless, registro medio-grave, tenuto sul Rhodes/pad. Si scrive con `MU.armonia`
(che conduce le parti); il `[CALC]` (`racconta_armonia`) dà le note e scioglie le
ambiguità. L'esempio: `Cm9 | A♭maj7 | Cm9 | G7♭9` (i–♭VI–i–V7♭9), verificato col calcolo
(Cm9 rootless E♭ G B♭ D, A♭maj7 G B♭ C E♭, G7♭9 A♭ B D F).

## 8. Melodia e ornamentazione

**Vuota.** La superficie melodica del DnB — un **hook** (vocal chop, stab, lead
sintetico) o una **linea** — non è ancora fatta qui. Nell'esempio la «linea» è il
**chop del break** (materiale ritmico) e il colore lo porta l'armonia (casella 7). Il
**vocal chop** è disponibile come tecnica (`kit.affetta`,
[vocal-chop.md](../istruzioni/vocal-chop.md)) e si innesterebbe qui allo stesso modo.
Per riempirla servirebbe un pezzo che chieda un hook o un lead.

## 9. Forma e densità

**Parziale.** `[DEC]` L'arco delle **entrate**: il break si enuncia da solo, il **drop**
aggiunge peso (sub) e colore (armonia), il **breakdown** toglie il break (la tensione),
poi si ri-droppa. L'esempio (`MU.forma`, 32 battute): intro 8 (break solo) → drop 8
(tutto) → breakdown 8 (sub + pad, break fuori) → drop 8. La forma lunga (più temi, la
seconda parte, il finale) è accennata, non sviluppata.

## 10. Sul Deluge

`[DEC]`+`[OSS]` Lo **slicing**: `kit.affetta(doc, kit, path, frames, n=64)` — un kit di
64 fette dell'amen, ognuna una `<zone>` con **REPEAT MODE ONCE** (la zona delimita la
fetta, come lo Slicer nativo; `[OSS]`, vedi [vocal-chop.md](../istruzioni/vocal-chop.md)).

⚠️ **Il tempo della song deve combaciare col tempo NATIVO del break.** Con ONCE la
fetta suona alla sua velocità nativa: a song più veloce del nativo le fette si
**sovrappongono**, più lenta si **aprono buchi**. `original AMEN.wav` è già stretchato a
~171 → a song 171 una fetta da 1/16 dura un 1/16 e il break si ricostruisce esatto. Un
amen grezzo (~138) va **stretchato prima** (il Deluge lo fa; `kit.affetta` no).

⚠️ **Un drum a parte per il loop INTERO in one-shot** (per sentire l'amen originale):
`K.add_drum` di una copia di una fetta + `set_sample(..., start=0, end=FRAMES)` + osc1
`loopMode=1` (ONCE). Non sequenziato — si innesca a mano sul dispositivo. È l'ultima
riga del kit, `amen intero`.

I suoni: **kit 808 From Mars** come telaio del drum affettato; **Square Saw Bass**
scurito (`applica_verbo 'piu scuro'`) per il sub; **Tal Rhodes** + `reverbAmount` per
il pad. Feel dritto: `S.set_swing(doc, 50)`.

## 11. Trappole del generatore

- **il break al tempo sbagliato**: se il nativo del break ≠ tempo della song, con ONCE
  le fette impastano (troppo veloce) o bucano (troppo lento) — scegli/stretcha il break
  al tempo del pezzo;
- **chop a caso**: rimescolare le **fette singole** a caso suona rotto; lavora per
  **beat** (4 fette contigue = un movimento coerente) e resta amen;
- ⚠️ **mettere lo swing**: il feel del break è **nell'audio**; uno swing di song lo
  sposta due volte. È il riflesso dallo swing jazz — spegnilo;
- **il sub fitto**: il half-time lo fa il contrasto col break veloce; un basso fitto lo
  ucciderebbe. Rado e grave;
- **appiattire la dinamica**: la dinamica dell'amen è nell'audio; non serve (e non si
  può) programmarla nota per nota — è il pregio del break;
- **niente riflesso**: il chop e l'arco si compongono PER il pezzo, all'orecchio.

### Fonti

- ⚠️ **Nessun corpus** DnB/jungle in casa (il Groove MIDI non ha l'etichetta):
  `[LIB]`+`[DEC]`. Il **break** è `[OSS]` (l'audio di un'esecuzione vera, l'amen di
  «Amen, Brother»); l'**analisi delle fette** (dov'è la cassa) è `[OSS]` stdlib
  (RMS + banda grave, `wave`); l'**armonia** è `[CALC]`;
- istruzione [dnb-jungle.md](../istruzioni/dnb-jungle.md), che rimanda a
  [vocal-chop.md](../istruzioni/vocal-chop.md); esempio `tools/dnb_scritto.py`. La v1
  (solo chop) è `DNB01`; con l'`amen intero` aggiunto al kit, caricato **via SysEx come
  DNB02**;
- **verdetto d'ascolto (19 settembre 2026): *«va bene»***. Il chop, l'arco e i livelli
  restano `[DEC]`, rifinibili sentendo.
