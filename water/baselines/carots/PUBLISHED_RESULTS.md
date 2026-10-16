# CAROTS published results and figures

**Everything indexed here belongs to the authors. Our project has produced zero benchmark results.** Acquisition and software smoke tests must never be presented as reproduction.

## Paper material

Read Table 1 in the [published PDF](artifacts/papers/CAROTS_ICML2025.pdf) for the original comparison and both CAROTS variants. Its best-F1 values are selected under the authors' reporting protocol; they are not operational-threshold scores from our common evaluation. The full and no-ensemble variants behave differently on WADI, which motivates studying both without choosing between them on our held-out tests.

The arXiv v1 source archive supplies the following editable source assets. They belong to that manuscript version; do not assume every source byte is identical to the proceedings edition.

| Source path beneath `artifacts/source/arxiv_v1/` | Use |
|---|---|
| `table/main.tex`, `table/std.tex` | Main reported results and standard deviations. |
| Other `table/*.tex` files | Ablations, architecture, causal discovery, computation, data description, similarity filtering, hyperparameters, over-time and synthetic results. |
| `figure/overview_jm_ver2.pdf`, `figure/components_jm_ver3.pdf` | Pipeline and components. |
| `figure/causalit_mtx_all.pdf` | Causal matrix illustration. |
| `figure/synthetic_all.pdf`, `figure/tsne_all_ver1.pdf` | Synthetic-series and embedding illustrations. |
| `references.bib`, `main.bbl` | Author bibliography and formatted references; individual references still require independent verification before reuse. |

All 13 table files and five figure PDFs are retained in the source bundle. Their existence does not supply underlying per-seed predictions or permit recomputing the reported statistics. The two repository overview images are separately available in [figure/](vendor/author_code/figure/).

## Downloaded author run artifacts

Each of [SWaT/cuts_plus/](artifacts/upstream_results/SWaT/cuts_plus/) and [WADI/cuts_plus/](artifacts/upstream_results/WADI/cuts_plus/) contains:

- `Graph.npy`: an author-derived causal graph array.
- Five `Graph_*.pdf` files: causal graph visualizations at upstream training steps.
- `best_result.txt`: causal-discovery validation loss and epoch, not anomaly detection F1.
- `checkpoint_best.pth`: **CUTS+ causal-discoverer checkpoint**, not final CAROTS detector weights.

The checkpoint role is confirmed by [trainer_carots.py](vendor/author_code/models/carots/trainer_carots.py), which loads this component into `model.causal_discoverer`, and the [CUTS+ trainer](vendor/author_code/models/carots/trainer_cuts_plus.py). Files were collected as bytes; binary checkpoints were not deserialized or executed.

No complete final-detector checkpoints, aligned test anomaly scores or complete detector logs were located in the audited tree. Store future project plots/results in our run folders and label any reused published figure or reported measurement with its source. Do not copy an author plot into a manuscript as if it came from our experiments.
