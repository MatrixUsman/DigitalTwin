"""Check the single article against preserved evidence; no experiment execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, subprocess, sys
import xml.etree.ElementTree as ET
from pypdf import PdfReader

M=Path(__file__).resolve().parent; P=M.parent; checks=[]; cache={}
def sha(path):
    path=Path(path)
    if path not in cache:
        h=hashlib.sha256()
        with path.open('rb') as f:
            for b in iter(lambda:f.read(1048576),b''): h.update(b)
        cache[path]=h.hexdigest()
    return cache[path]
def check(name, okay):
    checks.append({'check':name,'passed':bool(okay)})
    if not okay: raise AssertionError(name)
preserved={}
for cycle, expected in [
 ('residual_twin_v0.13','25a27508402677f5dae5128ccf515c1e6fca7266ee542a65dfb9ab1fcf55b1f2'),
 ('attack_audit_v0.14','987d8904dda988c7ccd51d61a5e52cf8e162e8f0156286aad89c385813b785dc'),
 ('evidence_admission_v0.15','dff21adcaf8f6697061e463068d9e50b97e342430973ec3731cb4982b109724a')]:
    path=P/'research_cycles'/cycle/'PACKAGE_MANIFEST.json'; d=json.loads(path.read_text())
    check(cycle+' manifest identity',sha(path)==expected)
    for name,h in d['sha256'].items(): check(cycle+' binding '+name,sha(P/name)==h)
    preserved[cycle]={'manifest_sha256':expected,'bindings':len(d['sha256'])}
base=json.loads((M/'BASE_IDENTITY.json').read_text())
path=P/base['previous_manifest']; check('previous revision manifest',sha(path)==base['previous_manifest_sha256'])
d=json.loads(path.read_text())
for name,h in d['sha256'].items(): check('previous revision '+name,sha(P/name)==h)
preserved['manuscript_after_v1.3']={'manifest_sha256':sha(path),'bindings':len(d['sha256'])}
example=Path('/Users/matrixusman/Downloads')/base['exemplar_filename']
check('teacher PDF unchanged',sha(example)==base['exemplar_sha256'])

assets=json.loads((M/'ASSET_RECEIPT.json').read_text())
for name,h in assets['inputs'].items(): check('asset input '+name,sha(P/name)==h)
for name,h in assets['outputs'].items(): check('asset output '+name,sha(M/name)==h)
old=P/'manuscript_after_v1.3'
for table in (old/'generated').glob('*.tex'):
    check('all prior table bytes '+table.name,sha(table)==sha(M/'generated'/table.name))
for name in ['imu_learning_curves.pdf','window_feasibility.pdf']:
    check('retained figure '+name,sha(old/'figures'/name)==sha(M/'figures'/name))

A=P/'local/attack_audit_v0.14/runs/audit_001'
N=P/'local/residual_twin_v0.13/runs/pilot_001'
summary=json.loads((A/'summary.json').read_text())
rows={r['method']:r for r in summary['rows'] if r['stratum']=='pooled'}
candidates=json.loads((N/'candidates.json').read_text())
selection=json.loads((N/'selection.json').read_text())
values=json.loads((M/'FIGURE_VALUES.json').read_text())
check('all 30 tuning points',len(values['tuning'])==len(candidates)==30)
for r in values['tuning']:
    c=next(c for c in candidates if c['plant']==r['plant'] and c['id']==r['candidate'])
    check('tuning criterion '+r['plant']+' '+r['candidate'],r['worst_q99']==c['worst_q99'])
    chosen=selection['models'][r['plant']][c['kind']]==r['candidate']
    check('selection star '+r['plant']+' '+r['candidate'],r['selected_within_role']==chosen)
for group in ['tradeoffs','ablations']:
    for r in values[group]:
        for key,v in r.items():
            if key=='method':continue
            check('graph '+group+' '+r['method']+' '+key,v==rows[r['method']][key]*(100 if key=='benign_fraction' else 1))
check('all registered methods retained',len(rows)==17 and len((M/'generated/audit.tex').read_text().splitlines())==20)
check('primary failed remains failed',summary['primary']['passed'] is False)
check('primary effect counts',rows['base_dual']['benign_alarms']==7156 and rows['rbf_dual']['benign_alarms']==7012 and rows['rbf_dual']['gap_points']==3)
check('denominators retained',all(r['eligible']==207900 and r['benign_points']==89100 and r['events']==108 for r in rows.values()))

main=(M/'main.tex').read_text(); expanded=main
for name in re.findall(r'\\input\{(sections/[^}]+)\}',main):
    expanded=expanded.replace('\\input{'+name+'}',(M/(name+'.tex')).read_text())
idx=json.loads((M/'REFERENCE_INDEX.json').read_text())
cited={k for group in re.findall(r'\\cite\{([^}]+)\}',expanded) for k in group.split(',')}
keys=set(re.findall(r'\\bibitem\{([^}]+)\}',(M/'references.tex').read_text()))
check('20 exact cited references',len(cited)==20 and cited==keys==set(idx['entries']))
check('18 recent cited versions',idx['recent_cited_versions']==18)
check('underlying bibliography unchanged',sha(M/'references.bib')==sha(old/'references.bib'))
expected=['Introduction','Literature Review','Methods','Experiments','Evaluation Metrics','Comparison Methods and Baselines','Results','Discussion','Conclusion']
body=expanded.split('\\begin{document}',1)[1].split('\\appendix')[0]
check('nine requested main sections',re.findall(r'\\section\{([^}]+)\}',body)==expected)
check('two algorithms present',all(x in expanded for x in ['Algorithm 1:','Algorithm 2:']))
figs=re.findall(r'\\includegraphics\[[^]]+\]\{([^}]+)\}',expanded)
check('seven included figures',len(figs)==7 and len(set(figs))==7)
check('one self-contained article',not (M/'supplement.tex').exists() and not re.search(r'Supplement[ ~]|supplementary material',expanded,re.I))
check('failed finding explicit','fails its declared improvement criterion' in expanded and 'below the required 10' in expanded)
check('separate real/synthetic tracks',all(x in expanded for x in ['normal-development','Synthetic','not a reproduction']))
conclusion=main.split('\\section{Conclusion}',1)[1].split('\\section*',1)[0]
check('short conclusion',len(conclusion.split())<=100)

receipt=json.loads((M/'MAIN_BUILD_RECEIPT.json').read_text());pdf=P/receipt['pdf']
check('successful offline build',receipt['returncode']==0 and receipt['offline'] and receipt['sources_unchanged'])
check('output PDF identity',sha(pdf)==receipt['pdf_sha256'])
for name in ['main.tex','references.tex',*['sections/'+p.name for p in (M/'sections').glob('*.tex')]]:
    check('built source '+name,sha(M/name)==receipt['source_sha256'][name])
log=(P/receipt['attempt']/'main.log').read_text()
check('no overfull boxes or unresolved references',not re.search(r'Overfull|undefined|LaTeX Warning|^!',log,re.M))
reader=PdfReader(pdf)
check('15 pages including appendices and references',len(reader.pages)==15)
check('sole-author PDF metadata',reader.metadata.get('/Author')=='Muhammad Usman')
tree=ET.fromstring(subprocess.check_output(['pdftotext','-bbox',str(pdf),'-']))
pages=[e for e in tree.iter() if e.tag.endswith('}page')];bounds=[]
for i,page in enumerate(pages,1):
    words=[e for e in page if e.tag.endswith('}word')]
    x0=[float(e.attrib['xMin']) for e in words];x1=[float(e.attrib['xMax']) for e in words]
    y0=[float(e.attrib['yMin']) for e in words];y1=[float(e.attrib['yMax']) for e in words]
    check(f'page {i} content within bounds',min(x0)>=0 and max(x1)<=float(page.attrib['width']) and min(y0)>=0 and max(y1)<=float(page.attrib['height']))
    bounds.append([min(x0),max(x1),min(y0),max(y1)])
txt=subprocess.check_output(['pdftotext',str(pdf),'-'],text=True)
check('no unresolved output glyphs','??' not in txt and '\ufffd' not in txt)
check('graph rendering executes no models',all(x not in (M/'generate_assets.py').read_text() for x in ['model.fit(', 'simulate(', 'train_model(']))
out={'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'scope':'same-assistant editorial and saved-evidence consistency; no independent replication','checks_passed':len(checks),'preserved':preserved,'pdf':str(pdf.relative_to(P)),'pdf_sha256':sha(pdf),'pages':15,'included_figures':figs,'references':len(keys),'conclusion_words_approx':len(conclusion.split()),'underfull_diagnostics':len(re.findall('Underfull',log)),'page_text_bounds':bounds,'checks':checks}
(M/'AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['checks_passed','pages','pdf_sha256','references','underfull_diagnostics']}))
