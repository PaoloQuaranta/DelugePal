"""Probe P1: un sample come oscillatore di quattro synth nuovi."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from delugexml import parse, serialize  # noqa: E402
from delugexml import musica as MU, song as S  # noqa: E402


class SampleOscillatorTest(unittest.TestCase):
    def test_probe_isolates_modes_on_new_synths(self):
        from sample_oscillator_probe import costruisci  # noqa: PLC0415

        doc = costruisci()
        instruments = S.instruments(doc)
        clips = doc.root.find('sessionClips').children
        self.assertEqual(len(instruments), 4)
        self.assertEqual(len(clips), 4)
        self.assertAlmostEqual(S.get_bpm(doc.root), 171)
        self.assertTrue(S.in_scale(doc.root, 60))
        expected = [
            ('ONCE', '1', '0', '0'),
            ('LOOP', '2', '0', '0'),
            ('REVERSE', '1', '1', '0'),
            ('STRETCH', '3', '0', '1'),
        ]
        for i, (name, mode, reverse, stretch) in enumerate(expected):
            inst, clip = instruments[i], clips[i]
            osc = inst.find('osc1')
            self.assertEqual(clip.get('clipName'), name)
            self.assertEqual(inst.tag, 'sound')
            self.assertEqual(osc.get('type'), 'sample')
            self.assertEqual(osc.get('fileName'),
                             'SAMPLES/sampleswap/advanced_operator_samplepack/'
                             'drums/original AMEN.wav')
            self.assertEqual((osc.get('loopMode'), osc.get('reversed'),
                              osc.get('timeStretchEnable')),
                             (mode, reverse, stretch))
            zone = osc.find('zone')
            self.assertEqual((zone.get('startSamplePos'),
                              zone.get('endSamplePos')), ('0', '268795'))
            self.assertEqual(clip.get('length'), '3072')
            self.assertEqual(clip.get('isPlaying'), '1' if i == 0 else '0')
            rows = S.note_rows(clip)
            self.assertEqual(len(rows), 1)
            notes = S.read_notes(rows[0])
            self.assertEqual([(n.pos, n.length) for n in notes], [(0, 3071)])

        reread = parse(serialize(doc))
        self.assertEqual(MU.verifica(reread), [])
        self.assertEqual(MU.avvertenze(reread), [])


if __name__ == '__main__':
    unittest.main()
