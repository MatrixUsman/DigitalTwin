"""Shared paths, immutable configuration and hash checks; no observation loading."""
from pathlib import Path
import os,sys,json,hashlib,io
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:
    os.environ[key]='1'
import numpy as np
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
OLD=HERE.parent/'recovery_v0.8'
INPUT=PROJECT/'local/recovery_v0.8/runs/confirmation_002'
LOCAL=PROJECT/'local/commissioning_v0.9'
sys.path.insert(0,str(OLD))
from common import check as old_check
from simulation import generate as old_generate

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def packed(**a):
    b=io.BytesIO();np.savez_compressed(b,**a);return b.getvalue()
def config():return json.loads((HERE/'config.json').read_text())
def check():
    f=json.loads((HERE/'FREEZE.json').read_text())
    for group in ['source_sha256','input_sha256']:
        for name,h in f[group].items():
            if sha(PROJECT/name)!=h:raise ValueError('Identity changed: '+name)
    return f

def bank(c):
    return [dict(id=f'{kind}_{p:02d}_{r:.0e}',kind=kind,order=p,ridge=r)
            for kind,key in [('arx','arx_orders'),('fir','fir_orders')]
            for p in c[key] for r in c['ridges']]

def normal_catalog(c):
    rows=[]
    for plant in ['Q1','Q2','Q3']:
        for i in range(3):rows.append(dict(name=f'train_{plant}_{i}.npz',plant=plant,stage='train',index=i))
        for stage,key in [('development','development_indices'),('allowance','allowance_indices'),('archived_check','archived_check_indices')]:
            for i in c[key]:rows.append(dict(name=f'cal_{plant}_{i:02d}.npz',plant=plant,stage=stage,index=i))
    names=[r['name'] for r in rows]
    if len(set(names))!=len(names):raise ValueError('Overlapping episode split')
    return rows
