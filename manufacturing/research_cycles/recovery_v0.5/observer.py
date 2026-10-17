"""Label-free observer, ordinary predictors and explicit recovery decisions."""
import numpy as np
from plant import advance


def predictions(y,context,cfg):
    n=len(y);following=np.empty_like(y);reference=np.empty_like(y)
    initial=np.r_[0.,cfg['amplitude'][1]*np.sin(cfg['phase_offset']),0.,0.]
    following[0]=initial;reference[0]=initial;gain=np.asarray(cfg['observer_gain'])
    for t in range(n-1):
        corrected=following[t]+gain*(y[t]-following[t])
        following[t+1]=advance(corrected,context[t],cfg['nominal'],cfg)
        reference[t+1]=advance(reference[t],context[t],cfg['nominal'],cfg)
    return following,reference


def design(y,u,order,context):
    rows=np.arange(order,len(y));x=y[rows[:,None]+np.arange(-order,0)].reshape(len(rows),-1)
    if context:x=np.column_stack([x,u[rows-1]])
    return np.column_stack([x,np.ones(len(x))]),rows


def fit_linear(episodes,mean,scale,cfg,context):
    xx=xy=None
    for ep in episodes:
        y=(ep['measurements']-mean)/scale;x,t=design(y,ep['available'],cfg['ar_order'],context)
        eligible=t>=cfg['warmup'];x=x[eligible];target=y[t[eligible]]
        xx=x.T@x if xx is None else xx+x.T@x;xy=x.T@target if xy is None else xy+x.T@target
    n=len(episodes)*(cfg['steps']-cfg['warmup']);pen=np.eye(len(xx))*cfg['ridge'];pen[-1,-1]=0
    return np.linalg.solve(xx/n+pen,xy/n)


def errors(ep,following,reference,fit,cfg):
    y=ep['measurements'];z=(y-fit['mean'])/fit['scale'];n=len(y)
    energy=np.empty((n,5));energy[0,0]=0.;energy[1:,0]=np.mean(np.diff(z,axis=0)**2,axis=1)
    for j,context in [(1,False),(2,True)]:
        x,t=design(z,ep['available'],cfg['ar_order'],context)
        energy[:cfg['ar_order'],j]=0.
        energy[t,j]=np.mean((x@fit['arx' if context else 'ar']-z[t])**2,axis=1)
    energy[:,3]=np.mean(((following-y)/fit['scale'])**2,axis=1)
    energy[:,4]=np.mean(((reference-y)/fit['scale'])**2,axis=1)
    if not np.isfinite(energy).all():raise ValueError('Invalid errors')
    return energy


def scores(energy,fit,cfg):
    f=energy[:,3];total=np.r_[0.,np.cumsum(f)];end=np.arange(1,len(f)+1);start=np.maximum(end-45,0)
    mean45=(total[end]-total[start])/(end-start)
    c=np.cumsum(np.minimum(f/fit['error_means'][3],cfg['cusum_cap'])-cfg['cusum_drift'])
    cusum=c-np.minimum.accumulate(np.minimum(c,0))
    fused=np.maximum(f/fit['error_means'][3],energy[:,4]/fit['error_means'][4])
    return np.column_stack([energy[:,:4],mean45,cusum,energy[:,4],fused])


def hysteresis(score,valid,high,low,dwell):
    alarm=False;count=0;out=np.zeros(len(score),dtype=bool);counter=np.zeros(len(score),dtype=int)
    for t,s in enumerate(score):
        if not valid[t]:count=0
        elif s>high:alarm=True;count=0
        elif alarm:
            count=count+1 if s<=low else 0
            if count>=dwell:alarm=False;count=0
        out[t]=alarm;counter[t]=count
    return out,counter


def candidate(zf,zr,valid,high,low,dwell):
    """Separate two-evidence implementation; intentionally test its equivalence."""
    latched=False;agree=0;out=[];counts=[]
    for f,r,ok in zip(zf,zr,valid):
        if not ok:agree=0
        elif f>high or r>high:latched=True;agree=0
        elif latched:
            if f<=low and r<=low:agree+=1
            else:agree=0
            if agree==dwell:latched=False;agree=0
        out.append(latched);counts.append(agree)
    return np.asarray(out),np.asarray(counts)


def decisions(stream,energy,fit,thresholds,valid,cfg):
    alarm=stream>thresholds;unknown=np.zeros((len(stream),11),dtype=bool)
    # Any command-dependent prediction becomes uncertain when context is unavailable.
    unknown[:,[2,3,4,5,6,7,8,9,10]]=~valid[:,None]
    follow,_=hysteresis(stream[:,3],valid,thresholds[3],thresholds[3]*cfg['low_threshold_fraction'],cfg['recovery_dwell'])
    fused,counter=hysteresis(stream[:,7],valid,thresholds[7],thresholds[7]*cfg['low_threshold_fraction'],cfg['recovery_dwell'])
    proposed,proposal_counter=candidate(energy[:,3]/fit['error_means'][3],energy[:,4]/fit['error_means'][4],valid,
        thresholds[7],thresholds[7]*cfg['low_threshold_fraction'],cfg['recovery_dwell'])
    if not np.array_equal(fused,proposed) or not np.array_equal(counter,proposal_counter):raise ValueError('Algebraic equivalence violated')
    return np.column_stack([alarm,follow,fused,proposed]),unknown,proposal_counter


def outcome(alarm,unknown,attack,authorized,state,reference,scale,cfg):
    start=cfg['warmup'];a=alarm & ~unknown;eligible=np.arange(len(a))>=start
    pos=attack & eligible;neg=~attack & eligible
    tp=int((a&pos).sum());fn=int(pos.sum())-tp;fp=int((a&neg).sum())
    # Restoring visibility of a retained alarm is not a fresh detection.
    rises=alarm & ~np.r_[False,alarm[:-1]] & ~unknown & ~np.r_[False,unknown[:-1]]
    indices=np.flatnonzero(pos)
    row={'tp':tp,'fp':fp,'fn':fn,'precision':tp/(tp+fp) if tp+fp else 0.,'recall':tp/(tp+fn) if tp+fn else None,
         'f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.,'eligible':int(eligible.sum()),
         'unknown':int((unknown&eligible).sum()),'coverage':float((~unknown)[eligible].mean()),
         'normal_points':int(neg.sum()),'normal_alarms':fp,'normal_known_points':int((neg&~unknown).sum()),
         'normal_alarm_fraction_full':fp/int(neg.sum()),'normal_alarm_fraction_known':fp/int((neg&~unknown).sum()) if (neg&~unknown).sum() else None,
         'normal_episodes':int((rises&neg).sum()),'authorized_alarms':int((a&authorized&eligible).sum()),
         'attack_present':bool(len(indices)),'overlap_hit':False,'fresh_hit':False,'delay_steps':None,'fresh_delay_steps':None,
         'post_alarm_points':None,'post_points':None,'first_clear_steps':None,'clear_while_corruption':0,'physical_return_steps':None}
    if len(indices):
        onset,end=indices[0],indices[-1]+1;hits=np.flatnonzero(a[onset:end]);fresh=np.flatnonzero(rises[onset:end])
        stop=min(len(a),end+250);clear=np.flatnonzero(~alarm[end:stop]&~unknown[end:stop])
        # Diagnostic only: distance from actual plant state to the approved-command nominal reference.
        distance=np.max(np.abs((state-reference)/scale),axis=1)
        returned=None
        for t in range(end,stop-cfg['recovery_dwell']+1):
            if np.all(distance[t:t+cfg['recovery_dwell']]<=.1):returned=int(t-end);break
        falls=alarm[:-1]&~alarm[1:]&~unknown[1:]&~unknown[:-1]
        row.update(overlap_hit=bool(len(hits)),fresh_hit=bool(len(fresh)),delay_steps=int(hits[0]) if len(hits) else None,
            fresh_delay_steps=int(fresh[0]) if len(fresh) else None,post_alarm_points=int(a[end:stop].sum()),post_points=stop-end,
            first_clear_steps=int(clear[0]) if len(clear) and len(hits) else None,clear_while_corruption=int(falls[onset:end-1].sum()),
            physical_return_steps=returned)
    return row
