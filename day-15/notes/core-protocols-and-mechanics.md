# Day 15 - Core Protocols, Packet Structures, & TCP/UDP Mechanics

## Overview

Packet-level network analysis requires a granular understanding of how data is structured, wrapped, and transmitted across local and global networks. This guide details network data units, encapsulation layers, MAC vs. IP addressing, IP packet headers, and the operational mechanics of transport-layer protocols (TCP and UDP).

---

## 1. Network Data Units & Encapsulation

When computers communicate, information is segmented into discrete units across different layers of the network stack:

| Networking Layer | Common Data-Unit Name | Primary Responsibility |
| :--- | :--- | :--- |
| **Application Layer (L7)** | Data or Message | High-level user/application content (e.g., HTTP request, DNS query). |
| **Transport Layer (L4)** | **Segment** (TCP) or **Datagram** (UDP) | Port-to-port communication, reliability, and flow control. |
| **Network Layer (L3)** | **Packet** | Logical addressing and routing across subnets (IPv4/IPv6). |
| **Data Link Layer (L2)** | **Frame** | Local physical link communication using MAC addresses. |

### 1.1 Encapsulation and Decapsulation
* **Encapsulation:** Moving *down* the network stack. Each layer prepends its own tracking header to the payload (e.g., HTTP data $\rightarrow$ TCP segment $\rightarrow$ IP packet $\rightarrow$ Ethernet frame).
* **Decapsulation:** Moving *up* the stack upon reception. The receiving host strips away headers layer by layer to interpret the raw payload.

---

## 2. Layer 2: Ethernet Frames & Addressing

Ethernet operates locally on a physical network segment (LAN) using physical hardware addresses.

### 2.1 MAC Address vs. IP Address

| Feature | MAC Address (Media Access Control) | IP Address (Internet Protocol) |
| :--- | :--- | :--- |
| **OSI Layer** | Data Link Layer (Layer 2) | Network Layer (Layer 3) |
| **Permanence** | Hardcoded into the network interface card (NIC) by the manufacturer. | Assigned dynamically (DHCP) or statically by software configuration. |
| **Scope** | Local network segment only (changes at every router hop). | End-to-end global communication across routers worldwide. |
| **Format Example** | `00:1A:2B:3C:4D:5E` | `192.0.2.10` |

---

## 3. Layer 3: IP Packets & TTL Mechanics

The Internet Protocol (IPv4/IPv6) handles logical routing across disparate networks.

### 3.1 Key IPv4 Header Fields
* **Source & Destination IP:** Logical originating and target addresses.
* **Protocol Number:** Identifies the encapsulated L4 protocol (`6` for TCP, `17` for UDP, `1` for ICMP).
* **TTL (Time to Live):** A hop-limit counter preventing routing loops. Decrements by 1 at each router hop.
  * *Default TTL Values:* Linux = 64; Windows = 128 (useful for passive OS fingerprinting).

---

## 4. Layer 4: Transport Protocols (TCP vs. UDP)

### 4.1 Transmission Control Protocol (TCP)
TCP is a **connection-oriented**, reliable transport protocol ensuring ordered, error-free data delivery.

#### The TCP 3-Way Handshake
1. **SYN:** Client sends a synchronizing packet with an Initial Sequence Number (ISN).
2. **SYN-ACK:** Server responds acknowledging the client sequence and providing its own ISN.
3. **ACK:** Client acknowledges the server response. The socket enters the `ESTABLISHED` state.

#### Key TCP Flags
* **SYN (`S`):** Initiate connection.
* **ACK (`.`):** Acknowledgment of data/sequence.
* **FIN (`F`):** Graceful connection termination.
* **RST (`R`):** Abrupt connection reset/rejection.
* **PSH (`P`):** Push data immediately to application buffer.

#### TCP Retransmissions
Occurs when a sender resends a segment because an expected acknowledgement (`Ack`) was not received within the timeout window. Can indicate packet loss, congestion, or network instability.

### 4.2 User Datagram Protocol (UDP)
* **Connectionless:** No handshake or session establishment.
* **Unreliable / Best-Effort:** No built-in retransmissions, flow control, or delivery guarantees.
* **Use Cases:** DNS lookups, VoIP, streaming, and real-time telemetry where speed outweighs guaranteed delivery.

---

## Summary Table: TCP vs. UDP

| Attribute | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
| :--- | :--- | :--- |
| **Connection Setup** | Yes (3-Way Handshake) | None |
| **Ordered Delivery** | Guaranteed (Sequence Numbers) | Not guaranteed |
| **Reliability** | Built-in retransmissions & ACKs | Best-effort |
| **Header Size** | 20 to 60 Bytes | Fixed 8 Bytes |
| **Typical Protocols** | HTTP/HTTPS, SSH, SMB | DNS, DHCP, Syslog |
