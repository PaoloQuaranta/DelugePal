# La rifondazione di `docs/MUSICA.md` sullo schema neutro

**Progetto approvato il 17 agosto 2026.** Chiude il punto 4 lasciato aperto
dalla sessione dello swing: *«`MUSICA.md` è ancora a forma di batteria reggae.
Con lo spettro che hai in mente — jazz, classica, barocca, antica,
contemporanei — quel documento va rifondato su uno schema neutro in cui il
reggae diventi un caso compilato fra molti.»*

---

## 1. Il problema

`docs/MUSICA.md` è cresciuto attorno a un solo pezzo. La sua spina dorsale è
«Reggae e dub — istruzioni compositive»; lo swing del jazz, misurato il 17
agosto, è entrato come sezione a sé; e il capitolo finale — «Quello che una
griglia di una battuta non dice» — è già un tentativo di uscire dal genere
singolo, scritto però *dentro* una struttura che non ha un posto dove metterlo.

Il perimetro dichiarato dall'utente è molto più largo: **jazz** per primo, poi
**classica, barocca, antica**, poi i **contemporanei** (elettronica, IDM,
techno, hip hop, trip hop, dub, DnB, jungle). Il folk è fuori.

Il documento com'è non regge quella larghezza per due ragioni distinte:

1. **è a forma di un genere.** Aggiungere il jazz vuol dire accodare una
   sezione; aggiungere l'antica vuol dire accodarne un'altra, con un'altra
   forma ancora. Dopo tre repertori nessuno sa più cosa manca a quale.
2. **non ha un posto per il materiale trasversale.** Le norme di sound design,
   la scala delle velocity, l'arco di densità, il protocollo di revisione: sono
   dentro capitoli di genere per accidente storico, e valgono per tutti.

E c'è una terza cosa, che è il vero guadagno atteso: a documento organizzato
per genere, **l'*inégalité* barocca e lo swing del jazz non si sfiorano mai.**
Sono la stessa domanda — dove cade il levare dentro il movimento — fatta a due
repertori, e il jazz ne ha la risposta misurata (levare al 61,7%, BUR 1,61).
Lo schema non serve a ordinare: serve a far collidere cose che il genere tiene
separate.

---

## 2. Lo schema neutro: undici caselle

Le caselle sono formulate come **domande**, non come campi. Il test usato per
sceglierle: devono sopravvivere **sia a Josquin sia alla jungle**. Uno schema
derivato da reggae + jazz avrebbe caselle come «griglia a 16 passi» o «velocity
groove», e nella musica antica sarebbero vuote non per mancanza di ricerca ma
perché la domanda non si pone.

| n | casella | la domanda |
|---|---|---|
| 1 | **Cos'è, e cosa non è** | i confini, e l'errore tipico di chi lo confonde con un vicino |
| 2 | **Metro e griglia** | quale unità, quanti passi, quanto è rigida |
| 3 | **Tempo** | il range vero, e cosa cambia ai bordi |
| 4 | **Feel** | dove cadono le note rispetto alla griglia |
| 5 | **Ruoli e spartizione** | chi occupa cosa, e **cosa lascia libero** |
| 6 | **Dinamica** | accenti, fantasmi, terrazzata, o «non è questo il parametro» |
| 7 | **Armonia** | vocabolario, ritmo armonico, condotta delle parti |
| 8 | **Melodia e ornamentazione** | materiale, sviluppo, cosa si improvvisa |
| 9 | **Forma e densità** | la scala lunga, l'arco |
| 10 | **Sul Deluge** | come si realizza con la macchina che c'è |
| 11 | **Trappole del generatore** | cosa sbaglia un programma **per costruzione** qui |

Perché ciascuna è irriducibile:

- la **1** è la casella che ferma «una ricerca sola dà le etichette, non il
  mestiere» — la lezione pagata con `DUBPAL01`;
- la **4** è quella dove collidono swing, inégalité, laid-back e rubato, e
  contiene gli unici `[MIS]` del progetto;
- la **5** è la griglia a quattro parti del reggae **generalizzata**: basso
  continuo più voci, comping più walking, sono la stessa domanda;
- la **7** dichiara un buco noto: `MU.armonia()` copre il vocabolario e **non**
  la condotta delle parti;
- la **10** è l'unica che nessuna skill esterna può compilare, ed è dove il
  progetto è già forte;
- la **11** sta **per repertorio** e non in un registro unico, perché «cosa
  sbaglia un generatore *qui*» non si trasferisce: le sette righe del dub, in
  una lista comune, sembrerebbero lezioni generali e non lo sono.

### Una casella vuota è informazione

`«Jazz / 6. Dinamica: vuota»` è un compito, e si sa già chi lo chiude. Le
caselle vuote dichiarano **cosa servirebbe per riempirle**, quindi l'agenda dei
lettori successivi — MusicXML, kern, Groove MIDI — si legge dallo schema invece
che da una lista a parte.

---

## 3. La struttura dei file

```
docs/MUSICA.md                    lo schema, il comune, l'indice
docs/repertori/reggae-dub.md      le 11 caselle: 6 piene, 4 parziali, 1 vuota
docs/repertori/jazz.md            le 11 caselle: 1 piena, 3 parziali, 7 vuote
```

**Nessun altro file.** I repertori restanti esistono solo come righe
nell'indice: un file che dice soltanto «vuota» è rumore da aprire, una riga
d'indice è la stessa informazione a costo zero.

Il nome è `repertori/` e non `generi/` perché «genere» copre la jungle e non
copre la musica antica né il barocco, che sono periodi. Lo spettro va «dalla
musica antica ai generi contemporanei»: *repertorio* è la parola che li tiene
insieme senza forzare.

### Perché diviso e non un file solo

Un file unico sarebbe 3-4000 righe da leggere per intero ogni volta che si
compone, e l'85% sarebbe sempre del repertorio sbagliato. Diviso, si legge lo
schema più la scheda che serve.

È la stessa disciplina che `SKILL.md` già prescrive per la skill grande —
*«si parte sempre da `references/00-navigation.md` e si caricano 1-3 file, non
di più»*. Applicarla al proprio documento invece che solo a quello altrui.

Scartata l'alternativa di mettere le schede dentro `.claude/skills/deluge-pal/`:
`SKILL.md` è il protocollo, `docs/` è la conoscenza, e la separazione regge da
inizio progetto.

### Una regola contro la duplicazione

**Un numero vive in una casella sola.** La collisione inégalité/swing si fa con
**rimandi**, non con copie: il 61,7% sta in `repertori/jazz.md` casella 4 e
basta. È la regola 2 del progetto («mai trascrivere a mano») applicata alla
prosa — altrimenti fra un mese ci sono due BUR diversi in due file e nessuno sa
quale è stato misurato.

---

## 4. Il contenuto di `MUSICA.md`

Tre parti, in quest'ordine.

### a) Lo schema

Le undici domande, ciascuna con *cosa vuol dire compilarla* e *cosa vuol dire
lasciarla vuota*. Due o tre righe l'una: è la legenda, non un trattato.

### b) Il comune

Tutto ciò che vale per ogni repertorio, che oggi è sparso dentro capitoli di
genere per accidente storico:

| cosa | oggi sta in | alimenta |
|---|---|---|
| norme di sound design: risonanza e il suo compenso, delay feedback, LPF/HPF ai bordi, l'LFO sul filtro | «Norme di sound design» | casella 10, ovunque |
| il corpus non è autoritativo, e da dove si sa cosa il firmware accetta | sezione omonima | metodo |
| il synth vuoto come telaio; struttura sullo strumento, valori e patch cable sulla clip | «Preset e come vengono usati» | casella 10, ovunque |
| la scala 0-127 delle velocity e le escursioni di accento per strumento | «Velocity groove», prima metà | casella 6, ovunque |
| swing di song ≠ laid-back di parte, e la grana in tick (96/movimento, 8,9 ms a 70 BPM) | «Ma swing e laid-back non sono la stessa cosa» | casella 4, ovunque |
| il meccanismo di `set_swing` e di `swingInterval` | «E come si porta sul Deluge» | caselle 4 e 10, ovunque |
| l'arco di densità 1-9 e i tre errori da generatore | «L'arco di densità» | casella 9, ovunque |
| variare è scelto, non randomizzato | «Il turnaround corregge un caso su quattro» | caselle 6 e 9 |
| cassa e basso sono una coppia, e va dichiarata | §3 di quel capitolo | casella 5 |
| la playability è una decisione, non una regola | §4 | casella 5 |
| il protocollo Keep / Change / Direction delle revisioni | §5 | metodo |
| quale fonte comanda su cosa, e che una fonte grande non è autorevole su tutto | testa del file | metodo |

Il **meccanismo** di `set_swing` sta nel comune perché è un fatto sulla
macchina, non sul jazz; i **valori** per stile (BUR → display) stanno in
`repertori/jazz.md`. La misura di come si è stabilito resta dove è già:
`FINDINGS.md` §6-undecies.

### c) L'indice, che è anche l'agenda

Una matrice repertorio × casella:

| repertorio | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| reggae / dub | ◐ | ● | ● | ◐ | ● | ● | ◐ | ○ | ◐ | ● | ● |
| jazz | ○ | ○ | ◐ | **●** | ○ | ○ | ◐ | ○ | ○ | ◐ | ○ |
| classica · barocca · antica | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| elettronica · IDM · techno · hip hop · trip hop · DnB · jungle | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |

`●` compilata · `◐` parziale, e la scheda dice di cosa · `○` vuota.

**Il grado di prova non sta nell'indice**: `[MIS]`, `[WEB]`, `[OSS]`, `[IPO]`,
`[MAN]` restano dentro la scheda, accanto all'affermazione che qualificano. La
matrice dice solo dove c'è qualcosa.

---

## 5. La forma di una scheda

Undici sezioni fisse, **sempre tutte e undici anche quando vuote**, sempre
nello stesso ordine: così si sa dove guardare senza leggere.

```markdown
# Reggae e dub

> stato: 6 piene, 4 parziali, 1 vuota · ultima revisione 17 agosto 2026

### 1. Cos'è, e cosa non è
…

### 6. Dinamica
…
```

Una casella vuota non è uno spazio bianco: dice cosa servirebbe per riempirla.

```markdown
### 6. Dinamica

**Vuota.** La chiuderebbe il Groove MIDI
(`to-read/MIDI/groove-v1.0.0-midionly.zip`, in attesa di decompressione):
porta velocity e microtiming misurati per genere, e farebbe per la batteria
quello che la Weimar ha fatto per lo swing.
```

---

## 6. Le correzioni ricevute

Oggi sono un registro cronologico unico in fondo a `MUSICA.md`. Con la casella
11 per repertorio il registro **si scioglie**:

| correzione | dove va |
|---|---|
| «è molto elementare e non assomiglia per niente a un pezzo dub», con la tabella dei sette errori | `reggae-dub.md`, casella 11 |
| «leggi anche documentazione», «leggi anche docs community» | il comune, metodo |
| «ora ci sono 4 envelope, non 2» | il comune, macchina |
| la risonanza non ha una soglia ma un compenso | il comune, già dentro le norme di sound design |

**Il registro si scioglie del tutto: non resta nessun indice cronologico.**
Era stato proposto e l'utente l'ha scartato.

Quello che il registro portava — **la data e la frase testuale dell'utente** —
non si perde: viaggia con ogni correzione dovunque finisca. È lì che serve,
accanto alla cosa che ha corretto. Quello che si perde è solo la possibilità di
leggerle in fila, e per la storia del progetto c'è già `HANDOFF.md`.

---

## 7. Cosa si scrive adesso, e cosa no

Il materiale in mano è asimmetrico: il reggae/dub ha prosa `[WEB]` corretta due
volte dall'ascolto; il jazz ha gli unici `[MIS]` del progetto (lo swing) più le
sigle e i voicing di `MU.armonia()`; tutto il resto è a zero.

Si compilano **due schede**. Il jazz si compila **con quello che c'è** — quattro
caselle toccate su undici — e non si va a cercare materiale nuovo in questa
sessione.

### Cosa NON si fa

- **non si riscrive il contenuto del reggae, si migra.** È stato corretto due
  volte dall'ascolto dell'utente: riformularlo lo espone a perdere proprio
  quelle correzioni. Concretamente: **le frasi si spostano come sono**, e a
  cambiare sono solo i titoli, l'ordine e le poche righe di raccordo. Le
  griglie a 16 passi, i numeri di velocity, le tabelle e le citazioni
  dell'utente restano parola per parola. **Se un pezzo non entra in nessuna
  delle undici caselle, è lo schema a essere sbagliato** e si torna a parlarne
  prima di buttare via il contenuto.
- **non si cerca materiale nuovo.** Il jazz resta a sette caselle vuote.
- **non si toccano `FINDINGS.md` e `ARCHITETTURA.md`.** La divisione regge: lì
  sta come si è misurato, in `MUSICA.md` come si usa.
- **non si traducono i documenti.** `docs/` resta in italiano, come deciso.

### L'unica modifica fuori da `docs/`

`.claude/skills/deluge-pal/SKILL.md` rimanda a `docs/MUSICA.md` per «come si
compone davvero in un genere», e l'avvertenza «su reggae e dub comanda
`docs/MUSICA.md`». Vanno aggiornati a «lo schema in `MUSICA.md` più la scheda
del repertorio in `docs/repertori/`». Nient'altro.

---

## 8. Come si vede che ha funzionato

- le undici caselle **hanno accolto tutto** il contenuto attuale di
  `MUSICA.md`, senza residui e senza inventare una dodicesima;
- nessun numero compare in due file;
- l'indice dice, senza aprire niente, **cosa manca a quale repertorio**;
- `MUSICA.md` più una scheda sola bastano a comporre in quel repertorio;
- il documento **sembrerà più povero di adesso**, ed è il segno che lo schema
  funziona: oggi le caselle vuote non si vedono soltanto perché non esistono
  come domande.

---

## 9. Il contesto: cosa resta aperto attorno a questo

Dalla chiusura della sessione precedente, per non perderlo — **non è parte di
questo lavoro**, ma è ciò che riempirà le caselle:

1. il valore assoluto della BUR non torna con la letteratura (1,61 contro
   ~1,3 pubblicato sullo stesso database, metodo dietro paywall); i rapporti
   fra sottoinsiemi sono invece nella direzione giusta;
2. sotto i 120 BPM la misura guarda probabilmente la figura sbagliata — nelle
   ballad lo swing va sulle semicrome. `[OSS]`
3. lo scarto di 2 col sorgente sullo swing resta ignoto
   (`song.SWING_SCARTO_SORGENTE`);
4. **questo documento** ← il lavoro di adesso;
5. i lettori successivi: **MusicXML** (costo quasi zero, stdlib, e il suo
   `<harmony>` serve anche il jazz), poi **kern** per l'antica e i corali
   analizzati;
6. il **Groove MIDI**, quando la decompressione di `to-read/` finisce: farebbe
   per la batteria quello che la Weimar ha fatto per lo swing — numeri misurati
   al posto dei `[WEB]`.

I punti 5 e 6 atterrano da soli nelle caselle vuote di §5, che è il motivo per
cui l'agenda non ha bisogno di una lista separata.
