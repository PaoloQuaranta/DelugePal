# Scrivere una parte di batteria jazz

**A cosa serve.** Hai un pezzo con una forma e ti serve la batteria. Questa
istruzione dice **chi fa cosa**, **quando**, e soprattutto **quando tacere**.

**Cosa ti serve prima di cominciare:**

- la forma, e dove cominciano e finiscono le frasi;
- quale sezione è (tema, assolo, ultimo giro): la batteria cambia;
- un groove template, cioè un batterista nominato da cui prendere il tocco.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura didattica, con libro e pagina |
| `[MIS]` | misurato su un corpus, con quale e quante esecuzioni |
| `[DEC]` | decisione presa qui, con la ragione |

---

## Prima di tutto: quattro strati che suonano SEMPRE

`[OSS]` Guardate una per una le 85 battute di `drummer10/session1/1` nel
Groove MIDI Dataset, con `GR.battute_per_voce()`. Un esecutore solo, quindi
`[OSS]` e non `[MIS]`.

Su 85 battute: **charleston a pedale 80, rullante 77, cassa 70, ride 54**.
Nessuna voce «entra ogni tanto». Nelle battute di tempo normale c'e' uno
strato costante, uguale ovunque:

```
ride       x...x.x.x...x.x.    il giggidi'
cassa      x...x...x...x...    quattro movimenti, leggeri: il feathering
hh pedale  ....x.......x...    2 e 4
rullante   ....x...........    il movimento 2
```

⚠️ **«Quasi sempre» non e' «sempre», e la differenza si sente.** Riempire
ogni battuta ha prodotto una batteria «un po' pesante»: *«un buon groove di
batteria deve lasciare anche spazio agli altri strumenti, non puo' riempire
sempre tutto»* (verdetto sulla versione 14). E le assenze del batterista vero
sono **sezionali**, non sparse: nelle battute 1-8 la cassa non c'e' affatto,
poi entra e resta. Quindi lo strato si alleggerisce **per sezione** -- sotto i
temi la cassa batte 1 e 3 invece di quattro -- non a caso battuta per battuta.

⚠️ **La varieta' sono AGGIUNTE SOPRA quello strato, non presenza o assenza.**
Il rullante tiene il 2 e ci mette sopra da zero a tre colpi, sui levare
(passi 6, 10, 14) e sui movimenti 3 e 4. Esempi presi dalle battute vere:

```
....x.....x.....    2 + levare del 3
....x.......x.x.    2 + 4 + levare del 4
....x...x...x.x.    2 + 3 + 4 + levare del 4
```

⚠️ **E il ride puo' migrare.** Alle battute 29-44 di quell'esecuzione il ride
tace e il giggidi' lo suona il **tom basso**. Il nome GM non e' il ruolo
musicale: e' la stessa lezione gia' scritta nella casella 10.

## Chi tiene e chi parla, e perche' non basta

`[LIB]` John Riley, *The Art of Bop Drumming*, pp. 8 e 24.

| voce | funzione |
|---|---|
| **ride** | tiene il tempo: quattro quarti di **uguale intensita**, piu' la nota di *skip* sui movimenti 2 e 4, suonata **piu' piano**. Non segue il comping: Riley, «tieni il ride fermo, perche' vorra' andare dietro alla cassa» |
| **charleston a pedale** | 2 e 4 |
| **rullante** | l'ancora sul 2, e sopra il comping |
| **cassa** | il feathering sui quattro movimenti, e sopra le **bombe** -- accenti isolati |

⚠️ **DUE COSE CHE QUESTA ISTRUZIONE DICEVA E SONO SBAGLIATE**, corrette il
10 settembre 2026 dopo che l'orecchio ha respinto la versione 13:

1. *«la cassa non suona le semiminime»*. Riley lo scrive a p. 24, ma e' un
   **esercizio** per sviluppare la cassa come terza mano. Questo batterista
   suona `x...x...x...x...` per decine di battute di fila: e' il feathering,
   e le velocity del groove template lo rendono leggero.
2. *«due battute di frase, poi quattro di silenzio»*. Riley p. 20, ed e'
   anche quello un **esercizio di pacing**. Preso alla lettera ha prodotto
   una batteria respinta cosi': «a parte il ride il resto e' troppo
   rarefatto, praticamente assente per intere battute. non e' che nel jazz il
   ride e' un clock e il resto suona ogni tanto, anche le altre parti di
   batteria hanno una funzione ritmica».

⚠️ **La lezione di metodo, e vale piu' delle due correzioni:** un libro
didattico insegna con esercizi che ISOLANO una cosa alla volta. Un esercizio
non e' una descrizione di come suona la musica. Quando un libro dice «non
fare X», controlla sul corpus se davvero non lo fanno.

### Il peso: 1 e 3, non 2 e 4

`[LIB]` p. 8, ed è una correzione esplicita a un luogo comune:

> «Per anni si è detto che 2 e 4 fossero i movimenti più importanti da sentire
> nel jazz. **L'idea è sbagliata.** In tutta la musica, jazz compreso, 1 e 3
> sono i movimenti "mamma" e "papà". La gente balla su 1 e 3, non su 2 e 4.
> [...] Serve un equilibrio, perché se 1 e 3 oppure 2 e 4 pesano troppo, la
> musica non groova.»

### Il suono: le note si tengono per mano

`[LIB]` p. 8. Ogni nota del ride deve avere **un inizio definito ma nessuna
fine**: il suono di ogni colpo deve **scorrere** in quello dopo, non stare
separato. Riley lo fa provare suonando il pattern sul rullante (suona rigido,
il suono finisce) e poi sul tom (suona meglio, le note si legano).

⚠️ In pratica, su una batteria scritta: **il ride non si buca**. Una nota
mancante è un silenzio, e il tempo si spezza.

---

## La frase: il comping si muove a gruppi, e non e' regolare

`[LIB]` Riley p. 20, il capitolo «Pacing»:

> «Un buon modo per imparare ad accompagnare musicalmente e' suonare ogni
> frase di **due battute due volte**, e poi suonare **quattro battute di solo
> tempo, senza comping**. Questo esercizio ti mostra un tipo di *ritmo* o
> *densita'* fra l'accompagnare e il tenere il tempo. Ricorda che le tue idee
> di comping devono **accompagnare** e **completare** quello che suonano gli
> altri.»

⚠️ **E' un esercizio, non una ricetta.** Quello che va preso e' il principio:
il comping ha una **densita' che cambia**, e non e' uniforme battuta per
battuta. Quello che NON va preso alla lettera e' il silenzio di quattro
battute: nelle battute vere il rullante e la cassa continuano a suonare il
loro strato, e a cambiare e' solo quanto ci mettono sopra.

### Dove cadono le frasi

`[LIB]` p. 32. Il **blues** è 12 battute divise in **tre frasi da quattro**.
La **forma standard** è 32 battute in quattro frasi da otto, AABA, e il *feel*
cambia spesso sul ponte.

Le frasi di due battute del comping si appoggiano su questa griglia: non
cominciano dove capita.

---

## L'arco: il solista fa tre cose sole

`[LIB]` p. 30, «Accompanying a Soloist».

Alla domanda «quando accompagno?» Riley risponde che decidono le orecchie, e
che devi **sempre sapere dove sei nella forma**. Gli assoli hanno una forma
fatta di **picchi e valli**, e il solista può fare solo tre cose:

- **salire verso un culmine**
- **scendere da un culmine**
- **stare in piano**

Il batterista sta in sincronia con quella forma. Riley lo spiega con due
telefonate: in una i due si ascoltano e si rispondono; nell'altra il secondo
dice «che bello… mmh… ciao» e riattacca. *«Quale delle due musiche ti
piacerebbe di più?»*

`[DEC]` Su un pezzo generato non c'è un solista che ascolta in tempo reale, ma
**la melodia la conosciamo già, nota per nota**. Quindi la regola diventa
eseguibile: la batteria **risponde dove la melodia lascia un buco** e **tace
dove è piena**.

⚠️ È l'errore della versione 14: le aggiunte più fitte stavano alle battute
21-22, che sono le due in cui l'assolo fa dodici note. Raddoppiare invece di
rispondere fa un muro. Le densità del tema e dell'assolo si contano prima di
scrivere un colpo:

```
tema     4 3 1 2 4 3 1 0 4 4 3 2      <- si risponde su 3, 4, 7, 8
assolo   5 6 6 2 5 7 6 1 12 12 5 0    <- si risponde su 16 e 20, si tace su 21-22
```

---

## I numeri misurati, come limite

`[MIS]` Groove MIDI Dataset, 37 esecuzioni jazz in 4/4.

| | valore |
|---|---|
| attacchi per battuta, tutte le voci insieme | **8,73**, deviazione 2,08 |
| passi che il ride colpisce in più di metà delle battute | **0, 4, 6, 8, 12, 14** — il giggidì |
| quanto spesso il ride colpisce quei passi | 78, 76, 65, 75, 71, 61 per cento |
| tutti gli altri passi del ride | sotto il 33% |

⚠️ **Non confondere questo numero con quello del Jazz Trio Database**, che dà
6,31 attacchi per battuta: JTD li conta con un rilevatore di onset su una
registrazione di trio missata, che ne trova meno. Inseguire quel numero ha
prodotto una versione intera da buttare — la 10 — perché un budget di sei
attacchi spalmato su sei voci **spezza il ride**, che da solo ne vale sei.

`[MIS]` Jazz Trio Database, 1099 esecuzioni: la densità della batteria **non
segue** quella del basso (correlazione +0,058, cioè niente). Non infittire la
batteria dove si infittisce il basso: il corpus lo nega.

---

## Il tocco, che non si scrive a mano

Il **groove template** (`GR.profilo()` + `MU.applica_groove()`) prende un
batterista nominato e ne estrae, passo per passo, di quanto un colpo anticipa
o ritarda e con che forza cade. Si applica al pattern **dopo** averlo scritto.

⚠️ E conferma il libro: sul template del blues i quarti del ride stanno a
velocity 127 e le crome swingate a 70. Riley, p. 8: *«assicurati che le quattro
semiminime siano suonate allo stesso volume e che la nota di skip **non** sia
accentata»*.

---

## Come si scrive, materialmente

```python
from delugexml import musica as MU, groove as GR

# un pattern e' una stringa di 16 passi: 'x' colpisce, '.' tace
note = MU.passi('x...x.x.x...x.x.', da=0)      # il giggidi', battuta 1
rapporto = MU.applica_groove(note, profilo, dove='ride')
```

`MU.passi()` mette i colpi sulla griglia a sedicesimi;
`MU.applica_groove()` ci posa sopra il tocco del batterista vero.

---

## Cosa NON fare

Ognuna di queste è stata provata e respinta all'ascolto, fra il 30 agosto e il
10 settembre 2026. Stanno nella casella 11 di `docs/repertori/jazz.md`.

- **non sorteggiare ogni passo per conto suo.** Sei voci indipendenti fanno
  una binomiale larga, e all'orecchio è «una batteria a grappoli di eventi
  discontinui»;
- **non spalmare un budget di attacchi su tutte le voci.** Il ride ne vuole
  sei per sé;
- ⚠️ **non far tacere le voci per intere battute.** È il difetto della
  versione 13: il ride diventa un orologio e il resto entra ogni tanto. Nelle
  battute vere tutte e quattro le voci suonano il loro strato, e a cambiare è
  solo quanto ci mettono sopra;
- **non far cambiare il ride battuta per battuta.** È il metronomo: se si
  buca, non tiene niente;
- ⚠️ **non prendere un esercizio per una descrizione.** I libri didattici
  isolano una cosa alla volta: «non suonare i quarti con la cassa» e «quattro
  battute di silenzio» sono esercizi, e presi alla lettera hanno prodotto due
  versioni respinte;
- **non copiare un pattern intero dal corpus.** Il più frequente del ride
  copre il 15% delle battute: ripeterlo dà una batteria a stampo, che è il
  difetto sentito il 30 agosto.

---

## Cosa manca a questa istruzione

- **il vocabolario delle figure di comping.** Riley ne dà quattro serie
  (Comp Example 1-4, pp. 18-29) in notazione, e la notazione non è ancora
  stata letta;
- **il fill.** Dove va, quanto dura, cosa cambia. Nel generatore oggi è una
  decisione arbitraria messa sul turnaround;
- **le spazzole**, e i feel diversi dallo swing (`More Jazz Essentials`,
  pp. 55-61);
- **la risposta in tempo reale**, che su un pezzo scritto non esiste per
  definizione.
