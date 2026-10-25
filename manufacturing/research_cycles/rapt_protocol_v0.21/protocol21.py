from pathlib import Path
import json,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
START=100

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def check():
    f=json.loads((HERE/'FREEZE.json').read_text())
    for path,digest in f['bindings'].items():
        if sha(PROJECT/path)!=digest:raise ValueError('Frozen binding changed: '+path)
    return f

def stage_paths(manifest,plant,role):
    rows=[r for r in manifest['files'] if r['plant']==plant and r['role']==role]
    if len(rows)!=9 or len({r['path'] for r in rows})!=9:raise ValueError('Expected nine unique admitted episodes')
    return rows

def load_role(manifest,plant,role,access,trim=False):
    from rapt import SequenceData
    obs=[];actions=[];names=[]
    for r in stage_paths(manifest,plant,role):
        path=PROJECT/r['path']
        if sha(path)!=r['sha256']:raise ValueError('Changed normal file')
        with np.load(path,allow_pickle=False) as z:
            y=z['measurements'].astype(np.float32);u=z['commands'].astype(np.float32);v=z['valid'].astype(bool)
        if y.shape!=(1200,4) or u.shape!=y.shape or v.shape!=(1200,) or not v.all():raise ValueError('Unadmitted feature shape/context')
        if not np.isfinite(y).all() or not np.isfinite(u).all():raise ValueError('Nonfinite observations')
        obs.append(y[START:] if trim else y);actions.append(u[START:] if trim else u);names.append(Path(r['path']).stem)
        access.append(dict(path=r['path'],sha256=r['sha256'],role=role,members=['measurements','commands','valid'],slice_start=START if trim else 0))
    return SequenceData(obs,actions,names=names)

def calibrate_eligible(losses,observations,cfg,start=START):
    from rapt.detector import Calibration
    if len(losses)!=len(observations) or not losses:raise ValueError('Population mismatch')
    flat=np.concatenate([a[start:] for a in losses]);raw=np.concatenate([a[start:] for a in observations])
    if flat.shape!=raw.shape or not np.isfinite(flat).all() or not np.isfinite(raw).all():raise ValueError('Invalid calibration')
    med=np.median(flat,axis=0);mx=flat.max(0);mean=flat.mean(1)
    return Calibration(per_dim_median=med,per_dim_max=mx,per_dim_thresh=mx+cfg.k_dim*(mx-med),
        mean_max=float(mean.max()),mean_std=float(mean.std()),mean_thresh=float(mean.max()+cfg.k_global*mean.std()),
        obs_min=raw.min(0),obs_max=raw.max(0),range_buffer=cfg.range_buffer,k_dim=cfg.k_dim,k_global=cfg.k_global)

def curve_summary(history):
    v=np.asarray(history['val_nll'],float);t=np.asarray(history['train_nll'],float)
    if len(v)!=100 or len(t)!=100 or not np.isfinite(v).all() or not np.isfinite(t).all():raise ValueError('Incomplete100-epoch curves')
    early=float(v[:20].min());late=float(v[-20:].min());best=int(np.argmin(v))+1
    return dict(epochs_completed=100,selected_epoch=best,first_train_nll=float(t[0]),last_train_nll=float(t[-1]),
        first_dev_nll=float(v[0]),last_dev_nll=float(v[-1]),best_dev_nll=float(v.min()),first20_minimum=early,
        last20_minimum=late,late_improvement=(early-late)/max(abs(early),1e-8),best_after_epoch90=best>90,
        convergence_certified=False)
