# Day 11 - Defensive Security Investigation & Mastery Checkpoint

## Overview
This project consolidates the first ten days of my cybersecurity learning through a comprehensive synthetic log-analysis, automated script parsing, and incident-triage exercise aligned with NIST SP 800-61 methodology.

## Learning objectives
* Assess knowledge of operating systems, networking, and security event structures.
* Analyse structured security event logs (`events.jsonl`).
* Correlate events by source IP, timestamp, user account, and event type.
* Build, test, and validate a robust Python JSONL log analyser (`analyze_events.py`).
* Distinguish raw observations from analytical hypotheses and conclusions.
* Produce a formal, evidence-based incident triage report (`triage-report.md`).
* Document software testing edge cases (`test-results.md`) and privacy limitations.

## Environment & Architecture
* **Host Operating System:** Windows / Parrot OS (VirtualBox VM)
* **Language & Runtime:** Python 3.x (Standard Library)
* **Data Format:** JSON Lines (`.jsonl`)
* **Key Dependencies:** Python standard library (`argparse`, `json`, `sys`, `pathlib`, `collections.Counter`)

## Lab Scope
This is a defensive learning exercise utilizing a controlled, synthetic dataset (`events.jsonl`) and baseline context (`case-context.md`). It does not involve investigating external systems or unauthorized accounts.

## Tools Created
* **`analyze_events.py`:** A production-grade Python CLI tool that ingests JSONL logs, counts event types, tracks authentication failures by source IP, flags threshold breaches (`[REVIEW]`) and correlations (`[CORRELATION]`), summarizes privilege use, and handles malformed data gracefully without crashing.

## Testing & Validation Summary
* **Test 1 (Version & Syntax):** Verified Python runtime and compiled bytecode successfully (`py_compile`).
* **Test 2 (Standard Dataset):** Processed 8 valid records matching manual analysis counts.
* **Test 3 (Threshold Modification):** Tested `--failure-threshold 2` to demonstrate rule sensitivity.
* **Test 4 (Missing File Error):** Verified clean `stderr` error output and exit status `2`.
* **Test 5 (Malformed JSON Handling):** Verified `JSONDecodeError` warning logs, zero valid records processed, and exit status `1`.

## Key Findings Summary
* **Authentication Anomaly:** Identified 3 failed logins followed by a success from unapproved IP `198.51.100.27`.
* **Privilege-Use:** Observed read-only `sudo systemctl status cron` execution requiring contextual review.
* **Scheduled Tasks:** Confirmed `daily-report.timer` execution aligned with routine baseline schedules.
* **Analyst Restraint:** Explicitly noted that while anomalies warrant review, available logs do not prove system compromise.

## Limitations
The available synthetic dataset lacks full memory dumps, process execution tress, network PCAPs, and session IDs, which prevents definitive attribution or compromise confirmation.

## Skills Demonstrated
* Defensive security log analysis
* Python CLI scripting & exception handling
* Software testing & test report authoring
* Incident triage report writing
* Linux system telemetry inspection (`whoami`, `id`, `ps`, `systemctl`, `ss`)

## Next steps
Advance to Day 12 exploratory threat hunting and advanced log parsing architectures.
