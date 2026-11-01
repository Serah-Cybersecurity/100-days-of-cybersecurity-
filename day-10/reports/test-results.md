# Day 10 - Linux Triage Script Test Results & Execution Report

## 1. Executive Summary & Tool Scope
* **Script Name:** `linux_triage.sh`
* **Purpose:** Collect a read-only, point-in-time system health and configuration snapshot for defensive analysis.
* **Operational Scope:** Local Parrot OS virtual machine environment.
* **Classification:** Beginner defensive utility (not a forensic memory acquisition tool or automated malware verdict generator).

## 2. Testing Methodology & Execution Log
* **Permission Validation:** Executed successfully under unprivileged user permissions (`user`), respecting system access boundaries.
* **Execution Command:** `./day-10/scripts/linux_triage.sh`
* **Output Redirection:** Verified terminal output stream and tested file redirection (`./day-10/scripts/linux_triage.sh > day-10/reports/test-results.md`).

## 3. Key Design Observations & Security Principles
* **Defensive Error Handling:** Utilized `command -v` conditional wrappers to ensure the script degrades gracefully if optional binaries are missing.
* **Data Minimization:** Excluded raw crontab file contents and restricted process inspection to command names (`comm`) to prevent leaking sensitive environment variables or credentials.
* **Read-Only Guarantee:** The script performed exclusively observational queries (`ps`, `systemctl`, `ss`, `crontab -l` status checks, and `find` directory checks) without modifying system states.

## 4. Conclusion
The `linux_triage.sh` automation script successfully gathered a structured system baseline, demonstrating core shell scripting logic and security-conscious data handling suitable for introductory incident response workflows.
