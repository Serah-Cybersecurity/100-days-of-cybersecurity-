# Lab Investigation Report: ARP and Routing Mechanics

**Author:** Serah  Mulwa

**Date:** November 4, 2026

**Module:** Day 17 - Network Control & Boundary Defence

## 1. Executive Summary

This lab investigation bridges theoretical network routing with practical Layer 2 neighbor resolution. By examining our Parrot OS virtual machine's routing table and neighbor cache, we explored how a host identifies its local default gateway, how ARP / neighbor states transition dynamically during active communications, and why computers must resolve the MAC address of their local router rather than a remote internet destination.

## 2. Default Gateway Identification

Before a host can transmit packets across subnets, it must identify its default gateway—the next-hop router responsible for forwarding traffic outside the local network.

* **Inspection Command:**
  ```bash
  ip route show default
  ```
* **Observed Output:**
  ```text
  default via 10.0.2.2 dev enp0s3 proto dhcp src 10.0.2.15 metric 100
  ```
* **Technical Analysis:** The kernel routes any traffic destined for external or unknown subnets through the next-hop gateway IP `10.0.2.2` via the primary network interface `enp0s3`.

## 3. Neighbour Table & State Analysis

Linux maintains a neighbor cache (the ARP table for IPv4) to map IP addresses to physical MAC addresses. Before generating traffic, our inspection showed the gateway entry in a `STALE` state.

### Understanding Neighbour Cache States:
* **`STALE`**: The cached IP-to-MAC mapping (`52:54:00:12:35:00`) is known and valid, but it has not been recently verified by active traffic.
* **`REACHABLE`**: The neighbor's reachability has been recently confirmed through active bidirectional traffic.
* **`INCOMPLETE`**: Address resolution is currently in progress (waiting for an ARP reply).
* **`FAILED`**: Resolution attempts failed completely.

## 4. Controlled Traffic Generation & State Transition

To test how the operating system manages neighbor states, we sent a single controlled ICMP Echo Request to our virtual default gateway:

* **Command Executed:**
  ```bash
  ping -c 1 10.0.2.2
  ```
* **Execution Result:** 
  1 packet transmitted, 1 received, 0% packet loss, RTT 0.306 ms.

* **Post-Ping Neighbour Table Inspection (`ip neigh show`):**
  ```text
  10.0.2.2 dev enp0s3 lladdr 52:54:00:12:35:00 REACHABLE
  ```

* **Observation:** Immediately following successful packet transmission and reception, the kernel probed and updated the neighbor state from **`STALE`** to **`REACHABLE`**.

## 5. Critical Conceptual Questions & Answers

### 1. Was the gateway present in the neighbour table before the connectivity test?
Yes, but its state was marked as `STALE`, indicating an existing cached entry that had not been recently verified.

### 2. Did its state change afterwards?
Yes. Sending traffic forced the kernel to re-verify reachability, transitioning the state to `REACHABLE`.

### 3. What MAC address is associated with it?
`52:54:00:12:35:00`, which corresponds to the virtual gateway interface configured by the VirtualBox hypervisor.

### 4. Why does the computer need the gateway's MAC address instead of the remote internet server's MAC address?
**The Core Networking Rule:** Layer 2 Ethernet frames cannot cross routers; they operate strictly on the local physical segment. When your computer communicates with an external server (like `1.1.1.1`), that server's MAC address does not exist on your local network. Therefore, your computer must wrap the packet inside an Ethernet frame addressed to your **local default gateway's MAC address**. The local router then unpacks the packet and forwards it across the internet.

## 6. Job Market Application

* **IT Support & Network Engineering:** Technicians use `ip route` and `ip neigh` daily to diagnose dropped connections. If a gateway MAC shows as `FAILED`, it signals a physical link disruption or VLAN misconfiguration.
* **SOC Analysts:** During incident investigations, understanding neighbor tables helps analysts map lateral movement and identify unauthorized communication between local hosts.
