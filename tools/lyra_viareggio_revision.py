"""Revise only Acid articulation/sound and Tine sound on a fresh SD snapshot."""
from pathlib import Path
from dataclasses import replace
import argparse
import json
from delugexml import parse_file, write_file
from delugexml import song as S, musica as M, sound as V, structure as ST
from delugexml import effects as FX, arranger as A
from delugexml.writer import FormatTable
from lyra_viareggio import automate

ROOT=Path(__file__).resolve().parents[1]


def tine(owner, params):
    ST.set_attr(owner,'lpfMode','SVF_Band')
    for name,value in {'volume':25,'lpfFrequency':28,'lpfResonance':17,
                       'hpfFrequency':15,'envelope2.attack':0,
                       'envelope2.decay':26,'envelope2.sustain':8,
                       'envelope2.release':23}.items():
        V.set(params,name,value)
    V.set_patch_cable(params,'envelope2','lpfFrequency',12)
    FX.set_distortion(owner,saturation=7,bitcrush=3,decimation=5,params_node=params)
    FX.set_mod_fx(owner,kind='phaser',rate=7,depth=13,feedback=8,params_node=params)


def acid(owner, params):
    for name,value in {'volume':23,'envelope1.attack':24,'envelope1.decay':42,
                       'envelope1.sustain':43,'envelope1.release':30,
                       'envelope2.attack':36,'envelope2.decay':42,
                       'envelope2.sustain':30,'envelope2.release':34,
                       'oscAWavetablePosition':16,'lpfFrequency':22,
                       'lpfResonance':23,'lfo1Rate':3,'lfo2Rate':4}.items():
        V.set(params,name,value)
    V.set_patch_cable(params,'envelope2','oscAWavetablePosition',17)
    V.set_patch_cable(params,'envelope2','lpfFrequency',15)
    V.set_patch_cable(params,'lfo1','oscAWavetablePosition',12)
    V.set_patch_cable(params,'lfo2','lpfFrequency',4)
    FX.set_distortion(owner,saturation=3,params_node=params)


def sustain(doc,clip):
    """Keep existing pitches/onsets; extend to the next reply when close enough.

    1.5-bar isolated notes, up to 2 bars plus 12 ticks for linked replies.
    Existing dyads are retained and sustained with the leading voice.
    """
    bar=S.ticks_per_bar(doc.root)
    end=int(clip.get('length'))
    rows=S.note_rows(clip)
    onsets=sorted({n.pos for r in rows for n in S.read_notes(r)})
    lengths={}
    for i,pos in enumerate(onsets):
        # Very close onsets are members of a dyad, not a separate phrase.
        later=next((p for p in onsets[i+1:] if p-pos>=bar//2),end)
        length=later-pos+bar//32 if later-pos<=2*bar else 3*bar//2
        lengths[pos]=min(length,end-pos)
    changed=[]
    for row in rows:
        old=S.read_notes(row)
        new=[]
        for i,n in enumerate(old):
            length=lengths[n.pos]
            if i+1<len(old):
                length=min(length,old[i+1].pos-n.pos)
            new.append(replace(n,length=length))
            changed.append((n.pos,n.length,length))
        if old:
            S.write_notes(row,new)
    # Slow, explicit phrase sweeps in addition to envelopes and LFOs.
    starts=[]
    for pos in onsets:
        if not starts or pos-starts[-1]>=2*bar:
            starts.append(pos)
    for param,values in [('oscAWavetablePosition',(13,32,19)),
                         ('lpfFrequency',(20,29,22))]:
        points={0:values[0]}
        for i,pos in enumerate(starts):
            stop=min(pos+lengths[pos]-1,starts[i+1]-1 if i+1<len(starts) else end-1)
            points[pos]=values[0]
            points[pos+(stop-pos)//2]=values[1]
            points[stop]=values[2]
        automate(clip,param,sorted(points.items()))
    return changed


def build(source):
    doc=parse_file(source)
    before={S.nome_strumento(i):A.instances(i) for i in S.instruments(doc)}
    reports=[]
    for name,edit in [('LYRA TINE01',tine),('LYRA ACID01',acid)]:
        inst=next(i for i in S.instruments(doc) if S.nome_strumento(i)==name)
        for _,clip in S.clips(doc):
            if S.instrument_of(doc,clip) is inst:
                edit(inst,clip)
                if edit is acid:
                    reports.extend(sustain(doc,clip))
    assert before=={S.nome_strumento(i):A.instances(i) for i in S.instruments(doc)}
    if M.verifica(doc):
        raise ValueError(M.verifica(doc))
    return doc,reports


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source',type=Path)
    parser.add_argument('--tine-preset',type=Path)
    parser.add_argument('--acid-preset',type=Path)
    args=parser.parse_args()
    doc,report=build(args.source)
    dest=ROOT/'out/lyra_viareggio/LYRA VIAREGGIO02.XML'
    write_file(doc,dest,FormatTable.load(ROOT/'out/format_table.json'))
    reread=parse_file(dest)
    assert not M.verifica(reread)
    dest.with_suffix('.notes.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    dest.with_suffix('.txt').write_text(M.racconta(reread),encoding='utf8')
    print(M.destinazione('LYRA VIAREGGIO',2))
    print('validation',M.verifica(reread),'warnings',M.avvertenze(reread))
    for source,name,edit in ((args.tine_preset,'LYRA TINE',tine),
                              (args.acid_preset,'LYRA ACID',acid)):
        if source is not None:
            preset=parse_file(source)
            edit(preset.root,preset.root)
            assert not M.verifica(preset)
            output=dest.parent/(name+'02.XML')
            write_file(preset,output,FormatTable.load(ROOT/'out/format_table.json'))
            assert not M.verifica(parse_file(output))
            print(M.destinazione(name,2,'SYNTHS'))
