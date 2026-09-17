# House / techno

**Parziale.** Compilata il 17 settembre 2026, **secondo genere del perimetro 3**.
Copre la **four-on-the-floor** (house e techno, sullo stesso asse): la sezione
ritmica è scritta e ascoltata (*«funziona»*). ⚠️ **Niente corpus** — sono generi
**programmati** — quindi è `[LIB]`+`[DEC]`, la convenzione di genere. ⚠️ E manca
proprio ciò che *fa* il genere: l'**arrangiamento** (build/drop, casella 9) e il
**suono/filtro in movimento** (casella 10).

Il dettaglio operativo sta in [batteria-house.md](../istruzioni/batteria-house.md)
e [basso-house.md](../istruzioni/basso-house.md), l'esempio in
`tools/house_scritto.py`. Questa scheda è la vista per casella.

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

`[LIB]`+`[DEC]` **house ~120-126**, **techno ~128-140**. L'esempio è a **124**.

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

**Parziale.** `[DEC]` Le velocity decise: cassa **112** (forte, uniforme), clap
**100**, open hat **80**, closed hat **46**. ⚠️ Ma la vera dinamica di house/techno
è il **sidechain** — il pompaggio di tutto sotto la cassa — che è una scelta di
**mix**, non una nota, e qui **manca**. Per questo la casella è parziale.

## 7. Armonia

`[LIB]` Nella **house** l'armonia è lo **stab** jazzy: un accordo corto e ripetuto
(min7/9, maj9, sus) in levare, preso dai **moduli d'armonia** del progetto, come per
l'hip hop e i sottogeneri jazz — *il sapore è scelta compositiva*
([jazz.md](jazz.md), casella 1). Nella **techno** spesso l'armonia è **minima o
assente** (un drone, un accordo solo): comanda il timbro. L'esempio:
`Am9 | Dm9 | Fmaj9 | Em9`, rootless, sul piano.

## 8. Melodia e ornamentazione

**Vuota.** Il *topline*/lead (il riff di synth, l'hook, il vocal chop) non è stato
toccato — lo stab è armonia, non melodia. Cosa manca: il lead in levare e il
vocal-chop campionato (materiale di `audio.py`).

## 9. Forma e densità

**Vuota**, ed è **l'essenza mancante del genere.** House e techno *sono* forma: il
**build/drop** su 16-32-64 battute (entrano ed escono le parti, il filtro si apre,
il breakdown toglie la cassa e la riporta). Una battuta non dice niente di un pezzo
techno. Cosa manca: la mappa di forma dance — vive in `arranger.py` e
nell'automazione, ed è il prossimo lavoro vero su questo genere.

## 10. Sul Deluge

**Parziale.** `[DEC]` L'esempio `tools/house_scritto.py`: kit **808 From Mars** (il
suono elettronico giusto, non un ripiego), `Square Saw Bass` scurito per il sub,
`Pianism I` per lo stab, `set_swing(55)`. ⚠️ **Cosa manca:** il **filtro in
movimento** (LFO→cutoff via `sound.set_patch_cable`, o l'automazione del cutoff) e
il **sidechain** — metà del carattere del genere. La libreria c'è; l'esempio non li
usa ancora.

## 11. Trappole del generatore

- **la cassa non si buca**: ogni movimento, è il motore (salvo il break);
- **l'open hat sta sul levare, non sul movimento**: sul movimento copre la cassa e
  ammazza la spinta;
- **il basso sta fuori dalla cassa**: sui levare — sul movimento raddoppia la cassa
  e il groove smette di pompare (l'opposto dell'hip hop);
- **il suono è elettronico**: un kit acustico non fa house/techno (serve 808/909/CR-78);
- **il movimento è nel filtro e nell'arrangiamento**, non nei colpi: aggiungere note
  non fa progredire un pezzo dance — lo fanno il build/drop e lo sweep.

### Fonti

- ⚠️ **Nessun corpus**: techno/house sono programmati. Il `dance` di Groove MIDI è
  **7 esecuzioni di 2 batteristi** (`[OSS]`, non `[MIS]` — la lezione del reggae), e
  non è four-on-the-floor;
- istruzioni [batteria-house.md](../istruzioni/batteria-house.md),
  [basso-house.md](../istruzioni/basso-house.md); esempio `tools/house_scritto.py`;
- **verdetto d'ascolto (17 settembre 2026): «funziona».**
