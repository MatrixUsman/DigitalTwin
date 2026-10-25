import sys,json,time,platform,subprocess,traceback
from datetime import datetime,timezone
from io19 import *
from mechanism19 import *
from sim19 import generate

def normal_records(plant,task):
    rows=[]
    for path in sorted(NORMAL.glob(f'normal_{task}_{plant}_*.npz')):
        z=load_npz(path);score=np.max(np.abs(z['residuals'][:,0]),axis=1)
        rows.append((z['commands'],score))
    if len(rows)!=9:raise ValueError('Expected nine normal observations per stage/plant')
    return rows

def development(w,c):
    models=bases();fits={};rows=[]
    for memory in c['memory_candidates']:
        totals=dict(memory=memory,alarms=0,starts=0,width_sum=0.,points=0);fits[str(memory)]={}
        for plant in models:
            scale=models[plant]['base']['scale'];train=normal_records(plant,'K13');cal=normal_records(plant,'L13');dev=normal_records(plant,'M13')
            m=fit_envelope(train,cal,scale,memory);fits[str(memory)][plant]=m
            for i,(u,s) in enumerate(dev):
                b=widths(u,scale,m);a,lo,hi=set_alarm(s,b);n=len(a)-START
                starts=int((a&~np.r_[False,a[:-1]])[START:].sum());alarms=int(a[START:].sum())
                rows.append(dict(memory=memory,plant=plant,episode=i,eligible=n,alarms=alarms,starts=starts,
                    envelope_coverage=float(np.mean(s[START:]<=b[START:])),mean_width=float(b[START:].mean())))
                totals['alarms']+=alarms;totals['starts']+=starts;totals['width_sum']+=float(b[START:].sum());totals['points']+=n
        totals['mean_width']=totals['width_sum']/totals['points'];rows.append(dict(selection_totals=totals))
    candidates=[r['selection_totals'] for r in rows if 'selection_totals' in r]
    selected=min(candidates,key=lambda r:(r['alarms'],r['starts'],r['mean_width'],r['memory']))
    w.write_json('development.json',dict(candidates=candidates,episode_diagnostics=[r for r in rows if 'memory' in r],fits=fits,
        selected_memory=selected['memory'],attack_access=False,source='exposed synthetic normal K13/L13/M13 task partitions'))
    w.write_json('selected.json',dict(memory=selected['memory'],models=fits[str(selected['memory'])],selection=selected))
    print('Selected normal-only memory',selected['memory'],flush=True)

def pilot(w,c):
    sim=json.loads((HERE.parent/'recovery_v0.8/FREEZE.json').read_text())['configuration'];p=sim['plants8'][1];rows=[]
    # Pilot-only paths differ from final configurations; all intervals are normal.
    for task in [dict(id='pilot_s',kind='smoothstep',amplitude=[.23,.28],frequency=.12,phase=.2,onset=400,duration=200,brief=10,offset=.1,slow=.7),
                 dict(id='pilot_l',kind='lissajous',amplitude=[.25,.30],frequency=.48,phase=.6,onset=400,duration=200,brief=10,offset=.1,slow=.7)]:
        tick=time.perf_counter();ep=generate(sim,task,p,'normal',190019,physical,plant_parameters,permitted,{},n=1200)
        elapsed=time.perf_counter()-tick
        refined=generate(dict(sim,substeps=sim['substeps']*2),task,p,'normal',190019,physical,plant_parameters,permitted,{},n=1200)
        error=float(np.max(np.abs(ep['state']-refined['state'])))
        rows.append(dict(task=task['id'],seconds=elapsed,max_refinement_difference=error,finite=bool(np.isfinite(ep['measurements']).all())))
        w.write_bytes(task['id']+'.npz',packed(**ep))
    # Conservative un-cached trajectory scaling; final uses seed-shared cached physics.
    estimate=max(r['seconds'] for r in rows)*(777600/1200)*2
    admitted=all(r['finite'] and r['max_refinement_difference']<1e-4 for r in rows) and estimate<250
    w.write_json('pilot.json',dict(rows=rows,estimated_final_seconds=estimate,admitted=admitted,final_generated=False))
    if not admitted:raise ValueError('Pilot cost/numerical gate failed; no final generation admitted')

def final(w,c):
    sim=json.loads((HERE.parent/'recovery_v0.8/FREEZE.json').read_text())['configuration'];models=bases()
    envelopes=json.loads((LOCAL/'development_001/selected.json').read_text())['models']
    thresholds=json.loads((OLD/'calibration.json').read_text());dc={'warmup':100,'return_tolerance':.1,'dwell':10,'recovery_horizon':250}
    plants=[]
    for pp in sim['plants8']:
        p=dict(pp,parent=pp['id'],group='matched');plants.append(p)
        shift=c['plant_shift'];p=dict(pp,id='U'+pp['id'][1:],parent=pp['id'],group='shifted',
            mass=(np.array(pp['mass'])*shift['mass_multiplier']).tolist(),damping=(np.array(pp['damping'])*shift['damping_multiplier']).tolist(),lag=pp['lag']+shift['lag_addition']);plants.append(p)
    catalog=[];timings=[]
    for ti,task in enumerate(c['tasks']):
        for pi,plant in enumerate(plants):
            cache={};parent=plant['parent'];scale=models[parent]['base']['scale']
            for seed in c['seeds']:
                for condition in c['conditions']:
                    rid=f'{task["id"]}_{plant["id"]}_{seed}_{condition}';noise_seed=1900000+ti*100000+pi*5000+seed
                    ep=generate(sim,task,plant,condition,noise_seed,physical,plant_parameters,permitted,cache)
                    obs=Observation(ep['measurements'],ep['available'],ep['valid']);tick=time.perf_counter()
                    refs,res,scores=infer(obs,models[parent],thresholds['cusum_k'][parent],dc)
                    a,b,lower,upper=alarms(res,scores,obs.valid,thresholds['thresholds'][parent],scale,obs.commands,envelopes[parent],residual13)
                    timings.append(dict(id=rid,seconds=time.perf_counter()-tick,points=len(a)))
                    w.write_bytes('score_'+rid+'.npz',packed(measurements=obs.measurements,commands=obs.commands,valid=obs.valid,
                        references=refs,scores=scores,alarms=a,width=b,lower=lower,upper=upper,
                        context_extrapolation=context(obs.commands,scale,envelopes[parent]['memory'])>envelopes[parent]['training_max_context']))
                    w.write_bytes('truth_'+rid+'.npz',packed(state=ep['state'],counterfactual=ep['truth_reference'],attack=ep['attack'],authorized=ep['authorized']))
                    catalog.append(dict(id=rid,plant=plant['id'],parent=parent,plant_group=plant['group'],task=task['id'],seed=seed,noise_seed=noise_seed,condition=condition))
            print('Sealed predictions',task['id'],plant['id'],flush=True)
    w.write_json('catalog.json',catalog);w.write_json('timings.json',timings)
    w.write_json('SCORES_SEALED.json',dict(utc=datetime.now(timezone.utc).isoformat(),outcomes_read=False,
        bindings={p.name:sha(p) for p in w.output_dir.glob('*.npz')}))
    rows=[]
    for item in catalog:
        z=load_npz(w.output_dir/('score_'+item['id']+'.npz'));t=load_npz(w.output_dir/('truth_'+item['id']+'.npz'));scale=models[item['parent']]['base']['scale']
        for j,method in enumerate(METHODS):
            a=z['alarms'][:,j];row=evaluate(a,t['attack'],t['state'],t['counterfactual'],scale,dc)
            extra=extra_metrics(a,t['attack'],t['state'],t['counterfactual'],scale)
            # Joint support includes detection delay; no unobserved samples dropped.
            joint=bool(row['overlap'] and extra['outside_inactive']==0 and row['clear_timely'] and not row['return_missing'])
            rows.append(dict(**item,method=method,**row,**extra,joint=joint,context_extrapolation_points=int(z['context_extrapolation'][START:].sum())))
    summary=summarize(rows);w.write_json('outcomes.json',rows)
    w.write_json('results.json',dict(episodes=len(catalog),outcomes=len(rows),summary=summary,primary=criterion(summary),
        simulation_only=True,final_exposed=True,novelty_established=False,scope='bounded prospectively frozen within-simulator transfer study'))

def main(phase,out):
    tick=time.monotonic();f=check(HERE/(phase.upper()+'_FREEZE.json'));c=f['configuration'];lim=Limits(**c['limits'][phase]);enforcement=install_worker_limits(lim)
    w=BudgetWriter(out,limit_bytes=lim.output_bytes,reserve_bytes=lim.parent_reserve_bytes)
    w.write_json('provenance.json',dict(utc=datetime.now(timezone.utc).isoformat(),phase=phase,configuration=c,operator='Codex',requested_author='Muhammad Usman',
        command=sys.argv,cwd=str(Path.cwd()),interpreter=sys.executable,python=sys.version,platform=platform.platform(),
        dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),
        git_revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),git_status=subprocess.check_output(['git','status','--short'],text=True),
        enforcement=enforcement,freeze_sha256=sha(HERE/(phase.upper()+'_FREEZE.json')),synthetic=True,raw_dataset_access=False))
    globals()[phase](w,c);check(HERE/(phase.upper()+'_FREEZE.json'))
    w.write_json('completion.json',dict(status='completed',wall_seconds=time.monotonic()-tick,usage=worker_usage(),
        utc=datetime.now(timezone.utc).isoformat(),artifact_sha256={p.name:sha(p) for p in out.iterdir() if p.is_file() and p.name!='worker.log'}))

if __name__=='__main__':
    phase=sys.argv[1];out=Path(sys.argv[2])
    try:main(phase,out)
    except BaseException:
        error=traceback.format_exc();print(error,flush=True)
        try:BudgetWriter(out,limit_bytes=262144000).write_json('failure.json',dict(traceback=error,usage=worker_usage()))
        except Exception:pass
        raise
