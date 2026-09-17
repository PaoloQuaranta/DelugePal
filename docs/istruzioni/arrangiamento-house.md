# Arrangiare un pezzo HOUSE / TECHNO — build/drop, filtro, sidechain

⚠️ **PERIMETRO.** Questa istruzione copre **l'essenza** della four-on-the-floor:
non la singola battuta (quella sta in [batteria-house.md](batteria-house.md) e
[basso-house.md](basso-house.md)), ma **l'arco** — come un pezzo dance *progredisce*.
House e techno **sono forma**: una battuta non dice niente di un pezzo, è il
**build/drop** e il **filtro in movimento** a farlo vivere.

> **La cosa da capire:** in un pezzo dance non si aggiungono note per far
> succedere qualcosa. Si **tolgono e si rimettono le parti**, si **apre il
> filtro**, si accende il **pompaggio**. Il movimento è nell'arrangiamento e nel
> suono, non nei colpi.

---

⚠️ **NIENTE CORPUS, come per tutto house/techno** (generi programmati): questo
documento è **`[LIB]`+`[DEC]`**, la convenzione di produzione elettronica. La
**struttura XML del sidechain** è invece `[OSS]` (verificata sui file veri del
Deluge, schema c1.3.0); la **magnitudine** del ducking (`0xDE000000`) è stata
tarata e **confermata all'orecchio** (*«va bene»*, 17 settembre 2026).

**Cosa ti serve prima di cominciare:**

- il groove già scritto (cassa, hat, clap, basso, stab) — vedi le due istruzioni
  sorelle;
- un kit **elettronico** (808/909) — il suo kick sarà il **trigger** del sidechain;
- l'idea dell'arco: quante battute, quante sezioni.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | convenzione di genere documentata |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | struttura XML osservata sui file veri del Deluge |
| `[da verificare]` | valore che si chiude solo all'orecchio, sul dispositivo |

---

## 1. L'arco — build/drop

`[LIB]`+`[DEC]` Un pezzo dance è un **arco di tensione**: si parte scarni, si
accumula, si esplode (il **drop**), si toglie tutto (il **breakdown**), si
riesplode. Le parti **entrano ed escono**; il filtro **apre e chiude**. Le durate
tipiche sono potenze di due: **8-16-32-64** battute.

L'arco minimo, quello dell'esempio (32 battute):

| sezione | battute | cosa suona | suono |
|---|---|---|---|
| **intro** | 8 | solo **cassa + closed hat** | filtro un po' chiuso |
| **build** | 4 | entrano **basso e stab** | il **cutoff apre** (rampa) |
| **drop** | 8 | **tutto** (clap, open hat, basso, stab) | **sidechain** che pompa |
| **breakdown** | 4 | **via la cassa**, restano stab + basso | stab **filtrato** scuro |
| **drop** | 8 | rientro pieno | filtro aperto, il pompaggio torna |

⚠️ **Il breakdown toglie la cassa**, ed è l'unico posto dove la four-on-the-floor
**si buca** (la regola dice «la cassa non si buca»: qui è l'eccezione che *fa* il
breakdown). Togliere il motore crea il vuoto da cui il drop successivo rientra.

**Come si stende, materialmente.** Si usa `MU.forma`: una clip per stato (una
batteria d'intro, una piena; uno stab normale, uno che apre, uno filtrato), e la
mappa delle sezioni nel tempo. `forma` fa i conti e piazza le clip sull'arranger;
la **stessa** clip riusata in due sezioni uguali (i due drop) diventa una clip
instanziata due volte. Una clip corta (4 battute) piazzata su una sezione lunga
(8) **si ripete in loop** — è l'arranger a farlo (`arranger.place` con `length`
multiplo).

## 2. Il filtro che apre

`[LIB]`+`[DEC]` Lo **sweep del cutoff** è metà del carattere del genere: nel
build il filtro si apre gradualmente (il pezzo «si accende»), e nel drop è
spalancato. Si scrive con:

```python
MU.apri_filtro(doc, clip_build, 8, 45, 0, LUNG, passi=9)  # cutoff 8 -> 45 sul build
```

`apri_filtro` prende il cutoff in **unità display (0-50)** e stende una rampa
sull'`lpfFrequency` della clip. ⚠️ **Vive nella clip**, quindi si applica **solo
dove quella clip suona**: è così che il build ha lo sweep e il drop no. Per uno
stab **fisso e scuro** (il breakdown) basta invece un valore fermo:
`sound.set(clip, 'lpfFrequency', 16)`.

*(La techno acid — il filtro che rotola di continuo con un LFO sul cutoff, la nota
sola — è la stessa famiglia, ma continua e non «di build»: `sound.set_patch_cable(node, 'lfo1', 'lpfFrequency', …)`. Non è coperta qui.)*

## 3. Il sidechain — il pompaggio

⚠️ **Il Deluge ha un SIDECHAIN interno, ed è cosa diversa dal COMPRESSORE.** È la
trappola: nell'XML esistono due elementi separati, `<audioCompressor>` (il
compressore vero: threshold, ratio, blend) e `<sidechain>` (l'inviluppo di
ducking). **Per pompare si usa il sidechain, mai il compressore.**

Il sidechain è un **inviluppo attack/release innescato dalle note di un kit**. La
pompa house si fa in tre pezzi, tutti in una chiamata:

```python
MU.sidechain(doc, iBass, quanto='0xDE000000', sync=7, manda_da=(iKit, KICK))
MU.sidechain(doc, iStab, quanto='0xDE000000', sync=7, manda_da=(iKit, KICK))
```

1. **il trigger** — `manda_da=(kit, nome_kick)` mette `sideChainSend` al massimo
   sul kick: è lui a innescare la pompa (i kit 808/909 di serie hanno il kick già
   a metà send);
2. **il ducking** — sul bersaglio (basso, stab) scrive `sidechainCompressorVolume`
   nei `<params>` di **ogni sua clip** — è la clip che suona — così il volume
   respira sotto la cassa;
3. **il tempo** — `syncLevel`/`syncType` nell'elemento `<sidechain>` dello
   strumento.

⚠️ **Si imposta UNA volta, a livello di suono, non per-sezione.** Pompa **da sé
dove batte la cassa**: nei drop sì; nel breakdown no, perché manca la cassa che lo
innesca; nell'intro è muto perché basso e stab non ci sono ancora.
**L'arrangiamento accende e spegne la pompa senza automazione.**

⚠️ **`quanto` si tara all'orecchio.** La struttura è presa dai file veri, ma la
*forza* e il *verso* del duck si giudicano **suonando** (`sidechainCompressorVolume`
non sta nella tabella dei parametri, quindi non ha una scala di display pulita).
Valori visti in file veri: `0xF2000000`, `0xDE000000`, `0xFC000000`. Per la house
dell'esempio **`0xDE000000` è confermato all'orecchio** (*«va bene»*, 17 settembre
2026); per un kit o un pezzo diverso, ri-giudicare da uno di questi.

---

## I vincoli

| vincolo | perché |
|---|---|
| **il drop non aggiunge note, rimette parti** | il movimento dance è togliere/rimettere + il filtro, non colpi in più |
| **la cassa si buca SOLO nel breakdown** | è l'eccezione che crea il vuoto; altrove è il motore |
| **il filtro apre nel build, è aperto nel drop** | lo sweep è metà del genere |
| **il sidechain col SIDECHAIN, non col compressore** | sono due elementi XML diversi; il compressore non pompa |
| **il pompaggio è mix, non nota** | si imposta una volta sul suono; l'arrangiamento lo accende togliendo/mettendo la cassa |
| **le sezioni in potenze di due** | 8-16-32-64: la griglia percettiva del dance |

---

## Come si decide UNA sezione

**«Cosa c'è dentro, e cosa sta succedendo al filtro e alla pompa?»**

1. **Le parti**: quali clip suonano (la cassa c'è? il basso? lo stab?).
2. **Il filtro**: è fermo, apre (build), o è chiuso (breakdown)?
3. **La pompa**: c'è la cassa? allora il sidechain pompa da sé. Non c'è? respira.
4. **Il giunto con la sezione dopo**: un breakdown chiama un drop; un build chiama
   il drop. L'arco è fatto di attese e rilasci.

---

## L'esempio lavorato

`tools/house2_scritto.py`: l'arco a 32 battute descritto sopra, sul giro
`Am9 | Dm9 | Fmaj9 | Em9`, kit 808, `Square Saw Bass` scurito, `Pianism I` per lo
stab. Il filtro apre nel build, lo stab del breakdown è filtrato scuro, il
sidechain pompa nei drop. `verifica()` vuota, nessuna avvertenza.
⚠️ **Verdetto dell'ascolto (17 settembre 2026): *«va bene»*.**

---

## Cosa manca a questo documento

- il **`[MIS]`**: non esiste (generi programmati), e non è una lacuna da colmare;
- la **techno acid** (LFO sul cutoff, continuo): nominata, non implementata;
- il **lead/topline** e il **vocal chop** (casella 8 della scheda): materiale di
  `audio.py`, fuori da qui.
