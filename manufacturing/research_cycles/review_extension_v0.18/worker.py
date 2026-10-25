import argparse,io,json,platform,subprocess,sys,time,traceback
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from common import HERE,PROJECT,OLD,MODELS,load,sha,check,evaluation
from core import replay,extra,summarize
from mfg_twin.supervisor import Limits,BudgetWriter,install_worker_limits,worker_usage
sys.path.insert(0,str(PROJECT/'research_cycles/attack_audit_v0.14'))
from audit_core import alarm_scores,settings

def main(out):
    begun=time.monotonic();f=check();c=f['configuration'];lim=Limits(**c['limits']);enforce=install_worker_limits(lim)
    w=BudgetWriter(out,limit_bytes=lim.output_bytes,reserve_bytes=lim.parent_reserve_bytes)
    original_config=json.loads((PROJECT/'research_cycles/attack_audit_v0.14/config.json').read_text())
    methods=original_config['methods']+[c['extra_method']]
    thresholds=json.loads((OLD/'calibration.json').read_text())['thresholds']
    cat=json.loads((OLD/'catalog.json').read_text())
    prior={(r['id'],r['method']):r for r in json.loads((OLD/'outcomes.json').read_text())}
    scales={p:load(MODELS/f'base_{p}.npz')['scale'] for p in ['Q1','Q2','Q3']}
    w.write_json('provenance.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,cwd=str(Path.cwd()),
      project='manufacturing',operator='Codex',requested_author='Muhammad Usman',configuration=c,
      python=sys.version,interpreter=sys.executable,platform=platform.platform(),training=False,new_simulation=False,
      observations='previously exposed saved synthetic v0.14 arrays',freeze_sha256=sha(HERE/'FREEZE.json'),enforcement=enforce,
      dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),
      git_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip(),
      git_dirty=subprocess.check_output(['git','status','--short'],cwd=PROJECT,text=True)))
    rows=[];diagnostics=[];newalarms=[];checks=0
    for item in cat:
        z=load(OLD/('score_'+item['id']+'.npz'));t=load(OLD/('truth_'+item['id']+'.npz'));scale=scales[item['plant']]
        residual=(z['measurements'][:,None,:]-z['references'])/scale
        oldalarm=alarm_scores(z['scores'],residual,z['valid'],thresholds[item['plant']],settings(original_config))
        np.testing.assert_array_equal(oldalarm,z['alarms']);checks+=1
        new,evidence=replay(z['scores'][:,0],residual[:,0],z['valid'],thresholds[item['plant']]['base'])
        rbfn,rbfe=replay(z['scores'][:,2],residual[:,2],z['valid'],thresholds[item['plant']]['rbf'])
        np.testing.assert_array_equal(rbfn,z['alarms'][:,methods.index('rbf_dual_nodwell')]);checks+=1
        alarms=np.column_stack([z['alarms'],new]);newalarms.append(new)
        for j,method in enumerate(methods):
            original=evaluation.evaluate(alarms[:,j],t['attack'],t['state'],t['counterfactual'],scale,original_config)
            if method!=c['extra_method']:
                for k,v in original.items():
                    if v!=prior[item['id'],method][k]:raise AssertionError(f'Old outcome mismatch {item["id"]}/{method}/{k}')
                    checks+=1
            rows.append(dict(**item,method=method,**original,**extra(alarms[:,j],t['attack'],t['state'],t['counterfactual'],scale,c,original)))
        if not t['attack'].any():
            for role,i,ev in [('base',0,evidence),('rbf',2,rbfe)]:
                score=z['scores'][:,i];threshold=thresholds[item['plant']][role]
                eligible=np.arange(len(score))>=c['warmup'];over=(score>threshold)&eligible
                referr=np.max(np.abs((t['state']-z['references'][:,i])/scale),axis=1)
                ref_over=(referr>threshold)&eligible
                for method in [role+'_point',role+'_dual',role+'_dual_nodwell']:
                    a=alarms[:,methods.index(method)];held=a&~over&eligible
                    diagnostics.append(dict(**item,method=method,threshold=threshold,
                      eligible=int(eligible.sum()),alarm_points=int((a&eligible).sum()),score_exceedances=int(over.sum()),
                      retained_with_clearance_evidence=int((held&ev).sum()),retained_without_clearance_evidence=int((held&~ev).sum()),
                      reference_error_exceedances=int(ref_over.sum()),noisy_and_reference_exceedances=int((over&ref_over).sum()),
                      reference_error_max=float(referr[eligible].max()),reference_error_median=float(np.median(referr[eligible])),
                      noise_only_exceedances=int((np.max(np.abs((z['measurements']-t['state'])/scale),axis=1)[eligible]>threshold).sum())))
    b=io.BytesIO();np.savez_compressed(b,alarms=np.stack(newalarms),ids=np.array([r['id'] for r in cat]),methods=np.array([c['extra_method']]))
    w.write_bytes('matched_alarms.npz',b.getvalue());w.write_json('outcomes.json',rows);w.write_json('diagnostics.json',diagnostics)
    summary=summarize(rows,methods,c)
    w.write_json('summary.json',dict(status='completed',scope='exploratory replay of exposed synthetic conditions',rows=summary,
      methods=methods,episodes=len(cat),outcomes=len(rows),parity_checks=checks,
      native_tolerance={p:(scales[p]*c['return_tolerance']).tolist() for p in scales},
      original_criterion='unchanged original v0.14 RBF dual 10% criterion failed; no new improvement criterion is tested here',
      timing_warning='conditional empirical delay distributions; 3 paired seeds are not independent robots',
      elapsed_seconds=time.monotonic()-begun,usage=worker_usage()))
    check();w.write_json('OUTPUT_SEAL.json',dict(utc=datetime.now(timezone.utc).isoformat(),sha256={p.name:sha(p) for p in out.iterdir() if p.is_file()}))
    print(json.dumps(dict(status='completed',episodes=len(cat),outcomes=len(rows),parity_checks=checks)),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);out=p.parse_args().output
    try:main(out)
    except BaseException:
        error=traceback.format_exc();print(error,flush=True)
        try:BudgetWriter(out,limit_bytes=104857600).write_json('failure.json',dict(traceback=error,usage=worker_usage()))
        except Exception:pass
        raise
