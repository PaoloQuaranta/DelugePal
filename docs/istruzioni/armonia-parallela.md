# L'armonia parallela (planing cromatico)

**A cosa serve.** Vuoi un blocco di suono che si sposta tutto insieme, senza che
gli accordi si «risolvano» l'uno nell'altro: una forma d'accordo che **scivola**
per semitoni. È il *planing* — l'armonia parallela, il gesto textural di Debussy
e di tanta musica modern.

È priorità 1 (armonia), e il primo pezzo di **cromatismo** del progetto.

⚠️ **Il cromatismo non è una scala: è una condotta.** L'[ottatonica](scala-ottatonica.md)
e l'[esatonale](scala-esatonale.md) sono campi armonici; qui non c'è un campo,
c'è un **modo di muoversi** — per semitoni. Quello che hanno in comune è che
nessuno dei tre risolve in senso tonale.

**Cosa ti serve prima di cominciare:** una **forma** d'accordo da far scivolare,
e la direzione (su o giù).

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sulle voci, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

---

## Il principio: la forma scivola, la funzione sparisce

`[LIB]` Piston, *Harmony* (5ª ed.), cap. 31 «After Common Practice», «Parallel
and Antiparallel Harmony», p. 496: nel planing gli accordi si muovono **in
parallelo**, mantenendo la stessa forma — e così **perdono il rapporto
funzionale** fra l'uno e l'altro. Sono uno **stream**, non una progressione.
L'esempio che Piston porta è di Debussy (String Quartet, p. 497).

È l'**opposto della condotta delle parti**: là le voci si muovono di poco, in
direzioni diverse, per legare un accordo al successivo; qui **tutte le voci si
muovono dello stesso intervallo**, e il legame è proprio che non cambia niente
tranne l'altezza.

⚠️ **Il punto tecnico che decide tutto:** `MU.armonia(..., condotta=False)`. Di
default la libreria riordina le voci per muoverne meno — e distruggerebbe il
parallelo. Con `condotta=False` ogni accordo è voicizzato rigido, in posizione
fondamentale, e la forma scivola identica. `[CALC]` Verificato dal test
`test_planing_cromatico`: `C7 Db7 D7 Eb7` con `condotta=False` dà ogni accordo =
il precedente + un semitono.

---

## Cos'è, e cosa si fa scivolare

Il planing **cromatico** muove la forma per **semitoni** (ogni passo uguale, la
`set_scale` è cromatica: tutte e 12 le note). Cosa scivola bene:

| forma | suono |
|---|---|
| **dom7** | ricco, jazz/modern — la settima e il tritono che scivolano |
| **triadi** (maggiori o minori) | il planing di Debussy, più limpido |
| **quartali** | aperto, sospeso |

⚠️ Il *diatonic planing* — far scivolare la forma **dentro una scala** (per
grado, non per semitono), dove la forma cambia un po' a ogni passo — è un colore
a parte: sta più sotto, nella sua sezione. Qui è tutto cromatico: la forma non
cambia mai.

---

## Come si stabilisce

1. **scegli una forma** (un dom7, una triade) e voicizzala;
2. **falla scivolare per semitoni**, su o giù, tenendola **identica**
   (`condotta=False`);
3. **non risolvere.** Niente cadenza, niente tonica d'arrivo: il colore sta nel
   blocco che si sposta e non punta a casa;
4. una **linea in cima** che segue lo scivolamento (una voce dell'accordo) rende
   il cromatismo udibile.

---

## Come si scrive, materialmente

```python
from delugexml import song as S, musica as MU

S.set_scale(doc, 'C', 'cromatica')        # nessuna tonalita': tutte le note
note = MU.armonia('C7 | Db7 | D7 | Eb7', registro='do3', durata='1/1',
                  condotta=False)          # ⚠️ False: la forma resta parallela
```

⚠️ **`condotta=False` non è un dettaglio**: con il default (`True`) gli accordi
si riordinano e il planing sparisce. È l'unico posto nelle istruzioni d'armonia
in cui la condotta va **spenta**.

---

## Esempio lavorato: l'onda cromatica

`[OSS]` Il primo pezzo di cromatismo del progetto — 12 settembre 2026. In
[`tools/planing_scritto.py`](../../tools/planing_scritto.py).

**L'idea:** il planing puro, da zero. Otto battute, tre voci, niente batteria.

**La progressione** — la stessa forma di dom7 che scivola per semitoni, su e giù:

```
C7 | Db7 | D7 | Eb7 | E7 | Eb7 | D7 | Db7
```

con `condotta=False`, così la forma resta rigida e parallela. La tromba cavalca
la settima di ogni accordo — una **linea cromatica** (sib-si-do-reb-re…).

**Dove si gioca:** niente risolve. Il blocco si sposta tutto insieme, per
semitoni, e non punta a nessuna casa — è lo stream parallelo di Debussy.

**Verdetto: approvato.** Il planing regge come colore, costruito dal nulla. Con
questo il progetto ha il suo primo **cromatismo** — una condotta, non una scala
— dopo le due scale simmetriche.

---

## Il diatonic planing: scivolare dentro una scala

⚠️ **Il fratello diatonico del planing cromatico.** Qui la forma **non** resta
rigida: scivola **dentro una scala**, per grado, e a ogni passo **cambia un po'**
perché si piega alle note disponibili. `[CALC]` I sette accordi di terza del Do
maggiore — Do, Re m, Mi m, Fa, Sol, La m, Si dim — sono tutti **dentro la scala**,
ma la forma flette: maggiore, minore, diminuita. È l'opposto del cromatico, dove
la forma non cambia mai. Verificato da `test_diatonic_planing`.

Il suono è più morbido e «dentro»: nessuna nota fuori tonalità, lo scivolamento
resta consonante col campo. `[DEC]` La condotta resta **spenta**
(`condotta=False`) come nel cromatico — è ancora uno stream parallelo, solo che il
parallelo è per **grado di scala** invece che per semitono. La `set_scale` è la
scala scelta (maggiore, un modo…), non la cromatica.

```python
S.set_scale(doc, 'C', 'maggiore')     # la scala dentro cui scivolare
note = MU.armonia('C | Dm | Em | F | G | Am', registro='do3', durata='1/1',
                  condotta=False)      # scivola per grado, la forma flette
```

---

## Cosa manca a questa istruzione

- ~~**il diatonic planing**~~ — **fatto** (sopra): la forma scivola dentro una
  scala, per grado, e flette a ogni passo;
- **le medianti cromatiche** — accordi a terza con una nota in comune (C→A♭→E),
  il colore «cinematografico»: c'è, in [`medianti-cromatiche.md`](medianti-cromatiche.md)
  (con le doppie medianti, a terza senza nota comune);
- **gli accordi di passaggio/approccio** cromatici — la colla funzionale: c'è, in
  [`accordi-di-passaggio.md`](accordi-di-passaggio.md).
