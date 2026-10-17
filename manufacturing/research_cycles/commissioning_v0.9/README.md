# Clean commissioning and reference adequacy v0.9

[Results](RESULTS.md) · [all 63 candidates](MODEL_BANK.md) · [normal-only plan](PLAN.md) · [scientific decision](DECISION.md) · [prior art](PRIOR_ART.md) · [figure](../../output/commissioning_v0.9/normal_reference_adequacy.png).

Completed a finite, prospectively specified normal-only experiment: 21 ordinary ARX/FIR configurations per plant, selection/allowance fitting on separate normal episodes, fifteen archived checks and 81 newly generated normal episodes. No attack experiment. Model computations receive only a restricted observation object; no true state/parameters/labels enter prediction.

Selected ARX orders 8/16/32 improve normal predictions versus the matched ARX(4). Q2's allowance falls by 51.27%, enabling all 108 normal clearance probes; it still misses the 95% point-feasibility requirement. Q3 improves by 38.56% in allowance but remains above tolerance. The overall gate fails. The subsequent Gaussian noise calculation explains why the maximum-plus-discrepancy rule can remain unsuitable even with a perfect reference. This calculation is post-study diagnosis and changes no frozen choice.

Twenty-three synthetic tests and 10,293 post-run checks passed, plus one reporting-merge regression. The first worker failed after normal selection, before fresh generation, on a duplicate reporting key. The separate reporting fix preserved the original worker and asserts byte-identical fits and identical scientific selection records before fresh generation. No model or threshold changed. All attempts remain under `local/commissioning_v0.9/runs/`.

Commands from `/Users/matrixusman/CUI/DigitalTwin` (historical launches must not be rerun into occupied directories):

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/commissioning_v0.9/freeze.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/commissioning_v0.9/run.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/commissioning_v0.9/run_reporting_fix.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/commissioning_v0.9/verify.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/commissioning_v0.9/noise_diagnostic.py
manufacturing/.venv-plots-v03/bin/python manufacturing/research_cycles/commissioning_v0.9/present.py
```

The existing isolated interpreter and supervisor record single-thread BLAS, revisions/dirty state, dependencies, CPU/wall/RSS/output limits, source hashes and failures. Old scientific inputs and PDFs remain unchanged. Mutable handoffs are archived before updates. The title AFTER is still provisional. ARX/FIR are established controls; no new-method novelty, attack benefit, physical validation or journal readiness follows from this milestone. Author facts and full paper-level reproductions remain unresolved.
