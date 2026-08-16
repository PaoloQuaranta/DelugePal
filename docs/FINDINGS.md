# Reverse engineering dello schema XML Deluge — risultati

**Build di riferimento:** `deluge-v1_3_0-beta+2026_08_06-0856ff9.bin` (sulla SD, root)
**Corpus:** 27 song + 2 kit + 3 file di SETTINGS, tutti con `firmwareVersion="c1.3.0"`
**Data:** 10 agosto 2026

Convenzione usata in tutto il documento:

- **[OSS]** osservato direttamente in file reali, con il numero di occorrenze
- **[DER]** derivato da dati reali con un ragionamento, non ancora confermato sul dispositivo
- **[CONF]** confermato sul dispositivo o dal codice sorgente del firmware
- **[IPO]** ipotesi non verificata

Le fonti primarie usate sono due: i file scritti dal dispositivo e il codice
sorgente del firmware. Elenco in [FONTI.md](FONTI.md).

---

## 1. Il punto che cambia il progetto: il Deluge non scrive XML valido

Questo è il risultato più importante e non era nell'handoff.

Su 378 song presenti sulla SD, **255 vengono rifiutate da un parser XML conforme**
(`xml.etree`). Non è corruzione: sono tre difetti sistematici e deterministici del
writer del firmware.

### 1.1 `&` non escapato — [OSS], 22 file su 378

Quando il nome di un preset o di un sample contiene `&`, il firmware lo scrive
alla lettera dentro il valore dell'attributo:

```xml
<sound name="R&b3" ...>
<fileName name="SAMPLES/DRUMS/187kit/187 Kit samples/131&SNR.WAV">
```

Nel corpus c1.3.0: 4 file, 18 occorrenze. Il parser del Deluge lo accetta;
qualunque parser conforme no.

**[CONF] dal sorgente.** `XMLSerializer::writeAttribute` in
`src/deluge/storage/Serializer.cpp` scrive il valore così com'è:

```cpp
write(name);
write("=\"");
write(value);     // nessuna funzione di escape
write("\"");
```

Non è un caso limite: **nessun valore di attributo viene mai escapato**. Quindi
vale anche per `<`, `>` e `"` nei nomi di sample o preset, anche se nel corpus
non ci sono campioni con quei caratteri. Un nome contenente `"` produrrebbe un
file irrecuperabile anche per il parser di questo progetto.

### 1.2 Blocco di attributi duplicato su `<audioClip>` — [OSS], 8 file su 378

Sempre e solo su `audioClip`, sempre lo stesso blocco, sempre con valori identici:

```xml
<audioClip
	trackName="AUDIO3"
	...
	isPlaying="1" isSoloing="0" isArmedForRecording="1"
	length="3072" colourOffset="14" section="0"
	isPlaying="1" isSoloing="0" isArmedForRecording="1"
	length="3072" colourOffset="14" section="0">
```

Gli attributi coinvolti sono quelli della classe base `Clip`
(`isPlaying`, `isSoloing`, `isArmedForRecording`, `length`, `colourOffset`,
`section`, a volte `selected`): due percorsi di codice li scrivono entrambi.
Nel corpus c1.3.0: 3 file, 36 occorrenze. Il difetto è presente anche in c1.2.0,
quindi non è una regressione della beta corrente. [OSS]

### 1.3 Formato legacy con due elementi radice — [OSS], 242 file

Le song scritte prima della 3.0 hanno:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<firmwareVersion>1.3.0</firmwareVersion>
<song>
```

`firmwareVersion` e `song` sono fratelli: il documento ha più di un elemento
radice, cosa che l'XML non ammette. Riguarda solo i file vecchi, ma un
convertitore deve saperli leggere.

### Conseguenza progettuale

**Non si può usare `xml.etree` (né lxml, né qualunque parser conforme) come base
del workflow.** Il progetto usa un parser tollerante scritto su misura
(`tools/delugexml/parser.py`) che riproduce la permissività del firmware:
nessuna decodifica di entità, attributi conservati come lista ordinata con
duplicati, più elementi radice ammessi.

---

## 2. Regole di serializzazione

### 2.1 Livello byte — [OSS], tutti i 32 file

- codifica UTF-8, **senza BOM**
- fine riga **LF**, mai CRLF
- indentazione con **tabulazioni**, una per livello
- **newline finale** presente

### 2.2 Attributi inline o uno per riga

La scelta **non dipende** dal numero di attributi né dalla lunghezza della riga.
Verificato: esistono elementi inline da 89 caratteri e elementi multiriga da 20.
Con 1, 2 o 3 attributi si osservano entrambe le forme; da 4 in su sempre
multiriga, ma è una conseguenza, non la regola.

La forma è una **proprietà fissa del punto del codice C++ che scrive
quell'elemento** — cioè, in pratica, del tag e dell'insieme di attributi
presenti.

**[CONF] dal sorgente.** La firma è letteralmente questa:

```cpp
void XMLSerializer::writeAttribute(char const* name, char const* value, bool onNewLine)
// if (onNewLine) { write("\n"); printIndents(); } else { write(" "); }
```

`onNewLine` è un parametro deciso a ogni singola chiamata. Non esiste nessuna
soglia, nessun calcolo di lunghezza: la formattazione è cablata call-site per
call-site. Il modello `inline_prefix` appreso dal corpus ha esattamente la forma
giusta, e la forma "ibrida" di `<midiKnob>` è semplicemente una classe che chiama
`writeAttribute(..., false)` per i propri campi e poi delega alla base che usa
`true`.

Corollario pratico: **la tabella di formato non è derivabile per regole, va
appresa**. Nessun ragionamento a priori può indovinare come è scritto un
elemento che non si è mai visto.

Il parametro modellato è `inline_prefix`: quanti attributi finiscono sulla stessa
riga di `<tag`. Tre casi osservati:

```xml
<!-- inline_prefix = tutti -->
<lfo1 type="triangle" syncLevel="0" syncType="0" />

<!-- inline_prefix = 0 -->
<reverb
	roomSize="1288490496"
	dampening="1546188288"
	pan="0">

<!-- inline_prefix = 2 — forma ibrida, osservata su <midiKnob> e
     sui device di MIDIDevices.XML -->
<midiKnob channel="2" ccNumber="6"
	relative="0"
	controlsParam="lpfResonance">
```

L'ibrido corrisponde a una classe che scrive i propri campi inline e poi delega
il resto alla classe base. [DER]

La forma dipende anche dall'**insieme** di attributi, non solo dal tag:
`<device port="din" />` è inline, `<device name=… vendorId=… productId=…>` è
multiriga. La tabella è quindi indicizzata su `(percorso, firma attributi)` con
ripiego su `(tag, firma)`, poi percorso, poi tag.

### 2.2-bis Il limite del modello: attributi raggruppati — [OSS], 1 file

Il modello è un intero solo, `inline_prefix`: **quanti attributi stanno sulla
riga del tag**, con tutti gli altri uno per riga. Copre 53 file su 53 tranne
uno, e quell'uno mostra una terza forma che il modello non sa esprimere:

```xml
				<midiOutput
					name="" channel="0" note="0">
```

Zero attributi sulla riga del tag, e poi **tutti e tre insieme** sulla riga
dopo. Non è «N inline e il resto singoli»: è un gruppo.

Viene dalla riga MIDI di un kit in `refs/songs/TRASF401MIDI.XML`, che è
l'unico esemplare esistente di quel nodo — un `<midiOutput>` dentro
`<soundSources>`, vedi §6-septies.

**Non è un difetto che tocchi il dispositivo.** Il round-trip *chirurgico* —
quello che si usa davvero, che riemette i nodi non modificati ricopiandone i
byte — resta byte-esatto anche su questo file; e il Deluge legge XML, non
conta gli spazi. A cadere è solo la ricostruzione completa dalle regole, che
è un'autoverifica del modello.

Non è stato allargato il modello per un caso solo: `test_roundtrip` lo
dichiara come eccezione **nominata**, e `test_rebuild_differisce_solo_negli_spazi`
controlla che la differenza resti di soli spazi bianchi. Se diventasse altro,
o se un secondo file ci cadesse, i due test lo dicono subito.

### 2.3 Elementi vuoti — [OSS]

Tre forme distinte, tutte da riprodurre:

```xml
<delay pingPong="1" analog="0" syncLevel="7" />     <!-- self-closing -->
<setting name="quantize" value="1"></setting>       <!-- vuoto, attributi inline -->
<osc2
	timeStretchAmount="0">
</osc2>                                             <!-- vuoto, attributi multiriga -->
```

Regola: se l'elemento ha tag di chiusura esplicito ed è vuoto, la chiusura sta
sulla stessa riga **solo se anche gli attributi erano inline**. [DER, confermato
dal fatto che assumere il contrario rompe 9 file su 32]

### 2.4 Validazione

| test | esito |
|---|---|
| round-trip chirurgico (rami intatti ricopiati) | **32/32 byte-identici** |
| rebuild completo dalle regole | **32/32 byte-identici** |
| leave-one-out (tabella appresa dagli *altri* file) | **29/32** |
| kit ricostruiti con tabella appresa solo dalle song | **2/2 byte-identici** |
| **file modificato caricato dal Deluge** | **[CONF] 10 ago 2026** |

L'ultima riga è quella che conta: `Mark100.XML` — prodotto da questi strumenti
cambiando il tempo di `Mark.XML` da 88 a 100 BPM, 11 byte diversi su 269 779 —
si apre sul dispositivo e mostra 100 BPM. Il byte-esatto non garantiva questo, ed
è il motivo per cui era elencato fra i rischi.

I 3 fallimenti del leave-one-out sono **buchi di copertura, non errori di
regola**: `CommunityFeatures.XML` e `MIDIDevices.XML` sono gli unici esemplari
del loro tipo (escludendoli dal training non resta nulla da cui imparare), e
`Mark.XML` contiene l'unica occorrenza della firma
`device|name,vendorId,productId`. Il test dei kit è quello significativo: la
tabella appresa **solo dalle song**, senza aver mai visto un percorso
`kit/soundSources/...`, ricostruisce entrambi i kit byte per byte.

---

## 3. Tempo

Il Deluge **non salva i BPM**. Salva:

```xml
timePerTimerTick="626" timerTickFraction="1805838522" inputTickMagnitude="1"
```

- `timePerTimerTick` — parte intera dei campioni audio per tick interno [OSS]
- `timerTickFraction` — parte frazionaria su 2^32, scritta come **int32 con
  segno**: `-238609295` va letto come `4056358001` [OSS, 11 file su 27 hanno il
  valore negativo]
- `inputTickMagnitude` — 1 (16 file) o 2 (11 file) [OSS]

**Formula [CONF]:**

```
campioni_per_tick = timePerTimerTick + uint32(timerTickFraction) / 2^32
BPM = 110250 / (campioni_per_tick × 2^inputTickMagnitude)
```

dove `110250 = 44100 × 60 / 24`.

Come è stata derivata: dà valori interi su **26 song su 27**, ed era l'unica fra
le cinque ipotesi testate che producesse tempi plausibili anche per le song con
`inputTickMagnitude=2` (108, 123, 157 BPM invece di 216, 246, 314). L'unica song
non intera è `Perche.XML` (68.573 BPM), compatibile con un tempo impostato a
orecchio o via tap tempo.

**Confermata sul dispositivo il 10 agosto 2026**: `Mark.XML` aperta sul Deluge
mostra **88 BPM**, esattamente il valore previsto.

Confermata anche la struttura dei due attributi, dal sorgente
(`src/deluge/model/song/song.cpp`): non sono due campi indipendenti ma le due
metà di un unico intero a 64 bit in virgola fissa 32.32.

```cpp
writer.writeAttribute("timePerTimerTick", timePerTimerTickBig >> 32);
writer.writeAttribute("timerTickFraction", (uint32_t)timePerTimerTickBig);
```

Il cast a `uint32_t` scritto poi come intero con segno è esattamente il motivo
per cui 11 song su 27 hanno `timerTickFraction` negativo.

Impostare il tempo tocca esattamente 2 righe del file:

```
- timePerTimerTick="626"          + timePerTimerTick="551"
- timerTickFraction="1805838522"  + timerTickFraction="1073741824"
```

---

## 4. Note

Le note di una `noteRow` sono impacchettate in un unico attributo esadecimale.
Il layout è stato ricavato, non indovinato: si sono enumerate tutte le larghezze
di record fra 6 e 16 byte e si è verificato quale rende le posizioni
**ovunque strettamente crescenti** su 3628 noteRow.

| attributo | larghezza record | coerenza |
|---|---|---|
| `noteDataWithLift` | **11 byte** | 1783/1783 |
| `noteDataWithSplitProb` | **14 byte** | 1845/1845 |

Tutte le altre larghezze danno 0%. Il risultato non è ambiguo.

### Campi — [OSS] su oltre 10 000 note

| byte | campo | range osservato | note |
|---|---|---|---|
| 0–3 | posizione in tick | 0 … 19956 | uint32 big-endian |
| 4–7 | durata in tick | 1 … 15265 | uint32 big-endian |
| 8 | velocity | 1 … 127 | |
| 9 | lift (release velocity) | 0 … 127 | |
| 10 | condizione / probabilità | 1 … 140 | **20 = 100%**, in 10386 note su 10511 |
| 11 | solo `WithSplitProb` — divisore dell'iterance | 0 … 8 | 0 = disattivata |
| 12 | solo `WithSplitProb` — maschera dei passi attivi | 0 … 128 | il bit *k* accende il passo *k+1* |
| 13 | solo `WithSplitProb` | sempre 0 nel corpus | presumibilmente fill |

Il byte 10 vale 20 nella stragrande maggioranza dei casi; i valori ≥ 128 (133,
136, 138) sono le condizioni "iteration dependence" del Deluge. Il byte 13 è
sempre 0 nel corpus. [OSS]

Verifica indipendente: aggiungendo una nota con velocity 100 e lift 64 alla
posizione 144 di durata 48, il blob prodotto è
`0x00000090 00000030 64 40 14` — cioè pos=0x90=144, len=0x30=48, vel=0x64=100,
lift=0x40=64, cond=0x14=20. Tutti i campi tornano.

### Iterance — byte 11 e 12 [CONF]

Erano il punto aperto più grosso. Risolto incrociando documentazione e dati.

Il changelog c1.3.0 dice che una nota porta *velocity, probability, lift,
**iterance** e **fill***, e che l'iterance CUSTOM ha un divisore da 1 a 8 con i
singoli passi attivabili. E il nome stesso dell'attributo — `noteDataWith`
**`SplitProb`** — dice che la probabilità è stata *separata* da ciò con cui
prima condivideva un byte (i valori ≥ 128 del byte 10 nel vecchio formato).

Ipotesi: byte 11 = divisore, byte 12 = maschera dei passi.

Predizione verificabile: **ogni bit acceso nella maschera deve stare sotto il
divisore** — non ha senso attivare il passo 5 su un divisore di 4.

**76 note su 76 coerenti, zero eccezioni.** [OSS] Le coppie osservate si
leggono da sole:

| byte 11 | byte 12 | significa |
|---|---|---|
| 4 | `0b1000` | 4 di 4 |
| 8 | `0b10000000` | 8 di 8 |
| 2 | `0b01` | 1 di 2 |
| 4 | `0b0100` | 3 di 4 |

Che è esattamente la notazione `3of4` mostrata dal dispositivo. Nel corpus la
maschera ha sempre **un solo bit acceso**, cioè la forma classica "N di M"; il
modo CUSTOM con più passi è previsto dal firmware ma non usato in questi file.

### `<scales>` e `userScale` [CONF]

Elemento presente in tutte e 27 le song c1.3.0, aggiunta della versione
community. `userScale` è una **maschera a 12 bit dei semitoni**: `4095` =
`0b111111111111` = cromatica.

Verificato: i bit accesi coincidono con i `<modeNotes>` della stessa song, **8
su 8** dove `userScale` non è 0. È la stessa scala scritta in due forme. [OSS]

### Note

**Una noteRow può portare `noteDataWithLift` e `noteDataWithSplitProb`
contemporaneamente.** Vanno riscritti entrambi e devono restare coerenti,
altrimenti il firmware legge l'uno e l'altro racconta un'altra storia.
`notes.write_row()` lo fa.

### Griglia temporale — [CONF]

```
tick per movimento = 24 × 2^inputTickMagnitude
```

cioè **48** con `inputTickMagnitude=1` e **96** con `2`.

È la stessa costante che compare nella formula del tempo, e questo non è una
coincidenza: tempo e griglia misurano la stessa cosa. Confermata in due modi
indipendenti.

**1. Dal dispositivo.** In `Perche.XML` (`inputTickMagnitude=2`) la nota
aggiunta a posizione 144 appare sul **quarto ottavo della prima battuta**.
Quindi 48 tick = un ottavo, 96 tick = un movimento = 24 × 2². La clip da
`length="768"` è di 2 battute di 4/4, non 4 come avevo inizialmente inferito.

**2. Dal corpus.** Se i tick per movimento raddoppiano con la magnitude, la
stessa suddivisione musicale deve costare il doppio dei tick. Sulle 27 song, il
MCD delle posizioni delle note:

| inputTickMagnitude | song | mediana MCD posizioni |
|---|---|---|
| 1 | 16 | 6 |
| 2 | 11 | 12 |

Rapporto **×2.00 esatto**, come previsto.

> Nota metodologica: il primo test che avevo scritto — "le lunghezze delle clip
> sono multipli interi di battute?" — **non discriminava**, perché l'ipotesi
> alternativa (48 tick fissi) è meno stretta e quindi passa ogni volta che passa
> il modello. Dava 18 sì e 9 no per entrambe. Il MCD delle posizioni separa le
> due popolazioni, la divisibilità delle lunghezze no.

### Numerazione delle ottave — [OSS], un solo campione

`y="72"` viene mostrato dal Deluge come **C4**. Ne segue che il dispositivo usa
la convenzione con il do centrale MIDI 60 = C3. Un solo dato, non verificato su
altre ottave.

---

## 5. `MIDIFollow.XML` — il punto aperto dell'handoff, risolto

L'handoff (§8) riportava un'incoerenza: un'altra AI sosteneva che
`defaultCCMappings` fosse diventato `cc_mappings` con un nuovo blocco
`<settings>`, e quell'affermazione era stata **giudicata probabilmente
allucinata** perché nessuna ricerca la confermava.

Il file reale sulla SD dice:

```xml
<defaults>
	<cc_mappings>
		<pitch>3</pitch>
		...
	</cc_mappings>
	<settings>
		<channels>
			<a><channel>17</channel><device port="upstreamUSB" /></a>
			<b><channel>8</channel><device port="upstreamUSB2" /></b>
			...
		</channels>
		<kit_root_note><note>36</note></kit_root_note>
		<feedback>…</feedback>
		<display_param><popup>enabled</popup></display_param>
	</settings>
</defaults>
```

**`cc_mappings` e `<settings>` esistono davvero in questa build.** L'affermazione
scartata era corretta; la conclusione "probabilmente allucinata" era sbagliata —
la ricerca non trovava riscontri perché la modifica è più recente della
documentazione e dei changelog consultati.

Vale come promemoria in entrambe le direzioni: non fidarsi di un'altra AI, ma
nemmeno concludere che una cosa non esiste solo perché non la si trova
documentata. **L'unica fonte primaria è il file scritto dal dispositivo.**

Nel file corrente: Channel A = 17 su `upstreamUSB`, Channel B = 8 su
`upstreamUSB2`, i 16 `track_*` tutti a 256 (= non assegnato), `kit_root_note` 36.
Il canale 17 per A è coerente con la convenzione "MPE/omni" del Deluge. [OSS]

---

## 6. Altri elementi rilevanti

### Il SysEx **è** implementato — la premessa dell'handoff è superata

L'handoff (§2) dava per assodato che l'unico canale strutturale fosse la SD card
e che il SysEx per leggere e modificare oggetti Deluge fosse "in discussione, non
implementato" (Discussion #94, giugno 2023).

**Non è più vero.** Il firmware contiene `src/deluge/storage/smsysex.cpp` e
`smsysex.h`, che implementano un **servizio di filesystem completo su SysEx**:

| ambito | operazioni |
|---|---|
| file | `open`, `close`, `readBlock`, `writeBlock` |
| filesystem | `getDirEntries`, `createDirectory`, `createPathDirectories`, `deleteFile`, `rename`, `copyFile`, `moveFile` |
| metadati | `updateTime`, `assignSession`, `doPing` |

Framing dei messaggi [CONF: sorgente + documentazione community]:

```
F0 00 21 7B 01 <comando> <seq> <payload JSON impacchettato a 7 bit> F7
   └────┬────┘ │
        │      └─ 0x06 richiesta JSON, 0x07 risposta
        └─ manufacturer ID Synthstrom (00 21 7B) + product ID (01)
```

Il payload è JSON con una sola chiave, per esempio
`{"open": {"path": "/SONGS/SONG004.XML", "write": 1}}`. I dati binari usano un
impacchettamento 7 bit (ogni 8 byte trasmessi trasportano 7 byte di dati; il
primo contiene i bit alti dei successivi). Fino a 4 file aperti insieme, blocchi
da 1024 byte, `dir` restituisce al massimo 25 voci per richiesta.

Nel sorgente si vede una sola guardia operativa
(`if (currentlyAccessingCard != 0) return;`), non un controllo del flag. Sulla SD
però `CommunityFeatures.XML` contiene
`<setting name="devSysexAllowed" value="0"></setting>`: **il flag esiste ed è
disattivato** [OSS]. Se e come gati il servizio non è stato verificato.

**Cosa cambia e cosa no.** Non diventa Producer Pal: resta accesso a *file*, non
a oggetti della sessione viva, quindi per vedere una modifica bisogna comunque
caricare la song. Ma toglie di mezzo lo scambio fisico della SD, che era tutta la
Fase 4 del piano. Un client Python che parla questo protocollo su USB MIDI
scriverebbe direttamente in `SONGS/` con il Deluge acceso.

Esiste già un client di riferimento da studiare prima di scriverne uno:
[silicakes/deluge-extensions](https://github.com/silicakes/deluge-extensions).

**Non verificato in questa sessione:** che il servizio risponda su questa build,
cosa faccia esattamente `devSysexAllowed`, e quanto sia sicuro scrivere sulla SD
mentre il dispositivo la sta usando.

### Inventario dello schema

`docs/SCHEMA_song_c1.3.0.md` — 155 percorsi di elemento distinti, con per ognuno
attributi, tipi, range interi ed enumerazioni osservate.
`docs/SCHEMA_kit_c1.3.0.md` — 37 percorsi.

Generati dal corpus, non scritti a mano. Tutto ciò che vi compare è **[OSS]**.

### Parametri come interi con segno a 32 bit

I `*Params` usano una notazione esadecimale con segno:
`volume="0x7FFFFFFF"` (massimo), `"0x00000000"` (centro), `"0x80000000"`
(minimo). Vale per volume, pan, frequenze di filtro, inviluppi, patch cable.
**La corrispondenza con il display è stata derivata** il 12 agosto 2026, ed è
esatta in aritmetica intera:

```
valore_senza_segno = display × 85899345        con 85899345 = 2³² // 50
```

`0x80000000`→0, `0x00000000`→25, `0x7FFFFFFF`→50. Su 183 101 valori del corpus:
56,7% soddisfa l'uguaglianza **al byte**, 39,2% sono i tre estremi speciali,
0,4% ci va vicino, 3,7% resta fuori. Implementazione in
`tools/delugexml/params.py`, che ritorna **None** sui valori fuori griglia
invece di approssimarli.

**E una seconda griglia, quella interna, verificata sul dispositivo.** Portando
il volume di un synth a 35 sullo schermo, il firmware ha scritto `0x34000000`:

```
valore  = interno × 33554432        33554432 = 2³² // 128
display = round(interno × 50 / 128)      interno 90 → 35
```

Il display mostra 0-50 — è la bassa risoluzione per cui il firmware ufficiale
veniva criticato — ma quello community lavora internamente più fine. Le due
griglie **non** coincidono: `0x34000000` (interna) contro `0x33333313` che
darebbe la storica per lo stesso 35. `pan` è sulla griglia interna, non su un
caso a parte come si era ipotizzato.

Conseguenza operativa: **passare per il display perde risoluzione**, 129 valori
interni su 51 mostrati. `internal_of()` e `from_internal()` la conservano e
sono byte-esatti; `from_display()` scrive come il dispositivo oggi.

### I patch cable — scala chiusa

Misura sul dispositivo del 12 agosto: `lfo1 → modulator1Volume` portato a **30**
ha prodotto `amount="0x26666666"` = 644 245 094 = **round(0,3 × 2³¹)**.

Il range mostrato dal dispositivo è **bipolare, −50…+50** (riferito da chi lo
usa). Ne segue che il fondoscala `+50` cade a `0x40000000`, cioè **metà**
dell'int32:

```
display = amount × 100 / 2³¹              amount = round(display × 2³¹ / 100)
+50 → 0x40000000        −50 → 0xC0000000
```

**Previsione verificata sul corpus**: se +50 è `0x40000000`, nessun valore
dovrebbe superarlo. Su **15 372** `amount` int32, il **100,00% sta entro
±0x40000000**, zero eccezioni, e cinque cadono esattamente sul fondoscala
(`0x40000000` ×3, `0xC0000000` ×2). Il limite viene raggiunto e mai superato.

Solo lo 0,67% corrisponde a un display **intero**: come per i parametri di
suono, la risoluzione interna è molto più fine dello schermo. Per questo
`cable_to_display()` ritorna un float e non arrotonda.

⚠️ **`polarity` nel file NON è il range dell'interfaccia.** Il cable misurato
si dichiara `polarity="unipolar"` mentre sul dispositivo mostrava un range
bipolare. Cosa descriva davvero quell'attributo resta **ignoto** — non
dedurne il comportamento dell'interfaccia.

> Nota di metodo: la prima lettura di questo diff era stata fatta riga per
> riga, e la cable nuova era stata **inserita in cima** alla lista. `difflib`
> aveva accoppiato righe di cable diverse, facendo attribuire al cable nuovo
> la `polarity` di quello successivo. Le liste vanno confrontate come
> strutture, non come testo.

### Le note fuori scala non sono un errore — e come mi sono convinto del contrario

**Il fatto:** una clip generata (`out/BASSO.XML`) mostrava all'apertura una
nota su quattro. Toggling scale mode le rende **tutte visibili, e restano
visibili** anche tornando in scale mode. Le note c'erano tutte.

**La mia diagnosi era sbagliata.** Avevo concluso che una nota fuori dalla
scala non ha una riga su cui esistere. Il corpus lo smentisce senza appello:

| | |
|---|---|
| song con note melodiche | 70 |
| di cui **con note fuori scala** | 7 |
| `Progsong.XML` | **315 note fuori scala**, `userScale="0"` |

Song scritte dal dispositivo contengono note fuori scala di routine, con
esattamente la stessa combinazione di attributi che credevo rotta. E chi usa
il Deluge conferma il meccanismo: in scale mode le note fuori scala non
vengono scartate, **la scala viene adattata** per includerle.

`<scales>/userScale` è una **maschera a 12 bit**: `4095` = `0xFFF` = tutti i
semitoni. Vale `0` in 28 song, `4095` in 4, e valori intermedi (`3837`,
`4027`, `1499`, `3005`, `3517`, `1725`, `4079`) in una ciascuno.

**Due errori di metodo, da non ripetere:**

1. **Ho cambiato due variabili per file e chiamato "conferma indipendente" il
   risultato.** Le due varianti che funzionavano modificavano una `inKeyMode`
   + `yScroll`, l'altra le altezze + `yScroll`: condividevano la variabile che
   probabilmente contava. Rifatta la bisezione a una variabile, **entrambe
   funzionavano da sole** — che è già la prova che il modello era sbagliato.
2. **Non ho interrogato il corpus prima di scrivere la diagnosi.** La risposta
   era lì: bastava contare le note fuori scala nelle song del dispositivo.

**Il crash non è riproducibile:** riaprendo lo stesso file si esce da scale
mode senza problemi. Un fenomeno intermittente non è un segnale su cui
bisezionare, e inseguirlo è stato tempo speso male.

**Quello che resta vero, ed è un difetto nostro:** una clip creata istanziando
un modello eredita `yScroll` e `inKeyScrollOffset` dal modello, cioè da una
clip con altro preset e altre altezze. `song.fit_clip_scroll_to_notes()` li
porta entrambi dove stanno le note — `yScroll` per la griglia cromatica,
`inKeyScrollOffset` per quella in scala, dove le righe sono **gradi** e non
semitoni.

`check_notes_playable()` è deprecata: dava una diagnosi sbagliata.

---

### (sezione superata, tenuta per storia)

**Il fatto, certo:** una clip generata con quattro note (`y=36` ×2, `41`, `43`)
su una song in Re maggiore, `inKeyMode="1"`, `yScroll="37"`, mostrava e faceva
sentire **una nota sola** sul dispositivo. E lo stesso file (`out/BASSO.XML`)
**manda il Deluge in crash** uscendo da scale mode.

Il file è formalmente impeccabile: round-trip byte-esatto, zero anomalie.
Nessuno strumento del progetto può accorgersene.

**La spiegazione che avevo dato era sbagliata.** Avevo scritto che le note
fuori scala non hanno una riga su cui esistere. Chi usa il dispositivo lo
smentisce: *in scale mode il Deluge non ignora le note fuori scala, adatta la
scala per includerle, creando una **user scale*** — e c'è infatti un nodo
`<scales>` con `userScale` e `disabledPresetScales`, mai studiato.

**E la mia "verifica" non verificava nulla:** le due varianti che funzionavano
cambiavano **due** cose ciascuna, e condividevano `yScroll`:

| | modifiche |
|---|---|
| `BASSOCRO` | `inKeyMode` 1→0 **+ `yScroll` 37→36** |
| `BASSOSCA` | altezze in scala **+ `yScroll` 37→35** |

Due vie che condividono una variabile non sono due conferme indipendenti: sono
una sola, e probabilmente su `yScroll`.

Bisezione vera in corso, una variabile per file: `BASSOY` (solo `yScroll`) e
`BASSOS` (solo le altezze). Finché non risponde il dispositivo, **la causa non
è nota** e questa sezione non va citata come acquisita.

> Resta valido, ed è indipendente: una clip creata da un modello eredita
> `yScroll` dal modello, che non ha nulla a che vedere con le altezze scritte.
> `scroll_clip_to_notes()` lo porta dove stanno le note.

### I valori modulabili non contano se la struttura li disattiva

Modificando `lpfFrequency` e `lpfResonance` su una patch commerciale FM, **non
succedeva niente**. Non era un errore di scrittura: quella patch ha
`lpfMode="Off"`, cioè il filtro è spento a monte, e i suoi parametri restano
scrivibili senza avere effetto.

**Verificato sul dispositivo:** portando `lpfMode` da `Off` a `24dB`, il filtro
si sente — anche con `mode="fm"`. Quindi il firmware community **permette il
filtro in sintesi FM**; il limite era l'attributo, non il motore. La
documentazione community non tratta la questione, quindi la risposta viene dal
dispositivo.

Divisione del formato, misurata: su 1442 attributi, **666 sono valori**
modulabili (scala 0-50/128) e **776 struttura**. La struttura decide se i
valori contano qualcosa.

Valori osservati su 144 file di 17 versioni di firmware, in
`tools/delugexml/structure.py`, che **rifiuta i valori mai visti** invece di
scriverli:

| attributo | valori osservati |
|---|---|
| `sound/mode` | subtractive (4100), fm (63), ringmod (8) |
| `sound/lpfMode` | 24dB, 12dB, 24dBDrive, Off, flanger, SVF_Band, SVF_Notch |
| `sound/hpfMode` | HPLadder, Off, flanger, SVF_Notch, SVF_Band |
| `sound/polyphonic` | auto, poly, choke, legato, mono |
| `osc*/type` | sample, saw, square, sine, analogSquare, wavetable, analogSaw, triangle, inLeft, inStereo |
| `lfo*/type` | sine, triangle, saw, square, rwalk |
| `unison` | num 1-8, detune 0-50, spread 0-50 |

[OSS] `filterRoute` vale `H2L` in **tutti** i 1644 casi. Il firmware accetterà
verosimilmente anche il percorso inverso, ma non è mai stato visto in un file:
scriverlo sarebbe un'ipotesi. Da qui `force=True`, che serve a esplorare
dichiarando di essere fuori dal verificato.

Da notare: in FM gli oscillatori **non portano `type`**, perché non c'è forma
d'onda da scegliere. Un preset subtractive ha `<osc1 type="square">`, la patch
FM ha solo `transpose`/`cents`/`retrigPhase`.

### Lo swing: il file usa una scala, il display un'altra

Scritto `swingAmount="25"`, il dispositivo mostra **75**. Il display usa
**0-100 con 50 al centro**; il file usa un valore **con segno centrato sullo
zero**:

```
display = swingAmount + 50          swingAmount = display − 50
```

Confermato dal corpus, dove `swingAmount` va da **−10 a +20**, il valore più
frequente è **0** (41 volte, cioè "dritto") e **26 sono negativi**.

L'ipotesi alternativa `display = 100 − valore`, che spiegava altrettanto bene
il singolo punto misurato, è **esclusa**: farebbe di 0 — il valore più comune,
e quello che il firmware scrive di default — lo swing massimo.

`song.set_swing()` prende le unità del display e `get_swing()` le restituisce,
così le due scale non si scambiano per sbaglio.

> Terzo parametro con questa forma, dopo la scala 0-50 dei suoni e quella dei
> patch cable: **il numero nel file non è quasi mai il numero sullo schermo.**
> Vale come regola di sospetto per ogni parametro nuovo.

### `preview` è una miniatura in cache, e i file generati la portano sbagliata

Osservato sul dispositivo il 12 agosto: nel browser dei file, **tutte** le song
generate mostravano ancora l'anteprima della song di partenza — l'automazione
disegnata a mano, non quella scritta da noi. Aprendole, il contenuto era invece
quello nuovo.

Quindi `preview` (l'attributo del nodo `<song>`, 144 valori) **non viene
ricalcolato al caricamento**: è un'immagine salvata, mostrata prima di aprire
il file. Copiandola verbatim, come fa la riscrittura chirurgica, resta quella
vecchia.

Non è un difetto di correttezza — la song si carica e suona giusto — ma è
fuorviante quando si generano molti file, perché nel browser sembrano tutti
uguali all'originale. Il dispositivo la riscrive al primo salvataggio.

[OSS] Il formato dei 144 valori non è stato decodificato, quindi non sappiamo
rigenerarla. Le alternative sarebbero azzerarla o lasciarla: per ora si lascia.

### Le automazioni — formato decodificato

Un parametro automatizzato non porta più un int32 ma una sequenza
impacchettata **nello stesso attributo**:

```
lpfFrequency="0x7FFFFFFF"                       valore fisso
lpfFrequency="0x800000008000000000000000A4…"    automazione
```

Formato, in parole da 32 bit:

```
[intestazione] (valore, posizione) (valore, posizione) …
```

- **una** parola di intestazione, poi coppie — il numero di parole è
  **dispari**, ed è il modo più rapido per riconoscere il formato
- `valore` è un int32 come quelli fissi, quindi si legge con `params.py`
- `posizione` è in tick, stessa unità delle note

Ricavato da un'automazione **disegnata sul dispositivo** — mezza battuta di
rampa in salita e mezza in discesa — e decodificata contro quella forma nota
in anticipo. Il decoder ha restituito esattamente quel triangolo:

```
display  0  7 14 21 29 36 43 50 | 50 43 36 29 21 14  7  0
tick     0 24 48 72 96 120 144 168  216 240 264 288 312 336 360
```

I valori cadono sulla griglia interna a 128 (0, 18, 37, 55, 73, 91, 110), il
picco è il saturato `0x7FFFFFFF`. Codec in `tools/delugexml/automation.py`,
con `ramp()` e `ramp_internal()` per costruirne.

L'intestazione è **il valore corrente del parametro** (`valueNow` nel sorgente),
non un conteggio.

### Scrivere l'automazione non basta: bisogna renderla visibile

Il blob corretto, nel posto corretto, **non si vede e non si sente** se manca
lo stato di interfaccia. Stabilito per bisezione sul dispositivo, partendo dal
file che funzionava e rompendolo una cosa per volta.

Servono, sulla clip che porta l'automazione:

```
onAutomationInstrumentClipView="1"
lastSelectedParamID="24"        lastSelectedParamKind="1"
lastSelectedParamShortcutX="8"  lastSelectedParamShortcutY="7"
lastSelectedInstrumentType="0"  lastSelectedPatchSource="15"
beingEdited="1"                 ← e questo era il pezzo mancante
```

`beingEdited` dice quale clip il Deluge apre entrando in clip view. Scrivendo
l'automazione sulla clip 1 mentre il flag era rimasto sulla clip 0, si atterra
sul kit — che non ha automazioni né filtro — e non si vede né si sente nulla.
Spostato il flag, compare.

**Ipotesi escluse per prima, sul dispositivo:** l'ordine degli attributi (i
`lastSelected*` prima o dopo `instrumentPresetName`: indifferente) e i nodi
`<bendRange>`/`<bendRangeMPE>` (assenti: indifferente). Entrambe sembravano
plausibili guardando il diff.

> È la **terza volta** che questo progetto incontra la stessa forma: il dato è
> caricato correttamente e manca l'attributo di interfaccia che porta a
> guardarlo. Prima `yScrollSongView`, con la clip una riga sotto lo schermo;
> poi lo stato della vista automazione; ora quale clip è aperta. Vale la pena
> tenerlo come euristica: **se un contenuto scritto non compare, cercare lo
> stato di vista prima di sospettare del contenuto.**

`automation.mark_view(doc, clip, param)` fa entrambe le cose;
`song.set_edited_clip()` mantiene `beingEdited` esclusivo.

Le automazioni compaiono anche su `patchCable/amount`: `Slowjunglesolo.XML` ha
`compressor → volumePostReverbSend` con 5 e 3 parole, `Euclid Song.XML` ha
`lfo2 → oscAWavetablePosition` con **125**.

⚠️ Conseguenza pratica: chiunque analizzi un parametro deve **filtrare per
lunghezza** prima di convertire, o legge una curva come se fosse un numero.
È già costato un errore in questa sessione. `automation.is_automation()` fa
esattamente questo controllo.

[OSS] Resta non derivata la mappatura su unità fisiche (dB, Hz). Quello che si
ha è la corrispondenza con il **numero mostrato dal dispositivo**, che per
generare è ciò che serve.

---

## 6-bis. Cosa tocca il dispositivo quando aggiungi una clip

Misurato il 12 agosto 2026 con una **scala controllata**: quattro salvataggi
consecutivi, ognuno a un passo dal precedente, tutti a partire da `TEMPL0`
caricata sul dispositivo — così tempo, root note e swing restano identici
(la randomizzazione del Deluge scatta alla creazione di una song, non al
salvataggio). I file sono in `refs/songs/TEMPL{0,2,3,4}.XML`.

### Il rumore di fondo del salvataggio: 2 attributi

`TEMPL0` → `TEMPL2`, ricaricata e risalvata **senza toccare nulla**: stessa
dimensione, 417 righe, e solo due valori diversi.

| attributo | prima | dopo |
|---|---|---|
| `roomSize` | 1288490112 | 1288489984 (−128, deriva di quantizzazione) |
| `syncLevel` | 4 | 3 |

Tutto il resto è **byte-identico**. È il risultato più utile della scala:
qualunque diff futuro fra due salvataggi è segnale quasi puro, e questi due
attributi sono gli unici da ignorare.

### Aggiungere note a una clip esistente

`TEMPL2` → `TEMPL3`, 4 note su 5 `noteRow` nella clip che c'era già:
20 righe aggiunte, e **fuori dalla clip cambia solo `preview`**. Nessuno dei
due scroll si muove — coerente, perché non nascono né clip né strumenti.

### Aggiungere una clip con uno strumento nuovo

`TEMPL3` → `TEMPL4`, una clip di kit: 3642 righe aggiunte, e fuori dalla clip
**esattamente tre** cose:

| attributo | prima | dopo | perché |
|---|---|---|---|
| `preview` | … | … | il disegnino della song |
| `yScrollSongView` | −7 | −6 | una clip in più: le righe di song view sono le clip |
| `yScrollArrangementView` | −7 | −6 | uno strumento in più: le righe dell'arranger sono gli strumenti |

E una riga **rimossa**: `beingEdited="1"` sulla clip synth, passato alla clip
di kit. È il marcatore della clip aperta; il dispositivo **omette
l'attributo** invece di scriverlo a `0` (entrambe le forme esistono nel
corpus, quindi sono legali). `duplicate_clip` lo azzera già, via
`EXCLUSIVE_FLAGS`.

### Le due regole di scroll

- `yScrollSongView` insegue il **numero di clip**
- `yScrollArrangementView` insegue il **numero di strumenti**

Entrambe con la stessa aritmetica: griglia di 8 righe, la riga `i` sta a
`i - scroll`, e il dispositivo scrolla al minimo che tiene l'ultima riga a
schermo. In tutte le song del corpus salvate dal dispositivo e non riscrollate
a mano, l'ultima riga cade esattamente alla riga 7.

`scroll_song_view_to()` e `scroll_arrangement_view_to()` implementano le due
regole. Il test `test_scroll_matches_device` non verifica le nostre
convinzioni: confronta il valore che calcoliamo con quello che il Deluge ha
davvero scritto in `TEMPL4`. Entrambi danno −6.

**Perché conta.** La domanda «cosa devo aggiornare fuori dalla clip quando ne
aggiungo una?» ha ora una risposta misurata invece che congetturata — ed è la
domanda che, non essendosi posta prima, è costata due sessioni con il caso
`yScrollSongView`.

---

## 6-ter. L'arranger: `clipInstances`

### Perché non si trovava

Cercando dove una clip d'arranger dichiari **quando** suona non si trova nulla:
le clip in `<arrangementOnlyTracks>` portano `length` e nient'altro di
temporale. È un vicolo cieco convincente, perché il contenitore esiste e
sembra il posto giusto.

La posizione sta dall'altro lato del legame — sul nodo dello **strumento**, e
in forma di attributo:

```xml
<sound presetName="ADDITIVE" clipInstances="0x00000C0000004F8000000000…">
```

Una fetch di `src/deluge/model/output.cpp` l'ha detto subito. Il tentativo
precedente di dedurlo dai file aveva prodotto la conclusione sbagliata
«il corpus non contiene arrangiamenti», quando ne contiene 2116.

### Il formato

È il **terzo blob** della famiglia, dopo le note e le automazioni: parole da
32 bit esadecimali maiuscole senza separatori. Qui in **terne**.

```
(pos, length, clipCode) (pos, length, clipCode) …
```

Scrittura, da `output.cpp`:

```c
uint32_t clipCode;
if (!thisInstance->clip) clipCode = 0xFFFFFFFF;
else {
    clipCode = thisInstance->clip->indexForSaving;
    if (thisInstance->clip->section == 255) clipCode |= (1 << 31);
}
```

Lettura, da `song.cpp` — è questa che dà il significato:

```c
uint32_t lookingForIndex = clipCode & ~((uint32_t)1 << 31);
bool isArrangementClip   = clipCode >> 31;
ClipArray* clips = isArrangementClip ? &arrangementOnlyClips : &sessionClips;
```

| campo | significato |
|---|---|
| `pos` | tick d'inizio sulla linea del tempo |
| `length` | durata dell'**istanza**, non della clip: una clip da una battuta stesa su otto è *una* istanza lunga otto |
| `clipCode` bit 0-30 | indice ordinale nella lista |
| `clipCode` bit 31 | 0 = `<sessionClips>`, 1 = `<arrangementOnlyTracks>` |
| `clipCode` = `0xFFFFFFFF` | nessuna clip: un buco nell'arrangiamento |

**`clipCode` non è un identificatore, è una posizione ordinale.** Rimuovere o
riordinare una clip invalida silenziosamente ogni istanza che punti a quel
posto o oltre. `arranger.check()` esiste per questo.

### La verifica

Che gli indici cadano in range non dimostra niente: ci cadrebbe anche una
decodifica sfasata. La prova è un'altra — **ogni istanza deve risolvere a una
clip dello stesso strumento che la ospita**, e un allineamento sbagliato delle
terne, o la lista sbagliata, romperebbe proprio quel legame.

Su tutto il corpus:

```
song con arrangiamento : 24
istanze totali         : 2116
risolte e coerenti     : 2115
sentinella 0xFFFFFFFF  : 1
indici fuori range     : 0
istanze di un altro strumento : 0
ricodifica identica    : 230/230 blob
```

Ricostruire il legame clip → strumento ha richiesto di scoprire che il corpus
ne usa **quattro forme diverse**, tutte ancora in circolazione. `instrument_of()`
le prova in quest'ordine, perché i file recenti portano il nome e quelli
vecchi solo lo slot numerico:

| sulla clip | sullo strumento |
|---|---|
| `instrumentPresetName` + `Folder` | `presetName` + `presetFolder` |
| `instrumentPresetSlot` + `SubSlot` | `presetSlot` + `presetSubSlot` |
| `trackName` | `<audioTrack name=…>` |
| `midiChannel` / `cvChannel` | `<midiChannel\|cvChannel channel=…>` |

Un invariante emerso dalla misura e non ipotizzato a priori: **nessuna
istanza si sovrappone a un'altra sullo stesso strumento**, su tutte e 2116. Una
traccia suona una clip sola per volta.

### La scrittura: cosa tocca il dispositivo, misurato

Coppia controllata `ARR0`/`ARR1`: stessa song salvata due volte, in mezzo
**una sola azione** — una clip vuota piazzata a 3:1:1 in arranger view.
Risultato: **zero nodi aggiunti o tolti, 7 attributi**.

| attributo | ARR0 | ARR1 |
|---|---|---|
| `clipInstances` (sullo strumento) | assente | `0x000003000000018000000000` |
| `inArrangementView` | assente | `1` |
| `xScrollSongView` | assente | `0` |
| `xZoomSongView` | assente | `24` |
| `beingEdited` (sulla clip) | `1` | rimosso |
| `selected` (sulla clip) | assente | `1` |
| `preview` | — | rigenerato |

Il blob decodifica in `pos=768, length=384, code=0` — battuta 3, una battuta,
`sessionClips[0]`. Cioè esattamente il 3:1:1 dichiarato prima di guardare.

**Un arranger vuoto non ha l'attributo affatto**: `clipInstances` è assente,
non vuoto.

### L'equivoco dei nomi, che il sorgente scioglie

`xScrollSongView`/`xZoomSongView` sembrano lo scroll dell'arranger e **non lo
sono**. Da `song.cpp`:

```c
if (getRootUI() == &arrangerView) {
    writer.writeAttribute("inArrangementView", 1);
    goto weAreInArrangementEditorOrInClipInstance;
}
…
weAreInArrangementEditorOrInClipInstance:
    writer.writeAttribute("xScrollSongView", xScrollForReturnToSongView);
    writer.writeAttribute("xZoomSongView",   xZoomForReturnToSongView);
```

Sono lo stato a cui **tornare uscendo** dall'arranger, scritti solo dentro quel
ramo — ecco perché viaggiano sempre con `inArrangementView` e compaiono in
**0 song su 114** senza arrangiamento.

Il vero asse dei tempi dell'arranger è `xScrollArrangementView` /
`xZoomArrangementView`, scritti sempre. Finestra visibile:

    [xScrollArrangementView, xScrollArrangementView + 16 * xZoomArrangementView)

16 colonne, zoom in tick per colonna sui livelli `48 × 2ⁿ` (osservati: 48, 96,
192, 384, 768, 1536). L'asse y sono gli **strumenti**, già coperto da
`scroll_arrangement_view_to()`.

Che questo possa nascondere un arrangiamento non è teorico: nel corpus
`Junglevar.XML` ha finestra `[0,1536)` e prima istanza a **14014**, cioè si
apre davvero su uno schermo vuoto.

### `beingEdited` non convive con l'arranger

Nel corpus `inArrangementView="1"` e `beingEdited` non coesistono **mai**, 20
casi su 20 — coerente, perché `beingEdited` vuol dire che una clip è aperta in
clip view. `selected` invece è indipendente dalla vista: compare anche in
session view, e in 7 song su 20 in arranger view non c'è. Quindi
`open_in_arranger()` **sposta** `beingEdited` in `selected`, non lo inventa.

### La verifica della scrittura

Partendo da `ARR0` e chiamando `place()` + `fit_view()`, l'output riproduce il
file scritto dal dispositivo **su ogni attributo di ogni nodo**, con la sola
eccezione di `preview` — la miniatura dello schermo, che il dispositivo
rigenera e che non sappiamo produrre (§7). Il blob esce identico byte per
byte. È un test di regressione in `test_arranger_scrittura`.

Poi un arrangiamento **nuovo**, non una riproduzione: `ARRTEST.XML`, tre
blocchi a battuta 1, 3-4 e 7, con quello centrale steso su due battute — cioè
il caso in cui l'istanza è più lunga della clip. Caricato via SysEx e
**verificato sul dispositivo il 14 agosto 2026**: si apre in arranger view,
i blocchi cadono dove previsto, i vuoti pure, e il blocco lungo fa suonare il
motivo due volte. La ripetizione per allungamento è quindi confermata: una
clip stesa è **una** istanza lunga, non tante corte.

### Le sezioni, e la clip "bianca"

Una **sezione è una scena**: le clip con lo stesso `section` partono insieme.
Il nodo `<sections>` non contiene le clip — porta solo `id` e `numRepeats` per
ciascuna — ed è l'attributo `section` *sulla clip* a dire a quale scena
appartiene.

Nel corpus le song dichiarano **12 o 24** sezioni secondo la versione (103 e
36 song): non è una costante del formato. `numRepeats` vale **0 in tutte e
2100**, quindi nessuno lo usa.

La forma tipica è la sezione 0 con una clip per strumento — il brano pieno — e
le altre con poche clip, cioè le varianti. Il caso puro è `Electronic.XML`:
sezioni 0-3 contengono tutte `000 TR-808`, quattro clip diverse dello stesso
strumento. Dalla documentazione community questo è letterale in grid view, dove
le righe sono le clip uniche e **le colonne sono le sezioni**. Con un limite:
se due clip dello stesso strumento cadono nella stessa sezione, in grid se ne
vede **una sola** — succede in 91 sezioni del corpus, quindi è legale ma
degradato (`song.same_section_conflicts()`).

**La clip bianca è la clip senza sezione.** Non appartenendo a nessuna scena
non compare in session view ed esiste solo nel punto della timeline dove sta.
È il gesto che rende l'arranger uno strumento di arrangiamento: si prende una
clip da una scena, la si piazza, la si converte in bianca, e da lì la si
modifica — un fill, un colpo tolto — senza toccare l'originale né le altre
ripetizioni.

Il criterio sul file è l'**assenza** di `section`, non `section="255"`: le 54
clip d'arranger del corpus non hanno l'attributo affatto, e tutte e 1127 le
clip di sessione ce l'hanno. Il 255 è la rappresentazione in memoria, imposta
dal firmware in base al contenitore:

```c
// Ensure all arranger-only Clips have their section as 255
for (…arrangementOnlyClips…) { clip->section = 255; }
```

`<arrangementOnlyTracks>` segue sempre `<sessionClips>` (8 song su 8).
`arranger.place_unique()` fa l'operazione completa; usa `copy_detached()` e
non `copy()`, perché i nodi copiati portano gli span del documento d'origine e
riusarli altrove produce XML troncato che si scrive senza errori e fallisce
solo alla rilettura.

### Verificato sul dispositivo

`ARRWHITE.XML` (14 agosto 2026): la clip bianca generata **si vede solo
nell'arranger** e non compare in session view, e il fill aggiunto sulla copia
non tocca l'originale né le altre ripetizioni.

`SCENE2.XML` (14 agosto 2026): due strumenti, due scene, arranger `A B A B`.
Le due tracce restano allineate a ogni cambio di scena — cioè le sezioni sono
state capite come gruppi di lancio e non come proprietà della singola clip.

### Cosa resta aperto

- `currentTrackInstanceArrangementPos`, scritto dal firmware quando si è
  entrati dentro un'istanza (`lastClipInstanceEnteredStartPos != -1`): mai
  osservato nella coppia
- la tabella dei **colori di sezione**. Il firmware la indicizza con
  `defaultClipSectionColours[clip->section]` ma non l'ho trovata nel sorgente,
  e `colour` sullo strumento vale 0 in 399 casi su 414, quindi non è quella la
  leva. Va ricavata dal dispositivo: quali indici danno quali colori

---

## 6-quater. Il tipo di una clip è dichiarato tre volte, e devono concordare

Un file generato è stato rifiutato dal Deluge con **«file corrupted»** pur
essendo XML valido, pulito secondo `audit_wellformed`, e rileggibile dal
parser senza un errore. Nessuno dei controlli esistenti poteva vederlo.

### La causa

`create.add_track()` rinominava il `<defaultParams>` del preset in
`soundParams` **sempre**, anche partendo da un preset di kit. Dal firmware,
`src/deluge/model/clip/instrument_clip.cpp`:

```c
else if (!strcmp(tagName, "soundParams")) {
    outputTypeWhileLoading = OutputType::SYNTH;
```

Quel tag **non è un'etichetta: è una dichiarazione di tipo al caricatore.**
La clip si annunciava synth, e poi mostrava righe indicizzate per `drumIndex`
con uno strumento `<kit>`. Contraddizione, e il file cade.

### Le tre dichiarazioni

Una `<instrumentClip>` dice di che tipo è da tre parti indipendenti, e vanno
tenute allineate:

| dove | kit | synth |
|---|---|---|
| contenitore dei parametri | `<kitParams>` | `<soundParams>` (o nessuno) |
| indice delle righe | `drumIndex` | `y` |
| attributo sulla clip | `affectEntire` presente | assente |

Nel corpus sono invarianti secchi: `kitParams` su **395 clip di kit su 395**;
`affectEntire` su **395 su 395** e su **0 clip di synth su 551**. Le clip di
synth senza contenitore sono 153, quindi l'assenza è lecita — è la presenza
di quello *sbagliato* a rompere.

`song.check_clip_types()` verifica l'accordo fra le tre. Sui 139 file scritti
dal dispositivo dà **0 falsi positivi**.

### Due trappole incontrate costruendo il controllo

**Un falso positivo su due file 3.0.1** (`Pacmegajam.XML`): hanno un `<sound>`
e un `<kit>` **sullo stesso `presetSlot` 0**, e una clip senza righe che vi si
lega non è attribuibile con certezza. Non è il file a essere sbagliato, è la
risoluzione per slot a essere ambigua. Il confronto clip↔strumento vale quindi
solo per i file che legano per nome.

**Un sospetto grave ed errato**: i blob delle note apparivano di lunghezze
incoerenti fra loro. Il record è **28 cifre** per `noteDataWithSplitProb` e
**22** per `noteDataWithLift`, e i blob generati erano multipli esatti come
quelli del dispositivo. Escluso misurando, non ragionando.

### Cosa invece NON serve

Le `noteRow` di kit scritte dal dispositivo portano un `<soundParams>` proprio
(7495 righe contro 18 senza), e quelle generate no. **Non è necessario**:
`SCENE2.XML` è stato verificato sul dispositivo senza. Un caso in cui la
quasi-totalità del corpus descrive un'abitudine del firmware, non un requisito.

---

## 6-quinquies. MIDI, CV e audio

### MIDI e CV: strumenti senza figli

`<midiChannel>` e `<cvChannel>` sono **nodi di soli attributi**, senza figli —
niente `soundSources`, niente `defaultParams`, niente patch cable. Non c'è
nessun suono da descrivere: tutto il peso sta sulla clip. Nel corpus 94
strumenti MIDI in 44 song e 9 CV in 7 song.

I canali sono **0-based nel file e 1-based sul display**: `channel="13"` è
*MIDI 14*. MIDI 0-15; CV 0-1, cioè le due uscite del pannello, coi gate 1-2
appaiati.

**Il `suffix` non è decorativo.** Dal manuale, capitolo MIDI: per avere più
clip che escano sullo stesso canale *simultaneamente*, quelle in più prendono
un suffisso (`2A`, `2B`) che le fa trattare come strumenti distinti. Quindi
`suffix="-1"` — 93 casi su 94 — significa "nessuno", e due strumenti con lo
stesso canale **e** lo stesso suffisso sono un conflitto: esistono nel file e
non possono suonare insieme. Stessa famiglia di `same_section_conflicts()`.

`cv2Source` sceglie cosa esce dalla seconda uscita CV. Dal sorgente
(`cv_instrument.cpp`): `0` off, `1` pitch, `2` mod, `3` aftertouch, `4`
velocity. [OSS] Una sola lettura del sorgente, non verificata sul dispositivo;
nel corpus compare solo il valore 1.

Il firmware accetta anche **zone MPE** al posto di un canale, con un tag
`<zone>` che vale `lower` o `upper`. Nel corpus non ce n'è nessuna.

### Un bug che il MIDI ha fatto emergere

Leggere le note di qualunque file di formato **vecchio** sollevava
`IndexError`. I record dei blob hanno tre larghezze:

| attributo | byte per nota |
|---|---|
| `noteData` | **10** — pos, length, velocity, lift, e finisce lì |
| `noteDataWithLift` | 11 |
| `noteDataWithSplitProb` | 14 |

`decode` leggeva sempre il byte di *condition* all'indice 10, che in un record
da 10 byte non esiste. Sono **1850 righe** nel corpus, mai lette prima perché
nessun percorso ci passava — finché non è arrivato il MIDI, dove i file vecchi
abbondano. Ora tutte le 12662 righe dei 139 file si leggono.

### Audio: l'unica clip che non contiene musica

Un `<audioClip>` è un **riferimento a un file**. 192 `<audioTrack>` in 40 song,
194 clip.

Tre cose che non si deducono dalle altre clip:

- il contenitore dei parametri è **`<params>`** — un terzo nome dopo
  `soundParams` e `kitParams` — su 194 clip su 194, e contiene la catena
  effetti, non un motore di sintesi
- il legame con la traccia è **per nome**: `trackName` contro `name`
- le clip audio portano **attributi duplicati**, scritti due volte dal
  firmware (`isPlaying`, `isSoloing`, `isArmedForRecording`, `length`,
  `colourOffset`, `section` su 71 clip: 265 attributi contati su 194 clip). È
  lo stesso difetto per cui questo progetto ha un parser tollerante; generando
  si scrivono una volta sola

`inputChannel` ha valori **testuali** (`none`, `left`, `right`, `stereo`,
`balanced`), e `mode` è `Player` o `Looper/FX`.

### Campioni e tick

`startSamplePos`/`endSamplePos` sono in **frame**, `length` in **tick**. Dal
sorgente (`audio_clip.cpp`), come li lega il dispositivo registrando:

```cpp
double samplesPerTick = sampleHolder.getDurationInSamples(true) / numTicksDone;
sampleHolder.endPos = sampleHolder.startPos + samplesPerTick * suggestedLength + 0.5;
```

cioè `fine − inizio = length × campioni_per_tick`. Nel corpus regge entro l'1%
su 154 clip su 185, mediana **esattamente 1.0000**.

Non è però un vincolo: `pitchSpeedIndependent` vale 1 su tutte e 194 le clip,
quindi il Deluge **stira il campione** per farlo stare nella clip. Rispettare
la relazione significa "velocità naturale".

Per non indicare posizioni inesistenti, `audio.wav_frames()` legge
l'intestazione del WAV — il file si scarica dalla SD con `dsysex get`.

### La clip vuota, e una sentinella che non c'era

Nove clip hanno `endSamplePos="9999999"`, e sembrava una sentinella "fino alla
fine del file". **Non lo è**: il sorgente scrive e rilegge il valore grezzo
senza nessun caso speciale.

La spiegazione vera è più semplice, e la dà una corrispondenza esatta: le 9
clip con `filePath=""` sono **le stesse 9** con `endSamplePos="9999999"`,
nessuna di più e nessuna di meno. È una **clip audio vuota** — uno slot pronto
a registrare — e `9999999` è solo il suo valore iniziale, insieme a
`startSamplePos="0"` e `attack="-2147483648"`. Stato legittimo, non difetto.

### Il crash E365, e la lezione che vale più del bug

Il primo `AUDIOTEST.XML` ha fatto **crashare il Deluge con E365**. Causa: il
`<params>` della clip ha **31 attributi e quattro figli** (`delay`, `lpf`,
`hpf`, `equalizer`), e quello generato ne aveva **11 e nessun figlio**.

Il nodo corretto era già stato estratto in un file, 1165 byte, prodotto
apposta. È stato invece ricopiato **a mano dall'anteprima troncata a 200
caratteri stampata a console** — e dove l'anteprima non arrivava, i valori
sono stati *inventati plausibili*:

| scritto a mano | valore vero |
|---|---|
| `ratio="8"` | `ratio="1073741824"` |
| `blend` | `compBlend` |
| `attack="12"` | `attack="83886080"` |
| `<stutter syncType syncLevel useSongStutter>` | `<stutter quantized reverse pingPong>` |

Il file era XML valido, si rileggeva, e passava `check()`, `check_clip_types()`
e `arranger.check()`. **Nessun controllo semantico può accorgersi di dati
inventati che sembrano giusti.**

Il rimedio non è "trascrivere meglio": `test_audio_costanti` confronta le
costanti incorporate col nodo vero del dispositivo, attributo per attributo e
figlio per figlio. Dodici asserzioni che sarebbero fallite subito.

La regola generale: **una costante catturata da un file del dispositivo va
generata da codice e confrontata da un test, mai trascritta.**

`test_costanti_catturate` estende il controllo a tutta la libreria, e
distingue due classi che vanno verificate in modo diverso:

| classe | esempi | verifica |
|---|---|---|
| **catture verbatim** | `CLIP_BASE`, `ARPEGGIATOR_BASE`, `BEND_RANGE`, `columnControls`, `TRACCIA_XML`, `PARAMS_XML` | uguaglianza col nodo del dispositivo, **valori e ordine** |
| **default scelti** | `ISTANZA_STRUMENTO`, `ISTANZA_MIDI`, `ISTANZA_CV` | il valore dev'essere uno che il dispositivo **scrive davvero** per quel tipo di nodo |

La seconda classe ha subito trovato un difetto che nessuno aveva visto:
`ISTANZA_STRUMENTO` scriveva **`isArmedForRecording="1"` sugli strumenti**, un
valore che nel corpus **non esiste** — 0 su 356 `<sound>` e 0 su 241 `<kit>`,
sempre `"0"`. L'`1` sta sulle *clip*, non sugli strumenti. Effetto: ogni
traccia generata nasceva armata per la registrazione. Corretto.

Diverso il caso di `activeModFunction`, che a prima vista sembrava un altro
difetto (scriviamo `0`, il più comune è `1`): è la funzione selezionata sulle
manopole e varia legittimamente — 1 in 181 casi, 0 in 84, poi 3, 4, 7, 5.
Una scelta fra valori osservati, non una deviazione.

Il test è stato provato per mutazione, perché un test che non fallisce mai non
protegge niente: valore cambiato, troncamento a 11 voci (il caso E365 esatto) e
`isArmedForRecording` rimesso a 1 vengono tutti e tre intercettati.

[OSS] Cosa significhi esattamente E365 non è stato trovato né nella
documentazione né nel sorgente. Il legame col `<params>` incompleto resta
un'inferenza, confermata solo dal fatto che correggendo quello il file si apre.

### Verificato sul dispositivo

`MIDICV.XML` e `AUDIOTEST2.XML` (14 agosto 2026): tracce MIDI e CV con le loro
note, e due clip audio dalla stessa registrazione a velocità naturale.

---

## 6-sexies. La rimozione: cosa punta a cosa

*15 agosto 2026. Verificato sul dispositivo.*

Togliere è l'operazione che il progetto non aveva. La domanda che la governa è
una sola: **cosa punta a cosa per posizione ordinale?** Misurato sulle 36 song
di `refs/songs`, passando al setaccio ogni attributo il cui nome contenesse
`index`, `code`, `slot`, `count`, `num`, `current`, `selected`, `section`,
`scroll`, e ogni nodo scalare con gli stessi.

### Verso una clip: due riferimenti — [OSS], 36 song

| dove | cosa |
|---|---|
| `clipInstances` sugli strumenti | `clipCode`, indice ordinale; il bit 31 sceglie la lista |
| `yScrollSongView` sul `<song>` | quale clip sta alla riga 0 dello schermo |

**E nient'altro.** L'unico riferimento ordinale in nodo-testo di tutto il
corpus è `<selectedDrumIndex>`, che riguarda i kit e che `kit.remove_drum()`
già aggiorna.

`yScrollSongView` conta **solo** `<sessionClips>`: le tracce di solo arranger
non hanno una riga in song view.

### Verso uno strumento: nessun ordinale — [OSS]

Le clip risolvono lo strumento per nome, slot o canale (quattro forme, vedi
`instrument_of()`), mai per posizione. L'unico ordinale che conta gli strumenti
è `yScrollArrangementView`. Conseguenza: togliere uno strumento non richiede
rinumerazioni, ma lascia **appese** le clip che lo nominano, che vanno via
con lui.

### `clipInstances` vuoto non esiste — [OSS], 203 strumenti

**92 strumenti su 203 non hanno l'attributo, ZERO ce l'hanno vuoto** (`0x`).
L'assenza è la forma con cui il dispositivo scrive "nessuna istanza". Scrivere
`0x` sarebbe inventare una forma mai osservata, per giunta su un dettaglio che
nessuno guarderebbe: `set_instances()` toglie l'attributo.

### `beingEdited` non va spostato — [OSS], 36 song

Vale 1 su una clip in **15 song su 36**, e su **nessuna clip nelle altre 21**.
«Nessuna clip aperta» è uno stato che il dispositivo scrive normalmente, quindi
togliere la clip aperta non obbliga a eleggerne un'altra — e non farlo evita di
aprire una clip che l'utente non ha chiesto.

### Lo scroll in specchio — la quinta volta della stessa famiglia

`_keep_row_visible()` **alza soltanto** lo scroll: risolve il contenuto finito
*sotto* il bordo, che è il caso dell'aggiunta. La rimozione produce l'opposto —
la vista resta parcheggiata *sopra* il contenuto, e la song view mostra il
vuoto mentre le clip sono tutte nel file. È il difetto di §3.1 rifatto al
contrario.

Non è teorico: **11 song su 36 hanno `yScrollSongView` positivo**, e
`Progsong.XML` vale 27 con 42 clip — tolte venti clip, lo scroll punterebbe
oltre l'ultima.

La correzione (`_keep_view_within()`) scende **solo** fino a rendere visibile
l'ultima riga, e **non ri-ancora in fondo**. Il dispositivo tiene l'ultima riga
alla riga 7 solo in **15 song su 36**; nelle altre 21 lo scroll è dove l'ha
lasciato una persona, e quello è stato da conservare. Cosa faccia il Deluge
quando si *cancella* non è mai stato misurato, quindi la correzione si ferma a
ciò che si può dimostrare: la vista non è cieca.

### Su un kit una riga non si toglie — [OSS], 395 clip di kit

**393 su 395** hanno una riga per *ogni* drum, suonato o no, con indici
contigui da 0. Togliere una riga rompe l'invariante e il file viene fermato da
`verifica()` stessa. Le due richieste vanno tenute diverse:

    la riga in questa clip  ->  svuotarla: quel drum tace QUI
    il drum dal kit         ->  kit.remove_drum(): esce da TUTTE le sue clip

### Verificato sul dispositivo

`RIMOSS001.XML` e `RIMOSS101.XML` (15 agosto 2026), generate col metodo di
SCROLLA/SCROLLB: due song identiche tranne per l'operazione in esame. Quattro
tracce arrangiate una per battuta, e la stessa song senza la traccia 2.

Sul Deluge: battuta 2 vuota, e **le battute 3 e 4 suonano ancora il proprio
materiale** — cioè le due istanze che puntavano agli indici 2 e 3 ora puntano
correttamente a 1 e 2. Song view mostra le tre clip rimaste, nessuna riga
cieca.

È la verifica che conta, perché un `clipCode` sbagliato produce un file **XML
valido che si rilegge senza errori**: nessun controllo sui byte se ne
accorgerebbe, e l'errore esiste solo suonando.

---

## 6-septies. Le trasformazioni: dove vive l'altezza

*16 agosto 2026. Verificato sul dispositivo.*

Trasporre vuol dire cose diverse secondo cosa si trasporta, e i due meccanismi
non si somigliano affatto.

### Su un synth: le righe SONO le altezze

Si cambia `y` sulla `<noteRow>`. Nessun altro riferimento da aggiornare, ma le
righe vanno riordinate e **`fit_clip_scroll_to_notes()` va richiamata**, o le
note restano scritte fuori dalla finestra visibile.

### Su un kit: `transpose` sugli oscillatori — [CONF] manuale, verificato

L'intonazione di un drum **non** sta nel `drumIndex`, che è solo una
posizione: sta in `transpose`, in semitoni, sugli `<osc1>`/`<osc2>` del suo
`<sound>`. Il manuale, voce TRANSPOSE del menu degli oscillatori:

> `TRANSPOSE — Semitones + cents for adjustment`

`cents` è il fine tuning in centesimi di tono. Non viene toccato: la
trasposizione in semitoni non ne ha bisogno, e nel corpus ci sono **due
codifiche in circolazione** dello stesso "nessuna alterazione" —
`cents=32` con `transpose` assente ×144, e `transpose=0 cents=0` ×47. Quale
sia più recente non è determinabile dal corpus, per la ragione di HANDOFF §7:
i valori non toccati vengono riportati identici a ogni risalvataggio.

**144 oscillatori su 204 non hanno affatto `transpose`**: trasporre lo
aggiunge, ed è comunque una forma osservata.

Conseguenza sulla portata, che va detta a chi chiama: intonare un drum cambia
lo **strumento**, quindi **tutte le clip di quel kit**. È la stessa distinzione
fra `kit.remove_drum()` e lo svuotare una riga.

### Non tutte le righe di un kit hanno un'altezza — [OSS]

Il manuale: «A synth, MIDI or CV row can be added in the kit view by pressing
[AUDITION]+[SYNTH], [AUDITION]+[MIDI], [AUDITION]+[CV]». Nei file, dentro
`<soundSources>`:

| tag | quanti | come si intona |
|---|---|---|
| `<sound>` | 3928 | `transpose` sugli `<osc>` |
| `<midiOutput name=… channel=… note=…>` | 1 | l'attributo `note`, fra 0 e 127 |
| `<gateOutput channel="…">` | 12 | **niente**: un gate non ha altezza |

Le righe di gate vengono saltate e dichiarate nel rapporto.

### La riga MIDI di un kit — [OSS], 1 esemplare, e l'ipotesi era SBAGLIATA

Una riga MIDI è un **`<midiOutput>` dentro `<soundSources>`, fratello dei
`<sound>`**, e porta la sua altezza nell'attributo **`note`**:

```xml
<midiOutput name="" channel="0" note="0" />
```

Sta nella lista dei drum come qualunque altra riga: in
`refs/songs/TRASF401MIDI.XML` è la diciassettesima (indice 16), dopo sedici
`<sound>`, e la clip ci scrive sopra le note con `drumIndex="16"` come su
ogni altro drum.

**Cosa questo progetto aveva scritto prima, e perché era sbagliato.** Era stata
implementata l'ipotesi che una riga MIDI fosse un `<sound>` con il suo
`<midiOutput>` **figlio** attivo, e che l'altezza stesse in `noteForDrum`.
Sbagliata su entrambi i punti. Il `<midiOutput>` figlio esiste su ogni
`<sound>` ma vale `channel="255" noteForDrum="255"` in tutti e 1180 i casi del
corpus — è un'altra cosa, mai vista attiva, e non è la riga MIDI di un kit.
Il codice l'avrebbe classificata «saltata» e non l'avrebbe trasposta affatto.

⚠ **La lezione di metodo vale più della correzione.** Il ragionamento di allora
era: «l'assenza dal corpus non è una prova di assenza, perché il corpus sono le
song di una persona che quella funzione non ha usato — e `noteForDrum` è
comunque un attributo *osservato*, quindi non sto inventando una struttura».
La prima metà era giusta. La seconda no: **un nome osservato nel posto
sbagliato è comunque il posto sbagliato.** «Non sto inventando» non è lo stesso
che «ho visto».

Chiusa il 16 agosto facendo salvare dal dispositivo un kit con una riga MIDI —
`[AUDITION]+[MIDI]` sulla riga, come dice il manuale — e guardando cosa scrive.
Un solo esemplare è bastato a demolire mesi di ipotesi ragionevole.

### Verificato sul dispositivo

`TRASF002`/`TRASF101`/`TRASF201`/`TRASF301`/`TRASF401` (16 agosto 2026), cinque
song a un passo l'una dall'altra:

| | esito |
|---|---|
| trasposizione cromatica su synth, +12 | **funziona** |
| trasposizione diatonica, +1 grado in re minore | **funziona**: `re fa la re` → `mi sol la# mi`, cioè tono, tono, semitono — intervalli diversi fra loro, che è ciò che una trasposizione a intervallo fisso non produce |
| `double_time` su un kit | **funziona**: stessa battuta, pattern due volte più fitto |
| **`transpose` sugli osc di un kit** | **funziona e si sente**: kick e rim più acuti di una quarta |

L'ultima riga chiude l'ipotesi sul kit. `sposta()` e `half_time()` non sono
state provate a parte, ma usano `map_notes` e `stretch`, che `double_time`
esercita entrambe.

E `TRASF401MIDI.XML`, salvata dall'utente lo stesso giorno con una riga MIDI e
una nota sul terzo movimento, ha chiuso l'altra ipotesi — smentendola.

---

## 6-octies. La finestra di clip view: una geometria sola, tre unità

*16 agosto 2026. Verificato sul dispositivo con tre coppie controllate.*

**`yScroll` governa la finestra verticale di OGNI clip**, e la geometria è
sempre la stessa — quella già nota per song view (§3.1 dell'handoff):

    riga sullo schermo = valore − yScroll        visibile se 0 ≤ riga ≤ 7

Quello che cambia col tipo di clip è **l'unità** del valore. Ogni riga della
tabella è stata misurata con una coppia di file salvati dal dispositivo, in cui
la stessa nota è stata portata a mano dalla riga più bassa dello schermo alla
più alta — sette righe, sette unità di differenza, ogni volta:

| clip | l'unità è | coppia | prova |
|---|---|---|---|
| synth cromatico | il **semitono** | — | 0 falsi positivi su 44 clip del corpus |
| synth in scala | il **grado** della scala | `SCALA0/1`, `SCALB0/1` | D3 alla riga 0 → `yScroll=37`, che è il grado di D3 in re maggiore; alla riga 7 → 30 |
| kit | la **posizione della riga** | `KITSCR0/1` | kick (posizione 6 su 16) alla riga 0 → `yScroll=6`; alla riga 7 → −1 |

Le sei song stanno in `refs/songs/`. In codice la conversione vive tutta in
`song.clip_rows_with_notes()`.

### Il grado, in formula

    grado(y) = (y // 12) × |scala| + |{c ∈ scala : c ≤ y mod 12}|

cioè quante note della scala stanno in `[0, y]`. Per D3 (y=62) in re maggiore
dà 37, che è il valore scritto dal dispositivo.

### Cosa NON governa la finestra — [OSS]

`inKeyScrollOffset` e `drumsScrollOffset` **non si muovono** quando si scrolla
la clip view: restano identici nelle due song di ogni coppia. Governano
qualcos'altro, e cosa resta ignoto. Non vengono più scritti: mettere valori in
attributi che non si sono capiti è precisamente il modo in cui sono nati i
difetti raccontati qui sotto.

### Quattro modelli sbagliati di fila, e perché i test non li hanno visti

Vale più della conclusione, perché è il modo in cui questo progetto si fa male:

1. **`inKeyScrollOffset` governa la modalità a scala.** Falso. Da qui
   `fit_clip_scroll_to_notes()` scriveva l'altezza in `yScroll` e un valore
   calcolato in `inKeyScrollOffset`. Cinque song caricate sul dispositivo si
   aprivano con lo schermo vuoto.
2. **`drumsScrollOffset` governa i kit.** Falso: è `yScroll` anche lì.
3. **«Non muovere se almeno una riga si vede».** Regola giusta per song view,
   sbagliata per `fit`: lasciava la nota più bassa sulla seconda riga e la più
   alta fuori.
4. **`drumIndex` è la riga di schermo.** Falso: la riga è la **posizione** del
   nodo `<noteRow>`, e sul dispositivo l'ordine delle righe di un kit lo
   decide chi suona.

Nessuno dei quattro è stato trovato da un test, e non per mancanza di test:
erano tutti verdi, perché **asserivano il modello sbagliato**. Un test scritto
da chi ha l'idea sbagliata conferma l'idea sbagliata. Tutti e quattro sono
emersi guardando lo schermo del Deluge, ed è esattamente ciò che dice la regola
in testa all'handoff — che qui è stata violata quattro volte di seguito
dichiarando «verificato sul dispositivo» dopo aver *ascoltato*, non guardato.

⚠️ Nota su un numero pubblicato con troppa sicurezza: nel corpus una sola clip
di kit su 356 ha i nodi fuori dall'ordine dei `drumIndex` (`Xmasjam1.XML`).
Era stato scritto come se dimostrasse che riordinare è raro. **Non lo
dimostra**: se il dispositivo, riordinando le righe, rinumera anche i drum,
un kit riordinato risulterebbe comunque «in ordine» e quel conteggio non
misurerebbe nulla. Non è stato verificato. La conclusione — contare per
posizione — resta giusta comunque, perché la posizione *è* l'ordine di
visualizzazione per definizione.

---

## 7. Cosa resta non verificato

1. **La modifica delle note sul dispositivo.** Il tempo è validato, ma tocca due
   attributi di testo; le note toccano la codifica binaria dei blob, che è il
   pezzo dove un errore di layout non si vedrebbe fino al caricamento.
2. Il byte 13 di `noteDataWithSplitProb`: sempre 0 nel corpus, quindi il
   significato resta ipotetico (probabilmente *fill*).
3. La scala musicale dei parametri esadecimali.
4. Il comportamento con `<` `>` `"` nei nomi di sample (nessun campione).
5. Che il servizio SysEx risponda su questa build, e cosa faccia `devSysexAllowed`.
6. Non esistono synth standalone salvati da c1.3.0 sulla SD: la cartella
   `SYNTHS/` è ferma a versioni 3.x/4.x. Lo schema dei sound è stato ricavato dai
   `<sound>` incorporati nelle song, che sono la stessa struttura, ma un file
   `SYNTHS/*.XML` scritto da questa build non è mai stato visto.
