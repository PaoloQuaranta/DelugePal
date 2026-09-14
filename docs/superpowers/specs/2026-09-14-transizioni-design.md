# Le transizioni — progetto

**Data:** 14 settembre 2026
**Cos'è:** la **terza faccia della struttura** (priorità 2, forma), dopo la
[mappa](2026-09-14-struttura-design.md) e l'[arco](2026-09-14-arco-dinamico-design.md).
Le transizioni sono i **giunti** fra le sezioni: dove una finisce e l'altra
comincia, e come si **cuciono**.

⚠️ **Scelta dell'utente il 14 settembre 2026** fra tre primi pezzi: **giunti
armonico-melodici + la clip bianca** (scelto), il fill di batteria, i tre modi a
confronto. Il primo perché dà a `arranger.place_unique` — la clip bianca, «finora
solo nominata» — il suo primo uso vero, e lavora sull'AABA che c'è già senza
aggiungere una batteria.

## Il metodo — `[CALC]` + un ascolto

Il `[CALC]` è il meccanismo della clip bianca (`MU.variazione`); l'ascolto è se il
giunto **cuce** — se il ponte arriva preparato e il ritorno chiude.

## Il principio (`[LIB]` narrative-and-transitions.md)

La transizione è dove il contorno dell'energia si sente di più. **Tre modi:**
**brusco** (di colpo, massimo contrasto), **rampa/build** (l'energia sale
nell'ultima battuta, la sezione nuova è il rilascio), **morbido** (sovrapposizione
o perno condiviso). E **la cadenza è la punteggiatura del giunto:** mezza o
ingannevole ai giunti interni («continua»), la piena tenuta per la fine.

## Il vocabolario del giunto (armonico-melodico)

- **turnaround** (già in `armonia-funzionale.md`): un giro I–vi–ii–V in coda che
  riporta. ⚠️ È anche l'**accelerazione del ritmo armonico** verso la cadenza — la
  stessa mossa di `ritmo-armonico.md`, vista dal giunto;
- **pickup**: una salita melodica nell'ultima battuta che consegna la sezione nuova
  (la rampa in miniatura);
- **break/stacco**: il mezzo movimento di silenzio prima dell'arrivo;
- **perno**: nota/accordo tenuto comune a due sezioni (la transizione morbida).

## Il meccanismo — `MU.variazione` (codice nuovo, thin su `place_unique`)

Una transizione tocca **un** giunto e non deve toccare gli altri. Il modo del
dispositivo è la clip **bianca** (arranger-only). `variazione(doc, sorgente, pos,
*, length=None)`: fa una copia bianca di `sorgente` (niente `section`), la piazza a
`pos`, la ritorna — lo strumento lo trova da sé. Modificarla non tocca l'originale
né le altre ripetizioni. Sotto c'è `arranger.place_unique`; sopra, l'AI riempie la
copia con `MU.togli`/`MU.scrivi`. ⚠️ Si varia **solo la voce che cambia** (se il
pickup è nella melodia, la clip bianca è quella della melodia).

`[CALC]` — `test_variazione`: la copia è bianca (arranger-only), è piazzata al
giunto, svuotarla non tocca la sorgente, una clip senza strumento è rifiutata.
`test_transizioni_scritto`: il pickup sale e arriva in alto (do5), il turnaround
stringe il ritmo armonico (2 accordi nella battuta 3) e risolve su Cmaj7, le
variazioni sono bianche, il pezzo è valido.

## L'esempio lavorato (l'ascolto)

`STRUTTURA03`: lo stesso AABA con due giunti — **A2→B** un **pickup** (la melodia
sale, consegna il ponte: rampa), **il ritorno (A3)** un **turnaround** che stringe
il ritmo armonico e risolve (morbido, la cadenza che chiude). Solo la melodia di A2
e l'ultimo A sono clip bianche; il resto è piano. In
`tools/transizioni_scritto.py`, si suona dall'arranger. Pronto e caricato; l'utente
ascolta se i giunti cuciono → `[OSS]`.

## Struttura / rimandi

- `docs/istruzioni/transizioni.md` (nuovo); `MU.variazione` in `musica.py` (thin su
  `arranger.place_unique`); `test_variazione` + `test_transizioni_scritto`;
  `tools/transizioni_scritto.py`;
- rimandi: `struttura.md` (la mappa), `arco-dinamico.md` (l'intensità dentro le
  sezioni), `armonia-funzionale.md` (il turnaround), `ritmo-armonico.md` (il
  turnaround = accelerazione alla cadenza).

## Cosa resta fuori

- il **fill di batteria** (`[MIS]` casella 9, 51 fill jazz): vuole una traccia di
  batteria nel pezzo;
- i **tre modi a confronto** sullo stesso giunto;
- la transizione **morbida** vera (sovrapposizione/cross-fade): qui il perno è solo
  un'idea;
- una primitiva che **alza l'ultimo giro** in automatico (final-chorus elevation).

## Cosa NON rifare

- **non toccare la clip di sezione per variare un giunto**: è per questo che la
  copia è bianca — modificando l'originale cambiano tutte le ripetizioni;
- **non copiare tutta la sezione per una voce sola**: la clip bianca è solo per la
  voce che cambia;
- **non chiudere senza l'ascolto**: metodo `[CALC]` + un ascolto.
