# La rifondazione di `MUSICA.md` sullo schema neutro — piano di implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Trasformare `docs/MUSICA.md` da documento a forma di reggae in uno
schema di undici caselle indipendente dal repertorio, con il reggae e il jazz
come due schede compilate in `docs/repertori/`.

**Architecture:** `MUSICA.md` tiene tre cose — lo schema (le undici domande),
il comune (ciò che vale per ogni repertorio) e l'indice (una matrice repertorio
× casella che è anche l'agenda). Ogni repertorio è un file separato con le
stesse undici sezioni nello stesso ordine, sempre tutte presenti anche quando
vuote. Il contenuto attuale **si sposta**, non si riscrive.

**Tech Stack:** Markdown. Python 3.13 di sistema per i due test, dentro
`tests/test_all.py`, che non usa pytest e non ha dipendenze.

## Global Constraints

- **Tutto in italiano.** `docs/` non si traduce.
- **Le frasi si spostano come sono.** Cambiano solo titoli, ordine e le poche
  righe di raccordo. Griglie a 16 passi, numeri di velocity, tabelle e
  citazioni dell'utente restano parola per parola.
- **Se un pezzo non entra in nessuna delle undici caselle, è lo schema a essere
  sbagliato.** Ci si ferma e lo si dice, non si butta via il contenuto.
- **Un numero vive in una casella sola.** Mai copiare un valore in due file:
  si rimanda.
- **I marcatori di provenienza restano dove sono** — `[MIS]`, `[WEB]`, `[OSS]`,
  `[IPO]`, `[MAN]` accanto all'affermazione che qualificano, mai nell'indice.
- **Non si tocca `FINDINGS.md` né `ARCHITETTURA.md`.**
- **Non si cerca materiale nuovo.** Il jazz si compila con quello che c'è.
- **I file si leggono e scrivono in UTF-8 esplicito** (`encoding='utf-8'`):
  su Windows il default è cp1252 e i simboli dell'indice si romperebbero.
- **Niente carattere non-ASCII nell'output dei test.** `check()` stampa su
  console Windows: `●`, `◐`, `○` vanno tradotti in `pieno`/`parziale`/`vuoto`
  prima di finire in una stringa stampata.
- Baseline della migrazione: **`94c52d8`**, l'ultimo commit in cui
  `docs/MUSICA.md` è ancora quello vecchio.

## Struttura dei file

| file | responsabilità |
|---|---|
| `docs/MUSICA.md` | schema, comune, indice. Nessun contenuto di repertorio |
| `docs/repertori/reggae-dub.md` | le 11 caselle: 6 piene, 4 parziali, 1 vuota |
| `docs/repertori/jazz.md` | le 11 caselle: 1 piena, 3 parziali, 7 vuote |
| `tests/test_all.py` | due test nuovi: struttura delle schede, coerenza dell'indice |
| `.claude/skills/deluge-pal/SKILL.md` | due rimandi da aggiornare |
| `HANDOFF.md` | tre rimandi da aggiornare — **fuori spec**, vedi Task 9 |

### Le convenzioni che i test faranno rispettare

1. **Una casella è un titolo `## `**, esattamente due cancelletti. Tutto ciò
   che sta dentro una casella e vuole un titolo usa `### ` o più.
2. **Le undici caselle ci sono sempre tutte, in ordine**, con questo testo
   esatto:

```
## 1. Cos'è, e cosa non è
## 2. Metro e griglia
## 3. Tempo
## 4. Feel
## 5. Ruoli e spartizione
## 6. Dinamica
## 7. Armonia
## 8. Melodia e ornamentazione
## 9. Forma e densità
## 10. Sul Deluge
## 11. Trappole del generatore
```

3. **Lo stato di una casella si legge dalla sua prima riga non vuota:**
   comincia con `**Vuota.**` → vuota; con `**Parziale.**` → parziale;
   qualunque altra cosa → piena. Non c'è un quarto stato.
4. **Una casella vuota o parziale dice cosa servirebbe per completarla**, nella
   stessa riga o subito sotto. È l'agenda.

---

## Task 1: Lo scheletro delle schede e il test di struttura

**Files:**
- Create: `docs/repertori/reggae-dub.md`
- Create: `docs/repertori/jazz.md`
- Modify: `tests/test_all.py` (in fondo, prima del blocco `if __name__`)

**Interfaces:**
- Produces: la costante `CASELLE` e la funzione `_caselle_di(path)` in
  `tests/test_all.py`, usate anche dal Task 6.

- [ ] **Step 1: Scrivere il test che fallisce**

In fondo a `tests/test_all.py`, subito prima di `if __name__ == '__main__':`

```python
# ------------------------------------------------- docs: lo schema neutro

REPERTORI = ROOT / 'docs' / 'repertori'

#: Le undici caselle dello schema neutro, nell'ordine fisso. Il testo del
#: titolo e' il numero, un punto, uno spazio e questa stringa. Vedi
#: docs/superpowers/specs/2026-08-17-musica-schema-neutro-design.md
CASELLE = [
    "Cos'è, e cosa non è",
    'Metro e griglia',
    'Tempo',
    'Feel',
    'Ruoli e spartizione',
    'Dinamica',
    'Armonia',
    'Melodia e ornamentazione',
    'Forma e densità',
    'Sul Deluge',
    'Trappole del generatore',
]


def _caselle_di(path):
    """I titoli di casella di una scheda, nell'ordine in cui compaiono.

    Una casella e' un titolo di livello 2 esatto: '### ' non conta, cosi'
    una scheda puo' articolarsi dentro una casella senza confondere il test.
    """
    righe = path.read_text(encoding='utf-8').splitlines()
    return [r.rstrip() for r in righe if r.startswith('## ')]


def test_schede_repertorio_hanno_le_undici_caselle():
    attesi = [f'## {i}. {c}' for i, c in enumerate(CASELLE, 1)]
    schede = sorted(REPERTORI.glob('*.md')) if REPERTORI.is_dir() else []
    check('esistono le schede di repertorio', len(schede) >= 1,
          f'{len(schede)} in {REPERTORI}')
    for s in schede:
        trovati = _caselle_di(s)
        check(f'{s.name}: le undici caselle, tutte e in ordine',
              trovati == attesi,
              f'{len(trovati)} titoli, primo scarto: '
              + next((f'atteso {a!r} trovato {t!r}'
                      for a, t in zip(attesi, trovati) if a != t), 'nessuno'))
```

- [ ] **Step 2: Eseguire e verificare che fallisca**

```bash
python tests/test_all.py 2>&1 | grep -i "casella\|schede di repertorio"
```

Atteso: `FAIL  esistono le schede di repertorio — 0 in ...\docs\repertori`,
e nessuna riga per le singole schede.

- [ ] **Step 3: Creare le due schede, solo lo scheletro**

`docs/repertori/reggae-dub.md`:

```markdown
# Reggae e dub

> Una scheda dello schema neutro. Lo schema, il materiale comune a tutti i
> repertori e l'indice stanno in [`../MUSICA.md`](../MUSICA.md).

## 1. Cos'è, e cosa non è

**Vuota.** Da compilare nel Task 4.

## 2. Metro e griglia

**Vuota.** Da compilare nel Task 4.

## 3. Tempo

**Vuota.** Da compilare nel Task 4.

## 4. Feel

**Vuota.** Da compilare nel Task 4.

## 5. Ruoli e spartizione

**Vuota.** Da compilare nel Task 4.

## 6. Dinamica

**Vuota.** Da compilare nel Task 4.

## 7. Armonia

**Vuota.** Da compilare nel Task 4.

## 8. Melodia e ornamentazione

**Vuota.** Da compilare nel Task 4.

## 9. Forma e densità

**Vuota.** Da compilare nel Task 4.

## 10. Sul Deluge

**Vuota.** Da compilare nel Task 4.

## 11. Trappole del generatore

**Vuota.** Da compilare nel Task 4.
```

`docs/repertori/jazz.md`: identico, con `# Jazz` come titolo e «Task 5» al
posto di «Task 4» nelle undici righe.

- [ ] **Step 4: Eseguire e verificare che passi**

```bash
python tests/test_all.py 2>&1 | grep -i "casella\|schede di repertorio"
```

Atteso: tre `PASS` — l'esistenza, `jazz.md`, `reggae-dub.md`.

- [ ] **Step 5: Eseguire la suite intera, per non aver rotto altro**

```bash
python tests/test_all.py 2>&1 | tail -5
```

Atteso: il totale sale di 3 rispetto a prima e i FAIL restano quelli noti
(0 con il corpus sul disco; 2 senza, entrambi documentati in `HANDOFF.md` §2).

- [ ] **Step 6: Commit**

```bash
git add docs/repertori tests/test_all.py
git commit -m "musica: lo scheletro delle schede di repertorio, e il test che le tiene in riga"
```

---

## Task 2: La rete di sicurezza della migrazione

Uno script usa e getta: dice quali righe del vecchio `MUSICA.md` non sono
atterrate da nessuna parte, e quali sono atterrate in due posti. Sta nello
scratchpad e **non entra nel repo**: dopo la migrazione non ha più uso.

**Files:**
- Create: `<scratchpad>/verifica_migrazione.py`

**Interfaces:**
- Produces: `python <scratchpad>/verifica_migrazione.py` stampa due elenchi,
  `ORFANE` e `DOPPIE`. Usato nei Task 3, 4, 5 come indicatore e nel Task 7
  come cancello.

- [ ] **Step 1: Scrivere lo script**

```python
"""Confronta il MUSICA.md di 94c52d8 con i tre file nuovi.

ORFANE: righe del vecchio che non compaiono in nessuno dei nuovi. Ognuna va
        o rimessa, o giustificata come riga di raccordo riscritta.
DOPPIE: righe presenti in piu' di un file nuovo. Violano "un numero vive in
        una casella sola" — a meno che non siano prosa di servizio.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve()
while not (ROOT / '.git').is_dir():
    ROOT = ROOT.parent

BASELINE = '94c52d8'
NUOVI = [
    ROOT / 'docs' / 'MUSICA.md',
    ROOT / 'docs' / 'repertori' / 'reggae-dub.md',
    ROOT / 'docs' / 'repertori' / 'jazz.md',
]

# righe che non portano contenuto: titoli, separatori, delimitatori di blocco
def portante(t):
    return bool(t) and not t.startswith('#') and t not in ('---', '```', '```python', '```bash', '>')

vecchio = subprocess.run(
    ['git', 'show', f'{BASELINE}:docs/MUSICA.md'],
    capture_output=True, text=True, encoding='utf-8', cwd=ROOT, check=True).stdout

testi = {}
for p in NUOVI:
    testi[p.name] = p.read_text(encoding='utf-8') if p.exists() else ''

orfane, doppie = [], []
for n, riga in enumerate(vecchio.splitlines(), 1):
    t = riga.strip()
    if not portante(t):
        continue
    dove = [nome for nome, testo in testi.items() if t in testo]
    if not dove:
        orfane.append((n, t))
    elif len(dove) > 1:
        doppie.append((n, t, dove))

print(f'ORFANE ({len(orfane)}) — righe del vecchio che non sono atterrate:')
for n, t in orfane:
    print(f'  {n:4}  {t[:110]}')
print(f'\nDOPPIE ({len(doppie)}) — righe presenti in piu di un file:')
for n, t, dove in doppie:
    print(f'  {n:4}  [{" + ".join(dove)}]  {t[:90]}')
sys.exit(0)
```

- [ ] **Step 2: Eseguirlo sulla situazione attuale, per tararlo**

```bash
python "$SCRATCH/verifica_migrazione.py" | head -20
```

`$SCRATCH` è
`C:/Users/polde/AppData/Local/Temp/claude/D--DelugePal/9e8a3ae8-f37d-491f-80f3-3b1ef116390d/scratchpad`.

Atteso adesso, con `MUSICA.md` ancora intatto: **`ORFANE (0)`** — ogni riga del
vecchio sta ancora nel vecchio, che è uno dei tre file nuovi. `DOPPIE` può
essere diverso da zero se una riga breve compare per caso anche in una scheda
scheletro: va guardato e ignorato se è prosa di servizio.

Se `ORFANE` non è 0 qui, lo script è sbagliato e va corretto prima di
proseguire — è l'unico momento in cui si conosce la risposta giusta in
anticipo.

- [ ] **Step 3: Nessun commit**

Lo script sta nello scratchpad e non va aggiunto a git. Verificare:

```bash
git status --short
```

Atteso: nessuna riga che nomini `verifica_migrazione.py`.

---

## Task 3: `MUSICA.md` — lo schema e il comune

Il file viene **riscritto**, ma il suo contenuto trasversale viene **spostato**
dalle sezioni attuali. Il contenuto di repertorio esce e sparisce da qui: lo
raccoglieranno i Task 4 e 5, che leggono il vecchio file da git.

**Files:**
- Modify: `docs/MUSICA.md` (riscrittura integrale)

**Interfaces:**
- Consumes: le convenzioni di titolo del Task 1.
- Produces: `docs/MUSICA.md` con tre parti — schema, comune, indice. L'indice
  arriva vuoto e lo compila il Task 6.

- [ ] **Step 1: Mettere da parte il vecchio, per averlo sott'occhio**

```bash
git show 94c52d8:docs/MUSICA.md > "$SCRATCH/MUSICA_prima.md"
```

- [ ] **Step 2: Scrivere la testa e lo schema**

Testa: cos'è il file, che non è una teoria generale della musica, la
disciplina dei marcatori, e **come si legge** — lo schema più una scheda sola,
mai tutte. Poi le undici caselle con due o tre righe l'una: *cosa vuol dire
compilarla* e *cosa vuol dire lasciarla vuota*. Il testo dei titoli è quello
del Task 1.

Dentro lo schema vanno dette, perché sono le ragioni per cui le caselle sono
quelle:

- il test che le ha scelte: **devono sopravvivere sia a Josquin sia alla
  jungle**;
- che l'*inégalité* barocca e lo swing del jazz cadono **nella stessa casella
  4**, ed è il guadagno vero dello schema;
- che **una casella vuota è informazione**, e dichiara cosa servirebbe.

- [ ] **Step 3: Spostare il comune, sezione per sezione**

Dodici blocchi, tutti da `$SCRATCH/MUSICA_prima.md`. Le righe indicate sono
quelle del vecchio file.

| dal vecchio | righe | va in |
|---|---|---|
| «Norme di sound design» intera, compreso «La risonanza non ha una soglia: ha un compenso» e «Come si applica quando c'è un LFO sul filtro» | 33-93 | comune → la macchina |
| «Il corpus non è autoritativo» intera, con la tabella delle fonti | 95-117 | comune → metodo |
| «Preset e come vengono usati» intera | 119-136 | comune → la macchina |
| «Velocity groove» dalla richiesta dell'utente alla scala 0-127 e alle escursioni per strumento, **senza** il one drop | 252-296 | comune → il mestiere |
| «Ma swing e laid-back non sono la stessa cosa», con i 96 tick, gli 8,9 ms e la nota su `MU.sposta()`/`MU.laid_back()` | 325-356 | comune → il mestiere |
| il **meccanismo** di `set_swing` e `swingInterval`: la formula display↔BUR, la tabella 4-8, il default 7 del firmware | 481-518 | comune → la macchina |
| «L'arco di densità» e i tre errori da generatore, **senza** l'arco dub d'esempio (599-612) | 567-597 | comune → il mestiere |
| «Il turnaround corregge un caso su quattro», la parte generale: variare è scelto, non randomizzato | 620-636 | comune → il mestiere |
| «Cassa e basso sono una coppia», la regola generale | 638-646 | comune → il mestiere |
| «La playability è una decisione, non una regola» intera | 659-675 | comune → il mestiere |
| «Il ciclo di revisione ha un protocollo»: Keep / Change / Direction | 677-702 | comune → metodo |
| dalla testa: che una fonte grande non è autorevole su tutto, e la tabella delle due skill | 7-29 | comune → metodo |
| «leggi anche documentazione», «leggi anche docs community» — con data e frase | 708-716 | comune → metodo |
| «ora ci sono 4 envelope, non 2» — con data e frase | 740-745 | comune → la macchina |

Le ultime due sono correzioni ricevute: **conservano la data e la frase
testuale dell'utente**, come dice la spec §6. Il registro cronologico non
esiste più e non se ne fa un indice.

Tre avvertenze su questo passo:

- **il meccanismo di `set_swing` sì, i valori per stile no.** La tabella
  `repertorio → display` (righe 521-529 del vecchio) è del jazz e va nella sua
  scheda: qui resta solo come si converte un BUR in un display e cosa fa
  `swingInterval`.
- **la misura di come lo si è stabilito non si copia**: sta in `FINDINGS.md`
  §6-undecies, e da qui ci si rimanda.
- lo specifico su reggae della testa vecchia — che `music-composition` dice
  «skank precisely on 2 and 4» e sbaglia il posto — **non** è comune: va in
  `reggae-dub.md` casella 11 (Task 4).

- [ ] **Step 4: Lasciare il posto all'indice**

In fondo, una sezione `## L'indice dei repertori` con una riga che dice che la
compila il Task 6. Non inventare la matrice adesso: dipende dallo stato vero
delle schede.

- [ ] **Step 5: Eseguire la rete di sicurezza**

```bash
python "$SCRATCH/verifica_migrazione.py" | head -60
```

Atteso: molte `ORFANE` — tutto il reggae e tutto il jazz, che i Task 4 e 5 non
hanno ancora raccolto. **Va guardato che fra le orfane non ci sia niente di
trasversale**: se compare una riga sulle norme di sound design o sul protocollo
di revisione, è stata persa in questo Task e va rimessa ora.

- [ ] **Step 6: Eseguire la suite**

```bash
python tests/test_all.py 2>&1 | tail -5
```

Atteso: come al Task 1, nessuna regressione.

- [ ] **Step 7: Commit**

```bash
git add docs/MUSICA.md
git commit -m "musica: MUSICA.md diventa lo schema e il comune"
```

---

## Task 4: La scheda `reggae-dub.md`

Il contenuto viene tutto da `$SCRATCH/MUSICA_prima.md`. **Le frasi si spostano
come sono.**

**Files:**
- Modify: `docs/repertori/reggae-dub.md`

**Interfaces:**
- Consumes: lo scheletro del Task 1, le convenzioni di stato del Task 1 §3.
- Produces: una scheda con 6 caselle piene, 4 parziali, 1 vuota — lo stato che
  il Task 6 confronterà con l'indice.

- [ ] **Step 1: Compilare le sei caselle piene**

| casella | dal vecchio, righe | cosa ci va |
|---|---|---|
| **2. Metro e griglia** | 155-170 | la griglia a 16 passi con le sei righe (charleston, cassa, rullante, skank, bubble, basso), e che una griglia è **una battuta** |
| **3. Tempo** | 203-204 | 50-100 BPM, 70-78 al centro del roots, e che 70 non è «lento per il dub» ma il posto giusto |
| **5. Ruoli e spartizione** | 155-158, 177-201, 207-227 | che il reggae è definito dalla **spartizione ritmica**, non dall'armonia; la batteria e le tre varianti di cassa; il basso come **strumento solista** con la quinta sotto la tonica; lo skank come armonia in levare. Più il rapporto cassa/basso **istanziato**: il basso suona l'uno che la batteria lascia vuoto (639-657) |
| **6. Dinamica** | 298-306, 363-391 | il velocity groove del one drop, e i pattern `hat`/`kick`/`rim` con il turnaround, lo skank e il bubble |
| **10. Sul Deluge** | 78-80, 229-241 | il kit sintetizzato dal synth vuoto, i patch cable di wobble e sirena, delay e riverbero come **strumenti compositivi**, i buchi fra le istanze in `arranger.py`, e la sirena di `DUBPAL02` con risonanza 12 e volume 17 |
| **11. Trappole del generatore** | 14-23, 142-148, 718-738 | la tabella dei sette errori di `DUBPAL01` con data e frase dell'utente; che nessuna delle due skill sa il reggae; che `music-composition` mette lo **skank sui passi 4 e 12** invece che su tutti i levare; e «una ricerca sola dà le etichette, non il mestiere» |

- [ ] **Step 2: Compilare le quattro caselle parziali**

Ognuna comincia con `**Parziale.**` e dice **di cosa** è parziale.

| casella | dal vecchio | cosa manca, da dichiarare |
|---|---|---|
| **1. Cos'è, e cosa non è** | 229-241, 172-176 | c'è il dub come *pratica* e la confusione skank/charleston. Manca il confine col vicino più insidioso — rocksteady, ska, dancehall — che nessuna fonte letta copre |
| **4. Feel** | 309-323, 346-356 | c'è che il one drop è swingato e laid-back, e che `set_swing(50)` era sbagliato. Manca **il numero**: nessuna misura, solo `[WEB]`. E `MU.laid_back()` non esiste — `MU.sposta()` trasla e basta, le note oltre la fine della clip restano fuori |
| **7. Armonia** | 222-227 | c'è il ritmo armonico: pochi accordi, spesso due alternati, e il carattere sta nello skank. Manca il vocabolario — nessuna progressione tipica, nessuna sigla |
| **9. Forma e densità** | 599-612 | c'è l'arco dub a sette tratti. È `[WEB/skill]`, **non misurato su niente**, e va detto: è la forma standard applicata al dub, da correggere all'ascolto |

- [ ] **Step 3: Dichiarare la casella vuota**

```markdown
## 8. Melodia e ornamentazione

**Vuota.** Nel roots la melodia è la linea di basso, che sta nella casella 5
come *ruolo*; qui servirebbe il materiale melodico vero — la voce, i fiati,
il melodica — e nessuna delle fonti lette lo copre. La chiuderebbero le
librerie MIDI per genere già in `to-read/MIDI/`, compresa
`(aq) Dub Beat Builder`, che però nessuno ha ancora aperto.
```

- [ ] **Step 4: Riportare le fonti in fondo**

Le sei fonti `[WEB]` del vecchio (righe 245-250) vanno in fondo alla scheda,
come sono.

- [ ] **Step 5: Verificare struttura e stato**

```bash
python tests/test_all.py 2>&1 | grep -i "reggae-dub"
```

Atteso: `PASS  reggae-dub.md: le undici caselle, tutte e in ordine`.

```bash
grep -c "^\*\*Vuota\.\*\*" docs/repertori/reggae-dub.md
grep -c "^\*\*Parziale\.\*\*" docs/repertori/reggae-dub.md
```

Atteso: `1` e `4`.

- [ ] **Step 6: Commit**

```bash
git add docs/repertori/reggae-dub.md
git commit -m "musica: il reggae diventa una scheda, sei caselle piene e una vuota"
```

---

## Task 5: La scheda `jazz.md`

**Files:**
- Modify: `docs/repertori/jazz.md`

**Interfaces:**
- Consumes: lo scheletro del Task 1.
- Produces: una scheda con 1 casella piena, 3 parziali, 7 vuote.

- [ ] **Step 1: Compilare la casella 4, l'unica piena**

Da `$SCRATCH/MUSICA_prima.md` righe 393-479, per intero: i numeri complessivi
(levare al 61,7%, BUR 1,61, quartili 56,8-65,9%), le tre tabelle — per stile,
per feel dichiarato, per tempo — il racconto dei tre tentativi che davano 1,10
/ 1,19 / 1,10, e le due cautele: che il valore assoluto non è riconciliato con
«Playing It Straight» (~1,3 sullo stesso database, metodo dietro paywall) e che
sotto i 120 BPM la misura guarda probabilmente le semicrome `[OSS]`.

È l'unica casella `[MIS]` del documento intero: va detto.

- [ ] **Step 2: Compilare le tre parziali**

```markdown
## 3. Tempo

**Parziale.** Non c'è un range dichiarato del repertorio: quello che c'è sono
le quattro fasce su cui è stato misurato lo swing — ≤ 120, 120-180, 180-240,
> 240 BPM — che dicono dove il materiale vive davvero (333 assoli, il grosso
fra 120 e 240). Manca il tempo *tipico* per stile, che `wjazzd.db` ha e che
non è stato ancora estratto.
```

Casella **7. Armonia**, parziale: c'è il vocabolario — `MU.armonia()`,
`MU.voci()`, `MU.sigla()`, i quattro voicing di `MU.VOICING` (`chiuso`,
`shell`, `senza-fondamentale`, `drop2`) e il dialetto di Weimar letto da
`WJ.sigla_weimar()`, 419 simboli su 419. Manca **la condotta delle parti**:
ogni accordo è costruito per conto suo, e i voicing alternati A/B del ii-V-I
non sono implementati. Rimandare a `HANDOFF.md` §6-octies, senza ricopiarne i
numeri.

Casella **10. Sul Deluge**, parziale: per il jazz serve
`S.set_swing(doc, 62, figura='1/8')`, perché il default del firmware swinga le
semicrome e su una linea di crome non muove niente. Qui va **solo** la tabella
di conversione, senza la colonna BUR — quella sta nella casella 4:

```markdown
| repertorio | `set_swing(doc, …, figura='1/8')` |
|---|---|
| dritto | 50 |
| **jazz complessivo** | **62** |
| HARDBOP · BEBOP | 64 |
| POSTBOP | 60 |
| FUSION | 56 |
| terzina esatta | 67 |
```

Manca tutto il resto: nessun pezzo jazz è mai stato generato, quindi del
suono, dei kit e dell'arrangiamento jazz sul Deluge non si sa niente.

- [ ] **Step 3: Dichiarare le sette vuote, ognuna con cosa la chiuderebbe**

```markdown
## 1. Cos'è, e cosa non è

**Vuota.** Servirebbe la delimitazione fra gli stili, che `wjazzd.db` ha già
come etichette — TRADITIONAL, SWING, BEBOP, COOL, HARDBOP, POSTBOP, FREE,
FUSION — e che nessuno ha ancora letto se non per filtrare la misura dello
swing.

## 2. Metro e griglia

**Vuota.** La chiuderebbe una misura sulle metriche di `wjazzd.db`, che porta
`bar/beat/tatum/division` per 200 809 note.

## 5. Ruoli e spartizione

**Vuota.** È la casella più difficile da chiudere con il materiale in casa:
`wjazzd.db` trascrive **la linea solista**, non l'accompagnamento, quindi del
rapporto fra comping, walking e solista non dice niente. Servirebbe MusicXML.

## 6. Dinamica

**Vuota.** La chiuderebbe il Groove MIDI
(`to-read/MIDI/groove-v1.0.0-midionly.zip`, in attesa di decompressione):
porta velocity e microtiming misurati per genere, e farebbe per la batteria
quello che la Weimar ha fatto per lo swing.

## 8. Melodia e ornamentazione

**Vuota, ed è la più vicina a chiudersi.** `wjazzd.db` è esattamente questo —
456 assoli trascritti a mano con **gli accordi allineati alla linea** — ed è
già su disco e già leggibile con `WJ.melodia()` e `WJ.armonia()`. Manca solo
guardarlo per lo sviluppo motivico invece che per lo swing.

## 9. Forma e densità

**Vuota.** AABA, il blues di dodici battute, il rhythm changes: niente di
tutto questo è scritto. La chiuderebbe MusicXML, o le lead sheet.

## 11. Trappole del generatore

**Vuota, e per una ragione precisa: nessun pezzo jazz è ancora stato
generato**, quindi nessuna trappola è stata osservata. Questa casella si
riempie al primo ascolto corretto dall'utente, come è successo al dub.
```

- [ ] **Step 4: Verificare struttura e stato**

```bash
python tests/test_all.py 2>&1 | grep -i "jazz.md"
grep -c "^\*\*Vuota" docs/repertori/jazz.md
grep -c "^\*\*Parziale\.\*\*" docs/repertori/jazz.md
```

Atteso: `PASS` sulla struttura, `7` vuote, `3` parziali.

⚠️ Il conteggio usa `^\*\*Vuota` **senza il punto finale**, perché due caselle
di questa scheda dicono `**Vuota, ed è la più vicina a chiudersi.**` e
`**Vuota, e per una ragione precisa: …**`. È il motivo per cui la convenzione
del Task 1 §3 dice *comincia con* e non *è uguale a*, e per cui `_stato_di()`
nel Task 6 è già scritta con `startswith('**Vuota')`: non va cambiata, va
lasciata così. Una casella **parziale** invece comincia sempre con
`**Parziale.**` esatto, punto compreso.

- [ ] **Step 5: Commit**

```bash
git add docs/repertori/jazz.md
git commit -m "musica: la scheda del jazz, una casella misurata e sette vuote"
```

---

## Task 6: L'indice, e il test che gli impedisce di derivare

**Files:**
- Modify: `docs/MUSICA.md` (la sezione lasciata vuota dal Task 3)
- Modify: `tests/test_all.py`

**Interfaces:**
- Consumes: `CASELLE` e `_caselle_di()` dal Task 1; lo stato dichiarato dalle
  schede dei Task 4 e 5.
- Produces: `_stato_di(path)` → lista di 11 stringhe fra `'pieno'`,
  `'parziale'`, `'vuoto'`.

- [ ] **Step 1: Scrivere il test che fallisce**

Sotto `test_schede_repertorio_hanno_le_undici_caselle` in `tests/test_all.py`:

```python
#: L'indice di MUSICA.md usa simboli; i test stampano su console Windows,
#: dove un carattere non-ASCII in una stringa stampata solleva
#: UnicodeEncodeError. Si traduce prima di stampare, mai dopo.
SIMBOLI = {'\u25cf': 'pieno', '\u25d0': 'parziale', '\u25cb': 'vuoto'}


def _stato_di(path):
    """Lo stato delle undici caselle, letto dalla prima riga non vuota di ognuna.

    Convenzione: '**Vuota' -> vuoto, '**Parziale.**' -> parziale, altro ->
    pieno. Il prefisso di 'Vuota' e' senza punto perche' una casella puo'
    dire '**Vuota, ed e' la piu' vicina a chiudersi.**'
    """
    stato, attesa = [], False
    for riga in path.read_text(encoding='utf-8').splitlines():
        if riga.startswith('## '):
            attesa = True
            stato.append(None)
        elif attesa and riga.strip():
            attesa = False
            t = riga.strip()
            stato[-1] = ('vuoto' if t.startswith('**Vuota')
                         else 'parziale' if t.startswith('**Parziale.**')
                         else 'pieno')
    return stato


def _righe_indice():
    """Le righe della matrice di MUSICA.md, come {nome file: [stati]}."""
    fuori = {}
    for riga in (ROOT / 'docs' / 'MUSICA.md').read_text(encoding='utf-8').splitlines():
        if not riga.startswith('|') or '](repertori/' not in riga:
            continue
        celle = [c.strip() for c in riga.strip('|').split('|')]
        nome = celle[0].split('](repertori/')[1].rstrip(')')
        fuori[nome] = [SIMBOLI.get(c.strip('* '), c) for c in celle[1:]]
    return fuori


def test_indice_repertori_coerente_con_le_schede():
    indice = _righe_indice()
    schede = sorted(REPERTORI.glob('*.md')) if REPERTORI.is_dir() else []
    check('l indice nomina tutte le schede',
          set(indice) == {s.name for s in schede},
          f'indice {sorted(indice)} vs schede {[s.name for s in schede]}')
    for s in schede:
        vero = _stato_di(s)
        check(f'{s.name}: nessuna casella senza stato leggibile',
              None not in vero and len(vero) == 11, str(vero))
        check(f'{s.name}: l indice coincide con la scheda',
              indice.get(s.name) == vero,
              f'indice {indice.get(s.name)} vs scheda {vero}')
```

- [ ] **Step 2: Eseguire e verificare che fallisca**

```bash
python tests/test_all.py 2>&1 | grep -i "indice"
```

Atteso: `FAIL  l indice nomina tutte le schede — indice [] vs schede
['jazz.md', 'reggae-dub.md']`, perché la matrice non esiste ancora.

- [ ] **Step 3: Scrivere la matrice in `MUSICA.md`**

La prima colonna **deve** contenere un link `](repertori/<file>)`, o il test
non trova la riga. Le due righe aggregate non hanno link e il test le ignora.

```markdown
| repertorio | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [reggae / dub](repertori/reggae-dub.md) | ◐ | ● | ● | ◐ | ● | ● | ◐ | ○ | ◐ | ● | ● |
| [jazz](repertori/jazz.md) | ○ | ○ | ◐ | **●** | ○ | ○ | ◐ | ○ | ○ | ◐ | ○ |
| classica · barocca · antica | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| elettronica · IDM · techno · hip hop · trip hop · DnB · jungle | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |

`●` compilata · `◐` parziale, e la scheda dice di cosa · `○` vuota.

Il **grado di prova** non sta qui: `[MIS]`, `[WEB]`, `[OSS]`, `[IPO]`, `[MAN]`
stanno dentro la scheda, accanto all'affermazione che qualificano. La matrice
dice solo dove c'è qualcosa.
```

- [ ] **Step 4: Eseguire e verificare che passi**

```bash
python tests/test_all.py 2>&1 | grep -i "indice"
```

Atteso: cinque `PASS`. Se una riga non coincide, **è l'indice a sbagliare, non
la scheda**: la scheda è la fonte, l'indice ne è la vista.

- [ ] **Step 5: Commit**

```bash
git add docs/MUSICA.md tests/test_all.py
git commit -m "musica: l indice dei repertori, e il test che gli impedisce di derivare"
```

---

## Task 7: Il cancello della migrazione

**Files:** nessuno modificato, salvo correzioni che questo Task facesse
emergere.

- [ ] **Step 1: Eseguire la rete di sicurezza sul risultato finale**

```bash
python "$SCRATCH/verifica_migrazione.py"
```

- [ ] **Step 2: Giustificare ogni orfana, una per una**

Ogni riga in `ORFANE` è una riga del vecchio `MUSICA.md` che non esiste più da
nessuna parte. Per ognuna, esattamente due esiti ammessi:

- **è una riga di raccordo riscritta** (una transizione, un «e infatti», un
  titolo di paragrafo sciolto): si annota nel messaggio di commit e si va
  avanti;
- **è contenuto**: si rimette nella casella che gli compete, e si rieseguono i
  test dei Task 1 e 6.

**Nessun terzo esito.** Se una riga non entra in nessuna casella, si ferma qui
e lo si dice — è il vincolo globale: sarebbe lo schema a essere sbagliato.

- [ ] **Step 3: Guardare le doppie**

Ogni riga in `DOPPIE` che contenga **un numero, una sigla o un nome di
funzione** viola «un numero vive in una casella sola»: si tiene in un file solo
e negli altri si rimanda. Prosa di servizio ripetuta (`**Vuota.**`, righe di
intestazione) non è una violazione.

- [ ] **Step 4: Eseguire la suite intera**

```bash
python tests/test_all.py 2>&1 | tail -5
```

Atteso: nessun FAIL nuovo rispetto al Task 1.

- [ ] **Step 5: Commit, se il Task ha corretto qualcosa**

```bash
git add -A docs
git commit -m "musica: chiuse le righe rimaste orfane dalla migrazione"
```

Se non c'era niente da correggere, nessun commit: si annota l'esito e basta.

---

## Task 8: I rimandi in `SKILL.md`

**Files:**
- Modify: `.claude/skills/deluge-pal/SKILL.md:193` e `:195-200`

- [ ] **Step 1: Aggiornare la riga della tabella «Altre skill»**

Riga 193, oggi:

```
| **come si compone davvero in un genere** | `docs/MUSICA.md` — pattern per genere, velocity groove, arco di densità, e le correzioni ricevute |
```

Diventa:

```
| **come si compone davvero in un repertorio** | `docs/MUSICA.md` per lo schema e ciò che vale per tutti, poi **la sola scheda che serve** in `docs/repertori/`. Mai tutte: l'indice in fondo a `MUSICA.md` dice cosa c'è e cosa manca, casella per casella |
```

- [ ] **Step 2: Aggiornare l'avvertenza sotto**

Righe 195-200: il rimando «su reggae e dub comanda `docs/MUSICA.md`» diventa
«comanda `docs/repertori/reggae-dub.md`». Il resto dell'avvertenza — che
`music-composer` non li ha, che `music-composition` mette lo skank nel posto
sbagliato — resta parola per parola.

- [ ] **Step 3: Verificare che non restino rimandi vecchi**

```bash
grep -n "MUSICA.md" .claude/skills/deluge-pal/SKILL.md
```

Atteso: due occorrenze, entrambe nella forma nuova. Nessuna che prometta
«pattern per genere» dentro `MUSICA.md`.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/deluge-pal/SKILL.md
git commit -m "skill: il rimando allo schema e alla scheda, non piu' al file unico"
```

---

## Task 9: I rimandi in `HANDOFF.md` — **aggiunta fuori dalla spec**

> ⚠️ **La spec §7 dice che `SKILL.md` è l'unica modifica fuori da `docs/`.**
> Questo Task la eccede, e la ragione è che `HANDOFF.md` descrive `MUSICA.md`
> in tre punti con parole che dopo il Task 3 sono **false** — «non è più vuoto:
> convenzioni reggae/dub … e sei correzioni ricevute». Un handoff che descrive
> una struttura che non esiste è precisamente il difetto che questo progetto
> paga più spesso. **Va confermato prima di eseguirlo**; se non si conferma, si
> salta e il piano resta valido.

**Files:**
- Modify: `HANDOFF.md:44`, `:281`, `:193` (la voce della tabella dei documenti)

- [ ] **Step 1: Riga 44, la tabella «cosa c'è già in mano»**

Oggi promette «convenzioni reggae/dub con le griglie a 16 passi, velocity
groove con i numeri, catalogo di pattern per genere, e sei correzioni
ricevute». Diventa la descrizione dello schema: undici caselle, il comune,
l'indice, e due schede in `docs/repertori/` — con il fatto che **l'indice è
anche l'agenda**.

- [ ] **Step 2: Riga 281, l'ordine di lettura consigliato**

Il punto 3 diventa: `docs/MUSICA.md` — lo schema neutro delle undici caselle e
ciò che vale per ogni repertorio; le schede stanno in `docs/repertori/` e se ne
legge **una per volta**.

- [ ] **Step 3: Aggiungere `docs/repertori/` all'albero del progetto**

In §5, sotto `docs\`, due righe: la cartella e cosa contiene.

- [ ] **Step 4: Verificare**

```bash
grep -n "MUSICA.md\|repertori" HANDOFF.md
```

Atteso: nessuna riga che descriva `MUSICA.md` come catalogo di pattern per
genere o come sede delle correzioni ricevute.

- [ ] **Step 5: Commit**

```bash
git add HANDOFF.md
git commit -m "handoff: i rimandi allo schema neutro e alle schede"
```

---

## Come si vede che è finita

Dalla spec §8, tutti e cinque verificabili:

| criterio | come si controlla |
|---|---|
| le undici caselle hanno accolto tutto, senza residui | `ORFANE` del Task 7, ognuna giustificata |
| nessun numero in due file | `DOPPIE` del Task 7, nessuna con cifre o nomi di funzione |
| l'indice dice cosa manca a quale repertorio senza aprire niente | `test_indice_repertori_coerente_con_le_schede` verde |
| `MUSICA.md` più una scheda bastano a comporre | lettura a campione: la scheda reggae non rimanda a `MUSICA.md` per niente che serva a scrivere una battuta |
| il documento sembra più povero, ed è giusto così | 11 caselle × 2 schede = 22, di cui 15 non piene |
