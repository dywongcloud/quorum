# QUORUM canon

Every label in `anchor-graph.md` is a real text, system, or result. This file
records its source, the cluster it occupies, and the authority under which the
graph reads it. `provenance` states where the label was checked. Local means the
full text was extracted from a downloaded copy and read during the build; an
SRE or DDIA chapter reference names the printed chapter. A URL names the
publisher's page or the authors' copy.

## Primary books (full text read during the build)

| Label | Source | Provenance |
|---|---|---|
| Site Reliability Engineering (Beyer, Jones, Petoff, Murphy) | https://sre.google/sre-book/table-of-contents/ | local: `Site Reliability Engineering.pdf`, chapters 1, 4, 5, 6, 8, 10, 15, 22, 26 read |
| Designing Data-Intensive Applications (Kleppmann) | https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/ | local: `Designing-Data-Intensive-Applications.pdf`, chapters 1-6, 8, 9, 10, 11 read |
| The Site Reliability Workbook (Beyer et al.) | https://sre.google/workbook/table-of-contents/ | publisher table of contents |
| Building Secure and Reliable Systems (Adkins et al.) | https://sre.google/static/pdf/building_secure_reliable_systems.pdf | publisher PDF |
| Release It! (Nygard) | https://pragprog.com/titles/mnee2/release-it-second-edition/ | publisher page; circuit breaker and bulkhead terminology |
| Readings in Database Systems (Stonebraker, Hellerstein) | https://www.redbook.io/ | authors' open edition |
| Distributed Systems (Tanenbaum, van Steen) | https://www.distributed-systems.net/ | authors' open edition |
| Distributed Algorithms (Lynch) | https://www.sciencedirect.com/book/9780123674900/distributed-algorithms | publisher record |
| Database Internals (Petrov) | https://www.databass.dev/ | author's page |
| Streaming Systems (Akidau et al.) | https://streamingbooks.net/ | authors' page |

## Impossibility, consistency, and consensus

| Label | Source | Cluster |
|---|---|---|
| Impossibility of Distributed Consensus with One Faulty Process (Fischer, Lynch, Paterson) | https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf | STANCE |
| Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services (Gilbert, Lynch) | https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL02-brewer-conjecture.pdf | STANCE |
| CAP Twelve Years Later (Brewer) | https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/ | STANCE |
| Consistency Tradeoffs in Modern Distributed Database System Design (Abadi) | https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf | STANCE |
| Harvest, Yield, and Scalable Tolerant Systems (Fox, Brewer) | https://radlab.cs.berkeley.edu/people/fox/static/papers/pdf/c18.pdf | STANCE |
| Consistency As Logical Monotonicity (Hellerstein, Alvaro) | https://www.cidrdb.org/cidr2011/Papers/CIDR11_Paper34.pdf | STANCE |
| Fallacies of Distributed Computing (Deutsch) | https://www.rgoarchitects.com/Files/fallacies.pdf | STANCE |
| End-to-End Arguments in System Design (Saltzer, Reed, Clark) | https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf | STANCE |
| Notes on Distributed Systems for Young Bloods (Hodges) | https://www.somethingsimilar.com/2013/01/14/notes-on-distributed-systems-for-young-bloods/ | STANCE |
| Time, Clocks, and the Ordering of Events (Lamport) | https://lamport.azurewebsites.net/pubs/time-clocks.pdf | STANCE |
| The Byzantine Generals Problem (Lamport, Shostak, Pease) | https://lamport.azurewebsites.net/pubs/byz.pdf | STANCE |
| The Part-Time Parliament (Lamport) | https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf | RULES |
| Paxos Made Simple (Lamport) | https://lamport.azurewebsites.net/pubs/paxos-simple.pdf | RULES |
| In Search of an Understandable Consensus Algorithm (Ongaro, Ousterhout) | https://raft.github.io/raft.pdf | RULES |
| Practical Byzantine Fault Tolerance (Castro, Liskov) | https://pmg.csail.mit.edu/papers/osdi99.pdf | RULES |
| Viewstamped Replication (Oki, Liskov) | https://pmg.csail.mit.edu/papers/vr.pdf | RULES |
| Zab: High-performance broadcast (Junqueira, Reed, Serafini) | https://marcoserafini.github.io/papers/zab.pdf | RULES |
| Unreliable Failure Detectors (Chandra, Toueg) | https://www.cs.cornell.edu/home/sam/FDpapers/jacm96.pdf | RULES |
| Linearizability (Herlihy, Wing) | https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf | RULES |
| A Critique of ANSI SQL Isolation Levels (Berenson et al.) | https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf | RULES |
| A Comprehensive Study of CRDTs (Shapiro et al.) | https://inria.hal.science/inria-00609399/document | RULES |
| Coordination Avoidance in Database Systems (Bailis et al.) | https://www.vldb.org/pvldb/vol8/p185-bailis.pdf | RULES |
| Highly Available Transactions (Bailis et al.) | https://www.vldb.org/pvldb/vol7/p181-bailis.pdf | RULES |
| The Transaction Concept (Gray) | https://www.hpl.hp.com/techreports/tandem/TR-81.3.pdf | RULES |
| Notes on Data Base Operating Systems (Gray) | https://www.hpl.hp.com/techreports/tandem/TR-81.2.pdf | RULES |
| SAGAS (Garcia-Molina, Salem) | https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf | RULES |
| Consistent Hashing and Random Trees (Karger et al.) | https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash99.pdf | RULES |
| Chord (Stoica et al.) | https://pdos.csail.mit.edu/papers/chord:sigcomm01.pdf | RULES |
| Kademlia (Maymounkov, Mazieres) | https://www.cs.rice.edu/Connexions/projects/IPv6/pdf/Kademlia.pdf | RULES |
| SWIM (Das et al.) | https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf | RULES |
| Epidemic Algorithms (Demers et al.) | https://www.cs.cornell.edu/home/rvr/papers/flowgossip.pdf | RULES |
| The Log-Structured Merge-Tree (O'Neil et al.) | https://www.cs.umb.edu/~poneil/LSM-Tree.pdf | RULES |
| Space/Time Trade-offs in Hash Coding (Bloom) | https://dl.acm.org/doi/10.1145/362686.362692 | RULES |
| TrueTime and external consistency (Corbett et al.) | https://research.google/pubs/spanner-googles-globally-distributed-database/ | RULES |
| Chain Replication (van Renesse, Schneider) | https://www.cs.cornell.edu/home/rvr/papers/OSDI04.pdf | RULES |

## Systems at scale

| Label | Source | Cluster |
|---|---|---|
| Dynamo (DeCandia et al.) | https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf | BREAK |
| The Chubby Lock Service (Burrows) | https://research.google/pubs/the-chubby-lock-service-for-loosely-coupled-distributed-systems/ | SYSTEMS |
| Bigtable (Chang et al.) | https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/ | SYSTEMS |
| The Google File System (Ghemawat et al.) | https://research.google/pubs/the-google-file-system/ | SYSTEMS |
| MapReduce (Dean, Ghemawat) | https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/ | SYSTEMS |
| Borg (Verma et al.) | https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/ | SYSTEMS |
| Borg, Omega, and Kubernetes (Burns et al.) | https://queue.acm.org/detail.cfm?id=2898444 | SYSTEMS |
| ZooKeeper (Hunt et al.) | https://www.usenix.org/conference/usenix-atc-10/zookeeper-wait-free-coordination-internet-scale-systems | SYSTEMS |
| Kafka (Kreps et al.) | https://notes.stephenholiday.com/Kafka.pdf | SYSTEMS |
| Cassandra (Lakshman, Malik) | https://www.cs.cornell.edu/projects/ladis2009/papers/lakshman-ladis2009.pdf | SYSTEMS |
| Megastore (Baker et al.) | https://research.google/pubs/megastore-providing-scalable-highly-available-storage-for-interactive-services/ | SYSTEMS |
| Dapper (Sigelman et al.) | https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/ | SYSTEMS |
| Monarch (Adams et al.) | https://www.vldb.org/pvldb/vol13/p3181-adams.pdf | SYSTEMS |
| Amazon Aurora (Verbitski et al.) | https://www.amazon.science/publications/amazon-aurora-design-considerations-for-high-throughput-cloud-native-relational-databases | SYSTEMS |
| Calvin (Thomson et al.) | https://cs.yale.edu/homes/thomson/publications/calvin-sigmod12.pdf | SYSTEMS |
| FoundationDB (Zhou et al.) | https://www.vldb.org/pvldb/vol14/p3213-zhou.pdf | SYSTEMS |
| IPFS (Benet) | https://ipfs.tech/ | BREAK |
| Bitcoin (Nakamoto) | https://bitcoin.org/bitcoin.pdf | BREAK |
| Local-First Software (Kleppmann et al.) | https://www.inkandswitch.com/local-first/ | BREAK |
| A Conflict-Free Replicated JSON Datatype (Kleppmann, Beresford) | https://arxiv.org/abs/1608.03960 | BREAK |
| Peritext (Litt et al.) | https://www.inkandswitch.com/peritext/ | BREAK |

## Physics, operations, edge, and verification

| Label | Source | Cluster |
|---|---|---|
| The Tail at Scale (Dean, Barroso) | https://cacm.acm.org/research/the-tail-at-scale/ | PHYSICS |
| Numbers Every Programmer Should Know (Dean) | https://colin-scott.github.io/personal_website/research/interactive_latency.html | PHYSICS |
| Universal Scalability Law (Gunther) | https://www.perfdynamics.com/Manifesto/USL.html | PHYSICS |
| Failure Trends in a Large Disk Drive Population (Pinheiro et al.) | https://research.google/pubs/failure-trends-in-a-large-disk-drive-population/ | PHYSICS |
| The Datacenter as a Computer (Barroso et al.) | https://research.google/pubs/the-datacenter-as-a-computer-an-introduction-to-the-design-of-warehouse-scale-machines/ | PHYSICS |
| Controlled Delay AQM (Nichols, Jacobson) | https://queue.acm.org/detail.cfm?id=2209336 | PHYSICS |
| BBR (Cardwell et al.) | https://queue.acm.org/detail.cfm?id=3022184 | PHYSICS |
| Eliminating Toil, SLOs, postmortems, cascading failures | Site Reliability Engineering, chapters 4, 5, 15, 22 | OPS |
| Addressing Cascading Failures (Beyer et al.) | https://sre.google/sre-book/addressing-cascading-failures/ | OPS |
| Metastable Failures (Bronson et al.) | https://www.usenix.org/conference/hotos21/presentation/bronson | BREAK |
| Chaos Engineering (Basiri et al.) | https://queue.acm.org/detail.cfm?id=3099565 | BREAK |
| Principles of Chaos Engineering | https://principlesofchaos.org/ | CATALOG |
| Timeouts, retries and jitter | https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ | OPS |
| Using load shedding to avoid overload | https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/ | OPS |
| The Emergence of Edge Computing (Satyanarayanan) | https://www.computer.org/csdl/magazine/ic/2017/01/mic2017010030/13rRUy9KxUY | BREAK |
| Fog Computing (Bonomi et al.) | https://dl.acm.org/doi/10.1145/2342509.2342513 | EDGE |
| Delay-Tolerant Networking (Fall) | https://dl.acm.org/doi/10.1145/863955.863960 | EDGE |
| The Sybil Attack (Douceur) | https://www.microsoft.com/en-us/research/publication/the-sybil-attack/ | EDGE |
| Zero Trust Networks (Gilman, Barth) | https://www.oreilly.com/library/view/zero-trust-networks/9781491962183/ | EDGE |
| Specifying Systems: TLA+ (Lamport) | https://lamport.azurewebsites.net/tla/book.html | VERIFY |
| Model Checking and Abstraction (Clarke et al.) | https://dl.acm.org/doi/10.1145/200836.200869 | VERIFY |
| The SPIN Model Checker (Holzmann) | https://spinroot.com/spin/whatispin.html | VERIFY |
| Verdi (Wilcox et al.) | https://verdi.uwplse.org/ | VERIFY |
| IronFleet (Hawblitzel et al.) | https://www.microsoft.com/en-us/research/publication/ironfleet-proving-practical-distributed-systems-correct/ | VERIFY |
| Jepsen analyses (Kingsbury) | https://jepsen.io/analyses | VERIFY |
| QuickCheck (Claessen, Hughes) | https://dl.acm.org/doi/10.1145/351240.351266 | VERIFY |
| How Complex Systems Fail (Cook) | https://howcomplexsystems.fail/ | STANCE |
| Normal Accidents (Perrow) | https://press.princeton.edu/books/paperback/9780691004125/normal-accidents | STANCE |
| The Ethnography of Infrastructure (Star) | https://dl.acm.org/doi/10.1145/353360.353367 | LENSES |
| Sorting Things Out (Bowker, Star) | https://mitpress.mit.edu/9780262522951/sorting-things-out/ | LENSES |

## Hardware bounds used in the Crucible move

| Quantity | Bound | Source |
|---|---|---|
| Same-datacenter round trip | about 0.5 ms | Numbers Every Programmer Should Know (Dean) |
| Cross-region round trip | tens of ms, speed-of-light bound | The Datacenter as a Computer (Barroso et al.) |
| p99 amplification with 100 fan-out leaves | 1 in 100 requests waits for the slowest leaf | The Tail at Scale (Dean, Barroso) |
| Disk annualized failure rate | single-digit percent, correlated within a batch | Failure Trends in a Large Disk Drive Population (Pinheiro et al.) |

No figure in `web/index.html` is printed without one of these sources or a
command that reproduces it. `scripts/validate_figures.py` re-measures all of
them at the final state.
