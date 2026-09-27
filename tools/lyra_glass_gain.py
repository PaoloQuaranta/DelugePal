"""Raise only Glass's clip volume after the controlled listening comparison."""
from pathlib import Path
from delugexml import parse_file, write_file, song as S, sound as V, musica as M
from delugexml.writer import FormatTable

ROOT = Path(__file__).resolve().parents[1]


def semantic(node):
    return node.tag, sorted(node.attrs), node.text, [semantic(c) for c in node.children]


def build(source):
    doc = parse_file(source)
    before = semantic(doc.root)
    inst = next(i for i in S.instruments(doc) if S.nome_strumento(i) == 'LYRA GLASS01')
    clips = [c for _, c in S.clips(doc) if S.instrument_of(doc, c) is inst]
    assert len(clips) == 1, 'Inspect updated song before changing multiple clips'
    clip = clips[0]
    old = V.get_raw(clip, 'volume')
    print('Glass volume:', V.get(clip, 'volume'), '-> 30/50')
    V.set(clip, 'volume', 30)
    changed = V.get_raw(clip, 'volume')
    V.set_raw(clip, 'volume', old)
    assert semantic(doc.root) == before
    V.set_raw(clip, 'volume', changed)
    assert not M.verifica(doc), M.verifica(doc)
    return doc


if __name__ == '__main__':
    doc = build(ROOT / 'out/lyra04_before_glass_gain.XML')
    path = ROOT / 'out/lyra_viareggio/LYRA VIAREGGIO05.XML'
    write_file(doc, path, FormatTable.load(ROOT / 'out/format_table.json'))
    reread = parse_file(path)
    assert semantic(reread.root) == semantic(doc.root)
    assert not M.verifica(reread)
    print('Warnings:', M.avvertenze(reread))
    print('Destination:', M.destinazione('LYRA VIAREGGIO', 5))
