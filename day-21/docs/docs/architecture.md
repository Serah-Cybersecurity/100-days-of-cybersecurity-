# Technical Note: End-to-End Pipeline Architecture & Stage Breakdown

**Author:** Serah  Mulwa

**Module:** Day 21 - SIEM Architecture, Log Ingestion & Security Data Engineering

## 1. Executive Summary

In enterprise security operations, raw telemetry arrives from disparate sensors in completely different formats and dialects. Without a rigorous, multi-stage data engineering pipeline, Security Information and Event Management (SIEM) platforms would drown in malformed records, missing timestamps, and unnormalised fields.

This technical document details the architectural design of my Mini-SIEM ingestion pipeline (`src/ingest.py`). It breaks down the complete data lifecycle—from raw synthetic log ingestion to streaming validation, Elastic Common Schema (ECS) normalisation, asset enrichment, dead-letter quarantine, and structured health reporting.

---

## 2. End-to-End Pipeline Architecture Diagram

The following Mermaid flowchart illustrates the precise execution path of security telemetry through our 7-stage streaming pipeline:

```mermaid
flowchart TD
    subgraph Data Sources [Raw Telemetry Sources]
        W["Windows Events (windows.jsonl)"]
        L["Linux Audit (linux.jsonl)"]
        F["Firewall Logs (firewall.jsonl)"]
        S["Suricata IDS (suricata.jsonl)"]
    end

    W & L & F & S --> IR

    subgraph Pipeline Processing Engine (src/ingest.py)
        IR["1. Input Reader (Streaming line-by-line generator)"] --> JP["2. JSON Parser (Syntax & Try-Except block)"]
        JP -->|Malformed JSON| Q["Quarantine (Dead-Letter Queue) data/quarantine/rejected.jsonl"]
        JP -->|Valid JSON| VAL["3. Validation Engine (ipaddress module & port bounds 1-65535)"]
        VAL -->|Invalid IP/Port| Q
        VAL -->|Valid Record| NORM["4. Normalisation Engine (Mapping to ECS subset + Raw Lineage)"]
        NORM --> ENR["5. Asset Enrichment Engine (O(1) CMDB lookup for business criticality)"]
        ENR --> DEDUP["6. Deduplication Engine (In-memory content hashing)"]
    end

    DEDUP --> STOR["7. Structured Storage (data/processed/normalized_*.jsonl)"]
    DEDUP --> REP["8. Reporting Engine (reports/ingestion_report.json)"]
```

---

## 3. Detailed Pipeline Stage Breakdown

### Stage 1: Data Sources
Enterprise security telemetry originates from multiple heterogeneous endpoints and sensors. In my lab environment, I simulated four distinct security data streams stored in `data/raw/`:
* **Windows Domain Controller (`windows.jsonl`):** Capturing authentication events (e.g., Windows Event ID 4625 failed logins and 4624 successful logins).
* **Linux Server (`linux.jsonl`):** Capturing administrative actions (`sudo` invocations, SSH sessions).
* **Network Firewall (`firewall.jsonl`):** Capturing perimeter traffic blocks and allows (`source_ip`, `destination_ip`, `action`).
* **Suricata IDS (`suricata.jsonl`):** Capturing network intrusion detection alerts and protocol metadata.

### Stage 2: Collection & Input Reading
Instead of loading massive log files entirely into RAM—which leads to Out-of-Memory (OOM) crashes in production—the pipeline utilizes Python's generator-based file iteration. It opens raw JSONL (JSON Lines) files line by line, ensuring low memory footprints and high streaming throughput.

### Stage 3: Parsing & Fault Tolerance
Raw log files often contain corrupted characters, truncated lines, or syntax errors injected during transmission. The parser wraps `json.loads(line)` inside a robust `try-except` block. If a line is malformed, the pipeline catches the `json.JSONDecodeError`, avoids crashing, and routes the bad record directly into the **Dead-Letter Queue (DLQ)** at `data/quarantine/rejected.jsonl`.

### Stage 4: Strict Validation Strategy
Before processing any record, the validation stage verifies foundational data integrity:
* **IP Address Validation:** Utilizes Python's built-in `ipaddress` library to ensure that `source.ip` and `destination.ip` conform to legitimate IPv4 or IPv6 standards, rejecting invalid strings (e.g., `999.999.999.999`).
* **Port Range Bounds:** Ensures port numbers fall within the valid TCP/UDP range (`1` to `65535`), rejecting out-of-bounds integers.
* **Failure Handling:** Any record failing validation is immediately intercepted and isolated in the quarantine DLQ.

### Stage 5: Elastic Common Schema (ECS) Normalisation
To make cross-tool searching possible, heterogeneous log keys are mapped into a unified ECS subset. For example:
* Windows `source_ip` and Zeek `id.orig_h` are both normalized into `source.ip`.
* Windows Event ID `4625` is translated into the unified action `authentication_failure`.
* **Forensic Raw Lineage:** To ensure no investigative detail is lost during normalisation, the complete original raw record dictionary is preserved inside a `raw_reference` field (`normalized["raw_reference"] = record`).

### Stage 6: Asset Enrichment
Raw IP addresses alone do not give incident responders business context. The enrichment module loads a local Configuration Management Database (CMDB) lookup table (`data/asset_inventory.json`). Using an **O(1) dictionary lookup**, the pipeline matches incoming IP addresses with their corresponding asset metadata—injecting hostnames (`workstation-01`), asset types (`workstation`), departments (`finance`), and criticality tiers (`medium`) directly into the event object.

### Stage 7: Deduplication
Network and endpoint sensors frequently retransmit identical log packets due to network retries or agent misconfigurations. The deduplication stage uses in-memory content hashing to track seen events within a batch, dropping duplicate records to prevent storage bloat and alert fatigue in the SOC.

### Stage 8: Storage & Reporting
* **Processed Storage:** Clean, normalized, and enriched events are written line-by-line to `data/processed/normalized_{source}.jsonl`.
* **Execution Reporting:** Upon batch completion, the pipeline calculates performance metrics and writes a structured summary report to `reports/ingestion_report.json`, tracking `records_received`, `records_processed`, `records_valid`, `records_rejected`, `records_duplicated`, `records_written`, and `processing_duration_seconds`.
