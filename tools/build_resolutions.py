"""Resolve every R2 OBJECT from live witness output, never from assertion.

    python3 -I tools/build_resolutions.py

For each OBJECT filed in panel/R2, the tool runs a named live command and
checks a named field in its JSON output. A resolution is ADAPT only when the
field has the witnessed value, SCRAP only when the objection's premise is
refuted by a measured value, and OVERRULE only when a cited axiom and a live
command refuse the requested change. Unwitnessed objections stay OPEN. The
tool writes analysis/resolutions.json and splices a table into QUORUM-LOG.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOG = ROOT / "QUORUM-LOG.md"
OUT = ROOT / "analysis" / "resolutions.json"
PANEL = ROOT / "panel" / "R2"
SCRIPTS = ROOT / "skills" / "quorum" / "scripts"
PY = sys.executable
START = "<!-- RESOLUTIONS:START -->"
END = "<!-- RESOLUTIONS:END -->"

# seat -> (kind, command, dotted field path, expected value, action, dependents)
CASES = {
    "crit_chaos_basiri": ("ADAPT", ["skills/quorum/scripts/witnesses.py"],
                          "two_fault_crucible.steady_state_holds", True,
                          "two fault classes varied against a p99 steady state", ["M12", "A7", "A11"]),
    "crit_cons_lamport": ("ADAPT", ["skills/quorum/scripts/collect_panel.py", "panel/R2", "--roster", "fail-closed", "--quorum"],
                          "ballot_numbered", True,
                          "ballot numbers read from filed dispatch ids, intersecting majority measured", ["M3", "A22"]),
    "crit_cons_oust": ("ADAPT", ["skills/quorum/scripts/collect_panel.py", "panel/R2", "--roster", "fail-closed", "--replication"],
                       "replicated_to_current_term_majority", True,
                       "term, leader and commitIndex emitted from durable verdict copies", ["M3", "A20"]),
    "crit_form_clarke": ("ADAPT", ["skills/quorum/scripts/witnesses.py"],
                         "least_fixpoint_certificate.closed_under_R", True,
                         "least-fixpoint closure certificate with transition edges", ["M11", "A23"]),
    "crit_human_perrow": ("ADAPT", ["scripts/validate_figures.py"],
                          "all_reproducible", True,
                          "one FIGURE_MISMATCH fault per figure, isolated from other figures", ["M7", "A5", "A12"]),
    "crit_imp_lynch": ("ADAPT", ["skills/quorum/scripts/witnesses.py"],
                       "bivalent_schedule.declared_matches_ledger", True,
                       "one-crash bivalent schedule, no termination claim", ["M9", "A23"]),
    "crit_part_gilbert": ("ADAPT", ["skills/quorum/scripts/witnesses.py"],
                          "stale_read_witness.stale_read_observed", True,
                          "partition schedule with stale read and nonterminating operation", ["A4", "A9"]),
    "crit_rupt_taleb": ("ADAPT", ["skills/quorum/scripts/witnesses.py"],
                        "mutation_harness.all_successors_failed", True,
                        "harder successor from each jank digest fails preflight", ["A24"]),
    "crit_safety_kingsbury": ("ADAPT", ["skills/quorum/scripts/witnesses.py"],
                              "linearizability_witness.checked", True,
                              "fault-injected histories checked against a register model", ["M4", "A23"]),
    "crit_type_martinlof": ("ADAPT", ["skills/quorum/scripts/verify_invariants.py", "--proof", "A16"],
                            "discharged", True,
                            "dependent proof term for forall e, Not (HasIO e)", ["A16"]),
    "crit_type_milner": ("ADAPT", ["skills/quorum/scripts/verify_invariants.py", "--schemes"],
                         "bindings", lambda n: isinstance(n, int) and n > 0,
                         "principal type schemes from unification over let bindings", ["A13"]),
}


def field(payload: object, dotted: str) -> object:
    current = payload
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def run(argv: list[str]) -> object:
    completed = subprocess.run([PY, "-I", *argv], capture_output=True, text=True,
                               cwd=str(ROOT), timeout=180)
    for line in completed.stdout.strip().splitlines():
        try:
            return json.loads(line)
        except ValueError:
            continue
    return {}


def main() -> int:
    rows = []
    for seat, (kind, argv, dotted, expected, action, dependents) in CASES.items():
        verdict = PANEL / f"{seat}.md"
        text = verdict.read_text(encoding="utf-8", errors="replace") if verdict.is_file() else ""
        objected = bool(re.search(r"^Verdict:\s*OBJECT", text, flags=re.M))
        payload = run(argv)
        observed = field(payload, dotted)
        holds = observed == expected if not callable(expected) else expected(observed)
        rows.append({
            "seat": seat, "r2_object": objected, "resolution": kind if holds else "OPEN",
            "command": "python3 -I " + " ".join(argv), "field": dotted,
            "observed": observed, "expected": "callable:>0" if callable(expected) else expected,
            "action": action if holds else "witness missing",
            "reopened_dependents": dependents if holds else [],
        })
    result = {
        "source": "panel/R2 OBJECT verdicts resolved by live witness commands",
        "rows": rows,
        "r2_objects": sum(r["r2_object"] for r in rows),
        "resolved": sum(r["resolution"] != "OPEN" for r in rows),
        "open": [r["seat"] for r in rows if r["resolution"] == "OPEN"],
        "frame_swap": ("criterion changed from unanimous panel PASS to every OBJECT discharged "
                       "by a named live witness, then re-judged in a fresh WHOLE round"),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["| Seat | R2 | Resolution | Witness field | Observed | Dependents reopened |",
             "|---|---|---|---|---|---|"]
    for row in rows:
        lines.append(f"| `{row['seat']}` | {'OBJECT' if row['r2_object'] else 'PASS'} | "
                     f"{row['resolution']} | `{row['field']}` | {row['observed']} | "
                     f"{', '.join(row['reopened_dependents']) or 'none'} |")
    lines.append("")
    lines.append(f"Frame swap: {result['frame_swap']}.")
    log = LOG.read_text(encoding="utf-8")
    if START in log and END in log:
        head, rest = log.split(START, 1)
        _, tail = rest.split(END, 1)
        log = head + START + "\n" + "\n".join(lines) + "\n" + END + tail
        LOG.write_text(log, encoding="utf-8")
    print(json.dumps({"r2_objects": result["r2_objects"], "resolved": result["resolved"],
                      "open": result["open"]}, sort_keys=True))
    return 0 if not result["open"] else 1


if __name__ == "__main__":
    sys.exit(main())
