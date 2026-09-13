# La dominante alterata: la tensione dopo la funzione

**A cosa serve.** Hai una **V7 funzionale** che risolve (vedi
[`armonia-funzionale.md`](armonia-funzionale.md)) e vuoi caricarla di **tensione**
— il suono «pieno» del jazz, la dominante che tira più forte perché è più
dissonante. Questa istruzione dice quali alterazioni si aggiungono (♭9, ♯9, ♯11,
♭13) e **quale scala** le fornisce.

È priorità 1 (armonia), il passo **dopo la spina funzionale**: là la funzione,
qui la sua tensione. E raccoglie l'«uso funzionale» che
[`scala-ottatonica.md`](scala-ottatonica.md) e [`scala-esatonale.md`](scala-esatonale.md)
avevano lasciato fuori.

⚠️ **È l'opposto delle due scale simmetriche come colore statico.** Lì ottatonica
ed esatonale *galleggiano* e non risolvono; qui la stessa scala sta **sopra una
dominante che risolve**, e la tensione serve la cadenza. La differenza è se
l'accordo va da qualche parte.

**Cosa ti serve prima di cominciare:** una casa funzionante e la V7 (primaria o
[secondaria](dominanti-secondarie.md)) da colorare.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[CALC]` | calcolo sulle note, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |

⚠️ **Niente `[OSS]`**: come tutta la spina funzionale, l'armonia si chiude col
`[CALC]` (regola precisa, decisione del 13 settembre 2026).

---

## Il principio: le tensioni non cambiano la funzione

`[LIB]` Smith, *Jazz Theory* (4ª ed.), cap. VIII «Functional Harmony», p. 57
(«Tensions and Chord Function»):

> «Aggiungere tensioni a un accordo non ne cambia la funzione. Per esempio, un
> accordo di settima di dominante con ♭9, ♯11 e 13 aggiunti **funziona ancora
> come dominante** nella sua tonalità. [...] più tensioni creano una tendenza
> maggiore dell'accordo a risolvere su un accordo particolare.»

Quindi la tensione **rinforza** la spinta, non la contraddice. `[LIB]` Smith
p. 78 («Outside Playing») racconta che Charlie Parker trattava le tensioni ♭9,
♯9, +11, ♭13 come **materiale melodico** che «non richiede risoluzione»: sono
colore, sopra una dominante che resta dominante.

---

## Il vocabolario: quattro scale per una dominante

Ogni gruppo di tensioni ha la sua scala. Tutte tengono le **note guida** del V7 —
la 3ª (la sensibile) e la 7ª (il tritono) — e cambiano il resto.

| scala | tensioni che dà | il suono |
|---|---|---|
| **alterata** (super-locria) | ♭9, ♯9, ♯11, ♭13 — **tutte** | la dominante più tesa, il «7alt» |
| **lidia dominante** | ♯11 (con 9 e 13 **naturali**) | brillante, aperto — nessun ♭ |
| **ottatonica HW** | ♭9, ♯9, ♯11, 13 | simmetrica, il dom7♭9 |
| **esatonale** (whole-tone) | ♯5 (♭13), ♯11 — **senza 5ª giusta** | il dom7♯5, vaporoso |

### Le due dal minore melodico

`[CALC]` L'**alterata** e la **lidia dominante** sono **modi della minore
melodica** (già in `song.MODI`), non del maggiore:

- **alterata** = 7º modo — l'alterata di Sol è la minore melodica di La♭ letta da
  Sol. Dà `♭9 ♯9 ♯11 ♭13`: ogni estensione abbassata (o alzata) tranne le note
  guida;
- **lidia dominante** = 4º modo — la lidia dominante di Sol è la minore melodica
  di Re letta da Sol. È un misolidio con la **4ª alzata**: dà il `♯11` ma tiene 9
  e 13 naturali.

`[LIB]` **La fonte è Levine, *The Jazz Piano Book*, cap. 9 «Scale Theory».**
Levine è l'opposto di Smith sull'approccio chord-scale: lo **abbraccia**, e nomina
proprio queste scale. Sull'**alterata**: *«i nomi per la scala alterata: il modo
**super-locrio**... il **settimo modo** [della minore melodica]... la scala
**diminished whole-tone**... per improvvisare sugli accordi di settima di
dominante alterati»* (fig. 9-24). La **lidia dominante** è il **4º modo** della
melodica (Levine, cap. 9).

⚠️ **Una storia di metodo da tenere.** Finché in casa c'era solo Smith — che
**rifiuta** il multi-scala (p. 77-78: «una sola forma di minore») — queste scale
erano `[CALC]` **senza** `[LIB]`, come le [medianti cromatiche](medianti-cromatiche.md):
non si era forzata una citazione. Levine è arrivato dopo (13 settembre 2026) e la
fonte c'era eccome. Il `[CALC]` (rotazioni della melodica, testato) regge lo
stesso — e ora ha la fonte accanto.

### Le due simmetriche, ora funzionali

`[LIB]` Smith, cap. IX «Chord Scale Theory», p. 77: *«la scala diminuita spesso
funziona bene con gli accordi alterati e con gli accordi che hanno tensioni
cromatiche»* — è l'**ottatonica HW** sopra la dominante (dà il dom7♭9). E
l'**esatonale** dà il dom7♯5: `[LIB]` Piston, *Harmony* (5ª ed.), cap. 31, p. 490
(la whole-tone). ⚠️ Sono le stesse scale di
[`scala-ottatonica.md`](scala-ottatonica.md) e
[`scala-esatonale.md`](scala-esatonale.md), qui **sopra una V che risolve**
invece che galleggianti.

---

## Come si stabilisce

1. **parti da una V7 funzionale** che risolve (la casa la fa `armonia-funzionale`);
2. **scegli la tensione** dal colore: tutta tesa → **alterata**; brillante senza
   ♭ → **lidia dominante**; il ♭9 simmetrico → **ottatonica HW**; vaporoso senza
   5ª → **esatonale**;
3. **scrivi le tensioni nella sigla** (`G7alt`, `G7#11`, `G7b9`, `G7#5`), o
   `set_scale` sulla scala per una melodia dentro di essa;
4. **risolvi.** ⚠️ È questo che la distingue dal colore statico: la dominante
   alterata **va a casa** — toglierle la risoluzione la riporta al galleggìo
   delle scale simmetriche.

---

## Come si scrive, materialmente

Le sigle alterate si parsano già (`7b9, 7#9, 7#5, 7#11, 7b13, 7alt`). Per una
melodia *dentro* la scala, `set_scale` sulle scale nuove:

```python
from delugexml import song as S, musica as MU

S.set_scale(doc, 'C', 'maggiore')          # la casa
note = MU.armonia('Dm7 | G7alt | Cmaj7', registro='do3', durata='1/1')
#                    ii    V7alt   I   -- la dominante tesa che risolve

# per improvvisare/scrivere una linea nell'alterata di Sol:
S.set_scale(doc, 'G', 'alterata')          # = La♭ minore melodica, letta da Sol
```

---

## Cosa NON fare

- **non togliere la risoluzione:** senza il ritorno a casa non è una dominante
  alterata, è una scala simmetrica che galleggia (allora vedi
  `scala-ottatonica.md` / `scala-esatonale.md`);
- **non chiamare «modo del maggiore» l'alterata o la lidia dominante:** sono modi
  della **minore melodica**, in `MODI` come intervalli;
- **non ricadere nel «i libri non le nominano»:** era vero con solo Smith, non con
  Levine (cap. 9), che le nomina — l'alterata e la lidia dominante hanno `[LIB]`.

---

## Cosa manca a questa istruzione

- ~~il **ritmo armonico**~~ — c'è, in [`ritmo-armonico.md`](ritmo-armonico.md);
- ~~gli **altri modi della minore melodica**~~ — c'è, in
  [`modi-minore-melodica.md`](modi-minore-melodica.md): il quadro dei sette modi
  (queste due colorano la dominante, le altre cinque altri accordi);
- il **voicing** delle tensioni (upper structure, quartale sulla dominante): è
  priorità 2 (forma).
