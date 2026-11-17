# Primary texts, read during the build

The two primary books were downloaded and their full text extracted before any
anchor label was written. Chapter titles below are copied from the printed
table of contents and from chapter headings in the extracted text. Each row
maps a chapter to the QUORUM graph node that carries its doctrine. A chapter
with no node is recorded as DECLINE in `traversal-ledger.md`, never silently
dropped.

Provenance: `Site Reliability Engineering.pdf` (7.3 MB) and
`Designing-Data-Intensive-Applications.pdf` (4.2 MB) were fetched from the URLs
named in `canon.md`, stored outside the distributable skill, and read with
`pdftotext -layout`. No chapter title here is reconstructed from memory.

## Site Reliability Engineering (Beyer, Jones, Petoff, Murphy), 34 chapters

| Chapter | Title as printed | Graph node |
|---|---|---|
| 1 | Introduction | `srech1`, `srebook` |
| 2 | The Production Environment at Google, from the Viewpoint of an SRE | `borg`, `warehouse` |
| 3 | Embracing Risk | `errorbudget`, `harvest` |
| 4 | Service Level Objectives | `srech4`, `slo`, `sli` |
| 5 | Eliminating Toil | `toil` |
| 6 | Monitoring Distributed Systems | `monitoring`, `fourgolden` |
| 7 | The Evolution of Automation at Google | `runbook`, `configmanagement` |
| 8 | Release Engineering | `srech8`, `releaseengineering` |
| 9 | Simplicity | `c_kiss`, `metastable` |
| 10 | Practical Alerting | `alerting` |
| 11 | Being On-Call | `oncall` |
| 12 | Effective Troubleshooting | `c_five`, `observability` |
| 13 | Emergency Response | `incident` |
| 14 | Managing Incidents | `incident`, `c_stpa` |
| 15 | Postmortem Culture: Learning from Failure | `postmortem` |
| 16 | Tracking Outages | `postmortem` |
| 17 | Testing for Reliability | `c_chaos`, `faultinjection` |
| 18 | Software Engineering in SRE | `runbook` |
| 19 | Load Balancing at the Frontend | `anycast`, `cdn` |
| 20 | Load Balancing in the Datacenter | `codel`, `bbr` |
| 21 | Handling Overload | `overload`, `loadshedding`, `backpressure` |
| 22 | Addressing Cascading Failures | `srech22`, `cascadingfailure` |
| 23 | Managing Critical State: Distributed Consensus for Reliability | `paxos`, `raft`, `chubby` |
| 24 | Distributed Periodic Scheduling with Cron | `leases` |
| 25 | Data Processing Pipelines | `streamingsystems`, `kafka` |
| 26 | Data Integrity: What You Read Is What You Wrote | `srech26`, `backup`, `merkle` |
| 27 | Reliable Product Launches at Scale | `canary` |
| 28 | Accelerating SREs to On-Call and Beyond | `oncall` |
| 29 | Dealing with Interrupts | `toil` |
| 30 | Embedding an SRE to Build a Production Frame | `c_premortem` |
| 31 | Communication and Collaboration in SRE | `c_andon` |
| 32 | The Evolving SRE Engagement Model | `c_strangler` |
| 33 | Lessons Learned from Other Industries | `perrow`, `cookfail` |
| 34 | Conclusion | `sreworkbook` |

Chapters 2, 3, 21, 22, 23 and 26 carry the bulk of the physics, consensus and
operations anchors. Chapter 23 is the reason `paxos` and `raft` sit in RULES
rather than in STANCE: the book treats them as operational mechanisms, not as
impossibility results. The `flp` node remains in STANCE because FLP is a bound,
not a mechanism.

## Designing Data-Intensive Applications (Kleppmann), 11 chapters

| Chapter | Title as printed | Graph node |
|---|---|---|
| 1 | Reliable, Scalable and Maintainable Applications | `ddia`, `p99budget` |
| 2 | Data Models and Query Languages | `redbook`, `c_adt` |
| 3 | Storage and Retrieval | `lsmtree`, `btree`, `bloomfilter`, `databaseinternals` |
| 4 | Encoding and Evolution | `wal`, `c_hyrum` |
| 5 | Replication | `leaderelection`, `quorumread`, `sloppyquorum`, `readrepair`, `vectorclock` |
| 6 | Partitioning | `consistenthash`, `rendezvous`, `pastry` |
| 7 | Transactions | `twophase`, `snapshotiso`, `transactions`, `saga` |
| 8 | The Trouble with Distributed Systems | `fallacies`, `timeout`, `failuredetector`, `youngblood` |
| 9 | Consistency and Consensus | `ddia2`, `linearizability`, `fencing`, `byzgen`, `raft` |
| 10 | Batch Processing | `mapreduce`, `batchcanon` |
| 11 | Stream Processing | `streamingsystems`, `kafka`, `bookkeeper` |

Chapter 8 is where the fallacies and the failure-detector anchors come from;
chapter 9 is where the linearizability, fencing-token and consensus anchors
come from. Chapters 5 and 6 grounded the quorum and placement rules. The
`localfirst` breaker is grounded in the author's later Local-First Software
work, cited separately in `canon.md`, not in this book.

## What was declined

DDIA chapter 2's relational-model history and chapter 10's MapReduce lineage
do not bear on a verification-sandbox brief at the level of a design move, so
their nodes are DECLINE rows in the ledger. SRE chapters 28 through 32 are
organizational practice; they are retained as catalog and operations anchors
but no Decision Record spends a move on them. Declining is recorded, not
ignored.
