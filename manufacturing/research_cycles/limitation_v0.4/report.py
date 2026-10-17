"""Post-execution descriptive report and figures from sealed result artifacts."""
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import numpy as np
from common import HERE,PROJECT,LOCAL,sha,check_freeze
from mechanism import score_streams

os.environ['MPLCONFIGDIR']=str(LOCAL/'matplotlib')
os.environ['XDG_CACHE_HOME']=str(LOCAL/'font_cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def aggregate(rows):
    fresh=[r['fresh_delay'] for r in rows if r['fresh_delay'] is not None]
    return {'seed_case_count':len(rows),'overlap_hits':sum(r['overlap_hit'] for r in rows),
        'fresh_hits':sum(r['fresh_hit'] for r in rows),'misses':sum(not r['overlap_hit'] for r in rows),
        'mean_point_recall':float(np.mean([r['recall'] for r in rows])),
        'mean_precision':float(np.mean([r['precision'] for r in rows])),
        'mean_f1':float(np.mean([r['f1'] for r in rows])),
        'mean_post_alarm_points':float(np.mean([r['post_alarm_points'] for r in rows])),
        'first_clear_censored':sum(r['first_clear_censored'] for r in rows),
        'median_fresh_delay_among_hits':float(np.median(fresh)) if fresh else None}


def main():
    freeze=check_freeze();cfg=freeze['configuration'];run=LOCAL/'runs/replay_001'
    verify=LOCAL/'verification/verify_001/verification.json'
    validation=json.loads(verify.read_text())
    if validation['status']!='passed':raise ValueError('Verification not passed')
    for p,h in validation['run_sha256'].items():
        if sha(run/p)!=h:raise ValueError('Run changed: '+p)
    rows=json.loads((run/'case_outcomes.json').read_text())
    normal=json.loads((run/'normal_outcomes.json').read_text())
    summary=json.loads((run/'summary.json').read_text());resources=json.loads((run/'supervisor.json').read_text())
    calibration=json.loads((run/'calibration.json').read_text())
    roster=json.loads((run/'cases.json').read_text());figure_dir=PROJECT/'output/limitation_v0.4';figure_dir.mkdir(exist_ok=True)
    groups=[]
    for model in cfg['models']:
        for score in cfg['scores']:
            for family in ['hold','slow','bias']:
                for duration in cfg['durations']:
                    eligible=[r for r in rows if r['model']==model and r['score']==score and r['family']==family and r['duration']==duration]
                    groups.append(dict(model=model,score=score,family=family,duration=duration,**aggregate(eligible)))
    with (HERE/'aggregate_outcomes.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(groups[0]));w.writeheader();w.writerows(groups)
    cnn=[]
    for duration in cfg['durations']:
        for score in cfg['scores']:
            eligible=[r for r in rows if r['model'].startswith('cnn') and r['score']==score and r['duration']==duration]
            cnn.append(dict(duration=duration,score=score,**aggregate(eligible)))
    diagnosis=[]
    for model in cfg['models']:
        for family in ['hold','slow','bias']:
            r=[x for x in rows if x['model']==model and x['family']==family and x['score']=='point' and x['duration']==450]
            ratios=[x['late_to_oracle'] for x in r if x['late_to_oracle'] is not None]
            diagnosis.append(dict(model=model,family=family,cases=len(r),
                late_lower_than_early=sum(x['late_mse']<x['early_mse'] for x in r),
                late_lower_than_oracle=sum(x['late_mse']<x['oracle_late_mse'] for x in r),
                median_late_to_oracle=float(np.median(ratios)) if ratios else None))
    safe={'study_id':cfg['study_id'],'synthetic_measurement_replay':True,
        'normal':normal,'aggregate_by_model_family_duration':groups,'cnn_descriptive_aggregates':cnn,
        'diagnostics':diagnosis,'resources':resources,'worker_usage':summary['usage'],
        'verification':{'passed':validation['passed'],'total':validation['total']},
        'interpretation':'Dependent paired scenarios on exposed normal development; seeds are computational repeats.'}
    (HERE/'RESULTS.json').write_text(json.dumps(safe,indent=2,allow_nan=False)+'\n')
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.hashsalt':'limitation-v04'})
    labels={'point':'Point error','mean45':'Mean 45','mean450':'Mean 450','cusum':'CUSUM'}
    colors=['#345995','#37a995','#d88c27','#b64c65']
    def save(fig,name):
        fig.savefig(figure_dir/(name+'.png'),dpi=180,bbox_inches='tight')
        fig.savefig(figure_dir/(name+'.svg'),bbox_inches='tight',metadata={'Date':None})
        p=figure_dir/(name+'.svg');p.write_text('\n'.join(s.rstrip() for s in p.read_text().splitlines())+'\n')
        plt.close(fig)
    fig,axs=plt.subplots(1,3,figsize=(14,4.3),layout='constrained')
    for k,s in enumerate(cfg['scores']):
        selected=[x for x in cnn if x['score']==s]
        for ax,key,factor in [(axs[0],'mean_point_recall',100),(axs[1],'mean_f1',1),(axs[2],'mean_post_alarm_points',1)]:
            ax.plot([5,45,450],[r[key]*factor for r in selected],marker='o',color=colors[k],label=labels[s])
            ax.set_xscale('log');ax.set_xticks([5,45,450],['5','45','450']);ax.set_xlabel('Synthetic duration (observations)');ax.grid(alpha=.18)
    axs[0].set_title('Alarm coverage within deviation');axs[0].set_ylabel('Mean point recall (%)')
    axs[1].set_title('Precision–recall trade-off');axs[1].set_ylabel('Mean case F1')
    axs[2].set_title('Alarm carryover after deviation');axs[2].set_ylabel('Alarm points in next 512 observations')
    axs[0].legend(fontsize=9);fig.suptitle('Fixed CNNs: all 63 scenarios per duration, all three seeds\nExploratory measurement replay; descriptive averages',fontsize=12)
    save(fig,'duration_tradeoff')
    fig,axs=plt.subplots(1,2,figsize=(12,4.7),layout='constrained')
    for ax,mode in zip(axs,['normal','long']):
        matrix=[]
        for model in cfg['models']:
            vals=[]
            for s in cfg['scores']:
                if mode=='normal':value=next(r['alarm_fraction']*100 for r in normal if r['model']==model and r['score']==s)
                else:value=100*np.mean([r['recall'] for r in rows if r['model']==model and r['score']==s and r['duration']==450])
                vals.append(value)
            matrix.append(vals)
        matrix=np.asarray(matrix);im=ax.imshow(matrix,aspect='auto',cmap='Blues')
        ax.set_xticks(range(4),[labels[x] for x in cfg['scores']],rotation=20)
        ax.set_yticks(range(6),cfg['models'])
        for i in range(6):
            for j in range(4):ax.text(j,i,f'{matrix[i,j]:.2f}',ha='center',va='center',color='white' if matrix[i,j]>matrix.max()*.6 else '#152536')
        ax.set_title('Unmodified normal alarm points (%)' if mode=='normal' else '450-observation deviation recall (%)')
    fig.suptitle('All models and scoring rules • same normal-calibration percentile',fontsize=12)
    save(fig,'all_controls')
    # Fixed example selection declared before outcomes: first onset, middle severity, seed 17.
    fig,axs=plt.subplots(3,2,figsize=(13,9),layout='constrained')
    name='cnn_seed17';thresholds=np.asarray(calibration[name]['thresholds']);mean=calibration[name]['normal_mean']
    with np.load(run/(name+'_normal.npz'),allow_pickle=False) as a:normal_energy=a['energy']
    with np.load(run/(name+'_overrides.npz'),allow_pickle=False) as a:
        for row,(family,mag) in enumerate([('hold',.5),('slow',.5),('bias',1.)]):
            for col,duration in enumerate([5,450]):
                case=next(x for x in roster if x['family']==family and x['magnitude']==mag and x['duration']==duration and x['onset']==8576)
                e=normal_energy.copy();changed=a[case['id']+'_energy'];start=case['onset'];e[start:start+len(changed)]=changed
                scores=score_streams(e,mean,cfg);idx=np.arange(start-64,start+duration+512);ax=axs[row,col]
                for k in [0,1,3]:ax.plot(idx-start,scores[idx,k]/thresholds[k],label=labels[cfg['scores'][k]],color=colors[k],linewidth=1)
                ax.axhline(1,color='black',linestyle=':',linewidth=1);ax.axvspan(0,duration,color='grey',alpha=.16)
                ax.set_yscale('symlog',linthresh=1);ax.set_ylim(bottom=0);ax.set_title(f'{family} {mag:g} • duration {duration}');ax.grid(alpha=.15)
                ax.set_xlabel('Observations relative to synthetic onset');ax.set_ylabel('Score / own normal threshold')
    axs[0,0].legend(fontsize=9);fig.suptitle('Prespecified examples • CNN seed 17 • shaded interval is the synthetic change',fontsize=12)
    save(fig,'fixed_examples')
    lines=['# Brief and persistent deviations: measured limitation and improvement test','',
        '## Material Passport','',
        '**Completed 17 October 2026.** Manufacturing; owner Haiqa Mushtaq; operator Codex. '+
        'Exploratory synthetic measurement replay using fixed v0.3 models. No fitting or new raw/final observations. '+
        f'All {validation["passed"]:,}/{validation["total"]:,} fresh-process verification checks passed.','',
        '## Main finding','',
        'The experiment supports a **conditional history-assimilation effect**, not a universal collapse of CNN prediction error. '+
        'Altered histories usually reduce error relative to the clean-history counterfactual for holds and slow playback. '+
        'However, late CNN error does not consistently fall below early error, and sensor offsets often amplify it. '+
        'Thus “the baseline learns every persistent deviation as normal” is contradicted by this experiment. Model weights never changed.','',
        'A causal CUSUM-style accumulator increases long-deviation alarm coverage, but produces substantial carryover and lower overall F1 than a 45-observation rolling mean. '+
        'The simpler rolling mean is the better measured compromise here. This is an established scoring technique, not an original digital-twin contribution.','',
        '## Execution and comparison','',
        '189 scenarios = 3 families × 3 severities × 3 durations × 7 fixed onsets. Six fixed predictors and four scoring rules produce 4,536 case outcomes. '+
        'All models use the same 4,096 normal threshold-calibration targets, rank 4,056 and strict exceedance; '+
        '8,192 later unmodified normal targets measure alarm burden. These are roles inside previously exposed normal development, not a new holdout. '+
        'Scores run continuously without event-boundary resets. All predictions and calibration were sealed before outcome calculation.','',
        'Holds, slow playback and gyroX offsets are explicitly synthetic edits to recordings. Slow playback does not rescale robot dynamics or accelerations. '+
        'Neither these edits nor their labels establish physical motion, attacks, cyber intent or live security. '+
        'Delays and rates use observations because time units remain unresolved.','',
        '## CNN results across all declared seeds','',
        'Each row averages the same 63 scenarios repeated for three fixed CNN seeds (189 dependent seed-case outcomes). '+
        'F1 is a mean of case-level unadjusted F1 across the full 8,192-target evaluation interval; it is not computed from pooled counts. '+
        'Event hits mean any alarm overlap; fresh starts and missed outcomes remain separate.','',
        '| Duration | Score | Point recall | Mean F1 | Event hits / 189 | Fresh starts / 189 | Post-event alarm points / 512 | Uncleared at 512 |',
        '|---:|---|---:|---:|---:|---:|---:|---:|']
    for r in cnn:
        lines.append(f'| {r["duration"]} | {labels[r["score"]]} | {r["mean_point_recall"]:.2%} | {r["mean_f1"]:.4f} | {r["overlap_hits"]} | {r["fresh_hits"]} | {r["mean_post_alarm_points"]:.2f} | {r["first_clear_censored"]} |')
    lines+=['','For 450-observation deviations, point error detects some part of 159/189 seed-case events, versus 155/189 for CUSUM. '+
        'Higher point recall therefore means more alarm coverage inside events, not more events detected. '+
        'The 45-point mean raises descriptive mean F1 from 0.2778 to 0.5127, while missing more events and carrying alarms further after release. '+
        'CUSUM remains active for all 512 post-event observations in 128/189 long seed-case outcomes. '+
        'For five-observation deviations, both rolling means miss all 189 events; CUSUM has only four fresh event starts. '+
        'A detection-delay median conditional on hits must not conceal these misses; all null delays are retained in local case outcomes.','',
        '![Duration trade-off](../../output/limitation_v0.4/duration_tradeoff.png)','',
        '## Normal alarms and strong controls','',
        '| Model | Point alarm % | Mean45 alarm % | Mean450 alarm % | CUSUM alarm % |',
        '|---|---:|---:|---:|---:|']
    for name in cfg['models']:
        vals=[next(r['alarm_fraction']*100 for r in normal if r['model']==name and r['score']==s) for s in cfg['scores']]
        lines.append('| '+name+' | '+' | '.join(f'{v:.3f}' for v in vals)+' |')
    lines+=['','A common calibration percentile does not yield identical later false-alarm rates. '+
        'The three CNN CUSUM rates range from 0.818% to 3.198%; point-scoring rates range from 0.989% to 1.111%. '+
        'AR remains the strongest normal predictor from v0.3, but low prediction error alone does not imply useful deviation detection. '+
        'Persistence has analytically zero error after the first full-hold sample. Mean, AR and persistence remain visible in the complete tables and figure.','',
        '![All controls](../../output/limitation_v0.4/all_controls.png)','',
        '## What the history diagnostic establishes','',
        'The oracle uses the original, unmodified prediction history but the same altered target; it is excluded from the main comparison. '+
        'The ratio below is median late actual MSE divided by late oracle MSE over all 21 long cases per family, separately for each fixed model. '+
        'Values below one mean changed histories reduce discrepancy; above one mean they increase it.','',
        '| Model | Holds | Slow playback | Sensor offsets |','|---|---:|---:|---:|']
    for model in cfg['models']:
        vals=[next(x['median_late_to_oracle'] for x in diagnosis if x['model']==model and x['family']==f) for f in ['hold','slow','bias']]
        lines.append('| '+model+' | '+' | '.join(f'{v:.3f}' if v is not None else 'undefined' for v in vals)+' |')
    lines+=['','Across the CNN seeds, late error is lower than early error in only 18/63 hold, 25/63 slow-playback and 9/63 offset outcomes. '+
        'The corresponding counts with late error below the oracle are 48/63, 54/63 and 2/63. '+
        'These paired results distinguish history conditioning from a general temporal decline. '+
        'The mean predictor has an exact ratio of one because it ignores history; the verifier checks that identity.','',
        '![Prespecified trace examples](../../output/limitation_v0.4/fixed_examples.png)','',
        '## Decision and next scientific step','',
        '1. Retain point error and the 45-point rolling mean as mandatory reference scorers. Keep the longer mean and accumulator as memory/carryover controls; do not present CUSUM as a successful general solution.',
        '2. The candidate problem is now sharper: preserve evidence of a sustained execution change while clearing it when the process demonstrably returns, without suppressing brief events. Simply accumulating residuals does not solve all three objectives.',
        '3. A context-aware recovery observer would need information beyond these residuals. Next specify a small dynamics-based simulation with permitted command context, plant/observer mismatch and legitimate changes; compare ordinary filters/reset rules using the same context. Freeze meaningful held-out task/plant conditions before generating their outcomes.',
        '4. Any mechanism designed from these outcomes is exploratory. Establish its exact difference from close prior art and then test it on fresh evidence. No new novelty, publication readiness or universal CASPER-family failure is claimed.','',
        '## Reproducibility and limitations','',
        f'The scoring campaign took **{resources["wall_seconds"]:.3f}s wall**, **{summary["usage"]["process_cpu_seconds"]:.3f}s CPU**, '+
        f'**{resources["sampled_peak_rss_bytes"]/1048576:.2f}MiB sampled peak RSS** and **{resources["output_bytes"]:,} bytes** before the supervisor receipt. '+
        'All caps passed; one scoring attempt and one successful verification attempt. All six models, all seeds, cases and misses remain visible.','',
        '22 synthetic tests passed before freezing. The first test attempt failed one float32 offset assertion (3.8e-6 rounding); '+
        'the fixture tolerance was corrected to one float32 spacing, with the failed log retained. No scientific run failed or required a parameter change. '+
        'The verifier separately recomputed energy, calibration, convolution-based smoothing, recursive CUSUM, point/event/post-event metrics, '+
        'full-versus-optimized predictions and all frozen identities. This is software verification, not independent scientific replication.','',
        'The old controller-data holdout remains exposed; this work uses a separate IMU nominal prefix already used for development. '+
        'All CNNs had reached a fixed training cap, so capacity/training effects remain unresolved. '+
        'Synthetic cases, seeds and windows are not independent robots. No confidence interval or significance claim is inferred. '+
        'Thresholds were calibrated on correlated normal scores; empirical ranks do not supply sequential false-alarm guarantees. '+
        'First-clear timing does not guarantee sustained recovery; later alarms and post-event alarm counts are retained.','',
        'See [protocol](PLAN.md), [freeze](FREEZE.json), [machine-readable results](RESULTS.json), '+
        '[all model/family/duration aggregates](aggregate_outcomes.csv), [execution and replay instructions](README.md), '+
        '[local full outcomes](../../local/limitation_v0.4/runs/replay_001/case_outcomes.json) and '+
        '[verification](../../local/limitation_v0.4/verification/verify_001/verification.json). '+
        'CUSUM background: [NIST control-chart handbook](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm).','']
    (HERE/'RESULTS.md').write_text('\n'.join(lines))
    outputs=[HERE/'RESULTS.md',HERE/'RESULTS.json',HERE/'aggregate_outcomes.csv']+list(figure_dir.glob('*'))
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'command':sys.argv,'source_sha256':sha(Path(__file__)),
        'matplotlib':matplotlib.__version__,'inputs':{str(p.relative_to(PROJECT)):sha(p) for p in run.iterdir() if p.is_file()},
        'verification_sha256':sha(verify),'outputs':{str(p.relative_to(PROJECT)):sha(p) for p in outputs},
        'post_execution_analysis':True}
    (LOCAL/'report_generation.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'aggregate_rows':len(groups),'figures':3,'outputs':len(outputs)},indent=2))


if __name__=='__main__':main()
