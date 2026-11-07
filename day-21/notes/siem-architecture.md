# Technical Note: Enterprise SIEM Architecture, Ingestion Pipelines & Data Quality Engineering

**Author:** Serah Mulwa

**Module:** Day 21 - SIEM Architecture, Log Ingestion & Security Data Engineering

---

## 1. Executive Summary

A Security Information and Event Management (SIEM) platform is the centralized foundation of modern Security Operations Centers (SOCs). However, a SIEM is only as effective as the data ingestion pipelines feeding it. If security telemetry collected from heterogeneous sensors (such as Suricata IDS, Zeek NSM, Windows Event Logs, and Linux Syslog) is malformed, delayed, unparsed, or unnormalized, downstream detection rules fail silently.

This technical note documents the end-to-end architecture of enterprise SIEM telemetry pipelines, compares schema transformation strategies, and evaluates data quality metrics generated during the implementation of the Day 21 ingestion engine (`scripts/siem_pipeline.py`).

---

## 2. End-to-End SIEM Data Pipeline Architecture

Security data moves through seven distinct stages from initial log generation on an endpoint or network sensor to the final dashboard rendered for a SOC analyst:

```
[ Data Source ] ──> [ Forwarding Agent ] ──> [ Log Ingestion Node ]
                                                   │
                                                   ▼
[ Dashboard / Alerting ] <── [ Indexing & Storage ] <── [ Parsing & Normalisation ]
```

1. **Log Generation (Source):** Operating systems, cloud services, firewalls, and network sensors generate raw telemetry (e.g., Syslog RFC 5424, Windows EVTX, EVE JSON).
2. **Collection & Secure Transport:** Lightweight agents (Logstash, Fluentbit, Vector, Elastic Agent) collect logs from local disks or API endpoints and transport them securely over TLS to central ingestion buffers.
3. **Parsing & Syntax Validation:** Ingestion nodes break unformatted log streams into key-value pairs and validate structural integrity (JSON formatting, key availability). Corrupted records are diverted to quarantine stores.
4. **Data Normalisation:** Vendor-specific keys (`src_ip`, `id.orig_h`, `SourceIp`) are translated into a single common taxonomy (such as the **Elastic Common Schema / ECS** subset: `source.ip`).
5. **Contextual Enrichment:** Ingestion processors enrich raw logs with threat intelligence IP reputation scores, GeoIP geographic coordinates, and internal Active Directory asset ownership context.
6. **Indexing & High-Performance Storage:** Structured, normalized JSON documents are indexed into data stores (Elasticsearch, OpenSearch, Splunk buckets) for sub-second search capabilities.
7. **Analytics, Correlation & Alerting:** Continuous detection engines query indexed data against rules (Sigma, SPL, KQL) to generate actionable SOC alerts.

---

## 3. Ingestion-Time Normalisation vs. Post-Ingestion Querying

Understanding when and where data transformation occurs is a fundamental distinction in security data engineering:

| Architectural Metric | Ingestion-Time Normalisation (ETL / Pipeline) | Post-Ingestion Querying (Schema-on-Read) |
| :--- | :--- | :--- |
| **Execution Point** | Occurs in the stream *before* indexing into database storage. | Occurs *during* analyst search execution across raw unparsed logs. |
| **Search Performance** | **Ultra-Fast:** Queries run against structured, pre-indexed common keys (`source.ip`). | **Slow:** Heavy CPU overhead required to extract regex patterns at search time. |
| **Storage & Overhead** | Slightly higher ingestion CPU; clean data structures stored. | Lower ingestion CPU; massive compute tax during search operations. |
| **Rule Portability** | High: Detection rules work across all vendor telemetry without rule edits. | Low: Analysts must write custom regex for every tool variation in every search query. |

---

## 4. Pipeline Execution Metrics & Data Quality Report

To ensure evidentiary integrity, the Day 21 mini-SIEM ingestion pipeline (`scripts/siem_pipeline.py`) processes raw multi-vendor log sources and enforces strict quarantine and deduplication rules:

### Ingestion Metrics Summary (`output/ingestion-metrics.json`):

* **Total Raw Telemetry Lines Scanned:** `5`
* **Valid Normalised Events Indexed:** `3` (`60.0%` success rate)
* **Malformed / Corrupted Lines Quarantined:** `1` (JSON decode failure isolated to `output/quarantine_malformed.jsonl`)
* **Duplicate Events Filtered:** `1` (Identical alert string hash dropped)
* **Target Output File:** `output/normalized_events.jsonl`

---

## 5. Key Portfolio Takeaways & Core Analyst Principles

1. **Garbage In, Garbage Out:** If upstream log parsers fail to normalize timestamps to standardized UTC ISO-8601 strings, or drop source port fields during ingestion, downstream SIEM correlation rules will fail silently without alerting defenders.
2. **Normalisation Is Structural Discipline:** Standardizing heterogeneous vendor attributes into a predictable ECS subset transforms isolated sensor data into a unified, searchable security dataset.
