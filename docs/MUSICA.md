# Conoscenza musicale — cosa funziona sul materiale di questo utente

Questo file **non** è una teoria generale della musica: per quella si invoca
la skill `music-composer`. Qui sta solo ciò che è stato imparato correggendo
il lavoro, e che nessuna skill generica sa.

Stessa disciplina del resto del progetto: si scrive ciò che è stato
verificato, e si segna `[OSS]` ciò che è supposto.

---

## Norme di sound design — dette dall'utente, 16 agosto 2026

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

### La risonanza non ha una soglia: ha un compenso

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

### Come si applica quando c'è un LFO sul filtro

Un wobble è `lfo1 → lpfFrequency`, cioè il cutoff **oscilla intorno alla sua
base**. Vanno scelti insieme, non uno per volta: base 25 con ampiezza 18 sta
fra 7 e 43 e resta sempre udibile; base 12 con la stessa ampiezza passa metà
del tempo sotto lo zero, e il wobble diventa un suono che sparisce a
intermittenza.

## Il corpus non è autoritativo — detto dall'utente, 16 agosto 2026

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

## Preset e come vengono usati

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

## Groove e generi

### Reggae e dub — istruzioni compositive

> ⚠️ **`music-composer` non serve per questo genere: non ha né reggae né dub.**
> Il suo `references/genres.md` copre Dubstep, Reggaeton, Bossa Nova e altro,
> ma di reggae e dub non c'è nessuna voce. Verificato il 16 agosto 2026 —
> controllare prima di appoggiarcisi.
>
> Tutto quanto segue viene da ricerca web ([WEB], fonti in fondo alla
> sezione). Non è ancora stato validato dall'ascolto dell'utente: `DUBPAL01`,
> scritto **prima** di questa ricerca, è stato giudicato «molto elementare e
> per niente somigliante a un pezzo dub».

#### Le quattro parti, e come si incastrano

Il reggae non è definito dall'armonia ma dalla **spartizione ritmica della
battuta fra le parti**. Ogni parte occupa un posto che le altre lasciano
libero. Griglia a 16 passi per battuta, come `MU.passi()`:

```
                0 1 2 3 4 5 6 7 8 9 . . . . . .
movimento       1       2       3       4
charleston      . . x . x . x . x . x . x . X .   ottavi, ma l'UNO è vuoto
cassa           . . . . . . . . x . . . . . . .   solo il 3
rullante/rim    . . . . . . . . x . . . . . . .   col la cassa, cross-stick
skank (accordi) . . x . . . x . . . x . . . x .   TUTTI i levare
bubble (organo) . x x . . x x . . x x . . x x .   i sedicesimi attorno al levare
basso           x . . . . . x . x . . . . x . .   frase di 1-2 battute, ripetuta
```

**Il punto che avevo sbagliato in `DUBPAL01`:** avevo messo il **charleston**
sui levare e non avevo affatto lo **skank**. È l'opposto. Il charleston fa una
*timeline regolare* — ottavi, o sedicesimi con i levare appena accentati — e
il levare è dello **skank**, che è armonia, non percussione.

#### La batteria

- **one drop**: cassa e rullante **insieme sul terzo movimento**, e il **primo
  movimento vuoto** — è l'accento dominante unico della battuta, e il nome
  viene proprio dal *lasciar cadere* l'uno. [WEB, concorde su 4 fonti]
- il rullante in roots è quasi sempre un **cross-stick / rimshot**, non un
  colpo pieno.
- **anche il charleston salta l'uno**, non solo la cassa. [WEB]
- **l'apertura di charleston sull'ultimo ottavo della battuta**, che porta
  dentro la battuta successiva, è prassi standard. È il dettaglio che fa
  suonare "vero" un pattern altrimenti corretto.
- **turnaround**: ogni 4 o 8 battute, sull'**ultima**, il rullante devia dal
  pattern con una girata sincopata. Senza, il giro è morto — ed è
  esattamente il difetto di `DUBPAL01`, che ripeteva quattro battute
  identiche.
- fill di charleston in **terzine**, appoggiate indietro, sono un altro
  elemento tipico.

Le varianti, che cambiano il carattere lasciando il rullante sul 3:

| | cassa | passi |
|---|---|---|
| **one drop** | solo il 3 | `........x.......` |
| **rockers** | tutti i movimenti | `x...x...x...x...` |
| **steppers** | tutti gli ottavi | `x.x.x.x.x.x.x.x.` |

Tempo: **50-100 BPM**, con 70-78 al centro del roots. Quindi 70 BPM non è
"lento per il dub", è il posto giusto.

#### Il basso

È **lo strumento solista**, non l'accompagnamento.

- **una frase di una o due battute, ripetuta ossessivamente.** [WEB] Questo
  era l'errore più grosso di `DUBPAL01`: una linea di quattro battute che si
  *sviluppa* è un'idea da un altro genere.
- **centrata sul terzo movimento**, non semplicemente "che evita l'uno".
- **lo spazio conta quanto le note**: quello che si toglie è materiale
  compositivo.
- per il sapore **dub** in particolare: **note ripetute, e soprattutto la
  quinta SOTTO la tonica**. [WEB] In sol minore è il **re grave** sotto il
  sol.
- segue gli accordi outlinando le note dell'accordo "in orizzontale".
- si taglia tutto **sopra i 1000 Hz**. [WEB]

#### L'armonia

**Pochi accordi, spesso solo due alternati.** [WEB] Quello che distingue
l'armonia reggae non è la complessità ma il **ritmo con cui è suonata** — lo
skank. Una progressione ricca suonata dritta non è reggae; due accordi
suonati in levare lo sono.

#### Il dub come *pratica*, non come stile

Il dub nasce al banco del mixer: si parte da un riddim già suonato e lo si
**smonta in tempo reale**.

- **si compone togliendo.** La struttura è "parti che entrano ed escono", non
  "sezioni che si sviluppano". Un vuoto di quattro battute con sole batteria
  ed eco vale più di un ritornello.
- **delay e riverbero sono strumenti compositivi**, non rifiniture. Il
  *"chick-a"* dello skank raddoppiato è delay, non due colpi suonati.
- l'eco classico si manda su **colpi singoli** — un rullante, una parola, uno
  stab — non su tutta la parte.
- in `arranger.py` questo si scrive con i **buchi fra le istanze**.

#### Fonti

[Feel It In The One-Drop, wayneandwax](https://wayneandwax.com/org/lessons/roots-riddim-tutorial.html) ·
[One drop rhythm, Wikipedia](https://en.wikipedia.org/wiki/One_drop_rhythm) ·
[Music Theory/Reggae, Wikibooks](https://en.wikibooks.org/wiki/Music_Theory/Reggae) ·
[Bubblin', Berklee](https://www.berklee.edu/berklee-today/spring-2015/The-Woodshed-Bubblin) ·
[Authentic Reggae & Dub Bass, soundfingers](https://soundfingers.com/blog/reggae-dub-production/authentic-reggae-dub-bass-tutorial/) ·
[Dub Mixing, Sound on Sound](https://www.soundonsound.com/techniques/dub-mixing)

### Velocity groove

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

#### Il velocity groove del one drop

- il colpo sul **3** è l'accento dominante e va nettamente sopra tutto il
  resto — è l'unico evento forte della battuta;
- **charleston mai identici**: gli ottavi dritti e uguali «suonano troppo
  squadrati», e i **levare vanno accentati appena**, non molto; [WEB]
- **fantasmi di rullante** fra un cross-stick e l'altro danno il tessuto;
- l'**apertura di charleston** sull'ultimo ottavo prima della battuta nuova è
  il colpo più forte del charleston.

#### Il feel: swing, non solo velocity

Il one drop è **laid-back**: gli ottavi di charleston sono **swingati**, e i
levare arrivano leggermente in ritardo — «leaning into the space rather than
cutting through it». [WEB]

Sul Deluge questo **non** si fa spostando le note: c'è lo swing di song, e la
sua scala è documentata (FINDINGS §6): il display va **0-100 con 50 = dritto**,
e nel file è un valore con segno centrato sullo zero.

```python
S.set_swing(doc, 57)      # unita' del display: sopra 50 = swingato
```

⚠️ In `DUBPAL01` avevo scritto `set_swing(doc, 50)`, cioè **dritto**. Per un
one drop è sbagliato in partenza.

### Pattern tipici per genere

Catalogo che cresce. Griglia a 16 passi = una battuta, direttamente
incollabile in `MU.passi()`.

#### Reggae / dub — one drop, 70 BPM

```python
hat  = '..x.o.X.o.x.o.X.'    # ottavi, l'UNO vuoto, levare appena accentati
kick = '........x.......'    # solo il 3
rim  = '..o.....X.....o.'    # il 3 e' l'evento, i fantasmi fanno tessuto
```

Ultima battuta di ogni gruppo di 4 — il **turnaround**, senza il quale il
giro è morto:

```python
rim4 = '..o.....X...x.X.'
hat4 = '..x.o.X.o.x.o.XX'    # doppio colpo che porta dentro la battuta dopo
```

Varianti di cassa che cambiano il carattere lasciando il rullante sul 3:

```python
rockers  = 'x...x...x...x...'
steppers = 'x.x.x.x.x.x.x.x.'
```

E le due parti armoniche, che sono la cosa che mancava del tutto:

```python
skank  = '..x...x...x...x.'   # accordi staccatissimi, TUTTI i levare
bubble = '.oo..oo..oo..oo.'   # organo, i sedicesimi attorno al levare
```

## Correzioni ricevute

*(ogni volta che una proposta viene corretta, la lezione va qui, con la data)*

**16 agosto 2026 — «leggi anche documentazione», «leggi anche docs
community».** Ero andato dritto ai file saltando il primo livello della
gerarchia del progetto. Da `ARCHITETTURA.md` §9b è poi venuto il pezzo che
serviva davvero e che i file non dicono: la matrice delle sorgenti di
modulazione, il fatto che gli inviluppi che modulano qualcosa di diverso dal
volume sono **bipolari con neutro 25**, e che i parametri globali (delay, mod
FX, riverbero, arpeggiatore, LFO1 rate) accettano **solo** Sidechain e LFO1
come sorgente. Quest'ultima è una regola che, violata, non dà errore: dà
silenzio.

**16 agosto 2026 — «è molto elementare e non assomiglia per niente a un pezzo
dub», «anche il ritmo di batteria è penoso».** Giudizio su `DUBPAL01`, ed era
un problema di conoscenza, non di strumenti: avevo fatto **una sola** ricerca
web sul dub, tirandone fuori nomenclatura (one drop, rockers, steppers) invece
di mestiere, e avevo invocato `music-composer` **senza leggerne i reference**
— che comunque non hanno reggae né dub. Gli errori concreti, tutti dovuti a
questo:

| errore | cosa era giusto |
|---|---|
| charleston sui levare, **skank assente** | il charleston fa una timeline regolare, il levare è dello skank, che è armonia |
| nessun *bubble* d'organo | riempie i sedicesimi attorno al levare |
| basso di 4 battute che si sviluppa | frase di **1-2 battute ripetuta**, centrata sul 3 |
| 4 battute di batteria identiche | **turnaround** sull'ultima di ogni 4 o 8 |
| velocity a due soli livelli | servono i **fantasmi**, sotto 70 |
| `set_swing(50)`, dritto | il one drop è **swingato e laid-back** |
| pad a note lunghe come parte armonica | in reggae l'armonia è **ritmica**, staccata, in levare |

La lezione di metodo: **una ricerca sola su un genere dà le etichette, non il
mestiere.** Le etichette bastano a scrivere qualcosa di formalmente corretto e
musicalmente morto — che è esattamente cosa è successo.

**16 agosto 2026 — «ora ci sono 4 envelope, non 2».** Un risultato di ricerca
web diceva «2 LFO and envelope options»: era il manuale ufficiale vecchio. Il
firmware community ha **4 inviluppi e 4 LFO**, e `TEMPL.XML` infatti porta
`envelope1..4` e `lfo1..4`. Vale come promemoria che sul firmware community
le fonti generaliste sono indietro, e che il guidebook ufficiale va letto
sapendo quale versione descrive.
