# HANDOFF — Deluge XML Workflow ("Producer Pal-like", asincrono)

**Data:** 10 agosto 2026
**Stato:** avvio progetto — nessun codice scritto, nessuno schema ancora mappato su file reali
**Contesto d'origine:** conversazione web app; questo documento serve a riaprire il lavoro in Cowork con accesso al filesystem e sessione persistente.

---

## 1. Obiettivo

Costruire un workflow che permetta di descrivere in linguaggio naturale strutture musicali (pattern, kit, preset synth, intere song) e ottenerne file XML validi per Synthstrom Deluge, da copiare sulla SD card.

L'ispirazione è **Producer Pal** (Adam Murray, GPL-3.0), che il figlio usa con Ableton Live. Vedi §2 per perché il modello non è replicabile 1:1.

---

## 2. Vincolo fondamentale: perché non è un MCP server

Producer Pal è un dispositivo Max for Live che espone un MCP server + REST API **dentro una sessione Live in esecuzione**. È bidirezionale e real-time: l'AI legge lo stato della sessione e scrive modifiche che compaiono immediatamente.

Il Deluge **non ha nulla di equivalente**. I suoi due soli canali sono:

| Canale | Real-time? | Copre la struttura? | Note |
|---|---|---|---|
| MIDI (note, CC, clock, MIDI Follow Mode) | Sì | **No** — solo performance/parametri | Già in uso nel progetto Launch Control XL |
| File XML su SD (SONGS/, KITS/, SYNTHS/) | No | **Sì** — struttura completa | Statici, letti al load |

Non esiste API strutturale live. **La direzione scelta è quindi asincrona**: generazione offline degli XML → copia su SD → load sul Deluge.

**Nota su una possibile evoluzione futura:** nel repo firmware (Discussion #94) si discute di definire messaggi **SysEx** per leggere e modificare oggetti Deluge, sia a livello file che a livello oggetto. Se/quando arrivasse, aprirebbe la strada a qualcosa di molto più vicino a Producer Pal. **Non è implementato.** Da ricontrollare periodicamente, non da assumere.

---

## 3. Cosa serve all'inizio della sessione Cowork

**Prerequisito bloccante — file da caricare:**

1. **Almeno una SONG XML reale** esportata dal Deluge, preferibilmente 2-3 file di complessità crescente:
   - una minimale (2 tracce, 1 pattern, note semplici)
   - una con un KIT
   - una con un synth con modulazione
2. **Un KIT XML** e **un SYNTH XML** standalone dalle rispettive cartelle.
3. Utile ma non bloccante: l'output di `ls -R` della SD card, per avere la struttura reale delle cartelle.

**Perché è bloccante:** lo schema XML del Deluge non è documentato ufficialmente e **è cambiato più volte tra le versioni di firmware** — in particolare c'è stato un passaggio da elementi XML annidati ad attributi. Qualsiasi generatore scritto contro uno schema ipotizzato produrrà file che il Deluge rifiuta o interpreta male. Lo schema va derivato da file reali generati **dalla tua build**.

---

## 4. Ambiente hardware/software di riferimento

- **Deluge**: community firmware **1.3.0-BETA-EA4E69E** (build con due bug MIDI confermati e segnalati su GitHub, vedi §7)
- **Controller**: Novation Launch Control XL mk2 + Exquis (MPE, Lower Zone, ch 1-7) via CME H2MIDI Pro
- **MIDI Follow**: canale 8 = Follow Channel B, ch 9-15 mixer per traccia, ch 16 riservato ai comandi globali
- **Ambiente di lavoro**: WSL / Linux, Python 3

---

## 5. Stato della SD card (task aperto, parallelo ma correlato)

Migrazione da SD vecchia a nuova:

- ✅ `SONGS/` — copiata, nessun conflitto
- ✅ `SYNTHS/` — copiata, riorganizzata in sottocartelle. **Verificato sicuro**: le song incorporano internamente uno snapshot dei parametri synth e non rileggono gli XML dopo il load. Unico vincolo: i path dei sample dentro `SAMPLES/` non devono cambiare.
- ✅ `KITS/` — copiata
- ⏳ `SAMPLES/` — **in corso**, con collisioni di nomi cartella tra contenuto personale e factory

**Approccio concordato per le collisioni:** diff dei *nomi file* dentro le cartelle in collisione (non del contenuto binario) → se nessun conflitto reale di filename, merge → se conflitti reali, rinominare le cartelle/file **personali** (mai i factory), poi `grep -rl` + `sed -i` per aggiornare i riferimenti negli XML di KIT/SYNTH già copiati.

Questa task e il progetto XML workflow condividono lo stesso parsing degli XML — conviene affrontarle nella stessa sessione.

---

## 6. Tool community da valutare

| Tool | Cosa fa | Riserva |
|---|---|---|
| **deluge-card** (PyPI, mupaduw) | API Python per il filesystem SD; legge song, tempo, key, scale, uso dei sample; sposta sample aggiornando i riferimenti | Documentato per **song XML da fw3.15** — molto più vecchio della tua build. Da verificare la compatibilità prima di adottarlo. |
| **deluge-cmd** (PyPI, mupaduw) | CLI sopra deluge-card: verifica struttura, lista song/sample usati e inutilizzati | Stessa riserva sulla versione |
| **Deluge Commander** | Gestione contenuti SD | Non ancora valutato |
| **deluge-tune-crafter** (IvanVeridian) | MIDI → XML Deluge; inietta tracce in un `base.xml` | Approccio "injection su template" — potenzialmente **il pattern giusto da imitare**: partire da una song reale come base invece di generare da zero |
| **Deluger** / lavori di Jamie Faye (Downrush) | Parser browser-based; approccio "scan everything you can find" per essere robusto ai cambi di schema | Fonte utile per capire lo schema, anche se non lo usiamo direttamente |

**Nota strategica:** il pattern "template-injection" (parti da una song vera, sostituisci/aggiungi nodi) è molto più robusto del pattern "genera da zero", data l'assenza di uno schema documentato. Da preferire almeno per la prima iterazione.

---

## 7. Bug firmware noti nella build in uso (EA4E69E)

Entrambi confermati sperimentalmente e segnalati su `SynthstromAudible/DelugeFirmware`:

1. **Le assegnazioni device MIDI-FOLLOW e le impostazioni MPE zone per device non persistono al power cycle**, pur mantenendo i numeri di canale. Confermato su SD nuova con un singolo device (esclusa corruzione storage / complessità multi-device).
   *Workaround:* accendere H2MIDI Pro **prima** del Deluge → azzerare le MPE zone della LCXL → rifare il Learn di Channel A/B a ogni sessione.
2. **Global MIDI CMD Learn** (`SETTINGS > MIDI > CMD`) non lega nessun input note, nonostante l'indicatore LEARN lampeggi e i Note-On siano confermati via MIDI-OX da tre sorgenti indipendenti.
   *Nessun workaround noto.*

Non impattano direttamente il workflow XML, ma sono contesto rilevante se si testa qualcosa che coinvolge MIDI.

---

## 8. Punto aperto da chiarire — schema MIDIFollow.XML

C'è un'**incoerenza non risolta** nei materiali precedenti sul file `MIDIFollow.XML` tra firmware 1.2 e 1.3:

- Un'affermazione (proveniente da un altro AI) sosteneva che il tag `defaultCCMappings` fosse stato rinominato in `cc_mappings`, con un nuovo blocco `<settings>`.
- Quella specifica affermazione **è stata analizzata e giudicata probabilmente allucinata**: ricerche su documentazione ufficiale, changelog e repo GitHub non hanno trovato `cc_mappings` da nessuna parte, e il file auto-generato dal dispositivo stesso conteneva `defaultCCMappings`.

**Da verificare guardando il file reale sulla SD, non fidandosi di nessuna delle due versioni.** Questo è il tipo esatto di errore che il progetto deve evitare per costruzione: mai inventare tag.

---

## 9. Piano di lavoro proposto

**Fase 0 — Reverse engineering dello schema**
Caricare i file reali. Parsing sistematico con `xml.etree` per estrarre l'inventario completo di tag, attributi, range dei valori. Produrre un documento di schema derivato empiricamente, con esplicita distinzione tra "osservato" e "inferito".

**Fase 1 — Round-trip test**
Prima di generare qualsiasi cosa: leggere una song, riscriverla senza modifiche, verificare che il diff sia vuoto (o che le differenze siano solo cosmetiche e innocue). Caricarla sul Deluge e confermare che apra correttamente. **Se questo test non passa, tutto il resto è inaffidabile.**

**Fase 2 — Modifica minima**
Cambiare un solo valore (es. tempo), verificare sul dispositivo. Poi: aggiungere una nota a un pattern esistente. Poi: aggiungere un pattern.

**Fase 3 — Generatore**
Solo a questo punto, uno strato che traduce descrizioni in linguaggio naturale → chiamate al generatore. Da valutare se come libreria Python + prompt, o come skill/plugin Cowork.

**Fase 4 (eventuale) — Automazione della copia**
Cartella sincronizzata / script che scrive direttamente sulla SD montata.

---

## 10. Preferenze di lavoro (importanti)

- **Approccio incrementale**, un passo verificato alla volta. Non generare grandi impianti prima di aver validato le fondamenta.
- **Riconoscimento esplicito degli errori** — se qualcosa non torna o è incerto, dirlo, non coprirlo con sicurezza apparente.
- **Verifica prima di operazioni distruttive**, sempre. La SD contiene lavoro personale.
- **Mai inventare tag, parametri o strutture XML.** Se non è stato osservato in un file reale o in una fonte primaria verificabile, va dichiarato come ipotesi.
- Diffidenza motivata verso le fonti deboli (video YouTube, post Facebook, risposte di altri AI) su dettagli tecnici precisi.

---

## 11. Prompt di apertura per la sessione Cowork

> Riprendiamo il progetto Deluge XML workflow. Ti carico [N] file XML reali dalla mia SD card (song, kit, synth) presi dal firmware community 1.3.0-BETA-EA4E69E.
>
> Fase 0: fai un'analisi sistematica dello schema — inventario di tutti i tag e attributi, con range dei valori osservati. Distingui chiaramente ciò che hai osservato da ciò che stai inferendo.
>
> Poi Fase 1: round-trip test — leggi e riscrivi una song senza modifiche, e mostrami il diff. Non passare oltre finché quello non è pulito.
>
> Leggi prima il file HANDOFF_deluge_xml_workflow.md per il contesto completo.
