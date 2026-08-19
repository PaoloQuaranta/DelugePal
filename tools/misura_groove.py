"""Le misure che riempiono le caselle 4, 6 e 9 del jazz. Uscita in `out/`.

Uno strumento di misura, non libreria: si esegue una volta, si legge il
risultato e i numeri si scrivono a mano nella scheda, con il loro marcatore.

    .venv/Scripts/python.exe tools/misura_groove.py > out/groove_jazz.txt

⚠️ `out/` non e' versionato, e il dataset nemmeno: questo file e' lo stato del
disco del giorno in cui e' stato eseguito. Se un numero della scheda non
torna, si riesegue qui prima di correggere la scheda.

OGNI SEZIONE STAMPA QUANTE ESECUZIONI E QUANTI BATTERISTI la sostengono. Non
e' rendicontazione: e' il numero che decide se cio' che si scrive e' [MIS] su
un repertorio o [OSS] su un esecutore.
"""
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from delugexml import groove as GR                          # noqa: E402
from delugexml import midi as MI                            # noqa: E402
from delugexml.musica import da_bur                         # noqa: E402

BASE = Path('to-read/MIDI/groove-v1.0.0-midionly/groove')
STILE = 'jazz'

#: Dentro l'etichetta `jazz` ma FUORI dallo swing di crome. La delimitazione
#: sta qui, dichiarata, e non nascosta dentro un filtro.
FUORI_DALLO_SWING = {'jazz/funk', 'jazz/fusion'}

#: I tre pad che il ride occupa nella mappa GM.
RIDE = {'ride', 'ride 2', 'campana del ride'}

PPQ = float(MI.TICK_PER_MOVIMENTO_DELUGE)


def _colpi(e):
    """strumento -> [(posizione in tick Deluge, velocity)], per una esecuzione."""
    f = MI.leggi(BASE / e.midi_filename)
    fattore = MI.TICK_PER_MOVIMENTO_DELUGE / f.ppq
    fuori: dict[str, list[tuple[float, int]]] = {}
    for t in f.tracce:
        for n in t.note:
            nome = MI.GM_PERCUSSIONI.get(n.y)
            if nome is None:
                continue                # percussione fuori dalla mappa GM
            fuori.setdefault(nome, []).append((n.pos * fattore, n.velocity))
    return fuori


def _riassunto(nome, valori, batteristi):
    if not valori:
        print(f'{nome:34s} vuoto')
        return
    v = sorted(valori)
    m = statistics.median(v)
    q = statistics.quantiles(v, n=4) if len(v) >= 4 else [v[0], m, v[-1]]
    print(f'{nome:34s} n={len(v):3d} batteristi={batteristi}  '
          f'BUR {m:.2f} (q1-q3 {q[0]:.2f}-{q[2]:.2f})  '
          f'levare {da_bur(m) * 100:.1f}%')


def la_delimitazione():
    """Cosa c'e' dentro l'etichetta `jazz`, e chi l'ha suonato."""
    print('=== la delimitazione: cosa sta dentro l etichetta `jazz` ===')
    tutte = GR.elenco(BASE, style=STILE)
    print(f'esecuzioni col prefisso `jazz`: {len(tutte)}  '
          f'su {sum(GR.valori(BASE, "style").values())} righe di info.csv')
    print(f'batteristi: {sorted({e.drummer for e in tutte})}')
    for colonna in ('style', 'beat_type', 'time_signature'):
        conto: dict[str, int] = {}
        for e in tutte:
            conto[getattr(e, colonna)] = conto.get(getattr(e, colonna), 0) + 1
        print(f'  per {colonna}: '
              + ', '.join(f'{k}={v}' for k, v in
                          sorted(conto.items(), key=lambda kv: -kv[1])))
    for bt in ('beat', 'fill'):
        sel = GR.elenco(BASE, style=STILE, beat_type=bt)
        conto = {}
        for e in sel:
            conto[e.drummer] = conto.get(e.drummer, 0) + 1
        print(f'  {bt}: {len(sel)} esecuzioni, {len(conto)} batteristi -- '
              + ', '.join(f'{k}={v}' for k, v in
                          sorted(conto.items(), key=lambda kv: -kv[1])))
        conto = {}
        for e in sel:
            conto[e.style] = conto.get(e.style, 0) + 1
        print('      per etichetta: '
              + ', '.join(f'{k}={v}' for k, v in
                          sorted(conto.items(), key=lambda kv: -kv[1])))


def la_scala():
    """La scala di velocity, con e senza le etichette fuori dallo swing."""
    print(f'\n=== scala di velocity, {STILE}, beat ===')
    for v in GR.scala(BASE, style=STILE).values():
        print(f'{v.strumento:24s} mediana {v.mediana:3d}  '
              f'q1-q3 {v.q1:3d}-{v.q3:3d}  min-max {v.minimo:3d}-{v.massimo:3d}'
              f'  colpi {v.colpi:6d}  esecuzioni {v.esecuzioni:3d}'
              f'  batteristi {v.batteristi}')

    # ⚠️ il controllo che dice se la delimitazione conta per la DINAMICA:
    # se le mediane non si muovono, il filtro serve allo swing e non a questa
    # tabella, e lo si puo' scrivere invece di lasciarlo supporre.
    print('\n--- la stessa scala, TOLTI funk e fusion (controllo) ---')
    racc: dict[str, list[int]] = {}
    quali: dict[str, set] = {}
    chi: dict[str, set] = {}
    for e in GR.elenco(BASE, style=STILE, beat_type='beat'):
        if e.style in FUORI_DALLO_SWING:
            continue
        for nome, note in _colpi(e).items():
            racc.setdefault(nome, []).extend(v for _, v in note)
            quali.setdefault(nome, set()).add(e.id)
            chi.setdefault(nome, set()).add(e.drummer)
    for nome, vs in sorted(racc.items(), key=lambda kv: -len(kv[1]))[:8]:
        vs.sort()
        q = statistics.quantiles(vs, n=4)
        print(f'{nome:24s} mediana {int(statistics.median(vs)):3d}  '
              f'q1-q3 {int(q[0]):3d}-{int(q[2]):3d}  '
              f'min-max {vs[0]:3d}-{vs[-1]:3d}  colpi {len(vs):6d}  '
              f'esecuzioni {len(quali[nome]):3d}  batteristi {len(chi[nome])}')


def lo_swing():
    """Il BUR: per esecuzione, per sottoinsieme, e sul kit contro sul ride."""
    print(f'\n=== BUR per esecuzione, {STILE}, beat 4/4 ===')
    righe = []
    for e in GR.elenco(BASE, style=STILE, beat_type='beat',
                       time_signature='4-4'):
        c = _colpi(e)
        tutte = [p for note in c.values() for p, _ in note]
        off = GR.origine(tutte, PPQ / 4)
        b_kit = GR.bur_da_posizioni([p - off for p in tutte], PPQ)
        pos_ride = [p - off for n in RIDE for p, _ in c.get(n, [])]
        # sotto i venti colpi il ride non e' una voce dell'esecuzione
        b_ride = (GR.bur_da_posizioni(pos_ride, PPQ)
                  if len(pos_ride) >= 20 else None)
        # su quante COPPIE di crome poggia il BUR del kit: e' la grandezza su
        # cui `WJ.swing()` mette una soglia (`minimo_coppie=20`) e questa
        # misura no, quindi va almeno riferita -- vedi il controllo in fondo.
        coppie = len(GR.levare_da_posizioni([p - off for p in tutte], PPQ))
        # e quelle del solo ride, che sono un'ALTRA grandezza: la soglia va
        # messa sulle coppie della voce che si sta misurando, non su quelle
        # del kit -- se no si filtra un numero con il conteggio di un altro.
        coppie_ride = len(GR.levare_da_posizioni(pos_ride, PPQ)) if pos_ride else 0
        righe.append((e, b_kit, b_ride, len(pos_ride), coppie, coppie_ride))
        print(f'{e.id:24s} {e.style:16s} {e.bpm:4d} BPM  '
              f'kit {"--  " if b_kit is None else f"{b_kit:.2f}"}  '
              f'ride {"--  " if b_ride is None else f"{b_ride:.2f}"}'
              f'  (coppie {coppie:4d}, colpi di ride {len(pos_ride):5d})')

    def sotto(sel, i):
        return ([r[i] for r in sel if r[i] is not None],
                len({r[0].drummer for r in sel if r[i] is not None}))

    print('\n--- il BUR per sottoinsieme, misurato sul KIT INTERO ---')
    gruppi = [
        ('tutto `jazz` beat 4/4', righe),
        ('senza funk e fusion',
         [r for r in righe if r[0].style not in FUORI_DALLO_SWING]),
        ('solo etichetta jazz/swing',
         [r for r in righe if r[0].style == 'jazz/swing']),
        ('solo jazz/funk', [r for r in righe if r[0].style == 'jazz/funk']),
        ('solo jazz/fusion', [r for r in righe if r[0].style == 'jazz/fusion']),
    ]
    for nome, sel in gruppi:
        _riassunto(nome, *sotto(sel, 1))

    print('\n--- lo stesso, per batterista (il controllo che conta) ---')
    for d in sorted({r[0].drummer for r in righe}):
        _riassunto(f'  {d}', *sotto([r for r in righe if r[0].drummer == d], 1))

    print('\n--- e per fascia di tempo, senza funk e fusion ---')
    dentro = [r for r in righe if r[0].style not in FUORI_DALLO_SWING]
    for lo, hi, nome in [(0, 120, '<= 120'), (120, 180, '120-180'),
                         (180, 240, '180-240'), (240, 999, '> 240')]:
        _riassunto(f'  {nome} BPM',
                   *sotto([r for r in dentro if lo < r[0].bpm <= hi], 1))

    # ⚠️ IL CONFRONTO APPAIATO. Sulle STESSE esecuzioni, se no il ride
    # sembrerebbe swingare di piu' solo perche' e' assente proprio nelle
    # esecuzioni meno swingate: sarebbe selezione, non strumento.
    print('\n--- kit contro ride, sulle STESSE esecuzioni (appaiato) ---')
    coppie = [r for r in dentro if r[1] is not None and r[2] is not None]
    if coppie:
        k = [r[1] for r in coppie]
        rd = [r[2] for r in coppie]
        _riassunto('  kit  ', k, len({r[0].drummer for r in coppie}))
        _riassunto('  ride ', rd, len({r[0].drummer for r in coppie}))
        avanti = sum(1 for r in coppie if r[2] > r[1])
        print(f'  il ride swinga PIU del kit in {avanti} esecuzioni '
              f'su {len(coppie)}')

    # ⚠️ IL CONTROLLO DI ROBUSTEZZA. `WJ.swing()` scarta gli assoli con meno
    # di 20 coppie di crome -- "una mediana su quattro valori non e' una
    # mediana" -- e qui quella soglia non c'e'. Se la mediana dipendesse dalle
    # esecuzioni magre, il confronto con Weimar non starebbe in piedi. Si
    # rialza la soglia e si guarda se il numero si muove.
    print('\n--- e se si applica la soglia di WJ.swing() (20 coppie) ---')
    magre = sum(1 for r in dentro if r[1] is not None and r[4] < 20)
    print(f'    esecuzioni delimitate con meno di 20 coppie: {magre} '
          f'su {sum(1 for r in dentro if r[1] is not None)}')
    for soglia in (0, 5, 10, 20):
        sel = [r for r in dentro if r[1] is not None and r[4] >= soglia]
        _riassunto(f'  kit,  coppie >= {soglia:2d}',
                   [r[1] for r in sel], len({r[0].drummer for r in sel}))
    # ⚠️ la stessa soglia sul RIDE, contata sulle coppie DEL RIDE. Il campione
    # si dimezza (il ride non c'e' in tutte le esecuzioni) e va detto: e' la
    # differenza fra "1,99 su 21 esecuzioni" e "2,00 su 10".
    for soglia in (0, 20):
        sel = [r for r in dentro if r[2] is not None and r[5] >= soglia]
        _riassunto(f'  ride, coppie di ride >= {soglia:2d}',
                   [r[2] for r in sel], len({r[0].drummer for r in sel}))


def il_profilo_aggregato():
    """Quali passi, su tutte le esecuzioni invece che su una sola.

    Ogni esecuzione pesa uno: se no il file da 193 battute deciderebbe da solo
    che cosa fa un batterista jazz.
    """
    print('\n=== profilo posizionale AGGREGATO (senza funk e fusion) ===')
    quota: dict[str, dict[int, list[float]]] = {}
    vel: dict[str, dict[int, list[int]]] = {}
    chi: dict[str, set] = {}
    quante: dict[str, int] = {}
    residuo: dict[str, list[tuple[float, str]]] = {}
    for e in GR.elenco(BASE, style=STILE, beat_type='beat',
                       time_signature='4-4'):
        if e.style in FUORI_DALLO_SWING:
            continue
        p = GR.profilo(BASE, e.id)
        for nome, passi in p.passi.items():
            tot = sum(s.colpi for s in passi)
            if tot < 40:
                continue        # esecuzione che di quello strumento tace
            quante[nome] = quante.get(nome, 0) + 1
            chi.setdefault(nome, set()).add(e.drummer)
            for s in passi:
                quota.setdefault(nome, {}).setdefault(
                    s.passo, []).append(s.colpi / tot)
                vel.setdefault(nome, {}).setdefault(
                    s.passo, []).append(s.velocity)
            forti = [s for s in passi if s.colpi >= 10]
            if forti:
                residuo.setdefault(nome, []).append((statistics.median(
                    [s.scarto for s in forti for _ in range(s.colpi)]),
                    e.drummer))

    for nome in sorted(quante, key=lambda n: -quante[n]):
        if quante[nome] < 8:
            continue
        print(f'{nome}  ({quante[nome]} esecuzioni, {len(chi[nome])} batteristi)')
        for eti, larghe in (('quota', True), ('vel  ', False)):
            for meta in (range(8), range(8, 16)):
                celle = []
                for passo in range(16):
                    if passo not in meta:
                        continue
                    qs = quota[nome].get(passo, [])
                    if larghe:
                        # un passo mai colpito in un'esecuzione vale ZERO,
                        # non "assente": se no le quote non sommano a uno
                        q = sum(qs) / quante[nome] if qs else 0.0
                        celle.append(f'{passo:2d}:{100 * q:4.1f}%')
                    else:
                        v = statistics.median(vel[nome][passo]) if qs else 0
                        celle.append(f'{passo:2d}:v{v:3.0f}')
                print(f'   {eti if meta.start == 0 else "     "} '
                      + ' '.join(celle))
        print()

    print('--- il RESIDUO per strumento, in tick Deluge (96 per movimento) ---')
    print('    + spinge, - trattiene. Origine e swing sono gia stati tolti.')
    for nome, vs in sorted(residuo.items(), key=lambda kv: -len(kv[1])):
        if len(vs) < 8:
            continue
        v = sorted(x for x, _ in vs)
        q = statistics.quantiles(v, n=4)
        print(f'{nome:24s} n={len(v):3d} batt={len({d for _, d in vs})}  '
              f'mediana {statistics.median(v):+6.2f}  '
              f'q1-q3 {q[0]:+6.2f}..{q[2]:+6.2f}  min-max {v[0]:+6.2f}..{v[-1]:+6.2f}')
    print('    un tick vale: '
          + ', '.join(f'{b} BPM = {60000 / b / 96:.2f} ms'
                      for b in (100, 120, 185, 215)))

    # ⚠️ IL CONFRONTO CHE DECIDE se esiste un pocket A STRATI. Le mediane qui
    # sopra vengono da esecuzioni diverse, e un'esecuzione intera puo' stare
    # avanti o indietro per conto suo: confrontarle fra loro direbbe poco.
    # Dentro la STESSA esecuzione, invece, l'ordine fra due strumenti e' una
    # domanda musicale -- chi spinge e chi trattiene? -- e la risposta e' un
    # conteggio, non una differenza di mediane.
    #
    # ⚠️ SI APPAIANO TUTTE LE COPPIE, non una scelta a mano. Una versione
    # precedente confrontava il solo ride col solo rullante e concludeva
    # "nessun ordine": ma quelle due sono le mediane PIU' VICINE del gruppo,
    # cioe' il confronto che aveva meno probabilita' di mostrare qualcosa.
    # Scegliere la coppia dopo aver visto le mediane e' scegliere il
    # risultato. Qui le coppie le decide il dataset, e si stampano tutte.
    print('\n--- OGNI coppia di strumenti, DENTRO la stessa esecuzione ---')
    per_es = []
    for e in GR.elenco(BASE, style=STILE, beat_type='beat',
                       time_signature='4-4'):
        if e.style in FUORI_DALLO_SWING:
            continue
        prof = GR.profilo(BASE, e.id)
        d = {}
        for nome, passi in prof.passi.items():
            forti = [s for s in passi if s.colpi >= 10]
            if sum(s.colpi for s in passi) < 40 or not forti:
                continue
            d[nome] = statistics.median(
                [s.scarto for s in forti for _ in range(s.colpi)])
        per_es.append((e, d))

    nomi = sorted({n for _, d in per_es for n in d},
                  key=lambda n: -sum(1 for _, d in per_es if n in d))
    tabella = []
    for i, primo in enumerate(nomi):
        for secondo in nomi[i + 1:]:
            v = [(d[primo] - d[secondo], e.drummer)
                 for e, d in per_es if primo in d and secondo in d]
            if len(v) < 8:
                continue        # sotto le otto esecuzioni non si conta niente
            diff = sorted(x for x, _ in v)
            tabella.append((abs(statistics.median(diff)), primo, secondo,
                            len(diff), statistics.median(diff),
                            sum(1 for x in diff if x > 0),
                            len({dr for _, dr in v}), diff[0], diff[-1]))
    # ⚠️ IL SEGNO, DETTO UNA VOLTA PER TUTTE. `Passo.scarto` e' il residuo
    # rispetto al passo: POSITIVO = il colpo cade DOPO la griglia (tardi),
    # NEGATIVO = prima (anticipa). Lo conferma `applica_groove()`, che fa
    # `pos + scarto`. Quindi `primo - secondo > 0` vuol dire che il PRIMO
    # arriva PIU' TARDI del secondo, non che gli sta davanti. Una versione
    # precedente di questa riga la chiamava "AVANTI" e faceva concludere il
    # rovescio della realta' sul charleston a pedale.
    for _, primo, secondo, n, med, tardi, batt, lo, hi in sorted(
            tabella, reverse=True):
        print(f'    {primo} - {secondo}'.ljust(50)
              + f'n={n:3d} batt={batt}  mediana {med:+5.2f} tick  '
                f'il primo e piu TARDI in {tardi:2d}/{n:<3d} '
                f'(min {lo:+.2f}, max {hi:+.2f})')

    # ⚠️ IL CONTROLLO CHE TOGLIE IL CONFONDIMENTO POSIZIONALE. Il residuo
    # dipende dal passo, e i due strumenti non suonano sugli stessi passi:
    # il charleston a pedale concentra i colpi sul 4 e sul 12 molto piu' del
    # ride. La differenza fra i due potrebbe quindi essere "chi suona dove" e
    # non "chi trattiene". Si rimisura sui SOLI passi 4 e 12, dove suonano
    # entrambi, e si guarda se regge.
    print('\n--- ride contro charleston, sui SOLI passi 4 e 12 ---')
    for quali, eti in (((4, 12), 'passi 4 e 12'), (tuple(range(16)), 'tutti i passi')):
        v = []
        for e, _ in per_es:
            prof = GR.profilo(BASE, e.id)
            d = {}
            for nome in ('ride', 'charleston a pedale'):
                sel = [x for x in prof.passi.get(nome, [])
                       if x.passo in quali and x.colpi >= 10]
                if sum(x.colpi for x in prof.passi.get(nome, [])) < 40 or not sel:
                    continue
                d[nome] = statistics.median(
                    [x.scarto for x in sel for _ in range(x.colpi)])
            if len(d) == 2:
                v.append(d['ride'] - d['charleston a pedale'])
        if v:
            print(f'    {eti:16s} n={len(v):3d}  ride - charleston '
                  f'{statistics.median(v):+5.2f} tick  '
                  f'il ride e piu TARDI in {sum(1 for x in v if x > 0)}/{len(v)}')

    # ⚠️ MESTIERE O LATENZA? E LA FISICA, SCRITTA GIUSTA.
    #
    # Un tick dura 60000/(BPM*96) ms, quindi SI ACCORCIA al salire del tempo.
    # Ne segue che una latenza FISSA di D millisecondi vale
    #
    #     D * BPM * 96 / 60000  tick
    #
    # cioe' e' proporzionale al BPM e in tick CRESCE al salire del tempo
    # (20 ms = 3,04 tick a 95 BPM, 6,88 tick a 215). Una scelta musicale e'
    # invece una frazione del movimento: costante in TICK, e in ms cala.
    #
    # ⚠️ Una versione precedente di questo blocco aveva la legge ROVESCIATA.
    # La conclusione reggeva lo stesso -- piatto-in-tick e' incompatibile sia
    # con "cresce" sia con "cala" -- ma la regola enunciata era falsa.
    #
    # ⚠️ E LA COLONNA IN MS NON E' UN SECONDO RISCONTRO: e' tick * 60000 /
    # (BPM*96), aritmetica sugli stessi numeri. Si stampa per leggibilita',
    # non come prova indipendente.
    print('\n--- latenza fissa in ms, o frazione del movimento? ---')
    print('    una latenza fissa CRESCE in tick col BPM; una scelta musicale sta ferma')
    for nome in ('charleston a pedale', 'rullante', 'kick', 'ride'):
        v = [(e.bpm, d[nome], d[nome] * 60000 / e.bpm / 96, e.drummer)
             for e, d in per_es if nome in d]
        if len(v) < 8:
            continue
        print(f'    {nome} (n={len(v)}, batt={len({dr for *_, dr in v})})')
        for lo2, hi2 in ((0, 110), (110, 130), (130, 999)):
            sel = [(t, m, dr) for b, t, m, dr in v if lo2 < b <= hi2]
            if len(sel) < 3:
                continue
            tick = [t for t, _, _ in sel]
            sd = statistics.stdev(tick) if len(tick) > 1 else 0.0
            print(f'      {lo2:3d}-{hi2:3d} BPM  n={len(sel):2d} '
                  f'batt={len({dr for *_, dr in sel})}  '
                  f'tick mediana {statistics.median(tick):+6.2f} '
                  f'media {statistics.mean(tick):+6.2f} '
                  f'dev.st {sd:4.2f} err.st {sd / len(tick) ** 0.5:4.2f}  '
                  f'(ms {statistics.median(m for _, m, _ in sel):+7.2f})')

        # ⚠️ LA VERSIONE FORTE: una regressione, non tre mediane. Le fasce
        # sono un raggruppamento arbitrario e la loro piattezza potrebbe
        # essere fortuna di composizione. La pendenza no.
        def pendenza(campione):
            n = len(campione)
            mx = statistics.mean(b for b, _ in campione)
            my = statistics.mean(t for _, t in campione)
            sxx = sum((b - mx) ** 2 for b, _ in campione)
            if n < 4 or sxx == 0:
                return None
            m = sum((b - mx) * (t - my) for b, t in campione) / sxx
            q = my - m * mx
            res = sum((t - (m * b + q)) ** 2 for b, t in campione)
            se = ((res / (n - 2)) / sxx) ** 0.5
            # cosa prevede una latenza FISSA pari alla mediana osservata in ms
            ms_med = statistics.median(t * 60000 / b / 96 for b, t in campione)
            atteso = ms_med * 96 / 60000
            return m, se, atteso, n

        for eti, camp in (('tutte', [(b, t) for b, t, _, _ in v]),
                          ('solo drummer1',
                           [(b, t) for b, t, _, dr in v if dr == 'drummer1'])):
            r = pendenza(camp)
            if r is None:
                continue
            m, se, atteso, n = r
            bpm = [b for b, _ in camp]
            sigma = abs(m - atteso) / se if se else float('inf')
            print(f'      pendenza [{eti}] n={n:2d} ({min(bpm)}-{max(bpm)} BPM): '
                  f'{m:+.4f} +/- {se:.4f} tick/BPM   '
                  f'latenza fissa prevede {atteso:+.4f}   '
                  f'distanza {sigma:.1f} sigma')


def i_fill():
    """I fill contro i beat: densita', durata, e quali strumenti."""
    print('\n=== i fill, contro i beat ===')
    for bt in ('fill', 'beat'):
        righe = []
        strum: dict[str, int] = {}
        for e in GR.elenco(BASE, style=STILE, beat_type=bt,
                           time_signature='4-4'):
            c = _colpi(e)
            n = sum(len(v) for v in c.values())
            if not n:
                continue
            battute = e.duration * e.bpm / 60.0 / 4.0
            righe.append((e, n, battute, n / battute))
            for nome, v in c.items():
                strum[nome] = strum.get(nome, 0) + len(v)
        dens = sorted(r[3] for r in righe)
        batt = sorted(r[2] for r in righe)
        tot = sum(strum.values())
        q = statistics.quantiles(dens, n=4)
        print(f'--- {bt}: {len(righe)} esecuzioni, '
              f'{len({r[0].drummer for r in righe})} batteristi ---')
        print(f'    battute       : min {batt[0]:.2f}  '
              f'mediana {statistics.median(batt):.2f}  max {batt[-1]:.2f}')
        print(f'    COLPI/BATTUTA : mediana {statistics.median(dens):.1f}  '
              f'(q1-q3 {q[0]:.1f}-{q[2]:.1f}, min {dens[0]:.1f}, max {dens[-1]:.1f})')
        print('    quota dei colpi per strumento: '
              + ', '.join(f'{n}={100 * q2 / tot:.1f}%' for n, q2 in
                          sorted(strum.items(), key=lambda kv: -kv[1])[:6]))

    print('\n--- la scala di velocity dei fill ---')
    for v in GR.scala(BASE, style=STILE, beat_type='fill').values():
        if v.colpi < 20:
            continue
        print(f'{v.strumento:24s} mediana {v.mediana:3d}  '
              f'q1-q3 {v.q1:3d}-{v.q3:3d}  colpi {v.colpi:5d}  '
              f'esecuzioni {v.esecuzioni:3d}  batteristi {v.batteristi}')


def il_template():
    """L'esecuzione da cui esce il groove template, e cosa c'e' dentro."""
    print('\n=== profilo del template ===')
    scelte = GR.elenco(BASE, style='jazz/swing', beat_type='beat',
                       time_signature='4-4')
    for e in sorted(scelte, key=lambda e: -e.duration)[:3]:
        print(f'  candidata: {e.id:22s} {e.bpm:4d} BPM  {e.duration:6.1f} s')
    scelta = max(scelte, key=lambda e: e.duration)
    print(GR.racconta(BASE, scelta.id))
    p = GR.profilo(BASE, scelta.id)
    print(f'BUR {p.bur:.2f}, battute {p.battute}')
    for nome, passi in sorted(p.passi.items(),
                              key=lambda kv: -sum(s.colpi for s in kv[1])):
        tot = sum(s.colpi for s in passi)
        if tot < 20:
            continue                    # troppo raro per dire qualcosa
        righe = '  '.join(
            f'{s.passo:2d}:v{s.velocity:3d}/{s.scarto:+.1f}/{s.colpi}'
            for s in passi if s.colpi >= p.battute * 0.05)
        print(f'{nome:22s} ({tot:4d} colpi su {p.battute} battute)  {righe}')

    # ⚠️ L'ESCURSIONE VERA che `applica_groove()` scrivera'. Le mediane
    # aggregate della sezione precedente stanno entro ~3,4 tick, ma sono
    # mediane su decine di esecuzioni: il profilo di UNA esecuzione porta uno
    # scarto per ogni passo, e l'escursione e' un'altra grandezza. Confonderle
    # farebbe sembrare il template molto piu' timido di quello che e'.
    tutti = [s2.scarto for passi in p.passi.values() for s2 in passi
             if s2.colpi >= p.battute * 0.05]
    if tutti:
        ms = 60000 / p.bpm / 96
        print(f'  scarti che il template scrivera: da {min(tutti):+.2f} a '
              f'{max(tutti):+.2f} tick, escursione {max(tutti) - min(tutti):.2f} '
              f'tick = {(max(tutti) - min(tutti)) * ms:.1f} ms a {p.bpm} BPM')

    # ⚠️ i due pad non suonano mai insieme: la stessa voce musicale --
    # il disegno di crome swingate -- cambia nome GM a meta' esecuzione.
    print('\n--- dove stanno, nel tempo, `ride` (n51) e `tom basso` (n43) ---')
    f = MI.leggi(BASE / scelta.midi_filename)
    note = sorted((n.pos, n.y) for t in f.tracce for n in t.note)
    fine = note[-1][0]
    for k in range(10):
        a, b = fine * k / 10, fine * (k + 1) / 10
        dentro = [y for pos, y in note if a <= pos < b]
        print(f'    decimo {k}: n43 `tom basso` = {dentro.count(43):4d}   '
              f'n51 `ride` = {dentro.count(51):4d}')

    # ⚠️ "mai insieme" va misurato, non dedotto dai decimi. La domanda giusta
    # non e' la simultaneita' esatta (che sarebbe un doppio colpo sullo stesso
    # istante, cosa che non fa nessuno) ma la SOVRAPPOSIZIONE: quante battute
    # portano entrambe le note, cioe' quanto dura il cambio di pad.
    bar = 4 * f.ppq
    b43, b51 = {}, {}
    for pos, y in note:
        if y == 43:
            b43[pos // bar] = b43.get(pos // bar, 0) + 1
        elif y == 51:
            b51[pos // bar] = b51.get(pos // bar, 0) + 1
    ent = set(b43) & set(b51)
    p43 = sorted(pos for pos, y in note if y == 43)
    p51 = [pos for pos, y in note if y == 51]
    croma = f.ppq // 2
    vicini = sum(1 for x in p51 if any(abs(x - c) <= croma for c in p43))
    print(f'    battute con ENTRAMBE: {len(ent)}  '
          f'(di cui {sum(1 for b in ent if b43[b] >= 2 and b51[b] >= 2)} '
          f'con almeno 2 colpi ciascuna)')
    print(f'    battute con la sola n43: {len(set(b43) - set(b51))}   '
          f'con la sola n51: {len(set(b51) - set(b43))}')
    print(f'    colpi n51 con una n43 entro una croma: {vicini} su {len(p51)}')
    print(f'    colpi esattamente simultanei: {len(set(p43) & set(p51))}')


def main() -> None:
    la_delimitazione()
    la_scala()
    lo_swing()
    il_profilo_aggregato()
    i_fill()
    il_template()


if __name__ == '__main__':
    main()
