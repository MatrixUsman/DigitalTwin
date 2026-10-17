import json,sys,time,platform,subprocess,traceback,argparse
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from io14 import HERE,PROJECT,RUN,MODELS,NORMAL,OLD,load_npz,packed,check,sha,Observation
from audit_core import infer,alarm_scores,calibrate,ROLES,specification,settings
from evaluation import evaluate,aggregate,primary,average_precision
from mfg_twin.supervisor import Limits,BudgetWriter,install_worker_limits,worker_usage
from common9 import old_generate

def main(out):
    begun=time.monotonic();f=check();c=f['configuration'];dc=settings(c);limits=Limits(**c['limits']);enforce=install_worker_limits(limits)
    writer=BudgetWriter(out,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
    now=lambda:datetime.now(timezone.utc).isoformat()
    writer.write_json('provenance.json',dict(utc=now(),configuration=c,command=sys.argv,cwd=str(Path.cwd()),
      operator='Codex',requested_author='Muhammad Usman',python=sys.version,platform=platform.platform(),synthetic=True,
      raw_CASPER_access=False,training=False,enforcement=enforce,freeze_sha256=sha(HERE/'FREEZE.json'),
      dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),
      git_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip(),
      git_status=subprocess.check_output(['git','status','--short'],cwd=PROJECT,text=True)))
    prior=json.loads((MODELS/'selection.json').read_text());models={};thresholds={};ks={};access=[];calrows=[]
    def read(plant,index,stage):
        name=f'train_{plant}_{index}.npz' if stage=='training_reference_statistic' else f'cal_{plant}_{index:02d}.npz'
        path=NORMAL/name
        if str(path.relative_to(PROJECT)) not in f['inputs']:raise ValueError('Unadmitted calibration file')
        with np.load(path,allow_pickle=False) as z:e=Observation(z['measurements'],z['available'],z['valid'])
        access.append(dict(file=str(path.relative_to(PROJECT)),stage=stage,members=['measurements','available','valid']))
        return e
    for plant in ['Q1','Q2','Q3']:
        models[plant]={'base':load_npz(MODELS/f'base_{plant}.npz')}
        for role in ['linear','rbf']:models[plant][role]=load_npz(MODELS/f'fit_{plant}_{prior["models"][plant][role]}.npz')
        train=[read(plant,j,'training_reference_statistic') for j in range(3)]
        s=np.concatenate([infer(e,models[plant],0.,dc)[2][c['warmup']:,0] for e in train])
        ks[plant]=float(np.mean(s)+np.std(s));writer.write_bytes(f'training_statistic_{plant}.npz',packed(scores=s,k=np.array(ks[plant])))
        cal=[read(plant,j,'normal_calibration') for j in range(9,14)]
        arrays=[infer(e,models[plant],ks[plant],dc) for e in cal]
        ss=np.concatenate([a[2][c['warmup']:] for a in arrays]);thresholds[plant]={}
        for i,role in enumerate(ROLES):
            threshold,rank=calibrate(ss[:,i],c['quantile']);assert rank==5445 and len(ss)==5500
            if role in ['base','linear','rbf']:
                if threshold!=prior['thresholds'][plant][role]:raise ValueError('Existing calibration mismatch')
                threshold=prior['thresholds'][plant][role]
            thresholds[plant][role]=threshold
        for j,(e,(refs,res,score)) in enumerate(zip(cal,arrays)):
            alarms=alarm_scores(score,res,e.valid,thresholds[plant],dc)
            writer.write_bytes(f'calibration_{plant}_{j:02d}.npz',packed(scores=score,alarms=alarms))
            for i,method in enumerate(c['methods']):
                a=alarms[c['warmup']:,i];rising=a&~np.r_[False,a[:-1]]
                calrows.append(dict(plant=plant,episode=j,method=method,points=len(a),alarms=int(a.sum()),episodes=int(rising.sum())))
    writer.write_json('access.json',access);writer.write_json('calibration.json',dict(thresholds=thresholds,cusum_k=ks,burdens=calrows))
    writer.write_json('CALIBRATION_SEALED.json',dict(utc=now(),fresh_generated=False,sha256={p.name:sha(p) for p in out.iterdir() if p.suffix=='.npz' or p.name in ['access.json','calibration.json']}))
    sim=json.loads((PROJECT/'research_cycles/recovery_v0.8/FREEZE.json').read_text())['configuration']
    for key in ['onset','end','brief_length','offset_radians','slow_rate']:sim[key]=c[key]
    assert sim['steps']==1200 and sim['dt']==.02
    cache={};catalog=[];timings=[]
    for ti,task in enumerate(c['tasks']):
        for pi,plant in enumerate(sim['plants8']):
            p=plant['id']
            for seed in c['seeds']:
                for condition in c['conditions']:
                    rid=f'{task["id"]}_{p}_{seed}_{condition}';noise_seed=510000+ti*10000+pi*3000+seed
                    ep=old_generate(sim,task,plant,condition,noise_seed,cache)
                    # No truth fields cross the observed-input boundary.
                    obs=Observation(ep['measurements'],ep['available'],ep['valid'])
                    tick=time.perf_counter();refs,res,score=infer(obs,models[p],ks[p],dc)
                    alarms=alarm_scores(score,res,obs.valid,thresholds[p],dc)
                    timings.append(dict(id=rid,seconds=time.perf_counter()-tick))
                    writer.write_bytes('score_'+rid+'.npz',packed(measurements=obs.measurements,commands=obs.commands,valid=obs.valid,references=refs,scores=score,alarms=alarms))
                    writer.write_bytes('truth_'+rid+'.npz',packed(state=ep['state'],counterfactual=ep['truth_reference'],attack=ep['attack'],authorized=ep['authorized']))
                    catalog.append(dict(id=rid,plant=p,task=task['id'],seed=seed,noise_seed=noise_seed,condition=condition))
        print('Sealed score arrays for task '+task['id'],flush=True)
    writer.write_json('catalog.json',catalog);writer.write_json('timings.json',timings)
    writer.write_json('SCORES_SEALED.json',dict(utc=now(),outcomes_read=False,sha256={p.name:sha(p) for p in out.iterdir() if p.name.startswith(('score_','truth_')) or p.name in ['catalog.json','timings.json']}))
    # Delayed joint evaluation starts only after every method/episode is saved and sealed.
    rows=[];pooled={k:[] for k in ['pooled','Q1','Q2','Q3']}
    for item in catalog:
        z=load_npz(out/('score_'+item['id']+'.npz'));t=load_npz(out/('truth_'+item['id']+'.npz'))
        for key in ['pooled',item['plant']]:pooled[key].append((t['attack'][100:],z['scores'][100:]))
        for j,method in enumerate(c['methods']):
            row=evaluate(z['alarms'][:,j],t['attack'],t['state'],t['counterfactual'],models[item['plant']]['base']['scale'],c)
            rows.append(dict(**item,method=method,**row))
    summary=aggregate(rows,c['methods'])
    aps={}
    for key,parts in pooled.items():
        labels=np.concatenate([a for a,_ in parts]);scores=np.concatenate([b for _,b in parts])
        aps[key]={role:average_precision(labels,scores[:,i]) for i,role in enumerate(ROLES)}
    for row in summary:row['average_precision']=aps[row['stratum']][specification(row['method'])[0]]
    writer.write_json('outcomes.json',rows)
    check();writer.write_json('summary.json',dict(status='completed',utc=now(),episodes=len(catalog),outcomes=len(rows),
      rows=summary,primary=primary(summary,c),wall_seconds=time.monotonic()-begun,usage=worker_usage(),
      novelty_established=False,scope='bounded synthetic candidate audit; no paper-level reproduction'))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);out=parser.parse_args().output
    try:main(out)
    except BaseException:
        error=traceback.format_exc();print(error,flush=True)
        try:BudgetWriter(out,limit_bytes=134217728).write_json('failure.json',dict(traceback=error,usage=worker_usage()))
        except Exception:pass
        raise
