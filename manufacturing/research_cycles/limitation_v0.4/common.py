import hashlib
import io
import json
from pathlib import Path
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
UPSTREAM = HERE.parent / 'baseline_training_v0.3'
LOCAL = PROJECT / 'local/limitation_v0.4'
sys.path.insert(0, str(UPSTREAM))
sys.path.insert(0, str(PROJECT / 'src'))


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        while block:=f.read(1024*1024): h.update(block)
    return h.hexdigest()


def packed(**arrays):
    f=io.BytesIO();np.savez_compressed(f,**arrays);return f.getvalue()


def check_freeze():
    f=json.loads((HERE/'FREEZE.json').read_text())
    for group in ['source_sha256','input_sha256']:
        for p,h in f[group].items():
            if sha(PROJECT/p)!=h:raise ValueError('Frozen identity changed: '+p)
    return f


def upstream_guard():
    """All prior package bindings, without opening any raw observations."""
    guard={}
    for name in ['PACKAGE_MANIFEST.json','FREEZE.json']:
        p=UPSTREAM/name;guard[str(p.relative_to(PROJECT))]=sha(p)
    old=json.loads((UPSTREAM/'PACKAGE_MANIFEST.json').read_text())
    for p,h in old['sha256'].items():
        if sha(PROJECT/p)!=h:raise ValueError('Upstream package mismatch: '+p)
        guard[p]=h
    freeze=json.loads((UPSTREAM/'FREEZE.json').read_text())
    guard.update(freeze['source_sha256'])
    vpath=PROJECT/'local/baseline_training_v0.3/verification/verify_001/verification.json'
    v=json.loads(vpath.read_text())
    run=PROJECT/'local/baseline_training_v0.3/runs/training_001'
    for p,h in v['run_artifact_sha256'].items():guard[str((run/p).relative_to(PROJECT))]=h
    history=json.loads((PROJECT/'local/baseline_training_v0.3/starting_guard.json').read_text())
    old=history['old_campaign']
    guard.update(old['frozen_source'])
    for item in old['frozen_inputs']:guard[item['path']]=item['sha256']
    guard.update(history['v02_files'])
    guard['research_cycles/contribution_v0.2/EVIDENCE_MANIFEST.json']=history['v02_manifest_sha256']
    guard['output/pdf/correction-evidence-casper-study.pdf']='c849f75b14b913646b1f756e5f73cf211163dc590216db693cd0d7cb72a4bd6f'
    # Older receipts bind all historic evidence; the existing v0.3 verifier
    # already checked these records. Their receipt is bound above.
    for p,h in guard.items():
        if 'datasets/raw/' in p:raise ValueError('Raw access is outside this cycle')
        if sha(PROJECT/p)!=h:raise ValueError('Previous identity changed: '+p)
    return guard


def load_source(config):
    run=PROJECT/config['source_run']
    with np.load(run/'prepared_development.npz',allow_pickle=False) as a:
        values=a['values'];indices=a['indices'];raw=a['raw_indices']
    if (values.shape!=(16429,9) or not np.isfinite(values).all()
        or not np.array_equal(indices,np.arange(45,16429))
        or not np.array_equal(raw,indices+65800)):
        raise ValueError('Unexpected development population')
    values.setflags(write=False)
    return run,values,indices,raw


def predictor(name, config, run):
    from model import load_weights_artifact, predict
    from core import predict_ar
    if name=='mean':return lambda y,t:np.zeros((len(t),9),dtype=np.float64)
    if name=='persistence':return lambda y,t:y[t-1].copy()
    if name=='ar4':
        with np.load(run/'ar_coefficients.npz',allow_pickle=False) as a:coef=a['coefficients']
        return lambda y,t:predict_ar(y,t,coef,4,1024)
    model=load_weights_artifact(config,run/f'{name}_weights.npz')
    return lambda y,t:predict(model,y,t,45,1024)
