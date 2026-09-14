# Il groove template: il tocco di un batterista vero

**A cosa serve.** Posare la **velocity** e il **microtiming** di **un** batterista
vero su un pattern di batteria scritto da noi. È **il tocco sopra la
[reazione](reazione.md)**: la parte reagisce già alla forma (rada dove il tema è
fitto), e il template le dà la **mano di una persona** al posto di un metronomo —
la cassa sfiorata, i fantasmi del rullante, il piede del charleston che pesa e
anticipa, il ride che respira.

È priorità 3 (ritmo). L'infrastruttura è scritta da tempo (`GR.profilo` legge,
`MU.applica_groove` posa): questa istruzione dice **come e quando** usarla, e le
trappole, ognuna già pagata.

**Cosa ti serve prima di cominciare:** un pattern di batteria scritto (da
[`batteria-jazz.md`](batteria-jazz.md), voci da `MU.passi()`) e un'**esecuzione
nominata** del Groove MIDI Dataset.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[MIS]` | misurato su un corpus |
| `[OSS]` | osservato — all'ascolto, o nei byte sul dispositivo |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ **Ritmo, quindi l'ascolto pieno.** I rapporti di `applica_groove` dicono *che*
il tocco è posato; l'orecchio dice se fa la differenza fra **una macchina e una
persona**. ⚠️ E la posizione è la parte più **sottile**: vedi «cosa si sente».

---

## Cos'è, e soprattutto cosa NON porta

Tre decisioni, e ognuna chiude un modo di sbagliare.

**Viene da UNA esecuzione nominata, non da una media.** `[DEC]`
`GR.profilo(base, id)` legge **un solo** file — batterista, stile, BPM e durata,
da nominare ogni volta che se ne cita un numero. Mediare il microtiming di
batteristi diversi lo tira verso zero, cioè **verso la griglia**: si perderebbe
esattamente ciò che si era andati a prendere. Ne segue che un profilo è `[OSS]`
**su quell'esecutore**, mentre la scala di velocity di `GR.scala()` è `[MIS]`
**sull'aggregato** — due affermazioni diverse.

**Porta solo il residuo: lo swing lo fa la song.** `[DEC]` Il profilo misura il
BUR dell'esecuzione e **lo toglie**; quel che resta — di quanto ogni voce arriva
prima o dopo il resto del kit — è il template. Lo swing è di song
(`S.set_swing()`, vale per basso e comping insieme alla batteria): se il template
lo portasse anche lui, sarebbe **applicato due volte**. Il BUR tolto non è
scarto — è il **controllo indipendente** sull'1,61 misurato sulla Weimar: due
corpora, due metodi, e le mediane cadono a due punti di distanza (**59,7% contro
61,7%**, BUR 1,48 contro 1,61, su 41 esecuzioni e 5 batteristi). `[MIS]` casella 4
di [`../repertori/jazz.md`](../repertori/jazz.md).

**Non inventa.** `[DEC]` Se il pattern chiede un colpo su un passo dove quel
batterista non ha mai suonato, la nota **resta com'è** e il passo finisce in
`senza_appoggio`, che va letto. È lo stesso cancello della sigla sconosciuta in
`MU.armonia()`: un template che si riempie i buchi da sé sarebbe **inventare con
la benedizione della funzione scritta per impedirlo**.

---

## Le tre trappole

⚠️ **Il nome GM non è il ruolo musicale.** `[OSS]` La voce si sceglie dai
**colpi** e dalla **posizione** che `GR.profilo()` riferisce, **mai dal nome**.
Su `drummer1/session3/2` il disegno continuo di crome swingate — il ride,
musicalmente — sta per otto decimi sulla nota **43**, che la mappa GM chiama *tom
basso*; chi scrive `dove='ride'` prende il profilo di un quinto di esecuzione.
(Sull'esecuzione dell'esempio qui sotto il ride è davvero il ride, ma è un caso
fortunato, non una regola.)

⚠️ **Il tempo conta, perché lo scarto è in TICK.** `[DEC]` Un residuo è una
frazione di movimento: scriverlo al **tempo a cui è stato misurato** ne conserva
i millisecondi, a un tempo diverso lo stesso scarto si allunga o si accorcia (a
185 BPM un tick vale 3,4 ms, a 125 ne vale 5,0). Si sceglie il tempo del pezzo
**vicino** a quello del template, o si sa cosa si sta trasportando. Casella 6 di
[`../repertori/jazz.md`](../repertori/jazz.md).

⚠️ **Uno scarto può valere quasi un passo intero → collisioni.** `[OSS]` Dal
taglio per voce (26 agosto 2026) un colpo in ritardo e quello dopo in anticipo
possono finire **sullo stesso tick**. Il Deluge lo accetta, ma `applica_groove`
lo **riferisce** in `collisioni` (regola 4: un'operazione silenziosa non è
correggibile).

---

## Come si applica, materialmente

`MU.applica_groove(note, prof, dove=…)` posa velocity e residuo su ciò che esce
da `MU.passi()`. **Si applica DOPO aver scritto le note**, una voce per volta, e
`dove` è il **nome GM nel profilo** (non il drum del kit).

```python
from delugexml import groove as GR, musica as MU

prof = GR.profilo(base, 'drummer1/session1/49')     # UNA esecuzione, nominata
ride = MU.passi('x...x.x.x...x.x.', da=0)            # lo spang-a-lang
MU.applica_groove(ride, prof, dove='ride')          # ⚠️ MUTA `ride` in posto
# ... lo stesso per rullante, cassa, piede ...
MU.rimappa_dinamica([ride, rullante, cassa, piede], pavimento=55)  # vedi sotto
MU.scrivi(doc, clip_kit, ride, dove='RIDE')         # 'RIDE' = il drum nel kit
```

⚠️ **`applica_groove` è l'unica del modulo che muta la lista** invece di
costruirne una nuova: il risultato è `note`, cambiata; il ritorno è solo il
**rapporto** (`toccate`, `senza_appoggio`, `collisioni`). Da leggere sempre.

---

## Cosa si vede, e cosa si sente

Sono due affermazioni diverse.

**Ciò che si VEDE, ed è meccanico.** `[OSS]` Il Deluge **non riquantizza al
salvataggio**: una clip con scarti da −6 a +2 tick, caricata e risalvata dal
dispositivo, torna con **31 posizioni su 31 conservate**, byte per byte
(§6-terdecies). È la scommessa su cui poggia tutto il template.

**Ciò che si SENTE, ed è un ascoltatore solo.** `[OSS]` La **velocity** si sente
chiara — la cassa sfiorata e i fantasmi contro un accento si distinguono. Il
**residuo di posizione** è sottile: sul giro intero a tempo pieno emerge
soprattutto la velocity, la posizione si stacca al tempo lento. ⚠️ Le domande
all'ascolto vanno fatte **aperte** («cosa senti?»), non binarie («volume o dove
cadono?»): una domanda binaria porta dentro la risposta (§6-terdecies).

---

## Adattare la dinamica al kit

⚠️ **Il template scende fino a velocity ~24 (i fantasmi). Su un kit che non dà
voce alle velocity basse — un kit elettronico campionato — quei colpi
spariscono, e la parte suona come se avesse note in meno.** `[OSS]` È il verdetto
dell'utente sulla prima stesura dell'esempio (14 settembre 2026): *«la versione
col tocco lascia fuori troppe note, le cancella»* — e non ne cancellava nessuna,
i conteggi erano identici; era la dinamica misurata a cadere sotto la soglia
udibile del kit.

`MU.rimappa_dinamica(voci, pavimento)` alza il **fondo** fino a `pavimento`,
tenendo **i rapporti** (fantasma < comp < ride < piede): una mappa lineare, il
forte resta dov'è. ⚠️ **Si rimappa l'INTERO insieme di voci in una volta**,
perché la dinamica che conta è quella **di kit** — il fantasma è piano *rispetto*
al ride e al piede; rimappare una voce sola gonfierebbe i fantasmi al fortissimo
dentro la loro riga.

⚠️ **Non è ritoccare la misura, è adattarla allo strumento.** `[DEC]` La forma
resta quella del batterista, cambia il range in cui cade. Resta una **decisione**
(quale pavimento, tarato a orecchio), non una misura — quindi va **dichiarata**,
e `rimappa_dinamica` ritorna da quale range a quale.

---

## Esempio lavorato: lo stesso pattern, due mani

In [`tools/groove_template_scritto.py`](../../tools/groove_template_scritto.py):
lo **stesso** pattern reattivo (spang-a-lang costante, rullante e cassa che
comps dove il tema tace), due passate di fila —

| passata | | `applica_groove` |
|---|---|---|
| 1 | **piatto** | no — ogni colpo a velocity 80, sulla griglia |
| 2 | **tocco** | `drummer1/session1/49` (jazz, 125 BPM) |

Il tocco, in numeri — la velocity **misurata** (mediana del batterista, `[OSS]`),
poi **rimappata** sul range udibile del kit `[55..97]`, e lo scarto in tick:

| voce | il piatto | misurato | rimappato (quel che suona) |
|---|---|---|---|
| **charleston a pedale** (2 e 4) | 80 | 97 / 90, scarto **−4 / −7** | **97 / 93**, **anticipa** |
| **ride** (spang-a-lang) | 80 | 68–88, levare **dopo** (+5) | **80–92** |
| **rullante** (comps) | 80 | fantasmi 24 / 27, accento 66 | **55 / 57**, accento **79** |
| **cassa** (feathering) | 80 | 42 / 44 | **65 / 67**, colpi leggeri |

`[CALC]` I rapporti sono puliti: **0 `senza_appoggio`, 0 `collisioni`** (il
pattern usa solo passi che il batterista suona davvero), e dopo la rimappa
nessun colpo scende sotto il pavimento udibile. Il pezzo è costruito in
`out/TOCCO01.XML` (BPM 125 = il tempo di misura; swing 60 di song, uguale nelle
due passate).

⚠️ **Storia del verdetto.** Prima stesura (senza rimappa), caricata come
`TOCCO02.XML`: *«la versione col tocco lascia fuori troppe note, le cancella»* —
i fantasmi (24) e la cassa (42) sparivano sul KIT009. Aggiunta la rimappa su
`[55..97]` (`TOCCO03.XML`). **Verdetto `[OSS]`, 14 settembre 2026: «ok
funziona».** Il tocco si sente come una mano e non come un metronomo, e nessuna
nota resta fuori. La rimappa non è un accessorio: senza, su un kit elettronico il
template si autodistrugge.

---

## Cosa NON fare

- **non mediare più esecuzioni** in un profilo: tira il microtiming verso la
  griglia, cioè verso zero;
- **non firmare un profilo col nome del genere**: è `[OSS]` su un esecutore, non
  `[MIS]` su un repertorio — un'esecuzione è un musicista;
- **non scegliere la voce dal nome GM**: si sceglie dai colpi e dalla posizione;
- **non lasciare lo swing nel template**: lo swing è di song, altrimenti è
  doppio;
- **non scrivere lo scarto a un tempo lontano** da quello di misura senza sapere
  di quanto lo si allunga;
- **non chiedere un passo che il batterista non ha suonato**: finisce in
  `senza_appoggio` e la nota resta piatta.

---

## Cosa manca a questa istruzione

- l'**aggancio** — quale voce della batteria risponde a un onset del basso fuori
  griglia: `genera_jazz.py --aggancio` lo prova (1,60× la probabilità del
  profilo), ma la misura per cui esiste non è ancora riprodotta all'ascolto
  (§6-vicies, casella 5 di [`../repertori/jazz.md`](../repertori/jazz.md));
- la **soglia di percettibilità** del residuo di posizione: serve un esperimento
  di psicoacustica, non un ascolto in più (§6-terdecies);
- il **pavimento della rimappa** è tarato a orecchio (55 sul KIT009), non
  misurato: dipende da come il singolo kit voce le velocity basse, e va rifatto
  per ogni kit;
- i **feel diversi dallo swing** (spazzole, terzine): un altro corpus, un'altra
  misura;
- il template **fuori dal jazz** (l'automazione dei generi elettronici): su
  domanda.
