# Jazz

> Una scheda dello schema neutro. Lo schema, il materiale comune a tutti i
> repertori e l'indice stanno in [`../MUSICA.md`](../MUSICA.md).

Da leggere prima del resto: **nessun pezzo jazz è mai stato generato.**
Quello che c'è in questa scheda o è misurato su un corpus (la casella 4), o è
già in libreria (la 7), o è materiale contato sul disco e non ancora letto
(la 6); niente è passato dall'ascolto dell'utente, perché non c'è ancora niente
da ascoltare. È la ragione per cui sette caselle su undici sono vuote, e per
cui la 11 è vuota **per costruzione** e non per trascuratezza: una trappola del
generatore si osserva, non si prevede.

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

*Nel frattempo, per comporre:* la **casella sorella 4** l'ha già posta senza
dirlo — lo swing è misurato su **coppie di crome dentro il movimento**, quindi
è quella l'unità in cui stanno tutte le domande dalla 4 in poi, e la casella 10
la converte in `figura='1/8'`. Basta a scrivere un pattern. Non basta per
quello che esce dal movimento diviso in due: i metri dispari, e le ballad,
dove la casella 4 stessa sospetta che lo swing si sposti sulle semicrome. Lì
si chiede **all'utente** che pezzo ha in mente, prima di scegliere la griglia.

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

**Vuota.** La chiuderebbe il Groove MIDI, che farebbe per la batteria quello
che la Weimar ha fatto per lo swing: velocity e microtiming di esecuzioni umane
misurati per genere. Non è più in attesa di niente — sta decompresso in
`to-read/MIDI/groove-v1.0.0-midionly/`, e `groove/info.csv` etichetta ogni file
con stile e BPM: **101 esecuzioni con `style` che comincia per `jazz`** (46
esatte, 55 nelle sottocategorie) **su 1150 righe**, contate il 17 agosto 2026
`[OSS]`. Il **prefisso** è la regola giusta, non la sottostringa: cercare
`reggae` dentro l'etichetta prenderebbe anche `latin/reggaeton` e
`latin/brazilian-sambareggae`, che reggae non sono — quante esecuzioni reggae
ci siano davvero sta nella casella 6 di
[`reggae-dub.md`](reggae-dub.md), dove serve a decidere se aprire il corpus.
`to-read/` è in `.gitignore`, quindi chi clona non trova né i file né
il conteggio da rifare: quel numero è lo stato del disco di quel giorno. Manca
solo leggerle, e il lettore c'è già: `MI.batteria()` dà le percussioni per nome
GM, e il suo rapporto PPQ dice quanto microtiming l'arrotondamento si porta
via.

*Nel frattempo, per comporre:* si usa la scala del comune, «Velocity groove» —
i tre livelli e le escursioni per strumento — sapendo che è `[WEB]` e che non
è del jazz: è quello che c'è, non la risposta. Ed è la casella dove il ripiego
può diventare la cosa vera in mezz'ora, perché il corpus non è da procurare ed
è **già sul disco** e il lettore c'è: leggerne una esecuzione con
`MI.batteria()` costa meno che cercare altrove.

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

*Nel frattempo, per comporre:* la si fa **a mano**, e la fonte è quella appena
nominata — `assets/jazz-voicings.md` di `music-composition`, a cui si arriva
dal suo `references/00-navigation.md`. L'alternanza A/B che quel file
specifica si realizza scegliendo il `voicing=` **accordo per accordo** invece
che una volta per tutta la progressione: la libreria non la fa da sola, ma non
la impedisce. `[WEB]` a quello che viene dalla skill.

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

**Vuota.** AABA, il blues di dodici battute, il rhythm changes: niente di
tutto questo è scritto. La chiuderebbe MusicXML, o le lead sheet — con la
stessa avvertenza della casella 5: il lettore va scritto, non procurato.

*Nel frattempo, per comporre:* la forma la sceglie quasi sempre l'**utente**
nominando il pezzo — «un blues», «un rhythm changes» — e allora è decisa e non
c'è niente da cercare. Se non la nomina, la domanda va **alla skill**:
`form/popular-song-forms.md`, dal `references/00-navigation.md`, che ha la
sezione AABA e quella del blues di 12 battute; `[WEB]` a quello che ne esce.
La **densità** invece non è di repertorio: la scala 1-9 e i tempi oltre i
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

Manca tutto il resto: nessun pezzo jazz è mai stato generato, quindi del
suono, dei kit e dell'arrangiamento jazz sul Deluge non si sa niente.

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
