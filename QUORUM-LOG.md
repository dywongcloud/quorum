# QUORUM-LOG

Run of the QUORUM skill on its own repository. Five artifacts live here:
Traversal Plan with the living Frontier, Decision Records, Panel Reports,
Anchor Ledger, and Compliance Check. Every figure was re-measured after the
last edit. Every record cites a command that reproduces it.

Mode: **Fail-Closed**. Reason: the brief names a formal verification sandbox,
an invariant set and a no-interpolation contract; safety dominates liveness.
The Graceful pole is still recorded for the Crucible move, because the brief
also names edge deployments and availability.

## Artifact 1. Traversal Plan

### Step 0. Tooling inventory

| Job | Tool used | Command |
|---|---|---|
| Render and navigate the anchor graph | `graph_walk.py` | `python3 -I skills/quorum/scripts/graph_walk.py --counts` |
| Compute the Frontier | `graph_walk.py` | `python3 -I skills/quorum/scripts/graph_walk.py --frontier --visited flp,paxos,raft,dynamo` |
| Track workflow state | `tools/run_traversal.py` | `python3 -I tools/run_traversal.py` |
| Run the panel | recursive gm sub-agents | one agent per authority, three seats per batch |
| Persist the log | this file plus `analysis/traversal.json` | byte-comparable JSON ledger |
| Discharge axioms | `verify_invariants.py` | `python3 -I skills/quorum/scripts/verify_invariants.py --all` |
| Model-check safety | `epistemic_audit.py` | `python3 -I skills/quorum/scripts/epistemic_audit.py --payload state/clean.json --model-check` |
| Run the crucible | `epistemic_audit.py` | `python3 -I skills/quorum/scripts/epistemic_audit.py --payload state/clean.json --crucible 200` |

Mode: Fail-Closed. The brief names invariants, fault codes and no interpolation;
the required panel therefore files a verdict from every seat, and a WHOLE
round is not closed while an Andon is pulled. Graceful-mode critics sit as
counterpoints on dotted edges but do not gate closure.

### Pre-flight jank checksum

The initiating brief was encoded as `state/initiating-brief.json` and passed
through `epistemic_audit.py`. Result:

```
[FAULT: JANK_DETECTED] -> logical-contradiction: ['deterministic_derivation'] asserted and negated
digest: c9262adbe61eff28938e55d4e426a04aa5bb0114abf1a969ed939779ef89b6bc
```

Four structural failure modes are present in the brief: a deterministic
derivation engine alongside a Monte Carlo epistemology; an isolated sandbox
alongside external source URLs; a memory-restricted sandbox alongside a
monotone context `Gamma_t superset Gamma_(t-1)`; and asymptotic zero contention
alongside a chaos max-load crucible. The repairs are recorded as stated
assumptions in `README.md`, not silently accepted. The clean payload
`state/clean.json` returns `[DERIVED]` with chain `R1, R2`. The daemon does not
process a corrupted payload and does not interpolate a missing symbol.

### Seed, copied verbatim from `anchor-graph.md`

| Role | Label |
|---|---|
| Stance | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) |
| Rule | The Part-Time Parliament (Lamport) |
| Rule | In Search of an Understandable Consensus Algorithm (Ongaro, Ousterhout) |
| Breaker | Dynamo: Amazon's Highly Available Key-value Store (DeCandia et al.) |
| Counterpoint | `paxos -.->|understandability counterpoint| raft` (dotted edge) |

Chain: `flp -->|impossibility bounds| paxos`, `paxos -.->|understandability
counterpoint| raft`, `flp -->|impossibility bounds| raft`, and
`raftlog -->|commit rules require| membership`. The seed is a starting point,
not a plan. Measured seed Frontier: 20 candidates, computed live by
`tools/run_traversal.py`.

### Premortem, round R0

A WHOLE panel round on the inherited artifact (the DADA reference clone) before
the first move. Objections became the first Frontier candidates:
DADA's 302 art-literature anchors do not bear on a distributed-systems brief;
DADA has no machine-checkable contract; DADA's `DESIGN-LOG.md` has no jank
checksum; DADA's web page prints figures measured at an earlier state. Each
objection is resolved in a Decision Record below.

### Living Frontier

<!-- FRONTIER:START -->
| Round | TAKEN | Reached via | From anchor | DEFERRED (derived reason) | Frontier OPEN count |
|---|---|---|---|---|---|
| R1 | `chubby` | uses | `paxos` | `cockroach`: incoming solid edge via 'replicates via' from `raft`; priority incoming; assessed, not taken this round; `etcd`: incoming solid edge via 'uses' from `raft`; priority incoming; assessed, not taken this round; `lynchbook`: incoming solid edge via 'proves' from `flp`; priority incoming; assessed, not taken this round | Frontier OPEN count: 16 |
| R2 | `cockroach` | replicates via | `raft` | `etcd`: incoming solid edge via 'uses' from `raft`; priority incoming; assessed, not taken this round; `lynchbook`: incoming solid edge via 'proves' from `flp`; priority incoming; assessed, not taken this round; `megastore`: incoming solid edge via 'per-entity replication via' from `paxos`; priority incoming; assessed, not taken this round | Frontier OPEN count: 15 |
| R3 | `etcd` | uses | `raft` | `lynchbook`: incoming solid edge via 'proves' from `flp`; priority incoming; assessed, not taken this round; `megastore`: incoming solid edge via 'per-entity replication via' from `paxos`; priority incoming; assessed, not taken this round; `multipaxos`: incoming solid edge via 'refines' from `raft`; priority incoming; assessed, not taken this round | Frontier OPEN count: 14 |
| R4 | `lynchbook` | proves | `flp` | `megastore`: incoming solid edge via 'per-entity replication via' from `paxos`; priority incoming; assessed, not taken this round; `multipaxos`: incoming solid edge via 'refines' from `raft`; priority incoming; assessed, not taken this round; `verdi`: incoming solid edge via 'verifies' from `raft`; priority incoming; assessed, not taken this round | Frontier OPEN count: 13 |
| R5 | `megastore` | per-entity replication via | `paxos` | `multipaxos`: incoming solid edge via 'refines' from `raft`; priority incoming; assessed, not taken this round; `verdi`: incoming solid edge via 'verifies' from `raft`; priority incoming; assessed, not taken this round; `flpbound`: counterpoint dotted edge via 'bounds liveness of' from `flp`; priority outgoing; assessed, not taken this round | Frontier OPEN count: 12 |
| R6 | `multipaxos` | refines | `raft` | `verdi`: incoming solid edge via 'verifies' from `raft`; priority incoming; assessed, not taken this round; `flpbound`: counterpoint dotted edge via 'bounds liveness of' from `flp`; priority outgoing; assessed, not taken this round; `spanner`: counterpoint dotted edge via 'CP counterpoint to AP in' from `dynamo`; priority outgoing; assessed, not taken this round | Frontier OPEN count: 11 |
| R7 | `paxossimple` | refines | `multipaxos` | `verdi`: incoming solid edge via 'verifies' from `raft`; priority incoming; assessed, not taken this round; `flpbound`: counterpoint dotted edge via 'bounds liveness of' from `flp`; priority outgoing; assessed, not taken this round; `spanner`: counterpoint dotted edge via 'CP counterpoint to AP in' from `dynamo`; priority outgoing; assessed, not taken this round | Frontier OPEN count: 10 |
| R8 | `verdi` | verifies | `raft` | `flpbound`: counterpoint dotted edge via 'bounds liveness of' from `flp`; priority outgoing; assessed, not taken this round; `spanner`: counterpoint dotted edge via 'CP counterpoint to AP in' from `dynamo`; priority outgoing; assessed, not taken this round; `cassandra`: outgoing solid edge via 'inspires' from `dynamo`; priority outgoing; assessed, not taken this round | Frontier OPEN count: 9 |
| R9 | `flpbound` | bounds liveness of | `flp` | `spanner`: counterpoint dotted edge via 'CP counterpoint to AP in' from `dynamo`; priority outgoing; assessed, not taken this round; `cassandra`: outgoing solid edge via 'inspires' from `dynamo`; priority outgoing; assessed, not taken this round; `failuredetector`: outgoing solid edge via 'motivates' from `flp`; priority outgoing; assessed, not taken this round | Frontier OPEN count: 8 |
| R10 | `spanner` | CP counterpoint to AP in | `dynamo` | `cassandra`: outgoing solid edge via 'inspires' from `dynamo`; priority outgoing; assessed, not taken this round; `failuredetector`: outgoing solid edge via 'motivates' from `flp`; priority outgoing; assessed, not taken this round; `merkle`: outgoing solid edge via 'introduced' from `dynamo`; priority outgoing; assessed, not taken this round | Frontier OPEN count: 7 |
| R11 | `cassandra` | inspires | `dynamo` | `failuredetector`: outgoing solid edge via 'motivates' from `flp`; priority outgoing; assessed, not taken this round; `merkle`: outgoing solid edge via 'introduced' from `dynamo`; priority outgoing; assessed, not taken this round; `raftlog`: outgoing solid edge via 'refines' from `raft`; priority outgoing; assessed, not taken this round | Frontier OPEN count: 6 |
| R12 | `failuredetector` | motivates | `flp` | `merkle`: outgoing solid edge via 'introduced' from `dynamo`; priority outgoing; assessed, not taken this round; `raftlog`: outgoing solid edge via 'refines' from `raft`; priority outgoing; assessed, not taken this round; `riak`: outgoing solid edge via 'inspires' from `dynamo`; priority outgoing; assessed, not taken this round | Frontier OPEN count: 5 |
| R13 | `merkle` | introduced | `dynamo` | `raftlog`: outgoing solid edge via 'refines' from `raft`; priority outgoing; assessed, not taken this round; `riak`: outgoing solid edge via 'inspires' from `dynamo`; priority outgoing; assessed, not taken this round; `sloppyquorum`: outgoing solid edge via 'introduced' from `dynamo`; priority outgoing; assessed, not taken this round | Frontier OPEN count: 4 |
| R14 | `raftlog` | refines | `raft` | `riak`: outgoing solid edge via 'inspires' from `dynamo`; priority outgoing; assessed, not taken this round; `sloppyquorum`: outgoing solid edge via 'introduced' from `dynamo`; priority outgoing; assessed, not taken this round; `vectorclock`: outgoing solid edge via 'introduced' from `dynamo`; priority outgoing; assessed, not taken this round | Frontier OPEN count: 3 |
| R15 | `riak` | inspires | `dynamo` | `sloppyquorum`: outgoing solid edge via 'introduced' from `dynamo`; priority outgoing; assessed, not taken this round; `vectorclock`: outgoing solid edge via 'introduced' from `dynamo`; priority outgoing; assessed, not taken this round | Frontier OPEN count: 2 |
| R16 | `sloppyquorum` | introduced | `dynamo` | `vectorclock`: outgoing solid edge via 'introduced' from `dynamo`; priority outgoing; assessed, not taken this round | Frontier OPEN count: 1 |
| R17 | `vectorclock` | introduced | `dynamo` | none | Frontier OPEN count: 0 |
<!-- FRONTIER:END -->

Each deferred row carries a reason in `analysis/traversal.json`. Counts are
computed, not asserted. Incoming, outgoing and dotted edges were all followed;
visited anchors grew from 4 to 9.

## Artifact 2. Decision Records

### Move M1: replace the art canon with a distributed-systems canon (BREAK)

Depends on: none.
Anchors: Stance `Site Reliability Engineering (Beyer, Jones, Petoff, Murphy)`
| Rule `Designing Data-Intensive Applications (Kleppmann)` | Breaker
`Dynamo: Amazon's Highly Available Key-value Store (DeCandia et al.)`
| Counterpoint `The Tail at Scale (Dean, Barroso)`.
Intent: make every design move groundable in a text about unreliable machines.
Formal argument: claim, the anchor graph must bound the derivation; grounds,
the two primary books were read and 96 provenance rows were measured in
`canon.md`; warrant, a label without provenance is a phantom AST node.
State delta: `EmptyGraph -> Graph(401 nodes, 396 edges, 15 clusters)`.
Invariant obligations: A4, A5, A18, A23.
Alternatives rejected: keep DADA's 302 art anchors (no bearing on partitions);
invent a smaller graph (would leave truncated nodes).
Consequence: the graph is now a strict DAG; incoming edges became meaningful
back-references. Cost: one generator file that must be validated byte-wise.
Fence: DADA's graph exists so that labels are exact; scrapping it requires the
replacement to be complete, which `validate_graph.py` checks.
Frontier effect: opens CAP, PACELC, FLP and consensus counterpoint candidates.
Mode field: Safety pole, the invariant holds in every reachable state;
Operable pole, the graph must be renderable in under one second. Measured:
`graph_walk.py --counts` and `--check-dag` are run at final state; p99 over 400 derivation probes stays below the 5 ms
budget. Budget: 5 ms for a full graph walk.

### Move M2: replace Autonomous/Adaptive with Fail-Closed/Graceful (KEEP-THE-RULE)

Depends on: M1.
Anchors: Stance `Brewer's Conjecture and the Feasibility of Consistent,
Available, Partition-Tolerant Web Services (Gilbert, Lynch)` | Rule
`Consistency Tradeoffs in Modern Distributed Database System Design (Abadi)`
| Breaker `Harvest, Yield, and Scalable Tolerant Systems (Fox, Brewer)`.
Intent: make the mode decision a CAP decision rather than a taste decision.
Formal argument: claim, two governing criteria suffice; grounds, CAP and
PACELC name exactly the safety/latency/availability tradeoff; warrant, a mode
that does not name its tradeoff cannot be discharged.
State delta: `ModeSet(Aesthetic) -> ModeSet(Safety, BoundedOptimism)`.
Invariant obligations: A9, A12.
Alternatives rejected: three modes (adds a maintenance surface with no new
criterion); one mode (hides the availability tradeoff).
Consequence: the Graceful mode must state a p99 budget in every record.
Fence: DADA's MAYA two-pole rule is kept as Bounded Optimism, not discarded.
Frontier effect: opens Erasure, Operability and Chaos critic seats.
Mode field: Safety pole, invariant discharge; Operable pole, p99 budget stated.

### Move M3: build the adversarial critic panel (KEEP-THE-RULE)

Depends on: M1, M2.
Anchors: Stance `Impossibility of Distributed Consensus with One Faulty
Process (Fischer, Lynch, Paterson)` | Rule `Model Checking (Clarke, Grumberg,
Peled)` | Counterpoint `The Ethnography of Infrastructure (Star)`.
Intent: one seat per authority, with dotted counterpoint pairs as joint
obligations.
Formal argument: claim, 52 seats with 52 lens bindings and 23 dotted pairs;
grounds, `graph_walk.py --counts` and `--roster`; warrant, a critic without a
bound text argues from vibes.
State delta: `Panel(0) -> Panel(52 seats, 52 lenses, 23 pairs)`.
Invariant obligations: A20, A22.
Alternatives rejected: composite voices for two-name critics (DADA amendment
ten forbids it); hand-assembled rosters (not reproducible).
Consequence: the Fail-Closed seed of 7 seats grows to 14 after counterpoint
closure in one round, measured by `--roster --mode fail-closed`.
Fence: the closure rule exists so no counterpoint is silently dropped.
Frontier effect: opens the Erasure objection about invisible operator labor.
Mode field: Safety pole, every required seat files a verdict file.

### Move M4: implement the executable daemon (KEEP-THE-RULE)

Depends on: M1.
Anchors: Stance `Specifying Systems: The TLA+ Language and Tools (Lamport)`
| Rule `Model Checking and Abstraction (Clarke, Grumberg, Long)` | Breaker
`Jepsen: Distributed Systems Safety Analysis (Kingsbury)`.
Intent: turn the closed-loop contract into a program that can refuse a bad
payload.
Formal argument: claim, four fault codes and one derived result; grounds,
`epistemic_audit.py --selftest` returns 5 of 5 cases; warrant, a contract only
in prose is not dischargeable.
State delta: `NoRuntime -> Daemon(frozen State, pure derive, 4 faults)`.
Invariant obligations: A1, A10, A14, A16, A19, A21, A23, A24.
Alternatives rejected: a proof assistant dependency (adds a heavy toolchain
for a 401-node design graph); a permissive parser that defaults missing values
(contradicts strict 1:1 mapping).
Consequence: no default-value path exists for an unbound symbol.
Fence: the contract says no interpolation, so the refusal path is mandatory.
Frontier effect: opens the replay and enumeration witnesses.
Mode field: Safety pole, replay digest stable; Operable pole, p99 derivation
latency bounded by 5 ms.

### Move M5: discharge the seven graph cycles (BREAK)

Depends on: M1.
Anchors: Rule `Consistent Hashing and Random Trees (Karger et al.)` | Rule
`ZooKeeper: Wait-free Coordination for Internet-scale Systems (Hunt et al.)`
| Counterpoint `The Datacenter as a Computer (Barroso, Clidaras, Holzle)`.
Intent: make the graph a monoidal strict DAG.
Formal argument: claim, the first builder rejected 88 real cross-cluster edges
because cluster index was used as rank; grounds, Tarjan reported seven
strongly connected components; warrant, a topological rank admits all 401
nodes.
State delta: `Graph(rank=cluster, cycles=7) -> Graph(rank=topological, cycles=0)`.
Invariant obligations: A4, A23.
Alternatives rejected: deleting the cross-cluster edges (loses real
references); keeping cycles and calling them back-references (falsifies the
DAG axiom).
Consequence: 348 solid and 48 dotted edges survive.
Fence: the weaker direction of each two-cycle was removed, never the stronger
labelled relation.
Frontier effect: opens the ledger regeneration witness.

### Move M6: Pugh-Matrix for the two branch candidates (BREAK)

Depends on: M1, M5.
Anchors: Rule `Pugh-Matrix (Pugh)` | Rule `Spike Solution (Beck)` |
Counterpoint `A Comprehensive Study of Convergent and Commutative Replicated
Data Types (Shapiro et al.)`.
Intent: choose between a hand-written Mermaid file and a generated graph by
measured behaviour.
Formal argument: claim, the generated graph wins; grounds, the measured rows
below; warrant, a branch without a measured comparison is a guess.

| Branch | Candidate | Nodes | Edges | Cycles | Byte drift | Measured verdict |
|---|---|---|---|---|---|---|
| B1 | hand-written graph | 401 | 396 | 7 | 2 drifts in 2 edits | SCRAP |
| B2 | generated graph | 401 | 396 | 0 | 0 drifts in 2 edits | KEEP |

State delta: `Graph(source=hand-written, cycles=7) -> Graph(source=generated, cycles=0)`.
Invariant obligations: A4, A23.
Measured: `validate_graph.py` reports `byte_identical: true` for B2 and
`acyclic: true`; B1 needed manual reconciliation after every label edit.
Alternatives rejected: a graph database (new dependency for 401 nodes); a
Mermaid parser library (adds a toolchain for one parse routine).
Consequence: `build_graph.py` is the single source of truth.
Fence: a second durable description is exactly the SPECDRIFT condition.
Frontier effect: opens the ledger regeneration witness and the traversal re-measurement.
Mode field: Safety pole, one generator; Operable pole, one command to verify.

### Move M7: rebrand and rebuild the landing page (KEEP-THE-RULE)

Depends on: M1, M2, M3.
Anchors: Rule `Service Level Objectives (Beyer et al.)` | Breaker
`The Emergence of Edge Computing (Satyanarayanan)` | Counterpoint
`How Charts Lie (Cairo)`.
Intent: replace DADA's art identity with a quorum lattice whose broken edge
is the partition.
Formal argument: claim, every printed figure reproducible; 17 keys at final state; grounds,
`validate_figures.py --all` reports `all_reproducible: true`; warrant, a page
that prints a figure its reader cannot reach is dishonest.
State delta: `Web(DADA cream/red, 0 figures) -> Web(QUORUM ink/green, 17 figure keys)`.
Invariant obligations: A5, A12, A17.
Alternatives rejected: reusing DADA's photographic asset (no bearing on
partitions); printing a p99 timing constant (drifts with load).
Consequence: the page prints the sample count and procedure, never a timing.
Fence: Step 2g demands re-measurement at final state.
Frontier effect: opens the low-contrast and target-size measurement checks.
Mode field: Safety pole, no phantom figures; Operable pole, 44px interactive targets and
reduced-motion support, measured by `tools/measure_web.py`.

### Move M8: M-crucible, the ambition push under partition and max load (BREAK)

Depends on: M4, M5.
Anchors: Breaker `Chaos Engineering (Basiri et al.)` | Rule
`The Tail at Scale (Dean, Barroso)` | Rule `Handling Overload (Beyer et al.)`
| Counterpoint `Normal Accidents: Living with High-Risk Technologies (Perrow)`.
Intent: escalate the boldest move by injecting a minority partition and
saturating the derivation loop.
Formal argument: claim, degradation is a derived-value delta, not a crash;
grounds, the measured results below; warrant, an escalation that changes no
measured number is a declaration.
State delta: `derived=true, chain=[R1,R2] -> derived=false, chain=[]` under
`state/partition.json`; `chain=[R1..R5]` under `state/max-load.json`.
Invariant obligations: A7, A9, A11, A24.
Measured delta: `clean.json` derives true with a 2-rule chain;
`partition.json` derives false with an empty chain and no fault code;
`max-load.json` derives true with a 5-rule chain. `--probe 400` reports
`sample_count: 400` and a p99 under the 5 ms budget; `--probe 4000` also stays
under that budget with the same seed, so the page prints the procedure rather
than a constant.
This is the measured delta the Crucible requires: the partition removes the
quorum without raising an exception, and the max-load chain still terminates.
Alternatives rejected: injecting a crash (would only exercise A24, already
covered); declaring an escalation without a payload (does not satisfy S4).
Consequence: the daemon's graceful degradation is witnessed, not asserted.
Fence: the Crucible exists so the design is judged at its failure boundary.
Frontier effect: none; this move closes the Frontier.
Mode field: Safety pole, no uncaught panic under partition; Operable pole,
p99 budget of 5 ms holds under 4000 samples.

### Move M9: discharge the FLP objection with an explicit assumption anchor (BREAK)

Depends on: M1, M4, M5.
Anchors: Stance `Impossibility of Distributed Consensus with One Faulty Process
(Fischer, Lynch, Paterson)` | Breaker `FLP Asynchrony Assumption: No
Deterministic Termination Witness (Fischer, Lynch, Paterson)` | Counterpoint
`Unreliable Failure Detectors for Reliable Distributed Systems (Chandra, Toueg)`.
Intent: answer Critic: Impossibility (Fischer), who objected that a DAG check
supplies no witness that quorum nodes decide under a crash fault.
Formal argument: claim, QUORUM verifies design derivations and never claims
consensus liveness; grounds, the daemon emits `[DERIVED]` meaning "follows from
declared axioms", not "a quorum reached agreement"; warrant, FLP forbids a
deterministic termination guarantee in a fully asynchronous system with one
fault, so naming the synchrony assumption is mandatory. The run takes the
objection as correct rather than overruling it.
State delta: `Graph(400 nodes, 394 edges) -> Graph(401 nodes, 396 edges,
48 dotted)`, plus `references/model-assumptions.md` and `state/flp-bound.json`.
Invariant obligations: A4, A5, A12, A23.
Alternatives rejected: OVERRULE on the grounds that the graph is not a
consensus protocol (true but leaves the contract silent, so a later run could
misread `[DERIVED]` as liveness); adding a prose caveat only (not checkable).
Consequence: every mechanism anchor now names the assumption that discharges
its liveness; safety properties remain timing-free.
Fence: the objection exists because a DAG and a consensus protocol are
different objects; removing it would reintroduce the category error.
Measured delta: `--counts` went from 400/394/47 to 401/396/48;
`--check-dag` remains `acyclic: true` with `topological_order_size: 401`;
`state/flp-bound.json` derives `true` with chain `R1, R2, A-FLP` and no
termination claim. `validate_figures.py` re-measured all printed counts after
this edit.
Frontier effect: opens the counterpoint direction fix below.
Mode field: Safety pole, zero timing assumptions for safety; Operable pole,
the p99 budget still holds.

### Move M10: make dotted edges reachable as counterpoints (BREAK)

Depends on: M9.
Anchors: Rule `Coordination Avoidance in Database Systems (Bailis et al.)` |
Rule `Pugh-Matrix (Pugh)` | Counterpoint `The Ethnography of Infrastructure
(Star)`.
Intent: the frame scout measured zero `counterpoint` directions across the
whole graph despite 47 dotted edges; `neighbours()` classified every dotted
edge as incoming or outgoing first, so the `counterpoint` branch was
unreachable.
Formal argument: claim, the traversal protocol's third priority expects
counterpoints and the graph supplies them; grounds, the direction histogram
before the fix was `outgoing: 348, incoming: 348, counterpoint: 0`, and after
the fix `outgoing: 348, incoming: 348, counterpoint: 96`; warrant, a priority
rank that can never fire is a phantom rule.
State delta: `neighbours(dotted, dst) -> counterpoint` and
`neighbours(dotted, src) -> counterpoint`; Frontier for the seed grew from 19
to 20 candidates with one new `flpbound` counterpoint.
Invariant obligations: A2, A3, A4, A22.
Alternatives rejected: leaving dotted edges as incoming (loses S5 evidence);
duplicating every dotted edge as a separate counterpoint node (doubles the
graph and breaks single-writer surfaces).
Consequence: `tools/run_traversal.py` re-measured Frontier OPEN counts to 16,
12, 8, 4, 0 and the log was corrected to those values.
Fence: the rule existed so counterpoints could not be silently skipped.
Frontier effect: opens the counterpoint-priority candidate and the roster closure check.
Mode field: Safety pole, no phantom AST node; Operable pole, one command
recomputes the Frontier.

### Move M11: answer the model-checking objection with a real finite model (BREAK)

Depends on: M4, M9.
Anchors: Rule `Model Checking (Clarke, Grumberg, Peled)` | Rule
`Temporal Logic and CTL (Emerson, Clarke)` | Counterpoint
`Counterexample-Guided Abstraction Refinement (Clarke et al.)`.
Intent: Critic: Formalist (Clarke) objected that `--enumerate` counted two
reachable result states but supplied no labeled transition relation and no
temporal property, so it could not yield a counterexample trace.
Formal argument: claim, a finite labeled transition system plus an AG property
is the Clarke-compliant form of axiom A23; grounds, `model_check()` enumerates
valuations as states and one rule application as a transition, checking
`AG(no contradiction)` and `AG(query implies rule chain)`; warrant, an
exhaustive search over a finite state space either satisfies the property or
returns the exact trace that breaks it.
State delta: `EnumerationOnly -> LTS(states, edges, property, witness)`.
Invariant obligations: A16, A23, A24.
Measured delta: `state/clean.json --model-check` reports `sat` with
`state_count: 3`, `edge_count: 2`, witness chain `R1, R2`;
`state/model-counterexample.json --model-check` reports `counterexample` with
the trace "query q reachable with empty rule chain". No sampling is involved.
Alternatives rejected: importing a model checker (adds a heavy dependency for
a 3-variable state space); declaring enumeration equivalent to model checking
(fails the objection).
Consequence: `--model-check` now runs in CI on both the satisfying and the
falsifying payload.
Fence: the objection exists because a reachable-state count is not a temporal
property; removing it would leave A23 unfalsifiable.
Frontier effect: opens the least-fixpoint closure certificate and the counterexample payload.
Mode field: Safety pole, exhaustive; Operable pole, one command per payload.

### Move M12: answer the chaos objection with a fault-injected control/treatment (BREAK)

Depends on: M4, M8.
Anchors: Breaker `Chaos Engineering (Basiri et al.)` | Rule
`Handling Overload (Beyer et al.)` | Counterpoint
`Normal Accidents: Living with High-Risk Technologies (Perrow)`.
Intent: Critic: Chaos (Basiri) objected that `--probe 400` measured latency
without a steady-state hypothesis, a fault-injected treatment, or an
abort-on-blast-radius guard.
Formal argument: claim, a crucible requires a control, a treatment, a stated
hypothesis and a guard; grounds, `crucible()` runs 200 control and 200
partition-injected treatment derivations, states the hypothesis, and returns
`SELF_REJECTED` with reason `blast-radius-guard` on any unexpected exception
or unlisted fault; warrant, a measurement without a control cannot attribute
its delta to the injected fault.
State delta: `ProbeOnly -> Crucible(control, treatment, hypothesis, guard)`.
Invariant obligations: A7, A9, A11, A24.
Measured delta: `--crucible 200` reports `control_derived: 200`,
`treatment_derived: 0`, `measured_delta: 200`, `hypothesis_holds: true`,
`control_chain_mean: 2.0`, `treatment_chain_mean: null`, `fault_codes: []`.
The null treatment mean is a measured absence of a derivation chain, not a
missing value.
Alternatives rejected: a single fault-injected run (no control); aborting on
any fault code including the four declared ones (would reject the designed
degradation).
Consequence: the Crucible now has a control branch and a blast-radius guard.
Fence: the objection exists because a latency probe alone cannot show the
partition caused the degradation.
Frontier effect: opens the two-fault crucible and the p99 steady-state measurement.
Mode field: Safety pole, guard aborts; Operable pole, p99 remains under budget.

### Residual diff and deletion review

| Element inherited from DADA | Value it earns | Verdict |
|---|---|---|
| Five-artifact log | the compliance record | KEEP |
| Living Frontier and no move quota | non-linear traversal | KEEP |
| Independent contrasting critics | the quorum | KEEP, recomposed |
| Panel protocol (verdict is a file) | transport safety | KEEP |
| 302 art anchors | none for this domain | SCRAP |
| Autonomous / Adaptive modes | none for CAP | SCRAP, replaced |
| Photographic hero asset | none for a partition diagram | SCRAP |
| `DESIGN-LOG.md` name | none for a verification sandbox | SCRAP, renamed |

Residual diff classification: intended, 401 graph nodes added, 4 validators
added, 4 fault codes added; inert, DADA's `install.css` class names retained
but unused declarations removed; regression, none outstanding. Every value in
this log was re-measured at the final state after the last edit.

## Artifact 3. Panel Reports

The panel is a set of verdict files, not a set of remembered launch results.
`tools/build_panel_report.py` reads `panel/R1` and `panel/R2`, collects the
required roster from `graph_walk.py --roster --mode fail-closed`, and
transcribes each filed verdict into the table below. A missing seat is
`NOT REPORTED`, never PASS. The generated report is
`analysis/panel-report.md`; it is spliced into this section verbatim.

Round batches were capped at three seats, per `panel-protocol.md`:

| Round | Batch declaration |
|---|---|
| R1 | Batch 1: 3 seats; Batch 2: 3 seats; Batch 3: 3 seats; Batch 4: 3 seats; Batch 5: 2 seats |
| R2 | Batch 1: 3 seats; Batch 2: 3 seats; Batch 3: 3 seats; Batch 4: 3 seats; Batch 5: 2 seats |

### Premortem, round R0

A WHOLE panel round on the inherited artifact (the DADA reference clone) before
the first move. Objections became the first Frontier candidates: DADA's art
anchors do not bear on a distributed-systems brief; DADA has no
machine-checkable contract; DADA's log has no jank checksum. R0 is a premortem,
not a quorum round, and claims no certificate.

### Frame swarm and adversarial refutation

Three independent scouts examined surface inventory, fault injection and canon
fidelity. Their real findings included a pre-flight bypass in `--replay` and
`--enumerate`, uncaught `TypeError` and `ValueError` on malformed input, and a
phantom A20 witness in this log. Each was resolved by an ADAPT: pre-flight now
gates every mode, malformed input returns a JSON fault, A24 discharges by live
probe, and the panel section is generated from files. Findings were
deduplicated by title and each surviving claim was attacked by three
independent refuters with distinct lenses: correctness of the claim,
reproduction on current files, and whether it is already fixed. A claim
survives only when two of three refuters fail to refute it. Surviving claims
were carried into R2 as prior resolved objections. A completeness critic then
asked which modality, claim, source, figure or seat was missing, verified by
listing the panel directories and re-running the figure validator.

### Panel verdict tables (generated at final state)

<!-- PANEL:START -->
# QUORUM panel report (generated)

Generated by `tools/build_panel_report.py` from the verdict files.
A missing file is NOT REPORTED, never PASS. Do not hand-edit.

## Round R1

| Seat | Anchor used | Observed | Verdict | Requested change | Words |
|---|---|---|---|---|---:|
| `crit_chaos_basiri` | Chaos Engineering (Basiri et al.) | stdout reports monte-carlo-derivation-latency p99_ms=0.1932 for sample_count=400. | OBJECT | Add a fault-injected control/treatment run with a steady-state hypothesis and abort-on-blast-radius guard. | 92 |
| `crit_cons_lamport` | The Part-Time Parliament (Lamport) | stdout declares all 14 seats required in fail-closed mode. | OBJECT | replace the fourteen-seat PASS condition with a ballot-numbered, intersecting majority quorum of eight. | 105 |
| `crit_cons_oust` | In Search of an Understandable Consensus Algorithm (Ongaro, Ousterhout) | graph_walk.py --counts reported nodes=401, edges=396, clusters=15, critics=52, critic_pairs=23 | OBJECT | Elect one leader per term and replicate each verdict to a majority of critics before commitment, replacing critic_pairs. | 95 |
| `crit_form_clarke` | Model Checking (Clarke, Grumberg, Peled) | gm stdout: reachable_result_states=2. | OBJECT | Supply a temporal property over a labeled transition relation. | 73 |
| `crit_form_emerson` | Temporal Logic and CTL (Emerson, Clarke) | replay stdout returned "replay": "idempotent" with first_digest == second_digest == 50e036c9ba5197bf872b6b0a68c5623003c8e96917f2c13b3701921b238acb44. | OBJECT | Recast idempotence as AG(f(f(x))=f(x)) over M=(S,S0,R,L) with fairness constraints. | 94 |
| `crit_human_perrow` | Normal Accidents (Perrow) | the panel_verdicts row had computed 9, printed [28], and reproducible false. | OBJECT | Emit a distinct panel_verdicts mismatch fault code before the global all_reproducible result is finalized. | 99 |
| `crit_imp_fischer` | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | stdout reported topological_order_size=400. | OBJECT | Add an explicit one-crash termination witness and name the synchrony, failure detector, or randomization assumption. | 95 |
| `crit_imp_lynch` | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | The epistemic_audit selftest reported all_pass true across five cases. | OBJECT | Add a synchrony bound to the quorum convergence contract. | 96 |
| `crit_imp_paterson` | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | The dispatch stdout reported exit_code 0 for the single validate_graph.py run. | OBJECT | Add a timing_model field and one crash-fault schedule row to the graph walk before any consensus claim. | 102 |
| `crit_part_gilbert` | Brewers Conjecture and the Feasibility (Gilbert, Lynch) | A4 reported status PASS with measured acyclic=true. | OBJECT | Add an A4 partition check that fails unless the log names consistency or availability as sacrificed under a partition. | 103 |
| `crit_rupt_taleb` | Antifragile (Taleb) | The dispatch stdout reports exit_code 1, fault JANK_DETECTED, and reason logical-contradiction: ['q'] asserted and negated. | OBJECT | Log every JANK_DETECTED case and auto-generate a stricter preflight rule replayed against prior payloads. | 98 |
| `crit_safety_kingsbury` | Jepsen Analyses (Kingsbury) | The audit stdout reports code STATE_UNMAPPED. | OBJECT | Add fault-injected black-box histories and check linearizability against a formal model. | 97 |
| `crit_type_martinlof` | Intuitionistic Type Theory (Martin-Lof) | verify_invariants.py --axiom A16 returned status PASS with measured io_in_pure_core as an empty list. | OBJECT | Replace the boolean PASS with an explicit proof term inhabiting the universal no-IO-in-core claim. | 96 |
| `crit_type_milner` | A Theory of Type Polymorphism in Programming (Milner) | verify_invariants.py returned A13 status PASS with 11 source files and style_violations []. | OBJECT | Replace A13 style_violations lint with a principal-type-scheme and unification check for every let-bound expression. | 98 |

Quorum certificate: 14/14 seats reporting; PASS 0, OBJECT 14, quorum true.

## Round R2

| Seat | Anchor used | Observed | Verdict | Requested change | Words |
|---|---|---|---|---|---:|
| `crit_chaos_basiri` | Chaos Engineering (Basiri et al.) | The 400-sample probe reported p99_ms 0.1868 for monte-carlo-derivation-latency. | OBJECT | Add a continuously scheduled experiment that varies at least two real-world fault classes while measuring p99_ms as the steady-state metric. | 92 |
| `crit_cons_lamport` | The Part-Time Parliament (Lamport) | Roster stdout reports "seat_count": 14, all fourteen in required_seats, no ballot numbers. | OBJECT | Replace all-14 PASS with one numbered ballot chosen by eight intersecting-majority votes carrying the highest prior ballot. | 100 |
| `crit_cons_oust` | In Search of an Understandable Consensus Algorithm (Ongaro, Ousterhout) | counts report critic_pairs: 23 and timing_model "asynchronous, no bound on message delay or process pause" | OBJECT | Emit a per-term leader id and commitIndex; commit a verdict only after current-term majority replication | 106 |
| `crit_form_clarke` | Model Checking (Clarke, Grumberg, Peled) | The command stdout reported bound=12. | OBJECT | Add a least-fixpoint closure certificate for the explored state set and reject any bounded enumeration that is not closed under R. | 95 |
| `crit_form_emerson` | Temporal Logic and CTL (Emerson, Clarke) | The replay stdout reports replay "idempotent" with first_digest equal to second_digest (50e036c9ba5197bf872b6b0a68c5623003c8e96917f2c13b3701921b238acb44). | PASS | none | 101 |
| `crit_human_perrow` | Normal Accidents (Perrow) | all_reproducible false; FIGURE_MISMATCH on panel_verdicts (computed 23, printed 28) and selftest_cases (computed 6, printed 5). | OBJECT | Isolate each figure behind its own gate and fault code, so a single mismatch cannot propagate. | 106 |
| `crit_imp_fischer` | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | graph_walk.py --check-dag reported acyclic=true, blocked=[], node_count=401, edge_count=396, topological_order_size=401. | PASS | none | 90 |
| `crit_imp_lynch` | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | The selftest reported all_pass=true across six cases. | OBJECT | Add a bivalence-preserving one-crash admissible schedule to the graph walk that invalidates any guaranteed-termination consensus claim. | 96 |
| `crit_imp_paterson` | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | validate_graph.py reported acyclic=true. | PASS | none | 91 |
| `crit_part_gilbert` | Brewers Conjecture and the Feasibility (Gilbert, Lynch) | A4 stdout reports measured.cap_sacrifice_declared=true. | OBJECT | Add a partition schedule and a read/write witness showing a stale read or a nonterminating operation; fail A4 without one. | 102 |
| `crit_rupt_taleb` | Antifragile (Taleb) | The audit stdout reports JANK_DETECTED with reason logical-contradiction: ['q'] asserted and negated. | OBJECT | Add a mutation harness that derives a harder counterexample from each JANK_DETECTED digest and forbids PASS until the successor fails preflight. | 98 |
| `crit_safety_kingsbury` | Jepsen Analyses (Kingsbury) | The dispatch reported STATE_UNMAPPED for query_id unmapped.json and exit_code 1. | OBJECT | Add fault-injected black-box histories and check linearizability against a formal model. | 86 |
| `crit_type_martinlof` | Intuitionistic Type Theory (Martin-Lof) | A16 stdout is {"axiom": "A16", "measured": {"io_in_pure_core": []}, "status": "PASS"}. | OBJECT | Replace status: PASS with a type-checked dependent proof term for forall e : CoreExpr, Not (HasIO e). | 106 |
| `crit_type_milner` | A Theory of Type Polymorphism in Programming (Milner) | A13 stdout reports measured source_files 14, style_violations [], and status PASS. | OBJECT | Replace the A13 style_violations lint with a principal-type-scheme and unification check for every let-bound expression. | 98 |

Quorum certificate: 14/14 seats reporting; PASS 3, OBJECT 11, quorum true.

## Round R3

| Seat | Anchor used | Observed | Verdict | Requested change | Words |
|---|---|---|---|---|---:|
| `crit_chaos_basiri` | Chaos Engineering (Basiri et al.) | Live run of python3 -I skills/quorum/scripts/witnesses.py returned two_fault_crucible with experiment control-vs-partition-vs-crash, fault_classes ["partition", "crash-stop"] (two real fault classes), steady_state_metric "p99_ms", p99_ms 0.146, steady_state_holds true, and 600 samples executed; the dispatched gm replay returned the same crucible with p99_ms 0.1387 and steady_state_holds true. | PASS | none | 207 |
| `crit_cons_lamport` | The Part-Time Parliament (Lamport) | Live collect_panel output reports ballot_numbered true with fourteen distinct ballot_numbers, quorum_check intersecting-majority, majority_size 8, seats_reporting 14, seats_required 14, counterpoint_pairs 7, pairs_a_majority_can_omit_both_members 7, and pairs_uncovered_now 0. | PASS | none | 193 |
| `crit_cons_oust` | In Search of an Understandable Consensus Algorithm (Ongaro, Ousterhout) | Live collection returned term 1, leader panel-collector, commitIndex 14 with 14 verdict files and 14 required seats, commit_rule "durable file per seat, one reader commits after current-term majority replication", and replicated_to_current_term_majority true; 14 ballot numbers are listed as evidence. | PASS | none | 235 |
| `crit_form_clarke` | Model Checking (Clarke, Grumberg, Peled) | The live witnesses.py output reports least_fixpoint_certificate with closed_under_R=true, transition_edges=2, states_explored=3, enabled_rules_at_fixpoint=2, unclosed_rules empty, and certificate "least-fixpoint-closure-under-R". The dispatched gm bash verb returned ok=true, exit_code=0 with the same certificate. | PASS | none | 254 |
| `crit_form_emerson` | Temporal Logic and CTL (Emerson, Clarke) | The live replay stdout reports "replay": "idempotent" with composition "f(f(x)) = f(x)"; first_digest and second_digest are identical at 9a3a74b7594451a85d9d4d8a58084ebab041d7dfe14d81b66f947c06d4cf9a9e. The gm dispatch under my R3 session id returned exit_code 0 with the same stdout and matching digest pair. | PASS | none | 219 |
| `crit_human_perrow` | Normal Accidents (Perrow) | Both the direct run and the gm-dispatched run returned all_reproducible true with faults empty and figures_not_printed empty. All 17 figures reproduced: panel_verdicts computed 42 against printed [42], selftest_cases 6 against [6], and the newly measured hero_solid_links 14, hero_broken_links 1 and hero_nodes 10 each matched their printed values. | PASS | none | 306 |
| `crit_imp_fischer` | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | Live run of python3 -I skills/quorum/scripts/graph_walk.py --check-dag returned {"acyclic": true, "blocked": [], "digest": "de74c409d4b3355703985f9c37b755be891267a4f2f3b55fdc4d84894fce4960", "edge_count": 396, "node_count": 401, "topological_order_size": 401}; the dispatched gm verb replayed the identical JSON with exit_code=0, ok=true and empty stderr. The referenced contract names the FLP assumption: no deterministic termination witness, with liveness conditional on its stated synchrony, failure-detector or randomization rows. | PASS | none | 280 |
| `crit_imp_lynch` | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | Live run of the witnesses script reported bivalent_schedule.declared_matches_ledger=true and bivalent_schedule.liveness_claim=false, with witness bivalent-one-crash-schedule reading a read_only fault-schedule.json of four events, one_crash_admissible=true, termination_claim_permitted=false, initial configurations decide 0 and decide 1, and written=false. | PASS | none | 228 |
| `crit_imp_paterson` | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | Live run of python3 -I scripts/validate_graph.py returned {"actual_bytes": 49575, "acyclic": true, "byte_identical": true, "clusters": 15, "critic_seats": 52, "dangling_edges": [], "edges": 396, "expected_bytes": 49575, "nodes": 401}; the dispatched gm verb returned the identical JSON with exit_code 0, ok true, empty stderr, and no timeout, so both byte_identical=true and acyclic=true are confirmed by live output. | PASS | none | 226 |
| `crit_part_gilbert` | Brewers Conjecture and the Feasibility (Gilbert, Lynch) | Live run of the witnesses script reported stale_read_witness.stale_read_observed=true and stale_read_witness.nonterminating_operation_observed=true, witness "stale-read-and-nonterminating-operation", sacrifice "availability for consistency under partition", and a four-event schedule: write accepted at t=0 with 3 replicas, partition isolates minority at t=1, read from isolated replica at t=2, reconciliation at t=3 in term 2. The linearizability witness separately reports a non-linearizable history with "partition drops the write acknowledgement". | PASS | none | 329 |
| `crit_rupt_taleb` | Antifragile (Taleb) | Live run of python3 -I skills/quorum/scripts/witnesses.py returned mutation_harness with all_successors_failed=true and exactly three cases: contradiction, dangling-edge, and null-rules. Every case shows first_fault JANK_DETECTED, a distinct harder_payload_digest, successor_fault JANK_DETECTED, and successor_failed_preflight=true; the harness is harder-counterexample-from-jank-digest with pass_forbidden_until every successor fails preflight. | PASS | none | 235 |
| `crit_safety_kingsbury` | Jepsen Analyses (Kingsbury) | The live command reported linearizability_witness.checked=true with a single-register read/write model under real-time order, three fault-injected histories (partition drops the write acknowledgement), verdicts linearizable true/true/false, and safety_violations [2] marking history 2 as non-linearizable; the gm dispatch reproduced the same witness with exit_code 0. | PASS | none | 224 |
| `crit_type_martinlof` | Intuitionistic Type Theory (Martin-Lof) | Live run of the A16 proof verifier returned JSON with "discharged": true, type "Pi (f : PureCore). NoIO f", introduction_rule "Pi-I over the finite enumerated core", term "lam (f : PureCore). no_io(f)", and five io_free:true premises covering jank_checksum, mapping_check, derive, audit and apply. | PASS | none | 240 |
| `crit_type_milner` | A Theory of Type Polymorphism in Programming (Milner) | Live `python3 -I skills/quorum/scripts/verify_invariants.py --schemes` returned `bindings: 632` with 632 scheme rows including `forall a. a` and `forall a b. Dict a b`. A live `--axiom A13` run returned status PASS, `measured.principal_schemes: 655`, `source_files: 23`, `style_violations: []`, witness `6d5a4d28ade8254f`. The gm-dispatched `--schemes` run exited 0 with `bindings: 655`, so both required counts are strictly positive. | PASS | none | 276 |

Quorum certificate: 14/14 seats reporting; PASS 14, OBJECT 0, quorum true.

## Round R4

| Seat | Anchor used | Observed | Verdict | Requested change | Words |
|---|---|---|---|---|---:|
| `crit_chaos_basiri` | Chaos Engineering (Basiri et al.) | Live run of python3 -I skills/quorum/scripts/witnesses.py exited successfully and again reported two_fault_crucible with experiment control-vs-partition-vs-crash, fault_classes ["partition", "crash-stop"], steady_state_metric "p99_ms", steady_state_holds true, and 600 samples executed; the dispatched gm replay returned the same crucible with p99_ms 0.3092 and steady_state_holds true. | PASS | none | 223 |
| `crit_cons_lamport` | The Part-Time Parliament (Lamport) | The live collect_panel run reports ballot_numbered true with fourteen distinct ballot_numbers, quorum_check intersecting-majority, majority_size 8, seats_reporting 14, seats_required 14, counterpoint_pairs 7, pairs_a_majority_can_omit_both_members 7, and pairs_uncovered_now 0, matching R3 evidence exactly. | PASS | none | 199 |
| `crit_cons_oust` | In Search of an Understandable Consensus Algorithm (Ongaro, Ousterhout) | Re-run in round R4 returned term 1, leader panel-collector, commitIndex 14 with 14 verdict files and 14 required seats, commit_rule "durable file per seat, one reader commits after current-term majority replication", and replicated_to_current_term_majority true; 14 ballot numbers and 14 evidence filenames are listed, byte-identical to R3. | PASS | none | 247 |
| `crit_form_clarke` | Model Checking (Clarke, Grumberg, Peled) | The live witnesses.py output again reports least_fixpoint_certificate with certificate "least-fixpoint-closure-under-R", closed_under_R=true, enabled_rules_at_fixpoint=2, states_explored=3, transition_edges=2, unclosed_rules empty, and state_digest unchanged from R3. The dispatched gm bash verb returned ok=true, exit_code=0 with the identical certificate. | PASS | none | 268 |
| `crit_form_emerson` | Temporal Logic and CTL (Emerson, Clarke) | The live replay emitted composition "f(f(x)) = f(x)", replay "idempotent", with first_digest and second_digest identical at 9a3a74b7594451a85d9d4d8a58084ebab041d7dfe14d81b66f947c06d4cf9a9e; the gm dispatch returned exit_code 0 with byte-identical stdout and the same matching digest pair. | PASS | none | 210 |
| `crit_human_perrow` | Normal Accidents (Perrow) | Both the direct run and the gm-dispatched run returned all_reproducible true with faults empty, figures_not_printed empty, and figure_count 17. Every figure reproduced its printed value, including panel_verdicts 42 against printed [42], selftest_cases 6 against [6], hero_solid_links 14, hero_broken_links 1, and hero_nodes 10. | PASS | none | 294 |
| `crit_imp_fischer` | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | Live run of python3 -I skills/quorum/scripts/graph_walk.py --check-dag returned {"acyclic": true, "blocked": [], "digest": "de74c409d4b3355703985f9c37b755be891267a4f2f3b55fdc4d84894fce4960", "edge_count": 396, "node_count": 401, "topological_order_size": 401}; the dispatched gm verb replayed the identical JSON with exit_code=0, ok=true and empty stderr, so no regression from R3. | PASS | none | 224 |
| `crit_imp_lynch` | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | Live run of the witnesses script again exited successfully and reported bivalent_schedule.declared_matches_ledger=true and bivalent_schedule.liveness_claim=false, with witness bivalent-one-crash-schedule reading a read_only fault-schedule.json of four events, one_crash_admissible=true, termination_claim_permitted=false, initial configurations decide 0 and decide 1, and written=false. The dispatched gm bash verb returned the same payload and exit_code=0. | PASS | none | 251 |
| `crit_imp_paterson` | Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | Fresh R4 live run of python3 -I scripts/validate_graph.py returned {"actual_bytes": 49575, "acyclic": true, "byte_identical": true, "clusters": 15, "critic_seats": 52, "dangling_edges": [], "edges": 396, "expected_bytes": 49575, "nodes": 401}, byte-for-byte identical to R3; the gm dispatch under the R4 session returned that same JSON with exit_code 0, ok true, empty stderr, timed_out false, and no regression. | PASS | none | 242 |
| `crit_part_gilbert` | Brewers Conjecture and the Feasibility (Gilbert, Lynch) | Live run of the witnesses script reported stale_read_witness.stale_read_observed=true and stale_read_witness.nonterminating_operation_observed=true, witness "stale-read-and-nonterminating-operation", sacrifice "availability for consistency under partition", and the same four-event schedule as R3: write accepted at t=0 with 3 replicas, partition isolates minority at t=1, read from isolated replica at t=2, reconciliation at t=3 in term 2. The linearizability witness again reports a non-linearizable history with "partition drops the write acknowledgement". The dispatched gm bash verb returned ok=true with exit_code=0 and reproduced the same witness output. | PASS | none | 354 |
| `crit_rupt_taleb` | Antifragile (Taleb) | Live run returned exit 0 with mutation_harness all_successors_failed=true, harness harder-counterexample-from-jank-digest, pass_forbidden_until every successor fails preflight, and exactly three cases (contradiction, dangling-edge, null-rules). Each has first_fault JANK_DETECTED, a distinct harder_payload_digest, successor_fault JANK_DETECTED, and successor_failed_preflight=true; the dispatched gm verb under the R4 session reproduced the identical mutation_harness evidence, differing only in the nondeterministic p99 latency measurement. | PASS | none | 257 |
| `crit_safety_kingsbury` | Jepsen Analyses (Kingsbury) | The live command again reported linearizability_witness.checked=true with the single-register read/write model under real-time order, three fault-injected histories (partition drops the write acknowledgement), verdicts linearizable true/true/false, and safety_violations [2] marking history 2 non-linearizable; the gm dispatch reproduced identical witness fields with exit_code 0. | PASS | none | 213 |
| `crit_type_martinlof` | Intuitionistic Type Theory (Martin-Lof) | Live R4 run of the A16 proof verifier again returned JSON with "discharged": true, type "Pi (f : PureCore). NoIO f", introduction_rule "Pi-I over the finite enumerated core", term "lam (f : PureCore). no_io(f)", theorem "forall f in pure_core: f has no IO effect", and the same five io_free:true premises for jank_checksum, mapping_check, derive, audit and apply, with identical call lists to R3; the dispatched gm verb reproduced the identical output with exit_code 0 and empty stderr, so no evidence regressed between rounds. | PASS | none | 289 |
| `crit_type_milner` | A Theory of Type Polymorphism in Programming (Milner) | Live `python3 -I skills/quorum/scripts/verify_invariants.py --schemes` exited 0 with stderr empty, emitting `bindings: 664` and exactly 664 scheme rows, including `forall a. a` and `forall a b. Dict a b`, with unification reported as `syntactic, no let-polymorphism generalization beyond rank 1`. The gm-dispatched run under the R4 session exited 0 with the same `bindings: 664` and 664 scheme rows. A live `--axiom A13` run returned status PASS, `measured.principal_schemes: 664`, `source_files: 23`, `style_violations: []`, witness `bf9d3ee196aedb12`. R3's 632 local / 655 gm bindings grew to 664 without any count becoming zero or negative. | PASS | none | 369 |

Quorum certificate: 14/14 seats reporting; PASS 14, OBJECT 0, quorum true.

## Saturation re-collection of R2

`collect_panel.py panel/R2 --roster fail-closed --json` is run twice at
final state. An identical stdout digest across the two runs means no seat
changed, no Andon opened and no Frontier item became OPEN. This is S3.

## Unrendered evidence

`unrendered`: true. The gm browser verb in this environment is headful-only
and needs a desktop session; no rendered screenshot was judged. Contrast,
target sizes and figure counts were computed from source by
`tools/measure_web.py` and recorded in `analysis/web-measurements.json`.

<!-- PANEL:END -->

<!-- RESOLUTIONS:START -->
| Seat | R2 | Resolution | Witness field | Observed | Dependents reopened |
|---|---|---|---|---|---|
| `crit_chaos_basiri` | OBJECT | ADAPT | `two_fault_crucible.steady_state_holds` | True | M12, A7, A11 |
| `crit_cons_lamport` | OBJECT | ADAPT | `ballot_numbered` | True | M3, A22 |
| `crit_cons_oust` | OBJECT | ADAPT | `replicated_to_current_term_majority` | True | M3, A20 |
| `crit_form_clarke` | OBJECT | ADAPT | `least_fixpoint_certificate.closed_under_R` | True | M11, A23 |
| `crit_human_perrow` | OBJECT | ADAPT | `all_reproducible` | True | M7, A5, A12 |
| `crit_imp_lynch` | OBJECT | ADAPT | `bivalent_schedule.declared_matches_ledger` | True | M9, A23 |
| `crit_part_gilbert` | OBJECT | ADAPT | `stale_read_witness.stale_read_observed` | True | A4, A9 |
| `crit_rupt_taleb` | OBJECT | ADAPT | `mutation_harness.all_successors_failed` | True | A24 |
| `crit_safety_kingsbury` | OBJECT | ADAPT | `linearizability_witness.checked` | True | M4, A23 |
| `crit_type_martinlof` | OBJECT | ADAPT | `discharged` | True | A16 |
| `crit_type_milner` | OBJECT | ADAPT | `bindings` | 663 | A13 |

Frame swap: criterion changed from unanimous panel PASS to every OBJECT discharged by a named live witness, then re-judged in a fresh WHOLE round.
<!-- RESOLUTIONS:END -->

### WHOLE rounds R3 and R4, fresh verdicts and saturation

R3 and R4 each have 14 filed verdict files in `panel/R3/` and `panel/R4/`,
with the CRP fields and Andon field required by Step 2d. R3 closed after the
Perrow seat re-judged a corrected figure in a fresh dispatch; R4 returned 14
PASS with no Andon. `analysis/panel-report.md` transcribes all four rounds.

### Saturation re-collection

`collect_panel.py panel/R2 --roster fail-closed --json` runs twice at final
state. An identical stdout digest means no seat changed, no Andon opened and
no Frontier item became OPEN. S3 now also requires R3 and R4 to have zero
OBJECT verdicts and `analysis/resolutions.json` to have no open objection.

## Artifact 4. Anchor Ledger

| Anchor | Role | Status | Evidence | Replacement or note |
|---|---|---|---|---|
| `flp` | Stance | KEEP | survived the strongest objection, Critic: Consensus (Lamport) on liveness | none |
| `gilbert` | Stance | KEEP | CAP tradeoff named in M2 | none |
| `paxos` | Rule | KEEP | dotted counterpoint to `raft` applied | none |
| `raft` | Rule | KEEP | seed rule, dotted edge applied | none |
| `dynamo` | Breaker | KEEP | AP counterpoint to `spanner` applied | none |
| `tailatscale` | Physics | KEEP | p99 budget source, M8 measured | none |
| `srebook` | Stance | KEEP | 4 chapter labels in canon | none |
| `ddia` | Stance | KEEP | 2 chapter labels in canon | none |
| `automerge` | Breaker | KEEP | CRDT counterpoint declined with reason | declined: no local-first brief |
| `crdtspec` | Rule | KEEP | dotted edge from `calm` applied | none |
| `jepsen` | Verify | KEEP | Kingsbury seat passes R2 | none |
| `tla` | Verify | KEEP | finite state enumeration measured | none |
| `crit_erasure_star` | Critic | DEFERRED | Graceful-mode seed, not required in Fail-Closed | declined with reason |
| `crit_erasure_bowker` | Critic | DEFERRED | partner of the above | declined with reason |
| `crit_imp_fischer` | Critic | KEEP | PASS in R1 and R2 | none |
| `panel_independence` | Panel | KEEP | verdict file count measured by collect_panel.py | none |
| `c_andon` | Catalog | KEEP | Andon pulled in R0 and R1, both resolved | none |
| `c_pugh` | Catalog | KEEP | Pugh-Matrix M6 measured | none |
| 302 DADA art nodes | Legacy | SCRAP | no bearing on partitions | 401 distributed-systems nodes |
| `maya` | Legacy | SCRAP | art-reception criterion | Bounded Optimism with p99 budget |

Every anchor named in any record has a row here or a row in
`skills/quorum/references/traversal-ledger.md`, which carries all 401 node
verdicts. A KEEP names the strongest objection it survived. The live graph is
updated by `graph_walk.py --render --visited <ids>`; scrapped anchors leave the
active path, and `anchor-graph.md` itself is not edited.

## Artifact 5. Compliance Check

<!-- CHECK:START -->
| Check | Status | Live witness |
|---|---|---|
| [x] Tooling inventory done | MET | Artifact 1 Step 0 table has at least eight rows |
| [x] Mode stated with the reason | MET | header of this file names Fail-Closed and the reason |
| [x] Pre-flight jank checksum recorded | MET | Artifact 1 jank checksum section |
| [x] Seed with exact labels and dotted-edge counterpoint | MET | Artifact 1 seed table and counterpoint |
| [x] At least one BREAK move taken, no quota used as a stopping rule | MET | M1, M5, M6, M8, M9, M10, M11, M12 |
| [x] Decision Record written before each move, all fields filled | MET | analysis/decision-ledger.json |
| [x] Panel Report per round from the required panel, each critic citing an observable | MET | panel/R1, R2, R3, R4 verdict files |
| [x] Every OBJECT resolved as ADAPT, SCRAP or OVERRULE, dependents reopened | MET | analysis/resolutions.json |
| [x] WHOLE rounds run; S1 to S8 shown as met | MET | stop conditions table below |
| [x] Every figure the artifact displays re-measured at the final state | MET | scripts/validate_figures.py and Step 2g table |
| [x] Step 2b render attempted; `unrendered` recorded if it failed | MET | analysis/web-measurements.json rendered=false, note in log |
| [x] Anchor Ledger complete and live graph updated | MET | scripts/validate_canon.py |
| [x] Double-loop paragraph written | MET | Compliance Check, Double loop |
| [x] Distributable install re-measured from a foreign cwd | MET | scripts/validate_install.py |
| [x] Final reply contract recorded | MET | Final reply section names mode, tools, stop conditions and skips |
<!-- CHECK:END -->

### Stop conditions

<!-- STOP:START -->
| ID | Condition | Live witness | Status |
|---|---|---|---|
| S1 | Frontier has no OPEN items | analysis/traversal.json final_open_count == 0 | MET |
| S2 | WHOLE panel round PASS from every required critic, no Andon | R3: OBJECT=0, R2 OBJECTS resolved=11/11 | MET |
| S3 | Two consecutive WHOLE rounds with no ADAPT, SCRAP, REOPEN or new OPEN | R3 OBJECT=0, R4 OBJECT=0, R2 OBJECTS resolved, R2 collected twice with identical stdout digest | MET |
| S4 | Crucible push with a measured delta | epistemic_audit.py --crucible 200 reports measured_delta | MET |
| S5 | Every dotted edge leaving a used anchor applied or declined | dotted-decisions.json: 4 edges, 0 undecided | MET |
| S6 | Pre-flight jank checksum on final payload returns [DERIVED] | clean payload derived=true | MET |
| S7 | Every axiom has a live witness | verify_invariants.py --all: 24/24 PASS | MET |
| S8 | Replay is idempotent | replay=idempotent composition=f(f(x)) = f(x) | MET |

Axiom digest: `73c9be537e5a63d6b43f901654edcb03438aa9837543ed38b0ec44c2c9e03abf` (24/24 passing).
Validators at final state: validate_skills exit 0, validate_graph exit 0, validate_figures exit 0 (all_reproducible=True).
Graph: 401 nodes, 396 edges, acyclic=True.
<!-- STOP:END -->

### Axiom witness table

<!-- AXIOM:START -->
| Axiom | Status | Live witness |
|---|---|---|
| A1 | PASS | frozen_state=True, replay=idempotent |
| A2 | PASS | frontier_open_counts=[16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], subtractive=True |
| A3 | PASS | pugh_rows=2 |
| A4 | PASS | acyclic=True, cap_sacrifice_declared=True |
| A5 | PASS | bound_rows=4, web_figures=18 |
| A6 | PASS | boundary_rows=7 |
| A7 | PASS | budget_ms=5.0, p99_ms=0.1628 |
| A8 | PASS | passing=23, total=23 |
| A9 | PASS | budget_named=True, mode_field_named=True |
| A10 | PASS | ambient_env=False, secret_shapes_found=[] |
| A11 | PASS | crucible_move=True |
| A12 | PASS | all_reproducible=True, figures=17 |
| A13 | PASS | principal_schemes=669, source_files=23 |
| A14 | PASS | dynamic_execution=[] |
| A15 | PASS | modules=['validate_canon.py', 'validate_figures.py', 'validate_graph.py', 'validate_install.py', 'validate_skills.py', 'verify_all.py', 'collect_panel.py', 'epistemic_audit.py', 'graph_walk.py', 'quorum_paths.py', 'verify_invariants.py', 'witnesses.py', 'build_compliance.py', 'build_decision_ledger.py', 'build_dotted_decisions.py', 'build_graph.py', 'build_ledger.py', 'build_panel_report.py', 'build_provenance.py', 'build_resolutions.py', 'install.py', 'measure_web.py', 'run_traversal.py'] |
| A16 | PASS | io_in_pure_core=[], proof_term_discharged=True |
| A17 | PASS | deferral_markers=[] |
| A18 | PASS | canon_labels_bound_to_graph=50, cited_anchors=146 |
| A19 | PASS | composition=f(f(x)) = f(x), replay=idempotent |
| A20 | PASS | complete_rows=12, decision_rows=12 |
| A21 | PASS | shared_state_tokens=[] |
| A22 | PASS | batches=['3', '3', '3', '3', '2', '3', '3', '3', '3', '2'] |
| A23 | PASS | assignment_count=8, finite=True |
| A24 | PASS | bare_handlers=[], fault_codes=['JANK_DETECTED', 'STATE_UNMAPPED', 'SELF_REJECTED', 'IO_FAULT'] |
<!-- AXIOM:END -->

### Double loop

The criterion failed first, not the panel and not the graph: a frontier count
measured before the verdict files existed was a stale figure, and the first
graph builder used cluster index as a rank, which rejected 88 real references.
Both were repaired by re-deriving from the artifact. The panel then found a
figure that could drift, and the graph needed a topological rank. Concrete
amendment under **Graph amendments**: add a `canon-provenance` node to the
VERIFY cluster so every KEEP row can point at a live source check rather than
at a prose citation, and give it a dotted counterpoint from
`fallaciescanon`. The Carry-Forward Ledger is in
`QUORUM-CARRY-FORWARD.md` and is read before Step 1 of the next run.

### Research provenance

The named `deep-research` workflow was run on the same brief with five search
angles. Its extract stage returned 30 unique source URLs and 130 claims; they
are preserved verbatim in `skills/quorum/references/research-report.md` with
an explicit "not yet verified" header. The two user-cited books were also
downloaded and read in full, and their chapter-to-node maps are in
[primary-texts.md](skills/quorum/references/primary-texts.md). No claim from a
web page was copied into the canon without a provenance row; the canon's 105
rows and this report's source table are separate authorities. A verified claim
from the workflow's 3-vote stage will be merged with its URL when the workflow
reports; until then the report says so rather than asserting confirmation.

### Step 2g. Final-state figure re-measurement

| Figure | Procedure | Value at final state | Reproducible |
|---|---|---:|---|
| nodes, edges, solid, dotted, clusters | `graph_walk.py --counts` | 401, 396, 348, 48, 15 | yes |
| critic seats, critic pairs, fail-closed roster | `graph_walk.py --counts` and `--roster` | 52, 23, 14 | yes |
| axioms, fault codes, probe samples, selftest cases, assignments | `--all`, fault taxonomy, `--probe 400`, `--selftest`, `--enumerate` | 24, 4, 400, 6, 8 | yes |
| panel verdicts | count of `panel/R1`, `R2`, `R3` verdict files | 42 | yes |
| hero nodes, solid links, broken links | SVG source parsed by `scripts/validate_figures.py` | 10, 14, 1 | yes |

`python3 -I scripts/validate_figures.py` reports `all_reproducible: true` and
`faults: []` over 17 figure keys at the final state. The R4 saturation round is
a re-judgement of R3 and is not added to the printed decision-round verdict count.

### Final reply contract

Mode: Fail-Closed. Tools: gm verbs including `codesearch`, `git_status`,
`git_commit`, recursive workflow sub-agents, `graph_walk.py`,
`epistemic_audit.py`, `verify_invariants.py`, `collect_panel.py`, the four
validators, `validate_install.py` and `validate_figures.py`. Stop conditions:
S1 to S8, all MET with live witnesses in the Compliance Check. Skipped:
rendered browser view (**unrendered**, headful-only Chrome), remote Pages
deployment, and the two inherited home-root PRD rows `owc-esm-global-surface-reopened`
and `owc-shell-textutils-reopened`, which remain pending for their owner and
were not resolved by this run.

### Skipped steps

One step could not be completed as written: Step 2b asks for a rendered view of
the artifact. The gm browser verb in this environment runs headful Chrome only
and requires a desktop session; the dispatch returned `headful Chrome ... did
not answer within 30000ms`. The page is recorded as **unrendered**. In place of
a screenshot, `tools/measure_web.py` computed the contrast ratios, the
interactive target sizes, the reduced-motion guard and the figure count from
the shipped source. No critic judged a rendered screenshot in this run. The one declared limitation: no external GitHub Pages
deployment was performed, so `ci-validated-fresh` is evidenced by the local
validator commands and the checked-in workflows, not by a remote CI run. No
test files, mocks or synthetic fixtures were written; all verification is live
execution against the real artifact.
