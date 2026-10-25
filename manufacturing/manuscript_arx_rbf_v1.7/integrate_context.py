"""Render the jointly released v0.19 campaign from saved results, no fitting."""
from pathlib import Path
import hashlib,json,os
M=Path(__file__).resolve().parent;P=M.parent;R=P/'local/context_recovery_v0.19/final_001';S=P/'research_cycles/context_recovery_v0.19'
cache=P/'local/manuscript_arx_rbf_v1.7/plot_cache';cache.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(cache);os.environ['XDG_CACHE_HOME']=str(cache)
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((R/'results.json').read_text());assert d['episodes']==216 and d['outcomes']==2376 and d['primary']['passed']==False
rows={x['method']:x for x in d['summary'] if x['group']=='pooled'}
labels={'base_dual':'Base dual','base_dual_nodwell':'Base no dwell','rbf_dual':'RBF dual','rbf_dual_nodwell':'RBF no dwell','following_point':'Following point','tolerance_point':'Tolerance point','entry_3of5':'Three-of-five','global_set':'Global interval','context_point':'Context point','context_hysteresis':'Context hysteresis','context_set':'Context interval'}
lines=[r'\begin{tabular}{lrrrrrrrr}\toprule',r'Method & Benign (\%) & Starts/h & Fresh & Fresh p95 & Outside inactive & Joint & Clear med./p95 & F1\\\midrule']
for m,r in rows.items():
 delay=r['clearance_delay'];lines.append(f"{labels[m]} & {100*r['occupancy']:.3f} & {r['starts_per_hour']:.1f} & {r['fresh']} & {r['fresh_delay']['p95']:.3f} & {r['outside_inactive']:,} & {r['joint']} & {delay['median']:.2f}/{delay['p95']:.2f} & {r['f1']:.3f} \\\\")
lines.append(r'\bottomrule\end{tabular}');(M/'generated/context_final.tex').write_text('\n'.join(lines)+'\n')
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
methods=['base_dual','base_dual_nodwell','global_set','context_hysteresis','context_set'];ticks=['Base\ndual','Base\nno dwell','Global\ninterval','Context\nhysteresis','Context\ninterval'];cols=['#426981','#849faa','#8d8985','#c99e77','#b56531']
fig,axs=plt.subplots(1,3,figsize=(10.5,2.6),constrained_layout=True)
for ax,key,scale,label in zip(axs,['occupancy','outside_inactive','fresh_delay'],[100,100/66357,1],['Benign alarm occupancy (%)','Outside-tolerance inactive (%)','Fresh detection p95 (s)']):
 vals=[rows[m][key]['p95'] if key=='fresh_delay' else rows[m][key]*scale for m in methods]
 ax.bar(range(5),vals,color=cols)
 for i,v in enumerate(vals):ax.text(i,v+(max(vals)*.025),f'{v:.2f}' if v>=.01 else f'{v:.4f}',ha='center',fontsize=8)
 ax.set_xticks(range(5),ticks,fontsize=8);ax.set_ylabel(label);ax.set_ylim(0,max(vals)*1.22);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
axs[2].axhline(rows['base_dual']['fresh_delay']['p95']+.2,color='#9b3030',ls='--',lw=1);axs[2].text(-.4,.265,'Declared delay ceiling',fontsize=7,color='#9b3030')
fig.savefig(M/'figures/context_final.pdf');plt.close(fig)
receipt_path=M/'NEW_EVIDENCE_ASSETS.json';rec=json.loads(receipt_path.read_text());rec['scope']='Exposed-data v0.18 diagnosis and prospectively frozen v0.19 within-simulator evaluation'
for f in [R/'results.json',P/'local/context_recovery_v0.19/development_001/selected.json',S/'FINAL_FREEZE.json',M/'generated/context_final.tex',M/'figures/context_final.pdf',Path(__file__).resolve()]:rec['sha256'][str(f.relative_to(P))]=sha(f)
receipt_path.write_text(json.dumps(rec,indent=2)+'\n')
print('Generated all11method final table and prospective outcome figure')
