import sys,json
from datetime import datetime,timezone
from io19 import *
f=check(HERE/'FINAL_FREEZE.json');out=LOCAL/'final_001';out.mkdir(parents=True,exist_ok=False)
limits=Limits(**f['configuration']['limits']['final']);w=BudgetWriter(out,limit_bytes=limits.output_bytes)
command=[sys.executable,str(HERE/f['worker']),str(out)]
w.write_json('launch.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=command,cwd=str(PROJECT),freeze_sha256=sha(HERE/'FINAL_FREEZE.json')))
r=supervise(command,cwd=PROJECT,output_dir=out,limits=limits,
    env={k:'1' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONDONTWRITEBYTECODE']})
w.write_json('supervisor.json',r);print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='completed' else 1)
