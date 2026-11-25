# Technical Note: Integrated Network Threat Hunting & Cross-Tool Architecture

**Author:** Serah Mulwa  
**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering  

## 1. Executive Summary

In enterprise Security Operations Centers (SOCs), relying on a single defensive tool creates dangerous operational blind spots. Signature-based Intrusion Detection Systems (IDS) like Suricata excel at triggering immediate alerts on known threat patterns, but they lack broad session context. Conversely, Network Security Monitoring (NSM) platforms like Zeek extract rich, stateful connection and protocol metadata, but do not generate traditional rule-based alerts out of the box.

This technical note documents the design and conceptual architecture of an **Integrated Threat Hunting Pipeline**. By combining Suricata detection alerts, Zeek session logs, and standardized **Community ID** flow hashing, security analysts can automate log normalization, perform rapid event correlation, and validate threat hypotheses across disparate telemetry sources.

## 2. Tool Capabilities & Comparative Matrix

To build an effective threat-hunting workflow, defenders must understand what each tool contributes to an investigation:

| Security Tool | Primary Role | Output Format | Investigative Strengths | Limitations |
| :--- | :--- | :--- | :--- | :--- |
| **Suricata** | Signature-based IDS / IPS | EVE JSON (`eve.json`) | Immediate pattern-matching alerts, signature rule matches, PCAP extraction hints. | Lacks comprehensive stateful connection logs for benign background traffic. |
| **Zeek** | Stateful Network Security Monitor | Structured JSON / Tab-delimited (`conn.log`, `dns.log`, `ssl.log`) | Deep protocol parsing, long-term session tracking, cross-log correlation via UIDs. | Does not natively output signature alert severity levels without custom scripting. |
| **Wireshark / tcpdump** | Deep Packet Inspection (DPI) | Raw PCAP (`.pcap`) | Full payload access, bit-level frame inspection, manual forensic validation. | High storage footprint; unscalable for real-time enterprise monitoring. |
| **Python Automation** | Telemetry Correlation & Normalization | Formatted JSON / Terminal Reports | Data normalization, cross-tool Community ID hashing, automated triage pipelines. | Dependent on clean input logs; non-real-time unless deployed as a service. |

## 3. The Integrated Monitoring & Correlation Pipeline

An enterprise-grade threat hunt follows a structured data pipeline that transforms raw network packets into actionable forensic timelines:

```text
                  AUTHORISED NETWORK TRAFFIC
                              │
                              ▼
                        PCAP CAPTURE
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                SURICATA               ZEEK
                    │                   │
                    ▼                   ▼
                EVE JSON           CONN / DNS / SSL
                    │                   │
                    └─────────┬─────────┘
                              ▼
                        NORMALISATION
                              │
                              ▼
                         CORRELATION (via Community ID)
                              │
                              ▼
                    INVESTIGATION TIMELINE
                              │
                              ▼
                     PYTHON AUTOMATION SCRIPT
                              │
                              ▼
                        ANALYST REVIEW
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
         Benign / Expected           Needs Escalation
                │                           │
                ▼                           ▼
          Document Evidence          Escalate via Playbook
```

### Pipeline Execution Stages:

1. **Traffic Capture:** Raw packets are ingested live from network taps or loaded offline from `.pcap` files.
2. **Dual-Engine Processing:** 
   * **Suricata** evaluates packets against signature rules (e.g., Emerging Threats rulesets) and writes alerts to `eve.json`.
   * **Zeek** dissects protocols statefully, populating `conn.log`, `dns.log`, and `ssl.log`.
3. **Data Normalization:** A Python script or SIEM normalizes timestamps, IP address representations, and protocol names into a common schema.
4. **Cross-Tool Correlation:** Matching records across tools using the standardized **Community ID** flow hash.
5. **Timeline Assembly:** Reconstructing network events chronologically (`Suricata Alert` $\rightarrow$ `Zeek DNS Query` $\rightarrow$ `Zeek Transport Flow`).
6. **Analyst Review:** Evaluating findings to distinguish expected benign behavior from true security incidents.

## 4. The Power of Community ID Standardisation

### The Correlation Challenge
Traditionally, linking an alert from Suricata to a session in Zeek required matching five separate transport fields: `Source IP`, `Source Port`, `Destination IP`, `Destination Port`, and `Protocol`. Because different tools format these 5-tuples differently—or represent protocol names as numbers versus strings—programmatic correlation was fragile and slow.

### The Community ID Solution
Developed as an open standard by Corelight, **Community ID** is a canonical flow hashing algorithm. It takes a network flow's 5-tuple, computes a SHA-1 digest, and outputs a uniform base64-encoded string prefixed by a version flag (e.g., `1:L26St...`).

$$\text{Community ID} = \text{Base64}\Big(\text{SHA-1}\big(\text{Seed} \parallel \text{IP}_{\text{src}} \parallel \text{IP}_{\text{dst}} \parallel \text{Proto} \parallel \text{Port}_{\text{src}} \parallel \text{Port}_{\text{dst}}\big)\Big)$$

* When **Suricata** fires an alert on a malicious packet, it embeds `"community_id": "1:..."` inside `eve.json`.
* When **Zeek** processes the exact same flow, its `community_id` package embeds `"community_id": "1:..."` inside `conn.log`.
* **Analyst Impact:** Triage scripts can instantly execute `select(community_id == X)` to retrieve both the signature alert and the full connection metadata in a single query.

## 5. Key Portfolio & SOC Takeaways

* **Correlation provides context:** A Suricata alert indicates *that* a rule fired; Zeek telemetry reveals *what happened next* across the network session.
* **Community ID bridges tool silos:** Using a standardized flow hash turns disparate log outputs into a unified relational database structure.
* **Proactive hunting over reactive alerting:** Integrating tools enables security analysts to pivot from known indicators to baseline anomalies, identifying advanced threats that bypass standard signatures.
