from pathlib import Path
import sys,json,time,hashlib,platform,subprocess,traceback
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parents[1]
sys.path[:0]=[str(P/'src'),str(P/'baselines/vendor/rapt_v020')]
from mfg_twin.supervisor import Limits,BudgetWriter,install_worker_limits,worker_usage

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main(out):
    lim=Limits(wall_seconds=60,cpu_seconds=50,rss_bytes=1073741824,output_bytes=5242880)
    enforcement=install_worker_limits(lim);w=BudgetWriter(out,limit_bytes=lim.output_bytes,reserve_bytes=lim.parent_reserve_bytes)
    import numpy as np,torch
    torch.set_num_threads(1);torch.set_num_interop_threads(1)
    from rapt import RaptConfig,RaptModel,SequenceData,train_rapt,NormStats,calibrate,score_sequence,RaptDetector
    from rapt.detector import score_dataset
    receipt=json.loads((H/'SOURCE_RECEIPT.json').read_text())
    for row in receipt['files']:
        assert sha(P.parent/row['path'])==row['sha256'],row['path']
    root=P/'local/residual_twin_v0.13/runs/pilot_001'
    paths=sorted(root.glob('normal_K13_Q1_*.npz'));assert len(paths)==9
    obs=[];commands=[];access=[]
    for path in paths:
        with np.load(path,allow_pickle=False) as z:
            y=z['measurements'][100:].astype(np.float32);u=z['commands'][100:].astype(np.float32)
        assert y.shape==u.shape and y.shape[1]==4 and np.isfinite(y).all() and np.isfinite(u).all()
        obs.append(y);commands.append(u);access.append({'path':str(path.relative_to(P)),'sha256':sha(path),'rows':len(y),'members':['measurements','commands'],'slice_start':100})
    cfg=RaptConfig(obs_dim=4,action_dim=4,train_dynamics=True,batch_size=32,num_epochs=1,seed=17)
    data=SequenceData(obs,commands,names=[p.stem for p in paths])
    w.write_json('provenance.json',{'utc':datetime.now(timezone.utc).isoformat(),'command':sys.argv,'cwd':str(P),'python':sys.version,'interpreter':sys.executable,'platform':platform.platform(),'git_revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip(),'git_status':subprocess.check_output(['git','status','--short'],cwd=P,text=True),'dependencies':subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),'upstream_revision':receipt['revision'],'inputs':access,'config':cfg.__dict__,'enforcement':enforcement,'synthetic':True,'attack_access':False,'checkpoint_saved':False,'worker_sha256':sha(__file__),'plan_sha256':sha(H/'PILOT_PLAN.md')})
    tick=time.perf_counter();model,stats,hist=train_rapt(cfg,data,device='cpu');elapsed=time.perf_counter()-tick
    # Independent algebraic fixture; no training measurements reused for checks.
    rng=np.random.default_rng(2026);x=rng.normal(size=(53,4)).astype(np.float32);a=rng.normal(size=(53,4)).astype(np.float32)
    tiny=RaptModel(RaptConfig(obs_dim=4,action_dim=4,train_dynamics=True,embed_dim=8,num_blocks=1)).eval()
    unit=NormStats(np.zeros(4,np.float32),np.ones(4,np.float32),-np.ones(4,np.float32),np.ones(4,np.float32))
    fixture=SequenceData([x],[a]);cc=calibrate(tiny,unit,fixture,tiny.cfg);batch=score_sequence(tiny,unit,x,a)
    det=RaptDetector(tiny,unit,cc,use_range=False);stream=np.stack([det.step(y,u).per_dim_loss for y,u in zip(x,a)])
    np.testing.assert_allclose(batch,stream,rtol=2e-5,atol=2e-6)
    assert np.all(batch[0]==0)
    np.testing.assert_allclose(cc.per_dim_thresh,batch.max(0)+2*(batch.max(0)-np.median(batch,axis=0)))
    np.testing.assert_allclose(cc.mean_thresh,batch.mean(1).max()+3*batch.mean(1).std())
    assert all(np.isfinite(v).all() for v in [batch,stream,cc.per_dim_thresh])
    w.write_json('result.json',{'status':'completed','training_rows':sum(map(len,obs)),'episodes':len(obs),'parameters':sum(p.numel() for p in model.parameters()),'epoch_wall_seconds':elapsed,'planning_100_epoch_seconds':elapsed*100,'history':hist,'synthetic_checks':5,'batch_stream_max_absolute_error':float(abs(batch-stream).max()),'usage':worker_usage(),'upstream_files_verified':len(receipt['files']),'trained_artifact_admitted':False,'note':'One-epoch timing only; no convergence or detection claim.'})

if __name__=='__main__':
    out=Path(sys.argv[1])
    try:main(out)
    except BaseException:
        traceback.print_exc()
        try:BudgetWriter(out,limit_bytes=5242880).write_json('failure.json',{'traceback':traceback.format_exc(),'usage':worker_usage()})
        except Exception:pass
        raise
