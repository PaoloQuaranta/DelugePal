# Il voicing: come disporre le note di un accordo

**A cosa serve.** Hai gli accordi (l'armonia è decisa) e devi decidere **come
suonarli** — quali note, in che registro, quante. Lo stesso `Cmaj7` può essere un
blocco caldo di quattro note vicine o due note nude e ariose: cambia il **colore,
il peso, il ruolo**, non l'armonia. Questa istruzione dice quale voicing scegliere.

È priorità 2 (forma), la prima faccia. Il codice fa già i cinque voicing
(`MU.voci`) e conduce le parti (`voci_condotte`); qui c'è la **scelta**.

**Cosa ti serve prima di cominciare:** gli accordi (le sigle), l'organico (chi
suona: c'è un basso? è un solo?) e il registro.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sulle note, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

⚠️ **Qui torna l'`[OSS]`, ed è una scelta di metodo — 13 settembre 2026.** A
differenza dell'armonia (che si chiude col solo `[CALC]`), il voicing ha una parte
d'orecchio: le **meccaniche** sono precise e testate, ma **quale** voicing suona
giusto è un giudizio — PERCHE l'ha già mostrato (il quartale «corretto» scartato
perché toglieva corpo). Quindi `[LIB]` + `[CALC]` per le meccaniche, e un esempio
lavorato **ascoltato** per la scelta.

---

## Il principio: non c'è un voicing giusto in assoluto

`[LIB]` Smith, *Jazz Theory* (4ª ed.), cap. VI «Chord Voicings», p. 35:

> «"Voicing" si riferisce al modo in cui le note dell'accordo vengono disposte.
> Ci sono molti approcci diversi. La scelta di quale usare dipende in parte dal
> **tipo di organico** — solo keyboard, trio, big band, ensemble vocale — ed è
> influenzata dalle **preferenze estetiche** dell'esecutore, del compositore o
> dell'arrangiatore.»

È la frontiera che separa questa istruzione dall'armonia: là c'era un fatto (le
note dell'accordo); qui c'è una **scelta**, e la scelta si giudica anche
all'orecchio.

⚠️ **La fonte profonda del voicing jazz è Levine, *The Jazz Piano Book*** (arrivato
il 13 settembre 2026): un intero libro dove Smith ha un capitolo. Ogni voicing di
sotto ha lì un capitolo suo — le shell in cap. 3 «Three-Note Voicings», il
rootless in cap. 7-8 «Left-Hand Voicings», il quartale in cap. 13 «Fourth Chords»
e cap. 12 «So What Chords», e le **upper structure** (il livello dopo) in cap. 14.
Smith dà il principio e la panoramica; Levine il mestiere.

⚠️ **La condotta delle parti è ORTOGONALE al voicing.** `voci_condotte` decide
*dove* (in che ottava) posare le voci per muoverne meno da un accordo al
successivo; il voicing decide *quali* voci. `[CALC]` La condotta **non cambia le
classi di altezza** (verificato da `test_condotta_delle_parti`): si può condurre
qualunque voicing. Il voicing è la forma di un accordo, la condotta il legame fra
accordi.

---

## Il vocabolario: cinque voicing

`[CALC]` Le meccaniche sono blindate dai test `test_voicing_chiuso_e_drop2`,
`test_voicing_shell_e_senza_fondamentale`, `test_voicing_senza_fondamentale_estensioni`,
`test_voicing_senza_settima_e_rifiutato`, `test_voicing_quartale`.

| voicing | cos'è | quando serve | `[LIB]` |
|---|---|---|---|
| **chiuso** | tutte le note dell'accordo, dalla fondamentale in su | il default; **caldo**, il corpo delle triadi | Smith cap. VI |
| **shell** | solo **3ª e 7ª** (le due note d'identità) | tessitura fitta, duo, quando un basso copre la fondamentale; l'**alternanza 7-3** del comping | Smith p. 37; **Levine cap. 3** «Three-Note Voicings» |
| **senza-fondamentale** (Bill Evans) | **3-5-7-9**, la fondamentale la fa un altro | il comping al piano (serve un basso sotto): `[LIB]` Smith p. 38, *«usati dai pianisti dove un altro strumento fa le fondamentali»* | Smith p. 38; **Levine cap. 7-8** «Left-Hand Voicings» |
| **drop2** | posizione chiusa con la **2ª voce dall'alto giù di un'ottava** | **spalanca** la tessitura: big band, chitarra; le parti muovono in parallelo | Smith p. 46; **Levine cap. 19** «Block Chords» |
| **quartale** | tre **quarte** giuste + una terza | modale, **aperto** (il «So What chord»); ⚠️ toglie corpo | Smith p. 81; **Levine cap. 13** «Fourth Chords», cap. 12 «So What» |

⚠️ **Il metodo di Levine, che vale più delle etichette.** *The Jazz Piano Book*
costruisce il voicing jazz su **due mosse**, e conviene conoscerle:

- **le three-note voicings** (cap. 3) — 3ª e 7ª più una nota — sono la **base** di
  tutto il comping: le due note d'identità reggono l'accordo, il resto è colore.
  È lo **shell** di questa istruzione, visto come punto di partenza e non come
  ripiego;
- le **left-hand voicings** rootless (cap. 7-8) hanno **due forme, «A» e «B»**, che
  si **alternano** scendendo per quinte in un ii-V-I — è così che il comping
  «cammina» senza saltare. `MU.voci_condotte` ottiene lo stesso fine (muovere
  meno voci) per calcolo, non per le due forme fisse: vedi la sua docstring.

⚠️ **Due limiti che il codice fa rispettare** (`[CALC]`): il **quartale** gira
solo sul minore settima (lo stack di quarte vuole 3ª e 7ª minori); **shell** e
**senza-fondamentale** vogliono un accordo che abbia 3ª e 7ª — una triade non le
ha, e la libreria rifiuta invece di inventare.

---

## Come si sceglie

Quattro leve, dalle più decise alle più fini:

1. **organico:** c'è un **basso** che fa le fondamentali? Allora **rootless** o
   **shell** (la fondamentale è coperta, si liberano le mani per il colore). È un
   **solo** che deve reggere tutto? Allora **chiuso** o **drop2** (la fondamentale
   dev'esserci);
2. **registro:** in **acuto** il chiuso e il quartale si assottigliano bene; in
   **grave** il chiuso diventa fangoso — apri con **drop2** o alleggerisci con
   **shell**;
3. **tessitura:** se c'è già tanto movimento intorno, **shell** (poche note, non
   ingombra); se lo spazio è vuoto, **drop2** (riempie, ampio);
4. **colore:** **caldo/corposo** → chiuso, triadi; **aperto/sospeso** → quartale;
   **liscio in parallelo** → drop2; il **suono del pianista jazz** → rootless.

⚠️ **Il quartale non è un traguardo.** `[OSS]` Su PERCHE (armonia modale)
l'utente ha preferito le triadi: *«le quarte aprono ma tolgono corpo»*. È un
colore del vocabolario, non un «meglio». Si sceglie per quello che serve al pezzo.

---

## Come si scrive, materialmente

Il voicing è un argomento di `MU.voci` e `MU.armonia`:

```python
from delugexml import song as S, musica as MU

# lo stesso giro, tre pesi diversi:
chiuso  = MU.armonia('Dm7 | G7 | Cmaj7', voicing='chiuso', registro='do3')
evans   = MU.armonia('Dm7 | G7 | Cmaj7', voicing='senza-fondamentale',
                     registro='do3')   # serve un basso che faccia le fondamentali
spread  = MU.armonia('Dm7 | G7 | Cmaj7', voicing='drop2', registro='do3')
```

⚠️ Il **rootless** presume un basso sotto: da solo «manca» la fondamentale
apposta. Accoppialo a una traccia di basso sulle fondamentali.

---

## Esempio lavorato: lo stesso ii-V-I, tre voicing

`[OSS]` **Ascoltato il 13 settembre 2026**, caricato sul Deluge (`VOICING01`). Il
confronto: `Dm7 | G7 | Cmaj7` voicizzato in tre modi — **chiuso**,
**senza-fondamentale** (col basso che fa le fondamentali), **drop2** — sullo
**stesso materiale**, così la differenza all'orecchio è solo il voicing. In
[`tools/voicing_scritto.py`](../../tools/voicing_scritto.py). Rhodes per gli
accordi, basso sulle fondamentali (necessario per il rootless), niente melodia né
batteria: si ascolta il peso.

**Verdetto: «sono tutti e tre belli e funzionano; quale preferisco in assoluto
dipende dal contesto».** ⚠️ È la conferma all'orecchio del principio di Smith
p. 35 — **non c'è un voicing giusto in assoluto**: i tre reggono, e la differenza
è di peso e tessitura, non di qualità. Che è precisamente ciò che questa istruzione
insegna a maneggiare. Ed è passata al primo colpo, come l'armonia: il voicing è
terreno fermo quanto lei, purché la scelta resti una scelta e non una gara.

---

## Cosa NON fare

- **non confondere voicing e condotta:** sono ortogonali — il voicing è quali
  note, la condotta come si legano gli accordi (`voci_condotte`);
- **non usare il rootless senza un basso:** la fondamentale manca apposta, e senza
  qualcuno che la faccia l'accordo perde terra;
- **non prendere il quartale per un miglioramento:** è un colore, e su PERCHE ha
  perso contro le triadi;
- **non forzare shell o rootless su una triade:** senza 3ª+7ª non stanno in piedi,
  e la libreria li rifiuta.

---

## Cosa manca a questa istruzione

- il **comping** — i pattern **ritmici** dell'accompagnamento (poggia su questo
  voicing + [`ritmo-armonico.md`](ritmo-armonico.md)): la prossima faccia della
  forma;
- le **upper structure** e i **polichordi** — voicing avanzati (Levine, cap. 14
  «Upper Structures»): su domanda di un pezzo;
- il **contrappunto** e la **struttura** lunga: le altre facce della priorità 2.
