"""Seal local evidence and snapshot mutable handoffs; no upload/publication."""
import json
import shutil
from datetime import datetime, timezone
from io14 import HERE, PROJECT, LOCAL, RUN, sha, check

freeze = check()
if (HERE / 'PACKAGE_MANIFEST.json').exists():
    raise SystemExit('Package already sealed')
verification = json.loads((HERE / 'VERIFICATION.json').read_text())
for name, digest in verification['run_sha256'].items():
    if sha(RUN / name) != digest:
        raise ValueError('Changed verified run ' + name)
presentation = json.loads((HERE / 'PRESENTATION.json').read_text())
if presentation['verified_run_sha256'] != sha(HERE / 'VERIFICATION.json'):
    raise ValueError('Changed presentation input')
for name, digest in presentation['outputs'].items():
    if sha(HERE / name) != digest:
        raise ValueError('Changed presented output ' + name)

snapshot = LOCAL / 'completed_handoff'
snapshot.mkdir(parents=True, exist_ok=False)
for name in ['AGENTS.md', 'STATUS.md', 'docs/WORK_LOG.md',
             'docs/TEACHER_REVIEW_ACTIONS_V0.13.md']:
    target = snapshot / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROJECT / name, target)

bindings = dict(freeze['sources'])
bindings.update(freeze['inputs'])
paths = (list(HERE.iterdir()) + list(RUN.iterdir()) +
         list((LOCAL / 'tests').rglob('*')) + list(snapshot.rglob('*')))
for path in paths:
    if path.is_file() and '__pycache__' not in path.parts:
        bindings[str(path.relative_to(PROJECT))] = sha(path)
record = dict(utc=datetime.now(timezone.utc).isoformat(),
              scope='local frozen attack-audit evidence; no public release',
              freeze_sha256=sha(HERE / 'FREEZE.json'),
              files=len(bindings), sha256=dict(sorted(bindings.items())))
for name, digest in bindings.items():
    if sha(PROJECT / name) != digest:
        raise ValueError('Package identity ' + name)
with (HERE / 'PACKAGE_MANIFEST.json').open('x') as output:
    json.dump(record, output, indent=2)
    output.write('\n')
print(json.dumps(dict(files=len(bindings),
                      manifest_sha256=sha(HERE / 'PACKAGE_MANIFEST.json'))))
