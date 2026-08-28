# Lo stimatore per passo: prendere la decisione che la casella 6 dichiara

**Progetto approvato il 26 agosto 2026.** Chiude il punto aperto che il ramo
`groove-midi` ha lasciato in `HANDOFF.md` §7 e §6-terdecies, e che
`docs/repertori/jazz.md` dichiara nella sezione «Il bordo fra due passi»:

> Un template è per definizione **per passo**, e un batterista che anticipa di
> mezza semicroma non ci sta dentro. Chiuderlo vorrebbe dire cambiare **come si
> aggrega** — non come si toglie lo swing — ed è una decisione di disegno che
> questa casella **non prende**: la dichiara, e la lascia a chi verrà.

Questo documento è chi verrà. **Non ripara un difetto**: sceglie fra stimatori,
e la scelta si fa con una misura, non con un argomento.

---

## 1. Il meccanismo, detto stretto

`profilo_da_colpi()` sceglie il passo con `round(dritta / passo_tick)` — il
**più vicino** — quindi `|residuo| <= mezzo passo` (12 tick) per costruzione.
Ne segue che un colpo che anticipa il suo passo di più di 12 tick non esce come
anticipo grande: esce come **ritardo grande sul passo precedente**. Il segno si
rovescia.

L'aggregazione poi è una mediana per cella `(strumento, passo % 16)`. Un gesto
la cui dispersione attraversa il confine finisce **contato in due celle con
segni opposti**, e la cella più numerosa decide il segno di ciò che si scrive.

⚠️ **Pesa sul charleston a pedale e quasi su nessun altro**, e la ragione non è
il charleston: è che mette il **43,7%** dei suoi colpi su due soli passi.
Rullante, cassa e ride spargono i colpi su otto passi o più, e una cella
ribaltata non li muove. La voce su cui la casella 6 poggia la conclusione più
forte è quindi anche la più esposta allo stimatore.

---

## 2. Cosa si tocca, e cosa NON si tocca

Si tocca **un punto solo** della catena: come si sceglie `passo` a partire da
`dritta`, in `tools/delugexml/groove.py`. Tutto il resto dell'ordine dichiarato
nel docstring di `profilo_da_colpi()` resta identico.

| | |
|---|---|
| origine del kit (`GR.origine()`) | **non toccata** |
| misura del BUR e `_senza_swing()` | **non toccati** |
| il residuo riportato, `dritta − passo·passo_tick` | **stessa formula** |
| `GR.scala()` | **non toccata** — guarda solo le velocity, che non dipendono dalle posizioni |
| firma di `MU.applica_groove()` | **invariata** |

Ne segue, e va scritto perché è la parte che nessuno deve andare a ricontrollare
per conto suo:

- **la scala di velocity della casella 6 non si muove**, perché `scala()` non
  legge posizioni;
- **la casella 4 non si muove**, perché il BUR si misura *prima*
  dell'assegnazione dei passi;
- **il «15 su 15» delle fasi grezze non può muoversi**, perché non passa da
  nessuna catena. Se si muove, l'errore è nostro e sta negli strumenti di
  misura, non nello stimatore.

---

## 3. I tre tagli, dietro un parametro

`profilo_da_colpi(..., taglio=...)` con tre valori, e **`'vicino'` resta il
default** finché la misura del §4 non ha scelto. Il default non cambia nello
stesso diff che introduce i tagli, per decisione: cambiare stimatore e cambiare
default insieme renderebbe illeggibile quale delle due cose ha mosso un numero.

Una funzione sola, per voce, ritorna uno **spostamento del taglio** in tick;
poi `passo = round((dritta − spostamento) / passo_tick)`.

| valore | lo spostamento è | |
|---|---|---|
| `'vicino'` | `0` | l'attuale `round()`, il termine di paragone |
| `'voce'` | la media circolare delle fasi della voce sulla griglia dei passi, **su tutti i suoi colpi** | stessa aritmetica di `GR.origine()`, **senza la sua finestra** — vedi sotto |
| `'rado'` | il **centro dell'arco vuoto più largo** della voce, meno mezzo passo | «non tagliare attraverso un gesto». Nessun parametro — vedi la correzione sotto |

⚠️ **`'voce'` NON può chiamare `GR.origine()`, e questa correzione è del 26
agosto 2026.** Una prima stesura di questa spec diceva «riuso letterale».
Misurato: `origine()` tiene solo i colpi dentro `finestra = 0,25 · passo`, e
sul charleston di `drummer10/session1/1` ne tiene **58 su 143** — cioè scarta
proprio quelli anticipati, che sono il fenomeno. Il numero che ne esce è
**−0,40 tick** invece di **−8,80**, e `'voce'` così non sposterebbe nessun
passo: sarebbe un candidato finto, che passa il confronto senza aver fatto
niente.

La finestra di `origine()` **non è un difetto e non va tolta di là**: serve a
tenere fuori dalla stima dello scarto comune del kit i levare swingati, che
stanno a 8 tick su 24 dalla griglia dei passi. Ma qui lo swing è **già stato
tolto** da `_senza_swing()` due righe sopra, e un levare swingato è ormai *su*
un passo, non fra due. La ragione della finestra non si trasporta, quindi
`'voce'` è una funzione **sorella**, con la stessa aritmetica circolare e senza
finestra, e il docstring dell'una deve nominare l'altra dicendo perché
differiscono.

⚠️ **`'voce'` non è nemmeno `origine()` del kit applicata due volte.** `origine()` toglie
lo scarto comune a tutto il kit e lo toglie *davvero*, lasciando a ogni
esecuzione uno zero arbitrario. Qui lo spostamento della voce si usa **solo per
decidere il passo** e non viene sottratto dal residuo riportato: il numero che
esce resta `dritta − passo·passo_tick`, cioè misurato rispetto alla griglia
vera. Confondere le due cose toglierebbe il feel invece di collocarlo.

⚠️ **CORREZIONE DEL 26 AGOSTO 2026, in attuazione: `'rado'` non ha parametri.**
Questo paragrafo diceva che `'rado'` ha **due parametri aperti** — la larghezza
della finestra di densità e la condizione di ripiego — da chiudere con una
misura di sensibilità. Attuato, quel criterio ha prodotto tre difetti, tutti
misurati sul corpus e sui casi sintetici:

1. **il taglio si incollava.** Il minimo di densità è un **altopiano** — un
   arco intero senza colpi — e l'argmin ne prendeva il primo punto della
   scansione, che sta sempre a fase 0. Traslando la voce di −4, −2, 0, +2, +4
   tick lo spostamento restava **−12,00 tutte le volte**. Sotto il criterio del
   §4, `'rado'` sarebbe stato bocciato per un difetto di contabilità invece che
   per la sua idea: **un fantoccio**;
2. **il ripiego non poteva scattare.** Il caso «semicrome piene» e la
   condizione `minimo >= ripiego · medio` si contraddicono: dati esatti sulla
   griglia collassano tutti su una fase sola, quindi il minimo è 0 comunque;
3. **la regola che doveva fissare la larghezza non decideva.** Su 118 voci del
   corpus jazz, «voci che si muovono oltre 1 tick» fa **35 → 25 → 36** per
   larghezze 2 → 3 → 4: non-monotona, nessun pianoro.

Il criterio corretto — **il centro dell'arco vuoto più largo** — li chiude
tutti e tre: trasla coi dati (rampa di pendenza 1, misurata), dà spostamento
**esattamente 0** sulle voci già sulla griglia per costruzione, e **non ha
nessun parametro da tarare**. Resta una domanda, e la misura il piano: se quel
vuoto sia sempre un vuoto *vero*, cioè quanto il buco più largo superi il buco
medio. Se non lo superasse, il centro sarebbe arbitrario — ma è una cosa da
misurare, non da presumere.

### 3.1 La conseguenza da accettare, e il limite che si sposta

Tutt'e due i candidati fanno sì che **`Passo.scarto` possa superare mezzo
passo**: è l'unico modo di dire «anticipa di mezza semicroma» invece di dire
«è in ritardo sul passo prima». Il limite dichiarato passa quindi da
`|scarto| <= passo_tick / 2` a `|scarto| < passo_tick`, e va scritto nel
docstring di `Passo` accanto alla riga del segno.

Ne segue che `MU.applica_groove()` può posare una nota **nel territorio del
passo accanto**. È voluto. Va però verificato che due note su passi adiacenti
non finiscano sullo **stesso tick**, e se può accadere il rapporto deve dirlo:
un'operazione silenziosa non è correggibile.

---

## 4. La prova che decide: linearità sotto traslazione per voce

**Il criterio, scelto il 26 agosto 2026:** uno stimatore è uno stimatore se la
sua risposta **segue la cosa che misura**. Si trasla **una voce sola** di δ
tick e si richiede che la posizione dichiarata da quella voce si muova di δ.
`round()` dà una sega che ripiega al bordo; una retta di pendenza 1 è il
comportamento sano.

Perimetro: le esecuzioni `jazz` `beat` `4-4` del Groove MIDI meno
`FUORI_DALLO_SWING`, ogni voce con almeno 40 colpi, δ ∈ {−8, −6, −4, −2, 0,
+2, +4, +6, +8} tick. Grandezze riportate per stimatore: **pendenza mediana**,
**scarto massimo dalla retta**, e **quante voci mostrano un salto ≥ mezzo
passo**.

**«Posizione dichiarata» va definita, se no la misura non è ripetibile.** Per
una cella `k` la posizione dichiarata è `k · passo_tick + scarto`, cioè dove
`applica_groove()` poserebbe davvero la nota. La grandezza della voce è la
**mediana su tutte le sue celle forti** (almeno 10 colpi a δ = 0) dello
spostamento rispetto a δ = 0.

⚠️ **E le celle vanno appaiate fra un δ e l'altro, non confrontate per numero
di passo.** È proprio il punto: uno stimatore che ripiega **sposta un gesto da
una cella all'altra**, quindi `k` cambia mentre il gesto è lo stesso. Le celle
si appaiano per **posizione dichiarata più vicina** a δ = 0, così che un gesto
che cambia `k` senza cambiare posizione risulti **continuo**: quel che deve far
saltare la curva è il ripiegamento dello stimatore, non la contabilità.
Appaiando per numero di passo si confronterebbero due popolazioni diverse sotto
la stessa etichetta, e ne uscirebbe un salto che non dice niente di come lo
stimatore tratta il gesto.

⚠️ **La trappola di questa misura, e sta scritta qui prima che qualcuno la
scopra sbagliando.** Traslare una voce sola muove anche `origine()` del kit, di
circa `δ · (colpi della voce / colpi totali)`, e per la stessa ragione può
muovere il BUR. Chi non lo neutralizza misura *anche quello* e conclude che
nessuno stimatore è lineare. **Origine e levare si congelano ai valori di
δ = 0** e si passano dentro; il piano deve verificarlo con un caso in cui il
congelamento è visibile, non darlo per fatto.

⚠️ **Due criteri sono stati considerati e scartati, e il motivo va tenuto.**
L'errore di ricostruzione per inversione — riscrivere il pattern col template e
confrontarlo coi colpi veri — **premia lo stimatore rotto**: spezzare un gesto
in due celle rende ciascuna delle due mediane più stretta, quindi l'errore
scende. E la tenuta delle conclusioni della casella 6 come bersaglio sarebbe
fabbricare la conclusione, che è esattamente il difetto della finestra di
grazia.

---

## 5. Cosa la sonda ha già mostrato, e cosa non mostra

Misurato il **26 agosto 2026** `[OSS]`, su due esecuzioni nominate, sul
charleston a pedale, celle con almeno 10 colpi — `passo: scarto/colpi`:

**`drummer10/session1/1`** (jazz/swing, 124 BPM, 143 colpi di pedale)

| stimatore | passi 3 e 4 | passi 11 e 12 | battere in minoranza |
|---|---|---|---|
| `'vicino'` (oggi) | `3:+3,8/41` `4:−8,3/29` | `11:+0,7/42` `12:−9,8/19` | **[4, 12]** |
| `'voce'` | `3:−3,1/20` `4:−10,7/50` | `11:−3,1/32` `12:−11,2/34` | nessuno |
| `'rado'` | idem | idem | nessuno |

**`drummer1/session3/2`** (jazz/swing, 185 BPM, 390 colpi di pedale) — che il
rovesciamento **non ce l'ha**: i due candidati non ce lo introducono, e le
celle si muovono di meno di un tick e mezzo.

Due cose che questa sonda **non** dice, e che il lavoro deve andare a prendere:
è **due esecuzioni**, quindi `[OSS]` e non `[MIS]`; e non ha misurato **nessuna
linearità** — mostra che il sintomo sparisce, che è il criterio scartato al
§4, non quello scelto.

⚠️ **Una previsione sbagliata, registrata perché è istruttiva.** Prima di
misurare, questo stesso documento stava per dichiarare morta la strada
`'voce'`: il ragionamento diceva che la media circolare di un gesto a cavallo
del confine vale circa **−1 tick**, quindi non sposterebbe nessun passo.
Misurata, sul charleston di `drummer10/session1/1` vale **−8,80 tick**
(concentrazione R = 0,16). La deduzione era sbagliata e la misura l'ha
ribaltata in un minuto. **La concentrazione bassa resta un sospetto vero** —
una media circolare su una voce sparsa è un numero debole — ed è precisamente
ciò che la prova di linearità deve mettere alla prova.

⚠️ **Due numeri di questo documento non vanno confusi, e sono a un ordine di
grandezza di distanza.** Sulla stessa voce, media circolare **senza** finestra
= **−8,80 tick** (143 colpi); `GR.origine()`, cioè **con** la sua finestra, =
**−0,40 tick** (58 colpi). Il secondo è il numero di una funzione che qui non
va usata, per la ragione scritta al §3. Chiunque veda `-0,4` mentre lavora su
`'voce'` sta chiamando la funzione sbagliata.

---

## 6. Le conseguenze: riportate, mai inseguite

Scelto il default, si rifà girare `tools/misura_groove.py` e si riporta cosa
cambia, **datato e con i numeri vecchi accanto ai nuovi**:

- «battere in minoranza» e celle al bordo — la tabella di `jazz.md`;
- il profilo posizionale (il 43,7%);
- il charleston contro il ride (**12 su 15**, e non «15 su 15»: quello che
  regge è delle fasi grezze) e la stratificazione;
- il massimo spostamento e l'escursione, che decidono se `set_swing()` si muove.

⚠️ **Se una di queste cambia in meglio, non è una prova che lo stimatore sia
giusto.** La prova è il §4. Queste sono conseguenze, e vanno scritte come tali.

---

## 7. I test

Sul modello dei 12 check che la correzione della finestra di grazia ha aggiunto,
**verificati per inversione**:

1. **neutralità del parametro**: con `taglio='vicino'` i numeri di oggi tornano
   **identici**. Se non tornano, il parametro non è neutro e tutto il confronto
   è viziato;
2. **il caso sintetico**, senza dataset, quindi gira sempre: una voce con un
   gesto centrato a −12 tick da un battere e dispersione ±4. `'vicino'` lo
   spezza in due celle di segno opposto, `'voce'` e `'rado'` no;
3. **la linearità sintetica**: traslata la voce di δ, la posizione dichiarata si
   muove di δ;
4. **il limite nuovo**: `|scarto| < passo_tick` sempre, su tutti e tre i tagli;
5. **il ripiego di `'rado'`**: una voce di semicrome piene non ha punti radi, e
   lo spostamento deve uscire `0`, non un numero inventato;
6. **su `applica_groove()`**: due note su passi adiacenti non finiscono sullo
   stesso tick, o il rapporto lo dice.

E la verifica per inversione dell'intero lavoro: **rimettendo `'vicino'` come
unico taglio, i check nuovi devono diventare rossi**. Un test che passa sia col
codice nuovo sia col vecchio non sta misurando quello che dice.

---

## 8. La documentazione, e due divieti che valgono

- `docs/repertori/jazz.md`, «Il bordo fra due passi»: la casella **prende** la
  decisione che oggi dichiara e non prende, datata, coi numeri vecchi accanto
  ai nuovi;
- `HANDOFF.md` §7 e §6-terdecies: il punto esce dai punti aperti;
- ⚠️ `write_bytes()`, **non** `write_text()`: su Windows `write_text()` traduce
  `\n` in `\r\n` e rende illeggibile la revisione, che in questo progetto è il
  meccanismo su cui poggia tutto il resto. Due agenti diversi ci sono già
  cascati nella stessa sessione;
- ⚠️ **non si rigenerano** `out/GROOVE0.XML`, `out/GROOVE1.XML`,
  `out/SWINGA.XML`, `out/SWINGB.XML`. Sono l'unico esemplare su cui poggiano i
  quattro ascolti e il giro sul dispositivo (31 posizioni su 31), e con lo
  stimatore nuovo la riga del pedale esce **ancora** diversa. Chi rivuole la
  coppia col codice di oggi **la scrive altrove e la confronta**.

---

## 9. Cosa NON è in questo lavoro

- **la soglia percettiva** — quanto grande debba essere un residuo perché si
  senta. Non la chiude un ascolto in più: servirebbe un protocollo di
  psicoacustica, e l'ascoltatore stesso ha dichiarato imprecise le proprie
  valutazioni;
- **cosa faccia il firmware a una nota che cade fra le crome** — resta
  `song.SWING_SCARTO_SORGENTE`;
- **la coppia d'ascolto sulla stratificazione**, e merita una riga perché è una
  dipendenza vera: è indicata su `drummer10/session1/1`, passi **4 e 12** —
  cioè esattamente le celle che questo lavoro sposta. Va fatta **dopo**. Farla
  prima vorrebbe dire ascoltare numeri destinati a cambiare.
