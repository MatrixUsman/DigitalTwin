"""Seal completed local evidence and check links/previous immutable identities."""
from datetime import datetime,timezone
import json
from pathlib import Path
import re
from support import HERE,PROJECT,LOCAL,sha,check_freeze

if __name__=='__main__':
    freeze=check_freeze(); paths=[]
    for directory in [HERE,LOCAL,PROJECT/'output/recovery_v0.6']:
        paths.extend(p for p in directory.rglob('*') if p.is_file() and '__pycache__' not in p.parts
                     and p.name not in ['PACKAGE_MANIFEST.json','HANDOFF_AUDIT.json'])
    identities={str(p.relative_to(PROJECT)):sha(p) for p in sorted(paths)}
    missing=[]
    for p in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if target.startswith(('https:','http:','#')):continue
            if not (p.parent/target.split('#')[0]).exists():missing.append([p.name,target])
    if missing:raise ValueError(missing)
    verification=json.loads((LOCAL/'verification.json').read_text())
    numerical=json.loads((LOCAL/'numerical_audit.json').read_text())
    access=json.loads((LOCAL/'config_access_audit.json').read_text())
    assert verification['status']==numerical['status']==access['status']=='passed'
    aggregate=json.loads((LOCAL/'runs/simulation_001/aggregate.json').read_text())
    assert aggregate==json.loads((HERE/'SUMMARY.json').read_text())
    for name,h in verification['run_sha256'].items():
        assert sha(LOCAL/'runs/simulation_001'/name)==h
    assert sha(HERE/'TABLES.md')==sha(LOCAL/'presentation_draft_001/TABLES.md')
    assert sha(HERE/'SUMMARY.json')==sha(LOCAL/'presentation_draft_001/SUMMARY.json')
    manifest=dict(utc=datetime.now(timezone.utc).isoformat(),type='Completed synthetic experiment; no publication approval',
        freeze_sha256=sha(HERE/'FREEZE.json'),sha256=identities)
    with (HERE/'PACKAGE_MANIFEST.json').open('x') as f:json.dump(manifest,f,indent=2);f.write('\n')
    receipt=dict(utc=datetime.now(timezone.utc).isoformat(),status='passed',source_bindings=len(freeze['source_sha256']),
        prior_input_bindings=len(freeze['input_sha256']),package_files=len(identities),synthetic_tests=23,
        replay_checks=verification['checks'],restricted_config_checks=access['checks'],numerical_trajectories=len(numerical['rows']),
        numerical_maximum=numerical['maximum'],missing_local_links=missing,primary_target_met=aggregate['primary_test']['passed'],
        numeric_presentation_tables_unchanged=True,visual_review='Comparison and final warmup-corrected examples inspected; readable labels/legends and all methods retained',
        package_sha256=sha(HERE/'PACKAGE_MANIFEST.json'),prior_scientific_sources_unchanged=True)
    with (HERE/'HANDOFF_AUDIT.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
    print(json.dumps(receipt,indent=2))
