# Deluge Pal — lo strato in linguaggio naturale

**Fase 7 del piano in `docs/PROSSIMI_PASSI.md`. Progetto approvato il 14 agosto 2026.**

---

## 1. Cosa deve succedere

Un ciclo, non un comando:

```
prompt  →  [libreria]  →  XML  →  SysEx  →  l'utente apre e ascolta
                                                     ↓
        ricarica come      ←  modifica  ←  «il basso è troppo statico»
        versione nuova          ↑
                           RISCARICA dal Deluge prima di toccare
```

Due porte d'ingresso, stesso percorso:

- **da zero**: si parte da `TEMPL0.XML` e si costruisce tutto
- **da una song esistente**: si parte da un file dell'utente

Oltre alla composizione: **sound design** e **mix**.

### La fonte della verità è il file sul Deluge

Prima di ogni modifica si **riscarica la song dal dispositivo**. L'utente la
apre, l'ascolta, e può averci messo mano — spostato una clip, cambiato un
suono. Lavorare su una copia locale cancellerebbe quel lavoro senza
accorgersene.

Questo esclude una "ricetta" dichiarativa come stato parallelo: sarebbe un
secondo stato da tenere allineato, e si disallineerebbe alla prima modifica
fatta sul dispositivo.

### Versioni invece di sovrascritture

`dsysex put` non sovrascrive mai. Ogni iterazione sale con un nome nuovo:
`HOUSE01`, `HOUSE02`, … Non è un ripiego — è la convenzione del Deluge stesso,
che numera i sotto-slot, e lascia tornare a una versione che piaceva.

---

## 2. Architettura: tre livelli

| livello | cosa fa | stato |
|---|---|---|
| **libreria** `tools/delugexml/` | l'unica cosa che scrive XML | esiste, 300 test |
| **strato musicale** `tools/delugexml/musica.py` | traduce fra lingua musicale e chiamate alla libreria | **da scrivere** |
| **skill** `.claude/skills/deluge-pal/` | il protocollo che il modello segue | **da scrivere** |

La separazione è ciò che rende il sistema sicuro: nessuna funzione dello
strato musicale accetta o produce XML, e la skill vieta di scriverlo a mano.

Motivazione dalla storia del progetto: due file generati sono stati rifiutati
dal dispositivo — `kitParams` scritto come `soundParams`, e il `<params>`
audio trascritto a mano da un'anteprima troncata (crash E365). Entrambi
passavano ogni controllo sintattico. Vedi FINDINGS §6-quater e §6-quinquies.

---

## 3. Lo strato musicale: `musica.py`

Quattro responsabilità. Nessuna sa cosa sia un attributo XML.

### 3.1 Raccontare

```python
def racconta(doc) -> str
```

Descrive una song in termini musicali: tempo, scala, per ogni traccia le clip
con le note come nomi di altezza e durate, l'arrangiamento in battute, i
parametri di suono salienti in unità del display.

**È il pezzo che rende possibile «proponi e correggo»**, e serve dopo ogni
riscaricamento per sapere cosa c'è davvero prima di toccarlo. Poggia su cose
già esistenti: `song.clips`, `arranger.arrangement`, `midicv.describe`,
`audio.describe`, `sound.read_all`.

### 3.2 Scrivere note

```python
def altezza(nome: str) -> int        # 'do4' o 'C4' -> 60
def note(altezze, ritmo, ...) -> list[Note]
def passi(pattern: str, ...) -> list[Note]
```

**Altezze**: nomi italiani (`do re mi fa sol la si`) e inglesi (`C D E F G A
B`), con alterazione (`fa#`, `mib`) e ottava. Convenzione: `do4` = `C4` = 60,
quella MIDI standard. `[OSS]` da confrontare con ciò che mostra il display del
Deluge.

**Ritmo percussivo**: una stringa di passi, uno per sedicesimo, che mappa
direttamente sulla griglia del Deluge — 16 colonne per battuta:

```
kick   x...x...x...x...
rim    ....x.......x...
hat    x.x.x.x.x.x.x.x.
```

**Ritmo melodico**: sequenza di altezze più una durata (`1/8`, `1/4`), oppure
posizioni esplicite in movimenti.

### 3.3 Verbi di suono e mix

```python
VERBI_RELATIVI = {...}               # «più scuro»: sposta di passo × forza
VERBI_ASSOLUTI = {...}               # «al centro»: porta a un valore fisso
def applica_verbo(doc, nodo, verbo, forza=1) -> dict[str, object]
def verbi_disponibili() -> list[str]
```

> **Cambiato in implementazione.** La spec prevedeva una tabella sola, `VERBI`,
> in cui «al centro» era scritto come passo `0` con significato speciale «vai
> al centro». Una revisione l'ha bocciato: `0` significava due cose, `forza`
> veniva ignorata senza dirlo, e il valore centrale ha senso solo per il `pan`
> — chi avesse aggiunto `('volume', 0)` intendendo «nessuna variazione» avrebbe
> ottenuto un salto silenzioso. Le due tabelle separate fanno sì che il dato
> dichiari cosa intende, invece di affidarlo a un commento.

`sound.set` lavora già in unità del display 0-50; qui manca solo la mappa
dalle parole ai parametri:

| verbo | parametro | direzione |
|---|---|---|
| più scuro / più chiuso | `lpfFrequency` (id 24) | −8 |
| più brillante / più aperto | `lpfFrequency` | +8 |
| più forte | `volume` (id 2) | +5 |
| più riverbero | `reverbAmount` (id 47) | +8 |
| a sinistra / a destra | `pan` (id 23) | −10 / +10 |
| più largo | `structure.set_unison(detune=…, spread=…)` | +detune |

Nota: `pan` è **posizione**, non larghezza. «Più largo» su un suono mono si
ottiene con l'unison (detune e spread), non spostando il pan.

**«Più scuro» non è un fatto, è gusto.** Perciò la tabella è scritta e
leggibile, non un'euristica nascosta, e ogni applicazione **riporta quale
parametro è stato mosso e di quanto**, così l'utente può scavalcarla.

Sound design strutturale (forme d'onda, modo di sintesi, LFO, unison) passa
per `structure.py`, che valida già i valori contro quelli osservati nel corpus.

### 3.4 Il cancello

```python
def verifica(doc) -> list[str]
```

Compone i controlli già esistenti:

- `song.check_clip_types` — le tre dichiarazioni di tipo devono concordare
- `song.same_section_conflicts` — due clip dello stesso strumento in una scena
- `arranger.check` — indici, sovrapposizioni, clip di altri strumenti
- `midicv.check` — canali, conflitti di suffisso
- `audio.check` — tracce risolte, posizioni sensate
- `kit.check_indices` — `drumIndex` coerenti

**Nessun file sale sul Deluge se `verifica()` non è vuota.** È la regola che
avrebbe fermato entrambi i crash di questa sessione.

---

## 4. La skill: `.claude/skills/deluge-pal/SKILL.md`

Il protocollo. Cinque regole, in ordine di importanza:

1. **Riscarica prima di modificare.** La song sul Deluge è la verità.
2. **Mai scrivere XML.** Mai costruire nodi di formato a mano, mai trascrivere
   valori da un file: solo chiamate alla libreria. Le costanti si generano da
   codice e si confrontano con un test (`test_costanti_catturate`).
3. **`verifica()` prima di ogni caricamento.** Sempre, senza eccezioni.
4. **Raccontare cosa è cambiato**, in termini musicali e con i valori esatti
   dei parametri toccati. Un'operazione silenziosa non è correggibile.
5. **Nomi versionati.** Mai sovrascrivere.

### Skill da invocare

| per | skill |
|---|---|
| convenzioni di genere, teoria, progressioni | `music-composer` |
| sintesi, filtri, timbro | `dsp-recipes` |
| come suona la roba dell'utente | `docs/MUSICA.md` (nel progetto) |

`music-composer` è oggi *scoped* a `D:\Webarmonium`: va copiata in
`~/.claude/skills/` per valere anche qui. Le sue schede di genere sono un
**pavimento, non un soffitto** — danno gli intervalli di tempo e gli strumenti
tipici, non come si muove davvero un groove. I suoi `scripts/*.py` producono
file MIDI e **non si usano**: il formato di destinazione è un altro.

### `docs/MUSICA.md`

Parte quasi vuoto e cresce a ogni correzione dell'utente. Stessa disciplina del
resto del progetto: si scrive solo ciò che è stato verificato, e si segna
`[OSS]` ciò che è supposto. È qui che finisce la conoscenza che nessuna skill
generica ha — come suona un basso *suo*, quali preset usa per cosa.

---

## 5. Flusso di una richiesta

```
1. capire l'intento, chiedere solo se ambiguo
2. se si parte da una song: dsysex get  →  racconta()  →  dire cosa c'è
3. costruire con chiamate alla libreria
4. verifica(doc)          →  se non vuota: NON caricare, riferire
5. write_file()
6. dsysex put <NOME><NN>  →  verifica per hash, già fatta dal tool
7. raccontare cosa è stato scritto, in termini musicali e con i valori
8. aspettare il giudizio d'ascolto
```

Il passo 4 è il cancello; il passo 7 è ciò che rende possibile il passo 8.

---

## 6. Errori

| caso | comportamento |
|---|---|
| `verifica()` non vuota | non si carica, si riferisce il problema in chiaro |
| Deluge non collegato | si scrive il file locale e lo si dice |
| nome remoto già esistente | si incrementa la versione |
| il campione di una clip audio non esiste sulla SD | `wav_frames` non può leggerlo: si chiede il percorso invece di indovinare |
| verbo di suono sconosciuto | si dice quali esistono, non si tira a indovinare |

---

## 7. Test

**Unitari** su `musica.py`, senza dispositivo:

- altezze: `do4`→60, `C4`→60, `fa#3`, `mib5`, nomi inventati rifiutati
- passi: `x...x...x...x...` → 4 note ai movimenti giusti; lunghezze diverse da 16 rifiutate
- `racconta()` su file noti del corpus, con valori attesi
- `verifica()`: zero falsi positivi su tutti i 139 file scritti dal dispositivo
- verbi: ogni voce della tabella tocca un parametro che esiste in `param_ids`

**Per mutazione**, come `test_costanti_catturate`: un test che non fallisce mai
non protegge niente.

**Di accettazione**: il ciclo completo sul dispositivo. Generare una song da
prompt, caricarla, aprirla, chiedere una modifica, ricaricarla. Chiude sullo
schermo del Deluge, non sul round-trip — la regola che vale in tutte le fasi.

---

## 8. Fuori ambito

- **import di file MIDI**: il ponte MIDI → clip Deluge è un'altra fase
- **composizione algoritmica** (Markov, L-system): serve per «sorprendimi», non
  per il ciclo principale
- **generazione di campioni audio**: le clip audio referenziano file esistenti
- **ricetta dichiarativa**: valutata e scartata, vedi §1

---

## 9. Punti aperti

- La tabella dei **verbi** nasce piccola e per forza arbitraria. Cresce dalle
  correzioni dell'utente, e ogni voce va segnata come gusto, non come fatto.
- La convenzione **`do4` = 60** va confrontata con ciò che mostra il display.
- **Sound design** è l'area meno verificata sul dispositivo: `structure.py`
  esiste ma è poco esercitata. Il ciclo «carica e ascolta» servirà anche a
  validare la libreria stessa.
- I **colori di sezione** restano non mappati (FINDINGS §6-ter): se l'utente
  dice «fai la scena B magenta», per ora non si può.
