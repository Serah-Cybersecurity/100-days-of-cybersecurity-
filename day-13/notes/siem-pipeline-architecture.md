# Day 13 - SIEM Data Pipeline Architecture & Documentation Standards

* **Author:** Serah Mulwa  
* **Date:** October 31, 2026  
* **Module:** SIEM Fundamentals & Log Engineering  

---

## 1. Executive Overview: The 11-Stage Data Pipeline

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│  1. GENERATION  │───>│ 2. COLLECTION│───>│  3. INGESTION   │───>│ 4. PARSING &    │───>│ 5. NORMALIZATION │
│  (Windows/Linux)│    │  (Forwarder) │    │(SIEM Indexer)   │    │    EXTRACTION   │    │      (CIM)       │
└─────────────────┘    └──────────────┘    └─────────────────┘    └─────────────────┘    └────────┬─────────┘
                                                                                                  │
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│11. TRIAGE & IR  │<───│  10. ALERT   │<───│ 9. DETECTION    │<───│ 8. SEARCH &     │<──────────────┘
│  (Human Review) │    │ GENERATION   │    │    RULES        │    │    ANALYSIS     │
└─────────────────┘    └──────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 2. Log Source Architecture

### Host-Centric vs. Network-Centric Telemetry
* **Host-Centric Sources:** Windows Security/System/PowerShell logs (`.evtx`), Linux auth logs (`/var/log/auth.log`), EDR telemetry. Focuses on internal execution and authentication context.
* **Network-Centric Sources:** Perimeter firewalls, core routers, VPN gateways, DNS servers, Web Proxies. Focuses on communication boundaries and external connections.
* **Combined Value:** Host telemetry identifies *what process ran*, while network telemetry identifies *where data was sent*.

---

## 3. Data Pipeline Stages Breakdown

### 3.1 Log Collection & Agents
* **Agents/Forwarders:** Lightweight endpoints (e.g., Splunk Universal Forwarder, Elastic Agent) that encrypt and stream events across port `9997` or `514`.
* **Syslog & APIs:** Direct streaming for network appliances and API polling for cloud environments (AWS CloudTrail, Entra ID).

### 3.2 Ingestion & Monitoring Gaps
* **The Ingestion Axiom:** A SIEM can only analyze the data it receives. A clean dashboard may indicate a broken forwarder rather than a secure network.

### 3.3 Parsing (Raw Text to Extracted Fields)
Transforms raw text strings into searchable key-value pairs using regular expressions:
```text
Raw: Oct 31 09:12:03 server01 sshd[2201]: Failed password for analyst from 198.51.100.27 port 50135 ssh2
Parsed -> _time: Oct 31 09:12:03 | host: server01 | process: sshd | user: analyst | src_ip: 198.51.100.27 | result: Failed
```

### 3.4 Normalization (Common Information Model / CIM)
Maps disparate vendor schemas into standardized parameters:
* Windows `TargetUserName` + Linux `username` ──> Normalized `user`
* Windows `IpAddress` + Firewall `src` ──> Normalized `src_ip`

### 3.5 Enrichment
Appends metadata context: Asset Criticality, Network Segment, Owner, GeoIP reputation, and Threat Intel flags.

### 3.6 Storage & Indexing Terms (Splunk)
* **Index:** Logical database storage container on disk (`index=security`).
* **Source:** File or stream origin (`C:\Windows\System32\Winevt\Logs\Security.evtx`).
* **Sourcetype:** Format classification driving parser logic (`sourcetype=WinEventLog:Security`).
* **Host:** Hostname or IP of originating endpoint (`host=HR_02`).
* **`_time`:** Normalized UTC event timestamp.

---

## 4. Architectural Documentation Standards

When documenting enterprise SIEM architecture, an analyst must record:

1. **Pipeline Bottlenecks:**
   * Document log sources experiencing ingestion latency ($\Delta t > 60\text{s}$) or dropped packets.
   * Track forwarder connection drops, network queue saturations, and CPU throttling.

2. **Parsing Failures:**
   * Audit unparsed event streams routed to fallback sourcetypes (e.g., `sourcetype=sourcetype:unparsed` or `_raw` extraction errors).
   * Document broken Regex patterns following vendor software updates.

3. **Index Routing Map:**
   * Maintain an explicit record mapping log streams to storage indexes for compliance and retention policies:
     * `index=windows` (Retention: 90 days)
     * `index=firewall` (Retention: 180 days)
     * `index=pci_compliance` (Retention: 365 days)

---

## 5. Core Analyst Axioms

> 💡 **Axiom 1:** *Absence of alerts is not evidence of security; verify ingestion status first.*  
> 💡 **Axiom 2:** *Normalization enables universal threat hunting across operating systems.*  
> 💡 **Axiom 3:** *Unparsed logs consume storage budget without providing investigative value.*
