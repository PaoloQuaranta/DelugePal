# Scrivere una linea di basso — feel TWOBEAT (dixieland)

⚠️ **PERIMETRO.** Questa istruzione copre **un feel solo**: il basso del *2-feel*
tradizionale — dixieland, swing antico. **Fondamentale sul 1, quinta sul 3**,
come la ballad, ma **veloce, corto e saltellante**: il basso "salta" fra i due
movimenti forti e spinge dentro la battuta dopo. **Non cammina** (se non per una
battuta di rilancio).

⚠️ **Il 2-feel è condiviso con la BALLAD** ([basso-ballad.md](basso-ballad.md)):
stessa architettura — 1 e 3, minime. Ma i due feel sono l'opposto per
temperamento, e il feel si dichiara **prima**:

| | ballad | twobeat |
|---|---|---|
| tempo | lento, ~58 | veloce, ~180-190 (`[MIS]` mediana 184) |
| articolazione | tenuta, legata, morbida | **corta, staccata, con scatto** |
| tono | scuro, caldo (contrabbasso) | brillante (contrabbasso *slappato*, o tuba) |
| carattere | spazio, calma | **spinta**, "oom-pah", non far dormire il pezzo |

---

**A cosa serve.** Hai un giro dixieland (spesso un giro di dominanti in catena,
o un blues) e ti serve il basso sotto. Questa istruzione dice come tenere il
*due* vivo e saltellante, invece che sonnolento come la ballad.

**Cosa ti serve prima di cominciare:**

- il giro, una sigla per battuta;
- il registro del basso: **mi1-do3** (28-48), come il walking e la ballad;
- il tempo: veloce, **~160-200 BPM**;
- **la controparte sul 2 e sul 4** — il "pah". Nel twobeat il basso fa il 1 e il
  3 ("oom"), e la risposta sta sul 2 e sul 4: il charleston croccante e il
  comping. Vedi [batteria-twobeat.md](batteria-twobeat.md).

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura didattica, con fonte |
| `[MIS]` | misurato su un corpus, con quale e quante esecuzioni |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ **Qui non c'è `[MIS]` sulla linea di basso, come per la ballad.** Il corpus
che *nomina* il twobeat è la **Weimar** (`rhythmfeel='TWOBEAT'`): **32 assoli, 8
solisti** — e sono **al 100% `TRADITIONAL`**: Armstrong, Bechet, Kid Ory, Bix
Beiderbecke, Johnny Dodds. Tempo 71-274, **mediana 184, in gran parte UP**. Ma la
Weimar porta la **linea del solista**, non il basso; il **Jazz Trio Database**
è walking e parte da 102 BPM; il **Groove MIDI** non ha un feel «twobeat». Quindi
la *conferma del genere e del tempo* è `[MIS]`, ma la linea di basso è
`[LIB]`+`[DEC]`.

---

## Il 2-feel, il cuore — 1 e 3, ma con lo scatto

`[LIB]` Riley, *The Art of Bop Drumming*, p. 57, «Playing in "2"» (citato in
`docs/repertori/jazz.md`, casella 1): nel 2-feel il bassista *«suona ritmi
basati sulla minima (movimenti 1 e 3) invece di una pulsazione di semiminime in
walking»*. È la stessa architettura della ballad:

```
mov:   1       2       3       4
       Fond.           Quinta
```

⚠️ **Ma poi Riley dà la chiave del twobeat**, ed è ciò che lo separa dalla
ballad: *«siccome suonare in "2" è meno attivo, devi assicurarti di tenere le
cose vive — suona con un po' di scatto e non lasciare che la musica suoni
addormentata»*. La ballad **è** addormentata di proposito; il twobeat no.

`[DEC]` Lo scatto, in pratica, è tre cose:

1. **note corte.** La fondamentale e la quinta non sono minime tenute (ballad):
   sono **note corte**, staccate — durano meno di un movimento, poi silenzio.
   È il rimbalzo del contrabbasso slappato o della tuba;
2. **velocity più ferma** (~85-95, contro i 60-75 della ballad): il basso
   dixieland tira, non accarezza;
3. **il rilancio** (sotto).

Scegli l'ottava minimizzando l'intervallo fra una fondamentale e la successiva,
come nel walking e nella ballad (`genera_jazz._vicino`).

---

## Il rilancio — la nota che spinge nella battuta dopo

`[DEC]`+`[LIB]` Il basso in due dixieland non resta fermo su 1 e 3: su molte
battute aggiunge una **nota di rilancio** sull'ultima croma (il "levare del 4"),
che porta cromaticamente o per grado alla fondamentale della battuta seguente.
È il "boom-boom, boom" che rende il *due* saltellante invece che quadrato.

```
mov:   1       2       3       4
       Fond.           Quinta      (rilancio) →  Fond. battuta dopo
```

Va usata **con parsimonia** — non tutte le battute, o diventa un metronomo: una
sì e una no, o dove il giro cambia accordo. È l'equivalente della figura
minima-semiminima-semiminima della ballad, ma **più corta e più avanti nel
tempo** (sull'ultima croma, non sul 3-4).

---

## Aprire con una battuta "in 4"

`[LIB]` Come la ballad apre al walking al culmine, il twobeat rilancia
**passando "in 4" per una battuta** — quattro semiminime che camminano verso il
punto d'arrivo, di solito sotto una **dominante** che risolve (il V7 → I). Poi
subito di nuovo in due. `[LIB]` jazz.md casella 1: *il feel cambia dentro il
pezzo* — Riley cita un brano col ponte in due e il resto no. Il *due* e il *4*
si alternano per sezione, non a caso.

---

## Come si scrive, materialmente

```python
from delugexml.notes import Note
# 96 tick = un movimento, 384 = una battuta, 48 = una croma
# 2-feel dixieland in Sib: fond. sul 1, quinta sul 3, CORTE, + rilancio
# (Sib1=34, Fa2=41; rilancio Do#2=37 -> Re della battuta dopo, un D7)
voce = {}
for pos, alt, dur, vel in [
    (0,   34, 72, 92),    # Sib1  il 1  (corto, non minima)
    (192, 41, 72, 88),    # Fa2   il 3
    (336, 37, 48, 80),    # Do#2  rilancio cromatico verso il Re della battuta 2
]:
    voce.setdefault(alt, []).append(Note(pos=pos, length=dur, velocity=vel))
```

⚠️ **Corto e staccato, non legato.** È l'opposto della ballad. La durata breve
(≈ 60-80 tick su una minima da 192) è ciò che fa il rimbalzo. Il legato qui
spegne il feel.

L'esempio lavorato è in `tools/twobeat_scritto.py` (basso in 2 + oom-pah +
batteria dixieland, un giro di dominanti in Sib). ⚠️ **Verdetto dell'ascolto
(17 settembre 2026):** *«ok funziona»*.

---

## Cosa NON fare

- **non fare il basso lento e legato.** Quello è la ballad: qui è corto, brillante,
  con scatto (`[LIB]` Riley: non lasciarlo suonare addormentato);
- **non camminare per tutto il pezzo.** Quattro note fisse per battuta è walking,
  un altro feel — il *4* è solo il rilancio di una battuta;
- **non dimenticare la quinta sul 3.** È lei, contro il pedale di sole
  fondamentali, a fare il *due*;
- **non mettere il rilancio su tutte le battute.** Una sì e una no: se è ovunque
  diventa quadrato e meccanico;
- **non usare `set_swing` per il basso in due.** Lo swing muove le crome; le
  note su 1 e 3 non lo sentono. Serve alle crome della batteria e ai rilanci
  ([batteria-twobeat.md](batteria-twobeat.md)).

---

## Cosa manca a questa istruzione

- **il `[MIS]` sulla linea**: nessun corpus in casa ha il basso del twobeat
  trascritto nota per nota (la Weimar dà il solista, il JTD è walking e parte da
  102 BPM). È lo stesso buco della ballad;
- **lo slap** del contrabbasso (la corda che schiocca sulla tastiera) e la
  **tuba**: sono scelte di **suono**, non di note — vanno in `dsp-recipes`/sound;
- **la frase** su più battute e il dialogo con la front line collettiva (il
  contrappunto dixieland di tromba/clarinetto/trombone), che è l'anima del
  genere e sta nella priorità 2 (contrappunto), non qui.
