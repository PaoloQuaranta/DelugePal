# Le medianti cromatiche

**A cosa serve.** Vuoi uno scarto d'accordo che sorprende ma resta morbido: da un
accordo a un altro **a distanza di terza**, legati da una nota che non si muove.
È il colore «cinematografico» — l'accostamento eroico o di meraviglia delle
colonne sonore.

È priorità 1 (armonia), la seconda faccia del **cromatismo** dopo l'[armonia
parallela](armonia-parallela.md).

⚠️ **È colore, non movimento.** Il planing è uno stream parallelo; la mediante
cromatica è un **accostamento** di due accordi a terza, tenuti insieme da una
nota comune. E a differenza del prestito, la casa non cambia modo: è un colore
cromatico sopra una casa che resta.

**Cosa ti serve prima di cominciare:** una **casa** (un accordo di riferimento) e
la direzione della terza (su o giù).

---

## Il grado di prova

| | |
|---|---|
| `[CALC]` | calcolo sulle note, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

⚠️ **Qui manca il `[LIB]`, ed è una scelta dichiarata.** Il termine «mediante
cromatica» è moderno (neo-riemanniano) e **non compare** nei libri in casa
(verificato su Piston e Smith). Il rigore viene allora dal **`[CALC]`** — il
fatto della nota comune, che è calcolabile e testato — non da una pagina. Piston
fa da contesto (cap. 28, «Other Chromatic Chords»), ma non lo si cita come se
nominasse la cosa.

---

## Il principio: a terza, una nota in comune

Due triadi le cui fondamentali distano una **terza** e che **non** sono
diatonicamente imparentate condividono **una sola** nota. È questo a distinguerle
dalle medianti diatoniche (Do → Mi m), che di note in comune ne hanno **due**.

`[CALC]` In Do maggiore, verificato da `test_medianti_cromatiche`:

| mediante | accordo | nota in comune | intervallo |
|---|---|---|---|
| **♭VI** | La♭ (A♭ C E♭) | **do** | terza maggiore, giù |
| **III** | Mi (E G# B) | **mi** | terza maggiore, su |
| **♭III** | Mi♭ (E♭ G B♭) | **sol** | terza minore, su |
| **VI** | La (A C# E) | **mi** | terza minore, giù |

La nota comune fa la **morbidezza** (una voce non si muove); le altre due si
spostano di un semitono o un tono, e quello scarto è la **sorpresa**. Niente
funzione: è un colore, non una cadenza. `[DEC]` Il ciclo delle medianti a terza
maggiore — **Do → La♭ → Mi → Do** — torna a casa dopo tre passi (è l'asse
dell'accordo aumentato).

---

## Il punto tecnico: la condotta va TENUTA

⚠️ `MU.armonia(..., condotta=True)` — il **default**, e qui serve. La condotta
tiene ferma la nota comune e muove le altre di poco: è proprio lei a far sentire
la morbidezza della mediante. È **l'opposto del planing**, dove la condotta
andava spenta. Verificato: su `C | Ab | E | C` la condotta tiene il do (Do→La♭) e
il sol# (La♭→Mi).

---

## Come si stabilisce

1. **parti da una casa** (Do);
2. **vai a una sua mediante cromatica** — scegli dalla tabella per il colore:
   La♭ (scuro, eroico), Mi (luminoso, meraviglia);
3. **tieni la nota comune** e muovi il resto di poco (`condotta=True`);
4. **torna a casa** — o gira (Do→La♭→Mi→Do). ⚠️ **Non risolvere la mediante per
   dominante**: diventerebbe una tonicizzazione, un'altra cosa.

---

## Come si scrive, materialmente

```python
from delugexml import song as S, musica as MU

S.set_scale(doc, 'C', 'maggiore')     # la casa; le medianti sono colore sopra
note = MU.armonia('C | Ab | C | E | C', registro='do3', durata='1/1')
# condotta di default (True): la nota comune tiene
```

---

## Esempio lavorato: Do fra le sue medianti

`[OSS]` La seconda faccia del cromatismo provata — 13 settembre 2026. In
[`tools/medianti_scritto.py`](../../tools/medianti_scritto.py).

**L'idea:** il colore cinematografico puro, da zero. Otto battute, tre voci,
niente batteria.

**La progressione** — Do fra le sue due medianti maggiori, con ritorno a casa:

```
C | Ab | C | E | C | Ab | E | C
```

`condotta=True`: su ogni salto una nota resta ferma (il **do** su Do↔La♭, il
**mi** su Do↔Mi), e le altre si muovono di poco. La tromba tocca le note
cromatiche nuove (il mi♭ di La♭, il sol# di Mi).

**Dove si gioca:** lo **scarto di terza** morbido-ma-sorprendente. La♭ scende
scuro/eroico, Mi sale luminoso; la casa (Do) resta il riferimento, e nessuna
mediante risolve per dominante.

**Verdetto: approvato.** Con questo il cromatismo ha due facce provate — il
**planing** (lo stream parallelo) e la **mediante** (lo scarto di terza). Anche
qui l'armonia ha retto al primo colpo.

---

## Cosa manca a questa istruzione

- **le doppie medianti cromatiche** — a terza ma senza **nessuna** nota in comune
  (Do → Fa#): più distanti, più straniate;
- **il diatonic planing** — far scivolare una forma dentro una scala;
- **gli accordi di passaggio/approccio** cromatici — l'ultima faccia del
  cromatismo, quella funzionale.
