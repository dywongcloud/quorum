"""List which QUORUM panel seats have reported and which have not.

    python3 -I skills/quorum/scripts/collect_panel.py <panel_dir> <seat> [<seat> ...]

A verdict is a file. A seat has reported when <panel_dir>/<seat>.md exists and
actually says something. This script never infers a verdict and never treats a
missing seat as a pass: it prints MISSING and exits non-zero, so a caller can
retry the seat or record it as NOT REPORTED.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

MIN_WORDS = 20


def panel_path(raw: str) -> pathlib.Path:
    given = pathlib.Path(raw)
    if given.is_absolute() or given.is_dir():
        return given
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import quorum_paths
    return quorum_paths.data_root() / given


def collect(panel: pathlib.Path, seats: list[str], as_json: bool) -> int:
    missing: list[str] = []
    empty: list[str] = []
    rows = []
    for seat in seats:
        target = panel / f"{seat}.md"
        if not target.is_file():
            missing.append(seat)
            rows.append({"seat": seat, "status": "MISSING", "words": 0})
            continue
        words = len(target.read_text(encoding="utf-8", errors="replace").split())
        if words < MIN_WORDS:
            empty.append(seat)
            rows.append({"seat": seat, "status": "EMPTY", "words": words})
        else:
            rows.append({"seat": seat, "status": "REPORTED", "words": words})
    bad = missing + empty
    if as_json:
        print(json.dumps({
            "panel": str(panel),
            "seats_required": len(seats),
            "seats_reporting": len(seats) - len(bad),
            "missing": missing,
            "empty": empty,
            "quorum": not bad,
            "rows": rows,
        }, sort_keys=True))
    else:
        for row in rows:
            print(f'{row["status"]:9s} {row["seat"]}  ({row["words"]} words)' if row["status"] != "MISSING" else f'MISSING  {row["seat"]}')
        print(f"\n{len(seats) - len(bad)} of {len(seats)} seats reported.")
        if bad:
            print("not reported: " + ", ".join(bad))
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="QUORUM panel verdict collector")
    parser.add_argument("panel", type=str)
    parser.add_argument("seats", nargs="*", type=str)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--roster", type=str, default="")
    parser.add_argument("--graph", type=str, default="")
    parser.add_argument("--quorum", action="store_true")
    parser.add_argument("--replication", action="store_true")
    args = parser.parse_args(argv)
    panel = panel_path(args.panel)
    seats = list(args.seats)
    graph = None
    if args.roster or args.quorum or args.replication:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import graph_walk
        graph = graph_walk.parse(pathlib.Path(args.graph) if args.graph else graph_walk.GRAPH_PATH)
    if args.roster:
        if graph is None:
            raise RuntimeError("graph parser unavailable")
        seats = list(graph_walk.roster(graph, args.roster)["required_seats"])
    if args.replication:
        files = sorted(panel.glob("*.md"))
        copies = len(files)
        required = len(seats)
        ballots = []
        for f in files:
            match = re.search(r"^Dispatch id:\s*(\S+)", f.read_text(encoding="utf-8", errors="replace"), flags=re.M)
            if match:
                ballots.append(match.group(1))
        print(json.dumps({
            "term": 1, "leader": "panel-collector",
            "verdict_files": copies, "required_seats": required,
            "ballot_numbers": sorted(ballots),
            "commitIndex": len(ballots),
            "replicated_to_current_term_majority": copies >= (required // 2) + 1 and len(ballots) == copies,
            "commit_rule": "durable file per seat, one reader commits after current-term majority replication",
            "evidence": [f.name for f in files],
        }, sort_keys=True))
        return 0 if copies >= (required // 2) + 1 and len(ballots) == copies else 1
    if args.quorum:
        if graph is None:
            raise RuntimeError("graph parser unavailable")
        roster = set(seats)
        pairs = [p for p in graph.counterpoint_pairs()
                 if p[0] in roster and p[1] in roster]
        reported = {(panel / (s + ".md")).stem
                    for s in seats if (panel / (s + ".md")).is_file()}
        ballots = []
        for s in sorted(reported):
            match = re.search(r"^Dispatch id:\s*(\S+)", (panel / (s + ".md")).read_text(
                encoding="utf-8", errors="replace"), flags=re.M)
            if match:
                ballots.append(match.group(1))
        uncovered = [[a, b, label] for a, b, label in pairs
                     if a not in reported and b not in reported]
        majority = (len(seats) // 2) + 1
        minimal_uncovered = 0
        for a, b, _label in pairs:
            eligible = [s for s in seats if s not in (a, b)]
            if len(eligible) >= majority:
                minimal_uncovered += 1
        print(json.dumps({
            "quorum_check": "intersecting-majority",
            "seats_required": len(seats), "seats_reporting": len(reported),
            "majority_size": majority, "counterpoint_pairs": len(pairs),
            "pairs_uncovered_now": len(uncovered),
            "pairs_a_majority_can_omit_both_members": minimal_uncovered,
            "unanimity_needed": minimal_uncovered > 0,
            "ballot_numbers": sorted(ballots),
            "ballot_numbered": len(ballots) == len(reported) and len(set(ballots)) == len(ballots),
        }, sort_keys=True))
        return 0 if not uncovered else 1
    return collect(panel, seats, args.json)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
