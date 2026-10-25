# Preparation failures

19 October 2026: first freeze command and subsequent run command both failed during module import, before a freeze, output attempt directory, normal-record loading or simulation. New local `common.py` shadowed a historical module required by `commissioning_v0.9/common9.py`; Python reported `ImportError: cannot import name 'check' from partially initialized module 'common'`.

Renamed the new helper to `io21.py` and updated only new-study imports. No old code or scientific choice changed. The failed commands were `.venv-reproduction-v02/bin/python research_cycles/observer_feasibility_v0.21/freeze.py` and the corresponding `run.py`, from `manufacturing/`. These were preparation failures, not consumed experimental attempts. The corrected freeze must complete before launching the single declared worker attempt.

The corrected freeze completed with140 identities. The first supervised launcher created `local/observer_feasibility_v0.21/normal_001/` and failed after0.0053s because `/bin/ps` was denied by the sandbox. Its terminal supervisor receipt is retained; there is no worker provenance, worker-log content or recorded scientific output. This does not prove that no CPU instruction executed before termination.

The separate `resume_monitor.py` permits only that exact pre-output monitor failure, verifies the original freeze, refuses existing `normal_002`, records its own source hash and the prior failure, and launches the identical worker with the same limits. Monitor-enabled execution completed once in6.142s wall/5.929s CPU. No monitor was disabled and no scientific parameter changed. The prospective admission criterion failed; there was no repeat or attack extension after that outcome.
