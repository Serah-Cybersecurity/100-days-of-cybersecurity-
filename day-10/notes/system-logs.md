# Day 10 - System Logs & Service Investigation Notes

## 1. Core Concepts & Definitions
* **System Log:** A recorded event or message produced automatically by the operating system kernel, background daemons, or applications.
* **Systemd Journal:** A centralized binary logging architecture managed by `systemd` that collects kernel and service logs efficiently.

## 2. Practical Triage Commands Executed
* **Recent System Warnings Audit:**
  * **Command:** `journalctl -b -p warning --no-pager -n 25`
  * **Flags Breakdown:**
    * `-b`: Restricts logs exclusively to the current system boot.
    * `-p warning`: Filters logs by priority severity (warnings and above).
    * `--no-pager`: Outputs text directly without opening interactive scrolling views.
    * `-n 25`: Limits output to the 25 most recent lines.
  * **Observation:** Successfully parsed system warning entries under unprivileged user permissions, respecting operational group boundaries without forced privilege escalation.
* **Service-Specific Log Query:**
  * **Command:** `journalctl -u cron --since today --no-pager`
  * **Observation:** Targeted logs exclusively for the `cron` service unit from midnight onward, demonstrating efficient narrow query filtering to avoid log floods.

## 3. Defensive Security & Threat Hunting Insights
* **The Power of Narrow Queries:** In enterprise environments handling gigabytes of log telemetry, filtering by time range (`--since`), service unit (`-u`), and priority (`-p`) is essential for rapid incident triage.
* **Data Sanitization Rule:** Always redact internal usernames, private IP addresses, and sensitive file paths before publishing log outputs to public GitHub portfolios.
