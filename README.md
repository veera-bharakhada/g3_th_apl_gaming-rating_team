# Bayesian Network-Based Estimation and Comparison of Player Skill Over Time

**CSE 516 — Probabilistic Graphical Models | Group 3 | Category: Theoretical AI**

## Overview

This project studies **TrueSkill Through Time (TTT)** — a Dynamic Bayesian Network model
for estimating player skill from match outcomes, which allows information to flow both
forward and backward through time (unlike Elo and the original TrueSkill, which only
filter forward). We reimplement the model from scratch, clearly separating its three PGM
verticals — **Representation, Learning, and Inference** — and benchmark it against
baselines and relevant SOTA work.

**Mathematical question:** How much does bidirectional information flow actually improve
skill estimates over forward-only filtering, and what is the computational cost of that
improvement?

## Base Paper

G. Landfried and E. Mocskos, *"TrueSkill Through Time: Reliable Initial Skill Estimates
and Historical Comparability with Julia, Python, and R,"* Journal of Statistical Software,
vol. 112, no. 6, pp. 1–41, Mar. 2025. doi: 10.18637/jss.v112.i06
→ see [`BasePaper/`](./BasePaper)

## SOTA Anchors

- R. Herbrich, T. Minka, T. Graepel, *"TrueSkill(TM): A Bayesian Skill Rating System,"*
  NIPS 2006 — the original forward-only filtering baseline (Microsoft Research).
- M. Jones, P. Chang, K. Murphy, *"Bayesian Online Natural Gradient (BONG),"* NeurIPS 2024
  (Google DeepMind) — a contemporary approximate online Bayesian inference method,
  used for written SOTA comparison/discussion in the final report.

## Repository Structure

| Folder | Purpose |
|---|---|
| [`BasePaper/`](./BasePaper) | Base paper PDF |
| [`Data/`](./Data) | ATP tennis match dataset, download scripts, synthetic dataset generator |
| [`Derivation/`](./Derivation) | Written math: Bayesian network factorization, message-passing derivations, parameter learning |
| [`Code/`](./Code) | Implementation: `representation/`, `learning/`, `inference/`, `baselines/`, `utils/` |
| [`Experiment/`](./Experiment) | Configs, random seeds, and run scripts for reproducible experiments |
| [`Results/`](./Results) | Output tables, plots, robustness/significance-test results, logs |
| [`M1/`](./M1) | Milestone 1 project proposal |

## Dataset

ATP (Association of Tennis Professionals) match history: ~447,000 singles/doubles
matches, 1915–2020, 19,000+ players. See [`Data/README.md`](./Data/README.md) for full
details and links.

## Team

- Dhruvi Shah
- Veera Bharakhada
- Divija Nayak
  
*(All members contribute to experiments, analysis, and the final report.)*

## Status

- **M1 (current):** Proposal submitted, base paper studied, dataset identified,
  repository structure set up.
- **M2:** Bayesian network + factor graph implementation, exact inference, baselines.
- **M3:** Loopy BP, expectation propagation, hyperparameter learning, initial experiments.
- **M4:** Full statistical analysis, robustness studies, final SOTA positioning.

## Setup

See [`Code/README.md`](./Code/README.md) for installation and run instructions
(updated as implementation progresses).
