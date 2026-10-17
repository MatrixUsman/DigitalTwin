"""Observed-input-only inference; no truth, labels, fitting or model selection."""
import numpy as np
from io14 import Observation,predict,residual13
ROLES=['base','linear','rbf','following','rbf_following','persistence','mean21','cusum']

def settings(config):
    return {k:config[k] for k in ['warmup','return_tolerance','dwell','methods'] if k in config}

def check_settings(c):
    if set(c)-{'warmup','return_tolerance','dwell','methods','recovery_horizon'}:
        raise ValueError('Only detector settings are admitted, not simulation/label configuration')

def cusum(score,k,start=100):
    if k<0 or not np.isfinite(k) or not np.isfinite(score).all():raise ValueError('Invalid CUSUM input')
    out=np.zeros(len(score));v=0.
    for t in range(start,len(score)):
        v=max(0.,v+score[t]-k);out[t]=v
    return out

def infer(obs,models,k,c):
    check_settings(c)
    if not isinstance(obs,Observation):raise TypeError('Restricted Observation required')
    base=models['base'];warmup=c['warmup'];y=obs.measurements;u=obs.commands
    b=predict(obs,base,warmup);f=predict(obs,base,warmup,following=True)
    refs=[b,residual13.correct(b,u,models['linear'],base['scale'],warmup),
          residual13.correct(b,u,models['rbf'],base['scale'],warmup),f,
          residual13.correct(f,u,models['rbf'],base['scale'],warmup)]
    p=y.copy();p[1:]=y[:-1];refs.append(p)
    a=y.copy()
    sums=np.vstack([np.zeros((1,4)),np.cumsum(y,axis=0)])
    t=np.arange(warmup,len(y));a[t]=(sums[t]-sums[t-21])/21;refs.append(a)
    refs=np.stack(refs,axis=1);e=(y[:,None,:]-refs)/base['scale']
    scores=np.column_stack([np.max(np.abs(e),axis=2),cusum(np.max(np.abs(e[:,0]),axis=1),k,warmup)])
    if not np.isfinite(scores).all():raise ValueError('Nonfinite score')
    return refs,e,scores

def specification(method):
    if method=='base_cusum':return 'cusum','point',1
    if method=='rbf_following_dual':return 'rbf_following','dual',10
    if method=='rbf_dual_nodwell':return 'rbf','dual',1
    role,rule=method.rsplit('_',1)
    if role not in ROLES or rule not in ['point','return1','long','dual']:raise ValueError('Unknown method')
    return role,rule,10

def alarm_scores(scores,residual,valid,thresholds,c):
    check_settings(c)
    known=np.logical_and.accumulate(valid);known[:c['warmup']]=False;out=[]
    for name in c['methods']:
        role,rule,dwell=specification(name);i=ROLES.index(role);s=scores[:,i];threshold=thresholds[role]
        if rule=='point':a=(s>threshold)&known
        else:
            windows={'return1':[1],'long':[41],'dual':[5,41]}[rule]
            evidence,_=residual13.return_evidence(residual[:,i],valid,windows=windows,
                         tolerance=c['return_tolerance'],start=c['warmup'])
            a=residual13.alarm_machine(s,known,evidence,threshold,dwell)
        out.append(a)
    return np.stack(out,axis=1)

def calibrate(scores,q=.99):
    s=np.asarray(scores)
    if s.ndim!=1 or not len(s) or not np.isfinite(s).all() or not 0<q<=1:raise ValueError('Invalid calibration')
    rank=int(np.ceil(q*len(s)));return float(np.sort(s)[rank-1]),rank
