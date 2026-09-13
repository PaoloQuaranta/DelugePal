# Il comping: il ritmo della mano che accompagna

**A cosa serve.** Hai gli accordi (l'armonia) e i voicing (quali note); il
**comping** è il **ritmo** con cui la mano che accompagna li suona — dove colpisce,
dove tace, come **risponde** al solista. È la faccia ritmica della forma: gli
stessi accordi possono martellare o respirare, e cambia tutto.

È priorità 2 (forma), la seconda faccia dopo il [voicing](voicing.md). Poggia su
`voicing.md` (quali note) e [`ritmo-armonico.md`](ritmo-armonico.md) (ogni quanto
cambia l'accordo); il comping aggiunge il **ritmo del colpo** e lo **spazio**.

**Cosa ti serve prima di cominciare:** la progressione (un accordo per battuta),
il voicing, e — se c'è — la melodia/il solista a cui rispondere.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sul meccanismo, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

⚠️ **`[CALC]` + un ascolto**, come il [voicing](voicing.md): il comping è ritmo, e
il ritmo ha parte d'orecchio. `[LIB]`/`[CALC]` per il vocabolario e le meccaniche,
un esempio lavorato **ascoltato** per il feel.

---

## Il principio: complementare il solista, non tappezzare

`[LIB]` Levine, *The Jazz Piano Book*, cap. 21 «Comping», p. 223: il comping è
quello che il pianista fa **dietro il solista** — lo *«stimola ritmicamente e
armonicamente»*, accentua i turnaround e i ponti, **rinforza la forma**. E la
regola che tiene insieme tutto: *«trova il punto medio fra **audacia e
ritegno**»*, alternando il comping aggressivo allo stare sullo sfondo.

⚠️ **Il comping è una conversazione, non tappezzeria.** Non riempie ogni
movimento: lascia spazio, e lo spazio è dove il solista respira.

---

## Il vocabolario

### Le tre collocazioni del colpo

`[LIB]` Levine, cap. 21 (fig. 21-2 e 21-6): un accordo si può colpire in tre modi
rispetto al movimento —

| collocazione | dove | effetto |
|---|---|---|
| **sul battere** | sul movimento | fermo, in chiaro |
| **anticipato** | mezzo movimento **prima** | la **spinta** — la sincope che definisce il comping jazz |
| **dietro** | mezzo movimento **dopo** | rilassato, laid-back |

⚠️ **L'anticipazione è la mossa più caratteristica.** `[CALC]` Nel meccanismo, un
colpo sull'**ultima croma** di una battuta cade appena prima del battere della
battuta dopo: è l'accordo che «arriva in anticipo» sul cambio. Verificato da
`test_comping`.

### Lo spazio, e la risposta al solista

`[LIB]` Levine, cap. 21, p. 228 e 231:

- **rado dove il solista è fitto, fitto dove respira** — il comping riempie i
  buchi della melodia invece di raddoppiarla (call-and-response);
- **non pestare nel registro del solista:** *«attenzione a non fare comping troppo
  nello stesso registro del solista»*. Se lui è acuto, tieniti basso.

`[DEC]` È la stessa lezione che la batteria ha imparato a caro prezzo (§6-tervicies
di `HANDOFF.md`): variare **aggiungendo dove c'è spazio**, non a tappeto.

### Il carattere

`[LIB]` Levine: un comping **«in due»** vuole colpi corti e staccati (tanto
spazio); uno **sostenuto** tiene gli accordi più a lungo. E l'audacia/ritegno si
**alternano**: un comping identico per tutto il pezzo è morto quanto una
progressione senza ritmo armonico.

---

## Come si scrive, materialmente

`[CALC]` La primitiva è `MU.comping`: una **stringa di ritmo per battuta**
(`'x..x....'`, 8 crome, `x`=colpo `.`=pausa) → gli accordi piazzati sui colpi,
voicizzati e **condotti** (`MU.armonia` sotto).

```python
from delugexml import song as S, musica as MU

S.set_scale(doc, 'C', 'maggiore')
# un ii-V-I rado, con l'anticipazione sul cambio (la x finale di ogni battuta):
rado = MU.comping('Dm7 | G7 | Cmaj7',
                  ['x..x...x', 'x..x...x', 'x..x....'],
                  voicing='senza-fondamentale', registro='do3')
```

⚠️ **Un accordo per battuta** (la primitiva è pensata così); il voicing e la
condotta sono quelli di `MU.armonia`. La `x` sull'ottava cella di ogni battuta
**anticipa** il battere della successiva.

---

## Esempio lavorato: lo stesso giro, due comping

`[OSS]` **Ascoltato il 13 settembre 2026**, caricato sul Deluge (`COMPING01`). Il
confronto: lo stesso `Dm7 | G7 | Cmaj7` comped in due modi — uno **rado e
anticipato** (con spazio), uno **fitto** — sullo stesso materiale, così la
differenza è solo il ritmo del comping. In
[`tools/comping_scritto.py`](../../tools/comping_scritto.py). Rhodes + basso,
niente melodia: lo **spazio** si sente meglio senza un solista che lo riempie.

**Verdetto: «suona bene, il rado ha spazio e spinta — approvato».** ⚠️ Conferma
all'orecchio le due mosse del principio: lo **spazio** (rado contro fitto) e la
**spinta** (l'anticipazione sull'ultima croma). Passato al primo colpo, come il
voicing — la forma è terreno fermo quanto l'armonia, purché la scelta resti una
scelta.

---

## Cosa NON fare

- **non riempire ogni movimento:** il comping è conversazione — lo spazio è dove
  il solista respira;
- **non pestare nel registro del solista** (Levine): se lui è acuto, tieniti basso;
- **non tenere lo stesso comping per tutto il pezzo:** audacia e ritegno si
  alternano;
- **non confondere comping e ritmo armonico:** il [ritmo armonico](ritmo-armonico.md)
  è ogni quanto **cambia** l'accordo; il comping è ogni quanto lo si **colpisce**.

---

## Cosa manca a questa istruzione

- il comping **latin/bossa** e il **two-bar clave** (Levine, cap. 21, li tocca):
  su domanda, quando servirà un pezzo latin;
- la **risposta misurata** a una melodia data (dove sono i buchi): qui è una
  scelta a mano, non ancora calcolata dalla melodia;
- il **contrappunto** e la **struttura** lunga: le altre facce della priorità 2.
