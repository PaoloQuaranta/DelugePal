"""Prepare a Glass carrier-level correction without changing FM modulation.

Use a freshly downloaded source for deployment. A local source can be used
to validate the proposed change while the device is unavailable.
"""
import argparse
from dataclasses import replace
from pathlib import Path
from delugexml import parse_file, write_file, song as S, musica as M
from delugexml import synthesis as SY, sound as V
from delugexml.writer import FormatTable
from lyra_glass_gain import semantic

ROOT = Path(__file__).resolve().parents[1]


def build(source):
    doc = parse_file(source)
    before = semantic(doc.root)
    inst = next(i for i in S.instruments(doc) if S.nome_strumento(i) == 'LYRA GLASS01')
    clip = next(c for _, c in S.clips(doc) if S.instrument_of(doc, c) is inst)
    osc = inst.find('osc1')
    original = osc.get('dx7patch')
    patch = SY.DX7Patch.decode(original)
    assert patch.algorithm == 5
    assert [patch.operators[k].level for k in (0, 2, 4)] == [83, 76, 66]
    assert V.get(clip, 'volume') == 30, 'Inspect changed mix before proceeding'
    operators = tuple(replace(op, level=op.level + 16) if k in (0, 2, 4) else op
                      for k, op in enumerate(patch.operators))
    changed = replace(patch, operators=operators).encode()
    a, b = bytes.fromhex(original), bytes.fromhex(changed)
    assert [(k, b[k]-a[k]) for k in range(156) if a[k] != b[k]] == [(37, 16), (79, 16), (121, 16)]
    # Use the synthesis API, then verify it made no unrelated change.
    SY.set_dx7(inst, SY.DX7Patch.decode(changed), params_node=clip)
    osc.set('dx7patch', original)
    assert semantic(doc.root) == before
    osc.set('dx7patch', changed)
    assert not M.verifica(doc), M.verifica(doc)
    return doc


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    doc = build(args.source)
    write_file(doc, args.output, FormatTable.load(ROOT/'out/format_table.json'))
    assert semantic(parse_file(args.output).root) == semantic(doc.root)
    print('Only DX7 carrier levels changed: 83/76/66 -> 99/92/82; volume remains 30')
    print('Warnings:', M.avvertenze(doc))
    print('Destination:', M.destinazione('LYRA VIAREGGIO', 6))
