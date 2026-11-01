# Day 13 - Splunk Practical Exercise & Advanced SPL Correlation Queries

* **Author:** Serah Mulwa
* **Date:** October 31, 2026
* **Module:** SIEM Fundamentals & Advanced Search Processing Language (SPL)
* **Target Audience:** Tier 1 SOC Analysts & Detection Engineers

---

## 1. Executive Summary & Strategy

Splunk is an enterprise-grade Security Information and Event Management (SIEM) and Big Data analytics platform widely deployed across enterprise Security Operations Centers (SOCs). 

While completing hands-on labs using custom Python tools provides fundamental architectural knowledge, mastering **Search Processing Language (SPL)** inside a live Splunk environment is a core technical requirement for security analysts. 

> 💡 **Golden Rule:** Do not spend money or install resource-intensive enterprise software solely for basic exercises. Master the query logic and pipeline syntax theoretically today, and apply it in free developer instances or enterprise labs later.

---

## 2. File Ingestion & Setup Workflow

When ingesting synthetic datasets (such as `events.jsonl`) into a Splunk instance via the Graphical User Interface (GUI), adhere to the following standard operating procedure:

1. **Access Data Ingestion:** Open the Splunk Web interface and navigate to **Settings** > **Add Data**.
2. **Select Upload Method:** Choose **Upload** to ingest files directly from your local workstation.
3. **Select Source File:** Browse to and select `day-13/lab/data/events.jsonl`.
4. **Source Format Parsing:** Inspect the data preview panel. Explicitly set the source format to **JSON** (`_json`) to ensure Splunk automatically extracts key-value pairs (e.g., `username`, `src_ip`, `event_id`) into indexed fields during ingestion.
5. **Index Allocation:** Assign the dataset to the `main` index (or a dedicated laboratory index such as `sec_lab`).
6. **Submit & Review:** Confirm settings and proceed to the Search & Reporting application.

---

## 3. Data Baseline Verification

Before executing complex analytical or correlation pipelines, **never assume field names or source classifications**. Always verify what Splunk actually assigned to your ingested data.

### Baseline Check Query
```spl
index=main
| head 20
```

* **Purpose:** Inspects the first 20 records indexed in `main`.
* **Technical Justification:** Verifies auto-extracted field names, default `sourcetype` labels, and timestamp parsing accuracy. If Splunk indexes a field under a different key name than expected, downstream analytical queries will return zero results.

---

## 4. Analytical SPL Query Toolkit

### Query 1 — Aggregate Event Types
```spl
index=main
| stats count by event_type
```
* **What it does:** Calculates total log volume grouped by the normalized `event_type` field (e.g., `authentication`, `network`, `process`, `service`).
* **How it works:** The `stats count by` command aggregates events into a summary table, similar to a SQL `GROUP BY` clause.
* **SOC Context:** Used during operational health checks to verify log feed continuity and detect sudden volume drops or spikes.

---

### Query 2 — Authentication Failure Summary
```spl
index=main event_type=authentication result=failure
| stats count by username src_ip
| sort - count
```
* **What it does:** Filters exclusively for failed authentication events, counts occurrences per `username` and `src_ip` combination, and orders results in descending order.
* **How it works:** Filters are applied on the left side of the initial pipe (`|`), followed by aggregation (`stats count`), and visual sorting (`sort - count`).
* **SOC Context:** Identifies high-volume authentication failure sources to highlight potential brute-force or credential-stuffing origin IPs.

---

### Query 3 — Chronological Event Timeline Reconstruction
```spl
index=main event_type=authentication
| sort 0 _time
| table _time host platform username src_ip result event_id
```
* **What it does:** Extracts all authentication telemetry, sorts events in chronological order, and formats the output into a structured investigation table.
* **How it works:** `sort 0 _time` overrides Splunk's default 10,000-record sorting cap to order the entire dataset by the internal `_time` epoch timestamp before outputting selected columns using `table`.
* **SOC Context:** Essential for forensic timeline construction during post-incident analysis.

---

### Query 4 — Cross-Platform Log Source Inspection
```spl
index=main
| stats count by platform source event_type
```
* **What it does:** Generates a multi-dimensional matrix showing event counts categorized by platform layer (`windows`, `linux`, `network`), log subsystem (`Security`, `sshd`, `firewall`), and event type.
* **How it works:** Groups counts across three distinct metadata keys simultaneously.
* **SOC Context:** Used by Detection Engineers to verify cross-platform coverage and validate log normalization standards across disparate operating systems.

---

### Query 5 — Temporal Brute-Force Correlation Engine
```spl
index=main event_type=authentication
| sort 0 _time
| streamstats time_window=10m
    count(eval(result="failure")) AS failures_last_10m
    BY username src_ip
| where result="success" AND failures_last_10m>=3
| table _time host username src_ip result failures_last_10m
```

#### Detailed Logic Breakdown:
1. `index=main event_type=authentication`: Isolates authentication events.
2. `sort 0 _time`: Orders all matching events chronologically to allow accurate temporal evaluation.
3. `streamstats time_window=10m count(eval(result="failure")) AS failures_last_10m BY username src_ip`: Calculates a rolling count of failed authentications per `username` and `src_ip` over a sliding 10-minute window as each event is processed.
4. `where result="success" AND failures_last_10m>=3`: Filters output strictly for successful logins that were immediately preceded by 3 or more failures within that 10-minute window.
5. `table ...`: Formats the final alert candidate for analyst review.

* **SOC Context:** Industry-standard behavioral correlation logic used to catch successful account compromises following brute-force attempts.

---

## 5. Core Analyst Principles

> 💡 **Axiom 1:** Time-based commands like `streamstats` rely on strict chronological sorting (`sort 0 _time`). Unsorted datasets produce invalid sliding-window calculations.
>
> 💡 **Axiom 2:** Query candidate detections do not constitute proof of compromise. They represent filtered telemetry requiring human investigation and context validation.
