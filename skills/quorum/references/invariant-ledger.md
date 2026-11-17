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
| A4 | anchor graph is a strict DAG | `--axiom A4` | `graph_walk.py --check-dag` |
| A5 | every latency or capacity claim cites a bound | `--axiom A5` | `references/canon.md` bounds table |
| A6 | every boundary states typestate and trust | `--axiom A6` | `references/field-notes.md` boundary rows |
| A7 | sampled probes report sample count and p99 | `--axiom A7` | `epistemic_audit.py --probe` output |
| A8 | all declared obligations discharge | `--axiom A8` | `verify_invariants.py --all` |
| A9 | degradation has a stated budget | `--axiom A9` | Traversal Plan mode field |
| A10 | no unchecked resource, no secret literal | `--axiom A10` | source scan in `verify_invariants.py` |
| A11 | one move under injected partition and max load | `--axiom A11` | `QUORUM-LOG.md` Move M-crucible |
| A12 | operator reproduces every printed figure in one command | `--axiom A12` | `scripts/validate_figures.py` |
| A13 | one style rule covers all source files | `--axiom A13` | source scan in `verify_invariants.py` |
| A14 | no string-built query, command or selector | `--axiom A14` | source scan in `verify_invariants.py` |
| A15 | no duplicate implementation or dead module | `--axiom A15` | module inventory in `verify_invariants.py` |
| A16 | IO confined to named entry points | `--axiom A16` | source scan in `verify_invariants.py` |
| A17 | no deferral marker in committed source | `--axiom A17` | source scan in `verify_invariants.py` |
| A18 | every foreign read states its authority | `--axiom A18` | `references/canon.md` provenance column |
| A19 | replay of one payload yields one result | `--axiom A19` | `epistemic_audit.py --replay` |
| A20 | one writer per surface, one owner per row | `--axiom A20` | `.gm/prd/` row ownership check |
| A21 | no shared mutable state, bounded resources | `--axiom A21` | source scan in `verify_invariants.py` |
| A22 | concurrency uses disjoint surfaces | `--axiom A22` | panel batch ledger in `QUORUM-LOG.md` |
| A23 | state space finite and enumerable | `--axiom A23` | `epistemic_audit.py --enumerate` |
| A24 | no uncaught panic, every error named | `--axiom A24` | `references/fault-taxonomy.md` plus source scan |

The commands are read-only. They never mutate the payload they measure. The
Compliance Check in `QUORUM-LOG.md` records the exact stdout digest of
`verify_invariants.py --all` at the final state, and Step 2g re-runs it after
the last edit so the recorded digest cannot be stale.
