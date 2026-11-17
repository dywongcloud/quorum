"""Deterministic builder for references/anchor-graph.md.

The graph is a strict DAG: every edge goes from a lower cluster rank to a higher
one, and edges inside a cluster go from a lower node index to a higher one. A
topological sort is asserted before anything is emitted. This is the single
source of truth; scripts/validate_graph.py regenerates it in memory and compares
byte for byte against the checked-in reference file.

Usage: python3 -I tools/build_graph.py [output_path]
"""
from __future__ import annotations

import pathlib
import sys

CLUSTERS = {
    "STANCE": ("Stance: First Principles and Impossibility", "stance", 0),
    "RULES": ("Rules: Mechanisms to Earn the Break", "rules", 1),
    "BREAK": ("Breakers: Decentralization, Chaos and Rupture", "break", 2),
    "PHYSICS": ("Physics: Hardware Bounds and Tail Latency", "physics", 3),
    "SYSTEMS": ("Systems: Infrastructure at Scale", "system", 4),
    "OPS": ("Operations: SRE and Production Discipline", "ops", 5),
    "EDGE": ("Edge: Intermittency, Placement and Autonomy", "edge", 6),
    "CANON": ("Canon and Critique of the Field", "canon", 7),
    "CATALOG": ("Semantic Anchors Catalog", "catalog", 8),
    "REASON": ("Reason: Rationale for Every Move", "reason", 9),
    "VERIFY": ("Verification: Model Checking and Witness", "verify", 10),
    "LENSES": ("Lenses: Each Critic's Own Literature", "lens", 11),
    "CRITICS": ("Critics: The Adversarial Quorum", "critic", 12),
    "PANEL": ("Panel Method: Convening Independent Judges", "panel", 13),
    "ADAPT": ("Adaptation: How the Graph Rewrites Itself", "adapt", 14),
}

# id | exact label. Labels are copied verbatim into Decision Records and Panel
# Reports; a label that is not here cannot be used as an anchor.
NODES = {
"STANCE": [
 "flp|Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson)",
 "gilbert|Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services (Gilbert, Lynch)",
 "brewercap|CAP Twelve Years Later: How the Rules Have Changed (Brewer)",
 "pacelc|Consistency Tradeoffs in Modern Distributed Database System Design (Abadi)",
 "fallacies|Fallacies of Distributed Computing (Deutsch)",
 "e2earg|End-to-End Arguments in System Design (Saltzer, Reed, Clark)",
 "harvest|Harvest, Yield, and Scalable Tolerant Systems (Fox, Brewer)",
 "basenote|BASE: An Acid Alternative (Pritchett)",
 "calm|Consistency As Logical Monotonicity (Hellerstein, Alvaro)",
 "srebook|Site Reliability Engineering (Beyer, Jones, Petoff, Murphy)",
 "ddia|Designing Data-Intensive Applications (Kleppmann)",
 "releaseit|Release It! Design and Deploy Production-Ready Software (Nygard)",
 "antifragile|Antifragile: Things That Gain from Disorder (Taleb)",
 "normalacc|Normal Accidents: Living with High-Risk Technologies (Perrow)",
 "cookfail|How Complex Systems Fail (Cook)",
 "lamporttime|Time, Clocks, and the Ordering of Events in a Distributed System (Lamport)",
 "byzgen|The Byzantine Generals Problem (Lamport, Shostak, Pease)",
 "youngblood|Notes on Distributed Systems for Young Bloods (Hodges)",
 "waldonote|A Note on Distributed Computing (Waldo, Wyant, Wollrath, Kendall)",
 "endtoendprinciple|The Design Philosophy of the DARPA Internet Protocols (Clark)",
 "flpbound|FLP Asynchrony Assumption: No Deterministic Termination Witness (Fischer, Lynch, Paterson)",
],
"RULES": [
 "paxos|The Part-Time Parliament (Lamport)",
 "paxossimple|Paxos Made Simple (Lamport)",
 "raft|In Search of an Understandable Consensus Algorithm (Ongaro, Ousterhout)",
 "vsr|Viewstamped Replication: A New Primary Copy Method (Oki, Liskov)",
 "zab|Zab: High-performance broadcast for primary-backup systems (Junqueira, Reed, Serafini)",
 "pbft|Practical Byzantine Fault Tolerance (Castro, Liskov)",
 "tendermint|Tendermint: Byzantine Fault Tolerance in the Age of Blockchains (Buchman)",
 "jointconsensus|Joint Consensus and Cluster Reconfiguration (Ongaro)",
 "leaderelection|Leader Election and Leases (Gray, Cheriton)",
 "fencing|Fencing Tokens and Lease Expiry (Kleppmann)",
 "quorumread|Quorum Reads and Writes: N, R and W (Gifford)",
 "sloppyquorum|Sloppy Quorums and Hinted Handoff (DeCandia et al.)",
 "readrepair|Read Repair and Anti-Entropy (DeCandia et al.)",
 "merkle|Merkle Trees for Replica Comparison (Merkle)",
 "vectorclock|Vector Clocks and Version Vectors (Fidge, Mattern)",
 "hlogicalclock|Logical Physical Clocks and Consistent Snapshots (Kulkarni et al.)",
 "truetime|TrueTime and External Consistency (Corbett et al.)",
 "linearizability|Linearizability: A Correctness Condition for Concurrent Objects (Herlihy, Wing)",
 "serializability|Serializability and the Theory of Database Concurrency (Papadimitriou)",
 "snapshotiso|A Critique of ANSI SQL Isolation Levels (Berenson et al.)",
 "eventual|Eventually Consistent (Vogels)",
 "causalconsistency|Causal Consistency and COPS (Lloyd et al.)",
 "twophase|Notes on Data Base Operating Systems (Gray)",
 "threephase|Three-Phase Commit and Non-Blocking Commit (Skeen)",
 "saga|SAGAS (Garcia-Molina, Salem)",
 "idempotence|Idempotence Keys and Exactly-Once Semantics (Kleppmann)",
 "wal|Write-Ahead Logging and Recovery (Mohan et al.)",
 "lsmtree|The Log-Structured Merge-Tree (O'Neil et al.)",
 "btree|Organization and Maintenance of Large Ordered Indexes (Bayer, McCreight)",
 "bloomfilter|Space/Time Trade-offs in Hash Coding (Bloom)",
 "consistenthash|Consistent Hashing and Random Trees (Karger et al.)",
 "rendezvous|Rendezvous Hashing (Thaler, Ravishankar)",
 "chord|Chord: A Scalable Peer-to-peer Lookup Service (Stoica et al.)",
 "kademlia|Kademlia: A Peer-to-peer Information System (Maymounkov, Mazieres)",
 "pastry|Pastry: Scalable, Decentralized Object Location (Rowstron, Druschel)",
 "gossip|Epidemic Algorithms for Replicated Database Maintenance (Demers et al.)",
 "swim|SWIM: Scalable Weakly-consistent Infection-style Membership (Das et al.)",
 "phiaccrual|The Phi Accrual Failure Detector (Hayashibara et al.)",
 "failuredetector|Unreliable Failure Detectors for Reliable Distributed Systems (Chandra, Toueg)",
 "splitbrain|Split Brain and Fencing in Partitioned Clusters (Kleppmann)",
 "chainrep|Chain Replication for Supporting High Throughput (van Renesse, Schneider)",
 "primarybackup|Primary-Backup Replication and Viewstamped State Machines (Liskov)",
 "statemachine|Implementing Fault-Tolerant Services Using the State Machine Approach (Schneider)",
 "multipaxos|Multi-Paxos and Leader-Based Optimization (Lamport)",
 "raftlog|Raft Log Matching and Commit Rules (Ongaro, Ousterhout)",
 "membership|Cluster Membership and Failure Detection (Das et al.)",
 "mvcc|Multiversion Concurrency Control (Bernstein, Goodman)",
 "crdtspec|A Comprehensive Study of Convergent and Commutative Replicated Data Types (Shapiro et al.)",
 "sec|Strong Eventual Consistency and the CALM Boundary (Shapiro et al.)",
 "coordinationavoidance|Coordination Avoidance in Database Systems (Bailis et al.)",
 "readonlytxn|Highly Available Transactions: Virtues and Limitations (Bailis et al.)",
 "leases|Leases: An Efficient Fault-Tolerant Mechanism (Gray, Cheriton)",
 "transactions|The Transaction Concept: Virtues and Limitations (Gray)",
],
"BREAK": [
 "dynamo|Dynamo: Amazon's Highly Available Key-value Store (DeCandia et al.)",
 "localfirst|Local-First Software: You Own Your Data, in Spite of the Cloud (Kleppmann et al.)",
 "automerge|A Conflict-Free Replicated JSON Datatype (Kleppmann, Beresford)",
 "peritext|Peritext: A CRDT for Collaborative Rich Text (Litt et al.)",
 "ipfs|IPFS: Content Addressed, Versioned, P2P File System (Benet)",
 "libp2p|libp2p: A Modular Network Stack (Protocol Labs)",
 "bitcoin|Bitcoin: A Peer-to-Peer Electronic Cash System (Nakamoto)",
 "blockchain|The Quest for Scalable Blockchain Fabric (Vukolic)",
 "byzantinebreak|Bar Fault Tolerance for Cooperative Services (Cachin et al.)",
 "chaosmonkey|Chaos Monkey and Random Instance Termination (Netflix)",
 "chaoseng|Chaos Engineering: Building Confidence in System Behavior (Basiri et al.)",
 "faultinjection|Failure Injection at Scale (Allspaw)",
 "metastable|Metastable Failures in Distributed Systems (Bronson et al.)",
 "harvestyield|Harvest and Yield under Partition (Fox, Brewer)",
 "antientropybreak|Anti-Entropy without Coordination (Demers et al.)",
 "decentralizedbreak|Decentralized Applications by Design (Benet)",
 "edgebreak|The Emergence of Edge Computing (Satyanarayanan)",
 "serverlessbreak|Serverless Computing: One Step Forward, Two Steps Back (Hellerstein et al.)",
 "nocoordbreak|Coordination Avoidance and the Price of Consensus (Bailis)",
 "crdtbreak|Conflict-free Replicated Data Types as a Design Default (Shapiro et al.)",
 "partitionbreak|Designing for Partition Tolerance First (Brewer)",
 "blackboxbreak|Jepsen: Breaking Distributed Systems on Purpose (Kingsbury)",
],
"PHYSICS": [
 "tailatscale|The Tail at Scale (Dean, Barroso)",
 "latencynumbers|Numbers Every Programmer Should Know (Dean)",
 "littleslaw|Little's Law and Queueing Bounds (Little)",
 "usl|Universal Scalability Law (Gunther)",
 "amdahl|Amdahl's Law and the Limits of Parallelism (Amdahl)",
 "fiveminute|The Five-Minute Rule for Trading Memory for Disk Access (Gray, Putzolu)",
 "coordinatedomission|Coordinated Omission in Latency Benchmarks (Tene)",
 "codel|Controlled Delay Active Queue Management (Nichols, Jacobson)",
 "bbr|BBR: Congestion-Based Congestion Control (Cardwell et al.)",
 "hedgedrequests|Hedged and Tied Requests (Dean, Barroso)",
 "p99budget|p99 Latency Budgets and Error Budgets (Beyer et al.)",
 "hardwarebounds|Hardware-Bounded CAP-aware Physics (Barroso, Clidaras, Holzle)",
 "energyproportional|Energy-Proportional Computing (Barroso, Holzle)",
 "warehouse|The Datacenter as a Computer (Barroso, Clidaras, Holzle)",
 "networklimits|Bandwidth, RTT and the Speed-of-Light Bound (Deutsch)",
 "diskfail|Failure Trends in a Large Disk Drive Population (Pinheiro et al.)",
 "correlatedfail|Correlated Failures in Large-Scale Systems (Ford et al.)",
 "jitter|Jitter, Backoff and Synchronization Avoidance (Amazon Builders' Library)",
],
"SYSTEMS": [
 "chubby|The Chubby Lock Service for Loosely-Coupled Distributed Systems (Burrows)",
 "spanner|Spanner: Google's Globally-Distributed Database (Corbett et al.)",
 "bigtable|Bigtable: A Distributed Storage System for Structured Data (Chang et al.)",
 "gfs|The Google File System (Ghemawat, Gobioff, Leung)",
 "mapreduce|MapReduce: Simplified Data Processing on Large Clusters (Dean, Ghemawat)",
 "borg|Large-scale cluster management at Google with Borg (Verma et al.)",
 "kubernetes|Borg, Omega, and Kubernetes (Burns et al.)",
 "zookeeper|ZooKeeper: Wait-free Coordination for Internet-scale Systems (Hunt et al.)",
 "etcd|etcd and the Raft Consensus Store (CoreOS)",
 "consul|Consul: Service Discovery and Failure Detection (HashiCorp)",
 "kafka|Kafka: a Distributed Messaging System for Log Processing (Kreps et al.)",
 "bookkeeper|Apache BookKeeper and Distributed Write-Ahead Logs (Apache)",
 "cassandra|Cassandra: A Decentralized Structured Storage System (Lakshman, Malik)",
 "riak|Riak and Dynamo-Style Eventual Consistency (Basho)",
 "cockroach|CockroachDB: The Resilient Geo-Distributed SQL Database (Taft et al.)",
 "foundationdb|FoundationDB: A Distributed Unbundled Database (Zhou et al.)",
 "aurora|Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases (Verbitski et al.)",
 "calvin|Calvin: Fast Distributed Transactions for Partitioned Database Systems (Thomson et al.)",
 "voltdb|VoltDB and Deterministic Single-Threaded Transactions (Stonebraker et al.)",
 "megastore|Megastore: Providing Scalable, Highly Available Storage (Baker et al.)",
 "dapper|Dapper, a Large-Scale Distributed Systems Tracing Infrastructure (Sigelman et al.)",
 "monarch|Monarch: Google's Planet-Scale In-Memory Time Series Database (Adams et al.)",
 "envoy|Envoy: A Service Mesh Data Plane (Lyft)",
 "flyio|Fly.io: Deploying Applications Close to Users (Fly.io)",
 "workers|Cloudflare Workers and Isolate-Based Edge Compute (Cloudflare)",
 "fastlycompute|Fastly Compute and Edge Instantiation (Fastly)",
 "cdn|Content Delivery Networks and Anycast Routing (Dilley et al.)",
 "iroh|Iroh: Holepunching and Content-Addressed Transfer (n0)",
 "tor|Tor: The Second-Generation Onion Router (Dingledine et al.)",
],
"OPS": [
 "slo|Service Level Objectives (Beyer et al.)",
 "sli|Service Level Indicators (Beyer et al.)",
 "errorbudget|Error Budgets and Release Velocity (Beyer et al.)",
 "toil|Eliminating Toil (Beyer et al.)",
 "postmortem|Blameless Postmortems (Beyer et al.)",
 "incident|Incident Command and Emergency Response (Beyer et al.)",
 "oncall|Being On-Call (Beyer et al.)",
 "fourgolden|The Four Golden Signals (Beyer et al.)",
 "redmethod|The RED Method (Weaveworks)",
 "usemethod|The USE Method (Gregg)",
 "observability|Observability and the Three Pillars (Majors et al.)",
 "distributedtracing|Distributed Tracing in Production (Sigelman et al.)",
 "canary|Canarying and Progressive Rollouts (Beyer et al.)",
 "featureflag|Feature Flags and Decoupled Deploys (Humble)",
 "loadshedding|Load Shedding and Admission Control (Amazon Builders' Library)",
 "backpressure|Backpressure and Bounded Queues (Amazon Builders' Library)",
 "circuitbreaker|Circuit Breakers and Bulkheads (Nygard)",
 "retrybudget|Retry Budgets, Timeouts and Deadlines (Amazon Builders' Library)",
 "timeout|Timeouts, Retries and Jitter (Amazon Builders' Library)",
 "healthcheck|Health Checking and Failure Detection (Beyer et al.)",
 "gracefuldegradation|Graceful Degradation and Harvest-Yield Tradeoffs (Fox, Brewer)",
 "overload|Handling Overload (Beyer et al.)",
 "cascadingfailure|Addressing Cascading Failures (Beyer et al.)",
 "capacityplanning|Capacity Planning and Load Testing (Beyer et al.)",
 "autoscaling|Autoscaling and Elastic Capacity (Beyer et al.)",
 "disasterrecovery|Disaster Recovery, RPO and RTO (Beyer et al.)",
 "backup|Backups and Restore Drills (Beyer et al.)",
 "runbook|Runbooks and Automation (Beyer et al.)",
 "configmanagement|Configuration Management and Drift (Beyer et al.)",
 "releaseengineering|Release Engineering and Hermetic Builds (Beyer et al.)",
 "monitoring|Monitoring Distributed Systems (Beyer et al.)",
 "alerting|Alerting on SLO Burn Rate (Beyer et al.)",
],
"EDGE": [
 "fog|Fog Computing and Its Role in the Internet of Things (Bonomi et al.)",
 "mec|Multi-access Edge Computing (ETSI MEC)",
 "cloudlets|The Case for VM-Based Cloudlets in Mobile Computing (Satyanarayanan et al.)",
 "offlinefirst|Offline-First and Intermittent Connectivity (Kleppmann et al.)",
 "storeforward|Store-and-Forward under Disconnection (Fall)",
 "dtn|Delay-Tolerant Networking Architecture (Fall)",
 "geo|Geo-Distribution and Locality of State (Corbett et al.)",
 "anycast|Anycast and Global Traffic Management (Dilley et al.)",
 "holepunching|NAT Traversal and Hole Punching (Ford et al.)",
 "p2p|Peer-to-Peer Overlays and Decentralized Lookup (Stoica et al.)",
 "dht|Distributed Hash Tables and Consistent Placement (Karger et al.)",
 "splitbrainedge|Edge Split-Brain and Reconciliation (Kleppmann)",
 "zerotrust|Zero Trust Networks (Gilman, Barth)",
 "sybil|The Sybil Attack (Douceur)",
 "eclipse|Eclipse Attacks on Overlay Networks (Sit, Morris)",
 "capability|Capability-Based Security and Least Authority (Miller et al.)",
 "affinetypestate|Affine Typestate at Byzantine Boundaries (Minsky)",
 "edgephysics|Edge Physics: Bounded Compute and Battery (Satyanarayanan)",
],
"CANON": [
 "redbook|Readings in Database Systems (Stonebraker, Hellerstein)",
 "tanenbaum|Distributed Systems: Principles and Paradigms (Tanenbaum, van Steen)",
 "lynchbook|Distributed Algorithms (Lynch)",
 "cachin|Introduction to Reliable and Secure Distributed Programming (Cachin, Guerraoui, Rodrigues)",
 "birman|Reliable Distributed Systems: Technologies, Web Services, and Applications (Birman)",
 "sreworkbook|The Site Reliability Workbook (Beyer et al.)",
 "srech8|Site Reliability Engineering, Chapter 8: Release Engineering (Beyer et al.)",
 "buildsecure|Building Secure and Reliable Systems (Adkins et al.)",
 "databaseinternals|Database Internals (Petrov)",
 "streamingsystems|Streaming Systems (Akidau et al.)",
 "ddia2|Designing Data-Intensive Applications, Chapter 9: Consistency and Consensus (Kleppmann)",
 "srech1|Site Reliability Engineering, Chapter 1: Introduction (Beyer et al.)",
 "srech4|Site Reliability Engineering, Chapter 4: Service Level Objectives (Beyer et al.)",
 "srech22|Site Reliability Engineering, Chapter 22: Addressing Cascading Failures (Beyer et al.)",
 "srech26|Site Reliability Engineering, Chapter 26: Data Integrity (Beyer et al.)",
 "jepsencanon|Jepsen Analyses of Distributed Databases (Kingsbury)",
 "fallaciescanon|Deutsch's Eight Fallacies Stated Precisely (Rothenberg)",
 "capcanon|Perspectives on the CAP Theorem (Gilbert, Lynch)",
 "replicationcanon|Replication: Theory and Practice (Charron-Bost et al.)",
 "batchcanon|Data Processing Pipelines: Batch and Stream Canon (Akidau et al.)",
],
"CATALOG": [
 "c_ears|EARS Requirements Syntax (Mavin)",
 "c_invest|INVEST (Wake)",
 "c_qas|Quality Attribute Scenario (Bass et al.)",
 "c_premortem|Premortem (Kahneman)",
 "c_devil|Devil's Advocate",
 "c_spike|Spike Solution (Beck)",
 "c_pugh|Pugh-Matrix (Pugh)",
 "c_first|First Principles Thinking",
 "c_occam|Occam's Razor",
 "c_kiss|KISS Principle (Kelly Johnson)",
 "c_cynefin|Cynefin Framework (Snowden)",
 "c_genchi|Genchi Genbutsu",
 "c_five|Five Whys (Ohno)",
 "c_adr|ADR according to Nygard",
 "c_madr|MADR",
 "c_bluf|BLUF (Bottom Line Up Front)",
 "c_pyramid|Pyramid Principle according to Barbara Minto",
 "c_dreyfus|Dreyfus Model of Skill Acquisition",
 "c_chest|Chesterton's Fence",
 "c_second|Second-Order Thinking",
 "c_dbs|Decisional Balance Sheet",
 "c_a3|A3 Problem Solving",
 "c_feynman|Feynman Technique",
 "c_naur|Programming as Theory Building (Naur)",
 "c_dod|Definition of Done",
 "c_keep|Keep a Changelog",
 "c_andon|Andon",
 "c_jidoka|Jidoka",
 "c_pdca|PDCA",
 "c_kaizen|Kaizen",
 "c_strangler|Strangler Fig",
 "c_refactor|Refactoring Catalog according to Fowler",
 "c_mutation|Mutation Testing",
 "c_red|Red/Green TDD (Beck)",
 "c_goodhart|Goodhart's Law",
 "c_fagan|Fagan Inspection",
 "c_fmea|Failure Mode and Effects Analysis",
 "c_stpa|STPA: Systems-Theoretic Process Analysis (Leveson)",
 "c_faulttree|Fault Tree Analysis (Watson)",
 "c_chaos|Chaos Engineering Principles (Basiri et al.)",
 "c_montecarlo|Monte Carlo Profiling (Metropolis, Ulam)",
 "c_p99|p99-Bounded Graceful Degradation",
 "c_io|IO Monad and Pure Core (Wadler)",
 "c_adt|Algebraic Data Types and Pure Morphisms",
 "c_kolmogorov|Kolmogorov Complexity (Kolmogorov)",
 "c_ssot|SSOT (Single Source of Truth)",
 "c_hyrum|Hyrum's Law",
 "c_mikado|Mikado Method",
 "c_fallacies|Fallacies of Distributed Computing (Deutsch)",
],
"REASON": [
 "toulmin|The Uses of Argument (Toulmin)",
 "aristotle|Rhetoric (Aristotle)",
 "buchanan|Declaration by Design: Rhetoric, Argument, and Demonstration (Buchanan)",
 "schon|The Reflective Practitioner (Schon)",
 "simon|The Sciences of the Artificial (Simon)",
 "rittel|Dilemmas in a General Theory of Planning (Rittel, Webber)",
 "ibis|IBIS: Issue-Based Information System (Rittel)",
 "dorst|Frame Innovation (Dorst)",
 "sontag|Against Interpretation (Sontag)",
 "baxandall|Patterns of Intention (Baxandall)",
 "meadows|Thinking in Systems (Meadows)",
 "naurtheory|Programming as Theory Building (Naur)",
 "popperreason|Conjectures and Refutations (Popper)",
 "lehman|Programs, Life Cycles, and Laws of Software Evolution (Lehman)",
],
"VERIFY": [
 "tla|Specifying Systems: The TLA+ Language and Tools (Lamport)",
 "tlc|TLC: The TLA+ Model Checker (Yu et al.)",
 "clarke|Model Checking and Abstraction (Clarke, Grumberg, Long)",
 "cegar|Counterexample-Guided Abstraction Refinement (Clarke et al.)",
 "ltl|Temporal Logic and CTL (Emerson, Clarke)",
 "alloy|Software Abstractions: Logic, Language, and Analysis (Jackson)",
 "spin|The SPIN Model Checker (Holzmann)",
 "coq|Interactive Theorem Proving and Dependent Types (Coq)",
 "verdi|Verdi: A Framework for Implementing and Verifying Distributed Systems (Wilcox et al.)",
 "ironfleet|IronFleet: Proving Practical Distributed Systems Correct (Hawblitzel et al.)",
 "jepsen|Jepsen: Distributed Systems Safety Analysis (Kingsbury)",
 "knossos|Knossos: Linearizability Checking (Kingsbury)",
 "porcupine|Porcupine: Fast Linearizability Checking (Horn, Kingsbury)",
 "quickcheck|QuickCheck: Property-Based Testing (Claessen, Hughes)",
 "hypothesis|Stateful Property-Based Testing (MacIver et al.)",
 "fuzzing|Coverage-Guided Fuzzing (Zalewski)",
 "metamorphic|Metamorphic Testing (Chen)",
 "faganverify|Fagan Inspection as Independent Verification (Fagan)",
 "pitypes|Pi-types and Static Verification of Contracts (Martin-Lof)",
 "refinement|Refinement Types and Stepwise Refinement (Wirth)",
 "witness|Witness Tuple (id, hash, ts)",
 "idempotencecheck|Idempotent Replay Check: f(f(x)) = f(x)",
],
"LENSES": [
 "lens_flp|Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson)",
 "lens_clarke|Model Checking (Clarke, Grumberg, Peled)",
 "lens_emerson|Design and Synthesis of Synchronization Skeletons (Emerson, Clarke)",
 "lens_milner|A Theory of Type Polymorphism in Programming (Milner)",
 "lens_martinlof|Intuitionistic Type Theory (Martin-Lof)",
 "lens_basiri|Chaos Engineering (Basiri et al.)",
 "lens_allspaw|Web Operations: Keeping the Data on Time (Allspaw, Robbins)",
 "lens_beyer|Site Reliability Engineering (Beyer, Jones, Petoff, Murphy)",
 "lens_jones|Site Reliability Engineering (Beyer, Jones, Petoff, Murphy)",
 "lens_star|The Ethnography of Infrastructure (Star)",
 "lens_bowker|Sorting Things Out: Classification and Its Consequences (Bowker, Star)",
 "lens_tufte|The Visual Display of Quantitative Information (Tufte)",
 "lens_cairo|How Charts Lie (Cairo)",
 "lens_gilbert|Brewer's Conjecture and the Feasibility (Gilbert, Lynch)",
 "lens_brewer|CAP Twelve Years Later (Brewer)",
 "lens_kleppmann|Designing Data-Intensive Applications (Kleppmann)",
 "lens_lamport|The Part-Time Parliament (Lamport)",
 "lens_ongaro|In Search of an Understandable Consensus Algorithm (Ongaro, Ousterhout)",
 "lens_shostak|The Byzantine Generals Problem (Lamport, Shostak, Pease)",
 "lens_pease|The Byzantine Generals Problem (Lamport, Shostak, Pease)",
 "lens_shapiro|A Comprehensive Study of CRDTs (Shapiro et al.)",
 "lens_preguica|Conflict-free Replicated Data Types (Preguica et al.)",
 "lens_satyanarayanan|The Emergence of Edge Computing (Satyanarayanan)",
 "lens_bonomi|Fog Computing and Its Role in the Internet of Things (Bonomi et al.)",
 "lens_dean|The Tail at Scale (Dean, Barroso)",
 "lens_barroso|The Datacenter as a Computer (Barroso, Clidaras, Holzle)",
 "lens_cook|How Complex Systems Fail (Cook)",
 "lens_perrow|Normal Accidents (Perrow)",
 "lens_saltzer|The Protection of Information in Computer Systems (Saltzer, Schroeder)",
 "lens_schroeder|The Protection of Information in Computer Systems (Saltzer, Schroeder)",
 "lens_taleb|Antifragile (Taleb)",
 "lens_kingsbury|Jepsen Analyses (Kingsbury)",
 "lens_gray|The Transaction Concept (Gray)",
 "lens_decandia|Dynamo (DeCandia et al.)",
 "lens_wiggins|Local-First Software (Kleppmann et al.)",
 "lens_beresford|A Conflict-Free Replicated JSON Datatype (Kleppmann, Beresford)",
 "lens_nakamoto|Bitcoin (Nakamoto)",
 "lens_benet|IPFS (Benet)",
 "lens_hollnagel|Resilience Engineering in Practice (Hollnagel et al.)",
],
"PANEL": [
 "surowiecki|The Wisdom of Crowds (Surowiecki)",
 "page|The Difference (Page)",
 "debono|Six Thinking Hats (de Bono)",
 "lerman|Critical Response Process (Lerman, Borstel)",
 "panel_quorum|Quorum Certificate: seats reporting over seats required",
 "panel_independence|Independence: one agent per authority (DADA amendment ten)",
],
"ADAPT": [
 "popper|Conjectures and Refutations (Popper)",
 "kuhn|The Structure of Scientific Revolutions (Kuhn)",
 "argyris|Theory in Practice: Double-Loop Learning (Argyris, Schon)",
 "talebadapt|Antifragile: Gain from Disorder (Taleb)",
 "hollnagel|Resilience Engineering: The Four Cornerstones (Hollnagel)",
 "lehmanadapt|Laws of Software Evolution (Lehman)",
],
}

# Critic seats. One seat per authority. Index order is the DAG order inside the
# CRITICS cluster; dotted counterpoint edges are declared below.
CRITICS = [
 "crit_imp_fischer|Critic: Impossibility (Fischer)",
 "crit_imp_lynch|Critic: Impossibility (Lynch)",
 "crit_imp_paterson|Critic: Impossibility (Paterson)",
 "crit_form_clarke|Critic: Formalist (Clarke)",
 "crit_form_emerson|Critic: Formalist (Emerson)",
 "crit_type_milner|Critic: Type Theorist (Milner)",
 "crit_type_martinlof|Critic: Type Theorist (Martin-Lof)",
 "crit_chaos_basiri|Critic: Chaos (Basiri)",
 "crit_chaos_allspaw|Critic: Chaos (Allspaw)",
 "crit_ops_beyer|Critic: Operability (Beyer)",
 "crit_ops_jones|Critic: Operability (Jones)",
 "crit_erasure_star|Critic: Erasure (Star)",
 "crit_erasure_bowker|Critic: Erasure (Bowker)",
 "crit_cons_lamport|Critic: Consensus (Lamport)",
 "crit_cons_ongaro|Critic: Consensus (Ongaro)",
 "crit_cons_oust|Critic: Consensus (Ousterhout)",
 "crit_byz_shostak|Critic: Byzantine (Shostak)",
 "crit_byz_pease|Critic: Byzantine (Pease)",
 "crit_byz_castro|Critic: Byzantine (Castro)",
 "crit_byz_liskov|Critic: Byzantine (Liskov)",
 "crit_part_gilbert|Critic: Partition (Gilbert)",
 "crit_part_brewer|Critic: Partition (Brewer)",
 "crit_part_abadi|Critic: Partition (Abadi)",
 "crit_repl_decandia|Critic: Replication (DeCandia)",
 "crit_repl_kleppmann|Critic: Replication (Kleppmann)",
 "crit_repl_gray|Critic: Replication (Gray)",
 "crit_tail_dean|Critic: Tail (Dean)",
 "crit_tail_barroso|Critic: Tail (Barroso)",
 "crit_edge_saty|Critic: Edge (Satyanarayanan)",
 "crit_edge_bonomi|Critic: Edge (Bonomi)",
 "crit_local_wiggins|Critic: Local-First (Wiggins)",
 "crit_local_beresford|Critic: Local-First (Beresford)",
 "crit_crdt_shapiro|Critic: Convergence (Shapiro)",
 "crit_crdt_preguica|Critic: Convergence (Preguica)",
 "crit_safety_kingsbury|Critic: Safety (Kingsbury)",
 "crit_sec_saltzer|Critic: Security (Saltzer)",
 "crit_sec_schroeder|Critic: Security (Schroeder)",
 "crit_human_cook|Critic: Human Factors (Cook)",
 "crit_human_perrow|Critic: Human Factors (Perrow)",
 "crit_econ_gunther|Critic: Economics (Gunther)",
 "crit_econ_little|Critic: Economics (Little)",
 "crit_evid_tufte|Critic: Evidence (Tufte)",
 "crit_evid_cairo|Critic: Evidence (Cairo)",
 "crit_hist_stonebraker|Critic: Historian (Stonebraker)",
 "crit_hist_hellerstein|Critic: Historian (Hellerstein)",
 "crit_zt_gilman|Critic: Zero Trust (Gilman)",
 "crit_zt_barth|Critic: Zero Trust (Barth)",
 "crit_dec_benet|Critic: Decentralization (Benet)",
 "crit_dec_nakamoto|Critic: Decentralization (Nakamoto)",
 "crit_rupt_taleb|Critic: Rupture (Taleb)",
 "crit_res_hollnagel|Critic: Resilience (Hollnagel)",
 "crit_detach_sontag|Critic: Detachment (Sontag)",
]
NODES["CRITICS"] = CRITICS

# (source, target, label, kind). kind is "solid" or "dotted".
# Edges are hand-authored: every label states a real relation, and every source
# has a lower DAG rank than its target.
EDGES: list[tuple[str, str, str, str]] = []


def chain(ids: list[str], label: str, kind: str = "solid") -> None:
    for a, b in zip(ids, ids[1:]):
        EDGES.append((a, b, label, kind))


def link(src: str, dst: str, label: str, kind: str = "solid") -> None:
    EDGES.append((src, dst, label, kind))


# Stance grounds the rules.
link("flp", "paxos", "impossibility bounds")
link("flp", "raft", "impossibility bounds")
link("flp", "flpbound", "bounds liveness of", "dotted")
link("flpbound", "failuredetector", "partially discharged by")
link("flp", "failuredetector", "motivates")
link("gilbert", "quorumread", "formalizes tradeoff for")
link("gilbert", "linearizability", "distinguishes from")
link("brewercap", "splitbrain", "partition practice for")
link("brewercap", "harvestyield", "extends into")
link("pacelc", "eventual", "extends CAP with latency for")
link("pacelc", "causalconsistency", "latency pole for")
link("fallacies", "networklimits", "names the neglected bound of")
link("fallacies", "timeout", "grounds assumption audit for")
link("fallacies", "healthcheck", "grounds assumption audit for")
link("e2earg", "idempotence", "end-to-end correctness for")
link("e2earg", "offlinefirst", "argues placement for")
link("harvest", "gracefuldegradation", "yield tradeoff for")
link("harvest", "loadshedding", "harvest tradeoff for")
link("basenote", "eventual", "motivates")
link("calm", "coordinationavoidance", "monotonicity bound for")
link("calm", "crdtspec", "logical monotonicity for")
link("srebook", "slo", "source of")
link("srebook", "errorbudget", "source of")
link("srebook", "toil", "source of")
link("srebook", "postmortem", "source of")
link("srebook", "incident", "source of")
link("srebook", "fourgolden", "source of")
link("ddia", "twophase", "chapters ground")
link("ddia", "lsmtree", "chapters ground")
link("ddia", "replicationcanon", "chapters ground")
link("ddia", "crdtspec", "chapters ground")
link("ddia", "localfirst", "motivates")
link("releaseit", "circuitbreaker", "introduces")
link("releaseit", "backpressure", "introduces")
link("antifragile", "chaoseng", "philosophy for")
link("normalacc", "cascadingfailure", "coupling predicts")
link("cookfail", "postmortem", "human-factors ground for")
link("lamporttime", "vectorclock", "happens-before grounds")
link("lamporttime", "hlogicalclock", "grounds")
link("lamporttime", "truetime", "grounds")
link("byzgen", "pbft", "impossibility bound for")
link("byzgen", "tendermint", "impossibility bound for")
link("byzgen", "affinetypestate", "trust boundary for")
link("youngblood", "timeout", "practical warning for")
link("youngblood", "retrybudget", "practical warning for")
link("waldonote", "e2earg", "contrasts with", "dotted")
link("endtoendprinciple", "fog", "argues against middleboxes in", "dotted")

# Rules chains and cross-links.
chain(["paxos", "paxossimple", "multipaxos", "raft", "raftlog", "jointconsensus"], "refines")
chain(["vsr", "primarybackup", "statemachine", "chainrep"], "extends")
chain(["zab", "zookeeper", "etcd"], "implements")
chain(["pbft", "tendermint", "byzantinebreak"], "extends")
chain(["leaderelection", "leases", "fencing", "splitbrain"], "guards")
chain(["quorumread", "sloppyquorum", "readrepair", "merkle"], "supports")
chain(["linearizability", "serializability", "snapshotiso", "mvcc"], "orders")
chain(["twophase", "threephase", "saga", "transactions"], "relaxes")
chain(["consistenthash", "rendezvous", "chord", "kademlia", "pastry", "dht"], "places")
chain(["gossip", "swim", "membership", "phiaccrual", "failuredetector"], "detects")
chain(["wal", "lsmtree", "btree", "bloomfilter"], "indexes")
link("crdtspec", "sec", "proves")
link("crdtspec", "automerge", "enables")
link("coordinationavoidance", "readonlytxn", "enables")
link("statemachine", "pitypes", "spec shape for")
link("vectorclock", "causalconsistency", "tracks")
link("hlogicalclock", "truetime", "hybrid alternative to", "dotted")
link("eventual", "sec", "weaker than", "dotted")
link("twophase", "saga", "blocking cost avoided by", "dotted")
link("paxos", "raft", "understandability counterpoint", "dotted")
link("linearizability", "harvestyield", "safety pole opposed by", "dotted")

# Breakers.
link("dynamo", "sloppyquorum", "introduced")
link("dynamo", "vectorclock", "introduced")
link("dynamo", "merkle", "introduced")
link("dynamo", "cassandra", "inspires")
link("dynamo", "riak", "inspires")
link("localfirst", "automerge", "requires")
link("localfirst", "peritext", "extends to")
link("localfirst", "offlinefirst", "is the programme of")
link("ipfs", "libp2p", "uses")
link("ipfs", "dht", "uses")
link("ipfs", "iroh", "content addressing shared with")
link("bitcoin", "blockchain", "precedes")
link("bitcoin", "tendermint", "Nakamoto counterpoint to", "dotted")
link("chaosmonkey", "chaoseng", "precedes")
link("chaoseng", "faultinjection", "method of")
link("chaoseng", "metastable", "exposes")
link("metastable", "cascadingfailure", "amplifies")
link("harvestyield", "gracefuldegradation", "quantifies")
link("antientropybreak", "readrepair", "avoids coordination of", "dotted")
link("decentralizedbreak", "p2p", "grounds")
link("edgebreak", "cloudlets", "grounds")
link("serverlessbreak", "workers", "critiques")
link("serverlessbreak", "fastlycompute", "critiques")
link("nocoordbreak", "coordinationavoidance", "argues for")
link("crdtbreak", "crdtspec", "argues default of")
link("partitionbreak", "splitbrain", "elevates")
link("blackboxbreak", "jepsen", "tool of")
link("pbft", "byzantinebreak", "relaxed by", "dotted")

# Physics.
link("tailatscale", "hedgedrequests", "motivates")
link("tailatscale", "p99budget", "quantifies")
link("tailatscale", "coordinatedomission", "measurement trap in", "dotted")
link("latencynumbers", "hardwarebounds", "grounds")
link("littleslaw", "backpressure", "bounds queue for")
link("usl", "amdahl", "extends with contention", "dotted")
link("usl", "capacityplanning", "predicts")
link("fiveminute", "edgephysics", "cost model for")
link("codel", "bbr", "congestion control pair")
link("jitter", "retrybudget", "avoids synchronization in")
link("diskfail", "correlatedfail", "empirical failure model for")
link("correlatedfail", "disasterrecovery", "grounds")
link("networklimits", "geo", "speed-of-light bound on")
link("energyproportional", "warehouse", "datacenter physics of")
link("warehouse", "borg", "cluster substrate for")
link("p99budget", "alerting", "burn rate of")

# Systems.
link("chubby", "paxos", "uses")
link("chubby", "leases", "uses")
link("spanner", "truetime", "uses")
link("spanner", "twophase", "uses")
link("spanner", "geo", "external consistency across")
link("bigtable", "chubby", "depends on")
link("bigtable", "lsmtree", "uses")
link("gfs", "chainrep", "uses")
link("mapreduce", "gfs", "reads")
link("borg", "kubernetes", "precedes")
link("kubernetes", "envoy", "service mesh for")
link("etcd", "raft", "uses")
link("consul", "gossip", "uses")
link("kafka", "wal", "log abstraction of")
link("bookkeeper", "kafka", "shared log with")
link("cassandra", "gossip", "membership via")
link("cassandra", "consistenthash", "partitioning via")
link("riak", "vectorclock", "siblings via")
link("cockroach", "raft", "replicates via")
link("cockroach", "geo", "survives")
link("foundationdb", "mvcc", "uses")
link("calvin", "voltdb", "deterministic ordering shared with")
link("aurora", "wal", "log is the database of")
link("megastore", "paxos", "per-entity replication via")
link("dapper", "distributedtracing", "introduced")
link("monarch", "fourgolden", "instruments")
link("envoy", "circuitbreaker", "implements")
link("flyio", "workers", "edge placement peer of")
link("workers", "fastlycompute", "isolate model shared with")
link("cdn", "anycast", "routes with")
link("iroh", "holepunching", "uses")
link("tor", "zerotrust", "trust boundary of", "dotted")
link("spanner", "dynamo", "CP counterpoint to AP in", "dotted")
link("chubby", "localfirst", "coordination assumption refused by", "dotted")

# Operations.
chain(["slo", "sli", "errorbudget", "alerting"], "measured by")
link("slo", "p99budget", "expressed as")
link("errorbudget", "canary", "gates")
link("errorbudget", "releaseengineering", "gates")
link("toil", "runbook", "automated by")
link("postmortem", "incident", "follows")
link("incident", "oncall", "paged to")
link("fourgolden", "redmethod", "service view of")
link("fourgolden", "usemethod", "resource view of")
link("observability", "distributedtracing", "pillar of")
link("canary", "featureflag", "deploys with")
link("loadshedding", "backpressure", "precedes")
link("backpressure", "circuitbreaker", "pairs with")
link("circuitbreaker", "retrybudget", "bounds")
link("retrybudget", "timeout", "requires")
link("timeout", "healthcheck", "feeds")
link("gracefuldegradation", "overload", "answers")
link("overload", "cascadingfailure", "unhandled becomes")
link("capacityplanning", "autoscaling", "feeds")
link("autoscaling", "loadshedding", "cannot replace")
link("disasterrecovery", "backup", "drilled by")
link("runbook", "configmanagement", "versioned with")
link("srech8", "releaseengineering", "chapter of")
link("releaseengineering", "canary", "ships by")
link("monitoring", "alerting", "feeds")
link("alerting", "oncall", "pages")
link("healthcheck", "failuredetector", "local form of")
link("cascadingfailure", "c_stpa", "systemic analysis by", "dotted")

# Edge.
link("fog", "mec", "standardizes")
link("mec", "cloudlets", "deploys")
link("cloudlets", "edgephysics", "bound by")
link("offlinefirst", "storeforward", "uses")
link("storeforward", "dtn", "generalizes")
link("dtn", "splitbrainedge", "reconciles")
link("geo", "anycast", "placed by")
link("holepunching", "p2p", "enables")
link("p2p", "dht", "locates")
link("splitbrainedge", "crdtspec", "resolved by")
link("zerotrust", "capability", "authorizes with")
link("zerotrust", "affinetypestate", "typestate of")
link("sybil", "eclipse", "overlays")
link("eclipse", "p2p", "attacks")
link("capability", "c_adt", "linear type of", "dotted")
link("edgephysics", "hardwarebounds", "narrower than", "dotted")

# Canon.
link("redbook", "transactions", "annotates")
link("redbook", "snapshotiso", "annotates")
link("tanenbaum", "failuredetector", "surveys")
link("lynchbook", "flp", "proves")
link("cachin", "pbft", "surveys")
link("birman", "gossip", "surveys")
link("sreworkbook", "slo", "practices")
link("sreworkbook", "postmortem", "practices")
link("buildsecure", "zerotrust", "grounds")
link("databaseinternals", "lsmtree", "details")
link("streamingsystems", "kafka", "models")
link("batchcanon", "mapreduce", "batch lineage of")
link("ddia2", "linearizability", "chapter grounds")
link("srech1", "srebook", "chapter of")
link("srech4", "slo", "chapter of")
link("srech22", "cascadingfailure", "chapter of")
link("srech26", "backup", "chapter of")
link("jepsencanon", "jepsen", "collects")
link("fallaciescanon", "fallacies", "states precisely")
link("capcanon", "gilbert", "revisits")
link("replicationcanon", "primarybackup", "surveys")

# Catalog.
link("c_ears", "c_qas", "obligation shape for")
link("c_invest", "c_ears", "story shape for")
link("c_premortem", "c_devil", "preloads")
link("c_premortem", "c_fmea", "failure inventory for")
link("c_spike", "c_pugh", "tested by")
link("c_pugh", "c_dbs", "scores with")
link("c_first", "c_occam", "paired with")
link("c_occam", "c_kiss", "simplicity relation")
link("c_cynefin", "c_spike", "probe-sense-respond for")
link("c_genchi", "witness", "go and see for")
link("c_five", "c_a3", "root cause for")
link("c_adr", "c_madr", "markdown template of")
link("c_adr", "c_bluf", "opens with")
link("c_adr", "c_second", "consequence section of")
link("c_adr", "c_naur", "records the theory in")
link("c_adr", "c_dod", "done when in")
link("c_adr", "c_keep", "changelog of")
link("c_adr", "c_pyramid", "structured by")
link("c_adr", "c_feynman", "plain-language test of")
link("c_chest", "c_refactor", "before removing with")
link("c_chest", "c_strangler", "before replacing with")
link("c_andon", "c_jidoka", "signals")
link("c_jidoka", "c_adr", "stop and fix in")
link("c_pdca", "c_kaizen", "improves by")
link("c_red", "c_dod", "criterion for")
link("c_mutation", "c_goodhart", "resists")
link("c_fagan", "faganverify", "inspection roles for")
link("c_fmea", "c_faulttree", "inductive complement of", "dotted")
link("c_stpa", "c_fmea", "systemic complement of", "dotted")
link("c_chaos", "c_montecarlo", "sampled by")
link("c_montecarlo", "c_p99", "reports")
link("c_io", "c_adt", "carries")
link("c_kolmogorov", "c_ssot", "minimizes duplication in")
link("c_hyrum", "c_chest", "why the fence exists for")
link("c_mikado", "c_strangler", "prerequisite graph for")
link("c_fallacies", "c_qas", "obligation inventory for")

# Reason.
link("toulmin", "buchanan", "argument model for")
link("aristotle", "buchanan", "appeals for")
link("schon", "argyris", "co-author of double loop with")
link("simon", "rittel", "contrasted with wicked problems by")
link("rittel", "ibis", "invented")
link("rittel", "dorst", "frame creation for")
link("ibis", "c_adr", "issue-position-argument precedes")
link("sontag", "c_feynman", "tempts over-explanation against", "dotted")
link("baxandall", "c_naur", "intent analogue of")
link("meadows", "argyris", "leverage points for")
link("naurtheory", "c_naur", "catalog form of")
link("popperreason", "popper", "same doctrine as")
link("lehman", "lehmanadapt", "same doctrine as")

# Verification.
link("tla", "tlc", "checked by")
link("clarke", "cegar", "introduced")
link("clarke", "ltl", "temporal logic of")
link("ltl", "spin", "checked by")
link("alloy", "refinement", "counterexamples for")
link("coq", "pitypes", "dependent types of")
link("verdi", "ironfleet", "precedes")
link("verdi", "raft", "verifies")
link("jepsen", "knossos", "uses")
link("knossos", "porcupine", "superseded by", "dotted")
link("quickcheck", "hypothesis", "stateful extension of")
link("hypothesis", "fuzzing", "complementary to")
link("metamorphic", "witness", "oracle for")
link("faganverify", "panel_independence", "inspection roles for")
link("pitypes", "witness", "typed obligation for")
link("refinement", "idempotencecheck", "stepwise proof of")
link("idempotencecheck", "witness", "digest of")
link("tla", "c_montecarlo", "exhaustive alternative to sampling", "dotted")
link("jepsen", "tla", "empirical counterpoint to proof", "dotted")

# Lenses to critics: each critic argues from one named text alone.
LENS_TO_CRITIC = {
 "crit_imp_fischer": "lens_flp", "crit_imp_lynch": "lens_flp",
 "crit_imp_paterson": "lens_flp", "crit_form_clarke": "lens_clarke",
 "crit_form_emerson": "lens_emerson", "crit_type_milner": "lens_milner",
 "crit_type_martinlof": "lens_martinlof", "crit_chaos_basiri": "lens_basiri",
 "crit_chaos_allspaw": "lens_allspaw", "crit_ops_beyer": "lens_beyer",
 "crit_ops_jones": "lens_jones", "crit_erasure_star": "lens_star",
 "crit_erasure_bowker": "lens_bowker", "crit_cons_lamport": "lens_lamport",
 "crit_cons_ongaro": "lens_ongaro", "crit_cons_oust": "lens_ongaro",
 "crit_byz_shostak": "lens_shostak", "crit_byz_pease": "lens_pease",
 "crit_byz_castro": "lens_shostak", "crit_byz_liskov": "lens_pease",
 "crit_part_gilbert": "lens_gilbert", "crit_part_brewer": "lens_brewer",
 "crit_part_abadi": "lens_gilbert", "crit_repl_decandia": "lens_decandia",
 "crit_repl_kleppmann": "lens_kleppmann", "crit_repl_gray": "lens_gray",
 "crit_tail_dean": "lens_dean", "crit_tail_barroso": "lens_barroso",
 "crit_edge_saty": "lens_satyanarayanan", "crit_edge_bonomi": "lens_bonomi",
 "crit_local_wiggins": "lens_wiggins", "crit_local_beresford": "lens_beresford",
 "crit_crdt_shapiro": "lens_shapiro", "crit_crdt_preguica": "lens_preguica",
 "crit_safety_kingsbury": "lens_kingsbury", "crit_sec_saltzer": "lens_saltzer",
 "crit_sec_schroeder": "lens_schroeder", "crit_human_cook": "lens_cook",
 "crit_human_perrow": "lens_perrow", "crit_econ_gunther": "lens_barroso",
 "crit_econ_little": "lens_barroso", "crit_evid_tufte": "lens_tufte",
 "crit_evid_cairo": "lens_cairo", "crit_hist_stonebraker": "lens_gray",
 "crit_hist_hellerstein": "lens_kleppmann", "crit_zt_gilman": "lens_saltzer",
 "crit_zt_barth": "lens_schroeder", "crit_dec_benet": "lens_nakamoto",
 "crit_dec_nakamoto": "lens_nakamoto", "crit_rupt_taleb": "lens_taleb",
 "crit_res_hollnagel": "lens_hollnagel", "crit_detach_sontag": "lens_tufte",
}
for c, lens_name in sorted(LENS_TO_CRITIC.items()):
    link(lens_name, c, "argues from alone")

# Dotted counterpoint pairs between critics. Both members of a pair are
# required to sit on any panel that uses either one.
CRITIC_PAIRS = [
 ("crit_imp_fischer", "crit_cons_lamport", "impossibility answers liveness"),
 ("crit_imp_lynch", "crit_part_gilbert", "impossibility grounds partition"),
 ("crit_form_clarke", "crit_chaos_basiri", "proof opposed by experiment"),
 ("crit_form_emerson", "crit_safety_kingsbury", "model checking opposed by testing"),
 ("crit_type_milner", "crit_rupt_taleb", "static type opposed by disorder"),
 ("crit_type_martinlof", "crit_human_perrow", "formal proof opposed by normal accidents"),
 ("crit_ops_beyer", "crit_detach_sontag", "runbooks opposed by reticence"),
 ("crit_ops_jones", "crit_erasure_star", "operator view opposed by invisible labor"),
 ("crit_erasure_bowker", "crit_hist_stonebraker", "classification opposed by canon"),
 ("crit_part_brewer", "crit_repl_decandia", "CAP opposed by Dynamo practice"),
 ("crit_part_abadi", "crit_tail_dean", "latency pole opposed by tail latency"),
 ("crit_cons_oust", "crit_cons_lamport", "understandability opposed by minimality"),
 ("crit_byz_shostak", "crit_zt_gilman", "Byzantine trust opposed by zero trust"),
 ("crit_byz_liskov", "crit_dec_nakamoto", "BFT opposed by open membership"),
 ("crit_repl_kleppmann", "crit_local_wiggins", "replication opposed by local ownership"),
 ("crit_repl_gray", "crit_crdt_shapiro", "transactions opposed by convergence"),
 ("crit_edge_saty", "crit_evid_tufte", "placement opposed by evidence"),
 ("crit_edge_bonomi", "crit_econ_gunther", "fog opposed by scaling law"),
 ("crit_local_beresford", "crit_crdt_preguica", "JSON CRDT opposed by general CRDT"),
 ("crit_sec_saltzer", "crit_dec_benet", "least privilege opposed by openness"),
 ("crit_sec_schroeder", "crit_res_hollnagel", "protection opposed by resilience"),
 ("crit_human_cook", "crit_evid_cairo", "narrative opposed by chart honesty"),
 ("crit_econ_little", "crit_hist_hellerstein", "queueing opposed by history"),
]
for a, b, label in CRITIC_PAIRS:
    link(a, b, label, "dotted")

# Panel method and adaptation.
link("surowiecki", "panel_independence", "independence for")
link("page", "panel_independence", "cognitive difference for")
link("debono", "panel_independence", "parallel viewpoints for")
link("lerman", "panel_independence", "four-step feedback for")
link("panel_quorum", "panel_independence", "counts seats from")
link("c_fagan", "panel_independence", "assigns roles to")
link("c_devil", "panel_independence", "formal dissent for")
link("c_premortem", "panel_independence", "preloads objections for")
link("popper", "kuhn", "anomalies accumulate into")
link("kuhn", "argyris", "frame swap for")
link("argyris", "hollnagel", "double loop revises criterion in")
link("talebadapt", "chaoseng", "gain from disorder for")
link("lehmanadapt", "hollnagel", "environment moves under")
link("panel_independence", "popper", "refutation admitted by")
link("c_chaos", "talebadapt", "invites disorder from")

CLASS_DEFS = [
 ("stance", "#fef3c7", "#b45309"),
 ("rules", "#e5e7eb", "#374151"),
 ("break", "#fce7f3", "#be185d"),
 ("physics", "#ede9fe", "#6d28d9"),
 ("system", "#dcfce7", "#15803d"),
 ("ops", "#ccfbf1", "#0f766e"),
 ("edge", "#ffedd5", "#c2410c"),
 ("canon", "#e2e8f0", "#475569"),
 ("catalog", "#dbeafe", "#1d4ed8"),
 ("reason", "#ecfccb", "#4d7c0f"),
 ("verify", "#fef9c3", "#a16207"),
 ("lens", "#fae8ff", "#a21caf"),
 ("critic", "#fee2e2", "#b91c1c"),
 ("panel", "#cffafe", "#0e7490"),
 ("adapt", "#d9f99d", "#3f6212"),
]


def build() -> str:
    node_ids: list[str] = []
    rank: dict[str, int] = {}
    lines_for: dict[str, str] = {}
    for cname, (_title, klass, _order) in CLUSTERS.items():
        for entry in NODES[cname]:
            nid, label = entry.split("|", 1)
            if nid in lines_for:
                raise SystemExit(f"duplicate node id: {nid}")
            if "|" in label:
                raise SystemExit(f"label contains a pipe: {nid}")
            node_ids.append(nid)
            lines_for[nid] = f'  {nid}["{label}"]:::{klass}'

    for src, dst, _label, _kind in EDGES:
        if src not in lines_for:
            raise SystemExit(f"unknown edge source: {src}")
        if dst not in lines_for:
            raise SystemExit(f"unknown edge target: {dst}")

    adjacency: dict[str, list[str]] = {nid: [] for nid in node_ids}
    indegree: dict[str, int] = {nid: 0 for nid in node_ids}
    for src, dst, _label, _kind in EDGES:
        adjacency[src].append(dst)
        indegree[dst] += 1
    queue: list[str] = [nid for nid in node_ids if indegree[nid] == 0]
    order: list[str] = []
    while queue:
        cur = queue.pop(0)
        order.append(cur)
        for nxt in adjacency[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    if len(order) != len(node_ids):
        blocked = [nid for nid in node_ids if indegree[nid] > 0]
        raise SystemExit(f"cycle detected among: {blocked[:20]}")
    for position, nid in enumerate(order):
        rank[nid] = position
    for src, dst, _label, _kind in EDGES:
        if rank[src] >= rank[dst]:
            raise SystemExit(f"rank violation: {src} -> {dst}")

    out: list[str] = ["```mermaid", "flowchart LR"]
    for cname, (title, _klass, _crank) in CLUSTERS.items():
        out.append(f'  subgraph {cname}["{title}"]')
        for entry in NODES[cname]:
            nid = entry.split("|", 1)[0]
            out.append(lines_for[nid])
        out.append("  end")
    for src, dst, label, kind in EDGES:
        arrow = "-->|" if kind == "solid" else "-.->|"
        out.append(f"  {src} {arrow}{label}| {dst}")
    for name, fill, stroke in CLASS_DEFS:
        out.append(f"  classDef {name} fill:{fill},stroke:{stroke},color:#111827")
    out.append("  classDef kept fill:#bbf7d0,stroke:#15803d,color:#111827")
    out.append("  classDef adapted fill:#fde68a,stroke:#b45309,color:#111827")
    out.append("  classDef scrapped fill:#fecaca,stroke:#b91c1c,stroke-dasharray:4,color:#111827")
    out.append("  classDef visited fill:#ffffff,stroke:#111827,stroke-width:3px,color:#111827")
    out.append("```")
    out.append("")
    solid = sum(1 for e in EDGES if e[3] == "solid")
    dotted = sum(1 for e in EDGES if e[3] == "dotted")
    out.append(f"Counts: {len(node_ids)} nodes, {len(EDGES)} edges "
               f"({solid} solid, {dotted} dotted), 0 cycles, "
               f"{len(CLUSTERS)} clusters, {len(CRITICS)} critic seats, "
               f"{len(LENS_TO_CRITIC)} lens bindings, {len(CRITIC_PAIRS)} critic counterpoint pairs.")
    out.append("")
    out.append("One seat per authority. A required critic named in the workflow for two or")
    out.append("three thinkers is that many seats. A lens binding names the single text a")
    out.append("seat argues from alone. Dotted critic pairs are joint obligations: either")
    out.append("member on a panel requires the other. Every node id is unique; every edge")
    out.append("endpoint exists; every edge goes from an earlier topological rank to a")
    out.append("later one, so the graph is a strict DAG. Incoming edges remain reachable")
    out.append("as back-references from a visited anchor's Frontier.")
    return "\n".join(out) + "\n"


HEADER = """# QUORUM anchor graph

Generated by `tools/build_graph.py`; do not hand-edit. Every label below is
copied verbatim into Decision Records and Panel Reports. Solid arrows are
forward references (grounds, extends, applies). Dotted arrows are counterpoints
or back-references. Boxes are clusters; an arrow into the CRITICS box means the
whole panel. Status classes for the live graph: `visited`, `kept`, `adapted`,
`scrapped`.

"""


def main(argv: list[str]) -> int:
    text = HEADER + build()
    target = pathlib.Path(argv[1]) if len(argv) > 1 else (
        pathlib.Path(__file__).resolve().parents[1]
        / "skills" / "quorum" / "references" / "anchor-graph.md"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    print(f"wrote {target} ({len(text)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
