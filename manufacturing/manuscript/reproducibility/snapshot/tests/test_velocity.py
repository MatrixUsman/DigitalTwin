"""SYNTHETIC velocity-control checks; no benchmark files or training runs."""

from dataclasses import FrozenInstanceError
from decimal import Decimal, Inexact, localcontext
import json
import math
import unittest

from mfg_twin.data import Observation
from mfg_twin.velocity import VelocityDetector, VelocityError, VelocityReference, fit_velocity


def synthetic_observation(qdot, *, q=None, dt=Decimal("0.05")):
    return Observation(q=(0.0,) * 6 if q is None else tuple(q), qdot=tuple(qdot), dt=dt)


def synthetic_varied_rows():
    return [synthetic_observation(tuple((channel + 1) * value for channel in range(6)))
            for value in (1.0, 2.0, 3.0, 4.0)]


class VelocityFitTests(unittest.TestCase):
    def test_synthetic_hand_calculated_population_reference(self):
        reference = fit_velocity(synthetic_varied_rows())
        self.assertEqual(reference.n, 4)
        self.assertEqual(reference.mean, tuple(2.5 * (j + 1) for j in range(6)))
        self.assertEqual(reference.variance, tuple(1.25 * (j + 1) ** 2 for j in range(6)))
        self.assertEqual(reference.sigma, tuple(math.sqrt(v) for v in reference.variance))

    def test_synthetic_fit_consumes_iterable_once_without_retaining_observations(self):
        class SinglePass:
            def __init__(self):
                self.calls = 0
                self.yielded = 0

            def __iter__(self):
                self.calls += 1
                if self.calls > 1:
                    raise AssertionError("Synthetic source iterated more than once")
                for observation in synthetic_varied_rows():
                    self.yielded += 1
                    yield observation

        source = SinglePass()
        reference = fit_velocity(source)
        self.assertEqual((source.calls, source.yielded, reference.n), (1, 4, 4))
        self.assertEqual(set(reference.to_dict()), {"n", "mean", "variance", "sigma"})

    def test_synthetic_population_not_sample_variance(self):
        reference = fit_velocity([synthetic_observation([-1] * 6), synthetic_observation([1] * 6)])
        self.assertEqual(reference.mean, (0,) * 6)
        self.assertEqual(reference.variance, (1,) * 6)
        self.assertEqual(reference.sigma, (1,) * 6)

    def test_synthetic_large_offset_retains_small_population_variance(self):
        rows = [synthetic_observation([1e12 + offset] * 6) for offset in (-3, -1, 1, 3)]
        reference = fit_velocity(rows)
        self.assertEqual(reference.mean, (1e12,) * 6)
        self.assertEqual(reference.variance, (5.0,) * 6)

    def test_synthetic_empty_and_singleton_fail(self):
        with self.assertRaises(VelocityError) as caught:
            fit_velocity([])
        self.assertEqual(caught.exception.reason, "empty_fit")
        with self.assertRaises(VelocityError) as caught:
            fit_velocity([synthetic_observation([1] * 6)])
        self.assertEqual(caught.exception.reason, "nonpositive_variance")
        self.assertEqual((caught.exception.channel, caught.exception.sample_count), (0, 1))

    def test_synthetic_constant_channel_is_not_dropped(self):
        rows = [synthetic_observation([x, x, x, 7, x, x]) for x in (1, 2, 3)]
        with self.assertRaises(VelocityError) as caught:
            fit_velocity(rows)
        self.assertEqual(caught.exception.reason, "nonpositive_variance")
        self.assertEqual((caught.exception.channel, caught.exception.sample_count), (3, 3))

    def test_synthetic_welford_delta_overflow_fails_at_channel(self):
        with self.assertRaises(VelocityError) as caught:
            fit_velocity([synthetic_observation([1e308] * 6), synthetic_observation([-1e308] * 6)])
        self.assertEqual(caught.exception.reason, "nonfinite_welford_delta")
        self.assertEqual((caught.exception.channel, caught.exception.sample_count), (0, 2))

    def test_synthetic_welford_product_overflow_fails(self):
        with self.assertRaises(VelocityError) as caught:
            fit_velocity([synthetic_observation([1e200] * 6), synthetic_observation([-1e200] * 6)])
        self.assertEqual(caught.exception.reason, "nonfinite_welford_increment")
        self.assertEqual(caught.exception.sample_count, 2)

    def test_synthetic_welford_accumulation_overflow_fails(self):
        rows = [synthetic_observation([value] * 6) for value in (8e153, -8e153, 8e153, -8e153)]
        with self.assertRaises(VelocityError) as caught:
            fit_velocity(rows)
        self.assertEqual(caught.exception.reason, "nonfinite_welford_m2")
        self.assertEqual(caught.exception.sample_count, 4)

    def test_synthetic_variance_underflow_does_not_add_epsilon(self):
        with self.assertRaises(VelocityError) as caught:
            fit_velocity([synthetic_observation([1e-200] * 6), synthetic_observation([-1e-200] * 6)])
        self.assertEqual(caught.exception.reason, "nonpositive_variance")

    def test_synthetic_positions_and_elapsed_time_cannot_change_fit(self):
        original = synthetic_varied_rows()
        changed = [synthetic_observation(o.qdot, q=[123.0 + i] * 6,
                                         dt=None if i == 0 else Decimal("1000"))
                   for i, o in enumerate(original)]
        self.assertEqual(fit_velocity(original), fit_velocity(changed))

    def test_synthetic_feature_only_input_required(self):
        for value in ([1] * 6, {"qdot": [1] * 6}, None):
            with self.subTest(value_type=type(value).__name__), self.assertRaises(VelocityError):
                fit_velocity([value])

    def test_synthetic_forged_nonfinite_observation_rechecked(self):
        # Observation normally rejects invalid input at construction; this fixture
        # deliberately bypasses that protection to exercise the control boundary.
        for invalid in (math.nan, math.inf, True):
            observation = synthetic_observation([0] * 6)
            object.__setattr__(observation, "qdot", (0, 0, invalid, 0, 0, 0))
            with self.subTest(invalid=invalid), self.assertRaises(VelocityError) as caught:
                fit_velocity([observation])
            self.assertEqual(caught.exception.channel, 2)


class VelocityScoreTests(unittest.TestCase):
    def setUp(self):
        self.reference = fit_velocity([synthetic_observation([-1] * 6), synthetic_observation([1] * 6)])
        self.detector = VelocityDetector(self.reference)

    def test_synthetic_maximum_absolute_z_score(self):
        self.assertEqual(self.detector.score(synthetic_observation([0, -2, 1, 0.5, 0, 0])), 2)
        self.assertEqual(self.detector.score(synthetic_observation([0] * 6)), 0)

    def test_synthetic_score_uses_each_fitted_mean_and_sigma(self):
        reference = fit_velocity(synthetic_varied_rows())
        standardized = (0.0, 1.0, -2.0, 0.5, -4.5, 3.0)
        values = tuple(mean + sigma * z for mean, sigma, z in
                       zip(reference.mean, reference.sigma, standardized))
        self.assertAlmostEqual(VelocityDetector(reference).score(synthetic_observation(values)), 4.5)

    def test_synthetic_score_ignores_positions_and_time(self):
        a = synthetic_observation([2, 0, 0, 0, 0, 0], q=[1] * 6, dt=None)
        b = synthetic_observation([2, 0, 0, 0, 0, 0], q=[900] * 6, dt=Decimal("999"))
        self.assertEqual(self.detector.score(a), self.detector.score(b))

    def test_synthetic_reference_does_not_learn_scoring_or_update_history(self):
        before = self.reference.to_dict()
        probe = synthetic_observation([2] * 6)
        score = self.detector.score(probe)
        for _ in range(10):
            self.detector.update(synthetic_observation([1000] * 6))
            self.detector.reset()
            self.detector.score(synthetic_observation([-999] * 6))
        self.assertEqual(self.reference.to_dict(), before)
        self.assertEqual(self.detector.score(probe), score)

    def test_synthetic_score_difference_overflow_fails(self):
        reference = VelocityReference(2, (-1e308,) * 6, (1.0,) * 6, (1.0,) * 6)
        with self.assertRaises(VelocityError) as caught:
            VelocityDetector(reference).score(synthetic_observation([1e308] * 6))
        self.assertEqual(caught.exception.reason, "nonfinite_score_difference")
        self.assertEqual(caught.exception.channel, 0)

    def test_synthetic_standardization_overflow_fails(self):
        variance = 1e-320
        reference = VelocityReference(2, (0.0,) * 6, (variance,) * 6, (math.sqrt(variance),) * 6)
        with self.assertRaises(VelocityError) as caught:
            VelocityDetector(reference).score(synthetic_observation([1e308] * 6))
        self.assertEqual(caught.exception.reason, "nonfinite_standardized_score")

    def test_synthetic_python_float_arithmetic_ignores_decimal_context(self):
        rows = synthetic_varied_rows()
        expected = fit_velocity(rows)
        probe = synthetic_observation([5] * 6)
        expected_score = VelocityDetector(expected).score(probe)
        with localcontext() as context:
            context.prec = 2
            context.traps[Inexact] = True
            self.assertEqual(fit_velocity(rows), expected)
            self.assertEqual(VelocityDetector(expected).score(probe), expected_score)


class VelocityReferenceTests(unittest.TestCase):
    def setUp(self):
        self.reference = fit_velocity(synthetic_varied_rows())

    def test_synthetic_reference_and_detector_are_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            self.reference.n = 100
        with self.assertRaises(TypeError):
            self.reference.mean[0] = 100
        detector = VelocityDetector(self.reference)
        with self.assertRaises(FrozenInstanceError):
            detector.reference = self.reference

    def test_synthetic_json_export_is_a_detached_finite_copy(self):
        exported = self.reference.to_dict()
        encoded = json.dumps(exported, allow_nan=False)
        self.assertEqual(json.loads(encoded), exported)
        exported["mean"][0] = 999
        exported["n"] = 999
        self.assertEqual(self.reference.mean[0], 2.5)
        self.assertEqual(self.reference.n, 4)

    def test_synthetic_reference_rejects_invalid_state(self):
        baseline = {"n": 2, "mean": (0,) * 6, "variance": (1,) * 6, "sigma": (1,) * 6}
        invalid = [{"n": True}, {"n": 1}, {"mean": [0] * 6}, {"mean": (0,) * 5},
                   {"variance": (0,) * 6}, {"variance": (-1,) * 6},
                   {"variance": (math.inf,) * 6}, {"sigma": (0,) * 6},
                   {"sigma": (2,) * 6}, {"mean": (True,) * 6}]
        for patch in invalid:
            with self.subTest(patch=patch), self.assertRaises(VelocityError):
                VelocityReference(**{**baseline, **patch})
        with self.assertRaises(VelocityError):
            VelocityDetector(None)


if __name__ == "__main__":
    unittest.main()
