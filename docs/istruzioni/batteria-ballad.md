# Scrivere una parte di batteria — feel BALLAD (spazzole)

⚠️ **PERIMETRO.** Questa istruzione copre **un feel solo**: la batteria della
ballad jazz — **spazzole**, tempo lento, molto spazio. **Non è il giggidì** del
bebop: il ride non martella, il polso è morbido e la parte lascia respirare
tutto il resto.

---

⚠️ **Questo documento è quasi tutto `[LIB]` e `[DEC]`, ed è la cosa da sapere.**
Il **Groove MIDI non ha un feel «ballad»** (verificato: nessuna etichetta), e la
Weimar dà il solista, non la batteria. Quindi qui **non c'è groove template né
scala di velocity misurata** — al contrario di swing e funk. La parte poggia
sulla letteratura e su decisioni dichiarate.

**Cosa ti serve prima di cominciare:**

- la forma, e dove sono i punti di respiro (fine frase, ponte, culmine);
- **il basso e il comping** — a tempo di ballad la batteria è la voce più
  discreta: sostiene, non guida. Vedi [basso-ballad.md](basso-ballad.md);
- il tempo: lento, **~50-70 BPM**.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura didattica, con fonte |
| `[MIS]` | misurato su un corpus (**qui non ce n'è**) |
| `[DEC]` | decisione presa qui, con la ragione |

---

## 1. Le spazzole, e come si rendono sul Deluge

`[DEC]` La spazzola fa due gesti: lo **strofinìo** (il movimento circolare
continuo sul rullante, un tappeto di suono senza attacchi netti) e i **colpetti**
morbidi. Il Deluge, senza un campione di spazzole, non li fa: qui si usa un **kit
acustico suonato pianissimo** come ripiego — velocity basse (30-55), il rullante
tenuto morbido. ⚠️ **Non è la stessa cosa:** le spazzole vere sono un campione, e
restano in «Cosa manca». Ma il *feel* — lento, soft, spazioso — passa lo stesso.

## 2. Il vocabolario

⚠️ **Il pattern fondamentale della ballad NON è il ride.** `[LIB]` DrumHelper /
DRUM! Magazine: la mano sinistra fa uno **strofinìo ovale continuo** con la
spazzola sul rullante — un tappeto di suono sostenuto — mentre la destra tocca il
**charleston sul 2 e sul 4** (o un pattern sul ride). Sul lento lo strofinìo si fa
più ampio e lento, i tocchi più morbidi. **Il «ride pattern» migra sul rullante**,
perché a quel volume il ride col bastone non c'è.

### Il rullante — lo strofinìo, il MOTORE

È la voce principale, non un colore. Lo strofinìo continuo non è rappresentabile a
colpi: si approssima con **tocchi morbidi e fitti** (semiminime, o terzine) a
velocity bassissima (25-35), che suggeriscono il tappeto sostenuto. Non è il
backbeat accentato del funk: è un **mormorio**.

### Il charleston (a mano molle o a pedale) — su 2 e 4

```
....x.......x...    2 e 4, morbido
```

La destra che tocca il 2 e il 4, piano. Al posto del giggidì.

### La cassa — feathering, leggerissima

```
x...............    solo il 1, appena sfiorata
```

`[LIB]` La cassa «feathered» del jazz (vedi [batteria-jazz.md](batteria-jazz.md)),
qui ancora più leggera: sul 1, quasi inudibile.

### Il ride / i piatti — solo accenti, MAI lo spang-a-lang

⚠️ `[LIB]` DrumHelper: a tempo di ballad **la maggior parte dei batteristi NON
suona il pattern del ride col bastone** (lo spang-a-lang) — *«the volume just
isn't there»*. Il ride resta per **accenti** morbidi, o un colpo sul 1 (o sul 1 e
sul 3), non per tenere il tempo. ⚠️ **Lo spang-a-lang fitto è una texture di
swing medio, non di ballad** — ed è l'errore in cui è facilissimo ricadere per
riflesso (ci sono ricaduto io, nella prima versione della demo).

---

## 3. La terzina, e come si ottiene

`[DEC]` La ballad jazz è quasi sempre a **terzina** (il pulse ternario lento). La
griglia del Deluge è a **16 passi** e le terzine native non le fa
([batteria-jazz.md](batteria-jazz.md), «cosa manca»). Si ottiene il lilt con
**`S.set_swing(doc, 66)`**: a 66-67 il levare cade sulla terzina (misurato nel
sorgente del firmware, vedi la docstring di `set_swing`). Così le crome dello
strofinìo del rullante e del comping prendono il feel ternario senza le terzine
vere.

⚠️ Lo swing muove le **crome**, non le minime: il basso in 2 non lo sente
([basso-ballad.md](basso-ballad.md)), lo strofinìo e il comping sì.

---

## 4. I vincoli

| vincolo | perché |
|---|---|
| **niente spang-a-lang sul ride** | `[LIB]` il giggidì col bastone è una texture di swing medio, non di ballad — il tempo lo tiene lo strofinìo sul rullante, non il ride |
| **niente accenti forti** | il backbeat del funk (v127) qui è fuori luogo: tutto è soft, il divario dinamico è piccolo e basso |
| **lascia il vuoto** | a tempo di ballad lo spazio è la sostanza: una battuta in cui la batteria quasi tace è giusta |
| **la batteria non guida** | sostiene il comping e il solista; segue la forma, non la impone |
| **nessuna regola su tutte le battute** | la trappola del generatore, come per gli altri feel |

---

## 5. Come si decide UNA battuta

La domanda, come sempre, ma con la mano leggera:

**«Cosa fanno il comping e il basso, e dove serve appena un tocco?»**

- sotto un accordo tenuto e un basso in 2, basta il pedale sul 2 e 4 e la cassa
  sul 1;
- a fine frase, o dove il solista respira, un colpetto morbido o un mezzo fill di
  spazzola;
- al **culmine** (dove il basso apre al walking, [basso-ballad.md](basso-ballad.md)),
  la batteria può crescere — il ride entra, il polso si fa più presente — e poi
  tornare giù.

---

## L'esempio lavorato

`tools/ballad_scritto.py`: la batteria della ballad — strofinìo sul rullante,
charleston su 2 e 4, cassa feathered, un piatto solo a inizio frase. ⚠️ **La
prima versione aveva lo spang-a-lang sul ride su ogni battuta — un riflesso, non
dalle fonti, e contro questa stessa istruzione; corretto il 16 settembre 2026.**
Verdetto dopo la correzione: *«va bene»*.

---

## Cosa manca a questo documento

- **il campione di spazzole**: senza, è un kit acustico soft. È una scelta di
  **suono** (sound design / un kit con spazzole), non di note;
- **il `[MIS]`**: nessun corpus di batteria ballad. Groove MIDI non ce l'ha;
- **le terzine vere e il rubato**: la griglia a 16 passi dà il lilt solo via
  `set_swing`; il rubato (tempo che respira) non è rappresentabile a BPM fisso e
  resta al solista;
- **lo strofinìo continuo** della spazzola, che nessun campione a colpi rende;
- **l'esempio lavorato** e l'ascolto.
