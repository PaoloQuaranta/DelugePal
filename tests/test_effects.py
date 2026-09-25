"""Effetti standard: test autonomi, senza song o preset privati."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from delugexml import parse, serialize, parse_file, sound as SND
from delugexml import effects as FX


class EffectsTest(unittest.TestCase):
    def setUp(self):
        self.doc = parse_file(Path(__file__).resolve().parents[1] / 'refs/synths/TEMPL.XML')
        self.sound = self.doc.root

    def test_delay_roundtrip_and_untouched_automation(self):
        SND.set_raw(self.sound, 'modFXDepth', '0x00000000000000008000000000')
        untouched = SND.get_raw(self.sound, 'modFXDepth')
        FX.set_delay(self.sound, analog=True, ping_pong=False, sync_level=7,
                     sync_type='triplet', feedback=22, rate=30)
        node = parse(serialize(self.doc)).root
        self.assertEqual(node.find('delay').get('syncType'), '10')
        self.assertEqual(node.find('delay').get('pingPong'), '0')
        self.assertEqual(SND.get(node, 'delayFeedback'), 22)
        self.assertEqual(SND.get_raw(node, 'modFXDepth'), untouched)

    def test_mod_fx_all_standard_types_and_separate_clip(self):
        clip = parse('<instrumentClip><soundParams modFXRate="0x00000000" '
                     'modFXDepth="0x00000000" /></instrumentClip>').root
        for kind in ('none', 'flanger', 'phaser', 'chorus', 'StereoChorus'):
            FX.set_mod_fx(self.sound, kind=kind, rate=17, depth=33, params_node=clip)
            self.assertEqual(self.sound.get('modFXType'), kind)
            self.assertEqual(SND.get(clip, 'modFXDepth'), 33)
        self.assertEqual(SND.get(self.sound, 'modFXDepth'), 25)

    def test_eq_and_distortion(self):
        FX.set_eq(self.sound, bass=25, treble=32, bass_frequency=20)
        FX.set_distortion(self.sound, saturation=15, bitcrush=13, decimation=21)
        node = parse(serialize(self.doc)).root
        self.assertEqual(node.get('clippingAmount'), '15')
        self.assertEqual(SND.get(node, 'equalizer.treble'), 32)
        self.assertEqual(SND.get(node, 'bitCrush'), 13)
        self.assertEqual(SND.get(node, 'sampleRateReduction'), 21)

    def test_unpatched_delay_layouts(self):
        for tag, cont in (('song', 'songParams'), ('kit', 'defaultParams')):
            doc = parse(f'<{tag}><{cont}><delay rate="0x00000000" '
                        f'feedback="0x80000000" /></{cont}></{tag}>')
            FX.set_delay(doc.root, analog=False, sync_type='dotted', feedback=20, rate=12)
            node = parse(serialize(doc)).root
            self.assertEqual(node.find('delay').get('syncType'), '19')
            self.assertEqual(SND.get(node, 'delay.feedback'), 20)
            self.assertEqual(SND.get(node, 'delay.rate'), 12)

    def test_audio_structure_belongs_to_track(self):
        from delugexml import audio
        track = parse(audio.TRACCIA_XML)
        clip = parse('<audioClip>' + audio.PARAMS_XML + '</audioClip>')
        FX.set_delay(track.root, analog=True, feedback=19, params_node=clip.root)
        self.assertEqual(track.root.find('delay').get('analog'), '1')
        self.assertEqual(SND.get(clip.root, 'delay.feedback'), 19)
        self.assertIsNone(clip.root.find('delay'))
        with self.assertRaises(ValueError):
            FX.set_mod_fx(clip.root, kind='phaser')

    def test_reverb_bad_value_preserves_global_config(self):
        doc = parse('<song><reverb model="1" roomSize="123" /></song>')
        before = serialize(doc)
        with self.assertRaises(ValueError):
            FX.set_reverb(doc.root, model='digital', room_size=51)
        self.assertEqual(serialize(doc), before)

    def test_fixture(self):
        from effetti_scritto import costruisci, CASES, ROOT
        if not (ROOT / 'refs/songs/TEMPL0.XML').exists():
            self.skipTest('template song privato assente')
        from delugexml import song as S, musica as MU
        doc = parse(serialize(costruisci()))
        clips = [c for _, c in S.clips(doc)]
        self.assertEqual(len(clips), len(CASES))
        self.assertEqual(sum(c.get('isPlaying') == '1' for c in clips), 1)
        self.assertEqual(MU.verifica(doc), [])
        self.assertEqual(MU.avvertenze(doc), [])
        for clip, inst, case in zip(clips, S.instruments(doc), CASES):
            name, family, options = case
            self.assertEqual(clip.get('clipName'), name)
            self.assertEqual(SND.get(clip, 'reverbAmount'), 25 if family == 'reverb' else 0)
            self.assertEqual(SND.get(clip, 'delayFeedback'), 22 if family == 'delay' else 0)
            self.assertEqual(inst.get('modFXType'), options.get('kind', 'none'))
            self.assertEqual(inst.get('clippingAmount'), str(options.get('saturation', 0)))

    def test_device_resave(self):
        """Il Deluge deve conservare ogni confronto FX, non solo aprire il file."""
        from effetti_scritto import costruisci, CASES, ROOT
        from delugexml import song as S, musica as MU
        path = ROOT / 'out/FXSTD01 2.XML'
        if not path.exists():
            self.skipTest('risalvataggio privato dal Deluge assente')
        expected = costruisci()
        actual = parse_file(path)
        self.assertEqual(MU.verifica(actual), [])
        self.assertEqual(MU.avvertenze(actual), [])
        expected_insts, actual_insts = S.instruments(expected), S.instruments(actual)
        expected_clips = [c for _, c in S.clips(expected)]
        actual_clips = [c for _, c in S.clips(actual)]
        self.assertEqual(len(actual_clips), len(CASES))
        self.assertEqual(len(actual_insts), len(CASES))
        reverb_a, reverb_b = expected.root.find('reverb'), actual.root.find('reverb')
        self.assertEqual(reverb_a.get('model'), reverb_b.get('model'))
        for attr in ('roomSize', 'dampening', 'width', 'hpf', 'lpf'):
            # Il motore converte fra int32 e float32 nel risalvataggio.
            self.assertLessEqual(abs(int(reverb_a.get(attr)) - int(reverb_b.get(attr))), 128)
        for before_inst, after_inst, before_clip, after_clip in zip(
                expected_insts, actual_insts, expected_clips, actual_clips):
            self.assertEqual(before_clip.get('clipName'), after_clip.get('clipName'))
            self.assertEqual(before_clip.get('section'), after_clip.get('section'))
            for attr in ('modFXType',):
                self.assertEqual(before_inst.get(attr), after_inst.get(attr))
            # Il firmware omette la saturazione nulla; la non nulla resta.
            self.assertEqual(int(before_inst.get('clippingAmount', '0')),
                             int(after_inst.get('clippingAmount', '0')))
            for attr in ('analog', 'pingPong', 'syncLevel', 'syncType'):
                self.assertEqual(before_inst.find('delay').get(attr),
                                 after_inst.find('delay').get(attr))
            for attr in ('delayRate', 'delayFeedback', 'modFXRate', 'modFXDepth',
                         'modFXFeedback', 'modFXOffset', 'reverbAmount',
                         'equalizer.bass', 'equalizer.treble',
                         'equalizer.bassFrequency', 'equalizer.trebleFrequency',
                         'bitCrush', 'sampleRateReduction'):
                self.assertEqual(SND.get_raw(before_clip, attr),
                                 SND.get_raw(after_clip, attr),
                                 f'{before_clip.get("clipName")}: {attr}')
            self.assertEqual(
                [(r.get('y'), S.read_notes(r)) for r in S.note_rows(before_clip)],
                [(r.get('y'), S.read_notes(r)) for r in S.note_rows(after_clip)])

    def test_reverb_global_is_distinct_from_send(self):
        doc = parse('<song><reverb model="1" roomSize="1288490112">'
                    '<compressor attack="327244" /></reverb>'
                    '<songParams reverbAmount="0x80000000" /></song>')
        FX.set_reverb(doc.root, model='digital', room_size=25, damping=50, width=0)
        FX.set_reverb_send(self.sound, 18)
        node = parse(serialize(doc)).root
        self.assertEqual(node.find('reverb').get('model'), '2')
        self.assertEqual(node.find('reverb').get('roomSize'), '1073741824')
        self.assertEqual(node.find('reverb').get('dampening'), '2147483647')
        self.assertEqual(node.find('reverb').find('compressor').get('attack'), '327244')
        self.assertEqual(SND.get(node, 'reverbAmount'), 0)
        self.assertEqual(SND.get(self.sound, 'reverbAmount'), 18)

    def test_invalid_calls_are_atomic(self):
        calls = (
            lambda: FX.set_delay(self.sound, analog=True, feedback=51),
            lambda: FX.set_delay(self.sound, analog='yes'),
            lambda: FX.set_delay(self.sound, sync_type='swing'),
            lambda: FX.set_delay(self.sound, sync_level=-1),
            lambda: FX.set_mod_fx(self.sound, kind='invented', depth=12),
            lambda: FX.set_eq(self.sound, bass=12, treble=True),
            lambda: FX.set_distortion(self.sound, bitcrush=10, saturation=16),
            lambda: FX.set_distortion(self.sound, saturation=3, decimation=1.5),
            lambda: FX.set_reverb(self.sound, model='digital'),
        )
        for call in calls:
            before = serialize(self.doc)
            with self.assertRaises(ValueError):
                call()
            self.assertEqual(serialize(self.doc), before)

    def test_missing_param_does_not_partially_change_either_node(self):
        clip = parse('<instrumentClip><soundParams modFXRate="0x00000000" />'
                     '</instrumentClip>')
        before = serialize(self.doc), serialize(clip)
        with self.assertRaises(ValueError):
            FX.set_mod_fx(self.sound, kind='phaser', rate=13, depth=42,
                          params_node=clip.root)
        self.assertEqual((serialize(self.doc), serialize(clip)), before)


if __name__ == '__main__':
    unittest.main()
