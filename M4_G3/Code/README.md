# Code — Model, inference and experimental evaluation

## Files

| File | Role |
|---|---|
| `src/CSE516_M2_Limitation_and_Solution.ipynb` | Original M2 individual-evidence extension and preliminary single-seed demonstration. |
| `src/CSE516_M3_Results_Analysis.ipynb` | Canonical ten-seed evaluation, baseline/extension comparison, robustness, plots and diagnostic analysis. |
| `requirements.txt` | Python package dependencies. |
| `verify_results.py` | Checks archived per-seed result CSVs and the paired-MAE summary; does not regenerate experiments. |

**Do not interpret M2 single-seed metrics as M3 ten-seed averages.** The final report's numerical comparisons come from the archived M3 results.

## Environment

Python 3 with `numpy`, `pandas`, `scipy`, `matplotlib`, `jupyter` and `notebook`. The unpinned `requirements.txt` specifies package names, **not** the exact versions used for the archived runs. For strict reproducibility, record the tested Python and package versions from the actual experiment environment; runtime values can change with hardware and library versions.

From `M4_G3/`:

```bash
python -m pip install -r Code/requirements.txt
python Code/verify_results.py
```

To capture the current environment (not necessarily the original experiment environment):

```bash
python --version
python -m pip freeze > environment-lock.txt
```

## Experiment settings

- Seeds: `42, 43, ..., 51` (NumPy `default_rng(seed)`); bootstrap seed: `2026`.
- Players: `P=12`; time points: `T=30`; matches/time: `M=12`.
- Prior SD: `sigma0=1`; drift SD: `sigma_d=0.12`; team logistic temperature: `tau=0.8`; individual-observation SD: `sigma_z=0.65`.
- Training: time points `0..20`; held-out testing: `21..29`.
- MAP optimiser: SciPy L-BFGS-B, `maxiter=500`, `ftol=1e-9`; Laplace Hessian jitter `1e-8`.
- Robustness sweeps: matches/time `{6,12,24}`, missing observations `{0,0.25,0.5,0.75}`, observation SD `{0.25,0.65,1.0,1.5}`.

## How to regenerate results

Open `src/CSE516_M3_Results_Analysis.ipynb` in Jupyter or Google Colab and execute its experiment cells in order. **The notebook contains Google Colab-specific `google.colab` download cells**, which will not run in ordinary local Jupyter without being skipped or adapted. It also writes experimental CSV files into a relative `M3_Results/` directory, rather than automatically overwriting `M4_G3/Results/`.

For local Jupyter, start from a deliberate working directory, e.g. `M4_G3/`:

```bash
jupyter notebook Code/src/CSE516_M3_Results_Analysis.ipynb
```

Execute the model, simulation, evaluation and plotting cells; skip Colab-only `files.download` / `google.colab` cells in local Jupyter. Check where the notebook actually saved `M3_Results/` and the plot files relative to the notebook kernel's working directory. Compare regenerated CSVs against the archived files in `Results/` **before replacing any archived outputs**. Some plots may be saved in separate relative locations or downloaded through Colab; inspect those cells before rerunning.

**Important:** This is an execution guide, not a claim that the notebook has been fully rerun in a fresh environment. A complete end-to-end reproducibility test should be performed before asserting that every output can be recreated with one command.

## Verification vs regeneration

`verify_results.py` reads `Results/main_10_seed_results.csv` and `Results/paired_mae_test.json`, checks seeds and summary statistics and reports the archived paired result. It is not a substitute for the notebook's generation of data, robustness experiments and plots. If you use the corrected version provided separately, it locates `M4_G3/Results/` from either `Code/` or `Code/src/`.

## Model and inference summary

The team-only model has latent Gaussian random-walk skill states and logistic likelihoods for observed doubles outcomes. The extension adds Gaussian player-specific observation factors. MAP optimisation fits the latent skill trajectory; the Laplace approximation estimates local posterior covariance from the Hessian. Hyperparameters and graphical structure are fixed, not learned. Predictions for held-out times do not condition on test outcomes or individual test observations.
