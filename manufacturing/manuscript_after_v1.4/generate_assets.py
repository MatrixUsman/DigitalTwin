"""Render saved evidence; no fitting, signal development or simulation."""
from pathlib import Path
import os, json, hashlib, sys
M=Path(__file__).resolve().parent; P=M.parent
os.environ['XDG_CACHE_HOME']=str(P/'local/manuscript_after_v1.4/plot_cache')
os.environ['MPLCONFIGDIR']=str(P/'local/manuscript_after_v1.4/plot_cache')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
inputs={}
def read(path):
    inputs[str(path.relative_to(P))]=hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text())
def table(name, spec, header, rows):
    text='\\begin{tabular}{'+spec+'}\\toprule\n'+header+r' \\\midrule'+'\n'
    text+='\n'.join(' & '.join(map(str,row))+r' \\' for row in rows)
    (M/'generated'/name).write_text(text+'\n\\bottomrule\\end{tabular}\n')
A=P/'local/attack_audit_v0.14/runs/audit_001'
N=P/'local/residual_twin_v0.13/runs/pilot_001'
s=read(A/'summary.json');cfg=read(P/'research_cycles/attack_audit_v0.14/config.json')
pooled={r['method']:r for r in s['rows'] if r['stratum']=='pooled'}
assert s['primary']['passed'] is False and len(pooled)==17
names={k:k.replace('_',' ') for k in pooled}
names['base_return1']='base return';names['rbf_return1']='RBF return'
names['rbf_dual_nodwell']='RBF dual, no dwell'
names['rbf_following_dual']='RBF following dual'
names['persistence_point']='persistence';names['mean21_point']='mean (21)';names['base_cusum']='base CUSUM'
for k in names:names[k]=names[k].replace('rbf','RBF')
table('audit.tex','lrrrrrrr','Method & F1 & AP & Benign & Hit/fresh & Early & Gaps & Clear',[
 [names[k],f'{r["f1"]:.4f}',f'{r["average_precision"]:.4f}',f'{r["benign_alarms"]:,}',f'{r["hits"]}/{r["fresh_hits"]}',r['premature'],f'{r["gap_points"]:,}',f'{r["clear_timely"]}/{r["returned_detected"]}'] for k,r in pooled.items()])
table('extended.tex','lrrrrr','Method & Precision & Recall & Benign (\\%) & Starts/h & Misses',[
 [names[k],f'{r["precision"]:.4f}',f'{r["recall"]:.4f}',f'{100*r["benign_fraction"]:.3f}',f'{r["benign_episodes_per_hour"]:.1f}',r['misses']] for k,r in pooled.items()])
table('strata.tex','lrrrrrr','Plant & Base benign & RBF benign & Base gaps & RBF gaps & Base fresh & RBF fresh',[
 [p,*[next(r for r in s['rows'] if r['stratum']==p and r['method']==m)[key] for key in ['benign_alarms','gap_points','fresh_hits'] for m in ['base_dual','rbf_dual']]] for p in ['Q1','Q2','Q3']])
sel=read(N/'selection.json');normal=read(N/'summary.json');rows=[]
for i,p in enumerate(['Q1','Q2','Q3']):
 b=next(r for r in normal['rows'] if r['plant']==p and r['role']=='base');r=next(r for r in normal['rows'] if r['plant']==p and r['role']=='rbf')
 _,k,width,ridge=sel['models'][p]['rbf'].split('_')
 rows.append([p,[8,16,32][i],k,width,ridge,f'{sel["thresholds"][p]["rbf"]:.6f}',f'{100*(r["rmse"]/b["rmse"]-1):+.4f}',f'{100*(r["q99"]/b["q99"]-1):+.4f}'])
table('selection.tex','lrrrrrrr',r'Plant & ARX $p$ & Centers & Width & Ridge & $\tau$ & $\Delta$RMSE (\%) & $\Delta q_{.99}$ (\%)',rows)
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(6.8,2.15));ax.set(xlim=(0,10),ylim=(-.2,4.2));ax.axis('off')
def box(x,y,w,h,text,color='#e8eef3'):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.07',facecolor=color,edgecolor='#526879',lw=.8));ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=8)
def arrow(a,b):ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','lw':1,'color':'#526879'})
box(.1,2.9,2.3,.9,'Clean commissioning\nfit, select, calibrate')
box(3.5,2.9,2.8,.9,'Frozen ARX + RBF\nreference and threshold')
box(.1,1.3,2.3,.9,'Clean initialization\n+ approved commands')
box(3.5,1.3,2.8,.9,'Predicted motion\n(no measurement update)')
box(7.3,1.3,2.5,.9,'Residual score\n+ return evidence')
box(3.5,.05,2.8,.75,'Current measurements', '#f1ede7')
box(7.3,.05,2.5,.75,'Alarm state + counter', '#f1ede7')
arrow((2.48,3.35),(3.4,3.35));arrow((4.9,2.85),(4.9,2.25));arrow((2.48,1.75),(3.4,1.75));arrow((6.38,1.75),(7.2,1.75));arrow((6.38,.42),(7.2,1.3));arrow((8.55,1.23),(8.55,.85))
fig.tight_layout(pad=.2);fig.savefig(M/'figures/model.pdf');plt.close(fig)
rid='N14_Q2_17_persistent_offset'
def npz(path):
 inputs[str(path.relative_to(P))]=hashlib.sha256(path.read_bytes()).hexdigest()
 return np.load(path,allow_pickle=False)
z=npz(A/f'score_{rid}.npz');t=npz(A/f'truth_{rid}.npz');cal=read(A/'calibration.json')
model=npz(N/'base_Q2.npz')
tt=np.arange(len(t['state']))*.02;dist=np.max(np.abs((t['state']-t['counterfactual'])/model['scale']),axis=1)
fig,axes=plt.subplots(3,1,figsize=(6.8,3.6),sharex=True,layout='constrained')
axes[0].plot(tt,z['scores'][:,0]/cal['thresholds']['Q2']['base'],label='Protected base',color='#285675',lw=1)
axes[0].plot(tt,z['scores'][:,3]/cal['thresholds']['Q2']['following'],label='Following',color='#a95835',lw=1)
axes[0].axhline(1,color='black',ls=':',lw=.8);axes[0].set_yscale('symlog',linthresh=1);axes[0].set_ylim(bottom=0);axes[0].set_ylabel('Score / threshold');axes[0].legend(loc='upper right',fontsize=8)
for m,col,offset in [('base_dual','#285675',1.3),('following_dual','#a95835',0)]:
 axes[1].step(tt,z['alarms'][:,cfg['methods'].index(m)].astype(int)+offset,where='post',color=col,lw=1)
axes[1].set_yticks([.5,1.8],['Following','Protected']);axes[1].set_ylabel('Alarm state');axes[1].text(23,2.55,'Raised line = alarm',ha='right',fontsize=7,color='#666666');axes[1].set_ylim(-.2,2.8)
axes[2].plot(tt,dist,color='#35553e',lw=1);axes[2].axhline(.1,color='black',ls=':',lw=.8,label='Return tolerance');axes[2].set_ylabel('True deviation');axes[2].set_xlabel('Episode time (s)');axes[2].legend(fontsize=8)
for ax in axes:ax.axvspan(cfg['onset']*.02,cfg['end']*.02,color='#999999',alpha=.17);ax.set_xlim(2,24)
fig.savefig(M/'figures/trace.pdf');plt.close(fig)

# All development outcomes, not a refit or a fresh parameter search.
candidates=read(N/'candidates.json')
assert len(candidates)==30 and all(r['status']=='eligible' for r in candidates)
ids=[r['id'] for r in candidates if r['plant']=='Q1']
labels=[('RBF '+k.replace('rbf_','').replace('_',' / ')) if k.startswith('rbf')
        else 'Linear '+k.split('_')[-1] for k in ids]
fig,axes=plt.subplots(1,3,figsize=(7.2,3.05),sharey=True,layout='constrained')
graph_values={'tuning':[], 'tradeoffs':[], 'ablations':[]}
for ax,p in zip(axes,['Q1','Q2','Q3']):
    rows={r['id']:r for r in candidates if r['plant']==p}
    values=[rows[k]['worst_q99'] for k in ids]
    colors=['#285675' if k.startswith('rbf') else '#a95835' for k in ids]
    ax.scatter(values,np.arange(10),c=colors,s=26,zorder=3)
    for y,k in enumerate(ids):
        selected=k in [sel['models'][p]['linear'],sel['models'][p]['rbf']]
        if selected:ax.scatter([values[y]],[y],marker='*',s=120,c='#182e40',zorder=4)
        graph_values['tuning'].append({'plant':p,'candidate':k,'worst_q99':values[y],'selected_within_role':selected})
    ax.set_title(p);ax.set_xlabel('Worst-episode $q_{.99}$')
    ax.set_yticks(np.arange(10),labels,fontsize=8)
    ax.grid(axis='y',color='#e7ebee',lw=.6);ax.tick_params(axis='y',length=0)
    ax.tick_params(axis='x',labelsize=8);ax.ticklabel_format(axis='x',style='plain',useOffset=False)
axes[0].invert_yaxis()
fig.savefig(M/'figures/tuning.pdf');plt.close(fig)

def horizontal_contrasts(filename,methods,display,metrics,height):
    fig,axes=plt.subplots(1,len(metrics),figsize=(7.2,height),sharey=True,layout='constrained')
    colors=['#a95835' if 'following' in k else '#285675' if k.startswith(('base','rbf')) else '#7d858b' for k in methods]
    rows=[]
    for ax,(key,title,fmt,scale) in zip(axes,metrics):
        vals=[pooled[k][key]*scale for k in methods]
        bars=ax.barh(np.arange(len(methods)),vals,color=colors,height=.6)
        ax.set_title(title,fontsize=9);ax.set_yticks(np.arange(len(methods)),display,fontsize=8)
        ax.tick_params(axis='y',length=0);ax.tick_params(axis='x',labelsize=8)
        ax.grid(axis='x',color='#e7ebee',lw=.6);ax.set_axisbelow(True)
        if key=='gap_points':
            ax.set_xscale('symlog',linthresh=1);ax.set_xlim(0,max(2,max(vals))*4)
        else:ax.set_xlim(0,max(vals)*1.28)
        for bar,v in zip(bars,vals):
            ax.annotate(format(v,fmt),(bar.get_width(),bar.get_y()+bar.get_height()/2),
                        xytext=(3,0),textcoords='offset points',va='center',fontsize=8)
    axes[0].invert_yaxis()
    fig.savefig(M/'figures'/filename);plt.close(fig)
    return [{'method':k,**{key:pooled[k][key]*scale for key,_,_,scale in metrics}} for k in methods]
graph_values['tradeoffs']=horizontal_contrasts('tradeoffs.pdf',
 ['base_dual','rbf_dual','rbf_dual_nodwell','following_point','following_dual','persistence_point','mean21_point','base_cusum'],
 ['Base dual','RBF dual','RBF dual, no dwell','Following point','Following dual','Persistence','Mean (21)','Base CUSUM'],
 [('f1','Schedule F1','.3f',1),('benign_fraction','Benign alarms (%)','.2f',100),('gap_points','Pre-return gap points',',.0f',1)],2.8)
graph_values['ablations']=horizontal_contrasts('ablations.pdf',
 ['rbf_point','rbf_return1','rbf_long','rbf_dual','rbf_dual_nodwell'],
 ['Point threshold','Point return + dwell','Long window + dwell','Dual window + dwell','Dual window, no dwell'],
 [('benign_alarms','Benign alarm points',',.0f',1),('premature','Early-clear events',',.0f',1),('gap_points','Pre-return gap points',',.0f',1)],2.1)
(M/'FIGURE_VALUES.json').write_text(json.dumps(graph_values,indent=2)+'\n')
out={str(p.relative_to(M)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(M.rglob('*')) if p.is_file() and ((p.suffix in ['.tex','.pdf'] and p.parent.name in ['figures','generated']) or p.name=='FIGURE_VALUES.json')}
(M/'ASSET_RECEIPT.json').write_text(json.dumps(dict(python=sys.version,numpy=np.__version__,matplotlib=matplotlib.__version__,inputs=inputs,outputs=out,operation='saved-artifact presentation only'),indent=2)+'\n')
print(json.dumps({'tables_figures':len(out),'source_bindings':len(inputs)}))
