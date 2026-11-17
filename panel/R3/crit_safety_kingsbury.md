Anchor used: Jepsen Analyses (Kingsbury)
Observed: The live command reported linearizability_witness.checked=true with a single-register read/write model under real-time order, three fault-injected histories (partition drops the write acknowledgement), verdicts linearizable true/true/false, and safety_violations [2] marking history 2 as non-linearizable; the gm dispatch reproduced the same witness with exit_code 0.
Verdict: PASS
Requested change: none
Command: python3 -I skills/quorum/scripts/witnesses.py
Dispatch id: 1794908244181-127-31abfc462882030f
Session id: 74e7b6ba-202b-4e6a-acb1-d05f903aca3b-r3sub14
Statements of meaning: The measured witness means the system's safety claim was tested by a model checker against black-box operation histories with an injected partition, and history 2 admits no legal serialization under real-time order, so the checker refutes linearizability for that execution rather than merely assuming or asserting safety.
Designer questions: Does the design survive a partition that drops a write acknowledgement without producing an unserializable read/write history, and is that safety boundary demonstrated by an executable witness?
Critic questions: Did the earlier objection that no fault-injected history and linearizability check existed get answered by live measurement rather than by restated claims, i.e. is checked=true paired with an actual safety-violation history?
Opinions: The prior OBJECT is resolved. The witness is concrete, model-based, fault-injected, and independently reproduced through the gm dispatch; a recorded safety violation is stronger evidence for this anchor than a clean run would have been, because it shows the checker distinguishes linearizable from non-linearizable histories.
Andon pulled: none
