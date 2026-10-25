"""Seal the completed research/design record, not an efficacy claim."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST = HERE / "PACKAGE_MANIFEST.json"


def main():
    missing_links = []
    local_links = 0
    for path in HERE.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if re.match(r"[a-zA-Z]+://", target) or target.startswith("#"):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            local_links += 1
            if not (path.parent / target).exists():
                missing_links.append({"source": str(path.relative_to(ROOT)),
                                      "target": target})
    if missing_links:
        raise ValueError(json.dumps(missing_links, indent=2))
    paths = sorted(p for p in HERE.rglob("*") if p.is_file()
                   and p != MANIFEST and "__pycache__" not in p.parts)
    bindings = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                for p in paths}
    manifest = {"utc": datetime.now(timezone.utc).isoformat(),
                "classification": "completed research/design and exploratory diagnostic; provisional novelty only",
                "candidate_trained": False, "originality_established": False,
                "submission_ready": False, "local_links_checked": local_links,
                "files": len(bindings), "bindings": bindings,
                "ignored_arrays": "Bound by decomposition/PACKAGE_MANIFEST.json; not copied or released"}
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    assert all(sha256((ROOT / p).read_bytes()).hexdigest() == value
               for p, value in bindings.items())
    print(json.dumps({"files": len(bindings), "local_links_checked": local_links,
                      "sha256": sha256(MANIFEST.read_bytes()).hexdigest(),
                      "all_rechecked": True}))


if __name__ == "__main__":
    main()
