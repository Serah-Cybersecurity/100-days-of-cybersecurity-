# Day 13 - SIEM Fundamentals and Detection Engineering

## Overview

This project introduces centralised security monitoring, multi-source log analysis, event correlation, and introductory detection engineering. Built from scratch as part of a self-directed cybersecurity journey.

## Learning objectives

- Explain SIEM architecture and pipeline flows.
- Understand log collection, forwarding, and ingestion.
- Understand parsing and normalisation (CIM principles).
- Examine common SIEM concepts and data modeling.
- Learn basic and advanced Splunk SPL (Search Processing Language).
- Analyse multi-source event data (`events.jsonl`).
- Build, test, and validate a custom Python event correlation tool.
- Create and evaluate a vendor-agnostic Sigma detection rule.
- Document investigation findings, test exit codes, and operational limitations.

## Environment

- Host: Lenovo ThinkPad / HP EliteBook
- Virtualisation: Oracle VirtualBox / KVM
- Guest OS: Parrot OS (Linux)
- Language: Python 3
- Data Format: JSON Lines (`.jsonl`)
- Dependencies: Python Standard Library (`json`, `argparse`, `ipaddress`, `datetime`, `collections`, `pathlib`)

## Project files

- `notes/`: Comprehensive technical learning notes (`siem-architecture.md`, `log-normalisation.md`, `spl-basics.md`, `detection-engineering.md`, etc.)
- `lab/data/`: Synthetic multi-source security-event dataset (`events.jsonl`) and environment case baseline (`case-context.md`)
- `scripts/`: Custom Python event correlation utility (`mini_siem.py`)
- `detections/`: Vendor-agnostic Sigma detection rule (`windows_failed_logon.yml`)
- `reports/`: Investigation reports and formal test validation suite (`test-results.md`)
- `screenshots/`: Visual evidence documenting terminal execution, directory trees, and parameter tuning

## Main project

The Python mini-SIEM tool analyses synthetic events from Windows, Linux, and network firewall sources. It ingests JSONL records, validates required schema keys, parses and normalizes timestamps to UTC, verifies IP addresses, and identifies configured authentication correlation patterns for human review.

## Detection logic

- **Threshold:** Requires $\ge 3$ failed authentication attempts.
- **Time Window:** Rolling 10-minute sliding window (`--window-minutes 10`).
- **Target Event:** Preceding failures followed by a successful logon (`result="success"`) for the same username and source IP address.

## Testing

Verified via a formal 7-step test suite covering version checks, compilation, standard dataset execution, threshold tuning (`--threshold 4`), time-window modifications, missing file error handling (Exit Code `2`), and malformed JSON resilience. Full results documented in `reports/test-results.md`.

## Limitations

This tool is an educational log analysis and correlation engine. It is **not** a production-grade enterprise SIEM, automated malware scanner, or active intrusion prevention system (IPS). Results depend entirely on log quality, schema consistency, and threshold tuning.

## What I learned

Demonstrated practical competence in log ingestion pipelines, custom Python event correlation, CLI argument parsing, Sigma YAML rule authoring, false positive/negative analysis, and SOC detection engineering principles.

## References

- [Sigma HQ Documentation](https://github.com/SigmaHQ/sigma)
- [Splunk Search Reference](https://docs.splunk.com/)
- [TryHackMe Security Operations Fundamentals](https://tryhackme.com/)
