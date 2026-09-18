# Trip-hop — la fusione (hip-hop + dub + armonia minore), e l'eco dub — progetto

**Data:** 18 settembre 2026
**Cos'è:** il **terzo genere del perimetro 3**, dopo hip hop e house/techno. Il
trip-hop non è una capacità nuova ma una **fusione con un carattere**: la batteria
hip-hop rallentata e polverosa, il basso dub, l'**armonia minore jazzy** (priorità
1) e lo spazio del dub. L'unico pezzo di suono davvero nuovo è l'**eco dub**, che
diventa una primitiva riusabile.

## Perché, e cosa si è deciso

Il trip-hop (Portishead, Massive Attack, Tricky) è downtempo, scuro, hazy,
cinematico. Il progetto ha già i pezzi: la batteria boom-bap (`batteria-hiphop.md`,
con la sua variante **lo-fi swingata/laid-back**), il basso sub, e i **moduli
d'armonia** per il minore jazzy. Il lavoro è **ricombinarli** col carattere giusto,
non inventare.

Deciso in brainstorming il 18 settembre 2026:

- **ricombinazione + una primitiva**: `MU.eco_dub` (l'eco dub, riusabile anche per
  dub e reggae). Il resto riusa gli strumenti esistenti;
- **sapore Portishead**: scuro, jazzy, **armonia al centro** (la priorità 1);
- **il vamp**, in **Do minore**: `Cm9 | Cm9 | A♭maj7 | G7♭9` — i–i–**♭VI**–**V7♭9**
  (il ♭VI caldo, prestito modale; la dominante alterata scura). Verificato col
  `[CALC]` (`racconta_armonia`, 18 set 2026): Cm9 rootless E♭ G B♭ D, A♭maj7
  C E♭ G B♭, G7♭9 A♭ B D F, condotti.

⚠️ **Metodo, misto (per le regole del progetto):** l'**armonia si chiude col
`[CALC]`** (memoria `armonia-si-chiude-col-calc`); batteria, basso, suono/eco → il
**tuo ascolto**. E i *livelli* (feedback dell'eco, swing, velocity) sono sfumature,
non leggi (memoria `livelli-sfumature-non-leggi`): buoni punti di partenza,
argomenti regolabili, non da tarare al millimetro.

## Il meccanismo dell'eco dub, dai file veri

- `delayFeedback` e `delayRate` sono **param** (`param_ids`: `GLOBAL_DELAY_FEEDBACK`
  / `GLOBAL_DELAY_RATE`) → nel `<defaultParams>` del preset, che `add_track` sposta
  sul `<params>` della **clip**.
- L'elemento **`<delay>`** (figlio dello strumento) porta `syncLevel`, `syncType`,
  `pingPong`, **`analog`** — e `analog=1` è il **degrado caldo** a ogni ripetizione,
  il suono del dub.
- Il preset `Pianism I` (il Rhodes del pezzo) ha già `delayRate`, `delayFeedback` e
  `<delay>`: niente scritture al buio.

## I quattro artefatti di questo giro

### 1. La primitiva — `MU.eco_dub`

```
eco_dub(doc, bersaglio, *, feedback=35, sync=7, analog=True, pingpong=False,
        rate=None) -> dict
```

Accende l'eco dub sul synth `bersaglio` (nodo strumento). Due livelli, come
`MU.acid`/`MU.sidechain`:

- **strumento** (elemento `<delay>`): `analog='1'` se `analog` (il degrado dub),
  `pingPong` se `pingpong`, `syncLevel=sync`/`syncType=0` (l'eco a tempo). Se
  l'elemento manca, lo crea;
- **ogni clip del bersaglio**: `delayFeedback = feedback` (le ripetizioni, unità
  display 0-50); se `rate` è dato (eco libero, non sincronizzato), scrive anche
  `delayRate`.

Ritorna un racconto e dichiara `da_verificare=True` (i livelli si giudicano
all'orecchio). Struttura `[OSS]` (attributi nel preset), livelli `[DEC]`.

### 2. Il pezzo — `tools/triphop_scritto.py`

Portishead-ish: **~84 BPM**, **Do minore**, forma breve.

- **armonia** (il centro): il vamp `Cm9 | Cm9 | A♭maj7 | G7♭9` sul Rhodes
  (`Pianism I`), voicing **rootless** grave, accordi **tenuti e molli** (velocity
  ~55), con l'**`eco_dub`** e un velo di **riverbero** (`reverbAmount`);
- **batteria** (808/kit, polverosa laid-back): boom-bap **rallentato** — cassa sul
  1 e sul 3 (col basso), rullante/backbeat sul 2 e 4 ma **più morbido**, ghost
  molli, hi-hat in crome con **più aria**; `set_swing(~56)` (il lilt lo-fi,
  laid-back). Riusa gli idiomi di `batteria-hiphop.md`, rallentati e swingati;
- **basso** dub: **sub profondo e rado**, segue le fondamentali del vamp
  (C, C, A♭, G), note lunghe, dietro il beat;
- forma con `MU.forma`: intro (Rhodes + eco, solo) → il giro pieno (tutti). ~16-24
  battute — compatto;
- `verifica()` vuota; `test_triphop_scritto` che controlla l'armonia (le classi di
  altezza del vamp), l'eco dub (delay analog + feedback sulle clip del Rhodes) e la
  forma.

### 3. L'istruzione — `docs/istruzioni/trip-hop.md`

Una sola (è una fusione): il carattere e la ricombinazione. Copre:
- **cos'è**: downtempo scuro cinematico; la fusione di hip-hop (batteria), dub
  (basso + spazio), jazz (armonia minore);
- **il feel**: lento (~70-90), **laid-back** (dietro il beat), swing leggero;
- **la batteria**: boom-bap rallentato, più morbido e con più aria — rimanda a
  `batteria-hiphop.md` (variante lo-fi), da non ripetere;
- **il basso**: dub, sub, rado — rimanda a `basso-hiphop.md`/dub;
- **l'armonia** (il cuore): minore jazzy, prestiti (♭VI), dominanti alterate,
  Rhodes rootless — rimanda ai **moduli d'armonia**; *il sapore è scelta
  compositiva* (come per hip hop e i sottogeneri jazz);
- **lo spazio**: l'`eco_dub` e il riverbero — l'atmosfera è metà del genere;
- **i gradi**: `[LIB]`+`[DEC]` (nessun corpus trip-hop nel Groove MIDI; la batteria
  si appoggia al `[MIS]` boom-bap dell'hip hop, rallentato); eco `[OSS]`+`[da
  verificare]`; armonia `[CALC]`;
- **cosa manca**: il vocal breathy e il sample/vinyl crackle (materiale di
  `audio.py`).

### 4. La scheda e l'indice

- `docs/repertori/trip-hop.md`: la vista per casella (11 caselle), come hip hop e
  house. Piene: 1 (cos'è), 3 (tempo), 4 (feel laid-back), 5 (ruoli), 6 (dinamica
  morbida), 7 (armonia minore, `[CALC]`), 10 (sul Deluge: `eco_dub`, Rhodes, kit).
  Parziali/vuote dichiarate: 8 (topline: il vocal/sample, `audio.py`), 9 (forma:
  accennata), 2 (metro), 11 (trappole).
- `docs/MUSICA.md`: **nuova riga** nell'indice per trip-hop (col link), come si è
  fatto per hip hop e house — spostandola dalla riga aggregata «elettronica · IDM ·
  trip hop · DnB · jungle».

## Cosa resta fuori (YAGNI)

- il **vocal** breathy e il **sample/vinyl crackle**: sono `audio.py` (campioni);
- il **collage à la DJ Shadow** (break tagliato): è la strada jungle/DnB, vuole lo
  slicing in `audio.py`;
- una primitiva per il **laid-back drag**: si ottiene con `set_swing` + eventuale
  `MU.applica_microtiming`, già esistenti — niente primitiva nuova;
- il tuning fine dei livelli (eco, swing): è ascolto/nuance.

## Rischi e come si chiudono

| rischio | mossa |
|---|---|
| l'eco dub non si sente / feedback runaway | `feedback` esposto come argomento, `[da verificare]`; partire moderato (~35) e giudicare all'orecchio |
| la batteria trip-hop senza corpus suona generica | `[LIB]`+`[DEC]` onesto, appoggiata al `[MIS]` boom-bap; il carattere (lento, morbido, aria) è dichiarato, non misurato |
| riflesso: rimettere lo spang-a-lang o un idioma d'altro feel | fondare il groove PER il trip-hop (memoria `riflesso-idioma-fuori-contesto`) |
| fine-riga corrotti | `write_bytes`/`newline=''`; `git diff --stat` == `--ignore-cr-at-eol` |
| `print()` con `⚠️` | vietato: console cp1252 |

## Fatto =

- `MU.eco_dub` col test verde;
- `triphop_scritto.py` che costruisce il pezzo, `verifica()` vuota, `test_triphop_scritto` verde;
- l'istruzione, la scheda (con la riga d'indice nuova) coerenti; suite INTERA verde prima di committare la scheda;
- il file caricato sul Deluge per l'ascolto — l'armonia è già chiusa col `[CALC]`, il resto lo chiude l'orecchio.
