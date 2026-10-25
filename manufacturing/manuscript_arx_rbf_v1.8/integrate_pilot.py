"""Present all completed finite-pilot outcomes without fitting or selection."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os

M = Path(__file__).resolve().parent
P = M.parent
R = P / "local/gain_limited_v0.23/normal_001"
S = P / "research_cycles/gain_limited_v0.23"
cache = P / "local/manuscript_arx_rbf_v1.8/plot_cache"
cache.mkdir(parents=True, exist_ok=True)
os.environ["MPLCONFIGDIR"] = str(cache)
os.environ["XDG_CACHE_HOME"] = str(cache)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = json.loads((R / "methods.json").read_text())
decision = json.loads((R / "FINAL_ADMISSION.json").read_text())
run = json.loads((R / "result.json").read_text())
assert run["status"] == "completed" and len(rows) == run["methods"] == 33
assert all(decision["execution_clauses"].values())
lookup = {r["id"]: r for r in rows}
selected = decision["scientific"]


def label(row, latex=False):
    key = row["id"]
    exact = {"direct_reference": "Direct reference", "unconstrained_tanh": "Unconstrained tanh",
             "unconstrained_fir": "Unconstrained FIR"}
    if key in exact:
        text = exact[key]
    elif key.startswith("kf_ratio"):
        text = key.replace("kf_ratio", "KF q/r=")
    elif key.startswith("saturated_fir_cap"):
        text = key.replace("saturated_fir_cap", "Clipped FIR C=")
    else:
        text = key.replace("context_r", "Context r=").replace("tanh_k", "Tanh k=")
        text = text.replace("_fir_k", " + FIR k=").replace("fir_k", "FIR k=")
        text = text.replace("leaky_k", "Leaky k=").replace("_r", ", r=")
    return text.replace("_", r"\_") if latex else text


def number(value):
    return "--" if value is None else f"{value:.5g}"


table = [r"\begin{tabular}{lrrrrc}\toprule",
         r"Method & Actual $K$ & Cap $C$ & Radius proxy & RMSE & Late loss drop\\\midrule"]
for row in rows:
    met = row["metrics"]
    late = row["extra"].get("underfit_flag")
    late_text = "yes" if late else "no" if late is not None else "--"
    table.append(" & ".join([label(row, True), number(met["certificate"]["K"]),
                              number(met["certificate"]["C"]),
                              number(met["primary_radius"]), number(met["rmse"]), late_text]) + r" \\")
table.append(r"\bottomrule\end{tabular}")
(M / "generated/gain_pilot.tex").write_text("\n".join(table) + "\n")

plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "pdf.fonttype": 42})
fig, axs = plt.subplots(1, 2, figsize=(10.4, 3.4), constrained_layout=True)
groups = [("constrained", "Constrained tanh", "#b54834", "^"),
          ("controls", "Reference / context / linear", "#256786", "o"),
          ("unconstrained", "Unconstrained tanh", "#555555", "s")]
for family, name, color, marker in groups:
    sub = [r for r in rows if r["metrics"]["primary_radius"] is not None
           and ((r["family"] == family) if family != "controls"
                else r["family"] not in ["constrained", "unconstrained"])]
    axs[0].scatter([r["metrics"]["rmse"] for r in sub],
                   [r["metrics"]["primary_radius"] for r in sub],
                   label=name, c=color, marker=marker, s=32, alpha=.8)
for name, short, color in [(selected["candidate"], "Selected candidate", "#b54834"),
                            (selected["simple_comparator"], "Selected control", "#256786")]:
    r = lookup[name]
    axs[0].scatter(r["metrics"]["rmse"], r["metrics"]["primary_radius"],
                   marker="*", s=130, c=color, edgecolors="black", linewidths=.5,
                   label=short, zorder=4)
axs[0].set_xlabel("Normal development RMSE (normalized)")
axs[0].set_ylabel("Empirical sufficient-radius proxy")
axs[0].grid(alpha=.15)
axs[0].legend(fontsize=9.5, frameon=False, loc="upper right")

histories = []
for row in rows:
    path = R / ("history_" + row["id"] + ".json")
    if not path.exists():
        continue
    history = json.loads(path.read_text())
    assert len(history) == 40
    family = row["family"]
    color = "#b54834" if family == "constrained" else "#256786" if family == "context" else "#555555"
    dash = "-" if row["id"] in [selected["candidate"], selected["simple_comparator"]] else "--"
    axs[1].plot([h["epoch"] for h in history], [h["training_window_mse"] for h in history],
                color=color, ls=dash, alpha=.8, linewidth=1,
                label=family)
    histories.append({"id": row["id"], "history": history})
assert len(histories) == 9
axs[1].set_xlabel("Fixed training epoch")
axs[1].set_ylabel("Training window MSE")
axs[1].set_yscale("log")
axs[1].grid(alpha=.15)
from matplotlib.lines import Line2D
axs[1].legend(handles=[
    Line2D([0],[0],color="#b54834",ls="--",label="Constrained tanh (6)"),
    Line2D([0],[0],color="#256786",ls="--",label="Command-only tanh (2)"),
    Line2D([0],[0],color="#555555",ls="--",label="Unconstrained tanh (1)"),
    Line2D([0],[0],color="#b54834",ls="-",label="Selected candidate")
], fontsize=9.5, frameon=False, loc="lower left")
fig.savefig(M / "figures/gain_feasibility.pdf")
plt.close(fig)

values = {"classification": "exposed normal development; no attack or population guarantee",
          "all_methods": rows, "final_admission": decision, "histories": histories,
          "not_plotted_no_finite_radius": [r["id"] for r in rows if r["metrics"]["primary_radius"] is None]}
(M / "PILOT_FIGURE_VALUES.json").write_text(json.dumps(values, indent=2) + "\n")
paths = [R / "methods.json", R / "FINAL_ADMISSION.json", R / "result.json", R / "supervisor.json",
         S / "config.json", S / "FREEZE.json", S / "PROTOCOL.md", S / "REVIEW_RELEASE.json",
         M / "generated/gain_pilot.tex", M / "figures/gain_feasibility.pdf",
         M / "PILOT_FIGURE_VALUES.json", Path(__file__).resolve()]
paths += sorted(R.glob("history_*.json"))
receipt = {"utc": datetime.now(timezone.utc).isoformat(),
           "command": ".venv-plots-v03/bin/python manuscript_arx_rbf_v1.8/integrate_pilot.py",
           "cwd": str(P), "training": False, "new_observations": False,
           "sha256": {str(p.relative_to(P)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
(M / "PILOT_ASSETS.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({"methods": len(rows), "pilot_passed": decision["passed"],
                  "selected": selected["candidate"], "control": selected["simple_comparator"]}))
