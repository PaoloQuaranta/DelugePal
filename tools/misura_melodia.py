"""Come e' fatta una linea di assolo jazz: la misura della casella 8.

    .venv/Scripts/python.exe tools/misura_melodia.py > out/melodia_jazz.txt

Risponde a due domande che la casella 8 di `docs/repertori/jazz.md` pone, e
che il 29 agosto 2026 sono diventate urgenti: il primo pezzo jazz generato
aveva un assolo CORRETTO E PIATTO -- media e mediana centrate sul corpus,
dispersione dimezzata -- e l'utente l'ha sentito («il solo potrebbe essere un
po' piu' pirotecnico»).

    1. DOVE stanno le corse dentro il giro di 12 battute, e dove i silenzi;
    2. QUANTO lunga dev'essere una cella perche' la sua ripetizione sia
       sviluppo motivico e non la scala.

⚠️ LA DOMANDA 1 NON E' «QUANTE NOTE PER BATTUTA». Quella era gia' misurata
(5,2 in mediana) ed e' esattamente cio' che ha prodotto una linea piatta: una
statistica aggregata dice dov'e' il centro, non dove sta l'interesse. Qui si
misura la DISTRIBUZIONE lungo la forma.

⚠️ LA DOMANDA 2 VUOLE UN RIFERIMENTO CASUALE, e senza non significa niente.
In una scala di sette note le celle corte ricorrono da se': senza confronto
con la stessa linea MESCOLATA si misurerebbe il vocabolario e lo si
chiamerebbe motivo. Il mescolamento conserva la distribuzione degli
intervalli e distrugge il solo ordine, che e' precisamente cio' che si vuole
isolare.

IL CAMPIONE. Solo i blues `A12` a feel `SWING`: la posizione dentro la forma
e' definita solo se la forma e' nota, e A12 e' anche la forma del pezzo che
si genera. Ogni assolo passa un controllo di PERIODICITA' -- la sigla alla
battuta b deve tornare alla b+12 nell'80% dei casi -- e chi non lo passa e'
scartato e contato, non aggiustato.

⚠️ UNA CORSA E' RELATIVA AL SOLISTA CHE LA SUONA. La soglia e' il terzo
quartile DI QUELL'ASSOLO, con un minimo assoluto di 8 note: senza la parte
relativa si misurerebbe chi suona fitto invece di dove accelera; senza il
minimo assoluto, in un assolo rado qualunque battuta media diventerebbe una
corsa.
"""
from __future__ import annotations

import collections
import random
import statistics as st
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import wjazz as WJ                           # noqa: E402

RADICE = Path(__file__).resolve().parent.parent
DB = RADICE / 'to-read' / 'MIDI' / 'wjazzd.db'

TICK_BATTUTA = 384
GIRO = 12
#: minimo assoluto perche' una battuta conti come corsa, oltre al terzo
#: quartile dell'assolo. 8 note in una battuta di 4/4 vuol dire crome piene.
CORSA_MINIMO = 8
#: sotto le 3 note una battuta e' «rada», la categoria che serve a chiedersi
#: cosa PRECEDE una corsa.
RADA_MASSIMO = 2
#: Piu' semi, non uno. ⚠️ Il rapporto reale/mescolato e' STABILE dove il
#: riferimento casuale e' grosso e INSTABILE dove tende a zero: su celle da 6
#: e 7 note il valore balla del 45% fra un seme e l'altro, perche' lo si sta
#: dividendo per quasi niente. Riportare un solo seme darebbe un numero
#: preciso e finto. Lo strumento stampa il minimo e il massimo, e chi legge
#: cita il minimo.
SEMI = (1, 7, 99, 2026, 12345)


def assoli(con) -> list[sqlite3.Row]:
    return list(con.execute(
        "select s.melid, s.performer, s.style from solo_info s "
        "join composition_info c on c.compid = s.compid "
        "where c.form = 'A12' and s.rhythmfeel = 'SWING'"))


def _ancora(acc):
    """(tick, battuta) da cui contare, e il controllo di periodicita'.

    Ritorna `None` se la griglia non e' un giro di 12 che si ripete: meglio
    scartare un assolo che allineare le sue battute a caso.
    """
    prime = [a for a in acc if a.bar >= 1 and a.sigla]
    if len(prime) < GIRO:
        return None, 'poche caselle'
    per_bar = {}
    for a in acc:
        if a.sigla and a.beat == 1:
            per_bar.setdefault(a.bar, a.sigla.testo)
    coppie = [(per_bar[b], per_bar[b + GIRO])
              for b in per_bar if b + GIRO in per_bar]
    if len(coppie) < 8:
        return None, 'giri insufficienti'
    uguali = sum(1 for x, y in coppie if x == y) / len(coppie)
    if uguali < 0.8:
        return None, f'griglia non periodica ({uguali:.0%})'
    return (prime[0].tick, prime[0].bar), None


def per_battuta(db, melid, ancora):
    """(posizione nel giro 1-12, note in quella battuta), battuta per battuta."""
    righe, _ = WJ.melodia(db, melid)
    pos = [n.pos for ns in righe.values() for n in ns]
    if len(pos) < 40:
        return None
    t0, b0 = ancora
    conta = collections.Counter((p - t0) // TICK_BATTUTA for p in pos)
    span = range(min(conta), max(conta) + 1)
    return [((b0 - 1 + b) % GIRO + 1, conta.get(b, 0)) for b in span]


def l_arco_del_giro(db, con) -> None:
    """DOVE stanno le corse e i silenzi dentro le dodici battute."""
    corse = collections.Counter(); vuote = collections.Counter()
    tot = collections.Counter(); note = collections.defaultdict(list)
    lunghezze = []; dopo = {True: [0, 0], False: [0, 0]}
    per_solista = collections.defaultdict(lambda: collections.defaultdict(list))
    usati, solisti, scartati = 0, set(), collections.Counter()

    for r in assoli(con):
        ancora, perche = _ancora(WJ.armonia(db, r['melid']))
        if ancora is None:
            scartati[perche] += 1
            continue
        battute = per_battuta(db, r['melid'], ancora)
        if battute is None:
            scartati['troppo corta'] += 1
            continue
        v = [c for _, c in battute]
        soglia = max(st.quantiles(v, n=4)[2], CORSA_MINIMO) if len(v) >= 4 \
            else CORSA_MINIMO

        corsa_prec = None
        run = 0
        for i, (p, c) in enumerate(battute):
            e_corsa = c >= soglia
            tot[p] += 1; note[p].append(c)
            if e_corsa: corse[p] += 1
            if c == 0: vuote[p] += 1
            per_solista[r['performer']][p].append(e_corsa)
            if i:
                dopo[corsa_prec][e_corsa] += 1
            corsa_prec = battute[i][1] <= RADA_MASSIMO
            run = run + 1 if e_corsa else (lunghezze.append(run) or 0) if run else 0
        if run: lunghezze.append(run)
        usati += 1; solisti.add(r['performer'])

    print(f'=== L\'arco del giro: {usati} assoli, {len(solisti)} solisti, '
          f'{sum(tot.values())} battute [MIS] ===\n')
    if scartati:
        print('scartati:', dict(scartati), '\n')
    print('  pos   corse   vuote   note (mediana)      n')
    for p in range(1, GIRO + 1):
        if not tot[p]:
            continue
        print(f'   {p:2}   {100 * corse[p] / tot[p]:5.1f}%  '
              f'{100 * vuote[p] / tot[p]:5.1f}%   {st.median(note[p]):5.1f}'
              f'{tot[p]:14}')

    pro = contro = 0
    for d in per_solista.values():
        alto = [x for p in (9, 10) for x in d.get(p, [])]
        basso = [x for p in (1, 12) for x in d.get(p, [])]
        if len(alto) < 6 or len(basso) < 6:
            continue
        if sum(alto) / len(alto) > sum(basso) / len(basso): pro += 1
        else: contro += 1
    print(f'\nsolisti con piu\' corse sul ii-V (9-10) che su 1 e 12: '
          f'{pro} su {pro + contro}')

    c = collections.Counter(lunghezze); n = sum(c.values())
    print(f'\nlunghezza di una corsa: mediana {st.median(lunghezze):.0f} battute, '
          f'media {st.mean(lunghezze):.2f}, massimo {max(lunghezze)}')
    print('  ', '  '.join(f'{k} battut{"a" if k == 1 else "e"}: '
                          f'{100 * c[k] / n:.0f}%'
                          for k in sorted(c) if c[k] / n >= 0.02))

    for rada, eti in ((True, 'rada (<=2 note)'), (False, 'piena')):
        d = dopo[rada]
        print(f'\ndopo una battuta {eti:16} una corsa arriva nel '
              f'{100 * d[True] / sum(d):5.1f}%  (n={sum(d)})')


def la_cella_e_la_scala(db, con) -> None:
    """QUANTO lunga dev'essere una cella perche' ripeterla sia un motivo."""
    def ripetute(cs):
        c = collections.Counter(cs)
        return sum(v for v in c.values() if v > 1) / len(cs)

    def celle(seq, L):
        return [tuple(seq[i:i + L]) for i in range(len(seq) - L + 1)]

    lunghezze = (2, 3, 4, 5, 6)
    linee = []
    for r in assoli(con):
        righe, _ = WJ.melodia(db, r['melid'])
        alt = [a for _, a in sorted((x.pos, a)
                                    for a, xs in righe.items() for x in xs)]
        if len(alt) >= 80:
            linee.append([alt[i + 1] - alt[i] for i in range(len(alt) - 1)])

    reale = {L: st.mean(ripetute(celle(iv, L)) for iv in linee)
             for L in lunghezze}
    finto = {L: [] for L in lunghezze}
    vince = {L: [] for L in lunghezze}
    for seme in SEMI:
        random.seed(seme)
        mescolate = []
        for iv in linee:
            m = iv[:]
            random.shuffle(m)
            mescolate.append(m)
        for L in lunghezze:
            b = [ripetute(celle(m, L)) for m in mescolate]
            finto[L].append(st.mean(b))
            vince[L].append(sum(1 for iv, x in zip(linee, b)
                                if ripetute(celle(iv, L)) > x))

    print(f'\n\n=== La cella e la scala: {len(linee)} assoli [MIS] ===\n')
    print('celle di N intervalli che ricompaiono nello stesso assolo, contro')
    print(f'la STESSA linea MESCOLATA. {len(SEMI)} semi: {", ".join(map(str, SEMI))}\n')
    print('  intervalli  note   reale   mescolato      rapporto      assoli')
    for L in lunghezze:
        r = sorted(reale[L] / f for f in finto[L])
        stab = 'stabile' if r[-1] - r[0] < 1 else 'BALLA'
        print(f'  {L:10}  {L + 1:4}  {100 * reale[L]:5.1f}%  '
              f'{100 * st.mean(finto[L]):8.2f}%  '
              f'{r[0]:6.2f}x - {r[-1]:6.2f}x  {stab:>8}'
              f'{min(vince[L]):5}/{len(linee)}')
    # ⚠️ output in ASCII puro, come `misura_groove.py`: questi file finiscono
    # in `out/` per redirezione, e la console di Windows e' cp1252.
    print('\nATTENZIONE: dove il rapporto BALLA il riferimento casuale tende a')
    print('   zero e lo si sta dividendo per quasi niente. Si cita il MINIMO,')
    print('   non la media, e a 7 note non si cita affatto un rapporto.')


def main() -> int:
    if not DB.exists():
        print(f'manca {DB}')
        return 1
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    l_arco_del_giro(str(DB), con)
    la_cella_e_la_scala(str(DB), con)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
