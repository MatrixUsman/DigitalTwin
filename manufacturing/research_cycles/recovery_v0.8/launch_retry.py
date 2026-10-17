"""Infrastructure-only retry: unchanged frozen worker; preserve failed launch."""
import sys,json
from datetime import datetime,timezone
from common import HERE,PROJECT,LOCAL,check,sha
from mfg_twin.supervisor import BudgetWriter,Limits,supervise
if __name__=='__main__':
 c=check()['configuration'];lim=Limits(**c['limits']);prior=LOCAL/'runs/confirmation_001'
 failure=json.loads((prior/'supervisor.json').read_text())
 assert failure['reason'].startswith('supervision_failure:PermissionError')
 assert failure['worker_log_bytes']==0 and not (prior/'provenance.json').exists()
 out=LOCAL/'runs/confirmation_002';out.mkdir(parents=True,exist_ok=False)
 command=[sys.executable,str(HERE/'worker.py'),'--output',str(out)];w=BudgetWriter(out,limit_bytes=lim.output_bytes)
 w.write_json('launch.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=command,cwd=str(PROJECT),freeze_sha256=sha(HERE/'FREEZE.json'),
  launch_sha256=sha(__file__),prior_failure_sha256=sha(prior/'supervisor.json'),reason='Permit required /bin/ps monitoring; frozen science unchanged; no outcomes from first launch'))
 r=supervise(command,cwd=PROJECT,output_dir=out,limits=lim);w.write_json('supervisor.json',r);print(json.dumps(r,indent=2))
 raise SystemExit(0 if r['status']=='completed' else 1)
