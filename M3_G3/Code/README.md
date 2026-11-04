# Code – M3 Experiments

## Contents

This folder contains the Jupyter Notebook used to implement and evaluate the proposed Bayesian player-skill estimation approach.

### Notebook

`CSE516_M3_Results_Analysis.ipynb`

## Notebook Description

The notebook contains the implementation of:

1. Synthetic doubles tennis match data generation.
2. Baseline model using team match outcomes.
3. Extended model incorporating individual-level performance observations.
4. Player-skill estimation and evaluation.
5. Experiments using ten random seeds (42–51).
6. MAE, RMSE, log-loss and Brier score calculations.
7. Statistical significance testing and bootstrap confidence intervals.
8. Robustness experiments involving sample size, missing observations and observation noise.
9. Player-level error analysis.
10. Runtime, convergence and uncertainty evaluation.
11. Export of experimental results and dataset files.

## Execution

The notebook can be opened and executed using Google Colab or Jupyter Notebook.

Run the notebook cells in their intended order to generate the synthetic data, execute the experiments and obtain the corresponding results.

## Reproducibility

Fixed random seeds are used for the experiments. Using the same code, seeds and parameters should reproduce the same synthetic data and numerical results.

Runtime measurements may vary across environments.

## Dependencies

The notebook uses Python and its scientific computing libraries, including NumPy, Pandas, SciPy and Matplotlib.

Refer to the notebook for the implementation details and experimental configuration.
