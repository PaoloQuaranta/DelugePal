# Il comping — progetto

**Data:** 13 settembre 2026
**Cos'è:** la seconda faccia della **priorità 2 (forma)**: il **ritmo** con cui la
mano che accompagna suona gli accordi. Poggia su `voicing` (quali note) e
`ritmo-armonico` (ogni quanto cambia l'accordo); aggiunge il **ritmo del colpo** e
lo **spazio**.

## Il metodo — `[CALC]` + un ascolto (deciso il 13 settembre 2026)

Come il voicing: il comping è ritmo, e il ritmo ha parte d'orecchio. `[LIB]` +
`[CALC]` per il vocabolario e le meccaniche; un esempio lavorato **ascoltato** per
il feel. L'agente arriva al «pronto da caricare»; l'ascolto è dell'utente.

## Il principio (`[LIB]` Levine, *The Jazz Piano Book*, cap. 21 «Comping»)

Il comping **complementa il solista**, ritmicamente e armonicamente; rinforza la
forma (accentua turnaround, ponti); è **conversazione, non tappezzeria** — *«trova
il punto medio fra audacia e ritegno»*.

## Il vocabolario

- **Le tre collocazioni del colpo** (`[LIB]` Levine fig. 21-2, 21-6): sul
  **battere**, **anticipato** (mezzo movimento *prima* — la sincope/spinta che
  definisce il comping jazz), **dietro** (mezzo dopo);
- **lo spazio** (`[LIB]` Levine): lascia spazio; **rado dove il solista è fitto,
  fitto dove respira** — call-and-response;
- **il registro** (`[LIB]` Levine): non pestare nel registro del solista;
- **il carattere**: «in due» vs sostenuto; audacia/ritegno alternati.

## Il meccanismo — `MU.comping` (codice nuovo)

Una stringa di ritmo per battuta (`x..x....`, 8 crome, `x`=colpo `.`=pausa) →
accordi piazzati sui colpi, voicizzati e **condotti**. Una `x` sull'**ultima**
cella anticipa il battere della battuta dopo.

⚠️ **Promuovo a primitiva `MU.comping(progressione, ritmi, *, voicing=, ...)`** il
meccanismo oggi sepolto in `genera_jazz._spec_comping`. È un **costruttore di spec
sopra `armonia()`**: la collocazione, il voicing e la condotta vengono da lì —
nessuna logica di piazzamento nuova. `genera_jazz` resta com'è (coppia
controllata): l'adozione della primitiva è un cleanup successivo, non forzato qui.

`[CALC]` — `test_comping`: i colpi cadono dove la stringa dice (`x..x....` → celle
0 e 3); l'anticipazione (una `x` sull'ultima croma cade a 336, prima del battere a
384); il colpo porta le note dell'accordo; ritmi ≠ battute è rifiutato.

## L'esempio lavorato (l'ascolto)

Lo stesso giro comped in **due modi** sullo stesso materiale — uno **rado e
anticipato** (con spazio), uno **fitto/sostenuto** — così la differenza è solo il
ritmo del comping. In `tools/comping_scritto.py`. Rhodes + basso; niente melodia
(lo spazio del comping si sente meglio senza un solista che lo riempie).
Caricato sul Deluge (`COMPING01`), l'utente ascolta → `[OSS]`.

## Struttura / rimandi

- `docs/istruzioni/comping.md` (nuovo); `MU.comping` in `musica.py`;
  `test_comping` + `test_comping_scritto`; `tools/comping_scritto.py`;
- rimandi: `voicing.md` (quali note), `ritmo-armonico.md` (ogni quanto cambia
  l'accordo); il comping aggiunge il ritmo del colpo.

## Cosa resta fuori (le prossime facce)

- il **contrappunto** (Piston *Counterpoint*, ora leggibile);
- la **struttura** lunga (l'`arranger`);
- il comping **latin/bossa** e il two-bar clave (Levine cap. 21 li tocca): su
  domanda, quando servirà un pezzo latin.

## Cosa NON rifare

- **non chiudere senza l'ascolto**: metodo `[CALC]` + un ascolto;
- **non forzare `genera_jazz` ad adottare `MU.comping` ora**: è una coppia
  controllata, l'adozione va fatta con la sua verifica;
- **non confondere comping e ritmo armonico**: il ritmo armonico è ogni quanto
  cambia l'accordo, il comping è ogni quanto lo si **colpisce**.
