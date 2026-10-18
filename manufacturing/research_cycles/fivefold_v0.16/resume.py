"""Infrastructure-only resume: preserve ps-denied attempt, unchanged science."""
import json,sys
from datetime import datetime,timezone
import run

run.RUN=run.P/'local/fivefold_v0.16/runs/validation_002'
repair=json.loads((run.HERE/'REPAIR_FREEZE.json').read_text())
assert run.sha(run.HERE/'resume.py')==repair['resume_sha256']
assert run.sha(run.HERE/'FREEZE.json')==repair['original_freeze_sha256']
run.frozen()
if '--worker' in sys.argv:
    try:run.worker()
    except BaseException:
        message=run.traceback.format_exc();print(message,flush=True)
        run.BudgetWriter(run.RUN,limit_bytes=52428800).write_json('failure.json',{'traceback':message,'usage':run.worker_usage()})
        raise
else:
    f=run.frozen();lim=run.Limits(**f['limits']);run.RUN.mkdir(parents=True,exist_ok=False)
    w=run.BudgetWriter(run.RUN,limit_bytes=lim.output_bytes)
    cmd=[sys.executable,str(run.HERE/'resume.py'),'--worker']
    w.write_json('launch.json',{'utc':datetime.now(timezone.utc).isoformat(),'command':cmd,'cwd':str(run.P),
       'freeze_sha256':run.sha(run.HERE/'FREEZE.json'),'repair_sha256':run.sha(run.HERE/'REPAIR_FREEZE.json')})
    result=run.supervise(cmd,cwd=run.P,output_dir=run.RUN,limits=lim,env={'PYTHONDONTWRITEBYTECODE':'1'})
    w.write_json('supervisor.json',result);print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['status']=='completed' else 1)
