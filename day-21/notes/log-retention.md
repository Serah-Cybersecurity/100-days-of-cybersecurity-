# Technical Note: Operational SIEM Data Management, Log Retention Strategies, Cryptographic Integrity & Pipeline Monitoring

**Author:** Serah Mulwa

**Module:** Day 21 - SIEM Architecture, Log Ingestion & Security Data Engineering

## 1. Executive Summary & Personal Reflections

Throughout my practical work on Day 21, I realized that building a functional Python log ingestion pipeline is only half the battle. In a production Security Operations Center (SOC), data management introduces massive operational challenges that test an engineer's understanding of scale, cost, and forensic integrity.

If an organization retains every raw log and packet capture forever on high-performance storage, infrastructure costs will bankrupt the security department. Conversely, if logs are deleted too early, an incident responder investigating a persistent threat will hit a dead end because the historical audit trail is gone. Furthermore, a SIEM is only as reliable as its data pipeline and the immutability of its evidence.

This technical note documents the complete operational data management policy I engineered for my Mini-SIEM project. It covers tiered storage retention matrices, cryptographic SHA-256 hashing for provenance verification, and automated pipeline health monitoring via structured JSON reporting.

---

## 2. Tiered Storage Architecture & Log Retention Strategy

To balance forensic investigative depth against enterprise infrastructure budgets, my Mini-SIEM retention policy utilizes a two-tier storage model combined with automated lifecycle rules:

1. **Hot Storage Tier (NVMe / High-Performance SSDs):**
   * **Purpose:** Optimized for active threat hunting, real-time alerting, and rapid full-text indexing queries.
   * **Duration:** Maintained for the initial 30 to 180 days depending on log category.

2. **Cold Storage Tier (Object Storage / AWS S3 / Compressed Archive):**
   * **Purpose:** Optimized for compliance audits, long-term trend analysis, and retrospective forensic investigations.
   * **Duration:** Maintained for 1 to 5 years.

### Hypothetical Retention Matrix for Mini-SIEM Telemetry:

| Log Category | Hot Storage Tier | Cold Storage Tier | Total Retention | Operational & Forensic Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Authentication Events** (Windows 4625/4624, Linux SSH) | 90 Days | 275 Days | 1 Year | Critical for tracking brute-force attacks, credential stuffing, and lateral movement across internal systems. |
| **Network Telemetry** (Zeek conn.log, Firewall JSONL) | 30 Days | 60 Days | 90 Days | Extremely high volume; older network connection metadata is rarely queried unless hunting a specific historical breach. |
| **Endpoint & IDS Alerts** (Suricata signatures) | 180 Days | 180 Days | 1 Year | Vital for tracking recurring malware campaigns and analyzing threat actor persistence over time. |
| **Administrative Activity** (`sudo`, Root Logins, Domain Admin actions) | 1 Year | 4 Years | 5 Years | High-risk privileged actions subject to strict compliance auditing (e.g., PCI-DSS, SOC 2). |

---

## 3. Cryptographic Log Integrity & Provenance Baselines

In a court of law or an internal corporate disciplinary hearing, log files act as digital evidence. If an attacker compromises a server and alters log files, investigations are severely compromised.

### SHA-256 Hashing Baseline:
To establish an immutable verification baseline for my project's raw ingestion files, I generated cryptographic SHA-256 hashes using the standard Linux utility (`sha256sum data/raw/*.jsonl`, as captured in `day21-15-cryptographic-log-integrity.png`):

```text
79b55085a25af6537c78c382fdf374a6c8633e4f1a5f17a951d947ab8e8d1acc  data/raw/firewall.jsonl
abad422cf2d5dc7113887bf7b0006d5ca1730061810a6e5a9b3bdafaa41e5add  data/raw/linux.jsonl
70a1c2ad77b4d0e98c00eac32ab56fae247b27db0f108908db4307dd59035b4c  data/raw/suricata.jsonl
2f77546ed5ae0a88bd361001bdacc65b2b090b4a5caf162be79ab9231bdbc8be  data/raw/windows.jsonl
```

* **Engineering Insight:** A cryptographic hash does *not* prove that a log was truthful when originally generated. If a malicious service writes a fake log entry, its hash will still be mathematically valid. What a hash *does* prove is **tamper-evidence**: it guarantees that the file has not been modified, truncated, or corrupted since the baseline hash was computed.

---

## 4. Pipeline Health Monitoring & Telemetry Tracking

A SIEM pipeline itself must be actively monitored. If a firewall rule blocks log forwarding or disk partitions fill up, a silent SIEM creates a dangerous false sense of security. 

To prevent this, my Mini-SIEM script (`src/ingest.py`) automatically generates structured health metrics saved to `reports/ingestion_report.json` (as verified in `day21-11-pipeline-execution-summary.png`):

* **`records_received`**: Total raw log lines ingested.
* **`records_processed`**: Successfully parsed JSON records.
* **`records_valid`**: Records passing IP and port bounds validations.
* **`records_rejected`**: Malformed or invalid records isolated into the quarantine Dead-Letter Queue (`data/quarantine/rejected.jsonl`).
* **`records_duplicated`**: Identical records caught by in-memory content hashing.
* **`records_written`**: Final clean events saved to storage.
* **`processing_duration_seconds`**: Batch execution timing.

---

## 5. Key Engineering Takeaways & Core Principles

1. **Storage costs dictate architecture:** Always balance forensic retention requirements against hardware and cloud storage budgets by implementing tiered storage.
2. **Hashes ensure provenance:** Use SHA-256 baselines to prove log immutability and detect unauthorized file tampering during forensic audits.
3. **Monitor your ingestion:** A silent SIEM is not a secure network; it is usually a broken pipeline. Always track your ingestion health metrics.
