# QUORUM critic panel

The panel is not DADA's art panel. Every seat is one authority from
distributed-systems theory, infrastructure, operations, or formal verification.
A named critic with two thinkers is two seats, never one composite voice: on a
sub-agent run each authority is its own agent, arguing from the single text
bound to it in `skills/quorum/references/anchor-graph.md` (the `LENSES` cluster).
The binding is mechanical: `graph_walk.py --seat <id>` prints the lens id and
label a seat argues from, and nothing else.

## Composition

Seed seats are fixed by the mode. The **counterpoint closure** then adds every
seat joined by a dotted critic edge to a seed seat, recursively, until the set
stops growing. A dotted pair is a joint obligation: neither member may be
reported without the other. `graph_walk.py --roster --mode <mode>` computes the
roster deterministically from the graph, so no panel is hand-assembled.

### Fail-Closed seed (safety-dominant)

| Seat id | Label | Bound lens |
|---|---|---|
| `crit_imp_fischer` | Critic: Impossibility (Fischer) | `lens_flp` |
| `crit_imp_lynch` | Critic: Impossibility (Lynch) | `lens_flp` |
| `crit_imp_paterson` | Critic: Impossibility (Paterson) | `lens_flp` |
| `crit_form_clarke` | Critic: Formalist (Clarke) | `lens_clarke` |
| `crit_form_emerson` | Critic: Formalist (Emerson) | `lens_emerson` |
| `crit_type_milner` | Critic: Type Theorist (Milner) | `lens_milner` |
| `crit_type_martinlof` | Critic: Type Theorist (Martin-Lof) | `lens_martinlof` |

At least one further seat is chosen for maximum difference and named in the
Traversal Plan. The counterpoint closure then applies.

### Graceful seed (bounded degradation)

| Seat id | Label | Bound lens |
|---|---|---|
| `crit_chaos_basiri` | Critic: Chaos (Basiri) | `lens_basiri` |
| `crit_chaos_allspaw` | Critic: Chaos (Allspaw) | `lens_allspaw` |
| `crit_ops_beyer` | Critic: Operability (Beyer) | `lens_beyer` |
| `crit_ops_jones` | Critic: Operability (Jones) | `lens_jones` |
| `crit_erasure_star` | Critic: Erasure (Star) | `lens_star` |
| `crit_erasure_bowker` | Critic: Erasure (Bowker) | `lens_bowker` |

At least three further seats are chosen for maximum difference. The
counterpoint closure then applies.

### Why Erasure sits on this panel

Infrastructure work has a canon that names systems, papers and their authors.
It also has labor that the canon does not name: the on-call rotation, the
classification work, the operator who kept a degraded service alive. Susan Leigh
Star and Geoffrey Bowker supply the doctrine. Their seat objects when the
artifact prints a system diagram whose human dependencies are absent, or when a
quorum certificate counts agents but not the people who would run the design.
This is the counterpoint to Critic: Historian (Stonebraker).

## Quorum certificate

A round is valid only when every required seat has filed a verdict file. The
certificate is `seats_reporting / seats_required` plus `PASS / OBJECT` counts,
computed by `collect_panel.py`. A missing seat is `NOT REPORTED`, never PASS and
never reconstructed. Fewer than the required number of seats means no quorum,
which means S2 is not met.

## Andon

Any seat may pull the Andon. Work stops until the objection is resolved as
ADAPT, SCRAP, or OVERRULE with a written reason citing the governing criterion
or a measurement that refuses the objection's premise. Three or more seats
objecting to the same anchor region force a frame swap.

## Evidence rule

Each verdict names one observable in the artifact and one literature anchor
that grounds the judgment. A verdict that cites only the Traversal Plan is
invalid and the seat is re-run. A verdict that asserts a number without the
command that reproduces it is invalid.

## Independence

No seat reads another seat's verdict before filing its own. On a sub-agent run,
the file is the verdict: the seat writes `panel/<round>/<seat>.md` as its last
action and returns the same text. `panel-protocol.md` holds the transport rules,
including the three-seat batch limit and the three-attempt retry bound.
