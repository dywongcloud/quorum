# QUORUM field notes: durable facts established by measurement

These are facts about the medium (distributed systems design and its
verification tooling), established by a command in this repository. Each row
says the measurement that established it and the move it changed. Read this
file before Step 1 of a later run on this project.

No row here is a claim about a future state of the repository. Where a number
moves, the row names the procedure that re-measures it instead of freezing the
number.

## Boundary ledger

An affine typestate at a Byzantine boundary: each row names the boundary, the
typestate before the read, and the trust assumption. `trust` is never implicit;
`typestate` is consumed once by the read.

| Boundary | Typestate | Trust | Detail |
|---|---|---|---|
| client_edge | Unauthenticated | zero-trust | capability token required |
| edge_region | CapabilityHeld | mTLS | identity checked per hop |
| region_quorum | QuorumCandidate | quorum | f+1 of 2f+1 replicas agree |
| quorum_storage | Committed | fencing | token checked on every write |
| storage_snapshot | SnapshotHeld | checksum | verified before derivation |
| operator_read | Audited | procedure | every printed figure has a procedure |

## Measurement facts

1. **A launch count is not a quorum.** With no verdict files yet present,
   `collect_panel.py panel/R1 --roster fail-closed --json` reported
   `seats_required: 14`, `seats_reporting: 0`, `quorum: false`. A caller that
   counted launched seats would have reported 14 of 14. The checker counts
   files, and the run keeps that rule. Re-measure with the same command after
   the seats file; do not read a frozen number from this note.

2. **Cluster index is not a topological rank.** The first graph builder
   rejected 88 real cross-cluster references such as Dynamo grounding sloppy
   quorums, because it compared cluster indices. A topological sort of the
   actual edges found seven strongly connected components; after breaking the
   weaker direction of each two-cycle, `validate_graph.py` reported
   `acyclic: true` with 400 nodes and 394 edges. Changed: the seed selection in
   the Traversal Plan, which had assumed stance nodes always precede rules
   nodes.

3. **A fault code is cheaper than interpolation.** `epistemic_audit.py
   --selftest` returns 5 of 5 cases: clean, contradiction, unmapped,
   unstated-assumption and dangling-edge. `state/unmapped.json` returns
   `STATE_UNMAPPED` naming the missing symbol. The daemon has no default-value
   path for an unbound symbol.

4. **Pre-flight must gate every mode, not only the default one.** An
   adversarial scout ran `--replay` and `--enumerate` against
   `state/jank-contradiction.json`: both returned success with no fault code,
   and `apply()` appended a context frame to a rejected payload. The run added
   a pre-flight check before all modes and made `apply()` a no-op on a corrupt
   state. The four A24 probes now assert this live.

5. **A traceback on the I/O port is a fault, not a diagnosis.** A payload with
   `rules: null` produced `TypeError` on stderr with empty stdout; a Mermaid
   block containing a `%%` comment produced `ValueError: unparsed graph line`.
   Both are now handled: `parse_state` types the field, `graph_walk.py` accepts
   inert comment lines, and `guarded_main` emits a JSON `JANK_DETECTED` with
   mode `engine-internal` for an unexpected exception. A24 discharges this by
   running the malformed inputs, not by scanning source text.

6. **Replay detects a second mutation.** `--replay` on `state/clean.json`
   emits one digest twice and checks composition `f(f(x)) = f(x)`. The
   Compliance Check records a digest from `verify_invariants.py --digest`
   after the last edit; a stale digest is a rejected claim, not a warning.

7. **A timing p99 is a sample, not a constant.** `--probe 400` reported p99
   0.2263 ms on one run and 0.8234 ms on a later run on the same machine;
   `--probe 4000` reported 0.3864 ms. The landing page therefore prints the
   sample count and the procedure, never a fixed timing figure. Re-measure
   with `python3 -I skills/quorum/scripts/epistemic_audit.py --probe 400`.

8. **A minority partition removes the quorum without raising a fault.**
   `state/partition.json` returns `derived: false` with `chain: []` and no
   fault code; `state/max-load.json` returns `derived: true` with a five-rule
   chain. The Crucible move measures degradation as a derived-value delta, not
   as an exception.

9. **A required critic counterpoint pair must sit together.** `--roster
   --mode fail-closed` grew a 7-seat seed to 14 seats in one closure round.
   Panel batches are computed from the roster, never hand-assembled.

10. **A figure measured before the last edit is a phantom witness.** An
    independent scout found that `QUORUM-LOG.md` recorded A20 as PASS with a
    28-file witness while the live checker reported 0 files and FAIL. The log
    was corrected to cite a command and a count produced after the verdicts
    file, and `validate_figures.py` recomputes every printed figure from the
    final tree. This is the Step 2g rule applied to the log itself.

11. **A checker that names its own detection tokens in source trips itself.**
    `verify_invariants.py` assembles deferral markers and secret shapes with a
    `tok()` helper, so A17 and A10 scan the code rather than the checker's
    literal strings. Detection tokens are data, not prose.

## Instrument check

A finding that appears only in a tool's output must be measured on the rendered
artifact before a move is spent on it. A contrast sampler once reported a
failure caused by a static server not applying cleanUrls; the same class of
error appears here when a graph validator reads a stale generated file. The
repair is always: regenerate, compare bytes, then judge the artifact.
