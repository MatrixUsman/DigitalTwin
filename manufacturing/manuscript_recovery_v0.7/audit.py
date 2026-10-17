"""Post-exposure traceability checks, not external peer review."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,sys
M=Path(__file__).resolve().parent;P=M.parent;C=P/'research_cycles/recovery_v0.7'
R=P/'local/recovery_v0.7/runs/confirmation_001'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(C))
from v7_common import check
freeze=check()
records=[
 dict(key='casper',doi='10.1145/3670414',year=2024,authors='Hakan Kayan and Ryan Heartfield and Omer Rana and Pete Burnap and Charith Perera',
      title='CASPER: Context-Aware IoT Anomaly Detection System for Industrial Robotic Arms',journal='ACM Transactions on Internet of Things',volume='5',number='3',pages='18',
      url='https://iotgarage.net/publications/pdfs/Kayan2024a.pdf',local='baselines/casper/artifacts/casper_corrected_vor_v1.1.pdf',status='Corrected VOR v1.1, 2025-02-05; first published August 2024; full text inspected'),
 dict(key='edge',doi='10.1109/JIOT.2025.3569780',year=2025,authors='Hakan Kayan and Ryan Heartfield and Omer Rana and Pete Burnap and Charith Perera',
      title='Real-Time Anomaly Detection for Industrial Robotic Arms Using Edge Computing',journal='IEEE Internet of Things Journal',volume='12',number='15',pages='29696--29712',
      url='https://iotgarage.net/publications/pdfs/Kayan2025a.pdf',local='local/contribution_v0.2/sources/edge_paper.pdf',status='Author-hosted full manuscript inspected; exact online publication day not asserted'),
 dict(key='twine',doi='10.1016/j.iot.2026.101976',year=2026,authors='Mubashar Iqbal and Sabah Suhail and Simon Freudenthaler and Muhammad Fahim and Raimundas Matulevičius',
      title='TWINE: ISO 23247-compliant digital twin and explainable AI framework for anomaly detection',journal='Internet of Things',volume='38',pages='101976',
      url='https://pureadmin.qub.ac.uk/ws/files/689658736/TWINE.pdf',local='local/comparator_admission_20261017/twine/qub_public_pdf.pdf',status='Locally available peer-reviewed accepted manuscript; live fetch failed this cycle; prior receipt retained'),
 dict(key='ayankoso',doi='10.3390/machines12090630',year=2024,authors='Samuel Ayankoso and Fengshou Gu and Hassna Louadah and Hamidreza Fahham and Andrew Ball',
      title='Artificial-Intelligence-Based Condition Monitoring of Industrial Collaborative Robots: Detecting Anomalies and Adapting to Trajectory Changes',journal='Machines',volume='12',number='9',pages='630',
      url='https://www.mdpi.com/2075-1702/12/9/630',local='local/recovery_v0.5/sources/ayankoso_pdf.pdf',status='Publisher full manuscript; published 2024-09-07, accepted 2024-09-04'),
 dict(key='meseguer',doi='10.1016/j.jprocont.2010.06.017',year=2010,authors='Jordi Meseguer and Vicenç Puig and Teresa Escobet and Jordi Saludes',
      title='Observer gain effect in linear interval observer-based fault detection',journal='Journal of Process Control',volume='20',number='8',pages='944--956',
      url='https://futur.upc.edu/2748744',status='Institutional metadata and publisher abstract; full method/code not audited; historical background'),
 dict(key='nist',year=2026,authors='{NIST/SEMATECH}',title='CUSUM Control Charts',url='https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm',
      status='Official e-Handbook section 6.3.2.3 read; 2026 is access year, not asserted publication date'),
 dict(key='rapio',doi='10.3390/jmse14151445',year=2026,authors='Ishaq Ahmed and Ayman Alharbi and Jun Lu and Amar Jaffar and Muhammad Bilal',
      title='Robust Adaptive Propagated Interval Observer for Actuator Fault Diagnosis in Underactuated AUVs',journal='Journal of Marine Science and Engineering',volume='14',number='15',pages='1445',
      url='https://www.mdpi.com/2077-1312/14/15/1445',status='Publisher-indexed metadata/text; direct page rate-limited; full recovery equations, exact online date and code unresolved'),
 dict(key='kaisar',doi='10.1109/OJCOMS.2026.3739185',year=2026,authors='Hunain Kaisar and Muhammad Rehan and Ijaz Ahmed and Muhammad Bilal and Muhammad Khalid',
      title='A Digital Twin-Based Cybersecurity Architecture for FDI Anomaly Detection and Isolation in Next Generation Robotic Vehicles',journal='IEEE Open Journal of the Communications Society',volume='7',pages='12709--12728',
      url='https://pure.kfupm.edu.sa/en/publications/a-digital-twin-based-cybersecurity-architecture-for-fdi-anomaly-d/',local='local/recovery_v0.5/sources/kaisar_crossref.json',status='Institutional abstract and Crossref metadata; full manuscript and exact publication day unresolved'),
 dict(key='voraus',year=2023,authors='Jan Thieß Brockmann and Marco Rudolph and Bodo Rosenhahn and Bastian Wandt',title='The voraus-AD Dataset for Anomaly Detection in Robot Applications',
      url='https://arxiv.org/abs/2311.04765',identifier='arXiv:2311.04765',status='Submitted 2023-11-08; author record reports IEEE T-RO acceptance, final issue/DOI not used; no data admission')]
for r in records:
    if 'local' in r:r['local_sha256']=sha(P/r['local'])
(M/'REFERENCE_MANIFEST.json').write_text(json.dumps(dict(checked_date='2026-10-17',records=records,
    verification='Manual primary-source inspection with explicit scope limits; local hashes rechecked by this script'),indent=2,ensure_ascii=False)+'\n')
bib=[]
for r in records:
    kind='article' if 'journal' in r else 'misc'
    fields={k:v for k,v in r.items() if k in ['title','journal','volume','number','pages','doi','url']}
    fields['author']=r['authors']
    if r['key']!='nist':fields['year']=r['year']
    fields['note']=r['status']
    bib.append('@'+kind+'{'+r['key']+',\n'+',\n'.join('  '+k+' = {'+str(v)+'}' for k,v in fields.items())+'\n}')
(M/'references.bib').write_text('\n\n'.join(bib)+'\n')
text='\n'.join(p.read_text() for p in (M/'sections').glob('*.tex'))+(M/'main.tex').read_text()
citations={x for y in re.findall(r'\\cite\{([^}]+)\}',text) for x in y.split(',')}
entries=set(re.findall(r'\\bibitem\{([^}]+)\}',(M/'references.tex').read_text()))
assert citations==entries=={r['key'] for r in records}
a=json.loads((R/'aggregate.json').read_text());by={r['method']:r for r in a['rows'] if r['stratum']=='pooled'}
assert not a['primary_test']['passed']
assert by['nominal_fixed_return']['benign_alarms']==2778 and by['fused_hysteresis']['benign_alarms']==2452
assert by['nominal_fixed_return']['premature_clear_events']==0 and by['matched_no_dwell']['premature_clear_events']==44
assert by['matched_hysteresis']['premature_clear_events']==5 and by['matched_no_margin']['premature_clear_events']==1
assert by['following_hysteresis']['benign_alarms']==1529 and by['following_hysteresis']['premature_clear_events']==90
assert by['nominal_fixed_return']['cleared_within_five_seconds']==90 and by['nominal_fixed_return']['max_clear_delay']==.92
assert json.loads((M/'generated/entry_ablation_equality.json').read_text())['all_equal']
sources=json.loads((M/'generated/SOURCE_IDENTITIES.json').read_text())
assert all(sha(P/k)==v for k,v in sources['source_sha256'].items())
assert len(json.loads((R/'outcomes.json').read_text()))==3312
audit=dict(utc=datetime.now(timezone.utc).isoformat(),status='passed',scientific_source_files=len(freeze['source_sha256']),
    preserved_inputs=len(freeze['input_sha256']),citations=sorted(citations),local_source_files=sum('local' in r for r in records),
    source_table_hashes_match=True,key_numeric_claims_match=True,primary_failure_retained=True,
    human_author_review='pending',external_peer_review=False,original_method_contribution='not established',
    scope='Source identity, key numerical claim assertions and citation-key coverage; source support reviewed manually in SOURCES_AND_ADMISSION.md')
(M/'AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps(audit))
