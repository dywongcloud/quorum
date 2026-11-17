Anchor used: Jepsen Analyses (Kingsbury)
Observed: The audit stdout reports code STATE_UNMAPPED.
Verdict: OBJECT
Requested change: Add fault-injected black-box histories and check linearizability against a formal model.
Command: /usr/bin/env -C /Users/dylanwong/projects/quorum /Users/dylanwong/.gm-tools/agentplug-runner dispatch gm bash "$(printf 'SESSION_ID=%s\npython3 -I skills/quorum/scripts/epistemic_audit.py --payload state/unmapped.json\n' '74e7b6ba-202b-4e6a-acb1-d05f903aca3b-sub14')"
Dispatch id: 1794901835219-86-1f3d48d3bc54222b
Session id: 74e7b6ba-202b-4e6a-acb1-d05f903aca3b-sub14
Jepsen rejects design claims unless a black-box history from a running system is checked against a formal model under faults. A deterministic fault code is not a client-visible history, and no partition, crash, pause, clock-skew schedule, or legality checker appears here. It establishes no linearizability, failover safety, or recovery.
