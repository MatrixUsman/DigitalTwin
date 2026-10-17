from pathlib import Path
import hashlib,io,json,sys,importlib.util
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
LOCAL=PROJECT/'local/attack_audit_v0.14'
RUN=LOCAL/'runs/audit_001'
PREVIOUS=HERE.parent/'residual_twin_v0.13'
MODELS=PROJECT/'local/residual_twin_v0.13/runs/pilot_001'
NORMAL=PROJECT/'local/recovery_v0.8/runs/confirmation_002'
OLD=HERE.parent/'commissioning_v0.9'
sys.path.insert(0,str(PROJECT/'src'));sys.path.insert(0,str(OLD))
from models import Observation,predict
spec=importlib.util.spec_from_file_location('residual13',PREVIOUS/'model.py')
residual13=importlib.util.module_from_spec(spec);spec.loader.exec_module(residual13)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for part in iter(lambda:f.read(1048576),b''):h.update(part)
    return h.hexdigest()

def packed(**arrays):
    import numpy as np
    b=io.BytesIO();np.savez_compressed(b,**arrays);return b.getvalue()

def load_npz(path):
    import numpy as np
    with np.load(path,allow_pickle=False) as z:result={k:z[k] for k in z.files}
    for value in result.values():value.flags.writeable=False
    return result

def check():
    f=json.loads((HERE/'FREEZE.json').read_text())
    for group in ['sources','inputs']:
        for name,h in f[group].items():
            if sha(PROJECT/name)!=h:raise ValueError('Changed frozen identity '+name)
    return f
