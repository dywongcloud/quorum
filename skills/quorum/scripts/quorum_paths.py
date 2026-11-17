"""Resolve the QUORUM runtime data plane from the package location or cwd.

    python3 -I skills/quorum/scripts/quorum_paths.py

The skill package ships the graph and the engine. The state payloads, the
panel verdicts, the landing page, the validators and the run log form a data
plane at the repository root. A bare copy of `skills/quorum/` does not carry
that plane, so every consumer resolves it by walking up from this file and
then from the current working directory. `tools/install.py` installs both
halves together; that is the supported install command.
"""
from __future__ import annotations

import json
import pathlib
import sys


def has_data_plane(base: pathlib.Path) -> bool:
    return ((base / "QUORUM-LOG.md").is_file()
            and (base / "state" / "clean.json").is_file()
            and (base / "web" / "index.html").is_file())


def candidates() -> list[pathlib.Path]:
    here = pathlib.Path(__file__).resolve()
    return [*here.parents, pathlib.Path.cwd().resolve(),
            *pathlib.Path.cwd().resolve().parents]


def data_root() -> pathlib.Path:
    seen: set[str] = set()
    for base in candidates():
        if base.as_posix() in seen:
            continue
        seen.add(base.as_posix())
        if has_data_plane(base):
            return base
    here = pathlib.Path(__file__).resolve()
    return here.parents[3]


def skill_dir() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def main(argv: list[str]) -> int:
    root = data_root()
    print(json.dumps({"data_root": root.as_posix(),
                      "complete": has_data_plane(root),
                      "skill_dir": skill_dir().as_posix()}, sort_keys=True))
    return 0 if has_data_plane(root) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
