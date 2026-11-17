Anchor used: Normal Accidents (Perrow)
Observed: all_reproducible false; FIGURE_MISMATCH on panel_verdicts (computed 23, printed 28) and selftest_cases (computed 6, printed 5).
Verdict: OBJECT
Requested change: Isolate each figure behind its own gate and fault code, so a single mismatch cannot propagate.
Command: /usr/bin/env -C /Users/dylanwong/projects/quorum /Users/dylanwong/.gm-tools/agentplug-runner dispatch gm bash "$(printf 'SESSION_ID=%s\npython3 -I scripts/validate_figures.py\n' '74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r2sub11')"
Dispatch id: 1794903020146-105-b4857ac055198b8
Session id: 74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r2sub11
Interactive complexity and tight coupling make accidents normal: two divergences here interact through one final boolean, hiding which failure propagated. Perrow demands slack and compartmentalization, not a coupled aggregate that turns local drift into a system-wide abort. Isolated fault signals let recovery begin before the cascade.
