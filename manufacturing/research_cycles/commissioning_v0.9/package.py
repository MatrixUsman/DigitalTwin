"""Preserve the completed local study; read-only Git checks, no publication."""
import json,re,subprocess
from datetime import datetime,timezone
from common9 import HERE,PROJECT,LOCAL,check,sha
f=check();run=LOCAL/'runs/normal_002';failure=LOCAL/'runs/normal_001'
fix=json.loads((HERE/'REPORTING_FIX.json').read_text())
for name,h in fix['source_sha256'].items():assert sha(HERE/name)==h
for name,h in fix['prior_sha256'].items():assert sha(failure/name)==h
for name in ['SELECTION_SEALED.json','NORMAL_SCORES_SEALED.json']:
    for key,h in json.loads((run/name).read_text())['sha256'].items():assert sha(run/key)==h
assert json.loads((run/'UNCHANGED_SELECTION.json').read_text())['selection_unchanged']
v=json.loads((HERE/'VERIFICATION.json').read_text());assert v['status']=='passed' and v['checks']==10293
assert v['verifier_sha256']==sha(HERE/'verify.py')
s=json.loads((run/'summary.json').read_text());assert s['status']=='completed' and s['role_outcomes']==576 and s['fresh_normal_episodes']==81
noise=json.loads((HERE/'NOISE_DIAGNOSTIC.json').read_text());assert noise['source_sha256']==sha(HERE/'noise_diagnostic.py')
presentation=json.loads((HERE/'PRESENTATION.json').read_text())
for mapping in ['source_sha256','outputs']:
    assert all(sha(PROJECT/key)==h for key,h in presentation[mapping].items())
assert presentation['generator_sha256']==sha(HERE/'present.py')
for name in ['RESULTS.md','MODEL_BANK.md']:
    assert (HERE/name).read_bytes()==(LOCAL/'presentation_attempt_001'/name).read_bytes()
# Scientific bindings in f include all previous source/freezes and historical handoff copies.
# Check current manuscript files separately; this task did not edit any manuscript/PDF.
prev=PROJECT/'manuscript_recovery_v0.8r1/TITLE_REVISION_AUDIT.json';ta=json.loads(prev.read_text())
for key,h in ta['new_source_sha256'].items():assert sha(PROJECT/key)==h
assert sha(PROJECT/'output/pdf/after-robotic-digital-twins.pdf')==ta['pdf_sha256']
links=0
for path in HERE.glob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
        if '://' in target or target.startswith('#'):continue
        assert (path.parent/target.split('#')[0]).exists(),(path,target);links+=1
scopes=['manufacturing/research_cycles/commissioning_v0.9','manufacturing/STATUS.md','manufacturing/AGENTS.md','manufacturing/README.md','manufacturing/docs/WORK_LOG.md','manufacturing/docs/PAPER_ROADMAP.md','docs/RESEARCH_PLAYBOOK.md','docs/WORK_LOG.md']
for cmd in [['git','diff','--check','--'],['git','diff','--cached','--check','--']]:subprocess.run(cmd+scopes,cwd=PROJECT.parent,capture_output=True,text=True,check=True)
for path in HERE.glob('*'):
    if path.suffix in ['.py','.md','.json']:
        assert all(line.rstrip()==line for line in path.read_text().splitlines()),path
assert not subprocess.check_output(['git','diff','HEAD','--name-only','--','water','smart_grids'],cwd=PROJECT.parent,text=True).strip()
exclude={'PACKAGE_MANIFEST.json','HANDOFF_AUDIT.json','.DS_Store'}
roots=[HERE,LOCAL/'runs',LOCAL/'tests',LOCAL/'sources',LOCAL/'prior_handoff',LOCAL/'prior_workspace',LOCAL/'presentation_attempt_001',LOCAL/'packaging',PROJECT/'output/commissioning_v0.9']
files={p for root in roots for p in root.rglob('*') if p.is_file() and p.name not in exclude and '__pycache__' not in p.parts}
# Snapshot mutable handoffs for this package so later status updates never alter its evidence.
for name in ['STATUS.md','AGENTS.md','README.md','docs/WORK_LOG.md','docs/PAPER_ROADMAP.md','docs/PAPER_ROADMAP_V0.9.md']:
    src=PROJECT/name;target=LOCAL/'completed_handoff'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(src.read_bytes());files.add(target)
for name in ['docs/WORK_LOG.md','docs/RESEARCH_PLAYBOOK.md']:
    target=LOCAL/'completed_workspace'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((PROJECT.parent/name).read_bytes());files.add(target)
bindings={str(p.relative_to(PROJECT)):sha(p) for p in sorted(files)}
manifest=dict(utc=datetime.now(timezone.utc).isoformat(),scope='Local normal-only development package, no public release. Mutable handoffs archived; immutable evidence remains at original paths.',scientific_freeze_sha256=sha(HERE/'FREEZE.json'),sha256=bindings)
(HERE/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');assert all(sha(PROJECT/k)==h for k,h in bindings.items())
audit=dict(utc=datetime.now(timezone.utc).isoformat(),status='passed',scientific_sources=len(f['source_sha256']),prior_inputs=len(f['input_sha256']),normal_files=66,
    synthetic_tests=23,reporting_regression=1,post_run_checks=10293,worker_attempts=2,completed_runs=1,candidate_fits=63,archived_normal_checks=15,fresh_normal_episodes=81,
    role_outcomes=576,normal_admission=False,attack_experiments=0,local_links_checked=links,package_files=len(bindings),package_sha256=sha(HERE/'PACKAGE_MANIFEST.json'),
    visual_qa='Final PNG inspected: clear labels, 95% requirement shown, no clipping/overlap.',previous_manuscripts_preserved=True,scoped_whitespace='passed',published=False)
(HERE/'HANDOFF_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit,indent=2))
