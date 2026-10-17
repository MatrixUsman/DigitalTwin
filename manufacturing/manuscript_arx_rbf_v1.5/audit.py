"""Bounded editorial checks against the preserved v1.4 source package."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re
from pypdf import PdfReader

M = Path(__file__).resolve().parent
P = M.parent
B = P / 'manuscript_after_v1.4'
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
checks = []
def check(label, condition):
    checks.append({'check': label, 'passed': bool(condition)})

base = json.loads((B / 'PACKAGE_MANIFEST.json').read_text())
identity = json.loads((M / 'BASE_IDENTITY.json').read_text())
check('base manifest preserved', sha(B/'PACKAGE_MANIFEST.json') == identity['base_manifest_sha256'])
for k, v in base['sha256'].items():
    check('base binding: ' + k, sha(P/k) == v)
for k, v in identity['unchanged_scientific_files'].items():
    check('unchanged source: ' + k, sha(M/k) == v and sha(B/k) == v)
old_title = 'AFTER: Digital Twins for Cyberattack and Recovery Monitoring in Industrial Robots'
new_title = 'ARX--RBF Motion Modeling for Cyberattack Detection and Recovery Monitoring in Industrial Robots'
expected = (B/'main.tex').read_text().replace(old_title, new_title).replace(
    'AFTER names the investigation; the present evidence does not validate a new state-of-the-art detector.',
    'The present evidence does not validate a new state-of-the-art detector.')
check('only authorized main-text replacements', (M/'main.tex').read_text() == expected)
receipt = json.loads((M/'MAIN_BUILD_RECEIPT.json').read_text())
for k, v in receipt['source_sha256'].items():
    check('compiled source preserved: ' + k, sha(M/k) == v)
pdf = P / receipt['pdf']
check('PDF matches build receipt', sha(pdf) == receipt['pdf_sha256'])
reader = PdfReader(pdf)
check('15 pages including appendices and references', len(reader.pages) == 15)
check('PDF title metadata', reader.metadata.title == identity['title'])
check('sole requested author metadata', reader.metadata.author == 'Muhammad Usman')
text = ' '.join(reader.pages[0].extract_text().split())
check('visible selected title', text.startswith(identity['title']))
check('visible requested byline', 'Muhammad Usman' in text)
log = (P/receipt['attempt']/'main.log').read_text()
for pattern in ['Overfull', 'undefined', 'Missing character', '! LaTeX Error']:
    check('no build issue: ' + pattern, pattern not in log)
check('20 bibliography entries preserved', len(re.findall(r'\\bibitem\{', (M/'references.tex').read_text())) == 20)
render = json.loads((P/'local/manuscript_arx_rbf_v1.5/RENDER_COMPARISON.json').read_text())
check('only pages 1 and 2 changed in render', render['changed_pages'] == [1, 2])
result = {'utc': datetime.now(timezone.utc).isoformat(), 'scope': 'Title-only local editorial verification, not new scientific validation',
          'passed': all(c['passed'] for c in checks), 'checks': len(checks), 'pages': len(reader.pages),
          'pdf_sha256': sha(pdf), 'underfull_diagnostics': log.count('Underfull'), 'details': checks}
(M/'AUDIT.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['passed','checks','pages','pdf_sha256','underfull_diagnostics']}))
if not result['passed']:
    raise SystemExit([c for c in checks if not c['passed']])
