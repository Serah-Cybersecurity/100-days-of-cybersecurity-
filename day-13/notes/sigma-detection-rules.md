# Day 13 - Introduction to Sigma Detection Rules & Vendor-Agnostic Engineering

* **Author:** Serah Mulwa

* **Date:** October 31, 2026

* **Module:** SIEM Fundamentals & Detection Engineering

* **Target Audience:** Tier 1 SOC Analysts & Detection Engineers

## 1. What is Sigma?

**Sigma** is an open-source, vendor-agnostic detection-rule format created by Florian Roth and Thomas Patzke. It allows security analysts, threat hunters, and detection engineers to describe security detection logic using lightweight, human-readable **YAML (YAML Ain't Markup Language)** files.

Think of Sigma as the universal "Sign Language" of detection engineering. Just as a PDF allows you to view the exact same document layout regardless of your operating system, a Sigma rule allows you to define a threat signature once and convert it into queries for Splunk, ElasticSearch, Microsoft Sentinel, QRadar, AWS Athena, and dozens of other platforms.

## 2. Why Sigma is Useful (The Multi-Platform Problem)

Imagine you work as a Senior Detection Engineer for a global enterprise:
* Your regional European office uses **Splunk**.
* Your North American headquarters uses **Microsoft Sentinel**.
* Your cloud infrastructure uses **AWS OpenSearch**.

Without Sigma, if a new ransomware variant emerges, you would have to write, test, and maintain three completely different queries (Splunk SPL, KQL, and Lucene). With Sigma, you write **one** universal Sigma rule and use conversion tools (like `sigmac`) to instantly generate all three backend queries.

## 3. Anatomy of a Sigma Rule

Every production-grade Sigma rule is divided into structured blocks. Let's examine the structure of our starter Windows failed logon rule:

```yaml
title: Windows Failed Logon Event
status: test

description: >
  Identifies a Windows Security event recording
  an unsuccessful account logon.

logsource:
  product: windows
  service: security

detection:
  selection:
    EventID: 4625

  condition: selection

fields:
- TargetUserName
- IpAddress
- LogonType

falsepositives:
- User entering an incorrect password
- Application using an outdated password
- Approved automated authentication failures

level: low
```

### Breakdown of Key Fields:
* **`title`**: Clear, human-readable name for the detection.
* **`status`**: Lifecycle stage (`experimental`, `test`, `stable`).
* **`description`**: Detailed explanation of what malicious activity or security event the rule catches.
* **`logsource`**: Target operating system (`product: windows`) and log subsystem (`service: security`).
* **`detection`**: Core logic engine containing named selectors and boolean evaluation conditions.
* **`fields`**: Attributes displayed in the analyst's alert console when the rule triggers.
* **`falsepositives`**: Known legitimate business activities that might inadvertently trigger this rule.
* **`level`**: Assigned severity rating (`low`, `medium`, `high`, `critical`) for triage prioritization.

## 4. Critical Engineering Limitations

When working with starter Sigma rules, analysts must keep two major limitations in mind:

1. **Field-Mapping Discrepancies:** Raw Sigma rules use standard vendor field names (e.g., Windows `EventID`), which may differ from normalized JSON keys (e.g., `event_id`). In enterprise SIEMs, normalization standards (like CIM) bridge this gap.

2. **Single Event vs. Temporal Correlation:** A basic Sigma rule detects a single occurrence (e.g., one failed logon). Complex multi-stage attack patterns (like three failures followed by a success within a specific time window) require advanced correlation rules or backend SIEM logic.

## 5. Job Market Application

In modern cybersecurity interviews, hiring managers frequently ask: *"Have you written or worked with Sigma rules?"* 
Being able to explain Sigma YAML structure, log source definitions, and how to translate vendor-agnostic rules into SIEM queries proves you are operating at an industry-standard level. Public GitHub repositories featuring custom `.yml` detection rules are prime portfolio assets.
