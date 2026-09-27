# Wavetable — verifica P2

## Stato al 27 settembre 2026

La matrice separa la wavetable singola, **chiusa**, dai range multipli,
**aperti con priorità P0** per il crash al reload. Questa distinzione
descrive il comportamento osservato sul firmware b76ed39.

`set_wavetable()` assegna un WAV singolo a un oscillatore. È stato usato
in LYRA VIAREGGIO per Acid, Allophones e Bowed Metal, con position, LFO,
inviluppi e filtri. L'utente ha ascoltato le revisioni creative e risalvato
la 04. Nel confronto fra `out/lyra_viareggio/LYRA VIAREGGIO04.XML` e
`out/lyra04_user_mix_latest.XML`, i tre percorsi WAV e la struttura degli
oscillatori sono identici; anche gli inviluppi e tutti i punti delle
automazioni sono conservati. Il Deluge normalizza il valore iniziale
dell'automazione e l'ordine/polarità dei patch cable, mentre il rough mix
cambia i volumi. I preset standalone Vox e Metal riletti dalla SD sono
byte-identici ai file caricati; resta da provarne il caricamento diretto.

## Range per nota

`set_wavetable_ranges()` e `wavetable_ranges()` leggono/scrivono intervalli
con limite superiore inclusivo. Il preset di prova assegna Acid fino a
MIDI 59, Allophones fino a 71 e Bowed Metal alle note successive. La song
WT RANGE TEST usa Do3, Do4 e Do5; è separata da LYRA.

La prima prova `WT RANGE01` ha prodotto un messaggio «file corrupted»;
la causa non è stata isolata. La successiva `WT RANGE02` lascia il WAV finale
in `osc1.fileName` e mette in `wavetableRanges` i due range inferiori.
Entrambi i file 02 sono stati caricati e riletti con hash identico.
L'utente conferma che **sia il preset sia la song 02 si aprono** e che Do3,
Do4 e Do5 producono tre timbri distinti. Ha quindi risalvato il preset
come `WT RANGE03`. Una prova più attenta ha chiarito che il preset si apre
e suona nella song da cui è stato salvato, ma **caricarlo in una song nuova
o dopo un riavvio fa crashare il Deluge**, già durante la preselezione.
La prima risposta non verificava quindi un caricamento da zero. Il target
è una nightly (`b76ed39`): il nesso causale con l'XML generato resta aperto.

Il file 03 scaricato dalla SD usa la forma canonica del writer del firmware:
tre `wavetableRange`, con `rangeTopNote` 59, 71 e assente nell'ultimo.
`wavetable_ranges()` rilegge esattamente le tre assegnazioni. Volume 32,
position 25 e gli altri parametri corrispondono alla versione generata;
il Deluge ha cambiato solo `arpeggiator.syncLevel` da 7 a 8 nel confronto
semantico con il preset 01. Un secondo salvataggio di `WT RANGE03`, scaricato
dopo riavvio, è byte-identico al primo (5.867 byte, stesso SHA-256). Il
crash sul caricamento da zero mostra che la validità XML, il round-trip
locale e il confronto semantico non bastano. Il file canonico scritto dal
Deluge e la nightly sono entrambi da investigare: non abbiamo ancora una
prova che attribuisca il difetto a uno dei due.

Nel sorgente di `b76ed39`, `Source::setOscType(WAVETABLE)` crea un range
iniziale con `topNote=32767`. `Sound::readSourceFromFile()` inserisce poi i
range letti dall'XML e restituisce `FILE_CORRUPTED` se trova un `topNote`
duplicato. Il writer omette `rangeTopNote` per l'ultimo range quando il
valore è 32767. Questa sequenza rende plausibile una collisione sul range
finale del file 03 caricato da zero; il file 02 evita quel secondo range
finale usando `osc1.fileName`. È una spiegazione del percorso di errore
previsto dal codice, non una prova che il crash osservato abbia solo questa
causa. Un preset creato interamente sul Deluge è ancora il confronto utile.

Il sottoinsieme affidabile comprende WAV mono singoli compatibili sulla SD,
position e modulazioni. `set_wavetable_ranges()` richiede ora
`experimental=True`: DelugePal rifiuta l'uso normale perché il preset
risalvato fa crashare il Deluge quando viene caricato da zero. La lettura dei
range esistenti resta disponibile. Il file 03 è stato scaricato integralmente
e conservato come prova per isolare il difetto. Dopo riavvio, il file sulla SD
è stato rinominato da `WT RANGE03.XML` a `WT RANGE03.BAK` nella stessa
cartella `SYNTHS/DelugePal`; risposta firmware `err=0`, elenco directory
confermato, rilettura `.BAK` byte-identica alla copia precedente (SHA-256
`d20a115664e3ffbeed7d84780ebbb25c72d2280e6d1cc1a073`). La cattura resta
locale e non viene pubblicata, perché contiene i parametri del corpus
personale. Anche `WT RANGE01.XML`, associato al primo errore, è stato
rinominato `WT RANGE01.BAK` nella stessa cartella (risposta SysEx `err=0`).
Il secondo `WT RANGE03.XML` è stato conservato localmente in
`out/wavetable_range/WT RANGE03.second_device.XML`, poi rinominato sulla SD
`WT RANGE03-2.BAK` (`err=0`, directory verificata). Prima di riabilitare
la scrittura ordinaria serve un confronto controllato con un preset multi
range creato interamente sul Deluge e caricato da zero sulla stessa nightly;
se anche questo crasha, ripetere su una build stabile o aprire una segnalazione
al firmware con i due file di prova.

Fonti: [manuale community sui range](https://delugecommunity.com/manual/device_overview/audio_files/);
firmware `b76ed39`, `src/deluge/processing/sound/sound.cpp`
(`readSourceFromFile`/writer), `src/deluge/processing/source.cpp`
(`setOscType`) e `src/deluge/storage/multi_range/multi_range.cpp`.
