"""Read saved joint results and generate auditable tables and static figures."""
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import resource
import sys
import time
script_started=time.monotonic()
from support import HERE,PROJECT,LOCAL,sha,arrays,check_freeze
os.environ['MPLCONFIGDIR']=str(PROJECT/'local/matplotlib-v03')
os.environ['XDG_CACHE_HOME']=str(PROJECT/'local/font-cache-v06')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

if __name__=='__main__':
    resource.setrlimit(resource.RLIMIT_CPU,(60,60));start=time.monotonic()
    check_freeze();run=LOCAL/'runs/simulation_001';result=json.loads((run/'aggregate.json').read_text())
    receipt=json.loads((LOCAL/'verification.json').read_text());assert receipt['status']=='passed'
    output=PROJECT/'output/recovery_v0.6';output.mkdir(parents=True,exist_ok=False)
    labels={'persistence':'Persistence','ar4':'AR(4)','arx4':'ARX(4)','following':'Following error',
        'following_mean45':'Following mean (45)','following_cusum':'Following CUSUM','fused':'Fused error',
        'fused_hysteresis':'Fused hysteresis','mode_hysteresis':'Mode hysteresis','envelope':'Envelope error',
        'envelope_hysteresis':'Envelope hysteresis','nominal_fixed_return':'Nominal entry + fixed return',
        'envelope_fixed_return':'Envelope entry + fixed return'}
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,3,figsize=(16,7.5),sharey=True)
    primary=[r for r in result['rows'] if r['stratum']=='within_range']
    stress=[r for r in result['rows'] if r['stratum']=='extrapolation']
    y=np.arange(len(primary));colors=['#167d8d' if r['method']=='envelope_fixed_return' else '#65758b' for r in primary]
    for ax,rows in zip(axes[:2],[primary,stress]):
        vals=[100*r['benign_alarm_fraction'] for r in rows];ax.barh(y,vals,color=colors)
        for i,v in enumerate(vals):ax.text(v+.1,i,f'{v:.2f}%',va='center',fontsize=8)
        ax.set_xlim(0,max(vals)*1.25+1);ax.set_xlabel('Benign observations alarmed (%)');ax.grid(axis='x',alpha=.2)
    axes[0].set_title('Within parameter range · primary');axes[1].set_title('Outside range · stress')
    axes[0].set_yticks(y,list(labels.values()));axes[0].invert_yaxis()
    axes[2].barh(y-.17,[r['overlap_hits'] for r in primary],height=.32,label='Events detected',color='#a9c8dc')
    axes[2].barh(y+.17,[r['premature_clear_events'] for r in primary],height=.32,label='Events with early clearing',color='#b84f47')
    axes[2].set_xlabel('Events out of 60');axes[2].set_title('Primary detection and recovery');axes[2].set_xlim(0,64);axes[2].legend(loc='lower right',fontsize=8)
    fig.suptitle('Command uncertainty and recovery — frozen synthetic experiment',fontsize=16)
    fig.text(.32,.02,'144 simulated episodes · 13 methods · normal-only stateful calibration · no real-robot validation',fontsize=10)
    fig.tight_layout(rect=(0,.05,1,.95));fig.savefig(output/'comparison.png',dpi=170);fig.savefig(output/'comparison.svg');plt.close(fig)
    fig,axes=plt.subplots(2,1,figsize=(12,7),sharex=True)
    names=['authorized_offset','persistent_offset'];cfg=check_freeze()['configuration']
    for ax,condition in zip(axes,names):
        ep=arrays(run/f'eval_A_low_17_{condition}.npz');t=np.arange(1000)*.02
        ax.plot(t,ep['approved'][:,0],label='Approved command',color='#65758b',lw=1)
        ax.plot(t,ep['state'][:,0],label='True simulated q1',color='#222',lw=1.2)
        ax.fill_between(t,ep['bank'][:,:,0].min(1),ep['bank'][:,:,0].max(1),alpha=.25,color='#167d8d',label='Sampled model envelope')
        for j,k in enumerate([7,8,12]):
            ax.fill_between(t,-.50-j*.07,-.46-j*.07,where=ep['alarm'][:,k]&~ep['unknown'][:,k]&(t>=2),color=['#888','#cf8b27','#167d8d'][j],label=labels[cfg['methods'][k]])
        ax.axvspan(0,2,alpha=.09,color='gray');ax.text(.08,.57,'Warmup excluded',fontsize=8,color='#555')
        ax.axvspan(6.5,10.5,alpha=.08,color='#da693c');ax.set_ylabel('Joint 1 (rad)');ax.set_title(condition.replace('_',' ').capitalize()+' · task A / low mismatch / seed 17')
        ax.set_ylim(-.70,.65);ax.grid(alpha=.15)
    axes[-1].set_xlabel('Simulation time (s)');axes[0].legend(ncol=3,fontsize=8,loc='upper right')
    fig.suptitle('Preselected paired examples; alarm strips show retained decisions',fontsize=14)
    fig.tight_layout(rect=(0,0,1,.95));fig.savefig(output/'examples.png',dpi=170);fig.savefig(output/'examples.svg');plt.close(fig)
    table=['# All declared results — generated from saved artifacts','',
        'Synthetic results. AP ranks unknown observations last; F1 uses every eligible attack target. Benign alarms exclude attack-containing episodes.','']
    for stratum in ['within_range','extrapolation']:
        table += [f'## {stratum}','','| Method | Benign alarms / points | Alarm episodes/h | Recall | F1 | AP | Events hit | Fresh hits | Early-clear events | Cleared ≤5s / returned detected |',
            '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
        for r in result['rows']:
            if r['stratum']!=stratum:continue
            table.append(f"| {labels[r['method']]} | {r['benign_alarms']}/{r['benign_points']} | {r['benign_episodes_per_hour']:.2f} | {100*r['recall']:.2f}% | {r['f1']:.4f} | {r['average_precision_unknown_ranked_last']:.4f} | {r['overlap_hits']}/{r['events']} | {r['fresh_hits']}/{r['events']} | {r['premature_clear_events']} | {r['cleared_within_five_seconds']}/{r['returned_detected_events']} |")
        table.append('')
    table+=['Source: `local/recovery_v0.6/runs/simulation_001/aggregate.json`.',f"SHA-256: `{sha(run/'aggregate.json')}`."]
    with (HERE/'TABLES.md').open('x') as f:f.write('\n'.join(table)+'\n')
    with (HERE/'SUMMARY.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    usage=resource.getrusage(resource.RUSAGE_SELF)
    report=dict(utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,source_sha256=sha(run/'aggregate.json'),
        wall_seconds=time.monotonic()-script_started,cpu_seconds=usage.ru_utime+usage.ru_stime,peak_rss_bytes=usage.ru_maxrss,
        python=sys.version,numpy=np.__version__,matplotlib=matplotlib.__version__,
        sha256={str(p.relative_to(PROJECT)):sha(p) for p in output.iterdir()})
    with (LOCAL/'presentation.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps(report,indent=2))
