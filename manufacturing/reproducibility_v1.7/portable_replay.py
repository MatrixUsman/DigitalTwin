"""Provenance-only adapter for running sealed workers outside a Git checkout.

Scientific sources and freezes remain unchanged. Exact substitutions and hashes are
saved per attempt. This is a labelled adapted execution, not byte-identical worker code.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, importlib.metadata, json, sys, types

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def adapt(text, version):
    edits = [("subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True)",
              "json.dumps({'numpy':__import__('importlib.metadata',fromlist=['version']).version('numpy')})")]
    if version == 18:
        edits += [("subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip()", 'None'),
                  ("subprocess.check_output(['git','status','--short'],cwd=PROJECT,text=True)", 'None')]
    else:
        edits += [("subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()", 'None'),
                  ("subprocess.check_output(['git','status','--short'],text=True)", 'None')]
    for old, new in edits:
        if text.count(old) != 1:
            raise ValueError('Unexpected worker provenance; do not guess a patch: ' + old)
        text = text.replace(old, new)
    return text, [{'old': a, 'new': b} for a, b in edits]

def adapt_compact_loader(text):
    """Bind the already provenance-adapted worker; retain compact writer/science."""
    old = "spec=importlib.util.spec_from_file_location('context_worker19',LocalPath(__file__).with_name('worker.py'))\nworker=importlib.util.module_from_spec(spec);spec.loader.exec_module(worker)"
    if text.count(old) != 1:
        raise ValueError('Unexpected compact worker loader; do not guess a patch')
    new = '# worker is provided as the provenance-adapted original module by portable_replay.py'
    return text.replace(old, new), {'old': old, 'new': new}

def selected_wrapper(cycle, version, phase):
    if version == 19 and phase == 'final':
        freeze = json.loads((cycle / 'FINAL_FREEZE.json').read_text())
        if freeze.get('worker') != 'worker_compact.py':
            raise ValueError('Unsupported final worker; no silent storage-policy change')
        return cycle / freeze['worker']
    return None

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study', type=int, choices=[18, 19], required=True)
    p.add_argument('--phase', choices=['development', 'pilot', 'final'], default='final')
    p.add_argument('--output', type=Path, required=True, help='Fresh output directory')
    p.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    a = p.parse_args()
    cycle = ROOT / 'research_cycles' / ('review_extension_v0.18' if a.study == 18 else 'context_recovery_v0.19')
    source = cycle / 'worker.py'
    original = source.read_text(); adapted, edits = adapt(original, a.study)
    wrapper = selected_wrapper(cycle, a.study, a.phase)
    compact_text, compact_edit = adapt_compact_loader(wrapper.read_text()) if wrapper else (None, None)
    output = a.output.resolve()
    if a.worker:
        sys.path.insert(0, str(cycle))
        if wrapper:
            worker = types.ModuleType('portable_context_worker19'); worker.__file__ = str(source)
            exec(compile(adapted, str(source), 'exec'), worker.__dict__)
            sys.argv = [str(wrapper), str(output)]
            exec(compile(compact_text, str(wrapper), 'exec'),
                 {'__name__': '__main__', '__file__': str(wrapper), 'worker': worker})
        else:
            sys.argv = [str(source), '--output', str(output)] if a.study == 18 else [str(source), a.phase, str(output)]
            exec(compile(adapted, str(source), 'exec'), {'__name__': '__main__', '__file__': str(source)})
        return
    output.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(ROOT / 'src'))
    from mfg_twin.supervisor import Limits, BudgetWriter, supervise
    config = json.loads((cycle / 'config.json').read_text())
    limit_dict = config['limits'] if a.study == 18 else config['limits'][a.phase]
    limits = Limits(**limit_dict)
    writer = BudgetWriter(output, limit_bytes=limits.output_bytes)
    writer.write_json('PORTABLE_ADAPTATION.json', {
        'utc': datetime.now(timezone.utc).isoformat(), 'study': a.study, 'phase': a.phase,
        'scope': 'Provenance-only adapted execution; scientific source and original freezes preserved',
        'original_worker_sha256': sha(source),
        'effective_worker_sha256': hashlib.sha256(adapted.encode()).hexdigest(),
        'adapter_sha256': sha(__file__), 'substitutions': edits,
        'final_storage_wrapper': None if wrapper is None else {
            'original_sha256': sha(wrapper), 'effective_sha256': hashlib.sha256(compact_text.encode()).hexdigest(),
            'loader_substitution': compact_edit, 'reference_role_indices': [0, 2, 3],
            'scientific_and_storage_logic': 'unchanged; only dependency binding targets the provenance-adapted worker'},
        'git_revision_meaning': 'null: extracted directory has no claimed Git identity; archived original receipts retain original identity',
        'dependencies_meaning': 'actual imported NumPy version, rather than unrelated full pip environment',
        'raw_dataset_access': False,
    })
    cmd = [sys.executable, str(Path(__file__).resolve()), '--worker', '--study', str(a.study),
           '--phase', a.phase, '--output', str(output)]
    result = supervise(cmd, cwd=ROOT, output_dir=output, limits=limits,
                       env={k:'1' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                                           'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONDONTWRITEBYTECODE']})
    writer.write_json('portable_supervisor.json', result)
    print(json.dumps(result, indent=2))
    if result['status'] != 'completed':
        raise SystemExit(1)

if __name__ == '__main__':
    main()
