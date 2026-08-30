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

**Misurata — la prima `[MIS]` del progetto.** Lo swing del jazz è misurato su
due corpora. ⚠️ Fino al 30 agosto 2026 questa riga diceva anche «e l'unica
piena di questa scheda»: era vera quando fu scritta e ha smesso di esserlo il
29 agosto, quando le caselle 7, 8 e 9 si sono riempite nello stesso giro. Le
righe che si vantano di essere sole invecchiano da sé.

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
su 50** — 29 delle loro 35 stanno fra i `fill` — e togliendole le mediane dei
**quattro strumenti portanti** della tabella qui sotto si spostano **al massimo
di 3 punti su 127**: rullante 47→48, charleston a pedale 70→70, ride 64→65,
kick 59→62. La **quinta riga si sposta di cinque**, `charleston chiuso` da
**38 a 43** `[MIS]`, ed è anche la riga più magra della tabella — 545 colpi
contro i 5 217-10 689 delle altre. La tabella vale quindi per l'etichetta
intera dove poggia su molti colpi, e lo dice invece di lasciarlo supporre.

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

Sulla griglia a 16 passi della casella 2, aggregando le **42 esecuzioni `beat`
4/4 senza funk e fusion**, ogni esecuzione pesata uno — se no il file da 193
battute deciderebbe da solo cosa fa un batterista jazz. Sono **42 e non le 41
della casella 4**: là il conteggio è delle esecuzioni con un BUR misurabile, e
la differenza è `drummer10/session1/7`, che non ha nemmeno una coppia di crome
da misurare — «Il bordo fra due passi» la nomina. Ogni cella è **quota
dei colpi di quello strumento · velocity mediana**; le colonne sono le otto
crome, e quel che manca al 100% sta sui passi dispari, cioè sulle semicrome
`[MIS]`:

| strumento (esecuzioni, batteristi) | 1 | lev 1 | 2 | lev 2 | 3 | lev 3 | 4 | lev 4 |
|---|---|---|---|---|---|---|---|---|
| **ride** (18, 4) | 13,8% v70 | 3,4% v64 | **15,3% v86** | 11,8% v67 | 15,2% v72 | 3,0% v68 | **13,6% v88** | 10,5% v66 |
| **charleston a pedale** (23, 3) | 8,2% v48 | 4,1% v62 | **26,1% v68** | 2,9% v64 | 8,5% v46 | 6,5% v58 | **23,9% v71** | 2,2% v61 |
| **rullante** (28, 5) | 5,3% v83 | 7,1% v47 | 11,8% v63 | 7,5% v54 | 5,1% v59 | 8,2% v48 | 10,8% v63 | 8,7% v58 |
| **kick** (23, 4) | **17,2% v65** | 5,7% v54 | 9,4% v54 | 6,6% v54 | 12,0% v59 | 8,9% v56 | 10,4% v58 | 6,4% v55 |

⚠️ **Questa tabella è stata rimisurata il 24 agosto 2026**, e le quote dei
movimenti sono **scese**: di mezzo punto per ride, rullante e cassa, di quasi
tre punti per il **charleston a pedale** (25,7 → 22,9 e 23,7 → 20,8). La
ragione sta più sotto, «La catena non era invertibile, e ora lo è». In breve:
un colpo che anticipa un movimento di più di mezza semicroma ora viene contato
sulla semicroma **precedente**, dov'è, invece che sul movimento. Si vede di
più sul charleston perché è la voce che di quei colpi ne ha di più.

⚠️ **E rimisurata una seconda volta il 26 agosto 2026**, quando lo stimatore
per passo è cambiato — «La decisione: il taglio si sposta per voce». Stavolta
le quote dei movimenti sono **risalite**, e il charleston più di tutti: **22,9
→ 26,1** sul 2 e **20,8 → 23,9** sul 4. I numeri di prima restano leggibili
qui sopra e nel resto di questa casella, con la loro data. ⚠️ **E non è il
ritorno del numero della grazia**, che sarebbe la lettura comoda: i valori
nuovi stanno **sopra** anche quelli di prima del 24 agosto (25,7 e 23,7), e
soprattutto ci arrivano per un'altra strada. La grazia teneva quei colpi sul
movimento **schiacciandone il residuo** dentro mezzo passo; `'voce'` ce li
riporta **conservandolo** intero. Le due cose danno quote simili e residui
molto diversi, ed è il residuo la ragione per cui questa casella esiste.

Quello che ne esce è il jazz che ci si aspetta, e nessuno gliel'ha imposto:

- **il ride fa lo *spang-a-lang*.** Colpisce i quattro movimenti in parti quasi
  uguali (13,8 · 15,3 · 15,2 · 13,6%), e il levare lo aggiunge **dopo il 2 e
  dopo il 4** (11,8 e 10,5%) e quasi mai dopo l'1 e il 3 (3,4 e 3,0%). E
  **accenta il 2 e il 4 di 16 punti** di velocity — v86 e v88 contro v70 e
  v72 `[MIS]`. Se un pattern di ride jazz va scritto a mano, questa riga è la
  risposta. ⚠️ **Rimisurata il 26 agosto 2026, e il ride si muove appena**,
  com'era previsto: fino a quel giorno i quattro movimenti erano **13,4 ·
  15,1 · 15,0 · 13,5%**, il levare dopo il 2 e il 4 **12,3 e 10,7%**, e la
  velocity dell'1 **v71**. Il levare dopo l'1 e il 3 e le due velocity
  accentate non si sono mosse di un decimo;
- **il charleston a pedale è il 2 e il 4, e quasi nient'altro:** **50,0%** dei
  suoi colpi (26,1 + 23,9) cade lì, con la velocity più alta dei quattro
  movimenti (68 e 71 contro 48 e 46 sull'1 e sul 3). È anche la **verifica che
  la griglia è allineata**: il piede sul 2 e sul 4 è un fatto noto del
  repertorio, e ritrovarlo sui passi 4 e 12 dice che l'origine della battuta
  nei file è davvero una stanghetta. ⚠️ **Ma altri 11,6% stanno sui passi 3 e
  11** (6,4 e 5,2%), cioè sulle semicrome che **precedono** il 2 e il 4, e non
  è un secondo disegno: è lo **stesso** piede, che anticipa tanto da finire
  oltre il confine del passo. Chi legge questa riga come «il charleston suona
  anche in levare di semicroma» legge un artefatto della griglia. ⚠️ **I due
  numeri di questa riga si sono mossi il 26 agosto 2026**: erano **43,7%** sui
  movimenti (22,9 e 20,8) e **17,5%** sui passi 3 e 11 (9,4 e 8,1). Lo
  stimatore nuovo riporta sul battere circa **un terzo** dei colpi che stavano
  sulla semicroma precedente, e i due movimenti si compensano quasi: −5,9
  punti sui passi 3 e 11, +6,3 sui movimenti. La sezione «La catena non era
  invertibile» misura il primo
  movimento, «Il bordo fra due passi» e la decisione che la chiude il
  secondo;
- **il rullante non ha un posto: ha due livelli.** È l'unico strumento sparso
  su tutti e sedici i passi — **oltre un terzo dei suoi colpi sta sulle
  semicrome** — e a separarlo non è la posizione ma la velocity: passi pari
  **47-83**, passi dispari **42-53**. È la definizione operativa di fantasma.
  ⚠️ **Le due fasce sono del 26 agosto 2026**: erano **47-72** e **41-54**. La
  fascia pari si allarga in alto **per un passo solo**, il primo della battuta
  (v83); tolto quello, gli altri sette stanno fra 47 e 63, cioè dove stavano.
  I due livelli restano separati — mediane **58,5 contro 45,5** — che è quel
  che la riga afferma;
- **la cassa sta sull'1 e sul 3** (17,2 e 12,0%, contro 9,4 e 10,4 sul 2 e sul
  4) e anche dove batte di più sta **piano**: v65 e v59 su 127, cioè dentro la
  fascia che il comune chiama «riempimento». Non è il colpo che definisce la
  battuta — è il contrario di quello che fa in un repertorio a cassa in
  quattro. ⚠️ **Anche questi numeri sono del 26 agosto 2026**: erano **17,2 e
  12,6%** contro **9,4 e 10,2%**, con **v65 e v62**. Il disegno non si è
  mosso — la cassa sta sull'1 e sul 3 in tutt'e due le versioni — ma il
  margine del 3 sul 4 si è assottigliato, da 2,4 a **1,6 punti**.

### Il microtiming che resta, e perché è poco

Tolti l'origine della griglia e lo swing — la catena di `GR.profilo()` — quello
che resta è il **residuo**, in tick Deluge (96 per movimento) `[MIS]`:

| strumento | esecuzioni | batteristi | mediana | q1-q3 |
|---|---|---|---|---|
| charleston a pedale | 23 | 3 | −5,66 | −7,10 … −3,34 |
| rullante | 26 | 4 | −3,23 | −4,97 … −0,81 |
| kick | 22 | 4 | −1,15 | −3,87 … +0,37 |
| ride | 18 | 4 | −1,10 | −3,16 … +0,23 |

**Le mediane stanno tutte entro 5,7 tick**: poche unità su 96 per movimento, e
tutte dalla stessa parte — **prima** della griglia. Per la scala, e per i
numeri che vengono dopo: un tick vale 6,25 ms a 100 BPM e 3,38 ms a 185.

⚠️ **Questa tabella è del 26 agosto 2026, e l'ordine delle quattro voci non è
cambiato: sono le prime due a staccarsi dalle altre.** Fino a quel giorno
diceva
charleston **−3,42** (q1-q3 −4,92 … −1,93), rullante **−1,78** (−3,42 …
−0,15), kick **−1,12** (−2,83 … −0,16), ride **−1,00** (−2,94 … +0,21), e la
riga qui sopra diceva «entro 3,5 tick». Le mediane sono diventate **più
negative**, cioè più anticipate, e proprio sulle due voci che anticipano di
più: il charleston di 2,2 tick, il rullante di 1,5, mentre kick e ride si
muovono di un decimo di tick o meno. ⚠️ **Il verso è quello giusto, e la
ragione è aritmetica**: col vecchio stimatore un colpo che anticipava troppo veniva
contato sul passo **precedente**, dove il suo residuo diventava **positivo e
grande**; ora viene contato sul passo che il gesto descrive, col suo residuo
**negativo e vero**. Togliere dei grandi positivi e rimetterli come grandi
negativi **abbassa** la mediana della voce, e la abbassa di più dove quei
colpi sono di più. Vedi «Il bordo fra due passi».

#### La catena non era invertibile, e ora lo è — 24 agosto 2026

⚠️ **Tutti i numeri di residuo di questa casella sono stati rimisurati**, e
questa sezione dice perché e di quanto. Non è una raffinatezza: toccava **un
colpo su tre**.

`GR.profilo()` toglie lo swing dalle posizioni misurate perché lo rimetta il
firmware, e per farlo inverte la mappa dello swing. Ma `profilo_da_colpi()`
calcolava il movimento con **mezzo passo di grazia** — `floor(p/ppq + 0,125)`
— così che un colpo appena prima del battere fosse attribuito al movimento
seguente. Ne usciva una **fase negativa**, e su una fase negativa
`_senza_swing()` prendeva il ramo della prima metà del movimento — quella che
il firmware **dilata** — per una nota che sta nella seconda, quella che il
firmware **comprime**. Non era l'inversa di niente.

Misurato sul corpus delimitato — 42 esecuzioni, 28 604 colpi `[MIS]`:

| | |
|---|---|
| colpi che prendevano una fase negativa | **9 535 su 28 604 (33,3%)** |
| errore mediano sulla posizione di quei colpi | **1,25 tick** (q1-q3 0,20-2,94) |
| errore massimo | **12,15 tick** |
| colpi che ne uscivano su un passo diverso da quello giusto | **956 (3,3%)** |

Non cade a caso: il difetto vive nell'**ultimo ottavo di movimento**, cioè
esattamente dove sta chi anticipa un battere. Il **charleston a pedale**, che
nel jazz suona il 2 e il 4 e li anticipa, ne aveva **il 50,4% dei colpi** — il
ride il 36,1%, la cassa il 37,0%, il rullante il 22,4% `[MIS]`. **Ha quindi
spostato un confronto fra voci**, che è ciò su cui questa casella poggia: le
conseguenze sono scritte una per una nelle sezioni che seguono.

⚠️ **E la giustificazione scritta nel codice era falsa.** Il commento diceva
che senza la grazia «il residuo uscirebbe grande quanto un movimento intero».
Non può: il passo si sceglie con `round(dritta / passo_tick)`, cioè si prende
il passo **più vicino**, quindi il residuo non supera **mezzo passo — 12 tick
— per costruzione**, con la grazia e senza. Sul corpus: **0 residui** oltre i
12 tick su 28 604, con o senza. La grazia non stava difendendo da niente.

⚠️ **Quel «per costruzione» è vero di `round()`, e dal 26 agosto 2026 non è
più vero del default.** Lo stimatore nuovo sposta il **confine** fra due
passi, quindi il residuo non è più limitato a mezzo passo: può arrivare vicino
a un passo intero, e sul template ci arriva. È il limite che resta, ed è
scritto in «Il limite che resta: l'ancoraggio». La riga qui sopra continua a
valere per quello che smentiva — la giustificazione della grazia — e per il
modo `'vicino'`.

**Cosa non è cambiato, ed è misurato e non supposto.** Il **BUR** passa da
`GR.levare_da_posizioni()`, che la fase la calcola già con la divisione
intera per difetto, e la **scala di velocity** non legge le posizioni: le
sezioni «La delimitazione», «La scala di velocity» e tutta la **casella 4**
escono **identiche riga per riga** dal confronto fra il prima e il dopo, e
così i **fill** della casella 9. Anche il **massimo spostamento singolo** del
template (+11,80 tick) e la sua **escursione** (22,83 tick) non si muovono.
⚠️ **Questi due si sono poi mossi il 26 agosto 2026**, per un'altra ragione e
in due versi opposti: vedi «Due grandezze diverse». Che non si fossero mossi
**il 24 agosto** resta vero, ed è quello che questa riga afferma.

⚠️ **Quello che invece è cambiato, e non era previsto, è l'assegnazione dei
passi.** Si supponeva che togliere la grazia cambiasse solo il residuo; cambia
anche **dove** finiscono 956 colpi su 28 604. La ragione è sana — un colpo
che, tolto lo swing, sta a più di mezza semicroma dal battere è **più vicino
alla semicroma precedente**, e lì va — ma la conseguenza va guardata in
faccia: dei sedici confini di passo di una battuta, i **quattro** che sono
anche confini di movimento si comportavano diversamente dagli altri dodici, e
la grazia lo nascondeva. Vedi «Il bordo fra due passi».

##### Il bordo fra due passi, e chi ci cade dentro

Poiché il passo è il **più vicino**, un colpo che anticipa il suo passo di più
di 12 tick dritti non esce come un anticipo grande: esce come un **ritardo**
grande sul passo precedente. Il segno si rovescia.

Con la grazia, sui **battere**, questo quasi non poteva accadere: i colpi
dell'ultimo ottavo di movimento finivano schiacciati dentro `[−6/levare, 0]`
tick, cioè **dentro mezzo passo ogni volta che il levare supera 0,5** — che è
il caso di **38 esecuzioni su 42** `[MIS]`. Le altre quattro sono tre a crome
dritte o quasi — `drummer10/session1/10` (levare 0,50, bordo −12,06 tick),
`drummer4/session1/2` (0,46, −13,11) e `drummer4/session1/3` (0,41, −14,64) —
più `drummer10/session1/7`, che di levare non ne ha affatto: è l'esecuzione
senza nemmeno una coppia di crome misurabile, quella che fa **41** il conteggio
della casella 4 mentre qui le esecuzioni delimitate sono **42**, e il suo
levare è lo 0,5 di ripiego. E il charleston a pedale del jazz suona quasi solo
sui battere: **la sua unanimità era in parte garantita dal difetto**, non dai
batteristi.

Ora i battere si comportano come tutti gli altri confini, e il rovesciamento
si vede. Quanto spesso, misurato `[MIS]` — la colonna in **grassetto** è lo
stimatore scelto il 26 agosto 2026 (`'voce'`), quella in *corsivo* accanto è
il `'vicino'` di prima, tenuto perché è la differenza fra le due ad aver
deciso:

| strumento | esecuzioni | con una cella oltre 9 tick | *(prima)* | col **battere in minoranza** | *(prima)* |
|---|---|---|---|---|---|
| rullante | 28 | **7** | *2* | **1** | *3* |
| charleston a pedale | 23 | **9** | *4* | **0** | *3* |
| kick | 23 | **6** | *2* | **2** | *2* |
| ride | 18 | **3** | *4* | **1** | *1* |

«Battere in minoranza» vuol dire che la semicroma **prima** di un movimento
porta **più colpi del movimento stesso**, con lo scarto di segno opposto: non
è un secondo disegno, è **lo stesso gesto** contato in due posti.

⚠️ **Le due colonne si muovono in versi opposti, e non è una contraddizione:
è il meccanismo.** Spostare il taglio per voce smette di **spezzare** il gesto
— i colpi tornano sul battere, e il battere torna in maggioranza — ma proprio
perché non li ripiega più sul passo accanto, ciascuno **conserva la sua
distanza vera dalla griglia**, che è grande. Le celle oltre i 9 tick perciò
**crescono** (2 → 7, 4 → 9, 2 → 6; solo il ride cala, 4 → 3) mentre il battere
in minoranza **cala** (3 → 1 sul rullante, 3 → 0 sul charleston, e resta fermo
su kick e ride). Chi legge la prima colonna da sola conclude che lo stimatore
è peggiorato; chi legge la seconda da sola conclude che ha risolto tutto.
Nessuna delle due letture è quella giusta.

Su `drummer10/session1/1` si legge nei conteggi `[OSS]`. Col vecchio
stimatore il charleston portava **41 e 42 colpi sui passi 3 e 11** (+3,8 e
+0,7 tick) contro **29 e 19 sui passi 4 e 12** (−8,3 e −9,8): il piede sul 2 e
sul 4 era in minoranza sul 2 e sul 4. Col nuovo porta **20 e 32 sui passi 3 e
11** (−3,1 e −3,1) contro **50 e 34 sui passi 4 e 12** (−10,7 e −11,2). Il
gesto non si è spostato di un tick: ha smesso di essere contato due volte, e
il residuo che se ne legge è quello che il batterista ha davvero suonato.

⚠️ **Succede a tutte le voci, ma pesa solo sul charleston**, e la ragione è la
tabella del profilo posizionale: il charleston mette **la metà dei suoi colpi
su due soli passi** (il 43,7% col vecchio stimatore, il 50,0% col nuovo),
quindi basta che uno dei due vada in minoranza perché la sua mediana pesata
sui colpi cambi segno; rullante, cassa e ride spargono i colpi su otto passi o
più, e una cella ribaltata non li muove. È per questo che la voce su cui
questa casella poggia la conclusione più forte è anche quella più esposta allo
stimatore.

**Non era un difetto della correzione: era un limite dello stimatore**, che la
correzione ha smesso di nascondere. Un template è per definizione **per
passo**, e un batterista che anticipa di mezza semicroma non ci stava dentro.
Chiuderlo voleva dire cambiare **come si aggrega** — non come si toglie lo
swing.

##### La decisione: il taglio si sposta per voce — 26 agosto 2026

⚠️ **Fino al 26 agosto 2026 qui c'era scritto che chiudere questo limite «è
una decisione di disegno che questa casella non prende: la dichiara, e la
lascia a chi verrà».** È stata presa quel giorno, ed è questa sezione. Il
rovesciamento del segno sui battere è **chiuso**. Il limite che resta è un
altro, più piccolo e di natura diversa, ed è la sezione dopo.

**Cosa è cambiato, in una riga.** Il passo su cui un colpo viene contato non
si sceglie più col `round()` puro — il passo **più vicino** — ma spostando il
**confine** fra due passi sulla **fase media di quella voce** dentro il passo.
Il taglio si sposta, la griglia no: il residuo resta misurato dalla griglia
vera. `GR.TAGLI` tiene i tre modi — `'vicino'` (il vecchio), `'voce'` (il
nuovo default) e `'rado'` — e ognuno resta chiamabile per nome, così che
qualunque numero di questa casella si possa rifare con l'altro.

**La misura che ha deciso, ed era scelta prima che i numeri esistessero.** Uno
stimatore è uno stimatore se la sua risposta **segue** la cosa che misura:
traslata una voce sola di δ tick, la posizione che dichiara deve muoversi di
δ. Provata su nove δ da −8 a +8 tick dentro un passo da 24, su **42
esecuzioni, 5 batteristi, 111 voci** `[MIS]`:

| | `'vicino'` (il vecchio) | `'voce'` (scelto) | `'rado'` |
|---|---:|---:|---:|
| pendenza mediana sotto traslazione | 0,808 | **0,998** | **0,998** |
| scarto massimo mediano (tick) | 3,28 | **1,47** | 1,97 |
| voci con un salto ≥ mezzo passo | 16 / 111 | 4 / 111 | **3 / 111** |
| celle mal ancorate | 0 *(impossibile per costruzione)* | **2** | 5 |

⚠️ **Perché questa misura e non due più ovvie**, ed è la parte da leggere
prima di tutte le altre. L'**errore di ricostruzione per inversione** premia
lo stimatore rotto: spezzare un gesto in due celle rende ciascuna delle due
mediane **più stretta**, quindi l'errore **scende** proprio dove lo stimatore
sbaglia di più. E prendere per bersaglio **la tenuta delle conclusioni di
questa casella** sarebbe fabbricare la conclusione, che è esattamente il
difetto della finestra di grazia. La linearità sotto traslazione non guarda
nessuna conclusione: guarda se lo stimatore segue.

**Cosa la misura chiude da sola, senza bisogno di nessun giudizio:**
`'vicino'` non è uno stimatore. Segue i dati per lo **0,808** contro lo
**0,998** di tutt'e due i candidati, e ha **16 voci su 111** che saltano di
mezzo passo contro 3 e 4. Questo è il risultato del lavoro, ed è netto.

⚠️ **Cosa la misura NON chiude — e la regola scritta prima selezionava
l'altro.** Fra `'voce'` e `'rado'` la pendenza è pari a tre decimali. La regola
scritta prima diceva: scartare per pendenza, poi vincere con **meno salti**, e
alla lettera seleziona **`'rado'`** — 3 contro 4. Il proprietario ha scelto
`'voce'`, per iscritto, **contro la propria regola**, e le ragioni stanno
tutte sul tavolo: il margine di `'rado'` è **una voce su 111**, cioè
plausibilmente rumore, mentre `'voce'` vince su **due** grandezze e con
margini più larghi — scarto massimo mediano 1,47 contro 1,97, celle mal
ancorate 2 contro 5; il **terzo criterio** della regola, «a parità vince
quello con meno parametri», era diventato **void**, perché dopo la riscrittura
nemmeno `'rado'` ne ha; e la **colonna dell'ancoraggio non esisteva** quando
la regola è stata scritta.

⚠️ **Questo fatto sta scritto perché è ciò che rende la decisione
verificabile.** Scavalcare una regola dopo aver visto i numeri è esattamente
il meccanismo della finestra di grazia, dove un criterio messo per una ragione
plausibile fabbricava la conclusione. L'unica difesa è che la regola **non sia
stata riscritta per far vincere il vincitore**, e qui non lo è: è dichiarata
**insufficiente** a decidere una parità che non aveva previsto, e la decisione
la firma una persona con tutte e quattro le colonne visibili. Chi rilegge può
non essere d'accordo — e ha davanti i numeri per dirlo.

⚠️ **E il «battere in minoranza», il 43,7% e il «12 su 15» NON sono entrati
nella scelta.** Era scritto nel piano **prima** della misura — il testo esatto,
col commit da cui si rilegge, è citato più sotto in «C'è una stratificazione, e
il piede anticipa tutto il resto» — e non è un
dettaglio di procedura: è la ragione per cui le sezioni qui sotto, dove
qualche conclusione di questa casella si rafforza, possono essere lette senza
sospettare che lo stimatore sia stato scelto per farle tornare. Sono
conseguenze: si riportano, non decidono.

**Cosa non si è mosso, ed è misurato e non supposto.** Il **BUR** e il levare
escono da `bur_da_posizioni()` su **tutte** le posizioni, prima che un passo
venga assegnato e senza mai vedere il taglio: restano **1,48 su 41 esecuzioni,
levare 59,7%**, e sulle esecuzioni nominate qui sotto vengono identici nei tre
modi. Tutta la **casella 4** è quindi intatta, e con lei il valore che
`S.set_swing()` scrive: **l'A/B dello swing già ascoltato sta in piedi così
com'è.** Non si muovono nemmeno la **delimitazione**, la **scala di velocity**
per strumento — che le posizioni non le legge — né i **fill** della casella 9.
⚠️ Le velocity **per passo** del profilo posizionale invece si muovono,
perché cambia quali colpi cadono in quale cella: è un'altra grandezza dalla
scala, e non va confusa con essa.

##### Il limite che resta: l'ancoraggio — 26 agosto 2026

⚠️ **Non è lo stesso limite di prima, ed è più piccolo.** Chiuso lo spezzarsi
di un gesto fra due celle, resta indeciso **su quale** dei due passi ancorarlo.
Per i dati soli, «14 tick prima del passo 4» e «10 tick dopo il passo 3» sono
**la stessa cosa** — e il gesto è anzi **più vicino** al passo debole, 10
contro 14. Nessun criterio di **distanza** può quindi preferire il battere: a
distinguerli c'è solo il **metro**, che è musica e non misura.

**Quanto pesa, misurato** il 26 agosto 2026 su **42 esecuzioni e 5
batteristi** `[MIS]`: **2 celle** col taglio scelto — il kick di
`drummer10/session1/8`, passi **7 e 15**, scarti **+13,04 e +13,93** tick su
14 e 13 colpi — contro **5** con `'rado'` e **0** con `'vicino'`. ⚠️ **Lo zero
di `'vicino'` non è una virtù: è impossibile per costruzione**, perché quel
modo il taglio non lo sposta mai e il suo residuo non può uscire da mezzo
passo. Le due celle di `'voce'` sporgono di **1,0 e 1,9 tick** oltre i 12 di
mezzo passo — che è la soglia con cui la misura definisce «mal ancorata» — e
su tutt'e tre i modi le celle contate stanno fra **+12,70 e +16,50**: sono
casi **genuinamente ambigui**, non collocazioni grossolanamente sbagliate.

**Perché non si è scritta una regola**, deciso lo stesso giorno: una regola
avrebbe dovuto pesare il metro contro la distanza **senza nessuna misura che
dica quanto**, cioè inventare un numero per due celle su 42 esecuzioni. Questo
progetto ha già pagato una volta il prezzo di un criterio plausibile messo
senza misura, e si chiamava finestra di grazia.

**E il caso, quando capita, si riconosce dalla cella stessa** — è questo che lo
rende visibile invece che silenzioso. Una cella mal ancorata ha **due marchi
insieme**, e li porta scritti in ciò che `GR.profilo()` già riferisce:

- **porta il gesto quasi intero mentre il battere accanto è quasi vuoto.** Sul
  kick di `drummer10/session1/8` `[OSS]`: passo 7 con **14 colpi** contro il
  passo 8 con **1**; passo 15 con **13** contro il passo 0 con **1**. È
  `Passo.colpi`, e il rapporto è di quattordici a uno e di tredici a uno;
- **ha `|scarto| > mezzo passo`**, cioè oltre 12 tick, che con `'vicino'` era
  **impossibile per costruzione**. È `Passo.scarto`, ed è il marchio che dice
  «qui il taglio è stato spostato», non «questo batterista è in ritardo».

⚠️ **Correzione del 28 agosto 2026: la ragione scritta il 26 era falsa.**
Diceva: «`MU.applica_groove()` già lo riferisce. Se il pattern chiede un passo
che il profilo non ha, la nota resta com'è e il passo finisce in
`senza_appoggio`, che va letto — il caso è visibile e non silenzioso, ed è lo
stesso principio del "non inventa"». **`senza_appoggio` non copre questo
caso**, e non lo copre per costruzione: scatta solo quando la cella **manca**
(`tools/delugexml/musica.py`, `per_passo.get(passo)` che torna `None`), mentre
una cella mal ancorata **c'è, ed è sbagliata**. Su queste celle
`senza_appoggio` resta **vuoto comunque vada**, e i modi di andar male sono
due: un pattern che chiede il passo 8 trova la cella da **un colpo solo** e ci
si appoggia; un pattern che chiede il passo 7 si prende i **+13,04 tick** e
posa la nota a **181** tick, mentre il confine fra i due passi sta a **180** e
il passo 8 comincia a **192** — cioè **oltre il confine, nel territorio del
passo accanto**. La decisione non cambia: nessuna regola. Cambia la ragione, ed
è quella dei due marchi qui sopra.

⚠️ **Ma questi sono livelli, e un livello in millisecondi non vuol dire
niente.** Convertirli e confrontarli con la finestra dell'udibile sarebbe la
scorciatoia comoda, ed è sbagliata: dopo `GR.origine()` il livello di ogni
esecuzione ha uno **zero arbitrario** — l'origine tolta è comune a tutto il kit
e cambia da esecuzione a esecuzione — quindi «−3,42 tick» non dice *rispetto a
che cosa*, e un millisecondo ricavato da lì non ha un referente. Qui i tick
servono a una cosa sola: a dire che il residuo è **piccolo**.

Con la finestra di 20-40 ms del comune si confrontano **due altre** grandezze,
e danno due verdetti opposti perché *sono* due cose diverse — non perché una
delle due sia sbagliata:

| grandezza | quanto | contro la finestra 20-40 ms | dove sta |
|---|---|---|---|
| **divario fra due pad** (ride − charleston) `[MIS]` | 21,2 ms *(13,5 fino al 26 agosto 2026)* | appena **dentro** | «E prima di tutto: 21,2 ms» |
| **singolo spostamento** che un template scrive `[OSS]` | 64,6 ms *(39,9 fino al 26 agosto 2026)* | **oltre** il bordo superiore | «Due grandezze diverse» |

La prima sta su decine di esecuzioni ed è la stratificazione misurata; la
seconda sta su **una** esecuzione e poggia su **un colpo solo**. Il divario è
inoltre convertito col BPM di **ogni** esecuzione, non a un 100 BPM di comodo:
è l'altra ragione per cui i conti di questa casella non si sommano fra loro. Le
cautele di ciascuna sono scritte nella sua sezione, e **nessuna delle due è il
livello della tabella qui sopra** — che infatti in millisecondi non viene
convertito.

⚠️ **Le due sono cresciute il 26 agosto 2026, col cambio di stimatore, e
hanno attraversato la finestra in due punti diversi.** Il divario è passato
**da sotto a dentro** (13,5 → 21,2 ms) e il singolo spostamento **da dentro a
oltre** (39,9 → 64,6 ms). Nessuna delle due è quindi più dove la riga
descriveva, e l'argomento «tanto il divario sta sotto la finestra» **non è più
disponibile**. La seconda però continua a poggiare su **un colpo solo**, e su
questo il cambio di stimatore non ha migliorato niente.

#### C'è una stratificazione, e il piede anticipa tutto il resto

Le mediane qui sopra vengono da esecuzioni diverse, e un'esecuzione intera può
stare avanti o indietro per conto suo: confrontarle fra loro direbbe poco. La
domanda va fatta **dentro la stessa esecuzione**, e a **tutte** le coppie —
sceglierne una dopo aver visto le mediane sarebbe scegliere il risultato.
Esecuzioni `beat` 4/4 senza funk e fusion `[MIS]`:

| coppia | esecuzioni | batteristi | il primo arriva | in | *(fino al 26 agosto 2026)* |
|---|---|---|---|---|---|
| charleston a pedale − ride | 15 | 3 | **4,60 tick PRIMA** | **15 su 15** | *3,21 tick prima, 12 su 15* |
| charleston a pedale − rullante | 22 | 3 | 2,64 tick prima | 20 su 22 | *2,09 tick prima, 17 su 22* |
| charleston a pedale − kick | 18 | 2 | 4,83 tick prima | 17 su 18 | *1,91 tick prima, 15 su 18* |
| rullante − ride | 14 | 3 | 0,26 tick dopo | 7 su 14 | *0,46 tick dopo, 8 su 14* |
| rullante − kick | 21 | 3 | 0,69 tick prima | 12 su 21 | *0,21 tick prima, 12 su 21* |
| kick − ride | 12 | 3 | 0,66 tick prima | 8 su 12 | *0,16 tick prima, 6 su 12* |

Il disegno sta tutto in una riga: **il charleston a pedale anticipa tutto il
resto**, in tutte e tre le coppie che lo riguardano — e contro il ride di
**4,60 tick in 15 esecuzioni su 15**, con scarti che vanno da **0,37 a 8,70
tick**, tutti dalla sua parte. Fra ride, cassa e rullante invece non c'è
ordine: mediane **sotto il tick** e conteggi fra 7 su 14 e 8 su 12.

⚠️ **Questa riga ha tre versioni, e vanno lette tutte e tre insieme.** Il
conteggio è stato **15 su 15** fino al 24 agosto 2026, **12 su 15** dal 24 al
26, e di nuovo **15 su 15** dal 26. Il divario mediano nel frattempo è
**cresciuto a ogni passaggio**: **2,59 → 3,21 → 4,60** tick.

- **il primo 15 su 15 era garantito da un difetto.** Con la finestra di
  grazia, sui battere il segno non poteva rovesciarsi: i colpi dell'ultimo
  ottavo di movimento finivano schiacciati dentro mezzo passo, e il charleston
  del jazz suona quasi solo sui battere. Non era l'accordo dei batteristi: era
  il parafango;
- **il 12 su 15 era la correzione, e il divario crebbe con lei.** Tolta la
  grazia, i colpi che anticipano un battere di più di mezza semicroma
  finivano sul passo precedente **col segno rovesciato**, e questo succedeva
  al charleston in **tre esecuzioni su ventitré** — esattamente le tre che
  allora contraddicevano: `drummer10/session1/1` (−4,10 tick),
  `drummer10/session1/3` (−3,84) e il template `drummer1/session3/2` (−0,25)
  `[OSS]`, le prime due col **battere in minoranza**, la terza già a zero
  prima della correzione (+0,08);
- **il secondo 15 su 15 è del 26 agosto 2026, e quelle tre esecuzioni stanno
  ora a +6,77, +4,02 e +0,37** `[OSS]`, cioè tutte dalla parte del disegno.

⚠️ **Un lettore ha ogni ragione di sospettare che lo stimatore sia stato
cambiato finché la vecchia conclusione non è tornata.** È il sospetto giusto,
ed è per questo che tutto il necessario a smontarlo è scritto e datato:

- **il criterio era la linearità sotto traslazione per voce**, fissato nel
  piano **prima** che le misure esistessero, e scelto **contro** due criteri
  più ovvi proprio perché quei due si sarebbero potuti piegare — l'errore di
  ricostruzione premia lo stimatore rotto, e la tenuta delle conclusioni di
  questa casella sarebbe stata la conclusione fabbricata da sé. Sta nella
  docstring di `la_prova_di_traslazione()`, non solo qui;
- **la stratificazione era esclusa dalla regola per iscritto.** Il piano al
  **punto di partenza del ramo** — `docs/superpowers/plans/2026-08-26-stimatore-per-passo.md`
  al commit `193ee8e`, cioè prima che esistesse una sola misura — dice
  testualmente, e si controlla con
  `git show 193ee8e:docs/superpowers/plans/2026-08-26-stimatore-per-passo.md`:

  > ⚠️ **Il «battere in minoranza», il 43,7% e il 12 su 15 NON entrano in
  > questa regola.** Sono conseguenze: si riportano al Task 7, non decidono.

  ⚠️ **Nel piano di oggi quella frase è diversa** — «NON **sono entrati** in
  questa **scelta**» — riscritta al commit `a61d51e`, cioè **dopo** la misura
  che ha deciso. Chi la cerchi nel piano di oggi trova un passato scritto a
  posteriori, e ha ragione a diffidarne: la citazione che vale è quella del
  punto di partenza, qui sopra. ⚠️ **Fino al 28 agosto 2026 questa riga ne
  citava una terza forma**, che non è né dell'una né dell'altra versione — «NON
  entrano in questa scelta», il verbo della prima col sostantivo della seconda
  — e senza nome di file né commit, cioè proprio la citazione che avrebbe
  dovuto essere la più verificabile della casella;
- **il default è stato scelto su altre quattro colonne**, e sulla quarta **il
  termine di paragone cambia**: pendenza 0,998 contro **0,808 di `'vicino'`**,
  scarto massimo mediano 1,47 contro **3,28 di `'vicino'`**, voci con un salto
  di mezzo passo 4 su 111 contro **16 di `'vicino'`** — e celle mal ancorate 2
  contro **5 di `'rado'`**, perché contro `'vicino'` la stessa colonna direbbe
  **2 contro 0**, cioè il verso sfavorevole al taglio scelto. ⚠️ Quello zero
  però è
  **impossibile per costruzione** — `'vicino'` il taglio non lo sposta mai, e
  il suo residuo non può uscire da mezzo passo — quindi non è una colonna su
  cui `'vicino'` possa perdere o vincere: è una colonna che esiste solo **fra i
  due candidati**. La tabella sta per intero in «La decisione: il taglio si
  sposta per voce». ⚠️ **Fino al 28 agosto 2026 questa riga non nominava
  nessuno dei termini di paragone**, e la quarta colonna cambiava comparatore
  in silenzio, nel verso favorevole;
- **il divario continua a crescere invece di tornare indietro.** Se lo
  stimatore fosse stato piegato per far tornare il vecchio risultato, ci si
  aspetterebbe il vecchio *numero*: 2,59 tick. Il numero di oggi è **4,60**,
  cioè **quasi il doppio** — l'unanimità è la stessa parola, la misura sotto
  no;
- ⚠️ **il 15 su 15 ESATTO è però contingente al taglio scelto: con `'rado'` la
  stessa grandezza dà 14 su 15 e +4,25 tick** `[MIS]`. Sta scritto qui perché
  **regge** questa difesa invece di indebolirla, e tacerlo sarebbe stato il
  modo più rapido di meritare il sospetto. **La direzione non è contingente:**
  i due candidati muovono il divario nello **stesso verso** e quasi della
  stessa quantità — 3,21 con `'vicino'`, **4,25 con `'rado'`, 4,60 con
  `'voce'`** — quindi «il charleston anticipa il ride, e più di prima» non
  dipende da quale dei due si scelga. Contingente è **solo l'unanimità
  esatta**, e dipende dall'unica scelta di tutto il ramo presa *dopo* i numeri
  e *contro* la regola scritta prima, che selezionava `'rado'`. Il dissenso
  unico sotto `'rado'` è `drummer1/session1/78`, a **−10,82 tick**, dove la
  **stessa** esecuzione sta a **+8,70** sotto `'voce'`: uno sbalzo di **19,5
  tick** su una sola esecuzione a **290 BPM** — che è per l'appunto un caso
  concreto della colonna «scarto massimo mediano» (1,47 contro 1,97) su cui
  `'voce'` è stato scelto. Anche il controllo sui soli passi 4 e 12 si muove:
  `'rado'` dà **4,31 e 13 su 14**, contro 4,73 e 14 su 14 di `'voce'`. Tutti
  questi numeri escono da `tools/misura_groove.py`, sezione «ride contro
  charleston, sui SOLI passi 4 e 12», che **dal 28 agosto 2026 misura tutti e
  tre i tagli** e stampa nominate le esecuzioni che dissentono: non vengono da
  una revisione, si rifanno rieseguendo lo strumento;
- **e il 15 su 15 che non è mai passato da nessuna catena non si è mosso di un
  decimo**: quello delle **fasi grezze**, qui sotto. È ancora quello da citare
  a chi chiede la cosa più solida di questa casella, e la ragione non è
  cambiata — non attraversa né origine, né swing, né stimatore per passo.

Quel che il 26 agosto **non** ha chiuso, e va detto qui perché il ritorno
dell'unanimità invita a crederlo: lo stimatore nuovo **non** è esente da celle
oltre mezzo passo — ne fa **di più**, non di meno — e lascia aperte due celle
mal ancorate. Vedi le due sezioni della «decisione» e dell'«ancoraggio».

**Cosa regge e cosa cade**, detto stretto:

- **regge la stratificazione come livello**, e a ogni giro più di prima: il
  charleston resta il più anticipato di tutti nella tabella del residuo, e il
  divario mediano contro il ride è cresciuto due volte su due — 2,59, poi
  3,21, poi 4,60 tick;
- **regge la controprova senza niente tolto**: sulle fasi grezze — nessuna
  origine, nessuno swing, quindi né grazia né stimatore per passo possibili —
  il charleston anticipa il ride in **15 su 15**, ed è la riga qui sotto.
  Quella misura non è cambiata di un decimo **in nessuna delle due
  correzioni**, e resta quella da citare a chi chiede la cosa più solida di
  questa casella: è l'unica delle due che non attraversi nessuna catena;
- **l'unanimità sul residuo lavorato è caduta il 24 agosto 2026 ed è tornata
  il 26** — 15 su 15, poi 12, poi di nuovo 15 — e non è la stessa misura che
  torna: il divario sotto è **quasi il doppio** di quello del primo 15 su 15.
  Il paragrafo qui sopra dice perché, e cosa si può controllare per non
  crederci sulla parola.

⚠️ **Il segno, perché è facile invertirlo.** `Passo.scarto` è il residuo
rispetto al passo: **positivo = il colpo cade dopo la griglia**, negativo =
prima. Lo conferma `MU.applica_groove()`, che fa `pos + scarto`. Il charleston
a pedale ha il residuo **più negativo** di tutti (−5,66 dal 26 agosto 2026,
−3,42 prima), quindi è il **più in anticipo**. E la stessa cosa si vede
**senza togliere niente** — né origine né swing — sulle fasi grezze dentro il
movimento, contando i soli colpi entro un
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
entrambi, la stratificazione **cresce** ancora: **4,73 tick e 14 su 14** (14
esecuzioni, 3 batteristi), contro 4,60 e 15 su 15 a passi liberi `[MIS]`. Fino
al 26 agosto 2026 i quattro numeri erano **3,57 e 14 su 14** contro **3,21 e
12 su 15**.

⚠️ **Ma questo controllo non è innocente come sembrava**, e va detto qui
invece che lasciarlo dedurre. Restringersi ai passi 4 e 12 **esclude per
costruzione** i colpi che, tolto lo swing, sono finiti sui passi 3 e 11 — cioè
proprio quelli che anticipano di più — quindi è un campione **potato dalla
parte giusta**. ⚠️ **Dal 26 agosto 2026 la potatura è più piccola, non
sparita:** lo stimatore nuovo riporta sul battere gran parte di quei colpi, e
la quota del charleston sui passi 3 e 11 scende da 17,5% a **11,6%** — ma più
di un decimo dei suoi colpi resta fuori dal controllo. E il controllo ha smesso di
essere quello che *ritrova* l'unanimità, visto che a passi liberi non è più
persa: oggi dice solo che il confondimento posizionale non spiega la
stratificazione. Restava, e resta, da non citare come «e sui passi dove
suonano entrambi è comunque quindici su quindici»: sui passi 4 e 12 le
esecuzioni appaiate sono **quattordici**.

⚠️ **E il template resta il caso estremo, come lo era prima.**
`drummer1/session3/2` — l'esecuzione che questa casella raccomanda più sotto
come groove template — sta a **+0,37 tick**, cioè **1,3 ms** a 185 BPM:
**ultimo della fila**, cioè il meno stratificato dei quindici, ma dalla parte
del disegno `[OSS]`. Le tre versioni di questo numero, tutte sullo stesso
file: **+0,08** con la grazia, **−0,25** dal 24 agosto 2026 — terzo dal fondo
e appena dalla parte sbagliata — **+0,37** dal 26. Su quel file la
stratificazione, comunque la si misuri, è **la più piccola del campione**: un
terzo di tick, cioè poco più di un millisecondo, non è un pocket a strati.

⚠️ **Una cosa però è cambiata di verso, e va scritta.** Fino al 26 agosto
2026 questa riga diceva che «con uno stimatore appena diverso il segno cambia
ancora», perché la mediana sui **colpi** dava −0,25 e quella sui **passi** non
pesata dava **−4,60**. Oggi le due **concordano nel segno**: sui colpi
**+0,38** — che è il +0,37 della fila, arrotondato dall'altra parte — e sui
passi **+1,62** `[MIS]`. La ragione della vecchia divergenza
era che i positivi grossi del charleston stavano su celle rade mentre i suoi
due passi dominanti erano negativi; ora quelle celle rade si sono
ricompattate. Resta vero che le due letture **non danno lo stesso numero** — è
sempre un file su cui la stratificazione è troppo piccola per essere robusta —
ma non danno più due segni. **La conclusione aggregata non dipende da lui**:
togliendolo restano **14 su 14** con mediana **+4,66**, su **14 esecuzioni e 3
batteristi** `[MIS]` (erano 12 su 14 e +3,33 fino al 26 agosto).

⚠️ **E questo CONFERMA metà dell'`[IPO]` del comune, non lo smentisce.** «Ma
swing e laid-back non sono la stessa cosa» riporta da `music-composition` un
pocket a strati con *«cassa sul tempo, rullante appena dietro, charleston
appena avanti»*. Il **charleston appena avanti c'è**, ed è la cosa più solida
che questa casella misuri.

Quello che **non** si trova è il resto — e va detto con precisione, perché il
numero e il verbo qui vanno letti insieme. Il **rullante dietro alla cassa**
non c'è nemmeno **come segno**: la mediana è **−0,69 tick** dal 26 agosto 2026
(−0,21 dal 24), e negativo vuol dire *prima*. E non c'è **come
sistematicità**, che è quel che servirebbe per chiamarlo uno strato: **il
rullante sta dietro alla cassa in 9 esecuzioni su 21, e davanti nelle altre
12** `[MIS]` — è la riga «rullante − kick» della tabella qui sopra, letta dal
capo che qui interessa, e il conteggio **non si è mosso in nessuna delle due
correzioni** — cioè testa o croce, e il divario vale **due terzi di tick**
contro i 4,60 che separano il piede dal ride. Un segno rovesciato e un
conteggio da testa o croce non fanno uno strato. Fra i tre strumenti battuti,
insomma, non c'è ordine, e il pocket a strati del jazz è **un solo strato**:
il piede.

#### Cosa esclude il test del tempo — e cosa no

⚠️ **Prima di cuocere quei 3,2 tick in un template.** Su un kit elettronico un
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
stesso fatto letto dall'altro capo — «ride − charleston = +4,60» e «charleston
− ride = 4,60 tick prima» sono la stessa riga, non due misure.

Le due ipotesi fanno previsioni **opposte** sul divario: se è una frazione del
movimento la pendenza è **zero**; se è una latenza fissa in millisecondi la
pendenza vale `ms × 96/60000` ed è **dello stesso segno del divario**, cioè
positiva. Su `beat` 4/4 senza funk e fusion `[MIS]`:

| divario | esec. | batt. | mediana | pendenza misurata | da costante-in-tick | da latenza fissa |
|---|---|---|---|---|---|---|
| ride − charleston | 15 | 3 | +4,60 tick (+21,2 ms) | **+0,0033 ± 0,0110** | **0,3 σ** | +0,0340 → **2,8 σ** |
| kick − charleston | 18 | 2 | +4,83 tick (+16,9 ms) | +0,0135 ± 0,0136 | **1,0 σ** | +0,0270 → 1,0 σ |
| rullante − charleston | 22 | 3 | +2,64 tick (+13,0 ms) | −0,0475 ± 0,0179 | 2,6 σ | +0,0208 → **3,8 σ** |

⚠️ **Questa tabella è del 26 agosto 2026, e va letta diversamente da come
questa casella la leggeva il giorno prima.** Fino ad allora diceva: ride
+3,21 tick (+13,5 ms), pendenza −0,0156 ± 0,0140, 1,1 σ e 2,7 σ; cassa +1,91
(+8,5 ms), −0,0120 ± 0,0106, 1,1 σ e 2,4 σ; rullante +2,09 (+12,1 ms), −0,0345
± 0,0128, 2,7 σ e 4,2 σ. Due cose sono cambiate di **verso**, e nessuna delle
due si vede guardando solo i divari.

**La latenza fissa in millisecondi non è più fuori su tutte e tre**, e la
forza va detta coppia per coppia con lo stesso metro di prima — un rifiuto
netto sopra i 3 σ, un'indicazione sotto: **3,8 σ** sul rullante, che è il
rifiuto netto; **2,8 σ** sul ride, che è un'indicazione forte; e ⚠️ **1,0 σ
sulla cassa, dove non c'è più nessun rifiuto.** La pendenza della cassa
(+0,0135) cade **esattamente a metà** fra le due previsioni, a un sigma da
ciascuna: quella coppia, oggi, non distingue niente. Chi citava «rifiutata su
tutte e tre» cita un numero che il cambio di stimatore ha portato via, come la
correzione della catena aveva portato via il «circa 4 σ su tutte e tre» due
giorni prima.

⚠️ **E il segno della pendenza non è più opposto su tutte e tre.** Fino al 26
agosto 2026 lo era su tutte e tre; oggi lo è **solo sul rullante**
(−0,0475). Su ride e cassa la
pendenza è **positiva**, cioè dello stesso segno che la latenza fissa prevede
— ma sul ride è **un decimo** della grandezza prevista (+0,0033 contro
+0,0340), che è il motivo per cui la rifiuta lo stesso. «Segno opposto» e
«troppo piccola» sono due modi diversi di non essere una latenza fissa, e
scriverli come se fossero lo stesso sarebbe scrivere il contrario di quel che
c'è.

**Due divari su tre restano indistinguibili da costante in tick** — ride e
cassa — che è la firma di una grandezza proporzionale al movimento, e sul ride
la compatibilità si è **stretta**, da 1,1 σ a **0,3 σ**. Per il terzo, il
rullante, non regge nessuna delle due ipotesi pure: il divario si
**restringe** al salire del tempo (2,6 σ da zero). Cioè **una sola coppia
oggi discrimina davvero**, ed è il ride: 0,3 σ da costante-in-tick contro 2,8
dalla latenza fissa.

⚠️ **Prima della correzione del 24 agosto questa sezione diceva quasi il
contrario**, ed è onesto tenerlo accanto: dava la latenza fissa fuori a ~4 σ
su tutte e tre e la costante-in-tick compatibile con **una sola** coppia. Il
24 agosto le due letture si sono scambiate il peso — la costante-in-tick ne
reggeva **due**, il rifiuto netto **una**. Il 26 agosto la direzione **non si
è invertita di nuovo**: è la stessa, e più marcata sul ride, più debole sulla
cassa.

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
| ≤ 110 BPM | 6 | 3 | −5,17 | −5,30 | 1,76 | 0,72 |
| 110-130 BPM | 8 | 3 | −6,50 | −6,17 | 3,44 | 1,22 |
| > 130 BPM | 9 | **2** | −5,65 | −4,87 | 4,39 | 1,46 |

⚠️ **E si guarda, non si conclude.** Un livello ha lo zero arbitrario detto
qui sopra, quindi da questa tabella non esce nessuna prova: la conclusione la
porta la regressione appaiata, che è sul divario. Questa tabella sta qui per
mostrare il **rumore** che c'è sotto, ed è tutto quello che le si può chiedere
— **le tre mediane vanno lette per quello che sono.** Dal 26 agosto 2026 non
sono ordinate affatto: −5,17, poi **−6,50**, poi −5,65, cioè è la fascia di
**mezzo** la più anticipata e le due esterne stanno quasi assieme. Fra la più
e la meno anticipata ci sono **1,33 tick**, con errori standard di
**0,72-1,46**: nessun andamento, in nessuno dei due versi. ⚠️ **E le tre
versioni di questa tabella dicono tre cose diverse, il che è precisamente il
punto.** Fino al 24 agosto le tre mediane coincidevano a 0,07 tick e questa
casella lo chiamava «una coincidenza, non una precisione». Dal 24 al 26
andavano da −4,06 a −2,11 su errori standard di 0,70-0,82, cioè poco più di
due errori standard su tre punti scelti a mano, con la fascia discriminante
fatta di **due batteristi**. Dal 26 non vanno da nessuna parte. Tre letture
diverse dalla stessa tabella in tre giorni sono la prova, non l'eccezione:
**un livello non decide niente**, né quando è piatto, né quando pende, né
quando fa la gobba. È la regressione appaiata a reggere la conclusione, non
questa tabella. E la colonna in millisecondi che compariva qui in una versione
precedente **non era un secondo riscontro**: è `tick × 60000/(BPM × 96)`, aritmetica sugli stessi
numeri.

**Cosa il test esclude, detto stretto:** che il divario fra il charleston e gli
altri pad sia un ritardo **costante in millisecondi**. Nient'altro — e con la
forza che la riga qui sopra dichiara, che dal 26 agosto 2026 è **3,8 σ sul
rullante, 2,8 sul ride e 1,0 sulla cassa**, dove quindi non esclude più
niente. Su una delle tre — il rullante — cade anche l'ipotesi opposta.

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
**0,3 σ sul ride e 1,0 sulla cassa**, ma **2,6 σ sul rullante** — la coppia per
cui, più sopra, «non regge nessuna delle due ipotesi pure». ⚠️ **E qui la
correzione del 24 agosto 2026 ha rovesciato il conto**: prima erano *due su
tre* a respingere questa versione, dopo è diventata **una su tre, e a 2,7 σ**.
⚠️ **Il 26 agosto 2026 non l'ha rovesciato di nuovo, l'ha stretto nello stesso
verso:** resta una su tre, a 2,6 σ, e sul ride l'accordo passa da 1,1 a **0,3
σ**. Il pedale proporzionale al movimento non è più la versione che i numeri
stringono di più: è quella che ne regge due su tre. Resta però **supposta**, e
per le due supposizioni che chiede — vedi il paragrafo qui sopra. Un pedale
che scattasse presto di un numero **fisso di millisecondi** resta invece rifiutato dalla
stessa regressione, come i pad battuti. La domanda del titolo — mestiere o
pedale — resta **senza risposta**; quel che è cambiato è che del pedale
sopravvive una versione **meno stretta di quanto questa casella scrivesse**.

⚠️ **E il confronto è sempre e solo fra pad.** `GR.origine()` toglie già lo
scarto comune a tutto il kit, quindi qui si esclude una latenza **di quel pad
rispetto agli altri** — mai una latenza di cattura della registrazione, che
essendo comune a tutti è **invisibile per costruzione**.

⚠️ **E prima di tutto: 21,2 ms.** Il divario ride/charleston, che è il più
largo dei tre, in millisecondi vale **21,2 ms** dal 26 agosto 2026 — cioè
appena **dentro** la finestra di 20-40 ms che il comune dichiara udibile. È
l'unica grandezza di questa sezione che con quella finestra si possa
confrontare, per la ragione detta più in alto: gli altri numeri sono livelli, e
un livello ha lo zero arbitrario. La stratificazione è **misurata bene e
piccola**: che si senta è un'altra affermazione.

⚠️ **E qui una frase di questa casella si è rovesciata, con una data.** Fino
al 26 agosto 2026 il divario valeva **13,5 ms** e la riga qui sopra diceva
**«sotto** la finestra». Non lo è più. Chi cercava in questa casella
l'argomento «tanto la stratificazione sta sotto la soglia dichiarata» non lo
trova più, e **non perché sia stato tolto: perché il numero l'ha attraversata**
salendo. Il che non dice che si senta — dice che quell'argomento non è
disponibile.

⚠️ **E dal 24 agosto 2026 quella finestra va maneggiata con due cautele.** La
prima: i 21,2 ms sono un divario **fra due strumenti**, cioè una grandezza
*relativa*, mentre la finestra qualifica **uno** spostamento contro la griglia.
Sono due domande diverse, e il comune ora le tiene separate — «Le due domande
sono diverse, e la soglia dipende dal tempo». Che la stratificazione si senta
**non è stato provato**: quei millisecondi non sono mai stati messi davanti a
un orecchio, e gli ascolti del 24 agosto (qui sotto) non permettono di
dedurlo, perché da lì **non esce nessuna soglia**.

La seconda, che è più insidiosa: **i 21,2 ms non sono un numero, sono 4,60
tick letti a un tempo.** Sono la conversione fatta col BPM di ciascuna
esecuzione — è detto qui sopra — e la stessa quantità **scritta** in una song
vale altri millisecondi: 4,60 tick sono 15,5 ms a 185 BPM, **28,8 a 100**,
47,9 a 60. Cioè **se la stratificazione misurata si senta dipende dal tempo a
cui la si scrive**, non solo da quanto è grande; e a 185 BPM, il tempo
dell'esecuzione da cui il template viene, sarebbe due terzi. ⚠️ **A 100 BPM
sono 28,8 ms, cioè dentro la finestra del comune e non più al suo bordo.** La
serie delle tre misure, alla stessa velocità di scrittura, è **16,2 → 20,1 →
28,8 ms**: sotto la finestra, poi al suo bordo inferiore, poi dentro. Il che
continua a non dire che si senta.

#### Due grandezze diverse, e la domanda che resta aperta

⚠️ **Le mediane aggregate non sono quello che un template scrive**, e
confonderle sarebbe comodo e falso. Le mediane qui sopra stanno entro 5,7 tick
perché sono **mediane su decine di esecuzioni**; il profilo di **una**
esecuzione porta invece uno scarto **per ogni passo e per ogni strumento**, e
`MU.applica_groove()` li applica **tutti**, senza nessuna soglia.

Sul template raccomandato, quindi `[OSS]`, coi valori di prima del 26 agosto
2026 in *corsivo* accanto:

- il **massimo spostamento singolo** è **−19,11 tick = 64,6 ms** a 185 BPM
  (splash, passo 12) — *era +11,80 tick = 39,9 ms, ride, passo 13*.
  Confrontato con la finestra 20-40 ms del comune — che qualifica *uno*
  spostamento, ed è quindi la grandezza giusta da metterle accanto — le sta
  ora **oltre il bordo superiore**, dove prima ci stava dentro per un pelo. Ed
  è cambiato anche il **segno**: quel colpo prima era in **ritardo** sul suo
  passo, ora è in **anticipo**;
- l'**escursione picco-picco** fra tutti i passi e tutti gli strumenti è
  **27,36 tick = 92,4 ms** — *era 22,83 tick = 77,1 ms*. Ma è la distanza fra
  il colpo più anticipato e il più ritardato del kit, non uno spostamento: a
  nessuna nota viene applicata.

⚠️ **E qui i due numeri vanno in due versi opposti, il che è la cosa
importante di questa sezione.** L'escursione su **tutti** i passi **sale**
(22,83 → 27,36 tick), ma quella sui soli passi che la tabella del profilo
tiene — almeno il 5% delle battute, cioè 10 colpi su 193 — **scende**: da
**15,78 a 13,57 tick** `[OSS]`. Non è una contraddizione: le due misurano cose
diverse, e la prima è dominata dalle celle con **un colpo solo**, che sono
esattamente quelle che il cambio di stimatore ha ridistribuito. **Riportare
solo la salita, o solo la discesa, sarebbe una mezza verità in tutt'e due i
versi.** La lettura onesta è che **il grosso del template non si è mosso** —
la riga sogliata, che è quella con dei colpi sotto, cala — mentre gli estremi
rumorosi si sono ridistribuiti fra strumenti diversi.

⚠️ **E gli estremi poggiano su 1-4 colpi, come prima.** I cinque scarti più
grandi vengono da passi colpiti **una volta sola** (splash passo 12, kick
passi 1 e 9, charleston passo 9) o quattro (tom basso passo 7) su **193
battute** `[OSS]`. Fino al 26 agosto 2026 erano ride passo 13, china passo 11,
charleston passo 5 e splash passo 15 con un colpo, rullante passo 1 con tre:
**cambiano i nomi, non la natura**. Non sono feel: sono il colpo isolato di un
batterista che si sposta, misurato come se fosse una regola. Chi costruisce un
template farebbe bene a **guardare i colpi prima dello scarto** —
`GR.profilo()` li riferisce — perché `applica_groove()` non distingue fra un
passo da 174 colpi e uno da 1.

⚠️ **E dal 26 agosto 2026 c'è una ragione in più per guardarli.** Il taglio si
sposta sulla **fase media della voce**, e una voce rada quella fase media la
determina male: lo splash che porta il massimo spostamento è così raro che la
tabella qui sopra non lo stampa nemmeno, perché in tutta l'esecuzione ha meno
di venti colpi. Su una voce così, lo scarto può arrivare **vicino a un passo
intero** — i −19,11 tick su 24 di questo caso — cioè il template può posare
una nota nel **territorio del passo accanto**. Sulle voci portanti, che di
colpi ne hanno centinaia, non succede: le celle del charleston stanno fra
−4,7 e +6,4.

**E se non si sentisse affatto?** Era la domanda che questa casella non poteva
chiudere. I 64,6 ms del colpo estremo sono oltre la finestra udibile, ma
poggiano su un colpo solo; la stratificazione che è **misurata bene** vale
21,2 ms, cioè appena **dentro** quella finestra. «Rappresentabile» non è
«percepibile». **Se all'ascolto il residuo non si fosse distinto**, il valore di
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
`[OSS]`. Che il dispositivo **conservi** quelle posizioni è un'altra
affermazione e sta nella casella 10: qui c'è **solo quello che si sente**.

⚠️ **La coppia è quella del 24 agosto 2026, ed è stata costruita PRIMA che la
finestra di grazia fosse tolta** da `GR.profilo_da_colpi()` (il difetto è stato
trovato quel giorno stesso, dopo l'ascolto; il commit che lo chiude è `18f26e5`,
del 25 agosto). I numeri di questa sezione sono quindi veri **di ciò
che è stato ascoltato**, ed è per questo che restano scritti così. Rifacendo
oggi la stessa catena la riga del pedale esce a **−4 tick** invece di −3, e con
lei cambiano **altre otto posizioni su 31**. `tools/genera_groove.py` descrive
come la coppia è stata fatta e stampa i due file nota per nota: **non è un
pulsante da premere.** Eseguirlo **sovrascriverebbe l'unico esemplare** di
`out/GROOVE0.XML` e `out/GROOVE1.XML` — i file su cui poggiano sia i quattro
ascolti qui sotto sia il giro sul dispositivo della casella 10, **31 posizioni
su 31 conservate** — e l'unica traccia che ne resterebbe è l'hash che il
registro di sessione conserva, `d781262c…` per `GROOVE1` e `853bcdec…` per
`GROOVE0`. Chi volesse la coppia col codice di oggi la scriva **altrove**, e la
confronti con questa invece di sostituirla.

⚠️ **E dal 26 agosto 2026 le ragioni per non rigenerarla sono due, non una.**
Alla finestra di grazia si aggiunge il **cambio di stimatore per passo**:
`tools/genera_groove.py` chiama `GR.profilo()` **senza passare `taglio`**,
quindi segue in silenzio il default del modulo, che oggi è `'voce'`. La coppia
ascoltata è perciò costruita sotto il **vecchio** default, e i residui che
porta non sono quelli che uscirebbero oggi. Il divieto **non si allenta perché
i numeri si sono mossi: è esattamente quando si sono mossi che serve.**

⚠️ **Questo NON tocca l'A/B dello swing**, e la distinzione va tenuta ferma
perché è facile sbagliarla. `out/SWINGA.XML` e `out/SWINGB.XML` non passano da
`GR.profilo()`: `tools/genera_swing.py` chiama `GR.origine()` e
`GR.bur_da_posizioni()` direttamente sulle posizioni MIDI grezze, e il BUR è
calcolato **prima** che un passo venga assegnato, senza mai vedere `taglio`.
Il valore che `S.set_swing()` scrive è quindi **intatto** — 1,48 su 41
esecuzioni, levare 59,7%, identico nei tre modi — e **l'A/B dello swing già
ascoltato sta in piedi così com'è.** La coppia costruita sotto il vecchio
default è `GROOVE0`/`GROOVE1`, non `SWINGA`/`SWINGB`.

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

⚠️ **Quei −3 tick sono della coppia del 24 agosto 2026**, costruita prima che
fosse tolta la finestra di grazia: col codice di oggi la stessa riga uscirebbe
a **−4 tick** — 25 ms a 100 BPM invece di 18,75 — e la coppia sarebbe un'altra.
La tabella qui sopra resta com'è perché è **ciò che è stato ascoltato**;
l'avvertenza per esteso, e il motivo per cui quei due file non vanno
rigenerati, sono in cima a questa sezione.

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
- **se la stratificazione misurata si senta.** I **21,2 ms** del divario
  ride/charleston non sono mai stati messi davanti a un orecchio, e per quanto
  detto qui sopra non basterebbe metterceli una volta. ⚠️ Erano 13,5 ms fino
  al 26 agosto 2026, cioè **sotto** la finestra dichiarata dal comune; ora ci
  stanno **dentro**, il che rende la domanda più interessante e non meno;
- **la stratificazione non è mai entrata in gioco.** Il template ascoltato è
  `drummer1/session3/2`, che di stratificazione ne ha **+0,37 tick** — ultimo
  della fila, come questa casella già dichiara più sopra: su quel file la
  stratificazione è la più piccola del campione, quindi l'ascolto non poteva
  né confermarla né smentirla. La coppia da fare adesso è su
  **`drummer10/session1/1`** (`jazz/swing`, 124 BPM, 164 s, BUR 1,82): sui passi
  4 e 12 il suo charleston a pedale sta a **−10,7 e −11,2** tick e il ride a
  **−2,7 e −4,0**, cioè **8,04 e 7,20 tick di divario** sui due passi più
  colpiti di ogni battuta, contro **+1,62 e −0,50** della stessa misura su
  `drummer1/session3/2` `[OSS]` su due esecuzioni. E lì il ride **è** `ride`
  (219 colpi, spang-a-lang su 0-4-6-8-12-14): niente trappola del nome GM.

  ⚠️ **Questi quattro numeri sono stati rimisurati il 26 agosto 2026, ed è
  proprio la coppia che questo lavoro ha spostato.** Fino a quel giorno il
  divario era di **5,64 e 5,93** tick, coi passi 4 e 12 a −8,3 e −9,8 contro
  −2,7 e −3,8, e su `drummer1/session3/2` valeva +1,00 e −0,37. Chi costruisce
  la coppia deve usare i numeri nuovi: le celle su cui poggia sono
  **esattamente** quelle che il cambio di stimatore ha ricompattato.

  ⚠️ **E quella non è più l'esecuzione col battere in minoranza** — lo era
  fino al 26 agosto 2026, ed è la ragione per cui questa riga esisteva. Il
  charleston portava **41 e 42 colpi sui passi 3 e 11** contro **29 e 19 sui 4
  e 12**; ora porta **20 e 32** contro **50 e 34**, cioè il piede sul 2 e sul 4
  è tornato in maggioranza su tutt'e due i movimenti. Resta però da guardare
  che sul **12** il margine è sottile (34 contro 32), e che il divario si
  misura **sui colpi che stanno sul battere**: una coppia costruita con
  `MU.applica_groove()` su un pattern che chiede il piede sul 4 e sul 12
  prende solo quelli. Le sezioni «Il bordo fra due passi» e «La decisione: il
  taglio si sposta per voce» dicono perché.

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

⚠️ **E dal 26 agosto 2026 uno scarto può arrivare vicino a un passo intero.**
Lo stimatore per passo sposta il confine fra due passi sulla fase media della
voce, quindi il residuo non è più limitato a mezzo passo: su una voce rada può
posare una nota nel **territorio del passo accanto**. Sul template
raccomandato il caso estremo vale **−19,11 tick su 24**, e sta su una voce da
meno di venti colpi. Quanto pesa, e perché non si è scritta una regola per
chiuderlo, stanno in «Il limite che resta: l'ancoraggio». A renderlo visibile è
la **cella stessa**: `GR.profilo()` riferisce `Passo.scarto` e `Passo.colpi`, e
uno scarto oltre mezzo passo — impossibile prima del 26 agosto 2026 — su una
cella che porta il gesto mentre il battere accanto è quasi vuoto è la firma del
caso.

⚠️ **Correzione del 28 agosto 2026.** Fino a quel giorno questa riga diceva che
«`senza_appoggio` è ciò che lo rende visibile invece che silenzioso». È falso:
`senza_appoggio` elenca i passi che il profilo **non ha**, e qui la cella c'è —
è il suo **contenuto** a essere spostato. Il paragrafo del «non inventa», due
capoversi più su, resta vero: parla dell'**altro** caso, quello della cella
**mancante**, che è l'unico che `senza_appoggio` sappia riferire.

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

**Compilata il 29 agosto 2026.** C'è il **vocabolario**, ed è completo:
`MU.armonia()`, `MU.voci()`, `MU.sigla()`, i quattro voicing di `MU.VOICING` —
`chiuso`, `shell`, `senza-fondamentale`, `drop2` — e il dialetto di Weimar, che
`WJ.sigla_weimar()` scioglie **per intero, senza fallimenti**. E c'è ora anche
**la condotta delle parti**, che era il buco dichiarato: `MU.voci_condotte()`,
usata di default da `MU.armonia()`. Come ci si è arrivati, e che cosa copre la
grammatica delle sigle, sta in [`../../HANDOFF.md`](../../HANDOFF.md)
§6-octies; quanti simboli distinti siano stati sciolti, e su quante
occorrenze, in §6-nonies.

### La condotta: cambia dove, non quali

Ogni accordo dopo il primo si posa nella **disposizione che muove meno voci**
rispetto a quello prima. Il primo è l'ancora e sta dove `registro` lo mette.

⚠️ **L'invariante che rende la cosa sicura: si scelgono le ottave, mai le
note.** Le classi di altezza di ogni accordo restano esattamente quelle che
`voci()` sceglie — chi vuole un'altra tensione cambia `voicing`, non la
condotta. Verificato sul primo pezzo jazz: passando il comping dalla tabella
scritta a mano a `MU.armonia()`, **tutte e 59 le posizioni di accordo hanno le
stesse classi di altezza di prima**, e 35 su 59 anche le stesse altezze esatte.

`condotta=False` dà il comportamento precedente, dove ogni accordo era
ancorato a `registro` per conto suo.

⚠️ **E l'orecchio l'ha promossa, il 29 agosto 2026.** Il criterio dichiarato
prima di aprire il lavoro era che la libreria **almeno eguagliasse** la tabella
scritta a mano — `JAZZ05` e `JAZZ06` differiscono solo per il comping, tutto il
resto è identico nota per nota. Il verdetto è stato *«ora il voicing è meglio
di prima»* `[OSS]`: non un pareggio. Vale la riserva di sempre — un
ascoltatore, una volta — ma la direzione è quella.

### ⚠️ Correzione: la fonte NON specificava quello che questa casella diceva

Fino al 29 agosto 2026 qui c'era scritto: *«la chiuderebbe
`assets/jazz-voicings.md` di `music-composition`, che è già la fonte da cui i
voicing vengono e che l'alternanza A/B la specifica: qui manca implementarla,
non trovarla»*. **È falso**, e va tenuto perché è il tipo di riga che manda
una sessione a implementare una cosa che non c'è.

Il paragrafo «Rootless voicings» di quella fonte ha **tre problemi
indipendenti**, tutti verificati in `test_condotta_delle_parti`:

| | |
|---|---|
| **i nomi non sono definiti** | scrive «A» = 3-5-7-9 *(or 7-9-3-5)* e «B» = 7-9-3-5 *(or 3-5-7-9)*, poi aggiunge *«the naming convention depends on the source»* |
| **il suo esempio non usa nessuna delle due forme** | il G7 è `b7-9-3-13`, con la **tredicesima** al posto della quinta |
| **la sua regola fallisce sul suo stesso esempio** | dichiara *«only one voice moves per chord change»*: `Dm7 → G7` ne muove una, `G7 → Cmaj7` ne muove **tre** |

Quel che resta solido è lo **scopo** — *«the voice leading is smooth»* — ed è
quello che si implementa. Sul ii-V-I del documento la funzione dà il suo stesso
`Dm7` e il suo stesso `Cmaj7`.

⚠️ **Il totale del movimento è lo stesso: sei semitoni per tutti e due.** Il
primo rapporto di questo lavoro aveva scritto «sei contro sette» ed era un
errore di aritmetica — il secondo cambio del documento muove 1+2+2 = 5, non 6.
Quel che cambia è la **distribuzione**: il documento fa una voce e poi tre, la
funzione due e due, cioè nessun cambio sobbalza. E ci arriva **senza sostituire
tensioni**, mentre il suo G7 ha bisogno della tredicesima.

### ⚠️ Il minimo movimento è goloso, e su tre giri esce dal registro

**È il difetto che si vede solo su una lunghezza vera.** Provata su un ii-V-I
la funzione sembrava a posto; provata sul blues per **tre giri**, il comping
scendeva di **diciassette semitoni** — da `[57, 60, 63, 67]` a
`[40, 43, 46, 50]` — perché il passo piccolo è sempre disponibile nella stessa
direzione e la scelta golosa lo prende ogni volta.

`MU.DERIVA_MASSIMA = 6` tiene ogni disposizione entro mezza ottava, **in
media**, dall'ancora che `registro` dichiara. Deriva da −17 a −5, estensione
toccata da 27 a 16 semitoni. C'è il test.

**La regola operativa che ne esce:** una funzione che sceglie un passo alla
volta va provata **sulla lunghezza a cui verrà usata**, non su un esempio da
manuale. Tre accordi non sono trentasei battute.

### Cosa resta fuori, e non è poco

- **La sostituzione di tensione** — la tredicesima al posto della quinta che il
  G7 del documento fa. È una scelta di **colore**, non di condotta, e la fonte
  la mostra una volta senza dire quando si applica: inventarne la regola
  sarebbe esattamente ciò che questa casella ha appena finito di correggere.
- **Il ritmo armonico** — quando un accordo cambia, e ogni quanto. Qui il giro
  è una casella per battuta perché così lo porta `wjazzd.db`; che sia una
  proprietà del repertorio non è misurato.
- **Le sostituzioni di accordo** — tritono, ii-V interpolati, turnaround
  alternativi. Il giro letto da `Walkin'` non ne ha nessuna, e la casella non
  dice se sia tipico o sia quel pezzo.

## 8. Melodia e ornamentazione

**Misurata il 29 agosto 2026**, e non su una statistica di comodo: la domanda
è arrivata da un difetto che si è **sentito**. Il primo pezzo jazz aveva un
assolo scritto per centrare la densità mediana del corpus, e la centrava —
media 5,00 contro 5,23 — ma l'utente l'ha giudicato *«poco pirotecnico»*, e la
casella 11 porta il numero che gli dà ragione: **dispersione dimezzata, zero
battute vuote, zero corse**. Da lì la domanda giusta: non *quante* note, ma
**dove**.

Lo strumento è `tools/misura_melodia.py`, l'ultimo giro sta in
`out/melodia_jazz.txt`. Il campione sono i blues **`A12` a feel `SWING`** di
`wjazzd.db` — la forma va nota perché la posizione dentro il giro abbia senso,
ed è anche la forma che si genera. Ogni assolo passa un controllo di
**periodicità** (la sigla alla battuta *b* deve tornare alla *b+12* nell'80%
dei casi); chi non lo passa è **scartato e contato**, non aggiustato: sono 15
su 81, quasi tutti per giri insufficienti.

### L'arco del giro: dove stanno le corse, e dove i silenzi

**66 assoli, 38 solisti, 4808 battute** `[MIS]`. Una **corsa** è una battuta
oltre il terzo quartile *di quell'assolo* e comunque da 8 note in su: la parte
relativa impedisce di misurare chi suona fitto invece di dove accelera, il
minimo assoluto impedisce che in un assolo rado qualunque battuta media
diventi una corsa.

| pos | l'accordo, in un blues | corse | vuote | note (mediana) |
|---|---|---|---|---|
| 1 | I | **13,3%** | 1,7% | 5 |
| 2 | IV | 17,5% | 1,8% | 5 |
| 3 | I | 18,8% | 3,3% | 5 |
| 4 | I | 27,4% | **7,4%** | 6 |
| 5 | IV | 19,4% | 2,3% | 6 |
| 6 | IV | 22,1% | **6,3%** | 6 |
| 7 | I | 23,6% | 3,0% | 6 |
| 8 | I | 27,9% | **10,3%** | 6 |
| **9** | **ii** | **34,4%** | 1,8% | **7** |
| **10** | **V** | **31,4%** | 2,3% | **7** |
| 11 | I | 21,5% | 2,0% | 5 |
| 12 | turnaround | 17,2% | **14,8%** | **4** |

Tre fatti, e nessuno era ricavabile dalla media:

- **le corse culminano sul ii-V**, battute 9-10: **34,4%** contro il **13,3%**
  della battuta 1, cioè **2,6 volte**. La mediana sale a 7 note dove altrove
  sta a 5;
- **i silenzi cadono sulle chiusure di frase** — battute 4, 8 e 12, con 7,4%,
  10,3% e **14,8%**. Sono le tre frasi da quattro battute del blues, e il
  solista respira alla fine di ognuna;
- **la battuta 12 è insieme la più vuota e la più rada** (mediana 4). Ci si
  ferma prima di ripartire, e il turnaround lo si lascia alla sezione ritmica.

**Regge sui singoli, non solo sull'aggregato: 25 solisti su 31** hanno
individualmente più corse sul ii-V che sulle battute 1 e 12. È una proprietà
del repertorio, non l'abitudine di qualcuno.

#### Una corsa dura UNA battuta

Mediana 1, media 1,63, massimo 10 `[MIS]`. **Il 62% delle corse è di una
battuta sola**, il 22% di due, il 10% di tre. Non è un tratto lungo: è uno
scoppio.

#### E le corse si addensano fra loro — la previsione era sbagliata

⚠️ **Scritto perché la previsione era l'opposto, ed era la mia.** Ci si aspetta
la domanda e la risposta: silenzio, poi scoppio. I dati dicono il contrario.

| dopo una battuta… | la successiva è una corsa nel |
|---|---|
| **rada** (fino a 2 note) | **17,6%** (n=800) |
| **piena** | **24,2%** (n=3942) |

Una corsa è **più** probabile dopo una battuta piena che dopo una rada. Un
assolo ha **zone** — tratti fitti e tratti radi — non un'alternanza colpo su
colpo. Chi genera alternando scoppio e silenzio scrive una cosa che nel corpus
non c'è.

### La cella e la scala: quanto lunga dev'essere per essere un motivo

**80 assoli** `[MIS]`. Quanto spesso una cella di *N* intervalli ricompare
nello stesso assolo, contro **la stessa linea mescolata** — che conserva la
distribuzione degli intervalli e distrugge il solo ordine, cioè isola
esattamente ciò che si vuole misurare.

| cella | note | reale | mescolato | rapporto (5 semi) | assoli |
|---|---|---|---|---|---|
| 2 intervalli | 3 | 80,2% | 78,4% | **1,02× - 1,03×** | 51/80 |
| 3 intervalli | 4 | 44,7% | 30,2% | 1,47× - 1,50× | 78/80 |
| 4 intervalli | **5** | 21,9% | 5,0% | **4,22× - 4,66×** | 78/80 |
| 5 intervalli | 6 | 11,3% | 0,6% | oltre **16×** | 73/80 |
| 6 intervalli | 7 | 6,7% | 0,07% | (non citabile) | 69/80 |

⚠️ **Sotto le quattro note non c'è sviluppo motivico: c'è la scala.** A tre
note la ripetizione è **indistinguibile dal caso** (1,02×), e in poco più di
metà degli assoli. Il segnale compare a **quattro** note e diventa netto a
**cinque**, dove una cella ricorre quattro volte più del caso in 78 assoli su
80. Ripetere una cella di tre note non produce un motivo: produce quello che
succederebbe comunque.

⚠️ **E il rapporto va citato solo dove è stabile.** Su celle da 6 e 7 note il
riferimento casuale tende a zero e lo si sta dividendo per quasi niente: fra
cinque semi il valore balla da 16 a 24 e da 84 a 140. Si cita il **minimo**, e
a sette note non si cita affatto un rapporto — si dice che una cella così
lunga **per caso non ricorre**, e quindi ogni sua ricorrenza è voluta. Lo
strumento stampa min e max e marca `BALLA` da sé, così la cosa non va
riscoperta.

⚠️ È la stessa soglia che ha retto il controllo anti-copiatura del pezzo
(casella 11, §6-quindecies dell'handoff), dove tre note in comune erano state
dichiarate «la scala, non una citazione». I due risultati sono indipendenti e
concordano.

### L'ornamentazione: il 3,9% delle note, e il vibrato ha un posto

`wjazzd.db` la annota, in `melody.f0_mod`, e non era stato notato prima.
**166 346 note di assoli a feel `SWING`** `[MIS]`:

| | quota | durata mediana | contro una nota nuda |
|---|---|---|---|
| nessuna | 96,1% | 0,107 s | — |
| **vibrato** | 1,89% | **0,493 s** | **4,59×** |
| slide | 1,48% | 0,102 s | 0,95× |
| bend | 0,25% | 0,102 s | 0,95× |
| fall-off | 0,23% | 0,193 s | 1,80× |

**Il vibrato sta sulle note lunghe** — quasi cinque volte la durata di una nota
qualunque — ed è la sola ornamentazione che si sceglie *per durata*. **Slide e
bend stanno su note di lunghezza ordinaria**: sono gesti di attacco e di
passaggio, non di tenuta. Il **fall-off** sta a metà, ed è un gesto di
chiusura.

⚠️ **Che il Deluge sappia farli è un'altra domanda, e sta nella casella 10.**
Qui c'è dove vanno, non come si scrivono: vibrato è un patch cable LFO →
pitch, slide e bend sono portamento o automazione. Nessuno dei tre è stato
provato sul dispositivo.

### Cosa serve per scrivere una linea, in breve

Le cinque cose da rispettare, tutte `[MIS]` qui sopra:

1. **l'arco del giro:** poche corse all'inizio, il picco sul **ii-V**, il vuoto
   sul **turnaround**;
2. **il respiro a fine frase:** battute 4, 8 e 12, con la 12 la più vuota;
3. **una corsa dura una battuta**, due al massimo;
4. **le corse si addensano**, non si alternano ai silenzi;
5. **un motivo è di almeno cinque note**, e ripeterne tre non serve a niente.

⚠️ **E la cosa da NON fare, che è quella che è già costata:** non scrivere per
centrare una media. La media è già misurata, vale 5,2 note per battuta, e una
linea costruita per rispettarla esce corretta e piatta.

*Cosa manca ancora:* **come una corsa è fatta dentro** — se sale, se scende, se
gira attorno a una nota — e la **collocazione dell'ornamentazione dentro la
frase**, che qui è misurata per durata ma non per posizione. Nessuna delle due
blocca la scrittura di una linea.

## 9. Forma e densità

**Misurata il 30 agosto 2026**, ed è la prima casella aperta sotto la regola
«Le caselle si riempiono su domanda» del comune. La domanda non era un difetto
sentito ma un **limite di capacità**: `genera_jazz.py` sapeva scrivere un blues
e nient'altro, perché la forma era cablata dentro.

### ⚠️ Correzione: la forma era già in casa

Fino al 30 agosto 2026 qui c'era scritto: *«Della forma non c'è ancora niente…
e la chiuderebbe MusicXML o le lead sheet, con la stessa avvertenza della
casella 5: il lettore va scritto, non procurato»*. **È falso.**

`wjazzd.db` ha una colonna `composition_info.form`, e la porta su **tutti e 361**
gli assoli a feel `SWING`. Nessuno l'aveva aperta. È la **seconda** riga
sbagliata trovata in due giorni — l'altra è nella casella 7 — e tutte e due
mandavano a cercare fuori qualcosa che era già su disco. Il perché sta nel
comune, «una casella scritta senza domanda invecchia sbagliata».

### Il vocabolario delle forme

La grammatica è `lettera + numero di battute`, ripetuta, e si legge con
`([A-Z])(\d+)`. **349 assoli swing su 361 hanno una forma scomponibile**; i 12
che restano sono `open`, cioè senza forma — e vanno tenuti fuori, non forzati.

| forma | assoli | cos'è |
|---|---|---|
| **`A8A8B8A8`** | **103** | l'**AABA** di 32 battute, la forma più comune del repertorio |
| **`A12`** | **81** | il **blues di 12 battute** |
| `A16B16` | 32 | 32 battute in due metà |
| `A8B8A8C8` · `A8A8B8C8` · `A8A8B8C12` | 19 | varianti di 32-36 battute |
| `A16` · `A8B8` · `A16A16` · `A16A16B16A16` | 24 | il resto |

⚠️ **E la colonna `template` nomina i due modelli canonici**, che questa casella
citava senza averli: **`Blues`** su 81 assoli e **`I Got Rhythm`** su 19 — cioè
il *rhythm changes*, che è un `A8A8B8A8` con la sua armonia. Sono etichette
scritte a mano dai trascrittori, quindi `[OSS]` sul singolo pezzo ma affidabili
come classificazione.

### L'arco dell'AABA: sale fino al ponte e ricade

**57 assoli, 36 solisti, 6777 battute** `[MIS]`. Stessa definizione di corsa
della casella 8 — battuta oltre il terzo quartile *di quell'assolo* e comunque
da 8 note in su — e stesso controllo di periodicità, qui con periodo 32.

⚠️ **53 assoli su 110 sono stati scartati**, e quasi tutti (35) per «giri
insufficienti»: un giro di 32 battute ne chiede più di 64 per verificare che si
ripeta, e molti assoli AABA sono di uno o due giri soli. È un limite del
metodo, non dei dati, ed è la ragione per cui il campione qui è più piccolo che
nella casella 8.

| sezione | battute | corse | vuote | note (mediana) |
|---|---|---|---|---|
| **A1** | 1-8 | **18,8%** | 5,7% | 5 |
| **A2** | 9-16 | 24,8% | 4,0% | 6 |
| **B**, il ponte | 17-24 | **26,3%** | 3,5% | 6 |
| **A3** | 25-32 | 20,9% | 4,6% | 5 |

**C'è un arco, ed è narrativo:** si parte rado, si cresce, si culmina sul
**ponte**, si ricade sull'ultimo A. Non è un ciclo che si ripete quattro volte:
le quattro sezioni di otto battute hanno densità diverse.

#### Il ponte è la sola sezione che non respira alla fine

Le chiusure di sezione — battute 8, 16, 24, 32 — non si comportano allo stesso
modo, e la differenza è la cosa più utile di questa casella:

| | batt. **8** | batt. **16** | batt. **24** | batt. **32** |
|---|---|---|---|---|
| | fine A1 | fine A2 | **fine ponte** | fine giro |
| battute vuote | **15,6%** | 10,5% | **6,2%** | 7,7% |
| corse | 22,2% | 19,5% | **29,3%** | 16,7% |
| note (mediana) | 4 | 4 | **6** | 4 |

Le fini di A1 e A2 **respirano** — vuote al 15,6% e al 10,5%, mediana 4. La
fine del ponte fa **il contrario**: ha il massimo di corse di tutto il giro
(29,3%) e non si svuota. **Spinge dentro l'ultimo A** invece di lasciargli
spazio.

⚠️ **E questo è un arco DIVERSO da quello del blues**, misurato nella casella 8:
là il punto più vuoto era il **turnaround** (battuta 12, vuoto al 14,8%) e il
picco di corse stava sul **ii-V** (battute 9-10). Le due forme non si
somigliano, e una regola presa dall'una **non vale sull'altra**. È il limite
che il comune dichiara: *su domanda si misura stretto, e stretto vale stretto*.

### I fill, misurati — 18 agosto 2026

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

**Parziale.** Tre correzioni, tutte del **29 agosto 2026** e tutte dallo
stesso pezzo in tre versioni. La casella si è aperta esattamente come
dichiarava di volersi aprire — «al primo pezzo jazz corretto dall'utente» — e
alla terza versione il verdetto è stato *«ora suona molto meglio»*.

⚠️ **Resta parziale, e non per modestia:** tre ascolti dello stesso
ascoltatore sullo stesso pezzo non sono un repertorio di trappole. Quel che c'è
è **un giro che si chiude**, non una casistica.

### Il primo pezzo jazz — 29 agosto 2026

`JAZZ01`: blues di 12 battute in fa, hardbop, tema/assolo/tema, 36 battute,
128 BPM, quattro tracce. Da dove viene ogni cosa, col grado di prova, sta in
[`../superpowers/specs/2026-08-29-primo-pezzo-jazz-design.md`](../superpowers/specs/2026-08-29-primo-pezzo-jazz-design.md);
il generatore è `tools/genera_jazz.py`.

Il verdetto dell'utente, per intero: *«non è niente male… non ho niente di cui
lamentarmi, forse il solo potrebbe essere un po' più pirotecnico, ma come test
va bene così»*.

```
Tengo:            groove, swing, comping, basso, forma e suoni. Nessuna
                  obiezione su niente di tutto questo.
Cambio:           l'assolo, che è poco pirotecnico.
Direzione:        più virtuosismo — i tratti di corsa e i silenzi che un
                  assolo vero alterna, non una densità più alta dappertutto.
Resta regolabile: il tempo (128 è scelto per far coincidere il template col
                  riferimento, non per gusto), il kit (KIT009 è un RX-5,
                  cioè una drum machine), e il numero di giri.
```

⚠️ **«Non ho niente di cui lamentarmi» NON vuol dire che il generatore ha
superato la prova, e la distinzione l'ha fatta l'utente stesso**: ha giudicato
il pezzo *«come test»*, non come musica da tenere. Un pezzo che nessuno voleva
conservare non mette sotto sforzo le stesse cose. Vale poi la riserva che il
comune mette su qualunque cosa esca da un orecchio: un ascolto, un
ascoltatore, nessuna ripetizione.

#### Perché l'assolo è piatto: MISURATO, e non è una questione di gusto

La linea era stata scritta per stare dentro le grandezze osservate su un
assolo vero — `Walkin'`, `wjazzd.db` melid 196 — e **ci sta dentro benissimo**.
È proprio quello il difetto. Note per battuta, 12 battute contro 83 `[OSS]`:

| | l'assolo generato | `Walkin'` (melid 196) |
|---|---|---|
| media | 5,00 | 5,23 |
| mediana | 5,0 | 5,0 |
| **deviazione standard** | **1,58** | **3,16** |
| minimo | 2 | **0** |
| massimo | 7 | **16** |
| battute vuote | **0 (0%)** | 7 (8%) |
| **battute da 8 note in su** | **0 (0%)** | **19 (23%)** |

Media e mediana sono centrate quasi esattamente; la **dispersione è la metà**.
I fuochi d'artificio stanno nel **23% di battute che corrono da 8 a 16 note**,
e il respiro nell'**8% che tace del tutto**. La linea generata non scende mai
sotto 2 e non sale mai sopra 7: ha il centro giusto e **non ha né le corse né i
silenzi**.

⚠️ **La lezione di metodo, che vale oltre questa casella: una statistica
aggregata dice dov'è il centro, non dove sta l'interesse.** Scrivere per
centrare una mediana produce la mediana, e la mediana non è pirotecnica. Non è
un errore di esecuzione — la misura di partenza era giusta e la linea la
rispetta — è che **era la misura sbagliata da rispettare**.

Ne segue un requisito preciso per la **casella 8**, quando verrà aperta: di un
assolo va misurata la **distribuzione nel tempo** — dove stanno le corse, quanto
durano, cosa le precede e cosa le segue — non la densità media. La media è già
misurata e non serve a scrivere.

⚠️ **E non basta alzare la varianza a caso.** Le corse di un assolo vero stanno
in *posti*: dopo un silenzio, verso la fine di una frase, sul turnaround. È
quella collocazione, non la dispersione, la cosa da andare a prendere.

#### Cosa questa correzione NON dice

Il pezzo non ha messo alla prova la lacuna che la **casella 7** dichiara — la
condotta delle parti. Il comping non è stato scritto con `MU.armonia()` ma
**a mano**, calcolando l'alternanza A/B dei voicing senza fondamentale, che è
il ripiego che la casella 7 prescrive. L'utente infatti non se n'è lamentato.
Quel silenzio quindi **non assolve la libreria**: assolve un aggiramento fatto
a mano, che va rifatto ogni volta finché la 7 non è chiusa.

### Il giro si chiude: cinque versioni in un pomeriggio — 29 agosto 2026

⚠️ **È la prima volta in questo progetto che una correzione dall'ascolto viene
convertita in una misura e rimessa nel generatore, con lo stesso orecchio che
approva il risultato.** Fino a qui l'ascolto aveva sempre e solo *aperto*
domande. Le cinque versioni sono una **coppia controllata a cinque**:
batteria, basso e comping hanno le stesse identiche note in tutte — verificato
confrontando i file — e cambia solo la tromba. Ogni verdetto parla quindi
dell'assolo e di nient'altro.

| | l'assolo | il verdetto |
|---|---|---|
| `JAZZ01` | scritto a mano, crome | *«poco pirotecnico»* |
| `JAZZ02` | dalle cinque regole, crome, scale d'accordo | *«alcune note sembrano fuori tonalità… non mi sembra più pirotecnico, soprattutto perché è tutto in ottavi»* |
| `JAZZ03` | pesi misurati sulla tonica, corse in sedicesimi | *«ora suona molto meglio. Le note sono a posto, le corse suonano bene ed è decisamente più pirotecnico»*. Riascoltando: *«le frasi finiscono sempre su note che non hanno molto senso dal punto di vista della gravitazione tonale»* |
| `JAZZ04` | atterraggi misurati **+ motivo cambiato** | **RESPINTA** — *«il solo in generale è peggio di quello precedente, che sbagliava solo la nota di atterraggio… molte note sembrano un po' ardite rispetto alla tonalità»* |
| `JAZZ05` | il cammino della 03 **identico**, e le sole due note di atterraggio | *«molto meglio»* |
| `JAZZ06` | l'assolo della 05 intatto; il **comping** passa dalla tabella a mano a `MU.armonia()` condotta | *«ora il voicing è meglio di prima. Va bene»* |

#### La correzione di JAZZ02, e perché era misurabile

```
Tengo:            l'arco del giro. Sulla forma non ha obiettato ne' la
                  prima ne' la seconda volta.
Cambio:           le note dell'assolo, e la griglia.
Direzione:        piu' vicino alla tonalita' del pezzo, e i sedicesimi.
Resta regolabile: il seme del generatore, i pesi, il registro.
```

⚠️ **«Fuori tonalità» non voleva dire fuori scala, e la misura lo ha
precisato.** `JAZZ02` costruiva la scala **di ogni accordo** — misolidia su F7
e Bb7, dorica su Gm7, misolidia su C7 — che è corretto sull'accordo e sbagliato
sul pezzo. Sui gradi relativi alla **tonica del pezzo**, contro gli 80 assoli e
le 33 714 note della sezione «L'ornamentazione» qui sopra:

| | `JAZZ02` | `JAZZ03` | corpus |
|---|---|---|---|
| **grado 11 sulle corse** (in fa il mi naturale) | **18,8%** | 8,3% | 6,7% |
| grado 3, **la terza blues** | 1,7% | 7,5% | 8,3% |
| grado 6 | 0,0% | 4,5% | 5,0% |
| grado 8 | 0,0% | 6,0% | 4,2% |
| *scarto totale dal corpus* | *41,4* | *33,7* | — |

Il difetto era **uno solo e localizzato**: il grado 11 a quasi il triplo della
sua quota, e **proprio sulle battute 9-10**, cioè sulle corse, dove si sente di
più. Non «note sbagliate»: **troppe** di una nota che nel repertorio c'è ma
sta bassa.

⚠️ **La lezione operativa: non conta solo QUANTE volte una nota compare, ma
DOVE.** La stessa quota distribuita male suona storta lo stesso. Nel generatore
questo è il peso che una nota dell'accordo prende **sui movimenti** — senza,
la distribuzione giusta produceva comunque una linea sbagliata.

#### Gli atterraggi, misurati — e la trappola che ci si è nascosta dentro

Le frasi della `JAZZ03` finivano dove il cammino capitava, perché il
generatore **non sapeva cosa fosse una fine di frase**: sceglieva ogni nota
con la stessa regola. Le tre fini erano il grado 1, il **b3** (la terza blues,
sola in una battuta altrimenti vuota) e l'**undicesima** — su F7 il sib, cioè
la sospensione che chiede il la e non risolveva, proprio a chiudere il giro
dell'assolo.

**Misurato su 1913 fini di frase in 80 assoli** `[MIS]` — ultima nota prima di
un buco di mezza battuta, la stessa soglia con cui le frasi sono contate più
sopra — come grado **sull'accordo sotto**:

| grado | fine frase | ovunque | rapporto |
|---|---|---|---|
| **fondamentale** | 22,1% | 14,1% | **1,57×** |
| **quinta** | 17,1% | 13,3% | **1,29×** |
| **settima minore** | 12,0% | 10,7% | 1,12× |
| terza | 7,4% | 8,2% | 0,90× |
| undicesima | 7,3% | 9,1% | 0,80× |
| nona bemolle | 2,5% | 4,5% | 0,56× |
| settima maggiore | 2,5% | 4,9% | 0,51× |

Le note dell'accordo sono il **58,7%** alle fini contro il **46,3%** ovunque.
Si atterra sullo **scheletro** e si evitano la settima maggiore e le alterate,
tutte dimezzate.

⚠️ **La terza NON è favorita (0,90×)**, ed è controintuitivo: non basta «una
nota dell'accordo», sono quelle tre.

⚠️ **Va applicato come passata a parte, non come peso in più dentro la scelta
della nota.** La misura lo impone: le fini seguono una distribuzione *diversa*
dal resto della linea, non una versione inclinata della stessa — un bonus sul
peso non abbasserebbe mai la terza.

#### La trappola: nel generatore lo stato passa da una battuta all'altra

⚠️ **Questa è la trappola vera del pomeriggio, ed è di macchina, non di
musica.** Per correggere l'undicesima finale la `JAZZ04` aveva cambiato
l'ultima nota del **motivo**. Sembra una modifica di una nota. Non lo è: il
motivo è l'ultima cosa che succede nella sua battuta, quindi la sua ultima
nota è il valore da cui **riparte il cammino della battuta dopo**. Tutto
l'assolo è divergiuto.

| | `JAZZ04` | `JAZZ05` |
|---|---|---|
| slot diversi dalla `JAZZ03`, su 192 | **56** | **2** |
| note cromatiche **sui movimenti** | 12% → **21%** | 12% → **12%** |

Quel passaggio dal 12 al 21 per cento è ciò che l'utente ha sentito come
«ardito», e l'ha sentito **subito**. La `JAZZ05` fa la stessa correzione senza
toccare il motivo: la passata di atterraggio cambia la sola ultima nota della
frase e lascia il cammino dov'era. **Due slot su 192.**

**La regola operativa:** in un generatore che cammina, una modifica sembra
locale e non lo è finché non si guarda **quale stato attraversa la battuta**.
Prima di dire «cambia solo X», si contano gli slot diversi.

#### E una misura aggregata può migliorare mentre la musica peggiora

⚠️ **È successo due volte nello stesso pomeriggio, e la seconda dopo che la
lezione era già scritta qui sopra.**

| | la misura diceva | l'orecchio diceva |
|---|---|---|
| `JAZZ01` | densità media 5,00 contro 5,23 del corpus: **centrata** | *«poco pirotecnico»* |
| `JAZZ04` | scarto dal corpus sui gradi **sceso** da 33,7 a 23,3 | *«peggio di quello precedente»* |

Nel secondo caso lo scarto era stato riportato **come un miglioramento**.
Contava *quante* note di ogni grado e non *dove* cadevano — che è
letteralmente la regola scritta poche righe più su, non applicata alla misura
stessa che la doveva verificare.

⚠️ **Una statistica aggregata non è un criterio di accettazione.** Serve a
trovare *dove guardare*, e la prima volta ha funzionato benissimo — il grado
11 al triplo sulle corse era invisibile a orecchio nudo e la misura l'ha
localizzato. Ma **la promozione la dà l'ascolto**, e una metrica che migliora
non è una prova che qualcosa sia migliorato.

#### Il grado 2, che resta fuori quota ed è dichiarato

Nella `JAZZ03` il grado 2 sta al **17,9%** contro il **9,8%** del corpus, ed è
lo scarto più grosso rimasto. È il sol: su Gm7 è la fondamentale e su C7 la
quinta, quindi prende il peso di nota d'accordo proprio sulle due battute più
fitte. Musicalmente ci sta, e l'ascolto non l'ha segnalato. Sta scritto perché
è il candidato numero uno se un domani qualcuno dirà che l'assolo gira sempre
sulle stesse note.

#### I sedicesimi, e cosa l'ascolto dice davvero del punto aperto

La `JAZZ02` era tutta in crome e l'utente ha nominato **quello** come la
ragione per cui non era pirotecnica. La `JAZZ03` porta le corse a 12
sedicesimi, e **12 note su 128 cadono fra le crome**.

⚠️ **Questo NON chiude il punto aperto di [`../../HANDOFF.md`](../../HANDOFF.md)
§7**, e la distinzione è quella di sempre. Resta ignoto **cosa** il firmware
faccia a una nota che cade fra le crome sotto `set_swing(figura='1/8')`: quel
che si sa adesso è solo che **scriverci sopra non produce niente che suoni
rotto** — *«le corse suonano bene»* `[OSS]`, un ascoltatore, una volta, senza
confronto controllato. Non è una misura del meccanismo: è l'assenza di un
sintomo. La coppia che deciderebbe va **costruita a fase 0,25 e 0,75**, ed è
descritta in §7.

Vale però come **declassamento della sua urgenza**: era una ragione per non
scrivere sedicesimi, e non lo è più.

### La correzione del 24 agosto 2026 — che non è di questo repertorio

**Il 24 agosto 2026 una correzione dall'ascolto era arrivata davvero — ma non
è di questo repertorio, e sta nel comune.** Vale la pena scrivere perché,
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
e quel momento è venuto il **29 agosto 2026**: sta in cima a questa casella.

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
