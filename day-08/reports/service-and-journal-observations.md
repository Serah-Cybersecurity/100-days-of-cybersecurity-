# Day 8 - Service and Systemd Journal Observation Report

## Overview
Audited system initialization and active background daemons using `systemctl`, and investigated system event logs using `journalctl` within the Parrot OS environment.

## Audit Findings & Observations

### 1. Init System & Service Management Verification
* **System Manager:** Verified active systemd service management via `systemctl`.
* **Running Services Observed:** Successfully listed 23 active background units. Examples include:
  1. `NetworkManager.service` — Manages network interfaces and connection states.
  2. `cron.service` — Executes scheduled background tasks and system maintenance jobs.
  3. `systemd-journald.service` — Collects, structures, and indexes kernel and system log data.

### 2. Systemd Journal Query Analysis (`journalctl`)
* **Command Executed:** `journalctl -n 30 --no-pager` and `journalctl --since "1 hour ago" --no-pager`
* **Journal Accessibility:** Successfully queried the systemd journal database. A standard user permission notice was observed (*"You are currently not seeing messages from other users and the system"*), indicating that full system-wide log auditing requires membership in groups such as `adm` or `systemd-journal`.
* **Example Log Messages:**
  * *Entry 1:* `Starting app-org.kde.spectacle.service - Spectacle screenshot capture utility.`
  * *Entry 2:* `Starting plasma-krunner.service - KRunner...`
* **What the Messages Indicate:** They provide a chronological audit trail of user-space application executions, desktop utility triggers, and IPC (D-Bus) service handshakes.
* **What They Do Not Prove:** The presence of these logs confirms what was recorded by the active session, but log absence or normal user activity does not definitively prove a system is free from compromise. Sophisticated attackers can attempt to clear logs or tamper with daemons during an intrusion.
