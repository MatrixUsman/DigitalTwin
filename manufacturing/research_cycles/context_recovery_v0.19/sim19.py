"""New synthetic trajectories and predeclared plant transfer conditions."""
import numpy as np

def path(t,rate,task):
    a,b=task['amplitude'];f=task['frequency'];phi=task['phase']
    if task['kind']=='lissajous':
        q=np.column_stack([a*np.sin(f*t),b*np.sin(1.37*f*t+phi)])
        v=np.column_stack([a*f*np.cos(f*t),b*1.37*f*np.cos(1.37*f*t+phi)])*rate[:,None]
    elif task['kind']=='smoothstep':
        arrays=[];derivatives=[]
        for amp,offset in [(a,0),(b,phi)]:
            phase=t*f+offset;k=np.floor(phase).astype(int);x=phase-k
            s=10*x**3-15*x**4+6*x**5;ds=(30*x**2-60*x**3+30*x**4)*f
            sign=np.where(k%2==0,1.,-1.);arrays.append(amp*sign*(2*s-1));derivatives.append(2*amp*sign*ds*rate)
        q=np.column_stack(arrays);v=np.column_stack(derivatives)
    else:raise ValueError('Unknown new family')
    return np.column_stack([q,v])

def commands(n,task,condition,dt=.02):
    t=np.arange(n)*dt;rate=np.ones(n);base=path(t,rate,task);approved=base.copy();executed=base.copy()
    attack=np.zeros(n,bool);authorized=attack.copy();a=task['onset'];b=a+task['duration']
    if condition=='authorized_changes':
        for lo,hi,amount in [(600,900,.07),(2000,2300,-.09),(4000,4400,.05)]:
            if lo<n:executed[lo:min(hi,n),0]+=amount;authorized[lo:min(hi,n)]=True
        approved=executed.copy()
    elif condition in ['brief_offset','persistent_offset']:
        end=a+task['brief'] if condition=='brief_offset' else b
        executed[a:end,0]+=task['offset'];attack[a:end]=True
    elif condition=='hold':executed[a:b,:2]=base[a-1,:2];executed[a:b,2:]=0.;attack[a:b]=True
    elif condition=='slow':
        rate[a:b]=task['slow'];phase=np.r_[0.,np.cumsum(rate[:-1])]*dt
        executed=path(phase,rate,task);executed[b:]=base[b:];attack[a:b]=True
    elif condition!='normal':raise ValueError('Unknown condition')
    return dict(approved=approved,available=approved.copy(),executed=executed,attack=attack,authorized=authorized,valid=np.ones(n,bool))

def generate(config,task,plant,condition,seed,physical,parameters,permitted,cache,n=None):
    n=n or (6000 if condition in ['normal','authorized_changes'] else 2400)
    ep=commands(n,task,condition);initial=np.r_[ep['approved'][0,:2],0.,0.]
    pars=parameters(config,plant);setting=permitted(config)
    def sim(u):
        key=(plant['id'],u.tobytes())
        if key not in cache:cache[key]=physical(initial,u,pars,setting,plant['lag'])[:,:4]
        return cache[key]
    state=sim(ep['executed']);truth=sim(ep['approved'])
    noise=np.random.default_rng(seed).normal(size=state.shape)*np.asarray(config['sensor_sigma'])*plant['noise']
    return dict(**ep,state=state,truth_reference=truth,measurements=state+noise)
