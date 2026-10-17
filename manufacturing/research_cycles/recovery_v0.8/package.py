"""Seal the completed local v0.8 package; no training, publication or Git writes."""
import json
import re
import subprocess
from datetime import datetime, timezone

from common import HERE, LOCAL, PROJECT, check, sha, write_json


def main():
    freeze = check()
    run = LOCAL / 'runs/confirmation_002'
    manuscript = PROJECT / 'manuscript_recovery_v0.8'
    for name in ['BEFORE_FRESH_GENERATION.json', 'SCORES_SEALED.json']:
        seal = json.loads((run / name).read_text())
        assert all(sha(run / key) == value for key, value in seal['sha256'].items())
    result = json.loads((run / 'summary.json').read_text())
    assert result['episodes'] == 216 and result['outcomes'] == 2808
    rows = json.loads((run / 'aggregate.json').read_text())['rows']
    assert result['methods'] == 13 and len(rows) == 91
    assert len([row for row in rows if row['stratum'] == 'pooled']) == 13
    assert len({row['method'] for row in rows}) == 13
    verified = json.loads((HERE / 'VERIFICATION.json').read_text())
    assert verified['status'] == 'passed' and verified['checks'] == 9610
    old = json.loads((HERE.parent / 'recovery_v0.7/PACKAGE_MANIFEST.json').read_text())
    assert len(old['sha256']) == 260
    assert all(sha(PROJECT / key) == value for key, value in old['sha256'].items())
    assert sha(PROJECT / 'output/pdf/alarm-recovery-model-mismatch-revised.pdf') == '9252c33e1d33c9f03308acb8e2b1839bb8079a2d7bb478da6b69245dabde8064'
    qa = json.loads((manuscript / 'PDF_QA.json').read_text())
    pdf = PROJECT / 'output/pdf/counterfactual-recovery-manuscript.pdf'
    assert qa['status'] == 'passed' and qa['pages'] == 10 and qa['pdf_sha256'] == sha(pdf)
    assert all(sha(PROJECT / key) == value for key, value in qa['page_sha256'].items())
    build = json.loads((manuscript / 'BUILD_RECEIPT.json').read_text())
    assert build['returncode'] == 0 and build['offline'] and build['pdf_sha256'] == sha(pdf)
    assert all(sha(manuscript / key) == value for key, value in build['source_sha256'].items())
    audit = json.loads((manuscript / 'AUDIT.json').read_text())
    assert audit['status'] == 'passed_with_scientific_limits' and audit['journal_ready'] is False
    assert all(sha(PROJECT / key) == value for key, value in audit['source_sha256'].items())
    links = []
    for path in list(HERE.glob('*.md')) + list(manuscript.glob('*.md')):
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            target = target.split('#')[0]
            assert not target or (path.parent / target).exists(), (path, target)
            links.append(target)
    paths = [HERE, manuscript, LOCAL / 'runs', LOCAL / 'tests', LOCAL / 'verification',
             LOCAL / 'sources', LOCAL / 'pdf_build', LOCAL / 'pdf_qa',
             LOCAL / 'pdf_qa_final', LOCAL / 'pdf_qa_delivery', PROJECT / 'output/recovery_v0.8']
    exclude = {'PACKAGE_MANIFEST.json', 'HANDOFF_AUDIT.json', '.DS_Store'}
    files = {p for root in paths for p in root.rglob('*')
             if p.is_file() and p.name not in exclude and '__pycache__' not in p.parts}
    files.add(pdf)
    files.update(PROJECT / p for p in ['AGENTS.md', 'STATUS.md', 'README.md',
                                      'docs/WORK_LOG.md', 'docs/PAPER_ROADMAP.md'])
    bindings = {str(p.relative_to(PROJECT)): sha(p) for p in sorted(files)}
    shared = {name: sha(PROJECT.parent / name)
              for name in ['docs/RESEARCH_PLAYBOOK.md', 'docs/WORK_LOG.md']}
    scopes = ['manufacturing/research_cycles/recovery_v0.8',
              'manufacturing/manuscript_recovery_v0.8', 'manufacturing/AGENTS.md',
              'manufacturing/STATUS.md', 'manufacturing/README.md',
              'manufacturing/docs/WORK_LOG.md', 'manufacturing/docs/PAPER_ROADMAP.md',
              'docs/RESEARCH_PLAYBOOK.md', 'docs/WORK_LOG.md']
    # Read-only: inspect both working tree and existing index; never stage/reset it.
    for command in [['git', 'diff', '--check', '--'], ['git', 'diff', '--cached', '--check', '--']]:
        subprocess.run(command + scopes, cwd=PROJECT.parent, check=True, capture_output=True, text=True)
    untracked_whitespace = []
    for path in files:
        if path.suffix not in {'.py', '.tex', '.md', '.json'} or LOCAL in path.parents:
            continue
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if line.rstrip() != line:
                untracked_whitespace.append([str(path.relative_to(PROJECT)), number])
    assert not untracked_whitespace, untracked_whitespace
    assert not subprocess.check_output(['git', 'diff', 'HEAD', '--name-only', '--', 'water', 'smart_grids'],
                                       cwd=PROJECT.parent, text=True).strip()
    manifest = dict(utc=datetime.now(timezone.utc).isoformat(),
                    scope='Local evidence package; no upload or public release. Earlier packages remain immutable.',
                    scientific_freeze_sha256=sha(HERE / 'FREEZE.json'), sha256=bindings,
                    workspace_sha256=shared)
    write_json(HERE / 'PACKAGE_MANIFEST.json', manifest)
    assert all(sha(PROJECT / key) == value for key, value in bindings.items())
    handoff = dict(utc=datetime.now(timezone.utc).isoformat(), status='passed_with_scientific_limits',
                   package_files=len(bindings), shared_files=len(shared),
                   scientific_sources=len(freeze['source_sha256']), prior_bindings=len(freeze['input_sha256']),
                   preserved_v07_package_files=260, preserved_revised_v07_pdf=True,
                   launch_attempts=2, completed_scientific_runs=1, episodes=216, methods=13, outcomes=2808,
                   pre_run_synthetic_tests=14, verification_checks=9610, local_links_checked=len(links),
                   pdf_pages=10, pdf_sha256=sha(pdf), package_sha256=sha(HERE / 'PACKAGE_MANIFEST.json'),
                   scoped_whitespace_checks='passed; frozen older files and independent Git index preserved',
                   primary_criterion='failed', candidate_decision='reject_uncertainty_addition', journal_ready=False,
                   next_task='Normal-only reference adequacy and clearance feasibility before any new attack study.',
                   published=False)
    write_json(HERE / 'HANDOFF_AUDIT.json', handoff)
    print(json.dumps(handoff, indent=2))


if __name__ == '__main__':
    main()
