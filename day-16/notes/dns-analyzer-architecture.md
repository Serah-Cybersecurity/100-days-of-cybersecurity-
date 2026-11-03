# Architectural Design & Implementation Notes: DNS Analyzer

**Author:** Serah Mulwa    
**Date:** November 3, 2026  
**Module:** Day 16 - DNS Security, Investigation, and Threat Detection  

---

## 1. Overview & Purpose
When building security automation tools in Python, writing functional code is only half the battle. As a security engineer, understanding *why* specific design choices were made is what separates a novice script from a production-grade utility. This document breaks down the key architectural decisions embedded inside `dns_analyzer.py`.

---

## 2. Key Architectural Decisions

### 2.1 Timestamp Normalization & UTC Conversion
* **The Mechanism:** Raw ISO 8601 strings from logs are parsed using `datetime.fromisoformat()` and explicitly converted to Coordinated Universal Time (UTC) using `.astimezone(timezone.utc)`.
* **The Rationale:** Enterprise networks span multiple time zones. Correlating logs from servers in Nairobi (`UTC+3`), London (`UTC+0`), and New York (`UTC-5`) requires a unified temporal baseline. Normalizing to UTC prevents forensic timeline misalignments during incident triage.

### 2.2 Strict IP Address Hygiene (`ipaddress`)
* **The Mechanism:** Client IP fields are passed through Python's native `ipaddress.ip_address()` module.
* **The Rationale:** This is a data sanitization and hygiene step. It ensures that malformed logs, script injection attempts, or corrupt characters do not break the grouping logic. *Note:* IP syntax validation does not verify device ownership, physical location, or malicious intent—it simply ensures structural integrity.

### 2.3 RFC-Compliant Query Name Validation (`validate_query_name`)
* **The Mechanism:** Domain names are checked against IETF standards (RFC 1035), verifying that total length does not exceed 253 characters and that individual dot-delimited labels do not exceed 63 characters.
* **The Rationale:** Attackers utilizing DNS tunneling often inject raw binary or heavily encoded strings into subdomains. Rigorous query validation ensures our script fails safely or logs warnings rather than crashing on anomalous input.

### 2.4 Sliding-Window Peak Query Frequency (`peak_queries`)
* **The Mechanism:** Uses a two-pointer sliding window algorithm over sorted chronological timestamps to calculate the highest request volume within any rolling 10-minute window.
* **The Rationale:** Traditional calendar-hour counters miss bursty activity. Sliding windows capture rapid-fire anomaly bursts (such as malware beaconing every 60 seconds or automated scanning scripts), mirroring how enterprise SIEM platforms detect threshold violations.

### 2.5 TXT Proportions & Error Ratios
* **The Mechanism:** Computes the ratio of `TXT` queries and `NXDOMAIN` error responses relative to total query volume.
* **The Rationale:** Neither TXT records nor NXDOMAIN errors are inherently malicious. However, calculating their statistical proportions allows an analyst to benchmark a client's behavior against normal network baselines.

### 2.6 Multi-Indicator Heuristic Flagging
* **The Mechanism:** The tool evaluates four distinct indicators (high frequency, long names, high TXT ratio, and NXDOMAIN spikes) and flags a client *only* if **at least two indicators are present simultaneously**.
* **The Rationale:** Single-indicator alerts generate catastrophic alert fatigue in SOC environments. Requiring concurrent behavioral signals dramatically improves the signal-to-noise ratio, though analysts must still investigate flagged hosts manually to rule out false positives.
