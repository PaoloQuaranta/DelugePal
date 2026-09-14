# Reagire alla forma (basso e batteria) — progetto

**Data:** 14 settembre 2026
**Cos'è:** il cuore della **priorità 3 (ritmo)**, e la correzione del difetto
d'origine del progetto. ⚠️ **Scelta dell'utente:** «passa al basso e batteria che
reagiscono alla forma». Una parte ritmica non va applicata uguale su tutto il
pezzo: deve **reagire** — fare spazio dove la melodia è fitta, seguire l'arco verso
il culmine.

## Il difetto d'origine, misurato

Il verdetto dell'11 settembre che fece ripartire il progetto: la batteria «suona
**discontinua** rispetto a basso e piano... e non le puoi **applicare
acriticamente**». Due guasti: **uniforme** (il basso a 4,00 note per battuta,
deviazione **0,00**) e **scollegata** (varia ma senza c'entrare). Il
[walking](walking.md) aveva già tolto l'uniformità (deviazione 0,94); mancava il
**c'entrare** — la correlazione col resto.

## Il metodo — ritmo, quindi l'ascolto pieno

Il `[CALC]` misura *se* la parte reagisce; l'orecchio dice se **respira** col pezzo.

## Il meccanismo — `MU.reazione` (codice nuovo)

⚠️ **Un ANALIZZATORE, non un generatore.** L'AI scrive la parte, `reazione` fa i
conti sul rapporto con un riferimento (la melodia, il comping), battuta per
battuta:

- la **deviazione** della densità della parte: sotto ~0,75 è **piatta** =
  `uniforme` (applicata acriticamente);
- la **correlazione** (Pearson) col riferimento: negativa = `complementa` (cala
  dove il rif è fitto), positiva = `segue` (si addensa con lui, verso il culmine),
  vicino a zero con variazione = `scollegata` (discontinua).

I due guasti sono `uniforme` e `scollegata`; i due modi buoni `complementa` e
`segue`. È il ruolo del corpus nel progetto — «prendere gli errori» — come
`contrappunto` e `controlla_fill`. `racconta_reazione` a parole (ASCII, cp1252).

`[CALC]` — `test_reazione`: una parte piatta è `uniforme`, una che cala dove il
rif è fitto `complementa`, una con la stessa forma `segue`, una ortogonale
`scollegata`; il difetto d'origine (deviazione 0,00) è `uniforme`.

## Reagire a due scale (`[DEC]`)

1. **battuta** — complementare la melodia (call-and-response, micro);
2. **sezione** — seguire l'[arco](2026-09-14-arco-dinamico-design.md) (la densità
   sale al culmine e ricade, `[MIS]` casella 9, macro).

## L'esempio lavorato

`REAZIONE01`: la stessa melodia (densità `1 4 1 4`), due bassi — **uniforme**
(`4 4 4 4`, `uniforme`, deviazione 0,00, il difetto d'origine) e **reattivo**
(`4 1 4 1`, `complementa`, correlazione −1,00: cammina dove il tema tace, tiene
dove è fitto). In `tools/reazione_scritto.py`, si suona dall'arranger. ⚠️ Vale per
la batteria allo stesso modo (`batteria_scritta.py` lo fa già a mano). Pronto e
caricato; l'utente ascolta se il basso reattivo respira → `[OSS]`.

## Struttura / rimandi

- `docs/istruzioni/reazione.md` (nuovo); `MU.reazione` + `MU.racconta_reazione` in
  `musica.py` (con `Reazione`, `_densita_per_battuta`, `_pearson`);
  `test_reazione` + `test_reazione_scritto`; `tools/reazione_scritto.py`;
- rimandi: `walking.md` (ha tolto l'uniformità del basso), `arco-dinamico.md`
  (l'arco, la scala macro), `batteria-jazz.md` (la batteria reagisce già a mano),
  casella 9 di `jazz.md`.

## Cosa resta fuori

- la reazione a **più riferimenti insieme** (basso vs melodia **e** batteria);
- l'**interazione** vera (non solo densità: raccogliere un accento, seguire un
  fraseggio);
- i **groove template** sopra la parte reattiva (già scritti);
- il resto della priorità 3, su domanda.

## Cosa NON rifare

- **non far generare la parte al codice**: `reazione` misura, non compone (il
  corpus dà relazioni, non superfici);
- **non confondere le due scale**: complementa dentro la sezione, segue sull'arco;
- **non credere che reagire sia riempire**: spesso la reazione a una melodia fitta
  è **tacere**.
