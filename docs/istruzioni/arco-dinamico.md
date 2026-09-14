# L'arco dinamico: come il pezzo sale e ricade

**A cosa serve.** Hai la [forma](struttura.md) — le sezioni disposte nel tempo —
ma una forma che ripete ogni sezione **uguale** è piatta. L'arco dinamico è la
**carne sullo scheletro**: come intensità e densità **salgono** verso un culmine e
**ricadono**. È ciò che fa sentire un pezzo come un discorso e non come un ciclo.

È priorità 2 (forma), la **seconda faccia della struttura** dopo la
[mappa](struttura.md). La mappa dice *dove* cadono le sezioni; l'arco dice *con
quanta intensità* ciascuna suona.

**Cosa ti serve prima di cominciare:** la forma (la mappa e le sezioni), e sapere
**dov'è il culmine** — nell'AABA è il ponte.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[MIS]` | misurato su un corpus, con quanti pezzi |
| `[CALC]` | calcolo sul meccanismo, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

⚠️ **`[CALC]` + un ascolto**, come le altre facce della forma. Il `[CALC]` è
l'aritmetica (la scala delle velocity, il ritmo armonico); l'ascolto è se **l'arco
si sente** — se il culmine arriva e il ritorno a casa si posa.

---

## Il principio: l'arco è misurato

`[MIS]` casella 9 di [`docs/repertori/jazz.md`](../repertori/jazz.md) (57 assoli
AABA, 36 solisti, 6777 battute): l'AABA **non è un ciclo che si ripete quattro
volte**. Le quattro sezioni hanno densità diverse, e c'è un arco **narrativo**:

| sezione | corse (culmini) | come suona |
|---|---|---|
| **A1** | 18,8% | si parte **radi** |
| **A2** | 24,8% | si cresce |
| **B**, il ponte | **26,3%** | il **culmine** |
| **A3** | 20,9% | si **ricade** a casa |

⚠️ **Il ponte è la sola sezione che non respira alla fine** (`[MIS]` casella 9):
alle chiusure di sezione le battute vuote sono A1 15,6%, A2 10,5%, **ponte 6,2%**,
finale 7,7%. A1 e A2 **respirano**; il ponte **tira dritto** — è il culmine, non si
ferma. Il finale respira di nuovo: è arrivato.

---

## Le leve: tre modi di salire, e devono salire **insieme**

L'intensità non è una cosa sola. `[DEC]` Tre leve, e il culmine si sente quando
salgono **tutte e tre** verso il ponte:

### 1. La densità (quante note)

`[MIS]` la mediana di note per sezione va da 5 (A) a 6 (ponte): il ponte è **più
fitto**. Radi sull'A d'apertura, corse sul ponte, di nuovo radi sul ritorno. È la
leva che la casella 9 misura direttamente.

### 2. Il ritmo armonico (ogni quanto cambia l'accordo)

`[LIB]` Il [ritmo armonico](ritmo-armonico.md) è una leva dell'arco: **accelerare
il cambio d'accordo spinge**. Nell'arco lungo, il ponte può **raddoppiare** il
ritmo armonico — due accordi a battuta dove l'A ne aveva uno — e quel raddoppio *è*
il culmine. È dove vive, nella forma lunga, la mossa che `ritmo-armonico.md`
chiamava «accelerare verso la cadenza».

### 3. La dinamica (quanto forte)

`[CALC]` La velocity: piano sull'apertura, forte sul culmine, mezzo sul ritorno.
La primitiva è `MU.dinamica`.

⚠️ **E il respiro** (`[MIS]`): i vuoti a fine sezione. A1 e A2 respirano (una
battuta vuota, una nota tenuta); il ponte no — tira dritto verso il culmine.

---

## Come si scrive, materialmente

Ogni sezione è una **clip distinta** (l'arco vuole che l'A d'apertura e l'A di
ritorno siano *diversi*: stessa idea, intensità diversa). Le tre leve:

```python
from delugexml import musica as MU

# la densita': quante note scrivi (rada l'A, fitto il ponte)
a1 = MU.melodia('mi4 sol4 mi4 do4', durata='1/1')          # 4 note, rada
b  = MU.melodia('sol4 la4 si4 do5 re5 do5 si4 la4 '        # 16 note, fitta
                'sol4 la4 si4 do5 si4 la4 sol4 mi4', durata='1/4')

# il ritmo armonico: durata piu' corta = piu' accordi = piu' spinta
a1_ch = MU.armonia('Cmaj7 | Am7 | Dm7 | G7', durata='1/1')                 # 1/batt
b_ch  = MU.armonia('Fmaj7 | Bb7 | Em7 | A7 | Dm7 | G7 | Cmaj7 | G7',
                   durata='1/2')                                           # 2/batt

# la dinamica: MU.dinamica scala le velocity a un livello
a1 = MU.dinamica(a1, 0.65)    # piano
b  = MU.dinamica(b,  1.2)     # forte
```

`MU.dinamica(note, fattore, *, minimo=1)` `[CALC]`: scala la velocity di ogni nota
per `fattore`, stretta fra `minimo` e 127, **senza mutare** l'originale (così la
stessa frase si posa a livelli diversi). Blindata da `test_dinamica`.

⚠️ **Per l'ultimo giro variato** (l'A che torna diverso, un fill, un tag finale)
c'è `arranger.place_unique`, la clip **"bianca"** — una copia indipendente da
modificare senza toccare le altre ripetizioni.

---

## Esempio lavorato: un AABA con l'arco (e il ritmo armonico)

`[OSS]` **Ascoltato il 14 settembre 2026**, caricato sul Deluge (`STRUTTURA02`).
Lo stesso AABA della [mappa](struttura.md), ora con l'arco steso sopra. In
[`tools/arco_scritto.py`](../../tools/arco_scritto.py):

| sezione | densità (note) | ritmo armonico | dinamica |
|---|---|---|---|
| **A1** | rada (4) | lento (1/batt) | piano (0.65) |
| **A2** | media (8) | lento (1/batt) | mezzo (0.85) |
| **B** ponte | **fitta (16)** | **veloce (2/batt)** | **forte (1.2)** |
| **A3** | rada (4) | lento (1/batt) | mezzo (0.75) |

⚠️ **Il ponte fa due cose in una:** è il culmine dell'arco **e** raddoppia il ritmo
armonico. Così questo pezzo prova, nello stesso ascolto, l'**arco dinamico** e il
**ritmo armonico** (che era chiuso col solo `[CALC]` e non era mai stato
ascoltato). Si suona dall'arranger.

**Verdetto: «suona giusto, approvato».** ⚠️ L'intensità **sale** al ponte e
**ricade** sull'ultimo A, e il ponte «tira» — anche perché gli accordi lì cambiano
il doppio più spesso. Con lo stesso ascolto è confermato il
[ritmo armonico](ritmo-armonico.md) che accelera sul culmine. Passa al primo colpo,
come le altre facce della forma.

---

## Cosa NON fare

- **non ripetere ogni sezione uguale:** una forma senza arco è un ciclo, non un
  discorso (casella 9: le quattro sezioni hanno densità diverse);
- **non far salire una leva sola:** il culmine si sente quando densità, ritmo
  armonico e dinamica salgono **insieme** — una sola non basta;
- **non far respirare il ponte alla fine:** è il culmine, tira dritto (`[MIS]`
  casella 9: il ponte è la sola sezione che non respira);
- **non sparare tutto forte dall'inizio:** senza un'apertura rada e piano non c'è
  culmine — solo un pezzo che stanca;
- **non confondere l'arco con la mappa:** la [mappa](struttura.md) dice *dove*
  cadono le sezioni, l'arco *con quanta intensità*.

---

## Cosa manca a questa istruzione

- l'arco su **più giri** (testa-soli-testa): l'intensità che cresce di chorus in
  chorus, non solo dentro un AABA;
- i **turnaround** e i pickup come segnali di transizione fra le sezioni:
  **[fatti](transizioni.md)** (la terza faccia della struttura). Resta il **fill di
  batteria**, che vuole una traccia di batteria nel pezzo;
- la **variazione automatica** dell'ultimo giro con `place_unique`: qui l'ultimo A
  è già una clip a sé, ma non c'è (ancora) una primitiva che «alza l'ultimo giro»;
- l'arco su generi **non-jazz** (l'EDM sale al drop, il pop al ritornello finale):
  la forma della salita cambia col genere — su domanda.
