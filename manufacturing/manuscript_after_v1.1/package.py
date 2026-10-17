"""Seal this editorial revision and a source-only, independently editable ZIP."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import zipfile

M = Path(__file__).resolve().parent
P = M.parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = M / 'PACKAGE_MANIFEST.json'
archive = P / 'output/AFTER-Muhammad-Usman-source.zip'
if manifest.exists() or archive.exists():
    raise SystemExit('This revision is already packaged; preserve it and version changes separately.')

audit = json.loads((M / 'AUDIT.json').read_text())
qa = json.loads((M / 'VISUAL_QA.json').read_text())
pdf = P / 'output/pdf/AFTER-Muhammad-Usman.pdf'
assert audit['status'] == qa['status'] == 'passed'
assert audit['pdf_sha256'] == qa['pdf_sha256'] == sha(pdf)
assert audit['audit_source_sha256'] == sha(M / 'audit.py')
assert qa['reviewed_pages'] == list(range(1, 21))

source = sorted([M / 'main.tex', M / 'references.bib'] +
                list((M / 'sections').glob('*.tex')) +
                list((M / 'generated').glob('*.tex')) +
                list((M / 'figures').glob('*.pdf')))
assert len(source) == 15
readme = '''# AFTER: editable manuscript source

Author: Muhammad Usman
Revision: 1.1, 17 October 2026
Format: neutral journal article, 20-page compiled version.

Open main.tex and compile with XeLaTeX (multiple passes) or Tectonic.
The bibliography is embedded in main.tex, so BibTeX is not needed.
references.bib provides matching entries for later journal-template conversion.
Keep sections/, generated/ and figures/ beside main.tex.

All tables and vector figures are already included. Compilation does not
require Python, datasets, models, experiments or external result storage.
The original PDF was compiled offline with Tectonic 0.17.0. Standard TeX
packages and Latin Modern fonts must be present in the chosen TeX environment.

The article reports saved synthetic attack/recovery simulations, clean
commissioning results, a synthetic residual-bound diagnostic and a separate
normal IMU prediction study. It does not establish a novel detector superior
to CASPER. Figures are Python/Matplotlib plots of saved artifacts.

This is a typesetting source package, not the complete experimental archive.
No raw datasets, trained models, restricted code or third-party papers are
included. No manuscript has been submitted or published. Review the claims,
authorship, affiliation and declarations before submission and adapt the
format and AI-assistance disclosure to the chosen journal's requirements.
'''
payload = {'AFTER-source/' + str(p.relative_to(M)): p.read_bytes() for p in source}
payload['AFTER-source/README.md'] = readme.encode()
archive.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as z:
    for name, contents in sorted(payload.items()):
        info = zipfile.ZipInfo(name, date_time=(2026, 10, 17, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        z.writestr(info, contents)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert set(z.namelist()) == set(payload)
    assert all(z.read(name) == data for name, data in payload.items())

receipt = dict(utc=datetime.now(timezone.utc).isoformat(), status='passed',
               archive=str(archive.relative_to(P)), archive_sha256=sha(archive),
               bytes=archive.stat().st_size, entries=len(payload),
               entry_sha256={k: hashlib.sha256(v).hexdigest() for k, v in sorted(payload.items())},
               source_sha256={str(p.relative_to(M)): sha(p) for p in source},
               scope='Typesetting sources only; no raw data, fitted model or third-party manuscript',
               validation='ZIP CRC and byte parity; compiled TeX/PDF inputs match the checked source')
(M / 'SOURCE_ARCHIVE.json').write_text(json.dumps(receipt, indent=2)+'\n')

# Preserve snapshots of mutable handoffs; never bind later sessions to live status files.
handoff = P / 'local/manuscript_after_v1.1/handoff'
handoff.mkdir(parents=True, exist_ok=True)
snapshots = []
for name in ['AGENTS.md', 'STATUS.md', 'docs/WORK_LOG.md']:
    dest = handoff / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise SystemExit('Handoff snapshot already exists: ' + str(dest))
    shutil.copyfile(P / name, dest)
    snapshots.append(dest)

files = sorted(p for p in M.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
files += [pdf, archive] + snapshots
sealed = dict(utc=datetime.now(timezone.utc).isoformat(),
              scope='Manuscript revision 1.1, rendered QA, evidence audit, source ZIP and archived handoffs',
              final_pdf=str(pdf.relative_to(P)), source_archive=str(archive.relative_to(P)),
              fresh_experiments=False, published=False,
              sha256={str(p.relative_to(P)): sha(p) for p in files},
              prior_package_manifests={k: v['manifest_sha256'] for k, v in audit['prior_packages'].items()})
manifest.write_text(json.dumps(sealed, indent=2)+'\n')
assert all(sha(P / name) == value for name, value in sealed['sha256'].items())
print(json.dumps(dict(status='passed', package_files=len(files), source_entries=len(payload),
                      archive_bytes=archive.stat().st_size, archive_sha256=sha(archive),
                      pdf_sha256=sha(pdf))))
