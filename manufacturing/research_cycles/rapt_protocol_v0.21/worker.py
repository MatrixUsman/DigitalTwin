from pathlib import Path
import sys,io,json,time,subprocess,platform,traceback
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parents[1]
sys.path[:0]=[str(P/'src'),str(P/'baselines/vendor/rapt_v020')]
from mfg_twin.supervisor import Limits,BudgetWriter,install_worker_limits,worker_usage

def main(out):
    limits=Limits(wall_seconds=120,cpu_seconds=90,rss_bytes=1073741824,output_bytes=26214400)
    enforcement=install_worker_limits(limits);w=BudgetWriter(out,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
    import numpy as np,torch
    torch.set_num_threads(1);torch.set_num_interop_threads(1)
    from protocol21 import check,load_role,calibrate_eligible,curve_summary,sha,START
    from rapt import RaptConfig,train_rapt,RaptModel,score_sequence
    from rapt.detector import risk_trajectory
    f=check();c=f['configuration'];cfg=RaptConfig(**c['rapt']);access=[]
    manifest=json.loads((H/'INPUT_MANIFEST.json').read_text())
    w.write_json('provenance.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,cwd=str(P),
        interpreter=sys.executable,python=sys.version,platform=platform.platform(),operator='Codex',requested_author='Muhammad Usman',
        dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),
        git_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip(),
        git_status=subprocess.check_output(['git','status','--short'],cwd=P,text=True),
        freeze_sha256=sha(H/'FREEZE.json'),configuration=c,enforcement=enforcement,synthetic=True,raw_robot_access=False,attack_access=False))
    tr=load_role(manifest,'Q1','fit',access,trim=True);dev=load_role(manifest,'Q1','development',access,trim=True)
    tick=time.perf_counter();model,stats,history=train_rapt(cfg,tr,dev,device='cpu');training_seconds=time.perf_counter()-tick
    summary=curve_summary(history);b=io.BytesIO();torch.save(model.state_dict(),b);w.write_bytes('model.pt',b.getvalue())
    w.write_json('config.json',cfg.__dict__);w.write_json('obs_stats.json',stats.to_dict());w.write_json('history.json',history);w.write_json('selection.json',summary)
    selected={name:sha(out/name) for name in ['model.pt','config.json','obs_stats.json','history.json','selection.json']}
    w.write_json('SELECTION_SEALED.json',dict(utc=datetime.now(timezone.utc).isoformat(),bindings=selected,calibration_opened=False))
    # Calibration opens only after the actual fitted checkpoint and normal selection are sealed.
    caldata=load_role(manifest,'Q1','calibration',access,trim=False)
    calloss=[score_sequence(model,stats,y,u) for y,u in zip(caldata.obs,caldata.actions)]
    cal=calibrate_eligible(calloss,caldata.obs,cfg);w.write_json('calibration.json',cal.to_dict())
    w.write_json('calibration_population.json',dict(episodes=9,start=START,stop=1200,eligible=9900,configuration_selection=False,formula='released gates on eligible normal rows'))
    devfull=load_role(manifest,'Q1','development',access,trim=False)
    arrays={};rows=[];checks=0
    restored=RaptModel(cfg);restored.load_state_dict(torch.load(out/'model.pt',map_location='cpu',weights_only=True));restored.eval()
    for i,(y,u) in enumerate(zip(devfull.obs,devfull.actions)):
        loss=score_sequence(model,stats,y,u);replay=score_sequence(restored,stats,y,u)
        if not np.array_equal(loss,replay):raise ValueError('Checkpoint replay differs')
        checks+=1
        for mode in [False,True]:
            risk=risk_trajectory(loss,y,cal,use_range=mode)
            if not np.isfinite(risk).all():raise ValueError('Nonfinite score')
            key='hybrid' if mode else 'model';arrays[f'{key}_{i:02d}']=risk.astype(np.float32)
            rows.append(dict(episode=devfull.names[i],method=key,eligible=1100,point_alarms=int((risk[START:]>1).sum()),max_risk=float(risk[START:].max())))
        arrays[f'loss_{i:02d}']=loss.astype(np.float32)
    b=io.BytesIO();np.savez_compressed(b,**arrays);w.write_bytes('normal_development_scores.npz',b.getvalue())
    for name,digest in selected.items():
        if sha(out/name)!=digest:raise ValueError('Calibration changed selected artifact')
        checks+=1
    check();checks+=len(f['bindings'])
    w.write_json('access.json',access);w.write_json('result.json',dict(status='completed',plant='Q1',seed=17,variant='raw',
        training_seconds=training_seconds,training_rows=9900,training_targets=9450,development_selection_targets=9450,
        calibration_rows=9900,normal_score_rows=9900,rows=rows,learning=summary,checks=checks,
        usage=worker_usage(),attack_evaluation=False,full_paper_reproduction=False,novelty_established=False))

if __name__=='__main__':
    out=Path(sys.argv[1])
    try:main(out)
    except BaseException:
        error=traceback.format_exc();print(error,flush=True)
        try:BudgetWriter(out,limit_bytes=26214400).write_json('failure.json',dict(traceback=error,usage=worker_usage()))
        except Exception:pass
        raise
