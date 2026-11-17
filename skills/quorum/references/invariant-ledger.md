# QUORUM invariant ledger

Every axiom in `SKILL.md` section 0.3 has one row here. The row names the
predicate, the command that discharges it, and the artifact that carries the
witness. `verify_invariants.py` runs the commands and prints one JSON object per
axiom with `status`, `measured` and `witness`. A row with status other than PASS
is a blocking OBJECT in the Compliance Check.

| ID | Predicate | Discharge command | Witness |
|---|---|---|---|
| A1 | frozen `State` with pure transitions | `python3 -I skills/quorum/scripts/verify_invariants.py --axiom A1` | `epistemic_audit.py` State dataclass and replay digest |
| A2 | each round removes an open condition | `--axiom A2` | `QUORUM-LOG.md` Frontier deltas |
| A3 | rival branches scored by measured behaviour | `--axiom A3` | Pugh-Matrix rows in `QUORUM-LOG.md` |
| A4 | anchor graph is a strict DAG, CAP sacrifice declared | `--axiom A4` | `graph_walk.py --check-dag` plus `model-assumptions.md` |
| A5 | every latency or capacity claim cites a bound | `--axiom A5` | `references/canon.md` bounds table |
| A6 | every boundary states typestate and trust | `--axiom A6` | `references/field-notes.md` boundary rows |
| A7 | sampled probes report sample count and p99 budget | `--axiom A7` | `epistemic_audit.py --probe` output |
| A8 | all declared obligations discharge | `--axiom A8` | `verify_invariants.py --all` |
| A9 | degradation has a stated budget | `--axiom A9` | Traversal Plan mode field |
| A10 | no unchecked resource, no secret literal | `--axiom A10` | source scan in `verify_invariants.py` |
| A11 | one move under injected partition and max load | `--axiom A11` | `QUORUM-LOG.md` Move M8 and M12 |
| A12 | operator reproduces every printed figure in one command | `--axiom A12` | `scripts/validate_figures.py` |
| A13 | one style rule covers all source files | `--axiom A13` | source scan and `--schemes` |
| A14 | no string-built query, command or selector | `--axiom A14` | source scan in `verify_invariants.py` |
| A15 | no duplicate implementation or dead module | `--axiom A15` | module inventory in `verify_invariants.py` |
| A16 | IO confined to named entry points | `--axiom A16` | source scan and `--proof A16` |
| A17 | no deferral marker in committed source | `--axiom A17` | source scan in `verify_invariants.py` |
| A18 | every foreign read states its authority | `--axiom A18` | `references/canon.md` provenance column |
| A19 | replay of one payload yields one result | `--axiom A19` | `epistemic_audit.py --replay` |
| A20 | one writer per surface, one owner per row | `--axiom A20` | `.gm/prd-log.jsonl` resolved rows |
| A21 | no shared mutable state, bounded resources | `--axiom A21` | source scan in `verify_invariants.py` |
| A22 | concurrency uses disjoint surfaces | `--axiom A22` | panel batch ledger in `QUORUM-LOG.md` |
| A23 | state space finite and enumerable | `--axiom A23` | `epistemic_audit.py --model-check` |
| A24 | no uncaught panic, every error named | `--axiom A24` | four live malformed-input probes |

## Coverage of the initiating brief

Every clause of the brief's invariant set maps to at least one axiom. No
clause is left as decoration. The mapping is checked by reading this table;
an unmapped clause is a blocking OBJECT from Critic: Type Theorist (Martin-Lof).

| Brief clause | Axiom | Article carrying the live witness |
|---|---|---|
| `f compose f = f` | A19, A23 | M4, M11 |
| `S_i disjoint S_j`, `R_i disjoint R_j` | A20, A22 | M3, Artifact 3 batch table |
| `not exists (UB or Races or Leaks)` | A21, A24 | M10, M11 |
| `lim Contention(n) = 0` | A22 | M3, M10 |
| `Abstraction = Clarke-compliant` | A23 | M11, `model_check()` |
| `forall sigma in AST: sigma in Gamma_real` | A4, A18 | M5, `validate_canon.py` |
| `forall n in AST: n = Expanded` | A17, A15 | M7, M10 |
| `Gen = argmin(DeltaSpec) minus Sycophancy` | A3, A8 | M6, Artifact 5 |
| `forall e in Exc: e Handled or Propagated` | A24 | M4, `fault-taxonomy.md` |
| `forall k in Secrets: k not in AST` | A10 | M4 |
| `forall f: f proves Spec` | A16, A23 | M4, M11 |
| `Gamma_t superset Gamma_(t-1)` | A1, A19 | M4, `context` monotonicity check |
| `State = ADT-isomorphic pure morphisms` | A1 | M4 |
| `Entropy = Subtractive` | A2 | Artifact 1 Frontier deltas |
| `Ontogeny = Stochastic empirical fitness` | A3, A7 | M6, M12 |
| `Topology = Monoidal strict DAG` | A4 | M5, M9 |
| `Physics = Hardware-bounded CAP-aware` | A5, A9 | M1, `model-assumptions.md` |
| `Boundaries = Affine typestate Byzantine` | A6 | `field-notes.md` boundary ledger |
| `Epistemology = Profiling Monte Carlo` | A7 | M12 |
| `Correctness = Pi-types static verification` | A16, A23 | `--proof A16`, `--schemes` |
| `Resilience = p99-bounded graceful` | A7, A9 | M1, M8 |
| `Contracts = Strict semantics zero-leak` | A10, A14 | M4 |
| `Crucible = Chaos max-load` | A11 | M8, M12 |
| `Teleology = Utility max (DX/UX)` | A12 | M7, `measure_web.py` |
| `Style(x) = Style(y)` | A13 | M10 |
| `forall q in IO: q Parameterized` | A14 | M4 |
| `K(Code) = min(K)` | A15 | M6, M10 |
| `Effects = IO_Monad` | A16 | M4 |
| `not exists (TODO or FIXME or elision)` | A17 | M10 |
| `AuthZ = ZeroTrust` | A6, A10 | `model-assumptions.md` |

The commands are read-only. They never mutate the payload they measure. The
Compliance Check in `QUORUM-LOG.md` is generated by
`tools/build_compliance.py` from live command exit statuses at final state,
and Step 2g re-runs it after the last edit so no recorded digest can be stale.
