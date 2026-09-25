# Filtri, routing e morph

Supporto verificato sulla build `2d7cdf8`, compresi ascolto e risalvataggio.

```python
from delugexml import structure as ST

ST.set_filter(strumento, lpf='SVF_Band', hpf='HPLadder', route='L2H',
              lpf_morph=25, hpf_morph=15, params_node=clip)
```

Per un preset omettere `params_node`: usa il suo `defaultParams`. Per un
drum della song passare la noteRow come `params_node`. Su un kit intero
passare il kit e la clip, che contiene `kitParams`.
La funzione valida tutti i valori e la presenza dei parametri prima di
modificare qualunque nodo. I morph sono interi 0-50; non passarli conserva
gli eventuali valori o automazioni esistenti. Passarli sostituisce anche
un'eventuale automazione, come `sound.set`.

Modi e routing appartengono allo strumento e cambiano tutte le sue clip.
Morph, drive e FM sono parametri della singola clip. `sound.get/get_raw`,
`sound.set/set_raw`, patch cable e automazioni usano sempre i nomi XML
`lpfMorph` e `hpfMorph`.

| Slot / modo | Terzo parametro |
|---|---|
| LPF SVF_Band / SVF_Notch | 0 passa-basso, 25 band/notch, 50 passa-alto |
| HPF SVF_Band / SVF_Notch | 0 passa-alto, 25 band/notch, 50 passa-basso |
| LPF 12dB / 24dB / 24dBDrive | drive |
| HPF HPLadder | filter FM |
| Off | filtro disattivato, valore conservato |

Routing: `H2L` HPF -> LPF; `L2H` LPF -> HPF; `PARA` parallelo.
Il vecchio `flanger` osservato nel corpus non compare nella mappa firmware
corrente e richiede l'esplicito `force=True`.

## Prova FILTER01

Generatore: `python tools/filtri_scritto.py`. 100 BPM, Do maggiore,
una nota Do3 per battuta, nove strumenti distinti in nove sezioni.
Lanciare **le sezioni**, una alla volta, per fermare la precedente.
Solo ROUTE H2L e' attiva al caricamento; usare lo scroll per le nove righe.

| Sezione | Nome | Prova |
|---|---|---|
| 0 | ROUTE H2L | LPF 24dB e HP ladder, HPF prima |
| 1 | ROUTE L2H | Stessi parametri, LPF prima |
| 2 | ROUTE PARA | Stessi parametri, parallelo |
| 3 | LP BAND | Morph SVF band nello slot LPF |
| 4 | LP NOTCH | Morph SVF notch nello slot LPF |
| 5 | HP BAND | Morph SVF band nello slot HPF |
| 6 | HP NOTCH | Morph SVF notch nello slot HPF |
| 7 | LP DRIVE | Drive ladder 24dB |
| 8 | HP FM | Filter FM HPLadder |

Le sezioni 3-8 hanno quattro battute con parametro a gradini **0, 25, 50, 0**.
L'altro filtro e' spento. Frequenze LPF/HPF 28/22, risonanze 20/25,
volume 24 e oscillatore saw a 40; niente riverbero, delay o patch cable.
Per i due ordini in serie la differenza puo' essere sottile: verificare
anche la voce FILTER ROUTE nel menu. Per HP FM ascoltare soprattutto la
differenza fra prima e terza battuta.

Caricato il 25 settembre 2026 in `/SONGS/DelugePal/FILTER01.XML`, 63015 byte.
Rilettura SysEx identica, SHA-256:
`43999ebedd3bbf59af744b7c46727369a34f91a316e8e28b441deb3b11b7c3f5`.
`musica.verifica` e `musica.avvertenze`: vuote.

Il 25 settembre 2026 l'utente ha ascoltato le nove sezioni e confermato:
**«funziona»** `[OSS]`. Ha risalvato come `FILTER01 2`; la rilettura SysEx
misura 62575 byte, SHA-256
`e3ec66cfab4b3ff3fe5f4284fdd9bddce953a3dce55a5f07799db65b774dd0d7`.
Il confronto semantico conserva esattamente i nove modi LPF/HPF, i routing
H2L/L2H/PARA, i blob completi `lpfMorph`/`hpfMorph`, le 36 note con tutti i
campi, lunghezze, sezioni e BPM. `verifica` e `avvertenze` restano vuote.
Il firmware ha soltanto normalizzato ordine degli attributi, nodi vuoti e
alcuni stati globali/di vista; per questo il file non e' byte-identico.
