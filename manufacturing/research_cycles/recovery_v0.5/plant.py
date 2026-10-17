"""Synthetic horizontal 2R point-mass arm. SI units; no real-robot interface."""
import numpy as np


def mass(q,p):
    a=p['m2']*p['l1']*p['l2'];cc=np.cos(q[1]);d=p['m2']*p['l2']**2
    return np.array([[(p['m1']+p['m2'])*p['l1']**2+d+2*a*cc,d+a*cc],[d+a*cc,d]])


def coriolis(q,v,p):
    a=p['m2']*p['l1']*p['l2']*np.sin(q[1])
    return np.array([-a*(2*v[0]*v[1]+v[1]**2),a*v[0]**2])


def derivative(x,command,p,cfg,free=False):
    q=x[:2];v=x[2:]
    tau=np.zeros(2) if free else np.clip(np.asarray(cfg['kp'])*(command[:2]-q)+np.asarray(cfg['kd'])*(command[2:]-v),-cfg['torque_limit'],cfg['torque_limit'])
    rhs=tau-coriolis(q,v,p)-np.asarray(p['b'])*v
    mat=mass(q,p);det=mat[0,0]*mat[1,1]-mat[0,1]**2
    acc=np.array([(mat[1,1]*rhs[0]-mat[0,1]*rhs[1])/det,(mat[0,0]*rhs[1]-mat[0,1]*rhs[0])/det])
    return np.r_[v,acc]


def advance(x,command,p,cfg,substeps=None,free=False):
    x=np.asarray(x,dtype=np.float64).copy();n=cfg['substeps'] if substeps is None else substeps;dt=cfg['dt']/n
    for _ in range(n):
        a=derivative(x,command,p,cfg,free);b=derivative(x+dt*a/2,command,p,cfg,free)
        c=derivative(x+dt*b/2,command,p,cfg,free);d=derivative(x+dt*c,command,p,cfg,free)
        x+=dt*(a+2*b+2*c+d)/6
    if not np.isfinite(x).all():raise ValueError('Nonfinite simulated state')
    return x


def kinetic(x,p):return float(x[2:]@mass(x[:2],p)@x[2:]/2)


def tip(q,p):
    return np.array([p['l1']*np.cos(q[0])+p['l2']*np.cos(q[0]+q[1]),
                     p['l1']*np.sin(q[0])+p['l2']*np.sin(q[0]+q[1])])


def commands(cfg,condition):
    n=cfg['steps'];base_phase=np.arange(n)*cfg['dt']*cfg['frequency']
    rate=np.ones(n);start,end=cfg['onset'],cfg['end']
    if condition in ['authorized_slow','slow']:rate[start:end]=cfg['slow_rate']
    phase=np.r_[0.,np.cumsum(rate[:-1])]*cfg['dt']*cfg['frequency']
    def trajectory(ph,r):
        q=np.column_stack([cfg['amplitude'][0]*np.sin(ph),cfg['amplitude'][1]*np.sin(ph+cfg['phase_offset'])])
        v=np.column_stack([cfg['amplitude'][0]*np.cos(ph),cfg['amplitude'][1]*np.cos(ph+cfg['phase_offset'])])*r[:,None]*cfg['frequency']
        return np.column_stack([q,v])
    baseline=trajectory(base_phase,np.ones(n));executed=baseline.copy();approved=baseline.copy()
    attack=np.zeros(n,dtype=bool);valid=np.ones(n,dtype=bool);authorized=np.zeros(n,dtype=bool)
    if condition in ['authorized_slow','slow']:
        executed=trajectory(phase,rate)
        # Rejoin approved schedule when unauthorized corruption ends; authorized
        # slowdown retains its legitimate accumulated phase delay.
        if condition=='slow':executed[end:]=baseline[end:];attack[start:end]=True
        else:approved=executed.copy();authorized[start:end]=True
    elif condition in ['authorized_offset','brief_offset','persistent_offset','context_gap_offset']:
        stop=start+cfg['brief_length'] if condition=='brief_offset' else end
        executed[start:stop,0]+=cfg['offset_radians']
        if condition=='authorized_offset':approved=executed.copy();authorized[start:stop]=True
        else:attack[start:stop]=True
        if condition=='context_gap_offset':valid[start:cfg['context_gap_end']]=False
    elif condition=='hold':
        executed[start:end,:2]=baseline[start-1,:2];executed[start:end,2:]=0.;attack[start:end]=True
    elif condition!='normal':raise ValueError('Unknown scenario')
    # The monitor receives held-last approved context while validity is false.
    available=approved.copy()
    for t in range(1,n):
        if not valid[t]:available[t]=available[t-1]
    return approved,available,executed,valid,attack,authorized


def simulate(cfg,p,condition,seed,role):
    approved,available,executed,valid,attack,authorized=commands(cfg,condition)
    n=cfg['steps'];state=np.empty((n,4));state[0]=np.r_[approved[0,:2],0.,0.]
    for t in range(n-1):state[t+1]=advance(state[t],executed[t],p,cfg)
    if np.max(np.abs(state[:,:2]))>np.pi or np.max(np.abs(state[:,2:]))>10:raise ValueError('Pilot state bounds exceeded')
    offsets={'train':10000,'calibration':20000,'evaluation':30000}
    # Matching seeds intentionally pair conditions and plant variants.
    noise=np.random.default_rng(seed+offsets[role]).normal(size=state.shape)*np.asarray(cfg['sensor_sigma'])
    return dict(state=state,measurements=state+noise,approved=approved,available=available,executed=executed,
                valid=valid,attack=attack,authorized=authorized,tip=np.stack([tip(q,p) for q in state[:,:2]]),
                time=np.arange(n)*cfg['dt'])
