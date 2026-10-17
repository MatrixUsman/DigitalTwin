"""Post-exposure analytical noise diagnostic; never changes fits or admission."""
import math,json
from datetime import datetime,timezone
from common9 import HERE,LOCAL,OLD,sha,np
from scipy.special import ndtr
from scipy.optimize import brentq
run=LOCAL/'runs/normal_002';old=json.loads((OLD/'FREEZE.json').read_text())['configuration']
N=5*(old['steps']-old['warmup']);delta=.1;records=[]
for plant in old['plants8']:
    with np.load(run/f'fit_{plant["id"]}_arx_04_1e-07.npz',allow_pickle=False) as z:scale=z['scale']
    sigma=np.array(old['sensor_sigma'])*plant['noise']/scale
    def cdf(x):return math.prod(math.erf(max(x,0)/(math.sqrt(2)*v)) for v in sigma)
    def quantile(prob,power=1):
        lo=0.;hi=1.
        for _ in range(90):
            mid=(lo+hi)/2
            value=power*sum(math.log(max(math.erf(mid/(math.sqrt(2)*v)),1e-300)) for v in sigma)
            if value<math.log(prob):lo=mid
            else:hi=mid
        return hi
    point95=quantile(.95);max95=quantile(.95,N);budget=delta-point95
    probability=math.exp(N*math.log(cdf(budget))) if budget>0 else 0.
    # Independent numerical implementation of the same Gaussian expression.
    F=lambda x:float(np.prod(2*ndtr(x/sigma)-1)) if x>0 else 0.
    independent=brentq(lambda x:F(x)-.95,1e-8,1.,xtol=1e-14)
    assert abs(point95-independent)<1e-12
    independent_probability=math.exp(N*math.log(F(delta-independent))) if delta>independent else 0.
    assert abs(probability-independent_probability)<1e-10
    records.append(dict(plant=plant['id'],standardized_sensor_sigma=sigma.tolist(),point_discrepancy_q95=point95,
        calibration_max_q95=max95,largest_allowance_compatible_with_95pct_population_coverage=budget,
        probability_noise_only_calibration_max_leaves_95pct_population_coverage=probability,
        population_feasibility_at_q95_calibration_max=cdf(delta-max95),independent_numeric_check='passed'))
r=dict(utc=datetime.now(timezone.utc).isoformat(),status='analytical_diagnostic',post_exposure=True,
    assumptions='Hypothetical perfect free reference; conditioned on observed training scales; independent zero-mean Gaussian sensor noise exactly as declared by the simulator. Empirical allowance is maximum of 5x1100 calibration discrepancies. Does not characterize arbitrary real sensors or a complete alarm machine.',
    formula='F(x)=product_j erf(x/(sqrt(2)*sigma_j/scale_j)); P(B<=b)=F(b)^N; population feasibility F(delta-B)>=0.95 iff B<=delta-F^{-1}(0.95).',
    N=N,delta=delta,records=records,source_sha256=sha(__file__),freeze_sha256=sha(HERE/'FREEZE.json'),
    action='Do not change the consumed tolerance, allowance or normal admission. Diagnose noise separately before specifying any new return rule.')
(HERE/'NOISE_DIAGNOSTIC.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
