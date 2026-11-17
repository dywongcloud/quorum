"""Persist the completed deep-research synthesis from the workflow result.

    python3 -I tools/build_research_final.py <result-json>

The input is the workflow's own result file. The tool writes only the
synthesis fields: findings with vote and confidence, source URLs, open
questions, caveats and measured stats. It never copies agent transcripts,
machine paths, local session state or credentials. A generated section is
spliced into `research-report.md` between the FINAL markers.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPORT = ROOT / "skills" / "quorum" / "references" / "research-report.md"
OUT = ROOT / "analysis" / "research-final.json"
START = "<!-- FINAL:START -->"
END = "<!-- FINAL:END -->"


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", str(text)).strip().replace("|", "/")


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(json.dumps({"fault": "JANK_DETECTED", "reason": "workflow result path required"}, sort_keys=True))
        return 1
    source = pathlib.Path(argv[0])
    payload = json.loads(source.read_text(encoding="utf-8"))
    result = payload["result"]
    findings = [{
        "claim": clean(f["claim"]),
        "confidence": f["confidence"],
        "vote": f["vote"],
        "evidence": clean(f["evidence"])[:1600],
        "sources": f["sources"],
    } for f in result["findings"]]
    data = {
        "status": "COMPLETE",
        "source_workflow": "deep-research",
        "stats": result["stats"],
        "summary": clean(result["summary"]),
        "caveats": clean(result["caveats"]),
        "open_questions": [clean(q) for q in result["openQuestions"]],
        "findings": findings,
        "refuted_count": len(result["refuted"]),
        "unverified_count": len(result["unverified"]),
        "sources": result["sources"],
    }
    blob = json.dumps(data, sort_keys=True)
    leaked = [p for p in ("/Users/", "/tmp/", "dywong", "pass" + "word=", "BEGIN PRIVATE")
              if p in blob]
    if leaked:
        print(json.dumps({"fault": "JANK_DETECTED", "reason": "local-state leak", "patterns": leaked}, sort_keys=True))
        return 1
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = ["## Final synthesis (generated from the workflow result)", "",
             "Status: COMPLETE. " + data["summary"], "",
             "| # | Confidence | Vote | Finding | Source URLs |", "|---:|---|---|---|---|"]
    for index, finding in enumerate(findings, 1):
        urls = " ".join(finding["sources"])
        lines.append(f"| {index} | {finding['confidence']} | {finding['vote']} | "
                     f"{finding['claim'][:700]} | {clean(urls)[:500]} |")
    lines.append("")
    lines.append("### Caveats")
    lines.append("")
    lines.append(data["caveats"])
    lines.append("")
    lines.append("### Open questions")
    lines.append("")
    for index, question in enumerate(data["open_questions"], 1):
        lines.append(f"{index}. {question}")
    log = REPORT.read_text(encoding="utf-8")
    if START in log and END in log:
        head, rest = log.split(START, 1)
        _, tail = rest.split(END, 1)
        log = head + START + "\n" + "\n".join(lines) + "\n" + END + tail
    else:
        log = log + "\n" + START + "\n" + "\n".join(lines) + "\n" + END + "\n"
    REPORT.write_text(log, encoding="utf-8")
    print(json.dumps({"wrote": str(OUT), "findings": len(findings),
                      "sources": len(data["sources"]),
                      "refuted": data["refuted_count"],
                      "unverified": data["unverified_count"]}, sort_keys=True))
    return 0 if findings else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
