# Technical Note: Professional Detection Engineering Habits & Operational Standards

**Author:** Serah Mulwa    
**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering  

---

## 1. Executive Summary

Executing detection tools like Suricata and Zeek is only the technical foundation of network defense. What separates a junior analyst running scripts from an elite detection engineer is an unwavering commitment to data hygiene, systematic verification, contextual analysis, and rigorous documentation standards.

This technical note documents the five core operational habits governing professional detection engineering and threat hunting workflows developed during Day 20.

---

## 2. The Five Core Detection Engineering Habits

### 2.1 Always Understand the Data Source
Before evaluating any alert or log entry, an analyst must establish the technical boundaries of the sensor that captured it.

* **Sensor Identity & Placement:** Identify whether the log originated from a perimeter gateway, internal SPAN/TAP, host-based socket, or cloud VPC mirror.
* **Visibility Scope:** Determine what traffic the sensor was physically capable of observing and verify whether inline devices (firewalls, proxies) dropped packets prior to sensor inspection.
* **Telemetry Integrity:** Check for interface packet drops, NIC ring buffer overflows, asymmetric routing anomalies, and Network Time Protocol (NTP) clock skew between sensors.

> *Core Rule:* A security engine cannot analyze network traffic it never received.

### 2.2 Do Not Confuse Alert Volume with Security Quality
High alert volume is frequently an indicator of poor detection tuning rather than robust security posture.

* **Alert Fatigue Mitigation:** Flooding Security Operations Center (SOC) dashboards with thousands of unrefined, low-fidelity alerts degrades operational focus and inflates Mean Time to Respond (MTTR).
* **Fidelity Over Quantity:** Engineering efforts must prioritize high-confidence, actionable rules that minimize false positives and provide clear context for incident response.

### 2.3 Never Interpret a Single Field in Isolation
Isolated data fields are context-free metrics. Drawing definitive conclusions from single log attributes leads to incorrect incident classification.

* **Destination Port 443:** Port 443 does not guarantee TLS/HTTPS protocol compliance; non-web protocols and C2 tools frequently utilize port 443 to bypass naive egress filters.
* **High Byte Volume:** Large session transfer values (`bytes_toserver` / `bytes_toclient`) indicate data movement but do not establish data exfiltration without user, process, and endpoint context.
* **Unsuccessful DNS Codes (`NXDOMAIN`):** Failed domain lookups routinely occur due to mistyped URLs, stale browser caches, or harmless application checks, and must not be declared malicious without frequency analysis or endpoint process lineage.
* **Signature Rule Fires:** A Suricata alert confirms pattern matching against a rule definition; it does not inherently prove system compromise.

### 2.4 Maintain Systematic Detection Documentation
Every enterprise detection rule must be accompanied by comprehensive lifecycle documentation. A standardized rule specification must include:

1. **Name & Purpose:** Clear title and underlying defensive objective.
2. **Rule Identifier:** Unique ID and revision number (`sid`, `rev`).
3. **Data Sources & Fields:** Required sensor logs and key fields evaluated (`community_id`, `dns.query`).
4. **Detection Logic:** Explicit rule syntax, regex patterns, or threshold parameters.
5. **False-Positive Considerations:** Documented benign activities known to trigger the rule.
6. **Known Limitations:** Boundary conditions where detection fails (e.g., Encrypted DNS / DoH).
7. **Validation Evidence:** Execution proof, PCAP traces, and test output verification.

### 2.5 Preserve Repeatability & Forensic Reproducibility
An investigation or automation deliverable is only as valid as its reproducibility. Every technical step must enable an independent analyst to replicate identical results.

* **Environment Specification:** Document exact software build versions (Suricata 7.0.10, Zeek 9.0.1, Python 3.11+).
* **Telemetry Control:** Record exact PCAP filenames (`day20.pcap`), capture parameters, and isolated configuration files (`suricata-day20.yaml`, `community_id.zeek`).
* **Execution Hygiene:** Track exact CLI invocation paths, input flags, script parameters (`--window-seconds`), and output file structures.

---

## 3. Portfolio Execution Checklist

| Requirement | Implementation Artifact | Operational Purpose |
| :--- | :--- | :--- |
| Data Normalization | `notes/normalisation-schema.md` | Maps vendor keys (Suricata/Zeek) to standard ECS subset fields. |
| Automation Engine | `scripts/cross_tool_correlator.py` | Enforces multi-factor validation (Hash, 5-Tuple, Timestamp, UID). |
| Threat Hunting | `notes/hunting-worksheet.md` | Executes hypothesis-driven searches across DNS and TLS logs. |
| Attack Mapping | `notes/detection-mapping.md` | Evaluates telemetry data components against MITRE ATT&CK. |
| Incident Report | `reports/day20-threat-hunting-report.md` | Documents multi-tool correlation evidence and investigative QA. |
| Timeline Analysis | `reports/investigation-timeline.md` | Maps chronological event flow with analytical limitation bounds. |
