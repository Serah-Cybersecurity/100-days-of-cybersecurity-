# Day 13 - Essential Splunk Search Processing Language (SPL) Command Toolkit

* **Author:** Serah Mulwa  
* **Date:** October 31, 2026  
* **Module:** SIEM Fundamentals & Log Engineering  
* **Target Audience:** Tier 1 SOC Analysts & Security Engineers  

---

## 1. Executive Summary & Command Architecture

The **Search Processing Language (SPL)** is Splunk's proprietary query language built to search, transform, aggregate, and analyze machine telemetry. SPL operates as a left-to-right sequential pipeline where the output of each command is passed down to the next using the pipe character (`|`).

```
[Raw Log Ingestion] ──> [base search] ──|──> [transformation/stats] ──|──> [eval/where filter] ──|──> [table output]
```

---

## 2. The 10 Essential SPL Commands Matrix

| Command | Primary Purpose | Pipeline Function | Job Market Frequency |
| :--- | :--- | :--- | :--- |
| **`search`** | Filters raw events matching specified criteria. | Base Filter (Entry Point) | Every Single Query |
| **`table`** | Displays selected fields in a clean tabular grid. | Presentation & Formatting | High |
| **`fields`** | Keeps or excludes specific fields from search memory. | Optimization & Performance | High |
| **`stats`** | Calculates statistical metrics (`count`, `dc`, `avg`, `values`). | Aggregation & Analysis | Critical |
| **`where`** | Filters results using boolean or numerical expressions. | Post-Aggregation Filter | High |
| **`sort`** | Orders results ascending (`+`) or descending (`-`). | Ordering & Ranking | High |
| **`timechart`** | Calculates and formats metrics over time intervals (`span=`). | Trend Analysis & Dashboards | High |
| **`eval`** | Creates dynamic fields or evaluates expressions/string operations. | Data Enrichment | High |
| **`dedup`** | Removes duplicate event rows based on field values. | Noise Reduction | Medium |
| **`streamstats`** | Calculates running/rolling statistics across sequential events. | Behavioral Sequence Analysis | Advanced |

---

## 3. Command Breakdown & Practical Examples

### 3.1 `table`
Formats output into clean column headers for reporting and documentation.

```spl
index=security EventCode=4624 
| table _time host TargetUserName IpAddress LogonType
```

### 3.2 `stats`
Calculates aggregated statistics across security logs. Key functions include `count`, `dc()` (distinct count), and `values()`.

```spl
index=security EventCode=4625 
| stats count dc(IpAddress) AS Unique_IPs values(IpAddress) AS IP_List BY TargetUserName
| sort - count
```

### 3.3 `where`
Filters aggregated results or dynamic calculated values using boolean logic.

```spl
index=security EventCode=4625 
| stats count BY TargetUserName, IpAddress 
| where count > 5
```

### 3.4 `sort`
Orders search output ascending (`+`) or descending (`-`).

```spl
index=security EventCode=4688 
| stats count BY NewProcessName 
| sort - count
```

### 3.5 `timechart`
Groups data into time buckets (`span=`) for line/bar chart visualization.

```spl
index=security EventCode=4625 
| timechart span=1h count BY TargetUserName
```

### 3.6 `eval`
Creates dynamic fields, calculates conditional logic (`if`), or tags risk levels.

```spl
index=security EventCode=4624 
| eval Risk_Level = if(LogonType==10, "HIGH_RDP", "NORMAL_LOGIN")
| table _time TargetUserName LogonType Risk_Level IpAddress
```

### 3.7 `streamstats`
Calculates rolling statistics over event streams chronologically without collapsing individual rows.

```spl
index=security 
| sort 0 _time 
| streamstats count current=true window=5 BY IpAddress
```

---

## 4. Documentation Standards & Analyst Rules

When recording SPL queries in SOC investigation logs:

1. **Document Pipeline Logic:** Explain the purpose of each pipe step (e.g., *"Filtered for EventCode 4625, grouped by source IP using `stats`, applied `where count > 5` to isolate brute-force sources"*).
2. **Include Time Bounds:** Always explicitly state `earliest=` and `latest=` parameters.
3. **Filter Early:** Place `index=` and static string filters before the first pipe (`|`) to optimize indexer memory usage.

> 💡 **Core Rule:** *SPL executes strictly left to right. Fields dropped by a command like `table` or `fields` early in the pipeline will not be available for downstream commands like `stats` or `eval`.*
