"""Seal completed evidence; archive mutable handoffs instead of freezing live paths."""
import csv
import json
import re
import shutil
from datetime import datetime, timezone
from io_utils import HERE, PROJECT, LOCAL, RUN, check_frozen, sha256

if (HERE/'PACKAGE_MANIFEST.json').exists(): raise ValueError('Preserve completed package.')
freeze=check_frozen();v=json.loads((HERE/'VERIFICATION.json').read_text())
assert v['status']=='passed' and v['summary_sha256']==sha256(RUN/'summary.json')
s=json.loads((RUN/'summary.json').read_text());records=json.loads((HERE/'ALL_OUTCOMES.json').read_text())
assert records==s['records'] and len(records)==216
with (HERE/'all_outcomes.csv').open() as stream:
    rows=list(csv.DictReader(stream))
assert len(rows)==216
for a,b in zip(rows,records):
    assert a['trace']==b['trace'] and a['method']==b['method']
    assert float(a['fraction'])==b['fraction'] and int(a['certified'])==b['certified']
prior_counts={}
for manifest in freeze['prior_packages']:
    bindings=json.loads((PROJECT/manifest).read_text())['sha256']
    for name,digest in bindings.items(): assert sha256(PROJECT/name)==digest,name
    prior_counts[manifest]=len(bindings)
links=0
for path in HERE.glob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
        if target.startswith(('http://','https://','#')):continue
        assert (path.parent/target.split('#')[0]).exists(),(path.name,target)
        links+=1
handoff=LOCAL/'completed_handoff';handoff.mkdir(exist_ok=False)
for name in ['AGENTS.md','STATUS.md','docs/WORK_LOG.md']:
    shutil.copyfile(PROJECT/name,handoff/name.replace('/','__'))
audit=dict(utc=datetime.now(timezone.utc).isoformat(),status='passed',frozen_sources=len(freeze['source_sha256']),
           preserved_prior_packages=prior_counts,relative_links=links,
           archived_handoffs=['AGENTS.md','STATUS.md','docs/WORK_LOG.md'],
           completed_outcomes=216,software_tests=20,artifact_verification_checks=v['checks'])
with (HERE/'HANDOFF_AUDIT.json').open('x') as stream:json.dump(audit,stream,indent=2);stream.write('\n')
files=[]
for base in [HERE,LOCAL]:
    for p in base.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name!='.DS_Store':
            if p.is_symlink():raise ValueError('unexpected link')
            files.append(p)
bindings={str(p.relative_to(PROJECT)):sha256(p) for p in sorted(files)}
with (HERE/'PACKAGE_MANIFEST.json').open('x') as stream:
    json.dump(dict(utc=datetime.now(timezone.utc).isoformat(),sha256=bindings,
                   scope='completed standard control and synthetic normal diagnostic; mutable live handoffs archived'),stream,indent=2);stream.write('\n')
print('Sealed',len(bindings),'files; checked',links,'relative links; prior packages unchanged.')
