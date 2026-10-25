"""Audit manuscript identities, citations, assets and compilation, not efficacy."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
from pypdf import PdfReader

M = Path(__file__).resolve().parent
P = M.parent
checks = []


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def check(name, condition):
    checks.append({"check": name, "passed": bool(condition)})


old = json.loads((P / "manuscript_arx_rbf_v1.7/PACKAGE_MANIFEST.json").read_text())
for name, expected in old["sha256"].items():
    check("preserved v1.7 " + name, digest(P / name) == expected)
base = json.loads((M / "BASE_IDENTITY.json").read_text())
for name, expected in base["bindings"].items():
    check("copied-source origin " + name, digest(P / name) == expected)
for directory in ["figures", "generated"]:
    for path in (P / "manuscript_arx_rbf_v1.7" / directory).glob("*"):
        if path.is_file():
            if directory == "figures" and path.name == "trace.pdf":
                check("historical trace drawing stream preserved",
                      PdfReader(M / directory / path.name).pages[0].get_contents().get_data()
                      == PdfReader(path).pages[0].get_contents().get_data())
                continue
            if directory == "figures" and path.name == "matched_review.pdf":
                layout = json.loads((M / "MATCHED_LAYOUT_REPAIR.json").read_text())
                source = json.loads((P / "research_cycles/review_extension_v0.18/REPORTING.json").read_text())
                for key, values in layout["parts"].items():
                    check("unchanged matched-figure part " + key,
                          values == [sum(d[key] for d in source["diagnostics"] if d["method"] == method)
                                     for method in layout["methods"]])
                source_rows = {r["method"]: r for r in source["pooled"]}
                check("unchanged matched-figure hourly starts", layout["starts_per_hour"]
                      == [source_rows[method]["benign_starts_per_hour"] for method in layout["methods"]])
                continue
            check("retained old numerical asset " + path.name,
                  digest(M / directory / path.name) == digest(path))

all_tex = [M / "main.tex", *sorted((M / "sections").glob("*.tex"))]
text = "\n".join(p.read_text() for p in all_tex)
citations = {key for group in re.findall(r"\\cite\{([^}]+)\}", text)
             for key in group.split(",")}
reference_list = re.findall(r"\\bibitem\{([^}]+)\}", (M / "references.tex").read_text())
check("28 unique cited references", len(reference_list) == len(set(reference_list)) == 28
      and citations == set(reference_list))
labels = re.findall(r"\\label\{([^}]+)\}", text)
check("unique manuscript labels", len(labels) == len(set(labels)))
for path in all_tex:
    for target in re.findall(r"\\input\{([^}]+)\}", path.read_text()):
        check("input exists " + target, (M / target).is_file() or (M / (target + ".tex")).is_file())
    for target in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", path.read_text()):
        check("figure exists " + target, (M / target).is_file())
for marker in ["TODO", "TBD", "PLACEHOLDER", "INSERT RESULT"]:
    check("no unresolved placeholder " + marker, marker not in text)
for marker in ["OpenAI Codex assisted", "not presented as a new theorem",
               "not evidence of an open gap", "already exposed", "5,175", "70,800",
               "518,400", "3.2055", "2.0123", "The primary criterion therefore fails"]:
    check("required evidence or qualification " + marker, marker in text)

for receipt_name in ["DIAGNOSTIC_ASSETS.json", "PILOT_ASSETS.json", "TRACE_LAYOUT_REPAIR.json", "MATCHED_LAYOUT_REPAIR.json"]:
    receipt_path = M / receipt_name
    check("asset receipt exists " + receipt_name, receipt_path.is_file())
    if receipt_path.is_file():
        for path, expected in json.loads(receipt_path.read_text())["sha256"].items():
            check("verified asset " + path, digest(P / path) == expected)

source = json.loads((P / "research_cycles/novelty_v0.22/decomposition/STRATA.json").read_text())
plotted = json.loads((M / "DIAGNOSTIC_FIGURE_VALUES.json").read_text())
check("all eight persistent channels plotted", plotted["displayed_prespecified_condition_strata"]
      == [r for task in ["L19", "S19"] for c in ["q1", "q2", "v1", "v2"]
          for r in source if r["condition"] == "persistent_offset"
          and r["task"] == task and r["channel"] == c])

build = json.loads((M / "MAIN_BUILD_RECEIPT.json").read_text())
for path, expected in build["source_sha256"].items():
    check("compiled source " + path, digest(M / path) == expected)
pdf = P / build["pdf"]
reader = PdfReader(pdf)
check("PDF identity", digest(pdf) == build["pdf_sha256"])
check("title preserved", reader.metadata.title == "ARX–RBF Motion Modeling for Cyberattack Detection and Recovery Monitoring in Industrial Robots")
check("user-selected byline preserved", reader.metadata.author == "Muhammad Usman")
log = (P / build["attempt"] / "main.log").read_text()
for problem in ["Overfull", "undefined", "Missing character", "! LaTeX Error"]:
    check("no compiler issue " + problem, problem not in log)
extracted = "\n".join(page.extract_text() for page in reader.pages)
check("PDF text nonempty", len(extracted) > 20000)
check("one integrated document", "separate manuscript supplement" not in text)
actions = (M / "AUTHOR_ACTIONS.md").read_text()
check("human approval not invented", "human author" in actions and "not inferred" in actions)
report = {"utc": datetime.now(timezone.utc).isoformat(),
          "classification": "manuscript consistency and byte identity; not scientific or author approval",
          "passed": all(c["passed"] for c in checks), "checks": len(checks),
          "pages": len(reader.pages), "pdf_sha256": digest(pdf), "details": checks}
(M / "AUDIT.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: report[k] for k in ["passed", "checks", "pages", "pdf_sha256"]}))
if not report["passed"]:
    raise SystemExit([c for c in checks if not c["passed"]])
