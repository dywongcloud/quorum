"""Validate every QUORUM skill package in skills/.

    python3 -I scripts/validate_skills.py

Checks YAML frontmatter, the interface descriptor, local reference targets, and
the workspace discovery symlink. GitHub Actions runs the same command.
"""
from __future__ import annotations

import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required: python3 -m pip install PyYAML==6.0.2")
    sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def validate(skill: pathlib.Path) -> list[str]:
    errors: list[str] = []
    entry = skill / "SKILL.md"
    if not entry.is_file():
        return [f"{entry}: missing SKILL.md"]
    text = entry.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        return [f"{entry}: YAML frontmatter required"]
    metadata = yaml.safe_load(parts[1])
    if not isinstance(metadata, dict):
        return [f"{entry}: metadata must be a mapping"]
    if metadata.get("name") != skill.name or not re.fullmatch(r"[a-z0-9-]{1,64}", skill.name):
        errors.append(f"{entry}: skill name must match its folder")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append(f"{entry}: description must contain 1 to 1024 characters")
    ui_path = skill / "agents" / "openai.yaml"
    if not ui_path.is_file():
        errors.append(f"{skill}: missing agents/openai.yaml")
    else:
        ui = yaml.safe_load(ui_path.read_text(encoding="utf-8"))
        interface = (ui or {}).get("interface", {})
        short = interface.get("short_description", "")
        if not 25 <= len(short) <= 64:
            errors.append(f"{skill}: short description must contain 25 to 64 characters")
        if "$" + skill.name not in interface.get("default_prompt", ""):
            errors.append(f"{skill}: default prompt must invoke the skill")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if "://" in target or target.startswith("#"):
            continue
        reference = (skill / target.split("#", 1)[0]).resolve()
        if not reference.is_relative_to(skill.resolve()) or not reference.is_file():
            errors.append(f"{entry}: invalid local reference {target}")
    discovery = ROOT / ".agents" / "skills" / skill.name
    if not discovery.is_symlink() or discovery.resolve() != skill.resolve():
        errors.append(f"{skill}: workspace discovery link is invalid")
    return errors


def main() -> int:
    skills = [p for p in SKILLS.iterdir() if p.is_dir()]
    if not skills:
        print("No skill packages found")
        return 1
    failures: list[str] = []
    for skill in skills:
        found = validate(skill)
        failures.extend(found)
        if not found:
            print(f"Valid skill: {skill.name}")
    for line in failures:
        print(line)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
