"""Regenerate the QUORUM anchor graph in memory and compare it to disk.

    python3 -I scripts/validate_graph.py

A graph that drifted from its builder is a second durable description and is
refused. The DAG check is delegated to graph_walk.py so there is one parser.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools" / "build_graph.py"
GRAPH = ROOT / "skills" / "quorum" / "references" / "anchor-graph.md"


def load_builder():
    spec = importlib.util.spec_from_file_location("quorum_build_graph", BUILDER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    if spec.loader is None:
        raise RuntimeError("builder module has no loader")
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_builder()
    expected = module.HEADER + module.build()
    actual = GRAPH.read_text(encoding="utf-8")
    sys.path.insert(0, str(ROOT / "skills" / "quorum" / "scripts"))
    import graph_walk
    graph = graph_walk.parse(GRAPH)
    dag = graph_walk.check_dag(graph)
    dangling = [f"{e.src} -> {e.dst}" for e in graph.edges
                if e.src not in graph.labels or e.dst not in graph.labels]
    result = {
        "byte_identical": expected == actual,
        "expected_bytes": len(expected.encode("utf-8")),
        "actual_bytes": len(actual.encode("utf-8")),
        "nodes": len(graph.labels),
        "edges": len(graph.edges),
        "acyclic": dag["acyclic"],
        "dangling_edges": dangling,
        "clusters": len(graph.clusters),
        "critic_seats": len([n for n in graph.labels if n.startswith("crit_")]),
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if result["byte_identical"] and result["acyclic"] and not dangling else 1


if __name__ == "__main__":
    sys.exit(main())
