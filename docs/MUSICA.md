# Conoscenza musicale — cosa funziona sul materiale di questo utente

Questo file **non** è una teoria generale della musica: per quella si invocano
le skill (vedi sotto). Qui sta solo ciò che è stato imparato correggendo
il lavoro, e che nessuna skill generica sa.

### Le due skill, e chi comanda su cosa — 17 agosto 2026

| skill | dimensione | a cosa serve **qui** |
|---|---|---|
| `music-composition` | 1,3 MB in 106 file di riferimento | il **mestiere**: forma, sviluppo motivico, densità, transizioni, protocollo di revisione. Si carica 1-3 file per domanda, seguendo `references/00-navigation.md` |
| `music-composer` | 62 KB in tutto | i suoi `scripts/*.py` **producono MIDI**, che `midi.py` sa rileggere. Come prosa è troppo corta per insegnare qualcosa: `genres.md` sono 7,5 KB per ~35 generi |

⚠️ **Su reggae e dub comanda questo file, non le skill.** Misurato il 17 agosto
2026: `music-composition` ha **tre righe** sul reggae in
`rhythm-groove/groove-and-feel.md` e una in `rhythmic-devices.md`;
`music-composer` non ha né l'uno né l'altro. E su un punto la skill grande
**indurrebbe in errore**: dice «skank guitar precisely on 2 and 4», che è la
conta in *half-time*. Presa alla lettera su una griglia a 16 passi mette lo
skank sui passi 4 e 12, mentre il posto giusto sono **tutti i levare** —
2, 6, 10, 14. Non è l'errore di `DUBPAL01` (lì lo skank mancava del tutto), ma
è la stessa famiglia: **lo skank finisce dove non va**, stavolta partendo da
una fonte che sembra autorevole perché è grande.

Il posto dove la skill grande vale davvero è **quello che questo file non
copriva affatto**: vedi «Quello che una griglia di una battuta non dice».

Stessa disciplina del resto del progetto: si scrive ciò che è stato
verificato, e si segna `[OSS]` ciò che è supposto.

---

## Norme di sound design — dette dall'utente, 16 agosto 2026

Sono cautele di buon senso che un generatore automatico viola con facilità,
perché ogni parametro preso da solo sembra ragionevole. Valgono per ogni
suono generato, non solo per il dub.

| parametro | il guaio | dove tenersi |
|---|---|---|
| **resonance** (LPF e HPF) | ai valori alti il filtro urla e poi autooscilla: quello che si sente è il filtro, non il suono | **non esiste una soglia assoluta** — vedi qui sotto |
| **delay feedback** | l'eco si accumula fino a saturare e coprire tutto il resto | sotto **~34/50**. In dub si arriva alti, ma è un gesto, non un'impostazione |
| **LPF frequency** | vicino a 0 il suono è **praticamente inaudibile** — non "scuro", proprio assente | mai vicino a 0 senza sapere perché |
| **HPF frequency** | speculare: vicino al massimo taglia tutto e non resta niente | mai vicino a 50 |

**La regola generale che le tiene insieme:** un parametro di filtro portato a
un estremo non produce un suono estremo, produce **silenzio**. E il silenzio
non si distingue da un bug di generazione, quindi costa il doppio: prima non
si sente niente, poi si cerca l'errore nel posto sbagliato.

⚠️ Da tenere insieme a una cosa già nota al progetto (FINDINGS §6): un valore
modulabile **non conta se la struttura lo disattiva**. `lpfFrequency` a 40 con
`lpfMode="Off"` è inudibile quanto `lpfFrequency` a 0. Prima la struttura,
poi il valore.

### La risonanza non ha una soglia: ha un compenso

**[CORREZIONE 16 agosto, dall'ascolto]** La prima versione di questa pagina
diceva «resonance sotto ~24/50». Sbagliato: con quella regola rispettata
(risonanza **20**) la sirena di `DUBPAL01` bucava comunque le orecchie.

Due ragioni, e nessuna delle due è un numero:

1. **Le ladder LPF/HPF del Deluge autooscillano alzando la risonanza**
   (doc community). Quanto sia "alto" dipende da cosa c'è intorno: 20 è
   innocuo su un pad grave e feroce su una sirena acuta a onde quadre, dove
   il picco risonante cade proprio nella banda in cui l'orecchio è più
   sensibile.
2. **L'eco moltiplica il picco.** Delay feedback che sale a 33 più riverbero
   a 34 non aggiungono coda: *ripetono e accumulano* la risonanza. Vanno
   contati insieme alla risonanza, non separatamente.

**Il compenso, detto dall'utente:** se si vuole una risonanza estrema, la si
paga **abbassando il volume della patch**. La risonanza gonfia una banda
stretta, e quello che esplode è il *livello percepito*, non il timbro:
togliendo volume si tiene il carattere e si toglie l'aggressione.

Applicato su `DUBPAL02`: risonanza 20 → **12** (non a zero, una sirena dub
senza risonanza non è una sirena) e volume 26 → **17**, più i due
accumulatori ridotti (feedback max 33 → 23, riverbero 34 → 24).

⚠️ E una cosa da guardare sempre, che era sfuggita: il synth vuoto `TEMPL`
porta già tre patch cable suoi, fra cui **`velocity → volume` a +50**, cioè
fondoscala. Non causa il problema ma moltiplica tutto quello che gli sta
sotto. Leggere `sound.patch_cables()` prima di dichiarare finito un suono.

### Come si applica quando c'è un LFO sul filtro

Un wobble è `lfo1 → lpfFrequency`, cioè il cutoff **oscilla intorno alla sua
base**. Vanno scelti insieme, non uno per volta: base 25 con ampiezza 18 sta
fra 7 e 43 e resta sempre udibile; base 12 con la stessa ampiezza passa metà
del tempo sotto lo zero, e il wobble diventa un suono che sparisce a
intermittenza.

## Il corpus non è autoritativo — detto dall'utente, 16 agosto 2026

> «Molte feature non esistono solo perché io non le ho usate nelle mie song,
> ma non è detto per questo che non esistano.»

Vale come regola di metodo generale ed è **già costata una volta**: le
tabelle dei patch cable stavano per essere costruite come cancello sul
corpus, cioè "coppia mai vista, coppia rifiutata". Sarebbe stato sbagliato e
avrebbe reso impossibile metà del sound design.

Misura che lo dimostra: il firmware espone **56** destinazioni di patch cable
(derivate da `param.h`), il corpus ne usa **37**. Le altre 19 esistono.

| per sapere cosa il firmware accetta | fonte |
|---|---|
| destinazioni di modulazione | `param_ids.py`, cioè l'enum di `param.h` |
| sorgenti di modulazione | capitolo Modulation del guidebook (ARCHITETTURA §9b) |
| enumerazioni corte (modi di filtro, forme d'onda) | `structure.py` — lì il corpus le esaurisce davvero |
| **quante volte una cosa è stata usata** | il corpus, e **solo** per questo |

Dove il corpus resta utile è come *informazione*: `sound.set_patch_cable()`
riferisce quante volte quella coppia compare, così chi legge sa se è terreno
battuto — ma non blocca niente.

## Preset e come vengono usati

Nessun preset di suono è stato usato finora: i suoni si progettano dal
**synth vuoto del dispositivo**, `refs/synths/TEMPL.XML` — due oscillatori
square, subtractive, filtro aperto, delay e riverbero a zero, modulatori FM
assenti. Non è un preset, è il telaio.

Due cose da sapere prima di usarlo:

- **dopo `create.add_track()` i parametri stanno sulla CLIP, non sullo
  strumento.** `<defaultParams>` del preset diventa il `<soundParams>` della
  clip. Quindi: struttura (forme d'onda, modo di sintesi, tipo di filtro,
  unisono, LFO) sullo **strumento**; valori e patch cable sulla **clip**.
- **un drum di kit è un `<sound>` completo**, con gli stessi oscillatori e
  inviluppi di un synth. Un kit sintetizzato si fa svuotando un kit di
  campioni e rimettendoci drum costruiti dallo stesso telaio. Il drum va
  progettato **prima** di `kit.add_drum()`: da lì in poi i suoi
  `defaultParams` vengono copiati nel `soundParams` della riga.

## Groove e generi

### Reggae e dub — istruzioni compositive

> ⚠️ **Nessuna delle due skill serve per questo genere.** `music-composer` non
> ha né reggae né dub: il suo `references/genres.md` copre Dubstep, Reggaeton,
> Bossa Nova e altro, ma di reggae e dub non c'è nessuna voce (verificato il 16
> agosto 2026). `music-composition`, che è venti volte più grande, ne ha
> **quattro righe in tutto** e sullo skank dice una cosa che qui sarebbe
> sbagliata (verificato il 17 agosto 2026, dettaglio in testa al file).
> Controllare prima di appoggiarcisi, sempre.
>
> Tutto quanto segue viene da ricerca web ([WEB], fonti in fondo alla
> sezione). Non è ancora stato validato dall'ascolto dell'utente: `DUBPAL01`,
> scritto **prima** di questa ricerca, è stato giudicato «molto elementare e
> per niente somigliante a un pezzo dub».

#### Le quattro parti, e come si incastrano

Il reggae non è definito dall'armonia ma dalla **spartizione ritmica della
battuta fra le parti**. Ogni parte occupa un posto che le altre lasciano
libero. Griglia a 16 passi per battuta, come `MU.passi()`:

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

**Il punto che avevo sbagliato in `DUBPAL01`:** avevo messo il **charleston**
sui levare e non avevo affatto lo **skank**. È l'opposto. Il charleston fa una
*timeline regolare* — ottavi, o sedicesimi con i levare appena accentati — e
il levare è dello **skank**, che è armonia, non percussione.

#### La batteria

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

Tempo: **50-100 BPM**, con 70-78 al centro del roots. Quindi 70 BPM non è
"lento per il dub", è il posto giusto.

#### Il basso

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

#### L'armonia

**Pochi accordi, spesso solo due alternati.** [WEB] Quello che distingue
l'armonia reggae non è la complessità ma il **ritmo con cui è suonata** — lo
skank. Una progressione ricca suonata dritta non è reggae; due accordi
suonati in levare lo sono.

#### Il dub come *pratica*, non come stile

Il dub nasce al banco del mixer: si parte da un riddim già suonato e lo si
**smonta in tempo reale**.

- **si compone togliendo.** La struttura è "parti che entrano ed escono", non
  "sezioni che si sviluppano". Un vuoto di quattro battute con sole batteria
  ed eco vale più di un ritornello.
- **delay e riverbero sono strumenti compositivi**, non rifiniture. Il
  *"chick-a"* dello skank raddoppiato è delay, non due colpi suonati.
- l'eco classico si manda su **colpi singoli** — un rullante, una parola, uno
  stab — non su tutta la parte.
- in `arranger.py` questo si scrive con i **buchi fra le istanze**.

#### Fonti

[Feel It In The One-Drop, wayneandwax](https://wayneandwax.com/org/lessons/roots-riddim-tutorial.html) ·
[One drop rhythm, Wikipedia](https://en.wikipedia.org/wiki/One_drop_rhythm) ·
[Music Theory/Reggae, Wikibooks](https://en.wikibooks.org/wiki/Music_Theory/Reggae) ·
[Bubblin', Berklee](https://www.berklee.edu/berklee-today/spring-2015/The-Woodshed-Bubblin) ·
[Authentic Reggae & Dub Bass, soundfingers](https://soundfingers.com/blog/reggae-dub-production/authentic-reggae-dub-bass-tutorial/) ·
[Dub Mixing, Sound on Sound](https://www.soundonsound.com/techniques/dub-mixing)

### Velocity groove

> Richiesta dell'utente, 16 agosto 2026: «conoscere drum pattern tipici di un
> genere è molto utile, e magari anche velocity grooves». Ha ragione, ed è
> quello che manca a `DUBPAL01`: i pattern erano quasi giusti e **piatti**.

**La velocity non è un dettaglio di rifinitura: è metà del groove.** Colpi
tutti uguali appiattiscono il polso, e il risultato "marcia" invece di
respirare — vale per qualunque genere.

La scala corrente della programmazione di batteria, su 127: [WEB]

| livello | velocity | quando |
|---|---|---|
| massimo | 110-127 | il colpo che definisce la battuta |
| forte | 100-110 | accenti |
| normale | 90-100 | il corpo del pattern |
| sottovoce | 70-90 | riempimento |
| **fantasma** | **< 70** (rullante: 35-50) | tessuto, non evento |

E di quanto varia un accento rispetto al colpo normale, per strumento: [WEB]

| | escursione |
|---|---|
| cassa | ~30 |
| rullante | ~20 |
| piatti e charleston | ~15 |

Regole pratiche che ne discendono:

- **rullante**: colpi principali 100-115, **fantasmi a 35-50** fra un accento
  e l'altro (sulla "e" o sulla "a" del movimento).
- **charleston**: variare fra **60-95**, con l'accento occasionale a 100. Su
  una fila di charleston: accento sui movimenti a 85-90, quelli in mezzo a
  65-75.

Nella libreria i livelli sono tre, e si scrivono nel pattern:

```
x  colpo (90)      X  accento (110)      o  fantasma (42)      .  silenzio
```

`MU.passi(pattern, velocity=…, accento=…, fantasma=…)` per spostarli. Il
terzo livello **non c'era** fino al 16 agosto 2026: è stato aggiunto proprio
per questa lacuna, perché con due soli livelli un fantasma è impossibile.

#### Il velocity groove del one drop

- il colpo sul **3** è l'accento dominante e va nettamente sopra tutto il
  resto — è l'unico evento forte della battuta;
- **charleston mai identici**: gli ottavi dritti e uguali «suonano troppo
  squadrati», e i **levare vanno accentati appena**, non molto; [WEB]
- **fantasmi di rullante** fra un cross-stick e l'altro danno il tessuto;
- l'**apertura di charleston** sull'ultimo ottavo prima della battuta nuova è
  il colpo più forte del charleston.

#### Il feel: swing, non solo velocity

Il one drop è **laid-back**: gli ottavi di charleston sono **swingati**, e i
levare arrivano leggermente in ritardo — «leaning into the space rather than
cutting through it». [WEB]

Lo **swing** si fa con lo swing di song, e la sua scala è documentata
(FINDINGS §6): il display va **0-100 con 50 = dritto**, e nel file è un valore
con segno centrato sullo zero.

```python
S.set_swing(doc, 57)      # unita' del display: sopra 50 = swingato
```

⚠️ In `DUBPAL01` avevo scritto `set_swing(doc, 50)`, cioè **dritto**. Per un
one drop è sbagliato in partenza.

##### Ma swing e laid-back non sono la stessa cosa — correzione del 17 agosto 2026

La versione precedente di questa pagina diceva che sul Deluge il laid-back
«non si fa spostando le note: c'è lo swing di song». **Sono due cose diverse,
e la seconda non copre la prima.**

- lo **swing** cambia il *rapporto* fra i due ottavi di ogni movimento, ed è
  un'impostazione **della song**: vale per tutte le tracce insieme;
- il **laid-back** è una parte intera che arriva costantemente *dopo* la
  griglia, indipendentemente dalle altre. `music-composition`
  (`rhythm-groove/groove-and-feel.md`) lo chiama pocket **a strati**: cassa sul
  tempo, rullante appena dietro, charleston appena avanti — e dice che è così
  che funzionano quasi tutti i groove di soul e reggae. Lo swing di song, che
  muove tutti insieme, non lo può produrre.

**E il Deluge ha la grana per farlo.** Con la RESOLUTION di default sono
**96 tick per movimento**; a 70 BPM un movimento dura 857 ms, quindi
**1 tick ≈ 8,9 ms**. La finestra di microtiming che si sente è 20-40 ms, cioè
**2-5 tick**: abbondantemente rappresentabile. Lo strumento esiste già ed è
`MU.sposta(doc, clip, tick=…)` (§6-quinquies).

⚠️ **Ma `sposta()` oggi non serve a questo, e va sistemata prima di usarla
così.** Trasla e basta: le note che finiscono oltre la fine della clip
**restano fuori** — il dispositivo le conserva e non le suona, e lo dice
`avvertenze()`. Su una clip in loop di una battuta un ritardo di 3 tick fa
uscire l'ultimo colpo invece di riportarlo in testa. Serve uno spostamento
**modulo la lunghezza della clip**, che non c'è: candidato a `MU.laid_back()`.

[IPO] Tutto questo paragrafo è **ragionato, non ascoltato.** Il numero di tick
è aritmetica sulla RESOLUTION documentata, ma che 3 tick di ritardo sul basso
si *sentano* come pocket e non come errore lo può dire solo l'ascolto. E qui
ascoltare è la verifica giusta: l'affermazione riguarda ciò che si sente.

### Pattern tipici per genere

Catalogo che cresce. Griglia a 16 passi = una battuta, direttamente
incollabile in `MU.passi()`.

#### Reggae / dub — one drop, 70 BPM

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

### Lo swing del jazz, MISURATO — 17 agosto 2026

Primi numeri `[MIS]` di questo documento: non vengono dal web né da una
skill, ma da **333 assoli e 27 943 coppie di crome** della Weimar Jazz
Database, misurati con `WJ.swing()`.

La grandezza è **dove cade il levare dentro il movimento**: 50% è dritto,
66,7% è la terzina. In BUR (*beat-upbeat ratio*, la misura standard della
letteratura): 1 dritto, 2 terzina.

**Complessivo: levare al 61,7%, BUR 1,61** (quartili 56,8%-65,9%).

Cioè: **il jazz non swinga in terzine.** Sta fra il dritto e la terzina, più
vicino alla terzina, e la variabilità fra assoli è larga.

#### Per stile

| stile | assoli | levare | BUR |
|---|---|---|---|
| HARDBOP | 57 | 64,3% | **1,80** |
| BEBOP | 42 | 63,6% | 1,75 |
| COOL | 45 | 63,3% | 1,73 |
| SWING | 45 | 62,2% | 1,65 |
| TRADITIONAL | 21 | 62,0% | 1,63 |
| POSTBOP | 106 | 59,8% | 1,49 |
| FREE | 5 | 58,1% | 1,39 |
| FUSION | 12 | 55,7% | **1,26** |

L'ordine ha senso musicale e nessuno gliel'ha imposto: il bebop e l'hard bop
sono il cuore dello swing di crome, il postbop si raddrizza, la fusion —
figlia del rock e del funk — è quasi dritta.

#### Per feel dichiarato

| rhythmfeel | assoli | levare | BUR |
|---|---|---|---|
| SWING | 278 | 62,4% | 1,66 |
| TWOBEAT | 21 | 62,0% | 1,63 |
| LATIN | 18 | 58,7% | 1,42 |
| FUNK | 12 | 55,7% | 1,26 |

#### Per tempo — e qui c'è la cosa da sapere

| tempo | assoli | levare | BUR |
|---|---|---|---|
| ≤ 120 | 22 | 58,5% | 1,41 |
| 120-180 | 116 | 65,4% | **1,89** |
| 180-240 | 94 | 63,7% | 1,75 |
| > 240 | 105 | 57,4% | **1,35** |

**Lo swing cala al salire del tempo**, come dice la letteratura: da 1,89 a
1,35 fra i medi e i velocissimi. Sopra i 240 BPM le crome sono quasi dritte —
non per scelta stilistica ma perché a quella velocità non c'è spazio.

E il caso dei lenti, che va letto e non preso alla lettera: sotto i 120 BPM il
numero **scende** a 1,41. Probabilmente perché nelle ballad lo swing si sposta
sulle **semicrome**, e questa misura guarda le crome — quindi lì misura il
livello metrico sbagliato. `[OSS]`, non verificato.

#### Come si è arrivati al numero, che vale più del numero

⚠️ **Tre tentativi hanno dato 1,10, 1,19 e 1,10, e sembravano confermarsi a
vicenda.** Erano lo stesso errore tre volte.

La posizione **annotata** nel database (`tatum`/`division`) **contiene già lo
swing**: i trascrittori scrivono una coppia di crome swingate come *tatum 1 e
3 di division 3*, cioè mettono la terzina nella griglia metrica. Filtrare le
crome con `division == 2` — che sembra ovvio, «prendi le crome» — seleziona
quindi le sole coppie che il trascrittore ha giudicato **dritte**. Il
risultato tornava 1,0 per costruzione.

Non l'ha trovato un test: l'ha trovato **guardare le righe grezze** di un
assolo lento e vedere `tatum=1/3`. E a smascherarlo è stato un **controllo
esterno**: la letteratura dice che lo swing cala col tempo e che i generi a
crome dritte stanno sotto. Nessuna delle due compariva. Ora compaiono
entrambe.

> È la versione musicale della regola già scritta in questo progetto: *un
> valore che si legge non è un valore che si legge giusto*. Una misura che
> non riproduce una previsione nota è sbagliata anche quando è ripetibile.

⚠️ **Quanto vale e quanto no.** «Playing It Straight» riporta ~1,3 di mediana
sullo **stesso** database; questa misura dà 1,61. Il metodo di quel lavoro non
è leggibile (articolo a pagamento), quindi **la differenza resta non
spiegata** e i valori assoluti sono provvisori. Le *differenze* fra
sottoinsiemi — swing contro fusion, medio contro velocissimo — sono invece
nella direzione che la letteratura descrive.

#### E come si porta sul Deluge — VERIFICATO il 17 agosto 2026

Servono **due** cose, e ignorarne una rende inutile l'altra.

**1. Quanto.** Il display di `set_swing()` **è** la percentuale di posizione
del levare — derivato dal sorgente (`playback_handler.cpp`: la prima metà del
blocco va per `(50+A)/50`, la seconda per `(50−A)/50`, quindi il punto di
mezzo cade a `(50+A)/100`). Quindi:

```
display = 100 × BUR / (BUR + 1)          BUR = display / (100 − display)
```

50 è dritto, **67 è la terzina**, e sotto 50 il levare arriva *in anticipo*.

**2. Su quale figura.** Ed è qui che stava la trappola: `swingInterval`
sceglie **quale figura viene swingata**, e il default del firmware è `7`,
cioè le **semicrome**. Su un groove di crome quel default non muove niente.

```python
S.set_swing(doc, 62, figura='1/8')     # il jazz misurato, SULLE CROME
```

| `swingInterval` | schermo del Deluge | figura swingata |
|---|---|---|
| 4 | 2nd | 1/2 |
| 5 | 4th | 1/4 |
| **6** | **8th** | **1/8 ← il jazz** |
| 7 | 16th | 1/16 ← default del firmware |
| 8 | 32nd | 1/32 |

Le note si muovono a **coppie** della figura nominata, e a spostarsi è la
seconda della coppia.

⚠️ **Tutte e 146 le song del corpus hanno `swingInterval="7"`.** Cioè lo
swing è sempre stato impostato sulle semicrome: su una linea di crome non
poteva sentirsi, e non perché il valore fosse basso.

Quindi la tabella qui sopra diventa scrivibile:

| repertorio | BUR | `set_swing(doc, …, figura='1/8')` |
|---|---|---|
| dritto | 1,00 | 50 |
| **jazz complessivo** | 1,61 | **62** |
| HARDBOP | 1,80 | 64 |
| BEBOP | 1,75 | 64 |
| POSTBOP | 1,49 | 60 |
| FUSION | 1,26 | 56 |
| terzina esatta | 2,00 | 67 |

##### E come ho sbagliato la tabella la prima volta

⚠️ La prima versione diceva **intervallo 5, «4th notes»** — spostata di un
posto. L'osservazione a cinque punti (etichetta ↔ numero nel file) era
giusta; sopra ci avevo appiccicato l'aritmetica del sorgente
`3 << (10 − swingInterval)`, che dà un blocco lungo **la metà** di quello
vero, e ne era uscita la conclusione controintuitiva «l'etichetta nomina il
blocco, non la figura». L'ho pure difesa.

L'ha smontata l'utente ascoltando: *«con 8th sento il primo ottavo dritto e
il secondo swingato»* — una frase che descrive la **coppia**, e la coppia è
fatta della figura nominata. Nessuna aritmetica poteva sostituirla.

> **La lezione:** avevo misurato la cosa giusta e dedotto quella sbagliata.
> La misura diceva solo «etichetta ↔ numero»; il significato musicale non era
> misurato, era **inferito** — e l'ho trattato come se avesse lo stesso peso.

Lo scarto col sorgente resta ignoto ed è dichiarato in
`song.SWING_SCARTO_SORGENTE`: i "swung tick" di quel codice non sono i tick
delle posizioni di nota, e dove si convertano non è stato trovato.

## Quello che una griglia di una battuta non dice — 17 agosto 2026

Rileggendo questa pagina alla luce di `music-composition` è venuta fuori una
cosa che non è un dettaglio mancante ma **un piano intero mancante**:

> Tutto ciò che c'è scritto sopra descrive **una battuta**. Un pezzo ne dura
> centoventi.

Le griglie a 16 passi, le velocity, lo swing, il turnaround ogni 4: sono la
grana fine, ed erano giuste da correggere. Ma il giudizio dell'utente su
`DUBPAL03` — *«va meglio, ma musicalmente ci sarebbe ancora moltissimo da
dire»* — arriva **dopo** che la grana fine era stata sistemata. Quello che
resta da dire vive su una scala più lunga, e di quella scala qui non c'era
niente.

### 1. L'arco di densità — il buco più grosso

`music-composition` (`orchestration/arrangement-density.md`) misura ogni
sezione su una scala di **densità 1-9**, e la regola che ne ricava è secca:

> «Density should always be moving, even if subtly. **Static density across a
> long section feels "stuck"**.»

E dà i tempi di tolleranza dell'ascoltatore: **30 secondi** a densità massima
sono comodi, **60** cominciano a pesare, **90 e oltre** e l'ascoltatore si
stacca. Un pezzo dub a 70 BPM fa una battuta ogni 3,4 secondi: novanta secondi
sono **26 battute**. Un arrangiamento che tiene tutte le parti accese per 32
battute è già oltre, e nessun controllo del progetto se ne accorge.

I tre errori catalogati che un generatore commette per costruzione, perché
scrive tutte le parti e poi le lascia accese:

| errore | cosa succede |
|---|---|
| **too much, too soon** | l'intro è già alla densità del ritornello, e da lì non si sale più |
| **static density** | nessun contrasto: «listeners track music partly through density variation» |
| **no silence** | mai un respiro. E il dub *è* il genere del respiro |

**Qui è dove il dub e la scala di densità coincidono.** «Si compone
togliendo» era già scritto in questa pagina, ma come attitudine. La scala lo
rende una decisione scrivibile: si sceglie il numero per ogni tratto, e
`arranger.py` lo esegue con i buchi fra le istanze — `place_unique()` e la
distanza fra le terne `(pos, length, clipCode)`. **La tecnica c'era già da
tre giorni; mancava la decisione da prendere.**

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

⚠️ [WEB/skill] L'arco qui sopra non è misurato su niente: è la forma standard
applicata al dub. Vale come punto di partenza da far correggere all'ascolto,
non come regola — esattamente lo stato in cui erano le griglie a 16 passi
prima del 16 agosto.

### 2. Il turnaround corregge un caso su quattro

`DUBPAL01` fu giudicato con «4 battute di batteria identiche», e la
correzione registrata è il **turnaround sull'ultima**. Giusto, e insufficiente:
corregge la battuta 4 e lascia identiche la 1, la 2 e la 3.

> «A 1-bar repeating loop sounds robotic. A 2- or 4-bar loop with subtle
> variations — an extra ghost note here, a missed hat there — feels alive.»

Cioè: la variazione non è un evento di confine, è un **tessuto**. Nel
vocabolario che questa pagina già usa, i **fantasmi** (`o`, 42 su 127) sono lo
strumento giusto perché costano poco: spostarne uno, toglierne uno, aggiungerne
uno cambia la battuta senza cambiare il pattern.

E il contrappeso, che vale quanto la regola, perché la correzione istintiva a
«suona piatto» è randomizzare tutto:

> «**Do not overhumanize by randomizing everything. Groove has intentional
> consistency.**»

Le variazioni sono **scelte e poche**, non rumore aggiunto ovunque. Un
generatore che randomizza le velocity ottiene un pattern che non è più piatto
e non è ancora un groove.

### 3. Cassa e basso sono una coppia, e qui non era dichiarato

`instrument-idiom/bass.md` è netto: «**Do not ignore the kick drum.** Bass
rhythm without kick context is incomplete», e dà quattro rapporti possibili —
unisono con la cassa, basso che riempie i buchi della cassa, basso lungo sotto
cassa fitta, cassa sui movimenti e basso sincopato.

Nella griglia delle quattro parti, più sopra, cassa e basso sono descritti in
due righe separate e il rapporto non è mai detto. Guardandolo adesso:

```
cassa           . . . . . . . . x . . . . . . .   solo il 3
basso           x . . . . . x . x . . . . x . .   l'UNO c'e'
```

Il basso **suona l'uno che la batteria lascia vuoto**, e sul 3 va all'unisono
con la cassa. È una scelta legittima e tipica — il basso copre il vuoto del one
drop — ma nel file sembrava un caso. **Scritta, diventa una cosa da tenere o da
cambiare di proposito**; non scritta, è una cosa che si rompe senza accorgersene
appena si tocca una delle due righe.

### 4. La playability è una decisione, non una regola

`instrument-idiom/drums-percussion.md` ha un controllo che sembra fatto apposta
per questo progetto: «MIDI can create patterns that no drummer would choose» —
quattro arti, tempo di spostarsi fra charleston, tom e piatto, fantasmi
realizzabili a quel tempo.

Vale, ma **non sempre, e la differenza va decisa ogni volta**:

| | la playability vincola? |
|---|---|
| roots one drop, kit suonato | **sì** — il genere nasce da una batteria vera, e un pattern impossibile suona finto |
| dub da banco del mixer, kit sintetizzato | **no** — `DUBPAL01` ha un kit costruito dal synth vuoto, nessun campione, nessun batterista implicito |

Il difetto è dichiararlo per caso invece che scegliere. Un kit sintetizzato che
suona un pattern a sei arti è una decisione; lo stesso pattern su un kit roots
è un errore.

### 5. Il ciclo di revisione ha un protocollo, e qui non lo si usava

Il ciclo di questo progetto — *«l'utente ascolta e dice cosa cambiare»* — è
esattamente ciò per cui esiste
`creative-workflows/revision-and-feedback-loops.md`. La sua regola centrale:

> Ogni richiesta di modifica contiene tre strati: **Keep** (cosa è piaciuto),
> **Change** (cosa no), **Direction** (l'asse su cui muoversi). «Preserve the
> liked material and change the smallest musical variable that could solve the
> problem.»

`applica_verbo()` fa già una cosa del genere per i **suoni**, e riferisce cosa
ha mosso. Per la **composizione** non esiste l'equivalente, e si vede nella
storia: `DUBPAL02` è stato corretto dichiarando cosa si cambiava (risonanza,
volume, feedback, riverbero) e **mai cosa si teneva**. Con la regola 1 —
riscaricare dal dispositivo — il danno è stato evitato per un pelo, e per un
motivo indipendente.

Da adottare nel rapporto di ogni revisione, prima di toccare il file:

```
Tengo:    …
Cambio:   …
Direzione: …
Resta regolabile: …
```

## Correzioni ricevute

*(ogni volta che una proposta viene corretta, la lezione va qui, con la data)*

**16 agosto 2026 — «leggi anche documentazione», «leggi anche docs
community».** Ero andato dritto ai file saltando il primo livello della
gerarchia del progetto. Da `ARCHITETTURA.md` §9b è poi venuto il pezzo che
serviva davvero e che i file non dicono: la matrice delle sorgenti di
modulazione, il fatto che gli inviluppi che modulano qualcosa di diverso dal
volume sono **bipolari con neutro 25**, e che i parametri globali (delay, mod
FX, riverbero, arpeggiatore, LFO1 rate) accettano **solo** Sidechain e LFO1
come sorgente. Quest'ultima è una regola che, violata, non dà errore: dà
silenzio.

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

**16 agosto 2026 — «ora ci sono 4 envelope, non 2».** Un risultato di ricerca
web diceva «2 LFO and envelope options»: era il manuale ufficiale vecchio. Il
firmware community ha **4 inviluppi e 4 LFO**, e `TEMPL.XML` infatti porta
`envelope1..4` e `lfo1..4`. Vale come promemoria che sul firmware community
le fonti generaliste sono indietro, e che il guidebook ufficiale va letto
sapendo quale versione descrive.
