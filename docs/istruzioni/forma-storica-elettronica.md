# Forma storica come materiale per musica elettronica

**Scopo (27 settembre 2026).** Prendere gesti espressivi della musica classica e barocca e usarli in produzioni nate sul Deluge. Il timbro, il beat e la durata delle sezioni restano liberi: questa non è una guida alla ricostruzione stilistica.

## Che cosa coprono già le fonti locali

| Fonte | Materiale utile oltre l'armonia | Stato nel progetto |
|---|---|---|
| Piston, *Harmony*, 5ª ed., capp. 7, 13, 18, 20 | motivo e variazione melodica; frase e periodo; tessitura; sequenza | base per la forma breve. `MU.forma` e `MU.variazione` dispongono clip, ma non decidono come sviluppare un motivo o far respirare una frase |
| Piston, *Counterpoint* (1970), introduzione e capp. 5-11 | indipendenza di ritmo e curva; struttura motivica; tre o più parti; contrappunto invertibile e canone | [contrappunto.md](contrappunto.md) copriva già due voci melodiche; la prova sotto apre il rapporto con la batteria e il passaggio del motivo fra timbri |
| Piston, *Counterpoint*, conclusione, p. 229 | rapporti contrappuntistici anche fra figure percussive prive di altezza | base per trattare gli accenti della batteria come una linea che risponde |

**Valutazione.** Piston copre bene armonia, frase, tessitura e relazioni fra le parti: l'ipotesi che copra soltanto l'armonia era troppo stretta. Nel cap. 7 definisce anche il *ground bass*; la [prova sul basso ostinato](basso-ostinato.md) ne verifica il principio di ritorno. Piston non basta però per attribuire a passacaglia e ciaccona un'unica struttura storica, né per scegliere e articolare forme lunghe come ritornello e fuga come processo di entrate e trasformazioni. Le registrazioni MIDI locali di MAESTRO non annotano quelle forme: servono per ascolto e confronto, non come etichette già pronte.

## Prima prova: `CONTRELE01`

`[LIB]` Piston descrive il contrappunto come rapporto fra dipendenza e indipendenza in armonia, ritmo e curva (introduzione, p. 9). Nel cap. 6 tratta la struttura motivica. La conclusione (p. 229) estende l'idea alle figure percussive. Questi sono i principi presi dalla fonte; la loro disposizione in un beat elettronico è `[DEC]`.

`[DEC]` La song di 16 battute in [`tools/contrappunto_elettronico_scritto.py`](../../tools/contrappunto_elettronico_scritto.py) ha quattro passaggi:

| Battute | Gesto |
|---|---|
| 1-4 | motivo su synth; alcuni colpi di rim coincidono con gli attacchi |
| 5-8 | il pluck risponde negli spazi e il rim sposta gli accenti |
| 9-12 | il motivo passa al pluck un'ottava sopra; il synth tace e la cassa si dimezza |
| 13-16 | ritorno del synth con una risposta indipendente del pluck |

`[CALC]` Il trasferimento conserva i quattro attacchi e le quattro classi di altezza del motivo; cambia registro e timbro. Gli accenti del rim nella prima battuta sono a 0 e 168 tick; nella quinta sono a 48, 120, 216 e 312 tick. La song occupa esattamente 16 battute; `MU.verifica` e `MU.avvertenze` sono vuote. Il 27 settembre 2026 `CONTRELE01.XML` è stato caricato in `/SONGS/DelugePal/` e riletto dalla SD: 144439 byte e hash SHA-256 identico al file locale. `[OSS]` **Ascoltata sul Deluge il 27 settembre 2026**: l'utente ha confermato «ok funziona». Non ha ancora espresso un giudizio separato sulla percezione dello scambio del motivo o sulla densità del rim.

## Seconda prova: `PERIODO01`

`[LIB]` Piston, *Harmony*, 5ª ed., cap. 11, p. 175: la semicadenza sulla dominante lascia una frase aperta; una coppia di frasi affini può chiudere la seconda con cadenza autentica. Cap. 13, p. 212: due frasi bilanciate formano un periodo; nell'esempio di Mozart citato da Piston i due inizi si assomigliano e sono soprattutto le cadenze a distinguersi.

`[DEC]` In [`tools/periodo_elettronico_scritto.py`](../../tools/periodo_elettronico_scritto.py) le battute 1-4 e 5-8 hanno le stesse prime due battute di melodia e armonia. La prima termina su La maggiore (V di Re minore), la seconda passa da La7 a Re minore (V7-i). Beat, durata delle frasi e pausa finale sono uguali, per esporre la differenza tra finale aperto e chiuso. L'organico resta synth, pad, basso e kit 808.

`[CALC]` Le due aperture melodiche coincidono nota per nota, i finali divergono, l'arco è di otto battute. `MU.verifica` e `MU.avvertenze` sono vuote. Il 27 settembre 2026 `PERIODO01.XML` è stato caricato in `/SONGS/DelugePal/` e riletto dalla SD: 139389 byte, hash SHA-256 identico al file locale. `[OSS]` **Ascoltata sul Deluge**: l'utente sente la prima frase arrivare sul La e la seconda risolvere sul Re. Questa era la distinzione fissata prima di costruire la prova.

## Come verificare le prossime prove

Per una proprietà definita dalle note — stesso inizio, intervalli, funzione degli accordi, arrivo sulla dominante o sulla tonica — bastano fonte teorica e controllo dei dati (`[LIB]` + `[CALC]`). La rilettura dalla SD conferma che i dati trasferiti sono quelli controllati. Dopo queste due prove riuscite, non serve chiedere un ascolto per ogni applicazione dello stesso principio.

L'ascolto (`[OSS]`) resta utile quando la domanda riguarda **l'effetto percepito**: se due linee si distinguono, se un ritorno viene riconosciuto, se beat e timbri mascherano una cadenza, se la densità funziona. Le relazioni armoniche sono calcolabili; il loro effetto espressivo in un particolare suono non si deduce interamente dai numeri. Il controllo sul dispositivo torna necessario anche se si introduce un nuovo tipo di suono o di scrittura XML.

## Terza prova: `SEQUENZA01`

`[LIB]` Piston, *Harmony*, 5ª ed., cap. 20, pp. 315-318: la sequenza trasporta sistematicamente un disegno melodico, ritmico e armonico. Tre apparizioni (due trasposizioni) stabiliscono il procedimento; dopo la terza la simmetria viene spesso variata o abbandonata. In una sequenza tonale i gradi restano nella stessa tonalità, quindi la qualità degli intervalli e degli accordi può cambiare.

`[DEC]` In [`tools/sequenza_elettronica_scritto.py`](../../tools/sequenza_elettronica_scritto.py) le battute 1-2 sono Re minore–Sol minore, 3-4 Mi diminuito–La minore, 5-6 Fa maggiore–Si bemolle maggiore. Il disegno ritmico e la curva arpeggiata tornano; entrambe le fondamentali di ogni coppia salgono di un grado in Re minore. Le battute 7-8 rompono il ciclo: attacchi ravvicinati su La7, poi Re minore tenuto. Beat, pad e basso rendono il processo una breve sezione elettronica.

`[CALC]` Sei battute di sequenza con quattro note ciascuna e attacchi relativi identici; tre coppie di fondamentali `Re–Sol`, `Mi–La`, `Fa–Sib`; due battute di uscita; otto battute totali. `MU.verifica` e `MU.avvertenze` sono vuote. Il 27 settembre 2026 `SEQUENZA01.XML` è stato caricato in `/SONGS/DelugePal/` e riletto dalla SD: 140843 byte, SHA-256 identico al file locale. `[OSS]` L'utente l'ha ascoltata: **funziona musicalmente, ma è molto banale**. La prova conferma la meccanica della sequenza, non offre ancora un esempio espressivo da imitare. Il task su questa sequenza è chiuso.

## Quarta prova: `CANONE01`

`[LIB]` Piston, *Counterpoint* (1970), cap. 11: nel canone la seconda voce
mantiene l'imitazione della prima a un intervallo e a una distanza temporale
stabiliti. Qui il principio viene trasferito a due synth: non si ricostruisce
uno stile storico.

`[DEC]` In
[`tools/canone_ottava_scritto.py`](../../tools/canone_ottava_scritto.py) la
guida espone una linea monofonica di otto battute in Re minore. La risposta
entra dopo una battuta e riproduce tutti i 32 eventi un'ottava sopra. Non ci
sono basso, accordi o batteria: l'attacco solo della guida, le sette battute di
sovrapposizione e la coda sola della risposta devono rendere udibile il
procedimento senza una terza parte che lo mascheri. I due timbri sono distinti,
ma ritmo, durate e intervalli della linea sono identici.

`[CALC]` Ogni evento della risposta è quello corrispondente della guida a
`+384` tick e `+12` semitoni, con la stessa durata. Il rapporto contiene 11
moti contrari, 24 obliqui, 3 diretti e un parallelo imperfetto; nessuna quinta
o ottava parallela, nessuna dissonanza sui movimenti forti, simultaneità degli
attacchi 50% e picchi sfasati. La timeline è di nove battute e contiene
esattamente due strumenti. `MU.verifica` e `MU.avvertenze` sono vuote.

Il 28 settembre 2026 `CANONE01.XML` è stato caricato in
`/SONGS/DelugePal/` e riletto byte per byte: 22605 byte, SHA-256
`ec311adc5e7d118d20ed345b5c74ad5000244af733a4aa0a96e8098c8665e1fe`, 0
timeout, 0 blocchi parziali e 0 riaperture. `[OSS]` L'utente ha ascoltato la
song sul Deluge e confermato: **«percepisco ingresso imitativo»**. La prova
chiude quindi sia la struttura sia il suo effetto percettivo: le due entrate si
distinguono come canone e non come semplice armonizzazione.

## Quinta prova: `INVERT01`

`[LIB]` Piston, *Counterpoint* (1970), capp. 9-10: nel contrappunto
invertibile le parti devono poter scambiare posizione senza perdere la propria
identita e senza rendere scorretto il rapporto verticale. Qui si prova lo
scambio all'ottava fra due sole linee, non la ricostruzione di uno stile
storico.

`[DEC]` In
[`tools/contrappunto_invertibile_scritto.py`](../../tools/contrappunto_invertibile_scritto.py)
le prime quattro battute presentano A sopra e B sotto. Nelle quattro successive
A ricompare esattamente un'ottava sotto e B esattamente un'ottava sopra. Non ci
sono basso, accordi o batteria: i due synth sono l'intero organico, cosi lo
scambio di registro e ruolo non viene spiegato da una terza parte.

`[CALC]` Note, attacchi e durate delle due linee restano identici fra le due
passate; cambiano soltanto `-12` semitoni per A e `+12` per B, dopo `+1536` tick.
Entrambe le disposizioni evitano quinte e ottave parallele e dissonanze sui
movimenti forti. Gli attacchi simultanei sono 2 su 13 (15%); i moti sono 18
obliqui, 2 diretti e un parallelo imperfetto, con picchi sfasati. Le dissonanze
residue cadono sui tempi deboli. La timeline e di otto battute, contiene
esattamente due strumenti e `MU.verifica`/`MU.avvertenze` sono vuote.

Il 28 settembre 2026 `INVERT01.XML` e stato caricato in
`/SONGS/DelugePal/` e riletto byte per byte: 22181 byte, SHA-256
`9ee77197749f19e06dac6cf7903de7ba289100f9b9b98f78e7127046101879b2`, 0
timeout, 0 blocchi parziali e 0 riaperture. `[OSS]` L'utente ha ascoltato la
song sul Deluge e confermato **«funziona e il tema è molto bello»**. Lo scambio
non compromette quindi ne il funzionamento musicale ne l'identita espressiva
del materiale; la prova e chiusa anche sul piano percettivo.

## Sesta prova: `TREPARTI01`

`[LIB]` Piston, *Counterpoint* (1970), capp. 7-8: aggiungere una terza parte
non significa dividere un accordo fra tre linee. Ciascuna conserva ritmo e
curva propri; inoltre la quarta fra le due voci superiori puo essere sostenuta
da una nota sotto e va quindi valutata nell'intera sonorita, non come se le due
parti alte fossero sole (p. 125).

`[DEC]` In
[`tools/tre_parti_scritto.py`](../../tools/tre_parti_scritto.py) voce alta,
media e bassa entrano all'inizio delle battute 1, 2 e 3. Da li intrecciano tre
ritmi diversi per sei battute e convergono su Re minore. Non ci sono accordi,
batteria o una quarta traccia: i tre synth sono l'intero tessuto musicale.

`[CALC]` Le tre coppie hanno simultaneita degli attacchi del 61%, 55% e 60%.
In ciascuna i moti contrari e obliqui superano quelli diretti e paralleli; non
compare nessuna quinta o ottava parallela. I tre culmini cadono a `2016`,
`2784` e `2976` tick. Dalla terza battuta si controllano anche le verticali
complete: 24 movimenti forti su 24 formano tre classi distinte e consonanti
rispetto al basso, ammettendo la quarta solo fra le parti superiori. Le tre
curve terminano insieme su Re-Fa-La alla fine dell'ottava battuta. La song ha
esattamente tre strumenti e `MU.verifica`/`MU.avvertenze` sono vuote.

Il 28 settembre 2026 `TREPARTI01.XML` e stato caricato in
`/SONGS/DelugePal/` e riletto byte per byte: 32958 byte, SHA-256
`ad6c165fed065c69c9fa6dce99b8710135b0bf67a4b12f5e62d3005f3dd7f17f`, 0
timeout, 0 blocchi parziali e 0 riaperture. `[OSS]` L'utente ha ascoltato la
song sul Deluge e confermato **«perfetto funziona»**. La prova a tre parti e
quindi chiusa anche sul piano percettivo.

## Settima prova: `VARIAZ01`

`[LIB]` La variazione mantiene riconoscibile un tema mentre ne trasforma una o
piu dimensioni. Qui il materiale di partenza non e un motivo astratto: sono le
quattro battute complete di A e B gia ascoltate in `INVERT01`. La forma e il
passaggio ai tre timbri sono decisioni elettroniche `[DEC]`, non una
ricostruzione di una forma storica particolare.

`[DEC]` In
[`tools/tema_variazioni_scritto.py`](../../tools/tema_variazioni_scritto.py)
la forma dura 24 battute: esposizione letterale (1-4), figurazione con note
vicine (5-8), distribuzione timbrica del tema fra due synth sopra il
controcanto (9-12), tessuto a tre parti (13-16), aumentazione esatta e pedale
conclusivo (17-24). Non c'e batteria: i cambi di superficie, registro e
densita devono restare in primo piano.

`[CALC]` L'esposizione conserva tutti i 13 eventi della linea A di `INVERT01`.
La figurazione ne conserva attacchi e altezze portanti e sale a 30 eventi; la
variazione timbrica ridistribuisce i 13 eventi senza perderli; le tre coppie
della variazione contrappuntistica hanno ritmi distinti, simultaneita inferiore
al 75% e nessuna quinta o ottava parallela. Nel finale ogni attacco e durata
della linea A sono moltiplicati per due. La song contiene tre synth, occupa
esattamente 24 battute e `MU.verifica`/`MU.avvertenze` sono vuote.

Il file locale `out/VARIAZ01.XML` misura 35035 byte e ha SHA-256
`da6754702b97f74061af86b4ff4c502552caa09735f5329dafad16c2de8945b6`.
Il 28 settembre 2026 e stato caricato in `/SONGS/DelugePal/VARIAZ01.XML` e
riletto byte per byte: 35035 byte e SHA-256 identico, 0 timeout, 0 blocchi
parziali e 0 riaperture. `[OSS]` L'utente lo ha ascoltato sul Deluge e ha
confermato: **«ok, funziona bene»**. La trasformazione del tema e quindi chiusa
anche sul piano percettivo.

## Copertura successiva, su domanda di un pezzo

1. **Ostinato e grandi ritorni**: il [basso ostinato](basso-ostinato.md) ha una prima prova strutturale. Restano la percezione del ritorno in una produzione reale, il ritornello e la varietà storica di passacaglia/ciaccona.
2. **Contrappunto invertibile e inversione dei ruoli** da *Counterpoint*, capp. 9-10: `INVERT01` chiude la prova a due voci sia nel calcolo sia all'ascolto. Una terza voce si aggiunge solo se un pezzo la richiede. Anche il canone rigoroso a due voci e chiuso sia nel calcolo sia all'ascolto.
3. **Tre e piu parti** da *Counterpoint*, capp. 7-8: `TREPARTI01` chiude la prova a tre voci sia nel calcolo sia all'ascolto. L'estensione oltre tre parti si fa solo se un pezzo la richiede.
4. **Variazione di un tema intero**: `VARIAZ01` chiude il controllo dei dati su
   esposizione, figurazione, passaggio timbrico, tre parti e aumentazione; il
   giudizio d'ascolto positivo chiude anche la riconoscibilita della forma.

La riga `classica · barocca · antica` in [`MUSICA.md`](../MUSICA.md) resta vuota: queste sono prove di **trasferimento** di gesti, non descrizioni verificate del repertorio storico. L'«antica» richiederà fonti proprie: non è coperta dai due Piston.
