"""Bounded normal-only motion-observer validation; no label or final access.

The existing selected template and AR control are immutable inputs. The emission bandwidth and two
score-component means are estimated from training endpoints. Diagnostic future
outcomes evaluate forecasts issued earlier; they never enter observer state.
"""
from __future__ import annotations

from array import array
from bisect import bisect_left
from collections import Counter, deque
from dataclasses import asdict
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
import sys
import time
from types import SimpleNamespace

from .contract import ContractError, LoadStats, Study, iter_development_records
from .control_study import TrainingCache, state_digest
from .controls import ARDetector, ARReference, TemplateReference

OBSERVER_PLAN_PATH = "configs/casper_right_arm_observer_v0.1.json"
MODES = ("synchronized", "unconstrained", "free_running")
SCORES = ("synchronized_residual", "synchronized_evidence", "unconstrained_residual", "free_running_residual")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def bound_path(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ContractError("Missing or external observer dependency")
    return path


def load_observer_plan(root: Path) -> dict:
    plan = json.loads((root / OBSERVER_PLAN_PATH).read_text())
    if plan.get("study_id") != "manufacturing-casper-right-arm-observer-v0.1":
        raise ContractError("Unsupported observer study version")
    if any(plan["access"].get(key) is not False for key in (
            "calibration_access", "protected_final_access", "labels_available_to_model")):
        raise ContractError("Observer validation cannot admit calibration, finals or labels")
    document = bound_path(root, plan["documentation"])
    if sha(document) != plan["documentation_sha256"]:
        raise ContractError("Observer-study documentation changed before admission")
    for key in ("data_contract", "evaluation_policy", "selected_controls"):
        reference = plan[key]
        if sha(bound_path(root, reference["path"])) != reference["sha256"]:
            raise ContractError("Observer-study frozen dependency mismatch")
    return plan


def load_references(root, plan):
    """Read selected fitted artifacts only; do not fit or inspect saved scores."""
    record = plan["selected_controls"]
    registry_path = bound_path(root, record["path"])
    if sha(registry_path) != record["sha256"]:
        raise ContractError("Selected-control registry changed")
    registry = json.loads(registry_path.read_text())
    if (registry["selection_partition"] != "development"
            or registry["refit_on_development"] is not False
            or registry["training_eligible_count"] != plan["access"]["fit"]["expected_eligible_rows"]
            or registry["development_eligible_count"] != plan["access"]["check_scores"]["expected_eligible_rows"]
            or registry["thresholds"] is not None or registry["final_test_admitted"] is not False):
        raise ContractError("Selected-control provenance incompatible with study")
    if sha(bound_path(root, registry["source_run"] + "/run.json")) != registry["run_manifest_sha256"]:
        raise ContractError("Selected-control run identity changed")
    references, provenance = {}, {}
    for family, cls in (("template", TemplateReference), ("ar", ARReference)):
        entry = registry["selected"][family]
        path = bound_path(root, entry["model_path"])
        if sha(path) != entry["model_file_sha256"]:
            raise ContractError("Selected-control file identity changed")
        saved = json.loads(path.read_text())
        reference = cls.from_dict(saved["reference"])
        if (saved["family"] != family or saved["candidate"] != entry["candidate_id"]
                or state_digest(reference) != entry["model_state_sha256"]
                or state_digest(reference) != saved["state_sha256"]
                or reference.n != registry["training_eligible_count"]):
            raise ContractError("Selected-control state identity changed")
        references[family] = reference
        provenance[family] = {key: entry[key] for key in (
            "candidate_id", "model_path", "model_file_sha256", "model_state_sha256")}
    if state_digest(references["template"].scaler) != state_digest(references["ar"].scaler):
        raise ContractError("Selected controls disagree on training-only transformation")
    return references["template"], references["ar"], provenance


def mse(a, b):
    value = math.fsum((x-y)**2 for x, y in zip(a, b))/len(a)
    if not math.isfinite(value) or value < 0:
        raise ContractError("Nonfinite diagnostic residual")
    return value


class Moments:
    def __init__(self):
        self.n = 0
        self.mean = self.m2 = 0.0
        self.minimum = self.maximum = None

    def add(self, value):
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ContractError("Nonfinite diagnostic value")
        self.n += 1
        delta = value-self.mean
        self.mean += delta/self.n
        self.m2 += delta*(value-self.mean)
        self.minimum = value if self.minimum is None else min(self.minimum, value)
        self.maximum = value if self.maximum is None else max(self.maximum, value)

    def to_dict(self):
        return {"n": self.n, "mean": self.mean if self.n else None,
                "variance": self.m2/self.n if self.n else None,
                "minimum": self.minimum, "maximum": self.maximum}


class Recurrence:
    """Diagnostic sampled pairs, with a declared nearest-past timestamp tolerance."""
    def __init__(self, period, factors, tolerance):
        self.period, self.factors, self.tolerance = period, tuple(factors), tolerance
        if period <= 0 or tolerance <= 0 or any(x <= 0 for x in factors):
            raise ContractError("Invalid recurrence diagnostic configuration")
        self.history = deque()
        self.attempted = self.matched = 0
        self.unmatched = Counter()
        self.loss = {str(f): Moments() for f in factors}
        self.lag = {str(f): Moments() for f in factors}
        self.error = {str(f): Moments() for f in factors}

    def reset(self):
        self.history.clear()

    def observe(self, elapsed, values, eligible, diagnostic):
        cutoff = elapsed-self.period*max(self.factors)-2*self.tolerance
        while self.history and self.history[0][0] < cutoff:
            self.history.popleft()
        if diagnostic and eligible:
            self.attempted += 1
            if not self.history:
                self.unmatched["no_prior_native_observations"] += 1
        if diagnostic and eligible and self.history:
            history = list(self.history)
            times = [item[0] for item in history]
            matched = []
            for factor in self.factors:
                target = elapsed-self.period*factor
                index = bisect_left(times, target)
                choices = history[max(0,index-1):min(len(history),index+1)]
                previous = min(choices, key=lambda item: (abs(item[0]-target), item[0]))
                if not previous[2] or abs(previous[0]-target) > self.tolerance:
                    self.unmatched["ineligible_past_endpoint" if not previous[2] else "no_native_match_within_tolerance"] += 1
                    matched = []
                    break
                matched.append((factor, previous))
            if matched:
                self.matched += 1
            # Every lag uses exactly the same diagnostic origin population.
            for factor, previous in matched:
                self.loss[str(factor)].add(mse(values, previous[1]))
                self.lag[str(factor)].add(elapsed-previous[0])
                self.error[str(factor)].add(elapsed-previous[0]-self.period*factor)
        self.history.append((elapsed, values, eligible))

    def to_dict(self):
        return {key: {"standardized_MSE": value.to_dict(), "actual_lag_seconds": self.lag[key].to_dict(), "matching_error_seconds": self.error[key].to_dict()}
                for key, value in self.loss.items()}


class ProspectiveForecasts:
    """Forecasts are fixed at origin; consume only first future timestamp >= due.

    Missing endpoints at a gap or partition end are explicitly right-censored.
    This diagnostic support does not alter the complete anomaly-score support.
    """
    def __init__(self, horizons, tolerance):
        self.horizons, self.tolerance = tuple(horizons), tolerance
        if not horizons or tolerance <= 0 or any(h <= 0 for h in horizons):
            raise ContractError("Invalid forecast diagnostic configuration")
        self.queues = {str(h): deque() for h in horizons}
        self.stats = {str(h): {name: Moments() for name in (*MODES, "persistence", "training_mean", "actual_horizon_seconds", "matching_error_seconds")}
                      for h in horizons}
        self.issued = Counter()
        self.censored = Counter()

    def issue(self, elapsed, values, observers):
        for horizon in self.horizons:
            predictions = {mode: tuple(observer.forecast(horizon).prediction) for mode, observer in observers.items()}
            self.queues[str(horizon)].append((elapsed, elapsed+horizon, values, predictions))
            self.issued[str(horizon)] += 1

    def observe(self, elapsed, values, eligible):
        for key, queue in self.queues.items():
            while queue and elapsed >= queue[0][1]:
                origin, due, persistent, predictions = queue.popleft()
                if not eligible or elapsed-due > self.tolerance:
                    self.censored[key] += 1
                    continue
                self.stats[key]["actual_horizon_seconds"].add(elapsed-origin)
                self.stats[key]["matching_error_seconds"].add(elapsed-due)
                self.stats[key]["training_mean"].add(mse(values, (0.,)*12))
                self.stats[key]["persistence"].add(mse(values, persistent))
                for mode, prediction in predictions.items():
                    self.stats[key][mode].add(mse(values, prediction))

    def reset(self):
        for key, queue in self.queues.items():
            self.censored[key] += len(queue)
            queue.clear()

    def to_dict(self):
        return {key: {"issued": self.issued[key], "censored": self.censored[key],
                      **{name: value.to_dict() for name, value in values.items()}}
                for key, values in self.stats.items()}


class ChannelErrors:
    def __init__(self, channels=12):
        self.n = 0
        self.sums = [0.] * channels

    def add(self, actual, predicted):
        self.n += 1
        for j, (a, b) in enumerate(zip(actual, predicted)):
            value = (a-b)**2
            if not math.isfinite(value):
                raise ContractError("Nonfinite per-channel diagnostic")
            self.sums[j] += value

    def to_dict(self):
        return {"n": self.n, "mean_squared_errors": [x/self.n for x in self.sums] if self.n else None}


def template_kinematics(reference):
    """Circular central position differences versus separately fitted velocity."""
    physical = [tuple(mean + sigma*x for mean,sigma,x in zip(reference.scaler.mean,reference.scaler.sigma,row)) for row in reference.means]
    squared, baseline = [0.]*6, [0.]*6
    dt = reference.period_seconds/reference.bins
    for k, row in enumerate(physical):
        for j in range(6):
            derivative = (physical[(k+1)%reference.bins][j]-physical[(k-1)%reference.bins][j])/(2*dt)
            squared[j] += (derivative-row[6+j])**2/reference.bins
            baseline[j] += (reference.scaler.mean[6+j]-row[6+j])**2/reference.bins
    residual = math.fsum(x/reference.scaler.variance[6+j] for j,x in enumerate(squared))/6
    null = math.fsum(x/reference.scaler.variance[6+j] for j,x in enumerate(baseline))/6
    return {"convention": "circular central difference of physical bin mean positions over 2*T/B; target physical bin mean velocity",
            "per_joint_MSE": squared, "training_mean_velocity_MSE": baseline,
            "per_joint_ratio": [a/b if b > 0 else None for a,b in zip(squared,baseline)],
            "standardized_MSE": residual, "standardized_training_mean_MSE": null,
            "aggregate_better_than_training_mean": residual < null}


class Progression:
    """Descriptive shortest circular MAP displacement; no measured phase truth."""
    def __init__(self, bins, period):
        self.bins, self.period = bins, period
        self.previous = None
        self.displacement, self.dt, self.deviation = Moments(), Moments(), Moments()
        self.unchanged = self.backward = self.large_jump = 0

    def reset(self):
        self.previous = None

    def observe(self, elapsed, phase_bin):
        if self.previous is not None:
            previous_time, previous_bin = self.previous
            dt = elapsed-previous_time
            if dt <= 0:
                raise ContractError("Nonpositive progression diagnostic elapsed time")
            movement = (phase_bin-previous_bin+self.bins/2)%self.bins-self.bins/2
            self.displacement.add(movement)
            self.dt.add(dt)
            self.deviation.add(movement-self.bins*dt/self.period)
            self.unchanged += movement == 0
            self.backward += movement < 0
            self.large_jump += abs(movement) > self.bins/4
        self.previous = elapsed,phase_bin

    def to_dict(self):
        n = self.displacement.n
        return {"shortest_signed_MAP_bin_displacement":self.displacement.to_dict(),
                "elapsed_seconds":self.dt.to_dict(),"displacement_minus_nominal_bins":self.deviation.to_dict(),
                "unchanged_fraction":self.unchanged/n if n else None,
                "backward_fraction":self.backward/n if n else None,
                "greater_than_quarter_cycle_fraction":self.large_jump/n if n else None,
                "phase_ground_truth":False,"half_cycle_tie":"negative"}


def records(study, plan, name, stats, summary, progress):
    scope = plan["access"][name]
    partition = scope["parent_partition"]
    if partition not in {"training", "development"}:
        raise ContractError("Only training and development are admitted")
    spec = study.partition(partition)
    start, stop = scope["rows_half_open"]
    if (start, stop) != (spec.start, spec.end):
        raise ContractError("Full normal partition required")
    expected = iter(row for a, b in scope["eligible_intervals_half_open"] for row in range(a, b))
    next_eligible = next(expected, None)
    summary.update(raw_rows_yielded=0, eligible_rows=0, exclusions={}, segment_start_rows=[], source_checks_completed=False)
    exclusions = Counter()
    stream = iter_development_records(study, partition, stats=stats)
    try:
        for record in stream:
            if record.row != start+summary["raw_rows_yielded"]:
                raise ContractError("Missing, duplicated or reordered observer row")
            summary["raw_rows_yielded"] += 1
            if record.eligible != (record.row == next_eligible):
                raise ContractError("Observer endpoint mask mismatch")
            if record.eligible:
                summary["eligible_rows"] += 1
                next_eligible = next(expected, None)
            else:
                exclusions[record.exclusion] += 1
                summary["exclusions"] = dict(exclusions)
            if record.observation is None:
                raise ContractError("Invalid observer observation")
            if record.observation.dt is None:
                summary["segment_start_rows"].append(record.row)
            if summary["raw_rows_yielded"] % 10000 == 0:
                progress()
            yield record
        if (summary["raw_rows_yielded"] != scope["raw_rows"]
                or summary["eligible_rows"] != scope["expected_eligible_rows"]
                or next_eligible is not None or not stats.stream_checks_completed):
            raise ContractError("Incomplete observer source/support checks")
        summary["source_checks_completed"] = True
    finally:
        stream.close()
        summary["load_stats"] = asdict(stats)


def run_observer_study(study: Study, plan: dict, writer, diagnostics: dict):
    from .observer import ObserverConfig, PhaseObserver, PreparedObservation, prepare_observation, phase_diagnostics
    started = time.perf_counter()
    stats = {key: LoadStats() for key in ("fit", "check_scores")}
    populations = {key: {} for key in stats}
    diagnostics.update(status="running", stage="reference_admission", populations=populations)
    reference, ar_reference, provenance = load_references(study.project_root, plan)
    if tuple(plan["model"].get("variants",MODES)) != MODES:
        raise ContractError("Observer variants differ from declared modes")
    original_hash = state_digest(reference)
    ar_hash = state_digest(ar_reference)
    diagnostic_config = plan["diagnostics"]
    stride = diagnostic_config["stride"]
    if type(stride) is not int or stride < 1:
        raise ContractError("Invalid diagnostic stride")
    normalizers = {"residual": Moments(), "correction_js": Moments()}
    score_arrays = {name: array("d") for name in SCORES}
    partition_results = {}
    kinematic_reference = template_kinematics(reference)

    def progress():
        writer.append_text("progress.jsonl", json.dumps({
            "stage": diagnostics["stage"], "elapsed_seconds": time.perf_counter()-started,
            "selected_input_rows_parsed": {key: value.selected_rows_parsed for key, value in stats.items()},
            "replay_rows_completed": diagnostics.get("replay_rows_completed"),
            "coverage_is_last_known_not_terminal": True}, allow_nan=False)+"\n")

    try:
        writer.write_json("input_references.json", {"template": reference.to_dict(), "ar": ar_reference.to_dict(),
                          "provenance": provenance, "template_state_sha256": original_hash, "ar_state_sha256": ar_hash})
        writer.write_text("development_index.jsonl", "")
        # One admitted training parse; cache features/emissions locally in memory.
        # The likelihood scale is fitted before any observer replay, never on dev.
        diagnostics["stage"] = "training_emission_scale"
        cache, standardized_cache, distance_cache = TrainingCache(), array("d"), array("d")
        nearest = Moments()
        for record in records(study, plan, "fit", stats["fit"], populations["fit"], progress):
            prepared = prepare_observation(reference, record.observation)
            cache.append(record.observation, record.eligible)
            standardized_cache.extend(prepared.standardized)
            distance_cache.extend(prepared.distances)
            if record.eligible:
                nearest.add(min(prepared.distances))
        config = ObserverConfig(max(nearest.mean, plan["model"]["temperature_floor"]),
                                plan["model"]["mixing_rate"], plan["model"]["initialization"])
        diagnostics["fitted_emission_scale"] = {"nearest_template_MSE": nearest.to_dict(), "temperature": config.temperature}

        def prepared_records(partition):
            if partition == "fit":
                for index, (observation, eligible) in enumerate(cache.records()):
                    prepared = PreparedObservation(reference, observation,
                        tuple(standardized_cache[index*12:(index+1)*12]),
                        tuple(distance_cache[index*reference.bins:(index+1)*reference.bins]))
                    yield SimpleNamespace(observation=observation, eligible=eligible), prepared
            else:
                for record in records(study, plan, partition, stats[partition], populations[partition], progress):
                    yield record, prepare_observation(reference, record.observation)

        for partition in ("fit", "check_scores"):
            diagnostics["stage"] = "training_normalizers_and_validation" if partition == "fit" else "development_validation"
            progress()
            observers = {mode: PhaseObserver(reference, config, mode=mode) for mode in MODES}
            ar = ARDetector(ar_reference)
            recurrence = Recurrence(reference.period_seconds, diagnostic_config["recurrence_factors"], diagnostic_config["recurrence_tolerance_seconds"])
            forecasts = ProspectiveForecasts(diagnostic_config["horizons_seconds"], diagnostic_config["forecast_tolerance_seconds"])
            one_step = {key: Moments() for key in (*MODES, "ar", "persistence", "training_mean")}
            per_channel = {key: ChannelErrors() for key in (*MODES,"ar","persistence","training_mean")}
            kinematic_observed, kinematic_observed_baseline = ChannelErrors(6), ChannelErrors(6)
            uncertainty = {mode: {"variance_sums": [0.]*12, "n": 0, "map_bin_counts": [0]*reference.bins} for mode in MODES}
            components = {mode: {name: Moments() for name in ("residual", "correction_js", "posterior_entropy", "posterior_resultant", "maximum_bin_mass", "ambiguous_fraction", "separated_competitor_mass")}
                          for mode in MODES}
            progression = {mode:Progression(reference.bins,reference.period_seconds) for mode in MODES}
            elapsed, eligible_count, previous, previous_physical = 0., 0, None, None
            replay_count = 0
            index_buffer = []
            for record, prepared in prepared_records(partition):
                replay_count += 1
                if replay_count % 10000 == 0:
                    diagnostics["replay_rows_completed"] = {"partition":partition,"rows":replay_count-1}
                    progress()
                observation = record.observation
                if observation.dt is None:
                    observers = {mode: PhaseObserver(reference, config, mode=mode) for mode in MODES}
                    ar.reset(); recurrence.reset(); forecasts.reset()
                    for item in progression.values(): item.reset()
                    elapsed, previous, previous_physical = 0., None, None
                else:
                    elapsed += float(observation.dt)
                values = prepared.standardized
                forecasts.observe(elapsed, values, record.eligible)
                steps = {mode: observer.propose(prepared) for mode, observer in observers.items()}
                if record.eligible:
                    eligible_count += 1
                    if not all(step.ready for step in steps.values()) or previous is None:
                        raise ContractError("Uninitialized observer on common eligible support")
                    ar_prediction = ar.predict(observation)
                    if ar_prediction is None:
                        raise ContractError("Uninitialized AR on common eligible support")
                    one_step["ar"].add(mse(values, ar_prediction))
                    per_channel["ar"].add(values,ar_prediction)
                    per_channel["persistence"].add(values,previous)
                    per_channel["training_mean"].add(values,(0.,)*12)
                    if previous_physical is None or observation.dt is None:
                        raise ContractError("Missing native history for causal kinematic diagnostic")
                    derivative = tuple((q-p)/float(observation.dt) for q,p in zip(observation.q,previous_physical))
                    kinematic_observed.add(observation.qdot,derivative)
                    kinematic_observed_baseline.add(observation.qdot,reference.scaler.mean[6:])
                    one_step["persistence"].add(mse(values, previous))
                    one_step["training_mean"].add(mse(values, (0.,)*12))
                    for mode, step in steps.items():
                        one_step[mode].add(step.residual)
                        per_channel[mode].add(values,step.prediction)
                        components[mode]["residual"].add(step.residual)
                        components[mode]["correction_js"].add(step.correction_js)
                        if (eligible_count-1) % stride == 0:
                            phase = phase_diagnostics(step.posterior)
                            components[mode]["posterior_entropy"].add(phase["entropy"])
                            components[mode]["posterior_resultant"].add(phase["resultant"])
                            components[mode]["maximum_bin_mass"].add(phase["maximum_mass"])
                            components[mode]["ambiguous_fraction"].add(int(phase["entropy"] > diagnostic_config.get("ambiguous_entropy_above",.5) or phase["resultant"] < diagnostic_config.get("ambiguous_resultant_below",.5)))
                            components[mode]["separated_competitor_mass"].add(phase["separated_competitor_mass"])
                            uncertainty[mode]["map_bin_counts"][phase["map_bin"]] += 1
                            progression[mode].observe(elapsed,phase["map_bin"])
                    if partition == "fit":
                        normalizers["residual"].add(steps["synchronized"].residual)
                        normalizers["correction_js"].add(steps["synchronized"].correction_js)
                    else:
                        residual = steps["synchronized"].residual/normalizers["residual"].mean
                        correction = steps["synchronized"].correction_js/normalizers["correction_js"].mean
                        score_arrays["synchronized_residual"].append(residual)
                        score_arrays["synchronized_evidence"].append(residual+correction)
                        for mode in MODES[1:]:
                            score_arrays[mode+"_residual"].append(steps[mode].residual/normalizers["residual"].mean)
                        index_buffer.append(json.dumps({"row": record.row, "timestamp": str(record.timestamp), "segment": record.segment}, separators=(",", ":"))+"\n")
                recurrence.observe(elapsed, values, record.eligible, record.eligible and (eligible_count-1) % stride == 0)
                for mode, observer in observers.items():
                    observer.commit(steps[mode])
                ar.update(observation)
                previous = values
                previous_physical = observation.q
                if record.eligible and (eligible_count-1) % stride == 0:
                    forecasts.issue(elapsed, values, observers)
                    for mode, observer in observers.items():
                        current = observer.forecast(0.)
                        uncertainty[mode]["n"] += 1
                        for j,value in enumerate(current.physical_phase_variance):
                            uncertainty[mode]["variance_sums"][j] += value
                if len(index_buffer) >= 1000:
                    writer.append_text("development_index.jsonl", "".join(index_buffer)); index_buffer.clear()
            if index_buffer:
                writer.append_text("development_index.jsonl", "".join(index_buffer))
            forecasts.reset()
            partition_results[partition] = {"eligible_count": eligible_count,
                "one_step_standardized_MSE": {name: value.to_dict() for name, value in one_step.items()},
                "inferred_progression": {mode:item.to_dict() for mode,item in progression.items()},
                "per_channel_standardized_MSE": {name:value.to_dict() for name,value in per_channel.items()},
                "causal_position_velocity_consistency": {"convention":"backward position difference divided by actual dt compared with current reported velocity", "error":kinematic_observed.to_dict(), "training_mean_velocity_error":kinematic_observed_baseline.to_dict(), "standardized_MSE":math.fsum(value/kinematic_observed.n/reference.scaler.variance[6+j] for j,value in enumerate(kinematic_observed.sums))/6, "standardized_training_mean_MSE":math.fsum(value/kinematic_observed_baseline.n/reference.scaler.variance[6+j] for j,value in enumerate(kinematic_observed_baseline.sums))/6},
                "mapped_phase_uncertainty": {mode:{"n":entry["n"], "mean_physical_variance":[x/entry["n"] for x in entry["variance_sums"]], "map_bin_counts":entry["map_bin_counts"]} for mode,entry in uncertainty.items()},
                "components": {mode: {name: value.to_dict() for name, value in items.items()} for mode, items in components.items()},
                "recurrence": recurrence.to_dict(), "recurrence_coverage":{"attempted":recurrence.attempted,"matched":recurrence.matched,"unmatched":dict(recurrence.unmatched)}, "prospective_forecasts": forecasts.to_dict()}
            if partition == "fit":
                if any(value.mean <= plan["model"]["normalizer_floor"] for value in normalizers.values()):
                    raise ContractError("Training score component degenerate; no hidden normalizer floor")
                fitted_before = {"config":config.to_dict(),"normalizers":{name:value.to_dict() for name,value in normalizers.items()},"emission_scale":nearest.to_dict()}
                writer.write_json("observer.model.json", {"kind": "independent_phase_observer_not_validated_physical_twin",
                    "template": reference.to_dict(), "observer_config": config.to_dict(),
                    "emission_scale_fit": nearest.to_dict(),
                    "normalizers": {name: value.to_dict() for name, value in normalizers.items()},
                    "training_eligible_count": eligible_count, "template_state_sha256": original_hash,
                    "paired_ablation_same_state": True, "development_refitting": False})
            progress()
            if partition == "fit":
                del cache, standardized_cache, distance_cache
        fitted_after = {"config":config.to_dict(),"normalizers":{name:value.to_dict() for name,value in normalizers.items()},"emission_scale":nearest.to_dict()}
        if fitted_before != fitted_after:
            raise ContractError("Fitted bandwidth or evidence normalizers changed during development")
        if original_hash != state_digest(reference) or ar_hash != state_digest(ar_reference):
            raise ContractError("Fitted reference changed during observer validation")
        score_manifest = {}
        for name, scores in score_arrays.items():
            if len(scores) != plan["access"]["check_scores"]["expected_eligible_rows"] or any(not math.isfinite(x) or x < 0 for x in scores):
                raise ContractError("Incomplete or nonfinite observer scores")
            payload = scores.tobytes()
            filename = name+".scores.f64"
            writer.write_bytes(filename, payload)
            score_manifest[name] = {"path": filename, "sha256": hashlib.sha256(payload).hexdigest(),
                                    "n": len(scores), "mean": math.fsum(scores)/len(scores),
                                    "min": min(scores), "max": max(scores)}
        validity = evaluate_validity(partition_results, plan, kinematic_reference)
        writer.write_json("observer_results.json", {"partitions": partition_results, "template_kinematics":kinematic_reference,
            "normalizers": {name: value.to_dict() for name, value in normalizers.items()},
            "scores": score_manifest, "score_format": {"bytes_per_score": array("d").itemsize, "byteorder": sys.byteorder},
            "validity": validity, "reference_unchanged": True, "all_fitted_parameters_unchanged": True, "paired_ablation_same_state": True,
            "calibrated": False, "final_test_admitted": False})
        diagnostics.update(status="completed", stage="completed", partitions=partition_results, validity=validity,
            score_counts={name: len(values) for name, values in score_arrays.items()}, reference_unchanged=True, all_fitted_parameters_unchanged=True,
            model_artifact="observer.model.json", model_file_sha256=sha(writer.output_dir/"observer.model.json"),
            calibrated_threshold=None, attack_metrics_computed=False, calibration_or_final_observations_parsed=False,
            paper_baseline_executed=False, physical_twin_validated=False)
        progress()
    except Exception as error:
        diagnostics.update(status="failed", failure_reason=f"{type(error).__name__}: {error}")
        raise
    finally:
        diagnostics["core_elapsed_seconds"] = time.perf_counter()-started
        diagnostics["load_stats"] = {key: asdict(value) for key, value in stats.items()}


def evaluate_validity(partitions, plan, kinematics):
    """Predeclared scientific gates can fail while technical execution succeeds."""
    criteria = []
    for partition in ("fit", "check_scores"):
        values = partitions[partition]
        recurrence = values["recurrence"]
        actual = recurrence["1.0"]["standardized_MSE"]["mean"]
        neighbor_values = [recurrence[key]["standardized_MSE"]["mean"] for key in ("0.5", "0.9", "1.1")]
        criteria.append({"id": partition+"_recurrence_local_minimum", "passed": actual is not None and all(x is not None and actual < x for x in neighbor_values),
                         "nominal_MSE": actual, "neighbor_MSE": neighbor_values})
    development = partitions["check_scores"]
    one = development["one_step_standardized_MSE"]
    criteria.append({"id": "development_prediction_better_than_training_mean", "passed": one["synchronized"]["mean"] < one["training_mean"]["mean"]})
    for horizon, values in development["prospective_forecasts"].items():
        criteria.append({"id": "development_forecast_"+horizon+"_beats_training_mean", "passed": values["synchronized"]["n"] > 0 and values["synchronized"]["mean"] < values["training_mean"]["mean"]})
    all_horizons = [(one["synchronized"]["mean"],one["free_running"]["mean"])] + [(value["synchronized"]["mean"],value["free_running"]["mean"]) for value in development["prospective_forecasts"].values() if value["synchronized"]["n"] > 0]
    criteria.append({"id":"synchronization_benefit_at_any_declared_horizon", "passed":any(a < b for a,b in all_horizons)})
    criteria.append({"id":"reference_kinematic_correspondence", "passed":kinematics["aggregate_better_than_training_mean"]})
    return {"criteria": criteria, "all_predeclared_checks_pass": all(item["passed"] for item in criteria),
            "designation": "empirical_motion_phase_observer", "physical_digital_twin_established": False,
            "limitations": ["No independently observed task phase", "Model-conditional phase uncertainty is not calibrated physical uncertainty", "No attack performance or causal plant dynamics validated"]}


def validate_observer_artifacts(run_dir: Path, plan: dict) -> dict:
    """Read saved models, exact coordinates and every score; never reopen raw data."""
    results = json.loads((run_dir/"observer_results.json").read_text())
    expected = iter(row for a,b in plan["access"]["check_scores"]["eligible_intervals_half_open"] for row in range(a,b))
    count, previous = 0, None
    with (run_dir/"development_index.jsonl").open() as handle:
        for line in handle:
            item = json.loads(line)
            timestamp = Decimal(item["timestamp"])
            if (set(item) != {"row", "timestamp", "segment"} or type(item["row"]) is not int
                    or item["row"] != next(expected, None) or not timestamp.is_finite()
                    or type(item["segment"]) is not int or (previous is not None and timestamp <= previous)):
                raise ContractError("Invalid saved observer coordinate")
            count += 1; previous = timestamp
    if count != plan["access"]["check_scores"]["expected_eligible_rows"] or next(expected, None) is not None:
        raise ContractError("Incomplete saved observer coordinates")
    if set(results["scores"]) != set(SCORES) or results["score_format"] != {"bytes_per_score": array("d").itemsize, "byteorder": sys.byteorder}:
        raise ContractError("Saved observer score inventory mismatch")
    arrays = {}
    for name, item in results["scores"].items():
        payload = (run_dir/item["path"]).read_bytes()
        scores = array("d"); scores.frombytes(payload)
        if (len(scores) != count or item["n"] != count or hashlib.sha256(payload).hexdigest() != item["sha256"]
                or any(not math.isfinite(x) or x < 0 for x in scores) or math.fsum(scores)/len(scores) != item["mean"]):
            raise ContractError("Saved observer score identity mismatch")
        arrays[name] = scores
    if any(b < a for a,b in zip(arrays["synchronized_residual"], arrays["synchronized_evidence"])):
        raise ContractError("Paired evidence score inconsistent")
    model = json.loads((run_dir/"observer.model.json").read_text())
    reference = TemplateReference.from_dict(model["template"])
    inputs=json.loads((run_dir/"input_references.json").read_text())
    if (model["template"] != inputs["template"] or state_digest(reference) != inputs["template_state_sha256"]
            or inputs["template_state_sha256"] != inputs["provenance"]["template"]["model_state_sha256"]):
        raise ContractError("Saved observer reference differs from pinned selected-control input")
    from .observer import ObserverConfig
    config = ObserverConfig.from_dict(model["observer_config"])
    if (state_digest(reference) != model["template_state_sha256"] or config.mixing_rate != plan["model"]["mixing_rate"] or config.initialization != plan["model"]["initialization"]
            or config.temperature != max(model["emission_scale_fit"]["mean"], plan["model"]["temperature_floor"])
            or model["emission_scale_fit"]["n"] != plan["access"]["fit"]["expected_eligible_rows"]
            or model["training_eligible_count"] != plan["access"]["fit"]["expected_eligible_rows"]
            or model["normalizers"] != results["normalizers"] or model["development_refitting"] is not False
            or model["paired_ablation_same_state"] is not True or results["paired_ablation_same_state"] is not True
            or results["reference_unchanged"] is not True or results["all_fitted_parameters_unchanged"] is not True or results["calibrated"] is not False
            or results["final_test_admitted"] is not False):
        raise ContractError("Saved observer state/configuration changed")
    if set(results["normalizers"]) != {"residual","correction_js"}:
        raise ContractError("Unexpected normalizer inventory")
    for item in results["normalizers"].values():
        if item["n"] != model["training_eligible_count"] or not math.isfinite(item["mean"]) or item["mean"] <= plan["model"]["normalizer_floor"]:
            raise ContractError("Invalid training normalizer")
    parts=results["partitions"]["check_scores"]["components"]
    scale=results["normalizers"]["residual"]["mean"]
    for name,item in results["scores"].items():
        mode="synchronized" if name.startswith("synchronized") else name.removesuffix("_residual")
        expected=parts[mode]["residual"]["mean"]/scale
        if name=="synchronized_evidence":
            expected+=parts[mode]["correction_js"]["mean"]/results["normalizers"]["correction_js"]["mean"]
        if not math.isclose(item["mean"],expected,rel_tol=1e-9,abs_tol=1e-12):
            raise ContractError("Saved score mean differs from declared paired formula")
    if results["validity"] != evaluate_validity(results["partitions"], plan, results["template_kinematics"]):
        raise ContractError("Saved scientific criteria differ from declared evaluation")
    return {"saved_index_rows": count, "score_variants": len(SCORES), "all_scores_finite": True,
            "paired_state_trajectory_shared": True, "all_references_immutable": True,
            "scientific_criteria_pass": results["validity"]["all_predeclared_checks_pass"],
            "calibration_or_final_opened": False}
