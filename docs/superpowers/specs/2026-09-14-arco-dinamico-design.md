# L'arco dinamico — progetto

**Data:** 14 settembre 2026
**Cos'è:** la **seconda faccia della struttura** (priorità 2, forma), dopo la
[mappa](2026-09-14-struttura-design.md). La mappa dice *dove* cadono le sezioni;
l'arco dice *con quanta intensità* ciascuna suona. È la carne sullo scheletro:
come il pezzo **sale** a un culmine e **ricade**.

⚠️ **Nasce da due richieste in una** (utente, 14 settembre 2026): fare l'arco
dinamico, e **usare il brano di test anche per provare il ritmo armonico**, che
era chiuso col solo `[CALC]` e non era mai stato ascoltato. Le due cose sono la
stessa: il ritmo armonico è una **leva** dell'arco — `ritmo-armonico.md` (riga
124) già indicava «il rapporto con la forma lunga» come priorità 2.

## Il metodo — `[CALC]` + un ascolto

Il `[CALC]` è l'aritmetica (la scala delle velocity, il ritmo armonico via
`durata`); l'ascolto è se **l'arco si sente** — se il culmine arriva e il ritorno
si posa.

## Il principio (`[MIS]` casella 9 di jazz.md)

L'AABA non è un ciclo ripetuto quattro volte: **si parte radi, si cresce, si
culmina sul ponte, si ricade** (57 assoli, 36 solisti, 6777 battute). Corse per
sezione: A1 18,8% → A2 24,8% → **B 26,3%** → A3 20,9%. E il **ponte è la sola
sezione che non respira alla fine** (vuote a fine sezione: A1 15,6%, A2 10,5%, **B
6,2%**, finale 7,7%): il culmine tira dritto.

## Le tre leve (devono salire insieme)

1. **densità** — quante note (`[MIS]` mediana 5 sull'A, 6 sul ponte);
2. **ritmo armonico** — il ponte **raddoppia** (2 accordi a battuta): è dove vive,
   nella forma lunga, «accelerare verso la cadenza» di `ritmo-armonico.md`;
3. **dinamica** — la velocity, con `MU.dinamica`.
   (+ il **respiro**: i vuoti a fine sezione, `[MIS]`.)

## Il meccanismo — `MU.dinamica` (codice nuovo)

`dinamica(note, fattore, *, minimo=1)`: scala la velocity di ogni nota per
`fattore`, stretta fra `minimo` e 127, **senza mutare** l'originale (così la stessa
frase si posa a piu' livelli — l'A che torna piu' piano). È la sola leva che voleva
aritmetica; densità (quante note) e ritmo armonico (`durata`) usano le primitive
che ci sono già.

`[CALC]` — `test_dinamica`: dimezza a 0.5, stringe a 127, rispetta il minimo, non
muta l'originale, rifiuta un fattore negativo. `test_arco_scritto`: nel pezzo la
densità sale al ponte e ricade (4<8<16>4), il ponte **raddoppia** il ritmo armonico
(A=4, B=8 attacchi), la dinamica culmina sul ponte, e l'ultimo A ricade sotto il
ponte su **tutte e tre** le leve.

## L'esempio lavorato (l'ascolto)

`STRUTTURA02`: lo stesso AABA della mappa, con l'arco steso — A1 rada/piano/lenta,
A2 cresce, **B fitta/forte/veloce (2 accordi a battuta)**, A3 ricade. In
`tools/arco_scritto.py`, si suona dall'arranger. Il ponte prova, nello stesso
ascolto, l'arco **e** il ritmo armonico. Pronto e caricato; l'utente ascolta se
l'arco si sente → `[OSS]`.

## Struttura / rimandi

- `docs/istruzioni/arco-dinamico.md` (nuovo); `MU.dinamica` in `musica.py`;
  `test_dinamica` + `test_arco_scritto`; `tools/arco_scritto.py`;
- rimandi: `struttura.md` (la mappa — dove cadono le sezioni), `ritmo-armonico.md`
  (una delle tre leve), casella 9 di `jazz.md` (l'arco misurato).

## Cosa resta fuori

- l'arco su **più giri** (testa-soli-testa): l'intensità che cresce di chorus in
  chorus;
- le **transizioni** (fill, turnaround): la terza faccia della struttura;
- la **variazione automatica** dell'ultimo giro con `place_unique`;
- l'arco su generi **non-jazz** (drop dell'EDM, ritornello finale del pop): la
  forma della salita cambia col genere, su domanda.

## Cosa NON rifare

- **non trasformare l'arco misurato in un motore**: i numeri della casella 9 dicono
  *dov'è* il culmine e la forma della salita, non generano le note (regola del 30
  agosto: il corpus dà relazioni, non superfici);
- **non far salire una leva sola**: il culmine vuole densità + ritmo armonico +
  dinamica insieme;
- **non chiudere senza l'ascolto**: metodo `[CALC]` + un ascolto.
