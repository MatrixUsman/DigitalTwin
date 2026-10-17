"""Causal synthetic measurement replay and fixed evidence scores; no fitting."""
import math
import numpy as np


def cases(config):
    result = []
    settings = [("hold", a) for a in config["hold_fractions"]]
    settings += [("slow", a) for a in config["playback_rates"]]
    settings += [("bias", a) for a in config["gyro_x_biases"]]
    for family, magnitude in settings:
        for duration in config["durations"]:
            for onset in config["onsets"]:
                result.append(dict(id=f"case{len(result):03d}", family=family,
                                   magnitude=magnitude, duration=duration, onset=onset))
    return result


def perturb(values, onset, duration, family, magnitude):
    """Coordinates here refer to observations, not target indices. Never mutate input."""
    values = np.asarray(values)
    if (values.ndim != 2 or values.shape[1] != 9 or not np.isfinite(values).all()
            or onset < 1 or duration < 1 or onset + duration > len(values)
            or not np.isfinite(magnitude)):
        raise ValueError("Invalid synthetic replay")
    out = values.copy(); stop = onset + duration
    if family == "hold" and 0 <= magnitude <= 1:
        out[onset:stop] = (1 - magnitude) * values[onset:stop] + magnitude * values[onset - 1]
    elif family == "slow" and 0 < magnitude <= 1:
        source = onset - 1 + magnitude * (np.arange(duration) + 1)
        lo, hi = np.floor(source).astype(int), np.ceil(source).astype(int)
        fraction = (source - lo)[:, None]
        out[onset:stop] = (1 - fraction) * values[lo] + fraction * values[hi]
    elif family == "bias":
        out[onset:stop, 3] += magnitude
    else:
        raise ValueError("Unknown family or invalid magnitude")
    if not np.isfinite(out).all(): raise ValueError("Nonfinite synthetic replay")
    return out


def rolling_mean(energy, width):
    x = np.asarray(energy, dtype=np.float64)
    if x.ndim != 1 or not len(x) or width < 1 or not np.isfinite(x).all():
        raise ValueError("Invalid moving average")
    total = np.r_[0., np.cumsum(x)]
    end = np.arange(1, len(x) + 1); start = np.maximum(0, end - width)
    return (total[end] - total[start]) / (end - start)


def accumulate(energy, normal_mean, drift, cap):
    x = np.asarray(energy, dtype=np.float64)
    if (x.ndim != 1 or not len(x) or not np.isfinite(x).all() or np.any(x < 0)
            or not np.isfinite([normal_mean, drift, cap]).all()
            or normal_mean <= 0 or drift <= 0 or cap <= drift):
        raise ValueError("Invalid accumulator")
    total = np.cumsum(np.minimum(x / normal_mean, cap) - drift)
    return total - np.minimum.accumulate(np.minimum(total, 0.))


def score_streams(energy, normal_mean, config):
    x = np.asarray(energy, dtype=np.float64)
    if x.ndim != 1 or not np.isfinite(x).all() or np.any(x < 0):
        raise ValueError("Invalid residual energy")
    return np.column_stack([x, rolling_mean(x, 45), rolling_mean(x, 450),
                            accumulate(x, normal_mean, config["cusum_drift"],
                                       config["cusum_increment_cap"])])


def calibrate(streams, start, stop, quantile):
    values = np.asarray(streams, dtype=np.float64)
    if (values.ndim != 2 or not 0 <= start < stop <= len(values)
            or not 0 < quantile <= 1 or not np.isfinite(values[start:stop]).all()):
        raise ValueError("Invalid calibration")
    rank = math.ceil(quantile * (stop - start))
    return np.sort(values[start:stop], axis=0)[rank - 1], rank


def normal_metrics(alarm, start, stop):
    a = np.asarray(alarm, dtype=bool)
    rises = a & ~np.r_[False, a[:-1]]
    return {"observations": stop - start, "alarm_points": int(a[start:stop].sum()),
            "alarm_fraction": float(a[start:stop].mean()),
            "episodes": int(rises[start:stop].sum()),
            "episodes_per_1000": float(rises[start:stop].sum() * 1000 / (stop - start)),
            "active_at_start": bool(a[start])}


def event_metrics(alarm, onset, duration, evaluation_start, evaluation_stop, post_window):
    a = np.asarray(alarm, dtype=bool); end = onset + duration
    if not 0 <= evaluation_start <= onset < end <= evaluation_stop <= len(a):
        raise ValueError("Event outside declared evaluation")
    event = a[onset:end]; rises = a & ~np.r_[False, a[:-1]]
    hits = np.flatnonzero(event); fresh = np.flatnonzero(rises[onset:end])
    tp = int(event.sum()); fp = int(a[evaluation_start:evaluation_stop].sum()) - tp
    fn = duration - tp; precision = tp / (tp + fp) if tp + fp else 0.
    recall = tp / duration
    post = a[end:min(evaluation_stop, end + post_window)]
    clears = np.flatnonzero(~post)
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall,
            "f1": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.,
            "overlap_hit": bool(len(hits)), "overlap_delay": int(hits[0]) if len(hits) else None,
            "fresh_hit": bool(len(fresh)), "fresh_delay": int(fresh[0]) if len(fresh) else None,
            "active_before_event": bool(a[onset - 1]) if onset else False,
            "pre_event_alarm_points": int(a[evaluation_start:onset].sum()),
            "post_alarm_points": int(post.sum()), "post_observations": len(post),
            "first_clear_delay": int(clears[0]) if len(clears) else None,
            "first_clear_censored": not bool(len(clears)),
            "event_alarm_episodes": int(rises[onset:end].sum())}


def error_summary(actual, oracle, duration):
    width = min(duration, 45)
    early = float(np.mean(actual[:width])); late = float(np.mean(actual[duration - width:duration]))
    oracle_early = float(np.mean(oracle[:width])); oracle_late = float(np.mean(oracle[duration - width:duration]))
    return {"early_mse": early, "late_mse": late, "oracle_early_mse": oracle_early,
            "oracle_late_mse": oracle_late,
            "late_to_early": late / early if early > 0 else None,
            "late_to_oracle": late / oracle_late if oracle_late > 0 else None,
            "early_late_overlap": duration < 90}
