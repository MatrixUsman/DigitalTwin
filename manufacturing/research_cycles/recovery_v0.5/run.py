"""One named supervised attempt; never overwrite or silently retry."""
import argparse
from datetime import datetime,timezone
import json
import re
import sys
from common import HERE,PROJECT,LOCAL,sha,check_freeze
from mfg_twin.supervisor import BudgetWriter,Limits,supervise

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--attempt',required=True);args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_]+',args.attempt):raise ValueError('Invalid attempt')
    f=check_freeze();limits=Limits(**f['configuration']['limits'])
    out=LOCAL/'runs'/args.attempt;out.mkdir(parents=True,exist_ok=False)
    writer=BudgetWriter(out,limit_bytes=limits.output_bytes)
    command=[sys.executable,str(HERE/'worker.py'),'--output',str(out)]
    writer.write_json('launch.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=command,
        cwd=str(PROJECT),freeze_sha256=sha(HERE/'FREEZE.json')))
    result=supervise(command,cwd=PROJECT,output_dir=out,limits=limits,env={'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
    writer.write_json('supervisor.json',result);print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['status']=='completed' else 1)
