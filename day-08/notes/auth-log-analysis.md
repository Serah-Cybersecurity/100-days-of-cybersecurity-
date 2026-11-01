# Project: Linux Authentication Log Analyzer, Version 1

## Overview
* **Input Dataset:** Fictional training authentication log (`data/auth.log`).
* **Input Size:** 9 lines total.
* **Objective:** Ingest raw authentication telemetry, stream data line-by-line defensively, parse OpenSSH-style log messages using regular expressions, aggregate failed authentication attempts by username using frequency counters, and output structured forensic reporting.

## Audit Observations
* **Failed-Password Events:** 5 total messages matched the failed password pattern:
  * `test_user`: 3 attempts
  * `unknown_user`: 2 attempts
* **Accepted-Password Events:** 2 messages matched the successful login pattern (`demo_user`: 1, `test_user`: 1).
* **Other Formats:** 1 recognized system event (SSH connection closure with `[preauth]` status).
* **Malformed Records:** 1 intentionally malformed training line caught and categorized by heuristic validation.

## Analytical Interpretation
The dataset contains multiple failed-password messages associated with two distinct account names (`test_user` and `unknown_user`). These records demonstrate how automated log parsers can aggregate repeated authentication failures and summarize telemetry by target user. 

However, these numerical counts alone do not establish that a malicious brute-force attack occurred. The dataset is entirely fictional, and no independent evidence of hostile intent, source IP compromise, or automated tool signatures is present.

## Limitations
* The parser recognizes only pre-defined OpenSSH message structures.
* The script does not perform source IP reputation checks or geolocation lookups.
* Timestamps are not normalized into a unified system timezone.
* Source IP addresses belong strictly to documentation-only IPv4 blocks (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`).
* The program does not correlate events across multiple servers or establish human user intent.
* The output does not verify whether an account was successfully compromised following a series of failures.

## Recommended Next Steps
* Validate the parser against larger, diverse enterprise log corpora (e.g., Apache, FTP, and sudo logs).
* Implement automated unit and regression testing using `pytest`.
* Optimize log ingestion streams for gigabyte-scale enterprise log rotation and high-speed processing.
* Integrate automated alerting thresholds to flag abnormal login frequency spikes.
