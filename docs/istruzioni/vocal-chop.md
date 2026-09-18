# Il VOCAL CHOP — affettare una voce e suonarla a ritmo

⚠️ **PERIMETRO.** Il vocal chop è un campione vocale **tagliato in fette** (una per
riga di un kit) e **innescato a ritmo**: il «yeah» stutterato di house/garage, il
frammento vocale del trip-hop. È **audio**, non note — riempie la casella 8 di
house/trip-hop, che era rimasta aperta perché è materiale di campioni. ⚠️ Lo
**stesso meccanismo** (affettare un campione in un kit) sblocca il **break tagliato**
di jungle/DnB.

> **La cosa da capire:** non si compone una melodia, si **ricompone un suono a
> pezzi**. Prendi una voce, la tagli, e riordini/ripeti le fette a tempo. Il
> materiale è il campione; la musica è il ritmo del taglio.

---

⚠️ **NIENTE CORPUS** (è una tecnica, non un repertorio): `[LIB]`+`[DEC]`. La
**struttura della fetta** è `[OSS]` (lo Slicer nativo del Deluge e i file veri:
`FINDINGS.md` §«Campioni e tick»).

**Cosa ti serve prima di cominciare:**

- un **campione** vocale sulla SD (`SAMPLES/...`) e la sua lunghezza in **frame**
  (`audio.wav_frames(path_locale)[0]`, col wav a portata — SD nel lettore, o `dsysex
  get`);
- **quante fette** (default 16, come lo Slicer; per una parola sola anche 8);
- il contesto (un beat house, un groove trip-hop).

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | convenzione documentata |
| `[OSS]` | struttura osservata (lo Slicer / i file veri) |
| `[DEC]` | decisione presa qui (il taglio, il pattern) |

---

## 1. Come si taglia — `kit.affetta`

Sul Deluge il vocal chop è un **kit di fette**: più drum row che puntano allo
**stesso** file, ognuna con una `<zone>` (start/end in **frame**) diversa. Lo
**Slicer nativo** lo fa da sé (in CLIPS: tieni premuto Select → SLICE → N fette); la
libreria lo fa con:

```python
frames = audio.wav_frames('E:/SAMPLES/RECORD/REC00027.WAV')[0]   # la lunghezza vera
fette = kit.affetta(doc, iChop, 'SAMPLES/RECORD/REC00027.WAV', frames, n=8)
# -> ['fetta 1', ..., 'fetta 8'], zone a [i*frames//n, (i+1)*frames//n]
```

⚠️ **Fette uguali** (N chunk): semplice e deterministico, come lo Slicer. Il taglio
sui **transienti** (sulle sillabe) è più musicale ma vuole analisi audio — futuro.

## 2. Il MODE — ONCE

`[OSS]` Ogni fetta deve **suonare intera** quando la innes­chi, a prescindere dalla
durata della nota: è il MODE **ONCE** (`loopMode`). `kit.affetta` NON lo scrive a
mano: costruisce le fette **copiando un drum one-shot vero** (il BD A di `808 From
Mars`, `loopMode=1`), così il valore è **ereditato da un drum che funziona**. ⚠️ Se
all'ascolto una fetta si tronca invece di suonare intera, è lì che si interviene
(verifica sul dispositivo).

## 3. Come si compone il chop

`[DEC]` La musica è il **ritmo del taglio**. Le mosse:

- **ricostruisci** la parola: le fette in ordine (1-2-3-…) sui sedicesimi/crome — si
  risente l'«mmyeah»;
- **stuttera**: ripeti una fetta (`1 1 1`), il glitch ritmico;
- **ri-ordina**: salta fra le fette (`1 · 8 · 4 · 8`), il chop che non è più la parola
  ma un pattern;
- **innesca a tempo**: sui movimenti, sui levare, in sincope — è una parte ritmica.

Si scrive come una batteria: `MU.scrivi(doc, clip, note, dove='fetta 3')`.

## 4. Il legame col break (jungle/DnB)

`kit.affetta` è **lo stesso gesto** su un **break** di batteria: tagli un amen/funky
drummer in fette e le riordini. Il vocal chop e il break-chop sono la stessa tecnica
su materiale diverso. (Il break vero è un altro pezzo/genere; qui c'è il meccanismo.)

---

## I vincoli

| vincolo | perché |
|---|---|
| **la fetta suona intera (ONCE)** | ereditato da un drum one-shot; senza, la fetta si tronca |
| **il campione è sulla SD** | il `fileName` è relativo (`SAMPLES/...`); se il file non c'è, silenzio |
| **il chop è ritmo, non melodia** | si riordinano/ripetono le fette a tempo, non si suonano altezze |
| **le fette uguali sono un punto di partenza** | se cadono male sulle sillabe, cambia N o (in futuro) taglia sui transienti |
| **niente riflesso** | il pattern del chop si compone PER il pezzo, all'orecchio |

---

## L'esempio lavorato

`tools/vocalchop_scritto.py`: l'«mmyeah» (`SAMPLES/RECORD/REC00027.WAV`, 142725 frame)
in **8 fette**, innescate su un beat **house** four-on-the-floor (808) + basso in
levare. Il chop ricostruisce la parola in crome, poi stuttera. `verifica()` vuota.
⚠️ **Verdetto dell'ascolto: da dare** (audio = ascolto pieno; il pattern e N sono
`[DEC]`, da rifinire).

---

## Cosa manca a questo documento

- il **taglio sui transienti** (onset): scelto «fette uguali»; l'onset è futuro
  (serve analisi audio, stdlib senza numpy);
- il **pitch/stretch** delle fette e gli **effetti** sul vocal: sound design;
- il **break** vero (jungle/DnB): il meccanismo c'è (`kit.affetta`), il genere no.
