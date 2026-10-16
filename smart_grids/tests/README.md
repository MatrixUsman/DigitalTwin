# Planned tests — Smart grids

No test implementation or benchmark execution exists yet. Future tests should cover:

- Read-only loading, header handling, schema and feature/label/timestamp alignment.
- Chronological splits and window isolation across partitions, episodes and gaps.
- Training-only fitting and calibration independence from held-out data/labels.
- Known-value metric cases, denominators, event boundaries and detection latency.
- Causal replay: changing future samples cannot alter earlier decisions.
- Run/configuration/dataset provenance and repeatability where supported.

Use tiny, explicitly labelled `fixtures/synthetic/` for offline software checks. They must run without private datasets or internet access. Synthetic checks never establish benchmark performance. Add domain-specific physical-consistency checks only where their assumptions are justified.
