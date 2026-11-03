# DNS Security & Detection Engineering
**Author:** Serah Mulwa  
**Date:** November 3, 2026  
**Module:** Day 16 - DNS Security, Investigation, and Threat Detection  

---

## 1. Overview & Purpose
While previous sections covered DNS fundamentals, troubleshooting, and packet capture analysis, this module shifts into **Detection Engineering**. As a junior SOC analyst, understanding how attackers abuse DNS allows you to build robust heuristics, write effective SIEM alert rules, and minimize false positives.

---

## 2. DNS Anomaly Indicators
Attackers target DNS because **Port 53 traffic is rarely blocked** by corporate firewalls. Unusual deviations from normal baseline behavior serve as primary investigative triggers:

| DNS Indicator | Observable Pattern | Possible Investigative Significance |
| :--- | :--- | :--- |
| **High Request Volume** | Thousands of queries from a single client IP in minutes. | Malware beaconing, automated scripts, or application looping. |
| **High Unique Subdomains** | Numerous queries to randomized subdomains (`xyz123.malicious.com`). | Domain Generation Algorithms (DGA) used by ransomware and C2 frameworks. |
| **Unusually Long Query Names** | Subdomain strings exceeding 60–100 characters. | Non-standard protocol usage or **DNS Tunnelling** (data exfiltration). |
| **High TXT-Query Concentration** | Heavy volume of TXT record requests from an endpoint. | Protocol abuse or data encoding within text fields. |
| **Repeated `NXDOMAIN` Responses** | Spikes in non-existent domain error codes. | Host reconnaissance or DGA malware searching for active C2 servers. |
| **Unusual Query Timing** | Periodic queries firing at exact intervals (e.g., every 60 seconds). | Automated C2 check-in beaconing. |

---

## 3. DNS Tunnelling & MITRE ATT&CK `T1071.004`
* **What it is:** Encapsulating non-DNS traffic (such as command-and-control payloads or stolen file data) inside standard DNS query and response subdomains.
* **MITRE ATT&CK Mapping:** Classified under **T1071.004 (Application Layer Protocol: DNS)**.
* **Detection Challenge:** Because resolvers forward recursive queries, malicious traffic blends easily with normal web traffic unless analyzed at scale.

---

## 4. Managing False Positives & Alert Fatigue
A major trap for junior analysts is treating every anomaly as a confirmed compromise. Legitimate services frequently trigger similar patterns:
* **Cloudflare / AWS APIs:** Utilize long cryptographic subdomains for telemetry.
* **CDNs:** Use dynamic routing tokens.
* **Email Security:** Routine DMARC/SPF checks generate heavy TXT query volumes.

**Best Practice:** Never build detection alerts on a single indicator. Combine multiple signals (e.g., high query frequency + long query names + high TXT ratio) into a compound rule.

---

## 5. Building a Detection Hypothesis
Before deploying detection logic in a SIEM, analysts formulate a clear detection hypothesis:

> **Hypothesis:** *"Identify internal clients exhibiting an unusual combination of high DNS request frequency, unusually long query names, and a high proportion of TXT queries, then flag them for human review."*

This behavioral heuristic approach outperforms static signatures, which fail against rapidly mutating malware.
