# Day 10 - Linux Process and Service Triage

## Overview
This project documents a beginner defensive-security exercise focused on inspecting Linux processes, running services, scheduled-task mechanisms, and listening TCP sockets within a simulated virtual machine environment.

## Learning Objectives
* Explain the distinction between processes and services.
* Inspect selected process attributes using `ps` and `/proc`.
* Examine systemd service and calendar timer configurations.
* Inspect listening TCP sockets using `ss`.
* Understand the investigative value and limitations of system logs (`journalctl`).
* Build, test, and document a read-only Bash triage script (`linux_triage.sh`).
* Document direct observations separately from analytical interpretations.

## Environment
* **Host Operating System:** Windows
* **Virtualisation:** Oracle VirtualBox
* **Guest Operating System:** Parrot OS
* **Core Tools:** Bash, `ps`, `systemctl`, `ss`, `journalctl`, `crontab`, `find`

## Project Structure
```text
day-10/
├── README.md
├── notes/
│   ├── processes.md
│   ├── services.md
│   ├── scheduled-tasks.md
│   └── triage-method.md
├── lab/
│   └── samples/
├── scripts/
│   └── linux_triage.sh
├── reports/
│   └── test-results.md
└── screenshots/
    ├── 01-triage-methodology-notes.png
    ├── 02-top-process-monitoring.png
    ├── ...
    └── 15-triage-script-testing-and-chmod.png
```

   ## What I Built
The linux_triage.sh script collects a limited, point-in-time system health snapshot to guide human investigation.

## Core Design Principles:
-Strictly Read-Only: Never modifies services, stops processes, changes permissions, or deletes files.

-Defensive Error Handling: Uses command -v conditional wrappers to degrade gracefully if binaries are missing.

-Data Minimization: Excludes raw crontab contents and restricts process reporting to command names (comm) to protect user privacy and avoid leaking sensitive environment variables.

## Testing & Validation
The script underwent rigorous syntax validation (bash -n) and empirical execution testing across all functional modules. Results, test matrices, and code-review evaluations are documented in reports/test-results.md.

## Key Findings & Analytical Method
-Observation vs. Interpretation: Maintained strict discipline in separating raw command output from analytical conclusions.

-Unprivileged Baseline: Conducted triage under standard user permissions (user), documenting operational restrictions honestly without forced privilege escalation.

## Limitations
-The tool does not detect all malware or provide a definitive security verdict.

-It does not inspect every possible persistence mechanism (e.g., shell profile modifications, kernel modules).

-Some telemetry is restricted under unprivileged user sessions.

-A point-in-time system snapshot is not a complete forensic memory acquisition.

## Safety and Privacy
All exercises were performed locally within a personal virtual machine. Sensitive process arguments, internal IP addresses, private credentials, and raw scheduled-task contents were strictly redacted prior to publication.

## What I Learned
I can now articulate the relationship between processes and services, audit cron and systemd persistence vectors, write defensive Bash automation scripts with error checking, and structure professional incident response reports.

## Next Steps
-Expand log parsing capabilities using advanced journalctl time filters.

-Practice live memory analysis and process tree mapping.
