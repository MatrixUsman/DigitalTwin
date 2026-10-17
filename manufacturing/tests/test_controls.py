"""SYNTHETIC model checks; no CASPER files, benchmark observations or results."""
from dataclasses import FrozenInstanceError
from decimal import Decimal
import json
import math
import unittest

from mfg_twin.controls import (ARAccumulator, ARDetector, ARReference, ControlError,
    Standardizer12, TemplateAccumulator, TemplateDetector, TemplateReference,
    estimate_period, fit_standardizer, fit_template_seed)
from mfg_twin.data import Observation


def observation(value, *, dt=Decimal('.0625'), multiplier=True):
    values = tuple(value * (i + 1) if multiplier else value for i in range(12))
    return Observation(values[:6], values[6:], dt)


def identity():
    return Standardizer12(2, (0.,) * 12, (1.,) * 12, (1.,) * 12)


def periodic(count=256, *, start=0, reset=True):
    return [observation(((i + start) % 16) - 8,
                        dt=None if i == 0 and reset else Decimal('.0625'))
            for i in range(count)]


def template(initialization=16):
    return fit_template_seed(periodic(), identity(), 1., 16, initialization=initialization)


def ar_reference(order=1, ridge=.1):
    accumulator = ARAccumulator(identity(), order)
    for i in range(30):
        accumulator.observe(observation(i, dt=None if i == 0 else Decimal('.0625')),
                            eligible=i >= order)
    return accumulator.finish(ridge)


class StandardizerTests(unittest.TestCase):
    def test_synthetic_population_reference(self):
        reference = fit_standardizer(observation(v) for v in [1., 2., 3., 4.])
        self.assertEqual(reference.n, 4)
        self.assertEqual(reference.mean, tuple(2.5 * (j + 1) for j in range(12)))
        self.assertEqual(reference.variance, tuple(1.25 * (j + 1) ** 2 for j in range(12)))
        for z in reference.transform(observation(5.)):
            self.assertAlmostEqual(z, 2.5 / math.sqrt(1.25))

    def test_synthetic_immutable_serialization(self):
        fitted = fit_standardizer(observation(v) for v in [1., 2., 3.])
        export = fitted.to_dict()
        restored = Standardizer12.from_dict(json.loads(json.dumps(export, allow_nan=False)))
        self.assertEqual(fitted, restored)
        export['mean'][0] = 400
        self.assertNotEqual(fitted.mean[0], 400)
        with self.assertRaises(FrozenInstanceError):
            fitted.n = 400
        with self.assertRaises(TypeError):
            fitted.mean[0] = 400

    def test_synthetic_empty_singleton_constant_fail(self):
        for rows in [[], [observation(1)], [observation(1)] * 2]:
            with self.subTest(n=len(rows)), self.assertRaises(ControlError):
                fit_standardizer(rows)

    def test_synthetic_one_constant_channel_fails_without_dropping_channel(self):
        rows = []
        for n in [1, 2, 3]:
            rows.append(Observation((0., n, n, n, n, n), (n,) * 6, Decimal('.05')))
        with self.assertRaises(ControlError):
            fit_standardizer(rows)

    def test_synthetic_invalid_export_and_nonfinite_fit(self):
        for patch in [{'n': True}, {'sigma': [0.] * 12}, {'sigma': [2.] * 12},
                      {'variance': [math.inf] * 12}, {'mean': [0.] * 11}]:
            with self.subTest(patch=patch), self.assertRaises(ControlError):
                Standardizer12.from_dict({**identity().to_dict(), **patch})
        with self.assertRaises(ControlError):
            fit_standardizer([observation(1e308, multiplier=False),
                              observation(-1e308, multiplier=False)])

    def test_synthetic_feature_only_interface(self):
        with self.assertRaises(ControlError):
            fit_standardizer([{'label': 0, 'row': 1}])


class ARTests(unittest.TestCase):
    def test_synthetic_independent_mean_normalized_ridge_solution(self):
        accumulator = ARAccumulator(identity(), 1)
        for i in range(4):
            accumulator.observe(observation(i, dt=None if i == 0 else Decimal('.05'),
                                            multiplier=False), i > 0)
        reference = accumulator.finish(.1)
        self.assertEqual(reference.n, 3)
        for intercept, slope in reference.coefficients:
            self.assertAlmostEqual(slope, 20 / 23, places=12)
            self.assertAlmostEqual(intercept, 26 / 23, places=12)

    def test_synthetic_normalized_ridge_invariant_to_replicated_targets(self):
        accumulators = [ARAccumulator(identity(), 1) for _ in range(2)]
        for index, accumulator in enumerate(accumulators):
            for _ in range(index + 1):
                for i in range(5):
                    accumulator.observe(observation(i, dt=None if i == 0 else Decimal('.05')),
                                        i > 0)
        for a, b in zip(accumulators[0].finish(.1).coefficients,
                        accumulators[1].finish(.1).coefficients):
            for x, y in zip(a, b):
                self.assertAlmostEqual(x, y, places=12)

    def test_synthetic_order_four_fit_and_two_ridges_share_statistics(self):
        reference = ar_reference(4)
        self.assertEqual(reference.n, 26)
        self.assertEqual(len(reference.coefficients), 12)
        self.assertTrue(all(len(row) == 5 for row in reference.coefficients))
        accumulator = ARAccumulator(identity(), 4)
        for i in range(30):
            accumulator.observe(observation(i, dt=None if i == 0 else Decimal('.05')), i >= 4)
        before = json.dumps(accumulator.gram)
        low, high = accumulator.finish(.001), accumulator.finish(.1)
        self.assertEqual(json.dumps(accumulator.gram), before)
        self.assertNotEqual(low.coefficients, high.coefficients)

    def test_synthetic_prediction_precedes_current_observation(self):
        detector = ARDetector(ar_reference())
        detector.update(observation(2., dt=None))
        self.assertEqual(detector.predict(observation(3.)), detector.predict(observation(300.)))
        prediction = detector.predict(observation(3.))
        expected = sum((v - p) ** 2 for v, p in zip(identity().transform(observation(3.)), prediction)) / 12
        self.assertAlmostEqual(detector.score(observation(3.)), expected)

    def test_synthetic_repeated_scores_do_not_update_history(self):
        detector = ARDetector(ar_reference())
        detector.update(observation(2., dt=None))
        before = tuple(detector.history)
        self.assertEqual(detector.score(observation(3.)), detector.score(observation(3.)))
        self.assertEqual(tuple(detector.history), before)

    def test_synthetic_nonfinite_residual_fails_explicitly(self):
        detector = ARDetector(ar_reference())
        detector.update(observation(2., dt=None))
        with self.assertRaises(ControlError):
            detector.score(observation(1e308, multiplier=False))

    def test_synthetic_initialization_and_gap_reset(self):
        detector = ARDetector(ar_reference(4))
        for i in range(4):
            current = observation(i, dt=None if i == 0 else Decimal('.05'))
            self.assertIsNone(detector.score(current))
            detector.update(current)
        self.assertIsNotNone(detector.score(observation(4)))
        self.assertIsNone(detector.score(observation(9, dt=None)))
        detector.update(observation(9, dt=None))
        self.assertIsNone(detector.score(observation(10)))

    def test_synthetic_eligible_loss_requires_complete_history(self):
        accumulator = ARAccumulator(identity(), 4)
        with self.assertRaises(ControlError):
            accumulator.observe(observation(3., dt=None), True)

    def test_synthetic_warmup_not_loss_targets(self):
        accumulator = ARAccumulator(identity(), 1)
        for i in range(20):
            accumulator.observe(observation(i, dt=None if i == 0 else Decimal('.05')), i >= 10)
        self.assertEqual(accumulator.finish(.1).n, 10)

    def test_synthetic_reference_roundtrip_development_cannot_refit(self):
        reference = ar_reference(4)
        encoded = json.dumps(reference.to_dict(), allow_nan=False)
        restored = ARReference.from_dict(json.loads(encoded))
        self.assertEqual(reference, restored)
        detector = ARDetector(restored)
        for i in range(20):
            current = observation(i * 100, dt=None if i == 0 else Decimal('.05'))
            detector.score(current)
            detector.update(current)
        self.assertEqual(json.dumps(reference.to_dict(), allow_nan=False), encoded)
        self.assertEqual(json.dumps(detector.reference.to_dict(), allow_nan=False), encoded)
        with self.assertRaises(FrozenInstanceError):
            reference.n = 100

    def test_synthetic_bad_ridge_empty_fit_and_nonfinite_reference(self):
        accumulator = ARAccumulator(identity(), 1)
        with self.assertRaises(ControlError):
            accumulator.finish(.1)
        for ridge in [0, -1, math.inf, True]:
            with self.subTest(ridge=ridge), self.assertRaises(ControlError):
                ar_reference(1, ridge)
        payload = ar_reference().to_dict()
        payload['coefficients'][0][0] = math.nan
        with self.assertRaises(ControlError):
            ARReference.from_dict(payload)

    def test_synthetic_invalid_time_fails_closed(self):
        detector = ARDetector(ar_reference())
        for dt in [Decimal('.1'), Decimal('1e-999'), Decimal('1e999')]:
            with self.subTest(dt=dt), self.assertRaises(ControlError):
                detector.update(observation(2, dt=dt))

    def test_synthetic_future_suffix_does_not_change_prefix_scores(self):
        reference = ar_reference()
        prefix = [observation(i, dt=None if i == 0 else Decimal('.05')) for i in range(10)]
        def replay(rows):
            detector, scores = ARDetector(reference), []
            for row in rows:
                scores.append(detector.score(row))
                detector.update(row)
            return scores
        self.assertEqual(replay(prefix), replay(prefix + [observation(1000)])[:10])


class PeriodTests(unittest.TestCase):
    def test_synthetic_true_period_and_tie_rule(self):
        estimate = estimate_period(periodic(), identity(), stride=2, min_lag=2, max_lag=12)
        self.assertEqual(estimate.lag, 8)
        self.assertEqual(estimate.period_seconds, 1.)
        self.assertEqual(estimate.objective, 0.)
        self.assertEqual(estimate.sampled_observations, 128)
        self.assertEqual(estimate.prefix_observations, 256)
        self.assertEqual(estimate.sampled_elapsed_seconds, 15.875)
        self.assertEqual([lag for lag, _ in estimate.lag_objectives], list(range(1, 14)))
        self.assertTrue(json.dumps(estimate.to_dict(), allow_nan=False))

    def test_synthetic_period_uses_actual_relative_seconds(self):
        rows = [observation(i % 16, dt=None if i == 0 else Decimal('.05')) for i in range(256)]
        estimate = estimate_period(rows, identity(), stride=2, min_lag=2, max_lag=12)
        self.assertAlmostEqual(estimate.period_seconds, .8, places=12)

    def test_synthetic_time_jitter_uses_mean_native_lag(self):
        rows, times, elapsed = [], [], 0.
        for i in range(256):
            dt = None if i == 0 else Decimal('.06') if i % 3 else Decimal('.07')
            if dt is not None:
                elapsed += float(dt)
            times.append(elapsed)
            rows.append(observation(i % 16, dt=dt))
        estimate = estimate_period(rows, identity(), stride=2, min_lag=2, max_lag=12)
        sampled_times = times[::2]
        expected = math.fsum(sampled_times[i] - sampled_times[i - 8]
                             for i in range(8, len(sampled_times))) / (len(sampled_times) - 8)
        self.assertEqual(estimate.period_seconds, expected)

    def test_synthetic_period_prefix_stops_at_reset(self):
        prefix = periodic()
        a = estimate_period(prefix, identity(), stride=2, min_lag=2, max_lag=12)
        b = estimate_period(prefix + periodic(start=7), identity(), stride=2, min_lag=2, max_lag=12)
        self.assertEqual(a, b)

    def test_synthetic_period_does_not_read_beyond_cap(self):
        def capped():
            yield from periodic()
            raise AssertionError('Read beyond declared synthetic prefix')
        estimate = estimate_period(capped(), identity(), stride=2, min_lag=2,
                                   max_lag=12, max_observations=256)
        self.assertEqual(estimate.sampled_observations, 128)

    def test_synthetic_short_or_aperiodic_prefix_fails(self):
        with self.assertRaises(ControlError):
            estimate_period(periodic(40), identity(), stride=2, min_lag=2, max_lag=12)
        with self.assertRaises(ControlError):
            estimate_period((observation(i) for i in range(256)), identity(),
                            stride=2, min_lag=2, max_lag=12)


class TemplateTests(unittest.TestCase):
    def test_synthetic_exact_template_bins_and_counts(self):
        reference = template()
        self.assertEqual(reference.n, 256)
        self.assertEqual(reference.counts, (16,) * 16)
        for phase in range(16):
            self.assertEqual(reference.means[phase], tuple((phase - 8) * (j + 1) for j in range(12)))

    def test_synthetic_warmup_phase_aligns_shift_without_current_target(self):
        reference = template()
        detector = TemplateDetector(reference)
        for row in periodic(16, start=5):
            self.assertIsNone(detector.score(row))
            detector.update(row)
        self.assertEqual(detector.offset, 5)
        current = periodic(1, start=5, reset=False)[0]
        self.assertEqual(detector.score(current), 0.)
        self.assertEqual(detector.predict(current), detector.predict(observation(1000.)))

    def test_synthetic_clock_wrap_and_elapsed_jitter(self):
        detector = TemplateDetector(template())
        for row in periodic(16):
            detector.update(row)
        self.assertEqual(detector.phase_for(observation(-8)), 0)
        detector.update(observation(-8))
        self.assertEqual(detector.phase_for(observation(-7, dt=Decimal('.03125'))), 0)
        self.assertEqual(detector.phase_for(observation(-7, dt=Decimal('.0625'))), 1)

    def test_synthetic_phase_freezes_after_initialization(self):
        detector = TemplateDetector(template())
        for row in periodic(16, start=5):
            detector.update(row)
        fitted_offset, losses = detector.offset, list(detector.losses)
        for row in periodic(20, start=10, reset=False):
            detector.score(row)
            detector.update(row)
        self.assertEqual(detector.offset, fitted_offset)
        self.assertEqual(detector.losses, losses)

    def test_synthetic_first_common_eligible_endpoint_is_scored(self):
        detector = TemplateDetector(template(initialization=1528))
        rows = periodic(1529, start=5)
        for row in rows[:1528]:
            self.assertIsNone(detector.score(row))
            detector.update(row)
        self.assertEqual(detector.score(rows[1528]), 0.)

    def test_synthetic_repeated_scores_do_not_update_clock_or_phase(self):
        detector = TemplateDetector(template())
        for row in periodic(16, start=5):
            detector.update(row)
        state = (detector.elapsed, detector.seen, detector.offset, list(detector.losses))
        current = periodic(1, start=5, reset=False)[0]
        self.assertEqual(detector.score(current), detector.score(current))
        self.assertEqual((detector.elapsed, detector.seen, detector.offset, detector.losses), state)

    def test_synthetic_gap_requires_new_warmup_and_offset(self):
        detector = TemplateDetector(template())
        for row in periodic(16, start=5):
            detector.update(row)
        self.assertIsNone(detector.score(observation(3., dt=None)))
        for row in periodic(16, start=9):
            self.assertIsNone(detector.score(row))
            detector.update(row)
        self.assertEqual(detector.offset, 9)

    def test_synthetic_full_training_aligns_independent_segment_phases(self):
        accumulator = TemplateAccumulator(template())
        for start in [0, 5]:
            for i, row in enumerate(periodic(64, start=start)):
                accumulator.observe(row, eligible=i >= 16)
        fitted = accumulator.finish()
        self.assertEqual(fitted.n, 96)
        self.assertEqual(fitted.counts, (6,) * 16)
        self.assertEqual(fitted.means, template().means)

    def test_synthetic_accumulator_rejects_uninitialized_eligible_target(self):
        accumulator = TemplateAccumulator(template())
        with self.assertRaises(ControlError):
            accumulator.observe(observation(1., dt=None), eligible=True)

    def test_synthetic_unseen_bins_and_short_warmup_fail(self):
        with self.assertRaises(ControlError):
            fit_template_seed(periodic(4), identity(), 1., 16)
        accumulator = TemplateAccumulator(template())
        for row in periodic(8):
            accumulator.observe(row, False)
        with self.assertRaises(ControlError):
            accumulator.finish()

    def test_synthetic_seed_stops_at_reset(self):
        a = fit_template_seed(periodic(), identity(), 1., 16)
        b = fit_template_seed(periodic() + periodic(start=7), identity(), 1., 16)
        self.assertEqual(a, b)

    def test_synthetic_reference_roundtrip_and_dev_not_fitted(self):
        reference = template()
        encoded = json.dumps(reference.to_dict(), allow_nan=False)
        restored = TemplateReference.from_dict(json.loads(encoded))
        self.assertEqual(reference, restored)
        detector = TemplateDetector(restored)
        for row in periodic(64, start=5):
            detector.score(row)
            detector.update(row)
        self.assertEqual(json.dumps(detector.reference.to_dict(), allow_nan=False), encoded)
        with self.assertRaises(FrozenInstanceError):
            reference.n = 100
        exported = reference.to_dict()
        exported['means'][0][0] = 999
        self.assertNotEqual(reference.means[0][0], 999)

    def test_synthetic_invalid_saved_template_fails(self):
        for patch in [{'period_seconds': 0}, {'bins': True}, {'n': 3},
                      {'counts': [0] * 16}, {'initialization': 0}]:
            with self.subTest(patch=patch), self.assertRaises(ControlError):
                TemplateReference.from_dict({**template().to_dict(), **patch})

    def test_synthetic_future_suffix_invariance(self):
        def replay(rows):
            detector, scores = TemplateDetector(template()), []
            for row in rows:
                scores.append(detector.score(row))
                detector.update(row)
            return scores
        prefix = periodic(40)
        self.assertEqual(replay(prefix), replay(prefix + [observation(1000.)])[:40])


if __name__ == '__main__':
    unittest.main()
