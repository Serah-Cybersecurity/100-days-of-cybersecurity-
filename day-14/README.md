# Day 14 - SOC Alert Triage and Investigation

## Overview

This project simulates the end-to-end alert triage workflow, incident investigation methodology, and automation tooling utilized by Level 1 Security Operations Centre (SOC) analysts. It establishes rigorous documentation standards, defensive Python programming, and structured incident escalation workflows.

## Learning Objectives

- Understand SOC operations, ticketing lifecycles, and shift handovers.
- Distinguish between raw events, security alerts, and validated incidents.
- Master alert severity versus investigation priority.
- Investigate security alerts using structured baseline comparison and evidence gap analysis.
- Classify alert outcomes (`True Positive`, `False Positive`, `Benign Positive`, `Inconclusive`).
- Apply appropriate NIST-aligned escalation procedures.
- Connect observed behaviors to the **MITRE ATT&CK® Framework**.
- Build, test, and validate a custom Python alert-queue parsing utility.
- Produce professional executive SOC case reports and chain-of-custody ledgers.

## Environment & Tech Stack

- **Host Operating System:** Windows 
- **Virtualization:** Oracle VirtualBox
- **Guest Operating System:** Parrot OS
- **Programming Language:** Python 3.13 (Standard Library: `pathlib`, `json`, `argparse`, `sys`, `datetime`)
- **Data Format:** JSON Lines (`.jsonl`)
- **Frameworks & Standards:** NIST SP 800-61 Rev. 3, MITRE ATT&CK®

## Repository Structure

```text
day-14/
├── README.md
├── notes/               # Operational guides, MITRE mapping, escalation protocols, chain of custody
├── lab/data/            # Synthetic alert queues and baseline case context
├── scripts/             # Python automation utilities (triage_queue.py)
├── cases/               # Individual incident dossiers (SOC-2026-001 through 003)
├── reports/             # Executive investigation summaries and test result reports
├── tests/               # Malformed test inputs and QA validation files
└── screenshots/         # Portfolio evidence captures (Screenshots 18 through 23)
