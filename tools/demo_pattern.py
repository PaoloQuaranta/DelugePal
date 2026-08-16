"""Dimostrazione del giro completo: template-injection su una song reale.

Fa quello che dovra' fare il generatore, ma con parametri scritti a mano
invece che ricavati dal linguaggio naturale:

  1. parte da una song vera
  2. duplica una clip esistente — con tutti i suoi soundParams, arpeggiator e
     patch cable gia' coerenti — invece di costruirne una da zero
  3. svuota le note della copia
  4. ci scrive un pattern nuovo, espresso in battute e movimenti

Il punto e' che nessuno di questi passaggi inventa struttura: la clip nuova e'
una copia byte-identica di una che il Deluge ha scritto, e le uniche cose che
cambiano sono gli attributi che vogliamo cambiare.

Uso:
    python demo_pattern.py <song> --clip N -o <out> [--degrees 0,3,5,7]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from delugexml import parse_file, serialize, Note   # noqa: E402
from delugexml import song as S                     # noqa: E402
from delugexml.writer import FormatTable            # noqa: E402

TABLE = Path(__file__).resolve().parent.parent / 'out' / 'format_table.json'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('song')
    ap.add_argument('--clip', type=int, required=True,
                    help='clip da usare come modello')
    ap.add_argument('-o', '--out', required=True)
    ap.add_argument('--root', type=int, default=60,
                    help='nota di partenza (60 = C3 sul display del Deluge)')
    ap.add_argument('--degrees', default='0,4,7,12',
                    help='semitoni sopra la nota di partenza')
    ap.add_argument('--bars', type=int, default=2)
    ap.add_argument('--step', type=float, default=0.5,
                    help='passo in movimenti: 0.5 = ottavi, 0.25 = sedicesimi')
    ap.add_argument('--vel', type=int, default=100)
    ap.add_argument('--section', help='sezione della copia; '
                                      'di default la prima libera')
    a = ap.parse_args()

    doc = parse_file(a.song)
    song = doc.root
    tpb = S.ticks_per_beat(song)
    bar = S.ticks_per_bar(song)
    print(f'{Path(a.song).name}: {S.get_bpm(song):.1f} BPM, '
          f'{tpb} tick per movimento, {bar} per battuta (4/4)')

    src = S.clips(doc)[a.clip][1]
    print(f'modello: clip {a.clip} — {S.clip_label(src)}')

    # La copia suona lo stesso preset dell'originale, quindi le due sono
    # variazioni mutuamente esclusive: metterle in sezioni diverse e' l'unico
    # modo per poterle lanciare separatamente. Vedi docs/ARCHITETTURA.md.
    sec = a.section or S.first_free_section(doc)
    dup = S.duplicate_clip(doc, a.clip, name='GEN', section=sec)
    length = bar * a.bars
    dup.set('length', str(length))
    print(f'copia  : clip {len(S.clips(doc))-1}, sezione {sec} '
          f'(l originale sta nella {src.get("section")}), '
          f'lunghezza {length} tick = {a.bars} battute')

    for row in S.note_rows(dup):
        if S.read_notes(row):
            S.write_notes(row, [])

    degrees = [int(d) for d in a.degrees.split(',')]
    step_ticks = S.beats_to_ticks(song, a.step)
    n_steps = length // step_ticks
    print(f'pattern: {n_steps} passi da {step_ticks} tick, '
          f'gradi {degrees} sopra {a.root}')

    placed = 0
    for i in range(n_steps):
        y = a.root + degrees[i % len(degrees)]
        row = S.note_row(dup, y, create=True)
        ns = S.read_notes(row)
        ns.append(Note(pos=i * step_ticks, length=step_ticks,
                       velocity=a.vel))
        S.write_notes(row, ns, create=True)
        placed += 1

    rows = S.note_rows(dup)
    print(f'         {placed} note su {len(rows)} righe '
          f'(y: {", ".join(r.get("y") for r in rows)})')

    table = FormatTable.load(TABLE) if TABLE.exists() else FormatTable()
    out = serialize(doc, table)
    Path(a.out).write_bytes(out.encode('utf-8', 'surrogateescape'))
    print(f'\nscritto {a.out} ({len(out.encode("utf-8", "surrogateescape"))} byte)')
    print(f'l originale e conservato integralmente: '
          f'{"si" if doc.raw[:len(doc.raw)//2] in out else "NO"}')


if __name__ == '__main__':
    sys.exit(main())
