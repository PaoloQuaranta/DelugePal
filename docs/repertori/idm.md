# Elettronica / IDM

**Parziale.** Aggiornata il 2 ottobre 2026. Copre due territori ascoltati:
IDM astratta/meccanica e IDM cameristica melodica. Il primo usa polimetro,
percussioni metalliche e timbro in trasformazione; il secondo tema, risposte,
armonia condivisa e forma narrativa. Non pretende di coprire ambient-IDM,
drill'n'bass, l'intera braindance melodica o glitch massimalista.

Il dettaglio operativo del territorio meccanico sta in
[idm.md](../istruzioni/idm.md); l'esempio in `tools/idm_scritto.py`. `IDM04` è
stata ascoltata e accettata sul dispositivo. Il secondo percorso,
[`TRAMA02` → `TRAMA06`](../istruzioni/brano-completo.md), aggiunge elettronica
melodica, contrappunto e forma lunga. `[OSS]` `TRAMA02` è un esito negativo:
batteria discontinua, suoni alti banali, contrappunto troppo denso e caotico.
Non conta come copertura riuscita. `[OSS]` `TRAMA03` migliora la batteria,
ma lascia armonia/basso incerti e FILO quasi inudibile; OMBRA è corretta
dall'utente. `[CALC]` `TRAMA04` conserva il salvataggio e coordina l'armonia
con un basso di appoggio; corregge l'inviluppo esterno DX7. `[OSS]` La 04
migliora un po', ma FILO resta quasi inudibile. `TRAMA05` aumenta soltanto
i livelli delle portanti DX7; la 06 porta le portanti al limite e riduce
l'attenuazione da velocity. `[OSS]` Il 2 ottobre l'utente accetta la 06 e
chiede di chiudere il task compositivo. Le caselle 7–9 sono ora compilate
per questi due territori; la casella 1 mantiene espliciti i limiti di repertorio.

---

## 1. Cos'è, e cosa non è

**Parziale.** Qui si distinguono elettronica meccanica, in cui la complessità
emerge da periodi diversi e trasformazione timbrica, ed elettronica cameristica,
in cui tema, risposte e armonia cooperano sopra un groove continuo. Entrambe
usano sottrazione e memoria invece di casualità senza direzione. **Non sono**
techno four-on-the-floor o DnB guidata da un break; usare gesti contrappuntistici
non rende TRAMA un esempio di prassi barocca. Sono due territori, non una
definizione esaustiva dell'IDM: gli altri sottogeneri restano da provare.

## 2. Metro e griglia

`[DEC]` 4/4 sottostante, griglia a sedicesimi e trentaduesimi per i retrigger.
Sopra il 4/4, clip indipendenti di **5, 6, 7 e 11 sedicesimi**: il polimetro
sposta continuamente gli accenti senza cambiare il metro globale.

## 3. Tempo

`[DEC]` **90 BPM** in `IDM04`: abbastanza lento da rendere leggibili i singoli
incastri e abbastanza veloce perché i burst a 1/32 restino gesto, non tremolo.
`TRAMA06` usa **102 BPM** per sostenere una linea melodica più lunga senza
comprimere l'aumentazione finale.

## 4. Feel

`[DEC]` `IDM04` è **dritto, swing 50**: la precisione è il carattere e il
movimento viene dallo sfasamento dei periodi. `TRAMA06` conserva lo swing
**54** della prima versione come leggera inclinazione comune; non è una regola
di repertorio.

## 5. Ruoli e spartizione

`[DEC]` THUD dà massa, CLICK definisce il bordo, HAT riempie l'alto, METAL porta
gli accenti lunghi; GLITCH è punteggiatura strutturale ricorrente; DRONE è l'unico strato
intonato. Le parti non si spartiscono per battere/levare ma per **registro,
durata e periodo**.

`[DEC]`+`[OSS]` In `TRAMA06` i ruoli sono narrativi: FILO porta il tema, OMBRA risponde
e accoglie la coda aumentata, CAMPO è un campo armonico lento, GROUND conserva
le fondamentali armoniche e il kit mantiene il groove. È un secondo modello di
spartizione, non ancora un'invariante del repertorio.

## 6. Dinamica

`[DEC]` Accenti gerarchici dentro ogni cellula: spesso il primo evento è più
forte, ma nelle variazioni THUD l'accento ruota fino al colpo finale. Gli altri
eventi funzionano da fantasmi. Il glitch decade dentro ogni burst. La dinamica
non è randomizzata: deve rendere riconoscibile ciascun periodo.

`[DEC]`+`[OSS]` Nel modello cameristico il culmine alterna la voce attiva,
senza far variare ogni ruolo allo stesso modo. Il kit conserva lo scheletro;
basso, campo e voci superiori hanno dinamiche e densita distinte.
I livelli DX7 finali e la correzione di OMBRA sono documentati nel
[caso ascoltato](../istruzioni/brano-completo.md#trama06-ulteriore-livello-filo):
la velocity delle note e il volume master da soli non descrivono il livello udibile.

## 7. Armonia

`[DEC]`+`[OSS]` Due modelli nel perimetro coperto. `IDM04` non ha progressione:
il campo armonico è il tritono
**Re–La♭**, tenuto e cromatico. `[CALC]` `TRAMA03`, in Re minore, non realizza
una progressione funzionale completa: CAMPO alterna i campi/dyad
**Re–Mi, Si♭–La, Sol–La, La–Sol** sopra il ground; nel build usa
**Re–La, Si♭–La, Sol–Re, Mi♭–Si♭, La–Mi**. Sono altezze volutamente aperte,
non sigle di accordo implicite. È un caso di elettronica melodica, non ancora
una pratica armonica generale dell'IDM o dell'ambient. La 03 rimane un
controesempio, non la ricetta da ripetere.

`[OSS]` I campi della 03 non sono risultati coerenti all'ascolto. `[DEC]`
La 04 usa Sol dorico e una sola mappa per basso e CAMPO: Sol minore,
Do maggiore/Do7, Fa maggiore e Si♭ maggiore. Il tema di FILO resta identico;
quattro note cromatiche di OMBRA sono adattate e l'ultima sospensione risolve
su Si♭. Questa realizzazione resta invariata fino alla 06 accettata.

`[DEC]` Nel caso cameristico il ritmo armonico e una mappa comune di
fondamentali e dyad, non cicli indipendenti: CAMPO non sostiene un campo
oltre il cambio del basso. La prima esposizione usa Sol–Do–Fa–Sol; nel basso
si articola la stessa fondamentale sul battere e sulla seconda cassa.
Le voci lunghe del campo lasciano spazio alle frasi e al culmine a tre parti.
Per la mappa completa, le durate e la condotta realizzata, vedere
[`trama_revisione.py`](../../tools/trama_revisione.py) e i test dedicati.
E un modello operativo accettato, non una misura statistica del repertorio.

## 8. Melodia e ornamentazione

`[DEC]`+`[OSS]` In `IDM04` non c'è una melodia tonale: il materiale sviluppato è
ritmico. Nel modello cameristico `TRAMA06` conserva il tema di tredici eventi di `TRAMA02`.
La 03 riduce gli attacchi delle due voci superiori da 367 a 123; la risoluzione
di coda della 04 porta il totale finale a 124. La revisione limita il vero
tre-parti alle battute 36–40. Tema letterale, risposta indipendente,
variazione, espansione di registro e aumentazione finale costruiscono il
discorso; l'ornamento non e un riempimento continuo fra le frasi.
La 06 chiude il caso compositivo all'ascolto. Tema e gesti sono scelte
dell'esempio: non diventano invarianti di tutta la musica elettronica.

## 9. Forma e densità

`[DEC]`+`[OSS]` `IDM04` usa 40 battute per **accrezione/mutazione**:
3 strati → 5 strati → interludio a 3–4 ruoli → ritorno pieno. Tre cellule di
cassa sullo stesso periodo di 6/16 evitano un fondamento identico dall'inizio
alla fine; otto eventi alternano due gesti glitch.
La prima versione scendeva fino alla sola cassa e lasciava la prima metà troppo
vuota; l'ascolto ha imposto almeno tre ruoli attivi nelle prime 28 battute.
Non è build/drop: la tensione viene da quanti periodi interagiscono.

`[CALC]` `TRAMA06` aggiunge una seconda famiglia: **58 battute**,
sezioni da 6/8/8/10/12/8 battute e coda di 8 sovrapposta alle ultime due del
ritorno. `[OSS]` L'arco per accumulo di `TRAMA02`, pur misurato, è stato
percepito come caos. `TRAMA03` mantiene la forma ma usa un groove invariato,
due vuoti superiori, una sola voce fitta alla volta e un culmine affidato anche
a registro e timbro. Questo arco e conservato nella 06 accettata: la forma
lunga e ora una prova compositiva chiusa, non soltanto una timeline valida.
Le battute e i giunti esatti vivono nella
[mappa del brano](../istruzioni/brano-completo.md#la-forma-conservata).

## 10. Sul Deluge

`[OSS]`+`[DEC]` Una traccia kit per periodo, perché una traccia suona una clip
per volta. `S.set_clip_length()` assegna le lunghezze arbitrarie;
`A.place(..., length=...)` stende le ripetizioni in arranger. `MU.automatizza`
muove cutoff e risonanza del drone. La clip del drone è cromatica e lo scroll
va rifatto dopo `S.set_key_mode(False)`. Il drone usa il synth subtractive
vuoto: triangolo + `analogSaw`, due voci di unisono e inviluppo sostenuto;
nessun multisample.

`[OSS]` `TRAMA06` completa il secondo percorso sul dispositivo: cinque
strumenti con clip estese sull'arranger, DX7 per FILO, ring modulation per
OMBRA e campo granulare. Si conserva il salvataggio utente prima di ogni
revisione. `SY.update_dx7_patch()` cambia soltanto il payload di una voce
esistente, senza il reset di inviluppo/routing di `SY.set_dx7()`.
La rilettura della 06 e identica al file inviato; l'utente chiude il task.

## 11. Trappole del generatore

`[DEC]`

- mettere tutti gli eventi in una clip: si perde l'indipendenza dei periodi;
- randomizzare: distrugge l'identità delle cellule e non crea sviluppo;
- aggiungere swing per riflesso: qui la precisione è il feel;
- glitch continuo: da punteggiatura diventa superficie piatta; l'esempio usa
  otto battute-evento isolate su quaranta e alterna due gesti;
- usare un multisample one-shot come drone: l'inviluppo può restare aperto ma
  la registrazione continua a decadere; l'esempio usa oscillatori subtractive;
- chiudere troppo il cutoff nel registro grave: il drone può risultare muto;
  l'esempio resta fra 40 e 48;
- richiudere l'inviluppo esterno dopo `set_dx7()`: in FILO della 03 il
  sustain 8 attenuava gli inviluppi già presenti negli operatori;
- attribuire tutto il livello DX7 al master: la prima correzione di ENV1
  non bastava; portanti e sensibilita alla velocity richiedevano una revisione;
- sovrascrivere OMBRA ricreando i preset: la filtratura salvata dall'utente
  fa parte del risultato accettato e va conservata;
- far variare la batteria come una voce di contrappunto: perde continuita;
- usare un basso contrappuntistico come ground sotto campi armonici con
  tempi di cambio diversi: la 03 lo rendeva percettivamente incerto;
- troppe altezze: competono con il fenomeno ritmico invece di incorniciarlo;
- cambiare key mode senza rifare lo scroll: note giuste ma invisibili;
- chiamare «IDM» un solo pezzo: questa scheda resta dichiaratamente parziale.
