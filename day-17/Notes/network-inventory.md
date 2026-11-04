# Network Configuration Inventory (Windows Host & Parrot OS Guest)

**Author:** Serah Mulwa  
**Date:** November 4, 2026  
**Module:** Day 17 - Network Control & Boundary Defence  

---

## 1. Executive Summary

This inventory documents the foundational network parameters, active interfaces, IP address assignments, routing tables, and neighbor cache entries across both my host operating system (Windows) and guest virtual machine (Parrot OS). Establishing a baseline network configuration is a vital operational step for incident response, troubleshooting addressing issues, and detecting network anomalies.

*Note: Sensitive home network configuration details have been sanitized using standardized RFC 1918 documentation ranges (`192.0.2.0/24` and `10.0.2.0/24`) to adhere to security best practices.*

---

## 2. Guest OS Baseline Inventory (Parrot OS)

### 2.1 Operating System & Package Verification
- **Distribution:** Parrot Security OS 7.4 (echo)
- **Kernel & Tools:** Linux Kernel with `iproute2-6.15.0`, `ss`, `python3` (3.13.5), `nftables` (v1.1.3), and `ufw` (0.36.2) operational.

### 2.2 Network Interfaces (`ip -br link` / `ip -br addr`)
| Interface Name | State | MAC Address | Assigned IPv4 Address | Subnet Mask / Prefix | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `lo` | UNKNOWN | `00:00:00:00:00:00` | `127.0.0.1` | `/8` | Internal loopback interface |
| `enp0s3` | UP | `08:00:27:3b:a4:b2` | `10.0.2.15` | `/24` | Primary virtual Ethernet adapter (NAT Mode) |

### 2.3 Routing Table & Route Lookup (`ip route`)
- **Default Route:** `default via 10.0.2.2 dev enp0s3 proto dhcp src 10.0.2.15 metric 100`
- **Subnet Route:** `10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.15 metric 100`
- **Route Lookup Test (`ip route get 1.1.1.1`):** Resolves destination `1.1.1.1` via next-hop gateway `10.0.2.2` bound to interface `enp0s3`.

### 2.4 Neighbor / ARP Cache (`ip neigh`)
| IP Address | Interface | Hardware (MAC) Address | State | Description |
| :--- | :--- | :--- | :--- | :--- |
| `10.0.2.2` | `enp0s3` | `52:54:00:12:35:00` | REACHABLE | VirtualBox NAT Gateway / Router |

### 2.5 Link Statistics (`ip -s link`)
- **Receive (RX) Statistics:** 18,050 packets received, 0 bytes error, 0 dropped.
- **Transmit (TX) Statistics:** 4,381 packets transmitted, 0 bytes error, 0 dropped.
- **Assessment:** Link performance is optimal with zero dropped frame counters across transmit and receive buffers.

---

## 3. Host OS Baseline Inventory (Windows)

### 3.1 Network Adapters (`Get-NetAdapter`)
| Adapter Name | Status | Link Speed | MAC Address | Interface Description |
| :--- | :--- | :--- | :--- | :--- |
| `Wi-Fi` | Up | 468 Mbps | `DC-FB-48-12-EF-EE` | Intel(R) Wireless-AC 9560 160MHz |
| `Ethernet 2` | Up | 1 Gbps | `0A-00-27-00-00-05` | VirtualBox Host-Only Ethernet Adapter |
| `Ethernet` | Disconnected | 0 bps | `48-2A-E3-4E-8F-D2` | Physical RJ-45 Controller |

### 3.2 IP Configuration (`Get-NetIPConfiguration`)
- **Active Wireless Interface (`Wi-Fi`):**
  - IPv4 Address: `192.168.100.3` (Subnet Prefix: `/24`)
  - IPv4 Default Gateway: `192.168.100.1`
  - Network Profile: Public / Bunny 6
- **Virtual Interface (`Ethernet 2`):**
  - IPv4 Address: `192.168.56.1` (Subnet Prefix: `/24`)
  - IPv4 Default Gateway: None (Host-Only Local Scope)

### 3.3 Routing Summary (`Get-NetRoute -AddressFamily IPv4`)
- **Default Route (`0.0.0.0/0`):** NextHop `192.168.100.1` via `Wi-Fi` interface (Metric 0).
- **Host Subnet Routes:** Direct on-link routes for `192.168.100.0/24` (`Wi-Fi`) and `192.168.56.0/24` (`Ethernet 2`).

---

## 4. Operational Analysis & Key Takeaways

1. **Dual System Verification:** Both systems maintain distinct physical and virtual network stacks. The Parrot OS virtual machine utilizes VirtualBox's NAT engine (`10.0.2.2`), ensuring guest internet access while abstracting internal host interfaces.
2. **Gateway Resolution:** The default gateway settings were successfully mapped across both environments, providing clear visibility into how outbound traffic exits local interfaces before entering perimeter networks.
3. **Analytical Baseline:** Verifying normal interface operation (0 error drops) provides an essential baseline for detecting abnormal behavior, network flooding, or unauthorized interface manipulation.
