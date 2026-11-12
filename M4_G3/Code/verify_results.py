"""Verify the archived M4 Group 3 results without rerunning experiments.

Run from any working directory:
    python M4_G3/Code/src/verify_results.py
or, if placed in Code/:
    python M4_G3/Code/verify_results.py
"""
from pathlib import Path
import csv
import json
import math
import statistics


def find_project_root(script_path: Path) -> Path:
    for directory in (script_path.parent, *script_path.parents):
        if (directory / "Results" / "main_10_seed_results.csv").is_file() and (
            directory / "Results" / "paired_mae_test.json"
        ).is_file():
            return directory
    raise FileNotFoundError(
        "Could not find M4_G3/Results/main_10_seed_results.csv and "
        "M4_G3/Results/paired_mae_test.json. Keep the original Results folder "
        "inside M4_G3."
    )


root = find_project_root(Path(__file__).resolve())
results = root / "Results"
with (results / "main_10_seed_results.csv").open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))

expected_seeds = set(range(42, 52))
assert len(rows) == 20, f"Expected 20 rows, found {len(rows)}"
assert {int(row["seed"]) for row in rows} == expected_seeds, "Unexpected seeds"
assert {(int(row["seed"]), row["model"]) for row in rows} == {
    (seed, model) for seed in expected_seeds for model in ("baseline", "extension")
}, "Expected one baseline and one extension row per seed"

print(f"M4 project root: {root}")
print("Archived results: 10 paired seeds (42–51), 20 model rows\n")
for metric in ("MAE", "RMSE", "logloss", "brier"):
    for model in ("baseline", "extension"):
        values = [float(row[metric]) for row in rows if row["model"] == model]
        assert all(math.isfinite(value) for value in values), f"Invalid {metric} values"
        print(f"{metric:9} {model:9} {statistics.mean(values):.4f} ± {statistics.stdev(values):.4f}")

paired_differences = []
for seed in sorted(expected_seeds):
    baseline = next(row for row in rows if int(row["seed"]) == seed and row["model"] == "baseline")
    extension = next(row for row in rows if int(row["seed"]) == seed and row["model"] == "extension")
    paired_differences.append(float(baseline["MAE"]) - float(extension["MAE"]))

with (results / "paired_mae_test.json").open(encoding="utf-8") as handle:
    paired = json.load(handle)
computed_reduction = statistics.mean(paired_differences)
archived_reduction = float(paired["mean_baseline_minus_extension_mae"])
assert math.isclose(computed_reduction, archived_reduction, rel_tol=1e-9, abs_tol=1e-12), (
    "Archived paired MAE reduction does not match the CSV"
)
print(f"\nPaired MAE reduction: {computed_reduction:.6f}")
print(f"Archived paired t-test p-value: {float(paired['p_value']):.6f}")
print(f"Archived bootstrap 95% CI: {paired['bootstrap_95_ci']}")
print(f"Seeds improving MAE: {sum(delta > 0 for delta in paired_differences)}/10")
print("PASS: archived CSV structure, KPI summaries, and paired MAE reduction verified.")
print("Note: this checks archived outputs; it does not rerun the model or independently recompute the p-value/bootstrap.")
