from pathlib import Path
import importlib.util,hashlib,json,sys
import numpy as np
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
OLD=PROJECT/'local/attack_audit_v0.14/runs/audit_001'
MODELS=PROJECT/'local/residual_twin_v0.13/runs/pilot_001'
sys.path.insert(0,str(PROJECT/'src'))
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
model=module('residual_model_review18',PROJECT/'research_cycles/residual_twin_v0.13/model.py')
evaluation=module('evaluation_review18',PROJECT/'research_cycles/attack_audit_v0.14/evaluation.py')
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def load(path):
    with np.load(path,allow_pickle=False) as z:return {k:z[k] for k in z.files}
def check():
    f=json.loads((HERE/'FREEZE.json').read_text())
    for p,h in f['sha256'].items():
        if sha(PROJECT/p)!=h:raise ValueError('Frozen binding changed: '+p)
    return f
