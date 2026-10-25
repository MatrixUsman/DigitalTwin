"""Causal endpoint estimates from joint position/velocity consistency.

This is standard weighted polynomial estimation, not a novelty claim.
Inputs are observations only; no attack labels, true state or counterfactual.
"""
import numpy as np


def endpoint_operator(window, dt, variance_q, variance_v, coupled=True):
    if not isinstance(window, int) or window < 3 or not np.isfinite(dt) or dt <= 0:
        raise ValueError('At least three past/current samples and positive dt required')
    variance = np.asarray([variance_q, variance_v], dtype=float)
    if not np.isfinite(variance).all() or np.any(variance <= 0):
        raise ValueError('Strictly positive finite measurement variances required')
    tau = np.arange(1 - window, 1, dtype=float) * dt
    hq = np.column_stack([np.ones(window), tau, tau * tau / 2])
    hv = np.column_stack([np.zeros(window), np.ones(window), tau])
    if coupled:
        h = np.vstack([hq, hv])
        whiten = np.repeat(1 / np.sqrt(variance), window)
        operator = np.linalg.pinv(h * whiten[:, None]) * whiten[None, :]
        return operator[:2]
    # Same polynomial orders as the coupled model, without derivative coupling.
    operator = np.zeros((2, 2 * window))
    operator[0, :window] = np.linalg.pinv(hq)[0]
    operator[1, window:] = np.linalg.pinv(hv[:, 1:])[0]
    return operator


def estimate(observations, variances, window, dt=.02, coupled=True):
    """Return [q1,q2,v1,v2] endpoints and a readiness mask; prefix is unready."""
    y = np.asarray(observations, dtype=float)
    var = np.asarray(variances, dtype=float)
    if y.ndim != 2 or y.shape[1] != 4 or var.shape != (4,):
        raise ValueError('Expected four position/velocity channels and variances')
    if not np.isfinite(y).all():
        raise ValueError('Nonfinite observations are not admitted')
    out = y.copy()
    ready = np.arange(len(y)) >= window - 1
    for joint in range(2):
        op = endpoint_operator(window, dt, var[joint], var[joint + 2], coupled)
        for t in range(window - 1, len(y)):
            history = y[t - window + 1:t + 1]
            out[t, [joint, joint + 2]] = op @ np.r_[history[:, joint], history[:, joint + 2]]
    return out, ready


def estimate_noise(training_sequences):
    """Robust second-difference scale, fitted on training observations only.

    Median absolute second differences divided by sqrt(6) estimate iid noise
    scale under locally affine motion. Curvature/noise correlation invalidate
    an exact variance interpretation; this is an explicit working estimate.
    """
    differences = []
    for sequence in training_sequences:
        y = np.asarray(sequence, dtype=float)
        if y.ndim != 2 or y.shape[1] != 4 or len(y) < 3 or not np.isfinite(y).all():
            raise ValueError('Invalid training sequence')
        differences.append(np.diff(y, n=2, axis=0))
    if not differences:
        raise ValueError('No training observations')
    d = np.concatenate(differences)
    sigma = np.median(np.abs(d - np.median(d, axis=0)), axis=0) / (.6744897501960817 * np.sqrt(6))
    if not np.isfinite(sigma).all() or np.any(sigma <= 0):
        raise ValueError('Degenerate scale; do not invent a positive channel variance')
    return sigma ** 2
