# Results

Output tables, plots, and logs from experiments.

## Structure (to be added)
- `tables/` — comparison tables (constant-skill model, Elo, TrueSkill, TTT) with 
  prediction accuracy, calibration, log-likelihood (mean ± std across runs)
- `plots/` — accuracy vs. computation-time trade-off, convergence curves
- `robustness/` — results from noise/data-reduction robustness studies, 
  including significance test outputs (e.g., paired test results)
- `logs/` — raw experiment logs

## Note
Results here should always be traceable back to the experiment config in `experiments/` 
that produced them.
