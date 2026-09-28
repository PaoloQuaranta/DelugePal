# LYRA VIAREGGIO — revisioni dark dub

## Stato finale — task compositivo chiuso

Il 27 settembre 2026 l'utente ha dichiarato chiuso il task compositivo.
Ultima consegna: `/SONGS/DelugePal/LYRA VIAREGGIO06.XML`, riletta identica
dopo il caricamento (890659 byte, SHA-256
`8012f8243875a2d503341470f859013bfa00aa75f45bb9030b3157936941eca5`).

Dopo la 04 l'utente ha fatto un rough mix e rimosso note sulla coda.
Le revisioni successive sono partite dai suoi salvataggi riscaricati:
05 porta il volume Glass da 15 a 30/50; 06 porta i carrier DX7 1/3/5
da 83/76/66 a 99/92/82. Confronti semantici confermano la conservazione
del resto della song. Il preset standalone Glass resta quello originale.

La chiusura creativa non chiude P2 DX7/wavetable e non costituisce una
conferma specifica della causa del basso livello di Glass. Nessuna ulteriore
prova Glass richiesta. Le sezioni successive documentano le revisioni precedenti.

## Revisione 04 — sei voci

Richiesta dell'utente: distribuire le parti dei due synth aggiunti fra sei
voci, mantenendo le due esistenti e creando due DX7 e due wavetable originali.
Riscaricata `/SONGS/DelugePal/LYRA VIAREGGIO03.XML` prima di intervenire.
Generatore: `tools/lyra_viareggio_six.py`.

| Voce | Materiale assegnato | Note | Timbro progettato |
|---|---|---:|---|
| LYRA TINE01 | comping: prima esposizione e ritorni | 60 | Tine filtrata/distorta della 02 |
| LYRA REED01 | comping: sezioni più rarefatte | 18 | DX7 algoritmo 32, sei portanti additive, organo nasale sostenuto |
| LYRA GLASS01 | comping: sezioni di sviluppo e conclusione | 47 | DX7 algoritmo 5, rapporti inarmonici, campane metalliche con coda |
| LYRA ACID01 | frasi: prima esposizione e ritorno centrale | 10 | Acid modulata della 02, registro della 03 |
| LYRA VOX01 | frasi: primo sviluppo, ripresa e conclusione | 13 | Allophones, risonanze vocali, passa-banda, attacco lento |
| LYRA METAL01 | frasi: sviluppi intermedi | 8 | Bowed Metal, filtro 12 dB, wavefold, saturazione e flanger |

Le due nuove tabelle sono state lette dalla SD, senza modificarle:
`SAMPLES/WAVETABLES/CommunityWavetables/Allophones.wav` (123016 byte) e
`SAMPLES/WAVETABLES/CommunityWavetables/Bowed Metal [ML].wav` (73864 byte).
Entrambe mono float32 a 44100 Hz, con metadato `clm ` da 2048 campioni/ciclo.

### Scelte dei quattro preset

- **Reed:** sei portanti, coarse 1/2/3/4/6/8, livelli 87/79/70/62/54/46;
  inviluppi sostenuti (livelli 99/99/99/0), feedback 0. Volume 25,
  pan 18, LPF 35/resonance 7, HPF 12, chorus rate 5/depth 15,
  delay analogico dotted sync XML 7 feedback 15, riverbero 14.
- **Glass:** algoritmo 5, tre coppie; modulatori coarse/fine
  7/41, 3/27, 11/6, livelli 73/67/61; portanti 83/76/66.
  Volume 23, pan 32, LPF 45/resonance 2, HPF 19;
  delay digitale even sync XML 7 feedback 12, riverbero 21, mod FX spento.
- **Vox:** volume 27, pan 20, oscillator A 43, position 22;
  passa-banda cutoff 34/resonance 12, HPF 12; ENV1 27/43/44/31,
  ENV2 39/43/34/34. ENV2→position +14, LFO1→position +7,
  ENV2→LPF +5. Chorus rate 4/depth 18, riverbero 22;
  delay analogico dotted sync XML 8 feedback 14.
- **Metal:** volume 23, pan 31, oscillator A 39, position 29;
  LPF 12 dB cutoff 32/resonance 8, HPF 18, wavefold 9, saturazione 4/15;
  ENV1 19/39/42/28, ENV2 34/40/24/31. ENV2→position -12,
  LFO1→position +9, ENV2→LPF +9. Flanger rate 6/depth 11/feedback 8;
  delay analogico dotted sync XML 7 feedback 17, riverbero 16.

Per le due nuove clip wavetable, anche position interpolata attraverso cinque
punti equidistanti nella clip: Vox 17/29/21/34/18, Metal 33/19/29/16/30.
Tutti i valori rimanenti e gli operatori DX7 completi sono nel generatore;
rapporto parametri in `out/lyra_viareggio/LYRA VIAREGGIO04.presets.json`.
Assegnazioni frase per frase in `LYRA VIAREGGIO04.distribution.json`.

### Verifica e consegna

Confronto esatto del multinsieme degli eventi nel tempo assoluto della song:
156 note prima e dopo, senza duplicazioni o perdite; conservati pitch,
onset, durata, velocity, lift e condizioni. Strum e frasi con note collegate
sono assegnati come gruppi. Strumenti originali, loro istanze e tutte le
altre clip identici; suoni/automazioni Tine e Acid conservati. Quattro nuovi
strumenti e quattro nuove istanze, stessa durata complessiva del brano.
Verifica e avvertenze vuote.

Caricati e riletti byte-identici nelle rispettive cartelle DelugePal:

| File | Byte | SHA-256 |
|---|---:|---|
| LYRA VIAREGGIO04.XML | 899177 | `820ddbbac912e844972b2dfe077bbd1942ce0f0653f0cf0033d18ba14feb2821` |
| LYRA REED01.XML | 5712 | `2a09e5e23d83758a02223ae7fbffe3d96aaaadb6032360bb413ee7ed96911cc2` |
| LYRA GLASS01.XML | 5709 | `3ad7368622df936ba710d3f898dc2deafdf940d6b12ab3fa1cd3c9c6cfe4209a` |
| LYRA VOX01.XML | 5877 | `e5d7e9de7ce2ce9d955720fde83ff60749f8b85e41bbbd60db9d5b6b81e934cd` |
| LYRA METAL01.XML | 5900 | `e456d9acdd5065750289c7d65a888ec804db9708f83b99e606240ff4765ed90c` |

Ascolto della 04 ancora da fare. I timbri descritti sono intenzioni di progetto,
non valutazioni ottenute da un rendering o da un ascolto dell'assistente.


## Revisione 03 — registro e fraseggio

Feedback sulla 02: «meglio». Richiesti Acid un'ottava sotto e più fraseggiata,
variazioni ritmiche/strum alla Tine. La 02 è stata nuovamente scaricata dalla SD.
`tools/lyra_viareggio_phrasing.py` mantiene tutti i parametri e le automazioni
della 02, tutti gli strumenti e tutte le istanze dell'arranger, batteria e
altre clip identiche nel confronto semantico.

- Acid: tutti i 23 attacchi originali trasposti esattamente di -12 semitoni.
  Quattro note lunghe sviluppate in nota d'appoggio, nota vicina e ritorno,
  con piccoli overlap. 31 note finali, registro Mi3–Mi4 (52–64 MIDI).
  Restano le pause e le frasi sostenute della 02.
- Tine: 17 accordi con strum alternato ascendente/discendente, 4 o 6 tick
  fra le voci (circa 40/60 ms); sei attacchi anticipati o ritardati di
  24 tick; quattro risposte soffici dopo 144 tick, velocity -15.
  114→125 note; stesse altezze e voicing, nessun cambiamento ai preset.

Verifica e avvertenze vuote. Caricata `/SONGS/DelugePal/LYRA VIAREGGIO03.XML`,
869665 byte, rilettura byte-identica, SHA-256
`7a4644b5278cb911b27e6e2dbf0e865410af4e9cd7fd237271a6006c5e9b9026`.
Ascolto della 03 confermato dall'utente: «meglio». Preset standalone restano
quelli 02. Device passa a parziale per DX7 e wavetable: funzionamento
nella song ascoltato, confronto dopo risalvataggio e reload standalone
ancora da eseguire. Le revisioni combinano più parametri e non isolano
l'effetto di ogni singolo controllo.


## Revisione 02 dopo ascolto

L'utente approva umanizzazione, armonia e arrangiamento della 01.
Acid viene giudicata troppo pianistica e breve; Tine troppo simile al piano
registrato. `tools/lyra_viareggio_revision.py` applica soltanto queste correzioni
alla 01 nuovamente scaricata dal Deluge, senza rieseguire l'umanizzazione.

- **Acid:** le stesse 23 note, altezze, attacchi e velocity, con durate
  252–672 tick (circa 2,5–6,7 s). Otto coppie di eventi con sovrapposizione
  temporale; restano anche gli appoggi a due voci già presenti.
  ENV1 A/D/S/R 24/42/43/30; ENV2 36/42/30/34. Volume 23,
  resonance LPF 23, LFO1 rate 3 e LFO2 rate 4, saturazione 3.
  Patch cable: ENV2→position +17, ENV2→LPF +15,
  LFO1→position +12, LFO2→LPF +4.
  Sweep interpolati per frase: position 13→32→19, LPF 20→29→22.
  Nel preset standalone, basi position 16 e LPF 22; gli sweep temporali
  appartengono alla clip nella song. HPF e restante trattamento conservati.
- **Tine:** tutte le note conservate. LPF passato a `SVF_Band`, cutoff 28,
  resonance 17, HPF 15; ENV2 0/26/8/23, ENV2→LPF +12.
  Saturazione 7/15, bitcrush 3/50, decimation 5/50, volume 25.
  Phaser al posto del chorus: rate 7, depth 13, feedback 8.

Confronto semantico sulla copia riletta: strumenti e clip estranei ai due
suoni sono identici; tutte le istanze dell'arranger e tutte le note Tine
sono identiche. Verifica e avvertenze vuote. La 02 e i due preset sono stati
caricati senza sovrascrivere la 01 e riletti byte-identici:

| Destinazione | Byte | SHA-256 |
|---|---:|---|
| `/SONGS/DelugePal/LYRA VIAREGGIO02.XML` | 868715 | `482e92591e1863f495f1fbe4439422f9aa4cd39dbfc2796f7625fa27ddf57021` |
| `/SYNTHS/DelugePal/LYRA TINE02.XML` | 5832 | `40784889b49274e45f1fa4e295c7f240dffdf256fa6c40c284fbd68d1ff01fe2` |
| `/SYNTHS/DelugePal/LYRA ACID02.XML` | 5972 | `d31647eda95329b502314ff18627481c556342b904d07d7c8f945ce9d18f9c55` |

Nella song i nomi delle tracce rimangono LYRA TINE01 e LYRA ACID01;
i parametri incorporati sono quelli revisionati. I file standalone 02
servono per riutilizzare i nuovi suoni in altre song.
Ascolto della 02 e risalvataggio ancora da fare. L'ascolto della 01 dimostra
che i motori DX7/wavetable caricano e suonano, ma non chiude il round-trip
semantico dopo un salvataggio del dispositivo.

---

26 settembre 2026. Generatore: `tools/lyra_viareggio.py`.

## Sorgente e conservazione

Riscaricata via SysEx `/SONGS/Lyra Viareggio.XML`: 845452 byte.
63 BPM, 384 tick/battuta, swing 66 sulle semicrome (intervallo XML 7).
La versione attuale contiene 52 istanze d'arranger e termina dopo 72 battute.
La vecchia copia in `refs/songs/` non contiene questa struttura.

Conservati strumenti originali, 52 istanze con posizioni/durate/riferimenti,
audio, melodie, basso, automazioni e numero di eventi di batteria.
Corretto lo scroll delle clip e aperta una vista complessiva dell'arranger.

## Batteria

1032 colpi, 24 clip, inclusi i fill indipendenti nell'arranger.
Niente randomizzazione: accenti e piccoli scarti dipendono dal ruolo del drum
e dalla posizione nella frase. Cassa sul movimento ferma, colpi interni
leggermente variati; rullante e clap ritardati; hat con accenti alternati e
rulli alleggeriti. Scarti complessivi -1..+3 tick (circa -10..+30 ms), velocity
-14..+4 rispetto all'originale. Nessun colpo aggiunto o cancellato.
Durata, lift, probability, iterance e fill sono conservati.
Le righe di batteria sorgenti non contengono automazioni di parametro.

## Accompagnamento composto

Due nuove tracce, due nuove istanze d'arranger. Piano: battute 9–68;
wavetable: 13–68. Entrambe contengono pause e frasi distinte.

Il basso e le parti esistenti usano soprattutto Mi/Fa/Lab/Si/Do/Reb.
Scelte compositive, da giudicare all'ascolto: Fm(maj7/9), Dbmaj7 senza
fondamentale, shell E7b9 e Bdim7, con le tensioni concentrate nei vuoti.
Voicing di piano: Lab3–Do4–Mi4, eventualmente Sol4; Lab3–Do4–Fa4;
Lab3–Re4–Fa4. Sezioni dense alleggerite a due voci; risposte Acid brevi
su Lab4/Si4/Do5/Mi5, con tre appoggi di Mi4. Scale OFF sulle nuove clip.
Dettaglio di ogni evento nel generatore e in `out/lyra_viareggio/racconto.txt`.

## Preset originali

### LYRA TINE01

DX7 autentico, algoritmo 5: coppie indipendenti 2→1, 4→3, 6→5.
Patch intera incorporata (156 byte), nessun banco SYX esterno richiesto.

| Operatore | Rapporto coarse/fine | Livello | Velocity sensitivity | EG rates | EG levels |
|---|---|---|---|---|---|
| 1 | 1/0 | 88 | 2 | 99,67,37,65 | 99,83,0,0 |
| 2 | 1/0 | 62 | 5 | 99,74,48,69 | 99,58,0,0 |
| 3 | 1/0 | 82 | 2 | 98,61,34,62 | 99,78,0,0 |
| 4 | 2/0 | 49 | 4 | 99,71,45,67 | 99,48,0,0 |
| 5 | 1/0 | 66 | 3 | 99,80,52,72 | 99,50,0,0 |
| 6 | 14/2 | 67 | 6 | 99,86,60,76 | 99,30,0,0 |

Feedback 2; detune operatori 7,7,8,6,7,7 (7 è neutro). Oscillator sync ON.
Gli altri valori di key scaling sono espliciti in `presets()`.
Envelope1 esterno aperto: attack 0, sustain/release 50; velocity→volume
rimossa come nell'inizializzazione DX7 del firmware.

Valori Deluge 0–50: volume 29, pan 22, LPF 42/resonance 3, HPF 10,
chorus rate 8/depth 10, riverbero 12, EQ bass 21/treble 23.
Delay analogico ping-pong, sync XML 7 dotted, feedback 13.

### LYRA ACID01

Percorso trovato sulla SD: `SAMPLES/WAVETABLES/CommunityWavetables/Acid.wav`.
332710 byte; mono float32, 44100 Hz, chunk `clm ` con ciclo da 2048 campioni,
40 frame. File letto, non ricreato né spostato.

Valori 0–50: volume 24, pan 29, OSC A 42, OSC B/noise 0,
position 17, LPF 24/resonance 13, HPF 16/resonance 2.
ENV1 A/D/S/R 8/25/27/22; ENV2 5/31/9/24.
LFO1 triangolare libero, rate 5; LFO2 sinusoidale libero, rate 9.
Patch cable in unità display: LFO1→position +9, ENV2→position +7,
ENV2→LPF +12, LFO2→LPF +3; velocity→volume del template conservata.
Delay analogico ping-pong, sync XML 7 dotted, feedback 20;
riverbero 17, EQ bass 18/treble 21.

Nella song, oltre ai patch cable, automazioni interpolate:
position 11–31, LPF 17–31, HPF 16–21. I punti esatti sono in `build()`;
la modulazione si somma a questi valori base.

## P2 e fonti

`tools/delugexml/synthesis.py` aggiunge `DX7Operator`, `DX7Patch`, lettura e
scrittura del payload unpacked, `set_dx7()` e `set_wavetable()` singola.
I generatori di song usano queste API, senza costruire XML a mano.

- [Documentazione community DX7](https://delugecommunity.com/features/dx_synth/):
  OSC1 nel motore sottrattivo; envelope esterno aperto e velocity gestita dagli operatori.
- Firmware **b76ed39**, `src/deluge/processing/sound/sound.cpp`:
  lettura/scrittura `dx7patch` di 156 byte, `fileName` wavetable.
- Stessa build, `contrib/dx7/sysex-format.txt` e `dsp/dx/fm_core.cpp`:
  ordine e limiti dei parametri, algoritmo 5 a tre coppie.
- Payload reale di `refs/songs/Qbix.XML`: decodifica e ricodifica identica.

Restano fuori dall'API i banchi SYX, scelta engine DX7/random detune e
multisample wavetable. Device ancora da verificare con ascolto e risalvataggio:
la rilettura SysEx prova il trasferimento, non il suono.

## Verifiche e consegna

Otto test dedicati passano (sei per la sintesi, due per conservazione song).
Unittest discovery: 27/27. Suite generale precedente all'inserimento del nuovo
wrapper: 2305/2306; l'unico errore allora presente, anche in HEAD, era la
priorità non normalizzata di `midi-follow`, poi corretta nella matrice.
`musica.verifica()` e `musica.avvertenze()` vuote sulla song generata e riletta.

Caricati senza sovrascrivere file, con rilettura byte-identica:

| Destinazione | Byte | SHA-256 |
|---|---:|---|
| `/SONGS/DelugePal/LYRA VIAREGGIO01.XML` | 867443 | `f96b83f31a3cdfb4198342ecae5b20c0d494425a10319c44db5074990cd362b5` |
| `/SYNTHS/DelugePal/LYRA TINE01.XML` | 5712 | `96d79a6c48e218b95a9238546d1cf279d3bd6bf0b0bd74e7df2ee435ef245730` |
| `/SYNTHS/DelugePal/LYRA ACID01.XML` | 5952 | `1f7fa66c5dd339615cf90c5235042b3352a007efe0f81d513e5493cd7c45db1c` |
