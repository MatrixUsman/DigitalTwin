"""SYNTHETIC explanatory-score checks, never CASPER or benchmark results."""
from dataclasses import FrozenInstanceError, fields, replace
from decimal import Decimal
import json
import math
import unittest

from mfg_twin.controls import ControlError, Standardizer12, TemplateReference
from mfg_twin.data import Observation
from mfg_twin.observer import (EvidenceScale, ObserverConfig, PhaseObserver,
                              prepare_observation)
from mfg_twin.observer_scores import SCORE_IDS, score_observer_proposal


def synthetic_case(*, rows=None, values=None, prior=(.25, .75), temperature=1., scaled=False):
    rows = ((0.,) * 12, (2.,) * 12) if rows is None else tuple(tuple(r) for r in rows)
    values = (0.,) * 12 if values is None else tuple(values)
    sigma = tuple(float(j + 1) for j in range(12)) if scaled else (1.,) * 12
    mean = tuple(float(j) for j in range(12)) if scaled else (0.,) * 12
    scaler = Standardizer12(8, mean, tuple(s * s for s in sigma), sigma)
    reference = TemplateReference(scaler, .05, len(rows), 1, len(rows) * 2,
                                  rows, (2,) * len(rows))
    config = ObserverConfig(temperature=temperature, mixing_rate=0., initialization=1)
    model = PhaseObserver(reference, config)
    model.commit(model.propose(Observation(mean[:6], mean[6:], None)))
    # Synthetic known state; one full-period step preserves this chosen prior.
    model.posterior = prior
    physical = tuple(m + s * z for m, s, z in zip(mean, sigma, values))
    observation = Observation(physical[:6], physical[6:], Decimal('.05'))
    prepared = prepare_observation(reference, observation)
    proposal = model.propose(prepared)
    scales = EvidenceScale(9, .3, .02)
    return model, prepared, proposal, scales


def score(case):
    model, prepared, proposal, scales = case
    return score_observer_proposal(proposal, prepared, model.config, scales)


class ScoreArithmeticTests(unittest.TestCase):
    def test_synthetic_closed_form_two_component_arithmetic(self):
        case = synthetic_case(temperature=2. / math.log(3.))
        scores = score(case)
        self.assertAlmostEqual(case[2].posterior[0], .5, places=15)
        self.assertAlmostEqual(case[2].posterior[1], .5, places=15)
        expected_k = .5 * math.log(2.) + .5 * math.log(2. / 3.)
        expected_c = (.125 * math.log(2. / 3.) + .25 * math.log(4. / 3.) +
                      .375 * math.log(6. / 5.) + .25 * math.log(4. / 5.))
        self.assertAlmostEqual(scores.bayesian_surprise, expected_k, places=15)
        self.assertAlmostEqual(scores.correction_js, expected_c, places=15)
        self.assertAlmostEqual(scores.predictive_energy, math.log(2.), places=15)
        self.assertEqual(scores.velocity_residual, 2.25)
        self.assertEqual(scores.residual_scaled, 2.25 / .3)

    def test_synthetic_kl_orientation_is_posterior_to_prior(self):
        case = synthetic_case(temperature=2. / math.log(3.))
        actual = score(case).bayesian_surprise
        reverse = .25 * math.log(.5) + .75 * math.log(1.5)
        self.assertGreater(abs(actual - reverse), .01)
        self.assertAlmostEqual(actual, .5 * math.log(4. / 3.), places=15)

    def test_synthetic_energy_equals_kl_plus_posterior_component_energy(self):
        for tau in (.001, .2, 1., 100.):
            with self.subTest(tau=tau):
                case = synthetic_case(temperature=tau, values=(.3,) * 12)
                scores = score(case)
                posterior_energy = sum(q * d / (2. * tau) for q, d in
                                       zip(case[2].posterior, case[1].distances))
                self.assertAlmostEqual(scores.predictive_energy,
                                       scores.bayesian_surprise + posterior_energy, places=11)

    def test_synthetic_equal_emission_leaves_distribution_and_zero_correction(self):
        case = synthetic_case(values=(1.,) * 12)
        scores = score(case)
        self.assertAlmostEqual(scores.correction_js, 0., places=15)
        self.assertAlmostEqual(scores.bayesian_surprise, 0., places=15)
        self.assertAlmostEqual(scores.predictive_energy, .5, places=15)

    def test_synthetic_exact_zero_distance_energy(self):
        scores = score(synthetic_case(rows=((0.,) * 12,) * 2))
        self.assertEqual(scores.predictive_energy, 0.)
        self.assertEqual(scores.velocity_residual, 0.)

    def test_synthetic_all_direct_likelihoods_underflow_but_energy_is_finite(self):
        case = synthetic_case(rows=((0.,) * 12,) * 2, values=(100.,) * 12,
                              prior=(.5, .5), temperature=1e-8)
        self.assertTrue(all(math.exp(-d / (2e-8)) == 0 for d in case[1].distances))
        scores = score(case)
        self.assertTrue(all(math.isfinite(x) for x in scores.to_dict().values()))
        self.assertEqual(scores.predictive_energy, 5e11)

    def test_synthetic_large_ratio_kl_avoids_division_overflow(self):
        case = synthetic_case(prior=(1e-320, 1.), rows=((0.,) * 12, (math.sqrt(2000.),) * 12))
        self.assertTrue(math.isinf(case[2].posterior[0] / case[2].prior[0]))
        scores = score(case)
        self.assertAlmostEqual(scores.bayesian_surprise, -math.log(1e-320), places=12)
        self.assertTrue(math.isfinite(scores.predictive_energy))

    def test_synthetic_zero_posterior_uses_zero_log_zero_limit(self):
        case = synthetic_case(temperature=1e-6)
        self.assertEqual(case[2].posterior, (1., 0.))
        self.assertAlmostEqual(score(case).bayesian_surprise, math.log(4.), places=15)

    def test_synthetic_subnormal_midpoint_cannot_divide_by_zero(self):
        case = synthetic_case(prior=(.5, .5), rows=((100.,) * 12, (0.,) * 12))
        model, prepared, step, scales = case
        # Mathematically consistent synthetic limiting distribution. Existing
        # observer construction is intentionally not changed by this extension.
        tiny = math.nextafter(0., 1.)
        prediction = (tiny * 100.,) * 12
        step = replace(step, prior=(tiny, 1.), posterior=(0., 1.),
                       prediction=prediction, physical_prediction=prediction,
                       residual=0., correction_js=0.)
        result = score_observer_proposal(step, prepared, model.config, scales)
        self.assertEqual(result.bayesian_surprise, 0.)
        self.assertEqual(result.predictive_energy, 0.)

    def test_synthetic_mixture_mean_component_distance_identity(self):
        case = synthetic_case(values=(1.,) * 12)
        _, prepared, step, _ = case
        component_distance = sum(p * d for p, d in zip(step.prior, prepared.distances))
        phase_variance = sum(p * sum((row[j] - step.prediction[j]) ** 2 for j in range(12)) / 12.
                             for p, row in zip(step.prior, prepared.reference.means))
        self.assertEqual(step.residual, .25)
        self.assertEqual(phase_variance, .75)
        self.assertEqual(component_distance, step.residual + phase_variance)
        # A small mean residual does not imply a well-localized phase mixture.
        self.assertGreater(component_distance, step.residual)

    def test_synthetic_velocity_score_indexes_all_six_velocity_channels(self):
        values = (100.,) * 6 + (1., 2., 3., 4., 5., 6.)
        case = synthetic_case(rows=((0.,) * 12,) * 2, values=values)
        self.assertEqual(score(case).velocity_residual, 91. / 6.)

    def test_synthetic_velocity_uses_training_standardized_units(self):
        case = synthetic_case(rows=((0.,) * 12,) * 2, values=(0.,) * 6 + (2.,) * 6,
                              scaled=True)
        self.assertEqual(score(case).velocity_residual, 4.)

    def test_synthetic_position_aligned_speed_amplitude_is_visible(self):
        # Artificial measurement arithmetic, not a physically valid robot
        # transition, attack simulation or measured benchmark improvement.
        rows = ((0.,) * 12,) * 2
        nominal = synthetic_case(rows=rows)
        changed = synthetic_case(rows=rows, values=(0.,) * 6 + (3.,) * 6)
        self.assertEqual(nominal[2].prediction[:6], changed[2].prediction[:6])
        self.assertEqual(nominal[1].standardized[:6], changed[1].standardized[:6])
        self.assertEqual(score(nominal).velocity_residual, 0.)
        self.assertEqual(score(changed).velocity_residual, 9.)

    def test_synthetic_legacy_pair_is_bit_exact_and_singletons_unscaled(self):
        case = synthetic_case()
        first = score(case)
        self.assertEqual((first.residual_scaled, first.residual_correction_scaled),
                         case[3].scores(case[2]))
        alternate = score_observer_proposal(case[2], case[1], case[0].config,
                                             EvidenceScale(20, 7., 11.))
        for key in ('O-C', 'O-K', 'O-L', 'O-Rv'):
            self.assertEqual(first.to_dict()[key], alternate.to_dict()[key])
        self.assertNotEqual(first.residual_scaled, alternate.residual_scaled)


class ScoreIsolationTests(unittest.TestCase):
    def test_synthetic_score_selection_cannot_change_trajectory_or_future_predictions(self):
        base, _, _, scales = synthetic_case()
        models = [PhaseObserver.from_state_dict(base.state_dict()) for _ in range(3)]
        for i in range(20):
            item = Observation((i / 20.,) * 6, (-i / 30.,) * 6, Decimal('.04'))
            proposals = []
            for index, model in enumerate(models):
                prepared = prepare_observation(model.reference, item)
                proposal = model.propose(prepared)
                if index:
                    scores = score_observer_proposal(proposal, prepared, model.config, scales)
                    exported = scores.to_dict() if index == 1 else {'O-L': scores.predictive_energy}
                    self.assertTrue(exported)
                proposals.append(proposal)
                model.commit(proposal)
            self.assertEqual(proposals[0].prediction, proposals[1].prediction)
            self.assertEqual(proposals[0].prediction, proposals[2].prediction)
            self.assertEqual(models[0].state_dict(), models[1].state_dict())
            self.assertEqual(models[0].state_dict(), models[2].state_dict())
            self.assertEqual(models[0].forecast(.5), models[1].forecast(.5))

    def test_synthetic_scoring_is_pure_and_outputs_are_frozen(self):
        case = synthetic_case()
        model, prepared, proposal, scales = case
        before = json.dumps(model.state_dict(), sort_keys=True)
        result = score(case)
        self.assertEqual(json.dumps(model.state_dict(), sort_keys=True), before)
        self.assertEqual(result, score(case))
        self.assertEqual(tuple(result.to_dict()), SCORE_IDS)
        with self.assertRaises(FrozenInstanceError):
            result.predictive_energy = 0.
        model.commit(proposal)
        self.assertEqual(model.posterior, proposal.posterior)
        with self.assertRaisesRegex(ControlError, 'stale'):
            model.commit(proposal)

    def test_synthetic_current_observation_changes_score_not_prior_prediction(self):
        model, first, proposal, scales = synthetic_case()
        other = prepare_observation(model.reference,
                    Observation((5.,) * 6, (-2.,) * 6, Decimal('.05')))
        second = model.propose(other)
        self.assertEqual(proposal.prior, second.prior)
        self.assertEqual(proposal.prediction, second.prediction)
        self.assertNotEqual(score_observer_proposal(proposal, first, model.config, scales),
                            score_observer_proposal(second, other, model.config, scales))

    def test_synthetic_feature_boundary_has_no_labels_or_absolute_coordinates(self):
        self.assertEqual({f.name for f in fields(Observation)}, {'q', 'qdot', 'dt'})
        self.assertEqual({f.name for f in fields(type(synthetic_case()[1]))},
                         {'reference', 'observation', 'standardized', 'distances'})


class ScoreFailureTests(unittest.TestCase):
    def setUp(self):
        self.model, self.prepared, self.proposal, self.scales = synthetic_case()

    def checked(self, proposal=None, prepared=None, config=None, scales=None):
        return score_observer_proposal(self.proposal if proposal is None else proposal,
                self.prepared if prepared is None else prepared,
                self.model.config if config is None else config,
                self.scales if scales is None else scales)

    def test_synthetic_prior_must_be_positive_normalized_and_finite(self):
        for values in ((0., 1.), (-.1, 1.1), (.5, .6), (math.nan, 1.), (math.inf, 0.),
                       (1e308, 1e308)):
            with self.subTest(values=values), self.assertRaises(ControlError):
                self.checked(proposal=replace(self.proposal, prior=values))

    def test_synthetic_posterior_must_be_nonnegative_normalized_and_finite(self):
        for values in ((-.1, 1.1), (.5, .6), (math.nan, 1.), (math.inf, 0.)):
            with self.subTest(values=values), self.assertRaises(ControlError):
                self.checked(proposal=replace(self.proposal, posterior=values))

    def test_synthetic_shapes_are_checked_without_zip_truncation(self):
        for field, value in (('prior', (1.,)), ('posterior', (1.,)),
                             ('prediction', (0.,) * 11), ('physical_prediction', (0.,) * 13)):
            with self.subTest(field=field), self.assertRaises(ControlError):
                self.checked(proposal=replace(self.proposal, **{field: value}))
        for field, value in (('standardized', (0.,) * 11), ('distances', (0.,))):
            with self.subTest(field=field), self.assertRaises(ControlError):
                self.checked(prepared=replace(self.prepared, **{field: value}))

    def test_synthetic_tampered_preparation_and_forecast_are_rejected(self):
        mutations = [('standardized', (1.,) * 12), ('distances', (-1., 4.)),
                     ('distances', (0., 5.)), ('distances', (0., math.inf))]
        for field, value in mutations:
            with self.subTest(field=field, value=value), self.assertRaises(ControlError):
                self.checked(prepared=replace(self.prepared, **{field: value}))
        mutations = [('prediction', (0.,) * 12), ('physical_prediction', (0.,) * 12),
                     ('residual', 0.), ('correction_js', 0.), ('residual', math.nan)]
        for field, value in mutations:
            with self.subTest(field=field), self.assertRaises(ControlError):
                self.checked(proposal=replace(self.proposal, **{field: value}))

    def test_synthetic_unmatched_current_measurement_rejected(self):
        other = prepare_observation(self.model.reference,
                         Observation((1.,) * 6, (1.,) * 6, Decimal('.05')))
        with self.assertRaises(ControlError):
            self.checked(prepared=other)

    def test_synthetic_wrong_emission_or_unconstrained_posterior_rejected(self):
        with self.assertRaisesRegex(ControlError, 'synchronized posterior'):
            self.checked(config=replace(self.model.config, temperature=9.))
        with self.assertRaisesRegex(ControlError, 'synchronized posterior'):
            self.checked(proposal=replace(self.proposal, posterior=(.5, .5)))

    def test_synthetic_warmup_and_invalid_reference_config_fail(self):
        with self.assertRaises(ControlError):
            self.checked(proposal=replace(self.proposal, ready=False))
        with self.assertRaises(ControlError):
            self.checked(config=replace(self.model.config, initialization=2))
        with self.assertRaises(ControlError):
            self.checked(prepared=replace(self.prepared, reference=object()))
        with self.assertRaises(ControlError):
            self.checked(scales=object())

    def test_synthetic_gap_reset_cannot_export_eligible_scores(self):
        prepared = prepare_observation(self.model.reference, Observation((0.,) * 6, (0.,) * 6, None))
        reset = self.model.propose(prepared)
        with self.assertRaises(ControlError):
            self.checked(proposal=reset, prepared=prepared)
        self.model.commit(reset)
        self.assertEqual(self.model.seen, 1)


if __name__ == '__main__':
    unittest.main()
