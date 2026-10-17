"""Seal the completed approved run without binding mutable project handoffs."""
import csv
import json
import re
import shutil
from pathlib import Path
from datetime import datetime, timezone
from io_utils import sha256, verify_frozen
from authorization import check_authorization

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
LOCAL = PROJECT/'local/casper_convergence_v0.11'
RUN = LOCAL/'runs/pilot_001'
manifest_path = HERE/'PACKAGE_MANIFEST.json'
if manifest_path.exists():
    raise ValueError('Preserve the existing completed package.')

freeze = json.loads((HERE/'FREEZE.json').read_text())
verify_frozen(PROJECT, freeze)
auth = json.loads((HERE/'RUN_AUTHORIZATION.json').read_text())
check_authorization(auth, sha256(HERE/'FREEZE.json'), freeze['configuration']['limits'])
v = json.loads((HERE/'VERIFICATION.json').read_text())
assert v['status'] == 'passed' and v['verified_models'] == 9
assert sha256(HERE/'verify.py') == v['verifier_sha256']
assert sha256(RUN/'summary.json') == v['summary_sha256']
assert sha256(HERE/'RUN_AUTHORIZATION.json') == json.loads((LOCAL/'execution_authorization.json').read_text())['authorization_sha256']
test = json.loads((PROJECT/freeze['test_receipt']).read_text())
assert test['tests'] == 17 and test['returncode'] == 0
assert sha256(PROJECT/freeze['test_receipt'].replace('receipt.json', 'tests.log')) == test['log_sha256']

counts = {}
prior = json.loads((PROJECT/'research_cycles/commissioning_v0.9/FREEZE.json').read_text())
for group in ['source_sha256', 'input_sha256']:
    for name, expected in prior[group].items():
        assert sha256(PROJECT/name) == expected, name
    counts[group] = len(prior[group])
for rel in ['research_cycles/commissioning_v0.9/PACKAGE_MANIFEST.json',
            'manuscript_after_v1.0/PACKAGE_MANIFEST.json',
            'research_cycles/casper_comparison_v0.10/PACKAGE_MANIFEST.json']:
    bindings = json.loads((PROJECT/rel).read_text())['sha256']
    for name, expected in bindings.items():
        assert sha256(PROJECT/name) == expected, name
    counts[rel] = len(bindings)

presentation = json.loads((HERE/'PRESENTATION.json').read_text())
assert presentation['script_sha256'] == sha256(HERE/'present.py')
assert presentation['source_summary_sha256'] == sha256(RUN/'summary.json')
for name, expected in presentation['artifacts'].items():
    assert sha256(HERE/name) == expected, name
summary = json.loads((RUN/'summary.json').read_text())
with (HERE/'all_outcomes.csv').open() as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 9
for row, model in zip(rows, summary['models']):
    assert row['model'] == model['model']
    assert float(row['standardized_mse']) == model['standardized_mse']
    assert float(row['native_mse']) == model['native_mse']
with (HERE/'per_channel_errors.csv').open() as handle:
    channels = list(csv.DictReader(handle))
assert len(channels) == 81
for row in channels:
    model = next(r for r in summary['models'] if r['model'] == row['model'])
    j = freeze['configuration']['columns'].index(row['channel'])
    assert float(row['standardized_mse']) == model['channel_standardized_mse'][j]
    assert float(row['native_mse']) == model['channel_native_mse'][j]
assert (HERE/'RESULTS.md').exists()

links = 0
for path in HERE.glob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if target.startswith(('http://', 'https://', '#')):
            continue
        assert (path.parent/target.split('#')[0]).exists(), (path.name, target)
        links += 1

archive = LOCAL/'completed_handoff'
archive.mkdir(exist_ok=False)
for name in ['AGENTS.md', 'STATUS.md', 'docs/WORK_LOG.md']:
    dest = archive/name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PROJECT/name, dest)

audit = dict(utc=datetime.now(timezone.utc).isoformat(), status='passed', local_links=links,
             preserved=counts, frozen_sources=len(freeze['source_sha256']),
             model_outcomes=9, per_channel_rows=81, explicit_user_approval=True,
             completion='one authorized scientific execution; all outcomes retained',
             scope='Saved-result arithmetic and package integrity, not independent security or physics validation.')
(HERE/'HANDOFF_AUDIT.json').write_text(json.dumps(audit, indent=2)+'\n')
paths = [p for base in [HERE, LOCAL] for p in base.rglob('*')
         if p.is_file() and not any(x in p.parts for x in ['__pycache__', 'plot_cache']) and p.name != '.DS_Store']
manifest = dict(utc=datetime.now(timezone.utc).isoformat(),
                scope='Completed local authorized convergence study; no publication. Mutable handoff snapshots archived.',
                scientific_freeze_sha256=sha256(HERE/'FREEZE.json'),
                sha256={str(p.relative_to(PROJECT)):sha256(p) for p in sorted(paths)})
with manifest_path.open('x') as handle:
    handle.write(json.dumps(manifest, indent=2)+'\n')
print(json.dumps(dict(status='passed', sealed_files=len(paths), local_links=links, preserved=counts), indent=2))
