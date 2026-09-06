"""Come il trio si spartisce la battuta: la misura della casella 5.

    .venv/Scripts/python.exe tools/misura_spartizione.py > out/spartizione_jazz.txt

Risponde al difetto sentito il 30 agosto 2026, che l'utente ha detto cosi':
«le interruzioni, accenti e struttura delle parti di batteria sono
strettamente correlati alla sezione ritmica, e non le puoi applicare
acriticamente». Misurato allora sui tre pezzi generati -- deviazione standard
dei colpi per battuta: batteria 1,48-1,65, comping 0,54-0,61, basso 0,00.

⚠️ IL BASSO NON VARIA MAI: 4,00 note per battuta, zero battute diverse da
quattro su 228. Qui si misura di quanto varia un bassista vero.

TUTTE LE SOGLIE STANNO QUI, non in `jtd.py`: il lettore non decide niente di
musicale. Ognuna porta accanto la frase che la giustifica.

⚠️ E DUE VINCOLI VENGONO DAI CONTROLLI di `tools/controlla_jtd.py`, girati
prima di questa misura:

  - il 10,1% dei beat in cui il basso «tace» ha in realta' un onset grezzo
    entro 50 ms: e' un allineamento mancato, non un silenzio. La misura 2 lo
    dichiara accanto al numero invece di tacerlo;
  - i pianisti sono 34 e Bill Evans da solo fa il 17,9% dei brani. Ogni
    numero sul piano esce col conteggio degli esecutori.
"""
from __future__ import annotations

import collections
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import jtd as JT                             # noqa: E402

ZIP = (Path(__file__).resolve().parent.parent / 'to-read' / 'MIDI'
       / 'jazz-trio-database-v02.zip')

#: Sotto questo numero di battute complete un brano non entra nelle medie: un
#: estratto corto da' distribuzioni che dipendono da dove e' stato tagliato
#: piu' che da chi suona.
MINIMO_BATTUTE = 32

#: Quanta parte dei «silenzi» del basso e' in realta' un allineamento mancato.
#: Misurato dal controllo 2 su tutti i 1204 brani in 4/4: 8183 su 80 977.
#: Sta qui perche' la misura 2 lo deve STAMPARE accanto al proprio numero.
QUOTA_ALLINEAMENTI_MANCATI = 10.1


def _brani(z, curati: bool):
    return JT.elenco(z, metro=4, curati=curati)


def densita_del_basso(z, brani) -> dict:
    """MISURA 1. Quanti onset di basso per battuta, e quanto si scostano.

    Il confronto e' col generatore: 4,00 esatte, deviazione 0,00.
    """
    per_battuta = collections.Counter()
    medie, deviazioni, esecutori, usati = [], [], set(), 0
    for b in brani:
        d = JT.battute(z, b.fname)
        if len(d.battute) < MINIMO_BATTUTE:
            continue
        usati += 1
        esecutori.add(b.bassista)
        conti = [x.densita['bass'] for x in d.battute]
        per_battuta.update(conti)
        medie.append(st.mean(conti))
        deviazioni.append(st.pstdev(conti))
    tot = sum(per_battuta.values())
    print('MISURA 1 -- la densita del basso per battuta')
    print(f'   {tot} battute, {usati} esecuzioni, {len(esecutori)} bassisti')
    print('   note per battuta   battute       %')
    for n in sorted(per_battuta):
        print(f'   {n:16}   {per_battuta[n]:7}   {100 * per_battuta[n] / tot:5.1f}')
    diverse = 100 * (tot - per_battuta[4]) / tot
    print(f'   battute DIVERSE da quattro: {diverse:.1f}%')
    print(f'   media per esecuzione:  mediana {st.median(medie):.2f}')
    print(f'   deviazione DENTRO l esecuzione:  mediana {st.median(deviazioni):.2f}')
    print('   -> il generatore fa 4,00 con deviazione 0,00 su 228 battute')
    return {'per_battuta': dict(per_battuta), 'battute': tot,
            'esecuzioni': usati, 'esecutori': len(esecutori),
            'diverse_da_quattro': diverse,
            'media_mediana': st.median(medie),
            'deviazione_mediana': st.median(deviazioni)}


def il_beat_saltato(z, brani) -> dict:
    """MISURA 2. Quanto spesso il basso NON suona sul beat, e su quale.

    ⚠️ Il numero grezzo e' un LIMITE SUPERIORE: il controllo 2 ha trovato che
    il 10,1% di questi silenzi ha un onset entro 50 ms, cioe' e' il
    rilevatore che ha mancato l'allineamento. Si stampa la correzione accanto.
    """
    per_posizione = collections.Counter()
    beat_per_posizione = collections.Counter()
    esecutori, usati = set(), 0
    for b in brani:
        g = JT.griglia(z, b.fname)
        if len(g) < MINIMO_BATTUTE * 4:
            continue
        usati += 1
        esecutori.add(b.bassista)
        for beat in g:
            beat_per_posizione[beat.posizione] += 1
            if beat.tace('bass'):
                per_posizione[beat.posizione] += 1
    tot_muti = sum(per_posizione.values())
    tot = sum(beat_per_posizione.values())
    grezzo = 100 * tot_muti / tot
    corretto = grezzo * (1 - QUOTA_ALLINEAMENTI_MANCATI / 100)
    print('\nMISURA 2 -- il beat su cui il basso tace')
    print(f'   {tot} beat, {usati} esecuzioni, {len(esecutori)} bassisti')
    print(f'   il basso tace su {tot_muti} beat: {grezzo:.1f}% grezzo, '
          f'{corretto:.1f}% tolto il {QUOTA_ALLINEAMENTI_MANCATI}% di')
    print('   allineamenti mancati misurato dal controllo 2')
    print('   posizione     beat   taciuti       %')
    for p in sorted(beat_per_posizione):
        q = per_posizione[p]
        print(f'   {p:9}   {beat_per_posizione[p]:6}   {q:7}   '
              f'{100 * q / beat_per_posizione[p]:5.1f}')
    return {'per_posizione': dict(per_posizione),
            'beat_per_posizione': dict(beat_per_posizione),
            'grezzo': grezzo, 'corretto': corretto,
            'esecuzioni': usati, 'esecutori': len(esecutori)}


#: Due onset entro questa distanza si dicono «insieme». E' una SCELTA
#: dichiarata, non una legge, ed e' il motivo per cui la misura 3 la ripete a
#: 20 e 50 ms: se il risultato dipendesse dalla finestra, non sarebbe un
#: risultato.
FINESTRA_COINCIDENZA = 0.030


def onset_fuori_griglia(x, strumento: str = 'bass') -> list[float]:
    """Gli onset di `strumento` dentro la battuta che non stanno su un beat.

    ⚠️ I confini da escludere sono i beat della battuta PIU' la sua fine, che
    e' il movimento della battuta dopo. Senza quest'ultimo, gli attacchi
    ANTICIPATI del battere successivo passano per note fuori griglia, ed e' un
    errore che si vede: misurato il 6 settembre 2026 su 12 brani, il quarto
    movimento portava 1112 onset contro i ~670 degli altri tre -- il 66% in
    piu' -- col 17,4% di loro ammassato a fase 0,97, cioe' un centesimo di
    movimento prima del battere.

    ⚠️ La misura 3 ha usato la versione senza il confine di fine dal 1
    settembre 2026: l'effetto sui suoi numeri e' dichiarato accanto a loro.

    Una definizione sola per le misure 3 e 6: due misure che dicono «fuori
    griglia» intendendo cose diverse non si possono confrontare.
    """
    confini = [bt.istante for bt in x.beat] + [x.fine]
    return [o for o in x.onsets[strumento]
            if all(abs(o - t) > FINESTRA_COINCIDENZA for t in confini)]


def _correlazione(a, b) -> float:
    """Pearson, scritto a mano.

    `statistics.correlation` c'e' solo dal 3.10, e la suite gira col Python di
    sistema di chi usa il progetto, che non e' garantito.
    """
    ma, mb = st.mean(a), st.mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den if den else 0.0


def accoppiamento(z, brani, finestre=(0.020, 0.030, 0.050)) -> dict:
    """MISURA 3. La batteria risponde al basso, o va per conto suo?

    Due cose diverse, e vanno tenute separate:
      a) le densita' per battuta si muovono insieme? (correlazione)
      b) quando il basso esce dalla griglia, ci esce anche la batteria?

    La (b) e' la domanda dell'utente alla lettera: se gli accenti fuori tempo
    dei due cadessero insieme piu' spesso del caso, «applicare la batteria
    acriticamente» sarebbe misurabilmente sbagliato.
    """
    coppie, esecutori, usati = [], set(), 0
    dentro = collections.Counter()
    fuori_basso = 0
    durata_totale = 0.0
    colpi_batteria = 0
    for b in brani:
        d = JT.battute(z, b.fname)
        if len(d.battute) < MINIMO_BATTUTE:
            continue
        usati += 1
        esecutori.add((b.bassista, b.batterista))
        bassi = [x.densita['bass'] for x in d.battute]
        batterie = [x.densita['drums'] for x in d.battute]
        if st.pstdev(bassi) > 0 and st.pstdev(batterie) > 0:
            coppie.append(_correlazione(bassi, batterie))
        for x in d.battute:
            durata_totale += x.fine - x.inizio
            colpi_batteria += len(x.onsets['drums'])
            fb = onset_fuori_griglia(x)
            fuori_basso += len(fb)
            for o in fb:
                for f in finestre:
                    if any(abs(o - d2) <= f for d2 in x.onsets['drums']):
                        dentro[f] += 1
    print('\nMISURA 3 -- l accoppiamento fra batteria e basso')
    print(f'   {usati} esecuzioni, {len(esecutori)} coppie basso-batteria')
    if coppie:
        print(f'   correlazione fra le densita per battuta: '
              f'mediana {st.median(coppie):+.3f}')
    else:
        print('   correlazione: n/d')
    print(f'   onset di basso FUORI dai beat: {fuori_basso}')
    # Il riferimento: quanto spesso due eventi cadrebbero vicini per caso, con
    # la stessa densita' di colpi di batteria distribuiti a caso nel tempo.
    densita_batteria = colpi_batteria / durata_totale if durata_totale else 0
    for f in finestre:
        q = dentro[f]
        atteso = 100 * min(1.0, densita_batteria * 2 * f)
        if fuori_basso:
            print(f'   di questi, con un colpo di batteria entro {f * 1000:3.0f} ms: '
                  f'{q:6} ({100 * q / fuori_basso:5.1f}%), atteso per caso '
                  f'{atteso:5.1f}%')
    return {'correlazione': st.median(coppie) if coppie else None,
            'fuori_griglia': fuori_basso, 'coincidenze': dict(dentro),
            'colpi_al_secondo': densita_batteria,
            'esecuzioni': usati, 'coppie': len(esecutori)}


def chi_sta_avanti(z, brani) -> dict:
    """MISURA 4. Lo scarto di ciascuno rispetto al beat di consenso.

    Il segno dice chi tira e chi trattiene. E' una relazione d'ensemble: non
    dice cosa si suona, dice come si sta insieme.

    ⚠️ Il beat di consenso e' calcolato DAI tre strumenti, quindi gli scarti
    sono per costruzione centrati intorno a zero: quello che conta e' la
    DIFFERENZA fra i tre, non il valore assoluto di ciascuno.
    """
    per_strumento = {s: [] for s in JT.STRUMENTI}
    usati = 0
    for b in brani:
        g = JT.griglia(z, b.fname)
        if len(g) < MINIMO_BATTUTE * 4:
            continue
        usati += 1
        for s in JT.STRUMENTI:
            v = [bt.scarti[s] for bt in g if bt.scarti[s] is not None]
            if v:
                per_strumento[s].append(st.mean(v))
    print('\nMISURA 4 -- chi sta avanti rispetto al beat comune')
    print(f'   {usati} esecuzioni')
    print('   strumento   mediana fra le esecuzioni (ms)   dispersione (ms)')
    for s in JT.STRUMENTI:
        v = per_strumento[s]
        if v:
            print(f'   {s:9}   {1000 * st.median(v):+29.1f}   '
                  f'{1000 * st.pstdev(v):14.1f}')
    return {s: (1000 * st.median(v) if v else None)
            for s, v in per_strumento.items()}


#: Quante note devono attaccare entro `FINESTRA_ACCORDO` perche' si dica
#: «accordo», cioe' comping e non linea.
NOTE_PER_ACCORDO = 2

#: ⚠️ REGOLA [IPO], NON MISURATA. In un trio il pianista fa comping E assolo,
#: e `piano_midi.mid` e' un flusso solo. 50 ms e' la finestra centrale; la
#: misura si ripete a 30 e 80 e la FORBICE si stampa: se il risultato balla,
#: nella scheda va la forbice al posto del numero.
FINESTRA_ACCORDO = 0.050


def il_piano(z, brani, finestre=(0.030, 0.050, 0.080)) -> dict:
    """MISURA 5. Il piano contro la sezione ritmica.

    Tre numeri: la densita' del piano per battuta ([MIS]), la quota di quella
    densita' che cade in accordi invece che in note singole ([IPO], perche'
    dipende dalla regola qui sopra), e come la densita' del piano si muove
    rispetto a quella del basso e della batteria nella STESSA battuta -- che
    e' la relazione, ed e' il motivo per cui la misura esiste.
    """
    densita, quote = [], {f: [] for f in finestre}
    con_basso, con_batteria = [], []
    esecutori, usati = set(), 0
    for b in brani:
        d = JT.battute(z, b.fname)
        if len(d.battute) < MINIMO_BATTUTE:
            continue
        usati += 1
        esecutori.add(b.pianista)
        p = [x.densita['piano'] for x in d.battute]
        ba = [x.densita['bass'] for x in d.battute]
        dr = [x.densita['drums'] for x in d.battute]
        densita.append(st.mean(p))
        if st.pstdev(p) > 0 and st.pstdev(ba) > 0:
            con_basso.append(_correlazione(p, ba))
        if st.pstdev(p) > 0 and st.pstdev(dr) > 0:
            con_batteria.append(_correlazione(p, dr))
        # ⚠️ La simultaneita' si misura sul MIDI, NON su `piano_onsets.csv`.
        # Il rilevatore di onset conta UN attacco per accordo: sul primo brano
        # da' 1070 eventi dove il MIDI ha 3138 note, e chiedergli quante note
        # attaccano insieme da' zero accordi a 30 ms, che e' impossibile per un
        # pianista che accompagna. Costava un numero falso e plausibile.
        f_midi = JT.piano(z, b.fname)
        if not f_midi.note or not f_midi.bpm:
            continue
        pos = sorted(n.pos for n in f_midi.note)
        for f in finestre:
            # la finestra in secondi diventa tick: il MIDI porta il tempo vero
            # nelle posizioni, con ppq e bpm suoi.
            larghezza = f * f_midi.ppq * f_midi.bpm / 60.0
            in_accordo = i = 0
            while i < len(pos):
                j = i
                while j + 1 < len(pos) and pos[j + 1] - pos[i] <= larghezza:
                    j += 1
                n = j - i + 1
                if n >= NOTE_PER_ACCORDO:
                    in_accordo += n
                i = j + 1
            quote[f].append(in_accordo / len(pos))
    print('\nMISURA 5 -- il piano contro la sezione ritmica')
    print(f'   {usati} esecuzioni, {len(esecutori)} pianisti')
    print(f'   ATTACCHI del piano per battuta: mediana {st.median(densita):.2f}'
          '   [MIS]')
    print('   (attacchi, non note: un accordo conta uno. E la grandezza'
          ' confrontabile')
    print('    con la densita di basso e batteria, che sono onset anche loro)')
    if con_basso:
        print(f'   correlazione con la densita del BASSO nella stessa battuta: '
              f'mediana {st.median(con_basso):+.3f}')
    if con_batteria:
        print(f'   correlazione con la densita della BATTERIA: '
              f'mediana {st.median(con_batteria):+.3f}')
    print('   quota di onset in accordo (= comping) -- [IPO], dipende dalla'
          ' finestra:')
    for f in finestre:
        print(f'      entro {f * 1000:3.0f} ms: {100 * st.median(quote[f]):5.1f}%')
    forbice = 100 * (st.median(quote[max(finestre)])
                     - st.median(quote[min(finestre)]))
    print(f'   FORBICE fra la finestra piu stretta e la piu larga: '
          f'{forbice:.1f} punti')
    print('   -> se la forbice supera 15 punti, il numero NON si scrive nella'
          ' scheda: si scrive la forbice')
    return {'densita': st.median(densita),
            'quote': {f: st.median(v) for f, v in quote.items()},
            'forbice': forbice,
            'con_basso': st.median(con_basso) if con_basso else None,
            'con_batteria': st.median(con_batteria) if con_batteria else None,
            'esecuzioni': usati, 'esecutori': len(esecutori)}


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
    fasi: list[float] = []
    esecutori, usati = set(), 0
    for b in brani:
        d = JT.battute(z, b.fname)
        if len(d.battute) < MINIMO_BATTUTE:
            continue
        usati += 1
        esecutori.add(b.bassista)
        for x in d.battute:
            fuori = onset_fuori_griglia(x)
            for i, bt in enumerate(x.beat):
                fine = (x.beat[i + 1].istante if i + 1 < len(x.beat)
                        else x.fine)
                if fine <= bt.istante:
                    continue
                for o in fuori:
                    if not bt.istante < o < fine:
                        continue
                    fase = (o - bt.istante) / (fine - bt.istante)
                    istogramma[int(fase / PASSO_FASE)] += 1
                    fasi.append(fase)
    tot = len(fasi)

    print('\nMISURA 6 -- dove cade la nota in piu del basso')
    print(f'   {tot} onset fuori dai beat, {usati} esecuzioni, '
          f'{len(esecutori)} bassisti')
    if not tot:
        return {'istogramma': {}, 'onsets': 0, 'picco': 0.0, 'piatta': True,
                'esecuzioni': usati, 'esecutori': len(esecutori)}
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

    # ⚠️ IL PICCO DIPENDE DA COME SI SCEGLIE L'INTERVALLO, e l'ampiezza
    # `PASSO_FASE` e' una decisione arbitraria. Se al variare dell'ampiezza il
    # picco si sposta piu' della tolleranza del criterio, il criterio non puo'
    # decidere: e' un fatto sulla statistica scelta, non sui dati, e va
    # stampato invece che scoperto dopo.
    picchi = []
    for larghezza in (0.02, 0.04, 0.05, 0.10):
        agg = collections.Counter()
        for k, v in istogramma.items():
            agg[int(k * PASSO_FASE / larghezza)] += v
        p = max(agg, key=lambda x: agg[x])
        picchi.append((p + 0.5) * larghezza)
    print('   picco al variare dell ampiezza (0,02 0,04 0,05 0,10): '
          + '  '.join(f'{p:.3f}' for p in picchi))
    fragile = max(picchi) - min(picchi) > TOLLERANZA_PICCO

    fasi.sort()
    q = [fasi[int(len(fasi) * f)] for f in (0.25, 0.5, 0.75)]
    print(f'   mediana {q[1]:.3f}, quartili {q[0]:.3f}-{q[2]:.3f} '
          '(non dipendono dall ampiezza degli intervalli)')

    if fragile:
        print(f'   ATTENZIONE: IL PICCO SI SPOSTA DI {max(picchi) - min(picchi):.3f} '
              f'al variare dell ampiezza, piu della tolleranza '
              f'{TOLLERANZA_PICCO}: il criterio fissato sul picco NON PUO '
              'DECIDERE, e la statistica da leggere e la mediana')
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
            'piatta': piatta, 'fragile': fragile, 'picchi': picchi,
            'mediana': q[1], 'quartili': (q[0], q[2]),
            'esecuzioni': usati, 'esecutori': len(esecutori)}


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
        return {'distribuzione': {}, 'medie': [], 'esecuzioni': 0,
                'esecutori': 0, 'battute': 0}
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
        print('   ATTENZIONE: va scritto accanto al numero: vorrebbe dire '
              'varieta dentro un esecuzione dipende da quanto denso suona')
    print('   da incollare in tools/genera_jazz.py:')
    print(f'   DISTRIBUZIONE_BASSO = {dict(sorted(conti.items()))}')
    return {'distribuzione': dict(conti), 'medie': medie,
            'esecuzioni': len(medie), 'esecutori': len(esecutori),
            'battute': tot, 'media': media, 'deviazione': dev}


#: Il criterio della misura 8, FISSATO PRIMA DI GUARDARE (6 settembre 2026,
#: dopo il verdetto sulla versione 08). Sopra questa autocorrelazione a
#: distanza 1 una linea NON e' una sequenza di battute indipendenti, e il
#: generatore -- che pesca ogni battuta per conto suo -- sbaglia struttura pur
#: avendo le marginali giuste. Sotto, l'indipendenza regge e «troppe
#: variazioni» vuol dire un'altra cosa, da cercare altrove.
SOGLIA_AUTOCORRELAZIONE = 0.10


def la_continuita(z, brani) -> dict:
    """MISURA 8. Una battuta somiglia a quella prima?

    Nasce da un ascolto, non da un'agenda: sulla versione 08 del blues
    l'utente ha detto «il basso ora ha un po' troppe variazioni» e «la
    batteria resta discontinua», mentre i numeri dicevano che il pezzo era
    MENO vario del corpus. Se un bassista vero varia in modo correlato da una
    battuta all'altra, allora pescare ogni battuta indipendente e' sbagliato
    anche quando la distribuzione e' giusta -- e sarebbe lo stesso difetto
    gia' dichiarato per la batteria in `_voce_dal_profilo()`.

    Due numeri per strumento: l'autocorrelazione a distanza 1 dei conti per
    battuta, e la quota di battute che hanno lo STESSO conto della precedente
    -- il secondo perche' e' leggibile, il primo perche' e' confrontabile.
    """
    fuori = {}
    for strumento in ('bass', 'drums'):
        auto, uguali, medie, devi = [], [], [], []
        esecutori, usati = set(), 0
        istogramma = collections.Counter()
        for b in brani:
            d = JT.battute(z, b.fname)
            if len(d.battute) < MINIMO_BATTUTE:
                continue
            conti = [x.densita[strumento] for x in d.battute]
            if st.pstdev(conti) == 0:
                continue
            usati += 1
            esecutori.add(b.bassista if strumento == 'bass' else b.batterista)
            auto.append(_correlazione(conti[:-1], conti[1:]))
            uguali.append(sum(1 for a, c in zip(conti, conti[1:]) if a == c)
                          / (len(conti) - 1))
            medie.append(st.mean(conti))
            devi.append(st.pstdev(conti))
            istogramma.update(conti)
        fuori[strumento] = {
            'autocorrelazione': st.median(auto) if auto else None,
            'uguali': st.median(uguali) if uguali else None,
            'media': st.median(medie) if medie else None,
            'deviazione': st.median(devi) if devi else None,
            'istogramma': dict(istogramma),
            'esecuzioni': usati, 'esecutori': len(esecutori)}

    print('\nMISURA 8 -- la continuita fra una battuta e la successiva')
    for strumento, r in fuori.items():
        if r['autocorrelazione'] is None:
            print(f'   {strumento}: n/d')
            continue
        print(f'   {strumento:6}  {r["esecuzioni"]} esecuzioni, '
              f'{r["esecutori"]} esecutori')
        print(f'           autocorrelazione a distanza 1: mediana '
              f'{r["autocorrelazione"]:+.3f}')
        print(f'           battute con lo stesso conto della precedente: '
              f'{100 * r["uguali"]:.1f}%')
        oltre = abs(r['autocorrelazione']) > SOGLIA_AUTOCORRELAZIONE
        print(f'           -> {"NON e" if oltre else "e"} una sequenza di '
              f'battute indipendenti (soglia {SOGLIA_AUTOCORRELAZIONE})')
        print(f'           colpi per battuta: mediana delle medie '
              f'{r["media"]:.2f}, delle deviazioni {r["deviazione"]:.2f}')
        # ⚠️ Sotto indipendenza la quota di battute uguali alla precedente e'
        # decisa SOLO dalla forma della distribuzione, quindi la si stampa
        # accanto: e' li' che il generatore diverge, non nella correlazione.
        tot = sum(r['istogramma'].values())
        coda = [f'{n}:{100 * q / tot:.1f}%'
                for n, q in sorted(r['istogramma'].items()) if q / tot >= 0.02]
        print(f'           distribuzione ({tot} battute): ' + '  '.join(coda))
    return fuori


def main() -> int:
    """Le sette misure, DUE volte: su tutto il corpus e sul solo JTD-300.

    Se le due passate divergono vince JTD-300 -- che e' il sottoinsieme su cui
    gli autori hanno lavorato di piu' -- e la divergenza si scrive. E' il modo
    in cui questo progetto distingue un risultato da un artefatto del
    campione.
    """
    if not ZIP.exists():
        print(f'manca {ZIP}')
        return 1
    with JT.apri(ZIP) as z:
        for etichetta, curati in (('TUTTO IL CORPUS', False),
                                  ('SOLO JTD-300 (curato)', True)):
            brani = _brani(z, curati)
            print(f'\n{"=" * 68}\n{etichetta} -- {len(brani)} esecuzioni in 4/4\n')
            densita_del_basso(z, brani)
            il_beat_saltato(z, brani)
            accoppiamento(z, brani)
            chi_sta_avanti(z, brani)
            il_piano(z, brani)
            dove_cade_la_nota_in_piu(z, brani)
            dentro_una_esecuzione(z, brani)
            la_continuita(z, brani)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
