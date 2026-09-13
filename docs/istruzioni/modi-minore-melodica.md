# I modi della minore melodica: una scala per ogni accordo

**A cosa serve.** Hai un accordo un po' fuori dal comune — un `maj7♯5`, un
`m7♭5`, un `7♭13`, un minore col ♭9 — e vuoi la **scala giusta** per scriverci
sopra una melodia o un voicing esteso. La minore melodica ha **sette modi**, e
ognuno è la casa di uno di questi accordi. Questa istruzione li mette in fila.

È priorità 1 (armonia), la coda che chiude il vocabolario delle scale: dopo i
sette modi del maggiore ([`armonia-modale.md`](armonia-modale.md)) e le
simmetriche, i sette della melodica.

⚠️ **Due li conosci già:** l'**alterata** (7º modo) e la **lidia dominante** (4º
modo) stanno in [`dominante-alterata.md`](dominante-alterata.md) perché colorano
la **dominante**. Qui ci sono gli altri cinque, e il quadro d'insieme.

**Cosa ti serve prima di cominciare:** l'accordo (o il suo tipo) su cui vuoi la
scala.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sugli intervalli, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ **Niente `[OSS]`**: l'armonia si chiude col `[CALC]` (decisione del 13
settembre 2026).

`[LIB]` **La fonte è Levine, *The Jazz Piano Book*, cap. 9 «Scale Theory».**
Levine tratta la minore melodica proprio come un **sistema di modi-per-accordo**:
per ogni modo dice l'accordo di casa (il settimo modo = super-locrio per il
`7alt`, fig. 9-24; il modo sul VI grado per il mezzo-diminuito, ecc.). La **scala**
melodica sta anche in `[LIB]` Piston, *Harmony* 5ª ed., cap. 4 «The Minor Mode»,
p. 43 (*«nel minore si usano diversi tipi di triadi e scale»*).

⚠️ **Da tenere:** finché in casa c'era solo Smith — che **rifiuta** il multi-scala
(p. 77-78) — il sistema era `[CALC]` senza `[LIB]`. Levine (arrivato il 13
settembre 2026) è la fonte che lo nomina. Il `[CALC]` (rotazioni della melodica,
ognuna col suo accordo) resta il guardiano.

---

## Il principio: ruota la melodica, trovi sette colori

`[CALC]` La minore melodica (in `song.MODI`: `0 2 3 5 7 9 11` — minore col ♮6 e
♮7) ruotata su ognuno dei suoi sette gradi dà sette scale. Ognuna «contiene» un
accordo caratteristico, quello costruito sulle sue terze:

| grado | modo | in `MODI` | accordo di casa | il colore |
|---|---|---|---|---|
| 1 | minore melodica | `minore melodica` | **m(maj7)**, m6 | la tonica minore «jazz» |
| 2 | dorico ♭2 | `dorico b2` | **m7(♭9)** / sus♭9 | minore con la ♭9 frigia |
| 3 | lidio aumentato | `lidio aumentato` | **maj7♯5** | maggiore luminoso, sospeso |
| 4 | lidia dominante | `lidia dominante` | **7♯11** | dominante brillante (vedi dominante-alterata) |
| 5 | misolidio ♭6 | `misolidio b6` | **7♭13** | dominante che tira al **minore** |
| 6 | locrio ♮2 | `locrio nat2` | **m7♭5** | il semidiminuito, il ii del minore |
| 7 | alterata | `alterata` | **7alt** | la dominante tesissima (vedi dominante-alterata) |

`[CALC]` Verificato da `test_modi_minore_melodica`: i cinque modi non-dominanti
sono rotazioni della melodica, e ognuno contiene le note del suo accordo di casa
(il lidio aumentato il `maj7♯5`, il locrio ♮2 il `m7♭5`, il misolidio ♭6 il `7♭13`,
il dorico ♭2 il minore con la ♭9).

---

## I due che servono più spesso

⚠️ **Il locrio ♮2 sul `m7♭5`, e il misolidio ♭6 sul `7♭13`: sono il ii-V del
minore.** Nel ii-V-i minore (vedi [`armonia-funzionale.md`](armonia-funzionale.md))
il `iiø7` vuole il **locrio ♮2** e il `V7♭13` (o `V7alt`) vuole il **misolidio ♭6**
(o l'**alterata**). Sono la ragione pratica per cui questi modi esistono: danno
la scala per improvvisare o scrivere sopra la cadenza minore.

- il **lidio aumentato** è il colore del `maj7♯5` — un maggiore che «apre» verso
  l'alto senza risolvere;
- il **dorico ♭2** è un minore con la ♭9: il suono frigio-ma-con-la-sesta-alta,
  usato sui `sus♭9` e su certi accordi minori sospesi.

---

## Come si scrive, materialmente

Le scale sono in `song.MODI`: `set_scale` per scriverci una melodia dentro; gli
accordi (`maj7#5`, `m7b5`, `7b13`) si parsano già in `MU.armonia`.

```python
from delugexml import song as S, musica as MU

# una melodia nel locrio nat2 di Re, sopra il iiø7 di un ii-V-i in Do minore:
S.set_scale(doc, 'D', 'locrio nat2')
accordi = MU.armonia('Dm7b5 | G7alt | Cm', registro='do3', durata='1/1')
```

⚠️ **Non sono modi del maggiore:** stanno in `MODI` come intervalli, ma vengono
dalla minore melodica. Chiamarli «modi» va bene; chiamarli «del maggiore» no.

---

## Cosa NON fare

- **il sistema dei modi ha `[LIB]`** ora (Levine, cap. 9): non ripetere il vecchio
  «i libri non lo nominano», vero solo quando c'era solo Smith;
- **non usarli come colore statico che galleggia:** a differenza delle scale
  simmetriche, questi servono **sopra un accordo preciso** — il locrio ♮2 senza il
  suo `m7♭5` sotto è solo una scala;
- **non confondere il locrio ♮2 col locrio** del maggiore (che ha la ♭2): è il ♮2
  a renderlo la scala del semidiminuito.

---

## Cosa manca a questa istruzione

- il **voicing** degli accordi estesi che queste scale colorano (upper structure,
  quartale): è priorità 2 (forma);
- i **modi della minore armonica** (frigio dominante ecc.): un altro sistema, non
  chiesto dal perimetro finché non serve a un pezzo;
- l'**uso melodico** vero e proprio — quali note toccare e quali evitare dentro il
  modo — che è melodia (casella 8), non armonia.
