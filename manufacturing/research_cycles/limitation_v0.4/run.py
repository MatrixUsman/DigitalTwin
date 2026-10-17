"""Non-overwriting supervisor for a named bounded experiment attempt."""
import argparse
from datetime import datetime, timezone
import json
import re
import sys
from common import HERE, PROJECT, LOCAL, sha, check_freeze
from mfg_twin.supervisor import BudgetWriter, Limits, supervise

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--attempt',required=True);args=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_]+',args.attempt):raise ValueError('Invalid attempt')
    freeze=check_freeze();limits=Limits(**freeze['configuration']['limits'])
    output=LOCAL/'runs'/args.attempt;output.mkdir(parents=True,exist_ok=False)
    writer=BudgetWriter(output,limit_bytes=limits.output_bytes)
    command=[sys.executable,str(HERE/'worker.py'),'--output',str(output)]
    writer.write_json('launch.json',{'utc':datetime.now(timezone.utc).isoformat(),'command':command,
        'cwd':str(PROJECT),'freeze_sha256':sha(HERE/'FREEZE.json')})
    result=supervise(command,cwd=PROJECT,output_dir=output,limits=limits,
        env={'TF_NUM_INTRAOP_THREADS':'1','TF_NUM_INTEROP_THREADS':'1','TF_CPP_MIN_LOG_LEVEL':'2',
             'CUDA_VISIBLE_DEVICES':'-1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
    writer.write_json('supervisor.json',result)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['status']=='completed' else 1)
