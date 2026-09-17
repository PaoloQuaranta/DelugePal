# Scrivere una parte di batteria — HOUSE / TECHNO (four-on-the-floor)

⚠️ **PERIMETRO.** Questa istruzione copre la **four-on-the-floor**: cassa su
**ogni** movimento, e tutto il resto vive **negli spazi fra le casse** (i levare).
Copre due generi vicini su un asse:

| | **house** | **techno** |
|---|---|---|
| tempo | ~120-126 | ~128-140 |
| feel | leggermente **swingato** (lo shuffle house) | **dritto** |
| carattere | caldo, soul, con gli **stab** jazzy | scuro, minimale, ipnotico |
| movimento | il clap e l'open hat | il **filtro** (automazione) |

**Non è** l'hip hop (cassa 1-3, non ogni movimento) né il funk (sincope). Qui la
cassa è **il metronomo**, e la musica sta in ciò che le gira intorno.

---

⚠️ **NIENTE CORPUS, e va detto subito.** Techno e house sono generi
**programmati**, non suonati: il Groove MIDI ha solo `dance` = **7 esecuzioni di
2 batteristi** (`[OSS]`, non `[MIS]` — la lezione del reggae), e non è
four-on-the-floor. Non c'è una libreria house/techno in casa. Quindi questo
documento è **`[LIB]`+`[DEC]`**: la four-on-the-floor è una **convenzione di
genere documentata** (produzione elettronica), non una misura.

**Cosa ti serve prima di cominciare:**

- il tempo (house ~124, techno ~130) e se è swingato (house) o dritto (techno);
- **il basso** — nella house il basso sta **fuori** dalla cassa (sui levare), il
  contrario dell'hip hop. Vedi [basso-house.md](basso-house.md);
- un kit **elettronico** (808/909/CR-78): il suono *è* il genere.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | convenzione di genere documentata |
| `[DEC]` | decisione presa qui, con la ragione |

---

## Il vocabolario — la griglia a 16 passi

`1 e + a  2 e + a  3 e + a  4 e + a`. I **movimenti** sono i passi 0, 4, 8, 12;
i **levare di croma** (la "&") sono 2, 6, 10, 14; i **sedicesimi** sono i dispari.

### La cassa — four-on-the-floor, il motore

```
x...x...x...x...    OGNI movimento
```

`[LIB]` La cassa batte **tutti e quattro i movimenti**, forte e uniforme
(velocity ~105-115). È il cuore pompante del genere: **non si buca** (se non per
un attimo di break). ⚠️ È l'opposto dell'hip hop (1 e 3) e del funk (sincope).

### Il clap / rullante — il backbeat, sul 2 e 4

```
....x.......x...    2 e 4
```

`[LIB]` Nella house è un **clap** (808), sul 2 e sul 4, sopra la cassa. Dà il
respiro. Nella techno minimale può mancare o farsi più raro.

### L'open hat — sui levare, LA firma

```
..x...x...x...x.    la "&" di ogni movimento (i levare di croma)
```

`[LIB]` L'**open hat** che si apre sul **levare** ("&", passi 2-6-10-14) — il
«tss-tss» fra una cassa e l'altra — è il **segno** della four-on-the-floor. È lui
a creare la spinta in levare che la cassa dritta non ha.

### Il closed hat — i sedicesimi, la trama

```
.x.x.x.x.x.x.x.x    i sedicesimi, molli
```

`[LIB]` Il closed hat riempie i **sedicesimi** (o i soli dispari, fuori dai
movimenti) piano, per la trama e il drive. Nella techno spesso è più fitto e
regolare; nella house respira di più.

### La percussione — cowbell, claves, conga

`[DEC]` Nella techno/house la percussione (cowbell 808, claves, shaker, conga)
riempie i levare per l'ipnosi. Con parsimonia, e non sui movimenti (dove c'è già
la cassa).

---

## Il feel — lo shuffle house, o il dritto techno

`[LIB]`+`[DEC]` La **house** ha spesso un lieve **swing** (lo «shuffle»): le crome
dell'hi-hat e degli stab sono spinte in avanti, `S.set_swing(doc, 55)` (un lilt
leggero, non la terzina). La **techno** è **dritta**: `S.set_swing(doc, 50)`.
⚠️ Lo swing muove le crome/sedicesimi, non i movimenti: la cassa four-on-the-floor
resta ferma comunque.

---

## I vincoli

| vincolo | perché |
|---|---|
| **la cassa non si buca** | è il motore: ogni movimento, sempre (salvo il break) |
| **l'open hat sta sul levare, non sul movimento** | se cade sul movimento copre la cassa e ammazza la spinta |
| **il clap non si sposta dal 2 e 4** | è l'ancora del backbeat |
| **il suono è elettronico** | un kit acustico non fa house: serve 808/909/CR-78 |
| **il movimento è nel filtro, non nelle note** | ⚠️ techno/house cambiano nell'**arrangiamento** e nel **filtro** (casella «cosa manca»), non aggiungendo colpi |
| **niente regola su tutte le battute** | la trappola del generatore |

---

## Come si decide UNA battuta

**«La cassa pompa; dove metto la spinta in levare, e cosa lascio all'arrangiamento?»**

1. **Fissa la cassa** su ogni movimento.
2. **Metti l'open hat** sui levare (la firma), il clap sul 2 e 4.
3. **Riempi coi closed hat / percussione** i sedicesimi, piano.
4. **Guarda il basso**: sta sui levare, fuori dalla cassa.
5. **Pensa all'arco**, non alla battuta: house e techno vivono del **build/drop**
   (togliere e rimettere parti su 16-32-64 battute). Vedi «cosa manca».

---

## L'esempio lavorato

`tools/house_scritto.py`: una house — 808 (cassa four-on-floor, clap 2-4, open
hat sui levare, closed hat), basso in levare, stab jazzy (piano), swing 55, ~124
BPM, un giro in La minore. ⚠️ **Verdetto dell'ascolto (17 settembre 2026):**
*«funziona»*.

---

## Cosa manca a questo documento

- ⚠️ **l'arrangiamento (build/drop)**: è l'**essenza** del genere, e non sta in
  una battuta — è l'arco su 32-64 battute (entrano/escono le parti, il filtro si
  apre). Vive in `arranger.py` e nell'automazione; qui c'è solo il groove;
- ⚠️ **il filtro in movimento**: lo sweep del cutoff (con LFO via patch cable, o
  automazione) è metà del genere. C'è la libreria (`sound.set_patch_cable`,
  l'automazione del cutoff), ma l'esempio non lo usa ancora;
- **il suono fine**: il kick pompato/sidechain, il reverb, il riverbero — sound
  design (`dsp-recipes`);
- il **`[MIS]`**: non esiste, e non è una lacuna da colmare col corpus (sono
  generi programmati).
