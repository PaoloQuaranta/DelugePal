# Jazz

> Una scheda dello schema neutro. Lo schema, il materiale comune a tutti i
> repertori e l'indice stanno in [`../MUSICA.md`](../MUSICA.md).

Da leggere prima del resto: **nessun pezzo jazz è mai stato generato.**
Quello che c'è in questa scheda o è misurato su un corpus — lo swing nella
casella 4, la dinamica e i fill nelle caselle 6 e 9 — o è già in libreria (la
7); **niente è passato dall'ascolto dell'utente**, perché non c'è ancora niente
da ascoltare, e **niente è stato verificato sul dispositivo**. È la ragione per
cui cinque caselle su undici sono ancora vuote, e per cui la 11 è vuota **per
costruzione** e non per trascuratezza: una trappola del generatore si osserva,
non si prevede.

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
mediana non sta in piedi sulle esecuzioni magre. Sul solo ride, stesso
controllo: 1,99 senza soglia, **2,00** con `[MIS]`.

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

| tempo | esecuzioni | BUR Groove MIDI | BUR Weimar |
|---|---|---|---|
| ≤ 120 | 21 | **1,11** | 1,41 |
| 120-180 | 11 | 1,59 | 1,89 |
| 180-240 | 8 | 1,60 | 1,75 |
| > 240 | 1 | — | 1,35 |

*(la colonna Weimar è quella della tabella «Per tempo» qui sopra, riportata
solo per affiancarla: se un giorno si corregge, si corregge lì.)*

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
da **cinque batteristi di studio** su un kit elettronico `[OSS]`. Le misure si
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
**`jazz/fusion` (11)**, che di swing di crome non ne hanno `[OSS]`. Le misure
di **swing** li escludono, e la casella 4 lo dichiara.

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

| strumento | esecuzioni | mediana | q1-q3 |
|---|---|---|---|
| charleston a pedale | 23 | −3,39 | −4,78 … −2,11 |
| rullante | 26 | −2,17 | −3,10 … −0,20 |
| kick | 22 | −1,23 | −2,68 … −0,50 |
| ride | 18 | −0,81 | −2,02 … +0,21 |

Un tick vale 6,25 ms a 100 BPM e 3,38 ms a 185, quindi **le mediane stanno
tutte entro 3,4 tick**: 21 ms a 100 BPM, 11 ms a 185. Cioè sul **bordo
inferiore** della finestra di 20-40 ms che il comune dichiara udibile, e sotto
di essa ai tempi veloci.

⚠️ **E qui il corpus non conferma il pocket a strati.** Il comune («Ma swing e
laid-back non sono la stessa cosa») riporta da `music-composition` che il
groove è a strati — rullante appena dietro, charleston appena avanti — e lo
segna `[IPO]`. Su questo corpus **non si vede**: le quartili delle quattro
righe si sovrappongono quasi per intero, e dentro **la stessa** esecuzione il
ride sta avanti al rullante in **8 casi su 14**, con differenza mediana di
**+0,34 tick** `[MIS]`. Otto su quattordici è testa o croce. Il residuo del
jazz è dunque piccolo e **non ordinato per strumento**: chi cerca un pocket a
strati non lo trovi qui, e chi scrive un template sappia che sta portando
qualche tick, non un carattere.

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
colpi**); le due **non suonano mai insieme** `[OSS]`. Chi scrive
`dove='ride'` prende quindi il profilo di un quinto di esecuzione, non il
disegno del pezzo. La voce si sceglie **dal numero di colpi e dalla posizione**
che `GR.profilo()` riferisce, mai dal nome — e per un pattern di ride jazz
scritto da zero è più sicuro il profilo **aggregato** della tabella qui sopra,
che sta su 18 esecuzioni e 4 batteristi.

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

**E non alza la voce.** Rullante **42**, cassa **40**, tom basso **67** `[MIS]`:
tutte e tre **sotto** le mediane dei `beat`, che stanno nella tabella della
casella 6 e non si ricopiano qui. Un fill jazz non è un crescendo — è un
cambio di strumento a volume uguale o minore. Il tom in particolare scende
proprio perché cambia ruolo: nei `beat` compare di rado e come accento, nei
fill è la voce corrente.

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

**Parziale.** C'è **quanto** swing e **su quale figura**. Verificato sul
dispositivo è il **meccanismo**, e in tutto il jazz è l'unica cosa che lo sia:
che il display sia la percentuale di posizione del levare, e che
`swingInterval` scelga quale figura viene swingata. Il **62** no: è aritmetica
su quel meccanismo a partire dal BUR misurato sul corpus Weimar, e nessuno
l'ha ancora ascoltato uscire dal Deluge. Serve
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
uno scarto di pochi tick; il rapporto fra le due crome lo mette
`S.set_swing(doc, …, figura='1/8')`, che vale per tutte le tracce insieme —
basso e comping compresi. Un template che portasse anche lo swing lo farebbe
applicare **due volte**, una dal firmware e una dalle posizioni scritte.

⚠️ **Il dispositivo ha un quantize/humanize che cancella il template**, per
riga e **distruttivo**, e chi lo gira non ha modo di sapere cosa sta
sovrascrivendo. Il meccanismo è di macchina e vale per ogni repertorio, quindi
sta nel comune di [`../MUSICA.md`](../MUSICA.md), «La macchina» — qui solo il
rimando, perché copiarlo vorrebbe dire tenerne due copie da correggere.

⚠️ **`length` sulla `<noteRow>` è un meccanismo altro, e non serve qui.** Dà
alla singola riga una lunghezza propria, che **può superare quella della
clip** — quindi è poliritmo, non suddivisione. Serve ai metri dispari e alle
figure che non chiudono con la battuta; **allo swing di crome in 4/4 non serve
affatto**, e usarlo per quello complicherebbe una clip senza cambiarne il
feel. È **osservato nei file e non verificato sul dispositivo**: resta un punto
aperto in [`../../HANDOFF.md`](../../HANDOFF.md) §7, dove sta anche cosa
succede quando riga e clip non sono in rapporto intero.

Manca tutto il resto: nessun pezzo jazz è mai stato generato, quindi del
suono, dei kit e dell'arrangiamento jazz sul Deluge non si sa niente.

⚠️ **E del groove template, sul dispositivo, non è stato verificato niente.**
Il meccanismo dello *swing* sì — è quello che l'apertura di questa casella
dichiara verificato — ma il template è un'altra cosa: **che il Deluge conservi
le posizioni fuori griglia** invece di riquantizzarle non è ancora stato
provato, e finché non lo è, lo scarto in tick che `MU.applica_groove()` scrive
è una scommessa. La velocity, che non dipende dalla posizione, non corre questo
rischio.

*Nel frattempo, per comporre:* di macchina, e non di repertorio, c'è già tutto
il telaio nel comune, «La macchina» — il synth vuoto `TEMPL.XML`, le norme di
sound design, prima la struttura e poi il valore, un drum di kit che è un
`<sound>` completo. Si parte da lì, esattamente come si è partiti per il dub, e
niente di quello vale meno perché il repertorio è un altro. Il **62** qui sopra
invece non è mai uscito da un Deluge: il primo pezzo jazz si fa **ascoltare
all'utente**, e la sua correzione è ciò che riempie la casella 11.

## 11. Trappole del generatore

**Vuota, e per una ragione precisa: nessun pezzo jazz è ancora stato
generato**, quindi nessuna trappola è stata osservata. Questa casella si
riempie al primo ascolto corretto dall'utente, come è successo al dub.

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
