# Il fill — progetto

**Data:** 14 settembre 2026
**Cos'è:** l'inizio della **priorità 3 (ritmo)**, dal fill. ⚠️ **Scelta
dell'utente:** «passa al ritmo, tratteremo i fill all'interno di quello». Il fill è
la **faccia ritmica delle transizioni** — la battuta in cui la batteria annuncia la
sezione nuova — e chiude la lacuna dichiarata di `batteria-jazz.md` («il fill: dove
va, quanto dura. Oggi è una decisione arbitraria messa sul turnaround») e la
battuta «(fill)» vuota di `batteria_scritta.py`.

## Il metodo — ritmo, quindi l'ascolto pieno

Ma il fill è **molto misurato**: `[MIS]`/`[CALC]` per la firma, l'ascolto per il
feel. L'agente arriva a «pronto da caricare»; l'ascolto è dell'utente. ⚠️ **Al 14
settembre l'ascolto è ancora pendente:** serve una traccia di batteria coi tom nel
pezzo (i kit in `refs/kits/` sono elettronici) e il dispositivo collegato.

## Il principio: dove lo dice la forma, cosa lo dice il corpus

⚠️ La casella 9 dice netto: **«dove va un fill non lo dice il corpus»** — il
dataset consegna i fill staccati da ogni pezzo. **Ma ora la forma c'è** (priorità
2): il fill va al **giunto** (l'ultima battuta di una sezione, sul turnaround). È
la convergenza — il **dove** dalla forma, il **cosa** dal corpus.

## La firma misurata (`[MIS]` casella 9, 51 fill jazz)

⚠️ **Due batteristi** (drummer1 44, drummer7 7): `[MIS]` con la cautela, descrive
quei due. Dura **una battuta** (0,93). **~1,2× più fitto** (15,7 vs 12,9), non il
doppio. ⚠️ **La firma NON è la densità: è che il ride si ferma (20% → 3%) e
arrivano i tom (10% → 29%).** E **non alza la voce** (stessa velocity o meno): un
cambio di strumento, non un crescendo.

## Il meccanismo — `MU.controlla_fill` (codice nuovo)

⚠️ **Un CHECKER, non un generatore.** Prende `beat` e `fill` (`ruolo -> [Note]`) e
fa i conti sulla firma: segnala se il ride non si ferma (quota > 10%), se i tom non
arrivano (< 15%), se è troppo fitto (> 1,5×), se è un crescendo (più forte del
beat). È il ruolo del corpus nel progetto — «prendere gli errori» — come
`contrappunto` per le due linee. `racconta_fill` lo dice a parole (ASCII, console
cp1252). Nuovi: `Fill`, `_ruolo_batteria` (riconosce il ruolo dal nome del drum).

`[CALC]` — `test_controlla_fill`: un fill con la firma non ha problemi; il ride
acceso, i tom assenti, il raddoppio dei colpi e il crescendo sono ognuno segnalato.

## Il meccanismo del DOVE — `MU.variazione` (già fatto)

Il fill si posa al giunto con la clip **bianca** (`MU.variazione`, dalle
[transizioni](2026-09-14-transizioni-design.md)): sostituisce l'ultima battuta di
una sezione senza toccare le altre. Il fill è la faccia ritmica di quel
meccanismo, non un meccanismo nuovo.

## L'esempio lavorato

`tools/fill_scritto.py`: scrive le battute **12 e 24** del blues di
`batteria_scritta.py` (i turnaround, marcati «(fill)» e vuoti) con la firma — ride
che si ferma, tom che scendono, ~1,2×, non più forte — e passa `controlla_fill`
senza problemi (`test_fill_scritto`). ⚠️ L'ascolto (build su un kit coi tom + il
dispositivo) è il passo che manca.

## Struttura / rimandi

- `docs/istruzioni/fill.md` (nuovo); `MU.controlla_fill` + `MU.racconta_fill` in
  `musica.py`; `test_controlla_fill` + `test_fill_scritto`; `tools/fill_scritto.py`;
- rimandi: `batteria-jazz.md` (il groove), `transizioni.md` (la clip bianca, il
  giunto), casella 9 di `jazz.md` (la firma misurata).

## Cosa resta fuori

- l'**ascolto** (build su un kit acustico coi tom): il passo che chiude la priorità
  3 per il fill;
- **quanto spesso** va un fill (il corpus non lo dice; la forma decide);
- il **mezzo fill**, il **pickup di batteria** su un movimento;
- i fill **non-jazz** (tom roll dell'EDM, crash-and-stop): un'altra firma, su
  domanda;
- il resto della priorità 3 (basso e batteria che reagiscono alla forma oltre il
  fill; i groove template applicati; gli altri feel).

## Cosa NON rifare

- **non far generare il fill al codice**: `controlla_fill` prende gli errori, non
  scrive il fill (il corpus dà relazioni, non superfici);
- **non firmare la firma col nome del genere senza la cautela**: 2 batteristi,
  descrive quei due;
- **non fare del fill un fuoco d'artificio**: è un cambio di strumento a volume
  uguale, non un crescendo denso.
