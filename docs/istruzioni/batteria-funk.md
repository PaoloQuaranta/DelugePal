# Scrivere una parte di batteria — feel FUNK (dritto)

⚠️ **PERIMETRO, e va letto prima di tutto.** Questa istruzione copre **un feel
solo**: il funk **dritto** — sedicesimi diritti, backbeat, `set_swing` a 50
(nessuno swing). **Non è «la batteria nel funk».**

Il funk ha altri feel accanto, e il Groove MIDI li tiene separati con
un'etichetta a sé — la misura sotto li ha **esclusi apposta**:

- il **purdieshuffle** (l'half-time shuffle) è **swingato**: BUR **1,80**
  misurata, un altro documento;
- il **new orleans / second line** è un altro idioma (il rullante fa lo
  *second-line* col cross-stick e i rulli), non è questo;
- il **funk/latin** è un altro feel ancora.

Il feel si dichiara **prima** di scrivere una nota. Qui si scrive il funk che
la gente chiama funk: James Brown, i Meters, Tower of Power — cassa
sincopata sul **the one**, backbeat sul 2 e sul 4, charleston in sedicesimi.

---

⚠️ **Questo documento NON dà una procedura che produce la parte.** Dà un
vocabolario, dei vincoli e il tocco. La parte la componi tu, battuta per
battuta, e ogni battuta è una decisione. È la stessa lezione della
batteria jazz ([batteria-jazz.md](batteria-jazz.md)), pagata dieci versioni:
le statistiche su tutto il corpus danno **rumore con la forma giusta**.

**Cosa ti serve prima di cominciare:**

- la forma, e dove cominciano e finiscono le sezioni;
- **il basso, nota per nota** — nel funk la batteria e il basso sono **una cosa
  sola**, agganciati sul *the one*. La cassa non si scrive senza sapere cosa fa
  il basso, e viceversa. Vedi [basso-funk.md](basso-funk.md);
- un groove template funk, cioè un batterista nominato da cui prendere il tocco.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura didattica, con fonte |
| `[MIS]` | misurato su un corpus, con quale e quante esecuzioni |
| `[OSS]` | osservato su un esecutore solo |
| `[DEC]` | decisione presa qui, con la ragione |

`[LIB]` **non è più forte di `[MIS]`, è diverso.** Il libro dice *come si fa*,
il corpus dice *cosa fanno davvero i dischi*.

⚠️ **La misura di tutto questo documento.** `[MIS]` Groove MIDI, etichetta
**esatta** `funk` (non il prefisso: `funk/purdieshuffle` e `funk/fast` sono
swingati e sono fuori), `beat_type='beat'`, scartate le esecuzioni con BUR > 1,3:
restano **33 esecuzioni su 36**, **quattro batteristi** (drummer1, 5, 7, 8),
tutte in 4/4, da 80 a 138 BPM (mediana 100). La BUR mediana è **1,02**: dritto,
come il feel promette. Lo strumento è `GR.quote_per_voce()` e `GR.scala()`.

---

## 1. Il vocabolario

Quali posizioni sono idiomatiche, e **quanto spesso** una voce le colpisce
nelle battute in cui suona. **È un catalogo, non una regola**: nessuna di
queste va usata sempre, e i numeri sono un limite, non un motore.

La griglia è a **16 passi** (sedicesimi). Le colonne sono i movimenti e le loro
suddivisioni: `1 e + a  2 e + a  3 e + a  4 e + a`.

### La cassa — il *the one* e la sincope

```
percento:   87  5 31 43  10 17 10 35  46 11 51 25   9 18 14  6
passo:       1  e  +  a   2  e  +  a   3  e  +  a    4  e  +  a
```

`[MIS]` La cassa è ancorata sul **movimento 1 all'87%**: è *the one*, la cosa
più stabile di tutto il funk. Il resto è **sincope**, e non è distribuito a
caso: il picco secondario è il **levare del 3** (il "+", 51%), poi il **3**
(46%) e la **"a" del 1** (43%). La cassa funk **spinge** dentro il movimento
successivo dai levare e dalle "a".

`[LIB]` music-composition, `instrument-idiom/bass.md`: *«Kick marks downbeats,
bass syncopates»* è una delle relazioni cassa/basso, ma nel funk vale spesso
l'opposto — la cassa **è** la sincope e il basso ci si incastra. La scelta è di
battuta.

⚠️ **La cassa NON è quattro colpi fissi.** Il 4 sta al 9%: mettere la cassa su
tutti i movimenti fa il rock, non il funk.

### Il rullante — backbeat forte + ghost note molli

Sono **due strati dinamici della stessa voce**, e vanno pensati insieme.

```
backbeat:   .  .  .  .  X  .  .  .   .  .  .  .   X  .  .  .   (2 e 4, ACCENTATI)
ghost:      .  o  .  .  .  o  .  o   .  o  .  o   .  o  .  o   (molli, riempiono)
percento:   22 40 14  7  46 39 25 62  22 58 17 26  37 31 23 52
```

`[MIS]` Il **backbeat** cade sul **2 (46%)** e sul **4 (37%)** ed è forte:
misurato a velocity **127** sulla voce accentata (`rullante elettrico` del
dataset), contro una **mediana 38** per i ghost. I **ghost** riempiono i
sedicesimi intorno, e non ovunque uguale: i picchi sono la **"a" del 2** (62%),
la **"e" del 3** (58%), la **"a" del 4** (52%), la **"e" del 1** (40%). È la
trama che fa *tirare* il funk.

`[DEC]` Nel dataset il backbeat forte e i ghost stanno spesso su **due note GM
diverse** (`rullante` e `rullante elettrico`): è un artefatto del kit
elettronico, non due strumenti. Qui è **una voce sola** con due velocity —
l'accento sul 2 e 4, i fantasmi molli intorno.

⚠️ **Il divario di velocity È il groove.** Se i ghost hanno la stessa forza del
backbeat non sono ghost: diventa un rullo, e il funk sparisce. Backbeat forte,
ghost quasi inudibili.

### Il charleston (a mano) — i sedicesimi

```
percento:   32 30 50 43  20 29 57 46  40 34 36 34  27 28 36 23
passo:       1  e  +  a   2  e  +  a   3  e  +  a    4  e  +  a
```

`[MIS]` Il charleston tiene il tempo sui **sedicesimi** (o sulle crome), molle
(mediana **37**), con i levare ("+" dei movimenti) leggermente più presenti
(50-57%). È il *clock* del funk, ma un clock che respira: gli accenti sporadici
sul levare sono ciò che lo distingue da un metronomo.

### Il charleston a pedale — i quarti, e il piede sul 4

```
percento:   44  0 19  0  39  0 17  0  24  0 19  1  62  0 20  0
passo:       1  e  +  a   2  e  +  a   3  e  +  a    4  e  +  a
```

`[MIS]` Il piede chiude sui **movimenti**, e più di tutto sul **4 (62%)**: è la
chiusura che prepara il ritorno al *the one*. Velocity mediana **55**.

### Il ride — quando c'è, è in crome

```
percento:   79  7 57 16  77  7 70 16  79  9 63 16  67  9 59 14
```

`[MIS]` Alcune esecuzioni usano il ride al posto del charleston: allora fa le
**crome** (movimenti + levare, tutti sopra il 57%), mediana **68**. È
un'alternativa al charleston, non un'aggiunta.

---

## 2. I vincoli

Cosa **non** si fa. Sono la faccia negativa della misura e della letteratura.

| vincolo | perché |
|---|---|
| **il *the one* non si tocca** | è l'ancora del funk: la cassa sul 1 sta all'87%. Bucarlo per troppe battute di fila scioglie il groove |
| **la cassa non batte quattro movimenti fissi** | `[MIS]` il 4 sta al 9%. Quattro casse è rock; il funk sincopa fra 1, "+" del 3 e le "a" |
| **i ghost restano molli** | `[MIS]` mediana 38 contro 127 del backbeat. Ghost alla forza del backbeat = rullo, non groove |
| **il backbeat non si sposta** | 2 e 4 sono l'asse; muoverli fa un altro feel |
| **il charleston non si buca a caso** | è il clock: se sparisce per intere battute il tempo galleggia (stessa famiglia del vincolo sul ride jazz) |
| **nessuna regola applicata a tutte le battute** | `[DEC]` è la trappola del generatore: dati scritti a mano al posto dei dadi suonano comunque a stampo. Vale qui come per il jazz |
| **la batteria non raddoppia il basso dove è fitto** | la relazione è di **collocazione**, non di quantità: incastri i colpi *dove* il basso lascia il buco o *dove* il basso spinge, non facendo tutti e due la stessa cosa |

---

## 3. Il tocco

`MU.applica_groove()` posa sul pattern il microtiming e le velocity di un
batterista funk nominato. **Si applica dopo aver scritto le note**, ed è
misurato.

⚠️ **Il pocket funk è TIGHT.** `[OSS]` Sul template `drummer8/session1/1`
(95 BPM, BUR 1,07) gli scarti stanno a **−1/−2 tick** sulla cassa e a
**0/+1** sul rullante: quasi sulla griglia. È l'opposto dello swing, dove il
levare si sposta di molto. Nel funk il carattere sta nelle **velocity** (il
divario ghost/backbeat) più che nello spostamento temporale.

```python
note = MU.passi('x.......x.......', da=0)      # cassa: the one + il 3
rapporto = MU.applica_groove(note, profilo_funk, dove='kick')
```

Il template si sceglie nominandolo, mai mediando più batteristi (media = verso
la griglia = perdi il pocket). Due funk diversi già in mano:

- `drummer8/session1/1` — funk **pulito**: backbeat netto, cassa scarna,
  charleston in crome. Il punto di partenza consigliato;
- `drummer5/session1/15` — funk **ghost-heavy**: rullante fitto di fantasmi,
  cassa più sincopata. Per una sezione più densa.

---

## 4. Come si decide UNA battuta

Non c'è una regola per l'intera parte. C'è una domanda, la stessa del jazz ma
con un'ancora in più:

**«Cosa fa il basso in questa battuta, dov'è il *the one*, e cosa serve?»**

1. **Fissa il *the one*.** Cassa sul 1, quasi sempre. È il punto attorno a cui
   gira tutto.
2. **Guarda il basso.** Nel funk cassa e basso si **agganciano**: dove il basso
   mette una nota accentata, spesso c'è la cassa; dove il basso lascia spazio,
   la batteria può parlare. Non raddoppiare tutto — incastrare.
3. **Metti il backbeat.** 2 e 4, forti. È la costante.
4. **Riempi con i ghost, con parsimonia.** Uno o due sedicesimi molli dove la
   battuta lo chiede — non tutti quelli del vocabolario in una volta.
5. **Dove sei nella forma?** Fine di frase (4, 8, 16 battute) chiede qualcosa
   di diverso dal mezzo — un buco, una sincope in più, un fill (vedi
   [fill.md](fill.md)).

`[LIB]` music-composition, `instrument-idiom/bass.md`, sul funk: *«Leave space;
let drums answer»*. Lo spazio non è vuoto, è la parte dove risponde qualcun
altro.

---

## L'esempio lavorato

`tools/funk_scritto.py` è una parte intera — batteria + basso — su un vamp
Em7 | A7 di 8 battute, col motivo scritto accanto a ogni battuta. Non è da
copiare: è da leggere. ⚠️ **Verdetto dell'ascolto (16 settembre 2026):** la
batteria *«va bene»*. (Il basso: *«meglio, soddisfacente per il test»* — vedi
[basso-funk.md](basso-funk.md).)

## Cosa manca a questo documento
- **le spazzole** e i feel funk vicini (purdieshuffle, second line);
- **il fill funk** nello specifico: [fill.md](fill.md) è tarato sullo swing;
- **le terzine e il mezzo-tempo**: la griglia a 16 passi tiene i sedicesimi
  dritti, ma non l'half-time shuffle.
