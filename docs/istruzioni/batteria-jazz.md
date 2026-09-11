# Scrivere una parte di batteria jazz

⚠️ **Questo documento NON dà una procedura che produce la parte.** Dà un
vocabolario, dei vincoli e il tocco. La parte la componi tu, battuta per
battuta, e ogni battuta è una decisione.

La ragione sta scritta qui perché è costata dieci versioni:

> «usare statistiche su tutto il corpus non funziona, e anche l'analisi
> formale di una singola fonte non può funzionare per astrarre leggi
> compositive generalizzabili, che soprattutto nel jazz di fatto non
> esistono»

**Cosa ti serve prima di cominciare:**

- la forma, e dove cominciano e finiscono le sezioni;
- **la melodia, nota per nota** — è il contesto di ogni decisione;
- un groove template, cioè un batterista nominato da cui prendere il tocco.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura didattica, con libro e pagina |
| `[MIS]` | misurato su un corpus, con quale e quante esecuzioni |
| `[OSS]` | osservato su un esecutore solo |
| `[DEC]` | decisione presa qui, con la ragione |

---

## 1. Il vocabolario

Quali posizioni sono idiomatiche. **È un catalogo, non una regola**: nessuna
di queste va usata sempre.

### Il ride

```
x...x.x.x...x.x.    il giggidì (spang-a-lang)
```

I quattro movimenti più i levare del 2 e del 4. `[MIS]` che siano proprio
questi sei passi: su 21 esecuzioni jazz del Groove MIDI sono i soli che il
ride colpisce in più di metà delle battute (78, 76, 65, 75, 71, 61 per cento);
tutti gli altri stanno sotto il 33%.

`[LIB]` Riley p. 8: quattro semiminime di **uguale intensità**, e la nota di
*skip* **non accentata**. Il groove template lo conferma da solo — 127 sui
movimenti, 70 sulle crome — quindi il tocco è già a posto.

### Il charleston a pedale

```
....x.......x...    2 e 4
```

`[LIB]` Riley p. 8, `[OSS]` in 80 battute su 85.

### La cassa

```
x.......x.......    il feathering: 1 e 3, leggeri
```

più una **bomba**, che è un colpo in più, sempre su un levare o sul 4:

```
..............x.    levare del 4
......x.........    levare del 2
............x...    sul 4
```

`[OSS]` Il template dà 96 sul passo 0 e 86 sull'8: colpi leggeri.

### Il rullante

Sui **levare**, più i movimenti 2 e 4:

```
.......x....x...    levare del 2 + movimento 4
..........x.....    levare del 3
....x.......x...    2 e 4
.......x..x.....    levare del 2 + levare del 3
..........x...x.    levare del 3 + levare del 4
.......x..x...x.    tre colpi, per le battute più libere
```

⚠️ Il rullante **tace spesso**: circa un terzo delle battute.

---

## 2. I vincoli

Cosa **non** si fa. Ognuno è stato violato e l'orecchio l'ha respinto: accanto
c'è quale versione e cosa ne è venuto fuori.

| vincolo | cosa succede se lo violi |
|---|---|
| **il ride non si buca mai** | il tempo si spezza. `[LIB]` Riley p. 8: ogni nota ha un inizio definito ma nessuna fine, e deve scorrere nella successiva |
| **nessuna voce tace per intere battute** | versione **13**: «a parte il ride il resto è troppo rarefatto, praticamente assente per intere battute. non è che nel jazz il ride è un clock e il resto suona ogni tanto» |
| **non riempire ogni battuta** | versione **14**: «suona un po' pesante. un buon groove deve lasciare anche spazio agli altri strumenti» |
| **il rullante non batte lo stesso movimento del charleston in ogni battuta** | versione **15**: due voci sullo stesso colpo per 36 battute è un metronomo, non una conversazione |
| **la cassa resta leggera**: 1 e 3, mai quattro movimenti fissi | versione **14**, di nuovo il peso |
| **la batteria non raddoppia la melodia dove è fitta** | versione **14**: le aggiunte più dense stavano dove l'assolo fa dodici note. Un muro |
| **nessuna regola applicata uniformemente a tutte le battute** | versioni **13, 14, 15**: erano generatori travestiti, con dati scritti a mano al posto dei dadi. Il regolare suona male |

---

## 3. Il tocco

`MU.applica_groove()` posa sul pattern il microtiming e le velocity di un
batterista nominato. **Si applica dopo aver scritto le note**, e non si
discute: è misurato.

```python
note = MU.passi('x...x.x.x...x.x.', da=0)
rapporto = MU.applica_groove(note, profilo, dove='ride')
```

---

## 4. Come si decide UNA battuta

Non c'è una regola per l'intera parte. C'è una domanda da farsi ogni volta:

**«Cosa sta facendo la melodia in questa battuta, e cosa serve?»**

Conta le note della melodia in quella battuta, e usa questo come punto di
partenza — non come legge:

| la melodia fa | il rullante |
|---|---|
| 0-2 note | parla: due o tre colpi. È lì che c'è posto |
| 3-5 note | un colpo, o niente |
| 6 o più | tace |

`[LIB]` Riley p. 30: il solista può fare tre cose — salire verso un culmine,
scendere, o stare in piano — e il batterista sta in sincronia con quella
forma. Su un pezzo scritto la melodia la conosci già nota per nota, quindi la
regola diventa eseguibile: **rispondi dove la melodia lascia un buco, tieniti
fuori dove è piena**.

Poi guarda anche:

- **dove sei nella forma.** `[LIB]` p. 32: il blues è 12 battute in **tre
  frasi da quattro**; la forma standard è 32 battute AABA. La fine di una
  frase chiede qualcosa di diverso dal mezzo;
- **in che sezione sei.** Sotto un tema la batteria sta più indietro che
  sotto un assolo;
- **cosa hai fatto due battute fa.** Se ripeti troppo diventa uno stampo, se
  non ripeti mai diventa rumore.

### Il peso: 1 e 3, non 2 e 4

`[LIB]` p. 8, ed è una correzione esplicita a un luogo comune:

> «Per anni si è detto che 2 e 4 fossero i movimenti più importanti da sentire
> nel jazz. **L'idea è sbagliata.** In tutta la musica, jazz compreso, 1 e 3
> sono i movimenti "mamma" e "papà". [...] Serve un equilibrio, perché se 1 e
> 3 oppure 2 e 4 pesano troppo, la musica non groova.»

---

## 5. L'esempio lavorato

`tools/batteria_scritta.py` è una parte intera per un blues di 36 battute, con
**il motivo scritto accanto a ogni battuta**. Non è da copiare: è da leggere,
come si legge una partitura per capire come si fa.

Qualche riga, per dare l'idea:

```
   3   .......x..x.....  x.......x.......   il tema ha UNA nota: qui c'è posto
   8   .......x..x...x.  x.....x.x.......   IL TEMA TACE: la battuta più libera
  20   ....x.......x.x.  x.............x.   UNA NOTA nell'assolo: la risposta piena
  21   ................  x.......x.......   DODICI note: la batteria esce di scena
```

Numeri di quella parte: **402 colpi in 36 battute**, rullante muto in **11**.
Le parti scritte a mano che l'orecchio preferiva prima ne avevano 415 e 11.

---

## 6. A cosa serve il corpus, e a cosa no

Questa sezione vale oltre la batteria, ed è la lezione più cara del progetto.

**Serve a:**

- dare il **vocabolario** — quali posizioni esistono davvero;
- dare il **tocco** — microtiming e velocity, che sono misurabili;
- **prendere gli errori** — un pattern che nessun batterista suona è
  probabilmente sbagliato.

**Non serve a:**

- ⚠️ **produrre la parte.** Le statistiche su tutto il corpus danno rumore con
  la forma giusta: sono state respinte tre volte (versioni 07-11);
- ⚠️ **dare leggi generali da una fonte sola.** «Questo batterista batte il
  movimento 2 quasi sempre» è vero di lui e falso come regola: applicato a 36
  battute ha prodotto un metronomo (versione 15). *Un esecutore non è un
  repertorio*.

E lo stesso vale per i libri: **un esercizio non è una descrizione**. Riley
scrive «non suonare le semiminime con la cassa» (p. 24) e «due battute di
frase, poi quattro di silenzio» (p. 20) per far isolare una cosa alla volta a
chi studia. Presi alla lettera hanno prodotto due versioni respinte.

---

## Cosa manca a questo documento

- **il vocabolario delle figure di Riley** (pp. 18-29): sono in notazione, e
  la notazione non è ancora stata trascritta;
- **il fill**: dove va, quanto dura. Oggi è una decisione arbitraria messa sul
  turnaround;
- **le spazzole** e i feel diversi dallo swing (pp. 55-61);
- **le terzine**: la griglia a sedicesimi non le rappresenta, e per questo
  alcuni batteristi del corpus non si possono leggere.
