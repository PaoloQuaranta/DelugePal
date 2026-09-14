# Aggancio: il basso che va incontro alla batteria

**A cosa serve.** Far sì che basso e batteria si **incontrino** nel tempo invece
di stare ognuno per sé. In un trio jazz i loro eventi fuori griglia **coincidono
1,60× più del caso** (`[MIS]`, misura 3 della casella 5): non è una questione di
densità — quella non si segue (correlazione +0,058) — ma di **collocazione**. Il
difetto d'origine: il basso del generatore era **quantizzato esatto, dispersione
zero**, e un basso senza microtiming **non può andare incontro** a una batteria
che ce l'ha (il [groove template](groove-template.md)).

È priorità 3 (ritmo). L'aggancio come *flag* (`genera_jazz.py --aggancio`)
esisteva già ma **non riproduceva la misura** — vedi «cosa non riproduce».
Questa istruzione parte da sotto: **dare al basso il microtiming che gli manca**.

**Cosa ti serve prima di cominciare:** un walking scritto, la batteria col
groove template, e un'**esecuzione di basso nominata** (dal Jazz Trio Database).

---

## Il grado di prova

| | |
|---|---|
| `[MIS]` | misurato su un corpus |
| `[OSS]` | osservato — all'ascolto, o su un'esecuzione nominata |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ **Ritmo, quindi l'ascolto pieno.** Il `[CALC]` dice che il basso è uscito
dalla griglia; l'orecchio dice se **respira** con la batteria invece di suonare
come un metronomo.

---

## Dove sta la vita: la dispersione, non il lay-back

`[MIS]` La misura 4 dà lo scarto di ciascuno rispetto al beat: **basso +2,3 ms**
(dispersione 6,4), batteria **−0,4 ms**, piano +15,3. È una **relazione** — come
si sta insieme — non una superficie.

⚠️ **Ma il lay-back mediano è minuscolo** (+2,3 ms ≈ mezzo tick a 125 BPM): se si
riproducesse solo quello, sarebbe sottile come il residuo di posizione della
batteria (§6-terdecies). **La vita sta nella dispersione** — misurata su trii
nominati, il basso ha **~3-4 tick di float nota per nota**, più della batteria.
È il float che distingue un basso *suonato* da uno *sequenziato*, e un basso
quantizzato ha dispersione **zero**: è quello il difetto.

---

## Da dove viene il float: UNA esecuzione nominata

`[DEC]` `jtd.microtiming(z, fname, 'bass')` dà la **sequenza** delle deviazioni
di un basso vero — nota per nota, di quanto arriva prima o dopo il beat.

⚠️ **È `[OSS]` su quell'esecuzione, non `[MIS]` su un repertorio**: mediare il
microtiming di bassisti diversi lo tira **verso zero**, la stessa ragione per cui
il groove template della batteria viene da un'esecuzione sola. E **non è una
distribuzione**: è la sequenza *reale*, posata in ordine. Sfruttare una
distribuzione darebbe rumore bianco; un bassista vero ha un *andamento*.

---

## Come si applica, materialmente

`MU.applica_microtiming(note, scarti_tick)` posa la sequenza sul walking, **in
ordine di tempo** (la nota più presto prende il primo scarto), ciclando se le
note sono più della sequenza.

```python
from delugexml import jtd as JT, musica as MU

sec = JT.microtiming(z, 'barronk-bemshaswing-...', 'bass')   # deviazioni, secondi
tick = [round(s * 96 * BPM / 60) for s in sec]               # al tempo del pezzo
MU.applica_microtiming(flat_bass, tick)                      # ⚠️ MUTA in posto
```

⚠️ **La conversione è in tick al tempo del pezzo:** un float è una manciata di
millisecondi, e `applica_microtiming` vuole i tick. `flat_bass` è la lista di
`Note` in ordine (le voci di `MU.linea()` appiattite): muta le stesse `Note`, che
restano nel dict per `MU.scrivi()`.

⚠️ **Non confondere tre cose:** il **float** è il microtiming di *una linea* (qui);
lo **swing** è di *song* (`set_swing`); il **groove template** è della *batteria,
per passo* (`applica_groove`). Sono tre strati diversi.

---

## Cosa NON riproduce, e va detto

⚠️ **Questo NON riproduce la misura 3 (coincidenza 1,60×).** Due ragioni,
entrambe reali (casella 5, 6 settembre 2026):

- sul generatore basso e batteria stanno sulla **stessa griglia a sedicesimi**,
  quindi la coincidenza è **tutto-o-niente** (o condividono il passo o distano
  ≥117 ms) mentre nel corpus è continua — 1,60× è un **numero di corpus**, non
  qualcosa che un singolo pezzo dimostra;
- la coincidenza *vera* vorrebbe basso **e** batteria dallo **stesso trio**,
  mentre qui il float viene da un basso JTD e il template da un batterista del
  Groove MIDI: due dischi diversi.

Quello che si sente qui è più semplice e vero lo stesso: **un basso che respira
contro uno che è un metronomo.** La coincidenza piena resta in «cosa manca».

---

## Esempio lavorato: lo stesso walking, due volte

In [`tools/aggancio_scritto.py`](../../tools/aggancio_scritto.py): lo **stesso**
walking, sotto la **stessa** batteria (groove template di `drummer1/session1/49`
+ rimappa), due passate —

| passata | il basso |
|---|---|
| 1 | **quantizzato** — sulla griglia esatta, dispersione 0 (il difetto) |
| 2 | **col float** di **Rufus Reid** («Bemsha Swing», 1984), nota per nota |

Il float, in tick a 125 BPM: `[2, −2, 2, 0, 4, −2, 0, 2, 2, 2, 6, 6, 6, 6, 0, 0]`
— mediana **+2**, dispersione **2,7**, da −2 a +6: per lo più dietro, ma con vera
variazione (qualche anticipo, qualche lay-back). `[CALC]` La passata 1 ha
**0 note su 16** fuori griglia, la 2 ne ha **12**. Il pezzo è `out/AGGANCIO01.XML`
(BPM 125, swing 60 di song), caricato come `/SONGS/DelugePal/AGGANCIO01.XML`,
riletto byte per byte.

⚠️ **Verdetto `[OSS]`, 14 settembre 2026: «ok funziona, è quasi impercettibile
ma va bene».** Il float si sente come un basso meno rigido, ma è un effetto
**piccolo** — qualche tick, come previsto: il microtiming del basso è sottile
(la vita era nella dispersione, e la dispersione qui è ~3 tick). È la stessa
lezione della posizione nella batteria (§6-terdecies): la velocity si sente, il
tempo no, o quasi. **Vale la pena solo dentro il pieno**, non come effetto da
mostrare da solo.

---

## Cosa NON fare

- **non mediare più bassisti** in un float: tira il microtiming verso la griglia;
- **non lasciare il basso quantizzato esatto**: è il difetto d'origine —
  dispersione zero, non può incontrare nessuno;
- **non aspettarsi 1,60× dal generatore**: è un numero di corpus, e la griglia a
  sedicesimi lo rende tutto-o-niente;
- **non confondere il float con lo swing o col groove template**: sono tre strati
  diversi, e sommarli male li applica due volte.

---

## Cosa manca a questa istruzione

- la **coincidenza vera** — basso **e** batteria dallo **stesso** trio JTD, così
  che la misura 3 diventi spendibile e non solo evocata;
- l'**aggancio come flag** (`--aggancio`, il secondo sorteggio della batteria):
  va rivisto o buttato alla luce di questo — il blocco non era lì;
- il **float fuori dal jazz** (altri strumenti, altri generi): su domanda.
