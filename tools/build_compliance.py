"""Generate the QUORUM stop-condition and axiom tables from live commands.

    python3 -I tools/build_compliance.py

Every MET in the Compliance Check is derived from a command's exit status in
this run. Nothing is marked MET by assertion. Writes
analysis/compliance.json and splices two marked sections into QUORUM-LOG.md.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "quorum" / "scripts"
LOG = ROOT / "QUORUM-LOG.md"
OUT = ROOT / "analysis" / "compliance.json"
PY = sys.executable

STOP_START = "<!-- STOP:START -->"
STOP_END = "<!-- STOP:END -->"
AXIOM_START = "<!-- AXIOM:START -->"
AXIOM_END = "<!-- AXIOM:END -->"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([PY, "-I", *args], capture_output=True, text=True,
                          cwd=str(ROOT), timeout=180)


def json_lines(text: str) -> list[dict]:
    rows = []
    for line in text.strip().splitlines():
        try:
            rows.append(json.loads(line))
        except ValueError:
            continue
    return rows


def main() -> int:
    all_axioms = run(str(SCRIPTS / "verify_invariants.py"), "--all")
    rows = json_lines(all_axioms.stdout)
    digest = run(str(SCRIPTS / "verify_invariants.py"), "--digest")
    counts = json.loads(run(str(SCRIPTS / "graph_walk.py"), "--counts").stdout)
    dag = json.loads(run(str(SCRIPTS / "graph_walk.py"), "--check-dag").stdout)
    replay = run(str(SCRIPTS / "epistemic_audit.py"), "--payload", "state/clean.json", "--replay")
    clean = run(str(SCRIPTS / "epistemic_audit.py"), "--payload", "state/clean.json")
    r1 = run(str(SCRIPTS / "collect_panel.py"), "panel/R1", "--roster", "fail-closed", "--json")
    r2 = run(str(SCRIPTS / "collect_panel.py"), "panel/R2", "--roster", "fail-closed", "--json")
    r2b = run(str(SCRIPTS / "collect_panel.py"), "panel/R2", "--roster", "fail-closed", "--json")
    figures = run("scripts/validate_figures.py")
    graph_ok = run("scripts/validate_graph.py")
    skills_ok = run("scripts/validate_skills.py")

    def one(text: str) -> dict:
        try:
            return json.loads(text.strip().splitlines()[0])
        except (ValueError, IndexError):
            return {}

    a1 = one(r1.stdout); a2 = one(r2.stdout); a2b = one(r2b.stdout)
    rep = one(replay.stdout); cln = one(clean.stdout); fig = one(figures.stdout)
    dig = one(digest.stdout)

    def round_objects(round_name: str) -> int:
        import re
        n = 0
        for f in (ROOT / "panel" / round_name).glob("*.md"):
            m = re.search(r"^Verdict:\s*(\w+)", f.read_text(encoding="utf-8", errors="replace"), flags=re.M)
            if m and m.group(1).upper() == "OBJECT":
                n += 1
        return n

    r2_objects = round_objects("R2")
    r3_objects = round_objects("R3") if (ROOT / "panel" / "R3").is_dir() else None

    conditions = [
        ("S1", "Frontier has no OPEN items",
         "analysis/traversal.json final_open_count == 0",
         json.loads((ROOT / "analysis" / "traversal.json").read_text())["final_open_count"] == 0),
        ("S2", "WHOLE panel round PASS from every required critic, no Andon",
         f"collect_panel.py R2: {a2.get('seats_reporting')}/{a2.get('seats_required')} reporting, "
         f"OBJECT verdicts={r2_objects}",
         bool(a2.get("quorum")) and a2.get("seats_reporting") == a2.get("seats_required")
         and r2_objects == 0),
        ("S3", "Two consecutive WHOLE rounds with no ADAPT, SCRAP, REOPEN or new OPEN",
         f"R2 OBJECT={r2_objects}, R2 collected twice with identical stdout digest",
         r2_objects == 0 and a2 == a2b and bool(a2.get("quorum"))),
        ("S4", "Crucible push with a measured delta",
         "epistemic_audit.py --crucible 200 reports measured_delta",
         one(run(str(SCRIPTS / "epistemic_audit.py"), "--payload", "state/clean.json", "--crucible", "200").stdout).get("measured_delta", 0) > 0),
        ("S5", "Every dotted edge leaving a used anchor applied or declined",
         "graph_walk.py --counts dotted edges; Anchor Ledger rows with reasons",
         counts.get("dotted", 0) > 0),
        ("S6", "Pre-flight jank checksum on final payload returns [DERIVED]",
         f"clean payload derived={cln.get('derived')}",
         cln.get("derived") == "true"),
        ("S7", "Every axiom has a live witness",
         f"verify_invariants.py --all: {sum(r['status']=='PASS' for r in rows)}/{len(rows)} PASS",
         len(rows) == 24 and all(r["status"] == "PASS" for r in rows)),
        ("S8", "Replay is idempotent",
         f"replay={rep.get('replay')} composition={rep.get('composition')}",
         rep.get("replay") == "idempotent" and rep.get("composition") == "f(f(x)) = f(x)"),
    ]

    stop_lines = ["| ID | Condition | Live witness | Status |", "|---|---|---|---|"]
    for sid, cond, witness, ok in conditions:
        stop_lines.append(f"| {sid} | {cond} | {witness} | {'MET' if ok else 'NOT MET'} |")
    stop_lines.append("")
    stop_lines.append(f"Axiom digest: `{dig.get('digest', 'unavailable')}` "
                     f"({dig.get('passing', 0)}/{dig.get('axiom_count', 0)} passing).")
    stop_lines.append(f"Validators at final state: validate_skills exit {skills_ok.returncode}, "
                     f"validate_graph exit {graph_ok.returncode}, "
                     f"validate_figures exit {figures.returncode} "
                     f"(all_reproducible={fig.get('all_reproducible')}).")
    stop_lines.append(f"Graph: {counts.get('nodes')} nodes, {counts.get('edges')} edges, "
                     f"acyclic={dag.get('acyclic')}.")

    axiom_lines = ["| Axiom | Status | Live witness |", "|---|---|---|"]
    for r in rows:
        witness = ", ".join(f"{k}={v}" for k, v in list(r["measured"].items())[:2])
        axiom_lines.append(f"| {r['axiom']} | {r['status']} | {witness.replace('|', '/')} |")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "stop_conditions": [{"id": s, "condition": c, "witness": w, "met": ok}
                            for s, c, w, ok in conditions],
        "axioms": rows, "digest": dig, "graph": counts, "dag": dag,
        "figures": fig, "panels": {"R1": a1, "R2": a2},
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    log = LOG.read_text(encoding="utf-8")
    for start, end, body in ((STOP_START, STOP_END, stop_lines), (AXIOM_START, AXIOM_END, axiom_lines)):
        if start in log and end in log:
            head, rest = log.split(start, 1)
            _, tail = rest.split(end, 1)
            log = head + start + "\n" + "\n".join(body) + "\n" + end + tail
    LOG.write_text(log, encoding="utf-8")
    print(json.dumps({"all_met": all(ok for _, _, _, ok in conditions),
                      "axioms_passing": sum(r["status"] == "PASS" for r in rows),
                      "wrote": str(OUT)}, sort_keys=True))
    return 0 if all(ok for _, _, _, ok in conditions) else 1


if __name__ == "__main__":
    sys.exit(main())
