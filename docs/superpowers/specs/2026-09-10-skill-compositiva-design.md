# La skill compositiva — progetto

**Data:** 10 settembre 2026
**Cos'è:** la ripartenza del livello musicale di Deluge Pal, dopo che tre
versioni di seguito sono state respinte all'ascolto. Non è un aggiustamento:
cambia da cosa vengono le note.

## Perché si riparte

Il livello musicale generava note così: misurava una frequenza su un corpus,
poi tirava i dadi con quella frequenza. Esempio vero, dalla versione 11: «questo
batterista colpisce il passo 8 nell'80% delle battute» → in ogni battuta tira
un dado, sotto 0,80 mette il colpo. Stessa cosa per il basso, per il solo, per
tutto.

Il proprietario del progetto, il 10 settembre:

> «hai creato un generatore random con parametri presi da analisi statistiche
> di un corpus enorme. come potrebbe mai produrre risultati accettabili?
> questo non è assolutamente quello che volevo. io immaginavo una skill
> compositiva più approfondita, con istruzioni teoriche armoniche e ritmiche e
> "groove template", il tutto basato su una analisi del corpus.»

Ha ragione, e la ragione si dice in una riga: **una distribuzione descrive com'è
fatto un insieme di dischi, non come si scrive una battuta.** Tirare i dadi con
la forma giusta produce rumore con la forma giusta.

### I tre verdetti, in fila

| data | versione | cosa cambiava | verdetto |
|---|---|---|---|
| 30 agosto | 06 → 07 | la batteria esce dal profilo invece che da una tabella | «la batteria suona discontinua rispetto a basso e piano» |
| 6 settembre | 08, 10 | il basso varia; la batteria prende la densità misurata | «il basso ha un po' troppe variazioni, ma non è malissimo. la batteria resta discontinua» |
| 10 settembre | 11 | il ride tiene il tempo | «ora sento il giggidì ma le altre parti di batteria non hanno molto senso» |

Tre giri, tre volte lo stesso difetto: le statistiche erano giuste e la musica
no.

⚠️ **E la regola che lo avrebbe evitato era già scritta, dal 30 agosto 2026:**
*«il corpus dà RELAZIONI, non superfici — vogliamo un tool per AI per creare
musica ORIGINALE, non repliche dei pattern studiati»*. È stata violata per tre
settimane di fila senza che nessuno se ne accorgesse. Sta in
`docs/MUSICA.md` e in HANDOFF §6-octodecies.

### Cosa manca, e nessuna misura lo dà

Il **mestiere**. Quando far respirare una frase. Come si risponde a una
domanda. Cosa cambia all'ultimo giro. Cosa fa la batteria nella battuta prima
di un cambio di sezione.

Il corpus è stato interrogato solo sulle superfici — *quanto spesso succede X*
— e il mestiere non sta lì.

## Cos'è la skill

Quattro cose, e vanno insieme.

### 1. Istruzioni

Scritte all'imperativo e organizzate per compito, non per argomento: *come si
scrive un walking*, *come si accompagna*, *come si costruisce una frase*, *cosa
cambia all'ultimo giro*.

La differenza con quello che c'è oggi, sullo stesso fatto:

> **Com'è adesso** (casella 5 di `docs/repertori/jazz.md`):
> «Il basso non attacca sul 15,0% dei beat, più spesso sul 2 e sul 4.»
>
> **Come dev'essere:**
> «Il walking respira lasciando cadere un movimento: tieni la nota precedente
> invece di attaccare. Falla sul 2 o sul 4, non sull'1. Serve a togliere peso
> prima di un cambio d'accordo. Nei dischi succede circa una volta ogni sei
> movimenti; molto più spesso e la linea si sfilaccia.»

Stesso numero. La seconda si può eseguire, la prima no.

### 2. Numeri

I vincoli misurati, attaccati all'istruzione che riguardano. **Non come motore:
come limiti.** Servono a dire quando una scelta esce dal seminato, non a
prendere la scelta.

Quelli che ci sono già, e che sul web non si trovano: lo swing per stile e per
tempo (BUR 1,89 fra 120 e 180 BPM, 1,35 sopra i 240); dove culminano le corse
dei solisti (sul ii-V); che un motivo sotto le cinque note è indistinguibile
dal caso; quanto varia un walking vero.

### 3. Groove template

Il tocco dei batteristi veri: da un'esecuzione nominata si estrae, passo per
passo, di quanto un colpo anticipa o ritarda e con che forza cade. Si applica a
**qualunque pattern scritto**.

⚠️ Non sono note, è il tocco. Ed è già fatto e già misurato: `groove.py` e
`MU.applica_groove()`. Non era lui il problema — l'errore è stato dargli in
pasto pattern tirati a dadi.

### 4. Primitive

Il codice che esegue una decisione senza sbagliare i conti. **Calcola, non
pesca.** Nessuna nota di un disco è mai finita in un pezzo generato, e il
progetto l'ha verificato esplicitamente (HANDOFF §6-quindecies).

| primitiva | decide l'AI | calcola il codice |
|---|---|---|
| `armonia()` | quali accordi, che registro, che voicing | quali note, con la condotta delle parti |
| `linea()` | quali altezze, dove, quanto lunghe | le posizioni esatte in tick |
| `trasponi()` | «più in alto di una terza, restando in tonalità» | quali note diventano quali |
| `applica_groove()` | quali colpi | di quanto anticipano o ritardano, e quanto forte |
| `verifica()` | — | se il file si carica sul dispositivo |

La prova che questa divisione funziona c'è già, ed è del 29 agosto 2026: il
comping è passato da una tabella di altezze scritta a mano a `MU.armonia()`,
che calcola la condotta cercando il minimo movimento. Verdetto: *«ora il
voicing è meglio di prima. Va bene»*. L'AI ha scelto **quali accordi**, il
codice ha deciso **quali note** — ed è andata meglio di quando le note le
aveva scritte una persona.

## Le tre decisioni prese il 10 settembre 2026

### 1. L'unità di lavoro: una parte per volta, poi il resto

In quest'ordine, e il primo è quello su cui si costruisce tutto:

1. **una parte sopra materiale dato** — «scrivi un walking sotto questo giro»,
   «metti una batteria dietro questo tema». Si ascolta subito, si corregge
   subito, e il corpus sa già rispondere a domande di questa forma;
2. **un pezzo intero** — più parti coordinate. Richiede in più la forma,
   l'arco e l'interazione fra le parti, che oggi mancano;
3. **una risposta a una domanda** — «perché questo ponte è debole?». È
   spiegare la regola che si userebbe.

⚠️ Il progetto finora ha fatto il **secondo** senza che nessuno l'avesse
deciso, saltando il primo.

### 2. Le note le decide l'AI, le primitive eseguono

La skill è fatta di istruzioni musicali. L'AI decide ogni nota in senso
musicale — quale accordo, quale gesto, dove respira la frase — e chiama le
primitive per non sbagliare i conti.

Scartate: che l'AI scriva tutte le note da sola (i modelli sbagliano a contare
i movimenti su decine di battute) e che il codice generi da regole con l'AI a
scegliere i parametri (è la strada che ha già fallito tre volte: l'AI non
compone, riempie un modulo).

### 3. Il mestiere viene dalla letteratura, verificato dove ha senso

La letteratura didattica dà il **quando e come**. Il corpus dà i numeri e
prende gli errori.

Il materiale c'è in casa, in `to-read/`: l'*Armonia* di **Walter Piston** in 34
capitoli, un **Jazz Theory**, e altro. ⚠️ `to-read/` non è versionato: chi
riprende questo progetto senza quei file non può rifare il lavoro.

⚠️ **Il rischio, dichiarato:** la letteratura è la fonte di cui questo progetto
ha imparato a diffidare — tre volte su tre, verificandola, diceva cose che i
dischi non confermano. E **molte istruzioni di mestiere non sono
verificabili**: «rispondi alla frase del solista» non si misura. Quelle
restano con l'etichetta della loro fonte, e chi legge sa quanto fidarsi.

Il sistema di gradi che il progetto usa già per i fatti — `[MIS]`, `[WEB]`,
`[OSS]`, `[IPO]`, `[MAN]` — si estende alle istruzioni.

## Cosa si salva del lavoro fatto

| | righe | destino |
|---|---|---|
| interfaccia Deluge (leggere, scrivere, USB) | 6 236 | **si tiene intera.** Non c'entra con questo discorso: sono le mani |
| `musica.py`, le primitive | 1 999 | **si tiene**, e probabilmente si allarga |
| groove template (`groove.py`) | 786 | **si tiene**: è la cosa che il proprietario aveva nominato |
| lettori di corpus (`jtd.py`, `wjazz.py`, `midi.py`) | ~1 200 | **si tengono**: servono a verificare le istruzioni |
| documentazione misurata (`MUSICA.md`, schede) | ~4 500 | **i fatti si tengono, la forma si riscrive** da referto a istruzioni |
| le 41 tabelle di `genera_jazz.py` | — | **si tengono**: giri armonici, forme AABA, ritmi di comping, sagome di walking sono vocabolario compositivo, scritto da teoria e non campionato |
| il generatore a dadi (15 punti di sorteggio) | ~300 | **si butta** |

Con lui se ne vanno `DISTRIBUZIONE_BASSO`, `DISTRIBUZIONE_BATTERIA` e
`QUOTE_SILENZIO` **come pesi di sorteggio**. Restano come fatti nella
documentazione.

## Da dove si comincia

**Il walking**, una parte sola, un repertorio solo.

1. si leggono i capitoli che servono di Piston e del Jazz Theory;
2. si scrivono le istruzioni per costruire una linea di walking, all'imperativo,
   ognuna con la sua fonte;
3. si attaccano i vincoli già misurati dove riguardano;
4. l'AI scrive una linea seguendo quelle istruzioni, con le primitive;
5. **si ascolta.**

Se la forma funziona su una parte, si replica sulle altre. Se non funziona, lo
si sa dopo una parte e non dopo tre settimane.

## Cosa NON è stato deciso

- **se la skill sia universale o legata al Deluge.** Oggi le primitive
  scrivono file del Deluge. Renderla universale vuol dire farle scrivere anche
  MIDI. La proposta è: costruirla sul Deluge, dove si ascolta subito, e
  astrarla se funziona;
- **quali repertori**, oltre al jazz che è il più misurato;
- **come si sa che funziona**, oltre all'ascolto di una persona sola. È il
  punto debole di tutto il progetto: il ciclo è lento e non scala.

## Cosa NON rifare

- **non trasformare una distribuzione in un motore.** Un numero misurato dice
  quando una scelta esce dal seminato, non quale scelta prendere;
- **non chiedere al corpus solo «quanto spesso».** La regola del 30 agosto
  chiede relazioni: cosa segue cosa, cosa risponde a cosa;
- **non confrontare due corpora come se contassero la stessa cosa.** È
  successo tre volte in una settimana, e una di quelle ha prodotto una
  versione intera da buttare (la 10);
- **non saltare l'unità di lavoro piccola.** Un pezzo intero nasconde quale
  parte è sbagliata.
