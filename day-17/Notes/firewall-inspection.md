# Lab Investigation Report: Host Firewall Inspection & Telemetry

**Author:** Serah Mulwa

**Date:** November 4, 2026

**Module:** Day 17 - Network Control & Boundary Defence

## 1. Executive Summary

This lab focused on non-destructive host firewall reconnaissance across both Windows and Linux (Parrot OS) environments. Before attempting to write rules or modify policies, security engineers must understand how active firewall profiles, default actions, port filters, and audit logs operate. This report documents our PowerShell inspections of Windows Firewall profiles, port filters, administrative log access resolutions, and Linux `nftables` / `ufw` evaluations.

## 2. Windows Firewall Profile & Rule Inspection

### 2.1 Profile Status Evaluation (`Get-NetFirewallProfile`)

Running our initial PowerShell query revealed the state of the three primary Windows firewall profiles:

```powershell
Get-NetFirewallProfile | Format-Table Name, Enabled, DefaultInboundAction, DefaultOutboundAction -AutoSize
```

* **Observed Output:**
  * **Domain:** Enabled (`True`)
  * **Private:** Enabled (`True`)
  * **Public:** Enabled (`True`)

* **Analyst Insight:** All profiles are active, ensuring that whether the workstation is connected to a secure domain, a trusted home network, or a public Wi-Fi hotspot, host boundary defense remains enabled.

### 2.2 Active Rule & Port Filter Sampling (`Get-NetFirewallRule`)

Because modern operating systems maintain thousands of internal firewall rules, we sampled enabled rules and inspected their underlying port allocations using:

```powershell
Get-NetFirewallRule -Enabled True | Get-NetFirewallPortFilter | Select-Object Protocol, LocalPort, RemotePort | Format-Table -AutoSize
```

* **Observed Port Bindings:**
  * Network Discovery and SSDP services mapped to UDP ports `1900` and `5353`.
  * Dynamic host configuration protocol (DHCP) bound to UDP source port `68` and destination port `67`.
  * Remote Management and RPC rules bound to specific local service ports while maintaining scoped remote connectivity.

## 3. Windows Firewall Logging Investigation (`pfirewall.log`)

To investigate firewall audit logs, we encountered and successfully resolved common administrative hurdles:

1. **Path & Permission Verification:**
   Initial attempts to read `C:\WINDOWS\System32\LogFiles\Firewall\pfirewall.log` from a standard user prompt resulted in `UnauthorizedAccessException`. 
   
2. **Elevated Remediation:**
   Launching PowerShell with **Administrator privileges** resolved the access issue. After ensuring logging was enabled and generating test traffic (`ping 8.8.8.8`), we queried the log tail:

   ```powershell
   Get-Content "$env:windir\System32\LogFiles\Firewall\pfirewall.log" -Tail 20
   ```

* **Observed Log Output:**
  ```text
  2026-11-04 12:37:55 ALLOW UDP 192.168.100.3 142.250.75.110 52039 443 0 - - - - - - SEND 13820
  2026-11-04 12:38:01 DROP ICMP 192.168.100.1 192.168.100.3 - - 84 - - - - - 8 0 - RECEIVE 4
  ```

* **Forensic Analysis:** The audit log successfully captured stateful session events, recording both outbound `ALLOW` actions (HTTPS traffic to Google IP) and inbound `DROP` actions (unsolicited ICMP / broadcast noise hitting the network interface).

## 4. Parrot OS Firewall Inspection (`nftables` & `UFW`)

We inspected the Linux kernel's underlying packet filtering framework on Parrot OS:

1. **nftables Ruleset Inspection:**
   ```bash
   sudo nft list ruleset
   ```
   Revealed active Netfilter chains (`ufw-before-input`, `ufw-before-output`, `ufw-user-input`) managed by the kernel.

2. **UFW Status & Policy Testing:**
   * Checked status: `sudo ufw status verbose` (initially inactive).
   * Enabled UFW and enforced default deny inbound: `sudo ufw default deny incoming`.
   * Adjusted logging levels (`sudo ufw logging medium`).
   * Safely disabled UFW (`sudo ufw disable`) after inspection to return the VM to its clean operational baseline.

## 5. Portfolio Visual Artifacts

The execution screenshots supporting this lab are stored in `day-17/screenshots/`:
* `124-windows-firewall-profiles-and-rules.png` — Profile states and rule sampling.
* `125-windows-firewall-port-filters.png` — Port filter protocol mappings.
* `127-windows-firewall-log-access-denied.png` — Permission handling verification.
* `129-windows-firewall-pfirewall-log-output.png` — Live `ALLOW` / `DROP` firewall audit entries.
* `117-ufw-enable-and-default-policies.png` — Linux UFW activation and default-deny enforcement.
* `120-nftables-ruleset-inspection-part1.png` — `nftables` kernel chain inspection.
