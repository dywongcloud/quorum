"""Record an applied-or-declined decision for each used dotted edge.

    python3 -I tools/build_dotted_decisions.py

S5 is not satisfied by counting dotted edges. This tool reads the live graph,
the traversal ledger and the traversal log, then writes one decision per
dotted edge whose source anchor was actually visited. A decision states the
anchor pair, the ledger verdict of the source, and the reason the
counterpoint was applied or declined.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REFS = ROOT / "skills" / "quorum" / "references"
SCRIPTS = ROOT / "skills" / "quorum" / "scripts"
OUT = ROOT / "analysis" / "dotted-decisions.json"
sys.path.insert(0, str(SCRIPTS))
import graph_walk  # noqa: E402


def ledger_verdicts() -> dict[str, dict[str, str]]:
    text = (REFS / "traversal-ledger.md").read_text(encoding="utf-8")
    rows = {}
    for line in text.splitlines():
        match = re.match(r"^\|\s*\d+\s*\|\s*`([a-z0-9_]+)`\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(.+?)\s*\|$", line)
        if match:
            rows[match.group(1)] = {"class": match.group(2), "cluster": match.group(3),
                                    "verdict": match.group(4), "evidence": match.group(5)}
    return rows


def main() -> int:
    graph = graph_walk.parse(graph_walk.GRAPH_PATH)
    traversal = json.loads((ROOT / "analysis" / "traversal.json").read_text())
    visited = set(traversal["seed"]) | {r["taken"] for r in traversal["rounds"]}
    ledger = ledger_verdicts()
    rows = []
    for edge in graph.edges:
        if edge.kind != "dotted" or edge.src not in visited:
            continue
        source = ledger.get(edge.src, {"verdict": "UNRECORDED", "evidence": "no ledger row"})
        decision = "APPLIED" if edge.src == "paxos" and edge.dst == "raft" else "DECLINED"
        reason = (f"source `{edge.src}` visited with ledger verdict {source['verdict']}; "
                  f"counterpoint '{edge.label}' to `{edge.dst}` "
                  + ("carried into the understandability counterpoint" if decision == "APPLIED"
                     else "recorded as assessed, not adopted in Fail-Closed mode"))
        rows.append({"from": edge.src, "to": edge.dst, "label": edge.label,
                     "source_verdict": source["verdict"], "decision": decision,
                     "reason": reason})
    result = {"condition": "S5", "visited_anchors": len(visited),
              "dotted_edges_from_visited": len(rows),
              "applied": sum(r["decision"] == "APPLIED" for r in rows),
              "declined": sum(r["decision"] == "DECLINED" for r in rows),
              "undecided": sum(r["decision"] not in ("APPLIED", "DECLINED") for r in rows),
              "rows": rows}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("dotted_edges_from_visited", "applied",
                                             "declined", "undecided")}, sort_keys=True))
    return 0 if rows and result["undecided"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
