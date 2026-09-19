# Elettronica / IDM astratta — polimetro, precisione e trasformazione

⚠️ **PERIMETRO.** Questa istruzione copre un angolo preciso dell'IDM: ritmo
programmato non quadrato, strati di periodo diverso, percussioni metalliche,
pochi centri tonali e timbro che cambia lentamente. È una direzione originale:
si usano variabili di mestiere, non melodie, riff, pattern o firme sonore di un
artista specifico.

> **La cosa da capire:** il movimento non viene dallo swing né dal caso. Nasce
> dall'interazione deterministica di sequenze brevi che hanno lunghezze diverse.
> Ogni strato è semplice; la figura complessiva non si ripete dentro il pezzo.

Il grado di prova è `[DEC]`: materiale, forma e livelli sono decisioni di questo
pezzo. Il comportamento delle clip a lunghezza arbitraria e delle istanze lunghe
in arranger è `[OSS]` nel formato e nella libreria. Il ciclo d'ascolto si è
chiuso su `IDM04`: ritmo, forma e densità erano già stati approvati in `IDM03`;
la quarta versione ha sostituito il finto drone a campione con un synth continuo.

## 1. Il polimetro: una traccia per periodo

Su una sola traccia il Deluge suona una clip per volta. Perciò ogni periodo
indipendente vive su una **traccia propria**. L'esempio usa quattro cellule in
sedicesimi:

| strato | lunghezza | materiale |
|---|---:|---|
| THUD-A | 6/16 | due masse, `x..x..` |
| CLICK | 5/16 | rim + clave fantasma |
| HAT | 7/16 | trama sottile, chiusa da maraca |
| METAL | 11/16 | cowbell e cymbal radi |

THUD-B e THUD-C conservano il periodo di 6/16 ma cambiano attacchi e posizione
dell'accento; l'arranger alterna le tre cellule senza aggiungere un quinto
periodo al polimetro.

I periodi 5, 6, 7 e 11 tornano tutti insieme dopo **2310 sedicesimi = 144,375
battute**: il pezzo dura 40 battute, quindi la figura globale non si ripete.
Questo è polimetro contro un 4/4 sottostante, non tempo dispari.

La lunghezza si imposta in tick con `song.set_clip_length(clip, n * 24)`; in
arranger `arranger.place(..., length=...)` stende una singola istanza e lascia
che la clip si ripeta secondo il proprio periodo.

## 2. Il feel è dritto

`song.set_swing(doc, 50)`. Qui la precisione meccanica è una parte del carattere:
spostare i levare con lo swing renderebbe tutti gli strati più simili e toglierebbe
nitidezza alla loro interferenza. Il movimento viene dalle **fasi**, non dal
microtiming umano.

## 3. Il glitch articola spesso, senza diventare continuo

Due clip GLITCH da una battuta contengono burst complementari a trentaduesimi,
rim e clave. Si alternano in **otto battute isolate**, distanti quattro o cinque
battute: abbastanza frequenti da diventare un vocabolario del pezzo, mai tanto
continue da trasformarsi in un tappeto.
Se il retrigger è continuo smette di articolare la forma e diventa una superficie
uniforme — lo stesso difetto che `MU.reazione` chiama piattezza.

## 4. Il centro tonale minimo

Il solo materiale intonato è un drone **Re2 + La♭2**, un tritono tenuto. La clip
deve essere cromatica:

```python
song.set_key_mode(cDrone, False)
song.fit_clip_scroll_to_notes(doc, cDrone)
```

L'ordine conta: dopo il passaggio a modalità cromatica si rifà lo scroll, altrimenti
le note possono essere corrette ma invisibili nella clip view.

## 5. Il timbro si muove più delle altezze

Il drone non usa campioni: nasce dal synth subtractive del Deluge. Un
triangolo porta il corpo e un `analogSaw`, scordato di −7 cent, porta le
armoniche che il filtro può trasformare; due voci di unisono (`detune 5`,
`spread 14`) evitano una linea perfettamente immobile. L'inviluppo di ampiezza
ha attacco 12, sustain 50 e release 24: la nota resta realmente sostenuta per
tutta la sua durata, invece di seguire il decadimento registrato di un
multisample.

Due automazioni percorrono le 36 battute in cui è attivo:

- `lpfFrequency`: 40 → 48;
- `lpfResonance`: 12 → 30.

La rampa resta nella fascia aperta approvata nell'ascolto precedente, ma ora
muove lo spettro prodotto dagli oscillatori continui. La prima versione usava
un multisample Rhodes one-shot: il filtro poteva cambiarne il colore, non
impedire al campione di decadere come un piano elettrico.

Sono punti di partenza `[DEC]`, non leggi. La trasformazione lenta tiene insieme
la forma mentre le percussioni cambiano continuamente relazione fra loro.

## 6. La forma: accrezione e sottrazione

Niente build/drop obbligatorio. L'esempio dispone direttamente le istanze:

```text
0–3    THUD-A + CLICK + HAT
4–11   + METAL + DRONE; primo cambio della cassa a battuta 8
12–19  densità 4–5, con una terza cellula THUD da battuta 16
20–27  interludio fratturato: 3–4 ruoli, mai sola cassa
28–39  ritorno pieno, THUD variato e glitch distribuiti
```

La densità non scende sotto tre ruoli nelle prime 28 battute. Il contrasto del
centro non nasce più da un vuoto lungo ma da sottrazioni brevi: CLICK e HAT si
passano il bordo alto mentre il drone resta presente. La cassa conserva il
periodo 6/16 ma alterna tre disegni, quindi il fondamento cambia senza perdere
il polimetro.

## I vincoli

- una traccia per periodo indipendente;
- periodi semplici, interazione complessa: niente random necessario;
- swing 50;
- glitch frequente ma discontinuo, in almeno due gesti;
- poche altezze, timbro in movimento;
- `fit_clip_scroll_to_notes()` dopo aver reso cromatica la clip;
- ritmo, suono e forma si chiudono solo ascoltando il Deluge.

## L'esempio lavorato

`tools/idm_scritto.py`: 90 BPM, quattro periodi 5/6/7/11, tre cellule THUD,
kit 808 usato come tavolozza metallica, due gesti glitch, drone synth Re–La♭ e
forma di 40 battute per accrezione/mutazione. La revisione destinata
all'ascolto è `IDM04`; `IDM03` resta la versione approvata per ritmo e forma,
mentre `IDM01` è la prima versione e `IDM02` il tentativo di trasferimento
incompleto. Nessuna versione viene cancellata o sovrascritta.

### Cosa ha cambiato l'ascolto

| versione | riscontro | correzione successiva |
|---|---|---|
| `IDM01` | prima metà scarna; sezione di sola cassa debole; glitch troppo radi; cassa invariata; drone muto | densità minima di tre ruoli, niente cassa sola, otto glitch, tre cellule THUD, cutoff riportato in fascia udibile |
| `IDM02` | trasferimento incompleto | nessuna cancellazione o sovrascrittura; nuova destinazione |
| `IDM03` | ritmo e forma approvati; il drone suona ancora come un piano corto | diagnosi della sorgente: `Tal Rhodes` è un multisample one-shot, non un oscillatore continuo |
| `IDM04` | «ok» | chiusura: drone subtractive, tutto il resto invariato |

Le correzioni non sono ricette universali, ma tre controlli riusabili per questo
territorio: la sottrazione non deve lasciare un vuoto non intenzionale; il ruolo
che dà massa deve poter mutare senza perdere il proprio periodo; un drone richiede
una **sorgente continua**, non soltanto note lunghe e sustain alto.
