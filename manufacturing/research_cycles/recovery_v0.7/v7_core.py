"""New command families and actuator lag; explicitly restricted detector inputs."""
import numpy as np
from v7_common import permitted
from plant import advance,mass,coriolis
from core import components,score_matrix,stateful,decision as old_decision

def path(s,rate,task):
    if task['kind']=='multisine':theta=.75*s+.10*np.sin(.2*s);speed=.75+.02*np.cos(.2*s)
    elif task['kind']=='chirp':theta=.45*s+.0125*s*s;speed=.45+.025*s
    else:raise ValueError('Unknown task')
    a,b=task['amplitude'];phi=task['phase_offset']
    q=np.column_stack([a*np.sin(theta)+.06*np.sin(2*theta),b*np.sin(theta+phi)+.04*np.sin(3*theta)])
    v=np.column_stack([a*np.cos(theta)+.12*np.cos(2*theta),b*np.cos(theta+phi)+.12*np.cos(3*theta)])*(speed*rate)[:,None]
    return np.column_stack([q,v])

def commands7(c,task,condition):
    n=c['steps'];a,b=c['onset'],c['end'];t=np.arange(n)*c['dt'];rate=np.ones(n)
    base=path(t,rate,task);approved=base.copy();executed=base.copy()
    attack=np.zeros(n,dtype=bool);authorized=attack.copy();valid=~attack
    if condition in ['slow','authorized_slow']:
        rate[a:b]=c['slow_rate'];s=np.r_[0,np.cumsum(rate[:-1])]*c['dt'];executed=path(s,rate,task)
        if condition=='slow':executed[b:]=base[b:];attack[a:b]=True
        else:approved=executed.copy();authorized[a:b]=True
    elif condition in ['authorized_offset','brief_offset','persistent_offset','context_gap_offset']:
        stop=a+c['brief_length'] if condition=='brief_offset' else b
        executed[a:stop,0]+=c['offset_radians']
        if condition=='authorized_offset':approved=executed.copy();authorized[a:stop]=True
        else:attack[a:stop]=True
        if condition=='context_gap_offset':valid[a:c['context_gap_end']]=False
    elif condition=='hold':executed[a:b,:2]=base[a-1,:2];executed[a:b,2:]=0;attack[a:b]=True
    elif condition!='normal':raise ValueError(condition)
    available=approved.copy()
    for i in range(1,n):
        if not valid[i]:available[i]=available[i-1]
    return dict(approved=approved,available=available,executed=executed,valid=valid,attack=attack,authorized=authorized)

def lag_derivative(x,u,p,c,lag):
    q,v,a=x[:2],x[2:4],x[4:]
    demanded=np.clip(np.asarray(c['kp'])*(u[:2]-q)+np.asarray(c['kd'])*(u[2:]-v),-c['torque_limit'],c['torque_limit'])
    rhs=a-coriolis(q,v,p)-np.asarray(p['b'])*v;m=mass(q,p);det=m[0,0]*m[1,1]-m[0,1]**2
    acc=np.array([(m[1,1]*rhs[0]-m[0,1]*rhs[1])/det,(m[0,0]*rhs[1]-m[1,0]*rhs[0])/det])
    return np.r_[v,acc,(demanded-a)/lag]

def physical(initial,command,p,c,lag):
    x=np.zeros((len(command),6));x[0,:4]=initial;h=c['dt']/c['substeps']
    for t in range(len(command)-1):
        if lag==0:
            x[t+1,:4]=advance(x[t,:4],command[t],p,c)
            x[t,4:]=np.clip(np.asarray(c['kp'])*(command[t,:2]-x[t,:2])+np.asarray(c['kd'])*(command[t,2:]-x[t,2:4]),-c['torque_limit'],c['torque_limit'])
        else:
            z=x[t].copy()
            for _ in range(c['substeps']):
                a=lag_derivative(z,command[t],p,c,lag);b=lag_derivative(z+h*a/2,command[t],p,c,lag)
                d=lag_derivative(z+h*b/2,command[t],p,c,lag);e=lag_derivative(z+h*d,command[t],p,c,lag)
                z+=h*(a+2*b+2*d+e)/6
            x[t+1]=z
    if lag==0:x[-1,4:]=np.clip(np.asarray(c['kp'])*(command[-1,:2]-x[-1,:2])+np.asarray(c['kd'])*(command[-1,2:]-x[-1,2:4]),-c['torque_limit'],c['torque_limit'])
    if not np.isfinite(x).all() or np.max(np.abs(x[:,:2]))>np.pi or np.max(np.abs(x[:,2:4]))>10:raise ValueError('Invalid physical trajectory')
    return x

def make_components(y,u,valid,following,bank,fit,settings):
    out=components(y,u,valid,following,bank,fit,settings)
    out['return_nomargin']=np.all(np.abs(y-bank[:,1])<=settings['physical_tolerance']*fit['scale'],axis=1)
    out['jump']=out['mode'].astype(bool)&~np.r_[False,out['mode'][:-1].astype(bool)]
    b=score_matrix(out,fit['mode_scales']);f=b[:,7]
    out['scores']=np.column_stack([b,f,f,out['base'][:,6]/fit['error_means'][4],f,b[:,3],f,f,f,f,out['base'][:,3]/fit['error_means'][3]])
    assert out['scores'].shape==(len(y),23)
    return out

def decide(comp,j,h,settings):
    s=comp['scores'][:,j];v=comp['valid'];r=comp['return_ok'];d=settings['recovery_dwell']
    if j<13:return old_decision(s,j,v,r,h,settings)
    if j==18:return s>h,~v
    if j in [17,19]:return stateful(s,v,h,d),~v
    if j==16:
        alarm=False;count=0;out=np.zeros(len(s),dtype=bool)
        for t,value in enumerate(s):
            if not v[t]:count=0
            else:
                if comp['jump'][t]:alarm=False;count=0
                if value>h:alarm=True;count=0
                elif alarm:
                    count=count+1 if value<=.5*h else 0
                    if count>=d:alarm=False;count=0
            out[t]=alarm
        return out,~v
    if j in [13,20]:d=1
    if j in [14,21]:r=comp['return_nomargin']
    return stateful(s,v,h,d,r),~v

def calibrate7(eps,j,c):
    candidates=np.unique(np.r_[0.,np.concatenate([e['scores'][:,j] for e in eps])]);cache={}
    def count(i):
        if i not in cache:
            n=0
            for e in eps:
                a,u=decide(e,j,candidates[i],permitted(c));n+=int((a&~u)[c['warmup']:].sum())
            cache[i]=n
        return cache[i]
    lo=0;hi=len(candidates)-1
    assert count(hi)<=162
    while lo<hi:
        mid=(lo+hi)//2
        if count(mid)<=162:hi=mid
        else:lo=mid+1
    assert lo==0 or count(lo-1)>162
    return dict(threshold=float(candidates[lo]),alarms=count(lo),preceding_alarms=count(lo-1) if lo else None,
        probes=[dict(index=i,threshold=float(candidates[i]),alarms=v) for i,v in sorted(cache.items())])
