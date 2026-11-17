"""Validate that every graph anchor has a ledger row and a provenance row.

    python3 -I scripts/validate_canon.py

A node with no ledger row or no provenance row is a phantom AST node. A
provenance row whose resolution site does not exist, or a row naming a node
absent from the graph, is a dangling citation. Both are refused. This is the
machine-checkable form of `forall sigma in AST: sigma in Gamma_real` and
`not exists phantom`.
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


def provenance_rows() -> dict[str, dict[str, str]]:
    text = (REFS / "anchor-provenance.md").read_text(encoding="utf-8")
    rows = {}
    for line in text.splitlines():
        match = re.match(r"^\|\s*`([a-z0-9_]+)`\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\S+)\s*\|$", line)
        if match:
            rows[match.group(1)] = {"kind": match.group(2),
                                    "cluster": match.group(3),
                                    "site": match.group(4)}
    return rows


def site_exists(site: str) -> bool:
    name, _, number = site.rpartition(":")
    target = (ROOT / name) if "/" in name else (REFS / name)
    if not target.is_file():
        return False
    try:
        return 1 <= int(number) <= len(target.read_text(encoding="utf-8").splitlines())
    except ValueError:
        return False


def main() -> int:
    graph = graph_walk.parse(graph_walk.GRAPH_PATH)
    ledger = (REFS / "traversal-ledger.md").read_text(encoding="utf-8")
    canon = (REFS / "canon.md").read_text(encoding="utf-8")
    ledger_ids = set(re.findall(r"^\|\s*\d+\s*\|\s*`([a-z0-9_]+)`\s*\|", ledger, flags=re.M))
    missing_ledger = sorted(set(graph.labels) - ledger_ids)
    extra_ledger = sorted(ledger_ids - set(graph.labels))
    cited_labels = set()
    canon_labels = set()
    for line in canon.splitlines():
        if line.startswith("| ") and " | " in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and cells[0] not in ("Label", "Quantity", "---"):
                cited_labels.update(re.findall(r"`([a-z0-9_]+)`", line))
                if cells[0] in set(graph.labels.values()):
                    canon_labels.add(cells[0])
    dangling = sorted(cited_labels - set(graph.labels))
    provenance = provenance_rows()
    uncovered = sorted(set(graph.labels) - set(provenance))
    extra_provenance = sorted(set(provenance) - set(graph.labels))
    bad_sites = sorted(node for node, row in provenance.items() if not site_exists(row["site"]))
    wrong_cluster = sorted(node for node, row in provenance.items()
                           if node in graph.labels and row["cluster"] != (graph.cluster_of[node] or "UNASSIGNED"))
    result = {
        "nodes": len(graph.labels),
        "ledger_rows": len(ledger_ids),
        "ledger_missing_nodes": missing_ledger,
        "ledger_extra_nodes": extra_ledger,
        "canon_cited_node_ids": len(cited_labels),
        "canon_labels_bound_to_graph": len(canon_labels),
        "canon_dangling_ids": dangling,
        "provenance_rows": len(provenance),
        "provenance_cited": sum(1 for row in provenance.values() if row["kind"] == "cited"),
        "provenance_derived": sum(1 for row in provenance.values() if row["kind"] == "derived"),
        "uncovered_labels": uncovered,
        "dangling_provenance_nodes": extra_provenance,
        "unresolvable_sites": bad_sites,
        "cluster_mismatches": wrong_cluster,
        "ok": (len(canon_labels) > 0 and not (missing_ledger or extra_ledger or dangling
               or uncovered or extra_provenance or bad_sites or wrong_cluster)),
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
