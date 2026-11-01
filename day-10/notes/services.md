# Day 10 - Linux Background Services & Systemd Audit Notes

## 1. Core Concepts & Definitions
* **Process vs. Service:** A process is a dynamic, temporary running instance of a program in RAM assigned a PID. A service is a persistent background workload managed through systemd unit files.
* **Service States:**
  * **Installed:** The software unit file exists on disk (`/lib/systemd/system/` or `/etc/systemd/system/`).
  * **Running (Active):** The service unit is actively executing in memory and supervising processes.
  * **Enabled:** The service has configuration symlinks set up to start automatically during system boot.

## 2. Practical Service Audits Executed
* **Active Running Services Audit:**
  * **Command:** `systemctl list-units --type=service --state=running --no-pager`
  * **Observed Total:** 23 active service units in memory.
  * **Key Units Identified:** `cron.service` (scheduler), `dbus.service` (system message bus), `lightdm.service` (display manager), `NetworkManager.service` (network interface daemon), `systemd-journald.service` (log collector), `virtualbox-guest-utils.service` (VM integration).
* **Startup Persistence Audit:**
  * **Command:** `systemctl list-unit-files --type=service --state=enabled --no-pager`
  * **Observed Total:** 41 enabled service unit files configured for automatic boot launch.
  * **Key Units Identified:** `apparmor.service` (MAC security), `ufw.service` (firewall), `ssh.service` / `sshd-keygen.service` (remote access management).

## 3. Defensive Security & Threat Hunting Insights
* **Running vs. Enabled Discrepancies:** Comparing active memory units against enabled unit files reveals operational gaps. For example, a service can be *enabled* for boot but currently stopped, or *running* dynamically without boot persistence.
* **Persistence Vector Auditing:** Attackers frequently drop unauthorized `.service` files inside `/etc/systemd/system/` to maintain backdoors across system reboots. Auditing enabled unit files is a primary step in incident response triage.
* **Read-Only Safety Principle:** System audits must strictly utilize read-only observational queries (`list-units`, `list-unit-files`) to prevent accidental service disruptions or system crashes.
