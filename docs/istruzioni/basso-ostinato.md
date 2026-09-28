# Basso ostinato: ritorno invariato, superficie mobile

**Scopo.** Usare un ciclo grave riconoscibile per dare continuità a una sezione elettronica mentre figurazione, densità e beat cambiano sopra di esso. La prova è formale, non una ricostruzione di una danza barocca né una valutazione estetica del brano.

## Fonti e confine

`[LIB]` Piston, *Harmony*, 5ª ed., cap. 7, p. 94 (PDF locale in `to-read/`), chiama *ground bass* un ostinato nella voce più grave lungo una frase o più. Menziona passacaglia e ciaccona come forme che possono usarlo per tutta la durata. Questa definizione operativa è sufficiente per testare la ripetizione di una **linea di basso reale**, non solo di una progressione di sigle.

`[WEB]` [Alexander Silbiger, *Chaconne and Passacaglia*, Oxford Bibliographies](https://academic.oup.com/reference/62400/reference-article-abstract/555408310) precisa che prima del 1800 la variazione su basso ostinato non era universale in questi generi. [Geoffrey Burgess, *The Ground-Bass Variation Dances of Marin Marais*, Oxford Handbook](https://academic.oup.com/edited-volume/61382/chapter-abstract/533160342) descrive invece il caso specifico di un ground di quattro battute ripetuto senza interruzione e bilanciato da variazioni inventive. Qui prendiamo **quel principio circoscritto**; non etichettiamo ogni passacaglia o ciaccona come un ground invariabile.

Il [basso continuo](basso-continuo.md) era una linea mutevole con cifre e una realizzazione delle voci superiori. In questa prova non ci sono cifre: il vincolo formale è il ritorno *letterale* della stessa linea grave.

## Prova `OSTINATO01`

`[DEC]` Venti battute a 106 BPM in Re minore, su synth e kit 808. Una clip `GROUND` di quattro battute contiene **nove note** con un profilo interno; l'arranger usa quella stessa clip alle battute 1, 5, 9, 13 e 17. Lo scheletro armonico Dm–C–Sib–A7 è un sostegno di lettura, non l'oggetto che viene ripetuto. La variazione avviene sopra il basso:

| Battute | Voci superiori e beat |
|---|---|
| 1–4 | accordi brevi e molto spazio |
| 5–8 | figurazione regolare in ottavi, hi-hat più fitto |
| 9–12 | risposte superiori sincopate |
| 13–16 | sottrazione: una sola risposta per battuta, senza rim e hi-hat |
| 17–20 | ritorno degli accordi con due frammenti di figurazione |

`[CALC]` `test_basso_ostinato_scritto` verifica che le cinque istanze d'arranger abbiano lo **stesso clipCode e lo stesso nodo**, durino esattamente quattro battute ciascuna e siano contigue. Controlla nove eventi nel ground, cinque firme di note superiori differenti, le classi di altezza ammesse in ogni battuta e la durata complessiva di venti battute. `MU.verifica` e `MU.avvertenze` sono vuote. Il generatore è [`tools/basso_ostinato_scritto.py`](../../tools/basso_ostinato_scritto.py).

`[CALC]` Il 27 settembre 2026 `OSTINATO01.XML` è stato caricato in `/SONGS/DelugePal/` e riletto dalla SD: **135883 byte**, SHA-256 `8b27240a79643108e0d0a7f287a516523e517bb3146d3a87849f6b82df7e2d9f` identico al file locale. La rilettura conferma il trasferimento dei dati.

`[OSS]` **Ascoltata sul Deluge**: l'utente sente il basso che continua a tornare e le variazioni delle altre voci. Il riscontro conferma che i due livelli formali sono percepibili in questa prova; non è un giudizio sulla qualità compositiva dell'esempio.

## Che cosa aggiunge alla copertura

La risorsa riutilizzabile è una separazione di livelli: **identità nel basso, trasformazione sopra**. Può dare coesione a una traccia elettronica più lunga anche quando la superficie cambia molto. Questa prova non decide quanto un ritorno si percepisca in un mix reale, né quanta trasformazione convenga in una produzione concreta. Quelle scelte richiedono il materiale del pezzo, non un esempio astratto.
