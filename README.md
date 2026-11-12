# Temporal Bayesian Player-Skill Estimation — CSE 516 Group 3

**Course:** CSE 516 — Probabilistic Graphical Models  
**Project:** Individual-Level Evidence for Temporal Bayesian Player-Skill Estimation: A Controlled Ablation  
**Team:** Dhruvi Shah · Divija Nayak · Veera Bharakhada  
**Status:** M1–M4 project artifacts assembled (final submission)

## Overview

Doubles-match outcomes reveal information about a team's combined strength but can leave the abilities of individual teammates difficult to distinguish. This project investigates whether **noisy individual-level observations** improve estimation of **time-varying latent player skills** compared with using team match outcomes alone.

The final experiment is a **controlled synthetic ablation** of two simplified temporal probabilistic models:

- **Team-only baseline:** latent Gaussian random-walk player skills with a logistic likelihood for doubles-match results.
- **Individual-evidence extension:** the same model and match outcomes, augmented with Gaussian observations associated with participating individual players.

Both models use maximum a posteriori (MAP) estimation via SciPy L-BFGS-B and a Laplace approximation to quantify local posterior uncertainty. This final comparison is **not** a reproduction of published TrueSkill Through Time (TTT) or a head-to-head benchmark against it.

## Project progression

| Milestone | Scope | Location |
|---|---|---|
| M1 — Proposal | Research question, TTT literature anchor, initial representation/inference/learning plan and dataset exploration | [`M1_G3/`](M1_G3/) |
| M2 — Implementation and extension | Initial TTT-inspired inference prototype and a separate individual-evidence MAP/Laplace extension; preliminary demonstrations | [`M2_G3/`](M2_G3/) |
| M3 — Evaluation | Ten-seed paired comparison, predictive metrics, robustness sweeps, uncertainty and player-level diagnostics | [`M3_G3/`](M3_G3/) |
| M4 — Final synthesis | Conference-style report, presentation, video link, consolidated code/data/results and reproducibility notes | [`M4_G3/`](M4_G3/) |

The research direction evolved across milestones. In particular, the **M2 original TTT-inspired prototype** and the **M2 individual-evidence extension** are distinct implementations. The M3/M4 numerical results refer to the simplified individual-evidence ablation, not to a direct comparison with the published TTT software.

## Final experimental setup

- **Data:** synthetic doubles matches with known latent skills; 12 players, 30 time points, 12 matches per time point.
- **Paired runs:** 10 seeds, 42–51; both models evaluated on matching synthetic conditions for each seed.
- **Split:** time points 0–20 for training; 21–29 for held-out evaluation.
- **Model parameters:** skill prior SD 1.0, temporal drift SD 0.12, logistic temperature 0.8, individual-observation noise SD 0.65.
- **Inference:** MAP via L-BFGS-B; Laplace covariance approximation from the local Hessian.
- **Metrics:** held-out latent-skill MAE/RMSE, match-outcome log-loss/Brier score, runtime, optimizer iterations and approximate posterior SD.
- **Additional analyses:** observation missingness, observation noise, match-count robustness, seed-42 player errors and a descriptive reliability diagram.

The synthetic individual observations are informative by construction. No test-period match outcomes or individual observations are used to fit the models.

## Main findings

| Metric (10 paired seeds; mean ± sample SD) | Team-only baseline | Individual evidence |
|---|---:|---:|
| Skill MAE ↓ | 0.4372 ± 0.1400 | **0.2632 ± 0.0366** |
| Skill RMSE ↓ | 0.5357 ± 0.1586 | **0.3284 ± 0.0395** |
| Match log-loss ↓ | 0.5835 ± 0.0568 | **0.5601 ± 0.0655** |
| Match Brier score ↓ | 0.1999 ± 0.0242 | **0.1893 ± 0.0269** |

The mean paired skill-MAE reduction is **0.173951** (about **39.8%** relative to baseline). All 10 paired seeds show an MAE reduction; the archived paired t-test gives **p ≈ 0.00547**, and the paired bootstrap 95% confidence interval for the reduction is approximately **[0.0971, 0.2736]**. These results support an improvement **within the specified synthetic generator**, not a general claim about real-world tennis or published TTT. Smaller approximate posterior SD alone does not demonstrate better uncertainty calibration.

## Repository guide

```text
.
├── README.md                         # This overview
├── BasePaper/                        # Published TTT reference paper
├── Data/                             # Earlier dataset/source notes
├── M1_G3/                            # Proposal milestone
├── M2_G3/                            # Initial implementation and extension
├── M3_G3/                            # Experimental evaluation milestone
└── M4_G3/                            # Final submission package
    ├── README.md                     # Final-project details
    ├── Report/M4_G3_Report.pdf
    ├── Presentation/M4_G3_Slides.pdf
    ├── Video/                        # Video link; see submission note below
    ├── Code/
    │   ├── README.md
    │   ├── requirements.txt
    │   ├── verify_results.py
    │   └── src/
    │       ├── CSE516_M2_Limitation_and_Solution.ipynb
    │       └── CSE516_M3_Results_Analysis.ipynb
    ├── Data/
    │   ├── README.md
    │   └── synthetic_doubles_data.csv
    └── Results/                      # CSV tables, tests, diagnostics and plots
```

For the **final deliverable**, start with [`M4_G3/README.md`](M4_G3/README.md). The M4 `Code/`, `Data/` and `Results/` directories each include their own documentation.

## Quick start: verify archived results

From the repository root, install Python 3 dependencies and run:

```bash
python -m pip install -r M4_G3/Code/requirements.txt
python M4_G3/Code/verify_results.py
```

The verifier checks the archived CSV structure, seed pairing, metrics and recorded MAE reduction. **It does not rerun the models or independently recompute the archived significance test.** To reproduce experiments, open [`M4_G3/Code/src/CSE516_M3_Results_Analysis.ipynb`](M4_G3/Code/src/CSE516_M3_Results_Analysis.ipynb) and follow [`M4_G3/Code/README.md`](M4_G3/Code/README.md). The notebook includes Google Colab-specific download cells and writes some results to a relative `M3_Results/` directory; a complete clean-environment rerun has not been asserted here.

## Research reference and scope

**Base paper:** G. Landfried and E. Mocskos, *TrueSkill Through Time: Reliable Initial Skill Estimates and Historical Comparability with Julia, Python, and R*, Journal of Statistical Software **112**(6), 2025. [DOI: 10.18637/jss.v112.i06](https://doi.org/10.18637/jss.v112.i06). The paper provides the temporal-skill modeling research context; the final experiment uses a simpler model and different inference approach.

**Limitations:** synthetic data only; player-level signals constructed to be informative; fixed hyperparameters; no published-TTT head-to-head evaluation; no demonstrated transfer to real-world player ratings; and approximate posterior uncertainty without a comprehensive calibration guarantee.

## Final submission notes

The M4 directory contains the report, slides, code, data and results. **Before submission, rename** `M4_G3/Video/M4_G3_Video.md` **to** `M4_G3/Video/M4_G3_Video_Link.txt` **to match the requested filename**, preserving the existing video URL. Verify the video is accessible to the evaluators. Each group member must also complete the required individual submission form separately.
