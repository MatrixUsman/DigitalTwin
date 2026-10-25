"""Synthetic mathematical/causality checks only; no benchmark results."""
import unittest
import numpy as np
from kinematics20 import endpoint_operator, estimate, estimate_noise


class SyntheticKinematics(unittest.TestCase):
    def test_noiseless_constant_acceleration_endpoint_and_offset_preserved(self):
        t = np.arange(100) * .02
        q = np.column_stack([.3 + .2*t + .07*t*t, -.1 + .4*t - .03*t*t])
        v = np.column_stack([.2 + .14*t, .4 - .06*t])
        y = np.column_stack([q, v])
        for window in [5, 9]:
            for coupled in [True, False]:
                out, valid = estimate(y, [1e-4, 2e-4, 3e-4, 4e-4], window, coupled=coupled)
                np.testing.assert_allclose(out[valid], y[valid], atol=1e-12)
                shifted = y.copy(); shifted[:, 0] += 1.7
                newer, _ = estimate(shifted, [1e-4]*4, window, coupled=coupled)
                np.testing.assert_allclose(newer[valid, 0] - out[valid, 0], 1.7, atol=1e-12)

    def test_future_changes_cannot_change_past(self):
        rng = np.random.default_rng(17); y = rng.normal(size=(120,4)); changed = y.copy(); changed[80:] += 100
        a, _ = estimate(y, [1]*4, 9); b, _ = estimate(changed, [1]*4, 9)
        np.testing.assert_array_equal(a[:80], b[:80])

    def test_prefix_unready(self):
        out, valid = estimate(np.zeros((20,4)), [1]*4, 9)
        self.assertEqual(valid.sum(), 12); self.assertFalse(valid[:8].any())

    def test_velocity_information_changes_position_estimate(self):
        y = np.zeros((15,4)); y[-5:,2] = 1
        coupled, _ = estimate(y, [1]*4, 5, coupled=True)
        uncoupled, _ = estimate(y, [1]*4, 5, coupled=False)
        self.assertGreater(abs(coupled[-1,0]), .001)
        self.assertEqual(uncoupled[-1,0], 0.)

    def test_invalid_inputs_fail(self):
        for variance in [0, -1, np.nan, np.inf]:
            with self.assertRaises(ValueError): endpoint_operator(5,.02,variance,1)
        with self.assertRaises(ValueError): estimate(np.full((10,4),np.nan),[1]*4,5)
        with self.assertRaises(ValueError): estimate_noise([np.zeros((20,4))])

    def test_training_variances_are_not_mutated_by_inference(self):
        rng = np.random.default_rng(42); var = estimate_noise([rng.normal(size=(1000,4))]); before = var.copy()
        estimate(rng.normal(size=(20,4))*1000, var, 9)
        np.testing.assert_array_equal(var, before)


if __name__ == '__main__': unittest.main()
