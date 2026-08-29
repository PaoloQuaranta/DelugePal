# Fonti

⚠️ **Questo documento ordina le fonti per AUTORITÀ — cioè chi vince in caso
di conflitto. Non è l'ordine in cui si cerca.** I due ordini sono quasi
opposti, e confonderli è l'errore che questo progetto ripete più spesso.

---

## L'ordine di RICERCA — si cerca dall'alto

Direttiva dell'utente, 16 agosto 2026. Quando serve sapere **come funziona il
Deluge**, si cerca in quest'ordine e ci si ferma appena si trova:

| | dove | perché prima |
|---|---|---|
| 1 | **documentazione community** — <https://delugecommunity.com> | descrive *questa* build, c1.3.0, comprese le feature che il guidebook non ha |
| 2 | **guidebook ufficiale**, 338 pagine sulla SD | il modello concettuale completo; molte cose sono spiegate in una frase |
| 3 | **sorgente del firmware** | quando le due sopra tacciono o si contraddicono |
| 4 | **i file locali** (`refs/`, `corpus_versions/`) | **ultimo**: per vedere com'è *scritta* una cosa che si è già capita |

**Perché la direttiva esiste.** La tendenza a partire dal punto 4 — cioè a
fare reverse engineering senza avere chiaro come funziona il dispositivo — ha
prodotto, documentati in questo repo:

- ricerca statistica sul corpus per cose spiegate in **una frase** del manuale
  (lo scroll di song view, `inputTickMagnitude` = RESOLUTION);
- **quattro modelli sbagliati di fila** sulla finestra di clip view, nessuno
  trovato dai test (FINDINGS §6-octies);
- l'ipotesi demolita sulla **riga MIDI di un kit**: un attributo osservato nel
  posto sbagliato (FINDINGS §6-septies);
- le tabelle dei **patch cable**, che stavano per diventare un cancello sul
  corpus finché l'utente non ha fatto notare che il corpus registra cosa ha
  suonato lui, non cosa il firmware accetta (`MUSICA.md`).

E un caso in cui il punto 1 ha **fatto risparmiare** il lavoro: le pagine
community sul motore di sintesi sono segnaposto dichiarati, quindi si passa
subito al guidebook invece di rileggerle sperando.

## L'ordine di AUTORITÀ — si decide dal basso

È quello del resto del documento, e va nella direzione opposta:

> La documentazione dice cosa **deve** valere. I file dicono com'è **scritto**.
> Solo il dispositivo dice se **funziona**.

Quindi: si cerca partendo dalla documentazione, si decide partendo dal
dispositivo. Una fonte alta nell'ordine di ricerca può benissimo essere
smentita da una bassa nell'ordine di autorità — è successo con la doc
community, che sui byte di comando SysEx è sbagliata.

---

## Primarie

### 1. I file scritti dal dispositivo

`refs/` — 32 file a `firmwareVersion="c1.3.0"` copiati da E:. È la fonte che ha
prodotto quasi tutto quello che c'è in FINDINGS.md, ed è l'unica che descrive
*questa* build.

Limite: descrive cosa il firmware ha scritto, non cosa è disposto a leggere.

### 2. Il codice sorgente del firmware

<https://github.com/SynthstromAudible/DelugeFirmware> — branch `community`.

File che sono serviti:

| file | cosa ci ho trovato |
|---|---|
| `src/deluge/storage/Serializer.cpp` | `writeAttribute(name, value, bool onNewLine)`: nessun escape XML, formattazione decisa call-site per call-site |
| `src/deluge/storage/smsysex.{h,cpp}` | il servizio filesystem su SysEx |
| `src/deluge/model/song/song.cpp` | `timePerTimerTick`/`timerTickFraction` sono le due metà di un uint64 32.32 |
| `src/deluge/storage/` | il serializzatore è stato estratto da `storage_manager` in `Serializer.cpp` / `JSONSerializer.cpp`, cioè il refactoring proposto nella Discussion #94 è avvenuto |

Limite importante: il branch `community` su GitHub **non è la build installata**
(`0856ff9`, 2026-08-06). Per dettagli fini vale la SD, non il repo.

### 3. Il dispositivo

Verifica diretta. Finora usata una volta, per confermare la formula del tempo
(`Mark.XML` → 88 BPM). È l'arbitro finale.

---

## Secondarie, utili

- **Doxygen del firmware** — <https://delugecommunity.com/doxygen/>
  Utile per orientarsi nelle classi (`NoteRow`, `Clip`, `Song`) senza scaricare
  il repo.
- **Note sul protocollo SysEx** —
  <https://delugecommunity.com/development/deluge/sysexprotocolnotes/>
  Framing, comandi, impacchettamento 7 bit, API a descrittori di file. Concorda
  con il sorgente su tutto ciò che ho controllato.
- **Wiki del repo** —
  <https://github.com/SynthstromAudible/DelugeFirmware/wiki>
- **Discussion #94, "Deluge save file parsing in the browser"** (giugno 2023) —
  <https://github.com/SynthstromAudible/DelugeFirmware/discussions/94>
  Quella citata nell'handoff. Va letta sapendo che è **datata**: descrive il
  SysEx come proposta futura, mentre nel frattempo è stato implementato.

## Strumenti community

- **[silicakes/deluge-extensions](https://github.com/silicakes/deluge-extensions)** (DEx)
  Client SysEx funzionante, con test end-to-end contro un Deluge collegato. È il
  riferimento da studiare se si vuole scrivere sulla SD via USB invece che
  spostandola.
- **[jamiefaye/downrush](https://github.com/jamiefaye/downrush)** — `xmlView/src/FmtSound.js`
  Descrive i formati binari. La fonte storica più citata sullo schema. Va presa
  con cautela: dichiaratamente incompleta e scritta per firmware molto più
  vecchi. Utile come conferma incrociata, mai come autorità.
- **[amiga909/deluge-synthstrom-utils](https://github.com/amiga909/deluge-synthstrom-utils)**
  Analizza gli XML per trovare sample mancanti e li corregge, con report.
  Direttamente pertinente alla task `SAMPLES/` rimasta aperta.
- **deluge-card / deluge-cmd** (PyPI, mupaduw) — le riserve dell'handoff restano
  valide: documentati per song XML da fw 3.15, molto più vecchio di questa build.
  Non valutati in questa sessione.

## Corpora musicali, e le loro licenze

⚠️ **Questi non sono fonti sul Deluge: sono il materiale da cui la conoscenza
musicale è misurata**, e a differenza di tutto il resto di questo documento
**portano obblighi di licenza.** Le fonti tecniche qui sopra si citano per
onestà; queste si citano perché è richiesto.

Nessuno dei due corpora è versionato — stanno in `to-read/`, fuori dal repo, e
non vengono ridistribuiti. Ma i **numeri** che ne escono stanno in
`docs/MUSICA.md` e nelle schede di `docs/repertori/`, che sono pubblicati: è
quello a far scattare l'attribuzione, non il file.

⚠️ **Le due licenze sono diverse, e non è un dettaglio.** Una chiede
l'attribuzione, l'altra ha anche una clausola di reciprocità — vedi in fondo.

### Groove MIDI Dataset — CC BY 4.0

1150 esecuzioni di batteria di dieci batteristi, etichettate per stile, BPM,
metro e `beat`/`fill`. Da qui vengono la **scala di velocity** e i **groove
template** della casella 6 del jazz, e il feel del primo pezzo jazz.

- **Licenza:** Creative Commons Attribution 4.0 International (CC BY 4.0),
  <https://creativecommons.org/licenses/by/4.0/>. Letta dal file `LICENSE`
  **dentro il dataset**, non dal web.
- **Citazione richiesta**, dalla pagina del dataset:

      Jon Gillick, Adam Roberts, Jesse Engel, Douglas Eck, and David Bamman.
      «Learning to Groove with Inverse Sequence Transformations.»
      International Conference on Machine Learning (ICML), 2019.

- <https://magenta.tensorflow.org/datasets/groove>

La CC BY chiede **l'attribuzione e nient'altro**: si può usare per qualunque
scopo, anche commerciale, purché si dica da dove viene.

### Weimar Jazz Database (WJazzD) — ODbL 1.0

456 assoli jazz trascritti a mano, con gli accordi e i battiti allineati alla
linea. Da qui vengono lo **swing misurato** della casella 4 e il **giro
armonico** del primo pezzo jazz.

- **Licenza:** Open Database License (ODbL) 1.0 per il database,
  <https://opendatacommons.org/licenses/odbl/1.0/>; i contenuti individuali
  sotto Database Contents License (DbCL) 1.0,
  <https://opendatacommons.org/licenses/dbcl/1.0/>.
- **Autore:** The Jazzomat Research Project (c) 2012-2017
- **Versione:** 2.1, `status` FINAL, creata il 2018-01-07
- <https://jazzomat.hfm-weimar.de/>

  ⚠️ **Licenza, autore e versione vengono dal database stesso**, tabella
  `db_info`, non da una pagina web:

      sqlite3 to-read/MIDI/wjazzd.db "select * from db_info"

  Per un database è la fonte più autoritativa che esista, ed è a portata di
  query. Vale la pena saperlo perché la licenza dell'ODbL **non l'avrei
  indovinata**: a occhio sembrava un caso da Creative Commons come l'altro.

- **Citazione richiesta**, dalla pagina del progetto:

      Pfleiderer, Martin; Frieler, Klaus; Abeßer, Jakob; Zaddach,
      Wolf-Georg; Burkhart, Benjamin (a cura di) (2017): Inside the
      Jazzomat — New Perspectives for Jazz Research. Schott Campus.

  ⚠️ La pagina, letta il 29 agosto 2026, ha reso il terzo nome come
  «Abessert». È quasi certamente un artefatto della **ß**, e il nome corretto
  è **Abeßer**. Scritto corretto e segnalato qui, invece che copiato com'era o
  corretto in silenzio: in un'attribuzione di licenza il nome di una persona è
  precisamente la cosa che non si tira a indovinare. Chi può, lo verifichi
  sulla pubblicazione.

### La clausola che l'ODbL ha e la CC BY no

⚠️ **L'ODbL è share-alike sui database derivati**: chi *distribuisce* un
database derivato da WJazzD deve distribuirlo sotto la stessa licenza. La CC BY
del Groove MIDI non chiede niente del genere.

Cosa questo progetto pubblica oggi, in fatto: **misure aggregate** — mediane,
conteggi, distribuzioni, e un giro armonico di dodici battute — dentro documenti
in prosa, non porzioni del database né un database. Il `.db` non è versionato e
non viene ridistribuito.

⚠️ **Questo è il quadro dei fatti, non un parere legale, e non è una cosa che
decide un agente.** Se il progetto un giorno pubblicasse estratti riga per riga,
o un file derivato interrogabile, la domanda andrebbe posta a chi di dovere
prima, non dopo.

---

## Fonti da non usare per dettagli tecnici

Il forum Synthstrom conferma il quadro generale — non esiste una specifica
ufficiale del formato XML, i firmware vecchi usano un formato incompatibile e i
file dell'era 2.x sono XML illegale con più nodi radice — ma sui dettagli precisi
di schema è aneddotico. Concorda con quanto osservato, e questo è tutto ciò che
gli si può chiedere.

---

## Cosa ha cambiato la ricerca sulle fonti

Due cose che i soli file non potevano dire:

1. **Perché la tabella di formato non è derivabile per regole.** Il sorgente
   mostra che `onNewLine` è un booleano deciso a ogni chiamata: non esiste
   nessuna soglia da scoprire. Apprendere dal corpus non era un ripiego, era
   l'unico approccio corretto.
2. **Il SysEx esiste.** Cambia la Fase 4 del piano, che era "scrivere sulla SD
   montata".

E una che ha rafforzato un risultato: il mancato escape di `&` non è un caso
limite di certi nomi ma la conseguenza del fatto che `writeAttribute` non
escapa **mai** nulla.
