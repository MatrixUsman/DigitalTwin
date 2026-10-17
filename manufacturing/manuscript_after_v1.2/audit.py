"""Verify a prose-only revision against its preserved, evidence-audited base."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import difflib
import hashlib
import json
import re
import subprocess
from pypdf import PdfReader

M = Path(__file__).resolve().parent
P = M.parent
S = P / 'manuscript_after_v1.1'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
checks = []


def require(ok, name):
    if not ok:
        raise AssertionError(name)
    checks.append(name)


base = json.loads((M / 'BASE_IDENTITY.json').read_text())
for name, digest in base['source_sha256'].items():
    require(sha(S / name) == digest, 'unchanged base ' + name)
old_package = json.loads((S / 'PACKAGE_MANIFEST.json').read_text())
for name, digest in old_package['sha256'].items():
    require(sha(P / name) == digest, 'preserved package ' + name)
require(sha(P / 'output/pdf/AFTER-Muhammad-Usman.pdf') == base['original_pdf_sha256'],
        'original PDF preserved')
old_audit = json.loads((S / 'AUDIT.json').read_text())
require(old_audit['status'] == 'passed' and old_audit['checks'] == 2461, 'base evidence audit')

patches = []
changes = []
numbers = lambda t: Counter(re.findall(r'\d+(?:[.,]\d+)*', t))
for name in ['main.tex', 'sections/return_bound.tex', 'sections/imu_reference.tex']:
    a, b = (S / name).read_text(), (M / name).read_text()
    require(numbers(a) == numbers(b), name + ' numerical-token multiset unchanged')
    require(re.findall(r'\$[^$]*\$', a, re.S) == re.findall(r'\$[^$]*\$', b, re.S),
            name + ' every inline mathematical expression unchanged')
    for env in ['equation', 'align', 'align*', 'proposition', 'proof', 'table', 'figure', 'thebibliography']:
        pattern = r'\\begin\{'+re.escape(env)+r'\}.*?\\end\{'+re.escape(env)+r'\}'
        require(re.findall(pattern, a, re.S) == re.findall(pattern, b, re.S), name + ' ' + env)
    for command in ['cite', 'ref', 'label', 'input', 'includegraphics', 'url']:
        pattern = r'\\'+command+r'(?:\[[^\]]*\])?\{[^}]+\}'
        require(re.findall(pattern, a) == re.findall(pattern, b), name + ' ' + command)
    aa, bb = a.splitlines(), b.splitlines()
    require(len(aa) == len(bb), name + ' local paragraph substitutions only')
    for line, (before, after) in enumerate(zip(aa, bb), 1):
        if before != after:
            require(numbers(before) == numbers(after), name + ':' + str(line) + ' paragraph numbers')
            changes.append(dict(file=name, line=line,
                                before_sha256=hashlib.sha256(before.encode()).hexdigest(),
                                after_sha256=hashlib.sha256(after.encode()).hexdigest(),
                                before=before, after=after))
    patches.extend(difflib.unified_diff(a.splitlines(True), b.splitlines(True),
                                      fromfile='manuscript_after_v1.1/'+name,
                                      tofile='manuscript_after_v1.2/'+name))

for directory in ['generated', 'figures']:
    for f in (S / directory).iterdir():
        if f.is_file():
            require(sha(f) == sha(M / directory / f.name), 'unchanged asset ' + directory + '/' + f.name)
require(sha(S / 'references.bib') == sha(M / 'references.bib'), 'bibliography file unchanged')
a, b = (S / 'main.tex').read_text(), (M / 'main.tex').read_text()
for command in ['title', 'author']:
    pattern = r'\\'+command+r'\{[^}]+\}'
    require(re.findall(pattern, a) == re.findall(pattern, b), command + ' unchanged')
require(a.split('\\section*{Data and code availability}', 1)[1] ==
        b.split('\\section*{Data and code availability}', 1)[1], 'availability, declarations and references unchanged')

receipt = json.loads((M / 'BUILD_RECEIPT.json').read_text())
pdf = P / receipt['pdf']
require(receipt['offline'] and receipt['returncode'] == 0, 'successful offline build')
require(sha(pdf) == receipt['pdf_sha256'], 'compiled PDF identity')
for name, digest in receipt['source_sha256'].items():
    require(sha(M / name) == digest, 'compiled input ' + name)
reader = PdfReader(pdf)
require(len(reader.pages) == 20, 'twenty pages')
require(reader.metadata.author == 'Muhammad Usman', 'sole author metadata')
txt = subprocess.check_output(['pdftotext', str(pdf), '-'], text=True)
require('�' not in txt and '??' not in txt, 'no missing glyph or unresolved-reference markers')
require('Muhammad Usman' in txt and 'Haiqa' not in txt, 'requested byline')
log = (P / receipt['attempt'] / 'main.log').read_text()
require(not re.search('Overfull|Underfull|undefined|Missing character', log), 'clean compiler log')
renders = sorted((P / 'local/manuscript_after_v1.2/qa').glob('page-*.png'))
require(len(renders) == 20, 'complete final rendering')

(M / 'REVISION.diff').write_text(''.join(patches))
(M / 'PARAGRAPH_CHANGES.json').write_text(json.dumps(changes, indent=2)+'\n')
result = dict(utc=datetime.now(timezone.utc).isoformat(), status='passed', checks=len(checks),
              changed_paragraphs=len(changes), prior_package_files=len(old_package['sha256']),
              prior_audit_sha256=sha(S / 'AUDIT.json'), pdf_pages=20, pdf_sha256=sha(pdf),
              source_sha256={name: sha(M / name) for name in
                             ['main.tex', 'sections/return_bound.tex', 'sections/imu_reference.tex']},
              rendered_page_sha256={str(p.relative_to(P)): sha(p) for p in renders},
              scope='Prose revision integrity and rendering, with saved per-paragraph changes',
              limitations='Numerical and structural checks do not prove semantic equivalence; prose reviewed by the same assistant, not an independent peer reviewer. No AI detector was used and no detector score is claimed.',
              abstract='Edited for clarity within the explicit whole-manuscript request; numerical claims preserved.',
              check_names=checks)
(M / 'AUDIT.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ['status', 'checks', 'changed_paragraphs', 'pdf_pages', 'pdf_sha256']}))
