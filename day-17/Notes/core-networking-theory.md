# Core Networking Theory: DHCP, DORA, and Infrastructure Security

**Author:** Serah Mulwa  

**Date:** November 4, 2026  

**Module:** Day 17 - Network Control & Boundary Defence  

## 1. Introduction to Core Networking Theory

When building a career in cybersecurity or network engineering, understanding packet-level analysis (Day 15) and application protocols (Day 16) is only part of the equation. You must also understand how devices acquire network identities, resolve local neighbors, route across subnets, and enforce security boundaries. This document breaks down the foundational theory behind **Dynamic Host Configuration Protocol (DHCP)**.

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

---

## 3. The DHCP DORA Process (Step-by-Step)

The foundational mechanism of DHCP allocation follows the **DORA** lifecycle:

```
[ Client Device ]                                  [ DHCP Server ]
       |                                                  |
       |--- 1. DHCPDISCOVER (Broadcast: 255.255.255.255)->|
       |                                                  |
       |<-- 2. DHCPOFFER (Proposed IP & Lease Configuration)
       |                                                  |
       |--- 3. DHCPREQUEST (Formal Acceptance Broadcast)->|
       |                                                  |
       |<-- 4. DHCPACK (Lease Final Confirmation) --------|
```

### Step 1: Discover (`DHCPDISCOVER`)
* **Mechanism:** The client lacks an IP address and broadcasts a UDP packet across the local segment.
* **Ports & Addressing:** Source IP `0.0.0.0`, Destination IP `255.255.255.255`, Source Port `68`, Destination Port `67`.
* **Intent:** Looking for any active DHCP server on the local broadcast domain.

### Step 2: Offer (`DHCPOFFER`)
* **Mechanism:** Available DHCP servers respond with a proposed IP address lease, subnet mask, gateway, and DNS configuration.

### Step 3: Request (`DHCPREQUEST`)
* **Mechanism:** The client broadcasts its formal acceptance of a specific server's offered configuration, implicitly notifying competing servers to release their reserved IPs back into the pool.

### Step 4: Acknowledgement (`DHCPACK`)
* **Mechanism:** The chosen DHCP server confirms the lease. The client binds the IP address to its network interface card and joins the active network.

---

## 4. Advanced DHCP Concepts

* **Lease Renewal:** Clients attempt to renew their IP lease at the 50% mark of their expiration timer using unicast communication.
* **DHCP Scope:** The contiguous pool of IP addresses authorized for allocation.
* **DHCP Reservation (Static DHCP):** Tying a specific IP address to a physical MAC address to ensure critical infrastructure (printers, servers) never changes its address.
* **DHCP Relay (IP Helper):** Routers block broadcast traffic (`255.255.255.255`) from crossing subnets. A relay agent catches client broadcast discovery messages and unicasts them across networks to a centralized DHCP server.

---

## 5. Defensive Controls & Security Mitigation

To protect enterprise networks from DHCP abuse, security teams implement:
* **DHCP Snooping:** A switch-level feature that classifies ports as *Trusted* (connected to legitimate servers) or *Untrusted* (connected to user ports). It inspects traffic and drops unauthorized `DHCPOFFER` or `DHCPACK` messages originating from untrusted ports.
* **Port Security & Rate Limiting:** Restricting the number of DHCP discover requests per port to mitigate **DHCP Starvation** attacks.
