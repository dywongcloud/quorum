"""QUORUM graph walk: parse the anchor graph and compute the living Frontier.

    python3 -I skills/quorum/scripts/graph_walk.py --counts
    python3 -I skills/quorum/scripts/graph_walk.py --check-dag
    python3 -I skills/quorum/scripts/graph_walk.py --label tailatscale
    python3 -I skills/quorum/scripts/graph_walk.py --seat crit_imp_fischer
    python3 -I skills/quorum/scripts/graph_walk.py --roster --mode fail-closed
    python3 -I skills/quorum/scripts/graph_walk.py --frontier --visited flp,gilbert,paxos
    python3 -I skills/quorum/scripts/graph_walk.py --render --visited flp,gilbert,paxos

All output is JSON or Mermaid text. No prose is emitted on stdout. The parser
reads the generated Mermaid fenced block in references/anchor-graph.md; it
never reads a second copy of the graph.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from dataclasses import dataclass

GRAPH_PATH = (pathlib.Path(__file__).resolve().parents[1]
              / "references" / "anchor-graph.md")

NODE_RE = re.compile(r'^\s*([A-Za-z0-9_]+)\["([^"]+)"\]:::([a-z]+)\s*$')
EDGE_RE = re.compile(r'^\s*([A-Za-z0-9_]+)\s+(-\.->|-->)\|([^|]+)\|\s+([A-Za-z0-9_]+)\s*$')
SUBGRAPH_RE = re.compile(r'^\s*subgraph\s+([A-Z0-9_]+)\["([^"]+)"\]\s*$')

FAIL_CLOSED_SEED = (
    "crit_imp_fischer", "crit_imp_lynch", "crit_imp_paterson",
    "crit_form_clarke", "crit_form_emerson",
    "crit_type_milner", "crit_type_martinlof",
)
GRACEFUL_SEED = (
    "crit_chaos_basiri", "crit_chaos_allspaw",
    "crit_ops_beyer", "crit_ops_jones",
    "crit_erasure_star", "crit_erasure_bowker",
)
PRIORITY = (
    "andon", "reopened", "break-dotted", "disagreement", "incoming", "outgoing",
)


@dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    label: str
    kind: str


@dataclass(frozen=True)
class Graph:
    labels: dict[str, str]
    classes: dict[str, str]
    clusters: dict[str, str]
    cluster_of: dict[str, str]
    edges: tuple[Edge, ...]

    def neighbours(self, node: str) -> list[dict[str, str]]:
        found: list[dict[str, str]] = []
        for e in self.edges:
            if e.dst == node:
                found.append({"candidate": e.src, "via": e.label,
                              "direction": "incoming", "kind": e.kind, "from": node})
            elif e.src == node:
                found.append({"candidate": e.dst, "via": e.label,
                              "direction": "outgoing", "kind": e.kind, "from": node})
            elif e.kind == "dotted" and (e.src == node or e.dst == node):
                other = e.dst if e.src == node else e.src
                found.append({"candidate": other, "via": e.label,
                              "direction": "counterpoint", "kind": e.kind, "from": node})
        return found

    def counterpoint_pairs(self) -> tuple[tuple[str, str, str], ...]:
        return tuple((e.src, e.dst, e.label) for e in self.edges
                     if e.kind == "dotted" and e.src.startswith("crit_") and e.dst.startswith("crit_"))


def parse(path: pathlib.Path) -> Graph:
    text = path.read_text(encoding="utf-8")
    labels: dict[str, str] = {}
    classes: dict[str, str] = {}
    clusters: dict[str, str] = {}
    cluster_of: dict[str, str] = {}
    edges: list[Edge] = []
    current = ""
    inside = False
    for line in text.splitlines():
        if line.strip() == "```mermaid":
            inside = True
            continue
        if inside and line.strip() == "```":
            break
        if not inside:
            continue
        m = SUBGRAPH_RE.match(line)
        if m:
            current = m.group(1)
            clusters[current] = m.group(2)
            continue
        if line.strip() == "end":
            current = ""
            continue
        m = NODE_RE.match(line)
        if m:
            nid, label, klass = m.group(1), m.group(2), m.group(3)
            if nid in labels:
                raise ValueError(f"duplicate node id {nid}")
            labels[nid] = label
            classes[nid] = klass
            cluster_of[nid] = current
            continue
        m = EDGE_RE.match(line)
        if m:
            edges.append(Edge(m.group(1), m.group(4), m.group(3),
                              "dotted" if m.group(2) == "-.->" else "solid"))
            continue
        if line.strip().startswith("classDef") or line.strip().startswith("%%"):
            continue
        if line.strip() in ("flowchart LR", ""):
            continue
        raise ValueError(f"unparsed graph line: {line!r}")
    for e in edges:
        if e.src not in labels or e.dst not in labels:
            raise ValueError(f"dangling edge {e.src} -> {e.dst}")
    return Graph(labels, classes, clusters, cluster_of, tuple(edges))


def check_dag(graph: Graph) -> dict[str, object]:
    indegree = {n: 0 for n in graph.labels}
    adjacency: dict[str, list[str]] = {n: [] for n in graph.labels}
    for e in graph.edges:
        adjacency[e.src].append(e.dst)
        indegree[e.dst] += 1
    queue = [n for n in graph.labels if indegree[n] == 0]
    order: list[str] = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for nxt in adjacency[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    acyclic = len(order) == len(graph.labels)
    return {
        "acyclic": acyclic,
        "node_count": len(graph.labels),
        "edge_count": len(graph.edges),
        "topological_order_size": len(order),
        "blocked": [n for n, d in indegree.items() if d > 0] if not acyclic else [],
        "digest": hashlib.sha256(
            json.dumps([graph.labels, [[e.src, e.dst, e.label, e.kind] for e in graph.edges]],
                       sort_keys=True).encode("utf-8")).hexdigest(),
    }


def roster(graph: Graph, mode: str) -> dict[str, object]:
    seed = FAIL_CLOSED_SEED if mode == "fail-closed" else GRACEFUL_SEED
    pairs = graph.counterpoint_pairs()
    seats = set(seed)
    changed = True
    rounds = 0
    while changed:
        changed = False
        rounds += 1
        for a, b, _label in pairs:
            if a in seats and b not in seats:
                seats.add(b)
                changed = True
            if b in seats and a not in seats:
                seats.add(a)
                changed = True
    return {
        "mode": mode,
        "seed_seats": list(seed),
        "closure_rounds": rounds - 1,
        "required_seats": sorted(seats),
        "seat_count": len(seats),
        "lens_bindings": {s: lens_for(graph, s) for s in sorted(seats)},
    }


def lens_for(graph: Graph, seat: str) -> dict[str, str]:
    for e in graph.edges:
        if e.dst == seat and e.label == "argues from alone":
            return {"lens": e.src, "label": graph.labels.get(e.src, "")}
    return {"lens": "", "label": ""}


def frontier(graph: Graph, visited: list[str], priority_flags: dict[str, list[str]]) -> dict[str, object]:
    seen: set[str] = set()
    candidates: list[dict[str, str]] = []
    for node in visited:
        if node not in graph.labels:
            continue
        for item in graph.neighbours(node):
            key = (item["candidate"], item["via"], item["direction"])
            if key in seen:
                continue
            seen.add(key)
            entry = dict(item)
            entry["priority"] = rank(item, priority_flags)
            candidates.append(entry)
    candidates.sort(key=lambda c: (PRIORITY.index(c["priority"]), c["candidate"], c["via"]))
    return {
        "visited": visited,
        "candidate_count": len(candidates),
        "open_count": len([c for c in candidates if c["candidate"] not in visited]),
        "candidates": candidates,
    }


def rank(item: dict[str, str], flags: dict[str, list[str]]) -> str:
    name = item["candidate"]
    if name in flags.get("andon", []):
        return "andon"
    if name in flags.get("reopened", []):
        return "reopened"
    if item["kind"] == "dotted" and name in flags.get("break-dotted", []):
        return "break-dotted"
    if name in flags.get("disagreement", []):
        return "disagreement"
    if item["direction"] == "incoming":
        return "incoming"
    return "outgoing"


def render(graph: Graph, visited: list[str]) -> str:
    lines = ["```mermaid", "flowchart LR"]
    for cluster, title in graph.clusters.items():
        lines.append(f'  subgraph {cluster}["{title}"]')
        for nid, label in graph.labels.items():
            if graph.cluster_of.get(nid) == cluster:
                lines.append(f'  {nid}["{label}"]:::{graph.classes[nid]}')
        lines.append("  end")
    for e in graph.edges:
        arrow = "-->|" if e.kind == "solid" else "-.->|"
        lines.append(f"  {e.src} {arrow}{e.label}| {e.dst}")
    taken = [n for n in visited if n in graph.labels]
    if taken:
        lines.append("  class " + ",".join(taken) + " visited")
    lines.append("```")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="QUORUM graph walk")
    parser.add_argument("--graph", type=str, default=str(GRAPH_PATH))
    parser.add_argument("--counts", action="store_true")
    parser.add_argument("--check-dag", action="store_true")
    parser.add_argument("--label", type=str)
    parser.add_argument("--seat", type=str)
    parser.add_argument("--roster", action="store_true")
    parser.add_argument("--mode", type=str, default="fail-closed",
                        choices=("fail-closed", "graceful"))
    parser.add_argument("--frontier", action="store_true")
    parser.add_argument("--visited", type=str, default="")
    parser.add_argument("--andon", type=str, default="")
    parser.add_argument("--reopened", type=str, default="")
    parser.add_argument("--break-dotted", type=str, default="")
    parser.add_argument("--disagreement", type=str, default="")
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args(argv)
    try:
        graph = parse(pathlib.Path(args.graph))
    except (OSError, ValueError) as exc:
        print(json.dumps({"fault": "JANK_DETECTED", "code": "JANK_DETECTED",
                          "reason": f"engine-internal: {type(exc).__name__}",
                          "query_id": "graph", "digest": ""}, sort_keys=True))
        return 1
    if args.counts:
        solid = len([e for e in graph.edges if e.kind == "solid"])
        dotted = len([e for e in graph.edges if e.kind == "dotted"])
        print(json.dumps({
            "nodes": len(graph.labels), "edges": len(graph.edges),
            "solid": solid, "dotted": dotted,
            "clusters": len(graph.clusters),
            "critics": len([n for n in graph.labels if n.startswith("crit_")]),
            "critic_pairs": len(graph.counterpoint_pairs()),
        }, sort_keys=True))
        return 0
    if args.check_dag:
        result = check_dag(graph)
        print(json.dumps(result, sort_keys=True))
        return 0 if result["acyclic"] else 1
    if args.label:
        print(json.dumps({"id": args.label, "label": graph.labels.get(args.label),
                          "class": graph.classes.get(args.label),
                          "cluster": graph.cluster_of.get(args.label)}, sort_keys=True))
        return 0 if args.label in graph.labels else 1
    if args.seat:
        print(json.dumps({"seat": args.seat, **lens_for(graph, args.seat)}, sort_keys=True))
        return 0
    if args.roster:
        print(json.dumps(roster(graph, args.mode), sort_keys=True))
        return 0
    visited = [v.strip() for v in args.visited.split(",") if v.strip()]
    if args.frontier:
        flags = {k: [x.strip() for x in v.split(",") if x.strip()]
                 for k, v in (("andon", args.andon), ("reopened", args.reopened),
                              ("break-dotted", args.break_dotted),
                              ("disagreement", args.disagreement))}
        print(json.dumps(frontier(graph, visited, flags), sort_keys=True))
        return 0
    if args.render:
        print(render(graph, visited))
        return 0
    print(json.dumps({"error": "no mode selected"}, sort_keys=True))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
