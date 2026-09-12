# Prendere in prestito (modal interchange)

**A cosa serve.** Hai una tonalità di casa — maggiore o minore — e vuoi un
colore che la tonalità diatonica non ha. Lo **prendi in prestito** da un modo
parallelo: stessa tonica, modo diverso. Questa istruzione dice quali accordi si
prendono, da dove, e cosa fa sì che restino un colore invece di cambiare
tonalità.

È priorità 1 (armonia) ed è il **ponte verso l'eclettismo** che l'utente cerca:
un modo controllato di mescolare i colori di modi diversi senza lasciare la
casa.

⚠️ **È l'orientamento opposto a [`armonia-modale.md`](armonia-modale.md).** Lì
l'armonia sta ferma in un modo e si evita ogni spinta tonale. Qui c'è una casa
tonale che funziona, e il prestito è una deviazione momentanea da cui si
rientra. Prima di cominciare, sappi in quale dei due mondi stai: se non c'è una
casa tonale, quello che ti serve è l'armonia modale, non questa.

**Cosa ti serve prima di cominciare:**

- la **tonalità di casa** (es. Do maggiore) e un **giro diatonico** che regge;
- il **punto** dove vuoi il colore;
- se hai una melodia, le sue note (il prestito va d'accordo con la voce in cima).

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sugli intervalli del modo parallelo, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

---

## Il principio: una casa, e un colore preso a prestito

`[LIB]` Smith, *Jazz Theory* (4ª ed.), cap. VIII «Functional Harmony», p. 66:

> «Gli accordi vengono spesso "presi in prestito" dal maggiore o dal minore
> parallelo; per questo si chiamano "accordi presi in prestito". Per esempio, un
> Fm può comparire come IVm nella tonalità di Do maggiore, preso in prestito dal
> Do minore (vedi il ponte di *On the Sunny Side of the Street*).»

L'idea che regge tutto: **la casa resta la casa, e l'accordo preso in prestito è
un ospite.** Colora una battuta e se ne va; il diatonico si riafferma. Il modo
parallelo non prende il comando — se lo prende, non hai preso in prestito: hai
modulato, che è un'altra cosa (Smith la tratta a parte, p. 67-68).

`[LIB]` Smith p. 75 dà la regola generale, e il modo di ritrovare ogni prestito:
*«quando un accordo è preso in prestito dal parallelo... lo si identifica come
un grado della tonalità da cui viene. Per esempio, un Fm7 usato in Do maggiore
lo identifichiamo come IV del Do minore parallelo.»* Quindi per sapere quali
note porta un prestito, lo si legge come un accordo **diatonico del minore
parallelo** — ed è da lì che arriva la sua nota di colore.

---

## Il vocabolario: cosa si prende, e da dove

`[CALC]` In una casa **maggiore**, i prestiti più idiomatici vengono dal **minore
parallelo**: portano le tre note che il minore ha e il maggiore no — la **3ª
minore**, la **6ª minore**, la **7ª minore** (in Do: mi♭, la♭, si♭). È una di
queste la «nota di colore» di ogni accordo, e toglierla lo riporta nel diatonico.

| prestito | accordo in Do | nota di colore | colore | fonte |
|---|---|---|---|---|
| **iv** | Fm | la♭ (♭6) | caldo, plagale, nostalgico | `[LIB]` Smith p. 66 (*Sunny Side of the Street*) |
| **♭VI** | A♭ | la♭ (♭6) | cinematografico, ampio | `[LIB]` Smith p. 75 |
| **♭VII** | B♭ | si♭ (♭7) | modale/rock; il I↔♭VII | `[LIB]` Smith p. 69 (*Killer Joe*) |
| **♭III** | E♭ | mi♭ (♭3) | scuro, bluesy | `[LIB]` Smith p. 75 |
| **Im** | Cm | mi♭ (♭3) | la scivolata luce→ombra | `[LIB]` Smith p. 67 (*On Green Dolphin Street*) |
| **iiø7** | Dm7♭5 | la♭ (♭6) | tensione prima della cadenza | `[CALC]` è il ii7 del Do minore |

⚠️ **Il I→Im è il prestito più netto che ci sia**, e Smith lo mette accanto al
iv: *«un altro prestito comune è il passaggio da I a Im»* (p. 67). Stessa
fondamentale, la terza che cala: tutto il colore si scurisce di colpo, senza
muovere il basso. *On Green Dolphin Street* apre così.

⚠️ **La napoletana, il ♭II, è l'eccezione: non viene dal minore.** `[LIB]`
Piston, *Harmony* (5ª ed.), cap. 26 «The Neapolitan Sixth», p. 407: è la triade
maggiore sul **♭2** (in Do, Re♭), e la sua nota di colore è il **re♭ (♭2)**, che
il minore parallelo non ha — viene dal **frigio** parallelo. Piston la usa
classicamente in **primo rivolto** (la «sesta napoletana») e prima della
cadenza; in Do risolve verso il V o direttamente verso il I. È il colore più
teatrale del gruppo.

`[CALC]` Le note di ogni accordo di questa tabella sono verificate da
`test_armonia_prestito_accordi_dal_parallelo` in `tests/test_all.py`: se qualcuno
cambia `song.MODI`, il test prende il documento che mente.

---

## La direzione inversa: una casa minore

Funziona anche al contrario: una **casa minore** prende in prestito dal
**maggiore** parallelo. `[LIB]` Smith p. 74: in minore i gradi **6 e 7** si
possono alzare, e i gradi alzati sono *«presi in prestito dal maggiore
parallelo»* (la notazione a frecce ↑6, ↑7 serve a ricordare quale forma usare).
Il maggiore parallelo porta tre note che il minore non ha: la **3ª**, la **6ª**
e la **7ª maggiori** (in La minore: do#, fa#, sol#).

| prestito | in La minore | nota di colore | fonte |
|---|---|---|---|
| **IV maggiore** | Re (D F# A) | fa# (♮6) | `[LIB]` Smith p. 74 — la schiaritura dorica |
| **ii minore** | Bm (B D F#) | fa# (♮6) | `[CALC]` dal maggiore |
| **I maggiore (Piccardia)** | La (A C# E) | do# (♮3) | `[LIB]` Piston, cap. 26 e dintorni |

⚠️ **Il IV maggiore è il contrario simmetrico del iv minore** di sopra: là una
casa maggiore prendeva la sottodominante minore (il la♭); qui una casa minore
prende la sottodominante maggiore (il fa#). Stesso grado, il IV, colorato
nell'altro verso.

⚠️ **Il V maggiore NON è un prestito.** In La minore l'E7 (col sol#) è la normale
dominante del minore armonico: il sol# è la sensibile che riporta a casa, non un
colore preso dal maggiore. Chiamarlo prestito vorrebbe dire chiamare prestito
ogni accordo del minore armonico.

`[CALC]` Il test `test_armonia_prestito_casa_minore` blinda questa tabella:
maggiore − minore parallelo = {♮3, ♮6, ♮7}.

---

## I vincoli: cosa lo tiene un prestito, e non una modulazione

| non fare | perché |
|---|---|
| **non restare fuori casa** | il prestito è un ospite: dopo il colore, il diatonico si riafferma. Se la tonalità nuova prende piede, hai modulato — e la modulazione vuole un'altra procedura (Smith p. 67-68) |
| **non incatenare due-tre prestiti di fila** | l'orecchio perde la casa. Un colore alla volta, fra accordi diatonici, si sente come colore; tre di fila si sentono come un cambio di tonalità o come ambiguità |
| **non mettere il prestito in posizione forte senza che risolva** | `[LIB]` Smith tratta questi accordi come preparazioni: stanno bene **prima** di un ritorno a casa, non come punto d'arrivo |
| **non scordare la melodia** | la nota di colore deve poter stare con la voce in cima. Il la♭ del Fm stona se la melodia in quel punto batte il la naturale: il prestito si decide guardando anche la cima, non solo la griglia |

---

## Come si decide, passo per passo

La forma «una decisione locale, poi si compone» — quella che ha fatto
funzionare il walking e l'armonia modale:

1. **parti da un giro diatonico che regge.** È la casa, e deve suonare stabile
   prima che tu la colori.
2. **scegli il punto del colore.** Il più naturale è il **IV che diventa iv**
   (in Do: Fmaj7 → Fm7), o la battuta prima di un ritorno a I.
3. **prendi l'accordo dal parallelo**, scegliendolo dalla tabella per il colore
   che vuoi: caldo → **iv**, cupo e ampio → **♭VI**, modale/rock → **♭VII**,
   teatrale → **♭II napoletano**, scuro di colpo → **I→Im**.
4. **controlla i vincoli**: torni a casa, non ne incateni troppi, la melodia
   regge la nota presa in prestito.

⚠️ **La mossa che li riassume, ed è quella dell'esempio:** il **IV→iv→I**. Il
Fmaj7 porta il la naturale, l'Fm7 lo abbassa al la♭, e il Do torna a casa. Il
colore è tutto in quella nota che scende di un semitono.

---

## Come si scrive, materialmente

La casa si dichiara con `set_scale`; gli accordi, prestito compreso, li realizza
`MU.armonia`, che calcola le note **dalla sigla, non dalla scala** — quindi il
la♭ dell'Fm esce anche se la scala è Do maggiore (`set_scale` scrive come è
disegnata la griglia, non filtra le altezze):

```python
from delugexml import song as S, musica as MU

S.set_scale(doc, 'C', 'maggiore')
note = MU.armonia('Cmaj7 | Fmaj7 | Fm7 | Cmaj7', registro='do3', durata='1/1')
```

⚠️ **Voicing per terze** (il default `'chiuso'`), **non quartale**. `[OSS]` È la
lezione di PERCHE (armonia modale, 11 settembre): le quarte aprono il suono ma
tolgono corpo, e il calore di un prestito come il iv sta proprio nel corpo delle
triadi. Il quartale è un colore del vocabolario, non un traguardo.

---

## Esempio lavorato: il pezzo in Do

`[OSS]` Il primo pezzo armonico del progetto **creato da zero**, e il primo
«creare dal nulla» andato a segno — 12 settembre 2026. Lo script è
[`tools/prestito_scritto.py`](../../tools/prestito_scritto.py); ogni nota è una
scelta, col motivo accanto.

**L'idea:** una casa in Do maggiore, dal nulla, col *iv* minore come colore
centrale. Otto battute, un accordo per battuta, tre voci — Rhodes per gli
accordi, tromba per la melodia, basso sulle fondamentali. Niente batteria.

**La progressione**, col prestito alla battuta 4:

```
Cmaj7 | Em7 | Fmaj7 | Fm7 | Em7 | Dm7 | G7 | Cmaj7
  I     iii    IV     iv    iii   ii    V     I
```

**Dove si gioca:** il IV→iv→I delle battute 3-4-5. La tromba canta il **la
naturale** sul Fmaj7 e lo abbassa al **la♭** sul Fm7, mentre l'armonia fa la
sottodominante minore; poi il Do torna a casa. Il colore è tutto in quel
semitono che scende, in cima.

**Verdetto: «sento la modulazione correttamente» — approvato.** ⚠️ E il fatto
che l'utente l'abbia chiamata «modulazione» è un dato, non un errore da
correggere: il iv preso in prestito è un colore così netto da sentirsi come un
cambio di tonalità, **pur risolvendo a casa**. È precisamente l'effetto cercato
— il prestito che colora senza che la casa se ne vada.

⚠️ **Ha funzionato al primo colpo**, come l'armonia modale e contro le dieci
versioni della batteria: conferma di nuovo che l'armonia è terreno più fermo del
ritmo, come dice il perimetro. E supera il «da zero», che nessuna istruzione
armonica aveva ancora toccato.

---

## Esempio lavorato: il pezzo in La minore

`[OSS]` Il gemello in minore del pezzo in Do, e la prova della direzione
inversa — 12 settembre 2026. Stesso script,
[`tools/prestito_scritto.py`](../../tools/prestito_scritto.py) (le costanti
`*_MIN`).

**L'idea:** una casa in La minore, dal nulla, col *IV maggiore* come colore — la
schiaritura dorica presa dal La maggiore parallelo. Otto battute, tre voci,
niente batteria, come il primo.

**La progressione**, col prestito alla battuta 4:

```
Am | Em | Dm | D | Am | Dm | E7 | Am
 i    v   iv   IV   i   iv   V7   i
```

**Dove si gioca:** il iv→IV delle battute 3-4. La tromba canta il **fa naturale**
sul Dm e lo alza al **fa#** sul Re maggiore, mentre l'armonia fa la
sottodominante maggiore; poi si rientra a casa. ⚠️ L'E7 della battuta 7 è la
normale dominante del minore (col sol#), **non** un prestito.

**È il contrario simmetrico del pezzo in Do:** là una casa maggiore scuriva il
IV in iv (il la che scende al la♭); qui una casa minore schiarisce il iv in IV
(il fa che sale al fa#). Stesso grado, i due versi.

**Verdetto: «sento la schiaritura, approvato».** Il IV maggiore in minore regge
come il iv minore in maggiore — al primo colpo, in tutt'e due i versi.

---

## Cosa manca a questa istruzione

- **la direzione inversa** — una casa **minore** che prende dal **maggiore** — è
  nel vocabolario e **provata sul IV maggiore** (secondo esempio lavorato).
  Restano nominate ma non provate la **terza di Piccardia** e il colore ♮6/♮7 del
  minore jazz;
- **le scale non diatoniche** che l'utente usa (ottatoniche, cromatiche): questo
  documento copre il prestito fra i modi diatonici paralleli, non quelle;
- **il ritmo armonico** — ogni quanto cambia l'accordo, e quanto dura il
  prestito prima di risolvere: qui è una scelta del caso, non una regola, come
  già in `armonia-modale.md`;
- ~~**la verifica su un pezzo DA ZERO**~~ — **superata il 12 settembre 2026**
  (vedi l'esempio lavorato): è la prima istruzione armonica a passare il «creare
  dal nulla», non solo l'armonizzare un'idea esistente.
