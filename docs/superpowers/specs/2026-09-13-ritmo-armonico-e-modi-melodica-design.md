# Il ritmo armonico e i modi della minore melodica — progetto

**Data:** 13 settembre 2026
**Cos'è:** le due ultime code dell'armonia, in un passo, **stesso metodo**
(`[LIB]` + `[CALC]`, niente ascolto): il **ritmo armonico** e **gli altri modi
della minore melodica** (i due dominanti erano già in `dominante-alterata`).

## Item A — `ritmo-armonico.md`

**A cosa serve.** Decidere ogni quanto cambia l'accordo e dove cade sul metro —
la cosa che tutte le istruzioni d'armonia lasciavano «alla scelta del caso».

**Contenuto:** la frequenza del cambio (leva principale); il peso del metro
(`[LIB]` Piston cap. 12 «Harmonic Rhythm», p. 189: la «tirannia della
stanghetta», lo stress agogico); il jazz (`[LIB]` Smith p. 53: l'alternanza
forte-debole del ii-V-I; p. 65: il ritmo armonico a minima); `[DEC]` accelerare
verso la cadenza.

**`[CALC]` — `test_ritmo_armonico`:** sul meccanismo, non sulle altezze — il
ritmo armonico si fissa con `durata` in `MU.armonia` (`pos = da + i·passo`); gli
attacchi distano `durata_in_tick(durata)`, e dimezzare `durata` raddoppia il
ritmo armonico. ⚠️ È il primo guardiano armonico sul **tempo** e non
sull'altezza: la regola «l'armonia si chiude col `[CALC]`» non impone che il
`[CALC]` sia sulle note.

## Item B — `modi-minore-melodica.md`

**A cosa serve.** Dare la scala giusta ad accordi fuori dal comune (`maj7♯5`,
`m7♭5`, `7♭13`, minore col ♭9): i sette modi della melodica, uno per accordo.

**Contenuto:** il quadro dei sette modi → sette accordi di casa. `[CALC]` I
quattro nuovi (dorico ♭2, lidio aumentato, misolidio ♭6, locrio ♮2) sono
rotazioni della melodica e ognuno contiene il suo accordo. I due dominanti
(alterata 7º, lidia dominante 4º) **rimandati** a `dominante-alterata.md`.

**`[LIB]`:** Piston cap. 4 «The Minor Mode», p. 43 per la scala melodica. ⚠️ Il
**sistema dei modi come chord-scale non è nominato** nei libri (Smith lo rifiuta,
p. 77-78; rimanda a Russell) → `[CALC]` + contesto, come l'alterata e le medianti.
Terza volta che la regola «non forzare la citazione» decide.

**`[CALC]` — `test_modi_minore_melodica`:** i quattro modi sono rotazioni della
melodica; lidio aumentato ⊇ maj7♯5, locrio ♮2 ⊇ m7♭5, misolidio ♭6 ⊇ 7+♭13,
dorico ♭2 ⊇ m7+♭9.

## Feasibility

Gli accordi (`maj7#5`, `m7b5`, `7b13`) si parsano già. Aggiunta di codice: quattro
scale in `song.MODI` (come ottatonica/esatonale/alterata) — nessun test fissa
l'insieme MODI. Il resto è documentazione + due guardiani `[CALC]`. Suite
**1282 → 1292**.

## Come si realizza

- rimandi incrociati: le «cosa manca» di funzionale, dominante-alterata, modale,
  prestito che dicevano «il ritmo armonico resta scelta del caso» ora puntano a
  `ritmo-armonico.md`; dominante-alterata rimanda a `modi-minore-melodica` per il
  quadro dei sette modi;
- `ritmo-armonico` avverte che `MU.armonia` usa un `durata` uniforme per chiamata:
  il ritmo armonico disuguale si compone a segmenti.

## Cosa resta fuori (e chiude l'armonia)

- il **voicing** degli accordi estesi, il ritmo armonico disuguale in una sola
  stringa: **priorità 2 (forma)** / comodità di libreria, non teoria;
- i **modi della minore armonica** (frigio dominante…): un altro sistema, su
  domanda di un pezzo;
- con questo la **priorità 1 (armonia) è chiusa, code comprese**: il prossimo
  passo è la forma.

## Cosa NON rifare

- **non forzare una citazione** per il sistema dei modi (come l'alterata);
- **non duplicare i due modi dominanti**: rimando a `dominante-alterata`;
- **niente esempio all'ascolto**: stesso metodo.
