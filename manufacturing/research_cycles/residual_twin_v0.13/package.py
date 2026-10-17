"""Seal local evidence and snapshot mutable handoffs; no upload/publication."""
import json,shutil
from datetime import datetime,timezone
from io13 import HERE,PROJECT,LOCAL,RUN,sha,check

freeze=check()
if (HERE/'PACKAGE_MANIFEST.json').exists():raise SystemExit('Package already sealed')
verification=json.loads((HERE/'VERIFICATION.json').read_text())
for name,h in verification['run_sha256'].items():
    if sha(RUN/name)!=h:raise ValueError('Changed verified run '+name)
presentation=json.loads((HERE/'PRESENTATION.json').read_text())
for name,h in presentation['outputs'].items():
    if sha(HERE/name)!=h:raise ValueError('Changed presented output '+name)
snapshot=LOCAL/'completed_handoff';snapshot.mkdir(parents=True,exist_ok=False)
for name in ['AGENTS.md','STATUS.md','docs/WORK_LOG.md','docs/TEACHER_REVIEW_ACTIONS_V0.13.md']:
    target=snapshot/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PROJECT/name,target)
bindings=dict(freeze['sources']);bindings.update(freeze['inputs'])
paths=list(HERE.iterdir())+list(RUN.iterdir())+list((LOCAL/'tests').rglob('*'))+list(snapshot.rglob('*'))
for p in paths:
    if p.is_file() and '__pycache__' not in p.parts:bindings[str(p.relative_to(PROJECT))]=sha(p)
record=dict(utc=datetime.now(timezone.utc).isoformat(),scope='local candidate-model evidence; no public release',
            freeze_sha256=sha(HERE/'FREEZE.json'),files=len(bindings),sha256=dict(sorted(bindings.items())))
for name,h in bindings.items():
    if sha(PROJECT/name)!=h:raise ValueError('Package identity '+name)
with (HERE/'PACKAGE_MANIFEST.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(dict(files=len(bindings),manifest_sha256=sha(HERE/'PACKAGE_MANIFEST.json'))))
