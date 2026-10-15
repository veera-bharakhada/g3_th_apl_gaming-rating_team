"""Coursework-inspired PGM diagnostics for the player-skill project.

Concepts adapted from the CSE516 L1-L2, L3-L4, L11-L12 and L13-L14 scribes:
- input validation/encoding and cautious correlation diagnostics;
- Bayesian-network parent/child and Markov-blanket queries;
- factorization listing;
- ancestral graph + moralization d-separation checks.

Important: this DAG is a generative dependency view for a small match history. It is
not the TTT factor graph used by the numerical smoother, and these diagnostics do not
replace inference or learn a new graph structure.
"""
from __future__ import annotations
from collections import deque
from itertools import combinations
import math


def validate_match_records(matches, n_players, n_times):
    """Validate the project's canonical {time,a,b,y_a} input and summarize labels."""
    required = {"time", "a", "b", "y_a"}
    errors = []
    seen = set()
    wins_a = 0
    for i, m in enumerate(matches):
        missing = required - set(m)
        if missing:
            errors.append(f"row {i}: missing fields {sorted(missing)}")
            continue
        t, a, b, y = m["time"], m["a"], m["b"], m["y_a"]
        if not isinstance(t, int) or not 0 <= t < n_times:
            errors.append(f"row {i}: time out of range")
        if not isinstance(a, int) or not isinstance(b, int) or a == b or not (0 <= a < n_players and 0 <= b < n_players):
            errors.append(f"row {i}: invalid player IDs")
        if y not in (0, 1):
            errors.append(f"row {i}: y_a must be binary 0/1")
        key = (t, min(a, b), max(a, b)) if isinstance(a, int) and isinstance(b, int) else None
        if key is not None and key in seen:
            errors.append(f"row {i}: duplicate unordered player pair in time step")
        if key is not None:
            seen.add(key)
        if y == 1:
            wins_a += 1
    return {
        "n_matches": len(matches),
        "n_players_declared": n_players,
        "n_time_steps_declared": n_times,
        "n_rows_with_errors": len(errors),
        "errors": errors,
        "player_a_win_fraction": wins_a / len(matches) if matches else math.nan,
        "outcome_encoding": "y_a=1 means player a won; y_a=0 means player b won",
    }


def build_match_dag(matches, n_players, n_times):
    """Build a small directed generative DAG for skill -> performance -> result."""
    parents = {}
    def node(name):
        parents.setdefault(name, set())
    def edge(source, target):
        node(source); node(target); parents[target].add(source)
    for t in range(n_times):
        for p in range(n_players):
            node(f"skill_{p}_{t}")
            if t + 1 < n_times:
                edge(f"skill_{p}_{t}", f"skill_{p}_{t+1}")
    for k, m in enumerate(matches):
        pa, pb, result = f"perf_a_{k}", f"perf_b_{k}", f"result_{k}"
        edge(f"skill_{m['a']}_{m['time']}", pa)
        edge(f"skill_{m['b']}_{m['time']}", pb)
        edge(pa, result); edge(pb, result)
    return parents


def children_map(parents):
    children = {n: set() for n in parents}
    for child, pars in parents.items():
        for p in pars:
            children.setdefault(p, set()).add(child)
    return children


def markov_blanket(node_name, parents):
    """Parents, children, and co-parents of the node's children."""
    children = children_map(parents)
    pars = set(parents.get(node_name, set()))
    ch = set(children.get(node_name, set()))
    co_parents = set()
    for child in ch:
        co_parents.update(parents.get(child, set()))
    return sorted((pars | ch | co_parents) - {node_name})


def factorization_terms(parents):
    """Return the BN factorization P(V)=product_v P(v | parents(v)) as readable terms."""
    return [f"P({v} | {', '.join(sorted(parents[v]))})" if parents[v]
            else f"P({v})" for v in sorted(parents)]


def _ancestors(nodes, parents):
    found = set(nodes); stack = list(nodes)
    while stack:
        n = stack.pop()
        for p in parents.get(n, set()):
            if p not in found:
                found.add(p); stack.append(p)
    return found


def d_separated(x, y, observed, parents):
    """D-separation test via ancestral restriction + moralization + evidence removal.

    This is a graph-only conditional-independence check (course L1-L2/L3-L4/L13-L14),
    not a numerical probability calculation.
    """
    X, Y, Z = set(x if isinstance(x, (list, tuple, set)) else [x]), set(y if isinstance(y, (list, tuple, set)) else [y]), set(observed)
    if (X | Y | Z) - set(parents):
        raise ValueError("Every queried/observed node must exist in the graph")
    relevant = _ancestors(X | Y | Z, parents)
    undirected = {n: set() for n in relevant}
    for child in relevant:
        pars = set(parents.get(child, set())) & relevant
        for p in pars:
            undirected[p].add(child); undirected[child].add(p)
        for p1, p2 in combinations(pars, 2):
            undirected[p1].add(p2); undirected[p2].add(p1)
    blocked = Z
    starts = [n for n in X if n not in blocked]
    targets = Y - blocked
    queue = deque(starts); seen = set(starts)
    while queue:
        n = queue.popleft()
        if n in targets:
            return False
        for nxt in undirected[n]:
            if nxt not in blocked and nxt not in seen:
                seen.add(nxt); queue.append(nxt)
    return True


def run_coursework_diagnostics(matches, n_players, n_times):
    """Return reproducible structural diagnostics on the first observed match."""
    audit = validate_match_records(matches, n_players, n_times)
    if not matches:
        return {"input_audit": audit, "graph": {"nodes": 0, "edges": 0}}
    parents = build_match_dag(matches, n_players, n_times)
    m = matches[0]
    perf_a, perf_b, result = "perf_a_0", "perf_b_0", "result_0"
    skill_a, skill_b = f"skill_{m['a']}_{m['time']}", f"skill_{m['b']}_{m['time']}"
    children = children_map(parents)
    edges = sum(len(v) for v in parents.values())
    return {
        "input_audit": audit,
        "graph": {"nodes": len(parents), "directed_edges": edges,
                 "factorization_term_count": len(parents)},
        "example_match": {"skill_a": skill_a, "skill_b": skill_b,
                          "performance_a": perf_a, "performance_b": perf_b,
                          "result": result},
        "markov_blanket_skill_a": markov_blanket(skill_a, parents),
        "d_separation_checks": {
            "skill_a_independent_of_skill_b_before_observing_result": d_separated(skill_a, skill_b, set(), parents),
            "skill_a_independent_of_skill_b_after_observing_result": d_separated(skill_a, skill_b, {result}, parents),
            "skill_a_independent_of_result_given_both_performances": d_separated(skill_a, result, {perf_a, perf_b}, parents),
        },
        "factorization_example_first_8": factorization_terms(parents)[:8],
        "interpretation": "Result is a common effect of the two performances: observing it can connect the players' skill variables (explaining away). Conditioning on both performances blocks the path to that match result.",
    }

if __name__ == "__main__":
    import argparse, json, os
    from skill_models import generate_synthetic
    parser = argparse.ArgumentParser(description="Run coursework-inspired graph diagnostics")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="../../Results/graph_diagnostics.json")
    args = parser.parse_args()
    _, sample_matches = generate_synthetic(seed=args.seed)
    diagnostics = run_coursework_diagnostics(sample_matches[:8], 8, 30)
    output = os.path.abspath(os.path.join(os.path.dirname(__file__), args.out))
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w") as handle:
        json.dump(diagnostics, handle, indent=2)
    print(json.dumps(diagnostics, indent=2))
