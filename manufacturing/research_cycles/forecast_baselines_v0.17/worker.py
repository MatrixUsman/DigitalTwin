from pathlib import Path
from datetime import datetime,timezone
import argparse,gc,hashlib,io,json,platform,subprocess,sys,time,traceback
H=Path(__file__).resolve().parent;P=H.parents[1];sys.path.insert(0,str(P/'src'))
from mfg_twin.supervisor import Limits,BudgetWriter,install_worker_limits,worker_usage
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()

def check():
    f=json.loads((H/'FREEZE.json').read_text())
    for group in ['sources','inputs']:
        for name,digest in f[group].items():
            if sha(P/name)!=digest:raise ValueError('Changed identity: '+name)
    return f

def main(a):
    f=check();phase=f['phases'][a.phase];limits=Limits(**phase['limits']);install_worker_limits(limits)
    import numpy as np,torch
    from adapter import create,configuration,batches,predict,forecast
    w=BudgetWriter(a.output,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
    with np.load(P/f['prepared'],allow_pickle=False) as z:d={k:z[k] for k in z.files}
    train,dev=d['training'],d['development'];ti,di=d['training_indices'],d['development_indices']
    assert (len(ti),len(di))==(8192,2048)
    w.write_json('provenance.json',{'utc':datetime.now(timezone.utc).isoformat(),'project':'manufacturing','owner':'Haiqa Mushtaq','operator':'Codex',
       'method':a.method,'phase':a.phase,'command':sys.argv,'cwd':str(Path.cwd()),'python':sys.version,'platform':platform.platform(),
       'git_revision':f['git_revision'],'git_status':f['git_status'],'upstream':f['upstream'][a.method],
       'configuration':configuration(a.method),'procedure':phase,'learning_rate':f['learning_rates'][a.method],
       'freeze_sha256':sha(H/'FREEZE.json'),'prepared_sha256':sha(P/f['prepared']),
       'dependencies':subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),'device':'CPU, one torch thread',
       'classification':'author model code under modified normal-only forecasting protocol; no attack result'})
    w.write_json('access.json',{'file':f['prepared'],'members':list(d),'raw_access':False,'final_access':False,'training_targets':8192,'development_targets':2048})
    records=[]
    for seed in phase['seeds']:
        started=time.monotonic();cpu_start=time.process_time();model=create(a.method,seed)
        optimizer=torch.optim.Adam(model.parameters(),lr=f['learning_rates'][a.method]);best=float('inf');best_state=None;best_epoch=None
        last=None;stale=0;history=[];reason='maximum_epochs'
        for epoch in range(1,phase['maximum_epochs']+1):
            if last is not None and time.process_time()-cpu_start+1.25*last+2>phase['per_seed_cpu_seconds']:
                reason='declared_cpu_admission';break
            tick=time.process_time();model.train();loss_sum=0.;seen=0
            for x,y,_ in batches(train,ti):
                optimizer.zero_grad();out=forecast(a.method,model,x);loss=(out-y).square().mean()
                if not torch.isfinite(loss):raise ValueError('Nonfinite training loss')
                loss.backward()
                if not all(torch.isfinite(v.grad).all() for v in model.parameters() if v.grad is not None):raise ValueError('Nonfinite gradient')
                optimizer.step();loss_sum+=float(loss.detach())*len(x);seen+=len(x)
            before={k:v.detach().clone() for k,v in model.state_dict().items()}
            dv=predict(a.method,model,dev,di)
            for k,v in model.state_dict().items():torch.testing.assert_close(v,before[k],rtol=0,atol=0)
            mse=float(np.mean((dv.astype(float)-dev[di])**2))
            if not np.isfinite(mse):raise ValueError('Nonfinite development MSE')
            accepted=mse<best-1e-6
            if accepted:best=mse;best_epoch=epoch;best_state=before;stale=0
            else:stale+=1
            last=time.process_time()-tick
            item={'epoch':epoch,'training_mse_during_updates':loss_sum/seen,'development_mse':mse,'selected':accepted,'cpu_seconds':last}
            history.append(item);w.append_text(f'seed{seed}_epochs.jsonl',json.dumps(item)+'\n')
            print(a.method+f' seed {seed} epoch {epoch}: MSE={mse:.8g}; CPU={last:.3f}s',flush=True)
            if stale>=5:reason='normal_development_patience';break
        if best_state is None:raise ValueError('No completed epoch')
        model.load_state_dict(best_state);prediction=predict(a.method,model,dev,di).astype(float)
        np.testing.assert_allclose(np.mean((prediction-dev[di])**2),best,rtol=0,atol=1e-12)
        buffer=io.BytesIO();torch.save(best_state,buffer);w.write_bytes(f'seed{seed}_weights.pt',buffer.getvalue())
        error=prediction-dev[di];scores=np.mean(error**2,axis=1);native=error*d['scale']
        buffer=io.BytesIO();np.savez_compressed(buffer,predictions=prediction,target=dev[di],scores=scores,
            native_scores=np.mean(native**2,axis=1),raw_indices=d['development_raw_indices']);w.write_bytes(f'seed{seed}_scores.npz',buffer.getvalue())
        record={'seed':seed,'method':a.method,'parameters':sum(v.numel() for v in model.parameters()),'epochs':len(history),'selected_epoch':best_epoch,
          'stopping_reason':reason,'standardized_mse':best,'standardized_mae':float(np.mean(np.abs(error))),
          'native_channel_rmse':np.sqrt(np.mean(native**2,axis=0)).tolist(),'targets':len(di),
          'wall_seconds':time.monotonic()-started,'cpu_seconds':time.process_time()-cpu_start,'history':history,
          'weights_sha256':sha(a.output/f'seed{seed}_weights.pt'),'scores_sha256':sha(a.output/f'seed{seed}_scores.npz')}
        records.append(record);w.write_json(f'seed{seed}_record.json',record)
        del model,optimizer,best_state,before;gc.collect()
    check();w.write_json('summary.json',{'status':'completed','method':a.method,'phase':a.phase,'records':records,
         'usage':worker_usage(),'attack_metrics':None,'threshold':None,'final_access':False})
    w.write_json('OUTPUT_SEAL.json',{'utc':datetime.now(timezone.utc).isoformat(),'sha256':{p.name:sha(p) for p in a.output.iterdir() if p.suffix in ['.json','.jsonl','.npz','.pt']}})

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--method',required=True,choices=['ModernTCN','iTransformer','TimeMixer']);ap.add_argument('--phase',required=True,choices=['pilot','full']);ap.add_argument('--output',required=True,type=Path);a=ap.parse_args()
    try:main(a)
    except BaseException:
        message=traceback.format_exc();print(message,flush=True)
        BudgetWriter(a.output,limit_bytes=52428800).write_json('failure.json',{'traceback':message,'usage':worker_usage()});raise
