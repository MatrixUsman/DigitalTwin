# ModernTCN — selected transfer candidate

Status on 17 October 2026: **literature/design candidate, not execution-ready**. This is a recent general time-series comparator transferred to original CASPER, not a paper that published CASPER results or a digital twin.

- [Current decision and admission gates](../../docs/COMPARATOR_ADMISSION.md)
- [Full source/method audit and upstream evaluation changes](../../docs/literature/REPLACEMENT_COMPARATORS_2026-10-17.md)
- [Official ICLR 2024 manuscript](https://proceedings.iclr.cc/paper_files/paper/2024/file/86b1437c1e4c3b3c4debff98234a67e7-Paper-Conference.pdf)
- [Received PDF](../../local/comparator_admission_20261017/replacements/moderntcn_paper.pdf)
- [MIT author repository, pinned revision](https://github.com/luodhhh/ModernTCN/tree/56a9a2c018385cd5acef015378cae7f084d1b11c)
- [Public-source retrieval manifest](../../local/comparator_admission_20261017/replacements/retrievals.json)

The collected source subset includes model, layer, RevIN, loader, experiment loop, run entry, SWaT configuration, dependency declaration and license. It is **not a complete runnable checkout**. No upstream dataset, weights, installation or code execution occurred. The original source pack remains unchanged; these additional receipts live in ignored local storage.

Before implementation/fitting, resolve the current-conditioned reconstruction versus past-only forecast interface, freeze the adapter/configuration, validate a separate dependency environment and synthetic isolation/alignment tests, and specify a new bounded pilot. Do not run the upstream test-validation/threshold/point-adjustment paths.
