"""Check presentation provenance and preserved evidence; run no experiments."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,subprocess,sys
from pypdf import PdfReader
import xml.etree.ElementTree as ET
M=Path(__file__).resolve().parent;P=M.parent;checks=[];cache={}
def sha(p):
    p=Path(p)
    if p not in cache:
        h=hashlib.sha256()
        with p.open('rb') as f:
            for b in iter(lambda:f.read(1048576),b''):h.update(b)
        cache[p]=h.hexdigest()
    return cache[p]
def check(name,ok):
    checks.append({'check':name,'passed':bool(ok)})
    if not ok:raise AssertionError(name)
preserved={}
for cycle,expected in [
 ('residual_twin_v0.13','25a27508402677f5dae5128ccf515c1e6fca7266ee542a65dfb9ab1fcf55b1f2'),
 ('attack_audit_v0.14','987d8904dda988c7ccd51d61a5e52cf8e162e8f0156286aad89c385813b785dc'),
 ('evidence_admission_v0.15','dff21adcaf8f6697061e463068d9e50b97e342430973ec3731cb4982b109724a')]:
    p=P/'research_cycles'/cycle/'PACKAGE_MANIFEST.json';d=json.loads(p.read_text())
    check(cycle+' manifest identity',sha(p)==expected)
    for name,h in d['sha256'].items():check(cycle+' binding '+name,sha(P/name)==h)
    preserved[cycle]={'manifest_sha256':expected,'bindings':len(d['sha256'])}
b=json.loads((M/'BASE_IDENTITY.json').read_text())
check('prior manuscript source unchanged',sha(P.parent/b['source'])==b['sha256'])
check('prior manuscript PDF unchanged',sha(P/'output/pdf/AFTER-Muhammad-Usman-revised.pdf')==b['prior_pdf_sha256'])
assets=json.loads((M/'ASSET_RECEIPT.json').read_text())
for name,h in assets['inputs'].items():check('presentation source '+name,sha(P/name)==h)
for name,h in assets['outputs'].items():check('presentation output '+name,sha(M/name)==h)
for name in ['attack','metrics','normal','normal_all','imu','noise','window']:
    check('older table unchanged '+name,sha(M/f'generated/{name}.tex')==sha(P/f'manuscript_after_v1.2/generated/{name}.tex'))
idx=json.loads((M/'REFERENCE_INDEX.json').read_text());main=(M/'main.tex').read_text();refs=(M/'references.tex').read_text()
keys=set(re.findall(r'\\bibitem\{([^}]+)\}',refs));cited={k for group in re.findall(r'\\cite\{([^}]+)\}',main) for k in group.split(',')}
check('exactly 20 cited bibliography entries',len(keys)==20 and keys==cited==set(idx['entries']))
check('recent cited versions 18/20',idx['recent_cited_versions']==18)
check('failed primary explicit',"fails its declared improvement criterion" in main and 'below the required 10' in main)
summary=json.loads((P/'local/attack_audit_v0.14/runs/audit_001/summary.json').read_text())
pooled={r['method']:r for r in summary['rows'] if r['stratum']=='pooled'}
check('all registered methods visible',len(pooled)==17 and len((M/'generated/audit.tex').read_text().splitlines())==20)
check('frozen primary remains failed',summary['primary']['passed'] is False)
check('candidate counts match prose',pooled['base_dual']['benign_alarms']==7156 and pooled['rbf_dual']['benign_alarms']==7012 and pooled['rbf_dual']['gap_points']==3)
check('correct denominator statements',all(r['eligible']==207900 and r['benign_points']==89100 and r['events']==108 for r in pooled.values()))
pdfs={}
for doc,filename,expected_pages in [('main','AFTER-Muhammad-Usman-v1.3.pdf',11),('supplement','AFTER-Muhammad-Usman-v1.3-supplement.pdf',12)]:
    receipt=json.loads((M/(doc.upper()+'_BUILD_RECEIPT.json')).read_text());pdf=P/'output/pdf'/filename
    check(doc+' build success',receipt['returncode']==0 and receipt['offline'] and receipt['sources_unchanged'])
    check(doc+' PDF build identity',sha(pdf)==receipt['pdf_sha256'])
    log=(P/receipt['attempt']/(doc+'.log')).read_text()
    check(doc+' no unresolved or overfull TeX diagnostics',not re.search(r'Overfull|Underfull|undefined|LaTeX Warning|^!',log,re.M))
    # Cross-document assets may have changed since the supplement build but are not referenced there.
    f=PdfReader(pdf)
    check(doc+' page count',len(f.pages)==expected_pages)
    check(doc+' sole PDF byline',f.metadata.get('/Author')=='Muhammad Usman')
    tree=ET.fromstring(subprocess.check_output(['pdftotext','-bbox',str(pdf),'-']))
    pages=[e for e in tree.iter() if e.tag.endswith('}page')];bounds=[]
    check(doc+' extracted pages align',len(pages)==expected_pages)
    for i,page in enumerate(pages,1):
        words=[e for e in page if e.tag.endswith('}word')]
        x0=[float(e.attrib['xMin']) for e in words];x1=[float(e.attrib['xMax']) for e in words]
        y0=[float(e.attrib['yMin']) for e in words];y1=[float(e.attrib['yMax']) for e in words]
        bounds.append([round(min(x0),2),round(max(x1),2)])
        check(f'{doc} page {i} text within page',min(x0)>=0 and max(x1)<=float(page.attrib['width']) and min(y0)>=0 and max(y1)<=float(page.attrib['height']))
    text=subprocess.check_output(['pdftotext',str(pdf),'-'],text=True)
    check(doc+' no unresolved markers','??' not in text and '\ufffd' not in text)
    pdfs[doc]={'file':str(pdf.relative_to(P)),'sha256':sha(pdf),'pages':expected_pages,'text_bounds':bounds}
conclusion=main.split('\\section{Conclusion}',1)[1].split('\\section*',1)[0]
check('short conclusion',len(conclusion.split())<=100)
check('no training in asset renderer',all(x not in (M/'generate_assets.py').read_text() for x in ['model.fit(', 'simulate(', 'train_model(']))
out={'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'scope':'editorial and saved-artifact consistency; not independent replication','checks_passed':len(checks),'preserved':preserved,'pdfs':pdfs,'conclusion_words_approx':len(conclusion.split()),'checks':checks}
(M/'AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['checks_passed','conclusion_words_approx','preserved']}))
