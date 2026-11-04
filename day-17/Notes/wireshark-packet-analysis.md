# Lab Investigation Report: Wireshark Packet Inspection & Telemetry Analysis

**Author:** Serah Mulwa   
**Date:** November 4, 2026  
**Module:** Day 17 - Network Control & Boundary Defence  

---

## 1. Executive Summary

This practical exercise focuses on packet-level analysis of core network control protocols using **Wireshark** on Parrot OS. By capturing live network traffic on interface `enp0s3`, applying precise Berkeley Packet Filters (BPF) and display filters, and performing deep-packet inspection on **ARP** and **ICMP** exchanges, this lab bridges high-level network theory with binary-level packet evidence.

---

## 2. Environment Preparation & Capture Configuration

### 2.1 Interface & Tool Verification
* **Active Network Adapter:** `enp0s3` (Virtual Ethernet, NAT Mode)
* **Execution Context:** Elevated privileges (`sudo wireshark`) to ensure promiscuous mode packet capture on the virtual socket.

### 2.2 Berkeley Packet Filter (BPF) Syntax
To isolate relevant control traffic without cluttering the capture buffer with ambient system noise, a targeted capture filter was applied prior to initiating packet capture:

```bpf
arp or (udp port 67 or udp port 68) or icmp
```

* **`arp`**: Captures Layer 2 Address Resolution Protocol frames.
* **`udp port 67 or udp port 68`**: Captures Layer 4 DHCP server and client communication.
* **`icmp`**: Captures Layer 3 Internet Control Message Protocol packets.

---

## 3. Display Filter Evaluation & Protocol Inspection

Once traffic was captured, various display filters were evaluated to isolate specific protocol headers and analyze packet details.

| Display Filter | Result / Packets Displayed | Forensic Evaluation & Analysis |
| :--- | :--- | :--- |
| **`arp`** | 8 Packets (80% of capture) | Displays broadcast ARP queries (`Who has 10.0.2.2?`) and unicast MAC replies from gateway `52:54:00:12:35:00`. |
| **`icmp`** | 2 Packets (20% of capture) | Displays bi-directional Echo Request (Frame 3) and Echo Reply (Frame 4) exchange between `10.0.2.15` and `10.0.2.2`. |
| **`ip`** | 2 Packets (20% of capture) | Isolates Layer 3 IPv4 traffic traversing the interface. |
| **`ipv6`** | 0 Packets (0.0% of capture) | Confirms zero active IPv6 traffic passed through the interface during the connectivity check. |
| **`dhcp` / `bootp`** | 0 Packets (0.0% of capture) | Confirms no dynamic IP allocation or lease renewal occurred during the live capture window. |

---

## 4. Deep-Packet Inspection Findings

### 4.1 Address Resolution Protocol (ARP) Request Analysis

Inspecting **Frame 1** in the Wireshark packet details pane revealed the exact structure of a Layer 2 address resolution query:

* **Frame Summary:** Frame 1: 42 bytes on wire (336 bits), 42 bytes captured on interface `enp0s3`.
* **Ethernet II Header:** 
  * Source MAC: `08:00:27:3b:a4:b2` (Parrot OS Virtual NIC)
  * Destination MAC: `52:54:00:12:35:00` (Unicast Gateway MAC)
* **Address Resolution Protocol Payload:**
  * **Hardware Type:** Ethernet (1)
  * **Protocol Type:** IPv4 (`0x0800`)
  * **Opcode:** `request (1)`
  * **Sender Hardware Address:** `08:00:27:3b:a4:b2`
  * **Sender Protocol Address:** `10.0.2.15`
  * **Target Hardware Address:** `00:00:00:00:00:00` (Unknown / Query target)
  * **Target Protocol Address:** `10.0.2.2`

**Key Insight:** The sender explicit sets the Target Hardware Address to all zeroes (`00:00:00:00:00:00`) because it is querying the local network segment to learn which hardware address owns IP `10.0.2.2`.

---

### 4.2 Internet Control Message Protocol (ICMP) Analysis

Inspecting **Frame 3** and **Frame 4** provided full details on Layer 3 ICMP messaging:

* **IPv4 Header Details (Frame 3 - Echo Request):**
  * Source IP: `10.0.2.15`
  * Destination IP: `10.0.2.2`
  * Header Length: 20 bytes
  * Time to Live (TTL): 64
  * Protocol ID: `ICMP (1)`
* **ICMP Payload Details:**
  * **Type:** `8` (Echo Request)
  * **Code:** `0`
  * **Sequence Number:** `1`
  * **Identifier:** `0x5e7a`
* **Response Frame (Frame 4 - Echo Reply):**
  * **Source IP:** `10.0.2.2`
  * **Destination IP:** `10.0.2.15`
  * **Type:** `0` (Echo Reply)
  * **Code:** `0`

---

## 5. Evidence Classification Framework

When conducting digital investigations and compiling SOC telemetry reports, evidence must be categorized into clear tiers to prevent misrepresentation:

1. **Observed Evidence:**
   * Live ARP resolution requests (`10.0.2.15` requesting MAC for `10.0.2.2`).
   * ICMP Echo Request and Reply sequence with 0% packet loss and 0.306 ms latency.
   * IPv4 header structures with TTL 64 and Protocol ID 1.

2. **Inferred Evidence:**
   * Gateway `10.0.2.2` is operational, responsive, and maintaining active Layer 2 bindings on VirtualBox interface `enp0s3`.
   * The kernel successfully updated its neighbor cache from `STALE` to `REACHABLE` immediately after receiving the ICMP reply packet.

3. **Expected (Theoretical) Behavior:**
   * According to RFC 2131, DHCP assigns IP addresses using the four-step **DORA** sequence (Discover, Offer, Request, Acknowledge) over UDP ports 67/68.
   * No DHCP packets were observed during this capture session because the virtual host obtained its lease prior to launching Wireshark.

---

## 6. Portfolio Visual Artifacts

The screenshots capturing this lab's execution are saved in `day-17/screenshots/`:

* `107-wireshark-dhcp-filter-empty.png` — Verification of `dhcp` display filter on pre-existing lease.
* `108-wireshark-icmp-ping-exchange.png` — Bi-directional ICMP Echo Request/Reply exchange.
* `109-wireshark-ip-filter.png` — Layer 3 IPv4 packet isolation.
* `111-wireshark-arp-packet-inspection.png` — Deep packet inspection of ARP request payload.
* `112-wireshark-icmp-ip-header-inspection.png` — IPv4 header breakdown (TTL 64, Protocol ID 1).
* `114-wireshark-capture-options-config.png` — Berkeley Packet Filter configuration on `enp0s3`.
