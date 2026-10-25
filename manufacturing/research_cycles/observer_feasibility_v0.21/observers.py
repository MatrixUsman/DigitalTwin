"""Established causal estimators; no labels, nominal reference or hidden state input."""
import numpy as np

DT = .02
MAD = .6744897501960817

def checked(y):
    y = np.asarray(y, float)
    if y.ndim != 2 or y.shape[1] != 4 or not len(y) or not np.isfinite(y).all():
        raise ValueError('Finite [q1,q2,v1,v2] observations required')
    return y

def robust_scale(x):
    return np.median(np.abs(x-np.median(x,axis=0)),axis=0)/MAD

def operator(w, variance, coupled):
    if w not in (5,9): raise ValueError('Undeclared history')
    variance=np.asarray(variance,float)
    if variance.shape!=(2,) or not np.isfinite(variance).all() or np.any(variance<=0):
        raise ValueError('Positive observation variances required')
    tau=np.arange(1-w,1)*DT
    hq=np.column_stack([np.ones(w),tau,tau**2/2])
    hv=np.column_stack([np.zeros(w),np.ones(w),tau])
    if coupled:
        h=np.vstack([hq,hv]);weight=np.repeat(1/np.sqrt(variance),w)
        return np.linalg.pinv(h*weight[:,None])*weight[None,:]
    op=np.zeros((3,2*w));op[0,:w]=np.linalg.pinv(hq)[0]
    op[1,w:]=np.linalg.pinv(hv[:,1:])[0]
    op[2,w:]=np.linalg.pinv(hv[:,1:])[1]
    return op

def polynomial(y,variance,w,coupled):
    y=checked(y);out=y.copy();acc=np.zeros((len(y),2))
    if len(y)>=w:
        h=np.lib.stride_tricks.sliding_window_view(y,w,axis=0)
        for j in range(2):
            z=np.concatenate([h[:,j],h[:,j+2]],axis=1)
            beta=z@operator(w,np.asarray(variance)[[j,j+2]],coupled).T
            out[w-1:,j]=beta[:,0];out[w-1:,j+2]=beta[:,1];acc[w-1:,j]=beta[:,2]
    return out,acc

def fit_noise(sequences):
    ys=[checked(y) for y in sequences]
    if not ys or min(map(len,ys))<10:raise ValueError('Insufficient training')
    q=np.concatenate([np.diff(y[:,:2],n=3,axis=0) for y in ys])
    v=np.concatenate([np.diff(y[:,2:],n=2,axis=0) for y in ys])
    variance=np.r_[robust_scale(q)**2/20,robust_scale(v)**2/6]
    if not np.isfinite(variance).all() or np.any(variance<=0):raise ValueError('Degenerate training noise')
    differences=[]
    for y in ys:
        _,a=polynomial(y,variance,9,True);differences.append(np.diff(a[8:],axis=0))
    jerk=robust_scale(np.concatenate(differences))**2/DT
    if not np.isfinite(jerk).all() or np.any(jerk<=0):raise ValueError('Degenerate training jerk')
    return {'variance':variance.tolist(),'jerk_density':jerk.tolist()}

def kalman_parameters(variance,jerk):
    r=np.diag(variance);dt=DT
    f=np.array([[1,dt,dt*dt/2],[0,1,dt],[0,0,1.]])
    h=np.array([[1.,0,0],[0,1.,0]])
    q=jerk*np.array([[dt**5/20,dt**4/8,dt**3/6],[dt**4/8,dt**3/3,dt**2/2],[dt**3/6,dt**2/2,dt]])
    p=np.diag([variance[0],variance[1],variance[1]/dt**2])
    for i in range(10000):
        prior=f@p@f.T+q;k=np.linalg.solve(h@prior@h.T+r,h@prior).T
        a=np.eye(3)-k@h;new=a@prior@a.T+k@r@k.T
        if np.linalg.norm(new-p)<=1e-10*max(np.linalg.norm(p),1e-20):return f,k
        p=new
    raise ValueError('Steady-state covariance did not converge')

def estimate(y,fit,family,setting,cache=None):
    y=checked(y);variance=np.asarray(fit['variance']);acc=np.zeros((len(y),2))
    if family in ('coupled','uncoupled'):
        out,acc=polynomial(y,variance,int(setting),family=='coupled')
    elif family=='raw':out=y.copy()
    elif family=='mean':
        out=y.copy();w=int(setting);s=np.vstack([np.zeros((1,4)),np.cumsum(y,axis=0)])
        if len(y)>=w:out[w-1:]=(s[w:]-s[:-w])/w
    elif family=='kf':
        out=y.copy()
        for j in range(2):
            key=(tuple(variance[[j,j+2]]),float(fit['jerk_density'][j]*setting))
            if cache is not None and key in cache:f,k=cache[key]
            else:
                f,k=kalman_parameters(np.array(key[0]),key[1])
                if cache is not None:cache[key]=(f,k)
            state=np.r_[y[0,[j,j+2]],0.]
            for t in range(1,len(y)):
                prior=f@state;state=prior+k@(y[t,[j,j+2]]-prior[:2])
                out[t,j],out[t,j+2],acc[t,j]=state
    else:raise ValueError('Undeclared estimator')
    prediction=out.copy();prediction[:,:2]+=out[:,2:]*DT+.5*acc*DT**2
    prediction[:,2:]+=acc*DT
    return out,prediction

GRID={'raw':[0],'mean':[5,9],'uncoupled':[5,9],'coupled':[5,9],'kf':[.01,.1,1.,10.]}
