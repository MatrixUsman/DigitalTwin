"""Synthetic diagnostics of explicitly identified successor source paths.

No dataset loader, training, network access or test-label threshold selection.
Extracted source belongs to the pinned MIT-licensed successor; see NOTICE.md.
"""
import ast
import hashlib
import json
from pathlib import Path

import numpy as np

EDGE_NOTEBOOK_SHA256 = "46bf5121bf6c2a4420d41f3914b23e0ccebc424891265c56f24386fb67ab07a0"


def cells_from_verified_notebook(path):
    data = Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest() != EDGE_NOTEBOOK_SHA256:
        raise ValueError("Pinned notebook identity mismatch")
    return ["".join(c.get("source", [])) for c in json.loads(data)["cells"]]


def prediction_target_indices(n, history, horizon):
    """Each row contains the genuine future targets of one forecasting window."""
    if min(history, horizon) < 1 or n < history + horizon:
        raise ValueError("Invalid forecasting support")
    return np.arange(n - history - horizon + 1)[:, None] + history + np.arange(horizon)


def aligned_rmse(predictions, observations, target_indices):
    predictions, observations = np.asarray(predictions), np.asarray(observations)
    target_indices = np.asarray(target_indices)
    if target_indices.dtype.kind not in "iu" or np.any(target_indices < 0):
        raise ValueError("Invalid target indices")
    if np.any(target_indices >= len(observations)):
        raise ValueError("Target outside observations")
    target = observations[target_indices]
    if predictions.shape != target.shape:
        raise ValueError("Prediction/target shape mismatch")
    if not np.isfinite(predictions).all() or not np.isfinite(target).all():
        raise ValueError("Nonfinite prediction/target")
    return np.sqrt(np.mean((predictions - target) ** 2, axis=-1))


class IdentityScaler:
    def inverse_transform(self, values):
        return np.asarray(values)


class ArrayModel:
    """Explicitly synthetic fake predictor used to isolate scorer behavior."""
    def __init__(self, values):
        self.values = values

    def predict(self, *args, **kwargs):
        return self.values.copy()


def source_diagnostics(cells):
    import pandas as pd
    from types import SimpleNamespace

    result = {"evidence_kind": "synthetic software diagnostics, not benchmark results"}
    # Execute only the score prefix, not the notebook's loaders or fitting cells.
    values = np.repeat(np.arange(200, dtype=float)[:, None], 9, axis=1)
    fake_predictions = values[30:, None, :]
    namespace = {"np": np, "cnn_model": ArrayModel(fake_predictions),
                 "w1": SimpleNamespace(test=None), "scaler_X": IdentityScaler(),
                 "test_data": pd.DataFrame(values)}
    prefix = cells[245].split("# Predict hitting arm.")[0]
    try:
        exec(compile(prefix, "edge_main.ipynb:cell245:prefix", "exec"), namespace)
    except ValueError as exc:
        result["D1"] = {"observed": "ValueError", "message": str(exc),
                        "predictions": len(fake_predictions), "hardcoded_targets": len(values)-45,
                        "source_history": 30, "source_target_offset": 45}
    else:
        raise AssertionError("Expected saved branch's 30/45 mismatch not reproduced")

    # Run the exact audited function, with perfect *future* predictions supplied.
    tree = ast.parse(cells[281])
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                    and n.name == "calculate_anomaly_rmse")
    module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    namespace = {"np": np}
    exec(compile(module, "edge_main.ipynb:cell281:function", "exec"), namespace)
    indices = prediction_target_indices(len(values), 45, 45)
    perfect = values[indices]
    wrong = namespace["calculate_anomaly_rmse"](
        pd.DataFrame(values), None, IdentityScaler(), ArrayModel(perfect), window_size=45)
    correct = aligned_rmse(perfect, values, indices)
    result["D2"] = {"synthetic_perfect_future_predictions": True,
                    "scoring_windows": len(perfect),
                    "upstream_l2_window_score_min": float(wrong.min()),
                    "upstream_l2_window_score_max": float(wrong.max()),
                    "correct_future_rmse_max": float(correct.max()),
                    "offset_rows": 45, "source_norm": "sqrt(sum), not root mean square"}

    # Cell 283 reads rmse_per_row_*; cell 281 defines rmse_per_window_*.
    active = ast.parse(cells[283])
    reads = sorted({n.id for n in ast.walk(active) if isinstance(n, ast.Name)
                    and isinstance(n.ctx, ast.Load) and n.id.startswith("rmse_per_")})
    writes = sorted({n.id for n in ast.walk(tree) if isinstance(n, ast.Name)
                     and isinstance(n.ctx, ast.Store) and n.id.startswith("rmse_per_")})
    slice_start = cells[283].index("    rmse_sliding_sums_test =")
    slice_end = cells[283].index("    # Concatenate RMSE arrays")
    import textwrap
    sums_source = textwrap.dedent(cells[283][slice_start:slice_end])
    ns = {"np": np, "size": 45}
    ns.update({name: np.arange(100, dtype=float) for name in reads})
    exec(compile(sums_source, "edge_main.ipynb:cell283:rolling_sums", "exec"), ns)
    before = ns["rmse_sliding_sums_test"].copy()
    ns.update({name: np.full(100, 1e6) for name in writes})
    exec(compile(sums_source, "edge_main.ipynb:cell283:rolling_sums", "exec"), ns)
    result["D3"] = {"reads": reads, "cell281_writes": writes,
                    "score_unchanged_when_lstm_window_scores_change": bool(
                        np.array_equal(before, ns["rmse_sliding_sums_test"])),
                    "boundary": "Saved sequential code path; paper-producing execution unknown"}
    a, b = np.array([9.] + [0.]*8), np.full(9, 1.1)
    result["D4"] = {"a_notebook_rmse": float(np.sqrt(np.mean(a*a))),
                    "b_notebook_rmse": float(np.sqrt(np.mean(b*b))),
                    "a_embedded_sum_abs": float(np.abs(a).sum()),
                    "b_embedded_sum_abs": float(np.abs(b).sum()),
                    "ordering_reverses": True}
    return result
