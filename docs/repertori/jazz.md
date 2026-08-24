# Jazz

> Una scheda dello schema neutro. Lo schema, il materiale comune a tutti i
> repertori e l'indice stanno in [`../MUSICA.md`](../MUSICA.md).

Da leggere prima del resto: **nessun pezzo jazz è mai stato generato.** Il
24 agosto 2026 è uscita da un Deluge la prima cosa jazz che qualcuno abbia
ascoltato, ed è **una clip di batteria di due battute** costruita per rispondere
a una domanda sola — casella 6, «Cosa si è sentito, e cosa non se ne può
dedurre». Non è
un pezzo, e del suono jazz sul Deluge continua a non dire niente.

Quello che c'è in questa scheda o è misurato su un corpus — lo swing nella
casella 4, la dinamica e i fill nelle caselle 6 e 9 — o è già in libreria (la
7); dall'**ascolto dell'utente** è passata **una cosa sola**, ed è quella clip.
Sul dispositivo sono verificati **due meccanismi** e nient'altro: lo swing, e —
dal 24 agosto — che il dispositivo **conservi le posizioni fuori griglia** che
il groove template scrive (casella 10). È la ragione per
cui cinque caselle su undici sono ancora vuote, e per cui la 11 è vuota **per
costruzione** e non per trascuratezza: una trappola del generatore si osserva,
non si prevede — e le due correzioni che quell'ascolto ha prodotto non sono del
jazz ma del metodo, quindi stanno nel comune. La casella 11 lo argomenta.

## 1. Cos'è, e cosa non è

**Vuota.** Servirebbe la delimitazione fra gli stili, che `wjazzd.db` ha già
come etichette — TRADITIONAL, SWING, BEBOP, COOL, HARDBOP, POSTBOP, FREE,
FUSION — e che nessuno ha ancora letto se non per filtrare la misura dello
swing.

*Nel frattempo, per comporre:* la domanda va **alla skill**, e qui — al
contrario che sul reggae — il jazz lo copre davvero:
`genres/jazz-styles.md` di `music-composition`, raggiunto come sempre dal suo
`references/00-navigation.md`. Ha una sezione per stile, ma **non per il
POSTBOP**, che lì non ha un nome suo (verificato il 18 agosto 2026) ed è
invece lo stile più numeroso della casella 4: se il pezzo è postbop, la
delimitazione resta da chiedere all'utente. Quello che esce dalla skill si
segna `[WEB]`.

## 2. Metro e griglia

**Vuota.** La chiuderebbe una misura sulle metriche di `wjazzd.db`, che porta
`bar/beat/tatum/division` per ogni nota trascritta — quante siano, e quante
abbiano una `division` che non si divide in due, sta in
[`../../HANDOFF.md`](../../HANDOFF.md) §6-nonies, «Cosa è annotato e cosa no».

*Nel frattempo, per comporre:* si scrive in **4/4**, e lo si dichiara come
**assunto `[IPO]`** — non è misurato qui, e `wjazzd.db` avrebbe le metriche
per stabilirlo. La griglia è quella di `MU.passi()` **a 16 passi per
battuta**, la stessa che la scheda del reggae usa nella sua casella 2: un
movimento sono quattro passi, quindi **la croma è due passi**, ed è la croma
che la casella 10 fa swingare con `figura='1/8'`. È anche l'unità in cui la
**casella sorella 4** ha già misurato — coppie di crome dentro il movimento —
quindi le domande dalla 4 in poi cadono su questa griglia senza conversioni.
Quello che esce dall'assunto — i metri dispari, e le ballad, dove la casella 4
stessa sospetta che lo swing si sposti sulle semicrome — si chiede
**all'utente** prima di scrivere.

## 3. Tempo

**Parziale.** **Il grosso del repertorio misurato sta fra 120 e 240 BPM.**
È quello che dice la distribuzione degli assoli sulle fasce di tempo su cui è
stato misurato lo swing — le fasce, e quanti assoli cadano in ognuna, stanno
nella casella 4, «Per tempo». È una distribuzione empirica dei tempi, letta da
dati raccolti per un'altra ragione. Non è però un range *dichiarato* del
repertorio, e manca il tempo *tipico* per stile, che
`wjazzd.db` ha e che non è stato ancora estratto.

*Nel frattempo, per comporre:* si prende quel che dà la **casella sorella 4**,
tabella «Per tempo»: le fasce, e quanti assoli cadono in ognuna. E si guarda
cosa il tempo si porta dietro, perché la stessa tabella lo dice — lo swing da
scrivere nella casella 10 cambia con la fascia, quindi tempo e swing si
scelgono insieme, non uno dopo l'altro. Il tempo del *pezzo* però lo dice
l'**utente**: questa è una distribuzione osservata, non una prescrizione.

## 4. Feel

**L'unica casella `[MIS]` del progetto, e l'unica piena di questa scheda.**
Lo swing del jazz è misurato; tutto il resto del jazz, qui, è dichiarato
mancante.

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

### Lo swing, misurato una seconda volta — 18 agosto 2026

Il **Groove MIDI Dataset** permette di rifare la domanda su un corpus diverso e
con un metodo diverso. I due non misurano la stessa cosa, e la differenza va
letta prima dei numeri:

| | Weimar Jazz Database | Groove MIDI Dataset |
|---|---|---|
| **cosa suona** | la **linea solista** trascritta | un **kit di batteria** intero |
| **contro cosa** | gli onset veri contro i **battiti annotati** dal trascrittore | gli onset contro la **griglia MIDI nominale** al BPM dichiarato da `info.csv`, tolta l'origine |
| **quanto** | 333 assoli, 27 943 coppie di crome | 41 esecuzioni `beat` 4/4, **5 batteristi** |
| **come si aggrega** | mediana per assolo, poi mediana fra assoli | mediana per esecuzione, poi mediana fra esecuzioni |
| **funzione** | `WJ.swing()` | `GR.bur_da_posizioni()`, dentro `GR.profilo()` |

L'aggregazione è la stessa in tutt'e due — **un'esecuzione vale un voto**, così
che una lunga non pesi come dieci corte — e questo rende i due numeri
confrontabili nonostante tutto il resto differisca.

Delimitato come dice la casella 6 — l'etichetta `jazz` per prefisso, **tolti
`jazz/funk` e `jazz/fusion`** — il Groove MIDI dà **levare al 59,7%, BUR 1,48**
(quartili 1,05-1,73), su **41 esecuzioni e 5 batteristi** `[MIS]`.

Accanto al **61,7% / BUR 1,61** di Weimar, quindi: **due punti di levare di
distanza.** Due corpora diversi, due metodi diversi, due strumenti diversi, e
le mediane cadono quasi nello stesso punto.

⚠️ **Un'obiezione, e il controllo che la chiude.** `WJ.swing()` scarta gli
assoli con meno di **20 coppie** di crome — «una mediana su quattro valori non
è una mediana» — e la misura sul Groove MIDI quella soglia non ce l'ha:
**18 delle 41 esecuzioni** poggiano su meno di 20 coppie, e alcune su una sola.
Rialzando la soglia il numero però **non si muove**: 1,48 senza soglia, 1,43 a
5 coppie, 1,46 a 10, **1,49 a 20** (23 esecuzioni, 4 batteristi) `[MIS]`. La
mediana non sta in piedi sulle esecuzioni magre.

Sul **solo ride** lo stesso controllo va fatto sulle **coppie del ride**, non
su quelle del kit — filtrare un numero col conteggio di un altro non
verificherebbe niente — e lì il campione **si dimezza**: 1,99 su 21 esecuzioni
e 4 batteristi senza soglia, **2,00 su 10 esecuzioni e 3 batteristi** con la
soglia a 20 `[MIS]`. Il valore non si muove, ma **il 2,00 poggia su metà delle
esecuzioni e su un batterista in meno**, e va citato con questo accanto.

⚠️ **Ma l'accordo fra due mediane non è un accordo su cosa faccia un
batterista jazz**, e questa è la parte che serve a chi compone. Il numero si
muove **molto di più dentro il Groove MIDI** che fra i due corpora:

| sottoinsieme | esecuzioni | batteristi | levare | BUR |
|---|---|---|---|---|
| tutta l'etichetta `jazz` | 47 | 5 | 55,7% | **1,26** |
| senza funk e fusion | 41 | 5 | 59,7% | **1,48** |
| sola etichetta `jazz/swing` | 10 | 2 | 61,6% | **1,60** |

e per batterista, sull'etichetta intera, va da **0,77** (`drummer4`, 2
esecuzioni) a **1,72** (`drummer10`, 9), con `drummer3` a 1,11 su 13 e
`drummer1` a 1,48 su 17 `[MIS]`. Cioè: **la delimitazione decide il numero.** Chi
misura senza dichiarare cosa ha incluso può produrre 1,26 o 1,60 dallo stesso
corpus, e nessuno dei due è sbagliato.

#### E lo strumento decide ancora di più

Il BUR qui sopra è misurato sul **kit intero**, perché è quello che
`GR.profilo()` restituisce. Misurato sul **solo ride** — lo strumento che nel
jazz porta lo swing — sulle **stesse 21 esecuzioni** che hanno l'uno e
l'altro, e quindi senza che la selezione possa spiegarlo:

| misurato su | esecuzioni | batteristi | levare | BUR |
|---|---|---|---|---|
| il kit intero | 21 | 4 | 61,4% | 1,59 |
| il **solo ride** | 21 | 4 | **66,6%** | **1,99** |

Il ride swinga più del kit in **17 esecuzioni su 21** `[MIS]`. Cioè **il ride
sta praticamente sulla terzina** (1,99 contro il 2,0 esatto), mentre cassa e
rullante, che accompagnano sulla griglia dritta, tirano l'insieme verso l'1,5.

**Quale credere, allora.** Non c'è un numero solo, e fingere che ci sia
sarebbe il vero errore:

- per una **linea di ride**, il valore misurato è ~2,0, cioè la terzina —
  Groove MIDI, 21 esecuzioni, 4 batteristi;
- per un **kit** preso insieme, ~1,5 — Groove MIDI, 41 esecuzioni, 5 batteristi;
- per una **linea melodica solista**, 1,61 — Weimar, 333 assoli.

Sono tre risposte a tre domande diverse, non tre stime della stessa. Lo swing
di song del Deluge però è **uno solo e vale per tutte le tracce**: la casella
10 deve quindi **scegliere**, e la scelta è una decisione musicale dichiarata,
non un dato. Quel che il numero non può fare è nascondere che sotto ci sono
quartili larghissimi (1,05-1,73 sul kit) e batteristi che vanno da 0,77 a 1,72.

#### La previsione che si ripete, e vale più dell'accordo

La casella qui sopra sospettava, `[OSS]` e non verificato, che **sotto i 120
BPM lo swing cali** perché nelle ballad si sposta sulle semicrome. Il Groove
MIDI, che non sa niente di Weimar, dice la stessa cosa `[MIS]`:

| tempo | esecuzioni | batteristi | BUR Groove MIDI | BUR Weimar |
|---|---|---|---|---|
| ≤ 120 | 21 | 4 | **1,11** | 1,41 |
| 120-180 | 11 | 3 | 1,59 | 1,89 |
| 180-240 | 8 | **2** | 1,60 | 1,75 |
| > 240 | 1 | 1 | — | 1,35 |

*(la colonna Weimar è quella della tabella «Per tempo» qui sopra, riportata
solo per affiancarla: se un giorno si corregge, si corregge lì.)*

⚠️ **La colonna dei batteristi va letta insieme alla forma.** Il massimo sta
sui medi, ma la fascia 180-240 sono **due soli batteristi** e quella sopra i
240 **uno**: la parte solida dell'accordo è il **minimo sui lenti**, che poggia
su 21 esecuzioni e 4 batteristi. Il resto della curva è nella stessa direzione
di Weimar e su un campione che non la sosterrebbe da solo.

I due corpora non concordano sui valori, ma concordano sulla **forma**: il
minimo sta sui lenti, il massimo sui medi. Un secondo corpus che riproduce una
previsione fatta sul primo vale più dell'accordo fra due mediane — è lo stesso
criterio con cui, qui sopra, si è smascherato l'errore delle tre misure che si
confermavano a vicenda. La fascia oltre i 240 BPM ha **una sola** esecuzione e
non dice niente.

## 5. Ruoli e spartizione

**Vuota.** È la casella più difficile da chiudere con il materiale in casa:
`wjazzd.db` trascrive **la linea solista**, non l'accompagnamento, quindi del
rapporto fra comping, walking e solista non dice niente. Servirebbe MusicXML —
che però il progetto non legge ancora: in `tools/delugexml/` ci sono il lettore
di MIDI, quello dell'XML del Deluge e quello di `wjazzd.db`, e nessun lettore
di partitura. Qui non manca il corpus, manca il codice che lo apre.

*Nel frattempo, per comporre:* la domanda va **alla skill**, dal suo
`references/00-navigation.md`: `genres/jazz-styles.md` per come comping,
walking e solista si spartiscono la battuta, e `instrument-idiom/bass.md` per
il walking. `[WEB]` a quello che ne esce. Il rapporto fra cassa e basso va
comunque **dichiarato** e non subìto, qualunque sia la fonte: il comune,
«Cassa e basso sono una coppia, e va dichiarata».

## 6. Dinamica

**Misurata sul Groove MIDI Dataset — 18 agosto 2026.** La velocity della
batteria jazz non viene più dal web: viene da **101 esecuzioni** col prefisso
`jazz` su **1150 righe** di `info.csv` — **50 `beat`** e **51 `fill`** — suonate
da **cinque batteristi** `[OSS]`, su un kit elettronico e in studio, che è
quanto dichiara la documentazione del dataset e non qualcosa che si legga nei
file `[MAN]`. Le misure si
rifanno con `.venv/Scripts/python.exe tools/misura_groove.py`; `to-read/` è in
`.gitignore`, quindi i conteggi qui sotto sono lo stato del disco di quel
giorno e non si riproducono senza il dataset.

⚠️ **Cinque batteristi non sono cinque parti uguali.** `drummer1` da solo porta
**19 `beat` su 50**, poi `drummer3` 13, `drummer10` 10, `drummer7` 6,
`drummer4` 2 `[OSS]`. Per questo ogni numero qui sotto porta accanto **quante
esecuzioni e quanti batteristi** lo sostengono: è la sola difesa contro il
travestire un esecutore da genere, ed è il motivo per cui `GR.scala()`
restituisce quel conteggio invece di limitarsi alla mediana.

### La delimitazione, prima dei numeri

L'etichetta si prende **per prefisso** — la regola di `GR.per_prefisso()`, non
la sottostringa: cercare `reggae` dentro l'etichetta prenderebbe anche
`latin/reggaeton` e `latin/brazilian-sambareggae`, che reggae non sono. Dentro
`jazz` così preso ci stanno però anche **`jazz/funk` (24 esecuzioni)** e
**`jazz/fusion` (11)**, che di swing di crome non ne hanno — e non è
un'impressione, è misurato: BUR **0,73** sulle 2 `beat` di funk (1 batterista)
e **1,10** sulle 4 di fusion (1 batterista), contro l'**1,48** delle 41 del
resto (5 batteristi) `[MIS]`. Cioè crome quasi dritte, su campioni piccoli ma
concordi. Le misure di **swing** li escludono per questo, e la casella 4 lo
ripete con la tabella.

Per la **dinamica** invece il taglio quasi non conta, ed è misurato e non
supposto: nel sottoinsieme `beat` funk e fusion sono appena **2 e 4 esecuzioni
su 50** — 29 delle loro 35 stanno fra i `fill` — e togliendole le mediane
della tabella qui sotto si spostano **al massimo di 3 punti su 127** `[MIS]`.
La tabella vale quindi per l'etichetta intera, e lo dice invece di lasciarlo
supporre.

### La scala di velocity, per strumento

Mediana e quartili dei colpi veri, sulle **50 esecuzioni `beat`** `[MIS]`:

| strumento | mediana | q1-q3 | min-max | colpi | esecuzioni | batteristi |
|---|---|---|---|---|---|---|
| rullante | **47** | 33-75 | 4-127 | 10 689 | 45 | 5 |
| charleston a pedale | **70** | 50-85 | 17-120 | 5 217 | 36 | 4 |
| ride | **64** | 52-81 | 5-127 | 7 422 | 32 | 5 |
| kick | **59** | 46-83 | 6-127 | 5 577 | 48 | 5 |
| charleston chiuso | 38 | 25-51 | 5-127 | 545 | 12 | 4 |

Tre cose che questa tabella dice e che la scala `[WEB]` del comune non diceva:

- **il jazz suona piano.** Le mediane dei quattro strumenti portanti stanno fra
  47 e 70 — e quella del charleston battuto scende a 38 — cioè dove il comune
  mette il «riempimento» (70-90) e sotto. Il «corpo del pattern» a 90-100,
  applicato al jazz, starebbe **più di quaranta punti sopra** il rullante vero;
- **il rullante è per lo più fantasma.** Mediana 47 e q1 a 33: un quarto dei
  colpi sta sotto 33. Il comune mette i fantasmi di rullante a 35-50 come
  eccezione fra un accento e l'altro; qui sono **il tessuto normale**, e
  l'escursione va da 4 a 127 `[MIS]`;
- **il charleston del jazz è quello a pedale**, non quello battuto: **5 217
  colpi su 36 esecuzioni** contro **545 su 12** `[MIS]`. È il piede sul 2 e sul
  4, e il profilo qui sotto dice esattamente dove cade.

### Il profilo posizionale: quali passi vengono accentati davvero

Sulla griglia a 16 passi della casella 2, aggregando le **41 esecuzioni `beat`
4/4 senza funk e fusion**, ogni esecuzione pesata uno — se no il file da 193
battute deciderebbe da solo cosa fa un batterista jazz. Ogni cella è **quota
dei colpi di quello strumento · velocity mediana**; le colonne sono le otto
crome, e quel che manca al 100% sta sui passi dispari, cioè sulle semicrome
`[MIS]`:

| strumento (esecuzioni, batteristi) | 1 | lev 1 | 2 | lev 2 | 3 | lev 3 | 4 | lev 4 |
|---|---|---|---|---|---|---|---|---|
| **ride** (18, 4) | 14,1% v70 | 3,4% v64 | **15,5% v86** | 12,3% v67 | 15,5% v72 | 3,0% v69 | **13,9% v88** | 10,7% v66 |
| **charleston a pedale** (23, 3) | 7,5% v44 | 4,3% v64 | **25,7% v66** | 2,7% v68 | 7,8% v50 | 6,8% v60 | **23,7% v71** | 1,9% v61 |
| **rullante** (28, 5) | 5,4% v75 | 7,0% v47 | 12,1% v58 | 7,8% v54 | 5,3% v58 | 8,2% v56 | 10,6% v63 | 8,5% v59 |
| **kick** (23, 4) | **18,8% v65** | 5,4% v54 | 9,8% v53 | 7,2% v58 | 13,7% v62 | 9,3% v53 | 10,7% v58 | 6,5% v52 |

Quello che ne esce è il jazz che ci si aspetta, e nessuno gliel'ha imposto:

- **il ride fa lo *spang-a-lang*.** Colpisce i quattro movimenti in parti quasi
  uguali (14,1 · 15,5 · 15,5 · 13,9%), e il levare lo aggiunge **dopo il 2 e
  dopo il 4** (12,3 e 10,7%) e quasi mai dopo l'1 e il 3 (3,4 e 3,0%). E
  **accenta il 2 e il 4 di 16 punti** di velocity — v86 e v88 contro v70 e
  v72 `[MIS]`. Se un pattern di ride jazz va scritto a mano, questa riga è la
  risposta;
- **il charleston a pedale è il 2 e il 4, e nient'altro:** metà dei suoi colpi
  (25,7 + 23,7 = **49,4%**) cade lì, con la velocity più alta della sua riga
  (66 e 71 contro 44 e 50 sull'1 e sul 3). È anche la **verifica che la
  griglia è allineata**: il piede sul 2 e sul 4 è un fatto noto del repertorio,
  e ritrovarlo sui passi 4 e 12 dice che l'origine della battuta nei file è
  davvero una stanghetta;
- **il rullante non ha un posto: ha due livelli.** È l'unico strumento sparso
  su tutti e sedici i passi — **oltre un terzo dei suoi colpi sta sulle
  semicrome** — e a separarlo non è la posizione ma la velocity: passi pari
  47-75, passi dispari 41-53. È la definizione operativa di fantasma;
- **la cassa sta sull'1 e sul 3** (18,8 e 13,7%, contro 9,8 e 10,7 sul 2 e sul
  4) e anche dove batte di più sta **piano**: v65 e v62 su 127, cioè dentro la
  fascia che il comune chiama «riempimento». Non è il colpo che definisce la
  battuta — è il contrario di quello che fa in un repertorio a cassa in
  quattro.

### Il microtiming che resta, e perché è poco

Tolti l'origine della griglia e lo swing — la catena di `GR.profilo()` — quello
che resta è il **residuo**, in tick Deluge (96 per movimento) `[MIS]`:

| strumento | esecuzioni | batteristi | mediana | q1-q3 |
|---|---|---|---|---|
| charleston a pedale | 23 | 3 | −3,39 | −4,78 … −2,11 |
| rullante | 26 | 4 | −2,17 | −3,10 … −0,20 |
| kick | 22 | 4 | −1,23 | −2,68 … −0,50 |
| ride | 18 | 4 | −0,81 | −2,02 … +0,21 |

**Le mediane stanno tutte entro 3,4 tick**: poche unità su 96 per movimento, e
tutte dalla stessa parte — **prima** della griglia. Per la scala, e per i
numeri che vengono dopo: un tick vale 6,25 ms a 100 BPM e 3,38 ms a 185.

⚠️ **Ma questi sono livelli, e un livello in millisecondi non vuol dire
niente.** Convertirli e confrontarli con la finestra dell'udibile sarebbe la
scorciatoia comoda, ed è sbagliata: dopo `GR.origine()` il livello di ogni
esecuzione ha uno **zero arbitrario** — l'origine tolta è comune a tutto il kit
e cambia da esecuzione a esecuzione — quindi «−3,39 tick» non dice *rispetto a
che cosa*, e un millisecondo ricavato da lì non ha un referente. Qui i tick
servono a una cosa sola: a dire che il residuo è **piccolo**.

Con la finestra di 20-40 ms del comune si confrontano **due altre** grandezze,
e danno due verdetti opposti perché *sono* due cose diverse — non perché una
delle due sia sbagliata:

| grandezza | quanto | contro la finestra 20-40 ms | dove sta |
|---|---|---|---|
| **divario fra due pad** (ride − charleston) `[MIS]` | 13,0 ms | **sotto** | «E prima di tutto: 13 ms» |
| **singolo spostamento** che un template scrive `[OSS]` | 39,9 ms | al **bordo superiore** | «Due grandezze diverse» |

La prima sta su decine di esecuzioni ed è la stratificazione misurata; la
seconda sta su **una** esecuzione e poggia su **un colpo solo**. Il divario è
inoltre convertito col BPM di **ogni** esecuzione, non a un 100 BPM di comodo:
è l'altra ragione per cui i conti di questa casella non si sommano fra loro. Le
cautele di ciascuna sono scritte nella sua sezione, e **nessuna delle due è il
livello della tabella qui sopra** — che infatti in millisecondi non viene
convertito.

#### C'è una stratificazione, e il piede anticipa tutto il resto

Le mediane qui sopra vengono da esecuzioni diverse, e un'esecuzione intera può
stare avanti o indietro per conto suo: confrontarle fra loro direbbe poco. La
domanda va fatta **dentro la stessa esecuzione**, e a **tutte** le coppie —
sceglierne una dopo aver visto le mediane sarebbe scegliere il risultato.
Esecuzioni `beat` 4/4 senza funk e fusion `[MIS]`:

| coppia | esecuzioni | batteristi | il primo arriva | in |
|---|---|---|---|---|
| charleston a pedale − ride | 15 | 3 | **2,59 tick PRIMA** | **15 su 15** |
| charleston a pedale − kick | 18 | 2 | 2,23 tick prima | 14 su 18 |
| charleston a pedale − rullante | 22 | 3 | 1,38 tick prima | 17 su 22 |
| kick − ride | 12 | 3 | 0,54 tick prima | 7 su 12 |
| rullante − ride | 14 | 3 | 0,34 tick prima | 8 su 14 |
| rullante − kick | 21 | 3 | 0,22 tick dopo | 11 su 21 |

Il disegno sta tutto in una riga: **il charleston a pedale anticipa tutto il
resto**, in tutte e tre le coppie che lo riguardano — e contro il ride in
**15 esecuzioni su 15**, con scarti da 0,08 a 6,03 tick. Fra ride, cassa e
rullante invece non c'è ordine: mediane sotto il mezzo tick e conteggi da testa
o croce.

⚠️ **Il segno, perché è facile invertirlo.** `Passo.scarto` è il residuo
rispetto al passo: **positivo = il colpo cade dopo la griglia**, negativo =
prima. Lo conferma `MU.applica_groove()`, che fa `pos + scarto`. Il charleston
a pedale ha il residuo **più negativo** di tutti (−3,39), quindi è il **più in
anticipo**. E la stessa cosa si vede **senza togliere niente** — né origine né
swing — sulle fasi grezze dentro il movimento, contando i soli colpi entro un
quarto di movimento dal battere e i soli strumenti che ne hanno almeno venti:
charleston **−6,85** tick (24 esecuzioni, 4 batteristi) contro ride **−2,35**
(18 esecuzioni, 4 batteristi), con rullante a **−4,10** (29 esecuzioni, 5
batteristi) e cassa a **−4,90** (25 esecuzioni, 4 batteristi); e appaiando
dentro la stessa esecuzione, il charleston anticipa il ride in **15 su 15**
(15 esecuzioni, 3 batteristi) `[MIS]`. Sono **tutte** negative perché qui
l'origine non è stata tolta e il kit intero sta prima della griglia: quello che
si guarda non è il valore, è **chi sta prima di chi**. E lì i due estremi
tengono — charleston primo, ride ultimo, come nella tabella del residuo —
mentre rullante e cassa **si scambiano di posto** fra le due misure, che è la
stessa cosa che dice il conteggio da testa o croce di quella coppia.

**E non è un artefatto di dove i due suonano.** Il residuo dipende dal passo, e
i due strumenti non suonano sugli stessi: il charleston concentra i colpi sul 4
e sul 12 molto più del ride, quindi la differenza poteva essere «chi suona
dove» e non «chi anticipa». Rimisurata sui **soli passi 4 e 12**, dove suonano
entrambi, la stratificazione **cresce**: **2,89 tick e 14 su 14** (14
esecuzioni, 3 batteristi), contro 2,59 e 15 su 15 a passi liberi `[MIS]`.

⚠️ **Ma il 15 su 15 è unanime per un pelo, e il pelo è proprio il template.**
`drummer1/session3/2` — l'esecuzione che questa casella raccomanda più sotto
come groove template — è **il caso estremo minimo** della fila: **+0,08 tick**,
cioè **0,3 ms**, il `min` dell'intervallo «0,08…6,03» citato qui sopra `[OSS]`.
Con uno stimatore appena diverso quel file **cambia segno**: la mediana sui
**colpi**, ristretta ai passi con almeno dieci, dà +0,08, mentre la mediana sui
**passi** non pesata dà −3,41 — perché i valori positivi grossi del charleston
stanno su passi da 1 a 24 colpi, mentre i suoi due passi dominanti (4 e 12,
172 e 165 colpi) sono negativi. **La conclusione aggregata non dipende da lui**
— togliendolo restano **14 su 14** con mediana +2,61, su **14 esecuzioni e 3
batteristi** `[MIS]` — ma chi usa quel file come template sappia che su di lui
la stratificazione **non c'è**.

⚠️ **E questo CONFERMA metà dell'`[IPO]` del comune, non lo smentisce.** «Ma
swing e laid-back non sono la stessa cosa» riporta da `music-composition` un
pocket a strati con *«cassa sul tempo, rullante appena dietro, charleston
appena avanti»*. Il **charleston appena avanti c'è**, ed è la cosa più solida
che questa casella misuri.

Quello che **non** si trova è il resto — e va detto con precisione, perché il
numero e il verbo qui vanno letti insieme. Il **rullante dietro alla cassa**
c'è **come segno**: la mediana è +0,22 tick, e positivo vuol dire dopo. Ma non
c'è **come sistematicità**, che è quel che servirebbe per chiamarlo uno strato:
succede in **11 casi su 21**, cioè testa o croce, e vale un **quarto di tick**
contro i 2,59 che separano il piede dal ride. Un segno giusto senza
sistematicità non è un pocket. Fra i tre strumenti battuti, insomma, non c'è
ordine, e il pocket a strati del jazz è **un solo strato**: il piede.

#### Cosa esclude il test del tempo — e cosa no

⚠️ **Prima di cuocere quei 2,6 tick in un template.** Su un kit elettronico un
divario sistematico fra due pad può venire dall'elettronica e non dal
batterista — e nei due versi: o il piede che scatta presto, o i tre pad battuti
che rispondono tardi. Una parte della domanda i dati la chiudono, un'altra no,
e le due vanno tenute separate.

**La fisica, scritta giusta.** Un tick dura `60000/(BPM × 96)` ms, quindi si
**accorcia** al salire del tempo. Ne segue che una latenza **fissa** di `D`
millisecondi vale `D × BPM × 96 / 60000` tick: è proporzionale al BPM e in tick
**cresce** al salire del tempo — 20 ms sono **3,04 tick a 95 BPM** e **6,88 a
215**. Una scelta musicale è invece una frazione del movimento: **costante in
tick**, e in millisecondi cala.

L'argomento portante è una **regressione**, non tre mediane — le fasce sono un
raggruppamento arbitrario, e la loro piattezza potrebbe essere fortuna di
composizione — ed è fatta sul **divario appaiato**, non sui livelli. Il motivo
è la riga qui sopra: dopo `GR.origine()` il livello di ogni esecuzione ha uno
**zero arbitrario**, quindi una pendenza sui livelli confonde; la *differenza*
fra due strumenti della stessa esecuzione quell'offset lo cancella per
costruzione, ed è l'unica grandezza definita.

⚠️ **E la tabella qui sotto è scritta al contrario di quella delle coppie**,
perché il charleston fa da riferimento: si legge **pad meno charleston**,
quindi il segno **positivo** dice che quel pad arriva **dopo** il piede. È lo
stesso fatto letto dall'altro capo — «ride − charleston = +2,59» e «charleston
− ride = 2,59 tick prima» sono la stessa riga, non due misure.

Le due ipotesi fanno previsioni **opposte** sul divario: se è una frazione del
movimento la pendenza è **zero**; se è una latenza fissa in millisecondi la
pendenza vale `ms × 96/60000` ed è **dello stesso segno del divario**, cioè
positiva. Su `beat` 4/4 senza funk e fusion `[MIS]`:

| divario | esec. | batt. | mediana | pendenza misurata | da costante-in-tick | da latenza fissa |
|---|---|---|---|---|---|---|
| ride − charleston | 15 | 3 | +2,59 tick (+13,0 ms) | **−0,0055 ± 0,0066** | **0,8 σ** | +0,0207 → **4,0 σ** |
| kick − charleston | 18 | 2 | +2,23 tick (+9,8 ms) | −0,0245 ± 0,0103 | 2,4 σ | +0,0156 → **3,9 σ** |
| rullante − charleston | 22 | 3 | +1,38 tick (+7,3 ms) | −0,0342 ± 0,0114 | 3,0 σ | +0,0117 → **4,0 σ** |

**La latenza fissa in millisecondi è rifiutata a circa 4 σ su tutte e tre le
coppie**, e non di poco: la pendenza misurata ha il **segno opposto** a quella
prevista. Il divario ride/charleston è inoltre **indistinguibile da costante in
tick** (0,8 σ), che è la firma di una grandezza proporzionale al movimento.

Per le altre due coppie non regge nessuna delle due ipotesi pure: il divario si
**restringe** al salire del tempo (2,4 e 3,0 σ da zero). Detto per intero:
quel che i dati rifiutano è netto, quel che affermano vale solo per la coppia
ride/charleston.

⚠️ **Qui sotto la grandezza CAMBIA, e il segno con lei.** La tabella per fascia
di tempo non porta un divario: porta il **livello del solo charleston a
pedale**, cioè il suo residuo dopo `GR.origine()` — la stessa colonna «mediana»
della tabella del residuo in cima a questa casella. È per questo che i numeri
sono **negativi** mentre i divari qui sopra sono positivi: negativo vuol dire
**prima della griglia**, ed è il piede che anticipa. Chi la leggesse come un
divario che si rovescia leggerebbe il contrario di quello che c'è scritto.

Il **livello del charleston a pedale** per fascia di tempo, con i conteggi che
mancavano `[MIS]`:

| fascia | esecuzioni | batteristi | charleston, tick (mediana) | (media) | dev. standard | errore standard |
|---|---|---|---|---|---|---|
| ≤ 110 BPM | 6 | 3 | −3,39 | −3,92 | 1,75 | 0,72 |
| 110-130 BPM | 8 | 3 | −3,32 | −3,42 | 1,87 | 0,66 |
| > 130 BPM | 9 | **2** | −3,39 | −2,92 | 1,99 | 0,66 |

⚠️ **E si guarda, non si conclude.** Un livello ha lo zero arbitrario detto
qui sopra, quindi da questa tabella non esce nessuna prova: la conclusione la
porta la regressione appaiata, che è sul divario. Questa tabella sta qui per
mostrare il **rumore** che c'è sotto, ed è tutto quello che le si può chiedere
— **le tre mediane vanno lette per quello che sono.** Coincidono a 0,07 tick,
ma l'errore standard è **0,66-0,72 tick**: l'accordo è **un decimo del
rumore**, cioè una coincidenza e non una precisione — e infatti le *medie*
delle stesse fasce si muovono di un tick pieno (−3,92 → −3,42 → −2,92). La
fascia che porta la discriminazione, poi, sono **due batteristi**. È la
regressione appaiata a reggere la conclusione, non questa tabella. E la
colonna in millisecondi che compariva qui in una versione precedente **non era
un secondo riscontro**: è `tick × 60000/(BPM × 96)`, aritmetica sugli stessi
numeri.

**Cosa il test esclude, detto stretto:** che il divario fra il charleston e gli
altri pad sia un ritardo **costante in millisecondi**. Nient'altro — su **tutte
e tre** le coppie; su due delle tre cade anche l'ipotesi opposta, ed è la riga
qui sopra.

⚠️ **E non esclude un pedale proporzionale al movimento** — quello sì, ma solo
quello, e va detto **nel verso giusto**, perché è dove questa casella ha già
sbagliato una volta. Il charleston a pedale **anticipa**: un pad che *ritarda*
non lo spiegherebbe, lo **contraddirebbe**. Il meccanismo dovrebbe essere
l'altro, e da qui in poi si **suppone** `[IPO]`: il «chick» non scatta a fine
corsa ma quando la corsa del pedale **supera una soglia**, cioè a un punto
*dentro* il gesto del piede, e l'onset cade presto. Perché ne venga un anticipo
**costante in tick** servono però **due** supposizioni, non una — che quel punto
cada a una frazione **fissa** del gesto, e che il gesto sia una frazione della
**battuta** e non una durata sua, mentre molla e massa di un pedale col tempo
non scalano. **Quel pedale non è mai stato misurato.**

⚠️ **E i numeri già scritti qui sopra lo stringono ancora.** Il charleston è il
riferimento comune di tutte e tre le regressioni, quindi un effetto
costante-in-tick dal **suo** lato prevede pendenza **zero su tutte e tre**: è
0,8 σ sul ride, ma **2,4 e 3,0 σ** su cassa e rullante — le stesse due coppie
per cui, più sopra, «non regge nessuna delle due ipotesi pure». **Due
su tre respingono anche questa versione.** E un pedale che scattasse presto di
un numero **fisso di millisecondi** è già rifiutato a ~4 σ dalla stessa
regressione, esattamente come i pad battuti. La domanda del titolo — mestiere o
pedale — resta quindi **senza risposta**, ma del pedale sopravvive **una
versione sola, supposta, e su una coppia su tre**.

⚠️ **E il confronto è sempre e solo fra pad.** `GR.origine()` toglie già lo
scarto comune a tutto il kit, quindi qui si esclude una latenza **di quel pad
rispetto agli altri** — mai una latenza di cattura della registrazione, che
essendo comune a tutti è **invisibile per costruzione**.

⚠️ **E prima di tutto: 13 ms.** Il divario ride/charleston, che è il più largo
dei tre, in millisecondi vale **13,0 ms** — cioè **sotto** la finestra di 20-40
ms che il comune dichiara udibile. È l'unica grandezza di questa sezione che
con quella finestra si possa confrontare, per la ragione detta più in alto: gli
altri numeri sono livelli, e un livello ha lo zero arbitrario. La
stratificazione è **misurata bene e piccola**: che si senta è un'altra
affermazione.

⚠️ **E dal 24 agosto 2026 quella finestra va maneggiata con due cautele.** La
prima: i 13,0 ms sono un divario **fra due strumenti**, cioè una grandezza
*relativa*, mentre la finestra qualifica **uno** spostamento contro la griglia.
Sono due domande diverse, e il comune ora le tiene separate — «Le due domande
sono diverse, e la soglia dipende dal tempo». Che la stratificazione si senta
**non è stato provato**: i 13,0 ms non sono mai stati messi davanti a un
orecchio, e gli ascolti del 24 agosto (qui sotto) non permettono di dedurlo,
perché da lì **non esce nessuna soglia**.

La seconda, che è più insidiosa: **i 13,0 ms non sono un numero, sono 2,59 tick
letti a un tempo.** Sono la conversione fatta col BPM di ciascuna esecuzione — è
detto qui sopra — e la stessa quantità **scritta** in una song vale altri
millisecondi: 2,59 tick sono 8,8 ms a 185 BPM, **16,2 a 100**, 27 a 60. Cioè
**se la stratificazione misurata si senta dipende dal tempo a cui la si scrive**,
non solo da quanto è grande; e a 185 BPM, il tempo dell'esecuzione da cui il
template viene, sarebbe la metà.

#### Due grandezze diverse, e la domanda che resta aperta

⚠️ **Le mediane aggregate non sono quello che un template scrive**, e
confonderle sarebbe comodo e falso. Le mediane qui sopra stanno entro 3,4 tick
perché sono **mediane su decine di esecuzioni**; il profilo di **una**
esecuzione porta invece uno scarto **per ogni passo e per ogni strumento**, e
`MU.applica_groove()` li applica **tutti**, senza nessuna soglia.

Sul template raccomandato, quindi `[OSS]`:

- il **massimo spostamento singolo** è **+11,80 tick = 39,9 ms** a 185 BPM
  (ride, passo 13). Confrontato con la finestra 20-40 ms del comune — che
  qualifica *uno* spostamento, ed è quindi la grandezza giusta da metterle
  accanto — sta al suo **bordo superiore**: è quanto di più grande quella
  finestra chiami ancora microtiming, non il minimo che chiami udibile;
- l'**escursione picco-picco** fra tutti i passi e tutti gli strumenti è
  **22,83 tick = 77,1 ms**. Ma è la distanza fra il colpo più anticipato e il
  più ritardato del kit, non uno spostamento: a nessuna nota viene applicata.

⚠️ **E gli estremi poggiano su 1-3 colpi.** I cinque scarti più grandi vengono
da passi colpiti **una volta sola** (ride passo 13, charleston passi 5 e 14,
rim passo 9) o tre (rullante passo 1) su **193 battute** `[OSS]`. Non sono
feel: sono il colpo isolato di un batterista che si sposta, misurato come se
fosse una regola. Chi costruisce un template farebbe bene a **guardare i colpi
prima dello scarto** — `GR.profilo()` li riferisce — perché `applica_groove()`
non distingue fra un passo da 172 colpi e uno da 1.

**E se non si sentisse affatto?** Era la domanda che questa casella non poteva
chiudere. I 39,9 ms del colpo estremo sono nella finestra udibile, ma poggiano
su un colpo solo; la stratificazione che è **misurata bene** vale 13 ms, cioè
**sotto** quella finestra. «Rappresentabile» non è «percepibile». **Se
all'ascolto il residuo non si fosse distinto**, il valore di
`MU.applica_groove()` sarebbe stato tutto nella **velocity** — la metà che non
dipende dalla posizione, e che la scala e il profilo posizionale qui sopra
sostengono da sole. Non è andata così, e la risposta arrivata il 24 agosto 2026
non è né un sì né un no: è la sezione qui sotto.

#### Cosa si è sentito, e cosa non se ne può dedurre — gli ascolti del 24 agosto 2026

**Cosa è stato ascoltato.** Una coppia controllata di due battute a 100 BPM,
`GROOVE0` e `GROOVE1`: stesso pattern, stesso kit, stesso swing, **identiche
riga per riga fuori dalle note**. `GROOVE1` porta il template di
`drummer1/session3/2` posato con `MU.applica_groove()` su quattro voci — ride,
charleston a pedale, cassa, rullante — e `GROOVE0` lo stesso pattern con le
velocity mediane della tabella in cima a questa casella, così che la differenza
fra i due file non fosse dominata dalla dinamica. **Un ascoltatore, tre ascolti
col metronomo acceso, più una quarta prova che l'ascoltatore ha fatto da sé**
`[OSS]`. La coppia si rigenera con
`tools/genera_groove.py`, che stampa i due file nota per nota e il loro
confronto. Che il dispositivo **conservi** quelle posizioni è un'altra
affermazione e sta nella casella 10: qui c'è **solo quello che si sente**.

| ascolto | la grandezza, **in tick** | a 100 BPM | esito |
|---|---|---|---|
| il giro intero, `GROOVE0` poi `GROOVE1` | tutto insieme | — | *«sento e vedo variazioni di velocity tra le note e variazione di timing delle note (dove cadono)»* |
| sola cassa contro sola linea di ride | **4 tick** di sfasamento fra due voci che nell'altro file cadono insieme | 25 ms | *«la cassa sul levare è anticipata rispetto al ride»* — **sentito, e attribuito allo strumento giusto** |
| sola riga del pedale contro il click | **3 tick** di anticipo di una voce sola sulla griglia, su tutti e quattro i suoi colpi | 18,75 ms | *«cadono sul click»* — **l'ascoltatore non lo distingueva**, ed è l'esito che ha poi corretto da sé, qui sotto |

L'ultima colonna è **quello che una persona ha riferito di sentire**, non una
misura: quanto ci si possa appoggiare sopra è scritto due sezioni più giù, ed è
meno di quanto sembri.

⚠️ **Le grandezze di questa sezione si dicono in tick, e i millisecondi sono una
conversione dichiarata a un tempo nominato.** Il residuo che
`MU.applica_groove()` scrive è **in tick**, cioè una frazione del movimento: un
tick vale `60000/(BPM × 96)` ms — 6,25 a 100 BPM, 3,38 a 185. Presentare i
millisecondi come *la* grandezza fa sembrare fisso qualcosa che si muove col
tempo, ed è esattamente l'errore che la correzione qui sotto ha smascherato.

⚠️ **Le tre domande erano binarie, e portavano dentro le parole della
risposta** — «volume o dove cadono?», «prima del ride o insieme?», «sul click o
appena prima?». Chiedere così suggerisce, e un ascoltatore compiacente
direbbe sempre di sì. Quel che le rende comunque informative è che **non ha
detto sempre di sì**: alla stessa forma di domanda ha risposto due volte «c'è»
e una volta «no». E la volta del «no» non se l'è tenuta: è andato a rifare
l'esperimento in altre condizioni, che è il contrario dell'ascoltatore
compiacente. Che le domande andassero fatte **aperte** resta un difetto di
questa sessione, ed è registrato nel comune, «Un ascolto non è una misura di
percezione».

##### La correzione, arrivata dall'utente e non richiesta

L'ascolto 3 sembrava chiuso. L'utente ha rifatto la prova rallentando il tempo,
e ha riferito:

*«però il punto 3 è un problema di percezione umana: difficile percepire
variazioni di ms. Se rallento molto i BPM sento open HH anticipato rispetto al
click, ma devo rallentare a 15 BPM.»*

La riga del charleston aperto porta **−3 tick esatti** su tutti e quattro i suoi
colpi — posizioni 93, 285, 477, 669 — e tre tick valgono `1875/BPM`
millisecondi:

| BPM | 3 tick valgono | esito |
|---|---|---|
| 185, il tempo dell'esecuzione da cui il template viene | 10,1 ms | mai provato |
| **100**, il tempo della coppia | **18,75 ms** | **non sentito** |
| 60 | 31,3 ms | mai provato |
| 47 | 39,9 ms | mai provato |
| **15** | **125 ms** | **sentito** |

⚠️ **Cosa cambia, ed è molto.** L'ascolto 3 a 100 BPM **non ha misurato
l'assenza dello scarto**: ha riferito che a quel tempo l'ascoltatore non lo
distingueva. Lo scarto c'è, sta nel file, sopravvive al salvataggio del
dispositivo — la casella 10 lo prova, 31 posizioni su 31 — e **si sente quando
lo si amplifica abbastanza**. «Non si sente» non è una proprietà del template:
la frase vera è **«a 100 BPM chi ascoltava non lo distingueva»** `[OSS]`.

⚠️ **Ed è caduto un argomento che questa casella aveva scritto il giorno
stesso.** Diceva che la riga del pedale era stata ascoltata «nella condizione
più favorevole che esista, una riga sola contro un click». Non era la più
favorevole: **mancava il tempo**. Un ascolto che vuole sapere se uno scarto è
percepibile ha **due** manopole, non una — l'isolamento e il tempo — e quel
giorno la seconda non era stata girata.

**È anche la più solida delle quattro risposte**, e per una ragione che non
dipende dall'orecchio di nessuno: non chiede di discriminare un millisecondo,
chiede di sentire la stessa differenza **amplificata 6,7 volte**. Che a 15 BPM
l'anticipo si senta dimostra che lo scarto è **davvero scritto e davvero
suonato** — che è quello che il cancello doveva stabilire.

##### Cosa NON se ne ricava: nessuna soglia — 24 agosto 2026

⚠️ È l'ascoltatore stesso a declassare i propri risultati, e ha ragione:

*«Considera che variazioni di pochi ms sono difficili da percepire
consapevolmente da un umano, soprattutto con un orecchio poco allenato come il
mio. Non credo che la differenza tra le mie risposte a 2 e 3 sia una "soglia". A
questo livello di dettaglio tutte le mie valutazioni sono imprecise.»*

Questa frase **è un dato**, e sta qui verbatim come le altre tre. Le ragioni
sono due, e la seconda è la più forte:

1. **gli ascolti 2 e 3 non sono lo stesso compito percettivo.** Il 2 confronta
   due voci che suonano insieme; il 3 confronta una voce con un riferimento
   esterno. Sono due domande diverse fatte all'orecchio, e la sensibilità
   dell'una non si trasporta all'altra: metterle in fila per dedurne un punto
   di passaggio **non era valido nemmeno prima** della prova a tempo lento;
2. **chi ascoltava dichiara la propria imprecisione.** Un ascolto, una persona,
   **nessuna ripetizione, nessuna prova alla cieca**, e per sua stessa ammissione
   un orecchio non allenato a discriminare millisecondi. Non toglie valore a ciò
   che ha **riferito**; toglie valore a ciò che se ne può **dedurre**.

Quindi da qui **non esce nessuna soglia**: né quella dello sfasamento fra due
voci, né quella dello spostamento contro un riferimento, né una loro differenza.
E la finestra **20-40 ms** che il comune dichiara `[WEB]` **resta dov'era**:
questi ascolti non la confermano e non la contraddicono, perché per toccarla
servirebbe una misura di percezione e questa non lo è.

**Quel che resta stabilito, e non è poco:** che le due domande — sfasamento fra
voci e spostamento contro un riferimento — sono **diverse e vanno poste
separate**; e che un residuo scritto **si sente, quando è abbastanza grande**.
**Quanto grande** è precisamente ciò che non è stato stabilito, e non lo
stabilirà un ascolto in più: servirebbe un protocollo diverso — **ripetizioni,
ordine casuale, ascolto alla cieca** — cioè un esperimento di psicoacustica, non
un'altra sessione al Deluge. È scritto qui come **ciò che manca**, non come una
lacuna da colmare in fretta: il progetto può comporre benissimo senza saperlo,
purché non finga di saperlo. Le due regole generali che ne escono stanno nel
comune di [`../MUSICA.md`](../MUSICA.md) — «Un ascolto non è una misura di
percezione» nel metodo, e «Le due domande sono diverse, e la soglia dipende dal
tempo» nel mestiere.

⚠️ **E niente di tutto questo tocca l'esito che si vede.** Che il dispositivo
conservi le 31 posizioni su 31 è **meccanico**, si legge nei byte, e sta nella
casella 10: le riserve di questa sezione riguardano l'orecchio, non il file.

`[IPO]` **E una cosa che si ragiona, non che si è ascoltata.** Dentro un pezzo
il click non c'è: il riferimento di una voce sono **le altre voci**. Uno
spostamento «assoluto» di una riga sola, in una tessitura, torna quindi a essere
una domanda *relativa* — contro gli altri strumenti — e l'assoluto puro esiste
solo contro un metronomo, o contro un pulso già in testa a chi ascolta. Se è
così, la grandezza che conta per un groove template è quella fra le voci; ma è
un ragionamento, e finché resta tale porta il suo marcatore.

**Le previsioni, e come sono andate.** Erano scritte **prima** dell'ascolto, nel
rapporto con cui la coppia è stata costruita, quindi non sono riscrivibili
adesso:

- previsione 2 — *«il residuo di posizione, sul giro intero, non si
  distinguerà»* — **smentita**, ed è la cosa più utile di tutto l'esperimento.
  La domanda offriva un'alternativa — volume **o** posizione — e l'utente ha
  nominato **tutt'e due**, che è più di quanto la domanda gli desse. Chi aveva
  previsto sapeva che le separazioni sui colpi forti valgono 6-12 ms e che
  quelle da 25 ms cadono su colpi isolati: i numeri erano giusti, la conclusione
  che ne aveva tratto no;
- previsione 3 — la riga del pedale, data per **incerta**, con un «forse» come
  esito atteso — **a 100 BPM** si è risolta in un **no netto**: *«cadono sul
  click»*. Il rapporto la chiamava «il risultato più informativo dei tre», e su
  una cosa aveva ragione: lì il timing è quasi l'unica cosa che cambia. Ma
  **informativo su che cosa** era sbagliato — non sul template, sul **tempo**;
  e a scoprirlo non è stato chi aveva previsto;
- previsione 1 — la differenza dinamica si sente — **confermata**, e non è una
  notizia: serviva a sapere che metà della risposta dell'utente non riguardava
  la domanda;
- la previsione 4 riguarda quello che si **vede**, non quello che si sente, e
  sta nella casella 10.

**Che una previsione sia stata smentita vale più che averla azzeccata**, e va
letto così: se la 2 fosse andata come previsto, questa casella oggi
concluderebbe che `MU.applica_groove()` vale per metà — la velocity — e che la
posizione è rappresentabile e non percepibile. Non è andata così: la posizione
si sente, quando è grande abbastanza, e **quanto grande dipende anche dal tempo
a cui la si scrive**.

E vale **due volte in più**, sulle conclusioni che questa sezione aveva scritto
il giorno stesso: le ha corrette **l'utente**, prima rifacendo un esperimento
che nessuno gli aveva chiesto di rifare, poi dicendo che le sue stesse risposte
non reggono il peso che ci era stato messo sopra. Le versioni stanno qui tutte
apposta — prima *«non si sente»*, poi *«a 100 BPM non lo distinguevo»*, infine
*«a questo livello di dettaglio tutte le mie valutazioni sono imprecise»* —
perché in questo progetto le correzioni venute dall'ascolto si conservano con la
data, non si sostituiscono in silenzio.

**Cosa resta aperto**, perché il passo dopo è già nominato:

- **quanto grande debba essere un residuo perché si senta.** Non lo sappiamo, e
  **non lo chiuderà un ascolto in più**: servirebbe ripetere, mescolare
  l'ordine, ascoltare alla cieca. Il tempo resta l'asse comodo per amplificare —
  a 60 BPM 3 tick valgono 31,3 ms, a 47 ne valgono 39,9, cioè i due bordi della
  finestra del comune — ma la manopola da girare per prima è il **protocollo**,
  non il metronomo;
- **se la stratificazione misurata si senta.** I **13,0 ms** del divario
  ride/charleston non sono mai stati messi davanti a un orecchio, e per quanto
  detto qui sopra non basterebbe metterceli una volta;
- **la stratificazione non è mai entrata in gioco.** Il template ascoltato è
  `drummer1/session3/2`, che di stratificazione ne ha **+0,08 tick** — il caso
  estremo minimo della fila, come questa casella già dichiara più sopra: su
  quel file la stratificazione non c'è, quindi l'ascolto non poteva né
  confermarla né smentirla. La coppia da fare adesso è su
  **`drummer10/session1/1`** (`jazz/swing`, 124 BPM, 164 s, BUR 1,82): sui passi
  4 e 12 il suo charleston a pedale sta a **−5,51 e −5,82** tick e il ride a
  **−1,48 e −2,18**, cioè **4,03 e 3,64 tick di divario** sui due passi più
  colpiti di ogni battuta, contro i +0,29 della stessa misura su
  `drummer1/session3/2` `[OSS]` su due esecuzioni. E lì il ride **è** `ride`
  (219 colpi, spang-a-lang su 0-4-6-8-12-14): niente trappola del nome GM.

### Lo swing non sta in questa casella

Il **BUR** — dove cade il levare dentro il movimento — è *feel*, non dinamica,
e vive nella **casella 4**, che ora lo misura su due corpora. Qui non è
ricopiato di proposito: un numero vive in una casella sola, e il valore da
scrivere sul dispositivo lo converte la casella 10.

### Come si usa

Il template si legge da **una esecuzione nominata** e si posa su un pattern:

```python
prof = GR.profilo(base, 'drummer1/session3/2')     # jazz/swing, 185 BPM
note = MU.passi('....x.......x...')                # il piede sul 2 e sul 4
MU.applica_groove(note, prof, dove='charleston a pedale')   # muta `note`
```

`applica_groove()` **muta la lista** e ritorna il rapporto, non le note; e
**non inventa**: se il pattern chiede un colpo su un passo dove quel batterista
non ha mai suonato, la nota resta com'è e il passo finisce in
`senza_appoggio`, che va letto.

L'esecuzione da cui il template esce va **nominata**, perché quello che ne
viene è `[OSS]` su un esecutore e non `[MIS]` su un repertorio: mediare il
microtiming di batteristi diversi lo tirerebbe verso la griglia, cioè verso
zero, perdendo esattamente ciò che si era andati a prendere. La più lunga fra
le `jazz/swing`, `beat`, 4/4 è **`drummer1/session3/2` — `drummer1`,
`jazz/swing`, 185 BPM, 250 s, 193 battute, BUR 1,49** `[OSS]`.

⚠️ **Il nome GM non è il ruolo musicale, e su questa esecuzione inganna.** Il
disegno continuo di crome swingate — il ride, musicalmente — sta per otto
decimi dell'esecuzione sulla nota **43**, che la mappa GM chiama `tom basso`
(**805 colpi**), e solo nel quinto centrale sulla nota **51**, `ride` (**238
colpi**). Le due **si scambiano il disegno** in una transizione di **26
battute** su 193 — 142 battute portano la sola 43, 20 la sola 51, e solo 10
hanno almeno due colpi di ciascuna — **senza mai raddoppiare lo stesso colpo**
(zero simultaneità esatte; 55 dei 238 colpi di `n51` hanno una `n43` entro una
croma) `[OSS]`. Chi scrive `dove='ride'` prende quindi il profilo di un quinto
di esecuzione, non il disegno del pezzo. La voce si sceglie **dal numero di
colpi e dalla posizione** che `GR.profilo()` riferisce, mai dal nome — e per
un pattern di ride jazz scritto da zero è più sicuro il profilo **aggregato**
della tabella qui sopra, che sta su 18 esecuzioni e 4 batteristi.

Lo **swing** non è nel template: lo fa `S.set_swing()`, che è di song. Il
template porta il solo residuo. La casella 10 dice quale valore e su quale
figura.

## 7. Armonia

**Parziale.** C'è il **vocabolario**, ed è completo: `MU.armonia()`,
`MU.voci()`, `MU.sigla()`, i quattro voicing di `MU.VOICING` — `chiuso`,
`shell`, `senza-fondamentale`, `drop2` — e il dialetto di Weimar, che
`WJ.sigla_weimar()` scioglie **per intero, senza fallimenti**. Manca **la
condotta delle parti**: ogni accordo è costruito per conto suo, e i voicing
alternati A/B del ii-V-I non sono implementati — cioè manca esattamente quello
che fa suonare un comping invece di una fila di accordi. Come ci si è arrivati,
e che cosa copre la grammatica delle sigle, sta in
[`../../HANDOFF.md`](../../HANDOFF.md) §6-octies; quanti simboli distinti siano
stati sciolti, e su quante occorrenze, in §6-nonies. **La chiuderebbe
`assets/jazz-voicings.md` di `music-composition`**, che è già la fonte da cui i
voicing vengono e che l'alternanza A/B la specifica: qui manca implementarla,
non trovarla.

*Nel frattempo, per comporre:* si scrivono le **altezze a mano**, con
`MU.accordi()`, leggendole da `assets/jazz-voicings.md` di
`music-composition` — la fonte già nominata qui sopra, raggiunta dal suo
`references/00-navigation.md` — e `[WEB]` a quello che ne esce. **Non** con
`MU.armonia()` cambiando `voicing=`: `MU.VOICING` ha **una sola** forma senza
fondamentale (3-5-7-9, cioè la sola «A») e `voci()` la restituisce sempre
ascendente, quindi la «B» non esiste e nessun argomento la produce. Un secondo
voicing scelto lì — `chiuso`, `drop2` — sarebbe un'alternanza **inventata**,
non quella del documento, ed è esattamente ciò che questa riga esiste per
impedire.

## 8. Melodia e ornamentazione

**Vuota, ed è la più vicina a chiudersi.** `wjazzd.db` è esattamente questo —
assoli trascritti a mano con **gli accordi allineati alla linea**, e quanti
siano lo dice [`../../HANDOFF.md`](../../HANDOFF.md), «La decisione sui
formati simbolici» — ed è già su disco e già leggibile con `WJ.melodia()` e
`WJ.armonia()`. Manca solo guardarlo per lo sviluppo motivico invece che per
lo swing.

*Nel frattempo, per comporre:* si guarda **un assolo solo** del corpus che è
già in casa — `WJ.elenco(db, style=…)` per sceglierlo, `WJ.melodia()` e
`WJ.armonia()` per leggerlo — e quello che se ne ricava è `[OSS]` su un
assolo, non `[MIS]`: un assolo è un musicista, non un repertorio. Se
`wjazzd.db` non c'è, e non è versionato, la domanda va **alla skill**:
`melody/motivic-development.md`, dal `references/00-navigation.md`, segnando
`[WEB]`.

## 9. Forma e densità

**Parziale.** Della **forma** non c'è ancora niente — AABA, il blues di dodici
battute, il rhythm changes — e la chiuderebbe MusicXML o le lead sheet, con la
stessa avvertenza della casella 5: il lettore va scritto, non procurato. Ci
sono invece **i fill**, misurati: quanto sono densi, quanto durano e con quali
strumenti si fanno.

### I fill, misurati — 18 agosto 2026

Il Groove MIDI etichetta ogni esecuzione `beat` o `fill`, e del jazz porta
**51 fill**, tutti in 4/4. Sono un animale diverso dai `beat`, ed è la ragione
per cui `GR.scala()` ha `beat_type='beat'` come default: mescolarli alzerebbe
le code senza dire niente di nessuno dei due.

⚠️ **Prima del numero, chi lo ha suonato: i 51 fill sono due batteristi**,
`drummer1` con **44** e `drummer7` con **7** `[OSS]`. I numeri qui sotto sono
aggregati su 51 esecuzioni e restano perciò `[MIS]` — ma con due soli
esecutori contro i cinque dei `beat` descrivono **quei due**, e generalizzarli
al jazz è un passo che il corpus non paga. Vale qui la stessa cautela che la
casella 6 mette sul dominio di `drummer1`, moltiplicata.

**Un fill dura una battuta.** Mediana **0,93 battute** (min 0,73, max 2,00):
non è una figura di due o quattro battute, è il buco di una battuta sola
`[MIS]`.

**E non è un fuoco d'artificio.** Colpi per battuta, contro le 48 esecuzioni
`beat` 4/4 `[MIS]`:

| | esecuzioni | batteristi | colpi/battuta (mediana) | q1-q3 |
|---|---|---|---|---|
| `fill` | 51 | 2 | **15,7** | 12,6-19,0 |
| `beat` | 48 | 5 | **12,9** | 11,1-14,2 |

Cioè **un quinto più fitto**, non il doppio. Chi generasse un fill jazz
raddoppiando i colpi sarebbe già fuori dal corpus.

**Quello che cambia davvero è chi suona.** La quota dei colpi per strumento
`[MIS]`:

| strumento | nei `beat` | nei `fill` |
|---|---|---|
| ride | 20,4% | **3,3%** |
| tom basso + tom medio-alto | 9,9% | **29,0%** |
| rullante | 30,8% | 40,3% |
| kick | 16,1% | 8,1% |

**Il fill è dove il ride si ferma e arrivano i tom.** Il ride passa da un colpo
su cinque a uno su trenta, i tom triplicano. È questa la firma del fill, non
la densità.

**E non alza la voce.** Ogni mediana con le esecuzioni che la sostengono — che
sono meno delle 51 della delimitazione, perché non tutti i fill portano tutti
gli strumenti — e 2 batteristi in ogni riga `[MIS]`: rullante **42** su **48**
esecuzioni, tom basso **67** su **43**, cassa **40** su **29**. Tutte e tre
stanno **sotto** la mediana dello stesso strumento nei `beat`: per rullante e
cassa il confronto è con la tabella della casella 6, per il tom basso — che lì
non compare perché la tabella porta i cinque strumenti portanti — la mediana
`beat` è **81**, su **38 esecuzioni e 5 batteristi** `[MIS]`. Un fill jazz non
è un crescendo: è un cambio di strumento a volume uguale o minore. Il tom in
particolare scende proprio perché cambia ruolo — nei `beat` compare di rado e
come accento, nei fill è la voce corrente.

### Cosa manca ancora

**Dove va un fill non lo dice il corpus.** Il dataset consegna i fill come file
separati, staccati da qualunque esecuzione: quanto spesso ne vada uno — ogni
quattro battute, ogni otto, sul turnaround — è esattamente ciò che non c'è, e
non è ricavabile da qui. Manca cioè tutta la **scala lunga**: le forme (AABA,
blues di 12, rhythm changes), quante volte si gira, dove cadono i fill dentro
il giro, e l'arco di densità del pezzo.

*Nel frattempo, per comporre:* la **forma** la sceglie quasi sempre l'**utente**
nominando il pezzo — «un blues», «un rhythm changes» — e allora è decisa e non
c'è niente da cercare. Se non la nomina, la domanda va **alla skill**:
`form/popular-song-forms.md`, dal `references/00-navigation.md`, che ha la
sezione AABA e quella del blues di 12 battute; `[WEB]` a quello che ne esce.
La **collocazione** dei fill dentro la forma va decisa lì, non qui. La
**densità** invece non è di repertorio: la scala 1-9 e i tempi oltre i
quali l'ascoltatore si stacca stanno nel comune, «L'arco di densità», e si
usano da subito.

## 10. Sul Deluge

**Parziale.** C'è **quanto** swing e **su quale figura**. Le cose di questo
repertorio che sono passate per un Deluge sono **tre**, e in tutto il jazz sono
le sole — ma non hanno lo stesso grado, e vanno contate separate.
**Verificati sul dispositivo sono due meccanismi**: che il display sia la
percentuale di posizione del levare e che `swingInterval` scelga quale figura
viene swingata; e — dal 24 agosto 2026 — che il dispositivo **conservi le
posizioni fuori griglia** che il groove template scrive, «Il Deluge non
riquantizza», qui sotto.

**Il terzo è di un altro genere: i primi due si vedono, questo si è sentito.**
Il 24 agosto 2026, su una coppia costruita apposta, **togliere lo swing dalle
posizioni e farlo rimettere al firmware non ha prodotto una differenza
udibile** `[OSS]`. ⚠️ **Non si scrive «verificato sul dispositivo», e non è
pedanteria.** Un ascoltatore, una sessione, nessuna ripetizione, nessuna prova
alla cieca: quel che regge in modo forte è l'**esclusione** dei modelli di
firmware che avrebbero prodotto differenze grosse, e quella non chiede
all'orecchio nessuna finezza — chiede solo che un ride raddrizzato si sarebbe
notato. Che non si senta **nessuna** differenza è invece osservato, e un
modello resta in piedi. È la stessa separazione che «Il Deluge non riquantizza»
fa già dentro di sé, presa nei due versi: non dire «verificato sul dispositivo»
avendo ascoltato, né il contrario. La coppia, i sei modelli del firmware, la
previsione scritta prima dell'ascolto e quel che resta aperto stanno nel comune
di [`../MUSICA.md`](../MUSICA.md), «Il groove template» — «Togliere lo swing e
rimetterlo torna a zero — ma contro sé stesso»: è meccanismo di macchina e non
del jazz, quindi qui il rimando e non la copia.

Il **62** no: è aritmetica sul meccanismo dello swing a partire dal BUR
misurato sul corpus Weimar, e nessuno l'ha ancora **giudicato** — è uscito da
un Deluge il 24 agosto 2026, ma su di lui non è stata fatta nessuna domanda, e
in fondo a questa casella c'è perché, insieme all'unico 62 che quel giorno una
domanda l'ha avuta, e che non è questo. Serve
`S.set_swing(doc, 62, figura='1/8')`, perché il default del firmware swinga le
semicrome e su una linea di crome non muove niente. Come funziona la scala — la
formula fra display e BUR, e quale `swingInterval` nomina quale figura — sta nel
comune, «Il meccanismo dello swing». Qui ci sono i valori del jazz, convertiti
dai BUR della casella 4:

| repertorio | `set_swing(doc, …, figura='1/8')` |
|---|---|
| dritto | 50 |
| **jazz complessivo** | **62** |
| HARDBOP · BEBOP | 64 |
| POSTBOP | 60 |
| FUSION | 56 |
| terzina esatta | 67 |

⚠️ **Questa tabella converte il BUR di Weimar, e da oggi non è più l'unico.**
La casella 4 ne misura un secondo sul Groove MIDI: sul kit intero **1,48**, sul
solo ride **1,99** — i due numeri sono `[MIS]` **lì**, con le loro esecuzioni e
i loro batteristi, e qui c'è solo la conversione, che è aritmetica sulla
formula del comune: display **60** e display **67**, la terzina.

I valori della tabella restano quelli di Weimar perché è la misura più larga, e
perché la riga di crome che si fa swingare somiglia più a una linea melodica
che a un kit intero. Ma è una **scelta dichiarata, non un dato**: chi scrive
una linea di ride ha una ragione misurata per salire verso 67, e chi scrive un
groove di batteria per scendere verso 60.

### Il groove template: come si scrive, nel jazz

La velocity e il microtiming vengono da **una esecuzione nominata** del Groove
MIDI, non da una media: `GR.profilo(base, id)` la legge,
`MU.applica_groove(note, prof, dove=…)` la posa su un pattern uscito da
`MU.passi()`. Quale esecuzione, come si sceglie la voce e perché il nome GM
non è il ruolo musicale stanno nella **casella 6**, che è dove le misure
vivono; qui c'è solo la parte di macchina.

E la parte di macchina è una sola cosa, ma decisiva: **il template porta il
solo residuo, lo swing lo fa la song.** `MU.applica_groove()` scrive velocity e
**uno scarto per ogni passo e per ogni strumento**, senza nessuna soglia — non
«pochi tick»: sul template raccomandato il più grande arriva a **quasi 12 tick,
cioè quasi 40 ms**, e la casella 6 lo dà per esteso insieme all'avvertenza che
serve, cioè che gli estremi poggiano su uno o tre colpi su 193 battute. Il
rapporto fra le due crome lo mette invece
`S.set_swing(doc, …, figura='1/8')`, che vale per tutte le tracce insieme —
basso e comping compresi. **Perché** le due cose vadano tenute separate — cioè
che un template il quale portasse anche lo swing lo farebbe applicare due volte
— non è del jazz e sta nel comune, «Il groove template»; del jazz sono i numeri
qui sopra e la figura da swingare.

⚠️ **Il dispositivo ha un quantize/humanize che cancella il template.** Il
meccanismo è di macchina e vale per ogni repertorio, quindi il suo posto è il
comune di [`../MUSICA.md`](../MUSICA.md), «La macchina» — «Il quantize/humanize
del dispositivo cancella il groove template», dove dal 24 agosto 2026 c'è per
esteso: quale gesto, in quale verso, e perché non si somma al template. Qui
resta il rimando e non la copia, ma il rimando ci resta: una scheda che tace su
un comando che cancella il proprio lavoro è peggio di una che lo ripete.

⚠️ **`length` sulla `<noteRow>` è un meccanismo altro, e non serve qui.** Dà
alla singola riga una lunghezza propria, che **può superare quella della
clip** — quindi è poliritmo, non suddivisione. Serve ai metri dispari e alle
figure che non chiudono con la battuta; **allo swing di crome in 4/4 non serve
affatto**, e usarlo per quello complicherebbe una clip senza cambiarne il
feel. È **osservato nei file e non verificato sul dispositivo**: resta un punto
aperto in [`../../HANDOFF.md`](../../HANDOFF.md) §7, dove sta anche cosa
succede quando riga e clip non sono in rapporto intero.

### Il Deluge non riquantizza — VERIFICATO sul dispositivo il 24 agosto 2026

Era la scommessa su cui poggiava tutto il template: **che il dispositivo tenga
le posizioni fuori griglia invece di riportarle sulla griglia**. Adesso non lo è
più, ed è la prima volta che questo progetto scrive note fuori griglia e le
rivede tornare indietro.

**Il giro, e cosa dice.** `GROOVE1` — la song della coppia della casella 6, 31
note su quattro righe, con scarti da **−6 a +2 tick** rispetto ai passi — è
stata caricata sul Deluge, **nessuna nota è stata toccata**, ed è stata
risalvata dal dispositivo. Riscaricata e confrontata nota per nota con quella
scritta: **31 posizioni su 31 conservate, nessuna spostata**, e i residui sono
tutti ancora lì `[OSS]`.

Il file risalvato è **36 545 byte** contro i 35 226 scritti — il firmware
aggiunge roba sua — e conserva **entrambi** gli attributi
`noteDataWithSplitProb` e `noteDataWithLift`, cioè non collassa le due
codifiche in una `[OSS]`.

⚠️ **Il sub-slot: il Deluge l'ha salvata come `GROOVE1 2`.** Nome col
**numero dopo uno spazio**, nella stessa cartella `/SONGS/DelugePal/` — il
dispositivo **non sovrascrive**, si fa un posto suo accanto. Chi risale un giro
del genere deve quindi **leggere il nome sul display** prima di riscaricare: il
percorso scritto con `MU.destinazione()` non è quello da cui la song torna
indietro, e `MU.origine()` legge ovunque proprio per questo.

⚠️ **Quello che questa sezione NON dice**, e vale la pena separarlo:

- **è quello che si vede, non quello che si sente.** Che quelle posizioni
  conservate si sentano — e da quanto grandi in poi — è un'altra affermazione e
  sta nella casella 6, che su di essa è molto più cauta. Questa qui è
  **meccanica**: si legge nei byte di due file, e nessuna riserva sull'orecchio
  di chi ascolta la tocca;
- **non riguarda il quantize/humanize.** `AUDITION` + `TEMPO` riscrive le
  posizioni di una riga ed è tuttora `[MAN]` e mai provato: durante questo giro
  è stato deliberatamente **non toccato**. Il comune, «Il quantize/humanize del
  dispositivo cancella il groove template»;
- **è un giro solo, su una song sola.** `[OSS]`, non una legge del firmware —
  ma è l'unico giro che serviva prima di scrivere altri template.

*(Era una previsione scritta **prima** del giro e data per `[IPO]`: «il
dispositivo tiene le posizioni in tick e la quantizzazione è un gesto
esplicito, non qualcosa che accada aprendo o salvando». **Confermata.** Le
altre tre previsioni riguardavano l'ascolto, e sono nella casella 6: due di
quelle non sono andate così.)*

Manca tutto il resto: nessun **pezzo** jazz è mai stato generato — la coppia del
24 agosto è una clip di batteria di due battute su un kit CR78, che per
giudicare una posizione va benissimo e del timbro jazz non dice niente — quindi
del suono, dei kit e dell'arrangiamento jazz sul Deluge non si sa niente.

*Nel frattempo, per comporre:* di macchina, e non di repertorio, c'è già tutto
il telaio nel comune, «La macchina» — il synth vuoto `TEMPL.XML`, le norme di
sound design, prima la struttura e poi il valore, un drum di kit che è un
`<sound>` completo. Si parte da lì, esattamente come si è partiti per il dub, e
niente di quello vale meno perché il repertorio è un altro. Il **62** qui sopra
invece **è uscito** da un Deluge il 24 agosto 2026 — le due song della coppia lo
portano entrambe, con `figura='1/8'` — ma non è stato **giudicato**: nessuno è
stato interrogato su di lui, ed essendo identico nei due file quell'ascolto non
lo metteva in gioco `[OSS]`.

⚠️ **Lo stesso giorno un 62 è stato messo in gioco, ma non è questo.** Nella
coppia dell'astrazione dello swing — quella descritta nel comune, e rimandata
in cima a questa casella — `swingAmount` è la sola riga che cambia fra i due
file, e in una delle due **tutto** lo swing viene di lì: che quella sia stata
sentita «sufficientemente simile» all'altra, dove lo swing stava nelle
posizioni di un'esecuzione vera, dice che un display 62 su `1/8` rifà a
orecchio lo swing di **quell'esecuzione** `[OSS]`. Ma quel 62 viene dal BUR di
quella singola esecuzione, non dal corpus
Weimar: **coincide** col valore della tabella, non lo conferma. Ed era una
domanda da «uguali o diverse», non un giudizio.

Il 62 della tabella resta quindi non **giudicato**, e ci vuole un pezzo jazz
vero fatto **ascoltare all'utente**: la sua correzione è ciò che riempie la
casella 11.

## 11. Trappole del generatore

**Vuota, e il 24 agosto 2026 una correzione dall'ascolto è arrivata davvero —
ma non è di questo repertorio, e sta nel comune.** Vale la pena scrivere perché,
perché è la prima volta che questa casella ha dovuto decidere.

Quel giorno l'utente ha ascoltato la coppia `GROOVE0`/`GROOVE1` sul dispositivo,
ha risposto a tre domande, e poi **ha corretto due volte**: rifacendo di sua
iniziativa una prova a tempo lentissimo, e **declassando i propri stessi
risultati** («a questo livello di dettaglio tutte le mie valutazioni sono
imprecise»). Sono correzioni vere, e sono nella casella 6 con la data.

Ma non sono trappole **di questo repertorio**. Riguardano *quanto peso dare
all'orecchio come strumento di misura* e *a che tempo si ascolta uno scarto* —
e l'orecchio è lo stesso quando ascolta dub, e un tick è una frazione di
movimento in qualunque genere. Il criterio dello schema è preciso: qui sta ciò
che **non si trasferisce**, e queste due si trasferiscono per intero. Stanno
quindi nel comune di [`../MUSICA.md`](../MUSICA.md) — «Un ascolto non è una
misura di percezione» e «Le due domande sono diverse, e la soglia dipende dal
tempo» — dove valgono per tutti invece che per il jazz soltanto.

E la coppia ascoltata, del resto, non era un pezzo da giudicare: era uno
strumento di misura costruito per rispondere a una domanda sola. Questa casella
si riempie al primo **pezzo jazz corretto dall'utente**, come è successo al dub,
e quel momento non è ancora venuto.

*Nel frattempo, per comporre:* qui non c'è dove andare a prendere niente, e
non è una lacuna da colmare in fretta — **una trappola si osserva**, e
osservarla vuol dire aver generato un pezzo e averlo fatto ascoltare. Il
ripiego quindi non è una fonte ma una **procedura**: si genera, si fa
ascoltare, e la correzione si scrive qui col protocollo del comune (`Tengo /
Cambio / Direzione`) e con la data. E le trappole del dub **non si prendono in
prestito**: lo schema dice che «cosa sbaglia un generatore *qui*» non si
trasferisce, e riportate sotto un altro repertorio sembrerebbero lezioni
generali senza esserlo. L'unica cosa che si porta dietro è la lezione di
metodo, che sta nel comune perché vale per tutti.

Il primo candidato è già nominato e sta nella **casella 10**: il valore di swing
del jazz è aritmetica su un meccanismo, non ascolto, e se qualcuno dirà che
quello swing suona sbagliato la correzione va scritta **qui**, col protocollo e
con la data.
