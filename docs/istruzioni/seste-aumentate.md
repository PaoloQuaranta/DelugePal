# Le seste aumentate: il colore cromatico prima della dominante

**A cosa serve.** Vuoi un accordo che **spinge alla dominante** con una tinta
cromatica calda e teatrale — il colore romantico che «apre» un attimo prima della
cadenza. Le tre seste aumentate (italiana, tedesca, francese) fanno questo: un
intervallo di **sesta aumentata** che si allarga sulla dominante.

È priorità 1 (armonia), un colore dello **spettro ampio** — classico e
romantico, non jazz — che sta accanto alla napoletana (l'altro accordo cromatico
pre-cadenza, già in [`armonia-prestito.md`](armonia-prestito.md)).

⚠️ **È parente del tritone sub.** La sesta tedesca è **enarmonicamente un accordo
di settima di dominante** — la stessa mossa che il jazz chiama tritone sub (in
[`accordi-di-passaggio.md`](accordi-di-passaggio.md)), letta con la grafia
classica. Piston lo dice in un altro modo: nasce da «V di V con la quinta
abbassata».

**Cosa ti serve prima di cominciare:** una casa tonale (vedi
[`armonia-funzionale.md`](armonia-funzionale.md)) e il punto — prima della
dominante — dove vuoi la spinta.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sulle note, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ **Niente `[OSS]`**: l'armonia si chiude col `[CALC]` (decisione del 13
settembre 2026).

---

## Il principio: una sesta aumentata che si allarga sulla dominante

`[LIB]` Piston, *Harmony* (5ª ed.), cap. 27 «Augmented Sixth Chords», p. 419:

> «I quattro accordi del gruppo noto come accordi di sesta aumentata hanno in
> comune l'**intervallo di sesta aumentata** creato dal **sesto grado minore** e
> dal **quarto grado cromaticamente alzato**. [...] Il quarto grado alzato, come
> sensibile della dominante, è la chiave della funzione di dominante secondaria
> di tre dei quattro accordi. L'intervallo di sesta aumentata si **espande, nella
> sua risoluzione normale, all'ottava sulla dominante**.»

In Do, la sesta aumentata è fra **la♭ (♭6)** e **fa♯ (♯4)**: le due note si
allargano di un semitono ciascuna verso **sol** (la dominante), da versi opposti.
`[CALC]` È questo il fatto che le definisce: `la♭` e `fa♯` distano un semitono da
`sol`, uno sopra e uno sotto.

⚠️ `[LIB]` Piston p. 419: la sesta aumentata *«non viene da una sottodominante
con la fondamentale alzata, ma da **V di V con la quinta abbassata**»* — cioè da
una dominante secondaria alterata. È da qui che nasce la parentela col tritone
sub.

---

## Il vocabolario: le tre seste

`[LIB]` Piston p. 420: tutte hanno tre note in comune — il **♭6** (nel basso), il
**♯4**, e la **tonica**; le distingue la quarta voce. In Do (verso Sol):

| sesta | note (in Do) | la quarta voce |
|---|---|---|
| **italiana** | la♭, do, fa♯ | nessuna (solo le tre comuni) |
| **tedesca** | la♭, do, **mi♭**, fa♯ | il ♭3 (mi♭) |
| **francese** | la♭, do, **re**, fa♯ | il 2 (re) |

`[CALC]` **La tedesca è un dom7 travestito.** La♭–do–mi♭–fa♯ sono, enarmonica­
mente, La♭–do–mi♭–**sol♭**: cioè **La♭7**. È lo stesso accordo che il jazz usa
come **tritone sub** (♭II7) — qui risolve su Sol (la V di Do), là sostituisce una
dominante. Stessa sonorità, due grafie e due mestieri.

⚠️ **La tedesca ha un problema di condotta** che il classico conosce: risolvendo
dritta sulla dominante fa **quinte parallele** (le famose «quinte di Mozart»).
`[DEC]` Il rimedio classico è passare per un `I` in secondo rivolto (il
`I⁶⁴` cadenzale) prima del V. Qui basta saperlo; il voicing fine è priorità 2.

---

## Come si stabilisce

1. **parti da una casa** e arriva al punto prima della dominante;
2. **metti la sesta aumentata** — italiana (scarna), tedesca (piena, il dom7
   travestito), francese (con il 2, più acida);
3. **risolvi sulla dominante:** il ♭6 scende e il ♯4 sale, allargandosi su Sol;
   poi la dominante fa il suo lavoro (V→I).

---

## Come si scrive, materialmente

La tedesca si può scrivere come il suo enarmonico dom7 (la sigla si parsa già);
italiana e francese non hanno una sigla standard, si scrivono per note.

```python
from delugexml import song as S, musica as MU

S.set_scale(doc, 'C', 'maggiore')
# la tedesca come dom7 enarmonico (La♭7), che risolve su Sol:
note = MU.armonia('Cmaj7 | Ab7 | G7 | Cmaj7', registro='do3', durata='1/1')
#                    I     Ger6   V    I   -- Ab7 = la sesta tedesca di Do
```

⚠️ Scritta così è **grafia jazz** (La♭7); la grafia classica scriverebbe fa♯, non
sol♭. Sul Deluge, che pensa per altezze e non per grafia, è la stessa cosa.

---

## Cosa NON fare

- **non farla risolvere altrove che sulla dominante:** la sesta aumentata si
  allarga su Sol — è lì che va, è quello il suo mestiere;
- **non dimenticare le quinte parallele della tedesca:** passa per il I⁶⁴ se le
  vuoi evitare (o accettale come colore, come faceva Mozart);
- **non confonderla con la napoletana:** quella è il ♭II *maggiore* (colore
  frigio), questa è una sesta aumentata verso la V — due colori pre-cadenza
  diversi.

---

## Cosa manca a questa istruzione

- il **voicing** che evita (o sfrutta) le quinte parallele della tedesca: è
  priorità 2 (forma);
- le **risoluzioni irregolari** e la modulazione con la sesta aumentata (Piston
  cap. 27 le tratta): qui basta la risoluzione normale sulla dominante.
