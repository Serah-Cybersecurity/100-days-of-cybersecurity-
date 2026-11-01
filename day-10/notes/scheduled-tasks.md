# Day 10 - Scheduled Tasks & Persistence Mechanism Audit Notes

## 1. Core Concepts & Definitions
* **Scheduled Task:** Work configured by an operating system or user to execute automatically at defined intervals, times, or system events (such as system startup).
* **Persistence:** Mechanisms that allow malware, backdoors, or scripts to survive reboots and maintain continuous access. Adversaries frequently abuse cron and systemd timers to achieve persistence.

## 2. Practical Triage Commands Executed
* **User Crontab Check:**
  * **Command:** `command -v crontab` and `crontab -l`
  * **Observation:** Verified utility availability and queried the user scheduling table. (Sanitized observation: No accessible user crontab configured for the standard unprivileged account).
* **System-Wide Cron Directory Audit:**
  * **Command:** Read-only Bash loop iterating through `/etc/cron.d`, `/etc/cron.hourly`, `/etc/cron.daily`, `/etc/cron.weekly`, and `/etc/cron.monthly`.
  * **Observation:** Listed standard system automation drop-ins (such as `apache2`, `logrotate`, `e2scrub_all`, `sysstat`) safely without opening internal script contents.
* **Systemd Timers Audit:**
  * **Command:** `systemctl list-timers --all --no-pager`
  * **Observation:** Audited 17 active calendar-based systemd timer units (including `apt-daily.timer`, `logrotate.timer`, and `lynis.timer`) and their corresponding service triggers.

## 3. Cron Syntax Reference
* **Format:** `[Minute] [Hour] [Day_of_Month] [Month] [Day_of_Week] [Command]`
* **Example Syntax Practice (`*/15 * * * *`):** Evaluated expressions to schedule commands at 15-minute intervals.

## 4. Defensive Security & Threat Hunting Insights
* **Modern Persistence Vectors:** Incident responders must inspect systemd timers alongside traditional cron jobs, as modern Linux malware frequently implements systemd persistence.
* **Data Sanitization Rule:** Never publish raw crontab contents, internal script paths, or personal usernames to public GitHub repositories to maintain security compliance.
