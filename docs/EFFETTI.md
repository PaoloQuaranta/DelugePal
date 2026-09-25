# Effetti standard — P1

API in `tools/delugexml/effects.py`, target community `b76ed39`.
Test locali e prova sul dispositivo completati il 25 settembre 2026.

`FXSTD01.XML` caricata il 25 settembre 2026 in `/SONGS/DelugePal/`,
con rilettura byte-identica. La verifica del trasferimento non cambia lo
stato della prova audio.

L'utente ha poi confermato «funziona, risalvato». `FXSTD01 2.XML` scaricata
via SysEx (103268 byte, SHA-256 `a9ecd21496898c0eb6fd6290c215249792a3563d065246e8a5a8f6df9f5580c3`).
Il test `test_device_resave` confronta tutte le 15 sezioni: note, tipi e
configurazioni FX, parametri e mandata. Il firmware omette
`clippingAmount="0"` e arrotonda `roomSize` di 128 unità nella scala 2^31;
sono normalizzazioni compatibili col sorgente e non cambiano la prova.

## Livelli e API

| API | Nodo e scala |
|---|---|
| `set_delay(owner, ...)` | `sound`, `kit`, `audioTrack` o `song`: analogico/digitale, ping-pong, sync; feedback e rate 0–50 in `params_node` |
| `set_mod_fx(owner, ...)` | Tipo sullo stesso owner; rate, depth, feedback e offset 0–50 in `params_node` |
| `set_eq(node, ...)` | Parametri di preset, clip, noteRow o song; bass/treble 0–50, neutro 25; frequenze 0–50 |
| `set_distortion(owner, ...)` | Saturazione 0–15 sull'owner; bitcrush e decimation 0–50 in `params_node` |
| `set_reverb_send(node, amount)` | Mandata 0–50 nei parametri della parte |
| `set_reverb(song, ...)` | Riverbero globale esistente: modello e room_size, damping, width, hpf, lpf 0–50 |

Se `params_node` è omesso, i parametri vengono cercati nell'owner: utile
per i preset e per la song. In una song passare la clip per synth/kit/audio,
oppure la noteRow per un drum. La struttura della traccia audio sta in
`audioTrack`, non in `audioClip`. La funzione non risolve automaticamente
il legame tra owner e clip: il chiamante passa i due nodi corrispondenti.

Gli argomenti omessi conservano il valore, comprese le automazioni.
Impostare esplicitamente un valore sostituisce l'eventuale automazione
di quel parametro, come `sound.set`. Un errore di valore o un parametro
mancante non lascia scritture parziali. Le API non creano contenitori di
parametri incompleti. Il nodo strutturale delay può essere aggiunto usando
solo gli attributi riconosciuti dal firmware.

```python
from delugexml import effects as FX

FX.set_delay(inst, params_node=clip, analog=True, ping_pong=True,
             sync_level=7, sync_type='even', feedback=22)
FX.set_mod_fx(inst, params_node=clip, kind='chorus', rate=22, depth=32)
FX.set_eq(clip, bass=25, treble=32)
FX.set_distortion(inst, params_node=clip, saturation=4, bitcrush=0)
FX.set_reverb_send(clip, 18)
FX.set_reverb(doc.root, model='mutable', room_size=30, damping=35)
```

`sync_level` è **il valore XML assoluto**, non l'indice del menu e non una
durata in tick. L'API espone il sottoinsieme 0–9 (0 = libero) senza
attribuirgli nomi musicali: il firmware converte il valore rispetto a
`inputTickMagnitude`. `sync_type` è `even`, `triplet` o `dotted`, salvato
rispettivamente come 0, 10, 19.

I nomi mod FX sono quelli XML, sensibili alle maiuscole: `none`, `flanger`,
`phaser`, `chorus`, `StereoChorus`, `dimension`, `TapeWarble`, `grainFX`.
Gli ultimi tre sono accettati perché presenti nel firmware; la prova P1
qui descritta copre solo i quattro effetti standard.

Il riverbero globale usa i modelli `freeverb`, `mutable`, `digital` (0–2).
I cinque controlli 0–50 vengono convertiti con la rappresentazione float32
del menu e salvati come interi decimali 0–2147483647. Pan e compressore del
riverbero sono conservati; questa API non li modifica. La mandata resta un
normale parametro esadecimale della parte, separato dalla configurazione globale.

## Prova FXSTD01

Generare con `.venv/Scripts/python.exe tools/effetti_scritto.py`.
Richiede la song modello locale `refs/songs/TEMPL0.XML`, il preset pubblico
`refs/synths/TEMPL.XML` e la tabella di formattazione locale.
Il generatore scrive `out/FXSTD01.XML` e non trasferisce da solo sul Deluge.
Destinazione calcolata: `musica.destinazione('fxstd', 1)`.

Quindici sezioni, con solo DRY inizialmente attiva. Lanciare una sezione
alla volta. Stesso synth saw, volume 20, stesse quattro note corte nelle
prime due battute, poi due battute vuote per ascoltare le code; 100 BPM.

| Sezione | Confronto con DRY |
|---|---|
| DRY | Riferimento asciutto |
| DELAY DIGITAL / ANALOG | Feedback 22, sync XML 7, ping-pong attivo; cambia solo analog |
| DELAY TRIPLET / DOTTED | Stesso delay digitale, cambia solo syncType |
| FLANGER / PHASER / CHORUS / STEREO CHORUS | Rate 22, depth 32, feedback e offset 25 |
| EQ BASS / EQ TREBLE | Solo la banda indicata a 40, l'altra resta neutra a 25 |
| SATURATION | Saturazione 8 |
| DECIMATION / BITCRUSH | Solo la distorsione indicata a 32 |
| REVERB | Mandata 25 al Mutable globale: room 30, damping 35, width 50 |

Le code del delay/riverbero precedente possono attraversare il cambio
sezione: attendere che decadano prima del confronto. La mandata di
riverbero e il feedback delay sono a zero in tutte le altre famiglie.

La prova è stata aperta, ascoltata e risalvata. Il confronto del file
risalvato è automatizzato in `tests/test_effects.py`; la percezione del
risultato è la conferma dell'utente, non una misura acustica indipendente.

## Fonti

- [Menu community](https://delugecommunity.com/reference/menu_hierarchies/)
  e capitolo Effects del Guidebook, già riassunto in `ARCHITETTURA.md` §10c.
- [ModControllableAudio b76ed39](https://github.com/SynthstromAudible/DelugeFirmware/blob/b76ed39/src/deluge/model/mod_controllable/mod_controllable_audio.cpp): struttura delay/clippingAmount e parametri EQ/distorsioni.
- [Conversioni dei tipi FX](https://github.com/SynthstromAudible/DelugeFirmware/blob/b76ed39/src/deluge/util/functions.cpp): nomi esatti riconosciuti dal caricatore.
- [SyncType](https://github.com/SynthstromAudible/DelugeFirmware/blob/b76ed39/src/deluge/model/sync.h) e [Song](https://github.com/SynthstromAudible/DelugeFirmware/blob/b76ed39/src/deluge/model/song/song.cpp): codici sync, conversione dei livelli e serializzazione del riverbero.
- [Menu room size](https://github.com/SynthstromAudible/DelugeFirmware/blob/b76ed39/src/deluge/gui/menu_item/reverb/room_size.h) e [modelli](https://github.com/SynthstromAudible/DelugeFirmware/blob/b76ed39/src/deluge/dsp/reverb/reverb.hpp): scala e codici del riverbero.
