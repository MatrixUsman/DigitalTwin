"""Fresh-process inference checks and separately written outcome arithmetic."""
import argparse
from datetime import datetime, timezone
import json
import re
import sys
from pathlib import Path
import numpy as np
from common import HERE,PROJECT,LOCAL,UPSTREAM,sha,check_freeze,load_source,predictor
from mechanism import perturb
from mfg_twin.supervisor import BudgetWriter, Limits, supervise, install_worker_limits, worker_usage

LIMITS=Limits(wall_seconds=180,cpu_seconds=120,rss_bytes=1073741824,output_bytes=10485760)


def independent_scores(x,mean,cfg):
    out=np.empty((len(x),4));out[:,0]=x
    for k,w in [(1,45),(2,450)]:
        out[:,k]=np.convolve(x,np.ones(w),mode='full')[:len(x)]/np.minimum(np.arange(1,len(x)+1),w)
    state=0.
    for t,e in enumerate(x):
        state=max(0.,state+min(e/mean,cfg['cusum_increment_cap'])-cfg['cusum_drift'])
        out[t,3]=state
    return out


def verify(run,output):
    install_worker_limits(LIMITS);f=check_freeze();cfg=f['configuration'];checks=[]
    def check(name,value):checks.append({'name':name,'passed':bool(value)})
    source,values,indices,raw=load_source(cfg)
    roster=json.loads((run/'cases.json').read_text());cal=json.loads((run/'calibration.json').read_text())
    rows=json.loads((run/'case_outcomes.json').read_text());norm=json.loads((run/'normal_outcomes.json').read_text())
    records={(r['model'],r['id'],r['score']):r for r in rows}
    check('189_cases_4536_unique_outcomes',len(roster)==189 and len(rows)==4536 and len(records)==4536)
    seal=json.loads((run/'SCORES_SEALED.json').read_text())
    for p,h in seal['sha256'].items():check('seal:'+p,sha(run/p)==h)
    check('label_join_after_seal',not seal['outcomes_computed'])
    for name in cfg['models']:
        with np.load(run/(name+'_normal.npz'),allow_pickle=False) as a:
            energy=a['energy'];normal_streams=a['streams'];check(name+':coordinates',np.array_equal(a['raw_indices'],raw))
        mean=float(np.sum(energy[:4096])/4096)
        check(name+':scale',mean==cal[name]['normal_mean'])
        normal_ref=independent_scores(energy,mean,cfg)
        check(name+':normal_scores',np.allclose(normal_streams,normal_ref,rtol=1e-10,atol=2e-9))
        thresholds=np.asarray(cal[name]['thresholds'])
        check(name+':thresholds',np.array_equal(np.sort(normal_streams[4096:8192],axis=0)[4055],thresholds))
        for k,s in enumerate(cfg['scores']):
            row=next(x for x in norm if x['model']==name and x['score']==s)
            a=normal_ref[:,k]>thresholds[k]; rises=np.flatnonzero(np.diff(np.r_[False,a].astype(int))==1)
            check(name+':normal_metrics:'+s,row['alarm_points']==int(a[8192:].sum()) and row['episodes']==int(np.sum((rises>=8192)&(rises<16384))))
        with np.load(source/(name+'_scores.npz'),allow_pickle=False) as a:base=a['predictions'].astype(np.float64)
        forward=predictor(name,json.loads((UPSTREAM/'config.json').read_text()),source)
        with np.load(run/(name+'_overrides.npz'),allow_pickle=False) as overrides:
            for case_number,c in enumerate(roster):
                start=c['onset'];end=start+c['duration'];stop=end+45;tag=name+':'+c['id']
                y=perturb(values,45+start,c['duration'],c['family'],c['magnitude'])
                pred=overrides[c['id']+'_predictions'];changed=overrides[c['id']+'_energy'];oracle=overrides[c['id']+'_oracle_energy']
                target=y[indices[start:stop]].astype(np.float64)
                check(tag+':finite_shape',pred.shape==(stop-start,9) and np.isfinite(pred).all())
                check(tag+':energy',np.allclose(np.sum((pred-target)**2,axis=1)/9,changed,rtol=1e-13,atol=1e-14))
                check(tag+':oracle',np.allclose(np.sum((base[start:stop]-target)**2,axis=1)/9,oracle,rtol=1e-13,atol=1e-14))
                if case_number==0:
                    full=forward(y,indices).astype(np.float64)
                    check(tag+':full_vs_optimized',np.allclose(full[start:stop],pred,rtol=1e-6,atol=1e-6))
                    check(tag+':unaffected_prediction_support',np.array_equal(full[:start],base[:start]) and np.array_equal(full[stop:],base[stop:]))
                if name=='mean':check(tag+':history_independent',np.array_equal(changed,oracle))
                if name=='persistence' and c['family']=='hold' and c['magnitude']==1:
                    check(tag+':constant_hold_zero_error',np.all(changed[1:c['duration']]==0))
                actual=energy.copy();actual[start:stop]=changed
                stream=independent_scores(actual,mean,cfg)
                width=min(c['duration'],45)
                for k,s in enumerate(cfg['scores']):
                    row=records[(name,c['id'],s)];alarm=stream[:,k]>thresholds[k]
                    hit=np.flatnonzero(alarm[start:end]);rise=np.flatnonzero(np.diff(np.r_[False,alarm].astype(int))==1)
                    fresh=rise[(rise>=start)&(rise<end)]-start
                    tp=int(alarm[start:end].sum());fp=int(alarm[8192:16384].sum())-tp;fn=c['duration']-tp
                    check(tag+':counts:'+s,(row['tp'],row['fp'],row['fn'])==(tp,fp,fn))
                    check(tag+':event:'+s,row['overlap_hit']==bool(len(hit)) and row['fresh_hit']==bool(len(fresh))
                        and row['overlap_delay']==(int(hit[0]) if len(hit) else None)
                        and row['fresh_delay']==(int(fresh[0]) if len(fresh) else None))
                    check(tag+':metrics:'+s,np.isclose(row['f1'],2*tp/(2*tp+fp+fn)) and np.isclose(row['recall'],tp/c['duration'])
                        and np.isclose(row['precision'],tp/(tp+fp) if tp+fp else 0))
                    post=alarm[end:end+512];clear=np.flatnonzero(~post)
                    check(tag+':post:'+s,row['post_alarm_points']==int(post.sum()) and row['first_clear_delay']==(int(clear[0]) if len(clear) else None)
                        and row['first_clear_censored']==(not bool(len(clear)))
                        and row['pre_event_alarm_points']==int(alarm[8192:start].sum())
                        and row['active_before_event']==bool(alarm[start-1]))
                    check(tag+':diagnostic:'+s,np.isclose(row['early_mse'],changed[:width].mean()) and np.isclose(row['late_mse'],changed[c['duration']-width:c['duration']].mean())
                        and np.isclose(row['oracle_late_mse'],oracle[c['duration']-width:c['duration']].mean()))
        del forward
    summary=json.loads((run/'summary.json').read_text());supervisor=json.loads((run/'supervisor.json').read_text())
    check('completed',summary['status']==supervisor['status']=='completed')
    check('wall_cap',supervisor['wall_seconds']<cfg['limits']['wall_seconds'])
    check('cpu_cap',summary['usage']['process_cpu_seconds']<cfg['limits']['cpu_seconds'])
    check('rss_cap',supervisor['sampled_peak_rss_bytes']<cfg['limits']['rss_bytes'])
    check('output_cap',sum(p.stat().st_size for p in run.iterdir() if p.is_file())<cfg['limits']['output_bytes'])
    check_freeze();check('all_frozen_inputs_unchanged',True)
    passed=sum(x['passed'] for x in checks)
    result={'status':'passed' if passed==len(checks) else 'failed','passed':passed,'total':len(checks),'checks':checks,
        'utc':datetime.now(timezone.utc).isoformat(),'command':sys.argv,'usage':worker_usage(),
        'freeze_sha256':sha(HERE/'FREEZE.json'),'run_sha256':{p.name:sha(p) for p in run.iterdir() if p.is_file()},
        'scope':'Separate score/metric arithmetic, full inference support checks and all frozen identities; no training or raw parse'}
    BudgetWriter(output,limit_bytes=LIMITS.output_bytes,reserve_bytes=LIMITS.parent_reserve_bytes).write_json('verification.json',result)
    print(json.dumps({k:result[k] for k in ['status','passed','total']},indent=2))
    if passed!=len(checks):
        print([x for x in checks if not x['passed']][:20]);raise SystemExit(1)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--attempt',required=True);p.add_argument('--worker',action='store_true');args=p.parse_args()
    if any(not re.fullmatch(r'[A-Za-z0-9_]+',x) for x in [args.run,args.attempt]):raise ValueError('Invalid identifier')
    run=LOCAL/'runs'/args.run;output=LOCAL/'verification'/args.attempt
    if args.worker:verify(run,output)
    else:
        output.mkdir(parents=True,exist_ok=False)
        cmd=[sys.executable,str(HERE/'verify.py'),'--run',args.run,'--attempt',args.attempt,'--worker']
        result=supervise(cmd,cwd=PROJECT,output_dir=output,limits=LIMITS,
            env={'TF_NUM_INTRAOP_THREADS':'1','TF_NUM_INTEROP_THREADS':'1','TF_CPP_MIN_LOG_LEVEL':'2',
                 'CUDA_VISIBLE_DEVICES':'-1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
        BudgetWriter(output,limit_bytes=LIMITS.output_bytes).write_json('supervisor.json',result)
        print(json.dumps(result,indent=2));raise SystemExit(0 if result['status']=='completed' else 1)
