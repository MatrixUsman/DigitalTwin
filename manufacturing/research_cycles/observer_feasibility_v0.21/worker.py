import sys,json,time,platform,subprocess,traceback
from datetime import datetime,timezone
from io21 import *
from observers import *

def main(out):
    f=freeze_check();tick=time.perf_counter();enforcement=install_worker_limits(LIMITS)
    w=BudgetWriter(out,limit_bytes=LIMITS.output_bytes,reserve_bytes=LIMITS.parent_reserve_bytes)
    models=bases();fits={};selection={};losses=[];access=[];cache={}
    w.write_json('provenance.json',{'project':'manufacturing','operator':'Codex','requested_author':'Muhammad Usman','utc':datetime.now(timezone.utc).isoformat(),'command':sys.argv,'cwd':str(Path.cwd()),'interpreter':sys.executable,'python':sys.version,'platform':platform.platform(),'dependencies':subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),'revision':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'dirty_state':subprocess.check_output(['git','status','--short'],text=True),'freeze_sha256':sha(HERE/'FREEZE.json'),'enforcement':enforcement,'synthetic':True,'no_attack_access':True})
    for plant in models:
        train=records('K13',plant,access);dev=records('M13',plant,access)
        fits[plant]=fit_noise([y[100:] for y,u,r in train]);selection[plant]={};scale=models[plant]['base']['scale']
        for fam,settings in GRID.items():
            trial=[]
            for setting in settings:
                sq=0.;n=0
                for y,u,r in dev:
                    _,p=estimate(y,fits[plant],fam,setting,cache)
                    e=(p[100:-1]-y[101:])/scale;sq+=float((e*e).sum());n+=e.size
                trial.append({'plant':plant,'family':fam,'setting':setting,'development_mse':sq/n,'scalar_targets':n})
            chosen=min(trial,key=lambda x:(x['development_mse'],x['setting']));selection[plant][fam]=chosen['setting'];losses.extend(trial)
    # Seal actual choices before any calibration record is opened.
    w.write_json('selection.json',{'fits':fits,'settings':selection,'losses':losses,'target':'next noisy observation','calibration_access':False,'truth_access':False})
    w.write_json('selection_access.json',access.copy());selected_sha=sha(out/'selection.json')
    widths={}
    for plant in models:
        widths[plant]={};cal=records('L13',plant,access);scale=models[plant]['base']['scale']
        for fam,s in selection[plant].items():
            scores=[]
            for y,u,r in cal:
                z,_=estimate(y,fits[plant],fam,s,cache);scores.append(np.max(np.abs((z-r)/scale),axis=1)[100:])
            widths[plant][fam]=quantile(np.concatenate(scores))
    w.write_json('calibration.json',{'widths':widths,'quantile':.99,'points_per_plant_family':9900,'selection_sha256':selected_sha})
    w.write_json('access.json',access)
    sim=json.loads((HERE.parent/'recovery_v0.8/FREEZE.json').read_text())['configuration']
    catalog=[];numerical=None
    for ti,task in enumerate(['arctansine','gaussian_pulses']):
        u=command_path(task);initial=np.r_[u[0,:2],0.,0.]
        for pi,old in enumerate(sim['plants8']):
            plant=dict(old,mass=(np.array(old['mass'])*[1.07,.92]).tolist(),damping=(np.array(old['damping'])*[.93,1.08]).tolist(),lag=old['lag']+.006)
            state=physical(initial,u,plant_parameters(sim,plant),permitted(sim),plant['lag'])[:,:4]
            if numerical is None:
                fine=physical(initial,u,plant_parameters(sim,plant),permitted(dict(sim,substeps=sim['substeps']*2)),plant['lag'])[:,:4]
                numerical={'max_abs_difference':float(abs(state-fine).max()),'tolerance':1e-4}
                w.write_json('numerical_check.json',numerical)
                if numerical['max_abs_difference']>=1e-4:raise ValueError('Numerical refinement failed')
            parent=old['id'];scale=models[parent]['base']['scale']
            for ni,noise in enumerate(['iid','ar1','encoder']):
                for seed in [17,42,2026]:
                    rid=f'{task}_{parent}_{noise}_{seed}';noise_seed=2100000+10000*ti+1000*pi+100*ni+seed
                    y=measurement(state,np.array(sim['sensor_sigma'])*plant['noise'],noise,noise_seed)
                    ref=predict(Observation(y,u,np.ones(len(y),bool)),models[parent]['base'],100)
                    estimates=[];alarms=[];bands=[]
                    for fam in GRID:
                        z,_=estimate(y,fits[parent],fam,selection[parent][fam],cache)
                        score=np.max(np.abs((z-ref)/scale),axis=1);a,l,h=set_alarm(score,widths[parent][fam])
                        estimates.append(z);alarms.append(a);bands.append((l<=.1)&(h>.1))
                    w.write_bytes('scores_'+rid+'.npz',packed(estimates=np.stack(estimates,axis=1),alarms=np.stack(alarms,axis=1),bands=np.stack(bands,axis=1),reference=ref,measurements=y,commands=u))
                    w.write_bytes('truth_'+rid+'.npz',packed(state=state))
                    catalog.append({'id':rid,'task':task,'plant':parent,'noise':noise,'seed':seed,'noise_seed':noise_seed})
            print('Sealed normal estimates',task,parent,flush=True)
    w.write_json('catalog.json',catalog)
    w.write_json('SCORES_SEALED.json',{'utc':datetime.now(timezone.utc).isoformat(),'files':{p.name:sha(p) for p in out.glob('*.npz')},'selection_sha256':selected_sha,'truth_joined':False})
    rows=[]
    for item in catalog:
        with np.load(out/('scores_'+item['id']+'.npz'),allow_pickle=False) as z, np.load(out/('truth_'+item['id']+'.npz'),allow_pickle=False) as truth:
            scale=models[item['plant']]['base']['scale'];state=truth['state'];ref_error=(z['reference'][100:]-state[100:])/scale
            for j,fam in enumerate(GRID):
                e=(z['estimates'][100:,j]-state[100:])/scale;a=z['alarms'][100:,j];score=np.max(np.abs((z['estimates'][100:,j]-z['reference'][100:])/scale),axis=1)
                rows.append(dict(**item,family=fam,points=len(a),squared_error_sum=float((e*e).sum()),scalar_values=e.size,rmse=float(np.sqrt(np.mean(e*e))),max_channel_abs_error=np.max(abs(e),axis=0).tolist(),p99_infinity_error=float(np.quantile(np.max(abs(e),axis=1),.99)),alarm_points=int(a.sum()),starts=int(np.sum(a&~np.r_[False,a[:-1]])),unknown_band_points=int(z['bands'][100:,j].sum()),width_coverage=float(np.mean(score<=widths[item['plant']][fam])),reference_rmse=float(np.sqrt(np.mean(ref_error**2)))))
    summary=[]
    for noise in ['all','iid','ar1','encoder']:
        for fam in GRID:
            rr=[r for r in rows if r['family']==fam and (noise=='all' or r['noise']==noise)]
            summary.append({'noise':noise,'family':fam,'episodes':len(rr),'points':sum(r['points'] for r in rr),'rmse':float(np.sqrt(sum(r['squared_error_sum'] for r in rr)/sum(r['scalar_values'] for r in rr))),'alarm_points':sum(r['alarm_points'] for r in rr),'starts':sum(r['starts'] for r in rr),'unknown_band_points':sum(r['unknown_band_points'] for r in rr),'mean_width_coverage':float(np.mean([r['width_coverage'] for r in rr])),'max_episode_p99_infinity_error':max(r['p99_infinity_error'] for r in rr)})
    d={(r['noise'],r['family']):r for r in summary};clauses={}
    for fam in ['raw','mean','uncoupled','kf']:clauses['pooled_rmse_lower_than_'+fam]=d['all','coupled']['rmse']<d['all',fam]['rmse']
    for noise in ['iid','ar1','encoder']:
        for fam in ['uncoupled','kf']:clauses[noise+'_rmse_not_worse_than_'+fam]=d[noise,'coupled']['rmse']<=d[noise,fam]['rmse']
    clauses['benign_points_not_above_raw']=d['all','coupled']['alarm_points']<=d['all','raw']['alarm_points']
    w.write_json('outcomes.json',rows);w.write_json('results.json',{'episodes':len(catalog),'outcomes':len(rows),'summary':summary,'admission':{'passed':all(clauses.values()),'clauses':clauses},'simulation_only':True,'attack_metrics':None,'novelty_established':False,'prospective_normal_evaluation_exposed':True})
    if sha(out/'selection.json')!=selected_sha:raise ValueError('Selection mutated')
    freeze_check()
    w.write_json('completion.json',{'status':'completed','seconds':time.perf_counter()-tick,'usage':worker_usage(),'artifact_sha256':{p.name:sha(p) for p in out.iterdir() if p.is_file() and p.name!='worker.log'}})

if __name__=='__main__':
    out=Path(sys.argv[1])
    try:main(out)
    except BaseException:
        error=traceback.format_exc();print(error,flush=True)
        try:BudgetWriter(out,limit_bytes=LIMITS.output_bytes).write_json('failure.json',{'error':error,'usage':worker_usage()})
        except Exception:pass
        raise
