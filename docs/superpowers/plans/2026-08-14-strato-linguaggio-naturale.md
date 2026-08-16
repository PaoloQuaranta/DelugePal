# Strato in linguaggio naturale — piano di implementazione

> **Per chi esegue:** SOTTO-SKILL RICHIESTA: usare `superpowers:subagent-driven-development` (consigliata) oppure `superpowers:executing-plans` per implementare il piano un task alla volta. I passi usano caselle (`- [ ]`) per il tracciamento.

**Obiettivo:** dare a Deluge Pal uno strato che traduce fra lingua musicale e chiamate alla libreria, così che il modello non scriva mai XML.

**Architettura:** un modulo `tools/delugexml/musica.py` con quattro responsabilità separate (raccontare, scrivere note, verbi di suono, cancello di validazione), più una skill `.claude/skills/deluge-pal/` che definisce il protocollo. Nessuna funzione dello strato accetta o produce XML.

**Tecnologie:** Python 3.13, nessuna dipendenza esterna. La libreria `tools/delugexml/` esiste già con 300 test.

**Spec:** `docs/superpowers/specs/2026-08-14-strato-linguaggio-naturale-design.md`

## Vincoli globali

- **PERCORSI ASSOLUTI, SEMPRE.** La working directory della sessione è `D:\`,
  il progetto è `D:\DelugePal`. Un percorso relativo come `docs/MUSICA.md`
  finirebbe in `D:\docs\MUSICA.md`, **fuori dal progetto e fuori dal
  repository git**. Ogni file creato o modificato da questo piano deve stare
  sotto `D:\DelugePal\`, e ogni percorso scritto qui è assoluto per quello.
  L'unica eccezione dichiarata è `~/.claude/skills/`, che è a livello utente
  di proposito.
- **Nessuna dipendenza esterna.** La suite non usa pytest «per non aggiungere dipendenze» (`tests/test_all.py:3`). Vale anche qui.
- **Interprete:** `.venv/Scripts/python.exe`, sempre da `D:\DelugePal`.
- **Suite:** un solo file `tests/test_all.py`, funzioni `test_*`, helper `check(nome, cond, dettaglio)`. Si lancia con `.venv/Scripts/python.exe tests/test_all.py` e stampa `N/N test superati`.
- **Lingua:** nomi e docstring in italiano, senza accenti nel codice (il resto della libreria scrive `perche'`, `piu'`).
- **Zero falsi positivi sul corpus:** ogni controllo nuovo deve dare zero segnalazioni sui 139 file scritti dal dispositivo. È la regola che ha già smascherato due controlli troppo severi.
- **Git:** repo inizializzato, `core.autocrlf false` e `.gitattributes` con `* -text`. **Non toccare quella configurazione:** normalizzare i fine riga romperebbe la riscrittura byte-esatta.
- **Convenzione di altezza:** `do4` = `C4` = 60 (MIDI standard). Segnata `[OSS]` nella spec: da confrontare col display del Deluge.
- **Griglia:** 384 tick per battuta, 96 per movimento, **24 per sedicesimo**.

---

### Task 1: Altezze — dai nomi ai numeri MIDI

**File:**
- Creare: `tools/delugexml/musica.py`
- Test: `tests/test_all.py` (aggiungere `test_musica_altezze`)

**Interfacce:**
- Consuma: niente
- Produce: `altezza(nome: str) -> int`, `nome_altezza(midi: int, italiano: bool = True) -> str`, costanti `NOMI_IT` e `NOMI_EN`

- [ ] **Passo 1: scrivere il test che fallisce**

In `tests/test_all.py`, prima di `if __name__ == '__main__':`

```python
def test_musica_altezze():
    """Nomi di altezza italiani e inglesi verso i numeri MIDI.

    Convenzione: do4 = C4 = 60, quella MIDI standard. [OSS] da confrontare
    con cio' che mostra il display del Deluge.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    check('do4 e il do centrale', MU.altezza('do4') == 60)
    check('e C4 e lo stesso', MU.altezza('C4') == 60)
    check('re2 come nelle prove d arranger', MU.altezza('re2') == 38)
    check('fa#3', MU.altezza('fa#3') == 54)
    check('mib5 e un semitono sotto mi5', MU.altezza('mib5') == 75
          and MU.altezza('mi5') == 76)
    check('sib4 non e confuso con si4', MU.altezza('sib4') == 70
          and MU.altezza('si4') == 71)
    check('Bb4 in inglese e lo stesso', MU.altezza('Bb4') == 70)
    check('maiuscole e minuscole indifferenti',
          MU.altezza('LA3') == MU.altezza('la3'))
    check('un nome inventato viene rifiutato',
          _raises(lambda: MU.altezza('zolfo3'), ValueError))
    check('un ottava fuori scala viene rifiutata',
          _raises(lambda: MU.altezza('do99'), ValueError))

    # andata e ritorno su tutta l'estensione
    sbagliati = [m for m in range(128)
                 if MU.altezza(MU.nome_altezza(m)) != m]
    check('nome_altezza e altezza sono l una l inversa dell altra',
          not sbagliati, f'{len(sbagliati)} rotti: {sbagliati[:5]}')
```

- [ ] **Passo 2: lanciarlo e vederlo fallire**

```bash
.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "musica|FAIL"
```

Atteso: `FAIL test_musica_altezze — eccezione ModuleNotFoundError`

- [ ] **Passo 3: scrivere l'implementazione minima**

Creare `tools/delugexml/musica.py`:

```python
"""Lo strato musicale: dalla lingua che parliamo alle chiamate alla libreria.

Nessuna funzione di questo modulo accetta o produce XML. Chi vuole scrivere
un file passa da `delugexml.song`, `create`, `arranger`: qui si traducono
soltanto altezze, ritmi e intenzioni.
"""
from __future__ import annotations

import re

#: I gradi della scala cromatica dal do, per nome.
NOMI_IT = {'do': 0, 're': 2, 'mi': 4, 'fa': 5, 'sol': 7, 'la': 9, 'si': 11}
NOMI_EN = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}

#: Come si scrive un'altezza in uscita, preferendo i diesis.
CROMATICA_IT = ('do', 'do#', 're', 're#', 'mi', 'fa', 'fa#', 'sol', 'sol#',
                'la', 'la#', 'si')
CROMATICA_EN = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

#: do4 = 60, la convenzione MIDI standard.
OTTAVA_DEL_DO_CENTRALE = 4

_ALTEZZA = re.compile(r'^([a-z]+)(#|b)?(-?\d+)$')


def altezza(nome: str) -> int:
    """Il numero MIDI di un nome di altezza: `do4`, `C4`, `fa#3`, `mib5`.

    Accetta nomi italiani e inglesi. L'ambiguita' e' una sola e va sciolta
    nell'ordine giusto: `si` (italiano) contro `b` seguito da bemolle. Si
    provano prima i nomi italiani, che sono piu' lunghi, poi la lettera
    inglese — cosi' `sib4` e' si bemolle e `Bb4` e' la stessa nota.
    """
    testo = nome.strip().lower()
    m = _ALTEZZA.match(testo)
    if not m:
        raise ValueError(f'{nome!r} non e un nome di altezza (es. do4, fa#3)')
    lettere, alterazione, ottava = m.group(1), m.group(2), int(m.group(3))

    grado = None
    for base, tabella in ((lettere, NOMI_IT), (lettere[:1], NOMI_EN)):
        if base in tabella and (base == lettere or len(lettere) == 1):
            grado = tabella[base]
            break
    if grado is None and len(lettere) == 2 and lettere[1] == 'b':
        # 'bb' o 'eb': lettera inglese piu' bemolle attaccato
        if lettere[0] in NOMI_EN:
            grado = NOMI_EN[lettere[0]]
            alterazione = 'b'
    if grado is None:
        raise ValueError(f'{nome!r}: {lettere!r} non e una nota')

    if alterazione == '#':
        grado += 1
    elif alterazione == 'b':
        grado -= 1

    midi = (ottava + 1) * 12 + grado
    if not 0 <= midi <= 127:
        raise ValueError(f'{nome!r} da {midi}, fuori dall estensione MIDI 0-127')
    return midi


def nome_altezza(midi: int, italiano: bool = True) -> str:
    """Il nome di un numero MIDI, coi diesis: 60 -> 'do4'."""
    if not 0 <= midi <= 127:
        raise ValueError(f'{midi} fuori dall estensione MIDI 0-127')
    tabella = CROMATICA_IT if italiano else CROMATICA_EN
    return f'{tabella[midi % 12]}{midi // 12 - 1}'
```

- [ ] **Passo 4: lanciare i test e vederli passare**

```bash
.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "altezza|do4|inversa|FAIL|superati"
```

Atteso: tutte le righe `PASS`, e il totale cresciuto di 10.

- [ ] **Passo 5: committare**

```bash
git add tools/delugexml/musica.py tests/test_all.py
git commit -m "musica: nomi di altezza italiani e inglesi verso MIDI"
```

---

### Task 2: Ritmi — dai pattern alle note

**File:**
- Modificare: `tools/delugexml/musica.py`
- Test: `tests/test_all.py` (aggiungere `test_musica_ritmi`)

**Interfacce:**
- Consuma: `altezza()` dal Task 1
- Produce: `TICK_PER_PASSO = 24`, `passi(pattern, *, velocity=90, accento=110, durata=None, da=0) -> list[Note]`, `melodia(spec, *, durata='1/8', da=0, velocity=80) -> dict[int, list[Note]]`, `durata_in_tick(spec) -> int`

- [ ] **Passo 1: scrivere il test che fallisce**

```python
def test_musica_ritmi():
    """Pattern a passi e melodie, verso le note della libreria.

    La stringa di passi mappa sulla griglia del Deluge: 16 colonne per
    battuta, quindi 24 tick per sedicesimo.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    check('un sedicesimo e 24 tick', MU.TICK_PER_PASSO == 24)
    check('16 passi fanno una battuta', 16 * MU.TICK_PER_PASSO == 384)

    kick = MU.passi('x...x...x...x...')
    check('quattro colpi sui movimenti', len(kick) == 4
          and [n.pos for n in kick] == [0, 96, 192, 288],
          str([n.pos for n in kick]))
    check('e durano un sedicesimo', all(n.length == 24 for n in kick))

    rim = MU.passi('....x.......x...')
    check('rim sul 2 e sul 4', [n.pos for n in rim] == [96, 288])

    acc = MU.passi('X...x...')
    check('la X e un accento', acc[0].velocity > acc[1].velocity,
          f'{acc[0].velocity} contro {acc[1].velocity}')

    check('un carattere estraneo viene rifiutato',
          _raises(lambda: MU.passi('x..o'), ValueError))
    check('una lunghezza che non e multiplo di 16 viene rifiutata',
          _raises(lambda: MU.passi('x...x'), ValueError))

    check('durata_in_tick: 1/8 e mezza pulsazione',
          MU.durata_in_tick('1/8') == 48)
    check('durata_in_tick: 1/4 e una pulsazione',
          MU.durata_in_tick('1/4') == 96)
    check('durata_in_tick: 1/1 e una battuta',
          MU.durata_in_tick('1/1') == 384)

    mel = MU.melodia('re2 fa#2 la2 re3', durata='1/8')
    check('quattro altezze diverse, una riga ciascuna', len(mel) == 4)
    check('sono le altezze giuste',
          sorted(mel) == [38, 42, 45, 50], str(sorted(mel)))
    pos = sorted(n.pos for note in mel.values() for n in note)
    check('a passo di croma', pos == [0, 48, 96, 144], str(pos))

    ripetuta = MU.melodia('re2 re2', durata='1/4')
    check('la stessa altezza due volte finisce in UNA riga con due note',
          len(ripetuta) == 1 and len(ripetuta[38]) == 2,
          str({k: len(v) for k, v in ripetuta.items()}))

    check('una pausa salta il posto',
          [n.pos for n in MU.melodia('re2 . re2', durata='1/4')[38]]
          == [0, 192])
```

- [ ] **Passo 2: lanciarlo e vederlo fallire**

```bash
.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "ritmi|passi|FAIL"
```

Atteso: `FAIL test_musica_ritmi — eccezione AttributeError: module ... has no attribute 'TICK_PER_PASSO'`

- [ ] **Passo 3: scrivere l'implementazione**

Aggiungere in fondo a `tools/delugexml/musica.py`:

```python
from .notes import Note                                   # noqa: E402

#: La griglia del Deluge e' larga 16 colonne per battuta, e una battuta e'
#: 384 tick: ogni colonna e' un sedicesimo.
TICK_PER_PASSO = 24
TICK_PER_BATTUTA = 384

#: I caratteri di un pattern a passi.
PAUSA = '.'
COLPO = 'x'
ACCENTO = 'X'


def passi(pattern: str, *, velocity: int = 90, accento: int = 110,
          durata: int | None = None, da: int = 0) -> list[Note]:
    """Le note di un pattern percussivo: `'x...x...x...x...'`.

    Un carattere per sedicesimo, come le colonne della griglia del Deluge:
    `x` colpo, `X` colpo accentato, `.` silenzio. La lunghezza dev'essere un
    multiplo di 16, cioe' un numero intero di battute.
    """
    testo = pattern.replace(' ', '')
    if not testo or len(testo) % 16:
        raise ValueError(
            f'un pattern ha 16 passi per battuta, questo ne ha {len(testo)}')
    ammessi = {PAUSA, COLPO, ACCENTO}
    estranei = sorted(set(testo) - ammessi)
    if estranei:
        raise ValueError(f'caratteri non ammessi {estranei}, '
                         f'usare {sorted(ammessi)}')
    lung = TICK_PER_PASSO if durata is None else durata
    out = []
    for i, c in enumerate(testo):
        if c == PAUSA:
            continue
        out.append(Note(pos=da + i * TICK_PER_PASSO, length=lung,
                        velocity=accento if c == ACCENTO else velocity))
    return out


def durata_in_tick(spec: str | int) -> int:
    """`'1/8'` -> 48 tick. Un intero passa invariato, gia' in tick."""
    if isinstance(spec, int):
        return spec
    testo = str(spec).strip()
    if '/' not in testo:
        raise ValueError(f'{spec!r} non e una durata (es. 1/8, 1/4)')
    num, den = testo.split('/', 1)
    try:
        n, d = int(num), int(den)
    except ValueError:
        raise ValueError(f'{spec!r} non e una durata (es. 1/8, 1/4)') from None
    if d <= 0 or n <= 0:
        raise ValueError(f'{spec!r}: numeratore e denominatore positivi')
    tick = TICK_PER_BATTUTA * n // d
    if tick <= 0:
        raise ValueError(f'{spec!r} da {tick} tick')
    return tick


def melodia(spec: str, *, durata: str | int = '1/8', da: int = 0,
            velocity: int = 80, stacco: int = 8) -> dict[int, list[Note]]:
    """Da `'re2 fa#2 la2 re3'` alle note, raggruppate per altezza.

    Il Deluge tiene le note in righe, una per altezza, quindi il risultato e'
    un dizionario altezza -> note e non una lista piatta: due `re2` nella
    stessa frase finiscono nella STESSA riga, non in due.

    Un punto e' una pausa: occupa il suo posto e non produce nota. `stacco`
    accorcia ogni nota rispetto al passo, cosi' due note uguali di fila si
    sentono staccate invece di fondersi.
    """
    passo = durata_in_tick(durata)
    lung = max(1, passo - stacco)
    out: dict[int, list[Note]] = {}
    for i, gettone in enumerate(spec.split()):
        if gettone == PAUSA:
            continue
        y = altezza(gettone)
        out.setdefault(y, []).append(
            Note(pos=da + i * passo, length=lung, velocity=velocity))
    return out
```

- [ ] **Passo 4: lanciare i test**

```bash
.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "passi|movimenti|melodia|altezze|croma|FAIL|superati"
```

Atteso: tutte `PASS`.

- [ ] **Passo 5: committare**

```bash
git add tools/delugexml/musica.py tests/test_all.py
git commit -m "musica: pattern a passi e melodie verso le note"
```

---

### Task 3: Il cancello — `verifica()`

**File:**
- Modificare: `tools/delugexml/musica.py`
- Test: `tests/test_all.py` (aggiungere `test_musica_verifica`)

**Interfacce:**
- Consuma: `song.check_clip_types`, `song.same_section_conflicts`, `arranger.check`, `midicv.check`, `audio.check`, `kit.check_indices`
- Produce: `verifica(doc) -> list[str]`

- [ ] **Passo 1: scrivere il test che fallisce**

```python
def test_musica_verifica():
    """Il cancello: nessun file sale sul Deluge se non passa.

    E' la regola che avrebbe fermato entrambi i file rifiutati dal
    dispositivo in questa storia — `soundParams` su una clip di kit
    (FINDINGS §6-quater) e il `<params>` audio incompleto (§6-quinquies).
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    # zero falsi positivi su tutto cio' che ha scritto il dispositivo
    sporchi = []
    n = 0
    for b in (ROOT / 'refs' / 'songs', ROOT / 'corpus_versions'):
        for q in sorted(b.rglob('*.XML')):
            try:
                d = parse_file(q)
            except Exception:                            # noqa: BLE001
                continue
            n += 1
            if MU.verifica(d):
                sporchi.append(f'{q.name}: {MU.verifica(d)[0]}')
    check(f'zero falsi positivi sui {n} file del dispositivo',
          not sporchi, '; '.join(sporchi[:2]))

    # e becca il difetto vero: una clip di kit che si dichiara synth
    doc = parse_file(REFS / 'songs' / 'ARR0.XML')
    from delugexml import create as C                     # noqa: PLC0415
    _, clip = C.add_track(doc, REFS / 'kits' / 'CR78FROMMARS.XML',
                          name='CR78FROMMARS', folder='KITS')
    check('un kit sano passa il cancello', not MU.verifica(doc),
          str(MU.verifica(doc)[:1]))
    kp = clip.find('kitParams')
    kp.tag = 'soundParams'
    kp.dirty = True
    problemi = MU.verifica(doc)
    check('e il cancello si chiude se la clip si contraddice',
          any('kit' in p and 'synth' in p for p in problemi),
          str(problemi[:2]))
```

- [ ] **Passo 2: lanciarlo e vederlo fallire**

```bash
.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "cancello|falsi positivi sui|FAIL"
```

Atteso: `FAIL test_musica_verifica — eccezione AttributeError: ... 'verifica'`

- [ ] **Passo 3: scrivere l'implementazione**

Aggiungere a `tools/delugexml/musica.py`:

```python
def verifica(doc) -> list[str]:
    """Tutti i controlli della libreria, in una chiamata sola.

    **Nessun file sale sul Deluge se questa lista non e' vuota.** Non e' una
    formalita': due file generati in questo progetto erano XML validi, si
    rileggevano senza errori, e il dispositivo li ha rifiutati — uno con un
    crash. Cio' che li avrebbe fermati e' esattamente questo insieme di
    controlli semantici.
    """
    from . import song as S                               # import locale: ciclo
    from . import arranger as A                           # noqa: PLC0415
    from . import midicv as M                             # noqa: PLC0415
    from . import audio as AU                             # noqa: PLC0415
    from . import kit as K                                # noqa: PLC0415

    problemi = []
    problemi += S.check_clip_types(doc)
    problemi += S.same_section_conflicts(doc)
    problemi += A.check(doc)
    problemi += M.check(doc)
    problemi += AU.check(doc)
    for strumento in S.instruments(doc):
        if strumento.tag == 'kit':
            problemi += K.check_indices(doc, strumento)
    return problemi
```

Se `kit.check_indices` ha una firma diversa, adattare la chiamata: verificarla con

```bash
.venv/Scripts/python.exe -c "import sys;sys.path.insert(0,'tools');import inspect;from delugexml import kit;print(inspect.signature(kit.check_indices))"
```

- [ ] **Passo 4: lanciare i test**

```bash
.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "cancello|falsi positivi|contraddice|FAIL|superati"
```

Atteso: tutte `PASS`.

- [ ] **Passo 5: committare**

```bash
git add tools/delugexml/musica.py tests/test_all.py
git commit -m "musica: verifica() come cancello prima di ogni caricamento"
```

---

### Task 4: Raccontare una song in termini musicali

**File:**
- Modificare: `tools/delugexml/musica.py`
- Test: `tests/test_all.py` (aggiungere `test_musica_racconta`)

**Interfacce:**
- Consuma: `nome_altezza()` dal Task 1; `song.clips`, `song.get_bpm`, `song.scale_name`, `song.ticks_per_bar`, `arranger.arrangement`, `midicv.describe`, `audio.describe`
- Produce: `racconta(doc) -> str`, `racconta_clip(doc, clip) -> str`

- [ ] **Passo 1: scrivere il test che fallisce**

```python
def test_musica_racconta():
    """Il racconto in termini musicali: e' cio' che rende correggibile il lavoro.

    Una modifica di cui non si sa dire cosa ha fatto non e' correggibile a
    parole, e il ciclo «proponi e io correggo» si spezza.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Aolac.XML')
    testo = MU.racconta(doc)
    check('il racconto dice il tempo',
          str(round(S.get_bpm(doc.root))) in testo, testo[:120])
    check('e la scala', S.scale_name(doc).split()[0].lower() in testo.lower(),
          S.scale_name(doc))
    check('e nomina gli strumenti',
          'ADDITIVE' in testo and 'KIT008' in testo)
    check('e conta le istanze d arranger', 'battut' in testo.lower())
    check('non contiene XML', '<' not in testo and '0x' not in testo,
          [r for r in testo.splitlines() if '<' in r or '0x' in r][:2])

    # le note escono come nomi, non come numeri
    d2 = parse_file(REFS / 'songs' / 'ARR0.XML')
    clip = d2.root.find('sessionClips').children[0]
    S.write_notes(S.add_note_row(clip, 62), [Note(pos=0, length=88)],
                  create=True)
    r = MU.racconta_clip(d2, clip)
    check('un re2 e raccontato come re2', 're2' in r, r)
    check('e non come 62', '62' not in r.replace('re2', ''), r)
```

- [ ] **Passo 2: lanciarlo e vederlo fallire**

```bash
.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "racconto|racconta|FAIL"
```

Atteso: `FAIL test_musica_racconta — eccezione AttributeError: ... 'racconta'`

- [ ] **Passo 3: scrivere l'implementazione**

Aggiungere a `tools/delugexml/musica.py`:

```python
def racconta_clip(doc, clip) -> str:
    """Una clip in termini musicali: righe, note, posizioni in movimenti."""
    from . import song as S                               # import locale: ciclo

    tpb = S.ticks_per_bar(doc.root)
    kit = S.is_kit_clip(clip)
    nomi = S.drum_names(doc, clip) if kit else []
    righe = []
    for r in S.note_rows(clip):
        note = S.read_notes(r)
        if not note:
            continue
        if kit:
            i = int(r.get('drumIndex') or -1)
            etichetta = nomi[i] if 0 <= i < len(nomi) else f'drum {i}'
        else:
            etichetta = nome_altezza(int(r.get('y')))
        quando = ', '.join(f'{n.pos / tpb + 1:g}' for n in note[:8])
        coda = '…' if len(note) > 8 else ''
        righe.append(f'      {etichetta:16} {len(note):2} note a battuta '
                     f'{quando}{coda}')
    testa = (f'   clip {S.clip_label(clip)!r}: '
             f'{int(clip.get("length") or 0) / tpb:g} battute, '
             f'sezione {clip.get("section")}')
    return '\n'.join([testa] + righe) if righe else testa + ' (vuota)'


def racconta(doc) -> str:
    """L'intera song in termini musicali, senza una riga di XML.

    Va letta dopo ogni riscaricamento dal dispositivo: e' il modo di sapere
    cosa c'e' davvero prima di modificarlo, e cio' che permette all'utente di
    correggere a parole quello che e' stato fatto.
    """
    from . import song as S                               # import locale: ciclo
    from . import arranger as A                           # noqa: PLC0415
    from . import midicv as M                             # noqa: PLC0415
    from . import audio as AU                             # noqa: PLC0415

    tpb = S.ticks_per_bar(doc.root)
    fuori = [f'{S.get_bpm(doc.root):.0f} BPM, {S.scale_name(doc)}, '
             f'swing {S.get_swing(doc)[0]}']

    fuori.append('')
    fuori.append('strumenti e clip:')
    for strumento in S.instruments(doc):
        nome = (strumento.get('presetName') or strumento.get('name')
                or f'<{strumento.tag}>')
        fuori.append(f'   <{strumento.tag}> {nome}')
        for _, clip in S.clips(doc):
            if S.instrument_of(doc, clip) is strumento:
                fuori.append(racconta_clip(doc, clip))

    ist = A.arrangement(doc)
    fuori.append('')
    if ist:
        fuori.append(f'arrangiamento ({len(ist)} blocchi):')
        for strumento, i, clip in ist:
            nome = A.nome_di(strumento)
            bianca = ' [bianca]' if clip is not None and A.is_white(clip) \
                else ''
            fuori.append(f'   battuta {i.pos / tpb + 1:g} per '
                         f'{i.length / tpb:g}: {nome}{bianca}')
    else:
        fuori.append('arrangiamento: vuoto (le clip vivono solo in session view)')

    extra = M.describe(doc) + AU.describe(doc)
    if extra:
        fuori.append('')
        fuori += ['   ' + r for r in extra]
    return '\n'.join(fuori)
```

- [ ] **Passo 4: lanciare i test**

```bash
.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "racconto|re2|non contiene XML|FAIL|superati"
```

Atteso: tutte `PASS`.

- [ ] **Passo 5: committare**

```bash
git add tools/delugexml/musica.py tests/test_all.py
git commit -m "musica: racconta() la song in termini musicali"
```

---

### Task 5: Verbi di suono e mix

**File:**
- Modificare: `tools/delugexml/musica.py`
- Test: `tests/test_all.py` (aggiungere `test_musica_verbi`)

**Interfacce:**
- Consuma: `sound.get`, `sound.set`, `param_ids.by_name`
- Produce: `VERBI: dict[str, tuple[str, int]]`, `applica_verbo(doc, nodo, verbo, forza=1) -> dict[str, object]`, `verbi_disponibili() -> list[str]`

> **ESITO — l'interfaccia consegnata è diversa da quella qui prevista.** La
> revisione ha bocciato la tabella unica `VERBI`, dove «al centro» era un passo
> `0` con significato speciale: `0` voleva dire due cose, `forza` veniva
> ignorata in silenzio, e il valore centrale ha senso solo per il `pan`.
> Consegnate invece **`VERBI_RELATIVI` e `VERBI_ASSOLUTI`**, due tabelle con
> contratti distinti. `applica_verbo()` e `verbi_disponibili()` restano come
> previsto. Il codice qui sotto resta come traccia di cio' che era stato
> pianificato — **non è cio' che sta nel repository.**

- [ ] **Passo 1: scrivere il test che fallisce**

```python
def test_musica_verbi():
    """I verbi di suono: gusto dichiarato, non euristica nascosta.

    Ogni applicazione deve riferire QUALE parametro ha mosso e di quanto,
    altrimenti l'utente non puo' scavalcare la scelta.
    """
    from delugexml import musica as MU                    # noqa: PLC0415
    from delugexml import param_ids as PI                 # noqa: PLC0415
    from delugexml import sound as SN                     # noqa: PLC0415

    # `by_name` SOLLEVA per un nome ignoto, non restituisce None
    ignoti = []
    for parametro, _ in MU.VERBI.values():
        try:
            PI.by_name(parametro)
        except ValueError:
            ignoti.append(parametro)
    check('ogni verbo punta a un parametro che esiste in tabella',
          not ignoti, str(ignoti))

    doc = parse_file(REFS / 'songs' / 'ARR0.XML')
    clip = doc.root.find('sessionClips').children[0]
    prima = SN.get(clip, 'lpfFrequency')
    esito = MU.applica_verbo(doc, clip, 'piu scuro')
    dopo = SN.get(clip, 'lpfFrequency')
    check('«piu scuro» abbassa il taglio del filtro', dopo < prima,
          f'{prima} -> {dopo}')
    check('e riferisce parametro, prima e dopo',
          esito['parametro'] == 'lpfFrequency' and esito['prima'] == prima
          and esito['dopo'] == dopo, str(esito))

    check('«piu brillante» lo rialza',
          MU.applica_verbo(doc, clip, 'piu brillante')['dopo'] > dopo)

    check('il valore resta nella scala 0-50',
          all(0 <= MU.applica_verbo(doc, clip, 'piu scuro', forza=9)['dopo']
              <= 50 for _ in range(4)))

    check('un verbo sconosciuto viene rifiutato dicendo quali esistono',
          _raises(lambda: MU.applica_verbo(doc, clip, 'piu blu'), ValueError))
    check('verbi_disponibili li elenca',
          'piu scuro' in MU.verbi_disponibili())
```

- [ ] **Passo 2: lanciarlo e vederlo fallire**

```bash
.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "verbo|verbi|FAIL"
```

Atteso: `FAIL test_musica_verbi — eccezione AttributeError: ... 'VERBI'`

- [ ] **Passo 3: scrivere l'implementazione**

Aggiungere a `tools/delugexml/musica.py`:

```python
#: Le parole verso i parametri, con la direzione in unita' del display 0-50.
#:
#: **Questa tabella e' gusto, non un fatto.** Nasce piccola e arbitraria, e
#: cresce dalle correzioni: quando l'utente dice «no, piu' scuro vuol dire
#: anche togliere risonanza», si aggiunge qui e si annota in docs/MUSICA.md.
#: Ogni applicazione riferisce cosa ha mosso, cosi' resta scavalcabile.
VERBI: dict[str, tuple[str, int]] = {
    'piu scuro': ('lpfFrequency', -8),
    'piu chiuso': ('lpfFrequency', -8),
    'piu brillante': ('lpfFrequency', +8),
    'piu aperto': ('lpfFrequency', +8),
    'piu forte': ('volume', +5),
    'piu piano': ('volume', -5),
    'piu riverbero': ('reverbAmount', +8),
    'meno riverbero': ('reverbAmount', -8),
    'a sinistra': ('pan', -10),
    'a destra': ('pan', +10),
    'al centro': ('pan', 0),          # 0 = porta al centro, non sposta
}

#: Il centro della scala del display, dove `pan` e' centrato.
CENTRO = 25


def verbi_disponibili() -> list[str]:
    return sorted(VERBI)


def applica_verbo(doc, nodo, verbo: str, forza: int = 1) -> dict:
    """Applica un verbo a una clip o a uno strumento, e dice cosa ha fatto.

    `forza` moltiplica il passo. Il risultato riporta parametro, valore prima
    e valore dopo: senza quello l'utente non puo' correggere una scelta che
    e' di gusto.
    """
    from . import sound as SN                             # import locale: ciclo

    chiave = verbo.strip().lower()
    if chiave not in VERBI:
        raise ValueError(f'{verbo!r} non e un verbo noto. Ci sono: '
                         f'{", ".join(verbi_disponibili())}')
    parametro, passo = VERBI[chiave]
    prima = SN.get(nodo, parametro)
    if prima is None:
        raise ValueError(f'{parametro} non e impostabile su questo nodo '
                         f'(assente o automatizzato)')
    dopo = CENTRO if passo == 0 else max(0, min(50, prima + passo * forza))
    SN.set(nodo, parametro, dopo)
    return {'verbo': chiave, 'parametro': parametro,
            'prima': prima, 'dopo': dopo}
```

- [ ] **Passo 4: lanciare i test**

```bash
.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "verbo|scuro|brillante|scala 0-50|FAIL|superati"
```

Atteso: tutte `PASS`. Se `param_ids.by_name` solleva invece di restituire `None` per un nome ignoto, adattare il primo controllo del test con un `try/except`.

- [ ] **Passo 5: committare**

```bash
git add tools/delugexml/musica.py tests/test_all.py
git commit -m "musica: verbi di suono e mix, con resoconto di cosa si e mosso"
```

---

### Task 6: Esportare il modulo e provarlo per mutazione

**File:**
- Modificare: `tools/delugexml/__init__.py:10-14`
- Test: `tests/test_all.py` (aggiungere `test_musica_mutazione`)

**Interfacce:**
- Consuma: tutto quanto sopra
- Produce: `delugexml.musica` importabile dal package

- [ ] **Passo 1: scrivere il test che fallisce**

```python
def test_musica_mutazione():
    """Il cancello deve avere i denti: se non fallisce mai, non protegge.

    Stessa disciplina di `test_costanti_catturate`: si guasta il documento di
    proposito e si pretende che `verifica()` se ne accorga.
    """
    from delugexml import musica as MU                    # noqa: PLC0415
    import delugexml                                      # noqa: PLC0415

    check('musica e esportato dal package', hasattr(delugexml, 'musica'))

    doc = parse_file(REFS / 'songs' / 'Aolac.XML')
    check('la song di partenza e sana', not MU.verifica(doc))

    # 1. un indice d'arranger che punta oltre la fine
    from delugexml import arranger as A                   # noqa: PLC0415
    for st in S.instruments(doc):
        ists = A.instances(st)
        if ists:
            A.set_instances(st, [A.Istanza(pos=i.pos, length=i.length,
                                           code=999) for i in ists])
            break
    check('un indice di clip inesistente viene visto',
          any('999' in p for p in MU.verifica(doc)),
          str(MU.verifica(doc)[:1]))

    # 2. due clip dello stesso strumento nella stessa scena
    d2 = parse_file(REFS / 'songs' / 'Aolac.XML')
    copia = S.duplicate_clip(d2, 0)
    copia.set('section', d2.root.find('sessionClips').children[0]
              .get('section'))
    check('due clip dello stesso strumento in una scena vengono viste',
          any('stesso strumento' in p for p in MU.verifica(d2)),
          str(MU.verifica(d2)[:1]))
```

- [ ] **Passo 2: lanciarlo e vederlo fallire**

```bash
.venv/Scripts/python.exe tests/test_all.py 2>&1 | grep -E "mutazione|esportato|denti|FAIL"
```

Atteso: `FAIL — musica e esportato dal package`

- [ ] **Passo 3: esportare il modulo**

In `tools/delugexml/__init__.py`, sostituire le ultime righe:

```python
from . import song, notes, arranger, midicv, audio, musica

__all__ = ['Node', 'Document', 'parse', 'parse_file', 'ParseProblem',
           'FormatTable', 'serialize', 'write_file', 'Note', 'song', 'notes',
           'arranger', 'midicv', 'audio', 'musica']
```

- [ ] **Passo 4: lanciare tutta la suite**

```bash
.venv/Scripts/python.exe tests/test_all.py 2>&1 | tail -3
```

Atteso: `N/N test superati`, con N cresciuto di circa 40 rispetto ai 300 di partenza.

- [ ] **Passo 5: committare**

```bash
git add tools/delugexml/__init__.py tests/test_all.py
git commit -m "musica: esportare il modulo e provare il cancello per mutazione"
```

---

### Task 7: La skill e la conoscenza musicale

**File** (assoluti: la working directory della sessione è `D:\`, non il progetto):
- Modificare: `D:\DelugePal\tools\delugexml\musica.py` (destinazione sulla SD)
- Test: `D:\DelugePal\tests\test_all.py` (aggiungere `test_musica_destinazione`)
- Creare: `D:\DelugePal\.claude\skills\deluge-pal\SKILL.md`
- Creare: `D:\DelugePal\docs\MUSICA.md`
- Copiare: `music-composer` da `D:\Webarmonium\.claude\skills\` a `~/.claude/skills/` — **questa sola** sta fuori dal progetto, di proposito: è una skill di dominio che deve valere in qualunque cartella

**Interfacce:**
- Produce: `CARTELLA_SD: str`, `destinazione(nome: str, versione: int = 1) -> str`

### La destinazione sulla SD è una sola

Richiesta esplicita dell'utente, dopo aver dovuto ripulire 34 file sparsi fra
le sue 135 song: **Deluge Pal scrive sempre e solo in `/SONGS/DelugePal/`.**

La cartella esiste già sulla SD e contiene il template più le quattro
dimostrazioni verificate. Il vincolo va messo **nel codice**, non solo nella
skill: una regola scritta solo in prosa viene disattesa.

```python
#: L'UNICA cartella del dispositivo in cui Deluge Pal scrive. Le song
#: dell'utente stanno in /SONGS/ e non vanno toccate: mescolarci i file
#: generati e' gia' costato una pulizia di 34 file a mano.
CARTELLA_SD = '/SONGS/DelugePal'

def destinazione(nome: str, versione: int = 1) -> str:
    """Il percorso remoto per una song generata: `/SONGS/DelugePal/HOUSE01.XML`.

    `dsysex put` non sovrascrive mai, quindi ogni iterazione del ciclo sale
    con la versione successiva. Non esiste un modo di elencare la cartella
    remota (il comando `dir` non risponde, vedi docs/SYSEX.md §4-bis): si
    prova la versione 1 e si incrementa finche' `put` accetta.
    """
```

Vincoli che il test deve blindare:

- il percorso comincia **sempre** con `CARTELLA_SD`; nessun argomento deve
  poter farlo uscire da lì — in particolare un `nome` che contenga `/`, `..`
  o una barra rovesciata va **rifiutato**, non ripulito in silenzio
- la versione compare come **due cifre** (`01`, `02`, … `99`); oltre, errore
- il nome viene normalizzato in maiuscolo con estensione `.XML`, perché è
  così che il dispositivo mostra le song
- un nome vuoto o di soli spazi viene rifiutato

**Interfacce:**
- Consuma: tutto `musica.py`
- Produce: il protocollo che il modello segue

- [ ] **Passo 1: rendere `music-composer` disponibile ovunque**

Oggi è *scoped* a Webarmonium, quindi non si applica lavorando in `D:\DelugePal`.

```bash
mkdir -p ~/.claude/skills && cp -r "/d/Webarmonium/.claude/skills/music-composer" ~/.claude/skills/ && ls ~/.claude/skills/music-composer
```

Atteso: `SKILL.md  assets  references  scripts`

- [ ] **Passo 2: scrivere `D:\DelugePal\docs\MUSICA.md`**

Parte quasi vuoto, per costruzione: contiene solo ciò che è stato verificato.

```markdown
# Conoscenza musicale — cosa funziona sul materiale di questo utente

Questo file **non** è una teoria generale della musica: per quella si invoca
la skill `music-composer`. Qui sta solo ciò che è stato imparato correggendo
il lavoro, e che nessuna skill generica sa.

Stessa disciplina del resto del progetto: si scrive ciò che è stato
verificato, e si segna `[OSS]` ciò che è supposto.

## Preset e come vengono usati

*(vuoto: da riempire dicendo quale preset fa cosa)*

## Groove e generi

*(vuoto: le schede di `music-composer` danno solo tempo e strumenti tipici.
Qui vanno le cose che le mancano — come si muove un basso, dove cadono gli
accenti, che durate)*

## Correzioni ricevute

*(ogni volta che una proposta viene corretta, la lezione va qui, con la data)*
```

- [ ] **Passo 3: scrivere `.claude/skills/deluge-pal/SKILL.md`**

```markdown
---
name: deluge-pal
description: Genera e modifica song per il Synthstrom Deluge a partire da descrizioni musicali a parole, caricandole sul dispositivo via SysEx. Usare quando si parla di comporre, arrangiare, mixare o progettare suoni per il Deluge, o quando si nominano clip, kit, arranger, tracce MIDI/CV o clip audio del Deluge.
---

# Deluge Pal

Il progetto sta in `D:\DelugePal`. **Leggere `HANDOFF.md` a inizio sessione.**

## Il ciclo

```
prompt → libreria → XML → SysEx → l'utente apre e ascolta
                                          ↓
    ricarica come     ←   modifica   ←   «il basso è troppo statico»
    versione nuova          ↑
                    RISCARICA dal Deluge prima di toccare
```

## Le cinque regole

1. **Riscarica prima di modificare.** La song sul Deluge è la verità: lui la
   apre e può averci messo mano. Lavorare su una copia locale cancella il suo
   lavoro senza accorgersene.
2. **Mai scrivere XML.** Mai costruire nodi di formato a mano, mai trascrivere
   valori letti da un file. Solo chiamate alla libreria. Le costanti si
   generano da codice e si confrontano con un test.
3. **`musica.verifica(doc)` prima di ogni caricamento.** Se non è vuota, non
   si carica e si riferisce il problema.
4. **Raccontare cosa è cambiato**, con `musica.racconta()` e con i valori
   esatti dei parametri toccati. Un'operazione silenziosa non è correggibile.
5. **Nomi versionati, e una sola cartella.** `put` non sovrascrive: `HOUSE01`,
   `HOUSE02`, … Il percorso si costruisce **sempre** con
   `musica.destinazione()`, che scrive solo in `/SONGS/DelugePal/`. Le 135
   song dell'utente stanno in `/SONGS/` e non si toccano.

## Perché la regola 2 non è un consiglio

Due file generati sono stati rifiutati dal dispositivo, uno con un crash:

- una clip di kit con `<soundParams>` invece di `<kitParams>` — quel tag
  dichiara al caricatore il TIPO della clip (FINDINGS §6-quater)
- il `<params>` di una clip audio trascritto a mano da un'anteprima troncata:
  11 attributi su 31, valori inventati (§6-quinquies, crash E365)

Entrambi erano XML validi e si rileggevano senza errori.

## Come si fa

```python
import sys; sys.path.insert(0, 'tools')
from delugexml import parse_file, write_file, musica as MU
from delugexml import song as S, create as C, arranger as A, midicv, audio
from delugexml.writer import FormatTable
```

| per | usare |
|---|---|
| leggere cosa c'è | `MU.racconta(doc)` |
| altezze | `MU.altezza('re2')`, `MU.nome_altezza(38)` |
| pattern di batteria | `MU.passi('x...x...x...x...')` |
| melodie | `MU.melodia('re2 fa#2 la2', durata='1/8')` |
| nuova traccia da preset | `C.add_track(doc, preset, name=…, folder=…)` |
| note | `S.write_notes(S.add_note_row(clip, y), note, create=True)` |
| arrangiamento | `A.place(doc, strumento, clip, pos=…, length=…)` poi `A.fit_view(doc)` |
| variazione indipendente | `A.place_unique(...)` — la clip "bianca" |
| suono e mix | `MU.applica_verbo(doc, nodo, 'piu scuro')` |
| controllo | `MU.verifica(doc)` |
| scrivere | `write_file(doc, path, FormatTable.load('out/format_table.json'))` |

## Trasferimento

```bash
.venv/Scripts/python.exe tools/dsysex.py --in "Deluge 0" --out "Deluge 1" get "/SONGS/DelugePal/NOME.XML" locale.XML
.venv/Scripts/python.exe tools/dsysex.py --in "Deluge 0" --out "Deluge 1" put locale.XML "/SONGS/DelugePal/NOME02.XML"
```

Le porte vanno sempre indicate. `put` rilegge e confronta gli hash da sé.

## Quando qualcosa va storto

| caso | cosa fare |
|---|---|
| `verifica()` non vuota | **non caricare**, riferire il problema in chiaro |
| Deluge non collegato (`ping` non risponde) | scrivere il file locale e dirlo; non fingere che sia salito |
| il nome remoto esiste già | incrementare la versione, mai forzare |
| il campione di una clip audio non è sulla SD | `audio.wav_frames` non può leggerlo: chiedere il percorso, non indovinare le posizioni |
| verbo di suono sconosciuto | dire quali esistono (`musica.verbi_disponibili()`) |
| il dispositivo rifiuta il file | è un difetto nostro, non un mistero del formato: bisezionare da un file che funziona, un fattore per volta |

## Altre skill

| per | skill |
|---|---|
| convenzioni di genere, teoria, progressioni | `music-composer` — è un **pavimento**: dà tempi e strumenti tipici, non come si muove un groove. I suoi `scripts/*.py` producono file MIDI e **non si usano** |
| sintesi, filtri, timbro | `dsp-recipes` |
| come suona la roba di questo utente | `docs/MUSICA.md` |

## Quando qualcosa non si vede sul dispositivo

Quattro volte su quattro il contenuto era giusto e mancava uno stato di
vista: `yScrollSongView`, `beingEdited`, lo scroll della clip, la finestra
dell'arranger. Prima di sospettare il dato, controllare la vista — e in ogni
caso **misurare con una coppia controllata**, non dedurre.
```

- [ ] **Passo 4: verificare che la skill sia vista**

Riavviare la sessione o lanciare:

```bash
ls -R .claude/skills/deluge-pal/ && head -4 .claude/skills/deluge-pal/SKILL.md
```

Atteso: il frontmatter con `name: deluge-pal`.

- [ ] **Passo 5: committare**

```bash
git add .claude/skills/deluge-pal/SKILL.md docs/MUSICA.md
git commit -m "skill deluge-pal: il protocollo del ciclo, e MUSICA.md da riempire"
```

---

### Task 8: Prova di accettazione sul dispositivo

**File:**
- Creare: `D:\DelugePal\out\PAL01.XML` (generato, ignorato da git)
- Creare: `D:\DelugePal\out\genera_pal01.py` (script di generazione)

**Interfacce:**
- Consuma: tutto

Nessun test automatico chiude questa fase. **La regola del progetto è che ogni fase si chiude sullo schermo del Deluge**, non sul round-trip.

- [ ] **Passo 1: generare una song da una descrizione a parole**

La descrizione: *«un pezzo in re minore a 124, kick sui quarti con rim sul 2 e 4, un basso che fa re-fa-la in crome, otto battute in arrangiamento»*. Salvare come `D:\DelugePal\out\genera_pal01.py` ed eseguirlo **da `D:\DelugePal`**:

```python
import sys
sys.path.insert(0, 'tools')
from delugexml import parse_file, write_file
from delugexml import song as S, create as C, arranger as A, musica as MU
from delugexml.writer import FormatTable

doc = parse_file('refs/songs/TEMPL0.XML')
S.set_bpm(doc.root, 124)
S.set_scale(doc, 're', 'minore')

# batteria
kit, kclip = C.add_track(doc, 'refs/kits/CR78FROMMARS.XML',
                         name='CR78FROMMARS', folder='KITS', length=384)
for drum, pattern in (('Kick CR78 12', 'x...x...x...x...'),
                      ('Rim CR78 02',  '....x.......x...')):
    riga = S.add_note_row(kclip, S.drum_index(doc, kclip, drum))
    S.write_notes(riga, MU.passi(pattern), create=True)

# basso: le note della clip che TEMPL0 porta gia'
basso = doc.root.find('sessionClips').children[0]
for y, note in MU.melodia('re2 fa2 la2 re3 la2 fa2 re2 .',
                          durata='1/8').items():
    S.write_notes(S.add_note_row(basso, y), note, create=True)
S.fit_clip_scroll_to_notes(doc, basso)

# arrangiamento: otto battute, le due tracce insieme
for strumento, clip in ((S.instrument_of(doc, basso), basso), (kit, kclip)):
    A.place(doc, strumento, clip, pos=0, length=8 * 384)
A.fit_view(doc)

problemi = MU.verifica(doc)
if problemi:
    sys.exit('il cancello e chiuso: ' + '; '.join(problemi))
write_file(doc, 'out/PAL01.XML', FormatTable.load('out/format_table.json'))
print(MU.racconta(doc))
```

Verificato: `TEMPL0.XML` contiene un solo `<sound>` chiamato `BOD2-01-RIGHT-PLACE` con una clip vuota, ed è in re maggiore — quindi `set_scale(doc, 're', 'minore')` cambia davvero il modo. I nomi dei modi ammessi sono `maggiore, minore, dorico, frigio, lidio, misolidio, locrio, minore armonica, minore melodica`.

Se i nomi dei drum del kit sono diversi da quelli scritti, leggerli con `S.drum_names(doc, kclip)` e correggerli — non aggirare il problema saltando il controllo.

- [ ] **Passo 2: raccontarla prima di caricarla**

```bash
cd /d/DelugePal && .venv/Scripts/python.exe -c "import sys;sys.path.insert(0,'tools');from delugexml import parse_file,musica as MU;print(MU.racconta(parse_file('out/PAL01.XML')))"
```

Il racconto deve corrispondere a quello che si è chiesto. Se non corrisponde, il difetto è nel codice, non nel Deluge.

- [ ] **Passo 3: passare il cancello**

```bash
cd /d/DelugePal && .venv/Scripts/python.exe -c "import sys;sys.path.insert(0,'tools');from delugexml import parse_file,musica as MU;print(MU.verifica(parse_file('out/PAL01.XML')) or 'pulito')"
```

Atteso: `pulito`. Se no, **non caricare**.

- [ ] **Passo 4: caricare e far ascoltare**

```bash
cd /d/DelugePal && .venv/Scripts/python.exe tools/dsysex.py --in "Deluge 0" --out "Deluge 1" put out/PAL01.XML "/SONGS/PAL01.XML"
```

Dire all'utente cosa aspettarsi, **prima** che guardi: quali tracce, quali battute, cosa deve sentire. Una previsione dichiarata in anticipo è ciò che rende la verifica un test.

- [ ] **Passo 5: chiudere il ciclo almeno una volta**

Chiedere una modifica, riscaricare `PAL01`, applicarla, ricaricare come `PAL02`, e far riascoltare. **La fase è chiusa quando il ciclo ha girato una volta intera**, non quando i test passano.

- [ ] **Passo 6: registrare**

Aggiornare `HANDOFF.md` e `docs/PROSSIMI_PASSI.md` (fase 7 fatta), e annotare in `docs/MUSICA.md` la prima correzione ricevuta.

```bash
git add -A && git commit -m "fase 7 verificata sul dispositivo: il ciclo gira"
```
