"""Explicitly synthetic fixtures: software checks, never benchmark observations."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("paired_analysis", Path(__file__).with_name("analyze.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def row(method, identifier="synthetic-1"):
    return dict(method=method, id=identifier, task="synthetic", plant="synthetic", parent="synthetic",
                plant_group="synthetic", condition="synthetic", seed=1, noise_seed=2, eligible=100,
                event=True, benign=False, outside_points=10, physical_return=50, return_missing=False,
                alarm_points=20, alarm_episodes=2, outside_inactive=3, joint=False, fresh=True,
                fresh_delay=.2, clear_delay=.4, returned_detected=True, overlap=True,
                already_clear_at_return=False)


class PairedTests(unittest.TestCase):
    def test_exact_identity_pairing_not_row_position(self):
        rows = [row("context_set", "b"), row("base_dual", "a"), row("context_set", "a"), row("base_dual", "b")]
        self.assertEqual([a["id"] for a, b in m.match(rows, "base_dual")], ["a", "b"])

    def test_rejects_missing_duplicate_and_metadata_difference(self):
        a, b = row("context_set"), row("base_dual")
        for rows in ([a], [a, b, copy.deepcopy(b)]):
            with self.assertRaises(ValueError):
                m.match(rows, "base_dual")
        b["eligible"] = 99
        with self.assertRaises(ValueError):
            m.match([a, b], "base_dual")

    def test_direction_and_signed_deltas(self):
        pairs = []
        for av, bv in ((1, 3), (4, 4), (7, 2)):
            a, b = row("context_set"), row("base_dual")
            a["outside_inactive"], b["outside_inactive"] = av, bv
            pairs.append((a, b))
        d = m.paired_metric(pairs, "outside_inactive", "event", "lower")
        self.assertEqual((d["wins"], d["ties"], d["losses"]), (1, 1, 1))
        self.assertEqual(d["delta"]["total"], 3)

    def test_missing_delay_not_zero_or_dropped_denominator(self):
        a, b = row("context_set"), row("base_dual")
        a["fresh_delay"] = None
        a["fresh"] = False
        d = m.paired_metric([(a, b)], "fresh_delay", "event", "lower")
        self.assertEqual((d["possible_pairs"], d["observed_pairs"], d["candidate_missing"]), (1, 0, 1))
        self.assertIsNone(d["delta"]["mean"])
        self.assertEqual(m.discordance([(a, b)], "fresh")["comparator_only"], 1)

    def test_clearance_censoring_separate_from_no_return(self):
        a, b = row("context_set"), row("context_set", "synthetic-2")
        a["clear_delay"] = None
        b.update(clear_delay=None, physical_return=None, return_missing=True, returned_detected=False)
        d = m.missingness([a, b])
        self.assertEqual(d["clearance_missing_total"], 2)
        self.assertEqual(d["clearance_censored_after_detected_return"], 1)
        self.assertEqual(d["return_missing"], 1)

    def test_joint_discordance_has_full_event_denominator(self):
        pairs = []
        for av, bv in ((True, True), (True, False), (False, True), (False, False)):
            a, b = row("context_set"), row("base_dual")
            a["joint"], b["joint"] = av, bv
            pairs.append((a, b))
        self.assertEqual(m.discordance(pairs, "joint"), dict(events=4, both=1, candidate_only=1, comparator_only=1, neither=1))

    def test_percentile_interpolation_and_finite_guard(self):
        self.assertEqual(m.quantile([0, 10], .95), 9.5)
        with self.assertRaises(ValueError):
            m.describe([float("nan")])

    def test_analysis_does_not_mutate_inputs(self):
        rows = [row(method) for method in ("context_set", *m.COMPARATORS)]
        before = copy.deepcopy(rows)
        table = m.analyze(rows)
        self.assertEqual(rows, before)
        self.assertFalse(table["inferential_tests"])
        self.assertFalse(table["new_final_evaluation"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
