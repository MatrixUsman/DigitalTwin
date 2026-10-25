from pathlib import Path
import hashlib,json
import numpy as np
H=Path(__file__).resolve().parent;P=H.parents[1]
ALLOWED=('measurements','commands','valid')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def checked_arrays(y,u,valid):
    if y.shape!=(1200,4) or u.shape!=(1200,4) or valid.shape!=(1200,) or not valid.all() or not np.isfinite(y).all() or not np.isfinite(u).all():raise ValueError('Expected complete finite 1200x4 normal episode')
    return y,u
def load_normal(manifest,role,access):
    rows=[r for r in manifest['files'] if r['role']==role]
    if role not in ['fit','development'] or len(rows)!=9:raise ValueError('Only nine fit/development episodes permitted')
    ys=[];us=[]
    for r in rows:
        if sha(P/r['path'])!=r['sha256']:raise ValueError('Changed normal input')
        with np.load(P/r['path'],allow_pickle=False) as z:
            y=z['measurements'].astype(float);u=z['commands'].astype(float);valid=z['valid'].astype(bool)
        checked_arrays(y,u,valid);ys.append(y);us.append(u);access.append(dict(path=r['path'],members=list(ALLOWED),role=role,rows=1200))
    return rows,ys,us
