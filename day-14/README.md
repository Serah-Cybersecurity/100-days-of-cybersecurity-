# Day 14 - SOC Alert Triage and Investigation

## Overview

This project introduces the alert triage workflow used by Level 1 Security Operations Centre analysts.

## Learning objectives

- Understand SOC operations.
- Distinguish events, alerts and incidents.
- Understand alert severity and priority.
- Investigate security alerts.
- Classify alert outcomes.
- Apply appropriate escalation procedures.
- Understand MITRE ATT&CK mapping.
- Build a Python alert-queue utility.
- Produce professional SOC reports.

## Environment

- Host: Windows
- Virtualisation: Oracle VirtualBox
- Guest: Parrot OS
- Language: Python
- Data format: JSON Lines
- Dependencies: Python standard library

## Main project

Three synthetic security alerts were investigated:
1. **SOC-2026-001 (High Severity):** Repeated failed logons followed by a successful logon and privilege assignment on host `WIN-LAB-01` from source IP `198.51.100.27`.
2. **SOC-2026-002 (Medium Severity):** Failed SSH authentication followed by successful logon on host `LINUX-LAB-01` from source IP `192.0.2.44`.
3. **SOC-2026-003 (Medium Severity):** New service (`backup-agent`) started on host `WIN-LAB-01`.

## Technical tool

The Python utility (`day-14/scripts/triage_queue.py`) validates and organises the supplied alert queue (`alert-queue.jsonl`). It enforces schema integrity, validates severity levels, logs malformed JSON records defensively to `sys.stderr`, and outputs alerts sorted by priority (Severity weight $\rightarrow$ Timestamp $\rightarrow$ Alert ID).

## Investigations

- **Case SOC-2026-001:** Source IP `198.51.100.27` is unapproved per the baseline. The login and privilege grant shared a Logon ID. Due to missing endpoint telemetry (EDR process trees) and unverified user identity, the alert was classified as **Inconclusive** and **Escalated** to Tier 2 IR.
- **Case SOC-2026-002:** Source IP `192.0.2.44` is approved per baseline context. Activity correlates with authorized change maintenance ticket `CHG-0142`. Classified as **Benign Positive** and **Closed**.
- **Case SOC-2026-003:** Service start of `backup-agent` matches normal operational baseline around 08:30 UTC under change reference `CHG-0160`. Classified as **Benign Positive** and **Closed**.

## Testing

A 6-step QA testing suite was conducted and recorded in `day-14/reports/test-results.md`:
- **TC-001 (Syntax):** Compiled cleanly via `python3 -m py_compile triage_queue.py`.
- **TC-002 (Happy Path):** Successfully processed `alert-queue.jsonl` (3 valid records, 0 invalid records).
- **TC-003 (Sorting):** Verified high-severity alert (`SOC-2026-001`) sorted to top of queue.
- **TC-004 (Missing File):** Confirmed missing file handling returns exit code `2` (`$? = 2`).
- **TC-005 (Malformed Input):** Confirmed `malformed.jsonl` triggers warning message to `stderr` without crashing.
- **TC-006 (Aggregation):** Verified severity count summary (`high: 1`, `medium: 2`).

## Limitations

This is a synthetic learning exercise. No real security incident was investigated.

## Skills demonstrated

- Applied a structured 9-step Tier 1 SOC alert triage methodology.
- Developed defensive Python log automation and error-handling routines.
- Evaluated events against authorized baseline inventories and Change Management tickets.
- Documented evidence gaps and conducted baseline cross-referencing.
- Mapped potential threat behaviors to the MITRE ATT&CK® Framework (T1110 Brute Force).
- Executed NIST SP 800-61 Rev. 3 incident escalation procedures without exceeding L1 authority.
- Computed SHA-256 cryptographic hashes to maintain Chain of Custody ledgers.
- Wrote executive-ready SOC case dossiers and QA test reports.

## References

- National Institute of Standards and Technology (NIST). *NIST SP 800-61 Revision 3: Incident Response Recommendations*.
- MITRE Corporation. *MITRE ATT&CK® Framework: Tactics and Techniques*.
