"""Revision 04: redistribute the two added parts across six original timbres.

The musical event multiset is preserved exactly. Chords (including strums)
and connected Acid gestures are kept together. Run against a fresh SD song.
"""
import argparse
import json
from collections import defaultdict, Counter
from dataclasses import astuple
from pathlib import Path
from delugexml import parse_file, write_file
from delugexml import musica as M, song as S, arranger as A, create as C
from delugexml import sound as V, structure as ST, synthesis as SY, effects as FX
from delugexml.writer import FormatTable
from lyra_viareggio import automate

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'out/lyra_viareggio'
TABLES={
    'LYRA VOX01':'SAMPLES/WAVETABLES/CommunityWavetables/Allophones.wav',
    'LYRA METAL01':'SAMPLES/WAVETABLES/CommunityWavetables/Bowed Metal [ML].wav',
}


def values(owner, params):
    for key,value in params.items():
        V.set(owner,key,value)


def presets():
    result={}
    op=SY.DX7Operator
    reed=parse_file(ROOT/'refs/synths/TEMPL.XML')
    # Algorithm 32 sums all six carriers. Sustained harmonic registers give
    # a reed-organ colour, with no tine transient or modulator decay.
    operators=tuple(op(rates=(86,99,99,67),levels=(99,99,99,0),
                       coarse=ratio,level=level,velocity=1,detune=detune,
                       right_depth=20,rate_scaling=2)
                    for ratio,level,detune in
                    [(1,87,7),(2,79,8),(3,70,6),(4,62,7),(6,54,8),(8,46,6)])
    SY.set_dx7(reed.root,SY.DX7Patch(operators,algorithm=32,feedback=0,name='LYRA REED'))
    values(reed.root,{'volume':25,'pan':18,'lpfFrequency':35,'lpfResonance':7,
                      'hpfFrequency':12})
    FX.set_mod_fx(reed.root,kind='chorus',rate=5,depth=15)
    FX.set_delay(reed.root,analog=True,ping_pong=True,sync_level=7,
                 sync_type='dotted',feedback=15)
    FX.set_reverb_send(reed.root,14)
    FX.set_eq(reed.root,bass=21,treble=22)
    result['LYRA REED01']=reed

    glass=parse_file(ROOT/'refs/synths/TEMPL.XML')
    # Three two-operator pairs, with inharmonic modulators and a dry bright
    # strike. Slower carrier release leaves a bell tail after a short chord.
    operators=[]
    for ratio,fine,level,carrier_level in [(7,41,73,83),(3,27,67,76),(11,6,61,66)]:
        operators.extend([
            op(rates=(99,57,32,42),levels=(99,68,0,0),level=carrier_level,
               velocity=3,right_depth=22,rate_scaling=3),
            op(rates=(99,75,46,55),levels=(99,48,0,0),level=level,
               coarse=ratio,fine=fine,velocity=5,right_depth=35,rate_scaling=3)])
    SY.set_dx7(glass.root,SY.DX7Patch(tuple(operators),algorithm=5,feedback=0,name='LYRA GLASS'))
    values(glass.root,{'volume':23,'pan':32,'lpfFrequency':45,'lpfResonance':2,
                       'hpfFrequency':19})
    FX.set_mod_fx(glass.root,kind='none')
    FX.set_delay(glass.root,analog=False,ping_pong=True,sync_level=7,
                 sync_type='even',feedback=12)
    FX.set_reverb_send(glass.root,21)
    FX.set_eq(glass.root,bass=18,treble=25)
    result['LYRA GLASS01']=glass

    vox=parse_file(ROOT/'refs/synths/TEMPL.XML')
    SY.set_wavetable(vox.root,TABLES['LYRA VOX01'])
    ST.set_attr(vox.root,'lpfMode','SVF_Band')
    values(vox.root,{'volume':27,'pan':20,'oscAVolume':43,
                     'oscAWavetablePosition':22,'lpfFrequency':34,'lpfResonance':12,
                     'hpfFrequency':12,'envelope1.attack':27,'envelope1.decay':43,
                     'envelope1.sustain':44,'envelope1.release':31,
                     'envelope2.attack':39,'envelope2.decay':43,
                     'envelope2.sustain':34,'envelope2.release':34,
                     'lfo1Rate':3,'lfo2Rate':5})
    V.set_patch_cable(vox.root,'envelope2','oscAWavetablePosition',14)
    V.set_patch_cable(vox.root,'lfo1','oscAWavetablePosition',7)
    V.set_patch_cable(vox.root,'envelope2','lpfFrequency',5)
    FX.set_mod_fx(vox.root,kind='chorus',rate=4,depth=18)
    FX.set_delay(vox.root,analog=True,ping_pong=True,sync_level=8,
                 sync_type='dotted',feedback=14)
    FX.set_reverb_send(vox.root,22)
    result['LYRA VOX01']=vox

    metal=parse_file(ROOT/'refs/synths/TEMPL.XML')
    SY.set_wavetable(metal.root,TABLES['LYRA METAL01'])
    ST.set_attr(metal.root,'lpfMode','12dB')
    values(metal.root,{'volume':23,'pan':31,'oscAVolume':39,
                       'oscAWavetablePosition':29,'lpfFrequency':32,'lpfResonance':8,
                       'hpfFrequency':18,'waveFold':9,
                       'envelope1.attack':19,'envelope1.decay':39,
                       'envelope1.sustain':42,'envelope1.release':28,
                       'envelope2.attack':34,'envelope2.decay':40,
                       'envelope2.sustain':24,'envelope2.release':31,
                       'lfo1Rate':6,'lfo2Rate':8})
    V.set_patch_cable(metal.root,'envelope2','oscAWavetablePosition',-12)
    V.set_patch_cable(metal.root,'lfo1','oscAWavetablePosition',9)
    V.set_patch_cable(metal.root,'envelope2','lpfFrequency',9)
    FX.set_distortion(metal.root,saturation=4)
    FX.set_mod_fx(metal.root,kind='flanger',rate=6,depth=11,feedback=8)
    FX.set_delay(metal.root,analog=True,ping_pong=True,sync_level=7,
                 sync_type='dotted',feedback=17)
    FX.set_reverb_send(metal.root,16)
    result['LYRA METAL01']=metal
    return result


def events(clip):
    return sorted([(int(r.get('y')),n) for r in S.note_rows(clip)
                   for n in S.read_notes(r)],key=lambda e:(e[1].pos,e[0]))


def fingerprint(ev):
    return Counter((pitch,*astuple(n)) for pitch,n in ev)


def group_events(ev,connected):
    groups=[]
    end=-1
    for pitch,n in ev:
        if not groups or n.pos>(end+12 if connected else groups[-1][0][1].pos+20):
            groups.append([])
            end=n.pos+n.length
        groups[-1].append((pitch,n))
        end=max(end,n.pos+n.length)
    return groups


def voice_for(bar,family):
    if family=='tine':
        return next(v for stop,v in [(17,0),(25,1),(33,2),(41,0),
                                    (49,1),(57,2),(65,0),(10000,2)] if bar<stop)
    return next(v for stop,v in [(21,0),(29,1),(37,2),(45,0),
                                (53,1),(61,2),(10000,1)] if bar<stop)


def write_events(doc,clip,ev):
    for row in S.note_rows(clip):
        S.write_notes(row,[])
    by_pitch=defaultdict(list)
    for pitch,n in ev:
        by_pitch[pitch].append(n)
    M.scrivi(doc,clip,dict(by_pitch))


def build(source):
    doc=parse_file(source)
    if S.ticks_per_bar(doc.root)!=384:
        raise ValueError('expected the observed 384 tick grid')
    designs=presets()
    report=[]
    for label,family,new_names in [('LYRA TINE01','tine',('LYRA REED01','LYRA GLASS01')),
                                    ('LYRA ACID01','acid',('LYRA VOX01','LYRA METAL01'))]:
        old_inst=next(i for i in S.instruments(doc) if S.nome_strumento(i)==label)
        source_clips=[c for _,c in S.clips(doc) if S.instrument_of(doc,c) is old_inst]
        insts=A.instances(old_inst)
        if len(source_clips)!=1 or len(insts)!=1:
            raise ValueError('Expected one arranged clip for '+label+'; inspect the updated song')
        old_clip=source_clips[0]
        original=events(old_clip)
        origin=insts[0].pos
        buckets=[[],[],[]]
        for group in group_events(original,connected=family=='acid'):
            bar=1+(origin+group[0][1].pos)//384
            index=voice_for(bar,family)
            buckets[index].extend(group)
            report.append({'family':family,'bar':bar,'voice':(label,*new_names)[index],
                           'notes':len(group)})
        assert fingerprint(original)==fingerprint(sum(buckets,[]))
        if any(not b for b in buckets):
            raise ValueError('An intended voice received no music')
        write_events(doc,old_clip,buckets[0])
        for name,notes in zip(new_names,buckets[1:]):
            inst,clip=C.add_track(doc,designs[name],name=name,folder='SYNTHS/DelugePal',
                                  length=int(old_clip.get('length')),playing=True)
            S.set_key_mode(clip,False)
            write_events(doc,clip,notes)
            A.place(doc,inst,clip,origin,insts[0].length)
            if family=='acid':
                last=int(clip.get('length'))-1
                vals=(17,29,21,34,18) if name=='LYRA VOX01' else (33,19,29,16,30)
                automate(clip,'oscAWavetablePosition',[(round(last*i/4),v) for i,v in enumerate(vals)])
        assert A.instances(old_inst)==insts
    A.fit_view(doc)
    assert not M.verifica(doc),M.verifica(doc)
    return doc,designs,report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path)
    doc,designs,report=build(p.parse_args().source)
    fmt=FormatTable.load(ROOT/'out/format_table.json')
    for name,d in [('LYRA VIAREGGIO04',doc),*designs.items()]:
        assert not M.verifica(d),M.verifica(d)
        path=OUT/(name+'.XML');write_file(d,path,fmt)
        assert not M.verifica(parse_file(path))
    (OUT/'LYRA VIAREGGIO04.distribution.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    (OUT/'LYRA VIAREGGIO04.txt').write_text(M.racconta(doc),encoding='utf8')
    print(Counter({n:sum(r['notes'] for r in report if r['voice']==n) for n in {r['voice'] for r in report}}))
    print('warnings',M.avvertenze(doc))
    print(M.destinazione('LYRA VIAREGGIO',4))
    for n in designs:
        print(M.destinazione(n[:-2],1,'SYNTHS'))
