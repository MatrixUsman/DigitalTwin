from pathlib import Path
import sys,json,io,time,platform,subprocess,traceback,hashlib
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parents[1]
sys.path.insert(0,str(P/'src'))
from mfg_twin.supervisor import Limits,BudgetWriter,install_worker_limits,worker_usage

def main(out):
    cfg=json.loads((H/'config.json').read_text());limits=Limits(**cfg['limits']);enforcement=install_worker_limits(limits)
    writer=BudgetWriter(out,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
    import numpy as np,torch
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
    from data23 import sha,load_normal
    from pilot23 import finite_pilot,admission
    freeze=json.loads((H/'FREEZE.json').read_text())
    def verify_inputs():
        for path,digest in freeze['bindings'].items():
            if sha(P/path)!=digest:raise ValueError('Frozen input changed: '+path)
    verify_inputs();manifest=json.loads((H/'INPUT_MANIFEST.json').read_text());access=[]
    writer.write_json('provenance.json',dict(utc=datetime.now(timezone.utc).isoformat(),project='manufacturing',operator='Codex',command=sys.argv,cwd=str(P),
        interpreter=sys.executable,python=sys.version,platform=platform.platform(),processor=platform.processor(),model_seed=cfg['model_seed'],configuration=cfg,
        dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),git_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip(),
        git_status=subprocess.check_output(['git','status','--short'],cwd=P,text=True),enforcement=enforcement,freeze_sha256=sha(H/'FREEZE.json'),
        upstream_execution='none; own explicit reimplementations',synthetic=True,exposed_normal_development=True,attack_data=False,final_calibration=False,fresh_confirmation=False))
    fit_rows,ys,us=load_normal(manifest,'fit',access);dev_rows,dys,dus=load_normal(manifest,'development',access)
    tick=time.perf_counter();records,linear=finite_pilot(fit_rows,dev_rows,ys,us,dys,dus,cfg,writer)
    outcome=admission(records,linear,cfg);verify_inputs()
    writer.write_json('methods.json',records);writer.write_json('admission.json',outcome);writer.write_json('access.json',access)
    bindings={p.name:sha(p) for p in out.iterdir() if p.is_file() and p.name!='worker.log'}
    writer.write_json('MODEL_AND_PREDICTION_SEAL.json',dict(utc=datetime.now(timezone.utc).isoformat(),bindings=bindings,models=33))
    writer.write_json('result.json',dict(status='completed',methods=len(records),neural_fits=9,linear_fits=len(linear),episodes_fit=len(ys),episodes_development=len(dys),
        fit_eligible_rows=9900,development_eligible_rows=9900,fit_and_evaluate_seconds=time.perf_counter()-tick,admission=outcome,usage=worker_usage(),
        novelty_established=False,attack_evaluation=False,fresh_confirmation=False))

if __name__=='__main__':
    out=Path(sys.argv[1])
    try:main(out)
    except BaseException:
        error=traceback.format_exc();print(error,flush=True)
        try:BudgetWriter(out,limit_bytes=52428800).write_json('failure.json',dict(traceback=error,usage=worker_usage()))
        except Exception:pass
        raise
