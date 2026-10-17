"""Post-exposure reporting only. Reads sealed results; never runs a detector."""
from pathlib import Path
import hashlib
import json
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RUN = PROJECT/'local/recovery_v0.7/runs/confirmation_001'
MAN = PROJECT/'manuscript_recovery_v0.7'
GEN = MAN/'generated'
FIG = MAN/'figures'
for p in (GEN, FIG): p.mkdir(parents=True, exist_ok=True)
read = lambda name: json.loads((RUN/(name+'.json')).read_text())
aggregate = read('aggregate'); outcomes = read('outcomes'); calibration = read('calibration')
summary = read('summary'); supervisor = read('supervisor')
rows = aggregate['rows']; pooled = [r for r in rows if r['stratum']=='pooled']
by = {r['method']: r for r in pooled}
methods = calibration['methods']
names = ['Persistence','AR(4)','ARX(4)','Following observer','Rolling mean (45)',
         'CUSUM','Fused point','Fused hysteresis','Mode hysteresis','Envelope point',
         'Envelope hysteresis','Fixed return','Envelope + fixed return',
         'No dwell','No noise margin','Reference entry only','Command reset',
         'Following hysteresis','Matched point','Matched hysteresis',
         'Matched no dwell','Matched no margin','Following entry only']
label = dict(zip(methods, names))
ids = dict(zip(methods, range(23)))
def table(name, headers, body, align):
    text = '\\begin{tabular}{'+align+'}\n\\toprule\n'+' & '.join(headers)+' \\\\\n\\midrule\n'
    text += ''.join(' & '.join(map(str, r))+' \\\\\n' for r in body)
    (GEN/(name+'.tex')).write_text(text+'\\bottomrule\n\\end{tabular}\n')

table('performance',['ID','Method','Precision','Recall','F1','AP'],
      [[ids[r['method']],label[r['method']]]+[f'{r[k]:.3f}' for k in ['precision','recall','f1','ap']] for r in pooled], 'rlrrrr')
table('burden',['ID','Benign points','Episodes/h','Overlap/fresh','Early clears','Clear / returned'],
      [[ids[r['method']],r['benign_alarms'],f"{r['benign_episodes_per_hour']:.1f}",
        f"{r['overlap_hits']}/{r['fresh_hits']}",r['premature_clear_events'],
        f"{r['cleared_within_five_seconds']}/{r['returned_detected_events']}"] for r in pooled], 'rrrrrr')
table('thresholds',['ID','Entry threshold','Calibration alarms','Threshold source'],
      [[j,f"{r['threshold']:.7g}",r['actual_normal_alarms'],
        {'unchanged_v0.6':'Retained','same_normal_population':'Old normal only',
         'matched_candidate_entry_diagnostic':'Matched ID 11'}[r['source']]] for j,r in enumerate(calibration['records'])], 'rrrl')
main = ['arx4','following_mean45','following_cusum','following_hysteresis','fused_hysteresis','mode_hysteresis','nominal_fixed_return']
table('main',['Method','Benign (\\%)','F1','Overlap/fresh','Early'],
      [[label[m],f"{100*by[m]['benign_fraction']:.2f}",f"{by[m]['f1']:.3f}",
        f"{by[m]['overlap_hits']}/{by[m]['fresh_hits']}",by[m]['premature_clear_events']] for m in main], 'lrrrr')
matched = ['nominal_fixed_return','matched_point','matched_hysteresis','matched_no_dwell','matched_no_margin']
table('matched',['Decision at same entry threshold','Benign points','Early clears','F1'],
      [[label[m],by[m]['benign_alarms'],by[m]['premature_clear_events'],f"{by[m]['f1']:.3f}"] for m in matched], 'lrrr')
groups = ['fused_hysteresis','mode_hysteresis','nominal_fixed_return','following_hysteresis']
table('strata',['Plant','Fused hyst.','Mode hyst.','Fixed return','Following hyst.'],
      [[p]+[str(next(r for r in rows if r['method']==m and r['stratum']==p)['benign_alarms']) for m in groups] for p in ['P1','P2','P3']], 'lrrrr')

event_summary = []
for m in methods:
    rr = [r for r in outcomes if r['method']==m and r['attack_present']]
    delays = [r['delay_steps']*.02 for r in rr if r['delay_steps'] is not None]
    fresh = [r['fresh_delay_steps']*.02 for r in rr if r['fresh_delay_steps'] is not None]
    clears = [r['clear_delay_from_return_seconds'] for r in rr if r['clear_delay_from_return_seconds'] is not None]
    event_summary.append(dict(method=m,events=len(rr),misses=sum(not r['overlap_hit'] for r in rr),
        fresh_misses=sum(not r['fresh_hit'] for r in rr),overlap_delay_median=float(np.median(delays)) if delays else None,
        overlap_delay_max=max(delays,default=None),fresh_delay_median=float(np.median(fresh)) if fresh else None,
        fresh_delay_max=max(fresh,default=None),clear_delay_max=max(clears,default=None),
        physical_return_missing=sum(r['physical_return_steps'] is None for r in rr),
        post_command_alarm_points=sum(r['post_alarm_points'] for r in rr),
        post_command_points=sum(r['post_points'] for r in rr)))
table('delay',['ID','Miss / no fresh','Overlap delay med/max (s)','Fresh delay med/max (s)','Clear max (s)'],
      [[j,f"{r['misses']}/{r['fresh_misses']}",f"{r['overlap_delay_median']:.2f}/{r['overlap_delay_max']:.2f}",
        f"{r['fresh_delay_median']:.2f}/{r['fresh_delay_max']:.2f}",f"{r['clear_delay_max']:.2f}" if r['clear_delay_max'] is not None else '--'] for j,r in enumerate(event_summary)], 'rrrrr')
(GEN/'event_summary.json').write_text(json.dumps(event_summary,indent=2)+'\n')
with (GEN/'all_outcomes.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=sorted(outcomes[0]));w.writeheader();w.writerows(outcomes)

# Exact paired equality, not inference from equal aggregate values.
equal=[]
for p in sorted(RUN.glob('eval_*.npz')):
    with np.load(p,allow_pickle=False) as a:
        equal.append(dict(episode=p.stem,alarms_identical=bool(np.array_equal(a['alarm'][:,11],a['alarm'][:,22])),
            unknown_identical=bool(np.array_equal(a['unknown'][:,11],a['unknown'][:,22]))))
(GEN/'entry_ablation_equality.json').write_text(json.dumps(dict(episodes=equal,
    all_equal=all(r['alarms_identical'] and r['unknown_identical'] for r in equal)),indent=2)+'\n')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,
                     'axes.spines.right':False,'figure.dpi':160,'savefig.bbox':'tight'})
colors=['#36658b','#3d8b79','#b47836','#685b9a','#65717a','#b44b52','#171f28']
fig,ax=plt.subplots(1,2,figsize=(9,3.7))
y=np.arange(len(main));ax[0].barh(y,[100*by[m]['benign_fraction'] for m in main],color=colors)
ax[0].set_yticks(y,[label[m] for m in main]);ax[0].invert_yaxis();ax[0].set_xlabel('Benign alarm points (%)')
ax[1].barh(y,[by[m]['premature_clear_events'] for m in main],color=colors)
ax[1].set_yticks(y,[]);ax[1].invert_yaxis();ax[1].set_xlabel('Events with premature clearing / 90')
ax[1].set_xlim(0,95);fig.tight_layout()
for ext in ['pdf','png']:fig.savefig(FIG/('tradeoff.'+ext))
plt.close(fig)
fig,ax=plt.subplots(figsize=(8,3.4));x=np.arange(3);width=.19
for j,m in enumerate(groups):
    vals=[100*next(r for r in rows if r['method']==m and r['stratum']==p)['benign_fraction'] for p in ['P1','P2','P3']]
    ax.bar(x+(j-1.5)*width,vals,width,label=label[m])
ax.set_xticks(x,['P1: no lag','P2: 40 ms lag','P3: 80 ms lag + noise'])
ax.set_ylabel('Benign alarm points (%)');ax.legend(ncol=2,fontsize=8);fig.tight_layout()
for ext in ['pdf','png']:fig.savefig(FIG/('plant_strata.'+ext))
plt.close(fig)
fig,ax=plt.subplots(1,2,figsize=(8.5,3.1));y=np.arange(len(matched))
ax[0].barh(y,[by[m]['benign_alarms'] for m in matched],color='#36658b')
ax[0].set_yticks(y,[label[m] for m in matched]);ax[0].invert_yaxis();ax[0].set_xlabel('Benign alarm points / 59,400')
ax[1].barh(y,[by[m]['premature_clear_events'] for m in matched],color='#b47836')
ax[1].set_yticks(y,[]);ax[1].invert_yaxis();ax[1].set_xlabel('Premature-clear events / 90');fig.tight_layout()
for ext in ['pdf','png']:fig.savefig(FIG/('matched_entry.'+ext))
plt.close(fig)

table('costs',['Component','Measured time (s)'],[[k.replace('_',' '),f'{v:.3f}'] for k,v in summary['costs'].items() if k!='decision_seconds'], 'lr')
table('decision_cost',['ID','Decision replay total (ms)'],[[j,f'{v*1000:.3f}'] for j,v in enumerate(summary['costs']['decision_seconds'])], 'rr')
values={'Wall':f"{supervisor['wall_seconds']:.3f}",'CPU':f"{summary['usage']['process_cpu_seconds']:.3f}",
        'RSS':f"{summary['usage']['peak_rss_bytes']/2**20:.2f}",'Output':f"{supervisor['output_bytes']/2**20:.2f}",
        'CandidateThreshold':f"{calibration['records'][11]['threshold']:.7g}",
        'RelativeIncrease':f"{-100*aggregate['primary_test']['comparisons']['fused_hysteresis']['reduction']:.2f}"}
(GEN/'values.tex').write_text(''.join('\\newcommand{\\'+k+'}{'+v+'}\n' for k,v in values.items()))
(HERE/'AGGREGATE.json').write_text(json.dumps(aggregate,indent=2)+'\n')
for name in ['summary','supervisor','calibration']:
    (HERE/(name.upper()+'.json')).write_text(json.dumps(read(name),indent=2)+'\n')
md='# Complete frozen v0.7 results\n\nAll observations are synthetic; outcomes are descriptive, paired and dependent.\n\n'
for stratum in ['pooled','P1','P2','P3']:
    md+='## '+stratum+'\n\n| Method | P/R/F1/AP | Benign alarm points | Episodes/h | Overlap / fresh | Early clear | Clear / returned |\n|---|---|---:|---:|---:|---:|---:|\n'
    for r in rows:
        if r['stratum']==stratum:
            md+=f"| {r['method']} | "+'/'.join(f'{r[k]:.4f}' for k in ['precision','recall','f1','ap'])+f" | {r['benign_alarms']}/{r['benign_points']} | {r['benign_episodes_per_hour']:.2f} | {r['overlap_hits']}/{r['fresh_hits']} | {r['premature_clear_events']} | {r['cleared_within_five_seconds']}/{r['returned_detected_events']} |\n"
    md+='\n'
(HERE/'TABLES.md').write_text(md)
hashes={str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [RUN/(n+'.json') for n in ['aggregate','outcomes','summary','supervisor','calibration']]}
(GEN/'SOURCE_IDENTITIES.json').write_text(json.dumps(dict(source_sha256=hashes,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    reporting_scope='Post-exposure presentation; no refitting, recalibration or reselection',numpy=np.__version__,matplotlib=matplotlib.__version__),indent=2)+'\n')
print(json.dumps(dict(methods=len(methods),outcomes=len(outcomes),figures=3,exact_entry_ablation_equality=all(r['alarms_identical'] for r in equal))))
