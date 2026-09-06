# Spendere le misure della casella 5 sul generatore — progetto

**Data:** 6 settembre 2026
**Perché adesso:** il 1 settembre la casella 5 di `docs/repertori/jazz.md` è
stata chiusa con cinque misure sul Jazz Trio Database, e §6-noviesdecies
dell'handoff ha nominato il passo successivo in una riga: *«spendere queste
misure sul generatore»*. Finora sono numeri che descrivono un corpus. Questo
progetto li fa diventare note in un file, e poi li fa ascoltare — perché
**finché un pezzo non è stato ascoltato, di queste misure si sa che sono
giuste, non che servono**.

## Il difetto che apre il lavoro, e non è nuovo

Il basso del generatore fa **4,00 note per battuta con deviazione 0,00** su
228 battute: quattro posizioni, una durata, mai un'eccezione. Il corpus dice
che **il 59,7% delle battute di un walking vero non ha quattro note** e che la
deviazione dentro la singola esecuzione è **1,03**.

Non è «meno vario»: è **fuori dalla distribuzione**, perché il valore centrale
del corpus copre solo il 40% delle battute.

E la batteria, resa varia il 30 agosto campionando le frequenze del profilo,
varia **contro uno sfondo fermo**: non sa niente di cosa fa il basso. La frase
dell'utente che ha aperto tutto il filone — *«le interruzioni, accenti e
struttura delle parti di batteria sono strettamente correlati alla sezione
ritmica, e non le puoi applicare acriticamente»* — è stata misurata e ha
ragione, ma **non nella densità** (+0,058, cioè niente): nella **coincidenza
degli eventi fuori griglia**, dove il basso e la batteria cadono insieme
**1,52 volte** più del caso a 20 ms.

## Le misure che si spendono, e quella che non si può

| misura | valore | si spende? |
|---|---|---|
| distribuzione delle note per battuta del basso | 0,7 / 6,1 / 16,2 / **40,3** / 22,9 / 8,8 / 4,9% | sì, ma **non questa**: vedi «una seconda uscita dalla stessa passata» |
| deviazione dentro l'esecuzione | 1,03 | sì, ed è il bersaglio vero |
| beat su cui il basso non attacca | 15,0%, ripartito 16,0 / 18,5 / 15,0 / 17,4% | sì |
| coincidenza basso-batteria fuori griglia a 20 ms | 30,6% contro 20,1% attesi = **1,52×** | sì |
| correlazione di densità basso↔batteria | +0,058 | **no**: è nulla, e generare una batteria «che si infittisce dove si infittisce il basso» sarebbe inventare una regola che il corpus nega |
| scarto relativo basso/batteria | +2,3 / −0,4 ms | **non si può**: 0,55 tick a 128 BPM, sotto la risoluzione |
| scarto relativo del piano | +15,3 ms = 3,1 tick | scrivibile, ma è una **terza** modifica e romperebbe l'attribuzione: resta per il giro dopo |

## La misura nuova, e il criterio fissato prima di guardare

La casella 5 conta **quanti** onset ci sono per battuta, non **dove** cadono
quelli in più. Il dato per saperlo c'è già: `jtd.griglia()` dà i beat e
`jtd.onsets()` gli onset grezzi, quindi la **fase** di ognuno dei 170 394
onset di basso fuori dai beat — `(t − beat_k) / (beat_{k+1} − beat_k)` — si
calcola con quello che è in casa.

Funzione nuova in `tools/misura_spartizione.py`, accanto alle cinque che ci
sono, e come loro **due volte**: su tutto il corpus e su JTD-300, con la regola
di sempre — se divergono vince JTD-300.

### E una seconda uscita dalla stessa passata, che serve più della prima

⚠️ **La distribuzione che la casella 5 pubblica non è quella da cui il
generatore deve pescare, e usarla sarebbe uno sbaglio.** Quella tabella mette
insieme 1099 esecuzioni: la sua dispersione vale **1,33** perché contiene sia
quanto varia un bassista dentro un pezzo (**1,03**, che la casella dà a parte)
sia quanto i bassisti differiscono fra loro (**0,84** di scarto fra le medie
delle esecuzioni). Un pezzo generato è **una** esecuzione, non 1099: pescare
dalla distribuzione aggregata gli darebbe il 29% di variabilità in più di
quella di un bassista vero.

La stessa passata produce quindi anche una seconda distribuzione, definita
così: **le note per battuta delle sole esecuzioni la cui media sta entro ±0,2
da 4,27**. Sono bassisti che in media fanno quello che fa il pezzo generato, e
la loro distribuzione messa insieme è quella di *una* esecuzione tipica, non
della somma di 1099. È discreta, fatta di interi, e non richiede nessun
ricentramento: è da lei che il generatore pesca.

**Il controllo, fissato adesso:** la sua dispersione deve stare entro ±0,10 da
**1,03**. Se ci sta, è la distribuzione giusta e si usa. Se non ci sta, si usa
lo stesso ma il numero va scritto accanto, perché vorrebbe dire che la
dispersione dentro un'esecuzione dipende da quanto quel bassista suona denso —
che è un risultato, non un intoppo.

**Il criterio, fissato adesso e prima di misurare:**

| esito | lettura | grado |
|---|---|---|
| picco entro ±0,04 da **0,66** | la nota in più è una **croma swingata** | `[MIS]` |
| picco entro ±0,04 da **0,50** | è una **croma dritta** | `[MIS]` |
| nessun intervallo oltre il doppio della media | distribuzione **piatta**: nessuna posizione preferita, il generatore usa la croma swingata dichiarandola | `[WEB]` |

⚠️ **Un controllo incrociato che non costa niente:** il picco dovrebbe cadere
sul rapporto di swing che la **casella 4** ha misurato per conto suo, su un
altro corpus e con un altro metodo. Se coincidono, due misure indipendenti si
confermano. Se no, è un risultato da scrivere, non da aggirare.

⚠️ **E ha una conseguenza tecnica:** il pezzo ha `set_swing(figura='1/8')`,
quindi una nota scritta sulla croma la sposta il firmware. Se il picco cade
sul rapporto di swing, scrivere la croma dritta è già giusto. Se cade a 0,50,
la croma va scritta al tick che **dopo** lo swing atterra lì, e lo strumento
per invertire la mappa esiste: `GR._senza_swing()`.

## Il basso

### La lacuna di libreria, che va chiusa prima

`walking()` ritorna una lista piatta di altezze e il chiamante la passa a
`MU.melodia(durata='1/4')`, che mette **una nota per passo fisso, tutte della
stessa lunghezza**. Un basso che tiene una nota per due movimenti e ne infila
una in più su una croma **non ci sta dentro**.

`MU.linea(eventi)` — da `(tick, altezza, durata)` alle note raggruppate per
riga. È il caso generale di cui `melodia()` è la scorciatoia a passo fisso, sta
in `musica.py` accanto a lei, e le due restano indipendenti: `melodia()` non
cambia e nessun chiamante esistente si tocca.

### Le due operazioni sopra la costruzione che c'è

La costruzione del walking resta **identica** — fondamentale, due gradi
dell'accordo, approccio cromatico sul quarto movimento. Sopra ci va un
procedimento in quattro passi, per ogni battuta:

1. **si pesca quante note** dalla distribuzione dentro l'esecuzione, più la
   media 4,27, arrotondato e non negativo;
2. **se sono meno di quattro**, si tolgono attacchi: quali movimenti, lo
   decide un sorteggio pesato con le quote misurate — 16,0 / 18,5 / 15,0 /
   17,4% — così i buchi restano più frequenti sul 2 e sul 4 come nel corpus.
   La nota precedente si allunga fino a coprire il movimento saltato; una
   battuta da zero note è la nota di prima che tiene per tutta la battuta;
3. **se sono più di quattro**, si aggiungono crome alla posizione che dice la
   misura qui sopra, di altezza **approccio cromatico alla nota che viene**;
4. le note restanti sono quelle che `walking()` costruisce già oggi, intatte.

⚠️ **Su quale movimento cada la nota in più è una decisione, non una misura.**
Il corpus lo direbbe — la stessa passata che calcola la fase sa anche in quale
movimento ogni onset fuori griglia cade — ma questa misura è stata
deliberatamente lasciata fuori per non allargare il lavoro. Il generatore
sceglie il movimento a caso fra quelli che hanno attaccato, uniforme, e lo
dichiara: se l'ascolto dice che le note in più cadono nel posto sbagliato, il
dato è a una passata di distanza.

Il bersaglio, verificato dai numeri che il generatore stampa: distribuzione
come quella del corpus e deviazione dentro il pezzo **vicino a 1,03** invece
di 0,00.

⚠️ **Seme separato, `SEME_BASSO`**, per la stessa ragione per cui
`SEME_BATTERIA` esiste dal 30 agosto: cambiare il basso non deve muovere
l'assolo, e viceversa.

### Perché l'approccio cromatico, e perché è una decisione e non una misura

**JTD non porta altezze.** Qualunque cosa suoni la nota in più è una decisione
di chi scrive il generatore, e va dichiarata come tale accanto al codice.
Scelto l'approccio cromatico perché **non introduce nessun principio nuovo**:
è lo stesso idioma che il file usa già sul quarto movimento di ogni battuta,
applicato un livello più in giù. La linea resta condotta invece di diventare
arpeggiata, e la nota in più tira verso quella dopo invece di stare ferma.

### Perché la nota tenuta e non il silenzio

**JTD ha onset, non note-off.** «Nessun attacco su quel beat» non è «silenzio»:
la nota precedente può essere ancora suonata, e il corpus **non può
distinguere le due cose**. La casella 5 scrive «il basso tace» ed è la lettura
che il dato consente, non un fatto osservato.

Scelta la nota tenuta: è quello che fa un contrabbassista quando salta un
movimento — la corda continua a suonare — e un buco vero su un movimento su
sei rischia di suonare come una linea rotta invece che come un walking. La
decisione sta dichiarata accanto alla regola.

## La batteria

`batteria()` riceve i passi su cui il basso ha una nota fuori griglia. Su quei
passi la probabilità del profilo di **ogni** voce viene moltiplicata per
**1,52**, con tetto a 1. Altrove, invariata.

**Tutte le voci e non solo cassa e rullante**, benché «il ride tiene il tempo e
non insegue il basso» sia musicalmente difendibile: gli onset di batteria del
JTD sono **aggregati**, e nessuna affermazione su quale pezzo del kit sia
ricavabile da lì. Distinguere fra voci sarebbe una regola `[IPO]` messa sopra
una misura. Il moltiplicatore non inventa colpi: alza la frequenza di quelli
che quel batterista suona davvero su quel passo.

### Un secondo sorteggio invece di uno modificato, ed è il punto che tiene in piedi il metodo

⚠️ `_voce_dal_profilo()` consuma un `random.Random` **sequenziale**: qualunque
cosa cambi il numero o l'ordine delle estrazioni sposta **tutti** i sorteggi
successivi, e la batteria uscirebbe diversa dappertutto invece che solo dove
c'è l'aggancio. **Il verdetto non sarebbe più attribuibile.** Vale sia per
alzare una probabilità dentro quel ciclo, sia — ed è l'errore che questa spec
conteneva fino alla revisione — per sostituire il sorteggio sequenziale con
uno per cella: anche uno schema per cella *equivalente in distribuzione*
produce colpi diversi, e la batteria della 08 non sarebbe più quella della 07.

Quindi **il sorteggio di base non si tocca**, e l'aggancio è un **secondo
sorteggio indipendente**, con seme proprio `SEME_AGGANCIO` e stato per cella,
che gira solo dove il basso ha una nota fuori griglia e la prima estrazione
non ha messo il colpo. Perché la probabilità complessiva risulti 1,52 volte
quella del profilo:

    p_extra = min(1, 0,52 × p / (1 − p))      con p = colpi / battute

così `p + (1 − p) × p_extra = 1,52 p`, con tetto a 1 quando `p ≥ 0,658`.

Ne discendono tre proprietà, e sono tutte verificabili:

1. la batteria della **08 è identica a quella della 07**, byte per byte — il
   flusso sequenziale non è stato toccato;
2. la **09 differisce dalla 08 solo per colpi in più**, mai in meno, e solo
   sui passi dove il basso ha un evento fuori griglia;
3. l'aggancio non inventa passi: il secondo sorteggio gira solo sui passi che
   il profilo di quel batterista già contiene, con la soglia `minimo` di
   `_voce_dal_profilo()` rispettata.

### L'aggancio è un passo condiviso, non una coincidenza garantita

Lo scarto che il groove template scrive arriva a ±11 tick (±54 ms) e a 128 BPM
la finestra di 20 ms sono **4 tick**. Mettere il colpo sullo stesso passo del
basso **non garantisce** che i due eventi cadano dentro i 20 ms. Quanto ci
cadano davvero lo dice il numero che il generatore stampa, non questo
progetto.

## I due pezzi

`VERSIONE = 8` di base; il flag `--aggancio` scrive la **09**.

    .venv/Scripts/python.exe tools/genera_jazz.py blues
    .venv/Scripts/python.exe tools/genera_jazz.py blues --aggancio

| | cosa cambia rispetto alla precedente |
|---|---|
| 07 → **08** | il basso: distribuzione, beat non attaccati, note in più. **La batteria non cambia**, ed è verificabile |
| 08 → **09** | la batteria si aggancia agli eventi fuori griglia del basso. **Il basso non cambia** |

Una cosa sola per versione, come le sei versioni precedenti. I tre pezzi
(blues, rhythm changes, modale) escono tutti perché `walking()` e `batteria()`
sono condivise; il verdetto si chiede sul **blues**, che ha sette versioni di
storia alle spalle.

## I numeri che il generatore stampa

Accanto ai rapporti che già stampa, misurati sul pezzo appena scritto e
affiancati a quelli del corpus:

- note per battuta: distribuzione e deviazione;
- quota di movimenti non attaccati, e su quale movimento;
- coincidenza basso-batteria a 20 / 30 / 50 ms, col riferimento casuale
  calcolato come lo calcola `misura_spartizione.py`.

Nella stessa forma in cui la casella 5 dà i numeri del corpus, in due colonne,
così il confronto si legge senza rifarlo.

## Il grado di prova di ogni pezzo

| cosa | grado |
|---|---|
| quante note per battuta, dove cadono i silenzi, la coincidenza 1,52× | `[MIS]` |
| dove cade la nota in più (fase) | `[MIS]`, oppure `[WEB]` se la distribuzione esce piatta |
| **che altezza** ha la nota in più | decisione: JTD non porta altezze |
| **nota tenuta** invece che silenzio | decisione: JTD ha onset, non note-off |
| **quale voce** del kit si aggancia | decisione: gli onset di batteria sono aggregati |
| la probabilità ×1,52 come modello | decisione: il corpus dà il rapporto, non il meccanismo |
| il verdetto dell'ascolto | `[OSS]`: un ascoltatore, nessuna prova alla cieca |

## Test, e la pulizia mirata

TDD, un test che fallisce prima di ogni pezzo:

- la misura della fase, che **salta** se il corpus non c'è (come i test del
  1 settembre);
- `walking()`: la distribuzione su molte battute dentro una tolleranza
  dichiarata, la deviazione vicino a 1,03, i silenzi più frequenti sul 2 e sul
  4, la nota tenuta lunga il doppio, la nota in più cromatica alla successiva;
- `MU.linea()`: le note raggruppate per altezza, le durate rispettate,
  `melodia()` invariata;
- `batteria()`: senza eventi fuori griglia il risultato è **identico** a
  quello di oggi (il flusso sequenziale non si è mosso), con eventi i colpi
  possono solo aumentare, mai diminuire, e solo sui passi del basso; il tetto
  a 1 quando `p ≥ 0,658`; e `p_extra` che porta la probabilità complessiva a
  1,52 p.

**Pulizia, nel codice che si riscrive:** via `RIDE`, `PEDALE`, `CASSE`,
`CASSA_PER_BATTUTA`, `RULLANTI` e `RULLANTE_PER_BATTUTA` (righe 915-950 di
`tools/genera_jazz.py`), definiti e **mai usati** dalla versione 07, quando il
disegno della batteria è passato al profilo.

## Cosa resta fuori, e va detto

- **la correlazione di densità**: misurata nulla, non si implementa;
- **lo scarto relativo del piano**: scrivibile ma rimandato, per non rompere
  l'attribuzione;
- **quale pezzo del kit risponde al basso**: il corpus non lo può dire, e
  resta il limite che pesa di più;
- **le altezze del basso del corpus**: JTD non le porta, le avrebbe FiloBass
  la cui licenza è ristretta;
- **la dinamica dell'insieme**: gli onset non portano intensità.

## Dove si scrive quando il lavoro chiude

| file | cosa |
|---|---|
| `docs/repertori/jazz.md`, casella 5 | la misura della fase |
| `docs/repertori/jazz.md`, casella 11 | cosa hanno cambiato la 08 e la 09, e il verdetto |
| `HANDOFF.md` | la sezione nuova, e «il prossimo passo» aggiornato |
| `docs/superpowers/plans/` | il piano di esecuzione |

## Come si sa che è finito

1. i test passano, compresi quelli nuovi;
2. la batteria della 08 è **identica** a quella della 07 — la guardia
   dell'attribuzione;
3. i numeri stampati dal generatore stanno dentro la distribuzione del corpus;
4. `MU.verifica()` è vuota e i pezzi si caricano sul dispositivo;
5. **l'utente li ha ascoltati e ha detto cosa sente.** Senza questo il lavoro
   non è finito: è solo giusto.
