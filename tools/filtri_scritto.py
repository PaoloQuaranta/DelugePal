"""FILTER01: routing, morph SVF nei due slot, drive LPF e FM HPF.

Nove strumenti in nove sezioni: lanciare una sezione alla volta.
Ogni clip dura quattro battute; nelle ultime sei il terzo parametro
passa a gradini 0, 25, 50, 0, una battuta ciascuno.
"""
from pathlib import Path

from delugexml import parse_file, write_file, create as C, song as S
from delugexml import musica as MU, structure as ST, sound as SND
from delugexml import automation as AU, params as P
from delugexml.writer import FormatTable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out' / 'FILTER01.XML'

# nome, LPF, HPF, routing, parametro variabile
CASES = (
    ('ROUTE H2L', '24dB', 'HPLadder', 'H2L', None),
    ('ROUTE L2H', '24dB', 'HPLadder', 'L2H', None),
    ('ROUTE PARA', '24dB', 'HPLadder', 'PARA', None),
    ('LP BAND', 'SVF_Band', 'Off', 'H2L', 'lpfMorph'),
    ('LP NOTCH', 'SVF_Notch', 'Off', 'H2L', 'lpfMorph'),
    ('HP BAND', 'Off', 'SVF_Band', 'H2L', 'hpfMorph'),
    ('HP NOTCH', 'Off', 'SVF_Notch', 'H2L', 'hpfMorph'),
    ('LP DRIVE', '24dB', 'Off', 'H2L', 'lpfMorph'),
    ('HP FM', 'Off', 'HPLadder', 'H2L', 'hpfMorph'),
)


def costruisci():
    doc = parse_file(ROOT / 'refs/songs/TEMPL0.XML')
    for inst in list(S.instruments(doc)):
        MU.togli(doc, inst)
    S.set_bpm(doc.root, 100)
    S.set_scale(doc, 'C', 'maggiore')
    bar = S.ticks_per_bar(doc.root)
    for index, (name, lpf, hpf, route, varying) in enumerate(CASES):
        inst, clip = C.add_track(
            doc, ROOT / 'refs/synths/TEMPL.XML', name=name, folder='SYNTHS',
            length=bar * 4, section=str(index), playing=index == 0)
        clip.set('clipName', name)
        ST.set_osc(inst, 1, type='saw')
        for cable in SND.patch_cables(clip):
            SND.remove_patch_cable(clip, cable['source'], cable['destination'])
        for param, value in {
            'volume': 24, 'oscAVolume': 40, 'oscBVolume': 0,
            'noiseVolume': 0, 'reverbAmount': 0, 'delayFeedback': 0,
            'lpfFrequency': 28, 'hpfFrequency': 22,
            'lpfResonance': 20, 'hpfResonance': 25,
            'envelope1.attack': 1, 'envelope1.release': 5,
        }.items():
            SND.set(clip, param, value)
        ST.set_filter(inst, lpf=lpf, hpf=hpf, route=route,
                      lpf_morph=0, hpf_morph=0, params_node=clip)
        # Stessa nota e stesso inviluppo per tutte le prove.
        MU.scrivi(doc, clip, MU.melodia(
            'do3 do3 do3 do3', durata='1/1', articolazione='legato',
            velocity=90, tick_per_battuta=bar))
        if varying:
            points = [AU.Punto(i * bar, int(P.from_display(v)[2:], 16))
                      for i, v in enumerate((0, 25, 50, 0))]
            SND.set_raw(clip, varying, AU.encode(points[0].raw, points))
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
    for case in CASES:
        print(case)
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('filter', 1))
