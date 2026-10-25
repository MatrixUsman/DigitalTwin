"""Normal-only cost refinement after a conservative pilot admission failure."""
import sys,time,json
from io19 import *
from mechanism19 import alarms
out=Path(sys.argv[1]);limits=Limits(wall_seconds=30,cpu_seconds=20,rss_bytes=1073741824,output_bytes=5242880)
install_worker_limits(limits);w=BudgetWriter(out,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
check(HERE/'DEVELOPMENT_FREEZE.json');check(HERE/'PILOT_FREEZE.json')
models=bases();envelopes=json.loads((LOCAL/'development_001/selected.json').read_text())['models'];cal=json.loads((OLD/'calibration.json').read_text());rows=[]
for plant in models:
    for path in sorted((LOCAL/'pilot_001').glob('pilot_*.npz')):
        z=load_npz(path);obs=Observation(z['measurements'],z['available'],z['valid']);tick=time.perf_counter()
        refs,res,scores=infer(obs,models[plant],cal['cusum_k'][plant],{'warmup':100,'return_tolerance':.1,'dwell':10})
        a,b,lo,hi=alarms(res,scores,obs.valid,cal['thresholds'][plant],models[plant]['base']['scale'],obs.commands,envelopes[plant],residual13)
        payload=packed(measurements=obs.measurements,commands=obs.commands,references=refs,scores=scores,alarms=a,width=b,lower=lo,upper=hi)
        rows.append(dict(parent_model=plant,normal_pilot=path.name,seconds=time.perf_counter()-tick,points=len(a),compressed_score_bytes=len(payload)))
pilot=json.loads((LOCAL/'pilot_001/pilot.json').read_text())
# Per task/plant: normal6000, authorized6000, common attack counterfactual2400,
# four distinct attacked trajectories2400 each. Noise seeds reuse all physics.
unique_physics_points=12*(6000+6000+5*2400)
physics=max(r['seconds']/1200 for r in pilot['rows'])*unique_physics_points
inference=max(r['seconds']/r['points'] for r in rows)*777600
estimate=1.5*physics+2*inference+20
bytes_estimate=max(r['compressed_score_bytes']/r['points'] for r in rows)*777600+777600*70+5000000
numeric=all(r['finite'] and r['max_refinement_difference']<1e-4 for r in pilot['rows'])
w.write_json('resource_admission.json',dict(admitted=bool(numeric and estimate<250 and bytes_estimate<250*1024**2),
    numeric_gate=numeric,previous_failed_admission_preserved=True,scientific_configuration_changed=False,
    unique_physics_points=unique_physics_points,total_observation_points=777600,
    measured_normal_inference_and_compression=rows,physics_estimate_seconds=physics,inference_estimate_seconds=inference,
    conservative_total_estimate_seconds=estimate,estimated_output_bytes=bytes_estimate,
    formula='1.5*unique-cache physics +2*worst measured infer/decision/compression +20s metadata',
    usage=worker_usage(),final_generated=False))
