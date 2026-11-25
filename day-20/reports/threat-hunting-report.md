# Day 20 Incident Investigation & Correlation Report: Multi-Tool Telemetry Pivoting

**Analyst:** Serah Mulwa  
**Lab Context:** Day 20 - Integrated Network Threat Hunting & Detection Engineering  
**Primary Dataset:** `pcap/day20.pcap`  

---

## 1. Executive Summary

This report documents the manual cross-tool correlation and investigation of network events captured in `day20.pcap`. By standardizing flow hashing via **Community ID** across Suricata (Intrusion Detection System) and Zeek (Network Security Monitoring), alerts were mapped to network metadata without relying on manual timestamp matching or complex multi-field database queries.

Using the extracted Community ID hash, Suricata signature detections were linked directly to Zeek connection records (`conn.log`). Subsequently, Zeek's internal transaction ID (`uid`) was leveraged to pivot into application-layer protocol logs (`dns.log`), reconstructing the full investigative chain of evidence.

---

## 2. CLI Workflow & Manual Pivoting Steps

### Step 1: Suricata Community ID Extraction
The Suricata EVE JSON output was queried using `jq` to extract alerts and their corresponding Community ID strings:

```bash
jq -r 'select(.event_type == "alert") | .community_id // empty' output/suricata/eve.json
```

* **Extracted Hash Sample:** `1:qQZURsTvB7+LXx5x83z0/KkPQA=`

### Step 2: Cross-Tool Lookup in Zeek (`conn.log`)
The extracted hash string was searched across Zeek connection logs using `grep` to verify matching 5-tuples:

```bash
grep -F '1:qQZURsTvB7+LXx5x83z0/KkPQA=' output/zeek/conn.log
```

* **Correlation Result:** Match confirmed. Both tools independently generated identical flow hashes for the same underlying network stream.

### Step 3: Zeek UID Extraction
From the matching connection record, the Zeek-specific transaction ID was isolated:

```bash
jq -r 'select(.community_id != null) | .uid' output/zeek/conn.log | head -n 1
```

* **Extracted Zeek UID:** `CUpfru4e9q1UHG9Axi`

### Step 4: Protocol Pivoting into `dns.log`
Using the extracted Zeek UID, protocol-specific telemetry was retrieved to inspect application layer payload details:

```bash
grep -F 'CUpfru4e9q1UHG9Axi' output/zeek/dns.log
```

* **Extracted Details:** Confirmed DNS query and response transactions for target host lookup (`2.debian.pool.ntp.org`).

---

## 3. Mandatory Investigative Analysis

### 1. Did Suricata produce the expected alert?
**Yes.** The custom signature rule (`sid:1000001`) fired successfully upon processing the target DNS traffic in `day20.pcap`.

### 2. Did the alert contain Community ID?
**Yes.** Explicitly enabling `community-id: true` and setting `community-id-seed: 0` under the `eve-log` block in `config/suricata-day20.yaml` ensured every alert record was populated with a `community_id` field.

### 3. Did Zeek record the corresponding connection?
**Yes.** Zeek’s `conn.log` captured the identical UDP connection tuple (`10.0.2.15:48359` $\to$ `192.168.100.1:53`).

### 4. Did both tools generate the same Community ID?
**Yes.** Both Suricata and Zeek were executed against the exact same trace file (`day20.pcap`) with identical seed parameters (`seed: 0`), resulting in the identical hash string (`1:qQZURsTvB7+LXx5x83z0/KkPQA=`).

### 5. What Zeek UID was associated with the connection?
**`CUpfru4e9q1UHG9Axi`**

### 6. Was there a related DNS record?
**Yes.** Pivoting via UID `CUpfru4e9q1UHG9Axi` into `dns.log` revealed the complete query/response transaction including transaction ID, query domain (`2.debian.pool.ntp.org`), record types (`A` / `AAAA`), and returned IP answers.

### 7. Were the timestamps consistent?
**Yes.** Timestamps recorded across Suricata `eve.json` and Zeek `conn.log`/`dns.log` aligned perfectly within the packet capture window.

### 8. What does the evidence establish?
The evidence conclusively proves that internal host `10.0.2.15` generated outbound DNS resolution requests to local gateway `192.168.100.1`, triggering Suricata signature rules while simultaneously capturing complete session state and application-layer metadata in Zeek.

### 9. What does the evidence not establish?
The network telemetry alone does not establish the intent of the process initiating the connection, whether the query was initiated by a legitimate system daemon or malicious software, or host-level details such as process names, parent PIDs, or user accounts. Host-based telemetry (e.g., Sysmon or auditd) would be required to establish host context.

---

## 4. Key Portfolio Takeaways & Core Analyst Principles

* **Community ID Correlates Multi-Vendor Tools:** Use Community ID flow hashes to bridge independent detection engines and telemetry platforms (Suricata $\to$ Zeek $\to$ SIEM).
* **Zeek UID Correlates Internal Log Streams:** Use Zeek UIDs to pivot across internal log boundaries (Connection `conn.log` $\to$ Protocol `dns.log` / `ssl.log` / `http.log`).
* **Evidence Hygiene:** Maintain rigid path control and consistent script configuration (`seed = 0`) to guarantee deterministic analysis results.
