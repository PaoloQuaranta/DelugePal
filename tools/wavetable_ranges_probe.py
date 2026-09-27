"""A standalone multirange wavetable preset and a three-register test song."""
import argparse
from pathlib import Path
from delugexml import parse_file, write_file, song as S, create as C
from delugexml import musica as M, sound as V, synthesis as SY, arranger as A
from delugexml.notes import Note
from delugexml.writer import FormatTable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out/wavetable_range'
RANGES = [
    (59, 'SAMPLES/WAVETABLES/CommunityWavetables/Acid.wav'),
    (71, 'SAMPLES/WAVETABLES/CommunityWavetables/Allophones.wav'),
    (None, 'SAMPLES/WAVETABLES/CommunityWavetables/Bowed Metal [ML].wav'),
]


def build(version=1):
    preset = parse_file(ROOT / 'refs/synths/TEMPL.XML')
    SY.set_wavetable_ranges(preset.root, RANGES, experimental=True)
    for key, value in {'volume': 32, 'oscAVolume': 50, 'oscBVolume': 0,
                       'noiseVolume': 0, 'oscAWavetablePosition': 25,
                       'lpfFrequency': 50, 'hpfFrequency': 0,
                       'envelope1.attack': 0, 'envelope1.sustain': 50,
                       'envelope1.release': 14}.items():
        V.set(preset.root, key, value)
    song = parse_file(ROOT / 'refs/songs/TEMPL0.XML')
    for inst in list(S.instruments(song)):
        M.togli(song, inst)
    S.set_bpm(song.root, 100)
    S.set_scale(song, 'C', 'maggiore')
    bar = S.ticks_per_bar(song.root)
    inst, clip = C.add_track(song, preset, name=f'WT RANGE{version:02}',
                             folder='SYNTHS/DelugePal', length=4*bar,
                             section='0', playing=True)
    clip.set('clipName', f'WT RANGE{version:02}')
    M.scrivi(song, clip, {48: [Note(0, bar*3//4, 100)],
                         60: [Note(bar, bar*3//4, 100)],
                         72: [Note(2*bar, bar*3//4, 100)]})
    A.place(song, inst, clip, 0, 4*bar)
    A.fit_view(song)
    return preset, song


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', type=int, default=1)
    version = parser.parse_args().version
    preset, song = build(version)
    assert SY.wavetable_ranges(preset.root) == RANGES
    assert not M.verifica(preset), M.verifica(preset)
    assert not M.verifica(song), M.verifica(song)
    OUT.mkdir(parents=True, exist_ok=True)
    fmt = FormatTable.load(ROOT / 'out/format_table.json')
    for name, doc in [(f'WT RANGE{version:02}.XML', preset),
                      (f'WT RANGE TEST{version:02}.XML', song)]:
        path = OUT / name
        write_file(doc, path, fmt)
        assert not M.verifica(parse_file(path))
        print('Local:', path, path.stat().st_size, 'bytes')
    print(M.racconta(song))
    print('Warnings:', M.avvertenze(song))
    print('Preset:', M.destinazione('WT RANGE', version, 'SYNTHS'))
    print('Song:', M.destinazione('WT RANGE TEST', version))
