# DnB / JUNGLE — l'amen affettato, ri-sequenziato, sotto un feel half-time

⚠️ **PERIMETRO.** Jungle e drum'n'bass **amen-led**: un break di batteria (l'amen)
**tagliato in fette** e **ri-sequenziato** a ~170 BPM, sotto un **sub half-time** e
un'**armonia minore** scura. È il primo genere della riga «elettronica · IDM · DnB ·
jungle». Non è una capacità nuova: lo **slicing** è lo stesso gesto del **vocal chop**
([vocal-chop.md](vocal-chop.md)) — cambia il **materiale** (un break, non una voce) e
il **fine del chop** (ricostruire un groove e poi editarlo, non rompere una parola).

> **La cosa da capire:** il break *è* una registrazione di un batterista vero. Le
> fette in ordine lo ricostruiscono; ri-ordinate lo **editano**. Il micro-timing
> umano è già dentro l'audio — non lo si mette con lo swing. E la corsa la fa il
> break: sotto, il basso e l'armonia vanno **lenti** (half-time), ed è quel contrasto
> a fare il DnB.

---

⚠️ **NIENTE CORPUS DnB/jungle in casa** (il Groove MIDI non ha l'etichetta):
`[LIB]`+`[DEC]`. Il **break** è `[OSS]` (l'audio di un'esecuzione vera, l'amen);
l'**analisi delle fette** (dov'è la cassa) è `[OSS]` stdlib; l'**armonia** è `[CALC]`;
il **chop** è `[DEC]`, da rifinire all'orecchio.

**Cosa ti serve prima di cominciare:**

- un **break** sulla SD (`SAMPLES/...`), meglio se **già al tempo del pezzo** (vedi §2
  perché conta), e la sua lunghezza in **frame** (`audio.wav_frames(path)[0]`);
- **quante fette** (§2): 64 = 1/16 su 4 battute, la risoluzione «jungle»;
- l'**armonia** (un vamp minore) e la **forma** (l'arco intro/drop/breakdown).

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | convenzione documentata |
| `[OSS]` | osservato (l'audio dell'amen, l'analisi stdlib delle fette, i file veri) |
| `[CALC]` | calcolato (l'armonia, con `racconta_armonia`) |
| `[DEC]` | deciso qui (il chop, il tempo, l'arco) |

---

## 1. Il break si affetta come il vocal chop — `kit.affetta`

Stesso meccanismo, stessa funzione, stessa regola del MODE: un kit di fette, ognuna
una `<zone>` dello stesso file, **REPEAT MODE ONCE** (la zona delimita la fetta, come
lo Slicer nativo). **Non si ripete qui**: sta in [vocal-chop.md](vocal-chop.md) §1-2.

```python
frames = audio.wav_frames('E:/SAMPLES/.../original AMEN.wav')[0]   # 268795
fette = kit.affetta(doc, iBreak, 'SAMPLES/.../original AMEN.wav', frames, n=64)
```

## 2. Il tempo, e perché il break va scelto già stretchato — `[DEC]`

⚠️ **Questo è ciò che distingue il break dal vocal chop.** Con ONCE ogni fetta suona
il suo audio alla **velocità nativa** del file. Se innesco le fette su una griglia
più **veloce** del loro tempo nativo, si **sovrappongono** (impastano); più lenta, si
aprono **buchi**. Per ricostruire il break pulito serve che **la durata della fetta =
il passo della griglia**, cioè:

> **tempo della song ≈ tempo nativo del break.**

L'amen usato (`original AMEN.wav`) è **già stretchato a ~171 BPM** (4 battute, 268795
frame): a song **171** una fetta da 1/16 dura quanto un 1/16, e in ordine il break
torna esatto. Un amen grezzo (es. `LOOP/amen.wav`, ~138) a 171 impasterebbe. **Scegli
il break al tempo del pezzo, o stretchalo prima** (il Deluge lo fa; `kit.affetta` no).

## 3. Il chop: ri-sequenziare per BEAT, non a caso — `[DEC]`

A differenza del vocal chop (dove le fette **in fila ricostruiscono la parola**, e il
chop sta nel **romperla**), qui in fila **ricostruiscono un groove** che suona bene: il
chop sta nell'**editarlo**. Le mosse che tengono il risultato musicale:

- ⚠️ **lavora per BEAT, non per singola fetta.** Un beat = **4 fette contigue** (con
  n=64) = un movimento coerente del batterista vero. Rimescolare i **beat** suona «amen
  editato»; rimescolare le fette singole a caso suona rotto;
- **le casse gravi sui movimenti forti.** Quali fette sono cassa lo dice un'**analisi
  di energia** (RMS + banda grave, stdlib — `tools` di sessione): nell'amen le casse
  gravi sono le fette **0, 24, 56**. Mettile a inizio delle battute (`[OSS]`);
- **rullate** (jungle snare roll): **stuttera** una fetta di rullante (4× un 1/16) per
  chiudere una frase — il «brrrap» del turnaround;
- **ripeti l'attacco**: riprendere il beat 0 (la cassa iconica) a metà giro àncora
  l'orecchio.

Si scrive come una batteria: `MU.scrivi(doc, clip, note, dove='fetta 12')`.

## 4. Il feel è DRITTO, e non è una dimenticanza — `[DEC]`

⚠️ **`set_swing(50)`.** Il break porta il suo micro-timing **nell'audio delle fette**:
uno swing di song lo sposterebbe una **seconda** volta (e sposterebbe anche sub e pad).
Il groove umano lo dà il disco, non `set_swing`. (È il contrario dello swing jazz, dove
il feel è nelle posizioni scritte — vedi la memoria `riflesso-idioma-fuori-contesto`:
non trasferire un idioma dove non va.)

## 5. Il half-time: il basso e l'armonia vanno lenti — `[DEC]`

Il DnB «si sente a metà tempo» non perché la batteria rallenti, ma perché **tutto il
resto** va lento:

- **SUB** (Square Saw Bass scurito): fondamentale grave **tenuta sul 1** (~3 movimenti)
  + una spinta corta sul 4, per battuta, sulle fondamentali del vamp. **Rado**: è il
  break a correre. Registro molto grave (C2 e sotto);
- **ARMONIA** (priorità 1, `[CALC]`): un vamp **minore** scuro, ritmo armonico lento
  (un accordo per battuta o meno). Rootless, tenuto, sul Rhodes/pad. Si scrive con
  `MU.armonia` (che conduce le parti) e si chiude col `[CALC]` (`racconta_armonia`).
  L'esempio: `Cm9 | Abmaj7 | Cm9 | G7b9` — i–♭VI–i–V7♭9 (il ♭VI caldo cinematico, la
  dominante alterata scura), lo stesso colore approvato nel trip-hop.

## 6. La forma — `[DEC]`

L'arco jungle vive di **entrate**: il break si enuncia, poi il **drop** aggiunge peso
(sub) e colore (armonia), poi il **breakdown** toglie il break (la tensione), poi si
ri-droppa. L'esempio, 32 battute con `MU.forma`:

```
intro  8 batt.  break solo                         (il groove si enuncia)
drop   8 batt.  break + sub + pad                  (il peso e il colore entrano)
break  8 batt.  sub + pad, il BREAK esce           (la tensione)
drop   8 batt.  rientro pieno
```

---

## I vincoli

| vincolo | perché |
|---|---|
| **il break al tempo del pezzo** | ONCE suona la fetta a velocità nativa; se il nativo ≠ song, impasta o buca (§2) |
| **chop per beat, non per fetta** | 4 fette contigue = un movimento coerente; rimescolare i beat resta musicale, le fette a caso no |
| **feel dritto (swing 50)** | il micro-timing è nell'audio; lo swing lo sposterebbe due volte |
| **il sub è rado e grave** | il half-time lo fa il contrasto col break veloce; un basso fitto lo ucciderebbe |
| **l'armonia è scura e lenta** | minore, ritmo armonico lento, curata col `[CALC]` — è la priorità 1 |
| **il campione è sulla SD** | il `fileName` è relativo (`SAMPLES/...`); se il file non c'è, silenzio |
| **niente riflesso** | il chop e l'arco si compongono PER il pezzo, all'orecchio |

---

## L'esempio lavorato

`tools/dnb_scritto.py`: `original AMEN.wav` in **64 fette**, ri-sequenziato per beat
(+ due rullate) a **171 BPM dritto**; **sub** half-time e **pad** minore
(`Cm9 | Abmaj7 | Cm9 | G7b9`, `[CALC]`) con un velo di riverbero; forma
intro→drop→breakdown→drop su **32 battute**. ⚠️ **Il kit AMEN porta anche un drum a
parte, `amen intero`** (l'ultima riga): il loop completo in one-shot (zona `[0, FRAMES]`,
ONCE), **non sequenziato** — serve a sentire il break originale innescandolo a mano
(richiesta dell'utente). Caricato **via SysEx come DNB02** (la v1 senza l'intero era già
`DNB01`; `put` non sovrascrive).
⚠️ **Verdetto dell'ascolto (19 settembre 2026): *«va bene»*.** Il chop, l'arco e i
livelli restano `[DEC]`, rifinibili all'orecchio (anche **quali beat** stanno bene
insieme si decide sentendo, come il vocal chop).

---

## Cosa manca a questo documento

- il **taglio sui transienti** (onset) invece che a fette uguali: più fedele agli hit
  dell'amen, ma vuole analisi audio più fine (stdlib, senza numpy) — futuro;
- la **Reese bass** (il basso detunato del DnB darkside/neurofunk) e i **layer** di
  cassa/rullante sotto il break: sound design, non ancora fatto;
- i **sottogeneri** (liquid, jungle ragga, neuro): qui c'è l'ossatura amen-led, non i
  dialetti;
- il **verdetto d'ascolto**: il pezzo è `[DEC]`, aspetta l'orecchio.
