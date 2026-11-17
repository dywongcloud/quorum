Anchor used: Jepsen Analyses (Kingsbury)
Observed: The dispatch reported STATE_UNMAPPED for query_id unmapped.json and exit_code 1.
Verdict: OBJECT
Requested change: Add fault-injected black-box histories and check linearizability against a formal model.
Command: /usr/bin/env -C /Users/dylanwong/projects/quorum /Users/dylanwong/.gm-tools/agentplug-runner dispatch gm bash "$(printf 'SESSION_ID=%s\npython3 -I skills/quorum/scripts/epistemic_audit.py --payload state/unmapped.json\n' '74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r2sub14')"
Dispatch id: 1794903118414-107-aee89eb1af350617
Session id: 74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r2sub14
A single deterministic input rejection is not a history of concurrent operations under partition, pause, or crash faults. Jepsen requires black-box operation histories, injected nemeses, and a model checker that proves or refutes linearizability.
