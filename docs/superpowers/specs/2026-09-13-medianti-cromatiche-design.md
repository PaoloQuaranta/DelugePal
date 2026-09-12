# Le medianti cromatiche — progetto

**Data:** 13 settembre 2026
**Cos'è:** la seconda faccia del cromatismo, dopo il planing. Copre le **medianti
cromatiche**: accordi a distanza di terza che condividono **una sola** nota, il
colore «cinematografico».

## Perché, e la scelta

Era in «cosa manca» dell'[armonia parallela](armonia-parallela.md). Scelta in
brainstorming il 13 settembre: dopo il planing (lo stream parallelo), la
mediante cromatica è l'altra condotta cromatica d'uso — ma è **colore d'accordo**
più che movimento: due triadi a terza, legate da una nota comune.

## Il principio: a terza, una nota in comune

Due accordi le cui fondamentali distano una **terza** (maggiore o minore) e che
**non** sono diatonicamente imparentati condividono **una sola** nota — contro le
**due** di una mediante diatonica (Do → Mi m). La nota comune fa la morbidezza;
lo scarto cromatico delle altre due voci fa la sorpresa. Niente funzione: è un
colore, non una cadenza.

⚠️ **La fonte qui è diversa dalle altre istruzioni.** Il termine «mediante
cromatica» è moderno (neo-riemanniano) e **non compare** nei libri in casa
(verificato su Piston). Quindi il rigore viene dal **`[CALC]`** — il fatto della
nota comune, verificabile e testato — non da una pagina citabile. Piston fa da
**contesto** (cap. 28 «Other Chromatic Chords», gli accordi cromatici e le
relazioni di terza), ma non lo si cita come se nominasse la cosa. È una scelta
dichiarata, approvata dall'utente.

⚠️ **La condotta va TENUTA** (`condotta=True`, il default): la nota comune resta
ferma e le altre voci si muovono di poco. È l'opposto del planing, dove la
condotta andava spenta.

## Cosa contiene l'istruzione

**Il vocabolario** — le quattro medianti cromatiche di una triade maggiore (in
Do): **La♭** e **Mi** (a terza maggiore, giù e su), **Mi♭** e **La** (a terza
minore). Ognuna una nota in comune con Do.

`[CALC]` Il test blinda il fatto che le definisce: le quattro condividono **una**
nota con Do, mentre la mediante diatonica (Mi m) ne condivide **due**.

**Il ciclo esatonico:** le medianti a terza maggiore (Do → La♭ → Mi → Do)
tornano a casa dopo tre passi — l'asse dell'accordo aumentato.

**Come si stabilisce:** scegli una casa (Do), vai a una sua mediante cromatica
tenendo la nota comune, torna. Non risolvere per dominante: il colore sta nello
scarto di terza.

## Il pezzo di prova (da zero)

Do che oscilla con le sue due medianti maggiori, e torna a casa, 8 battute, su
`set_scale` Do maggiore (la casa; le medianti sono il colore cromatico sopra):

```
C | Ab | C | E | C | Ab | E | C
```

con una melodia che mette in luce le note cromatiche nuove (il mi♭ di La♭, il
sol# di Mi), `condotta=True`. Il suono da colonna sonora. Rhodes / tromba /
basso, niente batteria.

**Feasibility verificata:** `Ab`, `E`, `Eb`, `A` parsano; `condotta=True` tiene
la nota comune (verificato su `C | Ab | E | C`). Nessuna aggiunta a `song.MODI`:
la casa è Do maggiore.

## Come si verifica / cosa resta

Test `[CALC]` verde; pezzo caricato (`MEDIANT01`), ascoltato; verdetto → esempio
lavorato. **Cosa resta fuori:** il *diatonic planing* e gli **accordi di
passaggio/approccio** cromatici — l'ultima faccia del cromatismo.

## Cosa NON rifare

- **non spegnere la condotta** qui: la nota comune tenuta È il colore (al
  contrario del planing);
- **non risolvere per dominante** la mediante: diventerebbe una tonicizzazione,
  un'altra cosa.
