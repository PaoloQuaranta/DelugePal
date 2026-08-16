# Test — la clip duplicata è fuori schermo?

**Data:** 12 agosto 2026
**Stato:** **CONFERMATA SUL DISPOSITIVO.** `SCROLLA` mostra 3 righe con la
quarta nascosta, `SCROLLB` ne mostra 4. Causa radice di HANDOFF.md §3.1.
**Correzione:** `scroll_song_view_to()` in `tools/delugexml/song.py`, chiamata
da `duplicate_clip()`. Coperta da `test_scroll_song_view` in `tests/test_all.py`.

> Rigenerando `SCROLLA` con la correzione attiva si ottiene un file
> **byte-identico a `SCROLLB`**, cioè esattamente quello che il dispositivo ha
> approvato (sha256 `7d52543c…dcf2a`).

Il documento resta come traccia del metodo: l'esperimento a un byte di
differenza è ciò che ha chiuso un'indagine ferma da due sessioni.

---

## L'ipotesi

La clip duplicata **viene caricata correttamente**. Non si vede perché finisce
alla riga 8 di una griglia che ne mostra 8, numerate 0–7: è appena sotto il
bordo inferiore dello schermo.

In song view ogni clip è una riga, e la finestra visibile parte da
`yScrollSongView`. La clip di indice `i` sta alla riga di schermo `i - yScroll`.

`Perche.XML` ha 3 clip e `yScrollSongView="-5"`: occupano le righe 5, 6, 7, cioè
esattamente le ultime tre. Aggiungendo una quarta clip **senza toccare lo
scroll**, quella va alla riga 8, che non esiste.

`duplicate_clip()` non tocca `yScrollSongView`. La stringa `yScroll` non compare
da nessuna parte nella libreria.

## Perché è credibile

Tre livelli, nell'ordine che vale:

1. **Manuale**, cap. 7 Song View (guidebook righe 4522–4527):

   > «Individual clips compressed to one row each in song view. The rows can be
   > navigated up and down **beyond the 8 physically displayed**.»

   e riga 676: «Rows represent clips.»

2. **File scritti dal dispositivo.** Quando il Deluge ha clonato una clip
   (`refs/songs/Gen2_cloned_by_deluge.XML`), ha spostato lui stesso
   `yScrollSongView` da `-5` a `-4`. Mantiene lo scroll quando aggiunge una
   riga; noi no.

3. **La clip era caricata.** Nel file risalvato dal dispositivo la frazione di
   `timePerTimerTick` è cambiata (`-238609295` → `-238534430`): è una
   riserializzazione dalla memoria, non una copia del file. Quindi il parser del
   Deluge l'aveva accettata. Il problema non è mai stato il caricamento.

Questo spiega anche perché il confronto fra i file non ha mai trovato niente:
**la differenza non era nella clip.** Era in un attributo del nodo `<song>`.

## Il test

Due file sulla SD in `E:\SONGS\`, che differiscono per **un solo byte**
(offset 1084, `yScrollSongView` `-5` contro `-4`). Entrambi derivano da
`Perche.XML` con la clip 1 duplicata in sezione 1, `colourOffset="-100"` per
renderla riconoscibile a colpo d'occhio.

| file | clip | yScroll | righe occupate | previsione |
|---|---|---|---|---|
| `SCROLLA.XML` | 4 | `-5` | 5, 6, 7, **8** | si vedono **3** righe; la quarta è nascosta sotto |
| `SCROLLB.XML` | 4 | `-4` | 4, 5, 6, 7 | si vedono **4** righe; la nuova è l'ultima, di colore diverso |

### Procedura

1. Carica `SCROLLA.XML`, premi `[SONG]`. **Conta le righe accese.**
2. Sempre in song view, **scrolla giù di una riga** (`▼`). Se compare una quarta
   riga di colore diverso → ipotesi confermata.
3. Carica `SCROLLB.XML`, premi `[SONG]`. **Conta le righe accese**, senza
   scrollare.

### Come si legge l'esito

| A senza scroll | A dopo scroll ▼ | B senza scroll | conclusione |
|---|---|---|---|
| 3 righe | 4 righe | 4 righe | **confermata.** Causa radice trovata, la correzione è aggiornare `yScrollSongView` quando si accoda una clip |
| 3 righe | 3 righe | 3 righe | smentita: la clip non c'è davvero, l'ipotesi è sbagliata |
| 4 righe | — | 4 righe | il bug non si riproduce: qualcosa è cambiato con la nuova nightly |

C'è anche una prova a costo zero: `Gen2.XML` è già sulla SD (5 clip,
`yScroll="-4"`, quindi la clip `GEN` sta alla riga 8). Caricala e scrolla giù di
una riga: se `GEN` compare, è la stessa conferma.

## Se confermata

La correzione è in `duplicate_clip()` e in qualunque funzione accodi clip:
dopo l'append, se l'ultima clip finisce sotto la riga 7, alzare
`yScrollSongView` quel tanto che basta — che è esattamente ciò che fa il
dispositivo. Da coprire con un test in `tests/test_all.py`.

**Non dichiarare niente di tutto questo risolto prima del punto 3.**
