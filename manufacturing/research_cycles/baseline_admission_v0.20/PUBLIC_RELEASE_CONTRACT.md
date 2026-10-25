# Public original-system evidence: proposed admission contract

**Metadata-only audit,19 October2026. This document proposes access boundaries; it does not authorize or claim final observation access.**

[Dataset](https://huggingface.co/datasets/hmunn/rapt-g1-ood), author-linked from official CSIRO code, revision`d40fa1f893cc4519d67abff142428ea0f0c4a1eb`, declares BSD-3-Clause. Saved metadata/card receipt:`DOCUMENT_RECEIPT.json`; complete file listing:`dataset_tree.json`. Public downloads need no iTrust-style request. Retain license/citation and immutable raw files; package only results/metadata unless separately approved.

## Exact source files

| Source file | Bytes | Expected source SHA256 (HuggingFace LFS oid) |
|---|---:|---|
| `g1_velocity/train_small.npz` |63,515,936|`363a04f7a339b46f347003bc91246d0e3106f4aaf4084fbee9130791b4c85859`|
| `g1_velocity/train.npz` |259,809,455|`d04b7561cdbc892e3c52dea4bf1a4b9a41c25610285afb1e92dd4f19f8b9e10c`|
| `g1_velocity/calibration.npz` |38,435,113|`382d0120c0842d4753414f798433c4c4b3228a3fac3c0ba8ccebd6c138cf5139`|
| `g1_velocity/test.npz` |129,363,718|`0e02b9aee18a42440d2492fd7dede6eceb9f4c2441e4c4f61965c8b3604ea7ae`|
| `g1_velocity_real/calibration.npz` |1,596,078|`851a058c09346f1245cf3a97015b547bdd032cc497c4abbba657406e75800997`|
| `g1_velocity_real/test.npz` |49,509,222|`315dcb6cf0d2cedc00b322ca63e9314bc4659f58a33510d7515b13ce137b6112`|

Author checkpoint at pinned code revision: `checkpoints/g1_29dof_velocity/model.pt`10,786,897bytes; config3,714; observation stats12,817; calibration11,756. Optional ONNX10,825,020bytes not required. Model/normalizer architecture correspondence must be checked with strict state-dictionary loading using `weights_only=True`. No original policy, IsaacLab installation, new physical run or LLM is necessary to replay the detector.

## Original inputs and semantics

`checkpoint_config.json` names96observation dimensions: root velocity3,gravity3,command velocity3,joint position29,joint velocity29,previous action29. A separate29-dimensional raw policy action is the forward-dynamics input. Sampling interval.02seconds. Do not map this pretrained model onto four-dimensional manufacturing signals.

The public card describes ragged float16NPZ arrays: `seq_%05d`, `act_%05d`, dimension names; test also labels/onset/fault. G1 physical runs are induced faults and deployment anomalies, **not an industrial-arm cyberattack/recovery benchmark**. Candidate transformation requires explicit unit/scaling/causality audit; no physically certified joint projection is justified from channel names alone.

## Metadata conflicts to resolve before final freeze

- Simulated velocity card reports225calibration episodes and14faultcategories; savedmetadata says`cal_episodes:0` and categories only`init_state,env_disturbance`, despite a38MBcalibration archive and833testsequences. These appear stale but are not silently corrected.
- Physical card and split description report50runs=11normal+39anomalous; its metadata note says78versus45. Missing-category arithmetic and exact current archive contents must be audited.
- Card says physical calibration~2.3minutes; paper§4.3describes3×1minute. Treat current release as its own identifiable calibration population.
- Physical intervention onsets are unknown(−1),some sequences1–22rows. Never manufacture onsets, treat short cases as normal, use sequence length as a detector feature, or report recovery/delay from unavailable labels.

A permissible metadata pass can inspect ZIP members/NumPy headers and provider label/name/onset arrays without opening signal arrays. Record it explicitly, before freezing method choices. Then fix the complete episode roster and coverage policy, including every short episode. Label counts are protocol design metadata; they must not be used to choose a favorable score variant.

## Proposed bounded two-track execution

1. **Author system release audit:** frozen pretrained model/normalizer, current public normal-calibration archive, released model-only and hybrid gates, and separately named paper-formula gates. All three declared before test signals. Public testlabels are joined after per-row scores are sealed. Report actual calibration population, episode confusion, scoreAP/AUROC, point support, runtime, unscorable first observations and short/missing cases. No oracle threshold.
2. **Transferred controlled mechanism study:** normal-only RAPT training on the same admissible numerical data as our method, common frozen synthetic tasks/threshold rules and prospective criteria. Full released architecture; all modifications disclosed. Evaluate recovery only where the simulator supplies a declared diagnostic truth.

Track1provides independent physical-recording evidence about the released detector, but cannot validate the same protected-command recovery hypothesis unless the required command/truthcontract is independently established. Never pool track1andtrack2scores or claim generalization merely from running both. At this audit stage neither track has been run.
