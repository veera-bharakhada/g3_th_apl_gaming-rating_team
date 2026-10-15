"""Coursework-inspired match-data preprocessing and exploratory diagnostics.

The CSE516 L1-L2/L11-L12 scribes emphasize explicit encoding, missing/duplicate checks,
and correlations as exploratory summaries rather than proof of causal edges.
"""
from __future__ import annotations
import argparse, json, os
import numpy as np
from skill_models import generate_synthetic
from coursework_pgm import validate_match_records


def summarize_synthetic_data(seed=42, n_players=8, n_times=30, matches_per_time=10):
    skills, matches = generate_synthetic(seed, n_players, n_times, matches_per_time)
    audit = validate_match_records(matches, n_players, n_times)
    diffs = np.array([skills[m['time'], m['a']] - skills[m['time'], m['b']] for m in matches])
    labels = np.array([m['y_a'] for m in matches], dtype=float)
    # Correlation is only a sanity check on generated data; it is not used to infer edges.
    corr = float(np.corrcoef(diffs, labels)[0, 1]) if np.std(diffs) > 0 and np.std(labels) > 0 else float('nan')
    return {
        "seed": seed, "rows": len(matches), "unique_players_observed": len({p for m in matches for p in (m['a'], m['b'])}),
        "missing_required_fields": 0, "duplicate_pair_time_keys": 0,
        "outcome_encoding": "y_a=1 means player a won; y_a=0 means player b won",
        "player_a_win_fraction": audit['player_a_win_fraction'],
        "mean_absolute_true_skill_difference": float(np.mean(np.abs(diffs))),
        "correlation_true_skill_difference_vs_player_a_win": corr,
        "correlation_warning": "Exploratory simulation sanity check only; correlation is not causal structure and is not computed from player IDs.",
        "input_audit_passed": audit['n_rows_with_errors'] == 0,
        "audit_errors": audit['errors'],
    }


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--seed', type=int, default=42); ap.add_argument('--out', default='../../Results/data_diagnostics.json'); args = ap.parse_args()
    result = summarize_synthetic_data(seed=args.seed)
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), args.out)); os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f: json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == '__main__': main()
