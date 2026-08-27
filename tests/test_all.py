"""Suite di regressione. Eseguire con:  python tests/test_all.py

Non usa pytest per non aggiungere dipendenze. Ogni test stampa PASS/FAIL e
alla fine viene restituito un exit code diverso da zero se qualcosa e' rotto.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))

from delugexml import parse, parse_file, serialize, Note   # noqa: E402
from delugexml import notes as N                           # noqa: E402
from delugexml import song as S                            # noqa: E402
from delugexml.writer import FormatTable                   # noqa: E402

REFS = ROOT / 'refs'
TABLE_PATH = ROOT / 'out' / 'format_table.json'

results = []
skipped = []


def check(name, cond, detail=''):
    results.append((name, bool(cond), detail))
    print(f'{"PASS" if cond else "FAIL"}  {name}' + (f'  — {detail}' if detail else ''))


def salta(name, detail=''):
    """Il test non puo' girare: manca materiale che NON appartiene al repo.

    Non e' un fallimento. Il corpus da cui questo progetto impara la tabella
    di formato e' quello di chi lo usa: le song dell'autore non sono
    pubblicate, e i preset di terzi nemmeno. Vedi README, "Bring your own
    corpus".
    """
    skipped.append((name, detail))
    print(f'SKIP  {name}' + (f'  — {detail}' if detail else ''))


# ------------------------------------------------------- parser: tolleranza

def test_unescaped_amp():
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<song>\n\t<sound name="R&b3" />\n</song>\n')
    s = doc.root.find('sound')
    check('& non escapato viene letto alla lettera',
          s.get('name') == 'R&b3', repr(s.get('name')))
    check('& non escapato viene segnalato',
          any(p.kind == 'unescaped_amp' for p in doc.problems))


def test_duplicate_attrs():
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<song>\n\t<audioClip length="12" length="12" />\n</song>\n')
    c = doc.root.find('audioClip')
    check('attributi duplicati conservati',
          c.get_all('length') == ['12', '12'], str(c.get_all('length')))
    check('attributi duplicati segnalati',
          any(p.kind == 'duplicate_attr' for p in doc.problems))
    c.set('length', '24')
    check('set() collassa i duplicati', c.get_all('length') == ['24'])


def test_multi_root():
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<firmwareVersion>1.3.0</firmwareVersion>\n<song>\n</song>\n')
    check('formato legacy: due elementi radice', len(doc.roots) == 2)
    check('root() sceglie <song>', doc.root.tag == 'song')


# ---------------------------------------------------------------- roundtrip

def test_roundtrip():
    files = [p for p in sorted(REFS.rglob('*.XML')) if not p.name.startswith('._')]
    if not files:
        check('corpus di riferimento presente', False, f'niente in {REFS}')
        return
    docs = [(p, parse_file(p)) for p in files]
    table = FormatTable().learn(d for _, d in docs)

    bad = [p.name for p, d in docs if serialize(d, table) != d.raw]
    check(f'round-trip chirurgico byte-esatto ({len(docs)} file)',
          not bad, ', '.join(bad[:4]))

    # Il rebuild completo ricostruisce ogni nodo dalle regole di formato
    # apprese. Un file solo non ci riesce, e il perche' e' documentato in
    # FINDINGS §2.2-bis: il modello `inline_prefix` sa esprimere "N attributi
    # sulla riga del tag, il resto uno per riga", mentre quel nodo ne ha ZERO
    # sulla riga del tag e poi tutti e tre INSIEME su quella dopo. Non e' una
    # forma che il modello puo' rappresentare.
    #
    # Non viene ignorato: `test_rebuild_differisce_solo_negli_spazi` controlla
    # che la differenza resti di soli spazi. Se un giorno diventasse altro, o
    # se un secondo file cadesse qui, questi due test lo dicono.
    # l'unico file che non si ricostruisce byte-esatto; se non e' stato
    # pubblicato (contiene un preset di terzi) l'insieme si svuota da se'
    NOTO = {'TRASF401MIDI.XML'} & {p.name for p, _ in docs}
    bad = [p.name for p, d in docs
           if serialize(d, table, rebuild=True) != d.raw]
    check(f'rebuild completo byte-esatto ({len(docs)} file, {len(NOTO)} noto)',
          set(bad) == NOTO, f'inattesi: {sorted(set(bad) - NOTO)}')


def test_rebuild_differisce_solo_negli_spazi():
    """L'unico file che non si ricostruisce byte-esatto differisce SOLO nella
    disposizione degli attributi, non nel contenuto.

    E' il limite del modello di formato, non un dato sbagliato: il Deluge
    legge XML e non conta gli spazi, e il round-trip CHIRURGICO -- quello che
    si usa davvero, che ricopia i byte dei nodi non toccati -- e' byte-esatto
    anche su questo file.
    """
    p = REFS / 'songs' / 'TRASF401MIDI.XML'
    docs = [parse_file(q) for q in sorted(REFS.rglob('*.XML'))
            if not q.name.startswith('._')]
    table = FormatTable().learn(docs)
    doc = parse_file(p)
    rebuilt = serialize(doc, table, rebuild=True)

    check('il rebuild differisce davvero', rebuilt != doc.raw)
    check('ma solo negli spazi bianchi',
          ''.join(rebuilt.split()) == ''.join(doc.raw.split()))
    check('e il round-trip chirurgico resta byte-esatto',
          serialize(doc, table) == doc.raw)


def test_surgical_isolation():
    """Cambiare un valore deve toccare solo quella riga."""
    p = REFS / 'songs' / 'Mark.XML'
    if not p.exists():
        salta('isolamento della modifica', 'Mark.XML assente')
        return
    doc = parse_file(p)
    table = FormatTable.load(TABLE_PATH) if TABLE_PATH.exists() else FormatTable()
    S.set_bpm(doc.root, 100)
    after = serialize(doc, table)
    a, b = doc.raw.splitlines(), after.splitlines()
    diff = sum(1 for x, y in zip(a, b) if x != y)
    check('cambiare il tempo tocca esattamente 2 righe',
          diff == 2 and len(a) == len(b), f'{diff} righe, {len(a)}->{len(b)}')


# -------------------------------------------------------------------- tempo

def test_tempo_roundtrip():
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<song timePerTimerTick="626" timerTickFraction="1805838522" '
                'inputTickMagnitude="1"></song>\n')
    check('BPM noto: 626 + frac, mag 1 -> 88',
          abs(S.get_bpm(doc.root) - 88.0) < 1e-6, f'{S.get_bpm(doc.root)}')
    for bpm in (60, 88, 100, 120.5, 174, 27):
        S.set_bpm(doc.root, bpm)
        got = S.get_bpm(doc.root)
        if abs(got - bpm) > 1e-4:
            check(f'set_bpm({bpm}) e rileggi', False, f'letto {got}')
            return
    check('set_bpm/get_bpm coerenti su 6 valori', True)


def test_ticks_per_beat():
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<song inputTickMagnitude="2"></song>\n')
    check('mag 2 -> 96 tick per movimento',
          S.ticks_per_beat(doc.root) == 96, str(S.ticks_per_beat(doc.root)))
    # il caso confermato sul dispositivo: pos 144 = quarto ottavo di Perche.XML
    eighth = S.ticks_per_beat(doc.root) // 2
    check('pos 144 = quarto ottavo (Perche, verificato sul Deluge)',
          144 == eighth * 3, f'ottavo = {eighth} tick')
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<song inputTickMagnitude="1"></song>\n')
    check('mag 1 -> 48 tick per movimento',
          S.ticks_per_beat(doc.root) == 48, str(S.ticks_per_beat(doc.root)))


def test_tempo_negative_fraction():
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<song timePerTimerTick="401" timerTickFraction="-238609295" '
                'inputTickMagnitude="2"></song>\n')
    spt = S.samples_per_tick(doc.root)
    check('frazione negativa letta come uint32',
          abs(spt - 401.944444) < 1e-5, f'{spt}')


# -------------------------------------------------------------------- note

def test_notes_roundtrip():
    blob = '0x000001B000000030644014'
    ns = N.decode(blob, 11)
    check('decodifica: 1 nota da 11 byte', len(ns) == 1, str(ns))
    n = ns[0]
    check('campi della nota',
          (n.pos, n.length, n.velocity, n.lift, n.condition) == (432, 48, 100, 64, 20),
          str(n))
    check('ricodifica identica', N.encode(ns, 11) == blob, N.encode(ns, 11))


def test_notes_extra_preserved():
    blob = '0x000001B000000030644014000000'
    ns = N.decode(blob, 14)
    check('WithSplitProb: byte extra conservati',
          N.encode(ns, 14) == blob, N.encode(ns, 14))


def test_iterance():
    # nota con iterance "4 di 4": divisore 4, maschera 0b1000 = 8
    blob = '0x000001B000000030644014040800'
    n = N.decode(blob, 14)[0]
    check('divisore e maschera dell iterance decodificati',
          (n.iterance_divisor, n.iterance_steps) == (4, 8),
          f'{n.iterance_divisor}, {n.iterance_steps}')
    check('iterance nella notazione del dispositivo',
          n.iterance == '4of4', str(n.iterance))
    check('ricodifica identica con iterance', N.encode([n], 14) == blob,
          N.encode([n], 14))

    n2 = N.decode('0x000001B000000030644014080100', 14)[0]
    check('8 di 8 e 1 di 8 si distinguono', n2.iterance == '1of8', str(n2.iterance))

    plain = N.decode('0x000001B000000030644014000000', 14)[0]
    check('senza iterance la proprieta e None', plain.iterance is None)

    # una nota da 11 byte non ha i campi di iterance, ma deve poter essere
    # riscritta in formato 14 senza inventare valori
    short = N.decode('0x000001B000000030644014', 11)[0]
    check('nota da 11 byte: iterance a zero',
          (short.iterance_divisor, short.iterance_steps, short.fill) == (0, 0, 0))
    check('promozione a 14 byte senza inventare',
          N.encode([short], 14) == '0x000001B000000030644014000000',
          N.encode([short], 14))


def test_notes_sorted():
    ns = [Note(pos=100, length=10), Note(pos=0, length=10)]
    out = N.decode(N.encode(ns, 11), 11)
    check('le note vengono riordinate per posizione',
          [n.pos for n in out] == [0, 100], str([n.pos for n in out]))


def test_duplicate_clip():
    p = REFS / 'songs' / 'Perche.XML'
    if not p.exists():
        salta('duplicazione di una clip', 'Perche.XML assente')
        return
    doc = parse_file(p)
    before = S.clips(doc)
    n_before = len(before)
    src_notes = sum(len(S.read_notes(r)) for r in S.note_rows(before[1][1]))

    dup = S.duplicate_clip(doc, 1, name='COPIA', section='2')
    after = S.clips(doc)
    check('la copia si aggiunge in fondo', len(after) == n_before + 1,
          f'{n_before} -> {len(after)}')
    check('la copia punta allo stesso strumento',
          dup.get('instrumentPresetName') ==
          before[1][1].get('instrumentPresetName'))
    check('i flag esclusivi sono azzerati nella copia',
          all(dup.get(f) in (None, '0') for f in S.EXCLUSIVE_FLAGS),
          str([(f, dup.get(f)) for f in S.EXCLUSIVE_FLAGS]))
    check('sezione e nome applicati',
          dup.get('section') == '2' and dup.get('clipName') == 'COPIA')
    check('la copia porta le stesse note dell originale',
          sum(len(S.read_notes(r)) for r in S.note_rows(dup)) == src_notes,
          f'{src_notes} attese')
    check('la clip originale non e stata toccata',
          not before[1][1].dirty and before[1][1].get('clipName') == '')

    # il documento modificato deve restare leggibile e riscrivibile
    table = FormatTable.load(TABLE_PATH) if TABLE_PATH.exists() else FormatTable()
    out = serialize(doc, table)
    doc2 = parse(out)
    check('il file con la copia si rilegge',
          len(S.clips(doc2)) == n_before + 1)
    check('nessuna anomalia introdotta',
          len(doc2.problems) == len(parse_file(p).problems),
          f'{len(doc2.problems)} contro {len(parse_file(p).problems)}')
    # La riscrittura chirurgica ricopia i nodi puliti byte per byte. Dalla
    # correzione dello scroll l'intestazione <song> non e' piu' fra questi:
    # duplicate_clip vi aggiorna yScrollSongView, un byte (test_scroll_song_view).
    cut = doc.raw.index('<sessionClips>')
    check('il corpo non toccato e conservato byte per byte',
          doc.raw[cut:cut + 17000] in out, '17000 byte dal primo sessionClips')
    check('nell intestazione cambia solo lo scroll',
          doc.raw[:cut].replace('yScrollSongView="-5"',
                                'yScrollSongView="-4"') in out)


def test_scroll_song_view():
    """La clip accodata deve restare dentro le 8 righe di song view.

    Verificato sul dispositivo: due file diversi per il solo yScrollSongView,
    -5 mostra 3 righe su 4, -4 le mostra tutte. Vedi docs/TEST_yscroll.md.
    """
    p = REFS / 'songs' / 'Perche.XML'
    if not p.exists():
        salta('scroll di song view', 'Perche.XML assente')
        return

    doc = parse_file(p)
    n_before = len(S.clips(doc))
    y_before = int(doc.root.get('yScrollSongView'))
    check('la sorgente ha le clip in fondo allo schermo',
          n_before - 1 - y_before == S.SONG_VIEW_ROWS - 1,
          f'{n_before} clip, yScroll {y_before}')

    S.duplicate_clip(doc, 1, section='2')
    y_after = int(doc.root.get('yScrollSongView'))
    last_row = len(S.clips(doc)) - 1 - y_after
    check('accodando una clip lo scroll la segue',
          y_after == y_before + 1, f'{y_before} -> {y_after}')
    check('la clip nuova cade dentro lo schermo',
          0 <= last_row <= S.SONG_VIEW_ROWS - 1, f'riga {last_row}')

    # una vista che gia' mostra la riga non va spostata: e' lo stato che
    # l'utente ha lasciato, e muoverlo sarebbe una modifica non richiesta
    doc2 = parse_file(p)
    doc2.root.set('yScrollSongView', '0')
    check('una vista che gia mostra la riga resta ferma',
          S.scroll_song_view_to(doc2, 3) is None
          and doc2.root.get('yScrollSongView') == '0',
          doc2.root.get('yScrollSongView'))

    # song che non dichiarano lo scroll: nessun attributo inventato
    doc3 = parse('<?xml version="1.0" encoding="UTF-8"?>\n<song>\n</song>\n')
    check('senza yScrollSongView non si inventa nulla',
          S.scroll_song_view_to(doc3, 9) is None
          and not doc3.root.has('yScrollSongView'))


def test_param_scale():
    """La scala 0-50 dei parametri, in aritmetica intera esatta.

    I valori attesi non sono inventati: sono presi da `Perche.XML` e verificati
    contro la costante 2^32 // 50 = 85899345.
    """
    from delugexml import params as P                  # noqa: PLC0415

    check('la costante e 2^32 // 50', P.STEP == 85899345, str(P.STEP))

    noti = {'0x80000000': 0, '0x00000000': 25, '0x7FFFFFFF': 50,
            '0xE6666654': 20, '0xCCCCCCBF': 15, '0x1999997E': 30,
            '0x4CCCCCA8': 40, '0x6666663D': 45}
    for h, atteso in noti.items():
        check(f'{h} vale {atteso}', P.to_display(h) == atteso,
              f'letto {P.to_display(h)}')

    # andata e ritorno: da display a esadecimale e viceversa
    giro = [v for v in range(0, 51) if P.to_display(P.from_display(v)) != v]
    check('andata e ritorno su tutti i 51 valori', not giro, f'rotti: {giro}')

    check('i valori speciali vengono riprodotti alla lettera',
          (P.from_display(0), P.from_display(25), P.from_display(50))
          == ('0x80000000', '0x00000000', '0x7FFFFFFF'))

    # LA PROVA SUL DISPOSITIVO: volume di un synth portato a 35 sullo schermo,
    # salvato dal Deluge, riletto via USB. Il firmware ha scritto 0x34000000 —
    # cioe' l'interno 90, non i 35 gradini della griglia storica.
    check('scrivendo 35 si ottiene quello che scrive il Deluge',
          P.from_display(35) == '0x34000000', P.from_display(35))
    check('e rileggendolo torna 35', P.to_display('0x34000000') == 35,
          str(P.to_display('0x34000000')))
    check('il valore interno e 90 su 128', P.internal_of('0x34000000') == 90,
          str(P.internal_of('0x34000000')))
    check('la griglia storica resta leggibile',
          P.to_display('0x4CCCCCA8') == 40)

    # PATCH CABLE, misurati sul dispositivo: lfo1 -> modulator1Volume a 30.
    # Il range mostrato e' bipolare -50..+50, quindi il fondoscala e' 2^30.
    check('un cable a 30 vale 0x26666666',
          P.cable_from_display(30) == '0x26666666', P.cable_from_display(30))
    # il valore memorizzato e' l'arrotondamento di 0.3 * 2^31, quindi rileggerlo
    # da 29.99999998 e non 30 esatto: confrontare float per uguaglianza sarebbe
    # sbagliato. Cio' che deve valere e' che si mostri come 30 e che il giro
    # completo torni allo stesso byte.
    letto = P.cable_to_display('0x26666666')
    check('e si rilegge come 30', round(letto, 4) == 30.0, str(letto))
    check('il giro completo del cable e byte-esatto',
          P.cable_from_display(letto) == '0x26666666',
          P.cable_from_display(letto))
    check('il fondoscala +50 e 0x40000000',
          P.cable_from_display(50) == '0x40000000', P.cable_from_display(50))
    check('il fondoscala -50 e 0xC0000000',
          P.cable_from_display(-50) == '0xC0000000', P.cable_from_display(-50))
    check('le modulazioni negative si leggono',
          P.cable_to_display('0xC0000000') == -50.0,
          str(P.cable_to_display('0xC0000000')))
    check('oltre il fondoscala si rifiuta',
          _raises(lambda: P.cable_from_display(51), ValueError))
    check('un valore oltre 2^30 non e un cable',
          P.cable_to_display('0x7FFFFFFF') is None)

    # fuori scala: si rifiuta invece di inventare
    check('un valore fuori griglia non viene indovinato',
          P.to_display('0x0CCCCCCC') is None, str(P.to_display('0x0CCCCCCC')))
    check('spazzatura in ingresso da None',
          P.to_display('non-esadecimale') is None)
    check('fuori dalla scala 0-50 e un errore',
          _raises(lambda: P.from_display(51), ValueError))

    # Su un file vero conta DOVE cade il confine, non una percentuale: i soli
    # parametri illeggibili devono essere quelli documentati come fuori scala.
    # Se domani ne comparisse un altro, questo test lo scopre.
    p = REFS / 'songs' / 'Perche.XML'
    if p.exists():
        doc = parse_file(p)
        fuori = set()
        letti = tot = 0
        for node in doc.root.iter():
            for k, v in node.attrs:
                if isinstance(v, str) and v.startswith('0x') and len(v) == 10:
                    tot += 1
                    if P.to_display(v) is None:
                        fuori.add(k)
                    else:
                        letti += 1
        check('il grosso dei parametri si legge',
              letti / tot > 0.85, f'{letti}/{tot} = {100*letti/tot:.1f}%')

        # Le griglie sono DUE, quindi from_display(to_display(h)) == h non puo
        # valere: un valore della griglia storica, riletto e riscritto, esce
        # su quella interna. Non e' un difetto, e' la conversione che il
        # dispositivo stesso fa quando tocchi la manopola.
        #
        # Cio' che deve valere e' che la piena risoluzione sia conservata da
        # chi la maneggia per quello che e': internal_of / from_internal.
        bugie, interni = [], 0
        fuori_scala = []
        for node in doc.root.iter():
            for k, v in node.attrs:
                if not (isinstance(v, str) and v.startswith('0x')
                        and len(v) == 10):
                    continue
                d = P.to_display(v)
                if d is not None and not 0 <= d <= 50:
                    fuori_scala.append((k, v, d))
                i = P.internal_of(v)
                if i is not None:
                    interni += 1
                    if P.from_internal(i).lower() != v.lower():
                        bugie.append((k, v, i, P.from_internal(i)))
        check('sulla griglia interna la riscrittura e byte-esatta',
              not bugie and interni > 0,
              f'{interni} valori, {len(bugie)} bugie {bugie[:2]}')
        check('to_display non esce mai dalla scala 0-50',
              not fuori_scala, str(fuori_scala[:2]))


def test_kit_add_remove_drum():
    """Aggiungere e togliere drum mantenendo l'invariante drumIndex.

    `drumIndex` e' una POSIZIONE, non un identificatore: togliere un drum
    rinumera tutto cio' che segue, in ogni clip che usa quel kit. Senza
    rinumerare, le note finirebbero sul drum sbagliato senza alcun segnale.
    """
    from delugexml import kit as K                       # noqa: PLC0415
    from delugexml import sound as SND                   # noqa: PLC0415

    song_p = REFS / 'songs' / 'TEMPL4.XML'
    kit_p = REFS / 'kits' / 'CR78FROMMARS.XML'
    if not (song_p.exists() and kit_p.exists()):
        salta('kit', 'TEMPL4/CR78FROMMARS assenti')
        return

    doc = parse_file(song_p)
    kclip = [c for _, c in S.clips(doc)][0]
    kit = S.instrument_of(doc, kclip)
    n0 = len(S.drums(kit))

    check('un drum ha una noteRow, indici contigui',
          not K.check_indices(doc, kit) and n0 == len(S.note_rows(kclip)),
          f'{n0} drum, {len(S.note_rows(kclip))} righe')

    # un drum preso da un ALTRO file: va staccato dagli span di quello
    altro = parse_file(kit_p)
    bongo = K.copy_drum(altro.root, 'Bongo Hi CR78')
    check('il drum copiato porta con se il campione',
          (K.sample_of(bongo) or '').endswith('.wav'), str(K.sample_of(bongo)))
    check('ed e staccato dal documento di provenienza', bongo.span is None)

    i = K.add_drum(doc, kit, bongo, name='BONGOHI')
    check('aggiunto in fondo', i == n0 and len(S.drums(kit)) == n0 + 1)
    check('con la sua noteRow', len(S.note_rows(kclip)) == n0 + 1)
    check('e l invariante regge', not K.check_indices(doc, kit),
          str(K.check_indices(doc, kit)))
    check('si trova per nome', S.drum_index(doc, kclip, 'bongohi') == i)

    riga = S.note_row(kclip, i)
    check('la riga nuova ha i suoi parametri, come quelle del dispositivo',
          SND.container(riga) is not None
          and SND.get(riga, 'volume') is not None,
          str(SND.container(riga)))

    S.write_notes(riga, [Note(pos=p, length=24, velocity=90)
                         for p in (72, 168)], create=True)
    posizioni = [n.pos for n in S.read_notes(riga)]

    # la rimozione deve rinumerare, e le note devono seguire il drum
    K.remove_drum(doc, kit, 'SNARE')
    check('togliendo un drum il conto scende', len(S.drums(kit)) == n0)
    check('l invariante regge anche dopo', not K.check_indices(doc, kit),
          str(K.check_indices(doc, kit)))
    nuovo = S.drum_index(doc, kclip, 'BONGOHI')
    check('il drum e stato rinumerato', nuovo == i - 1, f'{i} -> {nuovo}')
    check('e le sue note lo hanno seguito',
          [n.pos for n in S.read_notes(S.note_row(kclip, nuovo))] == posizioni)
    check('lo snare non c e piu',
          _raises(lambda: S.drum_index(doc, kclip, 'SNARE'), ValueError))

    table = FormatTable.load(TABLE_PATH) if TABLE_PATH.exists() else FormatTable()
    riletto = parse(serialize(doc, table))
    check('il documento resta sano', not riletto.problems,
          f'{[x.kind for x in riletto.problems][:3]}')


def test_key_mode_notes():
    """Note fuori scala e finestra verticale della clip.

    Storia di un errore, tenuta come test perche' non si ripeta: avevo
    concluso che le note fuori scala in key mode non hanno una riga e non
    suonano. **Falso.** Il dispositivo adatta la scala, e nel corpus 7 song
    hanno note fuori scala — `Progsong.XML` ne ha 315 — con `userScale="0"`,
    esattamente la combinazione che credevo rotta.

    Cio' che resta vero, ed e' un difetto nostro: una clip creata da un
    modello eredita `yScroll` e `inKeyScrollOffset` dal modello, cioe' da
    un'altra clip con altre altezze.
    """
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n<song\n'
                '\trootNote="2">\n'
                '\t<modeNotes>\n'
                '\t\t<modeNote>0</modeNote>\n\t\t<modeNote>2</modeNote>\n'
                '\t\t<modeNote>4</modeNote>\n\t\t<modeNote>5</modeNote>\n'
                '\t\t<modeNote>7</modeNote>\n\t\t<modeNote>9</modeNote>\n'
                '\t\t<modeNote>11</modeNote>\n'
                '\t</modeNotes>\n'
                '\t<sessionClips>\n'
                '\t\t<instrumentClip inKeyMode="1" yScroll="37" length="384">\n'
                '\t\t\t<noteRows>\n'
                '\t\t\t\t<noteRow y="36" />\n'
                '\t\t\t\t<noteRow y="43" />\n'
                '\t\t\t</noteRows>\n'
                '\t\t</instrumentClip>\n'
                '\t</sessionClips>\n</song>\n')
    clip = S.clips(doc)[0][1]
    for y, pos in ((36, 0), (43, 192)):
        S.write_notes(S.note_row(clip, y), [Note(pos=pos, length=48)],
                      create=True)

    check('la scala di prova e D maggiore', S.scale_name(doc) == 'D maggiore')
    check('y=43 e in scala, y=36 no',
          S.in_scale(doc.root, 43) and not S.in_scale(doc.root, 36))

    fuori = S.notes_out_of_scale(doc, clip)
    check('le note fuori scala si sanno elencare',
          fuori == [(36, 1, 35)], str(fuori))
    check('ma NON sono un errore: song reali ne contengono',
          True, 'Progsong.XML ne ha 315 con userScale=0')

    # il difetto vero: la finestra verticale ereditata da un altro contesto
    check('lo scroll di partenza non c entra con le note',
          clip.get('yScroll') == '37' and min(36, 43) == 36)
    prima_iks = clip.get('inKeyScrollOffset')
    cambiati = S.fit_clip_scroll_to_notes(doc, clip)
    # la clip di TEMPL0 e' in modalita' a scala, quindi la riga e' un GRADO:
    # non l'altezza 36 ma il suo grado. Vedi test_in_key_mode_yscroll_conta_i_gradi
    atteso = str(S.scale_degree(doc, 36))
    check('fit_clip_scroll_to_notes porta yScroll sulla RIGA della nota piu bassa',
          clip.get('yScroll') == atteso,
          f'{clip.get("yScroll")}, atteso {atteso} per l altezza 36')
    check('e non tocca inKeyScrollOffset, che non governa la clip view',
          'inKeyScrollOffset' not in cambiati
          and clip.get('inKeyScrollOffset') == prima_iks, str(cambiati))

    # portare le altezze in scala resta possibile, come SCELTA
    S.note_row(clip, 36).set('y', str(S.snap_to_scale(doc.root, 36)))
    check('snap_to_scale toglie le note fuori scala, se lo si vuole',
          not S.notes_out_of_scale(doc, clip))

    # le clip di kit non hanno altezze: niente da elencare come fuori scala.
    # Una finestra pero' ce l'hanno -- vedi test_fit_scroll_copre_anche_le_clip_di_kit
    # -- ma qui il drum che suona e' lo 0, gia' a schermo, quindi non si tocca
    # nulla e soprattutto non si AGGIUNGE l'attributo a un file che non l'ha.
    kdoc = parse('<?xml version="1.0" encoding="UTF-8"?>\n<song>\n'
                 '\t<sessionClips>\n'
                 '\t\t<instrumentClip inKeyMode="1" affectEntire="1">\n'
                 '\t\t\t<noteRows>\n\t\t\t\t<noteRow drumIndex="0" />\n'
                 '\t\t\t</noteRows>\n\t\t</instrumentClip>\n'
                 '\t</sessionClips>\n</song>\n')
    kclip = S.clips(kdoc)[0][1]
    S.write_notes(S.note_row(kclip, 0), [Note(pos=0, length=24)], create=True)
    check('una clip di kit non ha note fuori scala da elencare',
          not S.notes_out_of_scale(kdoc, kclip))
    check('il fit di un kit porta yScroll sulla riga che suona, non altrove',
          S.fit_clip_scroll_to_notes(kdoc, kclip) == {'yScroll': '0'}
          and not kclip.has('drumsScrollOffset'),
          f'{kclip.get("yScroll")} / dso={kclip.get("drumsScrollOffset")}')


def test_song_notes_hidden_by_scroll():
    """Note scritte che restano fuori dalla finestra di scroll della clip.

    [LACUNA revisione finale] Il gemello, a livello di CLIP, del famigerato
    yScrollSongView (HANDOFF.md 3.1): contenuto presente, invisibile.
    Entrambi gli script della prova d'accettazione (out/genera_pal01.py,
    out/genera_pal02.py) chiamano fit_clip_scroll_to_notes() dopo aver
    scritto le note -- serviva davvero -- ma prima di questa funzione
    nessuno segnalava il difetto se una generazione se ne dimenticava:
    misurato su TEMPL0.XML (yScroll=37, note a y=24/31/36), sia verifica()
    sia avvertenze() restituivano [].

    Misurato PRIMA di decidere quanto coprire: un controllo esteso anche
    alla modalita' a scala (inKeyMode='1'), usando inKeyScrollOffset in
    GRADI con la stessa formula di fit_clip_scroll_to_notes(), accusa 109
    clip su 131 nel corpus fidato refs/songs -- una percentuale implausibile
    per un difetto reale, la stessa trappola gia' descritta altrove in
    questo modulo per le note fuori scala ("il dispositivo adatta la
    scala"). Il controllo spedito copre quindi SOLO le clip cromatiche
    (inKeyMode diverso da '1'), dove e' misurato pulito su tutti i 139 file
    scritti dal dispositivo.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n<song>\n'
                '\t<sessionClips>\n'
                '\t\t<instrumentClip inKeyMode="0" yScroll="37" length="384">\n'
                '\t\t\t<noteRows>\n'
                '\t\t\t\t<noteRow y="24" />\n'
                '\t\t\t\t<noteRow y="31" />\n'
                '\t\t\t\t<noteRow y="36" />\n'
                '\t\t\t</noteRows>\n'
                '\t\t</instrumentClip>\n'
                '\t</sessionClips>\n</song>\n')
    clip = S.clips(doc)[0][1]
    for y, pos in ((24, 0), (31, 96), (36, 192)):
        S.write_notes(S.note_row(clip, y), [Note(pos=pos, length=24)],
                      create=True)

    fuori = S.notes_hidden_by_scroll(doc)
    check('un basso profondo sotto yScroll=37 viene segnalato',
          len(fuori) == 1 and 'yScroll=37' in fuori[0], str(fuori))
    check('arriva anche da avvertenze(), non da verifica()',
          any('yScroll=37' in a for a in MU.avvertenze(doc))
          and not MU.verifica(doc),
          str((MU.avvertenze(doc), MU.verifica(doc))))

    cambiati = S.fit_clip_scroll_to_notes(doc, clip)
    check('fit_clip_scroll_to_notes() corregge cio che questa funzione segnala',
          not S.notes_hidden_by_scroll(doc), str(cambiati))

    # basta UNA nota visibile per non essere segnalati: e normale che una
    # melodia ad ampio ambito non stia tutta in 8 righe, non e un difetto
    doc2 = parse('<?xml version="1.0" encoding="UTF-8"?>\n<song>\n'
                 '\t<sessionClips>\n'
                 '\t\t<instrumentClip inKeyMode="0" yScroll="40" length="384">\n'
                 '\t\t\t<noteRows>\n'
                 '\t\t\t\t<noteRow y="24" />\n'
                 '\t\t\t\t<noteRow y="42" />\n'
                 '\t\t\t</noteRows>\n'
                 '\t\t</instrumentClip>\n'
                 '\t</sessionClips>\n</song>\n')
    clip2 = S.clips(doc2)[0][1]
    for y, pos in ((24, 0), (42, 96)):
        S.write_notes(S.note_row(clip2, y), [Note(pos=pos, length=24)],
                      create=True)
    check('basta una nota nella finestra per non essere segnalati',
          not S.notes_hidden_by_scroll(doc2))

    # la modalita' a scala ORA e' coperta: la coppia SCALB0/SCALB1 ha chiuso
    # la formula. Senza <modeNotes> non c'e' scala, quindi la riga torna a
    # essere il semitono e con yScroll=37 la nota a 24 resta fuori.
    doc3 = parse('<?xml version="1.0" encoding="UTF-8"?>\n<song>\n'
                 '\t<sessionClips>\n'
                 '\t\t<instrumentClip inKeyMode="1" yScroll="37" '
                 'inKeyScrollOffset="21" length="384">\n'
                 '\t\t\t<noteRows>\n\t\t\t\t<noteRow y="24" />\n'
                 '\t\t\t</noteRows>\n\t\t</instrumentClip>\n'
                 '\t</sessionClips>\n</song>\n')
    clip3 = S.clips(doc3)[0][1]
    S.write_notes(S.note_row(clip3, 24), [Note(pos=0, length=24)], create=True)
    check('una clip in modalita a scala ORA e coperta',
          S.notes_hidden_by_scroll(doc3) != [],
          str(S.notes_hidden_by_scroll(doc3)))
    # l'etichetta segue la modalita' DICHIARATA dalla clip: qui non ci sono
    # <modeNotes>, quindi il conto dei gradi degenera nei semitoni, ma la clip
    # si dichiara in scala e il messaggio lo rispecchia
    check('e il messaggio dice in che unita sta la finestra',
          'gradi' in S.notes_hidden_by_scroll(doc3)[0],
          S.notes_hidden_by_scroll(doc3)[0])

    # anche le clip di kit sono soggette al controllo: la finestra e' sempre
    # `yScroll`, solo che li' l'unita' e' la POSIZIONE della riga.
    # Verificato sul dispositivo con KITSCR0/KITSCR1.
    kdoc = parse('<?xml version="1.0" encoding="UTF-8"?>\n<song>\n'
                 '\t<sessionClips>\n'
                 '\t\t<instrumentClip inKeyMode="0" yScroll="37" '
                 'affectEntire="1">\n'
                 '\t\t\t<noteRows>\n\t\t\t\t<noteRow drumIndex="0" />\n'
                 '\t\t\t</noteRows>\n\t\t</instrumentClip>\n'
                 '\t</sessionClips>\n</song>\n')
    kclip = S.clips(kdoc)[0][1]
    S.write_notes(S.note_row(kclip, 0), [Note(pos=0, length=24)], create=True)
    check('un kit con yScroll lontano dalle sue righe viene segnalato',
          S.notes_hidden_by_scroll(kdoc) != [],
          str(S.notes_hidden_by_scroll(kdoc)))
    check('e il messaggio dice che le righe sono drum',
          'righe di drum' in S.notes_hidden_by_scroll(kdoc)[0],
          S.notes_hidden_by_scroll(kdoc)[0])

    # zero falsi positivi sul corpus reale
    # La garanzia di zero falsi positivi vale sulle clip CROMATICHE, ed e'
    # misurata. In modalita' a scala non si puo' pretendere lo stesso, e il
    # motivo va detto invece che nascosto: **un file scritto dal dispositivo
    # non deve per forza mostrare le proprie note.** Chi scrolla altrove e
    # salva ottiene esattamente una clip "con le note fuori schermo", che e'
    # cio' che questa funzione dichiara -- correttamente. Il corpus contiene
    # anche clip in cui `yScroll` sembra essere rimasto in semitoni da un uso
    # precedente in cromatico: e' un'ambiguita' del formato, non del controllo.
    sporchi = []
    n = crom = scala = 0
    for base in (ROOT / 'refs' / 'songs', ROOT / 'corpus_versions'):
        for q in sorted(base.rglob('*.XML')):
            try:
                d = parse_file(q)
            except Exception:                            # noqa: BLE001
                continue
            n += 1
            for _, c in S.clips(d):
                if c.tag == 'audioClip' or S.is_kit_clip(c):
                    continue
                if not [r for r in S.note_rows(c)
                        if r.has('y') and S.read_notes(r)]:
                    continue
                if c.get('yScroll') is None:
                    continue
                in_scala = c.get('inKeyMode') == '1'
                ys = [int(r.get('y')) for r in S.note_rows(c)
                      if r.has('y') and S.read_notes(r)]
                y0 = int(c.get('yScroll'))
                visibile = any(y0 <= S.clip_row_of(d, c, y) < y0 + 8
                               for y in ys)
                if in_scala:
                    scala += not visibile
                else:
                    crom += 1
                    if not visibile:
                        sporchi.append(f'{q.name}: {S.clip_label(c)!r}')
    check(f'zero falsi positivi sulle {crom} clip cromatiche dei {n} file '
          'del dispositivo', not sporchi, '; '.join(sporchi[:3]))
    check('in modalita a scala il conto e noto e non preteso a zero',
          scala >= 0, f'{scala} clip in scala con le note fuori finestra')


def test_structure():
    """Gli attributi di struttura, e il rifiuto dei valori mai osservati."""
    from delugexml import structure as ST                # noqa: PLC0415

    p = REFS / 'songs' / 'DRUMS1_4.XML'
    if not p.exists():
        salta('struttura', 'DRUMS1_4.XML assente')
        return
    doc = parse_file(p)
    fm = [i for i in S.instruments(doc) if i.get('mode') == 'fm'][0]

    d = ST.describe(fm)
    check('la patch FM viene descritta come tale', d['mode'] == 'fm')
    check('e i suoi oscillatori non hanno forma d onda',
          'FM' in (d.get('osc1') or ''), str(d.get('osc1')))

    # il caso verificato sul dispositivo: il filtro era spento, non assente
    check('il filtro era spento', fm.get('lpfMode') == 'Off')
    ST.set_filter(fm, lpf='24dB')
    check('e si accende', fm.get('lpfMode') == '24dB')

    # un valore mai visto non si scrive per sbaglio
    check('modalita di filtro inventata rifiutata',
          _raises(lambda: ST.set_filter(fm, lpf='36dB'), ValueError))
    check('forma d onda inventata rifiutata',
          _raises(lambda: ST.set_osc(fm, 1, type='sawtooth'), ValueError))
    check('numero fuori intervallo rifiutato',
          _raises(lambda: ST.set_unison(fm, num=99), ValueError))
    check('filterRoute ha un valore solo nel corpus',
          _raises(lambda: ST.set_attr(fm, 'filterRoute', 'L2H'), ValueError))

    # ma si puo' esplorare, dichiarandolo
    check('force scrive comunque',
          ST.set_attr(fm, 'lpfMode', '36dB', force=True) == '36dB')
    ST.set_filter(fm, lpf='24dB')

    # e sul preset subtractive gli oscillatori hanno un tipo
    pr = REFS / 'synths' / 'TEMPL.XML'
    if pr.exists():
        sub = parse_file(pr).root
        check('un preset subtractive ha oscillatori con forma d onda',
              ST.describe(sub)['osc1'] == 'square', str(ST.describe(sub)['osc1']))
        ST.set_osc(sub, 1, type='saw', transpose=-12)
        check('cambio di forma d onda e trasposizione',
              sub.find('osc1').get('type') == 'saw'
              and sub.find('osc1').get('transpose') == '-12')


def test_sound_params_by_name():
    """Accesso ai parametri di suono per nome, nelle unita' del display."""
    from delugexml import sound as SND                   # noqa: PLC0415

    p = REFS / 'songs' / 'DRUMS1_4.XML'
    if not p.exists():
        salta('parametri per nome', 'DRUMS1_4.XML assente')
        return
    doc = parse_file(p)
    cl = [c for _, c in S.clips(doc)]
    kit, synth = cl[0], cl[1]

    check('la clip di synth usa <soundParams>',
          SND.container(synth).tag == 'soundParams')
    check('la clip di kit usa <kitParams>',
          SND.container(kit).tag == 'kitParams', SND.container(kit).tag)
    check('la song usa <songParams>',
          SND.container(doc.root).tag == 'songParams')

    # il volume di questa clip e' quello messo a mano sul dispositivo a 35
    check('il volume si legge come sul display',
          SND.get(synth, 'volume') == 35, str(SND.get(synth, 'volume')))

    # i quattro inviluppi usano gli stessi nomi: senza prefisso si scriverebbe
    # sul primo credendo di scrivere sul terzo
    check('gli inviluppi sono qualificati',
          'envelope1.attack' in SND.names(synth)
          and 'envelope3.release' in SND.names(synth))
    check('e si leggono distintamente',
          SND.get(synth, 'envelope1.attack') is not None
          and SND.get(synth, 'envelope3.attack') is not None)

    # un parametro automatizzato non ha un valore singolo: dirlo, non inventarlo
    check('un parametro automatizzato solleva invece di mentire',
          _raises(lambda: SND.get(synth, 'lpfFrequency'), SND.Automatizzato))
    check('ma il grezzo si legge lo stesso',
          SND.get_raw(synth, 'lpfFrequency').startswith('0x8'))

    scritto = SND.set(synth, 'lpfResonance', 35)
    check('scrittura per nome, andata e ritorno',
          scritto == '0x34000000' and SND.get(synth, 'lpfResonance') == 35,
          f'{scritto} -> {SND.get(synth, "lpfResonance")}')

    check('un nome sbagliato e un errore, con i nomi validi in coda',
          _raises(lambda: SND.set(synth, 'cutoffo', 10), ValueError))

    tutti = SND.read_all(synth)
    check('read_all copre tutti i parametri',
          len(tutti) == len(SND.names(synth)), f'{len(tutti)}')
    check('e marca gli automatizzati',
          tutti.get('lpfFrequency') == 'automatizzato',
          str(tutti.get('lpfFrequency')))

    table = FormatTable.load(TABLE_PATH) if TABLE_PATH.exists() else FormatTable()
    riletto = parse(serialize(doc, table))
    check('il documento resta sano dopo le scritture',
          not riletto.problems, f'{[x.kind for x in riletto.problems][:3]}')


def test_song_level():
    """Scala, swing, sezioni, lunghezza delle clip."""
    p = REFS / 'songs' / 'TEMPL4.XML'
    if not p.exists():
        salta('livello song', 'TEMPL4.XML assente')
        return
    doc = parse_file(p)

    check('la scala si legge col nome giusto',
          S.scale_name(doc) == 'D maggiore', S.scale_name(doc))
    check('gli intervalli sono dalla tonica, non altezze assolute',
          S.get_scale(doc) == (2, (0, 2, 4, 5, 7, 9, 11)), str(S.get_scale(doc)))

    S.set_scale(doc, 'F', 'dorico')
    check('set_scale per nome di nota e di modo',
          S.get_scale(doc) == (5, (0, 2, 3, 5, 7, 9, 10)), str(S.get_scale(doc)))
    check('e le classi di altezza seguono',
          sorted(S.scale_pitch_classes(doc.root)) == [0, 2, 3, 5, 7, 8, 10],
          str(sorted(S.scale_pitch_classes(doc.root))))
    check('i modeNote sono figli con il valore nel testo',
          [c.text for c in doc.root.find('modeNotes').children]
          == ['0', '2', '3', '5', '7', '9', '10'])

    S.set_scale(doc, 7, (0, 3, 5, 7, 10))          # pentatonica minore
    check('anche intervalli arbitrari', S.get_scale(doc) == (7, (0, 3, 5, 7, 10)))
    check('nota sconosciuta rifiutata',
          _raises(lambda: S.set_scale(doc, 'H', 'maggiore'), ValueError))
    check('modo sconosciuto rifiutato',
          _raises(lambda: S.set_scale(doc, 0, 'iperlidio'), ValueError))

    # [BUG CORRETTO revisione finale] set_scale() faceva
    # root.upper().replace('B', '#') sul nome: un bemolle come 'Ab' diventava
    # silenziosamente 'A#' invece di 'G#' -- UN SEMITONO SBAGLIATO, SENZA
    # ERRORE, perche' 'A#' resta comunque un nome valido. Ora riusa
    # musica.altezza() (via _grado_e_bemolle) invece di duplicare il parser,
    # quindi accetta lo stesso vocabolario -- italiano, inglese, diesis,
    # bemolle -- e i bemolle danno la nota giusta.
    S.set_scale(doc, 'Ab', 'maggiore')
    check('Ab e G#, non A#', S.get_scale(doc)[0] == 8, str(S.get_scale(doc)))
    S.set_scale(doc, 'Db', 'maggiore')
    check('Db e C#, non D#', S.get_scale(doc)[0] == 1, str(S.get_scale(doc)))
    S.set_scale(doc, 'Gb', 'maggiore')
    check('Gb e F#, non G#', S.get_scale(doc)[0] == 6, str(S.get_scale(doc)))
    # i due bemolle 'a due lettere' che il parser vecchio rifiutava per
    # errore (root.replace('B','#') su 'EB'/'BB' dava 'E#'/'##', nomi
    # assenti dalla tabella) anche se sono nomi legittimi
    S.set_scale(doc, 'Eb', 'maggiore')
    check('Eb e D#', S.get_scale(doc)[0] == 3, str(S.get_scale(doc)))
    S.set_scale(doc, 'Bb', 'maggiore')
    check('Bb e A#', S.get_scale(doc)[0] == 10, str(S.get_scale(doc)))
    # e i nomi italiani, che il parser vecchio non riconosceva affatto: chi
    # dice "re minore" non deve vedersi rifiutare il nome
    S.set_scale(doc, 're', 'minore')
    check('il nome italiano re funziona, come musica.altezza()',
          S.get_scale(doc)[0] == 2, str(S.get_scale(doc)))
    S.set_scale(doc, 'fa#', 'minore')
    check('e coi diesis', S.get_scale(doc)[0] == 6, str(S.get_scale(doc)))
    # l'intero 0-11 di prima resta valido: non deve rompersi
    S.set_scale(doc, 3, 'maggiore')
    check('un intero 0-11 resta accettato', S.get_scale(doc)[0] == 3)

    # Lo swing del display e' 0-100 con 50 al centro; nel file e' con segno.
    # Verificato sul dispositivo: scritto 25 grezzo, il display mostrava 75.
    grezzo = S.set_swing(doc, 75, 9)
    check('swing: il display 75 diventa +25 nel file', grezzo == 25, str(grezzo))
    check('e si rilegge come 75', S.get_swing(doc) == (75, 9),
          str(S.get_swing(doc)))
    check('50 e dritto, cioe zero nel file',
          S.set_swing(doc, 50) == 0)
    check('swing negativo',
          S.set_swing(doc, 40) == -10)
    check('fuori da 0-100 rifiutato',
          _raises(lambda: S.set_swing(doc, 101), ValueError))

    # 24 e' quello che scrive c1.3.0, non una costante del formato: nel corpus
    # 103 song ne hanno 12 e 36 ne hanno 24, secondo la versione.
    check('c1.3.0 scrive 24 sezioni',
          len(S.sections(doc)) == S.N_SEZIONI, str(len(S.sections(doc))))
    S.set_section_repeats(doc, 1, 4)
    check('ripetizioni di sezione', S.sections(doc)[1].get('numRepeats') == '4')
    check('sezione inesistente rifiutata',
          _raises(lambda: S.set_section_repeats(doc, 99, 1), ValueError))

    clip = [c for _, c in S.clips(doc)][1]
    avvisi = S.set_clip_length(clip, 192)
    check('la lunghezza cambia', clip.get('length') == '192')
    check('e le note che restano fuori vengono segnalate',
          len(avvisi) == 2, str(avvisi))
    check('lunghezza non valida rifiutata',
          _raises(lambda: S.set_clip_length(clip, 0), ValueError))

    # tutto questo deve restare riscrivibile e rileggibile
    table = FormatTable.load(TABLE_PATH) if TABLE_PATH.exists() else FormatTable()
    riletto = parse(serialize(doc, table))
    check('il documento sopravvive alle modifiche di livello song',
          not riletto.problems
          and S.get_scale(riletto) == (3, (0, 2, 4, 5, 7, 9, 11)),
          f'{[x.kind for x in riletto.problems][:3]}')


def test_create_track_from_preset():
    """Istanziare un preset dentro una song, e la trappola degli span.

    Gli span sono offset nel testo del documento di PROVENIENZA. Un nodo
    copiato da un file A dentro un file B, se resta "pulito", viene riemesso
    ricopiando i byte a quegli offset dal testo di B: esce spazzatura, non un
    errore. La prima volta ha prodotto tag troncati tipo

        <modKnob controlsParam="modulato
        Volume" />

    e il file si scriveva senza lamentele, fallendo solo alla rilettura.
    """
    from delugexml import create as C                    # noqa: PLC0415

    song_p = REFS / 'songs' / 'TEMPL0.XML'
    preset_p = REFS / 'synths' / 'TEMPL.XML'
    if not (song_p.exists() and preset_p.exists()):
        salta('creazione da preset', 'TEMPL0/TEMPL assenti')
        return

    doc = parse_file(song_p)
    n_clip, n_inst = len(S.clips(doc)), len(S.instruments(doc))
    y_song = int(doc.root.get('yScrollSongView'))

    inst, clip = C.add_track(doc, preset_p, name='TEMPL', folder='SYNTHS',
                             length=384, playing=True)

    check('lo strumento e la clip si aggiungono',
          len(S.clips(doc)) == n_clip + 1
          and len(S.instruments(doc)) == n_inst + 1)
    check('lo strumento perde i metadati di file',
          not inst.has('firmwareVersion')
          and not inst.has('earliestCompatibleFirmware'))
    check('e guadagna gli attributi di istanza',
          inst.get('presetName') == 'TEMPL'
          and inst.get('presetFolder') == 'SYNTHS'
          and inst.has('defaultVelocity'))
    check('defaultParams diventa il soundParams della clip',
          clip.find('soundParams') is not None
          and inst.find('defaultParams') is None)
    check('una clip vuota non porta noteRows',
          clip.find('noteRows') is None)
    check('gli scroll seguono, in entrambe le viste',
          int(doc.root.get('yScrollSongView')) == y_song + 1
          and int(doc.root.get('yScrollArrangementView')) == y_song + 1,
          f'{doc.root.get("yScrollSongView")}/'
          f'{doc.root.get("yScrollArrangementView")}')
    check('la clip nuova e quella aperta', clip.get('beingEdited') == '1')

    # la prova della trappola: il documento deve rileggersi senza anomalie
    table = FormatTable.load(TABLE_PATH) if TABLE_PATH.exists() else FormatTable()
    riletto = parse(serialize(doc, table))
    check('nessuna anomalia: gli span del preset non inquinano la song',
          not riletto.problems,
          f'{[p.kind for p in riletto.problems][:4]}')
    check('e la struttura sopravvive al giro',
          len(S.clips(riletto)) == n_clip + 1
          and len(S.instruments(riletto)) == n_inst + 1)

    # copy() dentro lo stesso documento deve invece CONSERVARE gli span
    c0 = [c for _, c in S.clips(doc)][0]
    check('copy() conserva lo span, copy_detached() no',
          c0.copy().span == c0.span and c0.copy_detached().span is None)


def test_automation():
    """L'automazione del cutoff, decodificata contro una forma nota.

    Disegnata sul dispositivo come mezza battuta di rampa in salita e mezza in
    discesa, poi salvata e riletta via USB. Il decoder deve restituire quel
    triangolo: se sbagliasse l'allineamento delle coppie, non uscirebbe.
    """
    from delugexml import automation as A                # noqa: PLC0415
    from delugexml import params as P                    # noqa: PLC0415

    p = REFS / 'songs' / 'DRUMS1_4.XML'
    if not p.exists():
        salta('automazione', 'DRUMS1_4.XML assente')
        return
    doc = parse_file(p)

    blob = None
    for node in doc.root.iter():
        v = node.get('lpfFrequency')
        if v and A.is_automation(v):
            blob = v
            break
    check('automazione trovata su lpfFrequency', blob is not None)
    if blob is None:
        return

    check('un valore fisso non e scambiato per automazione',
          not A.is_automation('0x7FFFFFFF'))

    testa, punti = A.decode(blob)
    check('22 punti', len(punti) == 22, str(len(punti)))
    check('intestazione conservata', testa == 0x80000000, hex(testa))

    disp = [P.to_display(pt.hex) for pt in punti]
    atteso = [0, 7, 14, 21, 29, 36, 43, 50, 50, 43, 43, 36, 36, 29, 29,
              21, 21, 14, 14, 7, 7, 0]
    check('il profilo e il triangolo disegnato', disp == atteso, str(disp))

    pos = [pt.pos for pt in punti]
    check('parte a 0 e finisce a 360', (pos[0], pos[-1]) == (0, 360),
          f'{pos[0]}..{pos[-1]}')
    check('la salita e per sedicesimi', pos[:8] == [0, 24, 48, 72, 96, 120,
                                                   144, 168], str(pos[:8]))
    check('le posizioni sono crescenti', pos == sorted(pos))
    check('nessun nodo interpolato in questo esemplare',
          not any(pt.interp for pt in punti))

    # il bit 31 della posizione e' il flag di interpolazione (auto_param.cpp),
    # non parte della posizione: senza mascherarlo si leggerebbe un tick assurdo
    finto = A.encode(0x80000000, [A.Punto(pos=48, raw=0x00000000, interp=True)])
    t3, p3 = A.decode(finto)
    check('il bit 31 si rilegge come interpolazione, non come posizione',
          p3[0].pos == 48 and p3[0].interp, f'{p3[0].pos}, {p3[0].interp}')
    check('e la parola di posizione lo riporta', p3[0].pos_word == 48 | (1 << 31),
          hex(p3[0].pos_word))

    # il giro completo deve tornare al byte: e' un blob, come le note
    check('ricodifica byte-identica',
          A.encode(testa, punti).lower() == blob.lower(),
          f'{len(A.encode(testa, punti))} contro {len(blob)}')

    # e una rampa costruita da noi si rilegge come tale
    # in unita interne i punti restano tutti sulla griglia, quindi leggibili.
    # Nota: interpolando i valori GREZZI la rampa usciva [0, 0, 0, 50, 50] —
    # estremi giusti e mezzo sbagliato, perche' fra 0x80000000 e 0x7FFFFFFF la
    # retta passa dalla parte sbagliata del wrap-around. Serve la monotonia,
    # non solo gli estremi.
    check('il massimo interno e 127, non 128',
          _raises(lambda: P.from_internal(128), ValueError)
          and P.to_display(P.from_internal(127)) == 50,
          P.from_internal(127))

    t2, p2 = A.ramp_internal(0, P.INTERNO_MAX, 0, 192, 5)
    d2 = [P.to_display(x.hex) for x in p2]
    check('una rampa generata sale da 0 a 50', d2[0] == 0 and d2[-1] == 50,
          str(d2))
    check('e sale davvero, punto per punto',
          all(b > a for a, b in zip(d2, d2[1:])), str(d2))
    check('tutti i punti restano leggibili', None not in d2, str(d2))
    check('le posizioni della rampa sono regolari',
          [x.pos for x in p2] == [0, 48, 96, 144, 192], str([x.pos for x in p2]))
    check('e si rilegge dopo la codifica',
          A.decode(A.encode(t2, p2))[1] == p2)

    # Rendere visibile l'automazione: verificato sul dispositivo. Scrivere il
    # blob non basta — se `beingEdited` resta su un'altra clip, il Deluge apre
    # quella e non si vede niente, pur essendo il blob corretto.
    doc2 = parse_file(REFS / 'songs' / 'TEMPL4.XML')
    cl = [c for _, c in S.clips(doc2)]
    kit, synth = cl[0], cl[1]
    kit.set('beingEdited', '1')
    A.mark_view(doc2, synth, 'lpfFrequency')
    check('la clip automatizzata diventa quella aperta',
          synth.get('beingEdited') == '1' and kit.get('beingEdited') == '0',
          f'kit={kit.get("beingEdited")}, synth={synth.get("beingEdited")}')
    check('e porta lo stato della vista',
          synth.get('onAutomationInstrumentClipView') == '1'
          and synth.get('lastSelectedParamID') == '24')
    check('beingEdited resta esclusivo',
          sum(1 for c in cl if c.get('beingEdited') == '1') == 1)
    # la vista si sa impostare per qualunque parametro in tabella, non piu'
    # solo per il cutoff: gli ID vengono dall'enum di param.h
    from delugexml import param_ids as PI                # noqa: PLC0415
    v = A.mark_view(doc2, synth, 'reverbAmount')
    check('mark_view funziona per ogni parametro in tabella',
          v['lastSelectedParamID'] == '47' and v['lastSelectedParamKind'] == '1',
          str(v))
    check('e per il cutoff da l ID verificato sul dispositivo',
          PI.by_name('lpfFrequency').id == 24)
    # gli UNPATCHED, letti dal file di un'automazione fatta a mano:
    # arpeggiatorGate -> id 11, kind 2. Da li' si e' saputo che i marcatori
    # dell'enum sono alias (11 e non 12) e che UNPATCHED_START=90 non entra
    # negli ID (11 e non 101).
    ag = PI.by_name('arpeggiatorGate')
    check('arpeggiatorGate = 11, quindi i marcatori sono alias', ag.id == 11,
          str(ag.id))
    check('e senza offset 90', ag.id < 90)
    check('Kind 2 su una clip di suono, non 3', ag.kind == 2, str(ag.kind))
    v2 = A.mark_view(doc2, synth, 'stutterRate')
    check('anche gli unpatched si sanno scrivere ora',
          v2['lastSelectedParamID'] == '0' and v2['lastSelectedParamKind'] == '2',
          str(v2))
    check('un nome fuori tabella resta un errore, non un indovinello',
          _raises(lambda: A.mark_view(doc2, synth, 'inventato'), ValueError))
    check('le scorciatoie si omettono se non osservate',
          'lastSelectedParamShortcutX' not in v)


def test_kit_drum_names():
    """I drum si indirizzano per nome, non per indice.

    TEMPL4 e' il banco di prova giusto: kit e synth nella stessa song, e le
    note stanno in posizioni decise PRIMA di leggere il file — kick sui
    movimenti 1 e 3, snare sul 2 e sul 4. Se il legame nome -> drumIndex e'
    sbagliato, le posizioni non tornano.
    """
    p = REFS / 'songs' / 'TEMPL4.XML'
    if not p.exists():
        salta('nomi dei drum', 'TEMPL4.XML assente')
        return
    doc = parse_file(p)
    cl = [c for _, c in S.clips(doc)]
    kit_clip, synth_clip = cl[0], cl[1]

    check('la clip di kit e riconosciuta', S.is_kit_clip(kit_clip))
    check('la clip di synth non e un kit', not S.is_kit_clip(synth_clip))

    names = S.drum_names(doc, kit_clip)
    check('il kit ha 16 drum', len(names) == 16, str(len(names)))
    check('drumIndex 0 = KICK, 1 = SNARE', names[:2] == ['KICK', 'SNARE'],
          str(names[:3]))

    i_kick = S.drum_index(doc, kit_clip, 'KICK')
    i_snare = S.drum_index(doc, kit_clip, 'SNARE')
    check('ricerca per nome', (i_kick, i_snare) == (0, 1), f'{i_kick},{i_snare}')

    kick = S.note_row(kit_clip, i_kick)
    snare = S.note_row(kit_clip, i_snare)
    check('le note del KICK cadono sui movimenti 1 e 3',
          [n.pos for n in S.read_notes(kick)] == [0, 192],
          str([n.pos for n in S.read_notes(kick)]))
    check('le note dello SNARE cadono sui movimenti 2 e 4',
          [n.pos for n in S.read_notes(snare)] == [96, 288],
          str([n.pos for n in S.read_notes(snare)]))

    check('nome inesistente: errore chiaro, non un indice sbagliato',
          _raises(lambda: S.drum_index(doc, kit_clip, 'BONGOZZO'), ValueError))
    check('un synth non ha drum',
          _raises(lambda: S.drum_names(doc, synth_clip), ValueError))


def _raises(fn, exc):
    try:
        fn()
    except exc:
        return True
    except Exception:                                # noqa: BLE001
        return False
    return False


def test_scroll_matches_device():
    """La formula riproduce cifra per cifra quello che ha fatto il dispositivo.

    TEMPL3 e TEMPL4 sono due salvataggi consecutivi, a un passo di distanza:
    fra i due e' stata aggiunta una clip di kit. Il dispositivo ha spostato
    `yScrollSongView` da -7 a -6 e con esso `yScrollArrangementView`, che
    nell'arranger conta gli strumenti invece delle clip.

    Non e' un test sulle nostre convinzioni: il valore atteso e' letto dal
    file che ha scritto il Deluge.
    """
    t3, t4 = REFS / 'songs' / 'TEMPL3.XML', REFS / 'songs' / 'TEMPL4.XML'
    if not (t3.exists() and t4.exists()):
        salta('scroll contro il dispositivo', 'TEMPL3/TEMPL4 assenti')
        return

    after = parse_file(t4)
    n_clip_after = len(S.clips(after))
    want_song = after.root.get('yScrollSongView')
    want_arr = after.root.get('yScrollArrangementView')

    doc = parse_file(t3)
    check('il punto di partenza ha una clip sola', len(S.clips(doc)) == 1,
          f'{len(S.clips(doc))}')

    # la clip aggiunta dal dispositivo e' l'ultima: indice n-1
    got_song = S.scroll_song_view_to(doc, n_clip_after - 1)
    check('yScrollSongView calcolato = quello scritto dal Deluge',
          got_song == want_song, f'nostro {got_song}, suo {want_song}')

    got_arr = S.scroll_arrangement_view_to(doc, n_clip_after - 1)
    check('yScrollArrangementView calcolato = quello scritto dal Deluge',
          got_arr == want_arr, f'nostro {got_arr}, suo {want_arr}')

    # il gradino precedente non aggiunge ne clip ne strumenti: niente si muove
    t2 = REFS / 'songs' / 'TEMPL2.XML'
    if t2.exists():
        a, b = parse_file(t2).root, parse_file(t3).root
        check('aggiungere solo note non muove gli scroll',
              a.get('yScrollSongView') == b.get('yScrollSongView')
              and a.get('yScrollArrangementView') == b.get('yScrollArrangementView'),
              f'{a.get("yScrollSongView")}/{a.get("yScrollArrangementView")} '
              f'contro {b.get("yScrollSongView")}/{b.get("yScrollArrangementView")}')


def test_add_note_row_sorted():
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n<song>\n'
                '\t<sessionClips>\n\t\t<instrumentClip length="768">\n'
                '\t\t\t<noteRows>\n\t\t\t\t<noteRow y="60" />\n'
                '\t\t\t\t<noteRow y="72" />\n'
                '\t\t\t</noteRows>\n\t\t</instrumentClip>\n'
                '\t</sessionClips>\n</song>\n')
    clip = S.clips(doc)[0][1]
    for y in (66, 50, 90):
        S.add_note_row(clip, y)
    ys = [int(r.get('y')) for r in S.note_rows(clip)]
    check('le noteRow restano ordinate per y', ys == sorted(ys), str(ys))
    check('inserite tutte', ys == [50, 60, 66, 72, 90], str(ys))
    try:
        S.add_note_row(clip, 66)
        check('rifiuta una y duplicata', False, 'nessun errore sollevato')
    except ValueError:
        check('rifiuta una y duplicata', True)


def test_new_row_notes():
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n<song>\n'
                '\t<sessionClips>\n\t\t<instrumentClip length="768">\n'
                '\t\t\t<noteRows>\n\t\t\t\t<noteRow y="60" />\n'
                '\t\t\t</noteRows>\n\t\t</instrumentClip>\n'
                '\t</sessionClips>\n</song>\n')
    clip = S.clips(doc)[0][1]
    row = S.note_row(clip, 60)
    try:
        S.write_notes(row, [Note(pos=0, length=48)])
        check('senza create=True rifiuta una riga vuota', False)
    except ValueError:
        check('senza create=True rifiuta una riga vuota', True)

    S.write_notes(row, [Note(pos=0, length=48, velocity=100)], create=True)
    check('crea entrambi gli attributi di note',
          all(row.has(x) for x in N.NEW_ROW_ATTRS),
          str([k for k, _ in row.attrs]))
    back = S.read_notes(row)
    check('la nota si rilegge', len(back) == 1 and back[0].velocity == 100,
          str(back))


def test_clear_notes_removes_attrs():
    """Svuotare una riga deve togliere gli attributi, non lasciarli a '0x'."""
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n<song>\n'
                '\t<sessionClips>\n\t\t<instrumentClip length="768">\n'
                '\t\t\t<noteRows>\n\t\t\t\t<noteRow y="60" '
                'noteDataWithSplitProb="0x000000000000003064401400 0000"'
                ' />\n'
                '\t\t\t</noteRows>\n\t\t</instrumentClip>\n'
                '\t</sessionClips>\n</song>\n'.replace(' 0000"', '0000"'))
    row = S.note_rows(S.clips(doc)[0][1])[0]
    check('partenza: la riga ha delle note', len(S.read_notes(row)) == 1)
    S.write_notes(row, [])
    check('svuotando spariscono gli attributi di note',
          not any(row.has(x) for x in N.ATTR_WIDTH),
          str([k for k, _ in row.attrs]))
    check('nessun blob vuoto "0x" lasciato in giro',
          all(v != '0x' for _, v in row.attrs), str(row.attrs))


def test_scale():
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<song rootNote="7">\n\t<modeNotes>\n'
                + ''.join(f'\t\t<modeNote>{m}</modeNote>\n'
                          for m in (0, 2, 3, 5, 7, 8, 10))
                + '\t</modeNotes>\n</song>\n')
    song = doc.root
    pcs = S.scale_pitch_classes(song)
    # root 7 = G, intervalli di minore naturale -> G A Bb C D Eb F
    check('scala di Perche letta come G minore',
          pcs == {7, 9, 10, 0, 2, 3, 5}, str(sorted(pcs)))
    check('G (67) e in scala', S.in_scale(song, 67))
    check('B naturale (71) non e in scala', not S.in_scale(song, 71))
    check('snap porta 71 su una nota della scala',
          S.in_scale(song, S.snap_to_scale(song, 71)),
          f'71 -> {S.snap_to_scale(song, 71)}')
    check('snap lascia stare cio che e gia in scala',
          S.snap_to_scale(song, 67) == 67)


def test_kit_vs_synth_rows():
    def clip_with(attr, vals):
        rows = ''.join(f'\t\t\t\t<noteRow {attr}="{v}" />\n' for v in vals)
        return parse('<?xml version="1.0" encoding="UTF-8"?>\n<song>\n'
                     '\t<sessionClips>\n\t\t<instrumentClip length="768">\n'
                     f'\t\t\t<noteRows>\n{rows}\t\t\t</noteRows>\n'
                     '\t\t</instrumentClip>\n\t</sessionClips>\n</song>\n')

    syn = S.clips(clip_with('y', [60, 64]))[0][1]
    kit = S.clips(clip_with('drumIndex', [0, 1]))[0][1]
    check('clip con y riconosciuta come synth', not S.is_kit_clip(syn))
    check('clip con drumIndex riconosciuta come kit', S.is_kit_clip(kit))
    check('attributo di indice scelto correttamente',
          (S.row_index_attr(syn), S.row_index_attr(kit)) == ('y', 'drumIndex'))

    S.add_note_row(kit, 3)
    idx = [int(r.get('drumIndex')) for r in S.note_rows(kit)]
    check('riga di kit aggiunta con drumIndex e in ordine',
          idx == [0, 1, 3], str(idx))
    check('nessuna y introdotta su una clip kit',
          all(not r.has('y') for r in S.note_rows(kit)))


def test_corpus_notes_roundtrip():
    """Ogni blob di note del corpus deve ricodificarsi identico."""
    total = bad = 0
    examples = []
    for p in sorted((REFS / 'songs').glob('*.XML')):
        doc = parse_file(p)
        for _, node in doc.path_iter():
            if node.tag != 'noteRow':
                continue
            for attr, w in N.ATTR_WIDTH.items():
                v = node.get(attr)
                if not v:
                    continue
                total += 1
                if N.encode(N.decode(v, w), w) != v.upper().replace('0X', '0x'):
                    bad += 1
                    if len(examples) < 3:
                        examples.append(f'{p.name}:{attr}')
    check(f'ricodifica identica su tutti i blob del corpus ({total})',
          bad == 0, f'{bad} diversi: {examples}')


def test_arranger():
    """`clipCode` e' un indice ordinale, e il bit 31 sceglie la lista.

    La prova non e' che gli indici stiano in range — quello lo farebbe anche
    una decodifica sfasata — ma che ogni istanza risolva a una clip DELLO
    STESSO strumento che la ospita. Un allineamento sbagliato delle terne, o
    la lista sbagliata, romperebbe proprio quel legame.
    """
    from delugexml import arranger as A                  # noqa: PLC0415

    ist = A.Istanza(pos=3072, length=20352, code=0x00000000)
    check('istanza in sessionClips', not ist.da_arranger and ist.indice == 0)
    arr = A.Istanza(pos=0, length=384, code=0x8000000E)
    check('bit 31 = clip d arranger', arr.da_arranger and arr.indice == 14)
    vuota = A.Istanza(pos=0, length=384, code=A.NESSUNA)
    check('0xFFFFFFFF e la sentinella', vuota.vuota and vuota.indice is None)
    check('fine = pos + length', arr.fine == 384)
    check('codice() ricostruisce il bit', A.codice(14, True) == 0x8000000E
          and A.codice(14) == 14)

    blob = '0x00000C0000004F8000000000000010000000018080000001'
    d = A.decode(blob)
    check('decode di due terne', len(d) == 2 and d[0].pos == 3072
          and d[0].length == 0x4F80 and d[1].da_arranger)
    check('encode e l inverso di decode', A.encode(d) == blob.upper()
          .replace('0X', '0x'))
    try:
        A.decode('0x0000000000000000')       # due parole: non e' una terna
        ok = False
    except ValueError:
        ok = True
    check('un blob non a terne viene rifiutato', ok)

    # il corpus: ogni istanza deve risolvere, e allo strumento giusto
    n_song = n_ist = n_ris = 0
    problemi = []
    for base in (ROOT / 'refs' / 'songs', ROOT / 'corpus_versions'):
        for p in sorted(base.rglob('*.XML')):
            try:
                doc = parse_file(p)
            except Exception:                            # noqa: BLE001
                continue
            if not A.has_arrangement(doc):
                continue
            n_song += 1
            for _, i, clip in A.arrangement(doc):
                n_ist += 1
                if clip is not None:
                    n_ris += 1
            for x in A.check(doc)[:2]:
                problemi.append(f'{p.name}: {x}')

    if n_song == 0:
        salta('corpus: arrangiamento',
              'nessuna song del corpus e disponibile')
        return
    check(f'corpus: {n_song} song con arrangiamento, {n_ist} istanze',
          n_song > 0 and n_ist > 0)
    check(f'tutte risolte tranne le sentinelle ({n_ris}/{n_ist})',
          n_ist - n_ris <= 1, f'{n_ist - n_ris} non risolte')
    check('nessuna istanza punta alla clip di un altro strumento',
          not problemi, '; '.join(problemi[:3]))


def test_arranger_scrittura():
    """Dalla ARR0 si deve riottenere la ARR1, che l'ha scritta il dispositivo.

    Coppia controllata: stessa song salvata due volte, in mezzo una sola
    azione — una clip vuota piazzata a 3:1:1 in arranger view. E' l'unico modo
    di sapere cosa il dispositivo tocca OLTRE al dato, ed e' la domanda che con
    `yScrollSongView` e `beingEdited` era gia' costata due volte.

    Differenza ammessa: `preview`, la miniatura dello schermo, che il
    dispositivo rigenera e che non sappiamo produrre (FINDINGS §7).
    """
    from delugexml import arranger as A                  # noqa: PLC0415

    p0, p1 = REFS / 'songs' / 'ARR0.XML', REFS / 'songs' / 'ARR1.XML'
    if not (p0.exists() and p1.exists()):
        salta('coppia ARR0/ARR1', 'file assenti')
        return

    doc = parse_file(p0)
    clip = doc.root.find('sessionClips').children[0]
    strumento = S.instrument_of(doc, clip)
    check('lo strumento della clip si risolve', strumento is not None)
    if strumento is None:
        return

    ist = A.place(doc, strumento, clip, pos=768)          # battuta 3
    check('istanza a battuta 3, lunga una battuta',
          ist.pos == 768 and ist.length == 384 and ist.indice == 0
          and not ist.da_arranger)
    A.fit_view(doc)

    vero = parse_file(p1)
    diffs = []
    conta = {}
    mio_m, ver_m = {}, {}
    for m, d in ((mio_m, doc), (ver_m, vero)):
        conta.clear()
        for perc, n in d.root.path_iter():
            k = conta.get(perc, 0)
            conta[perc] = k + 1
            m[f'{perc}#{k}'] = n
    check('stessi nodi, nessuno aggiunto o tolto',
          set(mio_m) == set(ver_m),
          f'{len(set(mio_m) ^ set(ver_m))} diversi')
    for k in mio_m:
        if k not in ver_m:
            continue
        da, db = dict(mio_m[k].attrs), dict(ver_m[k].attrs)
        for att in sorted(set(da) | set(db)):
            if da.get(att) != db.get(att) and att != 'preview':
                diffs.append(f'{k}:{att}')
    check('riproduce il file del dispositivo (preview esclusa)',
          not diffs, f'{len(diffs)} diversi: {diffs[:4]}')

    check('il blob e identico a quello scritto dal dispositivo',
          strumento.get('clipInstances')
          == '0x000003000000018000000000',
          strumento.get('clipInstances'))

    # le regole di visibilita' che la coppia ha rivelato
    check('inArrangementView acceso', doc.root.get('inArrangementView') == '1')
    beingEdited = [c for _, c in S.clips(doc) if c.get('beingEdited') == '1']
    check('nessuna clip resta beingEdited in arranger view', not beingEdited)

    # sovrapposizione rifiutata
    try:
        A.place(doc, strumento, clip, pos=768 + 192)
        ok = False
    except ValueError:
        ok = True
    check('un istanza sovrapposta viene rifiutata', ok)


def test_arranger_clip_bianca():
    """La clip "bianca": copia indipendente che vive solo sulla timeline.

    Il criterio e' l'ASSENZA di `section` — nel corpus 54 clip d'arranger su
    54 non hanno l'attributo, e 1127 clip di sessione su 1127 ce l'hanno.

    Il test che conta e' l'indipendenza: modificare la copia non deve toccare
    l'originale. E il round-trip, perche' una copia fatta con `copy()` invece
    che `copy_detached()` si scrive senza errori e fallisce alla rilettura.
    """
    from delugexml import arranger as A                  # noqa: PLC0415
    from delugexml.notes import Note as Nt               # noqa: PLC0415

    p = REFS / 'songs' / 'ARR0.XML'
    if not p.exists():
        salta('ARR0 per la clip bianca', 'file assente')
        return
    doc = parse_file(p)
    clip = doc.root.find('sessionClips').children[0]
    strumento = S.instrument_of(doc, clip)

    check('la sorgente appartiene a una scena', not A.is_white(clip))
    check('il contenitore d arranger non esiste ancora',
          doc.root.find('arrangementOnlyTracks') is None)

    bianca, ist = A.place_unique(doc, strumento, clip, pos=768, length=384)
    check('il contenitore viene creato dopo sessionClips',
          [c.tag for c in doc.root.children].index('arrangementOnlyTracks')
          == [c.tag for c in doc.root.children].index('sessionClips') + 1)
    check('la copia e bianca', A.is_white(bianca)
          and bianca.get('section') is None)
    check('e il bit 31 e acceso', ist.da_arranger and ist.indice == 0
          and ist.code == 0x80000000)

    # indipendenza: una nota nella copia non deve comparire nell'originale
    riga_b = S.add_note_row(bianca, 64)
    S.write_notes(riga_b, [Nt(pos=0, length=48)], create=True)
    ys_orig = [r.get('y') for r in S.note_rows(clip)]
    check('modificare la copia non tocca l originale', '64' not in ys_orig,
          f'righe dell originale: {ys_orig}')

    # round-trip: e' qui che una copy() con span sbagliati esplode
    testo = serialize(doc)
    ri = parse(testo)
    check('il documento si rilegge dopo la copia',
          len(A.clip_list(ri, True)) == 1
          and A.is_white(A.clip_list(ri, True)[0]))
    check('e l arrangiamento resta sano', not A.check(ri), A.check(ri)[:1])

    # una clip di un altro strumento va rifiutata
    from delugexml import Node as Nd                     # noqa: PLC0415
    altro = Nd(tag='sound', attrs=[('presetName', 'ALTRO')])
    try:
        A.place_unique(doc, altro, clip, pos=4096)
        ok = False
    except ValueError:
        ok = True
    check('copia su uno strumento estraneo rifiutata', ok)


def test_sezioni():
    """Una sezione e' una scena: clip che partono insieme."""
    esempio = REFS / 'songs' / 'Electronic.XML'
    if not esempio.exists():
        salta('Electronic.XML per le sezioni', 'assente')
        return
    doc = parse_file(esempio)
    check('le <section> hanno solo id e numRepeats',
          all({k for k, _ in s.attrs} <= {'id', 'numRepeats'}
              for s in S.sections(doc)))
    sez0 = S.clips_in_section(doc, 0)
    check('la sezione 0 raccoglie piu strumenti', len(sez0) > 1,
          f'{len(sez0)} clip')
    varianti = [len(S.clips_in_section(doc, i)) for i in range(4)]
    check('le sezioni 1-3 sono varianti piu piccole della 0',
          varianti[0] > max(varianti[1:]), f'{varianti}')

    # il conflitto di grid view esiste davvero nel corpus
    tot = 0
    for base in (ROOT / 'refs' / 'songs', ROOT / 'corpus_versions'):
        for q in sorted(base.rglob('*.XML')):
            try:
                d = parse_file(q)
            except Exception:                            # noqa: BLE001
                continue
            tot += len(S.same_section_conflicts(d))
    check(f'same_section_conflicts trova i casi degradati ({tot})', tot > 0)


def test_tipo_clip_kit():
    """Una clip deve dichiarare lo stesso tipo da tutte le parti.

    Regressione di un file che il Deluge ha rifiutato come corrotto pur essendo
    XML valido e rileggibile senza errori: `add_track` da un preset di kit
    metteva sulla clip `<soundParams>` invece di `<kitParams>`. Dal firmware
    (`instrument_clip.cpp`) quel tag non e' un'etichetta ma una dichiarazione:

        else if (!strcmp(tagName, "soundParams")) {
            outputTypeWhileLoading = OutputType::SYNTH;

    La clip si annunciava synth e poi mostrava righe con `drumIndex`.
    """
    from delugexml import create as C                    # noqa: PLC0415

    preset = REFS / 'kits' / 'CR78FROMMARS.XML'
    base = REFS / 'songs' / 'ARR0.XML'
    if not (preset.exists() and base.exists()):
        salta('preset di kit per il test', 'file assenti')
        return

    doc = parse_file(base)
    inst, clip = C.add_track(doc, preset, name='CR78FROMMARS', folder='KITS')
    check('lo strumento e un <kit>', inst.tag == 'kit')
    check('la clip porta kitParams, non soundParams',
          clip.find('kitParams') is not None
          and clip.find('soundParams') is None,
          [c.tag for c in clip.children])
    check('e affectEntire, senza cui non e riconoscibile come kit',
          clip.has('affectEntire') and S.is_kit_clip(clip))
    check('nessuna contraddizione di tipo', not S.check_clip_types(doc),
          S.check_clip_types(doc)[:2])

    # le note per nome di drum funzionano sulla clip appena creata, e la riga
    # c'e' gia' -- add_track() le ha messe tutte: niente add_note_row qui
    n_righe_prima = len(S.note_rows(clip))
    riga = S.drum_row(doc, clip, 'Kick CR78 12')
    S.write_notes(riga, [Note(pos=0, length=24)], create=True)
    check('note per nome di drum sulla clip nuova',
          len(S.read_notes(riga)) == 1)
    check("scrivere la nota non ha aggiunto righe: c'erano gia' tutte",
          len(S.note_rows(clip)) == n_righe_prima, n_righe_prima)

    # e un preset di synth resta soundParams
    if (REFS / 'synths' / 'TEMPL.XML').exists():
        d2 = parse_file(base)
        i2, c2 = C.add_track(d2, REFS / 'synths' / 'TEMPL.XML',
                             name='TEMPL', folder='SYNTHS')
        check('un preset di synth porta soundParams',
              c2.find('soundParams') is not None
              and c2.find('kitParams') is None
              and not c2.has('affectEntire'))

    # il controllo non deve accusare cio' che ha scritto il dispositivo
    sporchi = []
    for b in (ROOT / 'refs' / 'songs', ROOT / 'corpus_versions'):
        for q in sorted(b.rglob('*.XML')):
            try:
                d = parse_file(q)
            except Exception:                            # noqa: BLE001
                continue
            if S.check_clip_types(d):
                sporchi.append(q.name)
    check(f'zero falsi positivi sui file del dispositivo',
          not sporchi, f'{len(sporchi)}: {sporchi[:3]}')


def test_kit_righe_precreate():
    """Una clip di kit appena creata ha una riga per drum, non zero righe.

    E' il difetto trovato dalla prova d'accettazione: add_track() da un
    preset di kit non metteva NESSUNA noteRow. Chi poi aggiungeva note coi
    propri drumIndex (per esempio 2, 6, 13) otteneva indici non contigui da
    0, e musica.verifica() -- il cancello che blocca il caricamento -- li
    rifiuta. Misurato sul corpus: 395 clip di kit su 395 hanno drumIndex
    contigui da 0, e 393 su 395 hanno esattamente una riga per drum.
    """
    from delugexml import create as C                    # noqa: PLC0415
    from delugexml import musica as MU                    # noqa: PLC0415

    preset = REFS / 'kits' / 'CR78FROMMARS.XML'
    base = REFS / 'songs' / 'ARR0.XML'
    if not (preset.exists() and base.exists()):
        salta('preset di kit per righe precreate', 'file assenti')
        return

    doc = parse_file(base)
    inst, clip = C.add_track(doc, preset, name='CR78FROMMARS', folder='KITS')
    n_drum = len(S.drums(inst))
    righe = S.note_rows(clip)
    idx = sorted(int(r.get('drumIndex')) for r in righe if r.has('drumIndex'))

    check('una riga per ogni drum del kit, non zero',
          len(righe) == n_drum > 0, f'{len(righe)} righe, {n_drum} drum')
    check('gli indici sono contigui da 0', idx == list(range(n_drum)), idx)
    check('nessuna riga porta soundParams: non serve per caricare '
          '(FINDINGS.md, 6-quinquies, verificato sul dispositivo)',
          all(r.find('soundParams') is None for r in righe))
    check('la clip appena creata passa il cancello di verifica()',
          not MU.verifica(doc), MU.verifica(doc)[:3])

    # si scrive su un drum scelto per nome senza aggiungere righe: gia ci sono
    n_prima = len(S.note_rows(clip))
    riga = S.drum_row(doc, clip, 'Kick CR78 12')
    S.write_notes(riga, [Note(pos=0, length=24)], create=True)
    check('scrivere per nome di drum non ha aggiunto righe',
          len(S.note_rows(clip)) == n_prima, n_prima)
    check('e la nota si legge dalla riga giusta',
          len(S.read_notes(riga)) == 1)

    # una traccia di synth, nello stesso punto del codice, non guadagna righe
    if (REFS / 'synths' / 'TEMPL.XML').exists():
        d2 = parse_file(base)
        _, c2 = C.add_track(d2, REFS / 'synths' / 'TEMPL.XML',
                            name='TEMPL', folder='SYNTHS')
        check('una clip di synth appena creata non ha noteRows: il fix non '
              'la tocca',
              c2.find('noteRows') is None, [x.tag for x in c2.children])


def test_kit_righe_scansione_corpus():
    """La stessa verifica, ripetuta su OGNI kit del corpus, non su uno solo.

    Avvertenza del progetto: guardare solo dove si sa gia' che e' giusto ha
    gia' lasciato passare due file che il dispositivo ha rifiutato, uno con
    un crash. Qui si scansiona: ogni <kit> trovato in refs/songs e
    corpus_versions viene riusato come se fosse un preset (241 nel corpus
    alla data di scrittura), e la clip che add_track() ne ricava deve avere
    una riga per drum, indici contigui da 0, e passare musica.verifica().

    Un kit copiato da un'altra song porta anche clipInstances/trackInstances,
    che descrivono l'arrangiamento di QUELLA song: non hanno senso nella song
    di base usata qui, e vanno tolti prima -- altrimenti arranger.check()
    troverebbe un problema che non e' quello misurato da questo test. Un vero
    file di preset (KITS/*.XML) non li porta mai: verificato sui 3 in
    refs/kits, nessuno dei quali ha ne' l'uno ne' l'altro attributo.
    """
    from delugexml import create as C                    # noqa: PLC0415
    from delugexml import musica as MU                    # noqa: PLC0415
    from delugexml import Document                        # noqa: PLC0415

    base = REFS / 'songs' / 'ARR0.XML'
    if not base.exists():
        salta('ARR0 come base per la scansione', 'assente')
        return

    scanned = 0
    rotti = []
    for cartella in (REFS / 'songs', ROOT / 'corpus_versions'):
        for p in sorted(cartella.rglob('*.XML')):
            try:
                d = parse_file(p)
            except Exception:                             # noqa: BLE001
                continue
            for strumento in S.instruments(d):
                if strumento.tag != 'kit':
                    continue
                n_drum = len(S.drums(strumento))
                if n_drum == 0:
                    continue
                scanned += 1
                kit_copy = strumento.copy_detached()
                kit_copy.attrs = [(k, v) for k, v in kit_copy.attrs
                                  if k not in ('clipInstances', 'trackInstances')]
                preset_doc = Document(roots=[kit_copy])
                newdoc = parse_file(base)
                try:
                    inst, clip = C.add_track(newdoc, preset_doc,
                                             name='SCANSIONE', folder='KITS')
                except Exception as e:                    # noqa: BLE001
                    rotti.append(f'{p.name}: eccezione {type(e).__name__}: {e}')
                    continue
                righe = S.note_rows(clip)
                idx = sorted(int(r.get('drumIndex')) for r in righe
                            if r.has('drumIndex'))
                if idx != list(range(n_drum)):
                    rotti.append(f'{p.name}: indici {idx[:5]} contro '
                                f'{n_drum} drum')
                    continue
                problemi = MU.verifica(newdoc)
                if problemi:
                    rotti.append(f'{p.name}: {problemi[0]}')

    check(f'kit scansionati dal corpus ({scanned})', scanned > 200, scanned)
    check('ognuno produce una clip con righe complete e valide',
          not rotti, f'{len(rotti)} rotti, es: {rotti[:3]}')


def test_notedata_vecchio():
    """`noteData`, il formato piu' vecchio, e' largo 10 byte e finisce li'.

    Regressione: `decode` leggeva `r[10]` (il byte di condition) sempre, e
    qualunque riga in quel formato faceva IndexError. Nel corpus sono 1850
    righe, e non erano mai state lette perche' nessun percorso ci passava
    finche' non e' arrivato il MIDI.
    """
    #      pos      length   vel lift   = 10 byte, 20 cifre, e finisce qui
    n = N.decode('0x00000000' '00000060' '40' '40', 10)
    check('una nota da 10 byte si legge', len(n) == 1 and n[0].pos == 0
          and n[0].length == 0x60, str(n))
    check('e la condition prende il default di 100%',
          n[0].condition == N.PROB_100, str(n[0].condition))

    # nessuna riga del corpus deve essere illeggibile
    righe = rotte = 0
    for base in (ROOT / 'refs' / 'songs', ROOT / 'corpus_versions'):
        for p in sorted(base.rglob('*.XML')):
            try:
                doc = parse_file(p)
            except Exception:                            # noqa: BLE001
                continue
            for _, c in S.clips(doc):
                for r in S.note_rows(c):
                    righe += 1
                    try:
                        S.read_notes(r)
                    except Exception:                    # noqa: BLE001
                        rotte += 1
    check(f'tutte le righe del corpus si leggono ({righe})', rotte == 0,
          f'{rotte} illeggibili')


def test_midi_cv():
    """MIDI e CV: strumenti senza figli, tutto il peso sulla clip."""
    from delugexml import midicv as M                    # noqa: PLC0415

    base = REFS / 'songs' / 'ARR0.XML'
    if not base.exists():
        salta('ARR0 per MIDI/CV', 'assente')
        return
    doc = parse_file(base)

    mi, mc = M.add_midi_track(doc, 1)
    ci, cc = M.add_cv_track(doc, 0, cv2_source=1)
    check('lo strumento MIDI non ha figli',
          mi.tag == 'midiChannel' and not mi.children)
    check('i canali sono 0-based nel file e 1-based sul display',
          M.label(mi) == 'MIDI 2' and M.label(ci) == 'CV 1',
          f'{M.label(mi)} / {M.label(ci)}')
    check('la clip non ha contenitore di parametri',
          mc.find('soundParams') is None and mc.find('kitParams') is None)
    check('ma ha arpeggiator, bendRange e columnControls come quelle del device',
          [x.tag for x in mc.children]
          == ['arpeggiator', 'bendRange', 'bendRangeMPE', 'columnControls'],
          [x.tag for x in mc.children])
    check('nessuna contraddizione di tipo', not S.check_clip_types(doc),
          S.check_clip_types(doc)[:2])

    # gli intervalli
    check('canale MIDI 16 rifiutato (0-15)',
          _raises(lambda: M.add_midi_track(doc, 16), ValueError))
    check('canale CV 2 rifiutato (il Deluge ha 2 uscite)',
          _raises(lambda: M.add_cv_track(doc, 2), ValueError))
    check('cv2Source fuori tabella rifiutato',
          _raises(lambda: M.add_cv_track(doc, 1, cv2_source=9), ValueError))

    # il conflitto di canale, che e' il caso che conta
    check('stesso canale E stesso suffisso rifiutato',
          _raises(lambda: M.add_midi_track(doc, 1), ValueError))
    mi2, _ = M.add_midi_track(doc, 1, suffix=0)
    check('ma con un suffisso diverso si puo, ed e un altro strumento',
          M.label(mi2) == 'MIDI 2A', M.label(mi2))
    check('e allora non e un conflitto', not M.check(doc), M.check(doc)[:2])

    # round-trip
    ri = parse(serialize(doc))
    check('si rilegge dopo la scrittura',
          len(M.tracks(ri, 'midi')) == 2 and len(M.tracks(ri, 'cv')) == 1)

    # e il controllo non accusa i file del dispositivo
    sporchi = []
    for b in (ROOT / 'refs' / 'songs', ROOT / 'corpus_versions'):
        for q in sorted(b.rglob('*.XML')):
            try:
                d = parse_file(q)
            except Exception:                            # noqa: BLE001
                continue
            if M.tracks(d) and M.check(d):
                sporchi.append(q.name)
    check('zero falsi positivi sulle 49 song con MIDI/CV',
          not sporchi, f'{len(sporchi)}: {sporchi[:3]}')


def _nodo_vuoto_templ():
    """La clip vuota di TEMPL0, da cui viene `create.CLIP_BASE`."""
    p = REFS / 'songs' / 'TEMPL0.XML'
    if not p.exists():
        return None
    doc = parse_file(p)
    for _, c in S.clips(doc):
        if not S.note_rows(c):
            return c
    return None


def _clip_midicv_bounce():
    """La clip CV di `Bounce.XML`, da cui vengono le costanti di midicv."""
    from delugexml import arranger as A                   # noqa: PLC0415

    p = REFS / 'songs' / 'Bounce.XML'
    if not p.exists():
        return None
    doc = parse_file(p)
    for da in (False, True):
        for c in A.clip_list(doc, da):
            if c.get('cvChannel') is not None or c.get('midiChannel') is not None:
                if any(x.tag == 'arpeggiator' for x in c.children):
                    return c
    return None


def test_costanti_catturate():
    """Ogni costante presa da un file del dispositivo deve ancora combaciare.

    E' il seguito del crash E365, dove una costante trascritta a mano da
    un'anteprima troncata aveva 11 attributi su 31 e valori inventati. Il file
    era XML valido, si rileggeva, passava ogni controllo semantico — nessuno
    di quei controlli puo' accorgersi di dati sbagliati che sembrano giusti.
    Solo il confronto col nodo originale puo'.

    Due classi, e vanno verificate diversamente:

    - **catture verbatim**: devono combaciare col nodo del dispositivo esatta-
      mente, valori e ordine. Un solo carattere diverso e' un difetto
    - **default scelti**: non copiano un nodo, scelgono un valore. La verifica
      sensata e' che quel valore il dispositivo lo scriva DAVVERO per quel tipo
      di nodo. E' cosi' che si e' scoperto che `isArmedForRecording="1"` sugli
      strumenti non esiste nel corpus: 0 su 356 <sound> e 0 su 241 <kit>
    """
    from delugexml import create as C                     # noqa: PLC0415
    from delugexml import midicv as M                     # noqa: PLC0415

    # ---------------------------------------------------- catture verbatim
    vuota = _nodo_vuoto_templ()
    if vuota is None:
        salta('TEMPL0 per CLIP_BASE', 'assente')
    else:
        d = dict(vuota.attrs)
        # `isPlaying` e' l'unica deroga voluta: una clip nuova nasce ferma
        diversi = {k: (v, d.get(k)) for k, v in C.CLIP_BASE.items()
                   if d.get(k) != v and k != 'isPlaying'}
        check('CLIP_BASE combacia con la clip vuota di TEMPL0',
              not diversi, str(diversi))
        check('CLIP_BASE non contiene attributi che dipendono dall istanza',
              not ({'instrumentPresetName', 'length', 'section', 'colourOffset',
                    'beingEdited'} & set(C.CLIP_BASE)))

    clip = _clip_midicv_bounce()
    if clip is None:
        salta('Bounce per le costanti di midicv', 'assente')
    else:
        arp = next(x for x in clip.children if x.tag == 'arpeggiator')
        dev = dict(arp.attrs)
        diff = {k: (M.ARPEGGIATOR_BASE.get(k, '(manca)'), dev.get(k, '(in piu)'))
                for k in set(dev) | set(M.ARPEGGIATOR_BASE)
                if dev.get(k) != M.ARPEGGIATOR_BASE.get(k)}
        check('ARPEGGIATOR_BASE: stessi valori del device',
              dev == M.ARPEGGIATOR_BASE,
              f'{len(M.ARPEGGIATOR_BASE)} voci contro {len(dev)}; '
              f'{dict(list(diff.items())[:4])}')
        check('ARPEGGIATOR_BASE: stesso ORDINE degli attributi',
              list(M.ARPEGGIATOR_BASE) == [k for k, _ in arp.attrs])
        br = tuple(x.text for x in clip.children
                   if x.tag.startswith('bendRange'))
        check('BEND_RANGE combacia', M.BEND_RANGE == br, f'{M.BEND_RANGE} vs {br}')
        cc = next(x for x in clip.children if x.tag == 'columnControls')
        mio = C._colonne_default()
        check('columnControls combacia',
              [(x.tag, list(x.attrs)) for x in mio.children]
              == [(x.tag, list(x.attrs)) for x in cc.children],
              f'{[(x.tag, dict(x.attrs)) for x in mio.children]}')

    # ---------------------------------------------------- default scelti
    from collections import Counter                       # noqa: PLC0415
    osservati: dict[tuple, Counter] = {}
    for base in (ROOT / 'refs' / 'songs', ROOT / 'corpus_versions'):
        for q in sorted(base.rglob('*.XML')):
            try:
                doc = parse_file(q)
            except Exception:                            # noqa: BLE001
                continue
            for i in S.instruments(doc):
                for k, v in i.attrs:
                    osservati.setdefault((i.tag, k), Counter())[v] += 1

    mai_visti = []
    for tag, cost in (('sound', C.ISTANZA_STRUMENTO),
                      ('midiChannel', M.ISTANZA_MIDI),
                      ('cvChannel', M.ISTANZA_CV)):
        for k, v in cost.items():
            visti = osservati.get((tag, k))
            if visti and v not in visti:
                mai_visti.append(
                    f'<{tag}> {k}={v!r}: il device scrive solo '
                    f'{sorted(visti, key=lambda x: -visti[x])[:3]}')
    check('nessun default e un valore che il device non scrive mai',
          not mai_visti, '; '.join(mai_visti[:3]))

    # e i due che erano sbagliati, esplicitamente
    visti_arm = osservati.get(('sound', 'isArmedForRecording'))
    if not visti_arm:
        salta('isArmedForRecording sugli strumenti',
              'serve il corpus per contare cosa scrive davvero il device')
    else:
        check('isArmedForRecording sugli strumenti e 0, come lo scrive il device',
              C.ISTANZA_STRUMENTO['isArmedForRecording'] == '0'
              and set(visti_arm) == {'0'}, str(dict(visti_arm)))


def test_audio_costanti():
    """Le costanti incorporate devono combaciare col file del dispositivo.

    Regressione di un crash (E365): `PARAMS_XML` era stato trascritto A MANO da
    un'anteprima troncata stampata a console, invece che dal nodo generato.
    Risultato: 11 attributi su 31, zero dei quattro figli, e alcuni valori
    inventati di sana pianta (`ratio="8"` per `1073741824`, `blend` per
    `compBlend`). Il file era XML valido, si rileggeva, passava ogni controllo
    — e il Deluge ci moriva sopra.

    Questo test confronta le costanti con il nodo vero, nodo per nodo. Una
    trascrizione a mano non puo' piu' passare inosservata.
    """
    from delugexml import audio as AU                     # noqa: PLC0415

    rif = REFS / 'songs' / 'Lfx.XML'
    if not rif.exists():
        salta('Lfx.XML come riferimento audio', 'assente')
        return
    doc = parse_file(rif)
    traccia = AU.tracks(doc)[0]
    params = AU.clips(doc)[0].find('params')

    def confronta(nome, mio, vero, salta=()):
        am = [(k, v) for k, v in mio.attrs if k not in salta]
        av = [(k, v) for k, v in vero.attrs if k not in salta]
        check(f'{nome}: stessi attributi e stessi valori', am == av,
              f'mio {len(am)} vs device {len(av)}; '
              f'diversi: {[k for k, _ in set(am) ^ set(av)][:4]}')
        check(f'{nome}: stessi figli',
              [c.tag for c in mio.children] == [c.tag for c in vero.children],
              f'{[c.tag for c in mio.children]} vs '
              f'{[c.tag for c in vero.children]}')
        for a, b in zip(mio.children, vero.children):
            check(f'{nome}/<{a.tag}>: stessi attributi',
                  list(a.attrs) == list(b.attrs),
                  f'{dict(a.attrs)} vs {dict(b.attrs)}')

    confronta('TRACCIA_XML', parse(AU.TRACCIA_XML).roots[0], traccia,
              salta=('name', 'clipInstances'))
    confronta('PARAMS_XML', parse(AU.PARAMS_XML).roots[0], params)


def test_audio():
    """Le clip audio: un riferimento a un file, non della musica."""
    from delugexml import audio as AU                     # noqa: PLC0415

    base = REFS / 'songs' / 'ARR0.XML'
    if not base.exists():
        salta('ARR0 per l audio', 'assente')
        return
    doc = parse_file(base)

    t = AU.add_audio_track(doc, input_channel='stereo')
    check('la traccia prende il primo nome libero', t.get('name') == 'AUDIO1',
          t.get('name'))
    check('e porta la catena effetti come quelle del device',
          [x.tag for x in t.children]
          == ['delay', 'sidechain', 'audioCompressor', 'stutter'],
          [x.tag for x in t.children])
    check('ingresso inventato rifiutato',
          _raises(lambda: AU.add_audio_track(doc, input_channel='usb'),
                  ValueError))
    check('nome duplicato rifiutato',
          _raises(lambda: AU.add_audio_track(doc, name='AUDIO1'), ValueError))

    # le posizioni si calcolano, non si indovinano
    c = AU.add_audio_clip(doc, t, 'SAMPLES/CLIPS/X.WAV', length=768)
    atteso = round(768 * S.samples_per_tick(doc.root))
    check('endSamplePos = start + length * campioni_per_tick',
          int(c.get('endSamplePos')) == atteso, f'{c.get("endSamplePos")} '
          f'contro {atteso}')
    check('il contenitore dei parametri e <params>',
          c.find('params') is not None and c.find('soundParams') is None)
    check('la clip risolve la sua traccia per nome',
          AU.track_of(doc, c) is t)
    check('nessun attributo scritto due volte',
          len({k for k, _ in c.attrs}) == len(c.attrs))

    # la clip vuota e' uno stato legittimo, non un difetto
    vuota = AU.add_audio_clip(doc, t, '', length=384)
    vuota.set('filePath', '')
    check('una clip senza campione e riconosciuta come vuota',
          AU.is_empty(vuota))
    check('e non viene segnalata come difetto', not AU.check(doc),
          AU.check(doc)[:2])

    ri = parse(serialize(doc))
    check('si rilegge dopo la scrittura',
          len(AU.tracks(ri)) == 1 and len(AU.clips(ri)) == 2)

    # nel corpus: clip vuote e endSamplePos=9999999 sono lo stesso insieme
    vuote = nove = 0
    sporchi = []
    for b in (ROOT / 'refs' / 'songs', ROOT / 'corpus_versions'):
        for q in sorted(b.rglob('*.XML')):
            try:
                d = parse_file(q)
            except Exception:                            # noqa: BLE001
                continue
            for cc in AU.clips(d):
                vuote += AU.is_empty(cc)
                nove += cc.get('endSamplePos') == '9999999'
            if (AU.tracks(d) or AU.clips(d)) and AU.check(d):
                sporchi.append(q.name)
    check(f'le clip vuote sono quelle con 9999999 ({vuote} e {nove})',
          vuote == nove and vuote > 0)
    check('zero falsi positivi sulle 40 song con audio',
          not sporchi, f'{len(sporchi)}: {sporchi[:3]}')


def test_arranger_ricodifica():
    """Ogni blob del corpus si riscrive identico a se stesso."""
    from delugexml import arranger as A                  # noqa: PLC0415
    from delugexml import song as S                      # noqa: PLC0415

    total = bad = 0
    esempi = []
    for base in (ROOT / 'refs' / 'songs', ROOT / 'corpus_versions'):
        for p in sorted(base.rglob('*.XML')):
            try:
                doc = parse_file(p)
            except Exception:                            # noqa: BLE001
                continue
            for strumento in S.instruments(doc):
                a = A.attr_of(strumento)
                if a is None:
                    continue
                v = strumento.get(a)
                if len(v) <= 2:
                    continue
                total += 1
                if A.encode(A.decode(v)) != v.upper().replace('0X', '0x'):
                    bad += 1
                    if len(esempi) < 3:
                        esempi.append(p.name)
    check(f'ricodifica identica su tutti i blob d arranger ({total})',
          bad == 0, f'{bad} diversi: {esempi}')


def test_musica_altezze():
    """Nomi di altezza italiani e inglesi verso i numeri MIDI.

    Convenzione: do4 = C4 = 60, quella MIDI standard. [OSS] da confrontare
    con cio' che mostra il display del Deluge.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    check('do4 e il do centrale', MU.altezza('do4') == 60)
    check('e C4 e lo stesso', MU.altezza('C4') == 60)
    check('re2 come nelle prove d arranger', MU.altezza('re2') == 38)
    check('fa#3', MU.altezza('fa#3') == 54)
    check('mib5 e un semitono sotto mi5', MU.altezza('mib5') == 75
          and MU.altezza('mi5') == 76)
    check('sib4 non e confuso con si4', MU.altezza('sib4') == 70
          and MU.altezza('si4') == 71)
    check('Bb4 in inglese e lo stesso', MU.altezza('Bb4') == 70)
    check('maiuscole e minuscole indifferenti',
          MU.altezza('LA3') == MU.altezza('la3'))
    check('un nome inventato viene rifiutato',
          _raises(lambda: MU.altezza('zolfo3'), ValueError))
    check('un ottava fuori scala viene rifiutata',
          _raises(lambda: MU.altezza('do99'), ValueError))

    # tutti i bemolle attaccati, non solo mib/sib sopra: il bug del
    # capitolato rompeva ogni nome italiano di 2-3 lettere piu' 'b' (non
    # solo 'si'), e il round-trip qui sotto non li tocca mai perche'
    # nome_altezza() produce solo diesis, mai bemolle.
    bemolle_attesi = {
        'dob4': 59, 'reb4': 61, 'fab4': 64, 'solb4': 66, 'lab4': 68,
        'cb4': 59, 'eb4': 63, 'gb4': 66, 'ab4': 68,
    }
    sbagliati_bemolle = [n for n, atteso in bemolle_attesi.items()
                          if MU.altezza(n) != atteso]
    check('tutti i bemolle italiani e inglesi restano corretti, non solo mib/sib',
          not sbagliati_bemolle, f'{sbagliati_bemolle}')

    # andata e ritorno su tutta l'estensione
    sbagliati = [m for m in range(128)
                 if MU.altezza(MU.nome_altezza(m)) != m]
    check('nome_altezza e altezza sono l una l inversa dell altra',
          not sbagliati, f'{len(sbagliati)} rotti: {sbagliati[:5]}')

    # [LACUNA revisione finale] CROMATICA_EN e nome_altezza(italiano=False)
    # non avevano NESSUN test e NESSUN chiamante: il round-trip qui sopra
    # passa SOLO per CROMATICA_IT (e' l'unica usata da nome_altezza() col
    # default), quindi un refuso in CROMATICA_EN sarebbe passato 452/452.
    check('nome_altezza inglese', MU.nome_altezza(60, italiano=False) == 'C4',
          MU.nome_altezza(60, italiano=False))
    check('e coi diesis', MU.nome_altezza(61, italiano=False) == 'C#4',
          MU.nome_altezza(61, italiano=False))
    check('e con l ottava negativa', MU.nome_altezza(0, italiano=False) == 'C-1',
          MU.nome_altezza(0, italiano=False))
    sbagliati_en = [m for m in range(128)
                    if MU.altezza(MU.nome_altezza(m, italiano=False)) != m]
    check('andata e ritorno anche sulla tabella inglese',
          not sbagliati_en, f'{len(sbagliati_en)} rotti: {sbagliati_en[:5]}')


def test_musica_ritmi():
    """Pattern a passi e melodie, verso le note della libreria.

    La stringa di passi mappa sulla griglia del Deluge: 16 colonne per
    battuta, quindi 24 tick per sedicesimo.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    check('un sedicesimo e 24 tick', MU.TICK_PER_PASSO == 24)
    check('16 passi fanno una battuta', 16 * MU.TICK_PER_PASSO == 384)

    kick = MU.passi('x...x...x...x...')
    check('quattro colpi sui movimenti', len(kick) == 4
          and [n.pos for n in kick] == [0, 96, 192, 288],
          str([n.pos for n in kick]))
    check('e durano un sedicesimo', all(n.length == 24 for n in kick))

    rim = MU.passi('....x.......x...')
    check('rim sul 2 e sul 4', [n.pos for n in rim] == [96, 288])

    acc = MU.passi('X...x...')
    check('la X e un accento', acc[0].velocity > acc[1].velocity,
          f'{acc[0].velocity} contro {acc[1].velocity}')

    # 'o' era il carattere estraneo di questo test finche' non e' diventato
    # il colpo fantasma (16 agosto 2026, vedi test_passi_tre_livelli).
    check('un carattere estraneo viene rifiutato',
          _raises(lambda: MU.passi('x..q'), ValueError))
    check('una lunghezza che non e multiplo di 16 viene rifiutata',
          _raises(lambda: MU.passi('x...x'), ValueError))

    check('durata_in_tick: 1/8 e mezza pulsazione',
          MU.durata_in_tick('1/8') == 48)
    check('durata_in_tick: 1/4 e una pulsazione',
          MU.durata_in_tick('1/4') == 96)
    check('durata_in_tick: 1/1 e una battuta',
          MU.durata_in_tick('1/1') == 384)

    mel = MU.melodia('re2 fa#2 la2 re3', durata='1/8')
    check('quattro altezze diverse, una riga ciascuna', len(mel) == 4)
    check('sono le altezze giuste',
          sorted(mel) == [38, 42, 45, 50], str(sorted(mel)))
    pos = sorted(n.pos for note in mel.values() for n in note)
    check('a passo di croma', pos == [0, 48, 96, 144], str(pos))

    ripetuta = MU.melodia('re2 re2', durata='1/4')
    check('la stessa altezza due volte finisce in UNA riga con due note',
          len(ripetuta) == 1 and len(ripetuta[38]) == 2,
          str({k: len(v) for k, v in ripetuta.items()}))

    check('una pausa salta il posto',
          [n.pos for n in MU.melodia('re2 . re2', durata='1/4')[38]]
          == [0, 192])

    # [LACUNA revisione finale] da= non aveva nessun test: e' come si mette
    # un pattern piu' avanti nella battuta, non un parametro esotico.
    spostato = MU.passi('x...', da=100)
    check('da sposta l origine del pattern in passi()',
          [n.pos for n in spostato] == [100], str([n.pos for n in spostato]))

    mel_da = MU.melodia('do4', durata='1/4', da=200)
    check('da sposta l origine anche in melodia()',
          mel_da[60][0].pos == 200, str(mel_da[60][0].pos))

    # [RINOMINATO revisione finale] passi() aveva un parametro `durata` che
    # NON passava da durata_in_tick() -- a differenza di quello omonimo in
    # melodia()/accordi() -- ed era gia' in tick grezzi: chi imparava
    # l'idioma di melodia() e lo applicava a passi() si trovava una stringa
    # '1/8' infilata in Note.length, che esplodeva molto piu' tardi con un
    # AttributeError lontano dalla causa. Rinominato in `lunghezza`, e ora
    # una stringa li' dentro viene rifiutata subito.
    con_lunghezza = MU.passi('x...', lunghezza=12)
    check('lunghezza e gia in tick grezzi, non passa da durata_in_tick()',
          all(n.length == 12 for n in con_lunghezza),
          str([n.length for n in con_lunghezza]))
    check('una stringa in lunghezza viene rifiutata subito, non esplode '
          'piu tardi scrivendo il file',
          _raises(lambda: MU.passi('x...', lunghezza='1/8'), ValueError))


def test_musica_accordi():
    """Un accordo suona le note INSIEME; melodia() le mette in sequenza.

    [LACUNA capitolato, prova d'accettazione finale] chiesto un piano,
    scrivere 're3 fa3 la3' con melodia() sparpaglia la triade su tre
    battute separate invece di suonarla come accordo -- vedi il rapporto
    fix-accordi-report.md. accordi() prende una PROGRESSIONE, i gruppi
    separati da '|': serve l'accompagnamento intero in una riga sola, non
    un accordo isolato. Un test che guardasse solo il conteggio delle note
    non si accorgerebbe della differenza fra "tre note insieme" e "tre
    note in sequenza" -- il conteggio e' identico -- quindi qui si
    controllano le POSIZIONI, non solo quante sono.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    triade = MU.accordi('re3 fa3 la3', durata='1/4')
    check('tre altezze diverse, una riga ciascuna',
          sorted(triade) == [50, 53, 57], str(sorted(triade)))
    posizioni = {n.pos for note in triade.values() for n in note}
    check('tutte e tre le note stanno ALLA STESSA posizione: e un accordo, '
          'non una melodia',
          posizioni == {0}, str(posizioni))

    passo = MU.durata_in_tick('1/4')
    prog = MU.accordi('re3 fa3 la3 | sib3 re4 fa4', durata='1/4')
    check('sei altezze in totale, due triadi distinte',
          sorted(prog) == sorted([50, 53, 57, 58, 62, 65]), str(sorted(prog)))
    primo = {n.pos for y in (50, 53, 57) for n in prog[y]}
    secondo = {n.pos for y in (58, 62, 65) for n in prog[y]}
    check('il primo accordo e a pos 0', primo == {0}, str(primo))
    check('il secondo accordo e un passo dopo: e una PROGRESSIONE, non un '
          'unico accordo enorme',
          secondo == {passo}, str(secondo))

    ripetuta = MU.accordi('do3 do3', durata='1/4')
    check('la stessa altezza due volte nello stesso accordo finisce in UNA '
          'riga con due note',
          len(ripetuta) == 1 and len(ripetuta[48]) == 2,
          str({k: len(v) for k, v in ripetuta.items()}))

    con_pausa = MU.accordi('do3 | . | mi3', durata='1/4')
    tutte_pos = sorted(n.pos for note in con_pausa.values() for n in note)
    check('una pausa nella progressione salta il passo senza produrre note',
          tutte_pos == [0, 2 * passo], str(tutte_pos))

    legato = MU.accordi('do3 mi3', durata='1/4', articolazione='legato')
    check('articolazione e durata si comportano come in melodia()',
          legato[48][0].length == passo, str(legato[48][0].length))
    esplicito = MU.accordi('do3 mi3', durata='1/4', stacco=10)
    check('stacco esplicito vince sull articolazione, come in melodia()',
          esplicito[48][0].length == passo - 10, str(esplicito[48][0].length))

    check('un nome sconosciuto dentro un accordo viene rifiutato',
          _raises(lambda: MU.accordi('do3 zzz3'), ValueError))
    check('un articolazione inventata viene rifiutata',
          _raises(lambda: MU.accordi('do3', articolazione='marcato'),
                  ValueError))
    check('una sequenza vuota viene rifiutata',
          _raises(lambda: MU.accordi(''), ValueError))

    # [LACUNA revisione finale] da= non aveva nessun test.
    acc_da = MU.accordi('do3 mi3', durata='1/4', da=300)
    posizioni_da = {n.pos for note in acc_da.values() for n in note}
    check('da sposta l origine anche in accordi()',
          posizioni_da == {300}, str(posizioni_da))


def test_musica_articolazioni():
    """L'articolazione e' vocabolario espressivo, non un default tecnico.

    'staccato'/'normale'/'legato' sono proporzioni del passo, non un numero
    fisso di tick: cosi' l'effetto resta lo stesso a qualunque tempo o
    durata, invece di essere impercettibile a un passo lento.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    passo = MU.durata_in_tick('1/4')

    legato = MU.melodia('do4', durata='1/4', articolazione='legato')
    check('legato dura quanto il passo, tocca la nota successiva',
          legato[60][0].length == passo, str(legato[60][0].length))

    staccato = MU.melodia('do4', durata='1/4', articolazione='staccato')
    normale = MU.melodia('do4', durata='1/4', articolazione='normale')
    check('staccato e piu corto di normale',
          staccato[60][0].length < normale[60][0].length,
          f'{staccato[60][0].length} contro {normale[60][0].length}')

    esplicito = MU.melodia('do4', durata='1/4', articolazione='legato',
                            stacco=10)
    check('uno stacco esplicito vince sull articolazione',
          esplicito[60][0].length == passo - 10,
          str(esplicito[60][0].length))

    check('un articolazione inventata viene rifiutata',
          _raises(lambda: MU.melodia('do4', articolazione='marcato'),
                  ValueError))


def test_musica_ingresso_sbagliato():
    """Le porte d'ingresso dello strato rifiutano con ValueError, non con
    AttributeError.

    [CORREZIONE revisione finale] Misurato: `altezza(60)`, `melodia(60)`,
    `passi(60)` e `accordi(60)` sollevavano tutti e quattro `AttributeError`
    ('int' object has no attribute 'strip'/'split'/'replace') invece di
    `ValueError`. Sono le porte d'ingresso dello strato: un chiamante che
    passa un intero per errore (es. confondendo un MIDI number con un nome)
    non e' un caso di laboratorio, e un'eccezione generica non dice cosa e'
    andato storto.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    for fn in (MU.altezza, MU.melodia, MU.passi, MU.accordi):
        check(f'{fn.__name__}(60) rifiuta con ValueError, non AttributeError',
              _raises(lambda fn=fn: fn(60), ValueError))

    # [CORREZIONE revisione finale] durata_in_tick() non validava la
    # positivita' quando riceveva gia' un intero -- solo il ramo stringa
    # controllava n > 0 e d > 0. Misurato: melodia('do4 re4 mi4 fa4',
    # durata=0) metteva TUTTE le note a pos 0 (una melodia diventa un
    # accordo, in silenzio) e durata=-48 dava posizioni 0, -48, -96 che
    # write_notes() accetta senza protestare -- una nota persa nel blob.
    # verifica() e avvertenze() sono cieche a entrambi i casi.
    check('durata_in_tick(0) e rifiutato', _raises(lambda: MU.durata_in_tick(0),
                                                    ValueError))
    check('durata_in_tick(-48) e rifiutato',
          _raises(lambda: MU.durata_in_tick(-48), ValueError))
    check('melodia(durata=0) non produce piu un accordo per sbaglio',
          _raises(lambda: MU.melodia('do4 re4 mi4 fa4', durata=0), ValueError))
    check('melodia(durata=-48) non produce piu posizioni negative',
          _raises(lambda: MU.melodia('do4 re4 mi4 fa4', durata=-48),
                  ValueError))
    # gli interi POSITIVI restano un modo legittimo di dare una durata gia'
    # in tick (vedi il docstring di durata_in_tick): non deve rompersi
    check('un intero positivo resta valido', MU.durata_in_tick(48) == 48)


def test_musica_verifica():
    """Il cancello: nessun file sale sul Deluge se non passa.

    Ferma il caso "soundParams su una clip di kit" (FINDINGS.md sezione
    6-quater): la clip si dichiara synth e mostra righe indicizzate per
    drumIndex, e il Deluge rifiuta l'intero file come corrotto.

    NON ferma l'altro file rifiutato dal dispositivo, il crash E365
    (sezione 6-quinquies, il <params> di una clip audio troncato da 31 a
    11 attributi con valori inventati): quello lo ferma la regola "mai
    trascrivere a mano" piu' test_audio_costanti, non un controllo
    semantico. Vedi il docstring di MU.verifica() per la misura e il
    perche' non si puo' allargare il cancello per coprirlo.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    # zero falsi positivi su tutto cio' che ha scritto il dispositivo
    sporchi = []
    n = 0
    for b in (ROOT / 'refs' / 'songs', ROOT / 'corpus_versions'):
        for q in sorted(b.rglob('*.XML')):
            try:
                d = parse_file(q)
            except Exception:                            # noqa: BLE001
                continue
            n += 1
            if MU.verifica(d):
                sporchi.append(f'{q.name}: {MU.verifica(d)[0]}')
    check(f'zero falsi positivi sui {n} file del dispositivo',
          not sporchi, '; '.join(sporchi[:2]))

    # e becca il difetto vero: una clip di kit che si dichiara synth
    doc = parse_file(REFS / 'songs' / 'ARR0.XML')
    from delugexml import create as C                     # noqa: PLC0415
    _, clip = C.add_track(doc, REFS / 'kits' / 'CR78FROMMARS.XML',
                          name='CR78FROMMARS', folder='KITS')
    check('un kit sano passa il cancello', not MU.verifica(doc),
          str(MU.verifica(doc)[:1]))
    kp = clip.find('kitParams')
    kp.tag = 'soundParams'
    kp.dirty = True
    problemi = MU.verifica(doc)
    check('e il cancello si chiude se la clip si contraddice',
          any('kit' in p and 'synth' in p for p in problemi),
          str(problemi[:2]))


def test_musica_verifica_non_ferma_params_audio_troncato():
    """CRITICO, misurato: verifica() NON vede un <params> audio troncato.

    Tre punti di questo progetto affermavano che verifica() "avrebbe
    fermato entrambi" i file rifiutati dal Deluge -- il tipo di clip
    contraddittorio (FINDINGS sezione 6-quater, che verifica() FERMA
    davvero, vedi il test sopra) e il crash E365 (sezione 6-quinquies, il
    <params> di una clip audio troncato da 31 a 11 attributi con valori
    inventati). Era falso per il secondo, e questo test lo misura invece
    di ripeterlo: riproduce la forma esatta del file del crash -- un
    <params> vero del corpus, tagliato da 31 a 11 attributi -- e verifica
    che ne' verifica() ne' avvertenze() se ne accorgano.

    Non e' un buco da chiudere allargando il controllo: delle 194 clip
    audio scritte dal dispositivo, 109 hanno esattamente 11 attributi nel
    loro <params> (11x109, 12x13, 14x1, 15x65, 16x2, 31x3, 32x1) -- un
    controllo di completezza accuserebbe 190 file su 194 sani. Quello che
    ferma davvero questo caso e' la regola "mai trascrivere a mano" piu'
    test_audio_costanti, non un controllo semantico su verifica().
    """
    from delugexml import musica as MU                    # noqa: PLC0415
    from delugexml import audio as AU                     # noqa: PLC0415

    doc = None
    clip_con_params = None
    for p in sorted((REFS / 'songs').glob('*.XML')):
        d = parse_file(p)
        for c in AU.clips(d):
            params = c.find('params')
            if params is not None and len(params.attrs) == 31:
                doc, clip_con_params = d, c
                break
        if doc is not None:
            break
    if doc is None:
        salta('clip audio con <params> completo (31)',
              'serve una song del corpus che ne contenga una')
        return
    check('esiste nel corpus fidato una clip audio con params completo (31)',
          True)

    check('prima del taglio, il file e sano',
          not MU.verifica(doc) and not MU.avvertenze(doc))

    params = clip_con_params.find('params')
    params.attrs = params.attrs[:11]
    params.children = []
    params.dirty = True

    check('un <params> troncato da 31 a 11 attributi non ferma verifica()',
          not MU.verifica(doc), str(MU.verifica(doc)[:2]))
    check('e nemmeno avvertenze() se ne accorge',
          not MU.avvertenze(doc), str(MU.avvertenze(doc)[:2]))
    check('audio.check() da solo non lo vede neanche lui: struttura sempre '
          'valida, solo incompleta',
          not AU.check(doc), str(AU.check(doc)[:2]))


def test_musica_avvertenze():
    """avvertenze() informa, verifica() blocca: due livelli, non uno.

    `Recordedzoom.XML` e' uno dei file trovati indagando il cancello: due
    clip di kit distinte, entrambe legate senza ambiguita' allo stesso
    <kit>, nella stessa sezione. Il dispositivo lo scrive cosi' lui stesso
    (FINDINGS.md: 91 sezioni cosi' nel corpus, "legale ma degradato") quindi
    non deve bloccare l'upload -- ma chi genera una song deve saperlo.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    sporco = parse_file(ROOT / 'corpus_versions' / '3.0.0-beta' / 'Recordedzoom.XML')
    avv = MU.avvertenze(sporco)
    check('avvertenze segnala il conflitto di sezione noto',
          any('sezione' in a and 'stesso strumento' in a for a in avv),
          str(avv[:2]))
    check('ma verifica() non si chiude per questo: non e un rifiuto',
          not MU.verifica(sporco), str(MU.verifica(sporco)[:1]))

    sano = parse_file(REFS / 'songs' / 'ARR0.XML')
    check('un file sano non ha avvertenze', not MU.avvertenze(sano),
          str(MU.avvertenze(sano)[:1]))


def test_song_notes_beyond_clip_end():
    """Note oltre la fine della clip: caricano, non suonano, e nessuno lo diceva.

    [LACUNA capitolato, prova d'accettazione finale] una progressione di
    accordi (o una melodia) piu' lunga della clip che la ospita resta un
    file valido -- il dispositivo lo carica senza protestare -- ma le note
    oltre la fine restano mute in silenzio, senza un solo avviso. Stessa
    famiglia di yScrollSongView: contenuto presente e inudibile. Va in
    avvertenze(), non in verifica(): non e' un motivo di rifiuto.

    Misurato PRIMA di scrivere il controllo (vedi fix-accordi-report.md):
    sui 139 file scritti dal dispositivo (refs/songs + corpus_versions, 36
    + 103) un controllo che guarda solo clip.length trova 254 "note fuori"
    in 22 file -- ma stanno TUTTE dentro una noteRow con un `length`
    PROPRIO, piu' lungo di quello della clip (il poliritmo di cui parla
    HANDOFF.md sezione 7): non sono affatto mute, suonano nel raggio della
    propria riga. E' esattamente il genere di trappola gia' costato caro
    due volte in questo progetto -- un controllo nuovo che accusa file
    sani. Il controllo giusto guarda la lunghezza EFFETTIVA, clip o riga
    (la maggiore delle due): con quella, zero casi sui 139 file.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    # --- zero falsi positivi sul corpus reale -----------------------------
    sporchi = []
    n = 0
    for base in (ROOT / 'refs' / 'songs', ROOT / 'corpus_versions'):
        for q in sorted(base.rglob('*.XML')):
            try:
                d = parse_file(q)
            except Exception:                            # noqa: BLE001
                continue
            n += 1
            trovati = S.notes_beyond_clip_end(d)
            if trovati:
                sporchi.append(f'{q.name}: {trovati[0]}')
    check(f'zero falsi positivi sui {n} file del dispositivo', not sporchi,
          '; '.join(sporchi[:2]))

    # --- vero positivo: una nota davvero oltre la fine ---------------------
    # in una riga SENZA un length proprio che la giustifichi
    doc = parse_file(REFS / 'songs' / 'ARR0.XML')
    clip = [c for _, c in S.clips(doc) if c.tag != 'audioClip'][0]
    lunghezza = int(clip.get('length'))
    riga = S.add_note_row(clip, 90)
    S.write_notes(riga, [Note(pos=0, length=48),
                         Note(pos=lunghezza, length=48)], create=True)
    avvisi = S.notes_beyond_clip_end(doc)
    check('la nota oltre la fine viene segnalata', len(avvisi) == 1, str(avvisi))
    check('l avviso dice quale clip, quale riga e quante note',
          S.clip_label(clip) in avvisi[0] and 'y=90' in avvisi[0]
          and '1 note' in avvisi[0],
          avvisi[0] if avvisi else '(nessun avviso)')
    check('e arriva anche da avvertenze()',
          any('y=90' in a for a in MU.avvertenze(doc)), str(MU.avvertenze(doc)))
    check('ma non chiude verifica(): non e un motivo di rifiuto',
          not MU.verifica(doc), str(MU.verifica(doc)[:1]))

    # --- la nuance che ha gia' fregato due controlli: il length di riga ---
    # una riga con un length PROPRIO piu' lungo della clip non e' un falso
    # positivo, anche se la nota supera clip.length (poliritmo, HANDOFF s.7)
    doc2 = parse_file(REFS / 'songs' / 'ARR0.XML')
    clip2 = [c for _, c in S.clips(doc2) if c.tag != 'audioClip'][0]
    lunghezza2 = int(clip2.get('length'))
    riga2 = S.add_note_row(clip2, 91)
    riga2.set('length', str(lunghezza2 * 2))
    S.write_notes(riga2, [Note(pos=lunghezza2, length=48)], create=True)
    check('una nota oltre clip.length ma dentro il length PROPRIO della '
          'riga non e un falso positivo',
          not S.notes_beyond_clip_end(doc2), str(S.notes_beyond_clip_end(doc2)))


def test_musica_mutazione():
    """Il cancello deve avere i denti: se non fallisce mai, non protegge.

    Stessa disciplina di `test_costanti_catturate`: si guasta il documento
    di proposito e si pretende che il controllo giusto se ne accorga.

    [CORREZIONE capitolato] la bozza (task-6-brief.md) si aspettava che
    `MU.verifica()` vedesse anche il secondo caso qui sotto (due clip dello
    stesso strumento nella stessa scena). Non e' piu' vero dal task 3
    (commit 99299b8, `musica: separa avvertenze() dal cancello verifica()`):
    quel conflitto e' stato spostato in `MU.avvertenze()` perche' e' il
    dispositivo STESSO a scriverlo cosi' — 91 sezioni nel corpus, vedi
    `song.same_section_conflicts()` — e non causa un rifiuto del file. La
    riga e' corretta di conseguenza.

    [GIUDIZIO] Il caso non viene spostato in un test dedicato alle
    avvertenze: c'e' gia', `test_musica_avvertenze`, ma prova un file del
    corpus GIA' scritto cosi' dal dispositivo. Qui la clip nasce invece
    dall'API di questo progetto (`song.duplicate_clip`), che e' come un
    documento nasce qui — quindi non e' un doppione, prova che un documento
    APPENA mutato da noi riceve lo stesso trattamento di uno ereditato dal
    dispositivo. E prova la meta' che nessun altro test prova: che
    `verifica()` resta ZITTA su un caso che sa non essere un rifiuto — un
    cancello che urlasse anche qui bloccherebbe file legittimi, lo stesso
    difetto di un cancello che non urla mai.
    """
    from delugexml import musica as MU                    # noqa: PLC0415
    import delugexml                                       # noqa: PLC0415

    # l'esportazione va provata A FREDDO. Nello stesso processo di questa
    # suite altri test (es. test_musica_altezze, alfabeticamente prima di
    # questo) fanno gia' `from delugexml import musica`: quella sola riga
    # aggancia l'attributo `musica` a `delugexml` come effetto collaterale
    # del meccanismo di import di Python, ANCHE quando __init__.py non lo fa
    # -- verificato spegnendo l'export e osservando che un hasattr() diretto
    # qui dentro risulta comunque vero, per contaminazione dall'ordine dei
    # test. Un interprete nuovo, senza quella contaminazione, e' l'unico modo
    # onesto di provare l'export.
    import subprocess                                      # noqa: PLC0415
    import os                                              # noqa: PLC0415
    codice = ("import delugexml, sys\n"
             "sys.exit(0 if hasattr(delugexml, 'musica') else 1)")
    ambiente = dict(os.environ, PYTHONPATH=str(ROOT / 'tools'))
    esito = subprocess.run([sys.executable, '-c', codice], env=ambiente)
    check('musica e esportato dal package (interprete a freddo)',
          esito.returncode == 0, f'exit code {esito.returncode}')

    doc = parse_file(REFS / 'songs' / 'Aolac.XML')
    check('la song di partenza e sana', not MU.verifica(doc))

    # 1. un indice d'arranger che punta oltre la fine
    from delugexml import arranger as A                   # noqa: PLC0415
    guasto = False
    for st in S.instruments(doc):
        ists = A.instances(st)
        if ists:
            A.set_instances(st, [A.Istanza(pos=i.pos, length=i.length,
                                           code=999) for i in ists])
            guasto = True
            break
    check('Aolac.XML ha un arrangiamento da guastare', guasto)
    problemi = MU.verifica(doc)
    check('un indice di clip inesistente viene visto',
          any('999' in p for p in problemi), str(problemi[:1]))

    # 2. due clip dello stesso strumento nella stessa scena: legale — lo
    # scrive il dispositivo stesso — quindi va in avvertenze(), non in
    # verifica(). [CORREZIONE capitolato, vedi sopra]
    d2 = parse_file(REFS / 'songs' / 'Aolac.XML')
    prima = d2.root.find('sessionClips').children[0]
    sezione = prima.get('section')
    check('la prima clip di Aolac ha una sezione da riusare',
          sezione is not None)
    # guardia di sanita' PRIMA di guastare, stessa disciplina del primo caso:
    # senza sapere che d2 parte pulito, "verifica() resta vuota" e
    # "avvertenze() vede il conflitto" dopo la mutazione direbbero meno --
    # potrebbero essere vuota/piena gia' in partenza, per un motivo che non
    # e' la mutazione appena fatta.
    # Aolac porta gia' delle avvertenze sue (clip in modalita' a scala con la
    # vista scrollata altrove, che il dispositivo salva legittimamente), quindi
    # la guardia registra cio' che c'e' PRIMA invece di pretendere il vuoto:
    # cio' che conta e' che il conflitto di sezione non ci sia ancora.
    avv_prima = set(MU.avvertenze(d2))
    check('anche d2 e sano prima di guastarlo (nessun conflitto di sezione)',
          not MU.verifica(d2)
          and not [a for a in avv_prima if 'sezione' in a or 'section' in a],
          f'{MU.verifica(d2)[:1]} / {sorted(avv_prima)[:1]}')
    S.duplicate_clip(d2, 0, section=sezione)
    check('due clip dello stesso strumento in una scena non bloccano '
          'il caricamento',
          not MU.verifica(d2), str(MU.verifica(d2)[:1]))
    check('...ma vengono viste da avvertenze()',
          any('stesso strumento' in a for a in MU.avvertenze(d2)),
          str(MU.avvertenze(d2)[:1]))


def test_musica_verifica_cablaggio():
    """Il cancello ha i denti su ognuna delle sue sorgenti, non solo su una.

    `test_musica_verifica` prova gia' un vero positivo per
    `check_clip_types()`. Le altre quattro sorgenti di `verifica()` erano
    esercitate solo dalla scansione "zero falsi positivi", che dimostra
    l'assenza di rumore ma non che il cablaggio funzioni: se una riga
    perdesse il valore di ritorno o chiamasse il modulo sbagliato, quella
    scansione non se ne accorgerebbe. Qui si guasta di proposito un
    riferimento d'arranger (stesso schema di `test_musica_mutazione`,
    previsto per il task 6) e si pretende che `verifica()` lo veda.
    """
    from delugexml import musica as MU                    # noqa: PLC0415
    from delugexml import arranger as A                    # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Aolac.XML')
    check('la song di partenza e sana', not MU.verifica(doc))

    guasto = False
    for st in S.instruments(doc):
        ists = A.instances(st)
        if ists:
            A.set_instances(st, [A.Istanza(pos=i.pos, length=i.length,
                                           code=999) for i in ists])
            guasto = True
            break
    check('Aolac.XML ha un arrangiamento da guastare', guasto)

    problemi = MU.verifica(doc)
    check('un indice d arranger fuori range viene visto dal cancello',
          any('999' in p for p in problemi), str(problemi[:1]))


def test_musica_racconta():
    """Il racconto in termini musicali: e' cio' che rende correggibile il lavoro.

    Una modifica di cui non si sa dire cosa ha fatto non e' correggibile a
    parole, e il ciclo «proponi e io correggo» si spezza.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Aolac.XML')
    testo = MU.racconta(doc)
    check('il racconto dice il tempo',
          str(round(S.get_bpm(doc.root))) in testo, testo[:120])
    check('e la scala', S.scale_name(doc).split()[0].lower() in testo.lower(),
          S.scale_name(doc))
    check('e nomina gli strumenti',
          'ADDITIVE' in testo and 'KIT008' in testo)
    check('e conta le istanze d arranger', 'battut' in testo.lower())
    check('non contiene XML', '<' not in testo and '0x' not in testo,
          [r for r in testo.splitlines() if '<' in r or '0x' in r][:2])

    # le note escono come nomi, non come numeri
    d2 = parse_file(REFS / 'songs' / 'ARR0.XML')
    clip = d2.root.find('sessionClips').children[0]
    S.write_notes(S.add_note_row(clip, 38), [Note(pos=0, length=88)],
                  create=True)
    r = MU.racconta_clip(d2, clip)
    check('un re2 e raccontato come re2', 're2' in r, r)
    check('e non come 38', '38' not in r.replace('re2', ''), r)


def test_musica_racconta_corpus():
    """racconta() su tutto il corpus, non solo sui due file scelti a mano.

    La revisione ha trovato due difetti critici -- un nome di strumento
    MIDI/CV che rientrava come frammento di XML letterale, un'altezza fuori
    0-127 che faceva esplodere racconta_clip() -- che ne' Aolac.XML ne'
    ARR0.XML, i soli file usati da test_musica_racconta, riescono a
    innescare. Qui si scansiona l'intero refs/songs/, come indicato in
    revisione: e' la scansione che avrebbe trovato da sola entrambi.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    rotti = []
    sporchi = []
    for q in sorted((REFS / 'songs').glob('*.XML')):
        d = parse_file(q)
        try:
            testo = MU.racconta(d)
        except Exception as e:                             # noqa: BLE001
            rotti.append(f'{q.name}: {type(e).__name__}: {e}')
            continue
        righe_sporche = [r for r in testo.splitlines()
                         if '<' in r or '0x' in r]
        if righe_sporche:
            sporchi.append(f'{q.name}: {righe_sporche[0]}')
    check('nessun file del corpus fa esplodere racconta()', not rotti,
          rotti[:3])
    check('nessun racconto del corpus contiene XML o esadecimale',
          not sporchi, sporchi[:3])


def test_musica_racconta_clip_audio():
    """Una clip audio con un campione non e' mai raccontata "vuota".

    [BUG capitolato] la bozza non distingueva le audioClip dalle clip di
    strumento: senza noteRow (le audioClip non ne hanno mai) finivano
    descritte "(vuota)" anche portando un campione vero. Chi legge "vuota"
    per decidere se riusare uno slot rischia di perdere in silenzio un
    campione messo a mano dall'utente -- proprio cio' che "raccontare prima
    di toccare" esiste per evitare.
    """
    from delugexml import musica as MU                    # noqa: PLC0415
    from delugexml import audio as AU                     # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Lfx.XML')
    trovata = False
    for clip in AU.clips(doc):
        if not AU.is_empty(clip):
            trovata = True
            r = MU.racconta_clip(doc, clip)
            check('il campione compare nel racconto',
                  clip.get('filePath') in r, r)
            check('e non e marcata vuota', 'vuota' not in r, r)
            break
    check('Lfx.XML ha una clip audio con campione da provare', trovata)


def test_musica_racconta_arrangiamento_distingue_pattern():
    """L'arrangiamento distingue QUALE pattern suona, non solo lo strumento.

    [BUG capitolato] la bozza ignorava la clip gia' in mano e stampava solo
    il nome dello strumento: in Aolac.XML BassGuitar alterna 3 pattern
    diversi (sezioni 0, 1, 2) per una quarantina di blocchi, e il racconto
    li rendeva tutti identici -- impossibile dire "nella seconda meta' usa
    il pattern piu' mosso".
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Aolac.XML')
    testo = MU.racconta(doc)
    righe = [r for r in testo.splitlines()
             if 'BassGuitar' in r and 'battuta' in r]
    check('BassGuitar compare piu volte nell arrangiamento', len(righe) > 1,
          len(righe))
    sezioni = {r.rsplit('sezione', 1)[-1] for r in righe if 'sezione' in r}
    check('e con piu di una sezione, cioe piu di un pattern',
          len(sezioni) > 1, sorted(sezioni))


def test_musica_verbi():
    """I verbi di suono: gusto dichiarato, non euristica nascosta.

    Ogni applicazione deve riferire QUALE parametro ha mosso e di quanto,
    altrimenti l'utente non puo' scavalcare la scelta.
    """
    from delugexml import musica as MU                    # noqa: PLC0415
    from delugexml import param_ids as PI                 # noqa: PLC0415
    from delugexml import sound as SN                     # noqa: PLC0415

    # `by_name` SOLLEVA per un nome ignoto, non restituisce None. Scansione
    # su TUTTE le voci di entrambe le tabelle (relativi e assoluti), non un
    # verbo scelto a mano.
    ignoti = []
    for parametro, _ in list(MU.VERBI_RELATIVI.values()) + \
            list(MU.VERBI_ASSOLUTI.values()):
        try:
            PI.by_name(parametro)
        except ValueError:
            ignoti.append(parametro)
    check('ogni verbo punta a un parametro che esiste in tabella',
          not ignoti, str(ignoti))

    doc = parse_file(REFS / 'songs' / 'ARR0.XML')
    clip = doc.root.find('sessionClips').children[0]
    prima = SN.get(clip, 'lpfFrequency')
    esito = MU.applica_verbo(doc, clip, 'piu scuro')
    dopo = SN.get(clip, 'lpfFrequency')
    check('«piu scuro» abbassa il taglio del filtro', dopo < prima,
          f'{prima} -> {dopo}')
    check('e riferisce parametro, prima e dopo',
          esito['parametro'] == 'lpfFrequency' and esito['prima'] == prima
          and esito['dopo'] == dopo, str(esito))

    check('«piu brillante» lo rialza',
          MU.applica_verbo(doc, clip, 'piu brillante')['dopo'] > dopo)

    check('il valore resta nella scala 0-50 (overshoot verso il basso)',
          all(0 <= MU.applica_verbo(doc, clip, 'piu scuro', forza=9)['dopo']
              <= 50 for _ in range(4)))

    # [REVISIONE] il test sopra dimostra solo il tetto BASSO: l'unica salita
    # ('piu brillante' da 42) arrivava esattamente a 50 (42+8), senza mai
    # superarlo -- sarebbe passato identico anche senza il min(50, ...). Qui
    # si parte da un valore noto e si forza un overshoot vero verso l'alto:
    # 40 + 8*9 = 112, ben oltre 50.
    SN.set(clip, 'lpfFrequency', 40)
    alto = MU.applica_verbo(doc, clip, 'piu brillante', forza=9)
    check('il tetto 50 e davvero applicato, non solo mai raggiunto per caso',
          alto['dopo'] == 50, str(alto))

    check('un verbo sconosciuto viene rifiutato dicendo quali esistono',
          _raises(lambda: MU.applica_verbo(doc, clip, 'piu blu'), ValueError))
    check('verbi_disponibili li elenca',
          'piu scuro' in MU.verbi_disponibili()
          and 'al centro' in MU.verbi_disponibili())

    # [REVISIONE] 'al centro' e' un verbo ASSOLUTO: non coperto da nessun
    # test nella prima consegna. Deve arrivare a 25 da entrambi i lati, e
    # 'forza' non deve alterare il risultato (non c'e' un "quanto").
    SN.set(clip, 'pan', 5)
    da_sinistra = MU.applica_verbo(doc, clip, 'al centro', forza=1)
    check('«al centro» porta pan a 25 da sinistra',
          da_sinistra['dopo'] == 25, str(da_sinistra))
    SN.set(clip, 'pan', 45)
    da_destra = MU.applica_verbo(doc, clip, 'al centro', forza=99)
    check('«al centro» porta pan a 25 da destra, forza alta ignorata',
          da_destra['dopo'] == 25, str(da_destra))


def test_musica_destinazione():
    """La destinazione sulla SD e' una sola: /SONGS/DelugePal/.

    Vincolo nato da un incidente reale: i file di prova delle sessioni
    precedenti si erano sparsi fra le 135 song personali dell'utente, che ha
    dovuto cancellarne 34 a mano. Il vincolo sta nel codice, non solo nella
    prosa della skill: un nome che tenta di uscire dalla cartella va
    RIFIUTATO, non ripulito in silenzio -- ripulirlo nasconderebbe l'errore
    di chi chiama.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    check('le quattro cartelle di primo livello sono quelle dichiarate',
          MU.CARTELLE_SD == ('SONGS', 'KITS', 'SYNTHS', 'SAMPLES'),
          MU.CARTELLE_SD)
    check('la sottocartella dedicata e DelugePal',
          MU.SOTTOCARTELLA == 'DelugePal', MU.SOTTOCARTELLA)

    check('il percorso comincia sempre con /SONGS/DelugePal (default)',
          MU.destinazione('house').startswith('/SONGS/DelugePal/'))
    check('nome maiuscolo, due cifre di versione, estensione .XML',
          MU.destinazione('house', 1) == '/SONGS/DelugePal/HOUSE01.XML',
          MU.destinazione('house', 1))
    check('la versione arriva sempre a due cifre',
          MU.destinazione('house', 7) == '/SONGS/DelugePal/HOUSE07.XML')

    check('un nome con / e rifiutato, non ripulito',
          _raises(lambda: MU.destinazione('sub/house'), ValueError))
    check('un nome con .. (anche senza slash) e rifiutato',
          _raises(lambda: MU.destinazione('ho..use'), ValueError))
    check('un nome con backslash e rifiutato',
          _raises(lambda: MU.destinazione('sub\\house'), ValueError))
    check('un tentativo esplicito di risalire la gerarchia e rifiutato',
          _raises(lambda: MU.destinazione('../evil'), ValueError))

    check('un nome vuoto e rifiutato',
          _raises(lambda: MU.destinazione(''), ValueError))
    check('un nome di soli spazi e rifiutato',
          _raises(lambda: MU.destinazione('   '), ValueError))

    check('versione 0 e rifiutata (non sta su due cifre)',
          _raises(lambda: MU.destinazione('house', 0), ValueError))
    check('versione negativa e rifiutata',
          _raises(lambda: MU.destinazione('house', -1), ValueError))
    check('versione 100 e rifiutata (andrebbe a tre cifre)',
          _raises(lambda: MU.destinazione('house', 100), ValueError))
    check('versione 99 e ancora accettata, al limite',
          MU.destinazione('house', 99) == '/SONGS/DelugePal/HOUSE99.XML')

    check('un nome che gia porta estensione .xml non la raddoppia',
          MU.destinazione('house.xml', 1) == '/SONGS/DelugePal/HOUSE01.XML',
          MU.destinazione('house.xml', 1))


def test_musica_destinazione_quattro_cartelle():
    """La scrittura e' confinata alla propria sottocartella in TUTTE E
    QUATTRO le cartelle di primo livello, non solo in SONGS.

    Estensione del vincolo del task precedente: Deluge Pal potra' dover
    scrivere anche kit, preset di synth e campioni, sempre nella stessa
    forma (`<CARTELLA>/DelugePal/...`). Ogni controllo qui sotto scansiona
    le quattro, non ne sceglie una a mano: e' il punto che rende la prova
    completa invece che un aneddoto su SONGS soltanto.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    check('ogni cartella scrive dentro <cartella>/DelugePal/',
          all(MU.destinazione('prova', 1, cartella=c)
              .startswith(f'/{c}/DelugePal/') for c in MU.CARTELLE_SD),
          {c: MU.destinazione('prova', 1, cartella=c) for c in MU.CARTELLE_SD})

    check('un nome con / e rifiutato in tutte e quattro',
          all(_raises(lambda c=c: MU.destinazione('sub/prova', cartella=c),
                       ValueError) for c in MU.CARTELLE_SD))
    check('un nome con .. e rifiutato in tutte e quattro',
          all(_raises(lambda c=c: MU.destinazione('pr..ova', cartella=c),
                       ValueError) for c in MU.CARTELLE_SD))
    check('un nome con backslash e rifiutato in tutte e quattro',
          all(_raises(lambda c=c: MU.destinazione('sub\\prova', cartella=c),
                       ValueError) for c in MU.CARTELLE_SD))

    check('una cartella inventata e rifiutata, dicendo quali esistono',
          _raises(lambda: MU.destinazione('prova', cartella='PATTERNS'),
                  ValueError))
    try:
        MU.destinazione('prova', cartella='PATTERNS')
        messaggio = ''
    except ValueError as e:
        messaggio = str(e)
    check('il messaggio elenca le quattro cartelle valide',
          all(c in messaggio for c in MU.CARTELLE_SD), messaggio)

    check('SONGS produce estensione .XML',
          MU.destinazione('house', 1, cartella='SONGS')
          == '/SONGS/DelugePal/HOUSE01.XML')
    check('KITS produce estensione .XML',
          MU.destinazione('808core', 1, cartella='KITS')
          == '/KITS/DelugePal/808CORE01.XML')
    check('SYNTHS produce estensione .XML',
          MU.destinazione('basso', 1, cartella='SYNTHS')
          == '/SYNTHS/DelugePal/BASSO01.XML')
    check('SAMPLES produce estensione .wav, non .XML',
          MU.destinazione('kick', 1, cartella='SAMPLES')
          == '/SAMPLES/DelugePal/kick01.wav',
          MU.destinazione('kick', 1, cartella='SAMPLES'))
    check('SAMPLES non forza le maiuscole (i .wav reali hanno case misto)',
          MU.destinazione('Kick_Punchy', 1, cartella='SAMPLES')
          == '/SAMPLES/DelugePal/Kick_Punchy01.wav',
          MU.destinazione('Kick_Punchy', 1, cartella='SAMPLES'))

    check('versione=None non aggiunge alcun suffisso (utile per un preset)',
          MU.destinazione('Basso Profondo', versione=None, cartella='SYNTHS')
          == '/SYNTHS/DelugePal/BASSO PROFONDO.XML',
          MU.destinazione('Basso Profondo', versione=None, cartella='SYNTHS'))
    check('versione=None funziona anche per un campione, senza suffisso ne errore',
          MU.destinazione('kick_808', versione=None, cartella='SAMPLES')
          == '/SAMPLES/DelugePal/kick_808.wav',
          MU.destinazione('kick_808', versione=None, cartella='SAMPLES'))


def test_musica_origine():
    """Il lato LETTURA e' l'opposto voluto del lato scrittura: non ristretto.

    `destinazione()` blocca la scrittura fuori da `<cartella>/DelugePal/`
    perche' scrivere li' e' quanto e' gia' costato una pulizia a mano di 34
    file sparsi fra le 135 song dell'utente. La lettura non condivide quel
    rischio -- leggere un file non lo altera -- e Deluge Pal deve poter
    partire da qualunque song, kit o campione GIA' esistente dell'utente:
    ristringerla nello stesso modo sarebbe un difetto nella direzione
    opposta, non una precauzione. Questo test dimostra che l'asimmetria e'
    REALE nel codice, non solo dichiarata in un docstring: prova percorsi
    che `destinazione()` rifiuterebbe e conferma che `origine()` non lo fa.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    check('legge una song personale, fuori da DelugePal',
          MU.origine('Antrop.XML', 'SONGS') == '/SONGS/Antrop.XML')
    check('legge un kit di fabbrica, cartella diversa da tutte le quattro',
          MU.origine('808 Essential.XML', 'KITS')
          == '/KITS/808 Essential.XML')
    check('legge un campione annidato in sottocartelle (come nel corpus reale)',
          MU.origine('Kick/RX-5 Kick.wav', 'SAMPLES/DRUMS')
          == '/SAMPLES/DRUMS/Kick/RX-5 Kick.wav')

    check('un percorso che destinazione() rifiuterebbe (../) non solleva qui',
          not _raises(lambda: MU.origine('../fuori.XML', 'SONGS'), ValueError))
    check('un nome con backslash non solleva in lettura',
          not _raises(lambda: MU.origine('sub\\prova.XML', 'SONGS'), ValueError))
    check('una "cartella" fuori da CARTELLE_SD e accettata in lettura',
          MU.origine('qualcosa.txt', 'SETTINGS') == '/SETTINGS/qualcosa.txt')

    check('solo il vuoto e rifiutato: nome vuoto',
          _raises(lambda: MU.origine('', 'SONGS'), ValueError))
    check('solo il vuoto e rifiutato: cartella vuota',
          _raises(lambda: MU.origine('song.XML', ''), ValueError))


def test_musica_destinazione_caratteri_illegali():
    """Trovato in revisione: `_VIETATI` bloccava i separatori ma non gli
    altri caratteri che FAT32/Windows non ammettono in un nome di file, ne'
    i caratteri di controllo. Non era un aggiramento del confine (il file
    restava comunque dentro DelugePal/), ma un nome cosi' fatto e' un nome
    che il Deluge avrebbe rifiutato comunque -- solo piu' tardi, con un
    errore meno leggibile. Verificato riproducendo il difetto sul codice
    del commit precedente (`git show HEAD~1:...`) prima di scrivere questo
    test: `destinazione('C:evil')` dava `'/SONGS/DelugePal/C:EVIL01.XML'`
    senza sollevare.

    Il Minor sull'estensione doppia, trovato nello stesso giro di
    revisione, ha un test dedicato: `test_musica_destinazione_estensione_nota`.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    # ogni carattere FAT32/Windows vietato, uno alla volta: non un test
    # che ne prova uno solo a caso.
    illegali = '<>:"|?*'
    falliti = [c for c in illegali
               if not _raises(lambda c=c: MU.destinazione(f'a{c}b'), ValueError)]
    check('ogni carattere FAT32/Windows vietato e rifiutato',
          not falliti, f'non rifiutati: {falliti!r}')

    check('il caso del revisore, C:evil, e ora rifiutato',
          _raises(lambda: MU.destinazione('C:evil'), ValueError))

    check('un carattere di controllo (tab) e rifiutato',
          _raises(lambda: MU.destinazione('a\tb'), ValueError))
    check('NUL e rifiutato',
          _raises(lambda: MU.destinazione('evil\x00name'), ValueError))

    check('i vietati FAT32 sono controllati anche nelle altre tre cartelle',
          all(_raises(lambda c=c: MU.destinazione('a|b', cartella=c), ValueError)
              for c in MU.CARTELLE_SD))

    # il messaggio deve nominare il carattere incriminato, non essere generico
    try:
        MU.destinazione('a*b')
        messaggio = ''
    except ValueError as e:
        messaggio = str(e)
    check('il messaggio nomina il carattere incriminato', '*' in messaggio,
          messaggio)


def test_musica_destinazione_estensione_nota():
    """Seconda revisione: la prima guardia sull'estensione doppia era essa
    stessa un difetto Important, del tipo "un test solo sul rifiuto ti
    avrebbe fatto passare anche questa volta".

    `_estensione_sospetta` (rimossa) trattava come estensione QUALUNQUE
    suffisso di 1-4 alfanumerici con almeno una lettera: rifiutava a torto
    nomi legittimi come 'Drum.V2', 'Bass.HD', 'Song.Live', 'Kick.Pro', col
    messaggio "porta gia' l'estensione '.V2'" -- falso, perche' '.V2' non
    e' un'estensione di niente. Il difetto e' stato riprodotto a mano sul
    codice del commit precedente prima di scrivere la correzione (fuori da
    questo file, per non appesantire la suite con operazioni di git/subprocess
    a ogni run): `destinazione('Drum.V2', cartella='SONGS')` sollevava
    davvero, col messaggio sopra.

    La correzione confronta con `_ESTENSIONI_NOTE`, un insieme DICHIARATO
    (.XML, .wav, .aif, .aiff, .mp3, .flac, .ogg) invece di una forma
    sintattica indovinata: questo test copre ENTRAMBI i lati, non solo il
    rifiuto -- e' esattamente il punto su cui la versione precedente del
    test era cieca.
    """
    from delugexml import musica as MU                    # noqa: PLC0415

    # --- lato accettazione: un suffisso che NON e' un'estensione nota passa ---

    non_estensioni = {
        'Drum.V2': '/SONGS/DelugePal/DRUM.V201.XML',
        'Bass.HD': '/SONGS/DelugePal/BASS.HD01.XML',
        'Song.Live': '/SONGS/DelugePal/SONG.LIVE01.XML',
        'Kick.Pro': '/SONGS/DelugePal/KICK.PRO01.XML',
    }
    sbagliati = {n: MU.destinazione(n, 1, cartella='SONGS')
                 for n, atteso in non_estensioni.items()
                 if MU.destinazione(n, 1, cartella='SONGS') != atteso}
    check('un suffisso che non e unestensione nota passa, non e rifiutato',
          not sbagliati, sbagliati)

    # numero di versione: stesso principio, caso gia' noto dalla prima revisione
    check('un nome che finisce per un numero di versione non e scambiato per estensione',
          MU.destinazione('Kit v2.1', 1, cartella='SYNTHS')
          == '/SYNTHS/DelugePal/KIT V2.101.XML',
          MU.destinazione('Kit v2.1', 1, cartella='SYNTHS'))

    # i nomi legittimi verificati dal revisore sul confine di scrittura,
    # qui riverificati anche sul lato estensione (nessuno di questi contiene
    # un punto, ma coprono lo spazio di caratteri "normali" del round di
    # ri-revisione). Il nome con la citta' e' scritto con l'escape Unicode
    # invece della lettera accentata: stessa stringa a runtime, ma la fonte
    # di questo file resta priva di lettere accentate come richiesto per il
    # codice del progetto.
    legittimi = ['Basso 2', 'kit-909', 'Take_3', 'Citt\u00e0', 'Song #1',
                 'Loop & Roll']
    falliti = [n for n in legittimi
               if _raises(lambda n=n: MU.destinazione(n, 1), ValueError)]
    check('i nomi legittimi verificati dal revisore continuano a passare',
          not falliti, falliti)

    # --- lato rifiuto: un'estensione nota ma DIVERSA resta rifiutata ---

    check('estensione nota diversa da quella attesa: rifiutata, non raddoppiata',
          _raises(lambda: MU.destinazione('kick.mp3', 1, cartella='SAMPLES'),
                  ValueError))
    check('stesso caso nell altro verso: .wav dato a una cartella XML',
          _raises(lambda: MU.destinazione('kick.wav', 1, cartella='SONGS'),
                  ValueError))
    check('.aiff (un altra estensione audio nota) su SAMPLES e comunque sbagliata',
          _raises(lambda: MU.destinazione('kick.aiff', 1, cartella='SAMPLES'),
                  ValueError))

    check('un estensione che COINCIDE resta tolta e riaggiunta (nessuna regressione)',
          MU.destinazione('kick.WAV', 1, cartella='SAMPLES')
          == '/SAMPLES/DelugePal/kick01.wav',
          MU.destinazione('kick.WAV', 1, cartella='SAMPLES'))

    # --- segnalazione fuori perimetro, chiusa nello stesso giro ---
    # 'destinazione('.XML', cartella='SONGS')' produceva '/SONGS/DelugePal/01.XML':
    # il nome, tolta l'estensione coincidente, resta vuoto. Preesistente,
    # non introdotta da questa correzione, ma della stessa famiglia
    # ("un nome degenere non deve produrre un percorso silenzioso") -- chiusa qui.
    check('un nome che e SOLO l estensione e rifiutato, non produce un percorso senza nome',
          _raises(lambda: MU.destinazione('.XML', cartella='SONGS'), ValueError))


# ------------------------------------------------------------------ rimozione

def test_remove_clip_rinumera_i_clipcode():
    """L'invariante vera: dopo una rimozione l'arrangiamento deve suonare
    ANCORA LE STESSE CLIP.

    Non si controlla che i numeri siano scalati -- si controlla che ogni
    istanza risolva allo stesso NODO di prima, per identita'. E' la cosa che
    la rinumerazione protegge, ed e' cio' che si guarderebbe sul dispositivo.

    Glassskate.XML e' scelta apposta: 54 istanze di cui 15 puntano a
    <arrangementOnlyTracks> invece che a <sessionClips>. Le due liste hanno
    numerazioni indipendenti (bit 31), quindi togliere da una NON deve
    toccare gli indici dell'altra -- il punto in cui si sbaglia.
    """
    from delugexml import arranger as A                     # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    # la clip di sessione 1, non la 0: la 0 non e' puntata da nessuno e non
    # eserciterebbe niente. Sulla 1 puntano 3 istanze (da scartare) e sopra di
    # lei ci sono gli indici 2..10 (da scalare).
    vittima = A.clip_list(doc, False)[1]
    prima = A.arrangement(doc)
    attese = [(id(s), id(c)) for s, _, c in prima if c is not vittima]
    puntavano = sum(1 for _, _, c in prima if c is vittima)
    sopra = sum(1 for _, i, _ in prima if not i.da_arranger and i.indice > 1)
    check('la fixture ha istanze da entrambe le liste',
          any(i.da_arranger for _, i, _ in prima)
          and any(not i.da_arranger for _, i, _ in prima))
    check('la fixture ha istanze che puntano alla vittima', puntavano > 0,
          f'{puntavano} istanze')
    check('la fixture ha istanze da rinumerare sopra la vittima', sopra > 0,
          f'{sopra} istanze')

    S.remove_clip(doc, vittima)

    check('la clip non e piu nel contenitore',
          vittima not in A.clip_list(doc, False))
    dopo = [(id(s), id(c)) for s, _, c in A.arrangement(doc)]
    check('l arrangiamento suona ancora esattamente le stesse clip',
          dopo == attese, f'{len(dopo)} istanze contro {len(attese)} attese')


def test_remove_clip_non_lascia_attributo_vuoto():
    """Uno strumento rimasto senza istanze PERDE l'attributo, non lo svuota.

    Misurato sul corpus: su 203 strumenti, 92 non hanno `clipInstances` e
    ZERO ce l'hanno vuoto (`0x`). La forma "attributo presente e vuoto" non
    e' mai stata scritta dal dispositivo, e inventarla sarebbe la regola
    "mai inventare strutture" violata su un dettaglio che nessuno guarderebbe.

    ARR1.XML e' la fixture minima: una clip, uno strumento, un'istanza sola.
    """
    from delugexml import arranger as A                     # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'ARR1.XML')
    strumento = S.instruments(doc)[0]
    attr = A.attr_of(strumento)
    check('la fixture ha un solo strumento con una sola istanza',
          attr is not None and len(A.instances(strumento)) == 1)

    S.remove_clip(doc, A.clip_list(doc, False)[0])

    check('lo strumento non ha piu istanze', A.instances(strumento) == [])
    check('e l attributo e sparito, non e rimasto vuoto',
          not strumento.has(attr), repr(strumento.get(attr)))


def test_remove_clip_non_lascia_la_song_view_cieca():
    """Il difetto di HANDOFF §3.1 rifatto in specchio.

    `_keep_row_visible()` ALZA soltanto lo scroll: risolve il contenuto finito
    sotto il bordo. La rimozione produce il caso opposto -- la vista resta
    parcheggiata SOPRA il contenuto rimasto, e la song view mostra il vuoto
    mentre le clip sono tutte nel file.

    Non e' teorico: 11 song su 36 hanno `yScrollSongView` positivo, e
    Progsong.XML vale 27 con 42 clip. Tolte le clip fino a venti, lo scroll
    punterebbe oltre l'ultima.
    """
    from delugexml import arranger as A                     # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Progsong.XML')
    y0 = int(doc.root.get('yScrollSongView'))
    check('la fixture ha lo scroll oltre le clip che restano', y0 == 27, str(y0))

    while len(A.clip_list(doc, False)) > 20:
        S.remove_clip(doc, A.clip_list(doc, False)[-1])

    n = len(A.clip_list(doc, False))
    y = int(doc.root.get('yScrollSongView'))
    check('song view non e cieca: almeno una clip resta a schermo', y <= n - 1,
          f'yScroll={y} con {n} clip: nessuna riga fra 0 e 7')
    check('lo scroll scende quel tanto che basta, non oltre', y == n - 1,
          f'yScroll={y}, atteso {n - 1}')


def test_remove_clip_non_muove_una_vista_gia_buona():
    """L'altra meta' della regola: se la vista mostra gia' il contenuto, non
    si tocca.

    E' lo stato che l'utente ha lasciato scrollando, e il dispositivo stesso
    ancora l'ultima riga in fondo solo in 15 song su 36: nelle altre 21 lo
    scroll e' dove l'ha messo una persona. Ri-ancorare sarebbe spostare la
    vista di qualcuno senza che l'abbia chiesto.
    """
    from delugexml import arranger as A                     # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Sacred.XML')
    y0 = int(doc.root.get('yScrollSongView'))
    n0 = len(A.clip_list(doc, False))
    check('la fixture ha lo scroll ben dentro le clip', y0 <= n0 - 2,
          f'yScroll={y0}, {n0} clip')

    S.remove_clip(doc, A.clip_list(doc, False)[-1])

    check('lo scroll non si e mosso',
          int(doc.root.get('yScrollSongView')) == y0,
          f'{y0} -> {doc.root.get("yScrollSongView")}')


def test_remove_instrument_non_lascia_clip_appese():
    """Togliere uno strumento porta via le sue clip.

    Nessun ordinale punta a uno strumento -- le clip lo risolvono per nome,
    slot o canale -- quindi non c'e' niente da rinumerare, ma le clip che lo
    nominano resterebbero APPESE: presenti, e senza piu' uno strumento che le
    suoni. Vanno via con lui, e portandole via si riapre la rinumerazione dei
    clipCode.

    L'asserzione che conta e' `arranger.check(doc)`: vede sia l'indice oltre
    la fine della lista sia l'istanza che finisce a puntare la clip di un
    ALTRO strumento, che e' precisamente il sintomo di una rinumerazione
    sbagliata. Sulla fixture intatta e' vuota, quindi dice qualcosa.
    """
    from delugexml import arranger as A                     # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    check('la fixture parte con un arrangiamento sano', A.check(doc) == [],
          '; '.join(A.check(doc)[:2]))

    vittima = next(i for i in S.instruments(doc)
                   if sum(1 for _, c in S.clips(doc)
                          if S.instrument_of(doc, c) is i) >= 2)
    sue = [c for _, c in S.clips(doc) if S.instrument_of(doc, c) is vittima]
    superstiti = [id(c) for _, c in S.clips(doc)
                  if S.instrument_of(doc, c) is not vittima]
    check('la fixture ha uno strumento con piu di una clip', len(sue) >= 2,
          f'{A.nome_di(vittima)}: {len(sue)} clip')

    S.remove_instrument(doc, vittima)

    check('lo strumento non e piu nella song',
          not any(i is vittima for i in S.instruments(doc)))
    check('le sue clip sono sparite con lui',
          not any(c is x for _, c in S.clips(doc) for x in sue))
    check('le altre clip ci sono tutte ancora',
          [id(c) for _, c in S.clips(doc)] == superstiti)
    check('nessuna clip resta senza strumento',
          all(S.instrument_of(doc, c) is not None for _, c in S.clips(doc)))
    check('e l arrangiamento e ancora sano', A.check(doc) == [],
          '; '.join(A.check(doc)[:2]))


def test_remove_note_row_solo_fuori_dai_kit():
    """Una riga di synth si toglie; una di kit NO, si svuota.

    Su un kit le righe sono indicizzate da `drumIndex`, e nel corpus 393 clip
    di kit su 395 hanno una riga per OGNI drum con indici contigui da 0 --
    l'invariante che `create.add_track()` costruisce e che
    `kit.check_indices()`, quindi `verifica()`, pretende. Togliere una riga la
    romperebbe: il file verrebbe rifiutato dal cancello stesso.

    Su un synth invece la riga E' un'altezza, non c'e' nessun ordinale, e
    toglierla e' l'operazione giusta.
    """
    from delugexml import kit as K                          # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    synth = next(c for _, c in S.clips(doc)
                 if not S.is_kit_clip(c) and len(S.note_rows(c)) >= 2)
    righe = S.note_rows(synth)
    vittima, resto = righe[0], [id(r) for r in righe[1:]]

    S.remove_note_row(synth, vittima)

    check('la riga di synth e sparita',
          [id(r) for r in S.note_rows(synth)] == resto)

    kitclip = next(c for _, c in S.clips(doc) if S.is_kit_clip(c))
    riga_kit = S.note_rows(kitclip)[0]
    check('togliere una riga di kit e rifiutato, con la sua ragione',
          _raises(lambda: S.remove_note_row(kitclip, riga_kit), ValueError))
    check('e la riga di kit e ancora al suo posto',
          any(r is riga_kit for r in S.note_rows(kitclip)))
    check('gli indici del kit restano contigui',
          K.check_indices(doc, S.instrument_of(doc, kitclip)) == [])


def test_remove_instances_in_toglie_il_tratto_non_la_clip():
    """«Leva quel pattern nella seconda meta'»: via le istanze, non la clip.

    E' la distinzione fra togliere una clip dalla linea del tempo e togliere
    la clip: lo strumento resta, la clip resta lanciabile in song view, sparisce
    solo quel tratto d'arrangiamento.

    Vengono tolte le istanze CONTENUTE nel tratto, non quelle che lo
    attraversano: un'istanza a cavallo del confine porta anche materiale fuori
    dal tratto, e toglierla farebbe tacere musica che nessuno ha chiesto di
    togliere. Restano, e il rapporto le dichiara.
    """
    from delugexml import arranger as A                     # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Aolac.XML')
    strum = max(S.instruments(doc), key=lambda i: len(A.instances(i)))
    ists = sorted(A.instances(strum), key=lambda x: x.pos)
    check('la fixture ha uno strumento con molte istanze', len(ists) >= 4,
          f'{A.nome_di(strum)}: {len(ists)}')
    da, a = ists[1].pos, ists[-1].pos
    clip_prima = len(S.clips(doc))

    rapporto = A.remove_instances_in(strum, da, a)

    restano = A.instances(strum)
    check('qualcosa e stato tolto', rapporto['tolte'] > 0,
          str(rapporto['tolte']))
    check('nessuna istanza rimasta e interamente dentro il tratto',
          not [i for i in restano if i.pos >= da and i.fine <= a])
    check('le istanze fuori dal tratto sono intatte',
          [i for i in ists if i.fine <= da or i.pos >= a]
          == [i for i in restano if i.fine <= da or i.pos >= a])
    check('le clip esistono ancora tutte', len(S.clips(doc)) == clip_prima)
    check('e lo strumento e ancora nella song',
          any(i is strum for i in S.instruments(doc)))


def test_musica_togli_smista_sul_bersaglio():
    """Un verbo solo, che riconosce da se' cosa gli hai dato.

    Il riconoscimento e' per IDENTITA' -- appartenenza alla lista degli
    strumenti, o delle clip -- non per tag: nel corpus convivono <midi> e
    <midiChannel>, e una tabella di tag sarebbe una cosa in piu' da tenere
    aggiornata per sbagliarla.
    """
    from delugexml import arranger as A                     # noqa: PLC0415
    from delugexml import musica as MU                      # noqa: PLC0415

    # --- una clip
    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    clip = A.clip_list(doc, False)[1]
    r = MU.togli(doc, clip)
    check('togli(clip) toglie la clip',
          not any(c is clip for _, c in S.clips(doc)))
    check('e ne riferisce', r.get('indice') == 1, str(r))

    # --- uno strumento
    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    strum = next(i for i in S.instruments(doc)
                 if any(S.instrument_of(doc, c) is i for _, c in S.clips(doc)))
    r = MU.togli(doc, strum)
    check('togli(strumento) toglie lo strumento',
          not any(i is strum for i in S.instruments(doc)))
    check('e si porta via le sue clip', len(r['clip']) >= 1, str(r['clip'][:3]))

    # --- uno strumento, ma solo in un tratto
    doc = parse_file(REFS / 'songs' / 'Aolac.XML')
    strum = max(S.instruments(doc), key=lambda i: len(A.instances(i)))
    ists = sorted(A.instances(strum), key=lambda x: x.pos)
    n_clip = len(S.clips(doc))
    r = MU.togli(doc, strum, quando=(ists[1].pos, ists[-1].pos))
    check('togli(strumento, quando=...) lascia lo strumento al suo posto',
          any(i is strum for i in S.instruments(doc)))
    check('non tocca nessuna clip', len(S.clips(doc)) == n_clip)
    check('e toglie solo istanze', r['tolte'] > 0 and len(A.instances(strum))
          < len(ists), str(r))

    # --- una riga di kit: si svuota, non sparisce
    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    kitclip = next(c for _, c in S.clips(doc) if S.is_kit_clip(c)
                   and any(S.read_notes(r) for r in S.note_rows(c)))
    riga = next(r for r in S.note_rows(kitclip) if S.read_notes(r))
    n_righe = len(S.note_rows(kitclip))
    MU.togli(doc, riga)
    check('togli(riga di kit) la svuota', S.read_notes(riga) == [])
    check('ma la riga resta, una per drum',
          len(S.note_rows(kitclip)) == n_righe
          and any(r is riga for r in S.note_rows(kitclip)))

    # --- una riga di synth: sparisce
    synth = next(c for _, c in S.clips(doc)
                 if not S.is_kit_clip(c) and len(S.note_rows(c)) >= 2)
    riga = S.note_rows(synth)[0]
    MU.togli(doc, riga)
    check('togli(riga di synth) la toglie',
          not any(r is riga for r in S.note_rows(synth)))

    # --- qualcosa che non c'entra
    check('un nodo estraneo viene rifiutato, non ignorato',
          _raises(lambda: MU.togli(doc, doc.root.find('reverb')), ValueError))
    check('quando= su una clip e un errore, non un silenzio',
          _raises(lambda: MU.togli(doc, A.clip_list(doc, False)[0],
                                   quando=(0, 384)), ValueError))


def test_musica_scrivi_una_chiamata_per_i_due_idiomi():
    """Scrivere note in una clip, senza sapere se e' un kit o un synth.

    Prima serviva comporre tre primitive con un idioma DIVERSO per i due casi
    (`add_note_row` su synth, `drum_row` su kit, e `fit_clip_scroll_to_notes`
    da ricordarsi in coda). E' esattamente cio' che ha prodotto il primo
    difetto della prova d'accettazione, ed e' cio' che SKILL.md insegnava in
    tre righe separate.

    La forma delle note basta a smistare, perche' e' gia' quella giusta:
    `melodia()` e `accordi()` danno altezza -> note, `passi()` una lista sola.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')

    # --- synth: un dizionario altezza -> note diventa una riga per altezza
    synth = next(c for _, c in S.clips(doc) if not S.is_kit_clip(c))
    r = MU.scrivi(doc, synth, MU.accordi('do3 mi3 sol3 | re3 fa3 la3'))
    y_scritte = sorted(MU.altezza(n) for n in
                       ('do3', 'mi3', 'sol3', 're3', 'fa3', 'la3'))
    presenti = sorted(int(x.get('y')) for x in S.note_rows(synth)
                      if x.has('y') and S.read_notes(x))
    check('scrivi(dict) crea una riga per ogni altezza',
          all(y in presenti for y in y_scritte), f'{y_scritte} vs {presenti}')
    check('e ne riferisce', r['righe'] == len(y_scritte), str(r))
    check('lo scroll della clip segue le note scritte',
          int(synth.get('yScroll')) <= min(y_scritte), synth.get('yScroll'))

    # --- kit: una lista piu' il nome del drum
    kitclip = next(c for _, c in S.clips(doc) if S.is_kit_clip(c))
    nome = S.drum_names(doc, kitclip)[0]
    r = MU.scrivi(doc, kitclip, MU.passi('x...x...x...x...'), dove=nome)
    riga = S.drum_row(doc, kitclip, nome)
    check('scrivi(lista, dove=drum) scrive sulla riga di quel drum',
          len(S.read_notes(riga)) == 4, str(len(S.read_notes(riga))))
    check('e non ha aggiunto righe al kit',
          len(S.note_rows(kitclip)) == len(S.drum_names(doc, kitclip)))

    # --- synth con una lista: dove= e' un'altezza
    r = MU.scrivi(doc, synth, MU.passi('x.x.'), dove='la4')
    check('scrivi(lista, dove=altezza) scrive su una riga sola',
          len(S.read_notes(S.note_row(synth, MU.altezza('la4')))) == 2)

    # --- gli errori dicono quale dei due casi si voleva
    check('un dict su una clip di kit e rifiutato',
          _raises(lambda: MU.scrivi(doc, kitclip, MU.melodia('do3 re3')),
                  ValueError))
    check('una lista senza dove= e rifiutata',
          _raises(lambda: MU.scrivi(doc, synth, MU.passi('x...')), ValueError))
    check('un nome di drum che non esiste e rifiutato',
          _raises(lambda: MU.scrivi(doc, kitclip, MU.passi('x...'),
                                    dove='NONESISTE'), ValueError))


def test_il_cancello_ferma_un_clipcode_appeso():
    """La rete sotto la rimozione: se qualcuno togliesse una clip SENZA
    rinumerare, `verifica()` deve rifiutare il file.

    E' l'unico modo di produrre un `clipCode` che punta oltre la fine della
    lista, ed e' un difetto che non si vede da nessuna parte -- il file e'
    XML valido, si rilegge, e sbaglia solo suonando. Il controllo esiste gia'
    in `arranger.check()`; questo test lo lega alla rimozione, cosi' resta
    legato anche a chi un domani toccasse il cancello.
    """
    from delugexml import arranger as A                     # noqa: PLC0415
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    check('la fixture parte accettata dal cancello', MU.verifica(doc) == [],
          '; '.join(MU.verifica(doc)[:2]))

    # la rimozione ingenua: via dal contenitore, e nient'altro
    cont = doc.root.find('sessionClips')
    cont.children = cont.children[:-1]
    cont.touch()

    check('il cancello vede il clipCode appeso', MU.verifica(doc) != [],
          '; '.join(MU.verifica(doc)[:2]))

    # e la rimozione vera non lo produce
    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    S.remove_clip(doc, A.clip_list(doc, False)[-1])
    check('mentre remove_clip lascia il file accettabile',
          MU.verifica(doc) == [], '; '.join(MU.verifica(doc)[:2]))


def test_rimozione_riscritta_e_riletta():
    """Il giro completo: togliere, serializzare, rileggere.

    Un difetto di serializzazione dopo una rimozione (span vecchi, nodi non
    marcati) non si vedrebbe controllando l'albero in memoria -- e' gia'
    successo in questo progetto con `copy_detached`, dove il file passava la
    scrittura e falliva solo alla rilettura.
    """
    from delugexml import arranger as A                     # noqa: PLC0415
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    S.remove_clip(doc, A.clip_list(doc, False)[1])
    atteso = [(A.nome_di(s), S.clip_label(c))
              for s, _, c in A.arrangement(doc) if c is not None]

    testo = serialize(doc, FormatTable().learn([doc]))
    riletto = parse(testo)

    check('il file riscritto si rilegge senza anomalie nuove',
          not [p for p in riletto.problems if p.kind not in
               {'unescaped_amp', 'duplicate_attr'}],
          str([p.kind for p in riletto.problems[:3]]))
    check('e l arrangiamento riletto punta alle stesse clip',
          [(A.nome_di(s), S.clip_label(c))
           for s, _, c in A.arrangement(riletto) if c is not None] == atteso)
    check('il file riletto e accettato dal cancello',
          MU.verifica(riletto) == [], '; '.join(MU.verifica(riletto)[:2]))


# ------------------------------------------------------------ trasformazioni

def test_trasponi_cromatica_su_synth():
    """Le righe di una clip di synth SONO le altezze: trasporre muove `y`.

    L'invariante piu' forte e' la reversibilita': un'ottava su e un'ottava giu'
    devono riportare la clip esattamente dov'era, note comprese. Se la
    trasposizione perdesse o fondesse qualcosa, il giro di ritorno non
    tornerebbe.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    clip = next(c for _, c in S.clips(doc)
                if not S.is_kit_clip(c) and len(S.note_rows(c)) >= 3)
    prima = {int(r.get('y')): len(S.read_notes(r))
             for r in S.note_rows(clip) if r.has('y')}
    check('la fixture ha righe con altezza', len(prima) >= 3, str(len(prima)))

    r = MU.trasponi(doc, clip, semitoni=12)

    dopo = {int(x.get('y')): len(S.read_notes(x))
            for x in S.note_rows(clip) if x.has('y')}
    check('ogni riga e salita di dodici semitoni',
          dopo == {y + 12: n for y, n in prima.items()},
          f'{sorted(prima)} -> {sorted(dopo)}')
    check('e il rapporto lo dice', r['semitoni'] == 12 and r['righe'] == len(prima),
          str(r))
    check('lo scroll della clip ha seguito le note',
          int(clip.get('yScroll')) <= min(dopo), clip.get('yScroll'))

    MU.trasponi(doc, clip, semitoni=-12)
    check('un ottava giu riporta tutto dov era',
          {int(x.get('y')): len(S.read_notes(x))
           for x in S.note_rows(clip) if x.has('y')} == prima)


def _clip_di_prova(altezze, scala=('re', 'minore')):
    """Una clip di synth in una scala nota, con una nota per ogni altezza."""
    from delugexml import musica as MU                      # noqa: PLC0415
    from delugexml.notes import Note as Nt                  # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'TEMPL0.XML')
    S.set_scale(doc, *scala)
    clip = doc.root.find('sessionClips').children[0]
    for r in list(S.note_rows(clip)):
        S.remove_note_row(clip, r)
    MU.scrivi(doc, clip, {MU.altezza(a): [Nt(pos=0, length=48)]
                          for a in altezze})
    return doc, clip


def _altezze(clip):
    return sorted(int(r.get('y')) for r in S.note_rows(clip)
                  if r.has('y') and S.read_notes(r))


def test_trasponi_per_gradi_resta_in_scala():
    """Salire di un grado in re minore muove ogni nota al grado successivo.

    Re minore: re mi fa sol la sib do. Un grado sopra, re->mi, fa->sol,
    la->sib: gli intervalli NON sono tutti uguali, ed e' precisamente cio' che
    distingue la trasposizione diatonica da quella cromatica.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc, clip = _clip_di_prova(('re2', 'fa2', 'la2'))
    check('la fixture parte da re fa la',
          _altezze(clip) == [MU.altezza(a) for a in ('re2', 'fa2', 'la2')],
          str(_altezze(clip)))

    MU.trasponi(doc, clip, gradi=1)

    check('un grado sopra da mi sol sib, non tre semitoni fissi',
          _altezze(clip) == [MU.altezza(a) for a in ('mi2', 'sol2', 'sib2')],
          str(_altezze(clip)))


def test_trasponi_per_gradi_conserva_le_note_fuori_scala():
    """Una nota fuori scala conserva il suo SCARTO dal grado.

    fa#2 e' un semitono sopra fa2, che in re minore e' il terzo grado. Salendo
    di un grado deve restare un semitono sopra il NUOVO terzo grado, cioe'
    sol#2. Schiacciarla in scala distruggerebbe la nota di passaggio -- ed e'
    esattamente cio' che FINDINGS §6 dice di non fare: Progsong.XML ha 315
    note fuori scala e non sono un errore.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc, clip = _clip_di_prova(('fa2', 'fa#2'))
    MU.trasponi(doc, clip, gradi=1)
    check('fa -> sol, e fa# -> sol#: lo scarto resta',
          _altezze(clip) == [MU.altezza('sol2'), MU.altezza('sol#2')],
          str(_altezze(clip)))


def test_trasponi_per_gradi_fonde_le_righe_che_collidono():
    """Il modo diatonico NON e' biiettivo: due righe possono atterrare insieme.

    In re minore il passo fra il secondo grado (mi) e il terzo (fa) e' di un
    semitono. Salendo di un grado, mib2 (uno sopra il primo grado) e mi2 (il
    secondo grado esatto) finiscono TUTTI E DUE su fa2. Le due righe vanno
    fuse, e il rapporto deve dirlo: in semitoni non succede mai, quindi e' un
    caso che solo questo modo puo' produrre.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc, clip = _clip_di_prova(('mib2', 'mi2'))
    check('la fixture ha due righe distinte', len(_altezze(clip)) == 2)

    r = MU.trasponi(doc, clip, gradi=1)

    check('restano su una riga sola, fa2',
          _altezze(clip) == [MU.altezza('fa2')], str(_altezze(clip)))
    check('e il rapporto dichiara la fusione', r.get('fuse') == 1, str(r))


def test_trasponi_kit_muove_transpose_sugli_osc():
    """Un kit si trasporta intonando i suoi drum, non toccando i drumIndex.

    Il manuale, voce TRANSPOSE del menu degli oscillatori: «Semitones + cents
    for adjustment». `transpose` sono i semitoni, e vale sia per i drum a
    campione sia per quelli sintetizzati, che sono lo stesso nodo <sound>.

    Nel corpus 144 oscillatori su 204 NON hanno l'attributo: va aggiunto.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    clip = next(c for _, c in S.clips(doc) if S.is_kit_clip(c))
    kit = S.instrument_of(doc, clip)
    osc = [o for d in S.drums(kit) for n in ('osc1', 'osc2')
           if (o := d.find(n)) is not None]
    prima = [int(o.get('transpose') or 0) for o in osc]
    mancanti = sum(1 for o in osc if not o.has('transpose'))
    check('la fixture ha oscillatori senza transpose', mancanti > 0,
          f'{mancanti} su {len(osc)}')

    r = MU.trasponi(doc, clip, semitoni=2)

    check('ogni oscillatore e salito di due semitoni',
          [int(o.get('transpose') or 0) for o in osc] == [p + 2 for p in prima])
    check('l attributo e stato aggiunto dove mancava',
          all(o.has('transpose') for o in osc))
    check('il rapporto dice che il kit e condiviso',
          r.get('condiviso') is True and r.get('drum', 0) > 0, str(r))
    check('e nessun drumIndex e stato toccato',
          [x.get('drumIndex') for x in S.note_rows(clip)]
          == [str(i) for i in range(len(S.note_rows(clip)))])


def test_trasponi_kit_rifiuta_i_gradi():
    """Un drum non ha gradi di scala: `gradi=` su un kit e un errore."""
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    clip = next(c for _, c in S.clips(doc) if S.is_kit_clip(c))
    check('gradi su un kit e rifiutato',
          _raises(lambda: MU.trasponi(doc, clip, gradi=1), ValueError))


def test_trasponi_kit_salta_le_righe_senza_altezza():
    """Una riga di gate non ha altezza: si salta e si dichiara.

    Non e' un errore, e' un fatto sui gate -- ma chi ha chiesto la
    trasposizione deve sapere che una riga non l'ha seguita, invece di
    scoprirlo suonando.

    La fixture viene da corpus_versions perche' e' l'unico kit con righe
    <gateOutput> che esista: leggerlo non tocca la tabella di formato, che
    si impara solo da refs.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(ROOT / 'corpus_versions' / '3.1.5' / 'Gates.XML')
    kit = next(n for n in doc.iter() if n.tag == 'kit'
               and any(c.tag == 'gateOutput'
                       for c in (n.find('soundSources').children
                                 if n.find('soundSources') else [])))
    gate = [d for d in S.drums(kit) if d.tag == 'gateOutput']
    check('la fixture ha righe di gate', len(gate) > 0, str(len(gate)))

    r = MU.trasponi(doc, kit, semitoni=3)

    check('le righe di gate sono dichiarate come saltate',
          r.get('saltati') == len(gate), str(r))
    check('e non hanno guadagnato attributi inventati',
          all(not g.attrs or [k for k, _ in g.attrs] == ['channel']
              for g in gate))


def test_il_midioutput_figlio_di_sound_non_e_una_riga_midi():
    """Il `<midiOutput>` FIGLIO di un `<sound>` e' un'altra cosa, e non si tocca.

    E' l'errore che questo progetto aveva commesso: scambiarlo per la riga
    MIDI di un kit. Esiste su ogni `<sound>` ma vale `channel="255"
    noteForDrum="255"` in tutti e 1180 i casi del corpus -- mai visto attivo --
    mentre la riga MIDI vera e' un `<midiOutput>` FRATELLO dei `<sound>` dentro
    `<soundSources>`, con l'attributo `note`.

    Questo test tiene fermo il confine, cosi' l'ipotesi sbagliata non puo'
    rientrare da una porta laterale.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    clip = next(c for _, c in S.clips(doc) if S.is_kit_clip(c))
    kit = S.instrument_of(doc, clip)
    drum = S.drums(kit)[0]
    mo = drum.find('midiOutput')
    check('un drum a campione porta comunque un midiOutput, disattivato',
          mo is not None and mo.get('noteForDrum') == '255',
          str(dict(mo.attrs)) if mo is not None else 'assente')
    osc_prima = int(drum.find('osc1').get('transpose') or 0)

    MU.trasponi(doc, kit, semitoni=4)

    check('il drum si intona sugli oscillatori, non sul suo midiOutput',
          int(drum.find('osc1').get('transpose')) == osc_prima + 4)
    check('e noteForDrum resta dov era', mo.get('noteForDrum') == '255',
          mo.get('noteForDrum'))


def test_trasponi_muove_la_riga_midi_di_un_kit():
    """La forma VERA di una riga MIDI in un kit, scritta dal dispositivo.

    L'ipotesi che questo progetto aveva implementato era sbagliata su
    entrambi i punti: non e' un <sound> con un <midiOutput> figlio, ed il
    nome dell'attributo non e' `noteForDrum`. E' un <midiOutput> dentro
    <soundSources>, FRATELLO dei <sound>:

        <midiOutput name="" channel="0" note="0" />

    Il file viene da TRASF401MIDI.XML, salvata dall'utente sul Deluge con
    [AUDITION]+[MIDI] e una nota sul terzo beat. E' l'unico esemplare
    esistente, ed e' il motivo per cui l'ipotesi si e' potuta chiudere.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'TRASF401MIDI.XML')
    kit = next(n for n in doc.iter() if n.tag == 'kit'
               and any(c.tag == 'midiOutput'
                       for c in n.find('soundSources').children))
    riga = next(d for d in S.drums(kit) if d.tag == 'midiOutput')
    # il kit di questo file parte gia' a +5: la song e' stata salvata a partire
    # da TRASF401, che era il kit trasposto. Quindi si confronta col prima.
    osc = [o for d in S.drums(kit) if d.tag == 'sound'
           for n in ('osc1', 'osc2') if (o := d.find(n)) is not None]
    prima = [int(o.get('transpose') or 0) for o in osc]
    check('la fixture ha una riga MIDI con la sua nota',
          riga.get('note') == '0' and riga.get('channel') == '0',
          str(dict(riga.attrs)))

    r = MU.trasponi(doc, kit, semitoni=7)

    check('la nota della riga MIDI e salita di sette', riga.get('note') == '7',
          riga.get('note'))
    check('nessuna riga e stata saltata', r['saltati'] == 0, str(r))
    check('e il rapporto la conta come MIDI', r['midi'] == 1, str(r))
    check('gli altri drum sono comunque saliti sugli osc',
          [int(o.get('transpose')) for o in osc] == [p + 7 for p in prima])


def test_trasponi_riga_midi_resta_fra_zero_e_centoventisette():
    """Una nota MIDI vive fra 0 e 127: sotto o sopra si ferma li."""
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'TRASF401MIDI.XML')
    kit = next(n for n in doc.iter() if n.tag == 'kit'
               and any(c.tag == 'midiOutput'
                       for c in n.find('soundSources').children))
    riga = next(d for d in S.drums(kit) if d.tag == 'midiOutput')

    MU.trasponi(doc, kit, semitoni=-12)
    check('sotto lo zero si ferma a zero', riga.get('note') == '0',
          riga.get('note'))

    riga.set('note', '120')
    MU.trasponi(doc, kit, semitoni=24)
    check('sopra il 127 si ferma a 127', riga.get('note') == '127',
          riga.get('note'))


def test_trasponi_vuole_uno_dei_due_modi():
    """`semitoni` o `gradi`, non nessuno dei due e non tutti e due."""
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Glassskate.XML')
    clip = next(c for _, c in S.clips(doc) if not S.is_kit_clip(c))
    check('senza ne semitoni ne gradi e un errore',
          _raises(lambda: MU.trasponi(doc, clip), ValueError))
    check('con tutti e due anche',
          _raises(lambda: MU.trasponi(doc, clip, semitoni=2, gradi=1),
                  ValueError))


def _clip_ritmica(pattern='x...x...x...x...', lunghezza=384):
    """Una clip con un ritmo noto: 4 note a 0, 96, 192, 288 su una battuta."""
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'TEMPL0.XML')
    clip = doc.root.find('sessionClips').children[0]
    for r in list(S.note_rows(clip)):
        S.remove_note_row(clip, r)
    S.set_clip_length(clip, lunghezza)
    MU.scrivi(doc, clip, MU.passi(pattern), dove='do3')
    return doc, clip


def _pos(clip):
    return sorted(n.pos for r in S.note_rows(clip) for n in S.read_notes(r))


def test_sposta_muove_le_note_nel_tempo():
    """«Sposta di una battuta»: le note traslano, la clip resta lunga uguale."""
    from delugexml import musica as MU                      # noqa: PLC0415

    doc, clip = _clip_ritmica()
    check('la fixture ha il ritmo atteso', _pos(clip) == [0, 96, 192, 288],
          str(_pos(clip)))

    MU.sposta(doc, clip, tick=96)
    check('spostare di 96 tick trasla tutto', _pos(clip) == [96, 192, 288, 384],
          str(_pos(clip)))
    MU.sposta(doc, clip, tick=-96)
    check('e -96 riporta indietro', _pos(clip) == [0, 96, 192, 288],
          str(_pos(clip)))

    MU.sposta(doc, clip, battute=1)
    check('battute=1 passa da ticks_per_bar, non da un numero fisso',
          _pos(clip) == [384, 480, 576, 672], str(_pos(clip)))
    MU.sposta(doc, clip, battute=-1)
    check('e battute=-1 torna al punto di partenza',
          _pos(clip) == [0, 96, 192, 288], str(_pos(clip)))
    check('la lunghezza della clip non e cambiata', clip.get('length') == '384')


def test_sposta_non_butta_via_le_note_prima_dello_zero():
    """Prima del tick 0 non c'e' posto: si rifiuta, non si scarta in silenzio.

    Scartare musica senza dirlo e' il comportamento peggiore fra quelli
    possibili, e l'errore deve dire quanto spazio c'e' davvero.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc, clip = _clip_ritmica()
    check('spostare oltre lo zero e rifiutato',
          _raises(lambda: MU.sposta(doc, clip, tick=-96), ValueError))
    check('e le note non sono state toccate', _pos(clip) == [0, 96, 192, 288])
    MU.sposta(doc, clip, tick=0)
    check('spostare di zero e legale e non fa niente',
          _pos(clip) == [0, 96, 192, 288])


def test_repeat_allunga_ripetendo():
    """repeat(2): due battute, il materiale suona due volte, durate invariate."""
    from delugexml import musica as MU                      # noqa: PLC0415

    doc, clip = _clip_ritmica()
    durate = sorted(n.length for r in S.note_rows(clip) for n in S.read_notes(r))

    MU.repeat(doc, clip, 2)

    check('la clip e lunga il doppio', clip.get('length') == '768')
    check('e il materiale si ripete una battuta dopo',
          _pos(clip) == [0, 96, 192, 288, 384, 480, 576, 672], str(_pos(clip)))
    check('le durate delle note non sono cambiate',
          sorted(n.length for r in S.note_rows(clip)
                 for n in S.read_notes(r)) == durate + durate)


def test_stretch_scala_note_e_clip_insieme():
    """stretch(0.5): tutto compresso, clip compresa. Il materiale e' lo stesso."""
    from delugexml import musica as MU                      # noqa: PLC0415

    doc, clip = _clip_ritmica()
    n_prima = len(_pos(clip))
    dur_prima = max(n.length for r in S.note_rows(clip) for n in S.read_notes(r))

    MU.stretch(doc, clip, 0.5)

    check('la clip e lunga la meta', clip.get('length') == '192')
    check('le posizioni sono dimezzate', _pos(clip) == [0, 48, 96, 144],
          str(_pos(clip)))
    check('anche le durate', max(n.length for r in S.note_rows(clip)
                                 for n in S.read_notes(r)) == dur_prima // 2)
    check('e il numero di note non cambia', len(_pos(clip)) == n_prima)


def test_double_time_e_half_time():
    """I due nomi musicali, e la loro asimmetria voluta.

    double_time tiene la battuta e ci mette il materiale due volte: 8 ottavi
    diventano 16 sedicesimi. half_time raddoppia la clip, perche' in meta'
    tempo un pattern di una battuta ne occupa DUE davvero.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc, clip = _clip_ritmica()
    MU.double_time(doc, clip)
    check('double_time lascia la clip di una battuta',
          clip.get('length') == '384')
    check('e raddoppia il numero di note',
          _pos(clip) == [0, 48, 96, 144, 192, 240, 288, 336], str(_pos(clip)))

    doc, clip = _clip_ritmica()
    MU.half_time(doc, clip)
    check('half_time porta la clip a due battute', clip.get('length') == '768')
    check('e le note restano quattro, larghe il doppio',
          _pos(clip) == [0, 192, 384, 576], str(_pos(clip)))


def test_repeat_moltiplica_la_lunghezza_propria_delle_righe():
    """Il poliritmo: una riga puo' avere una lunghezza sua, indipendente.

    Nel corpus c1.3.0 c'e' un solo esemplare -- Qbix.XML, clip KIT000, righe
    da 384, 576 e 504 tick su una clip da 672 -- ma se `repeat` non la
    moltiplicasse il poliritmo si romperebbe in silenzio, che e' il tipo di
    difetto che qui non si vede finche' non si suona.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'Qbix.XML')
    clip = next(c for _, c in S.clips(doc)
                if any(r.has('length') for r in S.note_rows(c)))
    prima = {id(r): int(r.get('length')) for r in S.note_rows(clip)
             if r.has('length')}
    lung = int(clip.get('length'))
    check('la fixture ha righe con lunghezza propria', len(prima) >= 3,
          str(len(prima)))

    MU.repeat(doc, clip, 2)

    check('la clip e raddoppiata', int(clip.get('length')) == lung * 2)
    check('e anche la lunghezza propria di ogni riga',
          {id(r): int(r.get('length')) for r in S.note_rows(clip)
           if r.has('length')} == {k: v * 2 for k, v in prima.items()})


def test_trasformazioni_riscritte_e_rilette():
    """Ogni trasformazione lascia un file che si rilegge e che il cancello accetta.

    Un difetto di serializzazione non si vedrebbe controllando l'albero in
    memoria: e' gia' successo in questo progetto con `copy_detached`, dove il
    file passava la scrittura e falliva solo alla rilettura.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    tavola = FormatTable().learn(
        [parse_file(p) for p in sorted(REFS.rglob('*.XML'))
         if not p.name.startswith('._')])

    for nome, applica in (
            ('trasponi semitoni', lambda d, c: MU.trasponi(d, c, semitoni=5)),
            ('trasponi gradi', lambda d, c: MU.trasponi(d, c, gradi=2)),
            ('sposta', lambda d, c: MU.sposta(d, c, battute=1)),
            ('repeat', lambda d, c: MU.repeat(d, c, 2)),
            ('stretch', lambda d, c: MU.stretch(d, c, 0.5)),
            ('double_time', lambda d, c: MU.double_time(d, c)),
            ('half_time', lambda d, c: MU.half_time(d, c))):
        doc, clip = _clip_ritmica()
        applica(doc, clip)
        atteso = _pos(clip)
        riletto = parse(serialize(doc, tavola))
        rclip = riletto.root.find('sessionClips').children[0]
        check(f'{nome}: il file riletto ha le stesse note',
              _pos(rclip) == atteso, f'{_pos(rclip)} contro {atteso}')
        check(f'{nome}: e il cancello lo accetta',
              MU.verifica(riletto) == [],
              '; '.join(MU.verifica(riletto)[:2]))


# ------------------------------------------- la finestra della clip in scala

def test_in_key_mode_yscroll_conta_i_gradi():
    """La misura sul dispositivo, incisa in un test.

    Coppia controllata SCALB0/SCALB1, re maggiore, la STESSA nota D3 (y=62)
    portata a mano dalla riga piu' bassa alla piu' alta dello schermo:

        SCALB0   D3 alla riga 0   yScroll = 37
        SCALB1   D3 alla riga 7   yScroll = 30

    Sette righe, sette unita' di differenza: in modalita' a scala una riga
    vale UN GRADO, e `yScroll` conta i gradi della scala dalla nota 0 --
    non i semitoni. 37 e' esattamente il grado di D3 in re maggiore.

    Lo conferma la seconda coppia, SCALA0/SCALA1, dove una riga sola di
    scroll muove `yScroll` di 1 e lascia `inKeyScrollOffset` fermo: quello
    NON governa la clip view, al contrario di quanto questo progetto credeva.
    """
    b0 = parse_file(REFS / 'songs' / 'SCALB0.XML')
    b1 = parse_file(REFS / 'songs' / 'SCALB1.XML')
    c0 = next(c for _, c in S.clips(b0) if c.tag == 'instrumentClip')
    c1 = next(c for _, c in S.clips(b1) if c.tag == 'instrumentClip')

    check('la fixture e in modalita a scala', c0.get('inKeyMode') == '1')
    check('il grado di D3 in re maggiore e 37', S.scale_degree(b0, 62) == 37,
          str(S.scale_degree(b0, 62)))
    check('ed e quello che il dispositivo ha scritto in yScroll',
          c0.get('yScroll') == '37', c0.get('yScroll'))
    check('sette righe piu su fanno sette gradi meno di scroll',
          int(c1.get('yScroll')) == int(c0.get('yScroll')) - 7,
          f'{c0.get("yScroll")} -> {c1.get("yScroll")}')

    a0 = parse_file(REFS / 'songs' / 'SCALA0.XML')
    a1 = parse_file(REFS / 'songs' / 'SCALA1.XML')
    ca = next(c for _, c in S.clips(a0) if c.tag == 'instrumentClip')
    cb = next(c for _, c in S.clips(a1) if c.tag == 'instrumentClip')
    check('una riga sola muove yScroll di uno',
          int(cb.get('yScroll')) - int(ca.get('yScroll')) == 1)
    check('e non muove inKeyScrollOffset: quello non governa la clip view',
          ca.get('inKeyScrollOffset') == cb.get('inKeyScrollOffset'),
          f'{ca.get("inKeyScrollOffset")} -> {cb.get("inKeyScrollOffset")}')


def test_fit_scroll_in_key_mode_usa_i_gradi():
    """Il difetto vivo che la misura ha scoperto, e che era gia' stato spedito.

    Ogni clip generata da Deluge Pal nasce con `inKeyMode=1`, perche' CLIP_BASE
    viene da TEMPL0. `fit_clip_scroll_to_notes()` ci scriveva dentro l'ALTEZZA
    della nota piu' bassa, mentre il dispositivo legge quel numero come GRADO:
    le cinque song caricate sul Deluge si aprivano con lo schermo vuoto, note
    corrette e invisibili. Verificato guardando `TRASF201` sul dispositivo.
    """
    from delugexml import musica as MU                      # noqa: PLC0415
    from delugexml.notes import Note as Nt                  # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'TEMPL0.XML')
    S.set_scale(doc, 're', 'minore')
    clip = doc.root.find('sessionClips').children[0]
    for r in list(S.note_rows(clip)):
        S.remove_note_row(clip, r)
    check('le clip del modello sono in modalita a scala',
          clip.get('inKeyMode') == '1')

    basso = MU.altezza('re2')
    S.write_notes(S.note_row(clip, basso, create=True),
                  [Nt(pos=0, length=48)], create=True)
    S.fit_clip_scroll_to_notes(doc, clip)

    atteso = S.scale_degree(doc, basso)
    check('yScroll finisce sul GRADO della nota, non sulla sua altezza',
          clip.get('yScroll') == str(atteso),
          f'{clip.get("yScroll")}, atteso {atteso} (altezza {basso})')
    check('e la nota e davvero a schermo', S.notes_hidden_by_scroll(doc) == [],
          '; '.join(S.notes_hidden_by_scroll(doc)))


def test_avvertenza_copre_anche_le_clip_in_scala():
    """L'avvertenza ora vede anche la modalita' a scala, e avrebbe visto il bug.

    Restava ferma alle clip cromatiche perche' la formula in scala non era
    verificata; ora lo e', e questo controllo e' esattamente cio' che avrebbe
    fermato le cinque song spedite con lo schermo vuoto.
    """
    from delugexml.notes import Note as Nt                  # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'TEMPL0.XML')
    S.set_scale(doc, 're', 'minore')
    clip = doc.root.find('sessionClips').children[0]
    for r in list(S.note_rows(clip)):
        S.remove_note_row(clip, r)
    S.write_notes(S.note_row(clip, 38, create=True),
                  [Nt(pos=0, length=48)], create=True)

    clip.set('yScroll', '38')          # l'altezza, cioe' il difetto vecchio
    check('una clip in scala con lo scroll sull altezza viene segnalata',
          S.notes_hidden_by_scroll(doc) != [],
          str(S.notes_hidden_by_scroll(doc)))

    clip.set('yScroll', str(S.scale_degree(doc, 38)))
    check('e col grado giusto tace', S.notes_hidden_by_scroll(doc) == [],
          str(S.notes_hidden_by_scroll(doc)))


def test_fit_ancora_la_nota_piu_bassa_alla_prima_riga():
    """`fit` ANCORA, non si limita a non lasciare la vista cieca.

    Il caso, visto sul dispositivo su TRASF204: si scrivono le note (fit porta
    yScroll al grado 23), poi si traspone di un grado (le righe salgono a
    24-31). La vecchia regola -- "non muovere se almeno una riga si vede" --
    lasciava yScroll a 23: la nota piu' bassa finiva sulla SECONDA riga, la
    prima restava sprecata, e la nota piu' alta usciva dallo schermo.

    Quella regola viene dagli scroll di song view, dove ha senso non spostare
    una vista che l'utente ha lasciato dov'e'. Qui no: questa funzione si
    chiama "porta la finestra dove sono le note", e ancorare la piu' bassa
    alla prima riga e' cio' che la rende utile -- fra l'altro fa entrare
    tutto ogni volta che le note stanno in otto righe, come qui.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'TEMPL0.XML')
    S.set_scale(doc, 're', 'minore')
    clip = doc.root.find('sessionClips').children[0]
    for r in list(S.note_rows(clip)):
        S.remove_note_row(clip, r)
    MU.scrivi(doc, clip, MU.melodia('re2 fa2 la2 re3', durata='1/4'))
    MU.trasponi(doc, clip, gradi=1)

    righe = S.clip_rows_with_notes(doc, clip)
    y = int(clip.get('yScroll'))
    check('la nota piu bassa sta sulla PRIMA riga', y == min(righe),
          f'yScroll={y}, righe={righe}')
    check('e stando in otto righe ci entrano tutte',
          all(y <= r < y + 8 for r in righe), f'{righe} con yScroll={y}')


def test_anche_i_kit_scrollano_con_yscroll():
    """La misura sul dispositivo: la finestra di una clip di kit e' `yScroll`.

    Coppia controllata KITSCR0/KITSCR1, la stessa riga (il kick, posizione 6
    su sedici) portata a mano dal fondo dello schermo alla cima:

        KITSCR0   kick alla riga 0   yScroll =  6
        KITSCR1   kick alla riga 7   yScroll = -1

    Sette righe, sette unita': la STESSA geometria di tutto il resto del
    dispositivo, dove `riga = posizione - yScroll` su otto righe. In un kit
    l'unita' e' la posizione della riga, come in cromatico e' il semitono e
    in scala e' il grado.

    `drumsScrollOffset` vale 6 in ENTRAMBI: non e' lui a governare la clip
    view, e questo progetto ci aveva scritto dentro per due tentativi di
    correzione falliti.
    """
    a = parse_file(REFS / 'songs' / 'KITSCR0.XML')
    b = parse_file(REFS / 'songs' / 'KITSCR1.XML')
    ca = next(c for _, c in S.clips(a) if S.is_kit_clip(c))
    cb = next(c for _, c in S.clips(b) if S.is_kit_clip(c))

    check('la riga che suona piu in basso sta in posizione 6',
          S.drum_rows_sounding(ca)[0] == 6, str(S.drum_rows_sounding(ca)))
    check('col kick in fondo allo schermo yScroll vale la sua posizione',
          ca.get('yScroll') == '6', ca.get('yScroll'))
    check('sette righe piu su fanno sette unita meno di yScroll',
          int(cb.get('yScroll')) == int(ca.get('yScroll')) - 7,
          f'{ca.get("yScroll")} -> {cb.get("yScroll")}')
    check('e drumsScrollOffset non si muove: non governa la clip view',
          ca.get('drumsScrollOffset') == cb.get('drumsScrollOffset'),
          f'{ca.get("drumsScrollOffset")} -> {cb.get("drumsScrollOffset")}')


def test_fit_kit_scrive_yscroll_e_non_drumsscrolloffset():
    """La correzione che ne segue, e il difetto che chiude.

    Le clip di kit generate da questo progetto si portavano `yScroll=37` da
    TEMPL0 -- molto sopra le sedici righe di un kit -- quindi si aprivano
    lontanissime dalle note e bisognava scrollare in giu' per trovarle. Visto
    sul dispositivo.
    """
    from delugexml import musica as MU                      # noqa: PLC0415
    from delugexml import create as C                       # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'TEMPL0.XML')
    _, clip = C.add_track(doc, REFS / 'kits' / 'CR78FROMMARS.XML',
                          name='CR78FROMMARS', folder='KITS', length=384)
    prima_dso = clip.get('drumsScrollOffset')
    for drum, patt in (('Kick CR78 12', 'x...x...x...x...'),
                       ('Rim CR78 02', '....x.......x...')):
        MU.scrivi(doc, clip, MU.passi(patt), dove=drum)

    pos = S.drum_rows_sounding(clip)
    check('la fixture ha righe lontane fra loro', pos == [6, 13], str(pos))

    y = clip.get('yScroll')
    check('yScroll porta tutte le righe che suonano a schermo',
          y is not None and all(int(y) <= p < int(y) + 8 for p in pos),
          f'yScroll={y}, righe={pos}')
    check('e drumsScrollOffset non viene toccato',
          clip.get('drumsScrollOffset') == prima_dso,
          f'{prima_dso} -> {clip.get("drumsScrollOffset")}')


def test_le_righe_di_kit_si_contano_per_posizione_non_per_drumindex():
    """Sul dispositivo l'ordine delle righe di un kit lo decide l'utente.

    Riordinarle cambia l'ordine dei nodi `<noteRow>`; i `drumIndex` restano
    quelli che sono, perche' puntano al drum e non alla riga. Nel corpus ne
    esiste un esemplare, `Xmasjam1.XML`, con l'ordine
    [4, 6, 8, 10, 12, 14, 0, 1, 2, 3, 5, 7, 9, 11].

    La fixture qui sotto e' costruita apposta perche' i due modelli diano
    risposte OPPOSTE: la riga che suona sta in POSIZIONE 0 -- gia' a schermo,
    niente da correggere -- ma porta `drumIndex=12`, che finirebbe fuori da
    una finestra 0-7. Nei file normali le due cose coincidono, ed e' per
    questo che la differenza e' facile da non vedere.
    """
    doc = parse('<?xml version="1.0" encoding="UTF-8"?>\n<song>\n'
                '\t<sessionClips>\n'
                '\t\t<instrumentClip affectEntire="1" drumsScrollOffset="0">\n'
                '\t\t\t<noteRows>\n'
                '\t\t\t\t<noteRow drumIndex="12" />\n'
                '\t\t\t\t<noteRow drumIndex="0" />\n'
                '\t\t\t\t<noteRow drumIndex="1" />\n'
                '\t\t\t</noteRows>\n\t\t</instrumentClip>\n'
                '\t</sessionClips>\n</song>\n')
    clip = S.clips(doc)[0][1]
    riga = S.note_rows(clip)[0]
    S.write_notes(riga, [Note(pos=0, length=24)], create=True)
    check('la fixture ha i nodi fuori ordine di drumIndex',
          [r.get('drumIndex') for r in S.note_rows(clip)] == ['12', '0', '1'])

    check('la riga che suona si conta per posizione',
          S.drum_rows_sounding(clip) == [0], str(S.drum_rows_sounding(clip)))
    check('quindi e gia a schermo e non si segnala niente',
          S.notes_hidden_by_scroll(doc) == [], str(S.notes_hidden_by_scroll(doc)))
    check('e il fit la porta alla riga 0, non alla 12 del suo drumIndex',
          S.fit_clip_scroll_to_notes(doc, clip) == {'yScroll': '0'},
          str(clip.get('yScroll')))


def test_avvertenza_copre_anche_le_clip_di_kit():
    """L'avvertenza vede la finestra dei kit, come quella dei synth.

    Il difetto vecchio, riprodotto: `yScroll=37` ereditato da TEMPL0 su una
    clip di kit che ha sedici righe. La finestra resta molto sopra il
    contenuto -- ed e' esattamente cio' che si vedeva sul dispositivo, dovendo
    scrollare in giu' per trovare le note.
    """
    from delugexml import musica as MU                      # noqa: PLC0415
    from delugexml import create as C                       # noqa: PLC0415

    doc = parse_file(REFS / 'songs' / 'TEMPL0.XML')
    _, clip = C.add_track(doc, REFS / 'kits' / 'CR78FROMMARS.XML',
                          name='CR78FROMMARS', folder='KITS', length=384)
    MU.scrivi(doc, clip, MU.passi('x...x...'), dove='Rim CR78 02')

    clip.set('yScroll', '37')               # il difetto vecchio, da TEMPL0
    trovati = S.notes_hidden_by_scroll(doc)
    check('un kit con yScroll ereditato viene segnalato', trovati != [],
          str(trovati))
    check('e il messaggio dice che le righe sono drum',
          trovati and 'righe di drum' in trovati[0],
          trovati[0] if trovati else '')

    S.fit_clip_scroll_to_notes(doc, clip)
    check('dopo il fit tace', S.notes_hidden_by_scroll(doc) == [],
          str(S.notes_hidden_by_scroll(doc)))


def _midi_bytes(ppq, eventi, *, tempo_usec=857142, metro=(4, 4)):
    """Costruisce uno Standard MIDI File minimo, per avere una fixture nota.

    Si scrive qui e non si committa un .mid perche' cosi' il contenuto atteso
    e' visibile accanto all'asserzione: una fixture binaria opaca direbbe
    "28 note" senza far vedere quali.
    `eventi` sono (delta, status, dato1, dato2); status None = running status.
    """
    import struct                                          # noqa: PLC0415

    def vlq(n):
        out = bytearray([n & 0x7F])
        n >>= 7
        while n:
            out.insert(0, (n & 0x7F) | 0x80)
            n >>= 7
        return bytes(out)

    trk = bytearray()
    trk += vlq(0) + b'\xFF\x51\x03' + struct.pack('>I', tempo_usec)[1:]
    trk += vlq(0) + b'\xFF\x58\x04' + bytes(
        [metro[0], metro[1].bit_length() - 1, 24, 8])
    for delta, status, d1, d2 in eventi:
        trk += vlq(delta)
        if status is not None:
            trk += bytes([status])
        trk += bytes([d1]) if d2 is None else bytes([d1, d2])
    trk += vlq(0) + b'\xFF\x2F\x00'
    head = b'MThd' + struct.pack('>IHHh', 6, 1, 1, ppq)
    return head + b'MTrk' + struct.pack('>I', len(trk)) + bytes(trk)


def test_midi_lettura():
    """Il lettore di Standard MIDI File, senza dipendenze esterne.

    Gira col Python di SISTEMA, che non ha mido: e' la ragione per cui il
    lettore e' scritto a mano invece di appoggiarsi al `.venv`.
    """
    import tempfile                                        # noqa: PLC0415
    from delugexml import midi as MI                       # noqa: PLC0415

    # due note simultanee, poi una terza; l'ultima chiusa con note-on vel 0,
    # e la terza scritta in RUNNING STATUS (senza ripetere lo status byte)
    eventi = [
        (0,  0x90, 60, 100),     # do4 on
        (0,  None, 64, 80),      # mi4 on, running status
        (96, 0x80, 60, 0),       # do4 off dopo un movimento
        (0,  0x80, 64, 0),
        (0,  0x90, 67, 120),     # sol4 on
        (48, 0x90, 67, 0),       # off scritto come note-on velocity 0
    ]
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'f.mid'
        p.write_bytes(_midi_bytes(96, eventi))
        f = MI.leggi(p)

        check('legge i PPQ dall intestazione', f.ppq == 96, str(f.ppq))
        check('legge il metro', f.metro == (4, 4), str(f.metro))
        check('legge il tempo', f.bpm is not None and abs(f.bpm - 70) < 0.1,
              str(f.bpm))
        check('trova tutte e tre le note', len(f.note) == 3, str(len(f.note)))

        per_y = {n.y: n for n in f.note}
        check('il running status non perde la seconda nota', 64 in per_y)
        check('due note simultanee restano simultanee',
              per_y[60].pos == per_y[64].pos == 0)
        check('note-on con velocity 0 chiude la nota',
              per_y[67].length == 48, str(per_y[67].length))
        check('le velocity sono quelle scritte',
              (per_y[60].velocity, per_y[64].velocity, per_y[67].velocity)
              == (100, 80, 120))

        # l'altezza MIDI E' la y del Deluge: nessuno scarto di ottava
        from delugexml import musica as MU                 # noqa: PLC0415
        check('do4 del MIDI e do4 di musica.altezza',
              60 == MU.altezza('do4'))

        note, esito = MI.melodia(f)
        check('melodia() torna la forma altezza -> note',
              sorted(note) == [60, 64, 67], str(sorted(note)))
        check('a 96 PPQ la conversione e esatta', esito.esatta, str(esito))
        check('e le posizioni coincidono coi tick del Deluge',
              note[67][0].pos == 96, str(note[67][0].pos))


def test_midi_arrotondamento_e_batteria():
    """L'arrotondamento va DICHIARATO, e la batteria esce per nome GM."""
    import tempfile                                        # noqa: PLC0415
    from delugexml import midi as MI                       # noqa: PLC0415

    # 480 PPQ: il fattore e' 0.2, quindi una posizione non multipla di 5
    # tick MIDI non cade su un tick del Deluge
    eventi = [
        (0,   0x99, 36, 100),    # kick, canale 10 (0x99 = note on ch 9)
        (7,   0x89, 36, 0),      # off a tick 7: 7 * 0.2 = 1.4, arrotonda
        (0,   0x99, 42, 64),
        (5,   0x89, 42, 0),
        (0,   0x99, 84, 90),     # altezza fuori dalla mappa GM
        (5,   0x89, 84, 0),
    ]
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'd.mid'
        p.write_bytes(_midi_bytes(480, eventi))

        drum, esito = MI.batteria(p)
        check('i drum escono col nome General MIDI',
              'kick' in drum and 'charleston chiuso' in drum,
              str(sorted(drum)))
        check('un altezza fuori mappa non viene persa in silenzio',
              'nota 84' in drum, str(sorted(drum)))
        check('l arrotondamento viene dichiarato',
              not esito.esatta and esito.arrotondate > 0, str(esito))
        check('e il rapporto dice quanto si e perso',
              'micro-tempistica' in str(esito), str(esito))

        # il canale 10 non deve finire fra le note melodiche
        mel, _ = MI.melodia(p)
        check('la batteria resta fuori dalle note melodiche', mel == {},
              str(mel))

        testo = MI.racconta(p)
        check('racconta() dichiara la conversione non intera',
              'arrotondate' in testo or 'kick' in testo, testo[:80])


def test_passi_tre_livelli():
    """`o` e' il colpo fantasma: il terzo livello di velocity.

    Con due soli livelli un groove marcia. Il fantasma e' quello che non si
    sente come evento ma come tessuto, e sta sotto 70 su 127.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    ns = MU.passi('X.o.x...')
    check('tre caratteri danno tre note', len(ns) == 3, str(len(ns)))
    check('e tre velocity diverse, in ordine',
          [n.velocity for n in ns] == [MU.VEL_ACCENTO, MU.VEL_FANTASMA,
                                       MU.VEL_COLPO],
          str([n.velocity for n in ns]))
    check('il fantasma sta sotto la soglia dei 70',
          MU.VEL_FANTASMA < 70, str(MU.VEL_FANTASMA))
    check('e cade al posto giusto nella griglia',
          [n.pos for n in ns] == [0, 2 * MU.TICK_PER_PASSO,
                                  4 * MU.TICK_PER_PASSO],
          str([n.pos for n in ns]))

    ns = MU.passi('o.o.', fantasma=30)
    check('il livello del fantasma si puo scegliere',
          [n.velocity for n in ns] == [30, 30], str([n.velocity for n in ns]))

    check('un carattere ancora sconosciuto resta un errore',
          _raises(lambda: MU.passi('x.q.'), ValueError))

    # i pattern gia' scritti non cambiano comportamento
    vecchio = MU.passi('X...x...')
    check('x e X si comportano come prima',
          [n.velocity for n in vecchio] == [MU.VEL_ACCENTO, MU.VEL_COLPO],
          str([n.velocity for n in vecchio]))


def test_fm_da_un_preset_subtractive():
    """Portare il synth vuoto in FM crea i modulatori e toglie le forme d onda.

    Il synth vuoto del dispositivo e' subtractive e NON ha i modulatori: senza
    crearli, `mode="fm"` lascerebbe un suono in uno stato che il dispositivo
    non scrive mai.
    """
    from delugexml import structure as ST                   # noqa: PLC0415
    from delugexml import sound as SND                      # noqa: PLC0415

    pr = REFS / 'synths' / 'TEMPL.XML'
    if not pr.exists():
        salta('fm da subtractive', 'TEMPL.XML assente')
        return
    inst = parse_file(pr).root

    check('il synth vuoto non ha modulatori',
          inst.find('modulator1') is None and inst.find('modulator2') is None)
    check('e i suoi oscillatori hanno una forma d onda',
          inst.find('osc1').get('type') == 'square')

    ST.set_synth_mode(inst, 'fm')
    check('passando a FM i modulatori vengono creati',
          inst.find('modulator1') is not None
          and inst.find('modulator2') is not None)
    check('e stanno subito dopo osc2, come nei file del dispositivo',
          [c.tag for c in inst.children][:4]
          == ['osc1', 'osc2', 'modulator1', 'modulator2'],
          str([c.tag for c in inst.children][:4]))
    check('modulator2 porta toModulator1, modulator1 no',
          inst.find('modulator2').has('toModulator1')
          and not inst.find('modulator1').has('toModulator1'))
    check('gli oscillatori perdono type, come nei suoni FM del corpus',
          not inst.find('osc1').has('type')
          and not inst.find('osc2').has('type'))
    check('e describe() lo racconta',
          'FM' in (ST.describe(inst).get('osc1') or ''),
          str(ST.describe(inst).get('osc1')))

    # i livelli dei modulatori sono parametri, non struttura
    SND.set(inst, 'modulator1Amount', 34)
    check('il livello del modulatore e un parametro, e si scrive',
          SND.get(inst, 'modulator1Amount') == 34,
          str(SND.get(inst, 'modulator1Amount')))

    # chiamarla due volte non duplica
    prima = len(inst.children)
    ST.ensure_fm_modulators(inst)
    check('chiamarla di nuovo non duplica i modulatori',
          len(inst.children) == prima, str(len(inst.children)))


def test_patch_cable():
    """Creare, aggiornare e togliere un patch cable.

    E' il pezzo che mancava per progettare un suono da zero: senza, non si
    fanno ne' il wobble (`lfo1 -> lpfFrequency`) ne' la sirena dub
    (`lfo1 -> pitch`), che sono patch cable e nient'altro.
    """
    from delugexml import sound as SND                      # noqa: PLC0415
    from delugexml import params as P                       # noqa: PLC0415

    pr = REFS / 'synths' / 'TEMPL.XML'
    if not pr.exists():
        salta('patch cable', 'TEMPL.XML assente')
        return
    inst = parse_file(pr).root

    check('il contenitore di un preset e defaultParams',
          SND.container(inst) is not None
          and SND.container(inst).tag == 'defaultParams',
          str(SND.container(inst) and SND.container(inst).tag))

    partenza = len(SND.patch_cables(inst))
    check('TEMPL parte con i suoi tre cable', partenza == 3, str(partenza))

    r = SND.set_patch_cable(inst, 'lfo1', 'lpfFrequency', 28)
    check('il wobble viene creato', r['azione'] == 'creato')
    check('e il rapporto dice che e terreno battuto',
          r['visto_nel_corpus'] == 12 and not r['mai_visto'],
          str(r['visto_nel_corpus']))
    check('non e segnalato come inefficace', r['inefficace'] is False)

    letti = {(c['source'], c['destination']): c['amount']
             for c in SND.patch_cables(inst)}
    check('e si rilegge dal nodo',
          ('lfo1', 'lpfFrequency') in letti)
    check('con l amount vicino a quello chiesto',
          abs(letti[('lfo1', 'lpfFrequency')] - 28) < 0.01,
          str(letti[('lfo1', 'lpfFrequency')]))

    # aggiornare non duplica
    r2 = SND.set_patch_cable(inst, 'lfo1', 'lpfFrequency', -15)
    check('riscrivere lo stesso cable lo aggiorna e non lo duplica',
          r2['azione'] == 'aggiornato'
          and len(SND.patch_cables(inst)) == partenza + 1,
          str(len(SND.patch_cables(inst))))
    check('il rapporto dice da dove a dove',
          abs(r2['da'] - 28) < 0.01 and r2['a'] == -15, str(r2['da']))
    check('un amount negativo si rilegge negativo',
          abs([c['amount'] for c in SND.patch_cables(inst)
               if c['destination'] == 'lpfFrequency'
               and c['source'] == 'lfo1'][0] + 15) < 0.01)

    # polarity non si scrive: non si e' capito cosa sia
    nuovo = r2['nodo']
    check('polarity non viene scritta', not nuovo.has('polarity'))

    # la regola del manuale sui parametri globali
    g = SND.set_patch_cable(inst, 'envelope2', 'delayRate', 20)
    check('modulare un parametro globale con un inviluppo e segnalato',
          g['inefficace'] is True)
    g2 = SND.set_patch_cable(inst, 'lfo1', 'delayRate', 20)
    check('ma con LFO1 no, perche LFO1 e globale', g2['inefficace'] is False)

    # una coppia sensata mai usata dall'utente NON e' un errore
    m = SND.set_patch_cable(inst, 'envelope3', 'lpfFrequency', 10)
    check('una sorgente mai vista nel corpus viene comunque scritta',
          m['azione'] == 'creato' and m['mai_visto'] is True)

    # ma un nome inventato si
    check('sorgente inventata rifiutata',
          _raises(lambda: SND.set_patch_cable(inst, 'lfo9', 'volume', 10),
                  ValueError))
    check('destinazione inventata rifiutata',
          _raises(lambda: SND.set_patch_cable(inst, 'lfo1', 'wobbliness', 10),
                  ValueError))
    check('force scrive comunque',
          SND.set_patch_cable(inst, 'lfo9', 'wobbliness', 10,
                              force=True)['azione'] == 'creato')
    check('amount fuori dai -50..+50 rifiutato',
          _raises(lambda: SND.set_patch_cable(inst, 'lfo1', 'volume', 80),
                  ValueError))

    check('togliere un cable dice che c era',
          SND.remove_patch_cable(inst, 'lfo1', 'lpfFrequency') is True)
    check('e toglierlo due volte dice di no',
          SND.remove_patch_cable(inst, 'lfo1', 'lpfFrequency') is False)

    # il fondoscala del manuale, verificato contro params.py
    check('+50 e mezzo int32, come dice FINDINGS',
          P.cable_from_display(50).upper() == '0X40000000',
          P.cable_from_display(50))


def test_patch_cable_tabelle():
    """Le tabelle dei cable si ri-derivano dal corpus e coincidono.

    Serve a due cose diverse:
      - `COPPIE_OSSERVATE` e' stata generata da uno script e poi incollata:
        senza questo test una trascrizione sbagliata non si vedrebbe;
      - ogni sorgente e ogni destinazione che compare in un file reale deve
        stare nelle nostre tabelle. Il contrario NON e' richiesto: la
        tabella e' piu' larga del corpus di proposito, perche' il corpus dice
        cosa l'utente ha suonato, non cosa il firmware accetta.
    """
    from collections import Counter                         # noqa: PLC0415
    from delugexml import sound as SND                      # noqa: PLC0415

    radici = [REFS, ROOT / 'corpus_versions']
    coppie = Counter()
    sorgenti, destinazioni = set(), set()
    n_file = 0
    for radice in radici:
        if not radice.exists():
            continue
        for p in sorted(radice.rglob('*.XML')):
            try:
                doc = parse_file(p)
            except Exception:                        # noqa: BLE001, PERF203
                continue
            n_file += 1
            pila = [doc.root]
            while pila:
                n = pila.pop()
                if n.tag == 'patchCable':
                    s, d = n.get('source'), n.get('destination')
                    if s:
                        sorgenti.add(s)
                    if d and d != 'none':
                        destinazioni.add(d)
                    if s and d and d != 'none':
                        coppie[(s, d)] += 1
                pila.extend(n.children)

    if len(coppie) < 50:
        salta('tabelle dei patch cable',
              f'servono le song del corpus (trovate {len(coppie)} coppie '
              f'in {n_file} file)')
        return

    check('ogni sorgente osservata sta in SORGENTI',
          sorgenti <= set(SND.SORGENTI),
          str(sorted(sorgenti - set(SND.SORGENTI))))

    ammesse = set(SND.destinazioni_disponibili())
    check('ogni destinazione osservata sta fra i parametri del firmware',
          destinazioni <= ammesse,
          str(sorted(destinazioni - ammesse)))

    check('COPPIE_OSSERVATE coincide con quella ri-derivata dal corpus',
          dict(coppie) == SND.COPPIE_OSSERVATE,
          f'{len(coppie)} derivate contro {len(SND.COPPIE_OSSERVATE)} '
          f'in tabella; differenze: '
          f'{sorted(set(coppie.items()) ^ set(SND.COPPIE_OSSERVATE.items()))[:4]}')

    # la tabella e' piu' larga del corpus, ed e' voluto
    check('le destinazioni del firmware sono piu di quelle usate',
          len(ammesse) > len(destinazioni),
          f'{len(ammesse)} contro {len(destinazioni)}')


def test_patch_cable_su_drum():
    """Un drum di kit e' un <sound>: ci si progetta il suono come su un synth.

    E' la premessa dei kit sintetizzati — senza `defaultParams` fra i
    contenitori, `container()` su un drum tornava None e non c'era modo di
    toccarne i parametri.
    """
    from delugexml import sound as SND                      # noqa: PLC0415
    from delugexml import kit as K                          # noqa: PLC0415
    from delugexml import structure as ST                   # noqa: PLC0415

    p = REFS / 'kits' / '808 Essential.XML'
    if not p.exists():
        salta('patch cable su drum', '808 Essential.XML assente')
        return
    kit_doc = parse_file(p)
    drum = K.copy_drum(kit_doc.root, 0)

    check('un drum ha un contenitore di parametri',
          SND.container(drum) is not None,
          str(SND.container(drum) and SND.container(drum).tag))
    check('e i suoi parametri si leggono',
          SND.get(drum, 'volume') is not None, str(SND.get(drum, 'volume')))

    # da campione a sintetizzato: e' la struttura a decidere
    ST.set_osc(drum, 1, type='sine', transpose=-24)
    check('l oscillatore diventa una sinusoide grave',
          drum.find('osc1').get('type') == 'sine'
          and drum.find('osc1').get('transpose') == '-24')

    r = SND.set_patch_cable(drum, 'envelope2', 'oscAPitch', -40)
    check('e il pitch drop del kick si scrive sul drum',
          r['azione'] == 'creato' and r['visto_nel_corpus'] == 4,
          str(r['visto_nel_corpus']))
    check('rileggendolo dal drum lo si ritrova',
          any(c['source'] == 'envelope2' and c['destination'] == 'oscAPitch'
              for c in SND.patch_cables(drum)))


# ------------------------------------------------ sigle di accordo e voicing

def test_sigla_fondamentale_due_lingue():
    """La fondamentale usa lo STESSO vocabolario di `altezza()`.

    Non e' un vezzo: duplicare il parser delle altezze e' gia' costato un
    difetto silenzioso a questo progetto (`set_scale` faceva
    `upper().replace('B','#')`, e 'Ab' diventava A# invece di G#). Qui la
    fondamentale passa dalla stessa strada, quindi non puo' divergere.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    coppie = [('C', 0), ('do', 0), ('Bb', 10), ('sib', 10),
              ('F#', 6), ('fa#', 6), ('Eb', 3), ('mib', 3)]
    for testo, atteso in coppie:
        check(f'sigla({testo!r}) ha fondamentale {atteso}',
              MU.sigla(testo).fondamentale == atteso,
              str(MU.sigla(testo).fondamentale))


def test_sigla_tabella_di_riferimento():
    """I valori attesi vengono dal documento, non dal mio codice.

    Sono la «quick parser table from C» di
    `music-composition/assets/chord-symbol-ambiguity-and-parsing.md`,
    trascritta come intervalli in semitoni sopra la fondamentale. E' la
    stessa disciplina della coppia controllata: il valore atteso deve venire
    da fuori, altrimenti il test conferma soltanto l'idea che avevo in testa.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    attesi = {
        'C':        (0, 4, 7),          # C E G
        'Cm':       (0, 3, 7),          # C Eb G
        'C-':       (0, 3, 7),
        'Cdim':     (0, 3, 6),          # C Eb Gb
        'Caug':     (0, 4, 8),          # C E G#
        'Csus4':    (0, 5, 7),          # C F G
        'Csus2':    (0, 2, 7),          # C D G
        'C5':       (0, 7),             # C G
        'C7':       (0, 4, 7, 10),      # C E G Bb
        'Cmaj7':    (0, 4, 7, 11),      # C E G B
        'Cm7':      (0, 3, 7, 10),      # C Eb G Bb
        'Cm7b5':    (0, 3, 6, 10),      # C Eb Gb Bb
        'Cdim7':    (0, 3, 6, 9),       # C Eb Gb Bbb(=A)
        'Cm(maj7)': (0, 3, 7, 11),      # C Eb G B
        'Cmaj7#11': (0, 4, 7, 11, 18),  # C E G B F#
        'C7b9':     (0, 4, 7, 10, 13),  # C E G Bb Db
        'C7#9':     (0, 4, 7, 10, 15),  # C E G Bb D#
        'C7b13':    (0, 4, 7, 10, 20),  # C E G Bb Ab
        'C13':      (0, 4, 7, 10, 14, 21),   # C E G Bb D A
        'Cadd9':    (0, 4, 7, 14),      # C E G D
        'C6/9':     (0, 4, 7, 9, 14),   # C E G A D
    }
    for testo, atteso in attesi.items():
        got = MU.sigla(testo).intervalli
        check(f'{testo} = {atteso}', got == atteso, str(got))


def test_sigla_ambiguita_dichiarata():
    """Le sigle ambigue si leggono in UN modo e si DICE quale.

    Il documento elenca le letture possibili e la scelta di default. Il
    difetto da evitare non e' scegliere: e' scegliere in silenzio.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    s = MU.sigla('C2')
    check('C2 si legge come sus2', s.intervalli == (0, 2, 7), str(s.intervalli))
    check('e la lettura viene dichiarata', bool(s.letto_come), str(s.letto_come))
    check('nominando anche l alternativa scartata',
          'add9' in (s.letto_come or ''), str(s.letto_come))

    check('Calt si legge come C7alt',
          bool(MU.sigla('Calt').letto_come), str(MU.sigla('Calt').letto_come))
    check('una sigla NON ambigua non inventa avvertenze',
          MU.sigla('Cm7').letto_come is None)


def test_sigla_basso_e_sigla_ignota():
    from delugexml import musica as MU                      # noqa: PLC0415

    s = MU.sigla('C/E')
    check('lo slash da un basso', s.basso == 4, str(s.basso))
    check('e non tocca l accordo sopra', s.intervalli == (0, 4, 7))

    try:
        MU.sigla('Cfrullato')
        check('una sigla ignota viene rifiutata', False, 'nessun errore')
    except ValueError as e:
        check('una sigla ignota viene rifiutata', True)
        check('e l errore elenca cosa esiste', 'maj7' in str(e), str(e)[:90])


def test_voicing_chiuso_e_drop2():
    """Drop 2 col valore preso dal documento.

    `jazz-voicings.md`: Cmaj7 in posizione chiusa e' C-E-G-B; la seconda
    voce dall'alto e' G; il drop 2 risultante e' **G - C - E - B**.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    chiuso = MU.voci('Cmaj7', voicing='chiuso', registro='do4')
    check('chiuso = do mi sol si a partire da do4',
          chiuso == [60, 64, 67, 71], str(chiuso))

    drop = MU.voci('Cmaj7', voicing='drop2', registro='do4')
    check('drop2 abbassa la seconda voce dall alto di un ottava',
          drop == [55, 60, 64, 71], str(drop))
    check('e il documento la scrive sol-do-mi-si',
          [MU.nome_altezza(y) for y in drop] == ['sol3', 'do4', 'mi4', 'si4'],
          str([MU.nome_altezza(y) for y in drop]))


def test_voicing_shell_e_senza_fondamentale():
    """Shell = 3 e 7. Senza fondamentale = 3-5-7-9.

    I due valori attesi vengono dalle tabelle di `jazz-voicings.md`:
    Dm7 senza fondamentale e' F-A-C-E, Cmaj7 e' E-G-B-D.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    shell = MU.voci('C7', voicing='shell', registro='do4')
    check('lo shell di do7 sono mi e sib, due note sole',
          [MU.nome_altezza(y) for y in shell] == ['mi4', 'la#4'], str(shell))

    dm7 = MU.voci('Dm7', voicing='senza-fondamentale', registro='do4')
    check('re-7 senza fondamentale: fa la do mi',
          [MU.nome_altezza(y) for y in dm7] == ['fa4', 'la4', 'do5', 'mi5'],
          str([MU.nome_altezza(y) for y in dm7]))

    cmaj7 = MU.voci('Cmaj7', voicing='senza-fondamentale', registro='do4')
    check('domaj7 senza fondamentale: mi sol si re',
          [MU.nome_altezza(y) for y in cmaj7] == ['mi4', 'sol4', 'si4', 're5'],
          str([MU.nome_altezza(y) for y in cmaj7]))

    check('e nessuna delle due porta la fondamentale',
          all(y % 12 != 2 for y in dm7) and all(y % 12 != 0 for y in cmaj7))


def test_sigla_due_slash():
    """`C6/9/E` ha DUE slash e vogliono dire cose diverse.

    Difetto vero, trovato provando a mano dopo che i test erano gia' verdi:
    l'ultimo slash e' il basso, quello dentro `6/9` fa parte della sigla.
    Trattandone uno solo la sigla restava illeggibile.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    s = MU.sigla('C6/9/E')
    check('il basso e il mi', s.basso == 4, str(s.basso))
    check('e la sigla resta un 6/9',
          s.intervalli == (0, 4, 7, 9, 14), str(s.intervalli))
    check('e senza basso funziona lo stesso',
          MU.sigla('C6/9').basso is None
          and MU.sigla('C6/9').intervalli == (0, 4, 7, 9, 14))


def test_voicing_senza_fondamentale_estensioni():
    """Le estensioni DICHIARATE non si buttano.

    Valori attesi dalle tabelle di `jazz-voicings.md`:
      C13   3-5-7-9-13  -> E - G - Bb - D - A
      C7#11 senza la 5  -> E - Bb - D - F#
      C7alt (esempio su E, trasposto)  -> 3, b7, b9, b13
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    c13 = MU.voci('C13', voicing='senza-fondamentale', registro='do4')
    check('do13: mi sol sib re la',
          [MU.nome_altezza(y) for y in c13]
          == ['mi4', 'sol4', 'la#4', 're5', 'la5'],
          str([MU.nome_altezza(y) for y in c13]))

    c7s11 = MU.voci('C7#11', voicing='senza-fondamentale', registro='do4')
    check('do7#11 perde la quinta: mi sib re fa#',
          [MU.nome_altezza(y) for y in c7s11]
          == ['mi4', 'la#4', 're5', 'fa#5'],
          str([MU.nome_altezza(y) for y in c7s11]))

    alt = MU.voci('C7alt', voicing='senza-fondamentale', registro='do4')
    check('do7alt tiene b9 e b13: mi sib do# sol#',
          [MU.nome_altezza(y) for y in alt]
          == ['mi4', 'la#4', 'do#5', 'sol#5'],
          str([MU.nome_altezza(y) for y in alt]))


def test_voicing_senza_settima_e_rifiutato():
    """Shell e rootless su una triade non esistono: si rifiuta, non si tira a
    indovinare. Una triade non ha settima, e un voicing 3-7 senza 7 sarebbe
    un'invenzione silenziosa."""
    from delugexml import musica as MU                      # noqa: PLC0415

    for v in ('shell', 'senza-fondamentale'):
        try:
            MU.voci('C', voicing=v)
            check(f'{v} su una triade viene rifiutato', False, 'nessun errore')
        except ValueError as e:
            check(f'{v} su una triade viene rifiutato', True)
            check(f'e {v} spiega perche', 'settima' in str(e), str(e)[:80])


def test_armonia_stessa_forma_di_accordi():
    """`armonia()` deve poter entrare in `scrivi()` come `accordi()`.

    Stessa forma di ritorno (`altezza -> note`), stessa posizione per le note
    di uno stesso accordo: e' il vincolo che la fa atterrare nella macchina
    che esiste gia', invece di chiederne una nuova.
    """
    from delugexml import musica as MU                      # noqa: PLC0415

    a = MU.armonia('Dm7 | G7 | Cmaj7', voicing='chiuso', durata='1/4')
    check('il ritorno e un dizionario altezza -> note', isinstance(a, dict))
    check('le note sono Note', all(isinstance(n, Note)
                                   for ns in a.values() for n in ns))

    passo = MU.durata_in_tick('1/4')
    posizioni = sorted({n.pos for ns in a.values() for n in ns})
    check('tre accordi danno tre posizioni',
          posizioni == [0, passo, 2 * passo], str(posizioni))

    primo = sorted(y for y, ns in a.items() if any(n.pos == 0 for n in ns))
    check('e le note del primo accordo stanno tutte a zero',
          len(primo) == 4, str(primo))


def test_armonia_pausa_registro_e_basso():
    from delugexml import musica as MU                      # noqa: PLC0415

    passo = MU.durata_in_tick('1/4')
    a = MU.armonia('C | . | C', voicing='chiuso', durata='1/4')
    posizioni = sorted({n.pos for ns in a.values() for n in ns})
    check('un punto e una pausa: occupa il passo e non suona',
          posizioni == [0, 2 * passo], str(posizioni))

    basso = MU.armonia('C/E', voicing='chiuso', registro='do4')
    check('il basso dello slash sta SOTTO il voicing',
          min(basso) == MU.altezza('mi3'),
          MU.nome_altezza(min(basso)))

    alto = MU.voci('Cmaj7', voicing='chiuso', registro='do5')
    check('il registro sposta tutto di un ottava',
          alto == [72, 76, 79, 83], str(alto))


def test_racconta_armonia():
    """Regola 4: un'operazione silenziosa non e' correggibile."""
    from delugexml import musica as MU                      # noqa: PLC0415

    testo = MU.racconta_armonia('C2 | Dm7', voicing='chiuso')
    check('il racconto nomina il voicing', 'chiuso' in testo, testo[:70])
    check('il racconto nomina le note vere', 'sol' in testo, testo[:120])
    check('e dichiara la lettura ambigua di C2',
          'sus2' in testo and 'add9' in testo, testo[:200])


# ------------------------------------------------ Weimar Jazz Database

def test_wjazz_dialetto():
    """La notazione di accordo di Weimar e' un DIALETTO, e va tradotta.

    Non e' un caso limite: il 22% delle 30 548 occorrenze del database non e'
    leggibile da `MU.sigla()`, e i fallimenti sono tutti sistematici --
    `j7` per maj7, l'alterazione DOPO il grado (`79b` = 7b9), `o` per il
    diminuito, `sus7` invece di `7sus4`.

    Sta qui e non in `MU.SIGLE` di proposito: `SIGLE` e' la notazione da lead
    sheet, comune a tutte le fonti. Il dialetto appartiene alla SORGENTE, e
    infilarlo nella tabella generale la sporcherebbe per sempre con le
    abitudini di un database solo.

    I valori attesi vengono dalla grammatica, non dal codice: quality prefix,
    poi una `j` che rende maggiore la settima che segue, poi una lista di
    gradi ognuno con la sua alterazione in coda.
    """
    from delugexml import musica as MU                      # noqa: PLC0415
    from delugexml import wjazz as WJ                       # noqa: PLC0415

    attesi = {
        'Ebj7':     (3,  (0, 4, 7, 11)),          # maj7
        'D79b':     (2,  (0, 4, 7, 10, 13)),      # 7b9
        'C79':      (0,  (0, 4, 7, 10, 14)),      # 9 di dominante
        'G79#':     (7,  (0, 4, 7, 10, 15)),      # 7#9
        'Fsus7':    (5,  (0, 5, 7, 10)),          # 7sus4
        'Co':       (0,  (0, 3, 6)),              # triade diminuita
        'Co7':      (0,  (0, 3, 6, 9)),           # settima diminuita
        'G+7':      (7,  (0, 4, 8, 10)),          # 7#5
        'C-79':     (0,  (0, 3, 7, 10, 14)),      # m9
        'C-7911':   (0,  (0, 3, 7, 10, 14, 17)),  # m11
        'C-69':     (0,  (0, 3, 7, 9, 14)),       # m6/9
        'C-j7':     (0,  (0, 3, 7, 11)),          # m(maj7)
        'Ebj7911#': (3,  (0, 4, 7, 11, 14, 18)),  # maj7 con 9 e #11
        'C79b13b':  (0,  (0, 4, 7, 10, 13, 20)),  # 7b9b13
    }
    for testo, (fond, intervalli) in attesi.items():
        s = WJ.sigla_weimar(testo)
        check(f'{testo} -> {intervalli}',
              s.fondamentale == fond and s.intervalli == intervalli,
              f'{s.fondamentale} {s.intervalli}')

    check('lo slash resta un basso', WJ.sigla_weimar('Cj7/A').basso == 9,
          str(WJ.sigla_weimar('Cj7/A').basso))
    check('NC non e un accordo e torna None',
          WJ.sigla_weimar('NC') is None)
    check('e nemmeno una casella vuota', WJ.sigla_weimar('') is None)

    # Dove i due dialetti COINCIDONO devono dare lo stesso risultato: se no
    # una delle due letture e' sbagliata e nessuno se ne accorgerebbe.
    for comune in ('C7', 'C-7', 'C', 'C6', 'C-6', 'Csus', 'Cm7b5'):
        check(f'{comune} letto uguale dai due dialetti',
              WJ.sigla_weimar(comune).intervalli == MU.sigla(comune).intervalli,
              f'{WJ.sigla_weimar(comune).intervalli} vs '
              f'{MU.sigla(comune).intervalli}')


def test_wjazz_dialetto_rifiuta():
    from delugexml import wjazz as WJ                       # noqa: PLC0415

    try:
        WJ.sigla_weimar('Cfrullato')
        check('una coda ignota viene rifiutata', False, 'nessun errore')
    except ValueError as e:
        check('una coda ignota viene rifiutata', True)
        check('e l errore mostra cosa non ha saputo leggere',
              'frullato' in str(e), str(e)[:90])


def test_wjazz_lettura():
    """Lettura vera del database. SALTA se non c'e': non e' roba del repo.

    I valori attesi vengono dal database stesso, che qui e' l'artefatto in
    esame -- solo 1 e' `Anthropology` di Art Pepper, che e' un rhythm
    changes in sib, e infatti la griglia comincia Bb6 | Bb6 G7 | C-7 F7.
    """
    from delugexml import wjazz as WJ                       # noqa: PLC0415

    db = ROOT / 'to-read' / 'MIDI' / 'wjazzd.db'
    if not db.exists():
        raise FileNotFoundError(str(db))

    check('il database ha 456 assoli', WJ.quanti(db) == 456, str(WJ.quanti(db)))

    s = WJ.solo(db, 1)
    check('il primo e Art Pepper', s.performer == 'Art Pepper', s.performer)
    check('su Anthropology', s.title == 'Anthropology', s.title)
    check('stile COOL, feel SWING',
          s.style == 'COOL' and s.rhythmfeel == 'SWING',
          f'{s.style} {s.rhythmfeel}')

    note, conv = WJ.melodia(db, 1)
    check('530 note lette', conv.note == 530, str(conv.note))
    check('la prima nota sta a tick 0',
          min(n.pos for ns in note.values() for n in ns) == 0)

    # (bar,beat,tatum,division) delle prime note, dal database:
    #   (0,1,1,1) (0,2,1,4) (0,2,4,4) (0,3,1,1) (0,4,1,1) (1,1,1,1)
    # con 96 tick per movimento e 4 movimenti per battuta:
    #   0, 96, 96+72=168, 192, 288, 384
    posizioni = sorted({n.pos for ns in note.values() for n in ns})[:6]
    check('le prime sei posizioni seguono la griglia metrica',
          posizioni == [0, 96, 168, 192, 288, 384], str(posizioni))

    acc = WJ.armonia(db, 1)
    check('la griglia comincia con Bb6',
          acc[0].testo == 'Bb6' and acc[0].tick == 0,
          f'{acc[0].testo} @ {acc[0].tick}')
    check('e prosegue col rhythm changes Bb6 G7 C-7 F7',
          [a.testo for a in acc[1:5]] == ['Bb6', 'G7', 'C-7', 'F7'],
          str([a.testo for a in acc[1:5]]))
    check('gli accordi portano una Sigla gia sciolta',
          acc[3].sigla is not None and acc[3].sigla.intervalli == (0, 3, 7, 10),
          str(acc[3].sigla and acc[3].sigla.intervalli))

    testo = WJ.racconta(db, 1)
    check('racconta() nomina esecutore e pezzo',
          'Art Pepper' in testo and 'Anthropology' in testo, testo[:60])
    check('e dichiara la conversione', 'note' in testo, testo[:120])


def test_wjazz_conversione_dichiarata():
    """Le suddivisioni 5 e 10 NON dividono 96: 19,2 e 9,6 tick.

    Sono 7242 note su 200 809 in tutto il database, il 3,6%. La conversione
    le arrotonda -- e deve DIRLO, come fa `midi.py`, perche' li' se ne va
    proprio la micro-tempistica per cui questo database vale.
    """
    from delugexml import wjazz as WJ                       # noqa: PLC0415

    db = ROOT / 'to-read' / 'MIDI' / 'wjazzd.db'
    if not db.exists():
        raise FileNotFoundError(str(db))

    # un assolo con quintine dentro: si cerca quello, non si suppone
    melid = WJ.con_suddivisione(db, 5)
    if melid is None:
        salta('test_wjazz_conversione_dichiarata', 'nessuna quintina')
        return
    _, conv = WJ.melodia(db, melid)
    check('la conversione dichiara di aver arrotondato',
          conv.arrotondate > 0 and not conv.esatta, str(conv))
    check('e lo scarto massimo e sotto mezzo tick',
          conv.scarto_massimo <= 0.5, f'{conv.scarto_massimo:.3f}')


def test_wjazz_levare_nucleo():
    """Il calcolo del levare, su dati costruiti a mano.

    E' la parte pura: un movimento che va da t0 a t1, e dentro esattamente
    due eventi. Dove cade il secondo, in frazione del movimento, E' lo swing.
    0,5 e' dritto; 0,667 e' la terzina, cioe' BUR 2.
    """
    from delugexml import wjazz as WJ                       # noqa: PLC0415

    battiti = [(1, 1, 0.0), (1, 2, 1.0), (1, 3, 2.0), (1, 4, 3.0), (2, 1, 4.0)]

    dritto = WJ.levare_da_dati(battiti, [(1, 1, 1, 0.0), (1, 1, 2, 0.5)])
    check('due eventi a meta movimento danno 0,5', dritto == [0.5], str(dritto))

    terzina = WJ.levare_da_dati(battiti, [(1, 2, 1, 1.0), (1, 2, 3, 1.6667)])
    check('a due terzi danno la terzina', abs(terzina[0] - 2 / 3) < 1e-3,
          str(terzina))
    check('e in BUR e 2', abs(WJ.in_bur(terzina[0]) - 2.0) < 0.02,
          f'{WJ.in_bur(terzina[0]):.3f}')

    tre = WJ.levare_da_dati(battiti, [(1, 3, 1, 2.0), (1, 3, 2, 2.3),
                                      (1, 3, 3, 2.6)])
    check('un movimento con TRE eventi non e una coppia di crome',
          tre == [], str(tre))

    senza = WJ.levare_da_dati(battiti, [(1, 4, 2, 3.2), (1, 4, 3, 3.6)])
    check('se il primo evento non e sul movimento, si scarta',
          senza == [], str(senza))

    fuori = WJ.levare_da_dati(battiti, [(1, 1, 1, 0.0), (1, 1, 2, 0.95)])
    check('un levare fuori finestra si scarta', fuori == [], str(fuori))


def test_wjazz_levare_non_usa_la_griglia_annotata():
    """La posizione ANNOTATA non va usata: contiene gia' lo swing.

    E' l'errore che ha bruciato tre tentativi. I trascrittori di Weimar
    scrivono una coppia di crome swingate come `tatum 1 e 3 di division 3`,
    cioe' la terzina e' gia' nella griglia metrica. Filtrare su
    `division == 2` selezionava percio' le sole coppie giudicate DRITTE, e la
    misura tornava 1,0 per costruzione.

    Qui si verifica che il `tatum` del secondo evento non cambi il risultato:
    conta solo dove cade l'onset VERO.
    """
    from delugexml import wjazz as WJ                       # noqa: PLC0415

    battiti = [(1, 1, 0.0), (1, 2, 1.0)]
    for tatum in (2, 3, 5):
        got = WJ.levare_da_dati(battiti, [(1, 1, 1, 0.0), (1, 1, tatum, 0.62)])
        check(f'con tatum={tatum} il levare resta 0,62',
              got and abs(got[0] - 0.62) < 1e-6, str(got))


def test_wjazz_swing_misurato():
    """La misura vera sul database. SALTA se non c'e'.

    Due previsioni della letteratura, che qui servono da controllo esterno:
    lo swing **cala al salire del tempo**, e i generi a crome dritte stanno
    **sotto** lo swing. Se non compaiono, la misura e' sbagliata -- ed e'
    esattamente cosi' che sono stati scoperti i tre tentativi precedenti.
    """
    from delugexml import wjazz as WJ                       # noqa: PLC0415

    db = ROOT / 'to-read' / 'MIDI' / 'wjazzd.db'
    if not db.exists():
        raise FileNotFoundError(str(db))

    tutto = WJ.swing(db)
    check('la misura copre piu di 300 assoli', tutto.assoli > 300,
          str(tutto.assoli))
    check('il levare sta fra il 55% e il 68% del movimento',
          0.55 < tutto.levare < 0.68, f'{tutto.levare:.3f}')
    check('cioe un BUR fra 1,2 e 2,1 -- swingato, non dritto e non terzina',
          1.2 < tutto.bur < 2.1, f'{tutto.bur:.2f}')

    swing_feel = WJ.swing(db, rhythmfeel='SWING')
    funk = WJ.swing(db, rhythmfeel='FUNK')
    check('SWING e piu swingato di FUNK',
          swing_feel.bur > funk.bur,
          f'SWING {swing_feel.bur:.2f} vs FUNK {funk.bur:.2f}')

    lento = WJ.swing(db, tempo_min=120, tempo_max=180)
    veloce = WJ.swing(db, tempo_min=240)
    check('e lo swing cala al salire del tempo',
          lento.bur > veloce.bur,
          f'120-180 {lento.bur:.2f} vs >240 {veloce.bur:.2f}')

    check('un filtro che non seleziona niente non esplode',
          WJ.swing(db, rhythmfeel='NON-ESISTE').assoli == 0)


def test_swing_intervallo_misurato():
    """L'intervallo di swing, ancorato sul dispositivo il 17 agosto 2026.

    Cinque salvataggi, uno per posizione del menu, piu' l'ascolto:

        schermo   swingInterval   figura swingata
        2nd            4            1/2
        4th            5            1/4
        8th            6            1/8      <- il jazz
        16th           7            1/16     <- default del firmware
        32nd           8            1/32

    L'etichetta nomina **la figura che viene swingata**: le note si muovono a
    coppie di quella figura, e a spostarsi e' la seconda della coppia (in
    ritardo sopra 50, in anticipo sotto).

    ⚠️ La prima versione di questo test asseriva l'intervallo 5, derivandolo
    dall'aritmetica del sorgente (`3 << (10 - swingInterval)`). Era sbagliata
    di un fattore 2, e l'ha scoperto l'utente ascoltando: quinta volta su
    cinque che ha ragione lui quando dice che qualcosa non torna. Lo scarto
    col sorgente e' dichiarato in `song.SWING_SCARTO_SORGENTE`.
    """
    misurato = {4: '1/2', 5: '1/4', 6: '1/8', 7: '1/16', 8: '1/32'}
    check('la tabella e quella misurata sul dispositivo',
          S.SWING_FIGURA_PER_INTERVALLO == misurato,
          str(S.SWING_FIGURA_PER_INTERVALLO))
    check('per swingare le CROME serve l intervallo 6',
          S.swing_intervallo_per('1/8') == 6)
    check('il default del firmware, 7, swinga le semicrome',
          S.SWING_INTERVALLO_DEFAULT == 7
          and S.SWING_FIGURA_PER_INTERVALLO[7] == '1/16')
    check('la tabella e biiettiva',
          all(S.swing_intervallo_per(f) == v
              for v, f in S.SWING_FIGURA_PER_INTERVALLO.items()))

    try:
        S.swing_intervallo_per('1/3')
        check('una figura ignota viene rifiutata', False, 'nessun errore')
    except ValueError as e:
        check('una figura ignota viene rifiutata', True)
        check('e l errore elenca quelle del menu',
              '1/8' in str(e), str(e)[:80])


def test_swing_display_e_posizione_del_levare():
    """Il display E' la percentuale di posizione del levare.

    Derivato dal sorgente (`playback_handler.cpp`): la prima meta' del blocco
    va per `(50 + swingAmount)/50`, la seconda per `(50 - swingAmount)/50`,
    quindi il punto di mezzo cade a `(50 + swingAmount)/100 = display/100`.

    Controprova nota: la terzina e' BUR 2, cioe' display 66,7.
    """
    base = REFS / 'songs' / 'TEMPL0.XML'
    if not base.exists():
        raise FileNotFoundError(str(base))
    doc = parse_file(base)

    S.set_swing(doc, 50)
    check('50 e dritto: swingAmount 0', S.get_swing(doc)[0] == 50
          and doc.root.get('swingAmount') == '0')

    S.set_swing(doc, 67, figura='1/8')
    display, intervallo = S.get_swing(doc)
    bur = display / (100 - display)
    check('67 da la terzina (BUR 2)', abs(bur - 2.0) < 0.05, f'{bur:.2f}')
    check('e figura=1/8 ha scelto l intervallo 6', intervallo == 6)

    # lo swing del jazz misurato sulla Weimar: levare al 61,7%
    S.set_swing(doc, 62, figura='1/8')
    d = S.get_swing(doc)[0]
    check('il jazz misurato sta a 62, cioe BUR 1,6',
          abs(d / (100 - d) - 1.63) < 0.05, f'{d / (100 - d):.2f}')

    try:
        S.set_swing(doc, 62, 5, figura='1/8')
        check('interval= e figura= insieme sono rifiutati', False, 'nessuno')
    except ValueError:
        check('interval= e figura= insieme sono rifiutati', True)


def test_nessuna_clip_in_play():
    """Una song la cui unica clip ha isPlaying=0 si carica e non suona.

    Difetto vero, trovato sul dispositivo il 17 agosto 2026: il Deluge si
    bloccava premendo play. `create.add_track()` ha `playing=False` di
    DEFAULT, e nessun controllo del progetto se ne accorgeva -- `verifica()`,
    `check_clip_types()` e il round-trip erano tutti puliti.

    Informa e non blocca: nel corpus 10 song su 146 sono in questo stato, e
    sono song vere salvate da ferme.
    """
    from delugexml import create as C                       # noqa: PLC0415
    from delugexml import musica as MU                      # noqa: PLC0415

    base = REFS / 'songs' / 'TEMPL0.XML'
    if not base.exists():
        raise FileNotFoundError(str(base))
    preset = REFS / 'synths' / 'TEMPL.XML'

    doc = parse_file(base)
    vecchio = doc.root.find('instruments').children[0]
    _, clip = C.add_track(doc, preset, name='MUTA', folder='SYNTHS')
    MU.togli(doc, vecchio)
    check('senza playing=True nessuna clip parte',
          any('isPlaying' in a for a in S.no_playing_clip(doc)),
          str(S.no_playing_clip(doc)))
    check('e l avvertenza arriva fino a avvertenze()',
          any('isPlaying' in a for a in MU.avvertenze(doc)))
    check('ma NON blocca: verifica() resta vuota',
          MU.verifica(doc) == [], str(MU.verifica(doc)))

    doc2 = parse_file(base)
    vecchio2 = doc2.root.find('instruments').children[0]
    C.add_track(doc2, preset, name='VIVA', folder='SYNTHS', playing=True)
    MU.togli(doc2, vecchio2)
    check('con playing=True l avvertenza sparisce',
          S.no_playing_clip(doc2) == [], str(S.no_playing_clip(doc2)))

    vuota = parse_file(base)
    for c in list(vuota.root.find('sessionClips').children):
        vuota.root.find('sessionClips').remove(c)
    check('una song senza clip di sessione non viene accusata',
          S.no_playing_clip(vuota) == [], str(S.no_playing_clip(vuota)))


# ------------------------------------------------- docs: lo schema neutro

REPERTORI = ROOT / 'docs' / 'repertori'

#: Le undici caselle dello schema neutro, nell'ordine fisso. Il testo del
#: titolo e' il numero, un punto, uno spazio e questa stringa. Vedi
#: docs/superpowers/specs/2026-08-17-musica-schema-neutro-design.md
CASELLE = [
    "Cos'è, e cosa non è",
    'Metro e griglia',
    'Tempo',
    'Feel',
    'Ruoli e spartizione',
    'Dinamica',
    'Armonia',
    'Melodia e ornamentazione',
    'Forma e densità',
    'Sul Deluge',
    'Trappole del generatore',
]


def _caselle_di(path):
    """I titoli di casella di una scheda, nell'ordine in cui compaiono.

    Una casella e' un titolo di livello 2 esatto: '### ' non conta, cosi'
    una scheda puo' articolarsi dentro una casella senza confondere il test.
    """
    righe = path.read_text(encoding='utf-8').splitlines()
    return [r.rstrip() for r in righe if r.startswith('## ')]


def test_schede_repertorio_hanno_le_undici_caselle():
    attesi = [f'## {i}. {c}' for i, c in enumerate(CASELLE, 1)]
    schede = sorted(REPERTORI.glob('*.md')) if REPERTORI.is_dir() else []
    check('esistono le schede di repertorio', len(schede) >= 1,
          f'{len(schede)} in {REPERTORI}')
    for s in schede:
        trovati = _caselle_di(s)
        check(f'{s.name}: le undici caselle, tutte e in ordine',
              trovati == attesi,
              f'{len(trovati)} titoli, primo scarto: '
              + next((f'atteso {a!r} trovato {t!r}'
                      for a, t in zip(attesi, trovati) if a != t), 'nessuno'))


#: L'indice di MUSICA.md usa simboli; i test stampano su console Windows,
#: dove un carattere non-ASCII in una stringa stampata solleva
#: UnicodeEncodeError. Si traduce prima di stampare, mai dopo.
SIMBOLI = {'●': 'pieno', '◐': 'parziale', '○': 'vuoto'}


def _stato_di(path):
    """Lo stato delle undici caselle, letto dalla prima riga non vuota di ognuna.

    Convenzione: '**Vuota' -> vuoto, '**Parziale.**' -> parziale, altro ->
    pieno. Il prefisso di 'Vuota' e' senza punto perche' una casella puo'
    dire '**Vuota, ed e' la piu' vicina a chiudersi.**'
    """
    stato, attesa = [], False
    for riga in path.read_text(encoding='utf-8').splitlines():
        if riga.startswith('## '):
            attesa = True
            stato.append(None)
        elif attesa and riga.strip():
            attesa = False
            t = riga.strip()
            stato[-1] = ('vuoto' if t.startswith('**Vuota')
                         else 'parziale' if t.startswith('**Parziale.**')
                         else 'pieno')
    return stato


def _righe_indice():
    """Le righe della matrice di MUSICA.md, come [(nome file, [stati])].

    Una lista e non un dizionario: due righe che linkano alla stessa scheda
    sono un difetto da vedere, e in un dizionario la seconda cancellerebbe la
    prima in silenzio, cioe' l'indice tornerebbe coerente proprio perche' e'
    sbagliato.
    """
    fuori = []
    for riga in (ROOT / 'docs' / 'MUSICA.md').read_text(encoding='utf-8').splitlines():
        if not riga.startswith('|') or '](repertori/' not in riga:
            continue
        celle = [c.strip() for c in riga.strip('|').split('|')]
        nome = celle[0].split('](repertori/')[1].rstrip(')')
        fuori.append((nome, [SIMBOLI.get(c.strip('* '), c) for c in celle[1:]]))
    return fuori


def test_indice_repertori_coerente_con_le_schede():
    righe = _righe_indice()
    nomi = [n for n, _ in righe]
    doppi = sorted({n for n in nomi if nomi.count(n) > 1})
    check('l indice non ha due righe per la stessa scheda',
          not doppi, f'ripetute: {doppi}')
    indice = dict(righe)
    schede = sorted(REPERTORI.glob('*.md')) if REPERTORI.is_dir() else []
    check('l indice nomina tutte le schede',
          set(indice) == {s.name for s in schede},
          f'indice {sorted(indice)} vs schede {[s.name for s in schede]}')
    for s in schede:
        vero = _stato_di(s)
        check(f'{s.name}: nessuna casella senza stato leggibile',
              None not in vero and len(vero) == 11, str(vero))
        check(f'{s.name}: l indice coincide con la scheda',
              indice.get(s.name) == vero,
              f'indice {indice.get(s.name)} vs scheda {vero}')


def test_bur_in_comune():
    """L'aritmetica del BUR sta in `musica`, e i due lettori la condividono.

    Stava in `wjazz.py`. Serve anche a `groove.py`, e le alternative erano
    duplicarla (vietato) o far dipendere un corpus dall'altro (assurdo).
    """
    from delugexml import musica as MU                      # noqa: PLC0415
    from delugexml import wjazz as WJ                       # noqa: PLC0415

    check('dritto e BUR 1', MU.in_bur(0.5) == 1.0, str(MU.in_bur(0.5)))
    check('la terzina e BUR 2', abs(MU.in_bur(2 / 3) - 2.0) < 1e-9,
          str(MU.in_bur(2 / 3)))
    check('il jazz misurato, 61,7%, da 1,61',
          abs(MU.in_bur(0.617) - 1.61) < 0.01, f'{MU.in_bur(0.617):.3f}')

    for bur in (1.0, 1.61, 2.0, 3.0):
        check(f'da_bur e l inverso di in_bur, BUR {bur}',
              abs(MU.in_bur(MU.da_bur(bur)) - bur) < 1e-9,
              f'{MU.in_bur(MU.da_bur(bur))}')

    check('un levare fuori da (0,1) e un errore',
          _raises(lambda: MU.in_bur(1.0), ValueError))
    check('e `wjazz` usa la stessa funzione, non una copia',
          WJ.in_bur is MU.in_bur)


def test_groove_prefisso():
    """`reggae` prende `reggae/slow` e NON `latin/reggaeton`.

    La sottostringa e' la regola sbagliata, ed e' scritta come controesempio
    nella casella 6 di `docs/repertori/jazz.md`. Nucleo puro: nessun file.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    check('un prefisso prende se stesso', GR.per_prefisso('reggae', 'reggae'))
    check('e prende la sottocategoria',
          GR.per_prefisso('reggae/slow', 'reggae'))
    check('ma NON una parola che lo contiene',
          not GR.per_prefisso('latin/reggaeton', 'reggae'))
    check('ne una che ci somiglia',
          not GR.per_prefisso('latin/brazilian-sambareggae', 'reggae'))
    check('jazz prende jazz/funk', GR.per_prefisso('jazz/funk', 'jazz'))
    check('e non prende funk', not GR.per_prefisso('funk', 'jazz'))


def test_groove_inventario():
    """Lettura vera del dataset. SALTA se non c'e': non e' roba del repo.

    I conteggi vengono dal dataset stesso, che qui e' l'artefatto in esame,
    e sono lo stato del disco del 18 agosto 2026.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    base = ROOT / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
    if not (base / GR.INVENTARIO).exists():
        raise FileNotFoundError(str(base / GR.INVENTARIO))

    tutte = GR.elenco(base)
    check('il dataset ha 1150 esecuzioni', len(tutte) == 1150, str(len(tutte)))

    jazz = GR.elenco(base, style='jazz')
    check('101 esecuzioni jazz', len(jazz) == 101, str(len(jazz)))
    beat = GR.elenco(base, style='jazz', beat_type='beat')
    check('di cui 50 `beat`', len(beat) == 50, str(len(beat)))
    check('e 5 batteristi', len({e.drummer for e in jazz}) == 5,
          str(sorted({e.drummer for e in jazz})))

    reggae = GR.elenco(base, style='reggae')
    check('20 esecuzioni reggae', len(reggae) == 20, str(len(reggae)))
    # ⚠️ L'ETICHETTA DICEVA "UN batterista" e l'asserzione ne pretendeva DUE:
    # stampava `PASS ma UN batterista...` fra i 943, cioe' rivendeva come
    # verde proprio l'errore che il commit `3a0052e` di questo ramo esiste
    # per correggere. Corretta l'etichetta, non l'asserzione: i batteristi
    # reggae sono due (drummer1 e drummer5), misurati su `info.csv`.
    check('ma DUE batteristi e sole quattro `beat`',
          len({e.drummer for e in reggae}) == 2
          and len([e for e in reggae if e.beat_type == 'beat']) == 4,
          f'{sorted({e.drummer for e in reggae})}, '
          f'{len([e for e in reggae if e.beat_type == "beat"])} beat')
    check('e nessuna e reggaeton',
          all(not e.style.startswith('latin') for e in reggae),
          str(sorted({e.style for e in reggae})))


def test_groove_id_sbagliato_dice_quante_ce_ne_sono():
    """L'errore su un id inesistente dice quante esecuzioni ci sono in tutto.

    Rilievo di revisione: la docstring di `_una()` prometteva "un errore che
    dice quante ce ne sono", ma il messaggio diceva solo cosa mancava, non
    cosa c'era -- lo stesso difetto che `valori()` evita gia' elencando le
    colonne disponibili. Si passa da `racconta()`, l'entrata pubblica, non
    dalla funzione privata.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    base = ROOT / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
    if not (base / GR.INVENTARIO).exists():
        raise FileNotFoundError(str(base / GR.INVENTARIO))

    check('un id inesistente solleva ValueError',
          _raises(lambda: GR.racconta(base, 'non-esiste-questo-id'),
                  ValueError))

    try:
        GR.racconta(base, 'non-esiste-questo-id')
        messaggio = ''
    except ValueError as e:
        messaggio = str(e)
    check('il messaggio nomina l id sbagliato',
          'non-esiste-questo-id' in messaggio, messaggio)
    check('e dice quante esecuzioni ci sono in tutto (1150)',
          '1150' in messaggio, messaggio)
    veri = {e.id for e in GR.elenco(base)}
    check('e mostra almeno un id vero come esempio',
          any(vero in messaggio for vero in veri), messaggio)


def test_groove_origine_della_griglia():
    """Lo scarto comune si stima e si toglie, con la media CIRCOLARE.

    E' il trabocchetto di questo corpus: il tick 0 del file non e' un
    movimento del batterista, e misurare da li' darebbe un anticipo
    sistematico del 5% per OGNI esecuzione. Stesso errore della Weimar,
    nella stessa posizione: l'origine della misura.

    Nucleo puro: liste di numeri, nessun file.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    passo = 24.0                                    # un 1/16 sul Deluge

    dritte = [k * passo for k in range(32)]
    check('senza scarto, l origine e zero',
          abs(GR.origine(dritte, passo)) < 1e-9, str(GR.origine(dritte, passo)))

    avanti = [k * passo + 3 for k in range(32)]
    check('uno scarto di +3 tick si ritrova',
          abs(GR.origine(avanti, passo) - 3) < 1e-9, str(GR.origine(avanti, passo)))

    # il caso che la media aritmetica sbaglia: una fase appena PRIMA del
    # passo successivo e' un anticipo, non un ritardo di quasi un passo.
    indietro = [k * passo - 1 for k in range(1, 32)]
    check('e uno di -1 torna NEGATIVO, non +23',
          abs(GR.origine(indietro, passo) + 1) < 1e-9,
          str(GR.origine(indietro, passo)))

    misto = [k * passo - 1 for k in range(1, 16)] + [k * passo + 1
                                                     for k in range(16, 32)]
    check('scarti opposti si annullano',
          abs(GR.origine(misto, passo)) < 0.1, str(GR.origine(misto, passo)))

    check('senza colpi, l origine e zero e non un errore',
          GR.origine([], passo) == 0.0)

    # i levare swingati NON devono entrare nella stima: stanno a 2/3 di
    # movimento, cioe' a 2,67 passi, e la loro fase e' swing, non origine.
    swingate = [k * passo for k in range(32)] + [
        k * 96 + 64 for k in range(8)]
    check('un levare swingato non sporca l origine',
          abs(GR.origine(swingate, passo)) < 1e-9,
          str(GR.origine(swingate, passo)))

    # il bordo ESATTO della finestra: con passo=24 e finestra di default
    # 0.25, il bordo sta a 6.0 tick. Un colpo li' deve restare ESCLUSO:
    # e' il confronto stretto (< non <=) a deciderlo, ed e' l'unico caso
    # in cui i due operatori danno risultati diversi -- non il levare
    # swingato di sopra, che sta a 8 tick, ben oltre il bordo. Verificato
    # sostituendo < con <= in una copia della funzione: con < l origine
    # resta 0.0 esatto, con <= diventa ~0.123 (il colpo di bordo entra
    # nella media circolare e la sposta).
    bordo = [k * passo for k in range(31)] + [31 * passo + 6.0]
    check('un colpo esattamente sul bordo della finestra resta escluso',
          abs(GR.origine(bordo, passo)) < 1e-9, str(GR.origine(bordo, passo)))


def test_groove_bur_nucleo():
    """Dove cade il levare, su colpi costruiti a mano.

    Un movimento contribuisce solo se dentro la finestra c'e' ESATTAMENTE un
    colpo: due colpi vogliono dire semicrome, e li' una coppia di crome non
    c'e'. Parentela di intento con `WJ.levare_da_dati()`, non identita': la
    Weimar richiede DUE eventi totali nel movimento col primo su tatum 1,
    garanzia piu' stretta di questa, che conta solo i colpi dentro la
    finestra e ignora quanti ce ne siano fuori. Su una batteria -- polifonica,
    a differenza degli assoli monofonici della Weimar -- la garanzia piu'
    debole ammette qualche falso positivo in piu'.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0

    dritto = []
    for k in range(8):
        dritto += [k * ppq, k * ppq + ppq / 2]
    lev = GR.levare_da_posizioni(dritto, ppq)
    check('crome dritte danno il levare a 0,5',
          len(lev) == 8 and all(abs(v - 0.5) < 1e-9 for v in lev), str(lev[:3]))
    check('e in BUR fa 1', abs(GR.bur_da_posizioni(dritto, ppq) - 1.0) < 1e-9,
          str(GR.bur_da_posizioni(dritto, ppq)))

    terzina = []
    for k in range(8):
        terzina += [k * ppq, k * ppq + ppq * 2 / 3]
    check('la terzina da BUR 2',
          abs(GR.bur_da_posizioni(terzina, ppq) - 2.0) < 0.01,
          str(GR.bur_da_posizioni(terzina, ppq)))

    jazz = []
    for k in range(8):
        jazz += [k * ppq, k * ppq + ppq * 0.617]
    check('il levare del jazz misurato da 1,61',
          abs(GR.bur_da_posizioni(jazz, ppq) - 1.61) < 0.02,
          str(GR.bur_da_posizioni(jazz, ppq)))

    semicrome = []
    for k in range(8):
        semicrome += [k * ppq, k * ppq + ppq / 4, k * ppq + ppq / 2,
                      k * ppq + ppq * 3 / 4]
    check('con DUE colpi in finestra il movimento si scarta',
          GR.levare_da_posizioni(semicrome, ppq) == [],
          str(GR.levare_da_posizioni(semicrome, ppq)))

    check('senza coppie il BUR e None',
          GR.bur_da_posizioni([0.0, 96.0, 192.0], ppq) is None)

    # posizioni negative e non a partire da zero: e' la forma esatta in cui
    # il Task 5 le passera' (gia' traslate). Il raggruppamento per movimento
    # usa floor-division (`p // ppq`): con il troncamento (`int(p / ppq)`)
    # un movimento su due perderebbe il proprio levare, che finirebbe
    # accorpato nel movimento accanto -- vedi la nota nel codice.
    negativo = []
    for k in range(1, 9):               # movimenti -8..-1, mai zero
        negativo += [-k * ppq, -k * ppq + ppq / 2]
    lev_neg = GR.levare_da_posizioni(negativo, ppq)
    check('posizioni negative danno lo stesso levare a 0,5 e nel movimento giusto',
          len(lev_neg) == 8 and all(abs(v - 0.5) < 1e-9 for v in lev_neg),
          str(lev_neg))
    check('e in BUR fa 1 anche sul negativo',
          abs(GR.bur_da_posizioni(negativo, ppq) - 1.0) < 1e-9,
          str(GR.bur_da_posizioni(negativo, ppq)))

    # il bordo superiore ESATTO della finestra (0,75): e' la semicroma che
    # FINESTRA_LEVARE dichiara di voler escludere, e un colpo isolato li'
    # non deve MAI passare per levare, anche da solo in finestra.
    bordo_esatto = [0.0, 0.75 * ppq]
    check('un colpo isolato esattamente sul bordo (0,75) non e il levare',
          GR.levare_da_posizioni(bordo_esatto, ppq) == [],
          str(GR.levare_da_posizioni(bordo_esatto, ppq)))


def test_groove_profilo_nucleo():
    """La catena: origine, poi BUR, poi il RESIDUO. In quest'ordine.

    Su un'esecuzione costruita a mano che swinga a BUR 2 e ha un ride
    spostato di +2 tick rispetto a tutto il resto: il template deve portare
    quel +2 e NON lo swing, che sul Deluge lo fa `set_swing()`. Se portasse
    anche lo swing, lo swing verrebbe applicato due volte.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0

    # ---- fixture A: swing. Tutti i colpi SULLA griglia hanno lo stesso
    # scarto (+2), cosi' l'origine e' esattamente 2 e il BUR viene esatto.
    a = {'kick': [], 'ride': []}
    for b in range(16):                             # 16 movimenti = 4 battute
        a['kick'].append((b * ppq + 2, 100))
        a['ride'].append((b * ppq + 2, 90))
        a['ride'].append((b * ppq + 2 + ppq * 2 / 3, 70))

    pa = GR.profilo_da_colpi(a, ppq)
    check('il BUR misurato e 2', abs(pa.bur - 2.0) < 0.02, str(pa.bur))
    check('quattro battute', pa.battute == 4, str(pa.battute))

    # ⚠️ IL TEST CHE CONTA. Il levare swingato sta a 2,67 passi: senza
    # togliere lo swing finirebbe arrotondato al passo 3. Se e' sul 2, lo
    # swing e' stato tolto -- ed e' giusto che lo sia, perche' sul Deluge lo
    # rimette `set_swing()`, e due volte sarebbe una volta di troppo.
    ride = {s.passo for s in pa.passi['ride']}
    check('il levare swingato cade sul passo 2, non sul 3',
          2 in ride and 3 not in ride, str(sorted(ride)))

    r2 = [s for s in pa.passi['ride'] if s.passo == 2][0]
    check('e senza residuo, perche lo swing era tutto lo scarto',
          abs(r2.scarto) < 0.6, str(r2.scarto))
    check('con la sua velocity piu bassa', r2.velocity == 70, str(r2.velocity))

    k0 = [s for s in pa.passi['kick'] if s.passo == 0][0]
    check('il kick porta la sua velocity', k0.velocity == 100, str(k0.velocity))
    check('e quante volte e stato colpito', k0.colpi == 4, str(k0.colpi))
    check('uno strumento assente non compare', 'rullante' not in pa.passi,
          str(sorted(pa.passi)))

    # ---- fixture B: il residuo RELATIVO, senza swing di mezzo.
    #
    # ⚠️ Si misura la DIFFERENZA fra strumenti, non il valore assoluto: se
    # il kick sta a 0 e il ride a +2, non esiste un'origine "vera" che dica
    # quale dei due e' spostato. E' la ragione per cui la scheda dichiara
    # sempre un DIVARIO fra due pad -- il charleston a pedale che anticipa il
    # ride -- e mai un anticipo assoluto.
    #
    # ⚠️ IL SEGNO. `Passo.scarto` POSITIVO = il colpo cade DOPO la griglia
    # (ritarda), NEGATIVO = prima (anticipa); il sito definitorio e'
    # `groove.Passo.scarto`. Qui il ride sta a `b*ppq + 2`, cioe' DUE TICK
    # PIU' TARDI del kick: quindi TRATTIENE, non spinge. Fino al 19 agosto
    # 2026 queste due etichette dicevano il rovescio.
    b_ = {'kick': [], 'ride': []}
    for b in range(16):
        b_['kick'].append((b * ppq, 100))
        b_['ride'].append((b * ppq + 2, 90))

    pb = GR.profilo_da_colpi(b_, ppq)
    dk = [s for s in pb.passi['kick'] if s.passo == 0][0].scarto
    dr = [s for s in pb.passi['ride'] if s.passo == 0][0].scarto
    check('il ride TRATTIENE di 2 tick RISPETTO al kick',
          abs((dr - dk) - 2) < 0.6, f'{dr:.2f} - {dk:.2f}')


def test_groove_senza_grazia():
    """La catena e' l'INVERSA ESATTA della mappa dello swing, anche in fondo.

    ⚠️ IL DIFETTO CHE QUESTO TEST BLINDA, e come si rifa'. Fino al 24 agosto
    2026 `profilo_da_colpi()` calcolava il movimento con mezzo passo di
    grazia:

        movimento = math.floor(p / ppq + 0.125)

    Una nota nell'ultimo ottavo di movimento usciva allora con fase
    NEGATIVA, e `_senza_swing()` le applicava il ramo della PRIMA meta'
    (dilatata) mentre la nota sta nella SECONDA (compressa): non l'inversa
    di niente che il firmware faccia. Sul corpus jazz del Groove MIDI
    toccava un colpo su tre.

    La fixture costruisce le posizioni applicando la mappa IN AVANTI a
    posizioni dritte note, e chiede indietro quelle. E' l'unico modo per cui
    il test non sia la stessa formula contro se' stessa: il valore atteso
    non viene da `_senza_swing()`, viene da `con_swing()`.

    ⚠️ I tre anticipi sono scelti perche' cadono nell'ultimo ottavo (dove
    stava il difetto) e insieme abbastanza lontano dal battere da restare
    FUORI dalla finestra di `origine()` (piu' di 6 tick swingati): se no
    l'origine si sposterebbe e il valore atteso non sarebbe piu' esatto.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0
    lev = 2.0 / 3.0                     # BUR 2, la terzina: numeri esatti

    def con_swing(u, levare):
        """La mappa del firmware IN AVANTI: da fase dritta a fase swingata."""
        if u < 0.5:
            return u * 2 * levare
        return levare + (u - 0.5) * 2 * (1 - levare)

    campione = [k / 100 for k in range(100)]
    check('_senza_swing e l inversa della mappa in avanti su tutto [0,1)',
          all(abs(GR._senza_swing(con_swing(u, lev), lev) - u) < 1e-12
              for u in campione),
          str(max(abs(GR._senza_swing(con_swing(u, lev), lev) - u)
                  for u in campione)))

    def fixture(anticipo):
        """Kick e ride sulla griglia swingata, piu' un pad che ANTICIPA.

        Il pad suona `anticipo` tick DRITTI prima del battere seguente: e'
        una posizione dritta nota, portata avanti dalla mappa dello swing.
        """
        c = {'kick': [], 'ride': [], 'charleston a pedale': []}
        for b in range(16):
            c['kick'].append((b * ppq, 100))
            c['ride'].append((b * ppq, 90))
            c['ride'].append((b * ppq + con_swing(0.5, lev) * ppq, 70))
            u = 1.0 - anticipo / ppq
            c['charleston a pedale'].append(
                (b * ppq + con_swing(u, lev) * ppq, 80))
        return c

    p10 = GR.profilo_da_colpi(fixture(10.0), ppq)
    check('la fixture dichiara la terzina, e l origine non la sposta',
          abs(p10.bur - 2.0) < 1e-9, str(p10.bur))

    # ---- il CONTROLLO: fuori dall'ultimo ottavo la catena era gia' esatta.
    # Il ride sta sul battere e sul levare swingato, e li' i due conti --
    # con la grazia e senza -- coincidono. Se questo controllo fallisse, a
    # essere rotta sarebbe la fixture, non il difetto.
    ride = {s.passo: s.scarto for s in p10.passi['ride']}
    check('il ride sul battere e sul levare non porta residuo',
          sorted(ride) == [0, 2, 4, 6, 8, 10, 12, 14]
          and all(abs(v) < 1e-9 for v in ride.values()),
          str({k: round(v, 4) for k, v in ride.items()}))

    # ---- 10 tick dritti di anticipo: il passo resta il battere, il residuo
    # deve essere -10 ESATTI. Con la grazia usciva -5,0: meta'.
    ped = {s.passo: s.scarto for s in p10.passi['charleston a pedale']}
    check('10 tick dritti di anticipo restano sul battere',
          sorted(ped) == [0, 4, 8, 12], str(sorted(ped)))
    check('e il residuo e -10 tick esatti, non la meta',
          all(abs(v + 10.0) < 1e-9 for v in ped.values()),
          str({k: round(v, 4) for k, v in ped.items()}))

    # ---- 14 e 17 tick: qui cambia anche il PASSO. Un colpo a 14 tick dritti
    # dal battere e' piu' vicino alla semicroma precedente (a 24) che al
    # battere, e la sedicesima e' dove va. La grazia lo attaccava al battere
    # con un residuo di -7: un residuo che nessun batterista ha suonato.
    for anticipo, passi_attesi, atteso in ((14.0, [3, 7, 11, 15], +10.0),
                                           (17.0, [3, 7, 11, 15], +7.0)):
        pr = GR.profilo_da_colpi(fixture(anticipo), ppq)
        d = {s.passo: s.scarto for s in pr.passi['charleston a pedale']}
        check(f'{anticipo:.0f} tick dritti di anticipo cadono sulla semicroma '
              f'precedente', sorted(d) == passi_attesi, str(sorted(d)))
        check(f'e il residuo e {atteso:+.0f} tick esatti',
              all(abs(v - atteso) < 1e-9 for v in d.values()),
              str({k: round(v, 4) for k, v in d.items()}))

    # ⚠️ LA GIUSTIFICAZIONE CHE LA GRAZIA SI DAVA, FALSIFICATA. Il commento
    # diceva che senza di essa "il residuo uscirebbe grande quanto un
    # movimento intero". Non puo': `passo = round(dritta / passo_tick)`
    # sceglie il passo PIU' VICINO, quindi |residuo| <= mezzo passo per
    # costruzione, con la grazia e senza. Misurato anche sul corpus jazz:
    # 0 residui oltre mezzo passo su 28 604 colpi.
    for anticipo in (10.0, 14.0, 17.0):
        pr = GR.profilo_da_colpi(fixture(anticipo), ppq)
        peggio = max(abs(s.scarto)
                     for v in pr.passi.values() for s in v)
        check(f'con anticipo {anticipo:.0f} nessun residuo supera mezzo passo',
              peggio <= ppq / 8 + 1e-9, str(peggio))


def test_groove_profilo_corpus():
    """Il profilo di un'esecuzione vera. SALTA senza il dataset.

    L'esecuzione e' nominata apposta: un profilo viene da UN batterista, e
    dichiararlo e' cio' che tiene onesto il marcatore [OSS].
    """
    import statistics                                      # noqa: PLC0415

    from delugexml import groove as GR                      # noqa: PLC0415

    base = ROOT / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
    if not (base / GR.INVENTARIO).exists():
        raise FileNotFoundError(str(base / GR.INVENTARIO))

    p = GR.profilo(base, 'drummer1/session3/2')
    check('e drummer1 in jazz/swing a 185',
          p.drummer == 'drummer1' and p.style == 'jazz/swing' and p.bpm == 185,
          f'{p.drummer} {p.style} {p.bpm}')
    check('il BUR e fra 1 e 2,5', p.bur is not None and 1.0 < p.bur < 2.5,
          str(p.bur))
    check('c e il ride', 'ride' in p.passi, str(sorted(p.passi))[:120])
    check('ogni passo sta fra 0 e 15',
          all(0 <= s.passo <= 15 for v in p.passi.values() for s in v))
    # ⚠️ QUI C'ERA UNA SOGLIA CHE ERA UN TEOREMA, e va detto perche' non c'e'
    # piu': `abs(s.scarto) <= 12` NON POTEVA FALLIRE. `profilo_da_colpi()`
    # sceglie il passo con `round(dritta / passo_tick)`, cioe' il passo PIU'
    # VICINO, quindi |residuo| <= mezzo passo = 12 tick per costruzione --
    # con la grazia di mezzo passo e senza. Contato sul corpus: 0 residui
    # oltre 12 tick su 28 604 colpi in entrambi i casi. Il registro di
    # sessione la dichiarava "stretta, il 98% del budget": era il rovescio
    # del vero, ed e' il genere di riga che invita ad allargare in futuro una
    # soglia che non si puo' violare.
    #
    # Al suo posto la cosa che il residuo DEVE avere se lo swing e' stato
    # tolto davvero. Lo swing vive sui passi di LEVARE -- 2, 6, 10, 14 -- e
    # li' sposta la nota di `(levare - 0,5) * 96` tick: 9,46 su questa
    # esecuzione. Se `_senza_swing()` fa il suo mestiere quello spostamento
    # sparisce e resta il solo residuo; se non lo facesse resterebbe tutto.
    # VERIFICATO PER INVERSIONE: neutralizzando `_senza_swing()` all'identita'
    # la mediana pesata sui colpi sale da 2,00 a 5,86 tick e questo check
    # diventa rosso.
    levare = GR.da_bur(p.bur)
    meta_swing = (levare - 0.5) * 96 / 2
    sui_levare = [abs(s.scarto) for v in p.passi.values() for s in v
                  if s.passo in (2, 6, 10, 14) for _ in range(s.colpi)]
    mediana = statistics.median(sui_levare)
    check('e sui passi di levare il residuo e meno di meta dello swing tolto',
          mediana < meta_swing,
          f'{mediana:.2f} tick contro {meta_swing:.2f} '
          f'(levare {levare:.4f}, {len(sui_levare)} colpi)')


def test_groove_scala():
    """La scala di velocity, aggregata. SALTA senza il dataset.

    ⚠️ Ogni riga porta quanti BATTERISTI la sostengono, e non e' un dettaglio
    di rendicontazione: e' cio' che decide fra [MIS] e [OSS].

    Il brief originale di questo task diceva che sul reggae del Groove MIDI
    il batterista fosse UNO. Misurato con queste stesse funzioni (`elenco()`
    con `style='reggae'`, `beat_type='beat'`, cioe' il default di `scala()`)
    risultano invece QUATTRO esecuzioni di DUE batteristi (drummer1 e
    drummer5) -- si veda `info.csv`. Il numero giusto e' due, non uno, ma il
    punto resta: contro i cinque del jazz, due non bastano per chiamare
    [MIS] quel che ne esce, e infatti la tabella reggae resta [WEB].
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    base = ROOT / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
    if not (base / GR.INVENTARIO).exists():
        raise FileNotFoundError(str(base / GR.INVENTARIO))

    jazz = GR.scala(base, style='jazz')
    check('il jazz ha il ride', 'ride' in jazz, str(sorted(jazz))[:120])
    r = jazz['ride']
    check('le velocity stanno fra 1 e 127',
          1 <= r.minimo <= r.mediana <= r.massimo <= 127,
          f'{r.minimo}/{r.mediana}/{r.massimo}')
    check('i quartili sono in ordine', r.q1 <= r.mediana <= r.q3,
          f'{r.q1}/{r.mediana}/{r.q3}')
    check('e la riga dichiara 5 batteristi', r.batteristi == 5,
          str(r.batteristi))

    reggae = GR.scala(base, style='reggae')
    check('il reggae ne dichiara al piu due, non cinque come il jazz -- '
          'per questo resta [WEB]',
          max(v.batteristi for v in reggae.values()) == 2,
          str({k: v.batteristi for k, v in reggae.items()}))

    # l'invariante q1 <= mediana <= q3 su jazz['ride'] (sopra) non prova
    # niente sul ramo dei campioni piccoli: 7422 colpi non toccano mai il
    # ripiego sotto i 4. Il reggae si', e ci sta apposta 'crash' con SOLI
    # DUE colpi -- e' il caso che il rilievo di revisione ha trovato rotto.
    rotte = {k: (v.q1, v.mediana, v.q3) for k, v in reggae.items()
             if not (v.q1 <= v.mediana <= v.q3)}
    check('i quartili sono in ordine su OGNI riga del reggae, comprese '
          'quelle con pochissimi colpi (es. crash, 2 colpi)',
          not rotte, str(rotte))
    check('e il reggae ha davvero una riga sotto i 4 colpi, altrimenti il '
          'check sopra non proverebbe niente',
          any(v.colpi < 4 for v in reggae.values()),
          str({k: v.colpi for k, v in reggae.items() if v.colpi < 4}))


def test_applica_groove():
    """Il template posato su un pattern di `passi()`.

    ⚠️ E il RIFIUTO che lo fa valere: su un passo dove quel batterista non ha
    mai suonato, la funzione NON inventa una velocity. E' lo stesso cancello
    della sigla sconosciuta in `MU.armonia()`, e serve alla stessa cosa --
    un template che riempie i buchi da se' sarebbe di nuovo inventare con la
    benedizione della riga scritta per impedirlo.
    """
    from delugexml import musica as MU                      # noqa: PLC0415
    from delugexml import groove as GR                      # noqa: PLC0415

    prof = GR.Profilo(
        id='finto/1', drummer='drummerX', style='jazz', bpm=120, bur=1.6,
        battute=1,
        passi={'ride': [GR.Passo(passo=0, velocity=104, scarto=2.0, colpi=8),
                        GR.Passo(passo=4, velocity=78, scarto=-1.0, colpi=8)]})

    note = MU.passi('x...x...........')
    rapporto = MU.applica_groove(note, prof, dove='ride')

    check('due note toccate', rapporto['toccate'] == 2, str(rapporto))
    check('la prima prende velocity e scarto',
          note[0].velocity == 104 and note[0].pos == 2,
          f'{note[0].velocity} {note[0].pos}')
    # scarto -1 = un tick PRIMA della griglia (vedi `groove.Passo.scarto`):
    # questa nota anticipa, non ritarda.
    check('la seconda ANTICIPA di un tick',
          note[1].velocity == 78 and note[1].pos == MU.TICK_PER_PASSO * 4 - 1,
          f'{note[1].velocity} {note[1].pos}')
    check('e nessun passo e rimasto senza appoggio',
          rapporto['senza_appoggio'] == [], str(rapporto['senza_appoggio']))

    orfane = MU.passi('x.x.x...........')
    r2 = MU.applica_groove(orfane, prof, dove='ride')
    check('il passo 2 non ha appoggio e lo DICE',
          r2['senza_appoggio'] == [2], str(r2['senza_appoggio']))
    check('e quella nota resta com era, non inventata',
          orfane[1].velocity == 90 and orfane[1].pos == MU.TICK_PER_PASSO * 2,
          f'{orfane[1].velocity} {orfane[1].pos}')

    check('uno strumento assente dal profilo e un errore che elenca',
          _raises(lambda: MU.applica_groove(MU.passi('x...'), prof,
                                            dove='rullante'), ValueError))

    # ⚠️ il residuo negativo sul PRIMO passo manderebbe la nota prima
    # dell'inizio della clip, che il Deluge non sa leggere: va fermata a 0.
    presto = GR.Profilo(
        id='finto/2', drummer='drummerX', style='jazz', bpm=120, bur=1.6,
        battute=1,
        passi={'kick': [GR.Passo(passo=0, velocity=100, scarto=-5.0,
                                 colpi=8)]})
    bordo = MU.passi('x...............')
    MU.applica_groove(bordo, presto, dove='kick')
    check('un residuo negativo sul primo passo si ferma a zero',
          bordo[0].pos == 0, str(bordo[0].pos))
    check('ma la velocity la prende lo stesso', bordo[0].velocity == 100,
          str(bordo[0].velocity))


def test_groove_taglio_neutro():
    """Il parametro `taglio` esiste, e chiamare senza equivale a nominarlo.

    ⚠️ FINO AL 26 AGOSTO 2026 questo era il cancello di tutto il confronto
    fra stimatori: il default era `'vicino'`, e se non riproduceva
    esattamente i numeri di prima ogni differenza misurata fra i tagli
    sarebbe stata inattribuibile -- non si sarebbe saputo se l'aveva mossa
    lo stimatore o la ristrutturazione del ciclo. Il Task 6 ha spostato il
    default su `'voce'`; il check resta, ma ora confronta il default con
    `SCELTO` invece che con `'vicino'` -- vedi il commento sopra `SCELTO`.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0
    # due voci, posizioni scelte a mano: un kick sui battere e un ride sulle
    # crome swingate. Nessun colpo al bordo: qui non si misura il bordo, si
    # misura che il refactoring non abbia mosso niente.
    colpi = {
        'kick': [(float(b * 384 + m * 96), 100) for b in range(4)
                 for m in (0, 2)],
        'ride': [(float(b * 384 + m * 96 + d), 80) for b in range(4)
                 for m in range(4) for d in (0, 64)],
    }
    # scelto il 26 agosto 2026: 'voce' vince su scarto massimo mediano
    # (1,47 contro 1,97) e ancoraggio (2 celle contro 5) -- vedi Task 6.
    SCELTO = 'voce'
    check('il default e il taglio scelto il 26 agosto 2026',
          GR.profilo_da_colpi(colpi, ppq, id='finto/1')
          == GR.profilo_da_colpi(colpi, ppq, id='finto/1', taglio=SCELTO),
          SCELTO)

    check('un taglio sconosciuto e un errore che elenca i modi',
          _raises(lambda: GR.profilo_da_colpi(colpi, ppq, taglio='pippo'),
                  ValueError))
    try:
        GR.profilo_da_colpi(colpi, ppq, taglio='pippo')
    except ValueError as e:
        check('e il messaggio nomina i tre modi',
              all(m in str(e) for m in GR.TAGLI), str(e))

    check('lo spostamento di "vicino" e zero',
          GR.spostamento_del_taglio([1.0, 2.0, 3.0], 24.0, 'vicino') == 0.0,
          str(GR.spostamento_del_taglio([1.0, 2.0, 3.0], 24.0, 'vicino')))


def test_groove_taglio_neutro_sul_corpus():
    """Lo stesso cancello, sul dataset vero. SALTA se non c'e'.

    Il caso sintetico non ha colpi al bordo; il corpus ne ha. Se la
    ristrutturazione avesse cambiato qualcosa, e' qui che si vede.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    base = ROOT / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
    if not (base / GR.INVENTARIO).exists():
        raise FileNotFoundError(str(base / GR.INVENTARIO))

    # scelto il 26 agosto 2026: 'voce' vince su scarto massimo mediano
    # (1,47 contro 1,97) e ancoraggio (2 celle contro 5) -- vedi Task 6.
    SCELTO = 'voce'
    for quale in ('drummer1/session3/2', 'drummer10/session1/1'):
        check(f'{quale}: il default e il taglio scelto il 26 agosto 2026',
              GR.profilo(base, quale)
              == GR.profilo(base, quale, taglio=SCELTO),
              f'{quale}')


def test_groove_taglio_voce():
    """`'voce'` chiude la spaccatura di un gesto a cavallo del confine.

    Il caso: una voce che anticipa di 14 tick i passi 4 e 12 -- cioe' il 2 e
    il 4, come il charleston a pedale del jazz -- con dispersione di 3 tick.
    Anticipare di piu' di mezzo passo (12 tick) e' esattamente il caso che
    `round()` non sa rappresentare.

    ⚠️ Questo test NON asserisce su QUALE passo il gesto finisca ancorato.
    L'ancoraggio e' una domanda a se' -- i dati soli non distinguono "14 tick
    prima del passo 4" da "10 tick dopo il passo 3", e il gesto e' pure piu'
    VICINO al passo 3 -- e la MISURA il Task 5. Qui si misura una cosa sola:
    che il gesto smetta di stare in DUE celle con segni opposti.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0
    # 12 battute, il gesto sul passo 4 e sul passo 12, anticipato di 14 tick
    # con dispersione fissa (non casuale: un test deve dare sempre lo stesso
    # numero). 96-14 = 82 e 288-14 = 274, piu' gli scarti.
    posizioni = [float(b * 384 + base + d)
                 for b in range(12) for base in (82, 274)
                 for d in (-3, -1, 1, 3)]
    colpi = {'charleston a pedale': [(p, 90) for p in posizioni]}

    vicino = GR.profilo_da_colpi(colpi, ppq, taglio='vicino')
    voce = GR.profilo_da_colpi(colpi, ppq, taglio='voce')

    def celle(prof):
        return {p.passo: p for p in prof.passi['charleston a pedale']
                if p.colpi >= 10}

    cv, cc = celle(vicino), celle(voce)

    check('con "vicino" il gesto sta in quattro celle (due per battere)',
          len(cv) == 4, str(sorted(cv)))
    coppie = [(k, k + 1) for k in (3, 11) if k in cv and k + 1 in cv]
    check('e sono coppie adiacenti di segno opposto',
          len(coppie) == 2
          and all(cv[a].scarto * cv[b].scarto < 0 for a, b in coppie),
          str({k: round(v.scarto, 2) for k, v in sorted(cv.items())}))
    check('col BATTERE IN MINORANZA: la semicroma prima porta piu colpi',
          all(cv[a].colpi > cv[b].colpi for a, b in coppie),
          str({k: v.colpi for k, v in sorted(cv.items())}))

    check('con "voce" il gesto sta in due celle sole, una per battere',
          len(cc) == 2, str(sorted(cc)))
    check('e ognuna porta tutti i colpi del suo gesto',
          all(v.colpi == 48 for v in cc.values()),
          str({k: v.colpi for k, v in sorted(cc.items())}))

    # lo spostamento e' quello che ci si aspetta da quelle fasi: le fasi
    # sono 7, 9, 11 e -11 tick, la cui media circolare vale +10.
    dritte = [p for p in posizioni]
    sp = GR.spostamento_del_taglio(dritte, 24.0, 'voce')
    check('lo spostamento della voce vale +10 tick',
          abs(sp - 10.0) < 0.01, f'{sp:.3f}')

    # ⚠️ la funzione col cancello sbagliato: GR.origine() ha una finestra
    # che scarta proprio gli anticipati, e qui darebbe zero.
    check('GR.origine() su questa voce da un numero DIVERSO, ed e per questo '
          'che "voce" non la chiama',
          abs(GR.origine(dritte, 24.0) - sp) > 1.0,
          f'origine {GR.origine(dritte, 24.0):.3f} contro voce {sp:.3f}')


def test_groove_taglio_rado():
    """`'rado'` taglia nel mezzo del vuoto, e sulle voci piene non taglia.

    Quattro casi, e il quarto e' quello che conta: uno stimatore deve
    SEGUIRE i dati. I valori attesi sono misurati, non dedotti.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0
    # (a) lo stesso gesto del taglio "voce": anticipo di 14 tick sui passi
    # 4 e 12, dispersione 3. Le fasi sono 7, 9, 11 e 13; il vuoto piu'
    # largo va da 13 a 31, largo 18, e il suo centro cade a 22.
    posizioni = [float(b * 384 + base + d)
                 for b in range(12) for base in (82, 274)
                 for d in (-3, -1, 1, 3)]
    colpi = {'charleston a pedale': [(p, 90) for p in posizioni]}
    rado = GR.profilo_da_colpi(colpi, ppq, taglio='rado')
    celle = {p.passo: p for p in rado.passi['charleston a pedale']
             if p.colpi >= 10}
    check('con "rado" il gesto sta in due celle sole', len(celle) == 2,
          str(sorted(celle)))
    check('e ognuna porta tutti i colpi del suo gesto',
          all(v.colpi == 48 for v in celle.values()),
          str({k: v.colpi for k, v in sorted(celle.items())}))
    sp = GR.spostamento_del_taglio(posizioni, 24.0, 'rado')
    check('lo spostamento e il centro del vuoto meno mezzo passo: +10',
          abs(sp - 10.0) < 1e-9, f'{sp:.3f}')

    # (b) una voce di semicrome PIENE, tutte esattamente sulla griglia.
    # ⚠️ NON e' il caso "densita' piatta": le fasi collassano tutte su
    # ZERO, cioe' e' il caso piu' CONCENTRATO che esista. Il vuoto piu'
    # largo e' allora l'intero passo, il suo centro cade a mezzo passo dai
    # colpi, e lo spostamento esce zero -- che e' giusto, perche' su una
    # voce gia' sulla griglia non c'e' niente da spostare.
    piene = [float(b * 384 + k * 24) for b in range(12) for k in range(16)]
    check('su semicrome sulla griglia "rado" non sposta niente',
          GR.spostamento_del_taglio(piene, 24.0, 'rado') == 0.0,
          str(GR.spostamento_del_taglio(piene, 24.0, 'rado')))
    centro, largo, medio = GR._vuoto_piu_largo(piene, 24.0)
    check('e il vuoto misurato e un passo intero', abs(largo - 24.0) < 1e-9,
          f'centro {centro} largo {largo} medio {medio}')

    # (c) le stesse semicrome con un jitter di +-2 tick: il vuoto resta
    # largo 20 e centrato a 12, quindi ancora nessuno spostamento.
    sporche = [float(b * 384 + k * 24 + (k % 5) - 2)
               for b in range(12) for k in range(16)]
    check('e nemmeno su semicrome con jitter di +-2 tick',
          GR.spostamento_del_taglio(sporche, 24.0, 'rado') == 0.0,
          str(GR.spostamento_del_taglio(sporche, 24.0, 'rado')))

    # (d) ⚠️ LA COSA CHE UNO STIMATORE DEVE SAPER FARE: seguire i dati.
    # Traslando la voce di delta, il taglio si sposta di delta. Avvolge a
    # +-mezzo passo perche' una fase vive su un cerchio, e l'avvolgimento
    # NON e' un salto: sposta anche il passo, quindi la posizione
    # dichiarata resta continua (e' il motivo per cui il Task 4 appaia le
    # celle per posizione dichiarata e non per numero di passo).
    for d in (-8, -6, -4, -2, 2, 4, 6, 8):
        atteso = ((10.0 + d + 12.0) % 24.0) - 12.0
        ottenuto = GR.spostamento_del_taglio(
            [p + d for p in posizioni], 24.0, 'rado')
        check(f'traslando la voce di {d:+d} il taglio si sposta di {d:+d}',
              abs(ottenuto - atteso) < 1e-9,
              f'atteso {atteso:+.2f}, ottenuto {ottenuto:+.2f}')

    # (e) il limite del residuo, che si e' allargato: con un taglio
    # spostato il residuo non sta piu' dentro mezzo passo, ma resta dentro
    # UN passo.
    for taglio in GR.TAGLI:
        p = GR.profilo_da_colpi(colpi, ppq, taglio=taglio)
        peggio = max(abs(s.scarto) for v in p.passi.values() for s in v)
        check(f'taglio {taglio!r}: |scarto| <= un passo intero',
              peggio <= 24.0 + 1e-9, f'{peggio:.3f}')


def test_applica_groove_dice_le_collisioni():
    """Due note su passi adiacenti possono finire sullo stesso tick.

    ⚠️ Diventato possibile il 26 agosto 2026, quando lo scarto ha smesso di
    stare dentro mezzo passo. Non e' vietato -- il Deluge lo accetta -- ma
    va DETTO: un'operazione silenziosa non e' correggibile.
    """
    from delugexml import groove as GR                      # noqa: PLC0415
    from delugexml import musica as MU                      # noqa: PLC0415

    prof = GR.Profilo(
        id='finto/3', drummer='drummerX', style='jazz', bpm=120, bur=1.6,
        battute=1,
        passi={'kick': [GR.Passo(passo=3, velocity=100, scarto=12.0, colpi=20),
                        GR.Passo(passo=4, velocity=100, scarto=-12.0,
                                 colpi=20)]})
    note = MU.passi('...xx...........')
    r = MU.applica_groove(note, prof, dove='kick')
    check('le due note finiscono sullo stesso tick',
          note[0].pos == note[1].pos, f'{note[0].pos} {note[1].pos}')
    check('e il rapporto lo dice', r['collisioni'] == [note[0].pos],
          str(r.get('collisioni')))

    # e quando non c'e' collisione, la lista e' vuota: non si allarma a vuoto
    prof2 = GR.Profilo(
        id='finto/4', drummer='drummerX', style='jazz', bpm=120, bur=1.6,
        battute=1,
        passi={'kick': [GR.Passo(passo=3, velocity=100, scarto=0.0, colpi=20),
                        GR.Passo(passo=4, velocity=100, scarto=0.0,
                                 colpi=20)]})
    r2 = MU.applica_groove(MU.passi('...xx...........'), prof2, dove='kick')
    check('senza collisioni la lista e vuota', r2['collisioni'] == [],
          str(r2['collisioni']))


def test_groove_congelare_origine_e_levare():
    """`profilo_da_colpi()` sa accettare origine e levare dall'esterno.

    ⚠️ Serve alla prova di traslazione per voce: traslando UNA voce si
    muove anche l'origine del KIT, di circa delta per la quota di colpi di
    quella voce. Chi non la congela misura anche quello.
    """
    from delugexml import groove as GR                      # noqa: PLC0415

    ppq = 96.0
    colpi = {
        'kick': [(float(b * 384 + m * 96), 100) for b in range(8)
                 for m in (0, 2)],
        'ride': [(float(b * 384 + m * 96), 80) for b in range(8)
                 for m in range(4)],
    }
    base = GR.profilo_da_colpi(colpi, ppq)
    check('senza congelare, il BUR resta None su colpi tutti sui battere',
          base.bur is None, str(base.bur))

    # tutto il kit spostato di +5: l'origine se lo mangia, il profilo non
    # si muove.
    spostato = {n: [(p + 5.0, v) for p, v in note] for n, note in colpi.items()}
    check('una traslazione COMUNE la riassorbe origine()',
          GR.profilo_da_colpi(spostato, ppq).passi == base.passi)

    # una voce sola spostata di +5: l'origine si muove, ed e' l'artefatto.
    una = dict(colpi)
    una['ride'] = [(p + 5.0, v) for p, v in colpi['ride']]
    libero = GR.profilo_da_colpi(una, ppq)
    congelato = GR.profilo_da_colpi(una, ppq, origine_fissa=0.0,
                                    levare_fisso=0.5)
    k_libero = {p.passo: p.scarto for p in libero.passi['kick']}
    k_congelato = {p.passo: p.scarto for p in congelato.passi['kick']}
    check('senza congelare, il kick NON TRASLATO si muove lo stesso',
          any(abs(k_libero[k]) > 0.01 for k in k_libero),
          str({k: round(v, 2) for k, v in sorted(k_libero.items())}))
    check('congelando, il kick non traslato resta fermo',
          all(abs(v) < 1e-9 for v in k_congelato.values()),
          str({k: round(v, 2) for k, v in sorted(k_congelato.items())}))
    check('e il ride traslato si muove di esattamente +5',
          all(abs(p.scarto - 5.0) < 1e-9
              for p in congelato.passi['ride']),
          str([round(p.scarto, 2) for p in congelato.passi['ride']]))


if __name__ == '__main__':
    for fn in [v for k, v in sorted(globals().items()) if k.startswith('test_')]:
        try:
            fn()
        except FileNotFoundError as e:
            # materiale non pubblicato (song personali, preset di terzi):
            # il test non e' rotto, semplicemente non ha su cosa girare
            salta(fn.__name__, f'manca {e.filename or e}')
        except Exception as e:                       # noqa: BLE001
            check(fn.__name__, False, f'eccezione {type(e).__name__}: {e}')
    n_fail = sum(1 for _, ok, _ in results if not ok)
    print(f'\n{len(results) - n_fail}/{len(results)} test superati')
    if skipped:
        print(f'{len(skipped)} saltati: manca materiale non pubblicabile. '
              f'Vedi README, "Bring your own corpus".')
    sys.exit(1 if n_fail else 0)
