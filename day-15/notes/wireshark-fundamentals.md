# Day 15 - Wireshark Navigation & PCAP Fundamentals

## Overview

Wireshark is the industry-standard open-source network protocol analyzer. It allows security analysts, network engineers, and forensic investigators to inspect saved network packet captures (PCAP) or live interface streams. For a Security Operations Centre (SOC) analyst, Wireshark provides unvarnished, objective truth by revealing the exact protocol mechanics, transport states, and payload metadata of network communications.

---

## 1. Packet Capture File Formats (PCAP vs. PCAPNG)

Network packet data recorded from network taps, SPAN ports, or local interfaces is stored in specialized packet capture files.

| Feature / Format | `.pcap` (Libpcap Format) | `.pcapng` (PCAP Next Generation) |
| :--- | :--- | :--- |
| **Standard Type** | Legacy standard capture format. | Modern extensible capture format. |
| **Tool Compatibility** | Universally supported by older tools, Snort, Suricata, and legacy scripts. | Standard default format for modern Wireshark and TShark. |
| **Metadata Capabilities** | Basic packet timestamps and raw header bytes. | Multi-interface recording, hardware details, user comments, and custom metadata blocks. |
| **Forensic Best Practice** | Maintain original file integrity; compute SHA-256 hashes prior to and after analysis. | Supports embedded analyst comments directly within packet blocks without corrupting raw data. |

---

## 2. The 3-Pane Wireshark Graphical Interface

When opening a `.pcap` or `.pcapng` file in Wireshark, the graphical user interface presents three synchronized panes designed for rapid protocol inspection.

```
+-----------------------------------------------------------------------------------+
| [1. TOP PANE] PACKET LIST PANE                                                    |
| Displays chronological sequence of all captured packets.                          |
+-----------------------------------------------------------------------------------+
| [2. MIDDLE PANE] PACKET DETAILS PANE                                              |
| Hierarchical protocol tree showing OSI layer breakdown of selected packet.         |
+-----------------------------------------------------------------------------------+
| [3. BOTTOM PANE] PACKET BYTES PANE                                                |
| Raw binary data represented in hexadecimal and printable ASCII side-by-side.      |
+-----------------------------------------------------------------------------------+
```

### 2.1 Pane 1: Packet List Pane (Top Section)
Displays a master summary log of all packets contained in the capture file, sorted chronologically.

* **No. (Packet Index):** The sequential index of the packet (e.g., Packet `#1`, `#42`). Essential for referencing specific evidence in SOC case reports.
* **Time:** Timestamp of packet capture (configurable as absolute UTC time, relative time from start, or delta time).
* **Source / Destination:** IP addresses or MAC addresses of the transmitting and receiving endpoints.
* **Protocol:** Highest identified protocol layer (e.g., `TCP`, `DNS`, `HTTP`, `TLSv1.2`, `ARP`).
* **Length:** Total frame size in bytes on the wire.
* **Info:** Dynamic protocol-specific overview (e.g., TCP flags `[SYN]`, HTTP request paths `GET /index.html`, or DNS query domains).

### 2.2 Pane 2: Packet Details Pane (Middle Section)
When a packet is selected in the Packet List, this pane provides an expandable, hierarchical tree structure breaking down the packet layer by layer according to the OSI/TCP-IP models:

1. **Frame:** Physical capture parameters (interface ID, arrival time, byte length).
2. **Ethernet II:** Layer 2 link-layer details (Source/Destination MAC, EtherType).
3. **Internet Protocol (IPv4/IPv6):** Layer 3 network details (Source/Destination IP, TTL, Protocol ID).
4. **Transmission Control Protocol (TCP) / User Datagram Protocol (UDP):** Layer 4 transport details (Ports, Sequence/ACK numbers, TCP Flags).
5. **Application Layer (HTTP, DNS, TLS):** Layer 7 application details (Request methods, domain queries, status codes, SNI hostnames).

### 2.3 Pane 3: Packet Bytes Pane (Bottom Section)
Displays the raw, unalterable binary data of the selected packet in two side-by-side formats:
* **Left Column:** Hexadecimal (Hex) representation of every byte (e.g., `45 00 00 3c`).
* **Right Column:** ASCII text representation of printable characters. Non-printable bytes appear as dots (`.`).

---

## 3. Key SOC Analyst Guidance

1. **Investigative Workflow:** Scan the Packet List pane for protocol anomalies, use the Packet Details pane to expand specific layer headers, and cite exact packet numbers (`No.`) in your official case reports.
2. **Contextual Analysis:** High-level summaries in the Info column can be misleading. Always verify protocol state flags, return codes, and sequence numbers inside the Packet Details pane.
3. **Evidence Integrity:** Raw PCAP files contain unalterable network telemetry. Computing SHA-256 hashes ensures the integrity of network evidence throughout an investigation.
