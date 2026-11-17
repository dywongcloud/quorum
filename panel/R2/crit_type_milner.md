Anchor used: A Theory of Type Polymorphism in Programming (Milner)
Observed: A13 stdout reports measured source_files 14, style_violations [], and status PASS.
Verdict: OBJECT
Requested change: Replace the A13 style_violations lint with a principal-type-scheme and unification check for every let-bound expression.
Command: /usr/bin/env -C /Users/dylanwong/projects/quorum /Users/dylanwong/.gm-tools/agentplug-runner dispatch gm bash "$(printf 'SESSION_ID=%s\npython3 -I skills/quorum/scripts/verify_invariants.py --axiom A13\n' '74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r2sub6')"
Dispatch id: 1794902571234-99-522e2baabab6b16d
Session id: 74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r2sub6
Milner assigns each let binding a principal type scheme by unification; zero lint violations derive no type scheme. A PASS unsupported by generalization and instantiation is unmapped, so A13 must verify type inference before certifying well-typedness.
