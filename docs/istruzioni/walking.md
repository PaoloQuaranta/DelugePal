# Scrivere una linea di walking — feel SWING

⚠️ **PERIMETRO, e va letto prima di tutto.** Questa istruzione copre **un
feel solo**: lo swing con basso in walking, cioè l'idioma bebop/hardbop, grosso
modo 1945-1965. **Non è «il basso nel jazz».**

Nel jazz il basso fa anche altro, e la casella 1 di `docs/repertori/jazz.md`
lo misura: il **tradizionale è al 100% in due** (1 e 3, non quattro note), il
**fusion è al 100% funk**, e il **latin** compare dentro cool, hardbop e
postbop. Il feel si dichiara **prima** di scrivere una nota, e può cambiare da
una sezione all'altra.

⚠️ E i numeri misurati qui sotto vengono dal Jazz Trio Database, che è **un
corpus di walking**: su 1099 esecuzioni solo il 4,2% sta sotto le tre note per
battuta. Descrivono questo feel, non il jazz.

---

**A cosa serve.** Hai un giro di accordi e ti serve il basso sotto. Questa
istruzione dice come costruire la linea, nota per nota, e quanto scostarsi
dalle quattro note per battuta.

**Cosa ti serve prima di cominciare:**

- il giro, una sigla per battuta (o due, se l'armonia cambia a metà);
- il registro del basso: **mi1-do3** (numeri di nota MIDI 28-48);
- da dove parte la linea, cioè l'ultima nota suonata prima.

---

## Il grado di prova, e come si legge

Ogni riga di questo documento porta scritto da dove viene.

| | |
|---|---|
| `[LIB]` | letteratura didattica, con libro e capitolo |
| `[MIS]` | misurato su un corpus, con quale e quante esecuzioni |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ `[LIB]` **non è più forte di `[MIS]`, è diverso.** Il libro dice *come si
fa*, il corpus dice *cosa fanno davvero i dischi*. Quando si contraddicono, va
scritto qui invece di scegliere in silenzio.

---

## La procedura

`[LIB]` *Jazz Theory Justified*, cap. IV «Developing a Bass Line», pp. 27-28.

### Passo 1 — lo scheletro: le fondamentali

Metti la **fondamentale** di ogni accordo sul movimento dove l'accordo entra.
Con un accordo per battuta è il movimento 1; con due, i movimenti 1 e 3.

Scegli l'ottava in modo che **l'intervallo fra una fondamentale e la
successiva sia il più piccolo possibile**: una quarta su invece di una quinta
giù, una terza giù invece di una sesta su.

Questo passo è già codice: `genera_jazz._vicino(classe, riferimento)` dà la
nota di quella classe più vicina a dove sei arrivato, dentro il registro.

### Passo 2 — riempire, guardando l'intervallo

Cosa metti fra due fondamentali dipende **dalla distanza fra loro**. Non è una
tabella di forme: è una risposta a quello che è appena successo.

| distanza fra le due fondamentali | cosa ci metti |
|---|---|
| **terza** | una nota di passaggio **diatonica** in mezzo |
| **quarta o quinta** | una nota **del primo accordo** |
| **seconda** | **ripeti** la nota; oppure un **salto d'ottava** |
| **l'accordo dura tutta la battuta** | scendi **per grado dalla fondamentale alla quinta** |

Il salto d'ottava non è un abbellimento: serve a **riposizionarsi** quando la
linea sta arrivando in cima o in fondo al registro.

### Passo 3 — ammorbidire

Guarda la linea che è venuta fuori e cerca i punti dove scorre male. Puoi
usare la **terza, la quinta o la settima** dell'accordo, oppure note estranee.

Una linea per grado può proseguire *dentro* la battuta successiva: la
fondamentale del nuovo accordo può cadere sul **movimento 2** invece che sull'1.
Il libro lo dice esplicitamente: va benissimo.

### Cosa il libro dichiara di non dare

> «Questo metodo difficilmente produrrà una linea col fuoco e la spinta di un
> Ray Brown o di un Charles Mingus, ma un bassista competente saprà farla
> swingare e sosterrà adeguatamente l'armonia del pezzo.»

Tienilo presente: la procedura dà una linea **corretta**, non una linea
**bella**. Il resto è mestiere, e questa istruzione non lo contiene ancora.

---

## Quanto scostarsi dalle quattro note

La procedura del libro produce quattro note per battuta, sempre. I dischi non
fanno così.

`[MIS]` Jazz Trio Database, 319 esecuzioni scelte fra 1099, 65 bassisti,
34 048 battute. I numeri per esteso stanno nella casella 5 di
`docs/repertori/jazz.md`.

### Quante note ha una battuta

| note | quota |
|---|---|
| 1-2 | 2,0% |
| 3 | 15,6% |
| **4** | **48,7%** |
| 5 | 25,5% |
| 6 | 6,5% |
| 7 o più | 1,7% |

Circa **metà** delle battute non ne ha quattro. Media 4,24, deviazione 0,94.

⚠️ **Questi numeri sono un limite, non un motore.** Non sorteggiare quante
note fare: decidi tu, musicalmente, e usa la tabella per accorgerti se stai
esagerando in un senso o nell'altro. Il generatore di questo progetto ha
tirato i dadi con questa tabella per tre settimane e il risultato è stato
respinto tre volte.

### Far respirare la linea: lasciar cadere un movimento

Tieni la nota precedente invece di attaccare. Nei dischi succede sul
**15,0%** dei movimenti, e più spesso sul **2** e sul **4** che sull'1 e sul 3
(18,5% e 17,4% contro 16,0% e 15,0%).

`[DEC]` Il corpus porta **onset**, non note: «nessun attacco» potrebbe essere
un silenzio o una nota tenuta, e il dato non li distingue. Qui si tiene la
nota, perché è quello che fa un contrabbassista che salta un movimento — la
corda continua a suonare — e un buco vero suona come una linea rotta.

### Aggiungere una nota: la croma

Quando servono più di quattro note, aggiungi una croma. Cade a **0,65 del
movimento** — mediana su 144 838 onset fuori dai beat, `[MIS]` — che è dove il
Deluge mette una croma scritta dritta con `SWING = 64` (0,64). Quindi la
scrivi dritta e il firmware la mette al posto giusto.

⚠️ Il numero è una mediana su una distribuzione **larghissima**: i quartili
stanno fra 0,41 e 0,76. Le note fuori movimento di un bassista non sono una
cosa sola.

`[DEC]` Che altezza abbia la nota in più: il corpus non lo può dire, perché
JTD non porta le altezze del basso. Qui si usa l'**approccio cromatico alla
nota che viene** — un semitono sopra o sotto, quello più vicino a dove sei —
perché è lo stesso idioma del passo 2 applicato un livello più in giù.

---

## Come si scrive, materialmente

Tu decidi le note. Le primitive le mettono nel file senza sbagliare i conti.

```python
from delugexml import musica as MU

# (tick, altezza, durata) -- 96 tick = un movimento, 384 = una battuta
linea = [
    (0,   41, 96),    # fa2, movimento 1
    (96,  45, 96),    # la2
    (192, 48, 192),   # do3, tenuta due movimenti: qui la linea respira
    (384, 46, 96),    # sib2, battuta 2
]
note = MU.linea(linea, articolazione='staccato', velocity=78)
```

`MU.linea()` accetta anche i nomi (`'fa2'`, `'la#2'`) al posto dei numeri, e
`durata` può essere una figura (`'1/4'`, `'1/8'`).

Per sapere che nota di una certa classe sta più vicino a dove sei —
il passo 1 — usa `genera_jazz._vicino(classe, riferimento)`.

---

## Cosa NON fare

- **non sorteggiare.** Le tabelle qui sopra dicono quando una scelta esce dal
  seminato, non quale scelta prendere;
- **non mettere quattro note in ogni battuta.** È fuori dalla distribuzione,
  non «un po' meno vario»: il valore centrale copre metà dei casi;
- **non scegliere l'ottava a caso.** Il passo 1 dice di minimizzare
  l'intervallo, ed è la cosa che tiene insieme la linea;
- **non far cadere il movimento 1 della prima battuta**: «tieni la nota
  precedente» richiede che ce ne sia una.

---

## Cosa manca a questa istruzione

Va scritto, perché chi la legge sappia cosa non ci troverà:

- **quando** fare le cose. La linea cambia fra tema, assolo e ultimo giro, e
  qui non è detto;
- **la frase.** Domanda e risposta, gruppi di due e quattro battute;
- **la risposta agli altri.** Il basso e la batteria cadono insieme fuori
  griglia 1,60 volte più del caso (`[MIS]`), e qui non è usato;
- **il fuoco e la spinta**, che il libro stesso dichiara di non dare.
