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
import math
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

#: Il charleston suonato col PIEDE. Nel jazz sta sul 2 e sul 4, ed e' lo
#: strumento su cui cade la stratificazione misurata nella casella 6.
PEDALE = 'charleston a pedale'

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

    RITORNA il campione appaiato -- `[(esecuzione, {strumento: residuo})]` --
    perche' `il_template()` ne ha bisogno e ricostruirlo vorrebbe dire
    rileggere tutti i MIDI una seconda volta.
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
    print('    POSITIVO = dopo la griglia, NEGATIVO = prima. '
          'Origine e swing sono gia stati tolti.')
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
            for nome in ('ride', PEDALE):
                sel = [x for x in prof.passi.get(nome, [])
                       if x.passo in quali and x.colpi >= 10]
                if sum(x.colpi for x in prof.passi.get(nome, [])) < 40 or not sel:
                    continue
                d[nome] = statistics.median(
                    [x.scarto for x in sel for _ in range(x.colpi)])
            if len(d) == 2:
                v.append((d['ride'] - d[PEDALE], e.drummer))
        if v:
            print(f'    {eti:16s} n={len(v):3d} '
                  f'batt={len({dr for _, dr in v})}  ride - charleston '
                  f'{statistics.median(x for x, _ in v):+5.2f} tick  '
                  f'il ride e piu TARDI in '
                  f'{sum(1 for x, _ in v if x > 0)}/{len(v)}')

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

    # ⚠️ LA VERSIONE FORTE, E SULLA GRANDEZZA GIUSTA.
    #
    # Due correzioni rispetto a una versione precedente di questo blocco:
    #
    # 1. una REGRESSIONE invece di tre mediane per fascia. Le fasce sono un
    #    raggruppamento arbitrario e la loro piattezza puo' essere fortuna di
    #    composizione; la pendenza no.
    # 2. sul DIVARIO APPAIATO, non sui livelli. Dopo `origine()` il livello di
    #    ogni esecuzione ha uno ZERO ARBITRARIO -- l'origine tolta e' comune al
    #    kit e puo' variare da esecuzione a esecuzione -- quindi una pendenza
    #    sui livelli confonde. La DIFFERENZA fra due strumenti della stessa
    #    esecuzione quell'offset lo cancella per costruzione, ed e' l'unica
    #    grandezza definita. E' anche l'unica coerente con cio' che questo
    #    modulo puo' dire: un confronto fra pad, mai una latenza assoluta.
    #
    # Le due ipotesi fanno previsioni opposte sul divario:
    #   - divario costante in TICK (frazione del movimento: mestiere, oppure
    #     un gesto come la corsa del pedale)      -> pendenza 0
    #   - divario costante in MILLISECONDI (latenza fissa di un pad rispetto
    #     all'altro)  -> pendenza = ms_mediano * 96/60000, dello STESSO SEGNO
    #     del divario
    print('\n--- la stessa domanda sul DIVARIO APPAIATO (l unica grandezza definita) ---')
    for pad in ('rullante', 'kick', 'ride'):
        camp = [(e.bpm, d[pad] - d[PEDALE], e.drummer)
                for e, d in per_es if pad in d and PEDALE in d]
        if len(camp) < 4:
            continue
        n = len(camp)
        mx = statistics.mean(b for b, _, _ in camp)
        my = statistics.mean(y for _, y, _ in camp)
        sxx = sum((b - mx) ** 2 for b, _, _ in camp)
        if sxx == 0:
            continue
        m = sum((b - mx) * (y - my) for b, y, _ in camp) / sxx
        q = my - m * mx
        res = sum((y - (m * b + q)) ** 2 for b, y, _ in camp)
        se = ((res / (n - 2)) / sxx) ** 0.5
        ms = statistics.median(y * 60000 / b / 96 for b, y, _ in camp)
        atteso = ms * 96 / 60000
        print(f'    {pad} - {PEDALE}'.ljust(48)
              + f'n={n:2d} batt={len({dr for *_, dr in camp})}  '
                f'divario {statistics.median(y for _, y, _ in camp):+5.2f} tick '
                f'({ms:+5.1f} ms)')
        print(f'      pendenza {m:+.4f} +/- {se:.4f} tick/BPM   '
              f'da COSTANTE-IN-TICK (0,0000) {abs(m) / se:.1f} sigma   '
              f'da LATENZA FISSA ({atteso:+.4f}) {abs(m - atteso) / se:.1f} sigma')

    # ⚠️ IL CONTROLLO SENZA NIENTE TOLTO. Le fasi grezze dentro il movimento,
    # senza `origine()` e senza togliere lo swing: se il disegno c'e' deve
    # vedersi anche cosi'. Un colpo conta se sta entro un quarto di movimento
    # dal battere, e uno strumento conta se ne ha almeno venti.
    # ⚠️ OGNI RIGA PORTA I SUOI BATTERISTI. Il numero di esecuzioni da solo
    # non dice se cio' che si scrive e' [MIS] su un repertorio o [OSS] su un
    # esecutore: quattro esecuzioni di quattro batteristi e quattro dello
    # stesso non sono la stessa misura, e la scheda deve poterlo dire.
    print('\n--- controprova sulle FASI GREZZE (nessuna origine tolta) ---')
    grezze: dict[str, list[tuple[float, str]]] = {}
    coppia: list[tuple[float, str]] = []
    for e in GR.elenco(BASE, style=STILE, beat_type='beat',
                       time_signature='4-4'):
        if e.style in FUORI_DALLO_SWING:
            continue
        c = _colpi(e)
        riga = {}
        for nome in (PEDALE, 'ride', 'rullante', 'kick'):
            fasi = []
            for pos, _ in c.get(nome, []):
                f = pos % PPQ
                if f > PPQ / 2:
                    f -= PPQ
                if abs(f) < PPQ / 4:
                    fasi.append(f)
            if len(fasi) >= 20:
                riga[nome] = statistics.median(fasi)
        for k, val in riga.items():
            grezze.setdefault(k, []).append((val, e.drummer))
        if PEDALE in riga and 'ride' in riga:
            coppia.append((riga[PEDALE] - riga['ride'], e.drummer))
    for nome in (PEDALE, 'rullante', 'kick', 'ride'):
        v = grezze.get(nome, [])
        if v:
            print(f'    {nome:24s} n={len(v):3d} '
                  f'batt={len({d for _, d in v})}  '
                  f'fase mediana {statistics.median(x for x, _ in v):+6.2f} tick')
    if coppia:
        print(f'    {PEDALE} - ride: n={len(coppia)} '
              f'batt={len({d for _, d in coppia})}  '
              f'mediana {statistics.median(x for x, _ in coppia):+.2f} tick  '
              f'il charleston ANTICIPA in '
              f'{sum(1 for x, _ in coppia if x < 0)}/{len(coppia)}')

    # il campione appaiato ride/charleston, calcolato QUI una volta sola:
    # `il_template()` lo riusa invece di rileggere tutti i MIDI una seconda
    # volta per ricostruire gli stessi quindici numeri.
    return per_es


def il_difetto_della_grazia():
    """Di quanto il mezzo passo di grazia sbagliava, prima del 24 agosto 2026.

    ⚠️ QUESTA FUNZIONE PORTA IL CODICE VECCHIO CON SE', ED E' APPOSTA. Fino al
    24 agosto `profilo_da_colpi()` calcolava il movimento con

        movimento = math.floor(p / ppq + 0.125)

    cioe' con mezzo passo di grazia, e una nota nell'ultimo ottavo di
    movimento ne usciva con fase NEGATIVA: `_senza_swing()` le applicava
    allora il ramo della prima meta' (DILATATA) mentre la nota sta nella
    seconda (COMPRESSA). Il difetto e' stato corretto, quindi la libreria non
    sa piu' rifarlo -- ma la casella 6 dichiara di quanto sbagliava, e in
    questo progetto ogni numero della scheda deve uscire da una riga di
    questo file. Le due righe vecchie stanno percio' qui, dentro la misura
    che le seppellisce, e da nessun'altra parte.

    ⚠️ E FALSIFICA LA GIUSTIFICAZIONE che quel codice si dava. Il commento
    diceva che senza la grazia "il residuo uscirebbe grande quanto un
    movimento intero". Non puo': `passo = round(dritta / passo_tick)` sceglie
    il passo PIU' VICINO, quindi |residuo| <= mezzo passo per costruzione, con
    la grazia e senza. Si conta, invece di crederci.
    """
    print('\n=== il mezzo passo di grazia: di quanto sbagliava ===')
    passo_tick = PPQ / 4
    tot = 0
    err: list[float] = []
    per_str: dict[str, list[int]] = {}       # nome -> [colpi, con fase < 0]
    diverso = 0
    oltre_mezzo_passo = [0, 0]               # [piano, con la grazia]
    esecuzioni = 0
    # ⚠️ DOVE LA GRAZIA FACEVA ANCHE DA PARAFANGO, ed e' la ragione per cui
    # toglierla fa cadere un'unanimita'. Con la grazia i colpi dell'ultimo
    # ottavo di movimento finivano schiacciati dentro [-6/levare, 0] tick:
    # se `levare` sta sopra 0,5 quel bordo cade dentro mezzo passo, e un
    # colpo sul BATTERE non poteva MAI passare al passo precedente. Sotto
    # 0,5 -- crome dritte o quasi -- poteva. Si conta invece di crederci.
    riparate = 0
    scoperte: list[tuple[str, float, float]] = []
    for e in GR.elenco(BASE, style=STILE, beat_type='beat',
                       time_signature='4-4'):
        if e.style in FUORI_DALLO_SWING:
            continue
        esecuzioni += 1
        c = _colpi(e)
        tutte = [p for note in c.values() for p, _ in note]
        off = GR.origine(tutte, passo_tick)
        bur = GR.bur_da_posizioni([p - off for p in tutte], PPQ)
        levare = da_bur(bur) if bur is not None else 0.5
        if levare > 0.5:
            riparate += 1
        else:
            scoperte.append((e.id, levare, 6.0 / levare))
        for nome, note in c.items():
            riga = per_str.setdefault(nome, [0, 0])
            for pos, _ in note:
                p = pos - off
                tot += 1
                riga[0] += 1

                # --- il conto VECCHIO, con il mezzo passo di grazia ---
                mv = math.floor(p / PPQ + 0.125)
                fv = p / PPQ - mv
                dv = (mv + GR._senza_swing(fv, levare)) * PPQ
                pv = round(dv / passo_tick)

                # --- il conto di OGGI, la fase piana dentro il movimento ---
                mn, resto = divmod(p, PPQ)
                dn = (mn + GR._senza_swing(resto / PPQ, levare)) * PPQ
                pn = round(dn / passo_tick)

                if fv < 0:
                    riga[1] += 1
                    err.append(abs(dv - dn))
                if pv != pn:
                    diverso += 1
                for i, (d, q) in enumerate(((dn, pn), (dv, pv))):
                    if abs(d - q * passo_tick) > passo_tick / 2 + 1e-9:
                        oltre_mezzo_passo[i] += 1

    q = statistics.quantiles(err, n=4)
    print(f'    {esecuzioni} esecuzioni, {tot} colpi')
    print(f'    colpi che prendevano una fase NEGATIVA: {len(err)} '
          f'({100 * len(err) / tot:.1f}%)')
    print(f'    errore sulla loro posizione: mediana {statistics.median(err):.2f} '
          f'tick  (q1-q3 {q[0]:.2f}-{q[2]:.2f})  massimo {max(err):.2f} tick')
    print(f'    colpi che ne uscivano su un PASSO diverso: {diverso} '
          f'({100 * diverso / tot:.1f}%)')
    print('    dove cadeva, per strumento:')
    for nome, (n, neg) in sorted(per_str.items(), key=lambda kv: -kv[1][0])[:6]:
        print(f'      {nome:24s} {n:6d} colpi, con fase negativa {neg:5d} '
              f'({100 * neg / n:4.1f}%)')
    print(f'    residui oltre mezzo passo ({passo_tick / 2:.0f} tick), che il '
          f'commento diceva grandi quanto un movimento:')
    print(f'      con la fase piana {oltre_mezzo_passo[0]}, '
          f'con la grazia {oltre_mezzo_passo[1]}, su {tot}')
    print(f'    e dove la grazia faceva da parafango sui BATTERE '
          f'(levare > 0,5, cioe bordo -6/levare dentro mezzo passo):')
    print(f'      {riparate} esecuzioni su {esecuzioni}; le altre, scoperte:')
    for quale, lev, bordo in scoperte:
        print(f'        {quale:24s} levare {lev:.2f}  bordo {-bordo:+.2f} tick')


#: Le esecuzioni che la casella 6 NOMINA: quella raccomandata come template e
#: quella indicata per la coppia da ascoltare. I loro numeri per passo devono
#: uscire da qui e non da un conto a mano -- e' l'invariante che questo lavoro
#: si e' dato.
NOMINATE = ('drummer1/session3/2', 'drummer10/session1/1')

#: Un residuo oltre questo vale piu' di tre quarti di mezzo passo: quei colpi
#: stanno al confine con il passo accanto, e uno stimatore che li conta li'
#: puo' rovesciarsi. Non e' una soglia della musica, e' una del metodo.
BORDO = 9.0


def il_bordo_del_passo():
    """Quanti colpi stanno al confine fra due passi, dove il residuo si rovescia.

    ⚠️ PERCHE' ESISTE, e la data: 24 agosto 2026. `profilo_da_colpi()` sceglie
    il passo con `round()`, quindi |residuo| <= mezzo passo (12 tick) SEMPRE.
    Ne segue che un colpo che anticipa un passo di piu' di 12 tick dritti non
    esce come un anticipo grande: esce come un RITARDO grande sul passo
    precedente. Il segno si rovescia, e una mediana per strumento se ne va
    dietro.

    Fino al 24 agosto il mezzo passo di grazia di `profilo_da_colpi()` teneva
    i colpi dell'ultimo ottavo di movimento dentro [-9,7, 0] tick, quindi sui
    BATTERE il rovesciamento non poteva accadere -- e il charleston a pedale
    del jazz suona quasi solo li'. Tolta la grazia, i battere si comportano
    come tutti gli altri confini di passo, ed e' giusto che sia cosi': ma il
    rovesciamento diventa visibile e va misurato invece che subito.

    Stampa due cose: quante celle stanno al bordo, e -- per le esecuzioni che
    la scheda NOMINA -- i passi del battere con quello che li precede.
    """
    print('\n=== il bordo fra due passi: dove il residuo si rovescia ===')
    print(f'    una cella e "al bordo" se |scarto| >= {BORDO:.0f} tick '
          f'(mezzo passo = {PPQ/8:.0f}) e porta almeno 10 colpi')
    al_bordo: dict[str, int] = {}
    spezzate: dict[str, int] = {}
    quante: dict[str, int] = {}
    chi: dict[str, set] = {}
    for e in GR.elenco(BASE, style=STILE, beat_type='beat',
                       time_signature='4-4'):
        if e.style in FUORI_DALLO_SWING:
            continue
        p = GR.profilo(BASE, e.id)
        for nome, passi in p.passi.items():
            if sum(s.colpi for s in passi) < 40:
                continue
            quante[nome] = quante.get(nome, 0) + 1
            chi.setdefault(nome, set()).add(e.drummer)
            forti = {s.passo: s for s in passi if s.colpi >= 10}
            if any(abs(s.scarto) >= BORDO for s in forti.values()):
                al_bordo[nome] = al_bordo.get(nome, 0) + 1
            # ⚠️ LA FIRMA DI UN COLPO MUSICALE CONTATO IN DUE POSTI, e il
            # criterio e' il CONTEGGIO, non lo scarto: se la semicroma PRIMA
            # del battere porta piu' colpi del battere stesso, e i due scarti
            # hanno segni opposti, quei colpi non sono un secondo disegno --
            # sono lo stesso gesto, la cui dispersione ha passato il confine.
            # E' anche la condizione che fa RIBALTARE la mediana pesata sui
            # colpi, perche' la meta' piu' numerosa decide il segno.
            # ⚠️ Un criterio precedente guardava lo scarto (<=-6 contro
            # >=+6) e sbagliava bersaglio: prendeva esecuzioni che non si
            # ribaltano e mancava quelle che si ribaltano.
            if any(k in forti and k - 1 in forti
                   and forti[k - 1].colpi > forti[k].colpi
                   and forti[k].scarto * forti[k - 1].scarto < 0
                   for k in (0, 4, 8, 12)):
                spezzate[nome] = spezzate.get(nome, 0) + 1
    for nome in sorted(quante, key=lambda n: -quante[n]):
        if quante[nome] < 8:
            continue
        print(f'    {nome:24s} {quante[nome]:2d} esecuzioni, '
              f'{len(chi[nome])} batteristi   con una cella al bordo: '
              f'{al_bordo.get(nome, 0):2d}   col BATTERE IN MINORANZA: '
              f'{spezzate.get(nome, 0):2d}')

    print('\n--- i passi del battere, sulle esecuzioni che la scheda NOMINA ---')
    for quale in NOMINATE:
        p = GR.profilo(BASE, quale)
        print(f'  {quale}  ({p.bpm} BPM, BUR {p.bur:.2f}, '
              f'{p.battute} battute)')
        for nome in ('ride', PEDALE):
            passi = {s.passo: s for s in p.passi.get(nome, [])}
            tot = sum(s.colpi for s in passi.values())
            righe = '  '.join(
                f'{k:2d}:{passi[k].scarto:+5.1f}/{passi[k].colpi:3d}'
                for k in (3, 4, 11, 12) if k in passi)
            print(f'    {nome:22s} ({tot:3d} colpi)  {righe}')
        for a, b in ((4, 4), (12, 12)):
            r = {s.passo: s for s in p.passi.get('ride', [])}.get(a)
            c = {s.passo: s for s in p.passi.get(PEDALE, [])}.get(b)
            if r and c:
                print(f'      passo {a}: ride - charleston '
                      f'{r.scarto - c.scarto:+5.2f} tick')


def _dritte_della_voce(e, nome, colpi=None) -> list[float]:
    """Le posizioni DRITTE di una voce: origine tolta, swing tolto.

    Rifa' la prima passata di `GR.profilo_da_colpi()` per poter interrogare
    i tagli senza passare da un `Profilo` gia' aggregato. `colpi` si passa
    quando si interrogano piu' voci della stessa esecuzione, per non
    rileggere il file MIDI una volta per voce.
    """
    c = _colpi(e) if colpi is None else colpi
    tutte = [p for v in c.values() for p, _ in v]
    off = GR.origine(tutte, PPQ / 4)
    bur = GR.bur_da_posizioni([p - off for p in tutte], PPQ)
    lev = da_bur(bur) if bur is not None else 0.5
    fuori = []
    for pos, _ in c.get(nome, []):
        p = pos - off
        mov, resto = divmod(p, PPQ)
        fuori.append((mov + GR._senza_swing(resto / PPQ, lev)) * PPQ)
    return fuori


def il_vuoto_delle_voci():
    """Quanto e' netto il vuoto su cui `'rado'` mette il taglio.

    ⚠️ PERCHE' ESISTE, e cosa NON fa. `'rado'` non ha parametri: il centro
    del vuoto piu' largo e' una grandezza geometrica, non una taratura.
    Resta pero' una domanda che solo il corpus chiude: se il buco piu'
    largo fosse largo quanto gli altri, il suo centro sarebbe arbitrario e
    lo spostamento riassegnerebbe i passi in blocco.

    Questa sezione misura il rapporto `largo / medio` -- quanto il buco piu'
    largo supera quello che ci sarebbe se i colpi fossero sparsi piatti.
    NON decide niente: se quel rapporto stesse vicino a 1 su molte voci,
    servirebbe un ripiego, e sarebbe una decisione da prendere, non da
    inventare qui.
    """
    print('\n=== il vuoto su cui "rado" taglia: e un vuoto vero? ===')
    rapporti, spostamenti = [], []
    esecuzioni, batteristi = 0, set()
    for e in GR.elenco(BASE, style=STILE, beat_type='beat',
                       time_signature='4-4'):
        if e.style in FUORI_DALLO_SWING:
            continue
        c = _colpi(e)
        esecuzioni += 1
        batteristi.add(e.drummer)
        for nome in sorted(c):
            dritte = _dritte_della_voce(e, nome, colpi=c)
            if len(dritte) < 40:
                continue
            centro, largo, medio = GR._vuoto_piu_largo(dritte, PPQ / 4)
            if medio <= 0:
                continue
            rapporti.append(largo / medio)
            spostamenti.append(abs(centro - PPQ / 8))
    r = sorted(rapporti)
    q = statistics.quantiles(r, n=4)
    print(f'    {esecuzioni} esecuzioni, {len(batteristi)} batteristi, '
          f'{len(r)} voci con almeno 40 colpi')
    print(f'    largo/medio : min {r[0]:.1f}  q1 {q[0]:.1f}  '
          f'mediana {statistics.median(r):.1f}  q3 {q[2]:.1f}  '
          f'max {r[-1]:.1f}')
    for soglia in (1.5, 2.0, 3.0, 5.0):
        n = sum(1 for x in r if x < soglia)
        print(f'    voci col vuoto meno di {soglia:.1f} volte il medio: '
              f'{n:3d} su {len(r)}  ({100 * n / len(r):.1f}%)')
    s = sorted(spostamenti)
    print(f'    |spostamento| : mediana {statistics.median(s):.2f} tick, '
          f'q3 {s[int(len(s) * 0.75)]:.2f}, massimo {max(s):.2f}')


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


def il_template(per_es):
    """L'esecuzione da cui esce il groove template, e cosa c'e' dentro.

    `per_es` arriva da `il_profilo_aggregato()`: e' lo stesso campione
    appaiato, gia' calcolato.
    """
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
    # ⚠️ SENZA SOGLIA. `applica_groove()` non ne ha nessuna (`musica.py`: cerca
    # `per_passo.get(passo)` e applica quel che trova), quindi l'escursione
    # vera e' su TUTTI i passi, non solo su quelli che la stampa qui sopra
    # tiene. Una versione precedente riportava il 6,64 filtrato come se fosse
    # il massimo spostamento: era meta' del vero.
    ms = 60000 / p.bpm / 96
    tutti = [(s2.scarto, nome, s2.passo, s2.colpi)
             for nome, passi in p.passi.items() for s2 in passi]
    if tutti:
        lo = min(tutti)[0]
        hi = max(tutti)[0]
        estremo = max(tutti, key=lambda x: abs(x[0]))
        print(f'  scarti che applica_groove() scrivera (TUTTI i passi): '
              f'da {lo:+.2f} a {hi:+.2f} tick, escursione {hi - lo:.2f} tick '
              f'= {(hi - lo) * ms:.1f} ms a {p.bpm} BPM')
        print(f'  massimo SPOSTAMENTO singolo: {estremo[0]:+.2f} tick '
              f'= {abs(estremo[0]) * ms:.1f} ms  ({estremo[1]}, passo '
              f'{estremo[2]}, {estremo[3]} colpi)')
        print('  i cinque piu grandi in modulo, coi colpi che li sostengono:')
        for sc, nome, passo, colpi in sorted(tutti, key=lambda x: -abs(x[0]))[:5]:
            print(f'    {sc:+6.2f} tick  {nome:22s} passo {passo:2d}  {colpi} colpi')
        filtrati = [x[0] for x in tutti if x[3] >= p.battute * 0.05]
        print(f'  (con la soglia della stampa qui sopra sarebbe stato '
              f'{min(filtrati):+.2f}..{max(filtrati):+.2f}, '
              f'escursione {max(filtrati) - min(filtrati):.2f} tick: meta del vero)')

    # ⚠️ IL TEMPLATE DENTRO IL CAMPIONE. La casella 6 dice "12 su 15" sulla
    # stratificazione ride/charleston: va detto dove cade in quella fila
    # proprio l'esecuzione che si raccomanda come template.
    #
    # ⚠️ FINO AL 24 agosto 2026 quel conteggio era "15 su 15", e questo
    # commento lo citava cosi'. E' caduto col mezzo passo di grazia (commit
    # `18f26e5`): la sezione qui sotto stampa il numero vero, che oggi e' 12
    # su 15 col divario mediano cresciuto da 2,59 a 3,21 tick. L'unanimita'
    # che regge e' quella sulle FASI GREZZE, che non passa da nessuna catena
    # -- la stampa `il_profilo_aggregato()`, «controprova sulle FASI GREZZE»,
    # ed e' quella che la casella 6 cita adesso.
    print('\n--- dove cade il template nel campione appaiato ride/charleston ---')
    camp = sorted((d['ride'] - d[PEDALE], e2.id, e2.drummer)
                  for e2, d in per_es if 'ride' in d and PEDALE in d)
    for v, quale, _ in camp:
        print(f'    {v:+6.2f} tick  {quale}'
              + ('   <-- IL TEMPLATE' if quale == scelta.id else ''))
    senza = [(v, dr) for v, quale, dr in camp if quale != scelta.id]
    if senza:
        print(f'    tutte: n={len(camp)} '
              f'batt={len({dr for *_, dr in camp})} mediana '
              f'{statistics.median(v for v, *_ in camp):+.2f} '
              f'ride piu tardi in {sum(1 for v, *_ in camp if v > 0)}/{len(camp)}')
        print(f'    senza il template: n={len(senza)} '
              f'batt={len({dr for _, dr in senza})} mediana '
              f'{statistics.median(v for v, _ in senza):+.2f} '
              f'ride piu tardi in {sum(1 for v, _ in senza if v > 0)}/{len(senza)}')

    # e PERCHE' quel file sta al bordo: due stimatori danno segni opposti.
    # ⚠️ `.get()`, non `[...]`: il criterio del template e' "la piu' lunga
    # fra le jazz/swing", e niente garantisce che quella esecuzione porti
    # entrambi i pad. Con l'accesso diretto un template senza ride faceva
    # KeyError qui, dopo minuti di misure gia' stampate.
    print('    i due stimatori su quel file:')
    for nome in ('ride', PEDALE):
        passi = p.passi.get(nome, [])
        forti = [x for x in passi if x.colpi >= 10]
        if not forti:
            print(f'      {nome:22s} assente da questo template '
                  f'({sum(x.colpi for x in passi)} colpi)')
            continue
        sui_colpi = statistics.median(
            [x.scarto for x in forti for _ in range(x.colpi)])
        sui_passi = statistics.median([x.scarto for x in passi])
        print(f'      {nome:22s} sui COLPI (passi con >=10 colpi) '
              f'{sui_colpi:+6.2f}   sui PASSI (tutti, non pesata) {sui_passi:+6.2f}')

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


#: Di quanto si trasla una voce sola, in tick, nella prova di linearita'.
#: Fino a 8 su un passo da 24: oltre un terzo di passo la domanda cambia --
#: non e' piu' "lo stimatore segue?" ma "quale passo e' quello giusto?".
DELTA = (-8, -6, -4, -2, 0, 2, 4, 6, 8)


def la_prova_di_traslazione():
    """Uno stimatore e' uno stimatore se la sua risposta SEGUE i dati.

    ⚠️ E' LA MISURA CHE DECIDE il default di `GR.TAGLI`, ed e' scelta il 26
    agosto 2026 CONTRO due criteri piu' ovvi. L'errore di ricostruzione per
    inversione premia lo stimatore rotto -- spezzare un gesto in due celle
    rende ciascuna delle due mediane piu' stretta, quindi l'errore SCENDE. E
    la tenuta delle conclusioni della casella 6 come bersaglio sarebbe
    fabbricare la conclusione, che e' il difetto della finestra di grazia.

    ⚠️ ORIGINE E LEVARE SI CONGELANO ai valori di delta = 0: traslando una
    voce sola si muove anche l'origine del kit, e chi non lo neutralizza
    misura quell'artefatto e conclude che nessuno stimatore e' lineare.

    ⚠️ LE CELLE SI APPAIANO PER POSIZIONE DICHIARATA, non per numero di
    passo. E' il punto: uno stimatore che ripiega SPOSTA un gesto da una
    cella all'altra, quindi `k` cambia mentre il gesto e' lo stesso.
    Appaiare per `k` confronterebbe due popolazioni diverse sotto la stessa
    etichetta.
    """
    print('\n=== la prova di traslazione per voce: lo stimatore segue? ===')
    print(f'    delta provati: {DELTA} tick su un passo da {PPQ/4:.0f}')
    esiti = {t: {'pendenze': [], 'salti': [], 'voci': 0} for t in GR.TAGLI}
    esecuzioni, batteristi = 0, set()
    for e in GR.elenco(BASE, style=STILE, beat_type='beat',
                       time_signature='4-4'):
        if e.style in FUORI_DALLO_SWING:
            continue
        c = _colpi(e)
        tutte = [p for v in c.values() for p, _ in v]
        off0 = GR.origine(tutte, PPQ / 4)
        bur0 = GR.bur_da_posizioni([p - off0 for p in tutte], PPQ)
        lev0 = da_bur(bur0) if bur0 is not None else 0.5
        esecuzioni += 1
        batteristi.add(e.drummer)
        for nome in sorted(c):
            if len(c[nome]) < 40:
                continue
            for taglio in GR.TAGLI:
                dichiarate = {}
                for d in DELTA:
                    mosso = dict(c)
                    mosso[nome] = [(p + d, v) for p, v in c[nome]]
                    p = GR.profilo_da_colpi(
                        mosso, PPQ, taglio=taglio,
                        origine_fissa=off0, levare_fisso=lev0)
                    dichiarate[d] = sorted(
                        s.passo * PPQ / 4 + s.scarto
                        for s in p.passi.get(nome, []) if s.colpi >= 10)
                base = dichiarate[0]
                if not base:
                    continue
                esiti[taglio]['voci'] += 1
                # appaiamento per posizione dichiarata piu' vicina a delta=0
                mosse = []
                for d in DELTA:
                    if d == 0:
                        continue
                    scarti = [min(dichiarate[d], key=lambda x: abs(x - b)) - b
                              for b in base] if dichiarate[d] else []
                    if scarti:
                        mosse.append((d, statistics.median(scarti)))
                if len(mosse) < 2:
                    continue
                # pendenza per minimi quadrati passanti per l'origine
                num = sum(d * m for d, m in mosse)
                den = sum(d * d for d, _ in mosse)
                pend = num / den if den else 0.0
                esiti[taglio]['pendenze'].append(pend)
                esiti[taglio]['salti'].append(max(abs(m - d) for d, m in mosse))
    print(f'    {esecuzioni} esecuzioni, {len(batteristi)} batteristi')
    print(f'    {"taglio":10s} {"voci":>5s} {"pendenza mediana":>18s} '
          f'{"scarto max mediano":>20s} {"voci con un salto >= 12 tick":>30s}')
    for taglio in GR.TAGLI:
        v = esiti[taglio]
        if not v['pendenze']:
            continue
        print(f'    {taglio:10s} {v["voci"]:5d} '
              f'{statistics.median(v["pendenze"]):18.3f} '
              f'{statistics.median(v["salti"]):20.2f} '
              f'{sum(1 for s in v["salti"] if s >= PPQ / 8):30d}')


def main() -> None:
    la_delimitazione()
    la_scala()
    lo_swing()
    per_es = il_profilo_aggregato()
    il_difetto_della_grazia()
    il_bordo_del_passo()
    il_vuoto_delle_voci()
    la_prova_di_traslazione()
    i_fill()
    il_template(per_es)


if __name__ == '__main__':
    main()
