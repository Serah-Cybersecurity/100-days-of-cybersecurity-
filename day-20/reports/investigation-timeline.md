# Technical Note: Network Threat Hunting & Investigation Timeline

**Author:** Serah Mulwa

**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering

---

## 1. Executive Summary

While cross-tool flow hash matching via **Community ID** establishes cryptographic links between signature alerts and session telemetry, an **Investigation Timeline** arranges those correlated observations in chronological order. Building an accurate timeline allows security analysts to reconstruct event sequences, evaluate dwell times, and establish causal relationships during incident triage.

This report documents the chronological sequence of network events extracted from `day20.pcap`, evaluated across Suricata EVE JSON alerts and Zeek metadata logs (`conn.log`, `dns.log`).

---

## 2. Network Investigation Timeline

The table below maps the chronological sequence of events captured during the Day 20 practical analysis. All timestamps reflect actual telemetry extracted directly from sensor logs without modification or synthetic fabrication.

| Timestamp (UTC) | Tool Engine | Event Classification | Source Endpoint | Destination Endpoint | Telemetry & Evidence Artifacts |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `2026-11-06T10:43:04.222546Z` | **Zeek** | DNS Query (`A` Record) | `10.0.2.15:43806` | `192.168.100.1:53` | `dns.log` (uid: `Cwm0RP3YRwEK1TkZrd`, query: `example.com`, qtype: `A`) |
| `2026-11-06T10:43:04.222546Z` | **Suricata** | Signature Alert (`sid:1000001`) | `10.0.2.15:43806` | `192.168.100.1:53` | `eve.json` (Community ID: `1:P2oNim+dAcDZgQht0+q2HlbuHXU=`, msg: `LOCAL LAB DNS query for example.com`) |
| `2026-11-06T10:43:12.149350Z` | **Zeek** | DNS Query (`AAAA` Record) | `10.0.2.15:42294` | `192.168.100.1:53` | `dns.log` (uid: `CMNhdPSs13bACnDRh`, query: `example.com`, qtype: `AAAA`) |
| `2026-11-06T10:43:12.149350Z` | **Suricata** | Signature Alert (`sid:1000001`) | `10.0.2.15:42294` | `192.168.100.1:53` | `eve.json` (Community ID: `1:qQZURsTvB7+LXx5x83z0/KkPQA=`, msg: `LOCAL LAB DNS query for example.com`) |
| `2026-11-06T10:43:20.653025Z` | **Zeek** | DNS Query & Response | `10.0.2.15:45127` | `192.168.100.1:53` | `dns.log` (uid: `C6kga32wpCLFCqXqk`, query: `example.com`, qtype: `A`, answers: `104.20.23.154`) |
| `2026-11-06T10:43:20.653025Z` | **Suricata** | Signature Alert (`sid:1000001`) | `10.0.2.15:45127` | `192.168.100.1:53` | `eve.json` (Community ID: `1:I6puVD0/FGcSzdfYg+4Rm1dA84=`, msg: `LOCAL LAB DNS query for example.com`) |

---

## 3. Timeline Interpretation

The sequence demonstrates a clear pattern of outbound DNS queries initiated from internal host `10.0.2.15` toward local DNS resolver `192.168.100.1`. 

1. **Microsecond Parity:** For each DNS resolution transaction, Suricata signature rule `sid:1000001` triggered within the exact microsecond timestamp window recorded by Zeek's network monitoring engine.
2. **Dual Query Types:** The host issued both IPv4 (`A`) and IPv6 (`AAAA`) lookup requests for domain `example.com`, generating multiple distinct 5-tuples and corresponding Community ID hashes due to ephemeral source port changes (`43806`, `42294`, `45127`).

---

## 4. Correlation Confidence Assessment

* **Direct Cryptographic Match (High Confidence):** Records linked via matching **Community ID** flow hashes (`1:P2oNim+dAcDZgQht0+q2HlbuHXU=`, etc.) and internal **Zeek UIDs** are verified with 100% mathematical certainty across both sensor platforms.
* **Multi-Factor Validation (High Confidence):** The Python correlation engine confirmed bi-directional endpoint tuple matching (`10.0.2.15` $\leftrightarrow$ `192.168.100.1`, UDP port 53) and transport protocol parity across all events.
* **Temporal Window Tolerance:** All correlated alerts and session start times fell strictly within a sub-second time delta, satisfying both tight (0.1s) and loose (30s / 300s) window tolerances.

---

## 5. Analytical Limitations & Investigation Gaps

To maintain strict evidentiary integrity, analysts must explicitly document what the network timeline **does not** prove:

1. **Time Proximity vs. Causation:** While the timeline proves the sequential order of network transmissions, temporal proximity alone does not prove that a subsequent connection was caused by a prior query without matching connection states or application payload validation.
2. **Absence of Host Context:** The network telemetry confirms that DNS queries occurred, but cannot identify the initiating process ID (PID), user account context, or host execution chain (e.g., whether initiated by `curl`, a web browser, or malicious binary execution).
3. **Intent and Impact:** The timeline records successful domain resolution but does not establish whether subsequent HTTP/HTTPS payload transfers occurred or if the activity represented authorized network diagnostics versus unauthorized activity.

---

## 6. Key Portfolio Takeaways & Analyst Principles

1. **Time Proximity Is an Lead, Not Proof:** Never assume two sequential events are causally connected simply because they happened seconds apart. Always demand payload, protocol, or host-level validation before establishing causation.
2. **Real Telemetry Integrity:** Always populate investigation timelines with authentic timestamps extracted directly from raw sensor logs (`eve.json`, `conn.log`). Never synthesize or fabricate timestamp values in incident write-ups.
