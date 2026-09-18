# Il suono ACID — il TB-303, la linea, il filtro che evolve

⚠️ **PERIMETRO.** Questa istruzione copre l'**acid**: il suono del **Roland TB-303**
e la linea che lo porta. È un caso del «filtro in movimento» di
[arrangiamento-house.md](arrangiamento-house.md), portato al centro: nell'acid il
**filtro risonante È il pezzo**. Vale per l'acid house, l'acid techno, l'acid in
generale.

> **La cosa da capire:** una linea acid, in altezza, è quasi ferma — una-due note
> che rotolano. A renderla viva è il **filtro**: la risonanza che strilla,
> l'inviluppo che apre il cutoff a ogni nota (lo *squelch*), l'accento, lo slide,
> e il cutoff che **evolve** lungo il pezzo. *«Una battuta non dice niente, è il
> filtro che cambia.»*

---

⚠️ **NIENTE CORPUS** (generi programmati): `[LIB]`+`[DEC]`. Ma i **patch cable** del
303 sono `[OSS]` — attestati nel corpus del progetto: `envelope2→lpfFrequency`
**157** volte (lo squelch), `velocity→lpfFrequency` **129** (l'accento). I valori
del suono sono `[da verificare]` all'orecchio.

**Cosa ti serve prima di cominciare:**

- un synth mono con un LPF risonante (nel progetto: `Square Saw Bass`, già quasi un
  303 — ha `portamento`, `envelope2`, `envelope2→lpfFrequency`);
- una tonica bassa (sub), zona do1-do2;
- il tempo (acid house ~120-127, acid techno ~130-140).

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | convenzione documentata |
| `[DEC]` | decisione presa qui |
| `[OSS]` | patch cable osservati nel corpus |
| `[da verificare]` | valore che si chiude all'orecchio, sul dispositivo |

---

## 1. Cos'è un 303

`[LIB]` Un solo oscillatore con **due forme d'onda**: **dente di sega (saw)** —
l'acid brillante, urlante, il più iconico — o **onda quadra (square)** — più cava,
legnosa, nasale. Entrambe sono vere; l'esempio usa la saw.

Sotto, un **filtro passa-basso molto risonante**, un **inviluppo** che ne apre il
cutoff a ogni nota, l'**accento** (alcune note più forti, che aprono di più il
filtro) e lo **slide** (le note legate glissano).

## 2. Il suono — `MU.acid`

`MU.acid(doc, bersaglio, onda='saw', risonanza=…, cutoff=…, env_cutoff=…,
acc_cutoff=…, glide=…, env2_decay=…)` trasforma un synth in un 303. Tocca due
livelli (come `MU.sidechain`):

- **sullo strumento**: `polyphonic='mono'` (una voce sola, per il glide) e osc1
  `type=onda`;
- **su ogni clip** (è lì che vivono param e patch cable dei synth): **risonanza
  alta**, **cutoff base basso** (perché l'inviluppo abbia spazio per aprirlo),
  **portamento** (il tempo del glide), **env2 percussivo** (attacco 0, decay
  corto, sustain 0 → un blip di filtro per nota), e i due patch cable:
  `envelope2→lpfFrequency` (lo squelch) e `velocity→lpfFrequency` (l'accento).

I valori sono argomenti apposta: il 303 **si tara all'orecchio**, e la correzione
è una parola.

## 3. La linea

`[LIB]`+`[DEC]` **Rada in altezza, fitta in ritmo.** Sedicesimi che rotolano,
quasi tutti sulla **fondamentale**, con qualche **ottava**, **♭7** o **quinta** per
il wiggle. Le due mosse che la fanno acid, e non una scala:

- l'**accento**: alcuni passi a velocity alta (~120 contro ~70). L'accento *è* la
  velocity, e via `velocity→cutoff` apre di più il filtro proprio lì;
- lo **slide**: alcune note **legate** — la `length` che sfora sull'attacco della
  successiva — così in mono il 303 **glissa** da una all'altra.

## 4. Il filtro che evolve — `MU.automatizza`

`[LIB]`+`[DEC]` L'anima dell'acid: il **cutoff** (e spesso la **risonanza**) che
salgono e scendono lungo la sezione. `MU.automatizza(doc, clip, param, da, a,
da_tick, a_tick)` stende una rampa (unità display 0-50) di **qualunque** parametro:
`lpfFrequency` per il cutoff, `lpfResonance` per la risonanza. Nel build il filtro
apre; nel drop è spalancato; in intro/breakdown resta chiuso (muffled).

⚠️ **Solo `lpfFrequency` è verificato sul dispositivo**; la **risonanza in
automazione** è `[da verificare]`. Se non regge all'ascolto, si tiene la risonanza
fissa alta e si rampa il solo cutoff.

---

## I vincoli

| vincolo | perché |
|---|---|
| **risonanza alta, o non è acid** | è la risonanza che «strilla»; senza, è un basso qualunque |
| **la linea non è melodica** | è ritmo + filtro; l'altezza cambia poco |
| **l'accento è la velocity** | non una nota in più: la velocity alta apre il filtro (`velocity→cutoff`) |
| **lo slide è il legato in mono** | note che si sovrappongono + `portamento`>0; in poly non glissa |
| **il movimento è il filtro** | si fa evolvere il cutoff/risonanza, non si aggiungono note |
| **un osc solo** | il 303 ha un oscillatore; due impastano il carattere |

---

## Come si decide UNA sezione

**«Dov'è il filtro, e cosa fa la linea?»**

1. **La linea**: la stessa che rotola (rada in altezza), con accenti e slide.
2. **Il filtro**: chiuso (intro, muffled), che apre (build, `automatizza`), o
   spalancato (drop)?
3. **La risonanza**: alta sempre; se sale nel build, ancora più tensione.
4. **L'arco**: l'acid vive del filtro che sale e scende, non di sezioni che
   cambiano le note.

---

## L'esempio lavorato

`tools/acid_scritto.py`: techno minimale dritta (~132), four-on-the-floor 808, la
linea 303 su La (sedicesimi, accenti, slide), `MU.acid(onda='saw')`, e l'arco
intro → build (il filtro apre: cutoff **e** risonanza) → drop. `verifica()` vuota,
nessuna avvertenza. ⚠️ **Verdetto dell'ascolto (18 settembre 2026): *«l'idea
generale c'è»*** — la risonanza (40) regge, semmai da abbassare un pelo (ritocco
rimandato). I valori restano dei buoni punti di partenza.

---

## Cosa manca a questo documento

- il **`[MIS]`**: non esiste (generi programmati);
- la **taratura** dei valori 303 (risonanza, amount, decay, glide, profondità dello
  sweep): `[da verificare]` finché l'orecchio non la chiude;
- la **distorsione/overdrive** sul 303 (l'acid spinto): un effetto in più, nominato
  non implementato;
- il **vocal chop** (l'altra metà del lead techno): materiale di `audio.py`.
