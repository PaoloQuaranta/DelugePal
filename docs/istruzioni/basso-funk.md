# Scrivere una linea di basso — feel FUNK

⚠️ **PERIMETRO.** Questa istruzione copre **un feel solo**: il basso funk —
una **voce ritmica principale** su una griglia di sedicesimi, non un
accompagnamento che segue gli accordi. **Non cammina.** È l'opposto del walking
([walking.md](walking.md)): là quattro semiminime che collegano l'armonia, qui
un riff fitto e ripetibile che *è* il groove insieme alla cassa.

Il feel si dichiara **prima** di scrivere una nota, e può cambiare da una
sezione all'altra. La casella 1 di `docs/repertori/jazz.md` lo misura pure per
il jazz: il **fusion è al 100% funk**, non in walking.

---

**A cosa serve.** Hai un giro (spesso **statico** nel funk: uno o due accordi,
un vamp) e ti serve il basso. Questa istruzione dice come costruire il riff,
quanto fitto, dove metterlo nel tempo, e come agganciarlo alla batteria.

**Cosa ti serve prima di cominciare:**

- il centro tonale, o il vamp (nel funk l'armonia si muove poco: è il **ritmo**
  a portare il pezzo);
- il registro del basso: **mi1-do3** (numeri di nota MIDI 28-48), come il
  walking;
- **la cassa, colpo per colpo** — nel funk basso e cassa sono una cosa sola.
  Vedi [batteria-funk.md](batteria-funk.md).

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura didattica, con fonte |
| `[MIS]` | misurato su un corpus, con quale e quante esecuzioni |
| `[DEC]` | decisione presa qui, con la ragione |

---

## La misura — cosa fa davvero un basso funk

`[MIS]` **40 basslinee funk** dalla libreria `The_Magic_of_MIDI`
(`to-read/MIDI/`, file *funk* e *Funk-Demo*), **20 944 note** su **3 144
battute**. La traccia di basso presa per nome (`SLAPBASS`, `FINGERDBAS`, «bass»)
o per registro (mediana ≤ 54). ⚠️ **Un limite dichiarato:** sono file MIDI
programmati, non esecuzioni — le **velocity sono quasi piatte** (mediana 106,
ghost < 1%), quindi il corpus dice bene la **densità, le posizioni e gli
intervalli**, ma **non** la dinamica dei ghost, che resta `[LIB]`.

### Quanto è fitto

**Mediana 7,2 note per battuta** (media 6,7; da 1 a 14). ⚠️ **Questo è il
numero che il primo tentativo aveva sbagliato:** un basso funk a 4-5 note per
battuta suona jazzato, non funk. Il funk **riempie** i sedicesimi.

### Dove cadono

`[MIS]` Onset per passo (% delle note):

```
  1   e   +   a   2   e   +   a   3   e   +   a   4   e   +   a
 13   4   6   6   6   4   8   5   7   4   9   4   7   4   9   5
```

Il **movimento 1 è il picco** (13%): è *the one*. Dopo di lui vengono i
**levare** — il "+" di ogni movimento (passi 2, 6, 10, 14, tutti 6-9%). E c'è
attività su **tutti e sedici** i passi: il basso funk sincopa dappertutto,
ancorato al *the one*.

`[LIB]` Soundbrenner, *Funk groove*: *«Most funk grooves live on a sixteenth-note
grid in 4/4»*, e il basso funziona *«as a main rhythmic voice»*, non come
semplice sostegno dell'armonia.

### Che intervalli fa

`[MIS]` Fra una nota e la successiva:

| intervallo | % | cos'è |
|---|---|---|
| **0 semitoni** | **27%** | la nota **ribattuta**: ripetere la fondamentale è la spina del funk |
| 2 semitoni | 18% | un tono: passaggi di scala |
| **12 semitoni** | **15%** | l'**ottava**: la firma del funk |
| 3 semitoni | 11% | terza minore (la pentatonica) |
| 1 semitono | 8% | **cromatico**: approccio a una nota |
| 5 semitoni | 7% | la quarta |
| 7 semitoni | **2,5%** | la quinta — **rara** |

⚠️ **Il funk NON è root-fifth.** La quinta, che regge rock e country, qui è al
2,5%. Il basso funk è fatto di **fondamentale ribattuta + ottava + passi di
scala + cromatismi**. Chi mette root-quinta fa un altro genere.

---

## I quattro principi

`[LIB]` music-composition, `instrument-idiom/bass.md`: *«Funk/R&B: syncopated
riff, ghost-note feel, space as groove»*, ruolo **Riff bass** (*«memorable
repeated figure»*). E TalkingBass / Soundbrenner (web) per il dettaglio.

### 1. Il *the one*

`[MIS]` La nota sul **movimento 1** è l'ancora (il picco degli onset). Quasi
ogni riff funk atterra sul *the one* — di solito la **fondamentale**, forte —
e tutto il resto sincopa **attorno** a lei. `[LIB]` Soundbrenner: *«syncopations,
rests, riffs, and accents feel organized around that downbeat»*.

### 2. Il riff fitto, ripetibile

Il basso funk è una **figura di ~7 note** che si ripete e la riconosci quando
torna. Non è una linea che avanza: è un loop di una-due battute, con variazioni
piccole. La fondamentale **ribattuta** (27% degli intervalli) è ciò che lo tiene
in tensione.

### 3. I ghost note — la propulsione

`[LIB]` TalkingBass, *Funky Ghost Note Basslines*: i ghost sono note **mute e
percussive** («muted while they are plucked»), inserite fra le note piene per
**riempire lo spazio morto** e dare *«propulsion»* — «quasi una seconda parte di
batteria col basso». Il test è netto: *«togli i ghost e suona il groove; quando
li rimetti, il corpo del groove non cambia»*. Cioè: prima le **note del corpo**
(the one, i levare accentati), poi **riempi di fantasmi** i sedicesimi in mezzo.

Sul synth del Deluge un ghost è una nota **cortissima e a velocity bassa**
(30-45 contro 90-110 delle piene): non ha altezza percepita, ha solo ritmo. È lo
stesso divario che fa il tessuto del rullante ([batteria-funk.md](batteria-funk.md)).

### 4. L'aggancio con la cassa

`[LIB]` Soundbrenner: *«The bass often locks closely with the kick drum»*. E
`instrument-idiom/bass.md` dà le due relazioni del funk:

| relazione | effetto |
|---|---|
| **unisono con la cassa** | *«tight, punchy»*: i colpi cadono insieme, il *the one* raddoppiato |
| **il basso riempie i buchi della cassa** | *«groovier»*: la cassa spinge sul 1 e sulle sincopi, il basso tesse i sedicesimi in mezzo |

⚠️ Nel funk valgono **tutt'e due insieme**: le note **del corpo** del basso
cadono dove batte la cassa (the one, il 3), e i **ghost + i levare** riempiono
dove la cassa tace. Le due parti si scrivono **guardandosi**, mai separate.

---

## Il vocabolario dei movimenti

`[MIS]`+`[LIB]`, in ordine di frequenza misurata:

| mossa | quando |
|---|---|
| **fondamentale ribattuta** | il 27% degli intervalli: ribatti la fondamentale sui sedicesimi per la spinta. È la mossa numero uno |
| **salto d'ottava** | il 15%: fondamentale bassa → ottava sopra, sul levare. Slancio, e riapre il registro |
| **passo di scala (tono / terza minore)** | il 18% + 11%: frammenti di pentatonica/blues fra le fondamentali |
| **ghost / dead note** | `[LIB]`: nota muta e cortissima fra le piene, per il ritmo |
| **approccio cromatico** | l'8%: un semitono sotto (o sopra) la nota bersaglio, sul sedicesimo prima. Spinge dentro il *the one* o dentro il cambio |
| **la quinta** | il 2,5%: **poco**. Se ne fai la spina, non è funk |

⚠️ **L'ottava e la fondamentale ribattuta sono ciò che rende un riff "funk"** più
di qualunque scelta d'altezza — insieme ai ghost e allo spazio.

---

## Come si scrive, materialmente

Tu decidi le note. Le primitive le mettono nel file senza sbagliare i conti.
Costruisci prima **il corpo** (poche note piene sul the one e sui levare), poi
**riempi di ghost** i sedicesimi in mezzo.

```python
from delugexml.notes import Note
# 24 tick = un sedicesimo, 96 = un movimento, 384 = una battuta
# riff Em: the one, ribattuti, un'ottava, un cromatico -- ~7 note
riff = [
    (0,  28, 30, 110),   # E1  THE ONE, accento
    (2,  28, 12, 42),    # E1  ghost ribattuto (+di-1)
    (3,  28, 18, 92),    # E1  push (lock cassa a-di-1)
    (6,  40, 24, 100),   # E2  OTTAVA, sul levare del 2
    (8,  28, 18, 90),    # E1  il 3 (lock cassa)
    (10, 31, 18, 86),    # G1  levare del 3
    (14, 32, 12, 82),    # G#1 approccio cromatico all'A della battuta dopo
]
voce = {}
for passo, alt, dur, vel in riff:
    voce.setdefault(alt, []).append(Note(pos=passo*24, length=dur, velocity=vel))
```

⚠️ **Staccato, non legato.** Il funk è **percussivo**: note corte, staccate. Il
legato fa il soul o il sub-bass, non il funk tirato.

L'esempio lavorato è in `tools/funk_scritto.py` (il basso del vamp Em7 | A7).
⚠️ **Verdetto dell'ascolto (16 settembre 2026):** *«meglio, soddisfacente per il
test, niente di stellare»*. Il primo tentativo — scarno e jazzato — era stato
respinto; il «non stellare» è il *fuoco* che manca (la frase, la dinamica dei
ghost, lo slap), elencato in «Cosa manca».

---

## Cosa NON fare

- **non camminare.** Quattro semiminime lisce è walking, un altro feel;
- **non fare il basso scarno.** ~7 note per battuta: sotto le 5 suona jazzato,
  non funk (`[MIS]`);
- **non usare la root-quinta come spina.** È rock/country, non funk (`[MIS]`:
  la quinta è al 2,5%). Ribattuto + ottava + passi + cromatismi;
- **non scrivere il basso senza la cassa davanti.** Le due parti si agganciano;
- **non dimenticare i ghost.** Sono la propulsione: prima il corpo, poi i
  fantasmi in mezzo;
- **non far muovere l'armonia troppo.** Il funk vive su un vamp: porta il ritmo,
  non i cambi.

---

## Cosa manca a questa istruzione

- **la dinamica misurata dei ghost**: il corpus MIDI è a velocity piatta, quindi
  il divario ghost/pieno resta `[LIB]`. Servirebbe un corpus di esecuzioni vere;
- **lo slap** — pollice e pull-off: sul Deluge è una scelta di suono e dinamica,
  non di note. Va in `dsp-recipes`/sound;
- **la frase** su più battute: domanda e risposta fra riff, l'arrivo sul cambio;
- **il rapporto col comping** (chitarra/organo in levare): qui si guarda solo la
  cassa.
