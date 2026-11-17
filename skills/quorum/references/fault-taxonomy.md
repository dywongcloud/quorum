# QUORUM fault taxonomy

The `EPISTEMIC_AUDIT_DAEMON` has four terminating faults. A fault terminates a
query, not the run. It is machine-readable, names its failure mode, and never
contains prose outside the `reason` field. Every fault is recorded in the
Compliance Check with the query id that caused it and the repair that followed.

## `[FAULT: JANK_DETECTED]`

Pre-flight structural integrity. Four failure modes:

| Mode | Detection in `STATE_PAYLOAD` | Example |
|---|---|---|
| `logical-contradiction` | a declared axiom and its negation both asserted | "the system is CP" and "the system is AP" in one payload |
| `undefined-variable` | a query atom names a symbol absent from `state.variables` | `quorum.write_quorum` with no declared `write_quorum` |
| `category-error` | a boolean field holds a non-boolean, or a node id is used as a value | `linearizable: "maybe"` |
| `structural-decay` | duplicate node id, dangling edge, truncated record, phantom symbol | an AST node referenced by an edge but never declared |

Jank is detected before derivation. The engine does not process a corrupted
payload, does not repair it silently, and does not interpolate a missing value.
The repair is explicit and is written into the log as a new payload version.

## `[FAULT: STATE_UNMAPPED]`

Strict 1:1 state mapping. The engine returns the exact missing variable or axiom
name. It never substitutes a default, a synonym, or a value from another run.
`Gen = argmin(DeltaSpec) minus Sycophancy`: a plausible-looking answer that the
payload does not bound is worse than a fault.

## `[FAULT: SELF_REJECTED]`

Meta-cognitive loopback. Before emitting `[DERIVED]`, the engine attempts to
falsify its own derivation. Three rejection reasons:

| Reason | Test |
|---|---|
| `unstated-assumption` | a derivation step uses a rule not declared in `state.rules` |
| `probabilistic-guessing` | a step consults a random or fitted value instead of a declared value |
| `logical-leap` | the conclusion does not follow from the rule chain under boolean evaluation |

A rejection keeps its attempted chain in the log. The chain is evidence of the
falsification attempt, not a result.

## `[FAULT: IO_FAULT]`

Serialized output only. The I/O port accepts JSON, YAML, or a rigid Markdown
table. Conversational text, affective tokens, apologies, hedges, or unbound
prose in an emitted record are rejected. A fault is emitted as JSON whose only
keys are `fault`, `code`, `reason`, `query_id`, `digest`.

## Non-fault results

`[DERIVED]` is emitted as JSON with keys `derived`, `query_id`, `chain`,
`state_digest`, `context_digest`, `faults_cleared`. `chain` is a list of rule
ids in evaluation order. It is total: every step names a declared rule.

## Exception model

Every exception is handled or propagated. The engine has no bare panic, no
unchecked unwrap, and no hidden mutation. An unexpected exception is converted
into `[FAULT: JANK_DETECTED]` with mode `engine-internal` and a stable digest;
it is never swallowed and never printed as a traceback to the I/O port. This
satisfies `forall e in Exc: e in Handled or Propagated`.

## Idempotence

`f(f(x)) = f(x)` is checked by replaying the same payload twice and comparing
SHA-256 digests of the emitted JSON with the volatile `emitted_at` field
removed. A mismatch is `[FAULT: SELF_REJECTED]` with reason
`non-idempotent-replay`.
