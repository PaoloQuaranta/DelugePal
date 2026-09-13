# Il voicing — progetto

**Data:** 13 settembre 2026
**Cos'è:** la prima faccia della **priorità 2 (forma)**: come disporre le note di
un accordo. Il codice (`MU.voci`) fa già cinque voicing e conduce le parti
(`voci_condotte`); manca l'**istruzione** che insegni *quale scegliere*.

## Il metodo, deciso il 13 settembre 2026

⚠️ **`[CALC]` + un ascolto.** Diverso dall'armonia pura (che si chiude col solo
`[CALC]`): le **meccaniche** dei voicing sono precise e testate, ma **quale**
voicing suona giusto è un giudizio d'orecchio — PERCHE l'ha dimostrato (il
quartale «corretto» scartato perché toglieva corpo). Quindi: `[LIB]` + `[CALC]`
per le meccaniche, e **un esempio lavorato di confronto** caricato sul Deluge che
**l'utente ascolta**; il verdetto `[OSS]` chiude la scelta. ⚠️ L'agente arriva
fino al «pronto da caricare»: l'ultimo passo è dell'utente.

## L'istruzione — `docs/istruzioni/voicing.md`

**Principio** (`[LIB]` Smith, *Jazz Theory* 4ª ed., cap. VI «Chord Voicings»,
p. 35): il voicing è come si dispongono le note; la scelta dipende dall'**organico**
(solo piano, trio, big band…) e dal **gusto** — non c'è un voicing giusto in
assoluto.

**Il vocabolario — cinque voicing** (meccanica `[CALC]`, già in `MU.voci` e già
testata; uso e fonte):

| voicing | cos'è | quando | `[LIB]` |
|---|---|---|---|
| chiuso | tutte le note dalla fondamentale su | default, caldo, il corpo | Smith cap. VI |
| shell | 3ª + 7ª (le note d'identità) | tessitura fitta, duo, basso che copre la fondamentale; l'alternanza 7-3 del comping | Smith p. 37 |
| senza-fondamentale (Bill Evans) | 3-5-7-9 | comping al piano, serve un basso sotto | Smith p. 38 |
| drop2 | chiuso, 2ª voce dall'alto giù d'ottava | tessitura spalancata, big band/chitarra, moto parallelo | Smith p. 46 |
| quartale | tre quarte + una terza | modale, aperto (So What); ⚠️ toglie corpo, non automaticamente meglio | Smith p. 81 |

**Come si sceglie:** organico (basso presente → rootless/shell; solo → chiuso/drop2),
registro (acuto → chiuso/quartale assottiglia; grave → evita il chiuso fangoso),
tessitura (fitta → shell; ampia → drop2), colore (caldo → triadi; aperto →
quartale; liscio → drop2). ⚠️ La **condotta** (`voci_condotte`) è **ortogonale**:
qualunque voicing si può condurre — il voicing è la forma di un accordo, la
condotta è come si legano gli accordi fra loro.

## `[CALC]`

I guardiani delle meccaniche **esistono già**: `test_voicing_chiuso_e_drop2`,
`test_voicing_shell_e_senza_fondamentale`, `test_voicing_senza_fondamentale_estensioni`,
`test_voicing_senza_settima_e_rifiutato`. L'istruzione li **richiama**, non li
riscrive. Aggiunta: un guardiano che lega l'affermazione centrale dell'istruzione
— la **condotta è ortogonale al voicing** (`voci_condotte` cambia le ottave/le
disposizioni ma non le classi di altezza rispetto a `voci`) — se non è già coperto.

## L'esempio lavorato (l'ascolto)

Un **confronto**: lo stesso `Dm7 | G7 | Cmaj7` voicizzato in tre modi — **chiuso**,
**senza-fondamentale** (col basso che fa la fondamentale), **drop2** — così
l'utente sente la differenza di peso e tessitura sullo stesso materiale.

- material script versionato: `tools/voicing_scritto.py` (le tre versioni, con la
  ragione accanto);
- assemblaggio + SysEx in **scratchpad** (dipende da `refs/`, non versionato):
  da `TEMPL0.XML`, tre tracce, `MU.armonia`, `write_file`, `dsysex put` **da
  PowerShell**;
- l'agente prepara e consegna il comando di load; **l'utente ascolta** e dà il
  verdetto, che chiude la sezione «esempio lavorato» dell'istruzione con `[OSS]`.

## Rimandi

- `armonia-modale.md` cita già il quartale (So What) → link a `voicing.md`;
- le istruzioni d'armonia che rimandano il voicing alla «priorità 2» → puntano qui;
- `voicing.md` rimanda a `ritmo-armonico.md` e alla condotta (`MU.armonia`).

## Cosa resta fuori (le prossime facce della forma)

- il **comping** (i pattern ritmici dell'accompagnamento): poggia su voicing +
  ritmo armonico;
- il **contrappunto** (linee indipendenti);
- la **struttura** (l'arco lungo, l'arranger);
- le **upper structure** / i polichordi: voicing avanzati, su domanda di un pezzo.

## Cosa NON rifare

- **non riscrivere i guardiani `[CALC]`** dei voicing: esistono, si richiamano;
- **non chiudere l'istruzione senza l'ascolto**: il metodo qui è `[CALC]` + un
  ascolto, non il solo `[CALC]` dell'armonia — la scelta del voicing è udibile;
- **non trattare condotta e voicing come la stessa cosa**: sono ortogonali.
