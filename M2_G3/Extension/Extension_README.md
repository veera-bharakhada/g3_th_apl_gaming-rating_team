# M2 Extension — Individual-Level Evidence for Temporal Bayesian Player-Skill Estimation

**CSE 516 — Probabilistic Graphical Models | Group 3**  
**Authors:** Dhruvi Shah, Divija Nayak, Veera Bharakhada

## Purpose

Shared doubles-match outcomes provide team-level evidence but may not distinguish the contributions of individual teammates. This preliminary extension investigates whether adding simulated player-specific performance observations improves recovery of latent individual skills.

This is a **separate simplified temporal Bayesian implementation** using maximum a posteriori (MAP) optimisation and a Laplace approximation. It is **not a direct modification** of the original M2 restricted TTT-style expectation-propagation prototype.

## Files

| Path | Description |
|---|---|
| [`Report/CSE516_M2_Extension_Report.pdf`](Report/CSE516_M2_Extension_Report.pdf) | M2 extension report, including the graphical model, equations and preliminary results. |
| [`Code/CSE516_M2_Limitation_and_Solution.ipynb`](Code/CSE516_M2_Limitation_and_Solution.ipynb) | Self-contained experimental notebook. |
| [`Results/synthetic_doubles_data.csv`](Results/synthetic_doubles_data.csv) | Seed-42 synthetic doubles dataset (360 matches, 30 time points). |
| [`Results/skill_comparison.csv`](Results/skill_comparison.csv) | Team-only versus individual-evidence skill MAE and RMSE. |
| [`Results/prediction_comparison.csv`](Results/prediction_comparison.csv) | Held-out log-loss and Brier score. Runtime entries are not populated. |
| [`Results/player0_skill_estimation.png`](Results/player0_skill_estimation.png) | Illustrative Player 0 skill estimates and approximate uncertainty. |

## Model and experiment

- Latent player skills evolve under a Gaussian random-walk prior.
- Doubles outcomes are modelled using a logistic likelihood of team skill differences.
- The extension adds Gaussian observations of individual player performance, generated synthetically from latent skill plus noise.
- MAP estimates are computed using SciPy L-BFGS-B; a Laplace approximation supplies approximate posterior uncertainty.
- The data are split chronologically: times 0–20 for fitting and 21–29 for held-out evaluation. Held-out outcomes and individual observations are excluded from fitting.
- This M2 extension reports a **single preliminary seed (42)**. The subsequent M3 study separately evaluates ten seeds (42–51) and robustness experiments.

## Preliminary single-seed results

| Metric | Team outcomes only | Team + individual observations |
|---|---:|---:|
| Skill MAE | 0.372678 | 0.218028 |
| Skill RMSE | 0.466809 | 0.285278 |
| Held-out log-loss | 0.596247 | 0.554177 |
| Held-out Brier score | 0.204032 | 0.186403 |

These results illustrate the benefit of additional skill-related evidence **under the synthetic data-generating assumptions**. They do not establish improvement on real tennis data or every individual player.

## Reproduce

1. Open [`Code/CSE516_M2_Limitation_and_Solution.ipynb`](Code/CSE516_M2_Limitation_and_Solution.ipynb) in Google Colab or Jupyter.
2. Run the cells from top to bottom, including any dependency-installation cell.
3. The notebook creates a local `Limitation_Solution_Results/` directory with the synthetic data, comparison CSVs and Player 0 figure. Compare the generated outputs with the committed files under `Results/`.

The notebook's output directory is relative to the notebook's **execution working directory**; it is not automatically the repository's `Extension/Results/` folder. Runtime depends on the environment.

## Relationship to the milestones

- [`../../README.md`](../../README.md): original M2 prototype and its separate experiments.
- [`../../../M3_G3/`](../../../M3_G3/): subsequent ten-seed evaluation of team-only versus team-plus-individual evidence.

**Data note:** All individual observations in this extension are simulated, not real ATP player statistics.
