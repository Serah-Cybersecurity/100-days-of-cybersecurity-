# Day 10 - Linux Triage Script Professional Test Report

## 1. Executive Summary & Tool Scope
* **Script Name:** `linux_triage.sh`
* **Purpose:** Collect a read-only, point-in-time system health and configuration snapshot for defensive analysis.
* **Operational Scope:** Local Parrot OS virtual machine environment.
* **Classification:** Beginner defensive utility (not a forensic memory acquisition tool or automated malware verdict generator).

## 2. Rigorous Test Matrix Execution Results

| Test Case | Procedure | Expected Behaviour | Actual Result |
| :--- | :--- | :--- | :--- |
| **Syntax Validation** | Run `bash -n` on the script | No syntax errors | **Passed:** Script parsed cleanly with exit code `0`. |
| **Basic Execution** | Run the script normally | Headings and available information are displayed | **Passed:** Structured section banners and metadata rendered correctly. |
| **Process Inspection** | Review the process section | PID, PPID, user, and related attributes displayed via `ps` | **Passed:** Successfully listed processes sorted by parent PID (`--sort=ppid`). |
| **Service Query** | Review the service section | Running service information displayed via `systemctl` | **Passed:** Displayed active running service units in memory. |
| **Socket Query** | Review the socket section | Listening TCP socket information displayed via `ss` | **Passed:** Queried socket tables successfully. |
| **Timer Query** | Review the timer section | Systemd timer information displayed | **Passed:** Listed active calendar timers (`systemctl list-timers`). |
| **Crontab Privacy** | Review the crontab section | Script reports status without printing raw crontab contents | **Passed:** Reported crontab presence/absence status while protecting user privacy. |
| **Missing-Command Handling** | Observe sections with unavailable commands | Script displays an explanatory message instead of assuming success | **Passed:** Utilized `command -v` wrappers to handle missing dependencies gracefully. |

## 3. Code-Review & Architectural Evaluation
1. **Does it alter any processes or services?** No. All queries are strictly read-only observational commands.
2. **Does it stop or start services?** No. The script never invokes modification commands like `systemctl stop` or `systemctl restart`.
3. **Does it modify scheduled tasks?** No. It only inspects system cron directories and queries user crontab status.
4. **Does it collect the contents of the current user's crontab?** No. It deliberately avoids collecting raw crontab contents to prevent leaking sensitive file paths or credentials.
5. **Does it inspect every possible persistence mechanism?** No. It focuses on cron and systemd timers, omitting alternate vectors like startup scripts, shell profile injections, or kernel modules.
6. **Does successful execution prove that a system is free of malware?** **No.** The script provides a limited system snapshot to guide human investigation; it cannot provide a definitive malware verdict or full forensic guarantee.

## 4. Conclusion
The `linux_triage.sh` automation script successfully passed all syntax, execution, and boundary-testing criteria, adhering to professional security engineering and data minimization standards.
