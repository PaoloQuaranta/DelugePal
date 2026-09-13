# Le dominanti secondarie: tonicizzare senza modulare

**A cosa serve.** Hai una casa tonale che regge (vedi
[`armonia-funzionale.md`](armonia-funzionale.md)) e vuoi dare **spinta** a un
grado che non è la tonica — farlo sentire, per un attimo, come se fosse *lui* la
casa. Lo precedi con la **sua** dominante. È il modo con cui il tonale acquista
direzione e movimento senza cambiare tonalità.

È priorità 1 (armonia), la **seconda faccia della spina funzionale** dopo
`armonia-funzionale.md`, e costruisce su di essa.

⚠️ **Stesso confine casa/ospite del [prestito](armonia-prestito.md).** La
dominante secondaria è un ospite: tonicizza un grado e se ne va, la casa resta.
Se la tonalità nuova prende il comando, non hai tonicizzato: hai **modulato**,
che è un'altra cosa (`[LIB]` Piston, cap. 14 «Modulation», p. 222).

**Cosa ti serve prima di cominciare:** una casa tonale funzionante, e il grado a
cui vuoi dare spinta.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sulle note, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ **Niente `[OSS]`**: stessa scelta di metodo di `armonia-funzionale.md`
(l'armonia è regola precisa, la chiude il `[CALC]`).

---

## Il principio: ogni grado può avere la sua dominante

`[LIB]` Piston, *Harmony* (5ª ed.), cap. 16 «Secondary Dominants», p. 258, la
regola nella sua forma più netta:

> «**Qualunque grado della scala può essere preceduto dalla propria armonia di
> dominante senza indebolire la tonalità fondamentale.**»

E il nome dice la funzione, p. 258: gli accordi tonicizzati si chiamano *secondary
tonics*, *«la funzione stessa è dunque una di tonicizzazione»*. ⚠️ E non è una
minaccia alla casa — è un rinforzo: `[LIB]` Piston p. 258, *«lungi
dall'indebolire la tonalità, le dominanti secondarie possono essere un mezzo per
rafforzarla»* (se sottodominante e dominante sono a loro volta sostenute dalle
proprie dominanti, l'edificio tonale è irrobustito).

`[LIB]` Smith, *Jazz Theory* (4ª ed.), cap. VIII, p. 57, lo dice come **giustifica­
zione** del moto debole→forte: *«una dominante secondaria che "tonicizza"
l'accordo forte che segue»*; e apre la sezione «Secondary Functions and
Tonicization» a p. 65.

---

## Il vocabolario

### Le cinque dominanti secondarie diatoniche

`[CALC]` La dominante secondaria di un grado è un **accordo di settima di
dominante** (la 3ª maggiore + la 7ª minore, quindi il tritone) costruito una
**quinta giusta sopra** quel grado. In Do:

| tonicizza | grado | la sua dominante | in Do |
|---|---|---|---|
| il ii (Re m) | V7/ii | La7 | `A7 → Dm7` |
| il iii (Mi m) | V7/iii | Si7 | `B7 → Em7` |
| il IV (Fa) | V7/IV | Do7 | `C7 → Fmaj7` |
| il V (Sol) | V7/V | Re7 | `D7 → G7` |
| il vi (La m) | V7/vi | Mi7 | `E7 → Am7` |

⚠️ **Non si tonicizza il vii°** (il grado diminuito, Si dim in Do): un accordo
diminuito non è una tonica stabile su cui posarsi. `[LIB]` Piston elenca le
dominanti secondarie proprio come V of II … V of VI (cap. 16, p. 257), e il vii°
resta fuori.

### Il ii-V interpolato

Il jazz raramente mette la dominante secondaria da sola: le premette il **suo
ii**, ricreando un ii-V intero prima del bersaglio. Per tonicizzare Re m non solo
`A7 | Dm7` ma `Em7b5 | A7 | Dm7` — il ii-V di Re minore. `[LIB]` Smith cap. VIII
(«Secondary Functions and Tonicization», p. 65): è così che si estende la
tonicizzazione, ed è il motore dei giri di standard.

### Il ciclo delle quinte

`[CALC]` Incatenando le dominanti secondarie — **ognuna è la dominante della
successiva** — si ottiene il giro più forte del tonale: `E7 | A7 | D7 | G7 | C`.
`[LIB]` Piston p. 258: nella sua forma più estesa il principio *«produce uno
schema armonico sequenziale in cui ogni accordo diventa la dominante del
successivo»*. Ogni fondamentale sta una quinta sopra quella dopo.

### Il rimando: il tritone sub

La dominante secondaria si può sostituire col suo **♭II7** (il tritone sub): al
posto di `A7 → Dm7`, `Eb7 → Dm7`. Non si ripete qui — vive in
[`accordi-di-passaggio.md`](accordi-di-passaggio.md), che è la faccia cromatica e
funzionale della stessa mossa.

---

## Come si stabilisce

1. **parti da una casa funzionante** (`armonia-funzionale.md`);
2. **scegli il grado** a cui dare spinta — di solito il V (con `D7 → G7`) o il ii;
3. **mettici davanti la sua dominante** (una quinta sopra), o il ii-V intero se
   vuoi la spinta piena;
4. **risolvi sul bersaglio**, e **torna a casa**: la tonicizzazione è un ospite,
   non una nuova residenza.

---

## Come si scrive, materialmente

Le dominanti secondarie sono semplici accordi `7` su fondamentali fuori scala:
`MU.armonia` le calcola dalla sigla, la casa in `set_scale` non le filtra.

```python
from delugexml import song as S, musica as MU

S.set_scale(doc, 'C', 'maggiore')
note = MU.armonia('Cmaj7 | A7 | Dm7 | G7 | Cmaj7', registro='do3', durata='1/1')
#                    I     V7/ii  ii    V    I   -- A7 tonicizza il ii
```

---

## Cosa NON fare

- **non tonicizzare il vii°** diminuito: non è una tonica su cui posarsi;
- **non incatenarne troppe senza tornare a casa.** Come il prestito: un colore
  alla volta si sente come colore; una catena lunga si sente come modulazione;
- **non confondere tonicizzazione e modulazione.** La dominante secondaria colora
  un grado e rientra; se la casa nuova si insedia, hai cambiato tonalità.

---

## Cosa manca a questa istruzione

- **il tritone sub** come sostituto della V7/x — è in `accordi-di-passaggio.md`,
  qui solo rimandato;
- la **dominante alterata** — quando la V7/x porta ♭9, ♯9, ♯5, alt (la scala
  alterata / lidia dominante dal minore melodico, l'uso funzionale di ottatonica
  ed esatonale): la tensione della dominante è il passo dopo la spina;
- il **ritmo armonico** — quanto dura la tonicizzazione prima di risolvere — resta
  scelta del pezzo.
