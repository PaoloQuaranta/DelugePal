# Armonia: il prestito modale (modal interchange) — progetto

**Data:** 12 settembre 2026
**Cos'è:** la seconda istruzione armonica del progetto, dopo `armonia-modale.md`.
Dice come prendere in prestito un accordo da un modo parallelo per colorare una
tonalità di casa. È priorità 1 (armonia) e il ponte dichiarato verso
l'eclettismo che l'utente cerca.

## Perché, e la scelta fatta

Il perimetro, deciso l'11 settembre (§6-duetvicies, e `perimetro-deluge-pal` in
memoria), mette l'armonia al centro e chiede di *«attingere al bagaglio
espressivo di un genere»* invece di replicarlo. Il prestito modale è
esattamente questo: un modo controllato di mescolare i colori di modi diversi
senza lasciare la casa.

`armonia-modale.md`, scritta il giorno prima, ha già coperto lo **stare fermi in
un modo**. Questo documento copre l'orientamento **opposto**, e la scelta è
stata presa dall'utente in brainstorming il 12 settembre:

> La casa del prestito è una **tonalità maggiore o minore**.

Cioè il caso da manuale di Stuart Smith (`Jazz Theory`, 4ª ed., cap. VIII
«Functional Harmony», p. 66): hai una tonalità tonale e ci infili un ospite
preso dal parallelo. Non il caso modo→modo, che resta fuori (vedi in fondo).

## Il principio: una casa, e un colore preso a prestito

`[LIB]` Smith p. 66: *«Chords are often "borrowed" from the parallel major or
minor; accordingly, such chords are called "borrowed chords". For example, Fm
might occur as IVm in the key of C major as a chord borrowed from C minor.»*

L'idea che regge tutto: **hai una casa tonale, e l'accordo preso in prestito è
un ospite che la colora, non la sostituisce.** Dopo il colore, il diatonico si
riafferma. Se non torni a casa, non hai preso in prestito: hai modulato.

⚠️ **È l'orientamento opposto ad `armonia-modale.md`, e i due documenti vanno
linkati a vicenda.** Lì l'armonia è ferma e si evita ogni spinta tonale; qui
c'è una casa tonale funzionante, e il prestito è una deviazione momentanea da
cui si rientra. Chi legge deve sapere in quale dei due mondi sta lavorando.

## I due artefatti di questo giro

1. **L'istruzione** `docs/istruzioni/armonia-prestito.md`, file sorella di
   `armonia-modale.md`. È la parte che resta.
2. **Un pezzo di prova costruito da zero**, in Do maggiore, col *iv* minore come
   colore centrale, caricato sul Deluge. È l'esempio lavorato che chiude
   l'istruzione, e la prova del flusso «creare dal nulla» — che nessuna
   istruzione armonica del progetto ha ancora superato.

## L'istruzione: cosa contiene

Segue la forma collaudata delle istruzioni (vocabolario → vincoli → procedura
locale → esempio lavorato), coi gradi di prova `[LIB]`/`[CALC]`/`[DEC]`/`[OSS]`.
Fondata su **Smith p. 66-69** e su **Piston** (i capitoli sul mixture, letti in
corso d'opera — `to-read/`, non versionato).

### Il vocabolario

I prestiti ad alto valore in una casa **maggiore**, presi dal minore parallelo
e dagli altri modi paralleli. Ognuno con il colore che porta e la sua fonte:

| prestito | accordo in Do | colore | fonte |
|---|---|---|---|
| **iv** | Fm | caldo, plagale, nostalgico | `[LIB]` Smith p. 66 (*Sunny Side of the Street*) |
| **♭VI** | A♭ | cinematografico, ampio | `[LIB]` Piston (mixture) |
| **♭VII** | B♭ | modale/rock; il I↔♭VII «tonic-by-assertion» | `[LIB]` Smith p. 69 (*Killer Joe*) |
| **♭III** | E♭ | scuro, bluesy | `[CALC]` dal minore parallelo |
| **♭II** | D♭ | napoletano, teatrale | `[LIB]` Piston |
| **Im / I→Im** | Cm | scivolata luce→ombra | `[LIB]` Smith p. 67 (*On Green Dolphin Street*, *I'll Remember April*) |
| **iiø7** | Dm7♭5 | tensione di preparazione alla cadenza | `[CALC]` dal minore |

Le note di ogni accordo sono **derivabili** dagli intervalli della scala
parallela. Quindi un **test `[CALC]`** le blinda contro `song.MODI`, esattamente
come `armonia_modale_note_caratteristiche` fa già per l'armonia modale.

### I vincoli: cosa fa sì che sia un prestito e non un cambio di tonalità

- **torna a casa.** L'ospite se ne va; il diatonico si riafferma. Se resti
  fuori, hai modulato — e la modulazione è un'altra cosa (Smith la tratta a
  parte, p. 67-68).
- **non incatenare troppi prestiti.** Due o tre accordi presi in fila e
  l'orecchio perde la casa: diventa ambiguità o modulazione.
- **il prestito va in posizione di colore o di passaggio**, tipicamente prima di
  un ritorno a I o su un grado che hai già (il IV che diventa iv).
- **la melodia deve reggere la nota presa in prestito.** Il la♭ del Fm stona se
  la melodia in quel punto batte il la naturale. Il prestito si decide guardando
  anche la voce in cima, non solo la griglia degli accordi.

### La procedura LOCALE

La forma «una decisione locale, poi si compone» che ha fatto funzionare il
walking e l'armonia modale:

1. parti da un giro diatonico che regge — è la casa;
2. scegli il punto dove vuoi il colore (spesso il IV che diventa iv, o la
   battuta prima di un ritorno a I);
3. prendi l'accordo dal parallelo, scegliendolo dalla tabella per il colore che
   vuoi: caldo → iv, cupo → ♭VI / ♭II, modale/rock → ♭VII;
4. controlla i vincoli: torni a casa, la melodia regge la nota presa in prestito.

### Come si scrive, materialmente

```python
from delugexml import song as S, musica as MU

S.set_scale(doc, 'C', 'maggiore')
note = MU.armonia('Cmaj7 | Am7 | Fmaj7 | Fm7 | Cmaj7', registro='do3',
                  durata='1')
```

Voicing **per terze**, caldo — **non** quartale. `[OSS]` È la lezione di PERCHE
(11 settembre): il quartale non è automaticamente meglio, e qui il corpo delle
triadi è proprio il punto.

## Il pezzo di prova (da zero)

- **Casa:** Do maggiore. **La star:** il *iv* minore (Fm).
- **Giro, ~8 battute** — diatonico che fonda il Do, poi il IV→iv prima del
  ritorno:

  ```
  | Cmaj7 | Em7 | Fmaj7 | Fm7 | Cmaj7 | Am7 | Dm7  G7 | Cmaj7 |
                   IV →   iv           (il colore è la battuta 4)
  ```

- **Melodia:** una linea semplice che sopra l'Fm7 **canta il la♭** — la ♭6 presa
  in prestito. È lì che il prestito si *sente*, in cima, non solo sotto. Prima e
  dopo la melodia sta su note diatoniche, così il la♭ spicca come l'evento.
- **Strumenti sul Deluge:** tastiera che accompagna (voicing da `MU.armonia`), un
  synth per la melodia, basso sulle fondamentali. **Niente batteria** — è una
  dimostrazione d'armonia, e il ritmo è priorità 3.
- **Consegna:** XML caricato sul Deluge via SysEx. L'utente apre e ascolta.

## Cosa vuol dire «fatto»

- l'istruzione scritta e fondata sulle fonti (Smith citato con pagina, Piston
  dove serve);
- il test `[CALC]` verde sugli accordi presi in prestito;
- il pezzo caricato sul Deluge; l'utente lo apre, lo ascolta, e il suo verdetto
  diventa l'esempio lavorato — come *«frigio mi piace molto»* ha chiuso
  l'armonia modale.

## Rischi, e cose da verificare in corso d'opera

⚠️ **`MU.armonia` sa esprimere un accordo fuori scala?** L'Fm ha il la♭, che non
è nel Do maggiore. Il primo punto tecnico da verificare è che la primitiva
calcoli le note di un accordo **cromatico**, e come il Deluge — con la scala
impostata su Do maggiore — tratta le note fuori scala (sul dispositivo sono
suonabili: la scala è il layout della tastiera, non un filtro — ma va
verificato, non dato per scontato). Se la primitiva non regge il cromatico, il
design dell'istruzione **non cambia**: cambia solo il «come si scrive», e lo si
dichiara.

⚠️ **«Da zero» è terreno non ancora calpestato.** L'armonia modale ha superato
l'armonizzare un'idea esistente, non il creare dal nulla. Questo pezzo è la
prima prova di quel flusso, e potrebbe rivelare che «da zero» ha bisogni che
l'«armonizzare» non aveva (una melodia che non c'era, una forma da inventare).

## Cosa resta fuori da questo giro

- ~~**la direzione inversa**: una casa **minore** che prende in prestito dal
  maggiore parallelo~~ — **presa in carico il 12 settembre 2026**, vedi
  l'addendum in fondo.
- **le scale non diatoniche** che l'utente usa (ottatoniche, cromatiche): questo
  documento copre il prestito fra i sette modi diatonici, non quelle.
- **il ritmo armonico** (ogni quanto cambia l'accordo) resta una scelta del caso,
  non una regola — come già in `armonia-modale.md`.

## Cosa NON rifare

- **non quartale per default.** La lezione di PERCHE vale qui: il voicing è un
  colore del vocabolario, non un traguardo;
- **non fondare a memoria.** Il mestiere viene dalla fonte: Smith p. 66-69 è già
  letto, Piston si legge sui capitoli del mixture prima di scrivere la tabella;
- **non incatenare i prestiti.** È il vincolo che separa il prestito dalla
  modulazione, e va rispettato anche nel pezzo di prova.

---

## Addendum — la direzione inversa: casa minore (12 settembre 2026)

Dopo che il pezzo in Do maggiore è stato approvato all'ascolto, si chiude la
«cosa resta fuori» numero 1: una casa **minore** che prende in prestito dal
**maggiore** parallelo.

**La scelta (brainstorming, 12 settembre):** il colore protagonista è il **IV
maggiore** — il contrario simmetrico del iv minore del primo pezzo (IV↔iv).

**La fonte.** Smith p. 74: in minore i gradi **6 e 7 alzati** sono «presi in
prestito dal maggiore parallelo» (la notazione a frecce ↑6, ↑7). Da lì il
vocabolario di una casa minore:

| prestito | in La minore | nota di colore | fonte |
|---|---|---|---|
| **IV maggiore** | Re (D F# A) | fa# (♮6) | `[LIB]` Smith p. 74 — la schiaritura dorica |
| **ii minore** | Bm (B D F#) | fa# (♮6) | `[CALC]` dal maggiore |
| **I maggiore (Piccardia)** | La (A C# E) | do# (♮3) | `[LIB]` Piston, cap. 26 e dintorni |

⚠️ Il **V maggiore** (E7, col sol#) **non** è un prestito: è la normale
dominante del minore armonico. Va detto nell'istruzione, per non confondere le
due cose.

**Il test `[CALC]`** rispecchia quello già fatto, sull'altro verso: maggiore −
minore parallelo = {♮3, ♮6, ♮7} = {4, 9, 11}.

**Il pezzo di prova**, in La minore, da zero, col iv→IV come star:

```
Am | Em | Dm | D | Am | Dm | E7 | Am
 i    v   iv   IV   i   iv   V7   i
```

La melodia canta il **fa naturale** sul Dm (battuta 3) e lo alza al **fa#** sul
Re maggiore (battuta 4): il ♮6 in cima, simmetrico al la→la♭ del pezzo in Do.
Rhodes / tromba / basso, niente batteria.

**Codice:** si estende `tools/prestito_scritto.py` con la seconda progressione
(`PROGRESSIONE_MIN`, `MELODIA_MIN`, `BASSO_MIN`, e `comping_min()/tema_min()/
basso_min()`), non un file nuovo.

**Cosa resta fuori ancora:** la terza di Piccardia e il ♮6/♮7 jazz restano
nominati ma non provati; le scale non diatoniche idem.

---

## Addendum 2 — i colori del minore jazz e la Piccardia (12 settembre 2026)

Si chiudono gli ultimi due colori della casa minore, entrambi presi dal
maggiore parallelo e mostrati in **un solo pezzo**.

- **il colore del minore jazz** — gli accordi di tonica **m6** (col ♮6) e
  **m(maj7)** (col ♮7), cioè il sapore della minore melodica. Mostrato col
  *line cliché*: `Am → Am(maj7) → Am7 → Am6`, la discesa A-G#-G-F# su un pedale
  di tonica. `[LIB]` Smith p. 74 (il ♮6/♮7 «presi dal maggiore parallelo»); il
  line cliché è `[DEC]`, un'applicazione idiomatica nota.
- **la terza di Piccardia** — il finale che si apre: un pezzo in minore che
  chiude su una tonica **maggiore** (in La minore, La maggiore col do#, ♮3).
  `[LIB]` Piston (la pagina esatta si pinna scrivendo l'istruzione).

**Il pezzo**, in La minore, da zero, con entrambi i colori:

```
Am | Am(maj7) | Am7 | Am6 | Dm7 | E7 | Am | A
 i    i(maj7)   i7    i6    iv   V7   i    I(Picc.)
```

La melodia canta il line cliché in cima (la→sol#→sol→fa#, battute 1-4) e chiude
sul **do#** (battuta 8), così la Piccardia si sente anche in cima.

⚠️ **Fattibilità verificata:** `MU.sigla` legge nativamente `Am6`,
`Am(maj7)`/`AmMaj7` e `A` (maggiore). Nessuna sigla nuova da aggiungere.

**Il test** estende `test_armonia_prestito_casa_minore` con `Am6` (♮6=9) e
`AmMaj7` (♮7=11). **Il codice** aggiunge il terzo pezzo a `prestito_scritto.py`
(`*_JAZZMIN`). **Cosa resta fuori dopo:** le scale non diatoniche.
