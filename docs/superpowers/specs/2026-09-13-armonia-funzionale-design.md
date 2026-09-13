# La spina funzionale — progetto

**Data:** 13 settembre 2026
**Cos'è:** la **casa tonale che regge e risolve** — la fondazione che tutte le
altre istruzioni d'armonia danno per scontata (*«parti da un giro diatonico che
regge»*) ma nessuna insegna. Due facce: **`armonia-funzionale.md`** (ii-V-I,
cadenze, turnaround) e **`dominanti-secondarie.md`** (la tonicizzazione).

## Perché, e il buco che chiude

Le nove istruzioni d'armonia coprono il **colore** (modale, prestito, scale
simmetriche, cromatismo) ma non la **funzione** che colorano. Ogni istruzione
funzionale (`armonia-prestito`, `accordi-di-passaggio`) comincia con «parti da un
giro diatonico che regge»; ogni istruzione modale/simmetrica si definisce
*contro* «il ii-V-I, la dominante che risolve». La casa che tutte assumono — o
negano — non ha istruzione. È il centro di «jazz approfondito» del perimetro, ed
è l'unica grande istruzione d'armonia ancora non scritta.

## La variazione di metodo — decisa il 13 settembre 2026

⚠️ **Niente esempio lavorato all'ascolto**, per nessuna delle due facce. Motivo,
dato dall'utente: *«lo sviluppo dell'armonia ha sempre avuto un successo del
100%, perché sono regole precise ed è impossibile sbagliare»*. Il guardiano
`[CALC]` — il fatto testato contro `song.MODI`/calcolo — **sostituisce**
l'ascolto. Le istruzioni si chiudono con `[LIB]` + `[CALC]`, senza `[OSS]` né un
pezzo caricato sul Deluge. Resta valida per l'armonia (regola precisa), non per
il ritmo (dove l'ascolto ha respinto dieci versioni).

## Faccia 1 — `armonia-funzionale.md`

**A cosa serve.** Costruire una casa tonale che regge e risolve.

**Il principio — le tre funzioni.** Tonica (riposo) → Sottodominante
(allontanamento) → Dominante (tensione che vuole risolvere) → Tonica. È il
respiro del tonale, l'opposto dichiarato di `armonia-modale` (che lo evita).

**Vocabolario:**

- gli **accordi diatonici di settima** coi loro ruoli T/S/D, maggiore e minore;
- **il ii-V-I**, l'atomo — maggiore (`Dm7 | G7 | Cmaj7`) e minore
  (`Dm7b5 | G7b9 | Cm`);
- **le cadenze:** autentica (V→I), plagale (IV→I), d'inganno (V→vi), sospesa
  (…→V);
- **il turnaround:** I–vi–ii–V, e la variante I–VI7–ii–V (la VI7 è già una
  dominante secondaria → ponte alla Faccia 2).

**`[CALC]` — `test_armonia_funzionale`.** Il cuore testato: il **tritone del V7**
(3ª+7ª, in Do si–fa) risolve per semitono sul I (si→do, fa→mi) — è il tritono a
sciogliersi. Più: il ii-V-I minore con iiø7 e V7♭9; le note delle cadenze.
Verificati contro `song.MODI`/intervalli.

**`[LIB]`:** Smith, *Jazz Theory* (4ª ed.), cap. VIII «Functional Harmony»
(già in casa, già citato nel prestito p. 66); Piston, *Harmony* (5ª ed.), per le
funzioni e le cadenze. ⚠️ **Pagine da verificare sui PDF quando si scrive** — non
si inventano.

## Faccia 2 — `dominanti-secondarie.md`

**A cosa serve.** Dare spinta a un grado diverso dalla tonica «tonicizzandolo»
per un attimo con la sua dominante — senza modulare. Costruisce **sulla** Faccia
1, stesso confine **casa/ospite** del prestito.

**Vocabolario:**

- le **dominanti secondarie** diatoniche: V7/ii, V7/iii, V7/IV, V7/V, V7/vi
  (non il vii° diminuito — un accordo diminuito non si tonicizza);
- **il ii-V interpolato:** per tonicizzare Dm non solo A7 ma `Em7b5 | A7 | Dm`;
- **il ciclo delle quinte** incatenato (`E7 | A7 | D7 | G7 | C`): il giro più
  forte del tonale;
- **rimando** (non ripetizione) al **tritone sub** già in `accordi-di-passaggio`:
  la V7/x si può sostituire col suo ♭II7.

**`[CALC]` — `test_dominanti_secondarie`.** La V7/x è un dom7 (0,4,7,10) sulla
quinta giusta sopra x; il ii-V di x; il ciclo delle quinte.

**`[LIB]`:** Piston, *Harmony* (5ª ed.), «Secondary Dominants»; Smith cap. VIII.
⚠️ Pagine da verificare sui PDF.

**Vincoli:** non incatenarne troppe senza tornare (diventa modulazione — stesso
principio del prestito); il bersaglio dev'essere maggiore o minore, non
diminuito.

## Feasibility — perché non serve codice

Il vocabolario di sigle di `musica.py` è già completo: `7, m7, maj7, m7b5 (ø7),
dim7`, e gli alterati `7b9, 7#9, 7#5, 7b13, 7alt`. Le dominanti secondarie sono
semplici `7` su qualunque fondamentale, quindi si parsano già; `MU.armonia`
calcola le note **dalla sigla, non dalla scala**, e la condotta (`condotta=True`,
default) muove poco le voci. **Nessuna aggiunta a `song.MODI`, nessuna funzione
nuova.** Il lavoro è documentazione + due guardiani `[CALC]`.

## Come si realizza

- `set_scale(doc, 'C', 'maggiore')` — la casa; gli accordi con `MU.armonia`;
- rimandi incrociati: `armonia-funzionale` diventa il file-fondazione a cui
  `armonia-modale`, `armonia-prestito`, `accordi-di-passaggio` puntano quando
  dicono «la casa / un giro diatonico che regge»;
- test totali **1233 → 1258** (due guardiani nuovi, 25 check, nessun `_scritto`).

## Cosa resta fuori, e va detto nelle istruzioni

- il **ritmo armonico** — ogni quanto cambia l'accordo — resta scelta del caso,
  come in tutte le istruzioni d'armonia;
- la **dominante alterata** (uso funzionale di ottatonica/esatonale, scala
  alterata/lidia dominante dal minore melodico) è il passo naturale **dopo**
  questa: la tensione, dopo la funzione;
- le code già dichiarate altrove: doppie medianti, diatonic planing.

## Cosa NON rifare

- **non reintrodurre l'esempio all'ascolto** per l'armonia: la variazione di
  metodo dice che il `[CALC]` basta;
- **non inventare le pagine** di Smith e Piston: si aprono i PDF e si verifica,
  come per le altre istruzioni;
- **non duplicare il tritone sub:** vive in `accordi-di-passaggio`, qui è un
  rimando.
