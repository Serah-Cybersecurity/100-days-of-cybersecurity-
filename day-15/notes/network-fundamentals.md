# Day 15 - Network Traffic Analysis & Packet Architecture Foundations

## Overview

Network Traffic Analysis (NTA) and Packet Capture (PCAP) inspection are core competencies for Security Operations Centre (SOC) analysts. While operating system event logs detail activity *internal* to a host, packet-level telemetry reveals communications *between* endpoints, establishing transport status, exact byte counts, protocol mechanics, and payload data.

---

## 1. Network Models & Protocol Encapsulation

Network data relies on standard layered models to structure communications across systems.

### 1.1 OSI 7-Layer Model vs. TCP/IP 4-Layer Stack

| OSI Layer | Layer Name | TCP/IP Layer | Primary Protocols / Data Units | Security Relevance |
| :-: | :--- | :-: | :--- | :--- |
| **7** | Application | **Application** | HTTP, DNS, SSH, TLS (L6/7) | Application payloads, URIs, DNS domain queries. |
| **6** | Presentation | | ASCII, TLS/SSL Encapsulation | Encryption inspection, SNI extraction. |
| **5** | Session | | RPC, Sockets, SMB Sessions | Session establishment and state tracking. |
| **4** | Transport | **Transport** | TCP, UDP | Source/Destination ports, TCP flags, sequence tracking. |
| **3** | Network | **Internet** | IPv4, IPv6, ICMP | Logical routing, Source/Destination IPs, TTL values. |
| **2** | Data Link | **Network Access** | Ethernet, ARP, Wi-Fi (802.11) | Local physical routing, Source/Destination MACs. |
| **1** | Physical | | Copper Cables, Fiber, RF | Physical signal transmission. |

### 1.2 Data Encapsulation Sequence

When data is sent from a source host to a destination, each layer prepends a specialized tracking header:

$$\text{Data (L7)} \xrightarrow{\text{Transport}} \text{TCP/UDP Header} + \text{Payload (Segment/Datagram)} \xrightarrow{\text{Internet}} \text{IP Header} + \text{Segment (Packet)} \xrightarrow{\text{Link}} \text{Ethernet Header} + \text{Packet (Frame)}$$

When ingested by packet tools (Wireshark / TShark), **decapsulation** occurs, unpeeling layers from Link (L2) up to Application (L7).

---

## 2. Packet Headers & Protocol Mechanics

### 2.1 Layer 2: Ethernet Header Structure
Ethernet operates locally within a network segment using physical MAC addresses.

```text
+-------------------+-------------------+-------------------+
|  Destination MAC  |    Source MAC     |    EtherType      |
|    (6 Bytes)      |    (6 Bytes)      |    (2 Bytes)      |
+-------------------+-------------------+-------------------+
| 00:0c:29:ab:cd:ef | 00:50:56:12:34:56 |  0x0800 (IPv4)    |
+-------------------+-------------------+-------------------+
```
* **EtherType `0x0800`:** IPv4 payload.
* **EtherType `0x86DD`:** IPv6 payload.
* **EtherType `0x0806`:** Address Resolution Protocol (ARP).

### 2.2 Layer 3: IPv4 Header Fields
Enables logical, routed communications across subnets.

* **Source & Destination IPv4:** Originating client and target destination addresses.
* **Protocol Number:**
  * `1` = ICMP (Ping / Diagnostic)
  * `6` = TCP (Transmission Control Protocol)
  * `17` = UDP (User Datagram Protocol)
* **Time to Live (TTL):** Decremented at each routing hop. Linux default = 64; Windows default = 128 (used for passive OS OS-fingerprinting).

### 2.3 Layer 4: Transport Protocols

#### TCP vs. UDP Comparison

| Attribute | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
| :--- | :--- | :--- |
| **Connection Mechanism** | Connection-Oriented (3-Way Handshake) | Connectionless |
| **Reliability** | Retransmissions on packet loss | Best-effort (No acknowledgments) |
| **Header Size** | Minimum 20 Bytes | Fixed 8 Bytes |
| **Flow Control** | Dynamic window sizing | None |
| **Common Protocols** | HTTP, HTTPS, SSH, SMB, FTP | DNS, DHCP, Streaming, Syslog |

#### The TCP 3-Way Handshake Sequence

```text
  CLIENT (192.168.1.100)                         SERVER (198.51.100.10)
  (Ephemeral Port e.g. 52144)                         (Standard Port e.g. 80)
               |                                               |
               | -------- SYN (Seq=0, Flags=SYN) ------------> | [Step 1]
               |                                               |
               | <------- SYN-ACK (Seq=0, Ack=1) ------------- | [Step 2]
               |                                               |
               | -------- ACK (Seq=1, Ack=1) ----------------> | [Step 3]
               |                                               |
       [CONNECTION ESTABLISHED]                        [CONNECTION ESTABLISHED]
```

1. **SYN (Synchronize):** Client initiates connection with Initial Sequence Number (ISN).
2. **SYN-ACK (Synchronize-Acknowledge):** Server acknowledges client sequence number and returns its own ISN.
3. **ACK (Acknowledge):** Client acknowledges server response. Socket enters `ESTABLISHED` state.

---

## 3. Application Protocols (Layer 7)

### 3.1 Domain Name System (DNS) — Port 53 (UDP/TCP)
* Translates domain names to IP addresses.
* **SOC Significance:** Malware almost universally performs DNS lookup queries prior to Command & Control (C2) beaconing.

### 3.2 Hypertext Transfer Protocol (HTTP) — Port 80 (TCP)
* Plaintext application communication.
* Key Methods: `GET`, `POST`, `PUT`, `HEAD`.
* Key Status Codes: `200 OK`, `301/302 Redirect`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `500 Server Error`.

### 3.3 Transport Layer Security (TLS/HTTPS) — Port 443 (TCP)
* Encrypts L7 payloads.
* **Analyst Visibility:** Application content is hidden, but handshake metadata remains visible:
  * **SNI (Server Name Indication):** The cleartext domain requested by the client during handshake.
  * **TLS Certificate:** Server certificate subject, issuer, and validity parameters.

---

## 4. Key Takeaways for Analyst

1. **Host Logs vs. Network PCAPs:** Host logs verify process execution; PCAP analysis proves actual network connectivity, byte counts, and raw protocol interactions.
2. **Encapsulation Discipline:** Network analysis requires evaluating L2 (MAC), L3 (IP), L4 (TCP/UDP), and L7 (HTTP/DNS/TLS) layers in unison.
3. **Evidence Integrity:** Raw PCAPs preserve unalterable protocol headers necessary for network forensic investigations.
