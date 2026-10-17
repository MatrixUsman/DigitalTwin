import sys,json
from datetime import datetime,timezone
from common import HERE,PROJECT,LOCAL,check,sha
from mfg_twin.supervisor import BudgetWriter,Limits,supervise
if __name__=='__main__':
 c=check()['configuration'];lim=Limits(**c['limits']);out=LOCAL/'runs/confirmation_001';out.mkdir(parents=True,exist_ok=False)
 command=[sys.executable,str(HERE/'worker.py'),'--output',str(out)];w=BudgetWriter(out,limit_bytes=lim.output_bytes)
 w.write_json('launch.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=command,cwd=str(PROJECT),freeze_sha256=sha(HERE/'FREEZE.json')))
 r=supervise(command,cwd=PROJECT,output_dir=out,limits=lim);w.write_json('supervisor.json',r);print(json.dumps(r,indent=2))
 raise SystemExit(0 if r['status']=='completed' else 1)
