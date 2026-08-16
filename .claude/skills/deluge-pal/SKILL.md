---
name: deluge-pal
description: Genera e modifica song per il Synthstrom Deluge a partire da descrizioni musicali a parole, caricandole sul dispositivo via SysEx. Usare quando si parla di comporre, arrangiare, mixare o progettare suoni per il Deluge, o quando si nominano clip, kit, arranger, tracce MIDI/CV o clip audio del Deluge.
---

# Deluge Pal

Il progetto sta in `D:\DelugePal`. **Leggere `HANDOFF.md` a inizio sessione.**

## Il ciclo

```
prompt → libreria → XML → SysEx → l'utente apre e ascolta
                                          ↓
    ricarica come     ←   modifica   ←   «il basso è troppo statico»
    versione nuova          ↑
                    RISCARICA dal Deluge prima di toccare
```

## Le sei regole

0. **L'ordine in cui si cerca una risposta.** Quando serve sapere *come
   funziona il Deluge*, si cerca in quest'ordine e ci si ferma appena si
   trova:

   ```
   1. documentazione community  →  2. guidebook  →  3. sorgente del firmware
                                                    →  4. i file locali
   ```

   **I file locali sono l'ULTIMO passo, non il primo.** Servono a verificare
   com'è scritta una cosa che si è già capita, non a scoprire cosa fa il
   dispositivo. Partire da lì è reverse engineering senza modello, e in
   questo progetto è la fonte di errore più ricorrente che ci sia: ha
   prodotto ricerca statistica su cose spiegate in una frase del manuale, i
   quattro modelli sbagliati della finestra di clip view, e l'ipotesi
   demolita sulla riga MIDI di un kit.

   Non confondere questo con l'ordine di **autorità**, che è un'altra cosa e
   va nella direzione opposta (`HANDOFF.md` §0): la documentazione dice cosa
   *deve* valere, i file dicono com'è *scritto*, solo il dispositivo dice se
   *funziona*. Si cerca dall'alto, si decide dal basso.

1. **Riscarica prima di modificare.** La song sul Deluge è la verità: lui la
   apre e può averci messo mano. Lavorare su una copia locale cancella il suo
   lavoro senza accorgersene.
2. **Mai scrivere XML.** Mai costruire nodi di formato a mano, mai trascrivere
   valori letti da un file. Solo chiamate alla libreria. Le costanti si
   generano da codice e si confrontano con un test.
3. **`musica.verifica(doc)` prima di ogni caricamento.** Se non è vuota, non
   si carica e si riferisce il problema. `musica.avvertenze(doc)` è
   un'altra funzione, con un altro scopo: non blocca, segnala cose che il
   dispositivo carica comunque ma con un effetto collaterale silenzioso
   (due clip nella stessa sezione, contenuto presente e invisibile — la
   stessa famiglia di bug di `yScrollSongView`). Vale la pena leggerla e
   dirla, ma non è un motivo per fermarsi.
4. **Raccontare cosa è cambiato**, con `musica.racconta(doc)` (l'intera song)
   o `musica.racconta_clip(doc, clip)` (una clip sola), e con i valori esatti
   dei parametri toccati. Un'operazione silenziosa non è correggibile.
5. **Si scrive solo nella propria sottocartella; si legge ovunque.** La
   regola ha due versi, e non sono simmetrici apposta:
   - **In scrittura**, `put` non sovrascrive: `HOUSE01`, `HOUSE02`, … Il
     percorso si costruisce **sempre** con
     `musica.destinazione(nome, versione, cartella)`, mai a mano: scrive
     solo dentro `<cartella>/DelugePal/`, una delle quattro in
     `musica.CARTELLE_SD` (`SONGS`, `KITS`, `SYNTHS`, `SAMPLES`), e
     **rifiuta** — non ripulisce — un nome che tenti di uscirne (`/`, `..`,
     `\`), un carattere non ammesso da FAT32/Windows (`<>:"|?*`, i
     caratteri di controllo) o una cartella che non sia una delle quattro.
     **L'estensione la sceglie sempre `destinazione()` in base alla
     cartella** — `.XML` per song/kit/synth, `.wav` per i campioni — e non
     va mai indicata nel nome: se il nome ne porta già una diversa, viene
     rifiutato invece di produrne una doppia. Le 135 song, i kit e i
     campioni dell'utente stanno alla radice di quelle stesse cartelle e
     non si toccano: è già costato pulire a mano 34 file di prova finiti lì
     per sbaglio.
   - **In lettura**, nessuna restrizione: `musica.origine(nome, cartella)`
     legge una song, un kit o un campione qualunque, ovunque sulla SD —
     serve per partire da materiale esistente dell'utente ("fammi una
     variazione di questa mia song", "usa il rullante di quel kit"). Non
     confondere le due funzioni: `destinazione()` è dove *si scrive*,
     `origine()` è da dove *si legge*, e solo la prima ha un cancello.

## Perché la regola 2 non è un consiglio

Due file generati sono stati rifiutati dal dispositivo, uno con un crash:

- una clip di kit con `<soundParams>` invece di `<kitParams>` — quel tag
  dichiara al caricatore il TIPO della clip (FINDINGS §6-quater)
- il `<params>` di una clip audio trascritto a mano da un'anteprima troncata:
  11 attributi su 31, valori inventati (§6-quinquies, crash E365)

Entrambi erano XML validi e si rileggevano senza errori.

## Come si fa

```python
import sys; sys.path.insert(0, 'tools')
from delugexml import parse_file, write_file, musica as MU
from delugexml import song as S, create as C, arranger as A, kit as K
from delugexml import midicv, audio
from delugexml.writer import FormatTable
```

| per | usare |
|---|---|
| leggere cosa c'è | `MU.racconta(doc)`, o `MU.racconta_clip(doc, clip)` per una sola |
| altezze | `MU.altezza('re2')`, `MU.nome_altezza(38)` — italiano e inglese, `do4 = C4 = 60` |
| pattern di batteria | `MU.passi('x...x...x...x...', lunghezza=…)` — `x` colpo, `X` accento, `.` silenzio. `lunghezza` è **già in tick grezzi**, la durata della singola nota: non passa da `durata_in_tick()`. Non è lo stesso concetto di `durata` qui sotto, anche se i nomi si somigliano — non scambiarli |
| melodie | `MU.melodia('re2 fa#2 la2', durata='1/8', articolazione='staccato')` — `durata` qui è il **passo fra una nota e la successiva** e passa da `MU.durata_in_tick()` (accetta '1/8', non un intero a caso), `articolazione` sceglie in `MU.ARTICOLAZIONI` (staccato/normale/legato) |
| accordi e progressioni | `MU.accordi('re3 fa3 la3 \| sib3 re4 fa4', durata='1/4')` — le altezze di un gruppo suonano **insieme**, i gruppi separati da `\|` sono la progressione nel tempo (`durata` fra un accordo e il successivo, come in `melodia()`). Con `melodia()` le stesse note uscirebbero in fila, non insieme |
| nuova traccia da preset | `C.add_track(doc, preset, name=…, folder=…)` |
| **scrivere note** | `MU.scrivi(doc, clip, note, dove=…)` — **una sola chiamata per kit e synth.** Non dichiarare il tipo di clip: lo deduce, e la forma delle note fa il resto. Un **dict** (da `MU.melodia()` o `MU.accordi()`) diventa una riga per altezza, solo su synth. Una **lista** (da `MU.passi()`) va su una riga sola e vuole `dove=`: il **nome del drum** su un kit, l'**altezza** su un synth. Su synth chiama da sé `fit_clip_scroll_to_notes()`, quindi le note non restano invisibili |
| **togliere qualcosa** | `MU.togli(doc, bersaglio, quando=…)` — riconosce da sé il bersaglio: **strumento** (via lui e le sue clip), **clip** (via lei, e rinumera i `clipCode`), **noteRow di kit** (la svuota, perché una riga per drum deve esserci sempre), **noteRow di synth** (la toglie). `quando=(da, a)` in tick su uno strumento toglie **solo le istanze d'arranger in quel tratto** e lascia stare tutto il resto: è la differenza fra *«togli il basso»* e *«leva il basso nella seconda metà»* |
| un drum dal kit | `K.remove_drum(doc, kit, nome)` — diverso da `MU.togli(riga)`: toglie il drum dallo **strumento**, quindi cambia **tutte** le clip di quel kit, e rinumera i `drumIndex`. `MU.togli` su una riga fa tacere quel drum **in quella clip sola** |
| **trasporre** | `MU.trasponi(doc, bersaglio, semitoni=…)` oppure `gradi=…`, mai tutti e due. `semitoni=12` è un'ottava, sempre; `gradi=2` sale di due gradi **nella scala della song**, e una nota fuori scala conserva il suo scarto invece di essere schiacciata dentro. Bersaglio come in `togli`: strumento, clip o riga. Su un **kit** intona i drum (`transpose` sugli osc) e quindi cambia **tutte** le clip di quel kit — il rapporto lo dice in `condiviso`; `gradi=` lì è un errore, perché un drum non ha gradi |
| **spostare nel tempo** | `MU.sposta(doc, clip, tick=…)` oppure `battute=…`. **Rifiuta** di mandare note prima di zero e dice quanto spazio c'è, invece di scartarle |
| **allungare ripetendo** | `MU.repeat(doc, clip, volte)` — la clip diventa `volte` più lunga e il materiale si ripete; le **durate non cambiano** |
| **cambiare il rate** | `MU.stretch(doc, clip, fattore)` — scala note **e** lunghezza della clip insieme. Sopra ci sono i due nomi musicali: `MU.double_time(doc, clip)` tiene la battuta e raddoppia l'articolazione (8 ottavi → 16 sedicesimi), `MU.half_time(doc, clip)` **raddoppia la clip** (8 ottavi → 8 quarti). L'asimmetria è voluta |
| arrangiamento | `A.place(doc, strumento, clip, pos=…, length=…)` poi `A.fit_view(doc)` |
| variazione indipendente | `A.place_unique(...)` — la clip "bianca" |
| suono e mix | `MU.applica_verbo(doc, nodo, 'piu scuro')` — verbi in `MU.VERBI_RELATIVI` (spostano di tanto) e `MU.VERBI_ASSOLUTI` (portano a un valore fisso, `forza` ignorata); elenco completo con `MU.verbi_disponibili()` |
| controllo che blocca | `MU.verifica(doc)` |
| controllo che informa | `MU.avvertenze(doc)` |
| destinazione sulla SD (scrittura) | `MU.destinazione(nome, versione, cartella)` — **mai un percorso scritto a mano** |
| sorgente sulla SD (lettura) | `MU.origine(nome, cartella)` — nessuna restrizione, legge ovunque |
| scrivere | `write_file(doc, path, FormatTable.load('out/format_table.json'))` |

## Trasferimento

Il percorso remoto si costruisce sempre con `musica.destinazione()` per
scrivere, `musica.origine()` per leggere — mai a mano, vedi regola 5.
Esempio: `MU.destinazione('house', 2)` produce `/SONGS/DelugePal/HOUSE02.XML`;
`MU.origine('Antrop.XML', 'SONGS')` produce `/SONGS/Antrop.XML`, una song
personale dell'utente fuori da `DelugePal`.

```bash
# leggere una song dell'utente, per partire da materiale esistente
.venv/Scripts/python.exe tools/dsysex.py --in "Deluge 0" --out "Deluge 1" get "/SONGS/Antrop.XML" locale.XML

# ricaricare l'ultima versione generata, prima di modificarla (regola 1)
.venv/Scripts/python.exe tools/dsysex.py --in "Deluge 0" --out "Deluge 1" get "/SONGS/DelugePal/HOUSE01.XML" locale.XML

# scrivere la versione successiva
.venv/Scripts/python.exe tools/dsysex.py --in "Deluge 0" --out "Deluge 1" put locale.XML "/SONGS/DelugePal/HOUSE02.XML"
```

Le porte vanno sempre indicate. `put` rilegge e confronta gli hash da sé.

**`dsysex` non ha un comando per creare cartelle.** Le quattro
`<CARTELLA>/DelugePal/` esistono già sulla SD (create a mano). Se in futuro
servisse una destinazione nuova, va preparata allo stesso modo — spostando
la SD — prima di poterci scrivere: non c'è modo di farlo al volo via SysEx.

## Quando qualcosa va storto

| caso | cosa fare |
|---|---|
| `verifica()` non vuota | **non caricare**, riferire il problema in chiaro |
| `avvertenze()` non vuota | caricare comunque, ma dire cosa non si vedrà e perché |
| Deluge non collegato (`ping` non risponde) | scrivere il file locale e dirlo; non fingere che sia salito |
| il nome remoto esiste già | incrementare la versione, mai forzare |
| `destinazione()` solleva `ValueError` | il nome tentava di uscire dalla sottocartella, la cartella non è una delle quattro, o la versione ha superato 99: non aggirare l'errore, correggere l'argomento |
| serve leggere qualcosa fuori da `DelugePal` | è normale: `origine()` non ha restrizioni, è `destinazione()` (solo in scrittura) ad averle |
| il campione di una clip audio non è sulla SD | `audio.wav_frames` non può leggerlo: chiedere il percorso, non indovinare le posizioni |
| verbo di suono sconosciuto | dire quali esistono (`MU.verbi_disponibili()`) |
| il dispositivo rifiuta il file | è un difetto nostro, non un mistero del formato: bisezionare da un file che funziona, un fattore per volta |

## Altre skill

| per | skill |
|---|---|
| convenzioni di genere, teoria, progressioni | `music-composer` — **verificare prima che il genere ci sia**: reggae e dub NON ci sono |
| sintesi, filtri, timbro | `dsp-recipes` |
| **come si compone davvero in un genere** | `docs/MUSICA.md` — pattern per genere, velocity groove, e le correzioni ricevute |

### `music-composer`: due difetti trovati e RIPARATI il 16 agosto 2026

Trovati leggendo il sorgente e confrontando l'output con `mido`, **riparati
in loco** in `~/.claude/skills/music-composer/scripts/`. È una
skill globale dell'utente, non roba di questo repo: se un giorno viene
reinstallata o aggiornata, le riparazioni spariscono e vanno rifatte.

| pezzo | stato |
|---|---|
| `references/*.md` | sempre andati bene — è il grosso della skill. Unica avvertenza: **reggae e dub non ci sono** in `genres.md` |
| `DRUM_PATTERNS` | **aggiunti `reggae`, `reggae_rockers`, `reggae_steppers`** — vedi sotto |
| `generate_melody.py` | andava già bene |
| `generate_chords.py`, maggiori | andava già bene |
| `generate_drums.py` | **era rotto, ora funziona** |
| `generate_chords.py`, minori | **era irraggiungibile, ora c'è `--scale minor`** |

**Il difetto della batteria.** Righe 110-115: i due rami dell'`if` mettevano
entrambi `delay = 0` e `absolute_step` veniva calcolato e buttato. Siccome i
tempi MIDI sono **delta**, ogni nota partiva alla fine della precedente: ogni
pattern usciva come una fila di sessantaquattresimi raggruppati per
strumento, senza simultaneità e senza silenzi — cioè senza le due cose di cui
è fatta una batteria. Riparato aggiungendo `add_notes_absolute()` a
`midi_utils.py` (posizioni assolute → delta corretti) e usandola. Corretto
anche l'accento, che era fisso a `step % 4` e sbagliava i pattern in terzine:
ora `steps_per_beat = steps_per_bar // 4`.

**Il difetto degli accordi.** `parse_roman_numeral` sapeva già gestire il
minore, ma non esisteva il flag `--scale` e il chiamante non lo passava mai:
i gradi uscivano sempre dalla scala maggiore, quindi `VI` in sol minore dava
**mi** invece di **mi bemolle**. Aggiunto `--scale major|minor` (default
`major`, quindi nulla cambia se non lo si chiede).

⚠️ Le progressioni predefinite sono scritte **relative al maggiore**, con le
alterazioni esplicite (`andalusian` è `i - bVII - bVI - V`): con `--scale
minor` verrebbero abbassate due volte. Lo script ora se ne accorge, avvisa e
resta in maggiore.

⚠️ Il `delay = 0 if i == 0 else 0` c'è anche in melodia e accordi, ed è stato
**lasciato**: per materiale sequenziale senza pause il delta del `note_off`
precedente porta già il tempo, quindi lì non è un difetto. È un limite
latente — non saprebbe esprimere una pausa — non un bug.

**I tre stili reggae aggiunti.** `DRUM_PATTERNS` accettava solo `0`/`1` e
ricavava le velocity da «sul movimento / fuori dal movimento»: basta per un
quattro-quarti, non per un groove il cui carattere sta nelle dinamiche.
Esteso in modo retrocompatibile — **un valore sopra 1 è la velocity di quel
passo** e vince sull'accento automatico; gli stili preesistenti usano solo 0 e
1, quindi non cambiano. Con questo il one drop ha i fantasmi (40) accanto
all'accento (108), che con 0/1 era impossibile.

    reggae            cassa   ........X.......    solo il 3
    reggae_rockers    cassa   x...x...X...x...    tutti i movimenti
    reggae_steppers   cassa   X.x.x.x.X.x.x.x.    tutti gli ottavi
    (tutti e tre)     rim     ..o.....X.....o.    cross-stick sul 3, fantasmi
                      hat     ..x.x.x.x.x.x...    ottavi, l'UNO vuoto
                      aperto  ..............x.    porta dentro la battuta dopo

Il rullante è un **cross-stick** (`rim`, GM 37), non un backbeat pieno: in
roots è quello il suono. Lo *skank* non c'è perché non è una percussione — è
l'accordo in levare di chitarra e organo.

## Importare MIDI

`from delugexml import midi as MI` — lettore di Standard MIDI File **senza
dipendenze**, validato nota per nota contro `mido`. Serve per le librerie
libere di loop divisi per genere e per i **groove template**, che sono file
MIDI ordinari e portano timing e velocity di un groove suonato.

| per | usare |
|---|---|
| vedere cosa c'è in un file | `MI.racconta(path)` |
| note melodiche | `MI.melodia(path)` → `(altezza -> note, rapporto)`, la stessa forma di `MU.melodia()` |
| percussioni | `MI.batteria(path)` → `(nome GM -> note, rapporto)`, da dare a `MU.scrivi(..., dove=nome)` |

**Il rapporto va letto.** Un MIDI ha i suoi PPQ e il Deluge ne ha 96 per
movimento: se non sono in rapporto intero le posizioni si arrotondano, e lì
se ne va la micro-tempistica che rende utile un groove template. `Conversione`
dice quante note ha arrotondato e di quanto.

Le altezze **coincidono**: il numero di nota MIDI è già la `y` del Deluge,
nessuno scarto di ottava. Verificato, non supposto.

## Quando qualcosa non si vede sul dispositivo

Quattro volte su quattro il contenuto era giusto e mancava uno stato di
vista: `yScrollSongView`, `beingEdited`, lo scroll della clip, la finestra
dell'arranger. Prima di sospettare il dato, controllare la vista — e in ogni
caso **misurare con una coppia controllata**, non dedurre.
