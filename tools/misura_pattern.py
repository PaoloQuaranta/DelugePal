"""Chi tiene il tempo, e quanto lo tiene uguale: i pattern battuta per battuta.

    .venv/Scripts/python.exe tools/misura_pattern.py > out/pattern_jazz.txt

Nasce dal verdetto del 10 settembre 2026 sulla versione 10 del blues:

    «la batteria non va ancora bene, suona a grappoli di eventi discontinui.
    manca il flow di un ritmo costante mantenuto da qualche parte. il piu'
    classico e' il giggidi' del ride, che hai usato fino a jazz 06»

⚠️ E' la casella che `_voce_dal_profilo()` dichiarava aperta dal 30 agosto:
«riproduce la DENSITA' di ogni passo, non le CORRELAZIONI fra passi nella
stessa battuta. Un batterista che alterna due figure intere qui esce con le
due figure mescolate. Per averle davvero servirebbe leggere le battute una
per una». Questo strumento le legge una per una.

TUTTE LE SOGLIE STANNO QUI, non in `groove.py`: il lettore non decide niente
di musicale.

IL CRITERIO E' FISSATO PRIMA DI GUARDARE (10 settembre 2026): una voce TIENE
IL TEMPO se il suo pattern piu' frequente copre almeno `SOGLIA_TENUTA` delle
battute in cui quella voce suona. Sotto, e' una voce che commenta e non una
che tiene.
"""
from __future__ import annotations

import collections
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import groove as GR                          # noqa: E402
from delugexml import midi as MI                            # noqa: E402

BASE = (Path(__file__).resolve().parent.parent / 'to-read' / 'MIDI'
        / 'groove-v1.0.0-midionly' / 'groove')

#: Quanta parte delle battute deve coprire il pattern piu' frequente di una
#: voce perche' quella voce si dica «tiene il tempo». Fissata prima di
#: guardare: meta' e' il punto in cui «di solito fa questo» smette di essere
#: un modo di dire.
SOGLIA_TENUTA = 0.50

#: Sotto questo numero di battute un'esecuzione non entra: da dieci battute
#: non si dice se un pattern e' costante.
MINIMO_BATTUTE = 16

#: Lo spang-a-lang, i sei passi del «giggidi'»: battere, levare swingato del
#: 2 e del 4. E' l'ipotesi che il verdetto nomina, e qui si controlla se il
#: corpus la porta davvero invece di darla per buona.
SPANG = (0, 4, 6, 8, 12, 14)

TICK_BATTUTA = 384
TICK_PASSO = 24


#: Le tre note GM che sono lo STESSO piatto suonato in tre zone. Tenerle
#: separate spezza il disegno che si cerca: sul batterista del blues il `ride`
#: da solo copre 53 battute su 80 e il resto sta in `ride 2` e `campana del
#: ride`. ⚠️ E' una DECISIONE dichiarata, ed e' la stessa lezione gia' scritta
#: nella casella 10: il nome GM non e' il ruolo musicale.
FAMIGLIE = {
    'ride': ('ride', 'ride 2', 'campana del ride'),
    'charleston': ('charleston chiuso', 'charleston aperto'),
}


def battute_per_voce(base, id: str, *, taglio: str = 'voce') -> dict:
    """Per ogni voce, il pattern a 16 passi di OGNI battuta dell'esecuzione.

    ⚠️ USA LA STESSA CATENA DI `profilo_da_colpi()`, e non e' un vezzo: si
    toglie l'ORIGINE della griglia, si misura il BUR e SI TOGLIE LO SWING, e
    solo allora si sceglie il passo, con lo spostamento del taglio per voce.
    Il commento di quella funzione lo dice: «il passo si decide DOPO aver
    tolto lo swing: un levare swingato sta a 2,67 passi e si arrotonderebbe
    al 3».

    La prima stesura di questo strumento, il 10 settembre 2026, tagliava sul
    passo piu' vicino senza togliere lo swing, e ne usciva che il ride del
    jazz porta il giggidi' completo solo nell'11% delle battute -- che e' un
    artefatto del taglio, non un fatto sui batteristi.
    """
    e = GR._una(base, id)
    f = MI.leggi(Path(base) / e.midi_filename)
    fattore = MI.TICK_PER_MOVIMENTO_DELUGE / f.ppq
    ppq = float(MI.TICK_PER_MOVIMENTO_DELUGE)
    passo_tick = ppq / 4

    inverso = {n: fam for fam, nomi in FAMIGLIE.items() for n in nomi}
    colpi: dict[str, list[float]] = {}
    for t in f.tracce:
        for n in t.note:
            nome = MI.GM_PERCUSSIONI.get(n.y)
            if nome is None:
                continue                # una percussione fuori dalla mappa GM
            colpi.setdefault(inverso.get(nome, nome), []).append(
                n.pos * fattore)
    if not colpi:
        return {}

    tutte = [p for v in colpi.values() for p in v]
    off = GR.origine(tutte, passo_tick)
    bur = GR.bur_da_posizioni([p - off for p in tutte], ppq)
    levare = GR.da_bur(bur) if bur is not None else 0.5

    dritte: dict[str, list[float]] = {}
    for nome, posizioni in colpi.items():
        for pos in posizioni:
            movimento, resto = divmod(pos - off, ppq)
            dritte.setdefault(nome, []).append(
                (movimento + GR._senza_swing(resto / ppq, levare)) * ppq)

    per_voce: dict[str, dict[int, set[int]]] = {}
    ultima = 0
    for nome, note in dritte.items():
        sp = GR.spostamento_del_taglio(note, passo_tick, taglio)
        for dritta in note:
            passo = round((dritta - sp) / passo_tick)
            if passo < 0:
                continue                # prima dell'origine: fuori griglia
            battuta, dentro = divmod(passo, 16)
            per_voce.setdefault(nome, {}).setdefault(battuta, set()).add(dentro)
            ultima = max(ultima, battuta)

    return {voce: [''.join('x' if i in per_battuta.get(b, ()) else '.'
                           for i in range(16))
                   for b in range(ultima + 1)]
            for voce, per_battuta in per_voce.items()}


def per_passo(patterns: list[str]) -> list[float]:
    """Quanto spesso ogni passo viene colpito, sulle battute in cui la voce
    suona. E' il numero che serve a un generatore: un pattern intero al 15%
    non si copia, sedici probabilita' si'."""
    suonate = [p for p in patterns if 'x' in p]
    if not suonate:
        return [0.0] * 16
    return [sum(1 for p in suonate if p[i] == 'x') / len(suonate)
            for i in range(16)]


def _tenuta(patterns: list[str]) -> dict:
    """Quanto una voce ripete se stessa, sulle battute in cui suona."""
    suonate = [p for p in patterns if 'x' in p]
    if len(suonate) < MINIMO_BATTUTE:
        return {}
    conti = collections.Counter(suonate)
    piu_frequente, quante = conti.most_common(1)[0]
    # quanti pattern diversi servono per coprire l'80% delle battute
    corso, servono = 0, 0
    for _, q in conti.most_common():
        corso += q
        servono += 1
        if corso >= 0.8 * len(suonate):
            break
    uguali = sum(1 for a, b in zip(suonate, suonate[1:]) if a == b)
    return {'battute': len(suonate), 'diversi': len(conti),
            'pattern': piu_frequente, 'copertura': quante / len(suonate),
            'per_80': servono,
            'uguale_alla_precedente': uguali / max(1, len(suonate) - 1),
            'colpi': st.mean(p.count('x') for p in suonate)}


def main() -> int:
    if not BASE.exists():
        print(f'manca {BASE}')
        return 1

    esecuzioni = [e for e in GR.elenco(BASE, style='jazz',
                                       time_signature='4-4')]
    print(f'{len(esecuzioni)} esecuzioni jazz in 4/4 nel Groove MIDI Dataset')
    print(f'criterio fissato prima: tiene il tempo chi copre almeno '
          f'{SOGLIA_TENUTA:.0%} delle proprie battute con UN pattern\n')

    per_voce = collections.defaultdict(list)
    passi_voce = collections.defaultdict(list)
    tengono = collections.Counter()
    presenze = collections.Counter()
    spang_pieno, spang_totale = 0, 0
    usate = 0

    for e in esecuzioni:
        try:
            patterns = battute_per_voce(BASE, e.id)
        except Exception as exc:                             # noqa: BLE001
            print(f'   saltata {e.id}: {type(exc).__name__}: {exc}')
            continue
        if not patterns:
            continue
        usate += 1
        for voce, righe in patterns.items():
            r = _tenuta(righe)
            if not r:
                continue
            presenze[voce] += 1
            per_voce[voce].append(r)
            passi_voce[voce].append(per_passo(righe))
            if r['copertura'] >= SOGLIA_TENUTA:
                tengono[voce] += 1
        # il giggidi': quante battute di ride portano TUTTI e sei i passi
        for voce in ('ride',):
            for riga in patterns.get(voce, []):
                if 'x' not in riga:
                    continue
                spang_totale += 1
                if all(riga[i] == 'x' for i in SPANG):
                    spang_pieno += 1

    print(f'{usate} esecuzioni lette\n')
    print(f'{"voce":22} {"esec":>5} {"tiene":>6} {"copert":>7} '
          f'{"=prec":>6} {"divers":>7} {"per80":>6} {"colpi":>6}')
    for voce, righe in sorted(per_voce.items(),
                              key=lambda kv: -len(kv[1])):
        if len(righe) < 3:
            continue
        cop = st.median(r['copertura'] for r in righe)
        ug = st.median(r['uguale_alla_precedente'] for r in righe)
        dv = st.median(r['diversi'] for r in righe)
        p80 = st.median(r['per_80'] for r in righe)
        col = st.median(r['colpi'] for r in righe)
        quota = tengono[voce] / presenze[voce]
        print(f'{voce:22} {presenze[voce]:5} {quota:6.0%} {cop:7.1%} '
              f'{ug:6.1%} {dv:7.0f} {p80:6.0f} {col:6.2f}')

    print(f'\nil giggidi\': su {spang_totale} battute di ride, '
          f'{spang_pieno} portano tutti e sei i passi {SPANG} = '
          f'{100 * spang_pieno / max(1, spang_totale):.1f}%')

    # ⚠️ IL NUMERO CHE SERVE A UN GENERATORE non e' il pattern intero -- il
    # piu' frequente copre il 15% delle battute e non si copia -- ma quanto
    # spesso viene colpito OGNI PASSO. Un ride che colpisce i sei passi del
    # giggidi' nove volte su dieci tiene il tempo; uno che li colpisce meta'
    # delle volte suona a grappoli, ed e' il difetto sentito il 10 settembre.
    print('\nquanto spesso ogni passo viene colpito, sulle battute in cui la '
          'voce suona')
    print(f'{"voce":22} ' + ' '.join(f'{i:4}' for i in range(16))
          + '   colpi')
    for voce in ('ride', 'kick', 'rullante', 'charleston a pedale',
                 'charleston'):
        righe = passi_voce.get(voce)
        if not righe:
            continue
        media = [st.mean(x[i] for x in righe) for i in range(16)]
        print(f'{voce:22} ' + ' '.join(f'{100 * m:4.0f}' for m in media)
              + f'   {sum(media):5.2f}')

    print('\nsu quanti passi il ride sta sopra il 50%: ', end='')
    righe = passi_voce.get('ride', [])
    if righe:
        media = [st.mean(x[i] for x in righe) for i in range(16)]
        sopra = [i for i, m in enumerate(media) if m >= 0.5]
        print(f'{sopra}  (il giggidi\' e\' {list(SPANG)})')
    else:
        print('n/d')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
