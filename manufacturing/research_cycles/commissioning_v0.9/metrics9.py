"""Normal error and clearance opportunities, never attack-detection metrics."""
import numpy as np

def errors(y,pred,scale,warmup):
    z=(y-pred)/scale;s=np.max(np.abs(z),axis=1);a=s[warmup:]
    return s,dict(eligible=len(a),maximum=float(a.max()),q95=float(np.quantile(a,.95)),q99=float(np.quantile(a,.99)),
                  q999=float(np.quantile(a,.999)),standardized_rmse=float(np.sqrt(np.mean(z[warmup:]**2))),
                  channel_standardized_rmse=np.sqrt(np.mean(z[warmup:]**2,axis=0)).tolist())

def opportunities(score,b,c):
    ok=score+b<=c['return_tolerance'];probes=[]
    for start in c['probe_indices']:
        count=0;found=None
        for t in range(start,min(start+c['max_clear_steps']+1,len(score))):
            count=count+1 if ok[t] else 0
            if count>=c['dwell']:found=t;break
        probes.append(dict(start=start,cleared_at=found,delay_steps=None if found is None else found-start))
    return dict(allowance=float(b),algebraically_feasible=bool(b<c['return_tolerance']),
                feasible_points=int(ok[c['warmup']:].sum()),eligible=len(ok)-c['warmup'],
                cleared_probes=sum(p['cleared_at'] is not None for p in probes),probes=probes)

def summarize(rows,c):
    result=[]
    for plant in ['Q1','Q2','Q3']:
        for role in sorted({r['role'] for r in rows}):
            r=[v for v in rows if v['plant']==plant and v['role']==role]
            if not r:continue
            n=sum(v['eligible'] for v in r);fp=sum(v['feasible_points'] for v in r);probes=sum(len(v['probes']) for v in r);cleared=sum(v['cleared_probes'] for v in r)
            result.append(dict(plant=plant,role=role,model=r[0]['model'],episodes=len(r),eligible=n,allowance=r[0]['allowance'],
                 maximum=max(v['maximum'] for v in r),worst_episode_q99=max(v['q99'] for v in r),
                 mean_standardized_rmse=float(np.mean([v['standardized_rmse'] for v in r])),
                 feasible_points=fp,feasible_fraction=fp/n,cleared_probes=cleared,probes=probes,clearance_fraction=cleared/probes,
                 normal_admission=bool(r[0]['algebraically_feasible'] and fp/n>=c['admission_fraction'] and cleared/probes>=c['admission_fraction'])))
    selected=[r for r in result if r['role']=='selected_reference']
    return dict(rows=result,selected_reference_admitted_to_alarm_design=bool(len(selected)==3 and all(r['normal_admission'] for r in selected)),
                qualification='Necessary empirical normal-only feasibility; no attack recovery, novelty or safety guarantee.')
