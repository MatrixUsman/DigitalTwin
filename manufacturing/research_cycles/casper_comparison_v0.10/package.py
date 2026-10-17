"""Seal the completed local pilot and archive mutable handoff documents."""
import json
import re
import shutil
from pathlib import Path
from datetime import datetime, timezone
from io_utils import sha256, verify_frozen

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
LOCAL = PROJECT / 'local/casper_comparison_v0.10'
manifest_path = HERE / 'PACKAGE_MANIFEST.json'
if manifest_path.exists():
    raise ValueError('Preserve the completed package; do not overwrite its manifest.')

freeze = json.loads((HERE/'FREEZE.json').read_text())
verify_frozen(PROJECT, freeze)
v = json.loads((HERE/'VERIFICATION.json').read_text())
assert v['status'] == 'passed' and v['verified_models'] == 9
assert sha256(HERE/'verify.py') == v['verifier_sha256']
assert sha256(LOCAL/'runs/pilot_002/summary.json') == v['summary_sha256']
test = json.loads((PROJECT/freeze['test_receipt']).read_text())
assert sha256(PROJECT/freeze['test_receipt'].replace('receipt.json', 'tests.log')) == test['log_sha256']

prior = json.loads((PROJECT/'research_cycles/commissioning_v0.9/FREEZE.json').read_text())
for group in ['source_sha256', 'input_sha256']:
    for name, expected in prior[group].items():
        assert sha256(PROJECT/name) == expected, name
for rel in ['research_cycles/commissioning_v0.9/PACKAGE_MANIFEST.json', 'manuscript_after_v1.0/PACKAGE_MANIFEST.json']:
    for name, expected in json.loads((PROJECT/rel).read_text())['sha256'].items():
        assert sha256(PROJECT/name) == expected, name

next_dir = PROJECT/'research_cycles/casper_convergence_v0.11'
next_freeze = json.loads((next_dir/'FREEZE.json').read_text())
verify_frozen(PROJECT, next_freeze)
assert not (PROJECT/'local/casper_convergence_v0.11/runs').exists(), 'unexpected pending-run execution'
assert json.loads((next_dir/'RUN_AUTHORIZATION.json').read_text())['status'] == 'pending_user_approval'

archive = LOCAL/'completed_handoff'
archive.mkdir(exist_ok=False)
for name in ['AGENTS.md', 'STATUS.md', 'docs/WORK_LOG.md']:
    dest = archive/name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PROJECT/name, dest)
# Snapshot pending successor readiness rather than bind its mutable approval file.
shutil.copyfile(next_dir/'RUN_AUTHORIZATION.json', archive/'v0.11_pending_authorization.json')
shutil.copyfile(next_dir/'README.md', archive/'v0.11_pending_README.md')

links = 0
for path in HERE.glob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if target.startswith(('https://', 'http://', '#')):
            continue
        dest = target.split('#')[0]
        assert (path.parent/dest).exists(), (path.name, dest)
        links += 1

audit = dict(utc=datetime.now(timezone.utc).isoformat(), status='passed', local_links=links,
             preserved_prior_sources=len(prior['source_sha256']), preserved_prior_inputs=len(prior['input_sha256']),
             frozen_sources=len(freeze['source_sha256']), successor_frozen_sources=len(next_freeze['source_sha256']),
             successor_training='pending actual user resource approval', published=False,
             scope='Integrity and packaging; no new observation, fit or experimental claim.')
(HERE/'HANDOFF_AUDIT.json').write_text(json.dumps(audit, indent=2)+'\n')
paths = [p for base in [HERE, LOCAL] for p in base.rglob('*')
         if p.is_file() and '__pycache__' not in p.parts and p.name != '.DS_Store']
manifest = dict(utc=datetime.now(timezone.utc).isoformat(),
                scope='Completed local common-IMU pilot; no public release. Mutable status/approval are archived snapshots.',
                scientific_freeze_sha256=sha256(HERE/'FREEZE.json'),
                sha256={str(p.relative_to(PROJECT)):sha256(p) for p in sorted(paths)})
with manifest_path.open('x') as handle:
    handle.write(json.dumps(manifest, indent=2)+'\n')
print(json.dumps(dict(status='passed', sealed_files=len(paths), **{k:v for k,v in audit.items() if k!='status'}), indent=2))
