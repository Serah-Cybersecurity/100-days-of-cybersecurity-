# Technical Note: Zeek Internal Processing Pipeline & Engine Mechanics

**Author:** Serah Mulwa  
**Module:** Day 19 - Network Threat Hunting with Zeek  

---

## 1. Executive Summary

Understanding how Zeek processes network traffic under the hood is critical for effective threat hunting and incident analysis. Unlike simple packet capture tools or stateless packet filters, Zeek operates as a **stateful, protocol-aware network analysis engine**. 

This technical note details the **7-stage internal data pipeline** that transforms raw binary packets into structured, correlation-ready security telemetry (`conn.log`, `dns.log`, `ssl.log`, etc.).

---

## 2. The 7-Stage Internal Data Pipeline

Every byte captured by Zeek traverses seven distinct architectural processing stages before arriving in a SIEM dashboard or log analysis script:

```text
                  [ STAGE 1: PACKET INPUT ]
        (Live Network TAP / Interface or Offline PCAP)
                            │
                            ▼
                [ STAGE 2: PACKET DECODING ]
       (Ethernet ➔ IPv4/IPv6 ➔ TCP/UDP ➔ Layer Normalization)
                            │
                            ▼
              [ STAGE 3: CONNECTION TRACKING ]
    (5-Tuple Hashing & Bi-directional State Table Management)
                            │
                            ▼
         [ STAGE 4: PROTOCOL IDENTIFICATION & ANALYSIS ]
      (Dynamic Protocol Detection [DPD] & Spicy Decoders)
                            │
                            ▼
                 [ STAGE 5: EVENT ENGINE ]
  (Emits Low-Level Abstract Security Signals, e.g., dns_request)
                            │
                            ▼
               [ STAGE 6: ZEEK SCRIPTS / POLICY ]
   (Executes Event Handlers, Aggregates State, Notice Framework)
                            │
                            ▼
              [ STAGE 7: LOGGING ENGINE & OUTPUT ]
   (Writes Tab-Separated / JSON: conn.log, dns.log, ssl.log)
                            │
                            ▼
            [ PYTHON AUTOMATION / SIEM INGESTION ]
              (Splunk / Elastic / Custom Parsers)
```

---

## 3. Detailed Stage Breakdown

### Stage 1: Packet Input
Zeek ingests raw packet streams from two primary sources:
* **Live Capture:** Ingests live packets from network interfaces using `libpcap` sockets, network TAPs, or mirror/SPAN ports.
* **Offline Processing:** Reads saved packet capture files (`.pcap`, `.pcapng`) using the `-r` flag. Offline processing ensures complete test reproducibility during forensic investigations and lab work.

### Stage 2: Packet Decoding & Reassembly
The C++ core parses low-level header structures across physical, network, and transport layers:
* **Layers Processed:** Ethernet, VLAN (802.1Q), ARP, IPv4, IPv6, ICMP, TCP, and UDP.
* **Normalization:** Handles IP defragmentation and TCP stream reassembly. Out-of-order or duplicate TCP segments are buffered and re-ordered to present a clean byte stream to higher-level parsers.

### Stage 3: Connection Tracking & Sessionization
Zeek abstracts individual packets into stateful **connections** identified by a unique **5-tuple**:
1. Source IP Address (`id.orig_h`)
2. Source Port (`id.orig_p`)
3. Destination IP Address (`id.resp_h`)
4. Destination Port (`id.resp_p`)
5. Transport Protocol (`proto`)

When a session begins (e.g., a TCP SYN packet), Zeek assigns a globally unique identifier known as a **UID** (e.g., `C9xKz13aR8b3xQ1`). It distinguishes the **Originator** (client initiating the session) from the **Responder** (server answering the request).

### Stage 4: Protocol Identification (Dynamic Protocol Detection - DPD)
Instead of relying solely on standard port numbers (e.g., port 80 = HTTP), Zeek uses **Dynamic Protocol Detection (DPD)**:
* **How DPD Works:** Zeek inspects payload header signatures rather than port bindings. If an attacker runs an encrypted SSH tunnel or malware C2 channel over port 80, Zeek detects the SSH protocol handshake signatures and automatically routes the stream to the SSH protocol analyzer.
* **Spicy Parser Framework:** Modern Zeek versions utilize Spicy, a custom C++ parser generator that allows security engineers to build custom parsers for proprietary or emerging protocols.

### Stage 5: The C++ Event Engine
As protocol analyzers decode application streams, the C++ engine generates abstract internal **events** and pushes them onto an internal event queue.
* **Example Events:** `connection_established`, `dns_request`, `http_request`, `ssl_established`.
* **Key Concept:** An event is merely a signal indicating that a protocol action occurred—it does **not** imply malicious activity.

### Stage 6: Policy Script Interpreter
Zeek’s scripting engine executes custom `.zeek` scripts that register interest in specific events.
* **Capabilities:** Tracks state over long time windows, maintains counters, calculates statistical thresholds, checks threat intelligence feeds, and raises operational alerts using the **Notice Framework**.

### Stage 7: Logging Engine
Zeek flushes state summaries out to disk as structured log files.
* **Formats Supported:** Tab-Separated Values (TSV) by default, or structured JSON when configured via `redef LogAscii::use_json = T;`.
* **Core Output Logs:**
  * `conn.log`: Summary of every network connection (durations, byte counts, connection states).
  * `dns.log`: Complete record of all DNS queries, answers, TTLs, and query types.
  * `ssl.log`: TLS handshake metadata, Server Name Indication (SNI), and certificate details.
  * `http.log`: Web request URIs, HTTP methods, user-agents, and status codes.
  * `weird.log`: Protocol anomalies and non-standard packet structures.

---

## 4. Job Market & SOC Application

* **SOC Analyst (Tier 1 & Tier 2):** Uses Stage 7 logs ingested into SIEM systems (Splunk/Elastic) to reconstruct attack timelines without needing to open massive raw PCAP files in Wireshark.
* **Threat Hunter:** Leverages Stage 3 (Connection Sessionization) and Stage 4 (DPD) to hunt for non-standard protocol usage and covert communication channels.
* **Detection Engineer:** Authors custom Zeek scripts at Stage 6 to flag operational anomalies at the sensor level before logs reach the SIEM.

---

## 5. Key Portfolio Takeaways

* **Zeek views the network in sessions, not isolated packets.**
* **Dynamic Protocol Detection prevents attackers from hiding malicious traffic on non-standard ports.**
* **Events are internal engine signals; logs are structured analytical outputs.**
