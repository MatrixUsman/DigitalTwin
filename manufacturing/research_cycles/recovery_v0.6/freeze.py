"""Run synthetic checks, preserve their log, and freeze before fresh generation."""
from datetime import datetime,timezone
import json
import subprocess
import sys
from support import HERE,PROJECT,LOCAL,sha,config,old_guard,verify_map

if __name__=='__main__':
    if (HERE/'FREEZE.json').exists():raise FileExistsError('Freeze already exists')
    testdir=LOCAL/'tests';testdir.mkdir(parents=True,exist_ok=True)
    attempt=len(list(testdir.glob('tests_*.json')))+1
    sources=sorted(list(HERE.glob('*.py'))+[HERE/n for n in ['config.json','PLAN.md','PRIOR_ART.md','DIAGNOSIS.json']])
    hashes={str(p.relative_to(PROJECT)):sha(p) for p in sources}
    command=[sys.executable,str(HERE/'test_core.py')]
    result=subprocess.run(command,cwd=PROJECT,capture_output=True,text=True,timeout=60)
    log=testdir/f'tests_{attempt:03d}.log';log.write_text(result.stdout+result.stderr)
    receipt=dict(utc=datetime.now(timezone.utc).isoformat(),command=command,cwd=str(PROJECT),
                 returncode=result.returncode,source_sha256=hashes,log_sha256=sha(log))
    (testdir/f'tests_{attempt:03d}.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(result.stdout+result.stderr)
    if result.returncode:raise SystemExit(result.returncode)
    verify_map(hashes);guard=old_guard()
    for path in list(testdir.iterdir())+list((PROJECT/'src/mfg_twin').glob('*.py')):
        guard[str(path.relative_to(PROJECT))]=sha(path)
    verify_map(guard)
    record=dict(utc=datetime.now(timezone.utc).isoformat(),configuration=config(),source_sha256=hashes,
        input_sha256=guard,type='Local prospective simulation freeze; not external preregistration',
        fresh_observations_generated=False,raw_access=False)
    with (HERE/'FREEZE.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
    print(json.dumps(dict(frozen_sources=len(hashes),input_bindings=len(guard))))
