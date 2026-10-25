"""Plot saved exploratory scores only; no fitting, simulation or selection."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

M = Path(__file__).resolve().parent
P = M.parent
CACHE = P / "local/manuscript_arx_rbf_v1.8/plot_cache"
CACHE.mkdir(parents=True, exist_ok=True)
os.environ["MPLCONFIGDIR"] = str(CACHE)
os.environ["XDG_CACHE_HOME"] = str(CACHE)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

source = P / "research_cycles/novelty_v0.22/decomposition/STRATA.json"
rows = json.loads(source.read_text())
assert len(rows) == 48
selected = [r for r in rows if r["condition"] == "persistent_offset"]
assert len(selected) == 8
plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "pdf.fonttype": 42})
fig, axes = plt.subplots(1, 2, figsize=(9.8, 2.9), sharey=True,
                         constrained_layout=True)
values = []
for ax, task in zip(axes, ["L19", "S19"]):
    subset = [next(r for r in selected if r["task"] == task
                   and r["channel"] == c) for c in ["q1", "q2", "v1", "v2"]]
    x = np.arange(4)
    error = [r["mean_delta_log_squared_error"] for r in subset]
    variance = [r["mean_variance_contribution"] for r in subset]
    total = [r["mean_delta_log_score"] for r in subset]
    assert np.max(np.abs(np.array(error) + variance - total)) < 2e-5
    ax.bar(x - .17, error, width=.34, color="#256786", label="Squared-error term")
    ax.bar(x + .17, variance, width=.34, color="#cd853f", label="Variance term")
    ax.plot(x, total, "D", color="#242b32", markersize=4, label="Log-score change")
    ax.axhline(0, color="#6f777b", linewidth=.7)
    ax.set_xticks(x, [r"$q_1$", r"$q_2$", r"$v_1$", r"$v_2$"])
    ax.set_title(task + ": persistent offset", fontsize=11)
    ax.set_ylim(-4, 2.6)
    ax.grid(axis="y", alpha=.15)
    ax.set_axisbelow(True)
    values.extend(subset)
axes[0].set_ylabel("Change in mean log value")
axes[1].legend(fontsize=10, loc="upper right", frameon=False)
out = M / "figures/score_decomposition.pdf"
fig.savefig(out)
plt.close(fig)
(M / "DIAGNOSTIC_FIGURE_VALUES.json").write_text(json.dumps({
    "classification": "exploratory arithmetic decomposition, not causal risk attribution",
    "all_retained_source_strata": len(rows), "displayed_prespecified_condition_strata": values
}, indent=2) + "\n")
paths = [source, out, M / "DIAGNOSTIC_FIGURE_VALUES.json", Path(__file__).resolve()]
receipt = {"utc": datetime.now(timezone.utc).isoformat(),
           "command": ".venv-plots-v03/bin/python manuscript_arx_rbf_v1.8/integrate_diagnostics.py",
           "cwd": str(P), "training": False, "new_observations": False,
           "sha256": {str(p.relative_to(P)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in paths}}
(M / "DIAGNOSTIC_ASSETS.json").write_text(json.dumps(receipt, indent=2) + "\n")
print("Saved eight-channel descriptive decomposition figure from all retained strata.")
