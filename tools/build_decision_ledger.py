"""Build the repo-internal decision ledger from the committed run log.

    python3 -I tools/build_decision_ledger.py

A decision record is complete when QUORUM-LOG.md names its anchors, intent,
formal argument, state delta, invariant obligations, alternatives, consequence,
fence and frontier effect. The ledger carries no local session state and no
machine configuration: every field is read from the committed log. Axiom A20
consumes the ledger so a fresh checkout can discharge without a local store.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOG = ROOT / "QUORUM-LOG.md"
OUT = ROOT / "analysis" / "decision-ledger.json"
FIELDS = ("Depends on", "Anchors", "Intent", "Formal argument", "State delta",
          "Invariant obligations", "Alternatives rejected", "Consequence",
          "Fence", "Frontier effect")


def records(text: str) -> list[dict]:
    parts = re.split(r"^### Move (M\d+): (.+)$", text, flags=re.M)
    rows = []
    for index in range(1, len(parts), 3):
        move_id, title, body = parts[index], parts[index + 1], parts[index + 2]
        present = [name for name in FIELDS
                   if re.search(r"^" + re.escape(name) + r":", body, flags=re.M)]
        obligations = re.search(r"^Invariant obligations:\s*(.+)$", body, flags=re.M)
        rows.append({
            "id": move_id,
            "title": title.strip(),
            "fields_present": present,
            "missing_fields": [name for name in FIELDS if name not in present],
            "obligations": [x.strip() for x in obligations.group(1).split(",")] if obligations else [],
            "complete": len(present) == len(FIELDS),
            "body_digest": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        })
    return rows


def main() -> int:
    rows = records(LOG.read_text(encoding="utf-8"))
    data = {
        "source": "QUORUM-LOG.md, Artifact 2. Decision Records",
        "required_fields": list(FIELDS),
        "rows": rows,
        "row_count": len(rows),
        "complete_rows": sum(1 for row in rows if row["complete"]),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(OUT), **{k: data[k] for k in ("row_count", "complete_rows")}},
                     sort_keys=True))
    return 0 if rows and data["complete_rows"] == data["row_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
