"""Independent ordinary controls; standard library, feature-only, no data access.

All fitted objects are immutable. Callers enforce training-only fitting and common
eligible targets. Dynamic history/phase is initialized within each new segment;
call score before update. Scores are mean squared standardized prediction errors.
These controls do not establish a physical digital twin.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import math
from typing import Iterable

from .data import Observation

CHANNELS = 12


class ControlError(ValueError):
    """Fail closed without including raw observations in the diagnostic."""


def _finite(value: object, reason: str = "nonfinite arithmetic") -> float:
    if type(value) not in (float, int):
        raise ControlError(reason)
    try:
        result = float(value)
    except (ValueError, OverflowError) as exc:
        raise ControlError(reason) from exc
    if not math.isfinite(result):
        raise ControlError(reason)
    return result


def _vector(values: object, length: int = CHANNELS) -> tuple[float, ...]:
    if not isinstance(values, (tuple, list)) or len(values) != length:
        raise ControlError("invalid vector shape")
    return tuple(_finite(value) for value in values)


def _features(observation: Observation) -> tuple[float, ...]:
    if not isinstance(observation, Observation):
        raise ControlError("expected feature-only Observation")
    if len(observation.q) != 6 or len(observation.qdot) != 6:
        raise ControlError("expected six positions and six velocities")
    return _vector(observation.q + observation.qdot)


def _positive_int(value: object, name: str, minimum: int = 1) -> int:
    if type(value) is not int or value < minimum:
        raise ControlError("invalid " + name)
    return value


def _delta(observation: Observation) -> float:
    if not isinstance(observation, Observation):
        raise ControlError("expected feature-only Observation")
    if observation.dt is None:
        return 0.0
    delta = float(observation.dt)
    if not math.isfinite(delta) or delta <= 0 or delta > .075:
        raise ControlError("invalid continuous relative time")
    return delta


@dataclass(frozen=True, slots=True)
class Standardizer12:
    n: int
    mean: tuple[float, ...]
    variance: tuple[float, ...]
    sigma: tuple[float, ...]

    def __post_init__(self):
        _positive_int(self.n, "scaler sample count", 2)
        for field in ("mean", "variance", "sigma"):
            object.__setattr__(self, field, _vector(getattr(self, field)))
        for variance, sigma in zip(self.variance, self.sigma):
            if variance <= 0 or sigma <= 0 or sigma != math.sqrt(variance):
                raise ControlError("constant channel or invalid fitted scale")

    def transform(self, observation: Observation) -> tuple[float, ...]:
        return tuple(_finite((value - mean) / sigma) for value, mean, sigma in
                     zip(_features(observation), self.mean, self.sigma))

    def to_dict(self):
        return {"n": self.n, "mean": list(self.mean), "variance": list(self.variance),
                "sigma": list(self.sigma)}

    @classmethod
    def from_dict(cls, obj):
        if not isinstance(obj, dict) or set(obj) != {"n", "mean", "variance", "sigma"}:
            raise ControlError("invalid serialized scaler")
        return cls(**obj)


def fit_standardizer(observations: Iterable[Observation]) -> Standardizer12:
    """Welford population variance, eligible training observations only."""
    n, means, m2 = 0, [0.] * CHANNELS, [0.] * CHANNELS
    for observation in observations:
        n += 1
        for j, value in enumerate(_features(observation)):
            delta = _finite(value - means[j])
            means[j] = _finite(means[j] + delta / n)
            m2[j] = _finite(m2[j] + delta * (value - means[j]))
    if n < 2:
        raise ControlError("insufficient scaler observations")
    variance = tuple(_finite(value / n) for value in m2)
    if any(value <= 0 for value in variance):
        raise ControlError("constant channel or nonpositive variance")
    return Standardizer12(n, tuple(means), variance, tuple(math.sqrt(x) for x in variance))


def _solve_spd(matrix: list[list[float]], target: list[float]) -> tuple[float, ...]:
    """Deterministic Cholesky; no inverse, numerical fallback or hidden jitter."""
    size = len(target)
    lower = [[0.] * size for _ in range(size)]
    for i in range(size):
        for j in range(i + 1):
            residual = _finite(matrix[i][j] - math.fsum(lower[i][k] * lower[j][k]
                                                       for k in range(j)))
            if i == j:
                if residual <= 0:
                    raise ControlError("ridge normal equations not positive definite")
                lower[i][j] = math.sqrt(residual)
            else:
                lower[i][j] = _finite(residual / lower[j][j])
    intermediate = [0.] * size
    for i in range(size):
        intermediate[i] = _finite((target[i] - math.fsum(lower[i][j] * intermediate[j]
                                                        for j in range(i))) / lower[i][i])
    solution = [0.] * size
    for i in reversed(range(size)):
        solution[i] = _finite((intermediate[i] - math.fsum(lower[j][i] * solution[j]
                                                         for j in range(i + 1, size))) / lower[i][i])
    return tuple(solution)


@dataclass(frozen=True, slots=True)
class ARReference:
    scaler: Standardizer12
    order: int
    ridge: float
    n: int
    coefficients: tuple[tuple[float, ...], ...]

    def __post_init__(self):
        if not isinstance(self.scaler, Standardizer12):
            raise ControlError("invalid scaler")
        _positive_int(self.order, "AR order")
        _positive_int(self.n, "AR training targets", self.order + 1)
        ridge = _finite(self.ridge)
        if ridge <= 0:
            raise ControlError("ridge must be positive")
        object.__setattr__(self, "ridge", ridge)
        if len(self.coefficients) != CHANNELS:
            raise ControlError("invalid AR coefficient channel count")
        object.__setattr__(self, "coefficients", tuple(_vector(row, self.order + 1)
                                                       for row in self.coefficients))

    def to_dict(self):
        return {"kind": "channelwise_ar", "scaler": self.scaler.to_dict(), "order": self.order,
                "ridge": self.ridge, "n": self.n,
                "coefficients": [list(row) for row in self.coefficients]}

    @classmethod
    def from_dict(cls, obj):
        if not isinstance(obj, dict) or set(obj) != {"kind", "scaler", "order", "ridge", "n", "coefficients"} or obj["kind"] != "channelwise_ar":
            raise ControlError("invalid serialized AR reference")
        return cls(Standardizer12.from_dict(obj["scaler"]), obj["order"], obj["ridge"],
                   obj["n"], tuple(tuple(row) for row in obj["coefficients"]))


class ARAccumulator:
    """Per-channel average Gram sufficient statistics, with unpenalized intercept."""
    def __init__(self, scaler: Standardizer12, order: int):
        if not isinstance(scaler, Standardizer12):
            raise ControlError("invalid scaler")
        self.scaler, self.order = scaler, _positive_int(order, "AR order")
        self.n = 0
        size = order + 1
        self.gram = [[[0.] * size for _ in range(size)] for _ in range(CHANNELS)]
        self.cross = [[0.] * size for _ in range(CHANNELS)]
        self.history = deque(maxlen=order)

    def observe(self, observation: Observation, eligible: bool):
        if type(eligible) is not bool:
            raise ControlError("eligibility must be boolean")
        _delta(observation)
        if observation.dt is None:
            self.history.clear()
        values = self.scaler.transform(observation)
        if eligible:
            if len(self.history) < self.order:
                raise ControlError("eligible AR target has insufficient history")
            self.n += 1
            past = tuple(reversed(self.history))
            for channel, target in enumerate(values):
                design = (1.,) + tuple(row[channel] for row in past)
                gram, cross = self.gram[channel], self.cross[channel]
                for i, x in enumerate(design):
                    cross[i] = _finite(cross[i] + x * target)
                    for j in range(i + 1):
                        gram[i][j] = _finite(gram[i][j] + x * design[j])
        self.history.append(values)

    def finish(self, ridge: float) -> ARReference:
        ridge = _finite(ridge)
        if ridge <= 0 or self.n < self.order + 1:
            raise ControlError("invalid ridge or insufficient AR targets")
        size, coefficients = self.order + 1, []
        for gram, cross in zip(self.gram, self.cross):
            matrix = [[gram[max(i, j)][min(i, j)] / self.n +
                       (ridge if i == j and i > 0 else 0.)
                       for j in range(size)] for i in range(size)]
            coefficients.append(_solve_spd(matrix, [value / self.n for value in cross]))
        return ARReference(self.scaler, self.order, ridge, self.n, tuple(coefficients))


class ARDetector:
    def __init__(self, reference: ARReference):
        if not isinstance(reference, ARReference):
            raise ControlError("invalid AR reference")
        self.reference = reference
        self.history = deque(maxlen=reference.order)

    def reset(self):
        self.history.clear()

    def predict(self, observation: Observation) -> tuple[float, ...] | None:
        _features(observation)
        _delta(observation)
        if observation.dt is None or len(self.history) < self.reference.order:
            return None
        past = tuple(reversed(self.history))
        return tuple(_finite(weights[0] + math.fsum(weights[k + 1] * past[k][j]
                                                  for k in range(self.reference.order)))
                     for j, weights in enumerate(self.reference.coefficients))

    def score(self, observation: Observation) -> float | None:
        prediction = self.predict(observation)
        return None if prediction is None else _mse(self.reference.scaler.transform(observation), prediction)

    def update(self, observation: Observation):
        _delta(observation)
        if observation.dt is None:
            self.reset()
        self.history.append(self.reference.scaler.transform(observation))


def _mse(values, prediction) -> float:
    try:
        result = math.fsum((x - p) ** 2 for x, p in zip(values, prediction)) / CHANNELS
    except (OverflowError, ValueError) as exc:
        raise ControlError("nonfinite squared residual") from exc
    return _finite(result, "nonfinite squared residual")


@dataclass(frozen=True, slots=True)
class PeriodEstimate:
    period_seconds: float
    lag: int
    stride: int
    sampled_observations: int
    objective: float
    local_minima: tuple[tuple[int, float], ...]
    prefix_observations: int
    sampled_elapsed_seconds: float
    lag_objectives: tuple[tuple[int, float], ...]

    def to_dict(self):
        return {"period_seconds": self.period_seconds, "lag": self.lag, "stride": self.stride,
                "sampled_observations": self.sampled_observations, "objective": self.objective,
                "local_minima": [list(pair) for pair in self.local_minima],
                "prefix_observations": self.prefix_observations,
                "sampled_elapsed_seconds": self.sampled_elapsed_seconds,
                "lag_objectives": [list(pair) for pair in self.lag_objectives]}


def estimate_period(observations: Iterable[Observation], scaler: Standardizer12,
                    *, stride: int = 20, min_lag: int = 2, max_lag: int = 120,
                    max_observations: int = 20000) -> PeriodEstimate:
    """Training-only eligible continuous prefix; local lag-distance minima.

    The first provided observation anchors elapsed zero; a subsequent dt=None
    ends the prefix. Read no more than max_observations. Minima use neighbors on
    both sides, including lag min_lag-1 and max_lag+1. A plateau requires at least
    one strict side. Tie breaking is (objective, lag), never development labels.
    """
    _positive_int(stride, "period stride")
    _positive_int(min_lag, "minimum lag", 2)
    _positive_int(max_lag, "maximum lag", min_lag)
    _positive_int(max_observations, "prefix limit")
    sampled, times, elapsed, consumed = [], [], 0., 0
    iterator = iter(observations)
    for i in range(max_observations):
        try:
            observation = next(iterator)
        except StopIteration:
            break
        if i and observation.dt is None:
            break
        consumed += 1
        delta = _delta(observation)
        elapsed = _finite(elapsed + (delta if i else 0.))
        values = scaler.transform(observation)
        if i % stride == 0:
            sampled.append(values)
            times.append(elapsed)
    if len(sampled) < 4 * max_lag + 1:
        raise ControlError("insufficient continuous eligible period prefix")
    objectives = {}
    for lag in range(min_lag - 1, max_lag + 2):
        objectives[lag] = math.fsum(_mse(sampled[i], sampled[i - lag])
                                    for i in range(lag, len(sampled))) / (len(sampled) - lag)
    minima = tuple((lag, objectives[lag]) for lag in range(min_lag, max_lag + 1)
                   if objectives[lag] <= objectives[lag - 1] and objectives[lag] <= objectives[lag + 1]
                   and (objectives[lag] < objectives[lag - 1] or objectives[lag] < objectives[lag + 1]))
    if not minima:
        raise ControlError("no interior periodic lag minimum")
    lag, objective = min(minima, key=lambda pair: (pair[1], pair[0]))
    seconds = math.fsum(times[i] - times[i - lag] for i in range(lag, len(times))) / (len(times) - lag)
    return PeriodEstimate(_finite(seconds), lag, stride, len(sampled), objective, minima,
                          consumed, times[-1] - times[0], tuple(objectives.items()))


@dataclass(frozen=True, slots=True)
class TemplateReference:
    scaler: Standardizer12
    period_seconds: float
    bins: int
    initialization: int
    n: int
    means: tuple[tuple[float, ...], ...]
    counts: tuple[int, ...]

    def __post_init__(self):
        if not isinstance(self.scaler, Standardizer12):
            raise ControlError("invalid scaler")
        period = _finite(self.period_seconds)
        if period <= 0:
            raise ControlError("invalid nominal period")
        object.__setattr__(self, "period_seconds", period)
        _positive_int(self.bins, "phase bins", 2)
        _positive_int(self.initialization, "phase initialization")
        _positive_int(self.n, "template target count", self.bins)
        if len(self.means) != self.bins or len(self.counts) != self.bins:
            raise ControlError("invalid template shape")
        object.__setattr__(self, "means", tuple(_vector(row) for row in self.means))
        object.__setattr__(self, "counts", tuple(self.counts))
        if any(type(n) is not int or n < 1 for n in self.counts) or sum(self.counts) != self.n:
            raise ControlError("unseen phase bin or invalid bin counts")

    def to_dict(self):
        return {"kind": "nominal_periodic_template", "scaler": self.scaler.to_dict(),
                "period_seconds": self.period_seconds, "bins": self.bins,
                "initialization": self.initialization, "n": self.n,
                "means": [list(row) for row in self.means], "counts": list(self.counts)}

    @classmethod
    def from_dict(cls, obj):
        if not isinstance(obj, dict) or set(obj) != {"kind", "scaler", "period_seconds", "bins", "initialization", "n", "means", "counts"} or obj["kind"] != "nominal_periodic_template":
            raise ControlError("invalid serialized template")
        return cls(Standardizer12.from_dict(obj["scaler"]), obj["period_seconds"], obj["bins"],
                   obj["initialization"], obj["n"], tuple(tuple(row) for row in obj["means"]),
                   tuple(obj["counts"]))


def _phase(elapsed: float, period: float, bins: int) -> int:
    return int((elapsed % period) / period * bins) % bins


def _template_from_sums(scaler, period, bins, initialization, sums, counts):
    if any(n == 0 for n in counts):
        raise ControlError("unseen phase bin")
    return TemplateReference(scaler, period, bins, initialization, sum(counts),
                             tuple(tuple(_finite(value / n) for value in row)
                                   for row, n in zip(sums, counts)), tuple(counts))


def fit_template_seed(observations: Iterable[Observation], scaler: Standardizer12,
                      period_seconds: float, bins: int, *, initialization: int = 1528) -> TemplateReference:
    """Bootstrap bin means from eligible first-segment training observations only."""
    _positive_int(bins, "phase bins", 2)
    period_seconds = _finite(period_seconds)
    if period_seconds <= 0:
        raise ControlError("invalid nominal period")
    sums, counts, elapsed = [[0.] * CHANNELS for _ in range(bins)], [0] * bins, 0.
    for i, observation in enumerate(observations):
        if i and observation.dt is None:
            break
        delta = _delta(observation)
        elapsed = _finite(elapsed + (delta if i else 0.))
        phase = _phase(elapsed, period_seconds, bins)
        values = scaler.transform(observation)
        counts[phase] += 1
        for j, value in enumerate(values):
            sums[phase][j] = _finite(sums[phase][j] + value)
    return _template_from_sums(scaler, period_seconds, bins, initialization, sums, counts)


class TemplateDetector:
    """Warmup phase estimation, then fixed nominal time progression.

    During initialization only, sum residuals for every integer bin offset.
    After exactly initialization updates freeze argmin(loss, offset). No arriving
    scored observation can change phase, nominal period or fitted template.
    """
    def __init__(self, reference: TemplateReference):
        if not isinstance(reference, TemplateReference):
            raise ControlError("invalid template reference")
        self.reference = reference
        self.reset()

    def reset(self):
        self.elapsed = 0.
        self.seen = 0
        self.offset = None
        self.losses = [0.] * self.reference.bins

    def phase_for(self, observation: Observation) -> int | None:
        _features(observation)
        delta = _delta(observation)
        if observation.dt is None or self.offset is None:
            return None
        return (_phase(_finite(self.elapsed + delta), self.reference.period_seconds,
                       self.reference.bins) + self.offset) % self.reference.bins

    def predict(self, observation: Observation) -> tuple[float, ...] | None:
        phase = self.phase_for(observation)
        return None if phase is None else self.reference.means[phase]

    def score(self, observation: Observation) -> float | None:
        prediction = self.predict(observation)
        return None if prediction is None else _mse(self.reference.scaler.transform(observation), prediction)

    def update(self, observation: Observation):
        delta = _delta(observation)
        if observation.dt is None:
            self.reset()
        values = self.reference.scaler.transform(observation)
        self.elapsed = _finite(self.elapsed + (delta if self.seen else 0.))
        if self.offset is None:
            phase = _phase(self.elapsed, self.reference.period_seconds, self.reference.bins)
            for offset in range(self.reference.bins):
                loss = _mse(values, self.reference.means[(phase + offset) % self.reference.bins])
                self.losses[offset] = _finite(self.losses[offset] + loss)
        self.seen += 1
        if self.offset is None and self.seen == self.reference.initialization:
            self.offset = min(range(self.reference.bins), key=lambda k: (self.losses[k], k))


class TemplateAccumulator:
    """Fit all eligible targets after training-segment warmup alignment to seed."""
    def __init__(self, seed: TemplateReference):
        self.seed = seed
        self.detector = TemplateDetector(seed)
        self.sums = [[0.] * CHANNELS for _ in range(seed.bins)]
        self.counts = [0] * seed.bins

    def observe(self, observation: Observation, eligible: bool):
        if type(eligible) is not bool:
            raise ControlError("eligibility must be boolean")
        phase = self.detector.phase_for(observation)
        if eligible:
            if phase is None:
                raise ControlError("eligible template target not initialized")
            values = self.seed.scaler.transform(observation)
            self.counts[phase] += 1
            for j, value in enumerate(values):
                self.sums[phase][j] = _finite(self.sums[phase][j] + value)
        self.detector.update(observation)

    def finish(self) -> TemplateReference:
        return _template_from_sums(self.seed.scaler, self.seed.period_seconds, self.seed.bins,
                                   self.seed.initialization, self.sums, self.counts)
