"""Fixed six-channel velocity control for the bounded normal-only pilot.

This ordinary detector is not a digital twin. The caller supplies only admitted
eligible fitting observations. No labels, dataset paths, calibration, thresholds
or online adaptation are accepted here. All arithmetic uses Python floats.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

from .data import Observation


class VelocityError(ValueError):
    """Fail-closed control diagnostic without raw observation values."""

    def __init__(self, reason: str, *, channel: int | None = None,
                 sample_count: int | None = None) -> None:
        self.reason = reason
        self.channel = channel
        self.sample_count = sample_count
        super().__init__(f"{reason}; channel={channel}; sample_count={sample_count}")


def _finite(value: object, *, reason: str, channel: int,
            sample_count: int | None = None) -> float:
    if type(value) not in (int, float):
        raise VelocityError(reason, channel=channel, sample_count=sample_count)
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise VelocityError(reason, channel=channel, sample_count=sample_count) from exc
    if not math.isfinite(result):
        raise VelocityError(reason, channel=channel, sample_count=sample_count)
    return result


def _velocities(observation: Observation, *, sample_count: int | None = None) -> tuple[float, ...]:
    if not isinstance(observation, Observation):
        raise VelocityError("expected_feature_only_observation", sample_count=sample_count)
    values = observation.qdot
    if not isinstance(values, tuple) or len(values) != 6:
        raise VelocityError("expected_six_velocity_channels", sample_count=sample_count)
    return tuple(_finite(value, reason="invalid_velocity", channel=channel,
                         sample_count=sample_count)
                 for channel, value in enumerate(values))


@dataclass(frozen=True, slots=True)
class VelocityReference:
    n: int
    mean: tuple[float, ...]
    variance: tuple[float, ...]
    sigma: tuple[float, ...]

    def __post_init__(self) -> None:
        if type(self.n) is not int or self.n < 2:
            raise VelocityError("invalid_reference_sample_count", sample_count=self.n)
        for name in ("mean", "variance", "sigma"):
            values = getattr(self, name)
            if not isinstance(values, tuple) or len(values) != 6:
                raise VelocityError(f"invalid_reference_{name}_shape", sample_count=self.n)
            normalized = tuple(_finite(value, reason=f"nonfinite_reference_{name}",
                                       channel=channel, sample_count=self.n)
                               for channel, value in enumerate(values))
            object.__setattr__(self, name, normalized)
        for channel, (variance, sigma) in enumerate(zip(self.variance, self.sigma)):
            if variance <= 0:
                raise VelocityError("nonpositive_variance", channel=channel, sample_count=self.n)
            if sigma <= 0:
                raise VelocityError("nonpositive_sigma", channel=channel, sample_count=self.n)
            if sigma != math.sqrt(variance):
                raise VelocityError("sigma_variance_mismatch", channel=channel, sample_count=self.n)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-safe copy; mutations of the copy cannot alter the fit."""
        return {"n": self.n, "mean": list(self.mean),
                "variance": list(self.variance), "sigma": list(self.sigma)}


def fit_velocity(observations: Iterable[Observation]) -> VelocityReference:
    """Fit one-pass Welford means and population variances M2/n.

    The caller, not this feature-only function, enforces the allowed row ranges
    and structural eligibility. Every intermediate update must remain finite.
    Zero/negative variance fails with its channel; there is no epsilon, clipping,
    channel deletion, development-data fitting, or fallback estimator.
    """
    count = 0
    means = [0.0] * 6
    m2 = [0.0] * 6
    for observation in observations:
        count += 1
        values = _velocities(observation, sample_count=count)
        for channel, value in enumerate(values):
            delta = _finite(value - means[channel], reason="nonfinite_welford_delta",
                            channel=channel, sample_count=count)
            updated_mean = _finite(means[channel] + delta / count,
                                   reason="nonfinite_welford_mean",
                                   channel=channel, sample_count=count)
            delta_after = _finite(value - updated_mean, reason="nonfinite_welford_delta_after",
                                  channel=channel, sample_count=count)
            increment = _finite(delta * delta_after, reason="nonfinite_welford_increment",
                                channel=channel, sample_count=count)
            updated_m2 = _finite(m2[channel] + increment, reason="nonfinite_welford_m2",
                                 channel=channel, sample_count=count)
            if updated_m2 < 0:
                raise VelocityError("negative_welford_m2", channel=channel, sample_count=count)
            means[channel] = updated_mean
            m2[channel] = updated_m2
    if count == 0:
        raise VelocityError("empty_fit", sample_count=0)
    variances = []
    sigmas = []
    for channel, accumulated in enumerate(m2):
        variance = _finite(accumulated / count, reason="nonfinite_variance",
                           channel=channel, sample_count=count)
        if variance <= 0:
            raise VelocityError("nonpositive_variance", channel=channel, sample_count=count)
        sigma = _finite(math.sqrt(variance), reason="nonfinite_sigma",
                        channel=channel, sample_count=count)
        if sigma <= 0:
            raise VelocityError("nonpositive_sigma", channel=channel, sample_count=count)
        variances.append(variance)
        sigmas.append(sigma)
    return VelocityReference(count, tuple(means), tuple(variances), tuple(sigmas))


@dataclass(frozen=True, slots=True)
class VelocityDetector:
    reference: VelocityReference

    def __post_init__(self) -> None:
        if not isinstance(self.reference, VelocityReference):
            raise VelocityError("invalid_velocity_reference")

    def reset(self) -> None:
        """No dynamic state exists; the fitted reference remains fixed."""

    def score(self, observation: Observation) -> float:
        values = _velocities(observation)
        maximum = 0.0
        for channel, (value, mean, sigma) in enumerate(zip(values, self.reference.mean,
                                                        self.reference.sigma)):
            difference = _finite(value - mean, reason="nonfinite_score_difference", channel=channel)
            z = _finite(difference / sigma, reason="nonfinite_standardized_score", channel=channel)
            maximum = max(maximum, abs(z))
        return maximum

    def update(self, observation: Observation) -> None:
        """Deliberate no-op: scoring observations never modify the reference."""
