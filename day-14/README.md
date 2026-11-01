# Day 14 - SOC Alert Triage, Investigation & Incident Handling

## Overview

Day 14 marks the operational transition from detection engineering to active Security Operations Center (SOC) analysis. This project simulates the workflow of a Level 1 (Tier 1) SOC Analyst tasked with triaging, investigating, classifying, and escalating security alerts from an enterprise alert queue.

## Mission Objectives

- **Alert Queue Management:** Acknowledge, prioritize, and manage incoming security alerts.
- **Structured Triage Workflow:** Apply a systematic investigation methodology to analyze incident telemetry.
- **Classification Mastery:** Distinguish accurately between True Positives (TP), False Positives (FP), Benign Positives (BP), and Inconclusive findings.
- **MITRE ATT&CK Mapping:** Align observed behaviors with standard adversary tactics, techniques, and procedures (TTPs).
- **Automation & Scripting:** Build a Python alert-queue management utility to automate ticket handling and status updates.
- **Incident Escalation & Reporting:** Produce detailed handover reports and investigation documentation for Tier 2 Incident Response teams.

## Environment & Prerequisites

- **Host Environment:** Linux (Parrot OS / Ubuntu)
- **Programming Language:** Python 3 (Standard Library)
- **Frameworks:** MITRE ATT&CK Matrix for Enterprise
- **Data Formats:** JSON / Markdown

## Repository Structure

- `notes/`: Conceptual technical notes on SOC operations, triage frameworks, and classification standards.
- `lab/`: Simulated alert queues and event context files.
- `scripts/`: Custom Python alert-queue management utility.
- `reports/`: Investigation notes and formal escalation reports.
- `screenshots/`: Visual evidence documenting dashboard triage and utility execution.

## Alert Queue Overview

| Alert ID | Alert Name | Severity | Initial Status |
| :--- | :--- | :--- | :--- |
| `ALT-2026-001` | **Repeated Failed Logons Followed by Success** | High | New |
| `ALT-2026-002` | **Failed SSH Authentication** | Medium | New |
| `ALT-2026-003` | **Unexpected Service Start** | Medium | New |

## Key Concepts Mastered

1. **Alert Prioritization:** Evaluating risk, business context, and potential operational impact over raw alert volume.
2. **Evidentiary Standard:** Basing incident conclusions strictly on verifiable telemetry rather than assumptions.
3. **Escalation Protocols:** Structuring handovers to senior responders with complete context, timelines, and IoCs.

## References

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [NIST Computer Security Incident Handling Guide (SP 800-61 Rev. 2)](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
