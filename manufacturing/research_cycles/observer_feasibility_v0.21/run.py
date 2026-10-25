import sys,json
from datetime import datetime,timezone
from io21 import *
if __name__=='__main__':
    f=freeze_check();out=LOCAL/'normal_001';out.mkdir(parents=True,exist_ok=False)
    w=BudgetWriter(out,limit_bytes=LIMITS.output_bytes)
    command=[sys.executable,str(HERE/'worker.py'),str(out)]
    w.write_json('launch.json',{'utc':datetime.now(timezone.utc).isoformat(),'command':command,'cwd':str(PROJECT),'freeze_sha256':sha(HERE/'FREEZE.json')})
    r=supervise(command,cwd=PROJECT,output_dir=out,limits=LIMITS,env={k:'1' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONDONTWRITEBYTECODE']})
    w.write_json('supervisor.json',r);print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='completed' else 1)
