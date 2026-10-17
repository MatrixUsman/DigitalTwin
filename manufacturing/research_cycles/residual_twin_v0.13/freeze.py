"""Archive synthetic-test attempts and bind permitted inputs before fitting."""
import json,os,subprocess,sys,shutil
from datetime import datetime,timezone
from io13 import HERE,PROJECT,LOCAL,OLD,INPUT,FITS,sha

if (HERE/'FREEZE.json').exists():raise SystemExit('Freeze already exists')
c=json.loads((HERE/'config.json').read_text())
assert set(c['development_indices']).isdisjoint(c['calibration_indices'])
tests=LOCAL/'tests';tests.mkdir(parents=True,exist_ok=True)
attempt=tests/f'attempt_{len(list(tests.glob("attempt_*")))+1:03d}';attempt.mkdir(exist_ok=False)
for p in HERE.iterdir():
    if p.suffix in ['.py','.json','.md']:shutil.copy2(p,attempt/p.name)
command=[sys.executable,'-m','unittest','discover','-s',str(HERE),'-p','test_model.py','-v']
env={**os.environ,**{k:'1' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
  'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONDONTWRITEBYTECODE']}}
r=subprocess.run(command,cwd=PROJECT,env=env,text=True,capture_output=True,timeout=45)
(attempt/'stdout.txt').write_text(r.stdout);(attempt/'stderr.txt').write_text(r.stderr)
receipt=dict(utc=datetime.now(timezone.utc).isoformat(),command=command,cwd=str(PROJECT),returncode=r.returncode,
             python=sys.version,synthetic_only=True,source_sha256={p.name:sha(p) for p in attempt.glob('*.py')})
(attempt/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(r.stdout+r.stderr)
if r.returncode:raise SystemExit(r.returncode)
oldfreeze=json.loads((OLD/'FREEZE.json').read_text());oldpackage=json.loads((OLD/'PACKAGE_MANIFEST.json').read_text())['sha256']
inputs={}
for plant in ['Q1','Q2','Q3']:
    names=[f'train_{plant}_{j}.npz' for j in range(3)] + [f'cal_{plant}_{j:02d}.npz' for j in c['development_indices']+c['calibration_indices']]
    for name in names:
        p=INPUT/name;h=sha(p)
        if h!=oldfreeze['normal_files'][name]:raise ValueError('Changed historical normal file '+name)
        inputs[str(p.relative_to(PROJECT))]=h
selection=json.loads((FITS/'selection.json').read_text())
artifacts=[FITS/'selection.json']+[FITS/f'fit_{p}_{selection["selected"][p]["overall"]}.npz' for p in ['Q1','Q2','Q3']]
for p in artifacts:
    name=str(p.relative_to(PROJECT));h=sha(p)
    if oldpackage[name]!=h:raise ValueError('Changed historical artifact '+name)
    inputs[name]=h
sources=list(HERE.glob('*.py'))+list(HERE.glob('*.md'))+[HERE/'config.json']
for version in ['recovery_v0.6','recovery_v0.7','recovery_v0.8','commissioning_v0.9']:
    folder=HERE.parent/version;sources.extend(folder.glob('*.py'))
    sources.extend(p for p in [folder/'FREEZE.json',folder/'PACKAGE_MANIFEST.json'] if p.exists())
sources+=list((PROJECT/'src/mfg_twin').glob('*.py'))+list(attempt.iterdir())
for p in sources:
    name=str(p.relative_to(PROJECT))
    if name in oldpackage and sha(p)!=oldpackage[name]:raise ValueError('Changed historical source '+name)
record=dict(utc=datetime.now(timezone.utc).isoformat(),configuration=c,
 sources={str(p.relative_to(PROJECT)):sha(p) for p in sorted(set(sources))},inputs=inputs,
 tests=str((attempt/'receipt.json').relative_to(PROJECT)),scope='normal-only prospective parameterizations within existing simulator; no independent robot or attack evidence')
with (HERE/'FREEZE.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(dict(sources=len(record['sources']),inputs=len(inputs),freeze_sha256=sha(HERE/'FREEZE.json'))))
