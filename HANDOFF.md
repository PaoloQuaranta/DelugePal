# HANDOFF — Deluge Pal

**Data:** 18 agosto 2026
**Progetto:** `D:\DelugePal` (fino al 14 agosto si chiamava `deluge-xml-workflow`)
**Pubblico su:** <https://github.com/PaoloQuaranta/DelugePal>, GPL-3.0 — vedi §9
**SD card:** `E:` quando è nel lettore del PC (spesso è nel Deluge, quindi assente)
**Firmware:** community **1.3.0-beta build 2d7cdf8** (2026-08-12), flashata il
12 agosto. La precedente era build 0856ff9 (2026-08-06), su cui la scrittura
SysEx era rotta — vedi §3.2.

Sostituisce `docs/HANDOFF_originale.md`, che resta come storia.

> ## Lo stato in tre righe
>
> **Il sistema tecnico è finito e il ciclo gira davvero: il collo di
> bottiglia adesso è musicale, non software.** Il 16 agosto Deluge Pal ha
> generato il suo primo pezzo vero — un dub in sol minore, tre versioni,
> ciascuna corretta dall'ascolto dell'utente. Verdetto sull'ultima: *«va
> meglio, ma musicalmente ci sarebbe ancora moltissimo da dire»*.
> **943 test.** Il progetto è **pubblicato su GitHub** senza il corpus.
> Il 17-18 agosto `docs/MUSICA.md` è stato **rifondato sullo schema neutro**
> (§6-duodecies): il reggae non è più la forma del documento ma un caso
> compilato fra molti, e l'**indice** dice cosa manca a quale repertorio.
> Dal 18 al 25 agosto il ramo `groove-midi` ha **chiuso la casella 6 del
> jazz** — la dinamica, misurata su cinque batteristi veri invece che presa
> dal web — e ha costruito il **groove template** (§6-terdecies). È il primo
> lavoro di questo progetto il cui risultato non è una funzione che passa i
> test ma **un'affermazione sul mondo**, e si vede da quanto è costato.
>
> Per usarlo si invoca la skill **`deluge-pal`**
> (`.claude/skills/deluge-pal/SKILL.md`), che contiene il protocollo. Le sei
> regole di quel documento non sono consigli: ognuna nasce da un errore pagato.
> La **regola 0**, aggiunta il 16 agosto, è l'ordine in cui si cerca una
> risposta — vedi §0 qui sotto.

---

## Il prossimo lavoro

**Le competenze compositive.** L'utente lo ha detto in chiaro dopo aver
ascoltato il terzo tentativo di dub:

> «Serve sicuramente che Pal acquisisca serie competenze compositive, che al
> momento sono limitatissime. Ce ne occuperemo prossimamente: sto raccogliendo
> moltissimo materiale e in una prossima chat ci occuperemo di costruire un
> database serio.»

È il lavoro nominato, e tutto il resto è secondario.

**Da dove si comincia, adesso che lo schema esiste: dall'indice in fondo a
`docs/MUSICA.md`.** Non serve una lista di cose da fare a parte — ogni casella
vuota dichiara *cosa servirebbe per riempirla*, quindi l'agenda si legge dalla
matrice.

⚠️ **Questa tabella dava due caselle per vicine a chiudersi, e il 25 agosto
2026 ne resta una.** La riga che c'era prometteva che il Groove MIDI avrebbe
chiuso «la 6 del jazz e i `[WEB]` della 6 del reggae»: **per il jazz è andata
così, per il reggae era falsa**, e il perché sta due righe più giù. È corretta
invece che lasciata perché è dall'agenda che la prossima sessione decide dove
mettere le mani, e un'agenda ottimista la rimanderebbe esattamente lì.

| casella | cosa la chiude, e dov'è |
|---|---|
| ~~**jazz 6** (dinamica)~~ | **chiusa il 25 agosto 2026**, dal ramo `groove-midi`: velocity, profilo posizionale e microtiming residuo di **cinque batteristi** del Groove MIDI, con la scheda che porta accanto a ogni numero quante esecuzioni e quanti batteristi lo reggono. Vedi §6-terdecies |
| **jazz 8** (melodia e ornamentazione) | `wjazzd.db`, già leggibile con `WJ.melodia()`/`WJ.armonia()`: 456 assoli con **gli accordi allineati alla linea**, guardati finora solo per lo swing |

⚠️ **La 6 del reggae il Groove MIDI NON la chiude, e non è una questione di
sforzo.** Di reggae quel dataset porta **venti esecuzioni**, che sono **quattro
`beat` continue** — a 78, 64, 141 e 126 BPM, **due di `drummer1` e due di
`drummer5`**, **dieci minuti in tutto** — più sedici fill di due-tre secondi
l'uno, tutti di `drummer1`, che valgono altri 43 secondi. **Due batteristi.** E
dentro la fascia di tempo che la casella 3 del reggae dichiara ci cadono **due
sole** di quelle quattro, la 78 e la 64, **entrambe di `drummer1`**.
Firmare quei numeri `[MIS]` col nome del genere sarebbe travestire un esecutore
da repertorio, che è precisamente ciò che la casella 8 del jazz vieta in una
riga: *un assolo è un musicista, non un repertorio*. La 6 del reggae **resta
`[WEB]`**, e adesso ci sta scritto il conteggio col motivo. Il jazz, per
confronto, ne ha **101** (50 `beat` e 51 `fill`) e **cinque** batteristi — ed è
già il minimo per cui valga la pena.

Cosa c'è già in mano:

| | |
|---|---|
| `docs/MUSICA.md` | non è più vuoto: uno schema neutro di **undici caselle**, pensato per reggere da Josquin alla jungle, più **il comune** a ogni repertorio e **l'indice** — la matrice repertorio × casella che è anche l'**agenda**: dice cosa manca a quale repertorio senza aprire niente. I repertori compilati sono schede a sé in `docs/repertori/`: oggi reggae/dub e jazz, stato di ciascuna nell'indice |
| `tools/delugexml/midi.py` | il ponte per far entrare il materiale: legge Standard MIDI File **senza dipendenze**, validato nota per nota contro `mido` |
| `tools/delugexml/groove.py` | il lettore del **Groove MIDI**, sopra `midi.py`: cerca per stile, batterista e metro, e ne cava la scala di velocity e il **groove template**. §6-terdecies |
| `to-read/` | 112 000 file e 4,8 GB di libri, paper e librerie MIDI già raccolti dall'utente. **Fuori dal versionamento** |

### Il perimetro vero, detto dall'utente il 17 agosto 2026

**Il dub era solo un banco di prova, non l'obiettivo.** Va scritto perché
tutta la documentazione precedente — questo file compreso — è tarata su di
esso, e chi la leggesse ne dedurrebbe uno scopo sbagliato:

> «Ho usato il dub solo come esempio per testare. Ho gusti musicali eclettici
> e mi piacerebbe coprire uno spettro compositivo più ampio possibile, dalla
> musica antica ai generi contemporanei, passando per classica e jazz.»

E l'ordine di priorità, dato subito dopo:

| | |
|---|---|
| **1** | **jazz** — «mi interessa moltissimo» |
| **2** | classica, barocca, antica (in quest'ordine) |
| **3** | i generi contemporanei: elettronica, IDM, techno, hip hop, trip hop, dub, DnB, jungle |
| — | **folk: lasciar perdere**, non interessa |

Il folk fuori dal perimetro ha un effetto collaterale utile: **spariscono i
due problemi di licenza** che bloccavano il materiale simbolico. TheSession
(40 000 melodie in ABC) vieta esplicitamente l'uso con LLM, e la Essen
Folksong Collection è distribuita a licenza. Erano entrambi folk.

### La decisione sui formati simbolici — 17 agosto 2026

La domanda era se valesse la pena aggiungere ABC, `**kern` o MusicXML.
**Per suonare sul Deluge nessuno serve**: MIDI porta già altezza, attacco,
durata e velocity, che è esattamente il modello dati del dispositivo. Servono
per *imparare*, e portano tre cose che MIDI non può portare: la **grafia**
(fa♯ contro sol♭), la **separazione delle voci**, e l'**analisi già fatta da
umani**.

| formato | esito | perché |
|---|---|---|
| **`wjazzd.db`** | **primo** | non è un formato di partitura ma è dove sta il jazz: 456 assoli con accordi e battiti allineati, **già su disco** in `to-read/MIDI/`, e si legge con `sqlite3` della stdlib |
| **MusicXML** | **sì** | costo ≈ zero (`xml.etree` + `zipfile`, stdlib: è XML *ben formato*, al contrario di quello del Deluge) ed è l'ingresso universale. Il suo `<harmony>` porta i simboli di accordo, quindi serve **anche** il jazz |
| **`**kern`** | **sì, dopo** | l'unico con l'analisi: `BachChoralesAnalyzed` ha lo spine `**harm` allineato movimento per movimento, e il Josquin Research Project è la musica antica, che non esiste altrove |
| **ABC** | **no** | licenza bloccata sul corpus grosso, ed è un formato folk: non ha antica, classica, jazz né contemporanea |

⚠️ **I generi contemporanei non esistono come repertorio notato**, e non è una
lacuna da colmare: il loro materiale sono i groove (MIDI, già in `to-read/`),
l'arrangiamento (`arranger.py`) e il suono (`sound.py`). Per jungle e DnB il
materiale compositivo è il **break tagliato**, che vive in `audio.py` e nelle
righe di kit, non in nessuna notazione.

⚠️ **Da sapere prima di ripartire:** le due skill di composizione sono ora
**due**, e nessuna delle due sa il reggae — vedi `SKILL.md` e la casella 11,
«Trappole del generatore», di `docs/repertori/reggae-dub.md`. I due difetti
di `music-composer` sono stati riparati a mano
il 16 agosto in una skill *globale* dell'utente, fuori da questo repo: se
viene reinstallata spariscono.

E una lezione di metodo che vale per tutto il lavoro futuro sui generi:

> **Una ricerca sola su un genere dà le etichette, non il mestiere.** Il primo
> dub è stato scritto dopo *una* ricerca web, da cui erano usciti i nomi (one
> drop, rockers, steppers) e nient'altro. Bastavano a produrre qualcosa di
> formalmente corretto e musicalmente morto — mancavano lo skank, il bubble,
> il turnaround, i colpi fantasma e lo swing, cioè tutto.

### Gli altri punti, in ordine di valore

**1. Le due misure rimaste aperte**, entrambe piccole e con il metodo ormai
collaudato (una coppia controllata, un passo di differenza):

- **cosa governano `inKeyScrollOffset` e `drumsScrollOffset`.** Si sa solo che
  *non* governano la clip view: non si muovono scrollandola. Finché non si sa,
  non si scrivono.
- **se riordinare le righe di un kit rinumeri i `drumIndex`.** Vedi la nota in
  fondo a FINDINGS §6-octies.

**2. I punti aperti sul formato** in §7, che sono lì da prima e non bloccano
niente.

**3. Due code della pubblicazione**, piccole: `SKILL.md` dice «Il progetto sta
in `D:\DelugePal`», che per un clone è falso; e l'hook di pre-push non è
versionato, quindi vale solo su questa macchina (§9).

### Cosa NON rifare

- **non estendere un controllo a un caso non misurato.** È costato quattro
  modelli sbagliati di fila il 16 agosto (§6-sexies). Se non c'è una coppia
  controllata, il controllo resta fuori e lo dice.
- **non scrivere in un attributo che non si è capito.** Due dei quattro difetti
  nascono da lì.
- **non usare il corpus come cancello.** Regola data dall'utente il 16 agosto e
  già costata una volta: il corpus dice cosa ha suonato *lui*, non cosa il
  firmware accetta. Il numero che lo dimostra: il firmware espone **56**
  destinazioni di patch cable, il corpus ne usa **37**. Per sapere cosa il
  firmware accetta si guarda `param_ids.py` (dall'enum di `param.h`) e il
  guidebook, mai il corpus.
- **non dire «verificato sul dispositivo» avendo ascoltato**, se
  l'affermazione riguarda ciò che si vede. E viceversa.
- **non scrivere un file con `pathlib.write_text()` nudo.** Su Windows traduce
  `\n` in `\r\n`, e un documento che era a LF esce tutto riscritto: due agenti
  diversi ci sono cascati nella stessa sessione del 24-25 agosto, gonfiando un
  diff da **260/92 righe a 1773/1293** — l'85% non era contenuto. Non corrompe
  niente e non rompe nessun test: rende **illeggibile la revisione**, che è il
  meccanismo su cui poggia tutto quello che è scritto qui. Si usa
  `write_bytes()`, oppure `open(..., newline='')`, e **prima di committare** si
  controlla che `git diff --stat` e `git diff --stat --ignore-cr-at-eol` diano
  lo stesso numero.

---

## Il ciclo, in breve

```
prompt  →  libreria  →  XML  →  SysEx  →  l'utente apre e ascolta
                                                  ↓
      ricarica come     ←   modifica   ←   «il basso è troppo statico»
      versione nuova          ↑
                     RISCARICA dal Deluge prima di toccare
```

**La fonte della verità è il file sul dispositivo**, non una copia locale:
l'utente la apre e può averci messo mano.

**Dove si scrive.** Solo dentro una sottocartella `DelugePal` delle quattro
cartelle di primo livello: `/SONGS/DelugePal/`, `/KITS/DelugePal/`,
`/SYNTHS/DelugePal/`, `/SAMPLES/DelugePal/`. Il percorso si costruisce con
`musica.destinazione()`, mai a mano. **In lettura invece l'accesso è libero su
tutta la SD** — l'asimmetria è voluta: si legge ovunque, si scrive solo in casa
propria. Il 15 agosto è servita una pulizia di 34 file di prova finiti in mezzo
alle 135 song dell'utente.

**La SD è stata ripulita il 16 agosto**, con la scheda nel lettore del PC. In
`/SONGS/DelugePal/` c'erano rimaste due song, e il 16-17 agosto se ne sono
aggiunte tre del pezzo dub (§6-septies):

| | |
|---|---|
| `TEMPL0.XML` | la **base pulita** da cui partire: uno strumento, una clip **senza righe né note**, arrangiamento vuoto, 158 BPM in re maggiore. È lo stesso file da cui nasce `create.CLIP_BASE`, copia verificata di `refs/songs/TEMPL0.XML` |
| `TRASF205.XML` | l'unica song generata **dopo** tutte le correzioni della finestra di clip view: si rilegge, passa il cancello senza avvertenze, entrambe le clip ancorate |
| `DUBPAL01/02/03.XML` | il primo pezzo vero, in tre versioni. **`DUBPAL02` e `DUBPAL03` sono state risalvate dall'utente sul dispositivo**, quindi la copia in `out/` NON è più la verità: riscaricare prima di toccarle (regola 1) |

Tolti 32 file fra rotti, versioni superate e artefatti delle sessioni
precedenti — comprese `USBGEN.XML` e `AUTOFULL.XML`, che stavano alla radice
di `/SONGS/`. Le sei song delle misure erano già in `refs/songs/` e
committate: la verifica per hash è stata fatta prima di cancellarle.

Nota su `TEMPL0` come base: la sua clip porta `yScroll="37"` e
`inKeyMode="1"`, ed è **quel 37 che si è propagato** in ogni clip generata
fino al 16 agosto, causando il difetto della finestra (§6-sexies). Non è un
problema del file — caricandolo sul Deluge e suonandoci sopra, la vista la
gestisce il dispositivo — ma di chi ne eredita gli attributi senza
ricalcolarli. Oggi `fit_clip_scroll_to_notes()` lo fa, ed è la ragione per cui
va chiamata sempre dopo aver scritto note.

Le 133 song dell'utente alla radice non sono state toccate. **Attenzione a
`Perche.XML`**: sta alla radice di `/SONGS/`, il nome sembra un file di prova
e invece è una song dell'utente — è byte-identica alla copia in `refs/songs/`,
da cui viene metà del reverse engineering. Il file di prova omonimo era
`PercheN.XML`, e non c'è più.

⚠️ **Come si era sporcata, per non rifarlo.** Cinque file erano finiti sulla
SD col nome **troncato** (`TRASF0`, `TRASF1`, … senza estensione) e uno come
voce da **0 byte**, perché un percorso costruito in PowerShell conteneva un
NUL: in una stringa a virgolette doppie `` `0 `` è l'escape del carattere
nullo. Il Deluge non li mostrava nemmeno come song. `put` si era dichiarato
«verificato per hash» ogni volta, perché rilegge il percorso su cui ha
scritto e non quello che si voleva — vedi `docs/SYSEX.md`, «la verifica per
hash di `put` non è una verifica di destinazione».

`dir` via SysEx non risponde su questo firmware, quindi con la SD nel Deluge
l'elenco vero della cartella si vede solo dallo schermo; con la SD nel lettore
si guarda da `E:\SONGS\DelugePal\`, che è molto più comodo per fare pulizia.

---

## 0. Leggi prima questo

Il progetto ha una regola che è costata caro impararla:

> **La documentazione dice cosa deve valere. I file dicono com'è scritto. Solo
> il dispositivo dice se funziona.**

Nella sessione del 12 agosto ho ripetutamente saltato il primo e il terzo
livello, deducendo dai file, e ho sbagliato ogni volta. In particolare:

- ho fatto reverse engineering statistico su cose spiegate in una frase del
  manuale;
- ho dichiarato **risolto** il problema principale perché la clip risultava
  presente nel file XML dopo un salvataggio del dispositivo. **Non lo era**:
  guardando lo schermo, la clip non c'è. Essere nel file non dimostra essere
  stata caricata.

Prima di dichiarare qualcosa risolto: **guardalo sul Deluge.**

### E la contromisura, aggiunta il 16 agosto: l'ordine di ricerca

Direttiva dell'utente, data dopo l'ennesima ricaduta. La regola sopra dice
**chi vince**; questa dice **da dove si comincia**, e va nella direzione
opposta:

```
1. documentazione community  →  2. guidebook  →  3. sorgente  →  4. file locali
```

**I file locali sono l'ultimo passo.** Servono a vedere com'è *scritta* una
cosa già capita, non a scoprire cosa fa il dispositivo. Partire da lì è
reverse engineering senza modello, ed è la causa comune a quasi tutti gli
errori raccontati in questo documento — compresi i quattro modelli sbagliati
qui sotto. È regola 0 della skill, e il dettaglio con le prove sta in
`docs/FONTI.md`.

Si **cerca dall'alto, si decide dal basso**.

### E il 16 agosto l'ho violata di nuovo, quattro volte di fila

Vale la pena leggerlo prima di cominciare, perché è il modo in cui questo
progetto si fa male, e sapere la regola non basta a non ripeterlo.

Cercando come funziona la finestra verticale di una clip ho costruito quattro
modelli sbagliati uno dopo l'altro — `inKeyScrollOffset`, poi
`drumsScrollOffset`, poi una regola presa in prestito dal posto sbagliato, poi
`drumIndex` scambiato per la riga di schermo. Ogni volta ho corretto, scritto
un test, ed ero convinto di aver chiuso.

**Nessuno dei quattro è stato trovato da un test**, e non per mancanza di test:
erano tutti verdi, perché asserivano il modello che avevo in testa. *Un test
scritto da chi ha l'idea sbagliata conferma l'idea sbagliata.* È il limite
strutturale del TDD quando l'ignoto non sta nel codice ma nel comportamento di
una macchina esterna.

E soprattutto: tre volte su quattro avevo scritto «verificato sul dispositivo»
avendo **ascoltato** invece che guardato. Le song suonavano giuste davvero — la
riproduzione non dipende dallo scroll — ma la domanda era un'altra.

> **Verificare vuol dire guardare la cosa di cui si sta parlando.** Se
> l'affermazione riguarda ciò che si vede, ascoltare non conta.

Cosa ha funzionato, invece, tutte e tre le volte: la **coppia controllata** —
due file identici tranne per un passo, fatti salvare dal dispositivo. Ha chiuso
lo scroll di song view (§3.1), la modalità a scala e i kit (§6-sexies), e la
riga MIDI di un kit (§6-quinquies). È il metodo di questo progetto.

Ordine di lettura consigliato:

1. `docs/ARCHITETTURA.md` — il modello concettuale, dal manuale
2. `docs/FINDINGS.md` — lo schema derivato dai file, con prove e numeri
3. `docs/MUSICA.md` — lo schema neutro delle **undici caselle** e ciò che vale
   per ogni repertorio; le schede compilate stanno in `docs/repertori/` e se
   ne legge **una per volta**. È il documento su cui verte il prossimo lavoro
4. `docs/SYSEX.md` — il canale USB MIDI
5. `docs/FONTI.md` — l'ordine di ricerca e quello di autorità, che sono opposti
6. `README.md` — ora è **in inglese**: è la porta d'ingresso del repo pubblico,
   non più la guida pratica. Per quella valgono `SKILL.md` e questo documento

---

## 1. Obiettivo

Descrivere strutture musicali e ottenerne file validi per il Deluge, sul
modello di Producer Pal ma **asincrono**: si generano file lato PC, si portano
sul dispositivo, si caricano.

---

## 2. Cosa funziona, verificato sul dispositivo

| | |
|---|---|
| **Lettura e riscrittura** | round-trip byte-esatto, 33/33 file del corpus, sia in modalità chirurgica sia ricostruendo tutto dalle regole di formato |
| **Cambio di tempo** | `Mark100.XML` (88 → 100 BPM, 11 byte diversi su 269 779) caricata sul Deluge, mostra 100 |
| **Aggiunta di una nota** | `PercheN.XML`, nota su C4 al quarto ottavo della prima battuta, velocity 100 — vista sul dispositivo |
| **Formula del tempo** | `BPM = 110250 / (campioni_per_tick × 2^inputTickMagnitude)` |
| **Griglia** | `tick/movimento = 24 × 2^inputTickMagnitude`; è l'impostazione RESOLUTION della song |
| **Layout dei blob di note** | confermato dal convertitore ufficiale `contrib/midi2deluge` del repo firmware |
| **Lettura file via SysEx** | 269 kB scaricati in 59 s con hash verificato |
| **Clip duplicata** | `SCROLLB.XML` aperta sul Deluge: 4 righe, la copia in fondo. Vedi §3.1 |
| **Geometria di song view** | ogni clip è una riga; 8 righe a schermo; la clip `i` sta alla riga `i - yScrollSongView` |
| **Scrittura via SysEx** | `SONGS/USBGEN.XML` depositata via USB a Deluge acceso, 35 133 byte, hash verificato per rilettura |
| **Cosa tocca l'aggiunta di una clip** | misurato su una scala controllata di 4 salvataggi: `preview`, `yScrollSongView`, `yScrollArrangementView`, e nient'altro. `FINDINGS.md` §6-bis |
| **Le due regole di scroll** | song view conta le clip, arranger conta gli strumenti. La nostra formula dà gli stessi valori scritti dal dispositivo |
| **Percussioni** | `DRUMS1.XML`, generata sul PC indirizzando i drum **per nome** e depositata via USB: si vede e **suona** — kick 1·3, snare 2·4, charleston sulle crome |
| **Creare tracce da zero** | `NUOVATRK.XML` e `BASSO.XML`: strumento istanziato da un preset, clip, note, suono progettato. Un preset e il nodo strumento sono quasi lo stesso nodo |
| **Kit** | `KITPLUS.XML`: 17° drum preso da un altro file di kit, col suo campione. Si sente |
| **Automazioni per parametro** | tabella ID da `param.h`, tre ancoraggi verificati (24, 23, 47) su entrambe le metà dell'enum |
| **Automazioni** | rampa del cutoff LPF generata dalla libreria, `AUTOFULL.XML`: si vede sul dispositivo. Formato confermato sul **sorgente** (`auto_param.cpp`), non dedotto |
| **Scala dei parametri** | `display = (int32 + 2³¹) / (2³²/50)`, e griglia interna a 128 verificata muovendo una manopola a un valore noto |
| **Rimozione** | `RIMOSS001`/`RIMOSS101`, due song identiche tranne per una traccia tolta: sul Deluge la battuta 2 è vuota e **le battute 3 e 4 suonano ancora il proprio materiale**, cioè i `clipCode` rinumerati puntano giusto |
| **Trasposizione, synth** | `TRASF101` cromatica, `TRASF201` diatonica: `re fa la re` → `mi sol la# mi`, cioè tono, tono, semitono — intervalli diversi fra loro, che una trasposizione a intervallo fisso non produrrebbe |
| **Trasposizione, kit** | `TRASF401`: `transpose` sugli oscillatori dei drum, kick e rim **si sentono** più acuti di una quarta |
| **Double time** | `TRASF301`: stessa lunghezza di battuta, pattern due volte più fitto |
| **La finestra di clip view** | tre coppie controllate — `SCALA0/1`, `SCALB0/1`, `KITSCR0/1` — che danno **una geometria sola**, `riga = valore − yScroll` su otto righe, con l'unità che cambia: semitono, grado, posizione della riga. Vedi §6-sexies |
| **La riga MIDI di un kit** | `TRASF401MIDI`, fatta salvare dal dispositivo: è un `<midiOutput>` **fratello** dei `<sound>` dentro `<soundSources>`, altezza in `note`. Ha **smentito** l'ipotesi che il progetto aveva implementato. FINDINGS §6-septies |

| **Suoni progettati da zero** | `DUBPAL01`: kit **sintetizzato** (nessun campione), basso wobble, pad, sirena — tutti costruiti dal synth vuoto. Si sente. Vedi §6-septies |
| **Patch cable** | `lfo1 → lpfFrequency` (wobble), `lfo1 → pitch` (sirena), `envelope2 → oscAPitch` (pitch drop del kick): si sentono sul dispositivo |
| **Sintesi FM da un preset subtractive** | `structure.set_synth_mode(inst, 'fm')` crea i `<modulator1/2>` che il synth vuoto non ha e toglie il `type` dagli oscillatori, come fa il dispositivo |
| **Le posizioni fuori griglia sopravvivono al salvataggio** | `GROOVE1`, 31 note con scarti da −6 a +2 tick, aperta sul Deluge, **nessuna nota toccata**, risalvata dal dispositivo e riscaricata: **31 posizioni su 31 conservate**. Il Deluge **non riquantizza**. È meccanico, si legge nei byte. §6-terdecies |

La tabella qui sopra si è fermata all'11 agosto. Da allora sono arrivate le
fasi 6 e 7 — arranger, MIDI/CV, audio, e lo strato in linguaggio naturale —
tutte verificate sul dispositivo: vedi §6-ter e `docs/FINDINGS.md`.

**943 test** in `tests/test_all.py`, tutti verdi. Gli **84** aggiunti dal 18 al
25 agosto sono quelli del Groove MIDI e del groove template (§6-terdecies): una
parte legge il dataset e quindi salta senza `to-read/`, un'altra gira su **file
MIDI sintetici costruiti apposta**, così che gli invarianti veri — che l'origine
della griglia si tolga per intero, che il residuo torni zero quando lo swing è
noto, che `applica_groove()` non inventi su un passo senza appoggio — siano
verificabili anche da chi il corpus non ce l'ha.

⚠️ **Con il corpus sul disco sono 943 su 943 e zero saltati. In un clone —
niente `refs/` tranne `TEMPL.XML`, niente `corpus_versions/`, niente
`to-read/` — sono 460 su 460 con 82 SALTATI e ZERO fallimenti.** Questa cifra
è **misurata, non derivata**, il 25 agosto 2026: `git archive HEAD` in una
cartella vuota, che dà per costruzione esattamente i file versionati, e la
suite lanciata da lì con lo stesso `.venv`. I salti non sono un guasto:
`refs/` e `corpus_versions/` non sono più versionati (§9), e `salta()`
distingue "manca materiale che non è del repo" da "il codice è rotto".

⚠️ **E cade quello che questo documento diceva prima**, cioè che due test
*falliscono* senza corpus. **In un clone non fallisce niente**, e le ragioni
sono due, tutt'e due verificate rieseguendo:

| test dato per rotto | com'è davvero |
|---|---|
| `corpus di riferimento presente` | non scatta: `refs/synths/TEMPL.XML` **è pubblicato** (§9), quindi `refs/` non è mai vuota in un clone e il round-trip gira su quell'unico file |
| `COPPIE_OSSERVATE coincide con quella ri-derivata dal corpus` | **salta**, non fallisce: sopra di lui c'è già un `salta()` che scatta sotto le 50 coppie, ed era lì anche prima di questo ramo |

Quindi la riga vecchia era sbagliata su tutti e due i punti, e non per colpa
di questo ramo: era sbagliata anche su `main`. **L'unico modo di farne fallire
uno è togliere `refs/` per intero** — cosa che nessun clone fa — e allora è
uno solo: 428 su 429 con 84 saltati, e il rosso è `corpus di riferimento
presente`, che asserisce l'esistenza di una cartella. Misurato lo stesso
giorno, con lo stesso metodo, cancellando `refs/` dalla copia.

> **Euristica guadagnata sul campo, quattro volte.** Se un contenuto scritto
> correttamente non compare sul dispositivo, **cercare lo stato di vista prima
> di sospettare del contenuto.** È successo con `yScrollSongView` (clip una
> riga sotto lo schermo), con lo stato della vista automazione, con
> `beingEdited` (si apriva un'altra clip) e con `inKeyMode` (note fuori scala
> senza una riga su cui esistere). Ogni volta il dato era giusto.
>
> ⚠ **Attenzione al quarto caso: la mia diagnosi era SBAGLIATA.** Avevo
> concluso che le note fuori scala non hanno una riga e non suonano. Falso —
> il dispositivo adatta la scala, e `Progsong.XML` ha 315 note fuori scala.
> Il difetto reale era che una clip creata da un modello eredita `yScroll` e
> `inKeyScrollOffset` dal modello: usare `fit_clip_scroll_to_notes()`.
> Il racconto dell'errore, con i due sbagli di metodo che l'hanno prodotto,
> è in FINDINGS.md — vale più della conclusione.

---

## 3. I due blocchi storici, entrambi chiusi il 12 agosto 2026

### 3.1 La clip duplicata non compariva — RISOLTO

**Non era un problema di caricamento. La clip era sotto il bordo dello
schermo.**

In song view ogni clip è una riga e la finestra visibile parte da
`yScrollSongView`, un attributo del nodo `<song>`. La clip di indice `i` sta
alla riga `i - yScrollSongView`, e le righe sono 8, numerate 0–7.
`Perche.XML` ha 3 clip e `yScrollSongView="-5"`: occupano esattamente le righe
5, 6, 7. Accodandone una quarta senza toccare lo scroll, quella finisce alla
riga 8, che non esiste.

`duplicate_clip()` non toccava lo scroll: la stringa `yScroll` non compariva da
nessuna parte nella libreria.

Le tre prove, nell'ordine che vale:

1. **Manuale**, cap. 7 Song View: «Individual clips compressed to one row each
   in song view. The rows can be navigated up and down *beyond the 8 physically
   displayed*.» Di nuovo una cosa spiegata in una frase.
2. **File scritti dal dispositivo**: clonando una clip, il Deluge ha spostato
   lui stesso `yScrollSongView` da `-5` a `-4`, per tenere la riga nuova in
   fondo allo schermo.
3. **Dispositivo**: due file diversi per **un solo byte** (offset 1084),
   `SCROLLA` con `-5` e `SCROLLB` con `-4`. A mostra 3 righe con la quarta
   nascosta, B ne mostra 4. Protocollo e esito in `docs/TEST_yscroll.md`.

Correzione: `scroll_song_view_to()` in `tools/delugexml/song.py`, chiamata da
`duplicate_clip()` dopo l'append. Alza lo scroll solo quando serve — una vista
che già mostra la riga non viene spostata, perché è lo stato che l'utente ha
lasciato. Coperta da `test_scroll_song_view`.

Perché è costata due sessioni: **la differenza è stata cercata dentro la clip,
e non c'era.** Era nel nodo `<song>`. Confrontare i file ha continuato a dire
"identici" perché lo erano davvero, nella parte guardata.

### 3.2 La scrittura via SysEx — RISOLTA dal firmware

Era **PR #4633, "Fix USB MIDI receive packet loss"**, come ipotizzato.
Sulla nightly `1.3.0-beta build 2d7cdf8` (12 agosto 2026) la scrittura
funziona, senza toccare una riga del client:

| | prima (build 0856ff9) | ora (build 2d7cdf8) |
|---|---|---|
| blocco 64, file da 256 B | 22 byte su 64 | 256/256, hash identico |
| `Perche.XML`, blocco 768 | si ferma a **1000 byte esatti** | 28 715/28 715, hash identico |
| perdita | ~75% dei blocchi | **0 timeout, 0 blocchi parziali, 0 riaperture** |
| velocità | 4,6 kB/s in lettura | 62,6 kB/s in scrittura |

Depositare una song generata in `SONGS/` via USB, con il Deluge acceso e la SD
dentro, ora funziona ed è verificato per rilettura con hash.

---

## 4. La direzione: le song. I Pattern sono rimandati

**Decisione del 12 agosto 2026, presa dopo aver riesaminato la questione.**
La direzione è la **manipolazione delle song**. I file Pattern restano
un'opzione per uno stadio molto più avanzato del progetto.

Le sessioni precedenti raccomandavano il contrario. Quella raccomandazione
poggiava su quattro argomenti, e oggi non reggono:

| argomento di allora | stato |
|---|---|
| «aggira completamente il problema 3.1» | **caduto**: il 3.1 è risolto (§3.1) |
| «non tocca file esistenti, rischio nullo» | il rischio non si è mai materializzato: `put` non sovrascrive, roundtrip byte-esatto 33/33 |
| «implementazione di riferimento ufficiale» | è `contrib/midi2deluge`, un convertitore MIDI, non un file scritto dal dispositivo |
| «è esattamente il caso d'uso» | vero, ma vale solo per le note |

Le ragioni della scelta:

- **serve il massimo controllo.** Un Pattern porta solo le note di *una
  schermata* — niente tempo, sezioni, strumenti, lunghezze, sound design. La
  song le porta tutte.
- **salvare e ricaricare una song sul Deluge è veloce**, quindi il vantaggio
  vero dei Pattern (incollare senza ricaricare, mantenendo la sessione viva)
  vale poco in questo flusso di lavoro.
- **la base di prove è debole.** Nel manuale ufficiale i Pattern non esistono:
  tutte le occorrenze di "pattern" nel guidebook sono nel senso generico di
  sequenza. È una feature del solo firmware community, documentata solo dalla
  doc community — la stessa fonte che sui byte di comando SysEx è **sbagliata**.
  Nessun esemplare scritto dal dispositivo è mai stato visto.

Se un giorno si riprendono, il primo passo resta quello: farne salvare uno dal
dispositivo e confrontarlo con lo schema in `docs/ARCHITETTURA.md` §10 prima di
scrivere una riga di codice. Le cartelle `PATTERNS/` sulla SD non esistono
ancora, quindi non le ha mai usate nessuno.

---

## 5. Il progetto

```
D:\DelugePal\
  README.md              uso pratico
  HANDOFF.md             questo file
  docs\
    ARCHITETTURA.md      modello concettuale, dal manuale e dalla doc community
    FINDINGS.md          schema derivato dai file, con numeri e prove
    MUSICA.md            schema neutro delle undici caselle, il comune, l'indice
    repertori\           una scheda per repertorio compilato: reggae-dub.md, jazz.md
    SYSEX.md             canale USB MIDI: cosa funziona e cosa no
    FONTI.md             cosa è stato letto, in ordine di autorità
    PROSSIMI_PASSI.md    piano operativo delle sette fasi, chiuso
    PIANO_rimozione.md   il piano della rimozione, con il censimento misurato
    PIANO_trasformazioni.md  il piano delle trasformazioni. §3.0-bis e' tenuta
                         SBAGLIATA di proposito: l'errore vale piu' della
                         conclusione, e la correzione e' in FINDINGS §6-septies
    TEST_yscroll.md      l'esperimento che ha chiuso §3.1, con il metodo
    SCHEMA_song_c1.3.0.md, SCHEMA_kit_c1.3.0.md   inventario generato
    HANDOFF_originale.md l'handoff di partenza, per storia
  tools\
    delugexml\           la libreria (parser, writer, notes, song)
      sound.py           parametri E patch cable (`set_patch_cable`)
      structure.py       forme d'onda, modi di sintesi, modulatori FM
      midi.py            lettore Standard MIDI File, SENZA dipendenze
      wjazz.py           lettore della Weimar Jazz Database (solo sqlite3)
      groove.py          lettore del Groove MIDI: elenco, scala di velocity,
                         groove template. Non tocca mai un Document
      musica.py          lo strato in lingua musicale
    dsong.py             CLI: info, notes, tempo, note-add, clip-dup, row-add
    misura_groove.py     le misure delle caselle 4, 6 e 9 del jazz: si esegue,
                         si legge, i numeri si scrivono a mano nella scheda
    genera_groove.py     la coppia GROOVE0/GROOVE1 del cancello. NON e' un
                         pulsante da premere: rigenerarla sovrascriverebbe
                         l'unico esemplare ascoltato (§6-terdecies)
    genera_swing.py      la coppia SWINGA/SWINGB dell'astrazione dello swing
    dsysex.py            client SysEx: ping, dir, get, put — tutto funzionante
    …                    una ventina di strumenti di analisi, vedi README
  to-read\               112 000 file, 4,8 GB di libri e librerie MIDI raccolti
                         dall'utente. NON versionato: e' opera di terzi, e
                         percorrerlo faceva andare `git add` in timeout
  refs\                  59 file c1.3.0 — corpus di riferimento. **NON PIU'
    VERSIONATO** (§9): sta sul disco, git lo ignora. L'unico file pubblicato
    e' `synths/TEMPL.XML`, il synth vuoto del firmware.
    songs\ 43, kits\ 3, synths\ 2, settings\ 3, sd_salvati\ 8. Tutti scritti
    dal dispositivo.
    Dentro ci sono QUATTRO gruppi controllati, ognuno una misura: non
    separarli e non "ripulirli", sono le prove su cui poggiano i documenti.
      TEMPL0 -> TEMPL2 -> TEMPL3 -> TEMPL4   cosa tocca l'aggiunta di una
                         clip (FINDINGS §6-bis)
      SCALA0/1, SCALB0/1 la finestra in modalita' a scala: yScroll conta i
                         GRADI (FINDINGS §6-octies)
      KITSCR0/1          la finestra di una clip di kit: yScroll conta la
                         POSIZIONE della riga (FINDINGS §6-octies)
      TRASF401MIDI       l'unico esemplare di riga MIDI in un kit, che ha
                         smentito un'ipotesi (FINDINGS §6-septies). E' anche
                         l'unico file che non si ricostruisce byte-esatto
                         dalle regole di formato — vedi FINDINGS §2.2-bis,
                         e' noto e nominato nel test
  corpus_versions\       103 song di 16 versioni firmware (3.0.0 → 4.1.4-alpha,
                         c1.1.0, c1.2.0), divise per versione. FUORI da refs\
                         di proposito: la tabella di formato si apprende solo
                         da c1.3.0 e queste la inquinerebbero.
                         Anch'esse NON piu' versionate (§9)
  out\                   tabella di formato, inventari, file generati. L'unico
                         versionato e' `format_table.json`: e' un artefatto
                         DERIVATO e non contiene musica
  tests\test_all.py      943 test (460/460 + 82 salti in un clone, misurato)
  .venv\                 mido + python-rtmidi, per il SysEx
```

Python 3.13 di sistema per tutto tranne il SysEx, che usa `.venv`.

---

## 6. Il vincolo che ha determinato l'architettura

**Il firmware non scrive XML valido.** 255 song su 378 vengono rifiutate da un
parser conforme:

- `&` mai escapato (confermato nel sorgente: `writeAttribute` non escapa nulla)
- blocchi di attributi duplicati su `<audioClip>`
- formato legacy con due elementi radice

Quindi niente `xml.etree`: c'è un parser tollerante su misura in
`tools/delugexml/parser.py`, che conserva gli offset nel sorgente. Grazie a
questo un nodo non modificato viene riemesso **ricopiando i byte originali**:
cambiare il tempo di una song da 8577 righe tocca esattamente 2 righe.

La tabella di formato è **appresa dal corpus**, non derivata per regole — e
questa non è una scorciatoia: il sorgente mostra che la formattazione è un
booleano `onNewLine` deciso a ogni singola chiamata, quindi non esiste nessuna
regola da scoprire.

---

## 6-ter. Lo strato musicale — fase 7, chiusa il 15 agosto

`tools/delugexml/musica.py` traduce fra lingua musicale e chiamate alla
libreria. **Il modello non scrive mai XML**: chiama queste funzioni, che a loro
volta chiamano codice coperto da test.

| per | funzione |
|---|---|
| leggere cosa c'è, in termini musicali | `racconta(doc)`, `racconta_clip(doc, clip)` |
| altezze | `altezza('re2')`, `nome_altezza(38)` — italiano e inglese |
| batteria | `passi('x...x...x...x...')` — un carattere per sedicesimo, come la griglia |
| melodie | `melodia('re2 fa2 la2', durata='1/8', articolazione='staccato')` |
| accordi | `accordi('re3 fa3 la3 \| sib3 re4 fa4')` — le note insieme, progressione in una riga |
| suono e mix | `applica_verbo(doc, nodo, 'piu scuro')`, che riferisce cosa ha mosso |
| **il cancello** | `verifica(doc)` **blocca**, `avvertenze(doc)` **informa** |
| dove salvare | `destinazione(nome, versione, cartella)` |

**`verifica()` è la regola che non si salta**: nessun file sale sul dispositivo
se non è vuota. Ferma il primo dei due file rifiutati dal Deluge — la clip di
kit che si dichiarava synth (FINDINGS §6-quater) — e ha fermato la prima song
generata dalla prova d'accettazione.

**Non ferma il secondo.** Il crash E365 (FINDINGS §6-quinquies, il `<params>`
di una clip audio troncato da 31 a 11 attributi con valori inventati) resta
invisibile a `verifica()` — misurato: su quel file restituisce `[]`, e
`avvertenze()` pure. Quel caso lo ferma un'altra cosa: la regola «mai
trascrivere a mano, le costanti si generano da codice» (regola 2 della skill)
più `test_audio_costanti`, che confronta la costante incorporata col nodo vero
attributo per attributo. Non si può allargare il cancello per coprirlo anche
lì: 109 delle 194 clip audio scritte dal dispositivo hanno esattamente 11
attributi nel loro `<params>` (11×109, 12×13, 14×1, 15×65, 16×2, 31×3, 32×1)
— un controllo di completezza accuserebbe 190 file su 194 sani, la stessa
trappola dei falsi positivi già costata due volte in questo progetto.

**`avvertenze()` è il livello che informa senza bloccare**: conflitti di
sezione, note oltre la fine della clip, note scritte fuori dalla finestra di
scroll della clip (`song.notes_hidden_by_scroll()`, il gemello di
`yScrollSongView` a livello di clip). Roba che il dispositivo carica ed
esegue male o non esegue — la famiglia di difetti che in questo progetto è
costata più di tutte.

### Cosa ha trovato la prova d'accettazione

Generare una song *come la genererebbe il Pal* ha scovato tre difetti che 424
test non vedevano, perché tutti partivano da materiale già esistente:

- **`add_track` su un kit creava una clip senza righe.** Nel corpus **393 clip
  di kit su 395** hanno una riga per *ogni* drum, suonato o no, con indici
  contigui da 0. Chi aggiungeva note otteneva indici sparsi, e il cancello
  rifiutava. Corretto; aggiunta `song.drum_row()` per scrivere su un drum per
  nome.
- **Non esisteva un modo di scrivere un accordo.** `melodia()` mette una nota
  per passo: `re3 fa3 la3` usciva in fila invece che insieme. Ora c'è
  `accordi()`.
- **Nessuno avvisava se una nota cadeva oltre la fine della clip.** Il Deluge
  carica e non la suona. Ora è un'avvertenza — e la soglia è stata *misurata*:
  un controllo ingenuo accusava 254 note in 22 file sani, che erano poliritmi
  (righe più lunghe della clip).

---

## 6-quater. Togliere — chiusa il 15 agosto, verificata sul dispositivo

Il ciclo è «l'utente ascolta e dice cosa cambiare», e **metà di quello che una
persona dice è sottrattivo**. Fino al 15 agosto *«rifai il basso»* funzionava e
*«togli il basso»* no: in tutta la libreria c'erano `kit.remove_drum` e
`Node.remove`, e nient'altro.

Due verbi in `musica.py`, entrambi con un rapporto di ritorno come
`applica_verbo`. Sotto stanno le primitive, testate una per una.

| per | funzione |
|---|---|
| togliere | `togli(doc, bersaglio, quando=None)` |
| scrivere note | `scrivi(doc, clip, note, dove=None)` |

`togli` riconosce il bersaglio **per identità** — appartenenza alla lista degli
strumenti o delle clip — non per tag: nel corpus convivono `<midi>` e
`<midiChannel>`, e una tabella di tag sarebbe una cosa in più da sbagliare.

    strumento                 le sue clip, poi lui
    strumento + quando=(a,b)  solo le istanze d'arranger in quel tratto
    clip                      la clip, e i clipCode che la seguivano
    noteRow di kit            SVUOTATA: una riga per drum deve esserci
    noteRow di synth          tolta

`quando` è la differenza fra *«togli il basso»* e *«leva il basso nella seconda
metà»*. Toglie le istanze **contenute** nel tratto, non quelle che lo
attraversano: una a cavallo porta anche materiale fuori, e toglierla farebbe
tacere musica che nessuno ha chiesto di togliere. Restano, e il rapporto le
dichiara.

`scrivi` chiude la vecchia lacuna 3. Non serve dichiarare se la clip è un kit o
un synth, perché **la forma delle note lo dice già**: `melodia()` e `accordi()`
tornano `altezza -> note`, `passi()` una lista sola. Su synth chiama sempre
`fit_clip_scroll_to_notes()` in coda. Le tre righe che `SKILL.md` insegnava
separate — e le tre occasioni di prendere quella sbagliata — sono una sola.

**Il numero che conta:** i riferimenti a una clip nel corpus sono **due**,
`clipCode` e `yScrollSongView`, e nessuno dei due la nomina — entrambi la
contano. Il censimento e le altre misure sono in `docs/FINDINGS.md` §6-sexies.

**Un difetto trovato progettando, non da un test:** `_keep_row_visible()` alza
soltanto lo scroll, quindi la rimozione poteva lasciare la vista *sopra* il
contenuto — il §3.1 in specchio, quinta volta della stessa famiglia. Reale: 11
song su 36 hanno `yScrollSongView` positivo, `Progsong.XML` vale 27 con 42
clip. Corretto da `_keep_view_within()`, che scende solo quel tanto e non
ri-ancora in fondo.

---

## 6-quinquies. Trasformare — chiusa il 16 agosto, verificata sul dispositivo

*«Alza il basso di un'ottava»* è una richiesta ordinaria quanto *«più scuro»*,
e fino al 16 agosto voleva una funzione che non c'era.

Le cinque parole della lacuna — trasponi, raddoppia, dimezza, sposta, più
veloce — non erano cinque operazioni: tre di esse ne volevano dire due ciascuna.
Sciolte in sei nomi non ambigui:

| per | funzione |
|---|---|
| trasporre | `trasponi(doc, bersaglio, semitoni=…)` oppure `gradi=…` |
| spostare nel tempo | `sposta(doc, clip, tick=…)` oppure `battute=…` |
| allungare ripetendo | `repeat(doc, clip, volte)` |
| cambiare il rate | `stretch(doc, clip, fattore)` |
| l'articolazione al doppio | `double_time(doc, clip)` — la battuta **resta** |
| l'articolazione a metà | `half_time(doc, clip)` — la clip **raddoppia** |

L'asimmetria fra gli ultimi due è voluta: in metà tempo un pattern di una
battuta ne occupa due davvero, mentre in doppio tempo lo si suona due volte per
riempire la battuta.

**Trasporre non è la stessa operazione su un synth e su un kit.** Su un synth
le righe *sono* le altezze e si cambia `y`. Su un kit si intona il **suono** —
`transpose` sugli oscillatori del drum, confermato dal manuale e verificato sul
dispositivo — quindi cambia lo strumento e con lui *tutte* le clip di quel kit.
I `drumIndex` non si toccano mai. Dettagli e numeri in `docs/FINDINGS.md`
§6-septies.

**Il modo diatonico conserva lo scarto cromatico dal grado**, invece di
schiacciare in scala: una nota un semitono sopra il terzo grado resta un
semitono sopra il *nuovo* terzo grado. `snap_to_scale()` qui sarebbe sbagliata,
e distruggerebbe le 315 note fuori scala di `Progsong.XML` che FINDINGS §6 dice
espressamente di rispettare.

**E non è biiettivo**, a differenza del cromatico: in re minore mib2 e mi2
salgono entrambi su fa2. `song.retune_rows()` fonde le righe che collidono e lo
dichiara.

**La riga MIDI di un kit, e un'ipotesi demolita.** Il progetto aveva
implementato una supposizione — un `<sound>` col suo `<midiOutput>` figlio
attivo, altezza in `noteForDrum` — ed era sbagliata su entrambi i punti. La
forma vera è un `<midiOutput>` **fratello** dei `<sound>` dentro
`<soundSources>`, con l'altezza in **`note`**. È emersa solo facendo salvare al
dispositivo un kit con una riga MIDI (`refs/songs/TRASF401MIDI.XML`).

La lezione di metodo vale più della correzione: il ragionamento di allora era
«`noteForDrum` è un attributo *osservato*, quindi non sto inventando una
struttura». Vero, e insufficiente — **un nome osservato nel posto sbagliato è
comunque il posto sbagliato.** «Non sto inventando» non è «ho visto».

---

## 6-sexies. La finestra di clip view — chiusa il 16 agosto

Era l'ultima lacuna, e la più piccola sulla carta: «l'avvertenza sulle note
invisibili non copre le clip in modalità a scala». Ne è uscita **una geometria
sola per tutto il dispositivo**:

    riga sullo schermo = valore − yScroll        otto righe, 0-7

con l'unità che cambia col tipo di clip — il **semitono** in cromatico, il
**grado** in scala, la **posizione della riga** in un kit. Tre coppie
controllate, una per unità: `SCALA0/1`, `SCALB0/1`, `KITSCR0/1`, tutte in
`refs/songs/`. La conversione vive in `song.clip_rows_with_notes()`, e sia il
`fit` sia l'avvertenza ci passano — non c'è più nessun ramo speciale.

`fit_clip_scroll_to_notes()` **ancora** la riga più bassa alla prima riga dello
schermo, sempre. Non «lascia stare se qualcosa si vede»: quella è la regola di
song view, dove si conserva la vista dell'utente, e presa in prestito qui
lasciava la nota più alta fuori dallo schermo.

⚠️ **Quattro modelli sbagliati di fila, e nessun test li ha visti**, perché
erano tutti verdi asserendo il modello sbagliato. Sono emersi solo guardando lo
schermo del Deluge, dopo che erano stati dichiarati «verificati sul
dispositivo» avendo **ascoltato** invece che guardato — la riproduzione non
dipende dallo scroll, quindi suonavano giusti. Il racconto per esteso è in
`docs/FINDINGS.md` §6-octies e vale più della conclusione.

---

## 6-septies. Il primo pezzo vero — 16 agosto, e cosa ha insegnato

Il consiglio dell'handoff precedente era «usarlo, e vedere cosa manca
davvero». Ha funzionato: **un solo pezzo ha trovato più buchi di una revisione
a tavolino**, e li ha trovati in due strati diversi.

Il brief: dub elettronico lento, strumenti costruiti da zero, kit
**sintetizzato** e non a campioni, basso wobble, pad, sirena, uso creativo di
delay e filtri con automazioni.

### Strato 1: cosa mancava alla libreria

Tre lacune, tutte bloccanti per quel brief, tutte chiuse:

| mancava | perché bloccava | ora |
|---|---|---|
| **i patch cable** | senza, niente wobble (`lfo1 → lpfFrequency`) e niente sirena (`lfo1 → pitch`): sono patch cable e nient'altro | `sound.set_patch_cable / patch_cables / remove_patch_cable` |
| **i modulatori FM** | il synth vuoto è subtractive e non ha `<modulator1/2>`, presenti in **80 suoni FM su 80** del corpus | `structure.set_synth_mode(inst, 'fm')` li crea |
| **`defaultParams` fra i contenitori** | `sound.container()` su un drum tornava `None`: impossibile progettare il suono di una percussione | aggiunto in fondo a `CONTENITORI` |

Più una quarta trovata dopo, dall'ascolto: **`passi()` aveva due soli livelli
di velocity**, e con due livelli un colpo fantasma è inesprimibile. Ora `o` è
il fantasma (42 su 127).

⚠️ **Trappola del modulo `sound.py`**: definisce di proposito una funzione
`set()` che **oscura il builtin**. Usare `set()` lì dentro dà un `TypeError`
che sembra venire da tutt'altra parte. Deduplicare con un dict.

### Strato 2: cosa mancava a me

Il giudizio dell'utente sul primo tentativo: *«molto elementare e non
assomiglia per niente a un pezzo dub»*, e poi *«anche il ritmo di batteria è
penoso»*. Aveva ragione, e la causa era una sola: **avevo fatto una ricerca web
sola**, e ne erano uscite le etichette invece del mestiere.

Gli errori concreti, tutti dallo stesso buco:

| errore | cos'era giusto |
|---|---|
| charleston sui levare, **skank assente** | il charleston fa una timeline regolare; il levare è dello *skank*, che è **armonia** |
| niente *bubble* d'organo | riempie i sedicesimi attorno al levare |
| basso di 4 battute che si sviluppa | frase di **1-2 battute ripetuta**, centrata sul 3, con la quinta **sotto** la tonica |
| 4 battute di batteria identiche | **turnaround** sull'ultima di ogni 4 o 8 |
| `set_swing(50)`, dritto | il one drop è **swingato e laid-back** |
| pad a note lunghe come parte armonica | in reggae l'armonia è **ritmica**, staccata, in levare |

Tutto questo è ora nella scheda `docs/repertori/reggae-dub.md`, con le
griglie a 16 passi, i numeri delle velocity e le fonti.

### E una correzione di sound design che vale in generale

La sirena di `DUBPAL01` *«bucava le orecchie»* **pur rispettando** la soglia
che avevo scritto io (risonanza sotto 24). La soglia era sbagliata come
concetto: le ladder del Deluge **autooscillano**, e quanto sia "alto" dipende
dal registro e da cosa c'è intorno — lì il delay feedback che saliva a 33 e il
riverbero a 34 **ripetevano e accumulavano** il picco risonante.

Il rimedio, detto dall'utente: **se vuoi una risonanza estrema, la paghi
abbassando il volume della patch.** La risonanza gonfia una banda stretta, e
quello che esplode è il livello percepito, non il timbro.

> Nota di metodo, ripetuta due volte in un giorno: `DUBPAL02` è stata corretta
> partendo dalla song **riscaricata dal dispositivo**, non dalla copia locale —
> e infatti portava il volume a 29 invece dei 17 che avevo messo io. La regola 1
> non è formale: senza, quella correzione sarebbe stata cancellata.

---

## 6-octies. Le sigle di accordo — 17 agosto 2026

Primo passo del perimetro nuovo, e non è un lettore di file: è **il posto dove
i lettori atterreranno**. `wjazzd.db`, MusicXML e kern producono tutti e tre
armonia; costruirli prima avrebbe voluto dire tre rappresentazioni diverse da
riconciliare dopo.

**La lacuna era un concetto, non un formato.** `MU.accordi()` vuole le altezze
già scelte (`'do3 mi3 sol3'`): in tutta la libreria non esisteva la nozione di
*simbolo*. Per il reggae non si notava — lì l'armonia sono due accordi e il
mestiere sta nel ritmo. Per il jazz è l'opposto.

| per | funzione |
|---|---|
| una progressione per sigla | `MU.armonia('Dm7 \| G7alt \| Cmaj7', voicing=…, registro=…)` |
| le altezze di un accordo solo | `MU.voci('Cmaj7', voicing='drop2', registro='do4')` |
| sciogliere una sigla senza suonarla | `MU.sigla('C6/9/E')` |
| **raccontare cosa ha deciso** | `MU.racconta_armonia(…)` |

`armonia()` ha **la stessa forma di ritorno di `accordi()`** — `altezza →
note` — quindi entra in `MU.scrivi()` senza che nulla a valle sappia da dove
viene. Era il vincolo di progetto principale: atterrare nella macchina che
esiste, non chiederne una nuova.

**Da dove vengono i numeri, e perché conta.** Le sigle e le ambiguità da
`assets/chord-symbol-ambiguity-and-parsing.md`, i voicing da
`assets/jazz-voicings.md` — cioè dalla skill, non da me. E **i test portano i
valori attesi di quei documenti**: il drop 2 di domaj7 (`sol-do-mi-si`), il
senza-fondamentale di re-7 (`fa-la-do-mi`) e di domaj7 (`mi-sol-si-re`), il
`C7#11` senza la quinta (`mi-sib-re-fa#`). È la coppia controllata applicata a
un dominio non misurabile sul dispositivo: **il valore atteso deve venire da
fuori**, o il test conferma solo il modello che avevo in testa — che è
esattamente come sono nati i quattro modelli sbagliati del 16 agosto.

Tre cose che il progetto ha già pagato altrove, e qui sono state prevenute:

- **il maiuscolo conta**: `CM7` è maj7, `Cm7` è minore. La coda si normalizza
  guardando il caso *prima* di abbassarlo — è lo stesso difetto muto di
  `'Ab'` → A# in `set_scale`, dove un semitono sbagliato non dava errore.
- **la fondamentale riusa `altezza()`**, quindi italiano e inglese non possono
  divergere. Un secondo parser di altezze è una seconda occasione di sbagliare.
- **una sigla sconosciuta viene rifiutata** e l'errore elenca quelle che
  esistono, invece di indovinare note che nessuno ha chiesto.

⚠️ **Il limite, dichiarato e non nascosto: non c'è condotta delle parti.** Ogni
accordo è costruito per conto suo. Il documento mostra che nel ii-V-I i
voicing senza fondamentale si **alternano** fra due forme (A e B) proprio per
muovere una voce sola per cambio: le note qui sono giuste, il *collegamento*
no. `racconta_armonia()` lo dichiara a ogni chiamata.

**E un difetto trovato provando a mano dopo che i test erano verdi**, che vale
come promemoria: `C6/9/E` ha due slash con due significati diversi — l'ultimo
è il basso, quello dentro `6/9` è parte della sigla. I dieci test erano tutti
verdi e non lo vedevano. È la quinta volta in questo progetto che il difetto
sta in un caso che nessun test aveva pensato di scrivere.

---

## 6-nonies. Il lettore della Weimar Jazz Database — 17 agosto 2026

Secondo passo del perimetro nuovo, e il primo lettore vero.
`tools/delugexml/wjazz.py`, solo `sqlite3` della stdlib — nessuna dipendenza,
come `midi.py` che si era scritto il lettore di SMF invece di tirarsi dentro
`mido`.

| per | funzione |
|---|---|
| cercare | `WJ.elenco(db, style=…, rhythmfeel=…, instrument=…)`, `WJ.valori(db, campo)` |
| vedere | `WJ.racconta(db, melid)` |
| le note | `WJ.melodia(db, melid)` → `(altezza → note, Conversione)` |
| la griglia | `WJ.armonia(db, melid)` → `Accordo(tick, bar, beat, testo, sigla)` |
| il dialetto | `WJ.sigla_weimar(testo)` |

`melodia()` e `armonia()` hanno le forme che il progetto usa già, e
`armonia()` restituisce `MU.Sigla` **sciolte** — cioè atterrano in
`MU.armonia()` e in `MU.scrivi()`. Era il motivo per cui §6-octies veniva
prima.

### Il dialetto, e la misura che ha guidato il progetto

Il 22% delle 30 548 occorrenze di accordo **non era leggibile** da
`MU.sigla()`, e i fallimenti erano tutti sistematici: `j7` per maj7,
l'alterazione **dopo** il grado (`79b` = 7♭9), `o` per il diminuito, `sus7`
per 7sus4, `NC` per nessun accordo.

⚠️ **La verifica che contava non era quel 22%, ma l'altro 78%.** Un simbolo
che si legge non è un simbolo che si legge *giusto*, e un falso positivo lì
sarebbe stato muto. Misurato una per una: le code comuni ai due dialetti —
`7`, `-7`, `-`, `6`, `-6`, `sus`, `m7b5`, `69`, `+`, `7alt` — vogliono dire
la stessa cosa. **È quella misura che ha deciso l'architettura**:
`sigla_weimar()` prova prima la lettura canonica e scende alla grammatica di
Weimar solo quando fallisce, invece di riscrivere una grammatica che esiste.

Copertura finale: **419 simboli distinti su 419, zero fallimenti**; le 401
caselle `NC` tornano `None`.

**Il dialetto sta in `wjazz.py`, non in `MU.SIGLE`.** `SIGLE` è la notazione
da lead sheet, comune a tutte le fonti; le abitudini di un database solo,
messe lì, la sporcherebbero per sempre. Vale come regola per i lettori che
verranno.

### Cosa è annotato e cosa no

La tabella `melody` porta **la posizione metrica** (`bar/beat/tatum/division`)
**accanto** al tempo reale (`onset` in secondi). Quindi la metrica non va
dedotta: è scritta. E **la differenza fra le due è la micro-tempistica**, che
è il motivo per cui questo database vale più di una raccolta di MIDI.

**Lo swing misurato è arrivato subito dopo**, il 17 agosto: `WJ.swing()`, e i
primi numeri `[MIS]` del progetto. Vedi §6-decies.

⚠️ `division` vale 5 o 10 per 7242 note su 200 809 (il 3,6%) e 96 non si
divide per 5: quelle si arrotondano, e `Conversione` lo dichiara.

### Un difetto trovato dai test, che vale come promemoria

La prima versione estraeva la fondamentale con `MU.sigla()`. Ma `MU.sigla()`
è un parser di **accordi interi**: su `C7` restituiva la fondamentale *e si
mangiava la settima*, lasciando una triade. Quindici test rossi in una volta.

È la stessa famiglia di «un nome osservato nel posto sbagliato è comunque il
posto sbagliato»: la funzione era quella giusta per il vocabolario delle
altezze e quella sbagliata per estrarre un prefisso.

**Il materiale che resta in `to-read/MIDI/`**, ora che il primo è aperto:
`groove-v1.0.0-midionly/` — non uno zip da decomprimere, è già una cartella
decompressa; il suo `groove/info.csv` etichetta ogni file con stile e BPM, e
**quante esecuzioni porti a ciascun repertorio sta nella casella 6 della sua
scheda** — il jazz in `docs/repertori/jazz.md`, il reggae in
`docs/repertori/reggae-dub.md` — perché è lì che quel conteggio serve a
decidere se il numero è `[MIS]` o `[WEB]`, e per i due repertori ha deciso in
modo opposto (§6-terdecies). Dal 18 agosto quel dataset si legge con
`groove.py` e non a mano. Poi restano `POP909`, `maestro`,
`The_Magic_of_MIDI`, le librerie per genere e `(aq) Dub Beat Builder`.

---

## 6-decies. Lo swing misurato — 17 agosto 2026

`WJ.swing(db, style=…, rhythmfeel=…, tempo_min=…, tempo_max=…)`. Su **333
assoli e 27 943 coppie di crome**: levare al **61,7%** del movimento, cioè
**BUR 1,61**. Tabelle per stile, feel e tempo in `docs/repertori/jazz.md`,
«Lo swing del jazz, MISURATO», nella casella 4 — sono i primi numeri `[MIS]`
del progetto, contro i `[WEB]` di tutto il resto della pagina.

Il risultato in una riga: **il jazz non swinga in terzine.** Sta fra il dritto
e la terzina, HARDBOP e BEBOP in cima (1,80 e 1,75), FUSION in fondo (1,26), e
lo swing **cala al salire del tempo** — 1,89 fra 120 e 180 BPM, 1,35 sopra i
240.

### L'errore, che vale più del risultato

⚠️ **Tre tentativi hanno dato 1,10, 1,19 e 1,10 e sembravano confermarsi a
vicenda. Erano lo stesso errore tre volte.**

La posizione **annotata** (`tatum`/`division`) **contiene già lo swing**: i
trascrittori scrivono una coppia di crome swingate come *tatum 1 e 3 di
division 3*. Quindi selezionare le crome con `division == 2` — che sembra la
cosa ovvia — seleziona le sole coppie giudicate **dritte**, e la misura torna
1,0 per costruzione. Non un errore di calcolo: di **selezione**.

Due cose l'hanno smascherato, e nessuna delle due era un test:

1. **Un controllo esterno.** La letteratura dice che lo swing cala col tempo e
   che i generi a crome dritte stanno sotto. Nessuna delle due previsioni
   compariva. *Una misura che non riproduce una previsione nota è sbagliata
   anche quando è ripetibile* — e ripetibile lo era, tre volte.
2. **Guardare le righe grezze** di un assolo lento, e vedere `tatum=1/3`.

È la stessa famiglia dei quattro modelli sbagliati del 16 agosto: test verdi
che asserivano il modello che avevo in testa. Qui però i test non c'entrano
nemmeno — il codice faceva esattamente quel che dicevo io, ed era la domanda
a essere posta male.

### Cosa NON è verificato

- **Il valore assoluto non è riconciliato con la letteratura.** «Playing It
  Straight» riporta ~1,3 sullo **stesso** database, qui viene 1,61. Il metodo
  di quel lavoro è dietro un paywall, quindi la differenza resta non spiegata
  e i valori assoluti sono provvisori. Le *differenze* fra sottoinsiemi sono
  invece nella direzione pubblicata.
- ~~La mappatura su `set_swing()` è ignota~~ — **chiusa il 17 agosto 2026,
  sul dispositivo. Vedi §6-undecies.** Il display *è* la percentuale di
  posizione del levare, e serviva anche una seconda cosa che non avevo
  previsto: `swingInterval`, cioè **su quale figura** lo swing agisce.
- **Sotto i 120 BPM la misura guarda probabilmente il livello metrico
  sbagliato**: nelle ballad lo swing si sposta sulle semicrome. `[OSS]`

---

## 6-undecies. Lo swing sul dispositivo, e due errori — 17 agosto 2026

Sessione col Deluge collegato, per chiudere la mappatura di `set_swing()`.
Chiusa, ma è costata due errori miei — uno dei quali ha bloccato la macchina.

### Cosa si scrive, adesso

```python
S.set_swing(doc, 62, figura='1/8')     # il jazz misurato, sulle CROME
```

Servono **due** cose, e ignorarne una rende inutile l'altra:

1. **Quanto** — il display *è* la percentuale di posizione del levare.
   Derivato dal sorgente: `BUR = display / (100 − display)`, quindi 50 dritto,
   67 terzina, e sotto 50 il levare arriva in anticipo.
2. **Su quale figura** — `swingInterval`, misurato con cinque salvataggi:
   `4`=1/2, `5`=1/4, **`6`=1/8**, `7`=1/16, `8`=1/32. L'etichetta sullo
   schermo nomina la figura swingata, senza traduzioni.

⚠️ **Il default del firmware è `7`, le semicrome — e vale in 146 song su 146
del corpus.** Lo swing di song è sempre stato applicato alle semicrome: su
una linea di crome non poteva sentirsi, e non perché il valore fosse basso.
Per il jazz serve `figura='1/8'`.

### Errore 1: `isPlaying`, e un Deluge bloccato

Una song generata senza `playing=True` esce con la clip a `isPlaying="0"`. Se
è l'unica clip, il dispositivo **si blocca premendo play**. Il file passava
`verifica()`, `avvertenze()`, `check_clip_types()`, il round-trip e la
decodifica delle note: formalmente perfetto e inservibile.

Famiglia di `yScrollSongView`, con variante nuova: lì lo stato sbagliato era
di **vista**, qui di **lancio**. Ora lo segnala `song.no_playing_clip()` in
`avvertenze()` — informa e non blocca, perché **10 song su 146** del corpus
sono legittimamente in quello stato (salvate da ferme).

⚠️ **E la mia bisezione era viziata.** La variante «tengo il vecchio
strumento» avrebbe funzionato, ma non per il fattore che testava: quel
vecchio strumento si porta dietro una clip con `isPlaying="1"`. Cambiava due
cose insieme, e mi avrebbe fatto concludere «contano i due strumenti». A
trovare il difetto vero è stato il confronto con un file che **suona**
(`BASSO.XML`).

### Errore 2: misurato giusto, dedotto sbagliato

La tabella di `swingInterval` era uscita **spostata di un posto** (intervallo
5 per le crome). L'osservazione a cinque punti — etichetta ↔ numero nel file —
era giusta; sopra ci avevo sovrapposto l'aritmetica del sorgente
`3 << (10 − swingInterval)`, che dà un blocco lungo **la metà** di quello
vero. Ne era uscita la conclusione controintuitiva «l'etichetta nomina il
blocco, non la figura», e l'avevo pure difesa.

L'ha smontata l'utente ascoltando: *«con 8th sento il primo ottavo dritto e il
secondo swingato»* — una frase che descrive la **coppia**, e la coppia è fatta
della figura nominata.

> **Avevo misurato la cosa giusta e dedotto quella sbagliata.** La misura
> copriva solo «etichetta ↔ numero»; il significato musicale era **inferito**,
> e l'ho trattato come se pesasse quanto la misura. È una variante nuova
> dell'errore di sempre: non «dedurre dal file invece che dal dispositivo», ma
> **appoggiare una deduzione su una misura vera e spacciare il tutto per
> misurato**.

Lo scarto col sorgente resta **ignoto** ed è dichiarato in
`song.SWING_SCARTO_SORGENTE`: i "swung tick" di quel codice non sono i tick
delle posizioni di nota, e dove si convertano non è stato trovato. Dichiararlo
è meglio che aggiustarlo a posteriori.

### File lasciati sulla SD

In `/SONGS/DelugePal/`: `SWTEST01`-`SWTEST05` (la bisezione di `isPlaying`),
`SWDIV01`-`SWDIV04` (le quattro posizioni dell'intervallo, **salvate dal
dispositivo**: sono la prova, non ripulirle), `SWJAZZ01` (sbagliata,
intervallo 5) e `SWJAZZ02` (giusta). Le prime e `SWJAZZ01` si possono
togliere; le `SWDIV` no.

---

## 6-duodecies. La rifondazione di `MUSICA.md` — 17-18 agosto 2026

Chiude il punto lasciato aperto dalla sessione dello swing: *«`MUSICA.md` è
ancora a forma di batteria reggae»*. Il documento era cresciuto attorno a un
solo genere e non reggeva il perimetro vero — jazz, classica, barocca, antica,
contemporanei.

**Lo schema neutro sono undici caselle formulate come domande**, scelte col
criterio che dovessero sopravvivere **sia a Josquin sia alla jungle**:

    1 Cos'è, e cosa non è      5 Ruoli e spartizione      9 Forma e densità
    2 Metro e griglia          6 Dinamica                10 Sul Deluge
    3 Tempo                    7 Armonia                 11 Trappole del generatore
    4 Feel                     8 Melodia e ornamentazione

`MUSICA.md` tiene lo schema, il **comune** e l'**indice**; ogni repertorio è
una scheda in `docs/repertori/`. Si legge il comune più **la sola scheda che
serve**, mai tutte.

**Il guadagno non è l'ordine, è la collisione.** A documento organizzato per
genere, l'*inégalité* barocca e lo swing del jazz non si sfiorerebbero mai — e
sono la stessa domanda, dove cade il levare dentro il movimento, fatta a due
repertori. Lo schema le mette nella stessa casella 4.

### Due invarianti che un test tiene in piedi

Le undici caselle esistono e sono in ordine in ogni scheda; e **l'indice
coincide con lo stato che ogni scheda dichiara di sé**. Lo stato si legge dalla
**prima riga non vuota** di ogni casella: `**Vuota.**` (o `**Vuota, …**`),
`**Parziale.**` esatto, qualunque altra cosa = piena. Provato rompendolo: il
test diventa rosso e nomina la casella. **La scheda è la fonte, l'indice ne è
la vista** — quando divergono è l'indice a sbagliare.

### La riga «nel frattempo», e perché è il pezzo che conta

Una casella vuota dichiara *cosa servirebbe* per riempirla, ed è ciò che rende
l'indice un'agenda. Ma chi apre i file per comporre **stasera** non ha un corpus
da leggere: ha un pezzo da scrivere, e una casella che dice solo «servirebbe
MusicXML» **lo lascia libero di inventare**. Ogni casella non piena porta quindi
una riga che dice dove prendere la risposta provvisoria e con che fiducia —
chiedere a una skill (nominando il file e segnando `[WEB]`), chiedere
all'utente, **lasciare la parte fuori**, o prendere ciò che dà una casella
sorella.

⚠️ **Una riga «nel frattempo» che prescrive ciò che la libreria non sa fare è
peggio di nessuna riga.** È successo in revisione: quella della casella 7 del
jazz mandava a realizzare l'alternanza A/B dei voicing del ii-V-I, che è giusta
musicalmente ed è scritta nella skill — ma `MU.VOICING` ha **una sola** forma
senza fondamentale e `voci()` ordina sempre dal basso, quindi la "B" non è
raggiungibile. Chi la seguiva sceglieva un voicing qualunque, lo chiamava B, e
**inventava con la benedizione della riga scritta per impedirlo.** Ora manda
alle altezze a mano con `MU.accordi()` e nomina la strada da non prendere.

### Il cancello, e cosa è costato davvero

La regola della migrazione era **le frasi si spostano come sono**: il contenuto
era stato corretto due volte dall'ascolto dell'utente, e riformularlo avrebbe
perso proprio le correzioni. Delle 745 righe smontate, **una sola era contenuto
vero perduto** — la regola *«ogni volta che una proposta viene corretta, la
lezione va qui, con la data»*, che sciogliendo il registro era rimasta
**dimostrata in quattro blocchi ma non più prescritta**. Rimessa.

L'istruttoria completa, riga per riga, è in
`docs/superpowers/2026-08-17-musica-cancello-migrazione.md`, conservata apposta:
è l'unica prova che smontando il documento non si è perso niente.

**Tre cose di metodo che valgono oltre questo lavoro:**

- **assemblare un file estraendo intervalli di righe invece di ribatterle rende
  la letteralità *misurabile*** invece che dichiarata. È così che una revisione
  ha potuto verificare «quattordici diff di sola inserzione, zero righe
  riscritte» invece di crederci;
- **quella regola protegge il contenuto, non le coordinate della vecchia
  impaginazione.** «In fondo alla sezione», «più sopra» sono indirizzi: se
  diventano falsi si correggono, ed è un difetto che la regola non era fatta per
  conservare;
- **uno snippet può essere una prova, non un esempio.** Nella casella 10 del
  reggae resta `S.set_swing(doc, 57)` **senza `figura=`**, cioè inerte: non è
  stato corretto perché la casella 4 dice «*fu scritto senza*», e aggiustarlo
  renderebbe falsa quella frase. La cautela sta nella prosa.

⚠️ **Una trappola di Markdown da conoscere prima di scrivere queste schede:**
una riga che comincia con `>` e uno spazio apre una **citazione** in CommonMark,
e le righe successive ci entrano dentro come continuazione. Un confronto come
«oltre 240 BPM» scritto col segno di maggiore e mandato a capo all'inizio di una
riga si mangia mezza casella, e si vede solo a pagina resa.

### Il Groove MIDI: la versione giusta è quella che c'è

`info.csv` ha una colonna `audio_filename` popolata su 1090 righe su 1150:
**la differenza fra midionly e versione completa è l'audio delle esecuzioni**,
non un formato diverso. Per la casella 6 — velocity e microtiming — **il MIDI è
completo e l'audio non aggiunge niente**: porta nota, velocity e l'onset esatto
di ogni colpo, e il microtiming *è* lo scarto di quegli onset dalla griglia.

L'audio servirebbe per **un'altra cosa**: il **break tagliato** di jungle e DnB,
che vive in `audio.py` — un'esecuzione a kit intero *è* un break, e siccome il
MIDI dà l'onset esatto di ogni colpo i tagli si farebbero **su posizioni note**
invece che per rilevamento dei transienti. Per cavarne colpi singoli puliti
invece serve poco: è una ripresa a kit intero, quindi un rullante estratto porta
dentro il charleston. Jungle e DnB stanno in fondo alle priorità: **non
riscaricare niente adesso.**

### Gli archivi non vanno decompressi

`zipfile`, `tarfile` e `gzip` sono **stdlib**, quindi rientrano nella regola di
non aggiungere dipendenze: si elencano e si leggono i membri di un archivio
senza estrarre nulla. Provato su `POP909.zip` — 2898 MIDI elencati, uno letto in
memoria e dato a `midi.py`, che ha risposto col suo rapporto di conversione.

L'unico attrito: `MI.leggi()` vuole un **percorso**, quindi il membro va
appoggiato in un file temporaneo. Si toglie in tre righe — `leggi()` fa già
`Path(path).read_bytes()` al suo interno, basta affiancargli un `leggi_bytes()`.
**Non fatto**, è un'offerta rimasta aperta.

### Cosa NON rifare, e i residui dichiarati

- **non ricopiare un numero in due file.** Il vincolo è che un numero vive dove
  serve a prendere una decisione musicale; altrove è un rimando. È stato violato
  e corretto tre volte in questo lavoro;
- **non fidarsi di cosa contiene una skill senza aprirla.** `music-composition`
  non ha *niente* su ska, rocksteady e dancehall — zero occorrenze in 106 file —
  e **non ha una sezione POSTBOP**, che è lo stile più numeroso della misura
  dello swing. Le righe «nel frattempo» del reggae non ci mandano apposta;
- tre residui piccoli e dichiarati: la casella 10 del reggae letta **da sola**
  mostra ancora lo snippet inerte (di proposito, vedi sopra); il corpo della
  casella 8 del reggae usa il nome corto `(aq) Dub Beat Builder` mentre sul disco
  è `(aq) Dub Beat Builder - Demo`; e il contorno del Groove MIDI (percorso,
  data, avvertenza sul `.gitignore`) compare in entrambe le schede — il *numero*
  no, ed è il contorno a rendere ogni scheda leggibile da sola.

---

## 6-terdecies. Il Groove MIDI e il groove template — 18-25 agosto 2026

Chiude la casella **6 del jazz**, che era vuota, e costruisce la cosa che
`SKILL.md` nominava da sempre senza che nessuno l'avesse mai fatta: il **groove
template**, cioè la velocity e la micro-tempistica di un batterista vero posate
su un pattern scritto da noi.

⚠️ **È l'unico lavoro di questo progetto il cui risultato non è una funzione
che passa i test ma un'affermazione sul mondo.** *«Il charleston a pedale
anticipa il ride»* non è vera o falsa per come gira il codice, e **nessun test
verde può dirne il segno**. È la ragione per cui questa sezione racconta gli
errori quanto i risultati, e per cui un task solo — quello che scrive i numeri
nella scheda — è costato **cinque giri di correzione**.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `tools/delugexml/groove.py` | il **lettore del Groove MIDI Dataset**: 1150 esecuzioni di batteria di dieci batteristi, ognuna etichettata per stile, BPM, metro e `beat_type`. Riceve la radice del dataset come argomento — esattamente come `wjazz.py` riceve il percorso del `.db` — e **non tocca mai un `Document`**: è quello il confine, non l'elenco degli import. Riusa `MI.leggi()` e `MI.GM_PERCUSSIONI` invece di farsi un secondo vocabolario di percussioni. `elenco`, `valori`, `racconta`, `scala`, `profilo`, più `per_prefisso`, `origine`, `levare_da_posizioni`, `bur_da_posizioni` |
| `MU.applica_groove(note, prof, dove=…)` | **il verbo che posa il template** su ciò che esce da `MU.passi()`. Sta in `musica.py` e non in `groove.py` per lo stesso confine: `GR` legge, `MU` scrive. **Muta la lista** — è l'unica del modulo a farlo, mentre `passi()`, `melodia()`, `accordi()` e `armonia()` costruiscono e ritornano — e il docstring lo dichiara in cima, perché in un commento interno era invisibile a `help()` |
| `MU.in_bur()` / `MU.da_bur()` | l'aritmetica del BUR, **promossa** da `wjazz.py` al vocabolario comune. Serviva a due lettori di corpora diversi: duplicarla era vietato e far dipendere un lettore dall'altro assurdo. Primo compito del piano proprio perché tocca codice che funziona, quando i test esistenti possono ancora dire se si è rotto |
| `tools/misura_groove.py` | lo **strumento di misura** da cui escono i numeri delle schede: si esegue, si legge, i numeri si scrivono a mano col loro marcatore. Ogni sezione stampa **quante esecuzioni e quanti batteristi** la sostengono — non è rendicontazione, è il numero che decide fra `[MIS]` e `[OSS]` |
| `tools/genera_groove.py`, `tools/genera_swing.py` | i due generatori di **coppia controllata**: `GROOVE0`/`GROOVE1` per il cancello sul dispositivo, `SWINGA`/`SWINGB` per l'astrazione dello swing |
| `docs/repertori/jazz.md` | le caselle **4** (un secondo BUR, su un altro corpus e con un altro metodo), **6** (**da vuota a piena**), **9** (**da vuota a parziale**: i fill sì, la forma no) e **10** (come si scrive un template, e il giro sul dispositivo) |

⚠️ **`to-read/` è in `.gitignore`.** Chi clona non trova né il dataset né il
modo di rifare i conteggi: ogni numero di quelle caselle è **lo stato del disco
del giorno in cui è stato misurato**, e le schede lo dicono accanto ai numeri
invece di lasciarlo supporre.

### Il groove template: cos'è, e soprattutto cosa NON porta

Tre decisioni di progetto, e ognuna chiude un modo di sbagliare che il resto
del documento ha già pagato altrove.

**Viene da UNA esecuzione nominata, non da una media.** `GR.profilo(base, id)`
legge un solo file — `drummer1/session3/2`, cioè batterista, stile, BPM e
durata dichiarati ogni volta che se ne cita un numero. Mediare il microtiming
di batteristi diversi lo tira verso zero, cioè **verso la griglia**: si
perderebbe esattamente ciò che si era andati a prendere. Ne segue che un
profilo è `[OSS]` **su un esecutore**, mentre la scala di velocity di
`GR.scala()` è `[MIS]` **sull'aggregato** — due marcatori diversi perché sono
due affermazioni diverse, ed è il motivo per cui `scala()` restituisce
`esecuzioni` e `batteristi` accanto a ogni mediana invece della sola mediana.

**Porta solo il residuo: lo swing lo fa la song.** Se il template portasse
anche lo swing, e `S.set_swing(doc, 62, figura='1/8')` è **di song** e vale per
basso e comping insieme alla batteria, lo swing finirebbe applicato due volte.
Quindi `profilo()` misura il BUR dell'esecuzione e **lo toglie**; quello che
resta — di quanto ogni strumento arriva prima o dopo il resto del kit — è il
template. E quel BUR tolto non è materiale di scarto: è il **controllo
indipendente** sull'1,61 misurato sulla Weimar (§6-decies). Due corpora, due
metodi, due strumenti — la linea solista trascritta contro un kit intero — e le
mediane cadono a due punti di levare di distanza: **59,7% contro 61,7%**, cioè
BUR 1,48 contro 1,61, su 41 esecuzioni e 5 batteristi. La casella 4 le porta
tutt'e due, coi rispettivi metodi, e dice che **la delimitazione decide il
numero**: dalla stessa etichetta `jazz` escono 1,26 o 1,60 a seconda di cosa ci
si include.

**Non inventa.** Se il pattern chiede un colpo su un passo dove quel batterista
non ha mai suonato, `applica_groove()` **lascia la nota com'è** e mette il
passo in `senza_appoggio`, che va letto. È lo stesso cancello della sigla
sconosciuta in `MU.armonia()`, e per la stessa ragione: un template che si
riempie i buchi da sé sarebbe di nuovo **inventare con la benedizione della
riga scritta per impedirlo**, che è il difetto raccontato in §6-duodecies a
proposito delle righe «nel frattempo».

⚠️ **E una trappola che il nome nasconde: il nome GM non è il ruolo musicale.**
Su `drummer1/session3/2` il disegno continuo di crome swingate — il ride,
musicalmente — sta per otto decimi dell'esecuzione sulla nota **43**, che la
mappa GM chiama `tom basso` (805 colpi), e solo nel quinto centrale sulla nota
**51**, `ride` (238 colpi). Chi scrive `dove='ride'` prende il profilo di un
quinto di esecuzione. **La voce si sceglie dal numero di colpi e dalla
posizione** che `GR.profilo()` riferisce, mai dal nome.

### Cosa è verificato sul dispositivo, e cosa è stato ascoltato

Sono due affermazioni diverse e stanno in due caselle diverse, ed è la regola
della §8 applicata a un caso in cui era facilissimo confonderle.

**Quello che si VEDE, ed è meccanico.** `GROOVE1` — 31 note su quattro righe,
con scarti da **−6 a +2 tick** rispetto ai passi — è stata caricata sul Deluge,
**nessuna nota è stata toccata**, ed è stata risalvata dal dispositivo.
Riscaricata e confrontata nota per nota: **31 posizioni su 31 conservate,
nessuna spostata.** Il Deluge **non riquantizza al salvataggio**, e questa era
la scommessa su cui poggiava tutto il template. Si legge nei byte di due file, e
nessuna riserva sull'orecchio di chi ascolta la tocca. Il file risalvato è
36 545 byte contro i 35 226 scritti — il firmware aggiunge roba sua — e conserva
**entrambi** gli attributi `noteDataWithSplitProb` e `noteDataWithLift`.

⚠️ **Il sub-slot, che va saputo prima di risalire un giro del genere:** il
Deluge l'ha salvata come **`GROOVE1 2`**, col numero dopo uno spazio, nella
stessa cartella. **Non sovrascrive: si fa un posto suo accanto.** Il percorso
costruito con `MU.destinazione()` non è quello da cui la song torna indietro —
si legge il nome sul display, e `MU.origine()` legge ovunque proprio per
questo.

**Quello che si SENTE, ed è un ascoltatore solo.** Quattro ascolti sulla stessa
coppia, `[OSS]`, con le domande poste **prima** di dire all'utente cosa ci si
aspettava — la previsione era scritta nel rapporto e non gli è stata mostrata,
per non guidare l'ascolto:

| ascolto | la grandezza | esito |
|---|---|---|
| il giro intero, `GROOVE0` poi `GROOVE1` | tutto insieme | sente **e vede** sia le variazioni di velocity sia quelle di timing |
| cassa contro linea di ride | 4 tick = 25 ms a 100 BPM | *«la cassa sul levare è anticipata rispetto al ride»* — **sentito**, e attribuito allo strumento giusto |
| riga del pedale contro il metronomo | 3 tick = 18,75 ms a 100 BPM | *«cadono sul click»* — **non distinto** |
| lo stesso, rifatto dall'utente a tempo lentissimo | 3 tick = 125 ms a 15 BPM | **sentito** |

Delle tre previsioni sull'ascolto **due non sono andate così**, e vale più che
averle azzeccate: chi aveva previsto che il residuo di posizione non si
sarebbe distinto sul giro intero aveva **i numeri giusti e la conclusione
sbagliata**. Se fosse andata come previsto, oggi la casella 6 concluderebbe che
`applica_groove()` vale per metà — la sola velocity — e che la posizione è
rappresentabile ma non percepibile.

⚠️ **E un difetto di metodo che va registrato perché non si ripeta: le tre
domande erano binarie e portavano dentro le parole della risposta** — «volume o
dove cadono?», «prima del ride o insieme?», «sul click o appena prima?».
Chiedere così suggerisce, e un ascoltatore compiacente direbbe sempre di sì.
Quel che le rende comunque informative è che **non ha detto sempre di sì**: due
volte «c'è» e una volta «no», e la volta del «no» è andato a rifare
l'esperimento da sé. Le domande andavano fatte **aperte**.

⚠️ **Le grandezze si dicono in tick, e i millisecondi sono una conversione a un
tempo nominato.** Un tick vale `60000/(BPM × 96)` ms — 6,25 a 100 BPM, 3,38 a
185. Presentare i millisecondi come *la* grandezza fa sembrare fisso qualcosa
che si muove col tempo, ed è precisamente l'errore che l'ascolto a 15 BPM ha
smascherato.

### Il reggae, che l'agenda dava per chiudibile e non lo è

L'agenda in testa a questo documento diceva che il Groove MIDI avrebbe chiuso
«la 6 del jazz e i `[WEB]` della 6 del reggae». Per il jazz è andata così. Per
il reggae il progetto ha **corretto l'agenda invece di eseguirla**, ed è la
correzione in testa al documento.

Il conteggio, ricontato due volte perché due volte è stato sbagliato: **venti
esecuzioni reggae**, di cui **quattro `beat` continue** — a 78, 64, 141 e 126
BPM, **due di `drummer1` e due di `drummer5`**, **dieci minuti in tutto** —
più sedici fill di due-tre secondi l'uno, tutti di `drummer1`, che ne fanno
altri 43 secondi. **Due batteristi.** E dei quattro `beat` soltanto due cadono
nella fascia di tempo che la casella 3 del reggae dichiara: dentro il perimetro
della scheda il corpus ha **due esecuzioni di un batterista solo**. La 6 del
reggae resta `[WEB]`, e adesso ci sta scritto il conteggio col motivo.

⚠️ **Quel paragrafo ha sbagliato un numero due volte mentre difendeva una tesi
giusta**, ed è la parte istruttiva. La prima versione diceva «un batterista
solo» — era una deduzione (`drummer1` ha 18 righe su 20, quindi «praticamente
uno») e **la deduzione aveva mangiato il dato**. La seconda diceva «78, 78,
141, 126»: il secondo 78 era inventato, e quell'esecuzione sta a **64 BPM**.
Trovate tutt'e due dagli implementatori **ricontando invece di rileggere**, e
la seconda pesa: 64 è uno dei due soli tempi che cadono nella fascia
dichiarata, quindi non era decorativo. Le due correzioni stanno **datate** nel
progetto, non sostituite in silenzio.

### Il difetto della finestra di grazia — la lezione più cara del ramo

⚠️ **Una correzione di mezzo passo, messa per una ragione scritta nel commento
e falsa, falsava un terzo dei colpi del corpus e fabbricava la conclusione
portante della casella 6.**

`profilo_da_colpi()` calcolava il movimento con `math.floor(p/ppq + 0.125)` —
mezzo passo di grazia — perché un colpo appena prima del battere fosse
attribuito al movimento seguente. Ne usciva una **fase negativa**, e su una
fase negativa `_senza_swing()` prendeva il ramo della prima metà del movimento
— quella che il firmware **dilata** — per una nota che sta nella seconda,
quella che il firmware **comprime**. Non era l'inversa di niente, e la catena
si credeva esattamente invertibile.

La giustificazione scritta nel commento diceva che senza la grazia «il residuo
uscirebbe grande quanto un movimento intero». **Non può**: il passo si sceglie
con `round(dritta / passo_tick)`, cioè si prende il **più vicino**, quindi il
residuo non supera mezzo passo — 12 tick — **per costruzione**. Contati sul
corpus: **0 residui oltre 12 tick su 28 604, con la grazia e senza.** Non c'era
nessun fondo di verità da salvare.

Quanto pesava, misurato su **42 esecuzioni e 28 604 colpi**:

| | |
|---|---|
| colpi che prendevano una fase negativa | **9 535 (33,3%)** |
| errore mediano sulla loro posizione | 1,25 tick (q1-q3 0,20-2,94), massimo 12,15 |
| colpi che ne uscivano **su un passo diverso** | **956 (3,3%)** |

E non cadeva a caso: il difetto vive nell'**ultimo ottavo di movimento**, cioè
esattamente dove sta chi anticipa un battere. Il charleston a pedale — che nel
jazz suona il 2 e il 4 e li anticipa — ne aveva **il 50,4% dei suoi colpi**, il
ride il 36,1%, la cassa il 37,0%, il rullante il 22,4%.

⚠️ **E così è caduto il «15 su 15», che era il risultato portante della casella
6.** Il charleston contro il ride passa a **12 su 15**, col divario mediano
**cresciuto** da 2,59 a 3,21 tick. Le due cose vanno insieme e hanno una causa
sola: con la grazia i colpi sul battere non potevano passare al passo
precedente in **38 esecuzioni su 42**, quindi **quell'unanimità era in parte
garantita dal difetto, non dai batteristi.**

Cosa regge e cosa no, detto stretto:

- **regge, ed è più solido:** la controprova **sulle fasi grezze** — nessuna
  origine tolta, nessuno swing, quindi nessuna grazia possibile — dice **15 su
  15** e non è cambiata di un decimo. È quella da citare d'ora in poi;
- **regge la stratificazione come livello:** il charleston resta il più
  anticipato di tutti, e il divario contro il ride è più grande di prima;
- **si indebolisce** il rifiuto della latenza fissa, da «~4 sigma su tutte e
  tre le coppie» a 4,2 / 2,7 / 2,4 sigma: l'ipotesi del pedale è ora stretta da
  **una** coppia su tre, non da due;
- **cambiano segno due coppie**, e una era già scritta: il rullante non sta più
  dietro alla cassa nemmeno come segno;
- **non cambia niente** di BUR, scala di velocity, fill, massimo spostamento
  (+11,80 tick) ed escursione (22,83) — verificato eseguendo il tool col codice
  vecchio e col nuovo. Quindi il valore di `set_swing()` non si muove e
  **l'A/B già ascoltato dall'utente non va riletto.**

⚠️ **Non l'ha trovato un test, e nemmeno una revisione: l'ha trovato una
domanda dell'utente su un'altra cosa.** Aveva chiesto una prova A/B
sull'astrazione dello swing — *«è un punto dove è molto facile sbagliare»* — e
costruendola è venuto fuori questo. La correzione ha poi aggiunto **12 check**,
verificati **per inversione**: rimettendo la grazia la suite scende a 938 su
943 con 5 rossi.

⚠️ **E due punti del capitolato che ordinava la correzione erano falsi**:
togliere la grazia cambia **anche** l'assegnazione dei passi (il 3,3%) e il
profilo posizionale (le quote del charleston scendono di quasi tre punti).
Nessuno dei due era previsto.

### Quattro errori di direzione in quattro giri, e un quinto alla fine

⚠️ **I valori erano sempre giusti e il verso no**, e nessun test verde può
accorgersene. Quattro giri di correzione consecutivi sul task che scrive i
numeri, un errore di direzione per giro:

| | l'errore |
|---|---|
| **1** | **una legge fisica enunciata al contrario.** Un tick dura `60000/(BPM×96)` ms, quindi una latenza fissa di D ms vale `D×BPM×96/60000` tick: **cresce** col BPM. La scheda scriveva «cala». La conclusione sopravviveva, l'argomento era falso |
| **2** | **il segno del residuo invertito in tutta la prosa.** `Passo.scarto` è positivo quando il colpo cade **dopo** la griglia — lo conferma `applica_groove()`, che fa `pos + scarto` — quindi il charleston, che ha il residuo più negativo, **anticipa**. La prosa diceva «sta dietro». Trovato **dall'implementatore stesso**, e la frase invertita stava in **sette** posti fra codice, test, piano e spec |
| **3** | **una regressione fatta sulla grandezza sbagliata.** Era sui livelli assoluti, che dopo `origine()` hanno **zero arbitrario** — cosa che la scheda stessa dichiarava tre paragrafi sopra e poi violava. Rifatta sulla grandezza **appaiata** dà 0,8 sigma da costante-in-tick e 4,0 da latenza fissa: sostiene la lettura musicale molto meglio delle tre mediane |
| **4** | **un meccanismo che spiegava un anticipo con un ritardo.** Il paragrafo sul pedale nella casella 6: la conclusione reggeva, l'argomento con cui ci si arrivava era rovesciato |
| **+1** | alla **revisione finale**, il pronome: *«il rullante dietro alla cassa succede in 12 casi su 21»* citava **il numero giusto della cosa sbagliata** — dietro è 9 su 21, davanti 12. Riscritto senza pronome e con tutt'e due i conteggi |

⚠️ **E i quattro non sono tutti la stessa cosa**, che è la parte che serve a
chi riprende. **Due sono sopravvissuti a una revisione**: il segno del residuo
per due giri, il verso della prosa sul pedale per tutti e tre. **Due li ha
introdotti la correzione stessa** — la fisica invertita è entrata **col diff
che chiudeva il giro 1**, la regressione sulla grandezza sbagliata **col diff
del giro 2** — e li ha presi la revisione di quel giro, subito. Dei cinque giri
che il task è costato, quindi, **due sono serviti a riparare danni fatti
riparando**: è per questo che qui una correzione va rivista come se fosse
codice nuovo, e non spuntata come se fosse la chiusura di un rilievo.

**E l'escalation a occhi freschi ha pagato in modo misurabile.** Dopo tre giri
di errori di direzione consecutivi il quarto è stato affidato a un
implementatore **che non aveva scritto quel testo**, e ha trovato due cose che
i tre giri precedenti non avevano visto: un **settimo** posto con la frase
invertita, e l'errore di verso nella prosa della casella 6. Le due passate di
direzione successive non hanno trovato più niente. La regola operativa:

> Quando tre revisioni di fila trovano errori della **stessa famiglia** nello
> stesso testo, il problema non è il testo — è che chi lo rilegge non vede più
> il proprio verso. Si cambia lettore, non si rilegge meglio.

### L'utente, la sesta volta — e la prima in cui ha progettato la misura

⚠️ **L'utente ha declassato i propri stessi dati d'ascolto, e aveva ragione.**
Delle tre risposte date sulla coppia non esce **nessuna soglia**, per due
ragioni e la prima è la più forte: **gli ascolti 2 e 3 non sono lo stesso
compito percettivo** — il 2 confronta due voci fra loro, il 3 confronta una
voce con un riferimento esterno, e la sensibilità dell'una non si trasporta
all'altra. Metterle in fila per dedurne un punto di passaggio non era valido
**nemmeno prima**. La seconda ragione l'ha detta lui:

> *«Considera che variazioni di pochi ms sono difficili da percepire
> consapevolmente da un umano, soprattutto con un orecchio poco allenato come
> il mio. Non credo che la differenza tra le mie risposte a 2 e 3 sia una
> "soglia". A questo livello di dettaglio tutte le mie valutazioni sono
> imprecise.»*

E prima ancora aveva **rifatto l'esperimento di sua iniziativa**, a tempo
lentissimo, ribaltando una conclusione già scritta: a 15 BPM quei 3 tick valgono
125 ms invece di 18,75, e l'anticipo si sente. Quindi l'ascolto a 100 BPM non
aveva misurato l'assenza dello scarto ma **il limite della percezione a quel
tempo** — e cadeva anche l'argomento con cui la conclusione era stata difesa
(«ascoltata nella condizione più favorevole possibile»): mancava il tempo. Un
ascolto che vuole sapere se uno scarto è percepibile ha **due** manopole,
l'isolamento e il tempo, e quel giorno la seconda non era stata girata.

**È la sesta volta che l'utente ha ragione contro qualcosa di già scritto** —
le prime cinque sono in §8 — **ed è la prima in cui non ha obiettato a parole
ma ha progettato la misura che decide.** Che è esattamente la regola operativa
che quell'elenco prescrive: quando dice che non torna, si smette di argomentare
e si costruisce l'esperimento.

Quel che ne resta stabilito non è poco: che le due domande — sfasamento fra
voci e spostamento contro un riferimento — sono **diverse e vanno poste
separate**, e che un residuo scritto **si sente quando è abbastanza grande**.
**Quanto** grande è precisamente ciò che non è stato stabilito, e **non lo
chiuderà un ascolto in più**: servirebbe un protocollo di psicoacustica —
ripetizioni, ordine casuale, prova alla cieca. È scritto come ciò che manca,
non come una lacuna da colmare in fretta: si può comporre benissimo senza
saperlo, purché non si finga di saperlo.

### Il dato più onesto della sessione: il piano aveva torto cinque volte

⚠️ **Il capitolato scritto dal controllore conteneva difetti veri in cinque
task**, e ogni volta li ha trovati **chi ha rifatto i conti invece di fidarsi
del testo**:

| task | cosa il piano sbagliava |
|---|---|
| **4** | un suggerimento del controllore che l'implementatore ha **rifiutato**, e aveva ragione: applicare `f < finestra[1]` dentro `dentro` avrebbe fatto scendere il conteggio da due a uno sulle semicrome, e un pattern di sedicesimi puro sarebbe uscito con **un levare misurato in tutti e otto i movimenti** — `[0.5]*8` invece di `[]`, cioè una coppia di crome dichiarata dove non ce n'è nessuna. Un **falso positivo** nella misura dello swing. Verificato con calcolo indipendente dal ri-revisore, **non accettato sulla parola** |
| **5** | il codice campione passava le posizioni MIDI col ppq nativo (480) invece di riscalarle ai 96 tick del Deluge. Senza riscalatura il residuo massimo su dati reali è **59,01**, con **11,80** — rapporto esattamente 5,0 = 480/96. L'implementatore l'ha aggiunta di sua iniziativa |
| **6** | il brief asseriva **un** batterista reggae e ne sono **due**; e il ripiego sui quartili per campioni sotto i 4 colpi collassava q1 e q3 sul minimo, così che la mediana cadeva **fuori** da `[q1,q3]`. Difetto ereditato dal brief |
| **7** | il test previsto dal piano interrogava `MU.passi()` invece di `applica_groove()` e **passava per costruzione**; e un avvertimento nel dispaccio era infondato, perché il controllore aveva **ricordato** il testo del piano invece di rileggerlo |
| **9** | le quattro esecuzioni `beat` del reggae non sono a «78, 78, 141, 126» ma a **78, 64, 141, 126** |

> **Il metodo che ha funzionato non è stato «il piano era buono».** È stato che
> **ogni affermazione è stata ricontrollata da qualcuno che non l'aveva
> scritta**, e che chi implementava aveva il permesso di dire di no al
> capitolato — cosa che al Task 4 ha impedito un falso positivo. Un piano
> approvato è un'ipotesi con una data, non un'autorità.

### Due incidenti identici di terminatori di riga

⚠️ **`pathlib.write_text()` su Windows traduce `\n` in `\r\n`.** Due agenti
diversi ci sono cascati nella stessa sessione: la prima volta due file passati
da LF a CRLF hanno gonfiato un diff a **1410 e 958 righe**, la seconda
`jazz.md` dichiarava **1773/1293** mentre ignorando i terminatori erano
**260/92** — **l'85% del diff non era contenuto**.

Non corrompe niente e non rompe nessun test. Rende **illeggibile la
revisione**, che in questo progetto è il meccanismo su cui poggia tutto il
resto: le cinque correzioni di verso raccontate qui sopra sono state trovate
tutte in revisione, e una revisione si fa leggendo diff. Riparato con
`write_bytes()` in tutt'e due i casi, e la regola sta in testa al documento
sotto «Cosa NON rifare», dove la legge chi genera file.

### Cosa resta aperto, e cosa NON rifare

Punti aperti che questo lavoro lascia. I due di macchina — il limite dello
stimatore e cosa faccia il firmware fra le crome — sono anche in §7, insieme
alla soglia percettiva che gli ascolti non hanno stabilito:

- **la stratificazione misurata non è mai stata messa davanti a un orecchio.**
  I 13,5 ms di divario ride/charleston sono la parte **ben misurata**, e
  l'ascolto è stato fatto su `drummer1/session3/2`, che di stratificazione ne
  ha **−0,25 tick**: su quel file non c'era, quindi l'ascolto non poteva né
  confermarla né smentirla. La coppia da fare è su **`drummer10/session1/1`**
  (`jazz/swing`, 124 BPM, 164 s, BUR 1,82), dove sui passi 4 e 12 il divario è
  di **5,64 e 5,93 tick** e il ride **è** davvero `ride`;
- **il limite dello stimatore, che la correzione ha smesso di nascondere.** Un
  template è per definizione **per passo**, e un batterista che anticipa di
  mezza semicroma non ci sta dentro: esce sul passo precedente col segno
  rovesciato. Su alcune esecuzioni la semicroma *prima* del movimento porta più
  colpi del movimento stesso — «battere in minoranza». Pesa sul charleston
  perché mette il 43,7% dei suoi colpi su due soli passi. Chiuderlo vuol dire
  cambiare **come si aggrega**, ed è una decisione di disegno che la casella 6
  dichiara e non prende;
- **se il firmware faccia davvero quello che `_senza_swing()` modella.** L'A/B
  assolve il **modello dello swing** — quattro modelli a differenza grossa
  esclusi, l'utente ha risposto *«sufficientemente simili»* — ma non la
  **catena che scrive i template**, e resta aperto cosa faccia il firmware a
  una nota che cade **fra** le crome, che il template ne scrive. La
  dichiarazione di ignoranza esiste già: `song.SWING_SCARTO_SORGENTE`;
- **il ramo `groove-midi` non è ancora stato fuso.** La revisione finale — 30
  commit rivisti insieme, nessun Critical, quattro Important tutti chiusi — lo
  ha dichiarato **fondibile**. La decisione resta da prendere.

⚠️ **Cosa NON rifare, e vale come divieto operativo:**

- **non rigenerare `out/GROOVE0.XML` e `out/GROOVE1.XML`.**
  `tools/genera_groove.py` non è un pulsante da premere: eseguirlo
  **sovrascriverebbe l'unico esemplare** dei due file su cui poggiano i quattro
  ascolti e il giro sul dispositivo (31 posizioni su 31), e l'unica traccia che
  ne resterebbe sono gli hash nel registro di sessione — `853bcdec…` per
  `GROOVE0`, `d781262c…` per `GROOVE1`. La coppia è stata costruita **prima**
  che la grazia fosse tolta: rifacendo oggi la catena la riga del pedale esce a
  **−4 tick** invece di −3, e cambiano **altre otto posizioni su 31**. Chi
  rivuole la coppia col codice di oggi **la scriva altrove e la confronti**.
  `out/SWINGA.XML` e `out/SWINGB.XML` hanno lo stesso rischio e nessuno
  finora l'aveva scritto;
- **non citare più il «15 su 15» del residuo lavorato.** È 12 su 15. Il 15 su
  15 che regge è quello delle **fasi grezze**, che non passa da nessuna catena;
- **non convertire in millisecondi i livelli della tabella del residuo.** Dopo
  `GR.origine()` ogni esecuzione ha uno **zero arbitrario**: «−3,42 tick» non
  dice *rispetto a che cosa*, e un millisecondo ricavato da lì non ha un
  referente. Lì i tick servono a una cosa sola, a dire che il residuo è piccolo.

---

## 7. Punti aperti

> Le **lacune funzionali** — cosa il sistema non sa ancora fare — stanno in
> testa a questo documento, sotto «Il prossimo lavoro». Qui sotto ci sono i
> punti aperti sul *formato* e sulle verifiche mancanti.

- ~~`set_scale()` vuole i nomi inglesi (`D`) mentre `musica.altezza()`
  accetta anche gli italiani (`re`)~~ — **risolto, revisione finale del 15
  agosto**: `song.set_scale()` ora riusa `musica.altezza()` per riconoscere
  lo stesso vocabolario (italiano, inglese, diesis, bemolle), senza
  duplicare il parser. Il giro ha chiuso anche un difetto più subdolo,
  silenzioso: il codice vecchio faceva `root.upper().replace('B', '#')`, e
  un bemolle come `'Ab'` diventava silenziosamente `rootNote 10` (A#)
  invece di `8` (G#) — un semitono sbagliato senza nessun errore. Stesso
  per `'Db'` (dava D#, non C#) e `'Gb'` (dava G#, non F#)
- ~~`row-add` ha probabilmente lo stesso difetto di §3.1 a un livello più
  basso~~ — **c'era davvero, ed è risolto il 16 agosto** (§6-sexies, FINDINGS
  §6-octies). L'intuizione era giusta e anche più grave del previsto: non solo
  `row-add`, ma **ogni clip generata** si apriva con la finestra lontana dalle
  note. `yScroll` governa la clip view di tutti i tipi di clip, con tre unità
  diverse, e ora `fit_clip_scroll_to_notes()` ancora la riga più bassa in fondo
  allo schermo. Tre coppie controllate in `refs/songs/`
- ~~struttura delle istanze di clip nell'arranger~~ — **risolta e verificata
  sul dispositivo il 14 agosto 2026** (FINDINGS §6-ter,
  `tools/delugexml/arranger.py`). Le posizioni non stanno nelle clip ma in un
  attributo `clipInstances` sullo **strumento**, terne esadecimali
  `(pos, length, clipCode)`; `clipCode` è un **indice ordinale** e il bit 31
  sceglie fra `<sessionClips>` e `<arrangementOnlyTracks>`. Lettura provata su
  2116 istanze in 24 song; scrittura provata riproducendo la coppia
  controllata ARR0/ARR1 attributo per attributo, e poi generando un
  arrangiamento nuovo (`ARRTEST`) confermato sul dispositivo.
  Anche le clip "bianche" (senza `section`, bit 31) sono fatte e verificate:
  `arranger.place_unique()`
- **Le sezioni sono scene**, cioè gruppi di lancio, non una proprietà della
  singola clip. Nell'arranger le sezioni **non esistono**: si piazzano istanze
  di clip su tracce di strumento, e la sezione riemerge solo come colore.
  `numRepeats` ha quattro stati (`-2` esclusivo, `-1` non esclusivo, `0`
  infinito, positivo = conteggio), e vale 0 in tutte e 2100 le sezioni del
  corpus. Vedi FINDINGS §6-ter
- **Il tipo di una clip è dichiarato tre volte** — tag dei params, indice
  delle righe, `affectEntire` — e se non concordano il Deluge rifiuta l'intero
  file come corrotto, pur essendo XML valido. Costato un giro sul dispositivo;
  ora lo blocca `song.check_clip_types()`. Vedi FINDINGS §6-quater
- ancora aperta: la tabella dei **colori di sezione**, che il firmware indicizza
  con `defaultClipSectionColours[section]` e che non è stata trovata nel
  sorgente. Va ricavata dal dispositivo
- ~~quale attributo esprime la **lunghezza propria di una noteRow**~~ —
  **trovato nei file il 12 agosto: è `length` sulla `<noteRow>` stessa**, con
  `sequenceDirection` (`pingpong`) come attributo fratello. 197 righe in 60
  clip, distribuite quasi equamente fra righe di synth (108, con `y`) e di kit
  (92, con `drumIndex`): non è una cosa da kit. La lunghezza della riga **può
  superare quella della clip** (clip 384, riga 552), quindi è indipendente, non
  una suddivisione. Nel corpus c1.3.0 c'è un solo esempio (`Qbix.XML`, clip
  `KIT000`: righe da 384, 576 e 504 tick su una clip da 672); gli altri vengono
  da `corpus_versions\`. **Osservato nei file, non ancora verificato sul
  dispositivo** — resta da confermare che produca davvero il poliritmo, e da
  capire cosa succede quando riga e clip non sono in rapporto intero
- ~~formula esatta fra i tre livelli di scala dei parametri~~ — **trovata il
  12 agosto**, ed è un'uguaglianza intera esatta, non una regressione:

      valore_senza_segno = display × 85899345        85899345 = 2³² // 50

  Su 183 101 valori del corpus il 56,7% la soddisfa **al byte**, più un 39,2%
  di estremi speciali (`0x00000000` = 25 al centro, `0x7FFFFFFF` = 50,
  `0x80000000` = 0): **95,9% spiegato senza tolleranze**. In
  `tools/delugexml/params.py`, con `dsong.py params` che stampa i parametri
  nelle unità del display.

  **E una seconda griglia, verificata sul dispositivo.** Il volume di un synth
  portato a 35 sullo schermo ha prodotto `0x34000000` — cioè **interno 90 su
  128**, non `0x33333313` della griglia storica:

      valore = interno × 33554432        33554432 = 2³² // 128
      display = round(interno × 50 / 128)

  Il display mostra 0-50 (confermato: è la scarsa risoluzione per cui il
  firmware ufficiale veniva criticato), ma il firmware community lavora più
  fine. Quindi **passare per il display perde risoluzione**: 129 valori
  interni si schiacciano su 51 mostrati. `internal_of()` e `from_internal()`
  la conservano e sono byte-esatti; `from_display()` scrive sulla griglia
  interna, come fa il dispositivo oggi.

  **I patch cable hanno una scala loro, anch'essa chiusa sul dispositivo.**
  `lfo1 → modulator1Volume` a 30 → `0x26666666` = round(0,3 × 2³¹). Il range
  mostrato è bipolare −50…+50, quindi `+50 = 0x40000000`, metà dell'int32 —
  previsione verificata: su 15 372 valori del corpus il **100,00%** sta entro
  quel limite, e cinque ci cadono esattamente sopra.

  ⚠️ `polarity` nel file **non** è il range dell'interfaccia: il cable misurato
  si dichiara `unipolar` ma sul dispositivo era bipolare. Cosa sia resta ignoto.

  Attenzione: fuori griglia non sono certi *attributi* ma certi *valori* — lo
  stesso `lpfFrequency` è sulla griglia in una song e fuori in un'altra.

  > **Cautela metodologica.** Ho provato a datare le due griglie confrontando
  > le versioni di firmware in `corpus_versions\`: **non funziona**, e la
  > tabella che ne esce è ingannevole. I valori non toccati vengono riportati
  > identici a ogni salvataggio, mentre `firmwareVersion` registra solo
  > l'ultimo: una song del 2021 risalvata oggi si dichiara c1.3.0 e conserva
  > valori di allora. Le statistiche sul corpus non possono datare i singoli
  > valori. L'unica prova valida è muovere **un** parametro e guardare cosa
  > cambia.
- **cosa fa il firmware a una nota che cade FRA le crome**, quando lo swing di
  song è attivo. `song.set_swing()` con `swingInterval` a 1/8 muove la seconda
  di ogni coppia di **crome**; `GR._senza_swing()` modella lo swing come mappa
  lineare a tratti su **tutto** il movimento, e un groove template scrive note
  fra le crome. L'A/B del 24 agosto 2026 (§6-terdecies) **assolve il modello**
  — quattro modelli alternativi a differenza grossa sono esclusi — ma non
  risponde a questa domanda, e la divergenza fra le due letture è massima
  proprio a fase 0,25 e 0,75. Si chiuderebbe con una coppia controllata
  **costruita** a quelle fasi. Il buco noto adiacente è già dichiarato in
  `song.SWING_SCARTO_SORGENTE`
- **quanto grande debba essere un residuo di posizione perché si senta.** Non è
  una lacuna del Deluge ma del protocollo: gli ascolti del 24 agosto 2026 sono
  **un ascoltatore, nessuna ripetizione, nessuna prova alla cieca**, e
  l'ascoltatore stesso ha dichiarato imprecise le proprie valutazioni. Da lì
  non esce nessuna soglia, e non la darà un ascolto in più — servirebbe un
  esperimento di psicoacustica. Vale la pena saperlo perché la finestra
  **20-40 ms** che `MUSICA.md` dichiara resta `[WEB]` e non è stata né
  confermata né contraddetta
- **l'aggregazione per passo del groove template.** Un template è per passo, e
  un colpo che anticipa il suo passo di più di mezza semicroma esce sul passo
  **precedente col segno rovesciato**: su alcune esecuzioni la semicroma prima
  del movimento porta più colpi del movimento stesso. È un limite dello
  stimatore, non un difetto, e chiuderlo vuol dire cambiare come si aggrega.
  Dichiarato in `docs/repertori/jazz.md`, «Il bordo fra due passi»
- byte 10 delle note: i valori fra 21 e 127 non spiegati dai 20 gradini di
  probabilità — probabilmente il LATCHING descritto nel manuale
- perché 24 `<section>` quando il manuale ne descrive 12
- MPE nell'XML, mai guardato (il setup usa Exquis in Lower Zone)
- confronto dello schema **fra versioni di firmware**: non è più bloccato, le
  103 song sono state copiate in `corpus_versions\` divise per versione. Resta
  da fare l'analisi vera e propria (`scan_versions.py` è il punto di partenza)

---

## 8. Preferenze di lavoro

Dall'handoff originale, tutte confermate dall'esperienza:

- **approccio incrementale**, un passo verificato alla volta
- **riconoscimento esplicito degli errori**: se qualcosa non torna, dirlo
- **verifica prima di operazioni distruttive**, sempre — la SD contiene lavoro
  personale
- **mai inventare tag, parametri o strutture**: se non è stato osservato in un
  file reale o in una fonte primaria, va dichiarato come ipotesi
- diffidenza verso le fonti deboli su dettagli tecnici — inclusa la
  documentazione community, che sui byte di comando SysEx è **sbagliata**
  (dà 0x06/0x07, i valori giusti sono 0x04/0x05)
- solo firmware community, la retrocompatibilità con quello ufficiale non
  interessa

E tre regole guadagnate sul campo, ognuna pagata:

- **non dedurre dal file cosa fa il dispositivo.** Se la domanda è «il Deluge
  lo accetta?», l'unica risposta valida viene dallo schermo del Deluge.
- **«non sto inventando» non è «ho visto».** Un nome di attributo osservato nel
  posto sbagliato è comunque il posto sbagliato: è così che è nata l'ipotesi
  sbagliata sulla riga MIDI di un kit (FINDINGS §6-septies).
- **l'utente sa cose che i file non dicono.** Le tre correzioni più importanti
  del 16 agosto sono venute da tre sue frasi: che `cents` è il fine tuning, che
  i drum MIDI mancano dal corpus solo perché non li ha mai usati, e che
  l'ordine delle righe di un kit lo decide chi suona. Nessuna delle tre era
  ricavabile dai file — la prima è nel manuale, le altre due no. **Quando dice
  che qualcosa non torna, ha ragione lui**: è successo **sei volte su sei**, e
  ogni volta stavo per chiudere dichiarando fatto.

  La quinta, il 17 agosto, è la più istruttiva perché non l'ho corretta
  subito: avevo appena difeso la mia tabella dell'intervallo di swing con
  un'aritmetica presa dal sorgente. La sua obiezione era una frase sola —
  *«la divisione non dovrebbe essere 8th?»* — senza numeri e senza fonti, e
  aveva ragione. **La sua incredulità vale più della mia derivazione**, e la
  regola operativa che ne discende è: quando dice che non torna, si smette di
  argomentare e si progetta l'esperimento che decide.

  **La sesta, il 24 agosto, è la prima in cui quella regola l'ha eseguita
  lui.** Non ha obiettato a parole: ha **rifatto l'esperimento** — lo stesso
  ascolto a tempo lentissimo — e ha ribaltato una conclusione già scritta,
  perché a 15 BPM lo stesso scarto di 3 tick vale 125 ms invece di 18,75. Poi
  ha **declassato i propri stessi risultati**, dicendo che con un orecchio non
  allenato e senza prove alla cieca da lì non esce nessuna soglia — e aveva
  ragione anche in questo, perché i due ascolti che si stavano confrontando non
  erano nemmeno lo stesso compito percettivo. §6-terdecies.

---

## 9. La pubblicazione — 17 agosto 2026

Il repo è su <https://github.com/PaoloQuaranta/DelugePal>, **GPL-3.0**, con una
storia nuova di un commit solo. I 54 commit precedenti **non erano
pubblicabili**: ognuno porta con sé song scritte dal dispositivo.

### Cosa NON è pubblicato, e perché

| | |
|---|---|
| 130 song (27 in `refs/songs`, 103 in `corpus_versions`) | sono musica di qualcuno |
| preset di kit e synth | vengono da sample pack **a pagamento** |
| **le 16 fixture delle prove controllate** | vedi sotto |
| `docs/SCHEMA_*.md` | inventari generati: le colonne «valori osservati» citano nomi di song, di preset e 43 percorsi `SAMPLES/` |
| `refs/settings/` | la configurazione del dispositivo |
| `to-read/` | 4,8 GB di libri e librerie MIDI di terzi |

⚠️ **Il caso che non era ovvio: le fixture.** Erano state esplicitamente tenute
nel piano, poi la verifica ha mostrato che **una song del Deluge incorpora i
778 parametri di OGNI strumento che usa** — e tutte e 16, più tutti gli 8
`sd_salvati`, contengono la patch a pagamento `SYNTHS/BOD new/BOD2-01-RIGHT-PLACE`.
26 occorrenze.

Neutralizzarle sostituendo la patch è stato **valutato e scartato**:
distruggerebbe proprio ciò che le rende prove, cioè l'essere state scritte dal
dispositivo byte per byte. Un file riscritto da noi non dimostra più niente.

L'unico XML pubblicato è `refs/synths/TEMPL.XML`: è il synth **vuoto**, cioè i
default del firmware, non il lavoro di nessuno.

### Come è protetto

- **`.gitignore` deny-by-default**: tutto sotto `refs/` è escluso e rientra
  solo `TEMPL.XML`. Ripopolare le cartelle dalla SD non può far sfuggire nulla.
- **hook `pre-push`** in `.git/hooks/`: rifiuta il push se un commit contiene un
  `.XML` non previsto, un `.wav`, o roba sotto `corpus_versions/` o `to-read/`.
  Controlla **ogni commit del tratto**, non solo la punta — un file aggiunto e
  poi rimosso resterebbe pubblicato lo stesso. Provato in entrambe le
  direzioni. **Limite: gli hook non sono versionati**, vale su questa macchina.

### La storia vecchia

`D:\DelugePal-storia.bundle` (1,8 MB) contiene **tutti e 54 i commit e i 4
branch**. Verificato clonandolo prima di cancellare l'originale: 54 commit, i
messaggi giusti, le 162 song dentro. Si riapre con:

```
git clone D:\DelugePal-storia.bundle una-cartella
```

### Cosa resta da sistemare

- `.claude/skills/deluge-pal/SKILL.md` dice «Il progetto sta in `D:\DelugePal`»,
  che per chi clona è falso
- l'hook non è versionato: per condividerlo servirebbe una cartella `hooks/`
  tracciata più `core.hooksPath`
- il README dichiara i limiti noti, ma `docs/` resta **tutto in italiano** — la
  traduzione è stata valutata e rimandata: ~50 000 parole di prosa più le
  docstring, che sono saggi e non descrizioni di argomenti
