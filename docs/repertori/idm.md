# Elettronica / IDM

**Parziale.** Compilata il 19 settembre 2026. Copre l'IDM astratta e meccanica:
polimetro deterministico, percussioni metalliche, glitch discontinuo, centro tonale
minimo e timbro in trasformazione. Non pretende di coprire ambient-IDM,
drill'n'bass, braindance melodica o glitch massimalista.

Il dettaglio operativo sta in [idm.md](../istruzioni/idm.md); l'esempio in
`tools/idm_scritto.py`. Grado di prova: `[OSS]` meccanismo del Deluge · `[DEC]`
scelte compositive. `IDM04` è stata ascoltata e accettata sul dispositivo; la
scheda resta parziale perché descrive un solo territorio dell'IDM, non perché
l'esempio sia ancora in attesa di verifica.

---

## 1. Cos'è, e cosa non è

**Parziale.** Qui IDM significa elettronica programmata in cui la complessità
emerge da regole semplici: periodi diversi, sottrazione, precisione meccanica e
trasformazione timbrica. **Non è** techno four-on-the-floor, DnB guidata da un
break, né casualità senza memoria. È una sola regione del repertorio.

## 2. Metro e griglia

`[DEC]` 4/4 sottostante, griglia a sedicesimi e trentaduesimi per i retrigger.
Sopra il 4/4, clip indipendenti di **5, 6, 7 e 11 sedicesimi**: il polimetro
sposta continuamente gli accenti senza cambiare il metro globale.

## 3. Tempo

`[DEC]` **90 BPM** nell'esempio: abbastanza lento da rendere leggibili i singoli
incastri e abbastanza veloce perché i burst a 1/32 restino gesto, non tremolo.

## 4. Feel

`[DEC]` **Dritto, swing 50.** La precisione è il carattere. Il movimento viene
dallo sfasamento dei periodi, non dal microtiming; uno swing comune a tutti gli
strati ne indebolirebbe la separazione.

## 5. Ruoli e spartizione

`[DEC]` THUD dà massa, CLICK definisce il bordo, HAT riempie l'alto, METAL porta
gli accenti lunghi; GLITCH è punteggiatura strutturale ricorrente; DRONE è l'unico strato
intonato. Le parti non si spartiscono per battere/levare ma per **registro,
durata e periodo**.

## 6. Dinamica

`[DEC]` Accenti gerarchici dentro ogni cellula: spesso il primo evento è più
forte, ma nelle variazioni THUD l'accento ruota fino al colpo finale. Gli altri
eventi funzionano da fantasmi. Il glitch decade dentro ogni burst. La dinamica
non è randomizzata: deve rendere riconoscibile ciascun periodo.

## 7. Armonia

**Parziale.** Nessuna progressione. Il campo armonico è il tritono **Re–La♭**,
tenuto e cromatico, scelto come instabilità statica. Manca ancora una pratica
armonica più ampia dell'IDM melodica o ambientale.

## 8. Melodia e ornamentazione

**Parziale.** Non c'è una melodia tonale. Il materiale sviluppato è ritmico:
le cellule ricorrono in fasi diverse e due gesti di burst a 1/32 ornamentano
otto snodi.
Resta fuori una linea intonata o un motivo trasformato.

## 9. Forma e densità

**Parziale.** `[DEC]` Forma di 40 battute per **accrezione/mutazione**:
3 strati → 5 strati → interludio a 3–4 ruoli → ritorno pieno. Tre cellule di
cassa sullo stesso periodo di 6/16 evitano un fondamento identico dall'inizio
alla fine; otto eventi alternano due gesti glitch.
La prima versione scendeva fino alla sola cassa e lasciava la prima metà troppo
vuota; l'ascolto ha imposto almeno tre ruoli attivi nelle prime 28 battute.
Non è build/drop: la tensione viene da quanti periodi interagiscono. Manca una
forma più lunga o una seconda famiglia di materiali.

## 10. Sul Deluge

`[OSS]`+`[DEC]` Una traccia kit per periodo, perché una traccia suona una clip
per volta. `S.set_clip_length()` assegna le lunghezze arbitrarie;
`A.place(..., length=...)` stende le ripetizioni in arranger. `MU.automatizza`
muove cutoff e risonanza del drone. La clip del drone è cromatica e lo scroll
va rifatto dopo `S.set_key_mode(False)`. Il drone usa il synth subtractive
vuoto: triangolo + `analogSaw`, due voci di unisono e inviluppo sostenuto;
nessun multisample.

## 11. Trappole del generatore

`[DEC]`

- mettere tutti gli eventi in una clip: si perde l'indipendenza dei periodi;
- randomizzare: distrugge l'identità delle cellule e non crea sviluppo;
- aggiungere swing per riflesso: qui la precisione è il feel;
- glitch continuo: da punteggiatura diventa superficie piatta; l'esempio usa
  otto battute-evento isolate su quaranta e alterna due gesti;
- usare un multisample one-shot come drone: l'inviluppo può restare aperto ma
  la registrazione continua a decadere; l'esempio usa oscillatori subtractive;
- chiudere troppo il cutoff nel registro grave: il drone può risultare muto;
  l'esempio resta fra 40 e 48;
- troppe altezze: competono con il fenomeno ritmico invece di incorniciarlo;
- cambiare key mode senza rifare lo scroll: note giuste ma invisibili;
- chiamare «IDM» un solo pezzo: questa scheda resta dichiaratamente parziale.
