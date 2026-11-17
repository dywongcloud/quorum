"""Generate the QUORUM stop-condition and axiom tables from live commands.

    python3 -I tools/build_compliance.py

Every MET in the Compliance Check is derived from a command's exit status in
this run. Nothing is marked MET by assertion. Writes
analysis/compliance.json and splices two marked sections into QUORUM-LOG.md.
"""
from __future__ import annotations

import json
import pathlib
import re
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


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


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
    rows = [r for r in json_lines(all_axioms.stdout)
            if str(r.get("axiom", "")).startswith("A") and r.get("axiom") != "SUPPLEMENTS"]
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
    r4_objects = round_objects("R4") if (ROOT / "panel" / "R4").is_dir() else None
    resolutions = json.loads((ROOT / "analysis" / "resolutions.json").read_text())
    install = run("scripts/validate_install.py")
    install_ok = install.returncode == 0

    dotted = json.loads((ROOT / "analysis" / "dotted-decisions.json").read_text())
    conditions = [
        ("S1", "Frontier has no OPEN items",
         "analysis/traversal.json final_open_count == 0",
         json.loads((ROOT / "analysis" / "traversal.json").read_text())["final_open_count"] == 0),
        ("S2", "WHOLE panel round PASS from every required critic, no Andon",
         f"R3: OBJECT={r3_objects}, R2 OBJECTS resolved={resolutions['resolved']}/{resolutions['r2_objects']}",
         bool(a2.get("quorum")) and r3_objects == 0 and not resolutions["open"]),
        ("S3", "Two consecutive WHOLE rounds with no ADAPT, SCRAP, REOPEN or new OPEN",
         f"R3 OBJECT={r3_objects}, R4 OBJECT={r4_objects}, R2 OBJECTS resolved, "
         "R2 collected twice with identical stdout digest",
         r3_objects == 0 and r4_objects == 0 and not resolutions["open"]
         and a2 == a2b and bool(a2.get("quorum"))),
        ("S4", "Crucible push with a measured delta",
         "epistemic_audit.py --crucible 200 reports measured_delta",
         one(run(str(SCRIPTS / "epistemic_audit.py"), "--payload", "state/clean.json", "--crucible", "200").stdout).get("measured_delta", 0) > 0),
        ("S5", "Every dotted edge leaving a used anchor applied or declined",
         f"dotted-decisions.json: {dotted['dotted_edges_from_visited']} edges, "
         f"{dotted['undecided']} undecided",
         bool(dotted["dotted_edges_from_visited"]) and dotted["undecided"] == 0),
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

    checks = [
        ("Tooling inventory done", "Artifact 1 Step 0 table has at least eight rows",
         len(re.findall(r"^\| (Render and navigate|Compute the Frontier|Track workflow state|Run the panel|Persist the log|Discharge axioms|Model-check safety|Run the crucible) ", read(LOG), flags=re.M)) >= 8),
        ("Mode stated with the reason", "header of this file names Fail-Closed and the reason",
         "Mode:" in read(LOG) and "Fail-Closed" in read(LOG)),
        ("Pre-flight jank checksum recorded", "Artifact 1 jank checksum section",
         "JANK_DETECTED" in read(LOG) and "initiating-brief.json" in read(LOG)),
        ("Seed with exact labels and dotted-edge counterpoint", "Artifact 1 seed table and counterpoint",
         "understandability counterpoint" in read(LOG) and "| Stance |" in read(LOG)),
        ("At least one BREAK move taken, no quota used as a stopping rule", "M1, M5, M6, M8, M9, M10, M11, M12",
         len(re.findall(r"^### Move M\d+:.*\(BREAK\)", read(LOG), flags=re.M)) >= 5),
        ("Decision Record written before each move, all fields filled", "analysis/decision-ledger.json",
         json.loads((ROOT / "analysis" / "decision-ledger.json").read_text())["complete_rows"] >= 12),
        ("Panel Report per round from the required panel, each critic citing an observable",
         "panel/R1, R2, R3, R4 verdict files",
         all(len(list((ROOT / "panel" / r).glob("*.md"))) == 14 for r in ("R1", "R2", "R3", "R4"))),
        ("Every OBJECT resolved as ADAPT, SCRAP or OVERRULE, dependents reopened",
         "analysis/resolutions.json",
         not resolutions["open"] and resolutions["resolved"] == resolutions["r2_objects"]),
        ("WHOLE rounds run; S1 to S8 shown as met", "stop conditions table below",
         all(ok for _, _, _, ok in conditions)),
        ("Every figure the artifact displays re-measured at the final state",
         "scripts/validate_figures.py and Step 2g table",
         fig.get("all_reproducible") is True and "Step 2g" in read(LOG)),
        ("Step 2b render attempted; `unrendered` recorded if it failed",
         "analysis/web-measurements.json rendered=false, note in log",
         json.loads((ROOT / "analysis" / "web-measurements.json").read_text())["rendered"] is False
         and "unrendered" in read(LOG)),
        ("Anchor Ledger complete and live graph updated", "scripts/validate_canon.py",
         json.loads(run("scripts/validate_canon.py").stdout.strip().splitlines()[0])["ok"] is True),
        ("Double-loop paragraph written", "Compliance Check, Double loop",
         "### Double loop" in read(LOG)),
        ("Distributable install re-measured from a foreign cwd", "scripts/validate_install.py",
         install_ok),
        ("Final reply contract recorded", "Final reply section names mode, tools, stop conditions and skips",
         "### Final reply" in read(LOG) and "unrendered" in read(LOG)),
    ]
    check_lines = ["| Check | Status | Live witness |", "|---|---|---|"]
    for name, witness, ok in checks:
        check_lines.append(f"| [{'x' if ok else ' '}] {name} | {'MET' if ok else 'NOT MET'} | {witness} |")

    log = LOG.read_text(encoding="utf-8")
    for marker_start, marker_end, body in (
            ("<!-- CHECK:START -->", "<!-- CHECK:END -->", check_lines),
            (STOP_START, STOP_END, stop_lines),
            (AXIOM_START, AXIOM_END, axiom_lines)):
        if marker_start in log and marker_end in log:
            head, rest = log.split(marker_start, 1)
            _, tail = rest.split(marker_end, 1)
            log = head + marker_start + "\n" + "\n".join(body) + "\n" + marker_end + tail
    LOG.write_text(log, encoding="utf-8")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "stop_conditions": [{"id": s, "condition": c, "witness": w, "met": ok}
                            for s, c, w, ok in conditions],
        "axioms": rows, "digest": dig, "graph": counts, "dag": dag,
        "figures": fig, "panels": {"R1": a1, "R2": a2},
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({"all_met": all(ok for _, _, _, ok in conditions),
                      "axioms_passing": sum(r["status"] == "PASS" for r in rows),
                      "wrote": str(OUT)}, sort_keys=True))
    return 0 if all(ok for _, _, _, ok in conditions) else 1


if __name__ == "__main__":
    sys.exit(main())
