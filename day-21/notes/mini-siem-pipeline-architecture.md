# Technical Note: Enterprise SIEM Ingestion Pipeline, Data Quality Engineering & Multi-Source Normalisation

**Author:** Serah Mulwa

**Module:** Day 21 - SIEM Architecture, Log Ingestion & Security Data Engineering

## 1. Executive Summary & Personal Reflections

When studying cybersecurity as a beginner, it is easy to focus exclusively on attack techniques, packet captures, and alert rules while ignoring the underlying data engineering that makes security monitoring possible. Throughout my practical engineering work on Day 21, I learned a vital truth: **a Security Operations Center (SOC) is only as effective as its data pipeline.**

If an ingestion pipeline silently drops malformed log lines, fails to notice that a critical log source stopped sending telemetry, or cannot harmonize mismatched log formats, detection rules will fail during an active breach. 

This technical note documents my complete implementation of a production-grade Python Mini-SIEM ingestion pipeline. It covers synthetic fault injection, a 7-stage streaming architecture, automated unit testing, local asset inventory enrichment, and multi-source normalization connecting previous telemetry projects into a unified Elastic Common Schema (ECS) subset.

---

## 2. Synthetic Data Generation & Fault Injection (Part 6.1)

To build a resilient ingestion pipeline, you cannot test against pristine, perfectly formatted data. You must test how your system reacts to messy, corrupted inputs. I engineered four multi-source synthetic log files in `data/raw/`:

1. **`windows.jsonl`:** Windows authentication events (Event IDs 4625 and 4624).
2. **`linux.jsonl`:** Unix/Linux authentication logs (`sshd` successes and failures).
3. **`firewall.jsonl`:** Perimeter network connection records (`blocked` / `allowed`).
4. **`suricata.jsonl`:** Intrusion detection alerts and network signatures.

### Deliberate Fault Injection:
To prove our pipeline's error-handling resilience, I injected four major data quality anomalies directly into these raw files:
* **Invalid IP Address (`999.999.999.999`):** Injected into Windows logs to test IP validation logic.
* **Malformed JSON String (`MALFORMED_JSON_STRING...`):** Injected to test whether syntax errors crash the script or get isolated safely.
* **Out-of-Range Port (`70000`):** Injected into firewall logs to test TCP/UDP port boundary validation.
* **Duplicate Records:** Identical Linux authentication log lines repeated twice to test deduplication mechanics.

---

## 3. The 7-Stage Python Ingestion & Normalisation Architecture (`src/ingest.py`)

Rather than writing a basic script that reads a file all at once, I engineered a robust **7-stage streaming pipeline** in Python (`src/ingest.py`) utilizing only the standard library (`json`, `pathlib`, `ipaddress`, `datetime`, `sys`):

```
Raw Telemetry Input (JSONL)
        │
        ▼
1. INPUT READER (Line-by-line generator streaming)
        │
        ▼
2. JSON PARSER (try-except syntax validation)
        │
        ▼
3. VALIDATION (ipaddress module & port bounds 1-65535)
        │
        ▼
4. NORMALISATION (Mapping disparate fields to unified ECS subset)
        │
        ▼
5. DEDUPLICATION (In-memory content hashing)
        │
        ▼
6. QUARANTINE ISOLATION (Dead-Letter Queue for bad records)
        │
        ▼
7. PROCESSED OUTPUT & METRICS REPORTING (normalised_events.jsonl & ingestion_report.json)
```

### Key Engineering Mechanisms:
* **Line-by-Line Streaming:** Uses generators (`for line in file:`) to keep RAM consumption constant, preventing Out-of-Memory (OOM) crashes when processing large log files.
* **Robust IP & Port Validation:** Leverages Python's built-in `ipaddress` library to verify IPv4/IPv6 integrity instantly, rejecting spoofed octets before indexing.
* **Dead-Letter Queuing (DLQ):** Intercepts syntax and validation failures, writing them to `data/quarantine/rejected.jsonl` with line numbers and exception reasons without halting the pipeline.
* **Content-Based Deduplication:** Computes a cryptographic/string hash of incoming rows to prevent duplicate event inflation and analyst alert fatigue.

---

## 4. Automated Unit Testing & Pipeline Determinism (Part 7)

In professional software and security engineering, code without automated tests is considered unfinished. I created `tests/test_ingest.py` using Python's built-in `unittest` framework to validate eight core test scenarios:
* Valid and invalid IPv4 address checks.
* TCP/UDP port boundary validation (1–65535).
* ISO-8601 UTC timestamp normalisation.
* Multi-source event mapping for Windows, Firewall, and Suricata records.

### Pipeline Determinism:
To ensure our test suite runs reliably, the pipeline enforces strict separation between **Event Time** (`@timestamp` from the original log) and **Processing Time** (`event.created` / `event.ingested`). This ensures core data remains deterministic and testable. Running `python3 -m unittest discover -s tests -v` verifies 100% test success.

---

## 5. Asset Inventory & Contextual Enrichment (Part 8)

Raw IP addresses (`192.0.2.25`) provide little operational value during an incident investigation without business context. I built a local CMDB reference file (`data/asset_inventory.json`) mapping IP addresses to hostnames, departments, asset types, and criticality tiers.

* **O(1) Dictionary Lookup:** The ingestion script loads the inventory into memory as a keyed dictionary, enabling instant O(1) enrichment lookups during log processing.
* **Graceful Handling of Unknown Assets:** If an IP address is unmapped (such as external C2 infrastructure), the pipeline explicitly labels the asset as `unknown` rather than hallucinating metadata.

---

## 6. Multi-Source Integration & Raw Lineage Preservation (Part 9)

A major hurdle in SIEM engineering is unifying disparate log dialects (Windows Event IDs, Zeek connection logs, Firewall JSONL, and Suricata alerts) into a single analytical model without losing investigative depth.

* **Schema Mapping Protocol:** We mapped heterogeneous source fields (`source_ip`, `id.orig_h`, `timestamp`, `ts`) into a unified ECS subset (`source.ip`, `@timestamp`, `event.provider`, `event.action`).
* **Preserving Raw Lineage (`raw_reference`):** While normalisation makes logs searchable, it abstracts away vendor-specific details. Our pipeline preserves the complete original log record inside a `raw_reference` key, ensuring senior threat hunters have full forensic depth available during deep investigations.

---

## 7. Summary Verification Checklist for GitHub Portfolio

| Pipeline Stage / Artifact | File Path / Implementation | Engineering Purpose | 
| ----- | ----- | ----- | 
| **Raw Telemetry & Faults** | `data/raw/*.jsonl` | Multi-source synthetic inputs with deliberate data quality anomalies. | 
| **Core Pipeline Engine** | `src/ingest.py` | 7-stage streaming parser, validator, normaliser, and deduplicator. | 
| **Quarantine DLQ** | `data/quarantine/rejected.jsonl` | Intercepts malformed JSON and invalid IPs without dropping lineage. | 
| **Automated Tests** | `tests/test_ingest.py` | Python `unittest` suite validating 8 core boundary and mapping rules. | 
| **Asset Enrichment** | `data/asset_inventory.json` | O(1) CMDB lookup mapping IPs to business criticality tiers. | 
| **Metrics Report** | `reports/ingestion_report.json` | Quantifies pipeline health, success rates, and volume per source. | 
