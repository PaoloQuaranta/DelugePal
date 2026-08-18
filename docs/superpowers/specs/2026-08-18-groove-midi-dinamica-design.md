# Il Groove MIDI: la dinamica del jazz, e il groove template

**Progetto approvato il 18 agosto 2026.** Chiude la casella **6, Dinamica**
della scheda `docs/repertori/jazz.md`, che oggi è vuota, e costruisce il
**groove template** — la cosa che `SKILL.md` nomina da sempre («file MIDI
ordinari che portano timing e velocity di un groove suonato») senza che
nessuno l'avesse mai fatta.

Il punto di partenza è l'agenda scritta in testa a `HANDOFF.md`: *«jazz 6
(dinamica) — la chiude il Groove MIDI, già sul disco»*. È giusta per il jazz.
Per il reggae, come si vedrà al §2, **non lo è**, e questo progetto la corregge
invece di eseguirla.

---

## 1. Cosa chiude, e cosa lascia aperto

| casella | da → a |
|---|---|
| **jazz 6**, Dinamica | ○ → ● |
| **jazz 4**, Feel | ● → ● (ci entra un secondo BUR, misurato su un altro corpus) |
| **jazz 9**, Forma e densità | ○ → ◐ (i fill, non la forma) |
| **jazz 10**, Sul Deluge | ◐ → ◐ (ci entra il template, resta fuori tutto il resto) |
| **jazz 1**, Cos'è | ○ → ○ — **non si chiude**, ma la delimitazione operativa va detta nella 6 |
| **reggae 6** | ● → ● — restano i `[WEB]`, e si scrive **perché** |

---

## 2. Cosa il corpus regge davvero

`to-read/MIDI/groove-v1.0.0-midionly/groove/`, 1150 esecuzioni con
`info.csv`. Contati per **prefisso** di `style` il 18 agosto 2026 `[OSS]`:

| | esecuzioni | `beat` | `fill` | batteristi |
|---|---|---|---|---|
| jazz | 101 | 50 | 51 | 5 — ma `drummer1` ne ha 63 |
| reggae | 20 | **4** | 16 (~2,7 s l'uno) | **2**, e uno ne ha 18 |

Sulle sole `beat` del jazz i batteristi si spartiscono così: `drummer1` 19,
`drummer3` 13, `drummer10` 10, `drummer7` 6, `drummer4` 2. È poco per dire
«il jazz», abbastanza per dire «cinque batteristi di studio», ed è quest'ultima
la frase che va scritta accanto al numero.

⚠️ **Il reggae del Groove MIDI è un batterista solo e dieci minuti di
musica.** Quattro esecuzioni continue (78, 78, 141, 126 BPM) più sedici fill da
meno di tre secondi. Chiamare `[MIS]` quello che ne uscirebbe sarebbe
travestire un esecutore da repertorio — la stessa cosa che la casella 8 del
jazz vieta in una riga («un assolo è un musicista, non un repertorio»). Quindi
la casella 6 del reggae **resta `[WEB]`**, e ci si scrive il conteggio col
motivo, perché la riga ottimista che c'è oggi rimanderebbe la prossima sessione
esattamente qui.

⚠️ **L'etichetta `jazz` è larga.** Dentro ci sono `jazz/funk` (24) e
`jazz/fusion` (11), che di swing di crome non ne hanno — e la casella 4 lo dice
già dal lato Weimar, dove la fusion sta a BUR 1,26 contro l'1,80 dell'hard bop.
La delimitazione va **dichiarata nella 6**, non lasciata implicita nel filtro.

⚠️ **`to-read/` è in `.gitignore`.** Chi clona non trova né i file né il
conteggio da rifare: quei numeri sono lo stato del disco del 18 agosto 2026.

---

## 3. Il trabocchetto: l'origine della griglia

Misurato su `drummer1/session3/2_jazz-swing_185_beat_4-4.mid` — 185 BPM,
250 secondi. Dove cadono i colpi dentro il movimento, contando dal tick 0:

| | colpi | picco |
|---|---|---|
| ride | 249 | 0,958 |
| kick | 467 | 0,958 |
| rullante | 209 | 0,958 |
| charleston a pedale | 390 | 0,958 |

**Tutti gli strumenti allo stesso posto**, quindi non è feel: è che il tick 0
del file non è un movimento del batterista (la prima nota sta a tick 1287).
Misurare lo scarto dal tick 0 riporterebbe un anticipo sistematico del ~5% per
ogni esecuzione: un numero pulito, ripetibile e falso.

È lo stesso errore della Weimar, nella stessa posizione — **l'origine della
misura** — dove `tatum`/`division` conteneva già lo swing e costò tre tentativi
che si confermavano a vicenda. Qui la contromisura è che l'origine si **stima e
si toglie** prima di qualunque altra cosa — la **media circolare** degli onset
di tutti gli strumenti modulo il passo di 1/16, che è l'unica media sensata su
una grandezza che gira — e che l'anticipo assoluto **non si
dichiara affatto**: a 185 BPM quel 5% vale 16 ms, indistinguibile dalla latenza
di cattura del kit elettronico su cui il dataset è registrato. Quello che resta
dopo averlo tolto — lo scarto di *uno strumento rispetto agli altri* — è invece
feel, ed è misurabile.

---

## 4. Il doppio swing, e come si spartisce

Se lo swing lo scrive `S.set_swing(doc, 62, figura='1/8')`, che è **di song** e
quindi vale per basso e comping insieme alla batteria, e il template porta le
posizioni di un batterista **che stava già swingando**, lo swing finisce
applicato due volte.

**La spartizione decisa:**

| chi | cosa fa |
|---|---|
| `set_swing()` | lo swing, per tutta la song — batteria, basso e comping insieme |
| il groove template | **solo il residuo**: il ride che spinge rispetto al rullante che tiene indietro |

Quindi `profilo()` misura il BUR dell'esecuzione e **lo toglie**. Quel BUR non
è materiale di scarto: è il **controllo indipendente** sull'1,61 misurato sulla
Weimar — due corpora, due metodi, la stessa domanda. Se divergono è una cosa da
sapere prima di scrivere un pezzo. La casella 4 esiste per ospitare quel
confronto.

---

## 5. Cosa dice la documentazione del Deluge

Cercato nell'ordine della regola 0 (community → guidebook → sorgente → file).

**Il poliritmo non è una divisione in terzine, è lunghezza di riga più numero
di eventi.** Dal 4.0: *«set the length of a row, dial in how many steps you
would like to play on that row (automatically divided 'musically')»*. Sul
dispositivo sono due gesti — `AUDITION` + gira `◄►` per la lunghezza,
`AUDITION` + premi e gira `▼▲` per il numero di eventi euclidei — e nell'XML la
prima è l'attributo `length` sulla `<noteRow>` che `HANDOFF.md` §7 ha già
osservato in 197 righe e **mai verificato sul dispositivo**.

⚠️ **Serve per i tempi dispari, non per lo swing.** Il jazz è quasi sempre
scritto in metro binario con swing, e lì il meccanismo è `set_swing()`. I
tuplet servono ai tempi in 3, 5, 7. Le due cose non vanno confuse, ed è la
ragione per cui questo progetto **non** tocca `length` di `<noteRow>`.

**La risoluzione minima di nudge è il 384esimo, cioè un tick.** Dal manuale
community: *«This will nudge at the song's minimum resolution, default is 384th
notes»*. Un 384esimo di semibreve su 96 tick per movimento **è un tick**. Il
Deluge sposta le note un tick alla volta dalla sua interfaccia: le posizioni
fuori griglia sono la granularità nativa del gesto, non un abuso del formato.

Concorda coi file. Su 146 song del corpus, 27 840 note:

| | note | |
|---|---|---|
| sulla griglia di 1/16 | 18 635 | 66,9% |
| fuori | 9 205 | 33,1% |

Ma gli scarti fuori griglia sono quasi tutti **griglie più fini**: 7 018 a 12
tick (1/32), 1 903 a 6 e 18 (1/64). Le posizioni davvero irregolari sono poche
centinaia, sotto l'1%. Quindi le posizioni arbitrarie sono rappresentabili e il
corpus ne contiene — ma **un groove umano sarebbe il primo materiale a usarle
davvero**, ed è per questo che il cancello del §9 esiste.

**Due cose trovate per strada, da scrivere nelle schede:**

- esiste già un **quantize/humanize sul dispositivo**, `AUDITION` + `TEMPO`,
  orario quantizza e antiorario umanizza, **per riga e distruttivo**. È il
  concorrente diretto del template, con la differenza che quello randomizza e
  questo misura. Chi lo gira cancella il template senza saperlo;
- la **direzione di riproduzione è per riga** (`FORWard`/`REVErse`/`PINGpong`),
  cioè il `sequenceDirection` già visto nei file come fratello di `length`.

---

## 6. L'architettura

Ricalca il precedente collaudato: `wjazz.py` legge un corpus e non tocca mai un
`Document`; i verbi che scrivono stanno in `musica.py`.

### `tools/delugexml/groove.py` — legge, non scrive

Riceve la radice del dataset come argomento, esattamente come `WJ` riceve il
percorso del `.db`, così i test saltano quando `to-read/` non c'è. **Non tocca
mai un `Document`**: è quello il confine, non l'elenco degli import. Riusa
`MI.leggi()` e `MI.GM_PERCUSSIONI` — **nessun secondo vocabolario di nomi di
percussione** — e `musica` per il vocabolario comune, come già fa `wjazz.py`.

⚠️ **L'aritmetica del BUR è già scritta, e sta nel posto sbagliato per due
lettori.** `in_bur()` — `BUR = p / (1 − p)`, 0,5 dritto e 0,667 terzina — vive
oggi in `wjazz.py:497`. `groove.py` ha bisogno della stessa conversione, e le
alternative sono tre: duplicarla (vietato), far dipendere un lettore di corpus
dall'altro (assurdo: sono corpora diversi), o **promuoverla in `musica.py`**,
che è il vocabolario musicale comune che `wjazz.py` già importa. Si promuove.
È il primo compito del piano proprio perché tocca codice che funziona: va
fatto quando i test esistenti possono ancora dire se si è rotto qualcosa.

| per | funzione |
|---|---|
| cercare | `GR.elenco(base, style='jazz', beat_type='beat')` — per **prefisso** |
| quali etichette esistono | `GR.valori(base, 'style')` |
| vedere cosa c'è | `GR.racconta(base, id)` |
| la scala di velocity | `GR.scala(base, style='jazz')` → per strumento: mediana, quartili, **e quante esecuzioni e quanti batteristi** |
| quanto swinga | `GR.swing(base, style='jazz')` → BUR per esecuzione e aggregato |
| il template | `GR.profilo(base, id)` → per strumento e per passo: velocity mediana, scarto **residuo**, e quante volte quel passo è stato colpito |
| il microtiming aggregato | `GR.microtiming(base, style=…)` |

**La catena dentro `profilo()`, e l'ordine è la cosa che conta:**

1. leggi il MIDI con `MI.leggi()`;
2. **togli l'origine della griglia** (§3);
3. **misura il BUR** dell'esecuzione e **toglilo** (§4);
4. quel che resta è lo **scarto residuo**;
5. aggrega per strumento e per **passo della battuta**.

`id` è la colonna omonima di `info.csv` (`drummer1/session3/2`), che identifica
l'esecuzione senza passare per il nome del file. I passi sono **sedici per
battuta**, la stessa griglia che la casella 2 del jazz dichiara e che
`MU.passi()` usa: il template dev'essere applicabile a ciò che quella funzione
produce, quindi la griglia della misura e quella della scrittura sono la stessa
per costruzione.

Ogni numero che esce da `scala()` porta con sé il conteggio dei **batteristi**,
perché è quello che decide fra `[MIS]` e `[OSS]` — e sul reggae la funzione
stessa impedisce di sbagliare marcatore.

### `musica.py` — `MU.applica_groove(note, profilo, dove=…)`

Prende ciò che esce da `MU.passi()` e ci posa sopra il profilo: per ogni nota
trova il suo passo, ci mette la velocity misurata e sposta la posizione dello
scarto residuo. Il pattern resta la stringa leggibile che è; il feel arriva da
un'esecuzione vera.

⚠️ **Il template viene da UNA esecuzione nominata**, dichiarata con batterista,
stile e BPM — non dalla media di un sottoinsieme. Mediare il microtiming di
batteristi diversi lo tira verso zero, cioè verso la griglia: si perderebbe
esattamente ciò che si è andati a prendere. Quello che ne esce è perciò `[OSS]`
su quell'esecuzione, mentre la **scala** di `scala()` è `[MIS]` sull'aggregato:
due marcatori diversi perché sono due affermazioni diverse.

⚠️ **Se il pattern chiede un colpo su un passo dove quel batterista non ha mai
suonato, la funzione non inventa una velocity: lo dice e lascia la nota com'è.**
È lo stesso cancello della sigla sconosciuta in `MU.armonia()`. Un template che
riempie i buchi da sé sarebbe di nuovo inventare con la benedizione di una riga
scritta per impedirlo.

---

## 7. Dove finiscono i numeri

**`docs/repertori/jazz.md`.** La 6 prende la scala di velocity per strumento,
il profilo posizionale, il microtiming residuo e la delimitazione degli
`style`. La 4 prende il BUR del Groove MIDI accanto a quello di Weimar — il
numero è **nuovo** e il feel è la sua casella, quindi la 6 ci **rimanda** e non
lo copia. La 9 prende i fill. La 10 prende come si scrive un template, che
`AUDITION`+`TEMPO` lo cancella, e che `length` di `<noteRow>` è un meccanismo
altro e non verificato.

**`docs/repertori/reggae-dub.md`.** La 6 corregge la propria agenda: il conteggio
vero, e che resta `[WEB]` (§2).

**`docs/MUSICA.md`.** La scala `[WEB]` dei cinque livelli nel comune **resta
dov'è** — vale per tutti i generi ed è quello che c'è quando un repertorio non
ha misure sue — con accanto un rimando alla 6 del jazz, **mai una copia dei
numeri**. Nel comune, «La macchina», entrano le due cose di macchina che valgono
per chiunque: il groove template e il quantize/humanize del dispositivo.
Nell'indice: **jazz 6 da ○ a ●, jazz 9 da ○ a ◐**.

**`SKILL.md`.** `GR` nella tabella delle importazioni e una riga sotto
«Importare MIDI», dove i groove template sono nominati da sempre senza esistere.

**`HANDOFF.md`.** Una 6-terdecies con ciò che è costato: l'origine della
griglia, il doppio swing, e il reggae che il corpus non regge.

---

## 8. I test

Saltano senza `to-read/`, come quelli di `wjazz`. Quattro sono gli invarianti
veri, e **due si provano su file MIDI sintetici** invece che sul corpus, così
girano sempre:

| invariante | come |
|---|---|
| prefisso, non sottostringa | `elenco(style='reggae')` non prende `latin/reggaeton` |
| l'origine della griglia si toglie per intero | MIDI sintetico con scarto noto |
| il residuo è ciò che resta dopo lo swing | MIDI sintetico con swing noto: `GR.swing()` lo ritrova, il residuo torna zero |
| il rifiuto | `applica_groove()` su un passo senza appoggio non inventa, e lo dice |

Il test che tiene allineati indice e schede esiste già e vede da sé le caselle
che cambiano stato. Conteggio atteso: da **859** a circa **880**.

---

## 9. Il cancello sul dispositivo

Una coppia controllata, **una clip di sola batteria**, non un pezzo jazz — che
oggi avrebbe sette caselle vuote sotto e verrebbe scritto in gran parte su
ripieghi.

1. stessa clip due volte: `GROOVE0` senza template, `GROOVE1` con;
2. `put` di entrambe, riscarica, confronto attributo per attributo — dice solo
   che il giro è pulito;
3. **la parte che decide**: l'utente apre `GROOVE1` sul Deluge, la **risalva**,
   e la si riscarica. Se le posizioni tornano sulla griglia, il Deluge
   riquantizza e il template va ripensato. È l'unica prova che risponde, perché
   un file mai passato dal salvataggio del dispositivo non ha dimostrato niente;
4. l'ascolto: le due clip a confronto, e l'utente dice se il residuo si sente o
   se sta sotto la soglia.

⚠️ **Se il punto 3 va male, cade solo lo scarto di posizione.** La misura, la
scala di velocity e il confronto BUR restano validi. È il rischio vero del
progetto ed è dichiarato in partenza, non scoperto alla fine.

---

## 10. Cosa NON è in questo progetto

- **non si tocca `length` di `<noteRow>`** né il poliritmo: è un meccanismo
  altro, per i tempi dispari, e ha un suo punto aperto in `HANDOFF.md` §7;
- **non si genera un pezzo jazz.** Riempirebbe la casella 11, ma con le caselle
  1, 2, 5, 8 e 9 vuote la correzione dell'ascolto colpirebbe i ripieghi invece
  del template;
- **non si estende `midi.py`.** È il lettore generico validato contro `mido`; le
  etichette di un dataset non sono roba di MIDI;
- **non si scrive uno scarto per passo a mano** in `MU.passi()`: sposterebbe sul
  chiamante il compito di inventare i numeri;
- **non si mediano i microtiming** fra batteristi (§6).

---

## 11. Rischi dichiarati

| rischio | cosa succede | contromisura |
|---|---|---|
| il Deluge riquantizza al salvataggio | cade lo scarto di posizione | §9 punto 3, e il resto del lavoro regge |
| il residuo sta sotto la soglia dell'udibile | il template porta solo la velocity | §9 punto 4 lo dice per ascolto, non per aritmetica |
| il BUR del Groove MIDI diverge da Weimar | non si sa quale credere | si scrivono **entrambi** nella casella 4, coi due metodi |
| `drummer1` domina il jazz | la «scala» è più di lui che del jazz | il conteggio dei batteristi sta accanto a ogni numero |
