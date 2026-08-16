# Piano — la rimozione, e la chiamata sola per scrivere note

**Data:** 15 agosto 2026
**Copre:** le lacune 1 e 3 di `HANDOFF.md` §«Il prossimo lavoro»
**Stato:** implementato e **verificato sul dispositivo** il 15 agosto 2026.
547 test verdi. Vedi `HANDOFF.md` §6-quater e `docs/FINDINGS.md` §6-sexies.

> Quello che segue è il piano come è stato approvato, tenuto com'era. Due punti
> sono cambiati strada facendo, ed è giusto che si veda:
>
> - **§6 non ha richiesto codice.** `arranger.check()` aveva già il controllo
>   dell'indice appeso, e `verifica()` lo chiamava già. È stato aggiunto solo
>   un test che lo lega alla rimozione, perché resti legato anche a chi un
>   domani toccasse il cancello.
> - **Svuotare una riga di kit non ha richiesto una primitiva nuova**:
>   `write_notes(riga, [])` toglie già l'attributo delle note e lascia gli
>   indici contigui. Misurato prima di scriverne una che non serviva.

---

## 0. Perché

Il ciclo di Deluge Pal è «l'utente ascolta e dice cosa cambiare», e **metà di
quello che una persona dice è sottrattivo**: *«togli il piano»*, *«leva quel
pattern nella seconda metà»*, *«il basso non ci va»*. Oggi in tutta la libreria
esistono `kit.remove_drum` e `Node.remove` (un attributo) e nient'altro: non
c'è modo di eliminare una clip, uno strumento, una `noteRow`, un blocco
d'arrangiamento. *«Rifai il basso»* funziona, *«togli il basso»* no.

Insieme va la lacuna 3, perché abita lo stesso strato: scrivere note in una
clip richiede oggi di comporre tre primitive **con un idioma diverso per kit e
per synth**, ed è esattamente ciò che ha prodotto il primo difetto della prova
d'accettazione.

---

## 1. Il censimento dei riferimenti

Prima di progettare, la domanda che decide tutto: **cosa punta a cosa, per
posizione ordinale?** Misurato sulle 36 song di `refs/songs`, non dedotto.

### Verso una clip: due riferimenti, e nient'altro

| dove | cosa |
|---|---|
| `clipInstances` sugli strumenti | terne esadecimali; `clipCode` è un indice ordinale, il bit 31 sceglie la lista |
| `yScrollSongView` sul `<song>` | quale clip sta alla riga 0 dello schermo |

Nessun altro. Il censimento ha passato al setaccio ogni attributo il cui nome
contenesse `index`, `code`, `slot`, `count`, `num`, `current`, `selected`,
`section`, `scroll`, e ogni nodo scalare con gli stessi: l'**unico**
riferimento ordinale in nodo-testo di tutto il corpus è `<selectedDrumIndex>`,
che riguarda i kit e che `kit.remove_drum()` già aggiorna.

### Verso uno strumento: nessun ordinale

Le clip risolvono lo strumento **per nome, slot o canale** (`instrument_of()`,
quattro forme ancora in circolazione), mai per posizione. L'unico ordinale che
conta gli strumenti è `yScrollArrangementView`.

Conseguenza: togliere uno strumento non richiede nessuna rinumerazione, ma
lascia **appese** le clip che lo nominano. Vanno tolte con lui.

---

## 2. La superficie

Due verbi in `musica.py`, entrambi con un **rapporto di ritorno** — come
`applica_verbo`, che riferisce cosa ha mosso. I verbi smistano; l'operazione
vera sta nelle primitive di `song.py` / `arranger.py`, testate una per una.

```python
MU.togli(doc, bersaglio, quando=None) -> dict
MU.scrivi(doc, clip, note, dove=None) -> dict
```

### `togli`, per tipo di nodo

| bersaglio | effetto |
|---|---|
| strumento (`sound`, `kit`, `midi`, `cv`, `audioTrack`) | le sue clip, poi lui, poi `yScrollArrangementView` |
| strumento + `quando=(da, a)` | **solo** le istanze d'arranger in quell'intervallo; lo strumento resta |
| clip (`instrumentClip`, `audioClip`) | la clip, i `clipCode` che la seguivano, `yScrollSongView` |
| `noteRow` di kit | la **svuota** — vedi §4 |
| `noteRow` di synth | la toglie |

`quando` è ciò che rende dicibile *«leva quel pattern nella seconda metà»*
senza uccidere lo strumento: la distinzione fra togliere una clip dalla
timeline e togliere la clip.

### `scrivi`, per forma delle note

Le funzioni di composizione tornano già la forma giusta: `melodia()` e
`accordi()` danno `dict[altezza, list[Note]]` — il Deluge tiene le note in
righe, una per altezza — mentre `passi()` dà una `list[Note]`, che è una riga
sola perché un drum è una riga sola.

| `note` | `dove` | effetto |
|---|---|---|
| `dict` | — | una riga per altezza; solo clip di synth |
| `list` | nome di drum | quella riga; clip di kit |
| `list` | altezza | una riga sola; clip di synth |

In coda **sempre** `fit_clip_scroll_to_notes()`. Un `dict` su una clip di kit è
un errore che va detto con la sua ragione, non un `KeyError` lontano.

Questo chiude in una funzione le righe 90–92 di `SKILL.md`, l'idioma sbagliato
che quel documento insegnava, e il rischio delle note invisibili.

---

## 3. Cosa fa la rimozione di una clip

1. Trovare il contenitore e l'indice ordinale `i`, e **quale delle due liste**.
2. Toglierla dal contenitore.
3. Per ogni strumento: nelle sue istanze, scartare quelle con `indice == i` e
   scalare di uno quelle con `indice > i` — **solo nella stessa lista**. Il
   bit 31 separa due numerazioni indipendenti, ed è il punto in cui si sbaglia.
4. Se uno strumento resta senza istanze, **togliere l'attributo**, non
   scriverlo vuoto (§3.1).
5. Sistemare `yScrollSongView` (§5).

### 3.1 L'attributo vuoto non esiste

Su 203 strumenti del corpus: **92 senza attributo `clipInstances`, 0 con
l'attributo vuoto** (`0x`). La forma «attributo presente e vuoto» non è mai
stata scritta dal dispositivo. Scriverla sarebbe inventare una forma mai
osservata su un dettaglio che nessuno guarderebbe — la regola «mai inventare
tag, parametri o strutture» vale anche qui.

### 3.2 `beingEdited` non va spostato

Misurato: vale 1 su una clip in **15 song su 36**, e su **nessuna clip nelle
altre 21**. «Nessuna clip aperta» è uno stato che il dispositivo scrive
normalmente. Togliere la clip aperta quindi non obbliga a eleggerne un'altra —
e non farlo evita di aprire una clip che l'utente non ha chiesto.

---

## 4. Il kit: «togli il rullante» non toglie una riga

**393 clip di kit su 395** hanno una riga per *ogni* drum, suonato o no, con
indici contigui da 0. È l'invariante che `create.add_track()` costruisce e che
`kit.check_indices()` — quindi `verifica()` — pretende. Togliere una riga la
romperebbe, e il file verrebbe rifiutato dal cancello stesso.

Quindi **la portata segue ciò che nomini**:

- la **riga** in una clip → si svuota: il drum resta, muto in quella clip
- il **drum** nel kit → `kit.remove_drum()`, che esiste già, rinumera i
  `drumIndex` di ogni clip di quel kit, e cambia **tutte** le clip di quel kit

Sono due richieste diverse e vanno tenute diverse.

---

## 5. Lo scroll: la famiglia §3.1, in specchio

`_keep_row_visible()` **alza soltanto** lo scroll: risolve il contenuto finito
*sotto* il bordo inferiore. La rimozione produce il caso opposto — la vista
resta parcheggiata *sopra* il contenuto rimasto.

Non è teorico. **11 song su 36 hanno `yScrollSongView` positivo**:

| song | `yScrollSongView` | clip |
|---|---|---|
| `Progsong.XML` | 27 | 42 |
| `Aolac.XML` | 9 | 15 |
| `Mmmyeah.XML` | 9 | 36 |

Tolte venti clip da `Progsong`, lo scroll punterebbe oltre l'ultima: **tutte le
clip presenti nel file, nessuna a schermo.** È il difetto che è costato due
sessioni, rifatto al contrario.

Serve il gemello di `_keep_row_visible()`: dopo una rimozione, **abbassare** lo
scroll quel tanto che basta perché l'ultima riga sia visibile.

**Solo quel tanto — non ri-ancorare in basso.** Il dispositivo ancora l'ultima
riga alla riga 7 solo in **15 song su 36**; nelle altre 21 lo scroll è dove
l'utente l'ha lasciato scrollando, e quello è stato da conservare. Stessa
regola già scelta per `scroll_song_view_to()`: «una vista che già mostra la
riga non viene spostata».

Lo stesso vale per `yScrollArrangementView` quando sparisce uno strumento.

---

## 6. Il cancello impara una regola

`verifica()` oggi non ha nessun controllo che la rimozione possa violare. Ne
serve **uno**:

> Nessun `clipCode` deve puntare oltre la fine della lista che indicizza.

Un indice appeso è un file che il Deluge carica e in cui l'arrangiamento suona
la clip sbagliata, o niente. È invisibile a ogni controllo attuale, e la
rimozione è l'unica operazione che può produrlo. Sta in `arranger.check()`,
che `verifica()` già chiama.

Nessun altro allargamento del cancello: aggiungere controlli non misurati è la
trappola dei falsi positivi, già costata due volte in questo progetto.

---

## 7. Test

In `tests/test_all.py`, nello stile esistente. I casi che contano:

- rinumerazione con clip in **entrambe** le liste — il bit 31 è dove si sbaglia
- lo strumento che resta senza istanze perde l'attributo, non lo svuota
- lo scroll positivo: rimozione su `Progsong.XML`, nessuna vista cieca
- lo scroll che **non** si muove quando non serve (la vista dell'utente resta)
- la riga di kit svuotata resta indicizzata e contigua, e `verifica()` tace
- togliere uno strumento non lascia clip appese
- `scrivi()` su kit e su synth, e il `dict` su clip di kit che dice perché no
- round-trip byte-esatto di ciò che non è stato toccato
- il `clipCode` appeso viene fermato dal cancello

## 8. La verifica che conta

> La documentazione dice cosa deve valere. I file dicono com'è scritto. Solo il
> dispositivo dice se funziona.

Una song vera, generata, con qualcosa tolto, **aperta sul Deluge e guardata**.
Finché non è sullo schermo è «scritto nel file», non «funziona» — e questo
progetto ha già dichiarato risolto per due volte qualcosa che nel file c'era e
sul dispositivo non si vedeva.

Quello che va guardato, in particolare: che dopo aver tolto una clip
l'arrangiamento suoni ancora **le stesse clip di prima** (è ciò che la
rinumerazione dei `clipCode` protegge), e che la song view non sia cieca.
