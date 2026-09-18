# Trip-hop

**Parziale.** Compilata il 18 settembre 2026, **terzo genere del perimetro 3**.
Il trip-hop non è una capacità nuova ma una **fusione con un carattere**
(Portishead, Massive Attack): batteria hip-hop rallentata, basso dub, **armonia
minore jazzy** (il cuore), e lo spazio del dub. ⚠️ **Niente corpus** trip-hop
(il Groove MIDI non ha l'etichetta) → `[LIB]`+`[DEC]`; la batteria si appoggia al
`[MIS]` boom-bap dell'hip hop, l'armonia si chiude col `[CALC]`, l'eco è `[OSS]`.

Il dettaglio operativo sta in [trip-hop.md](../istruzioni/trip-hop.md), che rimanda
a [batteria-hiphop.md](../istruzioni/batteria-hiphop.md) e
[basso-hiphop.md](../istruzioni/basso-hiphop.md); l'esempio in
`tools/triphop_scritto.py`. Questa scheda è la vista per casella.

Il grado di prova: `[LIB]` convenzione · `[MIS]` misurato · `[CALC]` calcolato ·
`[OSS]` osservato · `[DEC]` deciso qui.

---

## 1. Cos'è, e cosa non è

**Parziale.** `[LIB]`+`[DEC]` Copre il **downtempo scuro e cinematico** alla
Portishead — un angolo di un genere ampio. È la fusione di tre lingue: la
**batteria** dell'hip-hop (rallentata, polverosa), il **basso** e lo **spazio** del
dub, l'**armonia** del jazz minore. Hazy, pigro, con molta aria.

**Cosa NON è:** l'hip-hop dritto (qui è più lento e laid-back), la house (non
four-on-the-floor), la techno (non ipnotico-ritmico: qui comanda l'armonia e
l'atmosfera).

## 2. Metro e griglia

`[DEC]` 4/4, **16 passi**. Spesso sentito in **half-time** (il backbeat pare cadere
ogni due movimenti, non ogni uno).

## 3. Tempo

`[LIB]`+`[DEC]` **~70-90 BPM**, downtempo. L'esempio è a **84**.

## 4. Feel

`[LIB]`+`[DEC]` **Laid-back**: dietro la griglia, pigro. Uno **swing leggero**
(`S.set_swing(doc, 56)`, il lilt lo-fi) — non dritto, non terzinato. La pigrizia è
il carattere.

## 5. Ruoli e spartizione

La spartizione: **Rhodes = l'armonia** (il cuore, tenuta e molle), **basso = il
sub dub** (rado, tenuto), **batteria = il groove polveroso** (boom-bap morbido),
**eco/riverbero = lo spazio** (metà del genere).

- **batteria** `[LIB]`+`[DEC]` su base `[MIS]`: boom-bap rallentato e morbido (cassa
  1-3 + sincope, backbeat velluto sul 2-4, ghost molli, hi-hat in crome con aria).
  Vedi [batteria-hiphop.md](../istruzioni/batteria-hiphop.md), variante lo-fi;
- **basso** `[LIB]`+`[DEC]`: dub, sub profondo, rado e tenuto, sulle fondamentali;
- **Rhodes**: il vamp minore, rootless, tenuto (casella 7).

## 6. Dinamica

`[DEC]` **Morbida.** Il backbeat non spacca (velocity ~105, non 127 del boom-bap);
i ghost molli (~40); l'hi-hat sotto. Il velluto è il punto. Le sfumature (velocity,
swing) sono punti di partenza regolabili, non leggi.

## 7. Armonia

`[CALC]` **Il cuore del genere.** Minore e jazzy, ed è **scelta compositiva** (come
per hip hop e i sottogeneri jazz — *il sapore è una scelta, non un'estrazione*):
accordi estesi (min7/min9, maj7 dei gradi presi in prestito), **prestiti modali**
(il **♭VI** caldo, cinematico), **dominanti alterate** (V7♭9 scura). Rhodes
rootless, registro medio-grave, tenuto — è l'eco a muoverlo. Si scrive con
`MU.armonia` (che conduce le parti); il `[CALC]` (`racconta_armonia`) dà le note e
scioglie le ambiguità. L'esempio: `Cm9 | Cm9 | A♭maj7 | G7♭9` (i–i–♭VI–V7♭9),
verificato col calcolo.

## 8. Melodia e ornamentazione

**Parziale.** `[DEC]` La linea di superficie del trip-hop è spesso un **vocal
breathy** o un **sample/hook**. Il **vocal chop** (il sample tagliato) ora è coperto:
`kit.affetta` fa un kit di fette (MODE CUT, si fermano con la nota), innescate a ritmo — vedi
[vocal-chop.md](../istruzioni/vocal-chop.md), esempio `tools/vocalchop_scritto.py`.
L'armonia (casella 7) porta il colore. ⚠️ **Resta fuori** il **vocal cantato** vero
(breathy, una registrazione, non generabile): per questo la casella è ancora
parziale.

## 9. Forma e densità

**Parziale.** `[DEC]` Il trip-hop vive di **loop ipnotici** con entrate/uscite: un
intro atmosferico (solo Rhodes + eco) da cui **entra il beat**, poi il giro pieno.
L'esempio: intro (4 battute, solo Rhodes) → full (tutti), con `MU.forma`. La forma
lunga (strofa/ritornello, breakdown dub) è accennata, non sviluppata.

## 10. Sul Deluge

`[DEC]` I suoni: `Tal Rhodes` (il Rhodes caldo), `Square Saw Bass` scurito (il sub),
kit **KIT009** (polveroso). Lo **spazio**:

- **eco dub** — `MU.eco_dub(doc, bersaglio, feedback, sync, analog=True, pingpong=True)`:
  sull'strumento l'elemento `<delay>` con **`analog=1`** (il degrado caldo a ogni
  ripetizione, il suono del dub), sincronizzato; sulle clip `delayFeedback`. `[OSS]`
  la struttura (attributi nel preset), `[da verificare]` i livelli. ⚠️ **Il feedback
  non resta positivo (oltre il 50%) a fine brano** o l'eco non decade (drone/runaway):
  default 24, gate in `MU.avvertenze()` (memoria `delay-feedback-non-positivo`);
- **riverbero** — un velo (`reverbAmount`) per la profondità hazy.

## 11. Trappole del generatore

- **non corre**: il trip-hop è lento e laid-back; se il groove è dritto e veloce non
  è trip-hop;
- **la batteria non spacca**: backbeat morbido, non il 127 del boom-bap; e lascia
  aria (crome, non sedicesimi);
- **il basso è rado**: dub, non una linea fitta; peso e spazio;
- **l'armonia è il cuore**: minore, estesa, curata col `[CALC]` — non un vamp
  qualunque;
- **lo spazio è uno strumento**: senza eco e riverbero manca metà del genere;
- **niente riflesso**: non incollare un idioma d'altro feel; fonda PER il trip-hop.

### Fonti

- ⚠️ **Nessun corpus** trip-hop nel Groove MIDI (nessuna etichetta): `[LIB]`+`[DEC]`.
  La batteria si appoggia al `[MIS]` boom-bap dell'hip hop (34 esecuzioni, 5
  batteristi), rallentato; l'armonia è `[CALC]`; l'eco è `[OSS]` (attributi del preset);
- istruzione [trip-hop.md](../istruzioni/trip-hop.md), che rimanda a
  [batteria-hiphop.md](../istruzioni/batteria-hiphop.md) e
  [basso-hiphop.md](../istruzioni/basso-hiphop.md); esempio `tools/triphop_scritto.py`;
- **verdetto d'ascolto (18 settembre 2026): *«per il resto va bene»*** — con una
  correzione: l'eco aveva feedback positivo (runaway), portato a 24 (decade).
  L'armonia era già chiusa col `[CALC]`.
