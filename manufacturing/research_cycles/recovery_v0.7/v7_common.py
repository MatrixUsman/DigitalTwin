import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
OLD=HERE.parent/'recovery_v0.6'
LOCAL=PROJECT/'local/recovery_v0.7'
RUN6=PROJECT/'local/recovery_v0.6/runs/simulation_001'
sys.path.insert(0,str(OLD))
from support import sha,arrays,packed,verify_map

def config():
    c=json.loads((OLD/'FREEZE.json').read_text())['configuration']
    c.update(json.loads((HERE/'config.json').read_text()));return c

def guard():
    g={}
    for name in ['FREEZE.json','PACKAGE_MANIFEST.json','HANDOFF_AUDIT.json']:
        p=OLD/name;g[str(p.relative_to(PROJECT))]=sha(p);d=json.loads(p.read_text())
        for key in ['source_sha256','input_sha256','sha256']:g.update(d.get(key,{}))
    return g

def check():
    f=json.loads((HERE/'FREEZE.json').read_text());verify_map(f['source_sha256']);verify_map(f['input_sha256']);return f

def roster(c):
    return [dict(id=f'eval_{t["id"]}_{p["id"]}_{seed}_{condition}',task=t['id'],plant=p['id'],
        stratum=p['id'],seed=seed,condition=condition,noise_seed=seed+80000+2000*ti+500*pi)
        for ti,t in enumerate(c['tasks7']) for pi,p in enumerate(c['plants7']) for seed in c['seeds'] for condition in c['evaluation_conditions']]

def permitted(c):
    keys=['nominal','bank','dt','substeps','kp','kd','torque_limit','amplitude','phase_offset','observer_gain',
          'ar_order','cusum_cap','cusum_drift','mode_duration','mode_position_jump','mode_velocity_jump',
          'noise_margin_sigma','physical_tolerance','sensor_sigma','recovery_dwell']
    return {k:c[k] for k in keys}
