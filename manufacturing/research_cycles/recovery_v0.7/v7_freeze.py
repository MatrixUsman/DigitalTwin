from datetime import datetime,timezone
import json
import subprocess
import sys
from v7_common import HERE,PROJECT,LOCAL,sha,guard,verify_map,config

if __name__=='__main__':
    if (HERE/'FREEZE.json').exists():raise FileExistsError('Consumed freeze')
    sources=sorted(list(HERE.glob('*.py'))+[HERE/'PLAN.md',HERE/'config.json'])
    hashes={str(p.relative_to(PROJECT)):sha(p) for p in sources}
    d=LOCAL/'tests';d.mkdir(parents=True,exist_ok=True);attempt=len(list(d.glob('*.json')))+1
    cmd=[sys.executable,str(HERE/'v7_test.py')];r=subprocess.run(cmd,cwd=PROJECT,capture_output=True,text=True,timeout=60)
    (d/f'tests_{attempt:03d}.log').write_text(r.stdout+r.stderr)
    (d/f'tests_{attempt:03d}.json').write_text(json.dumps(dict(command=cmd,returncode=r.returncode,source_sha256=hashes),indent=2)+'\n')
    print(r.stdout+r.stderr)
    if r.returncode:raise SystemExit(r.returncode)
    g=guard()
    for p in d.iterdir():g[str(p.relative_to(PROJECT))]=sha(p)
    verify_map(g);verify_map(hashes)
    record=dict(utc=datetime.now(timezone.utc).isoformat(),configuration=config(),source_sha256=hashes,input_sha256=g,
        type='Local prospective evaluation freeze; not external preregistration',fresh_generated=False)
    with (HERE/'FREEZE.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
    print(json.dumps(dict(sources=len(hashes),inputs=len(g))))
