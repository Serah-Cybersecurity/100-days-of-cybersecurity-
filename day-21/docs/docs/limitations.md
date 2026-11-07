# Technical Note: Project Limitations, Scope Boundaries & Architectural Trade-Offs

**Author:** Serah Mulwa

**Module:** Day 21 - SIEM Architecture, Log Ingestion & Security Data Engineering

## 1. Executive Summary & Engineering Honesty

In technical interviews and portfolio evaluations at Big Tech companies (such as Microsoft, Google, AWS, and Datadog), senior engineers and hiring managers immediately spot candidates who exaggerate their projects. Claiming that a local Python script is an "enterprise-grade SIEM" instantly signals a lack of real-world production experience.

A technically honest project is always stronger than an exaggerated one. It proves that the engineer understands not only *how* to build a functional prototype, but also *where* its boundaries lie, what architectural trade-offs were made, and how the system would need to be redesigned to scale to 50,000 corporate endpoints.

This document serves as an open, rigorous accounting of the current limitations, architectural constraints, and future evolution paths of my Mini-SIEM ingestion pipeline (`src/ingest.py`).

---

## 2. Documented Project Limitations & Scope Boundaries

### 1. Synthetic Data Source
* **Limitation:** The log files processed by this pipeline (`windows.jsonl`, `linux.jsonl`, `firewall.jsonl`, `suricata.jsonl`) are entirely synthetic and generated locally for lab testing.
* **Impact & Reality:** While they contain realistic forensic structures and injected faults (malformed JSON, invalid IPs, out-of-range ports), they do not replicate the sheer velocity, noise, network jitter, or protocol edge cases of live enterprise endpoints.

### 2. Learning Prototype Architecture
* **Limitation:** The entire pipeline is implemented as a monolithic Python batch-processing script running locally on a single machine.
* **Impact & Reality:** It is designed strictly as an educational learning prototype to master the mechanics of stream processing, parsing, validation, and normalisation. It is not a production-grade SIEM platform.

### 3. Lack of Distributed Ingestion
* **Limitation:** The ingestion script reads files locally from the filesystem rather than ingesting live telemetry across a distributed network.
* **Impact & Reality:** Production SIEM architectures rely on distributed message brokers (such as Apache Kafka, RabbitMQ, or Logstash buffers) to handle high-throughput, concurrent log forwarding from thousands of remote agents securely over TLS.

### 4. Absence of Enterprise-Grade Authentication & Access Control
* **Limitation:** The pipeline does not implement authentication, mutual TLS (mTLS) certificate verification, or Role-Based Access Control (RBAC).
* **Impact & Reality:** In a real deployment, agent-to-server communication requires strict cryptographic verification to prevent unauthorized log injection, spoofing, or Man-in-the-Middle (MitM) tampering.

### 5. Simplified Storage & Retention Management
* **Limitation:** Processed logs are written to flat JSONL files on a local disk directory (`data/processed/`), and quarantine records are dumped into a single text file (`data/quarantine/rejected.jsonl`).
* **Impact & Reality:** Production platforms use distributed NoSQL indexing clusters (like OpenSearch or Elasticsearch) with automated hot-to-cold index lifecycle management (ILM) policies, compression, and shard replication.

### 6. ECS-Inspired Normalisation (Not Full Compliance)
* **Limitation:** The normalisation engine (`src/normalizer.py`) maps disparate raw log keys into a simplified, custom subset inspired by the Elastic Common Schema (ECS).
* **Impact & Reality:** It is not fully compliant with the exhaustive official Elastic Common Schema specification, which includes hundreds of rigorous field definitions across diverse domains (network, file, process, url). It serves as a targeted subset optimized for our multi-source lab.

### 7. Deduplication Collisions & Edge Cases
* **Limitation:** Deduplication relies on in-memory content hashing of incoming log records within a batch execution.
* **Impact & Reality:** While effective for catching identical retransmissions, this simple hashing strategy may occasionally misclassify legitimate, rapid-fire repeated security events (e.g., two distinct users failing authentication at the exact same microsecond) as duplicates, leading to minor alert suppression.

---

## 3. Future Engineering Roadmap: Scaling to Enterprise Production

If tasked with scaling this Mini-SIEM architecture into a production-grade enterprise platform for global deployment, I would implement the following architectural evolutions:

1. **Decouple Ingestion via Message Queues:** Replace local file loops with an Apache Kafka cluster to buffer incoming log streams and prevent backpressure failures.
2. **Deploy Distributed Parsing Workers:** Scale parsing and normalisation across stateless worker nodes (e.g., Logstash or custom Go microservices).
3. **Migrate to OpenSearch / Elasticsearch:** Replace flat JSONL storage with a distributed indexing cluster to enable lightning-fast sub-second forensic search queries across petabytes of data.
4. **Implement mTLS Security:** Secure all agent-to-server communications using mutual TLS certificates and API token authentication.

---

## 4. Conclusion

Acknowledging these limitations does not diminish the value of the project—it elevates it. It demonstrates that I understand the gap between a local software prototype and a resilient, distributed enterprise security infrastructure.
