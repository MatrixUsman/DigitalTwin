"""Versioned, feature-only explanatory scores for the frozen phase observer.

No fitting, state mutation, data access, labels or thresholds occur here.  Pass
one synchronized ``propose`` result and its prepared observation, export scores,
then ``commit`` that same result.  The caller owns generation/order enforcement;
without a live observer this pure function cannot detect an already committed
proposal.  Mathematical consistency checks reject mismatched inputs.

C is natural-log Jensen--Shannon divergence, K is KL(posterior || prior), and
L is an unnormalized predictive energy, not a calibrated log probability.
Rv uses only the six velocity errors of the same twelve-channel prior forecast.
Legacy R and RC keep their original training scales and arithmetic exactly.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

from .controls import CHANNELS, ControlError, TemplateReference, _finite, _mse, _vector
from .observer import (EvidenceScale, ObserverConfig, ObserverStep,
                       PreparedObservation)


MASS_ABS_TOL = 1e-12
CONSISTENCY_REL_TOL = 1e-12
CONSISTENCY_ABS_TOL = 1e-14
NONNEGATIVE_ABS_TOL = 1e-14
SCORE_IDS = ("O-R", "O-RC", "O-C", "O-K", "O-L", "O-Rv")


@dataclass(frozen=True, slots=True)
class ObserverScores:
    residual_scaled: float
    residual_correction_scaled: float
    correction_js: float
    bayesian_surprise: float
    predictive_energy: float
    velocity_residual: float

    def to_dict(self) -> dict[str, float]:
        return dict(zip(SCORE_IDS, (self.residual_scaled,
                                   self.residual_correction_scaled,
                                   self.correction_js, self.bayesian_surprise,
                                   self.predictive_energy, self.velocity_residual)))


def _same(actual, expected, name):
    actual = _finite(actual)
    if not math.isclose(actual, expected, rel_tol=CONSISTENCY_REL_TOL,
                        abs_tol=CONSISTENCY_ABS_TOL):
        raise ControlError("inconsistent " + name)


def _distribution(values, bins, *, positive):
    result = _vector(values, bins)
    if any((p <= 0 if positive else p < 0) or p > 1. for p in result):
        raise ControlError("invalid explanatory-score probability support")
    if not math.isclose(math.fsum(result), 1., rel_tol=0., abs_tol=MASS_ABS_TOL):
        raise ControlError("explanatory-score probability mass is not normalized")
    # Deliberately do not smooth zero mass or silently normalize the input.
    return result


def _nonnegative(value):
    value = _finite(value, "nonfinite explanatory score")
    if value < -NONNEGATIVE_ABS_TOL:
        raise ControlError("negative explanatory score beyond roundoff tolerance")
    return max(0., value)


def _js(left, right):
    """JS without constructing a possibly underflowed subnormal midpoint."""
    terms = []
    for p, q in zip(left, right):
        log_p = math.log(p)
        log_q = math.log(q) if q > 0 else -math.inf
        maximum = max(log_p, log_q)
        log_middle = maximum + math.log(math.exp(log_p - maximum) +
                                        math.exp(log_q - maximum)) - math.log(2.)
        terms.append(.5 * p * (log_p - log_middle))
        if q > 0:
            terms.append(.5 * q * (log_q - log_middle))
    result = _nonnegative(math.fsum(terms))
    if result > math.log(2.) + NONNEGATIVE_ABS_TOL:
        raise ControlError("invalid explanatory-score JS bound")
    return result


def score_observer_proposal(proposal: ObserverStep, prepared: PreparedObservation,
                            config: ObserverConfig, scales: EvidenceScale) -> ObserverScores:
    """Compute six scores on one initialized synchronized proposal without mutation.

    Every vector and scalar must be finite.  Probability mass tolerance is
    1e-12 absolute; consistency uses 1e-12 relative / 1e-14 absolute.  Computed
    nonnegative scores in [-1e-14, 0) become zero; worse negatives fail closed.
    These are floating-point checks, not new learned/model parameters.  Posterior
    zero weights from exp underflow are valid, with 0 log 0 interpreted as zero.
    Strict positive prior support is required; no epsilon or hidden smoothing.
    """
    if not isinstance(proposal, ObserverStep) or not proposal.ready:
        raise ControlError("explanatory scores require an initialized proposal")
    if not isinstance(prepared, PreparedObservation) or not isinstance(prepared.reference, TemplateReference):
        raise ControlError("invalid explanatory-score prepared observation")
    if not isinstance(config, ObserverConfig) or not isinstance(scales, EvidenceScale):
        raise ControlError("invalid explanatory-score configuration or scales")
    reference = prepared.reference
    if config.initialization != reference.initialization:
        raise ControlError("observer and explanatory-score initialization differ")
    bins = reference.bins
    prior = _distribution(proposal.prior, bins, positive=True)
    posterior = _distribution(proposal.posterior, bins, positive=False)
    values = _vector(prepared.standardized)
    distances = _vector(prepared.distances, bins)
    prediction = _vector(proposal.prediction)
    physical = _vector(proposal.physical_prediction)
    for actual, expected in zip(values, reference.scaler.transform(prepared.observation)):
        _same(actual, expected, "prepared standardization")
    for distance, row in zip(distances, reference.means):
        if distance < 0:
            raise ControlError("negative explanatory-score distance")
        _same(distance, _mse(values, row), "prepared template distance")
    for j in range(CHANNELS):
        expected = math.fsum(p * row[j] for p, row in zip(prior, reference.means))
        _same(prediction[j], expected, "prior prediction")
        _same(physical[j], reference.scaler.mean[j] + reference.scaler.sigma[j] * prediction[j],
              "physical prediction")
    _same(proposal.residual, _mse(values, prediction), "prospective residual")
    if proposal.residual < 0 or _finite(proposal.correction_js) < 0:
        raise ControlError("negative legacy proposal score")

    # Match the immutable observer's exponent order, while avoiding exp(-D/2tau)
    # underflow and q/p overflow.  No normalizing density constant is asserted.
    log_weights = tuple(_finite(math.log(p) + _finite(-.5 * d / config.temperature))
                        for p, d in zip(prior, distances))
    maximum = max(log_weights)
    shifted = tuple(math.exp(value - maximum) for value in log_weights)
    denominator = math.fsum(shifted)
    for actual, numerator in zip(posterior, shifted):
        _same(actual, numerator / denominator, "synchronized posterior")
    correction = _js(prior, posterior)
    _same(proposal.correction_js, correction, "correction divergence")

    surprise = _nonnegative(math.fsum(q * (math.log(q) - math.log(p))
                                     for p, q in zip(prior, posterior) if q > 0))
    energy = _nonnegative(-(maximum + math.log(denominator)))
    try:
        velocity = _nonnegative(math.fsum((values[j] - prediction[j]) ** 2
                                         for j in range(6, 12)) / 6.)
    except (OverflowError, ValueError) as exc:
        raise ControlError("nonfinite velocity residual") from exc
    residual, combined = scales.scores(proposal)
    _nonnegative(residual)
    _nonnegative(combined)
    # Preserve the exact v0.1 JS value too: RC's old arithmetic remains intact.
    return ObserverScores(residual, combined, proposal.correction_js,
                          surprise, energy, velocity)
