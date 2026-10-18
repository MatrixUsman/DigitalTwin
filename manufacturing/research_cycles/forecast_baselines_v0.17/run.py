from pathlib import Path
from datetime import datetime,timezone
import argparse,json,sys,time
from worker import H,P,check,sha
from mfg_twin.supervisor import Limits,BudgetWriter,supervise

ap=argparse.ArgumentParser();ap.add_argument('--phase',required=True,choices=['pilot','full']);a=ap.parse_args()
f=check();phase=f['phases'][a.phase];limits=Limits(**phase['limits'])
if a.phase=='full':
    auth=json.loads((H/'RUN_AUTHORIZATION.json').read_text())
    assert auth['approved'] and auth['freeze_sha256']==sha(H/'FREEZE.json')
root=P/f'local/forecast_baselines_v0.17/{a.phase}_001';root.mkdir(parents=True,exist_ok=False)
started=time.monotonic();outcomes=[]
for method in ['ModernTCN','iTransformer','TimeMixer']:
    if time.monotonic()-started>=3*limits.wall_seconds:raise SystemExit('Total wall budget exhausted')
    out=root/method;out.mkdir();w=BudgetWriter(out,limit_bytes=limits.output_bytes)
    command=[sys.executable,str(H/'worker.py'),'--method',method,'--phase',a.phase,'--output',str(out)]
    w.write_json('launch.json',{'utc':datetime.now(timezone.utc).isoformat(),'command':command,'cwd':str(P),'freeze_sha256':sha(H/'FREEZE.json')})
    result=supervise(command,cwd=P,output_dir=out,limits=limits,env={'PYTHONDONTWRITEBYTECODE':'1'})
    w.write_json('supervisor.json',result);outcomes.append({'method':method,**result});print(method+' '+json.dumps(result),flush=True)
(root/'CAMPAIGN.json').write_text(json.dumps({'phase':a.phase,'outcomes':outcomes,'wall_seconds':time.monotonic()-started},indent=2)+'\n')
raise SystemExit(0 if all(r['status']=='completed' for r in outcomes) else 1)
