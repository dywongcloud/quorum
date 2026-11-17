"""Merge completed three-vote deep-research verdicts into the research report.

    python3 -I tools/build_research_synthesis.py <workflow-transcript-dir>

The journal records started and result entries under agent ids. Each verifier
transcript names its claim and source URL in the computed task. A claim is
reported as CONFIRMED only when three votes exist and at most one refutes it;
it is REFUTED when two or more refute it; a claim with fewer than three votes
is NOT REPORTED. Nothing is inferred from a partial vote.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPORT = ROOT / "skills" / "quorum" / "references" / "research-report.md"
OUT = ROOT / "analysis" / "research-synthesis.json"
START = "<!-- RESEARCH:START -->"
END = "<!-- RESEARCH:END -->"


def claim_and_source(transcript: pathlib.Path) -> tuple[str, str]:
    text = transcript.read_text(encoding="utf-8", errors="replace") if transcript.is_file() else ""
    task = ""
    for line in text.splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        content = str(row.get("message", {}).get("content", ""))
        if "## Claim under review" in content:
            task = content
            break
    match = re.search(
        r'## Claim under review.*?\n\s*"(.+?)"\s*\n\s*\*\*Source:\*\*\s*(\S+)',
        task, flags=re.DOTALL)
    if not match:
        return "", ""
    return match.group(1).strip(), match.group(2).strip()


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(json.dumps({"fault": "JANK_DETECTED", "reason": "transcript directory required"}, sort_keys=True))
        return 1
    base = pathlib.Path(argv[0])
    journal = base / "journal.jsonl"
    rows = [json.loads(line) for line in journal.read_text(encoding="utf-8").splitlines()]
    started = {r["agentId"]: r for r in rows if r.get("type") == "started" and r.get("phase") == "Verify"}
    results = {r["agentId"]: r.get("result") for r in rows
               if r.get("type") == "result" and isinstance(r.get("result"), dict)
               and "confidence" in r["result"]}
    groups: dict[str, dict] = {}
    for agent_id, verdict in results.items():
        claim, source = claim_and_source(base / f"agent-{agent_id}.jsonl")
        if not claim:
            continue
        group = groups.setdefault(claim, {"claim": claim, "source": source, "votes": []})
        if not group["source"] and source:
            group["source"] = source
        group["votes"].append({"confidence": verdict.get("confidence"),
                               "refuted": verdict.get("refuted") is True,
                               "counter_source": str(verdict.get("counterSource", ""))[:300]})
    confirmed = []
    refuted = []
    incomplete = []
    for group in groups.values():
        votes = group["votes"]
        n = len(votes)
        kills = sum(1 for v in votes if v["refuted"])
        row = {"claim": group["claim"], "source": group["source"],
               "votes": n, "refutations": kills}
        if n >= 3:
            (refuted if kills >= 2 else confirmed).append(row)
        else:
            incomplete.append(row)
    result = {"method": "three-vote adversarial verification; two refutations kill a claim",
              "claims_with_votes": len(groups),
              "confirmed": confirmed, "refuted": refuted,
              "not_reported": incomplete,
              "confirmed_count": len(confirmed), "refuted_count": len(refuted),
              "incomplete_count": len(incomplete)}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["## Adversarial verification result (generated)", "",
             f"Method: {result['method']}. {len(groups)} claims have at least one vote; "
             f"{len(confirmed)} confirmed, {len(refuted)} refuted, {len(incomplete)} NOT REPORTED.",
             "", "| Status | Claim | Source | Votes | Refutations |", "|---|---|---|---:|---:|"]
    for status, rows in (("CONFIRMED", confirmed), ("REFUTED", refuted), ("NOT REPORTED", incomplete)):
        for row in rows:
            claim = row["claim"].replace("|", "/").replace("\n", " ")
            lines.append(f"| {status} | {claim[:300]} | {row['source']} | {row['votes']} | {row['refutations']} |")
    log = REPORT.read_text(encoding="utf-8")
    if START in log and END in log:
        head, rest = log.split(START, 1)
        _, tail = rest.split(END, 1)
        log = head + START + "\n" + "\n".join(lines) + "\n" + END + tail
    else:
        log = log + "\n" + START + "\n" + "\n".join(lines) + "\n" + END + "\n"
    REPORT.write_text(log, encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("claims_with_votes", "confirmed_count",
                                             "refuted_count", "incomplete_count")}, sort_keys=True))
    return 0 if confirmed or refuted else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
