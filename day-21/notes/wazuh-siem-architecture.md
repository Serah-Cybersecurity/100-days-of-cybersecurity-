# Technical Note: Enterprise SIEM Architecture, Distributed Component Analysis & Wazuh Deep-Dive

**Author:** Serah Mulwa

**Module:** Day 21 - SIEM Architecture, Log Ingestion & Security Data Engineering

## 1. Executive Summary & Personal Reflections

Throughout Day 21 of my cybersecurity engineering journey, I transitioned from building a custom, Python-based Mini-SIEM ingestion pipeline (`src/ingest.py`) to studying how battle-tested enterprise platforms operate at scale. 

While building a script from scratch teaches you the fundamentals of parsing, validation, normalisation, and deduplication, production environments require robust, distributed systems. To understand how real-world Security Operations Centers (SOCs) protect thousands of corporate endpoints, I conducted a deep-dive architecture study of **Wazuh**, an open-source Security Information and Event Management (SIEM) and Extended Detection and Response (XDR) platform.

This technical note documents my comprehensive study of Wazuh’s distributed architecture, compares enterprise components directly against my Mini-SIEM pipeline design, and provides detailed engineering answers to ten critical SIEM architectural questions.

## 2. Component Data-Flow Comparison: Mini-SIEM vs. Enterprise Wazuh

A powerful realization during my studies was that enterprise SIEM platforms do not reinvent the wheel—they simply scale up the exact 7-stage data pipeline principles I implemented in my local project.

```
MINI-SIEM PIPELINE (Python Script):
Raw Files (data/raw/) ──> Input Reader ──> Parser ──> Validator ──> Normaliser ──> Deduplicator ──> Quarantine (DLQ) ──> Report

ENTERPRISE WAZUH ARCHITECTURE (Distributed Nodes):
Endpoints (Win/Linux) ──> Wazuh Agents (TLS) ──> Wazuh Server (Decoders/Rules) ──> Wazuh Indexer (OpenSearch) ──> Wazuh Dashboard (UI) ──> SOC Analyst
```

### Architectural Component Breakdown:

1. **Wazuh Agent (The Sensor):** Installed locally on endpoints (Windows, Linux, macOS), collecting OS logs, file integrity monitoring (FIM) changes, and vulnerability scans. (Equivalent to our raw log generators).

2. **Wazuh Server (The Processing Engine):** Receives encrypted telemetry from agents, decrypts packets, runs decoders and rules engines, and normalizes events. (Equivalent to our Python ingestion and normalisation script).

3. **Wazuh Indexer (The Distributed Database):** An OpenSearch/Elasticsearch-based engine storing and indexing processed security records for lightning-fast search queries. (Equivalent to our structured `normalised_events.jsonl` output).

4. **Wazuh Dashboard (The Analyst UI):** The web interface providing visualization graphs, alert panels, and compliance frameworks. (Equivalent to our JSON health reports and terminal summaries).

## 3. Comprehensive Architectural Write-Up: The 10 Core SIEM Questions

To prove my mastery of enterprise SIEM design—particularly for technical interviews at companies like Microsoft, AWS, and Datadog—I analyzed and answered the ten core architectural questions governing distributed security platforms:

### 1. What does the Wazuh agent collect?
The Wazuh agent acts as the local endpoint sensor, capturing operating system audit logs (Syslog, Windows Event IDs like 4625/4624), File Integrity Monitoring (FIM) telemetry tracking unauthorized system file changes, installed software inventories, rootkit scan results, and active network connections.

### 2. What does the Wazuh server do?
The server is the central brain of the platform. It manages agent registrations, authenticates connections, decrypts incoming TLS telemetry packets, executes decoders to parse raw formats, runs the correlation rules engine to detect malicious patterns, and forwards normalized events to the indexer cluster.

### 3. What does the Wazuh indexer do?
The indexer provides distributed, full-text storage and search capabilities. It organizes processed logs into structured JSON indices, allowing SOC analysts to execute complex forensic queries across millions of historical events in milliseconds.

### 4. What does the dashboard do?
The dashboard provides the graphical user interface (GUI) for security analysts. It queries the Wazuh indexer via secure REST APIs to render interactive threat visualization graphs, real-time alert feeds, and regulatory compliance dashboards (such as PCI-DSS and NIST).

### 5. How does an event travel from an endpoint to the dashboard?
* **Step 1:** An activity occurs on an endpoint (e.g., a failed login triggering Windows Event ID 4625).
* **Step 2:** The **Wazuh Agent** captures the event locally.
* **Step 3:** The agent compresses and encrypts the log, shipping it securely over TLS (Port 1514/1515) to the **Wazuh Server**.
* **Step 4:** The **Wazuh Server** decrypts the payload, decodes the log fields, and evaluates detection rules.
* **Step 5:** The server indexes the processed event into the **Wazuh Indexer** (Port 9200).
* **Step 6:** A **SOC Analyst** reviewing the **Wazuh Dashboard** queries the indexer and visualizes the failed login alert in real-time.

### 6. Why does the indexer need storage?
Storage is essential for historical trend analysis, retrospective threat hunting (searching logs from weeks or months prior to discover latent attacker dwell time), and meeting strict regulatory compliance data retention mandates (e.g., keeping security logs for 90+ days).

### 7. Why is communication between components secured?
Security telemetry contains sensitive enterprise data, including usernames, internal IP addresses, network topologies, and credentials. Enforcing TLS encryption and mutual authentication prevents Man-in-the-Middle (MitM) eavesdropping, log tampering, and unauthorized log injection attacks.

### 8. What would happen if the agent stopped communicating with the server?
The Wazuh server marks the agent status as **Disconnected**. The endpoint becomes a critical security **blind spot**—while the machine may continue generating local logs, the SOC receives no real-time telemetry or alerts until network connectivity or agent health is restored.

### 9. What would happen if the indexer became unavailable?
If the indexer cluster goes down, the Wazuh server cannot write processed logs to storage. While ingestion pipelines may buffer logs in memory temporarily for short outages, a prolonged indexer failure stalls log processing, causes dropped events, and blinds real-time dashboard alerts.

### 10. How would a SOC analyst identify a collection problem?
An analyst identifies collection failures by monitoring agent status dashboards (noting sudden spikes in disconnected endpoints), reviewing Wazuh server error logs (`/var/ossec/logs/ossec.log`), tracking ingestion drop metrics, or observing unexpected flatlines in dashboard event volume graphs.

## 4. Key Engineering Takeaways & Job Market Application

### What I Must Remember:
1. **SIEMs are distributed systems:** In production environments, collection, parsing, indexing, and visualization run on decoupled, scalable nodes rather than a single script.
2. **Connectivity is critical:** Agent health and indexer availability dictate whether a SOC has complete visibility or dangerous blind spots.

### Application in Big Tech Interviews:
When interviewing for Security Engineering or SIEM Architecture roles at companies like Microsoft, AWS, or Datadog, interviewers frequently ask: *"How would you design a scalable logging infrastructure for 50,000 corporate endpoints?"*

**The Winning Answer:** 
> *"I design distributed SIEM architectures separating collection agents, processing servers, indexing clusters, and presentation dashboards. I ensure encrypted transport via TLS, implement buffer queues to handle indexer outages, and monitor ingestion telemetry to prevent endpoint blind spots."*
