"""Run synthetic tests, preserve their receipt, then bind before real replay."""
import argparse
from datetime import datetime, timezone
import json
import re
import subprocess
import sys
from common import HERE, PROJECT, LOCAL, sha, upstream_guard

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--attempt',required=True);args=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_]+',args.attempt):raise ValueError('Invalid attempt')
    if (HERE/'FREEZE.json').exists():raise ValueError('Already frozen')
    output=LOCAL/'tests'/args.attempt;output.mkdir(parents=True,exist_ok=False)
    command=[sys.executable,'-m','unittest','-v','test_mechanism']
    result=subprocess.run(command,cwd=HERE,capture_output=True,text=True,timeout=60)
    (output/'tests.log').write_text(result.stdout+result.stderr)
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'command':command,'cwd':str(HERE),
        'returncode':result.returncode,'log_sha256':sha(output/'tests.log'),'synthetic':True}
    (output/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(result.stdout+result.stderr)
    if result.returncode:raise SystemExit(result.returncode)
    sources={str(p.relative_to(PROJECT)):sha(p) for p in HERE.iterdir() if p.suffix in ['.py','.json','.md']}
    sources['src/mfg_twin/supervisor.py']=sha(PROJECT/'src/mfg_twin/supervisor.py')
    inputs=upstream_guard()
    inputs[str((output/'receipt.json').relative_to(PROJECT))]=sha(output/'receipt.json')
    inputs[str((output/'tests.log').relative_to(PROJECT))]=sha(output/'tests.log')
    freeze={'study_id':'manufacturing-limitation-v0.4','utc':datetime.now(timezone.utc).isoformat(),
        'configuration':json.loads((HERE/'config.json').read_text()),'source_sha256':sources,'input_sha256':inputs,
        'raw_access':False,'interventions_executed':False,'type':'local pre-execution freeze, not external registration'}
    (HERE/'FREEZE.json').write_text(json.dumps(freeze,indent=2)+'\n')
    print('Frozen',len(sources),'source and',len(inputs),'input identities.')
