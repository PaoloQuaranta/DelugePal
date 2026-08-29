# Il primo pezzo jazz — progetto

**Data:** 29 agosto 2026
**Perche' adesso:** la casella 11 di `docs/repertori/jazz.md` dice che si
riempie «al primo pezzo jazz corretto dall'utente, e quel momento non e'
ancora venuto». Dopo undici giorni di misure sulla batteria jazz (rami
`groove-midi` e `stimatore-per-passo`, HANDOFF §6-terdecies e
§6-quaterdecies) Deluge Pal non ha mai scritto un pezzo jazz. Questo lavoro
non aggiunge una misura: **spende** quelle che ci sono.

## Cosa si costruisce

Un **blues di 12 battute in fa**, hardbop, medium swing, forma
**tema / assolo / tema = 36 battute**, quattro tracce sul Deluge:
batteria, basso walking, comping, tema.

**A 128 BPM**, e il tempo non e' un gusto: il groove template e' misurato a
124 BPM e l'assolo di riferimento sta a 128. Lo scarto che
`MU.applica_groove()` scrive e' in **tick**, cioe' una frazione di movimento:
scriverlo a un tempo diverso ne conserva la proporzione e ne cambia i
millisecondi. A 128 il template si sposta del 3%; a 140 dell'11%. **Scrivere
a 128 e' l'unico modo di non trasporre niente.**

## L'esito che conta

Non e' il file. E' **cosa l'utente dira' ascoltandolo**, che va scritto nella
casella 11 col protocollo del comune (`Tengo / Cambio / Direzione`) e con la
data. Il pezzo e' lo strumento; la correzione e' il prodotto.

⚠️ **Non e' una coppia controllata e non va usato come misura.** E' un pezzo
di musica sottoposto a un ascoltatore: quello che ne esce e' `[OSS]`, e la
regola del comune — «Un ascolto non e' una misura di percezione» — vale qui
per intero.

## Le fonti, una per una, col grado

| cosa | da dove | grado |
|---|---|---|
| swing | `S.set_swing(doc, 64, figura='1/8')` — valore HARDBOP/BEBOP, casella 10 | `[MIS]` |
| scala di velocity | `GR.scala(base, style='jazz')`, aggregata su esecuzioni e batteristi | `[MIS]` |
| groove template | `GR.profilo(base, 'drummer10/session1/1')` | `[OSS]` su **un** batterista |
| fill | casella 9: 1 battuta, 15,7 colpi/battuta, ride 20,4%→3,3%, tom 9,9%→29,0%, **non piu' forte** | `[MIS]` su 2 batteristi |
| giro armonico | letto da `wjazzd.db`, melid 196 (`Walkin'`, J.J. Johnson) | `[OSS]`, e coincide con il blues standard |
| voicing e alternanza A/B | `assets/jazz-voicings.md` di `music-composition` | `[WEB]` |
| walking bass | `references/instrument-idiom/bass.md` della stessa skill | `[WEB]` |
| forma di tema e assolo | osservata su melid 196, **non copiata** | `[OSS]` su un solista |
| 4/4, griglia a 16 passi | assunto, casella 2 | `[IPO]` |

## Il giro armonico

Letto dalla trascrizione di `Walkin'` (melid 196, F-maj, HARDBOP, SWING,
128 BPM, forma `A12`):

    | F7  | Bb7 | F7  | F7  |
    | Bb7 | Bb7 | F7  | F7  |
    | Gm7 | C7  | F7  | Gm7 C7 |

Blues classico in fa con turnaround ii-V, **nessuna sostituzione bebop**. E'
una griglia armonica generica, non una melodia: si usa tale e quale.

## Il comping, e la lacuna che aggira

⚠️ **La casella 7 dichiara che manca la condotta delle parti**: `MU.armonia()`
costruisce ogni accordo per conto suo e `MU.VOICING` ha **una sola** forma
senza fondamentale, quindi la «B» non esiste e nessun argomento la produce.
Il ripiego che la scheda prescrive e' scrivere **le altezze a mano** con
`MU.accordi()` leggendo i voicing dalla skill. **Si fa cosi'**, e non con
`MU.armonia()` cambiando `voicing=`, che darebbe un'alternanza inventata.

L'alternanza A (3-5-7-9) / B (7-9-3-5) calcolata a mano, registro di mano
sinistra:

| accordo | forma | note (MIDI) |
|---|---|---|
| F7 | A | 57 60 63 67 |
| Bb7 | B | 56 60 62 65 |
| Gm7 | A | 58 62 65 69 |
| C7 | B | 58 62 64 67 |

La condotta che ne esce: `F7 → Bb7` muove −1, **0**, −1, −2; il ii-V-I
`Gm7 → C7 → F7` muove **0**, **0**, −1, −2 e poi −1, −2, −1, **0**. Due note
comuni sul ii-V. **Non sara' questo il difetto del pezzo.**

Il ritmo del comping e' **sincopato**, scritto su una griglia di crome coi
punti dove non si suona (`.` e' una pausa, sia in `melodia()` che in
`accordi()`), e **varia di battuta in battuta**: un comping identico dodici
volte e' la stessa morte formale del primo dub.

## La batteria

Pattern scritto a mano con `MU.passi()` a 16 passi, poi
`MU.applica_groove(note, prof, dove=…)` con il profilo di
`drummer10/session1/1`.

- **ride**: 0-4-6-8-12-14, cioe' spang-a-lang. Sull'esecuzione scelta l'83%
  dei colpi di ride (181 su 219) sta su questi sei passi, e il profilo porta
  la forma dinamica: **127 sui movimenti, 70 sulle crome swingate**;
- **charleston a pedale**: 4 e 12, il 2 e il 4. Velocity 55-56;
- **rullante**: comping irregolare sui passi che il profilo copre. Il profilo
  porta **i colpi fantasma gia' dentro** — velocity 16-18 sui passi 7, 8 e 15
  contro 127 sui passi 4, 10, 12, 14 — quindi non vanno inventati;
- **cassa**: rada. Il profilo da' 96 sul passo 0 e 86 sull'8, e 118-127 sui
  passi 4 e 12, cioe' le bombe.

⚠️ **Ci si discosta dal template che la casella 6 raccomanda, e va scritto
nella scheda.** Lei raccomanda `drummer1/session3/2` perche' e' la piu' lunga
delle `jazz/swing` 4/4. Le due ragioni per non usarla:

1. sta a **185 BPM**, e il pezzo e' a 128. La grandezza che conta non e' la
   differenza fra i BPM ma **quanto vale un tick**: 3,378 ms a 185, 4,883 a
   128, quindi lo stesso scarto in tick uscirebbe **+45% piu' lungo**;
2. su di lei **il nome GM non e' il ruolo musicale** — il disegno del ride sta
   per otto decimi sulla nota 43, che la mappa GM chiama `tom basso`, e
   `dove='ride'` prenderebbe il profilo di un quinto di esecuzione. Su
   `drummer10/session1/1` il ride e' il ride: 219 colpi, spang-a-lang.

⚠️ **`drummer10/session1/1` e' anche l'esecuzione che porta la
stratificazione documentata**: charleston a pedale a −10,75 e −11,17 tick sui
passi 4 e 12, ride a −2,70 e −3,97, cioe' **8,0 e 7,2 tick di divario**. A 128
BPM un tick vale 4,883 ms, quindi il divario vale **39,1 e 35,1 ms**, dentro
la finestra 20-40 ms dichiarata dal comune. Il pezzo la mette davanti a un
orecchio per la prima volta. **Questo non chiude il punto aperto** — servirebbe
un protocollo di psicoacustica, ed e' scritto due volte in `HANDOFF.md` — ma
non e' nemmeno niente.

## Il tema e l'assolo

⚠️ **Originali, non trascritti.** Di `Walkin'` si osserva la **forma**, non si
copiano le note. Le grandezze misurate su melid 196 (434 note, 83 battute):

| grandezza | valore |
|---|---|
| densita' | **5,2 note/battuta** (un ottavo continuo ne farebbe 8) |
| estensione | 23 semitoni, 23 altezze diverse |
| moto | **61% degli intervalli minore o uguale a 2 semitoni**; mediana 2 |
| salti | quarta 17 volte, tritono 8, quinta 6 — rari |
| frasi | 31 buchi da mezza battuta in su, cioe' **una frase ogni ~2,7 battute**; buco mediano 0,75 battute |

Il tema e l'assolo si scrivono rispettando queste grandezze. Il **tema** e'
piu' rado e piu' cantabile dell'assolo, e i due giri di tema sono lo stesso
materiale; l'**assolo** sta alla densita' misurata.

## Sul Deluge

Quattro tracce, **una clip da 36 battute ciascuna**, cosi' basso, comping e
batteria variano nei tre giri invece di ripetersi identici. E' la lezione del
primo dub: formalmente corretto e musicalmente morto.

- `C.add_track(doc, preset, name=…, folder=…, length=…, playing=True)` —
  ⚠️ `playing` vale `False` di default e senza di esso premere play non fa
  partire niente;
- `S.set_swing(doc, 64, figura='1/8')` — il default del firmware swinga le
  semicrome e su una linea di crome non muove niente;
- `A.fit_view(doc)`;
- `MU.verifica(doc)` deve essere **vuota**, o non si carica;
- `MU.avvertenze(doc)` si legge e si riferisce comunque;
- `MU.racconta(doc)` a fine lavoro, coi valori esatti (regola 4);
- destinazione `MU.destinazione('jazz', 1)` produce `/SONGS/DelugePal/JAZZ01.XML`.

## I suoni

**Li nomina l'utente**, perche' la libreria della SD e' sua: da qui `dir` non
risponde su `/KITS` (tre tentativi) e la lista dei preset non e' leggibile per
intero. In locale ci sono solo `refs/kits/CR78FROMMARS.XML`,
`808 Essential.XML`, `808 From Mars.XML` — drum machine — e
`refs/synths/Tal Rhodes.XML`.

⚠️ **Un blues hardbop con una TR-808 non e' un blues hardbop**, e il giudizio
uscirebbe confuso: l'utente direbbe «non suona jazz» per il timbro invece che
per la scrittura, e la casella 11 registrerebbe una trappola che non e' del
generatore.

## Cosa NON si fa

- **non si copiano le note di nessun assolo.** Si osserva la forma e si scrive
  una linea propria;
- **non si usa `MU.armonia()` cambiando `voicing=`** per ottenere
  l'alternanza A/B: non esiste, e sarebbe inventata;
- **non si rigenera** `out/GROOVE0.XML`, `out/GROOVE1.XML`, `out/SWINGA.XML`,
  `out/SWINGB.XML`. Il divieto sta in `HANDOFF.md` e non c'entra con questo
  lavoro, ma questo lavoro tocca lo stesso modulo;
- **non si scrive un file con `pathlib.write_text()` nudo**: su Windows
  traduce il fine riga. Prima di committare, `git diff --stat` e
  `git diff --stat --ignore-cr-at-eol` devono dare lo stesso numero;
- **non si dice «verificato sul dispositivo» avendo ascoltato**, ne' il
  contrario.
