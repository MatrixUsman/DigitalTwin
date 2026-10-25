"""Render descriptive v0.18 results only from preserved saved outputs."""
from pathlib import Path
import hashlib,json,os
cache=Path(__file__).resolve().parent.parent/'local/manuscript_arx_rbf_v1.7/plot_cache'
cache.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(cache);os.environ['XDG_CACHE_HOME']=str(cache)
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
M=Path(__file__).resolve().parent;P=M.parent;S=P/'research_cycles/review_extension_v0.18'
r=json.loads((S/'REPORTING.json').read_text());rows={x['method']:x for x in r['pooled']}
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for f,h in r['source_sha256'].items():assert sha(P/f)==h
methods=['base_point','base_dual','base_dual_nodwell','rbf_point','rbf_dual','rbf_dual_nodwell']
names={'base_point':'Base point','base_dual':'Base dual','base_dual_nodwell':'Base no dwell','rbf_point':'RBF point','rbf_dual':'RBF dual','rbf_dual_nodwell':'RBF no dwell'}
lines=[r'\begin{tabular}{lrrrrrrr}\toprule',r'Method & Occupancy (\%) & Starts/h & Run med./p95 & Fresh & Detect med./p95 & Clear med./p95 & Gaps\\\midrule']
def timing(d):return '--' if d['n']==0 else f"{d['median']:.2f}/{d['p95']:.2f}"
for m in methods:
 d=rows[m];lines.append(f"{names[m]} & {100*d['benign_fraction']:.3f} & {d['benign_starts_per_hour']:.1f} & {timing(d['benign_alarm_duration_seconds'])} & {d['fresh_hits']}/108 & {timing(d['detection_delay_seconds'])} & {timing(d['clearance_delay_seconds'])} & {d['gap_points']} \\\\")
lines.append(r'\bottomrule\end{tabular}');(M/'generated/matched_review.tex').write_text('\n'.join(lines)+'\n')
# All-method timing table preserves non-detections and conditional denominators.
labels={m:m.replace('_',' ') for m in rows};labels.update(names)
lines=[r'\begin{tabular}{lrrrrrr}\toprule',r'Method & Misses & Detect med./p95 & Clear med./p95 & Already off & Censored & Outside inactive\\\midrule']
for m,d in rows.items():
 lines.append(f"{labels[m]} & {d['misses']} & {timing(d['detection_delay_seconds'])} & {timing(d['clearance_delay_seconds'])} & {d['already_inactive_at_return']} & {d['clearance_censored']} & {d['outside_inactive_after_detection_points']:,} \\\\")
lines.append(r'\bottomrule\end{tabular}');(M/'generated/timing_review.tex').write_text('\n'.join(lines)+'\n')
strata={(d['group'],d['stratum'],d['method']):d for d in r['strata']}
lines=[r'\begin{tabular}{lrrrr}\toprule',r'Stratum & Benign B/R & Starts/h B/R & Detect p95 B/R & Clear p95 B/R\\\midrule']
for group,vals in [('plant',['Q1','Q2','Q3']),('task',['N14','O14','P14']),('condition',['brief_offset','persistent_offset','hold','slow'])]:
 for val in vals:
  a,b=[strata[group,val,m] for m in ['base_dual_nodwell','rbf_dual_nodwell']]
  benign=f"{a['benign_alarms']}/{b['benign_alarms']}" if a['benign_points'] else '--'
  starts=f"{a['benign_starts_per_hour']:.1f}/{b['benign_starts_per_hour']:.1f}" if a['benign_points'] else '--'
  lines.append(f"{val.replace('_',' ')} & {benign} & {starts} & {a['detection_delay_seconds']['p95']:.2f}/{b['detection_delay_seconds']['p95']:.2f} & {a['clearance_delay_seconds']['p95']:.2f}/{b['clearance_delay_seconds']['p95']:.2f} \\\\")
lines.append(r'\bottomrule\end{tabular}');(M/'generated/strata_review.tex').write_text('\n'.join(lines)+'\n')
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
fig,axs=plt.subplots(1,2,figsize=(10.4,2.65),constrained_layout=True)
mm=['base_dual','base_dual_nodwell','rbf_dual','rbf_dual_nodwell'];x=np.arange(4)
parts=[]
for key in ['score_exceedances','retained_with_clearance_evidence','retained_without_clearance_evidence']:
 parts.append([sum(d[key] for d in r['diagnostics'] if d['method']==m) for m in mm])
bottom=np.zeros(4)
for values,col,label in zip(parts,['#426981','#c0814b','#9ba8aa'],['Entry exceedance','Dwell while evidence passes','Clearance evidence fails']):
 axs[0].bar(x,values,bottom=bottom,color=col,label=label);bottom+=values
for i,v in enumerate(bottom):axs[0].text(i,v+70,f'{int(v):,}',ha='center',fontsize=9)
for i,m in enumerate(mm):
 val=rows[m]['benign_starts_per_hour'];axs[1].bar(i,val,color='#426981' if 'base' in m else '#c0814b');axs[1].text(i,val+20,f'{val:.0f}',ha='center',fontsize=9)
for ax in axs:ax.set_xticks(x,['Base\ndwell10','Base\ndwell1','RBF\ndwell10','RBF\ndwell1']);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
axs[0].set_ylim(0,9200);axs[0].set_ylabel('Benign alarm points');axs[0].legend(fontsize=7,loc='upper right');axs[1].set_ylim(0,1830);axs[1].set_ylabel('Alarm starts / eligible benign hour')
fig.savefig(M/'figures/matched_review.pdf');plt.close(fig)
assets=[M/'generated/matched_review.tex',M/'generated/timing_review.tex',M/'generated/strata_review.tex',M/'figures/matched_review.pdf',S/'REPORTING.json',S/'VERIFICATION.json',S/'PACKAGE_MANIFEST.json',Path(__file__).resolve()]
receipt={'scope':'Exposed-data diagnostic extension; no fresh confirmation','sha256':{str(f.relative_to(P)):sha(f) for f in assets}}
(M/'NEW_EVIDENCE_ASSETS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Generated matched, timing and strata tables plus diagnostic figure')
