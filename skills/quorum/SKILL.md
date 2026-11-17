---
name: quorum
description: "QUORUM (Quorum-Ordered Universal Reasoning Over Unreliable Machines). A closed-loop formal verification sandbox for distributed systems design. Use when asked to design, review or harden infrastructure, edge deployments, replication, consensus, fault tolerance or decentralization, with a self-correcting adversarial critic panel and strict serialized derivation. Two modes: Fail-Closed (safety-dominant, no interpolation) and Graceful (bounded degradation, p99 budget). Non-linear: traverses the distributed-systems anchor graph through a living Frontier, with no move quota, until the quorum of critics converges. Uses any graph, workflow, diagram or task tooling available. Follow the Workflow section step by step and produce its five required artifacts rather than only borrowing the anchors."
---

# QUORUM: Quorum-Ordered Universal Reasoning Over Unreliable Machines

## 0. Contract (read first)

Loading this skill means performing the workflow below, not borrowing its
vocabulary. A run is complete only when these five artifacts exist in
`QUORUM-LOG.md` (create it and append as you go; if you cannot write files, put
them in your reply as a single JSON document with the same five keys):

1. **Traversal Plan**, including the living **Frontier**
2. **Decision Records**, one per move
3. **Panel Reports**, one per round
4. **Anchor Ledger**
5. **Compliance Check**

**There is no move quota.** The run ends when the stop conditions in Step 4 hold,
however many moves, rounds or revisits that takes. A move count is an outcome,
never a target. A partial run records its Open frontier and its resume point in
`QUORUM-LOG.md`. If `QUORUM-LOG.md` already exists with an Open frontier, resume
from it instead of starting over.

### 0.1 The daemon contract

The run is executed by the `EPISTEMIC_AUDIT_DAEMON`, a deterministic engine over
`STATE_PAYLOAD` (the brief plus everything measured from the artifact) and
`QUERY_VECTOR` (each requested decision). Its I/O port is machine-readable only:
JSON, YAML, or rigid Markdown tables. Conversational prose, affective tokens,
apologies and hedges are an `IO_FAULT`. The four faults terminate a query, not
the run; the fault is recorded and the query is reframed:

| Code | Trigger | Recovery |
|---|---|---|
| `[FAULT: JANK_DETECTED]` | contradiction, undefined variable, category error, or structural decay in `STATE_PAYLOAD` | name the failure mode, repair the payload, re-run pre-flight |
| `[FAULT: STATE_UNMAPPED]` | a query atom names a variable or axiom absent from the payload | name the missing variable or axiom, add it by measurement or decline the query |
| `[FAULT: SELF_REJECTED]` | derivation rests on an unstated assumption, a guess, or a logical leap | name the falsification, discharge it or abandon the derivation |
| `[FAULT: IO_FAULT]` | output contains prose, praise, hedging or unserialized text | reserialize the output |

Execution loop: ingest -> pre-flight jank checksum -> strict 1:1 state mapping ->
boolean derivation -> meta-cognitive loopback (attempt to falsify the derivation)
-> serialize -> terminate the query. `skills/quorum/scripts/epistemic_audit.py`
is the executable form of this contract; `skills/quorum/scripts/graph_walk.py`
is the executable form of the frontier.

### 0.2 Derivation discipline

- `Gen = argmin(DeltaSpec) minus Sycophancy`: minimize drift from the brief;
  never add a move to please a critic or to flatter the requester.
- Every function is typed against the spec (`f |- Spec`), never against vibes.
- Every `STATE_PAYLOAD` symbol resolves to a declared node (`not exists phantom`).
- Every node is fully expanded (`not exists trunc`): no elision, no `...` in a
  record, no placeholder body.
- Context is monotone: `Gamma_t` is a superset of `Gamma_(t-1)`; the daemon has
  no amnesia. A superseded record stays in the log, marked superseded.
- Effects are explicit. The daemon has no hidden mutation, no ambient authority,
  and no unhandled exception: every exception is handled or propagated.

### 0.3 Axiom ledger

Each axiom below has a checkable predicate. `verify_invariants.py` discharges
them against the repository at final state; the Compliance Check names the
witness for each row. An axiom that cannot be discharged is a blocking OBJECT.

| ID | Axiom | Predicate |
|---|---|---|
| A1 | `State = ADT-isomorphic pure morphisms` | derivation state is a frozen value; every transition returns a new value |
| A2 | `Entropy = Subtractive (O(1) cognitive)` | each round removes at least one open condition; new conditions are recorded |
| A3 | `Ontogeny = Stochastic empirical fitness` | rival branches are scored by measured behaviour, not by assertion |
| A4 | `Topology = Monoidal strict DAG` | anchor graph is acyclic; `graph_walk.py --check-dag` passes |
| A5 | `Physics = Hardware-bounded CAP-aware` | every latency or capacity claim cites a measured bound |
| A6 | `Boundaries = Affine typestate Byzantine` | each boundary carries a typestate and a trust assumption; no implicit trust |
| A7 | `Epistemology = Profiling Monte Carlo` | sampled probes report sample count and p99, not a point estimate |
| A8 | `Correctness = Pi-types static verification` | `verify_invariants.py` reports PASS for every declared obligation |
| A9 | `Resilience = p99-bounded graceful` | degradation has a stated budget; overload behaviour is measured |
| A10 | `Contracts = Strict semantics zero-leak` | no unchecked resource, no secret literal, no unbounded buffer |
| A11 | `Crucible = Chaos max-load` | at least one move is taken under injected partition and max load |
| A12 | `Teleology = Utility max (DX/UX)` | the operator can reproduce every printed figure in one command |
| A13 | `forall x,y in Code: Style(x) = Style(y)` | a single style rule covers all source files; validator checks it |
| A14 | `forall q in IO: q = Parameterized (not exists inj)` | no string-built query, command or selector |
| A15 | `K(Code) = min(K)` | no boilerplate file, no duplicate implementation, no dead module |
| A16 | `Effects = IO_Monad (not exists hidden_mut)` | IO is confined to named entry points; pure core has no IO |
| A17 | `not exists (deferral markers or elision)` | no deferral marker in any committed source line |
| A18 | `AuthZ = ZeroTrust` | every read of a foreign surface states its authority and is checked |
| A19 | `f(f(x)) = f(x)` | the daemon is idempotent; replay of one payload yields one result |
| A20 | `forall i != j: S_i disjoint S_j and R_i disjoint R_j` | one writer per surface; one owner per row |
| A21 | `not exists (UB or Races or Leaks)` | no shared mutable state; every resource has a bound |
| A22 | `lim(n->inf) Contention(n) = 0` | concurrency uses disjoint surfaces, never a contended lock |
| A23 | `Abstraction = Clarke-compliant` | state space is finite and enumerable; model checking covers it |
| A24 | `forall e in Exc: e in Handled or Propagated` | no uncaught panic; every error path is named |

## 1. Mode (choose once, state it in the Traversal Plan)

| | Fail-Closed | Graceful |
|---|---|---|
| Use when | The brief names an invariant, a safety property, money, identity, or "no data loss" | The brief names availability, an audience, an SLO, an edge or offline deployment |
| Governing criterion | The invariant holds in every reachable state (Clarke-compliant abstraction, Pi-type discharge) | **Bounded Optimism**: the ambitious pole (maximum decentralization and resilience) and the acceptable pole (p99-bounded operability) must both hold; if either is weak, revise the move |
| Required critics | Impossibility (Fischer, Lynch, Paterson), Formalist (Clarke, Emerson), Type Theorist (Milner, Martin-Lof), plus at least one more; 7 to 9 seats | Chaos (Basiri, Allspaw), Operability (Beyer, Jones), Erasure (Star, Bowker), plus at least three more chosen for maximum difference |
| Extra record field | Safety pole: the invariant discharged and the model that discharges it | Ambitious pole and Operable pole, each with its anchor and measured bound |

If the person does not name a mode, use **Fail-Closed** unless the brief names
availability, a public audience, an SLO or an edge deployment, and say which you
chose and why. In both modes the panel must include at least one pair of critics
joined by a dotted edge in the graph.

## 2. How the traversal works (non-linear)

You do not walk a list from top to bottom. You keep a **Frontier**: the set of
candidate moves reachable from the anchors already visited, in either direction.
Each quorum round spends one candidate and usually creates several more.

- **Reach** candidates by following every edge touching a visited anchor:
  outgoing solid edges (what the anchor grounds), incoming edges (what grounds
  it), and dotted edges (counterpoints).
- **Choose the next candidate** in this priority order: (1) open Andon
  objections, (2) REOPENED moves, (3) dotted counterpoints of BREAK moves not yet
  applied or declined, (4) the sharpest disagreement between critics in the last
  panel, (5) incoming-edge anchors that would ground what you have already done,
  (6) outgoing solid edges. Among candidates of equal rank, take the one that
  changes the most: a move that alters the state machine outranks one that alters
  a value, and a deletion that removes a competing failure mode outranks an
  addition. This is the leverage tiebreak.
- **Branch**: when two or more Breaker candidates are plausible, make each a
  branch. Write a Decision Record per branch, render each as a spike, run the
  panel on each, compare them in a Pugh-Matrix in the log, and SCRAP the losers.
  Their records stay, marked superseded.
- **Reopen**: every move records what it depends on. When a move is ADAPTed or
  SCRAPped, mark every dependent move REOPENED and put it on the Frontier.
- **Merge**: when two moves interact (consistency against latency, replication
  against edge autonomy), the interaction is itself a candidate; add it to the
  Frontier.

Frontier format, updated after every panel round:

```
## Frontier
| Candidate | Reached via (edge label, direction) | From anchor | Status OPEN / DEFERRED (reason) / TAKEN (Mn) |
```

## 3. Workflow

### Step 0. Tooling inventory (before anything else)

Check your tool list for tooling that handles graphs, workflows, diagrams, task
orchestration or knowledge graphs. Use what exists before falling back to plain
files. Record in the Traversal Plan which tool you used for each job, or "none
available". Do not invent tools, and do not claim a tool was used unless you
called it.

| Job | Use, if available | Fallback |
|---|---|---|
| Render and navigate the anchor graph | Mermaid renderer, graph database, or `graph_walk.py --render` | Mermaid text in `QUORUM-LOG.md` |
| Compute the Frontier | `graph_walk.py --frontier` over `references/anchor-graph.md` | Read the edge lines of the graph and list them by hand |
| Track workflow state | Todo, plan, task-list or workflow-engine tool | A checklist in `QUORUM-LOG.md` |
| Run the panel | One sub-agent per authority, not per critic | Sequential, written one authority at a time, each report fully written before the next is read |
| Persist the log | Docs or artifact tool, in addition to `QUORUM-LOG.md` | `QUORUM-LOG.md` only |
| Discharge axioms | `epistemic_audit.py` and `verify_invariants.py` | A witnessed command per axiom in the log |
| Model-check safety | `epistemic_audit.py --model-check` | Exhaustive finite LTS with a counterexample trace |
| Run the crucible | `epistemic_audit.py --crucible 200` | Control, fault-injected treatment, blast-radius guard |

### Step 1. Traversal Plan (before touching the work)

1. Restate the brief in one sentence. Choose the mode.
2. Run the pre-flight jank checksum on the `STATE_PAYLOAD`. Record the checksum
   result verbatim; a `JANK_DETECTED` fault names the contradiction and the
   repair. A payload that declares itself isolated while requiring external
   sources is a category error: record it, do not silently ignore it.
3. Choose the **seed** from `references/anchor-graph.md`: 1 Stance node, at least
   2 Rules nodes (follow solid edges), 1 Breaker node, and 1 counterpoint reached
   by a dotted edge from a node you chose. The seed is a starting point, not a
   plan; it will grow.
4. Copy every label exactly. Each label must occur verbatim in the graph.
5. Write the chain of labels with the edge label between each pair, then the
   initial Frontier (every candidate one hop from the seed, in both directions),
   then the first move or moves, tagged KEEP-THE-RULE or BREAK. At least one BREAK
   move must eventually be taken.
6. **Premortem, round R0.** If an artifact already exists, convene a WHOLE panel
   round on it as it stands before the first move, and enter its objections as the
   first Frontier candidates.
7. Render the graph and mark visited anchors with the `visited` class, using node
   ids from the graph.

### Step 2. The loop: spend one Frontier candidate per pass

**2a. Decision Record, written BEFORE you make the move:**

```
## Move Mn: <name>  (KEEP-THE-RULE | BREAK)
Depends on: M-ids, or "none"
Anchors: Stance <label> | Rule <label> | Breaker <label> | Counterpoint <label> (dotted edge from <label>)
Intent: what the move does to the state machine and to the operator.
Formal argument: claim, grounds, warrant, citing the anchors.
State delta: the ADT morphism from Gamma_t to Gamma_(t+1), named and total.
Invariant obligations: the axiom IDs this move must discharge.
Alternatives rejected: at least 2, each with the reason.
Consequence: second-order effects, failure modes opened, and what the move costs.
Fence: for any rule being broken, why that rule exists.
Frontier effect: the new candidates this move opens.
Mode field: Safety pole (Fail-Closed) | Ambitious pole and Operable pole (Graceful)
```

**2b. Make the move** in the actual artifact, then render or run it so the panel
can see the measured result. If you cannot run it, write "unrendered" in the
Panel Report and say so in the final reply.

**Measure the move; do not assume it.** Compare the artifact before and after and
record the number that changed: a p99, a quorum size, a replica count, a byte
count, a computed value. A change that measures as identical has not been applied,
whatever the source now says: find the lever that actually moves the work, and log
both the inert attempt and the substitute that worked. Assert on the **computed
value**, never on the fact that your edit went in.

**2c. Convene the panel** on the rendered artifact.

- Composition: the required critics for your mode, chosen from
  `references/critic-panel.md`.
- Independence: if you have a sub-agent or task tool, **one agent per authority,
  not per critic**. Every thinker named in a panel critic, and every text in the
  LENSES cluster, is instantiated as its own agent, arguing from that author's own
  doctrine alone. A two- or three-name critic convenes two or three separate
  agents. No reference may be merged into a composite voice, dropped, or reduced
  to a label, and the run is not compliant while a required critic has never sat
  on the panel. The panel must still meet the mode's composition rule. See
  `references/panel-protocol.md`: a verdict is a file, not a return value.
- Evidence rule: every critic points to something observable in the artifact and
  names one literature anchor that grounds the judgment. A critic that cites only
  the plan is invalid; redo it.
- Run the Critical Response Process in this order: (1) statements of meaning,
  (2) designer questions, (3) neutral questions from critics, (4) opinions, only
  after the designer permits them.
- Any critic may pull the Andon. Stop making new moves until its objection is
  resolved.

Panel Report format:

```
### Panel, Move Mn or WHOLE, round R  (artifact examined: <path or measurement>)
| Critic | Anchor used | Observed in the work | Verdict PASS/OBJECT | Requested change |
Statements of meaning: ...
Designer questions: ...
Critic questions: ...
Opinions: ...
Andon pulled: yes/no, by whom
Quorum certificate: <seats reporting>/<seats required>, <PASS count>/<OBJECT count>
```

**2d. Resolve every OBJECT** with exactly one of:

- **ADAPT**: change the move, re-run it, and re-run at least the objecting critics
  (maximum 3 rounds on one move, after which treat it as a frame swap).
- **SCRAP**: revert the move and mark its Decision Record as superseded; do not
  delete it.
- **OVERRULE**: allowed only with a written reason citing the governing criterion
  of the mode, or with a measurement that refuses the objection's premise. The
  objection stays in the log.

**Test an objection's premise against the artifact before you spend a move on
it.** A critic can be right about what it sees and wrong about what is there.
Measure the premise; if the measurement refuses it, the resolution is OVERRULE
with that measurement recorded. A move spent answering a false premise is a move
the work did not get.

Then mark every dependent move REOPENED. If 3 or more critics object to the same
move or the same anchor region, stop and perform a frame swap: replace that region
with a sibling anchor reached by an existing edge (dotted edges allowed) and log
it as a frame swap.

**2e. Update the Anchor Ledger, the Frontier and the live graph** after every
panel round:

```
| Anchor | Role | Status KEEP / ADAPT / SCRAP | Evidence | Replacement or note |
```

Every anchor named in any record gets a row. A KEEP must name the strongest
objection it survived. Add every new candidate to the Frontier and mark the one
you spent TAKEN. Then update the graph: apply `kept`, `adapted` or `scrapped` to
each anchor's node id, add any replacement anchor reached by an existing edge,
and re-render. Scrapped anchors leave the active path for this project; the
reference file itself is not edited. Do not write moves to please the critics'
score; the governing criterion decides.

**2f. Deletion review and residual diff.** Once, before the stop test: name the
substantial elements of the artifact that predate this run and say what each
earns. Anything that earns nothing is SCRAPped, and the record carries the
retained-value ledger: what the deletion must preserve so the surviving decisions
still read as decisions. For any move that refactors, consolidates or deletes,
attach a **residual diff** to its record: every computed value or behaviour that
changed, each classified intended / inert / regression, with regressions fixed
before the next move. The largest single improvement a run can make is often a
deletion; a run that only added has not looked.

**2g. Re-measure the artifact's own evidence at its final state.** Before the
stop test, and again after any change made after it: list every number, ratio,
count or measured claim the *artifact* displays to its own audience, and
re-measure each against the artifact as it now stands, by the procedure the
artifact states or implies. One row each: the printed figure / the procedure that
reproduces it / the value at the final state / reproducible or corrected. Correct
or delete every figure that drifted. Evidence the artifact cannot let anyone
reach is given a procedure or deleted. The same rule binds this log: a
verification row is evidence only if it was measured **after** the edit it
verifies. Run 2g after the last edit to the artifact and never earlier.

### Step 3. Whole-artifact rounds

Moves that pass alone can fail together. Run a **WHOLE** panel round on the entire
artifact whenever a cluster of related moves settles, whenever the Frontier
changes substantially, and always before the stop test. Objections raised here
about interactions become new Frontier candidates or REOPENED moves. Whole rounds
are not capped, but if 3 consecutive WHOLE rounds each produce a new OBJECT, do
not make another move: perform a frame swap or a double-loop revision of the
criterion, panel or graph instead.

### Step 4. Stop test and close

Do not close until all of these hold and Step 2g has been run against the
artifact in its final state. If any fails, go back to Step 2.

- **S1.** The Frontier has no OPEN items; each is TAKEN or DEFERRED with a
  recorded reason.
- **S2.** A WHOLE panel round returned PASS from every required critic with no
  Andon.
- **S3.** Saturation: two consecutive WHOLE rounds produced no ADAPT, SCRAP,
  REOPEN or new OPEN Frontier item.
- **S4.** Crucible push: you deliberately escalated the boldest move under
  injected partition and max load, and logged the result, **including what
  changed in the measured work**: a measured delta, or the measured finding that
  the intended lever was inert and which lever moved instead. A push that cannot
  be shown to have changed anything does not satisfy S4. A push is a move; if it
  survives, S2 and S3 must be satisfied again with it in place.
- **S5.** Every dotted edge leaving an anchor you used is either applied or
  declined with a recorded reason.
- **S6.** The pre-flight jank checksum on the final `STATE_PAYLOAD` returns
  `[DERIVED]`, with no fault code outstanding.
- **S7.** Every axiom in the Axiom Ledger has a live witness in the Compliance
  Check.
- **S8.** The daemon replay is idempotent: two runs over the same payload produce
  the same digest.

Then close:

1. **Double loop.** In one paragraph, say whether the criterion, the panel or
   the graph itself failed the work, and name one concrete amendment under
   "Graph amendments". Then write the **Carry-Forward Ledger**: the durable,
   domain-specific facts this run established by measurement, of the kind a
   later run in this medium would otherwise rediscover the hard way. One line
   each: the fact, the measurement that established it, and the move it changed.
   Keep it in `QUORUM-CARRY-FORWARD.md` and read that file before Step 1 of any
   later run on the same project.
2. **Compliance Check**, each line with a pointer to where it is satisfied:
   - [ ] Tooling inventory done; tool used for each job, or "none available"
   - [ ] Mode stated with the reason
   - [ ] Pre-flight jank checksum recorded
   - [ ] Seed with exact labels, including one dotted-edge counterpoint, and a
     living Frontier
   - [ ] At least one BREAK move taken, and no quota used as a stopping rule
   - [ ] A Decision Record written before each move, with all fields filled
   - [ ] A Panel Report per round from a panel meeting the mode's composition
     rule, each critic citing something observable
   - [ ] Every OBJECT resolved as ADAPT, SCRAP or OVERRULE, with dependents
     reopened
   - [ ] WHOLE rounds run; S1 to S8 each shown as met, with where
   - [ ] Every figure the artifact displays re-measured at the final state
   - [ ] Anchor Ledger complete and the live graph updated
   - [ ] Double-loop paragraph written
   - [ ] Final reply states the mode, the tools used, the stop conditions and
     everything skipped

## 4. Anti-skip rules

- An escalation you did not measure is not an escalation, and a patch you did not
  verify at the computed value is not a change.
- A move count is never a stopping criterion. Stopping because the first pass felt
  complete is a skip.
- A linear walk down a list is not a traversal: follow incoming and dotted edges,
  branch, and reopen settled moves.
- A commit message or code comment is not a Decision Record.
- A quick mental check or a one-line "I considered X" is not a panel.
- Naming an anchor is not using it: it must appear in a record's argument or in a
  critic's observation, tied to something in the work.
- Not looking for graph or workflow tooling is not the same as none being
  available.
- Short on effort is not an exemption. If an external limit forces a stop, write
  the Open frontier and say the run is incomplete; do not claim the stop
  conditions held.
- A verdict that exists only in a return value is not a verdict. It must be a
  file, collected by `collect_panel.py`.

## 5. Reading the graph

Solid arrows are forward references (grounds, extends, applies). Dotted arrows
are counterpoints or back-references. Boxes are clusters; an arrow into the
CRITICS box means the whole panel. Colors: amber stance, grey rules, pink
breakers, violet physics, green systems, slate canon, teal operations, orange
edge, red critics, magenta lenses, cyan panel method, lime adaptation, blue
catalog anchors, gold verification. Status classes for the live graph:
`visited`, `kept`, `adapted`, `scrapped`.

Read [references/anchor-graph.md](references/anchor-graph.md) before choosing
the seed and the panel. Copy labels from it exactly. The rest of the reference
set is a map, not a reading order:

| File | What it carries |
|---|---|
| [references/critic-panel.md](references/critic-panel.md) | seats, lens bindings, counterpoint closure |
| [references/panel-protocol.md](references/panel-protocol.md) | transport-safe rounds, one agent per authority |
| [references/invariant-ledger.md](references/invariant-ledger.md) | axiom-to-witness map |
| [references/fault-taxonomy.md](references/fault-taxonomy.md) | the four fault codes and the exception model |
| [references/canon.md](references/canon.md) | source and provenance of every anchor |
| [references/primary-texts.md](references/primary-texts.md) | SRE and DDIA chapter-to-node map, read during the build |
| [references/traversal-ledger.md](references/traversal-ledger.md) | one measured verdict per node |
| [references/field-notes.md](references/field-notes.md) | carry-forward facts established by measurement |
| [references/model-assumptions.md](references/model-assumptions.md) | the FLP bound and the assumptions that discharge liveness |
| [references/research-report.md](references/research-report.md) | cited extract-stage research, explicitly not yet verified |

The executable forms of the walk and the daemon are
`skills/quorum/scripts/graph_walk.py` and
`skills/quorum/scripts/epistemic_audit.py`. A run is not compliant while a
required verdict file is missing: `collect_panel.py` decides the quorum.
