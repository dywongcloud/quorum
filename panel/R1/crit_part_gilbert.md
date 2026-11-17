Anchor used: Brewers Conjecture and the Feasibility (Gilbert, Lynch)
Observed: A4 reported status PASS with measured acyclic=true.
Verdict: OBJECT
Requested change: Add an A4 partition check that fails unless the log names consistency or availability as sacrificed under a partition.
Command: /usr/bin/env -C /Users/dylanwong/projects/quorum /Users/dylanwong/.gm-tools/agentplug-runner dispatch gm bash "$(printf 'SESSION_ID=%s\npython3 -I skills/quorum/scripts/verify_invariants.py --axiom A4\n' '74e7b6ba-202b-4e6a-acb1-d05f903aca3b-sub12')"
Dispatch id: 1794901567912-83-c693de77a990fddb
Session id: 74e7b6ba-202b-4e6a-acb1-d05f903aca3b-sub12

Gilbert and Lynch prove that an asynchronous partition forbids both atomic consistency and availability for every non-failing replica. Acyclic anchor reachability is not that network model and discharges neither safety nor liveness. A4 must record the explicit guarantee sacrificed during a partition.