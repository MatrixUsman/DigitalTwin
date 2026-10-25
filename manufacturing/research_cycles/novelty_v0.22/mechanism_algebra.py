"""Synthetic scalar counterexamples; no robot/data/model benchmark is run."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import math
import platform
import subprocess
import sys
import time


def main():
    wall = time.perf_counter()
    cpu = time.process_time()
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    # The transformed model is deliberately conjugate to the original model.
    # This is an existence counterexample to "subtracting a reference fixes it".
    y_prev, y_next, command = 0.37, 0.42, 0.21
    ref_prev, ref_next = -0.12, 0.08
    mean = lambda y, u: 0.92 * y + 0.17 * u + 0.03
    logvar = lambda y, u: -0.4 + 0.2 * y - 0.1 * u
    raw_error = y_next - mean(y_prev, command)
    z_prev, z_next = y_prev - ref_prev, y_next - ref_next
    transformed_mean = mean(z_prev + ref_prev, command) - ref_next
    transformed_error = z_next - transformed_mean
    raw_score = raw_error ** 2 * math.exp(-logvar(y_prev, command))
    transformed_score = transformed_error ** 2 * math.exp(-logvar(z_prev + ref_prev, command))
    assert math.isclose(raw_error, transformed_error, abs_tol=1e-14)
    assert math.isclose(raw_score, transformed_score, abs_tol=1e-14)

    # Constant offsets in a perfectly fitted linear conditional predictor.
    delta = 0.5
    gain_rows = []
    for gain in [0.0, 0.5, 0.9, 0.99, 1.0]:
        conditional_error = (1.0 - gain) * delta
        reference_error = delta
        gain_rows.append(dict(gain=gain, conditional_error=conditional_error,
                             protected_reference_error=reference_error))
    assert gain_rows[-1]['conditional_error'] == 0.0
    assert gain_rows[-1]['protected_reference_error'] == 0.5

    # Fixed observed prediction error, changing variance: the released score
    # and Gaussian NLL are different quantities. Numbers are illustrative.
    fixed_error = 3.0
    variance_rows = []
    for lv in [0.0, 2.0, 6.0]:
        standardized_square = fixed_error ** 2 * math.exp(-lv)
        nll_without_constant = 0.5 * (standardized_square + lv)
        variance_rows.append(dict(log_variance=lv, squared_error=fixed_error ** 2,
                                 released_score=standardized_square,
                                 nll_without_constant=nll_without_constant))
    assert variance_rows[-1]['released_score'] < 0.03
    assert variance_rows[-1]['nll_without_constant'] > 3.0

    # Global min/max support cannot distinguish a modest conditional offset
    # from a valid value at another authorized phase.
    protected_reference, measured = -0.3, 0.2
    lo, hi = -1.0, 1.0
    in_global_range = lo <= measured <= hi
    intent_distance = abs(measured - protected_reference)
    assert in_global_range and intent_distance == 0.5

    script = Path(__file__).resolve()
    root = script.parents[3]
    def git(*args):
        p = subprocess.run(['git', *args], cwd=root, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return p.stdout.strip()
    result = dict(
        classification='synthetic algebraic software fixtures, not benchmark evidence',
        project='manufacturing', operator='Codex mechanism_audit subagent',
        seed=None, randomness='none', dataset=None, split_hashes=None,
        preprocessing='none', dependencies='Python standard library only',
        interpreter=sys.executable, python=sys.version, platform=platform.platform(),
        machine=platform.machine(), processor=platform.processor(),
        command='python3 research_cycles/novelty_v0.22/mechanism_algebra.py',
        cwd=str(Path.cwd()), git_revision=git('rev-parse', 'HEAD'),
        git_dirty=bool(git('status', '--porcelain')),
        upstream_revision='none executed; released RAPT formula inspected separately',
        script_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),
        started_utc=started, completed_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        wall_seconds=time.perf_counter()-wall, cpu_seconds=time.process_time()-cpu,
        checks=7, configuration=dict(delta=delta, gains=[0.0,0.5,0.9,0.99,1.0],
                                     fixed_prediction_error=fixed_error, log_variances=[0.0,2.0,6.0]),
        coordinate_counterexample=dict(raw_error=raw_error, transformed_error=transformed_error,
                                       raw_score=raw_score, transformed_score=transformed_score),
        conditional_gain_examples=gain_rows, variance_examples=variance_rows,
        range_counterexample=dict(in_global_range=in_global_range,intent_distance=intent_distance),
        interpretation='Existence/identity checks only. No claim about the fitted RAPT Jacobian or causes of its observed errors.'
    )
    output = script.with_name('mechanism_algebra_receipt.json')
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(output=str(output), checks=result['checks'],classification=result['classification'])))


if __name__ == '__main__':
    main()
