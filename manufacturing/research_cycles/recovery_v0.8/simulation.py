"""Synthetic generators. Truth and counterfactuals are evaluator-only."""
import numpy as np
from common import permitted
from v7_core import physical
from core import following_predictions,trajectory

def path(t,rate,task):
    f=task['frequency'];kind=task['kind']
    if kind=='chirp8':theta=f*t+.008*t*t;speed=f+.016*t
    elif kind=='modulated8':theta=f*t+.18*np.sin(.31*t);speed=f+.18*.31*np.cos(.31*t)
    else:theta=f*t;speed=np.full_like(t,f)
    a,b=task['amplitude'];phi=task['phase']
    q=np.column_stack([a*np.sin(theta)+.025*np.sin(2.3*theta),b*np.sin(theta+phi)+.018*np.sin(1.7*theta)])
    v=np.column_stack([a*np.cos(theta)+.0575*np.cos(2.3*theta),b*np.cos(theta+phi)+.0306*np.cos(1.7*theta)])*(speed*rate)[:,None]
    return np.column_stack([q,v])

def commands(c,task,condition):
    n=c['steps'];t=np.arange(n)*c['dt'];rate=np.ones(n);a,b=c['onset'],c['end']
    base=path(t,rate,task);approved=base.copy();executed=base.copy();attack=np.zeros(n,bool);authorized=attack.copy();valid=~attack
    if condition in ['authorized_slow','slow']:
        rate[a:b]=c['slow_rate'];s=np.r_[0,np.cumsum(rate[:-1])]*c['dt'];executed=path(s,rate,task)
        if condition=='slow':executed[b:]=base[b:];attack[a:b]=True
        else:approved=executed.copy();authorized[a:b]=True
    elif condition in ['authorized_offset','brief_offset','persistent_offset','context_gap_offset']:
        stop=a+c['brief_length'] if condition=='brief_offset' else b;executed[a:stop,0]+=c['offset_radians']
        if condition=='authorized_offset':approved=executed.copy();authorized[a:stop]=True
        else:attack[a:stop]=True
        if condition=='context_gap_offset':valid[a:c['context_gap_end']]=False
    elif condition=='hold':executed[a:b,:2]=base[a-1,:2];executed[a:b,2:]=0.;attack[a:b]=True
    elif condition!='normal':raise ValueError(condition)
    available=approved.copy()
    for t in range(1,n):
        if not valid[t]:available[t]=available[t-1]
    return dict(approved=approved,available=available,executed=executed,valid=valid,attack=attack,authorized=authorized)

def plant_parameters(c,p):
    a=dict(c['nominal']);a.update(l1=p['lengths'][0],l2=p['lengths'][1])
    a['m1']*=p['mass'][0];a['m2']*=p['mass'][1];a['b']=(np.asarray(a['b'])*p['damping']).tolist();return a

def generate(c,task,p,condition,seed,cache):
    ep=commands(c,task,condition);initial=np.r_[ep['approved'][0,:2],0.,0.];pars=plant_parameters(c,p);setting=permitted(c)
    def sim(u):
        key=(p['id'],u.tobytes())
        if key not in cache:cache[key]=physical(initial,u,pars,setting,p['lag'])[:,:4]
        return cache[key]
    state=sim(ep['executed']);truth_reference=sim(ep['approved'])
    noise=np.random.default_rng(seed).normal(size=state.shape)*np.asarray(c['sensor_sigma'])*p['noise']
    return dict(**ep,state=state,truth_reference=truth_reference,measurements=state+noise)

def monitor_inputs(ep,fit,c):
    from mechanism import reference,scalar
    y=ep['measurements'];u=ep['available'];valid=ep['valid'];scale=fit['scale']
    settings=permitted(c);initial=np.r_[u[0,:2],0.,0.]
    # Known initial approved pose, zero initial velocity, common to physical controls.
    nominal=trajectory(initial,u,c['nominal'],settings)
    following=following_predictions(y,u,dict(settings,amplitude=[0.,float(u[0,1])],phase_offset=np.pi/2))
    learned=reference(y,u,fit);one=reference(y,u,fit,follow=True)
    pr=np.r_[0.,scalar(y[1:],y[:-1],scale)]
    er=scalar(y,learned,scale);en=scalar(y,nominal,scale);ef=scalar(y,following,scale);ea=scalar(y,one,scale)
    scores=np.column_stack([pr,ea,ef,ef,en,en,er,er,er,er,er,er,er])
    return dict(scores=scores,nominal_error=en,learned_error=er,reference=learned,nominal_reference=nominal,
                following=following,one_step=one,valid=valid.copy())

def commissioning_task(i):
    return dict(id=f'T{i}',kind='multisine8',amplitude=[.22+.04*i,.34-.025*i],frequency=[.35,.7,1.1][i],phase=.5+.3*i)

def calibration_task(i):
    return dict(id=f'C{i}',kind='multisine8',amplitude=[.23+.012*(i%7),.29+.013*(i%9)],frequency=.32+.047*i,phase=.4+.06*(i%11))
