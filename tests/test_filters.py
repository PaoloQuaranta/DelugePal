"""Regressioni autonome per filtri community (senza corpus)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from delugexml import parse, serialize, structure as ST, sound as SND


class FiltersTest(unittest.TestCase):
    def setUp(self):
        self.doc = parse('<sound lpfMode="24dB" hpfMode="HPLadder" filterRoute="H2L">'
                         '<defaultParams lpfMorph="0x80000000" hpfMorph="0x80000000" '
                         'volume="0x00000000" /></sound>')
        self.inst = self.doc.root

    def test_routes_and_roundtrip(self):
        for route in ('H2L', 'L2H', 'PARA'):
            ST.set_filter(self.inst, route=route, lpf='SVF_Band',
                          hpf='SVF_Notch', lpf_morph=25, hpf_morph=50)
            reread = parse(serialize(self.doc)).root
            self.assertEqual(ST.describe(reread)['filterRoute'], route)
            self.assertEqual(SND.get(reread, 'lpfMorph'), 25)
            self.assertEqual(SND.get(reread, 'hpfMorph'), 50)
            self.assertEqual(SND.get(reread, 'volume'), 25)

    def test_invalid_is_atomic(self):
        for kwargs in ({'route': 'parallel'}, {'hpf': '24dB'},
                       {'lpf_morph': -1}, {'hpf_morph': 51},
                       {'lpf_morph': True}, {'lpf_morph': 1.5}):
            before = serialize(self.doc)
            with self.assertRaises(ValueError):
                ST.set_filter(self.inst, lpf='SVF_Band', **kwargs)
            self.assertEqual(serialize(self.doc), before)

    def test_clip_params_and_preserve_morph(self):
        clip = parse('<instrumentClip><soundParams lpfMorph="0x80000000" '
                     'hpfMorph="0x80000000" /></instrumentClip>').root
        ST.set_filter(self.inst, params_node=clip, hpf_morph=32)
        ST.set_filter(self.inst, hpf='SVF_Band')
        self.assertEqual(SND.get(clip, 'hpfMorph'), 32)
        self.assertEqual(SND.get(self.inst, 'hpfMorph'), 0)

    def test_missing_param_is_atomic(self):
        clip = parse('<instrumentClip><soundParams lpfMorph="0x80000000" />'
                     '</instrumentClip>').root
        before = serialize(self.doc)
        with self.assertRaises(ValueError):
            ST.set_filter(self.inst, route='L2H', params_node=clip,
                          lpf_morph=25, hpf_morph=25)
        self.assertEqual(serialize(self.doc), before)
        self.assertEqual(SND.get(clip, 'lpfMorph'), 0)

    def test_kit_and_rejected_target(self):
        kit = parse('<kit />').root
        ST.set_filter(kit, lpf='SVF_Notch', hpf='Off', route='PARA')
        self.assertEqual(kit.get('filterRoute'), 'PARA')
        with self.assertRaises(ValueError):
            ST.set_filter(parse('<instrumentClip />').root, route='L2H')

    def test_fixture_roundtrip(self):
        from filtri_scritto import costruisci, CASES, ROOT
        if not (ROOT / 'refs/synths/TEMPL.XML').exists():
            self.skipTest('preset privato assente')
        doc = parse(serialize(costruisci()))
        self._assert_fixture(doc, CASES)

    def test_device_resave(self):
        from filtri_scritto import costruisci, CASES, ROOT
        from delugexml import parse_file, song as S
        path = ROOT / 'out/FILTER01_2.XML'
        if not path.exists():
            self.skipTest('risalvataggio dal dispositivo assente')
        expected = costruisci()
        actual = parse_file(path)
        self._assert_fixture(actual, CASES)
        expected_clips = [c for _, c in S.clips(expected)]
        actual_clips = [c for _, c in S.clips(actual)]
        for before, after in zip(expected_clips, actual_clips):
            self.assertEqual(
                [(r.get('y'), S.read_notes(r)) for r in S.note_rows(after)],
                [(r.get('y'), S.read_notes(r)) for r in S.note_rows(before)])
            for param in ('lpfMorph', 'hpfMorph'):
                self.assertEqual(SND.get_raw(after, param),
                                 SND.get_raw(before, param))

    def _assert_fixture(self, doc, cases):
        from delugexml import song as S, musica as MU, automation as AU, params as P
        self.assertEqual(MU.verifica(doc), [])
        self.assertEqual(MU.avvertenze(doc), [])
        self.assertEqual(S.get_bpm(doc.root), 100)
        clips = [c for _, c in S.clips(doc)]
        self.assertEqual(len(clips), 9)
        self.assertEqual(sum(c.get('isPlaying') == '1' for c in clips), 1)
        bar = S.ticks_per_bar(doc.root)
        for clip, inst, case in zip(clips, S.instruments(doc), cases):
            name, lpf, hpf, route, varying = case
            self.assertEqual(clip.get('clipName'), name)
            self.assertEqual(inst.get('filterRoute'), route)
            self.assertEqual(inst.get('lpfMode'), lpf)
            self.assertEqual(inst.get('hpfMode'), hpf)
            self.assertEqual(int(clip.get('length')), bar * 4)
            if varying:
                _, points = AU.decode(SND.get_raw(clip, varying))
                self.assertEqual([(p.pos, P.to_display(p.hex), p.interp) for p in points],
                                 [(i * bar, v, False) for i, v in enumerate((0, 25, 50, 0))])


if __name__ == '__main__':
    unittest.main()
