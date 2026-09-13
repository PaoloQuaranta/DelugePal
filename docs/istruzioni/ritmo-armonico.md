# Il ritmo armonico: ogni quanto cambia l'accordo

**A cosa serve.** Hai una progressione e devi decidere **ogni quanto** cambia
l'accordo, e **dove** cade il cambio rispetto alla battuta. È il *ritmo armonico*
— la cosa che tutte le altre istruzioni d'armonia hanno finora lasciato «alla
scelta del caso». Qui c'è come si decide.

È priorità 1 (armonia), la coda che vale per **tutte** le istruzioni: modale,
funzionale, prestito, cromatismo. Non è un colore in più, è **come** i colori si
dispongono nel tempo.

**Cosa ti serve prima di cominciare:** la progressione (le sigle) e il tempo/metro
del pezzo.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sul meccanismo, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ **Niente `[OSS]`**: l'armonia si chiude col `[CALC]` (decisione del 13
settembre 2026). Qui il `[CALC]` è sul **meccanismo** — come `durata` fissa il
ritmo armonico — perché il ritmo armonico è una scelta di tempo, non un fatto di
altezze; il resto è `[LIB]` e `[DEC]`.

---

## Il principio: la frequenza del cambio, e il suo peso

`[LIB]` Piston, *Harmony* (5ª ed.), cap. 12 «Harmonic Rhythm», p. 189. Due idee
governano tutto:

- **la frequenza del cambio di fondamentale.** Cambiare accordo spesso spinge;
  cambiarlo di rado allarga. È la leva principale;
- **il peso del metro.** `[LIB]` Piston chiama «tirannia della stanghetta» la
  convenzione per cui il **primo movimento** della battuta è il più forte, gli
  altri via via più deboli. E lo **stress agogico**: un accordo che **dura di
  più** è percepito come più forte. Un cambio d'accordo sul battere pesa; sullo
  levare è una sincope.

⚠️ **La regola operativa che ne segue:** metti i cambi importanti — e la cadenza —
sul **battere**. Un accordo lungo su un tempo forte è un punto di riposo; un
accordo breve o fuori tempo tira in avanti.

---

## Il ritmo armonico nel jazz

`[LIB]` Smith, *Jazz Theory* (4ª ed.), cap. VIII, p. 53: *«gli accordi tendono a
disporsi in un'alternanza forte-debole, creando un senso di battere-levare dentro
il ritmo armonico»* — nel ii-V-I, I e II sono forti, V è debole. E il ritmo
armonico tipico dello standard è a **minima** (due accordi per battuta) o a
**semibreve** (uno): `[LIB]` Smith p. 65 fa costruire un giro «mantenendo un ritmo
armonico a minima».

⚠️ `[DEC]` **La mossa espressiva più comune: accelerare verso la cadenza.** Una
progressione può stare ferma (un accordo per battute intere) e poi **stringere**
sul ii-V-I — un accordo per movimento — proprio dove vuole risolvere. Il ritmo
armonico che accelera è di per sé una spinta verso casa.

---

## Come si decide

1. **scegli il passo di base** dal carattere: **lento** (un accordo per una o più
   battute) per il modale e l'ampio; **medio** (a minima) per lo standard;
   **veloce** (a movimento) per la spinta;
2. **allinea i cambi al metro:** i cambi importanti e la cadenza sul battere;
3. **varia dove serve:** stringi verso la cadenza, allarga sui punti di riposo. Un
   ritmo armonico uniforme per tutto il pezzo è raramente la scelta migliore —
   dice sempre la stessa cosa.

---

## Come si scrive, materialmente

`[CALC]` Sul Deluge il ritmo armonico si fissa con **`durata`** in `MU.armonia`:
ogni sigla dura `durata`, e la successiva parte subito dopo. `durata='1/1'` è un
accordo per battuta (semibreve), `'1/2'` due (minime), `'1/4'` quattro. Verificato
da `test_ritmo_armonico`: gli attacchi distano esattamente `durata`, e dimezzare
`durata` raddoppia il ritmo armonico.

```python
from delugexml import song as S, musica as MU

# ritmo armonico lento (modale/ampio): un accordo per battuta
lento = MU.armonia('Dm | Dm | Gm | Dm', durata='1/1', registro='do3')

# accelerare sul ii-V-I: una battuta ferma, poi due accordi nell'ultima
riposo = MU.armonia('Cmaj7', durata='1/1', da=0, registro='do3')
stretta = MU.armonia('Dm7 | G7', durata='1/2', da=MU.durata_in_tick('1/1'),
                     registro='do3')
```

⚠️ `MU.armonia` usa **un solo `durata` per chiamata**: per un ritmo armonico
**disuguale** (fermo, poi stretto) si compone a **segmenti** — più chiamate con
`durata` e `da` diversi, come sopra — e si uniscono. Non c'è (ancora) un modo di
dare durate diverse alle sigle di una stessa stringa.

---

## Cosa NON fare

- **non lasciare il ritmo armonico uniforme per default:** è la scelta che fa
  suonare «di servizio» una progressione giusta. Almeno stringi sulla cadenza;
- **non mettere la cadenza sul levare** senza volerlo: la risoluzione sul battere
  è ciò che la fa sentire come arrivo;
- **non confondere ritmo armonico e ritmo della parte:** qui si parla di ogni
  quanto cambia **l'accordo**, non di come si muovono le singole voci.

---

## Cosa manca a questa istruzione

- un modo di dare **durate disuguali** alle sigle di una sola stringa (oggi si fa
  a segmenti): è una comodità di libreria, non una lacuna di teoria;
- l'**anticipazione** dell'accordo (il cambio che arriva sul levare *prima* del
  battere, tipico del jazz e del pop): un colore ritmico-armonico che qui è solo
  nominato;
- il rapporto con la **forma** lunga (dove accelerare nell'arco di un intero
  pezzo): è priorità 2 (forma e densità).
