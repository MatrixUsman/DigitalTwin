"""Check a fresh extraction, synthetic fixtures and saved tables without experiments."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import traceback
import zipfile


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--science-python', type=Path, required=True)
    args = parser.parse_args()
    archive, output = args.archive.resolve(), args.output.resolve()
    interpreter = args.science_python.absolute()
    if not interpreter.is_file():
        parser.error('An existing isolated NumPy interpreter is required.')
    output.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'running',
               'archive': str(archive), 'archive_sha256': sha(archive),
               'scope': 'Clean extraction, identities, synthetic fixtures and saved-result arithmetic only',
               'raw_dataset_access': False, 'physics_or_training_rerun': False,
               'new_environment_installation': False, 'commands': [], 'seals': {}}
    try:
        with zipfile.ZipFile(archive) as z:
            names = z.namelist()
            if len(names) != len(set(names)):
                raise ValueError('Duplicate archive members')
            for item in z.infolist():
                p = PurePosixPath(item.filename)
                if p.is_absolute() or '..' in p.parts or '\\' in item.filename or p.parts[0] != 'manufacturing':
                    raise ValueError('Unsafe archive member')
                if (item.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('Symlinks are not admitted')
            if sum(i.file_size for i in z.infolist()) > 350 * 1048576:
                raise ValueError('Extraction exceeds the declared disk input cap')
            if z.testzip() is not None:
                raise ValueError('Archive CRC failed')
            z.extractall(output / 'extracted')
            receipt['archive_members'] = len(names)
        root = output / 'extracted/manufacturing'
        receipt['extracted_root'] = str(root)
        seals = [
            ('research_cycles/review_extension_v0.18/FREEZE.json', 'sha256', root),
            ('research_cycles/review_extension_v0.18/PACKAGE_MANIFEST.json', 'sha256', root / 'research_cycles/review_extension_v0.18'),
            ('research_cycles/context_recovery_v0.19/FINAL_FREEZE.json', 'bindings', root),
            ('research_cycles/context_recovery_v0.19/PACKAGE_MANIFEST.json', 'sha256', root),
            ('manuscript_arx_rbf_v1.7/PACKAGE_MANIFEST.json', 'sha256', root),
        ]
        for relative, key, base in seals:
            bindings = json.loads((root / relative).read_text())[key]
            for name, expected in bindings.items():
                if sha(base / name) != expected:
                    raise ValueError('Extracted seal mismatch: ' + name)
            receipt['seals'][relative] = len(bindings)
        env = dict(os.environ)
        env.pop('PYTHONPATH', None)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        commands = [
            ('package', [sys.executable, '-I', 'reproducibility_v1.7/test_package.py', '--verify-root', '.']),
            ('tables', [sys.executable, '-I', 'reproducibility_v1.7/replay_tables.py', '--output', 'reviewer_tables']),
            ('synthetic_v018', [str(interpreter), '-m', 'unittest', 'discover', '-s', 'research_cycles/review_extension_v0.18', '-p', 'test_*.py', '-v']),
            ('synthetic_v019', [str(interpreter), '-m', 'unittest', 'discover', '-s', 'research_cycles/context_recovery_v0.19', '-p', 'test_*.py', '-v']),
        ]
        for name, command in commands:
            result = subprocess.run(command, cwd=root, env=env, text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, timeout=60)
            log = output / (name + '.log')
            log.write_text(result.stdout)
            item = {'name': name, 'command': command, 'cwd': str(root), 'returncode': result.returncode,
                    'log': log.name, 'log_sha256': sha(log)}
            count = re.search(r'Ran (\d+) tests?', result.stdout)
            if count:
                item['synthetic_tests'] = int(count.group(1))
            receipt['commands'].append(item)
            if result.returncode:
                raise RuntimeError('Extraction validation failed; inspect ' + log.name)
        replay = json.loads((root / 'reviewer_tables/REPLAY_RECEIPT.json').read_text())
        if not replay['complete_requested_studies'] or replay['status'] != 'passed':
            raise ValueError('Incomplete saved-table replay')
        receipt['table_checks'] = replay['checks']
        receipt['table_receipt_sha256'] = sha(root / 'reviewer_tables/REPLAY_RECEIPT.json')
        receipt['allowlisted_files'] = len(json.loads((root / 'reproducibility_v1.7/ALLOWLIST.json').read_text())['files'])
        receipt['status'] = 'passed'
    except BaseException:
        receipt['status'] = 'failed'
        receipt['failure'] = traceback.format_exc()
        raise
    finally:
        receipt['wall_seconds'] = time.monotonic() - start
        (output / 'CLEAN_EXTRACTION_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
