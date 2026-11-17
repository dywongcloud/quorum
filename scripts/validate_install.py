"""Witness that the QUORUM skill runs outside the source checkout.

    python3 -I scripts/validate_install.py

Installs the distributable into a fresh temporary directory with
`tools/install.py`, then runs the installed `verify_invariants.py --all` from
a foreign working directory, with no access to the source repository. Every
axiom must PASS and no child may emit a traceback or an uncaught decode error.
The temporary install is removed by the context manager.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
PY = sys.executable


def run(argv: list[str], cwd: pathlib.Path) -> subprocess.CompletedProcess:
    return subprocess.run([PY, "-I", *argv], cwd=str(cwd), capture_output=True,
                          text=True, timeout=300)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="quorum-install-") as scratch:
        base = pathlib.Path(scratch)
        target = base / "home" / ".claude" / "skills" / "quorum"
        foreign = base / "elsewhere"
        foreign.mkdir(parents=True)
        installed = run([str(ROOT / "tools" / "install.py"), str(target)], foreign)
        axioms = run([str(target / "skills" / "quorum" / "scripts" / "verify_invariants.py"),
                      "--all"], foreign)
        panel = run([str(target / "skills" / "quorum" / "scripts" / "collect_panel.py"),
                     "panel/R1", "--roster", "fail-closed", "--json"], foreign)
        daemon = run([str(target / "skills" / "quorum" / "scripts" / "epistemic_audit.py"),
                      "--payload", "state/clean.json"], foreign)
        rows = []
        for line in axioms.stdout.strip().splitlines():
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if str(row.get("axiom", "")).startswith("A") and row.get("axiom") != "SUPPLEMENTS":
                rows.append(row)
        status = [r["status"] for r in rows]
        tracebacks = [name for name, proc in (("install", installed), ("axioms", axioms),
                                              ("panel", panel), ("daemon", daemon))
                      if "Traceback" in proc.stderr or "JSONDecodeError" in proc.stderr]
        result = {
            "install_exit": installed.returncode,
            "installed_files": json.loads(installed.stdout)["files"] if installed.stdout.strip().startswith("{") else 0,
            "axiom_rows": len(rows),
            "axioms_passing": status.count("PASS"),
            "axiom_exit": axioms.returncode,
            "panel_exit": panel.returncode,
            "daemon_exit": daemon.returncode,
            "foreign_cwd": str(foreign),
            "tracebacks": tracebacks,
            "ok": (installed.returncode == 0 and axioms.returncode == 0
                   and panel.returncode == 0 and daemon.returncode == 0
                   and len(rows) == 24 and all(s == "PASS" for s in status)
                   and not tracebacks),
        }
        print(json.dumps(result, sort_keys=True))
        return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
