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

⚠️ Resta fuori da questo giro il *diatonic planing* — far scivolare la forma
**dentro una scala** (per grado, non per semitono), dove la forma cambia un po'
a ogni passo. Qui è tutto cromatico: la forma non cambia mai.

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

⚠️ **In costruzione.** Il pezzo di prova è un'onda di dom7 paralleli — `C7 | Db7
| D7 | Eb7 | E7` e ritorno — con la tromba che cavalca la settima, una linea
cromatica: `tools/planing_scritto.py`. L'esempio e il verdetto dell'utente vanno
qui appena ascoltato sul Deluge.

---

## Cosa manca a questa istruzione

- **il diatonic planing** — far scivolare una forma *dentro una scala* (per
  grado): la forma cambia a ogni passo, ed è un altro colore;
- **le medianti cromatiche** — accordi a terza con una nota in comune (C→A♭→E),
  il colore «cinematografico»: un'altra faccia del cromatismo;
- **gli accordi di passaggio/approccio** cromatici — la colla funzionale (la
  dominante di tritono, la diminuita di passaggio) fra accordi diatonici.
