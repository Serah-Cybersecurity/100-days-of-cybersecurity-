# Incident Investigation Report: DNS Telemetry Analysis
**Analyst:** Serah Mulwa    
**Date:** November 3, 2026  
**Module:** Day 16 - DNS Security, Investigation, and Threat Detection  

---

## 1. Executive Summary
This report details an offline security analysis of synthetic DNS telemetry (`dns-events.jsonl`) conducted as part of the Day 16 detection engineering laboratory. Using a custom Python-based heuristic analyzer (`dns_analyzer.py`), three internal client endpoints (`192.0.2.10`, `192.0.2.25`, and `192.0.2.30`) were evaluated against baseline behavior across key metrics, including query volume, subdomain length, TXT-record proportions, and error frequencies (`NXDOMAIN`).

Out of the three clients analyzed, **one client (`192.0.2.25`) was flagged for human review** after triggering multiple concurrent behavioral heuristics. 

---

## 2. Investigation Scope & Environment
* **Dataset Source:** `day-16/lab/data/dns-events.jsonl` (17 synthetic DNS events).
* **Target Resolver IP:** `192.0.2.53`
* **Evaluation Parameters:**
  * Sliding-window query frequency threshold: $\ge 8$ queries / 10-minute window
  * Maximum query-name length threshold: $\ge 60$ characters
  * TXT-record ratio threshold: $\ge 4$ queries and $\ge 50\%$ proportion
  * `NXDOMAIN` ratio threshold: $\ge 3$ queries and $\ge 30\%$ proportion
* **Review Condition:** A client is flagged (`[REVIEW REQUIRED]`) when **two or more** indicators are met simultaneously.

---

## 3. Findings & Client Analysis

### 3.1 Client: `192.0.2.10`
* **Total Queries:** 6
* **Unique Query Names:** 5
* **Max Name Length:** 18 characters (`example.com`, `typo-check.invalid`)
* **TXT Queries:** 1 (17%)
* **NXDOMAIN Responses:** 1
* **Peak Queries in Window:** 6
* **Review Status:** `No multi-indicator review condition met.`
* **Analyst Assessment:** Normal baseline web browsing and routine configuration checks. No anomalous behavior observed.

### 3.2 Client: `192.0.2.25` (FLAGGED FOR REVIEW)
* **Total Queries:** 8
* **Unique Query Names:** 8
* **Max Name Length:** 65 characters (`application-health-check-region-west-node-0001.status.example.net`)
* **TXT Queries:** 6 (75%)
* **NXDOMAIN Responses:** 0
* **Peak Queries in Window:** 8
* **Review Status:** `[REVIEW REQUIRED]`
* **Triggered Indicators:**
  1. `high query frequency`
  2. `long query names`
  3. `high TXT-query proportion`
* **Analyst Assessment:** This client generated a high volume of long, structured queries targeting application health status endpoints, heavily skewed toward TXT records. While these patterns align with automated service monitoring or health-checking daemons, the presence of multiple anomaly indicators warrants human verification to rule out protocol abuse or covert data encapsulation.

### 3.3 Client: `192.0.2.30`
* **Total Queries:** 3
* **Unique Query Names:** 3
* **Max Name Length:** 16 characters (`mail.example.org`)
* **TXT Queries:** 0 (0%)
* **NXDOMAIN Responses:** 0
* **Peak Queries in Window:** 3
* **Review Status:** `No multi-indicator review condition met.`
* **Analyst Assessment:** Quiet client exhibiting standard API and mail server resolution traffic.

---

## 4. Analytical Limitations & Caveats
In accordance with case context boundaries, analysts must remember:
1. **Heuristic Nature:** Flagged findings represent behavioral heuristics, not confirmed malware or data exfiltration.
2. **Synthetic Data:** Telemetry was artificially generated for educational training and does not reflect live enterprise infrastructure.
3. **Context Dependency:** Resolution metrics alone are insufficient; findings must be correlated with EDR endpoint telemetry and local network baselines before escalation.

---

## 5. Recommendations
* **Baseline Tuning:** Verify whether client `192.0.2.25` hosts a scheduled application monitoring script or health-check utility.
* **Correlative Logging:** Cross-reference DNS timestamps with process execution logs (Sysmon / EDR) on the host to confirm process legitimacy.
* **Signal Optimization:** Retain multi-indicator correlation rules in SIEM deployments to prevent alert fatigue while catching anomalous network behavior.
