# Code

This folder contains the source code for the CSE516 M2 project on Bayesian estimation of player skill over time.

## Contents

- `src/` — prototype implementation, parameter-tuning scripts, experiment runner, graph/data diagnostics, and automated tests.
- `requirements.txt` — Python dependencies required by the source code.

## Environment

- Python 3.x
- Dependencies listed in `requirements.txt`

## Installation

Run from this `Code/` directory:

```bash
python -m pip install -r requirements.txt
```

## Run experiments

Run these commands from this `Code/` directory:

```bash
python src/run_experiments.py --runs 10 --seed 42
python src/parameter_learning.py --seed 42
python -m unittest discover -s src -p "test_*.py" -v
```

The benchmark uses 10 runs with seeds 42–51. The parameter-learning experiment uses seed 42.

## Outputs

The scripts generate experiment summaries, diagnostics, and plots. The project-level `Results/` directory contains the recorded outputs included with the submission.

## Notes

The current source includes a restricted TTT-style inference prototype and supporting experiment utilities. Refer to the main project `README.md` for the overall project scope and reported synthetic KPIs.
