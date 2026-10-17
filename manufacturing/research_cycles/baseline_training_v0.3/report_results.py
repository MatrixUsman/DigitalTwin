"""Generate aggregate report and scientific plots from sealed run artifacts."""
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RUN = PROJECT / "local/baseline_training_v0.3/runs/training_001"
VERIFY = PROJECT / "local/baseline_training_v0.3/verification/verify_001"
OUTPUT = PROJECT / "output/baseline_training_v0.3"
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT / "local/baseline_training_v0.3/matplotlib"))
os.environ["XDG_CACHE_HOME"] = str(PROJECT / "local/baseline_training_v0.3/font_cache")
Path(os.environ["XDG_CACHE_HOME"]).mkdir(parents=True, exist_ok=True)


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    summary = json.loads((RUN / "summary.json").read_text())
    supervisor = json.loads((RUN / "supervisor.json").read_text())
    verification = json.loads((VERIFY / "verification.json").read_text())
    if verification["status"] != "passed": raise ValueError("Unverified run")
    for name, expected in verification["run_artifact_sha256"].items():
        if digest(RUN / name) != expected: raise ValueError("Run changed after verification: " + name)
    with (RUN / "learning_curves.csv").open() as stream: rows = list(csv.DictReader(stream))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "svg.fonttype": "none"})
    colors = {17: "#19638D", 42: "#B94E14", 2026: "#35754D"}
    figure, axes = plt.subplots(1, 2, figsize=(12.5, 5.3), layout="constrained")
    for seed, color in colors.items():
        selected = [r for r in rows if int(r["seed"]) == seed]
        epoch = [int(r["epoch"]) for r in selected]
        axes[0].plot(epoch, [float(r["training_mse"]) for r in selected], color=color, linestyle="--", linewidth=1.5, alpha=.8)
        axes[0].plot(epoch, [float(r["development_mse"]) for r in selected], color=color, linewidth=2, label=f"Seed {seed}")
    axes[0].set(xlabel="Completed epoch", ylabel="Standardized MSE", title="CNN learning curves", yscale="log", xlim=(0, 30))
    axes[0].grid(axis="y", alpha=.2, which="both")
    axes[0].legend(title="Solid: development · dashed: training", fontsize=9, title_fontsize=8.5)
    records = sorted(summary["models"], key=lambda r: r["standardized_mse"])
    labels = {"mean": "Training mean", "persistence": "Persistence", "ar4": "AR(4)",
              "cnn_seed17": "CNN · seed 17", "cnn_seed42": "CNN · seed 42", "cnn_seed2026": "CNN · seed 2026"}
    losses = [r["standardized_mse"] for r in records]
    bars = [colors[r["seed"]] if r["seed"] is not None else "#707780" for r in records]
    axes[1].scatter(losses, np.arange(len(records)), c=bars, s=65, zorder=3)
    axes[1].set_yticks(np.arange(len(records)), [labels[r["model"]] for r in records])
    axes[1].set_ylim(-.5, len(records) - .5)
    axes[1].invert_yaxis()
    axes[1].set(xlabel="Standardized development MSE (lower is better)", title="Same 16,384 normal targets", xscale="log", xlim=(.05, 1.7))
    axes[1].grid(axis="x", alpha=.2, which="both")
    for i, loss in enumerate(losses): axes[1].text(loss * 1.07, i, f"{loss:.4f}", va="center", fontsize=9)
    figure.suptitle("Manufacturing baseline training · public nominal IMU recording\n65,536 training targets · chronological split · all declared seeds", fontsize=12)
    for suffix in ["png", "svg"]: figure.savefig(OUTPUT / ("learning_curves." + suffix), dpi=180)
    plt.close(figure)
    cnn = [r for r in summary["models"] if r["seed"] is not None]
    values = np.array([r["standardized_mse"] for r in cnn])
    persistence = next(r for r in records if r["model"] == "persistence")["standardized_mse"]
    aggregate = {"cnn_mean_standardized_mse": float(values.mean()), "cnn_sample_std_standardized_mse": float(values.std(ddof=1)),
                 "relative_mse_reduction_from_persistence": float(1 - values.mean() / persistence),
                 "interpretation": "Optimization variation on one normal-development block, not independent robot replications"}
    safe = {"study_id": summary["study_id"], "status": summary["status"], "training_targets": summary["training_targets"],
            "development_targets": summary["development_targets"], "models": summary["models"], "aggregate": aggregate,
            "supervisor": supervisor, "worker_usage": summary["usage"],
            "verification": {k: verification[k] for k in ["passed", "total", "status", "scope"]},
            "run_artifact_sha256": verification["run_artifact_sha256"], "source_freeze_sha256": digest(HERE / "FREEZE.json"),
            "verification_receipt_sha256": digest(VERIFY / "verification.json"), "attack_metrics": None,
            "thresholds": None, "final_access": False}
    (HERE / "RESULTS.json").write_text(json.dumps(safe, indent=2) + "\n")
    table = "\n".join(f"| {labels[r['model']]} | {r['standardized_mse']:.6f} | {r['native_mse']:.6f} | {r.get('selected_epoch', '—')} |" for r in summary["models"])
    costs = "\n".join(f"| {labels[r['model']]} | {r['fit_wall_seconds']:.6f} | {r['score_wall_seconds']:.6f} |" for r in summary["models"])
    report = f'''# Trained compact CNN baseline and normal-development controls

## Material Passport

- Project: manufacturing; owner Haiqa Mushtaq; operator Codex under the user's implementation/run instruction.
- Study: `manufacturing-baseline-training-v0.3`, 17 October 2026.
- Status: **completed** — three fitted CNN artifacts, three ordinary controls, complete learning curves and verified saved predictions.
- Scope: independently implemented Edge-2025 compact architectural family under the [frozen normal-only protocol](PLAN.md); all measured values derive from [RESULTS.json](RESULTS.json).
- Verification: fresh-process inference and saved-artifact arithmetic passed **{verification['passed']}/{verification['total']}** checks. This is a software/result readback, not independent scientific peer review.

## What was executed

One accepted supervised attempt fitted all three seeds, **17, 42 and 2026**, on **{summary['training_targets']:,}** eligible normal targets and scored **{summary['development_targets']:,}** subsequent development targets. No windows were excluded: both populations had 100% coverage under the declared timestamp-boundary rule. Training rows `[219,65800)` and development rows `[65800,82229)` were split before 45-step windows. Only the permitted nominal prefix was parsed; the full nominal file was hashed for identity.

The existing isolated Python 3.12.15 / TensorFlow 2.16.2 environment was reused unchanged. Each CNN has 1,369 parameters; batch 1024, Adamax 0.001, no shuffle, maximum 30 epochs, patience five, minimum improvement `1e-6`. Every seed selected epoch 30 by the frozen rule. All seed results are retained. The artifacts contain inference weights and explicit architecture/scaler metadata; they intentionally omit optimizer state.

## Measured outcomes

All values below describe **normal one-step prediction**, with lower MSE indicating more accurate forecasts on this block. Standardized-channel MSE is the predeclared checkpoint-selection quantity. Native-channel MSE applies the recorded per-channel scales back to the residuals; its channels have different physical units and it is a secondary score-semantic diagnostic.

| Method | Standardized MSE | Inverse-scaled native MSE | Selected epoch |
|---|---:|---:|---:|
{table}

Across CNN seeds, standardized MSE is **{values.mean():.6f} ± {values.std(ddof=1):.6f}** (arithmetic mean ± sample standard deviation). This is **{100 * aggregate['relative_mse_reduction_from_persistence']:.2f}% lower** than persistence on the same targets. AR(4) is the strongest predictor under both reported losses. It remains a required control in the next study. The three seeds describe computational variation on this recording, not three independent robot experiments.

![Saved learning curves and all-method comparison](../../output/baseline_training_v0.3/learning_curves.png)

[Editable vector figure](../../output/baseline_training_v0.3/learning_curves.svg). Figures are generated directly from saved epoch logs and model records; no observations are synthesized or removed for presentation.

All CNN curves continued improving at the declared epoch cap. These are valid selected artifacts from the bounded study; a convergence plateau has not been demonstrated. The standardized ranking and inverse-scaled ranking differ: every CNN beats persistence on standardized MSE, while persistence has lower native MSE. This makes the scoring convention an explicit experimental choice. It does not by itself demonstrate an attack-detection weakness or determine future alarm performance.

## Resources and failures

The full attempt took **{supervisor['wall_seconds']:.3f} s supervised wall time**, **{summary['usage']['process_cpu_seconds']:.3f} s worker CPU**, **{supervisor['sampled_peak_rss_bytes'] / 1048576:.2f} MiB sampled peak RSS**, and **{supervisor['output_bytes']:,} bytes** of outputs before the final supervisor receipt. All four caps passed: 600 s wall, 300 s CPU, 1 GiB monitored RSS, 50 MiB outputs. Runtime platform: Apple M5 Pro, 18 logical CPUs, 24 GiB RAM, macOS arm64; workers use single-thread settings. RSS monitoring is sampled, not an instantaneous memory ceiling.

| Method | Fit/development-selection wall seconds | Prediction-only wall seconds for all development targets |
|---|---:|---:|
{costs}

CNN fit cost includes initialization evaluation and repeated post-epoch training/development evaluation. Control fit cost excludes the shared scaler/loading step. Prediction timings exclude score calculation and file I/O. They are single laptop measurements, not end-to-end alarm latency or edge-device timing.

**Training failures/retries: zero. Synthetic test failures: zero.** The 25-test suite and all three seed fits completed on their first named attempts. Dependency deprecation/cache warnings were preserved in setup/test logs. Earlier v0.2 failures remain unchanged and are not erased from project history.

## Verification and usable artifacts

The fresh-process verifier loaded each selected checkpoint and reproduced all 16,384 saved predictions exactly. Separate NumPy calculations checked endpoint alignment, point/channel/aggregate error, every epoch-selection decision, stopping conditions, controls and resource limits. It also checked all 52 old source/configuration identities, 133 frozen input bindings, three old freeze/completion records, the old PDF and all previously bound v0.2 artifacts.

- [Pre-execution source/config/test freeze](FREEZE.json): 13 source/configuration identities after 25 passing synthetic tests.
- [Actual training artifacts](../../local/baseline_training_v0.3/runs/training_001/): all CNN weights, scaler/development arrays, AR coefficients, score/prediction arrays, epoch CSV, provenance and supervisor receipt.
- [Fresh-process verification](../../local/baseline_training_v0.3/verification/verify_001/verification.json).
- [Complete safe result summary](RESULTS.json) and [executable usage](README.md).

Raw data, fitted artifacts and environments remain local and ignored by Git. The new plotting environment is separate; the training environment and previous experiment bytes remain unchanged. No attack metric, threshold calibration or final-test exposure occurred.

## Next experimental use

Use these saved predictors and AR/persistence controls as the reference for a separately specified **exploratory limitation experiment** on brief versus persistent motion deviations. Any additional training budget must be declared before that experiment; its outcomes must not choose checkpoints. The trained pipeline, reproducible artifacts and normal-development measurements are now available. The broader novelty question is addressed by the next mechanism experiment, rather than by treating notebook corrections as a new algorithm.
'''
    (HERE / "RESULTS.md").write_text(report)
    receipt = {"utc": datetime.now(timezone.utc).isoformat(), "command": sys.argv, "matplotlib": matplotlib.__version__,
               "source_sha256": digest(Path(__file__)), "input_sha256": {str(p.relative_to(PROJECT)): digest(p) for p in [RUN / "summary.json", RUN / "learning_curves.csv", VERIFY / "verification.json"]},
               "output_sha256": {str(p.relative_to(PROJECT)): digest(p) for p in [HERE / "RESULTS.md", HERE / "RESULTS.json", OUTPUT / "learning_curves.png", OUTPUT / "learning_curves.svg"]}}
    (PROJECT / "local/baseline_training_v0.3/report_generation.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"cnn_mean_mse": float(values.mean()), "verification_checks": verification["total"], "report": str(HERE / "RESULTS.md"), "figure": str(OUTPUT / "learning_curves.png")}, indent=2))
