"""Create the editable revision archive and seal the editorial files."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import zipfile

M = Path(__file__).resolve().parent
P = M.parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
archive = P / 'output/AFTER-Muhammad-Usman-revised-source.zip'
manifest = M / 'PACKAGE_MANIFEST.json'
if archive.exists() or manifest.exists():
    raise SystemExit('Revision already packaged; preserve it and create a new version for later edits.')
audit = json.loads((M / 'AUDIT.json').read_text())
qa = json.loads((M / 'VISUAL_QA.json').read_text())
pdf = P / 'output/pdf/AFTER-Muhammad-Usman-revised.pdf'
assert audit['status'] == qa['status'] == 'passed'
assert audit['pdf_sha256'] == qa['pdf_sha256'] == sha(pdf)
assert qa['reviewed_pages'] == list(range(1, 21))

source = sorted([M/'main.tex', M/'references.bib'] +
                list((M/'sections').glob('*.tex')) +
                list((M/'generated').glob('*.tex')) + list((M/'figures').glob('*.pdf')))
assert len(source) == 15
payload = {'AFTER-revised-source/'+str(p.relative_to(M)): p.read_bytes() for p in source}
payload['AFTER-revised-source/README.md'] = b'''# AFTER: editable revision 1.2

Author: Muhammad Usman. Date: 17 October 2026.
Compile main.tex with XeLaTeX (multiple passes) or Tectonic.
Keep sections/, generated/ and figures/ beside main.tex.
The bibliography is embedded; BibTeX is not required. references.bib contains
matching records for later journal-template conversion.

This 20-page edition revises prose for clarity. Numerical findings, equations,
proofs, figures, tables, citations and declarations are preserved. No AI-detector
result is claimed. The truthful AI-assistance disclosure remains in the paper.

The verified build used offline Tectonic 0.17.0 with standard TeX packages and
Latin Modern fonts already installed. Python and datasets are not needed to
typeset the article. This archive contains no raw data or fitted model.

This is a manuscript source package, not the complete experiment archive.
Review the article, authorship and declarations before submission, then check
the chosen journal's scope and requirements. No submission or publication has
been performed. Detector classifications and journal acceptance are not assured.
'''
with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as z:
    for name, data in sorted(payload.items()):
        info = zipfile.ZipInfo(name, date_time=(2026, 10, 17, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        z.writestr(info, data)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist()) == set(payload)
    assert all(z.read(k) == v for k, v in payload.items())
receipt = dict(utc=datetime.now(timezone.utc).isoformat(), status='passed',
               archive=str(archive.relative_to(P)), archive_sha256=sha(archive),
               bytes=archive.stat().st_size, entries=len(payload),
               entry_sha256={k: hashlib.sha256(v).hexdigest() for k, v in payload.items()},
               scope='Editable typesetting files; no raw data, models, third-party manuscripts or detector tricks')
(M/'SOURCE_ARCHIVE.json').write_text(json.dumps(receipt, indent=2)+'\n')

handoff = P/'local/manuscript_after_v1.2/handoff'
snapshots = []
for name in ['AGENTS.md', 'STATUS.md', 'docs/WORK_LOG.md']:
    dest = handoff/name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise SystemExit('Handoff snapshot already exists: '+str(dest))
    shutil.copyfile(P/name, dest)
    snapshots.append(dest)
files = sorted(p for p in M.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
files += [pdf, archive] + snapshots
record = dict(utc=datetime.now(timezone.utc).isoformat(),
              scope='Prose revision, preservation audit, rendered QA, source archive and handoff snapshots',
              sha256={str(p.relative_to(P)): sha(p) for p in files},
              prior_package_sha256=sha(P/'manuscript_after_v1.1/PACKAGE_MANIFEST.json'),
              fresh_experiments=False, detector_upload=False, detector_score=None, published=False)
manifest.write_text(json.dumps(record, indent=2)+'\n')
assert all(sha(P/k) == v for k, v in record['sha256'].items())
print(json.dumps(dict(status='passed', package_files=len(files), archive_entries=len(payload),
                      archive_bytes=archive.stat().st_size, archive_sha256=sha(archive))))
