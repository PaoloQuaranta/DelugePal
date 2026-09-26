# Oscillatore sample — prova P1

`tools/sample_oscillator_probe.py` crea quattro synth dal preset vuoto
`refs/synths/TEMPL.XML`. Su ciascuno assegna all'oscillatore 1 lo stesso Amen
break gia' presente sulla SD, tramite `kit.set_sample()`, e imposta il playback
con `kit.set_sample_playback()`. Le clip sono in sezioni separate e la prima e'
attiva: si lanciano le altre una alla volta.

Il campione e' `SAMPLES/sampleswap/advanced_operator_samplepack/drums/original AMEN.wav`,
268795 frame, 48 kHz stereo. La lettura SysEx del 26 settembre 2026
ha confermato la presenza sulla SD e la dimensione di 1075224 byte. A 171 BPM
dura circa quattro battute. Ogni clip contiene una nota lunga otto battute.

| Sezione | `loopMode` | `reversed` | `timeStretchEnable` | Atteso all'ascolto |
|---|---:|---:|---:|---|
| ONCE | 1 | 0 | 0 | Suona una volta e si ferma circa a meta' clip |
| LOOP | 2 | 0 | 0 | Ripete il break nella seconda meta' |
| REVERSE | 1 | 1 | 0 | Suona una volta dalla fine all'inizio |
| STRETCH | 3 | 0 | 1 | Distribuisce il break sulle otto battute |

Il significato dei quattro modi e' descritto nel
[guidebook Deluge, sezione 9.13](https://synthstrom-audible-deluge.s3.us-east-2.amazonaws.com/Deluge-Guidebook-4p1-OLED.pdf).

`out/SAMPLEOSC01.XML` e' stato validato e riletto senza errori o avvertenze.
La suite completa passa 2306/2306 test, incluso il nuovo test del probe.
Il 26 settembre 2026 il file e' stato caricato
in `/SONGS/DelugePal/SAMPLEOSC01.XML`; rilettura byte-identica di 32169 byte,
SHA-256 `58900d08d2252be6a8e9e093aabce8d631059a4622f6f6f2603cd6f5b79f2f4a`,
zero timeout, blocchi parziali o riaperture.

L'utente ha confermato **«funziona, risalvato»**. La copia
`/SONGS/DelugePal/SAMPLEOSC01 2.XML` e' stata recuperata via SysEx: 32001 byte,
SHA-256 `62a8a14a92295741ab43d7acbc104f9741a1673718be7fdc46ed7f9a86f67358`.
`musica.verifica()` e `musica.avvertenze()` sono vuote. Il confronto semantico
con l'originale conserva quattro synth e clip, tempo, nomi, sezioni, lunghezze,
note, percorso e zona del campione e, per ogni oscillatore, `type`, `loopMode`,
`reversed` e `timeStretchEnable`. Il firmware ha tolto `transpose="0"`,
`cents="0"` e `retrigPhase="-1"` ereditati dal preset vuoto e aggiunto
`timeStretchAmount="0"` a ciascuno dei quattro oscillatori sample.
Il confronto completo degli attributi trova anche una nuova `preview`,
lo stato della clip selezionata e tre differenze globali fuori dalla prova
(reverb `roomSize` 1288490112→1288489984, compressor `syncLevel` 4→3,
`songParams.tempo` 0x00003DB8→0x000042CC). Il BPM effettivo resta 171.
Queste differenze non cambiano i quattro playback verificati; non sono state
classificate come equivalenti per il resto della song.
Il P1 dell'oscillatore sample e' chiuso.
