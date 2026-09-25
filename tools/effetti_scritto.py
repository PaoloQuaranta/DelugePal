"""FXSTD01: confronto isolato di effetti standard, una sezione alla volta.

Quindici sezioni con lo stesso synth e le stesse note. La prima e' asciutta.
Nessun caricamento implicito sul dispositivo: scrive solo in out/.
"""
from pathlib import Path

from delugexml import parse_file, write_file, create as C, song as S
from delugexml import musica as MU, structure as ST, sound as SND, effects as FX
from delugexml.writer import FormatTable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out/FXSTD01.XML'
CASES = (
    ('DRY', None, {}),
    ('DELAY DIGITAL', 'delay', {'analog': False, 'sync_type': 'even'}),
    ('DELAY ANALOG', 'delay', {'analog': True, 'sync_type': 'even'}),
    ('DELAY TRIPLET', 'delay', {'analog': False, 'sync_type': 'triplet'}),
    ('DELAY DOTTED', 'delay', {'analog': False, 'sync_type': 'dotted'}),
    ('FLANGER', 'mod', {'kind': 'flanger'}),
    ('PHASER', 'mod', {'kind': 'phaser'}),
    ('CHORUS', 'mod', {'kind': 'chorus'}),
    ('STEREO CHORUS', 'mod', {'kind': 'StereoChorus'}),
    ('EQ BASS', 'eq', {'bass': 40}),
    ('EQ TREBLE', 'eq', {'treble': 40}),
    ('SATURATION', 'distortion', {'saturation': 8}),
    ('DECIMATION', 'distortion', {'decimation': 32}),
    ('BITCRUSH', 'distortion', {'bitcrush': 32}),
    ('REVERB', 'reverb', {}),
)


def costruisci():
    doc = parse_file(ROOT / 'refs/songs/TEMPL0.XML')
    for inst in list(S.instruments(doc)):
        MU.togli(doc, inst)
    S.set_bpm(doc.root, 100)
    S.set_scale(doc, 'C', 'maggiore')
    FX.set_delay(doc.root, feedback=0)
    FX.set_mod_fx(doc.root, kind='none')
    FX.set_eq(doc.root, bass=25, treble=25)
    FX.set_distortion(doc.root, saturation=0, bitcrush=0, decimation=0)
    FX.set_reverb_send(doc.root, 0)
    FX.set_reverb(doc.root, model='mutable', room_size=30, damping=35,
                  width=50, hpf=0, lpf=50)
    bar = S.ticks_per_bar(doc.root)
    for index, (name, family, options) in enumerate(CASES):
        inst, clip = C.add_track(doc, ROOT / 'refs/synths/TEMPL.XML', name=name,
                                 folder='SYNTHS', length=bar * 4,
                                 section=str(index), playing=index == 0)
        clip.set('clipName', name)
        ST.set_osc(inst, 1, type='saw')
        for cable in SND.patch_cables(clip):
            SND.remove_patch_cable(clip, cable['source'], cable['destination'])
        for param, value in {
            'volume': 20, 'oscAVolume': 40, 'oscBVolume': 0, 'noiseVolume': 0,
            'lpfFrequency': 50, 'hpfFrequency': 0,
            'lpfResonance': 0, 'hpfResonance': 0,
            'envelope1.attack': 0, 'envelope1.release': 5,
        }.items():
            SND.set(clip, param, value)
        FX.set_delay(inst, analog=False, ping_pong=True, sync_level=7,
                      sync_type='even', feedback=0, params_node=clip)
        FX.set_mod_fx(inst, kind='none', rate=22, depth=32, feedback=25,
                       offset=25, params_node=clip)
        FX.set_distortion(inst, saturation=0, bitcrush=0, decimation=0,
                           params_node=clip)
        FX.set_eq(clip, bass=25, treble=25, bass_frequency=25, treble_frequency=25)
        FX.set_reverb_send(clip, 0)
        if family == 'delay':
            FX.set_delay(inst, feedback=22, params_node=clip, **options)
        elif family == 'mod':
            FX.set_mod_fx(inst, params_node=clip, **options)
        elif family == 'eq':
            FX.set_eq(clip, **options)
        elif family == 'distortion':
            FX.set_distortion(inst, params_node=clip, **options)
        elif family == 'reverb':
            FX.set_reverb_send(clip, 25)
        # Due battute di note corte, poi due di silenzio per ascoltare le code.
        MU.scrivi(doc, clip, MU.melodia('do3 sol3 do4 sol3', durata='1/2',
                                       articolazione='staccato', velocity=90,
                                       tick_per_battuta=bar))
    return doc


def scrivi(path=OUT):
    doc = costruisci()
    errors = MU.verifica(doc)
    if errors:
        raise ValueError(errors)
    write_file(doc, path, FormatTable.load(ROOT / 'out/format_table.json'))
    return path


if __name__ == '__main__':
    doc = costruisci()
    print(MU.racconta(doc))
    print('verifica:', MU.verifica(doc))
    print('avvertenze:', MU.avvertenze(doc))
    for index, case in enumerate(CASES):
        print(index, case)
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('fxstd', 1))
