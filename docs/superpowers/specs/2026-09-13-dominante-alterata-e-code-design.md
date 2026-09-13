# La dominante alterata e le code dell'armonia — progetto

**Data:** 13 settembre 2026
**Cos'è:** il secondo blocco che chiude l'armonia dopo la spina funzionale. Due
cose insieme, **stesso metodo** (`[LIB]` + `[CALC]`, niente esempio all'ascolto):

1. **la dominante alterata** — la tensione *dopo* la funzione;
2. **le code piccole** — doppie medianti, diatonic planing, + le seste aumentate.

## Item 1 — `dominante-alterata.md`

**A cosa serve.** Caricare di tensione una V7 che risolve (♭9, ♯9, ♯11, ♭13), e
dire **quale scala** dà quali tensioni. Raccoglie l'«uso funzionale» che
`scala-ottatonica` e `scala-esatonale` avevano parcheggiato.

**Quattro scale per la dominante:**

- **alterata** (super-locria) → tutte le alterazioni; **lidia dominante** → ♯11
  con 9 e 13 naturali. `[CALC]` Sono modi della **minore melodica** (7º e 4º),
  aggiunti a `song.MODI` (`alterata`, `lidia dominante`). ⚠️ **I libri non le
  nominano** (Smith rifiuta il multi-scala, p. 77-78; rimanda a Russell): come le
  medianti cromatiche, il rigore è nel `[CALC]`, senza forzare la citazione;
- **ottatonica HW** → dom7♭9. `[LIB]` Smith p. 77 («the diminished scale often
  works well with altered chords»);
- **esatonale** → dom7♯5, senza 5ª giusta. `[LIB]` Piston cap. 31, p. 490.

**`[LIB]` del principio:** Smith cap. VIII, p. 57 («Tensions and Chord Function»:
le tensioni non cambiano la funzione) e p. 78 (Parker: ♭9/♯9/+11/♭13 come
materiale melodico).

**`[CALC]` — `test_dominante_alterata`:** alterata e lidia dominante sono modi
della melodica; ognuna delle quattro scale tiene le note guida del V7 (3ª+7ª) e
dà le sue tensioni; la lidia dominante ha ♯11 e 13 naturale (niente ♭13);
l'esatonale ha ♯5 e non la 5ª giusta.

## Item 2 — le code

- **doppie medianti** → nuova sezione in `medianti-cromatiche.md`: a terza ma
  **senza nessuna** nota in comune (Do → Fa#, a tritono). `[CALC]`
  `test_medianti_doppie`: zero note in comune (contro una della cromatica, due
  della diatonica);
- **diatonic planing** → nuova sezione in `armonia-parallela.md`: la forma scivola
  **dentro una scala**, per grado, e flette (`condotta=False`). `[CALC]`
  `test_diatonic_planing`: i sette accordi di terza del Do maggiore sono dentro la
  scala e la forma flette (>1 qualità);
- **seste aumentate** → nuova istruzione `seste-aumentate.md`: it./ted./fr., la
  sesta aumentata ♭6–♯4 che si allarga sulla dominante. `[LIB]` Piston cap. 27
  «Augmented Sixth Chords», p. 419-420 («expands... to the octave on the
  dominant»; «V of V with lowered fifth»). `[CALC]` `test_seste_aumentate`: ♭6 e
  ♯4 a un semitono dalla dominante da versi opposti; la **tedesca è
  enarmonicamente un dom7** (Lab7 = il tritone sub — la parentela che Piston
  chiama «V di V con quinta abbassata»).

## Feasibility

Le sigle alterate (`7b9, 7#9, 7#5, 7#11, 7b13, 7alt`) e i dom7 delle seste si
parsano già. L'unica aggiunta di codice: due scale in `song.MODI` (come fecero
ottatonica/esatonale) — nessun test fissa l'insieme MODI, il modale cicla su una
lista hardcoded. Il resto è documentazione + quattro guardiani `[CALC]`.

## Cosa resta fuori (e va detto)

- il **ritmo armonico** (in tutte le istruzioni d'armonia);
- gli **altri modi della minore melodica** (servono le due che colorano la
  dominante, non tutti e sette);
- il **voicing** delle tensioni e delle seste (upper structure, quinte parallele
  della tedesca): è **priorità 2 (forma)**;
- con questo l'**armonia funzionale + tensione + cromatismo + modale + prestito +
  scale** è coperta: il prossimo passo esce dalla priorità 1.

## Cosa NON rifare

- **non forzare una citazione** per l'alterata / lidia dominante: i libri non le
  nominano, `[CALC]` + contesto;
- **non chiamarle «modi del maggiore»**: sono modi della minore melodica, in
  `MODI` come intervalli;
- **niente esempio all'ascolto**: stesso metodo della spina.
