"""Ordinary ARX/FIR identification and restricted causal prediction."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True,slots=True)
class Observation:
    measurements: np.ndarray
    commands: np.ndarray
    valid: np.ndarray
    def __post_init__(self):
        y=np.array(self.measurements,dtype=float,copy=True);u=np.array(self.commands,dtype=float,copy=True);v=np.array(self.valid,dtype=bool,copy=True)
        if y.ndim!=2 or y.shape[1]!=4 or u.shape!=y.shape or v.shape!=(len(y),):raise ValueError('Invalid observation shape')
        if not np.isfinite(y).all() or not np.isfinite(u).all():raise ValueError('Nonfinite observation')
        if not v.all():raise ValueError('Normal study requires complete command context')
        for name,a in [('measurements',y),('commands',u),('valid',v)]:
            a.flags.writeable=False;object.__setattr__(self,name,a)

def design(z,u,kind,order,start):
    if order<1 or start<order or start>=len(z):raise ValueError('Invalid history')
    t=np.arange(start,len(z));lags=t[:,None]+np.arange(-order,0)
    parts=([z[lags].reshape(len(t),-1)] if kind=='arx' else [])+[u[lags].reshape(len(t),-1),np.ones((len(t),1))]
    if kind not in ['arx','fir']:raise ValueError('Unknown model')
    return np.column_stack(parts),z[t]

def fit(episodes,spec,warmup):
    if spec['ridge']<=0:raise ValueError('Ridge must be positive')
    y=np.concatenate([e.measurements[warmup:] for e in episodes]);mean=y.mean(0);scale=y.std(0)
    if not np.isfinite(y).all() or np.any(scale<=0):raise ValueError('Invalid training channels')
    p=spec['order'];kind=spec['kind'];dim=p*(8 if kind=='arx' else 4)+1
    xx=np.zeros((dim,dim));xy=np.zeros((dim,4));n=0
    for e in episodes:
        x,target=design((e.measurements-mean)/scale,e.commands,kind,p,warmup)
        xx+=x.T@x;xy+=x.T@target;n+=len(x)
    penalty=np.eye(dim)*spec['ridge'];penalty[-1,-1]=0
    beta=np.linalg.solve(xx/n+penalty,xy/n)
    radius=0.
    if kind=='arx':
        a=np.zeros((p*4,p*4));a[:-4,4:]=np.eye((p-1)*4);a[-4:]=beta[:p*4].T
        radius=float(np.max(np.abs(np.linalg.eigvals(a))))
    return dict(beta=beta,mean=mean,scale=scale,radius=np.array(radius),order=np.array(p),
                kind=np.array(kind),ridge=np.array(spec['ridge']),training_targets=np.array(n))

def predict(obs,model,warmup,following=False):
    p=int(model['order']);kind=str(model['kind']);y=obs.measurements;u=obs.commands
    if not p<=warmup<len(y):raise ValueError('Insufficient prefix')
    if kind=='arx' and float(model['radius'])>=1:raise ValueError('Unstable homogeneous recurrence')
    z=(y-model['mean'])/model['scale'];pred=np.zeros_like(z);pred[:warmup]=z[:warmup]
    if kind=='fir':
        x,_=design(z,u,kind,p,warmup);pred[warmup:]=x@model['beta']
    else:
        for t in range(warmup,len(y)):
            hist=z[t-p:t] if following else pred[t-p:t]
            pred[t]=np.r_[hist.reshape(-1),u[t-p:t].reshape(-1),1.]@model['beta']
    result=pred*model['scale']+model['mean']
    if not np.isfinite(result).all():raise ValueError('Nonfinite reference')
    return result

def discrepancy(obs,reference,scale):return np.max(np.abs((obs.measurements-reference)/scale),axis=1)

def select(rows,kind=None):
    good=[r for r in rows if r['status']=='eligible' and (kind is None or r['kind']==kind)]
    if not good:raise ValueError('No eligible candidate')
    return min(good,key=lambda r:(r['worst_development_q99'],r['mean_development_rmse'],r['parameter_count'],r['id']))['id']
