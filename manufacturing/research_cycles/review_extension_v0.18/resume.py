"""One environmental retry: first attempt was killed before executing the worker."""
import json,sys
from datetime import datetime,timezone
from common import HERE,PROJECT,check,sha
from mfg_twin.supervisor import Limits,BudgetWriter,supervise
f=check();first=HERE/'runs/replay_001';receipt=json.loads((first/'supervisor.json').read_text())
assert receipt['rss_samples']==0 and receipt['worker_log_bytes']==0
assert not (first/'provenance.json').exists() and not (first/'outcomes.json').exists()
assert "Operation not permitted: '/bin/ps'" in receipt['reason']
limits=Limits(**f['configuration']['limits']);run=HERE/'runs/replay_002';run.mkdir(parents=True,exist_ok=False)
w=BudgetWriter(run,limit_bytes=limits.output_bytes);command=[sys.executable,str(HERE/'worker.py'),'--output',str(run)]
w.write_json('launch.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=command,cwd=str(PROJECT),
 freeze_sha256=sha(HERE/'FREEZE.json'),repair_freeze_sha256=sha(HERE/'REPAIR_FREEZE.json')))
r=supervise(command,cwd=PROJECT,output_dir=run,limits=limits,env={'PYTHONDONTWRITEBYTECODE':'1'})
w.write_json('supervisor.json',r);print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='completed' else 1)
