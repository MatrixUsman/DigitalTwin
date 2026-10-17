"""One bounded normal-calibration and fresh-simulation campaign; seal before labels."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback
import numpy as np
from support import HERE,PROJECT,OLD_RUN,sha,packed,arrays,check_freeze,roster,scaled_plant
from plant import commands
from core import trajectory, bank_predictions, following_predictions, components, score_matrix, calibrate, decision
from metrics import evaluate, aggregate
from mfg_twin.supervisor import BudgetWriter,Limits,install_worker_limits,worker_usage
from mfg_twin.metrics import average_precision

def main(out):
    start = time.monotonic(); frozen = check_freeze(); cfg = frozen['configuration']
    limits = Limits(**cfg['limits']); enforcement = install_worker_limits(limits)
    w = BudgetWriter(out,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
    def now(): return datetime.now(timezone.utc).isoformat()
    w.write_json('provenance.json',dict(utc=now(),command=sys.argv,cwd=str(Path.cwd()),python=sys.version,
        platform=platform.platform(),owner='Haiqa Mushtaq',operator='Codex',synthetic=True,raw_access=False,
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip(),
        git_status=subprocess.check_output(['git','status','--short'],cwd=PROJECT,text=True),
        dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),
        configuration=cfg,freeze_sha256=sha(HERE/'FREEZE.json'),enforcement=enforcement))
    fit = arrays(OLD_RUN/'fit.npz'); fit_hash = sha(OLD_RUN/'fit.npz')
    oldcfg = json.loads((HERE.parent/'recovery_v0.5/config.json').read_text())
    oldcfg.update({k:cfg[k] for k in ['bank','physical_tolerance','noise_margin_sigma','mode_duration',
                                      'mode_position_jump','mode_velocity_jump','mode_quantile']})
    cache = {}; costs = {}
    def get_bank(u,c):
        key=(u.tobytes(),c['frequency'],tuple(c['amplitude']),c['phase_offset'])
        if key not in cache: cache[key] = bank_predictions(u,c)
        return cache[key]
    def normal_parts(role):
        parts=[]
        for path in sorted(OLD_RUN.glob(role+'_*.npz')):
            ep=arrays(path)
            if ep['attack'].any(): raise ValueError('Non-normal calibration/training')
            comp=components(ep['measurements'],ep['available'],ep['valid'],ep['following'],
                            get_bank(ep['available'],oldcfg),fit,oldcfg)
            parts.append((path.stem,comp))
        if len(parts)!=18: raise ValueError('Normal population mismatch')
        return parts
    tick=time.monotonic(); train=normal_parts('train')
    mode_scales=[]
    for mode in [0,1]:
        values=np.concatenate([c['base'][cfg['warmup']:,7][c['mode'][cfg['warmup']:]==mode] for _,c in train])
        if not len(values): raise ValueError('Empty training mode')
        value=float(np.sort(values)[int(np.ceil(cfg['mode_quantile']*len(values)))-1])
        if value<=0 or not np.isfinite(value): raise ValueError('Invalid mode scale')
        mode_scales.append(value)
    mode_scales=np.asarray(mode_scales)
    w.write_bytes('fit.npz',packed(**fit,mode_scales=mode_scales))
    for name,c in train: w.write_bytes(name+'.npz',packed(**c))
    costs['training_normal_replay_seconds']=time.monotonic()-tick
    tick=time.monotonic(); calibration=[]
    for name,c in normal_parts('calibration'):
        c['scores']=score_matrix(c,mode_scales); calibration.append(c)
        w.write_bytes(name+'.npz',packed(**c))
    thresholds=[calibrate(calibration,j,cfg) for j in range(len(cfg['methods']))]
    w.write_json('calibration.json',dict(utc=now(),population=16200,budget=cfg['calibration_alarm_budget'],
        methods=cfg['methods'],records=thresholds,old_fit_sha256=fit_hash,fit_sha256=sha(out/'fit.npz')))
    pre_seal={p.name:sha(p) for p in out.iterdir() if p.suffix=='.npz' or p.name=='calibration.json'}
    w.write_json('BEFORE_FRESH_GENERATION.json',dict(utc=now(),sha256=pre_seal,fresh_observations_generated=False))
    costs['normal_calibration_seconds']=time.monotonic()-tick
    print('Normal-only calibration sealed; fresh generation begins.',flush=True)
    items=roster(cfg); w.write_json('roster.json',items)
    task_map={t['id']:t for t in cfg['tasks']}; plant_map={p['id']:p for p in cfg['fresh_plants']}
    physics_cache={}; tick=time.monotonic()
    for i,item in enumerate(items):
        c=dict(cfg); c.update(task_map[item['task']]); p=plant_map[item['plant']]
        approved,available,executed,valid,attack,authorized=commands(c,item['condition'])
        key=(item['task'],item['plant'],item['condition'])
        if key not in physics_cache:
            initial=np.r_[approved[0,:2],0.,0.]
            physics_cache[key]=trajectory(initial,executed,scaled_plant(c,p['mass_factor'],p['damping_factor']),c)
        state=physics_cache[key]
        if np.max(np.abs(state[:,:2]))>np.pi or np.max(np.abs(state[:,2:]))>10: raise ValueError('State bounds')
        noise=np.random.default_rng(item['noise_seed']).normal(size=state.shape)*np.asarray(c['sensor_sigma'])
        y=state+noise; bank=get_bank(available,c); following=following_predictions(y,available,c)
        comp=components(y,available,valid,following,bank,fit,c)
        score=score_matrix(comp,mode_scales)
        pairs=[decision(score[:,j],j,valid,comp['return_ok'],thresholds[j]['threshold'],c) for j in range(len(cfg['methods']))]
        alarm=np.column_stack([a for a,u in pairs]); unknown=np.column_stack([u for a,u in pairs])
        w.write_bytes(item['id']+'.npz',packed(state=state,measurements=y,approved=approved,available=available,
            executed=executed,valid=valid,attack=attack,authorized=authorized,reference=bank[:,1],bank=bank,
            following=following,scores=score,alarm=alarm,unknown=unknown,**{k:v for k,v in comp.items() if k!='valid'}))
        if (i+1)%24==0: print(json.dumps(dict(stage='fresh_scoring',episodes=i+1)),flush=True)
    costs['fresh_generation_scoring_seconds']=time.monotonic()-tick
    for name,h in pre_seal.items():
        if sha(out/name)!=h: raise ValueError('Fitted/normal artifact changed')
    seal={p.name:sha(p) for p in out.iterdir() if p.suffix=='.npz' or p.name in ['calibration.json','roster.json']}
    w.write_json('SCORES_SEALED.json',dict(utc=now(),sha256=seal,outcomes_computed=False))
    records=[]; pooled={s:[] for s in ['within_range','extrapolation']}
    for item in items:
        ep=arrays(out/(item['id']+'.npz'))
        pooled[item['stratum']].append((ep['attack'][cfg['warmup']:],
            np.where(ep['unknown'],-1.,ep['scores'])[cfg['warmup']:]))
        for j,name in enumerate(cfg['methods']):
            records.append(dict(**item,method=name,**evaluate(ep['alarm'][:,j],ep['unknown'][:,j],ep,fit,cfg)))
    result=aggregate(records,cfg)
    for stratum,items_in in pooled.items():
        labels=np.concatenate([x[0] for x in items_in]).astype(int).tolist()
        scored=np.concatenate([x[1] for x in items_in])
        for j,name in enumerate(cfg['methods']):
            row=next(r for r in result['rows'] if r['stratum']==stratum and r['method']==name)
            row['average_precision_unknown_ranked_last']=average_precision(labels,scored[:,j].tolist())
    w.write_json('outcomes.json',records); w.write_json('aggregate.json',result); check_freeze()
    w.write_json('summary.json',dict(status='completed',utc=now(),synthetic=True,training_episodes=18,
        calibration_episodes=18,evaluation_episodes=len(items),methods=len(cfg['methods']),outcomes=len(records),
        costs=costs,usage=worker_usage(),wall_seconds=time.monotonic()-start,
        scores_sha256=sha(out/'SCORES_SEALED.json'),before_fresh_sha256=sha(out/'BEFORE_FRESH_GENERATION.json')))
    print('All fresh streams sealed and joint outcomes saved.',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True); args=parser.parse_args()
    try: main(args.output)
    except BaseException:
        trace=traceback.format_exc(); print(trace,flush=True)
        try: BudgetWriter(args.output,limit_bytes=100663296).write_json('failure.json',dict(traceback=trace,usage=worker_usage()))
        except Exception: pass
        raise
