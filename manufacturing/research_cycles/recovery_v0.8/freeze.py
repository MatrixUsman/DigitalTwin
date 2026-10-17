import json,subprocess,sys
from datetime import datetime,timezone
from common import HERE,OLD,PROJECT,LOCAL,sha,guard,verify_map,config,write_json
if (HERE/'FREEZE.json').exists():raise FileExistsError('Freeze already exists')
sources=sorted(list(HERE.glob('*.py'))+[HERE/'PLAN.md',HERE/'config.json',HERE/'PRIOR_ART.md'])
hashes={str(p.relative_to(PROJECT)):sha(p) for p in sources}
d=LOCAL/'tests';d.mkdir(parents=True,exist_ok=True);attempt=len(list(d.glob('*.json')))+1
cmd=[sys.executable,str(HERE/'test_core.py')];r=subprocess.run(cmd,cwd=PROJECT,capture_output=True,text=True,timeout=60)
(d/f'tests_{attempt:03d}.log').write_text(r.stdout+r.stderr)
write_json(d/f'tests_{attempt:03d}.json',dict(command=cmd,returncode=r.returncode,source_sha256=hashes));print(r.stdout+r.stderr)
if r.returncode:raise SystemExit(r.returncode)
g=guard();old=json.loads((OLD/'FREEZE.json').read_text());g.update(old['source_sha256']);g.update(old['input_sha256'])
for p in d.iterdir():g[str(p.relative_to(PROJECT))]=sha(p)
for p in (LOCAL/'sources').glob('*'):
 if p.is_file():g[str(p.relative_to(PROJECT))]=sha(p)
verify_map(g);verify_map(hashes)
record=dict(utc=datetime.now(timezone.utc).isoformat(),configuration=config(),source_sha256=hashes,input_sha256=g,fresh_generated=False,type='Local prospective freeze')
with (HERE/'FREEZE.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(dict(sources=len(hashes),inputs=len(g))))
