"""Re-measure every figure printed by web/index.html at final state.

    python3 -I scripts/validate_figures.py

Each data-figure attribute names a key. The expected value is recomputed from
the graph, the scripts and the panel directory, never read from a cached file.
A drifted figure is reported and the command exits non-zero.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
WEB = ROOT / "web" / "index.html"
SCRIPTS = ROOT / "skills" / "quorum" / "scripts"
PYTHON = sys.executable


def run(script: str, *args: str) -> dict:
    completed = subprocess.run(
        [PYTHON, "-I", str(SCRIPTS / script), *args],
        capture_output=True, text=True, cwd=str(ROOT), timeout=120,
    )
    return json.loads(completed.stdout.strip())


def figures() -> dict[str, int]:
    counts = run("graph_walk.py", "--counts")
    roster = run("graph_walk.py", "--roster", "--mode", "fail-closed")
    selftest = run("epistemic_audit.py", "--selftest")
    probe = run("epistemic_audit.py", "--probe", "400")
    enumerated = run("epistemic_audit.py", "--payload", "state/clean.json", "--enumerate")
    axioms = pathlib.Path(SCRIPTS / "verify_invariants.py").read_text(encoding="utf-8")
    axiom_count = len(set(re.findall(r'"(A\d+)": check_A\d+', axioms)))
    ledger = pathlib.Path(SCRIPTS.parent / "references" / "fault-taxonomy.md").read_text(encoding="utf-8")
    fault_codes = len(set(re.findall(r"\[FAULT: ([A-Z_]+)\]", ledger)))
    panel = ROOT / "panel"
    verdicts = len(list(panel.glob("R*/*.md"))) if panel.exists() else 0
    return {
        "nodes": counts["nodes"],
        "edges": counts["edges"],
        "solid": counts["solid"],
        "dotted": counts["dotted"],
        "clusters": counts["clusters"],
        "critic_seats": counts["critics"],
        "critic_pairs": counts["critic_pairs"],
        "fail_closed_seats": roster["seat_count"],
        "axioms": axiom_count,
        "fault_codes": fault_codes,
        "probe_samples": probe["sample_count"],
        "selftest_cases": len(selftest["cases"]),
        "assignment_count": enumerated["assignment_count"],
        "panel_verdicts": verdicts,
    }


def printed() -> dict[str, list[int]]:
    html = WEB.read_text(encoding="utf-8")
    found: dict[str, list[int]] = {}
    for key, value in re.findall(r'data-figure="([a-z_]+)">(\d+)<', html):
        found.setdefault(key, []).append(int(value))
    return found


def main() -> int:
    expected = figures()
    shown = printed()
    rows = []
    for key, values in sorted(shown.items()):
        target = expected.get(key)
        rows.append({
            "figure": key,
            "printed": sorted(set(values)),
            "occurrences": len(values),
            "computed": target,
            "reproducible": target is not None and all(v == target for v in values),
        })
    missing = sorted(set(expected) - set(shown))
    result = {
        "figure_count": len(rows),
        "figures_not_printed": missing,
        "all_reproducible": all(r["reproducible"] for r in rows) and not missing,
        "rows": rows,
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if result["all_reproducible"] else 1


if __name__ == "__main__":
    sys.exit(main())
