"""Standard-library replay of exposed synthetic v0.19 episode-paired outcomes.

This adds descriptive reporting. It neither trains nor evaluates a new detector.
All deltas are candidate minus comparator; no inferential sampling claim is made.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = "context_set"
COMPARATORS = ("base_dual", "context_hysteresis", "global_set")
META = ("task", "plant", "parent", "plant_group", "condition", "seed", "noise_seed",
        "eligible", "event", "benign", "outside_points", "physical_return", "return_missing")
METRICS = (
    ("alarm_points", "benign", "lower"),
    ("alarm_episodes", "benign", "lower"),
    ("outside_inactive", "event", "lower"),
    ("joint", "event", "higher"),
    ("fresh", "event", "higher"),
    ("fresh_delay", "event", "lower"),
    ("clear_delay", "event", "lower"),
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def quantile(values, p):
    """Linear interpolation between finite-grid order statistics, not a CI."""
    if not values:
        return None
    x = sorted(values)
    position = (len(x) - 1) * p
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    return x[lower] + (position - lower) * (x[upper] - x[lower])


def describe(values):
    if not values:
        return dict(n=0, total=None, mean=None, median=None, p95=None, minimum=None, maximum=None)
    if any(not math.isfinite(v) for v in values):
        raise ValueError("Nonfinite metric")
    return dict(n=len(values), total=sum(values), mean=sum(values) / len(values),
                median=quantile(values, .5), p95=quantile(values, .95),
                minimum=min(values), maximum=max(values))


def match(rows, comparator):
    indices = {m: {} for m in (CANDIDATE, comparator)}
    for row in rows:
        method = row["method"]
        if method not in indices:
            continue
        key = row["id"]
        if key in indices[method]:
            raise ValueError("Duplicate method/episode identity")
        indices[method][key] = row
    left, right = indices[CANDIDATE], indices[comparator]
    if not left or set(left) != set(right):
        raise ValueError("Incomplete paired population")
    pairs = []
    for key in sorted(left):
        a, b = left[key], right[key]
        for field in META:
            if a[field] != b[field]:
                raise ValueError("Mismatched episode metadata: " + field)
        if bool(a["event"]) == bool(a["benign"]):
            raise ValueError("Exactly one event/benign role required")
        pairs.append((a, b))
    return pairs


def groups(pairs):
    yield "pooled", "all", pairs
    for key in ("task", "plant", "condition", "plant_group"):
        for value in sorted({a[key] for a, _ in pairs}):
            yield key, value, [(a, b) for a, b in pairs if a[key] == value]
    for value in sorted({(a["task"], a["plant"], a["condition"]) for a, _ in pairs}):
        yield "task_plant_condition", "|".join(value), [
            (a, b) for a, b in pairs if (a["task"], a["plant"], a["condition"]) == value]


def paired_metric(pairs, metric, population, direction):
    eligible = [(a, b) for a, b in pairs if a[population]]
    available = [(a[metric], b[metric]) for a, b in eligible
                 if a[metric] is not None and b[metric] is not None]
    delta = [float(a) - float(b) for a, b in available]
    # Fixed roundoff tolerance only for second-valued delays; integer counts exact.
    tolerance = 1e-12 if metric.endswith("delay") else 0
    ties = sum(abs(v) <= tolerance for v in delta)
    wins = sum(v < -tolerance if direction == "lower" else v > tolerance for v in delta)
    result = dict(metric=metric, population=population, preferred_direction=direction,
                  possible_pairs=len(eligible), observed_pairs=len(available),
                  candidate_missing=sum(a[metric] is None for a, _ in eligible),
                  comparator_missing=sum(b[metric] is None for _, b in eligible),
                  wins=wins, ties=ties, losses=len(delta) - wins - ties,
                  delta=describe(delta),
                  candidate_values=describe([float(a) for a, _ in available]),
                  comparator_values=describe([float(b) for _, b in available]),
                  conditional_on_both_observed=metric.endswith("delay"),
                  tie_tolerance=tolerance)
    return result


def discordance(pairs, key):
    eligible = [(a, b) for a, b in pairs if a["event"]]
    return dict(events=len(eligible),
                both=sum(bool(a[key]) and bool(b[key]) for a, b in eligible),
                candidate_only=sum(bool(a[key]) and not b[key] for a, b in eligible),
                comparator_only=sum(not a[key] and bool(b[key]) for a, b in eligible),
                neither=sum(not a[key] and not b[key] for a, b in eligible))


def missingness(rows):
    events = [a for a in rows if a["event"]]
    return dict(event_denominator=len(events),
                overlap_detected=sum(a["overlap"] for a in events),
                overlap_missed=sum(not a["overlap"] for a in events),
                fresh_detected=sum(a["fresh"] for a in events),
                fresh_missing=sum(a["fresh_delay"] is None for a in events),
                return_missing=sum(a["return_missing"] for a in events),
                overlap_and_return=sum(a["returned_detected"] for a in events),
                clearance_observed=sum(a["clear_delay"] is not None for a in events),
                clearance_missing_total=sum(a["clear_delay"] is None for a in events),
                clearance_censored_after_detected_return=sum(
                    a["returned_detected"] and a["clear_delay"] is None for a in events),
                already_inactive_at_return=sum(a["already_clear_at_return"] for a in events),
                active_at_return_then_clear=sum(a["returned_detected"] and
                    not a["already_clear_at_return"] and a["clear_delay"] is not None for a in events),
                joint_success=sum(a["joint"] for a in events))


def analyze(rows):
    comparisons, effects, episode_rows = [], [], []
    for comparator in COMPARATORS:
        pairs = match(rows, comparator)
        for group, value, pp in groups(pairs):
            prefix = dict(candidate=CANDIDATE, comparator=comparator, group=group, value=value)
            comparisons.append(dict(**prefix, matched_episodes=len(pp),
                benign_episodes=sum(a["benign"] for a, _ in pp),
                attack_episodes=sum(a["event"] for a, _ in pp),
                benign_hours=sum(a["eligible"] for a, _ in pp if a["benign"]) * .02 / 3600,
                fresh=discordance(pp, "fresh"), joint=discordance(pp, "joint"),
                candidate_missingness=missingness([a for a, _ in pp]),
                comparator_missingness=missingness([b for _, b in pp])))
            for metric, population, direction in METRICS:
                if any(a[population] for a, _ in pp):
                    effect = paired_metric(pp, metric, population, direction)
                    effects.append(dict(**prefix, **effect))
        for a, b in pairs:
            record = dict(id=a["id"], candidate=CANDIDATE, comparator=comparator,
                          **{key: a[key] for key in META})
            for metric, population, _ in METRICS:
                applicable = bool(a[population])
                record[metric + "_candidate"] = a[metric] if applicable else None
                record[metric + "_comparator"] = b[metric] if applicable else None
                record[metric + "_delta"] = (float(a[metric]) - float(b[metric])
                    if applicable and a[metric] is not None and b[metric] is not None else None)
            episode_rows.append(record)
    return dict(scope="post-final descriptive episode-paired analysis of exposed synthetic grid",
                delta_definition="candidate minus comparator",
                new_training=False, new_final_evaluation=False,
                inferential_tests=False, bootstrap=False,
                independent_real_robot_generalization=False,
                comparisons=comparisons, effects=effects, episodes=episode_rows)


def verify_original(rows, results):
    """Independent arithmetic against every original non-cross stratum/method."""
    checks = 0
    for summary in results["summary"]:
        rr = [r for r in rows if r["method"] == summary["method"] and
              (summary["group"] == "pooled" or r[summary["group"]] == summary["value"])]
        events, benign = [r for r in rr if r["event"]], [r for r in rr if r["benign"]]
        expected = dict(episodes=len(rr), events=len(events), benign_points=sum(r["eligible"] for r in benign),
            benign_alarms=sum(r["alarm_points"] for r in benign), starts=sum(r["alarm_episodes"] for r in benign),
            fresh=sum(r["fresh"] for r in events), hits=sum(r["overlap"] for r in events),
            joint=sum(r["joint"] for r in events), outside_points=sum(r["outside_points"] for r in events),
            outside_inactive=sum(r["outside_inactive"] for r in events),
            absent_return=sum(r["return_missing"] for r in events),
            already_inactive_at_return=sum(r["already_clear_at_return"] for r in events))
        for key, value in expected.items():
            if value != summary[key]:
                raise ValueError("Original summary disagreement: " + key)
            checks += 1
        for key in ("fresh_delay", "detection_delay", "clearance_delay"):
            source_key = "clear_delay" if key == "clearance_delay" else key
            values = [r[source_key] for r in events if r[source_key] is not None]
            d = describe(values)
            for field, original_field in (("n", "n"), ("median", "median"), ("p95", "p95"), ("maximum", "max")):
                a, b = d[field], summary[key][original_field]
                if (a is None) != (b is None) or (a is not None and not math.isclose(a, b, abs_tol=1e-12)):
                    raise ValueError("Original delay disagreement")
                checks += 1
    return checks


def export_csv(path, rows):
    if not rows:
        return
    with Path(path).open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((HERE / "INPUT_MANIFEST.json").read_text())
    for name, record in manifest["files"].items():
        if sha(HERE / "inputs" / name) != record["sha256"]:
            raise ValueError("Input changed: " + name)
    rows = json.loads((HERE / "inputs/outcomes.json").read_text())
    result = json.loads((HERE / "inputs/results.json").read_text())
    checks = verify_original(rows, result)
    table = analyze(rows)
    for effect in table["effects"]:
        assert effect["wins"] + effect["ties"] + effect["losses"] == effect["observed_pairs"]
        checks += 1
    for comparison in table["comparisons"]:
        for name in ("fresh", "joint"):
            d = comparison[name]
            assert sum(d[k] for k in ("both", "candidate_only", "comparator_only", "neither")) == d["events"]
            checks += 1
    write(output / "paired.json", table)
    flat = []
    for r in table["effects"]:
        d = {k: v for k, v in r.items() if not isinstance(v, dict)}
        for part in ("delta", "candidate_values", "comparator_values"):
            d.update({part + "_" + k: v for k, v in r[part].items()})
        flat.append(d)
    export_csv(output / "paired_effects.csv", flat)
    export_csv(output / "episode_pairs.csv", table["episodes"])
    write(output / "REPLAY.json", dict(status="passed", checks=checks, original_outcomes=len(rows),
        episode_pairs=len(table["episodes"]), descriptive_effect_rows=len(flat),
        group_contrasts=len(table["comparisons"]), original_primary=result["primary"],
        original_primary_unchanged=True, final_outcomes_exposed_before_analysis=True,
        input_manifest_sha256=sha(HERE / "INPUT_MANIFEST.json"), source_sha256=sha(__file__),
        outputs={p.name: sha(p) for p in sorted(output.iterdir())}))
    print(json.dumps(dict(status="passed", checks=checks, paired_episodes=len(table["episodes"]),
                         group_contrasts=len(table["comparisons"]), effects=len(flat))))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
