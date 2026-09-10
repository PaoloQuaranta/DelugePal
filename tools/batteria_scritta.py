"""La batteria del blues, SCRITTA seguendo `docs/istruzioni/batteria-jazz.md`.

⚠️ Nessun sorteggio. Ogni colpo viene dai principi di John Riley, *The Art of
Bop Drumming*, e accanto a ogni riga c'e' scritto quale.

LA STRUTTURA DEL FILE RIFLETTE LA DIVISIONE DEI RUOLI, ed e' il punto:

  - `RIDE` e `PEDALE` TENGONO IL TEMPO. Sono due stringhe sole, uguali in
    ogni battuta, e non cambiano mai. Riley p. 8: le quattro semiminime di
    uguale intensita' piu' la nota di skip, il charleston su 2 e 4, e ogni
    nota che scorre nella successiva -- quindi il ride NON si buca;
  - `FIGURE` e `PIANO` PARLANO. Il rullante e' la voce principale del
    comping, la cassa fa le bombe sulla stessa figura (p. 24, «come una terza
    mano», e «non suonare le semiminime con la cassa»).

L'UNITA' NON E' LA BATTUTA, E' LA FRASE DI DUE BATTUTE. Riley p. 20: si suona
una frase di due battute, la si RIPETE, e poi si TACE tenendo solo il tempo.
Quando un'idea si ripete cosi' si chiama «riff». Il generatore a sorteggio
non ripeteva mai e non taceva mai, ed e' il difetto sentito il 10 settembre:
«suona a grappoli di eventi discontinui».

I passi, sulla griglia a sedicesimi: 0 = movimento 1, 4 = movimento 2,
8 = movimento 3, 12 = movimento 4. I dispari 2, 6, 10, 14 sono i levare, che
il firmware swinga.
"""
from __future__ import annotations

#: IL RIDE, in ogni battuta e senza eccezioni. Sei colpi: i quattro movimenti
#: piu' i levare del 2 e del 4. `[MIS]` che siano proprio questi sei: sono i
#: soli passi che il ride colpisce in piu' di meta' delle battute su 21
#: esecuzioni jazz del Groove MIDI (78, 76, 65, 75, 71, 61 per cento).
RIDE = 'x...x.x.x...x.x.'

#: IL CHARLESTON A PEDALE, sui movimenti 2 e 4. `[LIB]` Riley p. 8.
PEDALE = '....x.......x...'

#: Il vocabolario del comping: figure di DUE battute, (rullante, cassa).
#: ⚠️ Sono scritte qui, non campionate: le figure di Riley (pp. 18-29) sono in
#: notazione e la notazione non e' ancora stata letta. `[DEC]`, e vanno
#: sostituite quando quelle pagine saranno trascritte.
FIGURE = {
    # domanda corta: un colpo sul levare del 2, risposta sul 4 con la bomba
    'corta': (('......x.........', '................'),
              ('............x...', '......x.........')),

    # domanda su due colpi, risposta che anticipa: comincia sul levare di 1
    'anticipa': (('....x.....x.....', '..............x.'),
                 ('..x.............', '........x.......')),

    # la piu' densa, per il culmine dell'assolo: quattro colpi e due bombe
    'culmine': (('..x...x...x.....', '....x.......x...'),
                ('......x.....x.x.', 'x...............')),

    # la chiusa: un accento solo sul primo movimento, e poi silenzio
    'chiusa': (('x...............', 'x...............'),
               ('................', '................')),
}

#: DOVE vanno le figure: battuta di partenza (da 1) -> nome della figura.
#: Ogni figura occupa DUE battute. Le battute che non compaiono qui sono
#: «tempo»: suonano solo ride e charleston.
#:
#: L'arco segue Riley p. 30, «il solista puo' fare tre cose: salire verso un
#: culmine, scendere, o stare in piano», e le frasi si appoggiano sulle TRE
#: FRASI DA QUATTRO in cui si divide il blues (p. 32).
PIANO = {
    # --- primo giro, il TEMA: sta in piano, lascia spazio -----------------
    3:  'corta',        # chiude la prima frase di quattro
    7:  'corta',        # la stessa figura RIPETUTA: e' il «riff» di Riley
    # 9-12: tempo. Alla 12 c'e' il fill del turnaround

    # --- secondo giro, l'ASSOLO: sale -------------------------------------
    13: 'anticipa',
    15: 'anticipa',     # ripetuta
    # 17-18: tempo, il respiro che Riley chiede fra una frase e l'altra
    19: 'culmine',
    21: 'culmine',      # ripetuta: e' il punto piu' alto del pezzo
    # 23: tempo. Alla 24 il fill

    # --- terzo giro, il TEMA di nuovo: scende ------------------------------
    # 25-26: tempo
    27: 'corta',
    # 29-32: tempo, la discesa
    33: 'corta',
    35: 'chiusa',       # 35 l'accento, 36 silenzio sotto il ride
}

#: Le voci che parlano, nell'ordine in cui `FIGURE` le porta.
PARLANO = ('rullante', 'kick')


def per_battuta(battute: int) -> list[dict[str, str]]:
    """Per ogni battuta, `{voce: pattern}`. Le voci sono quelle del profilo.

    Ride e charleston ci sono sempre. Rullante e cassa solo dove il piano
    mette una figura: altrove tacciono, ed e' il silenzio che fa la frase.
    """
    fuori = [{'ride': RIDE, 'charleston a pedale': PEDALE}
             for _ in range(battute)]
    for prima, nome in PIANO.items():
        figura = FIGURE.get(nome)
        if figura is None:
            raise ValueError(f'battuta {prima}: figura {nome!r} sconosciuta, '
                             f'ci sono {sorted(FIGURE)}')
        for scarto, (rullante, cassa) in enumerate(figura):
            b = prima - 1 + scarto
            if b >= battute:
                raise ValueError(f'la figura {nome!r} alla battuta {prima} '
                                 f'esce dal pezzo, che ha {battute} battute')
            if 'x' in rullante:
                fuori[b]['rullante'] = rullante
            if 'x' in cassa:
                fuori[b]['kick'] = cassa
    return fuori


def racconta(battute: int = 36) -> str:
    """Una riga per battuta, per guardare la forma invece di immaginarla."""
    righe = []
    for i, voci in enumerate(per_battuta(battute), 1):
        parla = [v for v in PARLANO if v in voci]
        righe.append(f'{i:3}  {voci["ride"]}  '
                     f'{voci.get("rullante", "." * 16)}  '
                     f'{voci.get("kick", "." * 16)}'
                     + ('' if parla else '   (tempo)'))
    return '\n'.join(righe)


if __name__ == '__main__':
    print('  b  ride              rullante          cassa')
    print(racconta())
    parlate = sum(1 for v in per_battuta(36) if 'rullante' in v or 'kick' in v)
    print(f'\n{parlate} battute su 36 hanno comping, '
          f'{36 - parlate} sono solo tempo')
