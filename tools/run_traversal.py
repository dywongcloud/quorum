"""Run a witnessed, non-linear QUORUM traversal and emit its Frontier ledger.

    python3 -I tools/run_traversal.py

The round count is derived from the live graph, not fixed in advance. Each
round recomputes the Frontier from the anchors visited so far, takes the
highest-priority unvisited candidate, and defers the others with a reason
derived from that candidate's own edge direction, kind, priority and From
anchor. The final OPEN count is measured from the recomputed Frontier. The
generated rows are spliced into QUORUM-LOG.md between the FRONTIER markers.
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "quorum" / "scripts"
OUT = ROOT / "analysis" / "traversal.json"
LOG = ROOT / "QUORUM-LOG.md"
START = "<!-- FRONTIER:START -->"
END = "<!-- FRONTIER:END -->"
sys.path.insert(0, str(SCRIPTS))
import graph_walk  # noqa: E402

SEED = ["flp", "paxos", "raft", "dynamo"]


def reason(item: dict[str, str]) -> str:
    """A deferral reason derived from the candidate's own measured fields."""
    return (f"{item['direction']} {item['kind']} edge via '{item['via']}' from "
            f"`{item['from']}`; priority {item['priority']}; assessed, not taken this round")


def priority_key(item: dict[str, str]) -> tuple[int, int, str, str]:
    kind_order = 0 if item["kind"] == "dotted" else 1
    return (graph_walk.PRIORITY.index(item["priority"]), kind_order,
            item["candidate"], item["from"])


def main() -> int:
    graph = graph_walk.parse(graph_walk.GRAPH_PATH)
    missing = [n for n in SEED if n not in graph.labels]
    if missing:
        print(json.dumps({"error": "unknown seed anchor", "missing": missing}, sort_keys=True))
        return 1
    flags = {"andon": ["flp"], "reopened": [], "break-dotted": [], "disagreement": []}
    initial = graph_walk.frontier(graph, SEED, flags)["candidates"]
    seed_frontier_candidates = len(initial)
    known = {item["candidate"] for item in initial}
    visited = list(SEED)
    rounds = []
    guard = len(graph.labels) + 1
    while guard > 0:
        guard -= 1
        live = graph_walk.frontier(graph, visited, flags)["candidates"]
        open_items = [item for item in live if item["candidate"] in known
                      and item["candidate"] not in visited]
        by_candidate: dict[str, dict[str, str]] = {}
        for item in open_items:
            by_candidate.setdefault(item["candidate"], item)
        ranked = sorted(by_candidate.values(), key=priority_key)
        if not ranked:
            break
        taken = ranked[0]
        visited.append(taken["candidate"])
        remaining = [item for item in ranked[1:]]
        rounds.append({
            "round": len(rounds) + 1,
            "taken": taken["candidate"],
            "taken_from": taken["from"],
            "taken_via": taken["via"],
            "taken_priority": taken["priority"],
            "deferred": [{"candidate": item["candidate"], "from": item["from"],
                          "reason": reason(item)} for item in remaining],
            "frontier_open_count": len(remaining),
            "visited_count": len(visited),
        })
    final_open = rounds[-1]["frontier_open_count"] if rounds else 0
    result = {
        "mode": "fail-closed",
        "seed": SEED,
        "dotted_counterpoint": {"from": "paxos", "to": "raft",
                               "label": "understandability counterpoint"},
        "seed_frontier_candidates": seed_frontier_candidates,
        "distinct_seed_candidates": len(known),
        "rounds": rounds,
        "round_count": len(rounds),
        "final_open_count": final_open,
        "all_adjudicated": final_open == 0 and bool(rounds),
        "graph_digest": graph_walk.check_dag(graph)["digest"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = ["| Round | TAKEN | Reached via | From anchor | DEFERRED (derived reason) | Frontier OPEN count |",
             "|---|---|---|---|---|---|"]
    for row in rounds:
        deferred = "; ".join(f"`{d['candidate']}`: {d['reason']}" for d in row["deferred"][:3]) or "none"
        lines.append(f"| R{row['round']} | `{row['taken']}` | {row['taken_via']} | "
                     f"`{row['taken_from']}` | {deferred} | Frontier OPEN count: "
                     f"{row['frontier_open_count']} |")
    log = LOG.read_text(encoding="utf-8")
    if START in log and END in log:
        head, rest = log.split(START, 1)
        _, tail = rest.split(END, 1)
        log = head + START + "\n" + "\n".join(lines) + "\n" + END + tail
        LOG.write_text(log, encoding="utf-8")
    print(json.dumps({"wrote": str(OUT), "seed_frontier_candidates": seed_frontier_candidates,
                      "round_count": len(rounds),
                      "open_counts": [r["frontier_open_count"] for r in rounds]},
                     sort_keys=True))
    return 0 if result["all_adjudicated"] else 1


if __name__ == "__main__":
    sys.exit(main())
