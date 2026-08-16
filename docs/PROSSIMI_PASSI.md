# Prossimi passi

## Il piano per la copertura massima

**Deciso il 12 agosto 2026: copertura massima conseguibile, niente
scorciatoie.** Niente strato in linguaggio naturale finché sotto non c'è
sostanza, e niente "basta partire da un template" usato come alibi per non
affrontare la creazione.

### La misura del territorio

Inventario sul corpus di 41 file: **359 path unici, 1442 attributi.**

| area | path | attributi | stato al 12 agosto |
|---|---|---|---|
| parametri di suono | 138 | **778** | valori sì (scala 0-50/128), struttura no |
| note e righe | 21 | 178 | **fatto**, verificato |
| kit e drum | 19 | 149 | note per nome sì, creare/cambiare drum no |
| clip | 17 | 105 | duplicare sì, creare da zero no |
| livello song | 14 | 99 | solo tempo e scroll |
| effetti | 34 | 90 | stessa scala, nessuna funzione dedicata |
| MIDI e CV | 10 | 26 | **fatto e verificato sul dispositivo** (FINDINGS §6-quinquies) |
| arranger | 8 | 37 | **fatto e verificato sul dispositivo** (FINDINGS §6-ter), tranne `section="255"` |

La riga dell'arranger diceva `1 | 0 | niente` ed era **sbagliata due volte**.
La prima per un errore di classificazione: i path delle clip d'arranger
contengono `instrumentClip` e finivano contati sotto «clip». La seconda perché
le posizioni temporali non stanno nei nodi ma in un attributo `clipInstances`
sugli strumenti — 2116 istanze su 24 song, cercate a lungo dove non erano.

La lettura è completa per costruzione — round-trip byte-esatto su 41/41. Il
numero che conta è quanto sappiamo **autorare**.

### Il fatto che ridimensiona tutto

Un file preset (`SYNTHS/*.XML`, `KITS/*.XML`) e il nodo strumento dentro la
song sono **quasi lo stesso nodo**: stesso tag, 8 attributi in comune.
Differenze, tutte sistematiche:

- il preset porta `firmwareVersion` e `earliestCompatibleFirmware`: si tolgono
- la song aggiunge `presetName`, `presetFolder`, `colour`, `defaultVelocity`,
  `activeModFunction`, `isArmedForRecording`
- `<defaultParams>` del preset diventa il `<soundParams>` della clip
- `<arpeggiator>` passa dallo strumento alla clip

Quindi **creare uno strumento non è scrivere 778 attributi: è istanziare un
preset**, che è ciò che fa il dispositivo. I 778 attributi restano da capire
per *modificare* il suono, non per crearlo.

### Le fasi, in ordine di dipendenza

**1. Istanziare preset e creare clip.** ✅ **FATTA E VERIFICATA** il 12 agosto:
`NUOVATRK.XML`, generata aggiungendo a `TEMPL0` una traccia che prima non
esisteva, **si apre e suona**. In `tools/delugexml/create.py`
(`instrument_from_preset`, `add_track`).

> Trappola trovata qui, e grave: il serializzatore ricopia i **byte originali**
> dei nodi non modificati usando gli span. `Node.copy()` li conserva — giusto
> dentro un documento, **rovinoso fra documenti**, perché i nodi del preset
> portano offset nel testo del preset. Produceva XML troncato e ricucito
> (`<modKnob controlsParam="modulato` / `Volume" />`), **scrivendo senza
> errori** e fallendo solo alla rilettura. Corretto con
> `Node.copy_detached()`, con test di regressione.

**2. Livello song.** Scala e root note, sezioni, lunghezza delle clip, swing,
time signature. 99 attributi, tutti testuali e già leggibili.

**3. Suono e FX.** La parte grossa. La scala dei valori c'è; manca l'accesso
per nome ai parametri e la creazione di strutture — oscillatori, inviluppi,
LFO, patch cable nuovi.

**4. Kit.** ✅ **FATTA E VERIFICATA**: `KITPLUS.XML`, un 17° drum preso da un
altro file di kit con il suo campione, **si sente**. In `tools/delugexml/kit.py`.

> `drumIndex` è una **posizione**, non un identificatore: `remove_drum()`
> rinumera ogni clip che usa il kit, altrimenti le note finiscono sul drum
> sbagliato senza alcun segnale. `check_indices()` verifica l'invariante.
> I parametri per singolo drum (75) funzionavano già: la noteRow di kit ha un
> `soundParams`, quindi `sound.py` la tratta come ogni altro contenitore.

**5. Automazioni su tutti i parametri.** ✅ **FATTA per i parametri PATCHED**,
verificata sul dispositivo. In `tools/delugexml/param_ids.py`.

Gli ID **non** si misurano uno per uno: vengono dall'ordine degli enum in
`param.h`, con la regola che le voci `FIRST_*` sono alias e non consumano un
valore. Tre ancoraggi verificati generando automazioni e ascoltando quale
parametro si muove:

| parametro | id | perché quello |
|---|---|---|
| `lpfFrequency` | 24 | dal file di un'automazione fatta a mano |
| `pan` | 23 | LOCAL a metà enum |
| `reverbAmount` | 47 | GLOBAL, **oltre la giunzione** `LOCAL_LAST = 45` |

Con un LOCAL e un GLOBAL corretti, uno scarto costante è escluso su entrambe
le metà. Validazione aggiuntiva senza dispositivo: i nomi risolti devono
esistere nel corpus, e 35 su 55 combaciano — i tre che non compaiono
(`pitch`, `volumePostFX`, `volumePostReverbSend`) sono destinazioni di patch
cable, quindi vivono altrove.

**Anche verificato: le coordinate `lastSelectedParamShortcutX/Y` non servono.**
Omesse per `pan` e `reverbAmount`, l'automazione funziona lo stesso.

**Anche gli UNPATCHED sono risolti**, con una sola misura. Automatizzando a
mano `arpeggiatorGate` su una clip di synth, il firmware ha scritto
`lastSelectedParamID="11"` e `lastSelectedParamKind="2"`. Tre risposte in un
numero:

- **11 e non 12** → i marcatori `FIRST_/LAST_ARP_PARAM` sono alias
- **11 e non 101** → `UNPATCHED_START = 90` **non** entra negli ID
- **Kind 2, non 3** → su una clip di suono gli unpatched shared sono
  `UNPATCHED_SOUND`. Il Kind dipende dal **contesto d'uso**, non dal
  parametro. [OSS] il caso arranger, dove sarebbero presumibilmente
  `UNPATCHED_GLOBAL`, non è verificato.

**83 parametri in tabella, 63 con nome, 5 ancoraggi verificati** che coprono
entrambe le metà dell'enum patched e quello unpatched.

**6. Arranger, audio, MIDI/CV.** ✅ **FATTA.**

> «Prima serve corpus: sei `audioClip` in tutto, `arrangementOnlyTracks` quasi
> assente» diceva questa riga, ed era **falso su entrambi i conti**. Il corpus
> ha 2116 istanze d'arranger in 24 song, 194 clip audio in 40 song, 94
> strumenti MIDI e 9 CV. Non mancava materiale: mancava sapere dove guardare —
> le posizioni d'arranger stanno in un attributo sugli strumenti, non nei nodi
> delle clip.

- **arranger** (`arranger.py`): `clipInstances`, clip bianche, sezioni.
  Verificato sul dispositivo con `ARRTEST`, `ARRWHITE`, `SCENE2`
- **MIDI/CV** (`midicv.py`): canali, suffix, CV2. Verificato con `MIDICV.XML`
- **audio** (`audio.py`): campioni, posizioni in frame, clip vuote.
  Verificato con `AUDIOTEST2.XML` — il primo tentativo faceva crashare il
  Deluge (E365) per una costante trascritta a mano invece che generata

Vedi FINDINGS §6-ter, §6-quater, §6-quinquies.

**7. Lo strato in linguaggio naturale.** ✅ **FATTA E VERIFICATA** il 15 agosto
2026. `tools/delugexml/musica.py` più la skill `deluge-pal`. Il ciclo ha
girato due volte sul dispositivo: `PAL01` generata da una descrizione a
parole, `PAL02` con la correzione chiesta a voce applicata alla song
riscaricata dal Deluge. **452 test.** Vedi HANDOFF §6-ter.

> La prova d'accettazione ha trovato tre difetti che 424 test non vedevano,
> perché tutti partivano da materiale già esistente invece di **creare** come
> crea il Pal: clip di kit senza righe, nessun modo di scrivere un accordo,
> nessuna avvertenza per le note oltre la fine della clip.

### Il piano è finito

Tutte e sette le fasi sono chiuse e verificate sul dispositivo. Ciò che resta
sono i punti aperti elencati in HANDOFF §7, non fasi di un piano.

### La regola che vale in tutte le fasi

Ogni fase si chiude **sullo schermo del Deluge**, non sul round-trip. Tre volte
su tre, quando qualcosa non compariva, il contenuto era giusto e mancava lo
stato di vista — vedi l'euristica in HANDOFF §2.

---


> **Aggiornato il 12 agosto 2026.** Le tre prove qui sotto sono **fatte**, e con
> loro sono caduti entrambi i blocchi storici: la clip duplicata (era fuori
> schermo, HANDOFF §3.1) e la scrittura SysEx (era il firmware, §3.2). La
> sezione resta come storia del percorso.
>
> Lo stato attuale è: si genera una song sul PC, la si deposita in `SONGS/` via
> USB con il Deluge acceso, e la si apre. Tutto verificato con hash e sullo
> schermo.
>
> **La direzione è la sezione B, completare il modello delle song.** I file
> Pattern (C-bis) sono stati valutati e **rimandati**: motivazioni in
> HANDOFF.md §4.

## Fatto — verifica sul dispositivo

Nessun file prodotto da questi strumenti era mai stato aperto dal Deluge. Finché
non succedeva, il progetto non aveva fondamenta: "byte-esatto" e "il dispositivo
lo carica" sono due affermazioni diverse.

Tre prove, in quest'ordine, ognuna da fare **su una copia** e mai sul file
originale:

### 1. File identico (controllo di sanità)

```bash
python tools/roundtrip.py refs/songs/Perche.XML --table out/format_table.json
```

Deve dire `1/1 byte-identici` in entrambe le modalità. Se sì, copiare
`refs/songs/Perche.XML` sulla SD con un altro nome e aprirla. Serve a escludere
che il problema sia la copia stessa.

### 2. Tempo modificato

> La **formula** del tempo è già confermata: `Mark.XML` originale letta sul
> Deluge mostra 88 BPM, il valore previsto. Quello che resta da verificare qui
> non è più l'aritmetica ma il fatto che il dispositivo apra un file **scritto
> da noi**.

```bash
python tools/dsong.py tempo refs/songs/Mark.XML --bpm 100 -o out/Mark100.XML
```

Copiare `out/Mark100.XML` in `E:\SONGS\` come `Mark100.XML` (nome nuovo, non
sovrascrivere). Aprirla: deve mostrare **100 BPM**.

Se non apre, il problema è la serializzazione e va investigato prima di
qualunque altra cosa.

### 3. Nota aggiunta

```bash
python tools/dsong.py note-add refs/songs/Perche.XML --clip 1 --row 72 --pos 144 --len 48 --vel 100 -o out/PercheN.XML
```

La clip 1 ha 12 note su 9 righe; la riga `y=72` ne ha una sola a pos 432. Dopo
la modifica ne ha due. Sul dispositivo va verificato che la nota nuova compaia
alla posizione giusta e con la velocity giusta.

---

## Dopo la verifica

### A — allargare il corpus

Il limite attuale non sono le regole ma la **copertura**. Il leave-one-out
fallisce solo dove un elemento compare una volta sola in tutto il corpus.

Materiale che manca e che si ottiene salvando dal dispositivo con questa build:

- ~~un **synth standalone** (`SYNTHS/`)~~ — **ottenuto** il 12 agosto:
  `refs/synths/TEMPL.XML`, 5 499 byte, il primo a c1.3.0
- ~~un **kit** salvato da questa build~~ — **ottenuto**:
  `refs/kits/CR78FROMMARS.XML`, 99 083 byte
- ~~una **song minimale** creata da zero~~ — **ottenute due**:
  `refs/songs/TEMPL0.XML` (11 804 byte, una clip vuota) e `TEMPL1.XML`
  (121 762 byte, una clip synth e una di kit con note a posizioni note in
  anticipo). Vedi la nota qui sotto su cosa NON sono
- una song con **arrangement** (non solo sessionClips): il corpus copre poco
  `arrangementOnlyTracks` — **resta da fare**

> **Attenzione su TEMPL0/TEMPL1: non sono i default di fabbrica.** Le due song,
> entrambe create nuove, hanno tempo, root note e swing **diversi fra loro**
> (158 BPM / root 2 / swing 2-7 contro 136 / root 7 / swing 9-7), e la clip
> vuota di TEMPL0 porta un preset reale, non uno di default.
>
> Il motivo, riferito da chi usa il dispositivo: **il Deluge randomizza BPM,
> root note e altri parametri a ogni creazione di una song nuova.** Non è
> ereditarietà dello stato, è casualità voluta. (Non verificato da me: due
> campioni non distinguono le due spiegazioni.)
>
> Due conseguenze. Un template neutro va **normalizzato da noi** (tempo, root,
> swing), non ottenuto salvando. E soprattutto: per costruire una coppia
> controllata **non si creano due song nuove** — si parte da una e si salva
> con un altro nome, perché la randomizzazione scatta alla creazione, non al
> salvataggio.
>
> Quello per cui valgono: sono piccole, sono di questa build, e le note di
> TEMPL1 stanno a posizioni decise in anticipo — kick a 0 e 192, snare a 96 e
> 288, synth a 0/96/192/288 su altezze crescenti con l'ultima tenuta. Il
> decoder è stato verificato contro una risposta nota, non contro sé stesso.

Dopo ogni aggiunta:

```bash
python tools/roundtrip.py refs --learn --table out/format_table.json
python tools/crossval.py refs
python tests/test_all.py
```

### B — completare il modello

Fatti: **duplicazione di una clip** e **creazione di noteRow da zero**
(`clip-dup`, `row-add`, e il giro completo in `demo_pattern.py`). Restano:

1. **Verifica sul dispositivo della clip duplicata.** È l'unica cosa che manca
   per considerare chiuso il pezzo. `out/Gen.XML` è pronto: contiene una clip
   `GEN` con un arpeggio di 16 note su due battute, costruita duplicando la
   clip 1 di `Perche.XML`. Da copiare in `E:\SONGS\` con un nome nuovo e
   aprire. Da controllare: che la clip nuova compaia in session view, suoni con
   il preset giusto, e che le note siano dove ce le aspettiamo.
2. **Scala musicale dei parametri esadecimali.** Serve per esporre volume,
   filtro e inviluppi in unità sensate invece che come `0x7FFFFFFF`.
3. **Byte 11–13 di `noteDataWithSplitProb`.** Quasi sempre 0; oggi vengono
   conservati senza interpretarli, il che è corretto ma limita.
4. **Kit e drum.** ~~Non ancora affrontato.~~ **Fatto e VERIFICATO SUL
   DISPOSITIVO** il 12 agosto 2026: `out/DRUMS1.XML`, generata sul PC e
   depositata in `SONGS/` via USB, si vede in session view e **suona
   correttamente** — kick sui movimenti 1 e 3, snare sul 2 e sul 4,
   charleston chiuso sulle crome con l'ultima aperta.

   Il riconoscimento delle clip di kit e la scelta fra `y` e `drumIndex`
   c'erano già. Quello che mancava era il passaggio **dai numeri ai nomi**:
   `drumIndex` è la posizione ordinale dentro `<kit>/<soundSources>`, e ogni
   suono lì dentro ha un `name`. Aggiunte in `song.py`: `instruments()`,
   `instrument_of()`, `drums()`, `drum_names()`, `drum_index()`.

   Sul CLI, `note-add` e `row-add` accettano ora `--drum SNARE` invece di un
   indice, e `dsong.py notes` stampa il nome del drum accanto all'indice.

   Due difetti reali trovati per strada, entrambi corretti:

   - `note-add` non passava `create=True` a `write_notes`, quindi falliva su
     ogni riga vuota. Sui synth non si vedeva perché la riga di destinazione
     aveva sempre note; **su un kit le 16 righe esistono tutte fin dall'inizio
     e quasi tutte sono vuote**, quindi era il caso normale
   - `row-add` su un kit dava un traceback, perché la riga c'è già. Ora spiega
     che su un kit si usa `note-add` e stampa il comando giusto

   Il legame nome → indice è verificato contro `TEMPL4`, dove le note erano
   state messe sul dispositivo in posizioni decise **prima** di leggere il
   file: se il legame fosse sbagliato, kick e snare non cadrebbero sui
   movimenti attesi.

### C — il canale SysEx: valutato, funziona

> **Chiuso il 12 agosto 2026.** Lettura e scrittura funzionano entrambe sulla
> nightly build 2d7cdf8. `dsysex.py` implementa `ping`, `dir`, `get`, `put`;
> `put` rifiuta di sovrascrivere e verifica sempre per rilettura con hash.
> `devSysexAllowed="0"` non impedisce nulla: il servizio risponde comunque.
> Il piano in tre punti qui sotto è stato eseguito. Resta valido l'avvertimento
> finale sui nomi nuovi.



Il firmware implementa un servizio di filesystem su SysEx (dettagli in
`FINDINGS.md` §6). Sostituisce la Fase 4 "copia sulla SD montata" con qualcosa
di molto migliore: scrivere in `SONGS/` via USB MIDI con il Deluge acceso.

In ordine, senza scrivere una riga di codice per i primi due passi:

1. Provare **[deluge-extensions](https://github.com/silicakes/deluge-extensions)**
   contro il dispositivo. Risponde su questa build? Basta un `doPing` o un `dir`.
2. Capire cosa fa `devSysexAllowed` (oggi `0` in `CommunityFeatures.XML`). Il
   servizio funziona lo stesso o va abilitato? Nel sorgente non si vede il
   controllo del flag, ma non ho letto tutto.
3. Solo se i primi due danno esito positivo, un client Python minimale:
   `open` + `writeBlock` + `close` è tutto ciò che serve per depositare una song.

Rischio da non sottovalutare: scrivere sulla SD mentre il dispositivo la sta
usando non è la stessa cosa che scriverci da spenta. Prima di usarlo sul serio
va capito cosa succede se si scrive la song attualmente caricata. Meglio
limitarsi a nomi nuovi.

### C-bis — i file Pattern: valutati e rimandati

> **Decisione del 12 agosto 2026.** Non sono la strada. Servono controllo su
> tempo, sezioni, strumenti e lunghezze, che un Pattern non porta; salvare e
> ricaricare una song sul Deluge è veloce, quindi il loro unico vantaggio reale
> — incollare senza perdere la sessione viva — vale poco qui. Motivazioni
> complete in HANDOFF.md §4. Quanto segue è la valutazione originale.


Leggendo la documentazione community è emerso che esiste un formato dedicato
proprio a quello che serve: i **Pattern**, XML autonomi in `PATTERNS/MELODIC` e
`PATTERNS/RHYTHMIC/`, che contengono le note con velocity, probability, lift,
iterance e fill, si caricano nella clipboard e si incollano dove si vuole.

Schema e dettagli in [ARCHITETTURA.md](ARCHITETTURA.md) §10.

Perché è meglio dell'iniezione di clip nelle song:

- non tocca nessun file esistente — rischio nullo
- formato piccolo e dedicato, con implementazione di riferimento ufficiale
  (`contrib/midi2deluge` nel repo firmware)
- è esattamente il caso d'uso "dammi un pattern e mettilo sul Deluge"

Da fare, in ordine:

1. Salvare un Pattern dal dispositivo per avere un esemplare reale scritto da
   questa build, e confrontarlo con lo schema del convertitore.
2. Verificare che le cartelle `PATTERNS/` esistano sulla SD (al momento no).
3. Implementare la scrittura di Pattern nella libreria — è molto meno lavoro
   della manipolazione delle song, e il blob di note è già fatto.
4. Provare anche `contrib/midi2deluge`: se genera Pattern validi, la strada
   "genera MIDI, converti" non richiede di scrivere nulla.

La manipolazione delle song resta utile per tempo, sezioni e struttura, ma per
la parte creativa i Pattern sono la strada giusta.

### D — solo alla fine, lo strato in linguaggio naturale

Non prima che A e B siano solidi. La forma più probabile è una skill che chiama
le funzioni della libreria, non un generatore di XML: l'XML lo deve scrivere solo
il codice testato, mai il modello direttamente.

---

## Task correlata ancora aperta

La migrazione di `SAMPLES/` dall'handoff (§5) non è stata toccata in questa
sessione. Il parser ora disponibile la rende molto più facile: si possono
estrarre tutti i riferimenti a file dagli XML di song, kit e synth, confrontarli
con l'albero reale di `SAMPLES/` e trovare i riferimenti rotti prima di spostare
qualsiasi cosa, invece che dopo.

Uno strumento `check_samples.py` che faccia questo è probabilmente il modo
migliore di affrontare quella task, ed è mezz'ora di lavoro con quello che c'è
già.

Prima di scriverlo però conviene guardare
[amiga909/deluge-synthstrom-utils](https://github.com/amiga909/deluge-synthstrom-utils),
che fa esattamente questo: analizza gli XML, trova i sample mancanti, li corregge
e produce un report. Se funziona sui file di questa build, non c'è niente da
scrivere.
