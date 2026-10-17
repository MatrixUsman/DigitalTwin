"""Report all frozen outcomes and explicitly labelled post-study diagnostics."""
import os,json,csv,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2];cache=root/'local/attack_audit_v0.14/plot_cache';cache.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(cache);os.environ['XDG_CACHE_HOME']=str(cache)
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io14 import HERE,RUN,MODELS,check,sha,load_npz

f=check();c=f['configuration'];v=json.loads((HERE/'VERIFICATION.json').read_text())
for name,h in v['run_sha256'].items():
    if sha(RUN/name)!=h:raise ValueError('Changed verified output '+name)
s=json.loads((RUN/'summary.json').read_text());sup=json.loads((RUN/'supervisor.json').read_text())
rows=json.loads((RUN/'outcomes.json').read_text());catalog=json.loads((RUN/'catalog.json').read_text());cal=json.loads((RUN/'calibration.json').read_text())
pooled={r['method']:r for r in s['rows'] if r['stratum']=='pooled'}
checks={'label':'post-study descriptive diagnostics; not a changed primary criterion','alarm_array_differences':{},'early_falls':[]}
for pair in [('base_dual','base_long'),('rbf_dual','rbf_long')]:checks['alarm_array_differences'][' vs '.join(pair)]=0
rowmap={(r['id'],r['method']):r for r in rows};scales={p:load_npz(MODELS/f'base_{p}.npz')['scale'] for p in ['Q1','Q2','Q3']}
for item in catalog:
    z=load_npz(RUN/('score_'+item['id']+'.npz'));t=load_npz(RUN/('truth_'+item['id']+'.npz'))
    for pair in [('base_dual','base_long'),('rbf_dual','rbf_long')]:
        checks['alarm_array_differences'][' vs '.join(pair)]+=int(np.count_nonzero(z['alarms'][:,c['methods'].index(pair[0])]!=z['alarms'][:,c['methods'].index(pair[1])]))
    positive=np.flatnonzero(t['attack'])
    if not len(positive):continue
    begin,end=int(positive[0]),int(positive[-1])+1
    distance=np.max(np.abs((t['state']-t['counterfactual'])/scales[item['plant']]),axis=1)
    for j,method in enumerate(c['methods']):
        r=rowmap[item['id'],method];a=z['alarms'][:,j];hits=np.flatnonzero(a[begin:end])
        if not len(hits):continue
        first=begin+int(hits[0]);stop=r['physical_return'] if r['physical_return'] is not None else len(a)
        falls=np.flatnonzero(a[:-1]&~a[1:])+1
        for k in falls[(falls>first)&(falls<stop)]:
            checks['early_falls'].append(dict(id=item['id'],method=method,index=int(k),seconds=float(k*.02),
                true_distance=float(distance[k]),outside_tolerance=bool(distance[k]>.1),attack_active=bool(t['attack'][k]),preexisting_at_onset=bool(a[begin-1])))
outside={m:len({r['id'] for r in checks['early_falls'] if r['method']==m and r['outside_tolerance']}) for m in c['methods']}
checks['events_with_early_fall_outside_tolerance']=outside
(HERE/'DESCRIPTIVE_DIAGNOSTICS.json').write_text(json.dumps(checks,indent=2)+'\n')
with (HERE/'summary.csv').open('w',newline='') as out:
    w=csv.DictWriter(out,fieldnames=list(s['rows'][0]));w.writeheader();w.writerows(s['rows'])
with (HERE/'events.csv').open('w',newline='') as out:
    rr=[r for r in rows if r['event']];fields=sorted(set().union(*(r.keys() for r in rr)))
    w=csv.DictWriter(out,fieldnames=fields);w.writeheader();w.writerows(rr)
breakdown=[]
for key in ['task','condition']:
    for value in sorted({r[key] for r in rows}):
        for method in c['methods']:
            rr=[r for r in rows if r[key]==value and r['method']==method];events=[r for r in rr if r['event']]
            tp,fp,fn=[sum(r[k] for r in rr) for k in ['tp','fp','fn']]
            breakdown.append(dict(group=key,value=value,method=method,episodes=len(rr),tp=tp,fp=fp,fn=fn,
              f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None,events=len(events),hits=sum(r['overlap'] for r in events),
              fresh_hits=sum(r['fresh'] for r in events),premature=sum(r['premature'] for r in events),
              gap_points=sum(r['gap_points'] or 0 for r in events),clear_timely=sum(r['clear_timely'] for r in events),
              benign_points=sum(r['eligible'] for r in rr if r['benign']),benign_alarms=sum(r['alarm_points'] for r in rr if r['benign'])))
with (HERE/'strata.csv').open('w',newline='') as out:
    w=csv.DictWriter(out,fieldnames=list(breakdown[0]));w.writeheader();w.writerows(breakdown)
lines=['# Attack and recovery audit: results','', '## Material Passport','',
 '- Project: manufacturing. Operator: Codex, at the user’s explicit request. Date: 17 October 2026 (Asia/Karachi).',
 '- Material: frozen, bounded synthetic experiment using saved models; no retraining or CASPER raw-data access.',
 '- Verification: deterministic saved inference replay and separate metric arithmetic; not an independent real-robot replication.',
 '', '## Decision','',
 '**The candidate did not meet the declared attack/recovery advantage criterion.** The nonlinear RBF correction reduced pooled benign occupancy by 2.01%, below the required 10%, and increased the registered pre-return gap count from two points to three. Q1 benign occupancy worsened. The primary conclusion remains unchanged despite favorable secondary comparisons.',
 '', 'There is a useful measured contrast: a protected command-driven reference retains evidence much better than a one-step-following reference. The ordinary base reference achieves that benefit too. It does not establish a distinct contribution from the nonlinear correction, short window or dwell counter.',
 '', '## Complete main comparison','',
 'All rows have 207,900 eligible points, including 89,100 wholly benign points and 108 attack events. The schedule-positive population is 25,002 points. There is complete eligible coverage. F1 and AP use unadjusted corruption-schedule labels; post-corruption alarm retention may reduce precision. The separate recovery columns answer a different question.',
 '', '| Method | F1 | AP | Benign alarm points | Overlap / fresh hits | Early-clear events | Pre-return gap points | Timely clears / detected-returned |',
 '|---|---:|---:|---:|---:|---:|---:|---:|']
for method in c['methods']:
    r=pooled[method];lines.append(f'| {method} | {r["f1"]:.4f} | {r["average_precision"]:.4f} | {r["benign_alarms"]:,} | {r["hits"]} / {r["fresh_hits"]} | {r["premature"]} | {r["gap_points"]:,} | {r["clear_timely"]} / {r["returned_detected"]} |')
lines+=['','Continuous scores are shared across the return-rule variants, so their AP values are identical by construction. AP does not score the retained alarm state. Misses are visible in the hit counts: persistence misses41events and mean21 misses60. Their clearance denominator excludes those misses and must not be described as overall success.',
 '', '## What each component contributed','',
 '| Contrast | Measured finding | Interpretation |','|---|---|---|',
 '| RBF dual vs base dual | Same108overlap hits and one early-clear event; benign points7,156→7,012; gap points2→3 | The nonlinear correction provides no worthwhile overall advantage under the frozen criterion. |',
 '| RBF dual vs RBF long | Exactly0different alarm entries across all189episodes | The short-window component contributes nothing to these outputs. This is empirical equality, not a theorem for every input. |',
 '| RBF dual vs no-dwell | Benign points7,012→1,195; same108hits and one registered early-clear event; timely clear108/108for both | Dwell is costly in these conditions. The two early-clear events occur on different episodes; matching counts do not imply identical behavior. |',
 '| Base dual vs following dual | Early-clear events1→90; gaps2→2,970; following F10.7070 vs base0.6381 | Following is stronger on schedule F1 but loses sustained evidence more often. Neither metric alone establishes overall superiority. |',
 '| Following point vs RBF dual | F10.9202 vs0.6407; early-clear events108vs1 | High schedule detection performance can coexist with poor retained evidence under this recovery objective. |',
 '| Base CUSUM |108hits, no pre-return gaps,0/108timely clearances | Accumulated evidence retains alarms but does not clear within the declared horizon. |',
 '', '## Plant strata for the primary comparison','',
 '| Plant | Base / RBF benign points | Base / RBF pre-return gaps | Base / RBF fresh hits |', '|---|---:|---:|---:|']
for p in ['Q1','Q2','Q3']:
    d={r['method']:r for r in s['rows'] if r['stratum']==p};a=d['base_dual'];b=d['rbf_dual']
    lines.append(f'| {p} | {a["benign_alarms"]} / {b["benign_alarms"]} | {a["gap_points"]} / {b["gap_points"]} | {a["fresh_hits"]} / {b["fresh_hits"]} |')
lines+=['','Complete plant summaries, all task/condition strata and every event—including misses and conditional delays—are in `summary.csv`, `strata.csv` and `events.csv`. No favorable stratum replaces the primary all-plant requirement.',
 '', '## Meaning of “early clear”','',
 'The registered metric counts an alarm falling after the first overlap and before a stable post-corruption return. It includes a preexisting benign alarm that overlaps onset and then falls before a fresh detection. It is stricter than asking whether the physical deviation exceeds tolerance at the falling edge.',
 '', 'For the RBF candidate, the one registered event is N14/Q2/seed42/slow. Its alarm falls at index349, only two samples after onset347, with true standardized deviation0.0164868—below0.1. A new alarm starts at index352. This is an early continuity break under the registered criterion; it is not evidence that the robot was outside tolerance at that instant. The base control has two gap points in the same episode; the candidate has three. Do not inflate that one-point difference into a major safety finding.',
 '', 'A post-study diagnostic evaluates every early falling edge against truth at that instant. It is labelled exploratory and does not replace the primary result:',
 '', '| Method | Events with an early fall while true deviation exceeds0.1 |', '|---|---:|']
for method in c['methods']:lines.append(f'| {method} | {outside[method]} |')
lines+=['','The evaluator can compute the counterfactual state because this is simulation. The monitor cannot. No physical safety guarantee or real-world attack detection result follows. A second plot illustrates the registered protected/following contrast for the first task,Q2,seed17,persistent offset; this is a post-study illustration, not an additional independent experiment.',
 '', '## Calibration, provenance and cost','',
 'Saved base/linear/RBF fits and thresholds were unchanged. New controls used the same five old normal calibration episodes per plant, rank5,445 of5,500, and strict exceedance. The CUSUM reference statistic used training only. No model, gate or threshold was chosen using these attacks. Equal point quantiles do not equalize stateful alarm occupancy; calibration burdens are preserved in calibration.json.',
 '', f'The single run completed in {sup["wall_seconds"]:.3f}s wall and {s["usage"]["process_cpu_seconds"]:.3f}s worker CPU. Sampled peak RSS was {sup["sampled_peak_rss_bytes"]/2**20:.2f}MiB; worker getrusage peak was {s["usage"]["peak_rss_bytes"]/2**20:.2f}MiB. Monitored output was {sup["output_bytes"]/2**20:.2f}MiB. All stayed within120s/90s/1GiB/128MiB. Sampling is not an instantaneous memory ceiling. Costs cover the shared17-method pipeline, not independently measured per-method deployment latency.',
 '', f'25synthetic tests passed before freezing26source/test bindings and303prior evidence identities. A fresh-process verifier passed {v["checks"]:,} checks in {v["seconds"]:.3f}s, replaying all references/scores/alarms and independently computing event, contingency, AP and primary-outcome arithmetic. No run failed or retried. Full scores were sealed before joint truth evaluation.',
 '', '## Scientific interpretation audit','',
 '| Check | Disposition |','|---|---|',
 '| Simpson/group reversal | Primary plant strata and full task/condition tables retained; Q1 worsening remains visible. |',
 '| Ecological inference | No generalization across real robots or manufacturers. |',
 '| Selection bias | Fixed synthetic tasks/conditions; not a representative deployment sample. |',
 '| Collider bias | No result-conditioned filtering or method exclusion. |',
 '| Base rates |25,002/207,900schedule-positive points; precision is specific to this constructed mixture. |',
 '| Regression to mean | Paired controls and unchanged fits; v0.13 failure remains acknowledged. |',
 '| Survivorship | All189episodes/3,213outcomes retained; misses and no-clear outcomes visible. |',
 '| Look-elsewhere | Primary failed; secondary contrasts do not replace it. |',
 '| Forking paths | Frozen settings; post-study early-fall clarification explicitly labelled. |',
 '| Causality | Controlled software ablations, not causal claims about industrial deployments. |',
 '| Reverse causality | Training/calibration before generation; no labels/truth/schedule in detector input settings. |',
 '', 'All11categories were considered using the research skill guidance. No significance tests or confidence intervals are invented. Three paired noise seeds reuse simulator/task/plant structure. This is a same-assistant audit, not external peer review.',
 '', '## Contribution decision','',
 'Retire the RBF-plus-dual-window assembly as a claimed improvement on this evidence. Keep its code and all negative outcomes as development records. The protected-reference contrast is scientifically useful, but is also achieved by the simpler base model and does not demonstrate a new algorithm. See [novelty audit](NOVELTY_AUDIT.md). CASPER/Edge are not beaten by these results: they use different information, and full compatible paper-level reproduction remains unresolved.',
 '', 'A new model proposal should begin with a specific failure in a compatible published baseline and independent evidence. FactoryNet is a new public-data lead with explicit setpoint/feedback structure, but its latest manuscript/release, permissions, fault semantics and trusted-input correspondence still need admission. It has not been downloaded or used. The user’s original-method publication objective remains active; this audit is not silently substituted as the intended journal contribution.',
 '', '![All registered methods](comparison.png)', '', '![Protected and following references](reference_trace.png)']
text='\n'.join(lines)+'\n'
replacements={'misses41events':'misses 41 events','misses60':'misses 60','Same108overlap':'Same 108 overlap','points7,156':'points 7,156','points2→3':'points 2→3','Exactly0different':'Exactly 0 different','all189episodes':'all 189 episodes','points7,012':'points 7,012','same108hits':'same 108 hits','clear108/108for':'clear 108/108 for','events1→90':'events 1→90','gaps2→2,970':'gaps 2→2,970','F10.7070':'F1 0.7070','base0.6381':'base 0.6381','F10.9202 vs0.6407':'F1 0.9202 vs 0.6407','events108vs1':'events 108 vs 1','|108hits':'| 108 hits',',0/108':', 0/108','index349':'index 349','onset347':'onset 347','deviation0.0164868':'deviation 0.0164868','below0.1':'below 0.1','index352':'index 352','exceeds0.1':'exceeds 0.1','task,Q2,seed17,persistent':'task, Q2, seed 17, persistent','rank5,445 of5,500':'rank 5,445 of 5,500','within120s/90s/1GiB/128MiB':'within 120 s / 90 s / 1 GiB / 128 MiB','shared17-method':'shared 17-method','25synthetic':'25 synthetic','freezing26source':'freezing 26 source','and303prior':'and 303 prior','|25,002/207,900schedule-positive':'| 25,002/207,900 schedule-positive','All189episodes/3,213outcomes':'All 189 episodes / 3,213 outcomes','All11categories':'All 11 categories'}
for a,b in replacements.items():text=text.replace(a,b)
text=text.replace('s wall',' s wall').replace('s worker CPU',' s worker CPU').replace('MiB',' MiB').replace('GiB',' GiB')
text=text.replace('0/108timely', '0/108 timely').replace('6.457s', '6.457 s').replace('1  GiB', '1 GiB').replace('128  MiB', '128 MiB')
(HERE/'RESULTS.md').write_text(text)

methods=c['methods'];fig,axes=plt.subplots(1,3,figsize=(13.3,7.2),sharey=True,layout='constrained');y=np.arange(len(methods))
colors=['#b45e42' if m=='rbf_dual' else '#426981' for m in methods]
for ax,key,title in zip(axes,['benign_fraction','premature','f1'],['Benign alarm-state occupancy (%)','Registered early-clear events / 108','Unadjusted schedule F1']):
    vals=[pooled[m][key]*(100 if key=='benign_fraction' else 1) for m in methods];ax.barh(y,vals,color=colors)
    ax.set_title(title,fontsize=10);ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
axes[0].set_yticks(y,methods,fontsize=8);axes[0].invert_yaxis();axes[2].set_xlim(0,1)
fig.suptitle('Synthetic attack/recovery audit — all 17 registered methods',fontsize=12)
fig.savefig(HERE/'comparison.png',dpi=180);fig.savefig(HERE/'comparison.svg');plt.close(fig)
rid='N14_Q2_17_persistent_offset';z=load_npz(RUN/('score_'+rid+'.npz'));t=load_npz(RUN/('truth_'+rid+'.npz'));tt=np.arange(1200)*.02
fig,axes=plt.subplots(3,1,figsize=(9.8,7),sharex=True,layout='constrained')
axes[0].plot(tt,z['scores'][:,0]/cal['thresholds']['Q2']['base'],label='Protected base score / threshold',color='#426981')
axes[0].plot(tt,z['scores'][:,3]/cal['thresholds']['Q2']['following'],label='Following score / threshold',color='#b45e42')
axes[0].axhline(1,color='black',ls=':',lw=1);axes[0].set_yscale('symlog',linthresh=1);axes[0].set_ylim(bottom=0);axes[0].set_ylabel('Score / threshold');axes[0].legend(fontsize=8,loc='upper right')
for m,col,offset in [('base_dual','#426981',1.2),('following_dual','#b45e42',0.)]:
    axes[1].step(tt,z['alarms'][:,c['methods'].index(m)].astype(int)+offset,where='post',color=col,label=m)
axes[1].set_yticks([0,1,1.2,2.2],['following off','following on','base off','base on'],fontsize=8);axes[1].set_ylabel('Alarm state')
dist=np.max(np.abs((t['state']-t['counterfactual'])/scales['Q2']),axis=1)
axes[2].plot(tt,dist,color='#35553e');axes[2].axhline(.1,color='black',ls=':',lw=1,label='Return tolerance 0.1');axes[2].set_ylabel('True standardized\ndeviation');axes[2].set_xlabel('Episode time (s)');axes[2].legend(fontsize=8)
for ax in axes:
    ax.axvspan(c['onset']*.02,c['end']*.02,color='#999999',alpha=.18);ax.set_xlim(2,24);ax.spines[['top','right']].set_visible(False)
fig.suptitle('Post-study illustration: N14 / Q2 / seed 17 / persistent offset\nGrey shading denotes the corrupted-command interval',fontsize=11)
fig.savefig(HERE/'reference_trace.png',dpi=180);fig.savefig(HERE/'reference_trace.svg');plt.close(fig)
for path in HERE.glob('*.svg'):path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
names=['RESULTS.md','summary.csv','events.csv','strata.csv','DESCRIPTIVE_DIAGNOSTICS.json','comparison.png','comparison.svg','reference_trace.png','reference_trace.svg']
(HERE/'PRESENTATION.json').write_text(json.dumps(dict(python=sys.version,numpy=np.__version__,matplotlib=matplotlib.__version__,verified_run_sha256=sha(HERE/'VERIFICATION.json'),
 outputs={name:sha(HERE/name) for name in names}),indent=2)+'\n')
print(json.dumps(dict(outputs=len(names),differences=checks['alarm_array_differences'],outside_tolerance_events=outside)))
