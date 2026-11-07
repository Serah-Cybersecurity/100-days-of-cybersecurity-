# Technical Note: Enterprise SIEM Architecture, Data Ingestion & Security Data Engineering

**Author:** Serah Kathini Mulwa  
**Program:** Women Techsters Fellowship — Cybersecurity Track  
**Module:** Day 21 — SIEM Architecture, Log Ingestion & Security Data Engineering  

---

## 1. Executive Summary & Personal Reflections

A Security Information and Event Management (SIEM) platform is the central nervous system of any modern Security Operations Center (SOC). However, one of the most critical lessons I have learned transitioning into security data engineering is that **a SIEM is only as good as the telemetry pipeline feeding it**. 

If security data collected across heterogeneous network sensors, cloud audit logs, firewalls, and endpoints arrives at the SIEM malformed, unparsed, unnormalized, or with misaligned timestamps, downstream detection rules will fail silently. A missing log line or an unparsed IP address is not just a technical error—it is a blind spot that adversaries can exploit.

This document details my engineering analysis of the 12-stage enterprise SIEM data pipeline, breaks down key data transformation mechanics (parsing, normalisation, enrichment), outlines my pipeline resilience and quarantine strategies, and discusses the real-world operational considerations required for building high-scale security data lakes.

---

## 2. End-to-End 12-Stage SIEM Data Pipeline Architecture

In enterprise security, data does not simply jump from an endpoint into an analyst's dashboard. It travels through twelve distinct stages. Understanding this complete end-to-end flow allows me to pinpoint exactly where pipeline failures occur when debugging ingestion issues.

```
[ 1. SECURITY DATA SOURCES ]
            │
            ▼
[ 2. DATA COLLECTION ]
            │
            ▼
[ 3. DATA TRANSPORT ]
            │
            ▼
[ 4. PARSING & EXTRACTION ]
            │
            ▼
[ 5. NORMALISATION (ECS) ]
            │
            ▼
[ 6. ENRICHMENT ]
            │
            ▼
[ 7. INDEXING & STORAGE ]
            │
            ▼
[ 8. SEARCH & CORRELATION ]
            │
            ▼
[ 9. DETECTION RULES ]
            │
            ▼
[ 10. ALERT GENERATION ]
            │
            ▼
[ 11. SOC ANALYST INVESTIGATION ]
            │
            ▼
[ 12. DOCUMENTATION & RESPONSE ]
```

### Stage-by-Stage Engineering Breakdown:

1. **Security Data Sources:** Telemetry originates at the edge—operating systems (Windows EVTX, Linux Syslog), cloud audit trails (AWS CloudTrail, Azure Activity Logs), firewalls, and network security monitoring sensors (Suricata EVE JSON, Zeek metadata).
2. **Data Collection:** Lightweight endpoint agents (such as Elastic Agent or Splunk Universal Forwarder) or agentless listeners harvest raw log streams directly from the operating system or log directories.
3. **Data Transport:** Collected logs are pushed across the network via secure transport protocols (TLS-encrypted TCP, HTTPS, or message brokers like Apache Kafka) to ingestion buffer nodes.
4. **Parsing & Extraction:** Ingestion engines run pattern matching (e.g., regex, Grok filters) to transform raw, unstructured text strings into structured key-value pairs.
5. **Normalisation (ECS Mapping):** Vendor-specific field names (e.g., `src_ip`, `id.orig_h`, `SourceIpAddress`) are translated into a standardized, unified taxonomy—specifically an educational subset of the **Elastic Common Schema (ECS)**.
6. **Enrichment:** Parsed events are augmented with real-time operational context, such as Active Directory user details, internal asset ownership (e.g., `department: Finance`), GeoIP coordinates, or threat intelligence reputation scores.
7. **Indexing & Storage:** The clean, enriched records are indexed into high-performance database clusters (such as Elasticsearch or OpenSearch) optimized for sub-second search and structured retrieval.
8. **Search & Correlation:** Query engines run scheduled or ad-hoc searches across indexed fields to link events across different data sources within specified time windows.
9. **Detection Rules:** Structured logic (written in Sigma, KQL, or SPL) continuously evaluates normalized incoming data streams against known attacker techniques and anomalies.
10. **Alert Generation:** When rule conditions are satisfied, actionable alerts are generated and pushed into the incident queue with assigned severity levels.
11. **SOC Analyst Investigation:** Security analysts Triage the alert, correlate supporting telemetry using unique identifiers (like Community ID or Zeek UIDs), and establish whether the event represents a true positive incident.
12. **Documentation & Response:** Responders document their findings, execute remediation steps (such as host isolation or credential revoking), and update rule definitions to prevent future false positives.

---

## 3. Core Technical Distinctions: Parsing vs. Normalisation vs. Enrichment

One of the common points of confusion for junior analysts is mixing up **parsing**, **normalisation**, and **enrichment**. In my engineering work, I treat them as three completely separate transformation layers:

* **Parsing (Structural Extraction):** Reads an unformatted log string and extracts fields into a structured JSON object, preserving whatever raw key names the vendor chose.
  * *Raw String Input:* `2026-11-07 14:30:00 FAILED_LOGIN user=serah src=192.168.1.50`
  * *Parsed Output:* `{"user": "serah", "src": "192.168.1.50"}`
* **Normalisation (Taxonomy Standardization):** Takes those extracted vendor keys and maps them into a consistent enterprise schema (Elastic Common Schema). This ensures that a source IP is *always* labeled `source.ip`, regardless of which tool generated it.
  * *Parsed Input:* `{"user": "serah", "src": "192.168.1.50"}`
  * *Normalized ECS Output:* `{"user.name": "serah", "source.ip": "192.168.1.50"}`
* **Enrichment (Contextual Augmentation):** Adds critical business context to the normalized record before indexing so analysts don't have to look it up manually during triage.
  * *Normalized Output:* `{"source.ip": "192.168.1.50"}`
  * *Enriched Output:* `{"source.ip": "192.168.1.50", "asset.hostname": "workstation-dev-01", "asset.owner": "Serah Kathini", "network.zone": "Internal Corporate"}`

---

## 4. Pipeline Resilience, Validation & Quarantine Strategies

Building an ingestion pipeline requires designing for failure. Vendors frequently change log formats without notice, networks drop packets, and corrupt data enters the stream. If a pipeline crashes every time it sees a malformed line, security operations halt.

In my Python implementation (`scripts/siem_pipeline.py`), I built a robust multi-stage data validation and quarantine architecture:

```
Raw Telemetry Input
        │
        ▼
[ Syntax Validation (JSON Parsing) ] ── (Fail) ──► [ Quarantine Queue (DLQ) ]
        │ (Pass)
        ▼
[ Schema Validation (Mandatory Fields) ] ── (Fail) ──► [ Quarantine Queue (DLQ) ]
        │ (Pass)
        ▼
[ Deduplication Check (Record Hash) ] ── (Duplicate) ──► [ Drop / Metrics Log ]
        │ (Unique)
        ▼
[ ECS Normalisation Mapping ]
        │
        ▼
Indexed Production Output (`normalized_events.jsonl`)
```

### Key Safety Protocols Implemented:

1. **Syntax Validation & Dead-Letter Queuing (DLQ):** If a record fails JSON parsing due to syntax corruption or truncation, the pipeline catches the exception, attaches a failure reason and timestamp, and routes the raw text to a quarantine file (`quarantine_malformed.jsonl`). This isolates the bad record without stopping the pipeline.
2. **Schema Validation:** Records that pass syntax checks must still contain baseline telemetry anchors (such as a valid timestamp or source identifier). Unanchored events are diverted to quarantine to prevent silent indexing bugs downstream.
3. **Deduplication:** Hash checking prevents duplicate events (caused by network retransmissions or agent forwarder loops) from inflating storage costs and skewing detection metrics.
4. **Data Quality Reporting:** The pipeline outputs automated metrics (`output/ingestion-metrics.json`) detailing total lines processed, valid events normalized, malformed records isolated, and overall ingestion success rates.

---

## 5. Production & Operational Engineering Considerations

When scaling ingestion architecture to handle high-volume enterprise or cloud environments, several critical design principles must be enforced:

* **Addressing Schema Drift:** Vendors regularly modify their software updates, changing field names or adding nested objects. Ingestion pipelines must be built with strict exception handling and automated alerting on dead-letter queue spike rates so engineers are alerted to schema drift immediately.
* **Preserving Raw Telemetry Lineage:** Normalization should never discard original events. I ensure the raw unparsed record is stored within a `raw_reference` field inside the normalized event. This preserves evidentiary integrity for forensic deep-dives and legal compliance.
* **Garbage In, Garbage Out:** Detection rules rely entirely on upstream data quality. If an ingestion parser misinterprets a time zone (e.g., confusing UTC with local time), correlation windows will misalign, causing high-priority security alerts to fail silently.

---

## 6. Summary Checklist for Portfolio Verification

| Engineering Stage | Implementation Artifact | Defensive Function |
| :--- | :--- | :--- |
| **Data Ingestion** | `input/sample_security_logs.jsonl` | Multi-source raw telemetry input (Suricata, Zeek, Windows simulation). |
| **Pipeline Engine** | `scripts/siem_pipeline.py` | Python script for parsing, schema validation, quarantine handling, and ECS normalization. |
| **Quarantine Isolation** | `output/quarantine_malformed.jsonl` | Dead-letter queue capturing corrupted or unanchored log lines. |
| **Normalized Output** | `output/normalized_events.jsonl` | Clean, ECS-mapped JSON lines ready for SIEM indexing. |
| **Pipeline Reporting** | `output/ingestion-metrics.json` | JSON report quantifying total lines, success rates, and error metrics. |
