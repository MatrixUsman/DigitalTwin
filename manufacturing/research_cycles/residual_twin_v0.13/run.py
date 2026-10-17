"""One bounded local normal-only candidate pilot; never overwrite or retry."""
import json,sys
from datetime import datetime,timezone
from io13 import HERE,PROJECT,RUN,check,sha
from mfg_twin.supervisor import Limits,BudgetWriter,supervise

f=check();lim=Limits(**f['configuration']['limits'])
RUN.mkdir(parents=True,exist_ok=False)
w=BudgetWriter(RUN,limit_bytes=lim.output_bytes)
command=[sys.executable,str(HERE/'worker.py'),'--output',str(RUN)]
w.write_json('launch.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=command,cwd=str(PROJECT),
  freeze_sha256=sha(HERE/'FREEZE.json'),scope='synthetic normal-only candidate pilot, no attacks'))
r=supervise(command,cwd=PROJECT,output_dir=RUN,limits=lim,
  env=dict(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',
           NUMEXPR_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1'))
w.write_json('supervisor.json',r);print(json.dumps(r,indent=2))
raise SystemExit(0 if r['status']=='completed' else 1)
