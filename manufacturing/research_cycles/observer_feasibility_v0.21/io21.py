"""Study-specific IO name avoids historical modules named common."""
from pathlib import Path
import sys,json,hashlib,io
import numpy as np
HERE=Path(__file__).resolve().parent;PROJECT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'context_recovery_v0.19'))
import io19
from io19 import physical,plant_parameters,permitted,Observation,bases
from io14 import predict
from mechanism19 import set_alarm,quantile
from mfg_twin.supervisor import Limits,BudgetWriter,install_worker_limits,worker_usage,supervise
LOCAL=PROJECT/'local/observer_feasibility_v0.21'
NORMAL=PROJECT/'local/residual_twin_v0.13/runs/pilot_001'
LIMITS=Limits(wall_seconds=180,cpu_seconds=120,rss_bytes=1073741824,output_bytes=52428800)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def packed(**kw):
    b=io.BytesIO();np.savez_compressed(b,**kw);return b.getvalue()
def freeze_check():
    f=json.loads((HERE/'FREEZE.json').read_text())
    for p,h in f['bindings'].items():
        if sha(PROJECT/p)!=h:raise ValueError('Changed frozen source/input '+p)
    return f

def records(task,plant,access):
    result=[]
    for p in sorted(NORMAL.glob(f'normal_{task}_{plant}_*.npz')):
        with np.load(p,allow_pickle=False) as z:
            result.append((z['measurements'].copy(),z['commands'].copy(),z['references'][:,0].copy()))
        access.append({'path':str(p.relative_to(PROJECT)),'sha256':sha(p),'members':['measurements','commands','references/base']})
    if len(result)!=9:raise ValueError('Normal partition mismatch')
    return result

def command_path(kind,n=1500):
    t=np.arange(n)*.02
    if kind=='arctansine':
        qs=[];vs=[]
        for amp,freq,phase in [(.31,.66,.3),(.28,.81,.9)]:
            s=np.sin(freq*t+phase);k=1.8
            qs.append(amp*2/np.pi*np.arctan(k*s))
            vs.append(amp*2/np.pi*k*freq*np.cos(freq*t+phase)/(1+(k*s)**2))
        return np.column_stack(qs+vs)
    if kind=='gaussian_pulses':
        q=np.zeros((n,2));v=q.copy()
        for j in range(2):
            for k,(center,width) in enumerate([(5.,1.4),(13.,2.2),(23.,1.8)]):
                a=(.28+.03*j)*(-1)**(k+j);z=(t-center-.6*j)/width;g=a*np.exp(-z*z/2)
                q[:,j]+=g;v[:,j]+=-z/width*g
        return np.column_stack([q,v])
    raise ValueError('Unknown task')

def measurement(state,sigma,kind,seed):
    rng=np.random.default_rng(seed);noise=rng.normal(size=state.shape)*sigma
    if kind=='ar1':
        for t in range(1,len(noise)):noise[t]=.65*noise[t-1]+np.sqrt(1-.65**2)*noise[t]
    if kind in ('iid','ar1'):return state+noise
    if kind=='encoder':
        q=np.round((state[:,:2]+noise[:,:2])/.0001)*.0001
        v=np.zeros_like(q);v[1:]=np.diff(q,axis=0)/.02
        return np.column_stack([q,v])
    raise ValueError('Unknown noise')
