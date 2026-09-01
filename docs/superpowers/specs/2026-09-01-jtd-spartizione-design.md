# Il lettore del Jazz Trio Database, e la casella 5 — progetto

**Data:** 1 settembre 2026
**Perche' adesso:** il 30 agosto tre lavori diversi si sono fermati sulla
casella 5 di `docs/repertori/jazz.md` — «ruoli e spartizione» — e l'handoff
ha nominato come prossimo passo un **lettore di partiture MusicXML**. Questo
progetto verifica quella premessa, la trova **falsa**, e prende la strada che
i numeri indicano.

## Il difetto che apre il lavoro

L'utente, dopo aver ascoltato i tre pezzi jazz:

> «La batteria suona discontinua rispetto a basso e piano che sono
> praticamente costanti… le interruzioni, accenti e struttura delle parti di
> batteria sono strettamente correlati alla sezione ritmica, e non le puoi
> applicare acriticamente.»

Misurato allora — deviazione standard dei colpi per battuta:

| batteria | comping | basso |
|---|---|---|
| 1,48 – 1,65 | 0,54 – 0,61 | **0,00** |

**Il basso non varia mai:** 4,00 note per battuta, zero battute diverse da
quattro su 228, quattro posizioni, una sola durata. La batteria e' stata resa
varia campionando le frequenze di tre esecuzioni — col metodo che la regola
«relazioni, non superfici» vieta — e adesso varia **contro uno sfondo fermo**.

## La premessa dell'handoff, verificata il 1 settembre 2026

L'handoff e la casella 5 affermano, in tre punti diversi: *«nessun corpus in
casa ha l'insieme che suona insieme… non e' questione di quanti dati, e' che
il dato non c'e'»*, e concludono che serve MusicXML. Misurato:

| affermazione | esito |
|---|---|
| MusicXML su disco | **0 file.** La strada dichiarata richiedeva **anche** procurare un corpus, e questo non era scritto |
| «nessun insieme in casa» | **falsa.** `to-read/MIDI/songs_archive` ha **17 230** file multitraccia, **241** dei quali di artisti jazz; su 14 letti a campione con `midi.py`, **11 portano basso e batteria insieme**, con i ruoli nominati (`ACOU BASS`, `DRUMS`, `A.PIANO 1`) |
| MusicXML risolverebbe la casella 5 | **no.** In **PDMX** — 250 000 spartiti di pubblico dominio, il piu' grande corpus MusicXML libero — **oltre il 90% ha meno di cinque parti e piu' della meta' sono pezzi solistici**; gli autori scrivono che gli spartiti multitraccia *non sono di pubblico dominio*. Niente batteria |
| esiste un corpus d'insieme con licenza | **si': il Jazz Trio Database**, ed e' esattamente cio' che le tre righe danno per inesistente |

⚠️ **E' la quarta volta che una casella scritta senza domanda manda a cercare
fuori qualcosa di gia' raggiungibile** — le altre tre stanno in HANDOFF
§6-octodecies. Le righe da correggere quando il lavoro chiude: la casella 5 di
`jazz.md`, «Il prossimo lavoro» in testa all'handoff, e §6-octodecies.

⚠️ **Il MusicXML non e' cancellato: e' riqualificato.** Resta giustificato per
la **priorita' 2** dell'utente — classica, barocca, antica — dove
**OpenScore Lieder** e **OpenScore String Quartets** sono **CC0** e curati.
Non e' pero' la risposta a *questa* domanda, e finora lo si credeva.

## La fonte

**Jazz Trio Database** (Cheston, Schlichting, Cross, Harrison — TISMIR 2024).

| | |
|---|---|
| contenuto | **1294 brani, 44,5 ore** di trio jazz, **1947–2015** |
| esecutori | **34 pianisti, 98 bassisti, 106 batteristi** |
| come e' fatto | separazione di sorgente su registrazioni vere, poi rilevamento di onset e beat. Sono **esecuzioni**, non sequenze programmate |
| licenza | **MIT** su annotazioni e codice. L'audio va richiesto e **non serve** |
| dove sta | `to-read/MIDI/jazz-trio-database-v02.zip`, **24 MB**, gia' scaricato. `to-read/` non e' versionato |
| accuratezza dichiarata | F-measure **0,94** sugli onset contro annotazione manuale |
| metro | **1204 brani in 4/4**, 90 in 3/4 |

Per ogni brano, dentro lo zip:

| file | contenuto |
|---|---|
| `beats.csv` | per ogni beat: l'istante di consenso, l'onset di **piano, basso e batteria** su quel beat — **colonna vuota = quello strumento non ha suonato li'** — e `metre_auto`, la posizione nella battuta |
| `bass_onsets.csv`, `drums_onsets.csv`, `piano_onsets.csv` | tutti gli onset, **anche quelli fra i beat** |
| `piano_midi.mid` | il piano con altezze e velocity. Lo legge gia' `midi.py` |
| `metadata.json` | i tre musicisti per nome, tempo, metro, `in_30_corpus`, valutazioni manuali |

⚠️ **Solo 34 brani su 1294 hanno validazione manuale** (`has_annotations`);
il sottoinsieme curato **JTD-300** ne ha 300 (`in_30_corpus`).

## Cosa si misura — cinque misure, tutte relazioni

La regola 2 del comune si applica **prima** di prendere una misura, e la prova
e' una riga: *due generazioni con la stessa misura devono poter essere
diverse*. Nessuna delle cinque fissa **cosa** si suona.

**1. La densita' del basso per battuta.** Distribuzione degli onset per
battuta su tutti i bassisti, percentuale di battute diverse da quattro, e
**dove** cade l'evento in piu' o in meno (posizione metrica da `metre_auto`).
E' la risposta diretta al 4,00 con deviazione zero.

**2. Il beat che il basso salta.** La colonna vuota di `beats.csv`: quanto
spesso accade, e su quale posizione metrica. Dice se un walking vero lascia
buchi e dove.

**3. L'accoppiamento batteria↔basso.** Per battuta: correlazione fra le due
densita'; e quanto spesso un colpo di batteria fuori griglia coincide con un
onset di basso fuori griglia, entro una **finestra dichiarata** (come
`FINESTRA_LEVARE` in `wjazz.py`: e' una scelta, non una legge di natura).
E' la frase dell'utente resa misurabile.

**4. Chi sta avanti.** Scarto medio di ciascuno strumento rispetto al beat di
consenso — le tre colonne sono gia' allineate nel `beats.csv`. Dice se il
basso tira e la batteria trattiene: una relazione d'ensemble, non una
superficie.

**5. Il piano: comping e assolo, e cosa fa il basso sotto.** Densita' del
piano per battuta e registro, contro la densita' del basso e della batteria
nella stessa battuta.

⚠️ **Il limite di questa quinta misura va scritto accanto al numero, non
dopo.** In un trio **il pianista fa tutt'e due le cose**, e `piano_midi.mid`
e' **un flusso solo**: separare comping e assolo richiede una regola —
*n note entro una finestra = accordo di comping; nota singola sopra una certa
altezza = linea* — che e' **`[IPO]`**, non misurata. Quindi:

- la densita' complessiva del piano e' `[MIS]`;
- **ogni numero che dica «comping» invece che «piano» e' `[IPO]`**, e la
  regola che lo produce va dichiarata coi suoi parametri;
- si riportano **entrambe** le versioni, con e senza la separazione, cosi'
  che un lettore veda quanto la regola sposta il risultato.

## Il codice — tre pezzi, sul modello di quelli che ci sono

| | |
|---|---|
| `tools/delugexml/jtd.py` | gemello di `wjazz.py`. **Stdlib pura** (`zipfile`, `csv`, `json`), legge **dentro lo zip senza decomprimere** — la regola di HANDOFF §6-duodecies. Nessuna dipendenza nuova, quindi i test girano col Python di sistema |
| `tools/misura_spartizione.py` | gemello di `misura_melodia.py`: gira le cinque misure e stampa accanto a ogni numero **quante esecuzioni e quanti esecutori lo reggono**, come per la casella 6 |
| test in `tests/test_all.py` | **saltano se lo zip non c'e'**, come gia' quelli di `wjazzd.db` e del corpus |

L'API di `jtd.py`:

| funzione | da' |
|---|---|
| `elenco(path, *, bassista=…, batterista=…, pianista=…, metro=…, curati=False)` | l'indice dei brani, filtrato. `curati=True` restringe a JTD-300 |
| `metadati(path, fname)` | i campi di `metadata.json`, coi `NaN` gia' resi `None` |
| `griglia(path, fname)` | i beat: istante, posizione metrica, e lo scarto dei tre strumenti (o `None` se quello strumento tace su quel beat) |
| `onsets(path, fname, strumento)` | gli onset grezzi di uno strumento |
| `battute(path, fname)` | per battuta: densita' e posizioni di ciascuno dei tre. E' la forma su cui girano le misure 1, 2, 3 e 5 |
| `piano(path, fname)` | il `piano_midi.mid` passato a `midi.py` — serve `midi.leggi_bytes()`, l'offerta rimasta aperta in §6-duodecies, tre righe |

## I controlli da fare PRIMA di fidarsi di qualunque numero

E' la parte che decide se il lavoro vale: ognuno di questi, se salta, rende
sbagliata ogni cifra a valle **senza far fallire nessun test**.

1. ⚠️ **Il beat annotato e' il quarto?** Il tempo dichiarato ha mediana
   **193 bpm** e massimo 299, alto per un trio. Si confronta `metadata.tempo`
   con l'intervallo mediano fra i beat: **se il beat non fosse il quarto, ogni
   densita' «per battuta» sarebbe sbagliata di un fattore due.**
2. **La colonna vuota significa davvero «non ha suonato»?** Controprova sugli
   onset grezzi: se in quell'intorno un onset c'e', la colonna vuota e' un
   fallimento di allineamento e non un silenzio. Si misura **quanto spesso**
   succede, e la percentuale si dichiara.
3. **I `NaN` di `metadata.json`** non sono JSON stretto: `json` di Python li
   accetta, altri lettori no. Si normalizzano a `None` all'ingresso.
4. **I 90 brani in 3/4** si tengono fuori dalle medie e si contano a parte:
   una densita' per battuta mediata fra 3/4 e 4/4 non vuol dire niente.
5. **Doppia misura.** Ogni numero di titolo si calcola su tutto **e** su
   JTD-300. Se divergono vince JTD-300, e **la divergenza si scrive**.

## Cosa resta fuori, e va detto

- ⚠️ **La batteria non e' per strumento.** Gli onset non dicono se e' cassa,
  rullante o ride: la casella potra' dire *quando* la batteria si muove
  rispetto alla sezione ritmica, **mai con che pezzo**.
- **Niente forma ne' sezioni** in JTD: «cosa cambia al confine di sezione»
  richiederebbe dedurre la forma, e resta fuori dalla v1.
- **Niente altezze del basso.** Le avrebbe **FiloBass** (48 trascrizioni
  professionali con MIDI, accordi e forma), ⚠️ ma la sua licenza e'
  **ristretta** — materiale sotto copyright, richiesta da firmare, non
  trasferibile: stessa famiglia di TheSession ed Essen, gia' scartate.
- **Il generatore non si tocca in questo giro.** Prima i numeri, poi la scelta
  di cosa spendere: e' il metodo che ha fatto uscire il rhythm changes giusto
  alla prima versione.
- **I 241 file jazz locali** restano una controprova disponibile a costo quasi
  zero (servono program change e nome traccia in `midi.py`, ~30 righe), **non
  usata in questo giro**: sono sequenze programmate senza licenza, buone per i
  ruoli e non per il feel.

## Dove finiscono i numeri

| | |
|---|---|
| `docs/repertori/jazz.md`, casella 5 | le cinque misure col grado accanto, e i conteggi di esecuzioni ed esecutori |
| `docs/MUSICA.md`, l'indice | la riga del jazz passa da `○` a `●` sulla 5 |
| `docs/FONTI.md` | JTD fra le fonti, **con la nota di copyright MIT**: la licenza la richiede |
| `HANDOFF.md` | una sezione nuova, e la **correzione delle tre righe** che davano il dato per inesistente |

## Criteri di accettazione

1. `python tests/test_all.py` passa col Python di sistema, e i test nuovi
   **saltano** se lo zip non c'e'.
2. `tools/misura_spartizione.py` gira e stampa le cinque misure, ognuna col
   numero di esecuzioni e di esecutori che la reggono.
3. I cinque controlli preliminari sono stati fatti e il loro **esito e'
   scritto**, anche quando l'esito e' «va bene».
4. Nessun numero entra in `jazz.md` senza il suo grado e senza i conteggi.
5. Nessun file generato in precedenza cambia: questo giro non tocca il
   generatore.
