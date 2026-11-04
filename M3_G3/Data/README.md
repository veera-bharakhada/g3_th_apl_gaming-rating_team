# Data – Synthetic Doubles Tennis Dataset

## Dataset Description

**File:** `synthetic_doubles_data.csv`

This dataset contains 360 synthetically generated doubles tennis matches used for the M3 experimental evaluation.

It contains the following columns:

| Column | Description |
|---|---|
| `time` | Match time point |
| `a1`, `a2` | Player IDs in Team A |
| `b1`, `b2` | Player IDs in Team B |
| `a_wins` | Team A match outcome |
| `perf_a1`, `perf_a2` | Simulated individual performance observations for Team A |
| `perf_b1`, `perf_b2` | Simulated individual performance observations for Team B |

## Data Generation

The dataset was generated programmatically using a fixed random seed (42), with the default experimental configuration.

The data is synthetic and was created to provide controlled individual-level performance observations for evaluating the proposed extension.

## Usage

The dataset is used for the baseline and extended Bayesian player-skill estimation experiments.

It is intended to support reproducibility and demonstrate the input format used in the experiments.

## Important Note

This dataset does not contain actual ATP match statistics or real player-performance records. The individual-level observations are simulated and should not be interpreted as real-world tennis statistics.

The notebook contains the data-generation procedure.
