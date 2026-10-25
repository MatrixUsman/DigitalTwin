from pathlib import Path
import sys,json,io,time,platform,subprocess,traceback
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parents[2]
sys.path[:0]=[str(P/'src'),str(P/'baselines/vendor/rapt_v020')]
from mfg_twin.supervisor import Limits,BudgetWriter,install_worker_limits,worker_usage

def main(out):
    limits=Limits(wall_seconds=60,cpu_seconds=45,rss_bytes=1073741824,output_bytes=26214400)
    enforcement=install_worker_limits(limits);w=BudgetWriter(out,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
    import numpy as np,torch
    torch.set_num_threads(1);torch.set_num_interop_threads(1)
    from core import check,sha,decompose,episode_summary,START
    from rapt import RaptConfig,RaptModel,NormStats
    f=check();manifest=json.loads((H/'INPUT_MANIFEST.json').read_text());catalog=manifest['episodes']
    modeldir=P/manifest['model_directory'];cfg=RaptConfig.from_json(modeldir/'config.json');model=RaptModel(cfg)
    model.load_state_dict(torch.load(modeldir/'model.pt',map_location='cpu',weights_only=True));model.eval()
    stats=NormStats.from_dict(json.loads((modeldir/'obs_stats.json').read_text()))
    tasks={r['id']:r for r in json.loads((P/'research_cycles/context_recovery_v0.19/config.json').read_text())['tasks']}
    w.write_json('provenance.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,cwd=str(P),interpreter=sys.executable,python=sys.version,
        platform=platform.platform(),operator='Codex',project='manufacturing',model_seed=17,selected_epoch=14,
        dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),
        git_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip(),
        git_status=subprocess.check_output(['git','status','--short'],cwd=P,text=True),
        freeze_sha256=sha(H/'FREEZE.json'),configuration=f['configuration'],enforcement=enforcement,
        synthetic=True,exposed_evidence=True,training=False,fresh_confirmation=False))
    access=[];timings=[];bindings={};summaries=[];checks=[];total=0
    for r in catalog:
        with np.load(P/r['score_path'],allow_pickle=False) as z:
            y=z['measurements'].astype(np.float32);u=z['commands'].astype(np.float32);valid=z['valid'].astype(bool)
        expected=6000 if r['condition'] in ['normal','authorized_changes'] else 2400
        if y.shape!=(expected,4) or u.shape!=y.shape or valid.shape!=(expected,) or not valid.all() or not np.isfinite(y).all() or not np.isfinite(u).all():raise ValueError('Feature contract mismatch')
        access.append(dict(path=r['score_path'],members=['measurements','commands','valid'],rows=expected));total+=len(y)
        tick=time.perf_counter();a=decompose(model,stats,y,u)
        for k in ['mean','logvar','squared_error','loss']:
            if a[k].shape!=y.shape or not np.isfinite(a[k]).all():raise ValueError('Invalid decomposition '+k)
        original=P/r['prior_rapt_score_path']
        with np.load(original,allow_pickle=False) as z:old=z['loss']
        if not np.array_equal(a['loss'],old):raise ValueError('Original per-channel score parity failed '+r['id'])
        access.append(dict(path=r['prior_rapt_score_path'],members=['loss'],purpose='unchanged score parity'))
        checks.append(dict(id=r['id'],per_channel_score_exact=True,scalars=int(old.size)))
        b=io.BytesIO();np.savez_compressed(b,**a);name='decomposition_'+r['id']+'.npz';w.write_bytes(name,b.getvalue());bindings[name]=sha(out/name)
        summaries.append(episode_summary(r,a,tasks));timings.append(dict(id=r['id'],seconds=time.perf_counter()-tick,rows=expected))
    if total!=129600 or len(summaries)!=36 or len({r['id'] for r in summaries})!=36:raise ValueError('Incomplete population')
    check()
    w.write_json('DECOMPOSITION_SEALED.json',dict(utc=datetime.now(timezone.utc).isoformat(),bindings=bindings,episodes=36,rows=total,
        truth_members_opened=False,thresholds_changed=False,training=False))
    w.write_json('episode_summary.json',summaries);w.write_json('access.json',access);w.write_json('timings.json',timings);w.write_json('parity.json',checks)
    w.write_json('result.json',dict(status='completed',episodes=36,rows=total,eligible_rows=total-36*START,
        original_loss_scalar_parity=sum(r['scalars'] for r in checks),inference_and_reporting_seconds=sum(r['seconds'] for r in timings),
        usage=worker_usage(),novelty_established=False,training=False,fresh_confirmation=False,
        interpretation='Arithmetic decomposition of released scores, not causal attribution or an improved detector'))

if __name__=='__main__':
    try:main(Path(sys.argv[1]))
    except BaseException:
        error=traceback.format_exc();print(error,flush=True)
        try:BudgetWriter(Path(sys.argv[1]),limit_bytes=26214400).write_json('failure.json',dict(traceback=error,usage=worker_usage()))
        except Exception:pass
        raise
