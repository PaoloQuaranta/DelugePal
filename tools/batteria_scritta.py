"""La batteria del blues, SCRITTA guardando le battute di un batterista vero.

⚠️ NESSUN SORTEGGIO, e nessuna statistica. La struttura viene dall'aver
guardato una per una le 85 battute di `drummer10/session1/1` nel Groove MIDI
Dataset -- lo stesso batterista da cui il pezzo prende il tocco -- con
`GR.battute_per_voce()`. `[OSS]` su un esecutore.

COSA MOSTRANO QUELLE BATTUTE, ed e' l'opposto di come questa parte era
scritta il 10 settembre 2026:

  - le quattro voci suonano QUASI SEMPRE. Su 85 battute: charleston a pedale
    80, rullante 77, cassa 70, ride 54. Nessuna di loro «entra ogni tanto»;
  - sotto c'e' uno STRATO COSTANTE, uguale in ogni battuta di tempo normale:
    il ride fa il giggidi', la cassa fa QUATTRO MOVIMENTI (il feathering), il
    charleston sta su 2 e 4, il rullante sta sul MOVIMENTO 2;
  - la varieta' sono AGGIUNTE SOPRA quello strato, non presenza o assenza. Il
    rullante tiene il 2 e ci mette sopra da zero a tre colpi, sui levare e sui
    movimenti 3 e 4.

⚠️ DUE COSE CHE AVEVO SCRITTO E SONO SBAGLIATE:

  1. «la cassa non suona i quarti» -- lo dice Riley a p. 24, ma e' un
     ESERCIZIO per sviluppare la cassa come terza mano. Questo batterista
     suona `x...x...x...x...` per decine di battute di fila. E' il
     *feathering*, e le velocity del groove template lo rendono leggero;
  2. «due battute di frase, poi quattro di silenzio» -- Riley p. 20, ed e'
     anche quello un esercizio di pacing, non una descrizione. Preso alla
     lettera ha prodotto una batteria che l'orecchio ha respinto: «a parte il
     ride il resto e' troppo rarefatto, praticamente assente per intere
     battute».

⚠️ E UNA TERZA, dopo il verdetto sulla versione 14: «quasi sempre» non e'
«sempre». Il batterista suona la cassa in 70 battute su 85 e il rullante in
77, e le sue assenze sono SEZIONALI -- nelle battute 1-8 la cassa non c'e'
affatto. Riempire ogni battuta ha dato una batteria «un po' pesante», e
«un buon groove deve lasciare anche spazio agli altri strumenti». Da qui le
`SEZIONI`, e le aggiunte che rispondono ai buchi della melodia invece di
raddoppiarla.

I passi, sulla griglia a sedicesimi: 0 = movimento 1, 4 = movimento 2,
8 = movimento 3, 12 = movimento 4. I dispari 2, 6, 10, 14 sono i levare, che
il firmware swinga.
"""
from __future__ import annotations

#: LO STRATO COSTANTE: cosa suona ogni voce in OGNI battuta.
#: Osservato sulle battute 13-20 e 29-44 di `drummer10/session1/1`, dove il
#: tempo e' normale. `[OSS]`.
STRATI = {
    #: il giggidi'. `[MIS]` che siano proprio questi sei passi: sono i soli
    #: che il ride colpisce in piu' di meta' delle battute su 21 esecuzioni
    #: jazz del Groove MIDI.
    'ride': 'x...x.x.x...x.x.',
    #: 2 e 4. `[LIB]` Riley p. 8, e `[OSS]` in 80 battute su 85.
    'charleston a pedale': '....x.......x...',
    #: il movimento 2, che questo batterista tiene quasi ovunque. E' l'ancora
    #: del rullante, non il suo comping: quello sta nelle aggiunte.
    'rullante': '....x...........',
    #: IL FEATHERING: quattro movimenti, leggeri. Le velocity le mette il
    #: groove template, che su questo esecutore da' colpi bassi sui movimenti
    #: 1 e 3.
    'kick': 'x...x...x...x...',
}

#: LE SEZIONI: dove lo strato cambia. `(prima, ultima, nome, sostituzioni)`.
#:
#: ⚠️ Nasce dal verdetto sulla versione 14: «in generale è giusto variare
#: aggiungendo piuttosto che togliere, ma non si può applicare come una regola
#: assoluta. un buon groove di batteria deve lasciare anche spazio agli altri
#: strumenti, non può riempire sempre tutto».
#:
#: Avevo trasformato «quasi sempre» in «sempre»: il batterista vero suona la
#: cassa in 70 battute su 85 e il rullante in 77, non in tutte. E `[OSS]` le
#: sue assenze sono SEZIONALI, non sparse: nelle battute 1-8 la cassa non c'e'
#: affatto, poi entra e resta.
#:
#: Qui la cassa fa il feathering pieno solo sotto l'assolo. Sotto i due temi
#: batte 1 e 3, che e' meta' del peso, perche' li' la melodia ha bisogno di
#: spazio.
SEZIONI = (
    (1,  12, 'tema',   {'kick': 'x.......x.......'}),
    (13, 24, 'assolo', {}),
    (25, 36, 'tema',   {'kick': 'x.......x.......'}),
)

#: LE AGGIUNTE, battuta per battuta (da 1). Si sommano allo strato.
#:
#: Il vocabolario e' quello che il batterista usa davvero: i levare (passi 6,
#: 10, 14) e i movimenti 3 e 4 (8, 12).
#:
#: ⚠️ DOVE vanno le ha decise la melodia, non un arco astratto. La batteria
#: RISPONDE dove il tema o l'assolo lasciano un buco, e TACE dove sono pieni.
#: Nella versione 14 era il contrario: le aggiunte piu' fitte stavano alle
#: battute 21-22, che sono le due in cui l'assolo fa dodici note. Era un muro.
#:
#: Densita' del tema, battuta per battuta:  4 3 1 2 4 3 1 0 4 4 3 2
#: Densita' dell'assolo (battute 13-24):    5 6 6 2 5 7 6 1 12 12 5 0
#:
#: ⚠️ Le battute 12 e 24 non compaiono: le sovrascrive il fill del turnaround.
AGGIUNTE = {
    # --- primo giro, il TEMA: si risponde dove il tema respira -------------
    3:  {'rullante': '..........x.....'},   # il tema ha UNA nota
    4:  {'rullante': '......x.........'},   # il tema entra solo alla fine
    7:  {'rullante': '..........x...x.'},   # una nota sola
    8:  {'rullante': '......x...x.....'},   # il tema TACE: e' il posto piu' libero
    11: {'rullante': '............x...'},

    # --- secondo giro, l'ASSOLO -------------------------------------------
    16: {'rullante': '......x.....x.x.'},   # assolo a 2 note: si risponde
    17: {'rullante': '..........x.....'},
    19: {'rullante': '............x...'},
    20: {'rullante': '..x...x...x...x.',    # assolo a 1 nota: la risposta piena
         'kick':     '..............x.'},
    # 21 e 22: l'assolo fa DODICI note. La batteria non aggiunge niente
    23: {'rullante': '..........x.x...'},

    # --- terzo giro, il TEMA di nuovo -------------------------------------
    27: {'rullante': '..........x.....'},
    28: {'rullante': '......x.........'},
    31: {'rullante': '..........x...x.'},
    32: {'rullante': '......x...x.....'},   # il tema tace
    35: {'rullante': '............x...'},
    36: {'rullante': 'x...............', 'kick': 'x...............'},
}


def _somma(*patterns: str) -> str:
    """Sovrappone piu' pattern: un passo suona se lo suona almeno uno."""
    return ''.join('x' if any(p[i] == 'x' for p in patterns) else '.'
                   for i in range(16))


def _strato(battuta: int) -> dict[str, str]:
    """Lo strato di quella battuta: il default, con le sostituzioni della
    sezione in cui cade."""
    fuori = dict(STRATI)
    for prima, ultima, _nome, sostituzioni in SEZIONI:
        if prima <= battuta <= ultima:
            fuori.update(sostituzioni)
    return fuori


def sezione(battuta: int) -> str:
    """Come si chiama la sezione in cui cade quella battuta."""
    for prima, ultima, nome, _ in SEZIONI:
        if prima <= battuta <= ultima:
            return nome
    return ''


def per_battuta(battute: int) -> list[dict[str, str]]:
    """Per ogni battuta, `{voce: pattern}`. Le voci sono quelle del profilo."""
    for b, voci in AGGIUNTE.items():
        if not 1 <= b <= battute:
            raise ValueError(f'aggiunta alla battuta {b}, fuori dal pezzo '
                             f'che ne ha {battute}')
        for voce in voci:
            if voce not in STRATI:
                raise ValueError(f'battuta {b}: voce {voce!r} sconosciuta, '
                                 f'ci sono {sorted(STRATI)}')
    for _, _, _nome, sostituzioni in SEZIONI:
        for voce in sostituzioni:
            if voce not in STRATI:
                raise ValueError(f'sezione: voce {voce!r} sconosciuta')

    fuori = []
    for b in range(1, battute + 1):
        extra = AGGIUNTE.get(b, {})
        fuori.append({voce: _somma(base, extra.get(voce, '.' * 16))
                      for voce, base in _strato(b).items()})
    return fuori


def racconta(battute: int = 36) -> str:
    """Una riga per battuta, per guardare la forma invece di immaginarla."""
    voci = ('ride', 'charleston a pedale', 'rullante', 'kick')
    righe = []
    for i, parte in enumerate(per_battuta(battute), 1):
        colpi = sum(parte[v].count('x') for v in voci)
        segno = f'  {sezione(i)}' + (' <-' if i in AGGIUNTE else '')
        righe.append(f'{i:3}  ' + '  '.join(f'{parte[v]:16}' for v in voci)
                     + f'  {colpi:2}{segno}')
    return '\n'.join(righe)


if __name__ == '__main__':
    print('  b  ride              hh-pedale         rullante          '
          'cassa             colpi')
    print(racconta())
    parti = per_battuta(36)
    tot = sum(p[v].count('x') for p in parti
              for v in ('ride', 'charleston a pedale', 'rullante', 'kick'))
    print(f'\n{tot} colpi in 36 battute = {tot / 36:.1f} per battuta')
    print(f'{len(AGGIUNTE)} battute su 36 hanno aggiunte sopra lo strato')
