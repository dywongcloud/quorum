"""EPISTEMIC_AUDIT_DAEMON: closed-loop boolean derivation over a bounded state.

    python3 -I skills/quorum/scripts/epistemic_audit.py --payload <file.json>
    python3 -I skills/quorum/scripts/epistemic_audit.py --payload <file.json> --replay
    python3 -I skills/quorum/scripts/epistemic_audit.py --payload <file.json> --enumerate
    python3 -I skills/quorum/scripts/epistemic_audit.py --payload <file.json> --probe 400
    python3 -I skills/quorum/scripts/epistemic_audit.py --selftest

The engine is a pure morphism over a frozen State. It emits JSON only. It has
no hidden mutation, no ambient authority, no string-built command, and no
uncaught exception. Every fault is JSON with keys fault, code, reason,
query_id, digest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import sys
import time
from dataclasses import dataclass, replace
from typing import Any

HEDGES = (
    "i think", "probably", "maybe", "it seems", "should be fine",
    "sorry", "great question", "as an ai", "roughly", "approximately",
)
TRUNCATION_MARKERS = ("." * 3, "/" * 2 + "." * 3, "<snip>", "[omitted]")
PROBE_SEED = 20261116
MAX_ENUM_VARIABLES = 12


@dataclass(frozen=True)
class Rule:
    id: str
    premises: tuple[str, ...]
    negated: tuple[str, ...]
    conclusion: str


@dataclass(frozen=True)
class State:
    variables: tuple[tuple[str, bool], ...]
    rules: tuple[Rule, ...]
    query: str
    axioms: tuple[str, ...]
    negations: tuple[str, ...]
    nodes: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
    context: tuple[tuple[str, ...], ...]
    secrets: tuple[str, ...]
    query_id: str


@dataclass(frozen=True)
class Fault:
    code: str
    reason: str
    query_id: str
    digest: str


@dataclass(frozen=True)
class Derived:
    query_id: str
    result: bool
    chain: tuple[str, ...]
    state_digest: str
    context_digest: str
    faults_cleared: tuple[str, ...]


def digest(value: Any) -> str:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def state_digest(state: State) -> str:
    return digest([
        list(state.variables),
        [[r.id, list(r.premises), list(r.negated), r.conclusion] for r in state.rules],
        state.query, list(state.axioms), list(state.negations),
        list(state.nodes), [list(e) for e in state.edges],
        [list(c) for c in state.context], list(state.secrets),
    ])


def fault_record(f: Fault) -> dict[str, Any]:
    return {
        "fault": f.code,
        "code": f.code,
        "reason": f.reason,
        "query_id": f.query_id,
        "digest": f.digest,
    }


def derived_record(d: Derived) -> dict[str, Any]:
    return {
        "derived": "true" if d.result else "false",
        "query_id": d.query_id,
        "chain": list(d.chain),
        "state_digest": d.state_digest,
        "context_digest": d.context_digest,
        "faults_cleared": list(d.faults_cleared),
    }


def parse_state(raw: Any) -> tuple[State | None, Fault | None]:
    qid = "unbound"
    if not isinstance(raw, dict):
        return None, Fault("JANK_DETECTED", "structural-decay: payload is not an object", qid, digest(raw))
    qid = str(raw.get("query_id", "unbound"))
    required = ("variables", "rules", "query", "axioms", "negations",
                "nodes", "edges", "context", "secrets")
    missing = [k for k in required if k not in raw]
    if missing:
        return None, Fault("JANK_DETECTED", f"structural-decay: missing fields {missing}", qid, digest(raw))
    variables = raw["variables"]
    if not isinstance(variables, dict):
        return None, Fault("JANK_DETECTED", "category-error: variables is not an object", qid, digest(raw))
    for name, value in variables.items():
        if not isinstance(name, str) or not isinstance(value, bool):
            return None, Fault("JANK_DETECTED", f"category-error: variable {name!r} is not boolean", qid, digest(raw))
    if not isinstance(raw["rules"], list):
        return None, Fault("JANK_DETECTED", "category-error: rules is not an array", qid, digest(raw))
    rules: list[Rule] = []
    for item in raw["rules"]:
        if not isinstance(item, dict) or not all(k in item for k in ("id", "premises", "negated", "conclusion")):
            return None, Fault("JANK_DETECTED", "category-error: malformed rule", qid, digest(raw))
        premises = item["premises"]
        negated = item["negated"]
        if not isinstance(premises, list) or not isinstance(negated, list):
            return None, Fault("JANK_DETECTED", "category-error: rule operands are not arrays", qid, digest(raw))
        if not all(isinstance(x, str) for x in premises + negated):
            return None, Fault("JANK_DETECTED", "category-error: rule operand is not a symbol", qid, digest(raw))
        rules.append(Rule(str(item["id"]), tuple(premises), tuple(negated), str(item["conclusion"])))
    for key in ("axioms", "negations", "nodes", "secrets"):
        if not isinstance(raw[key], list) or not all(isinstance(x, str) for x in raw[key]):
            return None, Fault("JANK_DETECTED", f"category-error: {key} is not a string array", qid, digest(raw))
    if not isinstance(raw["query"], str):
        return None, Fault("JANK_DETECTED", "category-error: query is not a string", qid, digest(raw))
    edges: list[tuple[str, str]] = []
    for pair in raw["edges"]:
        if not isinstance(pair, list) or len(pair) != 2 or not all(isinstance(x, str) for x in pair):
            return None, Fault("JANK_DETECTED", "category-error: edge is not a pair of symbols", qid, digest(raw))
        edges.append((pair[0], pair[1]))
    context: list[tuple[str, ...]] = []
    for frame in raw["context"]:
        if not isinstance(frame, list) or not all(isinstance(x, str) for x in frame):
            return None, Fault("JANK_DETECTED", "category-error: context frame is not a string array", qid, digest(raw))
        context.append(tuple(frame))
    state = State(
        variables=tuple(sorted(variables.items())),
        rules=tuple(rules),
        query=raw["query"],
        axioms=tuple(raw["axioms"]),
        negations=tuple(raw["negations"]),
        nodes=tuple(raw["nodes"]),
        edges=tuple(edges),
        context=tuple(context),
        secrets=tuple(raw["secrets"]),
        query_id=qid,
    )
    return state, None


def jank_checksum(state: State) -> Fault | None:
    names = [n for n, _ in state.variables]
    values = dict(state.variables)
    qid = state.query_id
    if len(names) != len(set(names)):
        return Fault("JANK_DETECTED", "structural-decay: duplicate variable declaration", qid, state_digest(state))
    if len(state.nodes) != len(set(state.nodes)):
        return Fault("JANK_DETECTED", "structural-decay: duplicate AST node id", qid, state_digest(state))
    node_set = set(state.nodes)
    for src, dst in state.edges:
        if src not in node_set or dst not in node_set:
            return Fault("JANK_DETECTED", f"structural-decay: dangling edge {src} -> {dst}", qid, state_digest(state))
    for src, dst in state.edges:
        if src not in values and src not in node_set:
            return Fault("JANK_DETECTED", f"undefined-variable: {src} has no declaration", qid, state_digest(state))
        if dst not in values and dst not in node_set:
            return Fault("JANK_DETECTED", f"undefined-variable: {dst} has no declaration", qid, state_digest(state))
    declared = set(names) | node_set | {r.conclusion for r in state.rules}
    for rule in state.rules:
        for symbol in rule.premises + rule.negated:
            if symbol not in declared:
                return Fault("JANK_DETECTED", f"undefined-variable: rule {rule.id} uses {symbol}", qid, state_digest(state))
    overlap = set(state.axioms) & set(state.negations)
    if overlap:
        return Fault("JANK_DETECTED", f"logical-contradiction: {sorted(overlap)} asserted and negated", qid, state_digest(state))
    for name in state.axioms:
        if name in values and values[name] is not True:
            return Fault("JANK_DETECTED", f"logical-contradiction: axiom {name} declared false", qid, state_digest(state))
    for name in state.negations:
        if name in values and values[name] is not False:
            return Fault("JANK_DETECTED", f"logical-contradiction: negation {name} declared true", qid, state_digest(state))
    previous: set[str] = set()
    for index, frame in enumerate(state.context):
        current = set(frame)
        if not current.issuperset(previous):
            return Fault("JANK_DETECTED", f"structural-decay: context frame {index} loses prior state", qid, state_digest(state))
        previous = current
    for secret in state.secrets:
        if secret in node_set or secret in values:
            return Fault("JANK_DETECTED", "category-error: secret appears in AST", qid, state_digest(state))
    blob = json.dumps([list(state.nodes), list(state.axioms), list(state.negations)], ensure_ascii=True)
    for marker in TRUNCATION_MARKERS:
        if marker in blob:
            return Fault("JANK_DETECTED", f"structural-decay: truncation marker {marker}", qid, state_digest(state))
    return None


def mapping_check(state: State) -> Fault | None:
    declared = {n for n, _ in state.variables} | {r.conclusion for r in state.rules} | set(state.nodes)
    if state.query not in declared:
        return Fault("STATE_UNMAPPED", f"missing variable or axiom: {state.query}", state.query_id, state_digest(state))
    for name in tuple(state.axioms) + tuple(state.negations):
        if name not in declared:
            return Fault("STATE_UNMAPPED", f"missing variable or axiom: {name}", state.query_id, state_digest(state))
    return None


def derive(state: State) -> tuple[Derived | None, Fault | None]:
    for rule in state.rules:
        if len(rule.premises) == 0 and len(rule.negated) == 0 and rule.conclusion not in state.axioms:
            return None, Fault("SELF_REJECTED", f"unstated-assumption: rule {rule.id} has no declared premise", state.query_id, state_digest(state))
    values = dict(state.variables)
    derived_set: set[str] = set(state.axioms)
    chain: list[str] = []
    changed = True
    while changed:
        changed = False
        for rule in state.rules:
            if rule.conclusion in derived_set:
                continue
            positive = all(p in derived_set or values.get(p) is True for p in rule.premises)
            negative = all(values.get(n) is False and n not in derived_set for n in rule.negated)
            if positive and negative:
                derived_set.add(rule.conclusion)
                chain.append(rule.id)
                changed = True
    result = state.query in derived_set or values.get(state.query) is True
    for rule in state.rules:
        if rule.id not in chain and rule.conclusion == state.query and result:
            return None, Fault("SELF_REJECTED", f"logical-leap: {state.query} asserted without rule {rule.id}", state.query_id, state_digest(state))
    if any(not isinstance(value, bool) for value in values.values()):
        return None, Fault("SELF_REJECTED", "probabilistic-guessing: non-boolean valuation", state.query_id, state_digest(state))
    return Derived(
        query_id=state.query_id,
        result=result,
        chain=tuple(chain),
        state_digest=state_digest(state),
        context_digest=digest([list(c) for c in state.context]),
        faults_cleared=("JANK_DETECTED", "STATE_UNMAPPED", "SELF_REJECTED", "IO_FAULT"),
    ), None


def audit(state: State) -> dict[str, Any]:
    for check in (jank_checksum, mapping_check):
        problem = check(state)
        if problem is not None:
            return fault_record(problem)
    outcome, problem = derive(state)
    if problem is not None:
        return fault_record(problem)
    if outcome is None:
        return fault_record(Fault("SELF_REJECTED", "derivation produced no result", state.query_id, state_digest(state)))
    record = derived_record(outcome)
    text = json.dumps(record, sort_keys=True).lower()
    for hedge in HEDGES:
        if hedge in text:
            return fault_record(Fault("IO_FAULT", f"unserialized or affective token: {hedge}", state.query_id, state_digest(state)))
    return record


def apply(state: State) -> State:
    """f: State -> State. Pure and idempotent: applying f twice is f once."""
    if jank_checksum(state) is not None or mapping_check(state) is not None:
        return state
    outcome, problem = derive(state)
    if problem is not None or outcome is None:
        return state
    last = set(state.context[-1]) if state.context else set()
    if not outcome.result or state.query in last:
        return state
    return replace(state, context=state.context + (tuple(sorted(last | {state.query})),))


def load_payload(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sample_payload(seed: int, index: int) -> dict[str, Any]:
    rng = random.Random(seed + index)
    return {
        "query_id": f"probe-{index}",
        "variables": {"p": rng.choice((True, False)), "q": True, "r": False},
        "rules": [
            {"id": "R1", "premises": ["p", "q"], "negated": [], "conclusion": "s"},
            {"id": "R2", "premises": ["s"], "negated": ["r"], "conclusion": "t"},
        ],
        "query": "t",
        "axioms": ["q"],
        "negations": ["r"],
        "nodes": ["p", "q", "r", "s", "t"],
        "edges": [["p", "s"], ["s", "t"]],
        "context": [["p"], ["p", "q"]],
        "secrets": [],
    }


def probe(samples: int) -> dict[str, Any]:
    timings: list[float] = []
    for index in range(samples):
        payload = sample_payload(PROBE_SEED, index)
        state, problem = parse_state(payload)
        if problem is not None:
            continue
        if state is None:
            continue
        started = time.perf_counter()
        audit(state)
        timings.append((time.perf_counter() - started) * 1000.0)
    timings.sort()
    rank = max(0, min(len(timings) - 1, int(0.99 * len(timings))))
    return {
        "probe": "monte-carlo-derivation-latency",
        "seed": PROBE_SEED,
        "sample_count": len(timings),
        "p99_ms": round(timings[rank], 4) if timings else None,
        "min_ms": round(timings[0], 4) if timings else None,
        "max_ms": round(timings[-1], 4) if timings else None,
        "unit": "milliseconds",
    }


def enumerate_space(state: State) -> dict[str, Any]:
    names = [n for n, _ in state.variables]
    if len(names) > MAX_ENUM_VARIABLES:
        return {"finite": False, "reason": f"variable count {len(names)} exceeds bound {MAX_ENUM_VARIABLES}"}
    reachable: set[str] = set()
    for mask in range(1 << len(names)):
        assignment = tuple((name, bool(mask & (1 << i))) for i, name in enumerate(names))
        candidate = replace(state, variables=tuple(sorted(assignment)))
        outcome, _ = derive(candidate)
        reachable.add(digest(bool(outcome is not None and outcome.result)))
    return {
        "finite": True,
        "assignment_count": 1 << len(names),
        "reachable_result_states": len(reachable),
        "variable_count": len(names),
        "bound": MAX_ENUM_VARIABLES,
    }


def selftest() -> dict[str, Any]:
    cases: list[tuple[str, dict[str, Any], str]] = []
    good = sample_payload(PROBE_SEED, 0)
    cases.append(("clean", good, "derived"))
    contradiction = json.loads(json.dumps(good))
    contradiction["negations"] = ["r", "q"]
    cases.append(("contradiction", contradiction, "JANK_DETECTED"))
    unmapped = json.loads(json.dumps(good))
    unmapped["query"] = "absent_symbol"
    cases.append(("unmapped", unmapped, "STATE_UNMAPPED"))
    assumption = json.loads(json.dumps(good))
    assumption["rules"] = [{"id": "R9", "premises": [], "negated": [], "conclusion": "s"}]
    cases.append(("unstated-assumption", assumption, "SELF_REJECTED"))
    decay = json.loads(json.dumps(good))
    decay["edges"] = [["p", "ghost"]]
    cases.append(("dangling-edge", decay, "JANK_DETECTED"))
    results: list[dict[str, Any]] = []
    for name, payload, expected in cases:
        state, problem = parse_state(payload)
        record = fault_record(problem) if problem is not None else audit(state)  # type: ignore[arg-type]
        actual = record.get("code") or ("derived" if "derived" in record else "unknown")
        results.append({"case": name, "expected": expected, "actual": actual, "pass": actual == expected})
    return {"selftest": "epistemic_audit", "cases": results, "all_pass": all(r["pass"] for r in results)}


def guarded_main(argv: list[str]) -> int:
    try:
        return main(argv)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(json.dumps(fault_record(Fault(
            "JANK_DETECTED", f"engine-internal: {type(exc).__name__}", "unbound", digest(None)
        )), sort_keys=True))
        return 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="QUORUM epistemic audit daemon")
    parser.add_argument("--payload", type=str)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--enumerate", action="store_true")
    parser.add_argument("--probe", type=int)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        print(json.dumps(selftest(), sort_keys=True))
        return 0
    if args.probe is not None:
        if args.probe < 1:
            print(json.dumps(fault_record(Fault("IO_FAULT", "probe sample count must be positive", "probe", digest(args.probe))), sort_keys=True))
            return 1
        print(json.dumps(probe(args.probe), sort_keys=True))
        return 0
    if args.payload is None:
        print(json.dumps(fault_record(Fault("IO_FAULT", "no payload path supplied", "unbound", digest(None))), sort_keys=True))
        return 1
    path = pathlib.Path(args.payload)
    try:
        raw = load_payload(path)
    except (OSError, ValueError) as exc:
        print(json.dumps(fault_record(Fault("JANK_DETECTED", f"engine-internal: {type(exc).__name__}", "unbound", digest(None))), sort_keys=True))
        return 1
    state, problem = parse_state(raw)
    if problem is not None or state is None:
        print(json.dumps(fault_record(problem or Fault("JANK_DETECTED", "parse failed", "unbound", digest(raw))), sort_keys=True))
        return 1
    preflight = jank_checksum(state) or mapping_check(state)
    if preflight is not None:
        print(json.dumps(fault_record(preflight), sort_keys=True))
        return 1
    if args.enumerate:
        print(json.dumps(enumerate_space(state), sort_keys=True))
        return 0
    first = audit(state)
    if args.replay:
        second = audit(state)
        result = {
            "replay": "idempotent" if digest(first) == digest(second) else "non-idempotent",
            "first_digest": digest(first),
            "second_digest": digest(second),
            "composition": "f(f(x)) = f(x)" if state_digest(apply(apply(state))) == state_digest(apply(state)) else "composition-diverges",
        }
        print(json.dumps(result, sort_keys=True))
        return 0
    print(json.dumps(first, sort_keys=True))
    return 0 if "derived" in first else 1


if __name__ == "__main__":
    sys.exit(guarded_main(sys.argv[1:]))
