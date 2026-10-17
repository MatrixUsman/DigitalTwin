"""Label-free command-envelope entry and independent physical-return evidence."""
import numpy as np
from support import scaled_plant
from plant import advance
from observer import errors, scores

def trajectory(initial, command, p, cfg):
    state = np.empty((len(command), 4)); state[0] = initial
    for t in range(len(command)-1):
        state[t+1] = advance(state[t], command[t], p, cfg)
    return state

def bank_predictions(context, cfg):
    initial = np.r_[0., cfg['amplitude'][1]*np.sin(cfg['phase_offset']), 0., 0.]
    return np.stack([trajectory(initial, context, scaled_plant(cfg, *f), cfg)
                     for f in cfg['bank']], axis=1)

def following_predictions(y, context, cfg):
    state = np.empty_like(y)
    state[0] = np.r_[0., cfg['amplitude'][1]*np.sin(cfg['phase_offset']), 0., 0.]
    gain = np.asarray(cfg['observer_gain'])
    for t in range(len(y)-1):
        state[t+1] = advance(state[t]+gain*(y[t]-state[t]), context[t], cfg['nominal'], cfg)
    return state

def command_mode(context, valid, cfg):
    age = cfg['mode_duration']; mode = np.zeros(len(context), dtype=int)
    for t in range(len(context)):
        if t and valid[t] and valid[t-1]:
            dq = np.max(np.abs(context[t,:2]-context[t-1,:2]-cfg['dt']*context[t-1,2:]))
            dv = np.max(np.abs(context[t,2:]-context[t-1,2:]))
            if dq > cfg['mode_position_jump'] or dv > cfg['mode_velocity_jump']: age = 0
        mode[t] = int(age < cfg['mode_duration'])
        age += 1
    return mode

def envelope_score(y, bank, sigma):
    if bank.shape != (len(y), 3, 4) or y.shape[1] != 4:
        raise ValueError('Unexpected observation/bank shape')
    sigma = np.asarray(sigma)
    if np.any(sigma <= 0) or not np.isfinite(bank).all() or not np.isfinite(y).all():
        raise ValueError('Nonfinite observation or invalid scale')
    lower, upper = bank.min(axis=1), bank.max(axis=1)
    return np.max(np.maximum(np.maximum(lower-y, y-upper), 0)/sigma, axis=1)

def components(y, context, valid, following, bank, fit, cfg):
    # The API has no true state, schedule, executed command, condition or labels.
    reference = bank[:,1]
    en = errors({'measurements':y, 'available':context}, following, reference, fit, cfg)
    base = scores(en, fit, cfg)
    env = envelope_score(y, bank, cfg['sensor_sigma'])
    return_ok = np.all(np.abs(y-reference)+cfg['noise_margin_sigma']*np.asarray(cfg['sensor_sigma'])
                       <= cfg['physical_tolerance']*fit['scale'], axis=1)
    return dict(base=base, envelope=env, return_ok=return_ok,
                mode=command_mode(context, valid, cfg), valid=valid.copy())

def score_matrix(comp, mode_scales):
    b = comp['base']; e = comp['envelope']; fused = b[:,7]
    result = np.column_stack([b[:,:6], fused, fused, fused/mode_scales[comp['mode']],
                              e, e, fused, e])
    if not np.isfinite(result).all() or np.any(result < 0): raise ValueError('Invalid score')
    return result

def stateful(score, valid, high, dwell, recovery=None):
    alarm = False; count = 0; result = np.zeros(len(score), dtype=bool)
    for t, s in enumerate(score):
        if not valid[t]: count = 0
        elif s > high: alarm = True; count = 0
        elif alarm:
            recover = bool(recovery[t]) if recovery is not None else s <= .5*high
            count = count+1 if recover else 0
            if count >= dwell: alarm = False; count = 0
        result[t] = alarm
    return result

def decision(score, method_index, valid, return_ok, high, cfg):
    unknown = ~valid if method_index >= 2 else np.zeros(len(score), dtype=bool)
    if method_index in [7,8,10,11,12]:
        recovery = return_ok if method_index in [11,12] else None
        alarm = stateful(score, valid, high, cfg['recovery_dwell'], recovery)
    else: alarm = score > high
    return alarm, unknown

def calibrate(episodes, j, cfg):
    # The candidate grid includes warmup scores, so a zero-alarm endpoint exists.
    candidates = np.unique(np.r_[0., np.concatenate([e['scores'][:,j] for e in episodes])])
    cache = {}
    def count(i):
        if i not in cache:
            cache[i] = int(sum(np.count_nonzero((decision(e['scores'][:,j], j, e['valid'], e['return_ok'],
                candidates[i], cfg)[0] & ~decision(e['scores'][:,j], j, e['valid'], e['return_ok'],
                candidates[i], cfg)[1])[cfg['warmup']:]) for e in episodes))
        return cache[i]
    lo, hi = 0, len(candidates)-1
    if count(hi) > cfg['calibration_alarm_budget']: raise ValueError('No feasible threshold')
    while lo < hi:
        mid = (lo+hi)//2
        if count(mid) <= cfg['calibration_alarm_budget']: hi = mid
        else: lo = mid+1
    if lo and count(lo-1) <= cfg['calibration_alarm_budget']: raise ValueError('Threshold not minimal')
    return dict(threshold=float(candidates[lo]), index=int(lo), grid_size=len(candidates),
                alarms=count(lo), preceding_alarms=count(lo-1) if lo else None,
                probes=[dict(index=int(i),threshold=float(candidates[i]),alarms=n) for i,n in sorted(cache.items())])
