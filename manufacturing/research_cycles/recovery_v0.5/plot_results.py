"""Standalone scientific figures from saved, verified synthetic outcomes."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from common import HERE,PROJECT,LOCAL,arrays,sha

if __name__=='__main__':
    result=json.loads((HERE/'RESULTS.json').read_text());run=LOCAL/'runs/reporting_001'
    out=PROJECT/'output/recovery_v0.5';out.mkdir(exist_ok=True,parents=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    names=list(result['all_methods']);records=list(result['all_methods'].values());y=np.arange(len(names))
    labels=['Persistence','AR(4)','ARX(4)','Following observer','Following + mean45','Following + CUSUM',
            'Command reference','Fused error','Following + hysteresis','Fused + hysteresis','Candidate (same rule)']
    fig,axs=plt.subplots(1,3,figsize=(14,6.5),sharey=True,gridspec_kw={'width_ratios':[1,1,1.5]},layout='constrained')
    colors=['#376b8a' if n in ['candidate_recovery','fused_hysteresis'] else '#438577' if n=='following' else '#8d99a6' for n in names]
    axs[0].barh(y,[100*r['clean_normal_fraction'] for r in records],color=colors)
    axs[1].barh(y,[100*r['recall'] for r in records],color=colors)
    left=np.zeros(len(y));columns=[('clear_before_physical_return','Before diagnostic return','#e5a451'),
        ('after','At/after diagnostic return','#4b8b7a'),('detected_but_not_cleared','No clear within 5 s','#7e76a5'),
        ('missed_events','Event missed','#bcc4cc')]
    for key,label,color in columns:
        values=np.asarray([r['cleared_after_hit']-r['clear_before_physical_return'] if key=='after' else r[key] for r in records])
        axs[2].barh(y,values,left=left,label=label,color=color);left+=values
    axs[0].set_yticks(y,labels);axs[0].invert_yaxis()
    axs[0].set_title('Alarms on clean episodes');axs[0].set_xlabel('Eligible observations (%)');axs[0].set_xlim(0,6.2)
    axs[1].set_title('Attack-command recall');axs[1].set_xlabel('Corruption-interval points (%)');axs[1].set_xlim(0,105)
    axs[2].set_title('First clear after command restoration');axs[2].set_xlabel('Events (all 30 retained)');axs[2].set_xlim(0,30)
    axs[2].legend(loc='upper center',bbox_to_anchor=(.5,-.09),ncol=1,frameon=False,fontsize=8)
    fig.suptitle('Synthetic two-joint arm: detection, normal alarms and recovery',fontsize=14)
    for ax in axs:ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    fig.savefig(out/'comparison.png',dpi=180);fig.savefig(out/'comparison.pdf');plt.close(fig)

    conditions=['brief_offset','persistent_offset','hold'];fig,axs=plt.subplots(2,3,figsize=(14,6.8),layout='constrained')
    rows=json.loads((run/'outcomes.json').read_text());dt=.02
    for col,condition in enumerate(conditions):
        ident=f'evaluation_light_17_{condition}';ep=arrays(run/(ident+'.npz'));t=ep['time'];where=np.flatnonzero(ep['attack']);begin=where[0]*dt;end=(where[-1]+1)*dt
        row=next(r for r in rows if r['id']==ident and r['method']=='candidate_recovery');returned=end+row['physical_return_steps']*dt
        top,bottom=axs[:,col];top.plot(t,ep['state'][:,0],color='#3b6c9b',label='Actual simulated joint1')
        top.plot(t,ep['reference'][:,0],color='#b97a3b',ls='--',label='Approved-command reference')
        top.set_title(condition.replace('_',' ').capitalize());top.set_ylabel('Joint angle (rad)')
        method_indices=[3,4,5,6,10];method_labels=['Following','Mean45','CUSUM','Reference','Candidate']
        for i,j in enumerate(method_indices):
            a=ep['alarm'][:,j]&~ep['unknown'][:,j]
            bottom.fill_between(t,i-.32,i+.32,where=a,step='post',color=['#438577','#8d99a6','#7e76a5','#b97a3b','#376b8a'][i])
        bottom.set_yticks(range(5),method_labels);bottom.set_ylim(4.6,-.6);bottom.set_xlabel('Simulation time (s)')
        for ax in [top,bottom]:
            ax.axvspan(begin,end,color='#d8b4ae',alpha=.3);ax.axvline(returned,color='#333',ls=':',lw=1.2)
            ax.set_xlim(5.7,12.8 if condition!='brief_offset' else 8);ax.grid(alpha=.15)
        if col==0:top.legend(fontsize=8,frameon=False,loc='upper left')
    fig.suptitle('Synthetic timelines: light plant, seed17 — fixed illustrative cases',fontsize=14)
    fig.supxlabel('Shading: corrupted command interval. Dotted line: declared physical-return diagnostic. Bands: alarm on.',fontsize=10)
    fig.savefig(out/'timelines.png',dpi=180);fig.savefig(out/'timelines.pdf');plt.close(fig)
    receipt={'input_results_sha256':sha(HERE/'RESULTS.json'),'script_sha256':sha(HERE/'plot_results.py'),
             'figures':{p.name:sha(p) for p in out.iterdir() if p.suffix in ['.pdf','.png']}}
    with (LOCAL/'figures.json').open('x') as f:f.write(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))
