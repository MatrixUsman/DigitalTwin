"""Explicitly synthetic normal residual generator and descriptive evaluation."""
import numpy as np
from control import Contract, upper_bounds, certificate


def catalog(c):
    return [dict(id=f'{ns["id"]}_{p["id"]}_s{seed}', noise=ns, profile=p, seed=seed)
            for ns in c['noise_settings'] for p in c['profiles'] for seed in c['seeds']]


def contract_for(c, row):
    ns, p = row['noise'], row['profile']
    drift = 2*p['amplitude']*abs(np.sin(p['frequency']/2))
    return Contract(tuple(ns['sigma']*np.asarray(c['sigma_multipliers'])), (ns['rho'],)*4,
                    tuple(c['bias_bound']), (float(drift),)*4, tuple(c['tolerance']),
                    tuple(c['windows']), c['alpha'])


def generate(c, row):
    """No real or simulated robot dynamics. Same innovations across settings."""
    n = c['samples']; con = contract_for(c, row)
    t = np.arange(n)[:, None]; phase = np.asarray(c['phases'])[None, :]
    p = row['profile']; delta = p['amplitude']*np.sin(p['frequency']*t+phase)
    bias = np.asarray(c['bias_bound'])*np.cos(0.003*t+phase)
    z = np.random.default_rng(row['seed']).normal(size=(n, 4))
    sigma, rho = np.asarray(con.sigma), np.asarray(con.rho)
    noise = np.empty_like(z); noise[0] = sigma*z[0]
    for i in range(1, n):
        noise[i] = rho*noise[i-1] + sigma*np.sqrt(1-rho*rho)*z[i]
    residual = delta+bias+noise
    return dict(residual=residual, delta=delta, bias=bias, noise=noise, valid=np.ones(n, dtype=bool))


def score(residual, valid, con):
    """Only permitted detector inputs; truth is not passed to this function."""
    correct = upper_bounds(residual, valid, con)
    wrong = upper_bounds(residual, valid, con, assume_iid=True)
    result = {f'fixed_{m}': u for m, u in correct.items()}
    result['multiwindow'] = certificate(correct, con.tolerance)[0]
    result.update({f'iid_assumption_{m}': wrong[m] for m in con.windows if m != 1})
    return result


def evaluate(c, row, truth, scores):
    start = max(c['windows'])-1; tol = np.asarray(c['tolerance']); records = []
    for method, bound in scores.items():
        selected = bound[start:]
        if not np.all(np.isfinite(selected)):
            raise ValueError('incomplete common support')
        yes = np.all(selected <= tol, axis=1)
        violation = np.abs(truth[start:]) > selected + 1e-12
        points = np.flatnonzero(yes)
        records.append(dict(trace=row['id'], noise=row['noise']['id'], profile=row['profile']['id'], seed=row['seed'],
                            method=method, eligible=len(yes), certified=int(yes.sum()), fraction=float(yes.mean()),
                            coverage_violation_channels=int(violation.sum()), any_coverage_violation=bool(violation.any()),
                            first_certificate_sample=int(points[0]+start+1) if len(points) else None,
                            assumptions_satisfied=not(method.startswith('iid_assumption') and row['noise']['rho']>0),
                            feasibility_pass=bool(yes.mean() >= c['feasibility_fraction'])))
    return records
