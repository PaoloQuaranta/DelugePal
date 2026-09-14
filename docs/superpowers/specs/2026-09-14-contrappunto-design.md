# Il contrappunto — progetto

**Data:** 14 settembre 2026
**Cos'è:** la terza faccia della **priorità 2 (forma)**, dopo il voicing (quali
note in un accordo) e il comping (il ritmo dell'accompagnamento). Il contrappunto
mette **due linee alla pari**, o una principale e una che le fa da contro: la
domanda è se si sentono come **due** voci o come **una raddoppiata**.

## Il metodo — `[CALC]` + un ascolto

Come voicing e comping. Il contrappunto ha una parte che si **misura** — gli
intervalli, i moti, le quinte parallele — e una che si **sente**: se «due voci» è
ciò che l'orecchio percepisce davvero. `[LIB]`/`[CALC]` per le meccaniche, un
esempio lavorato **ascoltato** per il giudizio. L'agente arriva al «pronto da
caricare»; l'ascolto è dell'utente.

## Il principio (`[LIB]` Piston, *Counterpoint*, 1970, Introduzione p. 9)

Il contrappunto è l'arte di combinare linee melodiche; il suo nucleo è
l'**intreccio di accordo e disaccordo** — di **dipendenza e indipendenza**. Ognuna
ha tre facce: **armonia** (consonanza / dissonanza), **ritmo** (attacchi insieme /
sfasati), **curva** (moto simile e picchi coincidenti / moto contrario-obliquo e
picchi sfasati). ⚠️ Non è «più indipendenza = meglio»: è il **dosaggio**. Piston
(p. 12, 76): non tutta la musica è contrappuntistica, e il grado di contrappunto
non misura la riuscita.

## Il vocabolario

- **I quattro moti** (`[LIB]` cap. 5, p. 83): **contrario** (opposti — il più
  indipendente), **obliquo** (una tiene, l'altra muove), **diretto**/simile
  (stessa direzione, intervallo diverso), **parallelo** (stessa direzione, stesso
  intervallo — dipendenza massima);
- **il solo divieto** (`[LIB]` p. 83): **quinte e ottave parallele** collassano le
  due voci in una. Terze/seste parallele (p. 85) sono un colore più tenue, non un
  divieto;
- ⚠️ **anti-dogmatismo sulle dirette** (`[LIB]` p. 86): sulle quinte/ottave
  raggiunte per moto simile *«non sono state formulate regole confermate dalla
  pratica»* — Piston chiede **discernimento**, non un elenco. È la stessa cosa che
  il progetto dice da sempre: leggi compositive generalizzabili non esistono;
- **la dissonanza** (`[LIB]` p. 75): la spezia dell'indipendenza, *«specialmente
  sui tempi importanti»*, ma preparata e risolta. ⚠️ In due parti la **quarta è
  dissonante** (p. 125: smette di esserlo nel tre-parti con una nota sotto);
- **le curve** (`[LIB]` p. 76): i picchi non arrivano nello stesso momento; le
  voci possono incrociarsi (p. 79) purché ogni curva resti riconoscibile.

## Il meccanismo — `MU.contrappunto` (codice nuovo)

⚠️ **È un ANALIZZATORE, non un costruttore.** Prende due voci già scritte (la
forma `y -> [Note]` di `melodia`/`linea`/`armonia`) e ne **misura** il rapporto.
È la divisione del progetto — *l'AI decide le note delle due linee, il codice fa i
conti sul loro rapporto* — la stessa di `voci_condotte` per il voicing. Il codice
non compone mai una voce.

Restituisce, per ogni punto in cui le due voci suonano insieme: l'**intervallo** e
la sua **specie** (perfetta/imperfetta/dissonante), il **moto** rispetto al punto
prima; e in aggregato le **quinte/ottave parallele** (segnalate come errore) e le
**dirette** (contate, non condannate — Piston p. 86), la **simultaneità** degli
attacchi (indipendenza ritmica), i **picchi** (indipendenza di curva), le
**dissonanze sul battere**. `racconta_contrappunto` lo dice a parole (regola 4),
**solo ASCII** perché la console di Windows è cp1252 (HANDOFF, 6 settembre 2026).

`[CALC]` — `test_contrappunto`: quinte parallele segnalate su ogni passo e il
contrario no; specie corrette (8a/5a perfette, 3a/6a imperfette, 4a/7a dissonanti
in due parti); moto contrario/obliquo/parallelo; simultaneità e attacchi; picchi
insieme vs sfasati; la pausa non produce intervallo.

## L'esempio lavorato (l'ascolto)

Lo stesso tema con **due seconde voci** sullo stesso materiale — una
**dipendente** (terze parallele, stesso ritmo, stesso picco) e una
**indipendente** (moto contrario, due tenuti/obliquo, ritmo sfasato). Così la
differenza è **solo** il grado di indipendenza. In `tools/contrappunto_scritto.py`.
Il `[CALC]` misura: dipendente = 5 diretto + 2 parallelo, 100% attacchi insieme,
picchi insieme; indipendente = 5 contrario + 2 obliquo, 75% insieme, picchi
sfasati; **nessuna delle due** ha quinte/ottave parallele. Pronto da caricare;
l'utente ascolta → `[OSS]`.

## Struttura / rimandi

- `docs/istruzioni/contrappunto.md` (nuovo); `MU.contrappunto` +
  `MU.racconta_contrappunto` in `musica.py` (con `Verticale`, `Contrappunto`,
  `TICK_PER_MOVIMENTO`); `test_contrappunto` + `test_contrappunto_scritto`;
  `tools/contrappunto_scritto.py`;
- rimandi: `voicing.md` (quali note), `comping.md` (il ritmo del colpo),
  `walking.md` e `armonia-funzionale.md` (il basso e le note-guida sono già linee
  contro cui si scrive un contro).

## Cosa resta fuori (le prossime facce)

- la **struttura** lunga (l'arco del pezzo): l'ultima faccia della priorità 2,
  l'`arranger` c'è già;
- il **tre-e-più parti** (Piston cap. 7-8): oggi il `[CALC]` guarda due voci per
  volta; la quarta giusta e le doppie non sono ancora sue;
- **invertibile** e **canone** (cap. 9-11): tecniche di sviluppo, su domanda;
- le **specie** di Fux: qui si è preso il contrappunto **libero** di Piston (stile
  Bach), non la progressione didattica nota-contro-nota.

## Cosa NON rifare

- **non far comporre una voce al codice**: `MU.contrappunto` analizza, non scrive
  — la divisione l'AI/le primitive è il cuore del progetto;
- **non trasformare Piston in un regolamento**: lui rifiuta le regole inventate
  (p. 86); il `[CALC]` conta le dirette, non le vieta;
- **non chiudere senza l'ascolto**: metodo `[CALC]` + un ascolto;
- **non confondere contrappunto e voicing/comping**: quelli lavorano sotto una
  melodia; il contrappunto mette due linee in rapporto.
