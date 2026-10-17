"""Standard Gaussian window bounds for CURRENT deviation; no fitted model or I/O."""
from dataclasses import dataclass
import math
import numpy as np


def positive_integer(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < 1:
        raise ValueError(name + ' must be a positive integer')
    return int(value)


@dataclass(frozen=True)
class Contract:
    sigma: tuple
    rho: tuple
    bias: tuple
    drift: tuple
    tolerance: tuple
    windows: tuple = (1, 41, 201)
    alpha: float = 0.05

    def __post_init__(self):
        size = None
        for name in ('sigma', 'rho', 'bias', 'drift', 'tolerance'):
            a = np.asarray(getattr(self, name), dtype=float)
            if a.ndim != 1 or a.size == 0 or not np.all(np.isfinite(a)) or np.any(a < 0):
                raise ValueError('invalid ' + name)
            if size is not None and len(a) != size:
                raise ValueError('channel dimensions differ')
            size = len(a)
            object.__setattr__(self, name, tuple(a.tolist()))
        if any(r >= 1 for r in self.rho) or any(t <= 0 for t in self.tolerance):
            raise ValueError('rho must be <1 and tolerance positive')
        ws = tuple(positive_integer(w, 'window') for w in self.windows)
        if not ws or len(set(ws)) != len(ws) or tuple(sorted(ws)) != ws:
            raise ValueError('windows must be increasing and unique')
        object.__setattr__(self, 'windows', ws)
        if isinstance(self.alpha, bool) or not math.isfinite(self.alpha) or not 0 < self.alpha < 1:
            raise ValueError('alpha must be in (0,1)')


def mean_variance(sigma, rho, window):
    """Exact variance for known stationary Gaussian AR(1), rho in [0,1)."""
    m = positive_integer(window, 'window')
    s, r = np.asarray(sigma, float), np.asarray(rho, float)
    if s.ndim != 1 or r.shape != s.shape or s.size == 0 or not np.all(np.isfinite(s + r)):
        raise ValueError('invalid noise vectors')
    if np.any(s < 0) or np.any(r < 0) or np.any(r >= 1):
        raise ValueError('invalid noise contract')
    k = np.arange(1, m, dtype=float)[:, None]
    return s*s*(m + 2*np.sum((m-k)*r[None, :]**k, axis=0))/(m*m)


def upper_bounds(residuals, valid, contract, *, global_start=1, assume_iid=False):
    """Return {m: [N,d] upper bound}. Incomplete/invalid windows are +infinity.

    rho=0 override is an explicitly misspecified diagnostic for correlated input.
    Time and all registered windows retain the same risk allocation in that control.
    No truth, attack label, reference adaptation, clock reset or window tuning.
    """
    start = positive_integer(global_start, 'global_start')
    e = np.asarray(residuals, dtype=float)
    ok = np.asarray(valid)
    if e.ndim != 2 or e.shape[0] < 1 or e.shape[1] != len(contract.sigma):
        raise ValueError('invalid residual shape')
    if ok.dtype != np.bool_ or ok.shape != (len(e),):
        raise ValueError('validity must be a Boolean vector')
    if not np.all(np.isfinite(e[ok])):
        raise ValueError('nonfinite valid residual')
    if start + len(e) > 2**53:
        raise ValueError('clock exceeds exact float64 integer support')
    n, d = e.shape
    t = np.arange(start, start+n, dtype=float)
    log_factor = math.log(2*d*len(contract.windows)*math.pi**2/(6*contract.alpha)) + 2*np.log(t)
    clean = np.where(ok[:, None], e, 0.0)
    prefix = np.vstack([np.zeros((1, d)), np.cumsum(clean, axis=0)])
    missing = np.r_[0, np.cumsum(~ok)]
    rho = np.zeros(d) if assume_iid else contract.rho
    result = {}
    for m in contract.windows:
        u = np.full_like(e, np.inf)
        if m <= n:
            means = (prefix[m:] - prefix[:-m])/m
            complete = (missing[m:] - missing[:-m]) == 0
            radius = np.sqrt(2*log_factor[m-1:, None]*mean_variance(contract.sigma, rho, m)[None, :])
            candidate = np.abs(means) + np.asarray(contract.bias) + radius + np.asarray(contract.drift)*(m-1)/2
            if not np.all(np.isfinite(candidate)):
                raise ValueError('nonfinite bound arithmetic')
            u[m-1:][complete] = candidate[complete]
        result[m] = u
    return result


def certificate(bounds, tolerance):
    """Intersect simultaneous upper bounds; all channels must be certified."""
    if not bounds:
        raise ValueError('empty bounds')
    arrays = [np.asarray(u, float) for u in bounds.values()]
    shape = arrays[0].shape
    if len(shape) != 2 or any(a.shape != shape or np.isnan(a).any() or np.any(a < 0) for a in arrays):
        raise ValueError('invalid bounds')
    tol = np.asarray(tolerance, float)
    if tol.shape != (shape[1],) or not np.all(np.isfinite(tol)) or np.any(tol <= 0):
        raise ValueError('invalid tolerance')
    envelope = np.minimum.reduce(arrays)
    return envelope, np.all(envelope <= tol, axis=1)
