"""Original dark-dub accompaniment for the freshly downloaded LYRA VIAREGGIO.

All XML authoring goes through delugexml. Original arrangement, audio and
melodic material are retained. No randomization: each drum role has a
repeatable, small phrasing contour; original fills retain their events.
"""
import json
from dataclasses import replace
from pathlib import Path
from collections import defaultdict
from delugexml import parse_file, write_file
from delugexml import song as S, musica as M, create as C, arranger as A
from delugexml import sound as V, structure as ST, effects as FX
from delugexml import synthesis as SY, automation as AU, params as P
from delugexml.notes import Note
from delugexml.writer import FormatTable

ROOT = Path(__file__).resolve().parents[1]
TABLE = 'SAMPLES/WAVETABLES/CommunityWavetables/Acid.wav'


def presets():
    ep = parse_file(ROOT / 'refs/synths/TEMPL.XML')
    op = SY.DX7Operator
    # Algorithm 5: three independent modulator/carrier pairs, 2->1, 4->3, 6->5.
    patch = SY.DX7Patch((
        op(rates=(99, 67, 37, 65), levels=(99, 83, 0, 0), level=88, velocity=2, right_depth=12, rate_scaling=2),
        op(rates=(99, 74, 48, 69), levels=(99, 58, 0, 0), level=62, velocity=5, coarse=1, right_depth=24, rate_scaling=3),
        op(rates=(98, 61, 34, 62), levels=(99, 78, 0, 0), level=82, velocity=2, detune=8, rate_scaling=2),
        op(rates=(99, 71, 45, 67), levels=(99, 48, 0, 0), level=49, velocity=4, coarse=2, detune=6, right_depth=30),
        op(rates=(99, 80, 52, 72), levels=(99, 50, 0, 0), level=66, velocity=3, rate_scaling=3),
        op(rates=(99, 86, 60, 76), levels=(99, 30, 0, 0), level=67, velocity=6, coarse=14, fine=2, right_depth=38, rate_scaling=3),
    ), algorithm=5, feedback=2, name='LYRA TINE')
    SY.set_dx7(ep.root, patch)
    for k, v in {'volume':29, 'pan':22, 'lpfFrequency':42, 'lpfResonance':3,
                 'hpfFrequency':10, 'noiseVolume':0}.items():
        V.set(ep.root,k,v)
    FX.set_mod_fx(ep.root,kind='chorus',rate=8,depth=10)
    FX.set_delay(ep.root,analog=True,ping_pong=True,sync_level=7,sync_type='dotted',feedback=13)
    FX.set_reverb_send(ep.root,12)
    FX.set_eq(ep.root,bass=21,treble=23)

    wt = parse_file(ROOT / 'refs/synths/TEMPL.XML')
    SY.set_wavetable(wt.root,TABLE)
    for k,v in {'volume':24,'pan':29,'oscAVolume':42,'oscBVolume':0,
                'oscAWavetablePosition':17,'lpfFrequency':24,'lpfResonance':13,
                'hpfFrequency':16,'hpfResonance':2,'noiseVolume':0,
                'envelope1.attack':8,'envelope1.decay':25,'envelope1.sustain':27,
                'envelope1.release':22,'envelope2.attack':5,'envelope2.decay':31,
                'envelope2.sustain':9,'envelope2.release':24,'lfo1Rate':5,'lfo2Rate':9}.items():
        V.set(wt.root,k,v)
    ST.set_lfo(wt.root,1,type='triangle',sync=0)
    ST.set_lfo(wt.root,2,type='sine',sync=0)
    V.set_patch_cable(wt.root,'lfo1','oscAWavetablePosition',9)
    V.set_patch_cable(wt.root,'envelope2','oscAWavetablePosition',7)
    V.set_patch_cable(wt.root,'envelope2','lpfFrequency',12)
    V.set_patch_cable(wt.root,'lfo2','lpfFrequency',3)
    FX.set_delay(wt.root,analog=True,ping_pong=True,sync_level=7,sync_type='dotted',feedback=20)
    FX.set_reverb_send(wt.root,17)
    FX.set_eq(wt.root,bass=18,treble=21)
    return ep,wt


def humanize(doc):
    report=[]
    beat=S.ticks_per_beat(doc.root)
    for ci,(_,clip) in enumerate(S.clips(doc)):
        if not S.is_kit_clip(clip):
            continue
        drums=S.drums(S.instrument_of(doc,clip))
        shifts=[]; velocities=[]
        for row in S.note_rows(clip):
            old=S.read_notes(row)
            if not old:
                continue
            name=S.nome_drum(drums[int(row.get('drumIndex'))])
            limit=int(row.get('length') or clip.get('length'))
            ns=[]
            for i,n in enumerate(old):
                phase=(n.pos//(beat//4))%8
                close=i>0 and n.pos-old[i-1].pos<=beat//4
                if name.startswith('BD'):
                    dt=0 if n.pos%beat==0 else (0,1,0,-1)[i%4]
                    dv=(0,-3,2,-2)[i%4] - (5 if close else 0)
                elif name.startswith('SD') or name.startswith('Clap'):
                    dt=(2,1,2,3)[i%4]
                    dv=(2,-4,0,-2)[i%4] - (10 if close else 0)
                elif name.startswith('OH'):
                    dt=(0,-1,1,0,-1,1,0,1)[phase]
                    dv=(0,-9,3,-6,-2,-10,4,-5)[phase] - (4 if close else 0)
                else:
                    dt=0; dv=-3
                # Never reorder adjacent rolls or move an attack outside its loop.
                lo=old[i-1].pos+1 if i else 0
                hi=min(limit-1,old[i+1].pos-1 if i+1<len(old) else limit-1)
                pos=max(lo,min(hi,n.pos+dt))
                vel=max(1,min(127,n.velocity+dv))
                ns.append(replace(n,pos=pos,velocity=vel))
                shifts.append(pos-n.pos);velocities.append(vel-n.velocity)
            S.write_notes(row,ns)
        report.append({'clip_index':ci,'notes':len(shifts),'timing_ticks':[min(shifts),max(shifts)],
                       'velocity_delta':[min(velocities),max(velocities)]})
    return report


# Voicings chosen around the actual E/F/Ab/B material; low root belongs to bass.
VOICES={
 'f':(56,60,64),        # Ab3 C4 E4: Fm(maj7)
 'f9':(56,60,64,67),   # Fm(maj9)
 'db':(56,60,65),      # Ab3 C4 F4: Dbmaj7 without root
 'e':(56,62,65),       # G#3 D4 F4: E7b9 shell
 'b':(56,62,65),       # Ab3 D4 F4: Bdim7 without root
 'shell':(56,64),      # m3/maj7 above F
}


def add_chord(notes,bar,beat,chord,duration,velocity,origin):
    tick=(bar-origin)*384+round(beat*96)
    for i,pitch in enumerate(VOICES[chord]):
        notes[pitch].append(Note(tick+(0,1,2,1)[i],duration,
                                 max(1,velocity+(0,-5,3,-3)[i])))


def piano_part():
    ns=defaultdict(list)
    # Eight separately shaped phrases, in absolute song bars (one-based).
    phrases={
      9:[(0,.5,'shell',55,66),(1,2.5,'e',34,73),(3,1.5,'db',65,64),
         (4,.5,'f',38,77),(5,3.5,'e',24,62),(7,.5,'db',88,69)],
      17:[(0,1.5,'shell',38,62),(3,2.5,'e',28,67),(6,.5,'f',48,64)],
      25:[(0,.5,'f9',66,75),(1,2.5,'e',34,67),(3,.5,'db',72,72),
          (4,1.5,'f',45,78),(5,2.5,'shell',33,61),(7,1.5,'e',37,73)],
      33:[(0,.5,'f9',82,78),(1,2.5,'b',39,68),(2,1.5,'f',46,73),
          (3,2.5,'b',36,72),(4,.5,'db',67,74),(5,2.5,'b',39,66),
          (6,1.5,'f9',55,81),(7,2.5,'b',28,62)],
      41:[(0,1.5,'shell',34,60),(3,.5,'shell',57,64),(6,2.5,'e',28,65)],
      49:[(0,.5,'f',46,76),(1,2.5,'b',34,72),(2,1.5,'db',67,74),
          (3,2.5,'b',34,70),(4,.5,'f9',82,79),(5,2.5,'b',28,67),
          (7,2.5,'b',26,61)],
      57:[(0,1.5,'shell',56,68),(2,.5,'f',62,71),(4,2.5,'e',33,64),
          (6,.5,'db',84,61)],
      65:[(0,1.5,'shell',92,58),(2,.5,'f',110,52)],
    }
    for start,events in phrases.items():
        for offset,beat,chord,duration,velocity in events:
            add_chord(ns,start+offset,beat,chord,duration,velocity,9)
    return ns


def wave_part():
    ns=defaultdict(list)
    # Short replies and a few sustained dyads; no continuous pad over the original.
    events=[(13,2,72,90,61),(14,3,71,36,54),(15,2.5,68,115,60),
            (23,3,76,60,58),(24,1.5,72,100,64),
            (27,2,68,90,64),(28,3,71,42,54),(31,2,72,130,65),
            (35,3,76,72,62),(36,1.5,72,96,67),(39,1.5,68,120,66),
            (43,2,71,80,56),(44,3,68,47,53),(47,2,72,135,60),
            (51,3,76,60,66),(52,1.5,72,95,62),(55,1.5,68,108,65),
            (59,2,72,140,59),(63,2.5,68,150,55),(67,1,72,170,48)]
    for bar,beat,pitch,length,vel in events:
        ns[pitch].append(Note((bar-13)*384+round(beat*96),length,vel))
    for bar in (31,47,63):
        ns[64].append(Note((bar-13)*384+192,110,47))
    return ns


def automate(clip,name,points):
    ps=[AU.Punto(pos,int(P.from_display(value),16),True) for pos,value in points]
    V.set_raw(clip,name,AU.encode(ps[0].raw,ps))


def build(source=ROOT/'out/lyra_viareggio_source.XML'):
    doc=parse_file(source)
    if S.ticks_per_bar(doc.root)!=384:
        raise ValueError('This composition is authored on the freshly observed 384-tick grid')
    original_instances=[(i,A.instances(i)) for i in S.instruments(doc)]
    drum_report=humanize(doc)
    ep,wt=presets()
    for preset,name,origin,bars,notes in (
        (ep,'LYRA TINE01',9,60,piano_part()),
        (wt,'LYRA ACID01',13,56,wave_part())):
        inst,clip=C.add_track(doc,preset,name=name,folder='SYNTHS/DelugePal',
                             length=bars*384,playing=True)
        S.set_key_mode(clip,False)
        M.scrivi(doc,clip,notes)
        A.place(doc,inst,clip,(origin-1)*384,bars*384)
        if preset is wt:
            automate(clip,'oscAWavetablePosition',[(0,14),(8*384,24),(16*384,18),
                     (24*384,31),(32*384,20),(40*384,28),(48*384,16),(56*384-1,11)])
            automate(clip,'lpfFrequency',[(0,22),(8*384,26),(16*384,23),
                     (24*384,31),(32*384,24),(40*384,29),(48*384,21),(56*384-1,17)])
            automate(clip,'hpfFrequency',[(0,16),(24*384,19),(40*384,17),(56*384-1,21)])
    for inst,instances in original_instances:
        assert A.instances(inst)==instances, 'Original arrangement changed'
    for _,clip in S.clips(doc):
        S.fit_clip_scroll_to_notes(doc,clip)
    A.fit_view(doc)
    errors=M.verifica(doc)
    if errors:
        raise ValueError(errors)
    return doc,ep,wt,drum_report


if __name__=='__main__':
    doc,ep,wt,drums=build()
    fmt=FormatTable.load(ROOT/'out/format_table.json')
    output=ROOT/'out/lyra_viareggio';output.mkdir(exist_ok=True)
    for d,name in ((doc,'LYRA VIAREGGIO01'),(ep,'LYRA TINE01'),(wt,'LYRA ACID01')):
        errors=M.verifica(d)
        if errors: raise ValueError(errors)
        p=output/(name+'.XML');write_file(d,p,fmt)
        assert not M.verifica(parse_file(p))
    (output/'racconto.txt').write_text(M.racconta(doc),encoding='utf8')
    (output/'drums.json').write_text(json.dumps(drums,indent=2),encoding='utf8')
    print('drum clips',len(drums),'notes',sum(d['notes'] for d in drums))
    print('validation',M.verifica(doc),'warnings',M.avvertenze(doc))
    print('destinations',M.destinazione('LYRA VIAREGGIO',1),
          M.destinazione('LYRA TINE',1,'SYNTHS'),M.destinazione('LYRA ACID',1,'SYNTHS'))
