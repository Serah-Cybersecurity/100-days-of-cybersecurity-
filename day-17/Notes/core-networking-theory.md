# Core Networking Theory: DHCP, ARP, Routing, NAT, and Firewalls

**Author:** Serah  Mulwa

**Date:** November 4, 2026

**Module:** Day 17 - Network Control & Boundary Defence

## 1. Introduction to Core Networking Theory

When building a career in cybersecurity or network engineering, understanding packet-level analysis (Day 15) and application protocols (Day 16) is only part of the equation. You must also understand how devices acquire network identities, resolve local neighbors, route across subnets, and enforce security boundaries.

This reference note breaks down the foundational mechanics behind **Dynamic Host Configuration Protocol (DHCP)**, **Address Resolution Protocol (ARP)**, **Routing**, **NAT**, and **Firewalls**, highlighting their operational workflows, security implications, and enterprise defensive controls.

---

## 2. Dynamic Host Configuration Protocol (DHCP)

### 2.1 What is DHCP?
Standardized originally in **RFC 2131**, **DHCP (Dynamic Host Configuration Protocol)** is a network management protocol that automates the assignment of IP addresses and essential network configuration parameters to devices on an IP network.

When a device connects to a network, it requires five core configuration elements to communicate:
1. **IP Address:** Its unique numeric identifier on the network.
2. **Subnet Mask / Prefix:** Defines the network versus host boundaries (e.g., `255.255.255.0` or `/24`).
3. **Default Gateway:** The IP address of the local router enabling inter-network communication.
4. **DNS Resolver:** The server translating human-readable domain names into IP addresses.
5. **Lease Duration:** The temporal validity of the assigned IP address.

### 2.2 Why DHCP Matters in Cybersecurity
Manually configuring thousands of workstations in an enterprise environment is operationally impossible. DHCP automates this, but it introduces an inherent trust model: **clients blindly accept the configuration they receive.**

If a rogue device injects false network parameters, clients can be tricked into:
* Routing traffic through unauthorized gateways (Man-in-the-Middle attacks).
* Using malicious DNS resolvers (DNS hijacking and phishing).
* Experiencing service disruptions via DHCP starvation attacks.

### 2.3 The DHCP DORA Process (Step-by-Step)
The foundational mechanism of DHCP allocation follows the **DORA** lifecycle:
* **Discover (`DHCPDISCOVER`):** The client lacks an IP address and broadcasts a UDP packet across the local segment (Source IP `0.0.0.0`, Destination IP `255.255.255.255`, Ports `68` to `67`).
* **Offer (`DHCPOFFER`):** Available DHCP servers respond with a proposed IP address lease, subnet mask, gateway, and DNS configuration.
* **Request (`DHCPREQUEST`):** The client broadcasts its formal acceptance of a specific server's offered configuration, implicitly notifying competing servers to release their reserved IPs back into the pool.
* **Acknowledgement (`DHCPACK`):** The chosen DHCP server confirms the lease. The client binds the IP address to its network interface card and joins the active network.

---

## 3. Address Resolution Protocol (ARP)

### 3.1 What is ARP?
Standardized in **RFC 826**, **Address Resolution Protocol (ARP)** bridges the gap between Layer 3 (Network Layer) logical IPv4 addressing and Layer 2 (Data Link Layer) physical hardware MAC addressing on a local area network (LAN).

When a host knows a destination IPv4 address but lacks the destination host's physical MAC address, it cannot construct a valid Ethernet frame. ARP provides the protocol mechanism to dynamically resolve this mapping.

### 3.2 The ARP Resolution Process
1. **Cache Check:** Sender inspects its local memory (ARP cache table). If an unexpired entry exists, frame transmission proceeds immediately.
2. **ARP Request (Broadcast):** If unmapped, Sender broadcasts an ARP Request frame to Ethernet destination `FF:FF:FF:FF:FF:FF` asking: *"Who has IP 192.0.2.20? Tell 192.0.2.10."*
3. **ARP Reply (Unicast):** The target device bearing IP `192.0.2.20` updates its own table with Sender's details and returns a unicast ARP Reply frame directly to Sender's MAC address.
4. **Caching & Transmission:** Sender caches the IP-to-MAC association and transmits the buffered payload frame.

### 3.3 Security Considerations & Mitigations
* **ARP Poisoning / Spoofing:** Because ARP is stateless and unauthenticated, an attacker can broadcast forged ARP replies linking the default gateway's IP to the attacker's MAC address, intercepting victim traffic (Man-in-the-Middle).
* **Defensive Controls:** Enterprise networks deploy **Dynamic ARP Inspection (DAI)** paired with **DHCP Snooping** to validate ARP replies against trusted DHCP binding databases and drop fraudulent frames automatically.

---

## 4. Routing Mechanics

### 4.1 What is Routing?
**Routing** is the process of selecting a path for network traffic to move from a source network to a destination network. A physical router connects disparate networks and forwards packets based on Layer 3 IP addresses. Operating systems also maintain local **Routing Tables** to direct outgoing traffic.

### 4.2 The Routing Table & Default Gateway
A routing table contains entries mapping destination prefixes to next-hop gateways, interfaces, and metrics:
* **Default Gateway:** The next-hop router used when a destination IP does not match a more specific local route in the routing table.
* **Longest Prefix Match:** When multiple routes match a destination, systems always select the most specific matching prefix (e.g., a `/24` route takes precedence over a `/16` route, which takes precedence over the default route `0.0.0.0/0`).

### 4.3 Packet Forwarding Across Routers
When a packet traverses a router:
1. The router receives the Ethernet frame, strips the Layer 2 header, and inspects the Layer 3 IP packet.
2. It consults its routing table and makes a forwarding decision.
3. It builds a brand-new Ethernet frame for the next network segment, decrementing the IP packet's **TTL (Time to Live)** by 1.
4. Source and destination IP addresses remain unchanged during standard routing (unlike NAT).

---

## 5. Network Address Translation (NAT)

### 5.1 What is NAT?
Standardized in **RFC 3022**, **NAT (Network Address Translation)** modifies IP address information in packet headers while packets transit network boundaries. Its primary use case is allowing multiple private-address devices (RFC 1918 ranges like `192.168.x.x`) to share a single public IP address.

### 5.2 Key NAT Variations
* **Static NAT:** One-to-one mapping between a private IP and a public IP.
* **Dynamic NAT:** Translates internal IPs using a pool of external public addresses.
* **PAT (Port Address Translation / NAT Overload):** Allows thousands of internal devices to share a single public IP simultaneously by appending unique transport-layer source ports to outgoing connections.

### 5.3 NAT is NOT a Firewall
NAT translates addressing information; it does not enforce security policy. While NAT makes unsolicited inbound connections difficult without pre-existing translation entries, it is never a substitute for a properly configured firewall.

---

## 6. Firewalls and Boundary Defence

### 6.1 Stateful vs. Stateless Firewalls
* **Stateless Firewall:** Evaluates each packet in isolation based strictly on static rule criteria (Five-Tuple: Source IP, Destination IP, Source Port, Destination Port, Protocol) without maintaining connection context.
* **Stateful Firewall:** Tracks active connection states (`NEW`, `ESTABLISHED`, `RELATED`, `INVALID`) using a connection state table, automatically permitting return traffic for authorized outbound connections.

### 6.2 Firewall Actions & Policy Design
* **Allow vs. Block vs. Drop vs. Reject:** Allow permits traffic; block/drop silently discards traffic without response; reject denies traffic and actively returns an ICMP unreachable message.
* **Default Deny:** The industry standard security posture where all traffic not explicitly permitted by rule evaluation is blocked by default.
* **Host-Based vs. Network Firewalls:** Network firewalls protect perimeter boundaries, while host-based tools (such as Windows Firewall or Linux `nftables`) protect individual systems at the kernel level.
