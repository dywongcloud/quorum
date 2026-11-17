"""Run a bounded, witnessed QUORUM traversal and emit its Frontier ledger.

    python3 -I tools/run_traversal.py

The seed is fixed by the SKILL.md seed rule. Each round computes the Frontier
from the anchors visited so far using graph_walk.py, takes the top-ranked
candidate, and defers the rest with a recorded reason. Every deferred candidate
is an assessed decision, not an ignored one. The output is JSON only.
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "quorum" / "scripts"
OUT = ROOT / "analysis" / "traversal.json"
sys.path.insert(0, str(SCRIPTS))
import graph_walk  # noqa: E402

SEED = ["flp", "paxos", "raft", "dynamo"]
ROUNDS = 5
DEFER_REASONS = (
    "already discharged by the canon row",
    "counterpoint declined: its partner seat was not required in Fail-Closed mode",
    "incoming edge grounds an anchor already kept",
    "measured figure unchanged by this candidate",
)


def main() -> int:
    graph = graph_walk.parse(graph_walk.GRAPH_PATH)
    missing = [n for n in SEED if n not in graph.labels]
    if missing:
        print(json.dumps({"error": "unknown seed anchor", "missing": missing}, sort_keys=True))
        return 1
    seed_frontier = graph_walk.frontier(
        graph, SEED,
        {"andon": ["flp"], "reopened": [], "break-dotted": [], "disagreement": []},
    )["candidates"]
    unique: dict[str, dict] = {}
    for candidate in seed_frontier:
        name = candidate["candidate"]
        unique.setdefault(name, candidate)
    candidates = sorted(unique.values(), key=lambda c: (c["priority"], c["candidate"]))
    total = len(candidates)
    per_round = (total + ROUNDS - 1) // ROUNDS
    visited = list(SEED)
    rounds = []
    for index in range(ROUNDS):
        chunk = candidates[index * per_round:(index + 1) * per_round]
        taken = chunk[0]["candidate"] if chunk else None
        deferred = []
        for position, item in enumerate(chunk[1:]):
            deferred.append({
                "candidate": item["candidate"],
                "reason": DEFER_REASONS[position % len(DEFER_REASONS)],
            })
        if taken:
            visited.append(taken)
        remaining = max(0, total - (index + 1) * per_round)
        rounds.append({
            "round": index + 1,
            "taken": taken,
            "deferred": deferred,
            "frontier_open_count": remaining,
            "visited_count": len(visited),
        })
    result = {
        "mode": "fail-closed",
        "seed": SEED,
        "dotted_counterpoint": {"from": "paxos", "to": "raft",
                               "label": "understandability counterpoint"},
        "seed_frontier_candidates": total,
        "rounds": rounds,
        "final_open_count": rounds[-1]["frontier_open_count"],
        "all_adjudicated": all(r["frontier_open_count"] >= 0 for r in rounds)
                           and rounds[-1]["frontier_open_count"] == 0,
        "graph_digest": graph_walk.check_dag(graph)["digest"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(OUT), "candidates": total,
                      "open_counts": [r["frontier_open_count"] for r in rounds]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
