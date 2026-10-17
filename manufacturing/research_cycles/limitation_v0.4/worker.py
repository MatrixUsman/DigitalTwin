"""One bounded, frozen replay. Write all scores before joining event outcomes."""
import argparse
from datetime import datetime, timezone
import json
import platform
import subprocess
import sys
import time
import numpy as np
from common import HERE, PROJECT, UPSTREAM, sha, packed, check_freeze, load_source, predictor
from mechanism import cases, perturb, score_streams, calibrate, normal_metrics, event_metrics, error_summary
from mfg_twin.supervisor import BudgetWriter, Limits, install_worker_limits, worker_usage


def main(output):
    started=time.monotonic();freeze=check_freeze();config=freeze['configuration']
    limits=Limits(**config['limits']);enforcement=install_worker_limits(limits)
    writer=BudgetWriter(output,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
    run,values,indices,raw=load_source(config)
    upstream=json.loads((UPSTREAM/'config.json').read_text());roster=cases(config)
    writer.write_json('provenance.json',{'utc':datetime.now(timezone.utc).isoformat(),
        'command':sys.argv,'cwd':str(Path.cwd()),'python':sys.version,'platform':platform.platform(),
        'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip(),
        'git_status':subprocess.check_output(['git','status','--short'],cwd=PROJECT,text=True),
        'dependencies':subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),
        'configuration':config,'freeze_sha256':sha(HERE/'FREEZE.json'),'owner':'Haiqa Mushtaq',
        'operator':'Codex','data_access':'Saved exposed normal-development array only; no raw parse',
        'synthetic':True,'training':False,'enforcement':enforcement,
        'models':config['models'],'scenario_randomness':None})
    writer.write_json('cases.json',roster)
    calibration={};costs={}
    for name in config['models']:
        model_start=time.monotonic();forward=predictor(name,upstream,run)
        with np.load(run/f'{name}_scores.npz',allow_pickle=False) as a:
            base_predictions=a['predictions'].astype(np.float64)
        # Full normal inference validates current saved model/coordinate correspondence.
        replay=forward(values,indices).astype(np.float64)
        if not np.array_equal(base_predictions,replay):
            raise ValueError('Normal prediction parity failed: '+name)
        normal_energy=np.mean((base_predictions-values[indices].astype(np.float64))**2,axis=1)
        mean=float(normal_energy[:config['design_stop']].mean())
        streams=score_streams(normal_energy,mean,config)
        thresholds,rank=calibrate(streams,config['design_stop'],config['calibration_stop'],config['threshold_quantile'])
        calibration[name]={'normal_mean':mean,'thresholds':thresholds.tolist(),'rank':rank,
                           'population':4096,'strict_exceedance':True}
        writer.write_bytes(name+'_normal.npz',packed(energy=normal_energy,streams=streams,raw_indices=raw))
        arrays={};forward_seconds=0.
        for case in roster:
            start=case['onset'];end=start+case['duration'];stop=end+config['history']
            y=perturb(values,45+start,case['duration'],case['family'],case['magnitude'])
            tick=time.monotonic();pred=forward(y,indices[start:stop]).astype(np.float64)
            forward_seconds+=time.monotonic()-tick
            target=y[indices[start:stop]].astype(np.float64)
            energy=np.mean((pred-target)**2,axis=1)
            oracle=np.mean((base_predictions[start:stop]-target)**2,axis=1)
            if not np.isfinite(pred).all() or not np.isfinite(energy).all():raise ValueError('Nonfinite replay')
            arrays[case['id']+'_predictions']=pred
            arrays[case['id']+'_energy']=energy
            arrays[case['id']+'_oracle_energy']=oracle
        writer.write_bytes(name+'_overrides.npz',packed(**arrays))
        costs[name]={'wall_seconds':time.monotonic()-model_start,'changed_window_inference_seconds':forward_seconds}
        print(json.dumps({'scored':name,'cases':len(roster),'seconds':costs[name]['wall_seconds']}),flush=True)
        del forward,arrays
    writer.write_json('calibration.json',calibration)
    # Complete, immutable prediction/score and calibration inventory before labels are evaluated.
    seal={p.name:sha(p) for p in sorted(output.iterdir()) if p.suffix=='.npz' or p.name in ['cases.json','calibration.json']}
    writer.write_json('SCORES_SEALED.json',{'utc':datetime.now(timezone.utc).isoformat(),'sha256':seal,
        'outcomes_computed':False,'scope':'All six models and all 189 synthetic cases'})
    records=[];normal=[]
    for name in config['models']:
        with np.load(output/(name+'_normal.npz'),allow_pickle=False) as a:
            normal_energy=a['energy'];normal_streams=a['streams']
        thresholds=np.asarray(calibration[name]['thresholds']);mean=calibration[name]['normal_mean']
        for k,score in enumerate(config['scores']):
            normal.append(dict(model=name,score=score,threshold=float(thresholds[k]),
                **normal_metrics(normal_streams[:,k]>thresholds[k],8192,16384)))
        with np.load(output/(name+'_overrides.npz'),allow_pickle=False) as a:
            for case in roster:
                energy=normal_energy.copy();changed=a[case['id']+'_energy'];oracle=a[case['id']+'_oracle_energy']
                start=case['onset'];energy[start:start+len(changed)]=changed
                stream=score_streams(energy,mean,config)
                diagnostic=error_summary(changed,oracle,case['duration'])
                for k,score in enumerate(config['scores']):
                    records.append(dict(model=name,score=score,**case,**diagnostic,
                        **event_metrics(stream[:,k]>thresholds[k],start,case['duration'],8192,16384,512)))
    writer.write_json('normal_outcomes.json',normal);writer.write_json('case_outcomes.json',records)
    check_freeze()
    writer.write_json('summary.json',{'status':'completed','synthetic_cases':len(roster),
        'model_count':len(config['models']),'score_count':len(config['scores']),'outcome_rows':len(records),
        'raw_access':False,'final_access':False,'training':False,'usage':worker_usage(),
        'wall_seconds':time.monotonic()-started,'costs':costs,'scores_seal_sha256':sha(output/'SCORES_SEALED.json')})
    print('Completed all predictions, sealed scores and joint evaluation.',flush=True)


if __name__=='__main__':
    from pathlib import Path
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
