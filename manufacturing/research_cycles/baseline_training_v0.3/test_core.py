import unittest
import numpy as np
from core import Scaler, eligible_endpoints, prepare, batches, score_predictions, EarlyStop, fit_ar, predict_ar


class SplitTests(unittest.TestCase):
    def fixture(self):
        return np.random.default_rng(2026).normal(size=(500, 9)), np.arange(500, dtype=np.int64) * 100

    def test_development_cannot_change_training(self):
        x, t = self.fixture()
        first = prepare(x, t, 350, 45)
        x[350:] = x[350:] * 10 + 200
        t[350:] *= 3
        second = prepare(x, t, 350, 45)
        for name in ["training", "training_indices"]:
            np.testing.assert_array_equal(first[name], second[name])
        np.testing.assert_array_equal(first["scaler"].mean, second["scaler"].mean)
        np.testing.assert_array_equal(first["scaler"].scale, second["scaler"].scale)
        self.assertEqual(first["maximum_gap"], second["maximum_gap"])

    def test_split_support_and_future_targets(self):
        x, t = self.fixture()
        result = prepare(x, t, 350, 45)
        batch, target = next(batches(result["development"], result["development_indices"], 45, 64))
        np.testing.assert_array_equal(batch[0], result["scaler"].transform(x[350:395]))
        np.testing.assert_array_equal(target[0], result["scaler"].transform(x[395:396])[0])
        self.assertEqual(len(result["development_indices"]), 105)

    def test_gap_excludes_all_crossing_windows(self):
        times = np.arange(120, dtype=np.int64) * 100
        times[60:] += 10000
        endpoints, coverage = eligible_endpoints(times, 10, 500)
        self.assertEqual(coverage["excluded_local_endpoints"], list(range(60, 70)))
        self.assertIn(59, endpoints)
        self.assertIn(70, endpoints)

    def test_duplicate_and_backward_time_are_boundaries(self):
        for value in [4900, 4800]:
            times = np.arange(100, dtype=np.int64) * 100
            times[50] = value
            endpoints, coverage = eligible_endpoints(times, 3, 500)
            self.assertEqual(coverage["nonpositive_transitions"], 1)
            self.assertFalse(set([50, 51, 52]) & set(endpoints))

    def test_gap_at_split_does_not_cross_populations(self):
        x, t = self.fixture()
        t[350:] += 100000
        result = prepare(x, t, 350, 45)
        self.assertEqual(result["development_coverage"]["coverage"], 1)

    def test_low_coverage_fails(self):
        x, t = self.fixture()
        t[400:] += 10000
        with self.assertRaises(ValueError):
            prepare(x, t, 350, 45)

    def test_nonfinite_and_constant_training_fail(self):
        x, t = self.fixture()
        for value in [np.nan, np.inf]:
            bad = x.copy(); bad[20, 0] = value
            with self.assertRaises(ValueError): prepare(bad, t, 350, 45)
        x[:350, 0] = 1
        with self.assertRaises(ValueError): prepare(x, t, 350, 45)

    def test_scaler_is_immutable(self):
        x, _ = self.fixture(); scaler = Scaler.fit(x)
        with self.assertRaises(ValueError): scaler.mean[0] = 1
        with self.assertRaises(ValueError): scaler.scale[0] = 1

    def test_fractional_timestamps_fail(self):
        x, t = self.fixture()
        with self.assertRaises(ValueError): prepare(x, t.astype(float), 350, 45)


class ArithmeticTests(unittest.TestCase):
    def test_future_changes_leave_earlier_forecast_inputs_unchanged(self):
        z = np.arange(100 * 9, dtype=np.float32).reshape(100, 9)
        first = next(batches(z, np.arange(45, 70), 45, 25))[0].copy()
        z[70:] += 999
        np.testing.assert_array_equal(first, next(batches(z, np.arange(45, 70), 45, 25))[0])

    def test_batching_preserves_order_and_last_short_batch(self):
        z = np.arange(100, dtype=float)[:, None]
        result = list(batches(z, np.arange(10, 100), 10, 32))
        self.assertEqual([len(y) for _, y in result], [32, 32, 26])
        np.testing.assert_array_equal(np.concatenate([y[:, 0] for _, y in result]), np.arange(10, 100))

    def test_invalid_batch_coordinates_fail(self):
        z = np.zeros((20, 9))
        for endpoints in [np.array([-1, 3]), np.array([3, 3]), np.array([3, 2]), np.array([3, 20]), np.array([3.5])]:
            with self.assertRaises(ValueError): list(batches(z, endpoints, 3, 8))

    def test_score_has_known_units_and_denominator(self):
        p, y, scale = np.array([[3., 4.], [0., 0.]]), np.zeros((2, 2)), np.array([2., 1.])
        score, native, result = score_predictions(p, y, scale)
        np.testing.assert_allclose(score, [np.sqrt(12.5), 0])
        np.testing.assert_allclose(native, [np.sqrt(26), 0])
        self.assertEqual(result["standardized_mse"], 6.25)
        self.assertEqual(result["native_mse"], 13.)

    def test_shape_and_nonfinite_scores_fail(self):
        for p in [np.zeros((3, 2)), np.full((2, 2), np.nan)]:
            with self.assertRaises(ValueError): score_predictions(p, np.zeros((2, 2)), np.ones(2))

    def test_exact_ar_process_recovers_coefficient_and_intercept(self):
        # Independent analytic recurrence: y[t] = 0.8*y[t-1] + 0.2.
        z = np.empty((100, 1)); z[0, 0] = 10.
        for t in range(1, 100): z[t, 0] = 0.8 * z[t - 1, 0] + 0.2
        coefficients = fit_ar(z, np.arange(1, 70), order=1, ridge=0)
        np.testing.assert_allclose(coefficients[:, 0], [0.8, 0.2], atol=1e-12)
        prediction = predict_ar(z, np.arange(70, 100), coefficients, order=1)
        np.testing.assert_allclose(prediction, z[70:], atol=1e-12)

    def test_ar_coefficients_unchanged_by_development(self):
        z = np.random.default_rng(17).normal(size=(100, 2))
        a = fit_ar(z[:70], np.arange(4, 70), order=4)
        z[70:] = 1e6
        np.testing.assert_array_equal(a, fit_ar(z[:70], np.arange(4, 70), order=4))


class SelectionTests(unittest.TestCase):
    def test_patience_and_ties_keep_earliest_checkpoint(self):
        rule = EarlyStop(3, 1e-6)
        self.assertEqual(rule.observe(1, 1), (True, False))
        self.assertEqual(rule.observe(2, 1), (False, False))
        self.assertEqual(rule.observe(3, 1 - 0.5e-6), (False, False))
        self.assertEqual(rule.observe(4, 2), (False, True))
        self.assertEqual(rule.best_epoch, 1)

    def test_improvement_resets_patience(self):
        rule = EarlyStop(2, 1e-6)
        for epoch, loss in enumerate([1., 2., 0.5, 0.6], 1):
            _, stop = rule.observe(epoch, loss)
            self.assertFalse(stop)
        self.assertEqual(rule.best_epoch, 3)

    def test_invalid_epochs_and_losses_fail(self):
        for epoch, loss in [(0, 1.), (2, 1.), (1, np.nan), (1, -1.)]:
            with self.assertRaises(ValueError): EarlyStop(5, 1e-6).observe(epoch, loss)


if __name__ == "__main__": unittest.main()
