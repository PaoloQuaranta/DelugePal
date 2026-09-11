"""La batteria del blues, COMPOSTA battuta per battuta.

⚠️ NON C'E' NESSUNA REGOLA APPLICATA UNIFORMEMENTE, ed e' il punto. Le tre
versioni precedenti erano generatori travestiti: uno strato costante piu' una
regola per le aggiunte, applicati a tutte e 36 le battute. Producevano
qualcosa di regolare, e il regolare suona male.

Il verdetto dell'11 settembre 2026, sulla versione 15: *«musicalmente le parti
di batteria meno peggio restano quelle di jazz 1-6»* -- cioe' quelle scritte a
mano. Guardate a confronto, la differenza non era la densita' (415 colpi
contro 447) ma il fatto che le loro sequenze NON HANNO UNA FORMULA: sono
irregolari come e' irregolare una persona che decide battuta per battuta.

E la ragione di fondo, detta dal proprietario:

    «usare statistiche su tutto il corpus non funziona, e anche l'analisi
    formale di una singola fonte non puo' funzionare per astrarre leggi
    compositive generalizzabili, che soprattutto nel jazz di fatto non
    esistono»

DA DOVE VIENE QUELLO CHE C'E' QUI DENTRO:

  - il VOCABOLARIO -- quali posizioni sono idiomatiche -- dal profilo di
    `drummer10/session1/1` e dalle parti di jazz 01-06;
  - i VINCOLI -- cosa non si fa -- da `docs/istruzioni/batteria-jazz.md`;
  - il TOCCO -- velocity e microtiming -- dal groove template, che si applica
    dopo;
  - la SEQUENZA -- quale figura in quale battuta -- da una decisione, una per
    battuta, col motivo scritto accanto.

I passi: 0 = movimento 1, 4 = movimento 2, 8 = movimento 3, 12 = movimento 4.
I dispari 2, 6, 10, 14 sono i levare, che il firmware swinga.
"""
from __future__ import annotations

#: Le due voci che NON variano, e sono costanti per decisione dichiarata.
#:
#: ⚠️ Il ride non si buca mai: `[LIB]` Riley p. 8, «ogni nota deve avere un
#: inizio definito ma nessuna fine, il suono deve scorrere nel successivo».
#: Una nota mancante e' un silenzio, e il tempo si spezza. I sei passi sono
#: `[MIS]`: i soli che il ride colpisce in piu' di meta' delle battute su 21
#: esecuzioni jazz del Groove MIDI.
COSTANTI = {
    'ride': 'x...x.x.x...x.x.',
    'charleston a pedale': '....x.......x...',
}

#: Il rullante e la cassa, battuta per battuta. Due colonne, sedici passi
#: ciascuna, e un motivo.
#:
#: ⚠️ LA CASSA STA SU 1 E 3, non su quattro movimenti: e' il feathering, e il
#: template gli da' 96 e 86 di velocity, cioe' colpi leggeri. Le bombe sono
#: i colpi in piu', sempre sui levare o sul 4.
#:
#: ⚠️ IL RULLANTE STA SUI LEVARE, e tace in nove battute su trentaquattro.
#: Nella versione 15 batteva il movimento 2 in tutte e 36, insieme al
#: charleston che batte lo stesso movimento: due voci sullo stesso colpo,
#: trentasei volte di fila. Era un metronomo.
#:
#: Le densita' della melodia, che sono il contesto di ogni decisione:
#:   tema (giri 1 e 3)   4 3 1 2 4 3 1 0 4 4 3 2
#:   assolo (giro 2)     5 6 6 2 5 7 6 1 12 12 5 0
#:
#: ⚠️ Le battute 12 e 24 le sovrascrive il fill del turnaround: qui sono
#: scritte come tempo, e non si sentiranno.
PARTE = '''
# --- primo giro: il TEMA. La batteria si siede e lascia entrare il pezzo. ---
#  b   rullante          cassa
   1   ................  x.......x.......   il tema entra, la batteria non commenta
   2   ..........x.....  x.......x.......   una prima risposta, piccola
   3   .......x..x.....  x.......x.......   il tema ha UNA nota: qui c'e' posto
   4   ..........x.....  x.............x.   la bomba sul levare spinge dentro la battuta 5
   5   ................  x.......x.......   il tema e' pieno: fuori dai piedi
   6   ............x...  x.......x.......   un segno solo, sul quattro
   7   .......x....x...  x.......x.......   una nota sola nel tema
   8   .......x..x...x.  x.....x.x.......   IL TEMA TACE: la battuta piu' libera del giro
   9   ................  x.......x.......   si rientra in silenzio
  10   ..........x.....  x.......x.......   il tema e' fitto, un colpo e basta
  11   ....x.......x...  x.......x.......   due e quattro: ci si prepara al turnaround
  12   ................  x.......x.......   (fill)

# --- secondo giro: l'ASSOLO. Qui la batteria diventa un interlocutore. ------
  13   ..........x.....  x.......x.......   l assolo parte, si accompagna e basta
  14   ................  x.......x.......   lo si lascia correre
  15   ..............x.  x.......x.......   una spinta sola, in fondo alla battuta
  16   .......x..x...x.  x...........x...   l assolo respira (due note): si risponde
  17   ..........x.....  x.......x.......   si torna indietro
  18   ................  x.......x.......   l assolo e' fitto: niente
  19   ............x...  x.......x.......   un segno per non sparire
  20   ....x.......x.x.  x.............x.   UNA NOTA nell assolo: la risposta piena
  21   ................  x.......x.......   DODICI note: la batteria esce di scena
  22   ................  x.......x.......   e ci resta
  23   ..........x...x.  x.......x.......   l assolo scende, si rientra
  24   ................  x.......x.......   (fill)

# --- terzo giro: il TEMA torna. Piu' assestata del primo giro, poi chiude. --
  25   ............x...  x.......x.......   piu' presente della battuta 1: siamo dentro
  26   ..........x.....  x.......x.......
  27   .......x..x.....  x.......x.......   una nota nel tema
  28   ..........x...x.  x.............x.   la bomba, come alla 4
  29   ................  x.......x.......
  30   ....x.......x...  x.......x.......   due e quattro, la meta' del giro
  31   .......x....x...  x.......x.......   una nota nel tema
  32   .......x..x...x.  x.....x.x.......   IL TEMA TACE di nuovo
  33   ................  x.......x.......
  34   ..........x.....  x.......x.......
  35   ............x...  x.......x.......   verso la chiusa
  36   x...............  x...............   un accento sul primo movimento, e via
'''


def leggi(testo: str = PARTE) -> list[dict[str, str]]:
    """Da testo a `[{voce: pattern}, ...]`, una voce per battuta.

    Le due voci costanti si aggiungono a ogni battuta. Il rullante compare
    solo dove parla: dove tace non c'e' la chiave, e il chiamante non scrive
    niente.
    """
    fuori = []
    for riga in testo.splitlines():
        riga = riga.split('#')[0].strip()
        if not riga:
            continue
        gettoni = riga.split()
        if len(gettoni) < 3:
            raise ValueError(f'riga {riga!r}: servono numero, rullante, cassa')
        numero, rullante, cassa = gettoni[0], gettoni[1], gettoni[2]
        if not numero.isdigit() or int(numero) != len(fuori) + 1:
            raise ValueError(f'battuta {numero}: attesa la '
                             f'{len(fuori) + 1}, le battute vanno in ordine')
        for nome, p in (('rullante', rullante), ('cassa', cassa)):
            if len(p) != 16 or set(p) - set('x.'):
                raise ValueError(f'battuta {numero}, {nome}: {p!r} non e un '
                                 f'pattern di sedici passi fatto di x e .')
        parte = dict(COSTANTI)
        if 'x' in rullante:
            parte['rullante'] = rullante
        if 'x' in cassa:
            parte['kick'] = cassa
        fuori.append(parte)
    return fuori


def per_battuta(battute: int) -> list[dict[str, str]]:
    """Come `leggi()`, ma controlla che il pezzo sia lungo quanto la parte."""
    parte = leggi()
    if len(parte) != battute:
        raise ValueError(f'la parte di batteria ha {len(parte)} battute, '
                         f'il pezzo ne vuole {battute}')
    return parte


def racconta() -> str:
    """Una riga per battuta, per guardare la forma invece di immaginarla."""
    voci = ('ride', 'charleston a pedale', 'rullante', 'kick')
    vuoto = '.' * 16
    righe = []
    for i, parte in enumerate(leggi(), 1):
        colpi = sum(parte.get(v, vuoto).count('x') for v in voci)
        righe.append(f'{i:3}  '
                     + '  '.join(f'{parte.get(v, vuoto):16}' for v in voci)
                     + f'  {colpi:2}')
    return '\n'.join(righe)


if __name__ == '__main__':
    parte = leggi()
    print('  b  ride              hh-pedale         rullante          '
          'cassa             colpi')
    print(racconta())
    voci = ('ride', 'charleston a pedale', 'rullante', 'kick')
    tot = sum(p.get(v, '.' * 16).count('x') for p in parte for v in voci)
    muti = sum(1 for p in parte if 'rullante' not in p)
    print(f'\n{len(parte)} battute, {tot} colpi = {tot / len(parte):.1f} per battuta')
    print(f'il rullante tace in {muti} battute')
    print('   (jazz 01-06, le parti preferite: 415 colpi, rullante muto in 11)')
