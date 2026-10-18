"""Revision integrity, scientific artifact bindings, table arithmetic and PDF checks."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re
from pypdf import PdfReader

M = Path(__file__).resolve().parent
P = M.parent
B = P/'manuscript_arx_rbf_v1.5'
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
checks = []
def check(name, condition):
    checks.append({'check': name, 'passed': bool(condition)})

identity = json.loads((M/'BASE_IDENTITY.json').read_text())
check('preserved base-manifest identity', sha(B/'PACKAGE_MANIFEST.json') == identity['base_manifest_sha256'])
for manifest in [B/'PACKAGE_MANIFEST.json', P/'research_cycles/fivefold_v0.16/PACKAGE_MANIFEST.json',
                 P/'research_cycles/forecast_baselines_v0.17/PACKAGE_MANIFEST.json']:
    d = json.loads(manifest.read_text())
    for k, v in d['sha256'].items():
        check(str(manifest.relative_to(P))+': '+k, (P/k).is_file() and sha(P/k) == v)
for folder in ['figures','generated']:
    for p in (B/folder).iterdir():
        if p.is_file():
            check('preserved prior scientific asset '+str(p.relative_to(B)), sha(M/p.relative_to(B)) == sha(p))
for f in ['sections/methods.tex','sections/metrics.tex','sections/uncertainty.tex','sections/earlier_results.tex','references.bib']:
    check('preserved prior source '+f, sha(M/f) == sha(B/f))
cv = json.loads((P/'research_cycles/fivefold_v0.16/VERIFICATION.json').read_text())
check('five-fold verification passed', cv['passed'] and cv['checks'] == 109 and len(cv['folds']) == 5)
for r in cv['folds']:
    row = f'{r["fold"]} & {r["targets"]} & {r["arx_rmse"]:.6f} & {r["arx_rbf_rmse"]:.6f}'
    check('five-fold table row '+str(r['fold']), row in (M/'generated/fivefold.tex').read_text())
fr = json.loads((P/'research_cycles/forecast_baselines_v0.17/VERIFICATION.json').read_text())
check('complete verified forecast study', fr['passed'] and fr['outcomes'] == 9 and fr['failures'] == 0)
asset = json.loads((M/'FORECAST_ASSET_RECEIPT.json').read_text())
check('forecast generation source bound', asset['verification_sha256'] == sha(P/'research_cycles/forecast_baselines_v0.17/VERIFICATION.json'))
check('forecast table bound', asset['table_sha256'] == sha(M/'generated/forecast.tex'))
for r in fr['rows']:
    row = f'{r["method"]} & {r["seed"]} & {r["epochs"]}/{r["selected_epoch"]} & {r["standardized_mse"]:.6f} & {r["cpu_seconds"]:.1f}'
    check('forecast table row '+r['method']+str(r['seed']), row in (M/'generated/forecast.tex').read_text())
receipt = json.loads((M/'MAIN_BUILD_RECEIPT.json').read_text())
for k,v in receipt['source_sha256'].items():
    check('compiled source '+k, sha(M/k) == v)
pdf = P/receipt['pdf']; reader = PdfReader(pdf)
check('PDF hash', sha(pdf) == receipt['pdf_sha256'])
check('at most 15 pages', len(reader.pages) <= 15)
title = 'ARX–RBF Motion Modeling for Cyberattack Detection and Recovery Monitoring in Industrial Robots'
check('selected title metadata', reader.metadata.title == title)
check('sole requested author metadata', reader.metadata.author == 'Muhammad Usman')
check('requested visible byline', 'Muhammad Usman' in reader.pages[0].extract_text())
log = (P/receipt['attempt']/'main.log').read_text()
for pattern in ['Overfull','undefined','Missing character','! LaTeX Error']:
    check('no build issue '+pattern, pattern not in log)
text = (M/'main.tex').read_text()+'\n'+'\n'.join(p.read_text() for p in (M/'sections').glob('*.tex'))
keys = set()
for group in re.findall(r'\\cite\{([^}]+)\}',text):
    keys.update(group.split(','))
refs = set(re.findall(r'\\bibitem\{([^}]+)\}',(M/'references.tex').read_text()))
check('20 references and complete citation match', keys == refs and len(refs) == 20)
index = json.loads((M/'REFERENCE_INDEX.json').read_text())
check('bibliography recency count preserved', index['recent_cited_versions'] == 18 and sha(M/'REFERENCE_INDEX.json') == sha(B/'REFERENCE_INDEX.json'))
check('no obsolete no-transformer statement', 'No transformer is trained' not in text)
check('stopping types disclosed', 'Stops: C, CPU admission; P, patience; E, epoch ceiling' in text)
check('retrospective validation disclosed', 'not nested cross-validation or independent confirmation' in text)
check('negative attack result preserved', 'The primary criterion therefore fails' in text and '2.0123' in text)
check('unexecuted MVT-Flow distinguished', 'Source/data audit only' in text)
check('AI assistance disclosure preserved', 'OpenAI Codex assisted' in text)
conclusion = text.split('\\section{Conclusion}')[1].split('\\section*{Declarations}')[0]
words = len(conclusion.split())
check('expanded concise conclusion', 150 <= words <= 260)
result = {'utc':datetime.now(timezone.utc).isoformat(),'scope':'Same-assistant integrity and arithmetic checks, not independent scientific replication',
    'passed':all(c['passed'] for c in checks),'checks':len(checks),'pages':len(reader.pages),'conclusion_words':words,
    'pdf_sha256':sha(pdf),'underfull_diagnostics':log.count('Underfull'),'details':checks}
(M/'AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['passed','checks','pages','conclusion_words','underfull_diagnostics']}))
if not result['passed']:
    raise SystemExit([c for c in checks if not c['passed']])
