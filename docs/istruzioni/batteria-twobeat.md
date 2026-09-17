# Scrivere una parte di batteria — feel TWOBEAT (dixieland)

⚠️ **PERIMETRO.** Questa istruzione copre **un feel solo**: la batteria del
*2-feel* tradizionale — dixieland, swing antico. **Non è il giggidì** del bebop
([batteria-jazz.md](batteria-jazz.md)) e **non sono le spazzole** della ballad
([batteria-ballad.md](batteria-ballad.md)). Qui comanda l'**oom-pah**: cassa e
basso sul 1 e 3, il charleston croccante sul 2 e 4.

---

⚠️ **Questo documento è quasi tutto `[LIB]` e `[DEC]`, come la ballad.** Il
**Groove MIDI non ha un feel «twobeat»** (verificato: l'etichetta non c'è) e la
Weimar dà il solista, non la batteria. Quindi **niente groove template né scala
di velocity misurata**. La parte poggia su Riley e su decisioni dichiarate.

**Cosa ti serve prima di cominciare:**

- la forma, e dove sono i giunti (fine frase, cambio di sezione);
- **il basso** — nel twobeat batteria e basso fanno insieme l'*oom* sul 1 e 3.
  Vedi [basso-twobeat.md](basso-twobeat.md);
- il tempo: veloce, **~160-200 BPM**.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura didattica, con fonte |
| `[MIS]` | misurato su un corpus (**qui non ce n'è per la batteria**) |
| `[DEC]` | decisione presa qui, con la ragione |

---

## L'oom-pah, il cuore

`[LIB]` Riley p. 57, «Playing in "2"» (citato in `docs/repertori/jazz.md`,
casella 1): nel 2-feel il batterista *«suona un groove più rilassato, il che si
può fare suonando meno figure basate sulla semiminima sul piatto ride [...].
Tieni il charleston croccante.»* Da qui le due voci portanti:

- il basso e la **cassa** stanno sul **1 e sul 3** — l'*oom*;
- il **charleston chiuso a mano** sta sul **2 e sul 4** — il *pah*, e va tenuto
  **croccante** (Riley), non molle come nella ballad.

```
cassa (oom):    x.......x.......   1 e 3, con la fond. del basso
charleston (pah): ....x.......x...   2 e 4, croccante
```

⚠️ **È questa alternanza 1-3 / 2-4 il feel.** Contro il walking (tutto sul ride
in crome) e contro la ballad (strofinìo continuo, molle): qui c'è uno **spazio
netto** fra l'oom e il pah, e lo scatto lo tiene vivo.

---

## Il vocabolario

### La cassa — 1 e 3, leggera ma presente

```
x.......x.......    1 e 3
```

`[DEC]` Più ferma della cassa "feathered" della ballad (che è quasi inudibile),
più leggera del funk (che sincopa): qui segna l'*oom* insieme al basso. Velocity
media (~65-75).

### Il charleston chiuso — 2 e 4, croccante

```
....x.......x...    2 e 4
```

`[LIB]` Riley: *«tieni il charleston croccante»*. È il *pah* e il backbeat del
dixieland: netto, corto, un po' più forte della cassa. È lui a tenere vivo un
feel che, di suo, è "meno attivo".

### Il rullante — il *press roll*, il tappeto (e il suo limite)

`[DEC]` La firma della batteria dixieland è il **press roll**: un rullo di
spazzola/bacchetta premuta che cresce e si risolve **sul 2 e sul 4**, spesso
"tirato" attraverso il backbeat. Non è rappresentabile a colpi discreti: si
**approssima** con crome molli e fitte a velocity bassa (28-40), con un tocco
appena più forte che *arriva* sul 2 e sul 4 (la risoluzione del rullo). ⚠️ **Non
è la stessa cosa** — il press roll vero è un buzz sostenuto, e resta in «Cosa
manca», come lo strofinìo della ballad.

### Il ride / i piatti — MAI lo spang-a-lang

⚠️ `[LIB]` Riley: nel 2-feel si suonano **meno figure di semiminima sul ride** —
cioè il giggidì **non c'è**. Il ride/piatto resta per **accenti**: uno *splash*
o una *choke* sul 1 a inizio frase, una crash al giunto di sezione. Mai il
pattern continuo. ⚠️ È lo **stesso riflesso** in cui si è ricascati con la
ballad (lo spang-a-lang messo per abitudine): il tempo lo tengono cassa,
charleston e press roll, non il ride.

---

## Lo swing — solido, non dritto e non terzina

`[MIS]` `docs/repertori/jazz.md`, casella 4, «Per tempo»: alla fascia del
twobeat (**180-240 BPM**, dove cade la mediana 184) il levare del jazz sta al
**63,7%** (BUR 1,75). Cioè uno swing **pieno**, non la terzina lenta della ballad
(66%) né il dritto. `S.set_swing(doc, 62)` mette il levare a ~62% e dà il lilt
alle **crome** — il press roll e i rilanci del basso. ⚠️ Le note su 1 e 3 (cassa,
charleston, oom del basso) sono **semiminime**: non sentono lo swing, e va bene
così — il *due* è fatto di movimenti forti, non di crome swingate.

⚠️ **A tempo più alto lo swing cala** (jazz.md casella 4: sopra i 240 le crome
sono quasi dritte). Se il twobeat va molto veloce, si abbassa `set_swing` verso
il dritto.

---

## I vincoli

| vincolo | perché |
|---|---|
| **niente spang-a-lang sul ride** | `[LIB]` Riley: nel 2-feel meno figure di semiminima sul ride. Il tempo lo tengono cassa+charleston+press roll |
| **il charleston sul 2 e 4 resta croccante** | `[LIB]` Riley lo dice esplicito: è ciò che tiene vivo un feel "meno attivo". Molle = ballad |
| **l'oom sta sul 1 e 3, il pah sul 2 e 4** | è l'alternanza che *è* il feel; riempirla di colpi la annulla |
| **lascia lo spazio fra oom e pah** | il *due* vive di quel vuoto netto; il funk lo riempirebbe di ghost, ma qui no |
| **nessuna regola su tutte le battute** | la trappola del generatore, come per ogni feel: varia il press roll, gli accenti, i giunti |

---

## Come si decide UNA battuta

La domanda di sempre, con l'ancora dell'oom-pah:

**«Dove sono l'oom (1 e 3) e il pah (2 e 4), e cosa serve intorno?»**

1. **Fissa l'oom-pah.** Cassa sul 1 e 3 con il basso, charleston croccante sul
   2 e 4. È l'ossatura.
2. **Stendi il press roll** come tappeto molle, con la risoluzione sul 2 e 4 —
   ma non identico ogni battuta.
3. **Guarda i giunti.** Fine di frase, cambio di sezione, arrivo su una
   dominante: lì entra un accento di piatto, uno *splash*, un mezzo fill
   (vedi [fill.md](fill.md)), o la battuta "in 4" del basso.
4. **Lascia respirare.** Una battuta in cui il press roll quasi tace, con solo
   oom-pah, è giusta.

---

## L'esempio lavorato

`tools/twobeat_scritto.py`: la sezione ritmica del twobeat — basso in 2
saltellante, oom-pah (cassa 1-3 / charleston 2-4), press roll sul rullante,
piatto solo ai giunti; comping "stride" sul 2 e 4. ⚠️ **Verdetto dell'ascolto
(17 settembre 2026):** *«ok funziona»*.

---

## Cosa manca a questo documento

- **il press roll vero**: un buzz sostenuto, che nessun campione a colpi rende —
  qui è approssimato con crome molli. È lo stesso limite dello strofinìo della
  ballad;
- **il `[MIS]`**: nessun corpus di batteria twobeat. Groove MIDI non ce l'ha;
- **il woodblock / temple block** (il "clop" clip-clop trad) e le **spazzole**:
  scelte di suono/kit, non di note;
- **il fill dixieland** e le rullate di rullante nello specifico:
  [fill.md](fill.md) è tarato sullo swing col ride.
