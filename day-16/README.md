# Day 16 - DNS Security and Investigation

## Overview
This project explores DNS architecture, DNS troubleshooting, network-level DNS analysis, and defensive DNS detection as part of the 100 Days of Cybersecurity Challenge.

## Learning Objectives
- Understand DNS resolution.
- Explain recursive and authoritative DNS.
- Identify DNS record types.
- Understand DNS caching and TTL.
- Examine DNS response codes.
- Understand DNSSEC, DoH, and DoT.
- Investigate DNS packets using Wireshark.
- Use `dig` and `nslookup`.
- Build a Python DNS telemetry analyzer.
- Identify unusual DNS behavior.
- Produce an evidence-based investigation report.

## Environment
- **Host:** Windows / Linux Mint Base
- **Virtualization:** Oracle VirtualBox
- **Guest OS:** Parrot Security OS
- **Tools:** `dig`, `nslookup`, Wireshark, TShark
- **Language:** Python 3
- **Dependencies:** Python standard library (`argparse`, `ipaddress`, `json`, `pathlib`, `collections`, `datetime`)

## Main Project
A custom Python utility (`dns_analyzer.py`) that analyzes synthetic DNS telemetry (`dns-events.jsonl`) and identifies clients exhibiting multiple unusual indicators.

## Detection Characteristics
- Query frequency (sliding-window peak analysis)
- Query-name length (subdomain character limits)
- TXT-query proportion (protocol abuse tracking)
- NXDOMAIN frequency (error code ratios)

## Testing
Comprehensive test suite executed covering syntax compilation, baseline execution, argument threshold tuning (`--min-queries`, `--long-name`), missing file error handling (Exit Code `2`), and malformed JSON resilience. Documented in `reports/test-results.md`.

## Findings
Offline analysis of 17 synthetic events across 3 clients identified `192.0.2.25` as a review candidate triggering high query frequency, long query names, and high TXT proportions. Documented in `reports/dns-investigation-report.md`.

## Limitations
This tool performs heuristic analysis only. It does not establish confirmed malicious activity, command-and-control communication, or data exfiltration without correlative endpoint and resolver evidence.

## Skills Demonstrated
- Network traffic capture and analysis using Wireshark and `dig`.
- Python-based log parsing, validation, and algorithmic metric calculation.
- Security detection engineering, hypothesis formulation, and alert tuning.
- Professional incident investigation reporting and documentation.

## References
- IETF RFC 1035: Domain Names - Implementation and Specification
- MITRE ATT&CK Framework: T1071.004 (Application Layer Protocol: DNS)
- Microsoft DNS Troubleshooting Guidance
