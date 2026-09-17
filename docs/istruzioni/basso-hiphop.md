# Scrivere una linea di basso — feel HIP HOP (boom-bap)

⚠️ **PERIMETRO.** Questa istruzione copre **un feel solo**: il basso dell'hip hop
boom-bap — **rado, grave, ancorato alla cassa**. È il **fondo** del beat, non una
voce che corre. **Non è il riff fitto del funk** ([basso-funk.md](basso-funk.md))
né il walking: qui comanda lo **spazio** e la **fondamentale pesante**.

⚠️ Ci sono due sotto-idiomi, e il feel si dichiara prima:

| | sub / 808 | boom-bap campionato |
|---|---|---|
| suono | sub sintetico, lungo, spesso con **glide** | contrabbasso/basso elettrico *campionato*, corto |
| note | poche, tenute, gravissime | frammento che segue il loop, staccato |
| tipico di | trap, dirty south, modern | East Coast, jazzy, lo-fi |

---

**A cosa serve.** Hai un beat (cassa e rullante) e un loop d'accordi «polveroso»,
e ti serve il basso che tiene il fondo. Questa istruzione dice come stare grave e
agganciato senza affollare.

**Cosa ti serve prima di cominciare:**

- il loop armonico (nell'hip hop l'armonia è **il campione**: un giro breve,
  spesso jazzy/soul, che si ripete);
- il registro: **grave**, spesso un'ottava sotto il funk — sul Deluge la zona
  **do1-do2** (24-36) per il sub, fino a mi2 per il boom-bap campionato;
- **la cassa, colpo per colpo** — il basso *è* il fondo della cassa. Vedi
  [batteria-hiphop.md](batteria-hiphop.md).

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura didattica, con fonte |
| `[MIS]` | misurato su un corpus, con quale e quante esecuzioni |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ **Qui non c'è `[MIS]`, come per ballad e twobeat.** Nessun corpus in casa ha
il basso dell'hip hop: il Groove MIDI è **batteria sola**, la libreria
`(aq) HipHop` sono **drum loop su canale 0** (kick/rullante/hat, nessun basso), e
in `The_Magic_of_MIDI` non c'è una popolazione hip-hop pulita. Quello che segue è
**letteratura e decisione**.

---

## Il cuore — l'aggancio alla cassa

`[LIB]`+`[DEC]` La regola numero uno del basso hip hop: **suona dove suona la
cassa**, e soprattutto la **fondamentale sul 1** (il «boom» principale) e sul 3.
Il basso e la cassa sono **una voce sola nel grave** — il basso dà l'altezza a
ciò che la cassa dà come colpo. Dove la cassa sincopa sul "+", spesso il basso la
segue; dove la cassa tace, il basso tace (o tiene).

⚠️ **Rado, non fitto.** Due-quattro note per battuta, non sette come il funk. Lo
spazio **è** il feel: un beat hip hop respira fra il boom e il bap.

---

## L'altezza — la fondamentale pesante, e poco altro

`[LIB]`+`[DEC]` Nell'hip hop l'armonia la porta il **loop campionato** (il
Rhodes/piano polveroso); il basso non la elabora, la **ancora**: suona la
**fondamentale** di ogni accordo del giro, nel registro grave, e poco altro. Le
mosse in più, con parsimonia:

- la **fondamentale ribattuta** o tenuta (il sub che dura);
- l'**ottava** grave↔sopra, come firma di groove (come nel funk, ma rara);
- un **passaggio** cromatico o di scala verso la fondamentale dell'accordo dopo,
  sull'ultima croma (il pickup, di rado);
- la **quinta** o la **settima** grave sotto un accordo tenuto, per colore.

⚠️ **Non farne un riff.** Se il basso diventa una figura fitta e melodica, è
funk o neo-soul, non boom-bap. Qui è il **fondo**.

---

## Sub tenuto o plucked corto — la scelta di suono

`[DEC]` Le due facce del perimetro qui sopra si scrivono diverse:

- **sub / 808**: note **lunghe e legate** (durano fin sotto la nota dopo), a
  volte con un **glide** fra due fondamentali. Velocity uniforme, grave, pieno;
- **boom-bap campionato**: note **corte e staccate**, che imitano il pizzicato di
  un contrabbasso preso da un disco. Più articolate, meno sub.

---

## Come si scrive, materialmente

```python
from delugexml.notes import Note
# 96 tick = un movimento, 384 = una battuta, 48 = una croma
# La minore, sub agganciato alla cassa (1 e 3), + un pickup verso il Re (Dm dopo)
# La0=33? no: sub grave. La1=33, Re2=38. Qui La1=33 sul 1, ottava/tenuta.
voce = {}
for pos, alt, dur, vel in [
    (0,   33, 168, 96),   # La1  il 1 (boom), tenuta
    (192, 33, 72,  88),   # La1  il 3, ribattuta corta (con la cassa)
    (336, 37, 48,  78),   # Do#2 pickup cromatico verso il Re della battuta dopo
]:
    voce.setdefault(alt, []).append(Note(pos=pos, length=dur, velocity=vel))
```

⚠️ **La scelta durata dice il sotto-idioma:** lunga = sub tenuto, corta =
boom-bap plucked. Aggancia sempre il 1 (e il 3) alla cassa.

L'esempio lavorato è in `tools/hiphop_scritto.py` (il sub di un giro lo-fi in La
minore, agganciato alla cassa). ⚠️ **Verdetto dell'ascolto (17 settembre 2026):**
*«ok funziona»*.

---

## Cosa NON fare

- **non fare un riff fitto.** Sette note per battuta è funk; qui 2-4, rade;
- **non camminare.** Quattro semiminime lisce è walking, un altro genere;
- **non scollegare il basso dalla cassa.** Il 1 (e il 3) del basso stanno dove
  batte la cassa: sono lo stesso colpo, uno grave e uno intonato;
- **non salire di registro.** L'hip hop vuole il **grave**: se il basso sta in
  mezzo, sparisce sotto il loop d'accordi;
- **non far muovere l'armonia col basso.** L'armonia è il loop campionato; il
  basso la ancora, non la cambia.

---

## Cosa manca a questa istruzione

- **il `[MIS]`**: nessun corpus di basso hip hop trascritto. È il buco di sempre
  (come ballad e twobeat);
- **il suono**: il sub 808 (con glide e distorsione) e il campione di contrabbasso
  polveroso sono scelte di **suono**, non di note — vanno in `dsp-recipes`/sound;
- **il sample-chop**: quando il basso *è* un pezzo di bassline campionata e
  tagliata (non note suonate), il materiale vive in `audio.py`, non qui;
- **il rapporto col loop campionato**: qui il basso àncora le fondamentali; il
  dialogo fine con la linea del sample resta da fare.
