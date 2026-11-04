# CSE516 Major Project – M3: Results and Analysis

## Project Overview

This project investigates Bayesian player-skill estimation over time using tennis match outcomes. It evaluates whether incorporating individual-level performance observations alongside team match outcomes improves the estimation of individual player skills.

The project compares two approaches:

- **Baseline Model:** Uses team match outcomes only.
- **Extended Model:** Uses team match outcomes along with individual-level performance observations.

The experiments use synthetically generated doubles tennis match data because the available ATP history dataset does not contain the individual-level statistics required for this extension.

## Project Structure

- `Report/` – Final M3 Results and Analysis report.
- `Code/` – Jupyter Notebook containing the implementation and experiments.
- `Data/` – Synthetic doubles tennis dataset used in the experiments.
- `Results/` – Experimental results, statistical analysis and robustness evaluation outputs.

## Experimental Evaluation

The evaluation includes:

- Comparison of baseline and extended models.
- Skill estimation accuracy using MAE and RMSE.
- Predictive performance using log-loss and Brier score.
- Experiments across ten random seeds (42–51).
- Statistical significance testing and bootstrap confidence intervals.
- Robustness analysis involving sample size, missing observations and observation noise.
- Player-level error analysis.
- Runtime, convergence and uncertainty analysis.

## Reproducibility

The experiments use fixed random seeds to ensure reproducibility. Running the notebook with the same code and parameters should reproduce the synthetic datasets and corresponding experimental results.

Runtime measurements may vary depending on the execution environment.

## Important Note

The dataset is synthetic and does not represent actual ATP match statistics. The implemented model is a simplified temporal Bayesian proof-of-concept inspired by TrueSkill Through Time and is not a complete implementation of the original TTT algorithm.

For further details, refer to the M3 report.
