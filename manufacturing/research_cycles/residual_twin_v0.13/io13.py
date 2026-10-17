from pathlib import Path
import hashlib,io,json,sys
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
LOCAL=PROJECT/'local/residual_twin_v0.13'
RUN=LOCAL/'runs/pilot_001'
OLD=PROJECT/'research_cycles/commissioning_v0.9'
INPUT=PROJECT/'local/recovery_v0.8/runs/confirmation_002'
FITS=PROJECT/'local/commissioning_v0.9/runs/normal_002'
sys.path.insert(0,str(PROJECT/'src'))

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
    return h.hexdigest()

def packed(**arrays):
    import numpy as np
    b=io.BytesIO();np.savez_compressed(b,**arrays);return b.getvalue()

def check():
    f=json.loads((HERE/'FREEZE.json').read_text())
    for group in ['sources','inputs']:
        for name,digest in f[group].items():
            if sha(PROJECT/name)!=digest:raise ValueError('Changed identity: '+name)
    return f
