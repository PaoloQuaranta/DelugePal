"""TRAMA04-06: revisione della song risalvata, armonia e livelli FILO.

Il tema insiste su Sol/Sib e usa Mi naturale: la nuova lettura e' Sol dorico.
La mappa serve a CAMPO e GROUND insieme. OMBRA e il mix vengono dal salvataggio.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

from delugexml import parse_file, write_file, song as S, sound as V, musica as M
from delugexml import synthesis as SY
from delugexml.notes import Note
from delugexml.writer import FormatTable

ROOT = Path(__file__).resolve().parents[1]
B = M.TICK_PER_BATTUTA
VERSION = 4
OUT = ROOT / 'out' / 'TRAMA04.XML'

# Fondamentale e due voci del campo. Le note della melodia possono aggiungere
# seste/noni o sospensioni; il basso dichiara sempre la fondamentale sul battere.
FIELDS = {
    'Gm': ('sol1', ('sib3', 're4')),
    'Bb': ('sib1', ('sib3', 'fa4')),
    'C': ('do2', ('sol3', 'mi4')),
    'C7': ('do2', ('sib3', 'mi4')),
    'F': ('fa1', ('la3', 'do4')),
}
HARMONY = (
    'Gm', 'Gm', 'Bb', 'Bb', 'Gm', 'Gm',                 # intro
    'Gm', 'C', 'F', 'Gm', 'Gm', 'C', 'C7', 'Gm',       # tema / risposta
    'Gm', 'F', 'C', 'Gm', 'Gm', 'C', 'Bb', 'C',        # variazione
    'Gm', 'F', 'Bb', 'Bb', 'Gm', 'Gm', 'C', 'C', 'F', 'C',
    'Bb', 'Gm', 'C', 'F', 'Gm', 'C', 'C7', 'Gm', 'F', 'C', 'Gm', 'Gm',
    'Gm', 'C', 'F', 'Gm', 'Gm', 'F', 'Gm', 'Gm',       # ritorno / inizio coda
    'Gm', 'C', 'F', 'C', 'Gm', 'Gm',                  # coda
)
PAD_GAPS = frozenset((31, 36, 37, 38, 39, 43))


def tracks(doc):
    instruments = {S.nome_strumento(i): i for i in S.instruments(doc)}
    clips = {}
    for name, inst in instruments.items():
        owned = [c for _, c in S.clips(doc) if S.instrument_of(doc, c) is inst]
        if len(owned) != 1:
            raise ValueError(f'{name}: attesa una clip, trovate {len(owned)}')
        clips[name] = owned[0]
    if set(instruments) != {'FILO', 'OMBRA', 'CAMPO', 'GROUND', 'TRAMA BEAT'}:
        raise ValueError('la fonte deve essere il salvataggio della song TRAMA')
    if any(int(c.get('length')) != 58 * B for c in clips.values()):
        raise ValueError('forma sorgente cambiata: analizzare prima di riscrivere')
    return instruments, clips


def rows(clip):
    return {int(r.get('y')): S.read_notes(r) for r in S.note_rows(clip)}


def _replace_notes(doc, clip, material):
    for row in list(S.note_rows(clip)):
        M.togli(doc, row)
    M.scrivi(doc, clip, material)


def bass():
    result = {}
    for bar, name in enumerate(HARMONY):
        pitch = M.altezza(FIELDS[name][0])
        if bar < 6:
            attacks = ((0, B - 24, 66),)
        elif bar < 52:
            attacks = ((0, 180, 76), (216, 144, 68))
        elif bar < 56:
            attacks = ((0, B - 24, 63),)
        elif bar == 56:
            attacks = ((0, 2 * B, 59),)
        else:
            attacks = ()
        for offset, length, velocity in attacks:
            result.setdefault(pitch, []).append(
                Note(pos=bar * B + offset, length=length, velocity=velocity))
    return result


def pad():
    result = {}
    bar = 0
    while bar < len(HARMONY):
        if bar in PAD_GAPS:
            bar += 1
            continue
        end = bar + 1
        while (end < len(HARMONY) and end not in PAD_GAPS
               and HARMONY[end] == HARMONY[bar]):
            end += 1
        for name in FIELDS[HARMONY[bar]][1]:
            result.setdefault(M.altezza(name), []).append(
                Note(pos=bar * B, length=(end - bar) * B - 24, velocity=36))
        bar = end
    return result


def counter(clip):
    """Due Mib diventano Mi; due Do# diventano Do. Il gesto resta identico."""
    result = {}
    changes = {(19, M.altezza('mib3')): M.altezza('mi3'),
               (21, M.altezza('do#3')): M.altezza('do3'),
               (28, M.altezza('mib3')): M.altezza('mi3'),
               (29, M.altezza('do#3')): M.altezza('do3')}
    for pitch, notes in rows(clip).items():
        for note in notes:
            target = changes.get((note.pos // B, pitch), pitch)
            # Ultimo Do della coda: una quarta sospesa che risolve sulla terza Sib.
            if pitch == M.altezza('do4') and note.pos == 57 * B + 192:
                result.setdefault(target, []).append(replace(note, length=96))
                result.setdefault(M.altezza('sib3'), []).append(
                    replace(note, pos=57 * B + 288, length=96))
            else:
                result.setdefault(target, []).append(deepcopy(note))
    for notes in result.values():
        notes.sort(key=lambda n: n.pos)
    return result


def build(source):
    doc = deepcopy(source)
    instruments, clips = tracks(doc)
    if M.verifica(doc):
        raise ValueError(f'sorgente non valida: {M.verifica(doc)}')
    patch = SY.DX7Patch.decode(instruments['FILO'].find('osc1').get('dx7patch'))
    if patch.algorithm != 5 or patch.name != 'TRAMA FILO':
        raise ValueError('patch FILO cambiata: analizzarla prima di correggere')
    # La documentazione community e set_dx7() richiedono ENV1 esterno aperto.
    # Qui si corregge soltanto quello; payload/carrier/volume del mix sono conservati.
    for name, value in (('envelope1.attack', 0), ('envelope1.sustain', 50),
                        ('envelope1.release', 50)):
        V.set(clips['FILO'], name, value)
    S.set_scale(doc, 'G', 'dorico')
    _replace_notes(doc, clips['GROUND'], bass())
    _replace_notes(doc, clips['CAMPO'], pad())
    _replace_notes(doc, clips['OMBRA'], counter(clips['OMBRA']))
    for clip in clips.values():
        if not S.is_kit_clip(clip):
            S.set_key_mode(clip, False)
    errors = M.verifica(doc)
    if errors:
        raise ValueError(f'revisione non valida: {errors}')
    return doc


def raise_filo_carriers(source, *, final=False):
    """05: +17 alle portanti; 06: portanti 99 e sensibilita velocity 2."""
    errors = M.verifica(source)
    if errors:
        raise ValueError(f'sorgente non valida: {errors}')
    doc = deepcopy(source)
    instruments, _ = tracks(doc)
    filo = instruments['FILO']
    patch = SY.DX7Patch.decode(filo.find('osc1').get('dx7patch'))
    if patch.algorithm != 5 or patch.name != 'TRAMA FILO':
        raise ValueError('patch FILO cambiata: analizzarla prima di correggere')
    # Algoritmo 5: portanti 1/3/5, modulatori 2/4/6.
    if final:
        if [(op.level, op.velocity) for op in patch.operators[::2]] != [(99,5),(91,4),(83,3)]:
            raise ValueError('portanti sorgente cambiate: attesa la TRAMA05')
        operators = tuple(replace(op, level=99, velocity=2) if index % 2 == 0 else op
                          for index, op in enumerate(patch.operators))
    else:
        # Stesso incremento per conservare il bilanciamento fra le tre coppie.
        if any(op.level > 82 for op in patch.operators[::2]):
            raise ValueError('portanti gia alzate: non applicare due volte il boost')
        operators = tuple(replace(op, level=op.level + 17) if index % 2 == 0 else op
                          for index, op in enumerate(patch.operators))
    SY.update_dx7_patch(filo, replace(patch, operators=operators))
    errors = M.verifica(doc)
    if errors:
        raise ValueError(f'revisione non valida: {errors}')
    return doc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='song TRAMA appena riscaricata')
    level_mode = parser.add_mutually_exclusive_group()
    level_mode.add_argument('--filo-levels', action='store_true',
                           help='solo portanti dalla TRAMA04 riscaricata, produce TRAMA05')
    level_mode.add_argument('--filo-final', action='store_true',
                           help='livelli approvati dalla TRAMA05 riscaricata, produce TRAMA06')
    args = parser.parse_args()
    version = 6 if args.filo_final else 5 if args.filo_levels else VERSION
    target = ROOT / 'out' / f'TRAMA{version:02d}.XML'
    if args.source.resolve() == target.resolve():
        raise ValueError('la sorgente non puo essere la destinazione')
    source = parse_file(args.source)
    levels_only = args.filo_levels or args.filo_final
    doc = raise_filo_carriers(source, final=args.filo_final) if levels_only else build(source)
    if levels_only:
        for label, song in (('prima', source), ('dopo', doc)):
            patch = SY.DX7Patch.decode(tracks(song)[0]['FILO'].find('osc1').get('dx7patch'))
            print(label, 'livelli operatori 1-6:', [op.level for op in patch.operators])
            print(label, 'sensibilita velocity 1-6:', [op.velocity for op in patch.operators])
    write_file(doc, target, FormatTable.load(ROOT / 'out' / 'format_table.json'))
    reread = parse_file(target)
    if M.verifica(reread):
        raise ValueError(M.verifica(reread))
    print(M.racconta(reread))
    print('verifica:', M.verifica(reread))
    print('avvertenze:', M.avvertenze(reread))
    print('scritto:', target)
    print('destinazione:', M.destinazione('trama', version))
