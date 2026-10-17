"""Deterministic manuscript assets from sealed aggregate results; no raw/model access."""
from pathlib import Path
from decimal import Decimal
import argparse, hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def esc(s):
 return ''.join({'&':r'\&','%':r'\%','_':r'\_','#':r'\#','{':r'\{','}':r'\}'}.get(c,c) for c in str(s))
def guard(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes)):
  q=Path(args[0].decode() if isinstance(args[0],bytes) else args[0]).resolve()
  if any(a=='datasets' and b=='raw' for a,b in zip(q.parts,q.parts[1:])):raise PermissionError('No raw data for manuscript generation')
 if event in ('socket.connect','socket.getaddrinfo'):raise PermissionError('Offline artifact generation')
sys.addaudithook(guard)
def load(name):return json.loads((ROOT/'reproducibility/inputs'/name).read_text())
def tab(headers,rows,align):
 return '\\begin{tabular}{'+align+'}\n\\toprule\n'+' & '.join(headers)+' \\\\\n\\midrule\n'+'\n'.join(' & '.join(map(str,row))+' \\\\' for row in rows)+'\n\\bottomrule\n\\end{tabular}\n'
def main():
 args=argparse.ArgumentParser();args.add_argument('--check',action='store_true');a=args.parse_args()
 manifest=json.loads((ROOT/'reproducibility/SOURCE_MANIFEST.json').read_text())
 for rec in manifest['entries']:
  assert sha(ROOT/rec['bundled_path'])==rec['sha256'],rec['bundled_path']
 s=load('FINAL_CAMPAIGN_V0.1_SUMMARY.json');r=load('FINAL_CAMPAIGN_V0.1_RECORD.json');o=load('OBSERVER_V0.1_SUMMARY.json');c=load('CONTROLS_V0.1_SUMMARY.json')
 methods=s['methods'];data=s['summary'];assert methods==r['methods'] and len(methods)==11
 output={}
 rows=[]
 for name in methods:
  x=data[name];v=x['mixed'];n=x['normal'];assert v['tp']+v['fn']==345602 and v['fp']+v['tn']==337044
  rows.append([name,*[f'{v[k]:.6f}' for k in ['precision','recall','f1','average_precision']],f"{100*n['points']['point_exceedance']:.4f}",f"{n['episodes_per_hour']:.2f}",f"{x['event_overlap_hits']}/8"])
 output['generated/main_results.tex']=tab(['Method','Precision','Recall','F1','AP',r'Normal (\%)',r'Episodes/h','Hits'],rows,'lrrrrrrr')
 output['generated/confusion.tex']=tab(['Method','TP','FP','FN','TN','Normal alarms','Episodes'],[[n,*[f"{data[n]['mixed'][k]:,}" for k in ['tp','fp','fn','tn']],f"{data[n]['normal']['points']['alarm_rows']:,}",f"{data[n]['normal']['episode_count']:,}"] for n in methods],'lrrrrrr')
 events={n:[x for x in s['event_outcomes_without_episode_lists'] if x['method']==n] for n in methods}
 assert all(len(x)==8 for x in events.values())
 # Keys and exact native delays are inherited from the verified full export.
 event_rows=[]
 for n in methods:
  ev=events[n]
  delays=[('MISS' if x['fresh_delay_seconds'] is None else f"{Decimal(x['fresh_delay_seconds']):.2f}") for x in ev]
  event_rows.append([n,*delays,str(data[n]['missed_events'])])
 output['generated/event_delays.tex']=tab(['Method',*[f'E{i}' for i in range(1,9)],'Misses'],event_rows,'lrrrrrrrrr')
 recovery={n:[x for x in s['recovery'] if x['method']==n] for n in methods}
 assert all(len(x)==8 for x in recovery.values())
 output['generated/recovery.tex']=tab(['Method',*[f'Z{i}' for i in range(1,9)]],[[n,*[f"{x['alarm_rows']}/{x['eligible_rows']}" for x in recovery[n]]] for n in methods],'lrrrrrrrr')
 output['generated/selection.tex']=tab(['Candidate','Development objective','Selected'],[[esc(x['id']),f"{x['development_mean_score']:.9f}",'yes' if x['id'] in {v['candidate_id'] for v in c['selection'].values()} else 'no'] for x in c['candidates']],'lrr')
 output['generated/thresholds.tex']=tab(['Method','Frozen threshold'],[[x['method'],format(x['threshold'],'.17g')] for x in r['run_matrix']],'lr')
 rr=[]
 for name,x in r['resource_receipts'].items():rr.append([esc(name),f"{x['wall_seconds']:.3f}",f"{x['process_cpu_seconds']:.3f}",f"{x['peak_rss_bytes']/2**20:.2f}",f"{x['total_output_bytes']/2**20:.3f}"])
 output['generated/resources.tex']=tab(['Phase','Wall (s)','CPU (s)','Peak RSS (MiB)','Output (MiB)'],rr,'lrrrr')
 rc=data['O-RC'];res=data['O-R'];macros={
 'RCFone':f"{rc['mixed']['f1']:.6f}",'RFone':f"{res['mixed']['f1']:.6f}",'RCRecallPct':f"{100*rc['mixed']['recall']:.4f}",'RCNormalPct':f"{100*rc['normal']['points']['point_exceedance']:.4f}",'RCEpisodes':str(rc['normal']['episode_count']),'RCEpisodeRate':f"{rc['normal']['episodes_per_hour']:.2f}",'FoneGain':f"{rc['mixed']['f1']-res['mixed']['f1']:.9f}",'ARFone':f"{data['AR-4']['mixed']['f1']:.6f}",'ARAP':f"{data['AR-4']['mixed']['average_precision']:.6f}",'AREpisodeRate':f"{data['AR-4']['normal']['episodes_per_hour']:.2f}",'TemplateFone':f"{data['T-32']['mixed']['f1']:.6f}",'TemplateRecallPct':f"{100*data['T-32']['mixed']['recall']:.4f}",'TemplateNormalPct':f"{100*data['T-32']['normal']['points']['point_exceedance']:.4f}",'PrevalencePct':f"{100*r['mixed_positive_prevalence']:.4f}",'NormalHours':f"{float(rc['normal']['exposure_seconds'])/3600:.5f}",'FitA':format(o['training_normalizers']['residual']['mean'],'.16g'),'FitB':format(o['training_normalizers']['correction_js']['mean'],'.16g'),'FitTau':format(o['fitted_observer_configuration']['temperature'],'.16g'),'ObserverMSE':f"{o['normal_partition_diagnostics']['check_scores']['components']['synchronized']['residual']['mean']:.6f}",'ARMSE':f"{c['selection']['ar']['selection_value']:.6f}",'AmbiguityPct':f"{100*o['normal_partition_diagnostics']['check_scores']['components']['synchronized']['ambiguous_fraction']['mean']:.2f}"}
 output['generated/values.tex']='% Generated from frozen aggregate artifacts. Do not edit.\n'+''.join('\\newcommand{\\'+k+'}{'+v+'}\n' for k,v in macros.items())
 # Three aligned horizontal panels; all methods, no error bars or tuned ranking.
 fig=[r'\begin{tikzpicture}',r'\begin{groupplot}[group style={group size=3 by 1,horizontal sep=0.65cm},width=0.29\textwidth,height=8cm,xbar,bar width=5pt,ymin=-0.7,ymax=10.7,ytick={0,...,10},yticklabels={'+','.join(methods)+r'},y dir=reverse,xmin=0,tick label style={font=\scriptsize},label style={font=\small},xmajorgrids=true,grid style={gray!20}]']
 for i,(title,get) in enumerate([(r'Point recall (\%)',lambda x:100*x['mixed']['recall']),(r'Normal alarms (\%)',lambda x:100*x['normal']['points']['point_exceedance']),(r'Normal episodes/h',lambda x:x['normal']['episodes_per_hour'])]):
  fig.append(r'\nextgroupplot[xlabel={'+title+'}'+('' if i==0 else ',yticklabels={}')+']')
  fig.append(r'\addplot[fill=blue!55,draw=blue!80!black] coordinates {'+' '.join(f'({get(data[n]):.10g},{j})' for j,n in enumerate(methods))+'};')
 fig += [r'\end{groupplot}',r'\end{tikzpicture}']
 output['figures/operating_tradeoffs.tex']='\n'.join(fig)+'\n'
 fig=[r'\begin{tikzpicture}',r'\begin{axis}[width=0.88\textwidth,height=5.5cm,ybar,bar width=7pt,xmin=0.4,xmax=8.6,ymin=0,xtick={1,...,8},xlabel={Scheduled event},ylabel={Positive observations alarmed (\%)},legend style={at={(0.5,1.02)},anchor=south,legend columns=2},ymajorgrids=true,grid style={gray!20},tick label style={font=\small}]']
 for name,color in [('O-R','gray'),('O-RC','blue')]:
  fig.append(r'\addplot[fill='+color+r'!55,draw='+color+r'!80!black] coordinates {'+' '.join(f"({j+1},{100*x['within_event_point_recall']:.10g})" for j,x in enumerate(events[name]))+'};')
 fig += [r'\legend{O-R,O-RC}',r'\end{axis}',r'\end{tikzpicture}']
 output['figures/event_point_coverage.tex']='\n'.join(fig)+'\n'
 refs=json.loads((ROOT/'editorial/references.json').read_text());bib=[];bb=[r'\begin{thebibliography}{99}']
 for x in refs:
  fields={'author':x['bibtex_author'],'title':'{'+x['title']+'}','year':x.get('year'),'journal' if x['type']=='article' else 'booktitle' if x['type']=='inproceedings' else 'howpublished':x['venue'],'volume':x.get('volume'),'number':x.get('number'),'pages':x.get('pages'),'doi':x.get('doi'),'url':x['url'],'note':x['version']}
  bib.append('@'+x['type']+'{'+x['key']+',\n'+',\n'.join('  '+k+' = {'+v+'}' for k,v in fields.items() if v)+'\n}\n')
  text=esc(', '.join(x['authors']))+'. '+esc(x['title'])+'. \\emph{'+esc(x['venue'])+'}'
  if x.get('volume'):text+=', '+esc(x['volume'])+('('+esc(x['number'])+')' if x.get('number') else '')
  if x.get('pages'):text+=', '+esc(x['pages'])
  if x.get('year'):text+=', '+x['year']
  text+='.'
  if x.get('doi'):text+=' DOI: \\href{https://doi.org/'+x['doi']+'}{\\nolinkurl{'+x['doi']+'}}.'
  text+=' \\url{'+x['url']+'}. '
  text+=esc(x['version'])+'.'
  bb.append('\\bibitem{'+x['key']+'} '+text)
 bb.append(r'\end{thebibliography}')
 output['references.bib']='\n'.join(bib)
 output['generated/references.tex']='\n\n'.join(bb)+'\n'
 assets={'kind':'deterministic_manuscript_asset_manifest','generator_sha256':sha(Path(__file__)),'source_manifest_sha256':sha(ROOT/'reproducibility/SOURCE_MANIFEST.json'),'reference_register_sha256':sha(ROOT/'editorial/references.json'),'inputs':{str(q.relative_to(ROOT)):sha(q) for q in sorted((ROOT/'reproducibility/inputs').glob('*.json'))},'assets':{name:hashlib.sha256(text.encode()).hexdigest() for name,text in output.items()},'raw_observations_used':False,'models_run':False,'figure_format':'PGFPlots source; PDF rendering deferred'}
 output['generated/ASSET_MANIFEST.json']=json.dumps(assets,indent=2)+'\n'
 for name,text in output.items():
  q=ROOT/name
  if a.check:assert q.exists() and q.read_text()==text,'Asset mismatch: '+name
  else:q.parent.mkdir(parents=True,exist_ok=True);q.write_text(text)
 print(json.dumps({'mode':'check' if a.check else 'build','assets':len(output),'methods':len(methods),'events':sum(map(len,events.values())),'raw_opened':False,'models_run':False}))
if __name__=='__main__':main()
