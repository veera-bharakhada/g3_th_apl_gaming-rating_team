# Experiments

Configuration files and random seeds for reproducible experiments.

## Structure (to be added)
- `configs/` — YAML/JSON config files specifying model hyperparameters, dataset splits, inference method used
- `seeds.txt` — random seeds used across runs for reproducibility
- `run_experiment.py` — entry point to launch an experiment from a config

## Convention
Each experiment config should specify:
- inference method (exact / approximate / win-lose-draw)
- learned parameters vs. fixed parameters
- dataset subset / noise level (for robustness studies)
- number of runs (for averaging + standard deviation reporting)
