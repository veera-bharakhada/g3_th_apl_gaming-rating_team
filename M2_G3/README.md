# Group 3 — CSE516 M2

## Project
**Bayesian Network-Based Estimation of Player Skill Over Time**

## M2 focus
1. Define the temporal Bayesian network and factorization.
2. Implement and test a restricted TTT-style inference prototype.
3. Report a small set of initial KPIs from reproducible synthetic experiments.
4. Describe active-trail pruning as a research direction for a later milestone.

## Main files
- `Report/M2_Group3_Report.pdf` — revised report focused on the agreed M2 scope.
- `Code/src/` — prototype, parameter tuning, graph diagnostics, extension pilot, and tests.
- `Results/` — KPI summaries, per-run results, logs, diagnostics, and plots.
- `M2_Group3_Colab_Demo.ipynb` — notebook used to run the project.
- `Report/ACTIVE_TRAIL_LIMITATION_NOTE.md` — research gap and validation plan.
- `Video/M2_Group3_Video_Script.txt` — walkthrough script.
- `Code/requirements.txt` — Python dependencies required to run the project.

## Initial Synthetic KPIs

- Skill-recovery MAE: 0.3179 ± 0.0406.
- EP convergence: 10/10 runs.
- Average EP iterations: 16.7.
- Best validation log-loss: 0.5640 on 60 validation matches.

These preliminary results were obtained from synthetic experiments using the restricted TTT-style prototype. They provide an initial assessment of skill estimation and inference behaviour.

## Run in Colab
Open `M2_Group3_Colab_Demo.ipynb`, upload/extract the project ZIP when prompted, then run the notebook cells in order. Save the executed notebook and the generated result archive.


## Scientific boundary
Active-trail pruning has not been validated. An off-season is not automatically a separator; posterior preservation and computational savings must be tested before making such claims.
