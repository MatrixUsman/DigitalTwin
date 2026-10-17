"""Read-only science and manuscript checks; write a new editorial audit receipt."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, math, re, subprocess
from pypdf import PdfReader

M=Path(__file__).resolve().parent;P=M.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def require(ok,name):
    if not ok:raise AssertionError(name)
    checks.append(name)

freeze=json.loads((P/'research_cycles/commissioning_v0.9/FREEZE.json').read_text())
for group in ['source_sha256','input_sha256']:
    for path,digest in freeze[group].items():require(sha(P/path)==digest,'preserved '+path)
package=json.loads((P/'research_cycles/commissioning_v0.9/PACKAGE_MANIFEST.json').read_text())
for path,digest in package['sha256'].items():require(sha(P/path)==digest,'prior package '+path)
presentation=json.loads((M/'PRESENTATION.json').read_text())
for path,digest in presentation['source_sha256'].items():require(sha(P/path)==digest,'presentation input '+path)
for path,digest in presentation['outputs'].items():require(sha(M/path)==digest,'presentation output '+path)
require(sha(M/'present.py')==presentation['generator_sha256'],'presentation generator')

a=json.loads((P/'local/recovery_v0.8/runs/confirmation_002/aggregate.json').read_text())
rows=[r for r in a['rows'] if r['stratum']=='pooled'];by={r['method']:r for r in rows}
require(len(rows)==13,'all thirteen attack methods')
for r in rows:
    require(r['eligible']==237600 and r['benign_points']==89100 and r['events']==135,r['method']+' denominators')
    require(math.isclose(r['f1'],2*r['tp']/(2*r['tp']+r['fp']+r['fn'])),r['method']+' F1 arithmetic')
    require(r['overlap_hits']+r['misses']==135,r['method']+' all events accounted')
c=by['learned_uncertainty_return'];b=by['nominal_fixed_return'];m=by['matched_no_allowance']
require((b['benign_alarms'],c['benign_alarms'],c['cleared'],c['returned_detected'])==(621,309,36,108),'main candidate claim')
require((m['benign_alarms'],m['cleared'],m['premature_clear_events'])==(140,108,0),'matched control claim')
require(not a['primary']['passed'] and not a['primary']['tests']['timely_return'],'failed primary criterion retained')
require(round(100*(1-c['benign_alarms']/b['benign_alarms']),2)==50.24,'50.24 percent reduction')
n=json.loads((P/'local/commissioning_v0.9/runs/normal_002/fresh_summary.json').read_text())
for plant,order,reduction in [('Q1',8,.06),('Q2',16,51.27),('Q3',32,38.56)]:
    rr={r['role']:r for r in n['rows'] if r['plant']==plant};s=rr['selected_reference'];b=rr['baseline_arx4']
    require(int(s['model'].split('_')[1])==order,plant+' order')
    require(round(100*(1-s['allowance']/b['allowance']),2)==reduction,plant+' allowance reduction')
    require(s['mean_standardized_rmse']<b['mean_standardized_rmse'],plant+' RMSE comparison')
    require(s['eligible']==29700 and s['probes']==108,plant+' normal denominators')
    require(s['model']==rr['selected_arx']['model'] and s['allowance']==rr['selected_arx']['allowance'],plant+' duplicate role disclosed')
require(not n['selected_reference_admitted_to_alarm_design'],'failed normal admission retained')
noise=json.loads((P/'research_cycles/commissioning_v0.9/NOISE_DIAGNOSTIC.json').read_text())
for r in noise['records']:
    limit=.1-r['point_discrepancy_q95']
    f=math.prod(math.erf(limit/(math.sqrt(2)*v)) for v in r['standardized_sensor_sigma'])
    require(math.isclose(f**5500,r['probability_noise_only_calibration_max_leaves_95pct_population_coverage'],rel_tol=1e-6),r['plant']+' noise formula')

tex=(M/'main.tex').read_text()
cites={k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',tex) for k in group.split(',')}
bibs=set(re.findall(r'\\bibitem\{([^}]+)\}',tex))
require(cites==bibs and len(bibs)==7,'all seven references cited, no missing keys')
require(tex.count('\\caption{')==8,'six tables and two figures')
require('authors\' review and approval remain pending' in tex,'no invented author approval')
require('All evaluation observations are synthetic' in tex,'synthetic evidence labelled')
receipt=json.loads((M/'BUILD_RECEIPT.json').read_text());pdf=P/receipt['pdf']
require(sha(pdf)==receipt['pdf_sha256'],'built PDF identity')
for path,digest in receipt['source_sha256'].items():require(sha(M/path)==digest,'build input '+path)
reader=PdfReader(pdf);require(len(reader.pages)==14,'fourteen-page PDF')
txt=subprocess.check_output(['pdftotext',str(pdf),'-'],text=True)
require('AFTER:' in txt and 'Muhammad Usman' in txt and 'Haiqa Mushtaq' in txt,'title and author names')
require('�' not in txt and '??' not in txt,'no missing text glyphs or unresolved references')
log=(P/receipt['attempt']/'main.log').read_text()
require(not re.search(r'Overfull|Underfull|undefined|Missing character',log),'clean TeX layout/reference log')
qa=P/'local/manuscript_after_v1.0/qa';renders=sorted(qa.glob('delivery-*.png'))
require(len(renders)==14,'all delivery pages rendered')
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='passed',checks=len(checks),
    prior_scientific_source_bindings=len(freeze['source_sha256']),prior_input_bindings=len(freeze['input_sha256']),
    prior_package_files=len(package['sha256']),pdf_sha256=sha(pdf),pdf_pages=14,source_sha256=sha(M/'main.tex'),
    rendered_page_sha256={str(p.relative_to(P)):sha(p) for p in renders},
    scope='Editorial integrity, numeric claim arithmetic, citations, build and preserved scientific evidence; no experiment or independent peer review',
    exclusions='No publication-readiness guarantee, new method validation, author-declaration confirmation or physical validation',
    check_names=checks)
(M/'AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','checks','prior_scientific_source_bindings','prior_input_bindings','prior_package_files','pdf_pages','pdf_sha256']}))
