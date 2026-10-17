import json,os,sys,subprocess,shutil
from datetime import datetime,timezone
from io14 import HERE,PROJECT,LOCAL,PREVIOUS,sha

if (HERE/'FREEZE.json').exists():raise SystemExit('Already frozen')
folder=LOCAL/'tests';folder.mkdir(parents=True,exist_ok=True)
attempt=folder/f'attempt_{len(list(folder.glob("attempt_*")))+1:03d}';attempt.mkdir(exist_ok=False)
for p in HERE.iterdir():
    if p.is_file():shutil.copy2(p,attempt/p.name)
command=[sys.executable,'-m','unittest','discover','-s',str(HERE),'-p','test_audit.py','-v']
env={**os.environ,**{k:'1' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONDONTWRITEBYTECODE']}}
r=subprocess.run(command,cwd=PROJECT,env=env,capture_output=True,text=True,timeout=45)
(attempt/'stdout.txt').write_text(r.stdout);(attempt/'stderr.txt').write_text(r.stderr)
(attempt/'receipt.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),command=command,cwd=str(PROJECT),python=sys.version,returncode=r.returncode,synthetic_only=True),indent=2)+'\n')
print(r.stdout+r.stderr)
if r.returncode:raise SystemExit(r.returncode)
prior=json.loads((PREVIOUS/'PACKAGE_MANIFEST.json').read_text())['sha256']
for name,h in prior.items():
    if sha(PROJECT/name)!=h:raise ValueError('Prior package changed '+name)
sources={str(p.relative_to(PROJECT)):sha(p) for p in list(HERE.iterdir())+list(attempt.iterdir()) if p.is_file()}
sources[str((PREVIOUS/'PACKAGE_MANIFEST.json').relative_to(PROJECT))]=sha(PREVIOUS/'PACKAGE_MANIFEST.json')
record=dict(utc=datetime.now(timezone.utc).isoformat(),configuration=json.loads((HERE/'config.json').read_text()),sources=sources,inputs=prior,
 tests=str((attempt/'receipt.json').relative_to(PROJECT)),authorization='user explicitly requests evidence for candidate novelty and attack advantage; small no-training diagnostic',prior_scientific_gate='v0.13 all-plant prediction criterion failed; unchanged')
with (HERE/'FREEZE.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(dict(sources=len(sources),prior_bindings=len(prior),freeze_sha256=sha(HERE/'FREEZE.json'))))
