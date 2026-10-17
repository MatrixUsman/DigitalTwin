"""Frozen command-conditioned residual reference; no online fitting or truth input."""
import numpy as np


def features(reference, commands, warmup=100, lags=(1, 4, 16, 32)):
    r = np.asarray(reference, dtype=float)
    u = np.asarray(commands, dtype=float)
    if r.ndim != 2 or r.shape[1] != 4 or u.shape != r.shape:
        raise ValueError('Expected aligned four-channel arrays')
    if not np.isfinite(r).all() or not np.isfinite(u).all():
        raise ValueError('Nonfinite predictor input')
    if not lags or min(lags) < 1 or max(lags) > warmup or warmup >= len(r):
        raise ValueError('Invalid history')
    t = np.arange(warmup, len(r))
    return np.column_stack([r[t]]+[u[t-k] for k in lags])


def centers_farthest(x, count):
    if count < 1 or count > len(x):
        raise ValueError('Invalid center count')
    chosen = [int(np.argmin(np.sum(x*x, axis=1)))]
    distance = np.sum((x-x[chosen[0]])**2, axis=1)
    for _ in range(1, count):
        chosen.append(int(np.argmax(distance)))
        distance = np.minimum(distance, np.sum((x-x[chosen[-1]])**2, axis=1))
    return np.array(x[chosen], copy=True)


def basis(x, model):
    z = (np.asarray(x)-model['feature_mean'])/model['feature_scale']
    if not np.isfinite(z).all():
        raise ValueError('Nonfinite features')
    if str(model['kind']) == 'linear':
        a = z
    elif str(model['kind']) == 'rbf':
        squared = np.maximum(0., np.sum(z*z, axis=1)[:, None]
                             + np.sum(model['centers']**2, axis=1)[None, :]
                             - 2*z@model['centers'].T)
        a = np.exp(-squared/(2*float(model['width'])**2))
    else:
        raise ValueError('Unknown correction')
    return np.column_stack([a, np.ones(len(a))])


def fit(x, residual, *, kind, count=0, width_factor=1., ridge=.001):
    x = np.asarray(x, dtype=float)
    target = np.asarray(residual, dtype=float)
    if x.ndim != 2 or target.shape != (len(x), 4) or len(x) < 2:
        raise ValueError('Invalid fitting shapes')
    if not np.isfinite(x).all() or not np.isfinite(target).all() or ridge <= 0 or width_factor <= 0:
        raise ValueError('Invalid fitting values')
    mean = x.mean(0); scale = x.std(0)
    scale = np.where(scale > 1e-12, scale, 1.)
    m = dict(kind=np.array(kind), feature_mean=mean, feature_scale=scale,
             ridge=np.array(ridge), count=np.array(count), width_factor=np.array(width_factor))
    if kind == 'rbf':
        centers = centers_farthest((x-mean)/scale, count)
        dist = np.linalg.norm(centers[:, None]-centers[None, :], axis=2)
        nonzero = dist[dist > 1e-12]
        width = width_factor*(float(np.median(nonzero)) if len(nonzero) else 1.)
        m.update(centers=centers, width=np.array(width))
    design = basis(x, m)
    penalty = np.eye(design.shape[1])*ridge; penalty[-1,-1] = 0
    m['beta'] = np.linalg.solve(design.T@design/len(x)+penalty, design.T@target/len(x))
    if not np.isfinite(m['beta']).all():
        raise ValueError('Nonfinite fitted model')
    for value in m.values():
        value.flags.writeable = False
    return m


def correct(reference, commands, model, state_scale, warmup=100, lags=(1,4,16,32)):
    reference = np.asarray(reference, dtype=float)
    scale = np.asarray(state_scale, dtype=float)
    if scale.shape != (4,) or not np.isfinite(scale).all() or np.any(scale <= 0):
        raise ValueError('Invalid state scale')
    x = features(reference, commands, warmup, lags)
    result = reference.copy()
    result[warmup:] += (basis(x, model)@model['beta'])*scale
    if not np.isfinite(result).all():
        raise ValueError('Nonfinite corrected reference')
    return result


def return_evidence(residual, valid, *, windows=(5,41), tolerance=.1, start=100):
    """Heuristic normal-consistency evidence, not a physical safety certificate."""
    e = np.asarray(residual, dtype=float); valid = np.asarray(valid, dtype=bool)
    if e.ndim != 2 or e.shape[1] != 4 or valid.shape != (len(e),):
        raise ValueError('Invalid residual shape')
    if not windows or min(windows) < 1 or tolerance <= 0 or not 0 <= start < len(e):
        raise ValueError('Invalid return settings')
    if np.any(~np.isfinite(e[valid])):
        raise ValueError('Nonfinite valid observation')
    known = np.logical_and.accumulate(valid)
    result = known.copy(); result[:start] = False
    sums = np.vstack([np.zeros((1,4)), np.cumsum(np.where(valid[:,None],e,0.),axis=0)])
    for width in windows:
        eligible = np.zeros(len(e),dtype=bool)
        t = np.arange(start+width-1,len(e))
        if len(t):
            means = (sums[t+1]-sums[t-width+1])/width
            eligible[t] = np.max(np.abs(means),axis=1) <= tolerance
        result &= eligible
    return result, known


def alarm_machine(score, known, evidence, threshold, dwell=10):
    s = np.asarray(score, dtype=float); known = np.asarray(known, dtype=bool)
    evidence = np.asarray(evidence, dtype=bool)
    if s.ndim != 1 or known.shape != s.shape or evidence.shape != s.shape:
        raise ValueError('Invalid alarm input')
    if not np.isfinite(s[known]).all() or not np.isfinite(threshold) or threshold < 0 or dwell < 1:
        raise ValueError('Invalid alarm settings')
    alarm = np.zeros(len(s), dtype=bool); active = False; streak = 0
    for t in range(len(s)):
        if not known[t]:
            streak = 0; alarm[t] = active; continue
        if s[t] > threshold:
            active = True; streak = 0
        elif active:
            streak = streak+1 if evidence[t] else 0
            if streak >= dwell:
                active = False; streak = 0
        alarm[t] = active
    return alarm
