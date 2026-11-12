# Group 3 — CSE 516 Milestone 2

**Project:** Bayesian Network-Based Estimation of Player Skill Over Time  
**Team:** Dhruvi Shah, Divija Nayak, Veera Bharakhada

## Original M2: temporal skill-inference prototype

The original M2 work defines a temporal Bayesian skill model and tests a restricted two-player TrueSkill Through Time (TTT)-style expectation-propagation (EP) prototype using synthetic match data. It includes supporting parameter experiments, diagnostics, an activity-aware pilot and automated tests. These are historical M2 investigations; they are **not** the same implementation as the individual-evidence extension below.

### Original M2 files

- [`Report/M2_Group3_Report.pdf`](Report/M2_Group3_Report.pdf) — original M2 report.
- [`M2_Group3_Colab_Demo.ipynb`](M2_Group3_Colab_Demo.ipynb) — demonstration notebook.
- [`Code/`](Code/) — source code, dependencies and execution instructions.
- [`Results/`](Results/) — original M2 experimental outputs and figures.
- [`M2_Data/README.md`](M2_Data/README.md) — synthetic-data description.
- [`Video/`](Video/) — original M2 video link file (currently named `M3_G2_video.md`; rename for clarity).

### Preliminary original M2 results

- Skill-recovery MAE: **0.3179 ± 0.0406**.
- EP convergence: **10/10 runs**.
- Mean EP iterations: **16.7**.
- Best validation log-loss: **0.5640** on 60 validation matches.

These values belong to the original restricted TTT-style EP prototype and **must not be compared as if they came from the separate MAP extension experiment**.

## M2 extension: individual-level evidence

The [`Extension/`](Extension/) folder contains a separate proof-of-concept study addressing the difficulty of distinguishing individual teammate skills from shared doubles outcomes. It introduces **synthetic individual performance observations** into a simplified temporal Bayesian model, fitted with **MAP/L-BFGS-B** and assessed with a **Laplace approximation**.

- [`Extension/README.md`](Extension/README.md) — detailed purpose, files, methods and reproduction steps.
- [`Extension/Report/CSE516_M2_Extension_Report.pdf`](Extension/Report/CSE516_M2_Extension_Report.pdf) — extension report.
- [`Extension/Code/CSE516_M2_Limitation_and_Solution.ipynb`](Extension/Code/CSE516_M2_Limitation_and_Solution.ipynb) — extension notebook.
- [`Extension/Results/`](Extension/Results/) — preliminary seed-42 outputs.

The extension's seed-42 skill MAE is **0.372678** for team-only evidence and **0.218028** with individual evidence. See its README for the remaining metrics. These are **single-seed preliminary results**, not the later M3 ten-seed averages.

## Progression

M2 established the original inference prototype and a separate individual-evidence extension. The subsequent [`M3_G3/`](../M3_G3/) milestone evaluates the team-only versus team-plus-individual-evidence ablation over ten seeds with statistical and robustness analysis. The final model is **not** presented as a full published TTT EP implementation or a head-to-head SOTA benchmark.

## Reproduction

For the original M2 code, see [`Code/README.md`](Code/README.md). For the separate extension notebook, see [`Extension/README.md`](Extension/README.md). Both use synthetic data; reported results do not establish real-world tennis performance.
