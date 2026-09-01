"""I controlli da passare PRIMA di fidarsi di un numero preso dal JTD.

    .venv/Scripts/python.exe tools/controlla_jtd.py > out/controlli_jtd.txt

Nessuno di questi cinque fa fallire un test se salta: sbaglierebbero in
silenzio ogni misura a valle. Per questo stanno in uno strumento a parte e il
loro esito si SCRIVE, anche quando l'esito e' «va bene».

Il primo e' l'unico che puo' fermare il lavoro: se il beat annotato non fosse
quello che il tempo dichiarato conta, ogni densita' «per battuta» sarebbe
sbagliata di un fattore due, e nessun test se ne accorgerebbe.
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

#: Quanto lontano da un beat puo' stare un onset perche' si possa dire che
#: «e' quel beat». 50 ms a 200 bpm sono un sesto di beat: larga abbastanza da
#: assorbire il rilevatore, stretta abbastanza da non inghiottire una croma.
#: E' una SCELTA dichiarata, non una legge.
FINESTRA_VICINO = 0.050


def uno_il_beat_e_quello_che_il_tempo_conta(z, brani):
    """CONTROLLO 1. Il beat annotato e' quello che il tempo dichiarato conta?

    Se non lo fosse, ogni densita' per battuta sarebbe sbagliata di un
    fattore due. Si confronta 60/intervallo-fra-i-beat col campo `tempo`.
    """
    rapporti = []
    for b in brani:
        g = JT.griglia(z, b.fname)
        if len(g) < 8 or not b.tempo:
            continue
        ibi = st.median([y.istante - x.istante for x, y in zip(g, g[1:])])
        if ibi > 0:
            rapporti.append((60 / ibi) / b.tempo)
    r = sorted(rapporti)
    print('CONTROLLO 1 -- il beat annotato e quello che il tempo conta')
    print(f'   (60/intervallo) / tempo dichiarato, su {len(r)} brani:')
    print(f'   mediana {st.median(r):.4f}   min {r[0]:.3f}   max {r[-1]:.3f}')
    ok = 0.95 < st.median(r) < 1.05
    print(f'   ESITO: {"passa" if ok else "NON PASSA -- FERMARSI"}')
    return ok


def due_la_cella_vuota_e_un_silenzio(z, brani):
    """CONTROLLO 2. Una cella vuota deve voler dire «non ha suonato».

    Se in quell'intorno un onset grezzo c'e', e' il rilevatore che ha mancato
    l'allineamento: allora la misura 2 conterebbe errori invece che silenzi.
    """
    muti = smentiti = 0
    for b in brani:
        g = JT.griglia(z, b.fname)
        ons = JT.onsets(z, b.fname, 'bass')
        i = 0
        for beat in g:
            if not beat.tace('bass'):
                continue
            muti += 1
            while i < len(ons) and ons[i] < beat.istante - FINESTRA_VICINO:
                i += 1
            if i < len(ons) and abs(ons[i] - beat.istante) <= FINESTRA_VICINO:
                smentiti += 1
    perc = 100 * smentiti / muti if muti else 0.0
    print('\nCONTROLLO 2 -- la cella vuota e un silenzio, non un errore')
    print(f'   beat in cui il basso tace: {muti}')
    print(f'   di questi, con un onset grezzo entro '
          f'{FINESTRA_VICINO * 1000:.0f} ms: {smentiti} ({perc:.1f}%)')
    print(f'   ESITO: {"passa" if perc < 10 else "ATTENZIONE: va dichiarato"}')
    return perc


def tre_i_nan_sono_spariti(z, brani):
    """CONTROLLO 3. Nessun `float('nan')` deve uscire da `metadati()`.

    Ogni confronto con lui e' falso, `==` compreso: sbaglia in silenzio.
    """
    trovati = 0
    for b in brani:
        for v in JT.metadati(z, b.fname).values():
            if isinstance(v, float) and v != v:
                trovati += 1
    print('\nCONTROLLO 3 -- i NaN di metadata.json sono diventati None')
    print(f'   NaN sopravvissuti: {trovati}')
    print(f'   ESITO: {"passa" if trovati == 0 else "NON PASSA"}')
    return trovati == 0


def quattro_i_tre_quarti_stanno_a_parte(z):
    """CONTROLLO 4. Una densita' per battuta mediata fra 3/4 e 4/4 non vuol
    dire niente. Si contano e si tengono fuori."""
    q = JT.elenco(z, metro=4)
    t = JT.elenco(z, metro=3)
    print('\nCONTROLLO 4 -- i 3/4 stanno a parte')
    print(f'   brani in 4/4: {len(q)}   in 3/4: {len(t)}')
    print('   ESITO: le misure girano sui soli 4/4, e il numero dei 3/4 si cita')
    return len(q), len(t)


def cinque_il_campione_regge(z, brani):
    """CONTROLLO 5. Quanti esecutori distinti reggono i numeri, e quanto pesa
    il piu' rappresentato.

    Un corpus dominato da un esecutore misurerebbe LUI, non il repertorio:
    e' la trappola gia' vista con la casella 6 del reggae, dove venti
    esecuzioni di due batteristi stavano per essere firmate col nome di un
    genere.
    """
    per_bassista = collections.Counter(b.bassista for b in brani)
    per_batterista = collections.Counter(b.batterista for b in brani)
    per_pianista = collections.Counter(b.pianista for b in brani)
    print('\nCONTROLLO 5 -- il campione regge')
    for nome, c in (('bassisti', per_bassista),
                    ('batteristi', per_batterista),
                    ('pianisti', per_pianista)):
        primo, quante = c.most_common(1)[0]
        print(f'   {nome:11}: {len(c):3} distinti; il piu presente e {primo} '
              f'con {quante} brani ({100 * quante / sum(c.values()):.1f}%)')
    return per_bassista, per_batterista


def main() -> int:
    if not ZIP.exists():
        print(f'manca {ZIP}')
        return 1
    with JT.apri(ZIP) as z:
        brani = JT.elenco(z, metro=4)
        print(f'JTD: {len(brani)} brani in 4/4\n')
        if not uno_il_beat_e_quello_che_il_tempo_conta(z, brani):
            print('\nATTENZIONE -- FERMARSI: il controllo 1 non passa.')
            return 2
        due_la_cella_vuota_e_un_silenzio(z, brani)
        tre_i_nan_sono_spariti(z, brani)
        quattro_i_tre_quarti_stanno_a_parte(z)
        cinque_il_campione_regge(z, brani)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
