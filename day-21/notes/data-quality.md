# Technical Note: SIEM Data Quality, Pipeline Resilience & Timestamp Engineering

**Author:** Serah Mulwa

**Module:** Day 21 - SIEM Architecture, Log Ingestion & Security Data Engineering

## 1. Executive Summary & Personal Reflections

When building introductory cybersecurity projects, it is easy to assume that incoming security logs are always clean, well-formed, and arrive on time. However, building production-grade telemetry pipelines on Day 21 has taught me a fundamental truth: **data is inherently messy, corrupted, delayed, and duplicated.**

In enterprise security—and especially at Big Tech scale—the dividing line between an amateur script and a professional detection engineering pipeline is how it handles bad data. If an ingestion pipeline silently drops malformed log lines or fails to notice that a critical log source has stopped sending telemetry, downstream detection rules will fail silently. A broken data pipeline creates immediate visibility gaps, blinding the Security Operations Center (SOC) during an active breach.

This technical note documents my engineering analysis of data quality challenges, the operational distinction between event time and ingestion time, pipeline error handling strategies, and quarantine architectures.

---

## 2. The Seven Deadly Sins of Log Data Quality

In a real-world enterprise network, log streams constantly encounter corrupt or ambiguous records. A professional ingestion pipeline must actively identify and manage these issues rather than crashing or ignoring them. 

| Data Quality Problem | Example Scenario | Why It Breaks Detection | How My Pipeline Handles It |
| :--- | :--- | :--- | :--- |
| **Missing Timestamp** | `{"src_ip": "10.0.2.15", "alert": "Brute force"}` | Impossible to order events chronologically or build an investigation timeline. | Assigns current UTC fallback timestamp or routes the event to quarantine. |
| **Invalid IP Address** | `{"source_ip": "999.999.999.999"}` | Breaks GeoIP enrichment lookups and CIDR-based firewall network matching rules. | Validates IP octets/regex patterns before indexing; flags anomalous entries. |
| **Malformed JSON** | `{"timestamp": "2026-11-07", "user": "admin" (missing closing brace)` | Causes parser crashes or halts entire file ingestion streams. | Wraps JSON parsing in `try-except` blocks; isolates bad lines into a quarantine DLQ. |
| **Duplicate Records** | The exact same Syslog packet received twice due to network retry loops. | Inflates event counts, skews metrics, and causes duplicate alert fatigue for analysts. | Implements in-memory hashing or sliding-window deduplication sets. |
| **Unknown Event Type** | An updated EDR agent sends a new event schema (`event_type: unknown_telemetry`). | Detection rules written for known schemas will ignore the event entirely. | Logs unrecognized types to review streams without destroying raw event lineage. |
| **Time-Zone Ambiguity** | `2026-11-07 14:30:00` (No `Z` or offset indicator). | Creates hours of offset errors when correlating logs across global data centers. | Enforces strict ISO-8601 UTC parsing and normalizes all incoming epochs. |
| **Missing Source Identifier**| An unlabelled log line stating only `Authentication denied`. | Analysts cannot identify which server, workstation, or firewall generated the alert. | Injects observer/sensor metadata tags during the initial ingestion phase. |

---

## 3. Event Time versus Ingestion Time: The Three Timestamp Pillars

A common beginner mistake is assuming that the time an event happened is identical to the time the SIEM processed it. In distributed environments, network lag, agent buffer queues, and transport congestion create massive time gaps.

To measure pipeline health and ensure accurate forensic timelines, modern SIEM architectures (and Elastic Common Schema standards) split timestamps into three distinct pillars:

1. **`@timestamp` (Event Time):** 
   * **Definition:** The exact moment the event occurred on the original system (e.g., when a user authenticated or a firewall dropped a packet).
   * **Purpose:** Used for forensic investigation, alert correlation, and timeline reconstruction.

2. **`event.created` (Observation Time):** 
   * **Definition:** The moment the local collection agent or forwarder first read and packaged the log file.
   * **Purpose:** Helps isolate whether delays originated on the endpoint agent.

3. **`event.ingested` (Storage Time):** 
   * **Definition:** The precise moment the central SIEM indexing cluster successfully wrote the record to storage.
   * **Purpose:** Monitors core pipeline transport health.

### Calculating Pipeline Latency:
By subtracting `@timestamp` from `event.ingested`, a Security Data Engineer can compute real-time pipeline latency. If latency spikes from 2 seconds to 45 minutes, an automated alert fires to notify engineers of network throttling or collector bottlenecks.

---

## 4. Implementing Pipeline Resilience & Quarantine in Python

In my Python implementation (`scripts/siem_pipeline.py`), data quality validation is built directly into the core ingestion loop. Rather than crashing when encountering bad data, the pipeline follows a strict validation hierarchy:

```
Raw Telemetry Input
        │
        ▼
[ Syntax Validation (JSON Parsing) ] ── (Fail) ──► [ Quarantine Dead-Letter Queue (DLQ) ]
        │ (Pass)
        ▼
[ Schema Validation (Mandatory Fields) ] ── (Fail) ──► [ Quarantine Dead-Letter Queue (DLQ) ]
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
* **Syntax Exception Handling:** Wrapping `json.loads()` inside a `try-except` block guarantees that corrupt or truncated log lines never crash the script.
* **Dead-Letter Queuing (DLQ):** Failed records are written out to `output/quarantine_malformed.jsonl` along with line numbers and exception messages, allowing engineers to audit parser errors without losing data visibility.
* **Automated Metrics Reporting:** The script outputs a structured JSON metrics file (`output/ingestion-metrics.json`) quantifying total lines scanned, valid records normalized, duplicate counts, and overall ingestion success rates.

---

## 5. Job Market & Big Tech Interview Positioning

When interviewing for Security Data Engineering or Detection Engineering roles at global tech companies (such as Microsoft, Google, AWS, or Datadog), interviewers frequently evaluate resilience engineering:

* **Interview Question:** *"How do you ensure your SIEM alerting rules don't blindside the SOC when a critical log source starts sending corrupted payloads due to a vendor software update?"*
* **Professional Answer:** *"I design ingestion pipelines with strict edge-validation, syntax try-except blocks, and isolated dead-letter queues. If an ingestion stream experiences schema drift or parsing error spikes, the pipeline quarantines the malformed records safely while emitting an automated operational alert on the pipeline success-rate metric, preventing silent detection failures."*

---

## 6. Summary Checklist for Portfolio Verification

| Data Quality Stage | Implementation Artifact | Engineering Purpose | 
| ----- | ----- | ----- | 
| **Syntax Protection** | `scripts/siem_pipeline.py` | `try-except` JSON parsing guards preventing runtime crashes. | 
| **Quarantine Isolation** | `output/quarantine_malformed.jsonl` | Dead-letter queue capturing corrupted or unanchored log lines. | 
| **Deduplication** | In-memory hash sets | Prevents duplicate event inflation and analyst alert fatigue. | 
| **Quality Reporting** | `output/ingestion-metrics.json` | Quantifies ingestion success rates and data quality health. | 
