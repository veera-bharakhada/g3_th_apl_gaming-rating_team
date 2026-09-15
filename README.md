# Bayesian Network-Based Estimation and Comparison of Player Skill Over Time

**CSE 516 — Probabilistic Graphical Models | Group 3 | Category: Theoretical AI**

## Overview

This project studies how the choice of inference method affects Bayesian estimates
of time-varying player skill, using **TrueSkill Through Time (TTT)** — a Dynamic
Bayesian Network model that lets information flow both forward and backward through
time — as the core probabilistic model and methodological focus.

**Mathematical question:** How much does bidirectional information flow through a
temporal Bayesian network improve skill estimates over forward-only filtering, and
what computational cost do the inference methods that enable this introduce?

We study this through the full PGM pipeline:
- **Representation** — a Dynamic Bayesian Network / factor graph over skill,
  performance, and match outcome
- **Inference** — exact belief propagation, loopy belief propagation, and
  expectation propagation
- **Learning** — parameter (not structure) learning via evidence maximization

## Base Paper

G. Landfried and E. Mocskos, *"TrueSkill Through Time: Reliable Initial Skill
Estimates and Historical Comparability with Julia, Python, and R,"* Journal of
Statistical Software, vol. 112, no. 6, pp. 1–41, Mar. 2025.
doi: [10.18637/jss.v112.i06](https://doi.org/10.18637/jss.v112.i06)
→ see [`BasePaper/`](./BasePaper)

## Baseline & SOTA Reference

- **Baseline:** R. Herbrich, T. Minka, T. Graepel, *"TrueSkill(TM): A Bayesian
  Skill Rating System,"* NIPS 2006 (Microsoft Research) — the original,
  forward-only filtering system that TTT generalizes.
- **SOTA reference:** M. Jones, P. Chang, K. Murphy, *"Bayesian Online Natural
  Gradient (BONG),"* NeurIPS 2024 (Kevin Murphy — Google DeepMind) — a recent,
  methodologically related approach to sequential Bayesian inference, used as
  our comparison axis for message-passing smoothing vs. single-step online
  optimization.

## Repository Structure

| Folder | Purpose |
|---|---|
| [`M1_G3/`](./M1_G3) | Milestone 1 submission: report, video link |
| [`BasePaper/`](./BasePaper) | Base paper PDF |
| [`Data/`](./Data) | ATP tennis match dataset, download scripts, synthetic dataset generator |

## Dataset

**Primary:** ATP (Association of Tennis Professionals) match history — ~447,000
singles/doubles matches, 1915–2020, 19,000+ players.
Source: https://github.com/glandfried/tennis_atp/releases/download/atp/history.csv.zip

**Validation:** A small synthetic dataset with a known ground-truth skill
trajectory, used to verify inference correctness before drawing conclusions from
real data.

See [`Data/README.md`](./Data/README.md) for full details.

## Team

- Dhruvi Shah
- Divija Nayak
- Veera Bharakhada

*Understanding of the full Representation–Inference–Learning pipeline is a shared
responsibility across the team; specific workstream ownership will be finalized
at the start of M2.*

## Status

- **M1 (current):** Proposal & scoping complete — problem statement, R/I/L
  mapping, baseline, SOTA position, dataset, initial KPIs, experimental plan,
  and timeline. See [`M1_G3/`](./M1_G3).
- **M2 (11 Oct 2026):** Bayesian network / factor graph implementation, exact
  belief propagation, Elo and TrueSkill baselines.
- **M3 (1 Nov 2026):** Loopy belief propagation, expectation propagation,
  hyperparameter learning, initial experiments and KPIs.
- **M4 (22 Nov 2026):** Full statistical analysis, robustness studies, final
  SOTA comparison, reproducibility package.

## Setup

See [`Code/README.md`](./Code/README.md) for installation and run instructions
(updated as implementation progresses).
