"""Fresh-process replay, independent outcome arithmetic and numerical audit."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import sys
import numpy as np
from common import HERE,PROJECT,LOCAL,sha,arrays,check_freeze
from plant import simulate
from observer import errors,scores,decisions,predictions
from mfg_twin.supervisor import BudgetWriter,Limits,install_worker_limits,worker_usage

def main(run,out):
    f=check_freeze();cfg=f['configuration'];install_worker_limits(Limits(**cfg['limits']))
    writer=BudgetWriter(out,limit_bytes=cfg['limits']['output_bytes']);checks=[]
    def check(name,ok):
        checks.append(dict(name=name,passed=bool(ok)))
        if not ok:raise AssertionError(name)
    def close(name,a,b,atol=1e-12):check(name,np.allclose(a,b,rtol=1e-10,atol=atol))
    seal=json.loads((run/'SCORES_SEALED.json').read_text())
    for name,h in seal['sha256'].items():check('sealed '+name,sha(run/name)==h)
    roster=json.loads((run/'roster.json').read_text());fit=arrays(run/'fit.npz')
    train=[arrays(run/(item['id']+'.npz')) for item in roster['train']]
    values=np.concatenate([e['measurements'][cfg['warmup']:] for e in train])
    close('training mean',values.mean(0),fit['mean'],0);close('training scale',values.std(0),fit['scale'],0)
    for with_context,key in [(False,'ar'),(True,'arx')]:
        x=[];target=[]
        for ep in train:
            z=(ep['measurements']-fit['mean'])/fit['scale']
            for t in range(cfg['warmup'],cfg['steps']):
                features=list(z[t-4:t].reshape(-1))
                if with_context:features+=list(ep['available'][t-1])
                x.append(features+[1.]);target.append(z[t])
        x=np.asarray(x);y=np.asarray(target);reg=np.eye(x.shape[1])*np.sqrt(cfg['ridge']*len(x));reg[-1,-1]=0
        independent=np.linalg.lstsq(np.vstack([x,reg]),np.vstack([y,np.zeros((len(reg),4))]),rcond=None)[0]
        close('augmented least squares '+key,independent,fit[key],1e-9)
    train_energy=np.concatenate([errors(e,e['following'],e['reference'],fit,cfg)[cfg['warmup']:] for e in train])
    close('training normalization',train_energy.mean(0),fit['error_means'])
    cal=json.loads((run/'calibration.json').read_text());normal=[]
    for item in roster['calibration']:
        ep=arrays(run/(item['id']+'.npz'));check('normal calibration '+item['id'],not ep['attack'].any())
        normal.append(ep['scores'][cfg['warmup']:])
    normal=np.concatenate(normal);thresholds=np.sort(normal,axis=0)[16037]
    check('calibration population and rank',len(normal)==16200 and cal['population']==16200 and cal['rank']==16038)
    close('threshold order statistics',thresholds,cal['thresholds'],0)
    check('calibration sealed before evaluation',cal['utc']<seal['utc'])
    records=json.loads((run/'outcomes.json').read_text());lookup={(r['id'],r['method']):r for r in records}
    check('complete outcomes',len(lookup)==len(records)==528)
    for item in roster['evaluation']:
        ident=item['id'];ep=arrays(run/(ident+'.npz'))
        check('aligned '+ident,ep['scores'].shape==(1000,8) and ep['alarm'].shape==(1000,11) and np.array_equal(ep['time'],np.arange(1000)*.02))
        check('finite '+ident,all(np.isfinite(v).all() for v in ep.values()))
        en=errors(ep,ep['following'],ep['reference'],fit,cfg);s=scores(en,fit,cfg)
        close('error replay '+ident,en,ep['energy']);close('score replay '+ident,s,ep['scores'])
        alarm,unknown,count=decisions(s,en,fit,thresholds,ep['valid'],cfg)
        check('decision replay '+ident,np.array_equal(alarm,ep['alarm']) and np.array_equal(unknown,ep['unknown']) and np.array_equal(count,ep['counter']))
        check('classical equivalence '+ident,np.array_equal(alarm[:,9],alarm[:,10]))
        # Direct event-by-event state-machine implementation, separate from both production functions.
        state=False;k=0;h=thresholds[7]
        for t in range(1000):
            if not ep['valid'][t]:k=0
            elif s[t,7]>h:state=True;k=0
            elif state and s[t,7]<=h*.5:
                k+=1
                if k==10:state=False;k=0
            elif state:k=0
            check('latch '+ident+':'+str(t),state==bool(alarm[t,10]) and k==count[t])
        for j,name in enumerate(cfg['decision_names']):
            row=lookup[(ident,name)];eligible=range(cfg['warmup'],cfg['steps']);pos=[t for t in eligible if ep['attack'][t]]
            neg=[t for t in eligible if not ep['attack'][t]];reported={t for t in eligible if alarm[t,j] and not unknown[t,j]}
            tp=len(set(pos)&reported);fp=len(set(neg)&reported);fn=len(pos)-tp
            check('counts '+ident+name,(tp,fp,fn)==(row['tp'],row['fp'],row['fn']))
            close('f1 '+ident+name,row['f1'],2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.)
            check('coverage '+ident+name,row['unknown']==sum(bool(unknown[t,j]) for t in eligible) and row['eligible']==900)
            first=next((t for t in pos if t in reported),None)
            check('event '+ident+name,row['overlap_hit']==(first is not None))
            expected=None if first is None else first-pos[0]
            check('delay '+ident+name,row['delay_steps']==expected)
            fresh=[t for t in pos if alarm[t,j] and not unknown[t,j] and not alarm[t-1,j] and not unknown[t-1,j]]
            check('fresh '+ident+name,row['fresh_hit']==bool(fresh) and row['fresh_delay_steps']==(fresh[0]-pos[0] if fresh else None))
            if pos:
                end=pos[-1]+1;post=range(end,min(end+250,1000))
                check('post '+ident+name,row['post_alarm_points']==sum(t in reported for t in post))
                clear=next((t-end for t in post if not alarm[t,j] and not unknown[t,j]),None) if first is not None else None
                check('clear '+ident+name,row['first_clear_steps']==clear)
                falls=sum(bool(alarm[t-1,j] and not alarm[t,j] and not unknown[t-1,j] and not unknown[t,j]) for t in pos[1:])
                check('false clear '+ident+name,row['clear_while_corruption']==falls)
        if item['condition']=='persistent_offset':
            other=arrays(run/(ident.replace('persistent_offset','authorized_offset')+'.npz'))
            check('identical motion different intent '+ident,np.array_equal(ep['measurements'],other['measurements']) and not np.array_equal(ep['available'],other['available']))
    # Predeclared complete replay and numerical refinement of one physical episode.
    chosen=arrays(run/'evaluation_light_17_persistent_offset.npz')
    replay=simulate(cfg,cfg['plants'][0],'persistent_offset',17,'evaluation')
    for key,value in replay.items():check('exact regeneration '+key,np.array_equal(value,chosen[key]))
    following,reference=predictions(replay['measurements'],replay['available'],cfg)
    check('exact observer regeneration',np.array_equal(following,chosen['following']) and np.array_equal(reference,chosen['reference']))
    refined=simulate({**cfg,'substeps':16},cfg['plants'][0],'persistent_offset',17,'evaluation')
    error=np.max(np.abs(refined['state']-chosen['state']),axis=0)
    check('full trajectory integration refinement',np.max(error)<1e-4)
    supervisor=json.loads((run/'supervisor.json').read_text());summary=json.loads((run/'summary.json').read_text())
    check('completed supervisor',supervisor['status']=='completed')
    check('worker cpu',summary['usage']['process_cpu_seconds']<=300)
    check('worker memory',summary['usage']['peak_rss_bytes']<=1073741824)
    check('output budget',sum(p.stat().st_size for p in run.iterdir() if p.is_file())<52428800)
    check_freeze();run_hash={p.name:sha(p) for p in sorted(run.iterdir()) if p.is_file()}
    writer.write_json('verification.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,status='passed',
        total=len(checks),passed=sum(c['passed'] for c in checks),checks=checks,run_sha256=run_hash,
        integration_max_abs_error_by_state=error.tolist(),freeze_sha256=sha(HERE/'FREEZE.json'),usage=worker_usage()))
    print(json.dumps(dict(status='passed',checks=len(checks),integration_error=error.tolist())))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--attempt',required=True);a=p.parse_args()
    out=LOCAL/'verification'/a.attempt;out.mkdir(parents=True,exist_ok=False)
    try:main(LOCAL/'runs'/a.run,out)
    except BaseException:
        import traceback
        (out/'failure.txt').write_text(traceback.format_exc());raise
