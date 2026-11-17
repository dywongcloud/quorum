# QUORUM

**Quorum-Ordered Universal Reasoning Over Unreliable Machines.** A closed-loop
formal verification sandbox for distributed systems design. It is an end-to-end
rework of [DADA](https://github.com/AnEntrypoint/dada) for distributed systems
theory, infrastructure, edge computing, fault tolerance and decentralization.

DADA traverses an anchor graph of graphic-design literature with a panel of art
critics. QUORUM keeps the machinery and replaces the domain: 401 nodes drawn
from the SRE books, Designing Data-Intensive Applications, the impossibility
results, the systems papers, the operations canon, and formal verification;
52 adversarial critic seats; and a graph walk whose stop conditions include a
chaos crucible and a replay idempotence proof.

## What is different from DADA

| DADA | QUORUM |
|---|---|
| Graphic design at maximum ambition | Distributed systems design under failure |
| Autonomous / Adaptive modes | Fail-Closed / Graceful modes |
| Inner necessity vs MAYA | Invariant discharge vs Bounded Optimism (p99 budget) |
| 302 art-literature anchors | 401 distributed-systems anchors |
| Art critics (Greenberg, Barthes, Papanek) | Authorities (Fischer, Lynch, Paterson, Lamport, Kleppmann, Star) |
| `DESIGN-LOG.md`, five artifacts | `QUORUM-LOG.md`, five artifacts |
| Measurement of contrast and pixel counts | Measurement of graph counts, digests, p99 and quorum certificates |
| No machine-checkable contract | `EPISTEMIC_AUDIT_DAEMON` with four fault codes and 24 dischargeable axioms |

## The daemon contract

The `EPISTEMIC_AUDIT_DAEMON` ingests a `STATE_PAYLOAD` and a `QUERY_VECTOR` and
runs: pre-flight jank checksum, strict 1:1 state mapping, boolean derivation,
meta-cognitive loopback (self-falsification), serialized output, termination.
Its output port accepts JSON, YAML or rigid Markdown tables only. The faults are
`[FAULT: JANK_DETECTED]`, `[FAULT: STATE_UNMAPPED]`,
`[FAULT: SELF_REJECTED]`, and `[FAULT: IO_FAULT]`. Read
[the fault taxonomy](skills/quorum/references/fault-taxonomy.md).

## Install

```sh
python3 -I tools/install.py ~/.claude/skills/quorum
```

The skill is repo-wide. `skills/quorum/` carries the graph, the engine and the
references; the state payloads, panel verdicts, validators, landing page and
run log live beside it under `state/`, `panel/`, `scripts/`, `tools/`, `web/`,
`analysis/` and `QUORUM-LOG.md`. Copying `skills/quorum/` alone leaves the
runtime data plane behind. `tools/install.py` installs both halves, preserves
the root `SKILL.md` link, refuses to overwrite a non-empty target, and never
copies local session state, git metadata or caches. `scripts/validate_install.py`
performs that install into a fresh temporary directory and runs all 24 axiom
discharges from a foreign working directory; that live run is the portability
witness.

Once the repository is published, the skills CLI form is
`npx skills add <owner>/quorum -s quorum`; that URL is not claimed as an
existing remote in this checkout.

Invoke `$quorum` with a design brief. The skill writes five artifacts to
`QUORUM-LOG.md`: Traversal Plan with a living Frontier, Decision Records, Panel
Reports, Anchor Ledger, and Compliance Check.

## Use

```sh
python3 -I skills/quorum/scripts/graph_walk.py --counts
python3 -I skills/quorum/scripts/graph_walk.py --frontier --visited flp,gilbert,paxos
python3 -I skills/quorum/scripts/graph_walk.py --roster --mode fail-closed
python3 -I skills/quorum/scripts/epistemic_audit.py --payload state/clean.json
python3 -I skills/quorum/scripts/epistemic_audit.py --payload state/clean.json --replay
python3 -I skills/quorum/scripts/collect_panel.py panel/R1 --roster fail-closed --json
```

`state/` holds 11 payloads: one clean derivation, a maximum-load chain, an FLP
bound, a partition, a model counterexample, the encoded initiating brief, and
one input for each fault code. None is a test fixture; each is a real input to
the daemon.

## Validation

```sh
python3 -I scripts/validate_skills.py
python3 -I scripts/validate_graph.py
python3 -I scripts/validate_figures.py
python3 -I skills/quorum/scripts/verify_invariants.py --all
```

All four run in CI on push and pull request. `validate_graph.py` regenerates the
anchor graph in memory and compares it byte for byte with the checked-in file.
`validate_figures.py` recomputes every number printed on the landing page at
final state. `verify_invariants.py` discharges all 24 axioms.

## Sources

[The canon](skills/quorum/references/canon.md) names the source and provenance
of every anchor. The two primary books were downloaded and their tables of
contents and relevant chapters read during the build:

- [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) (Beyer, Jones, Petoff, Murphy)
- [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) (Kleppmann)

## Stated assumptions

The initiating brief describes an `EPISTEMIC_AUDIT_DAEMON` running in a
deterministic sandbox isolated from external networks. This repository
implements that contract as the artifact's runtime; the build session itself
used external sources to establish the canon. The brief's invariant set is
encoded as 24 dischargeable axioms in
[the invariant ledger](skills/quorum/references/invariant-ledger.md).
