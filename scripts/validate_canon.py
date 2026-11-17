"""Validate that every graph anchor has a ledger row and a canon provenance rule.

    python3 -I scripts/validate_canon.py

A node with no ledger row is a phantom AST node. A node cited in the canon but
absent from the graph is a dangling citation. Both are refused. This is the
machine-checkable form of the invariants `forall sigma in AST: sigma in
Gamma_real` and `not exists phantom`.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REFS = ROOT / "skills" / "quorum" / "references"
sys.path.insert(0, str(ROOT / "skills" / "quorum" / "scripts"))
import graph_walk  # noqa: E402


def main() -> int:
    graph = graph_walk.parse(graph_walk.GRAPH_PATH)
    ledger = (REFS / "traversal-ledger.md").read_text(encoding="utf-8")
    canon = (REFS / "canon.md").read_text(encoding="utf-8")
    ledger_ids = set(re.findall(r"^\|\s*\d+\s*\|\s*`([a-z0-9_]+)`\s*\|", ledger, flags=re.M))
    missing = sorted(set(graph.labels) - ledger_ids)
    extra = sorted(ledger_ids - set(graph.labels))
    cited_labels = set()
    for line in canon.splitlines():
        if line.startswith("| ") and " | " in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and cells[0] not in ("Label", "Quantity", "---"):
                cited_labels.update(re.findall(r"`([a-z0-9_]+)`", line))
    dangling = sorted(cited_labels - set(graph.labels))
    result = {
        "nodes": len(graph.labels),
        "ledger_rows": len(ledger_ids),
        "ledger_missing_nodes": missing,
        "ledger_extra_nodes": extra,
        "canon_cited_node_ids": len(cited_labels),
        "canon_dangling_ids": dangling,
        "provenance_rows": len(re.findall(r"^\| .+ \| .+ \| .+ \|$", canon, flags=re.M)),
        "ok": not missing and not extra and not dangling,
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
