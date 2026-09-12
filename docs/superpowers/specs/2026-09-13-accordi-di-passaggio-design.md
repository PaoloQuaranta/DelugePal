# Gli accordi di passaggio e approccio — progetto

**Data:** 13 settembre 2026
**Cos'è:** la terza e ultima faccia del cromatismo. Copre la **diminuita di
passaggio** e la **sostituzione di tritono** (♭II7): la **colla cromatica**
funzionale dentro una tonalità.

## Perché, e la differenza con le altre due facce

Era l'ultimo punto in «cosa manca» del cromatismo. ⚠️ **A differenza del planing
e delle medianti** (colori NON funzionali, che sospendono il tonale), questi
accordi sono **funzionali**: stanno *dentro* una tonalità e servono a **lisciare
il movimento** fra due accordi diatonici, approcciando il successivo per
semitono. È il cromatismo del jazz e dello standard, non quello di Debussy.

## Il principio: un accordo infilato che approccia per semitono

Due dispositivi, tutt'e due `[LIB]` Smith, *Jazz Theory* (4ª ed.):

- **la diminuita di passaggio** — una `dim7` infilata fra due accordi diatonici
  a distanza di tono, col basso che sale (o scende) cromatico. In Do:
  `Cmaj7 → C#dim7 → Dm7`, basso do→do#→re. Smith cap. VIII, p. 59 (i «voice
  leading / linear chords»), e cap. IX, p. 75 (la dim7 come dominante nona
  incompleta, e il m7 che scivola cromatico fra due diatonici);
- **la sostituzione di tritono** — il `♭II7` al posto del `V7`: `Db7 → Cmaj7`
  invece di `G7 → Cmaj7`. Approccio cromatico dall'alto. Smith cap. VIII, p. 59,
  «Tritone Substitution: ♭II7 Substituted for V7».

`[CALC]` Il test blinda i due fatti che li definiscono: la diminuita di
passaggio ha la **fondamentale un semitono fra** i due accordi (basso cromatico
do→do#→re); il tritone sub **condivide il tritono** con il V7 che sostituisce
(Db7 e G7 hanno entrambi fa e si — la 3ª e la 7ª scambiate).

⚠️ **La condotta va TENUTA** (`condotta=True`, il default): la colla cromatica è
morbida proprio perché le voci si muovono di poco. Come le medianti, non come il
planing.

## Il pezzo di prova (da zero)

Un giro in Do che mostra i due dispositivi, su `set_scale` Do maggiore (la casa —
questi accordi sono funzionali, servono una tonalità):

```
Cmaj7 | C#dim7 | Dm7 | Db7 | Cmaj7 | C#dim7 | Dm7 | Db7
```

La **diminuita di passaggio** (C#dim7) sale cromatica fra Do e Re m; il **tritone
sub** (Db7) approccia Do dall'alto — un turnaround che rigira in cima. La melodia
tiene note d'accordo con una discesa sib→la→la♭ che eco del basso. `condotta=True`.
Rhodes / tromba / basso, niente batteria.

**Feasibility verificata:** `C#dim7`, `Db7` parsano; il basso è do→do#→re; Db7 e
G7 condividono {fa, si}; la condotta liscia la colla. Nessuna aggiunta a
`song.MODI` (la casa è Do maggiore).

## Come si verifica / cosa resta

Test `[CALC]` verde; pezzo caricato (`PASSAGG01`), ascoltato; verdetto → esempio
lavorato. **Con questo il cromatismo è chiuso** (planing, medianti, passaggio).
Resta fuori, sull'armonia: le doppie medianti, il diatonic planing, e i feel
non-swing del jazz — e poi si esce verso la priorità 2 (forma).

## Cosa NON rifare

- **non spegnere la condotta** qui: la colla è morbida perché le voci si muovono
  di poco (come le medianti, al contrario del planing);
- **non trattarli come colori statici**: sono funzionali, vivono dentro una
  tonalità e approcciano un bersaglio — toglierli dalla cadenza li svuota.
