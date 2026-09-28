# Basso continuo: il basso guida, le voci superiori realizzano

**Scopo.** Usare il basso continuo come rapporto compositivo in una produzione elettronica sul Deluge: una linea di basso conduce il movimento armonico, mentre synth superiori ne realizzano le cifre con disposizione, ritmo e densità scelti per il pezzo. Non serve imitare strumenti o prassi barocchi.

## Distinzione decisiva

**Basso continuo** indica una prassi di accompagnamento: si dà la linea di basso, eventualmente con cifre, e si realizzano sopra di essa le parti armoniche. **Basso ostinato** indica una linea che si ripete. Un continuo può anche usare un ostinato, ma non lo richiede. Nel nostro primo esempio il basso cambia nel corso delle otto battute e non forma un ciclo ripetuto.

`[LIB]` Piston, *Harmony*, 5ª ed., cap. 6, pp. 84-85 (PDF locale in `to-read/`): il basso cifrato guidava la tastiera nel riempire o rinforzare le parti; la realizzazione decide disposizione, condotta e linea superiore, e va esercitata ritmicamente. Le cifre si leggono come **intervalli sopra la nota reale del basso**; solo dopo si riconosce l'accordo.

`[WEB]` [Open Music Theory, *Introduction to thoroughbass*](https://openmusictheory.github.io/thoroughbassFigures.html) elenca le cifre e abbreviazioni comuni (`5/3`, `6/3`, `6/4`, `7`, `6/5`, `4/3`, `4/2`) e le alterazioni. [Oxford Bibliographies, *Continuo*](https://academic.oup.com/reference/62400/reference-article-abstract/555396142) precisa che molte linee storiche erano poco cifrate o senza cifre. Qui usiamo cifre esplicite perché rendono il primo test controllabile; non le trattiamo come requisito universale del continuo.

## Stato degli strumenti

`MU.armonia()` parte da **sigle di accordo** e `MU.voci_condotte()` sceglie una disposizione vicina alla precedente. Sono utili per la condotta, ma non rispondono alla domanda del continuo: «con questa nota effettiva al basso e queste cifre, quali note sono ammesse sopra?». Per questa prova il piccolo interprete sta in [`tools/basso_continuo_scritto.py`](../../tools/basso_continuo_scritto.py). Non è ancora una primitiva generale di `musica.py`.

## Prima prova: `BASSOC01`

`[DEC]` Otto battute elettroniche con 16 eventi di basso a durate diverse. Il lessico è limitato a `5/3`, `6/3`, `6/4`, `7/#3`, `6/5`; `7/#3` è la notazione interna esplicita per la terza alzata, non una pretesa grafia storica. La scala dichiarata è Re minore. Tre voci synth superiori sono scelte fra le classi di altezza date dalle cifre, in registro compatto, privilegiando poco movimento ed evitando quinte/ottave parallele. Nella seconda metà cambia il ritmo della realizzazione, mentre le cifre continuano a vincolare le note. Un beat 808 mantiene il contesto elettronico.

Il passaggio iniziale è il nucleo della prova: **Re al basso con `5/3`**, poi **Fa al basso con `6/3`**. Entrambe le cifre danno Re–Fa–La e le voci alte restano *fisicamente tenute* mentre il basso si muove. Questo mostra una differenza che una normale fila di sigle `Dm | Dm/F` potrebbe nascondere.

`[CALC]` Il test `test_basso_continuo_scritto` controlla i casi noti `Re 5/3`, `Fa 6/3`, `La 7/#3`, `Do# 6/5`; verifica tutte le 16 realizzazioni contro le rispettive cifre, la nota tenuta sul cambio Re→Fa, l'assenza di quinte/ottave parallele e le otto battute senza errori o avvisi XML. L'accordo con bass Do# `6/5` contiene Mi–Sol–La sopra: è La7/Do#, anche se la sigla non è l'input. Il 27 settembre 2026 `BASSOC01.XML` è stato caricato in `/SONGS/DelugePal/` e riletto dalla SD: 132997 byte, hash SHA-256 identico al file locale.

`[OSS]` **Ascoltata sul Deluge il 27 settembre 2026**: l'utente conferma che funziona e la trova un po' più interessante della sequenza precedente. Per questa serie di prove il giudizio estetico non è il criterio di riuscita: l'obiettivo è verificare il meccanismo e capire quale risorsa formale sia disponibile per produzioni future. Mix ed espressione potranno essere valutati su un brano concreto.

## Perimetro attuale

- La decodifica considera i gradi di Re minore e poche cifre dichiarate. Non copre ancora bassi senza cifre, tutte le alterazioni, ritardi figurati, cambi di cifra su una stessa nota tenuta o modulazioni.
- La scelta delle voci è una **realizzazione possibile**, non una soluzione unica. Cambiare registro, ritmo, densità o timbro conservando le note richieste è parte del valore espressivo del continuo.
- Il prossimo passo utile, se questa risorsa entra in una produzione reale, è dare a una melodia dell'utente una linea di basso con cifre e generare **due realizzazioni diverse** dello stesso materiale. Solo allora sapremo quali controlli meritano una funzione riutilizzabile in `musica.py`.
