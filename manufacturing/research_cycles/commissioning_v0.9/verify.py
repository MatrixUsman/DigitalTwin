"""Post-run consistency audit; no model selection change or new observations."""
import json,time
from datetime import datetime,timezone
from common9 import HERE,LOCAL,INPUT,PROJECT,check,sha,np,bank,normal_catalog
from models import fit,predict,Observation
from normal_io import NormalReader

start=time.monotonic();f=check();c=f['configuration'];run=LOCAL/'runs/normal_002';count=0

def ok(condition,message):
    global count
    if not condition:raise AssertionError(message)
    count+=1

def same(a,b,message):ok(np.array_equal(a,b),message)
def read_model(name):
    with np.load(run/name,allow_pickle=False) as z:return {k:z[k] for k in z.files}

for name in ['SELECTION_SEALED.json','NORMAL_SCORES_SEALED.json']:
    d=json.loads((run/name).read_text())
    for k,h in d['sha256'].items():ok(sha(run/k)==h,'seal '+k)
summary=json.loads((run/'summary.json').read_text());ok(summary['status']=='completed','worker completed')
reader=NormalReader(c,f['normal_files']);catalog=normal_catalog(c)
candidates=json.loads((run/'candidates.json').read_text());chosen=json.loads((run/'selection.json').read_text());models={}
ok(len(candidates)==63,'all candidate attempts')
for plant in ['Q1','Q2','Q3']:
    train=[reader.read(r['name'],'train') for r in catalog if r['plant']==plant and r['stage']=='train']
    dev=[reader.read(r['name'],'development') for r in catalog if r['plant']==plant and r['stage']=='development']
    records=[]
    for spec in bank(c):
        record=next(r for r in candidates if r['plant']==plant and r['id']==spec['id'])
        try:m=fit(train,spec,c['warmup'])
        except Exception:
            ok(record['status']=='failed','preserved fit failure');continue
        saved=read_model(f'fit_{plant}_{spec["id"]}.npz');models[(plant,spec['id'])]=saved
        for key in m:same(m[key],saved[key],'fit '+plant+spec['id']+key)
        if spec['kind']=='arx' and float(m['radius'])>=1:
            ok(record['status']=='rejected_unstable','unstable preserved');continue
        ok(record['status']=='eligible','stable status');q=[];rms=[]
        for i,e in enumerate(dev):
            pred=predict(e,m,c['warmup']);d=((e.measurements-pred)/m['scale'])[c['warmup']:];s=np.max(np.abs(d),axis=1)
            q.append(float(np.quantile(s,.99)));rms.append(float(np.sqrt(np.mean(d*d))))
            ok(q[-1]==record['development'][i]['q99'],'dev q99');ok(rms[-1]==record['development'][i]['standardized_rmse'],'dev rmse')
        ok(max(q)==record['worst_development_q99'],'dev worst');ok(float(np.mean(rms))==record['mean_development_rmse'],'dev mean')
        records.append(record)
    for label,kind in [('overall',None),('arx','arx'),('fir','fir')]:
        rr=[r for r in records if kind is None or r['kind']==kind]
        selected=sorted(rr,key=lambda r:(r['worst_development_q99'],r['mean_development_rmse'],r['parameter_count'],r['id']))[0]['id']
        ok(selected==chosen['selected'][plant][label],'independent selection')
    allowance={role:0. for role in chosen['roles'][plant]}
    for row in catalog:
        if row['plant']!=plant or row['stage']!='allowance':continue
        obs=reader.read(row['name'],'allowance')
        for role,mid in chosen['roles'][plant].items():
            m=models[(plant,'arx_04_1e-07' if mid=='command' else mid)]
            ref=obs.commands if mid=='command' else predict(obs,m,c['warmup'],following=role=='one_step_arx4')
            s=np.max(np.abs((obs.measurements-ref)/m['scale']),axis=1)
            allowance[role]=max(allowance[role],float(s[c['warmup']:].max()))
    ok(allowance==chosen['allowances'][plant],'normal allowance')
rows=json.loads((run/'metrics.json').read_text());roster=json.loads((run/'normal_roster.json').read_text())
ok(len(roster)==96 and len(rows)==576,'complete normal outcomes')
ok(sum(r['stage']=='fresh_normal' for r in roster)==81,'81 fresh normals')
for item in roster:
    with np.load(run/(item['id']+'.npz'),allow_pickle=False) as z:
        obs=Observation(z['measurements'],z['commands'],z['valid']);refs=z['references'];scores=z['scores']
    plant=item['plant'];scale=models[(plant,'arx_04_1e-07')]['scale']
    if item['stage']=='fresh_normal':ok(item['condition'] in c['normal_conditions'],'normal-only condition')
    for j,role in enumerate(item['roles']):
        mid=chosen['roles'][plant][role];m=models[(plant,'arx_04_1e-07' if mid=='command' else mid)]
        ref=obs.commands if mid=='command' else predict(obs,m,c['warmup'],following=role=='one_step_arx4')
        same(ref,refs[:,j],'prediction replay');s=np.max(np.abs((obs.measurements-ref)/scale),axis=1);same(s,scores[:,j],'score replay')
        row=next(r for r in rows if r['id']==item['id'] and r['role']==role);b=chosen['allowances'][plant][role];a=s[c['warmup']:]
        ok(row['maximum']==float(a.max()) and row['q99']==float(np.quantile(a,.99)),'error metrics')
        feasible=s+b<=.1;ok(row['feasible_points']==sum(bool(v) for v in feasible[c['warmup']:]),'independent feasible points')
        ok(row['algebraically_feasible']==(b<.1),'algebraic admission')
        for probe in row['probes']:
            first=probe['start'];last=min(len(s)-1,first+c['max_clear_steps']);found=None
            for ending in range(first+c['dwell']-1,last+1):
                if all(bool(v) for v in feasible[ending-c['dwell']+1:ending+1]):found=ending;break
            ok(probe['cleared_at']==found,'independent clearing window')
            ok(probe['delay_steps']==(None if found is None else found-first),'clearance delay')
        ok(row['cleared_probes']==sum(v['cleared_at'] is not None for v in row['probes']),'clearance count')
for stage,name in [('fresh_normal','fresh_summary.json'),('archived_check','archived_summary.json')]:
    s=json.loads((run/name).read_text());admissions=[]
    for r in s['rows']:
        local=[x for x in rows if x['stage']==stage and x['plant']==r['plant'] and x['role']==r['role']]
        eligible=sum(x['eligible'] for x in local);feasible=sum(x['feasible_points'] for x in local);n=sum(len(x['probes']) for x in local);cleared=sum(x['cleared_probes'] for x in local)
        ok(r['eligible']==eligible and r['feasible_points']==feasible and r['cleared_probes']==cleared and r['probes']==n,'aggregate counts')
        decision=r['allowance']<.1 and feasible/eligible>=.95 and cleared/n>=.95
        ok(r['normal_admission']==decision,'independent admission')
        if r['role']=='selected_reference':admissions.append(decision)
    ok(s['selected_reference_admitted_to_alarm_design']==all(admissions),'global admission')
access=json.loads((run/'access.json').read_text());ok(len(access)==66,'66 allowed reads')
ok({r['name'] for r in access}==set(f['normal_files']),'exact input coverage')
ok(all(r['members']==['measurements','available','valid'] for r in access),'restricted observation members')
check();out=dict(utc=datetime.now(timezone.utc).isoformat(),status='passed',checks=count,seconds=time.monotonic()-start,
    scope='All preserved hashes, refitted candidates, development selection, allowances, 576 prediction/score/metric rows; independent clearance windows and admission arithmetic. No new simulation; not independent physics or security validation.',
    freeze_sha256=sha(HERE/'FREEZE.json'),verifier_sha256=sha(__file__),worker_summary_sha256=sha(run/'summary.json'))
(HERE/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
