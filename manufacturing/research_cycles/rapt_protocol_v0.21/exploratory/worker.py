from pathlib import Path
import sys,json,io,time,platform,subprocess,traceback
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parents[2]
sys.path[:0]=[str(P/'src'),str(P/'baselines/vendor/rapt_v020'),str(P/'research_cycles/attack_audit_v0.14'),str(P/'research_cycles/context_recovery_v0.19')]
from mfg_twin.supervisor import Limits,BudgetWriter,install_worker_limits,worker_usage

def main(out):
    limits=Limits(wall_seconds=120,cpu_seconds=90,rss_bytes=1073741824,output_bytes=52428800)
    enforcement=install_worker_limits(limits);w=BudgetWriter(out,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
    import numpy as np,torch
    torch.set_num_threads(1);torch.set_num_interop_threads(1)
    from replay21 import check,sha,validate_population,decisions,quarters,summarize,METHODS,START
    from rapt import RaptConfig,RaptModel,NormStats,score_sequence
    from rapt.detector import Calibration,risk_trajectory
    f=check();manifest=json.loads((H/'INPUT_MANIFEST.json').read_text());catalog=manifest['episodes'];validate_population(catalog)
    modeldir=P/manifest['model_directory'];cfg=RaptConfig.from_json(modeldir/'config.json');model=RaptModel(cfg)
    model.load_state_dict(torch.load(modeldir/'model.pt',map_location='cpu',weights_only=True));model.eval()
    stats=NormStats.from_dict(json.loads((modeldir/'obs_stats.json').read_text()));cal=Calibration.from_dict(json.loads((modeldir/'calibration.json').read_text()))
    w.write_json('provenance.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,cwd=str(P),interpreter=sys.executable,python=sys.version,platform=platform.platform(),operator='Codex',requested_author='Muhammad Usman',
        dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),git_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip(),git_status=subprocess.check_output(['git','status','--short'],cwd=P,text=True),
        freeze_sha256=sha(H/'FREEZE.json'),enforcement=enforcement,configuration=f['configuration'],synthetic=True,exposed_evidence=True,training=False,fresh_confirmation=False))
    access=[];timings=[];scorebindings={};total=0
    # No evaluator-only member is opened until every selected recording is scored and sealed.
    for r in catalog:
        with np.load(P/r['score_path'],allow_pickle=False) as z:
            y=z['measurements'].astype(np.float32);u=z['commands'].astype(np.float32);valid=z['valid'].astype(bool)
        expected=6000 if r['condition'] in ['normal','authorized_changes'] else 2400
        if y.shape!=(expected,4) or u.shape!=y.shape or valid.shape!=(expected,) or not valid.all() or not np.isfinite(y).all() or not np.isfinite(u).all():raise ValueError('Feature contract mismatch')
        access.append(dict(path=r['score_path'],members=['measurements','commands','valid'],phase='score',rows=expected));total+=len(y)
        tick=time.perf_counter();loss=score_sequence(model,stats,y,u)
        risk=np.stack([risk_trajectory(loss,y,cal,use_range=v) for v in [False,True]],axis=1)
        alarm=np.stack([decisions(risk[:,j]) for j in range(2)],axis=1);seconds=time.perf_counter()-tick
        if loss.shape!=y.shape or not np.isfinite(loss).all() or risk.shape!=(expected,2):raise ValueError('Score alignment')
        b=io.BytesIO();np.savez_compressed(b,loss=loss,risk=risk,alarm=alarm)
        name='score_'+r['id']+'.npz';w.write_bytes(name,b.getvalue());scorebindings[name]=sha(out/name)
        timings.append(dict(id=r['id'],rows=len(y),seconds=seconds))
    if total!=129600:raise ValueError('Incomplete population')
    w.write_json('SCORES_SEALED.json',dict(utc=datetime.now(timezone.utc).isoformat(),truth_opened=False,episodes=36,mode_outputs=72,rows=total,bindings=scorebindings))
    from evaluation import evaluate,average_precision
    from mechanism19 import extra_metrics
    with np.load(P/manifest['evaluation_scale_path'],allow_pickle=False) as z:scale=z['scale']
    access.append(dict(path=manifest['evaluation_scale_path'],members=['scale'],phase='evaluation'))
    rows=[];labels=[];risks=[]
    ec=dict(warmup=100,return_tolerance=.1,dwell=10,recovery_horizon=250)
    for r in catalog:
        with np.load(P/r['truth_path'],allow_pickle=False) as z:
            state=z['state'];truth=z['counterfactual'];attack=z['attack'].astype(bool)
        access.append(dict(path=r['truth_path'],members=['state','counterfactual','attack'],phase='evaluation'))
        with np.load(out/('score_'+r['id']+'.npz'),allow_pickle=False) as z:risk=z['risk'];alarm=z['alarm']
        labels.append(attack[START:]);risks.append(risk[START:])
        for j,method in enumerate(METHODS):
            row={k:r[k] for k in ['id','plant','task','seed','condition']};row['method']=method
            row.update(evaluate(alarm[:,j],attack,state,truth,scale,ec));row.update(extra_metrics(alarm[:,j],attack,state,truth,scale))
            row['average_precision']=average_precision(attack[START:],risk[START:,j]);row['quarters']=quarters(risk[:,j],alarm[:,j],attack,state,truth,scale);rows.append(row)
    summary=summarize(rows);yy=np.concatenate(labels);ss=np.concatenate(risks)
    for r in summary:
        chosen=[i for i,e in enumerate(catalog) if r['group']=='pooled' or e[r['group']]==r['value']]
        j=METHODS.index(r['method']);r['average_precision']=average_precision(np.concatenate([labels[i] for i in chosen]),np.concatenate([risks[i][:,j] for i in chosen]))
    for name,digest in scorebindings.items():
        if sha(out/name)!=digest:raise ValueError('Evaluation mutated score')
    check()
    w.write_json('access.json',access);w.write_json('timings.json',timings);w.write_json('outcomes.json',rows);w.write_json('summary.json',summary)
    w.write_json('result.json',dict(status='completed',episodes=36,mode_outputs=72,rows=total,eligible_rows=len(yy),events_per_mode=int(sum(r['event'] for r in rows)//2),inference_seconds=sum(r['seconds'] for r in timings),usage=worker_usage(),training=False,fresh_confirmation=False,novelty_established=False))

if __name__=='__main__':
    out=Path(sys.argv[1])
    try:main(out)
    except BaseException:
        error=traceback.format_exc();print(error,flush=True)
        try:BudgetWriter(out,limit_bytes=52428800).write_json('failure.json',dict(traceback=error,usage=worker_usage()))
        except Exception:pass
        raise
