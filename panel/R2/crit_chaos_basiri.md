Anchor used: Chaos Engineering (Basiri et al.)
Observed: The 400-sample probe reported p99_ms 0.1868 for monte-carlo-derivation-latency.
Verdict: OBJECT
Requested change: Add a continuously scheduled experiment that varies at least two real-world fault classes while measuring p99_ms as the steady-state metric.
Command: /usr/bin/env -C /Users/dylanwong/projects/quorum /Users/dylanwong/.gm-tools/agentplug-runner dispatch gm bash "$(printf 'SESSION_ID=%s\npython3 -I skills/quorum/scripts/epistemic_audit.py --probe 400\n' '74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r2sub8')"
Dispatch id: 1794902796771-102-8b55e0df4026b2ac
Session id: 74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r2sub8
Basiri et al. require varying real-world events against a steady state and automating experiments continuously. A fixed 400-sample latency probe supplies one condition, so add continuous rotation of distinct fault classes.
