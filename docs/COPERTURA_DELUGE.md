# Copertura delle feature del Deluge

Questa è la fonte canonica per decidere **cosa DelugePal sa fare** e cosa
sviluppare dopo. Non misura quante righe di XML vengono riconosciute: distingue
quattro capacità diverse, perché leggere o conservare una feature non significa
saperla creare in sicurezza.

Target: firmware community **1.3.0-beta**, build `2d7cdf8` del 12 agosto 2026.
La matrice descrive quel target, non il firmware ufficiale e non release future.

## Come leggere gli stati

- `completa`: il comportamento richiesto per quella colonna è implementato;
- `parziale`: è coperto solo un sottoinsieme dichiarato nella riga;
- `solo-conservazione`: il parser e il writer non distruggono il dato, ma non
  esiste un'API autoriale affidabile;
- `assente`: la capacità non è implementata o non è stata verificata;
- `n/a`: quella dimensione non si applica alla capacità.

Nella colonna **Device**, `completa` significa che almeno una prova controllata
ha raggiunto e funzionato sul Deluge; `parziale` che la prova copre solo il
sottoinsieme indicato; `assente` che l'evidenza si ferma a documentazione,
codice, corpus o test locali. Un test locale verde non promuove da solo questa
colonna.

Priorità: `P0` blocca o rischia dati, `P1` porta molto valore al flusso
compositivo corrente, `P2` amplia il territorio senza bloccarlo, `P3` è
rifinitura o integrazione laterale. `—` si usa solo quando non resta lavoro.

## Matrice canonica

<!-- capability-matrix:start -->
| ID | Area | Capacità | Lettura | Conservazione | Scrittura | Device | Evidenza | Priorità | Prossimo passo |
|---|---|---|---|---|---|---|---|---|---|
| xml-tollerante | fondazioni | XML irregolare del firmware | completa | completa | completa | completa | `tools/delugexml/parser.py`, `tools/delugexml/writer.py` | — | — |
| roundtrip-chirurgico | fondazioni | Round-trip byte-esatto e rebuild | completa | completa | completa | completa | `tools/delugexml/writer.py`, `tests/test_all.py` | — | — |
| sysex-filesystem | fondazioni | Ping, get e put con rilettura hash | completa | completa | completa | completa | `tools/dsysex.py`, `docs/SYSEX.md` | — | — |
| gate-validazione | fondazioni | Controlli bloccanti e avvertenze | completa | n/a | completa | completa | `tools/delugexml/musica.py`, `tests/test_all.py` | — | — |
| preview-browser | fondazioni | Anteprima nel browser file del Deluge | completa | completa | assente | assente | `README.md`, `HANDOFF.md` | P3 | Studiare o invalidare in modo esplicito la cache preview |
| tempo-scala-swing | song-arranger | Tempo, scala, key mode e swing | completa | completa | completa | completa | `tools/delugexml/song.py`, `tests/test_all.py` | — | — |
| metro-risoluzione | song-arranger | Metro e risoluzione reale della song | completa | completa | parziale | parziale | `tools/delugexml/song.py`, `docs/MUSICA.md` | P1 | Aggiungere setter del metro e conversioni relative alla griglia reale |
| clip-note | song-arranger | Clip, noteRow e note | completa | completa | completa | completa | `tools/delugexml/song.py`, `tools/delugexml/notes.py` | — | — |
| sezioni-scene | song-arranger | Sezioni, scene e ripetizioni | completa | completa | completa | completa | `tools/delugexml/song.py`, `HANDOFF.md` | — | — |
| colori-sezione | song-arranger | Tabella colori delle sezioni | parziale | completa | assente | assente | `HANDOFF.md`, `docs/ARCHITETTURA.md` | P3 | Ricavare la tabella con una coppia controllata sul dispositivo |
| clip-duplicate | song-arranger | Duplicazione di clip in session view | completa | completa | completa | completa | `tools/delugexml/song.py`, `HANDOFF.md` | — | — |
| arranger-linked | song-arranger | Istanze collegate nell'arranger | completa | completa | completa | completa | `tools/delugexml/arranger.py`, `docs/FINDINGS.md` | — | — |
| arranger-white | song-arranger | Clip bianche indipendenti | completa | completa | completa | completa | `tools/delugexml/arranger.py`, `tests/test_all.py` | — | — |
| stato-viste | song-arranger | Scroll e stato della vista aperta | completa | completa | completa | completa | `tools/delugexml/song.py`, `tools/delugexml/automation.py` | — | — |
| velocity-lift | sequencer | Velocity, lift, posizione e durata | completa | completa | completa | completa | `tools/delugexml/notes.py`, `tests/test_all.py` | — | — |
| probability-note | sequencer | Probability indipendente per nota | parziale | completa | parziale | assente | `tools/delugexml/notes.py`, `docs/ARCHITETTURA.md` | P1 | Mappare i valori semantici e provarli con una coppia controllata |
| iterance-note | sequencer | Iterance classica e custom | completa | completa | parziale | assente | `tools/delugexml/notes.py`, `docs/FINDINGS.md` | P1 | Esporre costruttori validati e provare maschere multi-step |
| fill-condition | sequencer | Condizione Fill per nota | parziale | completa | solo-conservazione | assente | `tools/delugexml/notes.py`, `HANDOFF.md` | P1 | Identificare il byte 13 e verificarne almeno due stati |
| latching-condition | sequencer | Probability latching del formato storico | parziale | completa | solo-conservazione | assente | `tools/delugexml/notes.py`, `HANDOFF.md` | P2 | Separare latching dai valori probabilistici con file controllati |
| automation-curves | sequencer | Automazione interpolata e a gradini | completa | completa | completa | completa | `tools/delugexml/automation.py`, `tools/delugexml/musica.py` | — | — |
| parameter-locks | sequencer | Parameter lock per onset e drum | completa | completa | completa | completa | `tools/delugexml/musica.py`, `tools/junglevar5_scritto.py` | — | — |
| row-length | sequencer | Lunghezza indipendente della noteRow | completa | completa | solo-conservazione | assente | `tools/delugexml/song.py`, `HANDOFF.md` | P1 | Aggiungere API e verificare poliritmi con rapporti non interi |
| row-direction | sequencer | Direction e ping-pong per riga | completa | completa | solo-conservazione | assente | `docs/ARCHITETTURA.md`, `HANDOFF.md` | P2 | Salvare una coppia forward e ping-pong e modellarne gli attributi |
| euclidean-row | sequencer | Sequencer euclideo per riga | solo-conservazione | completa | assente | assente | `docs/ARCHITETTURA.md`, `README.md` | P1 | Catturare una riga euclidea e definire una primitiva indipendente |
| arpeggiatore | sequencer | Arpeggiatore classico e community | completa | completa | parziale | assente | `tools/delugexml/midicv.py`, `tools/delugexml/structure.py` | P1 | Esporre mode, rhythm, ratchet, spread e probabilità con test sul device |
| sintesi-subtractive | synth-fx | Sintesi sottrattiva | completa | completa | completa | completa | `tools/delugexml/create.py`, `tools/delugexml/structure.py` | — | — |
| sintesi-fm | synth-fx | Sintesi FM nativa | completa | completa | completa | completa | `tools/delugexml/structure.py`, `tests/test_all.py` | — | — |
| sintesi-ringmod | synth-fx | Sintesi ring modulation | completa | completa | parziale | assente | `tools/delugexml/structure.py`, `docs/ARCHITETTURA.md` | P2 | Creare e ascoltare una patch ringmod controllata |
| oscillator-sample | synth-fx | Oscillatore sample | completa | completa | parziale | parziale | `tools/delugexml/kit.py`, `tools/delugexml/structure.py` | P1 | Generalizzare set_sample dai drum ai synth e coprire loop e zone |
| wavetable | synth-fx | Oscillatore wavetable | completa | completa | parziale | assente | `tools/delugexml/structure.py`, `docs/ARCHITETTURA.md` | P2 | Modellare assegnazione WAV e parametri wavetable da un preset reale |
| dx7 | synth-fx | Importazione e motore DX7 | solo-conservazione | completa | assente | assente | `docs/ARCHITETTURA.md`, `docs/SCHEMA_song_c1.3.0.md` | P2 | Studiare un preset DX7 e il legame con i banchi SYX |
| modulazione | synth-fx | Patch cable e matrice di modulazione | completa | completa | completa | completa | `tools/delugexml/sound.py`, `tests/test_all.py` | — | — |
| inviluppi-lfo-unison | synth-fx | Inviluppi, LFO e unison | completa | completa | completa | completa | `tools/delugexml/sound.py`, `tools/delugexml/structure.py` | — | — |
| filtri-routing-morph | synth-fx | Tipi filtro, routing e morph | completa | completa | parziale | parziale | `tools/delugexml/structure.py`, `docs/FINDINGS.md` | P1 | Coprire routing L2H e parallelo, morph e filter FM |
| effetti-standard | synth-fx | Delay, reverb, mod FX, EQ e distorsioni | completa | completa | parziale | parziale | `tools/delugexml/sound.py`, `tools/delugexml/musica.py` | P1 | Aggiungere API strutturali e prove isolate per ogni famiglia FX |
| effetti-community | synth-fx | Grain, stereo chorus e wavefold | completa | completa | parziale | assente | `tools/delugexml/structure.py`, `tools/delugexml/param_ids.py` | P2 | Generare tre patch minime e verificarle sul dispositivo |
| master-compressor | synth-fx | Compressore master di song | completa | completa | parziale | assente | `tools/delugexml/sound.py`, `docs/ARCHITETTURA.md` | P2 | Distinguere API master dal compressore di traccia e dal sidechain |
| drum-lifecycle | kit-sampler | Aggiunta, copia, rimozione e rinumerazione drum | completa | completa | completa | completa | `tools/delugexml/kit.py`, `tests/test_all.py` | — | — |
| drum-sintetici | kit-sampler | Drum sintetizzati con sound completo | completa | completa | completa | completa | `tools/delugexml/kit.py`, `tools/delugexml/sound.py` | — | — |
| drum-sample | kit-sampler | Assegnazione sample e zona a un drum | completa | completa | completa | completa | `tools/delugexml/kit.py`, `tests/test_all.py` | — | — |
| slicing-uniforme | kit-sampler | Slicing uniforme in kit | completa | completa | completa | completa | `tools/delugexml/kit.py`, `tools/vocalchop_scritto.py` | — | — |
| slicing-transienti | kit-sampler | Slicing sui transienti | assente | n/a | assente | assente | `docs/istruzioni/vocal-chop.md`, `docs/repertori/dnb-jungle.md` | P1 | Aggiungere analisi transienti con confini correggibili |
| multisample-layers | kit-sampler | Multisample e velocity layer | solo-conservazione | completa | assente | assente | `docs/ARCHITETTURA.md`, `docs/repertori/idm.md` | P1 | Modellare più zone e selezione per velocity da un preset controllato |
| audio-tracce | audio | Creazione tracce e clip audio | completa | completa | completa | completa | `tools/delugexml/audio.py`, `tests/test_all.py` | — | — |
| audio-regioni | audio | Start, end e cambio del campione | completa | completa | completa | completa | `tools/delugexml/audio.py`, `tests/test_all.py` | — | — |
| audio-stretch-reverse | audio | Stretch, pitch e reverse delle audio clip | completa | completa | parziale | assente | `tools/delugexml/audio.py`, `tools/delugexml/sound.py` | P1 | Esporre parametri musicali e verificarli su una clip controllata |
| looper-resampling | audio | Looper, overdub e resampling interno | parziale | completa | parziale | assente | `tools/delugexml/audio.py`, `docs/ARCHITETTURA.md` | P2 | Catturare Player contro Looper e un overdub risalvato |
| midi-tracce | midi-cv | Tracce MIDI, canali e suffix | completa | completa | completa | completa | `tools/delugexml/midicv.py`, `tests/test_all.py` | — | — |
| cv-tracce | midi-cv | CV 1 e 2 con sorgente CV2 | completa | completa | completa | parziale | `tools/delugexml/midicv.py`, `HANDOFF.md` | P2 | Verificare sul device tutti i valori cv2Source |
| midi-cc | midi-cv | Automazione MIDI CC, bend e pressure | solo-conservazione | completa | assente | assente | `docs/ARCHITETTURA.md`, `tools/delugexml/midicv.py` | P1 | Modellare le righe di automazione CC e provarne una per tipo |
| midi-program-bank | midi-cv | Program change e bank select | solo-conservazione | completa | assente | assente | `docs/ARCHITETTURA.md`, `README.md` | P2 | Catturare una clip con program e bank e aggiungere API validata |
| mpe-zones | midi-cv | Lower e Upper MPE Zone | parziale | completa | assente | assente | `tools/delugexml/midicv.py`, `HANDOFF.md` | P1 | Creare una zona Lower per Exquis e verificare espressione per nota |
| pattern-files | artefatti-settings | File PATTERNS melodic e rhythmic | parziale | parziale | assente | assente | `docs/ARCHITETTURA.md`, `docs/PROSSIMI_PASSI.md` | P3 | Salvare un pattern reale prima di implementare il formato |
| synth-kit-presets | artefatti-settings | Preset standalone SYNTHS e KITS | completa | completa | parziale | parziale | `tools/delugexml/create.py`, `tools/delugexml/kit.py` | P2 | Aggiungere API esplicita di salvataggio preset e prova di reload |
| midi-follow | artefatti-settings | SETTINGS MIDIFollow | parziale | parziale | assente | assente | `docs/FINDINGS.md`, `docs/ARCHITETTURA.md` | P1 | Modellare mapping e persistenza per il setup Exquis e LCXL |
| performance-view | artefatti-settings | SETTINGS PerformanceView | parziale | parziale | assente | assente | `docs/ARCHITETTURA.md`, `README.md` | P3 | Acquisire due assegnazioni controllate e definire lo schema |
| community-features | artefatti-settings | SETTINGS CommunityFeatures | completa | completa | assente | assente | `docs/FINDINGS.md`, `docs/SYSEX.md` | P3 | Esporre solo i flag necessari al workflow con valori documentati |
| midi-device-defs | artefatti-settings | MIDI device definition files | parziale | parziale | assente | assente | `docs/ARCHITETTURA.md`, `README.md` | P2 | Modellare etichette CC e hideUnlabeledCC con un device reale |
| target-c130 | compatibilita | Target community 1.3.0-beta | completa | completa | completa | completa | `README.md`, `HANDOFF.md` | — | — |
| schema-multiversione | compatibilita | Confronto e migrazione tra firmware | parziale | completa | assente | assente | `HANDOFF.md`, `docs/PROSSIMI_PASSI.md` | P2 | Eseguire scan_versions e classificare differenze che richiedono migrazione |
<!-- capability-matrix:end -->

## Ordine di sviluppo consigliato

La priorità non deriva dal numero di righe mancanti ma dal flusso compositivo
attuale. L'ordine consigliato è:

1. **sequencer avanzato**: probability, iterance, Fill, row length, Euclidean
   e arpeggiatore;
2. **sampler e audio**: transient slicing, multisample, stretch e reverse;
3. **MPE e MIDI espressivo**, a partire dalla Lower Zone usata da Exquis;
4. **sintesi ed effetti community**: routing, morph, wavetable, grain e DX7;
5. **artefatti laterali e compatibilità**: Settings, Pattern e versioni.

Quando una capacità viene sviluppata, la sua riga cambia solo dopo tre passi:
test locale, prova controllata sul Deluge se la colonna Device deve salire, e
registrazione dell'evidenza. Una feature non diventa `completa` perché il suo
tag è comparso nel corpus.
