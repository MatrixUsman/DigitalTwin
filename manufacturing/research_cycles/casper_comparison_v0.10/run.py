from pathlib import Path
from datetime import datetime,timezone
import json,sys
HERE=Path(__file__).resolve().parent;P=HERE.parents[1];sys.path.insert(0,str(P/'src'))
from io_utils import sha256,verify_frozen
from mfg_twin.supervisor import BudgetWriter,Limits,supervise
f=json.loads((HERE/'FREEZE.json').read_text());verify_frozen(P,f);lim=Limits(**f['configuration']['limits'])
out=P/'local/casper_comparison_v0.10/runs/pilot_001';out.mkdir(parents=True,exist_ok=False)
cmd=[sys.executable,str(HERE/'worker.py'),'--output',str(out)];w=BudgetWriter(out,limit_bytes=lim.output_bytes)
w.write_json('launch.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=cmd,cwd=str(P),freeze_sha256=sha256(HERE/'FREEZE.json')))
env=dict(TF_NUM_INTRAOP_THREADS='1',TF_NUM_INTEROP_THREADS='1',TF_CPP_MIN_LOG_LEVEL='2',CUDA_VISIBLE_DEVICES='-1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
r=supervise(cmd,cwd=P,output_dir=out,limits=lim,env=env);w.write_json('supervisor.json',r);print(json.dumps(r,indent=2))
raise SystemExit(0 if r['status']=='completed' else 1)
