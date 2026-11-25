# DNS Troubleshooting Playbook & Reference Guide
**Author:** Serah Mulwa  
**Date:** November 3, 2026  
**Module:** Day 16 - DNS Security, Investigation, and Threat Detection  

---

## 1. Overview & Purpose
When users or systems lose connectivity to a service, DNS is frequently the root cause or the first place symptoms manifest. As a junior SOC analyst or network support technician, you must be able to systematically distinguish client-side configuration errors, resolver degradation, and upstream authoritative failures without guessing or flushing caches blindly.

According to enterprise troubleshooting standards (such as Microsoft networking guidelines), **always begin DNS troubleshooting from the client side** unless clear telemetry points to a server-side outage.

---

## 2. Client-Side Configuration Audit

### 2.1 Linux / Parrot OS Client Verification
Verify your operating system's local resolver configuration and Name Service Switch (NSS) mappings using native utilities:

1. **Check Upstream Resolvers:**
   ```bash
   cat /etc/resolv.conf
   ```
   * *What to look for:* Active `nameserver` IP entries pointing to your local gateway or trusted resolver.

2. **Test OS-Level Resolution (NSS):**
   ```bash
   getent ahosts example.com
   ```
   * *What to look for:* Verifies how the operating system queries name resolution across local files (`/etc/hosts`) and DNS.

3. **Check NetworkManager Status (Optional):**
   ```bash
   nmcli dev show | grep DNS
   ```
   * *What to look for:* Interface-specific DNS server bindings.

---

### 2.2 Windows Host Client Verification
When running virtualized environments on a Windows host, audit the host's networking and DNS stack via PowerShell:

1. **Audit All Network Adapters:**
   ```powershell
   ipconfig /all
   ```
   * *What to identify:* IPv4 address, subnet mask, default gateway, and assigned DNS server IPs for active adapters.

2. **Enumerate Assigned DNS Servers:**
   ```powershell
   Get-DnsClientServerAddress
   ```

3. **Test Windows Name Resolution:**
   ```powershell
   Resolve-DnsName example.com -Type A
   nslookup example.com
   ```

---

## 3. Common Error Symptoms & Resolution Table

| Symptom / Response Code | Root Cause Indicator | Recommended Actionable Step |
| :--- | :--- | :--- |
| **NXDOMAIN** (Non-Existent Domain) | The requested domain name does not exist in the authoritative zone. | Verify spelling, check for typos, or confirm if the domain has expired or been decommissioned. |
| **SERVFAIL** (Server Failure) | The upstream resolver encountered an internal error or failed to complete resolution. | Check upstream resolver health, network routing, or underlying DNSSEC validation errors. |
| **REFUSED** | The authoritative nameserver or resolver deliberately blocked the query request. | Examine firewall rules, Access Control Lists (ACLs), or rate-limiting configurations. |
| **Timeout / No Response** | Packet dropped or blocked along the path; resolver unreachable. | Test basic network reachability (`ping <resolver-ip>`) and check local port 53 filtering. |
| **Stale or Incorrect Answer** | Client or intermediate resolver cached outdated zone records. | Inspect the record's TTL value and compare responses directly against the authoritative nameserver using `dig`. |

---

## 4. The Professional Troubleshooting Sequence
When faced with a reported connectivity failure, follow this exact 7-step triage methodology:

1. **Verify Physical & Network Connectivity:** Ensure the workstation has an active IP address assignment and can reach the local network gateway.
2. **Check Configured DNS Servers:** Inspect `/etc/resolv.conf` (Linux) or `ipconfig /all` (Windows) to verify correct resolver assignments.
3. **Test Scope of Failure:** Determine whether *all* external domains fail or only a single specific domain.
4. **Examine Response Codes:** Identify whether error states return `NXDOMAIN`, `SERVFAIL`, or request timeouts.
5. **Compare OS Resolution with `dig` / `nslookup`:** Differentiate between local browser/OS caching issues and true upstream resolver failures.
6. **Determine Scope (Client vs. Server):** Is the issue isolated to a single workstation's network stack adapter, or is the entire subnet affected?
7. **Document & Escalate:** Record exact command strings, outputs, and timestamps. Escalate to infrastructure teams only if server-side intervention is required.

> ⚠️ **Golden Rule for Analysts:** Do not immediately flush DNS caches or modify network configurations blindly. Observe and understand what is failing first.
