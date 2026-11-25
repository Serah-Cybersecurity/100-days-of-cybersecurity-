# Technical Note: Search Processing Language (SPL) Fundamentals & Analytical Standards

**Author:** Serah Kathini Mulwa

**Program:** Women Techsters Fellowship — Cybersecurity Track

**Module:** Day 22 — Splunk Fundamentals & Search Processing Language (SPL)

---

## 1. Executive Summary & Purpose

In security operations, collecting log telemetry is only half the battle. Once data is ingested into an enterprise platform like Splunk, analysts must know how to effectively query, aggregate, filter, and extract actionable intelligence from it.

This document serves as an operational reference for **Search Processing Language (SPL)** within my `mini-siem-to-splunk-investigation-workbench` repository. It outlines the core mechanics of SPL execution pipelines, query optimization techniques, order of operations, and standards for documenting threat-hunting queries.

---

## 2. The SPL Pipeline Architecture & Pipe Operator (`|`)

SPL processes data sequentially from left to right using the Unix pipe operator (`|`). Each command takes the dataset produced by the preceding stage, transforms or filters it, and passes the updated dataset to the next command.

```
+------------------+       +-------------------+       +--------------------+       +---------------+
| 1. Base Search   | ----> | 2. Event Filter   | ----> | 3. Aggregation     | ----> | 4. Sorting    |
| (index=...)      |  |    | (| search ...)    |  |    | (| stats ...)      |  |    | (| sort ...)  |
+------------------+       +-------------------+       +--------------------+       +---------------+
```

### Dissecting an Example Query

```spl
index=cybersecurity_lab
| search event_outcome="failure"
| stats count by username
| sort - count
```

1. **`index=cybersecurity_lab` (Base Scoping):** Restricts the execution scope to the lab's storage partition, preventing resource-intensive cluster scans across unneeded indexes.
2. **`| search event_outcome="failure"` (Filtering):** Evaluates raw events within the index, retaining only records matching authentication failures.
3. **`| stats count by username` (Aggregation):** Summarizes individual events into a tabular structure, counting occurrences per unique `username`.
4. **`| sort - count` (Sorting):** Sorts the resulting table by `count` in descending order (denoted by `-`), placing high-frequency failure sources at the top.

---

## 3. Order of Operations: Performance & Data Preservation

The order of commands directly dictates query performance and data availability. Aggregating data too early discards raw event fields needed for subsequent operations.

### Correct Pipeline Flow (Filter Early, Aggregate Late)
```spl
index=cybersecurity_lab event.category="authentication"
| search event.action="authentication_failure"
| stats count as failures, dc(user.name) as distinct_users by source.ip
| where failures >= 5
| sort - failures
```
* **Why it works:** Filtering occurs at the index and early search levels, discarding irrelevant data while preserving raw key-value fields. Mathematical aggregations run only against relevant records.

### Incorrect Pipeline Flow (Premature Aggregation)
```spl
index=cybersecurity_lab
| stats count by host.name
| search event.action="authentication_failure"
```
* **Why it breaks:** The `stats` command collapses individual log events into host summary rows, discarding `event.action`. The downstream `search` fails because the field no longer exists in the tabular pipeline.

---

## 4. Portfolio Documentation Standards (`queries/`)

All reusable SPL query files saved within the `queries/` repository directory must adhere to a standardized header format:

```spl
-- =============================================================================
-- Query Title: High-Volume Authentication Failures
-- File Name: 01_authentication_anomalies.spl
-- Objective: Detect brute-force attempt patterns across multiple user accounts
-- Targeted Index: cybersecurity_lab
-- Required Fields: event.action, source.ip, user.name, host.name
-- Analytical Interpretation: High count with dc(user.name) > 1 suggests potential
--                            credential stuffing or horizontal brute-force activity.
-- Author: Serah Kathini Mulwa
-- =============================================================================

index=cybersecurity_lab event.category="authentication" event.action="authentication_failure"
| stats count as total_failures, dc(user.name) as distinct_users, values(user.name) as targeted_accounts by source.ip, host.name
| where total_failures > 3
| sort - total_failures
```

---

## 5. Core Operational Principles

1. **Scope Queries Explicitly:** Always specify `index=` at the very start of a search string to avoid querying `index=*`.
2. **Filter Before Transforming:** Apply criteria like `event.action=` or specific IP filters before invoking transforming commands like `stats`, `chart`, or `timechart`.
3. **Understand Sort Directions:** Using `-` before a field name in `sort` orders results from highest to lowest, surfacing top anomalies first.
4. **Preserve Context for Analysis:** Ensure base searches retain necessary fields before aggregating, keeping event-level detail accessible for deeper investigation.
