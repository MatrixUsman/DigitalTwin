"""Local reviewer packaging. Snapshot first; build only after final seals are confirmed."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import argparse, hashlib, json, shutil, zipfile

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
SUFFIXES = {'.py', '.json', '.md', '.txt', '.tex', '.bib', '.pdf', '.toml'}
LOCAL_ROOTS = (
    'local/attack_audit_v0.14/runs/audit_001/',
    'local/residual_twin_v0.13/runs/pilot_001/',
    'local/context_recovery_v0.19/',
)
EXCLUDE_PARTS = {'datasets', 'vendor', '.git', '__pycache__', '.aws', '.codex', '.agents'}

def digest(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()

def safe_path(name, root=PROJECT):
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name or not p.parts:
        raise ValueError('Unsafe relative path: ' + name)
    if any(x in EXCLUDE_PARTS or x.startswith('.venv') for x in p.parts):
        raise ValueError('Excluded material: ' + name)
    if p.parts[0] == 'local' and not name.startswith(LOCAL_ROOTS):
        raise ValueError('Non-allowlisted local material: ' + name)
    q = root / name
    for parent in [q, *q.parents]:
        if parent == root.parent:
            break
        if parent.is_symlink():
            raise ValueError('Symlink excluded: ' + name)
    if not q.resolve().is_relative_to(root.resolve()):
        raise ValueError('Escaping project: ' + name)
    return q

def candidates():
    """Resolve a finite policy to an explicit file list; never follow dataset paths."""
    found = {}
    def add(q, role):
        if not q.is_file() or q.is_symlink():
            return
        name = q.relative_to(PROJECT).as_posix()
        safe_path(name)
        found[name] = role
    # Our source and public-safe study descriptions/results; no recursive run sweep.
    for cycle in (PROJECT / 'research_cycles').iterdir():
        if not cycle.is_dir():
            continue
        for q in cycle.iterdir():
            if q.suffix in SUFFIXES or q.name == '.gitignore':
                add(q, 'research_source_or_report')
    for q in (PROJECT / 'src/mfg_twin').rglob('*.py'):
        if '__pycache__' not in q.parts:
            add(q, 'research_source')
    for name in ['pyproject.toml', 'docs/literature/RECOVERY_IMPROVEMENT_PRIOR_ART_2026-10-19.md', 'docs/REVISION_OUTCOME_V1.7.md']:
        add(PROJECT / name, 'study_context')
    # Exact v0.18 freeze dependencies are synthetic simulation artifacts only.
    f = json.loads((PROJECT / 'research_cycles/review_extension_v0.18/FREEZE.json').read_text())
    for name in f['sha256']:
        add(safe_path(name), 'v018_exact_replay_input')
    # Only synthetic normal commissioning/model artifacts. No raw real observations.
    normal = PROJECT / 'local/residual_twin_v0.13/runs/pilot_001'
    for pattern in ['normal_*.npz', 'base_*.npz', 'fit_*.npz', 'selection.json', 'provenance.json', 'supervisor.json', 'outcome.json']:
        for q in normal.glob(pattern):
            add(q, 'synthetic_commissioning_or_fitted_model')
    for q in (PROJECT / 'research_cycles/review_extension_v0.18/runs').rglob('*'):
        if q.is_file() and q.suffix in {'.json', '.npz', '.log'}:
            add(q, 'v018_saved_attempt')
    for q in (PROJECT / 'local/context_recovery_v0.19').rglob('*'):
        if q.is_file() and q.suffix in {'.json', '.npz', '.log'}:
            add(q, 'v019_synthetic_saved_attempt')
    # Actual v0.19 frozen dependency maps close historical imports/configuration.
    for freeze in (PROJECT / 'research_cycles/context_recovery_v0.19').glob('*FREEZE.json'):
        for name in json.loads(freeze.read_text()).get('bindings', {}):
            add(safe_path(name), 'v019_frozen_input')
    for q in (PROJECT / 'manuscript_arx_rbf_v1.7').rglob('*'):
        if q.is_file() and q.suffix in SUFFIXES:
            add(q, 'working_manuscript')
    add(PROJECT / 'output/pdf/ARX-RBF-Muhammad-Usman-v1.7.pdf', 'working_pdf')
    add(PROJECT / 'output/ARX-RBF-Muhammad-Usman-v1.7-latex.zip', 'editable_manuscript_archive')
    for q in HERE.iterdir():
        if q.suffix in {'.py', '.md', '.txt'}:
            add(q, 'reviewer_tools')
    return found

def snapshot():
    roles = candidates()
    records = [{'path': n, 'bytes': safe_path(n).stat().st_size,
                'sha256': digest(safe_path(n)), 'role': roles[n]} for n in sorted(roles)]
    return {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
            'scope': 'Local reviewer bundle; no public release or redistribution approval inferred',
            'project_prefix': 'manufacturing', 'files': records,
            'total_bytes': sum(r['bytes'] for r in records),
            'exclusions': ['All raw/processed CASPER and voraus-AD observations',
                           'Prepared real-IMU arrays and real-data checkpoints',
                           'Third-party vendor checkouts, packages, papers and compiler binaries',
                           'Credentials, approval records and unrelated local folders'],
            'limitations': ['Historical real-IMU numerical executions require separately authorized source data and pinned upstream code.',
                            'Old study reports are included; their entire historical input closure is not promised.',
                            'v0.18 and v0.19 synthetic input closures are included and checked.']}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['inventory', 'build'])
    p.add_argument('--refresh', action='store_true')
    p.add_argument('--confirmed-final-seals', action='store_true')
    p.add_argument('--max-total-mib', type=float, default=350)
    args = p.parse_args()
    allow = HERE / 'ALLOWLIST.json'
    if args.action == 'inventory':
        if allow.exists() and not args.refresh:
            p.error('Inventory exists; use --refresh to preserve it and create an updated snapshot.')
        if allow.exists():
            history = HERE / 'inventory_history'
            history.mkdir(exist_ok=True)
            shutil.copyfile(allow, history / (digest(allow) + '.json'))
        data = snapshot()
        allow.write_text(json.dumps(data, indent=2) + '\n')
        summary = {'files': len(data['files']), 'bytes': data['total_bytes'],
                   'mib': data['total_bytes'] / 1048576, 'allowlist_sha256': digest(allow),
                   'archive_created': False}
        (HERE / 'INVENTORY.json').write_text(json.dumps(summary, indent=2) + '\n')
        print(json.dumps(summary, indent=2))
        return
    if not args.confirmed_final_seals:
        p.error('Final archive intentionally blocked until root confirms seals/paths; then pass --confirmed-final-seals.')
    data = json.loads(allow.read_text())
    if data['total_bytes'] > args.max_total_mib * 1048576:
        p.error('Archive inputs exceed the approved total-byte cap; obtain a concrete budget decision.')
    required = ['research_cycles/context_recovery_v0.19/FINAL_FREEZE.json',
                'local/context_recovery_v0.19/final_001/results.json',
                'manuscript_arx_rbf_v1.7/PACKAGE_MANIFEST.json']
    names = {r['path'] for r in data['files']}
    if not set(required) <= names:
        p.error('Missing completed final study/manuscript seal in inventory: ' + str(set(required) - names))
    for record in data['files']:
        q = safe_path(record['path'])
        if q.stat().st_size != record['bytes'] or digest(q) != record['sha256']:
            raise ValueError('Changed after inventory: ' + record['path'])
    archive = HERE / 'manufacturing-reviewer-v1.7.zip'
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for record in data['files']:
            z.write(safe_path(record['path']), 'manufacturing/' + record['path'])
        z.writestr('manufacturing/reproducibility_v1.7/ALLOWLIST.json', json.dumps(data, indent=2) + '\n')
    receipt = {'created_utc': datetime.now(timezone.utc).isoformat(), 'archive': archive.name,
               'sha256': digest(archive), 'bytes': archive.stat().st_size,
               'files': len(data['files']) + 1, 'input_bytes': data['total_bytes'],
               'public_release': False, 'clean_unpack_test': 'pending'}
    (HERE / 'BUILD_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
