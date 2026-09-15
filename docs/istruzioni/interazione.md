# Interazione a livello di evento: chiamata e risposta

**A cosa serve.** Far sì che due parti si **rispondano** — non solo che una faccia
spazio all'altra (quello è la [reazione](reazione.md)), ma che metta i suoi eventi
**dove e quando** l'altra li chiede: **il basso che raccoglie un accento della
batteria, la batteria che segue un fraseggio**. È il passo oltre la reazione: dalla
*quantità* alla *collocazione*.

È priorità 3 (ritmo). ⚠️ **È la faccia UDIBILE dell'interazione**, al contrario
dell'[aggancio](aggancio.md) (microtiming, archiviato perché impercettibile): una
chiamata e risposta si sente, una figura presa insieme si sente.

**Cosa ti serve prima di cominciare:** la parte di **riferimento** (la melodia, il
comping — chi chiama) e la parte che risponde.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sull'interazione, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

⚠️ **Ritmo, quindi l'ascolto pieno.** Il `[CALC]` dice *dove* cadono gli eventi;
l'orecchio dice se è una **conversazione** o un accavallarsi.

---

## Il principio: oltre la densità

`[LIB]` Riley (in [`batteria-jazz.md`](batteria-jazz.md), casella 5): *«rispondi
dove lasciano un buco, tieniti fuori dove sono piene»*, e *«la fine di una frase
chiede qualcosa di diverso dal mezzo»*. È la relazione di **collocazione**, non di
quantità.

⚠️ **Perché la reazione non basta.** `MU.reazione` guarda la **densità per
battuta**: due parti con la stessa densità le vede uguali. Ma un tema che suona sui
movimenti 1-2 e tace sul 3-4, e una risposta che sta sul 3-4, hanno la **stessa
densità** e **collocazione opposta**: la reazione è muta, l'orecchio no. `MU.interazione`
guarda la **presenza di un onset per movimento**, e quella differenza la coglie.

---

## Il vocabolario: `MU.interazione`

`[CALC]` `MU.interazione(parte, riferimento)` guarda, cella per cella (il
movimento), la presenza di un onset nelle due parti:

| verdetto | cos'è | come suona |
|---|---|---|
| **risponde** | eventi nei **buchi** del riferimento (correlazione negativa) | chiamata e risposta: si parlano |
| **insieme** | eventi **sui colpi** del riferimento (correlazione positiva) | **figura** presa insieme se `cattura` è alta, **muro** se è bassa |
| **slegato** | né l'uno né l'altro | gli eventi non c'entrano coi buchi |
| **tace** | la parte non suona | — |

E un secondo numero, la **`cattura`**: degli **accenti** del riferimento, la quota
che la parte prende insieme (un onset nella stessa cella). È «il basso che raccoglie
un accento».

⚠️ **`insieme` non è di per sé un difetto.** Prendere una **figura** insieme (una
botta della sezione ritmica) è musica; pestare a caso sui colpi dell'altro senza
prenderne gli accenti è il **muro** che `batteria-jazz.md` vieta. A distinguerli è
la `cattura`: alta = figura, bassa = muro.

---

## Le due facce, quelle che l'utente ha nominato

`[DEC]`

1. **la batteria segue un fraseggio** → `risponde`: metti gli eventi **nei buchi**
   della frase. Dove il tema tace, rispondi; dove corre, tieniti fuori.
2. **il basso raccoglie un accento** → `cattura`: là dove il riferimento **accenta**,
   piazza un evento **insieme**. È la figura colta al volo.

⚠️ Le due sono **opposte come collocazione** (una nel buco, una sul colpo) e
convivono nel tempo: si risponde per lo più nei buchi, e ogni tanto si **cattura**
una botta grossa. Una parte matura fa tutt'e due.

---

## Come si scrive, materialmente

L'AI scrive la parte (dove risponde, cosa cattura); `MU.interazione` **misura** —
non compone, come `reazione` e `contrappunto`.

```python
from delugexml import musica as MU

print(MU.racconta_interazione(rhodes, tema, nomi=('rhodes', 'tema')))
# -> "risponde" (nei buchi), "insieme" (sui colpi), "slegato", "tace"
#    + correlazione (neg = risponde) e cattura accenti
```

`MU.interazione(parte, riferimento)` `[CALC]`: presenza per movimento delle due, la
**correlazione** (negativa = risponde nel buco, positiva = insieme) e la **cattura**
degli accenti. Blindato da `test_interazione`.

---

## Esempio lavorato: lo stesso tema, due Rhodes

`[OSS]` In [`tools/interazione_scritto.py`](../../tools/interazione_scritto.py): un
tema che **chiama** (una frase sui movimenti 1-2, un buco sul 3-4), e un Rhodes che
stacca un accordo, due passate —

| passata | il Rhodes | `MU.interazione` |
|---|---|---|
| 1 | **pesta** (movimento 1, sopra il tema) | `insieme`, correlazione **+0,55**, cattura **100%** |
| 2 | **risponde** (movimento 3, nel buco) | `risponde`, correlazione **−0,64**, cattura **0%** |

⚠️ **Le due passate hanno la STESSA densità** (uno stab per battuta): cambia solo
*dove* cade. Perciò `MU.reazione` le vede **identiche** (`uniforme` entrambe) mentre
`MU.interazione` le distingue — è la prova, in un test, che l'evento coglie ciò che
la densità non vede. Il pezzo è `out/INTERAZIONE01.XML` (BPM 120), caricato come
`/SONGS/DelugePal/INTERAZIONE01.XML`, riletto byte per byte. ⚠️ **Verdetto `[OSS]`,
15 settembre 2026: «ok funziona».** La conversazione (chiamata sui 1-2, risposta nel
buco del 3-4) si sente contro l'accavallarsi della passata che pesta. A differenza
dell'aggancio, **è un effetto pieno, non sottile**: la collocazione degli eventi si
sente, il microtiming no.

---

## Cosa NON fare

- **non pestare sui colpi del riferimento senza prenderne gli accenti**: è il
  **muro** — `insieme` con `cattura` bassa;
- **non confondere con la reazione**: quella è densità per battuta, questa è
  collocazione per movimento — una parte può passare la reazione e restare slegata;
- **non riempire ogni buco**: rispondere è anche lasciare un buco senza risposta,
  altrimenti la conversazione diventa chiacchiera;
- **non trattare `insieme` come un errore**: una figura presa insieme è musica.

---

## Cosa manca a questa istruzione

- l'interazione a **più di due parti** (il basso rispetto a melodia **e** batteria
  insieme): oggi `MU.interazione` guarda una coppia per volta, come `reazione`;
- la **cella** è fissa al movimento: una risposta in levare (mezzo movimento) la
  coglie solo in parte — si affinerebbe con una cella più piccola, ma più rumorosa;
- l'interazione **fuori dal jazz** (i botta-e-risposta dei generi elettronici): su
  domanda.
