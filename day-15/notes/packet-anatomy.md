# Day 15 - Network Packet Anatomy & Fundamental Encapsulation

## 1. Definition

A **network packet** (or Protocol Data Unit, PDU) is a formatted block of data carried across a packet-switched network. Rather than sending continuous raw data streams across communication channels, computer systems break messages down into discrete chunks. Each packet consists of control information (headers and trailers) and user data (the payload).

In network security and digital forensics, packets represent the atomic unit of wire-level evidence.

---

## 2. Encapsulation (OSI & TCP/IP Model Mapping)

**Encapsulation** is the process where each layer of the network protocol stack wraps lower-layer payloads with its own header controls as data moves down the stack from application to physical media.

$$\text{Application Payload} \longrightarrow \text{Segment (TCP/UDP)} \longrightarrow \text{Packet (IP)} \longrightarrow \text{Frame (Ethernet)} \longrightarrow \text{Bits (Physical)}$$

```
+-----------------------------------------------------------------------+
| Ethernet Header | IP Header | TCP Header | Application Data | Trailer |
+-----------------------------------------------------------------------+
|<-- Layer 2 ---->|<-- L3 --->|<-- L4 --->|<---- L7 Payload ->|<-- L2 ->|
```

As a packet travels across routers and switches, intermediate nodes strip and re-wrap Layer 2 Ethernet headers, but Layer 3 (IP) and Layer 4 (TCP/UDP) headers remain intact end-to-end (excluding NAT translation points).

---

## 3. Layer 2: Ethernet & Data Link Data

The **Ethernet Frame** operates at Layer 2 of the OSI model. It enables node-to-node communication across local physical networks using **Media Access Control (MAC)** addresses.

* **MAC Address Structure:** A 48-bit (6-byte) hexadecimal hardware identifier burned into Network Interface Cards (NICs), formatted as `XX:XX:XX:XX:XX:XX`.
  * **OUI (Organizationally Unique Identifier):** The first 3 bytes (e.g., `00:50:56` for VMware).
  * **NIC Specific Identifier:** The last 3 bytes assigned by the manufacturer.
* **Ethernet Frame Components:**
  * **Destination MAC Address (6 bytes)**
  * **Source MAC Address (6 bytes)**
  * **EtherType (2 bytes):** Specifies the encapsulated Layer 3 protocol (e.g., `0x0800` for IPv4, `0x86DD` for IPv6, `0x0806` for ARP).
  * **Payload (46 to 1500 bytes)**
  * **Frame Check Sequence (FCS / CRC, 4 bytes):** Used for hardware error detection.

---

## 4. Layer 3: Internet Protocol (IPv4 & IPv6)

The **Internet Protocol (IP)** operates at Layer 3, facilitating logical routing across interconnected subnets and global networks.

### IPv4 vs IPv6 Comparison

| Header Field / Feature | IPv4 | IPv6 |
| :--- | :--- | :--- |
| **Address Length** | 32 bits (4 bytes) e.g., `192.168.1.1` | 128 bits (16 bytes) e.g., `fe80::1` |
| **Address Space** | $2^{32} \approx 4.29 \times 10^9$ addresses | $2^{128} \approx 3.4 \times 10^{38}$ addresses |
| **Header Size** | Variable (20 to 60 bytes due to Options) | Fixed (40 bytes) for faster router parsing |
| **Key Fields** | Source IP, Dest IP, TTL, Protocol, Header Checksum | Source IP, Dest IP, Hop Limit, Next Header |

* **Source IP:** The logical address of the originating network interface.
* **Destination IP:** The target host logical address.
* **Time To Live (TTL) / Hop Limit:** An 8-bit counter decremented by every router traversed. Prevents packets from looping infinitely ($TTL = 0 \implies \text{ICMP Time Exceeded}$).

---

## 5. Layer 4: Transmission Control Protocol (TCP)

**TCP** provides connection-oriented, reliable, ordered delivery of data between application endpoints.

* **Source Port & Destination Port (16 bits each):** Range from `0` to `65535`.
* **Sequence Numbers (32 bits):** Tracks stream order, enabling reassembly and loss detection.
* **Acknowledgment Numbers (32 bits):** Confirms receipt of bytes from the remote endpoint.
* **TCP Control Flags (9 bits):** SYN, ACK, FIN, RST, PSH, URG.
* **Connection Lifecycle:** Established via the **3-Way Handshake** (`SYN` $\rightarrow$ `SYN-ACK` $\rightarrow$ `ACK`) and terminated via `FIN-ACK` or immediate `RST`.

---

## 6. Layer 4: User Datagram Protocol (UDP)

**UDP** is a lightweight, connectionless, stateless transport protocol that prioritizes speed over reliability.

* **Header Size:** Fixed at only **8 bytes** (Source Port, Destination Port, Length, Checksum).
* **No Handshake:** Transmits datagrams immediately without establishing a stateful session.
* **No Retransmissions:** Lost datagrams are dropped; error recovery is delegated to the application layer (e.g., DNS, VoIP, streaming).

---

## 7. The Five-Tuple

The **5-Tuple** is the fundamental construct used by firewalls, SIEMs, and netflow collectors to define a unique stateful network conversation:

$$\text{5-Tuple} = \{\text{Source IP}, \text{Destination IP}, \text{Source Port}, \text{Destination Port}, \text{Transport Protocol}\}$$

### Example 5-Tuple:
* **Source IP:** `10.0.0.15`
* **Destination IP:** `198.51.100.4`
* **Source Port:** `49152` (Ephemeral Client Port)
* **Destination Port:** `443` (HTTPS Standard Port)
* **Transport Protocol:** `TCP` (6)

---

## 8. Security Relevance & Forensics

Packet metadata provides critical evidentiary value during security investigations:
1. **Traffic Profiling:** Identifies top talkers, unexpected protocols, and non-standard port usage.
2. **Beaconing Detection:** Uncovers regular command-and-control (C2) callback intervals using packet timing.
3. **Lateral Movement Mapping:** Tracks host-to-host internal connections over SMB (`445`), SSH (`22`), or RDP (`3389`).

---

## 9. Analytical Limitations

> ⚠️ **Core Limitation:** Packet metadata alone **cannot** establish complete intent or system compromise.

* **No Process Context:** Metadata does not reveal which binary executable or local PID generated the packet.
* **Encrypted Payloads:** Modern TLS encryption obscures application data contents.
* **Spoofing & NAT:** Source IPs can be spoofed on UDP/ICMP traffic, and Network Address Translation (NAT) masks internal host identities behind single public gateways.
