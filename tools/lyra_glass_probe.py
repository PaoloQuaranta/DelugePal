"""Controlled listening probe for the user-reported silent Glass voice.

No edits to the production song. Compare the original preset, filter bypass,
and only the DX7 payload replaced by the audible Tine patch.
"""
from pathlib import Path
from delugexml import parse_file, write_file, song as S, sound as V
from delugexml import musica as M, create as C, arranger as A, effects as FX
from delugexml import synthesis as SY
from delugexml.writer import FormatTable
from lyra_viareggio_six import presets

ROOT = Path(__file__).resolve().parents[1]


def build(source):
    saved = parse_file(source)
    glass = next(i for i in S.instruments(saved) if S.nome_strumento(i) == 'LYRA GLASS01')
    tine = next(i for i in S.instruments(saved) if S.nome_strumento(i) == 'LYRA TINE01')
    clip = next(c for _, c in S.clips(saved) if S.instrument_of(saved, c) is glass)
    doc = parse_file(ROOT / 'refs/songs/TEMPL0.XML')
    for inst in list(S.instruments(doc)):
        M.togli(doc, inst)
    S.set_bpm(doc.root, 100)
    S.set_scale(doc, 'C', 'maggiore')
    FX.set_delay(doc.root, feedback=0)
    FX.set_mod_fx(doc.root, kind='none')
    FX.set_eq(doc.root, bass=25, treble=25)
    FX.set_distortion(doc.root, saturation=0, bitcrush=0, decimation=0)
    FX.set_reverb_send(doc.root, 0)
    bar = S.ticks_per_bar(doc.root)
    for index, name in enumerate(('A GLASS', 'B FILTERS OPEN', 'C TINE ENGINE')):
        preset = presets()['LYRA GLASS01']
        assert preset.root.find('osc1').get('dx7patch') == glass.find('osc1').get('dx7patch')
        for param in V.names(clip):
            if V.get_raw(preset.root, param) is not None:
                V.set_raw(preset.root, param, V.get_raw(clip, param))
        if index == 1:
            V.set(preset.root, 'hpfFrequency', 0)
            V.set(preset.root, 'lpfFrequency', 50)
        elif index == 2:
            SY.set_dx7(preset.root, SY.DX7Patch.decode(tine.find('osc1').get('dx7patch')))
        inst, probe = C.add_track(doc, preset, name=name, folder='SYNTHS/DelugePal',
                                  length=4*bar, section=str(index), playing=index == 0)
        probe.set('clipName', name)
        M.scrivi(doc, probe, M.melodia('do4 mi4 sol4 do4', durata='1/2',
                                     articolazione='normale', velocity=100,
                                     tick_per_battuta=bar))
        A.place(doc, inst, probe, index*4*bar, 4*bar)
    A.fit_view(doc)
    assert not M.verifica(doc), M.verifica(doc)
    return doc


if __name__ == '__main__':
    source = ROOT / 'out/lyra04_user_mix_latest.XML'
    doc = build(source)
    target = ROOT / 'out/lyra_viareggio/GLASS CHECK01.XML'
    write_file(doc, target, FormatTable.load(ROOT / 'out/format_table.json'))
    assert not M.verifica(parse_file(target))
    print(M.racconta(doc))
    print('Warnings:', M.avvertenze(doc))
    print('Destination:', M.destinazione('GLASS CHECK', 1))
