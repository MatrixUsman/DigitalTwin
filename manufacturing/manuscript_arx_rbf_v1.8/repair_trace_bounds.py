"""Expose a clipped label by enlarging only the historical PDF page box."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

M = Path(__file__).resolve().parent
P = M.parent
source = P / "manuscript_arx_rbf_v1.7/figures/trace.pdf"
target = M / "figures/trace.pdf"
reader = PdfReader(source)
assert len(reader.pages) == 1
page = reader.pages[0]
original_content = page.get_contents().get_data()
box = [float(x) for x in page.mediabox]
writer = PdfWriter()
writer.add_page(page)
expanded = [box[0], box[1], box[2], box[3] + 8.0]
writer.pages[0].mediabox = RectangleObject(expanded)
writer.pages[0].cropbox = RectangleObject(expanded)
with target.open("wb") as stream:
    writer.write(stream)
reloaded = PdfReader(target)
assert reloaded.pages[0].get_contents().get_data() == original_content
receipt = {
    "utc": datetime.now(timezone.utc).isoformat(),
    "classification": "layout repair only: 8pt upper page-box expansion; PDF drawing stream unchanged",
    "command": ".venv-pdf/bin/python manuscript_arx_rbf_v1.8/repair_trace_bounds.py",
    "cwd": str(P), "original_media_box": box, "new_media_box": expanded,
    "content_stream_sha256": sha256(original_content).hexdigest(),
    "content_stream_exactly_preserved": True,
    "new_signal_read_or_computed": False,
    "sha256": {str(p.relative_to(P)): sha256(p.read_bytes()).hexdigest()
               for p in [source, target, Path(__file__).resolve()]}}
(M / "TRACE_LAYOUT_REPAIR.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({"content_preserved": True, "top_padding_points": 8.0}))
