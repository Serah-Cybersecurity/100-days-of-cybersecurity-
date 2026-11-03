# DNS Security Investigation Report

## 1. Case Information
* **Case ID:** DAY16-DNS-001
* **Environment:** Synthetic DNS telemetry (Offline analysis)
* **Analyst:** Serah Mulwa 
* **Date:** November 3, 2026

## 2. Investigation Objective
To evaluate offline DNS telemetry logs using custom heuristic detection logic, identifying internal client endpoints exhibiting unusual behavioral characteristics that warrant secondary human review.

## 3. Scope
* **Input Dataset:** `day-16/lab/data/dns-events.jsonl` (17 synthetic records)
* **Client Addresses:** `192.0.2.10`, `192.0.2.25`, `192.0.2.30`
* **DNS Resolver:** `192.0.2.53`
* **Time Range:** 2026-11-03T09:00:00+03:00 to 09:24:00+03:00
* **Tools Used:** Python 3, custom `dns_analyzer.py` script, Wireshark, CLI utilities (`dig`, `wc`).

## 4. Methodology
The investigation utilized a programmatic heuristic parsing utility that performed:
* **Data Validation:** JSON schema enforcement and mandatory field checking.
* **Timestamp Normalization:** Converting ISO 8601 strings into UTC-aware datetime objects.
* **Client Grouping:** Aggregating queries per client IP address.
* **Metric Calculation:** Tracking total queries, unique query names, maximum subdomain lengths, and record types.
* **Error & Burst Analysis:** Calculating `NXDOMAIN` proportions and sliding-window peak request frequencies over a 10-minute interval.
* **Multi-Indicator Evaluation:** Flagging clients that trigger two or more behavioral anomaly thresholds simultaneously.

## 5. Findings

### Client 192.0.2.10
* **Observations:** Processed 6 total queries across 5 unique names, with a max name length of 18 characters, 1 TXT query (17%), 1 `NXDOMAIN` response, and a peak window frequency of 6.
* **Interpretation:** Normal browsing and baseline typing verification.
* **Review Status:** `No multi-indicator review condition met.` Does not warrant further review.

### Client 192.0.2.25
* **Observations:** Processed 8 total queries across 8 unique names, with a max name length of 65 characters (`application-health-check-region-west-node-0001.status.example.net`), 6 TXT queries (75%), 0 `NXDOMAIN` responses, and a peak window frequency of 8.
* **Triggered Indicators:** `high query frequency`, `long query names`, `high TXT-query proportion`.
* **Interpretation:** Exhibits bursty, structured polling behavior targeting application status endpoints with heavy TXT utilization. While meeting multi-indicator criteria for review, this pattern strongly aligns with automated health-checking daemons or monitoring agents rather than confirmed malicious activity.

### Client 192.0.2.30
* **Observations:** Processed 3 total queries across 3 unique names, with a max name length of 16 characters, 0 TXT queries (0%), 0 `NXDOMAIN` responses, and a peak window frequency of 3.
* **Interpretation:** Quiet client conducting standard API and mail server lookups.
* **Review Status:** `No multi-indicator review condition met.` Normal baseline behavior.

## 6. Detection Logic
* **Minimum queries:** 8
* **Time window:** 10 minutes
* **Long-name threshold:** 60 characters
* **Minimum TXT records:** 4
* **TXT proportion:** 50%
* **Minimum indicators:** 2

## 7. Testing
The analysis tool successfully passed all 7 validation tests, including syntax verification (`py_compile`), baseline execution, argument threshold tuning (`--min-queries`, `--long-name`), missing file error handling (exit code `2`), and malformed JSON resilience.

## 8. Limitations
* The dataset is entirely synthetic and fictional.
* No live DNS servers or network packets were captured during this evaluation.
* Endpoint process attribution (e.g., Sysmon / EDR process trees) and external domain reputation data were unavailable.

## 9. Recommendations
To conduct a true enterprise DNS investigation, analysts must gather:
1. Endpoint process telemetry to identify the local application initiating queries.
2. Resolver-side historical logs to verify recursive query paths.
3. Authoritative network baselines to separate legitimate scheduled monitoring tools from unauthorized scripts.

## 10. Conclusion
The synthetic dataset identifies `192.0.2.25` as a client exhibiting multiple unusual DNS characteristics. Specifically, its records show higher request frequency, longer query names, and a higher proportion of TXT requests compared to other clients. These characteristics justify further examination. However, they do not establish that DNS tunnelling, command-and-control communication, or other malicious activity occurred. Definitive conclusions require correlative endpoint and resolver evidence.
