# Spendere le misure della casella 5 sul generatore — piano di esecuzione

> **Per chi esegue:** SOTTO-SKILL RICHIESTA: usare
> `superpowers:subagent-driven-development` (consigliata) o
> `superpowers:executing-plans` per eseguire questo piano un compito alla
> volta. I passi usano caselle (`- [ ]`) per il tracciamento.

**Obiettivo:** il basso del generatore jazz varia come varia un walking vero, e
la batteria si aggancia ai suoi eventi fuori griglia; escono due pezzi, la 08 e
la 09, che cambiano **una cosa ciascuna** rispetto alla precedente.

**Architettura:** una funzione di libreria nuova (`MU.linea()`) perché una
linea a durate variabili oggi non è esprimibile; una misura nuova sul JTD che
dice dove cade la nota in più e da quale distribuzione pescare; `walking()` che
pesca quante note fare e le realizza per omissione o aggiunta; e un **secondo
sorteggio** per la batteria che può solo aggiungere colpi, così il flusso
sequenziale esistente non si muove e le due versioni restano confrontabili.

**Stack:** Python 3, solo stdlib. Nessuna dipendenza nuova, nessun pytest — la
suite è `tests/test_all.py` e si lancia da sola.

Il progetto sta in
`docs/superpowers/specs/2026-09-06-spendere-le-misure-design.md`.

## Vincoli globali

Valgono per **ogni** compito, e non si ripetono dentro i passi.

- **Solo stdlib.** Niente `numpy`, niente `pytest`, niente dipendenze nuove.
- **I file si scrivono in LF, senza BOM.** ⚠️ `pathlib.write_text()` su Windows
  traduce `\n` in `\r\n` e due agenti ci sono già cascati: usare `write_bytes()`
  o gli strumenti di edit. Un diff gonfiato è illeggibile, e la revisione è il
  meccanismo su cui poggia questo progetto.
- **I test si lanciano così**, da `D:\DelugePal`:

      .venv/Scripts/python.exe tests/test_all.py

  Un test che non ha materiale su cui girare **solleva `FileNotFoundError`** e
  il lanciatore lo segna SKIP: non è un fallimento. I test nuovi che vogliono
  il JTD seguono questa strada, come `test_jtd_elenco()`.
- **`check(nome, condizione, dettaglio)`** è l'unica asserzione. Niente
  `assert`: la suite deve arrivare in fondo e contare.
- **Ogni soglia sta accanto alla frase che la giustifica**, e le soglie di
  misura stanno in `tools/misura_spartizione.py`, mai in `jtd.py`: il lettore
  non decide niente di musicale.
- **Le costanti musicali nuove portano il grado di prova** — `[MIS]`, `[WEB]`,
  `[OSS]`, `[IPO]` — e la fonte, nel commento `#:` sopra di loro.
- **Un commit per compito**, messaggio in italiano, prima riga sotto i 72
  caratteri, e in coda:

      Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

- **Numeri che vengono dalle misure:** il compito 2 li produce, i compiti 3 e 5
  li usano. Non inventarli, non stimarli: si copiano dall'uscita che il compito
  2 stampa apposta per essere incollata.

## I file

| file | cosa ci si tocca |
|---|---|
| `tools/delugexml/musica.py` | **aggiunge** `linea()` dopo `melodia()`. `melodia()` non cambia |
| `tools/misura_spartizione.py` | **aggiunge** le misure 6 e 7 e le chiama in `main()` |
| `tools/genera_jazz.py` | `walking()` riscritta, `batteria()` con l'aggancio, il confronto stampato, il flag `--aggancio`, e via sei costanti morte |
| `tests/test_all.py` | quattro funzioni di test nuove, in coda al file |
| `docs/repertori/jazz.md` | casella 5: la misura nuova. Casella 11: cosa hanno cambiato la 08 e la 09 |
| `HANDOFF.md` | la sezione nuova |

---

## Compito 1: `MU.linea()`, la linea a durate proprie

**File:**
- Modifica: `tools/delugexml/musica.py` (dopo `melodia()`, che finisce a riga 324)
- Test: `tests/test_all.py` (in coda, prima di `if __name__ == '__main__':`)

**Interfacce:**
- Consuma: `Note`, `ARTICOLAZIONI`, `durata_in_tick()`, `altezza()` — tutti già
  in `musica.py`
- Produce: `MU.linea(eventi, *, velocity=80, articolazione='normale',
  stacco=None) -> dict[int, list[Note]]`, dove `eventi` è un iterabile di
  `(tick: int, altezza: int | str, durata: int | str)`. Il compito 4 la usa per
  scrivere il basso.

- [ ] **Passo 1: scrivere il test che fallisce**

In coda a `tests/test_all.py`, prima del blocco `if __name__`:

```python
def test_musica_linea():
    """`linea()`: ogni nota con la sua posizione e la sua durata.

    E' il caso GENERALE di cui `melodia()` e' la scorciatoia a passo fisso.
    Serve al walking, che dal 6 settembre 2026 tiene una nota per due
    movimenti e ne infila una in piu' su una croma: `melodia()` non lo sa
    esprimere perche' applica UNA durata a tutta la stringa.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    a = MU.linea([(0, 'do4', '1/4'), (96, 're4', '1/4')],
                 velocity=78, articolazione='staccato')
    b = MU.melodia('do4 re4', durata='1/4', velocity=78,
                   articolazione='staccato')
    check('a passo fisso linea() da le stesse note di melodia()', a == b,
          f'{a} vs {b}')

    c = MU.linea([(192, 60, 48), (0, 60, 192), (240, 61, 48)])
    check('le note della stessa altezza stanno nella stessa riga',
          sorted(c) == [60, 61] and len(c[60]) == 2, str(sorted(c)))
    check('e in ordine di posizione anche se date sparse',
          [n.pos for n in c[60]] == [0, 192], str([n.pos for n in c[60]]))
    check('la durata e per nota, non per linea',
          [n.length for n in c[60]] == [163, 41],
          str([n.length for n in c[60]]))

    d = MU.linea([(0, 60, 96)], articolazione='legato')
    check('legato tiene tutta la durata', d[60][0].length == 96,
          str(d[60][0].length))

    for cattivo, perche in (
            ([(-1, 60, 48)], 'tick negativo'),
            ([(0, 60, 0)], 'durata nulla')):
        try:
            MU.linea(cattivo)
            check(f'linea() rifiuta: {perche}', False, 'nessuna eccezione')
        except ValueError:
            check(f'linea() rifiuta: {perche}', True)

    try:
        MU.linea([(0, 60, 48)], articolazione='inventata')
        check('linea() rifiuta un articolazione sconosciuta', False,
              'nessuna eccezione')
    except ValueError:
        check('linea() rifiuta un articolazione sconosciuta', True)
```

- [ ] **Passo 2: lanciarlo e vederlo fallire**

Comando: `.venv/Scripts/python.exe tests/test_all.py`

Atteso: `test_musica_linea` fallisce con
`eccezione AttributeError: module 'delugexml.musica' has no attribute 'linea'`.

- [ ] **Passo 3: implementare**

In `tools/delugexml/musica.py`, subito **dopo** `melodia()` e **prima** di
`SEPARATORE_ACCORDI`:

```python
def linea(eventi, *, velocity: int = 80, articolazione: str = 'normale',
          stacco: int | None = None) -> dict[int, list[Note]]:
    """Da `[(tick, altezza, durata), ...]` alle note, raggruppate per altezza.

    Il caso GENERALE di cui `melodia()` e' la scorciatoia a passo fisso: li'
    una durata sola vale per tutta la stringa e le note stanno su una griglia
    regolare, qui ognuna porta la sua posizione e la sua durata.

    [LACUNA capitolato] Serve da quando il walking ha smesso di fare quattro
    note per battuta (6 settembre 2026): una linea che TIENE una nota per due
    movimenti e ne infila una in piu' su una croma non e' esprimibile a passo
    fisso. `melodia()` resta com'e' -- e' la forma comoda per una frase, e
    nessun chiamante si tocca.

    `altezza` e' un numero di nota MIDI oppure un nome (`'do4'`, `'fa#2'`):
    lo stesso vocabolario di `melodia()`. `durata` e' in tick oppure una
    figura (`'1/8'`), ed e' lo SPAZIO che la nota occupa: quanto suona lo
    decide `articolazione`, come li'. Gli eventi non devono essere in ordine.
    """
    if articolazione not in ARTICOLAZIONI:
        raise ValueError(
            f'articolazione {articolazione!r} sconosciuta, usare '
            f'{sorted(ARTICOLAZIONI)}')
    out: dict[int, list[Note]] = {}
    for tick, alt, durata in eventi:
        if not isinstance(tick, int) or tick < 0:
            raise ValueError(f'tick {tick!r}: la posizione e un intero non '
                             f'negativo, in tick')
        passo = durata_in_tick(durata)
        if stacco is not None:
            lung = max(1, passo - stacco)
        else:
            lung = max(1, round(passo * ARTICOLAZIONI[articolazione]))
        y = alt if isinstance(alt, int) else altezza(alt)
        out.setdefault(y, []).append(
            Note(pos=tick, length=lung, velocity=velocity))
    for note in out.values():
        note.sort(key=lambda n: n.pos)
    return out
```

- [ ] **Passo 4: lanciarlo e vederlo passare**

Comando: `.venv/Scripts/python.exe tests/test_all.py`

Atteso: i sette `check` di `test_musica_linea` PASS, e **nessun test già
esistente cambia esito** — `melodia()` non è stata toccata.

- [ ] **Passo 5: commit**

```bash
git add tools/delugexml/musica.py tests/test_all.py
git commit -m "musica: linea(), il caso generale di melodia() a durate proprie

Una linea che tiene una nota per due movimenti e ne infila una in piu' su
una croma non e' esprimibile a passo fisso, e il walking dal 6 settembre
fa tutt'e due le cose. melodia() resta intatta.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Compito 2: le misure 6 e 7 sul Jazz Trio Database

**File:**
- Modifica: `tools/misura_spartizione.py` (due funzioni nuove, e `main()`)
- Test: `tests/test_all.py`

**Interfacce:**
- Consuma: `JT.battute()`, `JT.elenco()`, `MINIMO_BATTUTE`,
  `FINESTRA_COINCIDENZA` — tutti già nel file
- Produce: **due numeri che i compiti 3 e 5 useranno**: la fase su cui cade la
  nota in più, e `DISTRIBUZIONE_BASSO`, un `dict[int, int]` da incollare in
  `genera_jazz.py`

⚠️ **Il criterio di lettura è fissato nella spec, PRIMA di guardare i dati.**
Non si cambia dopo aver visto il risultato: picco entro ±0,04 da 0,66 → croma
swingata `[MIS]`; entro ±0,04 da 0,50 → croma dritta `[MIS]`; nessun intervallo
oltre il doppio della media → distribuzione piatta, e la posizione diventa
`[WEB]`.

- [ ] **Passo 1: scrivere il test che fallisce**

In coda a `tests/test_all.py`:

```python
def test_misura_fase_e_distribuzione():
    """Le misure 6 e 7 di `misura_spartizione.py`. SALTA senza il corpus.

    Non controlla i VALORI -- quelli sono il risultato, e fissarli qui
    vorrebbe dire deciderli prima di misurarli -- ma le proprieta' che, se
    saltassero, renderebbero sbagliata ogni cifra a valle senza far fallire
    niente: le fasi stanno dentro (0,1), il totale torna, e il filtro sulla
    media seleziona davvero.
    """
    import misura_spartizione as MS                         # noqa: PLC0415
    from delugexml import jtd as JT                         # noqa: PLC0415

    zip_ = ROOT / 'to-read' / 'MIDI' / 'jazz-trio-database-v02.zip'
    if not zip_.exists():
        raise FileNotFoundError(str(zip_))

    with JT.apri(zip_) as z:
        brani = JT.elenco(z, metro=4, curati=True)[:12]

        sei = MS.dove_cade_la_nota_in_piu(z, brani)
        istogramma = sei['istogramma']
        check('la misura 6 ha contato qualcosa', sei['onsets'] > 0,
              str(sei['onsets']))
        check('e il totale dell istogramma torna',
              sum(istogramma.values()) == sei['onsets'],
              f"{sum(istogramma.values())} vs {sei['onsets']}")
        check('le fasi stanno dentro (0, 1)',
              all(0 <= k * MS.PASSO_FASE < 1 for k in istogramma),
              f'{min(istogramma)}..{max(istogramma)}')
        check('il picco e una fase, non un indice',
              0.0 < sei['picco'] < 1.0, f"{sei['picco']:.3f}")

        sette = MS.dentro_una_esecuzione(z, brani)
        check('la misura 7 ha selezionato delle esecuzioni',
              sette['esecuzioni'] > 0, str(sette['esecuzioni']))
        check('la distribuzione e fatta di conteggi interi non negativi',
              all(isinstance(k, int) and k >= 0 and v > 0
                  for k, v in sette['distribuzione'].items()),
              str(sorted(sette['distribuzione'])[:5]))
        check('e le esecuzioni scelte hanno la media dentro la tolleranza',
              all(abs(m - MS.MEDIA_BERSAGLIO) <= MS.TOLLERANZA_MEDIA
                  for m in sette['medie']),
              f"{len(sette['medie'])} esecuzioni")
```

- [ ] **Passo 2: lanciarlo e vederlo fallire**

Comando: `.venv/Scripts/python.exe tests/test_all.py`

Atteso: `test_misura_fase_e_distribuzione` fallisce con
`eccezione AttributeError: module 'misura_spartizione' has no attribute
'dove_cade_la_nota_in_piu'`. ⚠️ Se invece esce SKIP, il corpus non c'è e il
compito non si può fare: fermarsi e dirlo.

- [ ] **Passo 3: implementare le due misure**

In `tools/misura_spartizione.py`, dopo `il_piano()` e prima di `main()`:

```python
#: L'ampiezza degli intervalli dell'istogramma delle fasi. 0,02 vuol dire
#: cinquanta intervalli dentro il movimento: abbastanza fini da distinguere
#: 0,50 da 0,66, abbastanza larghi da non fare rumore su 170 mila onset.
PASSO_FASE = 0.02

#: Il criterio di lettura, FISSATO PRIMA DI MISURARE (spec del 6 settembre
#: 2026). Un picco entro questa distanza da 0,66 dice croma swingata, entro
#: questa da 0,50 dice croma dritta.
TOLLERANZA_PICCO = 0.04

#: La media di note per battuta del corpus, misura 1. La misura 7 tiene le
#: esecuzioni che stanno entro `TOLLERANZA_MEDIA` da qui: sono bassisti che
#: in media fanno quello che fara' il pezzo generato, e la loro distribuzione
#: messa insieme e' quella di UNA esecuzione tipica.
MEDIA_BERSAGLIO = 4.27
TOLLERANZA_MEDIA = 0.2

#: La dispersione DENTRO l'esecuzione, misura 1. La misura 7 controlla di
#: ritrovarla: se la distribuzione selezionata non ce l'ha, e' un risultato da
#: scrivere, non un intoppo da aggirare.
DEVIAZIONE_ATTESA = 1.03
TOLLERANZA_DEVIAZIONE = 0.10


def dove_cade_la_nota_in_piu(z, brani) -> dict:
    """MISURA 6. La FASE degli onset di basso che non stanno su un beat.

    La misura 1 conta QUANTE note ci sono per battuta, non DOVE cadono quelle
    in piu'. Il generatore ha bisogno del dove, e il dato c'e': la posizione
    di ogni onset dentro il movimento in cui cade.

    ⚠️ «Fuori dai beat» ha la stessa definizione della misura 3 -- piu' di
    `FINESTRA_COINCIDENZA` da qualunque beat -- e non una nuova: due misure
    che dicono «fuori griglia» intendendo cose diverse non si possono
    confrontare.
    """
    istogramma = collections.Counter()
    esecutori, usati, tot = set(), 0, 0
    for b in brani:
        d = JT.battute(z, b.fname)
        if len(d.battute) < MINIMO_BATTUTE:
            continue
        usati += 1
        esecutori.add(b.bassista)
        for x in d.battute:
            sul_beat = [bt.istante for bt in x.beat]
            for i, bt in enumerate(x.beat):
                fine = (x.beat[i + 1].istante if i + 1 < len(x.beat)
                        else x.fine)
                if fine <= bt.istante:
                    continue
                for o in x.onsets['bass']:
                    if not bt.istante < o < fine:
                        continue
                    if any(abs(o - t) <= FINESTRA_COINCIDENZA
                           for t in sul_beat):
                        continue
                    istogramma[int((o - bt.istante) / (fine - bt.istante)
                                   / PASSO_FASE)] += 1
                    tot += 1

    print('\nMISURA 6 -- dove cade la nota in piu del basso')
    print(f'   {tot} onset fuori dai beat, {usati} esecuzioni, '
          f'{len(esecutori)} bassisti')
    if not tot:
        return {'istogramma': {}, 'onsets': 0, 'picco': 0.0, 'piatta': True}
    picco = max(istogramma, key=lambda k: istogramma[k])
    centro = (picco + 0.5) * PASSO_FASE
    media = tot / len(istogramma)
    piatta = all(v < 2 * media for v in istogramma.values())
    print('   fase      onset       %')
    for k in sorted(istogramma):
        print(f'   {k * PASSO_FASE:4.2f}   {istogramma[k]:8}   '
              f'{100 * istogramma[k] / tot:5.1f}')
    print(f'   picco a fase {centro:.3f} '
          f'({100 * istogramma[picco] / tot:.1f}% degli onset)')
    if piatta:
        print('   -> PIATTA: nessun intervallo supera il doppio della media, '
              'nessuna posizione preferita. La posizione resta [WEB]')
    elif abs(centro - 0.66) <= TOLLERANZA_PICCO:
        print('   -> CROMA SWINGATA [MIS]: il picco sta entro '
              f'{TOLLERANZA_PICCO} da 0,66')
    elif abs(centro - 0.50) <= TOLLERANZA_PICCO:
        print('   -> CROMA DRITTA [MIS]: il picco sta entro '
              f'{TOLLERANZA_PICCO} da 0,50')
    else:
        print(f'   -> il picco non e ne 0,50 ne 0,66: {centro:.3f}. '
              'E un risultato, va scritto e non aggirato')
    return {'istogramma': dict(istogramma), 'onsets': tot, 'picco': centro,
            'piatta': piatta, 'esecuzioni': usati,
            'esecutori': len(esecutori)}


def dentro_una_esecuzione(z, brani) -> dict:
    """MISURA 7. La distribuzione delle note per battuta di UNA esecuzione.

    ⚠️ QUESTA E' LA DISTRIBUZIONE DA CUI IL GENERATORE DEVE PESCARE, non
    quella della misura 1. La misura 1 mette insieme 1099 esecuzioni: la sua
    dispersione somma quanto varia un bassista dentro un pezzo (1,03) e
    quanto i bassisti differiscono fra loro. Un pezzo generato e' UNA
    esecuzione, e pescare dall'aggregata gli darebbe piu' varieta' di quanta
    ne abbia un bassista vero.

    Selezionate le esecuzioni la cui media sta entro `TOLLERANZA_MEDIA` da
    `MEDIA_BERSAGLIO`, e messe insieme le loro battute.
    """
    conti = collections.Counter()
    medie, esecutori, guardati = [], set(), 0
    for b in brani:
        d = JT.battute(z, b.fname)
        if len(d.battute) < MINIMO_BATTUTE:
            continue
        guardati += 1
        per_battuta = [x.densita['bass'] for x in d.battute]
        media = st.mean(per_battuta)
        if abs(media - MEDIA_BERSAGLIO) > TOLLERANZA_MEDIA:
            continue
        medie.append(media)
        esecutori.add(b.bassista)
        conti.update(per_battuta)

    tot = sum(conti.values())
    print('\nMISURA 7 -- la distribuzione DENTRO una esecuzione')
    print(f'   {len(medie)} esecuzioni su {guardati} hanno la media entro '
          f'{TOLLERANZA_MEDIA} da {MEDIA_BERSAGLIO}, '
          f'{len(esecutori)} bassisti, {tot} battute')
    if not tot:
        return {'distribuzione': {}, 'medie': [], 'esecuzioni': 0}
    campione = [n for n, q in conti.items() for _ in range(q)]
    media, dev = st.mean(campione), st.pstdev(campione)
    print('   note per battuta   battute       %')
    for n in sorted(conti):
        print(f'   {n:16}   {conti[n]:7}   {100 * conti[n] / tot:5.1f}')
    print(f'   media {media:.2f}, deviazione {dev:.2f}')
    dentro = abs(dev - DEVIAZIONE_ATTESA) <= TOLLERANZA_DEVIAZIONE
    print(f'   -> la deviazione {"STA" if dentro else "NON STA"} entro '
          f'{TOLLERANZA_DEVIAZIONE} da {DEVIAZIONE_ATTESA}, che e la '
          'deviazione dentro l esecuzione della misura 1')
    if not dentro:
        print('   ⚠️ va scritto accanto al numero: vorrebbe dire che la '
              'varieta dentro un esecuzione dipende da quanto denso suona')
    print('   da incollare in tools/genera_jazz.py:')
    print(f'   DISTRIBUZIONE_BASSO = {dict(sorted(conti.items()))}')
    return {'distribuzione': dict(conti), 'medie': medie,
            'esecuzioni': len(medie), 'esecutori': len(esecutori),
            'battute': tot, 'media': media, 'deviazione': dev}
```

E in `main()`, dopo la chiamata a `il_piano()` di ciascuna delle due passate,
aggiungere nello stesso punto e con lo stesso schema:

```python
        dove_cade_la_nota_in_piu(z, brani)
        dentro_una_esecuzione(z, brani)
```

⚠️ Vanno chiamate in **tutt'e due** le passate — tutto il corpus e JTD-300 —
come le cinque che ci sono già: se divergono vince JTD-300.

- [ ] **Passo 4: lanciare i test e vederli passare**

Comando: `.venv/Scripts/python.exe tests/test_all.py`

Atteso: i sette `check` nuovi PASS, il resto invariato.

- [ ] **Passo 5: girare la misura intera e salvarla**

Comando:

```bash
.venv/Scripts/python.exe tools/misura_spartizione.py > out/spartizione_jazz.txt
```

Poi **leggere l'uscita** e prendere nota di tre cose:
1. il verdetto della misura 6 (croma swingata / croma dritta / piatta) e la
   fase del picco;
2. se le due passate concordano (se no, **vince JTD-300**);
3. la riga `DISTRIBUZIONE_BASSO = {...}` stampata dalla misura 7, presa dalla
   passata **su tutto il corpus**.

⚠️ Il file `out/` non è versionato: i numeri vanno trascritti dove il compito 3
li usa e nella casella 5 (compito 7), altrimenti si perdono.

- [ ] **Passo 6: commit**

```bash
git add tools/misura_spartizione.py tests/test_all.py
git commit -m "jtd: dove cade la nota in piu, e da quale distribuzione pescare

La misura 1 dice QUANTE note per battuta, non DOVE cadono quelle in piu':
la 6 lo misura sulla fase degli onset fuori dai beat, col criterio di
lettura fissato nella spec prima di guardare.

La 7 e' quella che serve di piu': la distribuzione della misura 1 mette
insieme 1099 esecuzioni e la sua dispersione somma la varieta' di un
bassista e le differenze fra bassisti. Un pezzo generato e' una esecuzione
sola, quindi si pesca dalle esecuzioni che in media fanno 4,27.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Compito 3: `walking()` pesca quante note fare

**File:**
- Modifica: `tools/genera_jazz.py`, `walking()` alle righe 248-289 e le
  costanti sopra di lei
- Test: `tests/test_all.py`

**Interfacce:**
- Consuma: i numeri del compito 2
- Produce: `walking(giro_esteso, forme_basso, rng) -> list[NotaBasso]`, dove
  `NotaBasso` è un `NamedTuple` con `tick: int`, `altezza: int`, `durata: int`.
  ⚠️ **La firma cambia** — prima ritornava `list[int]` — e l'unico chiamante è
  `costruisci()`, che il compito 4 aggiorna.

- [ ] **Passo 1: scrivere il test che fallisce**

In coda a `tests/test_all.py`:

```python
def test_walking_variabile():
    """Il basso non fa piu' quattro note per battuta.

    I bersagli vengono dalla casella 5: distribuzione e deviazione dentro
    l'esecuzione (1,03), silenzi piu' frequenti sul 2 e sul 4. Le tolleranze
    sono larghe apposta -- si controlla che il generatore stia DENTRO la
    distribuzione misurata, non che la riproduca al decimo su 36 battute.
    """
    import random                                           # noqa: PLC0415
    import genera_jazz as GJ                                # noqa: PLC0415

    giro = list(GJ.GIRO_BLUES) * 30       # 360 battute, per avere statistica
    linea = GJ.walking(giro, GJ.FORME_BLUES, random.Random(1))

    check('walking() ritorna NotaBasso, non numeri',
          all(isinstance(n, GJ.NotaBasso) for n in linea), str(linea[0]))
    check('le note sono in ordine di tick',
          all(a.tick < b.tick for a, b in zip(linea, linea[1:])))
    check('nessuna nota esce dal registro del basso',
          all(GJ.BASSO_MIN <= n.altezza <= GJ.BASSO_MAX for n in linea))

    per_battuta = collections.Counter(n.tick // GJ.TICK_BATTUTA for n in linea)
    conti = [per_battuta.get(i, 0) for i in range(len(giro))]
    media = sum(conti) / len(conti)
    dev = statistics.pstdev(conti)
    check('la media sta vicino a 4,27 del corpus', 4.0 <= media <= 4.6,
          f'{media:.2f}')
    check('la deviazione sta vicino a 1,03 e non e zero', 0.8 <= dev <= 1.3,
          f'{dev:.2f}')
    diverse = 100 * sum(1 for c in conti if c != 4) / len(conti)
    check('le battute diverse da quattro sono circa il 60%',
          50 <= diverse <= 70, f'{diverse:.1f}%')

    # i movimenti non attaccati, e su quale cadono
    muti = collections.Counter()
    ticks = {n.tick for n in linea}
    for i in range(len(giro)):
        for m in range(4):
            if i * GJ.TICK_BATTUTA + m * 96 not in ticks:
                muti[m + 1] += 1
    quota = 100 * sum(muti.values()) / (4 * len(giro))
    check('i movimenti non attaccati sono circa il 15%',
          11 <= quota <= 19, f'{quota:.1f}%')
    check('e sono piu frequenti sul 2 e sul 4 che sull 1 e sul 3',
          muti[2] + muti[4] > muti[1] + muti[3],
          f'2+4={muti[2] + muti[4]}, 1+3={muti[1] + muti[3]}')

    # la nota tenuta: chi salta un movimento allunga quella prima
    lunghe = [n for n in linea if n.durata >= 192]
    check('le note tenute ci sono, e durano almeno due movimenti',
          bool(lunghe), f'{len(lunghe)} note')
    check('nessuna nota si sovrappone alla successiva',
          all(a.tick + a.durata <= b.tick
              for a, b in zip(linea, linea[1:])))

    # le note in piu': stanno fuori dal movimento e vanno per grado
    in_piu = [n for n in linea if n.tick % 96]
    check('ci sono note fuori dal movimento', bool(in_piu),
          f'{len(in_piu)} note')
    check('e stanno tutte alla posizione dichiarata',
          all(n.tick % 96 == GJ.TICK_NOTA_IN_PIU for n in in_piu),
          str({n.tick % 96 for n in in_piu}))
    cromatiche = 0
    for n in in_piu:
        seguenti = [x for x in linea if x.tick > n.tick]
        if seguenti and abs(seguenti[0].altezza - n.altezza) == 1:
            cromatiche += 1
    check('e sono approcci cromatici alla nota che viene',
          cromatiche == len(in_piu), f'{cromatiche} su {len(in_piu)}')

    check('a parita di seme la linea e identica',
          GJ.walking(giro, GJ.FORME_BLUES, random.Random(1)) == linea)
```

⚠️ Il test usa `collections` e `statistics`: aggiungerli agli import in testa a
`tests/test_all.py` se non ci sono (`import collections`, `import statistics`).

- [ ] **Passo 2: lanciarlo e vederlo fallire**

Comando: `.venv/Scripts/python.exe tests/test_all.py`

Atteso: fallisce con `eccezione AttributeError: module 'genera_jazz' has no
attribute 'NotaBasso'` — oppure con `TypeError` sulla firma a tre argomenti.

- [ ] **Passo 3: le costanti nuove**

In `tools/genera_jazz.py`, nella sezione «Il basso», **dopo** `BASSO_MIN,
BASSO_MAX` (riga 231):

```python
#: Quante note per battuta, e con che frequenza. ⚠️ NON e' la distribuzione
#: che la casella 5 pubblica: quella mette insieme 1099 esecuzioni e vale
#: 1,33 di dispersione perche' somma la varieta' di un bassista (1,03) e le
#: differenze fra bassisti (0,84). Un pezzo e' UNA esecuzione. Questa viene
#: dalla misura 7 di `tools/misura_spartizione.py`, che tiene le esecuzioni
#: la cui media sta entro 0,2 da 4,27. `[MIS]` sul Jazz Trio Database.
DISTRIBUZIONE_BASSO = {}      # <- la riga stampata dalla misura 7, compito 2

#: Su quale movimento cade il silenzio, in percentuale di beat non attaccati.
#: Misura 2 della casella 5: il basso tace di piu' sul 2 e sul 4. `[MIS]`.
QUOTE_SILENZIO = (16.0, 18.5, 15.0, 17.4)

#: Dove cade la nota in piu' dentro il movimento, in tick su 96. 48 e' la
#: croma dritta, che il firmware poi swinga: con `SWING = 64` il levare va a
#: fase 0,64, cioe' dove la misura 6 ha trovato il picco. ⚠️ Se la misura 6
#: avesse dato un picco lontano da 0,64 questo numero sarebbe diverso -- vedi
#: il passo 4 del compito 3 nel piano.
TICK_NOTA_IN_PIU = 48

#: ⚠️ Un seme a parte per il basso, come `SEME_BATTERIA` per la batteria:
#: cambiare il basso non deve muovere l'assolo, e viceversa.
SEME_BASSO = 34
```

⚠️ `DISTRIBUZIONE_BASSO` va riempita con la riga che la misura 7 ha stampato al
passo 5 del compito 2. Un dizionario vuoto fa fallire i test: è voluto.

- [ ] **Passo 4: controllare `TICK_NOTA_IN_PIU` contro la misura 6**

Lo swing della song sposta il levare: con `SWING = 64` l'ampiezza è
`64 − SWING_CENTRO = 14`, la prima metà del movimento viene dilatata di
`(50 + 14) / 50 = 1,28`, e una croma scritta a metà movimento atterra a fase
`0,5 × 1,28 = 0,64`.

- se il picco della misura 6 sta entro **±0,04 da 0,64**, `TICK_NOTA_IN_PIU`
  resta **48** e non si fa altro;
- se sta altrove, il tick va calcolato perché la nota atterri **dove dice la
  misura**, invertendo la mappa dello swing:

  ```python
  from delugexml import groove as GR
  TICK_NOTA_IN_PIU = round(GR._senza_swing(fase_misurata, 0.64) * 96)
  ```

  e il commento `#:` sopra la costante va aggiornato col numero vero.

- [ ] **Passo 5: implementare `walking()`**

Sostituire `walking()` (righe 248-289) e aggiungere sopra di lei:

```python
class NotaBasso(NamedTuple):
    """Una nota del walking: dove sta, che altezza ha, quanto spazio occupa.

    ⚠️ Fino al 6 settembre 2026 `walking()` ritornava numeri di nota e basta,
    perche' le note erano quattro per battuta a durata fissa. Adesso una nota
    puo' tenere due movimenti e un'altra durare mezzo, quindi la posizione e
    la durata sono parte del risultato e non piu' del chiamante.
    """

    tick: int
    altezza: int
    durata: int


def _approccio(da: int, a: int) -> int:
    """Il vicino cromatico di `a` piu' vicino a `da`, dentro il registro.

    E' l'idioma che il quarto movimento usa da sempre -- `bass.md` della
    skill, «stepwise/chromatic connection», `[WEB]` -- e dal 6 settembre 2026
    lo usa anche la nota in piu'. ⚠️ Che altezza abbia la nota in piu' e' una
    DECISIONE e non una misura: JTD non porta le altezze del basso.
    """
    sopra, sotto = a + 1, a - 1
    scelto = sopra if abs(sopra - da) <= abs(sotto - da) else sotto
    return max(BASSO_MIN, min(BASSO_MAX, scelto))


def _pesca(rng, distribuzione: dict[int, int]) -> int:
    """Un valore pescato dalla distribuzione, dove i pesi sono conteggi."""
    if not distribuzione:
        raise ValueError('DISTRIBUZIONE_BASSO e vuota: va riempita con la '
                         'riga che stampa la misura 7 di misura_spartizione')
    chiavi = sorted(distribuzione)
    return rng.choices(chiavi, weights=[distribuzione[k] for k in chiavi])[0]


def walking(giro_esteso: list[str], forme_basso, rng) -> list[NotaBasso]:
    """La linea di walking, che NON e' quattro note per battuta.

    La costruzione delle altezze e' quella di sempre: fondamentale sul primo
    movimento, due gradi dell'accordo, e sul quarto l'AVVICINAMENTO cromatico
    alla fondamentale che viene. Sopra ci stanno tre cose misurate sul Jazz
    Trio Database (casella 5 di `docs/repertori/jazz.md`):

      - QUANTE note per battuta si pesca da `DISTRIBUZIONE_BASSO`: il 59,7%
        delle battute di un walking vero non ne ha quattro, e il generatore
        ne faceva 4,00 con deviazione 0,00;
      - i movimenti NON attaccati sono il 15,0%, piu' spesso il 2 e il 4
        (`QUOTE_SILENZIO`), e la nota precedente si allunga a coprirli;
      - le note IN PIU' cadono a `TICK_NOTA_IN_PIU` dentro il movimento.

    ⚠️ Due cose qui dentro sono DECISIONI, non misure, perche' JTD porta
    onset senza altezze e senza note-off: che la nota in piu' sia un
    approccio cromatico, e che il movimento saltato sia una nota TENUTA e non
    un silenzio. Stanno scritte accanto al codice che le esegue.
    """
    per_battuta, precedente = [], 41       # fa2, da cui si parte
    for i, casella in enumerate(giro_esteso):
        parti = casella.split('|')
        dopo = giro_esteso[(i + 1) % len(giro_esteso)].split('|')[0]
        prossima = ACCORDI[dopo][0]
        forma = FORME[forme_basso[i % len(forme_basso)]]

        if len(parti) == 2:
            # ⚠️ DUE ACCORDI IN UNA BATTUTA: la fondamentale del secondo va sul
            # TERZO movimento. Ignorarlo darebbe un basso che sta sull'accordo
            # sbagliato per meta' battuta -- sul blues succede solo sul
            # turnaround, sul rhythm changes su ventiquattro battute su
            # trentadue.
            f1, f2 = ACCORDI[parti[0]][0], ACCORDI[parti[1]][0]
            battuta = [_vicino(f1, precedente)]
            battuta.append(_vicino((f1 + forma[1]) % 12, battuta[-1]))
            battuta.append(_vicino(f2, battuta[-1]))
        else:
            fond = ACCORDI[parti[0]][0]
            battuta = [_vicino(fond, precedente)]
            for grado in forma[1:]:
                battuta.append(_vicino((fond + grado) % 12, battuta[-1]))

        # il quarto movimento: cromatico verso la fondamentale che viene
        battuta.append(_approccio(battuta[-1], _vicino(prossima, battuta[-1])))
        per_battuta.append(battuta)
        precedente = battuta[-1]

    # --- quali movimenti attaccano, e dove vanno le note in piu' -----------
    grezzi: list[tuple[int, int]] = []
    aggiunte: list[int] = []                      # i tick delle note in piu'
    for i, altezze in enumerate(per_battuta):
        base = i * TICK_BATTUTA
        quante = _pesca(rng, DISTRIBUZIONE_BASSO)

        # ⚠️ La primissima nota del pezzo non si toglie mai: «tenere la nota
        # precedente» richiede che ce ne sia una, e all'inizio non c'e'.
        vivi = [0, 1, 2, 3]
        candidati = [m for m in vivi if not (i == 0 and m == 0)]
        for _ in range(max(0, 4 - quante)):
            if not candidati:
                break
            scelto = rng.choices(
                candidati, weights=[QUOTE_SILENZIO[m] for m in candidati])[0]
            vivi.remove(scelto)
            candidati.remove(scelto)

        for m in vivi:
            grezzi.append((base + m * 96, altezze[m]))
        for m in rng.sample(vivi, min(max(0, quante - 4), len(vivi))):
            aggiunte.append(base + m * 96 + TICK_NOTA_IN_PIU)

    # --- le altezze delle aggiunte, e le durate ---------------------------
    grezzi.sort()
    per_tick = dict(grezzi)
    for tick in aggiunte:
        seguente = min((t for t in per_tick if t > tick), default=None)
        if seguente is None:
            continue                       # una aggiunta dopo l'ultima nota
        precede = max(t for t in per_tick if t < tick)
        per_tick[tick] = _approccio(per_tick[precede], per_tick[seguente])

    fine = len(per_battuta) * TICK_BATTUTA
    ordinati = sorted(per_tick)
    return [NotaBasso(tick=t, altezza=per_tick[t],
                      durata=(ordinati[k + 1] if k + 1 < len(ordinati)
                              else fine) - t)
            for k, t in enumerate(ordinati)]
```

- [ ] **Passo 6: lanciare i test e vederli passare**

Comando: `.venv/Scripts/python.exe tests/test_all.py`

Atteso: i quattordici `check` di `test_walking_variabile` PASS. ⚠️ Se «la media
sta vicino a 4,27» fallisce, il sospetto è `DISTRIBUZIONE_BASSO` incollata dalla
passata sbagliata: dev'essere quella su tutto il corpus.

- [ ] **Passo 7: commit**

```bash
git add tools/genera_jazz.py tests/test_all.py
git commit -m "il basso non fa piu' quattro note per battuta

Quante ne fa si pesca dalla distribuzione dentro l'esecuzione; i movimenti
non attaccati sono il 15% e stanno piu' spesso sul 2 e sul 4, con la nota
prima che si allunga a coprirli; le note in piu' cadono sulla croma.

Due decisioni dichiarate accanto al codice, perche' JTD porta onset senza
altezze e senza note-off: l'altezza della nota in piu' e' un approccio
cromatico, e il movimento saltato e' una nota tenuta, non un silenzio.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Compito 4: la 08 esce, e la batteria è quella di prima

**File:**
- Modifica: `tools/genera_jazz.py`, `costruisci()` righe 1100-1128, `VERSIONE`
  riga 121, e il changelog nel docstring

**Interfacce:**
- Consuma: `walking()` del compito 3, `MU.linea()` del compito 1
- Produce: `out/JAZZ08.XML`, `out/RHYTHM08.XML`, `out/MODALE08.XML`

- [ ] **Passo 1: spostare il calcolo del basso prima della batteria**

In `costruisci()`, la linea del basso serve **prima** della batteria (il
compito 5 le passerà i passi fuori griglia), ma le tracce vanno aggiunte
nell'ordine di sempre o cambia l'ordine delle tracce nel file.

Subito dopo `giro = _giro_esteso(p)` e **prima** del commento
`# --- batteria ---`:

```python
    # ⚠️ La linea si calcola QUI, prima della batteria, perche' dal 6
    # settembre 2026 la batteria ha bisogno di sapere dove il basso esce
    # dalla griglia. La TRACCIA invece si aggiunge sotto, al suo posto di
    # sempre: l'ordine delle tracce nel file non cambia.
    linea = walking(giro, p.forme_basso, random.Random(SEME_BASSO))
```

- [ ] **Passo 2: scrivere il basso con `linea()`**

Nella sezione `# --- basso walking ---`, sostituire le tre righe che chiamano
`walking()` e `MU.melodia()` con:

```python
    note = MU.linea([(n.tick, n.altezza, n.durata) for n in linea],
                    articolazione='staccato', velocity=78)
    rapporti.append(MU.scrivi(doc, clip_basso, note))
```

- [ ] **Passo 3: la versione, e il changelog**

`VERSIONE = 8`, e in cima al changelog nel docstring del modulo:

```
#:   08  6 settembre 2026. IL BASSO SPENDE LA CASELLA 5: quante note per
#:       battuta si pesca dalla distribuzione misurata invece di essere
#:       sempre quattro, il 15% dei movimenti non attacca (piu' spesso il 2
#:       e il 4) e la nota prima si allunga, e le note in piu' cadono sulla
#:       croma come approccio cromatico.
#:       ⚠️ LA BATTERIA NON CAMBIA, ed e' verificabile: il confronto con la
#:       07 sta nel compito 4 del piano del 6 settembre.
```

- [ ] **Passo 4: generare i tre pezzi**

```bash
.venv/Scripts/python.exe tools/genera_jazz.py blues
```

Poi lo stesso per `rhythm` e `modale` (i nomi esatti li stampa lo script se si
sbaglia). Atteso su ciascuno: `verifica(): vuota`, e il file scritto in `out/`.

- [ ] **Passo 5: la guardia dell'attribuzione, come test permanente**

⚠️ **È il controllo che rende leggibile il verdetto dell'ascolto.** La batteria
della 08 deve essere identica a quella della 07: se non lo è, il flusso
sequenziale del sorteggio si è mosso e il compito va rifatto, non aggirato.

Non un comando usa-e-getta: un test, perché la stessa guardia serve alla 09
contro la 08. In coda a `tests/test_all.py`:

```python
def _righe_di_kit(path):
    """Le note della clip di kit di una song, per drum. La clip di kit e'
    quella le cui righe portano `drumIndex` invece di `y`."""
    doc = parse_file(path)
    for _, clip in S.clips(doc):
        righe = S.note_rows(clip)
        if righe and righe[0].get('drumIndex') is not None:
            return {r.get('drumIndex'): S.read_notes(r) for r in righe}
    raise ValueError(f'{path}: nessuna clip di kit')


def test_jazz08_ha_la_batteria_della_07():
    """La 08 cambia il basso e NIENT'ALTRO. SALTA senza i pezzi generati.

    ⚠️ E' la guardia dell'attribuzione: se la batteria si muovesse, il
    verdetto dell'ascolto sulla 08 non parlerebbe piu' del solo basso. `out/`
    non e' versionato, quindi il test salta per chi non ha generato i pezzi.
    """
    a, b = ROOT / 'out' / 'JAZZ07.XML', ROOT / 'out' / 'JAZZ08.XML'
    for x in (a, b):
        if not x.exists():
            raise FileNotFoundError(str(x))
    sette, otto = _righe_di_kit(a), _righe_di_kit(b)
    check('la 08 ha le stesse righe di batteria della 07', sette == otto,
          'diverse: ' + str([d for d in sette
                             if sette[d] != otto.get(d)]))
```

Comando: `.venv/Scripts/python.exe tests/test_all.py`

Atteso: **PASS**. Se FAIL, il dettaglio dice quali drum divergono, e la causa
è quasi certamente una chiamata a `rng` aggiunta o spostata dentro il ciclo di
`batteria()`.

- [ ] **Passo 6: commit**

```bash
git add tools/genera_jazz.py
git commit -m "JAZZ08: il basso vario nel pezzo, e la batteria intatta

costruisci() calcola la linea prima della batteria (che nella 09 dovra'
sapere dove il basso esce di griglia) ma aggiunge le tracce nell'ordine di
sempre, e scrive il basso con MU.linea() perche' melodia() non sa esprimere
durate diverse.

La batteria della 08 e' identica a quella della 07: e' la guardia che rende
attribuibile il verdetto dell'ascolto.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Compito 5: l'aggancio della batteria, e la 09

**File:**
- Modifica: `tools/genera_jazz.py` — `batteria()` righe 1057-1091, le costanti
  della sezione batteria, `main()` per il flag
- Test: `tests/test_all.py`

**Interfacce:**
- Consuma: `walking()` (compito 3), `_voce_dal_profilo()` invariata
- Produce: `batteria(p, prof, fuori_griglia=None)`, dove `fuori_griglia` è un
  `dict[int, set[int]]` battuta → passi; `out/JAZZ09.XML`

- [ ] **Passo 1: scrivere il test che fallisce**

```python
def test_aggancio_batteria():
    """L'aggancio puo' solo AGGIUNGERE colpi, e solo dove il basso esce.

    ⚠️ E' la proprieta' su cui poggia l'attribuzione: se il sorteggio di base
    si muovesse, la 09 differirebbe dalla 08 dappertutto invece che solo
    dove c'e' l'aggancio, e il verdetto dell'ascolto non direbbe piu' niente.
    """
    import genera_jazz as GJ                                # noqa: PLC0415
    from delugexml import groove as GR                      # noqa: PLC0415

    base = ROOT / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
    if not base.exists():
        raise FileNotFoundError(str(base))
    prof = GR.profilo(base, GJ.BLUES.esecuzione)

    senza = GJ.batteria(GJ.BLUES, prof)
    check('senza eventi fuori griglia la batteria e quella di sempre',
          GJ.batteria(GJ.BLUES, prof, {}) == senza)

    battute = len(GJ.BLUES.giro) * GJ.GIRI
    tutti = {b: {2, 6, 10, 14} for b in range(battute)}
    con = GJ.batteria(GJ.BLUES, prof, tutti)

    da_drum = lambda uscita: {d: {n.pos for n in note} for d, note, _ in uscita}
    prima, dopo = da_drum(senza), da_drum(con)
    check('l aggancio non toglie mai un colpo',
          all(prima[d] <= dopo.get(d, set()) for d in prima),
          str({d: len(prima[d] - dopo.get(d, set())) for d in prima}))
    check('e ne aggiunge almeno uno',
          sum(len(dopo[d] - prima.get(d, set())) for d in dopo) > 0,
          str(sum(len(dopo[d] - prima.get(d, set())) for d in dopo)))

    passi_leciti = {2, 6, 10, 14}
    nuovi = [pos for d in dopo for pos in dopo[d] - prima.get(d, set())]
    check('i colpi in piu stanno solo sui passi del basso',
          all((pos % GJ.TICK_BATTUTA) // 24 in passi_leciti for pos in nuovi),
          str({(p % GJ.TICK_BATTUTA) // 24 for p in nuovi}))

    check('e a parita di seme l aggancio e riproducibile',
          da_drum(GJ.batteria(GJ.BLUES, prof, tutti)) == dopo)

    p = 0.30
    atteso = min(1.0, 0.52 * p / (1 - p))
    check('p_extra porta la probabilita complessiva a 1,52 p',
          abs((p + (1 - p) * atteso) - 1.52 * p) < 1e-9,
          f'{p + (1 - p) * atteso:.4f} vs {1.52 * p:.4f}')
    check('e ha il tetto a 1 quando p e alta',
          GJ._probabilita_aggancio(0.8) == 1.0,
          str(GJ._probabilita_aggancio(0.8)))
```

- [ ] **Passo 2: lanciarlo e vederlo fallire**

Comando: `.venv/Scripts/python.exe tests/test_all.py`

Atteso: `eccezione TypeError: batteria() takes 2 positional arguments but 3
were given`.

- [ ] **Passo 3: togliere le sei costanti morte**

In `tools/genera_jazz.py` cancellare `RIDE` (riga 915), `PEDALE` (920), `CASSE`
(924), `CASSA_PER_BATTUTA` (930), `RULLANTI` (937), `RULLANTE_PER_BATTUTA`
(945) **coi loro commenti**: sono i pattern scritti a mano rimasti dalla
versione 07, quando il disegno è passato al profilo, e non li usa nessuno.

⚠️ `FILL` e `FILL_BATTUTE` (righe 953-966) **restano**: quelli sono usati.

Controllo prima di cancellare:

```bash
grep -n "RIDE\b\|PEDALE\|CASSE\|CASSA_PER_BATTUTA\|RULLANTI\|RULLANTE_PER_BATTUTA" tools/genera_jazz.py
```

Atteso dopo la cancellazione: resta solo `'ride': 'RIDE'` dentro `VOCI` e
`'RIDE': '...'` dentro `FILL`, che sono nomi di drum e non le costanti tolte.

- [ ] **Passo 4: implementare l'aggancio**

Nella sezione batteria, dopo `TENUTI`:

```python
#: Quante volte piu' del caso un colpo di batteria cade insieme a un onset di
#: basso fuori griglia: 30,6% osservato contro 20,1% atteso, a 20 ms, su
#: 170 394 onset. Casella 5, misura 3. `[MIS]`, e confermato su JTD-300
#: (1,51x). ⚠️ Il corpus da' il RAPPORTO, non il meccanismo: usarlo come
#: moltiplicatore di probabilita' e' una decisione.
RAPPORTO_AGGANCIO = 1.52

#: ⚠️ Un seme a parte, e uno stato per cella. E' il punto su cui poggia
#: l'attribuzione: il sorteggio di base NON si tocca -- toccarlo, anche solo
#: cambiandone lo schema, sposterebbe ogni estrazione successiva e la
#: batteria della 09 non sarebbe piu' confrontabile con quella della 08.
SEME_AGGANCIO = 55


def _probabilita_aggancio(p: float) -> float:
    """La probabilita' del SECONDO sorteggio, dato il profilo.

    Il primo sorteggio mette il colpo con probabilita' `p`. Perche' quella
    complessiva sia `RAPPORTO_AGGANCIO * p` serve
    `p + (1 - p) * q = 1,52 p`, cioe' `q = 0,52 p / (1 - p)`, col tetto a 1
    che scatta da `p >= 1 / 1,52 = 0,658` in su.
    """
    if p >= 1:
        return 1.0
    return min(1.0, (RAPPORTO_AGGANCIO - 1) * p / (1 - p))
```

E `batteria()` diventa:

```python
def batteria(p, prof, fuori_griglia=None) -> list[tuple[str, list, dict]]:
    """Le righe di batteria, tutte le battute, col template posato sopra.

    `fuori_griglia` e' battuta -> i passi su cui il BASSO ha una nota fuori
    dai movimenti. Dove ce n'e' una, la batteria ha 1,52 volte piu'
    probabilita' di colpire: e' la misura 3 della casella 5, l'unico punto in
    cui il corpus dice che i due si rispondono davvero -- nella densita' per
    battuta non lo fanno (+0,058, cioe' niente).

    ⚠️ L'aggancio e' un SECONDO sorteggio, indipendente, che puo' solo
    aggiungere colpi: il flusso di `_voce_dal_profilo()` resta identico a
    quello di prima, quindi senza `fuori_griglia` questa funzione da' esattamente
    cio' che dava. E' la guardia che rende attribuibile il verdetto.

    ⚠️ QUALE pezzo del kit si agganci il corpus NON lo puo' dire: gli onset di
    batteria del JTD sono aggregati. Si agganciano tutte le voci, e questa e'
    una decisione dichiarata.
    """
    per_drum: dict[str, list] = {d: [] for d in TENUTI}
    rng = random.Random(SEME_BATTERIA)
    battute = len(p.giro) * GIRI
    fill_battute = {len(p.giro) * (g + 1) - 1 for g in range(GIRI - 1)}
    fuori_griglia = fuori_griglia or {}

    for battuta in range(battute):
        da = battuta * TICK_BATTUTA
        if battuta in fill_battute:
            for drum, pattern in FILL.items():
                per_drum[drum].extend(MU.passi(pattern, da=da))
            continue
        for voce, drum in VOCI.items():
            if drum not in per_drum:
                continue
            pattern = _voce_dal_profilo(prof, voce, rng)
            if pattern:
                pattern = _aggancia(prof, voce, pattern,
                                    fuori_griglia.get(battuta, ()), battuta)
                per_drum[drum].extend(MU.passi(pattern, da=da))

    fuori = []
    for voce, drum in VOCI.items():
        note = per_drum[drum]
        if not note:
            continue
        rapporto = MU.applica_groove(note, prof, dove=voce)
        fuori.append((drum, note, rapporto))
    return fuori
```

E la funzione dell'aggancio, sopra `batteria()`:

```python
def _aggancia(prof, voce, pattern: str, passi, battuta: int,
              minimo: int = 3) -> str:
    """I colpi in piu' dove il basso esce dalla griglia.

    ⚠️ NON inventa passi: gira solo su quelli che il profilo di quel
    batterista contiene davvero, con la stessa soglia `minimo` di
    `_voce_dal_profilo()`. Un passo che lui non suona resta vuoto.
    """
    if not passi:
        return pattern
    per_passo = {x.passo: x for x in prof.passi.get(voce, [])}
    fuori = list(pattern)
    for passo in passi:
        if passo >= len(fuori) or fuori[passo] == 'x':
            continue
        x = per_passo.get(passo)
        if x is None or x.colpi < minimo:
            continue
        p = min(1.0, x.colpi / max(1, prof.battute))
        rng = random.Random((SEME_AGGANCIO, battuta, voce, passo))
        if rng.random() < _probabilita_aggancio(p):
            fuori[passo] = 'x'
    return ''.join(fuori)
```

- [ ] **Passo 5: i passi fuori griglia, e il flag**

Sopra `costruisci()`:

```python
def passi_fuori_griglia(linea) -> dict[int, set[int]]:
    """Battuta -> i passi su cui il basso ha una nota FUORI dai movimenti.

    Il passo e' quello della griglia a sedicesimi che usa la batteria: 16 per
    battuta, 24 tick l'uno. Un passo multiplo di 4 e' un movimento, e non
    conta -- l'aggancio riguarda gli eventi fuori griglia, non i battere.
    """
    fuori: dict[int, set[int]] = {}
    for n in linea:
        passo = (n.tick % TICK_BATTUTA) // 24
        if passo % 4 == 0:
            continue
        fuori.setdefault(n.tick // TICK_BATTUTA, set()).add(passo)
    return fuori
```

In `costruisci()`, la chiamata alla batteria diventa:

```python
    for drum, note, rapporto in batteria(
            p, prof, passi_fuori_griglia(linea) if aggancio else None):
```

con `costruisci(p, prof, aggancio=False)`. In `main()`:

```python
    aggancio = '--aggancio' in sys.argv[1:]
    ...
    doc, rapporti = costruisci(p, prof, aggancio=aggancio)
    ...
    remoto = MU.destinazione(p.nome, 9 if aggancio else VERSIONE)
```

⚠️ Il flag va tolto dalla lista degli argomenti prima di leggere il nome del
pezzo, o `genera_jazz.py blues --aggancio` cercherebbe un pezzo chiamato
`--aggancio`.

E il changelog:

```
#:   09  6 settembre 2026. LA BATTERIA SI AGGANCIA al basso: dove lui ha una
#:       nota fuori griglia, lei ha 1,52 volte piu' probabilita' di colpire.
#:       Rispetto alla 08 cambia SOLO questo, e solo in piu': mai un colpo
#:       in meno. Si scrive con `--aggancio`.
```

- [ ] **Passo 6: lanciare i test e vederli passare**

Comando: `.venv/Scripts/python.exe tests/test_all.py`

Atteso: gli otto `check` di `test_aggancio_batteria` PASS.

- [ ] **Passo 7: generare la 09, e la seconda guardia**

```bash
.venv/Scripts/python.exe tools/genera_jazz.py blues --aggancio
```

Poi lo stesso per `rhythm` e `modale`. La verifica è di nuovo un test, che
riusa `_righe_di_kit()` del compito 4:

```python
def test_jazz09_aggiunge_e_basta():
    """La 09 cambia la batteria e NIENT'ALTRO, e solo in piu'.

    SALTA senza i pezzi generati. ⚠️ Se qualche colpo SPARISCE, il secondo
    sorteggio ha toccato il primo: e' il difetto che tutto l'impianto e'
    fatto per rendere impossibile, e va corretto, non accettato.
    """
    otto, nove = ROOT / 'out' / 'JAZZ08.XML', ROOT / 'out' / 'JAZZ09.XML'
    for x in (otto, nove):
        if not x.exists():
            raise FileNotFoundError(str(x))
    a, b = _righe_di_kit(otto), _righe_di_kit(nove)

    persi, aggiunti = 0, 0
    for d, note in a.items():
        prima = {n.pos for n in note}
        dopo = {n.pos for n in b.get(d, [])}
        persi += len(prima - dopo)
        aggiunti += len(dopo - prima)
    check('la 09 non perde nessun colpo rispetto alla 08', persi == 0,
          f'{persi} persi')
    check('e ne aggiunge', aggiunti > 0, f'{aggiunti} aggiunti')

    doc8, doc9 = parse_file(otto), parse_file(nove)
    basso = lambda doc: [(S.clip_label(c), [(r.get('y'), S.read_notes(r))
                                            for r in S.note_rows(c)])
                         for _, c in S.clips(doc)
                         if S.clip_label(c) == 'Square Saw Bass']
    check('e il basso della 09 e identico a quello della 08',
          basso(doc8) == basso(doc9))
```

Comando: `.venv/Scripts/python.exe tests/test_all.py` — atteso: PASS.

- [ ] **Passo 8: commit**

```bash
git add tools/genera_jazz.py tests/test_all.py
git commit -m "JAZZ09: la batteria si aggancia agli eventi fuori griglia

Un secondo sorteggio, indipendente e con seme proprio, che puo' solo
aggiungere colpi: il flusso di _voce_dal_profilo() non si muove, quindi la
09 differisce dalla 08 solo dove il basso esce di griglia. Con
p_extra = 0,52 p / (1 - p) la probabilita' complessiva viene 1,52 p, che e'
il rapporto misurato.

Quale voce si agganci il corpus non lo puo' dire -- gli onset di batteria
sono aggregati -- quindi si agganciano tutte, ed e' dichiarato.

Via anche sei costanti morte dalla versione 07: i pattern scritti a mano
che il profilo ha sostituito e nessuno usava.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Compito 6: il generatore stampa i numeri del pezzo

**File:**
- Modifica: `tools/genera_jazz.py` — una funzione nuova, chiamata da `main()`

**Interfacce:**
- Consuma: la `linea` e l'uscita di `batteria()`
- Produce: `confronto_col_corpus(linea, righe) -> str`

- [ ] **Passo 1: implementare**

```python
#: Millisecondi per tick al tempo del pezzo: 60000 / (BPM * 96). A 128 BPM
#: sono 4,883 ms, quindi la finestra di 20 ms della casella 5 vale 4,1 tick.
MS_PER_TICK = 60000 / (BPM * 96)


def confronto_col_corpus(linea, righe) -> str:
    """I numeri del pezzo appena scritto, accanto a quelli del corpus.

    Le cifre del corpus vengono dalla casella 5 di `docs/repertori/jazz.md`,
    misure 1, 2 e 3. ⚠️ Il riferimento casuale della coincidenza e' calcolato
    come lo calcola `tools/misura_spartizione.py`: densita' di colpi per
    secondo per l'ampiezza della finestra nei due versi.
    """
    battute = max(n.tick for n in linea) // TICK_BATTUTA + 1
    conti = collections.Counter(n.tick // TICK_BATTUTA for n in linea)
    per_battuta = [conti.get(i, 0) for i in range(battute)]

    ticks = {n.tick for n in linea}
    muti = collections.Counter()
    for i in range(battute):
        for m in range(4):
            if i * TICK_BATTUTA + m * 96 not in ticks:
                muti[m + 1] += 1

    colpi = sorted(n.pos for _, note, _ in righe for n in note)
    fuori = sorted(t for t in ticks if t % 96)
    durata_s = battute * TICK_BATTUTA * MS_PER_TICK / 1000
    densita = len(colpi) / durata_s if durata_s else 0

    fuori_testo = []
    for ms in (20, 30, 50):
        soglia = ms / MS_PER_TICK
        vicini = sum(1 for t in fuori
                     if any(abs(t - c) <= soglia for c in colpi))
        atteso = 100 * min(1.0, densita * 2 * ms / 1000)
        quota = 100 * vicini / len(fuori) if fuori else 0
        fuori_testo.append(f'   entro {ms:2} ms: {quota:5.1f}% contro '
                           f'{atteso:5.1f}% attesi per caso'
                           + (f'   ({quota / atteso:.2f}x)' if atteso else ''))

    r = [f'--- il pezzo, accanto al corpus (casella 5) ---',
         f'   note per battuta: media {st.mean(per_battuta):.2f} '
         f'(corpus 4,27), deviazione {st.pstdev(per_battuta):.2f} '
         f'(corpus 1,03, generatore fino alla 07: 0,00)',
         '   quante note        battute       %']
    d = collections.Counter(per_battuta)
    for n in sorted(d):
        r.append(f'   {n:16}   {d[n]:7}   {100 * d[n] / battute:5.1f}')
    diverse = 100 * sum(1 for c in per_battuta if c != 4) / battute
    r.append(f'   battute diverse da quattro: {diverse:.1f}% (corpus 59,7%)')
    tot_muti = sum(muti.values())
    r.append(f'   movimenti non attaccati: '
             f'{100 * tot_muti / (4 * battute):.1f}% (corpus 15,0%)')
    r.append('   per movimento: ' + ', '.join(
        f'{m}: {100 * muti[m] / battute:.1f}%' for m in (1, 2, 3, 4))
        + '   (corpus 16,0 / 18,5 / 15,0 / 17,4)')
    r.append(f'   note di basso fuori dai movimenti: {len(fuori)}')
    r.extend(fuori_testo)
    r.append('   (corpus: 30,6% contro 20,1% a 20 ms, cioe 1,52x)')
    return '\n'.join(r)
```

⚠️ Vuole `import collections` e `import statistics as st` in testa a
`genera_jazz.py`: aggiungerli se non ci sono.

In `main()`, dopo il blocco `--- rapporti (regola 4) ---`:

```python
    print()
    print(confronto_col_corpus(linea, righe_batteria))
```

`costruisci()` deve quindi restituire anche la linea e le righe di batteria:
cambiarne il ritorno in `(doc, rapporti, linea, righe_batteria)` e aggiornare
il chiamante in `main()`.

- [ ] **Passo 2: lanciarlo e leggere i numeri**

```bash
.venv/Scripts/python.exe tools/genera_jazz.py blues --aggancio
```

Atteso, e **va guardato davvero**: media fra 4,0 e 4,6; deviazione fra 0,8 e
1,3; battute diverse da quattro intorno al 60%; movimenti non attaccati intorno
al 15% e più frequenti sul 2 e sul 4; e il rapporto di coincidenza a 20 ms
**sopra 1**. ⚠️ Se il rapporto a 20 ms fosse ≈1 l'aggancio non sta arrivando
alle note — probabile che gli scarti del groove template lo stiano portando
fuori finestra, e va scritto nella casella 11 invece di essere nascosto.

- [ ] **Passo 3: commit**

```bash
git add tools/genera_jazz.py
git commit -m "il generatore misura il pezzo che ha appena scritto

Note per battuta, movimenti non attaccati e coincidenza basso-batteria,
nella stessa forma in cui la casella 5 da' i numeri del corpus e accanto a
quelli: il confronto si legge senza rifarlo.

Il riferimento casuale della coincidenza e' calcolato come in
misura_spartizione.py, non stimato a occhio.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Compito 7: la documentazione

**File:**
- Modifica: `docs/repertori/jazz.md` — casella 5 e casella 11
- Modifica: `HANDOFF.md` — sezione nuova, e «il prossimo passo»

- [ ] **Passo 1: la casella 5**

Dopo «Il walking non è quattro note per battuta», aggiungere una sezione con
la misura 6 e la misura 7: la distribuzione delle fasi, il verdetto secondo il
criterio fissato prima, il confronto col rapporto di swing della casella 4, e
la distribuzione dentro l'esecuzione con la sua deviazione. Ogni numero col suo
grado di prova, e i conteggi di esecuzioni e bassisti accanto — *un esecutore
non è un repertorio*.

- [ ] **Passo 2: la casella 11**

Una sezione nuova con: cosa ha cambiato la 08, cosa la 09, i numeri stampati
dal generatore accanto a quelli del corpus, e — quando arriva — **il verdetto
dell'ascolto**, `[OSS]`, con le parole dell'utente.

- [ ] **Passo 3: l'handoff**

Sezione `## 6-vicies` col titolo del lavoro e la data, che dica: la misura
nuova e il suo criterio, l'errore di statistica trovato in revisione (pescare
dalla distribuzione aggregata invece che da quella dentro l'esecuzione),
l'errore trovato scrivendo il piano (il sorteggio per cella avrebbe rotto la
guardia che doveva proteggere), le tre decisioni dichiarate, e cosa NON rifare.

Aggiornare «Il prossimo lavoro» in testa: il passo dichiarato il 1 settembre è
stato fatto, e quello dopo è **lo scarto relativo del piano** (+15,3 ms = 3,1
tick), già misurato e non ancora speso.

- [ ] **Passo 4: commit**

```bash
git add docs/repertori/jazz.md HANDOFF.md
git commit -m "casella 5: dove cade la nota in piu, e le misure spese

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Compito 8: l'ascolto

⚠️ **Senza questo il lavoro non è finito: è solo giusto.**

- [ ] **Passo 1: caricare i pezzi**

`out/JAZZ08.XML` e `out/JAZZ09.XML` sul Deluge, in `/SONGS/DelugePal/`, con lo
strumento SysEx del progetto (`tools/dsysex.py`). Verificare che il dispositivo
li apra: `MU.verifica()` vuota non basta, la risposta valida viene dallo
schermo del Deluge.

- [ ] **Passo 2: chiedere due verdetti separati**

Prima la **08** contro la 07 — cambia solo il basso. Poi la **09** contro la
08 — cambia solo la batteria. Chiedere cosa si sente, non se va bene.

- [ ] **Passo 3: scrivere i verdetti dove vanno**

Nella casella 11 con le parole dell'utente e il grado `[OSS]`, e nel changelog
del generatore accanto alla versione. ⚠️ Se un verdetto è negativo, **non
correggere subito**: la regola del progetto è che quando l'utente dice che
qualcosa non torna ha ragione — sei volte su sei — e che si smette di
argomentare e si progetta l'esperimento che decide.

---

## Cosa NON fare, in questo lavoro

- **non toccare il sorteggio sequenziale di `_voce_dal_profilo()`**, in nessun
  modo, nemmeno per «renderlo più pulito»: è la guardia dell'attribuzione;
- **non implementare la correlazione di densità** fra basso e batteria: è
  misurata **nulla** (+0,058), e scriverla sarebbe inventare una regola che il
  corpus nega;
- **non scrivere lo scarto relativo del piano** (+15,3 ms): è la terza
  modifica, e romperebbe l'attribuzione dei due ascolti;
- **non decidere quale pezzo del kit risponde al basso**: gli onset di batteria
  del JTD sono aggregati e il corpus non lo può dire;
- **non aggiustare il criterio della misura 6 dopo aver visto il risultato**: è
  fissato nella spec, ed è metà del suo valore;
- **non usare `pathlib.write_text()`** per scrivere file di testo: su Windows
  traduce `\n` in `\r\n` e rende illeggibile il diff.
