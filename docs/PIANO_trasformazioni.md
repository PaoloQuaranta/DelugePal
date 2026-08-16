# Piano — le trasformazioni musicali

**Data:** 15 agosto 2026
**Copre:** la lacuna 1 di `HANDOFF.md` §«Il prossimo lavoro» (era la 2)
**Stato:** implementato e **verificato sul dispositivo** il 16 agosto 2026.
609 test verdi. Vedi `HANDOFF.md` §6-quinquies e `docs/FINDINGS.md` §6-septies.

> Quello che segue è il piano come è stato approvato. Cosa è cambiato dopo:
>
> - **§3 è stata verificata e non è più un'ipotesi**: `transpose` sugli
>   oscillatori funziona, e si sente. Era l'unico punto del lavoro che
>   poggiasse su un attributo mai messo alla prova.
> - **§3.0-bis era SBAGLIATA**, ed è stata riscritta. La riga MIDI di un kit
>   non è un `<sound>` con un `<midiOutput>` figlio e l'altezza in
>   `noteForDrum`: è un `<midiOutput>` **fratello** dei `<sound>` dentro
>   `<soundSources>`, con l'altezza in **`note`**. L'ha mostrato l'unico
>   esemplare esistente, `refs/songs/TRASF401MIDI.XML`, fatto salvare dal
>   dispositivo. Vedi `FINDINGS.md` §6-septies, che tiene anche la lezione di
>   metodo.
> - `sposta()` e `half_time()` non sono state provate a parte sul dispositivo:
>   usano `map_notes` e `stretch`, che `double_time` esercita entrambe.

---

## 0. Perché

`applica_verbo` copre timbro e mix, ma non esiste **trasponi**, **raddoppia**,
**dimezza**, **sposta di una battuta**, **più veloce**. *«Alza il basso di
un'ottava»* è una richiesta ordinaria quanto *«più scuro»*, e oggi vuole una
funzione che non c'è.

Le cinque parole non sono cinque operazioni: `trasponi` e `sposta` sono
univoche, mentre `raddoppia`, `dimezza` e `più veloce` vogliono dire due cose
diverse ciascuna. Il piano le scioglie in nomi non ambigui.

---

## 1. Le operazioni

```python
MU.trasponi(doc, bersaglio, semitoni=…)   # oppure gradi=…
MU.sposta(doc, bersaglio, tick=…)         # oppure battute=…
MU.repeat(doc, clip, volte)               # 1 battuta -> 2, materiale ripetuto
MU.stretch(doc, clip, fattore)            # note e lunghezza clip, insieme
MU.double_time(doc, clip)                 # = stretch(0.5) + repeat(2)
MU.half_time(doc, clip)                   # = stretch(2)
```

`stretch` è la primitiva del tempo; `repeat`, `double_time` e `half_time` sono
i nomi musicali costruiti sopra. Su una clip di una battuta con otto ottavi:

| chiamata | risultato |
|---|---|
| `repeat(2)` | due battute, gli otto ottavi suonano due volte, durate invariate |
| `double_time()` | resta **una** battuta, gli ottavi diventano sedici sedicesimi |
| `half_time()` | diventa **due** battute, gli otto ottavi diventano otto quarti |
| `stretch(1.5)` | il caso generale, per chi vuole il numero esatto |

L'asimmetria fra `double_time` (la clip resta) e `half_time` (la clip
raddoppia) non è una svista: in metà tempo un pattern di una battuta ne occupa
due davvero, mentre in doppio tempo lo si suona due volte per riempire la
battuta. È quello che fa un musicista.

Il bersaglio si riconosce **per identità**, come in `togli`: strumento, clip o
`noteRow`. Le operazioni sul tempo prendono una clip.

---

## 2. Trasporre un synth: si muovono le righe

Le righe di una clip di synth **sono** le altezze, quindi si cambia `y`.

- `semitoni=12` alza di un'ottava, sempre e ovunque
- `gradi=2` sale di due gradi **nella scala della song** — che è una proprietà
  della song e non della clip, quindi si legge con `get_scale()`

### 2.1 Le note fuori scala non si perdono

Trasporre per gradi conserva lo **scarto cromatico dal grado**: una nota un
semitono sopra il terzo grado resta un semitono sopra il *nuovo* terzo grado.

    pc      = (y - root) % 12
    grado   = l'ultimo intervallo <= pc          scarto = pc - intervallo
    nuovo_y = root + ottava*12 + intervalli[grado + n] + scarto

`snap_to_scale()` esiste già ma **qui sarebbe sbagliata**: schiaccerebbe in
scala le note che il corpus dice espressamente di rispettare — `Progsong.XML`
ne ha 315, e `FINDINGS.md` §6 dedica una sezione all'errore di averle
considerate un difetto.

### 2.2 Le collisioni esistono solo nel modo diatonico

In semitoni la trasposizione è **biiettiva**: due righe non possono finire
sulla stessa altezza. Per gradi **sì**, ovunque il passo fra due gradi sia di
un semitono — in una scala maggiore, fra il terzo e il quarto grado: una nota
con scarto 1 dal grado *n* e una con scarto 0 dal grado *n+1* atterrano
insieme.

Le righe che collidono vanno **fuse** (le note dell'una si aggiungono
all'altra) e il rapporto deve dichiararlo. Non è un caso di laboratorio.

---

## 3. Trasporre un kit: si muove il suono

Un kit **si trasporta eccome**, e non toccando i `drumIndex`: l'intonazione di
un drum vive in **`transpose`**, in semitoni, sugli `<osc1>`/`<osc2>` del suo
`<sound>`. Vale sia per i drum a campione sia per quelli sintetizzati, che sono
lo stesso nodo.

Confermato dal manuale, che è la fonte di grado più alto — voce TRANSPOSE del
menu di `osc1`, `osc2` e dei modulatori FM:

> `TRANSPOSE — Semitones + cents for adjustment`

Osservato nel corpus (204 oscillatori di drum che portano `transpose` o
`cents`): valori da −7 a +8.

### 3.0 Non tutte le righe di un kit hanno un'altezza

Il manuale dice che un kit può contenere righe di quattro tipi:

> «A synth, MIDI or CV row can be added in the kit view by pressing
> [AUDITION]+[SYNTH], [AUDITION]+[MIDI], [AUDITION]+[CV]»

E nei file si vedono, dentro `<soundSources>`:

| tag | quanti | come si intona |
|---|---|---|
| `<sound>` (campione o sintetizzato) | 3928 | `transpose` sugli `<osc>` |
| `<sound>` con `<midiOutput>` attivo | 0 nel corpus | `noteForDrum` — **ipotesi**, §3.0-bis |
| `<gateOutput channel="…">` | 12 | **niente**: un gate non ha altezza |

Le righe di gate vengono **saltate e dichiarate nel rapporto**. Non è un
errore — è un fatto sui gate — e chi ha chiesto la trasposizione deve sapere
che una riga non l'ha seguita.

### 3.0-bis I drum MIDI — ⚠ QUESTA SEZIONE ERA SBAGLIATA

> **Tenuta com'era, perché l'errore vale più della conclusione.** La forma vera
> è in `FINDINGS.md` §6-septies: un `<midiOutput>` **fratello** dei `<sound>`
> dentro `<soundSources>`, con l'altezza nell'attributo **`note`** — non un
> `<sound>` col suo `<midiOutput>` figlio, e non `noteForDrum`.
>
> Il ragionamento qui sotto è giusto nella prima metà e sbagliato nella
> seconda, ed è per questo che è istruttivo.


`<midiOutput>` è presente su ogni `<sound>` ma vale `channel="255"
noteForDrum="255"` in **tutti e 1180 i casi del corpus**, cioè disattivato.

**L'assenza qui non dice niente sul formato.** Il corpus è fatto delle song di
una persona sola, che quella funzione non l'ha ancora usata: è un campione
parziale, non una prova che la cosa non esista. Il manuale dice il contrario, e
la riga MIDI in un kit potrà servire.

Cambia anche il peso della regola «mai inventare tag, parametri o strutture»:
`noteForDrum` **è** un attributo osservato, 1180 volte. Non è una struttura
inventata — è una struttura nota su un valore mai visto. Quindi si implementa:

    midiOutput con channel != 255  ->  noteForDrum += semitoni, limitato a 0-127
    noteForDrum == 255            ->  nessuna nota assegnata, non si tocca

**Resta un'ipotesi finché non la si guarda sul dispositivo**, e va detto sia
qui sia nel rapporto della funzione. Il primo esemplare di kit con una riga
MIDI chiude il punto: si fa scrivere dal Deluge e si confronta.

Il codice sceglie in quest'ordine — MIDI attivo, poi oscillatori, poi nulla —
così una forma futura che non conosciamo cade nel ramo «saltata e dichiarata»
invece di far esplodere la trasposizione di un kit misto.

### 3.1 L'attributo va aggiunto, quasi sempre

| forma | quanti |
|---|---|
| `cents=32`, **`transpose` assente** | 144 |
| `transpose=0`, `cents=0` | 47 |

**144 oscillatori su 204 non hanno affatto `transpose`**: trasporre deve
aggiungerlo. È comunque una forma osservata, perché 47 lo scrivono esplicito.

### 3.2 `cents` non si tocca

`cents` è il fine tuning, in centesimi di tono. La trasposizione in semitoni
non ne ha bisogno, e il corpus mostra **due codifiche in circolazione** dello
stesso "nessuna alterazione" — 32 in una, 0 nell'altra.

Non si prova a datarle dalle versioni di firmware: `HANDOFF.md` §7 spiega
perché quella strada non funziona (i valori non toccati vengono riportati
identici a ogni risalvataggio, e `firmwareVersion` registra solo l'ultimo).
Resta un punto aperto, non una conclusione.

### 3.3 La portata segue ciò che nomini

Intonare un drum cambia lo **strumento**, quindi **tutte le clip di quel kit**.
È la stessa distinzione fra `kit.remove_drum` e lo svuotare una riga:

    una noteRow di kit   ->  intona QUEL drum
    una clip o un kit    ->  intona TUTTI i suoi drum

In entrambi i casi il rapporto dichiara che il kit è condiviso, perché il
risultato si sente anche in clip che non sono state nominate.

### 3.4 `gradi=` su un kit è un errore

Un drum non ha gradi di scala. Solo `semitoni=`, e l'errore lo dice.

---

## 4. Il resto

- **`sposta` rifiuta** di mandare note prima di zero, invece di scartarle in
  silenzio, e dice quanto spazio c'è. Scartare musica senza dirlo è il
  comportamento peggiore fra quelli possibili.
- le note che finiscono **oltre la fine della clip** sono già coperte da
  `avvertenze()` (`notes_beyond_clip_end`): si informa, non si blocca.
- **`fit_clip_scroll_to_notes()`** in coda a ogni trasposizione di synth, o le
  note restano scritte e fuori dalla finestra visibile — la famiglia di
  difetti che in questo progetto è costata più di tutte.
- `repeat` e `stretch` moltiplicano anche la **lunghezza propria delle righe**
  dove c'è (`length` sulla `<noteRow>`): 1 clip su 318 nel corpus, `Qbix.XML`,
  rara ma reale. Senza, il poliritmo si rompe in silenzio.
- `notes.encode()` **ordina già per posizione**, quindi spostare e ripetere non
  richiedono di riordinare a mano.

---

## 5. Test

In `tests/test_all.py`, nello stile esistente:

- ottava su e ottava giù riporta le righe esattamente dov'erano
- trasposizione per gradi in re minore: i gradi si muovono, e una nota fuori
  scala conserva il suo scarto
- la collisione diatonica fonde due righe e lo dichiara
- `semitoni` su una clip di kit muove `transpose` sugli osc, e lo aggiunge dove
  manca
- una riga `<gateOutput>` viene saltata e dichiarata, senza far fallire il resto
- un drum con `<midiOutput>` attivo muove `noteForDrum`, e resta nei limiti
  0-127; con `noteForDrum=255` non viene toccato
- `gradi` su un kit è rifiutato con la sua ragione
- `sposta` all'indietro oltre lo zero è rifiutato, e dice di quanto
- `repeat(2)` raddoppia lunghezza clip, note, e la lunghezza propria delle
  righe di `Qbix.XML`
- `double_time` lascia la lunghezza della clip e raddoppia il numero di note
- `half_time` raddoppia la lunghezza e non il numero di note
- round-trip: trasformare, serializzare, rileggere, stesso significato
- ogni trasformazione lascia il file accettato da `verifica()`

## 6. La verifica sul dispositivo

Una song generata e la stessa trasposta di un'ottava e in double time, sul
metodo della coppia già usato due volte.

**Il kit è la parte da guardare e sentire**, non solo da leggere: `transpose`
sugli osc è un attributo *osservato* nel corpus ma mai messo alla prova da
questo progetto. Che il Deluge lo applichi come semitoni su un drum a campione
è un'ipotesi finché non lo si sente.

E resta il punto aperto della riga MIDI in un kit (§3.0-bis): il codice c'è,
la prova no. Si chiude facendo salvare dal Deluge un kit con una riga MIDI —
`[AUDITION]+[MIDI]` sulla riga, secondo il manuale — e guardando che forma ha
davvero `<midiOutput>` quando è in uso.
