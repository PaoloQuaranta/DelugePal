# La scala esatonale (whole-tone)

**A cosa serve.** Vuoi un colore **sospeso**, che galleggia e non si posa da
nessuna parte: il suono «acquatico» di Debussy. L'esatonale è quella scala —
l'altra faccia simmetrica dopo l'[ottatonica](scala-ottatonica.md).

È priorità 1 (armonia), una delle scale non diatoniche che l'utente usa.

⚠️ **È gemella dell'[ottatonica](scala-ottatonica.md):** tutt'e due simmetriche,
statiche, senza funzione (come l'[armonia modale](armonia-modale.md)). Il colore
però è diverso — l'ottatonica è **tesa** (dim7, dom7♭9), l'esatonale è
**sospesa** (aumentate, dom7♯5).

**Cosa ti serve prima di cominciare:** una nota di partenza (per simmetria ce ne
sono sei equivalenti) e il registro.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sugli intervalli, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

⚠️ **La fonte qui è Piston, non Smith.** Il *Jazz Theory* di Smith tratta
l'ottatonica ma **non** la whole-tone (verificato): per questa scala si cambia
libro.

---

## Il principio: colore simmetrico, non funzione

`[LIB]` Piston, *Harmony* (5ª ed.), cap. 31 «After Common Practice», «The
Whole-Tone Scale», p. 490: *«la scala esatonale di sei note è una partizione
simmetrica dell'ottava cromatica.»*

Essendo **tutta di toni**, è simmetrica per tono: trasposta di due semitoni
torna su sé stessa, quindi esistono solo **2 esatonali distinte**.

⚠️ **Non ha la quinta giusta, e questo decide tutto.** Tutte le distanze sono
toni: niente quinta giusta, niente terza minore → **nessuna triade consonante,
solo aumentate**. È la ragione tecnica del suo galleggiare. `[LIB]` Piston, cap.
28, p. 439: *«una successione cromatica di triadi aumentate perde il senso di
tonalità definita… questa simmetria suggerisce l'origine della scala
esatonale.»*

Come l'ottatonica: **colore statico, non funzione**. Non risolve; sotto una
cadenza, collassa.

---

## Cos'è, materialmente

Sei note, tutte a un tono l'una dall'altra. In Do: **do re mi fa# sol# la#**
(`0,2,4,6,8,10`) — è quella in `song.MODI` (`'esatonale'`). L'altra esatonale
parte un semitono sopra (do# re# fa sol la si).

`[CALC]` Il test `test_scala_esatonale` blinda: è **simmetrica per tono**
(+2 = sé stessa), ha **6 note**, ed esistono **2 forme distinte**.

---

## Il vocabolario: cosa genera

| accordo | esempio | perché |
|---|---|---|
| **triade aumentata** | C+, D+ | **solo 2 distinte** nella scala (C+ = E+ = G#+; D+ = F#+ = A#+); le due insieme fanno l'intera scala |
| **dom7♯5** | C7♯5 | su ogni grado, tutto dentro la scala |
| **dom7♭5** | C7♭5 | idem |

⚠️ **La mossa che fa sentire la scala: i dom7♯5 paralleli che salgono per tono.**
`C7♯5 → D7♯5 → E7♯5 → …` — cambiano di colore ma restano nello stesso campo
simmetrico, e non puntano a nessuna casa. È il galleggiamento.

---

## Come si stabilisce

1. **scegli una forma** e una nota di partenza;
2. **muoviti per toni** — il ciclo di dom7♯5 che sale, o due triadi aumentate che
   si alternano: la simmetria resa udibile;
3. **non risolvere.** Niente cadenza, niente tonica: il colore sta nel galleggiare;
4. **fai suonare note della scala in melodia** — una linea whole-tone in cima
   dichiara la scala.

---

## Come si scrive, materialmente

```python
from delugexml import song as S, musica as MU

S.set_scale(doc, 'C', 'esatonale')
note = MU.armonia('C7#5 | D7#5 | E7#5 | F#7#5', registro='do3', durata='1/1')
```

⚠️ Voicing **per terze** (`'chiuso'`); la condotta delle parti trova le note
comuni fra un accordo e il successivo.

---

## Esempio lavorato: il ciclo che sale per tono

`[OSS]` La seconda scala simmetrica provata — 12 settembre 2026. In
[`tools/esatonale_scritto.py`](../../tools/esatonale_scritto.py).

**L'idea:** il colore sospeso puro, da zero. Otto battute, tre voci, niente
batteria.

**La progressione** — i dom7♯5 che salgono per tono, i sei distinti più il
ritorno:

```
C7#5 | D7#5 | E7#5 | F#7#5 | G#7#5 | A#7#5 | C7#5 | D7#5
```

tutti dentro una sola esatonale. In cima, una **melodia ondeggiante whole-tone**
(sol#-la#-do-re-mi-re-do-la#).

**Dove si gioca:** il ciclo sale per toni e **non si posa** — niente quinta
giusta, niente cadenza, niente casa. Il colore sta nel galleggiare.

**Verdetto: approvato.** La whole-tone regge come colore, costruita dal nulla.
Con questo il progetto ha **tutt'e due le scale simmetriche** — l'ottatonica
tesa e l'esatonale sospesa — ognuna provata all'ascolto.

---

## Cosa manca a questa istruzione

- **il cromatismo** — non una scala con un centro ma una condotta (il movimento
  per semitoni): un capitolo a sé;
- **l'uso funzionale** — il dom7♯5 che **risolve** (la tensione alterata del
  jazz), opposto del colore statico di qui;
- **le altre scale artificiali** non simmetriche (Piston, cap. 31, le tratta
  accanto a questa).
