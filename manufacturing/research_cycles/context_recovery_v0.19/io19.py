from pathlib import Path
import sys,json,hashlib,io,importlib.util
import numpy as np
HERE=Path(__file__).resolve().parent;PROJECT=HERE.parents[1];LOCAL=PROJECT/'local/context_recovery_v0.19'
sys.path.insert(0,str(HERE.parent/'attack_audit_v0.14'))
from io14 import MODELS,load_npz,Observation,residual13
from audit_core import infer
from evaluation import evaluate
from common9 import old_generate
from simulation import plant_parameters
from v7_core import physical
from v7_common import permitted
from mfg_twin.supervisor import Limits,BudgetWriter,install_worker_limits,worker_usage,supervise
NORMAL=MODELS;OLD=PROJECT/'local/attack_audit_v0.14/runs/audit_001'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def packed(**arrays):
    b=io.BytesIO();np.savez_compressed(b,**arrays);return b.getvalue()
def write(p,x):
    p=Path(p)
    with p.open('x') as f:json.dump(x,f,indent=2,allow_nan=False);f.write('\n')
def bases():
    chosen=json.loads((MODELS/'selection.json').read_text());out={}
    for plant in ['Q1','Q2','Q3']:
        out[plant]={'base':load_npz(MODELS/f'base_{plant}.npz')}
        for role in ['linear','rbf']:out[plant][role]=load_npz(MODELS/f'fit_{plant}_{chosen["models"][plant][role]}.npz')
    return out
def check(path):
    f=json.loads(Path(path).read_text())
    for name,h in f['bindings'].items():
        if sha(PROJECT/name)!=h:raise ValueError('Frozen identity changed '+name)
    return f
def source_bindings():
    files=set(HERE.glob('*.py'))|{HERE/'PLAN.md',HERE/'config.json',PROJECT/'docs/literature/RECOVERY_IMPROVEMENT_PRIOR_ART_2026-10-19.md'}
    for module in list(sys.modules.values()):
        path=getattr(module,'__file__',None)
        if path:
            p=Path(path).resolve()
            if p.is_relative_to(PROJECT) and ('research_cycles' in p.parts or 'mfg_twin' in p.parts) and p.suffix=='.py':files.add(p)
    return {str(p.relative_to(PROJECT)):sha(p) for p in sorted(files)}
