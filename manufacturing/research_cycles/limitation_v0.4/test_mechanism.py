"""Explicitly synthetic fixtures; no benchmark observations or weights."""
import json
from pathlib import Path
import unittest
import numpy as np
from mechanism import (cases, perturb, rolling_mean, accumulate, score_streams,
                       calibrate, event_metrics, normal_metrics, error_summary)


class SyntheticChecks(unittest.TestCase):
    def setUp(self):
        self.x = np.arange(1800, dtype=np.float32).reshape(200, 9) / 10
        self.config = json.loads((Path(__file__).parent / "config.json").read_text())

    def test_roster_complete_and_within_support(self):
        roster = cases(self.config)
        self.assertEqual(len(roster), 189); self.assertEqual(len({x['id'] for x in roster}), 189)
        for c in roster:
            self.assertGreaterEqual(c['onset'], 8192)
            self.assertLess(c['onset'] + c['duration'] + 512, 16384)

    def test_interval_support_and_no_mutation(self):
        before = self.x.copy()
        for family, magnitude in [('hold', .5), ('slow', .5), ('bias', 1)]:
            y = perturb(self.x, 50, 45, family, magnitude)
            np.testing.assert_array_equal(self.x, before)
            np.testing.assert_array_equal(y[:50], before[:50]); np.testing.assert_array_equal(y[95:], before[95:])

    def test_causality_under_future_changes(self):
        future = self.x.copy(); future[70:] += 100
        for family, magnitude in [('hold', .5), ('slow', .5), ('bias', 1)]:
            np.testing.assert_array_equal(perturb(self.x, 50, 45, family, magnitude)[:70],
                                          perturb(future, 50, 45, family, magnitude)[:70])

    def test_hold_analytic_persistence(self):
        y = perturb(self.x, 50, 45, 'hold', 1)
        np.testing.assert_array_equal(y[50:95], np.repeat(self.x[49:50], 45, axis=0))
        self.assertEqual(float(np.square(y[51:95] - y[50:94]).sum()), 0.)

    def test_identity_interventions(self):
        for family, magnitude in [('hold', 0), ('slow', 1), ('bias', 0)]:
            np.testing.assert_array_equal(perturb(self.x, 50, 45, family, magnitude), self.x)

    def test_slow_interpolation(self):
        y = perturb(self.x, 50, 10, 'slow', .5)
        np.testing.assert_allclose(y[50], (self.x[49] + self.x[50]) / 2)
        np.testing.assert_array_equal(y[51], self.x[50])

    def test_bias_modality(self):
        y = perturb(self.x, 50, 45, 'bias', 2)
        cols = [0, 1, 2, 4, 5, 6, 7, 8]
        np.testing.assert_array_equal(y[:, cols], self.x[:, cols])
        # Subtracting float32 values near 100 loses a few ulps; require the
        # intended offset within one float32 spacing at the fixture maximum.
        np.testing.assert_allclose(y[50:95, 3] - self.x[50:95, 3], 2,
                                   rtol=0, atol=float(np.spacing(self.x.max())))

    def test_invalid_perturbations(self):
        for args in [(0, 2, 'hold', 1), (199, 2, 'hold', 1), (2, 3, 'slow', 2), (2, 3, 'bad', 1)]:
            with self.assertRaises(ValueError): perturb(self.x, *args)

    def test_prediction_influence_support(self):
        y = perturb(self.x, 50, 20, 'bias', 1)
        p = np.array([self.x[t-45:t].mean(0) for t in range(45, 200)])
        q = np.array([y[t-45:t].mean(0) for t in range(45, 200)])
        target = np.arange(45, 200)
        outside = (target < 50) | (target >= 115)
        np.testing.assert_array_equal(p[outside], q[outside])

    def test_rolling_matches_direct_mean(self):
        x = np.random.default_rng(17).uniform(size=1000)
        for width in [1, 45, 450]:
            np.testing.assert_allclose(rolling_mean(x, width), [np.mean(x[max(0,i-width+1):i+1]) for i in range(len(x))], atol=1e-13)

    def test_cusum_matches_recursive_definition(self):
        x = np.random.default_rng(42).exponential(size=16384)
        actual = accumulate(x, 1, 1.5, 25); ref=[]; s=0.
        for value in x:
            s=max(0., s+min(value,25)-1.5); ref.append(s)
        np.testing.assert_allclose(actual, ref, atol=2e-11, rtol=1e-10)

    def test_accumulator_memory_decay_and_cap(self):
        x = np.array([1000., 0, 0, 0])
        np.testing.assert_array_equal(accumulate(x, 1, 1.5, 25), [23.5,22.,20.5,19.])

    def test_scores_prefix_causality(self):
        x = np.random.default_rng(2026).uniform(size=1000); y=x.copy();y[600:]=100
        np.testing.assert_array_equal(score_streams(x, 1, self.config)[:600], score_streams(y, 1, self.config)[:600])

    def test_nonfinite_scores_rejected(self):
        for x in [[1, float('nan')], [1, -1]]:
            with self.assertRaises(ValueError): score_streams(x, 1, self.config)
        with self.assertRaises(ValueError): accumulate([1], 0, 1.5, 25)

    def test_rank_and_strict_ties(self):
        x=np.arange(4096.)[:,None]; t, rank=calibrate(x,0,4096,.99)
        self.assertEqual(rank,4056); self.assertEqual(t[0],4055)
        self.assertEqual(int((x[:,0]>t[0]).sum()),40)
        t,_=calibrate(np.ones((4096,4)),0,4096,.99)
        self.assertEqual(int((np.ones((4096,4))>t).sum()),0)

    def test_calibration_future_independence(self):
        x=np.ones((12000,4));a,_=calibrate(x,4096,8192,.99);x[8192:]=1e8
        b,_=calibrate(x,4096,8192,.99);np.testing.assert_array_equal(a,b)

    def test_existing_alarm_not_fresh(self):
        x=np.zeros(100,dtype=bool);x[20:60]=True
        m=event_metrics(x,30,20,0,100,40)
        self.assertTrue(m['overlap_hit']);self.assertFalse(m['fresh_hit'])
        self.assertIsNone(m['fresh_delay']);self.assertEqual(m['overlap_delay'],0)
        self.assertEqual(m['first_clear_delay'],10)

    def test_misses_retained(self):
        m=event_metrics(np.zeros(100,dtype=bool),30,20,0,100,40)
        self.assertFalse(m['overlap_hit']);self.assertIsNone(m['overlap_delay'])
        self.assertEqual(m['fn'],20);self.assertEqual(m['f1'],0)

    def test_fresh_event_and_point_counts(self):
        x=np.zeros(100,dtype=bool);x[32:42]=True;x[90:]=True
        m=event_metrics(x,30,20,0,100,40)
        self.assertEqual((m['tp'],m['fp'],m['fn']),(10,10,10))
        self.assertEqual(m['fresh_delay'],2);self.assertEqual(m['f1'],.5)

    def test_post_clear_censoring(self):
        m=event_metrics(np.ones(100,dtype=bool),30,20,0,100,40)
        self.assertTrue(m['first_clear_censored']);self.assertIsNone(m['first_clear_delay'])

    def test_normal_boundary_episode(self):
        x=np.zeros(20,dtype=bool);x[5:15]=True
        m=normal_metrics(x,10,20)
        self.assertEqual(m['alarm_points'],5);self.assertEqual(m['episodes'],0)

    def test_oracle_ratio_and_short_overlap(self):
        m=error_summary(np.ones(450),np.ones(450)*2,450)
        self.assertEqual(m['late_to_oracle'],.5);self.assertFalse(m['early_late_overlap'])
        self.assertIsNone(error_summary(np.zeros(5),np.zeros(5),5)['late_to_oracle'])


if __name__ == '__main__': unittest.main()
