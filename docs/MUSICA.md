# Conoscenza musicale — cosa funziona sul materiale di questo utente

Questo file **non** è una teoria generale della musica: per quella si invocano
le skill (vedi «Le due skill, e chi comanda su cosa», nel comune). Qui sta solo
ciò che è stato imparato correggendo il lavoro, e che nessuna skill generica
sa.

Il perimetro è largo — jazz, poi classica, barocca e antica, poi i
contemporanei: elettronica, IDM, techno, hip hop, trip hop, dub, DnB, jungle —
e un documento a forma di un genere solo non lo regge. Quindi qui stanno tre
cose e nient'altro: **lo schema** con cui si descrive un repertorio qualunque,
**il comune** che vale per tutti, e **l'indice** delle schede. Un repertorio
compilato è una scheda in [`repertori/`](repertori/), una per file.

**Come si legge: lo schema più una scheda sola, mai tutte.** Le schede non
si leggono in fila e non si leggono per intero — si guarda lo schema per sapere
in quale casella cade la domanda, e poi quella casella nel repertorio su cui si
sta lavorando. È la disciplina che `SKILL.md` già prescrive per la skill grande
— si caricano 1-3 file, non di più — applicata al proprio documento invece che
solo a quello altrui.

Stessa disciplina del resto del progetto: si scrive ciò che è stato
verificato, e si segna `[IPO]` ciò che è supposto.

I marcatori, e cosa vuol dire ciascuno:

| marcatore | vuol dire |
|---|---|
| `[MIS]` | misurato su un corpus di musica, col numero e con quanti casi |
| `[WEB]` | preso da ricerca web, con la fonte |
| `[OSS]` | osservato nei file del corpus, coi numeri |
| `[MAN]` | affermato dalla documentazione |
| `[IPO]` | ipotesi non verificata |

**Il marcatore sta accanto all'affermazione che qualifica**, mai raccolto
in una lista a parte: un elenco di «cose misurate» separato dalle cose misurate
invecchia male, e dopo un mese non si sa più quale numero fosse quale.

E una regola contro la duplicazione, la stessa che vale nel codice: **un
numero vive in una casella sola.** Due repertori che si toccano si toccano con
un **rimando**, non con una copia — altrimenti fra un mese ci sono due valori
diversi in due file e nessuno sa quale è stato misurato. E *come* si è
misurato non sta qui affatto: sta in [`FINDINGS.md`](FINDINGS.md) e in
[`ARCHITETTURA.md`](ARCHITETTURA.md). Lì c'è come si è misurato, qui come si
usa.

---

## Lo schema: undici caselle

Le caselle sono formulate come **domande**, non come campi. Il test usato
per sceglierle: **devono sopravvivere sia a Josquin sia alla jungle.** Uno
schema ricavato dai due repertori che il progetto ha già in mano avrebbe
caselle come «griglia a 16 passi» o «velocity groove», e nella musica antica
sarebbero vuote non per mancanza di ricerca ma perché la domanda non si pone.

Il guadagno vero non è l'ordine, è la **collisione**. A documento
organizzato per genere l'*inégalité* barocca e lo swing del jazz non si
sfiorano mai, mentre sono la stessa domanda — dove cade il levare dentro il
movimento — fatta a due repertori. Nello schema cadono tutt'e due nella
**casella 4**, e lì uno dei due ha già la risposta misurata.

Le undici, sempre tutte e sempre in quest'ordine. Nelle schede sono titoli
di livello 2, con esattamente questo testo.

### 1. Cos'è, e cosa non è

I confini, e l'errore tipico di chi lo confonde con un vicino.
**Compilarla** vuol dire saper dire cosa il repertorio *non* è, e con che cosa
lo si scambia. **Vuota** vuol dire che se ne hanno le etichette e non il
mestiere — ed è la lezione più cara del progetto: una ricerca sola su un genere
basta a scrivere qualcosa di formalmente corretto e musicalmente morto.

### 2. Metro e griglia

Quale unità, quanti passi, quanto è rigida la griglia. **Compilarla**
vuol dire poter scrivere un pattern senza chiedersi su che cosa lo si conta.
**Vuota** vuol dire che non si sa in quale unità porre le domande dalla 4 in
poi.

### 3. Tempo

Il range vero, e cosa cambia ai bordi. **Compilarla** vuol dire un
intervallo con dentro il centro del repertorio, non un valore solo. **Vuota**
vuol dire che il tempo si sceglierà per abitudine, e l'abitudine è quella del
repertorio precedente.

### 4. Feel

Dove cadono le note rispetto alla griglia: swing, *inégalité*,
laid-back, rubato — oppure «dritto, ed è una scelta». È la casella dove i
repertori collidono, e l'unica del progetto che abbia numeri `[MIS]`.
**Vuota** vuol dire che si suonerà quantizzato.

### 5. Ruoli e spartizione

Chi occupa cosa, e soprattutto **cosa lascia libero**. Il basso continuo
più le voci, il comping più il walking, le sei parti del reggae: è la stessa
domanda fatta a repertori diversi. **Vuota** vuol dire parti che si
sovrappongono senza che nessuno l'abbia deciso.

### 6. Dinamica

Accenti, fantasmi, dinamica terrazzata — o «non è questo il parametro»,
che è a sua volta una risposta. **Compilarla** vuol dire numeri, non aggettivi.
**Vuota** vuol dire colpi tutti uguali, e un risultato che marcia invece di
respirare.

### 7. Armonia

Vocabolario, ritmo armonico, condotta delle parti. Qui il progetto ha un
buco noto e dichiarato: `MU.armonia()` copre il **vocabolario** — sigle e
voicing — e **non** la condotta delle parti. Una casella 7 che tace su come si
muovono le voci sta tacendo sul pezzo che manca.

### 8. Melodia e ornamentazione

Materiale, sviluppo, e cosa si improvvisa invece di scriverlo.
**Vuota** vuol dire note giuste e nessun discorso: la differenza fra una scala
percorsa e una frase.

### 9. Forma e densità

La scala lunga, l'arco. Questa casella esiste perché tutto il resto di una
scheda descrive **una battuta**:

> Un pezzo ne dura centoventi.

**Vuota** vuol dire un arrangiamento che accende tutte le parti all'inizio e
le lascia accese.

### 10. Sul Deluge

Come si realizza con la macchina che c'è: quali funzioni della libreria,
quali parametri, quali limiti. È l'unica casella che **nessuna skill esterna
può compilare**, ed è dove il progetto è già forte.

### 11. Trappole del generatore

Cosa sbaglia un programma **per costruzione** in questo repertorio. Sta
per repertorio e non in un registro unico, perché «cosa sbaglia un generatore
*qui*» non si trasferisce: le trappole del dub, raccolte in una lista comune,
sembrerebbero lezioni generali e non lo sono.

### Lo stato di una casella, e perché una casella vuota è informazione

La prima riga non vuota di una casella dichiara il suo stato, così si legge
senza contare niente:

| la casella comincia con | vuol dire |
|---|---|
| `**Vuota.**`, o `**Vuota, …**` | non c'è ancora niente |
| `**Parziale.**` | c'è qualcosa, e la casella dice cosa manca |
| qualunque altra cosa | è piena |

**Una casella vuota è informazione, non uno spazio bianco.** «Jazz /
6. Dinamica: vuota» è un compito, e una casella vuota o parziale **dichiara
cosa servirebbe per completarla** — quale lettore, quale corpus, quale misura.
Così l'agenda del progetto si legge dallo schema invece che da una lista tenuta
a parte, e i lettori che verranno atterrano da soli nella casella che
riempiono.

Per lo stesso motivo le undici ci sono **sempre tutte**, anche quando sono
vuote: è quello che permette di sapere dove guardare senza leggere, e di vedere
cosa manca senza che qualcuno debba accorgersene.

---

## Il comune

Quello che vale per **ogni** repertorio. Sta qui e non nelle schede per la
stessa ragione per cui un numero vive in una casella sola: scritto una volta,
si corregge una volta.

Tre parti — **metodo**, come si lavora e a chi si crede; **il mestiere**,
la musica dove non dipende dal repertorio; **la macchina**, il Deluge e la
libreria. Dove un pezzo di comune alimenta una casella precisa, la casella è
nominata.

**Dove sono documentate le funzioni.** Qui e nelle schede i nomi della
libreria dicono *quando* si usa una cosa; firma ed esempio stanno in
[`SKILL.md`](../.claude/skills/deluge-pal/SKILL.md), che le chiama con gli
alias `MU`, `S`, `C`, `A`, `K`, `MI`, `WJ`, `GR` — tabelle «Come si fa»,
«Importare MIDI», «Importare dalla Weimar Jazz Database», «Importare dal Groove
MIDI» — tranne il modulo `sound`,
patch cable compresi, che lì non c'è e sta in
[`HANDOFF.md`](../HANDOFF.md) §6-septies. Scritto qui una volta: una scheda si
legge sempre insieme al comune.

### Metodo

#### Le due skill, e chi comanda su cosa — 17 agosto 2026

| skill | dimensione | a cosa serve **qui** |
|---|---|---|
| `music-composition` | 1,3 MB in 106 file di riferimento | il **mestiere**: forma, sviluppo motivico, densità, transizioni, protocollo di revisione. Si carica 1-3 file per domanda, seguendo `references/00-navigation.md` |
| `music-composer` | 62 KB in tutto | i suoi `scripts/*.py` **producono MIDI**, che `midi.py` sa rileggere. Come prosa è troppo corta per insegnare qualcosa: `genres.md` sono 7,5 KB per ~35 generi |

⚠️ **Una fonte grande non è autorevole su tutto.** `music-composition` è
venti volte più grande dell'altra ed è la sola che insegni il mestiere, ma su un
repertorio che liquida in tre o quattro righe può dire una cosa che qui sarebbe
sbagliata — ed è già successo, su un repertorio che il progetto conosce meglio
di lei. Prima di appoggiarsi a una skill su un repertorio si guarda **quanto
quella skill ne parla davvero**; e quello che ne esce sbagliato si registra
nella casella 11 della scheda, «Trappole del generatore», dove resta attaccato
al repertorio in cui vale.

#### Il corpus non è autoritativo — detto dall'utente, 16 agosto 2026

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

#### Il ciclo di revisione ha un protocollo

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

*(ogni volta che una proposta viene corretta, la lezione va nella casella che
le compete — la 11 della scheda se è una trappola di quel repertorio, il comune
se vale per tutti — con la data)*

#### Si parte dal primo livello della gerarchia — correzione del 16 agosto 2026

**16 agosto 2026 — «leggi anche documentazione», «leggi anche docs
community».** Ero andato dritto ai file saltando il primo livello della
gerarchia del progetto. Da `ARCHITETTURA.md` §9b è poi venuto il pezzo che
serviva davvero e che i file non dicono: la matrice delle sorgenti di
modulazione, il fatto che gli inviluppi che modulano qualcosa di diverso dal
volume sono **bipolari con neutro 25**, e che i parametri globali (delay, mod
FX, riverbero, arpeggiatore, LFO1 rate) accettano **solo** Sidechain e LFO1
come sorgente. Quest'ultima è una regola che, violata, non dà errore: dà
silenzio.

### Il mestiere

#### Velocity groove

*Alimenta la casella 6, «Dinamica».*

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

⚠️ **Questa scala è `[WEB]`, e vale finché un repertorio non ha misure sue.**
È il ripiego onesto: dove nessuno ha aperto un corpus, questi sono i numeri che
ci sono, e valgono per qualunque genere. Ma dove un corpus è stato aperto la
scala misurata **vince su questa**, e un repertorio ce l'ha già: la **casella 6
di [`repertori/jazz.md`](repertori/jazz.md)** porta mediana, quartili ed
escursione per strumento della batteria jazz, con accanto quante esecuzioni e
quanti batteristi sostengono ogni riga. Là i numeri, qui il ripiego — e sono
**diversi**, in qualche riga di parecchio: chi scrive jazz usa quelli, non
questi. **Non si ricopiano qui**, per la regola in cima a questa pagina.

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

#### Ma swing e laid-back non sono la stessa cosa — correzione del 17 agosto 2026

*Alimenta la casella 4, «Feel».*

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
**1 tick ≈ 8,9 ms**. La finestra di microtiming che si sente è 20-40 ms `[WEB]`,
cioè **2-5 tick**: abbondantemente rappresentabile. Lo strumento esiste già ed è
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

⚠️ Il **24 agosto 2026** una parte di questo `[IPO]` è stata messa alla prova
per la prima volta — qui sotto — e non su un basso ma su una batteria. Quel che
si è sentito è la **separazione fra due voci**; che uno strato spostato *suoni*
come pocket invece che come errore resta non ascoltato.

##### La soglia non è una: assoluta e relativa — primo ascolto, 24 agosto 2026

⚠️ **La finestra 20-40 ms qui sopra qualifica UNO spostamento contro la
griglia** — una parte che arriva prima o dopo il tempo, cioè una grandezza
**assoluta**. Quanto due voci che suonano *insieme* debbano separarsi per essere
sentite separate è **un'altra domanda**, e quella finestra non la risponde: sono
due grandezze diverse, e vanno poste separate anche quando si misurano nella
stessa unità.

Il primo ascolto che questo progetto abbia mai fatto di note scritte fuori
griglia — **un ascoltatore, un giro di due battute, metronomo acceso** `[OSS]` —
dice questo e nient'altro:

- uno **sfasamento relativo dentro la finestra**, fra due voci che nell'altro
  file cadono insieme, è stato **sentito**, e attribuito allo strumento giusto;
- un **anticipo assoluto poco sotto la finestra**, di una voce sola contro il
  click, **non** è stato sentito.

I due numeri, la coppia di file da cui vengono e le cautele che si portano
dietro stanno nella **casella 6 di [`repertori/jazz.md`](repertori/jazz.md)**,
che è dove sono stati osservati: qui la distinzione, là il caso.

⚠️ **E si legga per quel poco che è.** Due esiti non sono due soglie: presi
insieme sono **compatibili con la finestra stessa** applicata a tutte e due le
grandezze — quello dentro si sente, quello sotto no. Quindi da qui **non** segue
che il relativo si senta prima dell'assoluto; segue che la finestra `[WEB]`, al
suo primo contatto con un orecchio, non è stata smentita in nessuno dei due
versi. Per separare davvero le due soglie servirebbe lo **stesso** numero di
millisecondi nelle due condizioni, ed è l'esperimento che manca.

**La conseguenza pratica invece regge, e non dipende dalle soglie:** il valore
di un groove template sta nei **rapporti fra gli strumenti**, non nello spostare
il tutto rispetto alla griglia. Uno spostamento uguale per tutti sposta il
*pezzo*, non il groove — e nell'ascolto qui sopra è stato provato nella
condizione più favorevole che esista, una riga sola contro un click, dove un
ascolto normale non ha neppure il riferimento.

#### L'arco di densità

*Alimenta la casella 9, «Forma e densità».*

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

L'arco concreto — quale numero per quale sezione — è di repertorio, e sta
nella casella 9 della scheda.

#### Variare è scelto, non randomizzato

*Alimenta le caselle 6 e 9.*

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

#### Cassa e basso sono una coppia, e va dichiarata

*Alimenta la casella 5, «Ruoli e spartizione».*

`instrument-idiom/bass.md` è netto: «**Do not ignore the kick drum.** Bass
rhythm without kick context is incomplete», e dà quattro rapporti possibili —
unisono con la cassa, basso che riempie i buchi della cassa, basso lungo sotto
cassa fitta, cassa sui movimenti e basso sincopato.

Quale dei quattro rapporti valga è di repertorio, e sta nella casella 5 della
scheda. Comune è che il rapporto vada **dichiarato**, e non lasciato al caso:
**Scritta, diventa una cosa da tenere o da cambiare di proposito**; non
scritta, è una cosa che si rompe senza accorgersene appena si tocca una delle
due righe.

#### La playability è una decisione, non una regola

*Alimenta la casella 5, «Ruoli e spartizione».*

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

### La macchina

#### Norme di sound design — dette dall'utente, 16 agosto 2026

*Alimenta la casella 10, «Sul Deluge».*

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

##### La risonanza non ha una soglia: ha un compenso

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

##### Come si applica quando c'è un LFO sul filtro

Un wobble è `lfo1 → lpfFrequency`, cioè il cutoff **oscilla intorno alla sua
base**. Vanno scelti insieme, non uno per volta: base 25 con ampiezza 18 sta
fra 7 e 43 e resta sempre udibile; base 12 con la stessa ampiezza passa metà
del tempo sotto lo zero, e il wobble diventa un suono che sparisce a
intermittenza.

#### Preset e come vengono usati

*Alimenta la casella 10, «Sul Deluge».*

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

#### Il meccanismo dello swing: quanto, e su quale figura — VERIFICATO il 17 agosto 2026

*Alimenta le caselle 4 e 10.*

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

L'esempio è **illustrativo**: mostra come si nomina la figura, non quale
valore scegliere. I valori per repertorio — quale display per quale BUR —
vivono nella casella 10 della scheda di quel repertorio, e solo lì: un numero
da scrivere con `set_swing()` è realizzazione sulla macchina, non feel. Il
feel — dove cade il levare, e se è misurato o supposto — sta nella casella 4,
e la 10 lo converte.

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

Che l'etichetta nomini la **figura** e non il blocco l'ha stabilito
l'ascolto dell'utente — *«con 8th sento il primo ottavo dritto e il secondo
swingato»*, una frase che descrive la coppia, e la coppia è fatta della figura
nominata. Come si è stabilito tutto questo sta in
[`FINDINGS.md`](FINDINGS.md) §6, in due sottosezioni: «Lo swing: il file usa
una scala, il display un'altra», da cui viene la formula qui sopra, e
«`swingInterval`: quale figura viene swingata», dove stanno anche come ci si
era arrivati sbagliando e cosa resta ignoto del sorgente
(`song.SWING_SCARTO_SORGENTE`). Qui c'è come si usa, lì come si è stabilito.

#### Il groove template: velocity e microtiming da un'esecuzione vera

*Alimenta le caselle 6 e 10.*

Un **groove template** è la velocity e la micro-tempistica di un groove suonato
davvero, prese da un'esecuzione e posate su un pattern scritto. Non è un
effetto del dispositivo e non è una funzione che «umanizza»: è **materiale**, e
si legge da un corpus. Due funzioni, e la seconda è l'unica che scriva:

- `GR.profilo(base, id)` costruisce il profilo da **una esecuzione nominata**
  del Groove MIDI — per ogni passo e per ogni strumento: quanti colpi, con che
  velocity, e con che scarto dalla griglia;
- `MU.applica_groove(note, prof, dove=…)` lo posa su un pattern uscito da
  `MU.passi()`. **Muta la lista** e ritorna il rapporto, non le note; e **non
  inventa**: un passo su cui quel batterista non ha mai suonato lascia la nota
  com'è e finisce in `senza_appoggio`, che va letto.

⚠️ **L'esecuzione va nominata, sempre.** Quello che esce da un profilo è
`[OSS]` **su un esecutore**, non `[MIS]` su un repertorio — e mediare il
microtiming di batteristi diversi lo tirerebbe verso la griglia, cioè verso
zero, perdendo esattamente ciò che si era andati a prendere. Quale esecuzione
scegliere, e perché il nome GM di una riga non è il suo ruolo musicale, è di
repertorio e sta nella casella 6 della scheda.

⚠️ **E il template porta il SOLO residuo: lo swing lo fa la song.** Il rapporto
fra le due crome lo mette `S.set_swing()`, che è un'impostazione **della song**
e vale per tutte le tracce insieme, basso e armonia compresi. Un template che
portasse anche lo swing lo farebbe applicare **due volte** — una dal firmware e
una dalle posizioni scritte — e il risultato non sarebbe «più swingato», sarebbe
sbagliato. Quale valore di swing, e su quale figura, sta nella casella 10 della
scheda; quanto è grande il residuo che il template scrive, nella casella 6.

#### Il quantize/humanize del dispositivo cancella il groove template

*Alimenta la casella 10.*

⚠️ `AUDITION` + `TEMPO`: **in senso orario quantizza, in senso antiorario
umanizza**, e agisce **per riga e in modo distruttivo** — riscrive le posizioni
di quella riga. `[MAN]`, dal manuale della community, e sul dispositivo **non
è stato provato**. Il marcatore copre questa frase e **finisce qui**: tutto
quello che segue è inferenza, e porta il suo.

È il **concorrente diretto** del groove template. Toccano la stessa cosa — la
posizione delle note rispetto alla griglia — quindi non si sommano: **chi passa
per ultimo vince**, e chi ha appena posato un profilo con `MU.applica_groove()`
e poi gira `TEMPO` su quella riga la sovrascrive. Le tre cose che vengono dopo
sono invece tutte `[IPO]`, e vanno tenute distinte dalla riga qui sopra:

- che l'umanizzazione lavori **randomizzando**, mentre il template **misura**,
  è la lettura corrente della parola «humanize» `[IPO]`: il manuale non lo dice
  e nessuno l'ha provato. È la differenza su cui poggia tutto il valore del
  template, ed è la prima da verificare;
- che quindi girare la manopola butti via una misura **nei due versi** — in
  senso orario per riportare le note sulla griglia, in senso antiorario per
  sostituirle con del rumore — segue dalla precedente `[IPO]`, non dal
  manuale;
- che il dispositivo **non lo segnali** è dedotto dal fatto che la manopola
  agisce sulla riga corrente senza chiedere niente `[IPO]`, non osservato.

Si verificano tutte e tre insieme, e con un gesto solo: girare quel comando su
una riga che porta un template, e guardare cosa resta. Va fatto sul
dispositivo, e scritto qui con la data quando arriva.

⚠️ **Il primo giro sul dispositivo, il 24 agosto 2026, NON l'ha fatto — e
apposta.** Quel giro serviva a sapere un'altra cosa: se il dispositivo
**conservi** le posizioni scritte fuori griglia quando si carica e si risalva
una song senza toccare niente. Le conserva `[OSS]`, ed è nella casella 10 di
[`repertori/jazz.md`](repertori/jazz.md). Girare `TEMPO` su una di quelle righe
avrebbe riscritto le posizioni proprio mentre si guardava se sopravvivevano: le
tre `[IPO]` qui sopra restano quindi da verificare **dopo**, su una copia, e da
sole.

Sta qui e non in una scheda perché è meccanismo di macchina e vale per ogni
repertorio — e perché una scheda che tace su un comando che cancella il proprio
lavoro è peggio di una che lo ripete.

#### Quattro inviluppi e quattro LFO, non due — correzione del 16 agosto 2026

*Alimenta la casella 10, «Sul Deluge».*

**16 agosto 2026 — «ora ci sono 4 envelope, non 2».** Un risultato di ricerca
web diceva «2 LFO and envelope options»: era il manuale ufficiale vecchio. Il
firmware community ha **4 inviluppi e 4 LFO**, e `TEMPL.XML` infatti porta
`envelope1..4` e `lfo1..4`. Vale come promemoria che sul firmware community
le fonti generaliste sono indietro, e che il guidebook ufficiale va letto
sapendo quale versione descrive.

---

## L'indice dei repertori

Una matrice repertorio × casella, che dice **senza aprire niente cosa manca
a quale repertorio**. Ogni riga viene dalla prima riga non vuota di ogni
casella della scheda corrispondente: la scheda è la fonte, questa matrice ne
è la vista.

| repertorio | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [reggae / dub](repertori/reggae-dub.md) | ◐ | ● | ● | ◐ | ● | ● | ◐ | ○ | ◐ | ◐ | ● |
| [jazz](repertori/jazz.md) | ○ | ○ | ◐ | ● | ○ | ● | ◐ | ○ | ◐ | ◐ | ○ |
| classica · barocca · antica | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| elettronica · IDM · techno · hip hop · trip hop · DnB · jungle | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |

`●` compilata · `◐` parziale, e la scheda dice di cosa · `○` vuota.

Il **grado di prova** non sta qui: `[MIS]`, `[WEB]`, `[OSS]`, `[IPO]`, `[MAN]`
stanno dentro la scheda, accanto all'affermazione che qualificano. La matrice
dice solo dove c'è qualcosa.

Gli altri repertori del perimetro — classica, barocca, antica; elettronica,
IDM, techno, hip hop, trip hop, DnB, jungle — non hanno un file, e non è una
dimenticanza: un file che dicesse soltanto «vuota» undici volte è rumore da
aprire, mentre una riga d'indice è la stessa informazione a costo zero. Le due
righe aggregate qui sopra, senza link, sono quella informazione: undici
caselle vuote, ripetuto per i due gruppi.
