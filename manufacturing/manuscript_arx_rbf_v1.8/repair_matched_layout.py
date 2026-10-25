"""Replot unchanged saved v0.18 values with an unobstructed legend."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, os
M=Path(__file__).resolve().parent; P=M.parent
cache=P/'local/manuscript_arx_rbf_v1.8/plot_cache'
os.environ['MPLCONFIGDIR']=str(cache);os.environ['XDG_CACHE_HOME']=str(cache)
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
source=P/'research_cycles/review_extension_v0.18/REPORTING.json'
r=json.loads(source.read_text());rows={d['method']:d for d in r['pooled']}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for path,digest in r['source_sha256'].items():assert sha(P/path)==digest
methods=['base_dual','base_dual_nodwell','rbf_dual','rbf_dual_nodwell']
keys=['score_exceedances','retained_with_clearance_evidence','retained_without_clearance_evidence']
parts=[[sum(d[key] for d in r['diagnostics'] if d['method']==m) for m in methods] for key in keys]
totals=np.sum(parts,axis=0)
assert totals.tolist()==[7156,1198,7012,1195]
starts=[rows[m]['benign_starts_per_hour'] for m in methods]
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
fig,axs=plt.subplots(1,2,figsize=(10.4,2.65))
fig.subplots_adjust(left=.075,right=.99,bottom=.22,top=.79,wspace=.28)
x=np.arange(4);bottom=np.zeros(4)
for values,color,label in zip(parts,['#426981','#c0814b','#9ba8aa'],['Entry exceedance','Dwell while evidence passes','Clearance evidence fails']):
    axs[0].bar(x,values,bottom=bottom,color=color,label=label);bottom+=values
for i,value in enumerate(totals):axs[0].text(i,value+70,f'{int(value):,}',ha='center',fontsize=10)
for i,(method,value) in enumerate(zip(methods,starts)):
    axs[1].bar(i,value,color='#426981' if 'base' in method else '#c0814b')
    axs[1].text(i,value+20,f'{value:.0f}',ha='center',fontsize=10)
for ax in axs:
    ax.set_xticks(x,['Base\ndwell10','Base\ndwell1','RBF\ndwell10','RBF\ndwell1'])
    ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
axs[0].set_ylim(0,9200);axs[0].set_ylabel('Benign alarm points')
axs[1].set_ylim(0,1830);axs[1].set_ylabel('Benign alarm starts / h')
handles,labels=axs[0].get_legend_handles_labels()
fig.legend(handles,labels,loc='upper center',ncol=3,fontsize=10,frameon=False,bbox_to_anchor=(.5,1.01))
target=M/'figures/matched_review.pdf';fig.savefig(target);plt.close(fig)
receipt={'utc':datetime.now(timezone.utc).isoformat(),
 'classification':'layout-only replot from unchanged saved v0.18 summary; no fitting, new data or changed values',
 'command':'.venv-plots-v03/bin/python manuscript_arx_rbf_v1.8/repair_matched_layout.py','cwd':str(P),
 'methods':methods,'parts':dict(zip(keys,parts)),'totals':totals.tolist(),'starts_per_hour':starts,
 'layout_change':'legend above panels; shorter axis label with identical hourly denominator; same figure canvas dimensions',
 'sha256':{str(p.relative_to(P)):sha(p) for p in [source,target,Path(__file__).resolve(),P/'manuscript_arx_rbf_v1.7/figures/matched_review.pdf']}}
(M/'MATCHED_LAYOUT_REPAIR.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Preserved all 16 plotted values and hourly denominators; moved obstructing legend.')
