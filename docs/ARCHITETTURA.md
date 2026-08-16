# Architettura del Deluge, e come si riflette negli XML

Documento riscritto **a partire dalla documentazione**, non dai file. La
versione precedente faceva il contrario, e si vedeva: il primo duplicato di
clip prodotto dal progetto veniva scartato dal dispositivo per una regola
scritta a chiare lettere nel manuale.

Fonti, in ordine di autorità:

1. **Guidebook ufficiale Synthstrom, OS 4.1.0** — 338 pagine, sulla SD
2. **Documentazione community** — <https://delugecommunity.com>
3. **Codice del firmware e strumenti in `contrib/`**
4. **I file reali della SD**, per verificare che quanto sopra valga per
   *questa* build

### Copertura della lettura

Onestà su cosa è stato letto, perché una lettura parziale spacciata per
completa è peggio di nessuna lettura.

**Guidebook: letto per intero.** Tutti e quattordici i capitoli — Overview,
Basic Operation, Sequencing, Synthesizers, Kits, Modulation, Song View,
Arranger View, Audio, Looping, Effects, MIDI, CV, System & General. Il
quindicesimo, "Community Guide", è solo una legenda di scorciatoie.

**Sezione Development del sito: letta per intero** — Getting Started,
Guidelines, Tools, UX Principles, SysEx Protocol Notes, e le cinque pagine di
Website Development. Da lì viene la regola sulla compatibilità dei file citata
in §12.

**Documentazione community:** lette tutte le pagine con contenuto reale —
Concepts, Getting Oriented, Sequencer, Playback, User Interfaces, MPE, Audio
Files, SD Card, Engines, e le pagine Features (Arpeggiator, Automation View,
Velocity Editor, Chord Keyboard, DX7, MIDI Device Definition Files, MIDI Follow
Mode, Note/Note Row Editor, Performance View, Save/Load Patterns), più
Menu Hierarchies, Tips and Tricks, Questions and Answers.

Diverse pagine del capitolo Manual sono **segnaposto**: `device_files`,
`user_interfaces/view`, `synth_sample_engine` dichiarano esplicitamente
contenuti «planned for future updates». Dove è così, è indicato.

Convenzione:

- **[MAN]** affermato dalla documentazione
- **[OSS]** verificato nei file del corpus, con i numeri
- **[DER]** dedotto incrociando le due cose
- **[APERTO]** non chiarito

> **Versioni.** Il guidebook copre l'OS ufficiale 4.1.0; la build in uso è la
> community c1.3.0, che riparte da 1.x e aggiunge parecchio. Dove divergono,
> vincono i file.

---

## 1. Architettura di sistema

Dal diagramma del manuale [MAN]:

```
SONG
 ├── SongEffects (catena effetti globale)
 └── CLIPS ── ciascuna con la propria catena effetti e modulazione
      ├── SYNTH ENGINE   (subtractive, wavetable, FM, DX7)
      ├── KIT             (più elementi, ciascuno un suono)
      ├── AUDIO ENGINE    (audio clip e campionamento)
      └── MIDI / CV
```

E la frase che spiega la struttura dei file:

> «**Sequenced Patterns are Stored with the Song**» [MAN]

Ripetuta nel capitolo Sequencer, due volte:

> «Saving synth presets in clip view will only save the synth settings.
> **Patterns are stored with songs not in synth presets.**»
> «Patterns are not stored in kit presets, they are stored with songs.»

Ecco perché duplicare una clip funziona senza toccare `<instruments>`: la clip
porta con sé sia le note sia uno *snapshot* dei parametri di suono.

## 2. I file del dispositivo [MAN]

| file | dove |
|---|---|
| song | `SONGS/` |
| preset synth | `SYNTHS/` |
| preset kit | `KITS/` |
| preset e definizioni MIDI | cartelle dedicate |
| **pattern** | `PATTERNS/MELODIC`, `PATTERNS/RHYTHMIC/KIT`, `PATTERNS/RHYTHMIC/DRUM` |
| `MIDIFollow.XML`, `PerformanceView.XML`, `CommunityFeatures.XML` | `SETTINGS/` |

Tutti XML. Le cartelle `PATTERNS/` vengono create dal dispositivo al primo
salvataggio.

---

## 3. Le quattro viste

| vista | una riga è | contiene |
|---|---|---|
| **Clip** | un'altezza (synth) o un suono del kit | la griglia di note di una clip |
| **Song / session** | **una clip** | tutte le clip, raggruppate in sezioni |
| **Arranger** | uno strumento — è qui che si parla di *track* | istanze di clip disposte nel tempo |
| **Keyboard** | — | layout isomorfico per suonare |

Le **track sono un concetto dell'arranger**: in song view le righe sono clip.

> «Think of arranger view as an extension of song view rather than a
> stand-alone function.» [MAN]

Tre affermazioni che chiudono il modello dell'arranger [MAN]:

> «Clip 'instances' are **identical, linked copies** of the original clip.
> Changing the instrument notes, structure of the actual clip will change
> equally in all instances.»

> «**Only one row per instrument**, MIDI, CV, audio and therefore each instance
> resides on the same row.»

> «**White** clips in arranger view indicate **unique clip instances which are
> independent, detached from any original source clip**. Used for variations
> and fills.»

E fra le scorciatoie: «Make clip instance unique: `[SHIFT]+[PAD]` creates a
'white' clip instance».

Da cui: `<arrangementOnlyTracks>` contiene quasi certamente proprio le clip
**bianche** — quelle che esistono solo nell'arrangement. Le istanze normali,
essendo riferimenti a una clip di sessione, devono stare altrove,
presumibilmente dentro lo strumento. **Non verificato nei file.** [APERTO]

### Mappatura sull'XML [DER]

```
<song>
  <instruments>            gli strumenti: <sound> <kit> <midi> <cvChannel> <audioTrack>
  <sessionClips>           la vista SONG: una clip per riga
  <arrangementOnlyTracks>  la vista ARRANGER
  <sections>               i gruppi di lancio
  <modeNotes> <scales>     la scala della song
```

Una clip referenzia il proprio strumento per **preset** (synth e kit), per
**`trackName`** (audio), o per **canale** (MIDI, CV). Nel corpus non ci sono
due strumenti dello stesso tipo con lo stesso identificatore. [OSS]

---

## 3b. Clip clonate e preset "collegati"

Il capitolo Song View descrive due operazioni distinte che finora avevo
confuso in una.

**Clonare una clip** (§7.4) [MAN]:

> «The clip will be cloned from the target to the destination and **assigned a
> different section and won't be launched**. **Cloned clips are initially linked
> to the original** but can be edited.»

Quindi il dispositivo, clonando, fa esattamente le due cose che ora fa anche
`duplicate_clip()`: sezione diversa e non in riproduzione. Ma aggiunge un terzo
elemento — il **collegamento** all'originale.

**Scollegare un preset** (§7.4) [MAN]:

> «**Clips with the same preset cannot be used multiple times within multiple
> instruments in the same song.** If a preset is already in use, the preset can
> be unlinked from its "original" creating an independent version. Example, to
> reuse preset 10, a new unlinked version, can be created as 10A.»

Cioè: un preset può stare dietro a **un solo strumento** per song. Due clip
sullo stesso preset condividono per forza lo stesso strumento — sono
*collegate*. Per averne due davvero indipendenti bisogna clonare il **preset**,
non la clip, ottenendo `10` e `10A`.

### NON risolto: la clip duplicata non compare in song view [APERTO]

> **Attenzione.** Una versione precedente di questo documento dichiarava il
> problema risolto. Era sbagliato. La clip duplicata dal progetto **non compare
> sul dispositivo**, verificato guardando lo schermo. Tutto quello che segue
> descrive cosa dice il *file*, e il file non basta a spiegare il
> comportamento.

Ottenuta una song in cui il **dispositivo stesso** ha clonato una clip, salvata
e riportata sul PC (`refs/songs/Gen2_cloned_by_deluge.XML`). Confrontando il
clone del Deluge con il duplicato del progetto, attributo per attributo:

| | clone del Deluge | duplicato del progetto |
|---|---|---|
| `section` | **diversa** dall'originale | **diversa** dall'originale |
| `isPlaying` | **0** | **0** |
| `colourOffset` | uguale alla sorgente | uguale alla sorgente |
| `selected`, `beingEdited` | assenti | assenti |
| figli | `arpeggiator`, `soundParams`, `columnControls`, `noteRows` | identici |

**Nessuna differenza strutturale visibile.** Eppure la clip del dispositivo si
vede e la nostra no.

Altri fatti accertati, che rendono il caso più strano invece che più chiaro:

- nella song risalvata dal dispositivo la clip prodotta dal progetto **è
  presente nel file**, con le sue 9 righe e 16 note
- i blob di note sono **byte per byte identici** a come li avevamo scritti
- il file passa il round-trip del parser senza anomalie

Da cui avevo concluso — **sbagliando** — che il Deluge l'avesse caricata.
Che sia nel file dopo un salvataggio non dimostra che sia stata caricata in
memoria: il ragionamento saltava un passaggio, e la verifica sullo schermo dice
il contrario.

**Il problema resta interamente aperto.** Non si sa perché la clip non compaia,
e le ipotesi finora formulate (sezione, `isPlaying`, attributo di collegamento)
sono state tutte smentite o non hanno prodotto effetto.

## 4. Clip sullo stesso strumento: variazioni, non polifonia

La regola che avevo violato. Il manuale la dice due volte nella stessa pagina
[MAN]:

> «Deluge will only play one instrument at one time in song view. So for
> example, **if two clips use the same synth preset, the clip rows can each be
> launched but each one will stop playback of the other**, allowing only one
> instance of each instrument to play at one time.»

> «Where there are multiple instances of the same instrument preset they will
> not play simultaneously. Only one will play when launched and the others with
> the same instrument will be stopped.»

| più clip … | sono | in riproduzione insieme |
|---|---|---|
| sullo **stesso** strumento | **variazioni**, mutuamente esclusive | no |
| su strumenti **diversi**, stessa sezione | **polifonia** | sì, mute separabile |

**L'errore.** Il primo duplicato copiava `isPlaying="1"` dall'originale, che era
pure lui in riproduzione, sullo stesso preset. Uno stato che il dispositivo non
può rappresentare: caricando la song, il Deluge scartava silenziosamente la clip
in più.

`duplicate_clip()` ora forza `isPlaying="0"`, mette la copia in una sezione
libera, e avvisa se la si lascia nella stessa sezione dell'originale.

---

## 5. Sezioni

> «Song sections group together clips so that they can be controlled, launched,
> armed etc together making it easy to play arrangements and structure live
> sets.» [MAN]

- 12 colori nella colonna `[SECTION]` [MAN]; nel corpus si osservano **24**
  elementi `<section>` [OSS] — la discrepanza resta [APERTO]
- ripetizioni: `INFINITE` (predefinito), un numero, o "launch non-exclusively"
  [MAN]. `numRepeats="0"` = INFINITE [DER]
- una clip appartiene a **una sola** sezione [MAN]
- la community aggiunge le modalità **FILL** e **ONCE** oltre a INFINITE [MAN]

---

## 6. Note

Le cinque proprietà di una nota, dalla documentazione community [MAN]:
**velocity, probability, lift, iterance, fill**.

### Ranges dal manuale

| proprietà | valori | note |
|---|---|---|
| velocity | 1–127, predefinito **64** | «Deluge pads are not velocity sensitive. The default velocity is 64» |
| probability | **5–100%**, a passi di 5 | 20 gradini; 100% = suona sempre |
| iterance | da **`1of2`** a **`8of8`** | «'1of2' plays the note on the 1st of every 2 bars» — il ciclo è la **battuta** |
| lift | release velocity | |
| fill | **FILL** o **NOT-FILL** | suona solo durante il comando FILL, oppure solo fuori |
| repeat | ripetizioni distribuite | «distributes multiple triggers equally within the note's time interval» |

**Il dettaglio che spiega il nome dell'attributo** [MAN]:

> «As of version **1.3**, probability, iteration, and fill conditions
> **combine** rather than exclude each other.»

Prima le tre condizioni erano alternative e stavano in un byte solo; dalla
1.3 sono indipendenti e ciascuna ha il suo. Da qui `noteDataWith`**`SplitProb`**
e i tre byte in più.

### Probabilità collegate

Il manuale descrive un comportamento particolare quando più note nella stessa
colonna hanno la stessa percentuale [MAN]:

> «If multiple notes are set at the same %, example 65%, Deluge offers an
> additional option indicated by **LATCHING**, 65 & 65. The LATCHING option
> means the note will only trigger if the previous equivalent note triggers.»

E fra i suggerimenti community: «the displayed dot indicates whether
probabilities are **linked or independent**».

È il candidato più probabile per i valori del byte 10 compresi fra 21 e 127,
che i 20 gradini di probabilità non spiegano. Non verificato. [APERTO]

### La codifica, confermata da codice ufficiale

Il convertitore `contrib/midi2deluge/midi2deluge.py` del repo firmware genera
le note così:

```python
def encode_note(position, length, velocity):
    return f"{position:08X}{length:08X}{velocity:02X}4014000000"
```

Che si legge campo per campo, e **conferma per intero il layout derivato in
[FINDINGS.md](FINDINGS.md)**:

| pezzo | byte | significato |
|---|---|---|
| `{position:08X}` | 0–3 | posizione in tick |
| `{length:08X}` | 4–7 | durata in tick |
| `{velocity:02X}` | 8 | velocity |
| `40` | 9 | lift = 64 |
| `14` | 10 | 0x14 = 20 = probabilità **100%** |
| `00` | 11 | divisore iterance = nessuno |
| `00` | 12 | maschera passi iterance |
| `00` | 13 | fill |

Conferma indipendente di ogni campo, inclusi i due che avevo ricavato per
ipotesi (iterance) e il valore 20 = 100% dedotto dalla frequenza nel corpus.

---

## 7. Scale

- la scala è una proprietà della **song**, non della clip [MAN]: «All songs with
  multiple clips set to SCALE mode will always be locked to the same [scale]»
- sette scale occidentali cicliche più le scale utente [MAN]
- `rootNote` = tonica in semitoni da C; `<modeNotes>` = gli intervalli [OSS]
- `<scales><userScale>` è una **maschera a 12 bit** dei semitoni: `4095` =
  cromatica. Verificato che i bit accesi coincidano con i `<modeNotes>`, **8 su
  8** [OSS]
- `inKeyMode` sulla clip: `1` in scala, `0` cromatica [DER]

### `y` è un'altezza MIDI assoluta [OSS]

Verifica: su 1235 righe con note, **86% dentro la scala dichiarata**; le song
con tutte le clip `inKeyMode=1` sono al **100%**, e il crollo si ha solo dove
ci sono clip cromatiche (Progsong 47%, con 35 clip a `inKeyMode=0`).

`y="72"` è mostrato come **C4** dal dispositivo, quindi il do centrale MIDI 60
è C3. [OSS, un campione]

---

## 8. Griglia temporale

```
tick per movimento = 24 × 2^inputTickMagnitude     → 48 oppure 96
```

Confermato da due direzioni indipendenti [CONF]: dal dispositivo (una nota a
posizione 144 in una song con magnitude 2 cade sul quarto ottavo della prima
battuta) e dal corpus (il MCD delle posizioni raddoppia esattamente fra
magnitude 1 e 2).

Dal manuale [MAN]: la griglia è per default **1/16 su una battuta** nei 16 pad
orizzontali; si può zoomare fino a 1/128; la quantizzazione di registrazione va
da 1/4 di battuta fino a 1/64, predefinita 1/32. La lunghezza predefinita di una
clip è **1 battuta**.

### `inputTickMagnitude` è l'impostazione RESOLUTION [CONF]

Nel menu SETTINGS → DEFAULTS c'è [MAN]:

> **RESOLUTION** — «Resolution for new songs. Options are **96, 192, 384, 768,
> 1536, 3072, 6144**. Default is **384**.»

Quei sette valori sono esattamente `96 × 2^n` per n da 0 a 6. E poiché la
risoluzione conta le suddivisioni di una **semibreve** (quattro movimenti):

```
RESOLUTION = 4 × tick_per_movimento = 96 × 2^inputTickMagnitude
```

| `inputTickMagnitude` | tick/movimento | RESOLUTION |
|---|---|---|
| 0 | 24 | 96 |
| **1** | **48** | **192** |
| **2** | **96** | **384** (predefinita) |
| 3 | 192 | 768 |
| … | … | … |

I due valori osservati nel corpus, 1 e 2, corrispondono alle risoluzioni 192 e
384. Il modello dei tick, derivato dai dati e confermato dal dispositivo, è ora
chiuso anche dal lato del manuale: `inputTickMagnitude` **non** è un parametro
misterioso, è l'impostazione RESOLUTION della song.

Coerente anche con «nudging happens at the song's minimum resolution, default
**384th notes**».

---

## 9. Synth e kit: due tipi di riga

> «Individual sounds per row. Typically samples but also synth-based sounds, or
> MIDI/CV outputs.» [MAN]

Una `<noteRow>` porta **o** `y` **o** `drumIndex`, mai entrambi [OSS]:

| attributo | righe nel corpus | significato |
|---|---|---|
| `y` | 1686 | altezza MIDI, clip melodica |
| `drumIndex` | 2059 | quale suono del kit, indice da 0 |

130 clip su kit, 168 su synth. `affectEntire` è presente su **tutte** le clip
kit e su **nessuna** synth [OSS] — coerente col manuale, che descrive AFFECT
ENTIRE come controllo dei kit.

---

## 10. I file Pattern — rimandati, ma documentati

> **Decisione del 12 agosto 2026: il progetto va sulle song, non sui Pattern.**
> Le motivazioni sono in HANDOFF.md §4. In breve: i Pattern portano solo le note
> di una schermata, serve più controllo di così, e nel manuale ufficiale non
> esistono — è una feature community di cui non si è mai visto un esemplare
> scritto dal dispositivo. Questa sezione resta come documentazione, non come
> piano.

Scoperti leggendo la documentazione community.

> «A Pattern represents all notes of the current Deluge screen, including the
> attributes Velocity, Probability, Lift, Iteration, and Fill.» [MAN]

Sono XML autonomi in `PATTERNS/MELODIC` e `PATTERNS/RHYTHMIC/{KIT,DRUM}`. Si
caricano **nella clipboard** e si incollano dove si vuole.

Schema, dal convertitore ufficiale:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<pattern>
  <attributes
    patternVersion="0.0.1"
    screenWidth="..."
    scaleType="1"
    yNoteOfBottomRow="..."/>
  <noteRows>
    <noteRow
      numNotes="..."
      yNote="..."
      yDisplay="..."
      noteDataWithSplitProb="0x..."/>
  </noteRows>
</pattern>
```

Da notare: qui la riga usa **`yNote`** (altezza MIDI) e **`yDisplay`**, non `y`
come nelle song, e porta **`numNotes`**. Il blob di note è invece lo stesso
formato.

**Perché conta.** Generare un pattern invece di iniettare una clip in una song:

- non tocca nessun file esistente, quindi rischio nullo
- formato piccolo, dedicato, con implementazione di riferimento
- è esattamente il caso d'uso "dammi un pattern e mettimelo sul Deluge"
- esiste già `contrib/midi2deluge`, che converte MIDI in Pattern — quindi anche
  la strada "genera MIDI e converti" è percorribile senza scrivere nulla

Non sostituisce la modifica delle song (tempo, struttura, sezioni), e quello
che copre — le note di una schermata — la manipolazione delle song lo copre
già, con più controllo. Da qui la decisione di rimandarli.

---

## 9b. Il suono: sorgenti di modulazione e parametri

Il capitolo Modulation dà la matrice completa delle **sorgenti** [MAN]:

| sorgente | ambito |
|---|---|
| Sidechain, LFO1 | globale al suono |
| LFO2, ENV1, ENV2, Velocity, Note, Random, Aftertouch, X, Y | per voce |

Sono esattamente i valori di `source=` che compaiono nei `<patchCable>` del
corpus. Attenzione a un nome che non coincide: quello che il manuale chiama
**Sidechain** nell'XML si scrive `compressor`. [OSS]

Un'osservazione utile per generare suoni sensati: quando ENV1 o ENV2 modulano
qualcosa che non sia il volume, il comportamento è **bipolare** e il valore
neutro è **25** — sotto modula in negativo, sopra in positivo. [MAN]

Le destinazioni non sono tutte disponibili per tutte le sorgenti: i parametri
"globali al suono" (delay, mod FX, arpeggiator rate, reverb, LFO1 rate)
accettano solo Sidechain e LFO1; i parametri per voce accettano tutto. [MAN]

Il capitolo Synthesizers dà l'elenco completo dei parametri con i nomi che si
ritrovano negli attributi XML: `osc1/osc2` con `type` (sine, saw, square,
triangle, analogSaw, analogSquare, wavetable, sample, in/inL/inR/inLR),
`transpose`, `cents`, `retrigPhase`, `pulseWidth`, `feedback`; i modi di synth
**subtractive, ringmod, FM** (il wavetable si ottiene assegnando WAVE come tipo
di oscillatore, non è un modo a sé); `unison` con `num` e `detune`;
`polyphonic` con POLYPHONIC / MONOPHONIC / AUTO / LEGATO / choke per i kit;
i quattro stadi ADSR per envelope; `syncLevel` con la scala 2 bar … 128th.

Altri default dal menu SETTINGS [MAN]: velocity **64**, bend range **12**
semitoni (MPE **48**), scala predefinita major, swing interval 1/16.

## 10b. Lunghezza per riga, non solo per clip

Ogni `<noteRow>` può avere una **lunghezza propria**, indipendente da quella
della clip. [MAN] Emerge in due punti:

- il sequencer euclideo lavora per riga e uno dei tre parametri è «length of
  the sequence row, similar to clip length»
- fra i suggerimenti community: «Set different row lengths within kit clips
  (e.g. hi-hat at length 7, kick at length 11) to create unusual pattern
  ratios» — poliritmi

Nel corpus non l'ho ancora cercato: le clip esaminate hanno righe tutte della
stessa lunghezza della clip. Da verificare quale attributo lo esprima. [APERTO]

## 10c. Scala dei parametri

Tre livelli, tutti documentati [MAN]:

| dove | rappresentazione |
|---|---|
| file XML | intero con segno a 32 bit: `0x80000000` minimo, `0x00000000` centro, `0x7FFFFFFF` massimo [OSS] |
| interno | 0–128 |
| menu | **0–50** |
| patch cable | **−50 … +50** |

Il capitolo Effects conferma il livello display parametro per parametro:
EQ bass e treble **0–50 con 25 neutro**, decimation e bitcrush **0–50**,
delay amount e rate **0–50**, saturation **OFF e 1–15**. Gli envelope hanno
neutro **25** quando modulano qualcosa che non sia il volume.

La conversione esatta fra i tre livelli non è stata derivata dai file, ma il
quadro è chiaro: i parametri bipolari hanno il centro a metà scala, ed è per
questo che nell'XML si vede `0x00000000` come valore neutro accanto a
`0x7FFFFFFF` e `0x80000000`. [APERTO solo la formula precisa]

## 10c-bis. Tre livelli di effetti

Il capitolo Effects mostra che la catena esiste identica a tre livelli [MAN]:

```
suono (synth, o singola riga di kit)  →  kit  →  song
```

Ognuno con la propria HPF, LPF, EQ, delay, mod FX, decimation, bitcrush,
stutter, mandata di riverbero e compressore. È esattamente la ragione per cui
nell'XML gli stessi nomi di parametro compaiono a tre profondità diverse:
`<songParams>` per la song, i parametri della clip per il kit, e
`<soundParams>` / `<defaultParams>` per il singolo suono. Il riverbero fa
eccezione: è un send/return **globale alla song**, e per parte si regola solo
la quantità.

## 10d. Automazione

> «Automation Clip View settings are **saved per Instrument per Clip with the
> Song**.» [MAN]

- per le clip synth e kit: **81 parametri** automatizzabili con riga
  selezionata; **26** con AFFECT ENTIRE attivo e per le audio clip; **22** a
  livello arranger
- per MIDI e CV: i CC 0–119 più pitch bend, mod wheel, channel pressure
- si possono automatizzare anche i patch cable e le profondità di modulazione
- nei kit l'automazione ha **due livelli**: di clip e di riga
- l'interpolazione fra due punti è lineare; senza, i valori cambiano a gradini

## 11. Gli altri file XML del dispositivo

Oltre a song, preset e pattern:

| file | contenuto |
|---|---|
| `SETTINGS/MIDIFollow.XML` | `cc_mappings` (parametro → numero di CC, **255 = non mappato**) e `settings` (canali A/B/C, i 16 canali per track introdotti in c1.3, kit root note, feedback) |
| `SETTINGS/PerformanceView.XML` | assegnazione dei parametri alle 16 colonne, i valori degli 8 pad per colonna, e quali pad erano tenuti al salvataggio. Cancellandolo si torna ai default; è modificabile a mano usando i nomi esatti dei parametri |
| `SETTINGS/CommunityFeatures.XML` | i flag delle funzioni community |
| `MIDI_DEVICES/DEFINITION/*.XML` | etichette dei CC per dispositivi esterni: `<midiDevice><definitionFile/><ccLabels 0="" … 119=""/><hideUnlabeledCC value="0"/></midiDevice>`. Song e preset ne conservano una copia locale come riserva |
| `DX7/*.syx` | banchi di patch DX7, 32 patch per file, sottocartelle ammesse |

La cartella `DX7/` sulla SD, che avevo notato senza capirla, è questa.

## 12. Cosa aggiunge il firmware community

Le voci che toccano i file, dalla documentazione community [MAN]:

- **probability, iterance e fill indipendenti per nota** — i byte 11–13
- **scale utente** salvabili, `<scales>`
- **clip FILL e ONCE** oltre a INFINITE
- **nomi delle clip** salvabili
- **automazione** estesa, inclusi stutter per clip e tempo nell'arranger
- **LFO 3–4 ed envelope 3–4**
- **rinomina dei CC MIDI**, salvata per strumento
- **DX7** come tipo di synth (c1.2.0)
- **CV a 2 canali**, con sorgente CV2 selezionabile
- **conversione MPE→mono** per clip
- **song macros**, **Performance View**, **Grid View**

> «files (including songs, presets, etc.) that use community features may not
> ever load correctly on the official firmware again» [MAN]

Non è un problema per questo progetto: si usa solo il firmware community.

### La regola che protegge il nostro lavoro

Dalle linee guida per i contributori al firmware [MAN]:

> «Changes to user file structures (project/synth XML files) or flash
> configuration must ensure **upward compatibility** with files created by
> official firmware or previous community releases. **Downward compatibility is
> preferred** when possible — older firmware versions must not break with newer
> configurations stored on the device. **Automatic upgrade mechanisms should be
> implemented** where applicable.»

Cioè: il progetto non deve inseguire ogni release. Un file scritto oggi per
c1.3.0 continuerà a caricarsi sulle versioni successive, e le vecchie song
continuano a caricarsi su quelle nuove — il firmware le converte da solo. È
anche il motivo per cui la SD contiene song a firmware 3.x e 4.x che il
dispositivo apre ancora.

## 12b. Audio clip e looping

Le audio clip sono cosa diversa dai sample [MAN]: i sample sono materia prima
per synth e kit, le audio clip sono clip a tutti gli effetti, sincronizzate al
tempo per time-stretching.

L'attributo `inputChannel` che si osserva nell'XML corrisponde alle sorgenti
documentate: LEFT, RIGHT, STEREO, BALANCED, **MIX** (l'uscita del Deluge prima
degli FX master, per il resampling interno), **OUTPUT** (dopo gli FX), OFF —
ciascuna con una variante "col puntino" che attiva il monitoring. [DER]

Nel looping, **ogni overdub è una clip audio a sé**, creata nella riga sotto
l'originale: «overdub loops are technically individual audio clips and as such
they can be muted, deleted, and have effects applied» [MAN]. Questo spiega
`overdubsShouldCloneAudioTrack` fra gli attributi di `<audioClip>`. La prima
clip registrata fissa lunghezza e tempo; le successive vi si allineano.

---

## 12. Cosa resta aperto

- **come si rappresenta il collegamento fra due clip dello stesso strumento**
  — è il problema che blocca la duplicazione, e va risolto guardando una song
  in cui il dispositivo stesso ha clonato una clip
- quale attributo esprime la **lunghezza propria di una noteRow**
- il legame fra i tre livelli di scala dei parametri: int32 nel file, 0-128
  interno, 0-50 a display
- struttura delle **istanze di clip** nell'arranger. Il manuale chiarisce il
  modello — «only one row per instrument» e «clip instances are identical,
  linked copies of the original clip», mentre le clip **bianche** sono
  «unique clip instances which are independent, detached from any original
  source clip», che è quasi certamente cosa contiene `arrangementOnlyTracks` —
  ma la forma nel file non è stata guardata
- perché **24** `<section>` e non 12
- scala musicale dei **parametri esadecimali** (`0x7FFFFFFF` → dB, Hz)
- il byte 10 assume valori fra 21 e 127 non spiegati dai 20 gradini di
  probabilità: forse il LATCHING che il manuale cita quando più note hanno la
  stessa percentuale
- **MPE**: il setup usa Exquis in Lower Zone, mai guardato nell'XML
- come si distinguono **FILL** e **ONCE** da INFINITE nel file
- confronto dello schema **fra versioni di firmware** — servono centinaia di
  song 3.x/4.x della SD accanto alle 27 c1.3.0
