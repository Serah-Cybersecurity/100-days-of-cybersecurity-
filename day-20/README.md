# Day 20: Integrated Network Threat Hunting & Detection Engineering

**Author:** Serah Mulwa  
**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering  

---

## Overview

This project demonstrates an advanced cross-tool network threat hunting and telemetry correlation workflow. By analyzing raw network packet captures using both **Suricata** (signature-based Intrusion Detection System) and **Zeek** (Network Security Monitoring framework), this project bridges the gap between static signature alerts and deep application-layer protocol metadata.

By integrating **Community ID** flow hashing across both detection engines, independent log streams are cryptographically bound, allowing automated multi-factor correlation, log pivoting via **Zeek UIDs**, data normalization, and hypothesis-driven threat hunting.

---

## Objectives

1. **Dual-Engine Execution:** Process an identical authorized PCAP (`day20.pcap`) through Suricata and Zeek simultaneously in isolated environments.
2. **Flow Standardization:** Configure deterministically seeded (`seed: 0`) Community ID generation in both engines (`suricata-day20.yaml` and `community_id.zeek`).
3. **Cross-Tool Correlation:** Execute manual (`jq`, `grep`) and automated (Python) cross-tool correlation matching 5-tuple network flows.
4. **Log Pivoting:** Leverage unique Zeek session identifiers (`uid`) to pivot from TCP/UDP connection state records (`conn.log`) directly into application-layer DNS transactions (`dns.log`) and TLS metadata (`ssl.log`).
5. **Data Normalization:** Structure raw telemetry into an educational subset of the **Elastic Common Schema (ECS)**.
6. **Automation Engineering:** Build a multi-factor Python correlation engine (`cross_tool_correlator.py`) supporting transport validation, bi-directional endpoint verification, configurable timestamp windowing (`--window-seconds`), and UID context expansion.
7. **Chronological Analysis:** Reconstruct a verified, microsecond-accurate network investigation timeline and formal threat hunting report.

---

## Technical Stack & Tooling

| Category | Tool / Platform | Deployment Context & Function |
| :--- | :--- | :--- |
| **Operating System** | Parrot Security OS | Isolated Linux analysis workstation |
| **Detection Engine** | Suricata `v7.0.10` | Signature-based packet inspection & EVE JSON alert logging |
| **NSM Framework** | Zeek `v9.0.1` | Network protocol metadata generation (`conn.log`, `dns.log`, `ssl.log`) |
| **Packet Capture** | Wireshark / `tcpdump` | Offline PCAP creation, verification, and packet frame inspection |
| **Automation Language** | Python `v3.11+` | Custom multi-factor log correlation engine script |
| **CLI Utilities** | `jq`, `grep`, `gawk` | Command-line JSON parsing, filtering, and string extraction |
| **Version Control** | Git / GitHub | Portfolio documentation and code repository management |

---

## Methodology

### 1. Hypothesis Formulation
The investigation operates on the hypothesis that when Suricata fires a signature alert for a target domain query (`sid:1000001`), Zeek independently records the underlying connection parameters (`conn.log`) and DNS protocol metadata (`dns.log`) under the exact same Community ID flow hash.

### 2. Telemetry Ingestion & Seed Alignment
* **Suricata Configuration:** `config/suricata-day20.yaml` configured with `community-id: true` and `community-id-seed: 0`.
* **Zeek Script Configuration:** `scripts/community_id.zeek` configured with `@load policy/protocols/conn/community-id-logging` and `redef CommunityID::seed = 0;`.
* **Execution:** Both tools processed `pcap/day20.pcap`, outputting structured JSON logs to isolated directories (`output/suricata/` and `output/zeek/`).

### 3. Multi-Factor Correlation & Validation Pipeline
Rather than blindly joining logs on hash values alone, the correlation method enforces a 5-stage validation pipeline implemented in Python (`scripts/cross_tool_correlator.py`):

$$\text{Telemetry Input} \longrightarrow \text{Hash Match} \longrightarrow \text{Protocol Check} \longrightarrow \text{Bi-directional Endpoint Match} \longrightarrow \text{Timestamp Window Tolerance} \longrightarrow \text{UID Pivoting}$$

1. **Hash Verification:** Primary lookup matching Suricata `community_id` to Zeek `conn.log` `community_id`.
2. **Protocol Parity:** Enforces transport protocol equivalence (TCP $\leftrightarrow$ TCP, UDP $\leftrightarrow$ UDP).
3. **Bi-directional Endpoint Match:** Validates $(SrcIP, SrcPort) \leftrightarrow (DstIP, DstPort)$ regardless of reported flow direction.
4. **Timestamp Delta Verification:** Verifies $|TS_{\text{Suricata}} - TS_{\text{Zeek}}| \le \text{window\_seconds}$.
5. **Context Expansion:** Pivots via Zeek `uid` to pull associated `dns.log` query/answer records and `ssl.log` SNI parameters.

---

## Results & Findings

### Summary Execution Metrics

```text
==========================================================
      DAY 20: INTEGRATED THREAT HUNTING CORRELATION REPORT 
==========================================================
[*] Suricata Total Records Parsed : 74 (Malformed: 0)
[*] Suricata Alerts Identified    : 4
[*] Zeek Connection Records       : 10 (Malformed: 0)
[*] Zeek DNS Records Loaded       : 12
[*] Zeek TLS/SSL Records Loaded   : 1
[*] Configured Time Window        : 30.0 seconds
----------------------------------------------------------
[+] Successfully Correlated Matches : 4
[-] Validation / Correlation Failures: 0
==========================================================
```

### Key Correlator Matches

* **Match #1:** Suricata alert `[1000001] LOCAL LAB DNS query for example.com` matched Zeek session `CMNhdPSs13bACnDRh` via Community ID `1:qQZURsTvB7+LXx5x83z0/KkPQA=`. Pivoting into `dns.log` revealed `AAAA` query for `example.com` returning IPv6 addresses (`2606:4700:10::ac42:93f3`, `2606:4700:10::6814:179a`).
* **Match #2:** Suricata alert matched Zeek session `Cwm0RP3YRwEK1TkZrd` via Community ID `1:P2oNim+dAcDZgQht0+q2HlbuHXU=`. Pivoting into `dns.log` revealed `A` query for `example.com` returning IPv4 answers (`172.66.147.243`, `104.20.23.154`).
* **Microsecond Timestamp Parity:** Alerts and connection start times aligned precisely within sub-second thresholds across testing windows (`0.1s`, `30s`, `300s`).

---

## Limitations

1. **5-Tuple Hash Collision Risk:** Community ID hashes do not incorporate timestamps. Re-used ephemeral ports across long timeframes generate identical hashes; timestamp windowing (`--window-seconds`) is strictly required to prevent false joins.
2. **Encryption Blindspots:** TLS 1.3 encryption conceals application payloads and HTTP URIs. Sensor visibility is restricted to handshake metadata (`ssl.log` SNI, ciphers, certificates).
3. **Absence of Host Context:** Network telemetry proves packet transmission, but cannot identify host process IDs (PIDs), parent process trees, user account context, or local disk execution without host EDR/Sysmon integration.
4. **Resolution vs. Connection:** Observing a successful DNS query does not guarantee that the host subsequently established an active TCP/UDP application session with the returned IP addresses.

---

## Safety and Scope

* **Authorized Environment:** All network packet captures, log datasets, and script executions were performed strictly within an authorized, isolated laboratory environment on Parrot OS.
* **Benign Testing Signature:** The Suricata alert rule (`sid:1000001`) utilized during this project is a benign local test rule designed to detect DNS lookups for `example.com`.
* **Evidentiary Integrity:** The generation of signature alerts and DNS telemetry in this lab demonstrates sensor capabilities and correlation workflows; it does not indicate malicious activity or system compromise.
