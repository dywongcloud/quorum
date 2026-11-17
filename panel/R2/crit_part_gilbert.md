Anchor used: Brewers Conjecture and the Feasibility (Gilbert, Lynch)
Observed: A4 stdout reports measured.cap_sacrifice_declared=true.
Verdict: OBJECT
Requested change: Add a partition schedule and a read/write witness showing a stale read or a nonterminating operation; fail A4 without one.
Command: /usr/bin/env -C /Users/dylanwong/projects/quorum /Users/dylanwong/.gm-tools/agentplug-runner dispatch gm bash "$(printf 'SESSION_ID=%s\npython3 -I skills/quorum/scripts/verify_invariants.py --axiom A4\n' '74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r2sub12')"
Dispatch id: 1794903012004-104-fa8316235c9c71d
Session id: 74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r2sub12

In an asynchronous network with lost messages, no atomic register is both available and consistent. A boolean declaration is not that proof, and acyclicity says nothing about partitions. The log must exhibit the sacrificed guarantee plus the matching stale read or nonterminating operation.
