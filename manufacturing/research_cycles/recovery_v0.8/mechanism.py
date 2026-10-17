"""Independent commissioning reference and explicitly restricted alarm logic."""
import numpy as np

def features(z,u,order=4):
    t=np.arange(order,len(z));lags=t[:,None]+np.arange(-order,0)
    return np.column_stack([z[lags].reshape(len(t),-1),u[lags].reshape(len(t),-1),np.ones(len(t))]),t

def fit_reference(episodes,order=4,ridge=1e-7,warmup=100):
    all_y=np.concatenate([e['measurements'][warmup:] for e in episodes])
    mean=all_y.mean(0);scale=all_y.std(0)
    if not np.isfinite(all_y).all() or np.any(scale<=0):raise ValueError('Invalid commissioning channel')
    xx=np.zeros((order*8+1,order*8+1));xy=np.zeros((order*8+1,4));n=0
    for e in episodes:
        z=(e['measurements']-mean)/scale;x,t=features(z,e['available'],order);ok=t>=warmup
        x=x[ok];target=z[t[ok]];xx+=x.T@x;xy+=x.T@target;n+=len(x)
    penalty=np.eye(len(xx))*ridge;penalty[-1,-1]=0
    beta=np.linalg.solve(xx/n+penalty,xy/n)
    A=np.zeros((4*order,4*order));A[:-4,4:]=np.eye(4*(order-1));A[-4:]=beta[:4*order].T
    radius=float(np.max(np.abs(np.linalg.eigvals(A))))
    if radius>=1:raise ValueError(f'Unstable commissioning reference: radius {radius}')
    return dict(mean=mean,scale=scale,beta=beta,radius=np.array(radius),order=np.array(order))

def reference(y,u,fit,follow=False):
    if y.shape!=u.shape or y.ndim!=2 or y.shape[1]!=4 or not np.isfinite(y).all() or not np.isfinite(u).all():raise ValueError('Invalid input')
    order=int(fit['order']);z=(y-fit['mean'])/fit['scale'];pred=np.zeros_like(z);pred[:order]=z[:order]
    for t in range(order,len(z)):
        hist=z[t-order:t] if follow else pred[t-order:t]
        x=np.r_[hist.reshape(-1),u[t-order:t].reshape(-1),1.]
        pred[t]=x@fit['beta']
    if not np.isfinite(pred).all():raise ValueError('Nonfinite reference')
    return pred*fit['scale']+fit['mean']

def scalar(y,r,scale):return np.max(np.abs((y-r)/scale),axis=1)

def bounds(discrepancy,reference_error,sensor_error=0.):
    if np.any(np.asarray(reference_error)<0) or sensor_error<0:raise ValueError('Negative allowance')
    a=reference_error+sensor_error
    return np.maximum(0,discrepancy-a),discrepancy+a

def known_context(valid):
    # A missing command leaves the free reference unresolved for this episode.
    return np.logical_and.accumulate(valid)

def latch(score,known,high,dwell=10,return_ok=None):
    active=False;count=0;out=np.zeros(len(score),bool)
    for t,s in enumerate(score):
        if not known[t]:count=0
        elif s>high:active=True;count=0
        elif active:
            ok=bool(return_ok[t]) if return_ok is not None else s<=.5*high
            count=count+1 if ok else 0
            if count>=dwell:active=False;count=0
        out[t]=active
    return out

def decide(e,j,h,b,c):
    s=e['scores'][:,j];known=known_context(e['valid']) if j!=0 else np.ones(len(s),bool)
    if j in [0,1,2,6,10]:return s>h,~known
    ret=None;d=c['dwell']
    if j==5:ret=e['nominal_error']<=c['return_tolerance']
    if j in [8,11]:ret=e['learned_error']<=c['return_tolerance']
    if j in [9,12]:ret=e['learned_error']+b<=c['return_tolerance']
    if j==12:d=1
    return latch(s,known,h,d,ret),~known

def calibrate(eps,j,b,c):
    grid=np.unique(np.r_[0.,np.concatenate([e['scores'][:,j] for e in eps])])
    budget=int(.01*sum(len(e['scores'])-c['warmup'] for e in eps));cache={}
    def count(k):
        if k not in cache:
            cache[k]=sum(int((decide(e,j,grid[k],b,c)[0]&~decide(e,j,grid[k],b,c)[1])[c['warmup']:].sum()) for e in eps)
        return cache[k]
    lo=0;hi=len(grid)-1
    assert count(hi)<=budget
    while lo<hi:
        m=(lo+hi)//2
        if count(m)<=budget:hi=m
        else:lo=m+1
    assert lo==0 or count(lo-1)>budget
    return dict(threshold=float(grid[lo]),alarms=count(lo),budget=budget,preceding=count(lo-1) if lo else None,
                probes=[dict(index=k,threshold=float(grid[k]),alarms=v) for k,v in sorted(cache.items())])
