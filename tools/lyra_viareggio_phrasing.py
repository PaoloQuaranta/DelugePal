"""Revision 03: lower Acid, add connecting figures and varied Tine attacks.

Run only on a freshly downloaded revision 02. Sound parameters, modulation,
drums and arrangement instances are preserved.
"""
import argparse
from collections import defaultdict
from dataclasses import replace
from pathlib import Path
from delugexml import parse_file, write_file
from delugexml import song as S, musica as M, arranger as A
from delugexml.writer import FormatTable

ROOT=Path(__file__).resolve().parents[1]


def acid(doc,clip):
    M.trasponi(doc,clip,semitoni=-12)
    notes=defaultdict(list)
    phrases=0
    # Reply gestures in these song bars; leave the other sustained phrases alone.
    bars={15,27,35,43,51,59}
    for row in S.note_rows(clip):
        pitch=int(row.get('y'))
        for n in S.read_notes(row):
            bar=13+n.pos//384
            if bar in bars and pitch>=56 and n.length>=480:
                # Long anchor, one neighbouring pitch, return. Two deliberate
                # one-beat gestures, with overlap to keep the phrase connected.
                neighbour={56:59,59:60,60:59,64:60}.get(pitch,pitch)
                if neighbour==pitch:
                    notes[pitch].append(n)
                    continue
                first=n.length-192
                notes[pitch].append(replace(n,length=first+12))
                notes[neighbour].append(replace(n,pos=n.pos+first,length=108,
                                                velocity=max(1,n.velocity-8)))
                notes[pitch].append(replace(n,pos=n.pos+first+96,length=96,
                                            velocity=max(1,n.velocity-3)))
                phrases+=1
            else:
                notes[pitch].append(n)
    M.scrivi(doc,clip,dict(notes))
    return phrases


def tine(doc,clip):
    events=sorted((n.pos,int(r.get('y')),n) for r in S.note_rows(clip)
                  for n in S.read_notes(r))
    chords=[]
    for pos,pitch,n in events:
        if not chords or pos-chords[-1][0]>2:
            chords.append((pos,[]))
        chords[-1][1].append((pitch,n))
    notes=defaultdict(list)
    strums=echoes=shifts=0
    for i,(start,voices) in enumerate(chords):
        shift={3:-24,9:24,16:-24,23:24,31:-24,38:24}.get(i,0)
        shifts+=bool(shift)
        spread=4 if i%3==1 else (6 if i%7==3 else 0)
        strums+=bool(spread)
        ordered=sorted(voices,reverse=bool(i%2))
        for rank,(pitch,n) in enumerate(ordered):
            pos=start+shift+rank*spread if spread else n.pos+shift
            notes[pitch].append(replace(n,pos=pos))
        # Selected soft offbeat answers in the space after a complete voicing.
        next_start=chords[i+1][0] if i+1<len(chords) else int(clip.get('length'))
        last_end=max(n.pos+n.length for _,n in voices)+shift
        if i in (4,13,22,32) and last_end<start+120 and next_start>start+192:
            for rank,(pitch,n) in enumerate(sorted(voices)):
                notes[pitch].append(replace(n,pos=start+144+rank*3,length=30,
                                            velocity=max(1,n.velocity-15)))
            echoes+=1
    M.scrivi(doc,clip,dict(notes))
    return {'strums':strums,'rhythmic_shifts':shifts,'soft_answers':echoes}


def build(source):
    doc=parse_file(source)
    if S.ticks_per_bar(doc.root)!=384:
        raise ValueError('This revision expects the observed 384-tick grid')
    arrangement=[A.instances(i) for i in S.instruments(doc)]
    report=[]
    for _,clip in S.clips(doc):
        name=S.clip_label(clip)
        if name=='LYRA ACID01':
            report.append(('Acid connecting phrases',acid(doc,clip)))
        elif name=='LYRA TINE01':
            report.append(('Tine',tine(doc,clip)))
    assert arrangement==[A.instances(i) for i in S.instruments(doc)]
    assert not M.verifica(doc),M.verifica(doc)
    return doc,report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path)
    doc,report=build(p.parse_args().source)
    dest=ROOT/'out/lyra_viareggio/LYRA VIAREGGIO03.XML'
    write_file(doc,dest,FormatTable.load(ROOT/'out/format_table.json'))
    check=parse_file(dest)
    assert not M.verifica(check),M.verifica(check)
    dest.with_suffix('.txt').write_text(M.racconta(check),encoding='utf8')
    print(report)
    print('warnings',M.avvertenze(check))
    print(M.destinazione('LYRA VIAREGGIO',3))
