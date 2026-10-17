"""Bounded synthetic fitting, calibration, sealed replay and joint evaluation."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback
import numpy as np
from common import HERE,PROJECT,sha,packed,arrays,check_freeze,roster
from plant import simulate
from observer import predictions,fit_linear,errors,scores,decisions,outcome
from mfg_twin.supervisor import BudgetWriter,Limits,install_worker_limits,worker_usage

def main(out):
    started=time.monotonic();f=check_freeze();cfg=f['configuration'];limits=Limits(**cfg['limits'])
    enforcement=install_worker_limits(limits)
    writer=BudgetWriter(out,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
    writer.write_json('provenance.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,cwd=str(Path.cwd()),
        python=sys.version,platform=platform.platform(),processor=platform.processor(),owner='Haiqa Mushtaq',operator='Codex',
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip(),
        git_status=subprocess.check_output(['git','status','--short'],cwd=PROJECT,text=True),
        dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),
        configuration=cfg,freeze_sha256=sha(HERE/'FREEZE.json'),synthetic=True,raw_data_access=False,
        prior_model_use=False,enforcement=enforcement))
    items={role:roster(cfg,role) for role in ['train','calibration','evaluation']};writer.write_json('roster.json',items)
    plants={p['id']:p for p in cfg['plants']};costs={};train=[]
    def generate(item):
        ep=simulate(cfg,plants[item['plant']],item['condition'],item['seed'],item['role'])
        following,reference=predictions(ep['measurements'],ep['available'],cfg)
        ep.update(following=following,reference=reference);return ep
    tick=time.monotonic()
    for item in items['train']:
        ep=generate(item)
        if ep['attack'].any():raise ValueError('Attack in training')
        train.append(ep);writer.write_bytes(item['id']+'.npz',packed(**ep))
    values=np.concatenate([e['measurements'][cfg['warmup']:] for e in train])
    fit=dict(mean=values.mean(axis=0),scale=values.std(axis=0))
    if not np.isfinite(values).all() or np.any(fit['scale']<=1e-12):raise ValueError('Invalid training scale')
    fit['ar']=fit_linear(train,fit['mean'],fit['scale'],cfg,False)
    fit['arx']=fit_linear(train,fit['mean'],fit['scale'],cfg,True)
    energy=np.concatenate([errors(e,e['following'],e['reference'],fit,cfg)[cfg['warmup']:] for e in train])
    fit['error_means']=energy.mean(axis=0)
    if not np.isfinite(fit['error_means']).all() or np.any(fit['error_means']<=0):raise ValueError('Invalid training errors')
    writer.write_bytes('fit.npz',packed(**fit));fit_hash=sha(out/'fit.npz');del train,values,energy
    costs['training_seconds']=time.monotonic()-tick
    print(json.dumps(dict(stage='normal_training',episodes=18,seconds=costs['training_seconds'])),flush=True)
    tick=time.monotonic();calibration=[]
    for item in items['calibration']:
        ep=generate(item)
        if ep['attack'].any():raise ValueError('Attack in calibration')
        en=errors(ep,ep['following'],ep['reference'],fit,cfg);s=scores(en,fit,cfg)
        calibration.append(s[cfg['warmup']:]);writer.write_bytes(item['id']+'.npz',packed(**ep,energy=en,scores=s))
    values=np.concatenate(calibration);rank=int(np.ceil(cfg['quantile']*len(values)))
    thresholds=np.sort(values,axis=0)[rank-1]
    if len(values)!=16200 or rank!=16038 or not np.isfinite(thresholds).all():raise ValueError('Calibration identity')
    writer.write_json('calibration.json',dict(population=len(values),rank=rank,thresholds=thresholds.tolist(),
        score_names=cfg['score_names'],strict_exceedance=True,fit_sha256=fit_hash,utc=datetime.now(timezone.utc).isoformat()))
    threshold_hash=sha(out/'calibration.json');del values,calibration
    costs['calibration_seconds']=time.monotonic()-tick
    print(json.dumps(dict(stage='normal_calibration',episodes=18,rank=rank,seconds=costs['calibration_seconds'])),flush=True)
    tick=time.monotonic()
    for number,item in enumerate(items['evaluation']):
        ep=generate(item)
        # Scoring API receives only permitted observations/context, never true state or event labels.
        observable={k:ep[k] for k in ['measurements','available']}
        en=errors(observable,ep['following'],ep['reference'],fit,cfg);s=scores(en,fit,cfg)
        alarm,unknown,counter=decisions(s,en,fit,thresholds,ep['valid'],cfg)
        writer.write_bytes(item['id']+'.npz',packed(**ep,energy=en,scores=s,alarm=alarm,unknown=unknown,counter=counter))
        if (number+1)%12==0:print(json.dumps(dict(stage='evaluation_scored',episodes=number+1)),flush=True)
    costs['evaluation_scoring_seconds']=time.monotonic()-tick
    if sha(out/'fit.npz')!=fit_hash or sha(out/'calibration.json')!=threshold_hash:raise ValueError('Fitted/calibrated state changed')
    seal={p.name:sha(p) for p in sorted(out.iterdir()) if p.suffix=='.npz' or p.name in ['roster.json','calibration.json']}
    writer.write_json('SCORES_SEALED.json',dict(utc=datetime.now(timezone.utc).isoformat(),sha256=seal,outcomes_computed=False))
    records=[]
    for item in items['evaluation']:
        ep=arrays(out/(item['id']+'.npz'))
        for j,name in enumerate(cfg['decision_names']):
            records.append(dict(**item,method=name,**outcome(ep['alarm'][:,j],ep['unknown'][:,j],ep['attack'],ep['authorized'],
                ep['state'],ep['reference'],fit['scale'],cfg)))
    writer.write_json('outcomes.json',records);check_freeze()
    writer.write_json('summary.json',dict(status='completed',synthetic=True,training_episodes=18,calibration_episodes=18,
        evaluation_episodes=48,methods=11,outcomes=len(records),eligible_per_method=43200,
        candidate_is_classical_hysteresis=True,costs=costs,usage=worker_usage(),wall_seconds=time.monotonic()-started,
        scores_seal_sha256=sha(out/'SCORES_SEALED.json')))
    print('Completed all declared synthetic episodes and joint outcomes.',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    try:main(args.output)
    except BaseException:
        # Failure evidence remains alongside partial artifacts; parent preserves signals/timeouts too.
        text=traceback.format_exc();print(text,flush=True)
        try:BudgetWriter(args.output,limit_bytes=52428800).write_json('failure.json',dict(traceback=text,usage=worker_usage()))
        except Exception:pass
        raise
