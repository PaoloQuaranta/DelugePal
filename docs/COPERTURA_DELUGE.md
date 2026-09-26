# Copertura delle feature del Deluge

Questa è la fonte canonica per decidere **cosa DelugePal sa fare** e cosa
sviluppare dopo. Non misura quante righe di XML vengono riconosciute: distingue
quattro capacità diverse, perché leggere o conservare una feature non significa
saperla creare in sicurezza.

Target: firmware community **1.3.0-beta**, beta Release 20260925, build
`b76ed39`. La migrazione da `2d7cdf8` e' stata riesaminata sul sorgente per
l'automazione MIDI; le prove Device storiche restano datate esplicitamente
nella colonna Evidenza. La matrice non descrive il firmware ufficiale.

## Come leggere gli stati

- `completa`: il comportamento richiesto per quella colonna è implementato;
- `parziale`: è coperto solo un sottoinsieme dichiarato nella riga;
- `solo-conservazione`: il parser e il writer non distruggono il dato, ma non
  esiste un'API autoriale affidabile;
- `assente`: la capacità non è implementata o non è stata verificata;
- `n/a`: quella dimensione non si applica alla capacità, oppure la capacità
  non esiste nel firmware target (con motivo esplicito nella riga).

Nella colonna **Device**, `completa` significa che almeno una prova controllata
ha raggiunto e funzionato sul Deluge; `parziale` che la prova copre solo il
sottoinsieme indicato; `assente` che l'evidenza si ferma a documentazione,
codice, corpus o test locali. Un test locale verde non promuove da solo questa
colonna.

Priorità: `P0` blocca o rischia dati, `P1` porta molto valore al flusso
compositivo corrente, `P2` amplia il territorio senza bloccarlo, `P3` è
rifinitura o integrazione laterale. `—` si usa solo quando non resta lavoro.

Fuori perimetro: il rilevamento automatico dei transienti in un file audio.
La prova sull'Amen break non ha separato in modo affidabile i colpi; per
quest'analisi si usano applicazioni audio dedicate. Lo slicing uniforme in
kit resta supportato.

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
| metro-risoluzione | song-arranger | Lunghezza delle clip e risoluzione reale della song (nessun metro globale nel formato) | completa | completa | completa | completa | `tools/delugexml/song.py`, `tools/delugexml/musica.py`, `tools/delugexml/create.py`, `tools/delugexml/audio.py`, `tools/delugexml/midicv.py`, `tools/metro_scritto.py`, `tests/test_all.py`, `HANDOFF.md` (METRO01-03) | — | — |
| clip-note | song-arranger | Clip, noteRow e note | completa | completa | completa | completa | `tools/delugexml/song.py`, `tools/delugexml/notes.py` | — | — |
| sezioni-scene | song-arranger | Sezioni, scene e ripetizioni | completa | completa | completa | completa | `tools/delugexml/song.py`, `HANDOFF.md` | — | — |
| colori-sezione | song-arranger | Tabella colori delle sezioni | parziale | completa | assente | assente | `HANDOFF.md`, `docs/ARCHITETTURA.md` | P3 | Ricavare la tabella con una coppia controllata sul dispositivo |
| clip-duplicate | song-arranger | Duplicazione di clip in session view | completa | completa | completa | completa | `tools/delugexml/song.py`, `HANDOFF.md` | — | — |
| arranger-linked | song-arranger | Istanze collegate nell'arranger | completa | completa | completa | completa | `tools/delugexml/arranger.py`, `docs/FINDINGS.md` | — | — |
| arranger-white | song-arranger | Clip bianche indipendenti | completa | completa | completa | completa | `tools/delugexml/arranger.py`, `tests/test_all.py` | — | — |
| stato-viste | song-arranger | Scroll e stato della vista aperta | completa | completa | completa | completa | `tools/delugexml/song.py`, `tools/delugexml/automation.py` | — | — |
| velocity-lift | sequencer | Velocity, lift, posizione e durata | completa | completa | completa | completa | `tools/delugexml/notes.py`, `tests/test_all.py` | — | — |
| probability-note | sequencer | Probability indipendente per nota | completa | completa | completa | completa | `tools/delugexml/notes.py`, `tools/delugexml/musica.py`, `tools/probability_scritto.py`, `tests/test_all.py`, `docs/ARCHITETTURA.md` | — | — |
| iterance-note | sequencer | Iterance classica e custom | completa | completa | completa | completa | `tools/delugexml/notes.py`, `tools/delugexml/musica.py`, `tools/iterance_scritto.py`, `tests/test_all.py`, `docs/FINDINGS.md` | — | — |
| fill-condition | sequencer | Condizione Fill per nota | completa | completa | completa | completa | `tools/delugexml/notes.py`, `tools/delugexml/musica.py`, `tools/fill_condition_scritto.py`, `tests/test_all.py`, `docs/FINDINGS.md` | — | — |
| latching-condition | sequencer | Probability latching/linkata | parziale | completa | solo-conservazione | assente | `tools/delugexml/notes.py`, `HANDOFF.md` | P2 | Catturare nel formato split una coppia indipendente/latching e distinguerla dai codici storici |
| automation-curves | sequencer | Automazione interpolata e a gradini | completa | completa | completa | completa | `tools/delugexml/automation.py`, `tools/delugexml/musica.py` | — | — |
| parameter-locks | sequencer | Parameter lock per onset e drum | completa | completa | completa | completa | `tools/delugexml/musica.py`, `tools/junglevar5_scritto.py` | — | — |
| row-length | sequencer | Lunghezza indipendente della noteRow | completa | completa | completa | completa | `tools/delugexml/song.py`, `tools/delugexml/musica.py`, `tools/row_length_scritto.py`, `tests/test_all.py`, `HANDOFF.md` | — | — |
| row-direction | sequencer | Direction e ping-pong per riga | completa | completa | solo-conservazione | assente | `docs/ARCHITETTURA.md`, `HANDOFF.md` | P2 | Salvare una coppia forward e ping-pong e modellarne gli attributi |
| euclidean-row | sequencer | Sequencer euclideo per riga | completa | completa | completa | completa | `tools/delugexml/musica.py`, `tools/euclid_scritto.py`, `tests/test_all.py`, `docs/FINDINGS.md`, `HANDOFF.md` | — | — |
| arpeggiatore | sequencer | Arpeggiatore classico e community | completa | completa | completa | completa | `tools/delugexml/arpeggiator.py`, `tools/delugexml/musica.py`, `tools/arpeggiatore_scritto.py`, `tests/test_all.py`, `HANDOFF.md` | — | — |
| sintesi-subtractive | synth-fx | Sintesi sottrattiva | completa | completa | completa | completa | `tools/delugexml/create.py`, `tools/delugexml/structure.py` | — | — |
| sintesi-fm | synth-fx | Sintesi FM nativa | completa | completa | completa | completa | `tools/delugexml/structure.py`, `tests/test_all.py` | — | — |
| sintesi-ringmod | synth-fx | Sintesi ring modulation | completa | completa | parziale | assente | `tools/delugexml/structure.py`, `docs/ARCHITETTURA.md` | P2 | Creare e ascoltare una patch ringmod controllata |
| oscillator-sample | synth-fx | Oscillatore sample | completa | completa | completa | completa | `tools/delugexml/kit.py`, `tools/sample_oscillator_probe.py`, `tests/test_sample_oscillator.py`, `docs/OSCILLATORE_SAMPLE.md`; SAMPLEOSC01 ascoltato, risalvato e confrontato semanticamente il 26 settembre 2026 | — | — |
| wavetable | synth-fx | Oscillatore wavetable | completa | completa | parziale | assente | `tools/delugexml/structure.py`, `docs/ARCHITETTURA.md` | P2 | Modellare assegnazione WAV e parametri wavetable da un preset reale |
| dx7 | synth-fx | Importazione e motore DX7 | solo-conservazione | completa | assente | assente | `docs/ARCHITETTURA.md`, `docs/SCHEMA_song_c1.3.0.md` | P2 | Studiare un preset DX7 e il legame con i banchi SYX |
| modulazione | synth-fx | Patch cable e matrice di modulazione | completa | completa | completa | completa | `tools/delugexml/sound.py`, `tests/test_all.py` | — | — |
| inviluppi-lfo-unison | synth-fx | Inviluppi, LFO e unison | completa | completa | completa | completa | `tools/delugexml/sound.py`, `tools/delugexml/structure.py` | — | — |
| filtri-routing-morph | synth-fx | Tipi filtro, routing e morph | completa | completa | completa | completa | `tools/delugexml/structure.py`, `docs/FILTRI.md`, `tests/test_filters.py`; FILTER01 ascoltata, risalvata e conservata semanticamente | — | — |
| effetti-standard | synth-fx | Delay, reverb, mod FX, EQ e distorsioni | completa | completa | parziale | completa | `tools/delugexml/effects.py`, `tools/effetti_scritto.py`, `tests/test_effects.py`, `docs/EFFETTI.md`; FXSTD01 confermata funzionante dall'utente il 25 settembre 2026, risalvata e confrontata semanticamente in 15 sezioni | P2 | P1 chiuso; ampliare la nuova API a pan/compressore del riverbero e ai livelli sync XML oltre 0–9 |
| effetti-community | synth-fx | Grain, stereo chorus e wavefold | completa | completa | parziale | assente | `tools/delugexml/structure.py`, `tools/delugexml/param_ids.py` | P2 | Generare tre patch minime e verificarle sul dispositivo |
| master-compressor | synth-fx | Compressore master di song | completa | completa | parziale | assente | `tools/delugexml/sound.py`, `docs/ARCHITETTURA.md` | P2 | Distinguere API master dal compressore di traccia e dal sidechain |
| drum-lifecycle | kit-sampler | Aggiunta, copia, rimozione e rinumerazione drum | completa | completa | completa | completa | `tools/delugexml/kit.py`, `tests/test_all.py` | — | — |
| drum-sintetici | kit-sampler | Drum sintetizzati con sound completo | completa | completa | completa | completa | `tools/delugexml/kit.py`, `tools/delugexml/sound.py` | — | — |
| drum-sample | kit-sampler | Assegnazione sample e zona a un drum | completa | completa | completa | completa | `tools/delugexml/kit.py`, `tests/test_all.py` | — | — |
| slicing-uniforme | kit-sampler | Slicing uniforme in kit | completa | completa | completa | completa | `tools/delugexml/kit.py`, `tools/vocalchop_scritto.py` | — | — |
| multisample-note | kit-sampler | Multisample con range per nota | parziale | completa | parziale | completa | `refs/synths/Tal Rhodes.XML`, `tools/delugexml/kit.py`, `tests/test_all.py`, `HANDOFF.md`; SAMPLERP01 ascoltato sul Deluge il 24 settembre 2026 | P2 | Esporre lettura strutturata e controlli completi dei range; la scrittura usa ancora un preset modello |
| velocity-layers | kit-sampler | Selezione dei range multisample per velocity | n/a | n/a | n/a | n/a | `docs/ARCHITETTURA.md` | — | Non supportata dalla build target `2d7cdf8`: il motore seleziona i sample range solo per nota |
| audio-tracce | audio | Creazione tracce e clip audio | completa | completa | completa | completa | `tools/delugexml/audio.py`, `tests/test_all.py` | — | — |
| audio-regioni | audio | Start, end e cambio del campione | completa | completa | completa | completa | `tools/delugexml/audio.py`, `tests/test_all.py` | — | — |
| audio-stretch-reverse | audio | Stretch, pitch e reverse delle audio clip | completa | completa | completa | completa | `tools/delugexml/audio.py`, `tools/delugexml/musica.py`, `tests/test_all.py`, `docs/ARCHITETTURA.md`, `HANDOFF.md`; AUDIOREV02 ascoltato sul Deluge il 24 settembre 2026 | — | — |
| looper-resampling | audio | Looper, overdub e resampling interno | parziale | completa | parziale | assente | `tools/delugexml/audio.py`, `docs/ARCHITETTURA.md` | P2 | Catturare Player contro Looper e un overdub risalvato |
| midi-tracce | midi-cv | Tracce MIDI, canali e suffix | completa | completa | completa | completa | `tools/delugexml/midicv.py`, `tests/test_all.py` | — | — |
| cv-tracce | midi-cv | CV 1 e 2 con sorgente CV2 | completa | completa | completa | parziale | `tools/delugexml/midicv.py`, `HANDOFF.md` | P2 | Verificare sul device tutti i valori cv2Source |
| midi-cc | midi-cv | Automazione MIDI CC, bend e pressure | completa | completa | completa | completa | `tools/delugexml/midicv.py`, `tools/delugexml/automation.py`, `tests/test_all.py`, `docs/superpowers/specs/2026-09-25-midi-cc-bend-pressure-design.md`; MIDIAUTO02 confermato sul dispositivo il 25 settembre 2026: CC a gradini, bend/pressure interpolabili | — | — |
| midi-program-bank | midi-cv | Program change e bank select | solo-conservazione | completa | assente | assente | `docs/ARCHITETTURA.md`, `README.md` | P2 | Catturare una clip con program e bank e aggiungere API validata |
| mpe-input-routing | midi-cv | Assegnazione di una Lower o Upper MPE Zone in ingresso | parziale | completa | assente | assente | `HANDOFF.md`, `docs/ARCHITETTURA.md`; il setup usa Exquis in Lower Zone ma non esiste ancora una cattura XML controllata | P2 | Catturare con e senza Learn dell'Exquis, distinguere `inputMPEZone` dal device MIDI e verificare la persistenza |
| mpe-note-expression | midi-cv | Pitch, slide/timbro e pressione per singola nota | completa | completa | completa | completa | `tools/delugexml/mpe.py`, `tests/test_all.py`, `HANDOFF.md`; MANTRA letta dal dispositivo contiene 26 noteRow espressive, 78 assi e 27 743 punti; MPEPROBE01 e' stata caricata, ascoltata e risalvata, conservando esattamente i tre assi | — | — |
| mpe-output-zones | midi-cv | Lower e Upper MPE Zone in uscita verso un synth esterno | parziale | completa | assente | assente | `tools/delugexml/midicv.py`, `docs/FINDINGS.md`; il firmware accetta entrambe le zone, senza esemplari nel corpus | P3 | Rimandare finche non esiste un sintetizzatore MPE esterno da pilotare e una prova device concreta |
| pattern-files | artefatti-settings | File PATTERNS melodic e rhythmic | parziale | parziale | assente | assente | `docs/ARCHITETTURA.md`, `docs/PROSSIMI_PASSI.md` | P3 | Salvare un pattern reale prima di implementare il formato |
| synth-kit-presets | artefatti-settings | Preset standalone SYNTHS e KITS | completa | completa | parziale | parziale | `tools/delugexml/create.py`, `tools/delugexml/kit.py` | P2 | Aggiungere API esplicita di salvataggio preset e prova di reload |
| midi-follow | artefatti-settings | SETTINGS MIDIFollow | parziale | parziale | assente | assente | `docs/FINDINGS.md`, `docs/ARCHITETTURA.md` | P1 | Modellare mapping e persistenza per il setup Exquis e LCXL |
| performance-view | artefatti-settings | SETTINGS PerformanceView | parziale | parziale | assente | assente | `docs/ARCHITETTURA.md`, `README.md` | P3 | Acquisire due assegnazioni controllate e definire lo schema |
| community-features | artefatti-settings | SETTINGS CommunityFeatures | completa | completa | assente | assente | `docs/FINDINGS.md`, `docs/SYSEX.md` | P3 | Esporre solo i flag necessari al workflow con valori documentati |
| midi-device-defs | artefatti-settings | MIDI device definition files | parziale | parziale | assente | assente | `docs/ARCHITETTURA.md`, `README.md` | P2 | Modellare etichette CC e hideUnlabeledCC con un device reale |
| target-c130 | compatibilita | Target community 1.3.0-beta, beta Release 20260925 (`b76ed39`) | completa | completa | completa | completa | `README.md`, `HANDOFF.md`; dispositivo aggiornato dall'utente il 25 settembre 2026 | — | — |
| schema-multiversione | compatibilita | Confronto e migrazione tra firmware | parziale | completa | assente | assente | `HANDOFF.md`, `docs/PROSSIMI_PASSI.md` | P2 | Eseguire scan_versions e classificare differenze che richiedono migrazione |
<!-- capability-matrix:end -->

## Ordine di sviluppo consigliato

La priorità non deriva dal numero di righe mancanti ma dal flusso compositivo
attuale. L'ordine consigliato è:

1. **sintesi ed effetti community**: routing, morph, wavetable, grain e DX7;
2. **sampler residuo**: lettura strutturata e controlli completi dei range;
3. **artefatti laterali e compatibilità**: Settings, Pattern e versioni.

Probability, iterance, Fill, row length, Euclidean e arpeggiatore sono gia'
coperti e verificati sul dispositivo. Il rilevamento automatico dei transienti
e' fuori perimetro, come indicato sopra.

Per il P1 sampler e audio, `kit.set_multisample()` sostituisce i range per nota
partendo dalla struttura di un preset multisample reale: l'ultimo range arriva
fino a TOP. `kit.set_sample_playback()` espone loop, reverse e stretch di un
oscillatore sample. `audio.stretch_clip()` cambia la durata in tick lasciando
ferma la regione in frame e sceglie pitch indipendente o collegato;
`audio.set_clip_playback()` imposta reverse e intonazione. `SAMPLERP01.XML` e
`AUDIOREV02.XML` sono stati caricati con rilettura byte-identica e ascoltati
con esito positivo dall'utente sul Deluge il 24 settembre 2026. Nel corpus i
`sampleRange` hanno `rangeTopNote`, ma nessuna soglia di velocity; il
[manuale](https://delugecommunity.com/manual/device_overview/audio_files/)
descrive i range per nota. Il sorgente della build target conferma che
[`Source::getRange` seleziona solo per nota](https://github.com/SynthstromAudible/DelugeFirmware/blob/2d7cdf8/src/deluge/processing/source.cpp#L137)
e che la voce gli passa
[solo l'altezza suonata](https://github.com/SynthstromAudible/DelugeFirmware/blob/2d7cdf8/src/deluge/model/voice/voice.cpp#L230):
non esiste selezione nativa di campioni per velocity in questa build. Il
reverse dell'oscillatore e quello della clip audio sono operazioni diverse;
per la clip la build target [scrive `reversed=1`](https://github.com/SynthstromAudible/DelugeFirmware/blob/2d7cdf8/src/deluge/model/clip/audio_clip.cpp#L1066-L1076)
e lo [rilegge](https://github.com/SynthstromAudible/DelugeFirmware/blob/2d7cdf8/src/deluge/model/clip/audio_clip.cpp#L1163-L1172).

La riga metro-risoluzione copre le API riusabili: creazione di clip, figure,
pattern e arranger seguono `inputTickMagnitude`. Gli script che compongono
brani specifici su una griglia dichiarata di 384 tick restano esempi per
quella risoluzione; non sono conversioni generiche di song arbitrarie.

Quando una capacità viene sviluppata, la sua riga cambia solo dopo tre passi:
test locale, prova controllata sul Deluge se la colonna Device deve salire, e
registrazione dell'evidenza. Una feature non diventa `completa` perché il suo
tag è comparso nel corpus.
