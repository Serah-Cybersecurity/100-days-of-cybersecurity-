# Incident Troubleshooting Playbook: Resolving DNS Failures in Enterprise Networks

**Author:** Serah Mulwa

**Date:** November 3, 2026

**Module:** Day 16 - DNS Security, Investigation, and Threat Detection

## 1. Introduction & Investigative Philosophy

When troubleshooting network connectivity issues, users rarely report clean technical errors. A typical user complaint sounds like this: 

> *"I can browse websites using their IP addresses, but domain names aren't resolving."*

As a junior security or support analyst, understanding how to decode this symptom is crucial. Being able to access a website via its raw IP address (e.g., `142.250.190.46`) proves that the physical network stack, local gateway, and routing configuration are healthy. The failure is isolated entirely to **name resolution**. 

---

## 2. Potential Root Causes

Before jumping to conclusions, an analyst must evaluate several possible root causes:

1. **Incorrect DNS Configuration:** Workstations pointing to dead, decommissioned, or misconfigured resolver IP addresses.
2. **Resolver Availability Failures:** The enterprise internal DNS resolver is offline, overwhelmed, or blocked by a firewall.
3. **Stale DNS Caching:** Outdated IP mappings stored in client operating system caches.
4. **Upstream ISP / Carrier Outages:** Recursive resolvers failing to reach authoritative root or TLD servers.
5. **Missing or Misconfigured Records:** Specific domains failing due to zone file errors.
6. **Network Filtering / Security Controls:** Corporate firewalls blocking Port 53 or intercepting traffic.

---

## 3. The Professional 8-Step Troubleshooting Methodology

Rather than guessing or randomly tweaking network adapters, professional engineers follow a strict, repeatable 8-step investigative sequence:

| Step | Investigative Question | Recommended Tool / Command | What You Are Looking For |
| :--- | :--- | :--- | :--- |
| **1** | Is the computer connected to the network? | `ping -c 4 8.8.8.8` or `ip link` | Verifies basic Layer 3 connectivity and default gateway reachability. |
| **2** | Which DNS server is configured? | `ipconfig /all` (Windows) / `cat /etc/resolv.conf` (Linux) | Checks whether the correct enterprise resolver IP is assigned. |
| **3** | Can the computer resolve a known domain? | `dig example.com` or `nslookup example.com` | Tests if basic name-to-IP resolution functions at all. |
| **4** | Which DNS response code is returned? | `dig +noall +answer example.com` | Identifies error flags (`SERVFAIL`, `NXDOMAIN`, `REFUSED`). |
| **5** | Do different record types behave differently? | `dig A example.com`, `dig MX example.com` | Determines if failure affects all records or specific types (like mail servers). |
| **6** | Is the issue limited to one client? | Compare results with neighboring workstations | Rules out whether the issue is isolated or network-wide. |
| **7** | Are relevant DNS service errors recorded? | Windows Event Viewer or Linux `/var/log/syslog` | Checks server-side logs for daemon crashes or timeouts. |
| **8** | Does packet evidence support behaviour? | Wireshark (`dns` filter) | Inspects raw packet handshakes, query retries, and dropped frames on Port 53. |

---

## 4. Microsoft's Enterprise Troubleshooting Guidance

Enterprise diagnostic frameworks (such as Microsoft's official DNS troubleshooting standards) emphasize a **dual-perspective collection strategy**:
* **Client-Side Diagnostics:** Gather local configuration data (`ipconfig /all`, DNS cache dumps via `ipconfig /displaydns`) to understand what queries the workstation is sending and where.
* **Server-Side Diagnostics:** Inspect DNS server event logs, query logs, and performance counters to verify whether the resolver is receiving incoming requests and successfully communicating with external authoritative servers.

---

## 5. The Professional Golden Rule

> **"Never immediately change DNS settings to a public resolver (like `8.8.8.8` or `1.1.1.1`) as a quick fix."**

### Why This Rule Matters:
In corporate enterprise environments, internal DNS configuration is deeply tied to **Active Directory domain authentication, internal file shares, intranet portals, split-horizon DNS filtering, and internal security controls**. 

Blindly switching a corporate workstation to a public resolver instantly breaks access to internal enterprise resources. Always establish the root cause through systematic triage before applying any remediation.
