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

## 2. Il MODE — ONCE (come lo Slicer nativo)

`[OSS]` **Verificato copiando una fetta salvata dallo Slicer nativo del Deluge**
(`MMYEAH.XML`): l'osc1 della fetta ha REPEAT MODE **ONCE** (`loopMode=1`) più la
`<zone>` `[start,end]`. La chiave che avevo sbagliato all'inizio:

- **è la ZONA a delimitare la fetta, non il mode.** ONCE «plays once, always the
  whole way through» significa «tutta la ZONA CARICATA `[start,end]`», non l'intero
  file. Un one-shot suona tutto solo perché la sua zona *è* tutto il file;
- quindi con ONCE **ogni innesco suona la fetta intera** (`[start,end]`), che è
  esattamente ciò che serve al chop: un colpo = un frammento.

`kit.affetta(..., mode='once')` (default) fa così. ⚠️ Se una fetta suona come la
**parola intera**, il difetto NON è il mode: è il **pattern** (le fette in fila,
contigue, ricostruiscono la parola) — vedi §3.

## 3. Come si compone il chop

`[DEC]` La musica è il **ritmo del taglio**. Le mosse:

- ⚠️ **NON metterle in fila (1-2-3-…-8) contigue**: ricostruiscono la parola e si
  risente l'«mmyeah» intero, non un chop — è l'errore che è costato tre ascolti;
- **buchi**: lascia silenzio fra i frammenti (non un colpo per sedicesimo) — è il
  silenzio a rendere «staccati» i pezzi;
- **stuttera**: ripeti una fetta (`8 8 8`), il glitch ritmico;
- **ri-ordina**: salta fra fette non contigue (`8 · 5 · 1 · 6`), il pattern che non è
  più la parola;
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
| **la fetta e' in ONCE, la zona la delimita** | ONCE suona la ZONA `[start,end]`, non tutto il file (come lo Slicer nativo); se senti la parola intera e' il PATTERN, non il mode |
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
