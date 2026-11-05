# Technical Note: Alert Triage & Incident Analysis - Thinking Like a SOC Analyst

**Author:** Serah Mulwa

**Module:** Day 18 - Network Security Monitoring & Intrusion Detection

## 1. Executive Summary

Deploying intrusion detection sensors and writing custom signatures represents only the first phase of network defense. In an enterprise Security Operations Center (SOC), sensors fire thousands of alerts daily. The primary responsibility of a Tier 1 security analyst is not just watching alerts appear, but systematically investigating, contextualizing, and classifying them.

This technical note outlines the standardized 5-stage SOC triage framework, multi-source log correlation, and professional documentation practices required to transform raw network alerts into actionable security decisions.

## 2. The 5-Stage SOC Analyst Triage Framework

When a security alert lands on your monitoring dashboard or SIEM queue, you must never jump to conclusions or assume malicious intent immediately. Instead, follow a structured 5-stage investigative workflow:

### Stage One: Validate the Alert (The Metadata Check)
Before analyzing intent, verify the technical integrity of the alert itself. Answer these core forensic questions:
* **What rule generated it?** Check the Signature ID (`sid`) and rule name (`msg`).
* **What is the timestamp?** When did this occur? Check for time zone alignment and whether you are analyzing live traffic or historical captures.
* **What are the IP addresses?** Identify the Source IP (`src_ip`) and Destination IP (`dest_ip`).
* **Which protocol was observed?** (e.g., DNS, HTTP, TLS, TCP).
* **Which sensor generated the event?** Crucial in multi-site or multi-cloud network architectures.

### Stage Two: Understand the Network Context
An IP address or domain name is meaningless without environmental context:
* Is the source an internal corporate workstation or an external scanner?
* Is the destination an approved business service or an unknown external host?
* Does network address translation (NAT) or proxying mask the true endpoint addresses?

### Stage Three: Correlate Relevant Evidence (Multi-Source Analysis)
A professional analyst never relies on a single log source. Cross-reference your findings across multiple enterprise data pipelines:
* **Suricata EVE JSON / Alerts:** Network detection events and protocol metadata.
* **DNS Logs:** Exact domain names requested, query types (`A`, `AAAA`, `TXT`), and upstream resolver responses.
* **Firewall / NetFlow Logs:** Whether traffic was permitted or dropped by corporate security policy.
* **Endpoint Detection & Response (EDR):** Process execution trees and host-level activity.
* **Authentication Logs:** Successful or failed user login attempts.

### Stage Four: Assess the Finding (Standardized Classifications)
Classify the alert into an industry-standard evidence-based category:
1. **Benign Activity:** Normal network traffic or administrative behavior.
2. **False Positive:** A misconfigured rule or benign pattern incorrectly flagged.
3. **Suspicious Activity:** Anomalous behavior requiring escalation or deeper review.
4. **Confirmed Policy Violation:** Unapproved software or file-sharing behavior.
5. **Confirmed Security Incident:** Verified malicious activity backed by robust telemetry.
6. **Inconclusive:** Corrupted or incomplete logs preventing reliable assessment.

### Stage Five: Document Your Decision
Professional analysis relies on objective conclusions supported by verifiable data, not drama. Record what was observed, which evidence supports your conclusion, what remains unknown, and whether escalation is necessary.

## 3. Job Market Relevance

* **SOC Tier 1 Analyst:** Spends shifts executing this 5-stage triage workflow across SIEM platforms, clearing false positives, and writing ticket notes for escalated incidents.
* **Incident Responder:** Takes over escalated tickets from Tier 1, utilizing correlated logs and PCAPs to scope the impact of confirmed security breaches across enterprise endpoints.
