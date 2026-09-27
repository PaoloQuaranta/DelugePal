"""Checks preservation against the actual device snapshot, when available."""
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from delugexml import parse_file, song as S, arranger as A, musica as M
from lyra_viareggio import build, presets


@unittest.skipUnless((ROOT/'out/lyra_viareggio_source.XML').exists(), 'private device snapshot absent')
class LyraTest(unittest.TestCase):
    def test_original_form_notes_and_drum_identity_preserved(self):
        old=parse_file(ROOT/'out/lyra_viareggio_source.XML')
        new,_,_,report=build()
        for a,b in zip(S.instruments(old),S.instruments(new)):
            self.assertEqual(a.attrs,b.attrs)
            self.assertEqual(A.instances(a),A.instances(b))
        before=S.clips(old)
        after=S.clips(new)
        # New session clips precede arrangement-only clips in enumeration.
        for where,a in before:
            old_group=[c for group,c in before if group==where]
            new_group=[c for group,c in after if group==where]
            b=new_group[old_group.index(a)]
            for ra,rb in zip(S.note_rows(a),S.note_rows(b)):
                na,nb=S.read_notes(ra),S.read_notes(rb)
                self.assertEqual(len(na),len(nb))
                for x,y in zip(na,nb):
                    if S.is_kit_clip(a):
                        self.assertLessEqual(abs(x.pos-y.pos),3)
                        self.assertEqual((x.length,x.condition,x.iterance_divisor,x.iterance_steps,x.fill,x.lift),
                                         (y.length,y.condition,y.iterance_divisor,y.iterance_steps,y.fill,y.lift))
                    else:
                        self.assertEqual(x,y)
            # Audio contents and automation preserved; only view can change.
            if a.tag=='audioClip':
                self.assertEqual(a,b)
        self.assertFalse(M.verifica(new))
        self.assertFalse(M.avvertenze(new))
        self.assertEqual(sum(r['notes'] for r in report),1032)
        self.assertEqual(A.extent(old),A.extent(new))

    def test_presets_in_song_match_exported_oscillators(self):
        doc,ep,wt,_=build()
        for inst,preset in zip(S.instruments(doc)[-2:],(ep,wt)):
            self.assertEqual(inst.find('osc1').attrs,preset.root.find('osc1').attrs)
        self.assertFalse(M.verifica(ep))
        self.assertFalse(M.verifica(wt))
