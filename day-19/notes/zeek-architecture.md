# Technical Note: Zeek Architecture & Network Security Monitoring Concepts

**Author:** Serah Mulwa  
**Module:** Day 19 - Network Threat Hunting with Zeek  

---

## 1. Executive Summary

While signature-based Intrusion Detection Systems like Suricata focus on matching known threat patterns to generate discrete alerts, **Zeek** (formerly Bro) takes an architectural approach focused on **protocol state tracking and metadata extraction**. 

Zeek passively sits on a network interface or inspects saved packet captures (`.pcap`), converts raw binary byte streams into structured protocol communications, and outputs lightweight, machine-readable logs (`conn.log`, `dns.log`, `ssl.log`, `http.log`). This technical note details Zeek's internal two-layer architecture, engine mechanics, and role in modern Security Operations Centers (SOCs).

---

## 2. The Two-Layer Engine Architecture

Zeek separates packet processing into two distinct layers: a high-performance C++ core and an event-driven scripting environment.

```
                    [ RAW PACKET STREAM (PCAP / Live Interface) ]
                                         │
                                         ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│ 1. THE EVENT ENGINE (C++)                                                    │
│    • Captures packets via libpcap socket interfaces.                         │
│    • Performs IP defragmentation & reassembles TCP streams.                  │
│    • Runs protocol decoders (Spicy framework: HTTP, DNS, TLS, SSH, SMB).      │
│    • Emits abstract internal security EVENTS (e.g., dns_request).             │
└───────────────────────────────────────┬───────────────────────────────────────┘
                                        │
                                        ▼ (Internal Events)
┌───────────────────────────────────────────────────────────────────────────────┐
│ 2. THE POLICY SCRIPT INTERPRETER (Zeek Scripting Language)                    │
│    • Listens for specific events via event handlers.                          │
│    • Applies enterprise policy logic, state counters, and threat feeds.       │
│    • Writes structured TSV/JSON logs (conn.log, dns.log, ssl.log, etc.).      │
└───────────────────────────────────────────────────────────────────────────────┘
```

### Layer 1: The Event Engine (C++)
The C++ core handles the computationally heavy task of raw packet handling:
1. **Packet Capture & Stream Assembly:** Uses `libpcap` to ingest packets, perform IP defragmentation, and reconstruct TCP byte streams.
2. **Protocol Decoders:** Decodes application-layer protocols (DNS, TLS, HTTP, SSH, etc.) statefully.
3. **Event Generation:** When a protocol milestone occurs (e.g., a host issues a DNS query), the C++ engine generates an internal **event** (such as `dns_request`) and passes it up to Layer 2.

### Layer 2: The Policy Script Interpreter
The policy layer interprets domain-specific Zeek scripts (`.zeek`):
* **Event Handlers:** Scripts register handlers that trigger whenever specific C++ events fire.
* **State Management:** Tracks sessions, byte counts, and connection outcomes.
* **Log Writing:** Formats extracted metadata into structured tab-separated values (TSV) or JSON files for SIEM ingestion.

---

## 3. Suricata vs. Zeek: Complementary Defense Pillars

| Feature | Suricata (IDS/IPS) | Zeek (NSM Framework) |
| :--- | :--- | :--- |
| **Primary Focus** | Signature matching & inline blocking | Network metadata, state tracking & logging |
| **Alert Trigger** | Rule matches specific byte pattern | Generates session state records for *all* traffic |
| **Output Type** | Security alerts (`eve.json` alert object) | Specialized protocol logs (`conn.log`, `dns.log`, `ssl.log`) |
| **Best Used For** | Intercepting known threats instantly | Forensic investigations, baselining & threat hunting |

---

## 4. Version Tracking & Environment Audit

In professional SOC engineering, always document the exact engine release running in your lab environment:

* **Installed Release:** Zeek version running on Parrot OS (`zeek --version`).
* **LTS Context:** Zeek 9.0.x represents the primary long-term support release branch (succeeding the 8.0.x LTS line), featuring the Spicy protocol parser framework and enhanced cluster communication channels.

---

## 5. Job Market Relevance & SOC Application

* **SIEM & Pipeline Engineers:** Ingest Zeek JSON feeds into Splunk or Elastic to build complete visibility dashboards without storing massive PCAP files indefinitely.
* **Threat Hunters:** Query `conn.log` and `dns.log` to establish network communication baselines, detect covert DNS tunneling, and hunt for long-duration beaconing connections.
* **Incident Responders:** Replay PCAPs gathered during an active breach through Zeek to generate connection timelines without sifting through raw Wireshark packets manually.
