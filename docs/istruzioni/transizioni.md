# Le transizioni: cucire i giunti fra le sezioni

**A cosa serve.** Hai la [forma](struttura.md) e il suo [arco](arco-dinamico.md),
ma il punto in cui una sezione **finisce** e la successiva **comincia** è dove
l'ascoltatore sente di più — o non sente niente, se il giunto è secco. Le
transizioni sono ciò che **cuce** i giunti: un turnaround che riporta, un pickup
che consegna il ponte, un tag che chiude.

È priorità 2 (forma), la **terza faccia della struttura** dopo la
[mappa](struttura.md) (dove cadono le sezioni) e l'[arco](arco-dinamico.md) (con
quanta intensità). La transizione è il **giunto** fra le sezioni.

**Cosa ti serve prima di cominciare:** la forma già stesa (le sezioni sulla
timeline), e sapere **quali giunti** vuoi articolare.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sul meccanismo, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

⚠️ **`[CALC]` + un ascolto**, come le altre facce della forma. Il `[CALC]` è il
meccanismo della clip **bianca** (`MU.variazione`); l'ascolto è se il giunto
**cuce** — se il ponte «arriva» preparato e il ritorno chiude.

---

## Il principio: tre modi di passare

`[LIB]` music-composition, `references/form/narrative-and-transitions.md`: la
transizione fra due sezioni è dove il contorno dell'energia si sente di più. Tre
modi:

| modo | cos'è | quando |
|---|---|---|
| **brusco** | la sezione nuova parte di colpo, massimo contrasto | per sorpresa, o un lancio energico; ⚠️ suona sconnesso se non «guadagnato» |
| **rampa / build** | l'energia sale nell'ultima battuta e la sezione nuova è il **rilascio** | per far «arrivare» un culmine (il ponte, il ritornello) |
| **morbido** | le due sezioni si sovrappongono o condividono un perno (una nota, un accordo) | per continuità e flusso |

⚠️ **La cadenza è la punteggiatura del giunto** (`[LIB]` stesso file): una **mezza
cadenza** o una **ingannevole** a un giunto interno dice «continua», e tiene la
cadenza piena (la risoluzione) **per la fine**. Un pezzo che chiude ogni sezione con
la stessa cadenza piena è sovra-articolato; uno che le tiene aperte all'interno
tira in avanti.

---

## Il vocabolario armonico-melodico del giunto

I dispositivi che cuciono un giunto senza batteria (la faccia scelta qui):

- **il turnaround** — un giro (I–vi–ii–V, o cromatico) in coda a una sezione che
  **riporta** al giro dopo: è già in [armonia-funzionale.md](armonia-funzionale.md)
  e [accordi-di-passaggio.md](accordi-di-passaggio.md). ⚠️ **Il turnaround è anche
  l'accelerazione del [ritmo armonico](ritmo-armonico.md) verso la cadenza:** la
  stessa mossa, vista dal giunto — l'accordo cambia più spesso proprio dove vuole
  risolvere;
- **il pickup** — una figura melodica (spesso una **salita**) nell'ultima battuta,
  che «consegna» la sezione nuova cadendo sul suo primo movimento. È la **rampa**
  in miniatura;
- **il break / lo stacco** — un mezzo movimento di silenzio (il «respiro prima del
  salto») che rende l'arrivo più netto;
- **il perno** — una nota o un accordo tenuto che appartiene a tutt'e due le
  sezioni: la transizione **morbida**.

---

## Il meccanismo: la clip "bianca"

`[CALC]` Una transizione tocca **un** giunto — l'ultima battuta di **una**
ripetizione — e non deve toccare le altre. Il modo del dispositivo è la clip
**bianca** (arranger-only): una copia indipendente che vive solo sulla timeline.

```python
from delugexml import musica as MU

# una copia bianca della clip di sezione, piazzata al giunto (tick):
coda = MU.variazione(doc, clip_sezione, pos=12 * MU.TICK_PER_BATTUTA)
# la si riempie come una clip qualunque -- il turnaround, il pickup:
MU.togli(doc, coda)                 # svuota la copia
MU.scrivi(doc, coda, materiale_del_giunto)
```

`MU.variazione(doc, sorgente, pos, *, length=None)` `[CALC]`: fa una copia
**bianca** di `sorgente` (arranger-only, niente `section`), la piazza a `pos`, e la
ritorna — lo strumento lo trova da sé. Modificarla **non tocca** l'originale né le
altre ripetizioni. Blindata da `test_variazione`. Sotto c'è
`arranger.place_unique`.

⚠️ **Varia solo la voce che cambia.** Se il pickup è nella melodia, la clip bianca
è quella della melodia; gli accordi restano la clip di sezione piana. Non serve
copiare tutto.

---

## Esempio lavorato: due giunti sull'AABA

`[OSS]` **Ascoltato il 14 settembre 2026**, caricato sul Deluge (`STRUTTURA03`).
Lo stesso AABA, con due giunti articolati dalla clip bianca. In
[`tools/transizioni_scritto.py`](../../tools/transizioni_scritto.py):

| giunto | modo | cosa fa |
|---|---|---|
| **A2 → B** | rampa / build | il **pickup**: la melodia sale (sol la si do5) nell'ultima battuta e consegna il ponte |
| **il ritorno (A3)** | morbido | il **turnaround**: l'ultimo A stringe il ritmo armonico (Dm7 G7 in una battuta) e **risolve** su Cmaj7 — la cadenza che chiude |

⚠️ Solo la melodia di A2 e l'ultimo A sono clip bianche; A1, B e gli accordi di A2
restano le sezioni piane. **Verdetto: «suona giusto, approvato».** Il ponte
«arriva» preparato dal pickup, e il ritorno **chiude** invece di ripartire: i
giunti cuciono. Passa al primo colpo, come le altre facce della forma.

---

## Cosa NON fare

- **non lasciare i giunti secchi:** senza una transizione le sezioni si giustappongono
  invece di cucirsi (a meno che il brusco sia voluto);
- **non copiare tutta la sezione per variare una voce:** la clip bianca è solo per
  la voce che cambia;
- **non chiudere ogni giunto con la cadenza piena:** tienila per la fine, apri gli
  interni con mezza o ingannevole (`[LIB]`);
- **non toccare l'originale:** la variazione è una copia bianca **apposta** — se
  modifichi la clip di sezione, cambi tutte le ripetizioni;
- **non confondere la transizione con l'arco:** l'[arco](arco-dinamico.md) è
  l'intensità *dentro* le sezioni, la transizione è il *giunto* fra loro.

---

## Cosa manca a questa istruzione

- ~~il **fill di batteria**~~ **[fatto](fill.md)** (la faccia ritmica del giunto):
  ride giù, tom su, ~1,2×, non più forte (`[MIS]` casella 9), posato al giunto con
  la stessa clip bianca. Resta l'ascolto pieno (vuole una batteria coi tom nel pezzo);
- i **tre modi a confronto** sullo stesso giunto (brusco / rampa / morbido), come
  il voicing e il comping mettevano a confronto le loro scelte;
- la transizione **morbida** vera (sovrapposizione, cross-fade): qui c'è il perno
  come idea, non ancora un esempio;
- una primitiva che **alza l'ultimo giro** in automatico (final-chorus elevation):
  oggi la variazione si scrive a mano, giunto per giunto.
