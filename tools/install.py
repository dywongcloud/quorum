"""Install the QUORUM distributable into a target skills directory.

    python3 -I tools/install.py /path/to/target

The skill is repo-wide: the graph, the state payloads, the validators, the
panel verdicts, the generated analyses and the run log all live outside
`skills/quorum/`. Copying only that directory would leave the runtime data
plane behind. This tool copies the whole distributable tree, preserves the
root SKILL.md link, and refuses to overwrite a non-empty target. It never
copies local session state, git metadata, caches or credentials.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOP_LEVEL = (
    "SKILL.md", "references", "README.md", "AGENTS.md", "QUORUM-LOG.md",
    "QUORUM-CARRY-FORWARD.md", ".gitignore", "skills", "scripts", "tools",
    "state", "web", "panel", "analysis", ".github", ".agents",
)
EXCLUDED = (".git", ".gm", ".agentplug", ".agentplug-kv", "__pycache__",
            ".verify_2310_01798", ".DS_Store")


def ignore(_directory: str, names: list[str]) -> list[str]:
    return [name for name in names
            if name in EXCLUDED or name.startswith(".agentplug")
            or name.endswith(".pyc") or name.startswith(".") and name not in (".github", ".agents")]


def manifest(target: pathlib.Path) -> dict:
    rows = []
    for path in sorted(target.rglob("*")):
        if path.is_symlink():
            rows.append((path.relative_to(target).as_posix(), "link:" + path.readlink().as_posix()))
        elif path.is_file():
            rows.append((path.relative_to(target).as_posix(),
                         hashlib.sha256(path.read_bytes()).hexdigest()))
    return {"files": len(rows),
            "digest": hashlib.sha256(json.dumps(rows, sort_keys=True).encode("utf-8")).hexdigest()}


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(json.dumps({"fault": "JANK_DETECTED", "reason": "one target directory required"}, sort_keys=True))
        return 1
    target = pathlib.Path(argv[0]).expanduser().resolve()
    if target == ROOT:
        print(json.dumps({"fault": "JANK_DETECTED", "reason": "target is the source repository"}, sort_keys=True))
        return 1
    if target.exists() and any(target.iterdir()):
        print(json.dumps({"fault": "JANK_DETECTED", "reason": "target is non-empty, no overwrite"}, sort_keys=True))
        return 1
    target.mkdir(parents=True, exist_ok=True)
    copied = 0
    for name in TOP_LEVEL:
        source = ROOT / name
        if not source.exists():
            continue
        destination = target / name
        if source.is_symlink():
            shutil.copy2(source, destination, follow_symlinks=False)
        elif source.is_dir():
            shutil.copytree(source, destination, symlinks=True, ignore=ignore)
        else:
            shutil.copy2(source, destination)
        copied += 1
    print(json.dumps({"target": str(target), "top_level_entries": copied, **manifest(target)},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
