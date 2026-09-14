# La struttura (mappa di forma) — progetto

**Data:** 14 settembre 2026
**Cos'è:** l'ultima faccia della **priorità 2 (forma)**, dopo voicing, comping e
contrappunto. La **struttura lunga**: come il materiale si dispone nel tempo — le
sezioni, il loro ordine, cosa torna e cosa contrasta. È ciò che rende possibile
«un pezzo intero» invece di una parte sola.

⚠️ **La struttura ha tre facce; questa è la MAPPA (lo scheletro).** Scelta
dell'utente il 14 settembre 2026, fra: **(1) mappa di forma** — dove cadono le
sezioni; **(2) arco dinamico** — come densità/intensità salgono e ricadono lungo
la forma; **(3) transizioni** — turnaround, fill, stacchi. Si parte dalla (1)
perché è il meccanismo che rende possibile il pezzo intero, e l'arranger è già lì.

## Il metodo — `[CALC]` + un ascolto

Come le altre facce della forma. Il `[CALC]` è dove cadono le sezioni (i conti in
tick); l'ascolto è se la **forma si sente** — se l'A torna riconoscibile e il ponte
contrasta. L'agente arriva al «pronto da caricare»; l'ascolto è dell'utente.

## Il principio (`[LIB]` + `[MIS]`)

`[LIB]` music-composition, `references/form/popular-song-forms.md`: le forme sono
**tipi di sezione combinati in un ordine**. ⚠️ La regola che pesa più delle mappe:
**ripetizione contro sviluppo** — una forma che ripete identica è statica,
*«l'ultima ripetizione deve pesare di più»* (final chorus elevation). Lo scheletro
è la mappa; lo sviluppo è la faccia dopo.

`[MIS]` casella 9 di `docs/repertori/jazz.md` (da `wjazzd.db`, 349 assoli swing con
forma scomponibile): l'**AABA** (`A8A8B8A8`, 103 assoli), il **blues** (`A12`, 81),
i **rhythm changes** (template *I Got Rhythm*, 19). Il vocabolario delle forme jazz
era **già misurato**; mancava l'istruzione e la primitiva che lo stende.

## Il meccanismo — `MU.forma` (codice nuovo)

Un thin layer sopra `arranger.place`. `forma(doc, mappa, sezioni, *, battute=8,
battute_per=None)`:

- `mappa`: la sequenza — `'A A B A'` o `['A','A','B','A']`;
- `sezioni`: `{nome: [clip, ...]}` — quali clip suonano in ogni sezione (una per
  strumento). Ogni clip sa già il suo strumento (`song.instrument_of`);
- calcola dove cade ogni sezione in tick e piazza le clip; ritorna il piano
  (`list[Sezione]`) e chiama `arranger.fit_view`.

⚠️ **NON compone e non crea clip:** il materiale lo scrive l'AI prima. È la
divisione di sempre — l'AI decide la forma, il codice la stende. `racconta_forma`
lo dice a parole (regola 4, solo ASCII).

⚠️ **Ripetizione = stessa clip a più posizioni** (il modo del dispositivo: cambiando
la clip cambiano tutte le ripetizioni). **Variazione = `arranger.place_unique`** (la
clip bianca), che è la faccia *sviluppo*, non questa.

`[CALC]` — `test_forma`: il piano cade ai tick giusti con `battute_per`; l'AABA
d'esempio è lungo 16 battute e ogni strumento ha 4 sezioni ai tick di `A A B A`;
una sezione ignota nella mappa è rifiutata **prima** di piazzare nulla; una mappa
vuota è rifiutata; il file d'esempio passa `verifica`.

## L'esempio lavorato (l'ascolto)

Un AABA vero (`STRUTTURA01`): Rhodes (accordi) + tromba (melodia), **A** = la casa
(`Cmaj7 Am7 Dm7 G7`, tema medio), **B** = il ponte (`Fmaj7 Bb7 Cmaj7 G7`, sul IV,
tema acuto, chiude sul V). Mappa `A A B A`, sezioni da 4 battute, 16 in tutto. In
`tools/forma_scritto.py`. ⚠️ Si suona **dall'arranger** (`open_in_arranger`): la
timeline è la forma; le clip di sessione restano ferme (l'`avvertenze` sul
`isPlaying` è qui attesa, non un difetto). Pronto da caricare; l'utente ascolta se
la forma si sente → `[OSS]`.

## Struttura / rimandi

- `docs/istruzioni/struttura.md` (nuovo); `MU.forma` + `MU.racconta_forma` +
  `Sezione` in `musica.py` (thin layer su `arranger.place`); `test_forma`;
  `tools/forma_scritto.py`;
- rimandi: `voicing.md`/`comping.md`/`contrappunto.md` (le facce dentro la
  battuta), casella 9 di `jazz.md` (il vocabolario misurato delle forme).

## Cosa resta fuori (le altre due facce della struttura, su domanda)

- l'**arco dinamico**: densità/intensità che salgono al ponte e ricadono — **già
  misurato** (`[MIS]` casella 9), da spendere sul generatore;
- le **transizioni**: turnaround, fill, stacchi, pickup fra sezioni;
- le **variazioni** con `place_unique` (l'ultimo giro diverso);
- la forma **non uniforme/annidata** (code che troncano, sovrapposizioni):
  `battute_per` copre le lunghezze diverse, non le sovrapposizioni.

## Cosa NON rifare

- **non far comporre la forma al codice**: `MU.forma` stende una mappa decisa
  dall'AI, non ne inventa una;
- **non usare `place` dove serve `place_unique`**: la ripetizione identica riusa la
  clip, la variazione vuole la clip bianca;
- **non chiudere senza l'ascolto**: metodo `[CALC]` + un ascolto;
- **non aspettarsi la session view**: è una forma d'arranger — `open_in_arranger`,
  poi play.
