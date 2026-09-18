# House / techno

**Quasi completa.** Compilata il 17 settembre 2026, **secondo genere del
perimetro 3**. Copre la **four-on-the-floor** (house e techno, sullo stesso asse):
la sezione ritmica è scritta e ascoltata (*«funziona»*), e il **17 settembre**
si è aggiunta **l'essenza del genere** — l'**arrangiamento** (build/drop, casella
9) e il **suono in movimento** (filtro + **sidechain interno**, casella 10):
scritti, con `verifica()` pulita, e **ascoltati sul dispositivo** (*«va bene»*, 17
settembre 2026). Il **18 settembre** si è aggiunto il **techno acid** — il TB-303
(casella 8, il lead; casella 10, il suono): la linea che rotola e il filtro
risonante che evolve, in attesa dell'ascolto. ⚠️ **Niente corpus** — sono generi
**programmati** — quindi è `[LIB]`+`[DEC]`, la convenzione di genere; la sola
struttura XML del sidechain e i patch cable del 303 sono `[OSS]` (file veri/corpus).

Il dettaglio operativo sta in [batteria-house.md](../istruzioni/batteria-house.md),
[basso-house.md](../istruzioni/basso-house.md),
[arrangiamento-house.md](../istruzioni/arrangiamento-house.md) e
[acid.md](../istruzioni/acid.md); gli esempi in `tools/house_scritto.py` (il
groove), `tools/house2_scritto.py` (l'arco) e `tools/acid_scritto.py` (l'acid).
Questa scheda è la vista per casella.

Il grado di prova: `[LIB]` convenzione documentata · `[DEC]` decisione presa qui.

---

## 1. Cos'è, e cosa non è

**Parziale.** Copre la **four-on-the-floor**, un angolo di un mondo vasto:
- **house** (~124, leggermente swingata, calda, stab jazzy);
- **techno** (~130, dritta, scura, minimale, il movimento è il filtro).

Il tratto comune: **cassa su ogni movimento** (il motore), e tutto il resto vive
**nei buchi fra le casse** (i levare).

**Cosa NON è:** l'hip hop (cassa 1-3, non ogni movimento), il funk (sincope). Qui
la cassa è **il metronomo**, e la musica sta in ciò che le gira intorno.

## 2. Metro e griglia

4/4, **16 passi** (sedicesimi). Rigida: la four-on-the-floor è quantizzata.

## 3. Tempo

`[LIB]`+`[DEC]` **house ~120-126**, **techno ~128-140** (l'**acid techno** ~130-140).
Gli esempi: la house a **124**, l'acid a **132**.

## 4. Feel

`[LIB]`+`[DEC]` La **house** ha un lieve **shuffle** (`set_swing(55)`, il lilt che
spinge crome e stab). La **techno** è **dritta** (`set_swing(50)`). ⚠️ Lo swing
muove le crome, non i movimenti: la cassa resta ferma su ogni battere comunque.

## 5. Ruoli e spartizione

La spartizione: **cassa = il motore** (ogni movimento), **basso = i levare**
(fuori dalla cassa), **stab = l'armonia** (in levare), **hi-hat/clap = l'alto** (open
hat sul levare, clap sul 2-4).

- **batteria** `[LIB]`+`[DEC]`: four-on-the-floor, open hat sui levare (la firma),
  clap sul 2 e 4, closed hat sui sedicesimi. Vedi
  [batteria-house.md](../istruzioni/batteria-house.md);
- **basso** `[LIB]`+`[DEC]`: **fuori dalla cassa**, sui levare, a **ottave** che
  rimbalzano — l'opposto dell'aggancio dell'hip hop. Vedi
  [basso-house.md](../istruzioni/basso-house.md).

## 6. Dinamica

`[DEC]` Le velocity decise: cassa **112** (forte, uniforme), clap **100**, open hat
**80**, closed hat **46**. ⚠️ Ma la vera dinamica di house/techno è il **sidechain**
— il pompaggio di tutto sotto la cassa — che è una scelta di **mix**, non una nota:
è coperto nella **casella 10** (`MU.sidechain`, il sidechain interno del Deluge).

## 7. Armonia

`[LIB]` Nella **house** l'armonia è lo **stab** jazzy: un accordo corto e ripetuto
(min7/9, maj9, sus) in levare, preso dai **moduli d'armonia** del progetto, come per
l'hip hop e i sottogeneri jazz — *il sapore è scelta compositiva*
([jazz.md](jazz.md), casella 1). Nella **techno** spesso l'armonia è **minima o
assente** (un drone, un accordo solo): comanda il timbro. L'esempio:
`Am9 | Dm9 | Fmaj9 | Em9`, rootless, sul piano.

## 8. Melodia e ornamentazione

`[LIB]`+`[DEC]` Il lead del techno è la **linea acid** (il riff del TB-303): **rada
in altezza** (una-due note che rotolano sui sedicesimi, con ottava/♭7/quinta),
**fitta in ritmo**, con **accenti** (velocity) e **slide** (legato in mono). Non è
melodia nel senso della frase: è ritmo + filtro. Il carattere lo dà lo *squelch*
del 303, non le altezze — vedi [acid.md](../istruzioni/acid.md) e la casella 10.
Esempio: `tools/acid_scritto.py`.

⚠️ **Resta fuori** il **vocal chop** campionato (l'altra faccia del lead dance):
è materiale di `audio.py`, non note.

## 9. Forma e densità

`[LIB]`+`[DEC]` **L'essenza del genere.** House e techno *sono* forma: il
**build/drop** su 16-32-64 battute — entrano ed escono le parti, il filtro apre, il
breakdown toglie la cassa e il drop la riporta. Una battuta non dice niente di un
pezzo dance.

L'arco si stende con **`MU.forma`** (la mappa delle sezioni nel tempo) +
`arranger`: una clip per stato (intro scarna, piena, stab che apre, stab
filtrato), riusate fra sezioni uguali; una clip corta piazzata su una sezione
lunga **si ripete in loop**. L'arco minimo, nell'esempio `tools/house2_scritto.py`
(32 battute):

| sezione | batt. | cosa suona |
|---|---|---|
| intro | 8 | cassa + closed hat |
| build | 4 | entrano basso e stab; il filtro apre |
| drop | 8 | tutto + il sidechain pompa |
| breakdown | 4 | via la cassa; stab filtrato + basso |
| drop | 8 | rientro pieno |

⚠️ Il **breakdown** è l'unico posto dove la cassa **si buca**: è l'eccezione che
crea il vuoto da cui il drop rientra. Dettaglio in
[arrangiamento-house.md](../istruzioni/arrangiamento-house.md).

## 10. Sul Deluge

`[DEC]` I suoni: kit **808 From Mars** (il suono elettronico giusto, non un
ripiego), `Square Saw Bass` scurito per il sub, `Pianism I` per lo stab,
`set_swing(55)`.

**Il suono in movimento** (l'esempio `tools/house2_scritto.py` lo usa):

- **filtro che apre** — `MU.apri_filtro(doc, clip, da, a, da_tick, a_tick)` stende
  una rampa del cutoff in unità display (0-50) sulla clip; vive nella clip, quindi
  vale solo dove quella clip suona (il build apre, il drop è spalancato). Per lo
  stab scuro del breakdown, un `lpfFrequency` fisso basso;
- **sidechain interno** — `MU.sidechain(doc, bersaglio, quanto, sync, manda_da)`.
  ⚠️ È il **sidechain** del Deluge, **non** il compressore (`<audioCompressor>`):
  sono due elementi XML distinti. Tre pezzi: `sideChainSend` pieno sul kick (il
  trigger), `sidechainCompressorVolume` nei `<params>` di ogni clip del bersaglio
  (il ducking — è la clip che suona), `<sidechain>` sync sullo strumento. Si
  imposta **una volta**: pompa da sé dove batte la cassa (drop sì, breakdown no);
- **il suono acid (TB-303)** — `MU.acid(doc, bersaglio, onda='saw'|'square', …)`:
  mono + osc + risonanza alta + `envelope2→lpfFrequency` (lo squelch) +
  `velocity→lpfFrequency` (l'accento) + portamento (slide). I due patch cable sono
  `[OSS]` (corpus: 157× e 129×); i valori sono `[da verificare]` all'orecchio. Vedi
  [acid.md](../istruzioni/acid.md), esempio `tools/acid_scritto.py`;
- **il filtro che evolve** — `MU.automatizza(doc, clip, param, …)` rampa **qualunque**
  parametro in unità display (0-50): cutoff **e** risonanza, l'anima dell'acid
  (`apri_filtro` ne è il wrapper su `lpfFrequency`). ⚠️ Solo `lpfFrequency` è
  verificato sul device; la risonanza in automazione è `[da verificare]`.

⚠️ La **struttura** del sidechain è `[OSS]` (verificata sui file veri, schema
c1.3.0: valori `0xF2000000`/`0xDE000000`/`0xFC000000`); la **magnitudine** del duck
(`sidechainCompressorVolume = 0xDE000000`) è `[OSS]`+`[ascolto]` — non ha scala di
display (`sidechainCompressorVolume` non è in `param_ids`), quindi si è tarata
all'orecchio: verdetto *«va bene»* (17 settembre 2026).

## 11. Trappole del generatore

- **la cassa non si buca**: ogni movimento, è il motore (salvo il break);
- **l'open hat sta sul levare, non sul movimento**: sul movimento copre la cassa e
  ammazza la spinta;
- **il basso sta fuori dalla cassa**: sui levare — sul movimento raddoppia la cassa
  e il groove smette di pompare (l'opposto dell'hip hop);
- **il suono è elettronico**: un kit acustico non fa house/techno (serve 808/909/CR-78);
- **il movimento è nel filtro e nell'arrangiamento**, non nei colpi: aggiungere note
  non fa progredire un pezzo dance — lo fanno il build/drop e lo sweep;
- **il drop non aggiunge, rimette**: si tolgono e si rimettono parti + si apre il
  filtro, non si accumulano colpi;
- **il sidechain col SIDECHAIN, non col compressore**: sono due elementi XML
  distinti (`<sidechain>` vs `<audioCompressor>`); il compressore non pompa;
- **l'acid è il filtro, non le note**: risonanza alta o non è acid; la linea è
  rada in altezza; l'accento è la velocity, lo slide è il legato in mono.

### Fonti

- ⚠️ **Nessun corpus**: techno/house sono programmati. Il `dance` di Groove MIDI è
  **7 esecuzioni di 2 batteristi** (`[OSS]`, non `[MIS]` — la lezione del reggae), e
  non è four-on-the-floor. Sono invece `[OSS]` (file veri/corpus) la struttura XML
  del sidechain e i patch cable del 303 (`envelope2→cutoff` 157×,
  `velocity→cutoff` 129×);
- istruzioni [batteria-house.md](../istruzioni/batteria-house.md),
  [basso-house.md](../istruzioni/basso-house.md),
  [arrangiamento-house.md](../istruzioni/arrangiamento-house.md),
  [acid.md](../istruzioni/acid.md); esempi `tools/house_scritto.py` (groove),
  `tools/house2_scritto.py` (arco), `tools/acid_scritto.py` (acid);
- **verdetto d'ascolto:** il groove (17 settembre 2026) *«funziona»*; l'arco +
  filtro + sidechain (17 settembre 2026) *«va bene»*; il **techno acid** (18
  settembre 2026) **in attesa d'ascolto**.
