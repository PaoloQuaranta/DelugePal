# La scala esatonale (whole-tone) — progetto

**Data:** 12 settembre 2026
**Cos'è:** la seconda scala non diatonica, gemella dell'ottatonica. Copre
l'**esatonale** (whole-tone): un colore simmetrico che galleggia, il suono di
Debussy.

## Perché, e la scelta

Dopo l'ottatonica, l'esatonale è l'altra scala simmetrica — era in «cosa manca»
della scala ottatonica. Stessa famiglia (simmetrica, statica, senza funzione),
colore diverso: l'ottatonica è tesa (dim7, dom7♭9), l'esatonale è sospesa
(aumentate, dom7♯5).

## Il principio: colore simmetrico, non funzione

L'esatonale è **simmetrica per tono**, quindi esistono solo **2 esatonali
distinte**. `[LIB]` Piston, *Harmony* (5ª ed.), cap. 31 «After Common
Practice», «The Whole-Tone Scale», p. 490: *«la scala esatonale di sei note è
una partizione simmetrica dell'ottava cromatica»*.

⚠️ **Non ha la quinta giusta.** Tutte le distanze sono toni: niente quinta
giusta, niente terza minore → **nessuna triade consonante, solo aumentate**. È
la ragione tecnica del suo galleggiare. `[LIB]` Piston, cap. 28, p. 439: *«una
successione cromatica di triadi aumentate perde il senso di tonalità definita…
questa simmetria suggerisce l'origine della scala esatonale».*

Come l'ottatonica e il modale: **colore statico, non funzione**. Non risolve; se
la metti sotto una cadenza, collassa.

⚠️ **La fonte è Piston, NON Smith** — Smith (il *Jazz Theory*) non tratta la
whole-tone (verificato: zero occorrenze). Qui cambia il libro.

## Cosa contiene l'istruzione

Forma delle istruzioni (principio → vocabolario → come si scrive → esempio).

**Il vocabolario** — gli accordi che l'esatonale genera:

- le **triadi aumentate** — solo **2 distinte** nella scala (C+ = E+ = G#+, e
  D+ = F#+ = A#+): le due insieme fanno l'intera scala;
- i **dom7♯5** e **dom7♭5** — su ogni grado, tutti dentro la scala;
- la mossa: **dom7♯5 paralleli che salgono per tono** — fa sentire la simmetria.

`[CALC]` Il test blinda: l'esatonale è **invariante per tono** (+2 = sé stessa),
ha **6 note**, e i dom7♯5 del ciclo ci stanno tutti dentro.

## Il pezzo di prova (da zero)

Il ciclo di dom7♯5 che sale per tono, 8 battute, su `set_scale` esatonale di Do
(`0,2,4,6,8,10`):

```
C7#5 | D7#5 | E7#5 | F#7#5 | G#7#5 | A#7#5 | C7#5 | D7#5
```

con una **melodia ondeggiante whole-tone** (sol#-la#-do-re-mi-re-do-la#) e il
basso sulle fondamentali (do-re-mi-fa#-sol#-la#). Il suono sospeso, "acquatico".
Rhodes / tromba / basso, niente batteria.

**Feasibility verificata:** `Caug`/`C+`, `C7#5`, `C7b5` parsano e sono tutti
whole-tone; `set_scale` accetta l'esatonale a 6 note. L'esatonale entra in
`song.MODI` come nominata, accanto all'ottatonica.

## Come si verifica / cosa resta

Test `[CALC]` verde; pezzo caricato (`ESATON01`), ascoltato; verdetto → esempio
lavorato. **Cosa resta fuori:** il cromatismo (una condotta, non una scala),
l'uso funzionale (dom7♯5 che risolve), le scale artificiali non simmetriche.

## Cosa NON rifare

- **non risolvere l'esatonale tonalmente**: ne ucciderebbe il galleggiamento;
- **non cercare una triade maggiore/minore** nella scala: non c'è, solo
  aumentate — è il punto, non una mancanza.
