# Canale SysEx — cosa funziona e cosa no

Sessione del 10 agosto 2026, firmware `0856ff9`, Deluge collegato via USB al PC.

**In breve:** il canale funziona, è corretto ed è usabile. Una song da 269 kB
scaricata via USB MIDI in **59 secondi**, byte-identica alla copia letta dalla
SD. Circa il 70% delle risposte va perso per strada, ma non conta: quello che
conta è quanto costa accorgersene.

---

## 1. Il protocollo, corretto

La documentazione community indica i byte di comando **0x06 / 0x07**. Sono
sbagliati, o descrivono una numerazione precedente. L'enum del firmware
(`src/deluge/io/midi/sysex.h`) dice:

```cpp
enum SysexCommands : uint8_t {
    Ping,       // 0
    Popup,      // 1
    HID,        // 2
    Debug,      // 3
    Json,       // 4   <- richiesta JSON
    JsonReply,  // 5   <- risposta JSON
    Pong = 0x7F
};
```

Con 0x06 il dispositivo **non risponde affatto**. Con 0x04 risponde in 3 ms.
È costato un'ora di diagnosi sbagliata: davo per buona la documentazione e
sospettavo il dispositivo.

Framing verificato sul campo:

```
richiesta  F0 00 21 7B 01 04 <seq> <JSON ASCII> F7
risposta   F0 00 21 7B 01 05 <seq> <JSON ASCII> [00 <binario packed 7/8>] F7
```

### Due superfici SysEx distinte

| prefisso | cosa | stato |
|---|---|---|
| `F0 7D …` | comandi di sviluppo: ping, popup, HID/OLED, debug | funziona |
| `F0 00 21 7B 01 …` | stesso dispatch con manufacturer ID ufficiale, include il servizio JSON | funziona |

Il firmware accetta entrambi i prefissi e imposta un flag interno
`developerSysexCodeReceived` per distinguerli. Osservati e confermati:

```
F0 7D 00 F7          -> F0 7D 7F 00 F7        (Ping -> Pong)
F0 7D 02 00 01 F7    -> 360 byte              (HID: contenuto dell'OLED)
```

### `devSysexAllowed` non blocca il servizio file

Sulla SD `CommunityFeatures.XML` contiene `devSysexAllowed="0"`, e **tutto
funziona lo stesso**: ping, sessione, dir, open, read, close. Qualunque cosa
gati quel flag, non è l'accesso al filesystem via SysEx. L'ipotesi che fosse il
sospetto numero uno era sbagliata.

### La sessione serve

`ping` funziona senza sessione. **Tutte le operazioni su file no.** Senza
sessione la richiesta viene semplicemente ignorata, senza errore.

```json
richiesta  {"session":{"tag":"dsysex"}}
risposta   {"^session":{"sid":2,"tag":"dsysex","midBase":16,"midMin":17,"midMax":23}}
```

Da lì in poi il byte di sequenza deve stare fra `midMin` e `midMax`, cioè
`(sid << 3) | 1…7`. Sette valori per sessione.

Dettaglio osservato: la risposta a `session` arriva con command byte **0x04** e
sequence **0**, non 0x05 — la sessione non esiste ancora quando il firmware
costruisce la risposta. Un client che filtra solo su 0x05 la scarta (ci sono
cascato).

---

## 2. La prova che conta

`/SONGS/Perche.XML` scaricato via USB MIDI e confrontato con la copia letta
direttamente dalla SD:

```
da SD diretta : 28715 byte
via SysEx     : 28715 byte
SHA256        : identici (0726E645…)
```

**Il canale è corretto.** Non c'è mai stata corruzione né troncamento in nessuna
delle prove.

---

## 3. Le risposte si perdono, ma la cosa è gestibile

Circa il 70% delle risposte da 768 byte e il 25% di quelle da 64 non arriva mai.
Le risposte che arrivano non sono **mai** troncate o corrotte.

### La cosa che ho sbagliato a lungo

Avevo descritto il comportamento come «le letture si piantano»: `read` funziona
per un po', poi smette del tutto mentre `close` risponde ancora. Sbagliato.

Non c'è nessun blocco. C'è una **perdita alta e senza memoria**, e quello che mi
faceva sembrare un blocco era il mio timeout: aspettavo 800 ms prima di
dichiarare persa una richiesta, quando **una risposta buona torna in 3-5 ms**.
Ogni perdita costava 200 volte il dovuto, e una sequenza di perdite consecutive
— del tutto normale al 70% — sembrava uno stallo permanente.

Con timeout a 60 ms e abbastanza ritentativi, il fenomeno sparisce: 269 kB
scaricati con **zero riaperture del file**.

### Conseguenza controintuitiva: conviene il blocco grande

Il blocco da 768 byte si perde molto più spesso di quello da 96, eppure è la
scelta migliore. Il costo di una perdita è solo il timeout, uguale per tutti,
mentre il payload è otto volte più grande.

Sweep end-to-end su `Perche.XML` (28 715 byte), hash verificato ogni volta:

| blocco | tempo | kB/s |
|---|---|---|
| 96 | 52,5 s | 0,5 |
| 256 | 18,5 s | 1,6 |
| 384 | 13,8 s | 2,1 |
| 512 | 12,6 s | 2,3 |
| **768** | **7,0 s** | **4,1** |

Monotono: più grande, più veloce, fino al limite di 768. Su `Mark.XML`
(269 779 byte): **59 s, hash identico**.

Anche il timeout conta quanto il blocco. A parità di blocco da 64:
800 ms → ~10 minuti, 120 ms → 124 s, 50 ms → 55 s.

### Tre volte ingannato dalla stessa misura sbagliata

Vale la pena scriverlo perché è costato ore.

1. Primo test: **una sola lettura** per dimensione. «768 va bene.» Non dice
   nulla.
2. Secondo test: **percentuale di successo** su 20-25 letture. Diceva «usa 64,
   è l'unico affidabile». Sbagliato — con ritentativi economici la percentuale
   di successo è irrilevante, conta il *tempo per byte trasferito*.
3. Terzo test: stessa percentuale su una sonda breve, dopo il riavvio, dava
   96 byte al 100% (20/20). Il download vero a 96 byte ha impiegato **422 s
   contro i 59 s a 768**, con 6565 timeout. La perdita compare sotto carico
   prolungato, non nei primi venti messaggi.

L'unica misura che vale è **trasferire un file vero, cronometrarlo e
verificarne l'hash**. Tutto il resto ha portato fuori strada.

### Il limite vero della dimensione

| blocco | esito |
|---|---|
| ≤ 768 | funziona, con la perdita descritta sopra |
| 1024 | **nessuna risposta, mai** |

La documentazione indica 1024 byte come massimo per operazione. Non funziona:
con l'impacchettamento 7/8 il blocco diventa ~1170 byte più il JSON.

Nota metodologica: il primo test misurava una singola lettura per dimensione e
concludeva «768 va bene». Un blocco che funziona una volta non dice nulla. Ma
anche il test ripetuto successivo portava fuori strada, perché misurava la
percentuale di successo invece del **tempo per byte trasferito** — che è la sola
metrica che conta quando i ritentativi sono economici.

### Ipotesi testate e scartate

Tutte le prove sono state fatte con il **Deluge fermo**, non in riproduzione,
con caricata la song vuota di default all'avvio.

| ipotesi | test | esito |
|---|---|---|
| contesa sulla SD dovuta alla riproduzione | dispositivo a riposo | **scartata** — le perdite ci sono comunque |
| le risposte arrivano ma tardi | timeout portato a 6 s | **scartata** — 7/25 a 768 byte, invariato |
| traffico troppo fitto, buffer che non si riciclano | pause da 0, 5, 20, 50, 150 ms fra le richieste | **scartata** — nessuna differenza |
| la porta MIDI sbagliata | provate tutte e tre le coppie del Deluge | **scartata** — 5/25, 8/25, 11/25, 13/25, nessun pattern |

Il firmware esce dal gestore SysEx senza rispondere quando la SD è occupata
(`if (currentlyAccessingCard != 0) return;`), il che darebbe esattamente questo
silenzio — ma con il dispositivo a riposo quella spiegazione non regge.

### Cosa resta: perdita di pacchetti USB

L'unico andamento solido è che **la probabilità di perdita cresce con la
lunghezza del messaggio** e non dipende dal ritmo:

| blocco | risposta | perdite osservate |
|---|---|---|
| 64 byte | ~140 byte | ~25 % |
| 768 byte | ~900 byte | ~70 % |

Il SysEx su USB viaggia in pacchetti da 4 byte. Una risposta da 140 byte sono
~35 pacchetti, una da 900 byte ~225. Con una perdita di circa l'1 % per
pacchetto si ottengono proprio quelle percentuali. E un SysEx a cui manca un
pacchetto è malformato, quindi viene scartato **intero** — il che spiega perché
non si sono mai visti troncamenti o corruzioni.

Dove si perdano i pacchetti non è determinabile da questo lato: può essere il
buffer di trasmissione USB del Deluge oppure la catena di ricezione sul PC
(python-rtmidi su Windows MM).

Il test che discrimina fra le due — un client con uno stack completamente
diverso — è stato fatto, e il risultato è nel paragrafo seguente.

---

## 4. DEx conferma: la perdita non è del client

Dopo un riavvio di PC e Deluge, DEx carica il filesystem — «non funziona sempre,
ogni tanto devo fare retry, ma quando funziona sembra veloce» — e **va in timeout
sul caricamento di una song**.

È lo stesso identico pattern misurato qui: operazioni piccole affidabili,
trasferimento di un file intero no. DEx usa Web MIDI dentro Chrome, cioè uno
stack host completamente diverso da python-rtmidi su Windows MM.

**Due client indipendenti, stesso comportamento: il difetto non è nel codice
client.** Resta il percorso comune — trasmissione USB del Deluge, driver USB MIDI
di Windows, cavo o hub.

La differenza fra i due: DEx ha un timeout da 10 s e non ritenta in modo
aggressivo, quindi si arrende. `dsysex.py` ritenta con timeout da 60 ms e passa.
Non perché sia scritto meglio, ma perché è tarato per un canale che perde.

Il riavvio ha cambiato qualcosa (prima DEx non si connetteva affatto), quindi
c'è uno stato che si sporca. Non indagato.

### Le tre interfacce USB MIDI sono equivalenti

Circola l'idea che la terza interfaccia USB MIDI del Deluge sia riservata al
SysEx. Misurato end-to-end su `Perche.XML`, hash verificato ogni volta:

| coppia di porte | tempo |
|---|---|
| 1 (`Deluge`) | 7,2 s |
| 2 (`MIDIOUT2/MIDIIN2`) | 6,5 s |
| 3 (`MIDIOUT3/MIDIIN3`) | 8,5 s |

Nessuna differenza utile. La scelta della porta non è la variabile.

## 4b. La causa: un bug del firmware, corretto oggi

**PR [#4633](https://github.com/SynthstromAudible/DelugeFirmware/pull/4633) —
"Fix USB MIDI receive packet loss + chainload corruption", unito l'11 agosto
2026** (commit `b93a9cf`), cioè **cinque giorni dopo** la build installata
(`0856ff9`, 6 agosto).

Causa radice, dalla descrizione del PR: il gestore di completamento BRDY
lasciava la pipe USB in stato ACK fra un trasferimento e l'altro. L'hardware
confermava quindi i pacchetti in arrivo anche quando nessun trasferimento era
armato, e quei pacchetti venivano poi distrutti da una terminazione forzata —
una perdita silenziosa, che l'host non può ritentare perché non sa che è
avvenuta.

La frase che chiude il caso:

> qualunque host che invii pacchetti bulk più ravvicinati dell'intervallo di
> polling di ~1 ms perdeva la maggior parte dei pacchetti dopo il primo

Il fix mette la pipe in NAK prima di elaborare (così l'host ritenta invece di
perdere), aspetta che PBUSY si liberi, svuota tutti i pacchetti residenti
portando il buffer di ricezione da 64 a 192 byte, ed evita la terminazione
forzata sui FIFO vuoti.

### Questo ribalta la diagnosi

Avevo attribuito la perdita alle **risposte** (Deluge → PC), perché il tasso
cresceva con la dimensione della risposta. Il bug è invece in **ricezione**
(PC → Deluge): sono le nostre *richieste* a non arrivare, e quindi la risposta
non parte proprio.

Riletto così, tutto torna, incluso ciò che prima non tornava:

| osservazione | spiegazione |
|---|---|
| blocchi di lettura più grandi sono monotonicamente più veloci | meno blocchi = **meno richieste** = meno occasioni di perderne una. Non era il payload a contare |
| la scrittura è corrotta | le richieste di scrittura sono grosse (~880 byte, molti pacchetti USB consecutivi): è il caso peggiore per questo bug |
| `ping` non fallisce mai | una richiesta minuscola, uno o due pacchetti |
| ritentare funziona | la perdita è sulla richiesta, quindi rispedirla è esattamente il rimedio giusto |
| mettere pause **fra** le richieste non serviva | il problema è la spaziatura dei pacchetti **dentro** un singolo messaggio, che dal client non si controlla |

### Cosa aspettarsi

Il fix è nel branch `community` e le nightly vengono generate ogni notte, quindi
la prima nightly successiva all'11 agosto 2026 dovrebbe contenerlo.

Non è garantito che risolva tutto: il PR parla di host Linux 6.16+ che non
spaziano le scritture, e Windows potrebbe comportarsi diversamente. Ma è la
spiegazione più probabile e non ha alternative sul tavolo.

**Un cavo o una porta USB diversi non possono correggerlo**, se la causa è
questa. Vale comunque escluderli, ma senza aspettarsi molto.

### Da tenere d'occhio

PR [#4765](https://github.com/SynthstromAudible/DelugeFirmware/pull/4765) (bozza,
5 agosto 2026) introduce una coda MIDI con priorità in cui **SYSEX è la priorità
più bassa**, sotto clock, note, expression e CC. Serve a evitare che il traffico
CC faccia saltare il clock. Se venisse unito, potrebbe peggiorare la banda SysEx
quando c'è altro traffico MIDI — rilevante qui, visto il setup con Launch
Control XL ed Exquis.

## 4-bis. `dir` può smettere di rispondere mentre tutto il resto funziona

Osservato il 12 agosto 2026, stessa build su cui poco prima `dir` funzionava:

- `ping` → risponde in 3 ms
- assegnazione di sessione → riesce (`sid=10`, range di sequence 81..87)
- `dir` su qualunque percorso, root compresa → **nessuna risposta**, per decine
  di ritentativi, con timeout corti e lunghi
- `open` + `readBlock` + `close` sullo stesso filesystem → **funzionano**, file
  scaricato e verificato

Quindi non è il canale, non è la sessione e non è il filesystem: è la sola
enumerazione delle cartelle. Era successo subito dopo che il dispositivo aveva
salvato quattro file.

**Ipotesi non verificata:** il firmware tiene un unico oggetto directory
condiviso, e se l'interfaccia lo sta usando (browser dei file aperto) la
richiesta via SysEx non trova nulla di libero. Spiegherebbe perché le
operazioni su singoli file, che usano descrittori separati, continuano ad
andare. Da confermare uscendo dal browser sul dispositivo e riprovando.

**Aggiramento, se ricapita:** `dir` non è necessario. Conoscendo il nome si va
diretti con `get`, e un `open` fallito dice che il file non c'è — è così che
sono stati recuperati TEMPL0, TEMPL1, TEMPL e CR78FROMMARS.

## 5. La scrittura — rotta fino alla build 0856ff9, funzionante dalla 2d7cdf8

> **Aggiornamento 12 agosto 2026.** Risolto dal firmware. Sulla nightly
> `1.3.0-beta build 2d7cdf8` la scrittura funziona senza modifiche al client:
>
> | prova | build 0856ff9 | build 2d7cdf8 |
> |---|---|---|
> | blocco 64, file da 256 B | 22 byte su 64 | 256/256, hash identico |
> | `Perche.XML` (28 715 B), blocco 768 | si ferma a 1000 byte esatti | completo, hash identico, 62,6 kB/s |
> | song generata in `SONGS/`, blocco 768 | mai riuscita | 35 133 byte, hash identico, 40,5 kB/s |
>
> In tutte e tre: **0 timeout, 0 blocchi parziali, 0 riaperture**. Era PR #4633
> «Fix USB MIDI receive packet loss», come previsto. Il confine dei 1000 byte,
> rimasto senza spiegazione qui sotto, era un effetto della perdita di
> pacchetti e non un limite del filesystem.
>
> Quanto segue resta come diagnosi della build vecchia: descrive due difetti
> **del client** che erano reali e sono stati corretti (il campo `size`
> ignorato e il numero di sequenza non verificato). Quelli valgono ancora.

Provata a fondo, e **non era utilizzabile sulla build 0856ff9**. Ma ora si sa
esattamente perché, e il client non produce più file corrotti in silenzio.

### Il bug che avevo io

La risposta a `write` contiene un campo `size`: **quanti byte il firmware ha
scritto davvero**, che può essere meno di quanti gliene abbiamo mandati. Il
client avanzava della lunghezza *richiesta* invece che di quella *confermata*,
lasciando buchi silenziosi nel file.

È questo che produceva i primi due file corrotti — non un problema di
impacchettamento. Corretto: ora `put` legge `size`, avanza di quello, e si ferma
segnalando l'errore invece di scrivere spazzatura.

### Cosa fa davvero il dispositivo

Con blocchi da 768, la prima cosa che si vede ora è:

```
! a 0:   chiesti 768, scritti 264
! a 264: chiesti 768, scritti 348
! a 612: chiesti 768, scritti 285
il dispositivo non scrive piu nulla a 897
```

Il Deluge riceve solo una parte del messaggio, scrive quel che ha ricevuto, e lo
dichiara onestamente. È **esattamente** la perdita di pacchetti USB in ricezione
del PR #4633: dei molti pacchetti consecutivi di una richiesta lunga ne
sopravvivono i primi.

### Blocchi piccoli: funzionano, ma non a lungo

| blocco | esito su un file da 256 byte |
|---|---|
| 32 | **scrittura verificata, hash identico** |
| 40 | **scrittura verificata, hash identico** |
| 48 | scrive 6 byte su 48 |
| 56 | scrive 14 byte su 56 |
| 64 | scrive 22 byte su 64 |
| 128 | scrive 44 byte su 128 |

Ma su un file vero si ferma comunque, e sempre allo stesso punto: **1000 byte
esatti**, in due esecuzioni indipendenti. Chiudere e riaprire in append
(`write: 2`) non sblocca nulla.

Quel confine così netto non è spiegato. Potrebbe essere un limite di scritture
per descrittore, o un buffer FAT che non viene svuotato. Non è stato indagato
oltre, perché la causa a monte è nota e corretta a monte.

### Un secondo bug mio, trovato per strada

Il client non verificava il **numero di sequenza** della risposta. Con una
perdita alta capita spesso che la risposta di un tentativo precedente arrivi
mentre si aspetta quella del tentativo corrente: accettarla significa credere
riuscita un'operazione mai arrivata. Corretto — `dsysex.py` ora scarta le
risposte con sequence diversa da quella attesa.

Necessario, ma da solo non bastava: serviva anche rispettare il campo `size`.

### La verifica per hash di `put` non è una verifica di destinazione

*16 agosto 2026, costata mezz'ora di diagnosi sbagliata.*

`put` scrive e poi **rilegge il percorso su cui ha appena scritto**,
confrontando gli hash. Dice quindi che i byte sono arrivati **interi**, e non
dice niente su dove siano arrivati: se il percorso è sbagliato, la rilettura
usa lo *stesso* percorso sbagliato e l'hash torna. Il messaggio «IDENTICO — la
scrittura è verificata» è vero e insufficiente insieme.

Successo caricando cinque file con un percorso costruito in PowerShell come
`"$n`01.XML"`: in una stringa a virgolette doppie **`` `0 `` è l'escape del
carattere NUL**, quindi il percorso conteneva uno zero binario al posto di
`01`. Tutti e cinque i `put` si sono dichiarati verificati; sul dispositivo i
file non c'erano dove dovevano.

Due conseguenze pratiche:

- **la verifica vera si fa rileggendo il nome che si voleva**, non quello che
  si è passato. Sono due controlli diversi e solo il secondo trova questo
  errore.
- una scrittura con un nome malformato può lasciare una **voce di directory
  danneggiata**: `/SONGS/DelugePal/TRASF001.XML` è rimasta rileggibile come
  0 byte, con `put` che continuava a dichiararla scritta. Non si recupera
  riscrivendoci sopra, perché `put` non sovrascrive: serve un nome nuovo.

Costruire i percorsi con `musica.destinazione()` evita la classe intera —
`destinazione()` rifiuta i caratteri di controllo, NUL compreso. La regola
«mai un percorso scritto a mano» vale anche per la riga di comando, non solo
per il codice.

### Il cambio di cavo non cambia niente

Provato un cavo diverso: `Perche.XML` in 7,7 s contro 7,0-7,2 s di prima, 112
timeout su 38 blocchi (~75% di perdita, come prima). Nessuna differenza. Anche
le tre interfacce USB MIDI sono equivalenti. Coerente con una causa nel
firmware.

## 6. Stato

| | |
|---|---|
| lettura | **funziona**, hash verificato su 269 kB, ~4,5 kB/s |
| scrittura | **non funziona**, file corrotti in modo riproducibile |

Per portare file *sul* Deluge resta la SD spostata a mano. Per leggerli senza
spostarla, `dsysex.py get` va benissimo.

### Ipotesi già provate e scartate

Non rifarle.

| ipotesi | esito |
|---|---|
| blocco multiplo di 7, per evitare gruppi incompleti nell'impacchettamento 7/8 (763 byte invece di 768) | **peggiora**: 28 429 byte scritti invece di 28 512. Scartata |
| cavo USB diverso | nessuna differenza |
| una delle altre due interfacce USB MIDI | equivalenti |
| riaprire il file in append quando si blocca | non sblocca |
| verificare il numero di sequenza delle risposte | necessario e corretto, ma da solo non basta |

Ciò che invece **ha** cambiato qualcosa: leggere il campo `size` della risposta
`^write`. Era il vero difetto del client, e ora `put` avanza di quanto il
dispositivo dichiara di aver scritto invece che di quanto gli è stato mandato.
Da lì in poi il client non produce più file corrotti in silenzio: si ferma e lo
dice.

### Cosa fare, alla luce del PR #4633

Aggiornare il firmware a una nightly successiva all'11 agosto 2026 e
**riprovare `put`**. Il PR corregge proprio la perdita di pacchetti USB in
ricezione, che è il caso peggiore per le richieste di scrittura — i messaggi
più lunghi che mandiamo.

Non ha senso lavorare sul client prima di quell'aggiornamento: tutte le
ipotesi lato PC sono state esaurite.

Se dopo l'aggiornamento il problema resta, l'unico indizio non spiegato è che
la scrittura si ferma sempre a **1000 byte esatti**, in esecuzioni
indipendenti — un confine troppo netto per essere perdita casuale.

### File di prova sulla SD

Erano stati lasciati dodici file di prova in `/SONGS/` (`Sxtest*`, `Sxok*`,
`Sb*.bin`, `Sc*.bin`). **Cancellati tutti** l'11 agosto 2026, verificato che
`E:\SONGS` contenesse solo XML legittimi.

Finché non è risolto, il trasferimento dei file resta quello che è sempre stato:
la SD spostata a mano. Funziona ed è veloce.
