# CSE 516 Major Project — Group 3 | Milestone 4 (Final Submission)

**Title:** Individual-Level Evidence for Temporal Bayesian Player-Skill Estimation: A Controlled Ablation  
**Team:** Dhruvi Shah, Divija Nayak, Veera Bharakhada  
**Course:** CSE 516 — Probabilistic Graphical Models

## Project overview

A doubles match result provides evidence about a team's combined strength but cannot always distinguish individual teammates' abilities. We compare two **simplified temporal Bayesian skill models** under identical synthetic experimental conditions:

- **Team-only baseline:** Gaussian random-walk latent player skills with logistic doubles-match outcome observations.
- **Individual-evidence extension:** the same model plus noisy Gaussian observations of each participating player's skill.

Both conditions use maximum a posteriori (MAP) estimation with SciPy L-BFGS-B and a Laplace approximation for local posterior uncertainty. This is an **internal evidence ablation**, not a reproduction of or empirical benchmark against published TrueSkill Through Time (TTT).

## Milestone progression

- **M1:** initial proposal and investigation of temporal skill models and inference methods.
- **M2:** temporal-PGM foundation; individual-evidence extension demonstrated in a separate notebook with preliminary single-seed results.
- **M3:** controlled ten-seed evaluation, chronological holdout, robustness sweeps and statistical analysis.
- **M4:** final conference-style report, statistical synthesis, presentation, technical artifacts and reproducibility documentation.

## Main experimental setup

- 12 players, 30 time points, 12 doubles matches per time point (360 matches per seed).
- Chronological training times **0–20** (252 matches) and test times **21–29** (108 matches).
- Paired random seeds **42–51**; each model sees the same synthetic match schedule and outcomes within a seed.
- Initial-skill SD 1.0; random-walk drift SD 0.12; logistic temperature 0.8; individual-observation SD 0.65.
- Only training-period observations are used for fitting. Test-period skill estimates are prior-based forward extrapolations, not smoothing with test evidence.

## Main results (10 paired seeds; mean ± sample SD)

| Held-out KPI | Team-only baseline | Individual-evidence extension |
|---|---:|---:|
| Skill MAE | 0.4372 ± 0.1400 | 0.2632 ± 0.0366 |
| Skill RMSE | 0.5357 ± 0.1586 | 0.3284 ± 0.0395 |
| Match log-loss / Bernoulli NLL | 0.5835 ± 0.0568 | 0.5601 ± 0.0655 |
| Brier score | 0.1999 ± 0.0242 | 0.1893 ± 0.0269 |

Mean paired skill-MAE reduction: **0.1740** (~39.8% relative to the baseline mean), paired t-test **p ≈ 0.0055**, improvement in **10/10** seeds. The study also evaluates match-count, observation-missingness and observation-noise robustness. Reduced approximate posterior SD is not, by itself, evidence of improved calibration.

## Repository layout

```text
M4_G3/
├── README.md
├── Report/
│   └── M4_G3_Report.pdf
├── Video/
│   └── M4_G3_Video.md
├── Presentation/
│   └── M4_G3_Slides.pdf
├── Code/
│   ├── README.md
│   ├── requirements.txt
│   ├── verify_results.py
│   └── src/
│       ├── CSE516_M2_Limitation_and_Solution.ipynb
│       └── CSE516_M3_Results_Analysis.ipynb
├── Data/
│   ├── README.md
│   └── synthetic_doubles_data.csv
└── Results/
    ├── README.md
    ├── main_10_seed_results.csv
    ├── main_summary_mean_sd.csv
    ├── paired_mae_test.json
    ├── *_robustness.csv
    ├── player_error_analysis_seed42.csv
    └── *.png
```

The above is the **intended final structure**. Check that the PDF, video link and other required files have actually been added before submission.

## Quick-start verification

Run from the `M4_G3/` directory:

```bash
python -m pip install -r Code/requirements.txt
python Code/verify_results.py
```

The verification script checks archived results; **it does not rerun the experiments**. See [Code/README.md](Code/README.md) for notebook execution, output paths and Colab caveats. See [Data/README.md](Data/README.md) for dataset provenance and [Results/README.md](Results/README.md) for result files.

## SOTA positioning and limitations

The research anchor is the published TrueSkill Through Time work by Landfried and Mocskos (Journal of Statistical Software, 2025). Our model borrows the temporal latent-skill idea but uses a simplified logistic likelihood, MAP fitting and Laplace uncertainty rather than the full published TTT inference system. No head-to-head SOTA experiment was conducted. Data are synthetic, individual observations are informative by construction, hyperparameters are fixed, and real-world generalization is untested. The next step is evaluation with meaningful real individual-level doubles statistics and a published-TTT comparison on identical data.

## Submission components

- `Report/M4_G3_Report.pdf` — final paper.
- `Presentation/M4_G3_Slides.pdf` — final presentation.
- `Video/M4_G3_Video.md` — video explanation.
- `Code/`, `Data/`, `Results/` — complete technical package.
- **Individual Google Form** — completed separately by each group member; not stored in this repository.

Verify that the linked video is accessible to the evaluators.
