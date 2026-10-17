"""Versioned identities and immutable v0.5 numerical dependencies."""
import hashlib
import io
import json
from pathlib import Path
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
OLD = HERE.parent / 'recovery_v0.5'
OLD_RUN = PROJECT / 'local/recovery_v0.5/runs/simulation_001'
LOCAL = PROJECT / 'local/recovery_v0.6'
sys.path.insert(0, str(OLD))
sys.path.insert(0, str(PROJECT / 'src'))

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        while b := f.read(1048576): h.update(b)
    return h.hexdigest()

def arrays(path):
    with np.load(path, allow_pickle=False) as f:
        return {k: f[k] for k in f.files}

def packed(**values):
    f = io.BytesIO()
    np.savez_compressed(f, **values)
    return f.getvalue()

def config():
    cfg = json.loads((OLD / 'config.json').read_text())
    cfg.update(json.loads((HERE / 'config.json').read_text()))
    return cfg

def old_guard():
    guard = {}
    for name in ['FREEZE.json', 'REPORTING_RECOVERY_FREEZE.json', 'PACKAGE_MANIFEST.json']:
        p = OLD / name
        guard[str(p.relative_to(PROJECT))] = sha(p)
        d = json.loads(p.read_text())
        for key in ['source_sha256', 'input_sha256', 'sha256']:
            guard.update(d.get(key, {}))
    # Include the presentation separately without changing scientific identities.
    p = PROJECT / 'simulation/BUNDLE_MANIFEST.json'
    guard[str(p.relative_to(PROJECT))] = sha(p)
    guard.update(json.loads(p.read_text())['sha256'])
    return guard

def verify_map(mapping):
    for name, expected in mapping.items():
        if 'datasets/raw/' in name or Path(name).is_absolute():
            raise ValueError('Disallowed input path')
        if sha(PROJECT / name) != expected:
            raise ValueError('Changed identity: ' + name)

def check_freeze():
    f = json.loads((HERE / 'FREEZE.json').read_text())
    verify_map(f['source_sha256']); verify_map(f['input_sha256'])
    return f

def roster(cfg):
    return [dict(id=f'eval_{t["id"]}_{p["id"]}_{seed}_{condition}',
                 task=t['id'], plant=p['id'], seed=seed, condition=condition,
                 stratum=p['stratum'], noise_seed=seed+40000+2000*ti+500*pi)
            for ti,t in enumerate(cfg['tasks']) for pi,p in enumerate(cfg['fresh_plants'])
            for seed in cfg['seeds'] for condition in cfg['evaluation_conditions']]

def scaled_plant(cfg, mass_factor, damping_factor):
    p = dict(cfg['nominal'])
    p.update(m1=p['m1']*mass_factor, m2=p['m2']*mass_factor,
             b=(np.asarray(p['b'])*damping_factor).tolist())
    return p
