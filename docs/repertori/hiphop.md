# Hip hop

**Parziale.** Compilata il 17 settembre 2026, **primo genere del perimetro 3**
(i contemporanei). Copre il **boom-bap**: la sezione ritmica è scritta e
ascoltata (*«ok funziona»*) — batteria `[MIS]`, basso `[LIB]`+`[DEC]`. La
**melodia** (la topline / il flow) e la **forma** restano vuote.

⚠️ Il dettaglio operativo sta nelle istruzioni
[batteria-hiphop.md](../istruzioni/batteria-hiphop.md) e
[basso-hiphop.md](../istruzioni/basso-hiphop.md), e l'esempio lavorato in
`tools/hiphop_scritto.py`. **Questa scheda è la vista per casella**, non li
ripete.

Il grado di prova: `[MIS]` misurato su un corpus · `[LIB]` letteratura ·
`[DEC]` decisione presa qui.

---

## 1. Cos'è, e cosa non è — `[MIS]`+`[DEC]`

Il **boom-bap**: dritto, lento (~90 BPM), cassa pesante sul 1 e sul 3, backbeat
forte, hi-hat in crome, molta aria. DJ Premier, Pete Rock, l'East Coast.

**Cosa NON è**, e con cosa lo si scambia:

- **non è il trap / dirty south** (808, hi-hat a trentaduesimi e triplet, sub
  con glide) — un altro suono;
- **non è il lo-fi / swung boom-bap** (il feel «Dilla»), che è **swingato e
  laid-back** — una variante `[LIB]`+`[DEC]`, non questo (vedi casella 4);
- **non è il neo-soul / jazzy** hip hop, più vicino allo swing;
- ⚠️ come per ogni feel, «hip hop» è un **ombrello**: qui è il boom-bap, non il
  genere intero.

## 2. Metro e griglia — `[DEC]`

4/4, **16 passi** (sedicesimi), la stessa griglia del resto del progetto.
Rigida: il boom-bap è dritto.

## 3. Tempo — `[MIS]`

`[MIS]` Groove MIDI, etichetta `hiphop`: da **67 a 140 BPM**, **mediana 91**. Il
centro del boom-bap sta ~**85-95**. (I vicini: il lo-fi ~70-90, il trap spesso in
half-time.)

## 4. Feel — `[MIS]` (la casella forte)

`[MIS]` Groove MIDI `hiphop`, `beat_type='beat'`: **34 esecuzioni, 5 batteristi**.
La BUR mediana è **1,03** — cioè **dritto** (quartili 1,01-1,07), col pocket
**stretto** (scarti −1/−2 tick, quasi sulla griglia). `S.set_swing(doc, 50)`.

⚠️ **Lo swing «Dilla» / lo-fi è un ALTRO sotto-idioma, NON questo corpus:** le
crome swingate e il ritardo dietro la griglia sono di altri esecutori. Resta
`[LIB]`+`[DEC]`: `S.set_swing(doc, 56)` per il lilt, da **dichiarare**, non
spacciare per il boom-bap dritto. È la lezione del reggae, *un esecutore non è un
repertorio*, qui in un verso.

## 5. Ruoli e spartizione — `[MIS]`+`[LIB]`

La spartizione: **basso + cassa = il grave** (1 e 3), **rullante + hi-hat =
l'alto** (backbeat 2-4 e crome), **il loop campionato = l'armonia**. L'**aria**
fra il boom e il bap è la firma.

- **batteria** `[MIS]`: cassa (boom) sul 1-3 + sincopi sul levare; rullante (bap)
  sul 2-4 a v127 + ghost molli; hi-hat in crome; pedale sui movimenti. Vocabolario
  e percentuali in [batteria-hiphop.md](../istruzioni/batteria-hiphop.md);
- **basso** `[LIB]`+`[DEC]`: sub **rado** e **grave**, agganciato alla cassa sul 1
  e 3 — nessun corpus in casa lo trascrive. Dettaglio in
  [basso-hiphop.md](../istruzioni/basso-hiphop.md).

## 6. Dinamica — `[MIS]`

`[MIS]` `GR.scala()` su `hiphop`: numeri, non aggettivi.

| voce | mediana | q1 | q3 |
|---|--:|--:|--:|
| rullante (backbeat accentato) | **127** | 118 | 127 |
| rullante (ghost) | ~50 | 29 | 127 |
| cassa | 62 | 45 | 75 |
| hi-hat chiuso | 41 | 29 | 61 |

⚠️ **Il divario 127 / 40-50 È il groove.** Se i ghost e l'hi-hat salgono alla
forza del backbeat, il boom-bap sparisce.

## 7. Armonia — `[LIB]`, presa dai moduli

⚠️ L'armonia dell'hip hop **è il loop campionato**: un giro breve (2-4 battute),
spesso jazzy/soul, ripetuto in modo ipnotico — min7/9, maj7/9, sus, il 7#9. Non è
un idioma armonico **proprio**: si prende dai **moduli d'armonia** del progetto
(modale/funzionale, ritmo armonico lento), esattamente come deciso per i
sottogeneri jazz — *il sapore è una scelta compositiva, non un'estrazione*
([jazz.md](jazz.md), casella 1). L'esempio: `Am9 | Dm9 | Fmaj7 | E7#9`, rootless,
sul Rhodes polveroso.

## 8. Melodia e ornamentazione — ○

**Vuota.** La «melodia» dell'hip hop è la **topline campionata** o il **flow del
rap** — che il Deluge non canta e che il progetto non ha toccato. Cosa manca: il
rapporto col **sample-chop** (una linea tagliata da un disco), che è materiale di
`audio.py`, non note suonate.

## 9. Forma e densità — ○

**Vuota.** La forma hip hop è **basata sul loop** (4/8/16 battute) con
intro/strofa/hook e i **drop** (togliere e rimettere parti). Cosa manca: la mappa
di forma del genere — l'apparato `MU.forma`/`MU.dinamica` del jazz si può
**provare** qui, su domanda.

## 10. Sul Deluge — `[DEC]`, parziale

L'esempio `tools/hiphop_scritto.py`: kit acustico (`KIT009`) di ripiego, `Square
Saw Bass` scurito per il sub, `Tal Rhodes` per il loop polveroso, `set_swing(50)`.

⚠️ **Cosa manca: il SUONO.** Il boom-bap vive del **campione polveroso** —
batteria vinilica filtrata e saturata, il sub 808 col glide e la distorsione. È
**sound design** (`dsp-recipes`), non note: qui c'è un kit di ripiego, ed è il
buco più grande all'ascolto.

## 11. Trappole del generatore — `[DEC]`

- **il basso non è un riff funk**: 2-4 note rade, non 7; è il fondo, non una voce;
- **l'hi-hat non sono sedicesimi fitti**: crome — l'hip hop lascia aria;
- **non swingare per riflesso**: il boom-bap è dritto (BUR 1,03); lo swing è la
  variante lo-fi, da dichiarare;
- **la cassa non è quattro movimenti fissi**: 1-3 + sincopi; quattro casse è
  house/rock;
- **i ghost non alla forza del backbeat**: il divario 127/50 è il groove.

### Fonti

- **Groove MIDI Dataset** (batteria, `[MIS]`); libreria **`(aq) HipHop`** (loop
  boom-bap East Coast, corroborazione — ma programmati);
- istruzioni [batteria-hiphop.md](../istruzioni/batteria-hiphop.md),
  [basso-hiphop.md](../istruzioni/basso-hiphop.md); esempio `tools/hiphop_scritto.py`;
- **verdetto d'ascolto (17 settembre 2026): «ok funziona».**
