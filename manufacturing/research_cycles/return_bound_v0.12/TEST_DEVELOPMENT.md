# Pre-freeze development record

No study trace was generated during software development.

1. AST inspection identified a verifier comparison requiring parentheses around `not(...)`; corrected before tests. Static inspection also corrected the recorded resource key to the existing supervisor's `process_cpu_seconds`.
2. Synthetic test attempt `local/return_bound_v0.12/tests/test_001` ran 20 tests: 19 passed; the gap-clock test failed an exact floating-point equality. Its largest difference was 2.77555756e-17, caused by different cumulative-sum roundoff after removing a missing input. The source snapshot, receipt and full failure log are preserved there.
3. Corrected only that numerical assertion to absolute tolerance 1e-15 (zero relative tolerance); the control, error budget and scientific design did not change. The test still requires the same global clock after the gap. The test runner now takes an explicit fresh attempt name and records tested source identities. The next command is `freeze.py --test-attempt test_002` using the project research interpreter. This is a software-test correction, not a rerun selected from experiment outcomes.
