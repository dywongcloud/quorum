"""Run every QUORUM validator in dependency order and emit one JSON report.

    python3 -I scripts/verify_all.py

This is the single operator command for axiom A12 ("the operator can reproduce
every printed figure in one command"). Each child is executed with an explicit
argument list, never a shell. A non-zero child exit is reported, never hidden.
The report names the command and the exit code for every step.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PY = sys.executable
STEPS = [
    ("validate_skills", ["scripts/validate_skills.py"]),
    ("build_provenance", ["tools/build_provenance.py"]),
    ("validate_canon", ["scripts/validate_canon.py"]),
    ("build_decision_ledger", ["tools/build_decision_ledger.py"]),
    ("validate_graph", ["scripts/validate_graph.py"]),
    ("build_graph", ["tools/build_graph.py"]),
    ("build_ledger", ["tools/build_ledger.py"]),
    ("run_traversal", ["tools/run_traversal.py"]),
    ("build_panel_report", ["tools/build_panel_report.py"]),
    ("measure_web", ["tools/measure_web.py"]),
    ("selftest", ["skills/quorum/scripts/epistemic_audit.py", "--selftest"]),
    ("model_check", ["skills/quorum/scripts/epistemic_audit.py", "--payload", "state/clean.json", "--model-check"]),
    ("counterexample", ["skills/quorum/scripts/epistemic_audit.py", "--payload", "state/model-counterexample.json", "--model-check"]),
    ("crucible", ["skills/quorum/scripts/epistemic_audit.py", "--payload", "state/clean.json", "--crucible", "200"]),
    ("replay", ["skills/quorum/scripts/epistemic_audit.py", "--payload", "state/clean.json", "--replay"]),
    ("proof", ["skills/quorum/scripts/verify_invariants.py", "--proof", "A16"]),
    ("schemes", ["skills/quorum/scripts/verify_invariants.py", "--schemes"]),
    ("quorum", ["skills/quorum/scripts/collect_panel.py", "panel/R1", "--roster", "fail-closed", "--quorum"]),
    ("replication", ["skills/quorum/scripts/collect_panel.py", "panel/R2", "--roster", "fail-closed", "--replication"]),
    ("collect_R1", ["skills/quorum/scripts/collect_panel.py", "panel/R1", "--roster", "fail-closed", "--json"]),
    ("collect_R2", ["skills/quorum/scripts/collect_panel.py", "panel/R2", "--roster", "fail-closed", "--json"]),
    ("validate_figures", ["scripts/validate_figures.py"]),
    ("axioms", ["skills/quorum/scripts/verify_invariants.py", "--all"]),
    ("witnesses", ["skills/quorum/scripts/witnesses.py"]),
    ("validate_install", ["scripts/validate_install.py"]),
    ("compliance", ["tools/build_compliance.py"]),
]


def main() -> int:
    rows = []
    for name, argv in STEPS:
        completed = subprocess.run([PY, "-I", *argv], capture_output=True, text=True,
                                  cwd=str(ROOT), timeout=300)
        rows.append({"step": name, "command": " ".join(argv),
                     "exit_code": completed.returncode,
                     "stdout_bytes": len(completed.stdout.encode("utf-8")),
                     "stderr_traceback": "Traceback" in completed.stderr})
    passing = sum(r["exit_code"] == 0 for r in rows)
    print(json.dumps({"steps": len(rows), "passing": passing,
                      "failing": [r["step"] for r in rows if r["exit_code"] != 0],
                      "rows": rows}, sort_keys=True))
    return 0 if passing == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
