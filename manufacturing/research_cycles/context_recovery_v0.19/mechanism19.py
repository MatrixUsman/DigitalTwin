"""Frozen contextual empirical envelopes; no truth or online fitting."""
import numpy as np

START=100
METHODS=['base_dual','base_dual_nodwell','rbf_dual','rbf_dual_nodwell',
         'following_point','tolerance_point','entry_3of5','global_set',
         'context_point','context_hysteresis','context_set']

def context(commands,scale,memory):
    u=np.asarray(commands,float);scale=np.asarray(scale,float)
    if u.ndim!=2 or u.shape[1]!=4 or scale.shape!=(4,) or np.any(scale<=0) or not np.isfinite(scale).all() or not np.isfinite(memory) or memory<=0 or not np.isfinite(u).all():
        raise ValueError('Invalid observed command context')
    d=np.r_[0.,np.max(np.abs(np.diff(u,axis=0)/scale),axis=1)]
    h=np.zeros(len(u));decay=np.exp(-1./memory)
    for t in range(1,len(u)):h[t]=max(d[t],decay*h[t-1])
    return h

def quantile(scores,q=.99):
    x=np.asarray(scores,float)
    if not len(x) or not np.isfinite(x).all():raise ValueError('Empty/nonfinite calibration')
    return float(np.sort(x)[int(np.ceil(q*len(x)))-1])

def fit_envelope(training,calibration,scale,memory):
    h=np.concatenate([context(u,scale,memory)[START:] for u,s in training])
    edges=np.quantile(h,[.9,.99]).tolist()
    hh=np.concatenate([context(u,scale,memory)[START:] for u,s in calibration])
    ss=np.concatenate([s[START:] for u,s in calibration]);which=np.searchsorted(edges,hh,side='right')
    glob=quantile(ss);counts=[];width=[]
    for j in range(3):
        part=ss[which==j];counts.append(len(part));width.append(quantile(part) if len(part)>=30 else glob)
    return dict(memory=memory,edges=edges,width=width,counts=counts,global_width=glob,training_max_context=float(h.max()),
                calibration_points=len(ss),training_points=len(h),quantile=.99,fallback_minimum=30)

def widths(commands,scale,model):
    h=context(commands,scale,model['memory']);ids=np.searchsorted(model['edges'],h,side='right')
    return np.asarray(model['width'])[ids]

def set_alarm(score,b,delta=.1,kind='set',start=START):
    s=np.asarray(score,float);b=np.broadcast_to(np.asarray(b,float),s.shape)
    if np.any(b<0) or not np.isfinite(s).all() or not np.isfinite(b).all():raise ValueError('Invalid empirical envelope')
    lower=np.maximum(0,s-b);upper=s+b;enter=lower>delta
    clear=(upper<=delta) if kind=='set' else (s<=delta)
    a=np.zeros(len(s),bool);active=False
    for t in range(start,len(s)):
        if enter[t]:active=True
        elif clear[t]:active=False
        a[t]=active
    return a,lower,upper

def alarms(residual,scores,valid,threshold,scale,commands,model,gate_module):
    if not np.asarray(valid).all():raise ValueError('Incomplete context not admitted')
    known=np.ones(len(valid),bool);known[:START]=False;parts=[]
    for role,idx,dwell in [('base',0,10),('base',0,1),('rbf',2,10),('rbf',2,1)]:
        ev,_=gate_module.return_evidence(residual[:,idx],valid,windows=[5,41],tolerance=.1,start=START)
        parts.append(gate_module.alarm_machine(scores[:,idx],known,ev,threshold[role],dwell))
    s=scores[:,0];point=(s>threshold['base'])&known
    parts.append((scores[:,3]>threshold['following'])&known)
    parts.append((s>.1)&known)
    counts=np.convolve(point.astype(int),np.ones(5,int),'full')[:len(s)]
    parts.append((counts>=3)&known)
    b=widths(commands,scale,model)
    parts.append(set_alarm(s,model['global_width'])[0])
    parts.append((np.maximum(0,s-b)>.1)&known)
    parts.append(set_alarm(s,b,kind='hysteresis')[0])
    a,lower,upper=set_alarm(s,b);parts.append(a)
    return np.stack(parts,axis=1),b,lower,upper

def extra_metrics(alarm,attack,state,truth,scale,dt=.02,delta=.1,start=START):
    a=np.asarray(alarm,bool);attack=np.asarray(attack,bool);distance=np.max(np.abs((state-truth)/scale),axis=1)
    outside=distance>delta;outside[:start]=False
    after=np.flatnonzero(attack)
    if len(after):outside[:after[0]]=False
    inactive=int((outside&~a).sum());total=int(outside.sum())
    padded=np.r_[False,a[start:],False];rises=np.flatnonzero(np.diff(padded.astype(int))==1);falls=np.flatnonzero(np.diff(padded.astype(int))==-1)
    duration=(falls-rises)*dt
    return dict(outside_points=total,outside_inactive=inactive,
                outside_inactive_fraction=inactive/total if total else None,
                alarm_durations_seconds=duration.tolist(),outside_max=float(distance[start:].max()))

def distributions(values):
    x=np.asarray([v for v in values if v is not None],float)
    return dict(n=len(x),median=float(np.median(x)) if len(x) else None,
                p95=float(np.quantile(x,.95)) if len(x) else None,max=float(x.max()) if len(x) else None)

def summarize(rows):
    result=[]
    groups=[('pooled','all')]+[(key,v) for key in ['plant','task','condition','plant_group'] for v in sorted({r[key] for r in rows})]
    for key,value in groups:
        for method in METHODS:
            rr=[r for r in rows if r['method']==method and (key=='pooled' or r[key]==value)]
            benign=[r for r in rr if r['benign']];attack=[r for r in rr if r['event']]
            n=sum(r['eligible'] for r in benign);points=sum(r['alarm_points'] for r in benign);starts=sum(r['alarm_episodes'] for r in benign)
            outside=sum(r['outside_points'] for r in attack);missing=sum(r['outside_inactive'] for r in attack)
            durations=[v for r in benign for v in r['alarm_durations_seconds']]
            tp,fp,fn=[sum(r[k] for r in rr) for k in ['tp','fp','fn']]
            result.append(dict(group=key,value=value,method=method,episodes=len(rr),benign_points=n,benign_alarms=points,
                occupancy=points/n if n else None,starts=starts,benign_hours=n*.02/3600,
                starts_per_hour=starts/(n*.02/3600) if n else None,alarm_duration=distributions(durations),events=len(attack),
                hits=sum(r['overlap'] for r in attack),fresh=sum(r['fresh'] for r in attack),misses=sum(not r['overlap'] for r in attack),
                joint=sum(r['joint'] for r in attack),outside_points=outside,outside_inactive=missing,
                outside_inactive_fraction=missing/outside if outside else 0.,absent_return=sum(r['return_missing'] for r in attack),
                inactive_by_return_plus_5=sum(r['clear_timely'] for r in attack),already_inactive_at_return=sum(r['already_clear_at_return'] for r in attack),
                detection_delay=distributions([r['detection_delay'] for r in attack]),fresh_delay=distributions([r['fresh_delay'] for r in attack]),
                clearance_delay=distributions([r['clear_delay'] for r in attack]),f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0))
    return result

def criterion(summary):
    d={r['method']:r for r in summary if r['group']=='pooled'};a=d['context_set'];base=d['base_dual'];h=d['context_hysteresis']
    reductions={k:1-a[k]/base[k] if base[k] else None for k in ['benign_alarms','starts']}
    clauses={'occupancy_20pct':reductions['benign_alarms'] is not None and reductions['benign_alarms']>=.2,
             'starts_10pct':reductions['starts'] is not None and reductions['starts']>=.1}
    for name,b in [('base',base),('matched_hysteresis',h)]:
        clauses[name+'_fresh_not_lower']=a['fresh']>=b['fresh']
        clauses[name+'_outside_not_worse']=a['outside_inactive_fraction']<=b['outside_inactive_fraction']
        clauses[name+'_joint_not_lower']=a['joint']>=b['joint']
        x,y=a['fresh_delay']['p95'],b['fresh_delay']['p95'];clauses[name+'_delay_cost']=x is not None and y is not None and x<=y+.2
    clauses['recovery_component_gain']=a['outside_inactive']<h['outside_inactive'] or a['joint']>h['joint']
    return dict(passed=all(clauses.values()),clauses=clauses,relative_reductions=reductions,novelty_established=False)
