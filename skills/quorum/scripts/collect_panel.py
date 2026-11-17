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
import sys

MIN_WORDS = 20


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
    args = parser.parse_args(argv)
    seats = list(args.seats)
    if args.roster:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import graph_walk
        graph = graph_walk.parse(pathlib.Path(args.graph) if args.graph else graph_walk.GRAPH_PATH)
        seats = list(graph_walk.roster(graph, args.roster)["required_seats"])
    return collect(pathlib.Path(args.panel), seats, args.json)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
