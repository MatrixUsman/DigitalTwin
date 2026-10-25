"""Synthetic tensor runtime estimate only; no research data read."""
from pathlib import Path
import sys,time,json,io,hashlib,platform,subprocess
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parents[1]
sys.path.insert(0,str(P/'src'))
from mfg_twin.supervisor import Limits,BudgetWriter,install_worker_limits,worker_usage
limits=Limits(wall_seconds=45,cpu_seconds=30,rss_bytes=1073741824,output_bytes=5242880)
install_worker_limits(limits)
out=Path(sys.argv[1]);writer=BudgetWriter(out,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
import numpy as np,torch
torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
from models23 import *
cfg=json.loads((H/'config.json').read_text());rng=np.random.default_rng(230017)
started=datetime.now(timezone.utc).isoformat();tick=time.process_time()
# Synthetic independent arrays, deliberately no invocation of the robot simulator.
ys=[rng.normal(size=(1200,4)) for _ in range(9)];us=[rng.normal(size=(1200,4)) for _ in range(9)]
devy=[rng.normal(size=(1200,4)) for _ in range(9)];devu=[rng.normal(size=(1200,4)) for _ in range(9)]
scale=fit_scale(ys,us);norm=lambda xs,prefix:[(x-scale[prefix+'_mean'])/scale[prefix+'_std'] for x in xs]
ys,us,devy,devu=norm(ys,'y'),norm(us,'u'),norm(devy,'y'),norm(devu,'u')
w=reference_fit(ys,us);zs=[y-reference_predict(u,w) for y,u in zip(ys,us)];ds=[y-reference_predict(u,w) for y,u in zip(devy,devu)];cs=[context(u) for u in us];dc=[context(u) for u in devu]
train=windows(zs,cs);dev=windows(ds,dc);prep_cpu=time.process_time()-tick
model=Adapter(.5,.25);tick=time.process_time();history,flag=train_adapter(model,train,dev,epochs=3);train_cpu=time.process_time()-tick
tick=time.process_time();pred=adapter_predict_many(model,zs+ds,cs+dc);inference_cpu=time.process_time()-tick
tick=time.process_time();linear=[]
for k in [.25,.5,.75,None]:
    mm=fir_fit(zs,cs,k,max_iterations=cfg['fir']['max_iterations'],tol=cfg['fir']['projected_gradient_tolerance']);linear.append(dict(kappa=k,converged=mm['converged'],iterations=mm['iterations']))
linear_cpu=time.process_time()-tick
epoch_cost=train_cpu/3.;fixed_estimate=prep_cpu+9*inference_cpu+4*linear_cpu+8.
estimates={str(epochs):dict(raw_cpu=fixed_estimate+9*epochs*epoch_cost,with_50pct_margin=1.5*(fixed_estimate+9*epochs*epoch_cost)) for epochs in [12,20,40,60,80,100]}
record=dict(classification='synthetic runtime fixture, not model or benchmark performance',utc=started,seed=230017,
    configuration=cfg,interpreter=sys.executable,python=sys.version,platform=platform.platform(),dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),
    git_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip(),git_dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=P,text=True)),
    command=sys.argv,cwd=str(P),dataset=None,real_normal_data_opened=False,source_bindings={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in list(H.glob('*.py'))+[H/'config.json',H/'PROTOCOL.md']},
    tensor_batches=list(train[0].shape),neural_parameter_count=sum(x.numel() for x in model.parameters()),preparation_cpu=prep_cpu,three_epoch_cpu=train_cpu,all18_episode_inference_cpu=inference_cpu,
    four_linear_fit_cpu=linear_cpu,linear_diagnostics=linear,estimates=estimates,usage=worker_usage(),estimate_not_guarantee=True)
writer.write_json('runtime.json',record)
print(json.dumps(dict(estimates=estimates,usage=record['usage'])))
