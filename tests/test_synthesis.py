import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from delugexml import parse_file, serialize
from delugexml import synthesis as SY


class SynthesisTest(unittest.TestCase):
    def test_device_dx7_payload_roundtrip(self):
        doc = parse_file(ROOT / 'refs/songs/Qbix.XML')
        osc = next(n for n in doc.iter() if n.get('dx7patch'))
        patch = SY.DX7Patch.decode(osc.get('dx7patch'))
        self.assertEqual(patch.encode(), osc.get('dx7patch'))
        self.assertEqual(patch.name, 'HARP-FLUTE')

    def test_operator_order_and_algorithm_units(self):
        ops = [SY.DX7Operator(level=80+i, coarse=i) for i in range(1, 7)]
        patch = SY.DX7Patch(tuple(ops), algorithm=5, name='LYRA TINE')
        data = bytes.fromhex(patch.encode())
        self.assertEqual(len(data), 156)
        self.assertEqual((data[16], data[18]), (86, 6))
        self.assertEqual((data[121], data[123]), (81, 1))
        self.assertEqual(data[134], 4)
        self.assertEqual(data[155], 63)

    def test_invalid_patch_does_not_mutate_preset(self):
        doc = parse_file(ROOT / 'refs/synths/TEMPL.XML')
        before = serialize(doc)
        with self.assertRaises(ValueError):
            SY.set_dx7(doc.root, SY.DX7Patch((SY.DX7Operator(coarse=32),)*6))
        self.assertEqual(serialize(doc), before)

    def test_dx7_envelope_and_wavetable_switch(self):
        from delugexml import sound as V
        doc = parse_file(ROOT / 'refs/synths/TEMPL.XML')
        SY.set_dx7(doc.root, SY.DX7Patch((SY.DX7Operator(),)*6))
        self.assertEqual(V.get(doc.root, 'envelope1.release'), 50)
        self.assertEqual(V.get(doc.root, 'envelope1.sustain'), 50)
        self.assertFalse(any(c['source']=='velocity' and c['destination']=='volume'
                             for c in V.patch_cables(doc.root)))
        SY.set_wavetable(doc.root, 'SAMPLES/WAVETABLES/CommunityWavetables/Acid.wav')
        osc = doc.root.find('osc1')
        self.assertEqual(osc.get('type'), 'wavetable')
        self.assertIsNone(osc.get('dx7patch'))
        self.assertEqual(osc.get('fileName'), 'SAMPLES/WAVETABLES/CommunityWavetables/Acid.wav')

    def test_sample_ranges_removed_when_switching_to_table(self):
        doc = parse_file(ROOT / 'refs/synths/Tal Rhodes.XML')
        osc = doc.root.find('osc1')
        self.assertTrue(osc.children)
        SY.set_wavetable(doc.root, 'SAMPLES/WAVETABLES/CommunityWavetables/Acid.wav')
        self.assertFalse(osc.children)
        self.assertIsNone(osc.get('loopMode'))

    def test_invalid_path_is_atomic(self):
        doc = parse_file(ROOT / 'refs/synths/TEMPL.XML')
        for path in ('SAMPLES/../bad.wav', 'SAMPLES/x.wav\n', 'SAMPLES/x.xml'):
            before = serialize(doc)
            with self.assertRaises(ValueError):
                SY.set_wavetable(doc.root, path)
            self.assertEqual(serialize(doc), before)

    def test_wavetable_note_ranges_roundtrip_and_switch(self):
        from delugexml.writer import FormatTable
        doc = parse_file(ROOT / 'refs/synths/TEMPL.XML')
        paths = ('SAMPLES/WAVETABLES/CommunityWavetables/Acid.wav',
                 'SAMPLES/WAVETABLES/CommunityWavetables/Allophones.wav',
                 'SAMPLES/WAVETABLES/CommunityWavetables/Bowed Metal [ML].wav')
        ranges = [(59, paths[0]), (71, paths[1]), (None, paths[2])]
        SY.set_wavetable_ranges(doc.root, ranges, experimental=True)
        self.assertEqual(SY.wavetable_ranges(doc.root), ranges)
        table = FormatTable.load(ROOT / 'out/format_table.json')
        encoded = serialize(doc, table)
        from delugexml import parse
        reread = parse(encoded)
        self.assertEqual(SY.wavetable_ranges(reread.root), ranges)
        self.assertIn('fileName="'+paths[2]+'"', encoded.split('<wavetableRanges>')[0])
        self.assertEqual(encoded.count('<wavetableRange\n'), 2)
        SY.set_wavetable(reread.root, paths[1])
        self.assertEqual(SY.wavetable_ranges(reread.root), [(None, paths[1])])
        self.assertIsNone(reread.root.find('osc1').find('wavetableRanges'))

    def test_invalid_wavetable_ranges_are_atomic(self):
        doc = parse_file(ROOT / 'refs/synths/TEMPL.XML')
        before = serialize(doc)
        good = 'SAMPLES/WAVETABLES/CommunityWavetables/Acid.wav'
        for ranges in ([(59, good)], [(59, good), (71, good)],
                       [(60, good), (60, good), (None, good)],
                       [(59, good), (None, 'SAMPLES/../bad.wav')]):
            with self.assertRaises(ValueError):
                SY.set_wavetable_ranges(doc.root, ranges, experimental=True)
            self.assertEqual(serialize(doc), before)

    def test_multirange_write_requires_explicit_experimental_opt_in(self):
        doc = parse_file(ROOT / 'refs/synths/TEMPL.XML')
        before = serialize(doc)
        with self.assertRaisesRegex(RuntimeError, 'crashes'):
            SY.set_wavetable_ranges(doc.root, [
                (59, 'SAMPLES/WAVETABLES/CommunityWavetables/Acid.wav'),
                (None, 'SAMPLES/WAVETABLES/CommunityWavetables/Allophones.wav'),
            ])
        self.assertEqual(serialize(doc), before)
