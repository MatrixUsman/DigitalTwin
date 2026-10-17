"""Offline aggregate/identity/LaTeX checks. No model, raw-data or TeX execution."""
from pathlib import Path
import argparse, collections, datetime, hashlib, json, math, re, subprocess, sys
import build_assets  # Installs raw-path and network rejection before any inputs are read.
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(test,message):
 if not test:raise ValueError(message)
def close(a,b):return math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12)
def clean(s):
 s=re.sub(r'\\begin\{verbatim\}.*?\\end\{verbatim\}','',s,flags=re.S)
 return re.sub(r'(?<!\\)%[^\n]*','',s)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--receipt',type=Path);args=parser.parse_args()
 manifest=read('reproducibility/SOURCE_MANIFEST.json')
 for entry in manifest['entries']:
  require(sha(ROOT/entry['bundled_path'])==entry['sha256'],'Bundled identity mismatch: '+entry['bundled_path'])
 require(len(manifest['entries'])==71,'Expected 71 source/input entries')
 require(sum(x['role']=='exact tested source/configuration' for x in manifest['entries'])==52,'Tested source count')
 s=read('reproducibility/inputs/FINAL_CAMPAIGN_V0.1_SUMMARY.json');r=read('reproducibility/inputs/FINAL_CAMPAIGN_V0.1_RECORD.json')
 methods=s['methods'];require(len(methods)==len(set(methods))==11 and methods==r['methods'],'Roster')
 require(r['actual_failed_final_attempts']==[] and not r['automatic_retries'],'Recorded failures/retries')
 require(r['holdout_now_exposed'] is True,'Exposed holdout must remain visible')
 require(len(s['event_outcomes_without_episode_lists'])==88 and len(s['recovery'])==88,'Event/recovery roster')
 for name in methods:
  d=s['summary'][name];v=d['mixed'];n=d['normal'];events=[x for x in s['event_outcomes_without_episode_lists'] if x['method']==name];recovery=[x for x in s['recovery'] if x['method']==name]
  require(d['seed'] is None,'Unexpected seed')
  require(v['tp']+v['fn']==345602 and v['fp']+v['tn']==337044,'Confusion population')
  require(close(v['precision'],v['tp']/(v['tp']+v['fp'])) and close(v['recall'],v['tp']/345602) and close(v['f1'],2*v['tp']/(2*v['tp']+v['fp']+v['fn'])),'Point arithmetic')
  require(d['coverage']['scored_rows']==897119 and d['coverage']['eligible_coverage']==1,'Final support')
  require(n['coverage']['eligible_rows']==214473 and close(n['points']['point_exceedance'],n['points']['alarm_rows']/214473),'Normal support')
  require(close(n['episodes_per_hour'],n['episode_count']/(float(n['exposure_seconds'])/3600)),'Episode exposure')
  require([x['event'] for x in events]==list(range(1,9)) and len(recovery)==8,'Event order/support')
  require(sum(x['alarm_rows'] for x in events)==v['tp'] and sum(x['alarm_rows'] for x in recovery)==v['fp'],'Event/recovery count reconciliation')
  require(sum(x['overlap_hit'] for x in events)==d['event_overlap_hits'],'Event hits')
  for x in events:
   require(not x['pre_existing_alarm'],'Actual no-pre-existing result changed')
   require((x['fresh_delay_seconds'] is None)==(not x['fresh_onset']),'Undefined delay/miss')
   require(close(x['within_event_point_recall'],x['alarm_rows']/x['eligible_rows']),'Event coverage')
 ref_list=read('editorial/references.json');keys={x['key'] for x in ref_list};require(len(keys)==len(ref_list)==13,'Reference uniqueness')
 index=read('editorial/SOURCE_EVIDENCE_INDEX.json')
 for key,x in index.items():require(sha(ROOT/x['path'])==x['sha256'],'Source note identity: '+key)
 tex=list(ROOT.glob('*.tex'))+list((ROOT/'sections').glob('*.tex'))+list((ROOT/'generated').glob('*.tex'))+list((ROOT/'figures').glob('*.tex'))
 bodies=[clean(p.read_text()) for p in tex];alltex='\n'.join(bodies)
 cited={x for group in re.findall(r'\\cite\{([^}]+)\}',alltex) for x in group.split(',')}
 require(cited==keys,'Missing or uncited reference keys: '+str(cited^keys))
 labels=re.findall(r'\\label\{([^}]+)\}',alltex);require(len(labels)==len(set(labels)),'Duplicate labels')
 require(set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',alltex))<=set(labels),'Unresolved cross-reference')
 for p,body in zip(tex,bodies):
  for target in re.findall(r'\\input\{([^}]+)\}',body):require((ROOT/(target if target.endswith('.tex') else target+'.tex')).is_file(),'Missing TeX input '+target)
  balance=0
  for match in re.finditer(r'(?<!\\)[{}]',body):
   balance+=1 if match[0]=='{' else -1;require(balance>=0,'Closing brace: '+str(p))
  require(balance==0,'Unclosed brace: '+str(p))
  stack=[]
  for token,name in re.findall(r'\\(begin|end)\{([^}]+)\}',body):
   if token=='begin':stack.append(name)
   else:require(bool(stack) and stack.pop()==name,'Environment mismatch: '+str(p))
  require(not stack,'Open environment: '+str(p))
 registry=read('editorial/CLAIM_EVIDENCE_MAP.json');expected={}
 for p in (ROOT/'sections').glob('*.tex'):
  text=p.read_text();markers=list(re.finditer(r'% claim: (\w+)\n',text))
  for i,marker in enumerate(markers):
   require(marker[1] not in expected,'Duplicate claim ID')
   span=text[marker.end():markers[i+1].start() if i+1<len(markers) else len(text)]
   expected[marker[1]]=(p,hashlib.sha256(span.encode()).hexdigest())
 require(set(expected)=={x['id'] for x in registry['claims']},'Unregistered claim marker')
 for claim in registry['claims']:
  p,span_sha=expected[claim['id']];require(sha(p)==claim['file_sha256'] and span_sha==claim['span_sha256'],'Stale claim span '+claim['id'])
  for evidence in claim['evidence']:require(sha(ROOT/evidence['path'])==evidence['sha256'],'Stale evidence '+evidence['path'])
 result=subprocess.run([sys.executable,str(ROOT/'tools/build_assets.py'),'--check'],capture_output=True,text=True)
 require(result.returncode==0,'Asset regeneration failed: '+result.stderr)
 receipt={'kind':'local_manuscript_package_check','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'success':True,'python':sys.version,'bundled_entries':71,'tested_source_identities':52,'references':len(keys),'claim_groups':len(expected),'tex_files_checked':len(tex),'methods':11,'event_rows':88,'recovery_rows':88,'checks':['content hashes','confusion, normal burden, event/recovery arithmetic','complete deterministic method/support roster','registered claim spans and evidence hashes','citation keys, TeX inputs, labels, braces and environment pairing','byte-identical asset regeneration'],'assets':json.loads(result.stdout),'raw_data_opened':False,'models_run':False,'new_benchmark_results':False,'synthetic_suite_reexecuted':False,'latex_compiled_by_this_check':False,'pdf_visual_qa_by_this_check':False,'limits':['Static checks cannot validate TeX compilation or layout.','AP and score truth rely on saved score audit, not recalculation from aggregate counts.','Claim links do not establish semantic completeness, author understanding or independent peer review.','This is not independent end-to-end experiment reproduction.'],'bindings':{str(p.relative_to(ROOT)):sha(p) for p in sorted(set(tex+[ROOT/'editorial/CLAIM_EVIDENCE_MAP.json',ROOT/'editorial/references.json',ROOT/'editorial/SOURCE_EVIDENCE_INDEX.json',ROOT/'tools/build_assets.py',Path(__file__)]))}}
 if args.receipt:args.receipt.parent.mkdir(parents=True,exist_ok=True);args.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({k:receipt[k] for k in ['success','bundled_entries','claim_groups','references','methods','event_rows','latex_compiled_by_this_check']}))
if __name__=='__main__':main()
