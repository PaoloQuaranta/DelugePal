"""La coppia controllata del cancello: GROOVE0 e GROOVE1.

Due song IDENTICHE tranne una cosa sola: la stessa clip di batteria, scritta
a mano con `MU.passi()`, con e senza il groove template di UNA esecuzione
nominata del Groove MIDI. Serve al Task 10 del piano groove-midi, cioe' alla
sola prova che puo' dire se il residuo di micro-tempistica esce da un Deluge
e se qualcuno lo sente.

    out/GROOVE0.XML   il pattern nudo          -> /SONGS/DelugePal/GROOVE0.XML
    out/GROOVE1.XML   lo stesso + il template  -> /SONGS/DelugePal/GROOVE1.XML

Tutto cio' che non e' il template dev'essere byte per byte lo stesso: se no
la differenza che si ascolta non e' attribuibile. Per questo le due song
escono dalla STESSA funzione, e alla fine lo script confronta i due file e
dichiara quali righe differiscono.

Da lanciare da D:\\DelugePal:

    .venv/Scripts/python.exe tools/genera_groove.py

⚠️ Vuole due cose non versionate: `refs/songs/TEMPL0.XML` (la song di
partenza) e il Groove MIDI Dataset in `to-read/`. Senza, si ferma dicendolo.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import parse_file, write_file                 # noqa: E402
from delugexml import song as S, create as C                 # noqa: E402
from delugexml import kit as K, musica as MU                 # noqa: E402
from delugexml import groove as GR                           # noqa: E402
from delugexml.writer import FormatTable                     # noqa: E402

RADICE = Path(__file__).resolve().parent.parent
BASE_GROOVE = RADICE / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
KIT = RADICE / 'refs' / 'kits' / 'CR78FROMMARS.XML'
TABELLA = RADICE / 'out' / 'format_table.json'

#: L'esecuzione che fa da template. E' la piu' lunga fra le `jazz/swing`,
#: `beat`, 4-4 del corpus -- il criterio del piano -- ed e' nominata perche'
#: un profilo e' [OSS] su un esecutore, mai [MIS] su un repertorio.
ESECUZIONE = 'drummer1/session3/2'

#: Il tempo della coppia. NON e' quello dell'esecuzione (185 BPM): il residuo
#: che il template scrive e' in TICK, e un tick vale 3,38 ms a 185 BPM contro
#: 6,25 ms a 100. A 100 BPM ogni spostamento che il template scrive vale
#: quasi il DOPPIO in millisecondi, e la finestra dell'udibile che il comune
#: dichiara (20-40 ms) e' in millisecondi. La licenza a trasporre e' la
#: regressione della casella 6: il divario ride/charleston e' indistinguibile
#: da costante-in-tick (0,8 sigma) -- ma vale per una coppia su tre, quindi e'
#: una scelta dichiarata e non un risultato. 100 BPM e' anche un tempo di
#: swing medio-lento perfettamente idiomatico.
BPM = 100

#: Lo swing lo fa la SONG, non il template: `figura='1/8'` perche' il default
#: del firmware swinga le semicrome e su una linea di crome non muove niente.
#: Il 62 viene dal BUR di Weimar (casella 10 del jazz) e NON e' mai uscito da
#: un Deluge: e' aritmetica sul meccanismo, non una misura sul dispositivo.
SWING = 62

#: Due battute, cosi' cassa e rullante possono dire due cose diverse e
#: l'orecchio ha il tempo di sentire il giro.
BATTUTE = 2
LUNGHEZZA = BATTUTE * MU.TICK_PER_BATTUTA

#: Le quattro voci, e la scelta e' la parte che conta.
#:
#: `voce` e' il nome nel PROFILO (mappa GM), `drum` e' il nome nel kit.
#: `velocity` e' la velocity piatta di GROOVE0: NON e' inventata, e' la
#: mediana aggregata di quello strumento nel jazz misurata su 50 esecuzioni
#: (casella 6, «La scala di velocity»). Sceglierla cosi' invece di lasciare
#: il default 90 di `passi()` riduce di proposito il divario di DINAMICA fra
#: le due song, perche' la domanda del cancello e' se si sente il RESIDUO di
#: posizione -- e una differenza di velocity grossa lo coprirebbe.
#:
#: ⚠️ `tom basso` e non `ride`: su questa esecuzione il disegno continuo di
#: crome swingate sta sulla nota GM 43 (805 colpi) per otto decimi, e sulla
#: 51 -- che la mappa chiama `ride` -- solo nel quinto centrale (238 colpi).
#: La voce si sceglie dai colpi e dalla posizione, mai dal nome.
VOCI = (
    # voce del profilo,      drum del kit,     velocity GROOVE0, pattern
    ('tom basso',            'CH CR78 03',     64,
     'x.x.x.x.x.x.x.x.'      # crome continue: il disegno di ride
     'x.x.x.x.x.x.x.x.'),
    ('charleston a pedale',  'OH CR78 03',     70,
     '....x.......x...'      # il piede sul 2 e sul 4
     '....x.......x...'),
    ('kick',                 'Kick CR78 12',   59,
     'x.x.....x.......'      # 1 e 3, con la bomba sul levare dell 1
     'x.....x.x.......'),    # e sul levare del 2 nella seconda battuta
    ('rullante',             'Snare CR78 13',  47,
     '......x.....x...'      # comping
     '..x.......x...x.'),
)

#: I drum del kit che restano. Gli altri si tolgono: quattro righe stanno
#: tutte in una schermata (ne entrano otto) e chi deve GUARDARE le posizioni
#: sul dispositivo non deve scrollare per farlo.
TENUTI = tuple(d for _, d, _, _ in VOCI)


def costruisci(prof, *, con_groove: bool):
    """La song. L'UNICA differenza fra le due e' `con_groove`."""
    doc = parse_file(TEMPL)
    S.set_bpm(doc.root, BPM)
    S.set_swing(doc, SWING, figura='1/8')

    # la song di partenza porta un synth: qui serve la sola batteria
    for strumento in list(S.instruments(doc)):
        MU.togli(doc, strumento)

    kit, clip = C.add_track(doc, KIT, name='CR78FROMMARS', folder='KITS',
                            length=LUNGHEZZA, playing=True)
    for nome in [d.get('name') for d in S.drums(kit)]:
        if nome not in TENUTI:
            K.remove_drum(doc, kit, nome)

    rapporti = []
    for voce, drum, velocity, pattern in VOCI:
        note = MU.passi(pattern, velocity=velocity)
        if con_groove:
            rapporti.append(MU.applica_groove(note, prof, dove=voce))
        rapporti.append(MU.scrivi(doc, clip, note, dove=drum))
    rapporti.append(S.fit_clip_scroll_to_notes(doc, clip))
    return doc, clip, rapporti


def scrivi_song(doc, nome: str) -> tuple[Path, str]:
    """Il percorso remoto lo costruisce `destinazione()`, e da quello viene
    il nome locale: nessun percorso scritto a mano (regola 5).

    ⚠️ `destinazione('groove', 0)` -- come lo scriveva il capitolato -- e'
    RIFIUTATO: la versione va da 1 a 99 e compare sempre a due cifre, quindi
    darebbe comunque GROOVE00. Lo zero e l'uno qui sono l'etichetta della
    coppia, non un numero di versione, e vanno nel nome.
    """
    remoto = MU.destinazione(nome, None)
    locale = RADICE / 'out' / Path(remoto).name
    write_file(doc, locale, FormatTable.load(TABELLA))
    return locale, remoto


def main() -> int:
    for percorso, cosa in ((TEMPL, 'la song di partenza'),
                           (KIT, 'il kit'),
                           (BASE_GROOVE, 'il Groove MIDI Dataset')):
        if not percorso.exists():
            print(f'manca {cosa}: {percorso}', file=sys.stderr)
            return 2

    prof = GR.profilo(BASE_GROOVE, ESECUZIONE)
    print(f'template: {GR.racconta(BASE_GROOVE, ESECUZIONE)}')
    print(f'          BUR {prof.bur:.3f}, {prof.battute} battute, '
          f'{len(prof.passi)} voci')
    tick_ms = 60000 / (BPM * 96)
    print(f'coppia a {BPM} BPM: un tick vale {tick_ms:.2f} ms '
          f'(a {prof.bpm} BPM ne varrebbe {60000 / (prof.bpm * 96):.2f})')
    print()

    scritti = []
    for nome, con_groove in (('groove0', False), ('groove1', True)):
        doc, clip, rapporti = costruisci(prof, con_groove=con_groove)

        problemi = MU.verifica(doc)
        if problemi:
            print(f'{nome}: il cancello e chiuso, NON si carica: '
                  + '; '.join(problemi), file=sys.stderr)
            return 1
        avvisi = MU.avvertenze(doc)

        locale, remoto = scrivi_song(doc, nome)
        scritti.append(locale)

        print('=' * 70)
        print(f'{locale.name}  ->  {remoto}')
        print('=' * 70)
        for r in rapporti:
            if r:
                print('  ', r)
        for a in avvisi:
            print('   avvertenza:', a)
        print()
        print(MU.racconta(doc))
        print()

    confronta(*scritti)
    return 0


def confronta(a: Path, b: Path) -> None:
    """Il controllo che rende la coppia una coppia: cosa e' cambiato davvero.

    Le note del Deluge stanno in blob esadecimali dentro `<noteRow>`, quindi
    una riga diversa fuori da li' vorrebbe dire che le due song differiscono
    per qualcosa che NON e' il template -- e la differenza che si ascolta non
    sarebbe piu' attribuibile.
    """
    prima = a.read_text('utf-8', 'surrogateescape').splitlines()
    dopo = b.read_text('utf-8', 'surrogateescape').splitlines()
    diverse = [(i, x, y) for i, (x, y) in enumerate(zip(prima, dopo), 1)
               if x != y]
    print('=' * 70)
    print(f'confronto {a.name} / {b.name}')
    print('=' * 70)
    if len(prima) != len(dopo):
        print(f'  ⚠ righe diverse in numero: {len(prima)} contro {len(dopo)}')
    fuori = [r for r in diverse
             if 'noteData' not in r[1] and 'noteData' not in r[2]]
    print(f'  righe totali: {len(prima)}')
    print(f'  righe diverse: {len(diverse)}, di cui su noteData: '
          f'{len(diverse) - len(fuori)}')
    if fuori:
        print('  ⚠ DIFFERENZE FUORI DALLE NOTE -- la coppia non e controllata:')
        for i, x, y in fuori[:20]:
            print(f'    r{i} - {x.strip()[:100]}')
            print(f'    r{i} + {y.strip()[:100]}')
    else:
        print('  nessuna differenza fuori dalle note: la coppia e controllata')


if __name__ == '__main__':
    raise SystemExit(main())
