# Data — Synthetic doubles-match observations

## File and provenance

`synthetic_doubles_data.csv` is a **360-match, seed-42 example dataset** generated for the simplified doubles skill-estimation experiments. It is not the combined dataset for all ten seeds. The M3 notebook regenerates separate synthetic match histories for seeds **42–51** during evaluation.

There are **no real ATP individual-performance measurements** in this dataset. Individual observations are simulated directly from latent skill plus Gaussian noise; this is a favorable proof-of-concept setting.

## Schema

| Column | Description |
|---|---|
| `time` | Time index of the match (0–29). |
| `a1`, `a2` | Two player IDs on team A. |
| `b1`, `b2` | Two player IDs on team B. |
| `a_wins` | Binary outcome, 1 if team A wins and 0 otherwise. |
| `perf_a1`, `perf_a2` | Synthetic individual performance observations for team A. |
| `perf_b1`, `perf_b2` | Synthetic individual performance observations for team B. |

## Generator and split

- 12 players, 30 time points, 12 matches per time point.
- Latent skills start with SD 1 and evolve by Gaussian random-walk increments of SD 0.12.
- Team A's win probability is the logistic function of the difference between team-average skills divided by temperature 0.8.
- Each participating player's individual observation equals their latent skill plus independent Gaussian noise with SD 0.65.
- Training times: 0–20; test times: 21–29. **No test outcomes or test individual observations enter model fitting.**
- Main experiment uses paired seeds 42–51; the CSV in this directory is only an illustrative seed-42 file.

## Reproduction

See `../Code/src/CSE516_M3_Results_Analysis.ipynb` for the generator and complete ten-seed experiments. See `../Code/README.md` for execution instructions, output directories and Google Colab-specific cells. Regenerating a CSV using the same seed also depends on running the same generator implementation and compatible numerical-library versions.

## Limitations

This dataset is synthetic and should not be interpreted as a real tennis dataset, nor as evidence that the same gains will transfer to actual players. The observation model assumes player-specific information that is directly informative about latent skill.
