# Technical Note: Enterprise Log Retention Architecture, Tiered Storage & Automated Lifecycle Management

**Author:** Serah Kathini Mulwa

**Program:** Women Techsters Fellowship — Cybersecurity Track

**Module:** Day 21 — SIEM Architecture, Log Ingestion & Security Data Engineering

## 1. Executive Summary & Personal Reflections

During my engineering work on Day 21, I learned that building an ingestion pipeline and processing logs is only half the battle. In a production Security Operations Center (SOC), data management introduces massive operational challenges. If an organization retains every raw log and packet capture forever on high-performance storage, infrastructure costs will bankrupt the department. Conversely, if logs are deleted too early, an incident responder investigating a persistent threat will hit a dead end because the historical audit trail is gone.

This technical note documents the hypothetical log retention and lifecycle management policy I designed for my Mini-SIEM project. It outlines a tiered storage model balancing high-performance searchability against cost-efficient archiving, along with automated lifecycle rules to govern data purging and regulatory immutability.

## 2. Tiered Storage Architecture: Hot vs. Cold Storage

To optimize cost and performance, enterprise SIEM deployments do not store all logs on the same storage tier. I structured my Mini-SIEM retention policy around a two-tier storage model:

1. **Hot Storage (NVMe / High-Performance SSDs):**
   * **Purpose:** Designed for active threat hunting, real-time alerting, and immediate SOC triage.
   * **Characteristics:** High IOPS, low latency, and optimized for fast full-text indexing queries (e.g., searching recent authentication failures or Suricata intrusion alerts).
   * **Duration:** Maintained for the initial 30 to 90 days of event generation.

2. **Cold Storage (Object Storage / AWS S3 / Glacier Archive):**
   * **Purpose:** Designed for compliance audits, long-term trend analysis, and retrospective forensic investigations.
   * **Characteristics:** Highly compressed, inexpensive storage where data is retrieved asynchronously.
   * **Duration:** Maintained for 1 to 5 years depending on data category and regulatory mandates.

## 3. Hypothetical Log Retention Matrix

Different security telemetry sources carry varying forensic values and storage volumes. Below is the retention policy I established for my Mini-SIEM architecture:

| Log Category | Hot Storage Tier | Cold Storage Tier | Total Retention | Operational & Forensic Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Authentication Events** (Windows 4625/4624, Linux SSH) | 90 Days | 275 Days | 1 Year | Critical for tracking brute-force attacks, credential stuffing, and lateral movement across internal systems. |
| **Network Telemetry** (Zeek conn.log, Firewall JSONL) | 30 Days | 60 Days | 90 Days | Extremely high volume; older network connection metadata is rarely queried unless hunting a specific historical breach. |
| **Endpoint & IDS Alerts** (Suricata signatures) | 180 Days | 180 Days | 1 Year | Vital for tracking recurring malware campaigns and analyzing threat actor persistence over time. |
| **Administrative Activity** (`sudo`, Root Logins, Domain Admin actions) | 1 Year | 4 Years | 5 Years | High-risk privileged actions subject to strict compliance auditing (e.g., PCI-DSS, SOC 2). |

## 4. Automated Lifecycle Management & Immutability Rules

To prevent manual errors and enforce predictable storage scaling, a professional SIEM must automate data lifecycle transitions. For my Mini-SIEM project, I defined two core automation rules:

### Rule 1: Automated Purging of Unneeded Debug Logs
* **The Problem:** Verbose debug logs and low-severity informational messages consume valuable storage space without providing actionable security intelligence.
* **The Automation Policy:** Lifecycle scripts automatically sweep processed log directories after 14 days, purging non-security debug logs while retaining structured normalization records (`normalised_events.jsonl`) and quarantine dead-letter queues (`rejected.jsonl`) for pipeline auditing.

### Rule 2: Administrative Immutability & Retention Locking
* **The Problem:** Sophisticated attackers who compromise root administrative accounts often attempt to delete audit logs to hide their tracks.
* **The Automation Policy:** Administrative audit logs and authentication failure records are tagged with write-once-read-many (WORM) compliance locks. Automated deletion scripts are strictly prohibited from purging these logs prior to the expiration of their mandated retention window, even if requested by an administrator with standard privileges.

## 5. Summary & Engineering Takeaways

Designing a log retention policy requires balancing two competing priorities: **investigative depth** and **infrastructure budget**. 

By establishing a tiered storage model (Hot NVMe for rapid triage, Cold object storage for long-term compliance) and enforcing automated lifecycle rules, my Mini-SIEM architecture ensures that security analysts have instant access to recent threat data while maintaining fiscal responsibility and cryptographic integrity.
