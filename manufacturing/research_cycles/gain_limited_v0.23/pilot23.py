"""Finite normal-only comparison; all selection is exposed development."""
import io,time
import numpy as np
import torch
from models23 import *

def finite_pilot(fit_rows,dev_rows,ys,us,dys,dus,cfg,writer):
    scale=fit_scale(ys,us)
    norm=lambda values,prefix:[(x-scale[prefix+'_mean'])/scale[prefix+'_std'] for x in values]
    ys,us,dys,dus=norm(ys,'y'),norm(us,'u'),norm(dys,'y'),norm(dus,'u')
    ref=reference_fit(ys,us,cfg['reference']['lags'],cfg['reference']['ridge'])
    bs=[reference_predict(u,ref,cfg['reference']['lags']) for u in us];dbs=[reference_predict(u,ref,cfg['reference']['lags']) for u in dus]
    zs=[y-b for y,b in zip(ys,bs)];dzs=[y-b for y,b in zip(dys,dbs)];cs=[context(u) for u in us];dcs=[context(u) for u in dus]
    buf=io.BytesIO();np.savez_compressed(buf,reference=ref,**scale);writer.write_bytes('common_reference.npz',buf.getvalue())
    common=dict(fit_rows=fit_rows,development_rows=dev_rows,reference=cfg['reference'],normalization=cfg['normalization'],channels=['q1','q2','v1','v2'],scale=1.)
    writer.write_json('common_contract.json',common)
    buf=io.BytesIO();np.savez_compressed(buf,fit_y=np.stack(ys),fit_u=np.stack(us),fit_base=np.stack(bs),fit_context=np.stack(cs),
        development_y=np.stack(dys),development_u=np.stack(dus),development_base=np.stack(dbs),development_context=np.stack(dcs))
    writer.write_bytes('normalized_records.npz',buf.getvalue())
    train=windows(zs,cs);dev=windows(dzs,dcs);records=[];context_cache={};linear_status=[]
    def register(name,corr,dcorr,cert,family,simple,kappa=None,extra=None):
        if len(corr)!=9 or len(dcorr)!=9 or any(a.shape!=(1200,4) or not np.isfinite(a).all() for a in corr+dcorr):raise ValueError('Invalid fitted prediction population')
        residual=[z-a for z,a in zip(dzs,dcorr)];met=metrics(residual,cert,cfg['quantile']);conditions={}
        for condition in cfg['conditions']:
            rr=[residual[i][START:] for i,r in enumerate(dev_rows) if r['condition']==condition]
            conditions[condition]=float(np.sqrt(np.mean(np.concatenate(rr)**2)))
        record=dict(id=name,family=family,simple_comparator=simple,kappa_budget=kappa,metrics=met,condition_rmse=conditions,extra=extra or {})
        records.append(record);buf=io.BytesIO();np.savez_compressed(buf,correction=np.stack(dcorr),residual=np.stack(residual))
        writer.write_bytes('prediction_'+name+'.npz',buf.getvalue());return record
    zero=[np.zeros_like(z) for z in zs];dzero=[np.zeros_like(z) for z in dzs]
    register('direct_reference',zero,dzero,dict(K=0.,C=0.),'direct',True)
    specs=[('context_r'+str(r),None,r,'context') for r in cfg['tanh']['rho']]
    specs += [('tanh_k'+str(k)+'_r'+str(r),k,r,'constrained') for k in cfg['tanh']['kappa'] for r in cfg['tanh']['rho']]
    specs += [('unconstrained_tanh',None,.25,'unconstrained')]
    for name,k,r,kind in specs:
        tick=time.perf_counter();model=Adapter(k,r,cfg['tanh']['width'],cfg['model_seed'],kind)
        history,underfit=train_adapter(model,train,dev,cfg['tanh']['epochs'],cfg['tanh']['learning_rate'],cfg['tanh']['weight_decay'])
        cert=model.certificate()
        if kind=='constrained' and (cert['K']>k or cert['C']>k or cert['rho']>=r):raise ValueError('Final constraint certificate violation')
        predictions=adapter_predict_many(model,zs+dzs,cs+dcs);a,da=predictions[:9],predictions[9:]
        blob=io.BytesIO();torch.save(model.state_dict(),blob);writer.write_bytes('model_'+name+'.pt',blob.getvalue())
        blob=io.BytesIO();np.savez_compressed(blob,**{key:value.detach().numpy() for key,value in model.state_dict().items()});writer.write_bytes('model_'+name+'.npz',blob.getvalue())
        writer.write_json('history_'+name+'.json',history)
        register(name,a,da,cert,kind,kind=='context',k,dict(underfit_flag=underfit,fit_seconds=time.perf_counter()-tick,epochs=len(history),parameter_count=sum(p.numel() for p in model.parameters())))
        if kind=='context':context_cache[name]=(a,da)
    def fit_fir(name,fit_z,dev_z,k,base_corr=None):
        f=cfg['fir'];model=fir_fit(fit_z,cs,k,f['lags'],f['ridge'],f['max_iterations'],f['projected_gradient_tolerance']);linear_status.append(dict(id=name,converged=model['converged'],iterations=model['iterations'],gradient_mapping=model['gradient_mapping']))
        metadata={key:value for key,value in model.items() if key!='weight'};buf=io.BytesIO();np.savez_compressed(buf,weight=model['weight']);writer.write_bytes('model_'+name+'.npz',buf.getvalue());writer.write_json('model_'+name+'.json',metadata)
        a=[fir_predict(z,c,model) for z,c in zip(fit_z,cs)];da=[fir_predict(z,c,model) for z,c in zip(dev_z,dcs)]
        if base_corr is not None:
            a=[x+y for x,y in zip(a,base_corr[0])];da=[x+y for x,y in zip(da,base_corr[1])]
        register(name,a,da,dict(K=model['K'],C=None),'additive_fir' if base_corr else 'fir',True,k,metadata)
        return model
    for k in cfg['tanh']['kappa']:fit_fir('fir_k'+str(k),zs,dzs,k)
    for context_name,(a,da) in context_cache.items():
        residual=[z-x for z,x in zip(zs,a)];dresidual=[z-x for z,x in zip(dzs,da)]
        for k in cfg['tanh']['kappa']:fit_fir(context_name+'_fir_k'+str(k),residual,dresidual,k,(a,da))
    unbounded=fit_fir('unconstrained_fir',zs,dzs,None)
    for cap in cfg['tanh']['kappa']:
        a=[fir_predict(z,c,unbounded,cap) for z,c in zip(zs,cs)];da=[fir_predict(z,c,unbounded,cap) for z,c in zip(dzs,dcs)]
        register('saturated_fir_cap'+str(cap),a,da,dict(K=unbounded['K'],C=cap),'saturated_fir',True,None,dict(cap=cap,source_model='unconstrained_fir'))
    for k in cfg['tanh']['kappa']:
        for r in cfg['tanh']['rho']:
            register('leaky_k'+str(k)+'_r'+str(r),[leaky(z,k,r) for z in zs],[leaky(z,k,r) for z in dzs],dict(K=k,C=None),'leaky',True,k,dict(rho=r))
    for ratio in cfg['kalman']['process_measurement_ratios']:
        a=[kalman(z,ratio)[0] for z in zs];da=[kalman(z,ratio)[0] for z in dzs]
        register('kf_ratio'+str(ratio),a,da,dict(K=1.,C=None),'kalman',True,None,dict(ratio=ratio,gain=kalman(zs[0],ratio)[1]))
    if len(records)!=33:raise ValueError('Finite roster count mismatch')
    writer.write_json('linear_solver_status.json',linear_status)
    return records,linear_status

def admission(records,linear_status,cfg):
    order=lambda r:(r['metrics']['primary_radius'],r['metrics']['rmse'],r['id'])
    candidate=min([r for r in records if r['family']=='constrained'],key=order)
    simple=min([r for r in records if r['simple_comparator'] and r['metrics']['primary_radius'] is not None],key=order)
    same=min([r for r in records if r['family'] in ['fir','additive_fir'] and r['kappa_budget']==candidate['kappa_budget']],key=order)
    a,b,c=candidate['metrics'],simple['metrics'],same['metrics'];gate=cfg['admission']
    radius_gain=1-a['primary_radius']/b['primary_radius'] if b['primary_radius']>0 else None
    rmse_gain=1-a['rmse']/b['rmse'] if b['rmse']>0 else None
    clauses=dict(radius_5pct=radius_gain is not None and radius_gain>=gate['radius_relative_reduction'],
        rmse_2pct=rmse_gain is not None and rmse_gain>=gate['rmse_relative_reduction'],
        all_episodes_within_5pct=all(x<=y*(1+gate['max_episode_rmse_relative_increase']) for x,y in zip(a['episode_rmse'],b['episode_rmse'])),
        all_conditions_within_5pct=all(candidate['condition_rmse'][k]<=simple['condition_rmse'][k]*(1+gate['max_condition_rmse_relative_increase']) for k in cfg['conditions']),
        same_budget_fir_radius_lower=a['primary_radius']<c['primary_radius'],same_budget_fir_rmse_not_higher=a['rmse']<=c['rmse'],
        linear_solvers_converged=all(r['converged'] for r in linear_status),complete_roster=len(records)==33)
    return dict(passed=all(clauses.values()),scope='worker scientific clauses only; FINAL_ADMISSION includes execution integrity',clauses=clauses,candidate=candidate['id'],simple_comparator=simple['id'],same_budget_fir=same['id'],radius_reduction=radius_gain,rmse_reduction=rmse_gain,
        candidate_underfit_flag=candidate['extra']['underfit_flag'],operational_tolerance_established=False,fresh_attack_admitted=False,novelty_established=False)
