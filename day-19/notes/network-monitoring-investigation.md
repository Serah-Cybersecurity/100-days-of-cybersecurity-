# Technical Note: Proactive Network Threat Hunting & Baselining Methodologies

**Author:** Serah Mulwa

**Module:** Day 19 - Network Threat Hunting with Zeek

## 1. Executive Summary

In enterprise defensive security, reactive alerting is only half the battle. While signature-based systems (like Suricata) alert analysts to known threat patterns, sophisticated adversaries frequently evade static rules by utilizing novel staging techniques, encrypted channels, or living-off-the-land binaries.

**Network threat hunting** is the proactive, human-driven process of searching through network telemetry (Zeek logs, connection flows, and protocol metadata) to uncover hidden threats that have bypassed automated alarms. This technical note explores baseline establishment, the 8 core threat hunting categories, and structured investigation workflows.

## 2. Establishing the Network Baseline

Before an analyst can effectively spot malicious anomalies, they must understand what normal activity looks like in their specific environment.

### 2.1 Defining the Baseline

A network baseline documents expected operational patterns over defined timeframes:

* **Authorized Infrastructure:** Knowing which internal servers are permitted to talk to external DNS resolvers versus internal domain controllers.

* **Expected Service Protocols:** Standard workstations utilize HTTPS (port 443) and DNS (port 53); internal servers utilize SSH (port 22) or RDP (port 3389).

* **Traffic Volume Profiles:** Typical daily byte counts, packet counts, and connection durations for endpoints.

### 2.2 The Fallacy of Blind Thresholds

A common beginner mistake is copying detection thresholds directly from internet tutorials (e.g., *"Alert if an endpoint makes more than 50 DNS queries in one minute"*). 

In modern corporate environments, web browsers loading media-rich dashboards or developer microservices can easily generate hundreds of queries in seconds. Professional detection engineers and threat hunters **always justify detection thresholds using empirical environmental context**, avoiding alert fatigue.

## 3. The 8 Core Threat Hunting Categories

When conducting an open-ended hunt across Zeek log datasets, analysts structure their investigations across 8 fundamental vectors:

| Hunt Category | Investigation Question | Indicators of Anomalous Behavior | 
| ----- | ----- | ----- | 
| **1. Connection Volume** | Which endpoint has the most observed connections? | A workstation communicating with hundreds of unique external IPs in minutes (port scanning or C2 beaconing). | 
| **2. Destination Ports** | Which destination ports appear most frequently? | Non-standard service ports (e.g., SSH running over port 8080 or management shells on ephemeral ports). | 
| **3. DNS Activity** | Which domain names are most common? | High-entropy domain strings, DGA patterns, or heavy traffic to newly registered TLDs. | 
| **4. DNS Failures** | Which requests received unsuccessful responses? | Spikes in `NXDOMAIN` (Non-Existent Domain) responses indicating DGA malware cycling through dead C2 servers. | 
| **5. TLS Versions** | Which TLS versions are present in the sample? | Outdated legacy protocols (`TLSv1.0`, `TLSv1.1`, `SSLv3`) lacking modern security controls. | 
| **6. Connection State** | Are there incomplete or rejected connections? | High volumes of `S0` (SYN sent, no reply) or `REJ` (Connection rejected) states from an internal host. | 
| **7. Transfer Volume** | Which connections transferred comparatively large amounts of data? | Imbalanced byte ratios where `orig_bytes` (upload) vastly exceeds `resp_bytes` (download) on external flows. | 
| **8. Service Diversity** | Which protocols or application services were identified? | Mismatched application traffic (Dynamic Protocol Detection showing HTTP running over port 443). | 

## 4. Practical Hunt Workflow

When analyzing Zeek datasets in lab or production environments, follow this repeatable 4-step methodology:

1. **Formulate a Hypothesis:** State a testable assumption (e.g., *"An infected workstation inside our subnet is beaconing to an external Command & Control server every 60 seconds"*).

2. **Query and Pivot:** Use command-line tools (`awk`, `sort`, `uniq`) or SIEM search languages to isolate anomalies in `conn.log` or `dns.log`.

3. **Contextualize and Correlate:** Take suspicious IPs or session UIDs and pivot across protocol logs (`ssl.log`, `http.log`) to evaluate certificates, User-Agents, and domain histories.

4. **Document and Report:** Record findings, separate true positives from administrative false positives, and compile actionable investigation notes.

## 5. Key Takeaways

* **Threat hunting starts with questions, not answers:** Hunts are exploratory investigations driven by curiosity and baselining.

* **Context is king:** Always verify whether an unusual traffic spike is a legitimate business process (such as a database backup) before escalating.

* **Combine telemetry sources:** Effective threat hunters never rely on a single log file; they correlate connection states, DNS lookups, and TLS metadata to establish undeniable proof.
