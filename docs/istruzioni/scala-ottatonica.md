# La scala ottatonica (diminuita)

**A cosa serve.** Vuoi un colore che non è né maggiore né minore né modale: un
suono **sospeso, simmetrico**, senza un centro che tiri. L'ottatonica è quella
scala. Questa istruzione dice cos'è, quali accordi genera, e come farla sentire
**senza** che collassi nel tonale.

È priorità 1 (armonia) ed è il primo passo verso le scale non diatoniche che
l'utente usa — le sue song hanno scale a otto note.

⚠️ **È parente dell'[armonia modale](armonia-modale.md), non del
[prestito](armonia-prestito.md).** Come il modale, l'ottatonica è **colore
statico, non funzione**: lì la staticità è una scelta, qui è una proprietà della
scala. Il prestito invece presuppone una casa tonale, che qui non c'è.

**Cosa ti serve prima di cominciare:**

- la **tonica** da cui parti (è solo un punto di partenza: per simmetria la scala
  ne ha quattro equivalenti);
- il registro dove vuoi l'armonia e la melodia.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sugli intervalli, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

---

## Il principio: colore simmetrico, non funzione

`[LIB]` Smith, *Jazz Theory* (4ª ed.), cap. IX, p. 75-76, «The "Diminished"
Scale»:

> «La scala "diminuita" (o "ottatonica") è spesso un'alternativa ricca di colore
> alle scale maggiori e minori. [...] Come l'accordo diminuito, la scala
> diminuita si può trasporre per semitono in una sola direzione due volte
> soltanto: una terza trasposizione riproduce le note dell'originale.»

Due conseguenze che decidono tutto:

1. **Esistono solo 3 ottatoniche distinte**, e la scala è **simmetrica per terza
   minore** — trasposta di tre semitoni, torna su sé stessa.
2. Quindi **niente sensibile, niente centro unico**: per simmetria ci sono
   quattro «toniche» equivalenti. La scala non risolve: shimmera.

Il lavoro, allora, è far sentire la simmetria — e **non risolverla**
tonalmente. Se le metti sotto una cadenza che tira a casa, il colore collassa,
esattamente come un modo che si fa riportare al maggiore.

---

## Cos'è, materialmente

Otto note, dal pattern ripetuto **tono-semitono** o **semitono-tono** — due
rotazioni della stessa scala. `[LIB]` Smith p. 76: la forma **tono-semitono
(WH)** parte dalla fondamentale di un **accordo diminuito**, la
**semitono-tono (HW)** dalla **terza di un accordo di dominante**. In Do:

| forma | note | per |
|---|---|---|
| **WH** (tono-semitono) | do re mi♭ fa solb la♭ la si | i **dim7** |
| **HW** (semitono-tono) | do re♭ mi♭ mi solb sol la si♭ | i **dom7♭9** |

`[CALC]` La HW di Do è `(0,1,3,4,6,7,9,10)` — è quella in `song.MODI`
(`'ottatonica'`). Il test `test_scala_ottatonica` blinda i due fatti che
contano: è **simmetrica per terza minore**, e i quattro dom7 qui sotto ci stanno
tutti dentro.

---

## Il vocabolario: cosa genera

| accordo | esempio | perché |
|---|---|---|
| **dim7** | Cdim7, E♭dim7… | la scala È fatta di due dim7 a distanza di terza minore |
| **dom7♭9** | C7♭9 | la HW sopra la dominante dà ♭9, ♯9, ♯11, 13 |
| **il ciclo dei quattro dom7** | **C7 – E♭7 – G♭7 – A7** | a terza minore l'uno dall'altro, **tutti dentro una sola ottatonica** |

⚠️ **Il ciclo dei quattro dom7 a terza minore è la mossa che fa sentire la
scala.** Perché sono simmetrici, condividono note: muovendoti per terze minori
l'armonia cambia colore ma resta nello stesso campo. È il suono «sospeso,
magico o minaccioso» dell'ottatonica.

---

## Come si stabilisce

1. **scegli una forma** e una nota di partenza (la HW, se pensi in dom7);
2. **gira per terze minori** — il ciclo `C7 → E♭7 → G♭7 → A7`, o due dim7 che si
   alternano: è la simmetria resa udibile;
3. **non risolvere.** Niente ii-V-I, niente cadenza che riporta a un tonale: il
   colore sta proprio nel non avere casa;
4. **fai suonare note della scala in melodia** — una linea ottatonica in cima
   dichiara la scala più di qualunque accordo.

---

## Come si scrive, materialmente

L'ottatonica è una scala nominata: `set_scale` la scrive nella griglia, e gli
accordi li realizza `MU.armonia` dalle sigle (le note le calcola dalla sigla,
non dalla scala):

```python
from delugexml import song as S, musica as MU

S.set_scale(doc, 'C', 'ottatonica')       # la HW di Do
note = MU.armonia('C7 | Eb7 | Gb7 | A7', registro='do3', durata='1/1')
```

⚠️ Voicing **per terze** (`'chiuso'`): la condotta delle parti trova da sé le
note comuni fra un dom7 e il successivo — è la simmetria che te le regala.

---

## Esempio lavorato: il ciclo simmetrico

`[OSS]` La prima prova di una scala non diatonica del progetto — 12 settembre
2026. In [`tools/ottatonica_scritto.py`](../../tools/ottatonica_scritto.py).

**L'idea:** il colore simmetrico puro, da zero. Otto battute, tre voci, niente
batteria.

**La progressione** — il ciclo dei quattro dom7 a terza minore, su due rotazioni:

```
C7 | Eb7 | Gb7 | A7 | C7 | Eb7 | Gb7 | A7
```

tutti dentro una sola ottatonica. In cima, una **linea ottatonica discendente**
(do-sib-la-sol-solb-mi-mib-reb), la scala per intero.

**Dove si gioca:** il ciclo gira per terze minori e **non torna mai a una
tonica** — è la simmetria resa udibile. Niente cadenza, niente casa: il colore
sta nel non posarsi.

**Verdetto: approvato.** La scala simmetrica regge come colore, costruita dal
nulla — il primo terreno non diatonico del progetto, e l'armonia ha tenuto anche
qui al primo colpo.

---

## Cosa manca a questa istruzione

- **l'esatonale** — l'altra scala simmetrica (triadi aumentate, dom7♯5, il suono
  di Debussy): un'altra istruzione;
- **il cromatismo** — che non è una scala con un centro ma una condotta (il
  movimento per semitoni): va trattato a parte;
- **l'uso funzionale** dell'ottatonica: la HW sopra una dominante che **risolve**
  (la tensione del jazz), che è l'opposto del colore statico di qui;
- **vedi anche** Piston, *Harmony* (5ª ed.), cap. 31 «After Common Practice»,
  sulle scale artificiali e simmetriche.
