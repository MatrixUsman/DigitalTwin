"""Working-revision checks; no scientific training or simulator execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re
from pypdf import PdfReader
M=Path(__file__).resolve().parent;P=M.parent;B=P/'manuscript_arx_rbf_v1.6'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
checks=[]
def check(name,condition):checks.append({'check':name,'passed':bool(condition)})
identity=json.loads((M/'BASE_IDENTITY.json').read_text())
check('sealed v1.6 manifest identity',sha(B/'PACKAGE_MANIFEST.json')==identity['manifest_sha256'])
for name,h in identity['sha256'].items():check('v1.6 preserved '+name,(P/name).is_file() and sha(P/name)==h)
for folder in ['figures','generated']:
 for p in (B/folder).iterdir():
  if p.is_file() and p.name!='audit.tex':
   check('unchanged historical asset '+str(p.relative_to(B)),sha(M/p.relative_to(B))==sha(p))
check('original 17-method numbers unchanged',(M/'generated/audit.tex').read_text().replace(' & Inactive ',' & Clear ')==(B/'generated/audit.tex').read_text())
for study in ['fivefold_v0.16','forecast_baselines_v0.17']:
 manifest=P/'research_cycles'/study/'PACKAGE_MANIFEST.json'
 for name,h in json.loads(manifest.read_text())['sha256'].items():check(study+' preserved '+name,(P/name).is_file() and sha(P/name)==h)
# Independent presentation checks against the completed result summaries.
r18=json.loads((P/'research_cycles/review_extension_v0.18/REPORTING.json').read_text())
match=(M/'generated/matched_review.tex').read_text()
for row in r18['pooled']:
 if row['method'] in ['base_point','base_dual','base_dual_nodwell','rbf_point','rbf_dual','rbf_dual_nodwell']:
  check('matched table occupancy '+row['method'],f"{100*row['benign_fraction']:.3f} & {row['benign_starts_per_hour']:.1f}" in match)
r19=json.loads((P/'local/context_recovery_v0.19/final_001/results.json').read_text())
check('complete fresh population',r19['episodes']==216 and r19['outcomes']==2376)
check('prospective criterion still fails',not r19['primary']['passed'] and sum(not x for x in r19['primary']['clauses'].values())==3)
table=(M/'generated/context_final.tex').read_text()
for row in r19['summary']:
 if row['group']=='pooled':
  check('fresh table values '+row['method'],f"{100*row['occupancy']:.3f} & {row['starts_per_hour']:.1f} & {row['fresh']} & {row['fresh_delay']['p95']:.3f} & {row['outside_inactive']:,} & {row['joint']}" in table)
check('eleven methods retained',table.count('\\\\')==12)
receipt=json.loads((M/'MAIN_BUILD_RECEIPT.json').read_text())
for f,h in receipt['source_sha256'].items():check('compiled source '+f,sha(M/f)==h)
pdf=P/receipt['pdf'];reader=PdfReader(pdf)
check('PDF bound',sha(pdf)==receipt['pdf_sha256'])
check('at most15pages',len(reader.pages)<=15)
check('title preserved',reader.metadata.title=='ARX–RBF Motion Modeling for Cyberattack Detection and Recovery Monitoring in Industrial Robots')
check('requested sole author',reader.metadata.author=='Muhammad Usman')
text=(M/'main.tex').read_text()+'\n'+'\n'.join(f.read_text() for f in (M/'sections').glob('*.tex'))
keys=set()
for group in re.findall(r'\\cite\{([^}]+)\}',text):keys.update(group.split(','))
refs=set(re.findall(r'\\bibitem\{([^}]+)\}',(M/'references.tex').read_text()))
check('22 real citations no unresolved keys',keys==refs and len(refs)==22)
idx=json.loads((M/'REFERENCE_INDEX.json').read_text());check('recent version count19of22',idx['count']==22 and idx['recent_cited_versions']==19)
for marker in ['index 100','index 104','at 140','at 149','Center locations and numerical bandwidth','inactive by return + 5 s','publicly accessible accepted author manuscript','The primary criterion therefore fails','2.0123','OpenAI Codex assisted']:
 check('required disclosure '+marker,marker in text)
check('no stale Kaisar inaccessible claim','full algorithm was inaccessible' not in text and 'inaccessible full Kaisar' not in text)
check('human approval not invented',(M/'AUTHOR_ACTIONS.md').exists() and 'awaits' in (M/'AUTHOR_ACTIONS.md').read_text())
log=(P/receipt['attempt']/'main.log').read_text()
for problem in ['Overfull','undefined','Missing character','! LaTeX Error']:check('no compiler issue '+problem,problem not in log)
for p in (M/'generated').glob('*'):
 if p.suffix=='.tex':check('generated table not empty '+p.name,p.stat().st_size>0)
# New study assets are separately bound by their integration receipt once produced.
if (M/'NEW_EVIDENCE_ASSETS.json').exists():
 for name,h in json.loads((M/'NEW_EVIDENCE_ASSETS.json').read_text())['sha256'].items():check('new evidence binding '+name,sha(P/name)==h)
r={'utc':datetime.now(timezone.utc).isoformat(),'scope':'Same-assistant manuscript integrity checks, not independent scientific replication','passed':all(c['passed'] for c in checks),'checks':len(checks),'pages':len(reader.pages),'pdf_sha256':sha(pdf),'details':checks}
(M/'AUDIT.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:r[k] for k in ['passed','checks','pages','pdf_sha256']}))
if not r['passed']:raise SystemExit([c for c in checks if not c['passed']])
