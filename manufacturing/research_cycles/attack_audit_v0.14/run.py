import sys,json
from datetime import datetime,timezone
from io14 import HERE,PROJECT,RUN,check,sha
from mfg_twin.supervisor import Limits,BudgetWriter,supervise
f=check();limits=Limits(**f['configuration']['limits']);RUN.mkdir(parents=True,exist_ok=False)
w=BudgetWriter(RUN,limit_bytes=limits.output_bytes)
command=[sys.executable,str(HERE/'worker.py'),'--output',str(RUN)]
w.write_json('launch.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=command,cwd=str(PROJECT),freeze_sha256=sha(HERE/'FREEZE.json')))
r=supervise(command,cwd=PROJECT,output_dir=RUN,limits=limits,
 env={k:'1' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONDONTWRITEBYTECODE']})
w.write_json('supervisor.json',r);print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='completed' else 1)
