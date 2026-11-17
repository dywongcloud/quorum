# Adversarial frame findings (as reported)

Two of three frame scouts reported. The third, canon fidelity, did not
report before its transport was stopped; its finding is recorded as
NOT REPORTED, never reconstructed. Findings are the scouts own words.
Each was resolved by an ADAPT described in QUORUM-LOG.md.

## F1: Surface inventory: claim-bearing files -> verifying command, and the coverage gap

Severity: minor

Snapshot 2026-11-16 23:08 local. NOTE: the tree is being written concurrently by other agents (README.md, AGENTS.md, QUORUM-LOG.md, QUORUM-CARRY-FORWARD.md, tools/run_traversal.py, state/initiating-brief.json, state/max-load.json, state/partition.json all appeared during this audit); re-run before acting. Command: python3 -I -c 'import pathlib; r=pathlib.Path("/Users/dylanwong/projects/quorum"); f=[p.relative_to(r).as_posix() for p in r.rglob("*") if p.is_file() and not any(x in p.parts for x in (".git",".gm","__pycache__")) and not p.relative_to(r).as_posix().startswith(".agentplug")]; print(len(f))' -> claim_bearing_candidates 43. Command: python3 -I -c 'import pathlib,re; t=pathlib.Path("/Users/dylanwong/projects/quorum/.github/workflows/validate.yml").read_text(); print("ci_run_steps",len(re.findall(r"^\s*- run:",t,re.M)))' -> ci_run_steps 9.

MAP (absolute paths under /Users/dylanwong/projects/quorum/):
- README.md, AGENTS.md, QUORUM-LOG.md, QUORUM-CARRY-FORWARD.md -> cd /Users/dylanwong/projects/quorum && python3 -I skills/quorum/scripts/verify_invariants.py --all (partial); no dedicated command for prose claims.
- skills/quorum/SKILL.md -> python3 -I scripts/validate_skills.py (frontmatter/links), python3 -I skills/quorum/scripts/verify_invariants.py --all (axiom ledger).
- skills/quorum/agents/openai.yaml, .agents/skills/quorum symlink -> python3 -I scripts/validate_skills.py.
- .github/workflows/validate.yml -> run its 9 steps locally; .github/workflows/pages.yml -> no local command.
- skills/quorum/references/anchor-graph.md -> python3 -I scripts/validate_graph.py; graph_walk.py --check-dag / --counts.
- references/canon.md -> verify_invariants.py --axiom A5 and --axiom A18 (row count only; no coverage check).
- references/critic-panel.md -> graph_walk.py --roster --mode fail-closed / --seat <id>.
- references/fault-taxonomy.md -> epistemic_audit.py --selftest plus malformed-payload probe.
- references/field-notes.md -> --axiom A6; collect_panel.py (claimed R1/R2 measurements).
- references/invariant-ledger.md -> verify_invariants.py --axiom A1..A24.
- references/panel-protocol.md, traversal-ledger.md -> collect_panel.py; --axiom A22; traversal-ledger.md has NO validator reference (verified: validator_refs_to_traversal_ledger 0).
- scripts/validate_skills.py, validate_graph.py, validate_figures.py -> run each of the three.
- skills/quorum/scripts/epistemic_audit.py -> --selftest, --replay, --probe 400, --enumerate, --payload <file>.
- skills/quorum/scripts/graph_walk.py -> --counts, --check-dag, --frontier, --render, --label, --seat.
- skills/quorum/scripts/verify_invariants.py -> --all, --digest, --axiom A<n>.
- skills/quorum/scripts/collect_panel.py -> panel/R1 and panel/R2 rosters.
- state/*.json (9 files) -> python3 -I skills/quorum/scripts/epistemic_audit.py --payload state/<name>.json.
- tools/build_graph.py -> validate_graph.py; tools/build_ledger.py -> byte compare against traversal-ledger.md; tools/run_traversal.py -> NO command (validator_refs_to_run_traversal 0).
- web/index.html -> validate_figures.py (15 data-figure attributes only); web/script.js, style.css, install.css, favicon.svg, .nojekyll -> no command; hero SVG numeric claims unverified (data_figure_in_hero 0).
- .gitignore -> git check-ignore -v; .gm/prd/*.yml (11 rows) -> --axiom A20 ownership check; .gm/* and .agentplug* are machine state, not claims.

PASSING at snapshot: validate_skills.py (Valid skill: quorum), validate_graph.py (byte_identical true, 397 nodes, 391 edges, acyclic true), epistemic_audit.py --selftest (5/5), --replay (idempotent), --probe 400, --enumerate, graph_walk.py --counts and --check-dag, all 9 state payloads, ast.parse(feature_version=(3,10)) on all 10 .py files (supports web/index.html's Python 3.10 claim).

## F2: BLOCKER: zero panel verdict files make 4 CI steps and the axiom suite fail

Severity: blocker

Files: /Users/dylanwong/projects/quorum/panel/R1/ and panel/R2/ are empty; .github/workflows/validate.yml lines 22-23 require both rosters to report.

Command: python3 -I -c 'import pathlib; r=pathlib.Path("/Users/dylanwong/projects/quorum/panel"); print("verdict_files",len(list(r.glob("R*/*.md"))),"dirs",[d.name for d in r.iterdir() if d.is_dir()])' -> verdict_files 0 dirs ['R1', 'R2'].

Command: cd /Users/dylanwong/projects/quorum && python3 -I skills/quorum/scripts/collect_panel.py panel/R1 --roster fail-closed --json -> RC 1, seats_required 14, seats_reporting 0, quorum false, all 14 seats MISSING. Same command with panel/R2 -> RC 1, 0/14.

Command: cd /Users/dylanwong/projects/quorum && python3 -I scripts/validate_figures.py -> RC 1, all_reproducible false; row {"figure":"panel_verdicts","printed":[28],"computed":0,"reproducible":false}.

Command: cd /Users/dylanwong/projects/quorum && python3 -I skills/quorum/scripts/verify_invariants.py --all -> RC 1; A8 FAIL (passing 21, total 23), A12 FAIL (all_reproducible false), A20 FAIL (panel_verdict_files 0, prd_rows 11, owned 11); 21 of 24 PASS. --digest -> RC 1, axiom_count 24, passing 21. Three of the four documented validators/CI gates are red at the checked-out tree.

## F3: BLOCKER: QUORUM-LOG.md, field-notes.md and QUORUM-CARRY-FORWARD.md cite panel witnesses that do not exist

Severity: blocker

Files: /Users/dylanwong/projects/quorum/QUORUM-LOG.md (28414 B), /Users/dylanwong/projects/quorum/skills/quorum/references/field-notes.md, /Users/dylanwong/projects/quorum/QUORUM-CARRY-FORWARD.md.

Command: python3 -I -c 'import pathlib; t=pathlib.Path("/Users/dylanwong/projects/quorum/QUORUM-LOG.md").read_text(); print([l.strip() for l in t.splitlines() if "A20" in l or "verdict files measured" in l][:6])' -> ['Invariant obligations: A20, A22.', '| `panel_independence` | Panel | KEEP | 14 verdict files measured | none |', '| A20 | PASS | 28 verdict files, one seat per surface |'].

Command: python3 -I -c 'import pathlib; t=pathlib.Path("/Users/dylanwong/projects/quorum/skills/quorum/references/field-notes.md").read_text(); print([l.strip() for l in t.splitlines() if "11 reported" in l])' -> 'count. Measured: 14 required, 11 reported, quorum false.'

Command: python3 -I -c 'import pathlib; t=pathlib.Path("/Users/dylanwong/projects/quorum/QUORUM-CARRY-FORWARD.md").read_text(); print([l.strip()[:120] for l in t.splitlines() if "R1 collection" in l])' -> '| A verdict that exists only in a return value is lost ... | R1 collection reported every filed seat from panel/R1/<seat>.md ...'.

Falsification: cd /Users/dylanwong/projects/quorum && python3 -I skills/quorum/scripts/verify_invariants.py --axiom A20 -> RC 1 {"axiom":"A20","measured":{"owned":11,"panel_verdict_files":0,"prd_rows":11},"status":"FAIL"}. And python3 -I skills/quorum/scripts/collect_panel.py panel/R1 --roster fail-closed --json -> seats_reporting 0. The Compliance Check records A20 as PASS with a 28-file witness; the live checker says FAIL with 0 files. This is a phantom witness in the derived state.

## F4: MAJOR: landing page prints 28 panel verdict files where the validator computes 0

Severity: major

File: /Users/dylanwong/projects/quorum/web/index.html line 104 `<span data-figure="panel_verdicts">28</span>`, line 87 'Every number below is recomputed by one command after the last edit. None is a claim about a past state of the repository.', line 134 'Every figure on this page is reproducible after the final edit.' Also /Users/dylanwong/projects/quorum/skills/quorum/references/canon.md line 135 'No figure in web/index.html is printed without one of these sources or a command that reproduces it.'

Command: cd /Users/dylanwong/projects/quorum && python3 -I scripts/validate_figures.py -> RC 1; the panel_verdicts row is {"computed":0,"figure":"panel_verdicts","occurrences":1,"printed":[28],"reproducible":false}; all_reproducible false.

Command: cd /Users/dylanwong/projects/quorum && python3 -I skills/quorum/scripts/verify_invariants.py --axiom A12 -> RC 1 {"axiom":"A12","measured":{"all_reproducible":false,"figures":14},"status":"FAIL"}. The printed figure was raised from 14 to 28 during this audit while the computed value stayed 0; the page's reproducibility claim is false.

## F5: MAJOR: daemon emits an uncaught TypeError traceback, and A24 reports PASS anyway

Severity: major

Files: /Users/dylanwong/projects/quorum/skills/quorum/scripts/epistemic_audit.py (docstring lines 9-12: 'no uncaught exception'; main() catches only OSError/ValueError around load_payload), /Users/dylanwong/projects/quorum/skills/quorum/references/fault-taxonomy.md lines 57-63 ('An unexpected exception is converted into [FAULT: JANK_DETECTED] with mode engine-internal and a stable digest; it is never swallowed and never printed as a traceback to the I/O port'), SKILL.md A24 ('no uncaught panic; every error path is named').

Exact command (works from any cwd):
python3 -I -c 'import json,pathlib; p=json.loads(pathlib.Path("/Users/dylanwong/projects/quorum/state/clean.json").read_text()); p["rules"]=5; print(json.dumps(p))' | python3 -I /Users/dylanwong/projects/quorum/skills/quorum/scripts/epistemic_audit.py --payload /dev/stdin
-> RC 1, stdout EMPTY, stderr: Traceback ... File ".../epistemic_audit.py", line 128, in parse_state / for item in raw["rules"]: / TypeError: 'int' object is not iterable. Same traceback for p["edges"]=5 (line 144) and p["context"]=5 (line 149). No `[FAULT: JANK_DETECTED]` record is emitted.

Falsification of the checker: cd /Users/dylanwong/projects/quorum && python3 -I skills/quorum/scripts/verify_invariants.py --axiom A24 -> RC 0 {"axiom":"A24","measured":{"bare_handlers":[],"fault_codes":[...]},"status":"PASS"}. A24 only scans source text for literal 'except:'/'assert ' tokens, so it certifies an engine that crashes on malformed input.

## F6: MAJOR: the pre-flight jank checksum does not detect the initiating brief's isolation contradiction

Severity: major

Files: /Users/dylanwong/projects/quorum/state/initiating-brief.json (variables isolated_from_external_networks=true AND external_sources_required=true; rule R1 concludes contradiction_network_isolation), /Users/dylanwong/projects/quorum/skills/quorum/SKILL.md Step 1.2 ('A payload that declares itself isolated while requiring external sources is a category error: record it, do not silently ignore it'), /Users/dylanwong/projects/quorum/skills/quorum/references/fault-taxonomy.md (JANK_DETECTED logical-contradiction / category-error modes). jank_checksum() only detects set(axioms) & set(negations) and boolean/axiom mismatches.

Command: cd /Users/dylanwong/projects/quorum && python3 -I skills/quorum/scripts/epistemic_audit.py --payload state/initiating-brief.json -> the JANK_DETECTED reason is "logical-contradiction: ['deterministic_derivation'] asserted and negated" (a different, syntactic overlap), not the isolation category error.

Exact command: python3 -I -c 'import json,pathlib; p=json.loads(pathlib.Path("/Users/dylanwong/projects/quorum/state/initiating-brief.json").read_text()); p["negations"]=[]; print(json.dumps(p))' | python3 -I /Users/dylanwong/projects/quorum/skills/quorum/scripts/epistemic_audit.py --payload /dev/stdin -> RC 0, {"derived":"true","chain":["R1"],"faults_cleared":["JANK_DETECTED","STATE_UNMAPPED","SELF_REJECTED","IO_FAULT"],...}. With the syntactic overlap removed, the engine derives the contradiction query as true and clears all four faults instead of halting at pre-flight.

## F7: MAJOR: canon.md/README claim provenance for every anchor; 329 of 379 distinct graph labels have none

Severity: major

Files: /Users/dylanwong/projects/quorum/skills/quorum/references/canon.md line 3 'Every label in anchor-graph.md is a real text, system, or result. This file records its source, the cluster it occupies, and the authority under which the graph reads it.'; /Users/dylanwong/projects/quorum/README.md line 83 'The canon names the source and provenance of every anchor.'

Exact command: python3 -I -c 'import pathlib,re; g=pathlib.Path("/Users/dylanwong/projects/quorum/skills/quorum/references/anchor-graph.md").read_text(); c=pathlib.Path("/Users/dylanwong/projects/quorum/skills/quorum/references/canon.md").read_text(); L=set(re.findall(r"^\s*\w+\[\"([^\"]+)\"\]:::\w+\s*$",g,re.M)); print("distinct_labels",len(L),"absent_from_canon",len([x for x in L if x not in c]))' -> distinct_labels 379 absent_from_canon 329. Sample absent labels: 'A Theory of Type Polymorphism in Programming (Milner)', 'Affine Typestate at Byzantine Boundaries (Minsky)', 'A3 Problem Solving', 'Andon'. canon.md has 105 table rows for 397 node declarations.

The checker masks this: cd /Users/dylanwong/projects/quorum && python3 -I skills/quorum/scripts/verify_invariants.py --axiom A18 -> RC 0 {"axiom":"A18","measured":{"empty_provenance":[],"provenance_rows":96},"status":"PASS"} -- it counts well-formed rows and never cross-references graph labels, so 329 phantom/unsourced anchors pass ZeroTrust.

## F8: MAJOR: the runnable graph walk is a fixed 5-round split with canned defer reasons, not a living Frontier

Severity: major

Files: /Users/dylanwong/projects/quorum/tools/run_traversal.py and /Users/dylanwong/projects/quorum/analysis/traversal.json. The module docstring claims 'Each round computes the Frontier from the anchors visited so far using graph_walk.py, takes the top-ranked candidate, and defers the rest with a recorded reason. Every deferred candidate is an assessed decision, not an ignored one.' In fact graph_walk.frontier() is called once, before the loop; the loop slices that single candidate list into ROUNDS=5 chunks; visited is appended but never used; defer reasons are DEFER_REASONS[position % 4] (no reference to the candidate); all_adjudicated is `all(open_count >= 0) and last == 0`, true by arithmetic.

Exact command: python3 -I -c 'import pathlib,json; t=pathlib.Path("/Users/dylanwong/projects/quorum/tools/run_traversal.py").read_text(); a=json.loads(pathlib.Path("/Users/dylanwong/projects/quorum/analysis/traversal.json").read_text()); rs=[d["reason"] for r in a["rounds"] for d in r["deferred"]]; print("frontier_calls",t.count("graph_walk.frontier("),"defer_reasons",len(rs),"distinct",len(set(rs)),"all_adjudicated",a["all_adjudicated"])' -> frontier_calls 1 defer_reasons 14 distinct 3 all_adjudicated True.

Exact command: python3 -I -c 'import pathlib; r=pathlib.Path("/Users/dylanwong/projects/quorum"); fs=[".github/workflows/validate.yml","scripts/validate_figures.py","scripts/validate_graph.py","scripts/validate_skills.py","skills/quorum/scripts/verify_invariants.py"]; print("validator_refs_to_run_traversal",sum("run_traversal" in (r/f).read_text() for f in fs))' -> validator_refs_to_run_traversal 0. No validator or CI step executes it, yet --axiom A15 reports PASS on a modules list that includes run_traversal.py while SKILL.md section 2 and the anti-skip rules forbid a linear walk and unmeasured moves.

## F9: MAJOR: graph_walk.py --render drops every classDef, so visited/kept/adapted/scrapped status classes never render

Severity: major

Files: /Users/dylanwong/projects/quorum/skills/quorum/scripts/graph_walk.py (parse() discards classDef lines at lines 122-123; render() never re-emits them), /Users/dylanwong/projects/quorum/skills/quorum/references/anchor-graph.md lines 830-848 (19 classDef lines including visited, kept, adapted, scrapped), /Users/dylanwong/projects/quorum/skills/quorum/SKILL.md Step 1.7 and 2e ('Render the graph and mark visited anchors with the visited class'; 'apply kept, adapted or scrapped to each anchor's node id ... and re-render').

Exact command: python3 -I /Users/dylanwong/projects/quorum/skills/quorum/scripts/graph_walk.py --render --visited flp,gilbert,paxos | python3 -I -c 'import sys; print("classDef_lines",sum("classDef" in l for l in sys.stdin))' -> classDef_lines 0.

Exact command: python3 -I -c 'import pathlib; print("classDef_lines",pathlib.Path("/Users/dylanwong/projects/quorum/skills/quorum/references/anchor-graph.md").read_text().count("classDef "))' -> classDef_lines 19. The render still emits `:::stance` etc. and `class flp,gilbert,paxos visited`, all referencing undefined classes, so the live graph required by the workflow cannot display status.

## F10: MINOR: verify_invariants.py and invariant-ledger.md promise a `witness` field that is never emitted

Severity: minor

Files: /Users/dylanwong/projects/quorum/skills/quorum/scripts/verify_invariants.py docstring line 7 'Output is one JSON object per axiom with status, measured and witness'; /Users/dylanwong/projects/quorum/skills/quorum/references/invariant-ledger.md lines 5-6 'prints one JSON object per axiom with status, measured and witness'; lines 36-38 require the Compliance Check to record the exact stdout digest. main() builds rows as {"axiom","status","measured"} only.

Exact command: python3 -I /Users/dylanwong/projects/quorum/skills/quorum/scripts/verify_invariants.py --axiom A1 | python3 -I -c 'import sys,json; print(sorted(json.load(sys.stdin)))' -> ['axiom', 'measured', 'status']. Same for --all (24 rows) and --digest. No axiom row carries a witness, so the Compliance Check cannot point to a per-axiom witness as the ledger requires.

## F11: MINOR: dotted 'counterpoint' frontier direction is unreachable dead code

Severity: minor

File: /Users/dylanwong/projects/quorum/skills/quorum/scripts/graph_walk.py lines 63-76: neighbours() handles `if e.dst == node` then `elif e.src == node`, so the third branch `elif e.kind == "dotted" and (e.src == node or e.dst == node)` (which would emit direction 'counterpoint') can never run. SKILL.md section 2 claims candidates are reached by 'outgoing solid edges, incoming edges, and dotted edges (counterpoints)'.

Exact command: python3 -I -c 'import sys,pathlib,collections; sys.path.insert(0,"/Users/dylanwong/projects/quorum/skills/quorum/scripts"); import graph_walk; g=graph_walk.parse(pathlib.Path("/Users/dylanwong/projects/quorum/skills/quorum/references/anchor-graph.md")); print(dict(collections.Counter(i["direction"] for n in g.labels for i in g.neighbours(n))))' -> {'outgoing': 391, 'incoming': 391}. Zero 'counterpoint' directions across all 397 nodes despite 47 dotted edges. The frontier still lists dotted edges, but never as the counterpoints the priority rule (rank 'break-dotted') and the traversal protocol describe.

## F12: MINOR: SKILL.md says Fail-Closed needs 7 to 9 seats; the executable roster requires 14

Severity: minor

Files: /Users/dylanwong/projects/quorum/skills/quorum/SKILL.md section 1 table (line 101) 'Required critics ... plus at least one more; 7 to 9 seats'; /Users/dylanwong/projects/quorum/web/index.html line 99 prints Fail-Closed roster 14; /Users/dylanwong/projects/quorum/QUORUM-CARRY-FORWARD.md line 18 'a 7-seat seed to 14 seats in 1 closure round'.

Exact command: python3 -I /Users/dylanwong/projects/quorum/skills/quorum/scripts/graph_walk.py --roster --mode fail-closed | python3 -I -c 'import sys,json; print("seat_count",json.load(sys.stdin)["seat_count"])' -> seat_count 14. /Users/dylanwong/projects/quorum/skills/quorum/references/critic-panel.md line 16 says the roster is computed deterministically from the graph, 'so no panel is hand-assembled' -- the contract's 7-to-9 bound and the machine roster disagree, and collect_panel.py requires all 14.

## F13: MINOR: README says six state payloads; state/ contains nine

Severity: minor

File: /Users/dylanwong/projects/quorum/README.md line 64 '`state/` holds six payloads: one clean derivation and one for each fault mode. None is a test fixture; each is a real input to the daemon.'

Exact command: python3 -I -c 'import pathlib; print(len(list(pathlib.Path("/Users/dylanwong/projects/quorum/state").glob("*.json"))))' -> 9. Names: clean.json, initiating-brief.json, io-fault.json, jank-contradiction.json, jank-dangling.json, max-load.json, partition.json, self-rejected.json, unmapped.json. Live check: python3 -I skills/quorum/scripts/epistemic_audit.py --payload state/<each>.json gives derived=true for clean/max-load/partition, derived=false for none, and the four fault codes for the fault payloads (so the payloads themselves work; only the documented count and 'one for each fault mode' description drifted).

## F14: MINOR: AGENTS.md calls QUORUM-CARRY-FORWARD.md 'committed' and README calls anchor-graph.md 'checked-in'; git tracks only .gitignore

Severity: minor

Files: /Users/dylanwong/projects/quorum/AGENTS.md line 42-43 '`QUORUM-CARRY-FORWARD.md` is durable project knowledge and is committed'; /Users/dylanwong/projects/quorum/README.md line 77 'validate_graph.py regenerates the anchor graph in memory and compares it byte for byte with the checked-in file'.

Exact command: git -C /Users/dylanwong/projects/quorum ls-files -> .gitignore (single tracked file). Exact command: git -C /Users/dylanwong/projects/quorum ls-files QUORUM-CARRY-FORWARD.md -> empty; same for skills/quorum/references/anchor-graph.md -> empty. git -C /Users/dylanwong/projects/quorum remote -v -> empty. All 43 claim-bearing files are untracked, so a clean checkout contains none of the files the CI workflow validates; the 'checked-in' and 'committed' states do not exist.

## F15: MINOR: hero SVG prints wrong node/link counts, and no validator covers them

Severity: minor

File: /Users/dylanwong/projects/quorum/web/index.html lines 33 and 66: '<desc>Twelve nodes arranged in three columns. Eleven links are solid; one link is broken...</desc>' and '<figcaption>Eleven solid links and one broken link...</figcaption>', while line 87/134 claim every number on the page is reproducible.

Exact command: python3 -I -c 'import pathlib,re; t=pathlib.Path("/Users/dylanwong/projects/quorum/web/index.html").read_text(); g=t.split("<g class=\"link\"",1)[1].split("</g>",1)[0]; print("circles",t.count("<circle "),"link_segments",len(re.findall(r"M\d",g)),"broken",g.count("class=\"broken\""))' -> circles 10 link_segments 15 broken 1, i.e. 14 solid + 1 broken, not 12 nodes / 11 solid.

Exact command: python3 -I -c 'import pathlib,re; t=pathlib.Path("/Users/dylanwong/projects/quorum/web/index.html").read_text(); h=t.split("<figure class=\"hero-art\"",1)[1].split("</figure>",1)[0]; print("data_figure_total",len(re.findall("data-figure=",t)),"data_figure_in_hero",len(re.findall("data-figure=",h)))' -> data_figure_total 15 data_figure_in_hero 0. scripts/validate_figures.py only checks data-figure attributes, so these two printed numbers are unverifiable by the documented command.

## F16: MINOR: build_graph.py's 'single source of truth' docstring asserts cluster-rank monotonicity; 56 edges violate it

Severity: minor

File: /Users/dylanwong/projects/quorum/tools/build_graph.py lines 3-5: 'The graph is a strict DAG: every edge goes from a lower cluster rank to a higher one, and edges inside a cluster go from a lower node index to a higher one.' /Users/dylanwong/projects/quorum/skills/quorum/references/field-notes.md item 3 and /Users/dylanwong/projects/quorum/QUORUM-CARRY-FORWARD.md line 10 state the opposite ('Cluster rank is not a topological rank'; builder now derives rank from topological order).

Exact command: python3 -I -c 'import pathlib,importlib.util,sys; r=pathlib.Path("/Users/dylanwong/projects/quorum"); sys.path.insert(0,str(r/"skills/quorum/scripts")); import graph_walk; g=graph_walk.parse(r/"skills/quorum/references/anchor-graph.md"); s=importlib.util.spec_from_file_location("bg",r/"tools/build_graph.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); cr={k:v[2] for k,v in m.CLUSTERS.items()}; print("cluster_rank_violations",len([(e.src,e.dst) for e in g.edges if cr[g.cluster_of[e.src]]>cr[g.cluster_of[e.dst]]]))' -> cluster_rank_violations 56 (first three: dynamo->sloppyquorum, dynamo->vectorclock, dynamo->merkle, all BREAK rank 2 -> RULES rank 1). The DAG itself is fine (python3 -I scripts/validate_graph.py -> acyclic true); only the docstring's structural claim is false and contradicts the field notes.

## F17: MINOR: traversal-ledger.md prints 52 PASS panel verdicts with zero verdict files and no validator

Severity: minor

Files: /Users/dylanwong/projects/quorum/skills/quorum/references/traversal-ledger.md (counts block: PASS 52), /Users/dylanwong/projects/quorum/tools/build_ledger.py docstring line 5 'Every row is derived from a command or a file comparison, never asserted', /Users/dylanwong/projects/quorum/skills/quorum/references/panel-protocol.md line 16 'A verdict is a file, not a return value' and critic-panel.md 'A missing seat is NOT REPORTED, never PASS'.

Exact command: python3 -I -c 'import pathlib,re; t=pathlib.Path("/Users/dylanwong/projects/quorum/skills/quorum/references/traversal-ledger.md").read_text(); print("PASS_verdict_rows",len(re.findall(r"^\| \d+ \| .*\| PASS \|",t,re.M)))' -> PASS_verdict_rows 52. Exact command: python3 -I -c 'import pathlib; r=pathlib.Path("/Users/dylanwong/projects/quorum/panel"); print("verdict_files",len(list(r.glob("R*/*.md"))))' -> verdict_files 0. decide() in build_ledger.py emits 'PASS' from `lens != ""` (a graph edge lookup), not from a filed verdict, and uses `cited = label in canon` (substring test) rather than a command. The ledger is byte-identical to its generator but no validator checks it: python3 -I -c 'import pathlib; r=pathlib.Path("/Users/dylanwong/projects/quorum"); fs=[".github/workflows/validate.yml","scripts/validate_figures.py","scripts/validate_graph.py","scripts/validate_skills.py","skills/quorum/scripts/verify_invariants.py"]; print("validator_refs_to_traversal_ledger",sum("traversal-ledger" in (r/f).read_text() for f in fs))' -> validator_refs_to_traversal_ledger 0.

## F18: Uncaught exceptions on malformed payload and valid Mermaid comment

Severity: blocker

Affected: /Users/dylanwong/projects/quorum/skills/quorum/scripts/epistemic_audit.py and /Users/dylanwong/projects/quorum/skills/quorum/scripts/graph_walk.py. A JSON payload with rules=null and a Mermaid graph containing a valid %% comment both terminate with empty stdout and Python tracebacks, violating the JSON-only output contract, the fault taxonomy's unexpected-exception rule, and AGENTS.md's no-unchecked-panics rule. /Users/dylanwong/projects/quorum/skills/quorum/scripts/verify_invariants.py nevertheless reports A24 PASS. Exact command:
```
python3 -I -c '
import json,pathlib,subprocess,sys
root=pathlib.Path("/Users/dylanwong/projects/quorum")
audit=str(root/"skills/quorum/scripts/epistemic_audit.py")
walk=str(root/"skills/quorum/scripts/graph_walk.py")
base=json.loads((root/"state/clean.json").read_text())
p=dict(base); p["rules"]=None
a=subprocess.run([sys.executable,"-I",audit,"--payload","/dev/stdin"],input=json.dumps(p),capture_output=True,text=True,cwd=str(root),timeout=30)
g=chr(10).join(["```mermaid","flowchart LR","  %% valid Mermaid comment","  a["+chr(34)+"A"+chr(34)+"]:::x","```"])
b=subprocess.run([sys.executable,"-I",walk,"--graph","/dev/stdin","--counts"],input=g,capture_output=True,text=True,cwd=str(root),timeout=30)
print(json.dumps({"audit":{"returncode":a.returncode,"stdout":a.stdout.strip(),"stderr_tail":a.stderr.strip().splitlines()[-1]},"graph_walk":{"returncode":b.returncode,"stdout":b.stdout.strip(),"stderr_tail":b.stderr.strip().splitlines()[-1]}},indent=2))
'
python3 -I /Users/dylanwong/projects/quorum/skills/quorum/scripts/verify_invariants.py --axiom A24
```
Observed: audit returncode=1, stdout empty, stderr tail TypeError: 'NoneType' object is not iterable; graph_walk returncode=1, stdout empty, stderr tail ValueError: unparsed graph line: '  %% valid Mermaid comment'. A24 prints status PASS with bare_handlers empty. Other scalar/null values for rules, edges, or context produce the same TypeError family; missing graph files produce FileNotFoundError.

## F19: --replay and --enumerate bypass preflight and mutate JANK state

Severity: blocker

Affected: /Users/dylanwong/projects/quorum/skills/quorum/scripts/epistemic_audit.py. The normal path correctly halts on /Users/dylanwong/projects/quorum/state/jank-contradiction.json with JANK_DETECTED, but --replay returns success with no fault code and --enumerate returns success with no fault code. The internal apply() called by --replay also appends a new context frame to the rejected payload, so a corrupted state is processed despite the SKILL.md pre-flight halt rule. Exact command:
```
python3 -I -c '
import importlib.util,json,pathlib,subprocess,sys
root=pathlib.Path("/Users/dylanwong/projects/quorum")
audit=root/"skills/quorum/scripts/epistemic_audit.py"
payload=root/"state/jank-contradiction.json"
rows=[]
for flags in ([],["--replay"],["--enumerate"]):
    p=subprocess.run([sys.executable,"-I",str(audit),"--payload",str(payload),*flags],capture_output=True,text=True,cwd=str(root),timeout=30)
    rows.append({"flags":flags,"returncode":p.returncode,"stdout":p.stdout.strip()})
spec=importlib.util.spec_from_file_location("qea",audit); m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m)
s,_=m.parse_state(json.loads(payload.read_text()))
print(json.dumps({"audit_modes":rows,"audit_result":m.audit(s),"context_before":list(s.context),"context_after_apply":list(m.apply(s).context)},indent=2))
'
```
Observed: normal mode returncode=1 and fault JANK_DETECTED; --replay returncode=0 with replay idempotent and composition f(f(x)) = f(x); --enumerate returncode=0 with finite true; audit(state) is still JANK_DETECTED, while context changes from [p],[p,q] to [p],[p,q],[p,q,t].

## F20: Sound derivations are falsely rejected as logical leaps

Severity: major

Affected: /Users/dylanwong/projects/quorum/skills/quorum/scripts/epistemic_audit.py. derive() rejects any true result if a rule with the same conclusion did not enter the chain. A redundant valid rule q->t is skipped because t is already derived, then its absence is misreported as a logical leap; a query answered directly by variable t=true is likewise rejected because an unrelated rule R1 concludes t. /Users/dylanwong/projects/quorum/skills/quorum/references/fault-taxonomy.md defines logical-leap as a conclusion that does not follow from the rule chain. Exact command:
```
python3 -I -c '
import copy,json,pathlib,subprocess,sys
root=pathlib.Path("/Users/dylanwong/projects/quorum"); script=str(root/"skills/quorum/scripts/epistemic_audit.py")
base=json.loads((root/"state/clean.json").read_text())
def run(label,p):
    r=subprocess.run([sys.executable,"-I",script,"--payload","/dev/stdin"],input=json.dumps(p),capture_output=True,text=True,timeout=30,cwd=str(root))
    return {"case":label,"returncode":r.returncode,"stdout":r.stdout.strip()}
p=copy.deepcopy(base); p["rules"].append({"id":"R3","premises":["q"],"negated":[],"conclusion":"t"})
a=run("redundant-valid-rule",p)
p={"query_id":"direct-variable","variables":{"p":False,"t":True},"rules":[{"id":"R1","premises":["p"],"negated":[],"conclusion":"t"}],"query":"t","axioms":[],"negations":[],"nodes":["p","t"],"edges":[],"context":[["p"]],"secrets":[]}
b=run("direct-variable-lookup",p)
print(json.dumps([a,b],indent=2))
'
```
Observed: both returncode=1 with SELF_REJECTED; reasons are logical-leap: t asserted without rule R3 and logical-leap: t asserted without rule R1.

## F21: No derivation still emits derived false with cleared faults

Severity: major

Affected: /Users/dylanwong/projects/quorum/skills/quorum/scripts/epistemic_audit.py. The shipped /Users/dylanwong/projects/quorum/state/partition.json cannot fire R1 (p=false) or R2 (r=true, so its negated premise is not false). The daemon nevertheless returns success with derived=false, chain=[], and faults_cleared listing all four faults. A payload using an AST node as a negated boolean value does the same. Exact command:
```
python3 -I /Users/dylanwong/projects/quorum/skills/quorum/scripts/epistemic_audit.py --payload /Users/dylanwong/projects/quorum/state/partition.json
python3 -I -c '
import json,subprocess,sys
root="/Users/dylanwong/projects/quorum"; script=root+"/skills/quorum/scripts/epistemic_audit.py"
p={"query_id":"node-as-value","variables":{"p":True},"rules":[{"id":"R1","premises":["p"],"negated":["ghost"],"conclusion":"t"}],"query":"t","axioms":[],"negations":[],"nodes":["p","t","ghost"],"edges":[],"context":[["p"]],"secrets":[]}
r=subprocess.run([sys.executable,"-I",script,"--payload","/dev/stdin"],input=json.dumps(p),capture_output=True,text=True,timeout=30,cwd=root)
print(json.dumps({"returncode":r.returncode,"stdout":r.stdout.strip()},indent=2))
'
```
Observed: both returncode=0 with derived=false, chain=[], and faults_cleared=[JANK_DETECTED, STATE_UNMAPPED, SELF_REJECTED, IO_FAULT].

## F22: Secret values are emitted despite the secrets list

Severity: major

Affected: /Users/dylanwong/projects/quorum/skills/quorum/scripts/epistemic_audit.py. jank_checksum checks secrets only against node ids and variable names. A secret equal to a rule id is emitted in chain, and a secret used as query_id is emitted verbatim; both payloads derive successfully. This contradicts SKILL.md's zero-leak contract and the brief's secrets-not-in-AST invariant. Exact command:
```
python3 -I -c '
import copy,json,pathlib,subprocess,sys
root=pathlib.Path("/Users/dylanwong/projects/quorum")
script=str(root/"skills/quorum/scripts/epistemic_audit.py")
base=json.loads((root/"state/clean.json").read_text())
def run(label,payload,needle):
    r=subprocess.run([sys.executable,"-I",script,"--payload","/dev/stdin"],input=json.dumps(payload),capture_output=True,text=True,timeout=30,cwd=str(root))
    return {"case":label,"returncode":r.returncode,"stdout":r.stdout.strip(),"secret_in_output":needle in r.stdout}
p=copy.deepcopy(base); p["secrets"]=["R1"]
a=run("secret-rule-id",p,"R1")
p=copy.deepcopy(base); p["secrets"]=["SECRET-TOKEN"]; p["query_id"]="SECRET-TOKEN"
b=run("secret-query-id",p,"SECRET-TOKEN")
print(json.dumps([a,b],indent=2))
'
```
Observed: both returncode=0, derived=true, no fault, secret_in_output=true; chain contains R1 or query_id contains SECRET-TOKEN.

## F23: Elision markers and non-string rule symbols are accepted

Severity: major

Affected: /Users/dylanwong/projects/quorum/skills/quorum/scripts/epistemic_audit.py. TRUNCATION_MARKERS are scanned only inside nodes/axioms/negations, and rule id/conclusion values are stringified with str() instead of type-checked. A rule id R...1 is emitted in chain, and null id/conclusion creates the phantom symbol None that can satisfy query None. SKILL.md requires every node fully expanded and every symbol declared; fault-taxonomy.md requires malformed rule operands to be JANK_DETECTED. Exact command:
```
python3 -I -c '
import copy,json,pathlib,subprocess,sys
root=pathlib.Path("/Users/dylanwong/projects/quorum"); script=str(root/"skills/quorum/scripts/epistemic_audit.py")
base=json.loads((root/"state/clean.json").read_text())
def run(name,p):
    r=subprocess.run([sys.executable,"-I",script,"--payload","/dev/stdin"],input=json.dumps(p),capture_output=True,text=True,cwd=str(root),timeout=30)
    d=json.loads(r.stdout); return {"case":name,"returncode":r.returncode,"fault":d.get("fault"),"derived":d.get("derived"),"chain":d.get("chain")}
p=copy.deepcopy(base); p["rules"][0]["id"]="R...1"
a=run("elision-rule-id",p)
p={"query_id":"nonstring-conclusion","variables":{"p":True},"rules":[{"id":None,"premises":["p"],"negated":[],"conclusion":None}],"query":"None","axioms":[],"negations":[],"nodes":["p"],"edges":[],"context":[["p"]],"secrets":[]}
b=run("nonstring-rule-symbols",p)
print(json.dumps([a,b],indent=2))
'
```
Observed: both returncode=0, fault=null, derived=true; chains are [R...1, R2] and [None].

## F24: Undefined axiom is classified as STATE_UNMAPPED instead of JANK_DETECTED

Severity: major

Affected: /Users/dylanwong/projects/quorum/skills/quorum/scripts/epistemic_audit.py. Adding an undeclared axiom z to the clean payload is a pre-flight structural error, but jank_checksum does not test axioms against declared variables/nodes/rule conclusions; mapping_check later returns STATE_UNMAPPED. /Users/dylanwong/projects/quorum/skills/quorum/references/fault-taxonomy.md assigns undefined variables in a STATE_PAYLOAD to JANK_DETECTED, while STATE_UNMAPPED is for the query atom. Exact command:
```
python3 -I -c '
import json,pathlib,subprocess,sys
root=pathlib.Path("/Users/dylanwong/projects/quorum"); script=str(root/"skills/quorum/scripts/epistemic_audit.py")
p=json.loads((root/"state/clean.json").read_text()); p["axioms"].append("z")
r=subprocess.run([sys.executable,"-I",script,"--payload","/dev/stdin"],input=json.dumps(p),capture_output=True,text=True,timeout=30,cwd=str(root))
print(json.dumps({"returncode":r.returncode,"stdout":r.stdout.strip(),"expected_fault":"JANK_DETECTED","actual_fault":json.loads(r.stdout)["fault"]},indent=2))
'
```
Observed: returncode=1, expected_fault=JANK_DETECTED, actual_fault=STATE_UNMAPPED, reason missing variable or axiom: z.

## F25: Graph walk accepts empty/absent graph and unknown visited anchors

Severity: major

Affected: /Users/dylanwong/projects/quorum/skills/quorum/scripts/graph_walk.py. An empty graph file is certified acyclic with zero nodes; --visited ghost silently returns an empty frontier with success; a missing graph produces an uncaught FileNotFoundError. The graph walk advertises JSON/Mermaid output and the anchor graph is specified as a 397-node strict DAG in /Users/dylanwong/projects/quorum/skills/quorum/references/anchor-graph.md. Exact command:
```
python3 -I -c '
import json,pathlib,subprocess,sys
root=pathlib.Path("/Users/dylanwong/projects/quorum")
walk=str(root/"skills/quorum/scripts/graph_walk.py")
def run(name,args,stdin=""):
    p=subprocess.run([sys.executable,"-I",walk,*args],input=stdin,capture_output=True,text=True,cwd=str(root),timeout=30)
    return {"case":name,"returncode":p.returncode,"stdout":p.stdout.strip(),"stderr_tail":p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""}
empty=run("empty-graph-check-dag",["--graph","/dev/stdin","--check-dag"],"")
ghost=run("unknown-visited-frontier",["--frontier","--visited","ghost"])
missing=run("missing-graph",["--graph",str(root/"does-not-exist.md"),"--counts"])
print(json.dumps([empty,ghost,missing],indent=2))
'
```
Observed: empty graph returncode=0 with acyclic=true, node_count=0, edge_count=0; ghost returncode=0 with candidate_count=0; missing graph returncode=1 with empty stdout and FileNotFoundError.

## F26: Frontier deduplication drops distinct anchor edges

Severity: major

Affected: /Users/dylanwong/projects/quorum/skills/quorum/scripts/graph_walk.py. frontier() deduplicates on (candidate, via, direction) but omits the anchor it came from. The real graph has ddia -->|chapters ground| twophase and ddia -->|chapters ground| lsmtree; visiting both anchors should produce two incoming rows with different From anchor values, but only the twophase row survives. SKILL.md's Frontier table has a From anchor column and requires every edge touching a visited anchor. Exact command:
```
python3 -I -c '
import importlib.util,json,pathlib,sys
root=pathlib.Path("/Users/dylanwong/projects/quorum")
p=root/"skills/quorum/scripts/graph_walk.py"
spec=importlib.util.spec_from_file_location("qgw",p); m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m)
g=m.parse(m.GRAPH_PATH)
visited=["twophase","lsmtree"]
f=m.frontier(g,visited,{"andon":[],"reopened":[],"break-dotted":[],"disagreement":[]})
expected=[{"candidate":e.src,"via":e.label,"direction":"incoming","from":e.dst} for e in g.edges if e.src=="ddia" and e.dst in visited and e.label=="chapters ground"]
actual=[c for c in f["candidates"] if c["candidate"]=="ddia"]
print(json.dumps({"visited":visited,"edge_rows":expected,"frontier_rows":actual},indent=2))
'
```
Observed: edge_rows has two rows, from twophase and from lsmtree; frontier_rows has one row, from twophase.

## F27: Fail-closed roster returns 14 seats despite 7-9 seat contract

Severity: major

Affected: /Users/dylanwong/projects/quorum/skills/quorum/scripts/graph_walk.py and /Users/dylanwong/projects/quorum/skills/quorum/SKILL.md. roster() starts with the seven fail-closed seats, then symmetrically closes dotted critic pairs, producing fourteen required seats. SKILL.md explicitly states Fail-Closed requires 7 to 9 seats. Exact command:
```
python3 -I -c '
import importlib.util,json,pathlib,sys
root=pathlib.Path("/Users/dylanwong/projects/quorum")
p=root/"skills/quorum/scripts/graph_walk.py"
spec=importlib.util.spec_from_file_location("qgw",p); m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m)
g=m.parse(m.GRAPH_PATH); r=m.roster(g,"fail-closed")
skill=(root/"skills/quorum/SKILL.md").read_text()
line=[x.strip() for x in skill.splitlines() if "7 to 9 seats" in x][0]
print(json.dumps({"skill_line":line,"seat_count":r["seat_count"],"within_7_to_9":7<=r["seat_count"]<=9,"required_seats":r["required_seats"]},indent=2))
'
```
Observed: skill_line contains 7 to 9 seats; seat_count=14; within_7_to_9=false. The graceful roster returns 9 seats.

## F28: Dotted edges never receive counterpoint direction

Severity: minor

Affected: /Users/dylanwong/projects/quorum/skills/quorum/scripts/graph_walk.py. Graph.neighbours() has a counterpoint branch guarded by e.kind == dotted and src/dst == node, but both conditions are already consumed by the preceding if/elif. Every dotted edge is therefore labeled incoming or outgoing, and counterpoint is unreachable. SKILL.md describes dotted edges as counterpoints or back-references. Exact command:
```
python3 -I -c '
import importlib.util,json,pathlib,sys
root=pathlib.Path("/Users/dylanwong/projects/quorum")
p=root/"skills/quorum/scripts/graph_walk.py"
spec=importlib.util.spec_from_file_location("qgw",p); m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m)
g=m.parse(m.GRAPH_PATH)
e=next(e for e in g.edges if e.kind=="dotted")
print(json.dumps({"edge":{"src":e.src,"dst":e.dst,"label":e.label,"kind":e.kind},"neighbours":g.neighbours(e.src),"counterpoint_direction_present":any(x["direction"]=="counterpoint" for x in g.neighbours(e.src))},indent=2))
'
```
Observed: edge waldonote - dotted -> e2earg with label contrasts with; neighbours returns direction outgoing, kind dotted; counterpoint_direction_present=false.

## F29: Traversal sorts priorities lexically, demoting reopened candidates

Severity: minor

Affected: /Users/dylanwong/projects/quorum/tools/run_traversal.py and /Users/dylanwong/projects/quorum/skills/quorum/scripts/graph_walk.py. run_traversal.py sorts candidates by the priority string rather than graph_walk.PRIORITY. Alphabetically, reopened sorts after outgoing, although SKILL.md ranks REOPENED second. With flp flagged reopened, the lexical sort chooses chubby/incoming first while the declared priority order chooses flp/reopened. Exact command:
```
python3 -I -c '
import json,pathlib,sys
root=pathlib.Path("/Users/dylanwong/projects/quorum")
sys.path[:0]=[str(root/"skills/quorum/scripts"),str(root/"tools")]
import graph_walk,run_traversal
g=graph_walk.parse(graph_walk.GRAPH_PATH)
flags={"andon":[],"reopened":["flp"],"break-dotted":[],"disagreement":[]}
sf=graph_walk.frontier(g,run_traversal.SEED,flags)["candidates"]
unique={}
for c in sf: unique.setdefault(c["candidate"],c)
lexical=sorted(unique.values(),key=lambda c:(c["priority"],c["candidate"]))
spec_order=sorted(unique.values(),key=lambda c:(graph_walk.PRIORITY.index(c["priority"]),c["candidate"],c["via"]))
print(json.dumps({"priority_order":list(graph_walk.PRIORITY),"lexical_first3":[{"candidate":c["candidate"],"priority":c["priority"]} for c in lexical[:3]],"spec_first3":[{"candidate":c["candidate"],"priority":c["priority"]} for c in spec_order[:3]],"top_differs":lexical[0]["candidate"]!=spec_order[0]["candidate"]},indent=2))
'
```
Observed: priority_order=[andon, reopened, break-dotted, disagreement, incoming, outgoing]; lexical_first3 starts with chubby/incoming; spec_first3 starts with flp/reopened; top_differs=true.

## F3: canon fidelity

Severity: NOT REPORTED

No verdict file was produced by this seat. The canon is checked by
validate_graph.py and verify_invariants.py --axiom A18 instead.
