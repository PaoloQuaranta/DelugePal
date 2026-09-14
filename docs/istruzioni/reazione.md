# Reagire alla forma: basso e batteria che non si applicano acriticamente

**A cosa serve.** Una parte ritmica — basso o batteria — non va **applicata
uguale** su tutto il pezzo: deve **reagire** a cosa succede intorno. Fare spazio
dove la melodia è fitta, riempire dove tace, addensarsi verso il culmine. È il
difetto d'origine di questo progetto, e la sua correzione.

È priorità 3 (ritmo), e usa la [forma](struttura.md): il basso e la batteria
reagiscono a **due scale** — la **battuta** (complementare la melodia) e la
**sezione** (seguire l'[arco](arco-dinamico.md)).

**Cosa ti serve prima di cominciare:** la parte di riferimento (la melodia, il
comping — ciò a cui reagire) e la forma.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[MIS]` | misurato su un corpus |
| `[CALC]` | calcolo sulla reazione, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

⚠️ **Ritmo, quindi l'ascolto pieno.** Il `[CALC]` misura *se* la parte reagisce;
l'orecchio dice se **respira** col pezzo.

---

## Il principio: il difetto d'origine, in due parole

⚠️ Il verdetto che ha fatto ripartire il progetto (utente, 11 settembre 2026):

> «La batteria suona **discontinua** rispetto a basso e piano che sono strettamente
> correlati alla sezione ritmica, e non le puoi **applicare acriticamente**.»

Sono **due** guasti in uno, e il generatore a dadi li aveva tutti e due:

- **applicata acriticamente** = la parte è **uniforme**. Il basso usciva a **4,00
  note per battuta, deviazione 0,00**: identica ogni battuta, un metronomo;
- **discontinua** = la parte **varia ma è scollegata** da ciò che le succede
  intorno. Varia, sì, ma a caso — non risponde a niente.

⚠️ **Reagire è il contrario di tutti e due: variare, E che la variazione c'entri.**
Il [walking](walking.md) ha già tolto l'uniformità (deviazione 0,94, non 0,00);
qui si aggiunge il **c'entrare** — la correlazione con il resto.

---

## Il vocabolario: quattro verdetti

`[CALC]` `MU.reazione` guarda, battuta per battuta, la **densità** della parte
(quante note) e la confronta con quella del riferimento:

| verdetto | cos'è | come suona |
|---|---|---|
| **uniforme** | densità piatta (deviazione ~0) | applicata **acriticamente** — il difetto d'origine |
| **scollegata** | varia, ma senza correlazione col riferimento | **discontinua** — l'altro difetto |
| **complementa** | cala dove il riferimento è **fitto** (correlazione negativa) | fa **spazio**: call-and-response |
| **segue** | si addensa **col** riferimento (correlazione positiva) | rinforza — tipico verso il culmine |

⚠️ **`complementa` e `segue` sono i due modi buoni**, `uniforme` e `scollegata` i
due guasti. Il più comune, e quello che `batteria_scritta.py` fa a mano, è
**complementare**: la batteria è rada dove il tema è fitto, piena dove tace.

---

## Reagire a due scale

`[DEC]` Una parte reagisce a **due** livelli, e servono tutti e due:

1. **la battuta — complementare la melodia.** Dove il riferimento è fitto, fai
   spazio (tieni una nota, lascia cadere un movimento); dove tace, riempi. È il
   call-and-response, misurabile con `MU.reazione` contro la melodia;
2. **la sezione — seguire l'[arco](arco-dinamico.md).** Attraverso la forma, la
   densità del basso e della batteria **sale al culmine e ricade**, come tutto il
   resto (`[MIS]` casella 9). È la stessa leva della densità dell'arco, applicata
   alla sezione ritmica.

⚠️ **Non confondere le due scale:** dentro una sezione stabile si **complementa**
la melodia (micro); attraverso le sezioni si **segue** l'arco (macro). Una parte
può fare le due cose insieme.

---

## Come si scrive, materialmente

L'AI scrive la parte (quali note, dove fare spazio); `MU.reazione` **misura** se
reagisce — non compone, come `contrappunto`.

```python
from delugexml import musica as MU

melodia = MU.linea([...])          # il riferimento
basso   = MU.linea([...])          # la parte che deve reagire

print(MU.racconta_reazione(basso, melodia, nomi=('basso', 'melodia')))
# -> "uniforme" (male), "scollegata" (male), "complementa"/"segue" (reagisce)
```

`MU.reazione(parte, riferimento)` `[CALC]`: densità per battuta delle due, la
**deviazione** della parte (sotto ~0,75 è piatta = uniforme) e la **correlazione**
col riferimento (negativa = complementa, positiva = segue, vicino a zero e con
variazione = scollegata). Blindato da `test_reazione`.

⚠️ **Vale per il basso E per la batteria.** Nell'esempio è il basso;
`batteria_scritta.py` fa lo stesso per la batteria da sempre (rada dove il tema è
fitto), e ora `MU.reazione` lo può **misurare**.

---

## Esempio lavorato: lo stesso tema, due bassi

`[OSS]` **Ascoltato il 14 settembre 2026**, caricato sul Deluge (`REAZIONE01`). In
[`tools/reazione_scritto.py`](../../tools/reazione_scritto.py): la stessa melodia
(densità che alterna rado/fitto, `1 4 1 4`), due bassi di fila —

| passata | basso | densità | `MU.reazione` |
|---|---|---|---|
| 1 | **uniforme** | `4 4 4 4` | `uniforme` (deviazione **0,00** — il difetto d'origine) |
| 2 | **reattivo** | `4 1 4 1` | `complementa` (correlazione **−1,00**) |

Il basso uniforme rimette in scena il difetto (4,00 note per battuta, deviazione
zero); il reattivo **cammina dove il tema tace e tiene dove è fitto**. **Verdetto:
«suona giusto, approvato».** ⚠️ Il basso reattivo **respira** col tema, l'uniforme
suona meccanico — il difetto d'origine del progetto e la sua correzione,
all'orecchio. Passa al primo colpo.

---

## Cosa NON fare

- **non applicare una parte uguale su tutto il pezzo:** è il difetto d'origine —
  `MU.reazione` lo chiama `uniforme`;
- **non farla variare a caso:** variare senza c'entrare è l'altro difetto,
  `scollegata` — «discontinua»;
- **non complementare quando servirebbe seguire (e viceversa):** dentro una
  sezione fai spazio, verso il culmine addensati;
- **non confondere reagire con riempire:** reagire è a volte **togliere** —
  spesso la reazione giusta a una melodia fitta è tacere.

---

## Cosa manca a questa istruzione

- la reazione a **più riferimenti insieme** (il basso rispetto a melodia **e**
  batteria): oggi `MU.reazione` guarda una coppia per volta;
- l'**interazione** vera (non solo densità: il basso che raccoglie un accento
  della batteria, la batteria che segue un fraseggio): la densità è una prima
  misura, non tutto;
- ~~i **groove template** applicati alla parte reattiva~~: **scritto** in
  [`groove-template.md`](groove-template.md) — il tocco (velocity e microtiming di
  un batterista vero) sopra la reazione;
- la reazione fuori dal jazz (l'automazione dei generi elettronici): su domanda.
