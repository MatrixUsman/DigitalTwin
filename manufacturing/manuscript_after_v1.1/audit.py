"""Audit saved evidence and editorial artifacts; never train or parse raw data."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import re
import subprocess
from pypdf import PdfReader

M = Path(__file__).resolve().parent
P = M.parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
checks = []


def require(ok, name):
    if not ok:
        raise AssertionError(name)
    checks.append(name)


freeze = json.loads((P / 'research_cycles/commissioning_v0.9/FREEZE.json').read_text())
for group in ['source_sha256', 'input_sha256']:
    for path, digest in freeze[group].items():
        require(sha(P / path) == digest, 'preserved ' + path)
packages = {}
for directory in ['research_cycles/commissioning_v0.9',
                  'research_cycles/casper_comparison_v0.10',
                  'research_cycles/casper_convergence_v0.11',
                  'research_cycles/return_bound_v0.12', 'manuscript_after_v1.0']:
    path = P / directory / 'PACKAGE_MANIFEST.json'
    package = json.loads(path.read_text())
    for name, digest in package['sha256'].items():
        require(sha(P / name) == digest, 'prior package ' + name)
    packages[directory] = {'files': len(package['sha256']), 'manifest_sha256': sha(path)}

presentation = json.loads((M / 'PRESENTATION.json').read_text())
for path, digest in presentation['source_sha256'].items():
    require(sha(P / path) == digest, 'presentation input ' + path)
for path, digest in presentation['outputs'].items():
    require(sha(M / path) == digest, 'presentation output ' + path)
require(sha(M / 'present.py') == presentation['generator_sha256'], 'presentation generator')

a = json.loads((P / 'local/recovery_v0.8/runs/confirmation_002/aggregate.json').read_text())
rows = [r for r in a['rows'] if r['stratum'] == 'pooled']
by = {r['method']: r for r in rows}
require(len(rows) == 13, 'all thirteen attack methods')
for r in rows:
    require(r['eligible'] == 237600 and r['benign_points'] == 89100 and r['events'] == 135,
            r['method'] + ' denominators')
    require(math.isclose(r['f1'], 2*r['tp']/(2*r['tp']+r['fp']+r['fn'])), r['method'] + ' F1')
    require(r['overlap_hits'] + r['misses'] == 135, r['method'] + ' all events accounted')
c = by['learned_uncertainty_return']
b = by['nominal_fixed_return']
m = by['matched_no_allowance']
require((b['benign_alarms'], c['benign_alarms'], c['cleared'], c['returned_detected']) ==
        (621, 309, 36, 108), 'main candidate claim')
require((m['benign_alarms'], m['cleared'], m['premature_clear_events']) == (140, 108, 0),
        'matched control claim')
require(not a['primary']['passed'] and not a['primary']['tests']['timely_return'],
        'failed primary criterion retained')
require(round(100*(1-c['benign_alarms']/b['benign_alarms']), 2) == 50.24, 'alarm reduction')

n = json.loads((P / 'local/commissioning_v0.9/runs/normal_002/fresh_summary.json').read_text())
for plant, order, reduction in [('Q1', 8, .06), ('Q2', 16, 51.27), ('Q3', 32, 38.56)]:
    rr = {r['role']: r for r in n['rows'] if r['plant'] == plant}
    s, b = rr['selected_reference'], rr['baseline_arx4']
    require(int(s['model'].split('_')[1]) == order, plant + ' order')
    require(round(100*(1-s['allowance']/b['allowance']), 2) == reduction, plant + ' allowance')
    require(s['mean_standardized_rmse'] < b['mean_standardized_rmse'], plant + ' RMSE')
    require(s['eligible'] == 29700 and s['probes'] == 108, plant + ' denominators')
    require(s['model'] == rr['selected_arx']['model'] and
            s['allowance'] == rr['selected_arx']['allowance'], plant + ' duplicate role')
require(not n['selected_reference_admitted_to_alarm_design'], 'failed normal admission')
noise = json.loads((P / 'research_cycles/commissioning_v0.9/NOISE_DIAGNOSTIC.json').read_text())
for r in noise['records']:
    limit = .1-r['point_discrepancy_q95']
    f = math.prod(math.erf(limit/(math.sqrt(2)*v)) for v in r['standardized_sensor_sigma'])
    require(math.isclose(f**5500,
            r['probability_noise_only_calibration_max_leaves_95pct_population_coverage'],
            rel_tol=1e-6), r['plant'] + ' Gaussian calculation')

w = json.loads((P / 'local/return_bound_v0.12/runs/diagnostic_001/summary.json').read_text())
wr = w['records']
envelope = [r for r in wr if r['method'] == 'multiwindow']
require(w['synthetic'] and not w['real_data_access'], 'residual study synthetic')
require(len(wr) == 216 and len(envelope) == 36, 'all residual outcomes')
require(all(r['eligible'] == 1000 for r in wr), 'common residual support')
for r in wr:
    require(r['fraction'] == r['certified']/r['eligible'], r['trace'] + ' ' + r['method'] + ' fraction')
require(sum(r['feasibility_pass'] for r in envelope) == 20 and
        not w['overall_feasibility_pass'], '20 of 36, failed overall gate')
require(all(r['certified'] == 0 for r in wr if r['method'] == 'fixed_1'), 'no instantaneous certificates')
require(all(not r['any_coverage_violation'] for r in wr if r['assumptions_satisfied']),
        'no observed valid-control violations, not a risk estimate')
slow = sorted(r['certified'] for r in envelope
              if r['noise'] == 'ar08_low' and r['profile'] == 'slow_within_tolerance')
require(slow == [858, 1000, 1000], 'correlated slow seed outcomes')

i = json.loads((P / 'local/casper_convergence_v0.11/runs/pilot_001/summary.json').read_text())
im = {r['model']: r for r in i['models']}
require(len(im) == 9 and i['training_targets'] == 8192 and i['development_targets'] == 2048,
        'all IMU models and common populations')
require(i['attack_metrics'] is None and i['threshold'] is None and not i['final_access'],
        'IMU prediction only')
require(i['scaler_unchanged'], 'training-only scaling unchanged')
require(all(r['eligible_observations'] == 2048 for r in im.values()), 'common IMU score support')
require(min(im, key=lambda k: im[k]['standardized_mse']) == 'ar4', 'AR4 lowest development error')
require(round(im['ar4']['standardized_mse'], 6) == .006074, 'AR4 MSE')
short = json.loads((P / 'local/casper_comparison_v0.10/runs/pilot_002/summary.json').read_text())
sm = {r['model']: r for r in short['models']}
reductions = []
for seed in [17, 42, 2026]:
    c = im['casper_cnn_seed'+str(seed)]
    e = im['edge_cnn_seed'+str(seed)]
    require(c['epochs'] == 27 and c['selected_epoch'] == 22 and
            c['stopping_reason'] == 'normal_development_patience', f'CASPER seed {seed} stopping')
    require(e['epochs'] == 100 and e['selected_epoch'] == 100 and
            e['stopping_reason'] == 'maximum_epochs', f'compact seed {seed} epoch limit')
    require(e['history'][-1]['development_mse'] < e['history'][-2]['development_mse'],
            f'compact seed {seed} still improving')
    reductions.append(100*(1-c['standardized_mse']/sm[c['model']]['standardized_mse']))
require(round(min(reductions), 2) == 46.11 and round(max(reductions), 2) == 58.12,
        'CASPER longer-training improvement range')

tex = (M / 'main.tex').read_text()
for section in ['return_bound', 'imu_reference']:
    tex = tex.replace('\\input{sections/'+section+'}', (M / 'sections' / (section+'.tex')).read_text())
cites = [k.strip() for group in re.findall(r'\\cite\{([^}]+)\}', tex) for k in group.split(',')]
bibs = re.findall(r'\\bibitem\{([^}]+)\}', tex)
require(list(dict.fromkeys(cites)) == bibs and len(bibs) == 9, 'nine references in first-citation order')
bibkeys = re.findall(r'@\w+\{([^,]+),', (M / 'references.bib').read_text())
require(set(bibkeys) == set(bibs), 'editable bibliography agrees')
require(tex.count('\\begin{table}') == 8 and tex.count('\\begin{figure}') == 4,
        'eight tables and four figures')
require('\\author{Muhammad Usman' in tex and 'Haiqa' not in tex, 'sole requested byline')
require('This research received no funding.' in tex and 'The author declares no competing interests.' in tex,
        'confirmed declarations')
require('AI assistance' in tex and 'does not denote a newly validated detector' in tex,
        'assistance and scientific scope explicit')
require('All observations in the attack and recovery simulations are synthetic.' in tex,
        'synthetic and separate real evidence distinguished')

receipt = json.loads((M / 'BUILD_RECEIPT.json').read_text())
pdf = P / receipt['pdf']
require(sha(pdf) == receipt['pdf_sha256'], 'PDF identity')
for path, digest in receipt['source_sha256'].items():
    require(sha(M / path) == digest, 'build input ' + path)
reader = PdfReader(pdf)
require(len(reader.pages) == 20, 'twenty-page PDF')
require(reader.metadata.author == 'Muhammad Usman', 'sole PDF author metadata')
txt = subprocess.check_output(['pdftotext', str(pdf), '-'], text=True)
require('AFTER:' in txt and 'Muhammad Usman' in txt and 'Haiqa' not in txt, 'PDF byline')
require('�' not in txt and '??' not in txt, 'no unresolved glyphs or references')
log = (P / receipt['attempt'] / 'main.log').read_text()
require(not re.search(r'Overfull|Underfull|undefined|Missing character', log), 'clean TeX log')
renders = sorted((P / 'local/manuscript_after_v1.1/qa_final').glob('page-*.png'))
require(len(renders) == 20, 'all final pages rendered')

result = dict(utc=datetime.now(timezone.utc).isoformat(), status='passed', checks=len(checks),
              prior_source_bindings=len(freeze['source_sha256']),
              prior_input_bindings=len(freeze['input_sha256']), prior_packages=packages,
              pdf_sha256=sha(pdf), pdf_pages=20, audit_source_sha256=sha(Path(__file__)),
              rendered_page_sha256={str(p.relative_to(P)): sha(p) for p in renders},
              scope='Editorial arithmetic, citations, presentation/build identity and preserved prior evidence',
              exclusions='No new experiment, independent peer review, acceptance prediction or human author approval',
              check_names=checks)
(M / 'AUDIT.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ['status', 'checks', 'prior_source_bindings',
                                       'prior_input_bindings', 'pdf_pages', 'pdf_sha256']}))
