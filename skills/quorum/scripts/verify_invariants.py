"""QUORUM axiom discharge: run each invariant as a live command.

    python3 -I skills/quorum/scripts/verify_invariants.py --all
    python3 -I skills/quorum/scripts/verify_invariants.py --axiom A4
    python3 -I skills/quorum/scripts/verify_invariants.py --digest

Output is one JSON object per axiom with status, measured and witness. A status
other than PASS is a blocking OBJECT. All child commands are executed with
explicit argument lists, never a shell, and every path is derived from this
file's location. The script itself is read-only.

Detection tokens are assembled from fragments so that the checker does not
trip its own scan: a literal marker in the checker would be indistinguishable
from a marker in the code it inspects.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "skills" / "quorum" / "scripts"
REFS = ROOT / "skills" / "quorum" / "references"
GRAPH = REFS / "anchor-graph.md"
LOG = ROOT / "QUORUM-LOG.md"
WEB = ROOT / "web" / "index.html"
PYTHON = sys.executable


def tok(*parts: str) -> str:
    return "".join(parts)


DEFER = (tok("TO", "DO"), tok("FIX", "ME"), tok("XX", "X"), tok("/", "/", ".", ".", "."))
SECRETS = (tok("AK", "IA"), tok("BEGIN PRIVATE", " KEY"), tok("Bea", "rer "), tok("pass", "word="))
DYNAMIC = (tok("shell", "=True"), tok("os.sys", "tem("), tok("ev", "al("), tok("ex", "ec("))
SHARED = (tok("glo", "bal "), tok("import thre", "ading"), tok("while T", "rue:"))
BARE = (tok("except", ":"), tok("assert", " "))
IO_TOKENS = (tok("op", "en("), tok("read", "_text"), tok("pr", "int("), tok("sub", "process"))


def run(script: str, *args: str) -> tuple[int, str]:
    completed = subprocess.run(
        [PYTHON, "-I", str(SCRIPTS / script), *args],
        capture_output=True, text=True, cwd=str(ROOT), timeout=120,
    )
    return completed.returncode, completed.stdout.strip() or completed.stderr.strip()


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def source_files() -> list[pathlib.Path]:
    paths = list(SCRIPTS.glob("*.py"))
    paths += list((ROOT / "tools").glob("*.py"))
    paths += list((ROOT / "scripts").glob("*.py"))
    return sorted(paths)


def source_text() -> str:
    return "\n".join(read(p) for p in source_files())


def json_or_none(text: str) -> dict:
    try:
        return json.loads(text)
    except ValueError:
        return {}


def check_A1() -> tuple[str, object]:
    code, out = run("epistemic_audit.py", "--payload", "state/clean.json", "--replay")
    text = read(SCRIPTS / "epistemic_audit.py")
    payload = json_or_none(out)
    ok = code == 0 and payload.get("replay") == "idempotent" and "@dataclass(frozen=True)" in text and "class State:" in text
    return ("PASS" if ok else "FAIL", {"replay": payload.get("replay"), "frozen_state": "@dataclass(frozen=True)" in text})


def check_A2() -> tuple[str, object]:
    counts = [int(x) for x in re.findall(r"Frontier OPEN count: (\d+)", read(LOG))]
    ok = len(counts) >= 3 and counts == sorted(counts, reverse=True) and counts[-1] == 0
    return ("PASS" if ok else "FAIL", {"frontier_open_counts": counts, "subtractive": ok})


def check_A3() -> tuple[str, object]:
    log = read(LOG)
    rows = re.findall(r"^\| B\d+ \|", log, flags=re.MULTILINE)
    ok = "Pugh-Matrix" in log and len(rows) >= 2 and "measured" in log.lower()
    return ("PASS" if ok else "FAIL", {"pugh_rows": len(rows)})


def check_A4() -> tuple[str, object]:
    code, out = run("graph_walk.py", "--check-dag")
    payload = json_or_none(out)
    ok = code == 0 and payload.get("acyclic") is True
    return ("PASS" if ok else "FAIL", {"acyclic": payload.get("acyclic"), "digest": payload.get("digest")})


def check_A5() -> tuple[str, object]:
    canon = read(REFS / "canon.md")
    section = canon.split("## Hardware bounds used in the Crucible move", 1)
    bounds = re.findall(r"^\| (\S[^|]*?) \| ([^|]+?) \| ([^|]+?) \|$", section[1], flags=re.MULTILINE) if len(section) == 2 else []
    data = [b for b in bounds if not b[0].startswith("---") and b[0] != "Quantity"]
    figures = re.findall(r'data-figure="([a-z_]+)"', read(WEB))
    ok = len(data) >= 4 and all(b[1].strip() and b[2].strip() for b in data) and len(figures) >= 6
    return ("PASS" if ok else "FAIL", {"bound_rows": len(data), "web_figures": len(figures)})


def check_A6() -> tuple[str, object]:
    notes = read(REFS / "field-notes.md")
    rows = re.findall(r"^\| (\S+) \| (\S+) \| (\S+) \|", notes, flags=re.MULTILINE)
    ok = len(rows) >= 4 and "trust" in notes.lower() and "typestate" in notes.lower()
    return ("PASS" if ok else "FAIL", {"boundary_rows": len(rows)})


def check_A7() -> tuple[str, object]:
    code, out = run("epistemic_audit.py", "--probe", "400")
    payload = json_or_none(out)
    budget_ms = 5.0
    ok = (code == 0 and payload.get("sample_count") == 400
          and isinstance(payload.get("p99_ms"), (int, float))
          and payload.get("p99_ms") < budget_ms
          and payload.get("unit") == "milliseconds")
    return ("PASS" if ok else "FAIL", {"sample_count": payload.get("sample_count"),
                                       "p99_ms": payload.get("p99_ms"),
                                       "budget_ms": budget_ms})


def check_A8() -> tuple[str, object]:
    others = [k for k in CHECKS if k != "A8"]
    statuses = {k: CHECKS[k]()[0] for k in others}
    ok = all(v == "PASS" for v in statuses.values())
    return ("PASS" if ok else "FAIL", {"passing": sum(v == "PASS" for v in statuses.values()), "total": len(statuses)})


def check_A9() -> tuple[str, object]:
    log = read(LOG)
    pole = "Operable pole" in log or "Safety pole" in log
    ok = pole and "budget" in log.lower() and "p99" in log.lower()
    return ("PASS" if ok else "FAIL", {"mode_field_named": pole, "budget_named": "budget" in log.lower(), "p99_named": "p99" in log.lower()})


def check_A10() -> tuple[str, object]:
    text = source_text()
    found = [s for s in SECRETS if s in text]
    ok = not found and tok("os", ".environ") not in text
    return ("PASS" if ok else "FAIL", {"secret_shapes_found": found, "ambient_env": tok("os", ".environ") in text})


def check_A11() -> tuple[str, object]:
    log = read(LOG)
    ok = "M-crucible" in log and "partition" in log.lower() and "max load" in log.lower() and "measured delta" in log.lower()
    return ("PASS" if ok else "FAIL", {"crucible_move": "M-crucible" in log})


def check_A12() -> tuple[str, object]:
    completed = subprocess.run(
        [PYTHON, "-I", str(ROOT / "scripts" / "validate_figures.py")],
        capture_output=True, text=True, cwd=str(ROOT), timeout=120,
    )
    payload = json_or_none(completed.stdout.strip())
    ok = completed.returncode == 0 and payload.get("all_reproducible") is True
    return ("PASS" if ok else "FAIL", {"figures": payload.get("figure_count"), "all_reproducible": payload.get("all_reproducible")})


def check_A13() -> tuple[str, object]:
    files = source_files()
    bad = [p.name for p in files if "\t" in read(p) or not read(p).startswith('"""')]
    ok = not bad and len(files) >= 6
    return ("PASS" if ok else "FAIL", {"source_files": len(files), "style_violations": bad})


def check_A14() -> tuple[str, object]:
    text = source_text()
    found = [s for s in DYNAMIC if s in text]
    ok = not found
    return ("PASS" if ok else "FAIL", {"dynamic_execution": found})


def check_A15() -> tuple[str, object]:
    files = source_files()
    names = [p.name for p in files]
    ok = len(names) == len(set(names)) and all(p.stat().st_size > 200 for p in files)
    return ("PASS" if ok else "FAIL", {"modules": names})


def check_A16() -> tuple[str, object]:
    text = read(SCRIPTS / "epistemic_audit.py")
    pure_names = ("jank_checksum", "mapping_check", "derive", "audit", "apply")
    violations = []
    for name in pure_names:
        match = re.search(rf"^def {name}\(.*?\):\n(.*?)(?=^def |\Z)", text, flags=re.MULTILINE | re.DOTALL)
        if match and any(t in match.group(1) for t in IO_TOKENS):
            violations.append(name)
    return ("PASS" if not violations else "FAIL", {"io_in_pure_core": violations})


def check_A17() -> tuple[str, object]:
    found = [p.name for p in source_files() if any(m in read(p) for m in DEFER)]
    return ("PASS" if not found else "FAIL", {"deferral_markers": found})


def check_A18() -> tuple[str, object]:
    canon = read(REFS / "canon.md")
    rows = re.findall(r"^\| (.+?) \| (.+?) \| (.+?) \|$", canon, flags=re.MULTILINE)
    data = [r for r in rows if r[0] not in ("Label", "---", "Quantity")]
    cited = [r for r in data if "http" in r[1] or "local:" in r[1] or "chapter" in r[1].lower()]
    empty = [r[0] for r in data if not r[2].strip()]
    ok = len(cited) >= 40 and not empty
    return ("PASS" if ok else "FAIL", {"provenance_rows": len(cited), "empty_provenance": empty[:5]})


def check_A19() -> tuple[str, object]:
    code, out = run("epistemic_audit.py", "--payload", "state/clean.json", "--replay")
    payload = json_or_none(out)
    ok = code == 0 and payload.get("replay") == "idempotent" and payload.get("composition") == "f(f(x)) = f(x)"
    return ("PASS" if ok else "FAIL", {"replay": payload.get("replay"), "composition": payload.get("composition")})


def check_A20() -> tuple[str, object]:
    prd = ROOT / ".gm" / "prd"
    files = sorted(prd.glob("*.yml")) if prd.exists() else []
    named = [p.name for p in files if re.search(r"^session_id:\s*\S+", read(p), flags=re.MULTILINE)]
    log = ROOT / ".gm" / "prd-log.jsonl"
    resolved = 0
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            try:
                if json.loads(line).get("id", "").startswith("quorum-"):
                    resolved += 1
            except ValueError:
                continue
    panel = ROOT / "panel"
    verdicts = sorted(panel.glob("R*/*.md")) if panel.exists() else []
    paths = [p.relative_to(panel).as_posix() for p in verdicts]
    ok = len(named) == len(files) and len(paths) == len(set(paths)) and len(verdicts) >= 10 and resolved >= 10
    return ("PASS" if ok else "FAIL", {"open_prd_rows": len(files), "owned": len(named),
                                       "resolved_log_rows": resolved, "panel_verdict_files": len(verdicts)})


def check_A21() -> tuple[str, object]:
    text = source_text()
    found = [s for s in SHARED if s in text]
    return ("PASS" if not found else "FAIL", {"shared_state_tokens": found})


def check_A22() -> tuple[str, object]:
    batches = re.findall(r"Batch \d+: (\d+) seats", read(LOG))
    ok = len(batches) >= 3 and all(int(b) <= 3 for b in batches)
    return ("PASS" if ok else "FAIL", {"batches": batches})


def check_A23() -> tuple[str, object]:
    code, out = run("epistemic_audit.py", "--payload", "state/clean.json", "--enumerate")
    payload = json_or_none(out)
    ok = code == 0 and payload.get("finite") is True and payload.get("assignment_count") == 8
    return ("PASS" if ok else "FAIL", {"finite": payload.get("finite"), "assignment_count": payload.get("assignment_count")})


def check_A24() -> tuple[str, object]:
    taxonomy = read(REFS / "fault-taxonomy.md")
    text = source_text()
    codes = ("JANK_DETECTED", "STATE_UNMAPPED", "SELF_REJECTED", "IO_FAULT")
    declared = all(c in taxonomy for c in codes) and "engine-internal" in taxonomy and not any(b in text for b in BARE)
    raw = read(ROOT / "state" / "clean.json")
    malformed = json.loads(raw)
    malformed["rules"] = None
    mermaid = "```mermaid\nflowchart LR\n  %% comment\n  a[\"A\"]:::x\n```"
    probes = [
        ("audit-null-rules", [PYTHON, "-I", str(SCRIPTS / "epistemic_audit.py"), "--payload", "/dev/stdin"], json.dumps(malformed)),
        ("walk-comment", [PYTHON, "-I", str(SCRIPTS / "graph_walk.py"), "--graph", "/dev/stdin", "--counts"], mermaid),
        ("audit-jank-replay", [PYTHON, "-I", str(SCRIPTS / "epistemic_audit.py"), "--payload", "state/jank-contradiction.json", "--replay"], None),
        ("audit-jank-enumerate", [PYTHON, "-I", str(SCRIPTS / "epistemic_audit.py"), "--payload", "state/jank-contradiction.json", "--enumerate"], None),
    ]
    results = []
    for name, argv, stdin in probes:
        completed = subprocess.run(argv, input=stdin, capture_output=True, text=True, cwd=str(ROOT), timeout=60)
        out = completed.stdout.strip()
        try:
            payload = json.loads(out)
        except ValueError:
            payload = {}
        results.append({
            "probe": name,
            "serialized": bool(payload),
            "traceback": "Traceback" in completed.stderr,
            "fault_code": payload.get("code"),
        })
    ok = declared and all(r["serialized"] and not r["traceback"] for r in results)
    for name, expect in (("audit-jank-replay", "JANK_DETECTED"), ("audit-jank-enumerate", "JANK_DETECTED")):
        row = next(r for r in results if r["probe"] == name)
        if row["fault_code"] != expect:
            ok = False
    return ("PASS" if ok else "FAIL", {"fault_codes": [c for c in codes if c in taxonomy], "bare_handlers": [b for b in BARE if b in text], "probes": results})


CHECKS = {
    "A1": check_A1, "A2": check_A2, "A3": check_A3, "A4": check_A4,
    "A5": check_A5, "A6": check_A6, "A7": check_A7, "A8": check_A8,
    "A9": check_A9, "A10": check_A10, "A11": check_A11, "A12": check_A12,
    "A13": check_A13, "A14": check_A14, "A15": check_A15, "A16": check_A16,
    "A17": check_A17, "A18": check_A18, "A19": check_A19, "A20": check_A20,
    "A21": check_A21, "A22": check_A22, "A23": check_A23, "A24": check_A24,
}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="QUORUM invariant discharge")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--axiom", type=str)
    parser.add_argument("--digest", action="store_true")
    args = parser.parse_args(argv)
    selected = list(CHECKS) if args.all or args.digest else ([args.axiom] if args.axiom else [])
    if not selected:
        print(json.dumps({"error": "no axiom selected"}, sort_keys=True))
        return 1
    rows = []
    for key in selected:
        status, measured = CHECKS[key]()
        rows.append({"axiom": key, "status": status, "measured": measured})
    if args.digest:
        print(json.dumps({
            "axiom_count": len(rows),
            "passing": sum(r["status"] == "PASS" for r in rows),
            "digest": hashlib.sha256(json.dumps(rows, sort_keys=True).encode("utf-8")).hexdigest(),
        }, sort_keys=True))
        return 0 if all(r["status"] == "PASS" for r in rows) else 1
    for row in rows:
        print(json.dumps(row, sort_keys=True))
    return 0 if all(r["status"] == "PASS" for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
