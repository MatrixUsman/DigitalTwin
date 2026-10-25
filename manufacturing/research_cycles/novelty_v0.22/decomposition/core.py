"""No-fit decomposition; model inputs/targets match released score_sequence."""
from pathlib import Path
import hashlib
import json
import numpy as np
import torch

H = Path(__file__).resolve().parent
P = H.parents[2]
START = 100

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def check():
    freeze = json.loads((H/'FREEZE.json').read_text())
    for path, digest in freeze['bindings'].items():
        if sha(P/path) != digest:
            raise ValueError('Changed frozen input: '+path)
    return freeze

@torch.no_grad()
def decompose(model, stats, obs, actions):
    from rapt.model import nll_per_dim
    if not model.cfg.train_dynamics or len(obs) < 2:
        raise ValueError('Only forward dynamics with at least two observations admitted')
    model.eval().to('cpu')
    o = torch.from_numpy(stats.normalize(obs).astype(np.float32)).to('cpu')
    a = torch.from_numpy(actions.astype(np.float32)).to('cpu')
    x = torch.cat([o[:-1], a[:-1]], dim=1)
    target = o[1:]
    mu, logvar, _ = model(x.unsqueeze(0))
    mse = (target-mu[0])**2
    loss = nll_per_dim(mu[0], logvar[0], target)
    def aligned(value):
        value = value.cpu().numpy()
        return np.concatenate([np.zeros((1,value.shape[1]),dtype=value.dtype),value])
    eligible = np.arange(len(obs)) >= START
    defined = np.arange(len(obs)) > 0
    return dict(mean=aligned(mu[0]),logvar=aligned(logvar[0]),
                squared_error=aligned(mse),loss=aligned(loss),
                defined=defined,eligible=eligible)

def region_stats(arrays, lo, hi):
    if not 1 <= lo < hi <= len(arrays['loss']):
        raise ValueError('Invalid defined-score region')
    mu, lv, mse, loss = [np.asarray(arrays[k][lo:hi],float) for k in ['mean','logvar','squared_error','loss']]
    channels=[]
    for j in range(loss.shape[1]):
        positive=(mse[:,j]>0)&(loss[:,j]>0)
        if positive.any():
            log_mse=np.log(mse[positive,j]);log_score=np.log(loss[positive,j]);logs=lv[positive,j]
            err=float(np.max(np.abs(log_score-(log_mse-logs))))
            if err>2e-5:raise ValueError('Float32 log-score identity discrepancy')
            log_summary=dict(points=int(positive.sum()),excluded_zero=int((~positive).sum()),
                mean_log_squared_error=float(log_mse.mean()),mean_log_variance=float(logs.mean()),
                mean_log_score=float(log_score.mean()),max_identity_roundoff=err)
        else:log_summary=dict(points=0,excluded_zero=int(len(loss)),mean_log_squared_error=None,
                             mean_log_variance=None,mean_log_score=None,max_identity_roundoff=None)
        channels.append(dict(channel=j,points=len(loss),mean_prediction=float(mu[:,j].mean()),
            mean_log_variance=float(lv[:,j].mean()),mean_variance=float(np.exp(lv[:,j]).mean()),
            mean_squared_error=float(mse[:,j].mean()),mean_score=float(loss[:,j].mean()),log_decomposition=log_summary))
    return dict(lo=lo,hi=hi,points=hi-lo,channels=channels)

def interval(row, tasks, length):
    task=tasks[row['task']]
    if row['condition'] in ['normal','authorized_changes']:
        return START,length,'full eligible benign episode'
    lo=task['onset']
    span=task['brief'] if row['condition']=='brief_offset' else task['duration']
    return lo,lo+span,'frozen v0.19 command-intervention schedule'

def episode_summary(row, arrays, tasks):
    lo,hi,meaning=interval(row,tasks,len(arrays['loss']));q=max(1,(hi-lo)//4)
    first=region_stats(arrays,lo,lo+q);last=region_stats(arrays,hi-q,hi)
    delta=[]
    for aa,bb in zip(first['channels'],last['channels']):
        a=aa['log_decomposition'];b=bb['log_decomposition']
        delta.append(dict(channel=aa['channel'],first_positive=a['points'],last_positive=b['points'],
            delta_mean_log_squared_error=None if not a['points'] or not b['points'] else b['mean_log_squared_error']-a['mean_log_squared_error'],
            delta_mean_log_variance=None if not a['points'] or not b['points'] else b['mean_log_variance']-a['mean_log_variance'],
            delta_mean_log_score=None if not a['points'] or not b['points'] else b['mean_log_score']-a['mean_log_score']))
    return dict(**{k:row[k] for k in ['id','plant','task','seed','condition']},
                interval_definition=meaning,first=first,last=last,log_changes=delta,
                eligible_all=region_stats(arrays,START,len(arrays['loss'])))
