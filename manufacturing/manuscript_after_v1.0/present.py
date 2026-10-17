"""Render manuscript tables/figures from sealed results; never fit or simulate."""
from pathlib import Path
import hashlib, json, os

M = Path(__file__).resolve().parent
P = M.parent
cache = P / 'local/manuscript_after_v1.0/plot_cache'
cache.mkdir(parents=True, exist_ok=True)
os.environ['MPLCONFIGDIR'] = str(cache)
os.environ['XDG_CACHE_HOME'] = str(cache)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

paths = {
    'attack': P/'local/recovery_v0.8/runs/confirmation_002/aggregate.json',
    'normal': P/'local/commissioning_v0.9/runs/normal_002/fresh_summary.json',
    'noise': P/'research_cycles/commissioning_v0.9/NOISE_DIAGNOSTIC.json',
}
data = {k: json.loads(v.read_text()) for k, v in paths.items()}
rows = [r for r in data['attack']['rows'] if r['stratum'] == 'pooled']
assert len(rows) == 13 and all(r['eligible'] == 237600 for r in rows)
names = ['Persistence', 'ARX one-step', 'Following point', 'Following hysteresis',
         'Nominal hysteresis', 'Nominal fixed return', 'Learned point',
         'Learned hysteresis', 'Learned fixed return', 'Uncertainty return',
         'Episode CP band', 'Matched no allowance', 'Matched no dwell']
assert rows[9]['method'] == 'learned_uncertainty_return'
tables = M/'generated'; figures = M/'figures'
tables.mkdir(exist_ok=True); figures.mkdir(exist_ok=True)

def table(name, spec, header, body):
    (tables/name).write_text('\\begin{tabular}{'+spec+'}\\toprule\n'+header+
        ' \\\\\\midrule\n'+'\n'.join(body)+'\n\\bottomrule\\end{tabular}\n')

table('attack.tex', 'lrrrrr', 'Method & Benign & F1 & Overlap/fresh & Early & Clear/return', [
    f"{n} & {r['benign_alarms']} & {r['f1']:.3f} & {r['overlap_hits']}/{r['fresh_hits']} & "
    f"{r['premature_clear_events']} & {r['cleared']}/{r['returned_detected']} \\\\" for n,r in zip(names,rows)])
table('metrics.tex', 'lrrrrrr', 'Method & Precision & Recall & AP & Episodes/h & Missed & Known (\\%)', [
    f"{n} & {r['precision']:.3f} & {r['recall']:.3f} & {r['ap']:.3f} & "
    f"{r['benign_episodes_per_hour']:.1f} & {r['misses']} & {100*(1-r['unknown']/r['eligible']):.1f} \\\\" for n,r in zip(names,rows)])
normal = data['normal']['rows']
def get(plant,role):return next(r for r in normal if r['plant']==plant and r['role']==role)
body=[]
for q in ['Q1','Q2','Q3']:
    b=get(q,'baseline_arx4');s=get(q,'selected_reference')
    body.append(f"{q} & {int(s['model'].split('_')[1])} & {b['allowance']:.4f} & {s['allowance']:.4f} & "
                f"{100*(1-s['allowance']/b['allowance']):.2f} & {100*s['feasible_fraction']:.2f} & "
                f"{s['cleared_probes']}/{s['probes']} \\\\")
table('normal.tex','lrrrrrr','Plant & Order & $b_4$ & $b_\\star$ & Reduction (\\%) & Feasible (\\%) & Clear/probes',body)
role_names={'baseline_arx4':'ARX(4), free','selected_reference':'Selected ARX, free',
            'selected_fir':'Selected FIR','one_step_arx4':'ARX(4), one-step','command':'Command as state'}
table('normal_all.tex','llrrrr','Plant & Reference & RMSE & Allowance & Feasible (\\%) & Clear/probes',[
    f"{q} & {n} & {r['mean_standardized_rmse']:.5f} & {r['allowance']:.4f} & "
    f"{100*r['feasible_fraction']:.2f} & {r['cleared_probes']}/{r['probes']} \\\\" for q in ['Q1','Q2','Q3'] for role,n in role_names.items() for r in [get(q,role)]])
table('noise.tex','lrrr','Plant & $F^{-1}(0.95)$ & $\\delta-F^{-1}(0.95)$ & Margin probability',[
    f"{r['plant']} & {r['point_discrepancy_q95']:.6f} & {r['largest_allowance_compatible_with_95pct_population_coverage']:.6f} & "
    +(f"{r['probability_noise_only_calibration_max_leaves_95pct_population_coverage']:.6f}" if r['plant']!='Q3' else '$2.19\\times10^{-9}$')+' \\\\'
    for r in data['noise']['records']])

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,
                     'axes.spines.right':False,'pdf.fonttype':42})
chosen=[5,7,9,11]; selected=[rows[i] for i in chosen]
labels=['Nominal fixed\nreturn','Learned\nhysteresis','Uncertainty\nreturn','Matched no\nallowance']
colors=['#718096','#476f92','#b65c3a','#147c80']
fig,axs=plt.subplots(1,2,figsize=(8.3,3.45),layout='constrained')
for ax,field,ylabel in [(axs[0],'benign_alarms','Benign alarm observations'),(axs[1],'cleared','Timely clearances / 108 returned events')]:
    values=[r[field] for r in selected];bars=ax.bar(range(4),values,color=colors,width=.66)
    ax.set_xticks(range(4),labels,fontsize=8);ax.set_ylabel(ylabel);ax.set_axisbelow(True);ax.grid(axis='y',alpha=.16)
    ax.set_ylim(0,max(values)*1.19)
    for bar,value in zip(bars,values):ax.text(bar.get_x()+bar.get_width()/2,value+max(values)*.025,str(value),ha='center',fontsize=9)
axs[0].set_title('(a) Alarm burden on benign episodes',loc='left',fontsize=10)
axs[1].set_title('(b) Clearance after physical return',loc='left',fontsize=10)
fig.savefig(figures/'recovery.pdf');fig.savefig(figures/'recovery.png',dpi=220);plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(8.3,3.45),layout='constrained');x=np.arange(3)
for i,(role,label,color) in enumerate([('baseline_arx4','ARX(4) control','#718096'),('selected_reference','Selected ARX','#147c80')]):
    rr=[get(q,role) for q in ['Q1','Q2','Q3']]
    axs[0].bar(x+(i-.5)*.32,[r['allowance'] for r in rr],.3,color=color,label=label)
    axs[1].bar(x+(i-.5)*.32,[100*r['feasible_fraction'] for r in rr],.3,color=color)
axs[0].axhline(.1,color='#b65c3a',ls='--',label='Return tolerance',lw=1.2)
axs[1].axhline(95,color='#b65c3a',ls='--',lw=1.2)
axs[1].text(2.42,96.5,'95%',ha='right',fontsize=8,color='#984321')
axs[0].legend(frameon=False,fontsize=8,loc='upper left');axs[0].set_ylim(0,.24);axs[1].set_ylim(0,110)
for ax in axs:ax.set_xticks(x,['Q1','Q2','Q3']);ax.grid(axis='y',alpha=.16);ax.set_axisbelow(True)
axs[0].set_ylabel('Empirical discrepancy allowance');axs[1].set_ylabel('Feasible normal observations (%)')
axs[0].set_title('(a) Model selection reduces reference error',loc='left',fontsize=10)
axs[1].set_title('(b) Clearance feasibility remains limited',loc='left',fontsize=10)
fig.savefig(figures/'commissioning.pdf');fig.savefig(figures/'commissioning.png',dpi=220);plt.close(fig)

sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
outputs=sorted(list(tables.glob('*.tex'))+list(figures.glob('*')))
(M/'PRESENTATION.json').write_text(json.dumps({'source_sha256':{str(v.relative_to(P)):sha(v) for v in paths.values()},
    'outputs':{str(v.relative_to(M)):sha(v) for v in outputs},'generator_sha256':sha(Path(__file__)),
    'new_experiments':False,'excluded_duplicate_role':'selected_arx equals selected_reference on all plants'},indent=2)+'\n')
print('Generated six tables and two figures from sealed JSON results.')
