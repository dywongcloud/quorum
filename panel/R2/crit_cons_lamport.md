Anchor used: The Part-Time Parliament (Lamport)
Observed: Roster stdout reports "seat_count": 14, all fourteen in required_seats, no ballot numbers.
Verdict: OBJECT
Requested change: Replace all-14 PASS with one numbered ballot chosen by eight intersecting-majority votes carrying the highest prior ballot.
Command: /usr/bin/env -C /Users/dylanwong/projects/quorum /Users/dylanwong/.gm-tools/agentplug-runner dispatch gm bash "$(printf 'SESSION_ID=%s\npython3 -I skills/quorum/scripts/graph_walk.py --roster --mode fail-closed\n' '74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r2sub9')"
Dispatch id: 1794902783000-100-3c9ec9cbb1ac197f
Session id: 74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r2sub9
A decree is chosen only when a majority accepts it in one numbered ballot, and any two majorities intersect. Fourteen-seat unanimity is no ballot, and without a total order on ballot numbers two rounds can choose conflicting decrees.
