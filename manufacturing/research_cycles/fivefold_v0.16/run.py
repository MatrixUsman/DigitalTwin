"""One bounded run using the prewritten freeze, retaining every fold failure."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,platform,subprocess,sys,time,traceback

HERE=Path(__file__).resolve().parent;P=HERE.parents[1]
sys.path.insert(0,str(P/'src'))
from mfg_twin.supervisor import Limits,BudgetWriter,supervise,install_worker_limits,worker_usage
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
RUN=P/'local/fivefold_v0.16/runs/validation_001'

def frozen():
    f=json.loads((HERE/'FREEZE.json').read_text())
    for group in ['sources','inputs']:
        for name,digest in f[group].items():
            if sha(P/name)!=digest:raise ValueError('Changed identity: '+name)
    return f

def packed(**arrays):
    import numpy as np
    s=io.BytesIO();np.savez_compressed(s,**arrays);return s.getvalue()

def worker():
    f=frozen();lim=Limits(**f['limits']);enforcement=install_worker_limits(lim)
    import numpy as np
    from core import arx,bounds,cut,fit_pair,score_pair,metrics
    w=BudgetWriter(RUN,limit_bytes=lim.output_bytes,reserve_bytes=lim.parent_reserve_bytes)
    w.write_json('provenance.json',{'utc':datetime.now(timezone.utc).isoformat(),'project':'manufacturing','owner':'Haiqa Mushtaq','operator':'Codex',
      'requested_author':'Muhammad Usman','synthetic':True,'raw_dataset_access':False,'command':sys.argv,'cwd':str(Path.cwd()),
      'python':sys.version,'platform':platform.platform(),'dependencies':subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),
      'hardware':f['hardware'],'git_revision':f['git_revision'],'git_status':f['git_status'],'freeze_sha256':sha(HERE/'FREEZE.json'),
      'configuration':f['configuration'],'enforcement':enforcement,'seeds':'deterministic refits; original simulator seeds recorded in input lineage'})
    episodes={};access=[]
    for plant in ['Q1','Q2','Q3']:
        episodes[plant]=[]
        for j in range(3):
            name=f'local/recovery_v0.8/runs/confirmation_002/train_{plant}_{j}.npz'
            assert name in f['inputs']
            with np.load(P/name,allow_pickle=False) as z:e=arx.Observation(z['measurements'],z['available'],z['valid'])
            assert len(e.measurements)==1200
            episodes[plant].append(e);access.append({'path':name,'members':['measurements','available','valid']})
    w.write_json('access.json',access);records=[]
    for fold in range(1,6):
        b=bounds(fold)
        for plant in ['Q1','Q2','Q3']:
            ident=f'{plant}_fold{fold}';row={'plant':plant,'fold':fold,'bounds':b,'expected_targets':300}
            tick=time.process_time()
            try:
                base,head=fit_pair([cut(e,b['train']) for e in episodes[plant]],plant)
                w.write_bytes(ident+'_base.npz',packed(**base));w.write_bytes(ident+'_rbf.npz',packed(**head))
                before=[{k:np.array(v,copy=True) for k,v in model.items()} for model in [base,head]]
                native=[];std=[]
                for e in episodes[plant]:
                    n,s=score_pair(cut(e,b['validation']),base,head);native.append(n);std.append(s)
                n=np.concatenate(native);s=np.concatenate(std)
                for model,prior in zip([base,head],before):
                    for key in model:np.testing.assert_array_equal(model[key],prior[key])
                w.write_bytes(ident+'_scores.npz',packed(native_error=n,standardized_error=s,
                    source_episode=np.repeat(np.arange(3),100),source_row=np.tile(np.arange(*b['scored']),3)))
                row.update(status='completed',**metrics(n,s),radius=float(base['radius']))
            except Exception as exc:
                row.update(status='failed',targets=0,error=repr(exc),traceback=traceback.format_exc())
            row['cpu_seconds']=time.process_time()-tick;records.append(row);w.write_json(ident+'_outcome.json',row)
            print(ident+' '+row['status'],flush=True)
    frozen();w.write_json('summary.json',{'outcomes':records,'planned_plant_folds':15,'completed':sum(r['status']=='completed' for r in records),
      'failed':sum(r['status']=='failed' for r in records),'expected_targets_per_method':4500,'scored_targets_per_method':sum(r['targets'] for r in records),
      'usage':worker_usage(),'attack_metrics':None,'threshold':None,'new_model_selection':False})
    w.write_json('OUTPUT_SEAL.json',{'utc':datetime.now(timezone.utc).isoformat(),'sha256':{p.name:sha(p) for p in RUN.iterdir() if p.suffix in ['.npz','.json']}})

if __name__=='__main__':
    if '--worker' in sys.argv:
        try:worker()
        except BaseException:
            msg=traceback.format_exc();print(msg,flush=True)
            BudgetWriter(RUN,limit_bytes=52428800).write_json('failure.json',{'traceback':msg,'usage':worker_usage()})
            raise
    else:
        f=frozen();lim=Limits(**f['limits']);RUN.mkdir(parents=True,exist_ok=False)
        w=BudgetWriter(RUN,limit_bytes=lim.output_bytes)
        command=[sys.executable,str(HERE/'run.py'),'--worker']
        w.write_json('launch.json',{'utc':datetime.now(timezone.utc).isoformat(),'command':command,'cwd':str(P),'freeze_sha256':sha(HERE/'FREEZE.json')})
        result=supervise(command,cwd=P,output_dir=RUN,limits=lim,env={'PYTHONDONTWRITEBYTECODE':'1'})
        w.write_json('supervisor.json',result);print(json.dumps(result,indent=2))
        raise SystemExit(0 if result['status']=='completed' else 1)
