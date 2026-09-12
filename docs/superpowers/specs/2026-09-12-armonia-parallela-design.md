# L'armonia parallela (planing cromatico) — progetto

**Data:** 12 settembre 2026
**Cos'è:** la prima istruzione sul **cromatismo**, che non è una scala ma una
**condotta**: il movimento per semitoni. Copre il **planing** — far scivolare
una forma d'accordo in parallelo.

## Perché, e la scelta

Il cromatismo era l'ultimo tassello in «cosa manca» dell'armonia sperimentale.
⚠️ **Non è una scala** (niente campo armonico con un centro): è un modo di
muoversi. Copre più tecniche; scelta in brainstorming il 12 settembre: partire
dal **planing cromatico (armonia parallela)** — il movimento cromatico più puro,
textural, che si sposa con le scale simmetriche appena fatte. Le medianti
cromatiche e gli accordi di passaggio restano per dopo.

## Il principio: la forma scivola, la funzione sparisce

Il planing prende una **forma d'accordo** e la fa scivolare per semitoni, **senza
cambiarla**. `[LIB]` Piston, *Harmony* (5ª ed.), cap. 31 «After Common
Practice», «Parallel and Antiparallel Harmony» (pagina da pinnare scrivendo). Gli
accordi non si relazionano fra loro in senso funzionale: sono uno **stream
parallelo**. È l'opposto della condotta delle parti (che muove le voci di poco
in direzioni diverse): qui **tutte le voci si muovono dello stesso intervallo**.

⚠️ **Il punto tecnico che decide tutto:** `MU.armonia(..., condotta=False)`. Di
default la condotta riordina le voci per muoverne meno — e distruggerebbe il
parallelo. Con `condotta=False` ogni accordo è voicizzato rigido (posizione
fondamentale), e la forma scivola identica. Verificato: `C7 Db7 D7 Eb7` con
`condotta=False` dà ogni accordo = il precedente + 1 semitono.

## Cosa contiene l'istruzione

Forma delle istruzioni (principio → vocabolario → come si scrive → esempio).

**Il vocabolario** — cosa si fa scivolare:

- i **dom7** (ricchi, il suono jazz/modern), le **triadi** (maggiori o minori,
  il suono Debussy), i voicing **quartali**;
- il movimento **cromatico** (per semitono) — contro il *diatonic planing* (per
  grado, dentro una scala), che resta fuori da questo giro.

`[CALC]` Il test blinda il fatto che definisce il planing: **la forma è rigida e
parallela** — il dom7 spostato di N semitoni = `voci()` della base + N.

**Come si stabilisce:** scegli una forma, falla scivolare per semitoni, **non
risolvere**. La `set_scale` è **cromatica** (tutte e 12: nessuna tonalità, ogni
nota disponibile) — si aggiunge `'cromatica'` a `song.MODI`.

## Il pezzo di prova (da zero)

Un'onda cromatica di dom7 paralleli, 8 battute, `condotta=False`, su `set_scale`
cromatica:

```
C7 | Db7 | D7 | Eb7 | E7 | Eb7 | D7 | Db7
```

(sale di cinque semitoni, poi ridiscende). La tromba cavalca la voce in cima,
una **linea cromatica**; il basso segue le fondamentali (anch'esse cromatiche).
Il suono parallelo, textural. Rhodes / tromba / basso, niente batteria.

**Feasibility verificata:** `set_scale` accetta la cromatica a 12 note;
`MU.armonia(..., condotta=False)` dà il parallelo rigido.

## Come si verifica / cosa resta

Test `[CALC]` verde; pezzo caricato (`PLANING01`), ascoltato; verdetto → esempio
lavorato. **Cosa resta fuori:** il *diatonic planing* (scivolare dentro una
scala), le **medianti cromatiche** (terze con nota comune) e gli **accordi di
passaggio/approccio** cromatici — altre facce del cromatismo, altri giri.

## Cosa NON rifare

- **non lasciare la condotta attiva** nel pezzo di prova: `condotta=False` è il
  planing; `condotta=True` lo annulla;
- **non risolvere** lo stream parallelo in una cadenza: il colore sta nel
  parallelo che non punta a casa.
