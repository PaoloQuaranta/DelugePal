# HANDOFF — Deluge Pal

**Data:** 20 settembre 2026
**Progetto:** `D:\DelugePal` (fino al 14 agosto si chiamava `deluge-xml-workflow`)
**Pubblico su:** <https://github.com/PaoloQuaranta/DelugePal>, GPL-3.0 — vedi §9
**SD card:** `E:` quando è nel lettore del PC (spesso è nel Deluge, quindi assente)
**Firmware:** community **1.3.0-beta build 2d7cdf8** (2026-08-12), flashata il
12 agosto. La precedente era build 0856ff9 (2026-08-06), su cui la scrittura
SysEx era rotta — vedi §3.2.

Sostituisce `docs/HANDOFF_originale.md`, che resta come storia.

> ## Lo stato in tre righe
>
> **Il sistema tecnico è finito e il ciclo gira davvero: il collo di
> bottiglia adesso è musicale, non software.** Il 16 agosto Deluge Pal ha
> generato il suo primo pezzo vero — un dub in sol minore, tre versioni,
> ciascuna corretta dall'ascolto dell'utente. Verdetto sull'ultima: *«va
> meglio, ma musicalmente ci sarebbe ancora moltissimo da dire»*.
> **997 test.** Il progetto è **pubblicato su GitHub** senza il corpus.
> Il 17-18 agosto `docs/MUSICA.md` è stato **rifondato sullo schema neutro**
> (§6-duodecies): il reggae non è più la forma del documento ma un caso
> compilato fra molti, e l'**indice** dice cosa manca a quale repertorio.
> Dal 18 al 25 agosto il ramo `groove-midi` ha **chiuso la casella 6 del
> jazz** — la dinamica, misurata su cinque batteristi veri invece che presa
> dal web — e ha costruito il **groove template** (§6-terdecies). È il primo
> lavoro di questo progetto il cui risultato non è una funzione che passa i
> test ma **un'affermazione sul mondo**, e si vede da quanto è costato.
>
> Dal 26 al 29 agosto il ramo `stimatore-per-passo` ha **cambiato come si
> aggrega** (§6-quaterdecies). Non è un modo migliore fra due: l'aggregazione
> usata da sempre — il passo **più vicino** — **non seguiva i dati**, e il
> criterio che lo dice era stato fissato prima che le misure esistessero. Il
> default di `GR.profilo()` è cambiato, e con esso alcuni numeri della
> casella 6.
>
> Il **29 agosto** Deluge Pal ha scritto il suo **primo pezzo jazz**
> (§6-quindecies) — un blues in fa. È il primo lavoro che *spende* le misure
> invece di aggiungerne, ed è nato da una domanda dell'utente: *«siamo entrati
> in un rabbit hole?»*. Il conto gli ha dato ragione — undici giorni erano
> andati tutti nella **casella 6**, che occupava il **67%** della scheda del
> jazz mentre **cinque caselle su undici** restavano vuote. Verdetto sul pezzo:
> *«non è niente male… forse il solo potrebbe essere un po' più pirotecnico»*,
> e quel «pirotecnico» **si misura**. La **casella 11** del jazz non è più
> vuota.
>
> E la **casella 8** — la melodia — e' stata **misurata lo stesso giorno**
> (§6-sexdecies), perche' il difetto sentito diceva dove guardare: le corse
> culminano sul **ii-V**, i silenzi sulle chiusure di frase, e un motivo e' di
> almeno **cinque** note perche' sotto le quattro la ripetizione e'
> indistinguibile dal caso. E la **casella 7** e' stata chiusa lo stesso
> giorno (§6-septdecies): `MU.armonia()` conduce le parti, e la fonte che la
> casella dava per risolutiva **non specificava** quello che le si attribuiva.
> Il jazz ha ora **cinque caselle piene** su undici -- il 30 agosto si e'
> aggiunta la **9**, la forma, che era gia' in `wjazzd.db` e nessuno aveva
> aperto.
>
> ⚠️ **Il 30 agosto sono cambiate DUE REGOLE, e valgono piu' di qualunque
> misura di questo file** -- stanno in §6-octodecies e nel comune di
> `docs/MUSICA.md`. La prima: le caselle si riempiono **su domanda**. La
> seconda, data dopo tre ascolti: **il corpus da' RELAZIONI, non superfici** --
> *«vogliamo un tool per AI per creare musica ORIGINALE, non repliche dei
> pattern studiati»*. Meta' del lavoro fatto sul jazz stava dalla parte
> sbagliata senza che nessuno se ne fosse accorto.
>
> Il generatore e' ora **parametrico sulla forma** e ha scritto tre pezzi --
> blues, rhythm changes, modale. ⚠️ **Il 1 settembre 2026 la casella 5 --
> ruoli e spartizione -- e' stata CHIUSA, e il lettore di partiture NON e'
> servito** (§6-noviesdecies). La riga che lo rendeva necessario -- «nessun
> corpus in casa ha l'insieme che suona insieme» -- era **falsa**, ed era
> scritta in tre posti. Il **Jazz Trio Database** porta **1294 trii** con
> piano, basso e batteria allineati agli stessi beat, licenza MIT, 24 MB. Il
> numero che apre tutto: **il 59,7% delle battute di un walking vero non ha
> quattro note**, contro il 4,00 con deviazione 0,00 del generatore.
>
> ⚠️ **E il 30 agosto e' cambiato il metodo, non solo il contenuto.** Le
> caselle si riempiono **su domanda**, non a tappeto: sta nel comune di
> `docs/MUSICA.md`, e la ragione sta nei tempi -- la casella 6, riempita senza
> che un pezzo la chiedesse, e' costata **undici giorni**; le caselle 8, 7 e 11,
> ognuna aperta da un difetto sentito, **otto ore in tutto**. Il generatore e'
> stato reso **parametrico sulla forma**, e il secondo pezzo -- un rhythm
> changes AABA -- e' uscito giusto **alla prima versione** contro le sei del
> blues.
>
> Il **6 settembre 2026** le misure della casella 5 sono state **spese sul
> generatore** (§6-vicies), e il basso ha smesso di fare quattro note per
> battuta. Misurando sono usciti **tre errori**: la misura 3 contava come
> «fuori griglia» il 15% di onset che erano attacchi anticipati del battere
> (**1,52× diventa 1,60×**, e la correzione rafforza il risultato); il criterio
> pre-registrato della misura nuova era **fragile** — fissato sul picco di un
> istogramma, che si sposta cambiando l'ampiezza degli intervalli — e non ha
> potuto decidere; e nessun `print` può contenere `⚠️`, perché la console di
> Windows è cp1252. ⚠️ **L'aggancio della batteria è scritto ma NON riproduce
> la misura per cui esisteva**, e il difetto sotto è del basso: è quantizzato
> esatto, dispersione zero, e non può andare incontro a una batteria che ha il
> microtiming. **1096 test.** Il verdetto dell'ascolto sulla 08 non è ancora
> stato dato.
>
> ⚠️ **Il 10-11 settembre 2026 il livello musicale ha cambiato natura, e
> quella è la cosa da leggere per prima** (§6-unetvicies, e il progetto in
> `docs/superpowers/specs/2026-09-10-skill-compositiva-design.md`). Il
> generatore a dadi è stato buttato: *«una distribuzione descrive com'è fatto
> un insieme di dischi, non come si scrive una battuta»*. Al suo posto ci
> sono **istruzioni compositive** in `docs/istruzioni/`, fatte di
> **vocabolario e vincoli** e non di leggi — perché leggi compositive
> generalizzabili, nel jazz, non esistono. Le parti si **compongono battuta
> per battuta**, e le primitive fanno i conti. Basso e batteria del blues sono
> scritti così e sono stati approvati: *«la linea regge»*, *«molto meglio»*.
> **1124 test.**
>
> **Il 20 settembre 2026 si è chiusa anche la prova compositiva
> jazz+ contemporanea.** Da idee già presenti in `JUNGLEVAR` è nato un brano
> completo jungle/IDM: armonia jazz con colore simbolista francese, batteria
> interamente programmata (niente Amen e niente slicing), pad in lenta
> evoluzione, parameter lock e ratchet, e `BASS-PUSH` anticipato come hook.
> Dopo cinque versioni e correzioni d'ascolto, l'utente ha approvato
> `JUNGLEVAR05`: *«mi ritengo soddisfatto»* `[OSS]`, un ascoltatore e una
> sessione. Il file scritto via SysEx e quello riletto dal Deluge hanno lo
> stesso SHA-256. La suite conta **1997 test**. Il giro ha inoltre fissato una
> regola di macchina: su una song esistente la griglia si legge con
> `S.ticks_per_bar()`, perché `JUNGLEVAR` usa **192 tick per battuta** mentre
> le costanti canoniche del modulo ne usano 384; groove, ratchet e lock
> devono essere scalati su quella griglia.
>
> Per usarlo si invoca la skill **`deluge-pal`**
> (`.claude/skills/deluge-pal/SKILL.md`), che contiene il protocollo. Le sei
> regole di quel documento non sono consigli: ognuna nasce da un errore pagato.
> La **regola 0**, aggiunta il 16 agosto, è l'ordine in cui si cerca una
> risposta — vedi §0 qui sotto.

---

## Il prossimo lavoro

⚠️ **Il perimetro è stato DECISO l'11 settembre 2026, e questa è la cosa da
leggere per prima** (§6-duetvicies, e il progetto in
`docs/superpowers/specs/2026-09-10-skill-compositiva-design.md`). In breve:
supporto compositivo, priorità **1) armonia** (ampia + jazz + modale),
**2) forma** (voicing, contrappunto, comping, struttura), **3) ritmo** (solo
jazz-in-poi, con groove template). Niente filologia: si attinge al bagaglio
espressivo, non si replica un genere. Il flusso è armonizzare/arrangiare
un'idea → creare da zero → l'utente rifinisce sul Deluge. **L'armonia non
dipende dai corpus di performance: dipende dalla teoria.** ⚠️ **Il 12-13
settembre l'armonia si è allargata molto** — prestito modale (due case), le due
scale simmetriche, il cromatismo (planing e medianti); **il 13 la spina
funzionale** (ii-V-I, cadenze, turnaround, dominanti secondarie) e poi **la
dominante alterata e le code** (doppie medianti, diatonic planing, seste
aumentate), infine **ritmo armonico e i modi della minore melodica** hanno
**chiuso l'armonia della priorità 1, code comprese**. ⚠️ **Poi è cominciata la
priorità 2, la forma**, dal **voicing** (§6-septvicies), poi il **comping**
(§6-noniesvicies, con `MU.comping`), il **contrappunto** (§6-tricies, con
`MU.contrappunto`) e infine la **struttura**, in tre facce: la **mappa di forma**
(§6-untrigies, con `MU.forma`), l'**arco dinamico** (§6-duotrigies, con
`MU.dinamica`, che prova anche il ritmo armonico rimasto senza ascolto) e le
**transizioni** (§6-trestrigies, con `MU.variazione`, la clip bianca): ⚠️ **con
questo la priorità 2 (forma) è coperta.** ⚠️ **Poi è cominciata la priorità 3, il
ritmo**: il **fill** (§6-quattuortrigies, con `MU.controlla_fill`) e poi la
**reazione** — basso e batteria che reagiscono alla forma invece di applicarsi
acriticamente (§6-quinquiestrigies, con `MU.reazione`), la **correzione del difetto
d'origine** del progetto, e infine il **groove template applicato** — il tocco di un
batterista vero sopra la reazione (§6-sexiestrigies, con `MU.rimappa_dinamica`), dove
l'ascolto ha trovato che su un kit elettronico il template misurato **si
autodistrugge** se non si adatta la dinamica al kit. Poi l'**aggancio** — il basso
che va incontro alla batteria: il difetto d'origine era un basso quantizzato
esatto, e ora prende il **microtiming** (il float) di un basso JTD nominato
(§6-septiestrigies, con `MU.applica_microtiming` e `jtd.microtiming`), verdetto
*«ok funziona, quasi impercettibile ma va bene»* — un effetto piccolo, come il
residuo di posizione della batteria. ⚠️ **La coincidenza vera (1,60×) è stata
ARCHIVIATA il 15 settembre** — data bloccata e payload impercettibile, §6-septiestrigies.
Poi l'**interazione a livello di evento** — chiamata e risposta, la parte che mette gli
eventi *dove* l'altra li chiede (§6-octiestrigies, con `MU.interazione`): la faccia
**udibile** dell'interazione, verdetto *«ok funziona»*, e coglie ciò che la densità
di `reazione` non vede. ⚠️ **Poi sono cominciati i FEEL diversi dallo swing**
(16 settembre 2026), in ordine di priorità dall'utente — **funk, ballad,
twobeat**. ⚠️ **Il FUNK è FATTO:** batteria e basso *dritti*, in
`docs/istruzioni/batteria-funk.md` e `docs/istruzioni/basso-funk.md`, con
l'esempio lavorato `tools/funk_scritto.py` (e `test_funk_scritto`) — verdetto
d'ascolto batteria *«va bene»*, basso *«meglio, soddisfacente per il test,
niente di stellare»*. Il carattere: cassa sincopata sul *the one*, backbeat
forte + ghost, charleston in crome, `swing` a 50; il basso non cammina — riff
fitto (~7 note/battuta), fondamentale ribattuta + ottave + ghost + cromatismi,
agganciato alla cassa. ⚠️ **Una lezione di metodo, la stessa del Jazz Trio
Database:** il basso funk pareva senza corpus (JTD è walking, Weimar è la linea
solista) — invece stava in `to-read/MIDI/The_Magic_of_MIDI` (40 basslinee
misurate) e sul web; la domanda giusta era al disco, non «non c'è». ⚠️ **Anche
la BALLAD è FATTA** (16 settembre 2026), in `docs/istruzioni/basso-ballad.md` e
`batteria-ballad.md`, esempio `tools/ballad_scritto.py` (e `test_ballad_scritto`),
verdetto *«va bene»*. ⚠️ **Il caso difficile, e la lezione:** la sezione ritmica
della ballad **non ha corpus** (Groove MIDI senza feel «ballad», JTD parte da
102 BPM, Weimar dà solo il solista) — quindi è `[LIB]`+`[DEC]`, non `[MIS]`,
dichiarato. Il carattere: tempo lento (~58-60), basso in **2** (fondamentale sul
1, quinta sul 3, minime, scuro), batteria a **spazzole** (lo strofinìo sul
rullante è il motore, non il ride), comping tenuto rootless; il lilt di terzina
via `set_swing(66)`. ⚠️ **Due cose restano dichiarate mancanti:** il *rubato*
(non rappresentabile a BPM fisso, resta al solista) e le *spazzole vere* (un
campione; qui un kit soft di ripiego). ⚠️ **E una lezione di riflesso, colta
dall'utente:** avevo messo lo **spang-a-lang sul ride** su ogni battuta — un mio
automatismo dallo swing, **non dalle fonti**, e contro la mia stessa istruzione;
a tempo di ballad il ride col bastone non si usa (*«the volume isn't there»*), il
tempo lo tiene lo strofinìo. Corretto. ⚠️ **E il TWOBEAT è FATTO** (17 settembre
2026), in `docs/istruzioni/basso-twobeat.md` e `batteria-twobeat.md`, esempio
`tools/twobeat_scritto.py` (e `test_twobeat_scritto`), verdetto *«ok funziona»*.
Il 2-feel dixieland: come la ballad (1 e 3, minime) ma **veloce e saltellante** —
basso corto e brillante col **rilancio** cromatico e una battuta **«in 4»** al V7,
l'**oom-pah** (cassa 1-3 / charleston croccante 2-4), il **press roll**
approssimato sul rullante, comping **«stride»** sul 2 e 4, e **niente
spang-a-lang** (Riley p. 57: nel 2-feel meno figure di semiminima sul ride, e il
charleston croccante «con un po' di scatto» — è ciò che separa il twobeat dalla
ballad). ⚠️ **La sezione ritmica è `[LIB]`+`[DEC]` come la ballad** (nessun corpus:
Weimar dà il solista, JTD walking da 102 BPM, Groove MIDI senza feel «twobeat»);
il `[MIS]` copre solo genere (Weimar TWOBEAT = 100% TRADITIONAL, 8 solisti —
Armstrong, Bechet, Kid Ory, Bix, Dodds), tempo (mediana 184) e swing (jazz.md
casella 4, fascia 180-240: levare 63,7%, `set_swing(62)`). ⚠️ **Con questo i tre
feel prioritari — funk, ballad, twobeat — sono FATTI.** Restano i **sottogeneri**
(l'altro asse, qui sotto in «I feel ritmici, e i sottogeneri») e l'**interazione a
più di due parti**, più in là. ⚠️ **E il 17 settembre 2026 è aperto il PERIMETRO 3
(i contemporanei) col primo genere: l'hip hop boom-bap** — batteria `[MIS]` (Groove
MIDI, dritto, BUR 1,03), basso `[LIB]`+`[DEC]`, sub rado agganciato alla cassa. Sta
in `docs/istruzioni/batteria-hiphop.md` e `basso-hiphop.md`, esempio
`tools/hiphop_scritto.py` (e `test_hiphop_scritto`), **scheda
`docs/repertori/hiphop.md`** con la sua riga nell'indice di `MUSICA.md`. Verdetto
*«ok funziona»*. ⚠️ **E il SECONDO genere è HOUSE/TECHNO** (four-on-the-floor):
`[LIB]`+`[DEC]` — niente corpus (generi programmati; il `dance` di Groove MIDI è
7 esecuzioni, 2 batteristi = `[OSS]`). Cassa su ogni movimento, open hat sui
levare, basso **fuori** dalla cassa a ottave (l'opposto dell'hip hop), kit 808.
`docs/istruzioni/batteria-house.md` e `basso-house.md`, esempio
`tools/house_scritto.py` (e `test_house_scritto`), **scheda
`docs/repertori/house.md`** con la sua riga nell'indice. Verdetto *«funziona»*.
⚠️ **E il 17 settembre 2026 l'essenza di house/techno è FATTA** — l'**arrangiamento**
(build/drop) e il **suono in movimento** (filtro + **sidechain interno del Deluge,
NON il compressore** — sono due elementi XML distinti, `<sidechain>` vs
`<audioCompressor>`; correzione esplicita dell'utente). Due primitive nuove in
`musica.py`: **`MU.apri_filtro`** (la rampa del cutoff in unità display 0-50, vive
nella clip) e **`MU.sidechain`** (send pieno sul kick + `sidechainCompressorVolume`
nei `<params>` di ogni clip del bersaglio + sync nell'elemento `<sidechain>`).
L'arco a 32 battute (intro/build/drop/breakdown/drop) in `tools/house2_scritto.py`
(e `test_house2_scritto`), steso con `MU.forma`; l'istruzione
`docs/istruzioni/arrangiamento-house.md`; **caselle 9 e 10 della scheda piene** e
l'indice aggiornato. ⚠️ **Il corpus NON aveva un esempio di volume-ducking**
(memoria `corpus-non-autoritativo`): la struttura si è presa dallo schema c1.3.0 e
dai file veri (`[OSS]`), la magnitudine (`0xDE000000`) si è tarata all'orecchio.
Caricato come `HOUSE02`, verdetto *«va bene»*.
⚠️ **E il 18 settembre 2026 il TECHNO ACID chiude la casella 8** — il TB-303. Due
primitive nuove: **`MU.acid`** (sullo strumento mono + osc `saw`/`square`; su ogni
clip risonanza alta + cutoff basso + portamento + env2 percussivo + i patch cable
`envelope2→lpfFrequency` lo squelch e `velocity→lpfFrequency` l'accento — attestati
`[OSS]` nel corpus, 157×/129×) e **`MU.automatizza`** (generalizza `apri_filtro` a
QUALUNQUE parametro, per rampare cutoff **e** risonanza; `apri_filtro` ne è ora il
wrapper). ⚠️ Il preset `Square Saw Bass` **era già quasi un 303** (aveva portamento,
`<envelope2>`, `envelope2→lpfFrequency`): niente scritture al buio. Pezzo
`tools/acid_scritto.py` (e `test_acid_scritto`), istruzione `docs/istruzioni/acid.md`,
casella 8 della scheda piena. Caricato come `ACID01`, verdetto *«l'idea generale
c'è»*. ⚠️ **Le rampe di cutoff E risonanza sono viste sul dispositivo** (l'utente
le ha guardate, 18 set 2026): il `[da verificare]` sulla risonanza in automazione è
sciolto. ⚠️ **E una direttiva dell'utente, data qui:** i *livelli* (risonanza 40,
gli amount, i decay) sono **sfumature compositive, non leggi assolute** — sono buoni
punti di partenza, non si tarano al millimetro né si trattano come `[da verificare]`
bloccanti (memoria `livelli-sfumature-non-leggi`). La risonanza 40 è lasciata così.
**1496 test.** Di house/techno resta solo il **vocal chop** (materiale di `audio.py`).
⚠️ **E il 18 settembre 2026 il TRIP-HOP** (terzo genere del perimetro 3) — la
**fusione** hip-hop + dub + armonia minore jazzy (sapore Portishead), non una
capacità nuova ma una ricombinazione. Una primitiva: **`MU.eco_dub`** (l'eco dub —
elemento `<delay>` `analog` che degrada + sync + `delayFeedback`; riusabile per
dub/reggae). Pezzo `tools/triphop_scritto.py` (vamp `Cm9|Cm9|A♭maj7|G7♭9` chiuso col
`[CALC]`, batteria boom-bap rallentata, basso dub, forma intro→full), istruzione
`docs/istruzioni/trip-hop.md`, **scheda nuova** `docs/repertori/trip-hop.md`
scorporata dall'aggregato dell'indice. Caricato come `TRIPHOP02`, verdetto *«per il
resto va bene»*. ⚠️ **REGOLA NUOVA dell'utente, e vale SEMPRE col delay:** a fine
brano il **feedback non deve restare positivo** (oltre il 50%, hex > `0x0`) o l'eco
non decade (drone/runaway, peggio con `analog` che auto-oscilla) — `MU.eco_dub`
default 24, **gate in `MU.avvertenze()`** che guarda il valore finale (memoria
`delay-feedback-non-positivo`). **1515 test.**
⚠️ **E il 19 settembre 2026 il VOCAL CHOP** — la casella 8 (il sample tagliato) di
house/trip-hop, il primo lavoro sui **campioni**. Primitiva **`kit.affetta`** (in
`kit.py`): affetta un campione in un kit di N drum-fetta (copie di un drum base, una
`<zone>` `[i*frames//n, (i+1)*frames//n]` per drum, REPEAT MODE **ONCE**). Riusabile
per il **break** di jungle/DnB (stesso gesto). Pezzo `tools/vocalchop_scritto.py`
(l'«mmyeah» dell'utente, `SAMPLES/RECORD/REC00027.WAV`, 142725 frame, in 8 fette su
un beat house), istruzione `docs/istruzioni/vocal-chop.md`, casella 8 aggiornata.
Caricato come `VOCALCHOP03`, verdetto *«ora sento le fette»*. ⚠️ **Due lezioni
pagate** (memoria `rappresentazione-o-pattern`): (1) una **fetta e' ONCE + `<zone>`**
— e' la ZONA a delimitare, non il mode; ONCE non suona «tutto il file», suona la
zona caricata (mi ero sbagliato due volte, ipotizzando CUT). L'ho scoperto facendo
**affettare il campione all'utente sul dispositivo** e confrontando i byte: il mio
drum era identico a quello dello Slicer nativo. (2) Il difetto udibile era il
**pattern** (fette in fila = la parola ricostruita), non il formato. ⚠️ **`dir` via
SysEx FUNZIONA** su c1.3.0 (cartelle non enormi) — il vecchio HANDOFF diceva di no.
**1527 test.** ⚠️ **Ora lo slicing c'e'**, quindi DnB/jungle (break tagliato) non
aspettano piu' un prerequisito: restano da aprire, ma il pezzo grosso (`kit.affetta`)
e' fatto. La scelta del genere è dell'utente (gusti eclettici); gli altri
contemporanei (DnB/jungle; elettronica/IDM) restano da aprire. ⚠️ **Il metodo cambia
per area:** l'armonia si
chiude col solo `[CALC]`; il **voicing** (parte d'orecchio) con `[CALC]` **+ un
ascolto**; il ritmo con l'ascolto pieno. Decisione dell'utente. ⚠️ **È arrivata
letteratura nuova (Levine ×2, Piston *Counterpoint*, Crook) e tutta l'armonia è
stata rivista con Levine: §6-octovicies** — Levine nomina le chord-scale che Smith
rifiutava, e ora hanno `[LIB]`. I tool djvu sono installati (memoria
`letteratura-composizione`).
⚠️ **E il 19 settembre 2026 il DnB/JUNGLE** — primo genere della riga aggregata
«elettronica · IDM · DnB · jungle», **scorporato** dall'aggregato dell'indice. Non una
capacità nuova: lo slicing (`kit.affetta`) è **lo stesso gesto del vocal chop** — cambia
il materiale (un break, non una voce) e il fine del chop (**ricostruire** un groove e poi
editarlo, non rompere una parola). Il break: `original AMEN.wav` (già stretchato a **171
BPM**, 4 battute, 268795 frame, su `SAMPLES/sampleswap/...`) in **64 fette** da 1/16 —
⚠️ **a song = tempo nativo del break** la durata della fetta combacia col passo di 1/16,
quindi in ordine il break si ricostruisce esatto (ONCE + zona), ri-sequenziato dà il
chop. Il chop lavora **per beat** (4 fette contigue = un movimento coerente), casse gravi
(fette 0/24/56, `[OSS]` da un'**analisi di energia stdlib** — RMS + banda grave, niente
numpy) sui movimenti forti, due rullate a chiudere le frasi. ⚠️ **Feel DRITTO
(swing 50):** il micro-timing del break è **nell'audio** delle fette; uno swing di song
lo sposterebbe due volte — è il rovescio dello swing jazz (memoria
`riflesso-idioma-fuori-contesto`, ora citata anche qui). Sotto, il **half-time** lo dà il
contrasto: **sub** rado e gravissimo (Square Saw Bass scurito, fondamentale sul 1 +
spinta sul 4) e **armonia** minore cinematica `Cm9 | A♭maj7 | Cm9 | G7♭9` (i–♭VI–i–V7♭9,
`[CALC]`, il colore del trip-hop) su Tal Rhodes tenuto + velo di riverbero. Forma
intro→drop→breakdown→drop, 32 battute, `MU.forma`. Pezzo `tools/dnb_scritto.py` (e
`test_dnb_scritto`), istruzione `docs/istruzioni/dnb-jungle.md` (rimanda a
`vocal-chop.md`), **scheda nuova** `docs/repertori/dnb-jungle.md` con la sua riga
nell'indice. ⚠️ **NIENTE CORPUS** DnB/jungle (Groove MIDI non ha l'etichetta):
`[LIB]`+`[DEC]`; break e analisi fette `[OSS]`, armonia `[CALC]`, chop/arco/livelli
`[DEC]`. **DNB01.XML** scritto sulla SD direttamente (era in `E:`), 64 fette. ⚠️ **Poi,
su richiesta dell'utente («aggiungi solo il campione, poi lo suono io»), aggiunto al kit
AMEN un drum in più — l'AMEN INTERO in one-shot** (zona `[0, FRAMES]`, ONCE; NON
sequenziato, per sentire il break originale innescandolo a mano). Kit a **65 righe**.
Trasferito **via SysEx come DNB02.XML** (la SD era tornata nel Deluge; `put` non
sovrascrive DNB01 e via SysEx non c'è delete → versione nuova), **verificato per
rilettura (hash identico)**. ⚠️ **`dir` via SysEx non rispondeva** (lettura larga, perdita
pacchetti in ricezione) mentre `ping` e `put` (scrittura, riparata dal firmware) vanno:
per il numero di versione mi sono fidato dello stato noto, e `put` è comunque un cancello.
**Verdetto d'ascolto (19 settembre 2026): «va bene»** (come house/hip-hop) — il chop,
l'arco e i livelli restano `[DEC]`, rifinibili. **1540 test.**

### I feel ritmici, e i sottogeneri — l'agenda del ritmo, 15 settembre 2026

⚠️ **Finora il ritmo è tutto SWING** (walking, ride col giggidì, la misura dello
swing, i groove template scelti). Il corpus ne ha molto di più. L'utente ha
deciso di restare sul **feel** (non sui sottogeneri, per ora) e ha dato la
priorità: **1) funk, 2) ballad, 3) twobeat**. Conteggi presi il 15 settembre
2026 (stato del disco: `wjazzd.db`, Groove MIDI).

⚠️ **Il cancello di sempre:** un'etichetta con pochi musicisti è `[OSS]` su un
esecutore, non `[MIS]` su un repertorio (la lezione del reggae). Per il feel
servono i solisti in Weimar (armonia/frase/vocabolario) **e** i batteristi in
Groove MIDI (il groove template) — e i due lati non hanno la stessa copertura.

| feel | Weimar `rhythmfeel` (assoli / solisti) | Groove MIDI (beat / batteristi) | nota |
|---|---|---|---|
| ~~SWING~~ | 361 / 67 | jazz 24/4, jazz/swing 11/2 | **fatto** |
| ~~1. FUNK~~ | 20 / 9 | funk 36/4 (33 dritte) | **fatto** (16 set 2026): batteria+basso dritti. Etichetta `funk` esatta, BUR 1,02 (esclusi `purdieshuffle`/`fast`, swingati); basso ~7 note/battuta `[MIS]` su 40 basslinee di `The_Magic_of_MIDI`. Template `drummer8/session1/1`. Verdetto «va bene» / «soddisfacente» |
| ~~2. BALLAD~~ | 10 / 7 | — (nessun feel «ballad») | **fatto** (16 set 2026): comping + basso in 2 + spazzole, `[LIB]`+`[DEC]` (niente corpus). Lo strofinìo tiene il tempo, non il ride; lilt via `set_swing(66)`. Restano rubato e spazzole vere. Verdetto «va bene» |
| ~~3. TWOBEAT~~ | 32 / 8 | — (nessun feel «twobeat») | **fatto** (17 set 2026): 2-feel dixieland — basso 1-3 corto e saltellante (rilancio + una battuta «in 4»), **oom-pah** (cassa 1-3 / charleston croccante 2-4), press roll approssimato, comping «stride» 2-4, niente spang-a-lang (Riley p. 57). `[LIB]`+`[DEC]` come la ballad; `[MIS]` solo su genere (100% TRADITIONAL, 8 solisti) e tempo (mediana 184). Verdetto «ok funziona». `basso-twobeat.md`/`batteria-twobeat.md`, `tools/twobeat_scritto.py` |

⚠️ **Metodo: ritmo = ascolto pieno.** E il feel non è solo `set_swing`: cambia il
vocabolario del basso (il funk non cammina), del ride/comping, degli accenti. Il
primo passo del funk è probabilmente spegnere lo swing e riscrivere basso e
batteria dritti — ma va disegnato, non dedotto.

**I sottogeneri jazz — l'ALTRO asse, per più avanti.** Non sono un feel: sono il
**dialetto** melodico/armonico del solista (frase, scelte d'accordo), e toccano la
priorità 1-2 più del ritmo. Salvati qui su richiesta dell'utente («ci torneremo»),
da `wjazzd.db` (assoli / solisti):

| sottogenere | assoli / solisti | | sottogenere | assoli / solisti |
|---|---|---|---|---|
| POSTBOP | 147 / 29 | | TRADITIONAL | 32 / 8 |
| HARDBOP | 76 / 17 | | FUSION | 20 / 9 |
| SWING | 66 / 14 | | FREE | 5 / 1 (`[OSS]`) |
| BEBOP | 56 / 12 | | COOL | 54 / 9 |

Si filtrano con `WJ.elenco(db, rhythmfeel=…)` e `WJ.elenco(db, style=…)`; le
etichette esatte con `WJ.valori(db, 'rhythmfeel')` / `'style'`.

⚠️ **Ma la faccia ARMONICA di quest'asse è un vicolo cieco, MISURATO il 17
settembre 2026** (`docs/repertori/jazz.md`, casella 1, «I sottogeneri NON si
distinguono per armonia»): bebop/cool/hardbop/postbop parlano la **stessa lingua
armonica** (dom7 ~45-50%, min7 ~24%, maj7 ~12%), e i due soli stili che spiccano —
TRADITIONAL (triadi + seste) e POSTBOP (sus/quartali + ritmo armonico più lento) —
sono **già nei moduli** (`armonia-funzionale`, `armonia-modale`, `ritmo-armonico`).
Il sapore armonico di un sottogenere è una **scelta compositiva**, non
un'estrazione. Del corpus resta da aprire solo la faccia **melodica** — il
dialetto del solista sopra le changes (tensioni, cromatismi, note «fuori») — che è
**casella 8 (la linea)**, non armonia. Decisione dell'utente: non aprire il
corpus finché l'interesse è armonico.

Il testo qui sotto è la formulazione ORIGINALE del lavoro, tenuta perché resta
vera nel merito — «serie competenze compositive» — ma ora ha una direzione
precisa.

**Le competenze compositive.** L'utente lo ha detto in chiaro dopo aver
ascoltato il terzo tentativo di dub:

> «Serve sicuramente che Pal acquisisca serie competenze compositive, che al
> momento sono limitatissime. Ce ne occuperemo prossimamente: sto raccogliendo
> moltissimo materiale e in una prossima chat ci occuperemo di costruire un
> database serio.»

È il lavoro nominato, e tutto il resto è secondario.

---

### ⚠️ ~~IL PROSSIMO PASSO CONCRETO: un lettore di partiture~~ — SUPERATO il 1 settembre 2026

> ⚠️ **QUESTA SEZIONE È STATA SMENTITA, e resta perché il modo in cui era
> sbagliata vale più del suo contenuto.** Il lettore MusicXML non serviva alla
> casella 5, e la casella 5 è stata chiusa senza di lui: vedi
> **§6-noviesdecies**. Ciò che segue è il ragionamento del 30 agosto, con le
> correzioni marcate. Il MusicXML resta invece la strada per **classica,
> barocca e antica** (OpenScore Lieder e String Quartets, **CC0**), dove il
> materiale notato con licenza c'è davvero.

**Non è una casella da riempire: è l'infrastruttura senza cui tre lavori
diversi si sono fermati nello stesso giorno.** Sta scritto per esteso nella
casella 5 di `docs/repertori/jazz.md`, «Le tre cose che questa casella ha
fermato»; qui c'è il perché in breve.

Il generatore scrive quattro parti — batteria, basso, comping, tema — e **non
sa come si rispondono**. Il basso esce a 4,00 note per battuta con deviazione
**zero** su 228 battute; la batteria, resa varia, suona scollata perché varia
contro uno sfondo fermo. L'utente:

> «Le interruzioni, accenti e struttura delle parti di batteria sono
> strettamente correlati alla sezione ritmica, e non le puoi applicare
> acriticamente.»

⚠️ ~~**E quella correlazione non è misurabile da nessun corpus in casa.** Il
Groove MIDI è **batteria sola**; `wjazzd.db` è **la linea solista sola**.
Nessuno dei due ha l'insieme che suona insieme — non è questione di quanti
dati, è che il dato non esiste.~~ **FALSO, verificato il 1 settembre 2026:**
nessuno aveva cercato fuori da quei due. Il Jazz Trio Database ha i tre
strumenti allineati agli stessi beat, licenza MIT, e la misura si è presa in
un pomeriggio. Interpellato il 30 agosto, l'utente aveva risposto: *«non ho
conoscenze sufficienti per risponderti, credo serva lettore»* — e la domanda
giusta non era a lui, era al disco.

**Serve quindi MusicXML** — `xml.etree` + `zipfile`, stdlib, costo di lettura
≈ zero, ed è già la decisione presa il 17 agosto («La decisione sui formati
simbolici»). Con `**kern` come seconda fonte, che porta l'analisi già fatta.

⚠️ **È anche l'unico caso in cui il metodo del comune dice di VEDERE ARRIVARE
il lavoro invece di aspettare che un pezzo lo chieda**: nessun ascolto può
produrre un lettore di partiture a metà pomeriggio. Il metodo su domanda copre
tutto ciò che è già raggiungibile; questo no.

**Da dove si comincia, adesso che lo schema esiste: dall'indice in fondo a
`docs/MUSICA.md`.** Non serve una lista di cose da fare a parte — ogni casella
vuota dichiara *cosa servirebbe per riempirla*, quindi l'agenda si legge dalla
matrice.

⚠️ **Questa tabella è ora VUOTA: tutt'e due le caselle che elencava sono
chiuse**, la 6 il 25 agosto e la 8 il 29. Resta come storia, e perché la riga
barrata dice più della sua assenza. ⚠️ **Chi cerca il prossimo lavoro NON lo
trova qui: lo trova nell'indice in fondo a `docs/MUSICA.md`**, dove il jazz ha
ancora vuote la 1, la 2 e la 5, e gli altri tre repertori del perimetro le
hanno vuote tutte e undici.

⚠️ La nota che questa tabella portava, e che vale ancora: **dava due caselle
per vicine a chiudersi, e il 25 agosto 2026 ne restava una.** La riga che c'era prometteva che il Groove MIDI avrebbe
chiuso «la 6 del jazz e i `[WEB]` della 6 del reggae»: **per il jazz è andata
così, per il reggae era falsa**, e il perché sta due righe più giù. È corretta
invece che lasciata perché è dall'agenda che la prossima sessione decide dove
mettere le mani, e un'agenda ottimista la rimanderebbe esattamente lì.

| casella | cosa la chiude, e dov'è |
|---|---|
| ~~**jazz 6** (dinamica)~~ | **chiusa il 25 agosto 2026**, dal ramo `groove-midi`: velocity, profilo posizionale e microtiming residuo di **cinque batteristi** del Groove MIDI, con la scheda che porta accanto a ogni numero quante esecuzioni e quanti batteristi lo reggono. Vedi §6-terdecies |
| ~~**jazz 8** (melodia e ornamentazione)~~ | **chiusa il 29 agosto 2026**, da `wjazzd.db`: l'arco del giro su **66 assoli e 38 solisti**, la soglia del motivo su 80, e l'ornamentazione su 166 346 note. Lo strumento e' `tools/misura_melodia.py`. Vedi §6-sexdecies |

⚠️ **La 6 del reggae il Groove MIDI NON la chiude, e non è una questione di
sforzo.** Di reggae quel dataset porta **venti esecuzioni**, che sono **quattro
`beat` continue** — a 78, 64, 141 e 126 BPM, **due di `drummer1` e due di
`drummer5`**, **dieci minuti in tutto** — più sedici fill di due-tre secondi
l'uno, tutti di `drummer1`, che valgono altri 43 secondi. **Due batteristi.** E
dentro la fascia di tempo che la casella 3 del reggae dichiara ci cadono **due
sole** di quelle quattro, la 78 e la 64, **entrambe di `drummer1`**.
Firmare quei numeri `[MIS]` col nome del genere sarebbe travestire un esecutore
da repertorio, che è precisamente ciò che la casella 8 del jazz vieta in una
riga: *un assolo è un musicista, non un repertorio*. La 6 del reggae **resta
`[WEB]`**, e adesso ci sta scritto il conteggio col motivo. Il jazz, per
confronto, ne ha **101** (50 `beat` e 51 `fill`) e **cinque** batteristi — ed è
già il minimo per cui valga la pena.

Cosa c'è già in mano:

| | |
|---|---|
| `docs/MUSICA.md` | non è più vuoto: uno schema neutro di **undici caselle**, pensato per reggere da Josquin alla jungle, più **il comune** a ogni repertorio e **l'indice** — la matrice repertorio × casella che è anche l'**agenda**: dice cosa manca a quale repertorio senza aprire niente. I repertori compilati sono schede a sé in `docs/repertori/`: oggi reggae/dub e jazz, stato di ciascuna nell'indice |
| `tools/delugexml/midi.py` | il ponte per far entrare il materiale: legge Standard MIDI File **senza dipendenze**, validato nota per nota contro `mido` |
| `tools/delugexml/groove.py` | il lettore del **Groove MIDI**, sopra `midi.py`: cerca per stile, batterista e metro, e ne cava la scala di velocity e il **groove template** (§6-terdecies). Dal 26 agosto 2026 il passo su cui un colpo viene contato si sceglie con `taglio=`, e il default **non** è più il passo più vicino: §6-quaterdecies |
| `to-read/` | 112 000 file e 4,8 GB di libri, paper e librerie MIDI già raccolti dall'utente. **Fuori dal versionamento** |

### Il perimetro vero, detto dall'utente il 17 agosto 2026

**Il dub era solo un banco di prova, non l'obiettivo.** Va scritto perché
tutta la documentazione precedente — questo file compreso — è tarata su di
esso, e chi la leggesse ne dedurrebbe uno scopo sbagliato:

> «Ho usato il dub solo come esempio per testare. Ho gusti musicali eclettici
> e mi piacerebbe coprire uno spettro compositivo più ampio possibile, dalla
> musica antica ai generi contemporanei, passando per classica e jazz.»

E l'ordine di priorità, dato subito dopo:

| | |
|---|---|
| **1** | **jazz** — «mi interessa moltissimo» |
| **2** | classica, barocca, antica (in quest'ordine) |
| **3** | i generi contemporanei: elettronica, IDM, techno, hip hop, trip hop, dub, DnB, jungle |
| — | **folk: lasciar perdere**, non interessa |

Il folk fuori dal perimetro ha un effetto collaterale utile: **spariscono i
due problemi di licenza** che bloccavano il materiale simbolico. TheSession
(40 000 melodie in ABC) vieta esplicitamente l'uso con LLM, e la Essen
Folksong Collection è distribuita a licenza. Erano entrambi folk.

### La decisione sui formati simbolici — 17 agosto 2026

La domanda era se valesse la pena aggiungere ABC, `**kern` o MusicXML.
**Per suonare sul Deluge nessuno serve**: MIDI porta già altezza, attacco,
durata e velocity, che è esattamente il modello dati del dispositivo. Servono
per *imparare*, e portano tre cose che MIDI non può portare: la **grafia**
(fa♯ contro sol♭), la **separazione delle voci**, e l'**analisi già fatta da
umani**.

| formato | esito | perché |
|---|---|---|
| **`wjazzd.db`** | **primo** | non è un formato di partitura ma è dove sta il jazz: 456 assoli con accordi e battiti allineati, **già su disco** in `to-read/MIDI/`, e si legge con `sqlite3` della stdlib |
| **MusicXML** | **sì** | costo ≈ zero (`xml.etree` + `zipfile`, stdlib: è XML *ben formato*, al contrario di quello del Deluge) ed è l'ingresso universale. Il suo `<harmony>` porta i simboli di accordo, quindi serve **anche** il jazz |
| **`**kern`** | **sì, dopo** | l'unico con l'analisi: `BachChoralesAnalyzed` ha lo spine `**harm` allineato movimento per movimento, e il Josquin Research Project è la musica antica, che non esiste altrove |
| **ABC** | **no** | licenza bloccata sul corpus grosso, ed è un formato folk: non ha antica, classica, jazz né contemporanea |

⚠️ **I generi contemporanei non esistono come repertorio notato**, e non è una
lacuna da colmare: il loro materiale sono i groove (MIDI, già in `to-read/`),
l'arrangiamento (`arranger.py`) e il suono (`sound.py`). Per jungle e DnB il
materiale compositivo è il **break tagliato**, che vive in `audio.py` e nelle
righe di kit, non in nessuna notazione.

⚠️ **Da sapere prima di ripartire:** le due skill di composizione sono ora
**due**, e nessuna delle due sa il reggae — vedi `SKILL.md` e la casella 11,
«Trappole del generatore», di `docs/repertori/reggae-dub.md`. I due difetti
di `music-composer` sono stati riparati a mano
il 16 agosto in una skill *globale* dell'utente, fuori da questo repo: se
viene reinstallata spariscono.

E una lezione di metodo che vale per tutto il lavoro futuro sui generi:

> **Una ricerca sola su un genere dà le etichette, non il mestiere.** Il primo
> dub è stato scritto dopo *una* ricerca web, da cui erano usciti i nomi (one
> drop, rockers, steppers) e nient'altro. Bastavano a produrre qualcosa di
> formalmente corretto e musicalmente morto — mancavano lo skank, il bubble,
> il turnaround, i colpi fantasma e lo swing, cioè tutto.

### Gli altri punti, in ordine di valore

⚠️ **0. La batteria va RIFATTA, e non e' un difetto da poco.** Il 30 agosto
2026 e' stata resa varia **campionando** le frequenze di tre esecuzioni
diverse: toglie il sintomo (i pezzi non suonano piu' uguali) col metodo che la
regola «relazioni, non superfici» vieta, e ne introduce uno nuovo che l'utente
ha sentito subito -- suona **scollata** dalla sezione ritmica. Va generata da
**forma + ensemble + idioma**, col corpus usato per il solo *feel*. ⚠️ **Dal
1 settembre 2026 non è più bloccato:** la casella 5 dice di quanto varia un
walking vero e a cosa si aggancia la batteria (§6-noviesdecies). Il lavoro è
adesso **spendere** quelle misure nel generatore, e farlo sentire.

**1. Le due misure rimaste aperte**, entrambe piccole e con il metodo ormai
collaudato (una coppia controllata, un passo di differenza):

- **cosa governano `inKeyScrollOffset` e `drumsScrollOffset`.** Si sa solo che
  *non* governano la clip view: non si muovono scrollandola. Finché non si sa,
  non si scrivono.
- **se riordinare le righe di un kit rinumeri i `drumIndex`.** Vedi la nota in
  fondo a FINDINGS §6-octies.

**2. I punti aperti sul formato** in §7, che sono lì da prima e non bloccano
niente.

~~**3. Due code della pubblicazione**~~ — **chiuse il 30 agosto 2026**,
insieme a una terza che non era in lista: la tabella `COPPIE_OSSERVATE` non
aveva lo script che la rigenera. Vedi §9.

### Cosa NON rifare

- **non estendere un controllo a un caso non misurato.** È costato quattro
  modelli sbagliati di fila il 16 agosto (§6-sexies). Se non c'è una coppia
  controllata, il controllo resta fuori e lo dice.
- **non scrivere in un attributo che non si è capito.** Due dei quattro difetti
  nascono da lì.
- **non usare il corpus come cancello.** Regola data dall'utente il 16 agosto e
  già costata una volta: il corpus dice cosa ha suonato *lui*, non cosa il
  firmware accetta. Il numero che lo dimostra: il firmware espone **56**
  destinazioni di patch cable, il corpus ne usa **37**. Per sapere cosa il
  firmware accetta si guarda `param_ids.py` (dall'enum di `param.h`) e il
  guidebook, mai il corpus.
- **non dire «verificato sul dispositivo» avendo ascoltato**, se
  l'affermazione riguarda ciò che si vede. E viceversa.
- **non scrivere un file con `pathlib.write_text()` nudo.** Su Windows traduce
  `\n` in `\r\n`, e un documento che era a LF esce tutto riscritto: due agenti
  diversi ci sono cascati nella stessa sessione del 24-25 agosto, gonfiando un
  diff da **260/92 righe a 1773/1293** — l'85% non era contenuto. Non corrompe
  niente e non rompe nessun test: rende **illeggibile la revisione**, che è il
  meccanismo su cui poggia tutto quello che è scritto qui. Si usa
  `write_bytes()`, oppure `open(..., newline='')`, e **prima di committare** si
  controlla che `git diff --stat` e `git diff --stat --ignore-cr-at-eol` diano
  lo stesso numero.

---

## Il ciclo, in breve

```
prompt  →  libreria  →  XML  →  SysEx  →  l'utente apre e ascolta
                                                  ↓
      ricarica come     ←   modifica   ←   «il basso è troppo statico»
      versione nuova          ↑
                     RISCARICA dal Deluge prima di toccare
```

**La fonte della verità è il file sul dispositivo**, non una copia locale:
l'utente la apre e può averci messo mano.

**Dove si scrive.** Solo dentro una sottocartella `DelugePal` delle quattro
cartelle di primo livello: `/SONGS/DelugePal/`, `/KITS/DelugePal/`,
`/SYNTHS/DelugePal/`, `/SAMPLES/DelugePal/`. Il percorso si costruisce con
`musica.destinazione()`, mai a mano. **In lettura invece l'accesso è libero su
tutta la SD** — l'asimmetria è voluta: si legge ovunque, si scrive solo in casa
propria. Il 15 agosto è servita una pulizia di 34 file di prova finiti in mezzo
alle 135 song dell'utente.

**La SD è stata ripulita il 16 agosto**, con la scheda nel lettore del PC. In
`/SONGS/DelugePal/` c'erano rimaste due song, e il 16-17 agosto se ne sono
aggiunte tre del pezzo dub (§6-septies):

| | |
|---|---|
| `TEMPL0.XML` | la **base pulita** da cui partire: uno strumento, una clip **senza righe né note**, arrangiamento vuoto, 158 BPM in re maggiore. È lo stesso file da cui nasce `create.CLIP_BASE`, copia verificata di `refs/songs/TEMPL0.XML` |
| `TRASF205.XML` | l'unica song generata **dopo** tutte le correzioni della finestra di clip view: si rilegge, passa il cancello senza avvertenze, entrambe le clip ancorate |
| `DUBPAL01/02/03.XML` | il primo pezzo vero, in tre versioni. **`DUBPAL02` e `DUBPAL03` sono state risalvate dall'utente sul dispositivo**, quindi la copia in `out/` NON è più la verità: riscaricare prima di toccarle (regola 1) |

Tolti 32 file fra rotti, versioni superate e artefatti delle sessioni
precedenti — comprese `USBGEN.XML` e `AUTOFULL.XML`, che stavano alla radice
di `/SONGS/`. Le sei song delle misure erano già in `refs/songs/` e
committate: la verifica per hash è stata fatta prima di cancellarle.

Nota su `TEMPL0` come base: la sua clip porta `yScroll="37"` e
`inKeyMode="1"`, ed è **quel 37 che si è propagato** in ogni clip generata
fino al 16 agosto, causando il difetto della finestra (§6-sexies). Non è un
problema del file — caricandolo sul Deluge e suonandoci sopra, la vista la
gestisce il dispositivo — ma di chi ne eredita gli attributi senza
ricalcolarli. Oggi `fit_clip_scroll_to_notes()` lo fa, ed è la ragione per cui
va chiamata sempre dopo aver scritto note.

Le 133 song dell'utente alla radice non sono state toccate. **Attenzione a
`Perche.XML`**: sta alla radice di `/SONGS/`, il nome sembra un file di prova
e invece è una song dell'utente — è byte-identica alla copia in `refs/songs/`,
da cui viene metà del reverse engineering. Il file di prova omonimo era
`PercheN.XML`, e non c'è più.

⚠️ **Come si era sporcata, per non rifarlo.** Cinque file erano finiti sulla
SD col nome **troncato** (`TRASF0`, `TRASF1`, … senza estensione) e uno come
voce da **0 byte**, perché un percorso costruito in PowerShell conteneva un
NUL: in una stringa a virgolette doppie `` `0 `` è l'escape del carattere
nullo. Il Deluge non li mostrava nemmeno come song. `put` si era dichiarato
«verificato per hash» ogni volta, perché rilegge il percorso su cui ha
scritto e non quello che si voleva — vedi `docs/SYSEX.md`, «la verifica per
hash di `put` non è una verifica di destinazione».

`dir` via SysEx non risponde su questo firmware, quindi con la SD nel Deluge
l'elenco vero della cartella si vede solo dallo schermo; con la SD nel lettore
si guarda da `E:\SONGS\DelugePal\`, che è molto più comodo per fare pulizia.

---

## 0. Leggi prima questo

Il progetto ha una regola che è costata caro impararla:

> **La documentazione dice cosa deve valere. I file dicono com'è scritto. Solo
> il dispositivo dice se funziona.**

Nella sessione del 12 agosto ho ripetutamente saltato il primo e il terzo
livello, deducendo dai file, e ho sbagliato ogni volta. In particolare:

- ho fatto reverse engineering statistico su cose spiegate in una frase del
  manuale;
- ho dichiarato **risolto** il problema principale perché la clip risultava
  presente nel file XML dopo un salvataggio del dispositivo. **Non lo era**:
  guardando lo schermo, la clip non c'è. Essere nel file non dimostra essere
  stata caricata.

Prima di dichiarare qualcosa risolto: **guardalo sul Deluge.**

### E la contromisura, aggiunta il 16 agosto: l'ordine di ricerca

Direttiva dell'utente, data dopo l'ennesima ricaduta. La regola sopra dice
**chi vince**; questa dice **da dove si comincia**, e va nella direzione
opposta:

```
1. documentazione community  →  2. guidebook  →  3. sorgente  →  4. file locali
```

**I file locali sono l'ultimo passo.** Servono a vedere com'è *scritta* una
cosa già capita, non a scoprire cosa fa il dispositivo. Partire da lì è
reverse engineering senza modello, ed è la causa comune a quasi tutti gli
errori raccontati in questo documento — compresi i quattro modelli sbagliati
qui sotto. È regola 0 della skill, e il dettaglio con le prove sta in
`docs/FONTI.md`.

Si **cerca dall'alto, si decide dal basso**.

### E il 16 agosto l'ho violata di nuovo, quattro volte di fila

Vale la pena leggerlo prima di cominciare, perché è il modo in cui questo
progetto si fa male, e sapere la regola non basta a non ripeterlo.

Cercando come funziona la finestra verticale di una clip ho costruito quattro
modelli sbagliati uno dopo l'altro — `inKeyScrollOffset`, poi
`drumsScrollOffset`, poi una regola presa in prestito dal posto sbagliato, poi
`drumIndex` scambiato per la riga di schermo. Ogni volta ho corretto, scritto
un test, ed ero convinto di aver chiuso.

**Nessuno dei quattro è stato trovato da un test**, e non per mancanza di test:
erano tutti verdi, perché asserivano il modello che avevo in testa. *Un test
scritto da chi ha l'idea sbagliata conferma l'idea sbagliata.* È il limite
strutturale del TDD quando l'ignoto non sta nel codice ma nel comportamento di
una macchina esterna.

E soprattutto: tre volte su quattro avevo scritto «verificato sul dispositivo»
avendo **ascoltato** invece che guardato. Le song suonavano giuste davvero — la
riproduzione non dipende dallo scroll — ma la domanda era un'altra.

> **Verificare vuol dire guardare la cosa di cui si sta parlando.** Se
> l'affermazione riguarda ciò che si vede, ascoltare non conta.

Cosa ha funzionato, invece, tutte e tre le volte: la **coppia controllata** —
due file identici tranne per un passo, fatti salvare dal dispositivo. Ha chiuso
lo scroll di song view (§3.1), la modalità a scala e i kit (§6-sexies), e la
riga MIDI di un kit (§6-quinquies). È il metodo di questo progetto.

Ordine di lettura consigliato:

1. `docs/ARCHITETTURA.md` — il modello concettuale, dal manuale
2. `docs/FINDINGS.md` — lo schema derivato dai file, con prove e numeri
3. `docs/MUSICA.md` — lo schema neutro delle **undici caselle** e ciò che vale
   per ogni repertorio; le schede compilate stanno in `docs/repertori/` e se
   ne legge **una per volta**. È il documento su cui verte il prossimo lavoro
4. `docs/SYSEX.md` — il canale USB MIDI
5. `docs/FONTI.md` — l'ordine di ricerca e quello di autorità, che sono opposti
6. `README.md` — ora è **in inglese**: è la porta d'ingresso del repo pubblico,
   non più la guida pratica. Per quella valgono `SKILL.md` e questo documento

---

## 1. Obiettivo

Descrivere strutture musicali e ottenerne file validi per il Deluge, sul
modello di Producer Pal ma **asincrono**: si generano file lato PC, si portano
sul dispositivo, si caricano.

---

## 2. Cosa funziona, verificato sul dispositivo

| | |
|---|---|
| **Lettura e riscrittura** | round-trip byte-esatto, 33/33 file del corpus, sia in modalità chirurgica sia ricostruendo tutto dalle regole di formato |
| **Cambio di tempo** | `Mark100.XML` (88 → 100 BPM, 11 byte diversi su 269 779) caricata sul Deluge, mostra 100 |
| **Aggiunta di una nota** | `PercheN.XML`, nota su C4 al quarto ottavo della prima battuta, velocity 100 — vista sul dispositivo |
| **Formula del tempo** | `BPM = 110250 / (campioni_per_tick × 2^inputTickMagnitude)` |
| **Griglia** | `tick/movimento = 24 × 2^inputTickMagnitude`; è l'impostazione RESOLUTION della song |
| **Layout dei blob di note** | confermato dal convertitore ufficiale `contrib/midi2deluge` del repo firmware |
| **Lettura file via SysEx** | 269 kB scaricati in 59 s con hash verificato |
| **Clip duplicata** | `SCROLLB.XML` aperta sul Deluge: 4 righe, la copia in fondo. Vedi §3.1 |
| **Geometria di song view** | ogni clip è una riga; 8 righe a schermo; la clip `i` sta alla riga `i - yScrollSongView` |
| **Scrittura via SysEx** | `SONGS/USBGEN.XML` depositata via USB a Deluge acceso, 35 133 byte, hash verificato per rilettura |
| **Cosa tocca l'aggiunta di una clip** | misurato su una scala controllata di 4 salvataggi: `preview`, `yScrollSongView`, `yScrollArrangementView`, e nient'altro. `FINDINGS.md` §6-bis |
| **Le due regole di scroll** | song view conta le clip, arranger conta gli strumenti. La nostra formula dà gli stessi valori scritti dal dispositivo |
| **Percussioni** | `DRUMS1.XML`, generata sul PC indirizzando i drum **per nome** e depositata via USB: si vede e **suona** — kick 1·3, snare 2·4, charleston sulle crome |
| **Creare tracce da zero** | `NUOVATRK.XML` e `BASSO.XML`: strumento istanziato da un preset, clip, note, suono progettato. Un preset e il nodo strumento sono quasi lo stesso nodo |
| **Kit** | `KITPLUS.XML`: 17° drum preso da un altro file di kit, col suo campione. Si sente |
| **Automazioni per parametro** | tabella ID da `param.h`, tre ancoraggi verificati (24, 23, 47) su entrambe le metà dell'enum |
| **Automazioni** | rampa del cutoff LPF generata dalla libreria, `AUTOFULL.XML`: si vede sul dispositivo. Formato confermato sul **sorgente** (`auto_param.cpp`), non dedotto |
| **Scala dei parametri** | `display = (int32 + 2³¹) / (2³²/50)`, e griglia interna a 128 verificata muovendo una manopola a un valore noto |
| **Rimozione** | `RIMOSS001`/`RIMOSS101`, due song identiche tranne per una traccia tolta: sul Deluge la battuta 2 è vuota e **le battute 3 e 4 suonano ancora il proprio materiale**, cioè i `clipCode` rinumerati puntano giusto |
| **Trasposizione, synth** | `TRASF101` cromatica, `TRASF201` diatonica: `re fa la re` → `mi sol la# mi`, cioè tono, tono, semitono — intervalli diversi fra loro, che una trasposizione a intervallo fisso non produrrebbe |
| **Trasposizione, kit** | `TRASF401`: `transpose` sugli oscillatori dei drum, kick e rim **si sentono** più acuti di una quarta |
| **Double time** | `TRASF301`: stessa lunghezza di battuta, pattern due volte più fitto |
| **La finestra di clip view** | tre coppie controllate — `SCALA0/1`, `SCALB0/1`, `KITSCR0/1` — che danno **una geometria sola**, `riga = valore − yScroll` su otto righe, con l'unità che cambia: semitono, grado, posizione della riga. Vedi §6-sexies |
| **La riga MIDI di un kit** | `TRASF401MIDI`, fatta salvare dal dispositivo: è un `<midiOutput>` **fratello** dei `<sound>` dentro `<soundSources>`, altezza in `note`. Ha **smentito** l'ipotesi che il progetto aveva implementato. FINDINGS §6-septies |

| **Suoni progettati da zero** | `DUBPAL01`: kit **sintetizzato** (nessun campione), basso wobble, pad, sirena — tutti costruiti dal synth vuoto. Si sente. Vedi §6-septies |
| **Patch cable** | `lfo1 → lpfFrequency` (wobble), `lfo1 → pitch` (sirena), `envelope2 → oscAPitch` (pitch drop del kick): si sentono sul dispositivo |
| **Sintesi FM da un preset subtractive** | `structure.set_synth_mode(inst, 'fm')` crea i `<modulator1/2>` che il synth vuoto non ha e toglie il `type` dagli oscillatori, come fa il dispositivo |
| **Le posizioni fuori griglia sopravvivono al salvataggio** | `GROOVE1`, 31 note con scarti da −6 a +2 tick, aperta sul Deluge, **nessuna nota toccata**, risalvata dal dispositivo e riscaricata: **31 posizioni su 31 conservate**. Il Deluge **non riquantizza**. È meccanico, si legge nei byte. §6-terdecies |

La tabella qui sopra si è fermata all'11 agosto. Da allora sono arrivate le
fasi 6 e 7 — arranger, MIDI/CV, audio, e lo strato in linguaggio naturale —
tutte verificate sul dispositivo: vedi §6-ter e `docs/FINDINGS.md`.

**997 test** in `tests/test_all.py`. ⚠️ **Uno è rosso, e solo su questa
macchina:** `COPPIE_OSSERVATE` si ri-deriva dal corpus, e i quattro preset
scaricati il 29 agosto per il pezzo jazz lo hanno allargato — vedi
§6-quindecies, «Cosa NON rifare». `refs/` è ignorato da git, quindi **su un
clone la suite è verde**; senza quei quattro file sono **989**, tutti verdi.
I **16** aggiunti il 29 agosto sono quelli del nome dei drum e del rebuild
(§6-quindecies). I **38** aggiunti dal 26 al
29 agosto sono quelli dello stimatore per passo (§6-quaterdecies), e buona
parte gira su voci **sintetiche costruite apposta**, perché il caso da provare
— un gesto che sporge oltre mezzo passo — nel corpus è raro e non si può
ordinare a un batterista. Gli **84** aggiunti dal 18 al
25 agosto sono quelli del Groove MIDI e del groove template (§6-terdecies): una
parte legge il dataset e quindi salta senza `to-read/`, un'altra gira su **file
MIDI sintetici costruiti apposta**, così che gli invarianti veri — che l'origine
della griglia si tolga per intero, che il residuo torni zero quando lo swing è
noto, che `applica_groove()` non inventi su un passo senza appoggio — siano
verificabili anche da chi il corpus non ce l'ha.

⚠️ **Con il corpus sul disco sono 943 su 943 e zero saltati. In un clone —
niente `refs/` tranne `TEMPL.XML`, niente `corpus_versions/`, niente
`to-read/` — sono 460 su 460 con 82 SALTATI e ZERO fallimenti.** Questa cifra
è **misurata, non derivata**, il 25 agosto 2026: `git archive HEAD` in una
cartella vuota, che dà per costruzione esattamente i file versionati, e la
suite lanciata da lì con lo stesso `.venv`. I salti non sono un guasto:
`refs/` e `corpus_versions/` non sono più versionati (§9), e `salta()`
distingue "manca materiale che non è del repo" da "il codice è rotto".

⚠️ **E cade quello che questo documento diceva prima**, cioè che due test
*falliscono* senza corpus. **In un clone non fallisce niente**, e le ragioni
sono due, tutt'e due verificate rieseguendo:

| test dato per rotto | com'è davvero |
|---|---|
| `corpus di riferimento presente` | non scatta: `refs/synths/TEMPL.XML` **è pubblicato** (§9), quindi `refs/` non è mai vuota in un clone e il round-trip gira su quell'unico file |
| `COPPIE_OSSERVATE coincide con quella ri-derivata dal corpus` | **salta**, non fallisce: sopra di lui c'è già un `salta()` che scatta sotto le 50 coppie, ed era lì anche prima di questo ramo |

Quindi la riga vecchia era sbagliata su tutti e due i punti, e non per colpa
di questo ramo: era sbagliata anche su `main`. **L'unico modo di farne fallire
uno è togliere `refs/` per intero** — cosa che nessun clone fa — e allora è
uno solo: 428 su 429 con 84 saltati, e il rosso è `corpus di riferimento
presente`, che asserisce l'esistenza di una cartella. Misurato lo stesso
giorno, con lo stesso metodo, cancellando `refs/` dalla copia.

> **Euristica guadagnata sul campo, quattro volte.** Se un contenuto scritto
> correttamente non compare sul dispositivo, **cercare lo stato di vista prima
> di sospettare del contenuto.** È successo con `yScrollSongView` (clip una
> riga sotto lo schermo), con lo stato della vista automazione, con
> `beingEdited` (si apriva un'altra clip) e con `inKeyMode` (note fuori scala
> senza una riga su cui esistere). Ogni volta il dato era giusto.
>
> ⚠ **Attenzione al quarto caso: la mia diagnosi era SBAGLIATA.** Avevo
> concluso che le note fuori scala non hanno una riga e non suonano. Falso —
> il dispositivo adatta la scala, e `Progsong.XML` ha 315 note fuori scala.
> Il difetto reale era che una clip creata da un modello eredita `yScroll` e
> `inKeyScrollOffset` dal modello: usare `fit_clip_scroll_to_notes()`.
> Il racconto dell'errore, con i due sbagli di metodo che l'hanno prodotto,
> è in FINDINGS.md — vale più della conclusione.

---

## 3. I due blocchi storici, entrambi chiusi il 12 agosto 2026

### 3.1 La clip duplicata non compariva — RISOLTO

**Non era un problema di caricamento. La clip era sotto il bordo dello
schermo.**

In song view ogni clip è una riga e la finestra visibile parte da
`yScrollSongView`, un attributo del nodo `<song>`. La clip di indice `i` sta
alla riga `i - yScrollSongView`, e le righe sono 8, numerate 0–7.
`Perche.XML` ha 3 clip e `yScrollSongView="-5"`: occupano esattamente le righe
5, 6, 7. Accodandone una quarta senza toccare lo scroll, quella finisce alla
riga 8, che non esiste.

`duplicate_clip()` non toccava lo scroll: la stringa `yScroll` non compariva da
nessuna parte nella libreria.

Le tre prove, nell'ordine che vale:

1. **Manuale**, cap. 7 Song View: «Individual clips compressed to one row each
   in song view. The rows can be navigated up and down *beyond the 8 physically
   displayed*.» Di nuovo una cosa spiegata in una frase.
2. **File scritti dal dispositivo**: clonando una clip, il Deluge ha spostato
   lui stesso `yScrollSongView` da `-5` a `-4`, per tenere la riga nuova in
   fondo allo schermo.
3. **Dispositivo**: due file diversi per **un solo byte** (offset 1084),
   `SCROLLA` con `-5` e `SCROLLB` con `-4`. A mostra 3 righe con la quarta
   nascosta, B ne mostra 4. Protocollo e esito in `docs/TEST_yscroll.md`.

Correzione: `scroll_song_view_to()` in `tools/delugexml/song.py`, chiamata da
`duplicate_clip()` dopo l'append. Alza lo scroll solo quando serve — una vista
che già mostra la riga non viene spostata, perché è lo stato che l'utente ha
lasciato. Coperta da `test_scroll_song_view`.

Perché è costata due sessioni: **la differenza è stata cercata dentro la clip,
e non c'era.** Era nel nodo `<song>`. Confrontare i file ha continuato a dire
"identici" perché lo erano davvero, nella parte guardata.

### 3.2 La scrittura via SysEx — RISOLTA dal firmware

Era **PR #4633, "Fix USB MIDI receive packet loss"**, come ipotizzato.
Sulla nightly `1.3.0-beta build 2d7cdf8` (12 agosto 2026) la scrittura
funziona, senza toccare una riga del client:

| | prima (build 0856ff9) | ora (build 2d7cdf8) |
|---|---|---|
| blocco 64, file da 256 B | 22 byte su 64 | 256/256, hash identico |
| `Perche.XML`, blocco 768 | si ferma a **1000 byte esatti** | 28 715/28 715, hash identico |
| perdita | ~75% dei blocchi | **0 timeout, 0 blocchi parziali, 0 riaperture** |
| velocità | 4,6 kB/s in lettura | 62,6 kB/s in scrittura |

Depositare una song generata in `SONGS/` via USB, con il Deluge acceso e la SD
dentro, ora funziona ed è verificato per rilettura con hash.

---

## 4. La direzione: le song. I Pattern sono rimandati

**Decisione del 12 agosto 2026, presa dopo aver riesaminato la questione.**
La direzione è la **manipolazione delle song**. I file Pattern restano
un'opzione per uno stadio molto più avanzato del progetto.

Le sessioni precedenti raccomandavano il contrario. Quella raccomandazione
poggiava su quattro argomenti, e oggi non reggono:

| argomento di allora | stato |
|---|---|
| «aggira completamente il problema 3.1» | **caduto**: il 3.1 è risolto (§3.1) |
| «non tocca file esistenti, rischio nullo» | il rischio non si è mai materializzato: `put` non sovrascrive, roundtrip byte-esatto 33/33 |
| «implementazione di riferimento ufficiale» | è `contrib/midi2deluge`, un convertitore MIDI, non un file scritto dal dispositivo |
| «è esattamente il caso d'uso» | vero, ma vale solo per le note |

Le ragioni della scelta:

- **serve il massimo controllo.** Un Pattern porta solo le note di *una
  schermata* — niente tempo, sezioni, strumenti, lunghezze, sound design. La
  song le porta tutte.
- **salvare e ricaricare una song sul Deluge è veloce**, quindi il vantaggio
  vero dei Pattern (incollare senza ricaricare, mantenendo la sessione viva)
  vale poco in questo flusso di lavoro.
- **la base di prove è debole.** Nel manuale ufficiale i Pattern non esistono:
  tutte le occorrenze di "pattern" nel guidebook sono nel senso generico di
  sequenza. È una feature del solo firmware community, documentata solo dalla
  doc community — la stessa fonte che sui byte di comando SysEx è **sbagliata**.
  Nessun esemplare scritto dal dispositivo è mai stato visto.

Se un giorno si riprendono, il primo passo resta quello: farne salvare uno dal
dispositivo e confrontarlo con lo schema in `docs/ARCHITETTURA.md` §10 prima di
scrivere una riga di codice. Le cartelle `PATTERNS/` sulla SD non esistono
ancora, quindi non le ha mai usate nessuno.

---

## 5. Il progetto

```
D:\DelugePal\
  README.md              uso pratico
  HANDOFF.md             questo file
  docs\
    ARCHITETTURA.md      modello concettuale, dal manuale e dalla doc community
    FINDINGS.md          schema derivato dai file, con numeri e prove
    MUSICA.md            schema neutro delle undici caselle, il comune, l'indice
    repertori\           una scheda per repertorio compilato: reggae-dub.md, jazz.md
    SYSEX.md             canale USB MIDI: cosa funziona e cosa no
    FONTI.md             cosa è stato letto, in ordine di autorità
    PROSSIMI_PASSI.md    piano operativo delle sette fasi, chiuso
    PIANO_rimozione.md   il piano della rimozione, con il censimento misurato
    PIANO_trasformazioni.md  il piano delle trasformazioni. §3.0-bis e' tenuta
                         SBAGLIATA di proposito: l'errore vale piu' della
                         conclusione, e la correzione e' in FINDINGS §6-septies
    TEST_yscroll.md      l'esperimento che ha chiuso §3.1, con il metodo
    SCHEMA_song_c1.3.0.md, SCHEMA_kit_c1.3.0.md   inventario generato
    HANDOFF_originale.md l'handoff di partenza, per storia
  tools\
    delugexml\           la libreria (parser, writer, notes, song)
      sound.py           parametri E patch cable (`set_patch_cable`)
      structure.py       forme d'onda, modi di sintesi, modulatori FM
      midi.py            lettore Standard MIDI File, SENZA dipendenze
      wjazz.py           lettore della Weimar Jazz Database (solo sqlite3)
      groove.py          lettore del Groove MIDI: elenco, scala di velocity,
                         groove template. Non tocca mai un Document
      musica.py          lo strato in lingua musicale
    dsong.py             CLI: info, notes, tempo, note-add, clip-dup, row-add
    misura_groove.py     le misure delle caselle 4, 6 e 9 del jazz: si esegue,
                         si legge, i numeri si scrivono a mano nella scheda
    genera_groove.py     la coppia GROOVE0/GROOVE1 del cancello. NON e' un
                         pulsante da premere: rigenerarla sovrascriverebbe
                         l'unico esemplare ascoltato (§6-terdecies)
    genera_swing.py      la coppia SWINGA/SWINGB dell'astrazione dello swing
    dsysex.py            client SysEx: ping, dir, get, put — tutto funzionante
    …                    una ventina di strumenti di analisi, vedi README
  to-read\               112 000 file, 4,8 GB di libri e librerie MIDI raccolti
                         dall'utente. NON versionato: e' opera di terzi, e
                         percorrerlo faceva andare `git add` in timeout
  refs\                  59 file c1.3.0 — corpus di riferimento. **NON PIU'
    VERSIONATO** (§9): sta sul disco, git lo ignora. L'unico file pubblicato
    e' `synths/TEMPL.XML`, il synth vuoto del firmware.
    songs\ 43, kits\ 3, synths\ 2, settings\ 3, sd_salvati\ 8. Tutti scritti
    dal dispositivo.
    Dentro ci sono QUATTRO gruppi controllati, ognuno una misura: non
    separarli e non "ripulirli", sono le prove su cui poggiano i documenti.
      TEMPL0 -> TEMPL2 -> TEMPL3 -> TEMPL4   cosa tocca l'aggiunta di una
                         clip (FINDINGS §6-bis)
      SCALA0/1, SCALB0/1 la finestra in modalita' a scala: yScroll conta i
                         GRADI (FINDINGS §6-octies)
      KITSCR0/1          la finestra di una clip di kit: yScroll conta la
                         POSIZIONE della riga (FINDINGS §6-octies)
      TRASF401MIDI       l'unico esemplare di riga MIDI in un kit, che ha
                         smentito un'ipotesi (FINDINGS §6-septies). E' anche
                         l'unico file che non si ricostruisce byte-esatto
                         dalle regole di formato — vedi FINDINGS §2.2-bis,
                         e' noto e nominato nel test
  corpus_versions\       103 song di 16 versioni firmware (3.0.0 → 4.1.4-alpha,
                         c1.1.0, c1.2.0), divise per versione. FUORI da refs\
                         di proposito: la tabella di formato si apprende solo
                         da c1.3.0 e queste la inquinerebbero.
                         Anch'esse NON piu' versionate (§9)
  out\                   tabella di formato, inventari, file generati. L'unico
                         versionato e' `format_table.json`: e' un artefatto
                         DERIVATO e non contiene musica
  tests\test_all.py      997 test, 989 senza i quattro preset del
                         29 agosto (il 460/460 + 82 salti in un
                         clone e' del 25 agosto, non rimisurato)
  .venv\                 mido + python-rtmidi, per il SysEx
```

Python 3.13 di sistema per tutto tranne il SysEx, che usa `.venv`.

---

## 6. Il vincolo che ha determinato l'architettura

**Il firmware non scrive XML valido.** 255 song su 378 vengono rifiutate da un
parser conforme:

- `&` mai escapato (confermato nel sorgente: `writeAttribute` non escapa nulla)
- blocchi di attributi duplicati su `<audioClip>`
- formato legacy con due elementi radice

Quindi niente `xml.etree`: c'è un parser tollerante su misura in
`tools/delugexml/parser.py`, che conserva gli offset nel sorgente. Grazie a
questo un nodo non modificato viene riemesso **ricopiando i byte originali**:
cambiare il tempo di una song da 8577 righe tocca esattamente 2 righe.

La tabella di formato è **appresa dal corpus**, non derivata per regole — e
questa non è una scorciatoia: il sorgente mostra che la formattazione è un
booleano `onNewLine` deciso a ogni singola chiamata, quindi non esiste nessuna
regola da scoprire.

---

## 6-ter. Lo strato musicale — fase 7, chiusa il 15 agosto

`tools/delugexml/musica.py` traduce fra lingua musicale e chiamate alla
libreria. **Il modello non scrive mai XML**: chiama queste funzioni, che a loro
volta chiamano codice coperto da test.

| per | funzione |
|---|---|
| leggere cosa c'è, in termini musicali | `racconta(doc)`, `racconta_clip(doc, clip)` |
| altezze | `altezza('re2')`, `nome_altezza(38)` — italiano e inglese |
| batteria | `passi('x...x...x...x...')` — un carattere per sedicesimo, come la griglia |
| melodie | `melodia('re2 fa2 la2', durata='1/8', articolazione='staccato')` |
| accordi | `accordi('re3 fa3 la3 \| sib3 re4 fa4')` — le note insieme, progressione in una riga |
| suono e mix | `applica_verbo(doc, nodo, 'piu scuro')`, che riferisce cosa ha mosso |
| **il cancello** | `verifica(doc)` **blocca**, `avvertenze(doc)` **informa** |
| dove salvare | `destinazione(nome, versione, cartella)` |

**`verifica()` è la regola che non si salta**: nessun file sale sul dispositivo
se non è vuota. Ferma il primo dei due file rifiutati dal Deluge — la clip di
kit che si dichiarava synth (FINDINGS §6-quater) — e ha fermato la prima song
generata dalla prova d'accettazione.

**Non ferma il secondo.** Il crash E365 (FINDINGS §6-quinquies, il `<params>`
di una clip audio troncato da 31 a 11 attributi con valori inventati) resta
invisibile a `verifica()` — misurato: su quel file restituisce `[]`, e
`avvertenze()` pure. Quel caso lo ferma un'altra cosa: la regola «mai
trascrivere a mano, le costanti si generano da codice» (regola 2 della skill)
più `test_audio_costanti`, che confronta la costante incorporata col nodo vero
attributo per attributo. Non si può allargare il cancello per coprirlo anche
lì: 109 delle 194 clip audio scritte dal dispositivo hanno esattamente 11
attributi nel loro `<params>` (11×109, 12×13, 14×1, 15×65, 16×2, 31×3, 32×1)
— un controllo di completezza accuserebbe 190 file su 194 sani, la stessa
trappola dei falsi positivi già costata due volte in questo progetto.

**`avvertenze()` è il livello che informa senza bloccare**: conflitti di
sezione, note oltre la fine della clip, note scritte fuori dalla finestra di
scroll della clip (`song.notes_hidden_by_scroll()`, il gemello di
`yScrollSongView` a livello di clip). Roba che il dispositivo carica ed
esegue male o non esegue — la famiglia di difetti che in questo progetto è
costata più di tutte.

### Cosa ha trovato la prova d'accettazione

Generare una song *come la genererebbe il Pal* ha scovato tre difetti che 424
test non vedevano, perché tutti partivano da materiale già esistente:

- **`add_track` su un kit creava una clip senza righe.** Nel corpus **393 clip
  di kit su 395** hanno una riga per *ogni* drum, suonato o no, con indici
  contigui da 0. Chi aggiungeva note otteneva indici sparsi, e il cancello
  rifiutava. Corretto; aggiunta `song.drum_row()` per scrivere su un drum per
  nome.
- **Non esisteva un modo di scrivere un accordo.** `melodia()` mette una nota
  per passo: `re3 fa3 la3` usciva in fila invece che insieme. Ora c'è
  `accordi()`.
- **Nessuno avvisava se una nota cadeva oltre la fine della clip.** Il Deluge
  carica e non la suona. Ora è un'avvertenza — e la soglia è stata *misurata*:
  un controllo ingenuo accusava 254 note in 22 file sani, che erano poliritmi
  (righe più lunghe della clip).

---

## 6-quater. Togliere — chiusa il 15 agosto, verificata sul dispositivo

Il ciclo è «l'utente ascolta e dice cosa cambiare», e **metà di quello che una
persona dice è sottrattivo**. Fino al 15 agosto *«rifai il basso»* funzionava e
*«togli il basso»* no: in tutta la libreria c'erano `kit.remove_drum` e
`Node.remove`, e nient'altro.

Due verbi in `musica.py`, entrambi con un rapporto di ritorno come
`applica_verbo`. Sotto stanno le primitive, testate una per una.

| per | funzione |
|---|---|
| togliere | `togli(doc, bersaglio, quando=None)` |
| scrivere note | `scrivi(doc, clip, note, dove=None)` |

`togli` riconosce il bersaglio **per identità** — appartenenza alla lista degli
strumenti o delle clip — non per tag: nel corpus convivono `<midi>` e
`<midiChannel>`, e una tabella di tag sarebbe una cosa in più da sbagliare.

    strumento                 le sue clip, poi lui
    strumento + quando=(a,b)  solo le istanze d'arranger in quel tratto
    clip                      la clip, e i clipCode che la seguivano
    noteRow di kit            SVUOTATA: una riga per drum deve esserci
    noteRow di synth          tolta

`quando` è la differenza fra *«togli il basso»* e *«leva il basso nella seconda
metà»*. Toglie le istanze **contenute** nel tratto, non quelle che lo
attraversano: una a cavallo porta anche materiale fuori, e toglierla farebbe
tacere musica che nessuno ha chiesto di togliere. Restano, e il rapporto le
dichiara.

`scrivi` chiude la vecchia lacuna 3. Non serve dichiarare se la clip è un kit o
un synth, perché **la forma delle note lo dice già**: `melodia()` e `accordi()`
tornano `altezza -> note`, `passi()` una lista sola. Su synth chiama sempre
`fit_clip_scroll_to_notes()` in coda. Le tre righe che `SKILL.md` insegnava
separate — e le tre occasioni di prendere quella sbagliata — sono una sola.

**Il numero che conta:** i riferimenti a una clip nel corpus sono **due**,
`clipCode` e `yScrollSongView`, e nessuno dei due la nomina — entrambi la
contano. Il censimento e le altre misure sono in `docs/FINDINGS.md` §6-sexies.

**Un difetto trovato progettando, non da un test:** `_keep_row_visible()` alza
soltanto lo scroll, quindi la rimozione poteva lasciare la vista *sopra* il
contenuto — il §3.1 in specchio, quinta volta della stessa famiglia. Reale: 11
song su 36 hanno `yScrollSongView` positivo, `Progsong.XML` vale 27 con 42
clip. Corretto da `_keep_view_within()`, che scende solo quel tanto e non
ri-ancora in fondo.

---

## 6-quinquies. Trasformare — chiusa il 16 agosto, verificata sul dispositivo

*«Alza il basso di un'ottava»* è una richiesta ordinaria quanto *«più scuro»*,
e fino al 16 agosto voleva una funzione che non c'era.

Le cinque parole della lacuna — trasponi, raddoppia, dimezza, sposta, più
veloce — non erano cinque operazioni: tre di esse ne volevano dire due ciascuna.
Sciolte in sei nomi non ambigui:

| per | funzione |
|---|---|
| trasporre | `trasponi(doc, bersaglio, semitoni=…)` oppure `gradi=…` |
| spostare nel tempo | `sposta(doc, clip, tick=…)` oppure `battute=…` |
| allungare ripetendo | `repeat(doc, clip, volte)` |
| cambiare il rate | `stretch(doc, clip, fattore)` |
| l'articolazione al doppio | `double_time(doc, clip)` — la battuta **resta** |
| l'articolazione a metà | `half_time(doc, clip)` — la clip **raddoppia** |

L'asimmetria fra gli ultimi due è voluta: in metà tempo un pattern di una
battuta ne occupa due davvero, mentre in doppio tempo lo si suona due volte per
riempire la battuta.

**Trasporre non è la stessa operazione su un synth e su un kit.** Su un synth
le righe *sono* le altezze e si cambia `y`. Su un kit si intona il **suono** —
`transpose` sugli oscillatori del drum, confermato dal manuale e verificato sul
dispositivo — quindi cambia lo strumento e con lui *tutte* le clip di quel kit.
I `drumIndex` non si toccano mai. Dettagli e numeri in `docs/FINDINGS.md`
§6-septies.

**Il modo diatonico conserva lo scarto cromatico dal grado**, invece di
schiacciare in scala: una nota un semitono sopra il terzo grado resta un
semitono sopra il *nuovo* terzo grado. `snap_to_scale()` qui sarebbe sbagliata,
e distruggerebbe le 315 note fuori scala di `Progsong.XML` che FINDINGS §6 dice
espressamente di rispettare.

**E non è biiettivo**, a differenza del cromatico: in re minore mib2 e mi2
salgono entrambi su fa2. `song.retune_rows()` fonde le righe che collidono e lo
dichiara.

**La riga MIDI di un kit, e un'ipotesi demolita.** Il progetto aveva
implementato una supposizione — un `<sound>` col suo `<midiOutput>` figlio
attivo, altezza in `noteForDrum` — ed era sbagliata su entrambi i punti. La
forma vera è un `<midiOutput>` **fratello** dei `<sound>` dentro
`<soundSources>`, con l'altezza in **`note`**. È emersa solo facendo salvare al
dispositivo un kit con una riga MIDI (`refs/songs/TRASF401MIDI.XML`).

La lezione di metodo vale più della correzione: il ragionamento di allora era
«`noteForDrum` è un attributo *osservato*, quindi non sto inventando una
struttura». Vero, e insufficiente — **un nome osservato nel posto sbagliato è
comunque il posto sbagliato.** «Non sto inventando» non è «ho visto».

---

## 6-sexies. La finestra di clip view — chiusa il 16 agosto

Era l'ultima lacuna, e la più piccola sulla carta: «l'avvertenza sulle note
invisibili non copre le clip in modalità a scala». Ne è uscita **una geometria
sola per tutto il dispositivo**:

    riga sullo schermo = valore − yScroll        otto righe, 0-7

con l'unità che cambia col tipo di clip — il **semitono** in cromatico, il
**grado** in scala, la **posizione della riga** in un kit. Tre coppie
controllate, una per unità: `SCALA0/1`, `SCALB0/1`, `KITSCR0/1`, tutte in
`refs/songs/`. La conversione vive in `song.clip_rows_with_notes()`, e sia il
`fit` sia l'avvertenza ci passano — non c'è più nessun ramo speciale.

`fit_clip_scroll_to_notes()` **ancora** la riga più bassa alla prima riga dello
schermo, sempre. Non «lascia stare se qualcosa si vede»: quella è la regola di
song view, dove si conserva la vista dell'utente, e presa in prestito qui
lasciava la nota più alta fuori dallo schermo.

⚠️ **Quattro modelli sbagliati di fila, e nessun test li ha visti**, perché
erano tutti verdi asserendo il modello sbagliato. Sono emersi solo guardando lo
schermo del Deluge, dopo che erano stati dichiarati «verificati sul
dispositivo» avendo **ascoltato** invece che guardato — la riproduzione non
dipende dallo scroll, quindi suonavano giusti. Il racconto per esteso è in
`docs/FINDINGS.md` §6-octies e vale più della conclusione.

---

## 6-septies. Il primo pezzo vero — 16 agosto, e cosa ha insegnato

Il consiglio dell'handoff precedente era «usarlo, e vedere cosa manca
davvero». Ha funzionato: **un solo pezzo ha trovato più buchi di una revisione
a tavolino**, e li ha trovati in due strati diversi.

Il brief: dub elettronico lento, strumenti costruiti da zero, kit
**sintetizzato** e non a campioni, basso wobble, pad, sirena, uso creativo di
delay e filtri con automazioni.

### Strato 1: cosa mancava alla libreria

Tre lacune, tutte bloccanti per quel brief, tutte chiuse:

| mancava | perché bloccava | ora |
|---|---|---|
| **i patch cable** | senza, niente wobble (`lfo1 → lpfFrequency`) e niente sirena (`lfo1 → pitch`): sono patch cable e nient'altro | `sound.set_patch_cable / patch_cables / remove_patch_cable` |
| **i modulatori FM** | il synth vuoto è subtractive e non ha `<modulator1/2>`, presenti in **80 suoni FM su 80** del corpus | `structure.set_synth_mode(inst, 'fm')` li crea |
| **`defaultParams` fra i contenitori** | `sound.container()` su un drum tornava `None`: impossibile progettare il suono di una percussione | aggiunto in fondo a `CONTENITORI` |

Più una quarta trovata dopo, dall'ascolto: **`passi()` aveva due soli livelli
di velocity**, e con due livelli un colpo fantasma è inesprimibile. Ora `o` è
il fantasma (42 su 127).

⚠️ **Trappola del modulo `sound.py`**: definisce di proposito una funzione
`set()` che **oscura il builtin**. Usare `set()` lì dentro dà un `TypeError`
che sembra venire da tutt'altra parte. Deduplicare con un dict.

### Strato 2: cosa mancava a me

Il giudizio dell'utente sul primo tentativo: *«molto elementare e non
assomiglia per niente a un pezzo dub»*, e poi *«anche il ritmo di batteria è
penoso»*. Aveva ragione, e la causa era una sola: **avevo fatto una ricerca web
sola**, e ne erano uscite le etichette invece del mestiere.

Gli errori concreti, tutti dallo stesso buco:

| errore | cos'era giusto |
|---|---|
| charleston sui levare, **skank assente** | il charleston fa una timeline regolare; il levare è dello *skank*, che è **armonia** |
| niente *bubble* d'organo | riempie i sedicesimi attorno al levare |
| basso di 4 battute che si sviluppa | frase di **1-2 battute ripetuta**, centrata sul 3, con la quinta **sotto** la tonica |
| 4 battute di batteria identiche | **turnaround** sull'ultima di ogni 4 o 8 |
| `set_swing(50)`, dritto | il one drop è **swingato e laid-back** |
| pad a note lunghe come parte armonica | in reggae l'armonia è **ritmica**, staccata, in levare |

Tutto questo è ora nella scheda `docs/repertori/reggae-dub.md`, con le
griglie a 16 passi, i numeri delle velocity e le fonti.

### E una correzione di sound design che vale in generale

La sirena di `DUBPAL01` *«bucava le orecchie»* **pur rispettando** la soglia
che avevo scritto io (risonanza sotto 24). La soglia era sbagliata come
concetto: le ladder del Deluge **autooscillano**, e quanto sia "alto" dipende
dal registro e da cosa c'è intorno — lì il delay feedback che saliva a 33 e il
riverbero a 34 **ripetevano e accumulavano** il picco risonante.

Il rimedio, detto dall'utente: **se vuoi una risonanza estrema, la paghi
abbassando il volume della patch.** La risonanza gonfia una banda stretta, e
quello che esplode è il livello percepito, non il timbro.

> Nota di metodo, ripetuta due volte in un giorno: `DUBPAL02` è stata corretta
> partendo dalla song **riscaricata dal dispositivo**, non dalla copia locale —
> e infatti portava il volume a 29 invece dei 17 che avevo messo io. La regola 1
> non è formale: senza, quella correzione sarebbe stata cancellata.

---

## 6-octies. Le sigle di accordo — 17 agosto 2026

Primo passo del perimetro nuovo, e non è un lettore di file: è **il posto dove
i lettori atterreranno**. `wjazzd.db`, MusicXML e kern producono tutti e tre
armonia; costruirli prima avrebbe voluto dire tre rappresentazioni diverse da
riconciliare dopo.

**La lacuna era un concetto, non un formato.** `MU.accordi()` vuole le altezze
già scelte (`'do3 mi3 sol3'`): in tutta la libreria non esisteva la nozione di
*simbolo*. Per il reggae non si notava — lì l'armonia sono due accordi e il
mestiere sta nel ritmo. Per il jazz è l'opposto.

| per | funzione |
|---|---|
| una progressione per sigla | `MU.armonia('Dm7 \| G7alt \| Cmaj7', voicing=…, registro=…)` |
| le altezze di un accordo solo | `MU.voci('Cmaj7', voicing='drop2', registro='do4')` |
| sciogliere una sigla senza suonarla | `MU.sigla('C6/9/E')` |
| **raccontare cosa ha deciso** | `MU.racconta_armonia(…)` |

`armonia()` ha **la stessa forma di ritorno di `accordi()`** — `altezza →
note` — quindi entra in `MU.scrivi()` senza che nulla a valle sappia da dove
viene. Era il vincolo di progetto principale: atterrare nella macchina che
esiste, non chiederne una nuova.

**Da dove vengono i numeri, e perché conta.** Le sigle e le ambiguità da
`assets/chord-symbol-ambiguity-and-parsing.md`, i voicing da
`assets/jazz-voicings.md` — cioè dalla skill, non da me. E **i test portano i
valori attesi di quei documenti**: il drop 2 di domaj7 (`sol-do-mi-si`), il
senza-fondamentale di re-7 (`fa-la-do-mi`) e di domaj7 (`mi-sol-si-re`), il
`C7#11` senza la quinta (`mi-sib-re-fa#`). È la coppia controllata applicata a
un dominio non misurabile sul dispositivo: **il valore atteso deve venire da
fuori**, o il test conferma solo il modello che avevo in testa — che è
esattamente come sono nati i quattro modelli sbagliati del 16 agosto.

Tre cose che il progetto ha già pagato altrove, e qui sono state prevenute:

- **il maiuscolo conta**: `CM7` è maj7, `Cm7` è minore. La coda si normalizza
  guardando il caso *prima* di abbassarlo — è lo stesso difetto muto di
  `'Ab'` → A# in `set_scale`, dove un semitono sbagliato non dava errore.
- **la fondamentale riusa `altezza()`**, quindi italiano e inglese non possono
  divergere. Un secondo parser di altezze è una seconda occasione di sbagliare.
- **una sigla sconosciuta viene rifiutata** e l'errore elenca quelle che
  esistono, invece di indovinare note che nessuno ha chiesto.

⚠️ **Il limite, dichiarato e non nascosto: non c'è condotta delle parti.** Ogni
accordo è costruito per conto suo. Il documento mostra che nel ii-V-I i
voicing senza fondamentale si **alternano** fra due forme (A e B) proprio per
muovere una voce sola per cambio: le note qui sono giuste, il *collegamento*
no. `racconta_armonia()` lo dichiara a ogni chiamata.

**E un difetto trovato provando a mano dopo che i test erano verdi**, che vale
come promemoria: `C6/9/E` ha due slash con due significati diversi — l'ultimo
è il basso, quello dentro `6/9` è parte della sigla. I dieci test erano tutti
verdi e non lo vedevano. È la quinta volta in questo progetto che il difetto
sta in un caso che nessun test aveva pensato di scrivere.

---

## 6-nonies. Il lettore della Weimar Jazz Database — 17 agosto 2026

Secondo passo del perimetro nuovo, e il primo lettore vero.
`tools/delugexml/wjazz.py`, solo `sqlite3` della stdlib — nessuna dipendenza,
come `midi.py` che si era scritto il lettore di SMF invece di tirarsi dentro
`mido`.

| per | funzione |
|---|---|
| cercare | `WJ.elenco(db, style=…, rhythmfeel=…, instrument=…)`, `WJ.valori(db, campo)` |
| vedere | `WJ.racconta(db, melid)` |
| le note | `WJ.melodia(db, melid)` → `(altezza → note, Conversione)` |
| la griglia | `WJ.armonia(db, melid)` → `Accordo(tick, bar, beat, testo, sigla)` |
| il dialetto | `WJ.sigla_weimar(testo)` |

`melodia()` e `armonia()` hanno le forme che il progetto usa già, e
`armonia()` restituisce `MU.Sigla` **sciolte** — cioè atterrano in
`MU.armonia()` e in `MU.scrivi()`. Era il motivo per cui §6-octies veniva
prima.

### Il dialetto, e la misura che ha guidato il progetto

Il 22% delle 30 548 occorrenze di accordo **non era leggibile** da
`MU.sigla()`, e i fallimenti erano tutti sistematici: `j7` per maj7,
l'alterazione **dopo** il grado (`79b` = 7♭9), `o` per il diminuito, `sus7`
per 7sus4, `NC` per nessun accordo.

⚠️ **La verifica che contava non era quel 22%, ma l'altro 78%.** Un simbolo
che si legge non è un simbolo che si legge *giusto*, e un falso positivo lì
sarebbe stato muto. Misurato una per una: le code comuni ai due dialetti —
`7`, `-7`, `-`, `6`, `-6`, `sus`, `m7b5`, `69`, `+`, `7alt` — vogliono dire
la stessa cosa. **È quella misura che ha deciso l'architettura**:
`sigla_weimar()` prova prima la lettura canonica e scende alla grammatica di
Weimar solo quando fallisce, invece di riscrivere una grammatica che esiste.

Copertura finale: **419 simboli distinti su 419, zero fallimenti**; le 401
caselle `NC` tornano `None`.

**Il dialetto sta in `wjazz.py`, non in `MU.SIGLE`.** `SIGLE` è la notazione
da lead sheet, comune a tutte le fonti; le abitudini di un database solo,
messe lì, la sporcherebbero per sempre. Vale come regola per i lettori che
verranno.

### Cosa è annotato e cosa no

La tabella `melody` porta **la posizione metrica** (`bar/beat/tatum/division`)
**accanto** al tempo reale (`onset` in secondi). Quindi la metrica non va
dedotta: è scritta. E **la differenza fra le due è la micro-tempistica**, che
è il motivo per cui questo database vale più di una raccolta di MIDI.

**Lo swing misurato è arrivato subito dopo**, il 17 agosto: `WJ.swing()`, e i
primi numeri `[MIS]` del progetto. Vedi §6-decies.

⚠️ `division` vale 5 o 10 per 7242 note su 200 809 (il 3,6%) e 96 non si
divide per 5: quelle si arrotondano, e `Conversione` lo dichiara.

### Un difetto trovato dai test, che vale come promemoria

La prima versione estraeva la fondamentale con `MU.sigla()`. Ma `MU.sigla()`
è un parser di **accordi interi**: su `C7` restituiva la fondamentale *e si
mangiava la settima*, lasciando una triade. Quindici test rossi in una volta.

È la stessa famiglia di «un nome osservato nel posto sbagliato è comunque il
posto sbagliato»: la funzione era quella giusta per il vocabolario delle
altezze e quella sbagliata per estrarre un prefisso.

**Il materiale che resta in `to-read/MIDI/`**, ora che il primo è aperto:
`groove-v1.0.0-midionly/` — non uno zip da decomprimere, è già una cartella
decompressa; il suo `groove/info.csv` etichetta ogni file con stile e BPM, e
**quante esecuzioni porti a ciascun repertorio sta nella casella 6 della sua
scheda** — il jazz in `docs/repertori/jazz.md`, il reggae in
`docs/repertori/reggae-dub.md` — perché è lì che quel conteggio serve a
decidere se il numero è `[MIS]` o `[WEB]`, e per i due repertori ha deciso in
modo opposto (§6-terdecies). Dal 18 agosto quel dataset si legge con
`groove.py` e non a mano. Poi restano `POP909`, `maestro`,
`The_Magic_of_MIDI`, le librerie per genere e `(aq) Dub Beat Builder`.

---

## 6-decies. Lo swing misurato — 17 agosto 2026

`WJ.swing(db, style=…, rhythmfeel=…, tempo_min=…, tempo_max=…)`. Su **333
assoli e 27 943 coppie di crome**: levare al **61,7%** del movimento, cioè
**BUR 1,61**. Tabelle per stile, feel e tempo in `docs/repertori/jazz.md`,
«Lo swing del jazz, MISURATO», nella casella 4 — sono i primi numeri `[MIS]`
del progetto, contro i `[WEB]` di tutto il resto della pagina.

Il risultato in una riga: **il jazz non swinga in terzine.** Sta fra il dritto
e la terzina, HARDBOP e BEBOP in cima (1,80 e 1,75), FUSION in fondo (1,26), e
lo swing **cala al salire del tempo** — 1,89 fra 120 e 180 BPM, 1,35 sopra i
240.

### L'errore, che vale più del risultato

⚠️ **Tre tentativi hanno dato 1,10, 1,19 e 1,10 e sembravano confermarsi a
vicenda. Erano lo stesso errore tre volte.**

La posizione **annotata** (`tatum`/`division`) **contiene già lo swing**: i
trascrittori scrivono una coppia di crome swingate come *tatum 1 e 3 di
division 3*. Quindi selezionare le crome con `division == 2` — che sembra la
cosa ovvia — seleziona le sole coppie giudicate **dritte**, e la misura torna
1,0 per costruzione. Non un errore di calcolo: di **selezione**.

Due cose l'hanno smascherato, e nessuna delle due era un test:

1. **Un controllo esterno.** La letteratura dice che lo swing cala col tempo e
   che i generi a crome dritte stanno sotto. Nessuna delle due previsioni
   compariva. *Una misura che non riproduce una previsione nota è sbagliata
   anche quando è ripetibile* — e ripetibile lo era, tre volte.
2. **Guardare le righe grezze** di un assolo lento, e vedere `tatum=1/3`.

È la stessa famiglia dei quattro modelli sbagliati del 16 agosto: test verdi
che asserivano il modello che avevo in testa. Qui però i test non c'entrano
nemmeno — il codice faceva esattamente quel che dicevo io, ed era la domanda
a essere posta male.

### Cosa NON è verificato

- **Il valore assoluto non è riconciliato con la letteratura.** «Playing It
  Straight» riporta ~1,3 sullo **stesso** database, qui viene 1,61. Il metodo
  di quel lavoro è dietro un paywall, quindi la differenza resta non spiegata
  e i valori assoluti sono provvisori. Le *differenze* fra sottoinsiemi sono
  invece nella direzione pubblicata.
- ~~La mappatura su `set_swing()` è ignota~~ — **chiusa il 17 agosto 2026,
  sul dispositivo. Vedi §6-undecies.** Il display *è* la percentuale di
  posizione del levare, e serviva anche una seconda cosa che non avevo
  previsto: `swingInterval`, cioè **su quale figura** lo swing agisce.
- **Sotto i 120 BPM la misura guarda probabilmente il livello metrico
  sbagliato**: nelle ballad lo swing si sposta sulle semicrome. `[OSS]`

---

## 6-undecies. Lo swing sul dispositivo, e due errori — 17 agosto 2026

Sessione col Deluge collegato, per chiudere la mappatura di `set_swing()`.
Chiusa, ma è costata due errori miei — uno dei quali ha bloccato la macchina.

### Cosa si scrive, adesso

```python
S.set_swing(doc, 62, figura='1/8')     # il jazz misurato, sulle CROME
```

Servono **due** cose, e ignorarne una rende inutile l'altra:

1. **Quanto** — il display *è* la percentuale di posizione del levare.
   Derivato dal sorgente: `BUR = display / (100 − display)`, quindi 50 dritto,
   67 terzina, e sotto 50 il levare arriva in anticipo.
2. **Su quale figura** — `swingInterval`, misurato con cinque salvataggi:
   `4`=1/2, `5`=1/4, **`6`=1/8**, `7`=1/16, `8`=1/32. L'etichetta sullo
   schermo nomina la figura swingata, senza traduzioni.

⚠️ **Il default del firmware è `7`, le semicrome — e vale in 146 song su 146
del corpus.** Lo swing di song è sempre stato applicato alle semicrome: su
una linea di crome non poteva sentirsi, e non perché il valore fosse basso.
Per il jazz serve `figura='1/8'`.

### Errore 1: `isPlaying`, e un Deluge bloccato

Una song generata senza `playing=True` esce con la clip a `isPlaying="0"`. Se
è l'unica clip, il dispositivo **si blocca premendo play**. Il file passava
`verifica()`, `avvertenze()`, `check_clip_types()`, il round-trip e la
decodifica delle note: formalmente perfetto e inservibile.

Famiglia di `yScrollSongView`, con variante nuova: lì lo stato sbagliato era
di **vista**, qui di **lancio**. Ora lo segnala `song.no_playing_clip()` in
`avvertenze()` — informa e non blocca, perché **10 song su 146** del corpus
sono legittimamente in quello stato (salvate da ferme).

⚠️ **E la mia bisezione era viziata.** La variante «tengo il vecchio
strumento» avrebbe funzionato, ma non per il fattore che testava: quel
vecchio strumento si porta dietro una clip con `isPlaying="1"`. Cambiava due
cose insieme, e mi avrebbe fatto concludere «contano i due strumenti». A
trovare il difetto vero è stato il confronto con un file che **suona**
(`BASSO.XML`).

### Errore 2: misurato giusto, dedotto sbagliato

La tabella di `swingInterval` era uscita **spostata di un posto** (intervallo
5 per le crome). L'osservazione a cinque punti — etichetta ↔ numero nel file —
era giusta; sopra ci avevo sovrapposto l'aritmetica del sorgente
`3 << (10 − swingInterval)`, che dà un blocco lungo **la metà** di quello
vero. Ne era uscita la conclusione controintuitiva «l'etichetta nomina il
blocco, non la figura», e l'avevo pure difesa.

L'ha smontata l'utente ascoltando: *«con 8th sento il primo ottavo dritto e il
secondo swingato»* — una frase che descrive la **coppia**, e la coppia è fatta
della figura nominata.

> **Avevo misurato la cosa giusta e dedotto quella sbagliata.** La misura
> copriva solo «etichetta ↔ numero»; il significato musicale era **inferito**,
> e l'ho trattato come se pesasse quanto la misura. È una variante nuova
> dell'errore di sempre: non «dedurre dal file invece che dal dispositivo», ma
> **appoggiare una deduzione su una misura vera e spacciare il tutto per
> misurato**.

Lo scarto col sorgente resta **ignoto** ed è dichiarato in
`song.SWING_SCARTO_SORGENTE`: i "swung tick" di quel codice non sono i tick
delle posizioni di nota, e dove si convertano non è stato trovato. Dichiararlo
è meglio che aggiustarlo a posteriori.

### File lasciati sulla SD

In `/SONGS/DelugePal/`: `SWTEST01`-`SWTEST05` (la bisezione di `isPlaying`),
`SWDIV01`-`SWDIV04` (le quattro posizioni dell'intervallo, **salvate dal
dispositivo**: sono la prova, non ripulirle), `SWJAZZ01` (sbagliata,
intervallo 5) e `SWJAZZ02` (giusta). Le prime e `SWJAZZ01` si possono
togliere; le `SWDIV` no.

---

## 6-duodecies. La rifondazione di `MUSICA.md` — 17-18 agosto 2026

Chiude il punto lasciato aperto dalla sessione dello swing: *«`MUSICA.md` è
ancora a forma di batteria reggae»*. Il documento era cresciuto attorno a un
solo genere e non reggeva il perimetro vero — jazz, classica, barocca, antica,
contemporanei.

**Lo schema neutro sono undici caselle formulate come domande**, scelte col
criterio che dovessero sopravvivere **sia a Josquin sia alla jungle**:

    1 Cos'è, e cosa non è      5 Ruoli e spartizione      9 Forma e densità
    2 Metro e griglia          6 Dinamica                10 Sul Deluge
    3 Tempo                    7 Armonia                 11 Trappole del generatore
    4 Feel                     8 Melodia e ornamentazione

`MUSICA.md` tiene lo schema, il **comune** e l'**indice**; ogni repertorio è
una scheda in `docs/repertori/`. Si legge il comune più **la sola scheda che
serve**, mai tutte.

**Il guadagno non è l'ordine, è la collisione.** A documento organizzato per
genere, l'*inégalité* barocca e lo swing del jazz non si sfiorerebbero mai — e
sono la stessa domanda, dove cade il levare dentro il movimento, fatta a due
repertori. Lo schema le mette nella stessa casella 4.

### Due invarianti che un test tiene in piedi

Le undici caselle esistono e sono in ordine in ogni scheda; e **l'indice
coincide con lo stato che ogni scheda dichiara di sé**. Lo stato si legge dalla
**prima riga non vuota** di ogni casella: `**Vuota.**` (o `**Vuota, …**`),
`**Parziale.**` esatto, qualunque altra cosa = piena. Provato rompendolo: il
test diventa rosso e nomina la casella. **La scheda è la fonte, l'indice ne è
la vista** — quando divergono è l'indice a sbagliare.

### La riga «nel frattempo», e perché è il pezzo che conta

Una casella vuota dichiara *cosa servirebbe* per riempirla, ed è ciò che rende
l'indice un'agenda. Ma chi apre i file per comporre **stasera** non ha un corpus
da leggere: ha un pezzo da scrivere, e una casella che dice solo «servirebbe
MusicXML» **lo lascia libero di inventare**. Ogni casella non piena porta quindi
una riga che dice dove prendere la risposta provvisoria e con che fiducia —
chiedere a una skill (nominando il file e segnando `[WEB]`), chiedere
all'utente, **lasciare la parte fuori**, o prendere ciò che dà una casella
sorella.

⚠️ **Una riga «nel frattempo» che prescrive ciò che la libreria non sa fare è
peggio di nessuna riga.** È successo in revisione: quella della casella 7 del
jazz mandava a realizzare l'alternanza A/B dei voicing del ii-V-I, che è giusta
musicalmente ed è scritta nella skill — ma `MU.VOICING` ha **una sola** forma
senza fondamentale e `voci()` ordina sempre dal basso, quindi la "B" non è
raggiungibile. Chi la seguiva sceglieva un voicing qualunque, lo chiamava B, e
**inventava con la benedizione della riga scritta per impedirlo.** Ora manda
alle altezze a mano con `MU.accordi()` e nomina la strada da non prendere.

### Il cancello, e cosa è costato davvero

La regola della migrazione era **le frasi si spostano come sono**: il contenuto
era stato corretto due volte dall'ascolto dell'utente, e riformularlo avrebbe
perso proprio le correzioni. Delle 745 righe smontate, **una sola era contenuto
vero perduto** — la regola *«ogni volta che una proposta viene corretta, la
lezione va qui, con la data»*, che sciogliendo il registro era rimasta
**dimostrata in quattro blocchi ma non più prescritta**. Rimessa.

L'istruttoria completa, riga per riga, è in
`docs/superpowers/2026-08-17-musica-cancello-migrazione.md`, conservata apposta:
è l'unica prova che smontando il documento non si è perso niente.

**Tre cose di metodo che valgono oltre questo lavoro:**

- **assemblare un file estraendo intervalli di righe invece di ribatterle rende
  la letteralità *misurabile*** invece che dichiarata. È così che una revisione
  ha potuto verificare «quattordici diff di sola inserzione, zero righe
  riscritte» invece di crederci;
- **quella regola protegge il contenuto, non le coordinate della vecchia
  impaginazione.** «In fondo alla sezione», «più sopra» sono indirizzi: se
  diventano falsi si correggono, ed è un difetto che la regola non era fatta per
  conservare;
- **uno snippet può essere una prova, non un esempio.** Nella casella 10 del
  reggae resta `S.set_swing(doc, 57)` **senza `figura=`**, cioè inerte: non è
  stato corretto perché la casella 4 dice «*fu scritto senza*», e aggiustarlo
  renderebbe falsa quella frase. La cautela sta nella prosa.

⚠️ **Una trappola di Markdown da conoscere prima di scrivere queste schede:**
una riga che comincia con `>` e uno spazio apre una **citazione** in CommonMark,
e le righe successive ci entrano dentro come continuazione. Un confronto come
«oltre 240 BPM» scritto col segno di maggiore e mandato a capo all'inizio di una
riga si mangia mezza casella, e si vede solo a pagina resa.

### Il Groove MIDI: la versione giusta è quella che c'è

`info.csv` ha una colonna `audio_filename` popolata su 1090 righe su 1150:
**la differenza fra midionly e versione completa è l'audio delle esecuzioni**,
non un formato diverso. Per la casella 6 — velocity e microtiming — **il MIDI è
completo e l'audio non aggiunge niente**: porta nota, velocity e l'onset esatto
di ogni colpo, e il microtiming *è* lo scarto di quegli onset dalla griglia.

L'audio servirebbe per **un'altra cosa**: il **break tagliato** di jungle e DnB,
che vive in `audio.py` — un'esecuzione a kit intero *è* un break, e siccome il
MIDI dà l'onset esatto di ogni colpo i tagli si farebbero **su posizioni note**
invece che per rilevamento dei transienti. Per cavarne colpi singoli puliti
invece serve poco: è una ripresa a kit intero, quindi un rullante estratto porta
dentro il charleston. Jungle e DnB stanno in fondo alle priorità: **non
riscaricare niente adesso.**

### Gli archivi non vanno decompressi

`zipfile`, `tarfile` e `gzip` sono **stdlib**, quindi rientrano nella regola di
non aggiungere dipendenze: si elencano e si leggono i membri di un archivio
senza estrarre nulla. Provato su `POP909.zip` — 2898 MIDI elencati, uno letto in
memoria e dato a `midi.py`, che ha risposto col suo rapporto di conversione.

L'unico attrito: `MI.leggi()` vuole un **percorso**, quindi il membro va
appoggiato in un file temporaneo. Si toglie in tre righe — `leggi()` fa già
`Path(path).read_bytes()` al suo interno, basta affiancargli un `leggi_bytes()`.
**Non fatto**, è un'offerta rimasta aperta.

### Cosa NON rifare, e i residui dichiarati

- **non ricopiare un numero in due file.** Il vincolo è che un numero vive dove
  serve a prendere una decisione musicale; altrove è un rimando. È stato violato
  e corretto tre volte in questo lavoro;
- **non fidarsi di cosa contiene una skill senza aprirla.** `music-composition`
  non ha *niente* su ska, rocksteady e dancehall — zero occorrenze in 106 file —
  e **non ha una sezione POSTBOP**, che è lo stile più numeroso della misura
  dello swing. Le righe «nel frattempo» del reggae non ci mandano apposta;
- tre residui piccoli e dichiarati: la casella 10 del reggae letta **da sola**
  mostra ancora lo snippet inerte (di proposito, vedi sopra); il corpo della
  casella 8 del reggae usa il nome corto `(aq) Dub Beat Builder` mentre sul disco
  è `(aq) Dub Beat Builder - Demo`; e il contorno del Groove MIDI (percorso,
  data, avvertenza sul `.gitignore`) compare in entrambe le schede — il *numero*
  no, ed è il contorno a rendere ogni scheda leggibile da sola.

---

## 6-terdecies. Il Groove MIDI e il groove template — 18-25 agosto 2026

Chiude la casella **6 del jazz**, che era vuota, e costruisce la cosa che
`SKILL.md` nominava da sempre senza che nessuno l'avesse mai fatta: il **groove
template**, cioè la velocity e la micro-tempistica di un batterista vero posate
su un pattern scritto da noi.

⚠️ **È l'unico lavoro di questo progetto il cui risultato non è una funzione
che passa i test ma un'affermazione sul mondo.** *«Il charleston a pedale
anticipa il ride»* non è vera o falsa per come gira il codice, e **nessun test
verde può dirne il segno**. È la ragione per cui questa sezione racconta gli
errori quanto i risultati, e per cui un task solo — quello che scrive i numeri
nella scheda — è costato **cinque giri di correzione**.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `tools/delugexml/groove.py` | il **lettore del Groove MIDI Dataset**: 1150 esecuzioni di batteria di dieci batteristi, ognuna etichettata per stile, BPM, metro e `beat_type`. Riceve la radice del dataset come argomento — esattamente come `wjazz.py` riceve il percorso del `.db` — e **non tocca mai un `Document`**: è quello il confine, non l'elenco degli import. Riusa `MI.leggi()` e `MI.GM_PERCUSSIONI` invece di farsi un secondo vocabolario di percussioni. `elenco`, `valori`, `racconta`, `scala`, `profilo`, più `per_prefisso`, `origine`, `levare_da_posizioni`, `bur_da_posizioni` |
| `MU.applica_groove(note, prof, dove=…)` | **il verbo che posa il template** su ciò che esce da `MU.passi()`. Sta in `musica.py` e non in `groove.py` per lo stesso confine: `GR` legge, `MU` scrive. **Muta la lista** — è l'unica del modulo a farlo, mentre `passi()`, `melodia()`, `accordi()` e `armonia()` costruiscono e ritornano — e il docstring lo dichiara in cima, perché in un commento interno era invisibile a `help()` |
| `MU.in_bur()` / `MU.da_bur()` | l'aritmetica del BUR, **promossa** da `wjazz.py` al vocabolario comune. Serviva a due lettori di corpora diversi: duplicarla era vietato e far dipendere un lettore dall'altro assurdo. Primo compito del piano proprio perché tocca codice che funziona, quando i test esistenti possono ancora dire se si è rotto |
| `tools/misura_groove.py` | lo **strumento di misura** da cui escono i numeri delle schede: si esegue, si legge, i numeri si scrivono a mano col loro marcatore. Ogni sezione stampa **quante esecuzioni e quanti batteristi** la sostengono — non è rendicontazione, è il numero che decide fra `[MIS]` e `[OSS]` |
| `tools/genera_groove.py`, `tools/genera_swing.py` | i due generatori di **coppia controllata**: `GROOVE0`/`GROOVE1` per il cancello sul dispositivo, `SWINGA`/`SWINGB` per l'astrazione dello swing |
| `docs/repertori/jazz.md` | le caselle **4** (un secondo BUR, su un altro corpus e con un altro metodo), **6** (**da vuota a piena**), **9** (**da vuota a parziale**: i fill sì, la forma no) e **10** (come si scrive un template, e il giro sul dispositivo) |

⚠️ **`to-read/` è in `.gitignore`.** Chi clona non trova né il dataset né il
modo di rifare i conteggi: ogni numero di quelle caselle è **lo stato del disco
del giorno in cui è stato misurato**, e le schede lo dicono accanto ai numeri
invece di lasciarlo supporre.

### Il groove template: cos'è, e soprattutto cosa NON porta

Tre decisioni di progetto, e ognuna chiude un modo di sbagliare che il resto
del documento ha già pagato altrove.

**Viene da UNA esecuzione nominata, non da una media.** `GR.profilo(base, id)`
legge un solo file — `drummer1/session3/2`, cioè batterista, stile, BPM e
durata dichiarati ogni volta che se ne cita un numero. Mediare il microtiming
di batteristi diversi lo tira verso zero, cioè **verso la griglia**: si
perderebbe esattamente ciò che si era andati a prendere. Ne segue che un
profilo è `[OSS]` **su un esecutore**, mentre la scala di velocity di
`GR.scala()` è `[MIS]` **sull'aggregato** — due marcatori diversi perché sono
due affermazioni diverse, ed è il motivo per cui `scala()` restituisce
`esecuzioni` e `batteristi` accanto a ogni mediana invece della sola mediana.

**Porta solo il residuo: lo swing lo fa la song.** Se il template portasse
anche lo swing, e `S.set_swing(doc, 62, figura='1/8')` è **di song** e vale per
basso e comping insieme alla batteria, lo swing finirebbe applicato due volte.
Quindi `profilo()` misura il BUR dell'esecuzione e **lo toglie**; quello che
resta — di quanto ogni strumento arriva prima o dopo il resto del kit — è il
template. E quel BUR tolto non è materiale di scarto: è il **controllo
indipendente** sull'1,61 misurato sulla Weimar (§6-decies). Due corpora, due
metodi, due strumenti — la linea solista trascritta contro un kit intero — e le
mediane cadono a due punti di levare di distanza: **59,7% contro 61,7%**, cioè
BUR 1,48 contro 1,61, su 41 esecuzioni e 5 batteristi. La casella 4 le porta
tutt'e due, coi rispettivi metodi, e dice che **la delimitazione decide il
numero**: dalla stessa etichetta `jazz` escono 1,26 o 1,60 a seconda di cosa ci
si include.

**Non inventa.** Se il pattern chiede un colpo su un passo dove quel batterista
non ha mai suonato, `applica_groove()` **lascia la nota com'è** e mette il
passo in `senza_appoggio`, che va letto. È lo stesso cancello della sigla
sconosciuta in `MU.armonia()`, e per la stessa ragione: un template che si
riempie i buchi da sé sarebbe di nuovo **inventare con la benedizione della
riga scritta per impedirlo**, che è il difetto raccontato in §6-duodecies a
proposito delle righe «nel frattempo».

⚠️ **E una trappola che il nome nasconde: il nome GM non è il ruolo musicale.**
Su `drummer1/session3/2` il disegno continuo di crome swingate — il ride,
musicalmente — sta per otto decimi dell'esecuzione sulla nota **43**, che la
mappa GM chiama `tom basso` (805 colpi), e solo nel quinto centrale sulla nota
**51**, `ride` (238 colpi). Chi scrive `dove='ride'` prende il profilo di un
quinto di esecuzione. **La voce si sceglie dal numero di colpi e dalla
posizione** che `GR.profilo()` riferisce, mai dal nome.

### Cosa è verificato sul dispositivo, e cosa è stato ascoltato

Sono due affermazioni diverse e stanno in due caselle diverse, ed è la regola
della §8 applicata a un caso in cui era facilissimo confonderle.

**Quello che si VEDE, ed è meccanico.** `GROOVE1` — 31 note su quattro righe,
con scarti da **−6 a +2 tick** rispetto ai passi — è stata caricata sul Deluge,
**nessuna nota è stata toccata**, ed è stata risalvata dal dispositivo.
Riscaricata e confrontata nota per nota: **31 posizioni su 31 conservate,
nessuna spostata.** Il Deluge **non riquantizza al salvataggio**, e questa era
la scommessa su cui poggiava tutto il template. Si legge nei byte di due file, e
nessuna riserva sull'orecchio di chi ascolta la tocca. Il file risalvato è
36 545 byte contro i 35 226 scritti — il firmware aggiunge roba sua — e conserva
**entrambi** gli attributi `noteDataWithSplitProb` e `noteDataWithLift`.

⚠️ **Il sub-slot, che va saputo prima di risalire un giro del genere:** il
Deluge l'ha salvata come **`GROOVE1 2`**, col numero dopo uno spazio, nella
stessa cartella. **Non sovrascrive: si fa un posto suo accanto.** Il percorso
costruito con `MU.destinazione()` non è quello da cui la song torna indietro —
si legge il nome sul display, e `MU.origine()` legge ovunque proprio per
questo.

**Quello che si SENTE, ed è un ascoltatore solo.** Quattro ascolti sulla stessa
coppia, `[OSS]`, con le domande poste **prima** di dire all'utente cosa ci si
aspettava — la previsione era scritta nel rapporto e non gli è stata mostrata,
per non guidare l'ascolto:

| ascolto | la grandezza | esito |
|---|---|---|
| il giro intero, `GROOVE0` poi `GROOVE1` | tutto insieme | sente **e vede** sia le variazioni di velocity sia quelle di timing |
| cassa contro linea di ride | 4 tick = 25 ms a 100 BPM | *«la cassa sul levare è anticipata rispetto al ride»* — **sentito**, e attribuito allo strumento giusto |
| riga del pedale contro il metronomo | 3 tick = 18,75 ms a 100 BPM | *«cadono sul click»* — **non distinto** |
| lo stesso, rifatto dall'utente a tempo lentissimo | 3 tick = 125 ms a 15 BPM | **sentito** |

Delle tre previsioni sull'ascolto **due non sono andate così**, e vale più che
averle azzeccate: chi aveva previsto che il residuo di posizione non si
sarebbe distinto sul giro intero aveva **i numeri giusti e la conclusione
sbagliata**. Se fosse andata come previsto, oggi la casella 6 concluderebbe che
`applica_groove()` vale per metà — la sola velocity — e che la posizione è
rappresentabile ma non percepibile.

⚠️ **E un difetto di metodo che va registrato perché non si ripeta: le tre
domande erano binarie e portavano dentro le parole della risposta** — «volume o
dove cadono?», «prima del ride o insieme?», «sul click o appena prima?».
Chiedere così suggerisce, e un ascoltatore compiacente direbbe sempre di sì.
Quel che le rende comunque informative è che **non ha detto sempre di sì**: due
volte «c'è» e una volta «no», e la volta del «no» è andato a rifare
l'esperimento da sé. Le domande andavano fatte **aperte**.

⚠️ **Le grandezze si dicono in tick, e i millisecondi sono una conversione a un
tempo nominato.** Un tick vale `60000/(BPM × 96)` ms — 6,25 a 100 BPM, 3,38 a
185. Presentare i millisecondi come *la* grandezza fa sembrare fisso qualcosa
che si muove col tempo, ed è precisamente l'errore che l'ascolto a 15 BPM ha
smascherato.

### Il reggae, che l'agenda dava per chiudibile e non lo è

L'agenda in testa a questo documento diceva che il Groove MIDI avrebbe chiuso
«la 6 del jazz e i `[WEB]` della 6 del reggae». Per il jazz è andata così. Per
il reggae il progetto ha **corretto l'agenda invece di eseguirla**, ed è la
correzione in testa al documento.

Il conteggio, ricontato due volte perché due volte è stato sbagliato: **venti
esecuzioni reggae**, di cui **quattro `beat` continue** — a 78, 64, 141 e 126
BPM, **due di `drummer1` e due di `drummer5`**, **dieci minuti in tutto** —
più sedici fill di due-tre secondi l'uno, tutti di `drummer1`, che ne fanno
altri 43 secondi. **Due batteristi.** E dei quattro `beat` soltanto due cadono
nella fascia di tempo che la casella 3 del reggae dichiara: dentro il perimetro
della scheda il corpus ha **due esecuzioni di un batterista solo**. La 6 del
reggae resta `[WEB]`, e adesso ci sta scritto il conteggio col motivo.

⚠️ **Quel paragrafo ha sbagliato un numero due volte mentre difendeva una tesi
giusta**, ed è la parte istruttiva. La prima versione diceva «un batterista
solo» — era una deduzione (`drummer1` ha 18 righe su 20, quindi «praticamente
uno») e **la deduzione aveva mangiato il dato**. La seconda diceva «78, 78,
141, 126»: il secondo 78 era inventato, e quell'esecuzione sta a **64 BPM**.
Trovate tutt'e due dagli implementatori **ricontando invece di rileggere**, e
la seconda pesa: 64 è uno dei due soli tempi che cadono nella fascia
dichiarata, quindi non era decorativo. Le due correzioni stanno **datate** nel
progetto, non sostituite in silenzio.

### Il difetto della finestra di grazia — la lezione più cara del ramo

⚠️ **Una correzione di mezzo passo, messa per una ragione scritta nel commento
e falsa, falsava un terzo dei colpi del corpus e fabbricava la conclusione
portante della casella 6.**

`profilo_da_colpi()` calcolava il movimento con `math.floor(p/ppq + 0.125)` —
mezzo passo di grazia — perché un colpo appena prima del battere fosse
attribuito al movimento seguente. Ne usciva una **fase negativa**, e su una
fase negativa `_senza_swing()` prendeva il ramo della prima metà del movimento
— quella che il firmware **dilata** — per una nota che sta nella seconda,
quella che il firmware **comprime**. Non era l'inversa di niente, e la catena
si credeva esattamente invertibile.

La giustificazione scritta nel commento diceva che senza la grazia «il residuo
uscirebbe grande quanto un movimento intero». **Non può**: il passo si sceglie
con `round(dritta / passo_tick)`, cioè si prende il **più vicino**, quindi il
residuo non supera mezzo passo — 12 tick — **per costruzione**. Contati sul
corpus: **0 residui oltre 12 tick su 28 604, con la grazia e senza.** Non c'era
nessun fondo di verità da salvare.

Quanto pesava, misurato su **42 esecuzioni e 28 604 colpi**:

| | |
|---|---|
| colpi che prendevano una fase negativa | **9 535 (33,3%)** |
| errore mediano sulla loro posizione | 1,25 tick (q1-q3 0,20-2,94), massimo 12,15 |
| colpi che ne uscivano **su un passo diverso** | **956 (3,3%)** |

E non cadeva a caso: il difetto vive nell'**ultimo ottavo di movimento**, cioè
esattamente dove sta chi anticipa un battere. Il charleston a pedale — che nel
jazz suona il 2 e il 4 e li anticipa — ne aveva **il 50,4% dei suoi colpi**, il
ride il 36,1%, la cassa il 37,0%, il rullante il 22,4%.

⚠️ **E così è caduto il «15 su 15», che era il risultato portante della casella
6.** Il charleston contro il ride passa a **12 su 15**, col divario mediano
**cresciuto** da 2,59 a 3,21 tick. Le due cose vanno insieme e hanno una causa
sola: con la grazia i colpi sul battere non potevano passare al passo
precedente in **38 esecuzioni su 42**, quindi **quell'unanimità era in parte
garantita dal difetto, non dai batteristi.**

Cosa regge e cosa no, detto stretto:

- **regge, ed è più solido:** la controprova **sulle fasi grezze** — nessuna
  origine tolta, nessuno swing, quindi nessuna grazia possibile — dice **15 su
  15** e non è cambiata di un decimo. È quella da citare d'ora in poi;
- **regge la stratificazione come livello:** il charleston resta il più
  anticipato di tutti, e il divario contro il ride è più grande di prima;
- **si indebolisce** il rifiuto della latenza fissa, da «~4 sigma su tutte e
  tre le coppie» a 4,2 / 2,7 / 2,4 sigma: l'ipotesi del pedale è ora stretta da
  **una** coppia su tre, non da due. ⚠️ **E il 26 agosto 2026, col cambio di
  stimatore, quei tre sigma sono diventati 3,8 / 2,8 / 1,0** — ma non tutti
  nello stesso verso: il rullante cala da 4,2 a 3,8, il ride sale appena da 2,7
  a 2,8, e la **cassa crolla da 2,4 a 1,0, cioè non porta più nessun rifiuto**
  (la sua pendenza cade a un sigma da tutt'e due le previsioni). Chi cita da qui
  «rifiutata su tutte e tre a ≥ 2,4 sigma» cita un numero superato. L'ipotesi
  del pedale resta stretta da una coppia su tre; i valori validi stanno nella
  casella 6 di `docs/repertori/jazz.md`, «Cosa esclude il test del tempo»;
- **cambiano segno due coppie**, e una era già scritta: il rullante non sta più
  dietro alla cassa nemmeno come segno;
- **non cambia niente** di BUR, scala di velocity, fill, massimo spostamento
  (+11,80 tick) ed escursione (22,83) — verificato eseguendo il tool col codice
  vecchio e col nuovo. Quindi il valore di `set_swing()` non si muove e
  **l'A/B già ascoltato dall'utente non va riletto.** ⚠️ **Gli ultimi due si
  sono poi mossi il 26 agosto 2026**, per un'altra ragione — il cambio di
  stimatore — e in due versi opposti: il massimo spostamento singolo va a
  **−19,11 tick**, cambiando anche segno, e l'escursione su tutti i passi sale
  a **27,36**, mentre quella sui soli passi con abbastanza colpi **scende**.
  Vedi la casella 6, «Due grandezze diverse». Che il 24-25 agosto non si
  fossero mossi resta vero, ed è quello che questa riga afferma; e il resto
  della riga — BUR, scala di velocity, fill, e quindi `set_swing()` e l'A/B
  dello swing — **regge anche oggi**, per la ragione scritta più sotto in
  «Cosa NON rifare».

⚠️ **Non l'ha trovato un test, e nemmeno una revisione: l'ha trovato una
domanda dell'utente su un'altra cosa.** Aveva chiesto una prova A/B
sull'astrazione dello swing — *«è un punto dove è molto facile sbagliare»* — e
costruendola è venuto fuori questo. La correzione ha poi aggiunto **12 check**,
verificati **per inversione**: rimettendo la grazia la suite scende a 938 su
943 con 5 rossi.

⚠️ **E due punti del capitolato che ordinava la correzione erano falsi**:
togliere la grazia cambia **anche** l'assegnazione dei passi (il 3,3%) e il
profilo posizionale (le quote del charleston scendono di quasi tre punti).
Nessuno dei due era previsto.

### Quattro errori di direzione in quattro giri, e un quinto alla fine

⚠️ **I valori erano sempre giusti e il verso no**, e nessun test verde può
accorgersene. Quattro giri di correzione consecutivi sul task che scrive i
numeri, un errore di direzione per giro:

| | l'errore |
|---|---|
| **1** | **una legge fisica enunciata al contrario.** Un tick dura `60000/(BPM×96)` ms, quindi una latenza fissa di D ms vale `D×BPM×96/60000` tick: **cresce** col BPM. La scheda scriveva «cala». La conclusione sopravviveva, l'argomento era falso |
| **2** | **il segno del residuo invertito in tutta la prosa.** `Passo.scarto` è positivo quando il colpo cade **dopo** la griglia — lo conferma `applica_groove()`, che fa `pos + scarto` — quindi il charleston, che ha il residuo più negativo, **anticipa**. La prosa diceva «sta dietro». Trovato **dall'implementatore stesso**, e la frase invertita stava in **sette** posti fra codice, test, piano e spec |
| **3** | **una regressione fatta sulla grandezza sbagliata.** Era sui livelli assoluti, che dopo `origine()` hanno **zero arbitrario** — cosa che la scheda stessa dichiarava tre paragrafi sopra e poi violava. Rifatta sulla grandezza **appaiata** dà 0,8 sigma da costante-in-tick e 4,0 da latenza fissa: sostiene la lettura musicale molto meglio delle tre mediane |
| **4** | **un meccanismo che spiegava un anticipo con un ritardo.** Il paragrafo sul pedale nella casella 6: la conclusione reggeva, l'argomento con cui ci si arrivava era rovesciato |
| **+1** | alla **revisione finale**, il pronome: *«il rullante dietro alla cassa succede in 12 casi su 21»* citava **il numero giusto della cosa sbagliata** — dietro è 9 su 21, davanti 12. Riscritto senza pronome e con tutt'e due i conteggi |

⚠️ **E i quattro non sono tutti la stessa cosa**, che è la parte che serve a
chi riprende. **Due sono sopravvissuti a una revisione**: il segno del residuo
per due giri, il verso della prosa sul pedale per tutti e tre. **Due li ha
introdotti la correzione stessa** — la fisica invertita è entrata **col diff
che chiudeva il giro 1**, la regressione sulla grandezza sbagliata **col diff
del giro 2** — e li ha presi la revisione di quel giro, subito. Dei cinque giri
che il task è costato, quindi, **due sono serviti a riparare danni fatti
riparando**: è per questo che qui una correzione va rivista come se fosse
codice nuovo, e non spuntata come se fosse la chiusura di un rilievo.

**E l'escalation a occhi freschi ha pagato in modo misurabile.** Dopo tre giri
di errori di direzione consecutivi il quarto è stato affidato a un
implementatore **che non aveva scritto quel testo**, e ha trovato due cose che
i tre giri precedenti non avevano visto: un **settimo** posto con la frase
invertita, e l'errore di verso nella prosa della casella 6. Le due passate di
direzione successive non hanno trovato più niente. La regola operativa:

> Quando tre revisioni di fila trovano errori della **stessa famiglia** nello
> stesso testo, il problema non è il testo — è che chi lo rilegge non vede più
> il proprio verso. Si cambia lettore, non si rilegge meglio.

### L'utente, la sesta volta — e la prima in cui ha progettato la misura

⚠️ **L'utente ha declassato i propri stessi dati d'ascolto, e aveva ragione.**
Delle tre risposte date sulla coppia non esce **nessuna soglia**, per due
ragioni e la prima è la più forte: **gli ascolti 2 e 3 non sono lo stesso
compito percettivo** — il 2 confronta due voci fra loro, il 3 confronta una
voce con un riferimento esterno, e la sensibilità dell'una non si trasporta
all'altra. Metterle in fila per dedurne un punto di passaggio non era valido
**nemmeno prima**. La seconda ragione l'ha detta lui:

> *«Considera che variazioni di pochi ms sono difficili da percepire
> consapevolmente da un umano, soprattutto con un orecchio poco allenato come
> il mio. Non credo che la differenza tra le mie risposte a 2 e 3 sia una
> "soglia". A questo livello di dettaglio tutte le mie valutazioni sono
> imprecise.»*

E prima ancora aveva **rifatto l'esperimento di sua iniziativa**, a tempo
lentissimo, ribaltando una conclusione già scritta: a 15 BPM quei 3 tick valgono
125 ms invece di 18,75, e l'anticipo si sente. Quindi l'ascolto a 100 BPM non
aveva misurato l'assenza dello scarto ma **il limite della percezione a quel
tempo** — e cadeva anche l'argomento con cui la conclusione era stata difesa
(«ascoltata nella condizione più favorevole possibile»): mancava il tempo. Un
ascolto che vuole sapere se uno scarto è percepibile ha **due** manopole,
l'isolamento e il tempo, e quel giorno la seconda non era stata girata.

**È la sesta volta che l'utente ha ragione contro qualcosa di già scritto** —
le prime cinque sono in §8 — **ed è la prima in cui non ha obiettato a parole
ma ha progettato la misura che decide.** Che è esattamente la regola operativa
che quell'elenco prescrive: quando dice che non torna, si smette di argomentare
e si costruisce l'esperimento.

Quel che ne resta stabilito non è poco: che le due domande — sfasamento fra
voci e spostamento contro un riferimento — sono **diverse e vanno poste
separate**, e che un residuo scritto **si sente quando è abbastanza grande**.
**Quanto** grande è precisamente ciò che non è stato stabilito, e **non lo
chiuderà un ascolto in più**: servirebbe un protocollo di psicoacustica —
ripetizioni, ordine casuale, prova alla cieca. È scritto come ciò che manca,
non come una lacuna da colmare in fretta: si può comporre benissimo senza
saperlo, purché non si finga di saperlo.

### Il dato più onesto della sessione: il piano aveva torto cinque volte

⚠️ **Il capitolato scritto dal controllore conteneva difetti veri in cinque
task**, e ogni volta li ha trovati **chi ha rifatto i conti invece di fidarsi
del testo**:

| task | cosa il piano sbagliava |
|---|---|
| **4** | un suggerimento del controllore che l'implementatore ha **rifiutato**, e aveva ragione: applicare `f < finestra[1]` dentro `dentro` avrebbe fatto scendere il conteggio da due a uno sulle semicrome, e un pattern di sedicesimi puro sarebbe uscito con **un levare misurato in tutti e otto i movimenti** — `[0.5]*8` invece di `[]`, cioè una coppia di crome dichiarata dove non ce n'è nessuna. Un **falso positivo** nella misura dello swing. Verificato con calcolo indipendente dal ri-revisore, **non accettato sulla parola** |
| **5** | il codice campione passava le posizioni MIDI col ppq nativo (480) invece di riscalarle ai 96 tick del Deluge. Senza riscalatura il residuo massimo su dati reali è **59,01**, con **11,80** — rapporto esattamente 5,0 = 480/96. L'implementatore l'ha aggiunta di sua iniziativa |
| **6** | il brief asseriva **un** batterista reggae e ne sono **due**; e il ripiego sui quartili per campioni sotto i 4 colpi collassava q1 e q3 sul minimo, così che la mediana cadeva **fuori** da `[q1,q3]`. Difetto ereditato dal brief |
| **7** | il test previsto dal piano interrogava `MU.passi()` invece di `applica_groove()` e **passava per costruzione**; e un avvertimento nel dispaccio era infondato, perché il controllore aveva **ricordato** il testo del piano invece di rileggerlo |
| **9** | le quattro esecuzioni `beat` del reggae non sono a «78, 78, 141, 126» ma a **78, 64, 141, 126** |

> **Il metodo che ha funzionato non è stato «il piano era buono».** È stato che
> **ogni affermazione è stata ricontrollata da qualcuno che non l'aveva
> scritta**, e che chi implementava aveva il permesso di dire di no al
> capitolato — cosa che al Task 4 ha impedito un falso positivo. Un piano
> approvato è un'ipotesi con una data, non un'autorità.

### Due incidenti identici di terminatori di riga

⚠️ **`pathlib.write_text()` su Windows traduce `\n` in `\r\n`.** Due agenti
diversi ci sono cascati nella stessa sessione: la prima volta due file passati
da LF a CRLF hanno gonfiato un diff a **1410 e 958 righe**, la seconda
`jazz.md` dichiarava **1773/1293** mentre ignorando i terminatori erano
**260/92** — **l'85% del diff non era contenuto**.

Non corrompe niente e non rompe nessun test. Rende **illeggibile la
revisione**, che in questo progetto è il meccanismo su cui poggia tutto il
resto: le cinque correzioni di verso raccontate qui sopra sono state trovate
tutte in revisione, e una revisione si fa leggendo diff. Riparato con
`write_bytes()` in tutt'e due i casi, e la regola sta in testa al documento
sotto «Cosa NON rifare», dove la legge chi genera file.

### Cosa resta aperto, e cosa NON rifare

Punti aperti che questo lavoro lascia. I due di macchina — l'ancoraggio, che
il 26 agosto 2026 è subentrato al limite dello stimatore, e cosa faccia il
firmware fra le crome — sono anche in §7, insieme alla soglia percettiva che
gli ascolti non hanno stabilito:

- **la stratificazione misurata non è mai stata messa davanti a un orecchio.**
  Il divario ride/charleston è la parte **ben misurata**, e l'ascolto è stato
  fatto su `drummer1/session3/2`, che di stratificazione ne ha quasi zero:
  l'ascolto non poteva né confermarla né smentirla. La coppia da fare è su
  **`drummer10/session1/1`** (`jazz/swing`, 124 BPM, 164 s, BUR 1,82), sui
  passi 4 e 12, e il ride lì **è** davvero `ride`. ⚠️ **I divari su cui
  poggiava questa riga sono stati rimisurati il 26 agosto 2026** — erano 5,64
  e 5,93 tick, e sono proprio le celle che il nuovo stimatore ha spostato: i
  numeri da usare per costruire la coppia stanno nella casella 6, «Cosa resta
  aperto», e vanno presi da lì e non da qui;
- ~~il limite dello stimatore, che la correzione ha smesso di nascondere~~ —
  **chiuso il 26 agosto 2026**, e la casella 6 lo racconta in «La decisione: il
  taglio si sposta per voce». `GR.profilo()` non prende più il passo **più
  vicino**: sposta il **confine** fra due passi sulla **fase media di quella
  voce**, così il gesto non si spezza più in due celle. Il criterio che ha
  deciso era fissato **prima** che le misure esistessero — la **linearità
  sotto traslazione per voce**: traslata una voce di δ tick, la posizione
  dichiarata deve muoversi di δ. Il vecchio modo la segue per lo 0,808, il
  nuovo per lo 0,998. Il «battere in minoranza» sul charleston passa da 3
  esecuzioni su 23 a **0**;
- ⚠️ **e i due criteri più ovvi erano trappole**, il che è la parte da non
  perdere. L'**errore di ricostruzione per inversione** premia lo stimatore
  rotto — spezzare un gesto in due celle stringe entrambe le mediane, quindi
  l'errore *scende* dove lo stimatore sbaglia di più. E prendere per bersaglio
  **la tenuta delle conclusioni della casella 6** avrebbe fabbricato la
  conclusione, che è il difetto della finestra di grazia rifatto uguale. Sta
  scritto nella docstring di `la_prova_di_traslazione()`, non solo nel piano;
- **l'ancoraggio: su quale dei due passi mettere un gesto ambiguo.** È il
  punto aperto che **subentra** a quello chiuso qui sopra, ed è **più
  piccolo**. Chiuso lo spezzarsi del gesto, resta indeciso *quale* passo debba
  ospitarlo: per i dati soli «14 tick prima del passo 4» e «10 tick dopo il
  passo 3» sono la stessa cosa, e il gesto è anzi **più vicino** al passo
  debole — nessun criterio di distanza può preferire il battere, a
  distinguerli c'è solo il metro. Misurato il 26 agosto 2026 su 42 esecuzioni
  e 5 batteristi: **2 celle** col modo scelto, contro 5 con `'rado'` e 0 con
  `'vicino'` — dove lo zero di `'vicino'` è **impossibile per costruzione**,
  non una virtù. Non si è scritta una regola perché avrebbe dovuto pesare il
  metro contro la distanza **senza nessuna misura che dica quanto**, cioè
  inventare un numero per due celle. Il caso resta **visibile, non
  silenzioso**, perché **la cella stessa lo dichiara**: porta il gesto quasi
  intero (14 colpi) mentre il battere accanto è quasi vuoto (1), e ha
  `|scarto|` oltre mezzo passo, che con `'vicino'` era impossibile per
  costruzione. Sono `Passo.colpi` e `Passo.scarto`, che `GR.profilo()` già
  riferisce. ⚠️ **Corretto il 28 agosto 2026:** fino a quel giorno qui c'era
  scritto che a renderlo visibile fosse `MU.applica_groove()`, «il passo che il
  profilo non ha finisce in `senza_appoggio`». **Non è vero:**
  `senza_appoggio` elenca i passi **mancanti**, mentre una cella mal ancorata
  c'è ed è sbagliata — su entrambe le celle misurate `senza_appoggio` resta
  vuoto. Vedi `docs/repertori/jazz.md`, «Il limite che resta: l'ancoraggio»;
- **se il firmware faccia davvero quello che `_senza_swing()` modella.** L'A/B
  assolve il **modello dello swing** — quattro modelli a differenza grossa
  esclusi, l'utente ha risposto *«sufficientemente simili»* — ma non la
  **catena che scrive i template**, e resta aperto cosa faccia il firmware a
  una nota che cade **fra** le crome, che il template ne scrive. La
  dichiarazione di ignoranza esiste già: `song.SWING_SCARTO_SORGENTE`;
- **il ramo `groove-midi` non è ancora stato fuso.** La revisione finale — 30
  commit rivisti insieme, nessun Critical, quattro Important tutti chiusi — lo
  ha dichiarato **fondibile**. La decisione resta da prendere.

⚠️ **Cosa NON rifare, e vale come divieto operativo:**

- **non rigenerare `out/GROOVE0.XML` e `out/GROOVE1.XML`.**
  `tools/genera_groove.py` non è un pulsante da premere: eseguirlo
  **sovrascriverebbe l'unico esemplare** dei due file su cui poggiano i quattro
  ascolti e il giro sul dispositivo (31 posizioni su 31), e l'unica traccia che
  ne resterebbe sono gli hash nel registro di sessione — `853bcdec…` per
  `GROOVE0`, `d781262c…` per `GROOVE1`. La coppia è stata costruita **prima**
  che la grazia fosse tolta: rifacendo oggi la catena la riga del pedale esce a
  **−4 tick** invece di −3, e cambiano **altre otto posizioni su 31**. Chi
  rivuole la coppia col codice di oggi **la scriva altrove e la confronti**.
  ⚠️ **Dal 26 agosto 2026 le ragioni sono due, non una:** `genera_groove.py`
  chiama `GR.profilo()` **senza passare `taglio`**, quindi segue in silenzio il
  default del modulo, che è cambiato. Il divieto **non si allenta perché i
  numeri si sono mossi — è quando si sono mossi che serve.** `out/SWINGA.XML` e
  `out/SWINGB.XML` hanno lo stesso rischio di sovrascrittura, e nessuno finora
  l'aveva scritto;
- ⚠️ **ma l'A/B dello swing NON è toccato dal cambio di default, e la
  distinzione va tenuta ferma.** `genera_swing.py` non chiama mai
  `GR.profilo()`: usa `GR.origine()` e `GR.bur_da_posizioni()` sulle posizioni
  MIDI grezze, e il BUR è calcolato **prima** che un passo venga assegnato,
  senza mai vedere `taglio` — resta 1,48 su 41 esecuzioni, levare 59,7%,
  identico nei tre modi. Il valore che `S.set_swing()` scrive è intatto e
  **l'A/B di `SWINGA`/`SWINGB` sta in piedi**. La coppia costruita sotto il
  vecchio default è `GROOVE0`/`GROOVE1`;
- ~~non citare più il «15 su 15» del residuo lavorato: è 12 su 15~~ — **il
  conteggio è tornato 15 su 15 il 26 agosto 2026**, col cambio di stimatore, e
  il divieto va letto oggi così: **non citarlo senza la sua storia.** Sono tre
  versioni — 15 su 15 garantito dal difetto della grazia, 12 su 15 dopo la
  correzione, 15 su 15 col nuovo stimatore — e il divario mediano sotto è
  cresciuto a ogni passaggio, **2,59 → 3,21 → 4,60 tick**, cioè non è la
  vecchia misura che torna. ⚠️ **E l'unanimità *esatta* dipende dal taglio:**
  con `'rado'` — l'altro candidato, quello che la regola scritta prima
  selezionava — la stessa grandezza dà **14 su 15 e +4,25 tick** `[MIS]`. La
  **direzione** no: entrambi i candidati muovono il divario nello stesso verso
  e quasi della stessa quantità (4,25 e 4,60 contro 3,21). Chi cita il
  conteggio citi anche questo. La casella 6 porta il conto per intero, compreso
  perché il criterio non poteva essere piegato per ottenerlo. Il 15 su 15
  delle **fasi grezze** resta quello che non passa da nessuna catena, e non si
  è mosso di un decimo in nessuna delle due correzioni;
- **non convertire in millisecondi i livelli della tabella del residuo.** Dopo
  `GR.origine()` ogni esecuzione ha uno **zero arbitrario**: il livello del
  charleston non dice *rispetto a che cosa*, e un millisecondo ricavato da lì
  non ha un referente. Lì i tick servono a una cosa sola, a dire che il residuo
  è piccolo.

---

## 6-quaterdecies. Lo stimatore per passo — 26-29 agosto 2026

Chiude il punto che §6-terdecies aveva lasciato aperto e che la casella 6 del
jazz **dichiarava senza prenderlo**: un groove template è per passo, e un colpo
che anticipa di più di mezzo passo usciva sul passo **precedente col segno
rovesciato** — lo stesso gesto contato in due celle.

⚠️ **Il risultato non è «un modo migliore di aggregare»: è che il modo usato da
sempre non misurava.** `round()` — il passo **più vicino** — segue i dati per
lo **0,808**, contro lo **0,998** dei due candidati, con **16 voci su 111** che
saltano di mezzo passo contro 3 e 4.

### Il criterio, e perché conta che sia stato fissato prima

**Uno stimatore è uno stimatore se la sua risposta segue ciò che misura.**
Traslata **una voce sola** di δ tick, la posizione che dichiara deve muoversi
di δ. Il criterio è stato scelto **prima che le misure esistessero**, ed è la
ragione per cui il risultato regge quando lo si attacca.

⚠️ **I due criteri più ovvi erano trappole**, e vanno tenute a mente perché si
ripresenteranno la prossima volta che si sceglie fra due modi di misurare:

| il criterio | perché non si può usare |
|---|---|
| l'**errore di ricostruzione per inversione** | **premia lo stimatore rotto**: spezzare un gesto in due celle stringe entrambe le mediane, quindi l'errore *scende* proprio dove lo stimatore sbaglia di più |
| la **tenuta delle conclusioni della casella 6** | sarebbe **fabbricare la conclusione** — la finestra di grazia di §6-terdecies rifatta uguale |

Stanno scritti nella docstring di `la_prova_di_traslazione()` e non solo nel
piano: un criterio che vive in un documento di progetto è un criterio che la
prossima sessione non trova.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `GR.spostamento_del_taglio(dritte, passo_tick, taglio)` | sposta il **confine** fra due passi invece della griglia. Tre modi: `'vicino'` (il vecchio `round()`), `'voce'` (la fase media della voce), `'rado'` (il centro dell'arco vuoto più largo) |
| il **default `'voce'`** su `profilo_da_colpi()` e `profilo()` | ⚠️ il residuo resta misurato **dalla griglia vera**, non dal taglio spostato: sottrarre anche lo spostamento toglierebbe il feel invece di collocarlo. È una riga sola, ed è quella che decide se il lavoro ha senso |
| tre sezioni nuove in `tools/misura_groove.py` | `il_vuoto_delle_voci()`, `la_prova_di_traslazione()`, `l_ancoraggio()`. E ora **ogni sezione dice con quale taglio** ha calcolato: prima `out/groove_jazz.txt` non lo diceva, e i suoi numeri dipendono dal taglio |
| `MU.applica_groove()` riferisce le **collisioni** | uno scarto può arrivare a un passo intero, quindi due note su passi adiacenti possono finire sullo stesso tick. Il Deluge lo accetta, ma un'operazione silenziosa non è correggibile |

### Cosa si è mosso, e cosa no

⚠️ **Il BUR non si è mosso, e non poteva:** si misura **prima** che un passo
sia assegnato, senza mai vedere `taglio`. Resta 1,48 su 41 esecuzioni. Ne segue
che `set_swing()` è intatto e **l'A/B sullo swing non va riletto**. La coppia
costruita col vecchio default è `GROOVE0`/`GROOVE1`, non `SWINGA`/`SWINGB` — e
il primo rapporto di questo lavoro aveva scritto il contrario.

I numeri che si sono mossi stanno nella casella 6, coi vecchi accanto ai nuovi.
**Due vanno contro conclusioni già scritte**, ed è la ragione per cui il
ritorno del «15 su 15» non è sospetto:

- la **latenza fissa non è più rifiutata sulla cassa**: 1,0 σ, dove non esclude
  più niente;
- il divario ride/charleston **entra** nella finestra 20-40 ms, quindi cade
  l'argomento «tanto sta sotto la soglia dell'udibile».

⚠️ **E il «15 su 15» che torna è dichiarato contingente:** con `'rado'` sarebbe
14 su 15, perché dipende dallo spareggio fra i due candidati — l'unica scelta
del lavoro presa **dopo** i numeri, e contro la regola scritta prima, che
selezionava `'rado'`. La *direzione* invece non dipende dal taglio: il divario
cresce con tutt'e due.

### Il dato che vale più dei numeri

⚠️ **Il piano ha avuto torto tre volte, e tre volte l'ha trovato chi lo
eseguiva** invece di aggirarlo: `'voce'` che chiamando `GR.origine()` sarebbe
stato un candidato finto — la finestra di quella funzione scarta proprio i
colpi anticipati, 58 su 143 — ; `'rado'` col taglio **incollato a fase 0**, che
sarebbe arrivato al confronto come un fantoccio; e la regola che doveva fissare
la larghezza della finestra, che sui dati **non decideva**. Una quarta l'ha
trovata la revisione finale: il motivo scritto per non chiudere l'ancoraggio
era falso, e sta corretto e datato dove stava.

È la conferma della regola di §6-terdecies: **un piano approvato è un'ipotesi
con una data.** Nessuno dei quattro l'ha trovato un test.

### Cosa NON rifare

- **non rigenerare** `out/GROOVE0.XML`, `out/GROOVE1.XML`, `out/SWINGA.XML`,
  `out/SWINGB.XML`. Il divieto di §6-terdecies **vale di più adesso**, non di
  meno: `tools/genera_groove.py` chiama `GR.profilo()` **senza passare
  `taglio`**, quindi segue in silenzio un default che è cambiato;
- **non citare un numero di `out/groove_jazz.txt` senza dire con quale taglio**
  è stato calcolato. Adesso il file lo stampa. Prima no, e quei numeri
  dipendono dal taglio più di quanto sembri.

---

## 6-quindecies. Il primo pezzo jazz — 29 agosto 2026

⚠️ **Questo lavoro non aggiunge una misura: spende quelle che c'erano.** È la
prima volta che succede, e la ragione per cui è stato fatto adesso è una
domanda dell'utente:

> «I punti aperti di jazz sono dettagli o aspetti importanti dello sviluppo?
> Da un po' ho la sensazione che siamo entrati in un rabbit hole.»

**Il conto gli ha dato ragione, e va scritto perché la prossima sessione ci
ricasca.** La scheda del jazz ha undici caselle: due piene, quattro parziali,
**cinque vuote**. Undici giorni — i rami `groove-midi` e `stimatore-per-passo` —
erano andati tutti nella **casella 6**, e gli ultimi quattro *dentro una casella
già chiusa*. Nel file la 6 occupava **1311 righe su 1954**, cioè il **67%**; la
casella 8, la melodia, ne aveva **17**. E la casella 11 dichiarava di sé che si
riempie «al primo pezzo jazz corretto dall'utente, e quel momento non è ancora
venuto»: dopo undici giorni di misure sulla batteria jazz, Deluge Pal non aveva
**mai scritto un pezzo jazz**.

⚠️ **Il difetto non era il lavoro fatto, ma l'assenza di una regola per
fermarsi.** Ogni misura ne apriva una più piccola, e nessuno ha mai chiesto
*questo cambia cosa Pal scrive?*. `midi.py`, `groove.py` e il metodo — misurare
su cinque batteristi invece di prendere le etichette dal web — restano buoni e
servono a **ogni** repertorio.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `tools/genera_jazz.py` | il generatore: blues di 12 battute in fa, hardbop, tema/assolo/tema, 36 battute, 128 BPM, quattro tracce. Tutte le scelte musicali stanno in tabelle in cima al file |
| `out/JAZZ01.XML` → `/SONGS/DelugePal/JAZZ01.XML` | sul dispositivo, caricato e verificato per rilettura |
| `song.nome_drum()` | un difetto della libreria trovato strada facendo — qui sotto |
| la **casella 11** del jazz | non è più vuota: la prima correzione dall'ascolto di un pezzo jazz, e il numero che la spiega |
| `docs/FONTI.md`, «Corpora musicali» | l'attribuzione delle due licenze, che mancava del tutto |

Il progetto del pezzo, con la provenienza e il grado di prova di ogni scelta,
sta in `docs/superpowers/specs/2026-08-29-primo-pezzo-jazz-design.md`.

⚠️ **`genera_jazz.py` NON è come `genera_groove.py` e `genera_swing.py`:**
rigenerarlo non distrugge niente. Non è una coppia controllata, non ci poggia
nessun ascolto A/B, e il divieto di quei due non si estende a questo.

### Il difetto della libreria: il nome di un drum sta in due posti

Il formato scrive il nome di un drum in **due grafie**. Il firmware recente lo
mette come **attributo** — `<sound name="KICK">` — ed è così in tutte le 43 song
del corpus e nei tre kit di terzi in `refs/kits/`. Il firmware vecchio lo
scriveva come **elemento figlio**, `<name>KICK</name>`.

`drum_index_of()` e `drum_names()` leggevano il solo attributo. Su `KIT009` —
un kit dell'utente — non trovavano **nessun** drum, e ogni scrittura per nome
falliva, mentre il dispositivo quel kit lo apre senza storie. Ora c'è
`song.nome_drum()`, che legge entrambe.

⚠️ **Che la forma a elemento fosse la VECCHIA l'ha detto l'utente**, non i file:
da soli dicevano solo che erano due. È la settima volta che una sua frase
sblocca qualcosa che i file non potevano dire — vedi §8.

⚠️ **E la causa vale oltre questo caso: la libreria è stata scritta contro il
materiale recente perché è l'unico che c'era.** Un kit di dieci anni fa non è
un caso limite esotico, è la libreria di chi usa il Deluge da dieci anni. Lo
stesso firmware vecchio scrive anche un elemento vuoto spezzato su due righe —
`REBUILD_NOTO` in `tests/test_all.py` porta ora tre file invece di uno.

### Il verdetto, e il numero che lo spiega

*«Non è niente male… non ho niente di cui lamentarmi, forse il solo potrebbe
essere un po' più pirotecnico, ma come test va bene così.»*

⚠️ **«Non ho niente di cui lamentarmi» non è «promosso», e la distinzione l'ha
fatta l'utente**: ha giudicato il pezzo *«come test»*. La casella 11 incassa
**una** direzione, e il resto è un ascolto solo, un ascoltatore, nessuna
ripetizione.

**La direzione però si misura, ed è il risultato che vale più del pezzo.**
L'assolo era stato scritto per stare dentro le grandezze osservate su un assolo
vero — `Walkin'`, melid 196 — e ci sta dentro benissimo. È quello il difetto.
Note per battuta, 12 battute contro 83:

| | generato | `Walkin'` |
|---|---|---|
| media | 5,00 | 5,23 |
| **deviazione standard** | **1,58** | **3,16** |
| massimo | 7 | **16** |
| battute vuote | **0%** | 8% |
| **battute da 8 note in su** | **0%** | **23%** |

Media e mediana centrate, **dispersione dimezzata**. I fuochi d'artificio stanno
nel 23% di battute che corrono da 8 a 16 note, e il respiro nell'8% che tace.

⚠️ **Una statistica aggregata dice dov'è il centro, non dove sta l'interesse.**
Scrivere per centrare una mediana produce la mediana. Non è un errore di
esecuzione — la misura era giusta e la linea la rispetta — **era la misura
sbagliata da rispettare**. Ne segue un requisito per la casella 8: di un assolo
va misurata la **distribuzione nel tempo**, dove stanno le corse e cosa le
precede, non la densità media.

### Come si è provato che la melodia non è copiata

Il tema e l'assolo sono originali, e la domanda l'ha posta l'utente. La risposta
è una misura, non una parola: la **più lunga sequenza di intervalli identici
consecutivi** — cioè una citazione, anche trasposta — fra la linea generata e i
corpora, con tre coppie di controllo:

| confronto | note con lo stesso profilo |
|---|---|
| generato vs `Walkin'`/Johnson — **la fonte letta** | **6** |
| generato vs `Walkin'`/Davis — mai aperto | 8 |
| **Davis vs Johnson — stesso pezzo, due umani** | **12** |
| Rollins/`Blue Seven` vs Johnson — due blues diversi | 5 |

⚠️ **Il controllo è la riga che conta.** Se ci fosse copiatura, il primo numero
sarebbe il più alto; è il più basso, e sotto al confronto con un assolo mai
aperto. Due musicisti veri sullo stesso pezzo condividono **12** note di
profilo: è quello il fondoscala, non zero. Sulle altezze assolute la sequenza
comune più lunga è di **3** note, che in una scala condivisa non è una
citazione, è la scala.

### L'attribuzione mancava, e una delle due licenze la richiede

I due corpora erano **nominati** in `MUSICA.md` e nelle schede, ma non c'era da
nessuna parte la licenza né la citazione richiesta: `FONTI.md` copriva le sole
fonti tecniche. Ora c'è, con i crediti anche nel `README.md`.

| corpus | licenza | letta da |
|---|---|---|
| Groove MIDI Dataset | **CC BY 4.0** | il file `LICENSE` **dentro** il dataset |
| Weimar Jazz Database | **ODbL 1.0** (contenuti: DbCL 1.0) | la tabella `db_info` **dentro** il `.db` |

⚠️ **La seconda non era indovinabile**, e il modo di trovarla vale come metodo:
`select * from db_info` dà licenza, autore, versione 2.1 e stato FINAL. Per un
database è la fonte più autoritativa che esista, ed era a portata di query da
due settimane. A occhio sembrava un altro caso Creative Commons.

⚠️ **L'ODbL ha una clausola di reciprocità sui database derivati che la CC BY
non ha.** `FONTI.md` porta il quadro dei fatti su cosa il progetto pubblica
oggi, scritto **come quadro dei fatti e non come parere legale**.

### Cosa NON rifare

- **non scrivere una linea melodica per centrare una media.** È il difetto che
  l'utente ha sentito, ed è misurato qui sopra;
- **non dedurre che una casella sia chiusa perché nessuno se n'è lamentato.**
  Il comping non ha sollevato obiezioni, ma non era stato scritto con
  `MU.armonia()`: l'alternanza A/B dei voicing era stata calcolata **a mano**,
  che è il ripiego prescritto dalla casella 7. Quel silenzio assolve
  l'aggiramento, non la libreria;
- **non far durare un ramo di misura oltre la domanda che lo ha aperto.** La
  regola operativa che mancava, e che ora esiste: prima di aprire una misura
  nuova, dire **cosa cambierebbe in ciò che Pal scrive**. Se la risposta è
  «niente», la misura aspetta;
- **non aggiungere file a `refs/` senza guardare i test.** I quattro preset
  scaricati per questo pezzo entrano nel corpus locale e hanno smosso due test:
  uno è stato chiuso (`REBUILD_NOTO`), l'altro — `COPPIE_OSSERVATE` — resta
  **rosso in locale** ed è una decisione dell'utente, perché rigenerare quella
  tabella inciderebbe i quattro preset dentro `sound.py`, che è versionato.
  `refs/` è ignorato da git: su un clone la suite resta verde.

---

## 6-sexdecies. La melodia, misurata — 29 agosto 2026

Chiude la **casella 8** del jazz, ed è il seguito diretto di §6-quindecies: la
domanda non è nata da un'agenda ma da un difetto **sentito**. L'assolo del
primo pezzo centrava la densità mediana del corpus e usciva piatto; la
domanda giusta non era *quante* note ma **dove**.

⚠️ **La regola di §6-quindecies è stata applicata prima di aprire la misura**,
ed è la prima volta: *cosa cambierebbe in ciò che Pal scrive?* Risposta —
l'assolo di `genera_jazz.py` è una tabella scritta a mano; misurata la
distribuzione, diventa generabile da una regola, e la prova è un secondo pezzo
che l'utente giudica. C'era un esito, quindi la misura si è aperta.

Lo strumento è `tools/misura_melodia.py`, l'ultimo giro in
`out/melodia_jazz.txt`. Il campione sono i blues `A12` a feel `SWING` di
`wjazzd.db`, con un controllo di **periodicità** della griglia: 15 assoli su 81
non lo passano e sono **scartati e contati**.

### I quattro risultati, in breve

**L'arco del giro** — 66 assoli, 38 solisti, 4808 battute `[MIS]`. Le corse
culminano sul **ii-V** (battute 9-10): **34,4%** contro il **13,3%** della
battuta 1, cioè 2,6 volte. I silenzi cadono sulle chiusure di frase — battute
4, 8 e **12**, quest'ultima vuota nel **14,8%** dei casi e la più rada di
tutte. **25 solisti su 31** lo fanno individualmente, quindi è del repertorio e
non di qualcuno. Una corsa dura **una battuta** (62%), due al massimo.

**La cella e la scala** — 80 assoli `[MIS]`. Una cella di **3 note ripetuta non
è un motivo: è la scala.** Contro la stessa linea mescolata il rapporto è
**1,02×**, cioè il caso. Il segnale compare a 4 note e diventa netto a **5**
(4,2×, in 78 assoli su 80).

**L'ornamentazione** — 166 346 note `[MIS]`, da `melody.f0_mod`, che nessuno
aveva notato. Il 3,9% delle note è ornato, e il **vibrato sta sulle note
lunghe**: 0,493 s di mediana contro 0,107 di una nota nuda, **4,6×**. Slide e
bend stanno invece su note di durata ordinaria — sono gesti di attacco, non di
tenuta.

**Dove atterra una frase** — 1913 fini di frase in 80 assoli `[MIS]`, misurate
il pomeriggio stesso perché l'ascolto le aveva nominate: *«le frasi finiscono
sempre su note che non hanno molto senso dal punto di vista della gravitazione
tonale»*. Si atterra sullo **scheletro dell'accordo** — fondamentale 1,57×,
quinta 1,29×, settima minore 1,12× — e le note dell'accordo passano dal 46,3%
ovunque al **58,7%** alle fini. ⚠️ La **terza non è favorita** (0,90×): non
basta «una nota dell'accordo», sono quelle tre.

### Le cinque lezioni di metodo, che valgono oltre la casella

⚠️ **1. La previsione era sbagliata, e nel verso che conta.** Ci si aspetta la
domanda e la risposta — silenzio, poi scoppio. I dati dicono il contrario: dopo
una battuta rada una corsa arriva nel **17,6%** dei casi, dopo una battuta
piena nel **24,2%**. Un assolo ha **zone**, non un'alternanza. Un generatore
costruito sull'intuizione avrebbe scritto una cosa che nel corpus non c'è.

⚠️ **2. Un rapporto contro un riferimento casuale va citato solo dove è
stabile.** Su celle da 6 e 7 note il riferimento tende a zero e lo si sta
dividendo per quasi niente: fra cinque semi il valore balla da 16 a 24 e da 84
a 140. Lo strumento gira **cinque semi**, stampa min e max e marca `BALLA` da
sé, così l'instabilità non va riscoperta. Si cita il minimo; a sette note non
si cita affatto un rapporto, si dice che per caso non ricorre.

⚠️ **3. In un generatore che cammina, una modifica sembra locale e non lo è.**
Per correggere l'undicesima finale, `JAZZ04` aveva cambiato l'ultima nota del
**motivo**: sembra una nota, ed è invece il valore da cui riparte il cammino
della battuta dopo. Tutto l'assolo è divergiuto — **56 slot su 192** invece di
3, con le note cromatiche **sui movimenti** dal 12% al 21%, che l'utente ha
sentito subito e ha respinto. `JAZZ05` fa la stessa correzione senza toccare
il motivo: **2 slot su 192**. Prima di dire «cambia solo X», si contano gli
slot diversi.

⚠️ **4. Una misura aggregata può migliorare mentre la musica peggiora, ed è
successo DUE VOLTE in un pomeriggio.** `JAZZ01` centrava la densità mediana ed
era piatto; `JAZZ04` **abbassava** lo scarto dal corpus sui gradi da 33,7 a
23,3 — e quel numero era stato riportato come un miglioramento — mentre
peggiorava. Contava *quante* note e non *dove*, che è la lezione appena
scritta, non applicata alla misura che la doveva verificare. **Una statistica
aggregata serve a trovare dove guardare, non a promuovere:** la promozione la
dà l'ascolto.

⚠️ **5. Due misure indipendenti hanno dato la stessa soglia.** Il controllo
anti-copiatura del pezzo (§6-quindecies) aveva dichiarato tre note in comune
«la scala, non una citazione», per argomento. Questa misura lo conferma con un
riferimento casuale: a tre note la ricorrenza è indistinguibile dal caso. Le
due cose non si sapevano l'una dell'altra.

### Cosa NON rifare

- **non citare un rapporto reale/mescolato senza guardare se balla.** È la
  ragione per cui `misura_melodia.py` non ha un seme solo;
- **non ripetere celle di tre note per «fare sviluppo motivico».** Misurato: è
  ciò che succederebbe comunque, ed è la soglia sotto cui si sta guardando il
  vocabolario e chiamandolo motivo;
- **non generare alternando corsa e silenzio**, per quanto sia l'immagine
  ovvia. Le corse si addensano;
- ⚠️ **non dare per scritto sul Deluge ciò che il corpus annota.** Vibrato,
  slide, bend e fall-off sono misurati *nel corpus*; che il dispositivo sappia
  farli è una domanda della **casella 10** e **nessuno dei tre è stato provato**.

---

## 6-septdecies. La condotta delle parti — 29 agosto 2026

Chiude la **casella 7** del jazz. `MU.voci_condotte()`: ogni accordo dopo il
primo si posa nella disposizione che muove meno voci rispetto a quello prima.
`MU.armonia()` la usa **di default**, `condotta=False` dà il comportamento
precedente, `voci()` e un accordo solo non cambiano.

⚠️ **L'invariante che rende la cosa sicura: cambia DOVE, non QUALI.** Si
scelgono le ottave, mai le note — le classi di altezza restano quelle che
`voci()` sceglie. Verificato sul pezzo: passando il comping dalla tabella
scritta a mano alla libreria, **tutte e 59 le posizioni di accordo hanno le
stesse classi di prima**, e 35 su 59 anche le stesse altezze esatte.

E `genera_jazz.py` **perde la tabella di altezze scritta a mano**. Era il
criterio dichiarato prima di aprire il lavoro — «la tabella sparisce» — ed è
quello che dice che la casella è chiusa davvero.

### Le tre cose che valgono più del codice

⚠️ **1. La casella 7 diceva una cosa falsa, e mandava una sessione a
implementarla.** Diceva: «la chiuderebbe `assets/jazz-voicings.md`… qui manca
implementarla, non trovarla». Quella fonte **non specifica** l'alternanza A/B
in modo implementabile, per tre ragioni indipendenti, tutte verificate in
`test_condotta_delle_parti`: i nomi A e B non sono definiti (la fonte stessa
scrive *«the naming convention depends on the source»*); il suo esempio non usa
nessuna delle due forme — il G7 è `b7-9-3-13`, con la tredicesima al posto
della quinta; e la regola che dichiara, *«only one voice moves per chord
change»*, **fallisce sul suo stesso esempio** (`Dm7 → G7` una voce,
`G7 → Cmaj7` tre). Resta solido lo **scopo**, ed è quello che si implementa.

⚠️ **La correzione è stata scritta nella casella, non sostituita in silenzio.**
Una riga che manda a cercare qualcosa che non c'è costa più di una casella
vuota.

⚠️ **2. Il minimo movimento è goloso, e si vede solo sulla lunghezza vera.** Su
un ii-V-I la funzione sembrava a posto. Sul blues per **tre giri** il comping
scendeva di **diciassette semitoni** — da `[57,60,63,67]` a `[40,43,46,50]` —
perché il passo piccolo è sempre disponibile nella stessa direzione e la scelta
golosa lo prende ogni volta. `MU.DERIVA_MASSIMA = 6` lo tiene entro mezza
ottava dall'ancora: deriva da −17 a −5. **La regola: una funzione che sceglie
un passo alla volta va provata sulla lunghezza a cui verrà usata.** Tre accordi
non sono trentasei battute.

⚠️ **3. `racconta_armonia()` avrebbe mentito.** Esiste per la regola 4 — un
operazione silenziosa non è correggibile — e non conosceva la condotta: avrebbe
riferito le altezze **non condotte** mentre `armonia()` ne scriveva altre. Ha
ora lo stesso default, e un test che confronta quel che dice con quel che viene
scritto. **Una funzione che rende conto e sbaglia il conto è peggio di
nessuna**, ed è il genere di difetto che nessun altro test avrebbe visto.

### Cosa resta fuori, e sta scritto nella casella

La **sostituzione di tensione** (la tredicesima al posto della quinta), il
**ritmo armonico** — quando un accordo cambia — e le **sostituzioni di
accordo**, che il giro letto da `Walkin'` non ha e su cui la casella non dice
se sia tipico o sia quel pezzo.

---

## 6-octodecies. Il metodo cambia, e la direzione anche — 30 agosto 2026

**È la sezione più importante di questo file per chi riprende**, perché due
delle tre cose che porta non sono risultati ma **regole**, e cambiano cosa si
fa e cosa non si fa.

### 1. Le caselle si riempiono SU DOMANDA, non a tappeto

Proposta dell'utente, dopo aver visto il ritmo di lavoro:

> «Visto che il repertorio è mastodontico… io punterei a usare questo primo
> passaggio sul blues per creare un metodo di riempimento delle caselle, da
> applicare **in itinere ogni volta che il task compositivo lo richiede**.»

⚠️ **E i tempi dei commit gli danno ragione di venti volte:**

| | come | costo |
|---|---|---|
| casella 6, dinamica | *a tappeto*, senza che un pezzo la chiedesse | **undici giorni** |
| caselle 8, 7, 11 | *su domanda*, ognuna aperta da un difetto sentito | **otto ore in tutto** |

Il ciclo in sette passi sta in `docs/MUSICA.md`, «Il comune → Metodo». **Il
passo che fa la velocità è il terzo: il difetto nomina la casella.** Non si
misura mai ciò di cui nessuno si è lamentato.

⚠️ **E c'è un secondo argomento, più insidioso della lentezza: una casella
scritta senza domanda invecchia SBAGLIATA.** In due giorni ne sono state
trovate **tre** — 7, 9, e di nuovo 7 — e tutte e tre mandavano a cercare fuori
qualcosa che era già su disco. Tutte e tre le ha trovate **un pezzo che
qualcuno voleva scrivere**.

### 2. Il corpus dà RELAZIONI, non superfici

**È la regola che decide cosa si può prendere da un corpus**, data dall'utente
dopo aver ascoltato tre pezzi:

> «Noi vogliamo un tool per AI per creare musica **ORIGINALE**, non repliche
> dei pattern studiati. Vogliamo usare quel database per produrre qualcosa di
> **nuovo ma coerente con il contesto**.»

Si applica **prima** di prendere una misura, e la prova è una riga: *due
generazioni con la stessa misura devono poter essere diverse*. Se la misura
fissa **cosa** si suona è una superficie; se fissa **come si sta** — dove si
atterra, quanto si cresce, cosa risponde a cosa — è una relazione.

L'inventario per esteso, con il caso grigio del groove template, sta nel
comune. In breve: gli atterraggi, la soglia del motivo, l'arco di densità e la
condotta delle parti stanno dalla parte giusta; **il pattern di batteria
campionato da un'esecuzione e le altezze pescate da un istogramma no**.

⚠️ **Metà del lavoro fatto sul jazz stava dalla parte sbagliata senza che
nessuno se ne fosse accorto.** È la ragione per cui la regola è scritta e non
sottintesa.

### 3. Il generatore è parametrico sulla forma, e ci sono tre pezzi

`tools/genera_jazz.py` non scrive più solo blues. Tutto ciò che dipende dalla
forma sta in una struttura `Pezzo`; il resto dello script non sa che forma
stia suonando.

    .venv/Scripts/python.exe tools/genera_jazz.py            il blues
    .venv/Scripts/python.exe tools/genera_jazz.py rhythm     il rhythm changes
    .venv/Scripts/python.exe tools/genera_jazz.py modale     il modale

⚠️ **La guardia del rifacimento, e va rifatta ogni volta che si tocca la
struttura:** dopo ogni cambio, rigenerare i pezzi che non si volevano toccare
deve dare file **byte per byte identici**. Ha funzionato due volte e ha
scoperto l'unico cambio non voluto (il basso sul turnaround, che era invece
una correzione giusta).

| pezzo | forma | verdetto |
|---|---|---|
| `JAZZ06` | blues di 12, sei versioni | *«molto meglio»* alla sesta |
| `RHYTHM06` | AABA, rhythm changes | *«la forma si sente bene»* **alla prima** |
| `MODALE06` | AABA, due modi dorici | *«suona modale, il comping non impasta»* |

⚠️ **Sei versioni per il primo pezzo, una per il secondo.** Groove, swing,
generatore d'assolo, atterraggi e condotta sono arrivati dal blues **senza una
modifica**. È l'argomento che rende sostenibile il metodo su domanda — col suo
limite: ha retto fra forme **dello stesso repertorio**, stesso tempo, stesso
batterista.

### Cosa è entrato in libreria, e da quale fonte

| | |
|---|---|
| `MU.voci_condotte()`, e `armonia(condotta=True)` di default | la condotta delle parti. ⚠️ **NON è l'alternanza A/B**: la fonte non la specifica, e le tre ragioni stanno nella sua docstring |
| `MU.DERIVA_MASSIMA` | il vincolo di registro. Senza, il minimo movimento è **goloso** e su tre giri il comping scendeva di **diciassette semitoni** |
| `voicing='quartale'` | lo stack di quarte, dalla fonte. **Rifiuta** fuori dal minore settima |
| `tools/misura_melodia.py` | l'arco del giro e la soglia del motivo |
| `tools/genera_coppie_cable.py` | ri-deriva `COPPIE_OSSERVATE`, che era «incollata» senza lo script |

### ⚠️ Il difetto aperto, ed è quello con cui la sessione si è chiusa

La batteria è stata resa varia **campionando** le frequenze di tre esecuzioni
diverse. Ha tolto il sintomo — i tre pezzi non suonavano più uguali — **col
metodo che la regola 2 vieta**, e l'utente ha sentito subito il difetto nuovo:

> «La batteria suona discontinua rispetto a basso e piano che sono
> praticamente costanti… le interruzioni, accenti e struttura delle parti di
> batteria sono strettamente correlati alla sezione ritmica, e non le puoi
> applicare acriticamente.»

Misurato — deviazione standard dei colpi per battuta:

| batteria | comping | basso |
|---|---|---|
| **1,48 - 1,65** | 0,54 - 0,61 | **0,00** |

**Il basso non varia mai**: 4,00 note per battuta, zero battute diverse da
quattro su 228, quattro posizioni, una sola durata. La batteria varia contro
uno sfondo fermo.

⚠️ ~~**E la correlazione che servirebbe non è misurabile da nessun corpus in
casa.** Il Groove MIDI è **batteria sola**, `wjazzd.db` è **la linea solista
sola**: si può misurare cosa fa un batterista e cosa fa un solista, e mai come
si rispondono. Non è questione di quanti dati — il dato non c'è.~~

⚠️ **FALSO, e corretto il 1 settembre 2026 (§6-noviesdecies).** L'errore non
era nei due corpora nominati — su quelli la frase è esatta — ma nel salto da
«questi due non ce l'hanno» a «il dato non esiste», fatto **senza cercare**.
Il Jazz Trio Database ce l'ha, con licenza MIT. **La correlazione è misurata:
nella densità per battuta non c'è (+0,058), nella coincidenza degli eventi
fuori griglia c'è e vale 1,52 volte il caso.**

---

## 6-noviesdecies. La casella 5, e una premessa che nessuno aveva verificato — 1 settembre 2026

**La cosa che questa sezione porta non è la casella: è come si è arrivati a
riempirla.** Il piano diceva di scrivere un lettore di partiture MusicXML. La
prima mezz'ora è stata spesa a controllare *perché* lo diceva, e la ragione
non reggeva.

### La riga falsa, e le tre volte che era scritta

L'handoff, la casella 5 di `jazz.md` e §6-octodecies dicevano tutt'e tre la
stessa cosa: *«nessun corpus in casa ha l'insieme che suona insieme — non è
questione di quanti dati, è che il dato non c'è»*. Misurato prima di scrivere
una riga di codice:

| affermazione | esito |
|---|---|
| MusicXML su disco | **zero file.** La strada dichiarata richiedeva **anche** procurare un corpus, e questo non era scritto da nessuna parte |
| «nessun insieme in casa» | **falsa.** `to-read/MIDI/songs_archive` ha **17 230** file multitraccia, **241** di artisti jazz; su 14 letti a campione con `midi.py`, **11 portano basso e batteria insieme** coi ruoli nominati (`ACOU BASS`, `DRUMS`) |
| il MusicXML risolverebbe la casella 5 | **no.** In **PDMX** — 250 000 spartiti di pubblico dominio, il più grande corpus MusicXML libero — oltre il **90% ha meno di cinque parti** e più della metà sono pezzi solistici, e gli autori scrivono che i multitraccia non sono di pubblico dominio. **Niente batteria** |
| esiste un corpus d'insieme con licenza | **sì**, ed era a un download di distanza |

⚠️ **È la quarta volta che una casella scritta senza domanda manda a cercare
fuori qualcosa di già raggiungibile** — le altre tre stanno in §6-octodecies e
nel comune di `MUSICA.md`. È anche la più cara, perché quella riga **aveva
cambiato il piano di lavoro** e non solo il contenuto di una scheda.

⚠️ **E ha portato via un esempio a una regola.** Il comune diceva: «alcune
caselle hanno prerequisiti che non si scoprono a metà pezzo — la casella 5
vuole un lettore MusicXML». La casella 5 è stata chiusa in un pomeriggio con
**200 righe di stdlib**. La regola resta scritta ma **senza prova**, e chi la
invoca per rimandare un lavoro deve portare l'esempio che adesso manca.

### La fonte: il Jazz Trio Database

**1294 esecuzioni** di trio jazz del 1947–2015 — **34 pianisti, 98 bassisti,
106 batteristi** — ottenute da registrazioni vere per separazione di sorgente
(Cheston, Schlichting, Cross, Harrison, TISMIR 2024). **Licenza MIT**,
attribuzione in `docs/FONTI.md`. **24 MB**, in `to-read/MIDI/`, e l'audio non
serve.

Per ogni brano: gli onset di **piano, basso e batteria allineati agli stessi
beat**, la posizione metrica, e il MIDI del piano. ⚠️ **La colonna vuota del
suo `beats.csv` dice quando quello strumento NON ha suonato su quel beat**, ed
è il dato su cui poggia tutta la casella.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `tools/delugexml/jtd.py` | il lettore, stdlib pura, legge **dentro lo zip senza decomprimere**. `elenco()`, `griglia()`, `battute()`, `onsets()`, `piano()`. Non decide niente di musicale: ogni soglia sta nello strumento di misura |
| `tools/controlla_jtd.py` | i **cinque controlli** che, se saltano, sbagliano ogni cifra a valle senza far fallire un test |
| `tools/misura_spartizione.py` | le cinque misure, **due volte**: su tutto il corpus e sul JTD-300 |
| `midi.leggi_bytes()` | tre righe, l'offerta rimasta aperta in §6-duodecies |

**1056 test**, e i nuovi saltano se il corpus non c'è.

### I numeri, e il primo dice tutto

| | tutto il corpus | JTD-300 |
|---|---|---|
| battute di basso **diverse da quattro** | **59,7%** | 58,7% |
| deviazione dentro la singola esecuzione | **1,03** | 1,05 |
| beat su cui il basso tace | 15,0% (corretto) | 14,8% |
| correlazione densità basso↔batteria | +0,058 | +0,062 |
| coincidenze fuori griglia a 20 ms | **30,6% contro 20,1% attesi** | 32,1% contro 21,3% |
| scarto sul beat: piano / basso / batteria | **+15,3 / +2,3 / −0,4 ms** | +16,4 / +2,9 / −0,2 |

⚠️ **Il generatore fa 4,00 note per battuta con deviazione 0,00.** Non è «meno
vario di un bassista vero»: è **fuori dalla distribuzione**, perché il valore
centrale del corpus copre solo il 40% delle battute.

⚠️ **E l'utente aveva ragione sulla batteria, ma non dove sembrava.** Nella
*densità* per battuta la batteria non segue il basso (+0,058, cioè niente).
Nella *coincidenza* degli eventi fuori griglia lo segue eccome: **1,52 volte
il caso** a 20 ms, e l'eccesso **cresce al restringersi della finestra**, che è
la forma di una sincronia vera e non di un artefatto. Confermato identico sul
campione indipendente JTD-300.

### Cosa NON si può chiedere a questa casella

- ⚠️ **quale pezzo del kit**: gli onset di batteria sono aggregati. «Il
  rullante fa X» non è ricavabile da qui, ed è il limite che pesa di più sul
  difetto del 30 agosto;
- le **altezze** di basso e batteria (le avrebbe FiloBass, licenza ristretta);
- la **forma**: JTD non annota sezioni;
- la **dinamica** d'insieme: gli onset non portano intensità.

### Cosa NON rifare

- **non fidarsi di una riga che dice «il dato non esiste» senza averla
  verificata.** Costa mezz'ora verificarla e ha cambiato la direzione del
  lavoro. Quattro volte su quattro, finora, la riga era sbagliata;
- **non misurare la simultaneità sugli onset detection.** `piano_onsets.csv`
  conta **un attacco per accordo** — 1070 eventi dove il MIDI ne ha 3138 — e
  chiedergli quante note attaccano insieme dà **0% di accordi a 30 ms**. Il
  numero era assurdo e per questo si è visto: se fosse stato solo *basso*
  sarebbe passato;
- **non citare il numero grezzo dei beat taciuti.** Il 10,1% di quei silenzi è
  un allineamento mancato, misurato dal controllo 2;
- **non far entrare nella scheda un numero la cui forbice supera la soglia**
  fissata prima di misurare. Il comping del piano sta fra il 69% e l'86% a
  seconda della finestra: nella casella c'è la forbice, non una percentuale.

### Il prossimo passo, e non è una casella

**Spendere queste misure sul generatore.** Il basso deve variare come varia un
walking vero, e la batteria deve agganciarsi agli eventi fuori griglia del
basso invece di essere campionata da un'esecuzione. ⚠️ E poi va fatto sentire:
finché un pezzo non è stato ascoltato dall'utente, di queste misure si sa che
sono giuste, non che servono.

---

## 6-vicies. Le misure spese sul basso, e tre errori trovati misurando — 6 settembre 2026

**Il passo che §6-noviesdecies nominava — «spendere queste misure sul
generatore» — è fatto per il basso, e non per la batteria.** Il basso della
versione **08** pesca quante note fare dalla distribuzione misurata invece di
farne sempre quattro; l'aggancio della batteria, la **09**, è scritto e
misurato ma **non riproduce la misura per cui esisteva**, e il perché vale più
del codice.

⚠️ **Le tre cose che questa sessione ha trovato sono tutte errori miei o del
lavoro precedente, e tutte e tre sono uscite da un controllo, non da un
ascolto.** È la stessa forma delle quattro volte precedenti.

### 1. La misura 3 contava 25 556 onset che non erano fuori griglia

Il numero pubblicato il 1 settembre — **30,6% contro 20,1%, cioè 1,52×** su
**170 394** onset — escludeva come «sul beat» i quattro beat **della battuta**
ma non la sua **fine**, che è il movimento della battuta dopo. Gli attacchi
**anticipati del battere successivo** passavano quindi per note fuori griglia:
il **15,0%** del totale, e si vedevano perché il quarto movimento ne portava il
**66% in più** degli altri tre, col 17,4% ammassato a fase 0,97.

**La correzione rafforza il risultato**, che è l'opposto di quel che avevo
previsto scrivendolo: quegli onset avevano il 22,4% di coincidenza, sotto la
media, perché un anticipo del battere e un colpo *sul* battere distano più di
20 ms. Il numero giusto è **32,1% contro 20,1% = 1,60×**, e **1,58×** su
JTD-300.

### 2. Il criterio fissato prima di misurare era fragile, e non ha potuto decidere

La misura nuova — dove cade la nota in più — aveva il suo criterio scritto
nella spec **prima** di guardare i dati, com'è regola qui. Ma era fissato sulla
fase di **picco**, e il picco **si sposta di 0,05 (0,18 su JTD-300) solo
cambiando l'ampiezza degli intervalli dell'istogramma**, che è una scelta
arbitraria di chi misura: con intervalli da 0,05 direbbe «croma swingata», con
quelli da 0,02 direbbe «nessuna delle due».

⚠️ **La lezione vale oltre la casella: una statistica pre-registrata dev'essere
anche ROBUSTA, non solo dichiarata prima.** Pre-registrare una statistica
fragile dà l'illusione del rigore senza la sostanza. Lo strumento ora stampa da
sé quanto il picco si sposta, e riporta la **mediana**, che non dipende dagli
intervalli: **0,651** e **0,636**. Ci cadono sopra tre cose indipendenti — la
terzina (0,667), lo swing del solista in hardbop della casella 4 (0,643), e la
posizione che il firmware dà alla croma con `SWING = 64` (0,640).

### 3. Nessun `print` può contenere `⚠️`

La console di Windows è **cp1252**: `strumento.py > file.txt` fa fallire la
scrittura con `UnicodeEncodeError`. È costato una passata di misura interrotta
a metà **senza che il codice di uscita lo dicesse** (il `; echo` in coda al
comando mascherava l'errore), e in `genera_jazz.py` colpiva proprio la riga che
segnala `verifica()` non vuota — cioè l'errore da segnalare sarebbe diventato
un errore diverso. Nei commenti e nei docstring l'emoji va bene: non si
codifica mai.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `MU.linea()` | il caso generale di cui `melodia()` è la scorciatoia a passo fisso: ogni nota con la sua posizione e la sua durata. Serviva perché un basso che tiene una nota per due movimenti non è esprimibile a passo fisso |
| `misura_spartizione` misure 6 e 7 | dove cade la nota in più, e la distribuzione **dentro** l'esecuzione |
| `onset_fuori_griglia()` | la definizione di «fuori griglia», scritta una volta sola per le misure 3 e 6 |
| `walking()` variabile | pesca quante note, i silenzi di due specie, gli approcci cromatici |
| `_aggancia()` + `--aggancio` | il secondo sorteggio della batteria, e i numeri che dicono che non basta |
| `confronto_col_corpus()` | il generatore misura il pezzo che ha appena scritto |

**1096 test**, e due di loro sono guardie dell'attribuzione: la batteria della
08 è identica a quella della 07, e la 09 alla 08 aggiunge colpi e non ne toglie
nessuno.

### La distribuzione giusta non è quella pubblicata, ed è il punto tecnico che conta

⚠️ La tabella delle note per battuta della casella 5 mette insieme **1099
esecuzioni**: la sua dispersione vale **1,33** perché somma quanto varia un
bassista dentro un pezzo (**1,03**) e quanto i bassisti differiscono fra loro
(**0,84**). **Un pezzo generato è UNA esecuzione**: pescare dall'aggregata gli
darebbe il **29% di varietà in più** di un bassista vero. La misura 7 prende le
sole esecuzioni la cui media sta entro 0,2 da 4,27 — 319 esecuzioni, 65
bassisti, 34 048 battute — e la sua deviazione è **0,94**, dentro la tolleranza
di ±0,10 da 1,03 fissata prima di misurare.

**E i silenzi sono di due specie.** Una battuta da tre note ha per forza un
movimento vuoto (il 5,0% dei movimenti viene da lì), ma il corpus ne misura il
15,0%: i restanti sono silenzi dove il bassista lascia il movimento e suona
altrove, e ognuno va compensato da una croma. Legarli al solo numero di note dà
il 5,6%; sorteggiarli indipendenti e poi far quadrare il conto dà il 19,4%.

### Perché l'aggancio della batteria non funziona, e cosa lo bloccherebbe davvero

| pezzo | senza aggancio | con aggancio | corpus |
|---|---|---|---|
| blues | 2,40× | 3,38× | 1,60× |
| rhythm changes | 1,66× | 2,39× | 1,60× |
| modale | **0,00×** | **0,00×** | 1,60× |

Nel generatore basso e batteria stanno sulla **stessa griglia a sedicesimi**:
o condividono il passo o distano 117 ms, quindi la coincidenza è
**tutto-o-niente** — le finestre da 20, 30 e 50 ms danno la stessa
percentuale — mentre nel corpus è continua. E quanto valga quel «tutto» lo
decide il **groove template**: il batterista del modale ha scarti fino a
**+10,9 tick**, e 20 ms sono **4,1 tick**.

⚠️ **Il difetto sotto è del basso, non della batteria: il basso del generatore
è quantizzato esatto, dispersione zero**, mentre la misura 4 dà al basso vero
+2,3 ms con dispersione 6,4. Un basso senza microtiming non può andare incontro
a una batteria che ce l'ha.

### Cosa NON rifare

- **non pre-registrare una statistica fragile.** Dichiararla prima non basta
  se dipende da una scelta arbitraria di chi misura;
- **non mettere emoji dentro un `print`**, e **non chiudere un comando con
  `; echo`**: maschera il codice di uscita di quello che conta;
- **non toccare il sorteggio sequenziale di `_voce_dal_profilo()`**, nemmeno
  per renderlo più pulito: due versioni confrontabili dipendono da lui;
- **non applicare un rapporto misurato alla grandezza sbagliata.** 1,60× sulla
  probabilità del profilo non fa 1,60× sulla coincidenza a 20 ms, e la
  differenza fra le due non si vede finché non si stampa il numero.

---

## 6-unetvicies. Il livello musicale cambia natura — 10-11 settembre 2026

⚠️ **È la sessione più importante del progetto, e non perché abbia prodotto
codice: perché ha cambiato cosa il livello musicale è.** Chi riprende da qui
legga prima
`docs/superpowers/specs/2026-09-10-skill-compositiva-design.md`.

### Il generatore a dadi è stato buttato, e l'utente ha detto perché

> «hai creato un generatore random con parametri presi da analisi statistiche
> di un corpus enorme. come potrebbe mai produrre risultati accettabili?
> questo non è assolutamente quello che volevo. io immaginavo una skill
> compositiva più approfondita, con istruzioni teoriche armoniche e ritmiche
> e "groove template", il tutto basato su una analisi del corpus.»

In una riga: **una distribuzione descrive com'è fatto un insieme di dischi,
non come si scrive una battuta.**

⚠️ E la regola che lo avrebbe evitato era scritta dal 30 agosto — *«il corpus
dà RELAZIONI, non superfici»* — ed è stata violata per tre settimane senza che
nessuno se ne accorgesse.

### Le tre decisioni di metodo, che il codice non racconta

1. **L'unità di lavoro è UNA PARTE sopra materiale dato**, poi il pezzo
   intero, poi le risposte a domande. Il progetto faceva il secondo senza che
   nessuno l'avesse deciso.
2. **Le note le decide l'AI, le primitive eseguono.** Il codice calcola e non
   pesca: condotta delle parti, posizioni, durate, groove template.
3. **Il mestiere viene dalla letteratura didattica**, verificata sul corpus
   dove ha senso. Il materiale è in `to-read/`, che **non è versionato**.

### Il walking: ha funzionato al primo colpo

`docs/istruzioni/walking.md` + `tools/walking_scritto.py`. La procedura viene
dal *Jazz Theory Justified* cap. IV: fondamentali sui movimenti dove l'accordo
entra, nell'ottava più vicina, poi si riempie **guardando l'intervallo fra le
fondamentali**. È relazionale: cosa metti dipende da cosa è appena successo.

Verdetto: *«la linea regge»*. I numeri misurati stanno accanto come **limiti,
non come motore**, e la linea esce di proposito più regolare dei dischi.

### La batteria: dieci versioni, e la lezione sta lì

| versione | cosa cambiava | verdetto |
|---|---|---|
| 13 | frasi di due battute con quattro di silenzio, da Riley p. 20 | «troppo rarefatta, praticamente assente per intere battute» |
| 14 | quattro strati costanti, dai pattern di un batterista vero | «va molto meglio, ora abbiamo un ritmo… un po' pesante» |
| 15 | cassa alleggerita per sezione, aggiunte che rispondono alla melodia | «un po' meglio, ma le parti meno peggio restano quelle di jazz 1-6» |
| **16** | **composta a mano, 36 battute una per una** | **«molto meglio»** |

⚠️ **La 13, la 14 e la 15 erano generatori travestiti.** Pur essendo
«scritte», erano una regola più le sue eccezioni applicate a tutte e 36 le
battute. La 16 no: ogni battuta è una decisione, col motivo scritto accanto, e
la sequenza non ha una formula.

**La prova interna sta dentro questa stessa sessione:** il walking ha
funzionato perché l'istruzione dà una procedura per una decisione **locale** e
poi si compone; la batteria non funzionava perché l'istruzione dava una
procedura per **l'intera parte**.

### La frase che decide cosa una skill può contenere

> «usare statistiche su tutto il corpus non funziona, e anche l'analisi
> formale di una singola fonte non può funzionare per astrarre leggi
> compositive generalizzabili, che soprattutto nel jazz di fatto non esistono»

Da qui la forma che `docs/istruzioni/batteria-jazz.md` ha adesso, e che vale
per tutte le istruzioni future:

- **vocabolario** — le figure idiomatiche, come catalogo;
- **vincoli** — cosa NON si fa, ognuno con la versione che l'ha violato;
- **il tocco** — il groove template, misurato;
- **una procedura LOCALE** — come si decide *una* battuta;
- **un esempio lavorato** — una parte intera commentata, da leggere non da
  copiare.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/` | le istruzioni compositive: walking, batteria |
| `tools/walking_scritto.py` | la linea di basso, 36 battute scritte |
| `tools/batteria_scritta.py` | la parte di batteria, 36 battute composte |
| `GR.battute_per_voce()` | i pattern battuta per battuta dal Groove MIDI — il lavoro di libreria dichiarato mancante dal 30 agosto |
| `GR.quote_per_voce()` | le quote condizionate alle battute in cui la voce suona |
| `MU.linea()` | il caso generale di `melodia()`, a durate proprie |
| `tools/misura_pattern.py` | chi tiene il tempo, misurato sui pattern |

**1124 test.**

### Come si leggono i PDF scansionati, che serve e non è ovvio

Riley e Crook sono **scansioni**: zero caratteri estraibili. Le pagine sono
CCITT G4 dentro il PDF. Si estraggono avvolgendo i byte grezzi in
un'intestazione TIFF — senza decodificare niente — e `System.Drawing` di .NET
le converte in PNG. **Non serve installare nulla.** Lo strumento sta nella
cartella di lavoro della sessione; se serve di nuovo, va rifatto o promosso.

⚠️ Piston in edizione leggibile è arrivato (600 pagine col testo). Le
scansioni vecchie sono state sostituite.

### Cosa NON rifare

- **non trasformare una distribuzione in un motore**;
- **non dedurre una legge generale da un esecutore solo.** «Questo batterista
  batte il movimento 2 quasi sempre» è vero di lui e falso come regola:
  applicato a 36 battute ha prodotto un metronomo;
- **non prendere un esercizio di un libro per una descrizione.** Riley scrive
  «non suonare le semiminime con la cassa» e «quattro battute di silenzio» per
  far isolare una cosa alla volta a chi studia. Presi alla lettera hanno
  prodotto due versioni respinte;
- **non scrivere una regola che valga per tutte le battute.** Se la sequenza
  ha una formula, si sente;
- **non trattare i verdetti come parametri da tarare.** «Troppo rada» →
  aggiungo, «troppo pesante» → tolgo è salire una collina a tentoni: tre giri
  così hanno prodotto tre «un po' meglio».

### Il prossimo passo

**Il comping del piano**, con lo stesso metodo: si guardano i pattern di una o
due fonti, si scrive l'istruzione come vocabolario e vincoli, si compone la
parte, si ascolta.

⚠️ Restano senza parte scritta il **rhythm changes** e il **modale**, che
usano ancora il generatore a sorteggio per basso e batteria.

---

## 6-duetvicies. Il perimetro, e la prima armonia — 11 settembre 2026

**Due cose in questa sessione: è stato deciso COSA deve fare lo strumento, e
l'armonia ha superato la sua prima prova al primo colpo.**

### Il perimetro, che mancava dal primo giorno

Alla domanda diretta «che lavoro deve fare lo strumento», l'utente:

> «competenze musicali limitate, approccio sperimentale ed eclettico.
> Supporto compositivo innanzi tutto **armonico** — spettro ampio e jazz
> approfondito, la musica modale mi piace molto — e **ritmico**, ma solo dal
> jazz in poi e solo alcuni generi, con groove template. Anche l'aspetto
> **formale** (voicing, contrappunto, comping, struttura). Mi interessa poco
> replicare filologicamente un genere: piuttosto attingere al **bagaglio
> espressivo** di un genere per le mie composizioni. Il supporto va da
> armonizzare-arrangiare un'idea esistente a creare un pezzo da zero che poi
> modifico sul Deluge.»

Sta per esteso nel design doc, sezione «Il perimetro», e in memoria
(`perimetro-deluge-pal`). ⚠️ Senza questa definizione il progetto aveva
inseguito i corpus disponibili (c'era `wjazzd` → si è fatto jazz) invece della
musica da fare — e nessuna delle 43 song dell'utente è jazz: sono elettronica,
jungle, industrial, modale, cromatico.

**La conseguenza sulla «grande limitazione del corpus».** La preoccupazione
dell'utente — *«se abbiamo solo swing, che senso ha il lavoro sul corpus»* — si
scioglie con le priorità: la limitazione (il Jazz Trio Database è tutto
walking; per l'insieme jazz manca il resto) tocca **solo la priorità 3, e solo
il jazz dentro di essa**. L'armonia — il centro — dipende dalla teoria, non da
quei corpus. Il jazz-swing fatto finora (fino a JAZZ16) non era sbagliato come
lavoro, era sbagliato come **centro**.

### La casella 1 del jazz, compilata

Le etichette di `wjazzd.db`, mai lette prima se non per lo swing, dicono che il
jazz non è un feel solo: **tradizionale al 100% in due**, **fusion al 100%
funk**, latin dentro cool/hardbop/postbop, e il postbop è lo stile più
numeroso. Le due istruzioni di batteria e basso sono state **ridelimitate**:
coprono lo swing con walking, una casella sola della griglia feel × strumento.
⚠️ E i corpus in casa insegnano quel solo feel — sta scritto accanto ai numeri
delle altre caselle, che descrivono lo swing-con-walking, non «il jazz».

### La prima istruzione armonica, e funziona

`docs/istruzioni/armonia-modale.md`, scritta leggendo **Piston** (*Harmony* 5ª
ed., cap. 5 e 30 — ora in edizione col testo estraibile) e il **Jazz Theory
Justified** (cap. IX). Il principio: l'armonia modale è **colore statico, non
funzione** — parte dalla scala, non dalla progressione, l'opposto del ii-V-I.
Il meccanismo, da Piston: i gradi III e VI **definiscono il modo**, e la
**dominante minore** al posto del V7 toglie la sensibile → il tritono → la
spinta che riporterebbe al tonale. Le affermazioni `[CALC]` (note
caratteristiche, triadi) sono **verificate da un test** contro `song.MODI`.

### PERCHE: il primo «armonizzare un'idea esistente» riuscito

Su una song dell'utente: riarmonizzato **solo l'arpeggio** (melodia e pad
intatti), richiesta «misterioso e alieno». La versione **Re frigio** —
oscillazione I ↔ ♭II (Re m ↔ Mi♭ maggiore), il suono andaluso, niente
sensibile, finale sospeso — è stata approvata: *«frigio mi piace molto»*.
L'esempio è documentato nell'istruzione; lo script sta in scratchpad (dipende
da `refs/songs/Perche.XML`, non versionato).

⚠️ **L'armonia ha funzionato al primo colpo**, contro le dieci versioni della
batteria: conferma che è terreno più fermo del ritmo, come dice il perimetro.

⚠️ **Una lezione: il voicing quartale NON è automaticamente meglio.** Provato
su PERCHE (più Mi♭, quarte impilate, tritono Mi♭–La), l'utente ha preferito le
triadi — le quarte aprono ma tolgono corpo. È un colore del vocabolario, non
un traguardo.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/armonia-modale.md` | la prima istruzione armonica: vocabolario dei sette modi, vincoli, come si decide, esempio lavorato |
| casella 1 di `jazz.md` | il perimetro stilistico: stili, feel, cosa i corpus in casa NON coprono |
| test `armonia_modale_note_caratteristiche` | blinda le affermazioni `[CALC]` dell'istruzione contro `song.MODI` |

**1136 test.**

### Il prossimo passo

Due strade, in ordine di vicinanza a quello che l'utente cerca:

1. **il modal interchange** — prendere in prestito un accordo da un modo
   parallelo. È il ponte diretto verso l'eclettismo dichiarato, e sta nel Jazz
   Theory p. 66 (già estratto, da leggere);
2. **un pezzo modale da zero** — l'istruzione ha superato l'armonizzare
   un'idea esistente, non ancora il creare dal nulla.

⚠️ Restano fuori dal perimetro coperto: i feel non-swing del jazz (in due,
latin, funk), le scale non diatoniche che l'utente usa (ottatoniche,
cromatiche), e tutta la priorità 2 (voicing, contrappunto, comping, struttura)
salvo `MU.armonia()` che già conduce le parti.

---

## 6-tervicies. L'armonia si allarga — prestito, scale simmetriche, cromatismo — 12-13 settembre 2026

**In due giorni l'armonia è passata dalla prima prova del prestito a una
copertura ampia dello spettro espressivo.** Sei istruzioni nuove, nove pezzi
costruiti da zero e caricati sul Deluge, **tutti approvati al primo colpo**. Il
metodo è quello di §6-unetvicies (istruzioni, non generatore); il flusso quello
di PERCHE — scrivi una parte → carica via SysEx → l'utente ascolta → il verdetto
chiude l'istruzione con l'esempio lavorato.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/armonia-prestito.md` | il **prestito modale** (modal interchange), due case. **Maggiore:** iv, ♭VI, ♭VII, ♭III, I→Im, ♭II napoletano (dal minore parallelo). **Minore:** IV maggiore (schiaritura dorica), colore del minore jazz (m6, m(maj7), il line cliché), Piccardia (dal maggiore parallelo). Tre esempi lavorati |
| `docs/istruzioni/scala-ottatonica.md` | la **diminuita**: simmetrica per terza minore, tesa (dim7, dom7♭9), il ciclo dei quattro dom7 a terza minore |
| `docs/istruzioni/scala-esatonale.md` | la **whole-tone**: simmetrica per tono, sospesa (aumentate, dom7♯5), il ciclo per tono |
| `docs/istruzioni/armonia-parallela.md` | il **planing cromatico**: una forma che scivola parallela, `condotta=False` |
| `docs/istruzioni/medianti-cromatiche.md` | le **medianti cromatiche**: scarto di terza con una nota in comune, `condotta=True` |
| `docs/istruzioni/accordi-di-passaggio.md` | gli **accordi di passaggio/approccio**: diminuita di passaggio (basso cromatico) e tritone sub (♭II7), `condotta=True` |
| `song.MODI` | tre scale nominate nuove: **ottatonica**, **esatonale**, **cromatica** |
| `tools/*_scritto.py` | i pezzi composti (materiale, con la ragione accanto): `prestito_scritto` (3 pezzi), `ottatonica_/esatonale_/planing_/medianti_/passaggio_scritto` |
| `tests/test_all.py` | un guardiano `[CALC]` per ogni istruzione + un test per ogni pezzo. Suite **1136 → 1233** |

### Il metodo ha retto, e lo dice un numero

Otto pezzi, **zero versioni respinte** — contro le dieci della batteria
(§6-unetvicies). Conferma quello che il perimetro diceva in teoria: **l'armonia
è terreno più fermo del ritmo**, e dipende dalla teoria, non da un corpus di
performance. L'unica correzione chiesta dall'utente in due giorni è stata di
scope (quale colore), mai «suona male».

### La leva tecnica: `condotta` accesa o spenta

⚠️ **È il punto che un agente deve sapere.** `MU.armonia(..., condotta=...)`:

- **`True`** (default) tiene la nota comune e muove poco le voci — serve
  all'armonia **modale**, al **prestito**, alle **medianti** (la morbidezza È la
  nota tenuta);
- **`False`** voicizza ogni accordo rigido, in fondamentale — serve **solo** al
  **planing** (la forma deve restare parallela; la condotta la romperebbe).

È l'unico posto in cui la condotta va spenta. Sta scritto in
`armonia-parallela.md` e nella docstring del pezzo.

### Le fonti, e una cosa onesta

| cosa | fonte |
|---|---|
| ottatonica | Smith, *Jazz Theory* (4ª ed.), p. 75-77 |
| whole-tone | Piston, *Harmony* (5ª ed.), cap. 31, p. 490 |
| planing | Piston, cap. 31 «Parallel and Antiparallel Harmony», p. 496 |
| Piccardia | Piston, cap. 5 «The Picardy Third», p. 64 |
| napoletana (♭II) | Piston, cap. 26 «The Neapolitan Sixth», p. 407 |
| minore jazz (↑6/↑7) | Smith, p. 74 |
| passaggio / tritone sub | Smith, cap. VIII p. 59 (+ cap. IX p. 75) |

⚠️ **Smith NON copre la whole-tone** (verificato: zero occorrenze): per quella si
cambia libro (Piston). ⚠️ **Le medianti cromatiche non hanno una fonte che le
NOMINI** (il termine è neo-riemanniano): il rigore sta nel `[CALC]` — il fatto
della nota comune, testato — dichiarato esplicitamente nell'istruzione, con
Piston cap. 28 come solo contesto. **Non si è forzata una citazione**, ed è una
regola: se la fonte non nomina la cosa, lo si dice.

⚠️ **Una citazione corretta verificando sul PDF** (§ commit `0d71210`): il libro
è **Smith, "Jazz Theory"** — non "Jazz Theory Justified" come dicevano
`armonia-modale.md` e `walking.md` — e la sezione «Modal Jazz» è nel cap. X, non
nel cap. IX. La Piccardia è Piston cap. 5, non cap. 26.

### Come si costruisce e si carica un pezzo di prova

I **material scripts** (`tools/*_scritto.py`) sono **versionati** e tengono le
note con la ragione accanto (come `walking_scritto.py`). L'**assemblaggio** — da
`refs/songs/TEMPL0.XML`, via il track di default, tre tracce da `refs/synths/`
(Tal Rhodes / 062 Trumpet / Square Saw Bass), `MU.scrivi`, `set_scale`,
`verifica`, `write_file` — più il `put` SysEx stanno in **scratchpad**, **non
versionati** (dipendono da `refs/`, escluso). Il template carica di default il
patch a pagamento BOD: si toglie con `MU.togli` e si parte puliti.

⚠️ **`dsysex put` va lanciato da PowerShell, non da Git Bash:** da Git Bash il
percorso remoto `/SONGS/DelugePal/...` viene storpiato in `C:/Program
Files/Git/SONGS/...` e l'`open` fallisce. Vedi la memoria `dsysex-da-powershell`.

### Cosa NON rifare

- **non sbagliare la `condotta`:** spenta per il planing, accesa per tutto il
  resto;
- **non forzare una citazione** quando la fonte non nomina la cosa: `[CALC]` +
  contesto, dichiarato;
- **non lanciare `dsysex put` da Git Bash** (storpia il path remoto);
- **non chiamare "modo" una scala simmetrica o cromatica:** va in `MODI` come
  intervalli, ma non è un modo del maggiore.

### Il prossimo passo

⚠️ **Il cromatismo è chiuso**, tre facce su tre: planing (`armonia-parallela.md`),
medianti (`medianti-cromatiche.md`), passaggio/approccio (`accordi-di-passaggio.md`).
Quindi:

1. **uscire dall'armonia verso la priorità 2, la forma**: voicing, contrappunto,
   comping, struttura (`MU.armonia()` già conduce le parti; il resto è da
   scrivere). È il passo naturale;
2. oppure restare sull'armonia e raccogliere le code rimaste (sotto).

⚠️ Restano comunque fuori, sull'armonia: le **doppie medianti** (terza senza
nota in comune), il **diatonic planing** (scivolare dentro una scala), i **feel
non-swing del jazz** (in due, latin, funk).

---

## 6-quatervicies. La spina funzionale — la casa che regge — 13 settembre 2026

**Scritta la fondazione che tutte le istruzioni d'armonia davano per scontata e
nessuna insegnava.** Due istruzioni nuove — `armonia-funzionale` (ii-V-I,
cadenze, turnaround) e `dominanti-secondarie` (la tonicizzazione) — chiudono il
buco più grosso dell'armonia: la **casa tonale che regge e risolve**, il centro
di «jazz approfondito». ⚠️ **Zero codice:** il vocabolario di sigle di
`musica.py` era già completo (`7, m7, maj7, m7b5, dim7`, e gli alterati fino a
`7alt`); il lavoro è documentazione + due guardiani `[CALC]`.

Il passo nasce da una domanda dell'utente — *«prima di passare alla priorità 2,
assicuriamoci che la copertura d'armonia sia completa»* — e da una ricognizione:
le nove istruzioni coprivano il **colore** (modale, prestito, scale simmetriche,
cromatismo) ma non la **funzione** che colorano. Ogni istruzione funzionale
cominciava con «parti da un giro diatonico che regge»; nessuna lo insegnava.

### La variazione di metodo: l'armonia si chiude col `[CALC]`, senza ascolto

⚠️ **Deciso dall'utente, ed è la cosa che un agente deve sapere.** Motivo: *«lo
sviluppo dell'armonia ha sempre avuto un successo del 100%, perché sono regole
precise ed è impossibile sbagliare»*. Da qui in avanti, **per l'armonia** il
guardiano `[CALC]` **sostituisce** l'esempio lavorato caricato sul Deluge: niente
`[OSS]`, niente pezzo di prova, niente `_scritto`. ⚠️ **Vale solo per l'armonia**
(regola precisa), **non per il ritmo**, dove l'ascolto ha respinto dieci versioni
della batteria. Le due istruzioni della spina sono le prime armoniche senza
esempio all'ascolto. Sta in memoria (`armonia-si-chiude-col-calc`) e nel design.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/armonia-funzionale.md` | le tre funzioni (T/S/D), il **ii-V-I** maggiore e minore (col iiø7 e la sensibile), le quattro **cadenze** (autentica, plagale, inganno, sospesa), il **turnaround** I-vi-ii-V |
| `docs/istruzioni/dominanti-secondarie.md` | le cinque **dominanti secondarie** (V7/ii…V7/vi, non il vii°), il **ii-V interpolato**, il **ciclo delle quinte**; il tritone sub rimandato ad `accordi-di-passaggio` |
| `tests/test_all.py` | `test_armonia_funzionale` + `test_dominanti_secondarie`, guardiani `[CALC]`. Suite **1233 → 1258** |
| rimandi | `armonia-funzionale` è il **file-fondazione**: prestito, accordi-di-passaggio e modale ora lo linkano per «la casa» |

### Le fonti, verificate sui PDF

| cosa | fonte |
|---|---|
| funzione vs. colore, circolo delle quinte, ii-V-I | Smith, *Jazz Theory* (4ª ed.), cap. VIII, p. 51 e 53 |
| funzioni tonali dei gradi | Piston, *Harmony* (5ª ed.), cap. 5, p. 52 |
| risoluzione del V7 (il tritono) | Piston, cap. 15, p. 243 |
| le quattro cadenze | Piston, cap. 11 «Cadences», p. 172 (sospesa 175, plagale 178, inganno 181) |
| dominanti secondarie / tonicizzazione | Piston, cap. 16 «Secondary Dominants», p. 257-258; Smith cap. VIII p. 57 e 65 |

⚠️ **L'offset dei PDF, che serve a chi ci torna:** in `to-read/`, col testo
estraibile. *Jazz Theory*: pagina-libro = pagina-PDF **+ 1**. Piston: pagina-libro
= pagina-PDF **− 19**. Le citazioni sono state lette sulla pagina, non dalla
memoria — e Piston da 600 pagine si scansiona in background, non in linea.

### Cosa NON rifare

- **non reintrodurre l'esempio all'ascolto per l'armonia:** la variazione di
  metodo dice che il `[CALC]` basta — ma vale **solo** per l'armonia, non per il
  ritmo;
- **non duplicare il tritone sub:** vive in `accordi-di-passaggio`, nelle
  dominanti secondarie è un rimando;
- **non inventare le pagine:** si aprono i PDF (offset sopra) e si verifica;
- **non tonicizzare il vii°** diminuito: non è una tonica su cui posarsi.

### Il prossimo passo

⚠️ **Con la spina, l'armonia funzionale c'è.** Resta, sull'armonia, in ordine:

1. ~~**la dominante alterata**~~ — **fatta il 13 settembre, §6-quinvicies**;
2. ~~le **code piccole**: doppie medianti, diatonic planing, seste aumentate~~ —
   **fatte il 13 settembre, §6-quinvicies**;
3. poi **la priorità 2, la forma** (voicing, contrappunto, comping, struttura).

---

## 6-quinvicies. La dominante alterata e le code — l'armonia è coperta — 13 settembre 2026

**Chiusa l'armonia della priorità 1.** Dopo la spina funzionale, due blocchi
insieme (**stesso metodo**: `[LIB]` + `[CALC]`, niente ascolto): la **dominante
alterata** (la tensione dopo la funzione) e le **code** che restavano — doppie
medianti, diatonic planing, seste aumentate. Con questo l'armonia copre
funzionale + tensione + cromatismo (tre facce + due estensioni) + modale +
prestito + scale simmetriche. Il prossimo passo **esce dalla priorità 1**.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/dominante-alterata.md` | le **quattro scale della dominante**: alterata (super-locria) e lidia dominante (modi della melodica), ottatonica HW, esatonale — con le tensioni che ciascuna dà |
| `docs/istruzioni/seste-aumentate.md` | le **seste aumentate** it./ted./fr.; ⚠️ la **tedesca è enarmonicamente un dom7** (il cugino classico del tritone sub) |
| `medianti-cromatiche.md` + sezione | le **doppie medianti** — a terza senza **nessuna** nota comune (Do→Fa#, il tritono) |
| `armonia-parallela.md` + sezione | il **diatonic planing** — la forma scivola *dentro* una scala, per grado, e flette (`condotta=False`) |
| `song.MODI` | due scale nuove: **`alterata`** (0,1,3,4,6,8,10) e **`lidia dominante`** (0,2,4,6,7,9,10), modi della minore melodica |
| `tests/test_all.py` | `test_dominante_alterata`, `test_seste_aumentate`, `test_medianti_doppie`, `test_diatonic_planing`. Suite **1258 → 1282** |

### La cosa da sapere: dove i libri non nominano la scala

⚠️ **La scala alterata e la lidia dominante NON sono nominate nei libri in casa.**
Smith rifiuta anzi il multi-scala (p. 77-78: «una sola forma di minore») e rimanda
a Russell (*Lydian Chromatic Concept*), che non c'è. Come per le **medianti
cromatiche**, la regola ha retto: **non si è forzata una citazione**; il rigore è
nel `[CALC]` (sono rotazioni della minore melodica, testato), dichiarato. È la
seconda volta che questa regola decide, ed è la stessa di §6-tervicies.

### Le fonti verificate (offset dei PDF in §6-quatervicies)

| cosa | fonte |
|---|---|
| le tensioni non cambiano la funzione | Smith, cap. VIII, p. 57 e 78 |
| l'ottatonica sopra la dominante alterata | Smith, cap. IX, p. 77 |
| l'esatonale / whole-tone | Piston, cap. 31, p. 490 |
| le seste aumentate | Piston, cap. 27 «Augmented Sixth Chords», p. 419-420 |

⚠️ **Le seste aumentate confermano il legame col tritone sub dal lato classico:**
Piston p. 419 dice che nascono da «V di V con la quinta abbassata», e la tedesca
è lo stesso accordo (Lab7 in Do) che il jazz chiama ♭II7. Due grafie, un suono.

### Cosa NON rifare

- **non forzare una citazione** per alterata/lidia dominante: `[CALC]` + contesto,
  come le medianti;
- **non chiamarle «modi del maggiore»**: sono della minore melodica, in `MODI`
  come intervalli;
- **non togliere la risoluzione alla dominante alterata**: senza il ritorno a
  casa torna a essere una scala simmetrica che galleggia (vedi ottatonica/esatonale).

### Il prossimo passo

⚠️ **L'armonia della priorità 1 è coperta.** Il passo naturale è ora la
**priorità 2, la forma**: voicing (upper structure, quartale, drop), contrappunto,
comping, struttura. `MU.armonia()` già conduce le parti; il resto è da scrivere.
~~Restano fuori dall'armonia solo cose di seconda fila (gli altri modi della
melodica, il ritmo armonico)~~ — **fatte anche quelle il 13 settembre,
§6-sexvicies**: l'armonia è chiusa, code comprese.

---

## 6-sexvicies. Il ritmo armonico e i modi della melodica — l'armonia è chiusa — 13 settembre 2026

**Le due ultime code dell'armonia, in un passo.** Il **ritmo armonico** (ogni
quanto cambia l'accordo, e dove cade sul metro) e **gli altri cinque modi della
minore melodica** (i due dominanti — alterata, lidia dominante — erano già in
`dominante-alterata`). Con questo la priorità 1 **non ha più code**: il prossimo
passo esce davvero verso la forma.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/ritmo-armonico.md` | ogni quanto cambia l'accordo, il peso del metro (la «tirannia della stanghetta», lo stress agogico), l'accelerare verso la cadenza; il meccanismo `durata` sul Deluge |
| `docs/istruzioni/modi-minore-melodica.md` | il quadro dei **sette modi** della melodica → sette accordi; i due dominanti rimandati a `dominante-alterata` |
| `song.MODI` | quattro modi nuovi: `dorico b2`, `lidio aumentato`, `misolidio b6`, `locrio nat2` |
| `tests/test_all.py` | `test_ritmo_armonico`, `test_modi_minore_melodica`. Suite **1282 → 1292** |
| rimandi | funzionale, dominante-alterata, modale e prestito ora puntano a `ritmo-armonico` dove dicevano «scelta del caso» |

### Le fonti verificate

| cosa | fonte |
|---|---|
| il ritmo armonico | Piston, cap. 12 «Harmonic Rhythm», p. 189 (la frequenza del cambio, la stanghetta, lo stress agogico); Smith p. 53 (l'alternanza forte-debole del ii-V-I) e p. 65 (a minima) |
| la scala minore melodica | Piston, cap. 4 «The Minor Mode», p. 43 |

### Le due cose da sapere

⚠️ **Il `[CALC]` del ritmo armonico è sul MECCANISMO, non sull'altezza:** il ritmo
armonico è tempo, non note, e il guardiano verifica che `durata` in `MU.armonia`
fissi la distanza fra gli attacchi (1/1 → 384 tick, 1/2 → 192). È il primo
guardiano armonico di questo tipo, e va bene: la regola «l'armonia si chiude col
`[CALC]`» non impone che il `[CALC]` sia sulle note.

⚠️ **Il sistema dei modi come chord-scale NON è nominato nei libri** (Smith lo
rifiuta, p. 77-78, rimanda a Russell): come l'alterata e le medianti, `[CALC]` +
contesto, senza forzare la citazione. **Terza volta** che questa regola decide.

### Cosa NON rifare

- **non forzare una citazione** per il sistema dei modi;
- **non duplicare i due modi dominanti** (alterata, lidia dominante): vivono in
  `dominante-alterata`, qui sono un rimando;
- il **ritmo armonico disuguale** si compone a segmenti (`durata` è uniforme per
  chiamata di `MU.armonia`): è una comodità di libreria mancante, non una lacuna
  di teoria.

### Il prossimo passo

⚠️ **L'armonia della priorità 1 è chiusa, code comprese.** Il passo è la
**priorità 2, la forma** — cominciata subito col voicing, §6-septvicies.

---

## 6-septvicies. La priorità 2 comincia: il voicing — 13 settembre 2026

**Primo passo della forma, e primo con un metodo nuovo.** Chiusa l'armonia, si
entra nella forma dalla faccia più vicina: il **voicing** — come disporre le note
di un accordo. `docs/istruzioni/voicing.md`.

### Il metodo cambia di nuovo: `[CALC]` + un ascolto

⚠️ **Deciso dall'utente, ed è il punto che un agente deve sapere.** Il voicing
**non** è «impossibile sbagliare» come l'armonia pura: le meccaniche sono precise
(e già testate), ma **quale** voicing suona giusto è un giudizio d'orecchio —
PERCHE l'aveva già mostrato (il quartale scartato perché toglieva corpo). Quindi
né il solo `[CALC]` dell'armonia né l'ascolto pieno del ritmo, ma un **ibrido**:
`[LIB]` + `[CALC]` per le meccaniche, e un esempio lavorato **ascoltato** per la
scelta. ⚠️ **Conseguenza:** l'agente non chiude l'istruzione da solo — l'ultimo
passo (l'ascolto) è dell'utente. La regola generale, in memoria
(`voicing-calc-piu-ascolto`): il metodo scala con **quanto orecchio** serve —
regola precisa → `[CALC]`; con una parte di gusto → `[CALC]` + un ascolto; corpo
di performance → ascolto pieno.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/voicing.md` | quando usare quale voicing (chiuso, shell, rootless/Bill Evans, drop2, quartale); il principio, come si sceglie, l'ortogonalità condotta/voicing |
| `tools/voicing_scritto.py` | il pezzo di **confronto**: lo stesso ii-V-I in tre voicing, per l'ascolto |
| `tests/test_all.py` | `test_voicing_scritto`. ⚠️ Le **meccaniche** dei voicing avevano **già** i guardiani (`test_voicing_*`, `test_condotta_delle_parti`): l'istruzione li richiama, non li riscrive. Suite **1292 → 1299** |
| `out/VOICING01.XML` | caricato e **verificato per rilettura** sul Deluge (non versionato: incorpora i preset) |

### Il codice del voicing c'era già, l'istruzione no

⚠️ **È il pattern della priorità 2.** `MU.voci` faceva già cinque voicing e
`voci_condotte` conduceva le parti — scritti nell'era del generatore. Mancava
l'istruzione che insegnasse **quando** usarli. Spesso, nella forma, parte
dell'infrastruttura esiste già: il lavoro è lo strato di **scelta**, non il
codice.

### Il verdetto, e cosa conferma

Le tre versioni (`VOICING01`, Rhodes + basso, lo stesso `Dm7 | G7 | Cmaj7` in
chiuso / rootless / drop2): **«sono tutti e tre belli e funzionano; quale
preferisco dipende dal contesto»**. Conferma all'orecchio il principio di Smith
(`[LIB]` cap. VI «Chord Voicings», p. 35: non c'è un voicing giusto in assoluto),
e **passa al primo colpo**, come l'armonia. Fonti: shell p. 37, rootless p. 38,
drop2 p. 46, quartale p. 81.

### Cosa NON rifare

- **non riscrivere i guardiani `[CALC]`** dei voicing: esistono, si richiamano;
- **non chiudere un'istruzione con parte d'orecchio senza l'ascolto:** il metodo
  qui è `[CALC]` + un ascolto, non il solo `[CALC]`;
- **non confondere voicing e condotta:** sono ortogonali.

### Il prossimo passo

⚠️ Le altre facce della priorità 2, in ordine di vicinanza: il **comping** (i
pattern **ritmici** dell'accompagnamento — poggia su voicing +
`ritmo-armonico`), poi il **contrappunto** (linee indipendenti), poi la
**struttura** (l'arco lungo, l'`arranger` c'è già). Il comping è il naturale
prossimo.

---

## 6-octovicies. Nuova letteratura, e la revisione dell'armonia con Levine — 13 settembre 2026

**L'utente ha aggiunto la letteratura che mancava**, e tutta l'armonia è stata
rivista contro di essa. Il grosso: **Levine, *The Jazz Piano Book*** — la fonte
canonica di voicing, comping e chord-scale del jazz, un intero libro dove Smith
aveva un capitolo.

### La letteratura nuova, e come si legge

| libro | formato | uso |
|---|---|---|
| Levine, *The Jazz Piano Book* | PDF (testo) | voicing, comping, chord-scale |
| Levine, *The Jazz Theory Book* | djvu | teoria jazz profonda (da minare su domanda) |
| Piston, *Counterpoint* (1970) | djvu | il **contrappunto** (faccia da fare) |
| Crook, *How to Improvise* | PDF scansione | melodia/assolo — servirà OCR |

⚠️ **Tool djvu installati:** DjVuLibre (winget `DjVuLibre.DjView`, dalla fonte
ufficiale) in `C:\Program Files (x86)\DjVuLibre\`; `djvutxt.exe --page=N` estrae
il testo (c'è un layer OCR, con rumore). ⚠️ Non su PATH in una shell nuova: usare
il percorso pieno. Tutto in memoria `letteratura-composizione`.

### La scoperta che dà ragione all'utente

⚠️ **Levine NOMINA le chord-scale che Smith RIFIUTA.** Smith (p. 77-78) nega
l'approccio multi-scala; Levine (cap. 9 «Scale Theory») lo **abbraccia** e nomina
proprio: la **scala alterata** (super-locrio = 7º modo della melodica =
«diminished whole-tone», fig. 9-24), la **lidia dominante** (4º modo), la
**diminished scale** (fig. 9-27), la **whole-tone** (fig. 9-40), e i modi della
melodica come sistema. Quattro istruzioni che erano `[CALC]` **senza** `[LIB]` (o
con la nota «i libri non le nominano») ora hanno la fonte. ⚠️ **La regola «non
forzare una citazione» ha retto:** quando non c'era la fonte non se n'è inventata
una; è arrivata dopo, e il `[CALC]` reggeva già. È la terza conferma di quella
regola, e la più bella: aveva ragione ad aspettare.

### Cosa è cambiato, per istruzione

| istruzione | cosa aggiunge Levine |
|---|---|
| `dominante-alterata`, `modi-minore-melodica` | `[LIB]` per l'alterata, la lidia dominante, il sistema dei modi (cap. 9) — tolta la nota «i libri non le nominano» |
| `scala-ottatonica`, `scala-esatonale` | `[LIB]` cap. 9 (diminished / whole-tone scale harmony) accanto a Smith/Piston |
| `voicing` | la fonte **profonda**: shell cap. 3, rootless cap. 7-8, quartale cap. 13, So What cap. 12, upper structures cap. 14 |
| `armonia-funzionale`, `accordi-di-passaggio`, `dominanti-secondarie`, `armonia-modale` | rimandi di conferma (ii-V-I cap. 2, tritone sub cap. 6, So What cap. 12) |

⚠️ **Non tutto cambia:** prestito, planing, medianti, seste aumentate, ritmo
armonico sono territorio classico (Piston) o di Debussy — Levine non li tratta, e
le loro fonti restano giuste. La revisione le **conferma**, non le tocca. (Il
*Jazz Theory Book* di Levine, più ampio, potrebbe toccarne alcuni: da minare su
domanda, non a tappeto.)

### Il prossimo passo

Invariato: il **comping** — Levine ha il capitolo apposta (da p. ~232), oltre a
`ritmo-armonico` + `voicing`. E *Counterpoint* (Piston) abilita il contrappunto
quando toccherà.

---

## 6-noniesvicies. La forma continua: il comping — 13 settembre 2026

**Seconda faccia della forma.** Dopo il voicing, il **comping** — il ritmo con cui
la mano che accompagna suona gli accordi. `docs/istruzioni/comping.md`, stesso
metodo del voicing (`[CALC]` + un ascolto).

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/comping.md` | il vocabolario: le tre collocazioni del colpo (battere / **anticipato** / dietro), lo **spazio** (rado dove il solista è fitto), il registro; da Levine cap. 21 |
| `MU.comping` (`musica.py`) | ⚠️ **codice nuovo**: una stringa di ritmo per battuta → accordi piazzati sui colpi, voicizzati e condotti; promuove `genera_jazz._spec_comping` a primitiva (thin wrapper su `armonia`) |
| `tools/comping_scritto.py` | il pezzo di confronto: rado/anticipato vs fitto |
| `tests/test_all.py` | `test_comping` + `test_comping_scritto`. Suite **1299 → 1308** |
| `out/COMPING01.XML` | caricato e verificato sul Deluge (non versionato) |

### Il verdetto, e la fonte

`COMPING01` (rado/anticipato vs fitto): **«suona bene, il rado ha spazio e spinta —
approvato»**. Conferma le due mosse — lo **spazio** e la **spinta**
(l'anticipazione) — al primo colpo. `[LIB]` Levine, *The Jazz Piano Book*, cap. 21
«Comping» (p. ~223-234): complementare il solista, «punto medio fra audacia e
ritegno», non pestare nel registro del solista.

### La cosa da sapere: `MU.comping` è un costruttore di spec

⚠️ `MU.comping` **non piazza note per conto suo**: costruisce lo spec e chiama
`armonia()` — la collocazione, il voicing e la condotta vengono da lì.
L'anticipazione è una `x` sull'**ultima** croma (nessun codice speciale). ⚠️
`genera_jazz` **non** è stato forzato ad adottarla (è una coppia controllata):
l'adozione è un cleanup successivo, con la sua verifica.

### Cosa NON rifare

- **non chiudere senza l'ascolto** (metodo `[CALC]` + un ascolto);
- **non forzare `genera_jazz`** ad adottare `MU.comping` ora;
- **non confondere comping e ritmo armonico:** il comping è ogni quanto si
  **colpisce** l'accordo, il ritmo armonico ogni quanto **cambia**.

### Il prossimo passo

Le facce restanti della forma: il **contrappunto** (Piston *Counterpoint*, ora
leggibile via djvu) e la **struttura** lunga (l'`arranger` c'è già). Il
contrappunto è il naturale prossimo.

---

## 6-tricies. La forma continua: il contrappunto — 14 settembre 2026

**Terza faccia della forma.** Dopo il voicing (quali note) e il comping (il ritmo
del colpo), il **contrappunto**: due linee **indipendenti** insieme. La domanda
che decide tutto è una: si sentono come **due** voci, o come **una raddoppiata**?
`docs/istruzioni/contrappunto.md`, stesso metodo (`[CALC]` + un ascolto).

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/contrappunto.md` | il vocabolario: i **quattro moti** (contrario / obliquo / diretto / parallelo), le **tre facce** dell'indipendenza (armonia, ritmo, curva), il solo divieto (5e/8e parallele), la dissonanza che risolve; da Piston, *Counterpoint* (1970), Intro + cap. 5 |
| `MU.contrappunto` (`musica.py`) | ⚠️ **codice nuovo, ma è un ANALIZZATORE, non un costruttore.** Prende due voci già scritte e ne misura il rapporto: intervallo e specie, moto, 5e/8e parallele (errore) e dirette (contate), simultaneità degli attacchi, picchi. `MU.racconta_contrappunto` lo dice a parole (regola 4, solo ASCII). Nuovi: `Verticale`, `Contrappunto`, `TICK_PER_MOVIMENTO` |
| `tools/contrappunto_scritto.py` | il pezzo di confronto: lo stesso tema con due seconde voci — una **dipendente** (terze parallele) e una **indipendente** (contrario/obliquo, ritmo sfasato) |
| `tests/test_all.py` | `test_contrappunto` + `test_contrappunto_scritto`. Suite **1308 → 1324** |

### La cosa da sapere: il codice non compone, misura

⚠️ **`MU.contrappunto` NON scrive una voce.** È la divisione del progetto — *l'AI
decide le note delle due linee, il codice fa i conti sul loro rapporto* — la
stessa di `voci_condotte` per il voicing. Il codice non ha mai composto una nota
di questo progetto (HANDOFF §6-quindecies) e continua a non farlo: qui fa da
**lente**, non da penna.

### La scoperta che dà (di nuovo) ragione al progetto

⚠️ **Piston è anti-dogmatico, e lo dice in una riga** (p. 86, sulle quinte/ottave
dirette): *«non sono state formulate regole confermate dalla pratica dei
compositori; lo studente sviluppi il discernimento, non regole inventate»*. È
esattamente il principio del perimetro (11 settembre): **leggi compositive
generalizzabili non esistono**. Per questo il `[CALC]` **conta** le dirette e non
le condanna, e segnala come errore **solo** le parallele di quinta e ottava — le
uniche che collassano davvero due voci in una (p. 83). Quarta dissonante in due
parti (p. 125), non nel tre-parti: la fonte specifica, e l'istruzione la segue.

### Il verdetto, e la fonte

⚠️ **Verdetto: «suona giusto, approvato»** (14 settembre 2026, caricato come
`CONTRAPPUNTO01`, Rhodes + basso). Il `[CALC]` misurava che la dipendente è tutta
moto diretto/parallelo, 100% di attacchi insieme, picchi coincidenti; la
indipendente 5 contrario + 2 obliquo, 75% insieme, picchi sfasati, **nessuna
delle due** con 5e/8e parallele — e l'orecchio ha **confermato**: la prima passata
suona come una voce raddoppiata, la seconda come due voci. Passa al primo colpo,
come voicing e comping. `[LIB]` Piston, *Counterpoint* (1970), Intro p. 9
(accordo/disaccordo), cap. 5 p. 72-86 (due-parti: moti, parallele, curve).

### Cosa NON rifare

- **non far comporre una voce al codice:** `MU.contrappunto` analizza, non scrive;
- **non chiudere senza l'ascolto** (metodo `[CALC]` + un ascolto);
- **non trasformare Piston in un regolamento:** conta le dirette, non le vieta;
- **non confondere contrappunto e voicing/comping:** quelli lavorano *sotto* una
  melodia; il contrappunto mette **due linee** in rapporto.

### Il prossimo passo

L'ultima faccia della forma: la **struttura** lunga — l'arco del pezzo, le
sezioni, le transizioni (l'`arranger` c'è già; la skill `music-composition` copre
«tutto ciò che dura più di una battuta»). Poi resta, dentro il contrappunto stesso
e **su domanda**: il **tre-e-più parti** (Piston cap. 7-8 — oggi il `[CALC]` guarda
due voci per volta), l'**invertibile** e il **canone** (cap. 9-11).

---

## 6-untrigies. La forma continua: la struttura (mappa di forma) — 14 settembre 2026

**Ultima faccia della forma, prima delle sue tre.** Dopo voicing, comping e
contrappunto — che lavorano **dentro** una o due battute — la **struttura**: come
il materiale si dispone nel tempo. La struttura ha tre facce, e l'utente ha scelto
di partire dalla **mappa di forma** (lo scheletro: dove cadono le sezioni), fra
mappa / arco dinamico / transizioni. `docs/istruzioni/struttura.md`, metodo
`[CALC]` + un ascolto.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/struttura.md` | il vocabolario: le sezioni (intro/A/ponte/out), le **mappe canoniche** (AABA, blues 12, rhythm changes, testa-soli-testa), le lunghezze; la regola che pesa di più (**ripetizione contro sviluppo**). `[LIB]` music-composition `references/form/popular-song-forms.md` + `[MIS]` casella 9 di `jazz.md` |
| `MU.forma` (`musica.py`) | ⚠️ **codice nuovo, thin layer su `arranger.place`.** Stende una mappa (`'A A B A'`) di clip sulla timeline dell'arranger, calcolando dove cade ogni sezione in tick. `battute_per` per le sezioni di lunghezza diversa. `MU.racconta_forma` a parole (regola 4, ASCII). Nuovo tipo `Sezione` |
| `tools/forma_scritto.py` | l'esempio: un **AABA** vero (Rhodes + tromba, A = casa, B = ponte sul IV), steso con `MU.forma`, aperto in arranger view |
| `tests/test_all.py` | `test_forma`. Suite **1324 → 1332** |

### La cosa da sapere: il codice stende, non compone (di nuovo)

⚠️ **`MU.forma` non compone e non crea clip.** Il materiale di ogni sezione lo
scrive l'AI prima; `forma` fa i **conti** — dove cade ogni sezione — e chiama
`arranger.place`. È la stessa divisione di `comping` e `contrappunto`. E due
distinzioni del modello del dispositivo, verificate: una sezione che si **ripete
identica** riusa la **stessa clip** a più posizioni (`place`); una ripetizione
**variata** vuole la clip **bianca** (`arranger.place_unique`) — ed è la faccia
*sviluppo*, non questa.

### La scoperta utile: si suona dall'arranger

⚠️ **La forma è una cosa d'arranger, non di session view.** `A.open_in_arranger`
apre la song in arranger view (verificato sul corpus: `inArrangementView="1"` è lo
stato di una song salvata così): la **timeline è la forma**. Le clip di sessione
restano ferme, e `avvertenze()` lo segnala — ma qui è **atteso**, non un difetto:
non si lanciano a mano, le suona la timeline. È il primo pezzo di questo progetto
che si ascolta dall'arranger e non dai lanci di sessione.

### Il verdetto, e la fonte

⚠️ **Verdetto: «suona giusto, approvato»** (14 settembre 2026, `STRUTTURA01`,
AABA di 16 battute). Il `[CALC]` verificava che le sezioni cadono ai tick di
`A A B A` e che il file è valido; l'orecchio ha **confermato** che la forma si
sente — l'A torna, il ponte contrasta. Passa al primo colpo, come le altre facce.
`[LIB]` music-composition `references/form/popular-song-forms.md`; `[MIS]` casella
9 di `docs/repertori/jazz.md` (AABA 103, blues 81, rhythm changes 19).

### Cosa NON rifare

- **non far comporre la forma al codice:** `MU.forma` stende una mappa decisa
  dall'AI;
- **non usare `place` dove serve `place_unique`:** ripetizione identica vs
  variazione;
- **non chiudere senza l'ascolto** (metodo `[CALC]` + un ascolto);
- **non aspettarsi la session view:** è una forma d'arranger.

### Il prossimo passo

Le **altre due facce della struttura**, su domanda: l'**arco dinamico** — densità e
intensità che salgono al ponte e ricadono sull'ultimo A, **già misurato** (`[MIS]`
casella 9), da spendere sul generatore; e le **transizioni** — turnaround, fill,
stacchi, con le **variazioni** via `arranger.place_unique`. Con questo la priorità
2 (forma) è **coperta nello scheletro**; restano le rifiniture su domanda.

---

## 6-duotrigies. La struttura continua: l'arco dinamico (e il ritmo armonico ascoltato) — 14 settembre 2026

**Seconda faccia della struttura.** Dopo la mappa (dove cadono le sezioni), l'arco
dinamico: **con quanta intensità** ciascuna suona. ⚠️ **Nasce da due richieste in
una:** fare l'arco, e **usare il brano di test anche per provare il ritmo armonico**
— che era chiuso col solo `[CALC]` e non era mai stato ascoltato. Le due cose sono
la stessa: il ritmo armonico è una **leva** dell'arco, e `ritmo-armonico.md` (riga
124) già indicava «il rapporto con la forma lunga» come lavoro di priorità 2.
`docs/istruzioni/arco-dinamico.md`, metodo `[CALC]` + un ascolto.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/arco-dinamico.md` | l'arco **misurato** (`[MIS]` casella 9 di `jazz.md`: A1 rado → ponte culmine → A3 ricade; il ponte è la sola sezione che non respira), steso su **tre leve** che salgono insieme: densità, ritmo armonico, dinamica |
| `MU.dinamica` (`musica.py`) | ⚠️ **codice nuovo**, la leva delle dinamiche: scala le velocity per un fattore, stretto fra `minimo` e 127, **senza mutare** l'originale (così la stessa frase si posa a più livelli). Le altre due leve usano primitive che c'erano già — densità (quante note) e `durata` (ritmo armonico) |
| `tools/arco_scritto.py` | l'esempio: l'AABA della mappa con l'arco steso — A1 rada/piano/lenta, A2 cresce, **B fitta/forte/veloce (2 accordi a battuta)**, A3 ricade |
| `tests/test_all.py` | `test_dinamica` + `test_arco_scritto`. Suite **1332 → 1341** |

### La convergenza: arco e ritmo armonico sono la stessa cosa

⚠️ **Il ponte fa due cose in una: è il culmine dell'arco E raddoppia il ritmo
armonico** (2 accordi a battuta invece di 1). Così `STRUTTURA02` prova, nello stesso
ascolto, l'arco dinamico e il ritmo armonico. È dove vive, nella forma lunga, la
mossa che `ritmo-armonico.md` chiamava «accelerare verso la cadenza». Il ritmo
armonico resta chiuso col `[CALC]` (decisione del 13 settembre); questo è un
**ascolto in più**, dentro la forma, non un cambio di metodo.

### La cosa da sapere: l'arco misurato NON è un motore

⚠️ I numeri della casella 9 dicono **dov'è** il culmine (il ponte) e la **forma**
della salita (radi → fitto → radi), non generano le note. `MU.dinamica` fa
l'aritmetica delle velocity; densità e ritmo armonico sono scelte dell'AI informate
dalla misura. È la regola del 30 agosto: il corpus dà relazioni, non superfici — e
qui la relazione è l'arco, non una distribuzione da campionare.

### Il verdetto, e la fonte

⚠️ **Verdetto: «suona giusto, approvato»** (14 settembre 2026, `STRUTTURA02`). Il
`[CALC]` verificava che sulle tre leve la densità sale al ponte e ricade
(4<8<16>4), il ponte raddoppia il ritmo armonico (A=4, B=8 attacchi), la dinamica
culmina sul ponte; l'orecchio ha **confermato** l'arco — il culmine arriva, il
ritorno si posa — e con esso il **ritmo armonico**, ascoltato per la prima volta
(un `[OSS]` di conferma dentro la forma, non un cambio del metodo `[CALC]`).
`[LIB]` `ritmo-armonico.md` (Piston, *Harmony*, cap. 12); `[MIS]` casella 9 di
`docs/repertori/jazz.md`.

### Cosa NON rifare

- **non trasformare l'arco misurato in un motore** (il corpus dà relazioni);
- **non far salire una leva sola:** il culmine vuole densità + ritmo armonico +
  dinamica insieme;
- **non chiudere senza l'ascolto** (metodo `[CALC]` + un ascolto);
- **non far respirare il ponte alla fine:** è il culmine, tira dritto (`[MIS]`).

### Il prossimo passo

L'ultima faccia della struttura: le **transizioni** — vedi §6-trestrigies, dove
sono state fatte.

---

## 6-trestrigies. La struttura si chiude: le transizioni — 14 settembre 2026

**Terza e ultima faccia della struttura.** Dopo la mappa (dove cadono le sezioni) e
l'arco (con quanta intensità), le **transizioni**: i **giunti** fra le sezioni, e
come si cuciono. ⚠️ **Scelta dell'utente** fra tre primi pezzi (giunti
armonico-melodici + clip bianca / fill di batteria / i tre modi a confronto): il
primo, perché dà a `arranger.place_unique` — la clip bianca, «finora solo
nominata» — il suo primo uso vero, senza aggiungere una batteria.
`docs/istruzioni/transizioni.md`, metodo `[CALC]` + un ascolto.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/transizioni.md` | i **tre modi** della transizione (brusco / rampa / morbido) e la cadenza come punteggiatura del giunto (mezza/ingannevole all'interno, piena per la fine); il vocabolario del giunto — turnaround, pickup, break, perno. `[LIB]` `narrative-and-transitions.md` |
| `MU.variazione` (`musica.py`) | ⚠️ **codice nuovo, thin su `arranger.place_unique`**: fa una copia **bianca** (arranger-only) di una clip di sezione, la piazza a un giunto, la ritorna — lo strumento lo trova da sé. Modificarla non tocca l'originale né le altre ripetizioni. È il meccanismo che rende la clip bianca finalmente usabile |
| `tools/transizioni_scritto.py` | l'esempio: l'AABA con due giunti — un **pickup** che sale e consegna il ponte (rampa), un **turnaround** sull'ultimo A che stringe il ritmo armonico e risolve (morbido) |
| `tests/test_all.py` | `test_variazione` + `test_transizioni_scritto`. Suite **1341 → 1352** |

### La cosa da sapere: la clip bianca varia UNA istanza

⚠️ **La copia è arranger-only (niente `section`): vive solo sulla timeline, non
sporca le scene di session view.** È il modo del dispositivo per variare **un**
giunto — l'ultima battuta di una ripetizione — senza toccare le altre. E si varia
**solo la voce che cambia:** nell'esempio la melodia di A2 (per il pickup) e
l'ultimo A (per il turnaround) sono bianche; A1, B e gli accordi di A2 restano le
sezioni piane. Verificato che modificarla non tocca la sorgente.

### La convergenza (di nuovo): il turnaround è ritmo armonico

⚠️ Il turnaround che chiude l'ultimo A **stringe il ritmo armonico** (Dm7 G7 in una
battuta, poi risolve su Cmaj7): è la stessa mossa di `ritmo-armonico.md`
(«accelerare verso la cadenza»), vista dal giunto. La struttura, l'armonia e il
ritmo si toccano qui.

### Il verdetto, e la fonte

⚠️ **Verdetto: «suona giusto, approvato»** (14 settembre 2026, `STRUTTURA03`). Il
`[CALC]` verificava che il pickup sale e arriva in alto (do5), il turnaround
stringe il ritmo armonico (2 accordi nella battuta 3) e risolve su Cmaj7, le
variazioni sono bianche; l'orecchio ha **confermato** che i giunti cuciono — il
ponte arriva preparato, il ritorno chiude. Passa al primo colpo. `[LIB]`
`references/form/narrative-and-transitions.md`.

### Cosa NON rifare

- **non toccare la clip di sezione per variare un giunto:** la copia è bianca
  apposta — modificando l'originale cambiano tutte le ripetizioni;
- **non copiare tutta la sezione per una voce sola** (la clip bianca è solo per la
  voce che cambia);
- **non chiudere senza l'ascolto** (metodo `[CALC]` + un ascolto).

### Il prossimo passo

⚠️ **Con questo la priorità 2 (forma) è coperta:** voicing, comping, contrappunto,
struttura (mappa, arco, transizioni). ⚠️ **Poi è cominciata la priorità 3, il
ritmo, dal fill** — vedi §6-quattuortrigies. Restano, su domanda dentro la forma:
i **tre modi a confronto**, la transizione **morbida** vera (sovrapposizione), una
primitiva che **alza l'ultimo giro** in automatico (final-chorus elevation).

---

## 6-quattuortrigies. Comincia la priorità 3: il fill — 14 settembre 2026

**Il ritmo, dal fill.** ⚠️ **Scelta dell'utente:** «passa al ritmo, tratteremo i
fill all'interno di quello». Il fill è la **faccia ritmica delle transizioni** — la
battuta in cui la batteria annuncia la sezione nuova — e chiude due lacune
dichiarate: quella di `batteria-jazz.md` («il fill: dove va, quanto dura. Oggi è
una decisione arbitraria») e la battuta «(fill)» vuota di `batteria_scritta.py`.
`docs/istruzioni/fill.md`.

### La convergenza: dove lo dice la forma, cosa lo dice il corpus

⚠️ La casella 9 diceva netto: **«dove va un fill non lo dice il corpus»** — il
dataset consegna i fill staccati da ogni pezzo. **Ora la forma c'è** (priorità 2):
il fill va al **giunto**, e si posa con `MU.variazione` (la clip bianca delle
transizioni). Il **dove** dalla forma, il **cosa** dal corpus. È la ragione per cui
il ritmo viene *dopo* la forma e non prima.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/fill.md` | la firma **misurata** (`[MIS]` casella 9, 51 fill, **2 batteristi** — con la cautela): dura una battuta, ~1,2× più fitto (non il doppio), e la firma NON è la densità ma che **il ride si ferma (20%→3%) e arrivano i tom (10%→29%)**, a volume uguale o minore |
| `MU.controlla_fill` (`musica.py`) | ⚠️ **codice nuovo, un CHECKER non un generatore**: prende `beat` e `fill` (`ruolo -> [Note]`) e segnala se il ride non si ferma, i tom non arrivano, è troppo fitto, è un crescendo. È il ruolo del corpus, «prendere gli errori», come `contrappunto`. Nuovi: `Fill`, `_ruolo_batteria` |
| `tools/fill_scritto.py` | scrive le battute **12 e 24** del blues (i turnaround vuoti di `batteria_scritta.py`) con la firma, e passa `controlla_fill` |
| `tests/test_all.py` | `test_controlla_fill` + `test_fill_scritto` + `test_fill_costruito`. Suite **1352 → 1365** |

### La cosa da sapere: il codice prende gli errori, non compone

⚠️ `MU.controlla_fill` **non genera il fill**: lo scrive l'AI (quali tom, quali
colpi), e il codice fa i conti sulla firma per dire se sta nel corpus. È la
divisione di sempre, e la regola del 30 agosto (il corpus dà relazioni, non
superfici): un fill generato raddoppiando i colpi sarebbe «rumore con la forma
giusta».

### Il verdetto, e cosa manca all'ascolto

⚠️ **Verdetto: «suona giusto, approvato»** (14 settembre 2026, `FILL01`). Il fill
**annuncia** la sezione nuova — il segnatempo tace, i tom scendono al giunto. ⚠️
**Su un kit di RIPIEGO:** i kit in `refs/kits/` sono elettronici (808, CR78) senza
tom; l'unico coi tom è il **TR-808 di `refs/songs/DRUMS1_4.XML`**
(KICK/SNARE/HATC/HATO/TOML/TOMM/TOMH), che **non ha il ride** — il segnatempo è il
charleston. Si è sentita la **struttura** del fill (segnatempo che si ferma, tom
che arrivano), non il timbro jazz. ⚠️ **Un kit acustico coi tom non è in casa**
(l'utente non era sicura di averne, e `/KITS` sulla SD non si elenca via SysEx —
la root sì, quella cartella va in timeout): resta il modo di sentirlo nel suo
suono. La build sta in `fill_scritto.costruisci()`. `[MIS]` casella 9 di
`docs/repertori/jazz.md`.

### Il prossimo passo

Chiudere l'ascolto del fill (kit coi tom + dispositivo). ⚠️ **La reazione — basso e
batteria che reagiscono alla forma — è §6-quinquiestrigies.**

---

## 6-quinquiestrigies. Il ritmo che reagisce: la correzione del difetto d'origine — 14 settembre 2026

**Il cuore della priorità 3, e la chiusura del cerchio.** ⚠️ **Scelta dell'utente:**
«passa al basso e batteria che reagiscono alla forma». È il **difetto d'origine**
del progetto (11 settembre): la batteria «suona **discontinua** rispetto a basso e
piano... e non le puoi **applicare acriticamente**». `docs/istruzioni/reazione.md`.

### I due guasti, e perché serviva la forma prima

⚠️ Il verdetto conteneva **due** difetti: **uniforme** (il basso a 4,00 note per
battuta, deviazione **0,00** — applicato acriticamente) e **scollegata** (varia ma
senza c'entrare — discontinua). Il `walking` aveva già tolto l'uniformità
(deviazione 0,94); mancava il **c'entrare**. E per c'entrare serve qualcosa a cui
reagire: la melodia, il comping, l'**arco** — cioè la forma, che ora c'è. È la
ragione per cui la priorità 3 viene dopo la 2.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/reazione.md` | i **quattro verdetti** (uniforme / scollegata = i guasti; complementa / segue = reagisce) e le **due scale**: la battuta (complementa la melodia, call-and-response) e la sezione (segue l'arco, `[MIS]` casella 9) |
| `MU.reazione` (`musica.py`) | ⚠️ **codice nuovo, un ANALIZZATORE non un generatore**: guarda la densità per battuta della parte (la **deviazione**: sotto 0,75 è piatta = uniforme) e la **correlazione** col riferimento (negativa = complementa, positiva = segue, ~0 con variazione = scollegata). Il ruolo del corpus, «prendere gli errori», come `contrappunto`. Nuovi: `Reazione`, `_pearson`, `_densita_per_battuta` |
| `tools/reazione_scritto.py` | l'esempio: la stessa melodia con due bassi — **uniforme** (4 4 4 4, il difetto d'origine rimesso in scena) e **reattivo** (4 1 4 1, complementa) |
| `tests/test_all.py` | `test_reazione` + `test_reazione_scritto`. Suite **1365 → 1374** |

### La cosa da sapere: reagire NON è riempire

⚠️ Spesso la reazione giusta a una melodia fitta è **tacere**. `MU.reazione`
misura la densità e la correlazione, non «quante note»: una parte che complementa
**cala** dove il riferimento è fitto. E `MU.reazione` non compone — l'AI scrive la
parte, il codice dice se reagisce (regola del 30 agosto: il corpus dà relazioni).

### Il verdetto, e la fonte

⚠️ **Verdetto: «suona giusto, approvato»** (14 settembre 2026, `REAZIONE01`). Il
`[CALC]` misurava che il basso uniforme è `uniforme` (deviazione 0,00, il difetto
d'origine) e il reattivo `complementa` (correlazione −1,00); l'orecchio ha
**confermato**: il basso reattivo respira col tema, l'uniforme suona meccanico. È il
**difetto d'origine del progetto, corretto e sentito**. Vale per la batteria allo
stesso modo (`batteria_scritta.py` lo fa già a mano). `[MIS]` casella 9 di
`docs/repertori/jazz.md`; il difetto d'origine sta in §6-vicies e nel design del 10
settembre.

### Il prossimo passo

Il **resto della priorità 3**, su domanda: la reazione a **più riferimenti**
insieme (il basso rispetto a melodia *e* batteria), l'**interazione** vera oltre la
densità (raccogliere un accento, seguire un fraseggio), i **groove template**
applicati (`GR.profilo` + `MU.applica_groove`, già scritti — il tocco sopra la
reazione), e i **feel** diversi dallo swing (spazzole, terzine). E l'ascolto del
fill nel suo suono (un kit acustico coi tom).

---

## 6-sexiestrigies. Il groove template applicato: il tocco, e la dinamica adattata al kit — 14 settembre 2026

Chiude «il tocco sopra la reazione», l'ultima voce che `reazione.md` lasciava in
«cosa manca». L'infrastruttura c'era da §6-terdecies (`GR.profilo` legge,
`MU.applica_groove` posa): qui diventa **un'istruzione**, con un esempio che è
stato **ascoltato**. E l'ascolto ha trovato un limite che nessun test poteva
vedere.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `docs/istruzioni/groove-template.md` | l'istruzione: cos'è il template, cosa **non** porta (una esecuzione nominata / solo il residuo, non lo swing / non inventa), le **tre trappole** (nome GM ≠ ruolo, il tempo conta perché lo scarto è in tick, le collisioni), come si applica, e **l'adattamento al kit** |
| `MU.rimappa_dinamica` (`musica.py`) | ⚠️ **codice nuovo**: alza il **fondo** della velocity a un pavimento udibile tenendo i **rapporti** (mappa lineare), sull'**intero insieme di voci** insieme. Muta in posto come `applica_groove`. Nato dall'ascolto — vedi sotto |
| `tools/groove_template_scritto.py` | l'esempio: lo **stesso** pattern reattivo, piatto (velocity 80) vs il tocco di `drummer1/session1/49` rimappato. `TOCCO03.XML` sul device, riletto byte per byte |
| `tests/test_all.py` | `test_rimappa_dinamica` + `test_groove_template_scritto`. Suite **1374 → 1386** |

### La cosa da sapere: il template si autodistrugge sul kit sbagliato

⚠️ Prima stesura caricata (`TOCCO02`), verdetto dell'utente: *«la versione col
tocco lascia fuori troppe note, le cancella»*. **Non ne cancellava nessuna** — i
conteggi erano identici (6/6, 6/6, 8/8, 24/24) e il file torna byte per byte dal
device. Era la **velocity**: i fantasmi del rullante (24) e la cassa sfiorata
(42) cadevano **sotto la soglia che il KIT009 — un RX-5 elettronico — dà voce**.
Il tocco misurato, applicato fedelmente, faceva suonare la parte svuotata. È
esattamente la differenza fra `[CALC]` verde e `[OSS]`: **nessun test poteva
vederlo**.

La correzione, scelta dall'utente: **rimappare**. Alzare il fondo a 55 tenendo i
rapporti del batterista (una mappa lineare, su tutte le voci — la dinamica che
conta è quella **di kit**). ⚠️ **Non è ritoccare la misura, è adattarla allo
strumento**, ed è dichiarato. Seconda stesura (`TOCCO03`): *«ok funziona»*.

⚠️ Due note di metodo da tenere:
- **il conteggio ha smentito la parola, non l'orecchio.** «Le cancella» era falso
  alla lettera e vero all'ascolto. Si onora l'osservazione **e** si spiega il
  meccanismo — non l'uno al posto dell'altro (§8: quando dice che non torna, ha
  ragione, sei volte su sei).
- **un difetto trovato implementando:** `racconta_tocco` leggeva il passo dalla
  posizione **già spostata** dallo scarto, e stampava passi e scarti sbagliati.
  Solo la stampa, non il file — ma è la stessa famiglia di «leggere lo stato dopo
  averlo mutato».

### Il verdetto, e la fonte

⚠️ **Verdetto `[OSS]`: «ok funziona»** (14 settembre 2026, `TOCCO03`). Il `[CALC]`
misurava 0 `senza_appoggio`, 0 `collisioni`, e dopo la rimappa niente sotto 55;
l'orecchio ha confermato che il tocco si sente come una **mano**, non un
metronomo, e nessuna nota resta fuori. ⚠️ **Il pavimento 55 è tarato a orecchio,
non misurato**: dipende da come il singolo kit voce le velocity basse, e va
rifatto per ogni kit. `docs/istruzioni/groove-template.md`; il template è di
§6-terdecies.

### Il prossimo passo

Il resto della priorità 3, su domanda: l'**aggancio** (già in
`genera_jazz.py --aggancio`, ma la misura per cui esiste non è ancora riprodotta
all'ascolto, §6-vicies), i **feel diversi dallo swing** (spazzole, terzine), e il
template **fuori dal jazz**.

---

## 6-septiestrigies. L'aggancio: il basso prende il microtiming — 14 settembre 2026

Riprende il punto che §6-vicies aveva lasciato aperto e che l'aggancio come *flag*
non chiudeva: **basso e batteria che si incontrano nel tempo.** La scoperta di
§6-vicies era che il blocco **non è la batteria ma il basso** — quantizzato
esatto, dispersione zero, non può andare incontro a una batteria che il
microtiming ce l'ha. Qui il basso lo prende.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `jtd.microtiming` (`jtd.py`) | ⚠️ **codice nuovo**: la **sequenza** delle deviazioni dal beat di uno strumento in un trio JTD nominato, in ordine. `[OSS]` su quell'esecuzione — mediare tira a zero, come per il groove template |
| `MU.applica_microtiming` (`musica.py`) | ⚠️ **codice nuovo**: posa quella sequenza su una linea scritta, in ordine di tempo, ciclando. Muta in posto |
| `tools/aggancio_scritto.py` | l'A/B: lo **stesso** walking sotto la **stessa** batteria (groove template), passata 1 **quantizzata**, passata 2 col **float** di Rufus Reid (*Bemsha Swing*, 1984). `AGGANCIO01` sul device |
| `docs/istruzioni/aggancio.md` | l'istruzione |
| `tests/test_all.py` | `test_applica_microtiming` + `test_jtd_microtiming` + `test_aggancio_scritto`. Suite **1386 → 1398** |

### La cosa da sapere: la vita sta nella dispersione, non nel lay-back

Misurando sei trii nominati (4/4): il **lay-back mediano** del basso è minuscolo
(0-2 tick, spesso zero alla risoluzione JTD di 10 ms), ma la **dispersione** è
~3-4 tick di float nota per nota — più della batteria. **È il float la vita**, e
un basso quantizzato ha dispersione **zero**. Riprodurre solo la mediana (un
template a 4 valori per posizione) sarebbe stato inutile: la scelta, presa
dall'utente, è **la sequenza reale di un'esecuzione nominata**, non una
distribuzione — un bassista ha un *andamento*, non rumore bianco.

⚠️ **Cosa NON riproduce, e sta scritto nell'istruzione:** la coincidenza 1,60×
(misura 3) resta un numero di **corpus**. Sul generatore la griglia a sedicesimi
la rende tutto-o-niente, e la coincidenza vera vorrebbe basso **e** batteria
dallo **stesso** trio (qui il float è JTD, il template è Groove MIDI: due dischi).
Questo demo mostra una cosa più semplice: **un basso che respira contro un
metronomo.**

### Il verdetto, e la fonte

⚠️ **Verdetto `[OSS]`: «ok funziona, è quasi impercettibile ma va bene»**
(14 settembre 2026, `AGGANCIO01`). L'utente lo ha sentito e approvato, **e ha
detto che è piccolo** — come previsto, e come la posizione nella batteria
(§6-terdecies): il microtiming del basso è sottile. ⚠️ Ne segue una cosa per il
futuro: **il float vale dentro il pieno, non come effetto da mostrare da solo**.
`docs/repertori/jazz.md` casella 5 (misure 3 e 4); il difetto d'origine è in
§6-vicies.

### Il prossimo passo, e una strada ARCHIVIATA

⚠️ **La «coincidenza vera» (riprodurre la misura 3, 1,60×) è archiviata — 15
settembre 2026, su domanda dell'utente: *«a cosa serve realmente?»*.** Tre motivi
che convergono, e stanno per esteso in `docs/istruzioni/aggancio.md`: (1)
l'orecchio ha già votato «quasi impercettibile» — è lo stesso microtiming, non un
suono nuovo; (2) il dato la blocca — la coincidenza dallo stesso trio vorrebbe
basso *e* batteria dalla stessa esecuzione, e solo il JTD ce l'ha, ma con la
batteria in onset **aggregati** (niente velocity né voce), mentre il groove
template è del Groove MIDI, batteria sola: tenere suono *e* coincidenza dallo
stesso disco è impossibile; (3) è replicare una **superficie** misurata, la
trappola vietata il 30 agosto. È la stessa lezione del lettore di partiture: si
archivia col motivo perché una sessione futura non ci ricaschi.

Restano: i **feel diversi dallo swing** (spazzole, terzine); e — se si vuole
spingere l'interazione — **l'interazione a livello di EVENTO** (raccogliere un
accento, seguire un fraseggio), che è udibile, al contrario di un residuo
sotto-tick. L'aggancio come flag (`--aggancio`) va rivisto o buttato: il blocco
non era lì.

---

## 6-octiestrigies. L'interazione a livello di evento — 15 settembre 2026

Chiude «l'interazione vera» che `reazione.md` lasciava in «cosa manca», e lo fa
sul lato **udibile** — al contrario dell'aggancio (microtiming, archiviato perché
impercettibile). L'idea: una parte non fa solo *spazio* all'altra (densità,
`reazione`), ma mette i suoi eventi **dove e quando** l'altra li chiede — il basso
che raccoglie un accento, la batteria che segue un fraseggio.

### Cosa c'è adesso che prima non c'era

| | |
|---|---|
| `MU.interazione` (`musica.py`) | ⚠️ **codice nuovo, un ANALIZZATORE**: presenza di un onset per **movimento** (più fine della battuta di `reazione`). Correlazione negativa = `risponde` (nei buchi), positiva = `insieme` (figura se `cattura` alta, muro se bassa); più `cattura`, la quota degli accenti del riferimento presi insieme. Con `Interazione` e `racconta_interazione` |
| `tools/interazione_scritto.py` | l'A/B: lo **stesso** tema (chiama sui movimenti 1-2, buco sul 3-4), un Rhodes che **pesta** (sul colpo) vs **risponde** (nel buco). `INTERAZIONE01` sul device |
| `docs/istruzioni/interazione.md` | l'istruzione, con le due facce |
| `tests/test_all.py` | `test_interazione` + `test_interazione_scritto`. Suite **1398 → 1410** |

### La cosa da sapere: l'evento coglie ciò che la densità non vede

Le due passate dell'esempio hanno la **stessa densità** (uno stab per battuta),
**collocazione opposta**. `MU.reazione` (densità per battuta) le vede **identiche**
— `uniforme` entrambe — mentre `MU.interazione` le distingue: `insieme` (+0,55,
cattura 100%) contro `risponde` (−0,64, cattura 0%). ⚠️ **È la prova, in un test,
che serviva un secondo analizzatore**: la densità dice *quanto*, l'interazione dice
*dove*, e sono due cose diverse. `reazione` resta il primo filtro; `interazione` è
il secondo.

⚠️ **`insieme` non è un difetto di per sé:** a distinguerlo dal muro è la
`cattura` — alta vuol dire figura presa insieme (musica), bassa vuol dire pestare a
caso sui colpi dell'altro.

### Il verdetto, e la fonte

⚠️ **Verdetto `[OSS]`: «ok funziona»** (15 settembre 2026, `INTERAZIONE01`). La
conversazione si sente contro l'accavallarsi, e — nota per il futuro — **è un
effetto PIENO, non sottile**: la collocazione degli eventi si sente, mentre il
microtiming (aggancio) no. È la conferma che, fra le due strade dell'interazione,
questa era quella da spendere e l'altra da archiviare.
`docs/istruzioni/interazione.md`; il principio `[LIB]` (Riley) è in `batteria-jazz.md`.

### Il prossimo passo

L'interazione a **più di due parti** (il basso rispetto a melodia *e* batteria
insieme: oggi `interazione` e `reazione` guardano una coppia per volta), e i **feel
diversi dallo swing** (spazzole, terzine). Poi, fuori dal ritmo, si sale di
priorità o di repertorio.

---

## 6-novemtrigies. Elettronica / IDM: il pezzo corretto dall'ascolto — 19 settembre 2026

È stata aperta la riga **elettronica / IDM** dell'indice con una scheda propria,
un'istruzione compositiva e un esempio lavorato di 40 battute. Il perimetro è
deliberatamente stretto: IDM astratta e meccanica, polimetro deterministico,
precisione dritta, metallo, glitch discontinuo e un centro tonale minimo. Non è
un tentativo di coprire tutta l'IDM né di replicare la superficie di un artista.

### Cosa c'è adesso

| | |
|---|---|
| `tools/idm_scritto.py` | quattro periodi indipendenti di 5/6/7/11 sedicesimi, tre cellule THUD sullo stesso periodo di 6/16, due gesti glitch, drone Re–La♭ e forma per accrezione/mutazione |
| `docs/istruzioni/idm.md` | vocabolario, vincoli, realizzazione sul Deluge e storia delle quattro versioni |
| `docs/repertori/idm.md` | la nuova scheda: 6 caselle piene, 5 parziali; il limite è dichiarato per territorio, non nascosto sotto l'etichetta “IDM” |
| `docs/MUSICA.md` | la vecchia riga aggregata è diventata una scheda collegata nell'indice |
| `tests/test_all.py` | forma, densità minima, periodi, tre kick realmente diversi, alternanza degli otto glitch, cromatismo e catena synth del drone |

### Le quattro versioni, e ciò che ha deciso l'orecchio

`IDM01` era tecnicamente valida ma musicalmente scarna: prima metà vuota,
interludio ridotto alla sola cassa, glitch troppo radi, cassa identica per tutto
il pezzo; inoltre il drone era muto perché la rampa di cutoff restava sotto la
fascia udibile nel registro grave. `IDM03` ha chiuso ritmo e forma: almeno tre
ruoli nelle prime 28 battute, niente cassa sola, otto glitch alternati e tre
cellule THUD. Verdetto: *«meglio»* e *«il resto va bene»*.

Restava il drone. Alzare il cutoff aveva corretto il silenzio, non la natura del
suono: `Tal Rhodes` usa un **multisample one-shot**. Il suo inviluppo poteva avere
sustain alto, ma la registrazione continuava a decadere come un piano elettrico.
`IDM04` parte invece dal synth vuoto del Deluge: triangolo + `analogSaw` a −7
cent, unisono 2 (`detune 5`, `spread 14`), livelli 30/18, ENV1 attacco 12,
sustain 50, release 24. Il filtro continua a muoversi 40→48 e la risonanza
12→30. Verdetto finale: *«ok»*.

⚠️ **La lezione tecnica:** un drone richiede una **sorgente continua**. Note
lunghe, sustain alto e release lungo non trasformano un campione percussivo in
un drone; il filtro cambia lo spettro disponibile, non ricrea l'energia che il
campione ha già perso.

⚠️ **La lezione compositiva:** “sottrarre” non significa lasciare un ruolo solo
senza una funzione. Qui il contrasto funziona quando CLICK e HAT si alternano
sopra una base di almeno tre ruoli. E la ripetizione di periodo non obbliga a
una cassa invariata: THUD-A/B/C mantengono 6/16 ma cambiano attacchi e accento.

### Stato tecnico finale

`IDM04.XML` è stata scritta come nuova versione in
`/SONGS/DelugePal/IDM04.XML`, senza cancellare o sovrascrivere le precedenti.
La rilettura SysEx è byte-identica: SHA-256
`8a37531ec94d286df7c41a780d000ac7bf50bf504257f64313cd3179f8f3ebe9`.
`MU.verifica()` vuota, `MU.avvertenze()` nessuna; suite **1560/1560**.

---

## 7. Punti aperti

> Le **lacune funzionali** — cosa il sistema non sa ancora fare — stanno in
> testa a questo documento, sotto «Il prossimo lavoro». Qui sotto ci sono i
> punti aperti sul *formato* e sulle verifiche mancanti.

- ~~`set_scale()` vuole i nomi inglesi (`D`) mentre `musica.altezza()`
  accetta anche gli italiani (`re`)~~ — **risolto, revisione finale del 15
  agosto**: `song.set_scale()` ora riusa `musica.altezza()` per riconoscere
  lo stesso vocabolario (italiano, inglese, diesis, bemolle), senza
  duplicare il parser. Il giro ha chiuso anche un difetto più subdolo,
  silenzioso: il codice vecchio faceva `root.upper().replace('B', '#')`, e
  un bemolle come `'Ab'` diventava silenziosamente `rootNote 10` (A#)
  invece di `8` (G#) — un semitono sbagliato senza nessun errore. Stesso
  per `'Db'` (dava D#, non C#) e `'Gb'` (dava G#, non F#)
- ~~`row-add` ha probabilmente lo stesso difetto di §3.1 a un livello più
  basso~~ — **c'era davvero, ed è risolto il 16 agosto** (§6-sexies, FINDINGS
  §6-octies). L'intuizione era giusta e anche più grave del previsto: non solo
  `row-add`, ma **ogni clip generata** si apriva con la finestra lontana dalle
  note. `yScroll` governa la clip view di tutti i tipi di clip, con tre unità
  diverse, e ora `fit_clip_scroll_to_notes()` ancora la riga più bassa in fondo
  allo schermo. Tre coppie controllate in `refs/songs/`
- ~~struttura delle istanze di clip nell'arranger~~ — **risolta e verificata
  sul dispositivo il 14 agosto 2026** (FINDINGS §6-ter,
  `tools/delugexml/arranger.py`). Le posizioni non stanno nelle clip ma in un
  attributo `clipInstances` sullo **strumento**, terne esadecimali
  `(pos, length, clipCode)`; `clipCode` è un **indice ordinale** e il bit 31
  sceglie fra `<sessionClips>` e `<arrangementOnlyTracks>`. Lettura provata su
  2116 istanze in 24 song; scrittura provata riproducendo la coppia
  controllata ARR0/ARR1 attributo per attributo, e poi generando un
  arrangiamento nuovo (`ARRTEST`) confermato sul dispositivo.
  Anche le clip "bianche" (senza `section`, bit 31) sono fatte e verificate:
  `arranger.place_unique()`
- **Le sezioni sono scene**, cioè gruppi di lancio, non una proprietà della
  singola clip. Nell'arranger le sezioni **non esistono**: si piazzano istanze
  di clip su tracce di strumento, e la sezione riemerge solo come colore.
  `numRepeats` ha quattro stati (`-2` esclusivo, `-1` non esclusivo, `0`
  infinito, positivo = conteggio), e vale 0 in tutte e 2100 le sezioni del
  corpus. Vedi FINDINGS §6-ter
- **Il tipo di una clip è dichiarato tre volte** — tag dei params, indice
  delle righe, `affectEntire` — e se non concordano il Deluge rifiuta l'intero
  file come corrotto, pur essendo XML valido. Costato un giro sul dispositivo;
  ora lo blocca `song.check_clip_types()`. Vedi FINDINGS §6-quater
- ancora aperta: la tabella dei **colori di sezione**, che il firmware indicizza
  con `defaultClipSectionColours[section]` e che non è stata trovata nel
  sorgente. Va ricavata dal dispositivo
- ~~quale attributo esprime la **lunghezza propria di una noteRow**~~ —
  **trovato nei file il 12 agosto: è `length` sulla `<noteRow>` stessa**, con
  `sequenceDirection` (`pingpong`) come attributo fratello. 197 righe in 60
  clip, distribuite quasi equamente fra righe di synth (108, con `y`) e di kit
  (92, con `drumIndex`): non è una cosa da kit. La lunghezza della riga **può
  superare quella della clip** (clip 384, riga 552), quindi è indipendente, non
  una suddivisione. Nel corpus c1.3.0 c'è un solo esempio (`Qbix.XML`, clip
  `KIT000`: righe da 384, 576 e 504 tick su una clip da 672); gli altri vengono
  da `corpus_versions\`. **Osservato nei file, non ancora verificato sul
  dispositivo** — resta da confermare che produca davvero il poliritmo, e da
  capire cosa succede quando riga e clip non sono in rapporto intero
- ~~formula esatta fra i tre livelli di scala dei parametri~~ — **trovata il
  12 agosto**, ed è un'uguaglianza intera esatta, non una regressione:

      valore_senza_segno = display × 85899345        85899345 = 2³² // 50

  Su 183 101 valori del corpus il 56,7% la soddisfa **al byte**, più un 39,2%
  di estremi speciali (`0x00000000` = 25 al centro, `0x7FFFFFFF` = 50,
  `0x80000000` = 0): **95,9% spiegato senza tolleranze**. In
  `tools/delugexml/params.py`, con `dsong.py params` che stampa i parametri
  nelle unità del display.

  **E una seconda griglia, verificata sul dispositivo.** Il volume di un synth
  portato a 35 sullo schermo ha prodotto `0x34000000` — cioè **interno 90 su
  128**, non `0x33333313` della griglia storica:

      valore = interno × 33554432        33554432 = 2³² // 128
      display = round(interno × 50 / 128)

  Il display mostra 0-50 (confermato: è la scarsa risoluzione per cui il
  firmware ufficiale veniva criticato), ma il firmware community lavora più
  fine. Quindi **passare per il display perde risoluzione**: 129 valori
  interni si schiacciano su 51 mostrati. `internal_of()` e `from_internal()`
  la conservano e sono byte-esatti; `from_display()` scrive sulla griglia
  interna, come fa il dispositivo oggi.

  **I patch cable hanno una scala loro, anch'essa chiusa sul dispositivo.**
  `lfo1 → modulator1Volume` a 30 → `0x26666666` = round(0,3 × 2³¹). Il range
  mostrato è bipolare −50…+50, quindi `+50 = 0x40000000`, metà dell'int32 —
  previsione verificata: su 15 372 valori del corpus il **100,00%** sta entro
  quel limite, e cinque ci cadono esattamente sopra.

  ⚠️ `polarity` nel file **non** è il range dell'interfaccia: il cable misurato
  si dichiara `unipolar` ma sul dispositivo era bipolare. Cosa sia resta ignoto.

  Attenzione: fuori griglia non sono certi *attributi* ma certi *valori* — lo
  stesso `lpfFrequency` è sulla griglia in una song e fuori in un'altra.

  > **Cautela metodologica.** Ho provato a datare le due griglie confrontando
  > le versioni di firmware in `corpus_versions\`: **non funziona**, e la
  > tabella che ne esce è ingannevole. I valori non toccati vengono riportati
  > identici a ogni salvataggio, mentre `firmwareVersion` registra solo
  > l'ultimo: una song del 2021 risalvata oggi si dichiara c1.3.0 e conserva
  > valori di allora. Le statistiche sul corpus non possono datare i singoli
  > valori. L'unica prova valida è muovere **un** parametro e guardare cosa
  > cambia.
- **cosa fa il firmware a una nota che cade FRA le crome**, quando lo swing di
  song è attivo. `song.set_swing()` con `swingInterval` a 1/8 muove la seconda
  di ogni coppia di **crome**; `GR._senza_swing()` modella lo swing come mappa
  lineare a tratti su **tutto** il movimento, e un groove template scrive note
  fra le crome. L'A/B del 24 agosto 2026 (§6-terdecies) **assolve il modello**
  — quattro modelli alternativi a differenza grossa sono esclusi — ma non
  risponde a questa domanda, e la divergenza fra le due letture è massima
  proprio a fase 0,25 e 0,75. Si chiuderebbe con una coppia controllata
  **costruita** a quelle fasi. Il buco noto adiacente è già dichiarato in
  `song.SWING_SCARTO_SORGENTE`.

  ⚠️ **Il 29 agosto 2026 ci si è scritto sopra per la prima volta, e non è
  suonato rotto.** `JAZZ03` porta 12 note su 128 fra le crome — le corse
  dell'assolo, in sedicesimi — e il verdetto è stato *«le corse suonano
  bene»* `[OSS]`. **Non chiude niente:** resta ignoto *cosa* il firmware
  faccia, e quella è l'assenza di un sintomo riferita da un ascoltatore una
  volta sola, non una misura del meccanismo. Cambia però l'urgenza: era una
  ragione per non scrivere sedicesimi, e non lo è più
- **quanto grande debba essere un residuo di posizione perché si senta.** Non è
  una lacuna del Deluge ma del protocollo: gli ascolti del 24 agosto 2026 sono
  **un ascoltatore, nessuna ripetizione, nessuna prova alla cieca**, e
  l'ascoltatore stesso ha dichiarato imprecise le proprie valutazioni. Da lì
  non esce nessuna soglia, e non la darà un ascolto in più — servirebbe un
  esperimento di psicoacustica. Vale la pena saperlo perché la finestra
  **20-40 ms** che `MUSICA.md` dichiara resta `[WEB]` e non è stata né
  confermata né contraddetta
- ~~l'aggregazione per passo del groove template~~ — **chiusa il 26 agosto
  2026** (§6-terdecies). `GR.profilo()` non prende più il passo più vicino:
  sposta il **confine** fra due passi sulla **fase media della voce**, e il
  gesto smette di spezzarsi fra due celle. Il criterio era fissato prima delle
  misure — la linearità sotto traslazione per voce, 0,998 contro 0,808 — e il
  «battere in minoranza» sul charleston passa da 3 esecuzioni su 23 a 0. La
  decisione, i numeri e il fatto che la regola scritta prima selezionasse
  l'altro candidato stanno in `docs/repertori/jazz.md`, «La decisione: il
  taglio si sposta per voce»
- **l'ancoraggio di un gesto ambiguo fra un passo debole e il battere
  accanto.** È il punto che subentra a quello qui sopra, ed è **più piccolo**:
  chiuso lo spezzarsi del gesto, resta indeciso su **quale** dei due passi
  metterlo, perché dai dati soli le due letture sono la stessa cosa e il gesto
  è anzi più vicino al passo debole. A distinguerli c'è solo il metro. Pesa
  **2 celle su 42 esecuzioni** col modo scelto (contro 5 e 0 con gli altri due,
  dove lo zero è impossibile per costruzione). Non si è scritta una regola
  perché avrebbe dovuto pesare il metro contro la distanza senza nessuna
  misura che dica quanto. Il caso è visibile e non silenzioso perché **la cella
  lo dichiara da sé**: porta il gesto (14 colpi) mentre il battere accanto è
  quasi vuoto (1), e ha `|scarto|` oltre mezzo passo — impossibile per
  costruzione con `'vicino'`. ⚠️ **Corretto il 28 agosto 2026:** qui c'era
  scritto che a renderlo visibile fosse `senza_appoggio`. Quello elenca i passi
  che il profilo **non ha**; una cella mal ancorata invece c'è, ed è il suo
  contenuto a essere spostato. Dichiarato in `docs/repertori/jazz.md`, «Il
  limite che resta: l'ancoraggio»
- byte 10 delle note: i valori fra 21 e 127 non spiegati dai 20 gradini di
  probabilità — probabilmente il LATCHING descritto nel manuale
- perché 24 `<section>` quando il manuale ne descrive 12
- MPE nell'XML, mai guardato (il setup usa Exquis in Lower Zone)
- confronto dello schema **fra versioni di firmware**: non è più bloccato, le
  103 song sono state copiate in `corpus_versions\` divise per versione. Resta
  da fare l'analisi vera e propria (`scan_versions.py` è il punto di partenza)

---

## 8. Preferenze di lavoro

Dall'handoff originale, tutte confermate dall'esperienza:

- **approccio incrementale**, un passo verificato alla volta
- **riconoscimento esplicito degli errori**: se qualcosa non torna, dirlo
- **verifica prima di operazioni distruttive**, sempre — la SD contiene lavoro
  personale
- **mai inventare tag, parametri o strutture**: se non è stato osservato in un
  file reale o in una fonte primaria, va dichiarato come ipotesi
- diffidenza verso le fonti deboli su dettagli tecnici — inclusa la
  documentazione community, che sui byte di comando SysEx è **sbagliata**
  (dà 0x06/0x07, i valori giusti sono 0x04/0x05)
- solo firmware community, la retrocompatibilità con quello ufficiale non
  interessa

E tre regole guadagnate sul campo, ognuna pagata:

- **non dedurre dal file cosa fa il dispositivo.** Se la domanda è «il Deluge
  lo accetta?», l'unica risposta valida viene dallo schermo del Deluge.
- **«non sto inventando» non è «ho visto».** Un nome di attributo osservato nel
  posto sbagliato è comunque il posto sbagliato: è così che è nata l'ipotesi
  sbagliata sulla riga MIDI di un kit (FINDINGS §6-septies).
- **l'utente sa cose che i file non dicono.** Le tre correzioni più importanti
  del 16 agosto sono venute da tre sue frasi: che `cents` è il fine tuning, che
  i drum MIDI mancano dal corpus solo perché non li ha mai usati, e che
  l'ordine delle righe di un kit lo decide chi suona. Nessuna delle tre era
  ricavabile dai file — la prima è nel manuale, le altre due no. **Quando dice
  che qualcosa non torna, ha ragione lui**: è successo **sei volte su sei**, e
  ogni volta stavo per chiudere dichiarando fatto.

  La quinta, il 17 agosto, è la più istruttiva perché non l'ho corretta
  subito: avevo appena difeso la mia tabella dell'intervallo di swing con
  un'aritmetica presa dal sorgente. La sua obiezione era una frase sola —
  *«la divisione non dovrebbe essere 8th?»* — senza numeri e senza fonti, e
  aveva ragione. **La sua incredulità vale più della mia derivazione**, e la
  regola operativa che ne discende è: quando dice che non torna, si smette di
  argomentare e si progetta l'esperimento che decide.

  **La sesta, il 24 agosto, è la prima in cui quella regola l'ha eseguita
  lui.** Non ha obiettato a parole: ha **rifatto l'esperimento** — lo stesso
  ascolto a tempo lentissimo — e ha ribaltato una conclusione già scritta,
  perché a 15 BPM lo stesso scarto di 3 tick vale 125 ms invece di 18,75. Poi
  ha **declassato i propri stessi risultati**, dicendo che con un orecchio non
  allenato e senza prove alla cieca da lì non esce nessuna soglia — e aveva
  ragione anche in questo, perché i due ascolti che si stavano confrontando non
  erano nemmeno lo stesso compito percettivo. §6-terdecies.

---

## 9. La pubblicazione — 17 agosto 2026

Il repo è su <https://github.com/PaoloQuaranta/DelugePal>, **GPL-3.0**, con una
storia nuova di un commit solo. I 54 commit precedenti **non erano
pubblicabili**: ognuno porta con sé song scritte dal dispositivo.

### Cosa NON è pubblicato, e perché

| | |
|---|---|
| 130 song (27 in `refs/songs`, 103 in `corpus_versions`) | sono musica di qualcuno |
| preset di kit e synth | vengono da sample pack **a pagamento** |
| **le 16 fixture delle prove controllate** | vedi sotto |
| `docs/SCHEMA_*.md` | inventari generati: le colonne «valori osservati» citano nomi di song, di preset e 43 percorsi `SAMPLES/` |
| `refs/settings/` | la configurazione del dispositivo |
| `to-read/` | 4,8 GB di libri e librerie MIDI di terzi |

⚠️ **Il caso che non era ovvio: le fixture.** Erano state esplicitamente tenute
nel piano, poi la verifica ha mostrato che **una song del Deluge incorpora i
778 parametri di OGNI strumento che usa** — e tutte e 16, più tutti gli 8
`sd_salvati`, contengono la patch a pagamento `SYNTHS/BOD new/BOD2-01-RIGHT-PLACE`.
26 occorrenze.

Neutralizzarle sostituendo la patch è stato **valutato e scartato**:
distruggerebbe proprio ciò che le rende prove, cioè l'essere state scritte dal
dispositivo byte per byte. Un file riscritto da noi non dimostra più niente.

L'unico XML pubblicato è `refs/synths/TEMPL.XML`: è il synth **vuoto**, cioè i
default del firmware, non il lavoro di nessuno.

### Come è protetto

- **`.gitignore` deny-by-default**: tutto sotto `refs/` è escluso e rientra
  solo `TEMPL.XML`. Ripopolare le cartelle dalla SD non può far sfuggire nulla.
- **hook `pre-push`** in `.git/hooks/`: rifiuta il push se un commit contiene un
  `.XML` non previsto, un `.wav`, o roba sotto `corpus_versions/` o `to-read/`.
  Controlla **ogni commit del tratto**, non solo la punta — un file aggiunto e
  poi rimosso resterebbe pubblicato lo stesso. Provato in entrambe le
  direzioni. **Limite: gli hook non sono versionati**, vale su questa macchina.

### La storia vecchia

`D:\DelugePal-storia.bundle` (1,8 MB) contiene **tutti e 54 i commit e i 4
branch**. Verificato clonandolo prima di cancellare l'originale: 54 commit, i
messaggi giusti, le 162 song dentro. Si riapre con:

```
git clone D:\DelugePal-storia.bundle una-cartella
```

### Cosa resta da sistemare

- ~~`SKILL.md` dice «Il progetto sta in `D:\DelugePal`»~~ — **corretto il 30
  agosto 2026**: dichiara che i percorsi sono relativi alla radice e che quel
  path è solo la macchina dell'autore
- ~~l'hook non è versionato~~ — **versionato il 30 agosto 2026** in
  `hooks/pre-push`. ⚠️ **Git non lo installa da sé**: esegue quelli in
  `.git/hooks/`, che non è versionata. Serve una riga, una volta per clone:

      git config core.hooksPath hooks

  Sta scritto nel commento dell'hook stesso e nel README, perché un hook che
  c'è e non gira è peggio di uno che manca: dà l'impressione di una guardia
- ⚠️ **E una terza coda che non era in questa lista**, trovata il 29 agosto
  aggiungendo quattro preset a `refs/`: la tabella `COPPIE_OSSERVATE` di
  `sound.py` era «generata da uno script e poi incollata» — e **lo script non
  era nel repo**. Chi allargava il corpus vedeva `test_patch_cable_tabelle`
  diventare rosso senza modo di rifare la tabella. Ora c'è
  `tools/genera_coppie_cable.py`, che la ri-deriva, dice cosa è cambiato e
  con `--scrivi` la sostituisce. ⚠️ Rigenerarla **incide il corpus locale in
  un file versionato**: va fatto quando il corpus è quello giusto, non ogni
  volta che il test diventa rosso
- il README dichiara i limiti noti, ma `docs/` resta **tutto in italiano** — la
  traduzione è stata valutata e rimandata: ~50 000 parole di prosa più le
  docstring, che sono saggi e non descrizioni di argomenti
