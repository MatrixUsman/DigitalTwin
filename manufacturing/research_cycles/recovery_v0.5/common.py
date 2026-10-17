"""Identity checks and local, non-overwriting artifact support."""
import hashlib
import io
import json
from pathlib import Path
import sys
import numpy as np

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
LOCAL=PROJECT/'local/recovery_v0.5'
sys.path.insert(0,str(PROJECT/'src'))

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        while block:=f.read(1024*1024):h.update(block)
    return h.hexdigest()

def packed(**arrays):
    f=io.BytesIO();np.savez_compressed(f,**arrays);return f.getvalue()

def arrays(path):
    with np.load(path,allow_pickle=False) as f:return {k:f[k] for k in f.files}

def check_freeze():
    frozen=json.loads((HERE/'FREEZE.json').read_text())
    for group in ['source_sha256','input_sha256']:
        for p,h in frozen[group].items():
            if 'datasets/raw/' in p:raise ValueError('Raw access prohibited')
            if sha(PROJECT/p)!=h:raise ValueError('Changed frozen identity: '+p)
    return frozen

def previous_guard():
    base=PROJECT/'research_cycles/limitation_v0.4';guard={}
    for name in ['FREEZE.json','PACKAGE_MANIFEST.json']:
        p=base/name;guard[str(p.relative_to(PROJECT))]=sha(p)
    old=json.loads((base/'FREEZE.json').read_text())
    guard.update(old['source_sha256']);guard.update(old['input_sha256'])
    guard.update(json.loads((base/'PACKAGE_MANIFEST.json').read_text())['sha256'])
    verified=json.loads((PROJECT/'local/limitation_v0.4/verification/verify_001/verification.json').read_text())
    for p,h in verified['run_sha256'].items():guard['local/limitation_v0.4/runs/replay_001/'+p]=h
    for p,h in guard.items():
        if 'datasets/raw/' in p:raise ValueError('Raw access prohibited')
        if sha(PROJECT/p)!=h:raise ValueError('Previous artifact changed: '+p)
    return guard

def roster(cfg,role):
    conditions=cfg['evaluation_conditions'] if role=='evaluation' else cfg['normal_conditions']
    return [dict(id=f'{role}_{p["id"]}_{seed}_{condition}',role=role,plant=p['id'],seed=seed,condition=condition)
            for p in cfg['plants'] for seed in cfg['seeds'] for condition in conditions]
