# Mini-SIEM Ingestion and Normalisation Pipeline

**Author:** Serah Mulwa

**Module:** Day 21 - SIEM Architecture, Log Ingestion & Security Data Engineering

---

## 1. Project Overview

A Python-based security data ingestion pipeline that processes synthetic security events from multiple sources, validating structural integrity, normalising log dialects into a unified Elastic Common Schema (ECS) subset, enriching records with local asset metadata, and isolating malformed data into a Dead-Letter Queue (DLQ).

---

## 2. Problem Statement

Security telemetry from different systems often uses different formats and field names—Windows domain controllers talk in Event IDs, firewalls log connection states, and network monitors output epoch timestamps and connection flow IDs.

This project demonstrates how heterogeneous security records can be validated and normalised without losing forensic raw lineage, ensuring high data quality for downstream Security Operations Center (SOC) detection rules.

---

## 3. End-to-End Pipeline Architecture

```
Raw Telemetry Input (data/raw/*.jsonl)
        │
        ▼
1. INPUT READER (Line-by-line generator streaming)
        │
        ▼
2. JSON PARSER (try-except syntax validation & DLQ isolation)
        │
        ▼
3. VALIDATION (ipaddress module & port bounds 1-65535)
        │
        ▼
4. NORMALISATION (Mapping fields to unified ECS subset + raw lineage)
        │
        ▼
5. ASSET ENRICHMENT (O(1) dictionary lookup for business criticality)
        │
        ▼
6. DEDUPLICATION (In-memory content hashing)
        │
        ▼
7. STRUCTURED STORAGE & METRICS (processed/ & reports/ingestion_report.json)
```

---

## 4. Key Features & Engineering Design

* **Line-by-Line Streaming:** Uses generator loops to process logs without memory bloat or Out-of-Memory (OOM) crashes.
* **Fault Tolerant Quarantine (DLQ):** Intercepts malformed JSON strings, invalid IP addresses, and out-of-range ports, routing them to `data/quarantine/rejected.jsonl` without halting execution.
* **Elastic Common Schema (ECS) Normalisation:** Unifies heterogeneous logs into a single analytical model while preserving original raw lineage (`raw_reference`).
* **Contextual Asset Enrichment:** Maps source IP addresses against a local CMDB reference (`data/asset_inventory.json`) with O(1) dictionary lookups to inject hostnames, departments, and criticality tiers.
* **Automated Unit Testing:** Covered by a 100% passing test suite (`tests/test_ingest.py`) using Python's built-in `unittest` framework.
* **Cryptographic Integrity:** Backed by SHA-256 hashing baselines to guarantee log immutability during forensic audits.

---

## 5. Quickstart Guide & Repository Usage

### Prerequisites
* Python 3.8+
* Linux / Parrot OS terminal environment

### Setup & Execution
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Serah-Cybersecurity/mini-siem-ingestion-pipeline.git
   cd mini-siem-ingestion-pipeline
   ```
2. **Create and Activate Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Run the Ingestion Pipeline:**
   ```bash
   python3 -m src.ingest
   ```
4. **Execute Automated Unit Tests:**
   ```bash
   python3 -m unittest discover -s tests -v
   ```
