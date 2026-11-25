# Technical Note: Splunk Architecture, Data Ingestion Mapping & Operational Foundations

**Author:** Serah Mulwa

**Module:** Day 22 - Splunk Fundamentals & Search Processing Language (SPL)

## 1. Executive Summary & Architectural Overview

Building directly upon the custom Python Mini-SIEM ingestion pipeline engineered on Day 21, Day 22 shifts focus from security data engineering to enterprise SIEM operations, threat hunting, and security analysis using **Splunk Enterprise**.

In enterprise Security Operations Centers (SOCs), ingestion pipelines parse and normalize raw security telemetry before forwarding it into indexing engines. Splunk acts as the primary analytical platform, converting massive volumes of machine-generated security telemetry into an inverted search index.

This technical document details the architectural configuration, data mapping strategies, sourcetype definitions, operational isolation standards, and local deployment audits used to ingest synthetic security events (`data/raw/` and `data/processed/`) into Splunk.

## 2. Telemetry Data Ingestion Map

To maintain strict data governance and forensic tracking, incoming log files are mapped into Splunk using controlled source identifiers, structural sourcetypes, and a dedicated storage index.

| Source File Path | Splunk Target Index | Assigned Sourcetype | Data Description & Telemetry Type |
| :--- | :--- | :--- | :--- |
| `data/raw/windows.jsonl` | `cybersecurity_lab` | `_json` | Raw Windows domain controller event logs (Event IDs 4624, 4625). |
| `data/raw/linux.jsonl` | `cybersecurity_lab` | `_json` | Raw Linux system and authentication logs (`sudo`, SSH sessions). |
| `data/raw/firewall.jsonl` | `cybersecurity_lab` | `_json` | Network perimeter firewall connection records (allows/blocks). |
| `data/raw/suricata.jsonl` | `cybersecurity_lab` | `_json` | Suricata Intrusion Detection System (IDS) alerts and payload metadata. |
| `data/processed/normalized_*.jsonl` | `cybersecurity_lab` | `_json` | Elastic Common Schema (ECS) normalized & enriched events from Day 21. |

## 3. Sourcetype Configuration & Parsing Strategy

### Why `_json` Sourcetype is Critical

In Splunk, the **sourcetype** dictates how the indexer breaks incoming raw data streams into discrete lines, extracts timestamps, and parses key-value attributes.

When ingesting JSON Lines (`.jsonl`) security telemetry, selecting `sourcetype=_json` provides three core technical advantages:

1. **Native Field Extraction at Index/Search Time:** Splunk automatically parses nested JSON attributes (e.g., `event.action`, `source.ip`, `user.name`) into queryable fields without requiring custom regular expression (`rex`) parsing.

2. **Prevention of Multi-line Log Corruption:** Unstructured ingestion can cause multi-line JSON structures to break across line boundaries, resulting in truncated records and syntax errors. Setting `_json` guarantees that each complete JSON object is preserved as a single, discrete Splunk event.

3. **Preservation of Data Types:** Numeric fields (such as port numbers `destination.port=80` or failed attempt counts) retain their integer context, enabling instant mathematical aggregations using SPL commands like `sum()`, `avg()`, and `stats`.

## 4. Index Isolation Strategy

All project telemetry is ingested into a custom, dedicated index named:
```
cybersecurity_lab
```

### Technical Justification for Index Isolation

1. **Prevention of Operational Log Pollution:** By default, Splunk writes its own system metrics and search diagnostics to internal indexes (`_internal`, `_audit`). Ingesting lab telemetry into default indexes (`main`) creates noise and complicates investigation queries.

2. **Access Control & RBAC Enforcement:** In enterprise environments, role-based access control (RBAC) restricts analyst access by index. Isolating security telemetry inside `cybersecurity_lab` mirrors production standards, ensuring sensitive audit streams are separated from general infrastructure logs.

3. **Optimized Search Performance:** Restricting base SPL queries to a specific index (`index=cybersecurity_lab`) drastically narrows the volume of raw data blocks the search head must read from disk, significantly improving query speed.

4. **Lifecycle & Retention Management:** Storing lab telemetry in a dedicated index allows custom data retention and storage quota policies without risking accidental deletion of enterprise operational data.

## 5. Technical Setup, Host Environment Audit & Installation Log

To ensure stability and resource efficiency, Splunk Enterprise was deployed natively on the Windows host machine rather than inside the Parrot OS virtual machine, preventing unnecessary hypervisor CPU and RAM contention.

### Host Environment Audit Records
* **System Specifications:** Windows Host, 8+ GB RAM allocated, multi-core CPU architecture.
* **Installation Path:** `C:\Program Files\Splunk`
* **Service Validation:** Splunkd Windows service running cleanly in the background, listening on default web interface port `8000` and management port `8089`.

## 6. Core Operational Principles & Analyst Insights

### A. Splunk is a Tool, Not an Analyst
Splunk indexes data at immense scale, but it lacks intrinsic security context. It does not automatically determine whether a series of failed logins represents a brute-force attack or a user who forgot their password. The security analyst must supply the domain knowledge, construct precise SPL queries, and interpret behavioral patterns within the operational environment.

### B. Distinguishing Source from Sourcetype
* **`source`:** Identifies the physical or logical origin point of the data stream (e.g., file path `/var/log/windows.jsonl` or network port `UDP:514`). It answers *where* the data came from.
* **`sourcetype`:** Defines the structural format and parsing rules of the data stream (e.g., `_json`, `cisco:asa`, `syslog`). It answers *how* the data should be processed.

### C. Garbage In, Garbage Out (GIGO)
Data analysis is only as reliable as the underlying data quality. If upstream parsing, validation, or normalisation on Day 21 was flawed, downstream Splunk queries will yield inaccurate or misleading security metrics. Security data engineering and threat hunting are fundamentally interdependent disciplines.

### D. Crucial Security & Operational Takeaways
1. **Local Security Boundaries:** This environment is a local sandbox. Management and search ports (`8000`, `8089`) must never be exposed to the public internet, and default credentials must be secured.
2. **Splunk Free License Behavior:** Transitioning from the 60-day Enterprise Trial to the perpetual Free license removes user authentication prompts, automatically granting full administrative privileges (`admin`) to anyone accessing `localhost:8000`.
3. **Hardware Realism:** Always match tool deployment strategies to available host system resources to maintain a stable, responsive learning environment.
