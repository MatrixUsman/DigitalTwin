"""Empirical phase observer; feature-only and independent of dataset access.

This model estimates position on an empirical cyclic trajectory.  It is not a
mechanistic robot model, and its phase probabilities are algorithmic weights,
not calibrated physical-state confidence.  Fitted templates/scales never adapt.
Every prospective forecast uses the previous posterior and elapsed time alone;
``propose`` computes an innovation without changing state and ``commit`` is the
only measurement-assimilation operation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math

from .controls import (CHANNELS, ControlError, TemplateReference, _delta,
                       _finite, _mse, _positive_int)
from .data import Observation


@dataclass(frozen=True, slots=True)
class ObserverConfig:
    """Train-only emission scale plus fixed constants, not a noise model.

    The caller fits ``temperature`` as the mean nearest-template standardized
    squared error on eligible training targets, floored at a declared 1e-8.
    The default .1 exists for synthetic use, not real-experiment selection.
    Emission weights are exp(-distance / (2 * temperature)).
    """
    temperature: float = .1
    mixing_rate: float = .02
    initialization: int = 1528

    def __post_init__(self):
        temperature, rate = _finite(self.temperature), _finite(self.mixing_rate)
        if temperature <= 0 or rate < 0:
            raise ControlError("invalid observer temperature or mixing rate")
        _positive_int(self.initialization, "observer initialization")
        object.__setattr__(self, "temperature", temperature)
        object.__setattr__(self, "mixing_rate", rate)

    def to_dict(self):
        return {"temperature": self.temperature, "mixing_rate": self.mixing_rate,
                "initialization": self.initialization}

    @classmethod
    def from_dict(cls, value):
        if not isinstance(value, dict) or set(value) != {"temperature", "mixing_rate", "initialization"}:
            raise ControlError("invalid serialized observer configuration")
        return cls(**value)


def _probabilities(values, bins=None):
    if not isinstance(values, (tuple, list)) or len(values) < 2 or (bins is not None and len(values) != bins):
        raise ControlError("invalid phase probability shape")
    result = tuple(_finite(v) for v in values)
    if any(v < 0 for v in result):
        raise ControlError("negative phase probability")
    total = math.fsum(result)
    if not math.isfinite(total) or total <= 0:
        raise ControlError("invalid phase probability mass")
    return tuple(v / total for v in result)


def propagate(probabilities, seconds, period_seconds, mixing_rate):
    """Fractional circular shift plus a time-scaled uniform mixture.

    This is a numerical transition rule, not an identified robot transition
    model.  Fractional shifts introduce bin diffusion; direct long-horizon
    forecasts need not equal repeated short-step propagation.
    """
    probabilities = _probabilities(probabilities)
    seconds, period_seconds, mixing_rate = map(_finite, (seconds, period_seconds, mixing_rate))
    if seconds < 0 or period_seconds <= 0 or mixing_rate < 0:
        raise ControlError("invalid phase propagation arguments")
    bins = len(probabilities)
    shift = _finite(seconds * bins / period_seconds)
    whole = math.floor(shift)
    fraction = shift - whole
    epsilon = -math.expm1(-mixing_rate * seconds)
    keep, uniform = 1. - epsilon, epsilon / bins
    shifted = tuple(keep * ((1. - fraction) * probabilities[(k - whole) % bins] +
                            fraction * probabilities[(k - whole - 1) % bins]) + uniform
                    for k in range(bins))
    return _probabilities(shifted, bins)


def jensen_shannon(left, right):
    """Natural-log JS divergence, 0..log(2); no arbitrary numerical clipping."""
    left, right = _probabilities(left), _probabilities(right)
    if len(left) != len(right):
        raise ControlError("phase distributions differ in size")
    terms = []
    for p, q in zip(left, right):
        middle = .5 * (p + q)
        if p > 0:
            terms.append(.5 * p * math.log(p / middle))
        if q > 0:
            terms.append(.5 * q * math.log(q / middle))
    result = _finite(math.fsum(terms))
    # Summation can leave a tiny negative cancellation error near equality.
    if result < -1e-14 or result > math.log(2.) + 1e-14:
        raise ControlError("invalid Jensen-Shannon arithmetic")
    return max(0., result)


def phase_diagnostics(probabilities):
    """Uncalibrated ambiguity summaries; a mean is undefined near zero resultant."""
    p = _probabilities(probabilities)
    bins = len(p)
    entropy = -math.fsum(v * math.log(v) for v in p if v > 0) / math.log(bins)
    real = math.fsum(v * math.cos(2. * math.pi * k / bins) for k, v in enumerate(p))
    imaginary = math.fsum(v * math.sin(2. * math.pi * k / bins) for k, v in enumerate(p))
    resultant = min(1., math.hypot(real, imaginary))
    map_bin = max(range(bins), key=lambda k: (p[k], -k))
    separated = [k for k in range(bins)
                 if min((k - map_bin) % bins, (map_bin - k) % bins) >= 2]
    second = max(separated, key=lambda k: (p[k], -k)) if separated else None
    return {"entropy": entropy, "resultant": resultant,
            "mean_phase": None if resultant < 1e-12 else (math.atan2(imaginary, real) / (2. * math.pi)) % 1.,
            "map_bin": map_bin, "maximum_mass": p[map_bin],
            "separated_competitor_bin": second,
            "separated_competitor_mass": p[second] if second is not None else 0.,
            "separated_competitor_distance": None if second is None else min((second - map_bin) % bins, (map_bin - second) % bins)}


@dataclass(frozen=True, slots=True)
class PreparedObservation:
    reference: TemplateReference = field(repr=False, compare=False)
    observation: Observation = field(repr=False)
    standardized: tuple[float, ...]
    distances: tuple[float, ...]


def prepare_observation(reference: TemplateReference, observation: Observation):
    """Compute the shared, current-measurement emission distances once per row."""
    if not isinstance(reference, TemplateReference):
        raise ControlError("invalid observer template")
    _delta(observation)
    values = reference.scaler.transform(observation)
    return PreparedObservation(reference, observation, values,
                               tuple(_mse(values, row) for row in reference.means))


@dataclass(frozen=True, slots=True)
class ObserverStep:
    prior: tuple[float, ...]
    posterior: tuple[float, ...]
    prediction: tuple[float, ...]
    physical_prediction: tuple[float, ...]
    residual: float
    correction_js: float
    ready: bool
    next_seen: int
    _owner: object = field(repr=False, compare=False)
    _generation: int = field(repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class Forecast:
    probabilities: tuple[float, ...]
    prediction: tuple[float, ...]
    physical_prediction: tuple[float, ...]
    physical_phase_variance: tuple[float, ...]
    entropy: float
    resultant: float
    mean_phase: float | None
    map_bin: int
    maximum_mass: float
    separated_competitor_bin: int | None
    separated_competitor_mass: float
    separated_competitor_distance: int | None


class PhaseObserver:
    """Three declared synchronization variants sharing one immutable mapping.

    synchronized: posterior proportional to prior times emission weight.
    unconstrained: same prospective prediction, but emission-only posterior.
    free_running: same warmup, then posterior equals nominal propagated prior.

    The first ``initialization`` observations use synchronized assimilation in
    every variant.  Current observations never enter their own predictions.
    """
    MODES = ("synchronized", "unconstrained", "free_running")

    def __init__(self, reference: TemplateReference, config: ObserverConfig | None = None,
                 mode: str = "synchronized"):
        if not isinstance(reference, TemplateReference):
            raise ControlError("invalid observer template")
        self.config = ObserverConfig() if config is None else config
        if not isinstance(self.config, ObserverConfig) or mode not in self.MODES:
            raise ControlError("invalid observer configuration or mode")
        if self.config.initialization != reference.initialization:
            raise ControlError("observer and reference initialization differ")
        self.reference, self.mode = reference, mode
        self._columns = tuple(tuple(row[j] for row in reference.means) for j in range(CHANNELS))
        self._owner, self._generation = object(), 0
        self.posterior = (1. / reference.bins,) * reference.bins
        self.seen = 0

    def _mapping(self, p):
        return tuple(_finite(math.fsum(weight * value for weight, value in zip(p, column)))
                     for column in self._columns)

    def _physical(self, prediction):
        return tuple(_finite(mean + sigma * value) for mean, sigma, value in
                     zip(self.reference.scaler.mean, self.reference.scaler.sigma, prediction))

    def _assimilate(self, prior, distances, *, unrestricted):
        weights = []
        for p, distance in zip(prior, distances):
            exponent = _finite(-.5 * distance / self.config.temperature)
            weights.append(exponent if unrestricted else (math.log(p) + exponent if p > 0 else -math.inf))
        maximum = max(weights)
        if not math.isfinite(maximum):
            raise ControlError("empty observer likelihood support")
        return _probabilities(tuple(math.exp(weight - maximum) for weight in weights), self.reference.bins)

    def propose(self, observation: Observation | PreparedObservation) -> ObserverStep:
        prepared = observation if isinstance(observation, PreparedObservation) else prepare_observation(self.reference, observation)
        if prepared.reference is not self.reference:
            raise ControlError("prepared observation belongs to another reference")
        observation = prepared.observation
        delta = _delta(observation)
        is_reset = observation.dt is None
        if self.seen == 0 and not is_reset:
            raise ControlError("observer stream must begin with a reset observation")
        seen = 0 if is_reset else self.seen
        prior = ((1. / self.reference.bins,) * self.reference.bins if is_reset else
                 propagate(self.posterior, delta, self.reference.period_seconds, self.config.mixing_rate))
        prediction = self._mapping(prior)
        residual = _mse(prepared.standardized, prediction)
        ready = not is_reset and seen >= self.config.initialization
        if self.mode == "free_running" and ready:
            posterior = prior
        else:
            posterior = self._assimilate(prior, prepared.distances,
                                        unrestricted=self.mode == "unconstrained" and ready)
        return ObserverStep(prior, posterior, prediction, self._physical(prediction),
                            residual, jensen_shannon(prior, posterior), ready, seen + 1,
                            self._owner, self._generation)

    def commit(self, proposal: ObserverStep):
        """Assimilate exactly one proposal from the current observer generation."""
        if not isinstance(proposal, ObserverStep) or proposal._owner is not self._owner or proposal._generation != self._generation:
            raise ControlError("foreign or stale observer proposal")
        self.posterior, self.seen = proposal.posterior, proposal.next_seen
        self._generation += 1

    def forecast(self, seconds: float) -> Forecast:
        """Prospective mapping, with phase-mixture variance only (no noise model)."""
        if self.seen == 0:
            raise ControlError("forecast requires assimilated history")
        p = propagate(self.posterior, seconds, self.reference.period_seconds, self.config.mixing_rate)
        prediction = self._mapping(p)
        variances = tuple(_finite(math.fsum(weight * (value - mean) ** 2 for weight, value in zip(p, column)) * sigma ** 2)
                          for column, mean, sigma in zip(self._columns, prediction, self.reference.scaler.sigma))
        return Forecast(p, prediction, self._physical(prediction), variances, **phase_diagnostics(p))

    def state_dict(self):
        return {"kind": "empirical_phase_observer", "reference": self.reference.to_dict(),
                "config": self.config.to_dict(), "mode": self.mode,
                "seen": self.seen, "posterior": list(self.posterior)}

    @classmethod
    def from_state_dict(cls, value):
        if not isinstance(value, dict) or set(value) != {"kind", "reference", "config", "mode", "seen", "posterior"} or value["kind"] != "empirical_phase_observer":
            raise ControlError("invalid serialized observer state")
        observer = cls(TemplateReference.from_dict(value["reference"]),
                       ObserverConfig.from_dict(value["config"]), value["mode"])
        seen = _positive_int(value["seen"], "observer seen count", 0)
        p = _probabilities(value["posterior"], observer.reference.bins)
        if not math.isclose(math.fsum(value["posterior"]), 1., rel_tol=0., abs_tol=1e-12):
            raise ControlError("serialized phase mass is not normalized")
        if seen == 0 and any(abs(v - 1. / observer.reference.bins) > 1e-12 for v in p):
            raise ControlError("uninitialized state must be uniform")
        observer.posterior, observer.seen = p, seen
        return observer


@dataclass(frozen=True, slots=True)
class EvidenceScale:
    """Training-only positive component means; caller controls fitting scope."""
    n: int
    mean_residual: float
    mean_correction: float

    def __post_init__(self):
        _positive_int(self.n, "evidence-scale targets")
        for name in ("mean_residual", "mean_correction"):
            value = _finite(getattr(self, name))
            if value <= 0:
                raise ControlError("zero or invalid evidence normalization mean")
            object.__setattr__(self, name, value)

    def scores(self, proposal: ObserverStep):
        if not isinstance(proposal, ObserverStep) or not proposal.ready:
            raise ControlError("paired scores require an initialized observer proposal")
        residual = _finite(proposal.residual / self.mean_residual)
        return residual, _finite(residual + proposal.correction_js / self.mean_correction)

    def to_dict(self):
        return {"n": self.n, "mean_residual": self.mean_residual,
                "mean_correction": self.mean_correction}

    @classmethod
    def from_dict(cls, value):
        if not isinstance(value, dict) or set(value) != {"n", "mean_residual", "mean_correction"}:
            raise ControlError("invalid serialized evidence scale")
        return cls(**value)
