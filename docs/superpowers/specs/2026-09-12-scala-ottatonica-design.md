# La scala ottatonica — progetto

**Data:** 12 settembre 2026
**Cos'è:** la prima istruzione su una **scala non diatonica**, dopo che il
prestito modale ha chiuso le due case tonali. Copre l'**ottatonica** (la scala
diminuita): un colore simmetrico, fuori dal tonale.

## Perché, e la scelta

Il perimetro mette l'armonia al centro, e l'utente è **sperimentale**: le sue
song usano scale a otto note, ottatoniche, cromatiche. Finora le istruzioni
coprono il diatonico (i sette modi) e il prestito fra modi paralleli; le scale
non diatoniche erano in «cosa manca».

Scelta in brainstorming il 12 settembre: **partire dall'ottatonica da sola** —
la più ricca e idiomatica, quella nominata dall'utente, ben documentata. L'
esatonale e il cromatismo restano per dopo (il cromatismo non è nemmeno una
scala con un centro: è una condotta, un'altra bestia).

## Il principio: colore simmetrico, non funzione

L'ottatonica è **statica per costruzione**, come l'armonia modale è statica per
scelta. `[LIB]` Smith, *Jazz Theory* (4ª ed.), cap. IX, p. 75-77, «The
"Diminished" Scale»: è il pattern ripetuto **tono-semitono** (o semitono-tono),
e *«come l'accordo diminuito, la scala diminuita si può trasporre per semitono
in una sola direzione due volte soltanto; una terza trasposizione riproduce le
note originali»* — cioè **esistono solo 3 ottatoniche distinte**, ed è simmetrica
per **terza minore**.

La conseguenza armonica: niente sensibile, niente centro unico (per simmetria ci
sono quattro «toniche» equivalenti). Non risolve: shimmera. Il lavoro è far
sentire la simmetria, e **non risolverla tonalmente** — se la risolvi, collassa,
esattamente come il modale.

## Cosa contiene l'istruzione

Forma collaudata (principio → vocabolario → come si stabilisce → come si scrive
→ esempio). Fonte: Smith p. 75-77; Piston cap. 31 «After Common Practice»
(scale artificiali/simmetriche) come secondaria, pagina da pinnare scrivendo.

**Il vocabolario** — gli accordi che l'ottatonica genera:

- le **due forme**: **tono-semitono (WH)** per i diminuiti, **semitono-tono
  (HW)** per i dom7♭9 (Smith p. 76: la WH parte dalla fondamentale del dim7, la
  HW dalla terza del dom7);
- i **dim7** e i **dom7♭9**;
- il cuore: il **ciclo dei quattro dom7 a terza minore** — `C7 Eb7 Gb7 A7` —
  tutti dentro una sola ottatonica. È la mossa che fa sentire la simmetria.

`[CALC]` Il test blinda due fatti: l'ottatonica è **invariante per terza minore**
(+3 semitoni = sé stessa) e i **quattro dom7** a terza minore stanno tutti dentro.

**Come si stabilisce:** il ciclo per terza minore (o l'alternanza di due dim7),
facendo sentire che la scala non ha un centro; evitare la cadenza che la
risolverebbe nel tonale.

## Il pezzo di prova (da zero)

Il ciclo simmetrico, 8 battute, su `set_scale` con l'ottatonica HW di Do
(`0,1,3,4,6,7,9,10`):

```
C7 | Eb7 | Gb7 | A7 | C7 | Eb7 | Gb7 | A7
```

con una **linea ottatonica discendente** in cima (do-sib-la-sol-solb-mi-mib-reb,
una nota per battuta) — il suono sospeso e simmetrico della scala. Rhodes /
tromba / basso sulle fondamentali (do-mib-solb-la), niente batteria.

**Feasibility verificata:** `set_scale` accetta l'ottatonica a 8 note e la
scrive in `modeNotes`; il Deluge la regge (le song dell'utente la usano). I dom7
li realizza `MU.armonia` dalle sigle.

## Come si verifica / cosa resta

Test `[CALC]` verde; pezzo caricato sul Deluge (nome nuovo `OTTATON01`),
ascoltato; il verdetto diventa l'esempio lavorato. **Cosa resta fuori:**
l'esatonale, il cromatismo, e l'uso **funzionale** dell'ottatonica (la HW sopra
una dominante che risolve, che è l'opposto del colore statico — un altro giro).

## Cosa NON rifare

- **non risolvere l'ottatonica tonalmente** nel pezzo di prova: ne ucciderebbe
  la simmetria, che è tutto il punto;
- **non chiamarla "modo"**: non è un modo del maggiore, è una scala simmetrica a
  sé — va in `song.MODI` (o dove) solo come intervalli, con la sua fonte.
