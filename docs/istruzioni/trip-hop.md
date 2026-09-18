# Comporre TRIP-HOP — la fusione (hip-hop + dub + armonia minore), e lo spazio

⚠️ **PERIMETRO.** Il trip-hop (Portishead, Massive Attack, Tricky) è **downtempo
scuro e cinematico**: non una capacità nuova, ma una **fusione con un carattere**.
Prende la **batteria** dall'hip-hop (rallentata, polverosa), il **basso** e lo
**spazio** dal dub, l'**armonia** dal jazz minore. Questo documento tiene insieme i
pezzi e dà il carattere; i dettagli delle singole parti stanno nelle istruzioni a
cui rimanda — non si ripetono qui.

> **La cosa da capire:** il trip-hop è **lento, hazy, dietro il beat**. Il groove è
> pesante e pigro, l'armonia è scura e ricca, e l'**atmosfera** (l'eco, il
> riverbero, il fruscio) è metà del genere. Non è musica «piena»: è musica che
> **respira**, con molto spazio.

---

⚠️ **NIENTE CORPUS trip-hop** (il Groove MIDI non ha l'etichetta): `[LIB]`+`[DEC]`.
La batteria si appoggia al `[MIS]` **boom-bap** dell'hip-hop, rallentato. L'armonia
si chiude col `[CALC]`. L'eco è `[OSS]` (struttura) + `[da verificare]` (livelli).

**Cosa ti serve prima di cominciare:**

- un **Rhodes** o un piano elettrico caldo (nel progetto: `Tal Rhodes`);
- un **sub** grave (`Square Saw Bass` scurito);
- un **kit polveroso** (acustico/vinilico, non troppo pulito);
- il giro armonico (minore).

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | convenzione documentata |
| `[MIS]` | misurato (qui: la batteria boom-bap dell'hip-hop, rallentata) |
| `[CALC]` | l'armonia, chiusa dal calcolo |
| `[OSS]` | struttura osservata (l'eco, nel preset) |
| `[DEC]` | decisione presa qui |

---

## 1. Il feel — lento, laid-back

`[LIB]`+`[DEC]` Tempo **~70-90 BPM** (l'esempio a **84**), spesso sentito in
**half-time**. Il carattere è **laid-back**: dietro la griglia, pigro. Uno **swing
leggero** (`S.set_swing(doc, ~56)`) dà il lilt lo-fi; non è dritto come il boom-bap
classico né terzinato come lo swing. La pigrizia è il punto.

## 2. La batteria — boom-bap rallentato e morbido

`[LIB]`+`[DEC]` (su base `[MIS]` hip-hop) La batteria è il **boom-bap dell'hip-hop
rallentato**, ma **più morbido e con più aria**:

- cassa sul **1 e 3** + una sincope sul levare (come il boom-bap);
- backbeat sul **2 e 4** ma **meno violento** (velocity ~105, non 127): il
  trip-hop è velluto, non spacca come il boom-bap East Coast;
- **ghost molli**, hi-hat in **crome** (non sedicesimi) con parsimonia — l'aria
  fa il genere;
- polveroso: il kit è vinilico/filtrato (sound design, `dsp-recipes`).

⚠️ **Non ripetere qui il boom-bap:** il vocabolario, le percentuali e il pocket
stanno in [batteria-hiphop.md](batteria-hiphop.md) (con la variante **lo-fi
swingata**, che è esattamente il feel giusto). Si parte da lì e si **rallenta e
ammorbidisce**.

## 3. Il basso — dub, sub, rado

`[LIB]`+`[DEC]` Il basso è **dub**: **sub profondo**, **rado**, **tenuto**, dietro
il beat. Segue le **fondamentali** del giro, con note lunghe che riempiono lo
spazio sotto. Poche note, molto peso. Vedi [basso-hiphop.md](basso-hiphop.md) per
il sub agganciato; qui è ancora **più rado e tenuto** (l'anima dub).

## 4. L'armonia — il cuore, minore e jazzy

`[CALC]` È il centro del trip-hop, ed è **scelta compositiva** (come per l'hip-hop
e i sottogeneri jazz: *il sapore è una scelta, non un'estrazione*). Il colore:
**minore**, con accordi **estesi** (min7/min9, maj7 dei gradi presi in prestito),
**prestiti modali** (il **♭VI** caldo e cinematico) e **dominanti alterate** (la
V7♭9 scura). Rhodes **rootless**, in registro medio-grave, accordi **tenuti e
molli** — è l'eco a muoverli.

Si scrive coi **moduli d'armonia** del progetto (`MU.armonia`, che conduce le
parti): l'esempio usa `Cm9 | Cm9 | A♭maj7 | G7♭9` — i–i–♭VI–V7♭9. Il `[CALC]`
(`racconta_armonia`) dà le note esatte e scioglie le ambiguità; per l'armonia il
calcolo **sostituisce** l'ascolto.

## 5. Lo spazio — l'eco e il riverbero

`[OSS]`+`[da verificare]` L'atmosfera è metà del genere. L'**eco dub** —
`MU.eco_dub(doc, bersaglio, feedback=…, sync=…, analog=True, pingpong=True)` — mette
sull'strumento un delay **analog** (che **degrada** a ogni ripetizione, il suono
del dub), **sincronizzato** al tempo, con feedback; sulle clip il `delayFeedback`.
Più un velo di **riverbero** (`reverbAmount`). Sul Rhodes e su colpi isolati, l'eco
crea la profondità hazy.

⚠️ **Il feedback non deve restare positivo (oltre il 50%, display > 25) a fine
brano:** l'eco non decade e resta un drone/runaway (peggio con `analog`, che
auto-oscilla). `MU.eco_dub` ha default 24 apposta, e `MU.avvertenze()` segnala ogni
feedback positivo lasciato. Un feedback alto va bene solo se automatizzato **giù**
prima della fine. È una **regola di sicurezza**, non una sfumatura.

---

## I vincoli

| vincolo | perché |
|---|---|
| **lento e laid-back** | il trip-hop è pigro, dietro il beat; se corre, non è trip-hop |
| **la batteria respira** | boom-bap rallentato e con aria; morbido, non martellato |
| **il basso è rado e tenuto** | dub: peso e spazio, non tante note |
| **l'armonia è scura e ricca** | minore, estesa, prestiti — è il cuore, la si cura col `[CALC]` |
| **lo spazio è uno strumento** | l'eco e il riverbero non sono un ripensamento |
| **niente riflesso da altri feel** | non incollare lo spang-a-lang o un groove d'altrove: fonda PER il trip-hop |

---

## Come si decide una battuta

**«Che colore ha l'armonia qui, e quanto spazio lascio intorno?»**

1. **L'armonia** (il cuore): scegli il grado e l'estensione, chiudi col `[CALC]`.
2. **Il groove**: boom-bap rallentato e morbido; cassa 1-3, backbeat velluto, aria.
3. **Il sub**: la fondamentale, tenuta, dietro il beat.
4. **Lo spazio**: dove l'eco e il riverbero aprono la profondità.

---

## L'esempio lavorato

`tools/triphop_scritto.py`: ~84 BPM, Do minore, il vamp `Cm9 | Cm9 | A♭maj7 | G7♭9`
sul Rhodes con eco dub + riverbero (armonia chiusa col `[CALC]`), batteria boom-bap
rallentata laid-back, basso sub dub, forma intro → full. `verifica()` vuota.
⚠️ **Verdetto dell'ascolto (18 settembre 2026): *«per il resto va bene»*** — con
una correzione: l'eco aveva un feedback positivo (runaway), portato a 24 (decade).
L'armonia era già chiusa col calcolo.

---

## Cosa manca a questo documento

- il **`[MIS]`** trip-hop: non esiste (nessun corpus dedicato); la batteria è il
  boom-bap `[MIS]` rallentato;
- il **vocal breathy** e il **vinyl crackle / sample**: sono l'altra faccia del
  topline, e vivono in `audio.py` (campioni), non nelle note;
- la **taratura** dei livelli dell'eco e dello swing: `[da verificare]`, sfumature.
