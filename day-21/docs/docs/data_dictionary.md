# Technical Note: Unified Data Dictionary & Elastic Common Schema (ECS) Field Mapping

**Author:** Serah Mulwa

**Module:** Day 21 - SIEM Architecture, Log Ingestion & Security Data Engineering

## 1. Executive Summary & Personal Reflections

When building a multi-source security ingestion pipeline, one of the biggest engineering hurdles is dealing with schema fragmentation. A Windows domain controller, a Linux SSH server, a perimeter firewall, and a Suricata IDS all use completely different keys to represent identical concepts. For instance, Windows logs IP addresses under `source_ip`, whereas Zeek network monitors use `id.orig_h`.

Without a standardized data dictionary, security analysts would have to memorize dozens of vendor-specific syntaxes to write effective detection queries. To solve this in my Mini-SIEM pipeline (`src/ingest.py`), I mapped all ingested telemetry into a unified subset inspired by the **Elastic Common Schema (ECS)**.

This document serves as the official data dictionary for my repository, defining every standardized field, its purpose, and concrete examples, while ensuring that complete forensic raw lineage is preserved.

---

## 2. Standardised ECS Field Mapping Reference Table

The table below outlines the core investigative anchors normalized across all incoming log sources in our pipeline:

| Field Name | Description | Example Value |
| :--- | :--- | :--- |
| **`@timestamp`** | The standardized ISO-8601 UTC timestamp capturing when the original event occurred on the endpoint. | `2026-11-06T08:00:00Z` |
| **`event.action`** | The normalized security action or outcome classified during the normalisation phase. | `authentication_failure` |
| **`event.category`** | High-level event classification grouping related security telemetry types. | `authentication` |
| **`event.provider`** | The originating platform, sensor, or log vendor that generated the telemetry. | `windows` |
| **`user.name`** | The account username or actor identifier associated with the activity. | `alex` |
| **`source.ip`** | The validated source IPv4 or IPv6 address initiating the network connection or event. | `192.0.2.25` |
| **`destination.ip`** | The validated destination IPv4 or IPv6 address targeted by the connection. | `198.51.100.20` |
| **`host.name`** | The hostname of the asset enriched via our local CMDB inventory lookup table. | `workstation-01` |
| **`asset.type`** | The categorized classification of the endpoint (e.g., workstation, server, firewall). | `workstation` |
| **`asset.department`** | The internal corporate department owning or operating the asset. | `finance` |
| **`asset.criticality`** | The assigned business impact tier used for prioritizing incident response (e.g., low, medium, high). | `medium` |
| **`raw_reference`** | The complete, unmodified original raw log dictionary preserved for forensic auditing and deep investigations. | `{"timestamp": "...", "event_id": 4625, ...}` |

---

## 3. Engineering Implementation & Normalisation Logic

Inside my normalisation module (`src/normalizer.py`), conditional Python mapping logic ensures that heterogeneous source keys are safely translated into our standardized data dictionary without throwing KeyErrors:

```python
# Example snippet illustrating safe key extraction and ECS normalisation
src_ip = record.get("source_ip") or record.get("id.orig_h") or record.get("src_ip")
dst_ip = record.get("destination_ip") or record.get("id.resp_h")

normalized = {
    "@timestamp": record.get("timestamp") or record.get("ts"),
    "event": {
        "provider": source_name,
        "action": map_action(source_name, record),
        "category": "authentication" if source_name == "windows" else "network"
    },
    "source": {
        "ip": src_ip
    },
    "destination": {
        "ip": dst_ip
    },
    "user": {
        "name": record.get("username") or record.get("user")
    },
    "raw_reference": record  # Preserving full forensic lineage
}
```

## 4. Why This Matters in the Job Market

In Big Tech security engineering interviews (at companies like Microsoft, AWS, Datadog, or Google), hiring managers look for candidates who understand **schema convergence**. Being able to explain how you abstract away vendor-specific log quirks into a clean, queryable data dictionary—while still preserving raw lineage for forensic depth—proves that you design production-grade data pipelines built for scale and investigative rigor.
