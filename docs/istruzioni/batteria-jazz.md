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

## I quattro ruoli, e non sono intercambiabili

`[LIB]` John Riley, *The Art of Bop Drumming*, pp. 8 e 24.

| voce | cosa fa | cosa NON fa |
|---|---|---|
| **ride** | tiene il tempo: quattro quarti di **uguale intensità**, più la nota di *skip* sui movimenti 2 e 4, suonata **più piano** | non segue mai il comping. Riley: «tieni il ride fermo, perché vorrà andare dietro alla cassa» |
| **charleston a pedale** | sui movimenti **2 e 4**, e basta | non commenta |
| **rullante** | è la voce **principale** del comping | non tiene il tempo |
| **cassa** | **bombe**: accenti isolati, e la stessa figura di due battute del rullante — «come una terza mano» | ⚠️ **non suona i quarti.** Riley lo dice in chiaro: *«non suonare le semiminime con la cassa»* |

Il ride e il charleston tengono. Il rullante e la cassa parlano. **Sono due
mestieri diversi che succedono insieme**, ed è la cosa che una batteria
generata sbaglia per prima.

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

## La frase: due battute, ripetute, poi si tace

`[LIB]` p. 20, il capitolo «Pacing». È la cosa più importante di questa
istruzione.

> «Un buon modo per imparare ad accompagnare musicalmente è suonare ogni frase
> di **due battute due volte**, e poi suonare **quattro battute di solo tempo,
> senza comping**. Questo esercizio ti mostra un tipo di *ritmo* o *densità*
> fra l'accompagnare e il tenere il tempo. Ricorda che le tue idee di comping
> devono **accompagnare** e **completare** quello che suonano gli altri.»

Quando un'idea si ripete così, si chiama **riff**.

Quindi l'unità dell'accompagnamento **non è la battuta**: è la frase di due
battute. E fra una frase e l'altra la batteria **tace**, cioè tiene solo il
tempo col ride e il charleston.

⚠️ **Questa è la ragione per cui una batteria generata battuta per battuta non
avrà mai senso**, per quanto giuste siano le sue statistiche: non ripete mai e
non si ferma mai.

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
la forma la conosciamo: **si decide l'arco in anticipo**, giro per giro, e la
densità del comping lo segue.

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
- **non far suonare tutte le voci in tutte le battute.** Senza silenzio non
  c'è frase;
- **non far cambiare il ride battuta per battuta.** È il metronomo: se si
  buca, non tiene niente;
- **non far suonare i quarti alla cassa;**
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
