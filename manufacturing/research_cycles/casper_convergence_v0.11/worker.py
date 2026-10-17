import argparse,gc,json,platform,subprocess,sys,time,traceback
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;PROJECT=HERE.parents[1]
sys.path.insert(0,str(PROJECT/'src'))
from mfg_twin.supervisor import BudgetWriter,Limits,install_worker_limits,worker_usage
from io_utils import sha256,npz_bytes,array_hash,load_prefix,verify_frozen

def main(out):
    freeze=json.loads((HERE/'FREEZE.json').read_text());verify_frozen(PROJECT,freeze);c=freeze['configuration']
    lim=Limits(**c['limits']);install_worker_limits(lim);w=BudgetWriter(out,limit_bytes=lim.output_bytes,reserve_bytes=lim.parent_reserve_bytes)
    import numpy as np
    import tensorflow as tf
    from core import batches,score_predictions,fit_ar,predict_ar,EarlyStop
    from model10 import prepare_raw,make_model,predict,pack_weights,aggregate,admit_epoch
    now=lambda:datetime.now(timezone.utc).isoformat();start=time.monotonic()
    w.write_json('provenance.json',dict(utc=now(),study_id=c['study_id'],owner='Haiqa Mushtaq',operator='Codex',command=sys.argv,cwd=str(Path.cwd()),
        python=sys.version,platform=platform.platform(),numpy=np.__version__,tensorflow=tf.__version__,configuration=c,
        freeze_sha256=sha256(HERE/'FREEZE.json'),git_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        git_status=subprocess.check_output(['git','status','--short'],text=True),dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),
        source_sha256=freeze['source_sha256'],classification='independent architectural implementation under modified normal-only protocol'))
    w.write_json('access.json',dict(utc=now(),path=c['data_path'],maximum_parsed_numeric_rows=c['development_raw_stop'],hash_entire_nominal_file=True,
                                  raw_intervals=[[c['raw_start'],c['training_raw_stop']],[c['training_raw_stop'],c['development_raw_stop']]],attack_files=[],final_access=False))
    frame=load_prefix(PROJECT/c['data_path'],c['data_sha256'],c['development_raw_stop'],c['columns']).iloc[c['raw_start']:]
    d=prepare_raw(frame[c['columns']].to_numpy(),frame['time'].to_numpy(),c['training_raw_stop']-c['raw_start'],c);del frame
    train,dev,ti,di=d['training'],d['development'],d['training_indices'],d['development_indices'];target=dev[di]
    if (len(ti),len(di))!=(8192,2048):raise ValueError('Unexpected endpoint count')
    scaler_hash=array_hash(d['mean'])+array_hash(d['scale'])
    w.write_bytes('prepared.npz',npz_bytes(**d));w.write_json('population.json',dict(training_targets=len(ti),development_targets=len(di),aggregate_targets=1294,
        train_raw_first=int(d['training_raw_indices'][0]),train_raw_last=int(d['training_raw_indices'][-1]),
        dev_raw_first=int(d['development_raw_indices'][0]),dev_raw_last=int(d['development_raw_indices'][-1]),clock_unit='unresolved',data_previously_exposed=True))
    records=[]
    def save(name,prediction,cost,extra):
        score,native,metrics=score_predictions(prediction,target,d['scale']);filename=name+'_scores.npz'
        w.write_bytes(filename,npz_bytes(predictions=prediction,scores=score,native_scores=native,rolling_standardized=aggregate(score),rolling_native=aggregate(native),
                                        raw_indices=d['development_raw_indices'],aggregate_raw_indices=d['development_raw_indices'][754:]))
        r=dict(model=name,**metrics,**cost,**extra,score_artifact=filename,score_sha256=sha256(out/filename));records.append(r);w.write_json(name+'_record.json',r)
        print(name+': dev MSE '+str(metrics['standardized_mse']),flush=True)
    for name in ['mean','persistence','ar4']:
        tick=time.process_time()
        if name=='ar4':
            coef=fit_ar(train,ti,4,.001,64);w.write_bytes('ar4_weights.npz',npz_bytes(coefficients=coef));pred=predict_ar(dev,di,coef,4,64)
        else:pred=np.zeros_like(target) if name=='mean' else dev[di-1]
        save(name,pred,dict(cpu_seconds=time.process_time()-tick),dict(seed=None))
    w.write_text('curves.csv','architecture,seed,epoch,train_mse,development_mse,accepted,cpu_seconds\n')
    for kind in c['architectures']:
        history_length=755 if kind=='casper_cnn' else 45
        for seed in c['seeds']:
            tf.keras.backend.clear_session();gc.collect();model=make_model(kind,seed);start_cpu=time.process_time();start_wall=time.monotonic()
            stop=EarlyStop(c['patience'],c['minimum_improvement']);hist=[];last=None;best=None;reason='maximum_epochs'
            for epoch in range(1,c['maximum_epochs']+1):
                if not admit_epoch(time.process_time()-start_cpu,last,c):reason='declared_cpu_admission_budget';break
                ep_cpu=time.process_time()
                for x,y in batches(train,ti,history_length,c['batch_size']):model.train_on_batch(x,y[:,None,:])
                before=array_hash(np.concatenate([v.ravel() for v in model.get_weights()]))
                tr=predict(model,train,ti,history_length,c['batch_size']);dv=predict(model,dev,di,history_length,c['batch_size'])
                after=array_hash(np.concatenate([v.ravel() for v in model.get_weights()]));assert before==after
                train_loss=score_predictions(tr,train[ti],d['scale'])[2]['standardized_mse'];dev_loss=score_predictions(dv,target,d['scale'])[2]['standardized_mse']
                accepted,finished=stop.observe(epoch,dev_loss)
                if accepted:best=[v.copy() for v in model.get_weights()]
                last=time.process_time()-ep_cpu;hist.append(dict(epoch=epoch,training_mse=train_loss,development_mse=dev_loss,accepted=accepted,cpu_seconds=last))
                w.append_text('curves.csv',f'{kind},{seed},{epoch},{train_loss:.17g},{dev_loss:.17g},{int(accepted)},{last:.9f}\n')
                print(f'{kind} seed {seed} epoch {epoch}: dev={dev_loss:.6f} CPU={last:.2f}s',flush=True)
                if finished:reason='normal_development_patience';break
            if best is None:raise ValueError('No complete selected epoch')
            model.set_weights(best);name=kind+'_seed'+str(seed);weight=name+'_weights.npz';w.write_bytes(weight,pack_weights(model))
            fit_cpu=time.process_time()-start_cpu;fit_wall=time.monotonic()-start_wall;tick=time.process_time();pred=predict(model,dev,di,history_length,64)
            save(name,pred,dict(fit_cpu_seconds=fit_cpu,fit_wall_seconds=fit_wall,score_cpu_seconds=time.process_time()-tick),dict(seed=seed,architecture=kind,
                history_length=history_length,parameters=model.count_params(),epochs=len(hist),selected_epoch=stop.best_epoch,stopping_reason=reason,
                per_fit_cpu_admission_budget_exceeded=fit_cpu>c['fit_cpu_seconds_per_model'],history=hist,weight_artifact=weight,weight_sha256=sha256(out/weight)))
            assert abs(records[-1]['standardized_mse']-stop.best_loss)<1e-12
            del model,pred,best,tr,dv;gc.collect()
    assert scaler_hash==array_hash(d['mean'])+array_hash(d['scale']);verify_frozen(PROJECT,freeze)
    w.write_json('summary.json',dict(status='completed',utc=now(),models=records,training_targets=len(ti),development_targets=len(di),
        usage=worker_usage(),wall_seconds=time.monotonic()-start,scaler_unchanged=True,attack_metrics=None,threshold=None,final_access=False))
    print('Completed all nine model/seed outcomes.',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);out=ap.parse_args().output
    try:main(out)
    except BaseException:
        message=traceback.format_exc();print(message,flush=True)
        try:BudgetWriter(out,limit_bytes=52428800).write_json('failure.json',dict(traceback=message,usage=worker_usage()))
        except Exception:pass
        raise
