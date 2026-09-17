# Scrivere una parte di batteria — feel HIP HOP (boom-bap)

⚠️ **PERIMETRO, e va letto prima di tutto.** Questa istruzione copre **un feel
solo**: l'hip hop **boom-bap** — dritto, lento (~90 BPM), backbeat forte,
sedicesimi radi. **Non è «la batteria nell'hip hop».**

L'hip hop ha altri idiomi accanto, e questo non li copre:

- il **trap / dirty south** è un altro suono (808, hi-hat a rulli di trentaduesimi,
  triplet) — un altro documento;
- il **lo-fi / swung boom-bap** (il feel «Dilla») è **swingato e laid-back**, e
  ⚠️ **NON è quello che il corpus misura** (vedi sotto): è una variante `[LIB]`+`[DEC]`;
- il **jazzy / neo-soul** hip hop è più vicino allo swing.

Il feel si dichiara **prima** di scrivere una nota. Qui si scrive il boom-bap che
la gente chiama così: DJ Premier, Pete Rock, l'East Coast — cassa pesante sul 1 e
sul 3, rullante che spacca sul 2 e sul 4, hi-hat in crome.

---

⚠️ **Questo documento NON dà una procedura che produce la parte.** Dà un
vocabolario, dei vincoli e il tocco. La parte la componi tu, battuta per battuta.
È la stessa lezione della batteria jazz e funk, pagata dieci versioni: le
statistiche su tutto il corpus danno **rumore con la forma giusta**.

**Cosa ti serve prima di cominciare:**

- la forma, e dove cominciano e finiscono le sezioni;
- **il basso, nota per nota** — nell'hip hop la batteria e il basso sono
  agganciati: il basso *è* il fondo della cassa. Vedi [basso-hiphop.md](basso-hiphop.md);
- il tempo: lento, **~85-95 BPM**.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura didattica, con fonte |
| `[MIS]` | misurato su un corpus, con quale e quante esecuzioni |
| `[OSS]` | osservato su un esecutore solo |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ **La misura di questo documento.** `[MIS]` Groove MIDI, etichetta **`hiphop`**
(per prefisso), `beat_type='beat'`: **34 esecuzioni**, **cinque batteristi**
(soprattutto drummer3, 7, 8), da 67 a 140 BPM (**mediana 91**). La BUR mediana è
**1,03**: cioè **dritto** — quartili 1,01-1,07. Il pocket è **stretto**: gli
scarti stanno a **−1/−2 tick** (kick −0,9, rullante −1,5), quasi sulla griglia.
Corroborato dai loop boom-bap della libreria `(aq) HipHop` (East Coast, ecc.),
che sono però **programmati**, non suonati. Strumenti: `GR.quote_per_voce()`,
`GR.scala()`, `GR.profilo()`.

⚠️ **La cosa più importante che la misura corregge:** il boom-bap di *questi*
batteristi è **dritto e sulla griglia**, NON swingato né laid-back. Lo swing
«Dilla» e il ritardo dietro la griglia sono un **altro sotto-idioma** (il lo-fi),
che questo corpus non ha — è la lezione del reggae, *un esecutore non è un
repertorio*, e vale in un verso: qui i batteristi suonano dritto, ma esiste un
hip hop swingato che sta altrove. Per quello, vedi «Lo swing» sotto.

---

## 1. Il vocabolario

Quali posizioni sono idiomatiche, e **quanto spesso** una voce le colpisce.
**È un catalogo, non una regola.** Griglia a **16 passi**: `1 e + a  2 e + a  3 e + a  4 e + a`.

### La cassa — il «boom», sul 1 e sul 3

```
percento:   76  3 43 29   6 19 40 30  45 23 36  9  18 18 22 27
passo:       1  e  +  a   2  e  +  a   3  e  +  a   4  e  +  a
```

`[MIS]` La cassa è ancorata sul **1 (76%)** e sul **3 (45%)** — i due «boom» del
boom-bap — e sincopa sui **levare**: il "+" del 1 (43%), il "+" del 2 (40%), il
"+" del 3 (36%). Mediana di velocity **62**, ~**4,4 colpi/battuta**: presente ma
non martellata. ⚠️ **Non è quattro casse fisse** (il 2 sta al 6%) né la cassa
fittissima del funk: è più **rada e pesante**, e lo spazio fa parte del groove.

### Il rullante — il «bap»: backbeat che SPACCA + ghost molli

Due strati dinamici della stessa voce, da pensare insieme.

```
backbeat:   .  .  .  .  X  .  .  .   .  .  .  .   X  .  .  .   (2 e 4, v127)
ghost:      .  o  .  .  .  o  o  o   o  o  .  o   .  o  o  o   (molli, ~50)
percento:   6 12  6  8  44  9 12 22  17 22  8 15  38 21 15 14
```

`[MIS]` Il **backbeat** cade sul **2 (44%)** e sul **4 (38%)**, ed è **fortissimo**:
la voce accentata del dataset (`rullante elettrico`) sta a velocity **mediana 127**
(q1 118), contro una mediana ~**50** dei ghost. I ghost riempiono intorno, non
ovunque uguale. ~**2,5 colpi/battuta**. ⚠️ **Il divario 127 / 50 È il groove**: se
i ghost hanno la forza del backbeat spariscono, e con loro il boom-bap.

### Il charleston a mano — le crome, molle

```
percento:  14 23 41 21  13 30 41 22  18 28 36 17  12 25 29 13
passo:      1  e  +  a   2  e  +  a   3  e  +  a    4  e  +  a
```

`[MIS]` L'hi-hat tiene il tempo sulle **crome**, con i **levare** ("+") più
presenti (36-41%). Mediana **41**: molle, sotto la cassa. ~**4,3 colpi/battuta**
— cioè **crome, non sedicesimi**: qui sta la differenza col funk, che riempie i
sedicesimi. L'hip hop lascia più aria.

### Il charleston a pedale — sui movimenti, rado

`[MIS]` Il piede chiude sui movimenti (~0,5 colpi/battuta), mediana 57. Sporadico.

---

## 2. Lo swing — dritto, e la variante swingata

`[MIS]` Il boom-bap misurato è **dritto**: BUR 1,03, `S.set_swing(doc, 50)`
(nessuno swing). È il feel di default di questo documento.

⚠️ `[LIB]`+`[DEC]` **La variante lo-fi / swung boom-bap** (il feel «Dilla») è
un'altra cosa: le crome dell'hi-hat sono **swingate** e leggermente **dietro** la
griglia (l'MPC swing, ~54-62%). Il corpus in casa **non ce l'ha** — sono altri
esecutori — quindi resta `[LIB]`+`[DEC]`. Per ottenerla: `S.set_swing(doc, 56)`
(un lilt leggero sulle crome dell'hi-hat) e, volendo, un tocco di ritardo. Ma è
una **scelta dichiarata**, non una misura: non spacciarla per il boom-bap dritto.

---

## 3. I vincoli

| vincolo | perché |
|---|---|
| **il boom sta sul 1 e sul 3** | `[MIS]` cassa 76%/45%. È l'ancora; bucare il 1 per troppe battute scioglie il groove |
| **la cassa non batte quattro movimenti fissi** | `[MIS]` il 2 sta al 6%. Quattro casse è rock/house, non boom-bap |
| **il backbeat spacca, i ghost restano molli** | `[MIS]` 127 contro ~50. Ghost alla forza del backbeat = rullo, non groove |
| **l'hi-hat sono CROME, non sedicesimi** | `[MIS]` ~4,3 colpi/battuta: il boom-bap lascia aria. I sedicesimi fitti fanno il funk o il trap |
| **dritto, salvo dichiararlo** | `[MIS]` BUR 1,03. Lo swing lo-fi è una variante `[LIB]`, da dichiarare, non il default |
| **nessuna regola su tutte le battute** | la trappola del generatore, come per ogni feel |

---

## 4. Come si decide UNA battuta

La domanda, con l'ancora del boom-bap:

**«Dove sono il boom (1 e 3) e il bap (2 e 4), cosa fa il basso, e cosa serve?»**

1. **Fissa il boom.** Cassa sul 1 e sul 3, con il basso.
2. **Metti il bap.** Rullante forte sul 2 e sul 4. È la costante.
3. **Guarda il basso.** Cassa e basso si agganciano sul 1 e sui levare sincopati:
   dove il basso mette una nota grave, spesso c'è la cassa.
4. **Riempi con parsimonia.** Un paio di sincopi di cassa sul "+", un pugno di
   ghost molli sul rullante, l'hi-hat in crome. Non tutto in una battuta.
5. **Dove sei nella forma?** Fine di frase (4, 8 battute), il ritornello: un buco,
   un fill, o l'hi-hat aperto.

---

## L'esempio lavorato

`tools/hiphop_scritto.py` è una parte intera — batteria + basso + un loop
d'accordi «polveroso» (Rhodes) — su un giro lo-fi di 4 battute in La minore.
⚠️ **Verdetto dell'ascolto (17 settembre 2026):** *«ok funziona»*.

---

## Cosa manca a questo documento

- **il suono**: il boom-bap vive del **campione polveroso** (batteria vinilica,
  filtrata, saturata) — è sound design, non note. Qui è un kit acustico di ripiego;
- **il trap** (808, hi-hat a trentaduesimi e triplet) e il **lo-fi swingato**, che
  sono idiomi vicini ma diversi;
- il **`[MIS]` sullo swing lo-fi**: servirebbe un corpus di esecuzioni swingate,
  che questo non è;
- il **fill hip hop** nello specifico: [fill.md](fill.md) è tarato sullo swing;
- il **break campionato** (la batteria *è* un loop tagliato da un disco): è la
  strada di jungle/DnB, e vive in `audio.py`, non qui.
