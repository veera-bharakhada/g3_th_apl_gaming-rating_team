# Results — Archived M3 experiments used for the M4 final report

## Provenance

The final M4 report summarizes the **M3 ten-seed paired ablation** and robustness experiments. No additional simulations are claimed for M4. The baseline and extension were evaluated under identical generated conditions for each seed. This directory contains archived experimental evidence, not a published TrueSkill Through Time benchmark.

## Archived files

| File | Contents |
|---|---|
| `main_10_seed_results.csv` | Per-seed, per-model main KPI values (10 seeds × 2 arms = 20 rows). |
| `main_summary_mean_sd.csv` | Archived means and sample standard deviations. |
| `paired_mae_test.json` | Paired skill-MAE reduction, significance test and bootstrap confidence interval. |
| `sample_size_robustness.csv` | Vary matches per time point (6, 12, 24). |
| `missing_observation_robustness.csv` | Vary fraction of missing individual observations. |
| `observation_noise_robustness.csv` | Vary individual observation noise SD. |
| `player_error_analysis_seed42.csv` | Per-player held-out skill errors for seed 42. |
| `MAE_comparison.png` | Skill-MAE comparison plot. |
| `RMSE_comparison.png` | Skill-RMSE comparison plot. |
| `Log_loss_comparison.png` | Held-out log-loss comparison plot. |
| `Brier_score_comparison.png` | Held-out Brier comparison plot. |
| `reliability_diagram_seed42.png` | Single-seed descriptive calibration/reliability diagram. |

## Main KPIs (10 paired seeds; mean ± sample SD)

| KPI | Team-only | + Individual evidence |
|---|---:|---:|
| Held-out skill MAE | 0.4372 ± 0.1400 | 0.2632 ± 0.0366 |
| Held-out skill RMSE | 0.5357 ± 0.1586 | 0.3284 ± 0.0395 |
| Held-out log-loss | 0.5835 ± 0.0568 | 0.5601 ± 0.0655 |
| Held-out Brier score | 0.1999 ± 0.0242 | 0.1893 ± 0.0269 |

Paired mean skill-MAE improvement is approximately 0.1740, with a 95% paired t-interval approximately [0.066, 0.282] and a paired t-test p-value approximately 0.0055. The extension improves skill MAE in all ten seeds. The probability-quality improvements are smaller. The seed-42 reliability diagram is descriptive and does not establish general calibration; no scalar expected calibration error (ECE) was archived.

## How to check or regenerate

From the `M4_G3/` directory:

```bash
python Code/verify_results.py
```

This **verifies archived outputs**, not their original generation. The source notebook `Code/src/CSE516_M3_Results_Analysis.ipynb` contains the simulation and robustness procedures; see `Code/README.md` for execution and output-location caveats. The notebook writes some CSVs into `M3_Results/` relative to its working directory and contains Colab-specific export cells. Do not assume running it automatically overwrites this directory.

## Statistical and interpretive cautions

- Skill MAE/RMSE compare estimated test-period skill trajectories to synthetic ground truth; held-out win predictions use log-loss and Brier score.
- Paired tests are based on the same seed in both arms. Mean ± SD and confidence intervals describe variability over this synthetic generator, not real-world uncertainty.
- Reduced posterior SD does **not** prove better-calibrated credible intervals.
- Runtime is hardware/environment dependent.
- Player-level failures and the reliability diagram are descriptive analyses of seed 42.
- Final paper figures and extra statistics (e.g. Wilcoxon/Holm) may have been post-processed from these CSVs. A standalone regeneration script for those extra final-paper figures/statistics is **not included in this README package**; do not claim it is until supplied and tested.
