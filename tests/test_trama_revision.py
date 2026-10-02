"""Guardiani della revisione da un salvataggio utente, non da preset ricreati."""
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from delugexml import parse, serialize, song as S, sound as V, musica as M
from delugexml import arranger as A
from delugexml.writer import FormatTable
import trama_scritto as TR
import trama_revisione as RV


def semantic(node):
    return (node.tag, sorted(node.attrs), node.text,
            tuple(semantic(c) for c in node.children))


def events(clip):
    return sorted((n.pos, int(r.get('y')), n.length, n.velocity)
                  for r in S.note_rows(clip) for n in S.read_notes(r))


class TramaCorpusAvailabilityTest(unittest.TestCase):
    def test_main_suite_reports_missing_revision_corpus_as_skip(self):
        import test_all as suite
        from contextlib import redirect_stdout
        from io import StringIO
        from tempfile import TemporaryDirectory
        from unittest.mock import patch
        with TemporaryDirectory() as directory:
            with patch.object(TR, 'TEMPLATE', Path(directory) / 'missing.XML'), \
                 patch.object(suite, 'results', []), patch.object(suite, 'skipped', []):
                with redirect_stdout(StringIO()):
                    suite.test_trama_saved_revision()
                self.assertEqual(suite.results, [])
                self.assertEqual(len(suite.skipped), 1)

    def test_missing_private_template_is_skipped_not_failed(self):
        from tempfile import TemporaryDirectory
        from unittest.mock import patch
        with TemporaryDirectory() as directory:
            with patch.object(TR, 'TEMPLATE', Path(directory) / 'missing.XML'):
                result = unittest.TestResult()
                TramaRevisionTest('test_preserves_source_and_user_sound_and_mix').run(result)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.failures, [])
        self.assertEqual(len(result.skipped), 1)


class TramaRevisionTest(unittest.TestCase):
    def test_final_filo_level_preserves_user_mix_and_every_non_patch_datum(self):
        from dataclasses import replace
        from delugexml import synthesis as SY
        saved = RV.raise_filo_carriers(self.doc)
        inst, clips = RV.tracks(saved)
        V.set(clips['FILO'], 'volume', 50)
        V.set_raw(clips['OMBRA'], 'lpfFrequency', '0xCA123456')
        before = semantic(saved.root)
        old = SY.DX7Patch.decode(inst['FILO'].find('osc1').get('dx7patch'))
        final = RV.raise_filo_carriers(saved, final=True)
        final_inst, _ = RV.tracks(final)
        actual = SY.DX7Patch.decode(final_inst['FILO'].find('osc1').get('dx7patch'))
        self.assertEqual([op.level for op in actual.operators], [99,67,99,61,99,55])
        self.assertEqual([op.velocity for op in actual.operators], [2,4,2,5,2,4])
        self.assertEqual(actual.operators[1::2], old.operators[1::2])
        restored = replace(actual, operators=tuple(
            replace(op, level=original.level, velocity=original.velocity)
            for op, original in zip(actual.operators, old.operators)))
        self.assertEqual(restored, old)
        self.assertEqual(semantic(saved.root), before)
        table = FormatTable.load(ROOT / 'out' / 'format_table.json')
        reread = parse(serialize(final, table))
        self.assertEqual(M.verifica(reread), [])
        SY.update_dx7_patch(RV.tracks(reread)[0]['FILO'], old)
        self.assertEqual(semantic(reread.root), before)

    def test_final_filo_refuses_changed_carriers_without_mutating_source(self):
        before = semantic(self.doc.root)
        with self.assertRaises(ValueError):
            RV.raise_filo_carriers(self.doc, final=True)
        self.assertEqual(semantic(self.doc.root), before)

    def test_carrier_boost_preserves_saved_song_except_three_output_levels(self):
        from dataclasses import replace
        from delugexml import synthesis as SY
        V.set(self.clips1['FILO'], 'volume', 50)
        before = semantic(self.doc.root)
        boosted = RV.raise_filo_carriers(self.doc)
        inst, clips = RV.tracks(boosted)
        old = SY.DX7Patch.decode(self.inst1['FILO'].find('osc1').get('dx7patch'))
        new = SY.DX7Patch.decode(inst['FILO'].find('osc1').get('dx7patch'))
        self.assertEqual([op.level for op in new.operators], [99, 67, 91, 61, 83, 55])
        self.assertEqual(V.get(clips['FILO'], 'volume'), 50)
        self.assertEqual(semantic(self.doc.root), before)
        expected = replace(old, operators=tuple(
            replace(op, level=level) for op, level in zip(old.operators, [99,67,91,61,83,55])))
        self.assertEqual(new, expected)
        table = FormatTable.load(ROOT / 'out' / 'format_table.json')
        reread = parse(serialize(boosted, table))
        self.assertEqual(semantic(reread.root), semantic(boosted.root))
        self.assertEqual(M.verifica(reread), [])
        before_boosted = semantic(boosted.root)
        with self.assertRaises(ValueError):
            RV.raise_filo_carriers(boosted)
        self.assertEqual(semantic(boosted.root), before_boosted)
        SY.update_dx7_patch(inst['FILO'], old)
        self.assertEqual(semantic(boosted.root), before)

    def setUp(self):
        try:
            self.source = TR.costruisci()
        except FileNotFoundError as error:
            raise unittest.SkipTest(f'manca corpus privato: {error.filename or error}') from error
        inst, clips = RV.tracks(self.source)
        # Cambiamenti utente deliberatamente diversi dal generatore e dalla 03 reale.
        V.set_raw(clips['OMBRA'], 'lpfFrequency', '0xCE123456')
        V.set(clips['OMBRA'], 'volume', 10)
        V.set(clips['CAMPO'], 'volume', 15)
        V.set(clips['GROUND'], 'volume', 32)
        inst['OMBRA'].set('clippingAmount', '1')
        self.before = semantic(self.source.root)
        self.doc = RV.build(self.source)
        self.inst0, self.clips0 = RV.tracks(self.source)
        self.inst1, self.clips1 = RV.tracks(self.doc)

    def test_preserves_source_and_user_sound_and_mix(self):
        self.assertEqual(semantic(self.source.root), self.before)
        for name in ('OMBRA', 'CAMPO', 'GROUND', 'FILO', 'TRAMA BEAT'):
            self.assertEqual(semantic(self.inst0[name]), semantic(self.inst1[name]))
        for name in ('OMBRA', 'CAMPO', 'GROUND', 'TRAMA BEAT'):
            for param in V.names(self.clips0[name]):
                self.assertEqual(V.get_raw(self.clips0[name], param),
                                 V.get_raw(self.clips1[name], param), (name, param))
        self.assertEqual(semantic(self.clips0['TRAMA BEAT']),
                         semantic(self.clips1['TRAMA BEAT']))

    def test_filo_changes_only_outer_envelope(self):
        allowed = {'envelope1.attack', 'envelope1.sustain', 'envelope1.release'}
        for param in V.names(self.clips0['FILO']):
            if param not in allowed:
                self.assertEqual(V.get_raw(self.clips0['FILO'], param),
                                 V.get_raw(self.clips1['FILO'], param), param)
        self.assertEqual([V.get(self.clips1['FILO'], p) for p in
                          ('envelope1.attack', 'envelope1.sustain', 'envelope1.release')],
                         [0, 50, 50])
        self.assertEqual(events(self.clips0['FILO']), events(self.clips1['FILO']))

    def test_bass_lands_on_kick_with_clear_roots(self):
        expected_roots = [31, 36, 29, 31, 31, 36, 36, 31]  # G1 C2 F1 G1 / G1 C2 C2 G1
        notes = events(self.clips1['GROUND'])
        for index, root in enumerate(expected_roots, 6):
            in_bar = [(pos - index * RV.B, pitch, length)
                      for pos, pitch, length, _ in notes
                      if index * RV.B <= pos < (index + 1) * RV.B]
            self.assertEqual(in_bar, [(0, root, 180), (216, root, 144)])
        for bar in range(6, 52):
            in_bar = [(p, y) for p, y, _, _ in notes
                      if bar * RV.B <= p < (bar + 1) * RV.B]
            self.assertEqual([p - bar * RV.B for p, _ in in_bar], [0, 216])
            self.assertEqual(len({y for _, y in in_bar}), 1)
        self.assertTrue(all(29 <= pitch <= 36 for _, pitch, _, _ in notes))
        self.assertEqual(notes[-1][:3], (56 * RV.B, 31, 2 * RV.B))

    def test_harmony_and_chromatic_conflicts_are_realized(self):
        self.assertEqual(S.get_scale(self.doc), (7, (0, 2, 3, 5, 7, 9, 10)))
        scale = {0, 2, 4, 5, 7, 9, 10}  # G dorian: C D E F G A Bb
        for name in ('FILO', 'OMBRA', 'CAMPO', 'GROUND'):
            self.assertTrue(all(y % 12 in scale for _, y, _, _ in events(self.clips1[name])))
        # Il punto prima incompatibile ora presenta Do/A nel controcanto,
        # Do nel basso e Mi/Sol nel campo: appartengono allo stesso accordo di Do6.
        for name, expected in (('GROUND', {36}), ('CAMPO', {55, 64}),
                               ('OMBRA', {45, 48})):
            actual = {y for p, y, length, _ in events(self.clips1[name])
                      if p < 30 * RV.B and p + length > 29 * RV.B}
            self.assertEqual(actual, expected, name)
        # Il campo non attraversa mai un cambio di fondamentale.
        for pos, _, length, _ in events(self.clips1['CAMPO']):
            names = {RV.HARMONY[bar] for bar in range(pos // RV.B,
                      (pos + length - 1) // RV.B + 1)}
            self.assertEqual(len(names), 1)

    def test_preserves_upper_rhythm_and_silences_with_coda_resolution(self):
        old = events(self.clips0['OMBRA'])
        new = events(self.clips1['OMBRA'])
        before_coda = 57 * RV.B + 192
        self.assertEqual([(p, length, vel) for p, _, length, vel in old if p < before_coda],
                         [(p, length, vel) for p, _, length, vel in new if p < before_coda])
        self.assertEqual([(p, y, length) for p, y, length, _ in new if p >= before_coda],
                         [(57 * RV.B + 192, 60, 96), (57 * RV.B + 288, 58, 96)])
        for bar in (31, 43):
            for name in ('FILO', 'OMBRA', 'CAMPO'):
                self.assertFalse(any(p < (bar + 1) * RV.B and p + length > bar * RV.B
                                     for p, _, length, _ in events(self.clips1[name])))

    def test_valid_roundtrip_and_form(self):
        table = FormatTable.load(ROOT / 'out' / 'format_table.json')
        reread = parse(serialize(self.doc, table))
        self.assertEqual(semantic(reread.root), semantic(self.doc.root))
        self.assertEqual(A.extent(reread), (0, 58 * RV.B))
        self.assertEqual(M.verifica(reread), [])
        self.assertEqual(M.avvertenze(reread), [])

    def test_rejects_an_unexpected_source_before_mutation(self):
        changed = deepcopy(self.source)
        _, clips = RV.tracks(changed)
        S.set_clip_length(clips['GROUND'], 8 * RV.B)
        before = semantic(changed.root)
        with self.assertRaises(ValueError):
            RV.build(changed)
        self.assertEqual(semantic(changed.root), before)


if __name__ == '__main__':
    unittest.main()
