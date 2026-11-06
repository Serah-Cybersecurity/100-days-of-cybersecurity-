# Incident Investigation Timeline & Sequence Report

**Author:** Serah Mulwa

**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering

**Dataset Analyzed:** `pcap/day20.pcap`

---

## 1. Executive Summary

During threat hunting operations, cross-tool correlation proves which telemetry records belong together mathematically, while an investigative timeline establishes the temporal sequence of events. This report documents the chronological sequence of network activity observed in `day20.pcap`, mapping Suricata signature alerts directly against Zeek protocol metadata.

---

## 2. Chronological Event Sequence

The table below maps the observed events in exact timestamp order, utilizing real telemetry extracted from Suricata `eve.json` and Zeek connection and protocol logs.

| Timestamp (UTC) | Telemetry Engine | Event Category | Source Endpoint | Destination Endpoint | Evidence Record & Artifacts |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `2026-11-06T10:43:04.222546Z` | **Zeek** | DNS Query (`A` Record) | `10.0.2.15:43806` | `192.168.100.1:53` | `dns.log` (UID: `Cwm0RP3YRwEK1TkZrd`, Query: `example.com`) |
| `2026-11-06T10:43:04.222546Z` | **Suricata** | Signature Alert | `10.0.2.15:43806` | `192.168.100.1:53` | `eve.json` (`sid:1000001`, Community ID: `1:P2oNim+dAcDZgQht0+q2HlbuHXU=`) |
| `2026-11-06T10:43:12.149350Z` | **Zeek** | DNS Query (`AAAA` Record) | `10.0.2.15:42294` | `192.168.100.1:53` | `dns.log` (UID: `CMNhdPSS13bACnDRh`, Query: `example.com`) |
| `2026-11-06T10:43:12.149350Z` | **Suricata** | Signature Alert | `10.0.2.15:42294` | `192.168.100.1:53` | `eve.json` (`sid:1000001`, Community ID: `1:qQZURsTvB7+LXx5x83z0/KkPQA=`) |
| `2026-11-06T10:43:20.653025Z` | **Zeek** | DNS Query & Response | `10.0.2.15:45127` | `192.168.100.1:53` | `dns.log` (UID: `C6kga32wpCLFCqXqk`, Query: `example.com`) |
| `2026-11-06T10:43:20.653025Z` | **Suricata** | Signature Alert | `10.0.2.15:45127` | `192.168.100.1:53` | `eve.json` (`sid:1000001`, Community ID: `1:I6puVD0/FGcSzdfYg+4Rm1dA84=`) |

---

## 3. Timeline Interpretation

The sequence demonstrates a clear pattern:

1. Internal host `10.0.2.15` initiated a series of DNS resolution requests to gateway DNS server `192.168.100.1` targeting domain `example.com`.
2. For each transaction, Suricata's detection engine identified the matching payload rule (`sid:1000001`) and logged an alert within the exact microsecond boundary of packet arrival.
3. Simultaneously, Zeek recorded protocol state and connection metadata, confirming that DNS resolution completed successfully with returned `A` and `AAAA` IP records.

---

## 4. Correlation Confidence Assessment

* **High Confidence (Direct Mathematical Mapping):** Records joined via matching **Community ID** flow hashes and **Zeek UIDs** are correlated with 100% certainty. We know with absolute mathematical confidence that Suricata Alert `1:P2oNim+dAcDZgQht0+q2HlbuHXU=` and Zeek Session `Cwm0RP3YRwEK1TkZrd` describe the exact same network packet stream.
* **Medium Confidence (Temporal Grouping):** Events occurring within the same packet capture window but on different ephemeral ports are grouped chronologically.

---

## 5. Analytical Limitations

* **Time Proximity Is Not Causation:** While events occurred close together in time, temporal proximity alone does not guarantee a single continuous user action. Protocol payload validation is required to establish cause-and-effect.
* **Host Telemetry Void:** Network telemetry proves that DNS queries were sent, but cannot reveal which local operating system process or binary generated the outbound socket connection.

---

## 6. Key Analyst Principles & Takeaways

1. **Time Proximity Is an Lead, Not Proof:** Never assume two sequential network events are causally linked without validating underlying protocol fields and payloads.
2. **Strict Telemetry Integrity:** Always use real, extracted timestamps from packet captures rather than simulated or estimated times.
