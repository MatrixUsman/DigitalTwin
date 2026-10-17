"""Seal the completed local research package without publishing or Git mutation."""
from pathlib import Path
from datetime import datetime,timezone
import json,re,subprocess
from v7_common import HERE,PROJECT,LOCAL,sha,check

freeze=check();man=PROJECT/'manuscript_recovery_v0.7';run=LOCAL/'runs/confirmation_001'
for name in ['BEFORE_FRESH_GENERATION.json','SCORES_SEALED.json']:
    d=json.loads((run/name).read_text())
    assert all(sha(run/k)==v for k,v in d['sha256'].items())
ver=json.loads((LOCAL/'verification.json').read_text());assert ver['status']=='passed' and ver['checks']==14635
qa=json.loads((man/'PDF_QA.json').read_text());assert qa['pages']==17
assert qa['pdf_sha256']==sha(PROJECT/'output/pdf/alarm-recovery-model-mismatch.pdf')
build=json.loads((man/'BUILD_RECEIPT.json').read_text());assert build['offline'] and build['returncode']==0
assert all(sha(man/k)==v for k,v in build['source_sha256'].items())
assert all(sha(PROJECT/k)==v for k,v in qa['render_sha256'].items())
assert json.loads((man/'AUDIT.json').read_text())['status']=='passed'
bad=[]
for p in list(HERE.glob('*.md'))+list(man.glob('*.md')):
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' in target or target.startswith('#'):continue
        target=target.split('#')[0]
        if target and not (p.parent/target).exists():bad.append([str(p),target])
assert not bad,bad
subprocess.run(['git','diff','--check'],cwd=PROJECT,check=True,capture_output=True,text=True)
# Preserve already frozen SVG serialization and generated-table formatting.
# The index contains independently staged files; never restage it to hide warnings.
cached=subprocess.run(['git','diff','--cached','--check'],cwd=PROJECT.parent,capture_output=True,text=True)
warning_files=sorted(set(re.findall(r'^([^\n]+?):\d+: (?:trailing whitespace|new blank line)',cached.stdout,re.M)))
expected={'manufacturing/output/recovery_v0.6/comparison.svg','manufacturing/output/recovery_v0.6/examples.svg',
          'manufacturing/research_cycles/recovery_v0.7/TABLES.md'}
assert set(warning_files)<=expected,warning_files
subprocess.run(['git','diff','HEAD','--check','--','.']+[':(exclude)'+p for p in sorted(expected)],
               cwd=PROJECT.parent,check=True,capture_output=True,text=True)
assert not subprocess.check_output(['git','diff','HEAD','--name-only','--','water','smart_grids'],cwd=PROJECT.parent,text=True).strip()
exclude={'PACKAGE_MANIFEST.json','HANDOFF_AUDIT.json'}
files=[p for root in [HERE,man,run,LOCAL/'tests'] for p in root.rglob('*')
       if p.is_file() and '__pycache__' not in p.parts and p.name not in exclude]
files += [LOCAL/'verification.json',PROJECT/'output/pdf/alarm-recovery-model-mismatch.pdf']
files += [p for p in (LOCAL/'pdf_build').glob('attempt_*/*') if p.suffix in ['.log','.json']]
bindings={str(p.relative_to(PROJECT)):sha(p) for p in sorted(set(files))}
manifest=dict(utc=datetime.now(timezone.utc).isoformat(),scope='Local workspace package; no public release; dependencies bound by scientific freeze',
    scientific_freeze_sha256=sha(HERE/'FREEZE.json'),source_inputs_preserved=True,sha256=bindings)
(HERE/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert all(sha(PROJECT/k)==v for k,v in bindings.items())
audit=dict(utc=datetime.now(timezone.utc).isoformat(),status='passed',package_files=len(bindings),
    scientific_sources=len(freeze['source_sha256']),prior_inputs=len(freeze['input_sha256']),
    experiment_attempts=1,episode_method_outcomes=3312,verification_checks=14635,pdf_pages=17,
    normal_and_score_seals_preserved=True,local_links_valid=True,scoped_git_whitespace_check_pass=True,
    cached_whitespace_warning_files=warning_files,
    sibling_projects_unchanged=True,primary_hypothesis='failed',original_algorithm='unestablished',
    author_review='pending',publication='not performed',package_manifest_sha256=sha(HERE/'PACKAGE_MANIFEST.json'))
(HERE/'HANDOFF_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps(audit))
