"""Resume only a pre-worker ps-permission failure; science freeze remains intact."""
import sys,json
from datetime import datetime,timezone
from io21 import *
if __name__=='__main__':
    freeze_check();previous=LOCAL/'normal_001';receipt=json.loads((previous/'supervisor.json').read_text())
    assert receipt['reason'].startswith('supervision_failure:PermissionError')
    assert receipt['rss_samples']==0 and receipt['worker_log_bytes']==0
    assert not (previous/'provenance.json').exists()
    out=LOCAL/'normal_002';out.mkdir(parents=True,exist_ok=False);w=BudgetWriter(out,limit_bytes=LIMITS.output_bytes)
    command=[sys.executable,str(HERE/'worker.py'),str(out)]
    w.write_json('launch.json',{'utc':datetime.now(timezone.utc).isoformat(),'command':command,'cwd':str(PROJECT),'freeze_sha256':sha(HERE/'FREEZE.json'),'resume_adapter_sha256':sha(__file__),'prior_failure_sha256':sha(previous/'supervisor.json'),'reason':'enable resource monitoring after ps sandbox denial; unchanged scientific worker'})
    r=supervise(command,cwd=PROJECT,output_dir=out,limits=LIMITS,env={k:'1' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONDONTWRITEBYTECODE']})
    w.write_json('supervisor.json',r);print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='completed' else 1)
