# Gli accordi di passaggio e approccio

**A cosa serve.** Hai due accordi diatonici e vuoi legarli più liscio, o dare
una spinta all'arrivo: infili **un accordo cromatico** che approccia il
successivo per semitono. È la **colla** del jazz e dello standard — la diminuita
che passa, la dominante che arriva dall'alto.

È priorità 1 (armonia), la terza e ultima faccia del **cromatismo**.

⚠️ **Questi sono FUNZIONALI**, al contrario dell'[armonia parallela](armonia-parallela.md)
e delle [medianti cromatiche](medianti-cromatiche.md) — che sono colori che
sospendono il tonale. Qui il cromatismo serve la tonalità: l'accordo infilato
approccia un bersaglio diatonico, e la casa resta.

**Cosa ti serve prima di cominciare:** un giro diatonico (la casa — come si
costruisce: [`armonia-funzionale.md`](armonia-funzionale.md)) e il punto dove
vuoi la colla.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sulle note, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

---

## I due dispositivi

### La diminuita di passaggio

Una `dim7` infilata fra due accordi diatonici a distanza di tono, col basso che
sale (o scende) **cromatico**. In Do: `Cmaj7 → C#dim7 → Dm7`, basso do→do#→re.
`[LIB]` Smith, *Jazz Theory* (4ª ed.), cap. VIII p. 59 (i «voice leading /
linear chords», accordi fatti di note di passaggio e di volta) e cap. IX p. 75
(la dim7 trattata come una dominante nona incompleta, e il m7 che scivola
cromatico fra due diatonici). `[CALC]` La fondamentale della diminuita sta **un
semitono fra** i due accordi — è quella a portare il basso cromatico.

### La sostituzione di tritono (♭II7)

Il `♭II7` al posto del `V7`: `Db7 → Cmaj7` invece di `G7 → Cmaj7`. Approccio
cromatico **dall'alto**. `[LIB]` Smith, cap. VIII p. 59 (e Levine, *The Jazz
Piano Book*, cap. 6 «Tritone Substitution»), «Tritone Substitution:
♭II7 Substituted for V7». `[CALC]` Funziona perché il ♭II7 e il V7 **condividono
il tritono**: G7 ha fa-si (la 3ª e la 7ª), e Db7 ha le stesse due note scambiate
— è il tritono a risolvere, e lo fa uguale con tutt'e due le fondamentali.

`[CALC]` Il test `test_accordi_di_passaggio` blinda i due fatti: il basso
cromatico do→do#→re, e il tritono condiviso fra Db7 e G7.

---

## Il punto tecnico: la condotta va TENUTA

⚠️ `MU.armonia(..., condotta=True)` — il default, e qui serve. La colla è liscia
**perché le voci si muovono di poco**: la condotta lega la diminuita di
passaggio e il tritone sub ai loro vicini. È come le medianti, al contrario del
planing (dove la condotta andava spenta).

---

## Come si stabilisce

1. **la diminuita di passaggio:** fra due accordi diatonici a un tono di
   distanza (I e ii, o ii e iii), infila la `dim7` sul semitono in mezzo, col
   basso cromatico;
2. **il tritone sub:** dove andrebbe un `V7`, mettici il `♭II7` — stessa tensione
   (lo stesso tritono), basso che scende di un semitono sul bersaglio;
3. **risolvi.** A differenza di planing e medianti, qui l'accordo cromatico
   **deve** andare da qualche parte: è una preparazione, non un colore fermo.

---

## Come si scrive, materialmente

```python
from delugexml import song as S, musica as MU

S.set_scale(doc, 'C', 'maggiore')      # la casa: sono funzionali
note = MU.armonia('Cmaj7 | C#dim7 | Dm7 | Db7 | Cmaj7', registro='do3',
                  durata='1/1')         # condotta di default (True): colla morbida
```

---

## Esempio lavorato: il turnaround cromatico

`[OSS]` La terza faccia del cromatismo provata — 13 settembre 2026. In
[`tools/passaggio_scritto.py`](../../tools/passaggio_scritto.py).

**L'idea:** la colla cromatica pura, da zero. Otto battute, tre voci, niente
batteria.

**La progressione** — un turnaround in Do coi due dispositivi:

```
Cmaj7 | C#dim7 | Dm7 | Db7 | Cmaj7 | C#dim7 | Dm7 | Db7
```

La **diminuita di passaggio** (C#dim7) sale cromatica fra Do e Re m (basso
do→do#→re); il **tritone sub** (Db7) approccia Do dall'alto al posto del Sol7.
`condotta=True`: la colla è morbida. Il Db7 finale rigira sul Cmaj7 in cima — il
turnaround.

**Dove si gioca:** il basso cromatico del passaggio e l'approccio dall'alto del
tritone sub. A differenza di planing e medianti, qui il cromatismo **risolve**:
è la colla funzionale dello standard.

**Verdetto: approvato.** Con questo il **cromatismo è chiuso**, tre facce su tre:
il **planing** (stream parallelo), le **medianti** (scarto di terza), il
**passaggio/approccio** (colla funzionale). L'armonia ha retto anche qui al primo
colpo.

---

## Cosa manca a questa istruzione

Con gli accordi di passaggio e approccio **il cromatismo è chiuso**: planing
(stream parallelo), medianti (scarto di terza), passaggio/approccio (colla
funzionale). Restano fuori, sull'armonia:

- **le doppie medianti cromatiche** (terza senza nota in comune);
- **il diatonic planing** (scivolare dentro una scala);
- i **feel non-swing del jazz** (in due, latin, funk) — e poi la **priorità 2,
  la forma** (voicing, contrappunto, comping, struttura).
