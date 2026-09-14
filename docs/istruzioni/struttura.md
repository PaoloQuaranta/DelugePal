# La struttura: la forma lunga, la mappa delle sezioni

**A cosa serve.** Hai il materiale — un tema, un giro, un groove — e devi
decidere **come si dispone nel tempo**: quante sezioni, in che ordine, quali
tornano e quali contrastano. È lo **scheletro** del pezzo: la stessa idea diventa
un AABA, un blues ripetuto, una testa-soli-testa a seconda della mappa.

È priorità 2 (forma), l'ultima faccia dopo [voicing](voicing.md), [comping](comping.md)
e [contrappunto](contrappunto.md). Quelle tre lavorano **dentro** una o due
battute; la struttura è ciò che **dura più di una battuta** — la forma dell'intero
pezzo. È anche ciò che rende possibile «un pezzo intero» invece di una parte sola.

⚠️ **Questa istruzione copre la MAPPA (lo scheletro): dove cadono le sezioni.** Le
altre due facce della struttura — l'**arco dinamico** (come densità e intensità
salgono e ricadono lungo la forma) e le **transizioni** (turnaround, fill, stacchi)
— sono in «Cosa manca», su domanda.

**Cosa ti serve prima di cominciare:** il materiale di ogni sezione già scritto in
**clip** (gli accordi, la melodia, il basso di ogni sezione), e l'organico.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[MIS]` | misurato su un corpus, con quanti pezzi |
| `[CALC]` | calcolo sulla timeline, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

⚠️ **`[CALC]` + un ascolto**, come le altre facce della forma. Il `[CALC]` è dove
cadono le sezioni (i conti in tick); l'ascolto è se la **forma si sente** — se l'A
torna riconoscibile e il ponte contrasta.

---

## Il principio: un pezzo è sezioni disposte nel tempo

`[LIB]` music-composition, `references/form/popular-song-forms.md`: quasi tutte le
forme popolari sono **costruite da un piccolo insieme di tipi di sezione**
(intro, verse, chorus, bridge, outro…) **combinati in un ordine**. Gli stessi tipi
si ricombinano fra generi. La forma **non** è una nota o un accordo: è la
disposizione.

⚠️ **La regola che conta più di tutte le mappe: ripetizione contro sviluppo**
(`[LIB]` stesso file). Una sezione che torna dà **riconoscibilità**; ma una forma
che ripete **identica** è statica — *«l'ultima ripetizione deve pesare di più»*
(final chorus elevation: si modula, si addensa, si aggiunge una voce). La mappa dà
lo scheletro; lo **sviluppo** (la variazione dell'ultimo giro) è la carne, ed è la
faccia successiva.

---

## Il vocabolario

### Le sezioni

`[LIB]` popular-song-forms.md: i mattoni, con cosa fanno —

| sezione | cosa fa | battute tipiche |
|---|---|---|
| **intro** | stabilisce tono, tempo, groove | 4-8 (o 1-2, moderno) |
| **A** / verse | il corpo, la casa | 8 (o 16) |
| **B** / bridge / ponte | il **contrasto**, spesso modula, poi riporta a casa | 8 |
| chorus | il gancio, il ritornello | 8-16 |
| **out** / outro | scarica la tensione, chiude | 4-8 |

### Le mappe canoniche

`[LIB]` popular-song-forms.md, e `[MIS]` casella 9 di
[`docs/repertori/jazz.md`](../repertori/jazz.md) (349 assoli swing con forma
scomponibile, da `wjazzd.db`) —

| mappa | cos'è | dato |
|---|---|---|
| **`A A B A`** | l'**AABA** di 32 battute, la forma più comune del jazz | `[MIS]` **103** assoli |
| **blues** (`A` × N) | il blues di **12 battute**, ripetuto | `[MIS]` **81** assoli; template `Blues` |
| **rhythm changes** | un AABA con l'armonia di *I Got Rhythm* | `[MIS]` **19**; template `I Got Rhythm` |
| **testa / soli / testa** | la testa una volta, poi i soli sul giro, poi la testa | `[LIB]` la prassi del jazz |
| **verse-chorus** | il default del pop | `[LIB]` |
| **intro-build-drop-breakdown** | la forma dell'EDM | `[LIB]` |

⚠️ **Niente filologia** (perimetro, 11 settembre 2026): la mappa è un colore
disponibile, non un obbligo. Si attinge al bagaglio (l'AABA, il blues, il
testa-soli-testa) per una composizione dell'utente, non si replica un genere.

### Le lunghezze

`[LIB]` popular-song-forms.md: default **8 battute** per sezione (o 16); il blues
fa eccezione a **12**. Corto dà urgenza, lungo dà spazio. ⚠️ Una sezione fuori
misura si sente: un chorus di 24 battute è ingombrante, uno di 4 non fa in tempo
a posarsi.

---

## Come si scrive, materialmente

Prima si scrive il **materiale di ogni sezione** in clip (con
[`armonia`](../../tools/delugexml/musica.py), `melodia`, `comping`… e `MU.scrivi`);
poi `MU.forma` le **stende sull'arranger**.

```python
from delugexml import musica as MU, arranger as A

# 'sezioni' dice quali clip suonano in ogni sezione (una per strumento):
sezioni = {'A': [clip_accordi_A, clip_melodia_A],
           'B': [clip_accordi_B, clip_melodia_B]}

piano = MU.forma(doc, 'A A B A', sezioni, battute=8)   # AABA, 32 battute
print(MU.racconta_forma(piano))
A.open_in_arranger(doc)                                # si suona dall'arranger
```

`MU.forma(doc, mappa, sezioni, *, battute=8, battute_per=None)` `[CALC]`: stende la
mappa sulla timeline, calcolando dove cade ogni sezione in tick, e piazza le clip
(`arranger.place`). `battute_per` cambia la lunghezza di una singola sezione
(`{'blues': 12, 'intro': 4}`). Blindato da `test_forma`.

⚠️ **Tre cose da sapere:**
- **non compone e non crea clip:** il materiale lo scrivi prima. `forma` fa i
  **conti**, come `comping` e `contrappunto` — l'AI decide la forma, il codice la
  stende;
- **una sezione che si ripete identica riusa la STESSA clip** (A A A usa un clip
  solo): è il modo del dispositivo — cambiando la clip cambiano tutte le
  ripetizioni;
- **per una ripetizione VARIATA** (l'ultimo A diverso, il fill dell'ultimo giro)
  si usa `arranger.place_unique`, la clip **"bianca"**: è la faccia *sviluppo*, non
  questa.

⚠️ **Si suona dall'arranger.** `A.open_in_arranger(doc)` apre la song in arranger
view: la **timeline è la forma**. Le clip di sessione restano ferme
(`avvertenze()` lo segnala: qui è atteso, non un difetto — non si lanciano a mano,
le suona la timeline).

---

## Esempio lavorato: un AABA

`[OSS]` **Ascoltato il 14 settembre 2026**, caricato sul Deluge (`STRUTTURA01`).
Un AABA vero, la forma più comune del jazz, steso con `MU.forma`. Due strumenti —
Rhodes per gli accordi, tromba per la melodia — e due materiali: **A** è la casa
(`Cmaj7 Am7 Dm7 G7`, tema medio), **B** il ponte (`Fmaj7 Bb7 Cmaj7 G7`, parte sul
**IV**, tema acuto, chiude sul **V** e riporta a casa). Mappa `A A B A`, sezioni da
4 battute. Si suona dall'arranger. In
[`tools/forma_scritto.py`](../../tools/forma_scritto.py).

**Verdetto: «suona giusto, approvato».** ⚠️ Si sente la **forma** — l'A che
**torna** riconoscibile, il ponte che **contrasta** e riporta a casa: lo scheletro
regge. È passata al primo colpo, come le altre facce della forma.

---

## Cosa NON fare

- **non far comporre la forma al codice:** `MU.forma` stende una mappa che decidi
  tu, non ne inventa una;
- **non ripetere una sezione identica all'infinito senza sviluppo:** una forma che
  non cresce è statica — l'ultima ripetizione deve pesare di più (`place_unique`);
- **non far contrastare il ponte troppo:** un ponte che cambia tutto si scolla — dà
  sollievo restando lo stesso pezzo (popular-song-forms.md);
- **non sbagliare le lunghezze:** 8 battute a sezione è la norma, 12 il blues;
  fuori misura si sente;
- **non aspettarsi che si suoni dalla session view:** è una forma d'arranger —
  `open_in_arranger`, poi play.

---

## Cosa manca a questa istruzione

- ~~l'**arco dinamico**~~ **[fatto](arco-dinamico.md)**: come densità e intensità
  salgono al ponte e ricadono sull'ultimo A (`[MIS]` casella 9). La seconda faccia
  della struttura;
- ~~le **transizioni**~~ **[fatte](transizioni.md)** (i giunti armonico-melodici):
  turnaround, pickup, break, con la clip bianca `MU.variazione`. Resta fuori il
  **fill di batteria**. La terza faccia della struttura;
- la forma **non uniforme e annidata** (una coda che tronca l'ultimo A, un intro
  di lunghezza dispari): `battute_per` copre le sezioni di lunghezza diversa, non
  ancora le sovrapposizioni.
