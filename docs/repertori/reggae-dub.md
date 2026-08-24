# Reggae e dub

> Una scheda dello schema neutro. Lo schema, il materiale comune a tutti i
> repertori e l'indice stanno in [`../MUSICA.md`](../MUSICA.md).

Da leggere prima del resto, e da datare: la cautela qui sotto è del 16
agosto 2026, cioè **prima** di `DUBPAL02` e `DUBPAL03`. Da allora l'ascolto
dell'utente ha corretto la grana fine (casella 11) e ha detto cosa resta
(casella 9).

> Tutto quanto segue viene da ricerca web ([WEB], fonti in fondo alla
> scheda). Non è ancora stato validato dall'ascolto dell'utente: `DUBPAL01`,
> scritto **prima** di questa ricerca, è stato giudicato «molto elementare e
> per niente somigliante a un pezzo dub».

## 1. Cos'è, e cosa non è

**Parziale.** C'è il dub come *pratica*, e c'è la confusione fra skank e
charleston — l'errore che il progetto ha già commesso. Manca il confine col
vicino più insidioso: **rocksteady, ska, dancehall**, che condividono il levare
e cambiano tempo, accento e ruolo del basso. Nessuna delle fonti in fondo lo
copre, quindi oggi «reggae» qui vuol dire *roots* e basta, e un vicino si
scambia senza accorgersene. La chiuderebbe una ricerca sui **confini** fra i
quattro: non le etichette, ma cosa si sente di diverso.

*Nel frattempo, per comporre:* si scrive **roots**, e lo si dichiara — è
l'unica cosa che questa scheda descrive, e restare dentro il suo perimetro è
una risposta, sconfinarci senza saperlo no. Se la richiesta nomina ska,
rocksteady o dancehall, la domanda va **all'utente** prima di scrivere: qui le
skill non sono un ripiego, e la casella 11 dice perché.

### Il dub come *pratica*, non come stile

Il dub nasce al banco del mixer: si parte da un riddim già suonato e lo si
**smonta in tempo reale**.

- **si compone togliendo.** La struttura è "parti che entrano ed escono", non
  "sezioni che si sviluppano". Un vuoto di quattro battute con sole batteria
  ed eco vale più di un ritornello.

### Lo skank non è il charleston

**Il punto che avevo sbagliato in `DUBPAL01`:** avevo messo il **charleston**
sui levare e non avevo affatto lo **skank**. È l'opposto. Il charleston fa una
*timeline regolare* — ottavi, o sedicesimi con i levare appena accentati — e
il levare è dello **skank**, che è armonia, non percussione.

## 2. Metro e griglia

Griglia a 16 passi per battuta, come `MU.passi()`:

```
                0 1 2 3 4 5 6 7 8 9 . . . . . .
movimento       1       2       3       4
charleston      . . x . x . x . x . x . x . X .   ottavi, ma l'UNO è vuoto
cassa           . . . . . . . . x . . . . . . .   solo il 3
rullante/rim    . . . . . . . . x . . . . . . .   col la cassa, cross-stick
skank (accordi) . . x . . . x . . . x . . . x .   TUTTI i levare
bubble (organo) . x x . . x x . . x x . . x x .   i sedicesimi attorno al levare
basso           x . . . . . x . x . . . . x . .   frase di 1-2 battute, ripetuta
```

Le sei righe sono le parti. Chi occupa cosa — e cosa lascia libero — è la
casella 5 per batteria e basso; lo skank è armonia e sta nella casella 7, e del
bubble non c'è altro che questa riga e il pattern della casella 6.

## 3. Tempo

Tempo: **50-100 BPM**, con 70-78 al centro del roots. Quindi 70 BPM non è
"lento per il dub", è il posto giusto.

**E cosa dice il corpus** — che è la domanda dei bordi, e ha due risposte
diverse. Il Groove MIDI etichetta `reggae` **venti esecuzioni**: quattro
continue (`beat`), ai tempi di **78, 64, 141 e 126 BPM**, e sedici fill **tutti a 78**
`[OSS]`. Il conteggio per intero, e perché su questo corpus non si misuri, sono
nella **casella 6**.

- **Il centro tiene.** Il 78 della `beat` e il 78 di tutti e sedici i fill
  cadono in mezzo al «70-78» che la riga qui sopra afferma senza marcatore, e
  il 64 sta dentro il range. È **corroborazione, non misura**: tutte le
  esecuzioni in fascia sono di `drummer1`, e un esecutore non è un repertorio.
- **Il tetto no, e non basta a spostarlo.** Il 141 e il 126 stanno **26-41 BPM
  sopra** i 100 dichiarati. Ma questo dice **cosa il corpus etichetta**, non
  fin dove arriva il reggae: l'etichetta può essere larga, come lo è `jazz`,
  che sotto di sé porta anche `jazz/funk` e `jazz/fusion`. La differenza è che
  lì le sottoetichette **si vedono e si escludono**, mentre qui le due veloci
  portano `reggae` nudo — l'unica sottoetichetta è `reggae/slow`, ed è il 64.
  **Il corpus non offre niente per separarle**, quindi il range di questa
  casella **non si muove** e resta `[WEB]`. Il primo posto dove guardare è la
  ricerca che la **casella 1** già chiede: ska, rocksteady e dancehall
  «condividono il levare e cambiano tempo», e finché quel confine non è
  tracciato non si sa se due esecuzioni veloci etichettate `reggae` siano
  reggae veloce o un vicino.

## 4. Feel

**Parziale.** C'è la direzione — il one drop è swingato e laid-back — e c'è
l'errore già fatto, `set_swing(50)`, cioè dritto. Manca **il numero**: qui non
c'è nessuna misura, solo `[WEB]`. E manca lo strumento per il laid-back:
`MU.laid_back()` non esiste, e `MU.sposta()` trasla e basta — le note che
finiscono oltre la fine della clip restano fuori, e il comune lo spiega in «Ma
swing e laid-back non sono la stessa cosa». La chiuderebbero un corpus di dub
misurato come si è misurato il jazz, e poi l'ascolto.

*Nel frattempo, per comporre:* lo swing si prende dalla **casella sorella**,
la 10, che porta il valore da scrivere — non è misurato, e la 10 lo dice. Ma
lo snippet lì è `set_swing(doc, 57)` **senza `figura=`**, cioè com'era stato
scritto: preso alla lettera il 57 cade sulle semicrome e su questo groove di
crome non muove niente. Si scrive **`figura='1/8'`**, che è la figura che
questa casella nomina due righe più sotto — senza, stasera non si sente
niente e sembra che il valore sia sbagliato. Il laid-back invece si **lascia
fuori**: finché `MU.laid_back()` non esiste,
`MU.sposta()` farebbe uscire dalla clip le note che ritarda, e un one drop
senza laid-back è una mancanza che si sente e si corregge, mentre un colpo
perso a fine battuta si cerca per ore altrove.

Il one drop è **laid-back**: gli ottavi di charleston sono **swingati**, e i
levare arrivano leggermente in ritardo — «leaning into the space rather than
cutting through it». [WEB]

Lo **swing** si fa con lo swing di song. Come funziona la scala — display,
BUR, e soprattutto `swingInterval`, che sceglie **quale figura** viene swingata
— sta nel comune, «Il meccanismo dello swing». Serve saperlo per leggere il
valore, che sta nella casella 10 e fu scritto senza: col default del firmware
lo swing cade sulle semicrome, e su un groove di crome quel 57 non muove
niente.

⚠️ In `DUBPAL01` avevo scritto `set_swing(doc, 50)`, cioè **dritto**. Per un
one drop è sbagliato in partenza.

## 5. Ruoli e spartizione

Il reggae non è definito dall'armonia ma dalla **spartizione ritmica della
battuta fra le parti**. Ogni parte occupa un posto che le altre lasciano
libero.

### La batteria

- **one drop**: cassa e rullante **insieme sul terzo movimento**, e il **primo
  movimento vuoto** — è l'accento dominante unico della battuta, e il nome
  viene proprio dal *lasciar cadere* l'uno. [WEB, concorde su 4 fonti]
- il rullante in roots è quasi sempre un **cross-stick / rimshot**, non un
  colpo pieno.
- **anche il charleston salta l'uno**, non solo la cassa. [WEB]
- **l'apertura di charleston sull'ultimo ottavo della battuta**, che porta
  dentro la battuta successiva, è prassi standard. È il dettaglio che fa
  suonare "vero" un pattern altrimenti corretto.
- **turnaround**: ogni 4 o 8 battute, sull'**ultima**, il rullante devia dal
  pattern con una girata sincopata. Senza, il giro è morto — ed è
  esattamente il difetto di `DUBPAL01`, che ripeteva quattro battute
  identiche.
- fill di charleston in **terzine**, appoggiate indietro, sono un altro
  elemento tipico.

Le varianti, che cambiano il carattere lasciando il rullante sul 3:

| | cassa | passi |
|---|---|---|
| **one drop** | solo il 3 | `........x.......` |
| **rockers** | tutti i movimenti | `x...x...x...x...` |
| **steppers** | tutti gli ottavi | `x.x.x.x.x.x.x.x.` |

### Il basso

È **lo strumento solista**, non l'accompagnamento.

- **una frase di una o due battute, ripetuta ossessivamente.** [WEB] Questo
  era l'errore più grosso di `DUBPAL01`: una linea di quattro battute che si
  *sviluppa* è un'idea da un altro genere.
- **centrata sul terzo movimento**, non semplicemente "che evita l'uno".
- **lo spazio conta quanto le note**: quello che si toglie è materiale
  compositivo.
- per il sapore **dub** in particolare: **note ripetute, e soprattutto la
  quinta SOTTO la tonica**. [WEB] In sol minore è il **re grave** sotto il
  sol.
- segue gli accordi outlinando le note dell'accordo "in orizzontale".
- si taglia tutto **sopra i 1000 Hz**. [WEB]

### Cassa e basso, quale dei quattro rapporti

Nella griglia delle sei parti, nella casella 2, cassa e basso sono descritti in
due righe separate e il rapporto non è mai detto. Guardandolo adesso:

```
cassa           . . . . . . . . x . . . . . . .   solo il 3
basso           x . . . . . x . x . . . . x . .   l'UNO c'e'
```

Il basso **suona l'uno che la batteria lascia vuoto**, e sul 3 va all'unisono
con la cassa. È una scelta legittima e tipica — il basso copre il vuoto del one
drop — ma nel file sembrava un caso.

La regola generale — che il rapporto vada **dichiarato** invece che subìto —
sta nel comune, «Cassa e basso sono una coppia, e va dichiarata». Qui c'è quale
dei quattro rapporti è questo.

### La playability vincola il roots, non il dub

Se il pattern debba restare suonabile da quattro arti non è una regola ma una
**decisione**, e qui le risposte sono due a seconda di cosa si sta facendo: il
roots one drop nasce da una batteria vera e la playability lo vincola; il dub
da banco del mixer, con kit sintetizzato, no — `DUBPAL01` ha un kit costruito
dal synth vuoto, senza nessun batterista implicito. Le due righe per esteso, e
perché dichiararlo invece di subirlo, stanno nel comune, «La playability è una
decisione, non una regola».

## 6. Dinamica

I tre livelli — colpo, accento, fantasma — e le loro escursioni per strumento
stanno nel comune, «Velocity groove»; che le variazioni siano **poche e
scelte**, e non velocity randomizzate, sta nel comune, «Variare è scelto, non
randomizzato». Qui c'è dove cadono nel one drop.

### Il velocity groove del one drop

- il colpo sul **3** è l'accento dominante e va nettamente sopra tutto il
  resto — è l'unico evento forte della battuta;
- **charleston mai identici**: gli ottavi dritti e uguali «suonano troppo
  squadrati», e i **levare vanno accentati appena**, non molto; [WEB]
- **fantasmi di rullante** fra un cross-stick e l'altro danno il tessuto;
- l'**apertura di charleston** sull'ultimo ottavo prima della battuta nuova è
  il colpo più forte del charleston.

### I pattern, one drop a 70 BPM

```python
hat  = '..x.o.X.o.x.o.X.'    # ottavi, l'UNO vuoto, levare appena accentati
kick = '........x.......'    # solo il 3
rim  = '..o.....X.....o.'    # il 3 e' l'evento, i fantasmi fanno tessuto
```

Ultima battuta di ogni gruppo di 4 — il **turnaround**, senza il quale il
giro è morto:

```python
rim4 = '..o.....X...x.X.'
hat4 = '..x.o.X.o.x.o.XX'    # doppio colpo che porta dentro la battuta dopo
```

Varianti di cassa che cambiano il carattere lasciando il rullante sul 3:

```python
rockers  = 'x...x...x...x...'
steppers = 'x.x.x.x.x.x.x.x.'
```

E le due parti armoniche, che sono la cosa che mancava del tutto:

```python
skank  = '..x...x...x...x.'   # accordi staccatissimi, TUTTI i levare
bubble = '.oo..oo..oo..oo.'   # organo, i sedicesimi attorno al levare
```

### Perché qui i `[WEB]` NON si possono rimpiazzare con dei `[MIS]`

Questa casella è piena, ma i suoi numeri vengono dal web e l'ascolto
dell'utente li ha già corretti una volta. Una versione precedente di queste
righe si intitolava «qui i `[WEB]` si possono rimpiazzare con dei `[MIS]`»:
con questo corpus **non si può**, e il conteggio vero dice perché.

Il corpus sarebbe il **Groove MIDI**, decompresso in
`to-read/MIDI/groove-v1.0.0-midionly/`, che di reggae porta **20 esecuzioni** —
19 con `style` esattamente `reggae`, una `reggae/slow`. Ma venti è il numero
che non conta. Ricontate il 24 agosto 2026 con `GR.elenco(base,
style='reggae')`, quelle venti si spartiscono così `[OSS]`:

| | quante | chi le suona | quanto dura |
|---|---|---|---|
| `beat` | **4** — a 78, 64, 141 e 126 BPM | `drummer1` 2, `drummer5` 2 | dieci minuti in tutto |
| `fill` | **16**, tutti a 78 BPM | `drummer1` 16 | 2,3-3,1 secondi l'uno, 43 secondi in tutto |

Cioè: **due batteristi**, **due esecuzioni continue ciascuno**, e undici minuti
di musica contando anche i fill. E dei quattro `beat` soltanto **due** — il 78
e il 64 — cadono nella fascia di tempo che la **casella 3** dichiara per questo
repertorio; il 141 e il 126 stanno molto sopra. Dentro il perimetro che questa
scheda descrive il corpus ha quindi **due esecuzioni di un batterista solo**.

Il criterio per fermarsi qui non è nuovo: lo enuncia in una riga la casella 8
di [`jazz.md`](jazz.md) — *un assolo è un musicista, non un repertorio* — e qui
vale moltiplicato, perché gli esecutori sono due e le esecuzioni quattro. Una
tabella di velocity ricavata da lì descriverebbe `drummer1` e `drummer5`, e la
firmerebbe «reggae». **La casella resta quindi `[WEB]`**, e non per pigrizia:
il corpus c'è, è stato aperto, e non regge il peso che gli si voleva mettere
addosso. Quanto ne serva perché regga si vede nella **casella 6 di
[`jazz.md`](jazz.md)**, che la scala di velocity ce l'ha misurata e porta
accanto a ogni riga le esecuzioni e i batteristi che la sostengono — i numeri
stanno lì e non si ricopiano qui.

*Quello che invece si può fare* è l'altra cosa, ed è legittima proprio perché
non si traveste: da una di quelle quattro esecuzioni si costruisce un **groove
template** con `GR.profilo()`, che è `[OSS]` **su quell'esecutore** e non
`[MIS]` sul reggae. Come si posa su un pattern sta nel comune di
[`../MUSICA.md`](../MUSICA.md), «La macchina». Al tempo di questo repertorio le
esecuzioni sono due, e sono le sole due da nominare:
**`drummer1/session1/184`** (78 BPM, 115 s) e **`drummer1/session1/201`**
(`reggae/slow`, 64 BPM, 112 s) `[OSS]`. Le altre due sono di `drummer5` e
stanno a 141 e 126 BPM, cioè fuori dalla casella 3.

⚠️ Due avvertenze che restano valide comunque. Le etichette si contano **per
prefisso**, e non per sottostringa — regola che nasce proprio qui, perché è
`reggae` la parola che dentro altre etichette compare senza essere reggae:
quali siano, e il conto che ne verrebbe, stanno nella casella 6 di
[`jazz.md`](jazz.md), col controesempio. E `to-read/` è in `.gitignore`, quindi
chi clona non trova i file: i conteggi qui sopra sono lo stato del disco di
quel giorno, non una proprietà del progetto.

## 7. Armonia

**Parziale.** C'è il ritmo armonico — pochi accordi, spesso due alternati —
e c'è dove sta il carattere, che è lo skank e non la progressione. Manca tutto
il **vocabolario**: quali sono i due accordi, nessuna progressione tipica,
nessuna sigla, e niente su come si muovono le voci dello skank. Servirebbe una
ricerca sulle progressioni del roots più il voicing di chitarra in levare —
roba che `MU.armonia()` saprebbe già scrivere, e che oggi nessuno le dice.

*Nel frattempo, per comporre:* il **ritmo** dello skank c'è già nelle caselle
sorelle — la griglia della 2 e il pattern della 6 — e quello basta a scriverlo
al posto giusto. Mancano solo le **altezze**, e quelle si chiedono
**all'utente**: la tonalità e i due accordi sono una frase sua, e su questo
repertorio la skill grande non è una fonte (casella 11). Un'armonia scritta
senza chiedergliela va segnata `[IPO]` e portata all'ascolto, non lasciata
passare per acquisita.

**Pochi accordi, spesso solo due alternati.** [WEB] Quello che distingue
l'armonia reggae non è la complessità ma il **ritmo con cui è suonata** — lo
skank. Una progressione ricca suonata dritta non è reggae; due accordi
suonati in levare lo sono.

## 8. Melodia e ornamentazione

**Vuota.** Nel roots la melodia è la linea di basso, che sta nella casella 5
come *ruolo*; qui servirebbe il materiale melodico vero — la voce, i fiati,
il melodica — e nessuna delle fonti lette lo copre. La chiuderebbero le
librerie MIDI per genere già in `to-read/MIDI/`, compresa
`(aq) Dub Beat Builder`, che però nessuno ha ancora aperto.

*Nel frattempo, per comporre:* si **lascia fuori**, e qui l'omissione non è un
ripiego ma la risposta. Nel roots la melodia è la linea di basso, che la
casella 5 ha per intero: un pezzo senza voce, senza fiati e senza melodica è
un pezzo dub, non un pezzo a cui manca qualcosa — «si compone togliendo» è
scritto nella casella 1. Se una linea in cima la si vuole davvero, si apre
`to-read/MIDI/(aq) Dub Beat Builder - Demo` — è quello il nome sul disco — con
`MI.melodia()` invece di inventarla, e quel che se ne ricava è `[OSS]` su una
libreria di loop, non un fatto del repertorio.

## 9. Forma e densità

**Parziale.** C'è l'arco dub a sette tratti, ed è tutto quello che c'è: è
`[WEB/skill]` e **non è misurato su niente**, come dice la riga che lo precede.
La chiuderebbe l'ascolto: un pezzo costruito su quest'arco, e il giudizio
dell'utente su dove è lungo e dove è corto. La scala di densità 1-9 con cui si
sceglierebbero i numeri sta nel comune, «L'arco di densità»; e che dentro il
giro la variazione sia scelta e non randomizzata — un fantasma spostato, un
charleston mancato, non rumore aggiunto ovunque — nel comune, «Variare è
scelto, non randomizzato».

*Nel frattempo, per comporre:* **l'arco qui sotto è il ripiego**, e si usa
com'è, con la fiducia che dichiara da sé — `[WEB/skill]`, misurato su niente.
Il controllo che si può fare stasera senza aprire altro sta nel comune,
«L'arco di densità»: i tempi oltre i quali l'ascoltatore si stacca, contati in
battute al tempo che si sta usando. Chiuderla è un'altra cosa, e la fa solo
l'**utente** dicendo dove il pezzo è lungo e dove è corto.

Le griglie a 16 passi, le velocity, lo swing, il turnaround ogni 4: sono la
grana fine, ed erano giuste da correggere. Ma il giudizio dell'utente su
`DUBPAL03` — *«va meglio, ma musicalmente ci sarebbe ancora moltissimo da
dire»* — arriva **dopo** che la grana fine era stata sistemata. Quello che
resta da dire vive su una scala più lunga, e di quella scala qui non c'era
niente.

⚠️ [WEB/skill] L'arco qui sotto non è misurato su niente: è la forma standard
applicata al dub. Vale come punto di partenza da far correggere all'ascolto,
non come regola — esattamente lo stato in cui erano le griglie a 16 passi
prima del 16 agosto.

Un arco dub di partenza, da provare e correggere all'ascolto:

```
intro       2   batteria ed eco, niente altro
riddim      6   tutte le parti dentro, e' il pieno del pezzo
dub 1       3   via basso e armonia, restano batteria e sirena
riddim      6   rientra tutto, ma con una variante
dub 2       1   SOLO eco. Il vuoto: "and then nothing"
riddim      7   il rientro piu' forte perche' ha qualcosa contro cui spingere
outro       2   si toglie a strati
```

## 10. Sul Deluge

**Parziale.** C'è cosa il dub chiede alla macchina, e manca **come la
macchina lo dà**. Dei tre punti qui sotto due — delay e riverbero come strumenti
compositivi, l'eco sui colpi singoli — sono veri in qualunque studio: sono
estetica, non Deluge. Ed è il terzo a mostrare il buco: **sul Deluge gli FX
stanno sul suono e sulla clip, non sono mandate per nota**, quindi «l'eco
classico si manda su colpi singoli» qui è un **requisito**, non un'istruzione.
Come si ottenga un eco su un colpo solo e non su tutta la parte **non è stato
verificato**: il comune dice che un drum di kit è un `<sound>` completo, e
quindi ha i suoi FX, ma se basti — e cosa costi in righe di kit e in clip — non
lo sa nessuno, perché non è stato provato sul dispositivo. È la prima cosa in
cui inciampa chi costruisce un dub su questa macchina, e questa casella la pone
senza rispondere.

*Nel frattempo, per comporre:* **non c'è un ripiego onesto** — come si ottenga
un eco su un colpo solo e non su tutta la parte è comportamento del
dispositivo, e supporlo qui sarebbe scrivere una risposta che nessuno ha
provato. Si chiede **all'utente**, che il Deluge ce l'ha in mano, prima di
costruire il kit. Quello che si può scrivere senza quella risposta è l'eco
come **decisione di arrangiamento** — i buchi fra le istanze in `arranger.py`,
qui sotto — che da essa non dipende.

Il telaio è comune e non si ripete qui: kit e drum costruiti dal synth vuoto
`TEMPL.XML`, le norme di sound design, il compenso fra risonanza e volume
applicato alla sirena di `DUBPAL02`, il wobble come `lfo1 → lpfFrequency`. Sta
tutto in [`../MUSICA.md`](../MUSICA.md), «La macchina». Del dub è quest'altra
cosa, che sul Deluge è una decisione di arrangiamento e non di suono:

- **delay e riverbero sono strumenti compositivi**, non rifiniture. Il
  *"chick-a"* dello skank raddoppiato è delay, non due colpi suonati.
- l'eco classico si manda su **colpi singoli** — un rullante, una parola, uno
  stab — non su tutta la parte.
- in `arranger.py` questo si scrive con i **buchi fra le istanze**.

E il valore dello swing di song, che è realizzazione sulla macchina e non
feel. Perché il one drop lo voglia — e che qui il numero non è misurato — sta
nella casella 4; qui c'è il numero da scrivere:

```python
S.set_swing(doc, 57)      # unita' del display: sopra 50 = swingato
```

## 11. Trappole del generatore

**16 agosto 2026 — «è molto elementare e non assomiglia per niente a un pezzo
dub», «anche il ritmo di batteria è penoso».** Giudizio su `DUBPAL01`, ed era
un problema di conoscenza, non di strumenti: avevo fatto **una sola** ricerca
web sul dub, tirandone fuori nomenclatura (one drop, rockers, steppers) invece
di mestiere, e avevo invocato `music-composer` **senza leggerne i reference**
— che comunque non hanno reggae né dub. Gli errori concreti, tutti dovuti a
questo:

| errore | cosa era giusto |
|---|---|
| charleston sui levare, **skank assente** | il charleston fa una timeline regolare, il levare è dello skank, che è armonia |
| nessun *bubble* d'organo | riempie i sedicesimi attorno al levare |
| basso di 4 battute che si sviluppa | frase di **1-2 battute ripetuta**, centrata sul 3 |
| 4 battute di batteria identiche | **turnaround** sull'ultima di ogni 4 o 8 |
| velocity a due soli livelli | servono i **fantasmi**, sotto 70 |
| `set_swing(50)`, dritto | il one drop è **swingato e laid-back** |
| pad a note lunghe come parte armonica | in reggae l'armonia è **ritmica**, staccata, in levare |

La lezione di metodo: **una ricerca sola su un genere dà le etichette, non il
mestiere.** Le etichette bastano a scrivere qualcosa di formalmente corretto e
musicalmente morto — che è esattamente cosa è successo.

### Il turnaround corregge un caso su quattro

`DUBPAL01` fu giudicato con «4 battute di batteria identiche», e la
correzione registrata è il **turnaround sull'ultima**. Giusto, e insufficiente:
corregge la battuta 4 e lascia identiche la 1, la 2 e la 3.

### E le due skill, qui, sbagliano

⚠️ **Su reggae e dub comanda questo file, non le skill.** Misurato il 17 agosto
2026: `music-composition` ha **quattro righe in tutto** sul reggae — tre in
`rhythm-groove/groove-and-feel.md` e una in `rhythmic-devices.md`;
`music-composer` non ha né l'uno né l'altro. E su un punto la skill grande
**indurrebbe in errore**: dice «skank guitar precisely on 2 and 4», che è la
conta in *half-time*. Presa alla lettera su una griglia a 16 passi mette lo
skank sui passi 4 e 12, mentre il posto giusto sono **tutti i levare** —
2, 6, 10, 14. Non è l'errore di `DUBPAL01` (lì lo skank mancava del tutto), ma
è la stessa famiglia: **lo skank finisce dove non va**, stavolta partendo da
una fonte che sembra autorevole perché è grande.

> ⚠️ **Nessuna delle due skill serve per questo genere.** `music-composer` non
> ha né reggae né dub: il suo `references/genres.md` copre Dubstep, Reggaeton,
> Bossa Nova e altro, ma di reggae e dub non c'è nessuna voce (verificato il 16
> agosto 2026). `music-composition`, che è venti volte più grande, ne ha le
> poche righe contate qui sopra, e sullo skank dice una cosa che qui sarebbe
> sbagliata (verificato il 17 agosto 2026, dettaglio qui sopra).
> Controllare prima di appoggiarcisi, sempre.

---

### Fonti

[Feel It In The One-Drop, wayneandwax](https://wayneandwax.com/org/lessons/roots-riddim-tutorial.html) ·
[One drop rhythm, Wikipedia](https://en.wikipedia.org/wiki/One_drop_rhythm) ·
[Music Theory/Reggae, Wikibooks](https://en.wikibooks.org/wiki/Music_Theory/Reggae) ·
[Bubblin', Berklee](https://www.berklee.edu/berklee-today/spring-2015/The-Woodshed-Bubblin) ·
[Authentic Reggae & Dub Bass, soundfingers](https://soundfingers.com/blog/reggae-dub-production/authentic-reggae-dub-bass-tutorial/) ·
[Dub Mixing, Sound on Sound](https://www.soundonsound.com/techniques/dub-mixing)
