# QUORUM model assumptions

This file exists because a panel seat objected that a DAG check supplies no
witness that quorum nodes decide under a crash fault. The objection was
resolved by ADAPT, not OVERRULE: the declaration below is now part of the
contract, and the anchor graph carries an explicit assumption node.

## What QUORUM claims

QUORUM verifies **design derivations**, not the liveness of a deployed
consensus protocol. Its state payload is finite, its rule set is declared, and
its derivation terminates because the rule chain is a strict DAG. That
termination is a property of the derivation engine, not of Paxos, Raft or any
replicated state machine.

The daemon therefore never emits a claim of the form "the system decides".
`[DERIVED]` means "this proposition follows from the declared axioms under the
declared rules". It does not mean "a quorum of replicas reached agreement".

## The FLP bound, stated explicitly

Fischer, Lynch and Paterson (JACM 32(2), 1985) prove that in a completely
asynchronous system no deterministic consensus protocol is totally correct in
spite of one fault: every protocol has a possible nonterminating run. QUORUM
does not attempt to refute that. Any anchor that describes a deployed consensus
mechanism carries one of these stated assumptions:

| Mechanism | Assumption that discharges liveness | Anchor |
|---|---|---|
| Paxos, Multi-Paxos | partial synchrony or a leader-election failure detector | `paxos`, `multipaxos`, `leaderelection` |
| Raft | leader election with randomized timeouts under partial synchrony | `raft`, `leaderelection` |
| PBFT, Tendermint | weak synchrony plus a bound of f Byzantine replicas in 3f+1 | `pbft`, `tendermint`, `byzgen` |
| Failure detectors | the Chandra-Toueg hierarchy, named per class | `failuredetector`, `phiaccrual` |
| Randomized consensus | local coin flips, probabilistic termination | `flp` |

Safety properties are held with zero timing assumptions. Liveness properties
are conditional on the row above. A record that asserts liveness without naming
its row is an OBJECT from Critic: Impossibility (Fischer), and the run stops
until it is repaired.

## Why the graph is still a DAG

`graph_walk.py --check-dag` discharges axiom A4 over the anchor graph. A DAG of
design anchors and a consensus protocol are different objects. The former has
no crash-prone processes and no message delays; the latter does. The FLP
assumption node, `flpbound`, is reached by a dotted counterpoint edge from
`flp` so that no traversal of the impossibility anchor can skip the bound.

## Synchrony bound

The derivation engine is asynchronous with no bound on message delay or
process pause; it makes no liveness claim. The panel's convergence contract
assumes partial synchrony for file delivery: a verdict file is durable on disk
at the moment the seat writes it, and the collector commits only after every
required file exists. There is no timeout and no election of a leader that can
partition the panel. Under an unbounded delay the panel does not converge and
S2 stays NOT MET; the run records that rather than guessing.

## Measurement

`state/flp-bound.json` encodes the assumption as a payload. The daemon returns
`[DERIVED]` with a chain that names the assumption rule; it never returns a
termination claim. `verify_invariants.py --axiom A4` re-checks the graph after
the node was added, and `validate_figures.py` re-measures the printed counts.

## CAP sacrifice under partition

Under a network partition QUORUM sacrifices **availability** for
**consistency** in Fail-Closed mode: a derivation that cannot name a quorum
returns `[FAULT: STATE_UNMAPPED]` rather than a plausible value. Graceful mode
sacrifices **consistency** of the derived set for **availability**, with the
degradation bounded by the stated p99 budget and recorded as a measured delta.
No row in this artifact claims both C and A under partition. A4 refuses to
pass unless this declaration is present, and `collect_panel.py --json` refuses
a quorum unless every required verdict file exists.

## Quorum arithmetic and the intersecting-majority objection

Critic: Consensus (Lamport) asked for a ballot-numbered intersecting majority
of eight instead of all fourteen seats. A counterexample measurement refuses
the premise: the roster has 14 seats and 23 dotted counterpoint pairs, so an
8-seat majority can omit both members of a required pair. With 14 required
seats, every pair has at least one member present and the closure rule pulls
in the other. The panel therefore keeps the unanimity rule; each filed verdict
still carries a ballot number, its dispatch id and its session id so that a
reader can reconstruct the vote order. `collect_panel.py --quorum` prints the
intersection check that decides this, and `--replication` prints the term,
leader and per-seat durable-copy evidence.

## Crash-fault schedule

`analysis/fault-schedule.json` records one crash-fault schedule with its
timing model. No consensus liveness claim is made over that schedule.
