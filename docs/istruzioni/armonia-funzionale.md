# Armonia funzionale: la casa che regge e risolve

**A cosa serve.** Vuoi una tonalità che si stabilisce, si allontana e **torna a
casa** — il respiro tonale su cui poggia lo standard e il jazz. Questa istruzione
dice come si costruisce quel giro: le tre funzioni, il **ii-V-I**, le cadenze, il
turnaround. È la **casa** che tutte le altre istruzioni d'armonia danno per
scontata (*«parti da un giro diatonico che regge»*) senza insegnarla.

È priorità 1 (armonia), ed è il centro di «jazz approfondito» del perimetro.

⚠️ **È l'orientamento opposto a [`armonia-modale.md`](armonia-modale.md).** Lì
l'armonia sta ferma e si evita ogni spinta funzionale; qui la spinta È il punto.
E prima di colorare con [prestito](armonia-prestito.md), [medianti](medianti-cromatiche.md)
o [accordi di passaggio](accordi-di-passaggio.md), la casa dev'essere questa.

**Cosa ti serve prima di cominciare:**

- la **tonalità** e il suo modo (Do maggiore, La minore);
- se hai una melodia, le sue note (la funzione va d'accordo con la voce in cima);
- il registro dove vuoi l'armonia.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sulle note, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ **Niente `[OSS]`, ed è una scelta di metodo — 13 settembre 2026.** L'armonia
è regola precisa: lo sviluppo armonico ha avuto un successo del 100% all'ascolto
(nessuna versione respinta in due giorni, contro le dieci della batteria). Quindi
questa istruzione **non porta un pezzo caricato sul Deluge**: la chiude il
`[CALC]`. La ragione per esteso sta nel design,
[`2026-09-13-armonia-funzionale-design.md`](../superpowers/specs/2026-09-13-armonia-funzionale-design.md).

---

## Il principio: ogni accordo ha una funzione

`[LIB]` Smith, *Jazz Theory* (4ª ed.), cap. VIII «Functional Harmony in Jazz»,
p. 51:

> «Nell'armonia funzionale ogni accordo gioca un **ruolo specifico** nella
> sequenza in cui compare. Un accordo può stabilire la tonalità all'inizio di un
> pezzo, servire una funzione conclusiva alla fine, vagare fra punti più stabili,
> prolungare un accordo che lo precede, ecc. Per contrasto, gli accordi in un
> contesto **non funzionale** sono usati soprattutto come sonorità — suoni con un
> particolare colore o tessitura.»

È la stessa frontiera che divide questa istruzione dal modale: **funzione contro
colore.** Qui gli accordi *tirano*.

`[LIB]` Piston, *Harmony* (5ª ed.), cap. 5 «Tonality and Modality», p. 52 («Tonal
Functions of the Scale Degrees», «Dominant Harmony»): i gradi della scala non
sono pari. Tre funzioni reggono il tonale:

| funzione | gradi | cosa fa |
|---|---|---|
| **Tonica** (T) | I (e vi, iii come suoi sostituti) | riposo, la casa |
| **Sottodominante** (S) | IV, ii | allontanamento, prepara la dominante |
| **Dominante** (D) | V, vii° | tensione, **vuole** risolvere sulla tonica |

Il moto **T → S → D → T** è il respiro. `[LIB]` Smith p. 51: gli accordi base di
ogni tonalità sono gli **accordi diatonici di settima**, e il loro movimento più
tipico segue il **circolo delle quinte** (per quinta discendente / quarta
ascendente).

---

## Il vocabolario

### Il ii-V-I, l'atomo

`[LIB]` Smith, cap. VIII, p. 53: *«Il paradigma [dell'alternanza forte-debole del
jazz] è la progressione **II V I**, che è ubiqua nel jazz. Come si usa di solito,
I e II sono accordi forti, V è un accordo debole.»* È la cellula minima del
tonale funzionale.

**Maggiore** (in Do): `Dm7 | G7 | Cmaj7` — il ii, il V, il I, tutti **diatonici**.

**Minore** (in Do minore): `Dm7b5 | G7b9 | Cm` — il **iiø7** (il mezzo-diminuito,
diatonico del minore) e il **V7 con la sensibile**. ⚠️ Il si naturale del G7 non
è nel Do minore naturale: è la **sensibile** presa dal minore armonico, ed è lei
a fare la spinta verso casa. Il ♭9 (la♭) è il colore idiomatico della dominante
di minore.

`[CALC]` **Il cuore, ed è quello che tira.** Il V7 porta un **tritone** fra la 3ª
e la 7ª (in G7: **si–fa**). Risolvendo sul I, tutt'e due si muovono di un
semitono in versi opposti: **si→do** (la sensibile sale alla tonica), **fa→mi**
(la 7ª scende alla 3ª del I). È il tritono a sciogliersi — la ragione fisica per
cui la dominante «vuole» la tonica. `[LIB]` Piston, cap. 15 «The Dominant Seventh
Chord», p. 243 («Regular Resolution»).

### Le cadenze

`[LIB]` Piston, cap. 11 «Cadences», p. 172: *«Non ci sono formule armoniche più
importanti di quelle usate per le chiuse di frase. Segnano i punti di respiro
della musica, stabiliscono o confermano la tonalità, e rendono coerente la
struttura formale.»* Quattro tipi:

| cadenza | formula | effetto |
|---|---|---|
| **autentica** | V → I | la chiusa piena. `[LIB]` Piston p. 172: la si estende col ii o il IV che la precede — è il ii-V-I |
| **plagale** | IV → I | la chiusa «amen», più morbida, senza sensibile. `[LIB]` Piston p. 178 |
| **d'inganno** | V → vi | promette la tonica e va altrove. `[LIB]` Piston p. 181 |
| **sospesa** (half) | … → V | si ferma **sulla** dominante: una domanda, non una risposta. `[LIB]` Piston p. 175 |

`[CALC]` **Perché l'inganno inganna dolce:** il vi (La m in Do) **contiene la
tonica**. La m è la-do-mi, e do-mi sono due delle tre note del Do maggiore: la V
non trova il I ma qualcosa che gli somiglia. La sorpresa è morbida perché la casa
è quasi lì.

### Il turnaround

Il giro che **rimanda** dalla fine all'inizio. La forma diatonica: **I – vi – ii
– V**, in Do `C | Am | Dm7 | G7` — tutti diatonici, e finisce sul V che rigira sul
I. `[DEC]` La variante **I – VI7 – ii – V** (`C | A7 | Dm7 | G7`) trasforma il vi
in una **dominante secondaria** (A7 = V7/ii): è il ponte diretto a
[`dominanti-secondarie.md`](dominanti-secondarie.md).

⚠️ `[LIB]` Smith p. 53 mostra anche un turnaround **cromatico** (Tadd Dameron,
*Lady Bird*): `Imaj7 | ♭IIImaj7 | ♭VImaj7 | ♭II7 | Imaj7`. È già cromatismo — la
colla sta in [`accordi-di-passaggio.md`](accordi-di-passaggio.md); qui basta
sapere che esiste.

---

## Come si stabilisce una casa

1. **scegli la tonalità** e scrivila con `set_scale` (è il layout della griglia);
2. **apri sulla tonica** — è la casa, e va sentita stabile prima di allontanarsi;
3. **allontanati verso la sottodominante** (IV o ii), poi **carica la dominante**
   (V7): è il T → S → D che prepara il ritorno;
4. **chiudi con la cadenza** che vuoi — autentica per la chiusa piena, d'inganno
   per rilanciare, sospesa per lasciare una domanda;
5. **per rigirare**, un turnaround (I–vi–ii–V) riporta al I e riparte.

---

## Come si scrive, materialmente

Gli accordi li realizza `MU.armonia`, che calcola le note **dalla sigla** e
conduce le parti (`condotta=True`, il default: muove poco le voci — il voice
leading già approvato il 29 agosto):

```python
from delugexml import song as S, musica as MU

S.set_scale(doc, 'C', 'maggiore')
note = MU.armonia('Cmaj7 | Am7 | Dm7 | G7 | Cmaj7', registro='do3', durata='1/1')
#                    I      vi     ii    V     I   -- turnaround + cadenza autentica
```

Per una casa minore, `set_scale(doc, 'C', 'minore')` e il ii-V-i col mezzo-diminuito:
`Dm7b5 | G7b9 | Cm`.

---

## Cosa NON fare

- **non confondere la casa col modale.** Se non vuoi che l'armonia tiri a casa,
  quello che ti serve è [`armonia-modale.md`](armonia-modale.md), non questa: lì
  il ii-V-I è precisamente l'errore;
- **non togliere la sensibile al V di minore.** Il Do minore naturale non ha il
  si: senza il si naturale del G7 la dominante non spinge, e la cadenza si
  affloscia;
- **non incatenare cadenze d'inganno.** L'inganno vive perché è raro: uno rilancia,
  due di fila diventano una progressione senza meta;
- **non dare per scontato il ritmo armonico.** Ogni quanto cambia l'accordo è una
  scelta del pezzo, non una regola di qui (come in tutte le istruzioni d'armonia).

---

## Cosa manca a questa istruzione

- **le dominanti secondarie** — dare spinta a un grado diverso dalla tonica
  tonicizzandolo: c'è, in [`dominanti-secondarie.md`](dominanti-secondarie.md),
  la seconda faccia della spina;
- **il ritmo armonico** — ogni quanto cambia l'accordo, e come la cadenza cade sul
  metro;
- **la dominante alterata** — la tensione della dominante (♭9, ♯9, ♯5, alt; la
  scala alterata e la lidia dominante dal minore melodico; l'uso funzionale di
  ottatonica ed esatonale): è il passo naturale **dopo** questa — la tensione,
  dopo la funzione;
- il **voicing** oltre il triadico/settima, il **comping**, il **contrappunto**:
  sono priorità 2 (forma), non questa istruzione.
