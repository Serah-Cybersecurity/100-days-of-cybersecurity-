# Day 15 - Correlating Network PCAPs with SIEM & Multi-Source Telemetry

## Overview

In day-to-day Security Operations Center (SOC) work, analyzing a raw packet capture (`.pcap`) in isolation rarely gives you the full picture. A PCAP records network motion across a specific wire or interface, but it cannot tell you which user logged into the system or which host process spawned the connection.

To build an air-tight incident timeline, I learned to correlate network-level packet evidence from Wireshark/TShark with host-based and perimeter logs ingested by a Security Information and Event Management (SIEM) platform.

---

## 1. The Multi-Source Telemetry Landscape

During an investigation, different security tools capture different slices of reality. Combining these sources allows us to eliminate blind spots and reconstruct host and network activity accurately.

| Telemetry Source | Primary Identifiers | What It Proves | Core Limitation |
| :--- | :--- | :--- | :--- |
| **Windows Event Logs** | Event ID 4624 (Logon), Event ID 4688 (Process Execution), User SID | System login sessions, user context, host privilege changes. | No visibility into wire-level packet contents or payloads. |
| **Sysmon Process Records** | Sysmon ID 1 (Process), Image Path, PID, PPID, SHA-256 Hash | Exact binary path, command-line arguments, parent-child process lineage. | Cannot verify if outbound network packets reached their target. |
| **Firewall Session Logs** | Source/Dest IP & Port, Action (`ALLOW`/`DENY`), Rule ID | Whether a network connection was permitted or blocked at the boundary. | Macro-level metadata only; does not record payload contents. |
| **DNS Server Logs** | Client IP, Requested FQDN, Query Type, Response Code | External domain lookup attempts and resolved IP infrastructure. | Does not confirm if data transfer occurred after DNS resolution. |
| **PCAP (Wireshark/TShark)** | Frame Length, TCP Flags, HTTP Headers, Raw Byte Streams | Direct, unalterable proof of data transmitted across the wire. | Scoped only to the capture point; encrypted SSL/TLS blocks payload view. |

---

## 2. Real-World Analyst Correlation Workflow

When a SIEM alert fires—for instance, **"Anomalous Outbound Web Traffic Detected"**—I follow a four-stage pivot across evidence layers:

```
[ Step 1: Endpoint Log ]  --> Sysmon Event ID 1: powershell.exe spawned by cmd.exe (PID 4412)
           │
[ Step 2: DNS Query Log ]  --> Query for evil-domain.com resolved to 192.0.2.45
           │
[ Step 3: Firewall Log  ]  --> ALLOW connection from 10.0.0.15:49812 to 192.0.2.45:80
           │
[ Step 4: Wireshark PCAP]  --> HTTP GET request displaying user-agent and GET /payload.bin
```

### Forensic Walkthrough:
1. **Endpoint Triage:** Check Sysmon logs to find the local process responsible for initiating outbound traffic (`powershell.exe`, PID `4412`).
2. **DNS Resolution Verification:** Query DNS server records to match the domain lookup timestamp with host `10.0.0.15`.
3. **Firewall Boundary Check:** Confirm the perimeter firewall permitted TCP traffic over port 80 to IP `192.0.2.45`.
4. **PCAP Deep Dive:** Open Wireshark, apply display filter `ip.addr == 192.0.2.45`, and reconstruct the unencrypted HTTP GET stream to inspect the requested file (`/payload.bin`).

---

## 3. Critical Investigative Rule: Avoid Temporal Fallacies

> ⚠️ **Key Rule:** **Never assume two events are connected simply because they happened around the same time.**

In high-volume corporate networks, thousands of log lines and network frames are generated every second. To prove correlation beyond reasonable doubt, I require at least **two matching pivot fields** alongside synchronized timestamps:
* **Pivot Field 1:** Exact Socket Pair (`Source IP:Port` $\leftrightarrow$ `Destination IP:Port`).
* **Pivot Field 2:** Matching Process Identifier / Host Identifier (linking Sysmon Event ID 3 Network Connections to local PIDs).
* **Pivot Field 3:** Cryptographic file hash verification between host downloads and endpoint executions.

---

## 4. Key Takeaways for Security Operations

* **Standardize Timestamps:** Always normalize log timestamps to Universal Coordinated Time (UTC) across all endpoints, firewalls, and packet captures to avoid clock drift issues during correlation.
* **Combine Tools for Context:** Network telemetry shows *what* moved across the network; host logs prove *who* and *what process* moved it. True threat hunting requires both.
