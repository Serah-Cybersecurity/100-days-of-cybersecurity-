# Day 8 - Linux Internals and Authentication Log Analysis

## Overview
This project documents my comprehensive study of Linux filesystem navigation, user identities, file permissions, process inspection, background services, system logs, automated unit testing, and Python-based authentication log analysis conducted in a Parrot OS VirtualBox environment.

## Learning Objectives
- Navigate the Linux filesystem and inspect system directories (`pwd`, `ls`, `cd`, `find`).
- Audit user and group identities (`whoami`, `id`, `groups`).
- Explain and manage ordinary Linux file permissions (`chmod`).
- Observe running processes (`ps`, `top`) and active systemd services (`systemctl`).
- Understand system logging architecture and journal navigation (`journalctl`, log inspection of `/var/log/dpkg.log`).
- Read and analyze authentication log entries.
- Build, test, and document a custom Python security log-analysis script.
- Document findings and limitations accurately.

## Environment
- **Operating system:** Linux
- **Linux distribution:** Parrot OS 7.3 KDE Security Edition
- **Python version:** Python 3.x
- **Git version:** Git installed
- **Virtualization environment:** Oracle VirtualBox (Windows host with bidirectional clipboard configured)
- **Date completed:** October 2026

## Tools and Commands Used
- **Filesystem & Inspection:** `pwd`, `ls`, `cd`, `cat`, `less`, `find`, `grep`
- **User Auditing:** `whoami`, `id`, `groups`
- **Permissions:** `chmod`
- **Process & Services:** `ps`, `top`, `systemctl`
- **Log Auditing:** `journalctl`, `/var/log/dpkg.log`, `/var/log/lynis.log`
- **Development & Version Control:** Python 3 (`pathlib`, `re`, `collections.Counter`, `unittest`), Git

---

## Main Project: Linux Authentication Log Analyzer, Version 1
The program reads a local fictional training dataset and counts selected failed-password and accepted-password messages, aggregates failed attempts by username, and identifies malformed log lines.

### Input Data
The dataset is fictional (`data/auth.log`) and was created specifically for training and testing without exposing production system logs. It is not evidence collected from a real system compromise.

### How to Run
From the `day-08/` directory:
```bash
python3 python/auth_log_analyzer.py 
```

### Verified Results for Training Dataset
Total input lines: 9

Failed-password messages: 5

Accepted-password messages: 2

Other recognized-format messages: 1

Malformed or unrecognized-format lines: 1

test_user failed logins: 3

unknown_user failed logins: 2

### Testing & Validation
~Implemented automated unit tests using Python's standard unittest framework (tests/test_auth_log_analyzer.py).


~Command: python3 -m unittest discover -s tests -v

Result: All test suites passed successfully with zero failures.

### Key Security Concepts
-Least Privilege: Restricting file permissions and service access to minimize the attack surface.

-Process & Service Inspection: Monitoring background daemons using systemctl to identify active system services.

-Authentication Auditing: Distinguishing between raw log observations (failed/accepted logins) and confirmed security breaches.

-Evidence-Based Interpretation: Avoiding false positives by recognizing that log events are telemetry, not proof of malicious intent.

### Findings and Interpretation
The script successfully parsed and aggregated authentication events from the training dataset. Because Parrot OS relies heavily on systemd-journald rather than traditional text logs like /var/log/auth.log, package lifecycle and system events were audited using alternative active logs such as /var/log/dpkg.log. While multiple failed logins were identified for test_user and unknown_user, these observations do not independently prove that an active brute-force attack or system compromise occurred.

### Limitations
-The parser recognizes only pre-defined OpenSSH message structures.

-The dataset is entirely fictional.

-Source IP addresses belong to documentation-only IPv4 blocks (192.0.2.0/24).

-The tool does not establish user identity, intent, or system compromise.

-The tool is not a production security monitoring system.

### What I Learned:
-Most important concept: Separating core analysis logic from I/O handling makes code testable and robust.

-Most useful command: systemctl --type=service --state=running for auditing active system daemons.

-Most difficult problem: Resolving VirtualBox shared folder permissions and configuring bidirectional clipboard daemons (VBoxClient) between Windows and Parrot OS.

How I resolved it: Installed guest utilities, verified service states, and utilized proper terminal paste shortcuts (Ctrl + Shift + V).

Future improvement: Add support for normalized timestamp parsing and structured JSON logging export.
