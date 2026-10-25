"""Read-only verification of earlier scientific bindings and this diagnostic."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCES = (
    "manuscript_arx_rbf_v1.6/PACKAGE_MANIFEST.json",
    "manuscript_arx_rbf_v1.7/PACKAGE_MANIFEST.json",
    "research_cycles/review_extension_v0.18/PACKAGE_MANIFEST.json",
    "research_cycles/context_recovery_v0.19/FINAL_FREEZE.json",
    "research_cycles/context_recovery_v0.19/PACKAGE_MANIFEST.json",
    "research_cycles/rapt_protocol_v0.21/exploratory/FREEZE.json",
    "research_cycles/novelty_v0.22/decomposition/PACKAGE_MANIFEST.json",
)


def digest(path):
    state = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            state.update(block)
    return state.hexdigest()


def main():
    records = []
    failures = []
    for source in SOURCES:
        manifest = ROOT / source
        data = json.loads(manifest.read_text())
        bindings = data.get("sha256", data.get("bindings"))
        if not isinstance(bindings, dict):
            raise ValueError(f"Unknown binding schema: {source}")
        # v0.18's package stores paths relative to its own directory; the other
        # inspected manifests use manufacturing-relative paths. Never guess
        # the root from file existence (README/.gitignore occur at both roots).
        binding_root = (manifest.parent if source ==
                        "research_cycles/review_extension_v0.18/PACKAGE_MANIFEST.json"
                        else ROOT)
        for relative, expected in bindings.items():
            path = binding_root / relative
            actual = digest(path) if path.is_file() else None
            if actual != expected:
                failures.append({"manifest": source, "path": relative,
                                 "expected": expected, "actual": actual})
        records.append({"manifest": source, "sha256": digest(manifest),
                        "binding_root": str(binding_root.relative_to(ROOT)),
                        "bindings_checked": len(bindings)})
    report = {"utc": datetime.now(timezone.utc).isoformat(),
              "classification": "byte preservation, not scientific validation",
              "correction": "Attempt 001 incorrectly resolved v0.18 paths from manufacturing; preserved receipt/source. No scientific artifact was altered.",
              "sources": records, "failures": failures,
              "all_match": not failures}
    (HERE / "PRESERVATION_RECEIPT.json").write_text(
        json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
