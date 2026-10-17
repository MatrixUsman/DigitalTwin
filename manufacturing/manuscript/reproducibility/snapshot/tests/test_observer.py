"""SYNTHETIC empirical-observer checks; no CASPER data or benchmark claims."""
from dataclasses import FrozenInstanceError
from decimal import Decimal
import json
import math
import unittest

from mfg_twin.controls import ControlError, Standardizer12, TemplateReference
from mfg_twin.data import Observation
from mfg_twin.observer import (EvidenceScale, ObserverConfig, PhaseObserver,
    jensen_shannon, phase_diagnostics, prepare_observation, propagate)


def reference(*, bins=8, initialization=4, scaled=False, ambiguous=False):
    mean = tuple(float(j) for j in range(12)) if scaled else (0.,) * 12
    sigma = tuple(float(j + 1) for j in range(12)) if scaled else (1.,) * 12
    scaler = Standardizer12(2, mean, tuple(s * s for s in sigma), sigma)
    rows = tuple(tuple(math.sin(2. * math.pi * k / bins * (2 if ambiguous else 1) + j * .25)
                       for j in range(12)) for k in range(bins))
    return TemplateReference(scaler, .4, bins, initialization, bins * 2, rows, (2,) * bins)


def observation(values=None, *, dt=Decimal('.05')):
    values = (0.,) * 12 if values is None else tuple(values)
    return Observation(values[:6], values[6:], dt)


def observer(ref=None, mode='synchronized', **config):
    ref = reference() if ref is None else ref
    return PhaseObserver(ref, ObserverConfig(initialization=ref.initialization, **config), mode)


def warmup(model):
    for i in range(model.config.initialization):
        item = observation(model.reference.means[i % model.reference.bins],
                           dt=None if i == 0 else Decimal('.05'))
        proposal = model.propose(item)
        model.commit(proposal)
    return model


class PropagationTests(unittest.TestCase):
    def test_synthetic_integer_phase_shift_wraps(self):
        self.assertEqual(propagate((0., 0., 0., 1.), 1., 4., 0.), (1., 0., 0., 0.))

    def test_synthetic_half_step_splits_mass(self):
        self.assertEqual(propagate((1., 0., 0., 0.), .5, 4., 0.), (.5, .5, 0., 0.))

    def test_synthetic_uniform_mixing_known_rate(self):
        result = propagate((1., 0., 0., 0.), 4., 4., math.log(2.) / 4.)
        self.assertEqual(result, (.625, .125, .125, .125))

    def test_synthetic_probability_mass_repeated_propagation(self):
        p = (1., 0., 0., 0.)
        for _ in range(1000):
            p = propagate(p, .017, 2.4, .02)
            self.assertTrue(all(0 <= value <= 1 for value in p))
            self.assertAlmostEqual(math.fsum(p), 1., places=14)

    def test_synthetic_bad_inputs_fail(self):
        for p, dt, period, rate in [((0., 0.), 1., 1., 0.), ((-1., 2.), 1., 1., 0.),
                                    ((1., 0.), -1., 1., 0.), ((1., 0.), 1., 0., 0.),
                                    ((1., 0.), 1., 1., -.1), ((math.inf, 0.), 1., 1., 0.)]:
            with self.subTest(args=(p, dt, period, rate)), self.assertRaises(ControlError):
                propagate(p, dt, period, rate)

    def test_synthetic_js_known_disjoint_distributions(self):
        self.assertEqual(jensen_shannon((1., 0.), (1., 0.)), 0.)
        self.assertAlmostEqual(jensen_shannon((1., 0.), (0., 1.)), math.log(2.))
        self.assertAlmostEqual(jensen_shannon((.1, .9), (.7, .3)),
                               jensen_shannon((.7, .3), (.1, .9)))

    def test_synthetic_uniform_ambiguity_has_no_mean_phase(self):
        result = phase_diagnostics((.25,) * 4)
        self.assertAlmostEqual(result['entropy'], 1.)
        self.assertLess(result['resultant'], 1e-12)
        self.assertIsNone(result['mean_phase'])
        self.assertEqual(result['separated_competitor_bin'], 2)
        self.assertEqual(result['separated_competitor_mass'], .25)

    def test_synthetic_opposite_modes_preserve_ambiguity(self):
        result = phase_diagnostics((.5, 0., .5, 0.))
        self.assertAlmostEqual(result['entropy'], .5)
        self.assertIsNone(result['mean_phase'])
        self.assertEqual(result['maximum_mass'], .5)
        self.assertEqual(result['separated_competitor_bin'], 2)
        self.assertEqual(result['separated_competitor_mass'], .5)
        self.assertEqual(result['separated_competitor_distance'], 2)

    def test_synthetic_nonadjacent_peak_is_distinct_from_neighbors(self):
        result = phase_diagnostics((.4, .3, .01, .02, .2, .03, .02, .02))
        self.assertEqual(result['map_bin'], 0)
        self.assertEqual(result['separated_competitor_bin'], 4)
        self.assertEqual(result['separated_competitor_mass'], .2)

    def test_synthetic_two_three_bins_have_no_nonadjacent_competitor(self):
        for p in [(1., 0.), (1., 0., 0.)]:
            result = phase_diagnostics(p)
            self.assertIsNone(result['separated_competitor_bin'])
            self.assertEqual(result['separated_competitor_mass'], 0.)
            self.assertIsNone(result['separated_competitor_distance'])


class ObserverTests(unittest.TestCase):
    def test_synthetic_current_values_cannot_change_prospective_prediction(self):
        model = warmup(observer())
        before = model.state_dict()
        a, b = model.propose(observation((0.,) * 12)), model.propose(observation((3.,) * 12))
        self.assertEqual(a.prediction, b.prediction)
        self.assertEqual(a.prior, b.prior)
        self.assertNotEqual(a.posterior, b.posterior)
        self.assertEqual(model.state_dict(), before)

    def test_synthetic_prepared_observation_matches_direct_path(self):
        model = warmup(observer())
        current = observation((.2,) * 12)
        self.assertEqual(model.propose(current), model.propose(prepare_observation(model.reference, current)))

    def test_synthetic_foreign_preparation_fails(self):
        model = observer()
        prepared = prepare_observation(reference(), observation(dt=None))
        with self.assertRaises(ControlError):
            model.propose(prepared)

    def test_synthetic_commit_is_only_state_change_and_stale_rejected(self):
        model = observer()
        proposal = model.propose(observation(dt=None))
        self.assertEqual(model.seen, 0)
        model.commit(proposal)
        self.assertEqual(model.seen, 1)
        self.assertEqual(model.posterior, proposal.posterior)
        with self.assertRaises(ControlError):
            model.commit(proposal)
        with self.assertRaises(ControlError):
            observer().commit(proposal)

    def test_synthetic_warmup_exact_length_and_reset(self):
        model = observer()
        for i in range(4):
            step = model.propose(observation(dt=None if i == 0 else Decimal('.05')))
            self.assertFalse(step.ready)
            model.commit(step)
        self.assertTrue(model.propose(observation()).ready)
        before = model.state_dict()
        reset = model.propose(observation(dt=None))
        self.assertFalse(reset.ready)
        self.assertEqual(model.state_dict(), before)
        model.commit(reset)
        self.assertEqual(model.seen, 1)
        self.assertFalse(model.propose(observation()).ready)

    def test_synthetic_first_observation_requires_reset(self):
        with self.assertRaises(ControlError):
            observer().propose(observation())

    def test_synthetic_initialization_is_identical_across_variants(self):
        models = [observer(mode=mode) for mode in PhaseObserver.MODES]
        for i in range(4):
            current = observation(reference().means[i], dt=None if i == 0 else Decimal('.05'))
            steps = [model.propose(current) for model in models]
            self.assertTrue(all(step.posterior == steps[0].posterior for step in steps))
            self.assertTrue(all(step.prediction == steps[0].prediction for step in steps))
            for model, step in zip(models, steps):
                model.commit(step)

    def test_synthetic_free_running_does_not_follow_scored_measurement(self):
        model = warmup(observer(mode='free_running'))
        a, b = model.propose(observation((0.,) * 12)), model.propose(observation((4.,) * 12))
        self.assertEqual(a.posterior, b.posterior)
        self.assertEqual(a.prior, a.posterior)
        self.assertEqual(a.correction_js, 0.)
        self.assertNotEqual(a.residual, b.residual)

    def test_synthetic_unconstrained_correction_ignores_prior_after_warmup(self):
        a, b = warmup(observer(mode='unconstrained')), warmup(observer(mode='unconstrained'))
        # Different allowed warmup histories create different prior states.
        for value in [2., 3., 4.]:
            b.commit(b.propose(observation((value,) * 12)))
        x = observation((-.3,) * 12)
        a_step, b_step = a.propose(x), b.propose(x)
        self.assertNotEqual(a_step.prior, b_step.prior)
        self.assertEqual(a_step.posterior, b_step.posterior)
        self.assertNotEqual(a_step.prediction, b_step.prediction)

    def test_synthetic_emission_temperature_formula(self):
        model = observer()
        item = observation(dt=None)
        prepared = prepare_observation(model.reference, item)
        result = model.propose(prepared)
        unnormalized = [math.exp(-d / (2. * model.config.temperature)) for d in prepared.distances]
        for actual, expected in zip(result.posterior, unnormalized):
            self.assertAlmostEqual(actual, expected / sum(unnormalized), places=14)

    def test_synthetic_stable_log_weights_when_direct_exp_underflows(self):
        model = observer(temperature=1e-8)
        step = model.propose(observation((100.,) * 12, dt=None))
        self.assertTrue(all(math.isfinite(v) for v in step.posterior))
        self.assertAlmostEqual(sum(step.posterior), 1.)

    def test_synthetic_nonfinite_arithmetic_fails_without_raw_diagnostic(self):
        with self.assertRaisesRegex(ControlError, 'nonfinite squared residual'):
            observer().propose(observation((1e308,) * 12, dt=None))

    def test_synthetic_invalid_time_break_must_be_loader_reset(self):
        model = warmup(observer())
        with self.assertRaises(ControlError):
            model.propose(observation(dt=Decimal('.1')))

    def test_synthetic_reference_and_configuration_are_immutable(self):
        model = warmup(observer())
        before = json.dumps(model.reference.to_dict(), sort_keys=True)
        config = model.config.to_dict()
        for i in range(20):
            model.commit(model.propose(observation((float(i),) * 12)))
        self.assertEqual(json.dumps(model.reference.to_dict(), sort_keys=True), before)
        self.assertEqual(model.config.to_dict(), config)
        with self.assertRaises(FrozenInstanceError):
            model.config.temperature = 900.

    def test_synthetic_ambiguous_reference_does_not_invent_unique_phase(self):
        model = observer(reference(ambiguous=True))
        step = model.propose(observation(model.reference.means[0], dt=None))
        self.assertAlmostEqual(step.posterior[0], step.posterior[4], places=14)
        diagnostics = phase_diagnostics(step.posterior)
        self.assertLess(diagnostics['resultant'], 1e-12)
        self.assertIsNone(diagnostics['mean_phase'])

    def test_synthetic_forecast_in_physical_units_with_phase_variance(self):
        model = observer(reference(scaled=True))
        model.commit(model.propose(observation(dt=None)))
        before = model.state_dict()
        result = model.forecast(.23)
        self.assertEqual(before, model.state_dict())
        for j, (prediction, actual) in enumerate(zip(result.prediction, result.physical_prediction)):
            self.assertAlmostEqual(actual, j + (j + 1) * prediction)
            variance = sum(p * (row[j] - prediction) ** 2 for p, row in
                           zip(result.probabilities, model.reference.means)) * (j + 1) ** 2
            self.assertAlmostEqual(result.physical_phase_variance[j], variance)

    def test_synthetic_forecast_rejects_uninitialized_negative_and_nonfinite(self):
        model = observer()
        with self.assertRaises(ControlError):
            model.forecast(1.)
        model.commit(model.propose(observation(dt=None)))
        for horizon in [-1., math.inf, math.nan]:
            with self.assertRaises(ControlError):
                model.forecast(horizon)

    def test_synthetic_serialization_resumes_causal_state(self):
        model = warmup(observer())
        restored = PhaseObserver.from_state_dict(json.loads(json.dumps(model.state_dict(), allow_nan=False)))
        self.assertEqual(restored.config, model.config)
        self.assertEqual(restored.reference, model.reference)
        a, b = model.propose(observation((.7,) * 12)), restored.propose(observation((.7,) * 12))
        for original, resumed in zip(a.prediction, b.prediction):
            self.assertAlmostEqual(original, resumed, places=14)

    def test_synthetic_invalid_serialization_and_configuration(self):
        base = observer().state_dict()
        for patch in [{'seen': -1}, {'mode': 'unknown'}, {'posterior': [1.] * 8}, {'seen': 0, 'posterior': [1.] + [0.] * 7}]:
            with self.subTest(patch=patch), self.assertRaises(ControlError):
                PhaseObserver.from_state_dict({**base, **patch})
        for config in [{'temperature': 0}, {'mixing_rate': -.1}, {'initialization': True}]:
            with self.subTest(config=config), self.assertRaises(ControlError):
                ObserverConfig(**config)


class EvidenceTests(unittest.TestCase):
    def test_synthetic_paired_scores_share_exact_step_and_do_not_update(self):
        model = warmup(observer())
        step = model.propose(observation((.6,) * 12))
        scale = EvidenceScale(100, 2., .5)
        before = model.state_dict()
        base, evidence = scale.scores(step)
        self.assertEqual(base, step.residual / 2.)
        self.assertEqual(evidence, base + step.correction_js / .5)
        self.assertEqual(model.state_dict(), before)

    def test_synthetic_zero_scale_is_failure_not_repaired(self):
        for n, r, c in [(0, 1., 1.), (1, 0., 1.), (1, 1., 0.), (1, math.inf, 1.)]:
            with self.assertRaises(ControlError):
                EvidenceScale(n, r, c)

    def test_synthetic_scale_roundtrip_and_warmup_not_scored(self):
        scale = EvidenceScale(10, .5, .2)
        self.assertEqual(EvidenceScale.from_dict(json.loads(json.dumps(scale.to_dict()))), scale)
        with self.assertRaises(ControlError):
            scale.scores(observer().propose(observation(dt=None)))


if __name__ == '__main__':
    unittest.main()
