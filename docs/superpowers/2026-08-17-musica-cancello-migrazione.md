> **Perché questo file è qui.** È il verbale del cancello della rifondazione di
> `docs/MUSICA.md` sullo schema neutro (17 agosto 2026): il vecchio documento,
> 745 righe cresciute attorno al solo reggae, è stato smontato e ridistribuito
> fra `docs/MUSICA.md` (schema, comune, indice) e le schede in
> `docs/repertori/`. La regola era **le frasi si spostano come sono**, e questo
> documento è la prova che è stata rispettata: le 45 righe che uno strumento
> di confronto aveva segnalato come non atterrate, istruite una per una. **Una
> sola era contenuto vero perduto**, ed è stata rimessa.
>
> Il progetto e il piano stanno in `specs/2026-08-17-musica-schema-neutro-design.md`
> e `plans/2026-08-17-musica-schema-neutro.md`. Nato come artefatto di lavoro,
> conservato qui perché è l'unica prova che la migrazione non ha perso niente.

# Task 7 — il cancello: le 45 ORFANE istruite una per una

**Stato:** DONE.
**Commit:** `9feaf1c` — *musica: la sola orfana che era contenuto, rimessa nel
comune*. Un file solo, `docs/MUSICA.md`, +4 righe.
**Suite:** `python tests/test_all.py` → **858/858 test superati**, `FAIL: 0`,
exit code 0. Era 858/858 dopo il Task 6, ed è 858/858 adesso.
**Rete di sicurezza:** ORFANE **45**, DOPPIE **15** — invariate prima e dopo.

Conteggio finale dell'istruttoria. Le sette etichette sono descrittive; il
brief ne ammette **due**, e la riduzione dell'una all'altro è al §0.1.

| esito | quante | esito del brief |
|---|---|---|
| raccordo riscritto, o titolo/transizione sciolti dalla rifondazione | 9 | 1 |
| indirizzo tipografico corretto **di proposito** (Task 3 e 4, e questo) | 4 | 1 |
| riga re-impaginata: parole tutte atterrate, provato sul testo appiattito | 6 | 1 |
| seam — due caselle che si toccano dentro la stessa riga sorgente | 2 | 1 |
| contenuto atterrato, ma con la riga riscritta per vincolo del brief | 8 | 2 |
| contenuto che per **regola dello schema** vive fuori dai tre file | 15 | 2 |
| **contenuto vero, rimesso in una casella** | **1** | 2 |
| non istruite | **0** | — |

**Totale 45.** I conteggi sono ricavati contando le etichette riga per riga
nelle tabelle del §1, non stimati: **9 + 4 + 6 + 2 + 8 + 15 + 1 = 45**.

**Nessuna riga è rimasta senza casella.** Lo schema non ha dovuto essere messo
in discussione.

### 0.1 La riduzione ai due esiti che il brief ammette

Il brief ammette **due** esiti e nessun terzo. Le sette etichette qui sopra
sono una classificazione più fine, utile a chi contesterà una riga singola, e
si riducono ai due senza residuo:

- **«è una riga di raccordo riscritta» — 21 righe.** Ci cadono i raccordi veri
  (9), gli indirizzi tipografici corretti di proposito (4), le
  re-impaginazioni (6) e i due seam. Gli indirizzi e i seam ci stanno di
  diritto e non per comodità: il brief nomina esplicitamente «un indirizzo
  tipografico ormai falso ("in fondo alla sezione", "qui sopra")» e «una riga
  re-impaginata di cui le parole sono tutte atterrate», e un seam è una riga
  che risulta orfana **solo** perché un a capo sorgente cade in mezzo a due
  frasi di due caselle diverse — cioè il caso limite della re-impaginazione.
- **«è contenuto» — 24 righe.** Ci cadono le 8 righe della tabella di
  conversione (contenuto atterrato, riga riscritta per un vincolo esplicito del
  brief del Task 5), le 15 di «come si è stabilito» che vivono fuori dai tre
  file per regola dello schema, e **la sola riga che ho dovuto rimettere io**.
  Di queste 24, ventitré erano **già nella casella che gli compete** quando
  sono arrivato: per quelle il secondo esito era già stato eseguito, e il mio
  lavoro è stato verificarlo. Una no, e l'ho eseguito (§2).

21 + 24 = 45. **Non esiste una terza pila**, e nessuna riga è stata archiviata
in una categoria che significhi «non so dove metterla».

---

## 0. Come ho istruito, e perché non mi sono fidato dell'occhio

Lo strumento confronta la **riga sorgente esatta**. Una riga con l'a capo
spostato risulta ORFANA anche se ogni parola è atterrata, e in quella sola
direzione può sbagliare. Quindi ogni volta che questo rapporto dice
«re-impaginata», dietro c'è una misura e non un giudizio: lo script
`$SCRATCH/istruttoria.py` appiattisce ogni sequenza di spazi (`re.sub(r'\s+',
' ')`) nei tre file nuovi e nella riga vecchia, e cerca la **sequenza di
parole**. Classifica in quattro modi:

- `ATTERRATA-INTERA` — la sequenza di parole c'è tutta in un file nuovo;
- `ATTERRATA-SPEZZATA` — un prefisso e un suffisso che insieme coprono la riga
  stanno in due posti diversi (è la firma di un *seam*);
- `PARZIALE` — solo una testa o una coda;
- `PERSA` — nemmeno quattro parole di fila.

Su questo si è poi innestato un secondo controllo, che è quello che conta
davvero per «non si è perso niente»: estrae da ogni riga ORFANA ogni **token
duro** e dice dove sia finito. Il metodo, dichiarato perché sia rifacibile:

- **cosa è un token duro** — `\d+[,.]\d+`, `\d+%`, `\d+`, oppure una sigla
  `[A-Z]{4,}[0-9]*`, oppure un `nome.funzione()`;
- **come si cerca** — con **confini veri**, non per sottostringa: davanti e
  dietro a un numero non devono esserci cifra, virgola o punto (altrimenti `1`
  combacia dentro `1,61`, `106` e `2026`, che è il difetto della prima
  stesura); attorno a una sigla, nessun carattere di parola;
- **su quali file** — sei: i tre nuovi, più `FINDINGS.md`, `ARCHITETTURA.md` e
  **`HANDOFF.md`**. Il perimetro a sei file è la correzione più importante
  della revisione: la prima stesura ne guardava quattro e sbagliava per questo
  una conclusione (§4.1).

Tutte le letture passano `encoding='utf-8'` esplicito. Lo script è
`$SCRATCH/audit_stretto.py`.

**Esito: due soli token assenti da tutti e sei i file, `1,00` e `2,00`, ed è
una notazione, non una perdita** — sono i BUR del dritto e della terzina, e in
`jazz.md:49` stanno scritti «1 dritto, 2 terzina». Ogni altro numero, sigla e
nome di funzione delle 45 righe è stato ritrovato.

---

## 1. Le 45 ORFANE, una per una

Le righe sono di `94c52d8:docs/MUSICA.md`. La colonna «esito» usa le sette
etichette della tabella in testa.

### Gruppo A — la testa del file (righe 4, 5)

| riga | testo | esito |
|---|---|---|
| 4 | `le skill (vedi sotto). Qui sta solo ciò che è stato imparato correggendo` | **indirizzo corretto di proposito** |
| 5 | `il lavoro, e che nessuna skill generica sa.` | **re-impaginata** |

La riga 5 risulta `ATTERRATA-INTERA` in `MUSICA.md`: è una falsa orfana pura,
trascinata dall'a capo della riga sopra. La riga 4 è il Minor 1 della revisione
del Task 3: «vedi **sotto**» puntava a una tabella che stava due righe più giù
e che ora sta a riga 186, oltre tutto lo schema. Sostituito con «vedi «Le due
skill, e chi comanda su cosa», nel comune». Le nove parole restanti della riga
(«Qui sta solo ciò che è stato imparato correggendo») sono in `MUSICA.md:4-5`,
verificate sul testo appiattito. **Nessuna perdita: un puntatore aggiustato.**

### Gruppo B — il rimando morto alla sezione dissolta (righe 25, 26)

| riga | testo | esito |
|---|---|---|
| 25 | `Il posto dove la skill grande vale davvero è **quello che questo file non` | **raccordo** |
| 26 | `copriva affatto**: vedi «Quello che una griglia di una battuta non dice».` | **raccordo** |

Due righe, due metà. La metà che **punta** («vedi «Quello che una griglia di
una battuta non dice»») è un indirizzo a una sezione che la rifondazione ha
sciolto nei blocchi 7-11 del comune: tenerla com'era vorrebbe dire un rimando
nel vuoto. La metà che **afferma** — dove `music-composition` vale davvero — è
già altrove, e non per parafrasi: la terza colonna della tabella delle skill,
spostata verbatim, dice *«il **mestiere**: forma, sviluppo motivico, densità,
transizioni, protocollo di revisione»* (`MUSICA.md:186`). È la stessa
affermazione, scritta prima e meglio, nella stessa pagina. E la clausola «che
questo file non copriva affatto» era vera del vecchio file e non lo è più: la
parte «il mestiere» del comune *è* quella copertura.

### Gruppo C — i tre indirizzi corretti dal Task 4 (righe 147, 151, 609)

| riga | testo | esito |
|---|---|---|
| 147 | `> sbagliata (verificato il 17 agosto 2026, dettaglio in testa al file).` | **indirizzo corretto di proposito** |
| 151 | `> sezione). Non è ancora stato validato dall'ascolto dell'utente: DUBPAL01,` | **indirizzo corretto di proposito** |
| 609 | `⚠️ [WEB/skill] L'arco qui sopra non è misurato su niente: è la forma standard` | **indirizzo corretto di proposito** |

Sono i rilievi R4, R6 e R7 della revisione del Task 4, e sono esattamente le
tre righe che quel rapporto dichiara di aver mosso (`105 → 108`, «nuove: [147,
151, 609]»). Verificate una per una nel file nuovo:

- 147: «dettaglio in testa al file» → «dettaglio **qui sopra**»
  (`reggae-dub.md:333`). Il dettaglio — la trappola dello skank — nella vecchia
  impaginazione stava in testa al file; ora sta nella stessa casella 11, sopra.
  L'indirizzo vecchio era diventato falso.
- 151: «fonti in fondo alla **sezione**» → «alla **scheda**»
  (`reggae-dub.md:11-12`). Non è più una sezione, è un file.
- 609: «L'arco qui **sopra**» → «qui **sotto**» (`reggae-dub.md:241`), perché
  R7 ha spostato il blocco `⚠️` *sopra* l'arco. Senza la correzione lo
  spostamento avrebbe prodotto il difetto stesso che R4 chiede di smettere di
  produrre.

Il token `DUBPAL01` della riga 151 è in `MUSICA.md` e in `reggae-dub.md`; il
`17`/`2026` della 147 in tutti e tre. Nessuna parola persa: solo l'indirizzo.

### Gruppo D — i due seam, e la coda del seam 655 (righe 159, 655, 656, 657)

| riga | testo | esito |
|---|---|---|
| 159 | `libero. Griglia a 16 passi per battuta, come MU.passi():` | **seam** |
| 655 | `drop — ma nel file sembrava un caso. **Scritta, diventa una cosa da tenere o da` | **seam** |
| 656 | `cambiare di proposito**; non scritta, è una cosa che si rompe senza accorgersene` | **re-impaginata** |
| 657 | `appena si tocca una delle due righe.` | **re-impaginata** |

Le righe 159 e 655 sono i due punti del vecchio file in cui **una frase di una
casella e una frase di un'altra si toccano dentro la stessa riga sorgente**.
Non si possono spostare intere senza portare in una casella materiale
dell'altra, quindi non possono che risultare ORFANE. Il mio controllo le trova
`ATTERRATA-SPEZZATA`, che è la firma esatta di un seam:

- 159: prefisso `libero.` in `reggae-dub.md:97` (casella 5); suffisso `Griglia
  a 16 passi per battuta, come MU.passi():` in `reggae-dub.md:44` (casella 2).
  1 + 8 = 9 parole su 9.
- 655: prefisso `drop — ma nel file sembrava un caso.` in `reggae-dub.md:152-153`
  (casella 5); suffisso `**Scritta, diventa una cosa da tenere o da` in
  `MUSICA.md` (comune, «Cassa e basso sono una coppia»). 8 + 8 = 16 su 16.

Le righe 656 e 657 sono la coda della frase generale del 655, che il Task 3 ha
rimesso nel comune **verbatim ma ri-mandata a capo** (perché nel vecchio
cominciava a metà riga). Il mio controllo le trova tutt'e due
`ATTERRATA-INTERA` in `MUSICA.md`: falsa orfana confermata, non ereditata.

### Gruppo E — la vecchia scala dello swing (righe 314, 315, 316)

| riga | testo | esito |
|---|---|---|
| 314 | `Lo **swing** si fa con lo swing di song, e la sua scala è documentata` | **contenuto, fuori dai tre file per regola dello schema** |
| 315 | `(FINDINGS §6): il display va **0-100 con 50 = dritto**, e nel file è un valore` | idem |
| 316 | `con segno centrato sullo zero.` | idem |

Questo è il gruppo su cui ho voluto la prova più dura, perché il Task 4 lo
liquida come «rinuncia deliberata» e la rinuncia è una parola che va
verificata. Le tre righe dicono tre cose:

1. *lo swing si fa con lo swing di song* — le prime otto parole sono in
   `reggae-dub.md:80` (**«Lo **swing** si fa con lo swing di song.»**),
   verificate sul testo appiattito;
2. *il display va 0-100 con 50 = dritto* — nel comune, `MUSICA.md:535-544`:
   «Il display di `set_swing()` **è** la percentuale di posizione del levare» e
   «**50 è dritto**, **67 è la terzina**, e sotto 50 il levare arriva *in
   anticipo*», più la formula `display = 100 × BUR / (BUR + 1)`. Il fatto c'è,
   con in più la formula che lo genera;
3. *nel file è un valore con segno centrato sullo zero* — **questa non è in
   nessuno dei tre file**, e ho verificato che sia esattamente dove il vecchio
   testo dice di andarla a cercare. `docs/FINDINGS.md`, sottosezione «Lo swing:
   il file usa una scala, il display un'altra», la porta parola per parola:
   *«Il display usa **0-100 con 50 al centro**; il file usa un valore **con
   segno centrato sullo zero**»*, con la conversione `display = swingAmount +
   50` e il range osservato nel corpus.

Il rimando che ci manda non è implicito: `MUSICA.md:576-581` nomina la
sottosezione per titolo e dice a cosa serve. È esattamente la divisione che il
comune stesso stabilisce a riga 43-45 — *«come si è misurato non sta qui
affatto: sta in `FINDINGS.md` e in `ARCHITETTURA.md`. Lì c'è come si è
misurato, qui come si usa»*. Ricopiare la rappresentazione interna del file
nella pagina d'uso sarebbe stato violare quella regola, non rispettarla.

### Gruppo F — l'intestazione del catalogo per genere (righe 360, 361)

| riga | testo | esito |
|---|---|---|
| 360 | `Catalogo che cresce. Griglia a 16 passi = una battuta, direttamente` | **raccordo + contenuto già atterrato** |
| 361 | `incollabile in MU.passi().` | idem |

Due frasi. «Catalogo che cresce» è il cappello della sezione «Pattern tipici
per genere», cioè di un catalogo *fra* generi che lo schema neutro ha sciolto
di proposito: i pattern di un repertorio stanno nella casella 6 di quel
repertorio, e un catalogo unico è precisamente la forma che la rifondazione
smonta. Non ha una casella perché non deve averla.

La seconda frase è invece un fatto — griglia a 16 passi = una battuta,
incollabile in `MU.passi()` — ed è atterrata: `reggae-dub.md:44`, «Griglia a 16
passi per battuta, come `MU.passi()`:», che è la metà destra della riga 159.
L'audit dei token conferma `MU.passi()` presente in `reggae-dub.md` e `16` in
tutti e tre.

### Gruppo G — la tabella di conversione BUR → display (righe 519, 521, 523-529)

| riga | testo | esito |
|---|---|---|
| 519 | `Quindi la tabella qui sopra diventa scrivibile:` | **raccordo, indirizzo morto** |
| 521 | `\| repertorio \| BUR \| set_swing(doc, …, figura='1/8') \|` | **contenuto atterrato, riga riscritta per vincolo** |
| 523 | `\| dritto \| 1,00 \| 50 \|` | idem |
| 524 | `\| **jazz complessivo** \| 1,61 \| **62** \|` | idem |
| 525 | `\| HARDBOP \| 1,80 \| 64 \|` | idem |
| 526 | `\| BEBOP \| 1,75 \| 64 \|` | idem |
| 527 | `\| POSTBOP \| 1,49 \| 60 \|` | idem |
| 528 | `\| FUSION \| 1,26 \| 56 \|` | idem |
| 529 | `\| terzina esatta \| 2,00 \| 67 \|` | idem |

Nove righe orfane **per costruzione**: il brief del Task 5 impone che la
tabella nella casella 10 del jazz **non abbia la colonna BUR** (i BUR vivono
nella casella 4), quindi ogni riga cambia testo e lo strumento, che confronta
la riga sorgente, non può che segnalarle tutte e nove.

Non ho ereditato il giudizio: ho seguito **ogni singolo valore**.

| valore del vecchio | dove sta ora | verificato |
|---|---|---|
| BUR 1,61 | `jazz.md:51` «Complessivo: levare al 61,7%, **BUR 1,61**» | audit token → `jazz.md` |
| BUR 1,80 · 1,75 · 1,49 · 1,26 | `jazz.md:60, 61, 65, 67`, tabella «Per stile» | audit token → `jazz.md` |
| BUR 1,00 e 2,00 | `jazz.md:49` «In BUR …: **1 dritto, 2 terzina**» | notazione diversa, valore identico |
| display 50 · 62 · 64 · 60 · 56 · 67 | `jazz.md:191-196`, tabella della casella 10 | audit token, tutti e sei |
| HARDBOP · BEBOP · POSTBOP · FUSION | `jazz.md`, tabella per stile e tabella della 10 | audit token → `jazz.md` |

Le righe 525 e 526 sono fuse in una — `| HARDBOP · BEBOP | 64 |` — perché nel
vecchio davano lo stesso display; nessuno dei due nomi né il 64 si è perso.

La riga 519, «Quindi la tabella **qui sopra** diventa scrivibile», è per giunta
un indirizzo morto due volte: «la tabella qui sopra» era quella di
`swingInterval`, che ora sta in un altro file. `jazz.md:186-187` la sostituisce
con un rimando che nomina la destinazione invece di indicare col dito — «Qui ci
sono i valori del jazz, **convertiti dai BUR della casella 4**».

### Gruppo H — «come ho sbagliato la tabella la prima volta» (righe 533-538, 544-546, 548-550)

| riga | testo (troncato) | esito |
|---|---|---|
| 533 | `⚠️ La prima versione diceva **intervallo 5, «4th notes»** — spostata di un` | **contenuto, in `FINDINGS.md` + `HANDOFF.md`** |
| 534 | `posto. L'osservazione a cinque punti (etichetta ↔ numero nel file) era` | idem |
| 535 | `giusta; sopra ci avevo appiccicato l'aritmetica del sorgente` | idem |
| 536 | `` `3 << (10 − swingInterval)`, che dà un blocco lungo **la metà** di quello `` | idem |
| 537 | `vero, e ne era uscita la conclusione controintuitiva «l'etichetta nomina il` | idem |
| 538 | `blocco, non la figura». L'ho pure difesa.` | idem |
| 544 | `> **La lezione:** avevo misurato la cosa giusta e dedotto quella sbagliata.` | idem |
| 545 | `> La misura diceva solo «etichetta ↔ numero»; il significato musicale non era` | idem |
| 546 | `> misurato, era **inferito** — e l'ho trattato come se avesse lo stesso peso.` | idem |
| 548 | `Lo scarto col sorgente resta ignoto ed è dichiarato in` | idem |
| 549 | `` `song.SWING_SCARTO_SORGENTE`: i "swung tick" di quel codice non sono i tick `` | idem |
| 550 | `delle posizioni di nota, e dove si convertano non è stato trovato.` | idem |

Il Task 3 (§5.1) e il Task 5 sostengono che questo blocco stia in `FINDINGS.md`
§6 «praticamente parola per parola». **L'ho controllato invece di crederci** —
ma la prima stesura di questo rapporto ha controllato in un perimetro troppo
stretto, e va detto: **il blocco vive in due file, non in uno.**
`HANDOFF.md:1042-1065`, «Errore 2: misurato giusto, dedotto sbagliato», lo
porta quasi verbatim ed è **la fonte più letterale delle due**; `FINDINGS.md`
§6 lo porta in forma riassunta dentro il blockquote «Come è stato sbagliato, la
prima volta». Le due si coprono a vicenda, ma non nella stessa misura, e il
conto l'ho fatto invece di stimarlo: `$SCRATCH/gruppo_h.py` cerca per ogni riga
il più lungo n-gram contiguo presente in ciascuna fonte.

**Sette delle dodici righe — 534, 535, 536, 537, 545, 546, 548 — hanno
sequenze di parole che sopravvivono solo in `HANDOFF.md`** (soglia: quattro
parole contigue). Tre — 544, 549, 550 — stanno in tutt'e due. Due — 533 e 538 —
non raggiungono le quattro parole contigue in nessuna fonte, e va detto perché:
non è contenuto mancante ma **punteggiatura**. La 538 finisce «blocco, non la
figura». L'ho pure difesa.» e `HANDOFF.md:1049` scrive «blocco, non la
figura», e l'avevo pure difesa.» — stessa frase, virgola al posto del punto,
che rompe l'n-gram e non il senso. La 533 porta i marcatori `**` e le
virgolette basse attorno a «4th notes», e `HANDOFF.md:1044-1045` dice la stessa
cosa senza. **Il contenuto di tutt'e due è coperto**; è la misura per n-gram a
non vederlo, ed è lo stesso limite dello strumento principale.

*(La prima stesura di questo paragrafo diceva «sette righe» ma ne elencava
nove, e una delle nove — la 541 — non è nemmeno del Gruppo H: è la citazione
dell'utente, Gruppo I. L'elenco qui sopra è ricavato dallo script.)*

Ogni affermazione, messa a fronte:

| affermazione del vecchio | `FINDINGS.md` §6 | `HANDOFF.md` 1042-1065 |
|---|---|---|
| la prima tabella era spostata di un posto, intervallo 5 per le crome | «La tabella era uscita spostata di un posto (intervallo 5 per le crome)» | «era uscita **spostata di un posto** (intervallo 5 per le crome)» |
| l'osservazione a cinque punti era giusta, l'aritmetica ci era stata sovrapposta | «all'osservazione a cinque punti — che era giusta — era stata sovrapposta quell'aritmetica» | «L'osservazione a cinque punti … era giusta; sopra ci avevo sovrapposto l'aritmetica del sorgente» — **quasi la riga 534-535 alla lettera** |
| `3 << (10 − swingInterval)` dà un blocco lungo la metà | «48 tick, una croma — mentre l'orecchio dice … 96 tick», «di un fattore esatto 2» | «`3 << (10 − swingInterval)`, che dà un blocco lungo **la metà** di quello vero» — **la riga 536 alla lettera** |
| ne usciva «l'etichetta nomina il blocco, non la figura» | «Ne usciva «l'etichetta nomina il blocco», controintuitivo e falso» | «Ne era uscita la conclusione controintuitiva «l'etichetta nomina il blocco, non la figura»» |
| **e l'avevo pure difesa** | *(assente)* | **`HANDOFF.md:1049`**, e di nuovo a **`:1221`** |
| la lezione: misurata la cosa giusta, dedotta quella sbagliata | «**Avevo misurato la cosa giusta e dedotto quella sbagliata**» | idem, riga 1055 |
| la misura copriva solo «etichetta ↔ numero», il senso musicale era inferito e pesato uguale | «la misura copriva solo «etichetta ↔ numero nel file» … trattata come se pesasse quanto la misura» | righe 1056-1057, con in più «è una variante nuova dell'errore di sempre» |
| lo scarto col sorgente è ignoto, dichiarato in `song.SWING_SCARTO_SORGENTE` | «I "swung tick" … **non sono** i tick delle posizioni di nota, e il punto in cui i due si convertono non è stato trovato. Dichiarato in `song.SWING_SCARTO_SORGENTE`» | `HANDOFF.md:1062-1064`: «Lo scarto col sorgente resta **ignoto** ed è dichiarato in `song.SWING_SCARTO_SORGENTE`: i "swung tick" di quel codice non sono i tick delle posizioni di nota, e dove si convertano non è stato trovato» — **le righe 548-550 alla lettera** |

**Dodici righe su dodici sono coperte.** È materiale di **«come si è
stabilito»**, che la regola in testa a `MUSICA.md` manda esplicitamente fuori
dalla pagina d'uso, e il comune ce lo rimanda per titolo di sottosezione. Non è
una casella dello schema perché **non deve esserlo**: è il caso di scuola della
divisione fra i documenti.

### Gruppo I — la frase dell'utente sull'ascolto (righe 540, 541, 542)

| riga | testo | esito |
|---|---|---|
| 540 | `L'ha smontata l'utente ascoltando: *«con 8th sento il primo ottavo dritto e` | **re-impaginata** |
| 541 | `il secondo swingato»* — una frase che descrive la **coppia**, e la coppia è` | **re-impaginata** |
| 542 | `fatta della figura nominata. Nessuna aritmetica poteva sostituirla.` | **raccordo** |

Questa è la riga a rischio vero di tutta la migrazione — è l'unica **citazione
testuale dell'utente** del capitolo dello swing, e `FINDINGS.md` la riassume
senza riportarla. È salva, verbatim, in `MUSICA.md:573-575`:

> Che l'etichetta nomini la **figura** e non il blocco l'ha stabilito
> l'ascolto dell'utente — *«con 8th sento il primo ottavo dritto e il secondo
> swingato»*, una frase che descrive la coppia, e la coppia è fatta della
> figura nominata.

Le tre righe sorgente risultano ORFANE perché l'attacco è cambiato: il vecchio
540 comincia con «L'ha smontata», e quel pronome punta alla tabella sbagliata
della prima volta, che nel comune non c'è. Riformulare l'attacco era obbligato;
la citazione e la frase che la spiega sono passate intatte. Resta fuori solo
«Nessuna aritmetica poteva sostituirla», che è la chiusa retorica della stessa
affermazione — il suo contenuto *è* «l'ha stabilito l'ascolto».

### Gruppo J — il cappello della scala lunga (righe 554, 555, 557, 558)

| riga | testo | esito |
|---|---|---|
| 554 | `Rileggendo questa pagina alla luce di music-composition è venuta fuori una` | **raccordo** |
| 555 | `cosa che non è un dettaglio mancante ma **un piano intero mancante**:` | **raccordo** |
| 557 | `> Tutto ciò che c'è scritto sopra descrive **una battuta**. Un pezzo ne dura` | **raccordo + contenuto atterrato** |
| 558 | `> centoventi.` | **re-impaginata** |

554-555 sono il cappello che introduce la citazione: parlano di «questa pagina»
e del momento in cui la mancanza è stata notata. La cosa che annunciano — che
manca un piano intero, non un dettaglio — nello schema neutro non è più una
notizia da dare in prosa: **è la ragione per cui la casella 9 esiste**, ed è
scritta come tale in `MUSICA.md:122-130`.

La riga 557 ha due metà. «Tutto ciò che c'è scritto **sopra**» è un indirizzo
alla vecchia impaginazione (puntava alle griglie a 16 passi) e diventa «tutto
il resto di **una scheda** descrive **una battuta**» — dove il soggetto è vero
nel file nuovo. La seconda metà, «Un pezzo ne dura centoventi.», è la citazione
vera, ed è in `MUSICA.md:127` come blockquote su una riga sola. Il controllo
trova la 558 `ATTERRATA-SPEZZATA`: la falsa orfana è solo l'a capo fra «dura» e
«centoventi».

### Gruppo K — la nota di servizio delle correzioni (riga 706) — **l'unica che era contenuto**

| riga | testo | esito |
|---|---|---|
| 706 | `*(ogni volta che una proposta viene corretta, la lezione va qui, con la data)*` | **CONTENUTO — rimessa** |

È l'unica delle 45 che non ho potuto chiudere annotandola, ed è argomentato al
§2.

---

## 2. La riga 706: perché è contenuto, e dove l'ho rimessa

La riga è la nota in corsivo che stava sotto `## Correzioni ricevute`. La
sezione è stata sciolta di proposito — la spec §6 lo chiede, e il Task 3 §5.5
lo esegue: le tre correzioni sono andate ciascuna nel blocco che le compete,
con la loro data. Fin qui è una riga di raccordo, e per due terzi lo è: la
parola «**qui**» è un indirizzo tipografico morto, come «in testa al file» e
«qui sopra» dei gruppi C e G.

Ma il terzo che resta **non è tipografia, è una regola di metodo**: *ogni volta
che una proposta viene corretta, la lezione si scrive, con la data.* E questa
regola, dopo la migrazione, **non era più detta da nessuna parte**. L'ho
verificato invece di supporlo, cercando in tutti e tre i file nuovi le stringhe
`con la data`, `la data`, `lezione`, `registra`, `correzion`:

- il **dove** sopravvive, per un caso solo: `MUSICA.md:194-196` dice che
  «quello che ne esce sbagliato si registra nella **casella 11** della scheda».
  Copre le trappole di repertorio, non le correzioni di metodo né quelle sulla
  macchina;
- il **con la data** non c'è. La pratica è visibile in quattro blocchi del
  comune che portano la data nel titolo («— correzione del 16 agosto 2026», «—
  correzione del 17 agosto 2026», «— detto dall'utente, 16 agosto 2026», «— 17
  agosto 2026»), ma è **dimostrata, non prescritta**. Un lettore fra sei mesi
  vede quattro blocchi datati e non ha nessuna riga che gli dica che datarli è
  la regola.

Perde un pezzo per cui lo schema **ha** una casella — il comune, parte
«Metodo» — quindi il secondo esito è quello dovuto: si rimette.

L'ho rimessa in coda a «Il ciclo di revisione ha un protocollo», che è la
sezione di cui è la conseguenza (`MUSICA.md:249-251`), **con le parole del
vecchio e il solo indirizzo aggiornato** — che è la trasformazione già
sanzionata da questo piano tre volte (Task 3 Minor 1, Task 4 R4/R6/R7), con la
motivazione che il revisore del Task 4 ha messo in chiaro: *«le frasi si
spostano come sono» protegge il contenuto, non le coordinate della vecchia
impaginazione.*

```markdown
*(ogni volta che una proposta viene corretta, la lezione va nella casella che
le compete — la 11 della scheda se è una trappola di quel repertorio, il comune
se vale per tutti — con la data)*
```

Quattro parole del vecchio sostituite («va **qui**» → «va nella casella che le
compete — … —»), quattordici tenute, compreso il «con la data» che era il punto.

**Conseguenza sulla rete di sicurezza, dichiarata:** la riga 706 **resta
ORFANA**. Lo strumento confronta la riga sorgente, l'indirizzo è cambiato, e la
riga non può che continuare a comparire nell'elenco — esattamente come le
righe 4, 147, 151 e 609. Il conto resta 45 prima e dopo, e questo rapporto è il
posto in cui è scritto perché.

Non ho toccato le schede né l'indice, quindi
`test_indice_repertori_coerente_con_le_schede` non poteva muoversi, e infatti
non si è mosso: i cinque check passano, con le stesse ventidue celle.

---

## 3. Le DOPPIE: 15, verificate, tutte innocue

Sono **15** e non 12: tre sono entrate col Task 6, e sono le righe `|---|---|---|---|`
della matrice dell'indice, che ha quattro colonne come le tabelle per stile e
per tempo di `jazz.md`. Nessuno le aveva ancora guardate; le ho guardate.

Il criterio è quello del brief: viola «un numero vive in una casella sola» ogni
riga doppia che contenga **un numero, una sigla musicale o un nome di
funzione**.

| righe | testo | contiene numero/sigla/funzione? |
|---|---|---|
| 10, 40, 198, 265, 505, 522 | `\|---\|---\|---\|` | no — solo trattini |
| 109, 275, 585, 669, 727 | `\|---\|---\|` | no |
| 411, 428, 437 | `\|---\|---\|---\|---\|` | no — **le tre nuove del Task 6** |
| 565 | `niente.` | no |

Quattordici su quindici sono **punteggiatura Markdown**: separatori di
intestazione di tabella. Non sono contenuto, e sono doppie perché lo strumento
cerca la riga come **sottostringa** — `|---|---|` è contenuto dentro
`|---|---|---|`, quindi una tabella a tre colonne fa scattare anche la riga a
due.

La quindicesima merita d'essere spiegata, perché è la sola che sembri una
parola. La riga vecchia 565 è `> niente.` — la fine di «e di quella scala qui
non c'era niente.». Ho verificato dove compaia la stringa `niente.` nei tre
file: **sette volte, in sette frasi diverse**.

| dove | la frase |
|---|---|
| `MUSICA.md:220` | «ma non blocca niente.» |
| `MUSICA.md:548` | «Su un groove di crome quel default non muove niente.» |
| `reggae-dub.md:84` | «su un groove di crome quel 57 non muove niente.» |
| `reggae-dub.md:239` | «di quella scala qui non c'era niente.» ← **la frase originale** |
| `jazz.md:133` | «del rapporto fra comping, walking e solista non dice niente.» |
| `jazz.md:184` | «su una linea di crome non muove niente.» |
| `jazz.md:199` | «dell'arrangiamento jazz sul Deluge non si sa niente.» |

Sette e non sei: la prima stesura aveva collassato in una le **tre** «non muove
niente.», che sono di tre soggetti diversi (il default del firmware, il 57 del
dub, il default sulle crome del jazz) e stanno in tre file. Non c'è nessuna
riga ripetuta: c'è una parola italiana comune che finisce sette periodi.

**Nessuna delle 15 viola il vincolo. Il giudizio ereditato regge, e adesso
copre anche le tre righe che l'avevano ereditato senza saperlo.**

### Il controllo che le DOPPIE non sanno fare, e che ho fatto

Le DOPPIE confrontano righe intere: un numero ripetuto in **due frasi diverse**
in due file non le fa scattare. È il difetto che il Task 3 §5.6 aveva
segnalato. Ho quindi eseguito l'audit incrociato dei token duri fra i tre file
nuovi, col metodo dichiarato al §0.

**Il conteggio grezzo non lo riporto, perché non è riproducibile e non
significa niente.** Dipende interamente da dove si mette il confine di token:

| conteggio | metodo | cosa lo separa dagli altri |
|---|---|---|
| **52** | prima stesura, ricerca per **sottostringa** | `1` combacia dentro `1,61`, `106`, `2026`: gonfiato da falsi positivi |
| **34** | stesso script, **confini veri** (né cifra né virgola né punto ai lati) | corretto, ma conta **anche le cifre isolate strutturali** — `1`…`11` dei numeri di casella, `17`/`2026` delle date |
| **21** | audit indipendente della revisione | corretto, e **esclude** quelle cifre strutturali, che non sono grandezze misurate ma etichette |

La differenza fra 34 e 21 è tutta lì: tredici token che sono **numeri di
casella e componenti di data**, cioè cose che *devono* comparire in tutti e tre
i file perché lo schema ha undici caselle in ognuno. Il criterio della
revisione è il migliore dei tre; nessuno dei tre è una misura.

**Quello che porta informazione non è il conteggio ma l'ispezione**: ho aperto
col contesto ogni token che comparisse in più di un file, e tolte le tre
coincidenze del §4.2 sono tutti **omografi**, cioè grandezze diverse che si
scrivono uguale:

| token | in `MUSICA.md` | in `jazz.md` / `reggae-dub.md` |
|---|---|---|
| `56` | destinazioni di patch cable del firmware | display dello swing FUSION |
| `60` | escursione di velocity del charleston | display dello swing POSTBOP |
| `62` | KB di `music-composer` | display dello swing del jazz |
| `1,3` | MB di `music-composition` | mediana di «Playing It Straight» |
| `106` | file di riferimento della skill | assoli POSTBOP |
| `57` | — | display del dub (reggae) / assoli HARDBOP (jazz) |

Due sole coincidenze **non** sono omografe, e le dichiaro al §4.2.

---

## 4. Le tre cose che restano da sapere

### 4.1 «L'ho pure difesa» è coperta — e come ho sbagliato a dire il contrario

La prima stesura di questo rapporto dichiarava che le cinque parole finali del
vecchio 538 — *«L'ho pure difesa»* — non fossero in nessun file, e mandava un
lettore futuro ad aggiungerle a `FINDINGS.md` §6. **Era falso, e l'istruzione
era dannosa:** avrebbe fatto duplicare in `FINDINGS.md` una cosa che
`HANDOFF.md` già porta, cioè esattamente il difetto contro cui esiste «un
numero vive in una casella sola».

Il fatto è coperto, due volte:

- **`HANDOFF.md:1049`** — «Ne era uscita la conclusione controintuitiva
  «l'etichetta nomina il blocco, non la figura», **e l'avevo pure difesa**.»
  È la riga 538 del vecchio quasi carattere per carattere.
- **`HANDOFF.md:1221`** — lo dice una seconda volta e con più forza, dentro il
  racconto della quinta correzione dell'utente: «non l'ho corretta subito:
  **avevo appena difeso la mia tabella dell'intervallo di swing** con
  un'aritmetica presa dal sorgente».

**Non c'è niente da aggiungere a nessun file.** L'errore era mio ed era di
**perimetro**: cercavo in quattro file (i tre nuovi più `FINDINGS.md` e
`ARCHITETTURA.md`) e `HANDOFF.md` non era fra questi, benché sia il documento
in cui il progetto tiene il racconto degli errori di metodo. L'audit del §0 ora
gira su sei file, ed è la ragione per cui questo paragrafo dice il contrario di
quello che diceva. Lascio la correzione visibile invece di riscrivere in
silenzio: un rapporto che serve a provare che non si è perso niente deve
mostrare anche dove **lui** aveva guardato male.

### 4.2 `50` e `67` vivono in due file, e non è un errore, ma va saputo

`MUSICA.md:544` dice «**50 è dritto, 67 è la terzina**» come proprietà della
formula; `jazz.md:191` e `jazz.md:196` li ripetono come righe di riferimento
della tabella di conversione (`| dritto | 50 |`, `| terzina esatta | 67 |`).
Sono la stessa grandezza in due file, quindi la lettera di «un numero vive in
una casella sola» è sfiorata.

**Non l'ho corretto, per tre ragioni.** Primo: non sono valori *di repertorio*
— sono i due estremi fissi del meccanismo, e discendono per aritmetica dalla
formula del comune (BUR 1 → 50, BUR 2 → 67). Non possono divergere: è
matematicamente impossibile che fra un mese ci siano due valori diversi, che è
il danno contro cui la regola esiste. Secondo: quella tabella è **incollata
identica dal brief del Task 5**, che ne prescrive il contenuto meno la colonna
BUR; toglierle le due righe di ancoraggio la renderebbe illeggibile e sarebbe
una modifica di merito presa di mia iniziativa contro un brief. Terzo:
`jazz.md:184-186` già rimanda al comune per il meccanismo, quindi il lettore
sa dov'è la fonte. **Lo segnalo perché sia una scelta e non una svista.**

Il caso gemello del `62` — l'esempio `S.set_swing(doc, 62, figura='1/8')` in
`MUSICA.md:551` e il `**62**` della tabella di `jazz.md:192` — è già stato
adjudicato dalla revisione del Task 3 (Important 1) e disinnescato con il
cartello «L'esempio è **illustrativo**» a `MUSICA.md:554-556`. L'ho verificato
ancora in piedi.

> ⚠️ **Questo paragrafo è un giudizio, non un fatto verificato, e va lasciato
> marcato tale.** L'argomento che lo regge — «è aritmetica, non può divergere»
> — è della stessa famiglia di quello che il Gruppo H documenta come **già
> fallito una volta in questo progetto**: un'aritmetica presa dal sorgente fu
> sovrapposta a un'osservazione corretta e ne uscì una conclusione falsa, che
> fu pure difesa. Qui l'aritmetica è più semplice e la formula è nel comune,
> ma la forma del ragionamento è quella. Chi rivedrà questa pagina non lo
> promuova a fatto: se un giorno `50` o `67` divergessero fra i due file, la
> spiegazione non sarà «impossibile», sarà che qualcuno ha cambiato la formula
> in un posto solo.

### 4.3 I riferimenti di riga di questo rapporto, verificati con uno script

Questo documento cita `file:riga` quarantasei volte, ed è la forma di prova su
cui si regge: chi lo contesterà aprirà quelle righe. **Un rapporto che si
vanta di essere verificabile riga per riga non può avere riferimenti
sbagliati**, e ne aveva.

`$SCRATCH/verifica_riferimenti.py` estrae ogni `nome.md:N` e `nome.md:N-M` dal
rapporto, apre il file vero e **stampa cosa c'è davvero** a quelle righe, senza
giudicare. Passandoglielo ho trovato **sette riferimenti sbagliati**:

- **sei a `MUSICA.md`, tutti sfalsati di esattamente +4** — `535-544`, `544`,
  `551`, `554-556`, `573-575`, `576-581` erano scritti quattro righe più su.
  L'offset è quello del mio commit `9feaf1c`, che ha inserito quattro righe a
  `MUSICA.md:249`: **tutte e sole le citazioni oltre la riga 249 e scritte
  prima della modifica** avevano derivato. Quelle sotto la 249 (`4-5`, `122-130`,
  `127`, `186`, `194-196`, `220`) erano giuste, e giuste erano anche le
  citazioni oltre la 249 che avevo calcolato **dopo** il commit (`249-251`, `548`) —
  il che è la prova che la causa è quella e non un errore di lettura;
- **uno a `HANDOFF.md`**, dove il range `1042-1057` era **troppo stretto**: il
  blocco arriva a `1065`, e le tre righe che tagliavo fuori sono proprio quelle
  che coprono `song.SWING_SCARTO_SORGENTE`. La cella che nella tabella del
  Gruppo H marcava quel fatto come assente da `HANDOFF.md` era quindi falsa —
  ed era falsa **dentro il paragrafo che serve a dimostrare che il perimetro
  era troppo stretto**, che è il posto peggiore in cui potesse stare.

Dopo la correzione lo script è stato rieseguito e tutti e quarantasei i
riferimenti mostrano il testo che il rapporto dice che mostrino.

**La lezione, che è la stessa del Gruppo H:** un numero di riga non è un fatto
stabile, è un puntatore in un file che cambia — e il file l'avevo cambiato io,
in questo stesso task. Chi aggiornerà `MUSICA.md` invaliderà di nuovo questi
riferimenti; lo script sta nello scratchpad ed è di tre righe utili, ma il modo
robusto sarebbe citare i **titoli di sezione** invece dei numeri.

### 4.4 Lo strumento sbaglia solo in un verso, e l'ho ricontrollato

L'affermazione «può accusare righe arrivate, non può dichiarare arrivata una
riga persa» regge per costruzione: `t in testo` è vero solo se la riga sorgente
compare **letteralmente** in un file nuovo, quindi un falso negativo (riga
persa dichiarata arrivata) richiederebbe che il testo ci sia davvero. Il rischio
residuo è di **granularità**, non di direzione: una riga che compare letterale
in un file nuovo ma per coincidenza — come `niente.` — non viene nemmeno
segnalata come orfana. È il motivo per cui l'audit dei token duri (§0) esiste,
e per cui il conto che chiude questo rapporto è quello, non le 45.

---

## 5. Comandi, per intero

```
$ python "$SCRATCH/verifica_migrazione.py"
ORFANE (45) — righe del vecchio che non sono atterrate:
DOPPIE (15) — righe presenti in piu di un file:
        (identiche prima e dopo la modifica)

$ python "$SCRATCH/istruttoria.py"
ORFANE dallo strumento: 45
  ATTERRATA-INTERA     3   (righe 5, 656, 657)
  ATTERRATA-SPEZZATA   3   (righe 159, 558, 655)
  PARZIALE / PERSA    39   istruite una per una al §1

$ python "$SCRATCH/audit_stretto.py"      # confini veri, perimetro a sei file
token duri delle ORFANE assenti da tutti e sei i file: 2
  riga 523: '1,00'   -> jazz.md:49 «1 dritto»
  riga 529: '2,00'   -> jazz.md:49 «2 terzina»
token in piu di uno dei tre file nuovi: 34, tutti aperti col contesto
  (omografi tranne 50/67/62, §4.2; il conteggio grezzo dipende dal
   confine di token e non e' una misura — §3)
"niente." nei tre file: 7 occorrenze, 7 frasi diverse

$ python tests/test_all.py
858/858 test superati        exit=0        FAIL: 0

$ git commit
9feaf1c musica: la sola orfana che era contenuto, rimessa nel comune
 docs/MUSICA.md | 4 ++++
 1 file changed, 4 insertions(+)

$ codifica dei tre file, dopo la modifica
MUSICA.md      BOM False  CRLF 0  righe 621  newline finale True
reggae-dub.md  BOM False  CRLF 0  righe 345  newline finale True
jazz.md        BOM False  CRLF 0  righe 205  newline finale True
```

`docs/FINDINGS.md`, `docs/ARCHITETTURA.md` e `HANDOFF.md` sono stati **letti e
mai scritti**: `git status` dopo il commit è pulito e il commit contiene un
file solo. La revisione di questo rapporto non ha prodotto un secondo commit —
ha corretto solo il rapporto, che non è un file versionato.

---

## 6. Il verdetto

Le 45 ORFANE non sono 45 perdite. Sono **9 raccordi**, **4 indirizzi corretti
di proposito**, **6 re-impaginazioni**, **2 seam**, **8 righe riscritte per un
vincolo esplicito del brief con tutti i loro valori ritrovati**, **15 righe di
«come si è stabilito» che per regola dello schema vivono in `HANDOFF.md` e
`FINDINGS.md`**, e **1 riga di contenuto, che ora è tornata nel comune**.

9 + 4 + 6 + 2 + 8 + 15 + 1 = **45**. Nei due esiti che il brief ammette:
**21 «riga di raccordo riscritta», 24 «è contenuto»** — di cui ventitré già
nella casella giusta e una rimessa da me (§0.1).

Zero righe sono rimaste senza casella. **Lo schema a undici caselle più il
comune ha retto tutto il vecchio file**, e l'unica cosa che ne è caduta fuori è
caduta dentro `HANDOFF.md` e `FINDINGS.md`, che sono il posto che lo schema
stesso le assegna.
