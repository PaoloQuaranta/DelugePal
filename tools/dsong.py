"""dsong - ispezione e modifica di una song Deluge.

Comandi:
    info    <file>                     intestazione, tempo, elenco clip
    notes   <file> [--clip N]          note per riga, decodificate
    tempo   <file> --bpm X -o OUT      cambia il tempo
    note-add <file> --clip N --row R --pos P --len L [--vel V] -o OUT

Ogni scrittura usa la modalita' chirurgica: tutto cio' che non tocchiamo
esce dal file byte per byte com'era. Alla fine viene sempre mostrato il
diff, perche' l'unica verifica che conta e' vedere cosa e' cambiato davvero.
"""
from __future__ import annotations

import argparse
import difflib
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file, serialize, Note          # noqa: E402
from delugexml import song as S                            # noqa: E402
from delugexml.writer import FormatTable                   # noqa: E402

DEFAULT_TABLE = Path(__file__).resolve().parent.parent / 'out' / 'format_table.json'


def load_table():
    if DEFAULT_TABLE.exists():
        return FormatTable.load(DEFAULT_TABLE)
    print(f'! tabella di formato non trovata in {DEFAULT_TABLE}; '
          'i nodi nuovi potrebbero essere formattati male.', file=sys.stderr)
    return FormatTable()


def show_diff(before: str, after: str, name: str) -> int:
    d = list(difflib.unified_diff(before.splitlines(), after.splitlines(),
                                  f'{name} prima', f'{name} dopo',
                                  lineterm='', n=1))
    changed = sum(1 for x in d if x[:1] in '+-' and x[:3] not in ('+++', '---'))
    for line in d:
        print('  ' + line)
    return changed


def save(doc, out: Path, table, name: str, backup: bool = True) -> None:
    after = serialize(doc, table)
    n = show_diff(doc.raw, after, name)
    print(f'\nrighe modificate: {n}')
    if out.exists() and backup:
        bak = out.with_suffix(out.suffix + '.bak')
        shutil.copy2(out, bak)
        print(f'backup: {bak}')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(after.encode('utf-8', 'surrogateescape'))
    print(f'scritto: {out}  ({len(after.encode("utf-8", "surrogateescape"))} byte)')


# ------------------------------------------------------------------ comandi

def cmd_info(a):
    doc = parse_file(a.file)
    song = doc.root
    print(f'file            : {a.file}')
    print(f'firmwareVersion : {song.get("firmwareVersion")}')
    print(f'earliestCompat  : {song.get("earliestCompatibleFirmware")}')
    print(f'timePerTimerTick: {song.get("timePerTimerTick")}'
          f' + {song.get("timerTickFraction")}/2^32')
    print(f'inputTickMagn.  : {song.get("inputTickMagnitude")}')
    print(f'BPM (derivato)  : {S.get_bpm(song):.3f}')
    print(f'rootNote        : {song.get("rootNote")}   '
          f'swing {song.get("swingAmount")}/{song.get("swingInterval")}')
    if doc.problems:
        print(f'\nanomalie del file: {len(doc.problems)}')
        for p in doc.problems[:5]:
            print(f'  r{p.line} {p.kind}: {p.detail[:80]}')

    cl = S.clips(doc)
    print(f'\nclip: {len(cl)}')
    print(f'{"#":>3} {"contenitore":<22} {"tipo":<16} {"nome":<32} '
          f'{"len":>6} {"righe":>6} {"note":>6}')
    for i, (cont, c) in enumerate(cl):
        s = S.clip_summary(c)
        print(f'{i:>3} {cont:<22} {s["tipo"]:<16} {s["nome"][:32]:<32} '
              f'{str(s["length"]):>6} {s["righe"]:>6} {s["note"]:>6}')


def cmd_notes(a):
    doc = parse_file(a.file)
    for i, (cont, c) in enumerate(S.clips(doc)):
        if a.clip is not None and i != a.clip:
            continue
        kind = 'kit' if S.is_kit_clip(c) else 'synth'
        print(f'\n=== clip {i} — {S.clip_label(c)} '
              f'({kind}, length={c.get("length")}) ===')

        # su un kit le righe hanno un nome: mostrarlo evita di ragionare per
        # indici, che e' il modo piu' facile di mettere la nota sul drum sbagliato
        names = []
        if kind == 'kit':
            try:
                names = S.drum_names(doc, c)
            except ValueError as exc:
                print(f'  (nomi dei drum non risolti: {exc})')

        for row in S.note_rows(c):
            ns = S.read_notes(row)
            if not ns and not a.all:
                continue
            if kind == 'kit':
                idx = row.get('drumIndex')
                nome = names[int(idx)] if names and idx is not None \
                    and int(idx) < len(names) else '?'
                label = f'drum {idx:>3} {nome:<8}'
            else:
                label = f'y {row.get("y"):>3}          '
            print(f'  {label}  {len(ns)} note')
            for n in ns[:a.limit]:
                print(f'      {n}')
            if len(ns) > a.limit:
                print(f'      … altre {len(ns) - a.limit}')


def cmd_params(a):
    from delugexml import params as P

    doc = parse_file(a.file)
    for i, (_, c) in enumerate(S.clips(doc)):
        if a.clip is not None and i != a.clip:
            continue
        kind = 'kit' if S.is_kit_clip(c) else 'synth'
        print(f'\n=== clip {i} — {S.clip_label(c)} ({kind}) ===')
        for blocco in c.children:
            if blocco.tag not in ('soundParams',):
                continue
            for nodo in [blocco] + [x for x in blocco.children
                                    if x.tag.startswith('envelope')]:
                righe = []
                for k, v in nodo.attrs:
                    if not (isinstance(v, str) and v.startswith('0x')):
                        continue
                    d = P.to_display(v)
                    if d is None and not a.all:
                        continue          # fuori scala: si tace, non si indovina
                    righe.append((k, v, d))
                if not righe:
                    continue
                if nodo is not blocco:
                    print(f'  [{nodo.tag}]')
                for k, v, d in righe:
                    mostrato = f'{d:>3}' if d is not None else 'fuori scala'
                    print(f'    {k:26} {mostrato:>11}   {v}')


def cmd_tempo(a):
    doc = parse_file(a.file)
    song = doc.root
    print(f'BPM prima : {S.get_bpm(song):.4f}')
    actual = S.set_bpm(song, a.bpm)
    print(f'BPM dopo  : {actual:.4f}  (richiesti {a.bpm})')
    err = abs(actual - a.bpm)
    if err > 0.001:
        print(f'  scarto di arrotondamento: {err:.5f} BPM')
    print()
    save(doc, Path(a.out), load_table(), Path(a.file).name)


def cmd_note_add(a):
    doc = parse_file(a.file)
    cl = S.clips(doc)
    if a.clip >= len(cl):
        sys.exit(f'clip {a.clip} inesistente (ce ne sono {len(cl)})')
    clip = cl[a.clip][1]
    rows = S.note_rows(clip)
    attr = S.row_index_attr(clip)

    # su un kit la riga si indirizza per nome: --drum SNARE invece di --row 1
    if a.drum is not None:
        if not S.is_kit_clip(clip):
            sys.exit(f'--drum vale solo sulle clip di kit; la clip {a.clip} '
                     f'e su un synth, usa --row con l altezza MIDI')
        try:
            index = S.drum_index(doc, clip, a.drum)
        except ValueError as exc:
            sys.exit(str(exc))
        dove = f'{a.drum.upper()} (drumIndex={index})'
    elif a.row is not None:
        index = a.row
        dove = f'{attr}={index}'
    else:
        sys.exit('serve --row oppure --drum NOME su una clip di kit')

    match = [r for r in rows if r.get(attr) == str(index)]
    if not match:
        presenti = ', '.join(str(r.get(attr)) for r in rows if r.has(attr))
        sys.exit(f'nessuna noteRow con {attr}={index} nella clip {a.clip}. '
                 f'Presenti: {presenti}')
    row = match[0]

    ns = S.read_notes(row)
    if any(n.pos == a.pos for n in ns):
        sys.exit(f'esiste gia una nota a pos={a.pos} su {dove}')
    clip_len = int(clip.get('length', '0') or 0)
    if clip_len and a.pos + a.len > clip_len:
        print(f'! attenzione: pos+len ({a.pos + a.len}) supera la '
              f'lunghezza della clip ({clip_len})')

    ns.append(Note(pos=a.pos, length=a.len, velocity=a.vel, lift=a.lift))
    print(f'note su {dove}: {len(ns) - 1} -> {len(ns)}')
    # create=True perche' su un kit la riga di destinazione e' spesso vuota,
    # e una riga vuota non porta nessun attributo di note
    S.write_notes(row, ns, create=True)
    print()
    save(doc, Path(a.out), load_table(), Path(a.file).name)


def cmd_clip_dup(a):
    doc = parse_file(a.file)
    before = len(S.clips(doc))
    src = S.clips(doc)[a.clip][1] if a.clip < before else None
    if src is None:
        sys.exit(f'clip {a.clip} inesistente (ce ne sono {before})')
    print(f'sorgente: clip {a.clip} — {S.clip_label(src)} '
          f'({len(S.note_rows(src))} righe, '
          f'{sum(len(S.read_notes(r)) for r in S.note_rows(src))} note)')

    dup = S.duplicate_clip(doc, a.clip, section=a.section, name=a.name,
                           colour_offset=a.colour)
    print(f'duplicata come clip {len(S.clips(doc)) - 1}, '
          f'sezione {dup.get("section")}')
    if a.clear_notes:
        for row in S.note_rows(dup):
            if S.read_notes(row):
                S.write_notes(row, [])
        print('  note della copia svuotate')
    print()
    save(doc, Path(a.out), load_table(), Path(a.file).name)


def cmd_row_add(a):
    doc = parse_file(a.file)
    cl = S.clips(doc)
    if a.clip >= len(cl):
        sys.exit(f'clip {a.clip} inesistente (ce ne sono {len(cl)})')
    clip = cl[a.clip][1]
    is_kit = S.is_kit_clip(clip)

    if a.drum is not None:
        if not is_kit:
            sys.exit(f'--drum vale solo sulle clip di kit; la clip {a.clip} '
                     f'e su un synth, usa --row con l altezza MIDI')
        try:
            index = S.drum_index(doc, clip, a.drum)
        except ValueError as exc:
            sys.exit(str(exc))
        etichetta = f'drumIndex={index} ({a.drum.upper()})'
    elif a.row is not None:
        index = a.row
        etichetta = f'{S.row_index_attr(clip)}={index}'
        if is_kit:
            try:
                nome = S.drum_names(doc, clip)[index]
                etichetta += f' ({nome})'
            except (ValueError, IndexError):
                pass
    else:
        sys.exit('serve --row (altezza MIDI o indice di drum) oppure '
                 '--drum NOME su una clip di kit')

    try:
        row = S.add_note_row(clip, index)
    except ValueError as exc:
        # su un kit le righe ci sono gia' tutte, una per drum: chi vuole
        # aggiungere un colpo cerca note-add, non row-add
        extra = ('\nSu un kit le righe esistono gia, una per drum. '
                 f'Per aggiungere un colpo:\n  python tools/dsong.py note-add '
                 f'{a.file} --clip {a.clip} --drum {a.drum or index} '
                 f'--pos {a.pos if a.pos is not None else 0} -o {a.out}'
                 ) if is_kit else ''
        sys.exit(f'{exc}{extra}')
    attr = S.row_index_attr(clip)
    presenti = [r.get(attr) for r in S.note_rows(clip) if r.has(attr)]
    print(f'aggiunta noteRow {etichetta}; '
          f'{attr} ora: {", ".join(presenti)}')
    if a.pos is not None:
        S.write_notes(row, [Note(pos=a.pos, length=a.len, velocity=a.vel)],
                      create=True)
        print(f'  con una nota a pos={a.pos} len={a.len} vel={a.vel}')
    print()
    save(doc, Path(a.out), load_table(), Path(a.file).name)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('info'); p.add_argument('file'); p.set_defaults(fn=cmd_info)

    p = sub.add_parser('notes')
    p.add_argument('file')
    p.add_argument('--clip', type=int)
    p.add_argument('--limit', type=int, default=8)
    p.add_argument('--all', action='store_true', help='mostra anche righe vuote')
    p.set_defaults(fn=cmd_notes)

    p = sub.add_parser('params',
                       help='parametri di suono nelle unita del display (0-50)')
    p.add_argument('file')
    p.add_argument('--clip', type=int)
    p.add_argument('--all', action='store_true',
                   help='mostra anche i valori fuori scala')
    p.set_defaults(fn=cmd_params)

    p = sub.add_parser('tempo')
    p.add_argument('file'); p.add_argument('--bpm', type=float, required=True)
    p.add_argument('-o', '--out', required=True)
    p.set_defaults(fn=cmd_tempo)

    p = sub.add_parser('note-add')
    p.add_argument('file')
    p.add_argument('--clip', type=int, required=True)
    p.add_argument('--row', type=int,
                   help='altezza MIDI su un synth, indice di drum su un kit')
    p.add_argument('--drum',
                   help='nome del drum (solo clip di kit): KICK, SNARE, …')
    p.add_argument('--pos', type=int, required=True, help='posizione in tick')
    p.add_argument('--len', type=int, required=True, help='durata in tick')
    p.add_argument('--vel', type=int, default=64)
    p.add_argument('--lift', type=int, default=64)
    p.add_argument('-o', '--out', required=True)
    p.set_defaults(fn=cmd_note_add)

    p = sub.add_parser('clip-dup', help='duplica una clip esistente')
    p.add_argument('file')
    p.add_argument('--clip', type=int, required=True)
    p.add_argument('--section', help='sezione della copia')
    p.add_argument('--name', help='clipName della copia')
    p.add_argument('--colour', help='colourOffset della copia')
    p.add_argument('--clear-notes', action='store_true',
                   help='svuota le note della copia, tenendo suono e righe')
    p.add_argument('-o', '--out', required=True)
    p.set_defaults(fn=cmd_clip_dup)

    p = sub.add_parser('row-add', help='aggiunge una noteRow a una clip')
    p.add_argument('file')
    p.add_argument('--clip', type=int, required=True)
    p.add_argument('--row', type=int,
                   help='altezza MIDI su un synth, indice di drum su un kit')
    p.add_argument('--drum',
                   help='nome del drum (solo clip di kit): KICK, SNARE, …')
    p.add_argument('--pos', type=int, help='se dato, aggiunge subito una nota')
    p.add_argument('--len', type=int, default=48)
    p.add_argument('--vel', type=int, default=64)
    p.add_argument('-o', '--out', required=True)
    p.set_defaults(fn=cmd_row_add)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == '__main__':
    sys.exit(main())
