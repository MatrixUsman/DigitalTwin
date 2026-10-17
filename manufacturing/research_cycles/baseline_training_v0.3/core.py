"""Chronological, finite, one-step normal-data training primitives."""
from dataclasses import dataclass
import numpy as np


def finite_matrix(values):
    values = np.asarray(values, dtype=np.float64)
    if values.ndim != 2 or not values.size or not np.isfinite(values).all():
        raise ValueError("Expected a nonempty finite matrix")
    return values


@dataclass(frozen=True)
class Scaler:
    mean: np.ndarray
    scale: np.ndarray

    @classmethod
    def fit(cls, training):
        training = finite_matrix(training)
        mean, scale = training.mean(axis=0), training.std(axis=0, ddof=0)
        if not np.isfinite(mean).all() or not np.isfinite(scale).all() or np.any(scale <= 0):
            raise ValueError("Constant or nonfinite training channel")
        mean.setflags(write=False)
        scale.setflags(write=False)
        return cls(mean, scale)

    def transform(self, values):
        values = finite_matrix(values)
        if values.shape[1] != len(self.mean):
            raise ValueError("Feature shape changed")
        result = ((values - self.mean) / self.scale).astype(np.float32)
        if not np.isfinite(result).all():
            raise ValueError("Nonfinite standardized data")
        result.setflags(write=False)
        return result


def eligible_endpoints(times, history, maximum_gap):
    times = np.asarray(times)
    if (times.ndim != 1 or not np.issubdtype(times.dtype, np.integer)
            or history < 1 or len(times) <= history or maximum_gap <= 0
            or not np.isfinite(maximum_gap)):
        raise ValueError("Invalid timestamp/history/gap specification")
    delta = np.diff(times)
    breaks = np.r_[False, (delta <= 0) | (delta > maximum_gap)]
    cumulative = np.cumsum(breaks)
    candidates = np.arange(history, len(times), dtype=np.int64)
    valid = cumulative[candidates] == cumulative[candidates - history]
    return candidates[valid], {
        "potential_targets": len(candidates), "eligible_targets": int(valid.sum()),
        "excluded_targets": int((~valid).sum()),
        "coverage": float(valid.mean()),
        "nonpositive_transitions": int(np.sum(delta <= 0)),
        "large_gap_transitions": int(np.sum(delta > maximum_gap)),
        "excluded_local_endpoints": candidates[~valid].tolist(),
    }


def prepare(values, times, training_rows, history, gap_multiple=5.0, minimum_coverage=0.95):
    values = finite_matrix(values)
    times = np.asarray(times)
    if (len(times) != len(values) or times.ndim != 1 or not np.issubdtype(times.dtype, np.integer)
            or training_rows <= history or len(values) - training_rows <= history
            or gap_multiple <= 0 or not 0 < minimum_coverage <= 1):
        raise ValueError("Invalid split or timestamp population")
    train_values, dev_values = values[:training_rows], values[training_rows:]
    train_times, dev_times = times[:training_rows], times[training_rows:]
    scaler = Scaler.fit(train_values)
    positive = np.diff(train_times)
    positive = positive[positive > 0]
    if not len(positive):
        raise ValueError("No positive training timestamp increments")
    median_delta = float(np.median(positive))
    maximum_gap = median_delta * gap_multiple
    train_indices, train_coverage = eligible_endpoints(train_times, history, maximum_gap)
    dev_indices, dev_coverage = eligible_endpoints(dev_times, history, maximum_gap)
    if min(train_coverage["coverage"], dev_coverage["coverage"]) < minimum_coverage:
        raise ValueError("Eligible coverage below declared admission floor")
    return {
        "scaler": scaler, "training": scaler.transform(train_values),
        "development": scaler.transform(dev_values), "training_indices": train_indices,
        "development_indices": dev_indices, "median_training_increment": median_delta,
        "maximum_gap": maximum_gap, "training_coverage": train_coverage,
        "development_coverage": dev_coverage,
    }


def batches(values, endpoints, history, batch_size):
    values = np.asarray(values)
    endpoints = np.asarray(endpoints)
    if (values.ndim != 2 or endpoints.ndim != 1 or not len(endpoints)
            or not np.issubdtype(endpoints.dtype, np.integer) or history < 1 or batch_size < 1
            or np.any(endpoints < history) or np.any(endpoints >= len(values))
            or np.any(np.diff(endpoints) <= 0)):
        raise ValueError("Invalid history/endpoints/batching")
    for first in range(0, len(endpoints), batch_size):
        selected = endpoints[first:first + batch_size]
        yield np.ascontiguousarray(values[selected[:, None] + np.arange(-history, 0)]), values[selected]


def score_predictions(predictions, targets, scale):
    predictions, targets = finite_matrix(predictions), finite_matrix(targets)
    scale = np.asarray(scale, dtype=np.float64)
    if predictions.shape != targets.shape or scale.shape != (targets.shape[1],) or not np.isfinite(scale).all() or np.any(scale <= 0):
        raise ValueError("Prediction/target/scaler mismatch")
    error_squared = (predictions - targets) ** 2
    native_squared = error_squared * scale ** 2
    if not np.isfinite(error_squared).all() or not np.isfinite(native_squared).all():
        raise ValueError("Nonfinite prediction error")
    scores = np.sqrt(error_squared.mean(axis=1))
    native_scores = np.sqrt(native_squared.mean(axis=1))
    return scores, native_scores, {
        "standardized_mse": float(error_squared.mean()),
        "native_mse": float(native_squared.mean()),
        "channel_standardized_mse": error_squared.mean(axis=0).tolist(),
        "channel_native_mse": native_squared.mean(axis=0).tolist(),
        "eligible_observations": len(targets),
    }


@dataclass
class EarlyStop:
    patience: int
    minimum_improvement: float
    best_loss: float = float("inf")
    best_epoch: int = 0
    stale_epochs: int = 0
    last_epoch: int = 0

    def __post_init__(self):
        if self.patience < 1 or self.minimum_improvement < 0 or not np.isfinite(self.minimum_improvement):
            raise ValueError("Invalid early-stop settings")

    def observe(self, epoch, loss):
        if epoch != self.last_epoch + 1 or not np.isfinite(loss) or loss < 0:
            raise ValueError("Invalid epoch/loss")
        self.last_epoch = epoch
        accepted = loss < self.best_loss - self.minimum_improvement
        if accepted:
            self.best_loss, self.best_epoch, self.stale_epochs = float(loss), epoch, 0
        else:
            self.stale_epochs += 1
        return accepted, self.stale_epochs >= self.patience


def fit_ar(values, endpoints, order=4, ridge=0.001, batch_size=1024):
    values = finite_matrix(values)
    if order < 1 or not np.isfinite(ridge) or ridge < 0:
        raise ValueError("Invalid AR configuration")
    width = order * values.shape[1] + 1
    xx, xy, n = np.zeros((width, width)), np.zeros((width, values.shape[1])), 0
    for x, y in batches(values, endpoints, order, batch_size):
        design = np.column_stack([x.reshape(len(x), -1), np.ones(len(x))])
        xx += design.T @ design
        xy += design.T @ y
        n += len(x)
    penalty = np.eye(width) * ridge
    penalty[-1, -1] = 0
    coefficients = np.linalg.solve(xx / n + penalty, xy / n)
    if not np.isfinite(coefficients).all():
        raise ValueError("Nonfinite AR coefficients")
    return coefficients


def predict_ar(values, endpoints, coefficients, order=4, batch_size=1024):
    coefficients = finite_matrix(coefficients)
    width = order * np.asarray(values).shape[1] + 1
    if coefficients.shape != (width, np.asarray(values).shape[1]):
        raise ValueError("AR coefficient shape")
    outputs = []
    for x, _ in batches(values, endpoints, order, batch_size):
        design = np.column_stack([x.reshape(len(x), -1), np.ones(len(x))])
        outputs.append(design @ coefficients)
    return np.concatenate(outputs)
