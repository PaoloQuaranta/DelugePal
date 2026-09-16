# Scrivere una linea di basso — feel BALLAD

⚠️ **PERIMETRO.** Questa istruzione copre **un feel solo**: il basso della ballad
jazz — un **2-feel** lento (due minime per battuta), con molto spazio. **Non
cammina** (se non al culmine). È l'opposto sia del walking (troppo fitto) sia del
funk (troppo sincopato): qui comanda lo **spazio**.

⚠️ **Il 2-feel è condiviso con il TWOBEAT** (priorità 3): stessa architettura —
fondamentale sul 1, quinta sul 3 — ma il twobeat è **veloce e saltellante**
(dixieland), la ballad è **lenta, morbida, con le spazzole**. Il feel si dichiara
prima, e cambia col tempo e col contesto.

---

**A cosa serve.** Hai un giro d'armonia lenta e ricca (una ballad vive sugli
accordi) e ti serve il basso sotto. Questa istruzione dice come tenere il fondo
senza affollarlo.

**Cosa ti serve prima di cominciare:**

- il giro, una sigla per battuta (o due, se cambia a metà);
- il registro del basso: **mi1-do3** (28-48), come il walking;
- il tempo: lento, **~50-70 BPM** (`[MIS]` Weimar, mediana 58).

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura didattica, con fonte |
| `[MIS]` | misurato su un corpus, con quale e quante esecuzioni |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ **Qui non c'è `[MIS]` sulla linea, ed è il punto debole — più ancora del funk.**
Nessun corpus in casa ha il basso della ballad: il **Jazz Trio Database** parte da
**102 BPM** (misurato: zero brani sotto), quindi non ha ballad; la **Weimar** dà
la linea **solista** (10 ballad, 7 sassofonisti, ~58 BPM), non il basso, e per di
più *«non ha coppie di crome misurabili»* — al tempo di ballad il solista non
tiene un pulse di crome, fa frasi rubate e fioriture in double-time. Quello che
segue è **letteratura e decisione**.

---

## Il 2-feel, il cuore

`[LIB]` PianoWithJonny / BassMusician Magazine, *Playing a "2 Feel"*: nella sua
forma fondamentale il 2-feel è **due minime per battuta — la fondamentale sul
movimento 1, la quinta sul movimento 3**. Crea **spazio** e una sensazione
calma. Per un principiante bastano le minime sulla fondamentale di ogni accordo.

```
mov:   1       2       3       4
       Fond.           Quinta
       (minima)        (minima)
```

Scegli l'ottava minimizzando l'intervallo fra una fondamentale e la successiva,
come nel walking (`genera_jazz._vicino`).

---

## Aggiungere spinta, senza affollare

`[LIB]` BassMusician: anche se il 2-feel poggia su un'architettura di minime, i
bassisti aggiungono valori più brevi per dare **momentum**. Il più semplice è la
figura **minima – semiminima – semiminima**:

```
mov:   1       2       3   4
       Fond.(minima)   Q.  (di passaggio verso la battuta dopo)
```

Cioè: tieni la fondamentale per due movimenti, poi due semiminime sul 3 e sul 4
che camminano verso la fondamentale successiva (una nota di passaggio diatonica
o cromatica). È un walking **in miniatura**, solo nella seconda metà della
battuta, e va usato **con parsimonia**: una battuta ogni tanto, non sempre.

---

## Aprire al culmine

`[LIB]` Nella forma della ballad il basso spesso **passa al walking** (quattro
note per battuta, `[walking.md](walking.md)`) o al **double-time** in un punto
di tensione — il ponte, l'ultimo A, o quando il solista raddoppia. È il
respiro grande della ballad: dallo spazio del 2-feel all'onda del walking, e
poi di nuovo giù. La forma lo decide (vedi [reazione.md](reazione.md)).

---

## Come si scrive, materialmente

```python
from delugexml import musica as MU
# 96 tick = un movimento, 384 = una battuta, 192 = una minima
# 2-feel: fondamentale sul 1, quinta sul 3 (F: fa1=29, do2=36)
linea = [
    (0,   29, 192),   # fa1  minima, movimento 1
    (192, 36, 192),   # do2  quinta, movimento 3
    (384, 26, 192),   # re1  battuta 2: nuova fondamentale
    (576, 33, 192),   # la1  quinta
]
note = MU.linea(linea, articolazione='legato', velocity=64)
```

⚠️ **Legato e piano.** Al contrario del funk (staccato, percussivo), il basso
della ballad è **tenuto e morbido** — le minime respirano, la velocity è bassa
(60-75). È lo spazio e il calore a fare il feel.

L'esempio lavorato è in `tools/ballad_scritto.py` (comping + basso in 2 +
spazzole, giro in Fa). ⚠️ **Verdetto dell'ascolto (16 settembre 2026):** *«va
bene»*.

---

## Cosa NON fare

- **non camminare per tutto il pezzo.** Quattro note fisse per battuta a tempo di
  ballad affolla e toglie il respiro — il walking è solo il culmine;
- **non affollare i movimenti.** Lo spazio del 2-feel **è** il feel;
- **non dimenticare la quinta sul 3.** È lei che dà al 2-feel il suo peso, contro
  il solo pedale di fondamentali;
- **non fare il basso staccato e brillante.** È soul/funk, non ballad: qui è
  tenuto, scuro, morbido;
- **non usare `set_swing` sul basso in minime.** Lo swing muove le crome; le
  minime non lo sentono. Serve alle spazzole ([batteria-ballad.md](batteria-ballad.md)).

---

## Cosa manca a questa istruzione

- **il `[MIS]`**: nessun corpus di ballad col basso trascritto. È il buco più
  grande, più del funk;
- **il rubato**: qui il basso è in tempo lento e stabile; il rubato vero (tempo
  che respira) non è rappresentabile sulla griglia a BPM fisso del Deluge, e
  resta al solista. Vedi [batteria-ballad.md](batteria-ballad.md), stessa nota;
- **il tono**: una ballad vuole un basso caldo e scuro (contrabbasso); qui si
  scurisce un preset con `MU.applica_verbo(..., 'piu scuro')`, non è la stessa cosa;
- **la frase** su più battute, il dialogo col solista rubato.
