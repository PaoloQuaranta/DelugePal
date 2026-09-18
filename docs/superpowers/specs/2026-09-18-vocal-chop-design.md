# Vocal chop — affettare un campione in un kit, e suonarlo a ritmo — progetto

**Data:** 18 settembre 2026
**Cos'è:** il **vocal chop** — la casella 8 di house/trip-hop lasciata aperta perché
è **audio**, non note. Si taglia un campione vocale in fette (una per drum row di un
kit) e le si innesca a ritmo. Lo **stesso meccanismo** (slicing) sblocca poi
jungle/DnB (il break tagliato).

## Perché, e cosa si è deciso

Deciso in brainstorming il 18 settembre 2026, dopo aver guardato la documentazione
(su richiesta dell'utente):

- il campione è **`SAMPLES/RECORD/REC00027.WAV`** (il «mmyeah» dell'utente, dalla
  song `Mmmyeah.XML`): **142725 frame, mono 24-bit 44.1k, ~3,24 s** (letti con
  `audio.wav_frames`);
- **8 fette** uguali, contesto **house** (four-on-the-floor, la casa del vocal chop);
- **ricombinazione + una primitiva** (`kit.affetta`), come per il trip-hop.

⚠️ **La documentazione ha corretto il design** (regola 0):
- il Deluge ha uno **Slicer nativo** (in CLIPS: tieni premuto Select → SLICE → N):
  fa un **kit con una riga per fetta** ([delugecommunity.com](https://delugecommunity.com),
  Audio Files);
- nel file, una fetta è `<osc type="sample" loopMode="…" …><zone startSamplePos="…"
  endSamplePos="…"/></osc>`, posizioni in **frame** (FINDINGS §«Campioni e tick»);
- il **MODE** (ONCE/CUT/LOOP/STRETCH) è l'attributo **`loopMode`** (intero 0-3); una
  fetta corta (< 2 s) vuole **ONCE** (suona intera all'innesco).

⚠️ **`dir` via SysEx FUNZIONA su questo firmware** (per cartelle non enormi) — il
vecchio HANDOFF diceva di no. Le cartelle grandi (`/SONGS/`, 137 voci) però non
rispondono; la SD nel lettore resta la via comoda. (Da aggiornare in `docs`.)

## Come si evita di scrivere un `loopMode` alla cieca

Non c'è un kit affettato sulla SD da imitare, e `loopMode` è device-behavior (non si
indovina, memoria del progetto). Soluzione: **i drum-fetta si costruiscono COPIANDO
un drum one-shot vero** (un kick di `808 From Mars`, che ha già il `loopMode` giusto
per un one-shot) e cambiando **solo** `fileName` e la `<zone>`. Il `loopMode` è così
**ereditato da un drum che funziona**, non scritto a mano. ⚠️ Se all'ascolto la
fetta viene troncata invece di suonare intera, è lì che si interviene (verifica sul
dispositivo).

## I tre artefatti di questo giro

### 1. La primitiva — `kit.affetta`

```
affetta(doc, kit, path, frames, *, n=16, base=0) -> list[str]
```

Trasforma un `kit` (nodo strumento kit, con almeno un drum) in un **kit di N fette**:
- porta i drum del kit a **N**, copiando il drum `base` (per ereditarne `loopMode`,
  `reversed`, gli inviluppi — un one-shot che funziona);
- su ogni drum `i` scrive `fileName=path` e la `<zone>` a
  `[i·frames//n, (i+1)·frames//n]` con `kit.set_sample` (che gia' scrive `type=sample`
  e la zona);
- aggiorna le noteRow delle clip del kit (una riga per drum), come fa `kit.add_drum`;
- ritorna i **nomi** dei drum-fetta (`fetta 1`… `fetta N`), per scriverci le note.

`path` è **relativo alla SD** (`SAMPLES/RECORD/REC00027.WAV`), come lo scrive il
dispositivo. `frames` viene da `audio.wav_frames(path_locale)[0]`. Riusabile per il
**break** (jungle/DnB) con lo stesso identico gesto.

### 2. Il pezzo — `tools/vocalchop_scritto.py`

House four-on-the-floor + il vocal chop come **hook**:
- **~124 BPM**, kit **808** per il beat (cassa four-on-floor, clap 2-4, open hat sui
  levare, closed hat) — riusa gli idiomi di `batteria-house.md`;
- un **kit di 8 fette** dell'mmyeah (`kit.affetta(..., n=8)`), innescate a ritmo: un
  pattern di chop che ripete/stuttera le fette (es. `1 . 1 2 . 3 . 4` — un gioco di
  frammenti, non tutte le 8 in fila), `[DEC]` all'orecchio;
- un basso house in levare (riuso `basso-house.md`) e, volendo, uno stab — minimale,
  il vocal è il protagonista;
- forma breve con `MU.forma` o una singola sezione loopata;
- `verifica()` vuota, `avvertenze()` pulite; `test_vocalchop_scritto`.

### 3. L'istruzione — `docs/istruzioni/vocal-chop.md`

Il vocal chop: cos'è (un campione vocale tagliato in un kit di fette, innescate a
ritmo), come si taglia (`kit.affetta`, fette uguali; lo Slicer nativo fa lo stesso),
il MODE one-shot (ereditato da un drum vero), come si compone il chop (ripetizioni,
stutter, ri-ordine delle fette — è ritmo + scelta), e il legame col **break**
(jungle/DnB: stesso meccanismo su un break di batteria). Gradi: `[LIB]`+`[DEC]`;
struttura della fetta `[OSS]` (Slicer/FINDINGS); la scelta del taglio è compositiva.

## La scheda e l'indice

- `docs/repertori/house.md` **casella 8**: da «Vuota/parziale» a piena per il **vocal
  chop** (oltre al lead acid già presente); link a `vocal-chop.md`, esempio
  `tools/vocalchop_scritto.py`.
- `docs/repertori/trip-hop.md` **casella 8**: il vocal chop ora è coperto (era
  dichiarato mancante); link a `vocal-chop.md`.
- Nessuna riga d'indice nuova (vocal chop non è un repertorio: è una tecnica che
  riempie la casella 8 di due repertori). L'indice si aggiorna solo se cambiano gli
  stati delle caselle 8 (contratto: verificare che indice == scheda).

## Il caricamento (SD nel lettore)

La SD è nel lettore (`E:`), il Deluge è scollegato. Il campione è già sulla SD
(`SAMPLES/RECORD/REC00027.WAV`): **niente upload**. Il pezzo si scrive
**direttamente** in `E:\SONGS\DelugePal\` (la sottocartella DelugePal, regola 5
rispettata), col nome da `MU.destinazione()` (validazione), senza SysEx. Poi l'utente
rimette la SD nel Deluge e apre la song.

## Cosa resta fuori (YAGNI)

- il **taglio sui transienti** (onset): scelto «fette uguali»; l'onset resta futuro
  (serve analisi audio, stdlib senza numpy);
- il **break** vero (jungle/DnB): la primitiva lo abilita, ma è un altro pezzo/genere;
- il **pitch/stretch** delle fette, gli effetti sul vocal: sound design, all'orecchio.

## Rischi e come si chiudono

| rischio | mossa |
|---|---|
| `loopMode` sbagliato → la fetta si tronca | ereditato da un drum one-shot vero; se all'ascolto tronca, si corregge sul dispositivo |
| la fetta non suona (sample mancante/percorso) | il file è sulla SD (verificato su E:); `fileName` relativo come lo scrive il dispositivo |
| il chop suona meccanico | il pattern delle fette è `[DEC]` all'orecchio (ripetizioni/stutter), non tutte in fila |
| scrivere fuori da DelugePal sulla SD | percorso `E:\SONGS\DelugePal\`, nome da `MU.destinazione()`; mai la radice |
| fine-riga / `print` non-ASCII | `write_bytes`/LF, `git diff` coerente; solo ASCII nei `print` |

## Fatto =

- `kit.affetta` col test verde (N drum, zone corrette, loopMode ereditato);
- `vocalchop_scritto.py` che costruisce il pezzo, `verifica()` vuota, `test_vocalchop_scritto` verde;
- istruzione e schede (casella 8 di house e trip-hop) coerenti; suite INTERA verde prima di committare le schede;
- il pezzo scritto in `E:\SONGS\DelugePal\` per l'ascolto — la scelta del taglio e del pattern la chiude l'orecchio.
